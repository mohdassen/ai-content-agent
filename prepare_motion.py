import asyncio
import json
import math
import subprocess
from pathlib import Path

import edge_tts

from src.story import saudi_ai_datacenter_story

FPS = 30
VOICE = "ar-SA-HamedNeural"
RATE = "+18%"
MIN_SCENE_SECONDS = 3.8
TAIL_PAD_SECONDS = 0.55


def duration(path: Path) -> float:
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip()
    return float(raw)


async def synth(text: str, path: Path) -> None:
    await edge_tts.Communicate(text=text, voice=VOICE, rate=RATE).save(str(path))


def write_typescript_timeline(timeline: list[dict], total_frames: int) -> None:
    target = Path("motion/src/generatedTimeline.ts")
    target.parent.mkdir(parents=True, exist_ok=True)
    compact = [
        {
            "index": item["index"],
            "from": item["from"],
            "frames": item["frames"],
            "audio_seconds": item["audio_seconds"],
        }
        for item in timeline
    ]
    target.write_text(
        "export type TimelineScene = {index:number; from:number; frames:number; audio_seconds:number};\n"
        f"export const TIMELINE: TimelineScene[] = {json.dumps(compact, ensure_ascii=False)};\n"
        f"export const TOTAL_FRAMES = {total_frames};\n",
        encoding="utf-8",
    )


def main() -> None:
    story = saudi_ai_datacenter_story()
    public = Path("motion/public")
    audio_dir = public / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    measured = []
    for idx, scene in enumerate(story["scenes"], start=1):
        path = audio_dir / f"scene_{idx:02}.mp3"
        asyncio.run(synth(scene["narration"], path))
        actual = duration(path)
        scene_seconds = max(MIN_SCENE_SECONDS, actual + TAIL_PAD_SECONDS)
        frames = int(math.ceil(scene_seconds * FPS))
        measured.append((idx, scene, actual, frames))

    timeline = []
    cursor = 0
    for idx, scene, actual, frames in measured:
        allowed = frames / FPS
        if actual > allowed - 0.30:
            raise RuntimeError(f"AUDIO_TIMING_INTERNAL_ERROR scene={idx} audio={actual:.2f}s slot={allowed:.2f}s")
        timeline.append({
            "index": idx,
            "from": cursor,
            "frames": frames,
            "audio_seconds": round(actual, 3),
            "narration": scene["narration"],
            "caption": scene["on_screen_text"],
        })
        cursor += frames

    payload = {
        "fps": FPS,
        "durationInFrames": cursor,
        "durationSeconds": round(cursor / FPS, 3),
        "title": story["title"],
        "caption": story["caption"],
        "timeline": timeline,
    }
    (public / "story.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_typescript_timeline(timeline, cursor)
    print(json.dumps({"motion_assets": "ready", "duration_seconds": payload["durationSeconds"], "scenes": len(timeline)}))


if __name__ == "__main__":
    main()
