from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


class PublishingBlocked(RuntimeError):
    pass


def load_approval(path: str = "data/output/approval_request.json") -> Dict:
    approval_path = Path(path)
    if not approval_path.exists():
        raise PublishingBlocked("No approval record exists")
    return json.loads(approval_path.read_text(encoding="utf-8"))


def assert_publish_allowed(path: str = "data/output/approval_request.json") -> Dict:
    state = load_approval(path)
    if not state.get("approved") or not state.get("publishing_allowed"):
        raise PublishingBlocked("Publishing blocked: explicit approval is required")
    return state


def publish_stub(video_path: str, approval_path: str = "data/output/approval_request.json") -> Dict:
    """Safety gate for future YouTube/Instagram/TikTok adapters.

    This intentionally does not call any platform API yet. Every future adapter
    must call assert_publish_allowed before uploading content.
    """
    state = assert_publish_allowed(approval_path)
    video = Path(video_path)
    if not video.exists():
        raise FileNotFoundError(video)
    return {
        "status": "ready_for_platform_adapter",
        "video": str(video),
        "approval": state,
    }
