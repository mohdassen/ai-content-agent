from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

import requests

from src.publishing import assert_publish_allowed
from src.youtube_upload import upload_resumable


class PlatformConfigurationError(RuntimeError):
    pass


def _metadata(story: Dict) -> Dict:
    hashtags = " ".join(f"#{tag.lstrip('#')}" for tag in story.get("hashtags", []))
    caption = story.get("caption", "").strip()
    return {
        "title": story.get("title", "خلف الرقم"),
        "caption": (caption + "\n\n" + hashtags).strip(),
        "ai_disclosure": bool(story.get("ai_disclosure", True)),
    }


def publish_all(video_path: str, story: Dict, approval_path: str = "data/output/approval_request.json", dry_run: bool = True) -> List[Dict]:
    assert_publish_allowed(approval_path)
    video = Path(video_path)
    if not video.exists():
        raise FileNotFoundError(video)

    results = []
    for fn in (publish_youtube, publish_instagram, publish_tiktok):
        results.append(fn(video, story, dry_run=dry_run))
    return results


def publish_youtube(video: Path, story: Dict, dry_run: bool = True) -> Dict:
    meta = _metadata(story)
    if dry_run:
        return {
            "platform": "youtube_shorts",
            "status": "dry_run",
            "video": str(video),
            "title": meta["title"],
            "privacy": "private",
            "containsSyntheticMedia": meta["ai_disclosure"],
        }

    if os.getenv("YOUTUBE_LIVE_UPLOAD", "false").lower() != "true":
        raise PlatformConfigurationError(
            "YouTube uploader is configured but locked. Set YOUTUBE_LIVE_UPLOAD=true explicitly."
        )

    # Private is intentionally hard-coded for the first production phase.
    # Google restricts uploads from unverified API projects to private anyway,
    # and we do not want an accidental public post during onboarding.
    result = upload_resumable(video, story, privacy_status="private")
    result["containsSyntheticMedia"] = meta["ai_disclosure"]
    return result


def publish_instagram(video: Path, story: Dict, dry_run: bool = True) -> Dict:
    meta = _metadata(story)
    if dry_run:
        return {
            "platform": "instagram_reels",
            "status": "dry_run",
            "video": str(video),
            "caption": meta["caption"],
        }

    page_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    ig_user_id = os.getenv("INSTAGRAM_USER_ID")
    public_video_url = os.getenv("PUBLIC_VIDEO_URL")
    if not all([page_token, ig_user_id, public_video_url]):
        raise PlatformConfigurationError(
            "INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID, and PUBLIC_VIDEO_URL are required"
        )

    raise PlatformConfigurationError("Instagram live publishing is disabled until account/API review is complete")


def publish_tiktok(video: Path, story: Dict, dry_run: bool = True) -> Dict:
    meta = _metadata(story)
    if dry_run:
        return {
            "platform": "tiktok",
            "status": "dry_run",
            "video": str(video),
            "title": meta["caption"],
            "privacy": "SELF_ONLY",
            "is_aigc": meta["ai_disclosure"],
        }

    access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    if not access_token:
        raise PlatformConfigurationError("TIKTOK_ACCESS_TOKEN is missing")

    creator = requests.post(
        "https://open.tiktokapis.com/v2/post/publish/creator_info/query/",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json; charset=UTF-8"},
        timeout=30,
    )
    creator.raise_for_status()

    raise PlatformConfigurationError("TikTok live publishing is disabled until video.publish approval/audit is complete")


def write_publish_plan(results: List[Dict], output_dir: str = "data/output") -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "publish_plan.json"
    path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
