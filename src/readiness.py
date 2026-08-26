from __future__ import annotations

import os
from typing import Dict, List


def _has(*names: str) -> bool:
    return all(bool(os.getenv(name)) for name in names)


def platform_readiness() -> Dict:
    checks: List[Dict] = [
        {
            "platform": "telegram",
            "ready": _has("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"),
            "required_secrets": ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"],
        },
        {
            "platform": "pexels",
            "ready": _has("PEXELS_API_KEY"),
            "required_secrets": ["PEXELS_API_KEY"],
        },
        {
            "platform": "youtube",
            "ready": _has("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN") or _has("YOUTUBE_ACCESS_TOKEN"),
            "required_secrets": ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"],
            "scope": "https://www.googleapis.com/auth/youtube.upload",
        },
        {
            "platform": "instagram",
            "ready": _has("INSTAGRAM_ACCESS_TOKEN", "INSTAGRAM_USER_ID"),
            "required_secrets": ["INSTAGRAM_ACCESS_TOKEN", "INSTAGRAM_USER_ID"],
        },
        {
            "platform": "tiktok",
            "ready": _has("TIKTOK_ACCESS_TOKEN"),
            "required_secrets": ["TIKTOK_ACCESS_TOKEN"],
        },
    ]
    return {
        "all_ready": all(item["ready"] for item in checks),
        "checks": checks,
        "safe_default": "dry_run/private",
    }
