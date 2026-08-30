"""Free/local thumbnail generation as SVG."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import save_artifact
from fst.visuals.charts import write_svg_card

def generate_thumbnail(database_path: Path, output_dir: Path, video_id: str, topic: str) -> Path:
    path = write_svg_card(output_dir / video_id / "thumbnail.svg", topic[:34], "Business Documentary", "#0f172a")
    save_artifact(database_path, video_id, "thumbnail", path); return path
