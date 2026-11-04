/* ==================== C2: search suggestions ====================
   Kept out of 10-library.js, which the monolith guard holds at 700 lines, and
   separate from the search engine on purpose: the builders are pure (query in,
   rows out) so the tests can rank them without a DOM, and only sugRender
   touches the page. Loaded after 12-search.js, which owns recentLoad, and
   after 10-library.js, which owns searchFoldKey, digitNorm, fmtNL, numL, T
   and L. */
/* ---------------- C2: suggestions while typing ----------------
   Pure row builders first (testable without a DOM), then the listbox. */
let SUG_ROWS = [], SUG_CUR = -1, SUG_OPEN = false;
const SUG_MAX = 10;                      // 5 recent + 3 chapter + 2 number
const sugEl = () => document.getElementById('searchSuggest');
const sugInp = () => document.getElementById('searchInput');
function sugVerseNumbers(q){
  const m = digitNorm(q).replace(/[।॥]/g, '.').match(/^(\d{1,2})(?:[.:\-\/\s](\d{0,2}))?$/);
  if(!m || +m[1] < 1 || +m[1] > 18) return [];   // "2.4" prefixes 2.40…2.47
  const pre = m[2] || '';
  return versesForChapter(+m[1] - 1).filter(l => !pre || l.norm.split('.')[1].startsWith(pre));
}
function sugChapterRows(q){
  const f = searchFoldKey(q), e = searchExactKey(q);
  if(!f && !e) return [];
  return DATA.filter((ch, ci) => ch && ch.themes && ci < 18).filter(ch => {
    const n = [ch.names.en, ch.names.ne, ch.names.hi].join(' ');
    return (f && searchFoldKey(n).includes(f)) || (e && searchExactKey(n).includes(e));
  });
}
/* One flat list of rows: ↑/↓ is a single index and each row carries its own
   kind, so the listbox never needs nested keyboard handling. */
function sugRowsFor(q){
  q = String(q || '').trim();
  if(q.length < 2) return [];
  const rows = [], seen = new Set();
  const push = (kind, label, hint, value) => {
    if(rows.length < SUG_MAX && !seen.has(kind + '|' + value)){
      seen.add(kind + '|' + value);
      rows.push({kind, label, hint, value});
    }
  };
  recentLoad().filter(x => x.toLowerCase() !== q.toLowerCase())
    .slice(0, 5).forEach(x => push('recent', x, L('search_recent'), x));
  sugChapterRows(q).slice(0, 3).forEach(ch =>
    push('chapter', T(ch.names), L('chapters') + ' ' + numL(ch.num), String(ch.num)));
  sugVerseNumbers(q).slice(0, 2).forEach(l =>
    push('verse', L('verse') + ' ' + fmtNL(l.norm), L('verses'), l.norm));
  return rows;
}
function sugClose(){
  SUG_ROWS = []; SUG_CUR = -1; SUG_OPEN = false;
  const list = sugEl(), hint = document.getElementById('searchSuggestHint'), inp = sugInp();
  if(list){ list.hidden = true; list.innerHTML = ''; }
  if(hint) hint.hidden = true;
  if(inp){ inp.setAttribute('aria-expanded', 'false'); inp.removeAttribute('aria-activedescendant'); }
}
function sugRender(q){
  const list = sugEl(), inp = sugInp();
  if(!list || !inp) return;
  SUG_ROWS = sugRowsFor(q); SUG_CUR = -1;
  if(!SUG_ROWS.length) return sugClose();
  list.innerHTML = SUG_ROWS.map((r, i) =>
    `<li id="sug-${i}" role="option" aria-selected="false" class="sug-row"
         onclick="App.library.sugPick(${i})" onmousedown="event.preventDefault()"
       ><span class="sug-label">${esc(r.label)}</span
       ><span class="sug-kind">${esc(r.hint)}</span></li>`).join('');
  list.hidden = false; SUG_OPEN = true;
  inp.setAttribute('aria-expanded', 'true');
  inp.removeAttribute('aria-activedescendant');
  const hint = document.getElementById('searchSuggestHint');
  if(hint){ hint.textContent = L('search_suggest_hint'); hint.hidden = false; }
}
function sugMove(delta){
  if(!SUG_OPEN || !SUG_ROWS.length) return;
  SUG_CUR = (SUG_CUR + delta + SUG_ROWS.length) % SUG_ROWS.length;
  SUG_ROWS.forEach((_, i)=>{
    const el = document.getElementById('sug-' + i);
    if(!el) return;
    const on = i === SUG_CUR;
    el.setAttribute('aria-selected', on ? 'true' : 'false');
    el.classList.toggle('is-active', on);
  });
  const inp = sugInp();
  if(inp) inp.setAttribute('aria-activedescendant', 'sug-' + SUG_CUR);
  const el = document.getElementById('sug-' + SUG_CUR);
  if(el && el.scrollIntoView) el.scrollIntoView({block: 'nearest'});
}
function sugPick(i){
  const r = SUG_ROWS[i], inp = sugInp();
  if(!r || !inp) return;
  sugClose();
  if(r.kind === 'chapter'){ inp.value = ''; searchX(); App.views.chapter(+r.value - 1); return; }
  inp.value = r.value; searchX(); doSearch();
}
/* Returns true when the key was consumed, so the caller never also submits. */
function sugKey(e){
  const k = e.key;
  if(k === 'ArrowDown' || k === 'ArrowUp'){
    if(!SUG_OPEN){ sugRender(sugInp().value); return SUG_OPEN; }
    sugMove(k === 'ArrowDown' ? 1 : -1); e.preventDefault(); return true;
  }
  if(k === 'Escape' && SUG_OPEN){ sugClose(); e.preventDefault(); return true; }
  if(k === 'Enter' && SUG_OPEN && SUG_CUR >= 0){ sugPick(SUG_CUR); e.preventDefault(); return true; }
  return false;
}
function sugBlur(){ setTimeout(sugClose, 120); }
