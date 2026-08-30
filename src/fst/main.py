"""Command-line entry point."""
from __future__ import annotations
import argparse
from fst.config.settings import Settings
from fst.core.logging import configure_logging
from fst.pipeline.runner import PipelineRunner

def build_parser() -> argparse.ArgumentParser:
    parser=argparse.ArgumentParser(description="FST free-only documentary pipeline")
    sub=parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init-db", help="Create SQLite tables")
    cj=sub.add_parser("create-job", help="Create a pending job"); cj.add_argument("--topic", default=None)
    run=sub.add_parser("run", help="Run/resume full development pipeline"); run.add_argument("--topic", default=None); run.add_argument("--video-id", default=None)
    return parser

def main() -> None:
    settings=Settings.from_env(); settings.validate(); configure_logging(settings.log_level); runner=PipelineRunner(settings); args=build_parser().parse_args()
    if args.command=="init-db": runner.initialize(); print(f"Initialized database at {settings.database_path}")
    elif args.command=="create-job": print(f"Created video job {runner.create_job(args.topic)}")
    elif args.command=="run": print(f"Completed video job {runner.run_all(args.topic, args.video_id)}")
if __name__ == "__main__": main()
