"""Free/local topic discovery."""
from __future__ import annotations
from fst.db.models import TopicCandidate

class TopicDiscoveryProvider:
    def discover(self) -> list[TopicCandidate]: raise NotImplementedError

class LocalTopicDiscoveryProvider(TopicDiscoveryProvider):
    def discover(self) -> list[TopicCandidate]:
        return [
            TopicCandidate("The rise and reset of WeWork", "Business model, governance, IPO failure, bankruptcy, and lessons.", "fixture"),
            TopicCandidate("Netflix's transition from DVDs to streaming", "How Netflix changed distribution, licensing, and original content.", "fixture"),
            TopicCandidate("Nokia and the smartphone disruption", "Why a dominant phone company struggled during the iPhone/Android era.", "fixture"),
        ]
