let DATA = null;
/* The verses arrive from data/ch<N>.js — one file per chapter, loaded by the
   script tags at the end of <body>. The loader assembles DATA and boots the
   app when the last one lands. */
const GITA_CH = {};
__DATALOADER__
const UI = __UI__;
const READER_SIZES = [80,90,100,110,120,130,140];
function savedReaderSize(){
  let size = 100;
  try{ size = Number(localStorage.getItem('gitaReaderSize')); }catch(e){}
  return READER_SIZES.includes(size) ? size : 100;
}
/* The site-wide language preference lives in localStorage. Keep a per-tab copy
   in sessionStorage as well: an update reload should restore this tab exactly,
   even if another tab has since chosen a different language. The history-entry
   snapshot is a further fallback. Owner 2026-10-14 reported नेपाली switching to
   English on a service-worker reload; language is now checked at first paint
   and again before the route renders. Whitelist all three codes so stale storage
   falls back to English rather than rendering a partial interface. */
const GITA_LANGS = ['en','ne','hi'];
function savedLang(){
  let l = null;
  try{ l = sessionStorage.getItem('gitaLang'); }catch(e){}
  if(!GITA_LANGS.includes(l)){
    try{
      const snap = history.state && history.state.gitaSession;
      if(snap && snap.path === location.pathname + location.search
         && snap.hash === (location.hash || '')) l = snap.lang;
    }catch(e){}
  }
  if(!GITA_LANGS.includes(l)){
    try{ l = localStorage.getItem('gitaLang'); }catch(e){}
  }
  return GITA_LANGS.includes(l) ? l : 'en';
}
const GITA_SESSION_KEY = 'gita.session.v1';
let GITA_RESTORING = false, GITA_PENDING_RESTORE = null, GITA_SESSION_TIMER = null,
    GITA_SESSION_MIRROR = false;
const state = { chapter:null, theme:null, idx:0, lang:savedLang(), view:'welcome', section:null, shared:null,
                readerSize:savedReaderSize() };
function sessionPathKey(){ return (location.pathname || '/') + (location.search || ''); }
function sessionNodePath(root, node){
  const path = []; let cur = node;
  while(cur && cur !== root){
    const parent = cur.parentElement;
    if(!parent) return null;
    path.unshift(Array.prototype.indexOf.call(parent.children, cur));
    cur = parent;
  }
  return cur === root ? path : null;
}
function sessionOpenDetails(root){
  if(!root) return [];
  const out = [];
  root.querySelectorAll('details[open]').forEach(el=>{
    const path = sessionNodePath(root, el);
    if(path) out.push(path);
  });
  return out;
}
function restoreSessionDetails(root, paths){
  if(!root || !Array.isArray(paths)) return;
  paths.forEach(path=>{
    if(!Array.isArray(path) || path.length > 32) return;
    let el = root;
    for(const n of path){
      if(!Number.isInteger(n) || n < 0 || !el.children[n]) return;
      el = el.children[n];
    }
    if(el && el.tagName === 'DETAILS') el.open = true;
  });
}
function sessionOrigin(o){
  if(!o || typeof o !== 'object') return null;
  const views = ['welcome','sections','chapters','chapter'];
  if(!views.includes(o.view)) return null;
  return {view:o.view,
    section:Number.isInteger(o.section) ? o.section : null,
    chapter:Number.isInteger(o.chapter) ? o.chapter : null,
    theme:Number.isInteger(o.theme) ? o.theme : null};
}
function validSessionSnapshot(s, pathKey, hash){
  if(!s || typeof s !== 'object' || s.version !== 1
     || s.path !== pathKey || s.hash !== hash || typeof s.route !== 'string'
     || !['welcome','sections','chapters','chapter','learn','search','favorites','play'].includes(s.view)
     || !GITA_LANGS.includes(s.lang)) return false;
  if(s.modal){
    const hs = history.state;
    if(!hs || hs.gitaModal !== true || !/^\d{1,2}\.\d{1,2}$/.test(s.modal.id)
       || hash !== '#v=' + s.modal.id) return false;
  }
  return true;
}
function readSessionSnapshot(){
  const pathKey = sessionPathKey(), hash = location.hash || '', candidates = [];
  try{
    const hs = history.state && history.state.gitaSession;
    if(validSessionSnapshot(hs, pathKey, hash)) candidates.push(hs);
  }catch(e){}
  try{
    const stored = JSON.parse(sessionStorage.getItem(GITA_SESSION_KEY) || 'null');
    if(validSessionSnapshot(stored, pathKey, hash)) candidates.push(stored);
  }catch(e){}
  candidates.sort((a,b)=>(Number(b.updated)||0)-(Number(a.updated)||0));
  const chosen = candidates[0];
  if(!chosen) return null;
  try{
    const lang = sessionStorage.getItem('gitaLang');
    if(GITA_LANGS.includes(lang) && lang !== chosen.lang) return {...chosen, lang};
  }catch(e){}
  return chosen;
}
function captureQuizSession(){
  const root = document.getElementById('view'), kind = state.view === 'play' ? 'play'
    : state.lrAt && state.lrAt.kind;
  if(!root || !root.querySelector('.lr-qbox') || !Array.isArray(LQ) || !LQ.length
     || !['story','drill','play'].includes(kind)) return null;
  const queue = LQ.map(it=>it && it.qid);
  if(queue.some(id=>typeof id !== 'string' || !id)) return null;
  const index = Number.isInteger(LQi) ? Math.max(0, Math.min(LQi, LQ.length)) : 0;
  const quiz = {seed:kind === 'play' ? null : (Number.isInteger(state.lrAt.seed) ? state.lrAt.seed : null),
    queue, index, misses:Number.isInteger(LQmiss) ? Math.max(0,LQmiss) : 0, ui:null};
  if(index >= LQ.length) return quiz;
  const item = LQ[index], ui = {kind:item.kind};
  if(item.kind === 'pick' && Array.isArray(item.opts)){
    ui.optionOrder = item.opts.map(o=>o && o.oid).filter(x=>typeof x === 'string');
    const wrong = root.querySelector('.lr-opt.wrong');
    if(wrong && wrong.dataset.lrOpt) ui.wrong = wrong.dataset.lrOpt;
  }else if(item.kind === 'order' && Array.isArray(item.chips)){
    ui.chipOrder = Array.from(root.querySelectorAll('.lr-chips .lr-chip2'))
      .map(el=>Number(el.dataset.lrChip)).filter(Number.isInteger);
    ui.picked = Array.isArray(LQpick) ? LQpick.filter(Number.isInteger) : [];
    ui.bad = !!root.querySelector('.lr-fb .bad');
  }else if(item.kind === 'match' && LQpick && typeof LQpick === 'object'){
    ui.match = {left:Number.isInteger(LQpick.left) ? LQpick.left : null,
      right:Number.isInteger(LQpick.right) ? LQpick.right : null,
      done:Object.keys(LQpick.done || {}).filter(k=>/^\d{1,2}\.\d{1,2}$/.test(k))};
  }
  quiz.ui = ui;
  return quiz;
}
function captureSessionSnapshot(){
  const bg = document.getElementById('modalBg'), modalOpen = !!(bg && bg.classList.contains('open'));
  let modal = null;
  if(modalOpen && state.chapter != null && state.theme != null && DATA && DATA[state.chapter]){
    try{
      const s = sutraAt(DATA[state.chapter].themes[state.theme], state.idx).s;
      modal = {id:s.n, mode:state.mode || 'theme', navIdx:Number.isInteger(state.navIdx) ? state.navIdx : 0,
        openDetails:sessionOpenDetails(document.getElementById('modal')),
        openWords:Array.from(document.querySelectorAll('#modal .words.open')).map(el=>el.id).filter(Boolean),
        meaningsHidden:!!document.querySelector('#modal .words.mean-off'),
        menuOpen:!!(document.getElementById('mVerseMenu') && !document.getElementById('mVerseMenu').hasAttribute('hidden')),
        shareOpen:!!(document.getElementById('sharePanel')
          && getComputedStyle(document.getElementById('sharePanel')).display === 'flex'),
        scrollTop:document.getElementById('modal') ? document.getElementById('modal').scrollTop : 0};
    }catch(e){}
  }
  const origin = sessionOrigin(state.origin);
  let shared = null;
  try{ shared = state.shared && state.shared.id ? state.shared.id : null; }catch(e){}
  const snap = {version:1, updated:Date.now(), path:sessionPathKey(), hash:location.hash || '',
    route:viewHash() || '', view:state.view, lang:state.lang,
    section:Number.isInteger(state.section) ? state.section : null,
    chapter:Number.isInteger(state.chapter) ? state.chapter : null,
    theme:Number.isInteger(state.theme) ? state.theme : null,
    idx:Number.isInteger(state.idx) ? state.idx : 0,
    origin, shared,
    query:(document.getElementById('searchInput') && document.getElementById('searchInput').value) || '',
    openDetails:sessionOpenDetails(document.getElementById('view')),
    scrollY:Math.max(0, window.scrollY || window.pageYOffset || 0),
    modal, readerSize:state.readerSize};
  if(state.view === 'learn'){
    snap.learn = {at:state.lrAt || null,
      test:typeof lrTest === 'number' ? lrTest : 0,
      open:typeof lrOpen === 'object' && lrOpen ? lrOpen : {},
      level:typeof LV === 'object' && LV ? LV.level : 'full',
      shown:typeof LV === 'object' && LV ? LV.shown : {}};
    const quiz = captureQuizSession();
    if(quiz) snap.learn.quiz = quiz;
    if(state.lrAt && state.lrAt.kind === 'free' && FP && FP.v)
      snap.learn.free = {ci:FP.ci, ti:FP.ti, verse:FP.v.n,
        deal:Array.isArray(FP.deal) ? FP.deal.slice() : [],
        picked:Array.isArray(FP.picked) ? FP.picked.slice() : []};
  }
  if(state.view === 'play' && typeof PL === 'object' && PL){
    snap.play = {scope:PL.scope, ch:PL.ch, mode:PL.mode, run:PL.run,
      q:PL.q || null, active:!!PL.active};
    const quiz = captureQuizSession();
    if(quiz) snap.play.quiz = quiz;
  }
  return snap;
}
function saveSessionSnapshot(mirrorHistory){
  if(GITA_RESTORING || !state || !state.view) return;
  const snap = captureSessionSnapshot();
  try{ sessionStorage.setItem(GITA_SESSION_KEY, JSON.stringify(snap)); }catch(e){}
  if(mirrorHistory === false) return;
  try{
    const old = history.state && typeof history.state === 'object' ? history.state : {};
    const next = {...old, gitaSession:snap};
    if(snap.modal) next.gitaModal = true;
    else if(next.gitaModal) delete next.gitaModal;
    history.replaceState(next, '', location.href);
  }catch(e){}
}
function scheduleSessionSave(mirrorHistory){
  if(GITA_RESTORING) return;
  GITA_SESSION_MIRROR = GITA_SESSION_MIRROR || mirrorHistory !== false;
  clearTimeout(GITA_SESSION_TIMER);
  GITA_SESSION_TIMER = setTimeout(function(){
    const mirror = GITA_SESSION_MIRROR;
    GITA_SESSION_MIRROR = false;
    saveSessionSnapshot(mirror);
  }, 100);
}
let GITA_RESTORE_OBSERVER = null, GITA_RESTORE_FINISHING = false;
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
           && DATA[ci] && DATA[ci].themes[at.ti]){
    lrDrill(ci, at.ti, thVerses(DATA[ci].themes[at.ti]),
      Number.isInteger(snap.learn.quiz && snap.learn.quiz.seed) ? snap.learn.quiz.seed
        : (Number.isInteger(at.seed) ? at.seed : null));
  }else if(at.kind === 'free' && snap.learn.free){
    const f = snap.learn.free, loc = verseLoc(f.verse);
    if(loc && loc.ci === ci){
      FP.ci = ci; FP.ti = Number.isInteger(f.ti) ? f.ti : -1;
      FP.v = verseAt(loc); FP.order = (FP.v.flow||[]).filter(x=>x.k==='p');
      const valid = a => Array.isArray(a) && a.length === FP.order.length
        && a.every(Number.isInteger) && new Set(a).size === a.length
        && a.every(i=>i >= 0 && i < FP.order.length);
      FP.deal = valid(f.deal) ? f.deal.slice() : FP.order.map((_,i)=>i);
      FP.picked = Array.isArray(f.picked) ? f.picked.filter(i=>Number.isInteger(i)
        && i >= 0 && i < FP.order.length).slice(0,FP.order.length) : [];
      state.view='learn'; state.chapter=ci; state.theme=FP.ti < 0 ? null : FP.ti;
      state.lrAt = {kind:'free', ti:FP.ti}; lrFreePaint();
    }
  }else showLearn(ci);
}
async function finishSessionRestore(){
  if(!GITA_PENDING_RESTORE || GITA_RESTORE_FINISHING) return;
  const snap = GITA_PENDING_RESTORE;
  const root = document.getElementById('view');
  if(!root || !root.children.length || root.querySelector('#bootNote')) return;
  GITA_RESTORE_FINISHING = true;
  try{
    if(snap.view === 'welcome' && snap.shared){
      let shared = verseLoc(snap.shared);
      if(!shared){
        const n = parseInt(String(snap.shared).split('.')[0],10);
        if(n >= 1 && n <= 18) await loadChapter(n);
        shared = verseLoc(snap.shared);
      }
      if(shared){ state.shared = shared; showWelcome(); }
    }
    if(snap.origin) state.origin = sessionOrigin(snap.origin);
    if(snap.view === 'learn'){
      restoreLearnSession(snap);
      if(snap.learn && snap.learn.quiz) restoreQuizSession(snap.learn.quiz);
    }
    if(snap.view === 'play' && snap.play && snap.play.active && snap.play.q){
      PL.scope = snap.play.scope === 'ch' ? 'ch' : 'all';
      PL.ch = Number.isInteger(snap.play.ch) ? snap.play.ch : 0;
      PL.mode = Number.isInteger(snap.play.mode) ? snap.play.mode : 0;
      PL.run = Number.isInteger(snap.play.run) ? snap.play.run : 0;
      PL.q = snap.play.q; PL.active = true;
      plNext(snap.play.q);
      if(snap.play.quiz) restoreQuizSession(snap.play.quiz);
    }
    restoreSessionDetails(document.getElementById('view'), snap.openDetails);
    if(snap.modal){
      let loc = verseLoc(snap.modal.id);
      if(!loc){
        const ch = parseInt(String(snap.modal.id).split('.')[0],10);
        if(ch >= 1 && ch <= 18) await loadChapter(ch);
        loc = verseLoc(snap.modal.id);
      }
      if(loc){
        await loadChapter(loc.ci + 1);
        window.scrollTo({top:Math.max(0, Number(snap.scrollY)||0), behavior:'auto'});
        openModal(loc.ci, loc.ti, loc.si, snap.modal.mode,
          Number.isInteger(snap.modal.navIdx) && snap.modal.navIdx >= 0 ? snap.modal.navIdx : 0,
          null, true);
        restoreModalSession(snap.modal);
      }
    }
  }catch(e){}
  state.keepScroll = false;
  GITA_RESTORING = false;
  GITA_PENDING_RESTORE = null;
  GITA_RESTORE_FINISHING = false;
  if(GITA_RESTORE_OBSERVER){ GITA_RESTORE_OBSERVER.disconnect(); GITA_RESTORE_OBSERVER = null; }
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    if(snap.modal){
      const m = document.getElementById('modal');
      if(m && Number.isFinite(snap.modal.scrollTop)) m.scrollTop = Math.max(0, snap.modal.scrollTop);
    }else window.scrollTo({top:Math.max(0, Number(snap.scrollY)||0), behavior:'auto'});
    saveSessionSnapshot();
  }));
}
function watchSessionRestore(snap){
  GITA_PENDING_RESTORE = snap;
  const root = document.getElementById('view');
  if(!root) return;
  GITA_RESTORE_OBSERVER = new MutationObserver(()=>finishSessionRestore());
  GITA_RESTORE_OBSERVER.observe(root, {childList:true});
}
function T(o){ return o ? (o[state.lang] || o.en || o) : ''; }
/* Phase 2.3: the chapter's traditional colophon — the closing line that names
   the chapter ("... iti <name>o nāma <ordinal>o 'dhyāyaḥ"). It is scripture,
   not our prose, so it carries the Devanagari with its transliteration and
   nothing else: no label, no gloss, no pill. It is deliberately set apart from
   the verse and translation blocks, so it can never read as either. */
