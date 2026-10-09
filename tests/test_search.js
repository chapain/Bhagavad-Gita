#!/usr/bin/env node
'use strict';
/* Focused regressions for the app's search-only normalization. These execute
   the emitted helpers (not a Python reimplementation) against shipped verses. */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert/strict');

const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const helperStart = html.indexOf('function normTxt(');
const helperEnd = html.indexOf('function fmtN(', helperStart);
assert(helperStart >= 0 && helperEnd > helperStart,
       'the built app must emit its search normalization helpers');
const searchContext = vm.createContext({});
vm.runInContext(html.slice(helperStart, helperEnd), searchContext);

const exactKey = searchContext.searchExactKey;
const foldedKey = searchContext.searchFoldKey;
const prepareQuery = searchContext.prepareSearchQuery;
const searchMatches = (text, query) => searchContext.searchTextMatches(
  exactKey(text), foldedKey(text), prepareQuery(query));

const data = [];
for (let n = 1; n <= 18; n++) {
  const raw = fs.readFileSync(path.join(ROOT, 'data', `ch${n}.js`), 'utf8');
  const match = raw.match(/^GITA_CH\[\d+\] = ([\s\S]*);\n$/);
  assert(match, `data/ch${n}.js must contain a JSON chapter payload`);
  data.push(JSON.parse(match[1]));
}
const verses = data.flatMap(ch => ch.themes.flatMap(theme =>
  theme.parts.flatMap(part => part.sutras)));
const displayRef = ref => ref.split('.').map(part => String(Number(part))).join('.');
function verse(ref) {
  const found = verses.find(item => displayRef(item.n) === ref);
  assert(found, `verse ${ref} must exist in the shipped data`);
  return found;
}

let passed = 0;
function test(name, fn) {
  fn();
  passed++;
  console.log('PASS:', name);
}

test('NFC and NFD spellings share the exact canonical key', () => {
  const nfc = 'kṛṣṇa';
  const nfd = nfc.normalize('NFD');
  assert.notEqual(nfc, nfd, 'fixture must exercise different Unicode forms');
  assert.equal(exactKey(nfc), exactKey(nfd));
  assert(searchMatches(nfc, nfd));
  assert(searchMatches(nfd, nfc));
});

test('ASCII spellings find the intended Sanskrit verse text', () => {
  const cases = [
    ['krishna', '1.28'],
    ['karmanye vadhikaraste', '2.47'],
    ['dharmakshetre', '1.1'],
    ['yada yada hi dharmasya', '4.7'],
    ['sarvadharman parityajya', '18.66'],
  ];
  for (const [query, ref] of cases) {
    assert(searchMatches(verse(ref).t, query), `${query} should find ${ref}`);
  }
});

test('documented keyboard spellings fold only in the ASCII search path', () => {
  for (const [iast, ascii] of [
    ['śa', 'sha'], ['ṣa', 'sha'], ['ṛ', 'ri'], ['ca', 'cha'],
    ['ā', 'a'], ['ā', 'aa'], ['ī', 'i'], ['ī', 'ee'],
    ['ū', 'u'], ['ū', 'oo'], ['ṇ', 'n'],
  ]) {
    assert(searchMatches(iast, ascii), `${ascii} should find ${iast}`);
  }
  assert.equal(foldedKey('aa ee oo'), foldedKey('ā ī ū'));
});

test('explicit IAST queries preserve Sanskrit distinctions', () => {
  assert(!searchMatches('a', 'ā'), 'short and long a remain distinguishable');
  assert(!searchMatches('śa', 'ṣa'), 'ś and ṣ remain distinguishable');
  assert(!searchMatches('ta', 'ṭa'), 'dental t and retroflex ṭ remain distinguishable');
  assert(!searchMatches('śa', 'sa'), 's remains distinct from ś/ṣ');
  assert(searchMatches('śa', 'sha') && searchMatches('ṣa', 'sha'),
         'the documented ASCII sh spelling intentionally covers ś and ṣ');
});

test('13.27 retains its short-a IAST search spelling', () => {
  const text = verse('13.27').t;
  const correct = 'vinaśyatsvavinaśyantaṃ';
  const wrong = 'vinaśyatsvavināśyantaṃ';
  assert(text.includes(correct), '13.27 data keeps vinaśyatsvavinaśyantaṃ');
  assert(searchMatches(text, correct));
  assert(!searchMatches(text, wrong), 'the long-a spelling must not match precise IAST search');
});

test('result count labels use singular/plural wording in all three languages', () => {
  const start = html.indexOf('function resultCountLabel(');
  const end = html.indexOf('\nfunction announceView', start);
  assert(start >= 0 && end > start, 'resultCountLabel() must be emitted');
  const translations = {
    en: { result: 'result', results: 'results' },
    ne: { result: 'परिणाम', results: 'परिणामहरू' },
    hi: { result: 'परिणाम', results: 'परिणाम' },
  };
  const countContext = vm.createContext({ state: { lang: 'en' } });
  countContext.numL = n => String(n);
  countContext.L = key => translations[countContext.state.lang][key];
  vm.runInContext(html.slice(start, end), countContext);
  for (const [lang, one, many, none] of [
    ['en', '1 result', '2 results', '0 results'],
    ['ne', '1 परिणाम', '2 परिणामहरू', '0 परिणामहरू'],
    ['hi', '1 परिणाम', '2 परिणाम', '0 परिणाम'],
  ]) {
    countContext.state.lang = lang;
    assert.equal(countContext.resultCountLabel(1), one, `${lang}: singular`);
    assert.equal(countContext.resultCountLabel(2), many, `${lang}: plural`);
    assert.equal(countContext.resultCountLabel(0), none, `${lang}: zero uses plural`);
  }
});

test('search and favorites render counts through the grammar helper', () => {
  const searchStart = html.indexOf('function doSearch(){');
  const searchEnd = html.indexOf('\nfunction clearSearch(){', searchStart);
  const favStart = html.indexOf('function showFavorites(){');
  const favEnd = html.indexOf('\nfunction resultCountLabel', favStart);
  assert(searchStart >= 0 && searchEnd > searchStart, 'doSearch() must be emitted');
  assert(favStart >= 0 && favEnd > favStart, 'showFavorites() must be emitted');
  const searchCode = html.slice(searchStart, searchEnd);
  const favoritesCode = html.slice(favStart, favEnd);
  assert(searchCode.includes('resultCountLabel(0)'), 'zero-result labels use the helper');
  assert(searchCode.includes('resultCountLabel(hits.length)'), 'search count uses the helper');
  assert(favoritesCode.includes('resultCountLabel(saved.length)'), 'favorite count uses the helper');
  assert(searchCode.includes('searchTextMatches('), 'doSearch() uses the tested search matcher');
  assert.match(html, /VERSE_FOLDED_TEXT\.push\(searchFoldKey\(s\.t\)\)/,
               'loose spelling folds are confined to the IAST verse field');
});

console.log(`\nsearch regressions: ${passed} tests passed`);
