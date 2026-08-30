"""Free SVG chart/graphic generation."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import save_artifact

def write_svg_card(path: Path, title: str, body: str, bg: str = "#111827") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    esc=lambda s: s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    path.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720"><rect width="100%" height="100%" fill="{bg}"/><text x="80" y="170" fill="#f9fafb" font-family="Arial" font-size="58" font-weight="700">{esc(title[:34])}</text><text x="80" y="270" fill="#d1d5db" font-family="Arial" font-size="34">{esc(body[:70])}</text><line x1="80" y1="560" x2="1120" y2="560" stroke="#38bdf8" stroke-width="8"/></svg>''')
    return path

def generate_charts(database_path: Path, output_dir: Path, video_id: str, topic: str) -> list[Path]:
    p = write_svg_card(output_dir / video_id / "visuals" / "chart_01.svg", "Business Lessons", topic)
    save_artifact(database_path, video_id, "charts", p.parent)
    return [p]
