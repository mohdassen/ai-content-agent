from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class PerformanceSnapshot:
    platform: str
    content_id: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    followers_gained: int = 0
    avg_watch_seconds: float = 0.0
    completion_rate: float = 0.0


def normalized_score(item: PerformanceSnapshot) -> float:
    """Heuristic 0-10 content performance score.

    It intentionally rewards retention/share signals more than raw views so the
    learning engine does not chase vanity metrics alone.
    """
    views = max(item.views, 1)
    share_rate = item.shares / views
    comment_rate = item.comments / views
    follower_rate = item.followers_gained / views

    score = (
        min(item.completion_rate, 1.0) * 4.0
        + min(share_rate / 0.02, 1.0) * 2.0
        + min(comment_rate / 0.01, 1.0) * 1.0
        + min(follower_rate / 0.01, 1.0) * 2.0
        + min(item.avg_watch_seconds / 45.0, 1.0) * 1.0
    )
    return round(min(score, 10.0), 2)


def write_snapshot(snapshot: PerformanceSnapshot, output_dir: str = "data/analytics") -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{snapshot.platform}_{snapshot.content_id}.json"
    payload: Dict = asdict(snapshot)
    payload["performance_score"] = normalized_score(snapshot)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def rank_content(items: List[PerformanceSnapshot]) -> List[Dict]:
    results = [dict(asdict(x), performance_score=normalized_score(x)) for x in items]
    return sorted(results, key=lambda x: x["performance_score"], reverse=True)
