from src.renderer import write_srt, write_storyboard
from src.story import saudi_ai_datacenter_story
from src.telegram_gate import TelegramApprovalGate
from src.video import compose_vertical_video
from src.visuals import fetch_scene_visuals
from src.voice import synthesize_scene_audio


MIN_REAL_VISUAL_RATIO = 1.0


def main() -> None:
    story = saudi_ai_datacenter_story()
    board = write_storyboard(story)
    subtitles = write_srt(story)
    audio_files = synthesize_scene_audio(story)
    visual_files = fetch_scene_visuals(story)

    total_scenes = len(story.get("scenes", []))
    real_visuals = sum(1 for item in visual_files if item is not None)
    visual_ratio = (real_visuals / total_scenes) if total_scenes else 0.0

    print(f"Storyboard: {board}")
    print(f"Subtitles: {subtitles}")
    print(f"Audio scenes: {len(audio_files)}")
    print(f"Real stock visuals: {real_visuals}/{total_scenes}")

    # Hard quality gate: never send a synthetic test-pattern/fallback reel for approval.
    # Every scene must have a real visual before the review video is rendered.
    if visual_ratio < MIN_REAL_VISUAL_RATIO:
        missing = [str(i + 1) for i, item in enumerate(visual_files) if item is None]
        raise RuntimeError(
            "VISUAL_QUALITY_GATE_FAILED: real visuals are required for every scene. "
            f"Missing scenes: {', '.join(missing)}. "
            "Configure PEXELS_API_KEY or another approved visual provider before review delivery."
        )

    video = compose_vertical_video(story, audio_files, subtitles, visual_files=visual_files)
    approval = TelegramApprovalGate().request_approval(story, video)

    print(f"Video: {video}")
    print(f"Approval delivery: {approval.get('delivery')}")
    print(f"Title: {story['title']}")
    print("Publishing remains disabled until an explicit approval is recorded.")


if __name__ == "__main__":
    main()
