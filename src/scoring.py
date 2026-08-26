from dataclasses import dataclass


@dataclass
class TopicSignals:
    curiosity: float
    emotion: float
    shareability: float
    freshness: float
    monetization: float
    market_relevance: float
    competition: float


def viral_score(s: TopicSignals) -> float:
    """Return a transparent 0-10 opportunity score.

    Competition is inverted: lower competition improves the score.
    """
    values = [
        s.curiosity,
        s.emotion,
        s.shareability,
        s.freshness,
        s.monetization,
        s.market_relevance,
        s.competition,
    ]
    if any(v < 0 or v > 10 for v in values):
        raise ValueError("All topic signals must be between 0 and 10")

    score = (
        s.curiosity * 0.22
        + s.emotion * 0.12
        + s.shareability * 0.18
        + s.freshness * 0.12
        + s.monetization * 0.13
        + s.market_relevance * 0.15
        + (10 - s.competition) * 0.08
    )
    return round(score, 2)
