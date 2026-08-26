import asyncio
import json
import math
import subprocess
from pathlib import Path

import edge_tts

from src.story import saudi_ai_datacenter_story

FPS = 30
VOICE = "ar-SA-HamedNeural"
RATE = "+14%"
MIN_SCENE_SECONDS = 3.2
TAIL_PAD_SECONDS = 0.28


def duration(path: Path) -> float:
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path)
    ], text=True).strip()
    return float(raw)


async def synth(text: str, path: Path) -> None:
    await edge_tts.Communicate(text=text, voice=VOICE, rate=RATE).save(str(path))


def add_tail_silence(source: Path, dest: Path, seconds: float) -> None:
    total = duration(source) + seconds
    subprocess.run([
        "ffmpeg", "-y", "-i", str(source), "-af", f"apad=pad_dur={seconds}",
        "-t", f"{total:.3f}", "-c:a", "libmp3lame", "-b:a", "160k", str(dest),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def concat_audio(files: list[Path], output: Path) -> None:
    concat = output.parent / "narration_concat.txt"
    concat.write_text("\n".join(f"file '{p.resolve()}'" for p in files), encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-c:a", "libmp3lame", "-b:a", "192k", str(output),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def write_typescript_timeline(timeline: list[dict], total_frames: int) -> None:
    target = Path("motion/src/generatedTimeline.ts")
    target.parent.mkdir(parents=True, exist_ok=True)
    compact = [{"index": x["index"], "from": x["from"], "frames": x["frames"], "audio_seconds": x["audio_seconds"]} for x in timeline]
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

    timeline = []
    cursor = 0
    padded_files: list[Path] = []

    for idx, scene in enumerate(story["scenes"], start=1):
        raw_path = audio_dir / f"scene_{idx:02}_raw.mp3"
        padded_path = audio_dir / f"scene_{idx:02}.mp3"
        asyncio.run(synth(scene["narration"], raw_path))
        actual = duration(raw_path)
        if actual < 0.8:
            raise RuntimeError(f"AUDIO_INVALID scene={idx} duration={actual:.2f}s")
        add_tail_silence(raw_path, padded_path, TAIL_PAD_SECONDS)
        slot_seconds = max(MIN_SCENE_SECONDS, duration(padded_path))
        frames = int(math.ceil(slot_seconds * FPS))
        timeline.append({
            "index": idx,
            "from": cursor,
            "frames": frames,
            "audio_seconds": round(actual, 3),
            "narration": scene["narration"],
            "caption": scene["on_screen_text"],
        })
        padded_files.append(padded_path)
        cursor += frames

    master = audio_dir / "master_narration.mp3"
    concat_audio(padded_files, master)
    master_seconds = duration(master)
    total_frames = max(cursor, int(math.ceil((master_seconds + 0.35) * FPS)))

    payload = {
        "fps": FPS,
        "durationInFrames": total_frames,
        "durationSeconds": round(total_frames / FPS, 3),
        "masterAudioSeconds": round(master_seconds, 3),
        "title": story["title"],
        "caption": story["caption"],
        "timeline": timeline,
    }
    (public / "story.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_typescript_timeline(timeline, total_frames)
    print(json.dumps({"motion_assets": "ready", "duration_seconds": payload["durationSeconds"], "master_audio_seconds": payload["masterAudioSeconds"], "scenes": len(timeline)}))


if __name__ == "__main__":
    main()
