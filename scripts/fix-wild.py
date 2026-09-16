from pathlib import Path
import re

path = Path('index.html')
s = path.read_text(encoding='utf-8')
start = s.find('async function wild(){')
end = s.find('\n\nasync function eggs(){', start)
if start < 0 or end < 0:
    raise SystemExit('Could not find wild() boundaries')

new = r'''async function wild(){
  const b=$('wild');
  try{
    const a=await ev(), n=N(), m=new Map(), inc=[], lure=[];
    const active=a.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n));
    active.forEach(e=>{
      const title=e.title||'Event';
      const url=e.article_url||e.url||'';
      const spawns=Array.isArray(e.details?.spawns)?e.details.spawns:(Array.isArray(e.spawns)?e.spawns:[]);
      spawns.forEach(p=>{
        if(!p||typeof p!=='object')return;
        const name=p.name||p.pokemon_name||p.species;
        if(!name)return;
        const key=String(name).trim().toLowerCase();
        if(!m.has(key))m.set(key,{...p,name:String(name).trim(),events:[]});
        const q=m.get(key);
        if(!q.events.some(v=>v.title===title))q.events.push({title,url});
      });
      const bonuses=Array.isArray(e.details?.bonuses)?e.details.bonuses:[];
      bonuses.forEach(v=>{
        const text=typeof v==='string'?v:v?.text||v?.name||'';
        if(/incense/i.test(text))inc.push([title,text,url]);
        if(/lure/i.test(text))lure.push([title,text,url]);
      });
    });
    const a1=[...m.values()];
    const unique=x=>x.filter((v,i)=>x.findIndex(y=>y[0]===v[0]&&y[1]===v[1])===i);
    const incU=unique(inc), lureU=unique(lure);
    const eventCards=()=>a1.length?'<div class=section>Event-Pokémon i det fri</div>'+a1.map((p,i)=>`<div class="card click" data-w="${i}"><div class=row><div class=img>${p.asset_url?`<img src="${E(p.asset_url)}" alt="${E(p.name)}" loading="lazy">`:'🌿'}</div><div class=grow><div class=name>${E(p.name)}</div><div class=small>${E(p.events.map(v=>v.title).join(' · ')||'Event-spawn')}</div></div>›</div></div>`).join(''):'<div class=note>Ingen aktive event-spawns registreret lige nu.</div>';
    const bonusCards=(ls,label)=>ls.length?'<div class=section>'+label+'</div>'+ls.map(x=>`<div class="card"><b>${E(x[0])}</b><div class=small>• ${E(x[1])}</div>${x[2]?`<button class="btn" type="button" data-event-url="${E(x[2])}" style="margin-top:7px;width:100%;cursor:pointer">Åbn eventet ↗</button>`:''}</div>`).join(''):'<div class=note>Ingen aktive '+label.toLowerCase()+' angivet.</div>';
    const render=tab=>{
      b.querySelectorAll('[data-wtab]').forEach(x=>x.classList.toggle('active',x.dataset.wtab===tab));
      const c=b.querySelector('#wild-content');
      if(tab==='event')c.innerHTML=eventCards();
      else if(tab==='incense')c.innerHTML=dailyIncenseCards()+bonusCards(incU,'Aktive Incense-bonusser');
      else c.innerHTML=lureCards()+bonusCards(lureU,'Aktive Lure-bonusser');
      b.querySelectorAll('[data-daily]').forEach(x=>x.onclick=()=>showDailyIncense());
      b.querySelectorAll('[data-w]').forEach(x=>x.onclick=async()=>{
        const p=a1[Number(x.dataset.w)];
        if(!p)return;
        const q=await poke(pid(p)), t=[];
        const addT=v=>{
          if(v==null)return;
          if(Array.isArray(v)){v.forEach(addT);return;}
          if(typeof v==='object'){addT(v.name??v.type??v.value??v.typeName);return;}
          const z=typeof v==='number'?TYPE_NAMES[v]:String(v).trim();
          if(z&&!t.includes(z))t.push(z);
        };
        [q?.types,q?.type,q?.type1,q?.type2,q?.data?.types,q?.data?.type,q?.data?.type1,q?.data?.type2,p?.types,p?.type,p?.type1,p?.type2].forEach(addT);
        const events=p.events||[];
        open(`<h2>${E(p.name)}</h2><div class=section>Type</div><div class=card>${t.map(v=>E(v)).join(' · ')||'Ikke oplyst'}</div><div class=section>Shiny-chance</div><div class=card>✨ ${E(shiny(p,q,'wild'))}</div><div class=section>Hvorfor spawner den?</div>${events.length?events.map(v=>`<div class="card ${v.url?'click':''}" ${v.url?`data-event-url="${E(v.url)}"`:''}><div class=name>${E(v.title)}</div>${v.url?'<div class=small style="margin-top:5px">Åbn eventet ↗</div>':'<div class=small style="margin-top:5px">Event-link ikke oplyst.</div>'}</div>`).join(''):'<div class=card><div class=small>Event ikke oplyst.</div></div>'}`);
      });
    };
    b.innerHTML='<div class="wild-tabs"><button class="wild-tab active" data-wtab="event">Event-spawns</button><button class="wild-tab" data-wtab="incense">Incense</button><button class="wild-tab" data-wtab="lure">Lure</button></div><div id="wild-content"></div>';
    b.querySelectorAll('[data-wtab]').forEach(x=>x.onclick=()=>render(x.dataset.wtab));
    render('event');
    up();
  }catch(e){
    console.error('In The Wild failed',e);
    b.innerHTML='<div class=note>Kunne ikke hente wild-data. Tryk ↻ og prøv igen.</div>';
  }
}'''

path.write_text(s[:start]+new+s[end:],encoding='utf-8')
print('patched')
