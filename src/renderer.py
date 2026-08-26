import json
from pathlib import Path
from typing import Dict


def write_storyboard(story: Dict, output_dir: str = "data/output") -> Path:
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "storyboard.json"
    path.write_text(json.dumps(story, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def write_srt(story: Dict, output_dir: str = "data/output") -> Path:
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "subtitles.srt"
    blocks = []
    for i, scene in enumerate(story["scenes"], start=1):
        start = _ts(float(scene["start"]))
        end = _ts(float(scene["end"]))
        blocks.append(f"{i}\n{start} --> {end}\n{scene['narration']}\n")
    path.write_text("\n".join(blocks), encoding="utf-8")
    return path


def _ts(seconds: float) -> str:
    total_ms = max(0, int(round(seconds * 1000)))
    h, rem = divmod(total_ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
