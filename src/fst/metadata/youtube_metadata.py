"""YouTube metadata generation."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import save_artifact
from fst.db.models import write_json

def generate_metadata(database_path: Path, output_dir: Path, video_id: str, topic: str, script: dict) -> dict:
    metadata={"title": f"{topic}: The Business Story", "description": f"A free/local generated documentary package about {topic}. Sources and claims are checked in the local dossier.", "tags": ["business", "documentary", "company"], "chapters": [f"0:00 {s['title']}" for s in script.get("sections", [])], "privacy_status": "private"}
    path=write_json(output_dir / video_id / "youtube_metadata.json", metadata); save_artifact(database_path, video_id, "youtube_metadata", path); return metadata
