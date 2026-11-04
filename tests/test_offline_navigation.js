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
};
const caches = {open: async () => cache, match: key => cache.match(key)};
function response(body, code = 200) {
  return {body, status: code, ok: code >= 200 && code < 300, type: 'basic', clone() { return response(body, code); }};
}
vm.runInNewContext(fs.readFileSync('sw.js', 'utf8'), {
  self: {addEventListener: (name, fn) => handlers[name] = fn},
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
  console.log('offline navigation: visited chapter and root cached separately; unvisited, error and unknown pages do not masquerade as the app');
})().catch(err => { console.error(err); process.exitCode = 1; });
