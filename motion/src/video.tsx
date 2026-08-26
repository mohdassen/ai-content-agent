import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {TIMELINE} from './generatedTimeline';

const C={bg:'#050b09',bg2:'#0a1713',panel:'#10241d',text:'#f7faf8',accent:'#52e39c',accent2:'#baffdc',muted:'#91aa9f',line:'#1c4435'};
const font='Noto Sans Arabic, Noto Kufi Arabic, Arial, sans-serif';

type P={duration:number};
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};

const Atmosphere=()=>{const f=useCurrentFrame();const drift=Math.sin(f/32)*25;return <>
  <AbsoluteFill style={{background:`radial-gradient(circle at ${48+drift/20}% 20%,#123528 0%,${C.bg2} 28%,${C.bg} 70%)`}}/>
  <AbsoluteFill style={{opacity:.11,backgroundImage:`linear-gradient(${C.line} 1px,transparent 1px),linear-gradient(90deg,${C.line} 1px,transparent 1px)`,backgroundSize:'96px 96px',transform:`translate(${drift}px,${drift*.35}px) scale(1.08)`}}/>
  <AbsoluteFill style={{background:'linear-gradient(180deg,rgba(0,0,0,.05),transparent 35%,rgba(0,0,0,.42))'}}/>
</>};

const Brand=()=> <div style={{position:'absolute',top:66,right:66,fontFamily:font,color:C.accent,fontSize:26,fontWeight:900,direction:'rtl',letterSpacing:.2}}>خلف الرقم</div>;

const SceneShell:React.FC<{duration:number;children:React.ReactNode}>=({duration,children})=>{const f=useCurrentFrame();const enter=interpolate(f,[0,10],[0,1],clamp);const exit=interpolate(f,[Math.max(0,duration-10),duration],[1,0],clamp);const scale=interpolate(f,[0,duration],[1.045,1],clamp);return <AbsoluteFill style={{opacity:Math.min(enter,exit),transform:`scale(${scale})`,overflow:'hidden',color:C.text}}><Atmosphere/><Brand/>{children}</AbsoluteFill>};

const KineticCaption:React.FC<{text:string;accent?:string}>=({text,accent})=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const p=spring({frame:f-4,fps,config:{damping:18,stiffness:120}});return <div style={{position:'absolute',left:72,right:72,bottom:155,textAlign:'center',fontFamily:font,fontSize:40,lineHeight:1.48,fontWeight:850,color:C.text,direction:'rtl',opacity:p,transform:`translateY(${(1-p)*32}px)`}}>{text}<div style={{height:4,width:`${p*130}px`,background:accent||C.accent,margin:'18px auto 0',borderRadius:8}}/></div>};

const NumberHero:React.FC<P>=({duration})=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const p=spring({frame:f,fps,config:{damping:12,stiffness:105}});const switchP=interpolate(f,[16,42],[0,1],clamp);const oldY=interpolate(switchP,[0,1],[0,-150],clamp);const newY=interpolate(switchP,[0,1],[150,0],clamp);const pulse=1+Math.sin(f/4)*.015;return <SceneShell duration={duration}>
  <div style={{position:'absolute',top:255,left:70,right:70,fontFamily:font,fontSize:34,color:C.muted,textAlign:'center',direction:'rtl'}}>قفزة في قدرة مراكز البيانات</div>
  <div style={{position:'absolute',top:430,left:0,right:0,height:420,overflow:'hidden',textAlign:'center'}}>
    <div style={{fontSize:250,fontWeight:950,letterSpacing:-12,transform:`translateY(${oldY}px) scale(${pulse})`,opacity:1-switchP,color:'#d7e2dd'}}>68</div>
    <div style={{position:'absolute',top:0,left:0,right:0,fontSize:250,fontWeight:950,letterSpacing:-12,transform:`translateY(${newY}px) scale(${.85+p*.15})`,opacity:switchP}}>467 <span style={{fontSize:68,color:C.accent,letterSpacing:0}}>MW</span></div>
  </div>
  <div style={{position:'absolute',top:895,left:155,right:155,height:12,borderRadius:20,background:C.panel,overflow:'hidden'}}><div style={{height:'100%',width:`${interpolate(f,[12,58],[8,100],clamp)}%`,background:`linear-gradient(90deg,${C.accent},${C.accent2})`,boxShadow:`0 0 25px ${C.accent}`}}/></div>
  <div style={{position:'absolute',top:970,left:0,right:0,textAlign:'center',fontSize:34,color:C.accent,fontWeight:900}}>≈ 6.9×</div>
  <KineticCaption text="السعودية رفعت قدرة مراكز البيانات من 68 إلى 467 ميغاواط. لماذا هذا الرقم مهم؟"/>
