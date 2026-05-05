def test_create_extension(pg):
    pg("CREATE EXTENSION IF NOT EXISTS pg_tokenizer CASCADE")
    pg("CREATE EXTENSION IF NOT EXISTS vchord_bm25 CASCADE")
    rows = pg("SELECT extname FROM pg_extension WHERE extname = 'vchord_bm25'")
    assert len(rows) == 1


def test_bm25_index_and_query(pg):
    pg("CREATE EXTENSION IF NOT EXISTS vector")
    pg("CREATE EXTENSION IF NOT EXISTS pg_tokenizer CASCADE")
    pg("CREATE EXTENSION IF NOT EXISTS vchord_bm25 CASCADE")
    pg("""
        CREATE TABLE test_bm25 (
            id SERIAL PRIMARY KEY,
            passage TEXT,
            embedding bm25_catalog.bm25vector
        )
    """)
    # Insert bm25vectors directly (token_id:frequency pairs)
    pg("INSERT INTO test_bm25 (passage, embedding) VALUES ('hello world', '{1:1, 2:1}'::bm25_catalog.bm25vector), ('hello postgres', '{1:1, 3:1}'::bm25_catalog.bm25vector)")
    pg("CREATE INDEX idx_bm25 ON test_bm25 USING bm25 (embedding bm25_catalog.bm25_ops)")
    rows = pg("SELECT indexname FROM pg_indexes WHERE indexname = 'idx_bm25'")
    assert len(rows) == 1
