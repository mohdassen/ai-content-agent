import React from 'react';
import {AbsoluteFill, OffthreadVideo, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

const C={cyan:'#35D7FF',gold:'#F2C14E',white:'#F7FBFF',muted:'#A7BBCD'};
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const fade=(f:number,a:number,b:number,c:number,d:number)=>interpolate(f,[a,b,c,d],[0,1,1,0],clamp);

const Metric:React.FC<{f:number}>=({f})=>{const p=interpolate(f,[120,260],[0,1],clamp);const value=Math.round(interpolate(p,[0,1],[68,467],clamp));const enter=spring({frame:f-75,fps:30,config:{damping:20,stiffness:90}});return <div style={{position:'absolute',left:66,top:430,width:500,height:730,opacity:fade(f,55,85,310,345)*enter}}>
  <div style={{fontSize:17,letterSpacing:1.5,color:C.muted,direction:'rtl',textAlign:'right'}}>قدرة مراكز البيانات</div>
  <svg viewBox="0 0 500 430" style={{position:'absolute',left:0,top:85,width:500,height:430}}>
    {[0,1,2,3].map(i=><line key={i} x1="20" x2="475" y1={355-i*88} y2={355-i*88} stroke="rgba(167,187,205,.14)" strokeWidth="1"/>)}
    <defs><linearGradient id="fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={C.cyan} stopOpacity=".20"/><stop offset="1" stopColor={C.cyan} stopOpacity="0"/></linearGradient></defs>
    <path d="M38 340 C130 330 185 292 240 232 C302 164 360 102 458 55 L458 365 L38 365Z" fill="url(#fill)" opacity={p}/>
    <path d="M38 340 C130 330 185 292 240 232 C302 164 360 102 458 55" fill="none" stroke={C.cyan} strokeWidth="7" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1-p} style={{filter:'drop-shadow(0 0 10px rgba(53,215,255,.7))'}}/>
    <circle cx="38" cy="340" r="9" fill={C.cyan}/><circle cx="458" cy="55" r="12" fill={C.gold} style={{filter:'drop-shadow(0 0 12px rgba(242,193,78,.75))'}}/>
  </svg>
  <div style={{position:'absolute',left:6,bottom:94}}><div style={{fontSize:18,color:C.muted}}>2016</div><div style={{fontSize:62,fontWeight:950,color:C.cyan}}>68 <span style={{fontSize:20}}>MW</span></div></div>
  <div style={{position:'absolute',right:0,bottom:84,textAlign:'right'}}><div style={{fontSize:18,color:C.muted}}>TODAY</div><div style={{fontSize:76,fontWeight:950,color:C.gold}}>{value} <span style={{fontSize:20}}>MW</span></div></div>
</div>};

const Growth:React.FC<{f:number}>=({f})=>{const s=spring({frame:f-335,fps:30,config:{damping:16,stiffness:105}});return <div style={{position:'absolute',left:70,top:575,width:470,opacity:fade(f,325,350,470,500),transform:`scale(${.92+.08*s})`,transformOrigin:'left center'}}><div style={{fontSize:26,color:C.muted,direction:'rtl'}}>هذا يعني نموًا يقارب</div><div style={{fontSize:118,fontWeight:950,lineHeight:1,color:C.gold,marginTop:15}}>6.9×</div><div style={{fontSize:25,fontWeight:800,color:C.white,direction:'rtl',marginTop:15}}>سبعة أضعاف تقريبًا</div></div>};

const Meaning:React.FC<{f:number}>=({f})=>{const o=fade(f,490,525,735,785);return <div style={{position:'absolute',left:66,top:500,width:500,opacity:o,direction:'rtl',textAlign:'right'}}><div style={{fontSize:23,color:C.muted}}>الرقم لا يمثل كهرباء فقط</div><div style={{fontSize:42,fontWeight:900,lineHeight:1.35,marginTop:20,color:C.white}}>إنه البنية التي ستشغّل</div><div style={{display:'flex',gap:12,flexWrap:'wrap',justifyContent:'flex-start',direction:'rtl',marginTop:26}}>{['الذكاء الاصطناعي','الحوسبة','الخدمات الرقمية'].map((x,i)=><div key={x} style={{padding:'12px 18px',borderRadius:18,border:`1px solid ${i===0?'rgba(242,193,78,.34)':'rgba(53,215,255,.24)'}`,background:'rgba(3,12,24,.38)',fontSize:21,fontWeight:800,color:i===0?C.gold:C.cyan}}>{x}</div>)}</div></div>};

export const MasterExplainer:React.FC=()=>{const f=useCurrentFrame();const {fps}=useVideoConfig();const brand=interpolate(f,[0,22],[0,1],clamp);return <AbsoluteFill style={{background:'#020712',overflow:'hidden',fontFamily:'Arial,sans-serif'}}>
  <OffthreadVideo src={staticFile('presenter-master.mp4')} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover'}} volume={1}/>
  <AbsoluteFill style={{background:'linear-gradient(90deg,rgba(2,7,18,.20) 0%,rgba(2,7,18,.05) 49%,rgba(2,7,18,0) 70%)',pointerEvents:'none'}}/>
  <div style={{position:'absolute',top:70,left:62,right:62,display:'flex',justifyContent:'space-between',alignItems:'center',opacity:brand}}><span style={{fontSize:12,letterSpacing:2.6,color:'rgba(247,251,255,.5)'}}>BEHIND THE NUMBER</span><span style={{fontSize:28,fontWeight:950,color:C.gold,direction:'rtl'}}>خلف الرقم</span></div>
  <Metric f={f}/><Growth f={f}/><Meaning f={f}/>
  <div style={{position:'absolute',left:66,bottom:92,width:485,height:1,background:'linear-gradient(90deg,rgba(53,215,255,.55),rgba(242,193,78,.35),transparent)',opacity:interpolate(f,[15,45],[0,1],clamp)}}/>
</AbsoluteFill>};
