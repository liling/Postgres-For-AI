def test_create_extension(pg):
    pg("CREATE EXTENSION IF NOT EXISTS vector")
    rows = pg("SELECT extname FROM pg_extension WHERE extname = 'vector'")
    assert len(rows) == 1
    assert rows[0][0] == "vector"


def test_vector_type_and_distance(pg):
    pg("CREATE EXTENSION IF NOT EXISTS vector")
    pg("CREATE TABLE test_vectors (id serial PRIMARY KEY, v vector(3))")
    pg("INSERT INTO test_vectors (v) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[1,0,0]')")
    rows = pg("SELECT (v <-> '[1,2,3]')::text FROM test_vectors ORDER BY v <-> '[1,2,3]'")
    assert len(rows) == 3
    assert float(rows[0][0]) == 0.0


def test_vector_cosine_search(pg):
    pg("CREATE EXTENSION IF NOT EXISTS vector")
    pg("CREATE TABLE test_cosine (id serial PRIMARY KEY, v vector(3))")
    pg("INSERT INTO test_cosine (v) VALUES ('[1,0,0]'), ('[0,1,0]'), ('[0,0,1]')")
    rows = pg("SELECT id FROM test_cosine ORDER BY v <=> '[1,0,0]' LIMIT 1")
    assert rows[0][0] == "1"
