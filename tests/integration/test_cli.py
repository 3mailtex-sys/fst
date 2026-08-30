import os
import subprocess
import sys


def test_cli_init_db_creates_database(tmp_path):
    database_path = tmp_path / "fst.sqlite3"
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    env["FST_DATABASE_PATH"] = str(database_path)
    env["FST_DATA_DIR"] = str(tmp_path / "data")

    result = subprocess.run(
        [sys.executable, "-m", "fst.main", "init-db"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )

    assert database_path.exists()
    assert "Initialized database" in result.stdout
