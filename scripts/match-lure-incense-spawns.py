from pathlib import Path
import re
import subprocess

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def replace_function(src, name, replacement):
    starts = [src.find('async function ' + name + '(){'), src.find('function ' + name + '(){')]
    starts = [x for x in starts if x >= 0]
    if not starts:
        raise SystemExit(f'Could not find {name}')
    start = min(starts)
    brace = src.find('{', start)
    depth = 0
    for i in range(brace, len(src)):
        if src[i] == '{':
            depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0:
                return src[:start] + replacement + src[i + 1:]
    raise SystemExit(f'Could not safely replace {name}')

replacement = r'''async function showNormalLureSpawns(){try{let a=await ev(),n=N(),active=a.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n)),items=[];active.forEach(e=>{let raw=JSON.stringify(e);if(!/lure module|lure modules|regular lure|active regular lure/i.test(raw))return;let found=[],d=e.details||{};Object.keys(d).forEach(k=>{let v=d[k];if(/lure/i.test(k)&&Array.isArray(v))found.push(...v)});[e.lure_spawns,e.lureSpawns,e.spawns,d.lure_spawns,d.lureSpawns,d.spawns].filter(Array.isArray).forEach(v=>found.push(...v));found.forEach(v=>{let name=typeof v==='string'?v:String(v?.name||v?.pokemon||'').trim();if(name)items.push({name,event:e,raw:v})})});let seen=new Set();items=items.filter(x=>{let k=x.name.toLowerCase();if(seen.has(k))return false;seen.add(k);return true});let h='<h2>🌸 Lure Module · Spawns</h2><div class=small>Pokémon fra det aktuelle Lure-event</div><div class=section>Spawns</div>';if(items.length){h+=items.map(x=>'<div class="card click" role="button" tabindex="0"><div class=row><div class=img><img src="'+E(lureImg(x.name))+'" alt="'+E(x.name)+'"></div><div class=grow><div class=name>'+E(x.name)+'</div><div class=small>'+E(x.event.title||'Aktivt event')+'</div><div class=small style="margin-top:5px">'+E(lureShinyText(x.raw,x.event))+'</div></div><span style="font-size:22px">›</span></div>'+(x.event.article_url||x.event.url?'<button class="btn" type="button" data-lure-event-url="'+E(x.event.article_url||x.event.url)+'" style="width:100%;margin-top:8px;cursor:pointer">Åbn eventet ↗</button>':'')+'</div>').join('')}else{let baseline=['Bulbasaur','Charmander','Squirtle','Pikachu','Eevee','Rattata','Pidgey','Zubat','Spearow','Magikarp','Abra','Machop','Cubone','Snorlax','Passimian'];h+='<div class=small style="margin-bottom:8px">Normal Lure har ingen permanent fast artsliste. Når der ikke er et Lure-specifikt event, følger den den almindelige vilde spawn-pool. Her vises derfor en standardreference — ikke en garanteret lokal encounter-liste.</div>'+baseline.map(name=>'<div class="card click" role="button" tabindex="0"><div class=row><div class=img><img src="'+E(lureImg(name))+'" alt="'+E(name)+'"></div><div class=grow><div class=name>'+E(name)+'</div><div class=small>'+E(lureShinyText(name,''))+'</div></div><span style="font-size:22px">›</span></div></div>').join('')}h+='<div class=section>Shiny-chance</div><div class=card><div class=small>For Pokémon uden en specifik event-rate vises et standard-estimat på ca. 1/512. Hvis et event udtrykkeligt angiver en øget shiny-chance, markeres den som event-forøget. Den præcise rate er ikke altid offentliggjort af Niantic.</div></div>';open(h)}catch(e){open('<h2>🌸 Lure Module · Spawns</h2><div class=note>Kunne ikke hente Lure-spawns. Tryk ↻ igen.</div>')}}'''

s = replace_function(s, 'showNormalLureSpawns', replacement)
blocks = re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>', s, re.I)
for i, js in enumerate(blocks, 1):
    f = Path(f'/tmp/lure-incense-script-{i}.js')
    f.write_text(js, encoding='utf-8')
    subprocess.run(['node', '--check', str(f)], check=True)
for needle in ['<div class="card click" role="button"', 'Lure Module · Spawns', 'showLurePokemonTypes']:
    if needle not in s:
        raise SystemExit('Missing ' + needle)
p.write_text(s, encoding='utf-8')
