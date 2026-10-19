/* Spaced repetition (Phase B) — 5-step Leitner schedule across 3 stages:
   New (0) -> Learning (box 1..2: 1d, 3d) -> Review (box 3..5: 7d, 21d, 60d). */
const SRS_DAYS = [0, 1, 3, 7, 21, 60];
function srsToday(d){
  d = d instanceof Date ? d : new Date();
  return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
}
function srsAddDays(ymd, days){
  const p = String(ymd || srsToday()).split('-').map(Number);
  const dt = new Date(Date.UTC(p[0]||2026, (p[1]||1)-1, (p[2]||1) + (Number(days)||0)));
  return dt.toISOString().slice(0,10);
}
function srsStreakDays(){
  try{
    const a = JSON.parse(localStorage.getItem('gitaStreak') || '[]');
    if(!Array.isArray(a)) return [];
    return [...new Set(a.filter(x => typeof x === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(x)))].sort();
  }catch(e){ return []; }
}
function srsTouchStreak(today){
  const t = today || srsToday();
  if(!/^\d{4}-\d{2}-\d{2}$/.test(t)) return;
  const next = [...new Set([...srsStreakDays(), t])].sort().slice(-365);
  try{ localStorage.setItem('gitaStreak', JSON.stringify(next)); }catch(e){}
}
function srsStreakCount(today){
  const set = new Set(srsStreakDays());
  if(!set.size) return 0;
  const t = today || srsToday();
  let cur = set.has(t) ? t : srsAddDays(t, -1);
  if(!set.has(cur)) return 0;
  let n = 0;
  while(set.has(cur)){ n++; cur = srsAddDays(cur, -1); }
  return n;
}
function srsSeedHeld(p, vn, today){
  if(!p || !/^\d{1,2}\.\d{2}$/.test(vn)) return;
  const t = today || srsToday();
  p.srs = p.srs ? {...p.srs} : {};
  if(!p.srs[vn]) p.srs[vn] = {box:1, due:srsAddDays(t, 1), reps:1, lapses:0};
  srsTouchStreak(t);
}
function srsUnseedHeld(p, vn){
  if(!p || !p.srs || !p.srs[vn]) return;
  if((p.srs[vn].reps || 0) <= 1) delete p.srs[vn];
  if(!Object.keys(p.srs).length) delete p.srs;
}
function srsRecord(chNum, vn, ok, today){
  if(!/^\d{1,2}\.\d{2}$/.test(vn) || !(chNum >= 1 && chNum <= 18)) return null;
  const t = today || srsToday();
  const p = lrGet(chNum);
  p.srs = p.srs ? {...p.srs} : {};
  const cur = p.srs[vn] || {box:0, due:t, reps:0, lapses:0};
  const box = ok ? Math.min(5, (cur.box || 0) + 1) : 1;
  const due = srsAddDays(t, SRS_DAYS[box]);
  p.srs[vn] = {box, due, reps:(cur.reps || 0) + (ok ? 1 : 0), lapses:(cur.lapses || 0) + (ok ? 0 : 1)};
  lrPut(chNum, p);
  srsTouchStreak(t);
  return p.srs[vn];
}
function srsDueChapter(chNum, today){
  const t = today || srsToday();
  const a = lrAll(), p = a[chNum];
  const srs = (p && p.srs) || {};
  return Object.keys(srs).filter(vn => srs[vn].due <= t).sort((x,y)=>{
    if(srs[x].due !== srs[y].due) return srs[x].due < srs[y].due ? -1 : 1;
    return x < y ? -1 : (x > y ? 1 : 0);
  });
}
function srsDueAll(today){
  const t = today || srsToday(), a = lrAll();
  let total = 0, firstCi = null;
  for(let n=1; n<=18; n++){
    const srs = (a[n] && a[n].srs) || {};
    const due = Object.keys(srs).filter(vn => srs[vn].due <= t);
    if(due.length){
      total += due.length;
      if(firstCi === null) firstCi = n - 1;
    }
  }
  return {total, firstCi};
}
function srsBarHtml(ci){
  const chNum = ci + 1, a = lrAll(), p = a[chNum] || {};
  const srs = p.srs || {}, tracked = Object.keys(srs).length;
  const due = srsDueChapter(chNum), streak = srsStreakCount();
  if(!tracked && !streak) return '';
  const status = due.length
    ? fmt(L('srs_ch_due'), {n:numL(due.length)})
    : (tracked ? fmt(L('srs_all_caught_up'), {n:numL(tracked)}) : '');
  const stTxt = streak ? fmt(L('srs_streak'), {n:numL(streak)}) : '';
  const line = [status, stTxt].filter(Boolean).join(' · ');
  const btn = due.length
    ? `<button type="button" class="lr-cta sm" onclick="App.learn.review(${ci})">${esc(L('srs_review_btn'))}</button>`
    : '';
  return `<div class="lr-srs-bar" id="lrSrsBar"><span class="lr-srs-txt">${esc(line)}</span>${btn}</div>`;
}
function srsWelcomeHtml(){
  const info = srsDueAll();
  if(!info.total || info.firstCi === null) return '';
  const lbl = info.total === 1 ? L('srs_due_one') : fmt(L('srs_due_many'), {n:numL(info.total)});
  return `<button type="button" class="w-due" id="wDueBtn" onclick="App.learn.openDue()">${esc(lbl)} →</button>`;
}
function lrOpenDue(){
  const info = srsDueAll();
  if(info.firstCi === null) return;
  lrReview(info.firstCi);
}
function lrReview(ci, seed){
  if(!GITA_CH[ci+1]||!GITA_CH[ci+1].themes){ loadChapter(ci+1).then(()=>lrReview(ci, seed)).catch(gitaLoadFail); return; }
  const ch = DATA[ci], p = lrGet(ch.num), srs = p.srs || {};
  let ids = srsDueChapter(ch.num);
  if(!ids.length) ids = Object.keys(srs).sort((a,b)=>(srs[a].due||'').localeCompare(srs[b].due||''));
  if(!ids.length) ids = Object.keys(p.held || {});
  const idSet = new Set(ids.slice(0, 7));
  const vs = [];
  ch.themes.forEach(t=>thVerses(t).forEach(s=>{ if(idSet.has(s.n)) vs.push(s); }));
  if(!vs.length) return showLearn(ci);
  lrDrill(ci, -1, vs, seed);
}
function srsFinishReview(ci){
  view.innerHTML = `<div class="lrn fade-in"><div class="lr-finis">
      <div class="lr-seal">✓</div>
      <h2>${esc(L('srs_review_btn'))}</h2>
      <p>${esc(L('srs_review_done'))}</p>
      <button class="lr-cta" onclick="showLearn(${ci})">${esc(L('opt_learn_s'))}</button>
    </div></div>`;
  scrollViewTop();
}

