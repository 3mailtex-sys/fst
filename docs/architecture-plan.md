# Automated YouTube Business Documentary System: Architecture Plan

## Current repository contents

At the start of this planning task, the repository is intentionally almost empty:

- `.git/` — Git repository metadata.
- `.gitkeep` — placeholder file so the otherwise-empty repository can be committed.

There is no application code, configuration, documentation, tests, or production folder structure yet.

## Design principles

This project should be built slowly and predictably. The first production version should be modular, understandable, and resumable rather than clever or overly complex.

Core rules:

- Use Python for the main application.
- Keep the folder structure stable.
- Keep each pipeline stage replaceable.
- Store API keys and secrets in environment variables only.
- Store video/job state so failed runs can resume.
- Prefer official APIs and licensed assets.
- Avoid scraping that violates website terms.
- Prioritize factual accuracy over speed.
- Detect unsupported claims instead of inventing sources.
- Add automation in phases, not all at once.


## Free-only requirement

This project must be designed as a free-only system unless the user explicitly approves a future change.

Rules:

- Do not introduce paid APIs, SaaS products, subscriptions, or paid services.
- Prefer local and open-source tools whenever practical.
- Use Gemini only through its available free tier and design the app to handle free-tier rate limits.
- Voice generation should be local and free.
- Video editing and assembly should use free/local tools such as FFmpeg where practical.
- YouTube Data API and YouTube Analytics API should use their free access/quota only.
- Do not add ElevenLabs, paid stock APIs, paid search APIs, paid video-generation APIs, Make, or other paid services.
- Do not treat a free trial as a free dependency.
- If a component cannot realistically be completed for free, stop before implementation, clearly flag the limitation, and propose a free alternative or reduced-scope approach.

This constraint affects provider choices throughout the system. Provider interfaces should still be replaceable, but the initial implementation must use free/local options only.

## Proposed fixed folder structure

```text
fst/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── docs/
│   ├── architecture-plan.md
│   ├── api-services.md
│   ├── pipeline.md
│   └── operations.md
├── src/
│   └── fst/
│       ├── __init__.py
│       ├── main.py
│       ├── config/
│       │   ├── __init__.py
│       │   └── settings.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── logging.py
│       │   ├── errors.py
│       │   ├── retry.py
│       │   └── state.py
│       ├── db/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── database.py
│       │   └── migrations/
│       ├── pipeline/
│       │   ├── __init__.py
│       │   ├── runner.py
│       │   └── stages.py
│       ├── topics/
│       │   ├── __init__.py
│       │   ├── discovery.py
│       │   └── scoring.py
│       ├── research/
│       │   ├── __init__.py
│       │   ├── providers.py
│       │   ├── researcher.py
│       │   └── dossier.py
│       ├── fact_checking/
│       │   ├── __init__.py
│       │   ├── claims.py
│       │   └── verifier.py
│       ├── writing/
│       │   ├── __init__.py
│       │   ├── script.py
│       │   └── storyboard.py
│       ├── audio/
│       │   ├── __init__.py
│       │   └── tts.py
│       ├── visuals/
│       │   ├── __init__.py
│       │   ├── stock.py
│       │   ├── generation.py
│       │   └── charts.py
│       ├── video/
│       │   ├── __init__.py
│       │   ├── subtitles.py
│       │   ├── assembler.py
│       │   └── ffmpeg.py
│       ├── metadata/
│       │   ├── __init__.py
│       │   ├── youtube_metadata.py
│       │   └── thumbnail.py
│       ├── quality/
│       │   ├── __init__.py
│       │   └── checks.py
│       ├── publishing/
│       │   ├── __init__.py
│       │   ├── youtube_upload.py
│       │   └── analytics.py
│       └── learning/
│           ├── __init__.py
│           └── optimizer.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/
│   ├── run_pipeline.py
│   ├── run_stage.py
│   └── dev_check.py
├── data/
│   ├── input/
│   ├── output/
│   ├── working/
│   └── cache/
└── logs/
```

## Folder and file explanations

### Root files

- `README.md` — beginner-friendly setup and usage instructions.
- `pyproject.toml` — Python project metadata, dependencies, and tool configuration.
- `.env.example` — list of required environment variables without real secrets.
- `.gitignore` — prevents secrets, generated videos, logs, local databases, and caches from being committed.

