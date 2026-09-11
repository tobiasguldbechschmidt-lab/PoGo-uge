from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
start=s.index('async function raids(){')
end=s.index('async function wild(){', start)
new=r'''const RAID_WEAK={
  Normal:['Fighting'],Fire:['Water','Ground','Rock'],Water:['Electric','Grass'],Electric:['Ground'],Grass:['Fire','Ice','Poison','Flying','Bug'],Ice:['Fire','Fighting','Rock','Steel'],Fighting:['Flying','Psychic','Fairy'],Poison:['Ground','Psychic'],Ground:['Water','Grass','Ice'],Flying:['Electric','Ice','Rock'],Psychic:['Bug','Ghost','Dark'],Bug:['Fire','Flying','Rock'],Rock:['Water','Grass','Fighting','Ground','Steel'],Ghost:['Ghost','Dark'],Dragon:['Ice','Dragon','Fairy'],Dark:['Fighting','Bug','Fairy'],Steel:['Fire','Fighting','Ground'],Fairy:['Poison','Steel']
};
const RAID_COUNTERS={
  Fighting:[['Mega Lucario','Mega Blaziken','Mega Mewtwo X'],['Lucario','Machamp','Conkeldurr']],
  Water:[['Primal Kyogre','Mega Swampert','Mega Gyarados'],['Kyogre','Swampert','Kingler']],
  Ground:[['Primal Groudon','Mega Garchomp','Mega Swampert'],['Groudon','Garchomp','Rhyperior']],
  Rock:[['Mega Diancie','Mega Tyranitar','Mega Aerodactyl'],['Rampardos','Rhyperior','Tyrantrum']],
  Electric:[['Mega Manectric','Mega Ampharos','Mega Raikou'],['Xurkitree','Zekrom','Raikou']],
  Grass:[['Mega Sceptile','Mega Venusaur','Mega Abomasnow'],['Kartana','Roserade','Zarude']],
  Fire:[['Mega Blaziken','Mega Charizard Y','Mega Houndoom'],['Reshiram','Blaziken','Chandelure']],
  Ice:[['Mega Glalie','Mega Abomasnow','Mega Rayquaza'],['Mamoswine','Galarian Darmanitan','Weavile']],
  Poison:[['Mega Gengar','Mega Beedrill','Mega Venusaur'],['Nihilego','Overqwil','Roserade']],
  Flying:[['Mega Rayquaza','Mega Pidgeot','Mega Salamence'],['Rayquaza','Staraptor','Yveltal']],
  Bug:[['Mega Scizor','Mega Beedrill','Mega Pinsir'],['Volcarona','Pheromosa','Genesect']],
  Psychic:[['Mega Mewtwo Y','Mega Alakazam','Mega Gardevoir'],['Mewtwo','Hoopa Unbound','Metagross']],
  Ghost:[['Mega Gengar','Mega Banette','Mega Sableye'],['Dawn Wings Necrozma','Gengar','Chandelure']],
  Dark:[['Mega Tyranitar','Mega Houndoom','Mega Absol'],['Darkrai','Hydreigon','Tyranitar']],
  Steel:[['Mega Lucario','Mega Metagross','Mega Scizor'],['Metagross','Dusk Mane Necrozma','Lucario']],
  Dragon:[['Mega Rayquaza','Mega Garchomp','Mega Salamence'],['Rayquaza','Palkia Origin','Dialga Origin']],
  Fairy:[['Mega Gardevoir','Mega Diancie','Mega Mawile'],['Gardevoir','Togekiss','Xerneas']]
};
function raidDetails(r){
  const types=(r.types||[]).map(x=>String(x?.name||x?.type||x).trim()).filter(Boolean);
  const weak=[];
  Object.keys(RAID_WEAK).forEach(atk=>{
    let mult=1;
    types.forEach(def=>{
      if((RAID_WEAK[def]||[]).includes(atk)) mult*=1.6;
      const resist={Normal:['Rock','Steel','Ghost'],Fire:['Fire','Water','Rock','Dragon'],Water:['Water','Grass','Dragon'],Electric:['Electric','Grass','Dragon'],Grass:['Fire','Grass','Poison','Flying','Bug','Dragon','Steel'],Ice:['Fire','Water','Ice','Steel'],Fighting:['Poison','Flying','Psychic','Bug','Fairy'],Poison:['Poison','Ground','Rock','Ghost','Steel'],Ground:['Grass','Bug','Flying'],Flying:['Electric','Rock','Steel'],Psychic:['Psychic','Steel','Dark'],Bug:['Fire','Fighting','Poison','Flying','Ghost','Steel','Fairy'],Rock:['Fighting','Ground','Steel'],Ghost:['Dark','Normal'],Dragon:['Steel','Fairy'],Dark:['Fighting','Dark','Fairy'],Steel:['Fire','Water','Electric','Steel'],Fairy:['Fire','Poison','Steel']};
      if((resist[atk]||[]).includes(def)) mult*=def==='Ghost'&&atk==='Normal'?0.39:1/1.6;
    });
    if(mult>1) weak.push([atk,mult]);
  });
  weak.sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0]));
  return weak;
}
async function raids(){let b=$('raids');try{let raw=await get(U.raids,60000),n=[],sh=[];Object.entries(raw||{}).forEach(([g,ls])=>(Array.isArray(ls)?ls:[]).forEach(r=>(/^Shadow/i.test(r.name)?sh:n).push({...r,g})));let tier=r=>{let t=String(r.tier||r.g||'').toLowerCase();return t.includes('mega')?'Mega':t.includes('5')?'5-stjernet':t.includes('3')?'3-stjernet':'1-stjernet'},players=r=>r.recommended_players??r.recommendedPlayers??r.min_players??r.minPlayers??(tier(r)==='Mega'?'5+':tier(r)==='5-stjernet'?'4–6':tier(r)==='3-stjernet'?'2–3':'1'),draw=r=>`<div class="card click" data-r="${encodeURIComponent(JSON.stringify(r))}"><div class=row><div class=img>${r.asset_url?`<img src="${E(r.asset_url)}">`:'⚔️'}</div><div class=grow><div class=name>${E(r.name)}</div><div class=small>${E((r.types||[]).join(' · '))} · ✨ ${E(shiny(r,null))}</div></div>›</div><div class=stats><div class=stat><b>${players(r)}</b><span>Spillere</span></div><div class=stat><b>${r.cp_range?.max??'—'}</b><span>Hundo CP</span></div><div class=stat><b>${r.boosted_cp_range?.max??'—'}</b><span>Boost hundo</span></div></div></div>`;let group=(arr)=>{let h='';['1-stjernet','3-stjernet','5-stjernet','Mega'].forEach(t=>{let q=arr.filter(r=>tier(r)===t);if(q.length)h+=`<div class=section>${t}</div>`+q.map(draw).join('')});return h};b.innerHTML=`<div class="raid-tabs"><button class="raid-tab active" data-raid-tab="normal">Mega / normale</button><button class="raid-tab" data-raid-tab="shadow">Shadow</button></div><div id="raid-normal">${group(n)}</div><div id="raid-shadow" style="display:none">${group(sh)}</div>`;let tabs=b.querySelectorAll('[data-raid-tab]');tabs.forEach(x=>x.onclick=()=>{let shadow=x.dataset.raidTab==='shadow';tabs.forEach(t=>t.classList.toggle('active',t===x));$('raid-normal').style.display=shadow?'none':'';$('raid-shadow').style.display=shadow?'':'none'});b.querySelectorAll('[data-r]').forEach(x=>x.onclick=()=>{let r=JSON.parse(decodeURIComponent(x.dataset.r)),weak=raidDetails(r),groups={};weak.forEach(([type,m])=>{groups[type]=RAID_COUNTERS[type]||[[],[]]});let weakness=weak.length?weak.map(([t,m])=>`${t}${m>=2.5?' (2× svaghed)':m>1.5?' (svag)': ' (svag)'}`).join(' · '):'Ingen svagheder fundet';let mega=[...new Set(weak.flatMap(([t])=>groups[t][0]))].slice(0,6),non=[...new Set(weak.flatMap(([t])=>groups[t][1]))].slice(0,6);open(`<h2>${E(r.name)}</h2><div class=small>${players(r)} spillere</div><div class=section>Type</div><div class=card>${E((r.types||[]).join(' · ')||'Ikke oplyst')}</div><div class=section>Gode mod den</div><div class=card><b>Svag mod:</b> ${E(weakness)}<div class=section>Mega / Primal</div>${mega.length?mega.map(v=>`<div class=small>• ${E(v)}</div>`).join(''):'<div class=small>Ingen specifikke Mega/Primal fundet.</div>'}<div class=section>Ikke Mega</div>${non.length?non.map(v=>`<div class=small>• ${E(v)}</div>`).join(''):'<div class=small>Ingen specifikke counters fundet.</div>'}</div><div class=section>Shiny-chance</div><div class=card>✨ ${E(shiny(r,null))}</div><div class=stats><div class=stat><b>${r.cp_range?.max??'—'}</b><span>Hundo CP</span></div><div class=stat><b>${r.boosted_cp_range?.max??'—'}</b><span>Boost hundo</span></div><div class=stat><b>${r.shiny_available===true?'Mulig':'Ikke angivet'}</b><span>Shiny</span></div></div>`)});up()}catch(e){b.innerHTML='<div class=note>Kunne ikke hente raids.</div>'}}
'''
s=s[:start]+new+s[end:]
p.write_text(s)
