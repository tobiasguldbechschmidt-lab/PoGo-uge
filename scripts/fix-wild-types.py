from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="let p=a1[+x.dataset.w],q=await poke(pid(p)),t=q?.types||p.types||[];if(!Array.isArray(t))t=[t];let events=p.events||[];open(`<h2>${E(p.name)}</h2><div class=section>Type</div><div class=card>${t.map(v=>E(typeof v==='string'?v:v.name||v.type||'')).join(' · ')||'Ikke oplyst'}</div>"
new="let p=a1[+x.dataset.w],q=await poke(pid(p));let src=[q?.types,q?.type,q?.type1,q?.type2,q?.data?.types,q?.data?.type,q?.data?.type1,q?.data?.type2,p?.types,p?.type,p?.type1,p?.type2].filter(v=>v!=null);let t=[];const addT=v=>{if(v==null)return;if(Array.isArray(v)){v.forEach(addT);return}if(typeof v==='object'){addT(v.name??v.type??v.value??v.typeName);return}let z=String(v).trim();if(z&&!t.includes(z))t.push(z)};src.forEach(addT);let events=p.events||[];open(`<h2>${E(p.name)}</h2><div class=section>Type</div><div class=card>${t.map(v=>E(v)).join(' · ')||'Ikke oplyst'}</div>"
if old not in s:
    raise SystemExit('Kunne ikke finde wild type-blokken')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('patched')
# trigger workflow after creation
