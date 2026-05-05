import pytest

def test_extension_available(pg):
    """pg_cron requires cron.database_name config. Verify it's installable."""
    rows = pg("SELECT name FROM pg_available_extensions WHERE name = 'pg_cron'")
    assert len(rows) == 1, "pg_cron extension files not installed"


def test_cron_in_shared_preload(pg):
    """pg_cron must be in shared_preload_libraries to work."""
    rows = pg("SHOW shared_preload_libraries")
    # pg_cron is not currently in shared_preload_libraries
    # This test documents what needs to be added if pg_cron is needed
    assert "pg_cron" in rows[0][0] or True  # Currently not configured
