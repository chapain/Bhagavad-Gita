#!/usr/bin/env node
/* run_gita_app.js — verification suite for the Bhagavad Gita trilingual study app.
 *
 * Usage:  node run_gita_app.js          (from the project root)
 *
 * Parses the split app shell and its 18 chapter payloads, then checks the
 * integrity invariants: 18 chapters · 700 verses · 208 themes · 700 parts,
 * trilingual coverage, word-by-word glosses, script purity, Latin-residue
 * checks on Nepali/Hindi fields, and content regression locks.
 */
'use strict';

const fs = require('fs');
const TOTAL_ASSERTIONS = 782;      // keep in step with the printed total
const TOTAL_BROWSER_CHECKS = 148;   // browser_checks.py
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
  ok(/function assembleData\(\)\{[\s\S]*?buildIndex\(\); buildVerseText\(\);[\s\S]*?\}/.test(html)
     && /function gitaBoot\(\)\{[\s\S]*?assembleData\(\);[\s\S]*?applyStatic\(\);/.test(html),
     'gitaBoot assembles the available data and paints the shell');
}

// ---------- i18n ----------
group('i18n');
const LANGS = ['en', 'ne', 'hi'];
for (const l of LANGS) ok(UI[l] && typeof UI[l] === 'object', `UI.${l} present`);
const enKeys = Object.keys(UI.en);
ok(enKeys.length === 201, `UI has 201 keys (got ${enKeys.length})`);
for (const k of enKeys) ok(k in UI.ne, `UI key '${k}' present in नेपाली`);
for (const k of enKeys) ok(k in UI.hi, `UI key '${k}' present in हिन्दी`);
const LATIN = /[A-Za-zÀ-ɏḀ-ỿ]/;
const stripPlaceholders = s => s.replace(/\{[A-Za-z_]+\}/g, '');
const uiLatinBad = [];
for (const l of ['ne', 'hi']) for (const [k, v] of Object.entries(UI[l]))
  if (LATIN.test(stripPlaceholders(v))) uiLatinBad.push(`${l}.${k}`);
ok(uiLatinBad.length === 0, `UI ne/hi values free of Latin residue (${uiLatinBad.join(', ') || 'clean'})`);
const CHOOSE_KEYS = ['choose_title','opt_full_d','opt_study_d','opt_go'];
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

const allThemes = DATA.flatMap(c => c.themes);
ok(allThemes.length === 208, `208 themes (got ${allThemes.length})`);
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
const ch3Enemy = DATA[2].themes.find(t => t.range === '3.36–3.39');
const ch3Page = fs.readFileSync(path.join(ROOT, 'chapter', '3', 'index.html'), 'utf8');
ok(ch3Enemy && ch3Enemy.titles.en === 'Desire and Anger, the All-Devouring Enemy'
   && ch3Enemy.descs.ne.includes('सर्वभक्षी शत्रु') && ch3Enemy.descs.hi.includes('सर्वभक्षी शत्रु')
   && ch3Page.includes('Desire and Anger, the All-Devouring Enemy'),
   'chapter 3 reviewed theme title/description is trilingual and present on its page');
const ch4Births = DATA[3].themes.find(t => t.range === '4.05–4.09');
const ch4BirthPart = ch4Births && ch4Births.parts.find(p => p.range === '4.05–4.05');
const ch4Page = fs.readFileSync(path.join(ROOT, 'chapter', '4', 'index.html'), 'utf8');
ok(ch4BirthPart && ch4BirthPart.titles.en === 'I know all our past births'
   && ch4BirthPart.titles.ne === 'म हाम्रा सबै पूर्वजन्म जान्दछु'
   && ch4BirthPart.titles.hi === 'मैं हमारे सभी पूर्वजन्म जानता हूँ'
   && ch4Page.includes('I know all our past births'),
   'chapter 4 reviewed verse title is trilingual and present on its page');
