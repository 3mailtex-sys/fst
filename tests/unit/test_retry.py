import pytest

from fst.core.retry import retry


def test_retry_returns_success_after_temporary_failures():
    calls = {"count": 0}

    def operation():
        calls["count"] += 1
        if calls["count"] < 2:
            raise RuntimeError("temporary")
        return "ok"

    assert retry(operation, attempts=2, delay_seconds=0) == "ok"
    assert calls["count"] == 2


def test_retry_rejects_invalid_attempt_count():
    with pytest.raises(ValueError, match="attempts"):
        retry(lambda: "ok", attempts=0)
