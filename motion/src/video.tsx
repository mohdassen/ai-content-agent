import React from 'react';
import {
  AbsoluteFill,
  Audio,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const C = {
  bg: '#07130f',
  bg2: '#0a1a15',
  panel: '#10241d',
  text: '#f7faf8',
  accent: '#55e69f',
  accent2: '#b8ffda',
  muted: '#9cb5aa',
  line: '#24483a',
};

const font = 'Noto Sans Arabic, Noto Kufi Arabic, Arial, sans-serif';

const Brand: React.FC = () => (
  <div style={{position: 'absolute', top: 72, right: 70, fontFamily: font, color: C.accent, fontSize: 27, fontWeight: 800, direction: 'rtl'}}>
    خلف الرقم
  </div>
);

const Caption: React.FC<{children: React.ReactNode}> = ({children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const y = interpolate(spring({frame, fps, config: {damping: 18}}), [0, 1], [34, 0]);
  return (
    <div style={{position: 'absolute', left: 75, right: 75, bottom: 185, textAlign: 'center', fontFamily: font, fontSize: 43, lineHeight: 1.5, fontWeight: 800, color: C.text, direction: 'rtl', transform: `translateY(${y}px)`}}>
      {children}
    </div>
  );
};

const Grid: React.FC = () => (
  <AbsoluteFill style={{opacity: 0.16, backgroundImage: `linear-gradient(${C.line} 1px, transparent 1px),linear-gradient(90deg, ${C.line} 1px, transparent 1px)`, backgroundSize: '90px 90px'}} />
);

const Scene: React.FC<{index: number; children: React.ReactNode}> = ({index, children}) => (
  <AbsoluteFill style={{background: `radial-gradient(circle at 50% 20%, ${C.bg2}, ${C.bg} 62%)`, color: C.text, overflow: 'hidden'}}>
    <Grid />
    <Brand />
    {children}
    <Audio src={staticFile(`audio/scene_${String(index).padStart(2, '0')}.mp3`)} />
  </AbsoluteFill>
);

const NumberHero: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame, fps, config: {damping: 14, stiffness: 105}});
  const value = Math.round(interpolate(p, [0, 1], [68, 467]));
  const scale = interpolate(p, [0, 1], [0.82, 1]);
  return <Scene index={1}>
    <div style={{position: 'absolute', top: 330, left: 0, right: 0, textAlign: 'center', fontFamily: font, color: C.muted, fontSize: 34, direction: 'rtl'}}>قدرة مراكز البيانات في السعودية</div>
    <div style={{position: 'absolute', top: 520, left: 0, right: 0, display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: 22, transform: `scale(${scale})`}}>
      <span style={{fontSize: 235, fontWeight: 950, letterSpacing: -8}}>{value}</span>
      <span style={{fontSize: 72, color: C.accent, fontWeight: 900}}>MW</span>
    </div>
    <div style={{position: 'absolute', top: 860, left: 165, width: 750, height: 18, borderRadius: 20, background: C.panel, overflow: 'hidden'}}>
      <div style={{height: '100%', width: `${p * 100}%`, background: `linear-gradient(90deg, ${C.accent}, ${C.accent2})`}} />
    </div>
    <Caption>من 68 إلى 467 ميغاواط… لماذا هذا الرقم مهم؟</Caption>
  </Scene>;
};

