from src.tiktok_upload import build_post_info


def test_tiktok_defaults_private_and_marks_ai():
    info = build_post_info({
        "caption": "قصة اليوم",
        "hashtags": ["AI", "السعودية"],
        "ai_disclosure": True,
    })
    assert info["privacy_level"] == "SELF_ONLY"
    assert info["is_aigc"] is True
    assert "#AI" in info["title"]


def test_tiktok_caption_is_bounded():
    info = build_post_info({"caption": "x" * 3000})
    assert len(info["title"]) <= 2200
