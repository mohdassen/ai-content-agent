import React from 'react';
import {AbsoluteFill, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const C={bg:'#020712',panel:'#07182B',cyan:'#35D7FF',gold:'#F2C14E',white:'#F7FBFF',muted:'#9CB2C8'};
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};

const Grid=()=> <AbsoluteFill style={{background:'radial-gradient(circle at 76% 32%,rgba(53,215,255,.11),transparent 29%),radial-gradient(circle at 20% 58%,rgba(242,193,78,.05),transparent 25%),linear-gradient(180deg,#04101f 0%,#020712 100%)'}}><div style={{position:'absolute',inset:0,opacity:.16,backgroundImage:'linear-gradient(rgba(53,215,255,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(53,215,255,.08) 1px,transparent 1px)',backgroundSize:'72px 72px',maskImage:'linear-gradient(to bottom,transparent 7%,black 32%,black 80%,transparent 100%)'}}/></AbsoluteFill>;

const DataWall:React.FC=()=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const enter=spring({frame:f-12,fps,config:{damping:20,stiffness:90}});const p=interpolate(f,[48,188],[0,1],clamp);const v=Math.round(interpolate(p,[0,1],[68,467],clamp));return <div style={{position:'absolute',right:54,top:285,width:510,height:870,opacity:enter,transform:`translateX(${(1-enter)*65}px)`}}>
 <div style={{position:'absolute',inset:0,borderRadius:34,border:'1px solid rgba(53,215,255,.38)',background:'linear-gradient(145deg,rgba(8,28,49,.93),rgba(3,13,27,.86))',boxShadow:'0 30px 90px rgba(0,0,0,.48),0 0 40px rgba(53,215,255,.08)'}}/>
 <div style={{position:'absolute',top:38,left:38,right:38,direction:'rtl',textAlign:'right'}}><div style={{fontSize:30,fontWeight:900,color:C.white}}>قدرة مراكز البيانات</div><div style={{fontSize:13,letterSpacing:1.8,marginTop:8,color:C.muted}}>SAUDI DATA CENTER CAPACITY</div></div>
 <svg viewBox="0 0 430 480" style={{position:'absolute',left:40,top:145,width:430,height:480}}>{[0,1,2,3,4].map(i=><line key={i} x1="36" x2="398" y1={400-i*78} y2={400-i*78} stroke="rgba(157,179,200,.14)" strokeWidth="2"/>)}<path d="M68 370 C145 353 205 304 255 237 C305 170 350 105 385 76" fill="none" stroke={C.cyan} strokeWidth="7" strokeLinecap="round" strokeDasharray="570" strokeDashoffset={570*(1-p)} style={{filter:'drop-shadow(0 0 10px rgba(53,215,255,.75))'}}/><circle cx="68" cy="370" r="9" fill={C.cyan}/><circle cx="385" cy="76" r="12" fill={C.gold} style={{filter:'drop-shadow(0 0 12px rgba(242,193,78,.85))'}}/><rect x="363" y={400-324*p} width="44" height={324*p} rx="8" fill="rgba(242,193,78,.18)" stroke={C.gold}/></svg>
 <div style={{position:'absolute',left:46,bottom:104,textAlign:'center'}}><b style={{fontSize:56,color:C.cyan}}>68</b><div style={{fontSize:15,color:C.muted}}>MW</div></div><div style={{position:'absolute',right:38,bottom:88,textAlign:'center'}}><b style={{fontSize:78,color:C.gold}}>{v}</b><div style={{fontSize:15,color:C.muted}}>MW</div></div>
 <div style={{position:'absolute',left:175,right:175,bottom:30,height:54,borderRadius:18,border:'1px solid rgba(53,215,255,.22)',display:'flex',alignItems:'center',justifyContent:'center',fontSize:22,fontWeight:900,color:C.white}}>6.9×</div>
 </div>};

const LowerThird=()=> <div style={{position:'absolute',left:64,right:64,bottom:72,height:185,borderRadius:28,border:'1px solid rgba(242,193,78,.36)',background:'linear-gradient(90deg,rgba(5,18,34,.92),rgba(5,18,34,.78))',boxShadow:'0 20px 55px rgba(0,0,0,.35)',padding:'28px 38px',direction:'rtl',textAlign:'right'}}><div style={{fontSize:34,fontWeight:950,color:C.white}}>من <span style={{color:C.cyan}}>68</span> إلى <span style={{color:C.gold}}>467</span> ميغاواط</div><div style={{fontSize:20,lineHeight:1.55,color:C.muted,marginTop:10}}>نمو يقارب سبعة أضعاف في قدرة مراكز البيانات السعودية.</div></div>;

export const StudioAcceptance:React.FC=()=>{const f=useCurrentFrame();const intro=interpolate(f,[0,18],[0,1],clamp);return <AbsoluteFill style={{background:C.bg,overflow:'hidden',fontFamily:'Arial,sans-serif'}}><Grid/>
 <div style={{position:'absolute',top:62,left:58,right:58,display:'flex',justifyContent:'space-between',alignItems:'center',opacity:intro}}><span style={{fontSize:12,letterSpacing:2.4,color:'rgba(247,251,255,.56)'}}>BEHIND THE NUMBER</span><span style={{fontSize:30,fontWeight:950,color:C.gold,direction:'rtl'}}>خلف الرقم</span></div>
 <div style={{position:'absolute',left:-24,top:230,width:590,height:1450,overflow:'visible'}}><OffthreadVideo src={staticFile('presenter-cutout.webm')} style={{position:'absolute',width:760,height:1350,left:-82,top:0,objectFit:'contain'}}/></div>
 <div style={{position:'absolute',left:510,top:330,width:2,height:720,background:'linear-gradient(to bottom,transparent,rgba(53,215,255,.32),transparent)'}}/>
 <DataWall/><LowerThird/>
 </AbsoluteFill>};
