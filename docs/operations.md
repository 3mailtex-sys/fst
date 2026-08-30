# Operations

## Common commands

```bash
python -m fst.main init-db
python -m fst.main create-job --topic "A company story"
python -m fst.main run --topic "A company story"
python -m pytest
python scripts/dev_check.py
```

## Configuration

Environment variables:

- `FST_MODE` — `development` or `production`; default is `development`.
- `FST_DATABASE_PATH` — SQLite database path; default `data/working/fst.sqlite3`.
- `FST_DATA_DIR` — local data folder; default `data`.
- `FST_LOG_LEVEL` — `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.
- `GEMINI_API_KEY` — optional until a later real Gemini provider is enabled; must use free tier.
- `YOUTUBE_CLIENT_SECRETS` — path to official YouTube OAuth client secrets for later real upload/analytics.
- `YOUTUBE_TOKEN_PATH` — local OAuth token cache path; do not commit it.
- `PIPER_EXECUTABLE` — local Piper command path for later real local TTS.
- `FFMPEG_EXECUTABLE` / `FFPROBE_EXECUTABLE` — local FFmpeg tools.

## Development mode

Development mode uses local fixtures and mock providers. It creates deterministic files and database state without using API quota or publishing publicly.

## Production mode notes

Production mode requires real free-tier/free-quota credentials and further provider configuration. If a component cannot be done for free, implement a reduced local alternative and document the limitation before relying on a paid service.

## Scheduling

Use local cron with `scripts/schedule_cron_example.sh`. Self-hosted n8n community edition can be considered later; paid n8n cloud is excluded.
