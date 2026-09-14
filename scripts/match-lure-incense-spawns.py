from pathlib import Path
import re
import subprocess

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def replace_function(src, name, replacement):
    candidates = [src.find('async function ' + name + '(){'), src.find('function ' + name + '(){')]
    candidates = [x for x in candidates if x >= 0]
    if not candidates:
        raise SystemExit(f'Could not find {name}')
    start = min(candidates)
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

replacement = r'''async function showNormalLureSpawns(){
  $('x').onclick=()=>$('modal').classList.remove('open');
  try{
    let a=await ev(),n=N(),active=a.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n));
    active.sort((x,y)=>(y.start||0)-(x.start||0));
    let hasSpawns=e=>{
      let d=e.details||{};
      if(Array.isArray(e.lure_spawns)&&e.lure_spawns.length)return true;
      if(Object.keys(d).some(k=>/lure/i.test(k)&&Array.isArray(d[k])&&d[k].length))return true;
      if(Array.isArray(d.spawns)&&d.spawns.length)return true;
      return false;
    };
    let e=active.find(e=>hasSpawns(e)&&/lure/i.test(JSON.stringify(e)))||active.find(hasSpawns);
    if(!e){open('<h2>🌸 Lure Module · Spawns</h2><div class=note>Der er ingen registrerede Lure-spawns lige nu.</div>');return}
    let d=e.details||{},vals=[];
    Object.keys(d).forEach(k=>{if(/lure/i.test(k)&&Array.isArray(d[k]))vals.push(...d[k])});
    if(!vals.length&&Array.isArray(e.lure_spawns))vals=e.lure_spawns;
    if(!vals.length&&Array.isArray(d.spawns))vals=d.spawns;
    let list=[];
    vals.forEach(v=>{
      let p=typeof v==='string'?{name:v}:v||{};
      let name=p.name||p.pokemon||p.species||p.pokemon_name;
      if(name){p={...p,name:String(name)};if(!list.some(x=>x.name===p.name))list.push(p)}
    });
    if(!list.length){open(`<h2>🌸 Lure Module · Spawns</h2><div class=small>${E(e.title)}</div><div class=note>Eventet har ingen læsbare Pokémon-spawns endnu.</div>`);return}
    open(`<h2>🌸 Lure Module · Spawns</h2><div class=small>${E(e.title)}</div><div class=section>Spawns</div>${list.map((p,i)=>`<div class="card click" data-lure-p="${i}"><div class=row><div class=img>${p.asset_url?`<img src="${E(p.asset_url)}" alt="${E(p.name)}" loading="lazy">`:lureImg(p.name)?`<img src="${E(lureImg(p.name))}" alt="${E(p.name)}" loading="lazy">`:'🌸'}</div><div class=grow><div class=name>${E(p.name)}</div><div class=small>${p.shiny_available===true?'✨ Shiny mulig':'Shiny ikke oplyst'}</div></div>›</div></div>`).join('')}`);
    document.querySelectorAll('[data-lure-p]').forEach(x=>x.onclick=()=>{let p=list[+x.dataset.lureP];showLurePokemonTypes(p.name,p.asset_url||lureImg(p.name))});
  }catch(e){open('<h2>🌸 Lure Module · Spawns</h2><div class=note>Kunne ikke hente Lure-spawns. Tryk ↻ igen.</div>')}
}'''

s = replace_function(s, 'showNormalLureSpawns', replacement)
blocks = re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>', s, re.I)
for i, js in enumerate(blocks, 1):
    f = Path(f'/tmp/lure-incense-script-{i}.js')
    f.write_text(js, encoding='utf-8')
    subprocess.run(['node', '--check', str(f)], check=True)
for needle in ['data-lure-p=', 'Lure Module · Spawns', 'showLurePokemonTypes']:
    if needle not in s:
        raise SystemExit('Missing ' + needle)
p.write_text(s, encoding='utf-8')
