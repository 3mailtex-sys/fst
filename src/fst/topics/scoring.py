"""Topic scoring with simple local rules."""
from __future__ import annotations
from fst.db.models import TopicCandidate

KEYWORDS = ("rise", "fall", "reset", "transition", "disruption", "bankruptcy", "lessons")

def score_topic(topic: TopicCandidate) -> TopicCandidate:
    text = f"{topic.title} {topic.description}".lower()
    score = 50 + sum(8 for word in KEYWORDS if word in text) + min(len(topic.description) / 10, 20)
    return TopicCandidate(topic.title, topic.description, topic.source, round(score, 2))

def rank_topics(topics: list[TopicCandidate]) -> list[TopicCandidate]:
    return sorted((score_topic(t) for t in topics), key=lambda t: t.score, reverse=True)
