def test_create_extension(pg):
    pg("CREATE EXTENSION IF NOT EXISTS age")
    rows = pg("SELECT extname FROM pg_extension WHERE extname = 'age'")
    assert len(rows) == 1


def test_age_load(pg):
    """Verify AGE module can be loaded. Graph operations may have PG18 compat issues."""
    pg("CREATE EXTENSION IF NOT EXISTS age")
    pg("LOAD 'age'")
    rows = pg("SELECT extname FROM pg_extension WHERE extname = 'age'")
    assert len(rows) == 1
