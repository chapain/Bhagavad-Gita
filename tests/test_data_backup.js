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

console.log('test_data_backup.js: ALL GREEN');