const ServerFactory: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return <Scene index={2}>
    <div style={{position: 'absolute', top: 310, left: 125, right: 125, display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 18}}>
      {Array.from({length: 16}).map((_, i) => {
        const p = spring({frame: frame - i * 2, fps, config: {damping: 16}});
        return <div key={i} style={{height: 125, borderRadius: 22, background: C.panel, border: `1px solid ${C.line}`, opacity: p, transform: `translateY(${(1-p)*30}px)`}}>
          <div style={{width: 13, height: 13, borderRadius: 10, background: i % 3 === 0 ? C.accent : C.muted, margin: '22px 0 0 22px', boxShadow: i % 3 === 0 ? `0 0 22px ${C.accent}` : 'none'}} />
          <div style={{height: 7, margin: '25px 20px 0', background: C.line, borderRadius: 8}} />
          <div style={{height: 7, margin: '10px 20px 0', background: C.line, borderRadius: 8}} />
        </div>;
      })}
    </div>
    <div style={{position: 'absolute', top: 790, left: 0, right: 0, textAlign: 'center', fontFamily: font, fontSize: 64, fontWeight: 950, direction: 'rtl'}}>آلاف الخوادم تعمل بلا توقف</div>
    <Caption>الذكاء الاصطناعي لا يعيش في التطبيق فقط.</Caption>
  </Scene>;
};

const FactoryShift: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame, fps, config: {damping: 16}});
  return <Scene index={3}>
    <div style={{position: 'absolute', top: 360, left: 110, right: 110, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
      <div style={{width: 330, height: 330, borderRadius: 52, background: C.panel, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: font, fontSize: 46, direction: 'rtl', color: C.muted}}>تخزين</div>
      <div style={{fontSize: 85, color: C.accent, transform: `translateX(${interpolate(p,[0,1],[-50,0])}px)`}}>→</div>
      <div style={{width: 390, height: 390, borderRadius: 62, background: C.accent, color: C.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', fontFamily: font, fontWeight: 950, fontSize: 52, direction: 'rtl', transform: `scale(${0.85 + p*0.15})`}}>مصنع<br/>حوسبة</div>
    </div>
    <Caption>مركز البيانات يتحول من مخزن ملفات إلى مصنع حوسبة للـAI.</Caption>
  </Scene>;
};

const Flow: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const items = ['AI', 'GPU', 'POWER', 'COOLING', 'FIBER'];
  return <Scene index={4}>
    <div style={{position: 'absolute', top: 385, left: 75, right: 75}}>
      <div style={{fontFamily: font, fontSize: 34, color: C.muted, textAlign: 'center', marginBottom: 75, direction: 'rtl'}}>ما الذي يشغّل الذكاء الاصطناعي؟</div>
      <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 12}}>
        {items.map((item, i) => {
          const p = spring({frame: frame - i * 8, fps, config: {damping: 14}});
          return <React.Fragment key={item}>
            <div style={{width: 170, height: 170, borderRadius: 34, background: i === 0 ? C.accent : C.panel, color: i === 0 ? C.bg : C.text, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: item.length > 5 ? 25 : 34, fontWeight: 950, transform: `scale(${p})`, opacity: p, border: `1px solid ${i === 0 ? C.accent : C.line}`}}>{item}</div>
            {i < items.length - 1 && <div style={{fontSize: 42, color: C.accent, opacity: p}}>→</div>}
          </React.Fragment>;
        })}
      </div>
    </div>
    <Caption>رقائق، كهرباء، تبريد، وألياف ضوئية… كلها تدخل في المعادلة.</Caption>
  </Scene>;
};

const Investment: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame, fps, config: {damping: 15}});
  const value = interpolate(p, [0,1], [0,16]);
  return <Scene index={5}>
    <div style={{position: 'absolute', top: 360, left: 0, right: 0, textAlign: 'center', fontFamily: font, color: C.muted, fontSize: 36, direction: 'rtl'}}>استثمارات مراكز البيانات منذ 2016</div>
    <div style={{position: 'absolute', top: 520, left: 0, right: 0, textAlign: 'center'}}>
      <span style={{fontSize: 220, fontWeight: 950}}>{value.toFixed(1)}</span>
      <div style={{fontFamily: font, fontSize: 72, color: C.accent, fontWeight: 900, direction: 'rtl'}}>مليار ريال+</div>
    </div>
    <Caption>الاستثمارات تجاوزت 16 مليار ريال.</Caption>
  </Scene>;
};

