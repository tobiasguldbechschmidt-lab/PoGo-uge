from pathlib import Path
import re
import subprocess

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def replace_function(src, name, replacement):
    start = src.find('async function ' + name + '(){')
    if start < 0:
        start = src.find('function ' + name + '(){')
    if start < 0:
        raise SystemExit('Could not find ' + name)
    brace = src.find('{', start)
    depth = 0
    for i in range(brace, len(src)):
        if src[i] == '{':
            depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0:
                return src[:start] + replacement + src[i + 1:]
    raise SystemExit('Could not safely replace ' + name)

replacement = r'''async function showLurePokemonTypes(name,image){let title=String(name||'Pokémon');let shinyOdds='1/512';let shinyPercent='0,20 %';try{let r=await fetch('https://pokeapi.co/api/v2/pokemon/'+encodeURIComponent(lurePokemonSlug(title)));if(!r.ok)throw Error('pokemon not found');let d=await r.json();let types=(d.types||[]).sort((a,b)=>a.slot-b.slot).map(x=>lureTypeName(x.type?.name)).filter(Boolean);open('<h2>🔎 '+E(title)+'</h2><div class=row style="justify-content:center"><div class=img><img src="'+E(image||d.sprites?.front_default||'')+'" alt="'+E(title)+'"></div></div><div class=section>✨ Shiny chance</div><div class=card><div class=name>'+E(shinyOdds)+' ('+E(shinyPercent)+')</div><div class=small style="margin-top:5px">Standard wild odds. Eventer kan give boosted shiny odds.</div></div><div class=section>Typer</div><div class=card><div class=name>'+E(types.join(' · ')||'Ukendt type')+'</div><div class=small style="margin-top:5px">Pokémon-typen/typerne er vist for den valgte Pokémon.</div></div>')}catch(e){open('<h2>🔎 '+E(title)+'</h2><div class=section>✨ Shiny chance</div><div class=card><div class=name>'+E(shinyOdds)+' ('+E(shinyPercent)+')</div><div class=small style="margin-top:5px">Standard wild odds. Eventer kan give boosted shiny odds.</div></div><div class=note>Kunne ikke hente typen lige nu. Prøv igen.</div>')}}'''

s = replace_function(s, 'showLurePokemonTypes', replacement)

blocks = re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>', s, re.I)
for i, js in enumerate(blocks, 1):
    f = Path(f'/tmp/lure-type-script-{i}.js')
    f.write_text(js, encoding='utf-8')
    subprocess.run(['node', '--check', str(f)], check=True)

for x in ['function lurePokemonSlug', 'function showLurePokemonTypes', 'Lure Module · Spawns', '✨ Shiny chance']:
    if x not in s:
        raise SystemExit('Missing ' + x)

p.write_text(s, encoding='utf-8')
