/* ==================== Learn by heart ==================== */
/* ---------------- progress ----------------
   One key for all 18 chapters. Hardened like the favourites: a parse that
   succeeds still has to yield the shape we expect, or one bad value would
   throw on every render with no way back but clearing site data. */
/* Theme positions may change; stored completion needs its verse-range map.
   Historical maps are data, not guessed from the new index. Canonical verse
   holdings and favourites are independent and must never be reset here. */
const LR_LEGACY_MAP_OPTIONS = __LR_LEGACY_JSON__;
function lrAll(){
  try{
    const o = JSON.parse(localStorage.getItem('gitaLearn') || 'null');
    if(!o || typeof o !== 'object' || Array.isArray(o)) return {};
    const out = {};
    for(const k in o){
      if(!/^\d{1,2}$/.test(k) || +k < 1 || +k > 18) continue;
      const c = o[k];
      if(!c || typeof c !== 'object' || Array.isArray(c)) continue;
      const th = {};
      if(c.themes && typeof c.themes === 'object' && !Array.isArray(c.themes))
        for(const t in c.themes) if(/^\d+$/.test(t) && c.themes[t] === 1) th[t] = 1;
      const hd = {};
      if(c.held && typeof c.held === 'object' && !Array.isArray(c.held))
        for(const v in c.held) if(c.held[v] === 1) hd[v] = 1;
      out[k] = {story: c.story === 1 ? 1 : 0, themes: th, held: hd};
      if(Array.isArray(c.map) && c.map.length <= 78
         && c.map.every(r=>typeof r==='string' && /^\d{1,2}\.\d{2}–\d{1,2}\.\d{2}$/.test(r)))
        out[k].map = c.map.slice();
    }
    return out;
  }catch(e){ return {}; }
}
function lrGet(n){
  const a = lrAll(), existed = Object.prototype.hasOwnProperty.call(a, n);
  const p = a[n] || {story:0, themes:{}, held:{}};
  const ch = DATA && DATA[+n-1];
  // Do not migrate a chapter while its lazy payload is still unavailable.
  if(!ch || !ch.themes || !ch.themes.length) return p;
  const next = ch.themes.map(t=>t.range), before = JSON.stringify(p);
  let previous = p.map;
  if(!previous){
    const possibilities = LR_LEGACY_MAP_OPTIONS[n] || [];
    // A legacy record with no version cannot distinguish two different maps.
    // Do not transfer its numeric flags to an arbitrary interpretation.
    previous = possibilities.length === 1 ? possibilities[0] : null;
  }
  const same = previous && previous.join('|') === next.join('|');
  const kept = {};
  if(previous){
    for(const oldIndex in p.themes){
      const range = previous[+oldIndex], newIndex = next.indexOf(range);
      if(newIndex >= 0) kept[newIndex] = 1;
    }
  }
  p.themes = kept;
  if(!same) p.story = 0;  // the changed thread needs to be learned anew
  p.map = next;
  // p.held is deliberately untouched, even when an old theme disappears.
  if(existed && JSON.stringify(p) !== before){
    a[n] = p;
    try{ localStorage.setItem('gitaLearn', JSON.stringify(a)); }catch(e){}
  }
  return p;
}
function lrIast(){ return state.lang === 'en'; }
function lrGloss(w){
  return state.lang==='ne' ? (w[3]||w[2]) : state.lang==='hi' ? (w[4]||w[2]) : w[2];
}
function lrHeldOn(n, vn){ const p = lrGet(n); return !!(p.held||{})[vn]; }
function lrHold(n, vn, on){
  const p = lrGet(n); p.held = p.held || {};
  if(on) p.held[vn] = 1; else delete p.held[vn];
  lrPut(n, p);
}
function chVerseN(ch){ let n=0; ch.themes.forEach(t=> n += vCount(t)); return n; }
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

