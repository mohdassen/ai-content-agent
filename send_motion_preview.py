from pathlib import Path

from src.story import saudi_ai_datacenter_story
from src.telegram_gate import TelegramApprovalGate


def main() -> None:
    video = Path("motion/out/behind-the-number-motion.mp4")
    if not video.exists():
        raise RuntimeError("Remotion video is missing")
    story = saudi_ai_datacenter_story()
    result = TelegramApprovalGate().request_approval(story, video, output_dir="motion/out")
    print(f"Motion preview delivery: {result.get('delivery')}")


if __name__ == "__main__":
    main()
