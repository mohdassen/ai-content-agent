from pathlib import Path
p=Path('motion/src/video.tsx');s=p.read_text(encoding='utf-8')
# Never synthesize the approved presenter from CSS primitives. The previous
# placeholder looked like a toy avatar and did not match the approved concept.
if 'const Presenter=' in s:
 a=s.index('const Presenter='); b=s.find('const Brand=()=>',a)
 if b!=-1:s=s[:a]+s[b:]
s=s.replace("<Presenter side={f%240<120?'left':'right'}/>","")
# Keep the documentary environment and channel identity until a real transparent
# presenter asset matching the approved concept is available in public/character.
old="const Brand=()=> <div style={{position:'absolute',top:62,right:62,fontFamily:font,color:C.accent,fontSize:24,fontWeight:900,direction:'rtl'}}>خلف الرقم <span style={{color:C.muted,fontSize:18}}>• BEHIND THE NUMBER</span></div>;"
new="const Brand=()=> <div style={{position:'absolute',top:48,right:48,zIndex:50,filter:'drop-shadow(0 8px 18px rgba(0,0,0,.55))'}}><img src={staticFile('brand-logo.svg')} style={{width:126,height:126,objectFit:'contain'}} /></div>;"
if old in s:s=s.replace(old,new)
for olda in ("staticFile('public/audio/master.mp3')","staticFile('/public/audio/master.mp3')","staticFile('audio/master.mp3')","staticFile('/audio/master.mp3')"):s=s.replace(olda,"staticFile('audio/master_narration.mp3')")
if 'master.mp3' in s or '/public/audio/' in s:raise SystemExit('Legacy audio path still present')
p.write_text(s,encoding='utf-8');print('Toy presenter removed; approved-character-only policy enforced')
