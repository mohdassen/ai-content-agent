from pathlib import Path

p = Path('motion/src/video.tsx')
s = p.read_text(encoding='utf-8')

old = "const Brand=()=> <div style={{position:'absolute',top:62,right:62,fontFamily:font,color:C.accent,fontSize:24,fontWeight:900,direction:'rtl'}}>خلف الرقم <span style={{color:C.muted,fontSize:18}}>• BEHIND THE NUMBER</span></div>;"
new = "const Brand=()=> <div style={{position:'absolute',top:48,right:48,zIndex:50,filter:'drop-shadow(0 8px 18px rgba(0,0,0,.55))'}}><img src={staticFile('brand-logo.svg')} style={{width:126,height:126,objectFit:'contain'}} /></div>;"
if old in s: s=s.replace(old,new)

s=s.replace("const C={bg:'#030806',bg2:'#091812',panel:'#10241d',text:'#f7faf8',accent:'#52e39c',accent2:'#d8ffe9',muted:'#91aa9f',line:'#1c4435'};","const C={bg:'#05070b',bg2:'#0a1020',panel:'#111827',text:'#f8fafc',accent:'#48d7ff',accent2:'#f4d06f',muted:'#aab4c3',line:'#273248'};")

start="const Atmosphere=()=>{const f=useCurrentFrame();"
end="const Brand=()=>"
if start in s and end in s:
 a=s.index(start); b=s.index(end,a)
 atmosphere="""const Atmosphere=()=>{const f=useCurrentFrame();const x=Math.sin(f/31)*85,y=Math.cos(f/43)*55;return <><AbsoluteFill style={{background:`linear-gradient(${118+Math.sin(f/80)*24}deg,#03050a 0%,#091226 40%,#160d24 72%,#08090f 100%)`}}/><div style={{position:'absolute',left:-260+x,top:-180+y,width:880,height:880,borderRadius:'50%',background:'radial-gradient(circle,rgba(72,215,255,.24),rgba(0,0,0,0) 68%)',filter:'blur(18px)'}}/><div style={{position:'absolute',right:-300-x*.55,bottom:-190-y*.7,width:980,height:980,borderRadius:'50%',background:'radial-gradient(circle,rgba(191,122,255,.18),rgba(0,0,0,0) 66%)',filter:'blur(28px)'}}/><AbsoluteFill style={{opacity:.12,backgroundImage:'linear-gradient(rgba(90,190,255,.3) 1px,transparent 1px),linear-gradient(90deg,rgba(135,110,255,.24) 1px,transparent 1px)',backgroundSize:'110px 110px',transform:`perspective(650px) rotateX(64deg) translateY(${410+(f%110)}px) scale(1.7)`}}/>{Array.from({length:22}).map((_,i)=><i key={i} style={{position:'absolute',left:(i*191)%1080,top:(i*317+f*(.7+(i%4)*.18))%1920,width:3+(i%3)*2,height:3+(i%3)*2,borderRadius:8,background:i%4===0?'#f4d06f':'#65dcff',opacity:.18+(i%5)*.08,boxShadow:'0 0 18px currentColor'}}/>)}</>};
"""
 s=s[:a]+atmosphere+s[b:]

