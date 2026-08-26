from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Optional
import requests

PEXELS_VIDEO_SEARCH = "https://api.pexels.com/videos/search"


def _best_vertical_file(video: dict) -> Optional[str]:
    candidates = []
    for f in video.get("video_files", []):
        width = f.get("width") or 0
        height = f.get("height") or 0
        link = f.get("link")
        if not link:
            continue
        # Prefer portrait, then higher resolution while keeping download sizes reasonable.
        portrait_bonus = 1 if height >= width else 0
        pixels = width * height
        candidates.append((portrait_bonus, pixels, link))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][2]


def fetch_scene_visuals(story: Dict, output_dir: str = "data/output") -> List[Optional[Path]]:
    """Fetch royalty-free stock video when PEXELS_API_KEY is configured.

    The function is intentionally optional. When no API key is present or a request fails,
    it returns None for that scene and the video composer uses its built-in motion-graphic fallback.
    """
    key = os.getenv("PEXELS_API_KEY", "").strip()
    result: List[Optional[Path]] = []
    out = Path(output_dir) / "visuals"
    out.mkdir(parents=True, exist_ok=True)

    if not key:
        return [None for _ in story.get("scenes", [])]

    headers = {"Authorization": key}
    for idx, scene in enumerate(story.get("scenes", []), start=1):
        query = scene.get("visual_prompt", "technology data center")
        # Reduce highly descriptive AI prompts to search-friendly terms.
        query = query.replace("vertical 9:16", "").replace("realistic documentary style", "")[:120]
        try:
            response = requests.get(
                PEXELS_VIDEO_SEARCH,
                headers=headers,
                params={"query": query, "orientation": "portrait", "per_page": 5},
                timeout=20,
            )
            response.raise_for_status()
            videos = response.json().get("videos", [])
            url = _best_vertical_file(videos[0]) if videos else None
            if not url:
                result.append(None)
                continue
            dest = out / f"scene_{idx:02}.mp4"
            with requests.get(url, stream=True, timeout=60) as media:
                media.raise_for_status()
                with dest.open("wb") as fh:
                    for chunk in media.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            fh.write(chunk)
            result.append(dest)
        except Exception:
            result.append(None)
    return result
