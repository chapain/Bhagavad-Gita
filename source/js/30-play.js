/* ---------------- Play ----------------
   A front door onto the drill engine that needs no path, no progress and no
   commitment: open it from the tool row at any time, pick a scope and a mode,
   and answer as long as you like. Deliberately UNSCORED and unsaved — Learn by
   heart is the path with gating and progress; Play is the shuffle you drop
   into. If Play started tracking progress the two would blur (owner 2026-09-01).
   Everything here reuses lrRun/lrPaint/lrPick/lrChip. */
var PL = {scope:'all', ch:0, mode:0, run:0, q:null, active:false};

function showPlay(){
  if(!App.library.ready()){ loadAllChapters().then(showPlay); return; }
  PL.active = false;
  App.library.rememberOrigin();
  App.session.update({view:'play', chapter:null, theme:null}); App.views.persist(); App.views.renderCrumbs();
  view.innerHTML = `
    <div class="lrn fade-in">
      <h2 class="view-title">${esc(L('play_title'))}</h2>
      <div class="view-sub">${esc(L('play_sub'))}</div>

      <div class="pl-scope">
        <span class="pl-lb">${esc(L('play_scope'))}</span>
        <button class="lr-ghost${PL.scope==='all'?' on':''}" onclick="plScope('all')">${esc(L('play_all'))}</button>
        <button class="lr-ghost${PL.scope==='ch'?' on':''}" onclick="plScope('ch')">${esc(L('play_ch'))}</button>
        ${PL.scope==='ch' ? `<select class="pl-sel" onchange="App.play.chooseChapter(+this.value)">
            ${DATA.map((c,i)=>`<option value="${i}"${i===PL.ch?' selected':''}>${esc(L('chapter'))} ${numL(c.num)} · ${esc(T(c.names))}</option>`).join('')}
          </select>` : ''}
      </div>

      <div class="pl-modes">
        ${[[1,'play_m1','play_m1_d'],[2,'play_m2','play_m2_d'],[3,'play_m3','play_m3_d']].map(([m,tk,d])=>`
          <button class="pl-mode" onclick="plStart(${m})">
            <span class="n">${numL(m)}</span>
            <span class="b"><b>${esc(L(tk))}</b><span>${esc(L(d))}</span></span>
          </button>`).join('')}
      </div>
    </div>` + backFoot('App.views.welcome()', L('home_plain'));
  scrollViewTop();
}
function plScope(s){ PL.scope = s; showPlay(); }
function plChooseChapter(ci){ PL.ch = ci; showPlay(); }

/* The pool Play draws from: the whole book, or one chapter. */
function plPool(){
  const out = [];
  DATA.forEach((c,ci)=>{
    if(PL.scope === 'ch' && ci !== PL.ch) return;
    c.themes.forEach(t=>App.learn.themeVerses(t).forEach(s=>out.push(s)));
  });
  return out;
}
/* An option is a WHOLE VERSE, never its opening line: a first pāda is not a
   verse, and choosing between four fragments is a different (easier, shallower)
   task than choosing between four ślokas — owner 2026-09-01.
   A welcome consequence: full verses are unique book-wide (verified across all
   700), whereas four PAIRS share a first pāda — 3.35/18.47, 6.15/6.28,
   9.34/18.65, 16.07/18.30 — so the identical-option guard that case needed is
   no longer required. Browser behavior checks assert that each rendered set
   contains four distinct complete verses. */
function hemiSplit(s){
  return String(s||'').split(/[।|]/).map(x => x.replace(/[॥\|\s]+$/g,'').trim()).filter(Boolean);
}
function slokaDeva(s){
  const h = hemiSplit(s && s.d);
  if(h.length < 2) return (s && s.d) || '';
  return h.map((p,i) => p + ((i % 2 === 0 && i < h.length - 1) ? ' ।' : ' ॥')).join(' ');
}
function slokaIast(s){
  const h = hemiSplit(s && s.t);
  if(h.length < 2) return (s && s.t) || '';
  return h.map((p,i) => p + ((i % 2 === 0 && i < h.length - 1) ? ' |' : ' ||')).join(' ');
}
const plFull = v => slokaDeva(v);
function saAsk(s){
  return `<div class="lr-qsub dv" lang="sa">${esc(slokaDeva(s))}`
    + (s.t ? `<div class="giast" lang="sa-Latn">${esc(slokaIast(s))}</div>` : '')
    + `</div>`;
}

