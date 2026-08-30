"""Claim extraction."""
from __future__ import annotations

def extract_claims(dossier: dict) -> list[str]:
    return [point.strip() for point in dossier.get("key_points", []) if point.strip()]
