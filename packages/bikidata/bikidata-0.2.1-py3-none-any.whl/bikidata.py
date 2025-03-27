import sys, logging, gzip, re, os, tarfile
from typing import Union
from functools import lru_cache
import numpy as np
import duckdb
import xxhash

log = logging.getLogger("bikidata")
handler = logging.StreamHandler()
log.addHandler(handler)
log.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(levelname)-9s %(name)s %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)

DB_PATH = os.getenv("BIKIDATA_DB", "bikidata.duckdb")
DB = duckdb.connect(DB_PATH)


def literal_to_parts(literal: str):
    literal_value = language = datatype = None
    if literal.startswith('"'):
        end_index = literal.rfind('"')
        if end_index > 0:
            literal_value = literal[1:end_index]
            remainder = literal[end_index + 1 :].strip()
            language = datatype = None
            if remainder.startswith("@"):
                language = remainder[1:]
                datatype = None
            elif remainder.startswith("^^"):
                datatype = remainder[2:]
                language = None
    return literal_value, language, datatype


def decode_unicode_escapes(s):
    # See: https://www.w3.org/TR/n-triples/#grammar-production-UCHAR
    unicode_escape_pattern_u = re.compile(
        r"\\u([0-9a-fA-F]{4})"
    )  # \uXXXX (4 hex digits)
    unicode_escape_pattern_U = re.compile(
        r"\\U([0-9a-fA-F]{8})"
    )  # \UXXXXXXXX (8 hex digits)

    def replace_unicode_escape_u(match):
        hex_value = match.group(1)
        return chr(
            int(hex_value, 16)
        )  # Convert hex to integer, then to Unicode character

    def replace_unicode_escape_U(match):
        hex_value = match.group(1)
        return chr(
            int(hex_value, 16)
        )  # Convert hex to integer, then to Unicode character

    s = unicode_escape_pattern_U.sub(replace_unicode_escape_U, s)
    s = unicode_escape_pattern_u.sub(replace_unicode_escape_u, s)

    return s


class StringParamException(Exception):
    pass


def read_nt(triplefile_paths: list):
    if not type(triplefile_paths) == list:
        raise StringParamException(
            "triplefile_paths must be a list of paths to n-triple files, or file-like objects"
        )
    for triplefile_path in triplefile_paths:
        if isinstance(triplefile_path, (str, bytes, os.PathLike)):
            if triplefile_path.endswith(".gz"):
                thefile = gzip.open(triplefile_path, "rb")
            else:
                thefile = open(triplefile_path, "rb")
        elif hasattr(triplefile_path, "read"):
            thefile = triplefile_path
        else:
            raise StringParamException(
                "Each path in triplefile_paths must be a string, bytes, os.PathLike object, or a file-like object"
            )

        g = ""
        for line in thefile:
            if not line.endswith(b" .\n"):
                if line.endswith(b" {\n") and line.startswith(b"<"):
                    # Cater for .trig files by looking for a pattern like
                    # ^<IRI> {\n
                    parts = line.decode("utf8").split(" ")
                    if len(parts) == 2:
                        g = parts[0]
                        continue
                else:
                    continue
            line = decode_unicode_escapes(line.decode("utf8"))
            line = line.strip()
            line = line[:-2]
            parts = line.split(" ")
            if len(parts) > 2:
                s = parts[0]
                p = parts[1]
                o = " ".join(parts[2:])

            if not (s.startswith("<") and s.endswith(">")):
                continue
            if not (p.startswith("<") and p.endswith(">")):
                continue

            yield s, p, o, g


def H(v: str):
    return xxhash.xxh64_hexdigest(v).upper()


def build_bikidata(
    triplefile_paths: list,
):
    if len(triplefile_paths) > 0:
        log.debug(f"Building Bikidata index with {triplefile_paths}")
        iterator = read_nt(triplefile_paths)
    else:
        log.error("No triples to index, triplefile_paths not given")
        return

    TRIPLE_PATH = os.getenv("BIKIDATA_TRIPLE_PATH", "triples")
    MAP_PATH = os.getenv("BIKIDATA_MAP_PATH", "maps")

    count = 0

    TRIPLE_OUT_FILE = open(TRIPLE_PATH, "w")
    MAP_OUT_FILE = open(MAP_PATH, "w")

    for s, p, o, g in iterator:
        ss = H(s)
        pp = H(p)
        oo = H(o)
        gg = H(g)
        TRIPLE_OUT_FILE.write(f"{ss}\t{pp}\t{oo}\t{gg}\n")
        MAP_OUT_FILE.write(f"{ss}\t|\t{s}\n")
        MAP_OUT_FILE.write(f"{pp}\t|\t{p}\n")
        MAP_OUT_FILE.write(f"{oo}\t|\t{o}\n")

    TRIPLE_OUT_FILE.close()
    MAP_OUT_FILE.close()

    DB_SCHEMA = """
    create table if not exists literals (hash ubigint, value varchar);
    create table if not exists iris (hash ubigint, value varchar);
    create table if not exists triples (s ubigint, p ubigint, o ubigint, g ubigint);    
    """

    DB = duckdb.connect(DB_PATH)
    DB.execute(DB_SCHEMA)
    DB.execute(
        rf"insert into triples(s,p,o) select ('0x' || column0).lower()::ubigint, ('0x' || column1).lower()::ubigint, ('0x' || column2).lower()::ubigint from read_csv('{TRIPLE_PATH}', delim='\t', header=false)"
    )
    DB.execute(
        rf"""insert into literals select ('0x' || column0).lower()::ubigint, ANY_VALUE(column1) from read_csv('{MAP_PATH}', delim='\t|\t', header=false, max_line_size=5100000) where substr(column1, 1, 1) = '"' group by column0 order by column0 """
    )

    DB.execute(
        rf"""insert into iris select ('0x' || column0).lower()::ubigint, ANY_VALUE(column1) from read_csv('{MAP_PATH}', delim='\t|\t', header=false, max_line_size=5100000) where substr(column1, 1, 1) != '"'  group by column0 order by column0 """
    )
    DB.execute("pragma create_fts_index('literals', 'hash', 'value')")
    DB.commit()