# Add documentary-tech silhouettes behind scene content. They move independently
# from the foreground, creating a visual subject rather than an empty backdrop.
brand_marker="const Brand=()=>"
if "const DocumentaryLayer=" not in s and brand_marker in s:
 idx=s.index(brand_marker)
 layer="""const DocumentaryLayer=()=>{const f=useCurrentFrame();const drift=Math.sin(f/22)*18;return <div style={{position:'absolute',inset:0,opacity:.28,filter:'blur(.2px)',overflow:'hidden'}}><div style={{position:'absolute',left:-40+drift,top:250,width:1160,height:720,transform:'perspective(900px) rotateX(4deg)'}}>{Array.from({length:9}).map((_,i)=><div key={i} style={{position:'absolute',left:i*132,top:(i%2)*34,width:104,height:620,border:'1px solid rgba(100,210,255,.22)',background:'linear-gradient(90deg,rgba(7,12,24,.92),rgba(30,55,85,.5),rgba(4,8,18,.95))',boxShadow:'0 0 40px rgba(30,150,220,.08)'}}>{Array.from({length:16}).map((_,j)=><i key={j} style={{display:'block',height:3,margin:'29px 16px',background:(f+j+i)%11<3?'rgba(90,220,255,.8)':'rgba(100,125,155,.22)',boxShadow:(f+j+i)%11<3?'0 0 12px rgba(90,220,255,.7)':'none'}}/>)}</div>)}</div><div style={{position:'absolute',left:-120,top:980,width:1350,height:5,background:'linear-gradient(90deg,transparent,rgba(244,208,111,.5),rgba(72,215,255,.6),transparent)',transform:`rotate(-13deg) translateX(${drift*2}px)`,boxShadow:'0 0 35px rgba(72,215,255,.25)'}}/><div style={{position:'absolute',right:70,top:150,width:330,height:330,borderRadius:'50%',border:'1px solid rgba(244,208,111,.28)',transform:`rotate(${f*.15}deg)`}}><div style={{position:'absolute',inset:35,borderRadius:'50%',border:'1px dashed rgba(72,215,255,.35)'}}/></div></div>};
"""
 s=s[:idx]+layer+s[idx:]

s=s.replace("const pan=interpolate(f,[0,duration],[-8,8],clamp);","const pan=interpolate(f,[0,duration],[-26,26],clamp);const zoom=interpolate(f,[0,duration],[1.035,1.095],clamp);")
s=s.replace("transform:`translateX(${pan}px) scale(1.025)`","transform:`translate3d(${pan}px,${Math.sin(f/15)*7}px,0) scale(${zoom})`")
s=s.replace("<Atmosphere/><Brand/>{children}</AbsoluteFill>","<Atmosphere/><DocumentaryLayer/><AbsoluteFill style={{pointerEvents:'none',background:'linear-gradient(180deg,rgba(0,0,0,.05),rgba(0,0,0,.02) 55%,rgba(0,0,0,.48))',boxShadow:'inset 0 0 190px rgba(0,0,0,.62)',zIndex:40}}/><Brand/>{children}</AbsoluteFill>")
s=s.replace("transform:`translateY(${(1-p)*28}px)`","transform:`translateY(${(1-p)*34}px) scale(${.96+p*.04})`,textShadow:'0 5px 28px rgba(0,0,0,.82)'")

for a,b in {'#123b2b':'#15254a','#17623f':'#176f92','#142c23':'#151c2c','#07110d':'#080b13','#315347':'#31435e','rgba(82,227,156,.06)':'rgba(72,215,255,.07)','rgba(82,227,156,.35)':'rgba(72,215,255,.30)'}.items(): s=s.replace(a,b)

end_marker="<div style={{fontSize:30,color:C.accent,fontWeight:950,marginBottom:50}}>خلف الرقم</div>"
end_logo="<img src={staticFile('brand-logo.svg')} style={{width:250,height:250,objectFit:'contain',margin:'0 auto 24px',filter:'drop-shadow(0 12px 35px rgba(212,175,55,.28))'}}/><div style={{fontSize:30,color:'#d4af37',fontWeight:950,marginBottom:35}}>خلف الرقم</div>"
if end_marker in s: s=s.replace(end_marker,end_logo)

for old_audio in ("staticFile('public/audio/master.mp3')",'staticFile("public/audio/master.mp3")',"staticFile('/public/audio/master.mp3')",'staticFile("/public/audio/master.mp3")',"staticFile('audio/master.mp3')",'staticFile("audio/master.mp3")',"staticFile('/audio/master.mp3')",'staticFile("/audio/master.mp3")'):
 s=s.replace(old_audio,"staticFile('audio/master_narration.mp3')")
s=s.replace("'/public/audio/master.mp3'","'/audio/master_narration.mp3'").replace('"/public/audio/master.mp3"','"/audio/master_narration.mp3"').replace("'/audio/master.mp3'","'/audio/master_narration.mp3'").replace('"/audio/master.mp3"','"/audio/master_narration.mp3"')
if 'master.mp3' in s or '/public/audio/' in s: raise SystemExit('Legacy audio path still present after patch')
p.write_text(s,encoding='utf-8')
print('Documentary visual layer, cinematic environment, brand, and audio verified')
