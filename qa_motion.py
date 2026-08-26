import json
import subprocess
from pathlib import Path

VIDEO = Path("motion/out/behind-the-number-motion.mp4")


def probe(path: Path) -> dict:
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_type,width,height,duration:format=duration,size",
        "-of", "json", str(path)
    ], text=True)
    return json.loads(raw)


def main() -> None:
    if not VIDEO.exists() or VIDEO.stat().st_size < 500_000:
        raise RuntimeError("MOTION_QA_FAILED: render missing or implausibly small")

    info = probe(VIDEO)
    streams = info.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not video:
        raise RuntimeError("MOTION_QA_FAILED: no video stream")
    if not audio:
        raise RuntimeError("MOTION_QA_FAILED: no audio stream")
    if (video.get("width"), video.get("height")) != (1080, 1920):
        raise RuntimeError(f"MOTION_QA_FAILED: expected 1080x1920, got {video.get('width')}x{video.get('height')}")

    total = float(info.get("format", {}).get("duration") or 0)
    if not 35.0 <= total <= 45.5:
        raise RuntimeError(f"MOTION_QA_FAILED: duration {total:.2f}s outside 35-45.5s target")

    story = Path("motion/public/story.json")
    if not story.exists():
        raise RuntimeError("MOTION_QA_FAILED: story provenance/timeline missing")
    payload = json.loads(story.read_text(encoding="utf-8"))
    if len(payload.get("timeline", [])) != 8:
        raise RuntimeError("MOTION_QA_FAILED: expected 8 synchronized scenes")
    for scene in payload["timeline"]:
        slot = scene["frames"] / payload["fps"]
        if scene["audio_seconds"] > slot - 0.10:
            raise RuntimeError(f"MOTION_QA_FAILED: narration clipping risk in scene {scene['index']}")

    print(json.dumps({
        "motion_qa": "passed",
        "resolution": "1080x1920",
        "duration_seconds": round(total, 2),
        "audio": True,
        "scenes": 8,
    }))


if __name__ == "__main__":
    main()
