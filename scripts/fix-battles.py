from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
start=s.find('function battleQ')
end=s.find('async function ev',start)
if start<0 or end<0:
    raise SystemExit('battle anchors not found')
replacement=r'''function battleQ(e){let s=(e.title+' '+(e.category||'')+' '+(e.type||'')).toLowerCase();return /battle league|go battle league|league:|cup:/.test(s)}
function battles(){
  let b=$('battles');
  let schedule=[
    [['Great League: Mega Edition','Ultra League: Mega Edition','Master League: Mega Edition'],'2026-09-08T20:00:00Z','2026-09-15T20:00:00Z'],
    [['Great League','Ultra League: Mega Edition','Willpower Cup: Great League Edition'],'2026-09-15T20:00:00Z','2026-09-22T20:00:00Z'],
    [['Ultra League','Master League: Mega Edition','Retro Cup: Great League Edition'],'2026-09-22T20:00:00Z','2026-09-29T20:00:00Z'],
    [['Master League','Mega Color Cup: Great League Edition'],'2026-09-29T20:00:00Z','2026-10-06T20:00:00Z'],
    [['Great League: Mega Edition','Ultra League: Mega Edition','Master League: Mega Edition'],'2026-10-06T20:00:00Z','2026-10-13T20:00:00Z'],
    [['Great League','Ultra League: Mega Edition','Little Cup: Little Edition'],'2026-10-13T20:00:00Z','2026-10-20T20:00:00Z'],
    [['Ultra League','Master League: Mega Edition','Fantasy Cup: Ultra League Edition'],'2026-10-20T20:00:00Z','2026-10-27T20:00:00Z'],
    [['Master League','Mega Halloween Cup: Great League Edition'],'2026-10-27T20:00:00Z','2026-11-03T21:00:00Z'],
    [['Great League: Mega Edition','Ultra League: Mega Edition','Master League: Mega Edition'],'2026-11-03T21:00:00Z','2026-11-10T21:00:00Z'],
    [['Great League','Ultra League: Mega Edition','2026 GO LAIC Cup: Great League Edition'],'2026-11-10T21:00:00Z','2026-11-17T21:00:00Z']
  ].map(x=>({titles:x[0],start:new Date(x[1]),end:new Date(x[2])}));
  let n=N(),fmt=d=>d.toLocaleString('da-DK',{weekday:'short',day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'}),card=e=>`<div class="card"><div class="name">${e.titles.map(E).join(' · ')}</div><div class="small" style="margin-top:6px">${fmt(e.start)} → ${fmt(e.end)}</div></div>`;
  let current=schedule.filter(e=>e.start<=n&&e.end>=n),upcoming=schedule.filter(e=>e.start>n),next=upcoming[0];
  let h='<div class="note">GO Battle League-rotationer følger den offentliggjorte Twilight Trails-plan. Tiderne vises i din lokale tid.</div><div class="section">🟢 I gang lige nu</div>';
  h+=current.length?current.map(card).join(''):'<div class="note">Ingen rotation fundet lige nu.</div>';
  h+='<div class="section">⏭️ Næste rotation</div>'+ (next?card(next):'<div class="note">Ingen kommende rotation fundet.</div>');
  let later=upcoming.slice(1,6);if(later.length)h+='<div class="section">📅 Kommende rotationer</div>'+later.map(card).join('');
  b.innerHTML=h;up()
}
'''
s=s[:start]+replacement+s[end:]
p.write_text(s,encoding='utf-8')
print('Battle League schedule updated')
