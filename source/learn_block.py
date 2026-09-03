# -*- coding: utf-8 -*-
"""learn_block.py — "Learn by heart": the JS and CSS for the third way.

Kept in its own module because it is ~430 lines of self-contained behaviour and
build_gita.py is already long. It is injected verbatim into the app shell.

The pedagogy, and why the order is not negotiable:
  1. THE STORY — a chapter's themes, in sequence, are its plot. Learn the spine
     first and every verse afterwards has somewhere to hang. Nobody remembers
     700 loose verses; anybody can remember 18 stories of 6-18 beats.
  2. THE VERSES — only once the spine holds. Theme by theme: meet each verse,
     then be asked to PRODUCE it, not merely recognise it.

Everything is recall, not re-reading. Being asked and struggling is what builds
the trace; re-reading feels like learning and is not. A miss is requeued and
comes round again, and a stage passes only when the whole run is clean.
"""

LEARN_JS = r"""
/* ---------------- progress ----------------
   One key for all 18 chapters. Hardened like the favourites: a parse that
   succeeds still has to yield the shape we expect, or one bad value would
   throw on every render with no way back but clearing site data. */
function lrAll(){
  try{
    const o = JSON.parse(localStorage.getItem('gitaLearn') || 'null');
    if(!o || typeof o !== 'object' || Array.isArray(o)) return {};
    const out = {};
    for(const k in o){
      if(!/^\d{1,2}$/.test(k)) continue;
      const c = o[k];
      if(!c || typeof c !== 'object' || Array.isArray(c)) continue;
      const th = {};
      if(c.themes && typeof c.themes === 'object' && !Array.isArray(c.themes))
        for(const t in c.themes) if(/^\d+$/.test(t) && c.themes[t] === 1) th[t] = 1;
      out[k] = {story: c.story === 1 ? 1 : 0, themes: th};
    }
    return out;
  }catch(e){ return {}; }
}
function lrGet(n){ const a = lrAll(); return a[n] || {story:0, themes:{}}; }
function lrPut(n, o){
  const a = lrAll(); a[n] = o;
  try{ localStorage.setItem('gitaLearn', JSON.stringify(a)); }catch(e){}
}
function lrReset(n){
  if(!confirm(L('learn_restart_q'))) return;
  const a = lrAll(); delete a[n];
  try{ localStorage.setItem('gitaLearn', JSON.stringify(a)); }catch(e){}
  showLearn(state.chapter);
}
function fmt(s, o){ return String(s).replace(/\{(\w+)\}/g, (m,k)=> k in o ? o[k] : m); }

const lrShuffle = a => { a = a.slice();
  for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a; };
const lrSample = (arr,n) => lrShuffle(arr).slice(0,n);
/* every verse of a theme, flattened — parts are one verse each now, but the
   container is still there, so never assume */
function thVerses(t){ const out=[]; t.parts.forEach(p=>p.sutras.forEach(s=>out.push(s))); return out; }

/* ---------------- the path ---------------- */
function showLearn(ci){
  rememberOrigin();
  state.view='learn'; state.chapter=ci; state.lrAt = null;
  state.section = state.section || Math.ceil(DATA[ci].num/6);
  state.theme=null; renderCrumbs();
  const ch = DATA[ci], p = lrGet(ch.num);
  const total = ch.themes.length, done = Object.keys(p.themes).length;
  const pct = Math.round((p.story + done) / (1 + total) * 100);

  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'),'showSections()'],
      [wayName(Math.ceil(ch.num/6)), `showChapters(${Math.ceil(ch.num/6)})`],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, null]])}
    ${chTitle(ch)}
    ${modeSwitch(ci)}
    <div class="lrn fade-in">
      <div class="view-sub">${esc(fmt(L('learn_sub'),{}))}</div>
      <div class="lr-prog"><i style="width:${pct}%"></i></div>
      <div class="lr-progl">${esc(fmt(L('learn_walked'),{p:numL(pct)}))}</div>

      <div class="lr-step ${p.story?'done':'now'}">
        <div class="lr-badge">${p.story?'✓':numL(1)}</div>
        <div class="lr-body">
          <h3>${esc(L('learn_s1'))}</h3>
          <p>${esc(fmt(L('learn_s1_d'),{n:numL(total)}))}</p>
          <button class="lr-cta" onclick="lrStory(${ci},0)">
            ${esc(p.story?L('learn_again'):L('learn_begin'))}</button>
        </div>
      </div>

      <div class="lr-step ${p.story?(done===total?'done':'now'):'locked'}">
        <div class="lr-badge">${(p.story&&done===total)?'✓':numL(2)}</div>
        <div class="lr-body">
          <h3>${esc(L('learn_s2'))}</h3>
          <p>${p.story ? esc(fmt(L('learn_s2_d'),{a:numL(done),b:numL(total)}))
                       : esc(L('learn_s2_locked'))}</p>
          ${p.story ? `<div class="lr-grid">${ch.themes.map((t,ti)=>`
            <button class="lr-chip${p.themes[ti]?' ok':''}" onclick="lrTheme(${ci},${ti},0)">
              <span class="n">${p.themes[ti]?'✓':numL(ti+1)}</span>
              <span class="t">${esc(T(t.titles))}</span>
              <span class="v">${numL(vCount(t))}</span>
            </button>`).join('')}</div>`
          : `<button class="lr-ghost" onclick="lrSkip(${ci})">${esc(L('learn_skip'))}</button>`}
        </div>
      </div>

      <div class="lr-foot">
        <span>${esc(L('learn_local'))}</span>
        ${(p.story||done)?`<button class="lr-ghost sm" onclick="lrReset(${ch.num})">${esc(L('learn_restart'))}</button>`:''}
      </div>
    </div>` + backFoot(`showRead(${ci},'full')`, L('back_chapter_one'));
  scrollViewTop();
}
/* Re-enter the learn path in the new language, as near as possible to where
   the reader was. The current QUESTION is genuinely unrecoverable — it was
   generated from the old language's strings — but the theme or story step is
   not, so restart that rather than the whole chapter. */
function lrRelang(ci){
  const at = state.lrAt;
  if(at && at.kind === 'theme' && DATA[ci] && DATA[ci].themes[at.ti]) return lrTheme(ci, at.ti, 0);
  if(at && at.kind === 'story') return lrStory(ci, 0);
  showLearn(ci);
}
function lrSkip(ci){ const n=DATA[ci].num, p=lrGet(n); p.story=1; lrPut(n,p); showLearn(ci); }

/* ---------------- stage 1: the story ----------------
   Small chapters get read -> whole chain. Larger ones earn the middle two
   steps; drilling four stages over six themes is ceremony, not teaching. */
function lrPlan(ch){ return ch.themes.length >= 10 ? [0,1,2,3] : [0,3]; }

function lrStory(ci, step){
  state.view='learn'; state.chapter=ci; state.theme=null;
  state.lrAt = {kind:'story', step:step};
  const ch = DATA[ci], th = ch.themes, plan = lrPlan(ch);
  const k = plan.indexOf(step), n = plan.length;
  if(step === 0) return lrStoryRead(ci, ch, th, k+1, n);

  let items;
  if(step === 1){
    const groups = [];
    for(let i=0;i<th.length;i+=4) groups.push(th.slice(i,i+4).map((t,j)=>({t,i:i+j})));
    items = groups.filter(g=>g.length>1).map(g=>({kind:'order',
      ask: esc(fmt(L('learn_order_few'),{n:numL(g.length)})),
      chips: g.map(x=>({id:x.i, label:T(x.t.titles)})),
      answer: g.map(x=>x.i)}));
  } else if(step === 2){
    items = th.slice(0,-1).map((t,i)=>{
      const right = th[i+1];
      const wrong = lrSample(th.filter((_,j)=>j!==i+1&&j!==i), 3);
      return {kind:'pick',
        ask: esc(fmt(L('learn_after'),{t:T(t.titles)})),
        opts: lrShuffle([right,...wrong]).map(x=>({label:T(x.titles), ok:x===right})),
        note: esc(T(right.descs))};
    });
  } else {
    items = [{kind:'order',
      ask: esc(fmt(L('learn_order_all'),{n:numL(th.length)})),
      chips: th.map((t,i)=>({id:i, label:T(t.titles)})),
      answer: th.map((_,i)=>i)}];
  }
  const nxt = plan[k+1];
  lrRun(ci, items, fmt(L('learn_step'),{a:numL(k+1),b:numL(n)}),
    nxt === undefined ? ()=>lrStoryDone(ci) : ()=>lrStory(ci, nxt));
}

function lrStoryRead(ci, ch, th, k, n){
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'),'showSections()'],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, `showLearn(${ci})`],
      [L('learn_s1'), null]])}
    <div class="lrn fade-in">
      <div class="lr-k">${esc(fmt(L('learn_step'),{a:numL(k),b:numL(n)}))}</div>
      <h2 class="view-title">${esc(fmt(L('learn_read_h'),{n:numL(ch.num)}))}</h2>
      <div class="view-sub">${esc(L('learn_read_d'))}</div>
      <ol class="lr-thread">${th.map((t,i)=>`
        <li><span class="bead">${numL(i+1)}</span>
          <div><b>${esc(T(t.titles))}</b>
            <span class="rg">${esc(_drangeJS(t.range))}</span>
            <p>${esc(T(t.descs))}</p></div></li>`).join('')}</ol>
      <div class="lr-nav">
        <button class="lr-cta" onclick="lrStory(${ci},${lrPlan(ch)[1]})">${esc(L('learn_read_go'))}</button>
      </div>
    </div>` + backFoot(`showRead(${ci},'full')`, L('back_chapter_one'));
  scrollViewTop();
}
function lrStoryDone(ci){
  const ch = DATA[ci], p = lrGet(ch.num); p.story = 1; lrPut(ch.num, p);
  view.innerHTML = `<div class="lrn fade-in"><div class="lr-finis">
      <div class="lr-seal">✓</div>
      <h2>${esc(fmt(L('learn_story_done'),{n:numL(ch.num)}))}</h2>
      <p>${esc(L('learn_story_done_d'))}</p>
      <button class="lr-cta" onclick="showLearn(${ci})">${esc(L('learn_to_verses'))}</button>
    </div></div>`;
  scrollViewTop();
}

/* ---------------- stage 2: the verses of one theme ---------------- */
function lrTheme(ci, ti, k){
  state.view='learn'; state.chapter=ci; state.theme=ti;
  /* Remember the sub-view. A language switch cannot re-render a half-answered
     question — its options were built from the old language's strings — but it
     CAN put the reader back at the top of the same theme rather than at the
     chapter's path home, which is a much shorter walk back. */
  state.lrAt = {kind:'theme', ti:ti};
  const ch = DATA[ci], t = ch.themes[ti], vs = thVerses(t);
  if(k < vs.length) return lrMeet(ci, ti, k, vs);
  lrDrill(ci, ti, vs);
}
function lrMeet(ci, ti, k, vs){
  const ch = DATA[ci], t = ch.themes[ti], s = vs[k], last = k === vs.length-1;
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'),'showSections()'],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, `showLearn(${ci})`],
      [T(t.titles), null]])}
    <div class="lrn fade-in">
      <div class="lr-k">${esc(L('learn_meet'))} · ${numL(k+1)} / ${numL(vs.length)}</div>
      <h2 class="view-title">${esc(T(t.titles))}</h2>
      <div class="lr-vnum">${esc(fmtNL(s.n))}</div>
      <div class="lr-quarters">${(s.flow||[]).filter(f=>f.k==='p').map((q,qi)=>`
        <div class="lr-q" id="lrq${qi}">
          <button class="lr-qh" onclick="lrTog(${qi})" aria-expanded="false" aria-controls="lrw${qi}">
            <span class="pip">${numL(qi+1)}</span>
            <span class="tx"><span class="dv" lang="sa">${q.d}</span>
              <span class="ia" lang="sa-Latn">${esc(q.t)}</span></span>
            <span class="chev">▾</span>
          </button>
          <div class="lr-words" id="lrw${qi}" hidden>${(q.words||[]).map(w=>`
            <div class="lr-word">
              <span class="d" lang="sa">${w[0]}</span>
              <span class="i" lang="sa-Latn">${esc(w[1])}</span>
              <span class="m">${esc(state.lang==='ne'?(w[3]||w[2]):state.lang==='hi'?(w[4]||w[2]):w[2])}</span>
            </div>`).join('')}</div>
        </div>`).join('')}</div>
      <div class="lr-mean"><span class="lb">${esc(L('in_other_words'))}</span>
        <div>${esc(T(s.paras))}</div></div>
      <div class="lr-nav">
        <button class="lr-ghost" onclick="lrTheme(${ci},${ti},${k-1})" ${k?'':'disabled'}>${esc(L('previous'))}</button>
        <span class="lr-hint">${esc(L('learn_meet_hint'))}</span>
        <button class="lr-cta" onclick="lrTheme(${ci},${ti},${k+1})">
          ${esc(last?L('learn_recall'):L('learn_next_verse'))}</button>
      </div>
    </div>` + backFoot(`showRead(${ci},'full')`, L('back_chapter_one'));
  scrollViewTop();
}
function lrTog(i){
  const box = document.getElementById('lrq'+i), w = document.getElementById('lrw'+i);
  if(!box||!w) return;
  const open = box.classList.toggle('open');
  w.hidden = !open;
  const b = box.querySelector('.lr-qh'); if(b) b.setAttribute('aria-expanded', open);
}

/* Is a word worth blanking? Judge the gloss by its CONTENT word: an early
   filter on /^(the|of|and)/ threw away "of all sacrifices" and "the great
   elements" — the best words in those verses — leaving four verses in the
   Gita with no cloze at all. */
function lrMeaty(w){
  if(!w || !w[0] || !w[2]) return false;
  if(w[0].length < 4) return false;
  const core = String(w[2]).replace(/^(?:the|of|a|an|to|in|by|for|from|with|O)\s+/i,'').trim();
  if(core.length < 4) return false;
  return !/^(and|but|indeed|also|too|not|even|alone|thus|so)$/i.test(core);
}
function lrDrill(ci, ti, vs){
  const ch = DATA[ci], t = ch.themes[ti];
  const pool = [], others = [];
  ch.themes.forEach(x=>thVerses(x).forEach(s=>{
    others.push(s);
    (s.flow||[]).forEach(f=>(f.words||[]).forEach(w=>{ if(lrMeaty(w)) pool.push(w); }));
  }));
  const items = [];
  vs.forEach(s=>{
    /* meaning -> verse. Distractors come from the same CHAPTER so the choice
       turns on what the verse says, not on which line looks unfamiliar. */
    /* Options are shown as the verse's FIRST PADA, so a distractor whose first
       pada is identical to the answer would render two indistinguishable
       choices with one marked wrong. 6.15 and 6.28 open with the same line
       (युञ्जन्नेवं सदात्मानं) — rare, but it must never happen. */
    /* Options are WHOLE VERSES, not opening lines — a first pāda is not a
       verse, and picking between four fragments is a shallower task than
       picking between four ślokas (owner 2026-09-01). Full verses are also
       unique book-wide, where four pairs share a first pāda. */
    const _full = v => v.d;
    const mine = _full(s);
    const wrong = lrSample(others.filter(o=>o.n!==s.n && _full(o)!==mine), 3);
    items.push({kind:'pick',
      ask: esc(L('learn_which')) + `<div class="lr-qsub">${esc(T(s.paras))}</div>`,
      opts: lrShuffle([s].concat(wrong)).map(o=>
        ({label: _full(o), sub: fmtNL(o.n), deva:1, ok:o===s})),
      note: `${esc(fmtNL(s.n))} — ${esc(T(s.lits))}`});

    /* Cloze on the AUTHORED WORD-SPLIT, never by blanking the recited line.
       Sanskrit sandhi means the dictionary form usually does NOT appear
       literally in the pada: पश्य + एताम् fuses to पश्यैतां, महतीम् is written
       महतीं, and उभयोः surfaces inside सेनयोरुभयोर्. A .replace() on the line
       missed 52% of words and failed SILENTLY — the line rendered intact, so
       the question read "which word is missing?" with nothing missing and
       every option equally arbitrary (owner hit this at 1.3, 2026-09-01).
       The word-split is authored data and always correct: hide a word THERE,
       and show the recited line beneath as the cue that ties it back. */
    const qs = (s.flow||[]).filter(f=>f.k==='p');
    const cands = [];
    qs.forEach(function(q,qi){
      const ws = q.words||[];
      if(ws.length < 2) return;                    // nothing to hide it among
      ws.forEach(function(w,wi){ if(lrMeaty(w)) cands.push({q:q,qi:qi,w:w,wi:wi,ws:ws}); });
    });
    if(cands.length){
      const c = cands[Math.floor(Math.random()*cands.length)];
      const split = c.ws.map(function(w,i){ return i===c.wi
        ? '<span class="lr-blank">?</span>'
        : '<span class="lr-tok">'+w[0]+'</span>'; }).join('<span class="lr-plus">+</span>');
      /* Distractors must be wrong AND non-obvious. Three separate traps:
         - same surface form as the answer, or same meaning -> not a distractor
         - a form ALREADY VISIBLE in the split is eliminable at a glance, so it
           silently makes the question easier (2.4% of questions before this)
         - two distractors identical to each other renders the same option
           twice (0.7% before this) — which looks like a bug, and is one */
      const shownForms = {};
      c.ws.forEach(function(x){ shownForms[x[0]] = 1; });
      const seenOpt = {};
      seenOpt[c.w[0]] = 1;
      const dw = [];
      lrShuffle(pool).forEach(function(x){
        if(dw.length >= 3) return;
        if(x[2] === c.w[2]) return;          // same meaning
        if(shownForms[x[0]]) return;         // already on screen
        if(seenOpt[x[0]]) return;            // duplicate option
        seenOpt[x[0]] = 1; dw.push(x);
      });
      items.push({kind:'pick',
        ask: esc(fmt(L('learn_missing'),{q:numL(c.qi+1), v:fmtNL(s.n)}))
             /* NO recited-line cue. It was added to help where sandhi
                transforms a word, but measured against the real data it gives
                the answer away in 6,069 of 6,394 questions — either literally
                (मामकाः inside मामकाः पाण्डवाश्चैव) or all but a letter
                (कुर्वत inside किमकुर्वत). Only 325 would keep a cue that
                genuinely helps, which is not worth a 95% leak.
                The surrounding words of the split ARE the context: supplying
                the missing word of a pāda you know is exactly the recall being
                tested (owner caught both leaks, 2026-09-01). */
             + `<div class="lr-split" lang="sa">${split}</div>`,
        opts: lrShuffle([c.w].concat(dw)).map(function(o){
                return {label:o[0], sub:o[1], deva:1, ok:o===c.w}; }),
        note: `<b lang="sa">${esc(c.w[0])}</b> (${esc(c.w[1])}) — ${esc(c.w[2])}`});
    }
  });
  /* Reorder the verses of the theme. The chip must NOT carry the verse number:
     printing "1.1 / 1.2 / 1.3" turns recall into sorting integers, which tests
     nothing (owner spotted this at ch1.t1, 2026-09-01). The paraphrase alone is
     the cue — verified unique across all 700 verses at this length. */
  if(vs.length > 1) items.push({kind:'order',
    ask: esc(fmt(L('learn_vorder'),{t:T(t.titles)})),
    chips: vs.map((s,i)=>({id:i, label: T(s.paras).slice(0, 64) + '…'})),
    answer: vs.map((_,i)=>i)});

  /* Reorder the four quarters — for EVERY verse of the theme, not a sample.
     Every verse in the Gītā has exactly four, all textually distinct, so the
     drill is always fair, and putting a śloka back together pāda by pāda is
     how it is actually committed to memory. Doing one verse per theme left
     478 of the 700 never practised this way (owner 2026-09-01). */
  vs.forEach(qv=>{
    const qq = (qv.flow||[]).filter(f=>f.k==='p');
    if(qq.length > 2) items.push({kind:'order',
      ask: esc(fmt(L('learn_qorder'),{v:fmtNL(qv.n)})),
      chips: qq.map((q,i)=>({id:i, label:q.d, deva:1})),
      answer: qq.map((_,i)=>i)});
  });

  lrRun(ci, lrShuffle(items), T(t.titles), ()=>{
    const p = lrGet(ch.num); p.themes[ti] = 1; lrPut(ch.num, p);
    const nxt = ch.themes.findIndex((_,i)=>!lrGet(ch.num).themes[i]);
    view.innerHTML = `<div class="lrn fade-in"><div class="lr-finis">
        <div class="lr-seal">✓</div>
        <h2>${esc(T(t.titles))}</h2>
        <p>${esc(fmt(L('learn_theme_done_d'),{n:numL(vs.length)+' '+(vs.length===1?L('verse'):L('verses'))}))}</p>
        ${nxt>=0 ? `<button class="lr-cta" onclick="lrTheme(${ci},${nxt},0)">${esc(L('learn_next_theme'))}</button>`
                 : `<p class="lr-all">${esc(fmt(L('learn_all_done'),{n:numL(ch.num)}))}</p>`}
        <button class="lr-ghost" onclick="lrFree(${ci},${ti})">${esc(L('learn_free_go'))}</button>
        <button class="lr-ghost" onclick="showRead(${ci},'full')">${esc(L('back_chapter_one'))}</button>
      </div></div>`;
    scrollViewTop();
  });
}

/* ---------------- free practice ----------------
   After a theme is held, the reader may keep going for as long as they like:
   one verse from this theme with its four pādas shuffled, reorder, then pull
   another. Deliberately OUTSIDE the queue engine — nothing is scored, nothing
   is required, and leaving costs nothing. Practice, not examination. */
var FP = {ci:0, ti:0, v:null, order:[], deal:[], picked:[]};
function lrFree(ci, ti){
  state.view='learn'; state.chapter=ci; state.theme=ti;
  state.lrAt = {kind:'theme', ti:ti};
  FP.ci = ci; FP.ti = ti;
  lrFreePick();
}
function lrFreePick(){
  const ch = DATA[FP.ci], t = ch.themes[FP.ti], vs = thVerses(t);
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
  const ch = DATA[FP.ci], t = ch.themes[FP.ti], v = FP.v;
  const done = FP.picked.length === FP.order.length;
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'),'showSections()'],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, `showLearn(${FP.ci})`],
      [T(t.titles), null]])}
    <div class="lrn fade-in">
      <div class="lr-k">${esc(L('learn_free'))}</div>
      <h2 class="view-title">${esc(T(t.titles))}</h2>
      <div class="view-sub">${esc(L('learn_free_d'))}</div>
      <div class="lr-qbox">
        <div class="lr-ask">${esc(fmt(L('learn_qorder'),{v:fmtNL(v.n)}))}</div>
        <div class="lr-slots" id="fpSlots">${FP.picked.map((ix,k)=>
          `<span class="lr-slot dv" lang="sa">${numL(k+1)}. ${esc(FP.order[ix].d)}</span>`).join('')}</div>
        <div class="lr-chips" id="fpChips">${(FP.deal||FP.order.map((_,i)=>i)).map(ix=>
          FP.picked.indexOf(ix) >= 0 ? '' :
          `<button class="lr-chip2 dv" lang="sa" onclick="lrFreeTap(${ix})">${esc(FP.order[ix].d)}</button>`
        ).join('')}</div>
        <div class="lr-fb" id="fpFb">${done
          ? `<div class="good">${esc(L('learn_thread_ok'))}</div>
             <div class="lr-cue" lang="sa-Latn">${esc(v.t)}</div>`
          : ''}</div>
      </div>
      <div class="lr-nav">
        <button class="lr-cta" onclick="lrFreePick()">${esc(L('learn_shuffle'))}</button>
        <span class="lr-hint">${esc(fmtNL(v.n))}</span>
        <button class="lr-ghost" onclick="showRead(${FP.ci},'full')">${esc(L('learn_done_free'))}</button>
      </div>
    </div>` + backFoot(`showRead(${FP.ci},'full')`, L('back_chapter_one'));
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

/* ---------------- Play ----------------
   A front door onto the drill engine that needs no path, no progress and no
   commitment: open it from the tool row at any time, pick a scope and a mode,
   and answer as long as you like. Deliberately UNSCORED and unsaved — Learn by
   heart is the path with gating and progress; Play is the shuffle you drop
   into. If Play started tracking progress the two would blur (owner 2026-09-01).
   Everything here reuses lrRun/lrPaint/lrPick/lrChip. */
var PL = {scope:'all', ch:0, mode:0, run:0, q:null};

function showPlay(){
  rememberOrigin();
  state.view='play'; state.chapter=null; state.theme=null; renderCrumbs();
  view.innerHTML = `
    <div class="lrn fade-in">
      <h2 class="view-title">${esc(L('play_title'))}</h2>
      <div class="view-sub">${esc(L('play_sub'))}</div>

      <div class="pl-scope">
        <span class="pl-lb">${esc(L('play_scope'))}</span>
        <button class="lr-ghost${PL.scope==='all'?' on':''}" onclick="plScope('all')">${esc(L('play_all'))}</button>
        <button class="lr-ghost${PL.scope==='ch'?' on':''}" onclick="plScope('ch')">${esc(L('play_ch'))}</button>
        ${PL.scope==='ch' ? `<select class="pl-sel" onchange="PL.ch=+this.value;showPlay()">
            ${DATA.map((c,i)=>`<option value="${i}"${i===PL.ch?' selected':''}>${esc(L('chapter'))} ${numL(c.num)} · ${esc(T(c.names))}</option>`).join('')}
          </select>` : ''}
      </div>

      <div class="pl-modes">
        ${[[1,'play_m1','play_m1_d'],[2,'play_m2','play_m2_d'],[3,'play_m3','play_m3_d']].map(([m,t,d])=>`
          <button class="pl-mode" onclick="plStart(${m})">
            <span class="n">${numL(m)}</span>
            <span class="b"><b>${esc(L(t))}</b><span>${esc(L(d))}</span></span>
          </button>`).join('')}
      </div>
    </div>` + backFoot('showWelcome()', L('home_plain'));
  scrollViewTop();
}
function plScope(s){ PL.scope = s; showPlay(); }

/* The pool Play draws from: the whole book, or one chapter. */
function plPool(){
  const out = [];
  DATA.forEach((c,ci)=>{
    if(PL.scope === 'ch' && ci !== PL.ch) return;
    c.themes.forEach(t=>thVerses(t).forEach(s=>out.push(s)));
  });
  return out;
}
/* An option is a WHOLE VERSE, never its opening line: a first pāda is not a
   verse, and choosing between four fragments is a different (easier, shallower)
   task than choosing between four ślokas — owner 2026-09-01.
   A welcome consequence: full verses are unique book-wide (verified across all
   700), whereas four PAIRS share a first pāda — 3.35/18.47, 6.15/6.28,
   9.34/18.65, 16.07/18.30 — so the identical-option guard that case needed is
   no longer required. It stays as an assertion in the health checks. */
const plFull = v => v.d;

function plStart(mode){
  PL.mode = mode; PL.run = 0; PL.q = null;
  plNext();
}
/* One question at a time, drawn fresh — an endless game, not a finite queue. */
function plNext(keep){
  const pool = plPool();
  if(pool.length < 4){ showPlay(); return; }
  /* `keep` rebuilds the question that is already on screen — used when the
     reader switches language mid-game. Only the ASK, the NOTE and the numerals
     are language-bound; the verses and pādas are Devanagari either way, so the
     question is fully derivable from the verse id plus the option order we
     stored. Quitting to the menu for a language change was needless
     (owner 2026-09-02). */
  const s = keep ? (pool.find(v=>v.n === keep.n) || pool[Math.floor(Math.random()*pool.length)])
                 : pool[Math.floor(Math.random()*pool.length)];
  let item;

  if(PL.mode === 1){
    /* Given the number, choose the verse. Distractors must not share the
       answer's opening line: four verse PAIRS in the Gita open identically
       (3.35/18.47, 6.15/6.28, 9.34/18.65, 16.07/18.30), which would render two
       indistinguishable options with one marked wrong. */
    const mine = plFull(s);
    const ordered = keep ? keep.ord.map(n=>pool.find(v=>v.n===n)).filter(Boolean)
                         : null;
    const four = (ordered && ordered.length===4) ? ordered
               : lrShuffle([s].concat(lrSample(pool.filter(o=>o.n!==s.n && plFull(o)!==mine), 3)));
    PL.q = {n:s.n, ord:four.map(o=>o.n)};
    item = {kind:'pick',
      ask: esc(fmt(L('play_q1'),{v:fmtNL(s.n)})),
      opts: four.map(o=>({label:plFull(o), deva:1, ok:o===s})),
      note: `${esc(fmtNL(s.n))} — ${esc(T(s.lits))}`};

  }else if(PL.mode === 2){
    /* Given the verse, choose its number. Distractors are NEAR MISSES from the
       same chapter — random numbers from elsewhere would be given away by
       chapter recognition alone, testing nothing. */
    const same = pool.filter(o=>o.n.split('.')[0] === s.n.split('.')[0] && o.n !== s.n);
    const near = same.sort((a,b)=>
      Math.abs(parseInt(a.n.split('.')[1],10) - parseInt(s.n.split('.')[1],10)) -
      Math.abs(parseInt(b.n.split('.')[1],10) - parseInt(s.n.split('.')[1],10))).slice(0,6);
    const ordered2 = keep ? keep.ord.map(n=>pool.find(v=>v.n===n)).filter(Boolean) : null;
    const four2 = (ordered2 && ordered2.length===4) ? ordered2
                : lrShuffle([s].concat(lrSample(near.length >= 3 ? near : pool.filter(o=>o.n!==s.n), 3)));
    PL.q = {n:s.n, ord:four2.map(o=>o.n)};
    item = {kind:'pick',
      ask: esc(L('play_q2')) + `<div class="lr-qsub dv" lang="sa">${s.d}</div>`,
      opts: four2.map(o=>({label:fmtNL(o.n), ok:o===s})),
      note: `${esc(fmtNL(s.n))} — ${esc(T(s.lits))}`};

  }else{
    const qq = (s.flow||[]).filter(f=>f.k==='p');
    PL.q = {n:s.n, ord:[]};
    item = {kind:'order',
      ask: esc(fmt(L('learn_qorder'),{v:fmtNL(s.n)})),
      chips: qq.map((q,i)=>({id:i, label:q.d, deva:1})),
      answer: qq.map((_,i)=>i)};
  }
  /* A one-item run: when it finishes, deal another. That is the endless game. */
  lrRun(0, [item], L('play_title') + (PL.run ? ' · ' + fmt(L('play_round'),{n:numL(PL.run)}) : ''),
        ()=>{ PL.run++; plNext(); },
        {fn:'showPlay()', label:'play_title'});
}

/* ---------------- the drill engine ----------------
   One queue. A miss is not a failure: it goes to the back and comes round
   again, and the run ends only when the queue is genuinely empty. */
var LQ=[], LQi=0, LQmiss=0, LQdone=null, LQlab='', LQpick=[], LQci=0;
/* Where the queue's footer should lead. The learn path is inside a chapter;
   Play is not — it passed ci=0 and so offered "back to chapter", which sent the
   reader to chapter 1 from a game that spans the whole Gītā (owner
   2026-09-01). */
var LQback = null;
function lrRun(ci, items, label, done, back){
  LQci=ci; LQback=back||null; LQ=items.slice(); LQi=0; LQmiss=0; LQlab=label; LQdone=done; lrPaint();
}
function lrPaint(){
  if(LQi >= LQ.length) return LQdone();
  const it = LQ[LQi]; LQpick = [];
  /* A one-item queue (Play) has no progress to show: the bar would sit at 0%
     forever and the counter would read "1 / 1". Show the run's streak instead,
     which is the only number that means anything in an endless game
     (owner 2026-09-01). */
  const single = LQ.length === 1 && LQback;
  const pct = Math.round(LQi/LQ.length*100);
  const head = single
    ? `<div class="lr-progl pl-head">${esc(LQlab)}</div>`
    : `<div class="lr-prog"><i style="width:${pct}%"></i></div>
       <div class="lr-progl">${esc(LQlab)} · ${numL(LQi+1)} / ${numL(LQ.length)}${
         LQmiss?' · '+esc(fmt(L('learn_revisit'),{n:numL(LQmiss)})):''}</div>`;
  /* Re-shuffle the options every time the question is painted. They were
     shuffled once at build time, so a requeued question came back with the
     four verses in the SAME positions — and the reader already knew which one
     was wrong, making the retry a 1-in-3 guess rather than recall. Shuffling
     the ARRAY (not just the render) keeps lrPick's index honest, since it
     looks the answer up by position (owner 2026-09-02). */
  if(it.kind === 'pick' && it._seen) it.opts = lrShuffle(it.opts);
  it._seen = 1;
  const body = it.kind === 'pick'
    ? `<div class="lr-ask">${it.ask}</div>
       <div class="lr-opts">${it.opts.map((o,i)=>`
         <button class="lr-opt" onclick="lrPick(${i})">
           <span class="ol${o.deva?' dv':''}"${o.deva?' lang="sa"':''}>${o.deva?o.label:esc(o.label)}</span>
           ${o.sub?`<span class="os">${esc(o.sub)}</span>`:''}
         </button>`).join('')}</div>`
    : `<div class="lr-ask">${it.ask}</div>
       <div class="lr-slots" id="lrSlots"></div>
       <div class="lr-chips">${lrShuffle(it.chips).map(c=>`
         <button class="lr-chip2${c.deva?' dv':''}"${c.deva?' lang="sa"':''} onclick="lrChip(this,${c.id})">${esc(c.label)}</button>`).join('')}</div>`;
  view.innerHTML = `<div class="lrn fade-in">${head}
    <div class="lr-qbox">${body}<div class="lr-fb" id="lrFb"></div></div>
    </div>` + (LQback
      ? backFoot(LQback.fn, L(LQback.label))
      : backFoot(`showRead(${LQci},'full')`, L('back_chapter_one')));
  scrollViewTop();
}
function lrPick(i){
  const it = LQ[LQi], o = it.opts[i];
  document.querySelectorAll('.lr-opt').forEach((b,k)=>{
    b.disabled = true;
    if(it.opts[k].ok) b.classList.add('right');
    else if(k === i) b.classList.add('wrong');
  });
  const fb = document.getElementById('lrFb');
  if(o.ok){
    fb.innerHTML = `<div class="good">${esc(L('learn_yes'))}</div>`;
    LQi++; setTimeout(lrPaint, 620);
  }else{
    LQmiss++; LQ.push(it);
    /* The tick and cross on the options already say right and wrong, so the
       feedback line drops the verdict and keeps only what the reader cannot
       see: the correct verse and its meaning. The button says what pressing it
       DOES — in Play the same question returns, so "select again" is literally
       true; in a multi-question drill the missed item is requeued and comes
       back later, which is the same promise. (owner 2026-09-02) */
    fb.innerHTML = (it.note?`<div class="nt">${it.note}</div>`:'')
      + `<button class="lr-cta" onclick="LQi++;lrPaint()">${esc(L('learn_retry'))}</button>`;
  }
}
function lrChip(el, id){
  const it = LQ[LQi], want = it.answer[LQpick.length];
  const fb = document.getElementById('lrFb');
  if(id === want){
    /* Clear any standing "not there yet" the moment the reader gets it right.
       Without this the correction stays on screen for the rest of the question
       and reads as though the new, correct answer were also wrong
       (owner 2026-09-01). */
    if(fb) fb.innerHTML = '';
    LQpick.push(id); el.disabled = true; el.classList.add('used');
    /* carry the chip's script class through, or a Devanagari pāda drops back
       to the Latin face the moment it is placed */
    const dv = el.classList.contains('dv') ? ' dv' : '';
    document.getElementById('lrSlots').insertAdjacentHTML('beforeend',
      `<span class="lr-slot${dv}"${dv?' lang="sa"':''}>${numL(LQpick.length)}. ${esc(el.textContent.trim())}</span>`);
    if(LQpick.length === it.answer.length){
      fb.innerHTML = `<div class="good">${esc(L('learn_thread_ok'))}</div>`;
      LQi++; setTimeout(lrPaint, 700);
    }
  }else{
    LQmiss++;
    el.classList.add('shake'); setTimeout(()=>el.classList.remove('shake'), 380);
    const r = it.chips.find(c=>c.id===want);
    fb.innerHTML = `<div class="bad">${esc(L('learn_nextis'))} <b>${esc(r?r.label:'')}</b></div>`;
  }
}
"""