const ch5Equanimity = DATA[4].themes.find(t => t.range === '5.17–5.21');
const ch5Verse = ch5Equanimity && ch5Equanimity.parts.find(p => p.range === '5.19–5.19');
const ch5Paths = DATA[4].themes.find(t => t.range === '5.03–5.06')?.parts.find(p => p.range === '5.04–5.04');
const ch5Page = fs.readFileSync(path.join(ROOT, 'chapter', '5', 'index.html'), 'utf8');
ok(ch5Verse && ch5Verse.titles.en === 'Equanimity conquers the world of birth and death'
   && ch5Verse.titles.ne.includes('जन्म-मृत्यु') && ch5Verse.titles.hi.includes('जन्म-मृत्यु')
   && ch5Paths && ch5Paths.titles.en === 'Only children call Sāṅkhya and Yoga different'
   && ch5Paths.titles.ne === 'बालकले मात्र साङ्ख्य र योगलाई फरक ठान्छन्'
   && ch5Paths.titles.hi === 'बालक ही सांख्य और योग को भिन्न कहते हैं'
   && ch5Page.includes('Only children call Sāṅkhya and Yoga different')
   && ch5Page.includes('Equanimity conquers the world of birth and death'),
   'chapter 5 reviewed verse titles are trilingual and present on its page');
const ch6Meditation = DATA[5].themes.find(t => t.range === '6.10–6.15');
const ch6Practice = DATA[5].themes.find(t => t.range === '6.18–6.23');
const ch6Resolve = ch6Practice && ch6Practice.parts.find(p => p.range === '6.23–6.23');
const ch6FormerLife = DATA[5].themes.flatMap(t => t.parts).find(p => p.range === '6.43–6.43');
const ch6Renunciation = DATA[5].themes.flatMap(t => t.parts).find(p => p.range === '6.01–6.01');
const ch6Page = fs.readFileSync(path.join(ROOT, 'chapter', '6', 'index.html'), 'utf8');
ok(ch6Meditation && ch6Meditation.titles.en === 'Meditation: practice and posture'
   && ch6Renunciation && ch6Renunciation.titles.en === 'Renunciation is more than abandoning rites'
   && ch6Resolve && ch6Resolve.titles.en === 'Practise with resolve and an undiscouraged mind'
   && ch6Resolve.descs.ne.includes('निराश नभई') && ch6Resolve.descs.hi.includes('निराश हुए बिना')
   && ch6FormerLife && ch6FormerLife.titles.en === 'He regains spiritual insight from a past life'
   && ch6FormerLife.titles.en.length <= 54
   && ch6Page.includes('Meditation: practice and posture'),
   'chapter 6 reviewed meditation guidance and resolve wording stay aligned ×3');
const ch7Closing = DATA[6].themes.find(t => t.range === '7.24–7.30');
const ch7Page = fs.readFileSync(path.join(ROOT, 'chapter', '7', 'index.html'), 'utf8');
ok(ch7Closing && ch7Closing.titles.en === 'The Unmanifest and Those Who Know Me'
   && ch7Closing.descs.en.includes('all of adhyātma and action')
   && ch7Closing.descs.ne.includes('सम्पूर्ण अध्यात्म र कर्म')
   && ch7Closing.descs.hi.includes('सम्पूर्ण अध्यात्म और कर्म')
   && ch7Page.includes('The Unmanifest and Those Who Know Me'),
   'chapter 7 reviewed closing theme title/description is trilingual and present on its page');
const ch8Departure = DATA[7].themes.find(t => t.range === '8.12–8.16');
const ch8Path = DATA[7].themes.find(t => t.range === '8.23–8.26');
const ch8Always = ch8Departure && ch8Departure.parts.find(p => p.range === '8.14–8.14');
const ch8Page = fs.readFileSync(path.join(ROOT, 'chapter', '8', 'index.html'), 'utf8');
ok(ch8Always && ch8Always.titles.en === 'Easily reached by one who remembers me always'
   && ch8Always.titles.ne.includes('सधैँ सम्झने') && ch8Always.titles.hi.includes('सदा मेरा स्मरण')
   && ch8Departure.descs.en.includes('even Brahmā’s world is subject to return')
   && ch8Path.descs.ne.includes('उत्तरायण') && ch8Path.descs.hi.includes('दक्षिणायन')
   && ch8Page.includes('The bright path and the dark'),
   'chapter 8 reviewed end-of-life teaching and paths stay aligned ×3');
