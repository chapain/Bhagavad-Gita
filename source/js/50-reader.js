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
  /* Everything focusable behind the sheet: the skip link, the header, the phone
     toolbar, the phone tab bar, the page and the footer. The CSS only dims
     .tabbar (pointer-events:none, opacity .4), which stops a finger but not the
     Tab key or a screen reader — focus could land on furniture the reader cannot
     see. .atm is a decorative SVG (aria-hidden, pointer-events:none), so it stays. */
  document.querySelectorAll('body > .skip-link, body > header, body > .toolbar,'
    + ' body > nav.tabbar, body > .wrap, body > footer')
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
function copiedFeedback(msgKey){
  const p = $('#sharePanel'); if(p) p.style.display = 'none';
  const sh = $('#shareBtn');
  if(sh){ sh.textContent = L(msgKey || 'link_copied');
    setTimeout(function(){ sh.textContent = L('share'); }, 1600); }
}
function copyTextToClipboard(t, msgKey){
  function copied(){ copiedFeedback(msgKey); }
  try { navigator.clipboard.writeText(t).then(copied, copied); }
  catch(e){ const ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta);
    ta.select(); try{ document.execCommand('copy'); }catch(e2){} ta.remove(); copied(); }
}
function copyVerseLink(){
  copyTextToClipboard($('#spLink').textContent, 'link_copied');
}
/* D1: the copy follows the reader's language — Devanagari, IAST only where the
   app shows it (en), the literal in that language, then the link. Not the
   paraphrase: a verse in a chat, not an essay. Rationale: PROJECT.md. */
function verseShareParts(){
  const ch = DATA[state.chapter], t = ch.themes[state.theme];
  const {s} = App.library.entryAt(t, state.idx);
  return {s: s, url: shareUrl()};
}
function verseShareText(){
  const {s, url} = verseShareParts();
  const lines = [L('verse') + ' ' + fmtNL(s.n), s.d];
  if(state.lang === 'en' && s.t) lines.push(s.t);
  lines.push(T(s.lits), url);
  return lines.filter(Boolean).join('\n\n');
}
/* The same verse as formatted text, so Notes, Docs, a chat and the reader's
   own email paste it as a verse with a heading and a real link rather than as
   a run-on paragraph. Deliberately plain markup: chat apps strip CSS and a
   pasted stylesheet would only make the recipient's client do extra work. */
