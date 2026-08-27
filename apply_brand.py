from pathlib import Path

p = Path('motion/src/video.tsx')
s = p.read_text(encoding='utf-8')

# Brand mark
old = "const Brand=()=> <div style={{position:'absolute',top:62,right:62,fontFamily:font,color:C.accent,fontSize:24,fontWeight:900,direction:'rtl'}}>خلف الرقم <span style={{color:C.muted,fontSize:18}}>• BEHIND THE NUMBER</span></div>;"
new = "const Brand=()=> <div style={{position:'absolute',top:48,right:48,zIndex:50,filter:'drop-shadow(0 8px 18px rgba(0,0,0,.55))'}}><img src={staticFile('brand-logo.svg')} style={{width:126,height:126,objectFit:'contain'}} /></div>;"
if old in s:
    s = s.replace(old, new)

# Replace the old green-dominant palette with a premium neutral/cyan/gold palette.
s = s.replace(
    "const C={bg:'#030806',bg2:'#091812',panel:'#10241d',text:'#f7faf8',accent:'#52e39c',accent2:'#d8ffe9',muted:'#91aa9f',line:'#1c4435'};",
    "const C={bg:'#05070b',bg2:'#0a1020',panel:'#111827',text:'#f8fafc',accent:'#48d7ff',accent2:'#f4d06f',muted:'#aab4c3',line:'#273248'};"
)

# Replace the static green atmosphere with moving, multi-color cinematic layers.
start = "const Atmosphere=()=>{const f=useCurrentFrame();"
end = "const Brand=()=>"
if start in s and end in s:
    a = s.index(start)
    b = s.index(end, a)
    atmosphere = """const Atmosphere=()=>{const f=useCurrentFrame();const x=Math.sin(f/31)*85,y=Math.cos(f/43)*55;const hue=(f*0.55)%360;return <><AbsoluteFill style={{background:`linear-gradient(${118+Math.sin(f/80)*24}deg,#03050a 0%,#091226 40%,#160d24 72%,#08090f 100%)`}}/><div style={{position:'absolute',left:-260+x,top:-180+y,width:880,height:880,borderRadius:'50%',background:`radial-gradient(circle,hsla(${195+hue*.05},95%,62%,.25),rgba(0,0,0,0) 68%)`,filter:'blur(18px)'}}/><div style={{position:'absolute',right:-300-x*.55,bottom:-190-y*.7,width:980,height:980,borderRadius:'50%',background:`radial-gradient(circle,rgba(191,122,255,.18),rgba(0,0,0,0) 66%)`,filter:'blur(28px)'}}/><div style={{position:'absolute',left:160-x*.25,top:520-y*.35,width:740,height:520,borderRadius:'50%',background:`radial-gradient(circle,rgba(244,208,111,.13),rgba(0,0,0,0) 68%)`,filter:'blur(32px)',transform:`rotate(${f*.08}deg)`}}/><AbsoluteFill style={{opacity:.13,backgroundImage:'linear-gradient(rgba(90,190,255,.32) 1px,transparent 1px),linear-gradient(90deg,rgba(135,110,255,.26) 1px,transparent 1px)',backgroundSize:'110px 110px',transform:`perspective(650px) rotateX(64deg) translateY(${410+(f%110)}px) scale(1.7)`}}/>{Array.from({length:22}).map((_,i)=>{const px=(i*191)%1080,py=(i*317+f*(.7+(i%4)*.18))%1920;return <i key={i} style={{position:'absolute',left:px,top:py,width:3+(i%3)*2,height:3+(i%3)*2,borderRadius:8,background:i%4===0?'#f4d06f':'#65dcff',opacity:.18+(i%5)*.08,boxShadow:'0 0 18px currentColor'}}/>})}</>};
"""
    s = s[:a] + atmosphere + s[b:]

# More camera movement and depth, without changing narration timing.
s = s.replace("const pan=interpolate(f,[0,duration],[-8,8],clamp);", "const pan=interpolate(f,[0,duration],[-26,26],clamp);const zoom=interpolate(f,[0,duration],[1.035,1.095],clamp);")
s = s.replace("transform:`translateX(${pan}px) scale(1.025)`", "transform:`translate3d(${pan}px,${Math.sin(f/15)*7}px,0) scale(${zoom})`")
s = s.replace("<Atmosphere/><Brand/>{children}</AbsoluteFill>", "<Atmosphere/><AbsoluteFill style={{pointerEvents:'none',background:'linear-gradient(180deg,rgba(0,0,0,.08),rgba(0,0,0,.02) 55%,rgba(0,0,0,.48))',boxShadow:'inset 0 0 190px rgba(0,0,0,.66)',zIndex:40}}/><Brand/>{children}</AbsoluteFill>")
s = s.replace("transform:`translateY(${(1-p)*28}px)`", "transform:`translateY(${(1-p)*34}px) scale(${.96+p*.04})`,textShadow:'0 5px 28px rgba(0,0,0,.82)'")

# Replace remaining hard-coded green visual accents left by older scenes.
for old_color, new_color in {
    '#123b2b':'#15254a', '#17623f':'#176f92', '#142c23':'#151c2c', '#07110d':'#080b13',
    '#315347':'#31435e', 'rgba(82,227,156,.06)':'rgba(72,215,255,.07)',
    'rgba(82,227,156,.35)':'rgba(72,215,255,.30)'
}.items():
    s = s.replace(old_color, new_color)

# Closing logo treatment
end_marker = "<div style={{fontSize:30,color:C.accent,fontWeight:950,marginBottom:50}}>خلف الرقم</div>"
end_logo = "<img src={staticFile('brand-logo.svg')} style={{width:250,height:250,objectFit:'contain',margin:'0 auto 24px',filter:'drop-shadow(0 12px 35px rgba(212,175,55,.28))'}}/><div style={{fontSize:30,color:'#d4af37',fontWeight:950,marginBottom:35}}>خلف الرقم</div>"
if end_marker in s:
    s = s.replace(end_marker, end_logo)

# Stable narration path
for old_audio in (
    "staticFile('public/audio/master.mp3')", 'staticFile("public/audio/master.mp3")',
    "staticFile('/public/audio/master.mp3')", 'staticFile("/public/audio/master.mp3")',
    "staticFile('audio/master.mp3')", 'staticFile("audio/master.mp3")',
    "staticFile('/audio/master.mp3')", 'staticFile("/audio/master.mp3")',
):
    s = s.replace(old_audio, "staticFile('audio/master_narration.mp3')")
s = s.replace("'/public/audio/master.mp3'", "'/audio/master_narration.mp3'")
s = s.replace('"/public/audio/master.mp3"', '"/audio/master_narration.mp3"')
s = s.replace("'/audio/master.mp3'", "'/audio/master_narration.mp3'")
s = s.replace('"/audio/master.mp3"', '"/audio/master_narration.mp3"')

if 'master.mp3' in s or '/public/audio/' in s:
    raise SystemExit('Legacy audio path still present after patch')

p.write_text(s, encoding='utf-8')
print('Dynamic cinematic environment, channel identity, and audio paths verified')
