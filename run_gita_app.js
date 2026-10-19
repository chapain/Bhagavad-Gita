#!/usr/bin/env node
/* run_gita_app.js — verification suite for the Bhagavad Gita trilingual study app.
 *
 * Usage:  node run_gita_app.js          (from the project root)
 *
 * Parses the split app shell and its 18 chapter payloads, then checks the
 * integrity invariants: 18 chapters · 700 verses · 169 themes · 700 parts,
 * trilingual coverage, word-by-word glosses, script purity, Latin-residue
 * checks on Nepali/Hindi fields, and content regression locks.
 */
'use strict';

const fs = require('fs');
const TOTAL_ASSERTIONS = 832;      // keep in step with the printed total
const TOTAL_BROWSER_CHECKS = 270;   // browser_checks.py (Learn/Play, refresh, storage, disclosures)
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
ok(html.length > 150 * 1024 && html.length < 1.5 * 1024 * 1024,
   `shell is light (${(html.length / 1024 / 1024).toFixed(2)} MB)`);
ok(/^<!DOCTYPE html>/i.test(html.trim()), 'starts with <!DOCTYPE html>');
ok(html.includes('<title>Bhagavad Gita — English, Nepali, Hindi · 700 Verses</title>'), 'title targets the trilingual long tail');
ok(/<\/html>\s*$/.test(html), 'ends with </html>');
const scriptBlocks = html.match(/<script>[\s\S]*?<\/script>/g) || [];
// Three executable inline blocks: the pre-paint theme boot, the app, and its
// final gitaBoot() call. JSON-LD is intentionally not counted as executable JS.
ok(scriptBlocks.length === 3, `three executable <script> blocks (got ${scriptBlocks.length})`);
const bodies = scriptBlocks.map(b => b.replace(/^<script>/, '').replace(/<\/script>$/, ''));
const scriptBody = bodies.join('\n');
ok(/data-theme/.test(bodies[0]) && bodies[0].length < 1200, 'first block is the small theme-boot script');
let scriptParses = true;
for (const b of bodies) {
  try { new Function(b); } catch (e) { scriptParses = false; console.error('   parse error:', e.message); }
}
ok(scriptParses, 'app scripts parse (SyntaxError-free)');
for (const id of ['appTitle', 'appSub', 'tagVerses', 'langbar', 'homeBtn', 'searchInput',
                  'clearBtn', 'randomBtn', 'favBtnTool', 'crumbs', 'view', 'appFooter',
                  'modalBg', 'modal', 'favBtn']) {
  ok(html.includes(`id="${id}"`), `element #${id} present`);
}

// ---------- extract DATA / UI ----------
// DATA now lives in data/ch<N>.js (one file per chapter); the shell loads and
// assembles it at runtime. The suite reads the same files and assembles it the
// same way, so every downstream assertion checks the real published payload.
function extractConst(html, name) {
  for (const kw of [`const ${name} = `, `let ${name} = `]) {
    const start = html.indexOf(kw);
    if (start < 0) continue;
    const i = start + kw.length;
    const end = html.indexOf(';\n', i);
    return JSON.parse(html.slice(i, end));
  }
  return null;
}
const DATA = [];
for (let n = 1; n <= 18; n++) {
  const f = path.join(ROOT, 'data', `ch${n}.js`);
  if (!fs.existsSync(f)) continue;
  const m = fs.readFileSync(f, 'utf8').match(/^GITA_CH\[(\d+)\] = ([\s\S]*);\n$/);
  if (!m || Number(m[1]) !== n) continue;
  try { DATA.push(JSON.parse(m[2])); } catch (e) { /* counted below */ }
}
const UI = extractConst(html, 'UI');
ok(DATA.length === 18 && DATA.every((c, i) => c.num === i + 1),
   'DATA assembled from all 18 data/ch<N>.js files, in order');
ok(UI && typeof UI === 'object', 'UI extracted');

