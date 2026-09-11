from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old = "function shiny(p,q){let v=p.shiny_chance??p.shinyChance??p.shiny_odds??q?.shiny_chance??q?.shinyChance??q?.shiny_odds;return v==null?(p.shiny_available===true?'Shiny mulig — odds ikke oplyst':'Shiny-chance ikke oplyst'):(typeof v==='number'?'1/'+Math.round(v<1?1/v:v):String(v))}"
new = "function shiny(p,q){let v=p.shiny_chance??p.shinyChance??p.shiny_odds??q?.shiny_chance??q?.shinyChance??q?.shiny_odds;if(v!=null)return typeof v==='number'?'1/'+Math.round(v<1?1/v:v):String(v);if(p.shiny_available!==true)return 'Ikke mulig';let t=String(p.tier||p.g||'').toLowerCase();return t.includes('5')?'ca. 1/20':'ca. 1/64'}"
if old not in s:
    raise SystemExit('shiny function target not found')
s = s.replace(old, new, 1)

old2 = "players=r=>r.recommended_players??r.recommendedPlayers??r.min_players??r.minPlayers??(tier(r)==='Mega'?'5+':tier(r)==='5-stjernet'?'4–6':tier(r)==='3-stjernet'?'2–3':'1'),draw=r=>`<div class=\"card click\" data-r=\"${encodeURIComponent(JSON.stringify(r))}\"><div class=row><div class=img>${r.asset_url?`<img src=\"${E(r.asset_url)}\">`:'⚔️'}</div><div class=grow><div class=name>${E(r.name)}</div><div class=small>${E((r.types||[]).join(' · '))} · ${r.shiny_available===true?'✨ Shiny mulig':'Shiny ikke angivet'}</div></div>›</div>"
new2 = "players=r=>r.recommended_players??r.recommendedPlayers??r.min_players??r.minPlayers??(tier(r)==='Mega'?'5+':tier(r)==='5-stjernet'?'4–6':tier(r)==='3-stjernet'?'2–3':'1'),draw=r=>`<div class=\"card click\" data-r=\"${encodeURIComponent(JSON.stringify(r))}\"><div class=row><div class=img>${r.asset_url?`<img src=\"${E(r.asset_url)}\">`:'⚔️'}</div><div class=grow><div class=name>${E(r.name)}</div><div class=small>${E((r.types||[]).join(' · '))} · ✨ ${E(shiny(r,null))}</div></div>›</div>"
if old2 not in s:
    raise SystemExit('raid card target not found')
s = s.replace(old2, new2, 1)

old3 = "<div class=section>Gode mod den</div><div class=card><b>Svag mod:</b> ${E(c[0])}<div class=section>Mega / Primal</div>${c[1].map(v=>`<div class=small>• ${E(v)}</div>`).join('')}<div class=section>Ikke Mega</div>${c[2].map(v=>`<div class=small>• ${E(v)}</div>`).join('')}</div><div class=stats>"
new3 = "<div class=section>Gode mod den</div><div class=card><b>Svag mod:</b> ${E(c[0])}<div class=section>Mega / Primal</div>${c[1].map(v=>`<div class=small>• ${E(v)}</div>`).join('')}<div class=section>Ikke Mega</div>${c[2].map(v=>`<div class=small>• ${E(v)}</div>`).join('')}</div><div class=section>Shiny-chance</div><div class=card>✨ ${E(shiny(r,null))}</div><div class=stats>"
if old3 not in s:
    raise SystemExit('raid detail target not found')
s = s.replace(old3, new3, 1)

p.write_text(s, encoding='utf-8')
