import React from 'react';
import {AbsoluteFill, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const C={bg:'#020712',cyan:'#35D7FF',gold:'#F2C14E',white:'#F7FBFF',muted:'#9CB2C8'};
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};

const Grid=()=> <AbsoluteFill style={{background:'radial-gradient(circle at 22% 34%,rgba(53,215,255,.12),transparent 28%),radial-gradient(circle at 78% 58%,rgba(242,193,78,.05),transparent 24%),linear-gradient(180deg,#04101f 0%,#020712 100%)'}}><div style={{position:'absolute',inset:0,opacity:.15,backgroundImage:'linear-gradient(rgba(53,215,255,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(53,215,255,.07) 1px,transparent 1px)',backgroundSize:'72px 72px',maskImage:'linear-gradient(to bottom,transparent 7%,black 30%,black 82%,transparent 100%)'}}/></AbsoluteFill>;

const DataWall:React.FC=()=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const enter=spring({frame:f-10,fps,config:{damping:20,stiffness:90}});const p=interpolate(f,[42,170],[0,1],clamp);const v=Math.round(interpolate(p,[0,1],[68,467],clamp));return <div style={{position:'absolute',left:54,top:330,width:500,height:800,opacity:enter,transform:`translateX(${(1-enter)*-55}px)`}}>
 <div style={{position:'absolute',inset:0,borderRadius:34,border:'1px solid rgba(53,215,255,.36)',background:'linear-gradient(145deg,rgba(8,28,49,.94),rgba(3,13,27,.88))',boxShadow:'0 30px 90px rgba(0,0,0,.46),0 0 40px rgba(53,215,255,.08)'}}/>
 <div style={{position:'absolute',top:36,left:36,right:36,direction:'rtl',textAlign:'right'}}><div style={{fontSize:29,fontWeight:900,color:C.white}}>قدرة مراكز البيانات</div><div style={{fontSize:13,letterSpacing:1.8,marginTop:8,color:C.muted}}>SAUDI DATA CENTER CAPACITY</div></div>
 <svg viewBox="0 0 420 450" style={{position:'absolute',left:38,top:138,width:420,height:450}}>{[0,1,2,3,4].map(i=><line key={i} x1="34" x2="388" y1={375-i*72} y2={375-i*72} stroke="rgba(157,179,200,.14)" strokeWidth="2"/>)}<path d="M65 346 C138 332 198 286 248 224 C298 160 342 104 378 72" fill="none" stroke={C.cyan} strokeWidth="7" strokeLinecap="round" strokeDasharray="560" strokeDashoffset={560*(1-p)} style={{filter:'drop-shadow(0 0 10px rgba(53,215,255,.75))'}}/><circle cx="65" cy="346" r="9" fill={C.cyan}/><circle cx="378" cy="72" r="12" fill={C.gold}/></svg>
 <div style={{position:'absolute',left:44,bottom:96,textAlign:'center'}}><b style={{fontSize:54,color:C.cyan}}>68</b><div style={{fontSize:15,color:C.muted}}>MW</div></div><div style={{position:'absolute',right:34,bottom:82,textAlign:'center'}}><b style={{fontSize:76,color:C.gold}}>{v}</b><div style={{fontSize:15,color:C.muted}}>MW</div></div><div style={{position:'absolute',left:170,right:170,bottom:28,fontSize:22,fontWeight:900,color:C.white,textAlign:'center'}}>6.9×</div>
 </div>};

const LowerThird=()=> <div style={{position:'absolute',left:62,right:62,bottom:72,height:175,borderRadius:28,border:'1px solid rgba(242,193,78,.34)',background:'linear-gradient(90deg,rgba(5,18,34,.94),rgba(5,18,34,.80))',boxShadow:'0 20px 55px rgba(0,0,0,.35)',padding:'27px 36px',direction:'rtl',textAlign:'right'}}><div style={{fontSize:33,fontWeight:950,color:C.white}}>من <span style={{color:C.cyan}}>68</span> إلى <span style={{color:C.gold}}>467</span> ميغاواط</div><div style={{fontSize:19,lineHeight:1.55,color:C.muted,marginTop:10}}>نمو يقارب سبعة أضعاف في قدرة مراكز البيانات السعودية.</div></div>;

export const StudioAcceptance:React.FC=()=>{const f=useCurrentFrame();const intro=interpolate(f,[0,16],[0,1],clamp);return <AbsoluteFill style={{background:C.bg,overflow:'hidden',fontFamily:'Arial,sans-serif'}}><Grid/>
 <div style={{position:'absolute',top:62,left:58,right:58,display:'flex',justifyContent:'space-between',alignItems:'center',opacity:intro}}><span style={{fontSize:12,letterSpacing:2.4,color:'rgba(247,251,255,.56)'}}>BEHIND THE NUMBER</span><span style={{fontSize:30,fontWeight:950,color:C.gold,direction:'rtl'}}>خلف الرقم</span></div>
 <DataWall/>
 <div style={{position:'absolute',right:-42,top:245,width:590,height:1370,overflow:'visible'}}><OffthreadVideo src={staticFile('presenter-transparent.webm')} style={{position:'absolute',width:760,height:1350,right:-88,top:0,objectFit:'contain'}}/></div>
 <div style={{position:'absolute',left:558,top:355,width:2,height:690,background:'linear-gradient(to bottom,transparent,rgba(53,215,255,.26),transparent)'}}/>
 <LowerThird/>
 </AbsoluteFill>};
