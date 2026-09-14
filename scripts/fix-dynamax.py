from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'
s = INDEX.read_text(encoding='utf-8')

new = r'''async function dynamax(){
try{
  let r=await get(MAX,60000),raw=r?.currentList||r?.current||r?.data||r||[],a=Array.isArray(raw)?raw:Object.values(raw||{}).flat();
  if(!Array.isArray(a)||!a.length)throw 0;
  let clean=a.map(x=>{
    let n=x.names?.English||x.name||x.pokemon_name||x.species?.name||'Dynamax Pokémon';
    let tier=Number(x.tier||x.level||x.stars||x.starLevel||x.raidTier)||1;
    let types=maxTypes(x);
    let im=x.assets?.image||x.asset_url||x.image||x.image_url||'';
    let shiny=x.shiny_available!==false;
    let gmax=String(x.form||x.name||'').toLowerCase().includes('gigantamax')||String(x.type||'').toLowerCase().includes('gigantamax');
    return {n,tier:Math.max(1,Math.min(6,tier)),types,im,shiny,gmax};
  });
  clean.sort((x,y)=>x.tier-y.tier||x.n.localeCompare(y.n));
  let h=`<div class=note>Aktuelle Max Battle-bosser fra det live feed, opdateres automatisk. Shiny-raten er et community-estimat, da Niantic ikke offentliggør en officiel Max Battle-rate.</div>`;
  let groups={};
  clean.forEach(x=>(groups[x.tier]??=[]).push(x));
  Object.keys(groups).sort((a,b)=>a-b).forEach(t=>{
    h+=`<div class=section>Tier ${E(t)}</div>`;
    groups[t].forEach(x=>{
      let players=maxPlayers(x.tier,x.gmax),type=x.types.length?x.types.join(' · '):'Type ikke oplyst';
      h+=`<div class="card"><div class=row>${x.im?`<div class=img><img src="${E(x.im)}" alt=""></div>`:''}<div class=grow><div class=name>${E(x.n)}</div><div class=small>${E(type)}</div></div></div><div class=stats><div class=stat><b>${E(type)}</b><span>Type</span></div><div class=stat><b>${x.shiny?'ca. 1/128':'Ikke shiny-eligible'}</b><span>Shiny chance</span></div><div class=stat><b>${E(players)}</b><span>Ca. spillere</span></div></div><div class=note style="margin-bottom:0">Tier ${E(x.tier)} · ${x.gmax?'Gigantamax':'Dynamax'}${x.shiny?' · Shiny mulig':''}</div></div>`;
    });
  });
  $('max').innerHTML=h;up();
}catch(e){$('max').innerHTML='<div class=note>Max Battle-feed kunne ikke hentes. Tryk ↻ igen.</div>'}
}
function maxTypes(x){
  let v=x.types||x.type||x.pokemon_types||x.data?.types||x.data?.type||[];
  if(!Array.isArray(v))v=[v];
  const ids={1:'Normal',2:'Kamp',3:'Flyvende',4:'Gift',5:'Jord',6:'Sten',7:'Insekt',8:'Spøgelse',9:'Stål',10:'Ild',11:'Vand',12:'Græs',13:'Elektrisk',14:'Psykisk',15:'Is',16:'Drage',17:'Mørke',18:'Fe'};
  return v.map(t=>typeof t==='object'?(t.name||t.type||t.value||t.typeName||''):t).map(t=>ids[Number(t)]||String(t||'')).map(t=>t.trim()).filter(Boolean).map(t=>({normal:'Normal',fighting:'Kamp',flying:'Flyvende',poison:'Gift',ground:'Jord',rock:'Sten',bug:'Insekt',ghost:'Spøgelse',steel:'Stål',fire:'Ild',water:'Vand',grass:'Græs',electric:'Elektrisk',psychic:'Psykisk',ice:'Is',dragon:'Drage',dark:'Mørke',fairy:'Fe'}[t.toLowerCase()]||t)).filter((t,i,a)=>a.indexOf(t)===i);
}
function maxPlayers(t,g){if(g||t>=5)return '4–8+';if(t>=3)return '2–4';if(t===2)return '1–2';return '1 (solo)'}
'''

pat = re.compile(r'async function dynamax\(\)\{.*?\}\nfunction battleQ', re.S)
s2, n = pat.subn(new + '\nfunction battleQ', s, count=1)
if n != 1:
    raise SystemExit(f'Expected exactly one dynamax function replacement, got {n}')
INDEX.write_text(s2, encoding='utf-8')

# Validate every inline JavaScript block.
blocks = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', s2, flags=re.S|re.I)
for i, block in enumerate(blocks, 1):
    p = ROOT / f'.tmp-dynamax-{i}.js'
    p.write_text(block, encoding='utf-8')
    try:
        subprocess.run(['node','--check',str(p)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    finally:
        p.unlink(missing_ok=True)

if 'async function dynamax()' not in s2 or 'maxPlayers' not in s2 or 'ca. 1/128' not in s2:
    raise SystemExit('Dynamax markup/function validation failed')
