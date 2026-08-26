import json
from pathlib import Path

import pytest

from src.platforms import publish_all
from src.publishing import PublishingBlocked


def _story():
    return {
        "title": "اختبار",
        "caption": "وصف",
        "hashtags": ["السعودية", "تقنية"],
        "ai_disclosure": True,
    }


def test_publish_all_blocked_without_approval(tmp_path):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"demo")
    approval = tmp_path / "approval.json"
    approval.write_text(json.dumps({"approved": False, "publishing_allowed": False}), encoding="utf-8")

    with pytest.raises(PublishingBlocked):
        publish_all(str(video), _story(), str(approval), dry_run=True)


def test_publish_all_dry_run_after_approval(tmp_path):
    video = tmp_path / "video.mp4"
    video.write_bytes(b"demo")
    approval = tmp_path / "approval.json"
    approval.write_text(json.dumps({"approved": True, "publishing_allowed": True}), encoding="utf-8")

    result = publish_all(str(video), _story(), str(approval), dry_run=True)
    assert [item["platform"] for item in result] == ["youtube_shorts", "instagram_reels", "tiktok"]
    assert all(item["status"] == "dry_run" for item in result)
    assert result[0]["containsSyntheticMedia"] is True
    assert result[2]["is_aigc"] is True
