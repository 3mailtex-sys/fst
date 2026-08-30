import sqlite3

from fst.config.settings import Settings
from fst.core.state import PHASE_1_STAGES, StageStatus
from fst.db.database import initialize_database
from fst.pipeline.runner import PipelineRunner


def test_initialize_database_creates_tables(tmp_path):
    database_path = tmp_path / "fst.sqlite3"

    initialize_database(database_path)

    with sqlite3.connect(database_path) as connection:
        table_names = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }

    assert "videos" in table_names
    assert "pipeline_stages" in table_names


def test_pipeline_runner_creates_job_with_pending_stages(tmp_path):
    settings = Settings(
        database_path=tmp_path / "fst.sqlite3",
        data_dir=tmp_path / "data",
    )
    runner = PipelineRunner(settings)

    video_id = runner.create_job("Example topic")

    with sqlite3.connect(settings.database_path) as connection:
        video = connection.execute(
            "SELECT video_id, topic, status FROM videos WHERE video_id = ?",
            (video_id,),
        ).fetchone()
        stages = connection.execute(
            "SELECT stage_name, status FROM pipeline_stages WHERE video_id = ? ORDER BY stage_name",
            (video_id,),
        ).fetchall()

    assert video == (video_id, "Example topic", StageStatus.PENDING.value)
    assert len(stages) == len(PHASE_1_STAGES)
    assert {stage_name for stage_name, _ in stages} == set(PHASE_1_STAGES)
    assert {status for _, status in stages} == {StageStatus.PENDING.value}
