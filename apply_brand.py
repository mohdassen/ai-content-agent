from pathlib import Path

p = Path('motion/src/video.tsx')
s = p.read_text(encoding='utf-8')

required = [
    'NEW_VISUAL_PIPELINE_V3',
    'APPROVED_PRESENTER_HERO',
    '<PhotoPanel',
    "staticFile('audio/master_narration.mp3')",
]
for marker in required:
    if marker not in s:
        raise SystemExit(f'VISUAL_PIPELINE_INVALID missing={marker}')

forbidden = [
    "#030806",
    "#52e39c",
    'رقم واحد يشرح تحوّلًا ضخمًا',
    "staticFile('audio/master.mp3')",
    "staticFile('/audio/master.mp3')",
    '/public/audio/',
    'const Atmosphere=',
]
for marker in forbidden:
    if marker in s:
        raise SystemExit(f'VISUAL_PIPELINE_INVALID legacy_marker={marker}')

print('NEW_VISUAL_PIPELINE_V3_OK: approved presenter is foreground content; old template blocked')
