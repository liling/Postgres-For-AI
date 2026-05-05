def test_shared_preload_libraries(pg):
    rows = pg("SHOW shared_preload_libraries")
    libs = rows[0][0]
    expected = ["vchord", "vchord_bm25", "pg_tokenizer", "pg_stat_statements"]
    for lib in expected:
        assert lib in libs, f"Missing library: {lib}"
