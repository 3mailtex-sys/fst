#!/usr/bin/env bash
# Example free/local scheduler entry. Edit paths, then install manually with crontab -e.
cd /workspace/fst && PYTHONPATH=src FST_MODE=development python -m fst.main run >> logs/cron.log 2>&1
