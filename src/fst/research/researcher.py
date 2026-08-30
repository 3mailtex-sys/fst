"""Research collection."""
from __future__ import annotations
from pathlib import Path
import sqlite3
from fst.db.database import connect, save_artifact
from fst.db.models import SourceRecord, write_json
from fst.research.providers import ResearchProvider

class Researcher:
    def __init__(self, database_path: Path, output_dir: Path, provider: ResearchProvider) -> None:
        self.database_path, self.output_dir, self.provider = database_path, output_dir, provider
    def run(self, video_id: str, topic: str) -> list[SourceRecord]:
        sources = self.provider.search(topic)
        with connect(self.database_path) as con:
            con.executemany("INSERT INTO sources (video_id,title,url,publisher,published_at,text,reliability) VALUES (?,?,?,?,?,?,?)", [(video_id,s.title,s.url,s.publisher,s.published_at,s.text,s.reliability) for s in sources])
        path = write_json(self.output_dir / video_id / "sources.json", sources)
        save_artifact(self.database_path, video_id, "sources", path)
        return sources