</SceneShell>};

const Servers:React.FC<P>=({duration})=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const travel=interpolate(f,[0,duration],[0,-120],clamp);return <SceneShell duration={duration}>
  <div style={{position:'absolute',top:180,left:0,right:0,textAlign:'center',fontFamily:font,fontSize:31,color:C.muted,direction:'rtl'}}>خلف كل تطبيق AI… بنية تعمل بلا توقف</div>
  <div style={{position:'absolute',top:330,left:70,right:70,height:850,perspective:900,overflow:'hidden'}}>
    {[0,1].map(side=><div key={side} style={{position:'absolute',top:0,[side===0?'left':'right']:side===0?0:0,width:410,height:900,transform:`rotateY(${side===0?24:-24}deg) translateY(${travel}px)`,transformOrigin:side===0?'left center':'right center'}}>{Array.from({length:9}).map((_,i)=>{const p=spring({frame:f-i*3,fps,config:{damping:16}});return <div key={i} style={{height:92,marginBottom:16,borderRadius:14,background:'linear-gradient(180deg,#142a22,#0c1b16)',border:`1px solid ${C.line}`,boxShadow:'inset 0 0 24px rgba(0,0,0,.35)',opacity:p}}><div style={{display:'flex',gap:10,padding:'18px 20px'}}>{Array.from({length:5}).map((_,j)=><span key={j} style={{width:10,height:10,borderRadius:10,background:(i+j+f)%5<1.5?C.accent:'#456359',boxShadow:(i+j+f)%5<1.5?`0 0 14px ${C.accent}`:'none'}}/> )}</div><div style={{height:5,margin:'0 18px',borderRadius:5,background:C.line}}/></div>})}</div>)}
    <div style={{position:'absolute',left:'50%',top:40,bottom:0,width:3,background:`linear-gradient(180deg,${C.accent},transparent)`,boxShadow:`0 0 35px ${C.accent}`}}/>
  </div>
  <div style={{position:'absolute',top:1040,left:0,right:0,textAlign:'center',fontFamily:font,fontSize:56,fontWeight:950,direction:'rtl'}}>آلاف الخوادم</div>
  <KineticCaption text="الذكاء الاصطناعي لا يعيش في التطبيق فقط. خلفه آلاف الخوادم تعمل بلا توقف."/>
</SceneShell>};

const Factory:React.FC<P>=({duration})=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const p=spring({frame:f-8,fps,config:{damping:15}});return <SceneShell duration={duration}>
  <div style={{position:'absolute',top:270,left:0,right:0,textAlign:'center',fontFamily:font,fontSize:34,color:C.muted,direction:'rtl'}}>مركز البيانات لم يعد مجرد مخزن</div>
  <div style={{position:'absolute',top:470,left:110,right:110,height:520}}>
    <div style={{position:'absolute',left:0,top:100,width:250,height:300,borderRadius:38,border:`2px solid ${C.line}`,background:C.panel,display:'flex',alignItems:'center',justifyContent:'center',fontFamily:font,fontSize:42,color:C.muted,direction:'rtl',opacity:1-p*.75,transform:`translateX(${-p*70}px) scale(${1-p*.12})`}}>ملفات<br/>وتخزين</div>
    {Array.from({length:14}).map((_,i)=>{const q=interpolate(f,[10+i*2,45+i*2],[0,1],clamp);return <div key={i} style={{position:'absolute',left:300+q*240,top:150+(i%5)*46,width:14,height:14,borderRadius:14,background:C.accent,opacity:q,boxShadow:`0 0 18px ${C.accent}`}}/>})}
    <div style={{position:'absolute',right:0,top:35,width:390,height:390,borderRadius:65,background:`radial-gradient(circle at 35% 30%,${C.accent2},${C.accent} 45%,#1b704d)`,color:C.bg,display:'flex',alignItems:'center',justifyContent:'center',textAlign:'center',fontFamily:font,fontWeight:950,fontSize:57,direction:'rtl',transform:`scale(${.72+p*.28})`,boxShadow:`0 0 ${80*p}px rgba(82,227,156,.35)`}}>مصنع<br/>حوسبة</div>
  </div>
  <KineticCaption text="ومركز البيانات يتحول من مخزن للملفات إلى مصنع حوسبة للذكاء الاصطناعي."/>
