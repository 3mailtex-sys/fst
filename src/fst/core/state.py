"""Pipeline state definitions."""

from __future__ import annotations

from enum import StrEnum


class StageStatus(StrEnum):
    """Allowed status values for every pipeline stage."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED_RETRYABLE = "failed_retryable"
    FAILED_BLOCKED = "failed_blocked"
    SKIPPED = "skipped"


PHASE_1_STAGES: tuple[str, ...] = (
    "topic_discovery",
    "topic_scoring",
    "research",
    "fact_checking",
    "script_generation",
    "storyboard",
    "voice_generation",
    "visual_generation_collection",
    "video_assembly",
    "subtitles",
    "thumbnail_metadata",
    "quality_control",
    "youtube_upload",
    "analytics",
    "learning_optimization",
)