def extract_files(filepath: str):
    filepaths = []
    with tarfile.open(filepath, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.endswith(".nt"):
                _, filename = os.path.split(member.name)
                open(filename, "wb").write(tar.extractfile(member).read())
                filepaths.append(filename)
    return filepaths


def q_to_sql(query: dict):
    p = query.get("p", "id")
    o = query.get("o", "")
    pp = xxhash.xxh64_hexdigest(p).lower()
    oo = xxhash.xxh64_hexdigest(o).lower()
    if p == "id":
        return f"(select distinct s from triples where s = '0x{oo}'::ubigint)"

    elif p == "fts":
        return f"""
(with scored as (
    select *, fts_main_literals.match_bm25(hash, '{o}') AS score 
    from literals
)
select distinct T.s from triples T join (select * from scored where score is not null) S 
on S.hash = T.o)"""
    elif p[0] == "<" and p[-1] == ">":
        if o:
            return f"(select distinct s from triples where p = '0x{pp}'::ubigint and o = '0x{oo}'::ubigint)"

        else:
            return f"(select distinct s from triples where p = '0x{pp}'::ubigint)"


def query(opts):
    try:
        size = int(opts.get("size", 999))
    except:
        size = 999
    try:
        start = int(opts.get("start", 0))
    except:
        start = 0
    queries = []
    for query in opts.get("filters", []):
        op = query.get("op", "should")
        if not queries:
            queries = [q_to_sql(query)]
        else:
            if op in ("should", "or"):
                queries.append(" UNION " + q_to_sql(query))
            elif op in ("must", "and"):
                queries.append(" INTERSECT " + q_to_sql(query))
            elif op == "not":
                queries.append(" INTERSECT " + q_to_sql(query))

    # calc the total size based on unique s
    queries_joined = "\n".join(queries)
    subjects = DB.execute(queries_joined).df()
    total = subjects.shape[0]

    tofetch = set()

    # check for aggregates
    aggregates = {}
    for agg in opts.get("aggregates", []):
        agg_o = xxhash.xxh64_hexdigest(agg).lower()

        tmp = f"select count(s) as count, o, I.value as val from triples T join iris I on T.o = I.hash where p = '0x{agg_o}'::ubigint and s in ({queries_joined}) group by o, I.value"
        aggs = DB.execute(tmp).df()
        aggregates[agg] = aggs

    results = {}

    # get the batch based on size and start
    wanted = subjects[start : start + size]
    if wanted.shape[0] > 0:
        s_ids = ", ".join([str(row["s"]) for index, row in wanted.iterrows()])
        triples = DB.execute(
            f"select distinct s,p,o from triples  where s in ({s_ids})"
        ).df()

        for index, row in triples.iterrows():
            r_s = row.get("s")
            r_p = row.get("p")
            r_o = row.get("o")
            tofetch.add(r_s)
            tofetch.add(r_p)
            tofetch.add(r_o)
            results.setdefault(r_s, {}).setdefault(r_p, []).append(r_o)

        tofetch = ", ".join([str(x) for x in tofetch])

        HV = dict(
            [
                (hash, value)
                for hash, value in DB.execute(
                    f"(select hash, value from iris where hash in ({tofetch})) union (select hash, value from literals where hash in ({tofetch}))"
                ).fetchall()
            ]
        )

    results_mapped = {}
    for entity, fields in results.items():
        for field, vals in fields.items():
            for val in vals:
                results_mapped.setdefault(HV.get(entity), {}).setdefault(
                    HV.get(field), []
                ).append(HV.get(val))

    aggregates_mapped = {}
    for agg, aggs in aggregates.items():
        aggregates_mapped[agg] = []
        for _, row in aggs.iterrows():
            aggregates_mapped[agg].append((row["count"], row["val"]))

    back = {"results": results_mapped, "total": total, "size": size, "start": start}
    if aggregates:
        back["aggregates"] = aggregates_mapped

    return back


if __name__ == "__main__":

    TARGZ_PATH = os.getenv("TARGZ_PATH")
    if TARGZ_PATH:
        filepaths = extract_files(TARGZ_PATH)
        build_bikidata(filepaths)
    else:
        if sys.argv[1].endswith(".gz"):
            build_bikidata([sys.argv[1]])
        else:
            filepaths = [
                os.path.join(sys.argv[1], x)
                for x in os.listdir(sys.argv[1])
                if x.lower().endswith(".nt")
            ]
            build_bikidata(filepaths)
