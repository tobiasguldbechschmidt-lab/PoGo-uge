from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='async function wild(){'
insert="""const DAILY_INCENSE=[
['Galarian Articuno',144,1],['Galarian Zapdos',145,1],['Galarian Moltres',146,1],
['Vullaby',629,2],['Espurr',677,2],['Rockruff',744,2],['Gible',443,2],['Jangmo-o',782,2],['Tirtouga',564,3],['Archen',566,3],['Cryogonal',615,3],['Aerodactyl',142,3],['Absol',359,3],['Lapras',131,3],['Phantump',708,3],['Chimecho',358,3],['Tyrunt',696,3],['Audino',531,3],['Dedenne',702,3],['Miltank',241,3],['Munna',517,3],['Spritzee',682,3],['Inkay',686,3],['Sewaddle',540,3],['Nosepass',299,3],['Spoink',325,3],['Galarian Slowpoke',79,3],
['Dragonite',149,4],['Metagross',376,4],['Gardevoir',282,4],['Gengar',94,4],['Machamp',68,4],['Gyarados',130,4],['Mamoswine',473,4],['Rhyperior',464,4],['Aggron',306,4],['Flygon',330,4],['Houndoom',229,4],['Talonflame',663,4],['Abomasnow',460,4],['Bewear',760,4],['Altaria',334,4],['Wigglytuff',40,4],['Jumpluff',189,4],['Shiftry',275,4],['Toxicroak',454,4],['Slaking',289,4],['Forretress',205,4],['Alolan Sandslash',28,4],['Rapidash',78,4],['Pidgeot',18,4],['Blastoise',9,4],['Charizard',6,4],['Venusaur',3,4],['Ampharos',181,4],['Luxray',405,4],['Alakazam',65,4]
];
function dailyIncenseCards(){return '<div class=section>Daily Incense</div><div class=note>Sorteret fra sjældnest til mindst sjælden. Listen viser den særlige Daily Adventure Incense-pool; normale event- og sæsonspawns kan komme oveni.</div><button class="card click" data-daily="1" style="width:100%;text-align:left"><div class=row><span style="font-size:25px">🧭</span><div class=grow><div class=name>Daily Incense</div><div class=small>Se hele Daily Adventure Incense-poolen</div></div>›</div></button>'}
function showDailyIncense(){let h='<h2>Daily Incense</h2><div class=small>Daily Adventure Incense · sjældnest øverst</div>';h+='<div class=section>Pokémon</div>';h+=DAILY_INCENSE.map((v,i)=>`<div class="card click" data-daily-p="${i}"><div class=row><div class=img><img src="https://raw.githubusercontent.com/WatWowMap/pogo-data-api/main/images/pokemon/${v[1]}.png" onerror="this.style.display='none'"></div><div class=grow><div class=name>${E(v[0])}</div><div class=small>${v[2]===1?'Ekstremt sjælden':v[2]===2?'Meget sjælden':v[2]===3?'Sjælden':'Sjælden evolution'}</div></div>›</div></div>`).join('');open(h);document.querySelectorAll('[data-daily-p]').forEach(x=>x.onclick=async()=>{let v=DAILY_INCENSE[+x.dataset.dailyP],q=await poke(v[1]);let ts=[];let add=v=>{if(v==null)return;if(Array.isArray(v)){v.forEach(add);return}if(typeof v==='object'){add(v.name??v.type??v.value);return}let z=typeof v==='number'?TYPE_NAMES[v]:String(v).trim();if(z&&!ts.includes(z))ts.push(z)};add(q?.types);let p={shiny_available:true};let sc=v[2]<=2?'ca. 1/64':'ca. 1/64';if(v[2]===1)sc='ca. 1/20';open(`<h2>${E(v[0])}</h2><div class=section>Type</div><div class=card>${ts.join(' · ')||'Ikke oplyst'}</div><div class=section>Shiny-chance</div><div class=card>${sc}</div><div class=section>Kilde</div><div class=small>Daily Adventure Incense</div>`)})}
"""
if marker not in s: raise SystemExit('wild marker not found')
s=s.replace(marker,insert+marker,1)
needle="async function wild(){let b=$('wild');try{"
if needle not in s: raise SystemExit('wild start not found')
# Add the button to the existing Incense tab section without touching raid/overview.
s=s.replace("function bonusCards(ls,label){return ls.length?'<div class=section>'+label+'</div>'", "function bonusCards(ls,label){return ls.length?'<div class=section>'+label+'</div>'",1)
# Add Daily Incense button directly before the existing tab navigation is rendered.
old="b.innerHTML='<div class=wild-tabs><button class=wild-tab data-w=event>Event-spawns</button><button class=wild-tab data-w=inc>Incense</button><button class=wild-tab data-w=lure>Lure</button></div>'"
new="b.innerHTML='<div class=wild-tabs><button class=wild-tab data-w=event>Event-spawns</button><button class=wild-tab data-w=inc>Incense</button><button class=wild-tab data-w=lure>Lure</button></div>'"
# Instead of fragile exact replacement, inject handler after the tab click wiring by matching the known final expression.
if old not in s: raise SystemExit('wild tabs render not found')
# Keep the existing renderer, then add a Daily Incense button into the Incense tab content via a targeted replacement.
s=s.replace("w.innerHTML=eventCards();", "w.innerHTML=eventCards();",1)
# Add the button to the Incense tab's generated content by replacing the inc render branch.
s=s.replace("w.innerHTML=bonusCards(inc,'Incense');", "w.innerHTML=dailyIncenseCards()+bonusCards(inc,'Incense');",1)
# Wire the Daily Incense button after the existing wild tab handler setup.
anchor="document.querySelectorAll('[data-w]').forEach(x=>x.onclick=()=>{document.querySelectorAll('[data-w]').forEach(y=>y.classList.toggle('active',y===x));let v=x.dataset.w;w.innerHTML=v==='event'?eventCards():v==='inc'?dailyIncenseCards()+bonusCards(inc,'Incense'):bonusCards(lure,'Lure');document.querySelectorAll('[data-wp]').forEach(z=>z.onclick=async()=>{let p=a1[+z.dataset.wp],q=await poke(pid(p));"
if anchor not in s:
    # Search for a simpler known segment and append listener after wild function via the next function declaration.
    raise SystemExit('wild handler anchor not found')
s=s.replace(anchor,anchor,1)
# Ensure daily button opens the pool; this listener is global and only targets data-daily.
s=s.replace("document.querySelectorAll('[data-w]').forEach(x=>x.onclick=", "document.querySelectorAll('[data-daily]').forEach(x=>x.onclick=()=>showDailyIncense());document.querySelectorAll('[data-w]').forEach(x=>x.onclick=",1)
p.write_text(s)
"