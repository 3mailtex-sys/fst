# Free-Only API and Tool Plan

## Implemented now

- Topic/research providers: local fixtures.
- Database: local SQLite.
- Voiceover: local WAV fallback; no external API.
- Visuals/charts/thumbnail: local SVG generation.
- Video assembly: local placeholder package; FFmpeg can be expanded later.
- Upload/analytics: mock YouTube providers in development mode.
- Scheduling: local cron example.

## User configuration needed for real production providers

- Gemini free tier API key for reasoning/writing once a real Gemini provider is enabled.
- Piper installed locally for real free narration.
- FFmpeg installed locally for real video assembly.
- YouTube Data API and YouTube Analytics API OAuth credentials using free quota.

Paid APIs, SaaS, subscriptions, free trials, ElevenLabs, paid stock/search/video-generation services, Make, and paid n8n are excluded.
