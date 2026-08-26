import asyncio
from pathlib import Path
from typing import Dict, List

import edge_tts


DEFAULT_VOICE = "ar-SA-HamedNeural"


async def _synthesize(text: str, output_path: Path, voice: str) -> None:
    communicate = edge_tts.Communicate(text=text, voice=voice, rate="+0%", volume="+0%")
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
