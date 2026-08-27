import React from 'react';
import {AbsoluteFill, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const C={bg:'#020712',cyan:'#35D7FF',gold:'#F2C14E',white:'#F7FBFF',muted:'#9DB3C8'};
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};

const DataWall:React.FC=()=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const enter=spring({frame:f-15,fps,config:{damping:20,stiffness:90}});const p=interpolate(f,[55,190],[0,1],clamp);const value=Math.round(interpolate(p,[0,1],[68,467],clamp));return <div style={{position:'absolute',right:54,top:430,width:470,height:690,opacity:enter,transform:`translateX(${(1-enter)*55}px)`,transformOrigin:'right center'}}>
 <div style={{position:'absolute',inset:0,borderRadius:30,border:'1px solid rgba(53,215,255,.34)',background:'linear-gradient(145deg,rgba(8,27,48,.88),rgba(3,13,27,.78))',boxShadow:'0 28px 90px rgba(0,0,0,.48),0 0 38px rgba(53,215,255,.07)'}}/>
 <div style={{position:'absolute',top:34,left:34,right:34,direction:'rtl',textAlign:'right'}}><div style={{fontSize:27,fontWeight:900,color:C.white}}>قدرة مراكز البيانات</div><div style={{fontSize:13,marginTop:7,letterSpacing:1.7,color:C.muted}}>SAUDI DATA CENTER CAPACITY</div></div>
 <svg viewBox="0 0 400 400" style={{position:'absolute',left:35,top:125,width:400,height:400}}>{[0,1,2,3].map(i=><line key={i} x1="30" x2="375" y1={340-i*82} y2={340-i*82} stroke="rgba(157,179,200,.13)" strokeWidth="2"/>)}<path d="M58 315 C130 300 190 250 235 190 C285 120 325 88 360 58" fill="none" stroke={C.cyan} strokeWidth="6" strokeLinecap="round" strokeDasharray="520" strokeDashoffset={520*(1-p)} style={{filter:'drop-shadow(0 0 9px rgba(53,215,255,.7))'}}/><circle cx="58" cy="315" r="8" fill={C.cyan}/><circle cx="360" cy="58" r="11" fill={C.gold}/></svg>
 <div style={{position:'absolute',left:42,bottom:74,textAlign:'center'}}><b style={{fontSize:48,color:C.cyan}}>68</b><div style={{fontSize:14,color:C.muted}}>MW</div></div><div style={{position:'absolute',right:36,bottom:62,textAlign:'center'}}><b style={{fontSize:68,color:C.gold}}>{value}</b><div style={{fontSize:14,color:C.muted}}>MW</div></div><div style={{position:'absolute',left:178,bottom:28,fontSize:20,fontWeight:900,color:C.white}}>6.9×</div>
 </div>};

export const HybridLiveAcceptance:React.FC=()=>{const f=useCurrentFrame();const intro=interpolate(f,[0,18],[0,1],clamp);return <AbsoluteFill style={{background:C.bg,overflow:'hidden',fontFamily:'Arial,sans-serif'}}>
 <div style={{position:'absolute',left:-48,top:150,width:720,height:1600,overflow:'hidden'}}><OffthreadVideo src={staticFile('presenter-source.mp4')} style={{position:'absolute',width:1080,height:1920,left:-125,top:-145,objectFit:'cover',transform:'scale(.88)',transformOrigin:'top left'}}/></div>
 <AbsoluteFill style={{background:'linear-gradient(90deg,rgba(2,7,18,.02) 0%,rgba(2,7,18,.05) 43%,rgba(2,7,18,.30) 59%,rgba(2,7,18,.74) 100%)',pointerEvents:'none'}}/>
 <div style={{position:'absolute',top:70,left:58,right:58,display:'flex',alignItems:'center',justifyContent:'space-between',opacity:intro}}><span style={{fontSize:12,letterSpacing:2.6,color:'rgba(247,251,255,.54)'}}>BEHIND THE NUMBER</span><span style={{fontSize:27,fontWeight:950,color:C.gold,direction:'rtl'}}>خلف الرقم</span></div>
 <DataWall/>
 <div style={{position:'absolute',left:70,right:70,bottom:100,height:150,borderTop:'1px solid rgba(53,215,255,.25)',paddingTop:26,direction:'rtl',textAlign:'right'}}><div style={{fontSize:28,fontWeight:900,color:C.white}}>من 68 إلى 467 ميغاواط</div><div style={{fontSize:18,lineHeight:1.55,marginTop:10,color:C.muted}}>نمو يقارب سبعة أضعاف في قدرة البنية الرقمية.</div></div>
 </AbsoluteFill>};
