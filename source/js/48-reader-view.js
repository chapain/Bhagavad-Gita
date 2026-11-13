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
  verseViewState.isExpanded = on;
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
  } else {
    content.setAttribute('role', 'button');
    content.setAttribute('tabindex', '0');
    content.removeAttribute('aria-label');
    content.setAttribute('aria-expanded', 'false');
    fitWholeVerse();
  }
}
function toggleVerseExpansion(ev){
  const content = document.getElementById('verseContent');
  const t = ev && ev.target;
  if(ev && verseViewState && verseViewState.isExpanded && content
     && content.contains(t) && t && t.closest
     && t.closest('.pada-toggle,.spk-line,.words')) return;
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
