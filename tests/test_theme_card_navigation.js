#!/usr/bin/env node
'use strict';
/* Exercise the emitted chapter cards and verse lookup, not a reimplementation.
   Only unrelated UI helpers and the modal's DOM effects are stubbed. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
const lookupStart = html.indexOf('function sutraAt(');
const lookupEnd = html.indexOf('\n', lookupStart) + 1;
const start = html.indexOf('function showChapter(ci, anchorTi){');
const end = html.indexOf('// pāda display:', start);
assert(lookupStart >= 0 && lookupEnd > lookupStart && start >= 0 && end > start,
  'built showChapter() and sutraAt() must be present');
const code = html.slice(lookupStart, lookupEnd) + html.slice(start, end);
assert(code.includes('function sutraAt('), 'test must use the built verse lookup');

const DATA = Array.from({length: 18}, (_, ci) => {
  const raw = fs.readFileSync(path.join(ROOT, 'data', `ch${ci + 1}.js`), 'utf8');
  const match = raw.match(/^GITA_CH\[(\d+)\] = ([\s\S]*);\s*$/);
  assert(match && Number(match[1]) === ci + 1, `built chapter ${ci + 1} payload`);
  return JSON.parse(match[2]);
});
const view = {innerHTML: ''};
let opened = [];
function openVerse(ci, ti, si, mode, navIdx, invoker) {
  // Resolve the card's arguments with the actual emitted lookup. The full
  // modal's DOM machinery is deliberately outside this focused test.
  opened.push({ci, ti, si, mode, navIdx, invoker,
    verse: ctx.sutraAt(DATA[ci].themes[ti], si).s.n});
}
const ctx = vm.createContext({
  DATA,
  GITA_CH: Object.fromEntries(DATA.map(ch => [ch.num, ch])),
  state: {lang: 'en', section: null},
  view,
  persistView() {}, renderCrumbs() {}, viewHash: () => '',
  goHome() {}, showWelcome() {}, showSections() {}, showChapters() {},
  L: key => key === 'verse' ? 'Verse' : key,
  T: text => text.en,
  numL: String, fmtNL: String, fmtRangeL: String,
  esc: text => String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;'),
  wayCrumbs: () => '', wayName: () => '', chTitle: () => '',
  modeSwitch: () => '', colophonHtml: () => '', backFoot: () => '',
  App: {reader: {open: openVerse}},
  openModal: openVerse,
});
vm.runInContext(code, ctx);

const cardPattern = /<div class="mini"[^>]*onclick="([^"]+)"[^>]*>\s*<div class="vnum">([^<]+)<\/div>/g;
let checked = 0;
for (const [ci, ch] of DATA.entries()) {
  ctx.showChapter(ci);
  const cards = [...view.innerHTML.matchAll(cardPattern)];
  const expected = ch.themes.flatMap(t => t.parts.flatMap(p => p.sutras.map(s => s.n)));
  assert.equal(cards.length, ch.verses, `chapter ${ch.num}: one card per verse`);
  assert.deepEqual(cards.map(card => card[2].trim()), expected.map(n => `Verse ${n}`),
    `chapter ${ch.num}: the visible verse labels match the shipped verses`);

  for (const [, onclick, label] of cards) {
    const clickedCard = {label};
    const previousCount = opened.length;
    // Run the actual inline onclick from the generated HTML as a click, with
    // this bound to its card; do not reconstruct the index in the test.
    vm.runInContext(`(function(){${onclick}})`, ctx).call(clickedCard);
    assert.equal(opened.length, previousCount + 1, `${label}: one modal per click`);
    const result = opened[previousCount];
    assert.equal(result.mode, 'theme', `${label}: opened from a theme`);
    assert.equal(result.invoker, clickedCard, `${label}: click forwards its card`);
    assert.equal(`Verse ${result.verse}`, label.trim(),
      `${label}: card opened ${result.verse} (chapter ${ch.num}, theme ${result.ti}, index ${result.si})`);
    checked++;
  }
}
assert.equal(checked, 700, 'the navigation regression covers all 700 verse cards');
console.log(`theme card navigation: ${checked} cards open their own verses (including 4.19)`);
