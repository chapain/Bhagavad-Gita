// pāda display: Devanagari block with pādas on separate lines (speakers inline)
function pDanda(i, total){
  if(total === 2) return (i===0) ? ' ।' : ' ॥';
  return (i%4===1)?' ।':((i%4===3)?' ॥':'');
}
function pDandaLatn(i, total){
  if(total === 2) return (i===0) ? ' |' : ' ||';
  return (i%4===1)?' |':((i%4===3)?' ||':'');
}
/* verseLines(): two lines in source order, plus any speaker. */
function padaBlockDeva(s, withNum){
  /* withNum: number inside the final line's closing daṇḍas — ॥ १.२५ ॥ */
  const ls = verseLines(s), last = ls.reduce((a,it,i)=> it.k === 's' ? a : i, -1);
  let html = withNum ? '<div class="m-vlines">' : '', li = 0;
  for(let i = 0; i < ls.length; i++){
    const it = ls[i];
    if(it.k === 's'){
      html += `<span class="spk">${it.d}</span>`;
      if(it.t) html += `<span class="spk-iast" lang="sa-Latn">${esc(it.t)}</span>`;
      continue;
    }
    const marker = li ? '॥' : '।';
    if(withNum){
      const hasNumber = i === last;
      const number = hasNumber
        ? `<span class="gl-tail"> <span class="gl-n">${esc(fmtNL(s.n))}</span> ॥</span>`
        : '';
      html += `<div class="gline"><span class="gline-main${hasNumber?' has-number':''}">${it.d}${marker}${number}</span></div>`;
    } else {
      html += `<div class="gline">${it.d}${marker}</div>`;
    }
    if(it.t) html += `<div class="giast" lang="sa-Latn">${esc(it.t)}</div>`;
    li++;
  }
  if(withNum) html += '</div>';
  return html;
}
/* Two lines, never three: shrink --verse-fit until each line's text fits
   the card's inner width (not the line's clientWidth: 0 inline on phones,
   shrink-to-fit on desktop). The numbered line reserves the number's real
   reach past the text - its gap plus its width - measured, so the same
   formula fits the desktop tail (out of flow after the daṇḍa) and the phone
   one (in flow, so the centred block carries it). +1px tolerance. */
