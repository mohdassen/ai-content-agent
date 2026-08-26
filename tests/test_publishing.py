import json

import pytest

from src.publishing import PublishingBlocked, assert_publish_allowed


def test_publishing_is_blocked_without_approval(tmp_path):
    state = tmp_path / "approval.json"
    state.write_text(json.dumps({"approved": False, "publishing_allowed": False}), encoding="utf-8")
    with pytest.raises(PublishingBlocked):
        assert_publish_allowed(str(state))


def test_publishing_is_allowed_only_with_explicit_state(tmp_path):
    state = tmp_path / "approval.json"
    state.write_text(json.dumps({"approved": True, "publishing_allowed": True}), encoding="utf-8")
    result = assert_publish_allowed(str(state))
    assert result["approved"] is True
