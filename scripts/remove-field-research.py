from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

patterns = [
    r'<button class="menu" data-p="research">.*?</button>',
    r'<section class="page" id="p-research">.*?</section>\n',
]
for pattern in patterns:
    s2, n = re.subn(pattern, '', s, flags=re.S)
    if n != 1:
        raise SystemExit(f'Expected exactly one match for {pattern!r}, got {n}')
    s = s2

s = s.replace('Events, raids, wild, eggs, research, Dynamax og Battles.', 'Events, raids, wild, eggs, Dynamax og Battles.')
s = s.replace("\nasync function research(){try{let r=await get(U.research,60000),h='';Object.entries(r||{}).forEach(([g,ls])=>{if(Array.isArray(ls))h+=`<div class=section>${E(g)}</div>`+ls.map(x=>`<div class=\"card\"><div class=\"name\">${E(x.task||x.name||'Task')}</div><div class=small>${E(x.reward||x.rewards||'')}</div>${x.encounters?`<div class=small>${[].concat(x.encounters).map(y=>E(y.name||y.type||'Reward')).join(' · ')}</div>`:''}</div>`).join('')});$('research').innerHTML=h||'<div class=empty>Ingen research.</div>';up()}catch(e){$('research').innerHTML='<div class=note>Kunne ikke hente research.</div>'}}", '')
s = re.sub(r',research:B\+\'research_tasks\.json\'', '', s)
s = s.replace(",research:['Field Research Tasks','Rewards']", '')
s = s.replace("if(p==='research')research();", '')

if 'data-p="research"' in s or 'id="p-research"' in s or 'Field Research Tasks' in s or 'research()' in s:
    raise SystemExit('Field Research remnants remain in index.html')

p.write_text(s, encoding='utf-8')
print('Field Research removed successfully')
