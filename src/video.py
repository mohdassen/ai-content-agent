from pathlib import Path
from typing import Dict, List
import subprocess


def _run(cmd: List[str]) -> None:
    subprocess.run(cmd, check=True)


def _escape_ass_path(path: Path) -> str:
    return str(path).replace('\\', '/').replace(':', '\\:').replace("'", "\\'")


def compose_vertical_video(story: Dict, audio_files: List[Path], subtitles_path: Path, output_dir: str = "data/output") -> Path:
    out = Path(output_dir)
    scenes_dir = out / "scene_video"
    scenes_dir.mkdir(parents=True, exist_ok=True)
    scene_paths: List[Path] = []

    for idx, (scene, audio) in enumerate(zip(story["scenes"], audio_files), start=1):
        duration = max(1, int(scene["end"]) - int(scene["start"]))
        scene_path = scenes_dir / f"scene_{idx:02}.mp4"
        # MVP visual bed: subtle animated test pattern, scaled/cropped for 9:16.
        # A dedicated AI visual provider can replace this input later without changing the pipeline.
        vf = (
            "testsrc2=size=1080x1920:rate=30,"
            "eq=brightness=-0.45:saturation=0.35,"
            "drawbox=x=70:y=150:w=940:h=300:color=black@0.45:t=fill"
        )
        _run([
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", vf,
            "-i", str(audio),
            "-t", str(duration),
            "-vf", "format=yuv420p",
            "-af", f"apad=pad_dur={duration}",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
            "-c:a", "aac", "-b:a", "128k",
            "-shortest", str(scene_path)
        ])
        scene_paths.append(scene_path)

    concat_file = out / "concat.txt"
    concat_file.write_text("\n".join(f"file '{p.resolve()}'" for p in scene_paths), encoding="utf-8")
    joined = out / "joined.mp4"
    _run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(joined)])

    final_path = out / "behind_the_number_first_reel.mp4"
    sub = _escape_ass_path(subtitles_path.resolve())
    subtitle_filter = (
        f"subtitles='{sub}':force_style='FontName=Noto Sans Arabic,FontSize=22,"
        "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3,"
        "Shadow=1,Alignment=2,MarginV=170'"
    )
    _run([
        "ffmpeg", "-y", "-i", str(joined),
        "-vf", subtitle_filter,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "copy", "-movflags", "+faststart", str(final_path)
    ])
    return final_path
