from pathlib import Path
import re
import subprocess

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove old Lure listeners/function safely.
s=re.sub(r"document\.addEventListener\('click',e=>\{let b=e\.target\.closest\('\[data-lure-spawns\]'\);if\(b\)\{e\.stopPropagation\(\);showNormalLureSpawns\(\)\}\}\);",'',s)
s=re.sub(r"document\.addEventListener\('click',e=>\{let b=e\.target\.closest\('\[data-normal-lure\]'\);if\(b\)\{e\.stopPropagation\(\);showNormalLureSpawns\(\)\}\}\);",'',s)
s=re.sub(r"document\.addEventListener\('click',e=>\{let b=e\.target\.closest\('\[data-lure-event-url\]'\);if\(b\)\{e\.stopPropagation\(\);let u=b\.dataset\.lureEventUrl;if\(u\)window\.location\.assign\(u\)\}\}\);",'',s)

def remove_function(src,name):
    start=src.find('function '+name+'(){')
    if start<0:
        start=src.find('async function '+name+'(){')
    if start<0:
        return src
    brace=src.find('{',start)
    depth=0
    for i in range(brace,len(src)):
        if src[i]=='{': depth+=1
        elif src[i]=='}':
            depth-=1
            if depth==0:
                return src[:start]+src[i+1:]
    raise SystemExit('Could not safely remove '+name)

s=remove_function(s,'showNormalLureSpawns')

old="if(tab==='lure')b.querySelector('#wild-content').innerHTML=bonusCards(lure,'Lure Modules');"
new="if(tab==='lure')b.querySelector('#wild-content').innerHTML=lureCards();"
if old in s:
    s=s.replace(old,new,1)
else:
    raise SystemExit('Lure tab renderer marker not found')

marker='function dailyImg(id){'
if marker not in s:
    raise SystemExit('dailyImg marker not found')

code=r'''function lureCards(){return '<div class=section>Lure</div><div class="grid"><button class="card click" data-normal-lure="1" style="width:100%;text-align:left;min-height:105px"><div class=row><span style="font-size:25px">🌸</span><div class=grow><div class=name>Lure Module</div><div class=small>Varighed + Spawns</div></div>›</div></button></div>'}
function lureImg(name){let slug=String(name||'').toLowerCase().trim().replace(/[’'().:]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');return 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'+slug+'.png'}
async function lureSprite(name){try{let key='lure-poke-'+String(name||'').toLowerCase();if(C[key])return C[key];let slug=String(name||'').toLowerCase().trim().replace(/[’'().:]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');let r=await fetch('https://pokeapi.co/api/v2/pokemon/'+encodeURIComponent(slug));if(!r.ok)throw 0;let d=await r.json();return C[key]='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'+d.id+'.png'}catch{return lureImg(name)}}
function lureShinyText(item,event){let txt=JSON.stringify(item||'')+' '+JSON.stringify(event||'');if(/increased chance|increased chance to be shiny|increased chance of being shiny|øget chance.*shiny/i.test(txt))return '✨ Shiny: Forøget chance (event)';return '✨ Shiny: ca. 1/512 (standard-estimat)'}
function lureDurationInfo(active){let hits=active.filter(e=>/lure module|lure modules|lures/i.test(JSON.stringify(e)));let one=hits.find(e=>/one hour|1 hour|2-hour|2 hour|three hour|3-hour|3 hour/i.test(JSON.stringify(e)));if(one){let t=JSON.stringify(one);let d=/2-hour|2 hour/i.test(t)?'2 timer':/3-hour|3 hour|three hour/i.test(t)?'3 timer':'1 time';return {duration:d,event:one}}return {duration:'30 minutter',event:null}}
async function showNormalLureDuration(){try{let a=await ev(),n=N(),active=a.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n));let d=lureDurationInfo(active),h='<h2>🌸 Lure Module · Varighed</h2><div class=small>Normal Lure Module</div><div class=section>Normal varighed</div><div class=card><div class=name>30 minutter</div><div class=small style="margin-top:5px">Et normalt Lure Module tiltrækker Pokémon til en PokéStop og effekten kan ses og bruges af andre spillere i nærheden.</div></div>';if(d.event){let u=d.event.article_url||d.event.url||'';h+='<div class=section>Aktuel bonus</div><div class=card><div class=name>'+E(d.duration)+'</div><div class=small style="margin-top:5px">'+E(d.event.title||'Aktivt event')+' forlænger Lure Module-varigheden.</div>'+(u?'<button class="btn" type="button" data-lure-event-url="'+E(u)+'" style="width:100%;margin-top:8px;cursor:pointer">Åbn eventet ↗</button>':'')+'</div>'}else{h+='<div class=section>Aktuel bonus</div><div class=note>Ingen registreret aktiv global event-bonus for Normal Lure Module lige nu.</div>'}h+='<div class=section>Sådan virker det</div><div class=card><div class=small>Placér en Lure Module på en PokéStop. Den øger Pokémon-spawns omkring PokéStoppen og påvirker alle spillere, der er tæt nok på. Normal Lure har ikke en permanent fast Pokémon-liste; event- og sæsonændringer kan ændre hvilke Pokémon der tiltrækkes.</div></div><div class=section>Officiel info</div><div class=card><div class=small>Normal Lure Module varer normalt 30 minutter. Særlige events kan forlænge varigheden og samtidig give særlige Lure-spawns.</div></div>';open(h)}catch(e){open('<h2>🌸 Lure Module · Varighed</h2><div class=note>Kunne ikke hente Lure-data. Tryk ↻ igen.</div>')}}
async function showNormalLureSpawns(){try{let a=await ev(),n=N(),active=a.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n)),items=[];active.forEach(e=>{let raw=JSON.stringify(e),has=/lure module|lure modules|regular lure|active regular lure/i.test(raw);if(!has)return;let found=[];let d=e.details||{};Object.keys(d).forEach(k=>{let v=d[k];if(/lure/i.test(k)&&Array.isArray(v))found.push(...v)});let pools=[e.lure_spawns,e.lureSpawns,e.spawns,d.lure_spawns,d.lureSpawns,d.spawns].filter(Array.isArray);pools.forEach(v=>found.push(...v));let text=raw.match(/(?:attract|appearing|spawns)[^\n]{0,180}/ig)||[];found.forEach(v=>{let name=typeof v==='string'?v:String(v?.name||v?.pokemon||'').trim();if(name)items.push({name,event:e,raw:v})});if(!found.length&&/very high chance of appearing|chance of appearing/i.test(raw)){let title=e.title||'';let known={};if(/community day/i.test(title))known=title;}});let seen=new Set();items=items.filter(x=>{let k=x.name.toLowerCase();if(seen.has(k))return false;seen.add(k);return true});let h='<h2>🌸 Lure Module · Spawns</h2><div class=small>Pokémon tiltrukket af en normal Lure Module</div><div class=section>Sådan virker det</div><div class=card><div class=small>Normal Lure har ikke en fast permanent Pokémon-liste. Derfor viser denne visning især event-specifikke Lure-spawns, når et aktivt event ændrer Lure-poolen.</div></div>';if(items.length){h+='<div class=section>Aktuelle Lure-spawns</div><div id="lure-spawn-list">'+items.map((x,i)=>'<div class="card"><div class=row><div class=img><img id="lure-img-'+i+'" src="'+E(lureImg(x.name))+'" alt="'+E(x.name)+'"></div><div class=grow><div class=name>'+E(x.name)+'</div><div class=small>'+E(x.event.title||'Aktivt event')+'</div><div class=small style="margin-top:5px">'+E(lureShinyText(x.raw,x.event))+'</div></div></div>'+(x.event.article_url||x.event.url?'<button class="btn" type="button" data-lure-event-url="'+E(x.event.article_url||x.event.url)+'" style="width:100%;margin-top:8px;cursor:pointer">Åbn eventet ↗</button>':'')+'</div>').join('')+'</div>';items.forEach((x,i)=>{lureSprite(x.name).then(u=>{let el=$('lure-img-'+i);if(el)el.src=u})})}else{h+='<div class=section>Aktuelle spawns</div><div class=note>Der er ingen registrerede aktive events med særlige Normal Lure-spawns lige nu. Normal Lure følger den aktuelle vilde spawn-pool, så den har ikke en fast artsliste.</div>'}h+='<div class=section>Shiny-chance</div><div class=card><div class=small>For Pokémon uden en specifik event-rate vises et standard-estimat på ca. 1/512. Hvis et event udtrykkeligt angiver en øget shiny-chance, markeres den som event-forøget. Den præcise rate er ikke altid offentliggjort af Niantic.</div></div>';open(h)}catch(e){open('<h2>🌸 Lure Module · Spawns</h2><div class=note>Kunne ikke hente Lure-spawns. Tryk ↻ igen.</div>')}}
'''
s=s.replace(marker,code+marker,1)

