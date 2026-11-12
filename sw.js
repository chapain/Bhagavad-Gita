/* sw.js — offline cache for the Bhagavad Gita study app.
   Strategy: cache-first for the shell (the app is one static file and never
   changes between deploys), with a network revalidation for navigations so a
   new deploy is picked up on the next visit. */
const CACHE = 'gita-c13d94d99910';
/* chapter.css is precached even though the app itself never loads it: a reader
   who arrives on a /chapter/N/ landing page and later opens it offline would
   otherwise get an unstyled wall of text, while the manifest and README both
   promise "Works offline". The chapter PAGES stay out of the precache on
   purpose (18 of them, ~1.3 MB) — the runtime handler below caches whichever
   ones the reader actually visits, and now their stylesheet and its Devanagari
   font are always there. The font is a real file rather than a data: URI, so
   it is fetched once and shared by all 18 pages — but that also means it is a
   network request, which offline would fail without this line. */
/* './method/' is precached for the same reason as chapter.css: it is the one
   static page the app links to, it is small, and "works offline" is a promise
   made on the welcome screen. The navigation handler serves it back by exact
   URL — see below. */
const ASSETS = ['./', './index.html', './manifest.webmanifest',
                './icons/icon-192.png', './icons/icon-512.png', './icons/icon-maskable-512.png',
                './icons/apple-touch-icon.png', './favicon.ico', './chapter.css',
                './noto-deva-regular.woff2', './noto-deva-bold.woff2',
                './method/', './data/ch1.js', './data/ch2.js', './data/ch3.js', './data/ch4.js', './data/ch5.js', './data/ch6.js', './data/ch7.js', './data/ch8.js', './data/ch9.js', './data/ch10.js', './data/ch11.js', './data/ch12.js', './data/ch13.js', './data/ch14.js', './data/ch15.js', './data/ch16.js', './data/ch17.js', './data/ch18.js'];

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
    // Cache successful chapter navigations under their own URL, never as the
    // app shell. An unvisited chapter must not silently become the app offline.
    // The same rule covers any other page in scope — the method page is
    // precached, and a page the reader visited is kept under its own address —
    // but only an EXACT url match is ever served back: offline never hands over
    // a different page than the one asked for.
    const root = new URL('./', location.href).pathname;
    const isRoot = url.pathname === root || url.pathname === root + 'index.html';
    const inScope = url.pathname.startsWith(root);
    const chapterPath = url.pathname.slice(root.length);
    const isChapter = inScope &&
      /^chapter\/(?:[1-9]|1[0-8])\/(?:index\.html)?$/.test(chapterPath);
    e.respondWith(fetch(req).then(res => {
      if (res.ok && res.type === 'basic' && (isRoot || inScope)) {
        const copy = res.clone();
        return caches.open(CACHE).then(c => c.put(isRoot ? './index.html' : req, copy))
          .catch(() => undefined).then(() => res);
      }
      return res;
    }).catch(() => caches.open(CACHE).then(c =>
      isRoot ? c.match('./index.html').then(r => r || c.match('./')) :
      c.match(req)
    ).then(r => r || new Response(
      '<!doctype html><meta charset="utf-8"><title>Offline</title>' +
      '<p>You are offline and this page is not cached yet. Reconnect and reload.</p>',
      { status: 504, headers: { 'Content-Type': 'text/html; charset=utf-8' } }))));
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
