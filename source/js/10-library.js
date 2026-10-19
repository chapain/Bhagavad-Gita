// ---------- global verse index (search / favorites / random) ----------
const VERSES = [];
let SRCH_HITS = [], FAV_LIST = [];
function flatIndex(t,p,s){ let idx=0; for(const pp of t.parts){ if(pp===p) return idx+s; idx+=pp.sutras.length; } return idx; }
function sutraAt(t,i){ for(const p of t.parts){ if(i < p.sutras.length) return {s:p.sutras[i], part:p}; i-=p.sutras.length; } return {s:t.parts[t.parts.length-1].sutras[0], part:t.parts[t.parts.length-1]}; }
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
function recentLoad(){
  try{
    const a = JSON.parse(localStorage.getItem('gitaRecent') || '[]');
    return Array.isArray(a) ? a.filter(x => typeof x === 'string' && x.trim().length >= 2 && x.length <= 40).slice(0, 6) : [];
  }catch(e){ return []; }
}
function recentSave(q){
  q = String(q || '').trim();
  if(q.length < 2 || q.length > 40) return;
  const next = [q, ...recentLoad().filter(x => x.toLowerCase() !== q.toLowerCase())].slice(0, 6);
  try{ localStorage.setItem('gitaRecent', JSON.stringify(next)); }catch(e){}
}
function hlSearchText(text, q){
  const s = String(text || ''), needle = String(q || '').trim();
  if(needle.length < 2 || /^\d/.test(digitNorm(needle))) return esc(s);
  const re = new RegExp(needle.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
  let out = '', last = 0, m;
  while((m = re.exec(s)) !== null){
    out += esc(s.slice(last, m.index)) + '<mark class="srch-hl">' + esc(m[0]) + '</mark>';
    last = m.index + m[0].length;
    if(!m[0].length) break;
  }
  return out + esc(s.slice(last));
}
function srchChipsHtml(q, hitCount){
  const cur = String(q || '').trim().toLowerCase();
  const rec = recentLoad().filter(x => x.toLowerCase() !== cur);
  const items = hitCount === 0
    ? [...new Set([...rec, numL('2.47'), numL('4.7'), numL('18.66'), 'धर्मक्षेत्रे'])].slice(0, 6)
    : rec.slice(0, 5);
  if(!items.length) return '';
  const lbl = hitCount > 0 ? `<span class="srch-chips-lbl">${esc(L('search_recent'))}:</span>` : '';
  return `<div class="srch-chips fade-in">${lbl}${items.map(x =>
    `<button type="button" class="srch-chip" data-q="${esc(x)}" onclick="App.library.pickSearch(this.dataset.q)">${esc(x)}</button>`
  ).join('')}</div>`;
}
function pickSearch(q){
  const inp = $('#searchInput');
  if(!inp) return;
  inp.value = String(q || '');
  searchX();
  doSearch();
}
function doSearch(){
  if(!allChReady()){ loadAllChapters().then(doSearch); return; }
  const q = ($('#searchInput').value || '').trim();
  if(!q){ clearSearch(); return; }
  SRCH_HITS = [];
  rememberOrigin();
  App.session.update({view:'search', chapter:null, theme:null}); App.views.persist(); App.views.renderCrumbs();
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
      <div class="view-sub fade-in">${esc(L('no_results'))}</div>
      <div class="srch-empty-hint fade-in">${esc(L('search_try'))}</div>
      ${srchChipsHtml(q, 0)}`;
    announceView();
    return;
  }
  recentSave(q);
  SRCH_HITS = hits;
  view.innerHTML = `<div class="res-head fade-in" role="heading" aria-level="2">${esc(L('search_results'))}</div>
    <div class="res-count fade-in">${esc(resultCountLabel(hits.length))}</div>
    ${srchChipsHtml(q, hits.length)}
    <div class="grid verses fade-in">${hits.map((loc,i)=>{
      const ch = DATA[loc.ci], v = verseAt(loc);
      const th = ch.themes[loc.ti]; const part = sutraAt(th, loc.si).part;
      const pi = th.parts.indexOf(part);
      return `<div class="mini" role="button" tabindex="0" onclick="App.reader.open(${loc.ci},${loc.ti},${loc.si},'search',${i},this)">
        <div class="vnum">${esc(L('verse'))} ${esc(fmtNL(v.n))}</div>
        <div class="m-topic"><span class="mt-lab">${esc(L('verse_topic'))}:</span> ${hlSearchText(T(part.titles), q)}</div>
        <div class="padas" lang="sa">${App.reader.padaBlock(v)}</div>
        <div class="vhint">${hlSearchText(T(v.paras), q)}</div>
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
   takes over, remember the browsing position so App.views.renderCrumbs() can offer it as a
   real trail. Only recorded when leaving an actual browsing view, so repeatedly
   tapping Favorites doesn't overwrite the origin with itself. */
function rememberOrigin(){
  if(['welcome','sections','chapters','chapter'].includes(state.view)){
    App.session.update({origin:{view:state.view, section:state.section,
      chapter:state.chapter, theme:state.theme}});
  }
}
function goToOrigin(){
  const o = state.origin;
  if(!o){ App.views.sections(); return; }
  $('#searchInput').value = '';
  if(o.view === 'welcome') App.views.welcome();
  else if(o.view === 'sections') App.views.sections();
  else if(o.view === 'chapter' && o.chapter != null)
    App.views.chapter(o.chapter, o.theme == null ? undefined : o.theme);
  else if(o.section != null) App.views.chapters(o.section);
  else App.views.sections();
}
function showFavorites(){
  if(!allChReady()){ loadAllChapters().then(showFavorites); return; }
  rememberOrigin();
  App.session.update({view:'favorites', chapter:null, theme:null}); App.views.persist(); App.views.renderCrumbs();
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
      return `<div class="res-card" onclick="App.reader.open(${loc.ci},${loc.ti},${loc.si},'fav',${i},this.querySelector('.res-open'))">
        <button type="button" class="sr-only focusable res-open" aria-label="${esc(L('open_verse'))} ${esc(fmtNL(v.n))}"
          onclick="event.stopPropagation();App.reader.open(${loc.ci},${loc.ti},${loc.si},'fav',${i},this)"></button>
        <div class="res-top"><span class="res-num">${esc(fmtNL(v.n))}</span><span class="res-title">${esc(T(ch.names))}</span>
        <span class="fav-tools" onclick="event.stopPropagation()">
          <button class="fav-move" onclick="moveFav(${i},-1)" ${i===0?'disabled':''} aria-label="${esc(L('fav_move_up'))}" title="${esc(L('fav_move_up'))}">${L('fav_up')}</button>
          <button class="fav-move" onclick="moveFav(${i},1)" ${i===saved.length-1?'disabled':''} aria-label="${esc(L('fav_move_down'))}" title="${esc(L('fav_move_down'))}">${L('fav_down')}</button>
          <button class="res-remove" onclick="removeFav('${esc(v.n)}')">${esc(L('remove_fav'))}</button>
        </span></div>
        <div class="res-deva" lang="sa">${App.reader.padaBlock(v)}</div>
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
  App.reader.open(v.ci, v.ti, v.si, 'random');
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


/* Public Library boundary. Mutable indexes and saved-list navigation stay in
   this file; Reader and routing consume snapshots and lookup operations rather
   than reaching into those arrays directly. */
App.library = Object.freeze({
  location: verseLoc,
  verse: verseAt,
  entryAt: sutraAt,
  assemble: assembleData,
  onSearchInput,
  syncSearchControl: searchX,
  paintTheme,
  rememberOrigin,
  search: doSearch,
  pickSearch,
  clearSearch,
  randomVerse,
  showFavorites,
  toggleFavorite: toggleFav,
  indexOf(ci, ti, si){ return VERSES.findIndex(e=>e.ci===ci && e.ti===ti && e.si===si); },
  locationAt(index){ return VERSES[index] || null; },
  count(){ return VERSES.length; },
  ready: allChReady,
  isFavorite(id){ return FAV.includes(id); },
  favoriteLocations(){ return FAV_LIST.slice(); }
});
