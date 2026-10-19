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
    if(state.view === 'learn') App.learn.navigate(dx < 0 ? 1 : -1);
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
    App.reader.navigate(dx < 0 ? 1 : -1);              // swipe left → next, swipe right → previous
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
  App.library.assemble();
  /* Sync the language chrome first. state.lang already came from savedLang() and
     <html lang> from the pre-paint script, but the three buttons ship with
     English hard-coded on / aria-pressed="true" — a reader restored into नेपाली
     would otherwise see the wrong segment highlighted. syncLang() also calls
     applyStatic(), so the interface strings land in the restored language
     before the deep link below renders anything. */
  syncLang(state.lang);
  App.library.paintTheme();
  try{
    var path = location.pathname || '/';
    if (path.charAt(path.length-1) !== '/' && !/index.html$/i.test(path)){
      history.replaceState(history.state, '', path + '/' + (location.search||'') + (location.hash||''));
    }
  }catch(e){}
  const restore = readSessionSnapshot();
  if(restore){
    GITA_RESTORING = true; App.session.update({keepScroll:true});
    syncLang(restore.lang);
    try{ sessionStorage.setItem('gitaLang', restore.lang); }catch(e){}
    try{ sessionStorage.setItem('gita.route', restore.route || '#'); }catch(e){}
    const searchInput = document.getElementById('searchInput');
    if(searchInput) searchInput.value = restore.query || '';
    if(restore.play) App.play.hydrate(restore.play);
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
      var loc = App.library.location(vref);
      /* Owner 2026-08-31: a shared verse lands as an INVITATION, not a popup —
         the verse is shown on the welcome page with "click to see the
         meanings"; the four-pāda sheet opens when the receiver clicks. */
      if (loc) { App.session.update({shared:loc}); App.views.welcome(); return; }
      /* Out of range (#v=2.99) or a chapter that does not exist (#v=19.1):
         fall back to the welcome page instead of a blank one — and never ask
         for data/ch19.js: it is not there and its rejection used to escape. */
      var hn = parseInt(hp[0], 10);
      if (hn > 18) { App.views.welcome(); return; }
      loadChapter(hn).then(function(){
        loc = App.library.location(vref);
        if (loc) App.session.update({shared:loc});
        App.views.welcome();
      }).catch(function(){ gitaLoadFail(); });
      return; }
    var tm = /^#theme=([1-9]|1[0-8])\.([0-9]+)$/.exec(location.hash || '');
    if (tm) { const ci = parseInt(tm[1], 10) - 1, ti = parseInt(tm[2], 10);
      loadChapter(ci+1).then(function(){ App.views.verses(ci, ti); }).catch(function(){ gitaLoadFail(); }); return; }
    var m = /^#chapter=([1-9]|1[0-8])(&tab=(mula|full|study|chapter|learn))?$/.exec(location.hash || '');
    if(m){ const ci = parseInt(m[1], 10) - 1; const tb = m[3];
      loadChapter(ci+1).then(function(){
        if(tb === 'learn'){ App.learn.show(ci); }
        else { App.views.chapter(ci); }  /* full/mula/study/chapter all merge into the one chapter view */
      }).catch(function(){ gitaLoadFail(); }); return; }
    var h = location.hash || '';
    if(h === '#play'){ App.play.show(); return; }
    if(h === '#favorites'){ App.library.showFavorites(); return; }
    if(h === '#search'){ App.library.search(); return; }
    if(h === '#data'){ App.data.show(); return; }
    if(h === '#ways'){ App.views.sections(); return; }
    var wy = /^#way=([123])$/.exec(h);
    if(wy){ App.views.chapters(+wy[1]); return; }
    var stay = '';
    try{ stay = sessionStorage.getItem('gita.route')||''; }catch(e){}
    if(stay==='#play'){ App.play.show(); return; }
    if(stay==='#favorites'){ App.library.showFavorites(); return; }
    if(stay==='#search'){ App.library.search(); return; }
    if(stay==='#data'){ App.data.show(); return; }
    if(stay==='#ways'){ App.views.sections(); return; }
    var sw = /^#way=([123])$/.exec(stay);
    if(sw){ App.views.chapters(+sw[1]); return; }
    var sm = /^#chapter=([1-9]|1[0-8])(&tab=(mula|full|study|chapter|learn))?$/.exec(stay);
    if(sm){
      const ci = parseInt(sm[1],10)-1, tb=sm[3];
      loadChapter(ci+1).then(function(){
        if(tb==='learn') App.learn.show(ci);
        else App.views.chapter(ci);
      }).catch(function(){ gitaLoadFail(); }); return;
    }
    var st = /^#theme=([1-9]|1[0-8])\.([0-9]+)$/.exec(stay);
    if(st){
      const ci=parseInt(st[1],10)-1, ti=parseInt(st[2],10);
      loadChapter(ci+1).then(function(){ App.views.verses(ci, ti); }).catch(function(){ gitaLoadFail(); }); return;
    }
    App.views.welcome();
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
