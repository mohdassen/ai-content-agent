from pathlib import Path
from typing import Dict, List


def _ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _esc(text: str) -> str:
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}")


def build_motion_ass(story: Dict, scene_durations: List[float], output_dir: str = "data/output") -> Path:
    """Create lightweight branded motion graphics without external paid services.

    The number/keyword card appears briefly in the upper safe area while normal Arabic
    subtitles remain in the lower safe area. libass handles Arabic shaping and bidi.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "motion_graphics.ass"
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Metric,Noto Sans Arabic,74,&H00FFFFFF,&H00FFFFFF,&H00101010,&H7A101010,-1,0,0,0,100,100,0,0,3,2,0,8,90,90,250,1
Style: Brand,Noto Sans Arabic,26,&H00FFFFFF,&H00FFFFFF,&H00101010,&H70101010,-1,0,0,0,100,100,0,0,3,1,0,8,90,90,115,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    lines = [header]
    cursor = 0.0
    scenes = story.get("scenes", [])
    for idx, duration in enumerate(scene_durations):
        scene = scenes[idx] if idx < len(scenes) else {}
        metric = str(scene.get("on_screen_text", "")).strip()
        if metric:
            show_for = min(2.35, max(1.4, duration * 0.42))
            start, end = cursor + 0.12, cursor + show_for
            # Fade + gentle vertical movement gives a clean explainer-card feel.
            text = r"{\fad(120,180)\move(540,285,540,255)}" + _esc(metric)
            lines.append(f"Dialogue: 2,{_ass_time(start)},{_ass_time(end)},Metric,,0,0,0,,{text}\n")
        # Tiny persistent brand marker, intentionally subtle.
        if idx == 0:
            lines.append(f"Dialogue: 1,{_ass_time(cursor)},{_ass_time(cursor + duration)},Brand,,0,0,0,,خلف الرقم\n")
        cursor += duration
    path.write_text("".join(lines), encoding="utf-8")
    return path
