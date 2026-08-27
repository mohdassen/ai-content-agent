import React from 'react';
import {AbsoluteFill, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const C={bg:'#020712',cyan:'#35D7FF',gold:'#F2C14E',white:'#F7FBFF',muted:'#9DB3C8'};
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};

const DataWall:React.FC=()=>{
 const f=useCurrentFrame(); const {fps}=useVideoConfig();
 const enter=spring({frame:f-12,fps,config:{damping:18,stiffness:95}});
 const p=interpolate(f,[48,185],[0,1],clamp);
 const value=Math.round(interpolate(p,[0,1],[68,467],clamp));
 const pulse=.65+.35*Math.sin(f/8);
 return <div style={{position:'absolute',right:32,top:300,width:515,height:930,opacity:enter,transform:`perspective(1200px) rotateY(-5deg) translateX(${(1-enter)*100}px)`,transformOrigin:'right center'}}>
   <div style={{position:'absolute',inset:0,borderRadius:34,border:'1px solid rgba(53,215,255,.42)',background:'linear-gradient(145deg,rgba(7,24,43,.74),rgba(3,12,24,.52))',boxShadow:'0 35px 110px rgba(0,0,0,.55),0 0 55px rgba(53,215,255,.09)',backdropFilter:'blur(18px)'}}/>
   <div style={{position:'absolute',top:36,left:38,right:38,direction:'rtl'}}><div style={{fontSize:29,fontWeight:900,color:C.white}}>قدرة مراكز البيانات</div><div style={{fontSize:15,marginTop:7,letterSpacing:2,color:C.muted}}>SAUDI DATA CENTER CAPACITY</div></div>
   <svg viewBox="0 0 440 560" style={{position:'absolute',left:35,top:145,width:440,height:560}}>
    {[0,1,2,3,4].map(i=><line key={i} x1="34" x2="414" y1={480-i*95} y2={480-i*95} stroke="rgba(157,179,200,.14)" strokeWidth="2"/>)}
    <path d="M70 430 C150 405 205 330 260 245 C310 170 350 115 392 82" fill="none" stroke={C.cyan} strokeWidth="7" strokeLinecap="round" strokeDasharray="600" strokeDashoffset={600*(1-p)} style={{filter:'drop-shadow(0 0 10px rgba(53,215,255,.75))'}}/>
    <circle cx="70" cy="430" r="10" fill={C.cyan}/><circle cx="392" cy="82" r={12+4*pulse} fill={C.gold} style={{filter:'drop-shadow(0 0 12px rgba(242,193,78,.8))'}}/>
    <rect x="48" y="444" width="48" height="36" rx="9" fill="rgba(53,215,255,.28)" stroke={C.cyan}/>
    <rect x="368" y={480-398*p} width="48" height={398*p} rx="9" fill="rgba(242,193,78,.20)" stroke={C.gold}/>
   </svg>
   <div style={{position:'absolute',left:44,bottom:130,textAlign:'center'}}><b style={{fontSize:54,color:C.cyan}}>68</b><div style={{fontSize:17,color:C.muted}}>MW</div></div>
   <div style={{position:'absolute',right:38,bottom:112,textAlign:'center'}}><b style={{fontSize:82,color:C.gold,textShadow:'0 0 24px rgba(242,193,78,.25)'}}>{value}</b><div style={{fontSize:18,color:C.muted}}>MW</div></div>
   <div style={{position:'absolute',left:150,right:150,bottom:42,height:56,borderRadius:18,border:'1px solid rgba(53,215,255,.22)',display:'flex',alignItems:'center',justifyContent:'center',fontSize:25,fontWeight:900,color:C.white}}>6.9×</div>
 </div>
};

const Pointer:React.FC=()=>{const f=useCurrentFrame();const a=interpolate(f,[70,100,220,250],[0,1,1,0],clamp);const x=interpolate(f,[100,165],[0,72],clamp);return <div style={{position:'absolute',left:420+x,top:835,opacity:a,transform:'rotate(-8deg)',transformOrigin:'left center'}}><div style={{width:165,height:3,background:`linear-gradient(90deg,rgba(53,215,255,0),${C.cyan})`,boxShadow:'0 0 12px rgba(53,215,255,.9)'}}/><div style={{position:'absolute',right:-6,top:-6,width:15,height:15,borderRadius:20,background:C.cyan,boxShadow:'0 0 22px rgba(53,215,255,1)'}}/></div>};

export const HybridLiveAcceptance:React.FC=()=>{
 const f=useCurrentFrame(); const intro=interpolate(f,[0,18],[0,1],clamp);
 return <AbsoluteFill style={{background:C.bg,overflow:'hidden',fontFamily:'Arial,sans-serif'}}>
   <OffthreadVideo src={staticFile('presenter-source.mp4')} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',objectPosition:'42% center',transform:'scale(1.035) translateX(-105px)',transformOrigin:'center center'}}/>
   <AbsoluteFill style={{background:'linear-gradient(90deg,rgba(2,7,18,.05) 0%,rgba(2,7,18,.04) 36%,rgba(2,7,18,.38) 55%,rgba(2,7,18,.82) 100%)'}}/>
   <div style={{position:'absolute',top:48,left:48,right:48,display:'flex',alignItems:'center',justifyContent:'space-between',opacity:intro}}><span style={{fontSize:14,letterSpacing:3,color:'rgba(247,251,255,.64)'}}>BEHIND THE NUMBER • LIVE EXPLAINER</span><span style={{fontSize:28,fontWeight:950,color:C.gold,direction:'rtl'}}>خلف الرقم</span></div>
   <DataWall/><Pointer/>
   <div style={{position:'absolute',left:42,bottom:48,fontSize:14,letterSpacing:2.2,color:'rgba(247,251,255,.48)'}}>PRESENTER + INTERACTIVE DATA • NO LEGACY TEMPLATE</div>
 </AbsoluteFill>;
};