at=s.find("document.addEventListener('click',e=>{let b=e.target.closest('[data-event-url]')")
if at<0: raise SystemExit('event listener marker not found')
listener="document.addEventListener('click',e=>{let b=e.target.closest('[data-normal-lure]');if(b){e.stopPropagation();showNormalLureSpawns()}});document.addEventListener('click',e=>{let b=e.target.closest('[data-normal-lure-duration]');if(b){e.stopPropagation();showNormalLureDuration()}});document.addEventListener('click',e=>{let b=e.target.closest('[data-lure-event-url]');if(b){e.stopPropagation();let u=b.dataset.lureEventUrl;if(u)window.location.assign(u)}});"
s=s[:at]+listener+s[at:]

# Make the Lure card offer two sub-actions, matching the Incense pattern.
old_card="<div class=\"grid\"><button class=\"card click\" data-normal-lure=\"1\" style=\"width:100%;text-align:left;min-height:105px\"><div class=row><span style=\"font-size:25px\">🌸</span><div class=grow><div class=name>Lure Module</div><div class=small>Varighed + Spawns</div></div>›</div></button></div>"
new_card="<div class=\"card\"><div class=row><span style=\"font-size:25px\">🌸</span><div class=grow><div class=name>Lure Module</div><div class=small>Normal Lure Module</div></div></div><div class=\"grid\" style=\"margin-top:10px\"><button class=\"btn click\" data-normal-lure-duration=\"1\" type=\"button\">⏱ Varighed</button><button class=\"btn click\" data-normal-lure=\"1\" type=\"button\">🌸 Spawns</button></div></div>"
if old_card not in s: raise SystemExit('Lure card marker not found')
s=s.replace(old_card,new_card,1)

blocks=re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>',s,re.I)
for i,js in enumerate(blocks,1):
    f=Path(f'/tmp/script-{i}.js');f.write_text(js,encoding='utf-8');subprocess.run(['node','--check',str(f)],check=True)
for x in ['data-wtab="lure"','Lure Module','data-normal-lure="1"','data-normal-lure-duration="1"','showNormalLureSpawns','showNormalLureDuration','lureSprite','Shiny: ca. 1/512']:
    if x not in s: raise SystemExit('Missing '+x)
if 'data-lure-spawns="1"' in s: raise SystemExit('Old misplaced Lure Module card remains')
p.write_text(s,encoding='utf-8')
