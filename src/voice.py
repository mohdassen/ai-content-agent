import asyncio
from pathlib import Path
from typing import Dict, List
import subprocess

import edge_tts


DEFAULT_VOICE = "ar-SA-HamedNeural"


async def _synthesize(text: str, output_path: Path, voice: str) -> None:
    # Slightly faster delivery works better for Shorts/Reels while staying natural.
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+8%", volume="+0%")
    await communicate.save(str(output_path))


def synthesize_scene_audio(story: Dict, output_dir: str = "data/output/audio", voice: str = DEFAULT_VOICE) -> List[Path]:
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    outputs: List[Path] = []

    for i, scene in enumerate(story["scenes"], start=1):
        path = folder / f"scene_{i:02}.mp3"
        asyncio.run(_synthesize(scene["narration"], path, voice))
        outputs.append(path)

    return outputs


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def retime_story_to_audio(story: Dict, audio_files: List[Path], tail_padding: float = 0.18) -> Dict:
    """Set scene boundaries from the actual generated speech duration.

    This prevents sentences from being clipped by arbitrary storyboard timings.
    """
    cursor = 0.0
    for scene, audio in zip(story["scenes"], audio_files):
        duration = max(1.0, audio_duration(audio) + tail_padding)
        scene["start"] = round(cursor, 3)
        cursor += duration
        scene["end"] = round(cursor, 3)
    story["duration_seconds"] = round(cursor, 3)
    return story