function fitWholeVerse(){
  const v = $('#modal .m-whole-verse');
  if(!v || !v.clientWidth) return;
  const pf = parseFloat, ms = [...v.querySelectorAll('.gline-main')],
    r = document.createRange(), cs = getComputedStyle(v);
  /* inner width: clientWidth less padding and the card's 1px borders */
  const inner = v.clientWidth - pf(cs.paddingLeft) - pf(cs.paddingRight) - 2;
  const over = () => ms.some(el => { if(!el.firstChild) return false;
    r.selectNode(el.firstChild);
    const tr = r.getBoundingClientRect(), tail = el.querySelector('.gl-tail');
    /* how far the number reaches past the text: the gap plus its width */
    const num = tail ? tail.getBoundingClientRect().right - tr.right : 0;
    return tr.width > inner - num + 1; });
  let f = 1;
  while(true){ v.style.setProperty('--verse-fit', f.toFixed(2));
    if(f <= 0.3 || !over()) break; f -= 0.02; }
}
addEventListener('resize', fitWholeVerse);
if(document.fonts) document.fonts.ready.then(fitWholeVerse);

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
    const s = App.library.entryAt(DATA[state.chapter].themes[state.theme], state.idx).s;
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
  const next = {chapter:ci, theme:ti, idx:si, mode:mode,
    gpos:Math.max(0, App.library.indexOf(ci,ti,si))};
  if(mode === 'theme'){
    const b = themeBounds(DATA[ci].themes[ti]);
    next.pStart = b.start; next.pEnd = b.end;
  } else if(mode === 'search'){ next.mode = 'book'; }
  else if(mode === 'fav'){
    next.navList = App.library.favoriteLocations(); next.navIdx = navIdx || 0;
  }
  App.session.update(next);
  fillModal();
  bg.classList.add('open'); bg.setAttribute('aria-hidden','false');
  document.body.classList.add('modal-open');
  setAppInert(true); document.body.style.overflow='hidden';
  fitWholeVerse();
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
  App.views.persist();
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
  const n = App.library.entryAt(DATA[state.chapter].themes[state.theme], state.idx).s.n;
  return root + '/chapter/' + n.split('.')[0] + '/#v' + n;
}
function openSharePanel(){
  closeVerseMenu();
  $('#spLink').textContent = shareUrl();
  const p = $('#sharePanel');
  p.style.display = (p.style.display === 'flex') ? 'none' : 'flex';
}
function closeSharePanel(){ const p=$('#sharePanel'); if(p) p.style.display='none'; }
function copyTextToClipboard(t, msgKey){
  function copied(){
    const p = $('#sharePanel'); if(p) p.style.display = 'none';
    const sh = $('#shareBtn');
    if(sh){ sh.textContent = L(msgKey || 'link_copied');
      setTimeout(function(){ sh.textContent = L('share'); }, 1600); }
  }
  try { navigator.clipboard.writeText(t).then(copied, copied); }
  catch(e){ const ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta);
    ta.select(); try{ document.execCommand('copy'); }catch(e2){} ta.remove(); copied(); }
}
function copyVerseLink(){
  copyTextToClipboard($('#spLink').textContent, 'link_copied');
}
function verseShareText(){
  const ch = DATA[state.chapter], t = ch.themes[state.theme];
  const {s, part} = App.library.entryAt(t, state.idx);
  const lines = [L('verse') + ' ' + fmtNL(s.n) + ' — ' + T(part.titles), s.d];
  if(state.lang === 'en' && s.t) lines.push(s.t);
  lines.push(T(s.lits), T(s.paras), shareUrl());
  return lines.filter(Boolean).join('\n\n');
}
function copyVerseText(){
  copyTextToClipboard(verseShareText(), 'verse_copied');
}
function recentVersesLoad(){
  try{
    const a = JSON.parse(sessionStorage.getItem('gitaRecentVerses') || '[]');
    return Array.isArray(a) ? a.filter(x => typeof x === 'string' && /^\d{1,2}\.\d{2}$/.test(x)).slice(0, 6) : [];
  }catch(e){ return []; }
}
function recentVersesRecord(id){
  if(!/^\d{1,2}\.\d{2}$/.test(id)) return;
  const next = [id, ...recentVersesLoad().filter(x => x !== id)].slice(0, 6);
  try{ sessionStorage.setItem('gitaRecentVerses', JSON.stringify(next)); }catch(e){}
}
function recentVersesHtml(curId){
  const list = recentVersesLoad().filter(x => x !== curId).slice(0, 5);
  if(!list.length) return '';
  return `<div class="m-recent"><span class="m-rec-lbl">${esc(L('recent_verses'))}:</span>${list.map(id =>
    `<button type="button" class="srch-chip" onclick="App.reader.openId('${esc(id)}')">${esc(fmtNL(id))}</button>`
  ).join('')}</div>`;
}
function openVerseById(id){
  let loc = App.library.location(id);
  if(!loc){
    const n = parseInt(String(id).split('.')[0], 10);
    if(n >= 1 && n <= 18) loadChapter(n).then(()=>openVerseById(id)).catch(gitaLoadFail);
    return;
  }
  openModal(loc.ci, loc.ti, loc.si, state.mode || 'theme');
}
/* ---------- mobile: Android hardware / iOS swipe "back" closes the verse sheet ---------- */
let MODAL_HIST = false, MODAL_POPPING = false, MODAL_RETURN_FOCUS = null;
function pushModalHistory(){
  if(MODAL_HIST) return;
  try{ sessionStorage.setItem('gita.preModalHash', App.views.hash()); }catch(e){}
  try{ history.pushState({gitaModal:true}, ''); MODAL_HIST = true; }catch(e){}
}
function popModalHistory(){
  if(!MODAL_HIST) return;
  MODAL_HIST = false;
  if(MODAL_POPPING) return;               // we got here *from* popstate — nothing to unwind
  try{ history.back(); }catch(e){}
  App.views.persist();
}
window.addEventListener('popstate', ()=>{
  if($('#modalBg').classList.contains('open')){
    MODAL_POPPING = true; closeModal(); MODAL_POPPING = false;
  }
});

