"""SQLite database setup and helpers."""
from __future__ import annotations
from pathlib import Path
import sqlite3

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS videos (
 id INTEGER PRIMARY KEY AUTOINCREMENT, video_id TEXT NOT NULL UNIQUE, topic TEXT,
 status TEXT NOT NULL DEFAULT 'pending', youtube_id TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS pipeline_stages (
 id INTEGER PRIMARY KEY AUTOINCREMENT, video_id TEXT NOT NULL, stage_name TEXT NOT NULL, status TEXT NOT NULL,
 output_path TEXT, error_message TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE(video_id, stage_name),
 FOREIGN KEY(video_id) REFERENCES videos(video_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS topics (
 id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL UNIQUE, description TEXT NOT NULL DEFAULT '', score REAL NOT NULL DEFAULT 0,
 status TEXT NOT NULL DEFAULT 'candidate', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS sources (
 id INTEGER PRIMARY KEY AUTOINCREMENT, video_id TEXT NOT NULL, title TEXT NOT NULL, url TEXT NOT NULL, publisher TEXT,
 published_at TEXT, text TEXT NOT NULL, reliability REAL NOT NULL DEFAULT 0.5, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(video_id) REFERENCES videos(video_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS claims (
 id INTEGER PRIMARY KEY AUTOINCREMENT, video_id TEXT NOT NULL, text TEXT NOT NULL, status TEXT NOT NULL, source_ids TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(video_id) REFERENCES videos(video_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS artifacts (
 id INTEGER PRIMARY KEY AUTOINCREMENT, video_id TEXT NOT NULL, kind TEXT NOT NULL, path TEXT NOT NULL, metadata TEXT NOT NULL DEFAULT '{}',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE(video_id, kind), FOREIGN KEY(video_id) REFERENCES videos(video_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS analytics (
 id INTEGER PRIMARY KEY AUTOINCREMENT, video_id TEXT NOT NULL, views INTEGER NOT NULL DEFAULT 0, watch_time_minutes REAL NOT NULL DEFAULT 0,
 ctr REAL NOT NULL DEFAULT 0, collected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(video_id) REFERENCES videos(video_id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS learning_insights (
 id INTEGER PRIMARY KEY AUTOINCREMENT, note TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
"""

def connect(database_path: Path) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(database_path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

def initialize_database(database_path: Path) -> None:
    with connect(database_path) as con:
        con.executescript(SCHEMA_SQL)

def save_artifact(database_path: Path, video_id: str, kind: str, path: Path, metadata: str = "{}") -> None:
    with connect(database_path) as con:
        con.execute("INSERT OR REPLACE INTO artifacts (video_id, kind, path, metadata) VALUES (?, ?, ?, ?)", (video_id, kind, str(path), metadata))

def get_artifact(database_path: Path, video_id: str, kind: str) -> Path | None:
    with connect(database_path) as con:
        row = con.execute("SELECT path FROM artifacts WHERE video_id=? AND kind=?", (video_id, kind)).fetchone()
    return Path(row["path"]) if row else None
