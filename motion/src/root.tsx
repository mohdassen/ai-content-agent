import React from 'react';
import {Composition} from 'remotion';
import {BehindTheNumber} from './video';
import {HybridAcceptance} from './hybridAcceptance';
import {HybridLiveAcceptance} from './hybridLiveAcceptance';
import {TOTAL_FRAMES} from './generatedTimeline';

export const Root: React.FC = () => (
  <>
    <Composition
      id="BehindTheNumber"
      component={BehindTheNumber}
      durationInFrames={TOTAL_FRAMES}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="HybridAcceptance"
      component={HybridAcceptance}
      durationInFrames={360}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="HybridLiveAcceptance"
      component={HybridLiveAcceptance}
      durationInFrames={270}
      fps={30}
      width={1080}
      height={1920}
    />
  </>
);