function fillModal(){
  const ch = DATA[state.chapter], t = ch.themes[state.theme];
  const {s, part} = App.library.entryAt(t, state.idx);
  let partIdx = 0; { let acc = 0;
    for(let pi=0; pi<t.parts.length; pi++){ const len = t.parts[pi].sutras.length;
      if(state.idx >= acc && state.idx < acc+len){ partIdx = pi; break; } acc += len; } }
  if(state.gpos == null) App.session.update({gpos:Math.max(0, App.library.indexOf(state.chapter,state.theme,state.idx))});
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
    const peek = (pad.words||[]).map(w => w[0] + ' — ' + (w[2+LI] || w[2])).join(' · ');
    return `<div class="pada-box">
      <button type="button" class="pada-toggle" title="${esc(peek)}" aria-expanded="false" aria-controls="${id}" aria-describedby="padaHint" onclick="toggleWords(this)">
        <span class="pb-top"><span class="pb-num">${esc(L('pada_label'))} ${numL(idx+1)}</span></span>
        <span class="pb-deva" lang="sa">${pad.d}${pDanda(idx,total)}</span>
        <span class="pb-iast" lang="sa-Latn">${esc(pad.t)}${pDandaLatn(idx,total)}</span>
      </button>${wordsHtml(pad,id)}
    </div>`;
  }
  recentVersesRecord(s.n);
  const isSaved = App.library.isFavorite(s.n);
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
      <button type="button" role="menuitem" class="${isSaved?' saved':''}" id="favBtn" aria-pressed="${isSaved}" onclick="App.library.toggleFavorite('${s.n}')">${isSaved?ICONS.starF:ICONS.star} ${esc(isSaved?L('saved_verse'):L('save_verse'))}</button>
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
      <button class="sp-copy sp-copy-txt" id="shCpTxt" onclick="copyVerseText()">${esc(L('copy_verse_text'))}</button>
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
      ${recentVersesHtml(s.n)}
    </div>
    <div class="m-tail" aria-hidden="true"></div>
    <div class="m-nav">
      ${state.mode==='random'
        ? `<button class="m-random" onclick="App.library.randomVerse()">${ICONS.shuffle}<span>${esc(L('next_random'))}</span></button>`
        : state.mode==='theme'
          ? `<button onclick="navSutra(-1)" ${(state.idx>state.pStart||state.theme>0)?'':'disabled'}>${(state.idx===state.pStart && state.theme>0)?L('prev_theme'):L('previous')}</button>
             <span class="m-count">${Lof(state.idx-state.pStart+1, state.pEnd-state.pStart+1)}</span>
             ${state.idx===state.pEnd && state.theme===DATA[state.chapter].themes.length-1
               ? `<button class="m-back" onclick="backToTheme()">${esc(L('back_to_theme'))}</button>`
               : `<button onclick="navSutra(1)">${state.idx===state.pEnd?L('next_theme'):L('next')}</button>`}`
          : state.mode==='book'
          ? `<button onclick="navSutra(-1)" ${state.gpos>0?'':'disabled'}>${L('previous')}</button>
             <span class="m-count">${Lof(state.gpos+1, App.library.count())}</span>
             <button onclick="navSutra(1)" ${state.gpos<App.library.count()-1?'':'disabled'}>${L('next')}</button>`
          : `<button onclick="navSutra(-1)" ${(state.navIdx||0)>0?'':'disabled'}>${L('previous')}</button>
             <span class="m-count">${Lof((state.navIdx||0)+1, state.navList?state.navList.length:1)}</span>
             <button onclick="navSutra(1)" ${(state.navIdx||0) < (state.navList?state.navList.length-1:0)?'':'disabled'}>${L('next')}</button>`}
    </div>`;
  applyReaderSize();
  fitWholeVerse();
}
function setReaderSize(size){
  if(!READER_SIZES.includes(size)) return;
  App.session.update({readerSize:size});
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
  fitWholeVerse();
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
  let chapter=state.chapter, theme=state.theme, idx=state.idx,
      gpos=state.gpos, navIdx=state.navIdx, pStart=state.pStart, pEnd=state.pEnd;
  if(state.mode === 'theme'){
    const n = idx + d;
    if(n >= pStart && n <= pEnd) idx = n;
    else if(d > 0 && theme + 1 < DATA[chapter].themes.length){
      theme += 1;
      const b = themeBounds(DATA[chapter].themes[theme]);
      pStart = b.start; pEnd = b.end; idx = b.start;
    } else if(d < 0 && theme > 0){
      theme -= 1;
      const b = themeBounds(DATA[chapter].themes[theme]);
      pStart = b.start; pEnd = b.end; idx = b.end;
    } else return;
  } else if(state.mode === 'book'){
    gpos = Math.max(0, Math.min(App.library.count()-1, (gpos || 0) + d));
    const loc = App.library.locationAt(gpos);
    chapter = loc.ci; theme = loc.ti; idx = loc.si;
  } else if((state.mode === 'fav') && state.navList){
    const k = (navIdx || 0) + d;
    if(k < 0 || k >= state.navList.length) return;
    navIdx = k;
    const loc = state.navList[k];
    chapter = loc.ci; theme = loc.ti; idx = loc.si;
  } else return;
  gpos = Math.max(0, App.library.indexOf(chapter,theme,idx));
  App.session.update({chapter, theme, idx, gpos, navIdx, pStart, pEnd});
  fillModal();
  updateModalAddress();
  saveSessionSnapshot();
  const title = $('#modalTitle'); if(title) title.focus({preventScroll:true});
  const m = $('#modal'); if(m) m.scrollTo({top:0, behavior:'smooth'});
}
function backToTheme(){ closeModal(); App.views.verses(state.chapter, state.theme); }
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
  if(state.view === 'learn' && App.learn.canNavigate()){
    if(e.key==='ArrowLeft'){ e.preventDefault(); App.learn.navigate(-1); }
    if(e.key==='ArrowRight'){ e.preventDefault(); App.learn.navigate(1); }
  }
});



/* Reader owns the verse sheet and scripture presentation helpers used by cards. */
App.reader = Object.freeze({
  open: openModal,
  openId: openVerseById,
  close: closeModal,
  restore: restoreModalSession,
  refresh: fillModal,
  navigate: navSutra,
  shareText: verseShareText,
  padaBlock: padaBlockDeva
});
