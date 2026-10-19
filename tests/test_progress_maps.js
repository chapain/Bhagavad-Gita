#!/usr/bin/env node
'use strict';
// Run the ACTUAL emitted progress functions, including their historical map data.
const fs=require('fs'), path=require('path'), vm=require('vm'), assert=require('assert/strict');
const ROOT=path.join(__dirname,'..');
const html=fs.readFileSync(path.join(ROOT,'index.html'),'utf8');
const start=html.indexOf('const LR_LEGACY_MAP_OPTIONS = '), end=html.indexOf('function lrIast()',start);
assert(start>=0 && end>start,'map-aware progress code must be emitted');
const code=html.slice(start,end);
const contract=JSON.parse(fs.readFileSync(path.join(ROOT,'source','study_map_contract.json'),'utf8'));
const DATA=[];
for(let n=1;n<=18;n++){
  const raw=fs.readFileSync(path.join(ROOT,'data',`ch${n}.js`),'utf8');
  DATA.push(JSON.parse(raw.slice(raw.indexOf('=')+1).trim().replace(/;$/,'')));
}
let count=0;
function fixture(record={}, data=DATA, deny=false){
  const store={gitaLearn:JSON.stringify(record),gitaFav:'["3.06"]',gitaNotes:'{"3.06":"My note"}'};
  const ctx=vm.createContext({DATA:data,localStorage:{
    getItem:key=>{if(deny)throw Error('storage denied');return store[key]||null;},
    setItem:(key,value)=>{if(deny)throw Error('storage denied');store[key]=value;}
  }});
  vm.runInContext(code,ctx);
  return {store,ctx,get:n=>JSON.parse(vm.runInContext(`JSON.stringify(lrGet(${n}))`,ctx))};
}
function test(name,fn){fn();count++;console.log('PASS:',name);}
test('embedded legacy maps match the reviewed contract',()=>{
  const f=fixture();
  assert.deepEqual(JSON.parse(vm.runInContext('JSON.stringify(LR_LEGACY_MAP_OPTIONS)',f.ctx)),contract.legacy_map_options);
});
test('a fresh chapter gains a current map without invented completion',()=>{
  const p=fixture().get(3);assert.equal(p.story,0);assert.deepEqual(p.themes,{});
  assert.deepEqual(p.map,contract.approved_maps['3']);assert.deepEqual(p.held,{});
});
test('legacy numeric flags move by the retained verse range, not by index',()=>{
  const f=fixture({3:{story:1,themes:{0:1,2:1},held:{'3.06':1,'3.10':1}}});
  const p=f.get(3);assert.equal(p.story,0);assert.deepEqual(p.themes,{'1':1});
  assert.deepEqual(p.held,{'3.06':1,'3.10':1});assert.deepEqual(p.map,contract.approved_maps['3']);
});
test('migration is persisted and a repeated read is idempotent',()=>{
  const f=fixture({3:{story:1,themes:{2:1},held:{'3.06':1}}});
  const first=f.get(3), stored=f.store.gitaLearn;
  assert.deepEqual(f.get(3),first);assert.equal(f.store.gitaLearn,stored);
  assert.deepEqual(JSON.parse(stored)['3'].map,contract.approved_maps['3']);
});
test('a known current map keeps story and theme mastery',()=>{
  const p=fixture({3:{story:1,themes:{1:1,4:1},held:{'3.06':1},map:contract.approved_maps['3']}}).get(3);
  assert.equal(p.story,1);assert.deepEqual(p.themes,{'1':1,'4':1});assert.deepEqual(p.held,{'3.06':1});
});
test('an explicitly stamped old map migrates even when legacy possibilities are ambiguous',()=>{
  const old=contract.legacy_map_options['1'][0];
  const f=fixture({1:{story:1,themes:{0:1,1:1},held:{'1.01':1},map:old}});
  const p=f.get(1);assert.equal(p.story,0);assert.deepEqual(p.themes,{'0':1});assert.deepEqual(p.held,{'1.01':1});
});
test('ambiguous unversioned Chapter 1 does not acquire wrong completions',()=>{
  const p=fixture({1:{story:1,themes:{0:1,5:1},held:{'1.14':1}}}).get(1);
  assert.equal(p.story,0);assert.deepEqual(p.themes,{});assert.deepEqual(p.held,{'1.14':1});
});
test('ambiguous unversioned Chapter 2 preserves held verses, not guessed themes',()=>{
  const p=fixture({2:{story:1,themes:{7:1},held:{'2.19':1}}}).get(2);
  assert.equal(p.story,0);assert.deepEqual(p.themes,{});assert.deepEqual(p.held,{'2.19':1});
});
test('unchanged Chapter 17 retains its unversioned pilot progress',()=>{
  const p=fixture({17:{story:1,themes:{0:1,8:1},held:{'17.20':1}}}).get(17);
  assert.equal(p.story,1);assert.deepEqual(p.themes,{'0':1,'8':1});assert.deepEqual(p.held,{'17.20':1});
});
test('split old themes do not imply that either new theme has been learned',()=>{
  const old=contract.previous_maps['18'];const ix=old.indexOf('18.49–18.55');assert(ix>=0);
  const p=fixture({18:{story:1,themes:{[ix]:1},held:{'18.54':1},map:old}}).get(18);
  assert.equal(p.story,0);assert.deepEqual(p.themes,{});assert.deepEqual(p.held,{'18.54':1});
});
test('out-of-range numeric completion cannot inflate mastery',()=>{
  const p=fixture({3:{story:1,themes:{999:1,1:1},held:{},map:contract.approved_maps['3']}}).get(3);
  assert.deepEqual(p.themes,{'1':1});
});
test('migration does not change favourites, notes or another chapter',()=>{
  const other={story:1,themes:{1:1},held:{'17.05':1}};
  const f=fixture({3:{story:1,themes:{2:1},held:{'3.06':1}},17:other});f.get(3);
  assert.equal(f.store.gitaFav,'["3.06"]');assert.equal(f.store.gitaNotes,'{"3.06":"My note"}');
  assert.deepEqual(JSON.parse(f.store.gitaLearn)['17'],other);
});
test('lazy chapter metadata must not reset existing progress',()=>{
  const lazy=DATA.map(c=>({num:c.num,themes:[]}));
  const record={3:{story:1,themes:{2:1},held:{'3.06':1}}};const f=fixture(record,lazy),before=f.store.gitaLearn;
  assert.equal(f.get(3).story,1);assert.deepEqual(f.get(3).themes,{'2':1});assert.equal(f.store.gitaLearn,before);
});
test('bad local-storage JSON cannot crash the reading path',()=>{
  const f=fixture();f.store.gitaLearn='{broken';assert.equal(f.get(3).story,0);assert.deepEqual(f.get(3).themes,{});
});
test('storage denial still returns a safe usable chapter state',()=>{
  const p=fixture({},DATA,true).get(3);assert.equal(p.story,0);assert.deepEqual(p.themes,{});assert.deepEqual(p.held,{});
});
test('spaced-repetition (SRS) records survive chapter map migration',()=>{
  const srs={'3.06':{box:3,due:'2026-10-26',reps:3,lapses:0}};
  const f=fixture({3:{story:1,themes:{2:1},held:{'3.06':1},srs}});
  const p=f.get(3);
  assert.deepEqual(p.srs,srs);
});
test('SRS schedule promotes on right answer, demotes to box 1 on miss, orders due queue, and tracks streak',()=>{
  const srsStart=html.indexOf('const SRS_DAYS = [0, 1, 3, 7, 21, 60];');
  const srsEnd=html.indexOf('function srsBarHtml(',srsStart);
  assert(srsStart>=0 && srsEnd>srsStart,'SRS engine must be emitted');
  const f=fixture();
  vm.runInContext('function lrPut(n,o){const a=lrAll();a[n]=o;localStorage.setItem("gitaLearn",JSON.stringify(a));}\n'+html.slice(srsStart,srsEnd),f.ctx);
  // 1. New -> Box 1 (+1d) -> Box 2 (+3d) -> Box 3 (+7d)
  let r1=vm.runInContext('srsRecord(2,"2.47",true,"2026-10-19")',f.ctx);
  assert.equal(r1.box,1);assert.equal(r1.due,'2026-10-20');assert.equal(r1.reps,1);assert.equal(r1.lapses,0);
  let r2=vm.runInContext('srsRecord(2,"2.47",true,"2026-10-20")',f.ctx);
  assert.equal(r2.box,2);assert.equal(r2.due,'2026-10-23');assert.equal(r2.reps,2);
  let r3=vm.runInContext('srsRecord(2,"2.47",true,"2026-10-23")',f.ctx);
  assert.equal(r3.box,3);assert.equal(r3.due,'2026-10-30');assert.equal(r3.reps,3);
  // 2. Miss demotes to Box 1 (+1d) and increments lapses
  let miss=vm.runInContext('srsRecord(2,"2.47",false,"2026-10-30")',f.ctx);
  assert.equal(miss.box,1);assert.equal(miss.due,'2026-10-31');assert.equal(miss.lapses,1);
  // 3. Due ordering: earliest due first, future due excluded
  vm.runInContext('srsRecord(2,"2.11",true,"2026-10-15")',f.ctx); // due 2026-10-16
  vm.runInContext('srsRecord(2,"2.12",true,"2026-10-18")',f.ctx); // due 2026-10-19
  const due=JSON.parse(vm.runInContext('JSON.stringify(srsDueChapter(2,"2026-10-19"))',f.ctx));
  assert.deepEqual(due,['2.11','2.12'],'only due verses returned in ascending due order');
  const allDue=JSON.parse(vm.runInContext('JSON.stringify(srsDueAll("2026-10-19"))',f.ctx));
  assert.equal(allDue.total,2);assert.equal(allDue.firstCi,1);
  // 4. Streak counts consecutive days
  vm.runInContext('srsTouchStreak("2026-10-17");srsTouchStreak("2026-10-18");srsTouchStreak("2026-10-19");',f.ctx);
  assert.equal(vm.runInContext('srsStreakCount("2026-10-19")',f.ctx),3);
});
console.log(`\nprogress maps: ${count} tests passed — retained verse ranges migrate; held verses, notes and favourites survive`);
