import argparse
import json
from pathlib import Path

from src.platforms import publish_all, write_publish_plan


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish the latest approved reel")
    parser.add_argument("--live", action="store_true", help="Enable platform API calls; default is dry-run")
    parser.add_argument("--approval", default="data/state/approval.json")
    parser.add_argument("--video", default="data/output/behind_the_number_first_reel.mp4")
    parser.add_argument("--story", default="data/output/storyboard.json")
    args = parser.parse_args()

    story_path = Path(args.story)
    if not story_path.exists():
        raise FileNotFoundError(story_path)
    story = json.loads(story_path.read_text(encoding="utf-8"))

    results = publish_all(
        video_path=args.video,
        story=story,
        approval_path=args.approval,
        dry_run=not args.live,
    )
    plan = write_publish_plan(results)
    print(f"Publish plan: {plan}")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
