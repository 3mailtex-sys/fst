"""Simple local learning loop."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import connect, save_artifact
from fst.db.models import write_json

def update_learning(database_path: Path, output_dir: Path, video_id: str, analytics: dict) -> dict:
    insight={"video_id": video_id, "note": "Development analytics recorded; future scoring can prefer topics with better watch time once real data exists."}
    with connect(database_path) as con: con.execute("INSERT INTO learning_insights (note) VALUES (?)", (insight["note"],))
    path=write_json(output_dir / video_id / "learning.json", insight); save_artifact(database_path, video_id, "learning", path); return insight
