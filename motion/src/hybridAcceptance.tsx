import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';

const C={navy:'#071426',navy2:'#0B2036',cyan:'#38D9FF',gold:'#E9B949',white:'#F4F8FC',muted:'#A8B8C9',glass:'rgba(11,32,54,.62)'};

const Grid=()=> <AbsoluteFill style={{opacity:.14,backgroundImage:'linear-gradient(rgba(56,217,255,.22) 1px,transparent 1px),linear-gradient(90deg,rgba(56,217,255,.22) 1px,transparent 1px)',backgroundSize:'64px 64px'}}/>;

const Presenter:React.FC=()=>{
  const f=useCurrentFrame();
  const drift=Math.sin(f/26)*5;
  const scale=1.02+Math.sin(f/42)*.006;
  return <div style={{position:'absolute',left:18,bottom:0,width:455,height:1710,overflow:'hidden'}}>
    <div style={{position:'absolute',inset:0,background:'radial-gradient(circle at 52% 35%,rgba(56,217,255,.17),transparent 58%)'}}/>
    <Img src={'/avatars/official_presenter_heygen.jpg'} style={{width:'100%',height:'100%',objectFit:'cover',objectPosition:'44% 50%',transform:`translateY(${drift}px) scale(${scale})`,filter:'contrast(1.04) saturate(.96)'}}/>
    <div style={{position:'absolute',left:0,right:0,bottom:0,height:340,background:'linear-gradient(transparent,#071426 92%)'}}/>
  </div>;
};

