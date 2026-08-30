/* sw.js — offline cache for the Bhagavad Gita study app.
   Strategy: cache-first for the shell (the app is one static file and never
   changes between deploys), with a network revalidation for navigations so a
   new deploy is picked up on the next visit. */
const CACHE = 'gita-111a15446eb3';
const ASSETS = ['./', './index.html', './manifest.webmanifest',
                './icon-192.png', './icon-512.png', './icon-maskable-512.png',
                './apple-touch-icon.png', './favicon.ico',
                './data/ch1.js', './data/ch2.js', './data/ch3.js', './data/ch4.js', './data/ch5.js', './data/ch6.js', './data/ch7.js', './data/ch8.js', './data/ch9.js', './data/ch10.js', './data/ch11.js', './data/ch12.js', './data/ch13.js', './data/ch14.js', './data/ch15.js', './data/ch16.js', './data/ch17.js', './data/ch18.js'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE)
    .then(c => c.addAll(ASSETS))
    .then(() => self.skipWaiting())
    .catch(() => self.skipWaiting()));   // a missing optional asset must not abort install
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
        .catch(() => caches.match('./index.html').then(r => r || caches.match('./')))
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
    }).catch(() => hit))
  );
});
