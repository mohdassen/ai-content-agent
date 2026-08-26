from pathlib import Path
from typing import Dict, List, Optional
import json
import subprocess


def _run(cmd: List[str]) -> None:
    subprocess.run(cmd, check=True)


def _duration(path: Path) -> float:
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)], text=True)
    return float(json.loads(raw)["format"]["duration"])


def _stream_durations(path: Path) -> Dict[str, float]:
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration", "-of", "json", str(path)], text=True)
    result: Dict[str, float] = {}
    for stream in json.loads(raw).get("streams", []):
        if stream.get("duration") not in (None, "N/A"):
            result[stream["codec_type"]] = float(stream["duration"])
    return result


def _escape_ass_path(path: Path) -> str:
    return str(path).replace('\\', '/').replace(':', '\\:').replace("'", "\\'")


def _escape_drawtext(text: str) -> str:
    return text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace("%", "\\%")


def _base_vf() -> str:
    return "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,eq=contrast=1.07:saturation=1.04"


def _overlay_filter(text: str, duration: float) -> str:
    safe = _escape_drawtext(text)
    # Noto Kufi Arabic contains Arabic glyphs as well as Latin/digits, avoiding tofu squares.
    # Place the headline in the upper safe zone; subtitles live near the bottom.
    return (
        f"drawtext=text='{safe}':font='Noto Kufi Arabic':fontsize=62:fontcolor=white:"
        "borderw=3:bordercolor=black@0.70:box=1:boxcolor=black@0.30:boxborderw=20:"
        "x=(w-text_w)/2:y=h*0.13:"
        f"enable='between(t,0,{min(duration, 2.2):.2f})',format=yuv420p"
    )


def _render_single_visual(visual: Path, audio: Path, duration: float, scene_path: Path, text: str) -> None:
    suffix = visual.suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        vf = _base_vf() + ",zoompan=z='min(zoom+0.0022,1.16)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30," + _overlay_filter(text, duration)
        video_input = ["-loop", "1", "-i", str(visual)]
    else:
        vf = _base_vf() + "," + _overlay_filter(text, duration)
        video_input = ["-stream_loop", "-1", "-i", str(visual)]
    _run(["ffmpeg", "-y", *video_input, "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0", "-t", f"{duration:.3f}", "-vf", vf, "-af", f"apad=whole_dur={duration:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-pix_fmt", "yuv420p", str(scene_path)])


def _render_dual_visual(primary: Path, alternate: Path, audio: Path, duration: float, scene_path: Path, text: str) -> None:
    first = min(2.2, max(1.2, duration * 0.45))
    second = max(0.8, duration - first)
    base = _base_vf()
    overlay = _overlay_filter(text, duration)
    _run(["ffmpeg", "-y", "-stream_loop", "-1", "-i", str(primary), "-stream_loop", "-1", "-i", str(alternate), "-i", str(audio), "-filter_complex", f"[0:v]{base},trim=duration={first:.3f},setpts=PTS-STARTPTS[v0];[1:v]{base},trim=duration={second:.3f},setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0,{overlay}[v]", "-map", "[v]", "-map", "2:a:0", "-t", f"{duration:.3f}", "-af", f"apad=whole_dur={duration:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-pix_fmt", "yuv420p", str(scene_path)])


def compose_vertical_video(story: Dict, audio_files: List[Path], subtitles_path: Path, visual_files: Optional[List[Optional[Path]]] = None, output_dir: str = "data/output") -> Path:
    out = Path(output_dir)
    scenes_dir = out / "scene_video"
    scenes_dir.mkdir(parents=True, exist_ok=True)
    scene_paths: List[Path] = []
    visual_files = visual_files or [None for _ in story.get("scenes", [])]
    for idx, (scene, audio) in enumerate(zip(story["scenes"], audio_files), start=1):
        audio_duration = _duration(audio)
        duration = audio_duration + 0.18
        scene_path = scenes_dir / f"scene_{idx:02}.mp4"
        visual = visual_files[idx - 1] if idx - 1 < len(visual_files) else None
        if not visual or not visual.exists():
            raise RuntimeError(f"Missing real visual for scene {idx}; rendering aborted")
        alternate = visual.parent / f"scene_{idx:02}_pexels_alt.mp4"
        text = scene.get("on_screen_text", "")
        if visual.suffix.lower() == ".mp4" and alternate.exists():
            _render_dual_visual(visual, alternate, audio, duration, scene_path, text)
        else:
            _render_single_visual(visual, audio, duration, scene_path, text)
        scene_paths.append(scene_path)
    concat_file = out / "concat.txt"
    concat_file.write_text("\n".join(f"file '{p.resolve()}'" for p in scene_paths), encoding="utf-8")
    joined = out / "joined.mp4"
    _run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-pix_fmt", "yuv420p", str(joined)])
    final_path = out / "behind_the_number_first_reel.mp4"
    sub = _escape_ass_path(subtitles_path.resolve())
    subtitle_filter = (
        f"subtitles='{sub}':force_style='FontName=Noto Kufi Arabic,FontSize=18,"
        "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H78000000,"
        "BorderStyle=3,Outline=1,Shadow=0,Alignment=2,MarginL=80,MarginR=80,MarginV=245'"
    )
    _run(["ffmpeg", "-y", "-i", str(joined), "-vf", subtitle_filter, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(final_path)])
    streams = _stream_durations(final_path)
    vdur, adur = streams.get("video", 0.0), streams.get("audio", 0.0)
    if not vdur or not adur or abs(vdur - adur) > 0.75:
        raise RuntimeError(f"AV_QUALITY_GATE_FAILED: video={vdur:.2f}s audio={adur:.2f}s; review delivery blocked")
    return final_path
