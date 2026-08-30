"""YouTube publishing adapters. Development mode never publishes publicly."""
from __future__ import annotations
from pathlib import Path
import uuid
from fst.db.database import connect, save_artifact
from fst.db.models import write_json

class PublishingProvider:
    def upload(self, video_path: Path, metadata: dict) -> str: raise NotImplementedError

class MockYouTubePublishingProvider(PublishingProvider):
    def upload(self, video_path: Path, metadata: dict) -> str:
        return f"mock-youtube-{uuid.uuid4()}"

def upload_video(database_path: Path, output_dir: Path, video_id: str, video_path: Path, metadata: dict, provider: PublishingProvider | None = None) -> str:
    provider = provider or MockYouTubePublishingProvider(); youtube_id = provider.upload(video_path, metadata)
    with connect(database_path) as con: con.execute("UPDATE videos SET youtube_id=?, status='uploaded' WHERE video_id=?", (youtube_id, video_id))
    path=write_json(output_dir / video_id / "upload.json", {"youtube_id": youtube_id, "privacy_status": metadata.get("privacy_status", "private")})
    save_artifact(database_path, video_id, "upload", path); return youtube_id
