# FST: Free-Only YouTube Business Documentary Pipeline

FST is a modular Python system for producing business-documentary video packages. The current implementation is a complete free/local development pipeline: it discovers/scorers topics, creates local fixture research, verifies claims, writes a script/storyboard, creates local narration/visual placeholders, assembles a package marker, creates subtitles/thumbnail/metadata, runs quality checks, mocks YouTube upload/analytics, stores learning notes, and can be scheduled locally.

## Free-only rule

Use only free, local, open-source, or free-quota tools unless the user explicitly approves a future change. Do not add paid APIs, subscriptions, paid stock services, paid TTS, paid search APIs, paid video-generation APIs, Make, paid n8n, or free trials treated as dependencies.

## Requirements

- Python 3.11+
- SQLite from Python's standard library
- Optional later: FFmpeg for real video assembly, Piper for local speech, YouTube OAuth credentials for real upload/analytics, Gemini free tier for AI generation

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
cp .env.example .env
```

Phase 1/development mode does not require API keys.

## Run locally

Initialize the database:

```bash
python -m fst.main init-db
```

Create a pending job only:

```bash
python -m fst.main create-job --topic "Example business documentary topic"
```

Run the full development pipeline without spending API quota:

```bash
python -m fst.main run --topic "Example business documentary topic"
```

Outputs are written under `data/output/<video_id>/`; state is stored in `data/working/fst.sqlite3` by default.

## Verify

```bash
python -m pytest
python scripts/dev_check.py
```

## Modes

- `FST_MODE=development` uses local fixture/mock providers and never publishes publicly.
- `FST_MODE=production` is reserved for configured real providers. YouTube upload/analytics still require official free-quota API credentials and should start private/unlisted.

## Scheduling

Use local cron first. See `scripts/schedule_cron_example.sh`; edit paths before installing it with `crontab -e`.

## Known free/local limitations

- Local fixture research is for development testing, not final factual production.
- The fallback TTS creates a simple WAV tone so the pipeline remains testable without paid speech APIs; install/configure Piper later for real local narration.
- Video assembly currently writes a package marker in development mode; FFmpeg integration can be expanded with real media templates without paid services.
- Real YouTube upload and analytics require user-created OAuth credentials and free quota.
