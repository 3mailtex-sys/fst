"""Automated quality checks."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import connect, save_artifact
from fst.db.models import write_json
REQUIRED=("dossier","claims","script","storyboard","voiceover","visuals","subtitles","final_video","thumbnail","youtube_metadata")

def run_quality_checks(database_path: Path, output_dir: Path, video_id: str) -> dict:
    with connect(database_path) as con:
        artifacts={r["kind"]: r["path"] for r in con.execute("SELECT kind,path FROM artifacts WHERE video_id=?", (video_id,))}
        unsupported=con.execute("SELECT COUNT(*) FROM claims WHERE video_id=? AND status='unsupported'", (video_id,)).fetchone()[0]
    missing=[k for k in REQUIRED if k not in artifacts or not Path(artifacts[k]).exists()]
    report={"passed": not missing and unsupported == 0, "missing_artifacts": missing, "unsupported_claims": unsupported}
    path=write_json(output_dir / video_id / "quality_report.json", report); save_artifact(database_path, video_id, "quality_report", path); return report
