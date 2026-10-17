/* sw.js — offline cache for the Bhagavad Gita study app.
   Strategy: cache-first for the shell (the app is one static file and never
   changes between deploys), with a network revalidation for navigations so a
   new deploy is picked up on the next visit. */
const CACHE = 'gita-302930416ac2';
/* chapter.css is precached even though the app itself never loads it: a reader
   who arrives on a /chapter/N/ landing page and later opens it offline would
   otherwise get an unstyled wall of text, while the manifest and README both
   promise "Works offline". The chapter PAGES stay out of the precache on
   purpose (18 of them, ~1.3 MB) — the runtime handler below caches whichever
   ones the reader actually visits, and now their stylesheet and its Devanagari
   font are always there. The font is a real file rather than a data: URI, so
   it is fetched once and shared by all 18 pages — but that also means it is a
   network request, which offline would fail without this line. */
const ASSETS = ['./', './index.html', './manifest.webmanifest',
                './icon-192.png', './icon-512.png', './icon-maskable-512.png',
                './apple-touch-icon.png', './favicon.ico', './chapter.css',
                './noto-deva-regular.woff2', './noto-deva-bold.woff2',
                './data/ch1.js', './data/ch2.js', './data/ch3.js', './data/ch4.js', './data/ch5.js', './data/ch6.js', './data/ch7.js', './data/ch8.js', './data/ch9.js', './data/ch10.js', './data/ch11.js', './data/ch12.js', './data/ch13.js', './data/ch14.js', './data/ch15.js', './data/ch16.js', './data/ch17.js', './data/ch18.js'];

self.addEventListener('install', e => {
  /* addAll() is atomic — if even one optional asset 404s nothing is cached,
     while install still "succeeds" and the app silently loses its offline
     promise. Add each URL on its own: one bad asset costs that asset, not
     the whole cache, and install still never aborts. */
  e.waitUntil(caches.open(CACHE)
    .then(c => Promise.all(ASSETS.map(u => c.add(u).catch(() => undefined))))
    .then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;   // never touch cross-origin requests

  // The service worker script itself MUST come from the network every time, or
  // the browser can never discover a new worker and the cache pins itself
  // forever across deploys (typical "stuck SW" bug).
  if (url.pathname.endsWith('/sw.js') || url.pathname.endsWith('\sw.js')) {
    e.respondWith(fetch(req).catch(() => caches.match(req)));
    return;
  }

  if (req.mode === 'navigate') {
    // network-first for the page itself, so updates land; fall back to cache offline.
    // Only the app root is stored as the shell: caching any other page (e.g. a
    // /chapter/N/ landing page) as './index.html' would poison the offline fallback.
    e.respondWith(
      fetch(req)
        .then(res => {
          const u = new URL(req.url), root = new URL('./', location.href).pathname;
          if (u.pathname === root || u.pathname === root + 'index.html') {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put('./index.html', copy));
          }
          return res; })
        .catch(() => caches.match('./index.html').then(r => r || caches.match('./'))
          .then(r => r || new Response(
            '<!doctype html><meta charset="utf-8"><title>Offline</title>' +
            '<p>You are offline and this page is not cached yet. Reconnect and reload.</p>',
            { status: 504, headers: { 'Content-Type': 'text/html; charset=utf-8' } })))
    );
    return;
  }
  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      if (res && res.status === 200 && res.type === 'basic') {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => hit || new Response('', { status: 504, statusText: 'Offline' })))
  );
});
