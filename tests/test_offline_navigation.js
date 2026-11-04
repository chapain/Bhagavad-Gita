// Exercise the generated service worker's navigation routing without a browser.
// Real service-worker lifecycle and offline loading are covered by browser_checks.py.
const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const handlers = {};
const base = 'https://example.test/Bhagavad-Gita/';
const entries = new Map();
let online = true, status = 200;
const cache = {
  put: async (key, response) => entries.set(new URL(typeof key === 'string' ? key : key.url, base).href, response),
  match: async key => entries.get(new URL(typeof key === 'string' ? key : key.url, base).href),
  /* the fake body is the resolved URL, so a hit proves WHICH page came back */
  add: async key => { const u = new URL(typeof key === 'string' ? key : key.url, base).href;
    entries.set(u, response(u)); },
};
const caches = {open: async () => cache, match: key => cache.match(key)};
function response(body, code = 200) {
  return {body, status: code, ok: code >= 200 && code < 300, type: 'basic', clone() { return response(body, code); }};
}
vm.runInNewContext(fs.readFileSync('sw.js', 'utf8'), {
  self: {addEventListener: (name, fn) => handlers[name] = fn, skipWaiting: () => {}},
  caches, URL, location: {href: base + 'sw.js', origin: 'https://example.test'},
  Response: class { constructor(body, opts) { this.body = body; this.status = opts.status; } },
  fetch: async req => { if (!online) throw Error('offline'); return response(req.url, status); },
});
async function navigate(path) {
  let result;
  handlers.fetch({request: {method: 'GET', mode: 'navigate', url: base + path},
    respondWith: p => { result = p; }});
  return result;
}
(async () => {
  /* install: the worker precaches ASSETS, exactly as a browser would run it */
  let installing;
  handlers.install({waitUntil: promise => { installing = promise; }});
  await installing;
  assert.ok(entries.has(base + 'method/'),
            'install must precache the method page under its own URL');

  await navigate('');
  await navigate('chapter/1/');
  status = 404;
  await navigate('chapter/2/');
  status = 200;
  online = false;
  assert.strictEqual((await navigate('chapter/1/')).body, base + 'chapter/1/');
  assert.strictEqual((await navigate('chapter/2/')).status, 504);
  assert.strictEqual((await navigate('')).body, base);
  assert.strictEqual((await navigate('unknown/')).status, 504);

  /* The method page is precached, so it must open offline — by its own URL and
     nothing else. Before this, a precached page still fell through to the 504:
     only the root and chapter navigations ever consulted the cache. */
  assert.strictEqual((await navigate('method/')).body, base + 'method/',
                     'a precached page must open offline under its own URL');

  /* Any page the reader actually visited is kept under its own address too... */
  online = true;
  await navigate('notes/');
  online = false;
  assert.strictEqual((await navigate('notes/')).body, base + 'notes/',
                     'a visited page is served back offline under its own URL');

  /* ...but a page never visited, and never precached, still gets the honest 504
     rather than some other page pretending to be it. */
  assert.strictEqual((await navigate('never-visited/')).status, 504);
  assert.strictEqual((await navigate('chapter/7/')).status, 504,
                     'an unvisited chapter must not become a visited one offline');

  console.log('offline navigation: visited chapter, root and precached method page cached separately; '
            + 'unvisited, error and unknown pages do not masquerade as the app');
})().catch(err => { console.error(err); process.exitCode = 1; });
