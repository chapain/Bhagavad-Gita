#!/usr/bin/env node
'use strict';
/* test_data_backup.js — regression locks for Phase 5.4 export/import */

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');

// Extract the data module source from the built shell (it is inlined)
function mustContain(re, label){
  if(!re.test(html)){
    console.error('FAIL:', label);
    process.exit(1);
  }
  console.log('PASS:', label);
}

mustContain(/DATA_SCHEMA_VERSION = 1/, 'schema version is 1');
mustContain(/function dataCurrentSnapshot/, 'snapshot exists');
mustContain(/function dataLastBackup/, 'backup timestamp reader exists');
mustContain(/function dataBackupBadgeHtml/, 'backup status badge helper exists');
mustContain(/function dataValidateImport/, 'validator exists');
mustContain(/function dataMergeImport/, 'merge exists');
mustContain(/function dataExport/, 'export exists');
mustContain(/function showData/, 'data view exists');
mustContain(/gita-backup-/, 'export filename pattern');
mustContain(/versioned/, 'mentions versioned schema in comment');

// Simulate validation logic in Node (copy of JS function)
function dataValidateImport(obj){
  if(!obj || typeof obj !== 'object') return "not an object";
  if(obj.version !== 1) return "unsupported version";
  if(!obj.data || typeof obj.data !== 'object') return "missing data";
  const d = obj.data;
  if(d.favs && !Array.isArray(d.favs)) return "favs not array";
  if(d.favNotes && (typeof d.favNotes !== 'object' || Array.isArray(d.favNotes))) return "favNotes not object";
  if(d.learn && (typeof d.learn !== 'object' || Array.isArray(d.learn))) return "learn not object";
  if(Array.isArray(d.favs)){
    for(const v of d.favs){
      if(typeof v !== 'string' || !/^\d{1,2}\.\d{1,2}$/.test(v)) return "bad fav id: "+v;
    }
  }
  if(d.favNotes && typeof d.favNotes === 'object'){
    for(const k in d.favNotes){
      if(!/^\d{1,2}\.\d{1,2}$/.test(k)) return "bad note key: "+k;
      if(typeof d.favNotes[k] !== 'string') return "bad note value for "+k;
    }
  }
  if(d.learn && typeof d.learn === 'object'){
    for(const ch in d.learn){
      if(!/^\d{1,2}$/.test(ch)) return "bad learn chapter: "+ch;
      const c = d.learn[ch];
      if(!c || typeof c !== 'object') return "bad learn entry "+ch;
      if(c.themes && typeof c.themes !== 'object') return "bad themes "+ch;
      if(c.held && typeof c.held !== 'object') return "bad held "+ch;
    }
  }
  return null;
}

// Valid backup
const good = {
  version:1,
  app:"Bhagavad-Gita",
  exportedAt:new Date().toISOString(),
  data:{
    favs:["2.47","1.01"],
    favNotes:{"2.47":"my note"},
    learn:{"2":{story:1, themes:{0:1}, held:{"2.47":1}, map:["2.01–2.03"]}}
  }
};
if(dataValidateImport(good)!==null){ console.error('FAIL: good backup should validate'); process.exit(1); }
console.log('PASS: good backup validates');

// Bad version
const badVer = {...good, version:2};
if(dataValidateImport(badVer)===null){ console.error('FAIL: bad version should reject'); process.exit(1); }
console.log('PASS: bad version rejected');

// Bad fav id
const badFav = JSON.parse(JSON.stringify(good));
badFav.data.favs=["999"];
if(dataValidateImport(badFav)===null){ console.error('FAIL: bad fav should reject'); process.exit(1); }
console.log('PASS: bad fav id rejected');

// Merge logic (simplified)
function dataMergeImportSim(cur, imported){
  const favSet={};
  cur.favs.forEach(id=>favSet[id]=1);
  imported.data.favs.forEach(id=>favSet[id]=1);
  const mergedFavs=Object.keys(favSet).sort();
  return mergedFavs;
}
const cur={favs:["1.01"]};
const merged=dataMergeImportSim(cur, good);
if(merged.length!==2 || !merged.includes("2.47")){ console.error('FAIL: merge'); process.exit(1); }
console.log('PASS: merge unions favs');

