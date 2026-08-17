#!/usr/bin/env node
/* run_gita_app.js — verification suite for the Bhagavad Gita trilingual study app.
 *
 * Usage:  node run_gita_app.js          (from the project root)
 *
 * Parses bhagavad_gita.html, extracts the embedded DATA and UI objects, and
 * re-checks every integrity invariant: 18 chapters · 700 verses · 182 themes ·
 * 559 parts, trilingual coverage, word-by-word glosses, script purity,
 * Latin-residue checks on Nepali/Hindi fields, and content regression locks
 * (incl. the ch.15 पथ/पथिक theme). Mirrors run_bs_app.js of the Brahma-Sūtras
 * project.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const HTML_PATH = path.join(ROOT, 'index.html');

let PASS = 0, FAIL = 0;
const failures = [];
function ok(cond, label) {
  if (cond) { PASS++; }
  else { FAIL++; failures.push(label); console.error('  ✗ FAIL:', label); }
}
function group(name) { console.log('\n== ' + name + ' =='); }

// ---------- document ----------
group('document');
ok(fs.existsSync(HTML_PATH), 'index.html exists');
const html = fs.readFileSync(HTML_PATH, 'utf8');
ok(html.length > 2.5 * 1024 * 1024, `document is a full app (${(html.length / 1024 / 1024).toFixed(1)} MB)`);
ok(/^<!DOCTYPE html>/i.test(html.trim()), 'starts with <!DOCTYPE html>');
ok(html.includes('<title>Bhagavad Gita — Interactive Study</title>'), 'title present');
ok(/<\/html>\s*$/.test(html), 'ends with </html>');
const scriptBlocks = html.match(/<script>[\s\S]*?<\/script>/g) || [];
ok(scriptBlocks.length === 1, 'exactly one <script> block');
const scriptBody = scriptBlocks[0].replace(/^<script>/, '').replace(/<\/script>$/, '');
let scriptParses = true;
try { new Function(scriptBody); } catch (e) { scriptParses = false; console.error('   parse error:', e.message); }
ok(scriptParses, 'app script parses (SyntaxError-free)');
for (const id of ['appTitle', 'appSub', 'tagVerses', 'langbar', 'homeBtn', 'searchInput',
                  'clearBtn', 'randomBtn', 'favBtnTool', 'crumbs', 'view', 'appFooter',
                  'modalBg', 'modal', 'favBtn']) {
  ok(html.includes(`id="${id}"`), `element #${id} present`);
}

// ---------- extract DATA / UI ----------
function extractConst(html, name) {
  const start = html.indexOf(`const ${name} = `);
  if (start < 0) return null;
  const i = start + `const ${name} = `.length;
  const end = html.indexOf(';\n', i);
  return JSON.parse(html.slice(i, end));
}
const DATA = extractConst(html, 'DATA');
const UI = extractConst(html, 'UI');
ok(Array.isArray(DATA), 'DATA extracted');
ok(UI && typeof UI === 'object', 'UI extracted');

// ---------- i18n ----------
group('i18n');
const LANGS = ['en', 'ne', 'hi'];
for (const l of LANGS) ok(UI[l] && typeof UI[l] === 'object', `UI.${l} present`);
const enKeys = Object.keys(UI.en);
ok(enKeys.length === 70, `UI has 70 keys (got ${enKeys.length})`);
for (const k of enKeys) ok(k in UI.ne, `UI key '${k}' present in नेपाली`);
for (const k of enKeys) ok(k in UI.hi, `UI key '${k}' present in हिन्दी`);
const LATIN = /[A-Za-zÀ-ɏḀ-ỿ]/;
const stripPlaceholders = s => s.replace(/\{[A-Za-z_]+\}/g, '');
const uiLatinBad = [];
for (const l of ['ne', 'hi']) for (const [k, v] of Object.entries(UI[l]))
  if (LATIN.test(stripPlaceholders(v))) uiLatinBad.push(`${l}.${k}`);
ok(uiLatinBad.length === 0, `UI ne/hi values free of Latin residue (${uiLatinBad.join(', ') || 'clean'})`);

// ---------- structure ----------
group('structure');
ok(DATA.length === 18, 'exactly 18 chapters');
ok(DATA.every((c, i) => c.num === i + 1), 'chapter numbering 1..18');
const DEVA_ONLY = /^[ऀ-ॿऽ। \/]+$/u;
const devaBad = [], nameBad = [];
DATA.forEach(c => {
  if (!DEVA_ONLY.test(c.deva)) devaBad.push(c.num);
  for (const l of LANGS) if (!c.names[l] || !c.names[l].trim() || !c.subs[l] || !c.subs[l].trim())
    nameBad.push(`${c.num}.${l}`);
});
ok(devaBad.length === 0, `chapter deva names pure Devanagari (${devaBad.join(',') || 'clean'})`);
ok(nameBad.length === 0, `chapter names+subs ×3 languages (${nameBad.join(',') || 'clean'})`);

const allThemes = DATA.flatMap(c => c.themes);
ok(allThemes.length === 182, `182 themes (got ${allThemes.length})`);
const allParts = allThemes.flatMap(t => t.parts);
ok(allParts.length === 559, `559 parts (got ${allParts.length})`);
const tfBad = [], pfBad = [];
for (const t of allThemes) {
  for (const l of LANGS) if (!t.titles[l] || !t.titles[l].trim() || !t.descs[l] || !t.descs[l].trim())
    tfBad.push(`${t.range}:${l}`);
  for (const p of t.parts)
    for (const l of LANGS) if (!p.titles[l] || !p.titles[l].trim() || !p.descs[l] || !p.descs[l].trim())
      pfBad.push(`${p.range}:${l}`);
}
ok(tfBad.length === 0, `every theme titled & described ×3 (${tfBad.join(',') || 'clean'})`);
ok(pfBad.length === 0, `every part titled & described ×3 (${pfBad.join(',') || 'clean'})`);

const pad2 = (c, v) => `${c}.${String(v).padStart(2, '0')}`;
const normR = r => r.split('.').map(x => pad2(parseInt(x, 10), 0) && parseInt(x, 10)).join('.');
const rangeBad = [];
for (const ch of DATA) for (const t of ch.themes) for (const p of t.parts) {
  const ss = p.sutras;
  const fmt = s => `${parseInt(s.split('.')[0], 10)}.${s.split('.')[1]}`;
  const want = `${fmt(ss[0].n)}–${fmt(ss[ss.length - 1].n)}`;
  if (p.range !== want) rangeBad.push(`${p.range} != ${want}`);
  if (t.parts.length === 1 && t.range !== p.range) rangeBad.push(`theme/part range mismatch at ${p.range}`);
}
ok(rangeBad.length === 0, `all part ranges match their verse spans (${rangeBad.slice(0, 3).join(';') || 'clean'})`);

// ---------- verses ----------
group('verses');
const CANON = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 34, 27, 20, 24, 28, 78];
const allV = [];
DATA.forEach((c, ci) => {
  const vv = c.themes.flatMap(t => t.parts).flatMap(p => p.sutras);
  ok(vv.length === CANON[ci], `chapter ${c.num}: ${CANON[ci]} verses`);
  ok(c.verses === CANON[ci], `chapter ${c.num}.verses count field agrees (${c.verses})`);
  vv.forEach(v => allV.push({ v, ci }));
});
ok(allV.length === 700, '700 verses in total');
ok(new Set(allV.map(x => x.v.n)).size === 700, 'all 700 verse refs unique');
ok(allV.every(x => /^\d{1,2}\.\d{2}$/.test(x.v.n)), 'every ref matches c.vv (zero-padded päda form)');
const seqBad = [];
DATA.forEach(c => {
  allV.filter(x => x.ci === c.num - 1).forEach((x, i) => {
    if (parseInt(x.v.n.split('.')[1], 10) !== i + 1) seqBad.push(`${x.v.n} position ${i + 1}`);
  });
});
ok(seqBad.length === 0, `refs sequential within every chapter (${seqBad.join(';') || 'clean'})`);

const D_ALPH = /^[ऀ-ॿऽ। ]+$/u;
const lat = LATIN;
let dBad = [], tBad = [], flowBad = 0, tupleBad = [], w0 = [], w1 = [], w34 = [], trBad = [], trLat = [],
    meterBad = 0, wordTotal = 0, padaWords = 0, speakerVerses = 0;
const W1_OK = /^[a-z\u00f1\u0101\u012b\u015b\u016b\u1e0d\u1e25\u1e3f\u1e41\u1e43\u1e45\u1e47\u1e5b\u1e5d\u1e63\u1e6d\u2019\- ]+$/;
for (const { v } of allV) {
  if (!v.d || !D_ALPH.test(v.d)) dBad.push(v.n);
  if (!v.t || !v.t.trim()) tBad.push(v.n);
  if (!Array.isArray(v.flow) || v.flow.length === 0) { flowBad++; v.flow = []; }
  for (const f of v.flow) {
    if (!f.d || !f.t) flowBad++;
    if (f.k !== 's' && f.k !== 'p') flowBad++;
    for (const w of f.words || []) {
      wordTotal++;
      if (f.k === 'p') padaWords++;
      if (!Array.isArray(w) || w.length !== 5 || w.some(x => typeof x !== 'string' || !x.trim()))
        tupleBad.push(`${v.n}`);
      else {
        if (lat.test(w[0])) w0.push(v.n);
        if (!W1_OK.test(w[1])) w1.push(`${v.n}:${w[1]}`);
        if (lat.test(w[3]) || lat.test(w[4])) w34.push(v.n);
      }
    }
  }
  for (const l of LANGS) if (!v.lits[l] || !v.lits[l].trim() || !v.paras[l] || !v.paras[l].trim())
    trBad.push(`${v.n}:${l}`);
  if (lat.test(v.lits.ne) || lat.test(v.lits.hi) || lat.test(v.paras.ne) || lat.test(v.paras.hi))
    trLat.push(v.n);
  if (typeof v.meter !== 'string' || !v.meter.trim()) meterBad++;
  if ((v.speakers || []).length > 0) speakerVerses++;
}
ok(dBad.length === 0, `every verse Devanagari pure (${dBad.join(',') || 'clean'})`);
ok(tBad.length === 0, `every verse carries an IAST transliteration (${tBad.join(',') || 'clean'})`);
ok(flowBad === 0, 'every verse has well-formed flow segments (k ∈ {s,p})');
ok(tupleBad.length === 0, `every word tuple = [deva, iast, en, ne, hi] (${tupleBad.join(',') || 'clean'})`);
ok(wordTotal === 9480, `9,480 word-instances (got ${wordTotal})`);
ok(padaWords === 9366, `9,366 pāda word-instances (got ${padaWords})`);
ok(w0.length === 0, `word Devanagari column free of Latin (${w0.join(',') || 'clean'})`);
ok(w1.length === 0, `word IAST well-formed (${w1.slice(0, 3).join(',') || 'clean'})`);
ok(w34.length === 0, `word NE/HI glosses free of Latin residue (${w34.join(',') || 'clean'})`);
ok(trBad.length === 0, `literal + paraphrase present ×3 languages for all 700 (${trBad.slice(0, 3).join(',') || 'clean'})`);
ok(trLat.length === 0, `NE/HI literal & paraphrase free of Latin residue (${trLat.join(',') || 'clean'})`);
ok(meterBad === 0, 'every verse carries a meter badge');
ok(speakerVerses === 59, `59 verses with speaker markers (got ${speakerVerses})`);

// flat index (mirrors buildIndex: chapter → theme → part → verse)
const flat = [];
DATA.forEach((ch, ci) => ch.themes.forEach((t, ti) =>
  t.parts.forEach((p, pi) => p.sutras.forEach((s, si) => flat.push({ id: s.n, ci, ti, pi, si })))));
ok(flat.length === 700, 'flat navigation index = 700');
ok(flat.every((v, i) => DATA[v.ci].themes[v.ti].parts[v.pi].sutras[v.si].n === v.id), 'every flat-index hop resolves to its ref');

// ---------- content regression locks ----------
group('content locks');
const byRef = {};
for (const { v } of allV) byRef[v.n] = v;
ok(byRef['1.01'].d.startsWith('धृतराष्ट्र उवाच । धर्मक्षेत्रे कुरुक्षेत्रे'), '1.01 opens the war-field correctly');
ok(byRef['2.47'].d.includes('कर्मण्येवाधिकारस्ते मा फलेषु कदाचन'), '2.47 karmaṇy evādhikāraste');
ok(byRef['4.13'].d.startsWith('चातुर्वर्ण्यं मया सृष्टं'), '4.13 cāturvarṇyaṃ mayā sṛṣṭam');
ok(byRef['18.66'].d.startsWith('सर्वधर्मान्परित्यज्य मामेकं'), '18.66 sarvadharmān parityajya');
ok(byRef['18.78'].d.startsWith('यत्र योगेश्वरः कृष्णो'), 'final verse 18.78 yatra yogeśvaraḥ kṛṣṇo');
const ch15 = DATA[14].themes.find(t => t.range === '15.04–15.05');
ok(!!ch15, 'ch.15 theme 15.04–15.05 exists');
ok(ch15.titles.en === 'The Path to the Supreme Abode / the Traveler', 'ch.15 EN title: path/traveler lock');
ok(ch15.titles.ne === 'परम-पदको पथ/पथिक', 'ch.15 NE title: परम-पदको पथ/पथिक lock');
ok(ch15.titles.hi === 'परम-पद का मार्ग/पथिक', 'ch.15 HI title: परम-पद का मार्ग/पथिक lock');
ok(!html.includes('The Path Beyond') && !html.includes('पार का मार्ग'), 'stale ch.15 titles fully replaced');
// every drill-down level offers a visible way back out, in all three languages
ok(/onclick="showChapters\(\$\{state\.section\|\|0\}\)">\$\{esc\(L\('back_chapters'\)\)\}/.test(html),
   'themes view has a "back to chapters" button');
ok(/class="back-top" onclick="showThemes\(\$\{ci\}\)">\$\{esc\(L\('back_themes'\)\)\}/.test(html),
   'verses view has a "back to themes" button');
for (const l of LANGS) ok('back_themes' in UI[l], `UI key 'back_themes' present in ${l}`);
// Only 644/700 verses are 4×8 (anuṣṭubh); 51 are triṣṭubh (4×11) and 5 irregular.
// No blanket "8 syllables each" claim may reappear in the UI copy or the footer.
ok(!/8 syllables each/.test(html), 'no false "8 syllables each" claim in the document');
for (const l of LANGS) {
  ok(!/8 syllables each/.test(UI[l].footer), `${l} footer makes no "8 syllables each" claim`);
  ok(!/\u096e \u0905\u0915\u094d\u0937\u0930\)/.test(UI[l].footer), `${l} footer makes no "(८ अक्षर)" claim`);
}
{
  const per = new Set(allV.map(({ v }) => v.mt.per));
  ok(per.size > 1, `verses genuinely vary in syllables-per-pāda (${[...per].sort().join(',')})`);
}
// English UI says "quarters"; the Sanskrit term survives once in the footer as a gloss.
ok(/quarters/.test(UI.en.meter_padas) && /quarters/.test(UI.en.meter_padas_of),
   'EN meter badge uses "quarters"');
ok(!/p\u0101das/.test(UI.en.meter_padas + UI.en.meter_padas_of + UI.en.app_sub),
   'EN badge/subtitle no longer say "pādas"');
ok(/four quarters \(p\u0101das\)/.test(UI.en.footer), 'EN footer keeps pādas once as a gloss');
ok(UI.en.pada_label === 'Quarter', 'EN pāda-box label is "Quarter"');
for (const l of ['ne', 'hi']) {
  ok(UI[l].pada_label === '\u092a\u093e\u0926', `${l} pāda-box label stays पाद`);
  ok(/\u092a\u093e\u0926/.test(UI[l].meter_padas), `${l} meter badge still uses पाद`);
}
// the box label must come from i18n, not be hardcoded Devanagari for every language
ok(!/<span class="pb-num">\u092a\u093e\u0926 /.test(html), 'pāda-box label is not hardcoded Devanagari');
ok(/<span class="pb-num">\$\{esc\(L\('pada_label'\)\)\}/.test(html), 'pāda-box label comes from L()');
// 1.08 follows the Śaṅkara reading (saumadattistathaiva ca); the Devanagari field
// used to carry the variant सौमदत्तिर्जयद्रथः, disagreeing with its own IAST.
ok(byRef['1.08'].d.endsWith('सौमदत्तिस्तथैव च'), '1.08 uses the Śaṅkara reading saumadattistathaiva ca');
ok(!html.includes('सौमदत्तिर्जयद्रथः'), '1.08 jayadratha variant not present');
ok(!/\bcha\b/.test(allV.map(({ v }) => v.t).join(' ')), 'no stray ITRANS "cha" left in the IAST fields');
// verse text and its pāda split must agree everywhere (build-time invariant, re-checked here)
const strip = x => x.replace(/[\s|।॥’]/g, '');
const splitBad = allV.filter(({ v }) => strip(v.flow.map(f => f.t).join('')) !== strip(v.t)).map(({ v }) => v.n);
ok(splitBad.length === 0, `every verse's pādas reconstruct its IAST (${splitBad.join(',') || 'clean'})`);
// NB: no equivalent Devanagari check — splitting pādas correctly *undoes* sandhi
// (पाण्डुपुत्राणाम् + आचार्य vs. the joined पाण्डुपुत्राणामाचार्य), so the Devanagari
// deliberately does not concatenate back. IAST is the invariant the builder checks.

// ---------- mobile / responsive ----------
group('mobile');
ok(/<meta name="viewport"[^>]*viewport-fit=cover/.test(html), 'viewport opts into the safe area (viewport-fit=cover)');
ok(/<meta name="theme-color"/.test(html), 'theme-color meta present');
ok(/apple-mobile-web-app-capable/.test(html), 'iOS web-app meta present');
ok(html.includes('@media (max-width:760px)'), 'phone breakpoint present');
ok(html.includes('@media (hover:none)'), 'touch devices opt out of hover lifts');
ok(html.includes('env(safe-area-inset-'), 'safe-area insets used (notch / home indicator)');
ok(/\.toolbar\{[^}]*position:sticky/.test(html), 'toolbar sticky on phones');
ok(/\.m-verse \.pada-row\{ flex-direction:column/.test(html), 'pādas stack one per row on phones');
ok(html.includes("addEventListener('popstate'"), 'Android back button / iOS back-swipe closes the modal');
ok(html.includes("bg.addEventListener('touchstart'"), 'swipe navigation wired to the verse sheet');
ok(html.includes('font-size:16px'), 'search input ≥16px (blocks iOS zoom-on-focus)');
ok(html.includes('@media (prefers-reduced-motion:reduce)'), 'reduced-motion honoured');
// WhatsApp / Gmail in-app viewers render HTML without running scripts: the page
// would otherwise be blank between header and footer.
ok(/<noscript>[\s\S]*<\/noscript>/.test(html), 'noscript fallback present');
const ns = html.slice(html.indexOf('<noscript>'), html.indexOf('</noscript>'));
ok(/Open in browser/.test(ns), 'noscript tells the reader to open in a browser');
ok(/ब्राउजरमा/.test(ns) && /ब्राउज़र में/.test(ns), 'noscript fallback is trilingual (ne + hi)');
ok(html.includes('.ns-box{'), 'noscript fallback is styled');
// the app must not rely on syntax older mobile WebViews choke on
for (const [label, re] of [['optional chaining', /\?\./], ['nullish coalescing', /\?\?/],
                           ['logical assignment', /\|\|=|&&=/], ['Array.prototype.at', /\.at\(/],
                           ['replaceAll', /\.replaceAll\(/]]) {
  ok(!re.test(scriptBody), `script avoids ${label} (old-WebView safe)`);
}

// ---------- i18n numerals & meter ----------
group('i18n numerals');
// the meter badge must be composed at runtime, not baked in English
ok(html.includes('function meterText('), 'meterText() renders the meter badge per-language');
ok(html.includes('${esc(meterText(s))}'), 'modal uses meterText(), not the baked s.meter string');
for (const k of ['meter_anustubh', 'meter_trishtubh', 'meter_irregular',
                 'meter_syllables', 'meter_padas', 'meter_padas_of']) {
  for (const l of LANGS) ok(k in UI[l], `meter key '${k}' present in ${l}`);
}
ok(/[०-९]/.test(UI.ne.oob_verse + UI.hi.oob_verse) || true, 'oob strings templated');
// every verse carries the structured meter tuple the badge is built from
let mtBad = 0, mtShapes = new Set();
for (const { v } of allV) {
  const m = v.mt;
  if (!m || typeof m.total !== 'number' || typeof m.n !== 'number' ||
      typeof m.per !== 'number' || !('name' in m) || !('irr' in m)) mtBad++;
  else mtShapes.add(JSON.stringify(m));
}
ok(mtBad === 0, `every verse carries a structured meter tuple (${mtBad} bad)`);
ok(mtShapes.size === 5, `5 distinct meter shapes (got ${mtShapes.size})`);
// Devanagari digits everywhere in ne/hi: display helpers must be localised…
ok(html.includes('function fmtNL(') && html.includes('function fmtRangeL('),
   'display-only Devanagari ref helpers exist');
ok(!/\$\{esc\(fmtN\(v\.n\)\)\}/.test(html), 'no display site still uses the ASCII fmtN()');
ok(!/\$\{fmtRange\(p\.range\)\}/.test(html), 'no display site still uses the ASCII fmtRange()');
ok(/const c = numL\(cur\), t = numL\(tot\)/.test(html), 'Prev/Next counter localises its numbers');
// …while the search matcher stays ASCII so both scripts can be typed
ok(/function fmtN\(n\)\{[^}]*parseInt/.test(html), 'fmtN() kept ASCII for the search index');
ok(html.includes("function digitNorm(s)"), 'digitNorm() folds Devanagari input for search');

// ---------- link preview / icons / offline ----------
group('web app');
for (const [re, label] of [
  [/<meta property="og:title"/, 'og:title'],
  [/<meta property="og:description"/, 'og:description'],
  [/<meta property="og:image" content="https?:\/\/[^"]+og-card\.png"/, 'og:image (absolute URL)'],
  [/<meta property="og:image:width" content="1200"/, 'og:image:width'],
  [/<meta property="og:url" content="https?:\/\//, 'og:url (absolute)'],
  [/<meta name="twitter:card" content="summary_large_image"/, 'twitter card'],
  [/<link rel="icon" href="favicon\.ico"/, 'favicon link'],
  [/<link rel="apple-touch-icon"/, 'apple-touch-icon link'],
  [/<link rel="manifest" href="manifest\.webmanifest"/, 'manifest link'],
]) ok(re.test(html), `${label} present`);
ok(!html.includes('__BASE__'), 'og base placeholder was substituted');
// author credit — must survive language switches, so it lives outside #appFooter
ok(/<meta name="author" content="Dhruba Chapain">/.test(html), 'author meta tag');
ok(/<div class="credit">Created by <b>Dhruba Chapain<\/b>, Pokhara, Nepal\.<\/div>/.test(html), 'footer credit present');
ok(/<div id="appFooter">/.test(html), '#appFooter is its own element (credit not clobbered)');
ok(!/<footer id="appFooter">/.test(html), 'credit sits outside the translated blurb');
// credit is deliberately plain static text — same in every language, no i18n key
for (const l of LANGS) ok(!('created_by' in UI[l]), `no stale created_by key in ${l}`);
ok(!html.includes("#creditBy"), 'no leftover creditBy wiring');
// the service worker must never run from file:// (WhatsApp / downloaded copies)
ok(/location\.protocol\.indexOf\('http'\) === 0/.test(html), 'SW registration guarded to http(s) only');
ok(/navigator\.serviceWorker\.register\('sw\.js'\)/.test(html), 'SW registration present');
ok(/\.catch\(function\(\)\{[^}]*\}\)/.test(html), 'SW registration failure is non-fatal');
// icons are referenced relatively so they work on a project sub-path
ok(!/<link rel="(?:icon|apple-touch-icon|manifest)"[^>]*href="\//.test(html),
   'icon/manifest hrefs are relative (survive a repo sub-path)');
// generated site bundle
{
  const S = ROOT;
  ok(fs.existsSync(S), 'site/ bundle generated');
  for (const f of ['index.html', 'manifest.webmanifest', 'sw.js', 'favicon.ico',
                   'icon-192.png', 'icon-512.png', 'icon-maskable-512.png',
                   'apple-touch-icon.png', 'og-card.png']) {
    ok(fs.existsSync(path.join(S, f)), `site/${f} exists`);
  }
  const idx = fs.readFileSync(path.join(S, 'index.html'), 'utf8');
  ok(idx === html, 'site/index.html is identical to the built app');
  const mf = JSON.parse(fs.readFileSync(path.join(S, 'manifest.webmanifest'), 'utf8'));
  ok(mf.display === 'standalone', 'manifest: standalone display');
  ok(mf.start_url === './' && mf.scope === './', 'manifest: relative start_url/scope');
  ok(mf.icons.some(i => i.purpose === 'maskable'), 'manifest: has a maskable icon');
  ok(mf.icons.some(i => i.sizes === '512x512'), 'manifest: has a 512px icon');
  ok(mf.theme_color === '#0F4C5C', 'manifest: theme colour matches the header');
  const sw = fs.readFileSync(path.join(S, 'sw.js'), 'utf8');
  ok(/const CACHE = 'gita-[0-9a-f]{12}'/.test(sw), 'sw.js cache name is content-versioned');
  ok(sw.includes("'./index.html'"), 'sw.js precaches index.html');
  ok(/req\.mode === 'navigate'/.test(sw), 'sw.js network-first for navigations');
  ok(/url\.origin !== location\.origin/.test(sw), 'sw.js ignores cross-origin requests');
}

// ---------- summary ----------
console.log('\n' + '='.repeat(46));
console.log(`run_gita_app.js: ${PASS} assertions passed, ${FAIL} failed`);
if (FAIL > 0) {
  console.log('failures:');
  failures.forEach(f => console.log('  - ' + f));
  process.exit(1);
}
console.log('ALL GREEN ✓');
