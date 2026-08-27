const CACHE = 'pogo-uge-v1';
const SHELL = ['./index.html', './manifest.json', './icon.svg'];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = event.request.url;
  // Always go to network for the live event data so it's never stale
  if(url.includes('raw.githubusercontent.com')){
    event.respondWith(fetch(event.request));
    return;
  }
  // App shell: cache-first, fall back to network
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request))
  );
});
