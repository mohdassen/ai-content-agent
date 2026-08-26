from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import requests

PEXELS_VIDEO_SEARCH = "https://api.pexels.com/videos/search"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "BehindTheNumberAI/1.0 (faceless-content-research)"


def _best_vertical_file(video: dict) -> Optional[str]:
    candidates = []
    for f in video.get("video_files", []):
        width = f.get("width") or 0
        height = f.get("height") or 0
        link = f.get("link")
        if not link:
            continue
        portrait_bonus = 1 if height >= width else 0
        pixels = width * height
        candidates.append((portrait_bonus, pixels, link))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][2]


def _download(url: str, dest: Path) -> Path:
    with requests.get(url, stream=True, timeout=60, headers={"User-Agent": USER_AGENT}) as media:
        media.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in media.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)
    return dest


def _commons_query(scene: Dict) -> str:
    prompt = (scene.get("visual_prompt") or "data center artificial intelligence").lower()
    keywords = []
    mapping = [
        ("data center", "data center servers"),
        ("server", "data center servers"),
        ("riyadh", "Riyadh skyline"),
        ("saudi", "Saudi Arabia Riyadh"),
        ("artificial intelligence", "artificial intelligence computing"),
        ("ai", "artificial intelligence computing"),
        ("cloud", "cloud computing data center"),
        ("gpu", "GPU server"),
        ("investment", "Riyadh business skyline"),
    ]
    for needle, query in mapping:
        if needle in prompt and query not in keywords:
            keywords.append(query)
    return " ".join(keywords[:2]) or "data center servers"


def _commons_image(scene: Dict, idx: int, out: Path) -> tuple[Optional[Path], Optional[Dict]]:
    query = _commons_query(scene)
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": 6,
        "gsrlimit": 10,
        "prop": "imageinfo",
        "iiprop": "url|extmetadata|size",
        "iiurlwidth": 1600,
        "format": "json",
        "origin": "*",
    }
    response = requests.get(COMMONS_API, params=params, timeout=25, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()
    pages = list((response.json().get("query", {}).get("pages", {}) or {}).values())

    candidates = []
    for page in pages:
        info_list = page.get("imageinfo") or []
        if not info_list:
            continue
        info = info_list[0]
        thumb = info.get("thumburl") or info.get("url")
        if not thumb:
            continue
        width = info.get("thumbwidth") or info.get("width") or 0
        height = info.get("thumbheight") or info.get("height") or 0
        metadata = info.get("extmetadata") or {}
        license_name = (metadata.get("LicenseShortName") or {}).get("value", "")
        # Commons images should be reusable; reject entries where licensing metadata is absent.
        if not license_name:
            continue
        score = (1 if height >= width else 0, width * height)
        candidates.append((score, page, info, thumb, license_name))

    if not candidates:
        return None, None
    candidates.sort(key=lambda x: x[0], reverse=True)
    _, page, info, thumb, license_name = candidates[0]
    dest = out / f"scene_{idx:02}_commons.jpg"
    _download(thumb, dest)
    meta = info.get("extmetadata") or {}
    attribution = {
        "scene": idx,
        "provider": "Wikimedia Commons",
        "title": page.get("title", ""),
        "source": info.get("descriptionurl", ""),
        "license": license_name,
        "artist": (meta.get("Artist") or {}).get("value", ""),
        "query": query,
    }
    return dest, attribution


def fetch_scene_visuals(story: Dict, output_dir: str = "data/output") -> List[Optional[Path]]:
    """Return a real visual for each scene.

    Priority:
    1. Pexels portrait stock video when PEXELS_API_KEY exists.
    2. Wikimedia Commons reusable imagery without an API key.

    No synthetic test-pattern fallback is returned here. Missing visuals remain None and
    are blocked by the production quality gate.
    """
    key = os.getenv("PEXELS_API_KEY", "").strip()
    result: List[Optional[Path]] = []
    attributions: List[Dict] = []
    out = Path(output_dir) / "visuals"
    out.mkdir(parents=True, exist_ok=True)

    for idx, scene in enumerate(story.get("scenes", []), start=1):
        selected: Optional[Path] = None

        if key:
            query = scene.get("visual_prompt", "technology data center")
            query = query.replace("vertical 9:16", "").replace("realistic documentary style", "")[:120]
            try:
                response = requests.get(
                    PEXELS_VIDEO_SEARCH,
                    headers={"Authorization": key},
                    params={"query": query, "orientation": "portrait", "per_page": 5},
                    timeout=20,
                )
                response.raise_for_status()
                videos = response.json().get("videos", [])
                url = _best_vertical_file(videos[0]) if videos else None
                if url:
                    selected = _download(url, out / f"scene_{idx:02}_pexels.mp4")
                    attributions.append({"scene": idx, "provider": "Pexels", "query": query})
            except Exception:
                selected = None

        if selected is None:
            try:
                selected, attribution = _commons_image(scene, idx, out)
                if attribution:
                    attributions.append(attribution)
            except Exception:
                selected = None

        result.append(selected)

    (Path(output_dir) / "visual_attribution.json").write_text(
        json.dumps(attributions, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result
