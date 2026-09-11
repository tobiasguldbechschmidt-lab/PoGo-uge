const CACHE_NAME = "pogo-uge-v7";
const APP_SHELL = ["./","./index.html","./manifest.json","./icon.svg"];
self.addEventListener("install", e => e.waitUntil(caches.open(CACHE_NAME).then(c => c.addAll(APP_SHELL)).then(() => self.skipWaiting())));
self.addEventListener("activate", e => e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", e => {
  const r=e.request;
  if(r.method!=="GET") return;
  const u=new URL(r.url);
  if(u.hostname==="raw.githubusercontent.com" || u.pathname.endsWith(".json")){
    e.respondWith(fetch(r).catch(()=>new Response(JSON.stringify({error:true,offline:true}),{status:503,headers:{"Content-Type":"application/json"}})));return;
  }
  if(r.mode==="navigate" || r.destination==="document"){
    e.respondWith(fetch(r).then(async response=>{
      if(!response.ok) return response;
      let text=await response.text();
      text=text.replace("async function preload(){if(!cache.events)cache.events=get(URL.events).catch(()=>null)}preload();","async function preload(){if(!cache.events)cache.events=await get(URL.events).catch(()=>null)}preload();");
      const out=new Response(text,{status:response.status,statusText:response.statusText,headers:response.headers});
      const copy=out.clone();caches.open(CACHE_NAME).then(c=>c.put(r,copy));return out;
    }).catch(()=>caches.match(r).then(c=>c||caches.match("./index.html"))));return;
  }
  e.respondWith(caches.match(r).then(c=>c||fetch(r).then(response=>{if(response.ok&&u.origin===self.location.origin){const copy=response.clone();caches.open(CACHE_NAME).then(c=>c.put(r,copy))}return response}))); 
});