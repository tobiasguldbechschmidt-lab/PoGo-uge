<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>GO Uge</title>

<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="GO Uge">
<meta name="theme-color" content="#0d1b2a">
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icon.svg">

<style>
  :root{
    --bg:#0d1b2a;
    --card:#14263b;
    --card2:#1b3350;
    --red:#e3350d;
    --gold:#ffcb05;
    --text:#eef3f8;
    --muted:#9fb3c8;
    --line:#22405f;
    --purple:#a78bfa;
    --blue:#5fb3f0;
  }
  *{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
  html,body{height:100%;}
  body{
    margin:0;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", sans-serif;
    background: radial-gradient(circle at 50% -10%, #1b3350 0%, var(--bg) 60%);
    color:var(--text);
    min-height:100vh;
    padding: max(16px, env(safe-area-inset-top)) 14px max(16px, env(safe-area-inset-bottom));
    display:flex;
    align-items:flex-start;
    justify-content:center;
  }

  .app{ width:100%; max-width:420px; }

  .card{
    background:var(--card);
    border-radius:20px;
    border:1px solid var(--line);
    box-shadow:0 20px 60px rgba(0,0,0,0.4);
    overflow:hidden;
  }

  .header{
    position:relative;
    padding:18px 18px 0;
    background: linear-gradient(180deg, rgba(227,53,13,0.18), rgba(227,53,13,0) 70%);
    border-bottom:1px solid var(--line);
  }
  .header-row{ display:flex; align-items:center; gap:10px; }
  .pokeball{
    width:32px;height:32px;border-radius:50%;
    background: linear-gradient(var(--red) 0 47%, #0d1b2a 47% 53%, #fff 53% 100%);
    border:2px solid #0d1b2a;
    position:relative; flex:none;
  }
  .pokeball::after{
    content:""; position:absolute; top:50%; left:50%;
    width:9px;height:9px; background:#fff; border:2px solid #0d1b2a;
    border-radius:50%; transform:translate(-50%,-50%);
  }
  h1{ margin:0; font-size:18px; font-weight:700; }
  .refresh-btn{
    margin-left:auto;
    width:30px;height:30px;border-radius:50%;
    background:var(--card2); border:1px solid var(--line);
    color:var(--muted); display:flex; align-items:center; justify-content:center;
    cursor:pointer; font-size:14px;
  }
  .refresh-btn.spinning svg{ animation: spin 0.8s linear infinite; }
  @keyframes spin{ from{transform:rotate(0)} to{transform:rotate(360deg)} }
  .subtitle{ margin:12px 0 14px; font-size:12px; color:var(--muted); }

  .tabs{
    display:flex; gap:4px;
    padding:0 18px;
    margin-top:4px;
  }
  .tab{
    flex:1;
    text-align:center;
    padding:9px 0 11px;
    font-size:13px;
    font-weight:600;
    color:var(--muted);
    border-bottom:2px solid transparent;
    cursor:pointer;
  }
  .tab.active{
    color:var(--gold);
    border-bottom-color:var(--gold);
  }

  .panel{ display:none; }
  .panel.active{ display:block; }

  .list{ padding:6px 16px 16px; }
  .status{ padding:30px 10px; text-align:center; color:var(--muted); font-size:13px; }

  .day-group{ margin-top:14px; }
  .day-label{
    font-size:11px; text-transform:uppercase; letter-spacing:0.8px;
    color:var(--gold); font-weight:700; margin:0 0 6px 2px;
    display:flex; align-items:baseline; gap:6px;
  }
  .day-label .count{
    color:var(--muted); font-weight:500; text-transform:none; letter-spacing:0;
  }
  .day-empty{
    font-size:12px; color:var(--muted); padding:2px 2px 2px;
  }

  .event{
    display:flex; gap:12px;
    background:var(--card2); border:1px solid var(--line);
    border-radius:14px; padding:11px 12px; margin-bottom:8px;
    text-decoration:none; color:inherit;
  }
  .event-dot{ width:8px;height:8px;border-radius:50%; background:var(--red); margin-top:6px; flex:none; }
  .event.ongoing .event-dot{ background:var(--gold); }
  .event-body{ min-width:0; }
  .event-title{ font-size:14px; font-weight:600; margin:0 0 2px; }
  .event-time{ font-size:11.5px; color:var(--muted); margin:0 0 4px; }
  .event-type{ font-size:11px; color:#c4d3e2; margin:0; text-transform:capitalize; }

  /* Raid tier groups */
  .tier-group{ margin-top:14px; }
  .tier-label{
    font-size:11px; text-transform:uppercase; letter-spacing:0.8px;
    font-weight:700; margin:0 0 6px 2px;
    display:flex; align-items:center; gap:6px;
  }
  .tier-badge{
    display:inline-flex; align-items:center; justify-content:center;
    min-width:20px; height:20px; padding:0 5px;
    border-radius:6px;
    font-size:11px; font-weight:800;
    background:var(--gold); color:#28230a;
  }
  .tier-badge.mega{ background:var(--purple); color:#1c1330; }
  .tier-badge.tier5{ background:var(--blue); color:#0a2233; }

  .boss-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px;
  }
  .boss-card{
    background:var(--card2); border:1px solid var(--line);
    border-radius:14px; padding:10px 11px;
  }
  .boss-name{ font-size:13.5px; font-weight:600; margin:0 0 3px; display:flex; align-items:center; gap:5px; }
  .boss-name .shiny{ font-size:11px; }
  .boss-type{ font-size:10.5px; color:var(--muted); margin:0; text-transform:capitalize; }
  .boss-cp{ font-size:10px; color:#8fa3ba; margin:3px 0 0; }

  .footer{
    padding:10px 16px 14px; border-top:1px solid var(--line);
    font-size:10.5px; color:var(--muted); text-align:center;
  }
  .footer span{ display:block; margin-top:2px; }

  ::-webkit-scrollbar{ width:6px; }
  ::-webkit-scrollbar-thumb{ background:var(--line); border-radius:3px; }
</style>
</head>
<body>

<div class="app">
  <div class="card">
    <div class="header">
      <div class="header-row">
        <div class="pokeball"></div>
        <h1 id="titleText">Denne uge i GO</h1>
        <div class="refresh-btn" id="refreshBtn" title="Opdater">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M21 12a9 9 0 1 1-2.6-6.4M21 4v5h-5"/>
          </svg>
        </div>
      </div>
      <p class="subtitle" id="subtitle">Henter friske data …</p>
      <div class="tabs">
        <div class="tab active" data-tab="week">Denne uge</div>
        <div class="tab" data-tab="raids">Raids nu</div>
      </div>
    </div>

    <div class="panel active" id="panel-week">
      <div class="list" id="listWeek">
        <div class="status">Henter kommende events …</div>
      </div>
    </div>

    <div class="panel" id="panel-raids">
      <div class="list" id="listRaids">
        <div class="status">Henter aktuelle raid-bosses …</div>
      </div>
    </div>

    <div class="footer" id="footerText">
      Data: LeekDuck.com via ScrapedDuck
      <span id="updatedAt"></span>
    </div>
  </div>
</div>

<script>
const EVENTS_URL = "https://raw.githubusercontent.com/bigfoott/ScrapedDuck/data/events.json";
const RAIDS_URL = "https://pogoapi.net/api/v1/raid_bosses.json";

const refreshBtn = document.getElementById('refreshBtn');
const subtitleEl = document.getElementById('subtitle');
const titleEl = document.getElementById('titleText');
const footerEl = document.getElementById('footerText');
const updatedEl = document.getElementById('updatedAt');
const tabs = document.querySelectorAll('.tab');
const panels = { week: document.getElementById('panel-week'), raids: document.getElementById('panel-raids') };

let currentTab = 'week';

const dayNamesShort = ['Søndag','Mandag','Tirsdag','Onsdag','Torsdag','Fredag','Lørdag'];
const monthNames = ['jan','feb','mar','apr','maj','jun','jul','aug','sep','okt','nov','dec'];

function startOfDay(d){ const x = new Date(d); x.setHours(0,0,0,0); return x; }
function endOfDay(d){ const x = new Date(d); x.setHours(23,59,59,999); return x; }
function fmtTime(date){ return date.getHours().toString().padStart(2,'0') + ':' + date.getMinutes().toString().padStart(2,'0'); }
function fmtDate(date){ return date.getDate() + '. ' + monthNames[date.getMonth()].toUpperCase(); }
function sameDay(a,b){ return a.toDateString() === b.toDateString(); }
function escapeHtml(str){ const d = document.createElement('div'); d.textContent = str; return d.innerHTML; }
function titleCase(s){ return (s||'').toLowerCase().replace(/(^|\s)\S/g, c => c.toUpperCase()); }

// ---------- Tabs ----------
tabs.forEach(tab => {
  tab.addEventListener('click', () => {
    tabs.forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    Object.values(panels).forEach(p => p.classList.remove('active'));
    currentTab = tab.dataset.tab;
    panels[currentTab].classList.add('active');
    updateHeaderForTab();
  });
});

function updateHeaderForTab(){
  if(currentTab === 'week'){
    titleEl.textContent = 'Denne uge i GO';
    footerEl.firstChild.textContent = 'Data: LeekDuck.com via ScrapedDuck ';
  } else {
    titleEl.textContent = 'Aktuelle raids';
    footerEl.firstChild.textContent = 'Data: PoGoAPI.net ';
  }
}

// ---------- Events (This Week) ----------
const SKIP_TYPES = ['season', 'update'];
const MAX_EVENT_SPAN_DAYS = 20;

async function loadEvents(){
  const listEl = document.getElementById('listWeek');
  try{
    const res = await fetch(EVENTS_URL + '?t=' + Date.now(), {cache:'no-store'});
    if(!res.ok) throw new Error('HTTP ' + res.status);
    const raw = await res.json();
    const now = new Date();

    const events = raw
      .filter(e => !SKIP_TYPES.includes(e.eventType))
      .map(e => ({ ...e, startDate: e.start ? new Date(e.start) : null, endDate: e.end ? new Date(e.end) : null }))
      .filter(e => {
        if(!e.startDate && !e.endDate) return false;
        if(e.startDate && e.endDate){
          const spanDays = (e.endDate - e.startDate) / (1000*60*60*24);
          if(spanDays > MAX_EVENT_SPAN_DAYS) return false;
        }
        return true;
      });

    const days = [];
    for(let i=0;i<7;i++){ const d = new Date(now); d.setDate(d.getDate() + i); days.push(d); }

    renderWeek(events, days, now, listEl);
    return true;
  }catch(err){
    listEl.innerHTML = '<div class="status">Kunne ikke hente data lige nu.<br>Tjek din forbindelse og prøv igen.</div>';
    console.error(err);
    return false;
  }
}

function eventTimeLabel(e, day, now){
  const start = e.startDate, end = e.endDate;
  const dayStart = startOfDay(day), dayEnd = endOfDay(day);
  const startsToday = start && sameDay(start, day);
  const endsToday = end && sameDay(end, day);
  const startedBefore = start && start < dayStart;
  const endsAfter = end && end > dayEnd;

  if(startsToday && endsToday) return fmtTime(start) + '–' + fmtTime(end);
  if(startsToday && !end) return 'Fra ' + fmtTime(start);
  if(startsToday && endsAfter) return 'Fra ' + fmtTime(start) + ' · kører til ' + fmtDate(end);
  if(startedBefore && endsToday) return 'Slutter kl. ' + fmtTime(end);
  if(startedBefore && !end) return 'Løbende';
  if(startedBefore && endsAfter) return 'Kører hele dagen';
  if(start && !end) return fmtTime(start);
  return '';
}

function renderWeek(events, days, now, listEl){
  let html = '';
  let totalShown = 0;

  days.forEach((day, idx) => {
    const dayStart = startOfDay(day), dayEnd = endOfDay(day);
    const todaysEvents = events
      .filter(e => {
        const s = e.startDate || e.endDate;
        const en = e.endDate || e.startDate;
        return s <= dayEnd && en >= dayStart;
      })
      .sort((a,b) => (a.startDate ? a.startDate.getTime() : -Infinity) - (b.startDate ? b.startDate.getTime() : -Infinity));

    const label = idx === 0 ? 'I dag' : idx === 1 ? 'I morgen' : dayNamesShort[day.getDay()];
    html += `<div class="day-group"><p class="day-label">${label} <span class="count">· ${fmtDate(day)}</span></p>`;

    if(todaysEvents.length === 0){
      html += `<p class="day-empty">Ingen events</p>`;
    } else {
      todaysEvents.forEach(e => {
        const ongoing = e.startDate && e.startDate < dayStart;
        const timeStr = eventTimeLabel(e, day, now);
        html += `
          <a class="event ${ongoing ? 'ongoing' : ''}" href="${e.link || '#'}" target="_blank" rel="noopener">
            <div class="event-dot"></div>
            <div class="event-body">
              <p class="event-title">${escapeHtml(e.name || 'Event')}</p>
              <p class="event-time">${timeStr}</p>
              <p class="event-type">${escapeHtml((e.heading || e.eventType || '').replace(/-/g,' '))}</p>
            </div>
          </a>`;
        totalShown++;
      });
    }
    html += `</div>`;
  });

  listEl.innerHTML = totalShown === 0 ? '<div class="status">Ingen events fundet i den kommende uge.</div>' : html;
}

// ---------- Raids ----------
const TIER_ORDER = ['5','mega','4','3','2','1'];
const TIER_LABELS = { '1':'Tier 1', '2':'Tier 2', '3':'Tier 3', '4':'Tier 4', '5':'Tier 5', 'mega':'Mega', '6':'Tier 6' };

async function loadRaids(){
  const listEl = document.getElementById('listRaids');
  try{
    const res = await fetch(RAIDS_URL + '?t=' + Date.now(), {cache:'no-store'});
    if(!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    renderRaids(data.current || {}, listEl);
    return true;
  }catch(err){
    listEl.innerHTML = '<div class="status">Kunne ikke hente raid-data lige nu.<br>Tjek din forbindelse og prøv igen.</div>';
    console.error(err);
    return false;
  }
}

function renderRaids(current, listEl){
  let html = '';
  let totalShown = 0;

  TIER_ORDER.forEach(tier => {
    const bosses = current[tier];
    if(!bosses || bosses.length === 0) return;

    const badgeClass = tier === 'mega' ? 'mega' : (tier === '5' ? 'tier5' : '');
    html += `<div class="tier-group">
      <p class="tier-label"><span class="tier-badge ${badgeClass}">${TIER_LABELS[tier] || tier}</span></p>
      <div class="boss-grid">`;

    bosses.forEach(b => {
      const shiny = b.possible_shiny ? '<span class="shiny">✨</span>' : '';
      const types = (b.type || []).map(t => titleCase(t)).join(' / ');
      html += `
        <div class="boss-card">
          <p class="boss-name">${escapeHtml(b.name || 'Ukendt')}${shiny}</p>
          <p class="boss-type">${escapeHtml(types)}</p>
          <p class="boss-cp">CP ${b.min_unboosted_cp || '?'}–${b.max_boosted_cp || '?'}</p>
        </div>`;
      totalShown++;
    });

    html += `</div></div>`;
  });

  listEl.innerHTML = totalShown === 0 ? '<div class="status">Ingen aktuelle raid-bosses fundet.</div>' : html;
}

// ---------- Load both, refresh, visibility ----------
async function loadAll(isManual){
  if(isManual) refreshBtn.classList.add('spinning');
  subtitleEl.textContent = 'Henter friske data …';
  const [weekOk, raidsOk] = await Promise.all([loadEvents(), loadRaids()]);
  const now = new Date();
  if(weekOk || raidsOk){
    subtitleEl.textContent = currentTab === 'week' ? 'I dag til om 7 dage' : 'Opdateres løbende gennem dagen';
  } else {
    subtitleEl.textContent = 'Fejl ved hentning';
  }
  updatedEl.textContent = 'Opdateret ' + now.toLocaleDateString('da-DK') + ' ' + fmtTime(now);
  if(isManual) refreshBtn.classList.remove('spinning');
}

refreshBtn.addEventListener('click', () => loadAll(true));
loadAll(false);

document.addEventListener('visibilitychange', () => {
  if(document.visibilityState === 'visible') loadAll(false);
});

if('serviceWorker' in navigator){
  navigator.serviceWorker.register('sw.js').catch(()=>{});
}
</script>
</body>
</html>
