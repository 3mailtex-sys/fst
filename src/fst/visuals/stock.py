"""Free/local visual provider."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import save_artifact
from fst.db.models import Scene
from fst.visuals.charts import write_svg_card

class VisualProvider:
    def prepare(self, scene: Scene, path: Path) -> Path: raise NotImplementedError

class LocalSVGVisualProvider(VisualProvider):
    def prepare(self, scene: Scene, path: Path) -> Path:
        return write_svg_card(path, f"Scene {scene.number}", scene.visual)

def collect_visuals(database_path: Path, output_dir: Path, video_id: str, scenes: list[Scene], provider: VisualProvider | None = None) -> list[Path]:
    provider = provider or LocalSVGVisualProvider(); paths=[]
    for scene in scenes:
        paths.append(provider.prepare(scene, output_dir / video_id / "visuals" / f"scene_{scene.number:02d}.svg"))
    save_artifact(database_path, video_id, "visuals", output_dir / video_id / "visuals")
    return paths