function colophonHtml(ch){
  const c = ch && ch.colophon;
  if(!c || !c.deva) return '';
  return `<div class="colophon fade-in" lang="sa">${esc(c.deva)}`
       + (c.iast ? `<span class="col-iast" lang="sa-Latn">${esc(c.iast)}</span>` : '')
       + `</div>`;
}
function L(k){ const u = UI[state.lang] || UI.en; return (u[k] !== undefined) ? u[k] : k; }
function Lof(cur,tot){ const rev=['ne','hi'].includes(state.lang);
  const c = numL(cur), t = numL(tot);   // numL → Devanagari digits in ne/hi
  return rev ? `${t} ${L('of')} ${c}` : `${c} ${L('of')} ${t}`; }
/* Inline stroke icons. Emoji in UI chrome render differently on every OS and
   read as dated; currentColor strokes match the type and follow both themes. */
const ICONS = {
  home:'<svg class="ic" viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg>',
  star:'<svg class="ic" viewBox="0 0 24 24"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
  starF:'<svg class="ic fill" viewBox="0 0 24 24"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
  shuffle:'<svg class="ic" viewBox="0 0 24 24"><path d="M16 3h5v5"/><path d="M21 3 4 20"/><path d="M21 16v5h-5"/><path d="m15 15 6 6"/><path d="m4 4 5 5"/></svg>',
  search:'<svg class="ic" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>',
  moon:'<svg class="ic" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
  sun:'<svg class="ic" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M19.1 4.9l-1.8 1.8M6.7 17.3l-1.8 1.8"/></svg>',
  eye:'<svg class="ic" viewBox="0 0 24 24"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>',
  eyeOff:'<svg class="ic" viewBox="0 0 24 24"><path d="m3 3 18 18"/><path d="M10.6 5.1A11 11 0 0 1 12 5c6.5 0 10 7 10 7a17.7 17.7 0 0 1-3 3.9M6.6 6.6A16.8 16.8 0 0 0 2 12s3.5 7 10 7a10 10 0 0 0 4.4-1"/></svg>',
  play:'<svg class="ic" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="8.5" cy="8.5" r="1.4" fill="currentColor"/><circle cx="15.5" cy="15.5" r="1.4" fill="currentColor"/><circle cx="15.5" cy="8.5" r="1.4" fill="currentColor"/><circle cx="8.5" cy="15.5" r="1.4" fill="currentColor"/></svg>',
  closeX:'<svg class="ic" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>',
  clearX:'<svg class="ic" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>'
};
function applyStatic(){ $('#appTitle').textContent = L('app_title'); $('#appSub').textContent = L('app_sub');
  $('#tagVerses').textContent = L('tag_sub'); $('#appFooter').textContent = L('footer');
  $('#clearBtn').setAttribute('aria-label', L('clear'));
  $('#randLbl').textContent = L('random'); $('#favLbl').textContent = L('favorites');
  $('#homeLbl').textContent = L('home');
  $('#searchInput').placeholder = L('search_ph');
  $('#searchInput').setAttribute('aria-label', L('search_label'));
  const search = document.querySelector('.searchwrap'); if(search) search.setAttribute('aria-label', L('search_label'));
  const langGroup = document.querySelector('#langbar .seg'); if(langGroup) langGroup.setAttribute('aria-label', L('language'));
  const breadcrumb = $('#crumbs'); if(breadcrumb) breadcrumb.setAttribute('aria-label', L('breadcrumb'));
  { const pb = $('#playLbl'); if(pb) pb.textContent = L('play'); }
  /* Phase 3.3 — bottom tab labels (mobile). */
  const th = $('#tabHomeLbl'); if(th) th.textContent = L('home');
  const ts = $('#tabSearchLbl'); if(ts) ts.textContent = L('search_ph').replace('…','').trim() || 'Search';
  const tr = $('#tabRandLbl'); if(tr) tr.textContent = L('random');
  const tp = $('#tabPlayLbl'); if(tp) tp.textContent = L('play');
  const tf = $('#tabFavLbl'); if(tf) tf.textContent = L('favorites');
  searchX(); }
/* Phase 3.3 — keep the bottom tab bar in sync with state.view. Reading
   (read/themes/verses/learn) all map to Home because the tab bar is for
   top-level destinations, not in-chapter sub-views. */
function syncTabs(){
  const bar = $('#tabbar'); if(!bar) return;
  let tab = 'home';
  switch(state.view){
    case 'search': tab = 'search'; break;
    case 'play': tab = 'play'; break;
    case 'favorites': tab = 'fav'; break;
    case 'welcome': case 'sections': case 'chapters': tab = 'home'; break;
    default: /* read/themes/verses/learn = inside content -> Home */ tab = 'home';
  }
  /* Random is a transient action (it jumps straight to a verse), so it
     never stays selected — you land back in reading. */
  bar.querySelectorAll('.tab-btn').forEach(b=>{
    b.setAttribute('aria-selected', String(b.dataset.tab === tab));
  });
}
function tabGoSearch(){
  /* On phones the search input stays in the sticky top toolbar; tapping
     the Search tab just focuses it (the first tap on desktop/tablet
     goes through the toolbar button path instead, which shows a search
     results page from any field value). */
  if(window.matchMedia('(max-width:760px)').matches){
    try{ const si = $('#searchInput'); si.focus(); si.select(); }catch(e){}
    doSearch();
  } else {
    doSearch();
  }
}

/* The parts of a language change that are pure chrome: <html lang>, the three
   segmented buttons, and the static interface strings. Kept apart from setLang()
   because boot needs exactly this — and none of the view re-rendering below — to
   reflect a language restored from storage before the deep link paints. */
function syncLang(l){
  state.lang = l;
  try{ document.documentElement.lang = l; }catch(e){}
  document.querySelectorAll('#langbar .seg .lang-btn').forEach(b=>{
    const selected = b.dataset.lang === l; b.classList.toggle('on', selected);
    b.setAttribute('aria-pressed', String(selected));
  });
  applyStatic();
}
function setLang(l){
  if(!GITA_LANGS.includes(l)) return;   // ignore a stale bookmark or a bad call
  syncLang(l);
  /* Keep a per-tab copy as well as the site-wide default. A service-worker
     refresh in this tab must not pick up a different language chosen in
     another tab. The page's history snapshot is a third, same-entry fallback. */
  try{ sessionStorage.setItem('gitaLang', l); }catch(e){}
  try{ localStorage.setItem('gitaLang', l); }catch(e){}
  // Remember which verse the modal is showing: doSearch()/showFavorites()
  // below null out state.chapter/state.theme while re-rendering the
  // background view, which would otherwise leave the open modal stale.
  const modalOpen = $('#modalBg').classList.contains('open');
  const mCh = state.chapter, mTh = state.theme, mIdx = state.idx;
  if(state.view === 'welcome'){ showWelcome(); }
  else if(state.view === 'sections'){ showSections(); }
  else if(state.view === 'search'){ doSearch(); }
  else if(state.view === 'favorites'){ showFavorites(); }
  /* The learn path renders its own views and holds drill state in module
     vars, so it must NOT fall through to the generic chapter/theme restore
     below: with state.theme set that lands on the chapter view and the
     reader's drill simply disappears mid-question. Re-enter at the path's home — the
     only place that can safely rebuild in the new language, since a
     half-answered question's options were built from the old strings.
     Progress is already saved. */
  else if(state.view === 'learn'){ lrRelang(state.chapter); }
  /* Play rebuilds the question it is showing, in the new language, rather than
     quitting the game: PL.q holds the verse and the option order, and only the
     prompt, the note and the numerals were language-bound. If no question is
     open, fall back to the menu. */
  else if(state.view === 'play'){ if(PL.active && PL.q && PL.mode) plNext(PL.q); else showPlay(); }
  else {
    const ch = state.chapter, th = state.theme;
    if(ch == null){ if(state.section) showChapters(state.section); else showSections(); }
    else { showChapter(ch, th == null ? undefined : th); }
  }
  if(modalOpen && mCh != null && mTh != null){
    state.chapter = mCh; state.theme = mTh; state.idx = mIdx;
    fillModal();
  }
  saveSessionSnapshot();
}
const $ = s => document.querySelector(s);
const crumbs = $('#crumbs'), view = $('#view');

// ---------- global verse index (search / favorites / random) ----------
const VERSES = [];
function buildIndex(){
  VERSES.length = 0;
  (DATA||[]).forEach((ch, ci)=>{ if(!ch||!ch.themes) return;
    ch.themes.forEach((t, ti)=>{
      t.parts.forEach(p=> p.sutras.forEach((s, k)=> VERSES.push({ id:s.n, norm:fmtN(s.n), ci, ti, si:flatIndex(t,p,k) })));
    });
  });
}
function verseLoc(id){ return VERSES.find(v=>v.id===id); }
function verseAt(loc){ const t = DATA[loc.ci].themes[loc.ti]; return sutraAt(t, loc.si).s; }
function normTxt(s){ return String(s||'').normalize('NFD').toLowerCase(); }
function searchExactKey(s){ return normTxt(s).replace(/\s+/g, ''); }
function hasSearchDiacritics(s){ return /[\u0300-\u036f]/.test(normTxt(s)); }
/* Search-only ASCII fallback for the IAST verse field. These are deliberate
   keyboard spellings, not the validator's Sanskrit comparison rules. Marked
   IAST queries stay exact, preserving a/ā, ś/ṣ and t/ṭ. */
function searchFoldKey(s){
  return searchExactKey(s)
    .replace(/r\u0323\u0304/g, 'rri')  // ṝ -> rri
    .replace(/r\u0323/g, 'ri')         // ṛ -> ri
    .replace(/s\u0301/g, 'sh')         // ś -> sh
    .replace(/s\u0323/g, 'sh')         // ṣ -> sh
    .replace(/n\u0323/g, 'n')          // ṇ -> n
    .replace(/a\u0304/g, 'a')          // ā -> a (aa alias below)
    .replace(/i\u0304/g, 'i')          // ī -> i (ee alias below)
    .replace(/u\u0304/g, 'u')          // ū -> u (oo alias below)
    .replace(/a{2,}/g, 'a')            // aa... -> a
    .replace(/e{2,}/g, 'i')            // ee... -> i
    .replace(/o{2,}/g, 'u')            // oo... -> u
    .replace(/c(?!h)/g, 'ch');         // IAST c <-> common ch
}
function prepareSearchQuery(s){
  const exact = searchExactKey(s);
  return { exact, folded: hasSearchDiacritics(s) ? '' : searchFoldKey(s) };
}
function searchTextMatches(exactText, foldedText, query){
  return (!!query.exact && exactText.includes(query.exact)) ||
         (!!query.folded && foldedText.includes(query.folded));
}
function fmtN(n){ const m = String(n).split('.'); return m.length===2 ? (parseInt(m[0],10)+'.'+parseInt(m[1],10)) : String(n); }
function fmtRange(r){ const parts = String(r).split(/[–-]/).map(x=>x.trim()?fmtN(x):x); return (parts.length===2 && parts[0]===parts[1]) ? parts[0] : parts.join('–'); }
function digitNorm(s){ return String(s).replace(/[०-९]/g, d => '0123456789'['०१२३४५६७८९'.indexOf(d)]); }
function devaDigits(s){ return String(s).replace(/[0-9]/g, d => '०१२३४५६७८९'[d]); }
function numL(n){ return (state.lang==='ne'||state.lang==='hi') ? devaDigits(n) : String(n); }
/* Display-only variants of fmtN / fmtRange: identical text, but with Devanagari
   digits in ne/hi. The plain fmtN/fmtRange stay ASCII because VERSES[].norm and
   the search matcher compare against them. */
function fmtNL(n){ return numL(fmtN(n)); }
function fmtRangeL(r){ return numL(fmtRange(r)); }
function chaptersRange(a, b){ return L('range_chapters').replace('{a}', numL(a)).replace('{b}', numL(b)); }
/* Display lines are derived from the canonical verse text. Splitting on the
   danda preserves its order (including the mid-verse speakers in 1.21/1.28);
   IAST `uvāca` marks the speaker segment. */
