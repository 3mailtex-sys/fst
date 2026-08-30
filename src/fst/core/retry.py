"""Small retry helper for temporary failures."""

from __future__ import annotations

from collections.abc import Callable
from time import sleep
from typing import TypeVar

T = TypeVar("T")


def retry(operation: Callable[[], T], attempts: int = 3, delay_seconds: float = 1.0) -> T:
    """Retry an operation a small number of times before re-raising its error."""

    if attempts < 1:
        raise ValueError("attempts must be at least 1")

    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except Exception as exc:  # noqa: BLE001 - helper intentionally retries arbitrary operations.
            last_error = exc
            if attempt == attempts:
                break
            sleep(delay_seconds)

    assert last_error is not None
    raise last_error