</SceneShell>};

const Flow:React.FC<P>=({duration})=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const items=[['AI','ذكاء'],['GPU','رقائق'],['POWER','طاقة'],['COOL','تبريد'],['FIBER','ألياف']];return <SceneShell duration={duration}>
  <div style={{position:'absolute',top:230,left:0,right:0,textAlign:'center',fontFamily:font,fontSize:36,color:C.muted,direction:'rtl'}}>سلسلة كاملة وراء كل طلب AI</div>
  <div style={{position:'absolute',top:430,left:110,right:110}}>{items.map(([en,ar],i)=>{const p=spring({frame:f-i*8,fps,config:{damping:14}});const x=i%2===0?110:520;const y=i*150;return <React.Fragment key={en}><div style={{position:'absolute',left:x,top:y,width:280,height:112,borderRadius:56,border:`2px solid ${i===0?C.accent:C.line}`,background:i===0?'rgba(82,227,156,.12)':C.panel,display:'flex',alignItems:'center',justifyContent:'space-between',padding:'0 30px',transform:`translateX(${(1-p)*(i%2===0?-80:80)}px)`,opacity:p}}><span style={{fontSize:29,fontWeight:950,color:i===0?C.accent:C.text}}>{en}</span><span style={{fontFamily:font,fontSize:28,direction:'rtl',color:C.muted}}>{ar}</span></div>{i<items.length-1&&<div style={{position:'absolute',left:i%2===0?390:485,top:y+108,width:110,height:85,borderRight:`2px solid ${C.accent}`,borderBottom:`2px solid ${C.accent}`,opacity:p}}/>}</React.Fragment>})}</div>
  <KineticCaption text="وهذا يرفع الطلب على الرقائق والكهرباء والتبريد والألياف الضوئية."/>
</SceneShell>};

const Investment:React.FC<P>=({duration})=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const p=spring({frame:f,fps,config:{damping:13}});const v=interpolate(p,[0,1],[0,16]);return <SceneShell duration={duration}>
  <div style={{position:'absolute',top:250,left:0,right:0,textAlign:'center',fontFamily:font,fontSize:34,color:C.muted,direction:'rtl'}}>استثمارات مراكز البيانات منذ 2016</div>
  <div style={{position:'absolute',top:430,left:0,right:0,textAlign:'center'}}><div style={{fontSize:245,fontWeight:950,letterSpacing:-10}}>{v.toFixed(1)}</div><div style={{fontFamily:font,fontSize:68,color:C.accent,fontWeight:900,direction:'rtl'}}>مليار ريال+</div></div>
  <div style={{position:'absolute',top:900,left:140,right:140,height:220,display:'flex',alignItems:'end',gap:18}}>{[.15,.23,.31,.43,.55,.68,.82,1].map((h,i)=><div key={i} style={{flex:1,height:`${interpolate(p,[0,1],[3,h*100],clamp)}%`,borderRadius:'14px 14px 4px 4px',background:i===7?C.accent:C.line,boxShadow:i===7?`0 0 30px ${C.accent}`:'none'}}/>)}</div>
  <KineticCaption text="ومنذ 2016 تجاوزت استثمارات مراكز البيانات في المملكة 16 مليار ريال."/>
</SceneShell>};