const ComputeRace: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame, fps, config: {damping: 16}});
  return <Scene index={6}>
    <div style={{position: 'absolute', top: 350, left: 140, right: 140}}>
      {[['التطبيقات', 0.45], ['قدرة الحوسبة', 1]].map(([label, max], i) => (
        <div key={String(label)} style={{marginBottom: 90}}>
          <div style={{fontFamily: font, fontSize: 43, fontWeight: 800, direction: 'rtl', marginBottom: 18}}>{label}</div>
          <div style={{height: 92, background: C.panel, borderRadius: 24, overflow: 'hidden'}}>
            <div style={{height: '100%', width: `${p * Number(max) * 100}%`, background: i === 1 ? C.accent : C.line, borderRadius: 24}} />
          </div>
        </div>
      ))}
    </div>
    <Caption>السباق القادم ليس على التطبيقات فقط… بل على من يملك الحوسبة.</Caption>
  </Scene>;
};

const SaudiHub: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const nodes = [[320,520],[520,420],[700,600],[450,760],[670,850],[300,900]];
  return <Scene index={7}>
    <div style={{position: 'absolute', top: 310, left: 0, right: 0, textAlign: 'center', fontFamily: font, fontSize: 36, color: C.muted, direction: 'rtl'}}>شبكة حوسبة إقليمية</div>
    <div style={{position: 'absolute', top: 420, left: 130, width: 820, height: 650, borderRadius: '45% 55% 50% 50%', background: `linear-gradient(145deg, ${C.panel}, #15362a)`, border: `2px solid ${C.line}`}}>
      {nodes.map(([x,y], i) => {
        const p = spring({frame: frame - i*6, fps, config: {damping: 13}});
        return <div key={i} style={{position: 'absolute', left: x-130, top: y-420, width: 34, height: 34, borderRadius: 30, background: C.accent, transform: `scale(${p})`, boxShadow: `0 0 ${35*p}px ${C.accent}`}} />;
      })}
      <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 80, fontWeight: 950, color: C.accent}}>KSA</div>
    </div>
    <Caption>إذا استمر النمو، قد تصبح السعودية عقدة حوسبة رئيسية في المنطقة.</Caption>
  </Scene>;
};

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame, fps, config: {damping: 16}});
  return <Scene index={8}>
    <div style={{position: 'absolute', top: 470, left: 95, right: 95, textAlign: 'center', fontFamily: font, direction: 'rtl', transform: `scale(${0.92+p*0.08})`}}>
      <div style={{fontSize: 34, color: C.accent, fontWeight: 900, marginBottom: 55}}>خلف الرقم</div>
      <div style={{fontSize: 78, fontWeight: 950, lineHeight: 1.38}}>هل تصبح الحوسبة أصلًا استراتيجيًا مثل الطاقة؟</div>
      <div style={{fontSize: 31, color: C.muted, marginTop: 70}}>الرقم يلفت انتباهك… والقصة تشرح لماذا يهم.</div>
    </div>
    <Caption>وهنا تبدأ القصة خلف الرقم.</Caption>
  </Scene>;
};

export const BehindTheNumber: React.FC = () => (
  <AbsoluteFill style={{background: C.bg}}>
    <Sequence from={0} durationInFrames={150}><NumberHero /></Sequence>
    <Sequence from={150} durationInFrames={150}><ServerFactory /></Sequence>
    <Sequence from={300} durationInFrames={150}><FactoryShift /></Sequence>
    <Sequence from={450} durationInFrames={150}><Flow /></Sequence>
    <Sequence from={600} durationInFrames={150}><Investment /></Sequence>
    <Sequence from={750} durationInFrames={150}><ComputeRace /></Sequence>
    <Sequence from={900} durationInFrames={150}><SaudiHub /></Sequence>
    <Sequence from={1050} durationInFrames={150}><EndCard /></Sequence>
  </AbsoluteFill>
);
