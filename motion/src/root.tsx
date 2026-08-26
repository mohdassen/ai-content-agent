import React from 'react';
import {Composition} from 'remotion';
import {BehindTheNumber} from './video';

export const Root: React.FC = () => {
  return (
    <Composition
      id="BehindTheNumber"
      component={BehindTheNumber}
      durationInFrames={1080}
      fps={30}
      width={1080}
      height={1920}
    />
  );
};
