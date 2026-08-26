from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, Iterator, Tuple

import requests


INIT_ENDPOINT = "https://open.tiktokapis.com/v2/post/publish/video/init/"
CREATOR_ENDPOINT = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
MAX_CHUNK = 64 * 1024 * 1024


class TikTokUploadError(RuntimeError):
    pass


def build_post_info(story: Dict, privacy_level: str = "SELF_ONLY") -> Dict:
    hashtags = " ".join(f"#{tag.lstrip('#')}" for tag in story.get("hashtags", []))
    title = (story.get("caption", "").strip() + "\n\n" + hashtags).strip()
    return {
        "title": title[:2200],
        "privacy_level": privacy_level,
        "disable_duet": False,
        "disable_comment": False,
        "disable_stitch": False,
        "video_cover_timestamp_ms": 1000,
        "is_aigc": bool(story.get("ai_disclosure", True)),
    }


def _chunks(path: Path, chunk_size: int = MAX_CHUNK) -> Iterator[Tuple[int, int, bytes]]:
    total = path.stat().st_size
    start = 0
    with path.open("rb") as handle:
        while start < total:
            data = handle.read(chunk_size)
            if not data:
                break
            end = start + len(data) - 1
            yield start, end, data
            start = end + 1


def query_creator(access_token: str) -> Dict:
    response = requests.post(
        CREATOR_ENDPOINT,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    error = payload.get("error", {})
    if error.get("code") not in (None, "ok"):
        raise TikTokUploadError(error.get("message") or error.get("code"))
    return payload.get("data", {})


def direct_post_file(video_path: Path, story: Dict, access_token: str) -> Dict:
    if not video_path.exists():
        raise FileNotFoundError(video_path)

    creator = query_creator(access_token)
    privacy_options = creator.get("privacy_level_options", [])
    if privacy_options and "SELF_ONLY" not in privacy_options:
        raise TikTokUploadError("Creator account does not currently allow SELF_ONLY posting")

    size = video_path.stat().st_size
    chunk_size = min(MAX_CHUNK, max(1, size))
    total_chunks = max(1, math.ceil(size / chunk_size))
    body = {
        "post_info": build_post_info(story, privacy_level="SELF_ONLY"),
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": size,
            "chunk_size": chunk_size,
            "total_chunk_count": total_chunks,
        },
    }

    init = requests.post(
        INIT_ENDPOINT,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        json=body,
        timeout=30,
    )
    init.raise_for_status()
    init_payload = init.json()
    error = init_payload.get("error", {})
    if error.get("code") not in (None, "ok"):
        raise TikTokUploadError(error.get("message") or error.get("code"))

    data = init_payload.get("data", {})
    upload_url = data.get("upload_url")
    publish_id = data.get("publish_id")
    if not upload_url or not publish_id:
        raise TikTokUploadError("TikTok init response did not contain upload_url/publish_id")

    for start, end, chunk in _chunks(video_path, chunk_size=chunk_size):
        sent = requests.put(
            upload_url,
            headers={
                "Content-Type": "video/mp4",
                "Content-Length": str(len(chunk)),
                "Content-Range": f"bytes {start}-{end}/{size}",
            },
            data=chunk,
            timeout=300,
        )
        sent.raise_for_status()

    return {
        "platform": "tiktok",
        "status": "submitted",
        "publish_id": publish_id,
        "privacy": "SELF_ONLY",
        "is_aigc": bool(story.get("ai_disclosure", True)),
    }