function verseLines(s){
  if(!s || typeof s.d !== 'string' || typeof s.t !== 'string') return [];
  const ds = s.d.split('।').map(x=>x.trim()).filter(Boolean);
  const ts = s.t.split('।').map(x=>x.trim()).filter(Boolean);
  if(ds.length !== ts.length) return [];
  return ds.map((d,i)=>({k:ts[i].endsWith('uvāca')?'s':'l', d, t:ts[i]}));
}
/* Compute the metre only when it is displayed. The canonical data needs just
   each pāda's syllable count in `flow`; the UI formats this shape in the
   reader's language and uses Devanagari digits in ne/hi. */
function meterShape(s){
  const pads = (s && Array.isArray(s.flow) ? s.flow : []).filter(x=>x.k==='p');
  const total = pads.reduce((sum,x)=>sum + (Number(x.n)||0), 0), n = pads.length;
  if(total === 32) return {name:'anustubh', irr:0, total:32, n:4, per:8};
  if(total === 44) return {name:'trishtubh', irr:0, total:44, n:4, per:11};
  if(total === 22 && n === 2) return {name:'trishtubh', irr:0, total:22, n:2, per:11};
  if(total === 33 && n === 4) return {name:'anustubh', irr:1, total:33, n:4, per:0};
  return {name:'', irr:0, total, n, per:0};
}
function meterText(s){
  if(!s) return '';
  const m = meterShape(s), bits = [];
  if(m.name){
    let nm = L(m.name === 'anustubh' ? 'meter_anustubh' : 'meter_trishtubh');
    if(m.irr) nm += ' (' + L('meter_irregular') + ')';
    bits.push(nm);
  }
  bits.push(L('meter_syllables').replace('{n}', numL(m.total)));
  bits.push(m.per
    ? L('meter_padas_of').replace('{n}', numL(m.n)).replace('{k}', numL(m.per))
    : L('meter_padas').replace('{n}', numL(m.n)));
  return bits.join(' · ');
}
function verseSearchText(v){
  return v.n + ' ' + fmtN(v.n) + ' ' + v.d + ' ' + v.t + ' ' + v.lits.en + ' ' + v.lits.ne + ' ' + v.lits.hi
    + ' ' + v.paras.en + ' ' + v.paras.ne + ' ' + v.paras.hi + ' ' + T(v.lits);
}
const VERSE_TEXT = [], VERSE_FOLDED_TEXT = [];
function buildVerseText(){
  VERSE_TEXT.length = 0;
  VERSE_FOLDED_TEXT.length = 0;
  (DATA||[]).forEach(ch=>{
    if(!ch||!ch.themes) return;
    ch.themes.forEach(t=> t.parts.forEach(p=> p.sutras.forEach(s=>{
      const text = verseSearchText(s);
      VERSE_TEXT.push(searchExactKey(text));
      // Keep approximate folds out of English, Nepali, Hindi and Devanagari.
      VERSE_FOLDED_TEXT.push(searchFoldKey(s.t));
    })));
  });
}
function assembleData(){
  DATA = [];
  for(var n=1;n<=18;n++) DATA.push(GITA_CH[n] || null);
  buildIndex(); buildVerseText();
}
function allChReady(){ for(var n=1;n<=18;n++) if(!GITA_CH[n]||!GITA_CH[n].themes) return false; return true; }

// ---------- search ----------
let searchTimer = null;
function onSearchInput(v){
  clearTimeout(searchTimer); searchTimer = setTimeout(doSearch, 220); searchX();
}
/* the in-field ✕ exists only while there is text to clear — the modern
   pattern; a standing "Clear" button was dead chrome on an empty field */
function searchX(){ const f = document.querySelector('.sw-field');
  if(f) f.classList.toggle('has-x', ($('#searchInput').value || '').length > 0); }
function doSearch(){
  if(!allChReady()){ loadAllChapters().then(doSearch); return; }
  const q = ($('#searchInput').value || '').trim();
  if(!q){ clearSearch(); return; }
  SRCH_HITS = [];
  rememberOrigin();
  state.view = 'search'; state.chapter = null; state.theme = null; persistView(); renderCrumbs();
  const nq = prepareSearchQuery(q);
  /* Accept whatever separator the reader's keyboard gives. On a Devanagari
     layout the danda । sits where the full stop is, so १।१ is the natural way to
     type 1.1; also allow : - / , the double danda, and stray surrounding dandas. */
  const num = digitNorm(q).replace(/^[\s।॥]+|[\s।॥]+$/g, '')
                          .match(/^(\d{1,2})[.।॥:\-\/,\s]+(\d{1,2})$/);
  let hits;
  if(num){
    const target = parseInt(num[1],10) + '.' + parseInt(num[2],10);
    hits = VERSES.filter(loc => loc.norm === target);
    if(hits.length === 0){
      const c = parseInt(num[1],10), v = parseInt(num[2],10);
      let msg = '';
      if(c >= 1 && c <= 18){
        const cnt = DATA[c-1].verses;
        if(v < 1 || v > cnt) msg = L('oob_verse').replace('{ch}', numL(c)).replace('{n}', numL(cnt));
      } else {
        msg = L('oob_chapter');
      }
      if(msg){
        view.innerHTML = `<div class="res-head fade-in" role="heading" aria-level="2">${esc(L('search_results'))}</div>
          <div class="res-count fade-in">${esc(resultCountLabel(0))}</div>
          <div class="view-sub fade-in">${esc(msg)}</div>`;
        announceView();
        return;
      }
    }
  } else {
    /* Free text. The index holds verse numbers as ASCII ("1.1"), so a query in
       Devanagari digits — १, १७ — has to be converted too, or typing १ finds
       nothing while 1 finds the whole chapter. Try both forms. */
    const nqd = prepareSearchQuery(digitNorm(q).replace(/[।॥]/g, '.'));
    hits = [];
    VERSES.forEach((loc, i)=>{
      const t = VERSE_TEXT[i], folded = VERSE_FOLDED_TEXT[i];
      if(searchTextMatches(t, folded, nq) ||
         (nqd.exact !== nq.exact && searchTextMatches(t, folded, nqd))) hits.push(loc);
    });
  }
  if(hits.length === 0){
    view.innerHTML = `<div class="res-head fade-in" role="heading" aria-level="2">${esc(L('search_results'))}</div>
      <div class="res-count fade-in">${esc(resultCountLabel(0))}</div>
      <div class="view-sub fade-in">${esc(L('no_results'))}</div>`;
    announceView();
    return;
  }
  SRCH_HITS = hits;
  view.innerHTML = `<div class="res-head fade-in" role="heading" aria-level="2">${esc(L('search_results'))}</div>
    <div class="res-count fade-in">${esc(resultCountLabel(hits.length))}</div>
    <div class="grid verses fade-in">${hits.map((loc,i)=>{
      const ch = DATA[loc.ci], v = verseAt(loc);
      const th = ch.themes[loc.ti]; const part = sutraAt(th, loc.si).part;
      const pi = th.parts.indexOf(part);
      return `<div class="mini" role="button" tabindex="0" onclick="openModal(${loc.ci},${loc.ti},${loc.si},'search',${i},this)">
        <div class="vnum">${esc(L('verse'))} ${esc(fmtNL(v.n))}</div>
        <div class="m-topic"><span class="mt-lab">${esc(L('verse_topic'))}:</span> ${esc(T(part.titles))}</div>
        <div class="padas" lang="sa">${padaBlockDeva(v)}</div>
        <div class="vhint">${esc(T(v.paras))}</div>
      </div>`;}).join('')}</div>`;
  announceView();
}
function clearSearch(){
  $('#searchInput').value = '';
  searchX();
  goToOrigin();
}

// ---------- favorites (localStorage with in-memory fallback) ----------
let FAV = [], FAVNOTE = {};
// ---------- dark mode ----------
// The <head> script has already applied the theme. These functions handle the
// toggle, keep the button label and the browser chrome colour in step, and
// follow the phone's setting until the reader overrides it.
function themeIsDark(){ return document.documentElement.getAttribute('data-theme') === 'dark'; }
function paintTheme(){
  const dark = themeIsDark();
  const icon = $('#themeIcon'); if(icon) icon.innerHTML = dark ? ICONS.sun : ICONS.moon;
  const btn = $('#themeBtn');
  if(btn) btn.setAttribute('aria-label', dark ? L('theme_light') : L('theme_dark'));
  // colour the phone's status bar / address bar to match
  const mc = document.getElementById('themeColor');
  if(mc) mc.setAttribute('content', dark ? '#0E2A24' : '#1A5648');
}
function setTheme(dark, remember){
  if(dark) document.documentElement.setAttribute('data-theme','dark');
  else document.documentElement.removeAttribute('data-theme');
  if(remember){ try{ localStorage.setItem('gitaTheme', dark ? 'dark' : 'light'); }catch(e){} }
  paintTheme();
}
function toggleTheme(){ setTheme(!themeIsDark(), true); }
// If the reader has never chosen, keep following the phone as it changes
// (e.g. an automatic switch at sunset).
try{
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  const onSys = e => { let saved=null; try{ saved=localStorage.getItem('gitaTheme'); }catch(_){}
                       if(saved === null) setTheme(e.matches, false); };
  if(mq.addEventListener) mq.addEventListener('change', onSys);
  else if(mq.addListener) mq.addListener(onSys);
}catch(e){}

/* JSON.parse succeeding does NOT mean we got the shape we want: a stored
   'null', '5' or '{}' parses fine and then explodes on the first .indexOf /
   .includes — and FAV.includes() runs on every verse modal, so one bad write
   (a sync bug, a shared-device mishap, a hand-edited devtools value) would
   brick the app on every verse with no way back except clearing storage.
   Validate the TYPE, not just the parse, and fall back to empty. */
function favNoteLoad(){
  try{
    const o = JSON.parse(localStorage.getItem('gitaFavNotes') || '{}');
    if(!o || typeof o !== 'object' || Array.isArray(o)) return {};
    const out = {};
    for(const k in o) if(typeof o[k] === 'string') out[k] = o[k];
    return out;
  }catch(e){ return {}; }
}
function favNoteSave(){ try{ localStorage.setItem('gitaFavNotes', JSON.stringify(FAVNOTE)); }catch(e){} }
function favLoad(){
  try{
    const a = JSON.parse(localStorage.getItem('gitaFavs') || '[]');
    /* keep only well-formed verse ids, so a corrupt entry cannot poison the
       favourites list or render a broken card */
    return Array.isArray(a) ? a.filter(x => typeof x === 'string' && /^\d{1,2}\.\d{1,2}$/.test(x)) : [];
  }catch(e){ return []; }
}
FAV = favLoad(); FAVNOTE = favNoteLoad();
function favSave(){ try{ localStorage.setItem('gitaFavs', JSON.stringify(FAV)); }catch(e){} }
function toggleFav(id){
  const i = FAV.indexOf(id);
  if(i >= 0) FAV.splice(i,1); else FAV.push(id);
  favSave();
  const b = document.getElementById('favBtn');
  if(b){ const on = FAV.includes(id); b.innerHTML = (on ? ICONS.starF : ICONS.star) + esc(L(on ? 'saved_verse' : 'save_verse')); b.classList.toggle('saved', on); b.setAttribute('aria-pressed', String(on)); }
  if(state.view === 'favorites') showFavorites();
}
/* Search and Favorites are "detours": they replace the main view but the reader
   should still be able to get back to whatever they were reading. Before either
   takes over, remember the browsing position so renderCrumbs() can offer it as a
   real trail. Only recorded when leaving an actual browsing view, so repeatedly
   tapping Favorites doesn't overwrite the origin with itself. */
function rememberOrigin(){
  if(['welcome','sections','chapters','chapter'].includes(state.view)){
    state.origin = { view: state.view, section: state.section,
                     chapter: state.chapter, theme: state.theme };
  }
}
function goToOrigin(){
  const o = state.origin;
  if(!o){ showSections(); return; }
  $('#searchInput').value = '';
  if(o.view === 'welcome') showWelcome();
  else if(o.view === 'sections') showSections();
  else if(o.view === 'chapter' && o.chapter != null)
    showChapter(o.chapter, o.theme == null ? undefined : o.theme);
  else if(o.section != null) showChapters(o.section);
  else showSections();
}
function showFavorites(){
  if(!allChReady()){ loadAllChapters().then(showFavorites); return; }
  rememberOrigin();
  state.view = 'favorites'; state.chapter = null; state.theme = null; persistView(); renderCrumbs();
  const saved = FAV.map(verseLoc).filter(Boolean);
  FAV_LIST = saved;
  if(saved.length === 0){
    view.innerHTML = `<div class="res-head fade-in" role="heading" aria-level="2">${esc(L('favorites'))}</div>
      <div class="view-sub fade-in">${esc(L('no_favorites'))}</div>`;
    announceView();
    return;
  }
  view.innerHTML = `<div class="res-head fade-in" role="heading" aria-level="2">${esc(L('favorites'))}</div>
    <div class="res-count fade-in">${esc(resultCountLabel(saved.length))}</div>
    ${saved.map((loc,i)=>{
      const ch = DATA[loc.ci], v = verseAt(loc);
      const note = FAVNOTE[v.n] || '';
      return `<div class="res-card" onclick="openModal(${loc.ci},${loc.ti},${loc.si},'fav',${i},this.querySelector('.res-open'))">
        <button type="button" class="sr-only focusable res-open" aria-label="${esc(L('open_verse'))} ${esc(fmtNL(v.n))}"
          onclick="event.stopPropagation();openModal(${loc.ci},${loc.ti},${loc.si},'fav',${i},this)"></button>
        <div class="res-top"><span class="res-num">${esc(fmtNL(v.n))}</span><span class="res-title">${esc(T(ch.names))}</span>
        <span class="fav-tools" onclick="event.stopPropagation()">
          <button class="fav-move" onclick="moveFav(${i},-1)" ${i===0?'disabled':''} aria-label="${esc(L('fav_move_up'))}" title="${esc(L('fav_move_up'))}">${L('fav_up')}</button>
          <button class="fav-move" onclick="moveFav(${i},1)" ${i===saved.length-1?'disabled':''} aria-label="${esc(L('fav_move_down'))}" title="${esc(L('fav_move_down'))}">${L('fav_down')}</button>
          <button class="res-remove" onclick="removeFav('${esc(v.n)}')">${esc(L('remove_fav'))}</button>
        </span></div>
        <div class="res-deva" lang="sa">${padaBlockDeva(v)}</div>
        <div class="res-lit">${esc(T(v.lits))}</div>
        <div class="fav-note" onclick="event.stopPropagation()">
          <label for="fav-note-${esc(v.n)}">${esc(L('fav_note'))}</label>
          <textarea id="fav-note-${esc(v.n)}" rows="1" placeholder="${esc(L('fav_note_ph'))}"
            oninput="this.style.height='auto';this.style.height=this.scrollHeight+'px'"
            onchange="setFavNote('${esc(v.n)}', this.value)">${esc(note)}</textarea>
        </div>
      </div>`;}).join('')}`;
  // grow each note box to fit what is already written
  view.querySelectorAll('.fav-note textarea').forEach(t=>{
    if(t.value){ t.style.height='auto'; t.style.height=t.scrollHeight+'px'; }
  });
  announceView();
}
function removeFav(id){
  const i = FAV.indexOf(id);
  if(i>=0){ FAV.splice(i,1); favSave(); }
  if(FAVNOTE[id]){ delete FAVNOTE[id]; favNoteSave(); }
  showFavorites();
}
/* Favourites are a personal collection, so the reader orders them and can say
   why a verse matters. Both are stored beside the list itself. */
