/* Scripture presentation: the pāda block, the measure-and-shrink fit, the verse
   card's two shapes, reader text size, the ⋯ menu and the word-meaning switches.
   Split out of 50-reader.js on 2026-11-04 (604 of a 700-line guard); the sheet
   itself — opening, note field, history, sharing, navigation — stayed there.
   verseViewState lives here because every function below reads it. */
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
/* The anvaya — the verse's words in natural prose order, the construal a
   teacher gives before translating. It is scripture set as prose, so it is
   deliberately quieter than the verse and deliberately NOT inside
   #verseContent: that element is role="button" and owns the tap that opens the
   four pādas, and a block nested in it would be swallowed by that button and
   read aloud as part of its label. A sibling, therefore.

   The stored text is Devanagari with its own line breaks (the reference's
   sentences), so the breaks are rendered as breaks. IAST follows the app's rule
   for everything else: English shows it, Nepali and Hindi do not. */
function anvayaHtml(s){
  const a = s && s.anv;
  if(!a || !a.d) return '';
  const lines = a.d.split('\n').filter(x => x.trim());
  const body = lines.map(x => `<span class="av-line">${esc(x)}</span>`).join('');
  const iast = (state.lang === 'en' && a.t)
    ? `<span class="av-iast" lang="sa-Latn">${a.t.split('\n').filter(x=>x.trim())
        .map(x => `<span class="av-line">${esc(x)}</span>`).join('')}</span>`
    : '';
  /* One box, one control. Closed it is the anvaya as a sentence; opened it is
     that same sentence word by word, then the construed literal underneath —
     which belongs here because it is the word-by-word reading spoken, not a
     second opinion about the verse. */
  const pairs = anvayaPairsHtml(s);
  const construed = construedInAnvayaHtml(s);
  const hasMore = !!(pairs || construed);
  const id = `anv-body-${String(s.n).replace('.', '-')}`;
  if(!hasMore){
    return `<section class="m-anvaya" aria-label="${esc(L('anvaya_of'))}">`
      + `<span class="av-label" aria-hidden="true">${esc(L('anvaya'))}</span>`
      + `<div class="av-text" lang="sa">${body}</div>${iast}</section>`;
  }
  return `<section class="m-anvaya" aria-label="${esc(L('anvaya_of'))}">`
    + `<button type="button" class="av-toggle" aria-expanded="false" aria-controls="${id}"
         aria-label="${esc(L('anvaya_words_show'))}"
         onclick="App.reader.toggleAnvayaWords(this)">
         <span class="av-label" aria-hidden="true">${esc(L('anvaya'))}</span>
         <span class="av-chev" aria-hidden="true">▾</span>
       </button>`
    + `<div class="av-text" lang="sa">${body}</div>`
    + iast
    + `<div class="av-body" id="${id}" hidden>${pairs}${construed}</div>`
    + `</section>`;
}

/* The anvaya's tokens as word-meaning pairs, in prose order, one pair per line.

   anv.w holds row references, not glosses: an int is one row, {r:[i,j]} is a
   compound fused out of several, {t:...} alone is a word the anvaya supplies
   and the verse does not print. Reading the glosses off the rows here is what
   keeps one meaning in one place — if a row's gloss is corrected, both the
   pāda box and this list change together. */
function anvayaPairsHtml(s){
  const a = s && s.anv, toks = a && a.w;
  if(!Array.isArray(toks) || !toks.length) return '';
  const rows = [];
  (s.flow || []).forEach(it => (it.words || []).forEach(w => rows.push(w)));
  const LI = state.lang === 'en' ? 0 : (state.lang === 'ne' ? 1 : 2);
  const items = [];
  toks.forEach(tok => {
    if(typeof tok === 'number'){
      const w = rows[tok];
      if(w) items.push(pairHtml(w[0], w[1], w[2 + LI] || w[2]));
      return;
    }
    if(!tok || typeof tok !== 'object') return;
    const idx = tok.r || [];
    if(idx.length){
      /* a fused compound: its printed form, glossed by its members */
      const parts = idx.map(i => rows[i]).filter(Boolean);
      const deva = tok.t || parts.map(w => w[0]).join('');
      const gloss = parts.map(w => w[2 + LI] || w[2]).join(' ');
      items.push(pairHtml(deva, parts.map(w => w[1]).join(''), gloss));
    }else if(tok.t){
      /* supplied by the anvaya, with no row of the verse behind it */
      items.push(pairHtml(tok.t, '', suppliedGloss(tok.sup), true));
    }
  });
  if(!items.length) return '';
  return `<div class="av-pairs">`
    + `<span class="av-pairs-label">${esc(L('anvaya_words'))}</span>`
    + `<ol class="av-pair-list">${items.map(x => `<li class="av-pair">${x}</li>`).join('')}</ol>`
    + `</div>`;
}

function pairHtml(deva, iast, gloss, supplied){
  const mark = supplied ? ` <span class="av-sup" aria-hidden="true">·</span>` : '';
  const showIast = state.lang === 'en' && iast;
  return `<span class="av-word" lang="sa"${supplied ? ' data-supplied="1"' : ''}>${esc(deva)}${mark}</span>`
    + (showIast ? `<span class="av-wiast" lang="sa-Latn">${esc(iast)}</span>` : '')
    + `<span class="av-gloss">${esc(gloss || '')}</span>`;
}