let LR_RANDOM_STATE = null;
function lrRandom(){
  if(LR_RANDOM_STATE == null) return Math.random();
  LR_RANDOM_STATE = (Math.imul(LR_RANDOM_STATE,1664525) + 1013904223) >>> 0;
  return LR_RANDOM_STATE / 4294967296;
}
function lrNewSeed(){ return (Date.now() ^ Math.floor(Math.random()*4294967296)) >>> 0 || 1; }
function lrWithSeed(seed, fn){
  const prev = LR_RANDOM_STATE;
  LR_RANDOM_STATE = (Number(seed) >>> 0) || 1;
  try{ return fn(); }finally{ LR_RANDOM_STATE = prev; }
}
const lrShuffle = a => { a = a.slice();
  for(let i=a.length-1;i>0;i--){ const j=Math.floor(lrRandom()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a; };
const lrSample = (arr,n) => lrShuffle(arr).slice(0,n);
/* every verse of a theme, flattened — parts are one verse each now, but the
   container is still there, so never assume */
function thVerses(t){ const out=[]; t.parts.forEach(p=>p.sutras.forEach(s=>out.push(s))); return out; }

/* ---------------- the path ---------------- */
function showLearn(ci){
  if(!GITA_CH[ci+1]||!GITA_CH[ci+1].themes){ loadChapter(ci+1).then(()=>showLearn(ci)).catch(gitaLoadFail); return; }
  App.library.rememberOrigin();
  state.view='learn'; state.chapter=ci; App.views.persist(); state.lrAt = null;
  state.section = state.section || Math.ceil(DATA[ci].num/6);
  state.theme=null; App.views.renderCrumbs();
  const ch = DATA[ci], p = lrGet(ch.num);
  const total = ch.themes.length, done = Object.keys(p.themes).length;
  const nv = chVerseN(ch), nh = Object.keys(p.held||{}).length;
  const pct = Math.round((p.story + done + nh) / (1 + total + nv) * 100);
  /* Which stage the reader is on. Every step used to render as `.now`, so all
     three wore the saffron edge at once and the accent meant nothing; the CSS
     has always defined `.done` and a quiet resting state. Exactly one card is
     current: the first stage that is not finished. A finished stage is
     `done`; a stage further along is simply quiet (and stays clickable — this
     path has never gated the reader). */
  const s1done = !!p.story, s2done = total > 0 && done === total,
        s3done = nv > 0 && nh === nv;
  const firstOpen = !s1done ? 1 : (!s2done ? 2 : (!s3done ? 3 : 0));
  const stepCls = (k, isDone) =>
    'lr-step' + (isDone ? ' done' : (firstOpen === k ? ' now' : ''));

  view.innerHTML = `
    ${App.views.breadcrumbs([[L('sections_title'),'App.views.sections()'],
      [App.views.wayName(Math.ceil(ch.num/6)), `App.views.chapters(${Math.ceil(ch.num/6)})`],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, null]])}
    ${App.views.chapterTitle(ch)}
    ${App.views.modeSwitch(ci)}
    <div class="lrn fade-in">
      <div class="view-sub">${esc(fmt(L('learn_sub'),{}))}</div>
      <div class="lr-prog"><i style="width:${pct}%"></i></div>
      <div class="lr-progl">${esc(fmt(L('learn_walked'),{p:numL(pct)}))}
        · ${esc(fmt(L('learn_held_n'),{a:numL(nh),b:numL(nv)}))}</div>

      <div class="${stepCls(1, s1done)}">
        <div class="lr-badge">${s1done?'✓':numL(1)}</div>
        <div class="lr-body">
          <h3>${esc(L('learn_s1'))}</h3>
          <p>${esc(fmt(L('learn_s1_d'),{n:numL(total)}))}</p>
          <button class="lr-cta" onclick="lrStory(${ci},0)">
            ${esc(p.story?L('learn_again'):L('learn_begin'))}</button>
        </div>
      </div>

      <div class="${stepCls(2, s2done)}">
        <div class="lr-badge">${s2done?'✓':numL(2)}</div>
        <div class="lr-body">
          <h3>${esc(L('learn_s2'))}</h3>
          <p>${esc(fmt(L('learn_s2_d'),{a:numL(done),b:numL(total)}))}</p>
          <div class="lr-grid">${ch.themes.map((t,ti)=>`
            <button class="lr-chip${p.themes[ti]?' ok':''}" onclick="lrTheme(${ci},${ti},0)">
              <span class="n">${p.themes[ti]?'✓':numL(ti+1)}</span>
              <span class="t">${esc(T(t.titles))}</span>
              <span class="v">${numL(vCount(t))}</span>
            </button>`).join('')}</div>
        </div>
      </div>

      <div class="${stepCls(3, s3done)}">
        <div class="lr-badge">${s3done?'✓':numL(3)}</div>
        <div class="lr-body">
          <h3>${esc(L('learn_s3'))}</h3>
          <p>${esc(L('learn_s3_d'))}</p>
          <button class="lr-ghost" onclick="lrFreeCh(${ci})">${esc(L('learn_free_go'))}</button>
        </div>
      </div>

      <div class="lr-foot">
        <span>${esc(L('learn_local'))}</span>
        ${(p.story||done||nh)?`<button class="lr-ghost sm" onclick="lrReset(${ch.num})">${esc(L('learn_restart'))}</button>`:''}
      </div>
    </div>` + backFoot(`App.views.chapters(${state.section||0})`, L('back_chapters'));
  scrollViewTop();
}
/* Re-enter the learn path in the new language, as near as possible to where
   the reader was. The current QUESTION is unrecoverable — it was generated
   from the old language's strings — but the theme or the story step is not,
   so restart that rather than the whole chapter. */
function lrRelang(ci){
  const at = state.lrAt;
  if(at && at.kind === 'theme' && DATA[ci] && DATA[ci].themes[at.ti]) return lrTheme(ci, at.ti, 0);
  if(at && at.kind === 'story') return lrStory(ci, 0);
  showLearn(ci);
}

/* ---------------- stage 1: the story ----------------
   Small chapters get read -> whole chain. Larger ones earn the middle two
   steps; drilling four stages over six themes is ceremony, not teaching. */
function lrPlan(ch){ return ch.themes.length >= 10 ? [0,1,2,3] : [0,3]; }

function lrStory(ci, step, seed){
  state.view='learn'; state.chapter=ci; App.views.persist(); state.theme=null;
  const ch = DATA[ci], th = ch.themes, plan = lrPlan(ch);
  const k = plan.indexOf(step), n = plan.length;
  if(step === 0){
    state.lrAt = {kind:'story', step:step};
    return lrStoryRead(ci, ch, th, k+1, n);
  }
  const quizSeed = Number.isInteger(seed) ? seed : lrNewSeed();
  state.lrAt = {kind:'story', step:step, seed:quizSeed};
  return lrWithSeed(quizSeed, ()=>{
    let items;
    if(step === 1){
      const groups = [];
      for(let i=0;i<th.length;i+=4) groups.push(th.slice(i,i+4).map((t,j)=>({t,i:i+j})));
      items = groups.filter(g=>g.length>1).map((g,gi)=>({kind:'order', qid:'story:1:'+gi,
        ask: esc(fmt(L('learn_order_few'),{n:numL(g.length)})),
        chips: g.map(x=>({id:x.i, label:T(x.t.titles)})),
        answer: g.map(x=>x.i)}));
    } else if(step === 2){
      items = th.slice(0,-1).map((t,i)=>{
        const right = th[i+1];
        const wrong = lrSample(th.filter((_,j)=>j!==i+1&&j!==i), 3);
        return {kind:'pick', qid:'story:2:'+i,
          ask: esc(fmt(L('learn_after'),{t:T(t.titles)})),
          opts: lrShuffle([right,...wrong]).map(x=>
            ({oid:'theme:'+th.indexOf(x), label:T(x.titles), ok:x===right})),
          note: esc(T(right.descs))};
      });
    } else {
      items = [{kind:'order', qid:'story:3:all',
        ask: esc(fmt(L('learn_order_all'),{n:numL(th.length)})),
        chips: th.map((t,i)=>({id:i, label:T(t.titles)})),
        answer: th.map((_,i)=>i)}];
    }
    const nxt = plan[k+1];
    App.drills.run(ci, items, fmt(L('learn_step'),{a:numL(k+1),b:numL(n)}),
      nxt === undefined ? ()=>lrStoryDone(ci) : ()=>lrStory(ci, nxt));
  });
}

var lrTest = 0, lrOpen = {};
function lrStoryRead(ci, ch, th, k, n){
  view.innerHTML = `
    ${App.views.breadcrumbs([[L('sections_title'),'App.views.sections()'],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, `showLearn(${ci})`],
      [L('learn_s1'), null]])}
    <div class="lrn fade-in">
      <div class="lr-k">${esc(fmt(L('learn_step'),{a:numL(k),b:numL(n)}))}</div>
      <h2 class="view-title">${esc(fmt(L('learn_read_h'),{n:numL(ch.num)}))}</h2>
      <div class="view-sub">${esc(L('learn_read_d'))}</div>
      <div class="lr-nav" style="margin-top:8px">
        <button class="lr-ghost${lrTest?' on':''}" onclick="lrTest=lrTest?0:1;lrOpen={};lrStoryRead(${ci},DATA[${ci}],DATA[${ci}].themes,${k},${n})">${esc(L('learn_test'))}</button>
      </div>
      <ol class="lr-thread">${th.map((t,i)=>{
        const hide = lrTest && !lrOpen[i];
        return `<li><span class="bead">${numL(i+1)}</span>
          <div><b>${esc(T(t.titles))}</b>
            <span class="rg">${esc(_drangeJS(t.range))}</span>
            ${hide
              ? `<button class="lr-ghost sm" onclick="lrOpen[${i}]=1;lrStoryRead(${ci},DATA[${ci}],DATA[${ci}].themes,${k},${n})">${esc(L('learn_reveal'))}</button>`
              : `<p>${esc(T(t.descs))}</p>`}</div></li>`;
      }).join('')}</ol>
      <div class="lr-nav">
        <button class="lr-cta" onclick="lrStory(${ci},${lrPlan(ch)[1]})">${esc(L('learn_read_go'))}</button>
      </div>
    </div>` + backFoot(`App.views.chapter(${ci})`, L('back_chapter_one'));
  scrollViewTop();
}
function lrStoryDone(ci){
  state.view='learn'; state.chapter=ci; state.lrAt = {kind:'storyDone'};
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
  state.view='learn'; state.chapter=ci; App.views.persist(); state.theme=ti;
  /* Remember the sub-view so a reload returns to this verse/theme, not the
     chapter's learning-path landing page. */
  const ch = DATA[ci], t = ch.themes[ti], vs = thVerses(t);
  state.lrAt = {kind:'theme', ti:ti, k:k, stage:k < vs.length ? 'meet' : 'land'};
  if(k < vs.length) return lrMeet(ci, ti, k, vs);
  lrThemeLand(ci, ti, vs);
}
var LV = {level:'full', shown:{}};
function lrSetLevel(lv){ LV.level = lv; LV.shown = {}; lrMeet(LV.ci, LV.ti, LV.k, LV.vs); }
function lrPeek(id){ LV.shown[id] = 1; lrMeet(LV.ci, LV.ti, LV.k, LV.vs); }
function lrHideAt(level, wi){
  if(level==='full') return false;
  if(level==='first') return wi !== 0;
  if(level==='half') return wi % 2 === 1;
  if(level==='blind') return true;
  return false;
}
function lrThemeLand(ci, ti, vs){
  const ch = DATA[ci], t = ch.themes[ti];
  state.lrAt = {kind:'theme', ti:ti, k:vs.length, stage:'land'};
  const p = lrGet(ch.num); p.themes[ti] = 1; lrPut(ch.num, p);
  const nxt = ch.themes.findIndex((_,i)=>!lrGet(ch.num).themes[i]);
  view.innerHTML = `<div class="lrn fade-in"><div class="lr-finis">
      <div class="lr-seal">✓</div>
      <h2>${esc(T(t.titles))}</h2>
      <p>${esc(L('learn_land_d'))}</p>
      <button class="lr-cta" onclick="lrFree(${ci},${ti})">${esc(L('learn_free_go'))}</button>
      <button class="lr-ghost" onclick="lrDrill(${ci},${ti},thVerses(DATA[${ci}].themes[${ti}]))">${esc(L('learn_recall_opt'))}</button>
      ${nxt>=0 ? `<button class="lr-cta" onclick="lrTheme(${ci},${nxt},0)">${esc(L('learn_next_theme'))}</button>`
               : `<p class="lr-all">${esc(fmt(L('learn_all_done'),{n:numL(ch.num)}))}</p>`}
      <button class="lr-ghost" onclick="showLearn(${ci})">${esc(L('opt_learn_s'))}</button>
    </div></div>`;
  scrollViewTop();
}
function lrMeet(ci, ti, k, vs){
  const ch = DATA[ci], t = ch.themes[ti], s = vs[k], last = k === vs.length-1;
  state.lrAt = {kind:'theme', ti:ti, k:k, stage:'meet'};
  LV.ci=ci; LV.ti=ti; LV.k=k; LV.vs=vs;
  const held = lrHeldOn(ch.num, s.n);
  const qs = (s.flow||[]).filter(f=>f.k==='p');
  const levels = [
    ['full','learn_lad_full','learn_lad_full_s'],
    ['first','learn_lad_first','learn_lad_first_s'],
    ['half','learn_lad_half','learn_lad_half_s'],
    ['blind','learn_lad_blind','learn_lad_blind_s']
  ];
  view.innerHTML = `
    ${App.views.breadcrumbs([[L('sections_title'),'App.views.sections()'],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, `showLearn(${ci})`],
      [T(t.titles), null]])}
    <div class="lrn fade-in">
      <div class="lr-k">${esc(L('learn_meet'))} · ${numL(k+1)} / ${numL(vs.length)}</div>
      <h2 class="view-title">${esc(T(t.titles))}</h2>
      <div class="lr-vnum">${esc(fmtNL(s.n))}${held?' · '+esc(L('learn_held')):''}</div>
      <div class="lr-ladder">
        <div class="lr-k">${esc(L('learn_ladder'))}</div>
        <div class="lr-lads">${levels.map(([id,a,b])=>`
          <button type="button" class="lr-lad${LV.level===id?' on':''}" onclick="lrSetLevel('${id}')">
            <b>${esc(L(a))}</b><span>${esc(L(b))}</span>
          </button>`).join('')}</div>
        <div class="lr-hint">${esc(L('learn_tap_blank'))}</div>
      </div>
      <div class="lr-quarters">${qs.map((q,qi)=>{
        const words = q.words||[];
        const useSplit = words.length > 1;
        let line;
        if(!useSplit){
          line = `<span class="dv" lang="sa">${q.d}</span>` + (lrIast()?`<span class="ia" lang="sa-Latn">${esc(q.t)}</span>`:'');
        } else {
          line = words.map((w,wi)=>{
            const id = qi+'_'+wi;
            const hide = lrHideAt(LV.level, wi) && !LV.shown[id];
            if(hide) return `<span class="lr-gap" role="button" tabindex="0" onclick="event.stopPropagation();lrPeek('${id}')">?</span>`;
            return `<span class="lr-tokw"><span class="d" lang="sa">${w[0]}</span>`
              + (lrIast()?`<span class="i" lang="sa-Latn">${esc(w[1])}</span>`:'')
              + `</span>`;
          }).join('');
        }
        return `<div class="lr-q" id="lrq${qi}">
          <button class="lr-qh" onclick="lrTog(${qi})" aria-expanded="false" aria-controls="lrw${qi}">
            <span class="pip">${numL(qi+1)}</span>
            <span class="tx">${line}</span>
            <span class="chev">▾</span>
          </button>
          <div class="lr-words" id="lrw${qi}" hidden>${words.map(w=>`
            <div class="lr-word">
              <span class="d" lang="sa">${w[0]}</span>
              ${lrIast()?`<span class="i" lang="sa-Latn">${esc(w[1])}</span>`:''}
              <span class="m">${esc(lrGloss(w))}</span>
            </div>`).join('')}</div>
        </div>`;
      }).join('')}</div>
      <div class="lr-mean"><span class="lb">${esc(L('in_other_words'))}</span>
        <div>${esc(T(s.paras))}</div></div>
      <div class="lr-nav">
        <button class="lr-ghost" onclick="LV.shown={};lrTheme(${ci},${ti},${k-1})" ${k?'':'disabled'}>${esc(L('previous'))}</button>
        <button class="lr-ghost" onclick="lrHold(${ch.num},'${s.n}',${held?0:1});lrMeet(${ci},${ti},${k},LV.vs)">${esc(held?L('learn_unhold'):L('learn_mark_held'))}</button>
        <button class="lr-cta" onclick="LV.shown={};lrTheme(${ci},${ti},${k+1})">
          ${esc(last?L('learn_read_go'):L('learn_next_verse'))}</button>
      </div>
    </div>` + backFoot(`App.views.chapter(${ci})`, L('back_chapter_one'));
  scrollViewTop();
}

function lrMeetGo(d){
  if(state.view !== 'learn' || !LV || !LV.vs) return;
  if($('#modalBg') && $('#modalBg').classList.contains('open')) return;
  const k = LV.k + d;
  if(k < 0 || k >= LV.vs.length) return;
  LV.shown = {};
  lrTheme(LV.ci, LV.ti, k);
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
function lrDrill(ci, ti, vs, seed){
  state.view='learn'; state.chapter=ci; state.theme=ti;
  const quizSeed = Number.isInteger(seed) ? seed : lrNewSeed();
  state.lrAt = {kind:'drill', ti:ti, seed:quizSeed}; App.views.persist();
  return lrWithSeed(quizSeed, ()=>{
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
    /* Options are WHOLE ŚLOKAS, not opening lines — a first pāda is not a
       verse, and picking between four fragments is a shallower task than
       picking between four ślokas (owner 2026-09-01). Full verses are also
       unique book-wide, where four pairs share a first pāda. */
    const _full = v => slokaDeva(v);
    const mine = _full(s);
    const wrong = lrSample(others.filter(o=>o.n!==s.n && _full(o)!==mine), 3);
    items.push({kind:'pick', qid:'drill:meaning:'+s.n,
      ask: esc(L('learn_which')) + `<div class="lr-qsub">${esc(T(s.paras))}</div>`,
      opts: lrShuffle([s].concat(wrong)).map(o=>
        ({oid:'verse:'+o.n, label: _full(o), iast:slokaIast(o), sub: fmtNL(o.n), deva:1, ok:o===s})),
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
      const c = cands[Math.floor(lrRandom()*cands.length)];
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
      items.push({kind:'pick', qid:'drill:cloze:'+s.n+':'+c.qi+':'+c.wi,
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
                return {oid:'word:'+o[0], label:o[0], iast:o[1], deva:1, ok:o===c.w}; }),
        note: `<b lang="sa">${esc(c.w[0])}</b>${state.lang==='en' ? ` (${esc(c.w[1])})` : ''} — ${esc(c.w[2])}`});
    }
  });
  /* Reorder the verses of the theme. The chip must NOT carry the verse number:
     printing "1.1 / 1.2 / 1.3" turns recall into sorting integers, which tests
     nothing (owner spotted this at ch1.t1, 2026-09-01). The paraphrase alone is
     the cue — verified unique across all 700 verses at this length. */
  if(vs.length > 1) items.push({kind:'order', qid:'drill:verse-order:'+ti,
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
    if(qq.length > 2) items.push({kind:'order', qid:'drill:pada-order:'+qv.n,
      ask: esc(fmt(L('learn_qorder'),{v:fmtNL(qv.n)})),
      chips: qq.map((q,i)=>({id:i, label:q.d + pDanda(i, qq.length), iast:(q.t||'') + pDandaLatn(i, qq.length), deva:1})),
      answer: qq.map((_,i)=>i)});
  });

  App.drills.run(ci, lrShuffle(items), T(t.titles), ()=>{
    const p = lrGet(ch.num); p.themes[ti] = 1; lrPut(ch.num, p);
    const nxt = ch.themes.findIndex((_,i)=>!lrGet(ch.num).themes[i]);
    view.innerHTML = `<div class="lrn fade-in"><div class="lr-finis">
        <div class="lr-seal">✓</div>
        <h2>${esc(T(t.titles))}</h2>
        <p>${esc(fmt(L('learn_theme_done_d'),{n:numL(vs.length)+' '+(vs.length===1?L('verse'):L('verses'))}))}</p>
        ${nxt>=0 ? `<button class="lr-cta" onclick="lrTheme(${ci},${nxt},0)">${esc(L('learn_next_theme'))}</button>`
                 : `<p class="lr-all">${esc(fmt(L('learn_all_done'),{n:numL(ch.num)}))}</p>`}
        <button class="lr-ghost" onclick="lrFree(${ci},${ti})">${esc(L('learn_free_go'))}</button>
        <button class="lr-ghost" onclick="App.views.chapter(${ci})">${esc(L('back_chapter_one'))}</button>
      </div></div>`;
    scrollViewTop();
  });
  });
}

