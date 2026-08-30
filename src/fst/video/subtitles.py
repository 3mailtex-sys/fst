"""Subtitle generation."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import save_artifact
from fst.db.models import Scene

def _ts(seconds: float) -> str:
    h=int(seconds//3600); m=int(seconds%3600//60); s=int(seconds%60); ms=int((seconds-int(seconds))*1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def generate_subtitles(database_path: Path, output_dir: Path, video_id: str, scenes: list[Scene]) -> Path:
    t=0.0; blocks=[]
    for i, scene in enumerate(scenes, 1):
        start=t; t += scene.duration_seconds
        blocks.append(f"{i}\n{_ts(start)} --> {_ts(t)}\n{scene.narration}\n")
    path=output_dir / video_id / "subtitles.srt"; path.parent.mkdir(parents=True, exist_ok=True); path.write_text("\n".join(blocks))
    save_artifact(database_path, video_id, "subtitles", path); return path
