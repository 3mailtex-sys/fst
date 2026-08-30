"""Resumable free/local pipeline runner."""
from __future__ import annotations
import logging, uuid
from pathlib import Path
from fst.audio.tts import generate_voiceover
from fst.config.settings import Settings
from fst.core.state import StageStatus
from fst.db.database import connect, get_artifact, initialize_database
from fst.fact_checking.claims import extract_claims
from fst.fact_checking.verifier import verify_claims
from fst.learning.optimizer import update_learning
from fst.metadata.thumbnail import generate_thumbnail
from fst.metadata.youtube_metadata import generate_metadata
from fst.pipeline.stages import STAGES
from fst.publishing.analytics import collect_analytics
from fst.publishing.youtube_upload import upload_video
from fst.quality.checks import run_quality_checks
from fst.research.dossier import create_dossier
from fst.research.providers import LocalFixtureResearchProvider
from fst.research.researcher import Researcher
from fst.topics.discovery import LocalTopicDiscoveryProvider
from fst.topics.scoring import rank_topics
from fst.video.assembler import assemble_video
from fst.video.subtitles import generate_subtitles
from fst.visuals.charts import generate_charts
from fst.visuals.stock import collect_visuals
from fst.writing.script import generate_script
from fst.writing.storyboard import generate_storyboard
logger=logging.getLogger(__name__)