/* ---------------- free practice ----------------
   After a theme is held, the reader may keep going for as long as they like:
   one verse from this theme with its four pādas shuffled, reorder, then pull
   another. Deliberately OUTSIDE the queue engine — nothing is scored, nothing
   is required, and leaving costs nothing. Practice, not examination. */
var FP = {ci:0, ti:0, v:null, order:[], deal:[], picked:[]};
function lrFree(ci, ti){
  state.view='learn'; state.chapter=ci; App.views.persist(); state.theme=ti;
  state.lrAt = {kind:'free', ti:ti};
  FP.ci = ci; FP.ti = ti;
  lrFreePick();
}
function lrFreeCh(ci){
  state.view='learn'; state.chapter=ci; App.views.persist(); state.theme=null;
  state.lrAt = {kind:'free', ti:-1};
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


/* Learn public boundary. Session details are implemented in the adjacent
   feature file but exposed here as one supported interface. */
App.learn = Object.freeze({
  show: showLearn,
  relanguage: lrRelang,
  story: lrStory,
  storyDone: lrStoryDone,
  theme: lrTheme,
  drill: lrDrill,
  freePaint: lrFreePaint,
  snapshot: learnSessionSnapshot,
  restore: restoreLearnSession,
  canNavigate(){ return !!(LV && LV.vs); },
  navigate: lrMeetGo,
  themeVerses: thVerses,
  shuffle: lrShuffle,
  sample: lrSample
});