### `docs/`

Project documentation lives here.

- `architecture-plan.md` — this planning document.
- `api-services.md` — external API choices, setup steps, pricing notes, and replacement options.
- `pipeline.md` — detailed explanation of every pipeline stage.
- `operations.md` — how to run, monitor, resume, and troubleshoot the system.

### `src/fst/`

Main Python package for the application.

- `main.py` — command-line entry point for starting the app or pipeline.

### `src/fst/config/`

Configuration loading.

- `settings.py` — reads environment variables such as API keys, model names, database path, output path, and runtime options.

### `src/fst/core/`

Shared building blocks used by the whole system.

- `logging.py` — consistent structured logging.
- `errors.py` — custom error types.
- `retry.py` — retry helpers for temporary API failures.
- `state.py` — common state/status definitions for resumable jobs.

### `src/fst/db/`

Database layer, initially SQLite.

- `models.py` — database models such as videos, topics, sources, claims, scenes, assets, uploads, and analytics.
- `database.py` — database connection/session helpers.
- `migrations/` — future database schema migrations.

### `src/fst/pipeline/`

Pipeline orchestration.

- `runner.py` — runs one full video pipeline or resumes an incomplete one.
- `stages.py` — defines the ordered stages and their statuses.

### `src/fst/topics/`

Topic discovery and selection.

- `discovery.py` — finds candidate business documentary topics from approved sources and APIs.
- `scoring.py` — scores topics by interest, freshness, evidence availability, audience potential, and production difficulty.

### `src/fst/research/`

Research collection and organization.

- `providers.py` — replaceable adapters for search APIs, news APIs, official filings, company pages, and other legal sources.
- `researcher.py` — gathers source material for a selected topic.
- `dossier.py` — creates a structured research dossier with citations.

### `src/fst/fact_checking/`

Claim extraction and verification.

- `claims.py` — extracts important factual claims from research and scripts.
- `verifier.py` — checks whether each claim is supported by reliable sources.

### `src/fst/writing/`

Script and storyboard generation.

- `script.py` — generates documentary-style narration from the verified dossier.
- `storyboard.py` — turns the script into scenes with visual/audio instructions.

### `src/fst/audio/`

Voiceover generation.

- `tts.py` — adapter for a text-to-speech provider.

### `src/fst/visuals/`

Visual asset collection and generation.

- `stock.py` — searches licensed stock image/video providers.
- `generation.py` — adapter for image/video generation tools when licensed stock is unavailable or unsuitable.
- `charts.py` — generates charts and data graphics from verified numeric data.

### `src/fst/video/`

Video production.

- `subtitles.py` — creates subtitles from the script and narration timing.
- `assembler.py` — assembles visuals, audio, subtitles, transitions, and music into a final video.
- `ffmpeg.py` — safe wrapper around FFmpeg commands.

### `src/fst/metadata/`

YouTube packaging.

- `youtube_metadata.py` — generates title, description, tags, chapters, and pinned comment drafts.
- `thumbnail.py` — generates thumbnail concepts and final thumbnail assets.

### `src/fst/quality/`

Automated quality control.

- `checks.py` — verifies required assets exist, claims have citations, audio/video durations match, subtitles exist, and upload metadata is complete.

### `src/fst/publishing/`

Publishing and post-publication data.

- `youtube_upload.py` — uploads finished videos through the YouTube Data API.
- `analytics.py` — collects performance data from YouTube Analytics API.

### `src/fst/learning/`

Improvement loop.

- `optimizer.py` — uses analytics to improve future topic scoring, title styles, thumbnails, hooks, and retention decisions.

### `tests/`

Automated tests.

- `unit/` — fast tests for individual functions.
- `integration/` — tests for database, API adapters, and pipeline stage interactions.
- `fixtures/` — sample source documents, scripts, storyboards, and fake API responses.

### `scripts/`

Convenience scripts.

- `run_pipeline.py` — starts a full pipeline run.
- `run_stage.py` — runs or retries a single stage.
- `dev_check.py` — local validation helper.

### `data/`

Local runtime data. Most generated contents should be ignored by Git.

