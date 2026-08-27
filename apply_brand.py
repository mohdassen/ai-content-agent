from pathlib import Path
p=Path('motion/src/video.tsx');s=p.read_text(encoding='utf-8')

# Wire the approved AI-generated presenter artwork into the actual render.
if "./presenterAsset" not in s:
 s=s.replace("import {TIMELINE} from './generatedTimeline';", "import {TIMELINE} from './generatedTimeline';\nimport {APPROVED_PRESENTER_HERO} from './presenterAsset';")

# Premium navy/cyan/gold palette: no flat green background.
s=s.replace("const C={bg:'#030806',bg2:'#091812',panel:'#10241d',text:'#f7faf8',accent:'#52e39c',accent2:'#d8ffe9',muted:'#91aa9f',line:'#1c4435'};","const C={bg:'#050816',bg2:'#0b1730',panel:'#101c35',text:'#f8fafc',accent:'#34c9ff',accent2:'#f4c95d',muted:'#b2bfd2',line:'#26466e'};")

# Replace the generated green atmosphere with the approved presenter/studio image.
scene_marker="const SceneShell:React.FC<{duration:number;children:React.ReactNode}>="
if scene_marker in s:
 start=s.index(scene_marker)
 end=s.index("const Caption:",start)
 shell="""const ApprovedBackdrop=()=>{const f=useCurrentFrame();const zoom=1.16+Math.sin(f/55)*.035;const x=Math.sin(f/43)*18;const y=Math.cos(f/61)*12;return <><AbsoluteFill style={{background:'#050816'}}/><img src={APPROVED_PRESENTER_HERO} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',objectPosition:'center',transform:`translate3d(${x}px,${y}px,0) scale(${zoom})`,filter:'saturate(1.08) contrast(1.04) brightness(.78)'}}/><AbsoluteFill style={{background:'linear-gradient(180deg,rgba(3,7,18,.20) 0%,rgba(3,7,18,.30) 48%,rgba(3,7,18,.78) 100%)'}}/><AbsoluteFill style={{boxShadow:'inset 0 0 180px rgba(0,0,0,.55)'}}/></>};
const SceneShell:React.FC<{duration:number;children:React.ReactNode}>=({duration,children})=>{const f=useCurrentFrame();const enter=interpolate(f,[0,10],[0,1],clamp),exit=interpolate(f,[Math.max(0,duration-10),duration],[1,0],clamp);const pan=interpolate(f,[0,duration],[-14,14],clamp);return <AbsoluteFill style={{opacity:Math.min(enter,exit),transform:`translateX(${pan}px) scale(1.01)`,overflow:'hidden',color:C.text}}><ApprovedBackdrop/><Brand/>{children}</AbsoluteFill>};
"""
 s=s[:start]+shell+s[end:]

# Approved brand mark.
old="const Brand=()=> <div style={{position:'absolute',top:62,right:62,fontFamily:font,color:C.accent,fontSize:24,fontWeight:900,direction:'rtl'}}>خلف الرقم <span style={{color:C.muted,fontSize:18}}>• BEHIND THE NUMBER</span></div>;"
new="const Brand=()=> <div style={{position:'absolute',top:42,right:42,zIndex:50,filter:'drop-shadow(0 8px 18px rgba(0,0,0,.55))'}}><img src={staticFile('brand-logo.svg')} style={{width:118,height:118,objectFit:'contain'}} /></div>;"
if old in s:s=s.replace(old,new)

# Make captions readable over photographic scenes.
s=s.replace("color:C.text,direction:'rtl',opacity:p,transform:`translateY(${(1-p)*28}px)`","color:C.text,direction:'rtl',opacity:p,transform:`translateY(${(1-p)*28}px)`,background:'rgba(3,8,20,.58)',backdropFilter:'blur(8px)',border:'1px solid rgba(52,201,255,.20)',borderRadius:28,padding:'18px 26px',textShadow:'0 3px 18px rgba(0,0,0,.9)'")

# Remove legacy hard-coded greens inside foreground graphics.
for a,b in {'#123b2b':'#11254b','#17623f':'#167ca8','#142c23':'#16233a','#07110d':'#08101f','#315347':'#34577d','rgba(82,227,156,.06)':'rgba(52,201,255,.07)','rgba(82,227,156,.35)':'rgba(52,201,255,.28)'}.items():
 s=s.replace(a,b)

# Stable narration path.
for olda in ("staticFile('public/audio/master.mp3')","staticFile('/public/audio/master.mp3')","staticFile('audio/master.mp3')","staticFile('/audio/master.mp3')"):
 s=s.replace(olda,"staticFile('audio/master_narration.mp3')")
if 'master.mp3' in s or '/public/audio/' in s: raise SystemExit('Legacy audio path still present')
if 'APPROVED_PRESENTER_HERO' not in s: raise SystemExit('Approved presenter asset was not wired into video.tsx')
p.write_text(s,encoding='utf-8')
print('Approved presenter artwork is now part of the actual Remotion render')