/* The construed literal, inside the anvaya box: the same words in the same
   order, spoken as one line. It sits here rather than with the Reading because
   it is the word list above it put into a sentence — the two should be read
   together, and a reader who wants the smooth sense reaches the Reading next. */
function construedInAnvayaHtml(s){
  const lit = s && s.anv && s.anv.lit;
  if(!lit) return '';
  const text = T(lit);
  if(!text) return '';
  return `<div class="av-construed"><span class="av-construed-label">${esc(L('construed'))}</span>`
    + `<span class="av-construed-text">${esc(text)}</span></div>`;
}

/* The declared gloss of a supplied word, mirrored from
   source/anvaya.py SUPPLIED_GLOSS. Kept tiny on purpose: these are the words
   the grammar needs and the verse does not print, and there are a handful. */
const SUPPLIED_GLOSS = {
  he:     ['O', 'हे', 'हे'],            // vocative particle: printed, not a word of the verse
  idam:   ['this', 'यो', 'यह'],
  imam:   ['this', 'यो', 'यह'],
  imām:   ['this', 'यी', 'यह'],
  etat:   ['this', 'यो', 'यह'],
  etad:   ['this', 'यो', 'यह'],
  santi:  ['are', 'छन्', 'हैं'],
  asti:   ['is', 'छ', 'है'],
  sati:   ['being', 'हुँदा', 'होने पर'],
  bhavati:['is', 'हुन्छ', 'होता है'],
  bhavanti:['are', 'हुन्छन्', 'होते हैं'],
  syāt:   ['would be', 'हुन्थ्यो', 'होता'],
  āsīt:   ['was', 'थियो', 'था'],
  babhūva:['became', 'भयो', 'हुआ']
};
function suppliedGloss(sup){
  const g = sup && SUPPLIED_GLOSS[sup];
  if(!g) return '';
  const LI = state.lang === 'en' ? 0 : (state.lang === 'ne' ? 1 : 2);
  return g[LI];
}

function toggleAnvayaWords(btn){
  const sec = btn.closest('.m-anvaya');
  const box = sec && sec.querySelector('.av-body');
  if(!box) return;
  const open = btn.getAttribute('aria-expanded') !== 'true';
  btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  btn.setAttribute('aria-label', L(open ? 'anvaya_words_hide' : 'anvaya_words_show'));
  box.hidden = !open;
  btn.classList.toggle('open', open);
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

/* Option 1 - one verse box, two shapes. The two HTML strings are rebuilt for
   every verse. Keep this mutable state out of App.reader: that namespace is
   frozen, so assigning App.reader.currentVerseState would silently fail. */
let verseViewState = null;

/* Option 1 - one verse box, two shapes. The card itself converts in place;
   pāda and speaker controls own their clicks so revealing word meanings never
   collapses the expanded verse. */
function setVerseView(expanded){
  if(!verseViewState) return;
  const container = document.getElementById('verseContainer');
  const content = document.getElementById('verseContent');
  if(!container || !content) return;
  const on = !!expanded;
  const hadFocus = document.activeElement && content.contains(document.activeElement);
  verseViewState.isExpanded = on;
  if(App.reader && App.reader.closePeek) App.reader.closePeek();
  content.innerHTML = on ? verseViewState.expanded : verseViewState.whole;
  content.classList.toggle('m-whole-verse', !on);
  content.classList.toggle('m-verse', on);
  container.classList.toggle('expanded-mode', on);
  if(on){
    /* The expanded card contains real buttons, so it must not also claim to
       be a button or create nested interactive controls. */
    content.removeAttribute('role');
    content.removeAttribute('tabindex');
    content.removeAttribute('aria-label');
    content.removeAttribute('aria-expanded');
    refreshWordsBtn();
    if(hadFocus){
      const first = content.querySelector('.pada-toggle, .spk-line, .m-verse-back');
      if(first && first.focus) first.focus({preventScroll:true});
    }
  } else {
    content.setAttribute('role', 'button');
    content.setAttribute('tabindex', '0');
    content.removeAttribute('aria-label');
    content.setAttribute('aria-expanded', 'false');
    fitWholeVerse();
    if(hadFocus && content.focus) content.focus({preventScroll:true});
  }
}
function toggleVerseExpansion(ev){
  const content = document.getElementById('verseContent');
  const t = ev && ev.target;
  if(ev && verseViewState && verseViewState.isExpanded && content
     && content.contains(t) && t && t.closest){
    /* Inside the chart, three things belong to a quarter rather than to the
       card: its toggle, its speaker line, its word rows. */
    if(t.closest('.pada-toggle,.spk-line,.words')) return;
    /* The fourth is the paper around them. Each box is its own height, so the
       padding of the box beside an open one is a real target, and a reader who
       taps it means this quarter, not "go back to the whole verse" — which is
       what it used to do (owner, 2026-11-21). A click anywhere inside a pāda
       box toggles that box's words, exactly like tapping the pāda itself. */
    const box = t.closest('.pada-box');
    if(box){
      const btn = box.querySelector('.pada-toggle');
      if(btn){ toggleWords(btn); return; }
    }
  }
  setVerseView(!(verseViewState && verseViewState.isExpanded));
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
  if(!open && App.reader && App.reader.closePeek) App.reader.closePeek();
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