const Race:React.FC<P>=({duration})=>{const f=useCurrentFrame();const p=interpolate(f,[5,Math.min(duration-8,70)],[0,1],clamp);return <SceneShell duration={duration}>
  <div style={{position:'absolute',top:260,left:80,right:80,fontFamily:font,fontSize:39,textAlign:'center',direction:'rtl',color:C.muted}}>السباق الحقيقي ينتقل إلى طبقة أعمق</div>
  <div style={{position:'absolute',top:520,left:130,right:130}}><div style={{fontFamily:font,fontSize:38,direction:'rtl',marginBottom:18}}>التطبيقات</div><div style={{height:72,borderRadius:40,background:C.panel,overflow:'hidden'}}><div style={{height:'100%',width:`${p*38}%`,background:C.line,borderRadius:40}}/></div><div style={{fontFamily:font,fontSize:54,fontWeight:950,direction:'rtl',marginTop:90,color:C.accent}}>قدرة الحوسبة</div><div style={{height:108,borderRadius:54,background:C.panel,overflow:'hidden',marginTop:22}}><div style={{height:'100%',width:`${p*100}%`,background:`linear-gradient(90deg,#1e704f,${C.accent})`,borderRadius:54,boxShadow:`0 0 28px ${C.accent}`}}/></div></div>
  <div style={{position:'absolute',top:1035,left:0,right:0,textAlign:'center',fontSize:34,color:C.accent,fontWeight:950}}>COMPUTE IS THE MOAT</div>
  <KineticCaption text="لذلك السباق القادم ليس على التطبيقات فقط، بل على من يملك قدرة الحوسبة التي تشغلها."/>
</SceneShell>};

const Hub:React.FC<P>=({duration})=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const p=spring({frame:f,fps,config:{damping:14}});const nodes=[[300,170],[535,125],[650,340],[500,520],[275,500],[180,325]];return <SceneShell duration={duration}>
  <div style={{position:'absolute',top:245,left:0,right:0,textAlign:'center',fontFamily:font,fontSize:35,color:C.muted,direction:'rtl'}}>من مركز بيانات… إلى عقدة إقليمية</div>
  <div style={{position:'absolute',top:430,left:130,width:820,height:700,clipPath:'polygon(28% 3%,52% 8%,69% 2%,86% 20%,82% 45%,94% 62%,79% 83%,57% 92%,35% 84%,20% 69%,6% 46%,14% 22%)',background:'linear-gradient(145deg,#0c211a,#153c2d)',border:`2px solid ${C.line}`}}>
    {nodes.map(([x,y],i)=>{const q=spring({frame:f-i*7,fps,config:{damping:13}});return <React.Fragment key={i}><div style={{position:'absolute',left:410,top:350,width:2,height:Math.hypot(x-410,y-350),background:`linear-gradient(${C.accent},transparent)`,transformOrigin:'top',transform:`rotate(${Math.atan2(y-350,x-410)*180/Math.PI-90}deg) scaleY(${q})`,opacity:.45}}/><div style={{position:'absolute',left:x,top:y,width:30,height:30,borderRadius:30,background:C.accent,transform:`scale(${q})`,boxShadow:`0 0 ${34*q}px ${C.accent}`}}/></React.Fragment>})}
    <div style={{position:'absolute',left:350,top:285,fontSize:86,fontWeight:950,color:C.accent,transform:`scale(${.8+p*.2})`}}>KSA</div>
  </div>
  <KineticCaption text="إذا استمر النمو، قد تصبح السعودية عقدة رئيسية للحوسبة والذكاء الاصطناعي في المنطقة."/>
</SceneShell>};

const End:React.FC<P>=({duration})=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const p=spring({frame:f,fps,config:{damping:15}});return <SceneShell duration={duration}>
  <div style={{position:'absolute',top:310,left:90,right:90,textAlign:'center',fontFamily:font,direction:'rtl'}}><div style={{fontSize:31,color:C.accent,fontWeight:900,marginBottom:55}}>خلف الرقم</div><div style={{fontSize:76,fontWeight:950,lineHeight:1.42,transform:`scale(${.88+p*.12})`}}>هل تصبح الحوسبة<br/><span style={{color:C.accent}}>أصلًا استراتيجيًا</span><br/>مثل الطاقة؟</div></div>
  <div style={{position:'absolute',top:1000,left:180,right:180,height:2,background:`linear-gradient(90deg,transparent,${C.accent},transparent)`}}/>
  <KineticCaption text="فهل تصبح الحوسبة أصلاً استراتيجياً مثل الطاقة؟"/>
</SceneShell>};

const visuals=[NumberHero,Servers,Factory,Flow,Investment,Race,Hub,End];

export const BehindTheNumber:React.FC=()=> <AbsoluteFill style={{background:C.bg}}>
  <Audio src={staticFile('audio/master_narration.mp3')}/>
  {TIMELINE.map((t,i)=>{const Comp=visuals[i];return <Sequence key={t.index} from={t.from} durationInFrames={t.frames}><Comp duration={t.frames}/></Sequence>})}
</AbsoluteFill>;
