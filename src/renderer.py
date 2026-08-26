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
        start = _ts(scene["start"])
        end = _ts(scene["end"])
        blocks.append(f"{i}\n{start} --> {end}\n{scene['narration']}\n")
    path.write_text("\n".join(blocks), encoding="utf-8")
    return path


def _ts(seconds: int) -> str:
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02}:{m:02}:{s:02},000"
