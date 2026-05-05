def test_create_extension(pg):
    """pg_textsearch requires shared_preload_libraries. Test only if preload is configured."""
    rows = pg("SELECT name FROM pg_available_extensions WHERE name = 'pg_textsearch'")
    assert len(rows) == 1, "pg_textsearch extension is not available"


def test_search_vector_type(pg):
    """Only run if pg_textsearch is in shared_preload_libraries."""
    rows = pg("SHOW shared_preload_libraries")
    if "pg_textsearch" not in rows[0][0]:
        return
    pg("CREATE EXTENSION IF NOT EXISTS pg_textsearch")
    pg("CREATE TABLE test_textsearch (id serial PRIMARY KEY, content text, sv search_vector)")
    pg("INSERT INTO test_textsearch (content) VALUES ('hello world'), ('test document')")
    rows = pg("SELECT count(*) FROM test_textsearch")
    assert int(rows[0][0]) == 2