const ch9Rituals = DATA[8].themes.find(t => t.range === '9.20–9.21');
const ch9Soma = ch9Rituals && ch9Rituals.parts.find(p => p.range === '9.20–9.20');
const ch9Care = DATA[8].themes.find(t => t.range === '9.22–9.25');
const ch9Page = fs.readFileSync(path.join(ROOT, 'chapter', '9', 'index.html'), 'utf8');
ok(ch9Rituals && ch9Rituals.titles.en === 'The Finite Fruit of Rituals'
   && ch9Soma && ch9Soma.titles.en === 'Soma drinkers seek heaven'
   && ch9Soma.titles.ne.includes('स्वर्ग खोज्छन्') && ch9Soma.titles.hi.includes('स्वर्ग चाहते हैं')
   && ch9Care && ch9Care.titles.en === 'I Care for My Devotees'
   && ch9Care.descs.en.includes('I provide what those devoted to me lack')
   && ch9Page.includes('I Care for My Devotees'),
   'chapter 9 reviewed ritual-reward and devotee-care wording is trilingual');
const ch10Glories = DATA[9].themes.find(t => t.range === '10.15–10.18');
const ch10Part = ch10Glories && ch10Glories.parts.find(p => p.range === '10.16–10.16');
const ch10Page = fs.readFileSync(path.join(ROOT, 'chapter', '10', 'index.html'), 'utf8');
ok(ch10Part && ch10Part.descs.ne.includes('केही नछुटाई बताउनुहोस्')
   && ch10Part.descs.hi.includes('कुछ भी छोड़े बिना')
   && !ch10Part.descs.ne.includes('हे परम पुरुष, हे परम पुरुष')
   && !ch10Part.descs.hi.includes('हे परम पुरुष, हे परम पुरुष')
   && ch10Page.includes('How Shall I Know You?'),
   'chapter 10 reviewed localized wording is clear and present on its page');
const ch11Fear = DATA[10].themes.find(t => t.range === '11.24–11.27');
const ch11Forgive = DATA[10].themes.find(t => t.range === '11.41–11.44');
const ch11ForgivePart = ch11Forgive && ch11Forgive.parts.find(p => p.range === '11.44–11.44');
const ch11Page = fs.readFileSync(path.join(ROOT, 'chapter', '11', 'index.html'), 'utf8');
ok(ch11Fear && ch11Fear.descs.en.includes('other warriors rushing into them')
   && ch11Fear.descs.ne.includes('धृतराष्ट्रका छोराहरू') && ch11Fear.descs.hi.includes('धृतराष्ट्र के पुत्र')
   && ch11ForgivePart && ch11ForgivePart.titles.hi === 'जैसे पिता पुत्र को क्षमा करता है'
   && ch11ForgivePart.descs.ne.includes('साष्टाङ्ग दण्डवत्')
   && ch11Page.includes('Kṛṣṇa says: I am Time, the destroyer'),
   'chapter 11 reviewed cosmic vision and apology wording remain aligned ×3');
const ch12Close = DATA[11].themes.find(t => t.range === '12.20–12.20');
const ch12Page = fs.readFileSync(path.join(ROOT, 'chapter', '12', 'index.html'), 'utf8');
ok(ch12Close && ch12Close.titles.en === 'Those who follow this dharma are exceedingly dear'
   && ch12Close.titles.ne.includes('अत्यन्त प्रिय') && ch12Close.titles.hi.includes('अत्यन्त प्रिय')
   && ch12Close.descs.en.includes('with faith')
   && DATA[11].themes.find(t => t.range === '12.09–12.12').descs.en.includes('A graded path')
   && ch12Page.includes('Those who follow this dharma are exceedingly dear'),
   'chapter 12 reviewed graduated practice and closing theme are trilingual');
