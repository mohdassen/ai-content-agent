import json
import subprocess
from pathlib import Path

VIDEO = Path("motion/out/behind-the-number-motion.mp4")
MASTER_AUDIO = Path("motion/public/audio/master_narration.mp3")


def probe(path: Path) -> dict:
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,width,height,duration:format=duration,size",
        "-of", "json", str(path)
    ], text=True)
    return json.loads(raw)


def media_duration(path: Path) -> float:
    info = probe(path)
    return float(info.get("format", {}).get("duration") or 0)


def main() -> None:
    if not VIDEO.exists() or VIDEO.stat().st_size < 500_000:
        raise RuntimeError("MOTION_QA_FAILED: render missing or implausibly small")
    if not MASTER_AUDIO.exists() or MASTER_AUDIO.stat().st_size < 50_000:
        raise RuntimeError("MOTION_QA_FAILED: continuous master narration missing")

    info = probe(VIDEO)
    streams = info.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not video or not audio:
        raise RuntimeError("MOTION_QA_FAILED: render must contain video and audio")
    if (video.get("width"), video.get("height")) != (1080, 1920):
        raise RuntimeError(f"MOTION_QA_FAILED: expected 1080x1920, got {video.get('width')}x{video.get('height')}")

    total = media_duration(VIDEO)
    master = media_duration(MASTER_AUDIO)
    if not 30.0 <= total <= 70.0:
        raise RuntimeError(f"MOTION_QA_FAILED: duration {total:.2f}s outside short-form safety range")
    if total < master + 0.20:
        raise RuntimeError(f"MOTION_QA_FAILED: final video {total:.2f}s is not long enough for master narration {master:.2f}s")

    story = Path("motion/public/story.json")
    if not story.exists():
        raise RuntimeError("MOTION_QA_FAILED: story provenance/timeline missing")
    payload = json.loads(story.read_text(encoding="utf-8"))
    if len(payload.get("timeline", [])) != 8:
        raise RuntimeError("MOTION_QA_FAILED: expected 8 synchronized scenes")
    declared_master = float(payload.get("masterAudioSeconds") or 0)
    if declared_master and abs(declared_master - master) > 0.25:
        raise RuntimeError("MOTION_QA_FAILED: master narration metadata mismatch")

    print(json.dumps({
        "motion_qa": "passed",
        "resolution": "1080x1920",
        "duration_seconds": round(total, 2),
        "master_audio_seconds": round(master, 2),
        "continuous_narration": True,
        "scenes": 8,
    }))


if __name__ == "__main__":
    main()
