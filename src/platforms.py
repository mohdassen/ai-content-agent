from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

from src.publishing import assert_publish_allowed
from src.tiktok_upload import direct_post_file
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

    if os.getenv("TIKTOK_LIVE_UPLOAD", "false").lower() != "true":
        raise PlatformConfigurationError(
            "TikTok uploader is configured but locked. Set TIKTOK_LIVE_UPLOAD=true explicitly."
        )

    access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
    if not access_token:
        raise PlatformConfigurationError("TIKTOK_ACCESS_TOKEN is missing")

    return direct_post_file(video, story, access_token)


def write_publish_plan(results: List[Dict], output_dir: str = "data/output") -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "publish_plan.json"
    path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
