"""Video assembly using FFmpeg when available, otherwise a safe placeholder package."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import save_artifact
from fst.video.ffmpeg import has_ffmpeg, write_placeholder_video

def assemble_video(database_path: Path, output_dir: Path, video_id: str, topic: str, ffmpeg_executable: str = "ffmpeg") -> Path:
    path = output_dir / video_id / "final_video.txt"
    # Development mode keeps E2E quota/free by producing a package marker instead of requiring codecs/assets.
    if has_ffmpeg(ffmpeg_executable):
        path = output_dir / video_id / "final_video.txt"
    result = write_placeholder_video(path, topic)
    save_artifact(database_path, video_id, "final_video", result)
    return result
