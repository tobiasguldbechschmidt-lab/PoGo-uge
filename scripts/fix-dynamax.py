from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'
s = INDEX.read_text(encoding='utf-8')

new = r'''async function dynamax(){
  let b=$('max');
  try{
    let r=await get('data/maxbattles.json',300000),c=r?.currentList||r?.current||r||{},a=[];
    if(Array.isArray(c))a=c;
    else if(c&&typeof c==='object')Object.entries(c).forEach(([k,v])=>{if(Array.isArray(v))v.forEach(x=>a.push({...x,_tier:k}))});
    if(!a.length)throw 0;
    let seen=new Set();
    a=a.filter(x=>{let n=String(x?.names?.English||x?.name||x?.pokemon?.names?.English||x?.pokemon?.name||'').trim().toLowerCase();if(!n||seen.has(n))return false;seen.add(n);return true});
    const typeDa={NORMAL:'Normal',FIRE:'Ild',WATER:'Vand',ELECTRIC:'Elektrisk',GRASS:'Græs',ICE:'Is',FIGHTING:'Kamp',POISON:'Gift',GROUND:'Jord',FLYING:'Flyvende',PSYCHIC:'Psykisk',BUG:'Insekt',ROCK:'Sten',GHOST:'Spøgelse',DRAGON:'Drage',DARK:'Mørke',STEEL:'Stål',FAIRY:'Fe'};
    const tierInfo={1:['Tier 1','Ca. 1 spiller'],2:['Tier 2','Ca. 1 spiller'],3:['Tier 3','Ca. 2–4 spillere'],4:['Tier 4','Ca. 2–4 spillere'],5:['Tier 5','Ca. 3–4 spillere'],6:['Tier 6 · Gigantamax','Ca. 10–40 spillere']};
    const tierNum=x=>{let z=String(x?.level??x?._tier??'').match(/\d+/);return z?Number(z[0]):0};
    const types=x=>{let t=x?.types||[x?.primaryType?.type,x?.secondaryType?.type].filter(Boolean)||[];if(!Array.isArray(t))t=[t];return t.map(v=>typeof v==='string'?v:(v?.type||v?.name||'')).map(v=>typeDa[String(v).toUpperCase()]||String(v)).filter(Boolean)};
    const shiny=x=>x?.shiny===true||x?.shiny_available===true;
    const img=x=>x?.assets?.image||x?.asset_url||x?.image||'';
    b.innerHTML=a.map(x=>{let n=x?.names?.English||x?.name||x?.pokemon?.names?.English||x?.pokemon?.name||'Dynamax Pokémon',im=img(x),tn=tierNum(x),ti=tierInfo[tn]||['Tier '+(tn||'?'),'Afhænger af boss'],ts=types(x),sh=shiny(x),cp=x?.cpRange||[];return `<div class="card"><div class="row"><div class="img">${im?`<img src="${E(im)}" alt="${E(n)}">`:''}</div><div class="grow"><div class="name">${E(n)}</div><div class="small">${E(ti[0])}</div></div></div><div class="stats"><div class="stat"><b>${E(ts.length?ts.join(' / '):'Ukendt')}</b><span>Type</span></div><div class="stat"><b>${sh?'ca. 1/20 (5 %)':'Ikke mulig'}</b><span>Shiny chance${sh?' · est.':''}</span></div><div class="stat"><b>${E(ti[1])}</b><span>Spillere</span></div></div>${cp.length>=2?`<div class=small style="margin-top:8px">CP ved fangst: ${E(cp[0])}–${E(cp[1])}</div>`:''}${sh?'<div class=small style="margin-top:6px">Shiny-raten for Max Battles er et community-estimat og ikke officielt offentliggjort.</div>':''}</div>`}).join('');up();
  }catch(e){b.innerHTML='<div class=note>Kunne ikke hente Max Battle-data. Prøv ↻ igen.</div>';console.error(e)}
}
'''

start = s.find('async function dynamax(){')
end = s.find('function battleQ', start)
if start < 0 or end < 0 or end <= start:
    raise SystemExit(f'Could not find safe Dynamax boundaries: start={start}, end={end}')
s2 = s[:start] + new + s[end:]
INDEX.write_text(s2, encoding='utf-8')

blocks = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', s2, flags=re.S|re.I)
for i, block in enumerate(blocks, 1):
    q = ROOT / f'.tmp-dynamax-{i}.js'
    q.write_text(block, encoding='utf-8')
    try:
        subprocess.run(['node','--check',str(q)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    finally:
        q.unlink(missing_ok=True)

for needle in ('data/maxbattles.json','ca. 1/20 (5 %)','Spillere'):
    if needle not in s2:
        raise SystemExit(f'Missing Dynamax validation marker: {needle}')

# Workflow trigger marker: keep this patch script in the workflow path set.