function moveFav(i, d){
  const j = i + d;
  if(j < 0 || j >= FAV.length) return;
  [FAV[i], FAV[j]] = [FAV[j], FAV[i]];
  favSave(); showFavorites();
}
function setFavNote(id, text){
  text = (text||'').trim();
  if(text) FAVNOTE[id] = text; else delete FAVNOTE[id];
  favNoteSave();
}

// ---------- random verse ----------
function randomVerse(){
  if(!allChReady()){ loadAllChapters().then(randomVerse); return; }
  const v = VERSES[Math.floor(Math.random()*VERSES.length)];
  openModal(v.ci, v.ti, v.si, 'random');
}

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function vCount(t){ return t.parts.reduce((a,p)=>a+p.sutras.length,0); }

function crumb(label, action, isLast){
  const b = document.createElement('button'); b.textContent = label;
  // Long chapter names are truncated with CSS; keep the full text available as a
  // tooltip on hover and to screen readers. Truncation is visual only.
  b.title = label; b.setAttribute('aria-label', label);
  if(isLast){ b.className='cur'; b.disabled=true; } else b.onclick = action;
  return b;
}
/* On phones the header scrolls away, so a deeper view would otherwise open
   mid-page. Jump to the top whenever we actually move to a different view. */
let LAST_VIEW_SIG = null;
function scrollViewTop(){
  const sig = [state.view, state.section, state.chapter, state.theme].join('|');
  if(sig === LAST_VIEW_SIG) return;
  LAST_VIEW_SIG = sig;
  announceView();
  if(state.keepScroll) return;
  try{ window.scrollTo({top:0, behavior:'auto'}); }catch(e){ window.scrollTo(0,0); }
}
/* Speak the new view to screen readers. This app never navigates, so the only
   signal a non-sighted reader gets is this live region — the same signature
   scrollViewTop already dedupes on, so it fires exactly once per real change
   and stays silent when a re-render lands on the same place. */
function resultCountLabel(n){
  const count = numL(n);
  return `${count} ${L(n === 1 ? 'result' : 'results')}`;
}
function announceView(){
  const el = document.getElementById('srStatus');
  if(!el) return;
  let msg = '';
  try{
    const ch = (state.chapter != null && DATA[state.chapter]) ? DATA[state.chapter] : null;
    if(state.view === 'welcome')        msg = L('welcome_title');
    else if(state.view === 'search')
      msg = `${L('search_results')} · ${resultCountLabel(SRCH_HITS.length)}`;
    else if(state.view === 'favorites')
      msg = `${L('favorites')} · ${resultCountLabel(FAV_LIST.length)}`;
    else if(state.view === 'chapter' && ch && state.theme != null)
      msg = `${L('chapter')} ${numL(ch.num)} · ${T(ch.themes[state.theme].titles)}`;
    else if(ch) msg = `${L('chapter')} ${numL(ch.num)} · ${T(ch.names)}`;
    else if(state.section) msg = L('sections_title');
  }catch(e){}
  if(msg) el.textContent = msg;
  syncTabs();
}
/* Search and Favorites are "detours" off the browsing hierarchy. Rather than a
   breadcrumb trail, they show a single back button naming the page the reader came
   from — the same control and wording as the app's "← Back to themes" / "← Back to
   chapters" buttons, so Favorites is not a special case. Nothing becomes
   unreachable: that destination carries its own back button, so the hierarchy is
   walked one level at a time. */
/* These lists run four to five screens on a phone, and the only way back used to
   be the crumb at the very top. backFoot() repeats that one button at the end —
   same destination, same wording, so there is nothing new to learn. */
function backFoot(onclick, label){
  return `<div class="back-foot"><button class="back-top" onclick="${onclick}">${esc(label)}</button></div>`;
}

/* Theme ranges arrive padded (2.01-2.03); humans read 2.1-2.3 (PROJECT.md).
   The builder has _drange() for the static pages; the app needs it at runtime. */
