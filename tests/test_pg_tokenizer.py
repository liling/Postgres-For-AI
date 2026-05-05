def test_create_extension(pg):
    pg("CREATE EXTENSION IF NOT EXISTS pg_tokenizer")
    rows = pg("SELECT extname FROM pg_extension WHERE extname = 'pg_tokenizer'")
    assert len(rows) == 1
