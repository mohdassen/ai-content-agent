from pathlib import Path
from typing import Dict, List, Optional
import subprocess


def _run(cmd: List[str]) -> None:
    subprocess.run(cmd, check=True)


def _escape_ass_path(path: Path) -> str:
    return str(path).replace('\\', '/').replace(':', '\\:').replace("'", "\\'")


def compose_vertical_video(
    story: Dict,
    audio_files: List[Path],
    subtitles_path: Path,
    visual_files: Optional[List[Optional[Path]]] = None,
    output_dir: str = "data/output",
) -> Path:
    out = Path(output_dir)
    scenes_dir = out / "scene_video"
    scenes_dir.mkdir(parents=True, exist_ok=True)
    scene_paths: List[Path] = []
    visual_files = visual_files or [None for _ in story.get("scenes", [])]

    for idx, (scene, audio) in enumerate(zip(story["scenes"], audio_files), start=1):
        duration = max(1, int(scene["end"]) - int(scene["start"]))
        scene_path = scenes_dir / f"scene_{idx:02}.mp4"
        visual = visual_files[idx - 1] if idx - 1 < len(visual_files) else None

        if not visual or not visual.exists():
            raise RuntimeError(f"Missing real visual for scene {idx}; rendering aborted")

        suffix = visual.suffix.lower()
        if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
            # Still image: elegant Ken Burns motion to create a documentary-style vertical scene.
            vf = (
                "scale=1600:-2:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "zoompan=z='min(zoom+0.0012,1.12)':x='iw/2-(iw/zoom/2)':"
                "y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
                "eq=contrast=1.04:saturation=0.92,format=yuv420p"
            )
            _run([
                "ffmpeg", "-y", "-loop", "1", "-i", str(visual),
                "-i", str(audio),
                "-t", str(duration),
                "-vf", vf,
                "-af", f"apad=pad_dur={duration}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
                "-c:a", "aac", "-b:a", "128k", "-shortest", str(scene_path)
            ])
        else:
            vf = (
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,"
                "zoompan=z='min(zoom+0.0007,1.08)':d=1:s=1080x1920:fps=30,"
                "eq=contrast=1.03:saturation=0.95,format=yuv420p"
            )
            _run([
                "ffmpeg", "-y", "-stream_loop", "-1", "-i", str(visual),
                "-i", str(audio),
                "-t", str(duration),
                "-vf", vf,
                "-af", f"apad=pad_dur={duration}",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
                "-c:a", "aac", "-b:a", "128k", "-shortest", str(scene_path)
            ])
        scene_paths.append(scene_path)

    concat_file = out / "concat.txt"
    concat_file.write_text("\n".join(f"file '{p.resolve()}'" for p in scene_paths), encoding="utf-8")
    joined = out / "joined.mp4"
    _run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(joined)])

    final_path = out / "behind_the_number_first_reel.mp4"
    sub = _escape_ass_path(subtitles_path.resolve())
    subtitle_filter = (
        f"subtitles='{sub}':force_style='FontName=Noto Sans Arabic,FontSize=20,"
        "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,"
        "Shadow=1,Alignment=2,MarginV=150'"
    )
    _run([
        "ffmpeg", "-y", "-i", str(joined),
        "-vf", subtitle_filter,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-c:a", "copy", "-movflags", "+faststart", str(final_path)
    ])
    return final_path