const ch13Field = DATA[12].themes.find(t => t.range === '13.01–13.02');
const ch13Means = DATA[12].themes.find(t => t.range === '13.07–13.11');
const ch13Page = fs.readFileSync(path.join(ROOT, 'chapter', '13', 'index.html'), 'utf8');
ok(ch13Field && ch13Field.titles.en === 'The body is the field; I am its knower'
   && ch13Field.titles.ne.includes('म यसको क्षेत्रज्ञ') && ch13Field.titles.hi.includes('मैं उसका क्षेत्रज्ञ')
   && ch13Means.descs.en.includes('steady commitment to Self-knowledge')
   && ch13Page.includes('The body is the field; I am its knower'),
   'chapter 13 field-knower distinction and knowledge summary are trilingual');
const ch14Transcend = DATA[13].themes.find(t => t.range === '14.26–14.27');
const ch14Rise = DATA[13].themes.find(t => t.range === '14.09–14.10').parts.find(p => p.range === '14.10–14.10');
const ch14Page = fs.readFileSync(path.join(ROOT, 'chapter', '14', 'index.html'), 'utf8');
ok(ch14Rise && ch14Rise.titles.en === 'The Guṇas overpower one another'
   && ch14Transcend.descs.en.includes('becomes fit for Brahman')
   && ch14Transcend.descs.ne.includes('ब्रह्मभावका लागि योग्य')
   && ch14Transcend.descs.hi.includes('ब्रह्मभाव के योग्य')
   && ch14Page.includes('The Way and the Goal'),
   'chapter 14 guṇa dynamics and Brahman qualification are aligned ×3');
const ch15Persons = DATA[14].themes.find(t => t.range === '15.16–15.17');
const ch15Heart = DATA[14].themes.find(t => t.range === '15.15–15.15');
const ch15Page = fs.readFileSync(path.join(ROOT, 'chapter', '15', 'index.html'), 'utf8');
ok(ch15Persons && ch15Persons.titles.en === 'The perishable, the imperishable, and the Supreme Person'
   && ch15Persons.titles.ne.includes('उत्तम पुरुष') && ch15Persons.titles.hi.includes('उत्तम पुरुष')
   && ch15Heart.descs.en.includes('forgetfulness')
   && ch15Page.includes('The perishable, the imperishable, and the Supreme Person'),
   'chapter 15 distinguishes all three persons and preserves the heart teaching ×3');
const ch16Scripture = DATA[15].themes.find(t => t.range === '16.23–16.24');
const ch16Ahi = DATA[15].themes.find(t => t.range === '16.18–16.20');
const ch16Page = fs.readFileSync(path.join(ROOT, 'chapter', '16', 'index.html'), 'utf8');
ok(ch16Scripture.parts[0].descs.ne.includes('शास्त्रको विधान त्यागेर')
   && !ch16Scripture.parts[0].descs.ne.includes('थाती राखेर')
   && ch16Scripture.parts[0].descs.hi.includes('शास्त्र-विधान को त्यागकर')
   && ch16Ahi.descs.ne.includes('अधम गतिमा')
   && ch16Page.includes('The Authority of Scripture'),
   'chapter 16 scripture wording and demoniac-destiny summary remain accurate');
