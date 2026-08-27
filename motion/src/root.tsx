import React from 'react';
import {Composition} from 'remotion';
import {HybridLiveAcceptance} from './hybridLiveAcceptance';

export const Root: React.FC = () => (
  <Composition
    id="HybridLiveAcceptance"
    component={HybridLiveAcceptance}
    durationInFrames={270}
    fps={30}
    width={1080}
    height={1920}
  />
);
