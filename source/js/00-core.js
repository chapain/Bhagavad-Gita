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
/* Feature files publish their supported cross-feature operations here. Keeping
   one namespace makes dependencies visible without introducing a framework or
   changing the single-script build. */
const App = Object.create(null);
const SESSION_FIELDS = new Set(['chapter','theme','idx','lang','view','section','shared',
  'readerSize','origin','lrAt','keepScroll','mode','gpos','pStart','pEnd','navList','navIdx']);
function updateSessionState(patch){
  if(!patch || typeof patch !== 'object' || Array.isArray(patch)) return;
  for(const key of Object.keys(patch)){
    if(!SESSION_FIELDS.has(key)) throw new Error('Unknown session field: ' + key);
    state[key] = patch[key];
  }
}
App.session = Object.freeze({update:updateSessionState});
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
     || !['welcome','sections','chapters','chapter','learn','search','favorites','play','data'].includes(s.view)
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
function captureSessionSnapshot(){
  const bg = document.getElementById('modalBg'), modalOpen = !!(bg && bg.classList.contains('open'));
  let modal = null;
  if(modalOpen && state.chapter != null && state.theme != null && DATA && DATA[state.chapter]){
    try{
      const s = App.library.entryAt(DATA[state.chapter].themes[state.theme], state.idx).s;
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
    route:App.views.hash() || '', view:state.view, lang:state.lang,
    section:Number.isInteger(state.section) ? state.section : null,
    chapter:Number.isInteger(state.chapter) ? state.chapter : null,
    theme:Number.isInteger(state.theme) ? state.theme : null,
    idx:Number.isInteger(state.idx) ? state.idx : 0,
    origin, shared,
    query:(document.getElementById('searchInput') && document.getElementById('searchInput').value) || '',
    openDetails:sessionOpenDetails(document.getElementById('view')),
    scrollY:Math.max(0, window.scrollY || window.pageYOffset || 0),
    modal, readerSize:state.readerSize};
  if(state.view === 'learn') snap.learn = App.learn.snapshot();
  if(state.view === 'play') snap.play = App.play.snapshot();
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
async function finishSessionRestore(){
  if(!GITA_PENDING_RESTORE || GITA_RESTORE_FINISHING) return;
  const snap = GITA_PENDING_RESTORE;
  const root = document.getElementById('view');
  if(!root || !root.children.length || root.querySelector('#bootNote')) return;
  GITA_RESTORE_FINISHING = true;
  try{
    if(snap.view === 'welcome' && snap.shared){
      let shared = App.library.location(snap.shared);
      if(!shared){
        const n = parseInt(String(snap.shared).split('.')[0],10);
        if(n >= 1 && n <= 18) await loadChapter(n);
        shared = App.library.location(snap.shared);
      }
      if(shared){ state.shared = shared; App.views.welcome(); }
    }
    if(snap.origin) state.origin = sessionOrigin(snap.origin);
    if(snap.view === 'learn') App.learn.restore(snap);
    if(snap.view === 'play') App.play.restore(snap.play);
    restoreSessionDetails(document.getElementById('view'), snap.openDetails);
    if(snap.modal){
      let loc = App.library.location(snap.modal.id);
      if(!loc){
        const ch = parseInt(String(snap.modal.id).split('.')[0],10);
        if(ch >= 1 && ch <= 18) await loadChapter(ch);
        loc = App.library.location(snap.modal.id);
      }
      if(loc){
        await loadChapter(loc.ci + 1);
        window.scrollTo({top:Math.max(0, Number(snap.scrollY)||0), behavior:'auto'});
        App.reader.open(loc.ci, loc.ti, loc.si, snap.modal.mode,
          Number.isInteger(snap.modal.navIdx) && snap.modal.navIdx >= 0 ? snap.modal.navIdx : 0,
          null, true);
        App.reader.restore(snap.modal);
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
  const sl = $('#skipLink'); if(sl) sl.textContent = L('skip_to_content');
  $('#tagVerses').textContent = L('tag_sub'); $('#appFooter').textContent = L('footer');
  const footData = $('#footDataLink'); if(footData) footData.textContent = L('data_title') + ' · ' + L('data_export') + ' / ' + L('data_import');
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
  App.library.syncSearchControl(); }
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
    App.library.search();
  } else {
    App.library.search();
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
  // Remember which verse the modal is showing: App.library.search()/App.library.showFavorites()
  // below null out state.chapter/state.theme while re-rendering the
  // background view, which would otherwise leave the open modal stale.
  const modalOpen = $('#modalBg').classList.contains('open');
  const mCh = state.chapter, mTh = state.theme, mIdx = state.idx;
  if(state.view === 'welcome'){ App.views.welcome(); }
  else if(state.view === 'sections'){ App.views.sections(); }
  else if(state.view === 'search'){ App.library.search(); }
  else if(state.view === 'favorites'){ App.library.showFavorites(); }
  /* The learn path renders its own views and holds drill state in module
     vars, so it must NOT fall through to the generic chapter/theme restore
     below: with state.theme set that lands on the chapter view and the
     reader's drill simply disappears mid-question. Re-enter at the path's home — the
     only place that can safely rebuild in the new language, since a
     half-answered question's options were built from the old strings.
     Progress is already saved. */
  else if(state.view === 'learn'){ App.learn.relanguage(state.chapter); }
  /* Play rebuilds the question it is showing, in the new language, rather than
     quitting the game: the Play feature holds the verse and option order, and only the
     prompt, the note and the numerals were language-bound. If no question is
     open, fall back to the menu. */
  else if(state.view === 'play'){ App.play.relanguage(); }
  else {
    const ch = state.chapter, th = state.theme;
    if(ch == null){ if(state.section) App.views.chapters(state.section); else App.views.sections(); }
    else { App.views.chapter(ch, th == null ? undefined : th); }
  }
  if(modalOpen && mCh != null && mTh != null){
    state.chapter = mCh; state.theme = mTh; state.idx = mIdx;
    App.reader.refresh();
  }
  saveSessionSnapshot();
}
const $ = s => document.querySelector(s);
const crumbs = $('#crumbs'), view = $('#view');

