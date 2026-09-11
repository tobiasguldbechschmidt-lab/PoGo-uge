const CACHE_NAME = "pogo-uge-v6";

const APP_SHELL = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icon.svg"
];

// Install: cache only the static app shell.
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
});

// Activate: remove old app caches and take control immediately.
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key !== CACHE_NAME)
            .map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

// Fetch strategy:
// - HTML/navigation: network first, cache fallback.
// - Static files: cache first, then network.
// - Live JSON data: network only, so the app gets fresh data.
self.addEventListener("fetch", (event) => {
  const request = event.request;

  // Only handle GET requests.
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // Never cache live data from the data repositories.
  const isLiveData =
    url.hostname === "raw.githubusercontent.com" ||
    url.pathname.endsWith(".json");

  if (isLiveData) {
    event.respondWith(
      fetch(request).catch(() =>
        new Response(
          JSON.stringify({
            error: true,
            offline: true,
            message: "Live data is unavailable offline."
          }),
          {
            status: 503,
            headers: { "Content-Type": "application/json" }
          }
        )
      )
    );
    return;
  }

  // HTML pages: always try the newest version first.
  if (request.mode === "navigate" || request.destination === "document") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, copy);
            });
          }
          return response;
        })
        .catch(() =>
          caches.match(request).then(
            (cached) => cached || caches.match("./index.html")
          )
        )
    );
    return;
  }

  // Static assets: use cache first, then fetch and cache.
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;

      return fetch(request).then((response) => {
        if (response.ok && url.origin === self.location.origin) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, copy);
          });
        }
        return response;
      });
    })
  );
});
