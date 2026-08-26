import asyncio
import json
import subprocess
from pathlib import Path

import edge_tts

from src.story import saudi_ai_datacenter_story

FPS = 30
SCENE_FRAMES = [150, 150, 150, 150, 150, 150, 150, 150]
VOICE = "ar-SA-HamedNeural"
RATE = "+12%"


def duration(path: Path) -> float:
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip()
    return float(raw)


async def synth(text: str, path: Path) -> None:
    await edge_tts.Communicate(text=text, voice=VOICE, rate=RATE).save(str(path))


def main() -> None:
    story = saudi_ai_datacenter_story()
    public = Path("motion/public")
    audio_dir = public / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    timeline = []
    cursor = 0
    for idx, (scene, frames) in enumerate(zip(story["scenes"], SCENE_FRAMES), start=1):
        path = audio_dir / f"scene_{idx:02}.mp3"
        asyncio.run(synth(scene["narration"], path))
        actual = duration(path)
        allowed = frames / FPS
        # Never permit Remotion Sequence timing to clip narration.
        if actual > allowed - 0.10:
            raise RuntimeError(
                f"AUDIO_TOO_LONG scene={idx} audio={actual:.2f}s slot={allowed:.2f}s; shorten narration or extend timeline"
            )
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
        "durationSeconds": cursor / FPS,
        "title": story["title"],
        "caption": story["caption"],
        "timeline": timeline,
    }
    (public / "story.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"motion_assets": "ready", "duration_seconds": payload["durationSeconds"], "scenes": len(timeline)}))


if __name__ == "__main__":
    main()