// Execute actual emitted dataMergeImport for SRS (max box + earliest due tie-break) and streak
const vm = require('vm');
const dataStart = html.indexOf('const DATA_SCHEMA_VERSION = 1;');
const dataEnd = html.indexOf('function dataHandleImportFile(', dataStart);
const store = {
  gitaLearn: JSON.stringify({
    "2": {
      story: 1, themes: {"0": 1}, held: {"2.47": 1},
      srs: {
        "2.47": {box: 2, due: "2026-10-25", reps: 2, lapses: 0},
        "2.11": {box: 3, due: "2026-10-30", reps: 3, lapses: 0}
      }
    }
  }),
  gitaStreak: JSON.stringify(["2026-10-18"])
};
const ctx = vm.createContext({
  localStorage: {
    getItem: k => store[k] || null,
    setItem: (k, v) => { store[k] = v; }
  },
  FAV: [], FAVNOTE: {},
  esc: s => String(s), numL: s => String(s), L: k => k
});
vm.runInContext(html.slice(dataStart, dataEnd), ctx);
const impPayload = {
  version: 1,
  exportedAt: "2026-10-19T12:00:00Z",
  data: {
    favs: ["2.47"],
    learn: {
      "2": {
        story: 0, themes: {}, held: {"2.47": 1},
        srs: {
          "2.47": {box: 2, due: "2026-10-22", reps: 2, lapses: 0}, // tie on box 2 -> earliest due wins
          "2.11": {box: 1, due: "2026-10-20", reps: 1, lapses: 1}  // lower box 1 -> box 3 wins
        }
      }
    },
    streak: ["2026-10-19"]
  }
};
ctx.dataMergeImport(impPayload);
const mergedLearn = JSON.parse(store.gitaLearn);
if(mergedLearn["2"].srs["2.47"].due !== "2026-10-22" || mergedLearn["2"].srs["2.11"].box !== 3){
  console.error('FAIL: SRS merge max(box) + earliest due tie-break', mergedLearn["2"].srs);
  process.exit(1);
}
const mergedStreak = JSON.parse(store.gitaStreak);
if(mergedStreak.length !== 2 || !mergedStreak.includes("2026-10-18") || !mergedStreak.includes("2026-10-19")){
  console.error('FAIL: streak union', mergedStreak);
  process.exit(1);
}
console.log('PASS: SRS merge (max box + earliest due tie-break) and streak union');



// ---------- A5: the backup line on the Learn path ----------
{
  const start = html.indexOf('function dataBackupLine(');
  const end = html.indexOf('function dataBackupBadgeHtml(', start);
  if(start < 0 || end <= start){ console.error('FAIL: dataBackupLine() must be emitted'); process.exit(1); }
  const src = html.slice(start, end);

  // Fixed clock so "yesterday" is a fact, not whatever day CI runs on.
  const NOW = new Date(2026, 10, 4, 15, 30, 0);          // 4 Nov 2026, local
  const iso = d => d.toISOString().slice(0, 10);
  function run(backupAt, snapshot){
    const store = {};
    if(backupAt) store.gitaBackupAt = backupAt;
    const ctx = require('vm').createContext({
      localStorage: { getItem: k => (k in store ? store[k] : null),
                      setItem: (k, v) => { store[k] = v; },
                      removeItem: k => { delete store[k]; } },
      dataLastBackup(){ return store.gitaBackupAt || ''; },
      dataCurrentSnapshot(){ return snapshot; },
      dataStats: null, L: null, numL: n => String(n),
      Date: class extends Date { constructor(...a){ super(...(a.length ? a : [NOW.getTime()])); }
                                 static now(){ return NOW.getTime(); } },
    });
    ctx.dataStats = require('vm').runInContext(
      'function dataStats(snap){' +
      '  const favs=snap.favs||[],notes=snap.favNotes||{},learn=snap.learn||{};' +
      '  let held=0,chapters=0;' +
      '  for(const ch in learn){ if(!/^\\d{1,2}$/.test(ch)) continue; chapters++; }' +
      '  return {favs:favs.length,notes:Object.keys(notes).length,chapters:chapters,held:held}; }' +
      '; dataStats', ctx);
    const strings = {
      backup_never: 'No backup yet — export one',
      backup_today: 'Backed up today',
      backup_yesterday: 'Backed up yesterday',
      backup_n_days: 'Last backup {n} days ago',
    };
    ctx.L = k => strings[k];
    return require('vm').runInContext(src + '; dataBackupLine', ctx)();
  }

  const something = { favs: ['2.47'], favNotes: {}, learn: {} };
  const nothing   = { favs: [], favNotes: {}, learn: {} };

  const cases = [
    [iso(NOW),        something, 'Backed up today'],
    [iso(new Date(2026, 10, 3)), something, 'Backed up yesterday'],
    [iso(new Date(2026, 10, 1)), something, 'Last backup 3 days ago'],
    [iso(new Date(2026, 10, 4)), nothing,   'Backed up today'],
  ];
  for(const [at, snap, want] of cases){
    const got = run(at, snap);
    if(got !== want){ console.error('FAIL: backup line', at, '→', JSON.stringify(got), 'want', JSON.stringify(want)); process.exit(1); }
  }
  if(run('', nothing) !== ''){ console.error('FAIL: a first visit with nothing saved must stay silent'); process.exit(1); }
  if(run('', something) !== 'No backup yet — export one'){
    console.error('FAIL: saved data but no backup must say so'); process.exit(1);
  }
  // A future or corrupted stamp must never print a negative age.
  if(run('2026-12-25', something) !== 'Backed up today'){
    console.error('FAIL: a future backup date must clamp to today'); process.exit(1);
  }
  if(!/class="foot-link lr-backup"/.test(html) || !/App\.data\.show\(\)/.test(html)){
    console.error('FAIL: the Learn path must link the line to the data screen'); process.exit(1);
  }
  console.log('PASS: A5 backup line reads today/yesterday/N days, silent when empty, opens the data screen');
}

console.log('test_data_backup.js: ALL GREEN');
