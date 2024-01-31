import duckdb
import bso_coverage_tools as bct
import os


def test_mother_duck():
    error = "NOT CONNECTED"
    with duckdb.connect(f"md:?motherduck_token={os.getenv('MD_TOKEN')}") as con:
        error = "CONNECTED"
        con.sql(
            "UPDATE openalex_2021 SET  coverage = STRUCT_PACK(last_error := 'ALEX_DOI_NOT_FOUND', last_error_data := coverage.last_error_data, last_state := 'UNDEFINED') WHERE doi IS NULL"
        )
    return error


def bso_apply_coverage(row):
    res = bct.analyse_from_openalex_work(row)
    print(res)
    return res


def bso_task_coverage(n_rows=100):
    print(f"[BSO] Start applying coverage with n={n_rows}")
    with duckdb.connect(f"md:?motherduck_token={os.getenv('MD_TOKEN')}") as con:
        df = con.sql(f"SELECT * FROM openalex_2021 WHERE doi IS NOT NULL ORDER BY id LIMIT {n_rows}").df()
        print(f"[BSO] Start analyze of {df.size} entries")
        res_df = df.apply(bso_apply_coverage, axis=1)
