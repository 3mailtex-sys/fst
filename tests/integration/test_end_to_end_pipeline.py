import sqlite3
from pathlib import Path

from fst.config.settings import Settings
from fst.core.state import PHASE_1_STAGES, StageStatus
from fst.pipeline.runner import PipelineRunner


def test_development_pipeline_runs_end_to_end(tmp_path):
    settings = Settings(database_path=tmp_path / "fst.sqlite3", data_dir=tmp_path / "data")
    video_id = PipelineRunner(settings).run_all("Test Company Story")

    output_dir = settings.output_dir / video_id
    assert (output_dir / "dossier.json").exists()
    assert (output_dir / "claims.json").exists()
    assert (output_dir / "script.json").exists()
    assert (output_dir / "storyboard.json").exists()
    assert (output_dir / "subtitles.srt").exists()
    assert (output_dir / "final_video.txt").exists()
    assert (output_dir / "thumbnail.svg").exists()
    assert (output_dir / "youtube_metadata.json").exists()
    assert (output_dir / "quality_report.json").exists()
    assert (output_dir / "upload.json").exists()
    assert (output_dir / "analytics.json").exists()
    assert (output_dir / "learning.json").exists()

    with sqlite3.connect(settings.database_path) as connection:
        statuses = {
            row[0]
            for row in connection.execute(
                "SELECT status FROM pipeline_stages WHERE video_id = ?",
                (video_id,),
            )
        }
        video_status = connection.execute(
            "SELECT status FROM videos WHERE video_id = ?",
            (video_id,),
        ).fetchone()[0]

    assert statuses == {StageStatus.SUCCEEDED.value}
    assert video_status == "complete"


def test_stage_list_prevents_duplicate_stage_names():
    assert len(PHASE_1_STAGES) == len(set(PHASE_1_STAGES))