function plNextId(n){
  const p = n.split('.');
  return p[0] + '.' + String(+p[1] + 1).padStart(2,'0');
}
function plStart(mode){
  PL.mode = mode; PL.run = 0; PL.q = null; PL.active = true;
  plNext();
}
/* One question at a time, drawn fresh — an endless game, not a finite queue. */
function plNext(keep){
  const pool = plPool();
  if(pool.length < 4){ showPlay(); return; }
  /* `keep` rebuilds the question that is already on screen — used when the
     reader switches language mid-game. */
  let s = keep ? (pool.find(v=>v.n === keep.n) || pool[Math.floor(Math.random()*pool.length)])
               : pool[Math.floor(Math.random()*pool.length)];
  let item;

  if(PL.mode === 1){
    /* Manana: the śloka is given; the work is to take its sense.
       Distractors are other paraphrases, preferably the same chapter so
       the topic cannot give the answer away. */
    const sense = o => T(o.paras);
    const mine = sense(s);
    const same = pool.filter(o=>o.n.split('.')[0]===s.n.split('.')[0] && o.n!==s.n && sense(o)!==mine);
    const rest = pool.filter(o=>o.n!==s.n && sense(o)!==mine);
    const distract = same.length >= 3 ? same : rest;
    const ordered = keep ? keep.ord.map(n=>pool.find(v=>v.n===n)).filter(Boolean) : null;
    const four = (ordered && ordered.length===4) ? ordered
               : App.learn.shuffle([s].concat(App.learn.sample(distract, 3)));
    PL.q = {n:s.n, ord:four.map(o=>o.n)};
    item = {kind:'pick',
      ask: esc(L('play_q1')) + saAsk(s),
      opts: four.map(o=>({oid:'verse:'+o.n, label:sense(o), ok:o===s})),
      note: `${esc(fmtNL(s.n))} — ${esc(T(s.lits))}`};

  }else if(PL.mode === 2){
    /* Sandarbha: the argument is a chain. Given this verse, which follows?
       Last-of-chapter verses have no successor — draw again. */
    if(!keep){
      let guard = 0;
      while(guard++ < 40 && !pool.find(o=>o.n===plNextId(s.n)))
        s = pool[Math.floor(Math.random()*pool.length)];
    }
    const nxt = pool.find(o=>o.n===plNextId(s.n));
    if(!nxt){ showPlay(); return; }
    const ch = s.n.split('.')[0];
    const same = pool.filter(o=>o.n.split('.')[0]===ch && o.n!==s.n && o.n!==nxt.n);
    const rest = pool.filter(o=>o.n!==s.n && o.n!==nxt.n);
    const distract = same.length >= 3 ? same : rest;
    const ordered2 = keep ? keep.ord.map(n=>pool.find(v=>v.n===n)).filter(Boolean) : null;
    const four2 = (ordered2 && ordered2.length===4) ? ordered2
                : App.learn.shuffle([nxt].concat(App.learn.sample(distract, 3)));
    PL.q = {n:s.n, ord:four2.map(o=>o.n)};
    item = {kind:'pick',
      ask: esc(L('play_q2')) + saAsk(s),
      opts: four2.map(o=>({oid:'verse:'+o.n, label:plFull(o), iast:slokaIast(o), deva:1, ok:o===nxt})),
      note: esc(T(nxt.lits))};

  }else{
    const qq = (s.flow||[]).filter(f=>f.k==='p');
    PL.q = {n:s.n, ord:[]};
    item = {kind:'order',
      ask: esc(fmt(L('learn_qorder'),{v:fmtNL(s.n)})),
      chips: qq.map((q,i)=>({id:i, label:q.d + pDanda(i, qq.length), iast:(q.t||'') + pDandaLatn(i, qq.length), deva:1})),
      answer: qq.map((_,i)=>i)};
  }
  item.qid = 'play:'+PL.mode+':'+s.n;
  /* A one-item run: when it finishes, deal another. That is the endless game. */
  App.drills.run(0, [item], L('play_title') + (PL.run ? ' · ' + fmt(L('play_round'),{n:numL(PL.run)}) : ''),
        ()=>{ PL.run++; plNext(); },
        {fn:'App.play.show()', label:'play_title'});
}


function playSessionSnapshot(){
  const snap = {scope:PL.scope, ch:PL.ch, mode:PL.mode, run:PL.run,
    q:PL.q || null, active:!!PL.active};
  const quiz = App.drills.capture();
  if(quiz) snap.quiz = quiz;
  return snap;
}
function hydratePlaySession(saved){
  if(!saved) return;
  PL.scope = saved.scope === 'ch' ? 'ch' : 'all';
  PL.ch = Number.isInteger(saved.ch) ? saved.ch : 0;
  PL.mode = Number.isInteger(saved.mode) ? saved.mode : 0;
  PL.run = Number.isInteger(saved.run) ? saved.run : 0;
  PL.q = saved.q || null; PL.active = !!saved.active;
}
function restorePlaySession(saved){
  hydratePlaySession(saved);
  if(!saved || !saved.active || !saved.q) return;
  plNext(saved.q);
  if(saved.quiz) App.drills.restore(saved.quiz);
}
function relanguagePlay(){
  if(PL.active && PL.q && PL.mode) plNext(PL.q);
  else showPlay();
}
App.play = Object.freeze({
  show: showPlay,
  chooseChapter: plChooseChapter,
  next: plNext,
  snapshot: playSessionSnapshot,
  hydrate: hydratePlaySession,
  restore: restorePlaySession,
  relanguage: relanguagePlay,
  slokaDeva,
  slokaIast
});