function verseShareHtml(){
  const {s, url} = verseShareParts();
  const lit = state.lang === 'en' ? 'en' : state.lang;
  let h = '<p><strong>' + esc(L('verse') + ' ' + fmtNL(s.n)) + '</strong></p>'
        + '<p lang="sa">' + esc(s.d) + '</p>';
  if(state.lang === 'en' && s.t) h += '<p lang="sa-Latn"><em>' + esc(s.t) + '</em></p>';
  h += '<p lang="' + lit + '">' + esc(T(s.lits)) + '</p>'
     + '<p><a href="' + esc(url) + '">' + esc(L('verse') + ' ' + fmtNL(s.n)) + '</a></p>';
  return h;
}
function copyVerseText(){
  const plain = verseShareText();
  /* ClipboardItem is written synchronously inside the click: iOS Safari drops
     the permission if anything is awaited first. Where the API or the MIME
     support is missing (older Firefox, any odd webview) we fall back to the
     plain-text path that has always worked — never leave the reader with a
     dead button and a silent failure. */
  if(window.ClipboardItem && navigator.clipboard && navigator.clipboard.write){
    try{
      const item = new ClipboardItem({
        'text/html': new Blob([verseShareHtml()], {type:'text/html'}),
        'text/plain': new Blob([plain], {type:'text/plain'})
      });
      navigator.clipboard.write([item]).then(
        function(){ copiedFeedback('verse_copied'); },
        function(){ copyTextToClipboard(plain, 'verse_copied'); }
      );
      return;
    }catch(e){ /* fall through to plain text */ }
  }
  copyTextToClipboard(plain, 'verse_copied');
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
    const ws = it.words || [];
    /* The glosses ride with the rows as JSON: a verse has several word
       containers (four pādas plus speaker lines), so a global would be
       overwritten by whichever rendered last. */
    return `<div class="words" id="${id}" data-words="${esc(JSON.stringify(ws))}">${ws.map((w,i)=>`<div class="wrow" role="button" tabindex="0" data-wi="${i}" aria-expanded="false"><span class="wdeva" lang="sa">${w[0]}</span><span class="wiast" lang="sa-Latn">${esc(w[1])}</span><span class="wmean">${esc(w[2+LI] || w[2])}</span></div>`).join('')}</div>`;
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
  /* A note belongs to the verse, not to the saved list — every verse can carry
     one, and it is kept whether or not the verse is a favourite. */
  const noteText = App.library.note(s.n);

  /* Option 1: the whole verse and the four-quarter grid are both prepared up
     front, then swapped into the same box by toggleVerseExpansion(). */
  /* Both shapes carry their own short instruction, drawn from the two
     existing UI keys: the whole verse says how to open the four pādas, the
     expanded card says how to open a pāda's word meanings. Both hints sit
     inside #verseContent — never in a sibling bar or a second card — and the
     expanded one is a plain line above the grid, so it adds no disclosure. */
  const wholeVerseHtml = `${padaBlockDeva(s, true)}
      <span class="verse-expand-hint" aria-hidden="true">${esc(L('click_hint_pada'))}</span>`;
  const padaGridHtml = `<span class="sr-only" id="wordsHint">${esc(L('click_pada_meanings'))}</span>
      <span class="sr-only" id="padaHint">${esc(L('click_pada_meanings'))}</span>
      <button type="button" class="m-verse-back" aria-label="${esc(L('back_to_x').replace('{x}', L('verse')))}" title="${esc(L('back_to_x').replace('{x}', L('verse')))}" onclick="event.stopPropagation();App.reader.toggleVerseExpansion(event)">↩</button>
      ${spkHtml(topS)}
      <p class="pada-meanings-hint">${esc(L('click_pada_meanings'))}</p>
      <div class="pada-grid">
        <div class="pada-row">${boxHtml(pads[0],0,pads.length)}${boxHtml(pads[1],1,pads.length)}</div>
        ${midS.length ? `<div class="spk-mid">${spkHtml(midS)}</div>` : ''}
        ${pads.length===4 ? `<div class="pada-row">${boxHtml(pads[2],2,4)}${boxHtml(pads[3],3,4)}</div>` : ''}
      </div>`;
  verseViewState = { whole: wholeVerseHtml, expanded: padaGridHtml, isExpanded:false };
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
      <!-- img/share-art.jpg is the site's one painted face (960x504, repainted
           by build.py when Pillow is present). It earns its place here as the
           preview of what the copied link shows; the intrinsic width/height keep
           the panel from jumping, lazy loading keeps it off the first paint, and
           onerror removes it rather than showing a broken frame offline. -->
      <img class="sp-art" src="img/share-art.jpg" alt="" width="960" height="504"
           loading="lazy" decoding="async" onerror="this.remove()">
    </div>
    <div class="m-part">${esc(L('theme_sg'))} ${fmtRangeL(t.range)} · ${esc(T(t.titles))}</div>
    <div class="reader-copy">
      <div id="verseContainer" class="m-verse-box-container">
        <div id="verseContent" class="m-whole-verse" lang="sa" role="button" tabindex="0"
             aria-label="${esc(L('click_hint_pada'))}" aria-expanded="false"
             onclick="App.reader.toggleVerseExpansion(event)"
             onkeydown="if((event.key==='Enter'||event.key===' ')&&(event.target===this||!event.target.closest('.pada-toggle,.spk-line,.words,.m-verse-back'))){event.preventDefault();App.reader.toggleVerseExpansion(event)}">
          ${wholeVerseHtml}
        </div>
      </div>
      <div class="m-line lit"><span class="lb">${L('literal')}</span><div class="lt">${esc(T(s.lits))}</div></div>
      <div class="m-line para"><span class="lb">${L('in_other_words')}</span><div class="lt">${esc(T(s.paras))}</div></div>
      <details class="m-note"${noteText ? ' open' : ''}>
        <summary><span>${esc(L('note_label'))}</span>${noteText ? `<span class="m-note-dot" aria-hidden="true">•</span>` : ''}<span class="m-note-chev" aria-hidden="true">▾</span></summary>
        <textarea rows="2" aria-label="${esc(L('note_label'))}" placeholder="${esc(L('note_ph'))}"
          oninput="this.style.height='auto';this.style.height=this.scrollHeight+'px';App.library.setNote('${esc(s.n)}', this.value)">${esc(noteText)}</textarea>
      </details>
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
  setVerseView(false);
  // grow the note box to its saved text, as the saved cards do
  const nt = $('#modal .m-note textarea');
  if(nt && nt.value){ nt.style.height='auto'; nt.style.height=nt.scrollHeight+'px'; }
}

