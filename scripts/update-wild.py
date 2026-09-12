from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

css = '<style id="wild-tabs-css">.wild-tabs{display:flex;gap:8px;margin:0 0 12px}.wild-tab{flex:1;padding:10px 8px;border:1px solid var(--l);border-radius:12px;background:var(--c);color:var(--m);font-weight:800}.wild-tab.active{background:var(--y);color:#111}</style>'
if 'id="wild-tabs-css"' not in s:
    s = s.replace('</head>', css + '</head>', 1)

new_wild = r'''async function wild(){let b=$('wild');try{let a=await ev(),n=N(),m=new Map(),inc=[],lure=[];a.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n)).forEach(e=>{let title=e.title||'Event';(e.details?.spawns||e.spawns||[]).forEach(p=>{let k=String(p.name||p.id||p.dex||'');if(!k)return;if(!m.has(k))m.set(k,{...p,name:p.name||'Pokémon',events:[]});let q=m.get(k);if(!q.events.some(v=>v===title))q.events.push(title)});(e.details?.bonuses||[]).forEach(v=>{let t=typeof v==='string'?v:v.text||v.name||'';if(/incense/i.test(t))inc.push([title,t]);if(/lure/i.test(t))lure.push([title,t])})});let a1=[...m.values()];let unique=x=>x.filter((v,i)=>x.findIndex(y=>y[0]===v[0]&&y[1]===v[1])===i);inc=unique(inc);lure=unique(lure);function eventCards(){return a1.length?'<div class=section>Event-Pokémon i det fri</div>'+a1.map((p,i)=>`<div class="card click" data-w="${i}"><div class=row><div class=img>${p.asset_url?`<img src="${E(p.asset_url)}">`:'🌿'}</div><div class=grow><div class=name>${E(p.name)}</div><div class=small>${E(p.events.join(' · ')||'Event-spawn')}</div></div>›</div></div>`).join(''):'<div class=note>Ingen aktive event-spawns registreret.</div>'}function bonusCards(ls,label){return ls.length?'<div class=section>'+label+'</div>'+ls.map(x=>`<div class=card><b>${E(x[0])}</b><div class=small>• ${E(x[1])}</div></div>`).join(''):'<div class=note>Ingen aktive '+label.toLowerCase()+' angivet.</div>'}function render(tab){b.querySelectorAll('[data-wtab]').forEach(x=>x.classList.toggle('active',x.dataset.wtab===tab));if(tab==='event')b.querySelector('#wild-content').innerHTML=eventCards();if(tab==='incense')b.querySelector('#wild-content').innerHTML=bonusCards(inc,'Incense');if(tab==='lure')b.querySelector('#wild-content').innerHTML=bonusCards(lure,'Lure Modules');b.querySelectorAll('[data-w]').forEach(x=>x.onclick=async()=>{let p=a1[+x.dataset.w],q=await poke(pid(p)),t=q?.types||p.types||[];if(!Array.isArray(t))t=[t];let events=p.events||[];open(`<h2>${E(p.name)}</h2><div class=section>Type</div><div class=card>${t.map(v=>E(typeof v==='string'?v:v.name||v.type||'')).join(' · ')||'Ikke oplyst'}</div><div class=section>Shiny-chance</div><div class=card>✨ ${E(shiny(p,q))}</div><div class=section>Hvorfor spawner den?</div><div class=card>${events.length?events.map(v=>`<div class=small>• ${E(v)}</div>`).join(''):'<div class=small>Event ikke oplyst.</div>'}</div>`)})}b.innerHTML=`<div class="wild-tabs"><button class="wild-tab active" data-wtab="event">Event-spawns</button><button class="wild-tab" data-wtab="incense">Incense</button><button class="wild-tab" data-wtab="lure">Lure</button></div><div id="wild-content"></div>`;b.querySelectorAll('[data-wtab]').forEach(x=>x.onclick=()=>render(x.dataset.wtab));render('event');up()}catch(e){b.innerHTML='<div class=note>Kunne ikke hente wild-data.</div>'}}'''

pattern = r'async function wild\(\)\{.*?\}\nasync function eggs\(\)\{'
s2, n = re.subn(pattern, new_wild + '\nasync function eggs(){', s, count=1, flags=re.S)
if n != 1:
    raise SystemExit(f'Kunne ikke finde wild-funktionen: {n}')
p.write_text(s2, encoding='utf-8')
print('Wild opdateret')
