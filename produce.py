from src.renderer import write_srt, write_storyboard
from src.story import saudi_ai_datacenter_story
from src.video import compose_vertical_video
from src.visuals import fetch_scene_visuals
from src.voice import synthesize_scene_audio


def main() -> None:
    story = saudi_ai_datacenter_story()
    board = write_storyboard(story)
    subtitles = write_srt(story)
    audio_files = synthesize_scene_audio(story)
    visual_files = fetch_scene_visuals(story)
    video = compose_vertical_video(story, audio_files, subtitles, visual_files=visual_files)

    real_visuals = sum(1 for item in visual_files if item is not None)
    print(f"Storyboard: {board}")
    print(f"Subtitles: {subtitles}")
    print(f"Audio scenes: {len(audio_files)}")
    print(f"Real stock visuals: {real_visuals}/{len(visual_files)}")
    print(f"Video: {video}")
    print(f"Title: {story['title']}")
    print("Publishing remains disabled until approval and platform credentials are configured.")


if __name__ == "__main__":
    main()