function restoreModalSession(modalSnap){
  if(!modalSnap) return;
  const modal = document.getElementById('modal');
  /* Option 1: the quarters live in the converted verse box now, so rebuild
     that shape before the saved word-split ids can be re-applied. */
  if(modalSnap.verseExpanded) setVerseView(true);
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
/* ---------- D2: one word, all three glosses ----------
   It sits on the word rows, never the verse line: the printed verse is
   sandhi-joined (2.47 prints कर्मण्येवाधिकारस्ते as one token while its words
   are कर्मणि / एव / अधिकारः / ते), so a token cannot be mapped to a word
   without inventing a boundary. Tap, Enter/Space and contextmenu all reach it
   too — this is not a gesture-only feature. Full rationale: PROJECT.md. */
let PEEK_ROW = null, PEEK_BOX = null, PEEK_TIMER = 0, PEEK_DOWN = 0, PEEK_XY = null;

function langEndonym(l){
  /* The three endonyms are literals in the header switcher, not UI copy; read
     that one source rather than keeping a second copy of "नेपाली" in JS. */
  const b = document.querySelector('.lang-btn[data-lang="' + l + '"]');
  return b ? b.textContent.trim() : l;
}
function closeWordPeek(){
  if(PEEK_BOX && PEEK_BOX.parentNode) PEEK_BOX.parentNode.removeChild(PEEK_BOX);
  if(PEEK_ROW && PEEK_ROW.setAttribute) PEEK_ROW.setAttribute('aria-expanded','false');
  PEEK_BOX = null; PEEK_ROW = null;
}
function openWordPeek(row){
  if(!row || row === PEEK_ROW) return;
  closeWordPeek();
  const holder = row.closest ? row.closest('.words') : null;
  let ws = [];
  try{ ws = JSON.parse((holder && holder.getAttribute('data-words')) || '[]') || []; }
  catch(e){ return; }
  const w = ws[Number(row.getAttribute('data-wi')) || 0];
  if(!w) return;
  const lines = GITA_LANGS.map((l, i) =>
    `<span class="wp-line"><span class="wp-lang" lang="${l}">${esc(langEndonym(l))}</span>` +
    `<span lang="${l}">${esc(w[2 + i] || w[2])}</span></span>`).join('');
  const box = document.createElement('div');
  box.className = 'wpeek';
  box.setAttribute('role','status');
  box.innerHTML = (w[1] ? `<span class="wp-iast" lang="sa-Latn">${esc(w[1])}</span>` : '') + lines;
  row.parentNode.insertBefore(box, row.nextSibling);
  row.setAttribute('aria-expanded','true');
  PEEK_ROW = row; PEEK_BOX = box;
}
function toggleWordPeek(row){ if(row && row === PEEK_ROW) closeWordPeek(); else openWordPeek(row); }

document.addEventListener('pointerdown', e=>{
  const row = e.target && e.target.closest ? e.target.closest('.wrow') : null;
  if(!row){ closeWordPeek(); return; }
  if(e.pointerType === 'mouse' && e.button !== 0) return;
  PEEK_DOWN = Date.now(); PEEK_XY = [e.clientX, e.clientY];
  clearTimeout(PEEK_TIMER);
  /* 450 ms, and any move past 10 px cancels — a scroll flick must never open a
     peek halfway down the page. */
  PEEK_TIMER = setTimeout(function(){ PEEK_TIMER = 0; openWordPeek(row); }, 450);
}, true);
function peekPointerEnd(){ if(PEEK_TIMER){ clearTimeout(PEEK_TIMER); PEEK_TIMER = 0; } }
document.addEventListener('pointerup', peekPointerEnd, true);
document.addEventListener('pointercancel', peekPointerEnd, true);
document.addEventListener('pointermove', e=>{
  if(!PEEK_TIMER || !PEEK_XY) return;
  if(Math.abs(e.clientX - PEEK_XY[0]) > 10 || Math.abs(e.clientY - PEEK_XY[1]) > 10) peekPointerEnd();
}, true);
document.addEventListener('click', e=>{
  const row = e.target && e.target.closest ? e.target.closest('.wrow') : null;
  if(!row) return;
  /* A long press ends in a click as well; without this the peek would open and
     then close in the same gesture. */
  if(Date.now() - PEEK_DOWN > 400) return;
  toggleWordPeek(row);
});
document.addEventListener('contextmenu', e=>{
  const row = e.target && e.target.closest ? e.target.closest('.wrow') : null;
  if(!row) return;
  e.preventDefault(); peekPointerEnd(); openWordPeek(row);
});

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
    /* Escape closes the word peek first, so the sheet does not vanish while
       the reader is looking at one word. */
    if(e.key==='Escape' && PEEK_ROW){ closeWordPeek(); return; }
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
  padaBlock: padaBlockDeva,
  toggleVerseExpansion: toggleVerseExpansion
});
