from pathlib import Path
import re
import subprocess

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def remove_function(src, name):
    starts = [src.find('async function ' + name + '(){'), src.find('function ' + name + '(){')]
    starts = [x for x in starts if x >= 0]
    if not starts:
        raise SystemExit('Could not find ' + name)
    start = min(starts)
    brace = src.find('{', start)
    depth = 0
    for i in range(brace, len(src)):
        if src[i] == '{': depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0:
                return src[:start] + src[i+1:]
    raise SystemExit('Could not safely remove ' + name)

s = remove_function(s, 'eggs')

code = r'''async function eggs(){
let b=$('eggs');
try{
let raw=await get(U.eggs,60000),gs=Object.entries(raw||{});
$('tabs').innerHTML=gs.map(([d],i)=>`<button class="chip ${i?'':'active'}" data-t="${E(d)}">${E(d)}</button>`).join('');
function eggTypes(q,p){
let out=[];
function add(v){
 if(v==null)return;
 if(Array.isArray(v)){v.forEach(add);return}
 if(typeof v==='object'){add(v.name??v.type??v.value??v.typeName);return}
 let z=typeof v==='number'?TYPE_NAMES[v]:String(v).trim();
 if(z&& !out.includes(z))out.push(z)
}
[q?.types,q?.type,q?.type1,q?.type2,q?.data?.types,q?.data?.type,q?.data?.type1,q?.data?.type2,p?.types,p?.type,p?.type1,p?.type2].forEach(add);
return out
}
function hundoCp(q){
let a=Number(q?.attack),d=Number(q?.defense),st=Number(q?.stamina);
if(![a,d,st].every(Number.isFinite))return null;
let cpm=0.59740001;
return Math.max(10,Math.floor(((a+15)*Math.sqrt(d+15)*Math.sqrt(st+15)*cpm*cpm)/10));
}
function render(d){
let ls=raw[d]||[];
$('tabs').querySelectorAll('[data-t]').forEach(x=>x.classList.toggle('active',x.dataset.t===d));
b.innerHTML=ls.map((p,i)=>`<div class="card click" data-e="${i}"><div class=row><div class=img>${p.asset_url?`<img src="${E(p.asset_url)}" alt="${E(p.name)}" loading="lazy">`:'🥚'}</div><div class=grow><div class=name>${E(p.name)}</div><div class=small>${p.shiny_available===true?'✨ Shiny mulig':'Shiny ikke angivet'}</div></div>›</div></div>`).join('')||'<div class=note>Ingen Pokémon i denne Egg-pool.</div>';
b.querySelectorAll('[data-e]').forEach(x=>x.onclick=async()=>{
 let p=ls[+x.dataset.e],q=await poke(pid(p)),types=eggTypes(q,p),cp=hundoCp(q);
 let shinyText=p.shiny_available===true?'1/64 (1,56 %)':'Ikke mulig';
 open(`<h2>${E(p.name)}</h2><div class=small>Æg: ${E(d)}</div><div class=section>Type</div><div class=card>${E(types.join(' · ')||'Ikke oplyst')}</div><div class=section>Shiny-chance</div><div class=card>✨ <b>${E(shinyText)}</b><div class=small>Standard shiny-rate for Egg hatches. Særlige events kan give en anden rate.</div></div><div class=section>Hundo CP</div><div class=card><b>${cp??'—'}</b><div class=small>100 % IV (15/15/15) ved hatch på level 20.</div></div><div class=section>IV / CP</div><div class=stats><div class=stat><b>10/10/10</b><span>IV minimum</span></div><div class=stat><b>20</b><span>Hatch level</span></div><div class=stat><b>${cp??'—'}</b><span>Hundo CP</span></div></div>`)
})
}
render(gs[0]?.[0]||'');
$('tabs').querySelectorAll('[data-t]').forEach(x=>x.onclick=()=>render(x.dataset.t));
up()
}catch(e){b.innerHTML='<div class=note>Kunne ikke hente eggs.</div>'}
}
'''

marker='async function research(){'
if marker not in s: raise SystemExit('research marker not found')
s=s.replace(marker,code+marker,1)

blocks=re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>',s,re.I)
for i,js in enumerate(blocks,1):
    f=Path(f'/tmp/egg-script-{i}.js');f.write_text(js,encoding='utf-8');subprocess.run(['node','--check',str(f)],check=True)
for x in ['function hundoCp(q)','1/64 (1,56 %)','10/10/10','Hatch level','eggTypes(q,p)']:
    if x not in s: raise SystemExit('Missing '+x)
p.write_text(s,encoding='utf-8')