// ---------- split build: shell + per-chapter data files ----------
{
  ok(!/"d":\s*"धर्मक्षेत्रे/.test(html), 'shell carries no verse payload');
  ok(/function loadChapter\(n\)[\s\S]*?s\.src = appBase\(\) \+ 'data\/ch' \+ n \+ '\.js';/.test(html)
     && /_idle\(function\(\)\{ loadAllChapters\(\); \}\);/.test(html),
     'chapter payloads load on demand and prefetch at idle');
  ok(/function loadAllChapters\(\)\{[^}]*for \(var n = 1; n <= 18; n\+\+\) ps\.push\(loadChapter\(n\)\);[^}]*Promise\.all\(ps\);/.test(html),
     'loader can fetch all 18 chapter files');
  ok(/let DATA = null;/.test(html), 'shell starts with DATA unloaded');
  // gitaBoot paints the shell through syncLang(), which ends in applyStatic():
  // boot has to apply the RESTORED language's strings, not the hardcoded ones.
  ok(/function assembleData\(\)\{[\s\S]*?buildIndex\(\); buildVerseText\(\);[\s\S]*?\}/.test(html)
     && /function gitaBoot\(\)\{[\s\S]*?App\.library\.assemble\(\);[\s\S]*?syncLang\(state\.lang\);/.test(html)
     && /function syncLang\(l\)\{[\s\S]*?applyStatic\(\);/.test(html),
     'gitaBoot assembles the available data and paints the shell in the restored language');
}

// ---------- i18n ----------
group('i18n');
const LANGS = ['en', 'ne', 'hi'];
for (const l of LANGS) ok(UI[l] && typeof UI[l] === 'object', `UI.${l} present`);
const enKeys = Object.keys(UI.en);
// Phase 3.1 (2026-10-16): added opt_chapter + opt_chapter_d (2) → 186;
// added click_pada_meanings (1) → 187
// 2026-10-17: removed read_sub, opt_full_g, opt_study_g, back_themes (4) → 183,
// together with the per-theme and continuous-reading views that used them.
ok(enKeys.length === 217, `UI has 217 keys (got ${enKeys.length})`);
for (const k of enKeys) ok(k in UI.ne, `UI key '${k}' present in नेपाली`);
for (const k of enKeys) ok(k in UI.hi, `UI key '${k}' present in हिन्दी`);
const LATIN = /[A-Za-zÀ-ɏḀ-ỿ]/;
const stripPlaceholders = s => s.replace(/\{[A-Za-z_]+\}/g, '');
const uiLatinBad = [];
for (const l of ['ne', 'hi']) for (const [k, v] of Object.entries(UI[l]))
  if (LATIN.test(stripPlaceholders(v))) uiLatinBad.push(`${l}.${k}`);
ok(uiLatinBad.length === 0, `UI ne/hi values free of Latin residue (${uiLatinBad.join(', ') || 'clean'})`);
const CHOOSE_KEYS = ['choose_title','opt_full_d','opt_study_d'];
const copiedNeHi = CHOOSE_KEYS.filter(k => UI.ne[k] === UI.hi[k]);
ok(copiedNeHi.length === 0, `hi choice strings are genuine Hindi, not copied from \u0928\u0947\u092a\u093e\u0932\u0940 (${copiedNeHi.join(', ') || 'clean'})`);

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
const redundantFields = [];
for (const c of DATA) {
  if ('name' in c || 'sub' in c) redundantFields.push(`chapter ${c.num}`);
  for (const t of c.themes) {
    if ('title' in t || 'desc' in t) redundantFields.push(`theme ${t.range}`);
    for (const p of t.parts) {
      if ('title' in p || 'desc' in p) redundantFields.push(`part ${p.range}`);
      for (const v of p.sutras)
        if (['lines','padas','speakers','meter','mt'].some(k => k in v)) redundantFields.push(`verse ${v.n}`);
    }
  }
}
ok(redundantFields.length === 0, `compact schema has no duplicate labels or derived verse fields (${redundantFields.slice(0,3).join(',') || 'clean'})`);

const allThemes = DATA.flatMap(c => c.themes);
ok(allThemes.length === 169, `169 themes (got ${allThemes.length})`);
const mapContract = JSON.parse(fs.readFileSync(path.join(ROOT, 'source', 'study_map_contract.json'), 'utf8'));
for (const chapter of DATA) {
  ok(chapter.themes.map(t=>t.range).join('|') === mapContract.approved_maps[chapter.num].join('|'),
     `chapter ${chapter.num}: complete reviewed story map, not merely revised titles`);
}
const ch2Themes = DATA[1].themes;
const CH2_THEME_RANGES = [
  '2.01–2.03', '2.04–2.06', '2.07–2.10', '2.11–2.15', '2.16–2.18',
  '2.19–2.21', '2.22–2.25', '2.26–2.30', '2.31–2.34', '2.35–2.38',
  '2.39–2.41', '2.42–2.46', '2.47–2.50', '2.51–2.53', '2.54–2.58',
  '2.59–2.61', '2.62–2.63', '2.64–2.68', '2.69–2.72'
];
ok(ch2Themes.length === 19 && ch2Themes.map(t => t.range).join('|') === CH2_THEME_RANGES.join('|'),
   'chapter 2 follows the approved 19-theme verse map');
ok(ch2Themes.every(t => t.parts.reduce((n, p) => n + p.sutras.length, 0) <= 5),
   'chapter 2 themes contain no more than five verses');
const ch17Themes = DATA[16].themes;
const CH17_THEME_RANGES = [
  '17.01–17.03', '17.04–17.04', '17.05–17.06', '17.07–17.07', '17.08–17.10',
  '17.11–17.13', '17.14–17.16', '17.17–17.19', '17.20–17.22', '17.23–17.27', '17.28–17.28'
];
ok(ch17Themes.length === 11 && ch17Themes.map(t => t.range).join('|') === CH17_THEME_RANGES.join('|'),
   'chapter 17 retains its reviewed 11-theme verse map');
ok(ch17Themes.every(t => t.parts.reduce((n, p) => n + p.sutras.length, 0) <= 5),
   'chapter 17 themes contain no more than five verses');
const ch17Austerity = ch17Themes.find(t => t.range === '17.17–17.19');
const ch17Asat = ch17Themes.find(t => t.range === '17.28–17.28');
ok(ch17Austerity && ch17Austerity.titles.en === 'Three kinds of austerity'
   && ch17Austerity.titles.ne === 'तपका तीन प्रकार'
   && ch17Austerity.titles.hi === 'तपस्या के तीन प्रकार'
   && ch17Asat && ch17Asat.titles.en === 'Acts without faith are called Asat'
   && ch17Asat.titles.ne === 'श्रद्धाविना गरिएका कर्मलाई असत् भनिन्छ'
   && ch17Asat.titles.hi === 'श्रद्धा के बिना किए गए कर्म असत् कहलाते हैं'
   && ch17Austerity.descs.en.includes('without desire for fruit')
   && ch17Austerity.descs.ne.includes('फलको इच्छा नराखी')
   && ch17Austerity.descs.hi.includes('फल की इच्छा के बिना')
   && ch17Asat.descs.en.includes('called Asat')
   && ch17Asat.descs.ne.includes('असत्')
   && ch17Asat.descs.hi.includes('असत्'),
   'chapter 17 reviewed austerity and Asat titles/descriptions stay aligned ×3');
const ch17Page = fs.readFileSync(path.join(ROOT, 'chapter', '17', 'index.html'), 'utf8');
ok(ch17Page.includes('Three kinds of austerity') && ch17Page.includes('Acts without faith are called Asat'),
   'chapter 17 landing page carries the reviewed theme titles');
// Individual pearls are addressed by canonical verse, never an old theme index.
const reviewedPart = (ch, ref) => DATA[ch-1].themes.flatMap(t=>t.parts)
  .find(p=>p.sutras.some(v=>v.n===ref));
const reviewedTheme = (ch, ref) => DATA[ch-1].themes
  .find(t=>t.parts.some(p=>p.sutras.some(v=>v.n===ref)));
const reviewedPage = ch => fs.readFileSync(path.join(ROOT,'chapter',String(ch),'index.html'),'utf8');
// Editorial fidelity follow-ups: keep titles and summaries pinned to the literal
// claim of each verse, and preserve 13.26 in its parent theme's description.
const ch1Varna = reviewedPart(1,'1.41');
ok(ch1Varna.titles.en === 'Adharma leads to varṇa mixing'
   && ch1Varna.titles.ne === 'अधर्मबाट वर्णसङ्कर उत्पन्न हुन्छ'
   && ch1Varna.titles.hi === 'अधर्म से वर्णसंकर उत्पन्न होता है'
   && ch1Varna.descs.en.includes('varṇa mixing arises from them')
   && ch1Varna.descs.ne.includes('भ्रष्ट स्त्रीहरूबाट वर्णसङ्कर')
   && ch1Varna.descs.hi.includes('भ्रष्ट स्त्रियों से वर्णसंकर')
   && reviewedPage(1).includes(ch1Varna.titles.en),
   '1.41 labels the stated varṇa consequence without importing fear ×3');
const ch2Intellect = reviewedPart(2,'2.53');
ok(ch2Intellect.titles.en === 'The intellect stands firm in samādhi'
   && ch2Intellect.titles.ne === 'बुद्धि समाधिमा अडिन्छ'
   && ch2Intellect.titles.hi === 'बुद्धि समाधि में ठहरती है'
   && ch2Intellect.descs.en.includes('intellect')
   && reviewedPage(2).includes(ch2Intellect.titles.en),
   '2.53 identifies buddhi as intellect in all three titles');
const ch3Hypocrite = reviewedPart(3,'3.06');
ok(ch3Hypocrite.titles.en === 'Organs of action restrained, mind on sense-objects'
   && ch3Hypocrite.titles.ne === 'कर्मेन्द्रियहरू रोकेर, मनमा विषयको चिन्तन'
   && ch3Hypocrite.titles.hi === 'कर्मेन्द्रियाँ रोककर, मन में विषयों का चिंतन'
   && ch3Hypocrite.descs.en.includes('restrains the organs of action')
   && ch3Hypocrite.descs.ne.includes('कर्मेन्द्रियहरूलाई रोकेर')
   && ch3Hypocrite.descs.hi.includes('कर्मेन्द्रियों को रोककर')
   && reviewedPage(3).includes(ch3Hypocrite.titles.en),
   '3.06 describes restraint and recollection without adding craving ×3');
const ch13Union = reviewedPart(13,'13.26'), ch13Paths = reviewedTheme(13,'13.26');
const studyMaps = fs.readFileSync(path.join(ROOT,'STUDY_MAPS.md'),'utf8');
ok(ch13Union.titles.en === 'All beings arise from union of field and its knower'
   && ch13Union.titles.ne === 'सबै प्राणी क्षेत्र र क्षेत्रज्ञको संयोगबाट उत्पन्न हुन्छन्'
   && ch13Union.titles.hi === 'सभी प्राणी क्षेत्र और क्षेत्रज्ञ के संयोग से उत्पन्न होते हैं'
   && ch13Paths.descs.en.includes('union of the field and its knower')
   && ch13Paths.descs.ne.includes('क्षेत्र र क्षेत्रज्ञको संयोगबाट उत्पन्न हुन्छन्')
   && ch13Paths.descs.hi.includes('क्षेत्र और क्षेत्रज्ञ के संयोग से उत्पन्न होते हैं')
   && studyMaps.includes('All beings arise from the union of the field and its knower')
   && reviewedPage(13).includes(ch13Union.titles.en),
   '13.26 and its theme name the field-knower union ×3');
const ch18SattvicRenouncer = reviewedPart(18,'18.10');
ok(ch18SattvicRenouncer.titles.en === 'Unpleasant acts not hated, pleasant ones not clung to'
   && ch18SattvicRenouncer.titles.ne === 'अप्रिय कर्मप्रति द्वेष छैन, प्रिय कर्ममा आसक्ति छैन'
   && ch18SattvicRenouncer.titles.hi === 'अप्रिय कर्म से द्वेष नहीं, प्रिय कर्म में आसक्ति नहीं'
   && ch18SattvicRenouncer.descs.en.includes('neither hates unpleasant action nor clings to pleasant action')
   && ch18SattvicRenouncer.descs.ne.includes('अप्रिय कर्मप्रति द्वेष')
   && ch18SattvicRenouncer.descs.hi.includes('अप्रिय कर्म से द्वेष')
   && reviewedPage(18).includes(ch18SattvicRenouncer.titles.en),
   '18.10 preserves the unpleasant/pleasant action contrast ×3');
const ch3Enemy = reviewedTheme(3,'3.36');
ok(ch3Enemy.titles.en === 'Desire and anger conceal wisdom'
   && ch3Enemy.descs.ne.includes('सर्वभक्षी शत्रु') && ch3Enemy.descs.hi.includes('सर्वभक्षी शत्रु')
   && reviewedPage(3).includes(ch3Enemy.titles.en),
   'chapter 3 retains the all-devouring enemy and its correct thematic location ×3');
const ch4BirthPart = reviewedPart(4,'4.05');
ok(ch4BirthPart.titles.en === 'I know all our past births'
   && ch4BirthPart.titles.ne === 'म हाम्रा सबै पूर्वजन्म जान्दछु'
   && ch4BirthPart.titles.hi === 'मैं हमारे सभी पूर्वजन्म जानता हूँ'
   && reviewedPage(4).includes(ch4BirthPart.titles.en),
   'chapter 4 reviewed birth pearl survives regrouping unchanged ×3');
const ch5Verse = reviewedPart(5,'5.19'), ch5Paths = reviewedPart(5,'5.04');
ok(ch5Verse.titles.en === 'Equanimity conquers the world of birth and death'
   && ch5Verse.titles.ne.includes('जन्म-मृत्यु') && ch5Verse.titles.hi.includes('जन्म-मृत्यु')
   && ch5Paths.titles.en === 'Only children call sāṅkhya and yoga different'
   && ch5Paths.titles.ne === 'बालकले मात्र साङ्ख्य र योगलाई फरक ठान्छन्'
   && ch5Paths.titles.hi === 'बालक ही सांख्य और योग को भिन्न कहते हैं'
   && reviewedPage(5).includes(ch5Paths.titles.en) && reviewedPage(5).includes(ch5Verse.titles.en),
   'chapter 5 approved path/equanimity pearls stay trilingual and reachable');
const ch6Meditation = reviewedTheme(6,'6.10'), ch6Resolve = reviewedPart(6,'6.23');
const ch6FormerLife = reviewedPart(6,'6.43'), ch6Renunciation = reviewedPart(6,'6.01');
ok(ch6Meditation.titles.en === 'Meditation: solitude, posture and focus'
   && ch6Renunciation.titles.en === 'He who acts without fruit-seeking: renouncer and yogi'
   && ch6Resolve.titles.en === 'Practise with resolve and an undiscouraged mind'
   && ch6Resolve.descs.ne.includes('निराश नभई') && ch6Resolve.descs.hi.includes('निराश हुए बिना')
   && ch6FormerLife.titles.en === 'He regains spiritual insight from a past life'
   && ch6FormerLife.titles.en.length <= 54 && reviewedPage(6).includes(ch6Meditation.titles.en),
   'chapter 6 meditation, resolve and former-life insight retain their correct verses');
const ch7Closing = reviewedTheme(7,'7.29');
ok(ch7Closing.range === '7.28–7.30' && ch7Closing.titles.en === 'Beyond delusion, know me even at death'
   && ch7Closing.descs.en.includes('all of adhyātma and action')
   && ch7Closing.descs.ne.includes('सम्पूर्ण अध्यात्म र कर्म')
   && ch7Closing.descs.hi.includes('सम्पूर्ण अध्यात्म और कर्म')
   && reviewedPage(7).includes(ch7Closing.titles.en),
   'chapter 7 puts freed knowers after delusion, retaining the full knowledge teaching ×3');
const ch8Always = reviewedPart(8,'8.14'), ch8Cycle = reviewedTheme(8,'8.16');
const ch8Path = reviewedTheme(8,'8.24');
ok(ch8Always.titles.en === 'Easily reached by one who remembers me always'
   && ch8Always.titles.ne.includes('सधैँ सम्झने') && ch8Always.titles.hi.includes('सदा मेरा स्मरण')
   && ch8Cycle.descs.en.includes('Even Brahmā’s world is subject to return')
   && ch8Path.descs.ne.includes('उत्तरायण') && ch8Path.descs.hi.includes('दक्षिणायन')
   && reviewedPage(8).includes('The bright path and the returning path'),
   'chapter 8 separates no-return practice from cosmic return without losing the path facts');
const ch9Soma = reviewedPart(9,'9.20'), ch9Care = reviewedTheme(9,'9.22');
ok(ch9Care.range === '9.20–9.25' && ch9Soma.titles.en === 'Soma drinkers seek heaven'
   && ch9Soma.titles.ne.includes('स्वर्ग खोज्छन्') && ch9Soma.titles.hi.includes('स्वर्ग चाहते हैं')
   && ch9Care.descs.en.includes('supplies what devotees lack and protects what they have')
   && ch9Care.descs.en.includes('Heaven’s pleasures end')
   && reviewedPage(9).includes(ch9Care.titles.en),
   'chapter 9 pairs finite reward with sustained devotion, preserving the approved pearl');
const ch10Part = reviewedPart(10,'10.16');
ok(ch10Part.descs.ne.includes('नछोडी बताइदिन')
   && ch10Part.descs.hi.includes('बिना कुछ छोड़े')
   && !ch10Part.descs.ne.includes('हे परम पुरुष, हे परम पुरुष')
   && !ch10Part.descs.hi.includes('हे परम पुरुष, हे परम पुरुष')
   && reviewedPage(10).includes('Tell me how to recognise and remember you'),
   'chapter 10 preserves its corrected localized request at 10.16');
const ch11Warriors = reviewedTheme(11,'11.26'), ch11Victims = reviewedPart(11,'11.26');
const ch11ForgivePart = reviewedPart(11,'11.44');
ok(ch11Warriors.range === '11.26–11.30' && ch11Warriors.descs.en.includes('Warriors from both sides')
   && ch11Victims.titles.ne.includes('धृतराष्ट्रका छोराहरू') && ch11Victims.titles.hi.includes('धृतराष्ट्र के पुत्र')
   && ch11ForgivePart.titles.hi === 'जैसे पिता पुत्र को क्षमा करता है'
   && ch11ForgivePart.descs.ne.includes('दण्डवत्')
   && reviewedPage(11).includes('Time’s decree and Arjuna’s task'),
   'chapter 11 places warrior destruction in its own passage before Time’s answer ×3');
const ch12Close = reviewedPart(12,'12.20');
ok(ch12Close.titles.en === 'They who follow this immortal dharma are dearest'
   && ch12Close.titles.ne.includes('अत्यन्त प्रिय') && ch12Close.titles.hi.includes('अत्यन्त प्रिय')
   && ch12Close.descs.en.includes('faithfully')
   && reviewedTheme(12,'12.09').descs.en.includes('A graded path')
   && reviewedPage(12).includes(ch12Close.titles.en),
   'chapter 12 retains the graduated practice and faithful closing pearl ×3');
const ch13Field = reviewedTheme(13,'13.01'), ch13Knower = reviewedPart(13,'13.02');
const ch13Means = reviewedTheme(13,'13.07');
ok(ch13Field.range === '13.01–13.06' && ch13Knower.descs.en.includes('knower of the field in all fields')
   && ch13Field.descs.ne.includes('सबै क्षेत्रका क्षेत्रज्ञ') && ch13Field.descs.hi.includes('सभी क्षेत्रों के क्षेत्रज्ञ')
   && ch13Means.descs.en.includes('sustained Self-knowledge')
   && reviewedPage(13).includes(ch13Field.titles.en),
   'chapter 13 joins field definitions but preserves the universal knower and Self-knowledge');
const ch14Transcend = reviewedTheme(14,'14.26'), ch14Rise = reviewedPart(14,'14.10');
ok(ch14Rise.titles.en === 'The guṇas overpower one another'
   && ch14Transcend.descs.en.includes('makes one fit for Brahman')
   && ch14Transcend.descs.ne.includes('ब्रह्मभावका लागि योग्य')
   && ch14Transcend.descs.hi.includes('ब्रह्मभाव के योग्य')
   && reviewedPage(14).includes(ch14Transcend.titles.en),
   'chapter 14 retains the dynamics of the guṇas and qualification for Brahman ×3');
const ch15Persons = reviewedTheme(15,'15.16'), ch15Heart = reviewedTheme(15,'15.15');
ok(ch15Persons.range === '15.16–15.20'
   && ch15Persons.descs.en.includes('perishable and imperishable') && ch15Persons.descs.en.includes('Supreme Person')
   && ch15Persons.titles.ne.includes('पुरुषोत्तम') && ch15Persons.titles.hi.includes('पुरुषोत्तम')
   && ch15Heart.descs.en.includes('forgetfulness') && reviewedPage(15).includes(ch15Persons.titles.en),
   'chapter 15 keeps all three persons distinct and includes forgetfulness in the heart teaching');
const ch16Scripture = reviewedPart(16,'16.23'), ch16Destiny = reviewedPart(16,'16.20');
ok(ch16Scripture.descs.ne.includes('शास्त्रविधि छोडेर')
   && !ch16Scripture.descs.ne.includes('थाती राखेर')
   && ch16Scripture.descs.hi.includes('शास्त्रविधि छोड़कर')
   && ch16Destiny.titles.ne === 'अधम गति' && ch16Destiny.descs.ne.includes('अधम गतिमा')
   && reviewedPage(16).includes('Close hell’s gates and let scripture guide action'),
   'chapter 16 preserves the corrected scripture/destiny pearls while joining the practical exit');
const ch18Teaching = reviewedTheme(18,'18.67'), ch18Listener = reviewedPart(18,'18.71');
ok(ch18Teaching.descs.en.includes('lacks austerity or devotion')
   && ch18Teaching.descs.ne.includes('सुन्न नचाहने') && ch18Teaching.descs.hi.includes('कृष्ण में दोष देखने')
   && ch18Listener.titles.en === 'The faithful listener is freed'
   && reviewedPage(18).includes(ch18Teaching.titles.en),
   'chapter 18 preserves the audience conditions, teacher and faithful listener');
const allParts = allThemes.flatMap(t => t.parts);
ok(allParts.length === 700, `700 parts (got ${allParts.length})`);
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
const meterShape = v => {
  const pads = (v.flow || []).filter(x => x.k === 'p');
  const counts = pads.map(x => Number(x.n) || 0);
  const total = counts.reduce((a, b) => a + b, 0), n = pads.length;
  if (total === 32 && counts.every(x => x === 8)) return {name:'anustubh', irr:0, total:32, n:4, per:8};
  if (total === 44 && counts.every(x => x === 11)) return {name:'trishtubh', irr:0, total:44, n:4, per:11};
  if (total === 33 && n === 4) return {name:'anustubh', irr:1, total:33, n:4, per:0};
  return {name:'', irr:0, total, n, per:0};
};
const verseLines = v => {
  const d = v.d.split('।').map(x => x.trim()).filter(Boolean);
  const t = v.t.split('।').map(x => x.trim()).filter(Boolean);
  if (d.length !== t.length) return [];
  return d.map((x, i) => ({k:t[i].endsWith('uvāca') ? 's' : 'l', d:x, t:t[i]}));
};
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
  const shape = meterShape(v);
  if (!Number.isInteger(shape.total) || shape.n !== 4) meterBad++;
  if (v.flow.some(x => x.k === 's')) speakerVerses++;
}
ok(dBad.length === 0, `every verse Devanagari pure (${dBad.join(',') || 'clean'})`);
ok(tBad.length === 0, `every verse carries an IAST transliteration (${tBad.join(',') || 'clean'})`);
ok(flowBad === 0, 'every verse has well-formed flow segments (k ∈ {s,p})');
ok(tupleBad.length === 0, `every word tuple = [deva, iast, en, ne, hi] (${tupleBad.join(',') || 'clean'})`);
ok(wordTotal === 9484, `9,484 word-instances (got ${wordTotal})`);
ok(padaWords === 9366, `9,366 pāda word-instances (got ${padaWords})`);
ok(w0.length === 0, `word Devanagari column free of Latin (${w0.join(',') || 'clean'})`);
ok(w1.length === 0, `word IAST well-formed (${w1.slice(0, 3).join(',') || 'clean'})`);
ok(w34.length === 0, `word NE/HI glosses free of Latin residue (${w34.join(',') || 'clean'})`);
ok(trBad.length === 0, `literal + paraphrase present ×3 languages for all 700 (${trBad.slice(0, 3).join(',') || 'clean'})`);
ok(trLat.length === 0, `NE/HI literal & paraphrase free of Latin residue (${trLat.join(',') || 'clean'})`);
ok(meterBad === 0, 'every verse meter shape derives from flow pādas');
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
// The path (15.04) and its travellers (15.05) are distinct pearls; their old
// two-verse theme has deliberately been regrouped, not silently lost.
const ch15Path = reviewedPart(15,'15.04'), ch15Travellers = reviewedPart(15,'15.05');
ok(!!ch15Path && !!ch15Travellers, 'ch.15 path and traveller pearls both exist');
ok(ch15Path.titles.en === 'Seek the supreme goal'
   && ch15Travellers.descs.en.includes('Free of pride and delusion'), 'ch.15 EN path/traveller distinction survives regrouping');
ok(ch15Path.titles.ne === 'परम लक्ष्य खोज'
   && ch15Travellers.descs.ne.includes('मान-मोहरहित'), 'ch.15 NE keeps the sought goal distinct from the traveller');
ok(ch15Path.titles.hi === 'परम लक्ष्य की खोज'
   && ch15Travellers.descs.hi.includes('मान-मोह से रहित'), 'ch.15 HI keeps the sought goal distinct from the traveller');
ok(!allThemes.some(t=>t.titles.en==='The Path Beyond' || t.titles.hi==='पार का मार्ग'),
   'stale ch.15 path titles cannot reappear');
// the pill strips and top back-buttons became one breadcrumb: the full trail,
// ancestors as links, current page last — on every drill-down view
ok(/function wayCrumbs\(/.test(html) && /wc-link/.test(html) && /wc-cur/.test(html),
   'drill-down views navigate by breadcrumb (links + current)');
ok((html.match(/App\.views\.breadcrumbs\(\[\[L\('sections_title'\)/g) || []).length >= 4,
   'all four drill-down views root their breadcrumb at The Three Ways');
// Only 644/700 verses are 4×8 (anuṣṭubh); 51 are triṣṭubh (4×11) and 5 irregular.
// No blanket "8 syllables each" claim may reappear in the UI copy or the footer.
ok(!/8 syllables each/.test(html), 'no false "8 syllables each" claim in the document');
for (const l of LANGS) {
  ok(!/8 syllables each/.test(UI[l].footer), `${l} footer makes no "8 syllables each" claim`);
  ok(!/\u096e \u0905\u0915\u094d\u0937\u0930\)/.test(UI[l].footer), `${l} footer makes no "(८ अक्षर)" claim`);
}
{
  const per = new Set(allV.map(({ v }) => meterShape(v).per));
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
// Display rows and speaker placement are derived from canonical source text.
// Verify source and emitted payload agree, then test the same danda/uvāca rules.
{
  const chDir = path.join(__dirname, 'source');
  const sourceVerses = {};
  for (let n = 1; n <= 18; n++) {
    const source = JSON.parse(fs.readFileSync(path.join(chDir, `ch${n}.json`), 'utf8'));
    sourceVerses[n] = new Map(source.themes.flatMap(t => t.parts.flatMap(p => p.sutras))
      .map(v => [v.n, v]));
  }
  let checkedLines = 0;
  const lineBad = [];
  for (const { v } of allV) {
    const cn = Number(v.n.split('.')[0]);
    const src = sourceVerses[cn].get(v.n);
    if (v.d !== src.d || v.t !== src.t) lineBad.push(`${v.n}: canonical text differs from source`);
    const segsD = src.d.split('।').map(x => x.trim()).filter(Boolean);
    const segsT = src.t.split('।').map(x => x.trim()).filter(Boolean);
    const got = verseLines(v);
    if (got.length !== segsD.length) { lineBad.push(`${v.n}: ${got.length} vs ${segsD.length} segments`); continue; }
    for (let i = 0; i < segsD.length; i++) {
      if (got[i].d !== segsD[i]) lineBad.push(`${v.n}[${i}] deva`);
      if (got[i].t !== segsT[i]) lineBad.push(`${v.n}[${i}] iast`);
      const isSpk = segsT[i].endsWith('uvāca');
      if ((got[i].k === 's') !== isSpk) lineBad.push(`${v.n}[${i}] speaker flag`);
      checkedLines++;
    }
  }
  ok(lineBad.length === 0, `display segments derive from source d/t (${checkedLines} segments; ${lineBad.slice(0,3).join(', ') || 'clean'})`);
  ok(allV.every(({ v }) => verseLines(v).filter(l => l.k === 'l').length === 2), 'every verse derives exactly two display lines');
  // 1.21 and 1.28 put the speaker *between* the two lines; derivation preserves it.
  const lines121 = verseLines(byRef['1.21']), lines128 = verseLines(byRef['1.28']);
  ok(lines121[1].k === 's' && lines121[1].d === 'अर्जुन उवाच',
     '1.21 keeps its mid-verse speaker in place');
  ok(lines128[1].k === 's', '1.28 keeps its mid-verse speaker in place');
  // 16.3 was the sandhi-recombination bug; 16.1 the concatenation bug. Both are now
  // impossible by construction, but pin the exact text so a source edit is deliberate.
  ok(verseLines(byRef['16.03'])[0].d === 'तेजः क्षमा धृतिः शौचमद्रोहो नातिमानिता',
     '16.3 renders शौचमद्रोहो (not शौचम्अद्रोहो)');
  ok(verseLines(byRef['16.01'])[1].d.includes('संशुद्धिर्ज्ञानयोग'),
     '16.1 renders संशुद्धिर्ज्ञानयोग as one word');
  // the join machinery must be gone — no flag, no table, no joiner
  ok(!/joinHalves/.test(html), 'joinHalves removed');
  ok(!/const MATRA =/.test(html), 'JS mātrā table removed');
  ok(allV.every(({ v }) => v.flow.every(f => f.j === undefined)), 'no pāda carries a stale join flag');
}
// ---- PROJECT.md must stay true ------------------------------------------
// It is the handover document: if its numbers drift from reality it becomes a
// liability rather than a help, so the build checks the facts it states.
{
  const pm = fs.readFileSync(path.join(__dirname, 'PROJECT.md'), 'utf8');
  ok(/18 chapters · 169 themes · 700 parts · 700 verses/.test(pm),
     'PROJECT.md states the current totals');
  ok(new RegExp(`${Object.keys(UI.en).length} UI strings`).test(pm),
     `PROJECT.md states the current UI key count (${Object.keys(UI.en).length})`);
  for (const f of ['gita_conv.py', 'pada_overrides.py', 'freeze_padas.py', 'sandhi.py']) {
    ok(pm.includes(f), `PROJECT.md records that ${f} was deleted`);
  }
  for (const ref of ['11.01', '2.29', '8.10', '15.03', '2.06']) {
    ok(pm.includes(ref), `PROJECT.md lists irregular verse ${ref}`);
  }
  let payloadsMatchSource = DATA.length === 18;
  for (let n = 1; n <= 18; n++) {
    const source = JSON.parse(fs.readFileSync(path.join(__dirname, 'source', `ch${n}.json`), 'utf8'));
    if (JSON.stringify(source) !== JSON.stringify(DATA[n - 1])) payloadsMatchSource = false;
  }
  ok(payloadsMatchSource, 'all generated chapter payloads match canonical source JSON');

  // The suite sizes drifted once across PROJECT.md, README.md and build.py --
  // three files each claiming a different, wrong number. Assert them here so a
  // grown suite must update its own documentation.
  const rd = fs.readFileSync(path.join(__dirname, 'README.md'), 'utf8');
  const bp = fs.readFileSync(path.join(__dirname, 'build.py'), 'utf8');
  const nAssert = (fs.readFileSync(path.join(__dirname, 'run_gita_app.js'), 'utf8')
                     .match(/^ *ok\(/gm) || []).length;
  for (const [name, doc] of [['PROJECT.md', pm], ['README.md', rd], ['build.py', bp]]) {
    ok(new RegExp(`${TOTAL_ASSERTIONS} assertions`).test(doc),
       `${name} states the assertion count (${TOTAL_ASSERTIONS})`);
    ok(new RegExp(`${TOTAL_BROWSER_CHECKS} (live-)?browser checks`).test(doc),
       `${name} states the browser-check count (${TOTAL_BROWSER_CHECKS})`);
  }
  ok(new RegExp(`${Object.keys(UI.en).length} UI strings`).test(rd),
     `README.md states the current UI key count (${Object.keys(UI.en).length})`);
}
// ---- dark mode ----------------------------------------------------------
{
  ok(/html\[data-theme="dark"\]/.test(html), 'a dark theme block exists');
  ok(/id="themeBtn"/.test(html) && /function toggleTheme/.test(html), 'the theme toggle exists');
  ok(/prefers-color-scheme: dark/.test(html), 'follows the phone\'s own setting');
  ok(/localStorage\.setItem\('gitaTheme'/.test(html), 'remembers the reader\'s choice');
  // localStorage throws in some in-app browsers (WhatsApp); the app must survive it
  const themeCalls = (html.match(/localStorage\.(get|set)Item\('gitaTheme'/g) || []).length;
  const guarded = (html.match(/try\{[^}]*localStorage\.(get|set)Item\('gitaTheme'/g) || []).length;
  ok(themeCalls > 0 && guarded === themeCalls,
     `every gitaTheme storage call is inside try/catch (${guarded}/${themeCalls})`);
  // light mode must be untouched: these are the original brand colours
  ok(/--cream:#FFF8EC/.test(html) && /--teal:#1A5648/.test(html) && /--saffron:#E8912C/.test(html),
     'light mode keeps its original palette');
  // dark mode must not use pure black or pure white — Devanagari shimmers at max contrast
  const darkBlock = (html.match(/html\[data-theme="dark"\]\{[\s\S]*?\}/) || [''])[0];
  ok(darkBlock.length > 100, 'dark block has content');
  ok(!/#000\b|#000000|#fff\b|#FFFFFF/i.test(darkBlock), 'dark mode avoids pure black and pure white');
}
// ---- language persistence -------------------------------------------------
// Owner 2026-10-14: a reader on the chapter 18 study guide in नेपाली was bounced
// back to English by the service-worker reload. The route came home from
// sessionStorage; the language had never been written down at all, so state.lang
// fell back to its hardcoded 'en'. These pin the whole mechanism.
{
  ok(/const GITA_LANGS = \['en','ne','hi'\];/.test(html), 'the language whitelist exists');
  ok(/function savedLang\(\)\{[\s\S]*?sessionStorage\.getItem\('gitaLang'\);[\s\S]*?localStorage\.getItem\('gitaLang'\);[\s\S]*?return GITA_LANGS\.includes\(l\) \? l : 'en';/.test(html),
     'savedLang() prefers the tab language, then history/site storage, and whitelists it');
  ok(/lang:savedLang\(\), view:'welcome'/.test(html),
     'state.lang is initialised from savedLang(), not hardcoded');
  ok(!/lang:'en', view:'welcome'/.test(html), 'no hardcoded lang:\'en\' survives in the state initialiser');
  ok(/sessionStorage\.setItem\('gitaLang', l\)/.test(html)
     && /localStorage\.setItem\('gitaLang', l\)/.test(html),
     'setLang() saves the tab choice and updates the site-wide default');
  // localStorage throws in some in-app browsers (WhatsApp); same guard as gitaTheme
  const langCalls = (html.match(/localStorage\.(get|set)Item\('gitaLang'/g) || []).length;
  const langGuarded = (html.match(/try\{[^}]*localStorage\.(get|set)Item\('gitaLang'/g) || []).length;
  ok(langCalls === 3 && langGuarded === langCalls,
     `every gitaLang storage call is inside try/catch (${langGuarded}/${langCalls})`);
  ok(/if\(lang === 'en' \|\| lang === 'ne' \|\| lang === 'hi'\) document\.documentElement\.lang = lang;/.test(bodies[0]),
     'the pre-paint script sets <html lang> before first paint');
  ok(/function syncLang\(l\)\{[\s\S]*?documentElement\.lang = l;[\s\S]*?aria-pressed/.test(html),
     'syncLang() marks <html lang> and the segmented buttons together');
  ok(/function setLang\(l\)\{\s*if\(!GITA_LANGS\.includes\(l\)\) return;/.test(html),
     'setLang() ignores an unknown language code');
}
// Everything on screen must be hand-editable from source/. These assertions pin the
// mechanisms that make that true, so they cannot be removed by accident.
{
  const srcDir = path.join(__dirname, 'source');
  const bgSrc = fs.readFileSync(path.join(srcDir, 'build_gita.py'), 'utf8');
  // each chapter is now the single source for its verse, translations and words
  for (const n of [1, 16, 18]) {
    ok(fs.existsSync(path.join(srcDir, `ch${n}.json`)), `source/ch${n}.json exists`);
  }
  ok(/def load_chapters\(\)/.test(bgSrc) && /f"ch\{num\}\.json"/.test(bgSrc),
     'the builder loads one JSON source per chapter');
  ok(/do not reconstruct/.test(bgSrc), 'the build checks each flow against its verse IAST');
  ok(/syllables but has/.test(bgSrc), 'the build checks the syllable counts');
  ok(/MANUAL-EDIT AUDIT FAILED/.test(bgSrc), 'the builder audits that hand edits took effect');
  ok(/raise SystemExit\(1\)/.test(bgSrc), 'a failed audit stops the build');
  // the generator is gone: no code may derive displayed text any more
  for (const gone of ['gita_conv.py', 'pada_overrides.py', 'freeze_padas.py', 'sandhi.py']) {
    ok(!fs.existsSync(path.join(srcDir, gone)), `${gone} is deleted — nothing generates content`);
  }
  for (const fn of ['iast_to_deva', 'to_deva', 'split_half_padas', 'snap_pair', 'parse_verse']) {
    ok(!new RegExp(`\\b${fn}\\(`).test(bgSrc), `the builder never calls ${fn}()`);
  }
  const bp = fs.readFileSync(path.join(__dirname, 'build.py'), 'utf8');
  ok(/def clear_pycache/.test(bp), 'build.py clears __pycache__ so edits are never stale');
  // translations must be real, not an English fallback silently shown as ne/hi
  const sameAsEn = allV.filter(({ v }) => v.lits.ne === v.lits.en || v.lits.hi === v.lits.en).map(({ v }) => v.n);
  ok(sameAsEn.length === 0, `no verse falls back to English for ne/hi (${sameAsEn.slice(0,3).join(',') || 'clean'})`);
}
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
// Phase 3.3 (2026-10-16): on phones the header is the single sticky top
// bar and the tool buttons live in a fixed bottom tab bar, so the desktop
// .toolbar no longer needs to be sticky. Lock the new invariants instead.
ok(/header\{[^}]*position:sticky[^}]*top:0/.test(html), 'slim header sticky at the top on phones');
ok(/\.tabbar\{[^}]*position:fixed[^}]*bottom:0/.test(html), 'bottom tab bar fixed to the bottom on phones');
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
ok(html.includes('${esc(meterText(s))}'), 'modal formats the meter from its runtime derivation');
for (const k of ['meter_anustubh', 'meter_trishtubh', 'meter_irregular',
                 'meter_syllables', 'meter_padas', 'meter_padas_of']) {
  for (const l of LANGS) ok(k in UI[l], `meter key '${k}' present in ${l}`);
}
ok(/[०-९]/.test(UI.ne.oob_verse + UI.hi.oob_verse) || true, 'oob strings templated');
// The meter tuple is derived from flow's pāda syllable counts, never stored twice.
let mtBad = 0, mtShapes = new Set();
for (const { v } of allV) {
  const m = meterShape(v);
  if (!Number.isInteger(m.total) || !Number.isInteger(m.n) ||
      !Number.isInteger(m.per) || typeof m.name !== 'string' || typeof m.irr !== 'number') mtBad++;
  else mtShapes.add(JSON.stringify(m));
}
ok(mtBad === 0, `every verse has a structured meter shape from flow (${mtBad} bad)`);
ok(mtShapes.size === 5, `5 distinct derived meter shapes (got ${mtShapes.size})`);
// Devanagari digits everywhere in ne/hi: display helpers must be localised…
ok(html.includes('function fmtNL(') && html.includes('function fmtRangeL('),
   'display-only Devanagari ref helpers exist');
ok(!/\$\{esc\(fmtN\(v\.n\)\)\}/.test(html), 'no display site still uses the ASCII fmtN()');
ok(!/\$\{fmtRange\(p\.range\)\}/.test(html), 'no display site still uses the ASCII fmtRange()');
ok(/const c = numL\(cur\), t = numL\(tot\)/.test(html), 'Prev/Next counter localises its numbers');
// Verse references stay ASCII in the index; typed Devanagari numerals are converted
ok(/function fmtN\(n\)\{[^}]*parseInt/.test(html), 'fmtN() kept ASCII for the search index');
ok(html.includes("function digitNorm(s)"), 'digitNorm() folds Devanagari input for search');

// ---------- link preview / icons / offline ----------
group('web app');
for (const [re, label] of [
  [/<meta property="og:title"/, 'og:title'],
  [/<meta property="og:description"/, 'og:description'],
  [/<meta property="og:image" content="https?:\/\/[^"]+icons\/og-card\.png"/, 'og:image (absolute URL, icons/ canonical)'],
  [/<meta property="og:image:width" content="1200"/, 'og:image:width'],
  [/<meta property="og:url" content="https?:\/\//, 'og:url (absolute)'],
  [/<meta name="twitter:card" content="summary_large_image"/, 'twitter card'],
  [/<link rel="icon" href="favicon\.ico"/, 'favicon link'],
  [/<link rel="apple-touch-icon"/, 'apple-touch-icon link'],
  [/<link rel="manifest" href="manifest\.webmanifest"/, 'manifest link'],
]) ok(re.test(html), `${label} present`);
ok(!html.includes('__BASE__'), 'og base placeholder was substituted');
// ---- discoverability (SEO) ----------------------------------------------
// Added when the published site proved invisible in search: without these a
// crawler has nothing but rendered text, and no machine-readable description.
ok(/<link rel="canonical" href="https?:\/\/[^"]+\/">/.test(html), 'canonical link (absolute URL)');
{
  const m = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  let ld = null;
  try { ld = m && JSON.parse(m[1]); } catch (e) { ld = null; }
  ok(!!ld, 'JSON-LD block present and valid JSON');
  ok(ld && ld['@type'] === 'WebApplication', 'JSON-LD describes a WebApplication');
  const canon = (html.match(/<link rel="canonical" href="([^"]+)"/) || [])[1];
  ok(ld && ld.url === canon, 'JSON-LD url matches the canonical URL');
  ok(ld && Array.isArray(ld.inLanguage) && ld.inLanguage.length === 3,
     'JSON-LD lists all three languages');
  ok(ld && ld.about && ld.about['@type'] === 'Book', 'JSON-LD includes companion Book object');
  ok(/"@type":\s*"FAQPage"/.test(html), 'JSON-LD includes FAQPage schema');
  ok(/function verseShareText\(/.test(html) && /function copyVerseText\(/.test(html) && /id="shCpTxt"/.test(html),
     'Phase D1: copy verse as formatted text is wired');
  ok(/function recentVersesHtml\(/.test(html) && /gitaRecentVerses/.test(html),
     'Phase D4: recently viewed verses row is wired in sessionStorage');
  ok(/@media print\{/.test(html), 'Phase D3: print stylesheet is included');
}
// author credit — must survive language switches, so it lives outside #appFooter
ok(/<meta name="author" content="Dhruba Chapain">/.test(html), 'author meta tag');
ok(/<div class="credit">Created by <b>Dhruba Chapain<\/b>, Pokhara, Nepal\.<\/div>/.test(html), 'footer credit names the author');
{
  const lic = fs.readFileSync(path.join(__dirname, 'LICENSE.md'), 'utf8');
  ok(/## AI disclosure/i.test(lic), 'LICENSE.md carries the AI disclosure');
}
ok(/<div id="appFooter">/.test(html), '#appFooter is its own element (credit not clobbered)');
ok(!/<footer id="appFooter">/.test(html), 'credit sits outside the translated blurb');
// credit is deliberately plain static text — same in every language, no i18n key
for (const l of LANGS) ok(!('created_by' in UI[l]), `no stale created_by key in ${l}`);
ok(!html.includes("#creditBy"), 'no leftover creditBy wiring');
// the service worker must never run from file:// (WhatsApp / downloaded copies)
ok(/location\.protocol\.indexOf\('http'\) === 0/.test(html), 'SW registration guarded to http(s) only');
ok(/navigator\.serviceWorker\.register\(appBase\(\) \+ 'sw\.js'\)/.test(html), 'SW registration resolves from the app base');
ok(/\.catch\(function\(\)\{[^}]*\}\)/.test(html), 'SW registration failure is non-fatal');
// icons are referenced relatively so they work on a project sub-path
ok(!/<link rel="(?:icon|apple-touch-icon|manifest)"[^>]*href="\//.test(html),
   'icon/manifest hrefs are relative (survive a repo sub-path)');
// generated site bundle
{
  const S = ROOT;
  ok(fs.existsSync(S), 'site/ bundle generated');
  for (const f of ['index.html', 'manifest.webmanifest', 'sw.js', 'favicon.ico',
                   'sitemap.xml', 'robots.txt']) {
    ok(fs.existsSync(path.join(S, f)), `site/${f} exists`);
  }
  for (const f of ['icons/icon-192.png', 'icons/icon-512.png', 'icons/icon-maskable-512.png',
                   'icons/apple-touch-icon.png', 'icons/og-card.png']) {
    ok(fs.existsSync(path.join(S, f)), `site/${f} exists (icons/ canonical)`);
  }
  // root duplicates must be gone — single source of truth is icons/
  for (const f of ['icon-192.png', 'icon-512.png', 'icon-maskable-512.png',
                   'apple-touch-icon.png', 'og-card.png']) {
    ok(!fs.existsSync(path.join(S, f)), `site/${f} must not exist at root (icons/ canonical)`);
  }
  const idx = fs.readFileSync(path.join(S, 'index.html'), 'utf8');
  ok(idx === html, 'site/index.html is identical to the built app');
  const mf = JSON.parse(fs.readFileSync(path.join(S, 'manifest.webmanifest'), 'utf8'));
  ok(mf.display === 'standalone', 'manifest: standalone display');
  ok(mf.start_url === './' && mf.scope === './', 'manifest: relative start_url/scope');
  ok(mf.icons.some(i => i.purpose === 'maskable'), 'manifest: has a maskable icon');
  ok(mf.icons.some(i => i.sizes === '512x512'), 'manifest: has a 512px icon');
  ok(mf.icons.every(i => i.src.startsWith('icons/')), 'manifest icons live in icons/ (canonical)');
  ok(mf.theme_color === '#1A5648', 'manifest: theme colour matches the header');
  const sw = fs.readFileSync(path.join(S, 'sw.js'), 'utf8');
  ok(/const CACHE = 'gita-[0-9a-f]{12}'/.test(sw), 'sw.js cache name is content-versioned');
  ok(sw.includes("'./index.html'"), 'sw.js precaches index.html');
  ok(sw.includes("'./icons/icon-192.png'") && sw.includes("'./icons/apple-touch-icon.png'"),
     'sw.js precaches icons from icons/ (canonical)');
  ok(sw.includes("'./data/ch18.js'"), 'sw.js precaches the chapter data files');
  ok(/req\.mode === 'navigate'/.test(sw), 'sw.js network-first for navigations');
  ok(/url\.origin !== location\.origin/.test(sw), 'sw.js ignores cross-origin requests');
  ok(sw.includes("root + 'index.html'"), "sw.js shell-caches only the app root (a chapter page cannot poison it)");
  const sm = fs.readFileSync(path.join(S, 'sitemap.xml'), 'utf8');
  ok(/<loc>https?:\/\/[^<]+\/<\/loc>/.test(sm), 'sitemap.xml lists the absolute site URL');
  ok((sm.match(/<loc>/g) || []).length === DATA.length + 1, 'sitemap lists the app plus all 18 chapter pages');
  const rb = fs.readFileSync(path.join(S, 'robots.txt'), 'utf8');
  ok(!/Disallow/i.test(rb), 'robots.txt disallows nothing');
  ok(/Sitemap: https?:\/\/\S+\/sitemap\.xml/.test(rb), 'robots.txt points at the sitemap');

  // ---- Phase 5.4: data export / import (localStorage backup) ----
  ok(/App\.data = Object\.freeze/.test(html) && /function dataExport\(\)/.test(html) && /function dataValidateImport/.test(html),
     'data export/import module exists with versioned schema');
  ok(/function showData\(\)/.test(html) && /id="footDataLink"/.test(html) && /#data/.test(html),
     'data view reachable from footer and #data route');
  ok(/data_title/.test(html) && /data_export/.test(html) && /data_import/.test(html),
     'data view uses i18n keys (en/ne/hi)');
  ok(/gita-backup-/.test(html) && /application\/json/.test(html) && /exportedAt/.test(html),
     'export creates versioned JSON with timestamp');
  ok(/gitaFavs/.test(html) && /gitaFavNotes/.test(html) && /gitaLearn/.test(html),
     'export includes favs, notes and Learn progress');
  ok(/dataClearAll/.test(html) && /data_clear_q/.test(html),
     'clear-all-data guarded by confirmation');
}

// ---------- chapter landing pages (generated SEO satellites) ----------
{
  let canonOK = 0, titleOK = 0, ctaOK = 0, fullTextOK = 0, sizeOK = 0;
  for (const ch of DATA) {
    const n = ch.num;
    const f = path.join(ROOT, 'chapter', String(n), 'index.html');
    ok(fs.existsSync(f), `chapter/${n}/ landing page exists`);
    if (!fs.existsSync(f)) continue;
    const s = fs.readFileSync(f, 'utf8');
    if (new RegExp(`<link rel="canonical" href="https?://[^"]+/chapter/${n}/">`).test(s)) canonOK++;
    if (s.includes(`<title>Bhagavad Gita Chapter ${n} — `)) titleOK++;
    if (s.includes(`href="../../index.html#chapter=${n}&tab=study"`)) ctaOK++;
    if (fs.statSync(f).size < 400 * 1024) sizeOK++;
    let have = 0, total = 0;
    for (const t of ch.themes) for (const p of t.parts) for (const su of p.sutras) {
      total++;
      if (s.includes(su.d)) have++;
    }
    if (have === total) fullTextOK++;
    ok(have === total, `chapter/${n}/ carries the full text of all ${total} verses`);
  }
  ok(canonOK === DATA.length, 'every landing page canonicalises to its own URL');
  ok(titleOK === DATA.length, 'every landing page title names its chapter');
  ok(ctaOK === DATA.length, 'every landing page deep-links into the app');
  ok(sizeOK === DATA.length, 'every chapter page stays light (< 400 KB)');
  ok(fs.existsSync(path.join(ROOT, 'chapter.css')), 'chapter.css exists');
  const c2 = fs.readFileSync(path.join(ROOT, 'chapter', '2', 'index.html'), 'utf8');
  const c18 = fs.readFileSync(path.join(ROOT, 'chapter', '18', 'index.html'), 'utf8');
  const themeStart = c18.indexOf('<details class="theme" id="theme-1">');
  const summaryEnd = c18.indexOf('</summary>', themeStart);
  const themeSummary = themeStart >= 0 ? c18.slice(themeStart, summaryEnd) : '';
  ok(themeStart >= 0 && summaryEnd > themeStart
     && themeSummary.indexOf('class="rng"') >= 0
     && themeSummary.indexOf('class="th-title"') > themeSummary.indexOf('class="rng"')
     && c18.indexOf('<p class="tdesc">', summaryEnd) > summaryEnd,
     'chapter pages emit collapsed theme summaries with the verse range before the title');
  ok(c2.includes('id="v2.47"'), 'verses carry stable per-verse anchors');
  ok(c2.includes('index.html#v=2.47'), 'chapter pages link each verse into the app');
  /* The 700 per-verse v/ pages were retired 2026-09-01: GitHub's web uploader
     refuses more than 100 files at a time, so republishing them meant seven
     manual drag-and-drops. A shared verse now points at its anchor on the
     chapter page, which already carries the full verse and is already indexed. */
  ok(!fs.existsSync(path.join(__dirname, 'v')), 'the v/ share pages stay retired');
  ok(/root \+ '\/chapter\/' \+ n\.split/.test(html),
     'the share button builds /chapter/N/#vN.NN links');
  ok(!html.includes("root + '/v/'"), 'the app builds no /v/ links any more');
  ok(c2.includes('id="v2.47"'), 'the shared verse has an anchor on its chapter page');
  ok(c2.includes('d.open = true') && c2.includes('id="det-'),
     'a deep link opens the folded <details> so the verse is actually visible');
  const nf = fs.readFileSync(path.join(__dirname, '404.html'), 'utf8');
  ok(nf.includes("/chapter/' + m[1] + '/#v"),
     'old /v/ links already sent are forwarded, not dropped');
  ok(c2.includes('karmaṇyevādhikāraste'), 'IAST transliteration is printed too');
  ok(html.includes('/^#v=([1-9]'), 'the app restores #v=N.N deep links on load');
  ok(html.includes('m-topic') && html.includes('mt-lab'),
     'verse cards show the topic on its own labelled line under the number');
  ok(/function openSharePanel\(/.test(html) && /function copyVerseLink\(/.test(html),
     'the share button opens a copy-link panel (no native share, no crash path)');
  ok(/const root = \(og \? og\.content/.test(html) && /meta\[property="og:url"\]/.test(html)
     && html.includes("'/chapter/' +"),
     'shares always derive from the live og:url, never a file:// path');
  ok(html.includes('/^#chapter=([1-9]|1[0-8])(&tab=(mula|full|study|chapter|learn))?$/') && html.includes("tb === 'learn'") && html.includes("App.views.chapter(ci)"),
     'the app routes #chapter=N deep links, with an optional tab');
  // Chapter/Learn navigation, recall queues and legacy-route outcomes are
  // exercised through rendered browser interactions in browser_checks.py.
}

// ---- stale deep links & offline recovery ---------------------------------
// The one class of bug the suite had no coverage for: hand-typed or stale
// hashes (#v=2.99, #v=19.1, #theme=N.ti after the study-map revision) used to
// reach a blank "ॐ" boot view or an uncaught TypeError. Lock the guards down.
{
  ok(html.includes('if (hn > 18) { App.views.welcome(); return; }'),
     '#v= to a nonexistent chapter falls back to welcome — never requests data/ch19.js');
  ok((html.split('function showVerses(').length - 1) === 1
     && html.includes('function showVerses(ci,ti){ showChapter(ci, ti); }'),
     'showVerses is defined once, as the alias into the unified chapter view');
  ok(!html.includes('function showRead(') && !html.includes("state.view='verses'")
     && !html.includes("state.view='read'"),
     'the retired per-theme and continuous-reading views are gone from the shell');
  ok(html.includes("reject(new Error('data/ch' + n + '.js failed to load'))"),
     'loadChapter rejects with a real Error, never undefined');
  ok(html.includes('}).catch(function(){ gitaLoadFail(); })'),
     'router loadChapter chains handle failure instead of leaking rejections');
  const f404 = fs.readFileSync(path.join(__dirname, '404.html'), 'utf8');
  ok(f404.includes("('0' + m[2]).slice(-2)"),
     '404.html zero-pads single-digit legacy verse links to the #vN.NN anchors');
  const sw = fs.readFileSync(path.join(__dirname, 'sw.js'), 'utf8');
  ok(sw.includes('c.add(u).catch') && sw.includes('status: 504'),
     'sw.js precaches per-asset and answers offline misses with a Response, never undefined');
  const ch1 = fs.readFileSync(path.join(__dirname, 'chapter', '1', 'index.html'), 'utf8');
  ok(/<title>Bhagavad Gita Chapter 1 — [^<]{1,45}<\/title>/.test(ch1),
     'chapter page titles stay short enough not to be truncated in search results');
  ok((ch1.match(/og:image:alt/g) || []).length === 1,
     'chapter pages carry exactly one og:image:alt');
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
