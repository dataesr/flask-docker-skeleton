import duckdb
import os


def test_mother_duck():
    error = "NOT CONNECTED"
    with duckdb.connect(f"md:?motherduck_token={os.getenv('MD_TOKEN')}") as con:
        error = "CONNECTED"
        con.sql(
            "UPDATE openalex_2021 SET  coverage = STRUCT_PACK(last_error := 'ALEX_DOI_NOT_FOUND', last_error_data := coverage.last_error_data, last_state := 'UNDEFINED') WHERE doi IS NULL"
        )
    return error
