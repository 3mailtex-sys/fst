"""Storyboard generation."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import save_artifact
from fst.db.models import Scene, write_json

def generate_storyboard(database_path: Path, output_dir: Path, video_id: str, script: dict) -> list[Scene]:
    scenes = [Scene(i, s["narration"], f"Clean documentary visual for: {s['title']}", max(4.0, len(s["narration"].split()) / 2.5)) for i, s in enumerate(script["sections"], 1)]
    path = write_json(output_dir / video_id / "storyboard.json", scenes)
    save_artifact(database_path, video_id, "storyboard", path)
    return scenes
