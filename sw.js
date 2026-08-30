const CACHE = 'pogo-uge-v4';
const SHELL = ['./manifest.json', './icon.svg'];

self.addEventListener('install', (event) => {
  // Bypass any HTTP cache when precaching, so we always grab fresh files
  event.waitUntil(
    caches.open(CACHE).then(cache =>
      Promise.all(SHELL.map(url => fetch(url, { cache: 'reload' }).then(res => cache.put(url, res))))
    )
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  // Clean out any old cache versions from previous app updates
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  const url = event.request.url;

  // Live data: always go straight to the network, never cached
  if(url.includes('raw.githubusercontent.com')){
    event.respondWith(fetch(event.request));
    return;
  }

  // The app page itself (index.html / navigations): network-first.
  // This is the key fix — it means every time you open the app it tries
  // to fetch the latest version first, and only falls back to the old
  // cached copy if you're completely offline.
  if(event.request.mode === 'navigate' || url.endsWith('index.html') || url.endsWith('/')){
    event.respondWith(
      fetch(event.request, { cache: 'no-store' })
        .then(res => {
          caches.open(CACHE).then(cache => cache.put(event.request, res.clone()));
          return res;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Other static assets (icon, manifest): cache-first, fall back to network
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request))
  );
});
