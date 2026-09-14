from pathlib import Path
import re
import subprocess

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'function dailyImg(id){' not in s:
    raise SystemExit('dailyImg marker not found')

# A later function declaration intentionally overrides the existing Lure
# Pokémon details function without touching the click handlers.
fn = r'''function showLurePokemonTypes(name,image){let title=String(name||'Pokémon'),odds='1/512',pct='0,20 %';let slug=String(title).toLowerCase().trim().replace(/[’']/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');let special={'alolan rattata':'rattata-alola','alolan geodude':'geodude-alola','alolan diglett':'diglett-alola','alolan raichu':'raichu-alola','galarian meowth':'meowth-galar','galarian slowpoke':'slowpoke-galar','galarian slowbro':'slowbro-galar','galarian slowking':'slowking-galar','galarian darumaka':'darumaka-galar','galarian stunfisk':'stunfisk-galar','hisui qwilfish':'qwilfish-hisui','hisui voltorb':'voltorb-hisui','hisui electrode':'electrode-hisui'};slug=special[String(title).toLowerCase().trim()]||slug;fetch('https://pokeapi.co/api/v2/pokemon/'+encodeURIComponent(slug)).then(r=>{if(!r.ok)throw Error('pokemon not found');return r.json()}).then(d=>{let types=(d.types||[]).sort((a,b)=>a.slot-b.slot).map(x=>String(x.type?.name||'')).filter(Boolean).map(x=>({normal:'Normal',fire:'Ild',water:'Vand',electric:'Elektrisk',grass:'Græs',ice:'Is',fighting:'Kamp',poison:'Gift',ground:'Jord',flying:'Flyvende',psychic:'Psykisk',bug:'Insekt',rock:'Sten',ghost:'Spøgelse',dragon:'Drage',dark:'Mørke',steel:'Stål',fairy:'Fe'}[x]||x));open('<h2>🔎 '+E(title)+'</h2><div class=row style="justify-content:center"><div class=img><img src="'+E(image||d.sprites?.front_default||'')+'" alt="'+E(title)+'"></div></div><div class=section>✨ Shiny chance</div><div class=card><div class=name>'+E(odds)+' ('+E(pct)+')</div><div class=small style="margin-top:5px">Standard wild odds. Særlige events kan give boosted shiny odds.</div></div><div class=section>Typer</div><div class=card><div class=name>'+E(types.join(' · ')||'Ukendt type')+'</div></div>')}).catch(()=>open('<h2>🔎 '+E(title)+'</h2><div class=section>✨ Shiny chance</div><div class=card><div class=name>'+E(odds)+' ('+E(pct)+')</div><div class=small>Standard wild odds. Særlige events kan give boosted shiny odds.</div></div><div class=note>Kunne ikke hente typen lige nu. Prøv igen.</div>'))}
'''

marker = 'function dailyImg(id){'
s = s.replace(marker, fn + marker, 1)
blocks = re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>', s, re.I)
for i, js in enumerate(blocks, 1):
    f = Path(f'/tmp/lure-shiny-script-{i}.js')
    f.write_text(js, encoding='utf-8')
    subprocess.run(['node', '--check', str(f)], check=True)
if '✨ Shiny chance' not in s:
    raise SystemExit('Shiny details missing')
p.write_text(s, encoding='utf-8')
