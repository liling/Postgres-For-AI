def test_create_extension(pg):
    pg("CREATE EXTENSION IF NOT EXISTS pg_stat_statements")
    rows = pg("SELECT extname FROM pg_extension WHERE extname = 'pg_stat_statements'")
    assert len(rows) == 1


def test_query_stats(pg):
    pg("CREATE EXTENSION IF NOT EXISTS pg_stat_statements")
    pg("SELECT 42")
    rows = pg("SELECT count(*) FROM pg_stat_statements")
    assert int(rows[0][0]) >= 1
