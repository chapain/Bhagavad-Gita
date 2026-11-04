/* ==================== 12-search — the search screen ====================
   Split out of 10-library.js (2026-11-04) which kept the index, the saved list and
   this screen in 677 of the 700 lines the monolith guard allows. Builders it calls
   (prepareSearchQuery, searchTextMatches, SEARCH_PASSAGES, verseAt, sutraAt,
   allChReady) stay in 10-library.js, which loads first; it walks the index through
   versesMatching(). Results are owned here and read via srchAnnounced(). */
let SRCH_HITS = [];
/* Set only when C3 rescued a diacritic query onto its plain reading; read by
   the search render and by the screen-reader announcement, cleared otherwise. */
let SRCH_NOTE = '';
// ---------- search ----------
let searchTimer = null;
function onSearchInput(v){
  clearTimeout(searchTimer); searchTimer = setTimeout(doSearch, 220); searchX();
}
/* the in-field ✕ exists only while there is text to clear — the modern
   pattern; a standing "Clear" button was dead chrome on an empty field */
function searchX(){ const f = document.querySelector('.sw-field');
  if(f) f.classList.toggle('has-x', ($('#searchInput').value || '').length > 0); }
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
/* Zero results is the only place a chip earns its space: four real starting
   points the book actually contains. Recent queries are deliberately NOT a
   chip source any more — a live search screen that offers the reader's own past
   queries back while they type a new one is noise stacked on noise, and every
   keystroke of the previous search had been stored as its own "recent". */
