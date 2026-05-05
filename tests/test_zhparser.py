def test_create_extension(pg):
    pg("CREATE EXTENSION IF NOT EXISTS zhparser")
    rows = pg("SELECT extname FROM pg_extension WHERE extname = 'zhparser'")
    assert len(rows) == 1


def test_chinese_tokenization(pg):
    pg("CREATE EXTENSION IF NOT EXISTS zhparser")
    pg("CREATE TEXT SEARCH CONFIGURATION test_zh (PARSER = zhparser)")
    pg("ALTER TEXT SEARCH CONFIGURATION test_zh ADD MAPPING FOR n,v,a,i,e,l WITH simple")
    rows = pg("SELECT to_tsvector('test_zh', '中文分词测试')::text")
    assert len(rows) == 1
    assert len(rows[0][0]) > 0
    pg("DROP TEXT SEARCH CONFIGURATION IF EXISTS test_zh CASCADE")
