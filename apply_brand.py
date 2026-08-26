from pathlib import Path

p = Path('motion/src/video.tsx')
s = p.read_text(encoding='utf-8')
old = "const Brand=()=> <div style={{position:'absolute',top:62,right:62,fontFamily:font,color:C.accent,fontSize:24,fontWeight:900,direction:'rtl'}}>خلف الرقم <span style={{color:C.muted,fontSize:18}}>• BEHIND THE NUMBER</span></div>;"
new = "const Brand=()=> <div style={{position:'absolute',top:48,right:48,zIndex:50,filter:'drop-shadow(0 8px 18px rgba(0,0,0,.55))'}}><img src={staticFile('brand-logo.svg')} style={{width:126,height:126,objectFit:'contain'}} /></div>;"
if old in s:
    s = s.replace(old, new)
elif "staticFile('brand-logo.svg')" not in s:
    raise SystemExit('Brand marker not found; refusing silent patch')

# Push the visual language away from slide-deck motion: stronger camera drift,
# softer scene overlaps, animated captions, and a persistent cinematic vignette.
s = s.replace("const pan=interpolate(f,[0,duration],[-8,8],clamp);", "const pan=interpolate(f,[0,duration],[-22,22],clamp);const zoom=interpolate(f,[0,duration],[1.045,1.085],clamp);")
s = s.replace("transform:`translateX(${pan}px) scale(1.025)`", "transform:`translate3d(${pan}px,${Math.sin(f/17)*5}px,0) scale(${zoom})`")
s = s.replace("<Atmosphere/><Brand/>{children}</AbsoluteFill>", "<Atmosphere/><AbsoluteFill style={{pointerEvents:'none',boxShadow:'inset 0 0 180px rgba(0,0,0,.72)',zIndex:40}}/><Brand/>{children}</AbsoluteFill>")
s = s.replace("transform:`translateY(${(1-p)*28}px)`", "transform:`translateY(${(1-p)*34}px) scale(${.96+p*.04})`,textShadow:'0 5px 28px rgba(0,0,0,.8)'")

end_marker = "<div style={{fontSize:30,color:C.accent,fontWeight:950,marginBottom:50}}>خلف الرقم</div>"
end_logo = "<img src={staticFile('brand-logo.svg')} style={{width:250,height:250,objectFit:'contain',margin:'0 auto 24px',filter:'drop-shadow(0 12px 35px rgba(212,175,55,.28))'}}/><div style={{fontSize:30,color:'#d4af37',fontWeight:950,marginBottom:35}}>خلف الرقم</div>"
if end_marker in s:
    s = s.replace(end_marker, end_logo)

# prepare_motion.py always generates motion/public/audio/master_narration.mp3.
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
print('Channel identity, cinematic motion treatment, and audio paths verified')
