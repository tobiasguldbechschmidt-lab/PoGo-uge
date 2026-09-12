from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="function pid(p){let m=String(p.asset_url||p.name||'').match(/pm(\\d+)/i);return m?+m[1]:p.id||p.dex}async function poke(i){"
new="const TYPE_NAMES={1:'Normal',2:'Kamp',3:'Flyvende',4:'Gift',5:'Jord',6:'Klippe',7:'Bug',8:'Spøgelse',9:'Stål',10:'Ild',11:'Vand',12:'Græs',13:'Elektrisk',14:'Psykisk',15:'Is',16:'Drage',17:'Mørke',18:'Fe'};function pid(p){let s=String(p.asset_url||p.name||'');let m=s.match(/pokemon_icon_(\\d+)/i)||s.match(/pm(\\d+)/i);return m?+m[1]:p.pokedexId||p.id||p.dex}async function poke(i){"
if old not in s: raise SystemExit('pid block not found')
s=s.replace(old,new,1)
old2="let z=String(v).trim();if(z&&!t.includes(z))t.push(z)"
new2="let z=typeof v==='number'?TYPE_NAMES[v]:String(v).trim();if(z&&!t.includes(z))t.push(z)"
if old2 not in s: raise SystemExit('type conversion block not found')
s=s.replace(old2,new2,1)
p.write_text(s)
# trigger workflow
p.write_text(p.read_text()+'\n')
