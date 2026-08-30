"""Research dossier generation."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import save_artifact
from fst.db.models import SourceRecord, write_json

def create_dossier(database_path: Path, output_dir: Path, video_id: str, topic: str, sources: list[SourceRecord]) -> dict:
    key_points = [s.text for s in sources]
    dossier = {"topic": topic, "summary": f"A business documentary about {topic}.", "key_points": key_points, "sources": [s.__dict__ for s in sources]}
    path = write_json(output_dir / video_id / "dossier.json", dossier)
    save_artifact(database_path, video_id, "dossier", path)
    return dossier
