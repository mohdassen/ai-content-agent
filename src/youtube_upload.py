from __future__ import annotations

import json
import mimetypes
import os
from pathlib import Path
from typing import Dict, Optional

import requests


YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
UPLOAD_ENDPOINT = "https://www.googleapis.com/upload/youtube/v3/videos"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


class YouTubeUploadError(RuntimeError):
    pass


def build_video_resource(story: Dict, privacy_status: str = "private") -> Dict:
    hashtags = [tag.lstrip("#") for tag in story.get("hashtags", [])]
    description = story.get("caption", "").strip()
    if hashtags:
        description = (description + "\n\n" + " ".join(f"#{tag}" for tag in hashtags)).strip()

    # Keep private as the safe default. Unverified YouTube API projects are
    # restricted to private uploads by Google until the project passes audit.
    return {
        "snippet": {
            "title": story.get("title", "خلف الرقم")[:100],
            "description": description,
            "tags": hashtags[:30],
            "categoryId": str(story.get("youtube_category_id", "28")),
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }


def refresh_access_token(refresh_token: str, client_id: str, client_secret: str) -> str:
    response = requests.post(
        TOKEN_ENDPOINT,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        raise YouTubeUploadError("Google token refresh returned no access_token")
    return token


def access_token_from_env() -> str:
    direct = os.getenv("YOUTUBE_ACCESS_TOKEN")
    if direct:
        return direct

    refresh = os.getenv("YOUTUBE_REFRESH_TOKEN")
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    if all([refresh, client_id, client_secret]):
        return refresh_access_token(refresh, client_id, client_secret)

    raise YouTubeUploadError(
        "YouTube OAuth is not configured. Set YOUTUBE_ACCESS_TOKEN or "
        "YOUTUBE_REFRESH_TOKEN + YOUTUBE_CLIENT_ID + YOUTUBE_CLIENT_SECRET."
    )


def upload_resumable(
    video_path: Path,
    story: Dict,
    *,
    access_token: Optional[str] = None,
    privacy_status: str = "private",
) -> Dict:
    if not video_path.exists():
        raise FileNotFoundError(video_path)

    token = access_token or access_token_from_env()
    body = build_video_resource(story, privacy_status=privacy_status)
    mime = mimetypes.guess_type(str(video_path))[0] or "video/mp4"
    size = video_path.stat().st_size

    init = requests.post(
        UPLOAD_ENDPOINT,
        params={"uploadType": "resumable", "part": "snippet,status"},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Upload-Content-Length": str(size),
            "X-Upload-Content-Type": mime,
        },
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        timeout=30,
        allow_redirects=False,
    )
    init.raise_for_status()
    session_url = init.headers.get("Location")
    if not session_url:
        raise YouTubeUploadError("YouTube did not return a resumable upload URL")

    with video_path.open("rb") as handle:
        uploaded = requests.put(
            session_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": mime,
                "Content-Length": str(size),
            },
            data=handle,
            timeout=300,
        )
    uploaded.raise_for_status()
    result = uploaded.json()
    return {
        "platform": "youtube_shorts",
        "status": "uploaded",
        "video_id": result.get("id"),
        "privacy": result.get("status", {}).get("privacyStatus", privacy_status),
        "raw": result,
    }
