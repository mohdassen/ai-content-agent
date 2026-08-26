from pathlib import Path
from typing import Dict, List, Optional
import json
import subprocess


def _run(cmd: List[str]) -> None:
    subprocess.run(cmd, check=True)


def _duration(path: Path) -> float:
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "json", str(path)
    ], text=True)
    return float(json.loads(raw)["format"]["duration"])


def _stream_durations(path: Path) -> Dict[str, float]:
    raw = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration",
        "-of", "json", str(path)
    ], text=True)
    result: Dict[str, float] = {}
    for stream in json.loads(raw).get("streams", []):
        if stream.get("duration") not in (None, "N/A"):
            result[stream["codec_type"]] = float(stream["duration"])
    return result


def _escape_ass_path(path: Path) -> str:
    return str(path).replace('\\', '/').replace(':', '\\:').replace("'", "\\'")


def _render_single_visual(visual: Path, audio: Path, duration: float, scene_path: Path) -> None:
    suffix = visual.suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        vf = (
            "scale=1600:-2:force_original_aspect_ratio=increase,crop=1080:1920,"
            "zoompan=z='min(zoom+0.0016,1.14)':x='iw/2-(iw/zoom/2)':"
            "y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,"
            "eq=contrast=1.06:saturation=1.02,format=yuv420p"
        )
        video_input = ["-loop", "1", "-i", str(visual)]
    else:
        vf = (
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "fps=30,eq=contrast=1.05:saturation=1.02,format=yuv420p"
        )
        video_input = ["-stream_loop", "-1", "-i", str(visual)]
    _run([
        "ffmpeg", "-y", *video_input, "-i", str(audio),
        "-map", "0:v:0", "-map", "1:a:0", "-t", f"{duration:.3f}",
        "-vf", vf, "-af", f"apad=whole_dur={duration:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-pix_fmt", "yuv420p", str(scene_path)
    ])


def _render_dual_visual(primary: Path, alternate: Path, audio: Path, duration: float, scene_path: Path) -> None:
    half = max(1.0, duration / 2.0)
    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=contrast=1.05:saturation=1.03,format=yuv420p"
    _run([
        "ffmpeg", "-y",
        "-stream_loop", "-1", "-i", str(primary),
        "-stream_loop", "-1", "-i", str(alternate),
        "-i", str(audio),
        "-filter_complex",
        f"[0:v]{vf},trim=duration={half:.3f},setpts=PTS-STARTPTS[v0];"
        f"[1:v]{vf},trim=duration={max(1.0, duration-half):.3f},setpts=PTS-STARTPTS[v1];"
        "[v0][v1]concat=n=2:v=1:a=0[v]",
        "-map", "[v]", "-map", "2:a:0", "-t", f"{duration:.3f}",
        "-af", f"apad=whole_dur={duration:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-pix_fmt", "yuv420p", str(scene_path)
    ])


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
        audio_duration = _duration(audio)
        duration = audio_duration + 0.45
        scene_path = scenes_dir / f"scene_{idx:02}.mp4"
        visual = visual_files[idx - 1] if idx - 1 < len(visual_files) else None
        if not visual or not visual.exists():
            raise RuntimeError(f"Missing real visual for scene {idx}; rendering aborted")

        alternate = visual.parent / f"scene_{idx:02}_pexels_alt.mp4"
        if visual.suffix.lower() == ".mp4" and alternate.exists():
            _render_dual_visual(visual, alternate, audio, duration, scene_path)
        else:
            _render_single_visual(visual, audio, duration, scene_path)
        scene_paths.append(scene_path)

    concat_file = out / "concat.txt"
    concat_file.write_text("\n".join(f"file '{p.resolve()}'" for p in scene_paths), encoding="utf-8")
    joined = out / "joined.mp4"
    _run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-c:a", "aac", "-b:a", "160k", "-pix_fmt", "yuv420p", str(joined)
    ])

    final_path = out / "behind_the_number_first_reel.mp4"
    sub = _escape_ass_path(subtitles_path.resolve())
    subtitle_filter = (
        f"subtitles='{sub}':force_style='FontName=Noto Sans Arabic,FontSize=20,"
        "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H55000000,"
        "BorderStyle=3,Outline=2,Shadow=0,Alignment=2,MarginV=150'"
    )
    _run([
        "ffmpeg", "-y", "-i", str(joined), "-vf", subtitle_filter,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(final_path)
    ])

    streams = _stream_durations(final_path)
    vdur, adur = streams.get("video", 0.0), streams.get("audio", 0.0)
    if not vdur or not adur or abs(vdur - adur) > 0.75:
        raise RuntimeError(
            f"AV_QUALITY_GATE_FAILED: video={vdur:.2f}s audio={adur:.2f}s; review delivery blocked"
        )
    return final_path
