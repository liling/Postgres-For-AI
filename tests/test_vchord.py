def test_vchord_index_and_query(pg):
    pg("CREATE EXTENSION IF NOT EXISTS vector")
    pg("CREATE EXTENSION IF NOT EXISTS vchord")
    pg("CREATE TABLE test_vchord (id bigserial PRIMARY KEY, v vector(3))")
    pg("INSERT INTO test_vchord (v) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[7,8,9]')")
    pg("CREATE INDEX idx_vchord ON test_vchord USING vchordrq (v vector_cosine_ops)")
    rows = pg("SELECT indexname FROM pg_indexes WHERE indexname = 'idx_vchord'")
    assert len(rows) == 1
    rows = pg("SELECT id FROM test_vchord ORDER BY v <=> '[1,2,3]' LIMIT 1")
    assert rows[0][0] == "1"
