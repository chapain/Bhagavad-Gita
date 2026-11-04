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

test('a marked query that misses gets one folded second chance (C3)', () => {
  const alt = searchContext.searchFoldAlternative;
  assert.equal(typeof alt, 'function',
               'the built app must emit searchFoldAlternative()');
  const rescue = alt('sankhyā');
  assert(rescue && rescue.folded === 'sankhya',
         'a marked query folds to its plain reading');
  assert.equal(alt('sankhya'), null,
               'a query that is already plain is not folded again');
  // The rescue has to be a real one: zero exact hits, hits once folded.
  const exactHits = query => verses.filter(v => searchMatches(v.t, query)).length;
  const foldedHits = query => {
    const folded = foldedKey(query);
    return verses.filter(v => foldedKey(v.t).includes(folded)).length;
  };
  for (const q of ['sankhyā', 'arjunā', 'karmanyā']) {
    assert.equal(exactHits(q), 0, `${q} must miss the exact pass`);
    assert(foldedHits(q) > 0, `${q} must find verses once folded`);
  }
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

test('the floating listbox and stored queries are gone, by design', () => {
  /* 2026-11-04, owner report: the suggestion panel covered the live results and
     its first five rows were his own past queries — one search for 11.47 had
     stored "11", "11.", "11.4" and "11.47" as four separate recents, because
     the old code saved the query on every debounced live search. Search already
     renders its results as he types, so the overlay was removed, not restyled. */
  assert(!/id="searchSuggest"/.test(html), 'no floating suggestion list is emitted');
  assert(!/sugRowsFor|sugRender|sugKey|sugPick/.test(html), 'no suggestion code survives');
  assert(!/'gitaRecent'/.test(html), 'typed queries are never written to storage');
  const start = html.indexOf('function doSearch(){');
  const end = html.indexOf('\nfunction clearSearch(){', start);
  const code = html.slice(start, end);
  const zeroStart = code.lastIndexOf('if(total === 0){');
  const zeroEnd = code.indexOf('return;', zeroStart);
  assert(zeroStart >= 0 && zeroEnd > zeroStart, 'the zero-result branch must be locatable');
  assert(/srchChipsHtml\(\)/.test(code.slice(zeroStart, zeroEnd)),
         'the empty state offers its four real starters');
  assert(!/srchChipsHtml/.test(code.slice(zeroEnd)),
         'a screen with hits carries no chip row');
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
  // The headline count is the whole page: verses plus the chapter/theme passages
  // that share it. Counting only hits would say "0 results" above a theme card.
  assert(searchCode.includes('resultCountLabel(total)'), 'search count covers every result group');
  assert(/total = hits\.length \+ passages\.length/.test(searchCode),
         'the total adds passage hits to verse hits');
  // C3 reclaims the same total after a rescue, so it is recomputed, not frozen.
  assert(searchCode.includes('searchFoldAlternative(q)'),
         'doSearch() asks for a folded second chance');
  assert(/if\(total === 0\)\{[\s\S]*?searchFoldAlternative\(q\)/.test(searchCode),
         'the second chance is only taken when the exact pass found nothing');
  assert(searchCode.includes("SRCH_NOTE = L('search_meant')"),
         'the reader is told when the query was relaxed');
  assert(favoritesCode.includes('resultCountLabel(saved.length)'), 'favorite count uses the helper');
  assert(searchCode.includes('searchTextMatches('), 'doSearch() uses the tested search matcher');
  assert.match(html, /VERSE_FOLDED_TEXT\.push\(searchFoldKey\(s\.t\)\)/,
               'loose spelling folds are confined to the IAST verse field');
});

test('search v2 highlights substring matches safely and offers four real starters', () => {
  const hlStart = html.indexOf('function hlSearchText(');
  const hlEnd = html.indexOf('\nfunction doSearch(){', hlStart);
  assert(hlStart >= 0 && hlEnd > hlStart, 'hlSearchText and chip helpers must be emitted');
  const store = {};
  const ctx = vm.createContext({
    localStorage: {
      getItem: k => store[k] || null,
      setItem: (k, v) => { store[k] = v; },
    },
    esc: s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'),
    digitNorm: s => String(s).replace(/[०-९]/g, d => '0123456789'['०१२३४५६७८९'.indexOf(d)]),
    numL: s => String(s),
    L: k => k,
    $: () => null,
  });
  vm.runInContext(html.slice(hlStart, hlEnd), ctx);
  assert.equal(ctx.hlSearchText('The Yoga of Action', 'yoga'),
               'The <mark class="srch-hl">Yoga</mark> of Action');
  assert.equal(ctx.hlSearchText('Verse 2.47 <script>', '2.47'),
               'Verse 2.47 &lt;script&gt;', 'numeric queries are not wrapped in <mark>');
  const chips = ctx.srchChipsHtml();
  for (const q of ['2.47', '4.7', '18.66', 'धर्मक्षेत्रे'])
    assert(chips.includes(`data-q="${q}"`), `the empty state offers ${q}`);
  assert(!/gitaRecent/.test(html.slice(hlStart, hlEnd)),
         'the search screen keeps no history of what the reader typed');
});


/* ---- the widened index: titles, glosses, chapters, themes ---------------
   Search used to index the Sanskrit, the IAST and the paraphrase — so a reader
   who remembered the story ("Time's decree") or one word of the glossary ("not
   hating") got nothing. These execute the shipped `verseSearchText()` and
   `buildPassages()` against the real chapter payloads. */
function loadVerseIndex() {
  const start = html.indexOf('function verseSearchText(');
  const end = html.indexOf('\nconst VERSE_TEXT', start);
  assert(start >= 0 && end > start, 'verseSearchText() must be emitted');
  const ctx = vm.createContext({
    state: { lang: 'en' },
    T: value => (value && value.en) || '',
    fmtN: n => String(n),
    SANSKRIT_RE: /[\u0900-\u097F]/,
  });
  vm.runInContext(html.slice(start, end), ctx);
  return ctx;
}
function partOf(ref) {
  for (const ch of data) {
    for (const th of ch.themes) {
      for (const part of th.parts) {
        if (part.sutras.some(sutra => displayRef(sutra.n) === ref)) return part;
      }
    }
  }
  assert.fail(`no part holds verse ${ref}`);
}

test('a verse answers to its own title and to its word-by-word glosses', () => {
  const ctx = loadVerseIndex();
  const text = ref => ctx.verseSearchText(verse(ref), partOf(ref));
  assert(searchMatches(text('1.29'), 'My limbs fail'),
         'the verse title "My limbs fail" must find 1.29');
  assert(searchMatches(text('12.13'), 'not hating'),
         'a gloss word (not hating) must find its verse');
  assert(!searchMatches(text('12.13'), 'compassionate llama'),
         'the widened index must not match two absent words');
  const sanskritOnly = data[0].themes[0].parts[0].sutras[0];
  assert(ctx.verseSearchText(sanskritOnly, partOf(displayRef(sanskritOnly.n)))
           .includes(sanskritOnly.d),
         'the Devanagari line stays in the index');
});

test('chapters and themes are searchable by name, and only as passages', () => {
  const start = html.indexOf('const SEARCH_PASSAGES = [];');
  const end = html.indexOf('\nfunction assembleData(){', start);
  assert(start >= 0 && end > start, 'buildPassages() must be emitted');
  const ctx = vm.createContext({
    DATA: data,
    state: { lang: 'en' },
    T: value => (value && typeof value === 'object') ? (value.en || '') : (value || ''),
    searchExactKey: exactKey,
    searchFoldKey: foldedKey,
  });
  vm.runInContext(html.slice(start, end) + '\nbuildPassages();\nglobalThis.__passages = SEARCH_PASSAGES;', ctx);
  const passages = ctx.__passages;
  assert.equal(passages.filter(p => p.kind === 'chapter').length, 18,
               'every chapter is a passage result');
  assert.equal(passages.filter(p => p.kind === 'theme').length, 169,
               'every theme is a passage result');
  // Match exactly the way passageHits() does: the stored exact + folded keys.
  const hit = (kind, query) => passages.filter(p => p.kind === kind &&
    searchContext.searchTextMatches(p.exact, p.folded, prepareQuery(query)));
  assert(hit('chapter', 'Sankhya').some(p => p.ci === 1),
         'ASCII "Sankhya" must reach the chapter named Sāṅkhya');
  assert(hit('chapter', 'Moksha-Sannyasa').some(p => p.ci === 17),
         'ASCII "Moksha-Sannyasa" must reach chapter 18');
  assert(hit('theme', "Kṛṣṇa rebukes Arjuna's dejection").length === 1,
         'a theme title must find its theme');
  assert.equal(hit('chapter', 'not hating').length, 0,
               'passages do not borrow verse words');
});

test('a note is independent of the favourites list', () => {
  const start = html.indexOf('function removeFav(');
  const end = html.indexOf('\nfunction ', start + 10);
  assert(start >= 0 && end > start, 'removeFav() must be emitted');
  const body = html.slice(start, end);
  assert(!/FAVNOTE/.test(body),
         'un-favouriting must not touch the note store (notes outlive favourites)');
  assert(html.includes('function noteGet(') && html.includes('function notesList('),
         'the notes list reads the note store directly');
  assert(/note: noteGet,/.test(html) && /setNote: setFavNote,/.test(html),
         'the reader reaches notes through App.library');
  assert((html.match(/L\('note_label'\)/g) || []).length >= 2 &&
         html.includes("L('note_ph')"),
         'the note field is localized wherever it appears');
  assert(html.includes('class="m-note"') && html.includes('class="note-card"'),
         'a note can be written in the sheet and listed in saved');
  assert(!/id=|FAVNOTE/.test(html.slice(html.indexOf('function removeFav('),
                html.indexOf('function removeFav(') + 400)),
         'un-favouriting leaves the verse and its note alone');
});

console.log(`\nsearch regressions: ${passed} tests passed`);
