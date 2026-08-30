"""Free/local narration generation with a WAV fallback."""
from __future__ import annotations
from pathlib import Path
import math, struct, wave
from fst.db.database import save_artifact
from fst.db.models import Scene

class TTSProvider:
    def synthesize(self, text: str, path: Path, duration: float = 2.0) -> Path: raise NotImplementedError

class LocalToneTTSProvider(TTSProvider):
    def synthesize(self, text: str, path: Path, duration: float = 2.0) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True); rate=16000; frames=int(rate*duration)
        with wave.open(str(path), "w") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
            for i in range(frames):
                value=int(9000*math.sin(2*math.pi*220*i/rate)); w.writeframes(struct.pack('<h', value))
        return path

def generate_voiceover(database_path: Path, output_dir: Path, video_id: str, scenes: list[Scene], provider: TTSProvider | None = None) -> list[Path]:
    provider = provider or LocalToneTTSProvider(); paths=[]
    for scene in scenes:
        paths.append(provider.synthesize(scene.narration, output_dir / video_id / "audio" / f"scene_{scene.number:02d}.wav", min(scene.duration_seconds, 8)))
    save_artifact(database_path, video_id, "voiceover", output_dir / video_id / "audio")
    return paths
