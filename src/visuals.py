from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import requests

PEXELS_VIDEO_SEARCH = "https://api.pexels.com/videos/search"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "BehindTheNumberAI/1.0 (faceless-content-research)"

QUERY_RULES = [
    (("data center", "server", "gpu", "computing"), ["server rack blinking lights", "network server room racks", "data center corridor servers"]),
    (("chip", "semiconductor"), ["computer processor macro", "circuit board microchip macro"]),
    (("fiber",), ["fiber optic cable macro", "network cables server rack"]),
    (("power", "cooling"), ["industrial cooling pipes technology", "electrical substation infrastructure"]),
    (("riyadh", "saudi", "investment"), ["Riyadh skyline night", "Saudi Arabia Riyadh skyline"]),
]

BLOCKED_CONTEXT = {
    "airport", "terminal", "mall", "shopping", "fashion", "travel", "luggage", "hotel",
    "restaurant", "wedding", "warehouse", "boxes", "package", "packing", "delivery",
    "retail", "store", "shelf", "library", "books", "office desk"
}


def _queries(scene: Dict) -> List[str]:
    prompt = (scene.get("visual_prompt") or "").lower()
    queries: List[str] = []
    for needles, options in QUERY_RULES:
        if any(n in prompt for n in needles):
            queries.extend(options)
    return list(dict.fromkeys(queries))[:3] or ["server rack blinking lights", "data center corridor servers"]


def _best_file(video: dict) -> Optional[str]:
    # Landscape/near-square source footage is intentionally preferred. It is cropped to 9:16
    # later and tends to be substantially better for technical stock than weak portrait results.
    candidates = []
    for f in video.get("video_files", []):
        width, height, link = f.get("width") or 0, f.get("height") or 0, f.get("link")
        if not link or width < 720 or height < 720:
            continue
        pixels = width * height
        landscape_bonus = 2 if width >= height else 1
        candidates.append((landscape_bonus, pixels, link))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][2]


def _candidate_text(video: dict) -> str:
    user = video.get("user") or {}
    return " ".join(str(x) for x in [video.get("url", ""), user.get("name", ""), user.get("url", "")] if x).lower()


def _acceptable(video: dict) -> bool:
    text = _candidate_text(video)
    return not any(term in text for term in BLOCKED_CONTEXT)


def _download(url: str, dest: Path) -> Path:
    with requests.get(url, stream=True, timeout=60, headers={"User-Agent": USER_AGENT}) as media:
        media.raise_for_status()
        with dest.open("wb") as fh:
            for chunk in media.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    fh.write(chunk)
    return dest


def _commons_image(scene: Dict, idx: int, out: Path) -> tuple[Optional[Path], Optional[Dict]]:
    query = _queries(scene)[0]
    params = {"action": "query", "generator": "search", "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6, "gsrlimit": 10, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1600, "format": "json", "origin": "*"}
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
        metadata = info.get("extmetadata") or {}
        license_name = (metadata.get("LicenseShortName") or {}).get("value", "")
        title = page.get("title", "").lower()
        if not thumb or not license_name or any(term in title for term in BLOCKED_CONTEXT):
            continue
        width, height = info.get("thumbwidth") or info.get("width") or 0, info.get("thumbheight") or info.get("height") or 0
        candidates.append((width * height, page, info, thumb, license_name))
    if not candidates:
        return None, None
    candidates.sort(key=lambda x: x[0], reverse=True)
    _, page, info, thumb, license_name = candidates[0]
    dest = _download(thumb, out / f"scene_{idx:02}_commons.jpg")
    meta = info.get("extmetadata") or {}
    return dest, {"scene": idx, "provider": "Wikimedia Commons", "title": page.get("title", ""), "source": info.get("descriptionurl", ""), "license": license_name, "artist": (meta.get("Artist") or {}).get("value", ""), "query": query}


def fetch_scene_visuals(story: Dict, output_dir: str = "data/output") -> List[Optional[Path]]:
    key = os.getenv("PEXELS_API_KEY", "").strip()
    result: List[Optional[Path]] = []
    attributions: List[Dict] = []
    out = Path(output_dir) / "visuals"
    out.mkdir(parents=True, exist_ok=True)
    for idx, scene in enumerate(story.get("scenes", []), start=1):
        selected: Optional[Path] = None
        if key:
            try:
                urls: List[tuple[str, str]] = []
                for query in _queries(scene):
                    response = requests.get(PEXELS_VIDEO_SEARCH, headers={"Authorization": key}, params={"query": query, "per_page": 25, "size": "large"}, timeout=20)
                    response.raise_for_status()
                    for video in response.json().get("videos", []):
                        if not _acceptable(video):
                            continue
                        url = _best_file(video)
                        if url and all(url != existing[0] for existing in urls):
                            urls.append((url, query))
                        if len(urls) >= 2:
                            break
                    if len(urls) >= 2:
                        break
                if urls:
                    selected = _download(urls[0][0], out / f"scene_{idx:02}_pexels.mp4")
                    attributions.append({"scene": idx, "provider": "Pexels", "query": urls[0][1], "role": "primary", "relevance_gate": "passed"})
                if len(urls) > 1:
                    _download(urls[1][0], out / f"scene_{idx:02}_pexels_alt.mp4")
                    attributions.append({"scene": idx, "provider": "Pexels", "query": urls[1][1], "role": "alternate", "relevance_gate": "passed"})
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
    (Path(output_dir) / "visual_attribution.json").write_text(json.dumps(attributions, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
