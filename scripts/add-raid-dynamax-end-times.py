from pathlib import Path

# Adds the end-time overlay to the existing Raid and Dynamax cards without replacing menu/UI code.
root=Path(__file__).resolve().parents[1]
p=root/'index.html'
s=p.read_text(encoding='utf-8')
marker='</script>'
if s.count(marker)!=1:
    raise SystemExit(f'Expected one closing script tag, got {s.count(marker)}')

inject=r'''\n/* Raid / Max Battle rotation end times */
(function(){
  const ROTATION_ENDS={
    raid:{
      'Mega Beedrill':'2026-09-15T22:00:00','Mega Houndoom':'2026-09-15T22:00:00','Zacian - Hero':'2026-09-15T22:00:00','Hero Zacian':'2026-09-15T22:00:00','Shadow Thundurus':'2026-10-06T22:00:00','Mega Venusaur':'2026-09-22T22:00:00','Zamazenta - Hero':'2026-09-22T22:00:00','Hero Zamazenta':'2026-09-22T22:00:00','Mega Malamar':'2026-09-29T22:00:00','Buzzwole':'2026-09-29T22:00:00','Pheromosa':'2026-09-29T22:00:00','Xurkitree':'2026-09-29T22:00:00','Mega Victreebel':'2026-10-06T22:00:00','Xerneas':'2026-10-06T22:00:00'},
    max:{'Rhyhorn':'2026-09-20T21:00:00','Dynamax Rhyhorn':'2026-09-20T21:00:00','Articuno':'2026-09-27T21:00:00','Dynamax Articuno':'2026-09-27T21:00:00','Zapdos':'2026-09-27T21:00:00','Dynamax Zapdos':'2026-09-27T21:00:00','Moltres':'2026-09-27T21:00:00','Dynamax Moltres':'2026-09-27T21:00:00','Sobble':'2026-10-04T21:00:00','Dynamax Sobble':'2026-10-04T21:00:00'}
  };
  const normalize=n=>String(n||'').replace(/^Dynamax\s+/i,'').replace(/^Shadow\s+/i,'').replace(/\s+\(Hero of Many Battles\)$/i,'').trim();
  const fmt=v=>new Date(v).toLocaleString('da-DK',{day:'numeric',month:'long',hour:'2-digit',minute:'2-digit'});
  const endFor=(kind,name)=>ROTATION_ENDS[kind][name]||ROTATION_ENDS[kind][normalize(name)]||null;
  function attach(root,kind){root.querySelectorAll('.card').forEach(card=>{if(card.dataset.endAttached)return;const name=card.querySelector('.name')?.textContent?.trim();if(!name)return;const end=endFor(kind,name);card.dataset.endAttached='1';const line=document.createElement('div');line.className='small';line.style.marginTop='5px';line.textContent=end?'⏳ Slutter '+fmt(end):'⏳ Slutdato ikke offentliggjort';card.appendChild(line)})}
  function run(){const raids=document.getElementById('raids'),max=document.getElementById('max');if(raids)attach(raids,'raid');if(max)attach(max,'max')}
  const obs=new MutationObserver(run);document.addEventListener('DOMContentLoaded',()=>{const raids=document.getElementById('raids'),max=document.getElementById('max');if(raids)obs.observe(raids,{childList:true,subtree:true});if(max)obs.observe(max,{childList:true,subtree:true});run()});
})();
'''
s=s.replace(marker,inject+marker,1)
p.write_text(s,encoding='utf-8')
print('Added raid and Dynamax rotation end-time display')
