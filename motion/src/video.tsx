import React from 'react';
import {AbsoluteFill, interpolate, Sequence, spring, useCurrentFrame, useVideoConfig} from 'remotion';

const bg = '#07130f';
const panel = '#0e211b';
const text = '#f5f7f6';
const accent = '#53e39c';
const muted = '#9eb7ad';

const NumberBeat: React.FC<{from: number; to: number; suffix: string; title: string}> = ({from, to, suffix, title}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame, fps, config: {damping: 14, stiffness: 110}});
  const value = Math.round(interpolate(p, [0, 1], [from, to]));
  return <AbsoluteFill style={{background: bg, color: text, fontFamily: 'Noto Sans Arabic, Arial, sans-serif', justifyContent: 'center', alignItems: 'center'}}>
    <div style={{fontSize: 42, color: muted, marginBottom: 36, direction: 'rtl'}}>{title}</div>
    <div style={{display: 'flex', alignItems: 'baseline', gap: 20}}>
      <span style={{fontSize: 210, fontWeight: 900, letterSpacing: -8}}>{value}</span>
      <span style={{fontSize: 76, fontWeight: 800, color: accent}}>{suffix}</span>
    </div>
    <div style={{width: 720, height: 18, borderRadius: 20, background: panel, marginTop: 48, overflow: 'hidden'}}>
      <div style={{width: `${p * 100}%`, height: '100%', background: accent}} />
    </div>
  </AbsoluteFill>;
};

const FlowBeat: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const labels = ['AI', 'GPU', 'POWER', 'COOLING'];
  return <AbsoluteFill style={{background: '#091713', color: text, fontFamily: 'Arial, sans-serif', justifyContent: 'center', alignItems: 'center'}}>
    <div style={{fontSize: 46, color: muted, marginBottom: 70}}>WHAT POWERS AI?</div>
    <div style={{display: 'flex', alignItems: 'center', gap: 22}}>
      {labels.map((label, i) => {
        const local = frame - i * 10;
        const s = spring({frame: local, fps, config: {damping: 13}});
        return <React.Fragment key={label}>
          <div style={{transform: `scale(${s})`, opacity: s, width: 190, height: 190, borderRadius: 38, background: i === 0 ? accent : panel, color: i === 0 ? bg : text, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 900, fontSize: 40, boxShadow: '0 20px 60px rgba(0,0,0,.28)'}}>{label}</div>
          {i < labels.length - 1 && <div style={{fontSize: 54, color: accent}}>→</div>}
        </React.Fragment>;
      })}
    </div>
    <div style={{fontFamily: 'Noto Sans Arabic, Arial, sans-serif', fontSize: 44, direction: 'rtl', marginTop: 90}}>الذكاء الاصطناعي يحتاج بنية تحتية حقيقية</div>
  </AbsoluteFill>;
};

const InvestmentBeat: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame, fps, config: {damping: 16}});
  const value = interpolate(p, [0, 1], [0, 16]);
  return <AbsoluteFill style={{background: '#06110e', color: text, fontFamily: 'Noto Sans Arabic, Arial, sans-serif', justifyContent: 'center', alignItems: 'center'}}>
    <div style={{fontSize: 40, color: muted, direction: 'rtl'}}>استثمارات مراكز البيانات</div>
    <div style={{fontSize: 178, fontWeight: 900, marginTop: 28}}>{value.toFixed(1)}</div>
    <div style={{fontSize: 66, color: accent, fontWeight: 800, direction: 'rtl'}}>مليار ريال+</div>
    <div style={{marginTop: 70, width: 720, display: 'grid', gridTemplateColumns: 'repeat(8, 1fr)', gap: 16}}>
      {Array.from({length: 16}).map((_, i) => <div key={i} style={{height: 70, borderRadius: 14, background: i / 16 < p ? accent : panel, opacity: i / 16 < p ? 1 : .6}} />)}
    </div>
  </AbsoluteFill>;
};

const ClosingBeat: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 16}});
  return <AbsoluteFill style={{background: bg, color: text, fontFamily: 'Noto Sans Arabic, Arial, sans-serif', justifyContent: 'center', alignItems: 'center', padding: 100}}>
    <div style={{fontSize: 34, color: accent, fontWeight: 800, marginBottom: 44}}>خلف الرقم</div>
    <div style={{fontSize: 72, fontWeight: 900, textAlign: 'center', lineHeight: 1.35, direction: 'rtl', transform: `scale(${s})`}}>هل تصبح الحوسبة أصلًا استراتيجيًا مثل الطاقة؟</div>
    <div style={{fontSize: 31, color: muted, marginTop: 55, direction: 'rtl'}}>القصة ليست في الرقم وحده… بل فيما يغيّره.</div>
  </AbsoluteFill>;
};

export const BehindTheNumber: React.FC = () => {
  return <AbsoluteFill style={{background: bg}}>
    <Sequence from={0} durationInFrames={240}><NumberBeat from={68} to={467} suffix="MW" title="قدرة مراكز البيانات في السعودية" /></Sequence>
    <Sequence from={240} durationInFrames={270}><FlowBeat /></Sequence>
    <Sequence from={510} durationInFrames={270}><InvestmentBeat /></Sequence>
    <Sequence from={780} durationInFrames={300}><ClosingBeat /></Sequence>
  </AbsoluteFill>;
};