const GrowthChart:React.FC=()=>{
  const frame=useCurrentFrame(); const {fps}=useVideoConfig();
  const enter=spring({frame,fps,config:{damping:18,stiffness:90}});
  const p68=spring({frame:Math.max(0,frame-25),fps,config:{damping:20}});
  const p467=spring({frame:Math.max(0,frame-80),fps,config:{damping:18}});
  const lineP=interpolate(frame,[55,145],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const glow=0.5+0.5*Math.sin(frame/11);
  const panelX=interpolate(enter,[0,1],[70,0]);
  return <div style={{position:'absolute',right:45,top:250,width:590,height:1080,border:'1px solid rgba(56,217,255,.28)',borderRadius:38,background:C.glass,backdropFilter:'blur(18px)',boxShadow:'0 30px 80px rgba(0,0,0,.38), inset 0 1px rgba(255,255,255,.08)',transform:`translateX(${panelX}px)`,opacity:enter,overflow:'hidden'}}>
    <div style={{position:'absolute',inset:0,background:'linear-gradient(145deg,rgba(56,217,255,.08),transparent 35%,rgba(233,185,73,.04))'}}/>
    <div style={{position:'absolute',top:44,right:45,left:45,direction:'rtl',fontFamily:'Arial,sans-serif'}}>
      <div style={{fontSize:29,fontWeight:800,color:C.white}}>قدرة مراكز البيانات</div>
      <div style={{fontSize:17,color:C.muted,marginTop:7,letterSpacing:1}}>DATA CENTER CAPACITY</div>
    </div>
    <svg viewBox="0 0 520 650" style={{position:'absolute',left:35,top:175,width:520,height:650,overflow:'visible'}}>
      {[0,1,2,3,4].map((i)=><line key={i} x1="55" x2="495" y1={555-i*110} y2={555-i*110} stroke="rgba(168,184,201,.16)" strokeWidth="2"/>)}
      <line x1="55" x2="55" y1="90" y2="555" stroke="rgba(168,184,201,.3)" strokeWidth="2"/>
      <line x1="55" x2="495" y1="555" y2="555" stroke="rgba(168,184,201,.3)" strokeWidth="2"/>
      <g transform={`translate(115 0) scale(1 ${p68}) translate(0 ${555*(1-p68)})`}>
        <rect x="0" y="487" width="90" height="68" rx="18" fill="rgba(56,217,255,.34)" stroke={C.cyan} strokeWidth="3"/>
      </g>
      <g transform={`translate(330 0) scale(1 ${p467}) translate(0 ${555*(1-p467)})`}>
        <rect x="0" y="88" width="90" height="467" rx="18" fill="rgba(233,185,73,.28)" stroke={C.gold} strokeWidth="3"/>
      </g>
      <path d="M160 470 C235 420 290 265 375 110" fill="none" stroke={C.cyan} strokeWidth="6" strokeLinecap="round" strokeDasharray="560" strokeDashoffset={560*(1-lineP)} style={{filter:'drop-shadow(0 0 9px rgba(56,217,255,.7))'}}/>
      <circle cx="160" cy="470" r="10" fill={C.cyan}/><circle cx="375" cy="110" r={12+3*glow} fill={C.gold}/>
      <text x="160" y="615" textAnchor="middle" fill={C.muted} fontSize="24">START</text><text x="375" y="615" textAnchor="middle" fill={C.muted} fontSize="24">NOW</text>
    </svg>
    <div style={{position:'absolute',left:88,top:790,width:160,textAlign:'center'}}>
      <div style={{fontSize:54,fontWeight:900,color:C.cyan}}>68</div><div style={{fontSize:20,color:C.muted}}>MW</div>
    </div>
    <div style={{position:'absolute',right:75,top:790,width:190,textAlign:'center'}}>
      <div style={{fontSize:68,fontWeight:950,color:C.gold,textShadow:'0 0 22px rgba(233,185,73,.24)'}}>467</div><div style={{fontSize:20,color:C.muted}}>MW</div>
    </div>
    <div style={{position:'absolute',left:60,right:60,bottom:58,height:76,borderRadius:20,background:'rgba(56,217,255,.08)',border:'1px solid rgba(56,217,255,.16)',display:'flex',alignItems:'center',justifyContent:'center',gap:16}}>
      <span style={{fontSize:18,color:C.muted}}>CAPACITY GROWTH</span><span style={{fontSize:32,fontWeight:900,color:C.white}}>+587%</span>
    </div>
  </div>;
};

const GestureCue:React.FC=()=>{
  const f=useCurrentFrame(); const opacity=interpolate(f,[85,110,250,280],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const x=interpolate(f,[110,180],[0,105],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <div style={{position:'absolute',left:390+x,top:790,opacity,display:'flex',alignItems:'center',gap:8}}>
    <div style={{width:115,height:2,background:`linear-gradient(90deg,transparent,${C.cyan})`,boxShadow:'0 0 10px rgba(56,217,255,.8)'}}/><div style={{width:14,height:14,borderRadius:14,background:C.cyan,boxShadow:'0 0 18px rgba(56,217,255,.9)'}}/>
  </div>;
};

export const HybridAcceptance:React.FC=()=>{
  const f=useCurrentFrame();
  const title=interpolate(f,[0,22],[0,1],{extrapolateRight:'clamp'});
  return <AbsoluteFill style={{background:`radial-gradient(circle at 18% 25%,#123452 0%,${C.navy} 38%,#030912 100%)`,fontFamily:'Arial,sans-serif',color:C.white}}>
    <Grid/>
    <div style={{position:'absolute',top:64,left:62,right:62,display:'flex',justifyContent:'space-between',alignItems:'center',opacity:title}}>
      <div style={{fontSize:18,letterSpacing:3,color:C.muted}}>HYBRID BROADCAST ENGINE • ACCEPTANCE SCENE 01</div>
      <div style={{direction:'rtl',fontSize:30,fontWeight:900,color:C.gold}}>خلف الرقم</div>
    </div>
    <Presenter/><GrowthChart/><GestureCue/>
    <div style={{position:'absolute',left:62,bottom:74,width:900}}>
      <div style={{fontSize:20,color:C.cyan,letterSpacing:2}}>BEHIND THE NUMBER</div>
      <div style={{marginTop:10,fontSize:34,fontWeight:850,direction:'rtl'}}>الشخصية تشرح الرقم — والبيانات تظهر بجانبها، لا فوقها</div>
    </div>
  </AbsoluteFill>;
};