/* Learn session boundary: Core stores the returned plain object and never
   reaches into the memorization feature's mutable working state. */
function learnSessionSnapshot(){
  const snap = {at:state.lrAt || null,
    test:typeof lrTest === 'number' ? lrTest : 0,
    open:typeof lrOpen === 'object' && lrOpen ? lrOpen : {},
    level:typeof LV === 'object' && LV ? LV.level : 'full',
    shown:typeof LV === 'object' && LV ? LV.shown : {}};
  const quiz = App.drills.capture();
  if(quiz) snap.quiz = quiz;
  if(state.lrAt && state.lrAt.kind === 'free' && FP && FP.v)
    snap.free = {ci:FP.ci, ti:FP.ti, verse:FP.v.n,
      deal:Array.isArray(FP.deal) ? FP.deal.slice() : [],
      picked:Array.isArray(FP.picked) ? FP.picked.slice() : []};
  return snap;
}
function restoreLearnSession(snap){
  if(!snap || snap.view !== 'learn' || !snap.learn || !snap.learn.at) return;
  const ci = Number.isInteger(snap.chapter) ? snap.chapter : null;
  if(ci == null) return;
  const at = snap.learn.at;
  if(at.kind === 'story'){
    lrTest = snap.learn.test ? 1 : 0;
    lrOpen = snap.learn.open && typeof snap.learn.open === 'object' ? snap.learn.open : {};
    lrStory(ci, Number.isInteger(at.step) ? at.step : 0,
      Number.isInteger(at.seed) ? at.seed : null);
  }else if(at.kind === 'storyDone'){
    lrStoryDone(ci);
  }else if(at.kind === 'theme' && Number.isInteger(at.ti)){
    if(typeof LV === 'object' && LV){
      LV.level = ['full','first','half','blind'].includes(snap.learn.level) ? snap.learn.level : 'full';
      LV.shown = snap.learn.shown && typeof snap.learn.shown === 'object' ? snap.learn.shown : {};
    }
    lrTheme(ci, at.ti, Number.isInteger(at.k) ? at.k : 0);
  }else if(at.kind === 'drill' && Number.isInteger(at.ti)
           && ((at.ti === -1 && DATA[ci]) || (DATA[ci] && DATA[ci].themes[at.ti]))){
    const seed = Number.isInteger(snap.learn.quiz && snap.learn.quiz.seed) ? snap.learn.quiz.seed
      : (Number.isInteger(at.seed) ? at.seed : null);
    if(at.ti === -1) lrReview(ci, seed);
    else lrDrill(ci, at.ti, thVerses(DATA[ci].themes[at.ti]), seed);
  }else if(at.kind === 'free' && snap.learn.free){
    const f = snap.learn.free, loc = App.library.location(f.verse);
    if(loc && loc.ci === ci){
      FP.ci = ci; FP.ti = Number.isInteger(f.ti) ? f.ti : -1;
      FP.v = App.library.verse(loc); FP.order = (FP.v.flow||[]).filter(x=>x.k==='p');
      const valid = a => Array.isArray(a) && a.length === FP.order.length
        && a.every(Number.isInteger) && new Set(a).size === a.length
        && a.every(i=>i >= 0 && i < FP.order.length);
      FP.deal = valid(f.deal) ? f.deal.slice() : FP.order.map((_,i)=>i);
      FP.picked = Array.isArray(f.picked) ? f.picked.filter(i=>Number.isInteger(i)
        && i >= 0 && i < FP.order.length).slice(0,FP.order.length) : [];
      App.session.update({view:'learn', chapter:ci, theme:FP.ti < 0 ? null : FP.ti,
        lrAt:{kind:'free', ti:FP.ti}}); lrFreePaint();
    }
  }else showLearn(ci);
  if(snap.learn.quiz) App.drills.restore(snap.learn.quiz);
}