- `input/` — manually supplied source files if needed.
- `output/` — final videos, thumbnails, subtitles, and metadata exports.
- `working/` — intermediate files for each video job.
- `cache/` — temporary API responses and downloaded assets where allowed.

### `logs/`

Runtime logs. Logs should usually not be committed.

## State and resumability design

Every video should have a database record with a stable `video_id` and one status per stage.

Example stage statuses:

- `pending` — not started yet.
- `running` — currently in progress.
- `succeeded` — completed successfully.
- `failed_retryable` — failed because of a temporary issue such as rate limits or network errors.
- `failed_blocked` — failed because the system needs a decision, missing asset, unsupported claim, or invalid credentials.
- `skipped` — intentionally not needed for this video.

Each stage should save its output before the next stage begins. For example, research saves a dossier, script generation saves a script, storyboard generation saves scenes, voice generation saves audio files, and video assembly saves a final video path.

## External APIs, services, and free tool choices

### Required for the first useful automated system

These are required, but they must be free/local or free-quota only.

- Gemini API free tier — reasoning, summarization, research synthesis, claim extraction, script writing, storyboard writing, metadata drafting, and quality review. The system must include retries, rate-limit handling, and graceful stopping when the free tier is exhausted.
- Free/legal research sources — source finding must avoid paid search APIs. Initial choices should be official/public sources such as SEC EDGAR, company investor-relations pages, Wikipedia/Wikidata for topic leads only, GDELT, Google Trends public pages if allowed, RSS feeds, and other sources with legal free access.
- SQLite — local state database. This is free local infrastructure, not a hosted service.
- FFmpeg — free/open-source local video and audio assembly.
- Local/free text-to-speech — narration should use a local open-source engine such as Piper TTS first. If quality is insufficient, flag the limitation before adding any external provider.
- Python open-source libraries — use free packages for HTTP requests, database access, retries, subtitles, plotting, and testing.

### Optional but useful, still free-only

- Free stock media sources with usable licenses — possible examples include Wikimedia Commons, Internet Archive, Pexels free API, Pixabay free API, or other sources only after license/API terms are checked. The system must store asset license and attribution metadata.
- Local/open-source image generation — optional and only if it can run locally/free, such as Stable Diffusion through a local interface. If the local machine cannot run it, use generated charts/text graphics or licensed public-domain/Creative Commons assets instead.
- Local/open-source music and sound effects — use public-domain or Creative Commons audio only, with attribution tracking when required.
- Free official/open data sources — SEC EDGAR, Federal Reserve Economic Data where license terms allow, Companies House, data.gov, World Bank Open Data, OECD public data, and other free sources suitable for charts.
- Local similarity checks — use free/open-source text similarity methods to reduce accidental copying.
- Local content checks — use rule-based checks and Gemini free tier where available; do not add paid moderation services.

### Can be added later, free-only

- YouTube Data API free quota — uploading videos, thumbnails, descriptions, tags, playlists, and publishing settings. Implementation must respect quota limits.
- YouTube Analytics API free access/quota — collecting views, click-through rate, audience retention where available, traffic sources, and watch time.
- Local cron — simple free scheduling on the host machine.
- n8n self-hosted community edition — optional later only if self-hosted for free; do not use paid n8n cloud.
- Local filesystem storage — keep generated videos/assets locally at first. Cloud object storage should not be added unless a genuinely free tier is approved and not merely a trial.
- PostgreSQL local install — optional free database upgrade once SQLite becomes limiting.
- Local queue system — optional free tools such as Redis plus RQ/Celery/Dramatiq if parallel processing becomes necessary.
- Local review dashboard — optional local web app for reviewing scripts/assets before upload.
- Simple analytics experiments — compare title/thumbnail/content patterns using collected free YouTube Analytics data; do not add paid A/B testing platforms.

### Explicitly excluded unless the user later changes the requirement

- Paid search APIs such as SerpAPI paid plans or paid web-search subscriptions.
- Paid TTS services such as ElevenLabs paid plans.
- Paid stock services such as Storyblocks, Shutterstock, Getty Images, and Adobe Stock.
- Paid video-generation APIs or SaaS products.
- Paid automation platforms such as Make.
- Any service that is only temporarily free because of a free trial.


## Proposed free tool/API by component