LEARN_CSS = r"""
  /* ---------- Play ---------- */
  /* The scope row is the same segmented-pill grammar as the chapter chooser:
     soft pill = an option, gold pill = where you are (PROJECT.md, mode-box). */
  .pl-scope{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin:4px 0 22px;}
  .pl-scope .pl-lb{ font-family:system-ui,sans-serif; font-size:.74rem; letter-spacing:.14em;
                    text-transform:uppercase; color:var(--ink-soft);}
  .pl-scope .lr-ghost.on{ background:var(--saffron); border-color:var(--saffron);
                          color:var(--on-saffron);}
  /* matches .tool-btn geometry so the select sits level with the pills */
  .pl-sel{ padding:8px 16px; border-radius:999px; border:1px solid var(--line);
           background:var(--paper); color:var(--teal); font-family:inherit;
           font-weight:700; font-size:.85rem; max-width:100%; cursor:pointer;
           transition:.15s;}
  .pl-sel:hover{ border-color:var(--saffron);}
  .pl-modes{ display:grid; gap:11px; grid-template-columns:repeat(auto-fit,minmax(240px,1fr));}
  /* same shape as .card: --paper, 16px radius, 1px shadow, saffron on hover */
  .pl-mode{ display:flex; gap:13px; align-items:flex-start; text-align:left; padding:16px 18px;
            border-radius:16px; background:var(--paper); border:1px solid var(--line);
            border-left:2px solid var(--saffron);
            box-shadow:0 1px 2px rgba(var(--shadow),.05); cursor:pointer;
            font-family:inherit; transition:.18s;}
  .pl-mode:hover{ border-color:var(--saffron); border-left-color:var(--saffron-dark);
                  box-shadow:0 4px 14px rgba(var(--shadow),.10); transform:translateY(-2px);}
  .pl-mode .n{ flex:0 0 30px; height:30px; border-radius:50%; display:grid; place-items:center;
               background:var(--saffron-soft); color:var(--saffron-dark);
               font-family:system-ui,sans-serif; font-weight:700; font-size:.85rem;}
  .pl-mode .b{ flex:1; min-width:0;}
  .pl-mode .b b{ display:block; font-size:1.06rem; font-weight:700; color:var(--teal);
                 margin-bottom:4px;}
  .pl-mode .b span{ display:block; color:var(--ink-soft); font-size:.86rem; line-height:1.5;}
  @media (max-width:640px){ .pl-modes{ grid-template-columns:1fr;} .pl-sel{ flex:1 0 100%;} }

  /* ---------- Learn by heart ---------- */
  .lrn{ max-width:760px; }
  .lr-k{ font-family:system-ui,sans-serif; font-size:.68rem; letter-spacing:.2em;
         text-transform:uppercase; color:var(--ink-soft); margin-bottom:4px;}
  /* Owner 2026-09-01: the drill must not look like a different app. These
     mirror .tool-btn / .tool-btn.primary exactly — same padding, weight, size
     and hover — so a button here behaves like a button anywhere else. */
  .lr-cta{ background:var(--saffron); border:1px solid var(--saffron);
           color:var(--on-saffron); font-weight:700; font-size:.85rem;
           padding:8px 16px; border-radius:999px; cursor:pointer;
           font-family:inherit; transition:.15s;}
  .lr-cta:hover{ background:var(--saffron-dark); border-color:var(--saffron-dark);}
  .lr-ghost{ background:var(--paper); border:1px solid var(--line); color:var(--teal);
             font-weight:700; font-size:.85rem; padding:8px 16px; border-radius:999px;
             cursor:pointer; font-family:inherit; transition:.15s;}
  .lr-ghost:hover:not(:disabled){ border-color:var(--saffron); background:var(--saffron-soft);}
  .lr-ghost:disabled{ opacity:.35; cursor:default;}
  .lr-ghost.sm{ font-size:.76rem; padding:7px 13px;}

  .lr-prog{ height:5px; border-radius:3px; background:var(--chip); overflow:hidden; margin-top:8px;}
  .lr-prog i{ display:block; height:100%; background:var(--saffron); border-radius:3px;
              transition:width .45s cubic-bezier(.2,.8,.2,1);}
  .lr-progl{ font-family:system-ui,sans-serif; font-size:.74rem; color:var(--ink-soft); margin:7px 0 18px;}

  /* matches .card: --paper, 16px radius, the same 1px shadow and hover lift */
  .lr-step{ display:flex; gap:14px; padding:16px 18px; border-radius:16px; margin-bottom:13px;
            background:var(--paper); border:1px solid var(--line);
            border-left:2px solid var(--saffron);
            box-shadow:0 1px 2px rgba(var(--shadow),.05); transition:.18s;}
  /* the step you are on wears the full saffron edge; a finished one turns teal */
  .lr-step.now{ border-color:var(--saffron); border-left-color:var(--saffron-dark);}
  .lr-step.done{ border-left-color:var(--teal);}
  .lr-step.locked{ opacity:.55;}
  .lr-badge{ flex:0 0 30px; height:30px; border-radius:50%; display:grid; place-items:center;
             background:var(--saffron-soft); color:var(--saffron-dark);
             font-family:system-ui,sans-serif; font-weight:700; font-size:.84rem;}
  .lr-step.now .lr-badge{ background:var(--saffron); color:var(--on-saffron);}
  .lr-step.done .lr-badge{ background:var(--teal); color:var(--on-accent);}
  .lr-body{ flex:1; min-width:0;}
  .lr-body h3{ margin:1px 0 5px; font-size:1.06rem; font-weight:700; color:var(--teal);}
  .lr-body p{ margin:0 0 11px; color:var(--ink-soft); font-size:.88rem; line-height:1.55;}

  .lr-grid{ display:grid; gap:8px; grid-template-columns:repeat(auto-fill,minmax(196px,1fr));}
  .lr-chip{ display:flex; align-items:center; gap:9px; text-align:left; padding:10px 12px;
            border-radius:12px; background:var(--paper); border:1px solid var(--line);
            border-left:2px solid var(--saffron);
            cursor:pointer; font-family:inherit; transition:.15s;}
  .lr-chip:hover{ border-color:var(--saffron); box-shadow:0 4px 14px rgba(var(--shadow),.10);}
  .lr-chip.ok{ border-color:var(--teal); border-left-color:var(--teal); background:var(--teal-soft);}
  .lr-chip .n{ flex:0 0 22px; height:22px; border-radius:50%; display:grid; place-items:center;
               background:var(--chip); font-size:.7rem; font-family:system-ui,sans-serif;
               color:var(--ink-soft);}
  .lr-chip.ok .n{ background:var(--teal); color:var(--on-accent); font-weight:700;}
  .lr-chip .t{ flex:1; font-size:.85rem; line-height:1.3;}
  .lr-chip .v{ font-family:system-ui,sans-serif; font-size:.7rem; color:var(--ink-soft);}

  .lr-foot{ display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-top:16px;
            font-family:system-ui,sans-serif; font-size:.74rem; color:var(--ink-soft);}

  .lr-thread{ list-style:none; margin:16px 0 0; padding:0;}
  .lr-thread li{ display:flex; gap:13px; padding:12px 13px; border-radius:13px; position:relative;}
  .lr-thread li:not(:last-child):after{ content:''; position:absolute; left:28px; top:42px;
            bottom:-2px; width:2px; background:var(--line);}
  .lr-thread .bead{ flex:0 0 26px; height:26px; border-radius:50%; display:grid; place-items:center;
            background:var(--saffron-soft); color:var(--saffron-dark); z-index:1;
            font-family:system-ui,sans-serif; font-size:.75rem; font-weight:700;}
  .lr-thread b{ font-weight:700; font-size:1rem; color:var(--teal);}
  .lr-thread .rg{ font-family:system-ui,sans-serif; font-size:.7rem; color:var(--saffron-dark); font-weight:600; margin-left:7px;}
  .lr-thread p{ margin:4px 0 0; color:var(--ink-soft); font-size:.86rem; line-height:1.5;}

  .lr-vnum{ font-family:system-ui,sans-serif; font-size:1.3rem; font-weight:700;
            color:var(--saffron-dark); margin:10px 0 12px;}
  .lr-quarters{ display:flex; flex-direction:column; gap:9px;}
  .lr-q{ border-radius:16px; background:var(--paper); border:1px solid var(--line);
         border-left:2px solid var(--saffron);
         box-shadow:0 1px 2px rgba(var(--shadow),.05); overflow:hidden; transition:.18s;}
  .lr-q.open{ border-color:var(--saffron); border-left-color:var(--saffron-dark);}
  .lr-qh{ display:flex; gap:12px; align-items:center; width:100%; text-align:left;
          padding:14px 16px; background:none; border:none; cursor:pointer; font-family:inherit;}
  .lr-qh .pip{ flex:0 0 25px; height:25px; border-radius:50%; display:grid; place-items:center;
          background:var(--saffron-soft); color:var(--saffron-dark);
          font-family:system-ui,sans-serif; font-size:.73rem; font-weight:700;}
  .lr-q.open .pip{ background:var(--saffron); color:var(--on-saffron);}
  .lr-qh .tx{ flex:1; min-width:0;}
  .lr-qh .dv{ display:block; font-family:"Noto Serif Devanagari",Georgia,serif;
              font-size:1.12rem; line-height:1.7;}
  .lr-qh .ia{ display:block; font-size:.78rem; font-style:italic; color:var(--ink-soft); margin-top:2px;}
  .lr-qh .chev{ color:var(--ink-soft); transition:transform .22s;}
  .lr-q.open .chev{ transform:rotate(180deg); color:var(--saffron);}
  /* [hidden] is only display:none at the UA default, so ANY explicit display
     silently defeats it — the word grid was open on arrival despite carrying
     the attribute (owner 2026-09-02). Restore it explicitly. */
  .lr-words[hidden]{ display:none; }
  .lr-words{ display:grid; gap:8px; padding:2px 16px 16px;
             grid-template-columns:repeat(auto-fill,minmax(148px,1fr));}
  .lr-word{ padding:9px 11px; border-radius:10px; background:var(--paper);
            border:1px solid var(--line); border-left:2px solid var(--saffron);}
  .lr-word .d{ display:block; font-family:"Noto Serif Devanagari",Georgia,serif;
               font-size:1rem; color:var(--saffron-dark);}
  .lr-word .i{ display:block; font-size:.71rem; font-style:italic; color:var(--ink-soft); margin:1px 0 3px;}
  .lr-word .m{ display:block; font-size:.84rem; line-height:1.4;}
  .lr-mean{ margin-top:14px; padding:14px 16px; border-radius:14px;
            background:var(--saffron-soft); border:1px solid var(--line);}
  .lr-mean .lb{ display:block; font-family:system-ui,sans-serif; font-size:.65rem;
                letter-spacing:.18em; text-transform:uppercase; color:var(--saffron-dark); margin-bottom:5px;}

  .lr-nav{ display:flex; align-items:center; gap:11px; flex-wrap:wrap; margin-top:20px;}
  .lr-hint{ flex:1; text-align:center; font-family:system-ui,sans-serif;
            font-size:.76rem; color:var(--ink-soft);}

  /* The question card sits on --cream so the --paper options READ as raised
     cards on top of it. Both were --paper, so every boundary vanished and the
     screen went flat white (owner 2026-09-01). */
  .lr-qbox{ padding:18px; border-radius:16px; background:var(--cream);
            border:1px solid var(--line); border-left:2px solid var(--teal);
            box-shadow:0 1px 2px rgba(var(--shadow),.05);}
  /* the question is the loudest thing on the screen, and saffron-soft under a
     saffron rule marks it as the prompt rather than more prose */
  .lr-ask{ font-size:1.06rem; line-height:1.6; margin:-2px -4px 16px; padding:12px 14px;
           border-radius:12px; background:var(--saffron-soft);
           border-left:2px solid var(--saffron); color:var(--ink);}
  .pl-head{ margin:6px 0 14px !important; color:var(--saffron-dark) !important;
            font-weight:700; letter-spacing:.1em; text-transform:uppercase;}
  .lr-qsub{ margin-top:10px; padding:12px 14px; border-radius:11px; background:var(--paper);
            border:1px solid var(--line); color:var(--ink-soft); font-size:.92rem; line-height:1.6;}
  .lr-qsub.dv{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.1rem; color:var(--ink);}
  .lr-split{ margin-top:11px; padding:14px; border-radius:11px; background:var(--paper);
             border:1px solid var(--line); display:flex; flex-wrap:wrap; gap:7px;
             align-items:center; justify-content:center;}
  .lr-tok{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.1rem;}
  .lr-plus{ color:var(--ink-soft); font-size:.8rem;}
  .lr-blank{ display:inline-grid; place-items:center; min-width:52px; padding:2px 12px;
             border-radius:8px; background:var(--saffron-soft); color:var(--saffron-dark);
             border:2px dashed var(--saffron); font-weight:700; font-size:1.1rem;}
  .lr-cue{ margin-top:8px; text-align:center; font-family:"Noto Serif Devanagari",Georgia,serif;
           font-size:.95rem; color:var(--ink-soft);}
  .lr-opts{ display:grid; gap:9px;}
  /* Options are whole ślokas now (66-134 characters), so they stack: the verse
     takes the full width and its number sits underneath, instead of the two
     competing for one line (owner 2026-09-01). */
  /* --paper on --cream is only a 1.06:1 step, so the SHADOW does the lifting,
     not the fill: without it the options dissolve into the question card. */
  .lr-opt{ display:flex; flex-direction:column; align-items:flex-start; gap:4px;
           text-align:left; width:100%;
           padding:13px 15px; border-radius:12px; background:var(--paper);
           border:1px solid var(--line); border-left:2px solid var(--saffron);
           cursor:pointer; font-family:inherit;
           box-shadow:0 1px 3px rgba(var(--shadow),.10); transition:.15s;}
  .lr-opt:hover:not(:disabled){ border-color:var(--saffron); background:var(--saffron-soft);}
  .lr-opt:disabled{ cursor:default;}
  .lr-opt .ol{ width:100%; font-size:.96rem; line-height:1.5; color:var(--ink);}
  .lr-opt .ol.dv{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.04rem;
                  line-height:1.85;}
  /* the verse number under an option is a NUMBER — saffron, like every other
     verse number in the app */
  .lr-opt .os{ font-family:system-ui,sans-serif; font-size:.74rem; font-weight:700;
               color:var(--saffron-dark);}
  /* the verdict must be unmistakable at a glance, not a 1px border change */
  /* The verdict is carried by the OPTION, not by a line of prose underneath
     (owner 2026-09-02). A tick and a cross in the leading edge, plus the fill,
     say it faster than any wording — and in every language at once. */
  .lr-opt.right, .lr-opt.wrong{ position:relative; padding-right:44px;}
  .lr-opt.right::after, .lr-opt.wrong::after{
      position:absolute; right:13px; top:50%; transform:translateY(-50%);
      width:22px; height:22px; border-radius:50%; display:grid; place-items:center;
      font-family:system-ui,sans-serif; font-size:.82rem; font-weight:700;
      line-height:1;}
  .lr-opt.right{ border-color:var(--teal); border-left-color:var(--teal);
                 border-width:2px; background:var(--teal-soft);
                 box-shadow:0 2px 10px rgba(var(--shadow),.14);}
  .lr-opt.right::after{ content:"\2713"; background:var(--teal); color:var(--on-accent);}
  /* the chosen wrong answer must read as wrong at a glance: red fill, red edge,
     a cross. No dimming — opacity made the mistake harder to study, which is
     backwards, since the mistake is the thing worth looking at. */
  .lr-opt.wrong{ border-color:var(--danger); border-left-color:var(--danger);
                 border-width:2px; background:var(--danger-soft); box-shadow:none;}
  /* --on-danger, not #FFF: the dark theme's red is light (#E86B5C), where white
     measures only 3.14:1. Each palette supplies the ink its own red needs. */
  .lr-opt.wrong::after{ content:"\2715"; background:var(--danger); color:var(--on-danger);}

  .lr-chips{ display:flex; flex-wrap:wrap; gap:8px;}
  .lr-chip2{ padding:11px 15px; border-radius:12px; background:var(--paper);
             border:1px solid var(--line); border-left:2px solid var(--saffron);
             cursor:pointer; font-family:inherit;
             font-size:.87rem; text-align:left; max-width:100%; transition:.15s;}
  .lr-chip2:hover:not(:disabled){ border-color:var(--saffron); background:var(--saffron-soft);}
  .lr-chip2.used{ opacity:.3; cursor:default; border-left-color:var(--teal);}
  /* Quarter chips carry Devanagari and need the Sanskrit face at a readable
     size — the Latin default renders the conjuncts too small to compare. */
  .lr-chip2.dv{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.05rem;
                line-height:1.75;}
  .lr-chip2.shake{ animation:lrshk .34s; border-color:var(--saffron-dark);}
  @keyframes lrshk{ 0%,100%{transform:none} 22%{transform:translateX(-6px)} 66%{transform:translateX(6px)} }
  .lr-slots{ display:flex; flex-direction:column; gap:6px; margin-bottom:13px;}
  .lr-slot{ padding:10px 13px; border-radius:12px; background:var(--teal-soft);
            border:1px solid var(--teal); border-left:2px solid var(--teal);
            font-size:.87rem;}
  .lr-slot.dv{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.02rem;}

  .lr-fb{ margin-top:14px;}
  .lr-fb .good{ color:var(--teal); font-weight:700; font-size:.92rem;}
  .lr-fb .bad{ color:var(--saffron-dark); font-weight:700; font-size:.92rem;}
  .lr-fb .nt{ margin:10px 0 13px; padding:12px 14px; border-radius:11px; background:var(--paper);
              border:1px solid var(--line); color:var(--ink-soft); font-size:.88rem; line-height:1.6;}

  /* the seal screen earns a teal wash — this is the one moment of arrival */
  .lr-finis{ text-align:center; padding:40px 18px; border-radius:18px;
             background:var(--teal-soft); border:1px solid var(--teal);}
  .lr-seal{ width:58px; height:58px; margin:0 auto 16px; border-radius:50%; display:grid;
            place-items:center; background:var(--teal-soft); color:var(--teal); font-size:1.6rem;}
  .lr-finis h2{ margin:0 0 8px; font-size:1.35rem; color:var(--teal);}
  .lr-finis p{ color:var(--ink-soft); max-width:50ch; margin:0 auto 16px; line-height:1.65;}
  .lr-finis .lr-all{ color:var(--saffron-dark); font-weight:700;}
  .lr-finis .lr-cta,.lr-finis .lr-ghost{ margin:5px;}

  @media (max-width:640px){
    .lr-grid{ grid-template-columns:1fr;}
    .lr-words{ grid-template-columns:repeat(auto-fill,minmax(124px,1fr));}
    .lr-nav .lr-cta,.lr-nav .lr-ghost{ flex:1;}
    .lr-hint{ flex:1 0 100%; order:3;}
  }
"""