function _drangeJS(r){
  r = String(r||'');
  r = r.replace(/(\d+)\.0*(\d+)\s*[–-]\s*(\d+)\.0*(\d+)/g, function(m,a,b,c,d){
    const x = a+'.'+parseInt(b,10), y = c+'.'+parseInt(d,10);
    return x===y ? x : x+'–'+y;
  });
  return r.replace(/(\d+)\.0*(\d+)/g, function(m,a,b){ return a+'.'+parseInt(b,10); });
}

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
  rememberOrigin();
  state.view='learn'; state.chapter=ci; persistView(); state.lrAt = null;
  state.section = state.section || Math.ceil(DATA[ci].num/6);
  state.theme=null; renderCrumbs();
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
    ${wayCrumbs([[L('sections_title'),'showSections()'],
      [wayName(Math.ceil(ch.num/6)), `showChapters(${Math.ceil(ch.num/6)})`],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, null]])}
    ${chTitle(ch)}
    ${modeSwitch(ci)}
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
    </div>` + backFoot(`showChapters(${state.section||0})`, L('back_chapters'));
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
  state.view='learn'; state.chapter=ci; persistView(); state.theme=null;
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
    lrRun(ci, items, fmt(L('learn_step'),{a:numL(k+1),b:numL(n)}),
      nxt === undefined ? ()=>lrStoryDone(ci) : ()=>lrStory(ci, nxt));
  });
}

var lrTest = 0, lrOpen = {};
function lrStoryRead(ci, ch, th, k, n){
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'),'showSections()'],
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
    </div>` + backFoot(`showChapter(${ci})`, L('back_chapter_one'));
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
  state.view='learn'; state.chapter=ci; persistView(); state.theme=ti;
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
    ${wayCrumbs([[L('sections_title'),'showSections()'],
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
    </div>` + backFoot(`showChapter(${ci})`, L('back_chapter_one'));
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
  state.lrAt = {kind:'drill', ti:ti, seed:quizSeed}; persistView();
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
    /* Options are WHOLE VERSES, not opening lines — a first pāda is not a
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
        <button class="lr-ghost" onclick="showChapter(${ci})">${esc(L('back_chapter_one'))}</button>
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
  state.view='learn'; state.chapter=ci; persistView(); state.theme=ti;
  state.lrAt = {kind:'free', ti:ti};
  FP.ci = ci; FP.ti = ti;
  lrFreePick();
}
function lrFreeCh(ci){
  state.view='learn'; state.chapter=ci; persistView(); state.theme=null;
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
    ${wayCrumbs([[L('sections_title'),'showSections()'],
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
        <button class="lr-ghost" onclick="showChapter(${FP.ci})">${esc(L('learn_done_free'))}</button>
      </div>
    </div>` + backFoot(`showChapter(${FP.ci})`, L('back_chapter_one'));
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
var PL = {scope:'all', ch:0, mode:0, run:0, q:null, active:false};

function showPlay(){
  if(!allChReady()){ loadAllChapters().then(showPlay); return; }
  PL.active = false;
  rememberOrigin();
  state.view='play'; state.chapter=null; state.theme=null; persistView(); renderCrumbs();
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
        ${[[1,'play_m1','play_m1_d'],[2,'play_m2','play_m2_d'],[3,'play_m3','play_m3_d']].map(([m,tk,d])=>`
          <button class="pl-mode" onclick="plStart(${m})">
            <span class="n">${numL(m)}</span>
            <span class="b"><b>${esc(L(tk))}</b><span>${esc(L(d))}</span></span>
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
               : lrShuffle([s].concat(lrSample(distract, 3)));
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
                : lrShuffle([nxt].concat(lrSample(distract, 3)));
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
function lrPaint(resumeUi){
  if(LQi >= LQ.length) return typeof LQdone === 'function' ? LQdone() : showLearn(LQci);
  const it = LQ[LQi];
  if(!resumeUi) LQpick = [];
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
  /* Re-shuffle options on every fresh paint. Restore paints use the validated
     option/chip order from this tab's snapshot instead. */
  if(it.kind === 'pick' && it._seen && !resumeUi) it.opts = lrShuffle(it.opts);
  it._seen = 1;
  let body;
  if(it.kind === 'pick'){
    body = `<div class="lr-ask">${it.ask}</div>
       <div class="lr-opts">${it.opts.map((o,i)=>`
         <button class="lr-opt" data-lr-opt="${esc(o.oid||'')}" onclick="lrPick(${i})">
           <span class="onum">${numL(i+1)}</span>
           <span class="ol${o.deva?' dv':''}"${o.deva?' lang="sa"':''}>${o.deva?o.label:esc(o.label)}</span>
           ${o.iast?`<span class="giast" lang="sa-Latn">${esc(o.iast)}</span>`:''}
           ${o.sub?`<span class="os">${esc(o.sub)}</span>`:''}
         </button>`).join('')}</div>`;
  }else if(it.kind === 'match'){
    if(!resumeUi) LQpick = {left:null, right:null, done:{}};
    body = `<div class="lr-ask">${it.ask}</div>
      <div class="lr-match">
        <div class="lr-mcol nums">${it.left.map((o,i)=>`
          <button class="lr-mbtn num" data-n="${esc(o.n)}" onclick="lrMpick('left',${i})">${esc(o.lab)}</button>`).join('')}</div>
        <div class="lr-mcol vs">${it.right.map((o,i)=>`
          <button class="lr-mbtn vs" data-n="${esc(o.n)}" onclick="lrMpick('right',${i})">
            <span class="ol dv" lang="sa">${o.lab}</span>
            ${o.iast?`<span class="giast" lang="sa-Latn">${esc(o.iast)}</span>`:''}
          </button>`).join('')}</div>
      </div>`;
  }else{
    let chips = lrShuffle(it.chips);
    if(resumeUi && Array.isArray(resumeUi.chipOrder)){
      const byId = new Map(it.chips.map(c=>[c.id,c]));
      const ordered = resumeUi.chipOrder.map(id=>byId.get(id)).filter(Boolean);
      if(ordered.length === it.chips.length) chips = ordered;
    }
    body = `<div class="lr-ask">${it.ask}</div>
       <div class="lr-slots" id="lrSlots"></div>
       <div class="lr-chips">${chips.map(c=>`
         <button class="lr-chip2${c.deva?' dv':''}" data-lr-chip="${c.id}"${c.deva?' lang="sa"':''} onclick="lrChip(this,${c.id})"><span class="lr-t">${esc(c.label)}</span>${c.iast?`<span class="giast" lang="sa-Latn">${esc(c.iast)}</span>`:''}</button>`).join('')}</div>`;
  }
  view.innerHTML = `<div class="lrn fade-in">${head}
    <div class="lr-qbox">${body}<div class="lr-fb" id="lrFb"></div></div>
    </div>` + (LQback
      ? backFoot(LQback.fn, L(LQback.label))
      : backFoot(`showChapter(${LQci})`, L('back_chapter_one')));
  if(resumeUi) restoreQuizUi(it, resumeUi);
  scrollViewTop();
}
function restoreQuizUi(it, ui){
  const root = document.getElementById('view');
  if(!root || !ui) return;
  if(it.kind === 'pick' && ui.wrong && Array.isArray(it.opts)){
    const wrong = it.opts.findIndex(o=>o.oid === ui.wrong);
    if(wrong >= 0){
      const buttons = root.querySelectorAll('.lr-opt');
      buttons.forEach((b,i)=>{
        b.disabled = true;
        if(it.opts[i].ok) b.classList.add('right');
        else if(i === wrong) b.classList.add('wrong');
      });
      const fb = root.querySelector('#lrFb');
      if(fb) fb.innerHTML = (it.note?`<div class="nt">${it.note}</div>`:'')
        + `<button class="lr-cta" onclick="LQi++;lrPaint()">${esc(L('learn_retry'))}</button>`;
    }
  }else if(it.kind === 'order' && Array.isArray(LQpick)){
    const slots = root.querySelector('#lrSlots');
    LQpick.forEach((id,k)=>{
      const chip = it.chips.find(c=>c.id === id);
      if(!chip || !slots) return;
      const button = root.querySelector(`[data-lr-chip="${id}"]`);
      if(button){ button.disabled = true; button.classList.add('used'); }
      const slot = document.createElement('span');
      slot.className = 'lr-slot' + (chip.deva ? ' dv' : '');
      if(chip.deva) slot.lang = 'sa';
      slot.textContent = numL(k+1) + '. ' + chip.label;
      if(chip.iast){
        const iast = document.createElement('span');
        iast.className = 'giast'; iast.lang = 'sa-Latn'; iast.textContent = chip.iast;
        slot.appendChild(iast);
      }
      slots.appendChild(slot);
    });
    if(ui.bad){
      const fb = root.querySelector('#lrFb'), want = it.answer[LQpick.length];
      const next = it.chips.find(c=>c.id === want);
      if(fb) fb.innerHTML = `<div class="bad">${esc(L('learn_nextis'))} <b>${esc(next?next.label:'')}</b></div>`;
    }
  }else if(it.kind === 'match' && ui.match){
    const left = root.querySelectorAll('.lr-mbtn.num'), right = root.querySelectorAll('.lr-mbtn.vs');
    const done = new Set(Array.isArray(ui.match.done) ? ui.match.done : []);
    root.querySelectorAll('.lr-mbtn').forEach(b=>{
      if(done.has(b.dataset.n)){ b.disabled = true; b.classList.add('right'); }
    });
    if(Number.isInteger(ui.match.left) && left[ui.match.left]) left[ui.match.left].classList.add('on');
    if(Number.isInteger(ui.match.right) && right[ui.match.right]) right[ui.match.right].classList.add('on');
  }
}
function restoreQuizSession(saved){
  if(!saved || !Array.isArray(saved.queue) || !saved.queue.length || saved.queue.length > 500
     || !Array.isArray(LQ) || !LQ.length) return false;
  const base = new Map();
  LQ.forEach(it=>{ if(it && typeof it.qid === 'string') base.set(it.qid,it); });
  if(!base.size || saved.queue.some(id=>typeof id !== 'string' || !base.has(id))) return false;
  const counts = new Map();
  LQ.forEach(it=>counts.set(it.qid,(counts.get(it.qid)||0)+1));
  saved.queue.forEach(id=>counts.set(id,(counts.get(id)||0)-1));
  const diffs = Array.from(counts.values());
  const extra = diffs.reduce((n,x)=>n + Math.max(0,-x),0);
  if(diffs.some(n=>n>0) || saved.queue.length !== LQ.length + extra
     || !Number.isInteger(saved.misses) || saved.misses < extra) return false;
  const queue = saved.queue.map(id=>base.get(id));
  if(queue.length !== saved.queue.length) return false;
  LQ = queue;
  LQi = Number.isInteger(saved.index) ? Math.max(0,Math.min(saved.index,LQ.length)) : 0;
  LQmiss = Number.isInteger(saved.misses) ? Math.max(0,Math.min(saved.misses,1000)) : 0;
  if(LQi >= LQ.length){ LQpick = []; lrPaint(); return true; }
  const it = LQ[LQi], ui = saved.ui && saved.ui.kind === it.kind ? saved.ui : null;
  if(it.kind === 'pick'){
    if(ui && Array.isArray(ui.optionOrder)){
      const remaining = it.opts.slice(), ordered = [];
      ui.optionOrder.forEach(id=>{
        const k = remaining.findIndex(o=>typeof o.oid === 'string' && o.oid === id);
        if(k >= 0) ordered.push(remaining.splice(k,1)[0]);
      });
      it.opts = ordered.concat(remaining);
    }
    LQpick = [];
  }else if(it.kind === 'order'){
    const valid = new Set(it.answer);
    LQpick = ui && Array.isArray(ui.picked)
      ? ui.picked.filter((id,k,a)=>Number.isInteger(id)&&valid.has(id)&&a.indexOf(id)===k).slice(0,it.answer.length) : [];
  }else if(it.kind === 'match'){
    const m = ui && ui.match || {};
    LQpick = {left:Number.isInteger(m.left)&&m.left>=0&&m.left<it.left.length ? m.left : null,
      right:Number.isInteger(m.right)&&m.right>=0&&m.right<it.right.length ? m.right : null, done:{}};
    (Array.isArray(m.done)?m.done:[]).forEach(id=>{
      if(it.left.some(o=>o.n===id)&&it.right.some(o=>o.n===id)) LQpick.done[id]=1;
    });
  }else LQpick = [];
  lrPaint(ui);
  return true;
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
function lrMpick(side, i){
  const it = LQ[LQi];
  if(!LQpick || typeof LQpick !== 'object' || Array.isArray(LQpick)) LQpick = {left:null, done:{}};
  const col = side === 'left' ? it.left : it.right;
  const o = col[i];
  if(LQpick.done[o.n]) return;
  const btns = document.querySelectorAll(side==='left' ? '.lr-mbtn.num' : '.lr-mbtn.vs');
  btns.forEach(b=>b.classList.remove('on'));
  LQpick[side] = i;
  if(btns[i]) btns[i].classList.add('on');
  if(LQpick.left==null || LQpick.right==null) return;
  const a = it.left[LQpick.left], b = it.right[LQpick.right];
  const lb = document.querySelectorAll('.lr-mbtn.num')[LQpick.left];
  const rb = document.querySelectorAll('.lr-mbtn.vs')[LQpick.right];
  const fb = document.getElementById('lrFb');
  if(a.n === b.n){
    LQpick.done[a.n] = 1;
    if(lb){ lb.classList.add('right'); lb.disabled = true; lb.classList.remove('on'); }
    if(rb){ rb.classList.add('right'); rb.disabled = true; rb.classList.remove('on'); }
    LQpick.left = LQpick.right = null;
    if(Object.keys(LQpick.done).length >= it.left.length){
      if(fb) fb.innerHTML = `<div class="good">${esc(L('learn_yes'))}</div>`;
      LQi++; setTimeout(lrPaint, 700);
    }
  }else{
    if(lb) lb.classList.add('shake');
    if(rb) rb.classList.add('shake');
    setTimeout(()=>{
      if(lb){ lb.classList.remove('shake','on'); }
      if(rb){ rb.classList.remove('shake','on'); }
    }, 380);
    LQpick.left = LQpick.right = null;
    if(fb) fb.innerHTML = '';
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
    const chp = it.chips.find(c=>c.id===id);
    const iast = (chp && chp.iast) ? `<span class="giast" lang="sa-Latn">${esc(chp.iast)}</span>` : '';
    document.getElementById('lrSlots').insertAdjacentHTML('beforeend',
      `<span class="lr-slot${dv}"${dv?' lang="sa"':''}>${numL(LQpick.length)}. ${esc(chp?chp.label:el.textContent.trim())}${iast}</span>`);
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

function renderCrumbs(){
  scrollViewTop();
  crumbs.innerHTML='';
  if(state.view!=='search' && state.view!=='favorites') return;
  const o = state.origin || { view:'welcome' };
  const clear = fn => { $('#searchInput').value=''; fn(); };

  let label, action;
  if(o.view === 'welcome'){
    label = L('home_plain');            action = ()=>clear(showWelcome);
  } else if(o.chapter != null && o.theme != null){
    // Name each level as what it is — "Theme 1 · The Royal Secret", not just the
    // title, which can echo the chapter name (ch.9's theme 1 is "राजगुह्य", the
    // chapter "राजविद्या राजगुह्य योग"). Matches the verse modal's own wording.
    const ch = DATA[o.chapter];
    label = `${L('theme_sg')} ${numL(o.theme+1)} · ${T(ch.themes[o.theme].titles)}`;
    action = ()=>clear(()=>showChapter(o.chapter, o.theme));
  } else if(o.chapter != null){
    const ch = DATA[o.chapter];
    label = `${L('chapter')} ${numL(ch.num)} · ${T(ch.names)}`;
    action = ()=>clear(()=>showChapter(o.chapter));
  } else if(o.section != null){
    label = L('tab_'+['','karma','bhakti','jnana'][o.section]);
    action = ()=>clear(()=>showChapters(o.section));
  } else {
    label = L('sections_title');        action = ()=>clear(showSections);
  }

  const b = document.createElement('button');
  b.className = 'back-top';
  b.textContent = L('back_to_x').replace('{x}', label);
  b.title = b.textContent; b.setAttribute('aria-label', b.textContent);
  b.onclick = action;
  crumbs.appendChild(b);
}

function showChapters(section){
  const _from = (section-1)*6+1, _to = Math.min(18, section*6);
  const _need = [];
  for(let n=_from;n<=_to;n++) if(!GITA_CH[n]||!GITA_CH[n].themes) _need.push(n);
  if(_need.length){ Promise.all(_need.map(loadChapter)).then(()=>showChapters(section)).catch(function(){}); return; }
  /* The Three Ways is the door; there is no flat all-18 list. Every chapter
     list lives inside its way, so the niṣṭhā framing is never skipped. */
  state.view='chapters'; state.section=section; state.chapter=null; state.theme=null; persistView(); renderCrumbs();
  const list = DATA.filter(ch => ch && ch.num >= (section-1)*6+1 && ch.num <= section*6);
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'), 'showSections()'], [wayName(section), null]])}
    <div class="grid chapters fade-in">
      ${list.map(ch=>{
        const ci = DATA.indexOf(ch);
        return `<div class="card" role="button" tabindex="0" onclick="showChapter(${ci})">
          <span class="chip">${L('chapter')} ${numL(ch.num)}</span>
          <h3>${esc(T(ch.names))}</h3>
          <p>${esc(T(ch.subs))}</p>
          <div class="meta">${numL(ch.verses)} ${L('verses')}</div>
        </div>`;}).join('')}
    </div>` + backFoot('showSections()', L('back_ways'));
}

function daySpec(){
  const d = new Date();
  const dayNum = d.getFullYear()*10000 + (d.getMonth()+1)*100 + d.getDate();
  let total = 0; for(const n of CH_LEN) total += n;
  let k = dayNum % total, acc = 0;
  for(let i=0;i<CH_LEN.length;i++){
    if(k < acc + CH_LEN[i]){
      const v = k - acc + 1;
      return {ch:i+1, id:(i+1)+'.'+String(v).padStart(2,'0')};
    }
    acc += CH_LEN[i];
  }
  return {ch:1, id:'1.01'};
}
function viewHash(){
  if(state.view==='play') return '#play';
  if(state.view==='favorites') return '#favorites';
  if(state.view==='search') return '#search';
  if(state.view==='sections') return '#ways';
  if(state.view==='chapters' && state.section) return '#way='+state.section;
  if(state.view==='learn' && state.chapter!=null) return '#chapter='+(state.chapter+1)+'&tab=learn';
  if(state.view==='chapter' && state.chapter!=null && state.theme!=null)
    return '#theme='+(state.chapter+1)+'.'+state.theme;
  if(state.view==='chapter' && state.chapter!=null)
    return '#chapter='+(state.chapter+1)+'&tab=chapter';
  return '';
}
function persistView(){
  const h = viewHash();
  try{ sessionStorage.setItem('gita.route', h || '#'); }catch(e){}
  const modal = document.getElementById('modalBg');
  if(modal && modal.classList.contains('open')){ scheduleSessionSave(); return; }
  const cur = location.hash || '';
  if(cur !== h && (h || cur)){
    try{ history.replaceState(history.state, '', h || (location.pathname + location.search)); }catch(e){}
  }
  scheduleSessionSave();
}
function goHome(){
  if($('#modalBg').classList.contains('open')) closeModal();
  $('#searchInput').value = '';
  state.origin = null;
  showWelcome();
}
function showWelcome(){
  state.view='welcome'; state.chapter=null; state.theme=null; state.section=null; persistView(); renderCrumbs();
  view.innerHTML = `
    <div class="welcome fade-in">
      <div class="w-om">ॐ</div>
      <h2 class="view-title">${esc(L('welcome_title'))}</h2>
      <p class="view-sub">${esc(L('welcome_sub'))}</p>
      <div id="wDay"></div>
      <button class="tool-btn primary big" onclick="showSections()">${esc(L('welcome_enter'))}</button>
      <details class="welcome-guide">
        <summary>${esc(L('guide_explore'))}</summary>
        <ol>
          <li>${esc(L('guide_way'))}</li>
          <li>${esc(L('guide_chapter'))}</li>
          <li>${esc(L('guide_verse'))}</li>
        </ol>
      </details>
      <div class="w-foot">${esc(L('welcome_foot'))}</div>
    </div>`;
  const paint = (dv, shared)=>{
    if(!dv || state.view!=='welcome' || !DATA || !DATA[dv.ci]) return;
    const c = DATA[dv.ci], v = verseAt(dv);
    const part = sutraAt(c.themes[dv.ti], dv.si).part;
    const el = document.getElementById('wDay'); if(!el) return;
    el.innerHTML = `<div class="w-day fade-in" role="button" tabindex="0" onclick="openModal(${dv.ci},${dv.ti},${dv.si},'book',null,this)">
          <div class="wd-label">${esc(shared ? L('shared_label') : L('verse_of_day'))}</div>
          <div class="vnum">${esc(L('verse'))} ${esc(fmtNL(v.n))}</div>
          <div class="m-topic"><span class="mt-lab">${esc(L('verse_topic'))}:</span> ${esc(T(part.titles))}</div>
          <div class="padas" lang="sa">${padaBlockDeva(v)}</div>
          <div class="vhint">${shared ? esc(L('shared_hint')) : esc(T(v.paras))}</div>
        </div>`;
  };
  if(state.shared){ loadChapter(state.shared.ci+1).then(()=>paint(state.shared, true)).catch(gitaLoadFail); }
  else {
    const sp = daySpec();
    loadChapter(sp.ch).then(()=>paint(verseLoc(sp.id), false)).catch(gitaLoadFail);
  }
}
function sectionCard(k, chip, title, desc){
  return `<div class="card sect" role="button" tabindex="0" onclick="showChapters(${k})">
    <span class="chip">${esc(chip)}</span>
    <h3>${esc(title)}</h3>
    <p>${esc(desc)}</p>
  </div>`;
}
function showSections(){
  state.view='sections'; state.chapter=null; state.theme=null; state.section=null; state.shared=null; persistView(); renderCrumbs();
  view.innerHTML = `
    <div class="view-title fade-in" role="heading" aria-level="2">${esc(L('sections_title'))}</div>
    <div class="view-sub fade-in">${esc(L('sections_sub'))}</div>
    <div class="grid sections fade-in">
      ${sectionCard(1, chaptersRange(1,6), L('sec_karma'), L('sec_karma_desc'))}
      ${sectionCard(2, chaptersRange(7,12), L('sec_bhakti'), L('sec_bhakti_desc'))}
      ${sectionCard(3, chaptersRange(13,18), L('sec_jnana'), L('sec_jnana_desc'))}
    </div>
    `;
}

/* The way-pills became a breadcrumb (owner, 2026-08-27): by the time the
   reader reaches a chapter there is already the mūla/meaning/study tab row,
   and a second strip of pills was one chooser too many. A trail of names —
   The Three Ways › Way of Karma › Chapter 2 — says where you are without
   offering a parallel universe of buttons. Last item is the current page. */
function wayCrumbs(items){
  /* The trail always ends at where the reader actually is: ancestors are
     quiet links, the last item is the current page (aria-current). A view
     reached through a door therefore shows the door's Sanskrit name as its
     final crumb — and the chapter crumb before it stays a LIVE link back to
     the choice page (owner 2026-08-30: landing in a chapter left him no way
     back; wayCrumbs used to kill the action of a last-item link). */
  return `<nav class="way-crumb fade-in" aria-label="${esc(L('breadcrumb'))}">` + items.map((it,i)=>{
    const last = i === items.length - 1;
    const sep = i ? `<span class="wc-sep" aria-hidden="true">›</span>` : '';
    if(!last) return sep + `<button class="wc-chip wc-link" onclick="${it[1]}">${esc(it[0])}</button>`;
    return sep + `<span class="wc-chip wc-cur" aria-current="page">${esc(it[0])}</span>`;
  }).join('') + `</nav>`;
}
function wayName(k){ /* the trail carries the Sanskrit mārga name, as the
  landing cards do — "कर्ममार्ग · The Way of Karma" — so the map is always
  rooted in the tradition, in every language (owner 2026-10-09, HANDOFF §7.1:
  the UI says मार्ग; निष्ठा belongs to the verses — 3.3 is dvividhā, two) */
  return L('sec_'+['','karma','bhakti','jnana'][k]); }
/* The chapter's three views live in one quiet "View mode" chooser under the
   breadcrumb (owner, 2026-08-28) — a book folio control, not a strip of pills.
   Mula is the default because that is what a chapter *is*; the rest are views. */
/* The three ways of receiving a chapter live on the chapter page itself as
   an iOS-style segmented control — the same grammar as the language pills
   (owner 2026-08-30: the intermediary choice page "was just making things
   weirder"). One quiet line above says Choose; the raised segment says
   where you are. The segment descriptions ride in title/aria, so the
   control stays quiet but never cryptic. */
function modeSwitch(ci){
  /* Phase 3.1: compact tab strip. No framing card, no "How would you like…"
     label — with only two modes (read / learn) a question is dead weight.
     Quiet underlined tabs read like a book ("the text" / "memorize"), not a
     setup wizard. */
  const m = state.view === 'learn' ? 'learn' : 'chapter';
  const btn = (mode, lab, fn, tip) =>
    `<button class="ms-btn${m === mode ? ' on' : ''}" title="${tip}" aria-label="${tip}" aria-pressed="${m === mode ? 'true' : 'false'}" onclick="${fn}">${lab}</button>`;
  return `<div class="mode-box fade-in">
    <div class="mode-seg" role="tablist" aria-label="${esc(L('choose_title'))}">
      ${btn('chapter', esc(L('opt_chapter')), `showChapter(${ci})`, esc(L('opt_chapter_d')))}
      ${btn('learn',   esc(L('opt_learn_s')), `showLearn(${ci})`,   esc(L('opt_learn_d')))}
    </div>
  </div>`;
}
function chTitle(ch){
  const name = esc(T(ch.names));
  const head = state.lang === 'en'
    ? `<span class="chdeva">${ch.deva}</span> · ${name}`
    : name;
  return `<div class="view-title fade-in" role="heading" aria-level="2">${head}</div>`;
}
/* One chapter view: keep the theme map visible first, with each theme's range
   ahead of its title. Opening a theme reveals its description and verse cards;
   a verse card opens the Phase-3.2 sheet. showVerses stays as the alias for
   back-links and saved routes; a theme anchor opens that theme. */
function showChapter(ci, anchorTi){
  if(!GITA_CH[ci+1]||!GITA_CH[ci+1].themes){ loadChapter(ci+1).then(()=>showChapter(ci,anchorTi)).catch(gitaLoadFail); return; }
  if(!DATA[ci]||!DATA[ci].themes){ showWelcome(); return; }
  const ch = DATA[ci];
  /* A stale #theme= link (the study maps were renumbered in 15 chapters) can
     name a theme this chapter no longer has. Open the chapter without an
     anchor rather than one nothing matches; the guards downstream (the live
     label, the crumb, the scroll) then all see a theme that exists. */
  const at = (anchorTi != null && ch.themes[anchorTi] != null) ? anchorTi : null;
  state.view='chapter'; state.chapter=ci; state.section = state.section || Math.ceil(ch.num/6);
  state.theme = at;
  persistView(); renderCrumbs();
  const themeSec = (at != null) ? numL(at+1) : '';
  let flatSi = 0;
  const body = ch.themes.map((t,ti)=>{
    const verseCards = t.parts.map(p=>{
      const s = p.sutras[0];
      const si = flatSi++;
      /* The paraphrase is printed whole, not cut at 90 characters (the cut
         lived here until 2026-10-18): a reader working through the theme map
         stays in the chapter and wants the complete thought under each
         title — the longest paraphrase in the corpus is ~190 characters,
         four or five card lines. Clicking a card still opens the sheet for
         the Sanskrit and the word-by-word reading. */
      return `<div class="mini" role="button" tabindex="0" onclick="openModal(${ci},${ti},${si},'theme',null,this)">
        <div class="vnum">${L('verse')} ${fmtNL(s.n)}</div>
        <div class="vtitle">${esc(T(p.titles))}</div>
        <div class="vhint">${esc(T(s.paras))}</div>
      </div>`;
    }).join('');
    return `<details class="ch-theme" id="theme-${ti}"${at===ti?' open':''}>
      <summary class="ch-theme-head">
        <span class="rng">${fmtRangeL(t.range)}</span>
        <span class="ch-theme-name" role="heading" aria-level="3">${esc(T(t.titles))}</span>
      </summary>
      <div class="ch-theme-body">
        <p class="ch-theme-desc">${esc(T(t.descs))}</p>
        <div class="grid verses">${verseCards}</div>
      </div>
    </details>`;
  }).join('');
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'), 'showSections()'], [wayName(Math.ceil(ch.num/6)), `showChapters(${Math.ceil(ch.num/6)})`], [`${L('chapter')} ${numL(ch.num)}${themeSec?' · '+L('theme_sg')+' '+themeSec:''}`, null]])}
    ${chTitle(ch)}
    ${modeSwitch(ci)}
    <div class="view-sub fade-in">${esc(T(ch.subs))} — ${L('click_hint')}.</div>
    <div class="ch-flow fade-in">${body}${colophonHtml(ch)}</div>` + backFoot(`showChapters(${state.section||0})`, L('back_chapters'));
  /* If an anchor theme was requested (deep link / back), scroll to it. */
  if(at != null){
    requestAnimationFrame(()=>{
      const el = document.getElementById('theme-'+at);
      if(el){
        el.open = true;
        if(!GITA_RESTORING) el.scrollIntoView({behavior:'smooth', block:'start'});
      }
    });
  }
}
/* Alias for the older routes / back-links / stored view state. Phase 3.1 merged
   the per-theme page and the continuous-reading page into this one chapter
   view; a #theme=N.T link (published by the generated chapter pages) and the
   verse sheet's "back to theme" both land here with that theme opened. */
function showVerses(ci,ti){ showChapter(ci, ti); }

function flatIndex(t,p,s){ let idx=0; for(const pp of t.parts){ if(pp===p) return idx+s; idx+=pp.sutras.length; } return idx; }
function sutraAt(t,i){ for(const p of t.parts){ if(i < p.sutras.length) return {s:p.sutras[i], part:p}; i-=p.sutras.length; } return {s:t.parts[t.parts.length-1].sutras[0], part:t.parts[t.parts.length-1]}; }

// pāda display: Devanagari block with pādas on separate lines (speakers inline)
function pDanda(i, total){
  if(total === 2) return (i===0) ? ' ।' : ' ॥';
  return (i%4===1)?' ।':((i%4===3)?' ॥':'');
}
function pDandaLatn(i, total){
  if(total === 2) return (i===0) ? ' |' : ' ||';
  return (i%4===1)?' |':((i%4===3)?' ||':'');
}
/* The running verse is derived from the canonical d/t strings by verseLines().
   Its `।`-separated segments stay in source order: two verse lines, plus a
   speaker where the text has one (including the mid-verse positions in 1.21
   and 1.28). The modal's 2x2 boxes use the separate `flow` pāda records. */
function padaBlockDeva(s, withNum){
  /* withNum puts the verse number inside the closing daṇḍas of the final line
     — ॥ १.२५ ॥ — the way a printed edition sets it, instead of on a line of
     its own below. Same construction as the reading view's rd-n. */
  const ls = verseLines(s), last = ls.reduce((a,it,i)=> it.k === 's' ? a : i, -1);
  let html = '', li = 0;
  for(let i = 0; i < ls.length; i++){
    const it = ls[i];
    if(it.k === 's'){
      html += `<span class="spk">${it.d}</span>`;
      if(it.t) html += `<span class="spk-iast" lang="sa-Latn">${esc(it.t)}</span>`;
      continue;
    }
    const tail = li
      ? (withNum && i === last ? `॥ <span class="gl-n">${esc(fmtNL(s.n))}</span> ॥` : '॥')
      : '।';
    html += `<div class="gline">${it.d}${tail}</div>`;
    if(it.t) html += `<div class="giast" lang="sa-Latn">${esc(it.t)}</div>`;
    li++;
  }
  return html;
}


let SRCH_HITS = [], FAV_LIST = [];
/* The verse range a reader walks in thematic study: the WHOLE theme.
   Until 2026-09-01 this returned the enclosing part's bounds, which was right
   when a part grouped several verses. Parts are now one verse each (700 parts
   for 700 verses), so it returned {start:n, end:n} — a range of one — and
   Prev/Next were disabled on every verse in the app. The theme is the unit. */
function themeBounds(t){
  let n = 0; for(const p of t.parts) n += p.sutras.length;
  return {start:0, end:Math.max(0, n-1)};
}
function setAppInert(inert){
  document.querySelectorAll('body > header, body > .toolbar, body > .wrap, body > footer')
    .forEach(el=>{ el.inert = inert; });
}
function updateModalAddress(){
  try{
    const s = sutraAt(DATA[state.chapter].themes[state.theme], state.idx).s;
    const old = history.state && typeof history.state === 'object' ? history.state : {};
    history.replaceState({...old, gitaModal:true}, '', '#v=' + s.n);
  }catch(e){}
}
function openModal(ci,ti,si, mode, navIdx, invoker, restoring){
  if(!GITA_CH[ci+1]||!GITA_CH[ci+1].themes){ loadChapter(ci+1).then(()=>openModal(ci,ti,si, mode, navIdx, invoker, restoring)).catch(gitaLoadFail); return; }
  const bg = $('#modalBg');
  if(!bg.classList.contains('open')){
    const active = document.activeElement;
    MODAL_RETURN_FOCUS = invoker || (active && active !== document.body ? active : null);
  }
  mode = mode || 'theme';
  state.chapter=ci; state.theme=ti; state.idx=si; state.mode=mode;
  state.gpos = VERSES.findIndex(e => e.ci===ci && e.ti===ti && e.si===si);
  if(state.gpos < 0) state.gpos = 0;
  if(mode === 'theme'){
    const b = themeBounds(DATA[ci].themes[ti]);
    state.pStart = b.start; state.pEnd = b.end;
  } else if(mode === 'search'){ mode = 'book'; }
  else if(mode === 'fav'){ state.navList = FAV_LIST; state.navIdx = navIdx || 0; }
  state.mode = mode;
  fillModal();
  bg.classList.add('open'); bg.setAttribute('aria-hidden','false');
  document.body.classList.add('modal-open');
  setAppInert(true); document.body.style.overflow='hidden';
  const close = $('#modal .m-close'); if(close) close.focus({preventScroll:true});
  if(restoring) MODAL_HIST = true;
  else pushModalHistory();
  /* every verse has an address: the sheet writes #v=2.47 so the open verse
     can be shared. The session snapshot marks this as an in-app modal; on a
     reload it is restored as a sheet, while a copied #v= link stays an invite. */
  updateModalAddress();
  saveSessionSnapshot();
}
function closeModal(){
  const bg = $('#modalBg');
  const wasOpen = bg.classList.contains('open');
  closeVerseMenu(); closeSharePanel();
  bg.classList.remove('open'); document.body.style.overflow='';
  document.body.classList.remove('modal-open');
  if(wasOpen){
    setAppInert(false);
    const target = MODAL_RETURN_FOCUS && MODAL_RETURN_FOCUS.isConnected && !MODAL_RETURN_FOCUS.disabled
      ? MODAL_RETURN_FOCUS : document.getElementById('view');
    MODAL_RETURN_FOCUS = null;
    if(target && target.focus) target.focus({preventScroll:true});
    bg.setAttribute('aria-hidden','true');
    popModalHistory();
  }
  persistView();
}
/* ---------- share a verse: native share sheet where available, else copy ---------- */
function shareUrl(){
  /* When the app runs from a downloaded copy (file://), a file path is
     useless to the recipient — and feeding one to the native share sheet
     crashes some Chromes. Share the live site's address instead (the og:url
     tag carries it), so shares from ANY copy land on the public verse. */
  const og = document.querySelector('meta[property="og:url"]');
  const root = (og ? og.content : 'https://chapain.github.io/Bhagavad-Gita/').replace(/\/$/, '');
  /* Owner 2026-09-01: shares point at the verse's anchor on its CHAPTER page
     (/chapter/N/#vN.NN). The 700 one-per-verse v/ pages are gone — GitHub's
     web uploader caps at 100 files, so republishing them was seven manual
     drags every time. The chapter page already carries the full verse in all
     four scripts and is already indexed; its inline script opens the folded
     <details> and highlights the verse, so the link still lands on the verse.
     Trade-off: the link PREVIEW is the chapter's, not the verse's. */
  const n = sutraAt(DATA[state.chapter].themes[state.theme], state.idx).s.n;
  return root + '/chapter/' + n.split('.')[0] + '/#v' + n;
}
function openSharePanel(){
  closeVerseMenu();
  $('#spLink').textContent = shareUrl();
  const p = $('#sharePanel');
  p.style.display = (p.style.display === 'flex') ? 'none' : 'flex';
}
function closeSharePanel(){ const p=$('#sharePanel'); if(p) p.style.display='none'; }
function copyVerseLink(){
  const t = $('#spLink').textContent;
  function copied(){
    /* Job done — collapse the panel right away and flash the confirmation on
       the Share button itself, so the reader is straight back on the verse. */
    const p = $('#sharePanel'); if(p) p.style.display = 'none';
    const sh = $('#shareBtn');
    if(sh){ sh.textContent = L('link_copied');
      setTimeout(function(){ sh.textContent = L('share'); }, 1600); }
  }
  try { navigator.clipboard.writeText(t).then(copied, copied); }
  catch(e){ const ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta);
    ta.select(); try{ document.execCommand('copy'); }catch(e2){} ta.remove(); copied(); }
}
/* ---------- mobile: Android hardware / iOS swipe "back" closes the verse sheet ---------- */
let MODAL_HIST = false, MODAL_POPPING = false, MODAL_RETURN_FOCUS = null;
function pushModalHistory(){
  if(MODAL_HIST) return;
  try{ sessionStorage.setItem('gita.preModalHash', viewHash()); }catch(e){}
  try{ history.pushState({gitaModal:true}, ''); MODAL_HIST = true; }catch(e){}
}
function popModalHistory(){
  if(!MODAL_HIST) return;
  MODAL_HIST = false;
  if(MODAL_POPPING) return;               // we got here *from* popstate — nothing to unwind
  try{ history.back(); }catch(e){}
  persistView();
}
window.addEventListener('popstate', ()=>{
  if($('#modalBg').classList.contains('open')){
    MODAL_POPPING = true; closeModal(); MODAL_POPPING = false;
  }
});

function fillModal(){
  const ch = DATA[state.chapter], t = ch.themes[state.theme];
  const {s, part} = sutraAt(t, state.idx);
  let partIdx = 0; { let acc = 0;
    for(let pi=0; pi<t.parts.length; pi++){ const len = t.parts[pi].sutras.length;
      if(state.idx >= acc && state.idx < acc+len){ partIdx = pi; break; } acc += len; } }
  if(state.gpos == null) state.gpos = Math.max(0, VERSES.findIndex(e => e.ci===state.chapter && e.ti===state.theme && e.si===state.idx));
  // split flow: top speakers, mid speakers (between pāda 2 and 3), and the 4 pādas
  let topS = [], midS = [], pads = [];
  for(const it of s.flow){
    if(it.k==='s'){ (pads.length < 2 ? topS : midS).push(it); }
    else pads.push(it);
  }
  const LI = {en:0, ne:1, hi:2}[state.lang] || 0;
  let speakerId = 0;
  function wordsHtml(it, id){
    return `<div class="words" id="${id}">${(it.words||[]).map(w=>`<div class="wrow"><span class="wdeva" lang="sa">${w[0]}</span><span class="wiast" lang="sa-Latn">${esc(w[1])}</span><span class="wmean">${esc(w[2+LI] || w[2])}</span></div>`).join('')}</div>`;
  }
  function spkHtml(list){
    return list.map(x=>{
      const id = `words-speaker-${speakerId++}`;
      return `<button type="button" class="spk-line" aria-expanded="false" aria-controls="${id}" aria-describedby="wordsHint" onclick="toggleWords(this)">
        <span class="spk-main" lang="sa">${x.d} <span class="iast" lang="sa-Latn">${esc(x.t)}</span></span>
      </button>${wordsHtml(x,id)}`;
    }).join('');
  }
  function boxHtml(pad, idx, total){
    const id = `words-pada-${idx}`;
    return `<div class="pada-box">
      <button type="button" class="pada-toggle" aria-expanded="false" aria-controls="${id}" aria-describedby="padaHint" onclick="toggleWords(this)">
        <span class="pb-top"><span class="pb-num">${esc(L('pada_label'))} ${numL(idx+1)}</span></span>
        <span class="pb-deva" lang="sa">${pad.d}${pDanda(idx,total)}</span>
        <span class="pb-iast" lang="sa-Latn">${esc(pad.t)}${pDandaLatn(idx,total)}</span>
      </button>${wordsHtml(pad,id)}
    </div>`;
  }
  $('#modal').innerHTML = `
    <div class="m-head">
      <button type="button" class="m-close" aria-label="${esc(L('close_verse'))}" title="${esc(L('close_verse'))}" onclick="closeModal()">✕</button>
      <h2 class="m-title" id="modalTitle" tabindex="-1">
        <span class="m-num-chit">${esc(L('verse'))} ${fmtNL(s.n)}</span>
        <span class="m-vtitle">${esc(T(part.titles))}</span>
      </h2>
      <button type="button" class="m-more" id="mMoreBtn" aria-label="More" aria-haspopup="true" aria-expanded="false" onclick="toggleVerseMenu()">⋯</button>
    </div>
    <div class="m-menu" id="mVerseMenu" role="menu" hidden>
      <button type="button" role="menuitem" id="shareBtn" onclick="openSharePanel()">${L('share')}</button>
      <button type="button" role="menuitem" class="${FAV.includes(s.n)?' saved':''}" id="favBtn" aria-pressed="${FAV.includes(s.n)}" onclick="toggleFav('${s.n}')">${FAV.includes(s.n)?ICONS.starF:ICONS.star} ${esc(FAV.includes(s.n)?L('saved_verse'):L('save_verse'))}</button>
      <div class="m-menu-sep" role="separator"></div>
      <div class="m-meter">${esc(meterText(s))}</div>
      <div class="reader-size" role="group" aria-label="${esc(L('reader_size'))}">
        <span class="reader-size-label">${esc(L('reader_size'))}</span>
        <button type="button" id="readerSizeDown" onclick="stepReaderSize(-1)" aria-label="${esc(L('reader_size_decrease'))}" title="${esc(L('reader_size_decrease'))}">A−</button>
        <span class="reader-size-value" id="readerSizeValue" aria-live="polite" aria-atomic="true">${numL(state.readerSize)}%</span>
        <button type="button" id="readerSizeUp" onclick="stepReaderSize(1)" aria-label="${esc(L('reader_size_increase'))}" title="${esc(L('reader_size_increase'))}">A+</button>
        <button type="button" onclick="resetReaderSize()" aria-label="${esc(L('reader_size_reset'))}" title="${esc(L('reader_size_reset'))}">↺</button>
      </div>
      <button type="button" role="menuitem" class="wb-btn" id="wbMasterBtn" onclick="toggleAllMeanings(this)" disabled aria-pressed="false">${ICONS.eyeOff}<span>${L('hide_meanings')}</span></button>
    </div>
    <div class="share-panel" id="sharePanel">
      <div class="sp-hint">${L('share_hint')}</div>
      <div class="sp-link" id="spLink"></div>
      <button class="sp-copy" id="shCp" onclick="copyVerseLink()">${L('copy_link')}</button>
    </div>
    <div class="m-part">${esc(L('theme_sg'))} ${fmtRangeL(t.range)} · ${esc(T(t.titles))}</div>
    <div class="reader-copy">
      <div class="m-whole-verse" lang="sa">
        ${padaBlockDeva(s, true)}
      </div>
      <details class="m-words-section" id="mWordsSection">
        <summary><span class="m-wb-hint" id="wordsHint">${L('click_hint_pada')}</span></summary>
        <div class="m-words-body">
          <p class="m-pada-hint" id="padaHint">${esc(L('click_pada_meanings'))}</p>
          <div class="m-verse">
            ${spkHtml(topS)}
            <div class="pada-grid">
              <div class="pada-row">${boxHtml(pads[0],0,pads.length)}${boxHtml(pads[1],1,pads.length)}</div>
              ${midS.length ? `<div class="spk-mid">${spkHtml(midS)}</div>` : ''}
              ${pads.length===4 ? `<div class="pada-row">${boxHtml(pads[2],2,4)}${boxHtml(pads[3],3,4)}</div>` : ''}
            </div>
          </div>
        </div>
      </details>
      <div class="m-line lit"><span class="lb">${L('literal')}</span><div class="lt">${esc(T(s.lits))}</div></div>
      <div class="m-line para"><span class="lb">${L('in_other_words')}</span><div class="lt">${esc(T(s.paras))}</div></div>
    </div>
    <div class="m-tail" aria-hidden="true"></div>
    <div class="m-nav">
      ${state.mode==='random'
        ? `<button class="m-random" onclick="randomVerse()">${ICONS.shuffle}<span>${esc(L('next_random'))}</span></button>`
        : state.mode==='theme'
          ? `<button onclick="navSutra(-1)" ${(state.idx>state.pStart||state.theme>0)?'':'disabled'}>${(state.idx===state.pStart && state.theme>0)?L('prev_theme'):L('previous')}</button>
             <span class="m-count">${Lof(state.idx-state.pStart+1, state.pEnd-state.pStart+1)}</span>
             ${state.idx===state.pEnd && state.theme===DATA[state.chapter].themes.length-1
               ? `<button class="m-back" onclick="backToTheme()">${esc(L('back_to_theme'))}</button>`
               : `<button onclick="navSutra(1)">${state.idx===state.pEnd?L('next_theme'):L('next')}</button>`}`
          : state.mode==='book'
          ? `<button onclick="navSutra(-1)" ${state.gpos>0?'':'disabled'}>${L('previous')}</button>
             <span class="m-count">${Lof(state.gpos+1, VERSES.length)}</span>
             <button onclick="navSutra(1)" ${state.gpos<VERSES.length-1?'':'disabled'}>${L('next')}</button>`
          : `<button onclick="navSutra(-1)" ${(state.navIdx||0)>0?'':'disabled'}>${L('previous')}</button>
             <span class="m-count">${Lof((state.navIdx||0)+1, state.navList?state.navList.length:1)}</span>
             <button onclick="navSutra(1)" ${(state.navIdx||0) < (state.navList?state.navList.length-1:0)?'':'disabled'}>${L('next')}</button>`}
    </div>`;
  applyReaderSize();
}
function setReaderSize(size){
  if(!READER_SIZES.includes(size)) return;
  state.readerSize = size;
  try{ localStorage.setItem('gitaReaderSize', String(size)); }catch(e){}
  applyReaderSize();
}
function stepReaderSize(delta){
  const i = READER_SIZES.indexOf(state.readerSize);
  setReaderSize(READER_SIZES[Math.max(0, Math.min(READER_SIZES.length-1, i+delta))]);
}
function resetReaderSize(){ setReaderSize(100); }
function applyReaderSize(){
  const reader = document.querySelector('#modal .reader-copy');
  if(reader) reader.style.setProperty('--reader-scale', String(state.readerSize / 100));
  const value = document.getElementById('readerSizeValue');
  if(value) value.textContent = numL(state.readerSize) + '%';
  const down = document.getElementById('readerSizeDown');
  const up = document.getElementById('readerSizeUp');
  if(down) down.disabled = state.readerSize <= READER_SIZES[0];
  if(up) up.disabled = state.readerSize >= READER_SIZES[READER_SIZES.length-1];
}
/* Phase 3.2 — verse-sheet overflow menu (⋯). Share / Save / Text size /
   Hide-meanings live here so they don't crowd the top of the sheet. */
function toggleVerseMenu(){
  const menu = $('#mVerseMenu'), btn = $('#mMoreBtn');
  if(!menu || !btn) return;
  if(menu.hasAttribute('hidden')){ menu.removeAttribute('hidden'); btn.setAttribute('aria-expanded','true'); }
  else { menu.setAttribute('hidden',''); btn.setAttribute('aria-expanded','false'); }
}
function closeVerseMenu(){ const menu=$('#mVerseMenu'), btn=$('#mMoreBtn');
  if(menu && !menu.hasAttribute('hidden')){ menu.setAttribute('hidden',''); if(btn) btn.setAttribute('aria-expanded','false'); }
}
document.addEventListener('click', function(e){
  const menu = $('#mVerseMenu'), btn = $('#mMoreBtn');
  if(!menu || menu.hasAttribute('hidden')) return;
  if(menu.contains(e.target) || (btn && btn.contains(e.target))) return;
  closeVerseMenu();
});
// toggle pada-chheda (word split) open/closed on the clicked element's box/line
function toggleWords(el){
  const id = el.getAttribute('aria-controls');
  const words = id ? document.getElementById(id) : null;
  if(!words) return;
  const open = words.classList.toggle('open');
  el.setAttribute('aria-expanded', String(open));
  refreshWordsBtn();
}
/* The master hide/show switch only means something once at least one quarter
   is open — before that there is no meaning on screen to hide. So it waits,
   disabled, until a pada is clicked (owner, 2026-08-27). */
function refreshWordsBtn(){
  const btn = document.querySelector('#modal .wb-btn');
  if(!btn) return;
  const anyOpen = !!document.querySelector('#modal .words.open');
  btn.disabled = !anyOpen;
  if(!anyOpen){   // fresh slate: next opening shows meanings again
    btn.dataset.state = '';
    btn.setAttribute('aria-pressed', 'false');
    btn.innerHTML = ICONS.eyeOff + `<span>${esc(L('hide_meanings'))}</span>`;
    document.querySelectorAll('#modal .words').forEach(w=>w.classList.remove('mean-off'));
  }
}
// toggle meaning visibility across all word-splits in the modal
function toggleAllMeanings(btn){
  const hide = btn.dataset.state !== 'hidden';   // meanings start visible → first click hides
  btn.dataset.state = hide ? 'hidden' : 'shown';
  btn.setAttribute('aria-pressed', String(hide));
  btn.innerHTML = (hide ? ICONS.eye : ICONS.eyeOff) + `<span>${esc(L(hide ? 'show_meanings' : 'hide_meanings'))}</span>`;
  document.querySelectorAll('#modal .words').forEach(w=>{
    w.classList.toggle('mean-off', hide);
  });
}
function restoreModalSession(modalSnap){
  if(!modalSnap) return;
  const modal = document.getElementById('modal');
  restoreSessionDetails(modal, modalSnap.openDetails);
  (Array.isArray(modalSnap.openWords) ? modalSnap.openWords : []).forEach(id=>{
    const words = document.getElementById(id);
    if(!words || !modal.contains(words)) return;
    words.classList.add('open');
    modal.querySelectorAll('[aria-controls]').forEach(btn=>{
      if(btn.getAttribute('aria-controls') === id) btn.setAttribute('aria-expanded','true');
    });
  });
  refreshWordsBtn();
  if(modalSnap.meaningsHidden){
    const master = modal.querySelector('.wb-btn');
    if(master && !master.disabled) toggleAllMeanings(master);
  }
  if(modalSnap.shareOpen) openSharePanel();
  else if(modalSnap.menuOpen) toggleVerseMenu();
  if(Number.isFinite(modalSnap.scrollTop)) modal.scrollTop = Math.max(0, modalSnap.scrollTop);
}
function navSutra(d){
  if(state.mode === 'theme'){
    const n = state.idx + d;
    if(n >= state.pStart && n <= state.pEnd){
      state.idx = n;
    } else if(d > 0 && state.theme + 1 < DATA[state.chapter].themes.length){
      state.theme += 1;
      const b = themeBounds(DATA[state.chapter].themes[state.theme]);
      state.pStart = b.start; state.pEnd = b.end; state.idx = b.start;
    } else if(d < 0 && state.theme > 0){
      state.theme -= 1;
      const b = themeBounds(DATA[state.chapter].themes[state.theme]);
      state.pStart = b.start; state.pEnd = b.end; state.idx = b.end;
    } else return;
  } else if(state.mode === 'book'){
    state.gpos = Math.max(0, Math.min(VERSES.length-1, (state.gpos || 0) + d));
    const loc = VERSES[state.gpos];
    state.chapter = loc.ci; state.theme = loc.ti; state.idx = loc.si;
  } else if((state.mode === 'fav') && state.navList){
    const k = (state.navIdx || 0) + d;
    if(k < 0 || k >= state.navList.length) return;
    state.navIdx = k;
    const loc = state.navList[k];
    state.chapter = loc.ci; state.theme = loc.ti; state.idx = loc.si;
  } else return;
  state.gpos = VERSES.findIndex(e => e.ci===state.chapter && e.ti===state.theme && e.si===state.idx);
  if(state.gpos < 0) state.gpos = 0;
  fillModal();
  updateModalAddress();
  saveSessionSnapshot();
  const title = $('#modalTitle'); if(title) title.focus({preventScroll:true});
  const m = $('#modal'); if(m) m.scrollTo({top:0, behavior:'smooth'});
}
function backToTheme(){ closeModal(); showVerses(state.chapter, state.theme); }
document.addEventListener('keydown', e=>{
  /* Keyboard parity (audit 2026-08-30): the tappable divs carry role="button"
     tabindex="0"; Enter/Space must do what the tap does. */
  if((e.key==='Enter' || e.key===' ') && document.activeElement
     && document.activeElement.matches && document.activeElement.matches('[role="button"]')){
    e.preventDefault(); document.activeElement.click(); return;
  }
  const tag = (e.target && e.target.tagName) ? e.target.tagName : '';
  if($('#modalBg').classList.contains('open')){
    if(e.key==='Tab'){
      const modal = $('#modal');
      const focusables = Array.from(modal.querySelectorAll(
        'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])'
      )).filter(el=>el.getClientRects().length>0);
      if(!focusables.length){ e.preventDefault(); modal.focus(); return; }
      const first = focusables[0], last = focusables[focusables.length-1];
      if(e.shiftKey && (document.activeElement===first || !modal.contains(document.activeElement))){
        e.preventDefault(); last.focus();
      } else if(!e.shiftKey && (document.activeElement===last || !modal.contains(document.activeElement))){
        e.preventDefault(); first.focus();
      }
      return;
    }
    if(e.key==='Escape'){ closeModal(); return; }
    if(state.mode==='random') return;
    if(tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
    if(e.key==='ArrowLeft') navSutra(-1);
    if(e.key==='ArrowRight') navSutra(1);
    return;
  }
  if(tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
  if(state.view === 'learn' && LV && LV.vs){
    if(e.key==='ArrowLeft'){ e.preventDefault(); lrMeetGo(-1); }
    if(e.key==='ArrowRight'){ e.preventDefault(); lrMeetGo(1); }
  }
});


/* Keep a lightweight, per-tab checkpoint current. In addition to explicit
   route changes this catches disclosure toggles, search text, modal controls,
   and scroll position before either a manual reload or the SW update reload. */
let GITA_SCROLL_TIMER = null;
const checkpointSoon = () => scheduleSessionSave();
document.addEventListener('click', checkpointSoon, true);
document.addEventListener('input', checkpointSoon, true);
document.addEventListener('change', checkpointSoon, true);
document.addEventListener('toggle', checkpointSoon, true);
function checkpointScroll(){
  clearTimeout(GITA_SCROLL_TIMER);
  GITA_SCROLL_TIMER = setTimeout(()=>scheduleSessionSave(false), 180);
}
window.addEventListener('scroll', checkpointScroll, {passive:true});
document.addEventListener('scroll', checkpointScroll, true);
window.addEventListener('pagehide', ()=>saveSessionSnapshot());
document.addEventListener('visibilitychange', ()=>{
  if(document.visibilityState === 'hidden') saveSessionSnapshot();
});

/* Learn-by-heart: swipe between verses of the open theme (same as Previous/Next). */
(function(){
  const el = document.getElementById('view'); if(!el) return;
  let x0=null, y0=null, t0=0, lock=null;
  el.addEventListener('touchstart', e=>{
    if(e.touches.length!==1){ x0=null; return; }
    if(e.target && e.target.closest && e.target.closest('.lr-qh .tx')){
      const tx = e.target.closest('.tx');
      if(tx && tx.scrollWidth > tx.clientWidth + 4){ x0=null; return; }
    }
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; t0 = Date.now(); lock = null;
  }, {passive:true});
  el.addEventListener('touchmove', e=>{
    if(x0==null || e.touches.length!==1) return;
    const dx = e.touches[0].clientX - x0, dy = e.touches[0].clientY - y0;
    if(lock===null && (Math.abs(dx) > 12 || Math.abs(dy) > 12)) lock = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
  }, {passive:true});
  el.addEventListener('touchend', e=>{
    if(x0==null || lock!=='x'){ x0=null; return; }
    const dx = (e.changedTouches[0].clientX - x0);
    const dt = Date.now() - t0;
    x0 = null;
    if(dt > 800 || Math.abs(dx) < 60) return;
    if(state.view === 'learn') lrMeetGo(dx < 0 ? 1 : -1);
  }, {passive:true});
})();

/* ---------- mobile: horizontal swipe inside the verse sheet = prev / next ---------- */
(function(){
  const bg = $('#modalBg'); if(!bg) return;
  let x0=null, y0=null, t0=0, lock=null;
  bg.addEventListener('touchstart', e=>{
    if(e.touches.length!==1){ x0=null; return; }
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; t0 = Date.now(); lock = null;
  }, {passive:true});
  bg.addEventListener('touchmove', e=>{
    if(x0==null || e.touches.length!==1) return;
    const dx = e.touches[0].clientX - x0, dy = e.touches[0].clientY - y0;
    if(lock===null && (Math.abs(dx) > 12 || Math.abs(dy) > 12)) lock = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
  }, {passive:true});
  bg.addEventListener('touchend', e=>{
    if(x0==null || lock!=='x'){ x0=null; return; }
    const dx = (e.changedTouches[0].clientX - x0);
    const dt = Date.now() - t0;
    x0 = null;
    if(dt > 800 || Math.abs(dx) < 60) return;
    if(state.mode === 'random') return;
    navSutra(dx < 0 ? 1 : -1);              // swipe left → next, swipe right → previous
  }, {passive:true});
})();
/* Offline support when served over http(s): the service worker caches the app so
   it opens with no connection and "Add to Home Screen" behaves like a real app.
   Deliberately skipped for file:// (WhatsApp/Drive downloads) — SWs are not
   allowed there and would throw. Failure is always non-fatal. */
if ('serviceWorker' in navigator && location.protocol.indexOf('http') === 0) {
  window.addEventListener('load', function(){
    navigator.serviceWorker.register(appBase() + 'sw.js').catch(function(){ /* offline cache unavailable — app still works */ });
    /* A new SW skipWaiting()+claim() does not replace the JS already running.
       Reload only when this tab already had a controller — first install must
       not bounce the reader. */
    var had = !!navigator.serviceWorker.controller;
    navigator.serviceWorker.addEventListener('controllerchange', function(){
      if (had){ saveSessionSnapshot(); location.reload(); }
    });
  });
}
function gitaBoot(){
  assembleData();
  /* Sync the language chrome first. state.lang already came from savedLang() and
     <html lang> from the pre-paint script, but the three buttons ship with
     English hard-coded on / aria-pressed="true" — a reader restored into नेपाली
     would otherwise see the wrong segment highlighted. syncLang() also calls
     applyStatic(), so the interface strings land in the restored language
     before the deep link below renders anything. */
  syncLang(state.lang);
  paintTheme();
  try{
    var path = location.pathname || '/';
    if (path.charAt(path.length-1) !== '/' && !/index.html$/i.test(path)){
      history.replaceState(history.state, '', path + '/' + (location.search||'') + (location.hash||''));
    }
  }catch(e){}
  const restore = readSessionSnapshot();
  if(restore){
    GITA_RESTORING = true; state.keepScroll = true;
    syncLang(restore.lang);
    try{ sessionStorage.setItem('gitaLang', restore.lang); }catch(e){}
    try{ sessionStorage.setItem('gita.route', restore.route || '#'); }catch(e){}
    const searchInput = document.getElementById('searchInput');
    if(searchInput) searchInput.value = restore.query || '';
    if(restore.play){
      PL.scope = restore.play.scope === 'ch' ? 'ch' : 'all';
      PL.ch = Number.isInteger(restore.play.ch) ? restore.play.ch : 0;
      PL.mode = Number.isInteger(restore.play.mode) ? restore.play.mode : 0;
      PL.run = Number.isInteger(restore.play.run) ? restore.play.run : 0;
      PL.q = restore.play.q || null; PL.active = !!restore.play.active;
    }
    if(restore.modal){
      const old = history.state && typeof history.state === 'object' ? history.state : {};
      const route = restore.route || '';
      try{
        history.replaceState({...old, gitaModal:false}, '',
          location.pathname + (location.search || '') + route);
      }catch(e){}
    }
    watchSessionRestore(restore);
  }
  /* Deep links: the chapter landing pages (and shared messages) can open a
     specific verse — index.html#v=2.47 — or a whole chapter (#chapter=7). */
  (function(){

    var v = /^#v=([1-9][0-9]?\.[0-9]{1,2})$/.exec(location.hash || '');
    if (v) { var hp = v[1].split('.');
      var vref = hp[0] + '.' + (hp[1].length === 1 ? '0' + hp[1] : hp[1]);
      var loc = verseLoc(vref);
      /* Owner 2026-08-31: a shared verse lands as an INVITATION, not a popup —
         the verse is shown on the welcome page with "click to see the
         meanings"; the four-pāda sheet opens when the receiver clicks. */
      if (loc) { state.shared = loc; showWelcome(); return; }
      /* Out of range (#v=2.99) or a chapter that does not exist (#v=19.1):
         fall back to the welcome page instead of a blank one — and never ask
         for data/ch19.js: it is not there and its rejection used to escape. */
      var hn = parseInt(hp[0], 10);
      if (hn > 18) { showWelcome(); return; }
      loadChapter(hn).then(function(){
        loc = verseLoc(vref);
        if (loc) { state.shared = loc; }
        showWelcome();
      }).catch(function(){ gitaLoadFail(); });
      return; }
    var tm = /^#theme=([1-9]|1[0-8])\.([0-9]+)$/.exec(location.hash || '');
    if (tm) { const ci = parseInt(tm[1], 10) - 1, ti = parseInt(tm[2], 10);
      loadChapter(ci+1).then(function(){ showVerses(ci, ti); }).catch(function(){ gitaLoadFail(); }); return; }
    var m = /^#chapter=([1-9]|1[0-8])(&tab=(mula|full|study|chapter|learn))?$/.exec(location.hash || '');
    if(m){ const ci = parseInt(m[1], 10) - 1; const tb = m[3];
      loadChapter(ci+1).then(function(){
        if(tb === 'learn'){ showLearn(ci); }
        else { showChapter(ci); }  /* full/mula/study/chapter all merge into the one chapter view */
      }).catch(function(){ gitaLoadFail(); }); return; }
    var h = location.hash || '';
    if(h === '#play'){ showPlay(); return; }
    if(h === '#favorites'){ showFavorites(); return; }
    if(h === '#search'){ doSearch(); return; }
    if(h === '#ways'){ showSections(); return; }
    var wy = /^#way=([123])$/.exec(h);
    if(wy){ showChapters(+wy[1]); return; }
    var stay = '';
    try{ stay = sessionStorage.getItem('gita.route')||''; }catch(e){}
    if(stay==='#play'){ showPlay(); return; }
    if(stay==='#favorites'){ showFavorites(); return; }
    if(stay==='#search'){ doSearch(); return; }
    if(stay==='#ways'){ showSections(); return; }
    var sw = /^#way=([123])$/.exec(stay);
    if(sw){ showChapters(+sw[1]); return; }
    var sm = /^#chapter=([1-9]|1[0-8])(&tab=(mula|full|study|chapter|learn))?$/.exec(stay);
    if(sm){
      const ci = parseInt(sm[1],10)-1, tb=sm[3];
      loadChapter(ci+1).then(function(){
        if(tb==='learn') showLearn(ci);
        else showChapter(ci);
      }).catch(function(){ gitaLoadFail(); }); return;
    }
    var st = /^#theme=([1-9]|1[0-8])\.([0-9]+)$/.exec(stay);
    if(st){
      const ci=parseInt(st[1],10)-1, ti=parseInt(st[2],10);
      loadChapter(ci+1).then(function(){ showVerses(ci, ti); }).catch(function(){ gitaLoadFail(); }); return;
    }
    showWelcome();
  })();
  var _idle = window.requestIdleCallback || function(fn){ setTimeout(fn, 1200); };
  _idle(function(){ loadAllChapters(); });
}

(function(){
  if (!window.matchMedia || !matchMedia('(hover: none)').matches) return;
  var SEL = '.card,.theme,.mini,.res-card,.w-day,.lr-chip,.pl-mode,.mode-box,.way-crumb,.lr-opt,.lr-chip2,.lr-ghost,.lr-cta,.pl-sel,.ms-btn,.wc-link,.pada-box,.tool-btn';
  var cur = null;
  function hit(el){
    while (el && el.nodeType === 1){
      if (el.matches(SEL) && !el.classList.contains('vcard')) return el;
      el = el.parentElement;
    }
    return null;
  }
  function at(x,y){
    var n = hit(document.elementFromPoint(x,y));
    if (n === cur) return;
    if (cur) cur.classList.remove('is-press');
    cur = n;
    if (cur) cur.classList.add('is-press');
  }
  function clear(){ if (cur){ cur.classList.remove('is-press'); cur = null; } }
  document.addEventListener('touchstart', function(e){ var t=e.touches[0]; if(t) at(t.clientX,t.clientY); }, {passive:true});
  document.addEventListener('touchmove', function(e){ var t=e.touches[0]; if(t) at(t.clientX,t.clientY); }, {passive:true});
  document.addEventListener('touchend', clear, {passive:true});
  document.addEventListener('touchcancel', clear, {passive:true});
})();