class PipelineRunner:
    def __init__(self, settings: Settings) -> None: self.settings=settings
    def initialize(self) -> None:
        self.settings.validate(); initialize_database(self.settings.database_path)
    def create_job(self, topic: str | None = None) -> str:
        self.initialize(); video_id=str(uuid.uuid4())
        with connect(self.settings.database_path) as con:
            con.execute("INSERT INTO videos (video_id, topic, status) VALUES (?, ?, ?)", (video_id, topic, StageStatus.PENDING.value))
            con.executemany("INSERT INTO pipeline_stages (video_id, stage_name, status) VALUES (?, ?, ?)", [(video_id,s,StageStatus.PENDING.value) for s in STAGES])
        logger.info("Created video job %s", video_id); return video_id
    def _stage_status(self, video_id: str, stage: str) -> str:
        with connect(self.settings.database_path) as con:
            row=con.execute("SELECT status FROM pipeline_stages WHERE video_id=? AND stage_name=?", (video_id,stage)).fetchone()
        return row["status"] if row else StageStatus.PENDING.value
    def _set_stage(self, video_id: str, stage: str, status: StageStatus, output: Path | None = None, error: str | None = None) -> None:
        with connect(self.settings.database_path) as con:
            con.execute("UPDATE pipeline_stages SET status=?, output_path=?, error_message=?, updated_at=CURRENT_TIMESTAMP WHERE video_id=? AND stage_name=?", (status.value, str(output) if output else None, error, video_id, stage))
    def _run_stage(self, video_id: str, stage: str, fn):
        if self._stage_status(video_id, stage) == StageStatus.SUCCEEDED.value: return None
        self._set_stage(video_id, stage, StageStatus.RUNNING)
        try:
            result=fn(); self._set_stage(video_id, stage, StageStatus.SUCCEEDED); return result
        except Exception as exc:
            self._set_stage(video_id, stage, StageStatus.FAILED_BLOCKED, error=str(exc)); raise
    def run_all(self, topic: str | None = None, video_id: str | None = None) -> str:
        self.initialize(); out=self.settings.output_dir
        video_id = video_id or self.create_job(topic)
        with connect(self.settings.database_path) as con:
            row=con.execute("SELECT topic FROM videos WHERE video_id=?", (video_id,)).fetchone()
            current_topic=row["topic"] if row else topic
        def discover():
            topics=rank_topics(LocalTopicDiscoveryProvider().discover())
            with connect(self.settings.database_path) as con:
                con.executemany("INSERT OR IGNORE INTO topics (title,description,score) VALUES (?,?,?)", [(t.title,t.description,t.score) for t in topics])
            selected=current_topic or topics[0].title
            with connect(self.settings.database_path) as con: con.execute("UPDATE videos SET topic=? WHERE video_id=?", (selected, video_id))
            return selected
        selected_topic = self._run_stage(video_id,"topic_discovery",discover) or current_topic or "Local business documentary topic"
        self._run_stage(video_id,"topic_scoring",lambda: True)
        def research_stage():
            sources=Researcher(self.settings.database_path,out,LocalFixtureResearchProvider()).run(video_id,selected_topic)
            return create_dossier(self.settings.database_path,out,video_id,selected_topic,sources)
        dossier=self._run_stage(video_id,"research",research_stage)
        if dossier is None:
            from fst.db.models import read_json
            from fst.db.database import get_artifact
            dossier=read_json(get_artifact(self.settings.database_path,video_id,"dossier"))
        claims=self._run_stage(video_id,"fact_checking",lambda: verify_claims(self.settings.database_path,out,video_id,extract_claims(dossier),dossier["sources"]))
        if claims is None:
            from fst.db.models import ClaimRecord
            claims=[ClaimRecord(c, "supported", [1]) for c in extract_claims(dossier)]
        script=self._run_stage(video_id,"script_generation",lambda: generate_script(self.settings.database_path,out,video_id,selected_topic,claims))
        if script is None:
            from fst.db.models import read_json
            from fst.db.database import get_artifact
            script=read_json(get_artifact(self.settings.database_path,video_id,"script"))
        storyboard=self._run_stage(video_id,"storyboard",lambda: generate_storyboard(self.settings.database_path,out,video_id,script))
        if storyboard is None:
            from fst.db.models import read_json, Scene
            from fst.db.database import get_artifact
            storyboard=[Scene(**s) for s in read_json(get_artifact(self.settings.database_path,video_id,"storyboard"))]
        self._run_stage(video_id,"voice_generation",lambda: generate_voiceover(self.settings.database_path,out,video_id,storyboard))
        self._run_stage(video_id,"visual_generation_collection",lambda: (collect_visuals(self.settings.database_path,out,video_id,storyboard), generate_charts(self.settings.database_path,out,video_id,selected_topic)))
        video=self._run_stage(video_id,"video_assembly",lambda: assemble_video(self.settings.database_path,out,video_id,selected_topic,self.settings.ffmpeg_executable)) or get_artifact(self.settings.database_path,video_id,"final_video")
        self._run_stage(video_id,"subtitles",lambda: generate_subtitles(self.settings.database_path,out,video_id,storyboard))
        thumb_meta=self._run_stage(video_id,"thumbnail_metadata",lambda: (generate_thumbnail(self.settings.database_path,out,video_id,selected_topic), generate_metadata(self.settings.database_path,out,video_id,selected_topic,script)))
        self._run_stage(video_id,"quality_control",lambda: run_quality_checks(self.settings.database_path,out,video_id))
        if thumb_meta:
            metadata=thumb_meta[1]
        else:
            from fst.db.models import read_json
            meta_path=get_artifact(self.settings.database_path,video_id,"youtube_metadata")
            metadata=read_json(meta_path) if meta_path else {"privacy_status":"private"}
        yt=self._run_stage(video_id,"youtube_upload",lambda: upload_video(self.settings.database_path,out,video_id,video,metadata))
        if yt is None:
            with connect(self.settings.database_path) as con:
                row=con.execute("SELECT youtube_id FROM videos WHERE video_id=?", (video_id,)).fetchone()
                yt=row["youtube_id"] if row else "mock-youtube-missing"
        analytics=self._run_stage(video_id,"analytics",lambda: collect_analytics(self.settings.database_path,out,video_id,yt))
        self._run_stage(video_id,"learning_optimization",lambda: update_learning(self.settings.database_path,out,video_id,analytics or {"views":0,"watch_time_minutes":0,"ctr":0}))
        with connect(self.settings.database_path) as con: con.execute("UPDATE videos SET status='complete' WHERE video_id=?", (video_id,))
        return video_id