| Component | Proposed free/local choice | Notes |
| --- | --- | --- |
| Topic discovery | SEC EDGAR company feeds, Wikipedia/Wikidata leads, GDELT, RSS feeds, public trend/news sources where terms allow | Avoid paid search APIs. Treat broad public sources as leads, not final proof. |
| Topic scoring | Local Python scoring rules plus Gemini free tier for qualitative judgment | Store scores and reasons in SQLite. |
| Research | Official company filings/pages, SEC EDGAR, government/open datasets, reputable free-access articles, RSS/API sources with legal terms | Do not bypass paywalls or scrape against terms. |
| Research dossier | Gemini free tier plus local citation database | Every important point should link back to stored source metadata. |
| Fact checking | Local claim extraction rules plus Gemini free tier, cross-source checks, official-source preference | Unsupported claims should block or be rewritten. |
| Script generation | Gemini free tier | Must use verified dossier and avoid uncited claims. |
| Storyboard | Gemini free tier | Scene prompts should prefer achievable stock/charts/simple visuals. |
| Voiceover | Piper TTS local/open-source | Free and local; voice quality may be lower than paid services. |
| Visual collection | Wikimedia Commons, Internet Archive, Pexels/Pixabay free APIs if terms fit, official press/media pages when licensed | Track license, source URL, attribution, and usage constraints. |
| Image generation | Local Stable Diffusion only if available | Optional; fallback is charts, text graphics, and licensed assets. |
| Video generation | No paid API; use still images, Ken Burns motion, charts, captions, and FFmpeg effects | Fully AI-generated video may not be realistic for free on limited hardware. |
| Charts/graphics | matplotlib, Plotly/Kaleido where free, Pillow, SVG templates | Use only verified data. |
| Video assembly | FFmpeg local/open-source | Main assembly tool. |
| Subtitles | Script timings plus local alignment where possible, such as aeneas or Whisper-compatible local tools if available | Exact word-level alignment may need tuning. |
| Thumbnail | Pillow, matplotlib, local templates, optional local image generation | Avoid paid design tools/APIs. |
| Metadata | Gemini free tier plus local templates | Titles/descriptions should be policy-safe and accurate. |
| Quality control | Local Python checks, ffprobe, citation/license validation, Gemini free tier for review where quota allows | Mechanical checks are free; editorial judgment remains imperfect. |
| Upload | YouTube Data API free quota | Start with private or unlisted uploads. |
| Analytics | YouTube Analytics API free access/quota | Metrics may be delayed or limited. |
| Scheduling | Local cron first; self-hosted n8n community edition later if useful | No paid automation platforms. |
| Learning loop | SQLite plus local Python analysis | Use free analytics data to adjust scoring rules. |

## Automation potential and limitations

### Can be mostly or completely automated

- Topic discovery from approved APIs and public datasets.
- Topic scoring using clear scoring rules.
- Source collection using legal APIs.
- Dossier generation with citations.
- Claim extraction from dossiers and scripts.
- Script drafting from verified research.
- Storyboard generation.
- TTS voiceover generation.
- Stock media search using licensed APIs.
- Basic image generation for non-deceptive visuals.
- Chart generation from verified data.
- Video assembly with FFmpeg.
- Subtitle generation from script and audio timings.
- Title, description, tags, chapters, and thumbnail drafts.
- Mechanical quality checks.
- Scheduled runs.
- YouTube upload after OAuth setup and quota approval.
- Analytics collection after publishing.
- Feedback into future scoring rules.

### Has technical, legal, or API limitations

- Fully reliable factual accuracy cannot be guaranteed by an AI model alone. The system can reduce risk by requiring citations, cross-checking claims, and blocking unsupported claims.
- Some sources may be paywalled, rate-limited, copyrighted, or unavailable through legal APIs.
- Search APIs may miss important sources or return low-quality sources.
- YouTube upload requires account authorization, API quotas, and compliance with YouTube policies.
- YouTube Analytics data may be delayed and may not expose every desired metric.
- Fully automated thumbnail and title optimization is limited by YouTube API capabilities, platform rules, and the free-only constraint.
- Stock media licenses vary. The system must track license/source metadata for every asset.
- AI-generated visuals may contain inaccuracies, brand misuse, or misleading depictions if not checked, and free/local generation may be limited by local hardware.
- TTS pronunciation, pacing, and emotional tone may require tuning.
- Automated video quality checks can catch obvious problems but may not judge whether the documentary is genuinely compelling.
- Some financial/company data requires paid licenses or has redistribution restrictions.

