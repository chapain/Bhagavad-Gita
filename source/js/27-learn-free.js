/* ==================== 27-learn-free — free practice ====================
   Split out of 20-learn.js (2026-11-04) before the next feature needed the room:
   that module held the path, the story, the disclosure, the drill and this mode
   in 686 of 700 lines. This mode has its own state (FP) and no scoring, so it
   moves whole; 20-learn.js's screens still call lrFree/lrFreeCh by name, and
   25-learn-session.js still restores FP. lrShuffle and thVerses stay behind. */
/* ---------------- free practice ----------------
   After a theme is held, the reader may keep going for as long as they like:
   one verse from this theme with its four pādas shuffled, reorder, then pull
   another. Deliberately OUTSIDE the queue engine — nothing is scored, nothing
   is required, and leaving costs nothing. Practice, not examination. */
var FP = {ci:0, ti:0, v:null, order:[], deal:[], picked:[]};
function lrFree(ci, ti){
  App.session.update({view:'learn', chapter:ci, theme:ti}); App.views.persist();
  App.session.update({lrAt:{kind:'free', ti:ti}});
  FP.ci = ci; FP.ti = ti;
  lrFreePick();
}
function lrFreeCh(ci){
  App.session.update({view:'learn', chapter:ci, theme:null}); App.views.persist();
  App.session.update({lrAt:{kind:'free', ti:-1}});
  FP.ci = ci; FP.ti = -1;
  lrFreePick();
}
function lrFreePick(){
  const ch = DATA[FP.ci];
  const vs = FP.ti < 0
    ? ch.themes.reduce((a,th)=>a.concat(thVerses(th)), [])
    : thVerses(ch.themes[FP.ti]);
  const t = FP.ti < 0 ? null : ch.themes[FP.ti];
  /* avoid handing back the same verse twice running when the theme has
     more than one to choose from */
  let v = vs[Math.floor(Math.random()*vs.length)];
  if(vs.length > 1 && FP.v){
    let guard = 0;
    while(v.n === FP.v.n && guard++ < 12) v = vs[Math.floor(Math.random()*vs.length)];
  }
  FP.v = v; FP.picked = [];
  FP.order = (v.flow||[]).filter(f=>f.k==='p');
  /* The pādas must appear SHUFFLED or there is nothing to put in order — they
     were rendering in their natural sequence, which made the whole mode a
     no-op (owner 2026-09-01). Shuffle a display order ONCE per verse and keep
     it in state: reshuffling inside the paint would move the chips on every
     tap. Guard against the identity permutation, which would look like the
     bug even though the code was right. */
  const n = FP.order.length;
  let deal = FP.order.map((_,i)=>i);
  for(let guard=0; guard<20; guard++){
    deal = lrShuffle(FP.order.map((_,i)=>i));
    if(n < 2 || deal.some((ix,k)=>ix!==k)) break;
  }
  FP.deal = deal;
  lrFreePaint();
}
function lrFreePaint(){
  const ch = DATA[FP.ci], t = FP.ti < 0 ? null : ch.themes[FP.ti], v = FP.v;
  const tlab = t ? T(t.titles) : T(ch.names);
  const done = FP.picked.length === FP.order.length;
  view.innerHTML = `
    ${App.views.breadcrumbs([[L('sections_title'),'App.views.sections()'],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, `showLearn(${FP.ci})`],
      [tlab, null]])}
    <div class="lrn fade-in">
      <div class="lr-k">${esc(L('learn_free'))}</div>
      <h2 class="view-title">${esc(tlab)}</h2>
      <div class="view-sub">${esc(L('learn_free_d'))}</div>
      <div class="lr-qbox">
        <div class="lr-ask">${esc(fmt(L('learn_qorder'),{v:fmtNL(v.n)}))}</div>
        <div class="lr-slots" id="fpSlots">${FP.picked.map((ix,k)=>
          `<span class="lr-slot dv" lang="sa">${numL(k+1)}. ${esc(FP.order[ix].d)}</span>`).join('')}</div>
        <div class="lr-chips" id="fpChips">${(FP.deal||FP.order.map((_,i)=>i)).map(ix=>
          FP.picked.indexOf(ix) >= 0 ? '' :
          `<button class="lr-chip2 dv" lang="sa" onclick="lrFreeTap(${ix})"><span class="lr-t">${esc(FP.order[ix].d)}</span></button>`
        ).join('')}</div>
        <div class="lr-fb" id="fpFb">${done
          ? `<div class="good">${esc(L('learn_thread_ok'))}</div>
             <div class="lr-cue" lang="sa-Latn">${esc(v.t)}</div>`
          : ''}</div>
      </div>
      <div class="lr-nav">
        <button class="lr-cta" onclick="lrFreePick()">${esc(L('learn_shuffle'))}</button>
        <span class="lr-hint">${esc(fmtNL(v.n))}</span>
        <button class="lr-ghost" onclick="App.views.chapter(${FP.ci})">${esc(L('learn_done_free'))}</button>
      </div>
    </div>` + backFoot(`App.views.chapter(${FP.ci})`, L('back_chapter_one'));
  scrollViewTop();
}
function lrFreeTap(i){
  const want = FP.picked.length;               // the next pāda in true order
  if(i === want){
    FP.picked.push(i);
    lrFreePaint();
  }else{
    /* wrong pāda: shake the chip, say which one comes next, and let them try
       again. No score, no penalty — this is the mode for playing. */
    const btns = document.querySelectorAll('#fpChips .lr-chip2');
    btns.forEach(b=>{ if(b.getAttribute('onclick') === 'lrFreeTap(' + i + ')'){
      b.classList.add('shake'); setTimeout(()=>b.classList.remove('shake'), 380); }});
    const fb = document.getElementById('fpFb');
    if(fb) fb.innerHTML = `<div class="bad">${esc(L('learn_nextis'))} ` +
      `<b class="dv" lang="sa">${esc(FP.order[want].d)}</b></div>`;
  }
}
