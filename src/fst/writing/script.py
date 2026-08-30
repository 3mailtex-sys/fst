"""Documentary script generation from verified claims."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import save_artifact
from fst.db.models import ClaimRecord, write_json

def generate_script(database_path: Path, output_dir: Path, video_id: str, topic: str, claims: list[ClaimRecord]) -> dict:
    supported = [c.text for c in claims if c.status == "supported"]
    if not supported: raise ValueError("No supported claims available for script generation")
    sections = [
        {"title": "Hook", "narration": f"This is the story of {topic}, and what it reveals about business strategy."},
        {"title": "Context", "narration": supported[0]},
        {"title": "Turning point", "narration": supported[min(1, len(supported)-1)]},
        {"title": "Lessons", "narration": supported[-1]},
        {"title": "Close", "narration": "The bigger lesson is simple: markets change faster than comfortable companies expect."},
    ]
    script = {"topic": topic, "sections": sections}
    path = write_json(output_dir / video_id / "script.json", script)
    save_artifact(database_path, video_id, "script", path)
    return script