function srchChipsHtml(){
  const items = [numL('2.47'), numL('4.7'), numL('18.66'), 'धर्मक्षेत्रे'];
  return `<div class="srch-chips fade-in">${items.map(x =>
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

/* Free text searched more than the verse line: the phrase may come from a word
   gloss, which the card does not otherwise show, so name the word that matched
   rather than leaving the reader to wonder why a verse is in the list. */
function glossHit(s, q){
  const LI = {en:0, ne:1, hi:2}[state.lang] || 0;
  for(const f of (s.flow || [])) for(const w of (f.words || [])){
    for(const k of [2 + LI, 2]){
      const g = w[k];
      if(g && searchTextMatches(searchExactKey(g), '', q)) return [w[0], g];
    }
  }
  return null;
}
function passageHits(nq, nqd){
  const out = [];
  SEARCH_PASSAGES.forEach(p=>{
    if(searchTextMatches(p.exact, p.folded, nq)
       || (nqd.exact !== nq.exact && searchTextMatches(p.exact, p.folded, nqd))) out.push(p);
  });
  return out;
}
function resGroupHtml(label, count, inner){
  return `<div class="res-group fade-in"><div class="res-gl"><span>${esc(label)}</span>`
    + `<span class="res-gn">${numL(count)}</span></div>${inner}</div>`;
}
function passageCard(p, q){
  if(p.kind === 'chapter'){
    const ch = DATA[p.ci];
    return `<div class="res-passage" role="button" tabindex="0" onclick="App.views.chapter(${p.ci})">
      <div class="rp-top"><span class="rp-kind">${esc(L('chapter'))} ${numL(ch.num)}</span></div>
      <div class="rp-title">${hlSearchText(T(ch.names), q)}</div>
      <div class="rp-sub">${hlSearchText(T(ch.subs), q)}</div></div>`;
  }
  const ch = DATA[p.ci], t = ch.themes[p.ti];
  return `<div class="res-passage" role="button" tabindex="0" onclick="App.views.chapter(${p.ci},${p.ti})">
    <div class="rp-top"><span class="rp-kind">${esc(L('theme_sg'))} ${numL(p.ti+1)}</span>
      <span class="rp-rng">${esc(fmtRangeL(t.range))}</span></div>
    <div class="rp-title">${hlSearchText(T(t.titles), q)}</div>
    <div class="rp-sub">${esc(L('chapter'))} ${numL(ch.num)} · ${hlSearchText(T(ch.names), q)}</div></div>`;
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
  let hits, passages = [];
  if(num){
    const target = parseInt(num[1],10) + '.' + parseInt(num[2],10);
    hits = versesMatching(loc => loc.norm === target);
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
    hits = versesMatching((loc, exact, folded) =>
      searchTextMatches(exact, folded, nq) ||
      (nqd.exact !== nq.exact && searchTextMatches(exact, folded, nqd)));
    passages = passageHits(nq, nqd);
  }
  /* C3: a marked query that found nothing is almost always a slip on one
     vowel, not a word the book lacks. Re-run the same search on the plain
     reading before declaring zero. The results are real, so the count stays
     honest and the reader is told why the screen changed. */
  SRCH_NOTE = '';
  let total = hits.length + passages.length;
  if(total === 0){
    const alt = searchFoldAlternative(q);
    if(alt){
      const altHits = versesMatching((loc, exact, folded) =>
        searchTextMatches(exact, folded, alt));
      const altPassages = passageHits(alt, alt);
      if(altHits.length + altPassages.length){
        hits = altHits; passages = altPassages; total = hits.length + passages.length;
        SRCH_NOTE = L('search_meant').replace('{q}', q);
      }
    }
  }
  if(total === 0){
    view.innerHTML = `<div class="res-head fade-in" role="heading" aria-level="2">${esc(L('search_results'))}</div>
      <div class="res-count fade-in">${esc(resultCountLabel(0))}</div>
      <div class="view-sub fade-in">${esc(L('no_results'))}</div>
      <div class="srch-empty-hint fade-in">${esc(L('search_try'))}</div>
      ${srchChipsHtml()}`;
    announceView();
    return;
  }
  SRCH_HITS = hits;
  const themes = passages.filter(p=>p.kind === 'theme'),
        chapters = passages.filter(p=>p.kind === 'chapter'),
        groups = (hits.length?1:0) + (themes.length?1:0) + (chapters.length?1:0);
  const verseGrid = `<div class="grid verses">${hits.map((loc,i)=>{
      const ch = DATA[loc.ci], v = verseAt(loc);
      const th = ch.themes[loc.ti]; const part = sutraAt(th, loc.si).part;
      const wm = glossHit(v, nq);
      const shown = searchTextMatches(searchExactKey(T(part.titles) + ' ' + T(v.paras) + ' ' + v.d), '', nq);
      return `<div class="mini" role="button" tabindex="0" onclick="App.reader.open(${loc.ci},${loc.ti},${loc.si},'search',${i},this)">
        <div class="vnum">${esc(L('verse'))} ${esc(fmtNL(v.n))}</div>
        <div class="m-topic"><span class="mt-lab">${esc(L('verse_topic'))}:</span> ${hlSearchText(T(part.titles), q)}</div>
        <div class="padas" lang="sa">${App.reader.padaBlock(v)}</div>
        <div class="vhint">${hlSearchText(T(v.paras), q)}</div>
        ${wm && !shown ? `<div class="res-word">${esc(L('search_word_match').replace('{w}', wm[0] + ' — ' + wm[1]))}</div>` : ''}
      </div>`;}).join('')}</div>`;
  const passageGrid = list => `<div class="grid passages">${list.map(p=>passageCard(p, q)).join('')}</div>`;
  view.innerHTML = `<div class="res-head fade-in" role="heading" aria-level="2">${esc(L('search_results'))}</div>
    <div class="res-count fade-in">${esc(resultCountLabel(total))}</div>
    ${SRCH_NOTE ? `<div class="view-sub srch-relaxed fade-in">${esc(SRCH_NOTE)}</div>` : ''}
    ${hits.length
      ? (groups > 1 ? resGroupHtml(L('search_in_verses'), hits.length, verseGrid) : verseGrid)
      : ''}
    ${themes.length ? resGroupHtml(L('search_in_themes'), themes.length, passageGrid(themes)) : ''}
    ${chapters.length ? resGroupHtml(L('search_in_chapters'), chapters.length, passageGrid(chapters)) : ''}`;
  announceView();
}
function clearSearch(){
  $('#searchInput').value = '';
  searchX();
  goToOrigin();
}

/* Library's announceView speaks the count and the relaxed-query note; both are
   this module's state, so the read travels through a function. */
function srchAnnounced(){
  return resultCountLabel(SRCH_HITS.length) + (SRCH_NOTE ? ' · ' + SRCH_NOTE : '');
}
