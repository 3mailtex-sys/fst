"""YouTube analytics adapters with free mock development provider."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import connect, save_artifact
from fst.db.models import write_json

class AnalyticsProvider:
    def collect(self, youtube_id: str) -> dict: raise NotImplementedError

class MockYouTubeAnalyticsProvider(AnalyticsProvider):
    def collect(self, youtube_id: str) -> dict:
        return {"youtube_id": youtube_id, "views": 0, "watch_time_minutes": 0.0, "ctr": 0.0}

def collect_analytics(database_path: Path, output_dir: Path, video_id: str, youtube_id: str, provider: AnalyticsProvider | None = None) -> dict:
    data=(provider or MockYouTubeAnalyticsProvider()).collect(youtube_id)
    with connect(database_path) as con: con.execute("INSERT INTO analytics (video_id,views,watch_time_minutes,ctr) VALUES (?,?,?,?)", (video_id, data["views"], data["watch_time_minutes"], data["ctr"]))
    path=write_json(output_dir / video_id / "analytics.json", data); save_artifact(database_path, video_id, "analytics", path); return data
