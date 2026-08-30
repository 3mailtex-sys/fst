"""Simple citation-based claim verification."""
from __future__ import annotations
from pathlib import Path
from fst.db.database import connect, save_artifact
from fst.db.models import ClaimRecord, write_json

def verify_claims(database_path: Path, output_dir: Path, video_id: str, claims: list[str], sources: list[dict]) -> list[ClaimRecord]:
    verified: list[ClaimRecord] = []
    for claim in claims:
        matches = [i + 1 for i, source in enumerate(sources) if any(word in source.get("text", "").lower() for word in claim.lower().split()[:6])]
        verified.append(ClaimRecord(claim, "supported" if matches else "unsupported", matches))
    with connect(database_path) as con:
        con.executemany("INSERT INTO claims (video_id,text,status,source_ids) VALUES (?,?,?,?)", [(video_id,c.text,c.status,",".join(map(str,c.source_ids))) for c in verified])
    path = write_json(output_dir / video_id / "claims.json", verified)
    save_artifact(database_path, video_id, "claims", path)
    return verified
