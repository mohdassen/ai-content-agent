import React from 'react';
import {Composition} from 'remotion';
import {BehindTheNumber} from './video';
import {TOTAL_FRAMES} from './generatedTimeline';

export const Root: React.FC = () => (
  <Composition
    id="BehindTheNumber"
    component={BehindTheNumber}
    durationInFrames={TOTAL_FRAMES}
    fps={30}
    width={1080}
    height={1920}
  />
);
