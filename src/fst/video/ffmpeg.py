"""FFmpeg helpers with free/local fallback."""
from __future__ import annotations
import shutil, subprocess
from pathlib import Path

def has_ffmpeg(executable: str = "ffmpeg") -> bool: return shutil.which(executable) is not None

def run_ffmpeg(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, capture_output=True, text=True)

def write_placeholder_video(path: Path, title: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"Placeholder video package for {title}. Install FFmpeg for real MP4 assembly.\n")
    return path
