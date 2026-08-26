export type TimelineScene = {
  index: number;
  from: number;
  frames: number;
  audio_seconds: number;
};

// This safe default is overwritten by prepare_motion.py before every production render.
export const TIMELINE: TimelineScene[] = [
  {index: 1, from: 0, frames: 300, audio_seconds: 9.0},
  {index: 2, from: 300, frames: 240, audio_seconds: 7.0},
  {index: 3, from: 540, frames: 240, audio_seconds: 7.0},
  {index: 4, from: 780, frames: 240, audio_seconds: 7.0},
  {index: 5, from: 1020, frames: 210, audio_seconds: 6.0},
  {index: 6, from: 1230, frames: 240, audio_seconds: 7.0},
  {index: 7, from: 1470, frames: 240, audio_seconds: 7.0},
  {index: 8, from: 1710, frames: 180, audio_seconds: 5.0},
];

export const TOTAL_FRAMES = TIMELINE.reduce((sum, scene) => sum + scene.frames, 0);
