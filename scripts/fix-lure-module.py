from pathlib import Path
import re
import subprocess

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Remove the old misplaced listener exactly.
s=re.sub(r"document\.addEventListener\('click',e=>\{let b=e\.target\.closest\('\[data-lure-spawns\]'\);if\(b\)\{e\.stopPropagation\(\);showNormalLureSpawns\(\)\}\}\);",'',s)
s=re.sub(r"document\.addEventListener\('click',e=>\{let b=e\.target\.closest\('\[data-lure-event-url\]'\);if\(b\)\{e\.stopPropagation\(\);let u=b\.dataset\.lureEventUrl;if\(u\)window\.location\.assign\(u\)\}\}\);",'',s)

# Remove the old function with brace-aware parsing so no stray braces are left.
def remove_function(src,name):
    start=src.find('function '+name+'(){')
    if start<0:
        return src
    brace=src.find('{',start)
    depth=0
    end=None
    for i in range(brace,len(src)):
        if src[i]=='{': depth+=1
        elif src[i]=='}':
            depth-=1
            if depth==0:
                end=i+1
                break
    if end is None:
        raise SystemExit('Could not safely remove '+name)
    return src[:start]+src[end:]
s=remove_function(s,'showNormalLureSpawns')

old="if(tab==='lure')b.querySelector('#wild-content').innerHTML=bonusCards(lure,'Lure Modules');"
new="if(tab==='lure')b.querySelector('#wild-content').innerHTML=lureCards();"
if old not in s:
    raise SystemExit('Lure tab renderer marker not found')
s=s.replace(old,new,1)

marker='function dailyImg(id){'
if marker not in s:
    raise SystemExit('dailyImg marker not found')

code='''function lureCards(){return '<div class=section>Lure</div><button class="card click" data-normal-lure="1" style="width:100%;text-align:left"><div class=row><span style="font-size:25px">🌸</span><div class=grow><div class=name>Lure Module</div><div class=small>Spawns</div></div>›</div></button>'}\nasync function showNormalLureSpawns(){try{let a=await ev(),n=N(),matches=[];a.filter(e=>(!e.start||e.start<=n)&&(!e.end||e.end>=n)).forEach(e=>{let d=e.details||{},vals=[];Object.keys(d).forEach(k=>{if(/lure/i.test(k)&&Array.isArray(d[k]))vals.push(...d[k])});if(!vals.length&&/lure module/i.test(JSON.stringify(e))){let sp=d.spawns||e.spawns||[];if(Array.isArray(sp))vals=sp}vals.forEach(v=>{let name=typeof v==='string'?v:String(v?.name||v?.pokemon||'').trim();if(!name)return;let title=e.title||'Event',url=e.article_url||e.url||'',f=matches.find(x=>x.name.toLowerCase()===name.toLowerCase());if(!f){f={name,events:[]};matches.push(f)}if(!f.events.some(x=>x.title===title))f.events.push({title,url})})});let h='<h2>🌸 Lure Module · Spawns</h2><div class=small>Normal Lure Module · normalt 30 minutter</div><div class=section>Sådan virker det</div><div class=card><div class=small>Et almindeligt Lure Module har ikke en fast permanent Pokémon-liste. Det øger vilde spawns ved et PokéStop, og Pokémon-poolen følger den aktuelle vilde spawn-pool og aktive events.</div></div>';if(matches.length){h+='<div class=section>Aktuelle event-spawns</div>'+matches.map(x=>'<div class=card><div class=name>'+E(x.name)+'</div>'+x.events.map(v=>'<div class=small style="margin-top:5px">'+E(v.title)+'</div>'+(v.url?'<button class="btn" type="button" data-lure-event-url="'+E(v.url)+'" style="width:100%;margin-top:7px;cursor:pointer">Åbn eventet ↗</button>':'<div class=small style="margin-top:5px">Event-link ikke oplyst.</div>')).join('')+'</div>').join('')}else{h+='<div class=section>Aktuelle spawns</div><div class=note>Der er ingen registrerede aktive events, som ændrer Normal Lure Module-spawns lige nu.</div>'}h+='<div class=section>Bemærkning</div><div class=card><div class=small>Spawns kan ændre sig med sæsoner og events.</div></div>';open(h)}catch(e){open('<h2>🌸 Lure Module · Spawns</h2><div class=note>Kunne ikke hente Lure Module-data. Tryk ↻ igen.</div>')}}\n'''
s=s.replace(marker,code+marker,1)

listener="document.addEventListener('click',e=>{let b=e.target.closest('[data-normal-lure]');if(b){e.stopPropagation();showNormalLureSpawns()}});document.addEventListener('click',e=>{let b=e.target.closest('[data-lure-event-url]');if(b){e.stopPropagation();let u=b.dataset.lureEventUrl;if(u)window.location.assign(u)}});"
at=s.find("document.addEventListener('click',e=>{let b=e.target.closest('[data-event-url]')")
if at<0:
    raise SystemExit('event listener marker not found')
s=s[:at]+listener+s[at:]

blocks=re.findall(r'<script(?:[^>]*)>([\s\S]*?)</script>',s,re.I)
for i,js in enumerate(blocks,1):
    f=Path(f'/tmp/script-{i}.js')
    f.write_text(js,encoding='utf-8')
    subprocess.run(['node','--check',str(f)],check=True)

for x in ['data-wtab="lure"','Lure Module','data-normal-lure="1"','showNormalLureSpawns','Åbn eventet ↗']:
    if x not in s:
        raise SystemExit('Missing '+x)
if 'data-lure-spawns="1"' in s:
    raise SystemExit('Old misplaced Lure Module card remains')

p.write_text(s,encoding='utf-8')
