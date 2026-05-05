import os
import subprocess
import pytest


def run_sql(sql: str, dbname: str = "testdb") -> list[tuple]:
    """Execute SQL via docker exec."""
    result = subprocess.run(
        [
            "docker", "exec", "tests-postgres-test-1",
            "psql", "-U", "postgres", "-d", dbname,
            "-t", "-A", "-F", "|", "-c", sql,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"SQL failed: {sql}\nstderr: {result.stderr}")
    rows = []
    for line in result.stdout.strip().split("\n"):
        if line:
            rows.append(tuple(line.split("|")))
    return rows


def run_sql_raw(sql: str, dbname: str = "testdb") -> str:
    """Execute SQL via docker exec and return raw output."""
    result = subprocess.run(
        [
            "docker", "exec", "tests-postgres-test-1",
            "psql", "-U", "postgres", "-d", dbname,
            "-c", sql,
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"SQL failed: {sql}\nstderr: {result.stderr}")
    return result.stdout


@pytest.fixture(scope="session")
def pg():
    """Start docker-compose and provide run_sql helper."""
    compose_file = os.path.join(os.path.dirname(__file__), "docker-compose.test.yml")
    subprocess.run(
        ["docker", "compose", "-f", compose_file, "up", "-d", "--wait"],
        check=True,
    )
    yield run_sql
    subprocess.run(
        ["docker", "compose", "-f", compose_file, "down", "-v"],
        check=True,
    )


@pytest.fixture(autouse=True)
def cleanup(pg):
    """Clean up test tables and indexes after each test."""
    yield
    tables = pg("SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE 'test_%'")
    for (table,) in tables:
        pg(f'DROP TABLE IF EXISTS "{table}" CASCADE')
    indexes = pg("SELECT indexname FROM pg_indexes WHERE schemaname = 'public' AND indexname LIKE 'idx_%'")
    for (idx,) in indexes:
        pg(f'DROP INDEX IF EXISTS "{idx}" CASCADE')
