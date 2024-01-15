import duckdb
import os


def test_mother_duck():
    error = "NOT CONNECTED"
    with duckdb.connect(f"md:?motherduck_token={os.getenv('MD_TOKEN')}") as con:
        error = "CONNECTED"
        con.sql("UPDATE openalex_2021 set coverage.last_state = 'UNDEFINED' WHERE doi IS NULL")
        con.sql("UPDATE openalex_2021 set coverage.last_error = 'ALEX_DOI_NOT_FOUND' WHERE doi IS NULL")
    return error
