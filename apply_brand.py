from pathlib import Path

p = Path('motion/src/video.tsx')
s = p.read_text(encoding='utf-8')
old = "const Brand=()=> <div style={{position:'absolute',top:62,right:62,fontFamily:font,color:C.accent,fontSize:24,fontWeight:900,direction:'rtl'}}>خلف الرقم <span style={{color:C.muted,fontSize:18}}>• BEHIND THE NUMBER</span></div>;"
new = "const Brand=()=> <div style={{position:'absolute',top:48,right:48,zIndex:50,filter:'drop-shadow(0 8px 18px rgba(0,0,0,.55))'}}><img src={staticFile('brand-logo.svg')} style={{width:126,height:126,objectFit:'contain'}} /></div>;"
if old in s:
    s = s.replace(old, new)
elif "staticFile('brand-logo.svg')" not in s:
    raise SystemExit('Brand marker not found; refusing silent patch')

end_marker = "<div style={{fontSize:30,color:C.accent,fontWeight:950,marginBottom:50}}>خلف الرقم</div>"
end_logo = "<img src={staticFile('brand-logo.svg')} style={{width:250,height:250,objectFit:'contain',margin:'0 auto 24px',filter:'drop-shadow(0 12px 35px rgba(212,175,55,.28))'}}/><div style={{fontSize:30,color:'#d4af37',fontWeight:950,marginBottom:35}}>خلف الرقم</div>"
if end_marker in s:
    s = s.replace(end_marker, end_logo)

# Remotion staticFile() paths are relative to the public directory. A leading
# "public/" makes the renderer request /public/audio/... and causes a 404.
s = s.replace("staticFile('public/audio/master.mp3')", "staticFile('audio/master.mp3')")
s = s.replace('staticFile("public/audio/master.mp3")', 'staticFile("audio/master.mp3")')

p.write_text(s, encoding='utf-8')
print('Approved brand logo applied; Remotion static asset paths verified')