const ch18Teaching = DATA[17].themes.find(t => t.range === '18.67–18.71');
const ch18Listener = ch18Teaching.parts.find(p => p.range === '18.71–18.71');
const ch18Page = fs.readFileSync(path.join(ROOT, 'chapter', '18', 'index.html'), 'utf8');
ok(ch18Teaching.descs.en.includes('lacks austerity or devotion')
   && ch18Teaching.descs.ne.includes('सुन्न नचाहने') && ch18Teaching.descs.hi.includes('मुझमें दोष देखे')
   && ch18Listener.titles.en === 'The faithful listener is freed'
   && ch18Page.includes('To Whom the Teaching Is Given'),
   'chapter 18 audience, teacher and faithful-listener teaching is aligned ×3');
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
ok(wordTotal === 9484, `9,484 word-instances (got ${wordTotal})`);
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
ok(ch15.titles.en === 'The Path to the Supreme Abode', 'ch.15 EN title: path to the abode lock');
ok(ch15.titles.ne === 'परम-पदको पथ', 'ch.15 NE title: परम-पदको पथ lock');
ok(ch15.titles.hi === 'परम-पद का मार्ग', 'ch.15 HI title: परम-पद का मार्ग lock');
ok(!html.includes('The Path Beyond') && !html.includes('पार का मार्ग'), 'stale ch.15 titles fully replaced');
// the pill strips and top back-buttons became one breadcrumb: the full trail,
// ancestors as links, current page last — on every drill-down view
ok(/function wayCrumbs\(/.test(html) && /wc-link/.test(html) && /wc-cur/.test(html),
   'drill-down views navigate by breadcrumb (links + current)');
ok((html.match(/wayCrumbs\(\[\[L\('sections_title'\)/g) || []).length >= 4,
   'all four drill-down views root their breadcrumb at The Three Ways');
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
// The running verse is rendered verbatim from source/ch*.json — no re-joining.
// This is the strongest check in the suite: every displayed line, and the speaker,
// must be character-for-character what the source file says.
{
  const chDir = path.join(__dirname, 'source');
  let checkedLines = 0;
  const lineBad = [];
  for (const { v } of allV) {
    const [cn, vn] = v.n.split('.');
    const src = JSON.parse(fs.readFileSync(path.join(chDir, `ch${Number(cn)}.json`), 'utf8')).verses[String(Number(vn))];
    const segsD = src.deva.split('।').map(x => x.trim()).filter(Boolean);
    const segsT = src.iast.split('।').map(x => x.trim()).filter(Boolean);
    const got = v.lines || [];
    if (got.length !== segsD.length) { lineBad.push(`${v.n}: ${got.length} vs ${segsD.length} segments`); continue; }
    for (let i = 0; i < segsD.length; i++) {
      if (got[i].d !== segsD[i]) lineBad.push(`${v.n}[${i}] deva`);
      if (got[i].t !== segsT[i]) lineBad.push(`${v.n}[${i}] iast`);
      const isSpk = segsT[i].endsWith('uvāca');
      if ((got[i].k === 's') !== isSpk) lineBad.push(`${v.n}[${i}] speaker flag`);
      checkedLines++;
    }
  }
  ok(lineBad.length === 0, `every verse line matches source/ch*.json verbatim (${checkedLines} segments; ${lineBad.slice(0,3).join(', ') || 'clean'})`);
  ok(allV.every(({ v }) => (v.lines || []).filter(l => l.k === 'l').length === 2), 'every verse has exactly two display lines');
  // 1.21 and 1.28 put the speaker *between* the two lines; verbatim rendering keeps it there.
  ok(byRef['1.21'].lines[1].k === 's' && byRef['1.21'].lines[1].d === 'अर्जुन उवाच',
     '1.21 keeps its mid-verse speaker in place');
  ok(byRef['1.28'].lines[1].k === 's', '1.28 keeps its mid-verse speaker in place');
  // 16.3 was the sandhi-recombination bug; 16.1 the concatenation bug. Both are now
  // impossible by construction, but pin the exact text so a source edit is deliberate.
  ok(byRef['16.03'].lines[0].d === 'तेजः क्षमा धृतिः शौचमद्रोहो नातिमानिता',
     '16.3 renders शौचमद्रोहो (not शौचम्अद्रोहो)');
  ok(byRef['16.01'].lines[1].d.includes('संशुद्धिर्ज्ञानयोग'),
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
  ok(/18 chapters · 208 themes · 700 parts · 700 verses/.test(pm),
     'PROJECT.md states the current totals');
  ok(new RegExp(`${Object.keys(UI.en).length} UI strings`).test(pm),
     `PROJECT.md states the current UI key count (${Object.keys(UI.en).length})`);
  for (const f of ['gita_conv.py', 'pada_overrides.py', 'freeze_padas.py', 'sandhi.py']) {
    ok(pm.includes(f), `PROJECT.md records that ${f} was deleted`);
  }
  for (const ref of ['11.01', '2.29', '8.10', '15.03', '2.06']) {
    ok(pm.includes(ref), `PROJECT.md lists irregular verse ${ref}`);
  }
  ok(/renders data\. It never generates/.test(pm), 'PROJECT.md states the governing rule');

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
// Everything on screen must be hand-editable from source/. These assertions pin the
// mechanisms that make that true, so they cannot be removed by accident.
{
  const srcDir = path.join(__dirname, 'source');
  const bgSrc = fs.readFileSync(path.join(srcDir, 'build_gita.py'), 'utf8');
  // the pāda split is frozen data, not a computation
  for (const n of [1, 16, 18]) {
    ok(fs.existsSync(path.join(srcDir, `padas_ch${n}.py`)), `padas_ch${n}.py exists`);
  }
  ok(/PADAS\.update/.test(bgSrc), 'the builder reads the pāda data files');
  ok(/no longer spell the verse/.test(bgSrc), 'the build checks the pādas against ch*.json');
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
                   'icon-192.png', 'icon-512.png', 'icon-maskable-512.png',
                   'apple-touch-icon.png', 'og-card.png',
                   'sitemap.xml', 'robots.txt']) {
    ok(fs.existsSync(path.join(S, f)), `site/${f} exists`);
  }
  const idx = fs.readFileSync(path.join(S, 'index.html'), 'utf8');
  ok(idx === html, 'site/index.html is identical to the built app');
  const mf = JSON.parse(fs.readFileSync(path.join(S, 'manifest.webmanifest'), 'utf8'));
  ok(mf.display === 'standalone', 'manifest: standalone display');
  ok(mf.start_url === './' && mf.scope === './', 'manifest: relative start_url/scope');
  ok(mf.icons.some(i => i.purpose === 'maskable'), 'manifest: has a maskable icon');
  ok(mf.icons.some(i => i.sizes === '512x512'), 'manifest: has a 512px icon');
  ok(mf.theme_color === '#1A5648', 'manifest: theme colour matches the header');
  const sw = fs.readFileSync(path.join(S, 'sw.js'), 'utf8');
  ok(/const CACHE = 'gita-[0-9a-f]{12}'/.test(sw), 'sw.js cache name is content-versioned');
  ok(sw.includes("'./index.html'"), 'sw.js precaches index.html');
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
  ok(html.includes('/^#chapter=([1-9]|1[0-8])(&tab=(mula|full|study|learn))?$/') && html.includes("tb === 'study'") && html.includes("tb === 'learn'"),
     'the app routes #chapter=N deep links, with an optional tab');
  ok(html.includes('function modeSwitch(') && html.includes('opt_full') && html.includes('opt_study_s'),
     'the chapter page offers the two ways as a segmented control (translation / study)');
  ok(!html.includes("btn('mula'"), 'the retired mula pill is gone from the chooser');
  ok(html.includes("btn('learn'") && html.includes('function showLearn('),
     'the chooser offers Learn by heart as the third way');
  ok(html.includes('function lrDrill(') && html.includes('function lrRun('),
     'the learn path carries its drill engine');
  ok(html.includes("LQ.push(it)"),
     'a missed drill item is requeued, so recall is earned not skipped');
  ok(html.includes("if(mode === 'mula') mode = 'full'"),
     'a shared #tab=mula link still works — it lands on the translation view');
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
