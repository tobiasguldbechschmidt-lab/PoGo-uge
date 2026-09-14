from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
pattern=r'function battles\(\)\{.*?\}show\('
replacement=r'''function battles(){
  let b=$('battles');
  ev().then(a=>{
    let n=N();
    let all=a.filter(battleQ).filter(e=>e.start||e.end).sort((x,y)=>(x.start||x.end||0)-(y.start||y.end||0));
    let current=all.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n));
    let upcoming=all.filter(e=>e.start&&e.start>n);
    let nextStart=upcoming.length?upcoming[0].start:null;
    let next=nextStart?upcoming.filter(e=>e.start.getTime()===nextStart.getTime()):[];
    let fmt=d=>d?d.toLocaleString('da-DK',{weekday:'short',day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'}):'—';
    let range=e=>`${e.start?fmt(e.start):'Start ukendt'}${e.end?' → '+fmt(e.end):''}`;
    let card=e=>`<div class="card"><div class="name">${E(e.title)}</div><div class="small" style="margin-top:5px">${range(e)}</div>${e.end&&e.end>=n?`<div class="small" style="margin-top:5px">🟢 I gang nu</div>`:''}</div>`;
    let h='<div class=note>GO Battle League-rotationerne hentes fra den aktuelle event-feed og følger de offentliggjorte start- og sluttider.</div>';
    h+='<div class=section>🟢 I gang lige nu</div>';
    h+=current.length?current.map(card).join(''):'<div class=note>Ingen GO Battle League-rotation registreret som aktiv lige nu.</div>';
    h+='<div class=section>⏭️ Næste rotation</div>';
    h+=next.length?next.map(card).join(''):'<div class=note>Ingen kommende rotation fundet.</div>';
    let later=upcoming.filter(e=>!nextStart||e.start.getTime()>nextStart.getTime()).slice(0,6);
    if(later.length){h+='<div class=section>Kommende rotationer</div>'+later.map(card).join('')}
    b.innerHTML=h;up()
  }).catch(()=>b.innerHTML='<div class=note>Kunne ikke hente Battle League-data. Prøv ↻ igen.</div>')
}
show('''
if not re.search(pattern,s,flags=re.S):
    raise SystemExit('battle function pattern not found')
s=re.sub(pattern,replacement,s,count=1,flags=re.S)
p.write_text(s,encoding='utf-8')
print('Battle League UI updated')
