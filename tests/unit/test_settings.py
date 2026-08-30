from pathlib import Path

import pytest

from fst.config.settings import Settings


def test_settings_from_env_uses_defaults(monkeypatch):
    monkeypatch.delenv("FST_DATABASE_PATH", raising=False)
    monkeypatch.delenv("FST_DATA_DIR", raising=False)
    monkeypatch.delenv("FST_LOG_LEVEL", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    settings = Settings.from_env()

    assert settings.database_path == Path("data/working/fst.sqlite3")
    assert settings.data_dir == Path("data")
    assert settings.log_level == "INFO"
    assert settings.gemini_api_key is None


def test_settings_validate_rejects_invalid_log_level(tmp_path):
    settings = Settings(
        database_path=tmp_path / "fst.sqlite3",
        data_dir=tmp_path,
        log_level="LOUD",
    )

    with pytest.raises(ValueError, match="FST_LOG_LEVEL"):
        settings.validate()


def test_settings_validate_creates_directories(tmp_path):
    settings = Settings(
        database_path=tmp_path / "nested" / "fst.sqlite3",
        data_dir=tmp_path / "data",
    )

    settings.validate()

    assert settings.data_dir.exists()
    assert settings.database_path.parent.exists()
