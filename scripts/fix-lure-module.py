from pathlib import Path
import re
import subprocess

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def remove_function(src, name):
    starts = [src.find('async function ' + name + '(){'), src.find('function ' + name + '(){')]
    starts = [x for x in starts if x >= 0]
    if not starts:
        return src
    start = min(starts)
    brace = src.find('{', start)
    depth = 0
    for i in range(brace, len(src)):
        if src[i] == '{': depth += 1
        elif src[i] == '}':
            depth -= 1
            if depth == 0: return src[:start] + src[i+1:]
    raise SystemExit('Could not safely remove ' + name)

for name in ['lureCards','showNormalLureSpawns','showNormalLureDuration']:
    s = remove_function(s, name)

code = r'''function lureCards(){return '<div class=section>Lure</div><div class="card"><div class=row><span style="font-size:25px">🌸</span><div class=grow><div class=name>Lure Module</div><div class=small>Normal Lure Module</div></div></div><div class="grid" style="margin-top:10px"><button class="btn click" data-normal-lure-duration="1" type="button">⏱ Varighed</button><button class="btn click" data-normal-lure="1" type="button">🌸 Spawns</button></div></div>'}
function lureImg(name){let n=String(name||'').toLowerCase().trim();let map={'bulbasaur':1,'charmander':4,'squirtle':7,'pikachu':25,'eevee':133,'rattata':19,'pidgey':16,'zubat':41,'spearow':21,'magikarp':129,'abra':63,'machop':66,'cubone':104,'snorlax':143,'passimian':766,'gible':443,'jynx':124,'eevee':133,'totodile':158,'swinub':220,'snorunt':361,'mantine':226,'spheal':363,'piplup':393,'snover':459,'oshawott':501,'seel':86,'shellder':90,'magikarp':129,'sneasel':215,'wailmer':320,'feebas':349,'clamperl':366,'finneon':456,'cryogonal':615,'oddish':43,'bellsprout':69,'venonat':48,'tangela':114,'sudowoodo':185,'hoppip':187,'yanma':193,'roselia':315,'cherubi':420,'applin':840,'butterfree':12,'beedrill':15,'exeggcute':102,'scyther':123,'shuckle':213,'gulpin':316,'combee':415,'alolan geodude':74,'magnemite':81,'voltorb':100,'electrode':101,'jolteon':135,'nosepass':299,'aron':304,'beldum':374,'joltik':595,'alolan diglett':50,'onix':95,'electabuzz':125,'mareep':179,'skarmory':227,'lairon':305,'electrike':309,'shieldon':410,'psyduck':54,'spinarak':167,'chinchou':170,'surskit':283,'tympole':535,'tynamo':602,'stunfisk':618,'froakie':656,'gimmighoul':999};let id=map[n];return id?'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'+id+'.png':''}
function lureShinyText(item,event){let txt=JSON.stringify(item||'')+' '+JSON.stringify(event||'');if(/increased chance|increased chance to be shiny|increased chance of being shiny|øget chance.*shiny/i.test(txt))return '✨ Shiny: Forøget chance (event)';return '✨ Shiny: ca. 1/512 (standard-estimat)'}
function lureDurationInfo(active){let hits=active.filter(e=>/lure module|lure modules|lures/i.test(JSON.stringify(e)));let one=hits.find(e=>/one hour|1 hour|2-hour|2 hour|three hour|3-hour|3 hour|one-hour|two-hour/i.test(JSON.stringify(e)));if(one){let t=JSON.stringify(one);let d=/2-hour|2 hour|two-hour/i.test(t)?'2 timer':/3-hour|3 hour|three hour/i.test(t)?'3 timer':'1 time';return {duration:d,event:one}}return {duration:'30 minutter',event:null}}
async function showNormalLureDuration(){try{let a=await ev(),n=N(),active=a.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n)),d=lureDurationInfo(active),h='<h2>🌸 Lure Module · Varighed</h2><div class=small>Normal Lure Module</div><div class=section>Normal varighed</div><div class=card><div class=name>30 minutter</div><div class=small style="margin-top:5px">Et normalt Lure Module tiltrækker Pokémon til en PokéStop og effekten gælder også for andre spillere i nærheden.</div></div>';if(d.event){let u=d.event.article_url||d.event.url||'';h+='<div class=section>Aktuel bonus</div><div class=card><div class=name>'+E(d.duration)+'</div><div class=small style="margin-top:5px">'+E(d.event.title||'Aktivt event')+' ændrer Lure Module-varigheden.</div>'+(u?'<button class="btn" type="button" data-lure-event-url="'+E(u)+'" style="width:100%;margin-top:8px;cursor:pointer">Åbn eventet ↗</button>':'')+'</div>'}else h+='<div class=section>Aktuel bonus</div><div class=note>Ingen registreret aktiv global event-bonus for Normal Lure Module lige nu.</div>';h+='<div class=section>Sådan virker det</div><div class=card><div class=small>Placér en Lure Module på en PokéStop. Den øger Pokémon-spawns omkring PokéStoppen og kan ses og bruges af andre spillere tæt på. Normal Lure har ikke en permanent fast Pokémon-liste; sæsoner og events kan ændre hvilke Pokémon der tiltrækkes.</div></div><div class=section>Officiel info</div><div class=card><div class=small>Et normalt Lure Module varer normalt 30 minutter. Særlige events kan forlænge varigheden og give særlige Lure-spawns.</div></div>';open(h)}catch(e){open('<h2>🌸 Lure Module · Varighed</h2><div class=note>Kunne ikke hente Lure-data. Tryk ↻ igen.</div>')}}
async function showNormalLureSpawns(){try{let a=await ev(),n=N(),active=a.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n)),items=[];active.forEach(e=>{let raw=JSON.stringify(e);if(!/lure module|lure modules|regular lure|active regular lure/i.test(raw))return;let found=[],d=e.details||{};Object.keys(d).forEach(k=>{let v=d[k];if(/lure/i.test(k)&&Array.isArray(v))found.push(...v)});[e.lure_spawns,e.lureSpawns,e.spawns,d.lure_spawns,d.lureSpawns,d.spawns].filter(Array.isArray).forEach(v=>found.push(...v));found.forEach(v=>{let name=typeof v==='string'?v:String(v?.name||v?.pokemon||'').trim();if(name)items.push({name,event:e,raw:v})})});let seen=new Set();items=items.filter(x=>{let k=x.name.toLowerCase();if(seen.has(k))return false;seen.add(k);return true});let h='<h2>🌸 Lure Module · Spawns</h2><div class=small>Pokémon tiltrukket af en normal Lure Module</div><div class=section>Spawns</div>';if(items.length){h+='<div class=small style="margin-bottom:8px">Aktive event-spawns fra Normal Lure</div>'+items.map(x=>'<div class="card"><div class=row><div class=img><img src="'+E(lureImg(x.name))+'" alt="'+E(x.name)+'"></div><div class=grow><div class=name>'+E(x.name)+'</div><div class=small>'+E(x.event.title||'Aktivt event')+'</div><div class=small style="margin-top:5px">'+E(lureShinyText(x.raw,x.event))+'</div></div></div>'+(x.event.article_url||x.event.url?'<button class="btn" type="button" data-lure-event-url="'+E(x.event.article_url||x.event.url)+'" style="width:100%;margin-top:8px;cursor:pointer">Åbn eventet ↗</button>':'')+'</div>').join('')}else{let baseline=['Bulbasaur','Charmander','Squirtle','Pikachu','Eevee','Rattata','Pidgey','Zubat','Spearow','Magikarp','Abra','Machop','Cubone','Snorlax','Passimian'];h+='<div class=small style="margin-bottom:8px">Normal Lure har ingen permanent fast artsliste. Når der ikke er et Lure-specifikt event, følger den den almindelige vilde spawn-pool. Her vises derfor en løbende standardliste med Pokémon, som kan være blandt Normal Lure-spawns — ikke en garanteret lokal encounter-liste.</div>'+baseline.map(name=>'<div class="card"><div class=row><div class=img><img src="'+E(lureImg(name))+'" alt="'+E(name)+'"></div><div class=grow><div class=name>'+E(name)+'</div><div class=small>'+E(lureShinyText(name,''))+'</div></div></div></div>').join('')}h+='<div class=section>Shiny-chance</div><div class=card><div class=small>For Pokémon uden en specifik event-rate vises et standard-estimat på ca. 1/512. Hvis et event udtrykkeligt angiver en øget shiny-chance, markeres den som event-forøget. Den præcise rate er ikke altid offentliggjort af Niantic.</div></div>';open(h)}catch(e){open('<h2>🌸 Lure Module · Spawns</h2><div class=note>Kunne ikke hente Lure-spawns. Tryk ↻ igen.</div>')}}
'''
marker='function dailyImg(id){'
if marker not in s: raise SystemExit('dailyImg marker not found')
s=s.replace(marker,code+marker,1)

