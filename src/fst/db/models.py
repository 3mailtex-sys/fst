"""Data models for pipeline records."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import json

@dataclass(frozen=True)
class TopicCandidate:
    title: str; description: str; source: str = "local"; score: float = 0.0
@dataclass(frozen=True)
class SourceRecord:
    title: str; url: str; publisher: str; text: str; reliability: float = 0.5; published_at: str | None = None
@dataclass(frozen=True)
class ClaimRecord:
    text: str; status: str; source_ids: list[int]
@dataclass(frozen=True)
class Scene:
    number: int; narration: str; visual: str; duration_seconds: float
@dataclass(frozen=True)
class VideoJob:
    video_id: str; topic: str | None; status: str
@dataclass(frozen=True)
class PipelineStageRecord:
    video_id: str; stage_name: str; status: str; output_path: str | None = None; error_message: str | None = None

def write_json(path: Path, data: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=lambda o: asdict(o) if hasattr(o, "__dataclass_fields__") else str(o)))
    return path

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())
