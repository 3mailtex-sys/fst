"""Run basic developer checks for Phase 1."""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    """Run the test suite."""

    return subprocess.call([sys.executable, "-m", "pytest"])


if __name__ == "__main__":
    raise SystemExit(main())