## Phased development roadmap

### Phase 1: Project foundation

Goal: Create the stable project skeleton and one simple local pipeline runner.

Deliverables:

- Create the agreed folder structure.
- Add `pyproject.toml`, `.env.example`, `.gitignore`, and `README.md`.
- Add configuration loading from environment variables.
- Add logging.
- Add retry utilities.
- Add SQLite database setup.
- Add basic video/job state tracking.
- Add a no-op pipeline runner that can mark stages as pending, running, succeeded, or failed.

No external AI/video generation work yet.

### Phase 2: Topic discovery and scoring prototype

Goal: Automatically find and rank candidate topics.

Deliverables:

- Add one legal search/research provider adapter.
- Add topic candidate model.
- Add simple scoring rules.
- Store discovered topics and scores in SQLite.
- Produce a ranked topic report.

### Phase 3: Research dossier generation

Goal: Research one selected topic and produce a cited dossier.

Deliverables:

- Collect source links and snippets through approved APIs.
- Classify source quality.
- Use Gemini to summarize sources.
- Produce a structured dossier with source citations.
- Store source metadata and dossier output.

### Phase 4: Fact checking and claim control

Goal: Prevent unsupported claims from entering the script.

Deliverables:

- Extract important claims from the dossier.
- Verify each claim against stored sources.
- Mark claims as supported, weakly supported, unsupported, or conflicting.
- Block script generation if important claims are unsupported.

### Phase 5: Script and storyboard generation

Goal: Create a documentary script and scene plan from verified research.

Deliverables:

- Generate script sections with intro hook, narrative arc, and conclusion.
- Require claim citations in script notes.
- Generate scene-by-scene storyboard.
- Store script and storyboard versions.

### Phase 6: Voiceover generation

Goal: Generate narration audio.

Deliverables:

- Add TTS provider adapter.
- Generate audio per script segment.
- Store audio files and durations.
- Add pronunciation override support.

### Phase 7: Visual assets and charts

Goal: Match scenes with legal visual assets.

Deliverables:

- Add licensed stock media provider adapter.
- Track asset licenses and source URLs.
- Add chart generation for verified numeric data.
- Add optional image generation adapter.
- Store asset metadata per scene.

### Phase 8: Video assembly and subtitles

Goal: Produce a complete local video file.

Deliverables:

- Build FFmpeg wrapper.
- Assemble scenes, narration, captions, charts, and music.
- Generate subtitles.
- Export final video and subtitle files.

### Phase 9: Metadata, thumbnail, and quality control

Goal: Prepare the video for publishing and catch obvious problems.

Deliverables:

- Generate title, description, chapters, tags, and thumbnail concepts.
- Generate or assemble a thumbnail.
- Check citations, licenses, missing files, durations, subtitle presence, and metadata completeness.
- Produce a final publish package.

### Phase 10: YouTube upload

Goal: Upload finished videos through official YouTube APIs.

Deliverables:

- Add OAuth setup documentation.
- Upload video, thumbnail, description, tags, and publishing status.
- Store YouTube video ID and upload status.
- Support private/unlisted first, public later.

### Phase 11: Analytics and learning loop

Goal: Improve future decisions using performance data.

Deliverables:

- Pull YouTube Analytics data.
- Store metrics by video.
- Compare performance against topic/title/script/thumbnail features.
- Feed results into topic scoring and metadata generation.

### Phase 12: Scheduling and full automation

Goal: Run the complete system automatically.

Deliverables:

- Add scheduler using cron, GitHub Actions, cloud scheduler, or n8n.
- Add failure notifications.
- Add automatic resume after retryable failures.
- Optionally add human review gates for high-risk stages.
- Run end-to-end from topic discovery to analytics ingestion.

## Recommended approval checkpoint

Before implementation starts, approve or revise:

1. The folder structure.
2. The first free-only external services or local tools to use.
3. Whether uploads should initially be private, unlisted, or public.
4. Whether any human review gate is required before upload.

Implementation should not begin until this plan is approved.