if "if(tab==='lure')" not in s: raise SystemExit('Lure tab renderer not found')
s=re.sub(r"if\(tab==='lure'\)b\.querySelector\('#wild-content'\)\.innerHTML=[^;]+;", "if(tab==='lure')b.querySelector('#wild-content').innerHTML=lureCards();", s, count=1)

s=re.sub(r"document\.addEventListener\('click',e=>\{let b=e\.target\.closest\('\[data-(?:normal-lure|normal-lure-duration|lure-event-url|lure-spawns)\]'\);[\s\S]*?\}\);",'',s)
at=s.find("document.addEventListener('click',e=>{let b=e.target.closest('[data-event-url]')")
if at<0: raise SystemExit('event listener marker not found')
listener="document.addEventListener('click',e=>{let b=e.target.closest('[data-normal-lure]');if(b){e.stopPropagation();showNormalLureSpawns()}});document.addEventListener('click',e=>{let b=e.target.closest('[data-normal-lure-duration]');if(b){e.stopPropagation();showNormalLureDuration()}});document.addEventListener('click',e=>{let b=e.target.closest('[data-lure-event-url]');if(b){e.stopPropagation();let u=b.dataset.lureEventUrl;if(u)window.location.assign(u)}});"
s=s[:at]+listener+s[at:]

blocks=re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>',s,re.I)
for i,js in enumerate(blocks,1):
    f=Path(f'/tmp/script-{i}.js');f.write_text(js,encoding='utf-8');subprocess.run(['node','--check',str(f)],check=True)
for x in ['data-wtab="lure"','Lure Module','data-normal-lure="1"','data-normal-lure-duration="1"','showNormalLureSpawns','showNormalLureDuration','Shiny: ca. 1/512']:
    if x not in s: raise SystemExit('Missing '+x)
if 'data-lure-spawns="1"' in s: raise SystemExit('Old misplaced Lure Module card remains')
p.write_text(s,encoding='utf-8')