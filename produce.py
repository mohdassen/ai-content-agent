from src.renderer import write_srt, write_storyboard
from src.story import saudi_ai_datacenter_story


def main() -> None:
    story = saudi_ai_datacenter_story()
    board = write_storyboard(story)
    subtitles = write_srt(story)
    print(f"Storyboard: {board}")
    print(f"Subtitles: {subtitles}")
    print(f"Title: {story['title']}")
    print("Next gate: voice and visual providers. Publishing remains disabled.")


if __name__ == "__main__":
    main()
