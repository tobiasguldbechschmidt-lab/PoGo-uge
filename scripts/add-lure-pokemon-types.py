from pathlib import Path
import re
import subprocess

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def remove_function(src, name):
    starts = [src.find('async function ' + name + '(){'), src.find('function ' + name + '(){')]
    starts = [x for x in starts if x >= 0]
    if not starts:
        return src
    start = min(starts)
    brace = src.find('{', start)
    depth = 0
    for i in range(brace, len(src)):
        if src[i] == '{': depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0: return src[:start] + src[i+1:]
    raise SystemExit('Could not safely remove ' + name)

helper = r'''function lurePokemonSlug(name){let n=String(name||'').toLowerCase().trim();let m={'alolan rattata':'rattata-alola','alolan geodude':'geodude-alola','alolan diglett':'diglett-alola','alolan raichu':'raichu-alola','galarian meowth':'meowth-galar','galarian slowpoke':'slowpoke-galar','galarian slowbro':'slowbro-galar','galarian slowking':'slowking-galar','galarian darumaka':'darumaka-galar','galarian stunfisk':'stunfisk-galar','hisui qwilfish':'qwilfish-hisui','hisui voltorb':'voltorb-hisui','hisui electrode':'electrode-hisui','gimmighoul':'gimmighoul','gimmighoul (roaming form)':'gimmighoul'};return m[n]||n.replace(/[’']/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}
function lureTypeName(t){let m={normal:'Normal',fire:'Ild',water:'Vand',electric:'Elektrisk',grass:'Græs',ice:'Is',fighting:'Kamp',poison:'Gift',ground:'Jord',flying:'Flyvende',psychic:'Psykisk',bug:'Insekt',rock:'Sten',ghost:'Spøgelse',dragon:'Drage',dark:'Mørke',steel:'Stål',fairy:'Fe'};return m[String(t||'').toLowerCase()]||String(t||'')}
function lureShinyInfo(){return {odds:'1/512',percent:'0,20 %',note:'Standard wild odds'}}
async function showLurePokemonTypes(name,image){let title=String(name||'Pokémon');let shiny=lureShinyInfo();try{let r=await fetch('https://pokeapi.co/api/v2/pokemon/'+encodeURIComponent(lurePokemonSlug(title)));if(!r.ok)throw Error('pokemon not found');let d=await r.json();let types=(d.types||[]).sort((a,b)=>a.slot-b.slot).map(x=>lureTypeName(x.type?.name)).filter(Boolean);open('<h2>🔎 '+E(title)+'</h2><div class=row style="justify-content:center"><div class=img><img src="'+E(image||d.sprites?.front_default||'')+'" alt="'+E(title)+'"></div></div><div class=section>Shiny-chance</div><div class=card><div class=name>✨ '+E(shiny.odds)+' ('+E(shiny.percent)+')</div><div class=small style="margin-top:5px">'+E(shiny.note)+'. Shiny-odds kan være højere under særlige events.</div></div><div class=section>Typer</div><div class=card><div class=name>'+E(types.join(' · ')||'Ukendt type')+'</div><div class=small style="margin-top:5px">Pokémon-typen/typerne er vist for den valgte Pokémon.</div></div>')}catch(e){open('<h2>🔎 '+E(title)+'</h2><div class=section>Shiny-chance</div><div class=card><div class=name>✨ '+E(shiny.odds)+' ('+E(shiny.percent)+')</div><div class=small style="margin-top:5px">'+E(shiny.note)+'. Shiny-odds kan være højere under særlige events.</div></div><div class=note>Kunne ikke hente typen lige nu. Prøv igen.</div>')}}
'''
if 'function lurePokemonSlug(' not in s:
    marker='function dailyImg(id){'
    if marker not in s: raise SystemExit('dailyImg marker not found')
    s=s.replace(marker,helper+marker,1)
else:
    s=remove_function(s,'showLurePokemonTypes')
    s=helper.replace("function lurePokemonSlug(name){let n=String(name||'').toLowerCase().trim();let m={'alolan rattata':'rattata-alola','alolan geodude':'geodude-alola','alolan diglett':'diglett-alola','alolan raichu':'raichu-alola','galarian meowth':'meowth-galar','galarian slowpoke':'slowpoke-galar','galarian slowbro':'slowbro-galar','galarian slowking':'slowking-galar','galarian darumaka':'darumaka-galar','galarian stunfisk':'stunfisk-galar','hisui qwilfish':'qwilfish-hisui','hisui voltorb':'voltorb-hisui','hisui electrode':'electrode-hisui','gimmighoul':'gimmighoul','gimmighoul (roaming form)':'gimmighoul'};return m[n]||n.replace(/[’']/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}\nfunction lureTypeName(t){let m={normal:'Normal',fire:'Ild',water:'Vand',electric:'Elektrisk',grass:'Græs',ice:'Is',fighting:'Kamp',poison:'Gift',ground:'Jord',flying:'Flyvende',psychic:'Psykisk',bug:'Insekt',rock:'Sten',ghost:'Spøgelse',dragon:'Drage',dark:'Mørke',steel:'Stål',fairy:'Fe'};return m[String(t||'').toLowerCase()]||String(t||'')}\n",'')
    marker='function dailyImg(id){'
    s=s.replace(marker,helper+marker,1)

pattern=r"document\.addEventListener\('click',e=>\{let wild=document\.getElementById\('wild-content'\);if\(!wild\)return;let head=wild\.querySelector\('h2'\);if\(!head\|\|head\.textContent\.indexOf\('Lure Module · Spawns'\)<0\)return;let card=e\.target\.closest\('\.card'\);if\(!card\|\|e\.target\.closest\('button'\)\)return;let img=card\.querySelector\('img'\);let nm=card\.querySelector\('\.name'\);if\(!nm\)return;showLurePokemonTypes\(nm\.textContent\.trim\(\),img\?img\.src:''\)\}\);"
s=re.sub(pattern,'',s)
marker="document.addEventListener('click',e=>{let b=e.target.closest('[data-event-url]')"
pos=s.find(marker)
if pos<0: raise SystemExit('event listener marker not found')
listener="document.addEventListener('click',e=>{let mb=document.getElementById('mb');if(!mb||!document.getElementById('modal')?.classList.contains('open'))return;let head=mb.querySelector('h2');if(!head||head.textContent.indexOf('Lure Module · Spawns')<0)return;let card=e.target.closest('.card');if(!card||!mb.contains(card)||e.target.closest('button'))return;let img=card.querySelector('img');let nm=card.querySelector('.name');if(!nm)return;showLurePokemonTypes(nm.textContent.trim(),img?img.src:'')});"
s=s[:pos]+listener+s[pos:]

blocks=re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>',s,re.I)
for i,js in enumerate(blocks,1):
    f=Path(f'/tmp/lure-type-script-{i}.js');f.write_text(js,encoding='utf-8');subprocess.run(['node','--check',str(f)],check=True)
for x in ['function lurePokemonSlug','function lureShinyInfo','function showLurePokemonTypes','Lure Module · Spawns']:
    if x not in s: raise SystemExit('Missing '+x)
p.write_text(s,encoding='utf-8')
