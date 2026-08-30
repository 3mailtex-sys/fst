"""Application settings loaded from environment variables."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os
_ALLOWED_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_MODES = {"development", "production"}

@dataclass(frozen=True)
class Settings:
    database_path: Path = Path("data/working/fst.sqlite3")
    data_dir: Path = Path("data")
    log_level: str = "INFO"
    mode: str = "development"
    gemini_api_key: str | None = None
    youtube_client_secrets: Path | None = None
    youtube_token_path: Path = Path("data/working/youtube_token.json")
    piper_executable: str = "piper"
    ffmpeg_executable: str = "ffmpeg"
    ffprobe_executable: str = "ffprobe"

    @property
    def output_dir(self) -> Path: return self.data_dir / "output"
    @property
    def working_dir(self) -> Path: return self.data_dir / "working"
    @property
    def cache_dir(self) -> Path: return self.data_dir / "cache"

    @classmethod
    def from_env(cls) -> "Settings":
        secrets = os.getenv("YOUTUBE_CLIENT_SECRETS")
        return cls(
            database_path=Path(os.getenv("FST_DATABASE_PATH", "data/working/fst.sqlite3")),
            data_dir=Path(os.getenv("FST_DATA_DIR", "data")),
            log_level=os.getenv("FST_LOG_LEVEL", "INFO").upper(),
            mode=os.getenv("FST_MODE", "development").lower(),
            gemini_api_key=os.getenv("GEMINI_API_KEY") or None,
            youtube_client_secrets=Path(secrets) if secrets else None,
            youtube_token_path=Path(os.getenv("YOUTUBE_TOKEN_PATH", "data/working/youtube_token.json")),
            piper_executable=os.getenv("PIPER_EXECUTABLE", "piper"),
            ffmpeg_executable=os.getenv("FFMPEG_EXECUTABLE", "ffmpeg"),
            ffprobe_executable=os.getenv("FFPROBE_EXECUTABLE", "ffprobe"),
        )

    def validate(self) -> None:
        if self.log_level not in _ALLOWED_LOG_LEVELS:
            raise ValueError(f"FST_LOG_LEVEL must be one of: {', '.join(sorted(_ALLOWED_LOG_LEVELS))}")
        if self.mode not in _MODES:
            raise ValueError("FST_MODE must be development or production")
        for directory in (self.data_dir, self.output_dir, self.working_dir, self.cache_dir, self.database_path.parent, self.youtube_token_path.parent):
            directory.mkdir(parents=True, exist_ok=True)
