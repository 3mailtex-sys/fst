"""Research provider interfaces and free local fixture provider."""
from __future__ import annotations
from fst.db.models import SourceRecord

class ResearchProvider:
    def search(self, topic: str) -> list[SourceRecord]: raise NotImplementedError

class LocalFixtureResearchProvider(ResearchProvider):
    def search(self, topic: str) -> list[SourceRecord]:
        return [
            SourceRecord("Official company/background source", "local://official-background", "Local fixture", f"{topic} involves company strategy, market timing, leadership decisions, and competitive pressure.", 0.75),
            SourceRecord("Public business context source", "local://public-context", "Local fixture", f"Public reporting about {topic} highlights customer behavior, financing conditions, and execution risks.", 0.65),
            SourceRecord("Lessons source", "local://lessons", "Local fixture", f"The main lessons from {topic} concern incentives, durable advantage, governance, and adapting before markets shift.", 0.7),
        ]
