import React from 'react';
import {AbsoluteFill, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const C={navy:'#06111F',navy2:'#0A1D31',cyan:'#38D9FF',gold:'#E9B949',white:'#F6FAFD',muted:'#A9BAC9'};

const GlassChart:React.FC=()=>{
  const f=useCurrentFrame(); const {fps}=useVideoConfig();
  const enter=spring({frame:Math.max(0,f-14),fps,config:{damping:18,stiffness:100}});
  const p=interpolate(f,[45,170],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const n=interpolate(f,[70,180],[68,467],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  const glow=.55+.45*Math.sin(f/9);
  return <div style={{position:'absolute',right:42,top:360,width:500,height:920,borderRadius:36,border:'1px solid rgba(56,217,255,.34)',background:'linear-gradient(145deg,rgba(9,29,49,.76),rgba(4,15,27,.60))',boxShadow:'0 28px 90px rgba(0,0,0,.46), inset 0 1px rgba(255,255,255,.08)',backdropFilter:'blur(16px)',overflow:'hidden',opacity:enter,transform:`translateX(${(1-enter)*80}px) scale(${.97+.03*enter})`}}>
    <div style={{position:'absolute',inset:0,background:'radial-gradient(circle at 78% 18%,rgba(56,217,255,.14),transparent 35%)'}}/>
    <div style={{position:'absolute',top:34,right:34,left:34,direction:'rtl'}}>
      <div style={{fontSize:28,fontWeight:900,color:C.white}}>قدرة مراكز البيانات</div>
      <div style={{fontSize:15,letterSpacing:1.8,color:C.muted,marginTop:6}}>DATA CENTER CAPACITY</div>
    </div>
    <svg viewBox="0 0 430 520" style={{position:'absolute',left:34,top:130,width:430,height:520}}>
      {[0,1,2,3,4].map(i=><line key={i} x1="38" x2="406" y1={455-i*92} y2={455-i*92} stroke="rgba(169,186,201,.14)" strokeWidth="2"/>)}
      <line x1="38" x2="38" y1="70" y2="455" stroke="rgba(169,186,201,.28)" strokeWidth="2"/>
      <line x1="38" x2="406" y1="455" y2="455" stroke="rgba(169,186,201,.28)" strokeWidth="2"/>
      <rect x="86" y="397" width="72" height="58" rx="15" fill="rgba(56,217,255,.26)" stroke={C.cyan} strokeWidth="3"/>
      <rect x="285" y={455-365*p} width="72" height={365*p} rx="15" fill="rgba(233,185,73,.24)" stroke={C.gold} strokeWidth="3"/>
      <path d="M122 385 C190 350 235 230 321 95" fill="none" stroke={C.cyan} strokeWidth="5" strokeLinecap="round" strokeDasharray="500" strokeDashoffset={500*(1-p)} style={{filter:'drop-shadow(0 0 8px rgba(56,217,255,.8))'}}/>
      <circle cx="122" cy="385" r="9" fill={C.cyan}/><circle cx="321" cy="95" r={10+3*glow} fill={C.gold}/>
    </svg>
    <div style={{position:'absolute',left:48,top:660,width:165,textAlign:'center'}}><div style={{fontSize:54,fontWeight:950,color:C.cyan}}>68</div><div style={{fontSize:18,color:C.muted}}>MW</div></div>
    <div style={{position:'absolute',right:42,top:644,width:210,textAlign:'center'}}><div style={{fontSize:74,fontWeight:950,color:C.gold,textShadow:'0 0 24px rgba(233,185,73,.26)'}}>{Math.round(n)}</div><div style={{fontSize:18,color:C.muted}}>MW</div></div>
    <div style={{position:'absolute',left:42,right:42,bottom:42,height:78,borderRadius:20,border:'1px solid rgba(56,217,255,.16)',background:'rgba(56,217,255,.06)',display:'flex',alignItems:'center',justifyContent:'center',gap:12}}><span style={{fontSize:16,color:C.muted,letterSpacing:1.4}}>GROWTH</span><span style={{fontSize:32,fontWeight:900,color:C.white}}>6.9×</span></div>
  </div>;
};

export const HybridLiveAcceptance:React.FC=()=>{
  const f=useCurrentFrame();
  const shade=interpolate(f,[0,18],[0,1],{extrapolateRight:'clamp'});
  return <AbsoluteFill style={{background:C.navy,fontFamily:'Arial,sans-serif',color:C.white,overflow:'hidden'}}>
    <OffthreadVideo src={staticFile('presenter-source.mp4')} style={{position:'absolute',width:'100%',height:'100%',objectFit:'cover',transform:'translateX(-145px) scale(1.10)',transformOrigin:'center center'}}/>
    <AbsoluteFill style={{background:`linear-gradient(90deg,rgba(6,17,31,0) 0%,rgba(6,17,31,.02) 34%,rgba(6,17,31,.50) 60%,rgba(6,17,31,.88) 100%)`,opacity:shade}}/>
    <div style={{position:'absolute',top:58,left:52,right:52,display:'flex',justifyContent:'space-between',alignItems:'center'}}>
      <div style={{fontSize:15,letterSpacing:2.5,color:'rgba(246,250,253,.64)'}}>BEHIND THE NUMBER • LIVE DATA</div>
      <div style={{direction:'rtl',fontSize:27,fontWeight:950,color:C.gold}}>خلف الرقم</div>
    </div>
    <GlassChart/>
    <div style={{position:'absolute',left:455,top:845,width:160,height:2,background:`linear-gradient(90deg,rgba(56,217,255,0),${C.cyan})`,boxShadow:'0 0 12px rgba(56,217,255,.8)',opacity:interpolate(f,[75,105,240,265],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}/>
    <div style={{position:'absolute',left:598,top:839,width:14,height:14,borderRadius:14,background:C.cyan,boxShadow:'0 0 18px rgba(56,217,255,.95)',opacity:interpolate(f,[75,105,240,265],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'})}}/>
  </AbsoluteFill>;
};
