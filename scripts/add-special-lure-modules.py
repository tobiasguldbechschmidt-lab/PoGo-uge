from pathlib import Path
import re
import subprocess

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def replace_function(src,name,replacement):
    starts=[src.find('async function '+name+'(){'),src.find('function '+name+'(){')]
    starts=[x for x in starts if x>=0]
    if not starts: raise SystemExit('Could not find '+name)
    start=min(starts); brace=src.find('{',start); depth=0
    for i in range(brace,len(src)):
        if src[i]=='{': depth+=1
        elif src[i]=='}':
            depth-=1
            if depth==0: return src[:start]+replacement+src[i+1:]
    raise SystemExit('Could not safely replace '+name)

special={
 'Glacial Lure':['Jynx','Eevee','Totodile','Swinub','Snorunt','Mantine','Spheal','Piplup','Snover','Oshawott','Seel','Shellder','Magikarp','Sneasel','Wailmer','Feebas','Clamperl','Finneon','Cryogonal'],
 'Mossy Lure':['Oddish','Bellsprout','Venonat','Tangela','Eevee','Sudowoodo','Hoppip','Yanma','Roselia','Cherubi','Applin','Butterfree','Beedrill','Exeggcute','Scyther','Shuckle','Gulpin','Combee'],
 'Magnetic Lure':['Pikachu','Alolan Geodude','Magnemite','Voltorb','Electrode','Jolteon','Nosepass','Aron','Beldum','Joltik','Alolan Diglett','Onix','Electabuzz','Mareep','Skarmory','Lairon','Electrike','Shieldon'],
 'Rainy Lure':['Psyduck','Spinarak','Chinchou','Surskit','Electrike','Joltik','Tympole','Tynamo','Stunfisk','Froakie'],
 'Golden Lure':['Gimmighoul']
}

def js_array(xs):
    return '['+','.join(repr(x) for x in xs)+']'

cards="""function lureCards(){let h='<div class=section>Lure</div>';h+='<div class=card><div class=row><span style=\"font-size:25px\">🌸</span><div class=grow><div class=name>Lure Module</div><div class=small>Normal Lure Module</div></div></div><div class=grid style=\"margin-top:10px\"><button class=\"btn click\" data-normal-lure-duration=\"1\" type=\"button\">⏱ Varighed</button><button class=\"btn click\" data-normal-lure=\"1\" type=\"button\">🌸 Spawns</button></div></div>';"""
for name in special:
    key=name.lower().replace(' ','-')
    cards+=f"h+='<div class=\"card\"><div class=row><span style=\\\"font-size:25px\\\">🌸</span><div class=grow><div class=name>{name}</div><div class=small>Type-specifikt Lure Module</div></div></div><div class=grid style=\\\"margin-top:10px\\\"><button class=\\\"btn click\\\" data-special-lure-duration=\\\"{key}\\\" type=\\\"button\\\">⏱ Varighed</button><button class=\\\"btn click\\\" data-special-lure=\\\"{key}\\\" type=\\\"button\\\">🌸 Spawns</button></div></div>';"
cards+="return h}\n"

s=replace_function(s,'lureCards',cards)

fn="""function specialLureData(type){return {glacial-lure:{title:'Glacial Lure',types:'Vand/Ice',spawns:%s},mossy-lure:{title:'Mossy Lure',types:'Insekt/Græs/Gift',spawns:%s},magnetic-lure:{title:'Magnetic Lure',types:'Elektrisk/Stål/Sten',spawns:%s},rainy-lure:{title:'Rainy Lure',types:'Vand/Insekt/Elektrisk',spawns:%s},golden-lure:{title:'Golden Lure',types:'Gimmighoul',spawns:%s}}[type]||null}\nfunction showSpecialLureSpawns(type){let d=specialLureData(type);if(!d)return;let h='<h2>🌸 '+E(d.title)+' · Spawns</h2><div class=small>'+E(d.types)+'-relaterede Pokémon</div><div class=section>Spawns</div>';h+=d.spawns.map((name,i)=>'<div class=\"card click\" data-special-lure-p=\"'+i+'\"><div class=row><div class=img><img src=\"'+E(lureImg(name))+'\" alt=\"'+E(name)+'\"></div><div class=grow><div class=name>'+E(name)+'</div><div class=small>✨ Shiny chance: ca. 1/512 (0,20 %)</div></div>›</div></div>').join('');h+='<div class=section>Shiny-chance</div><div class=card><div class=small>Pokémon uden en særskilt offentliggjort rate vises med standard-estimatet ca. 1/512. Events kan ændre shiny-odds.</div></div>';open(h);document.querySelectorAll('[data-special-lure-p]').forEach(x=>x.onclick=()=>{let p=d.spawns[+x.dataset.specialLureP];showLurePokemonTypes(p,lureImg(p))})}\nfunction showSpecialLureDuration(type){let d=specialLureData(type);if(!d)return;open('<h2>🌸 '+E(d.title)+' · Varighed</h2><div class=small>Type-specifikt Lure Module</div><div class=section>Normal varighed</div><div class=card><div class=name>30 minutter</div><div class=small style=\"margin-top:5px\">Et Lure Module varer normalt 30 minutter. Særlige events kan forlænge varigheden.</div></div><div class=section>Sådan virker det</div><div class=card><div class=small>'+E(d.title)+' tiltrækker primært Pokémon fra de relevante typer omkring PokéStoppen. Spawns kan påvirkes af sæsoner og events.</div></div><div class=section>Shiny</div><div class=card><div class=small>Tryk på en Pokémon under Spawns for at se dens shiny chance og typer.</div></div>')}\n"""%(js_array(special['Glacial Lure']),js_array(special['Mossy Lure']),js_array(special['Magnetic Lure']),js_array(special['Rainy Lure']),js_array(special['Golden Lure']))
marker='function dailyImg(id){'
if marker not in s: raise SystemExit('dailyImg marker not found')
s=s.replace(marker,fn+marker,1)

listener="document.addEventListener('click',e=>{let b=e.target.closest('[data-special-lure]');if(b){e.stopPropagation();showSpecialLureSpawns(b.dataset.specialLure)}});document.addEventListener('click',e=>{let b=e.target.closest('[data-special-lure-duration]');if(b){e.stopPropagation();showSpecialLureDuration(b.dataset.specialLureDuration)}});"
if listener not in s: s=s.replace("document.addEventListener('click',e=>{let b=e.target.closest('[data-event-url]')",listener+"document.addEventListener('click',e=>{let b=e.target.closest('[data-event-url]')",1)

blocks=re.findall(r'<script(?:[^>]*)>([\\s\\S]*?)</script>',s,re.I)
for i,js in enumerate(blocks,1):
    f=Path(f'/tmp/special-lure-{i}.js');f.write_text(js,encoding='utf-8');subprocess.run(['node','--check',str(f)],check=True)
for needle in ['Glacial Lure','Mossy Lure','Magnetic Lure','Rainy Lure','Golden Lure','data-special-lure=','data-special-lure-p=','Shiny chance']:
    if needle not in s: raise SystemExit('Missing '+needle)
p.write_text(s,encoding='utf-8')
