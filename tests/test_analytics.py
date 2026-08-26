from src.analytics import PerformanceSnapshot, normalized_score, rank_content


def test_retention_and_shares_outweigh_views_alone():
    viral_quality = PerformanceSnapshot(
        platform="youtube",
        content_id="a",
        views=10000,
        shares=300,
        comments=120,
        followers_gained=150,
        avg_watch_seconds=38,
        completion_rate=0.82,
    )
    vanity_views = PerformanceSnapshot(
        platform="youtube",
        content_id="b",
        views=100000,
        shares=50,
        comments=20,
        followers_gained=30,
        avg_watch_seconds=10,
        completion_rate=0.20,
    )

    assert normalized_score(viral_quality) > normalized_score(vanity_views)
    assert rank_content([vanity_views, viral_quality])[0]["content_id"] == "a"
