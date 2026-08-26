from src.scoring import TopicSignals, viral_score


def test_score_range():
    score = viral_score(TopicSignals(9, 8, 8, 7, 8, 9, 5))
    assert 0 <= score <= 10


def test_low_competition_scores_higher():
    base = dict(curiosity=8, emotion=8, shareability=8, freshness=8, monetization=8, market_relevance=8)
    low = viral_score(TopicSignals(**base, competition=2))
    high = viral_score(TopicSignals(**base, competition=9))
    assert low > high
