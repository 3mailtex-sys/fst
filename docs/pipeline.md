# Pipeline Overview

The runner supports a full free/local development pipeline and resumable stage state.

Stages:

1. Topic discovery — local fixture provider creates candidate topics.
2. Topic scoring — local rules rank candidates and prevent duplicate topic inserts.
3. Research — local fixture research sources are stored in SQLite and a dossier is generated.
4. Fact checking — claims are extracted and verified against stored source text.
5. Script generation — a documentary-style script is generated from supported claims.
6. Storyboard — script sections become scenes.
7. Voice generation — local WAV fallback creates testable narration assets.
8. Visual generation/collection — SVG scene cards and graphics are created locally.
9. Video assembly — development mode writes a final package marker; FFmpeg expansion is reserved for real media.
10. Subtitles — SRT subtitles are generated from scene timing.
11. Thumbnail and metadata — local SVG thumbnail and private YouTube metadata are generated.
12. Quality control — required artifacts and unsupported claims are checked.
13. YouTube upload — mock provider stores a fake YouTube ID in development mode.
14. Analytics — mock provider stores zeroed analytics in development mode.
15. Learning/optimization — local insight is stored for future scoring improvements.

Each stage stores status in SQLite. Completed stages are skipped on resume where possible, and artifacts are reused by later stages.
