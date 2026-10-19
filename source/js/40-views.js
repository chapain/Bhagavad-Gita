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
  App.session.update({view:'chapters', section:section, chapter:null, theme:null}); persistView(); renderCrumbs();
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
  if(state.view==='data') return '#data';
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
  if($('#modalBg').classList.contains('open')) App.reader.close();
  $('#searchInput').value = '';
  App.session.update({origin:null});
  showWelcome();
}
function showWelcome(){
  App.session.update({view:'welcome', chapter:null, theme:null, section:null}); persistView(); renderCrumbs();
  view.innerHTML = `
    <div class="welcome fade-in">
      <section class="welcome-hero" aria-labelledby="welcomeTitle">
        <div class="welcome-copy">
          <div class="w-mark" aria-hidden="true">
            <span class="w-om">ॐ</span><span class="w-mark-line"></span>
          </div>
          <h2 class="view-title" id="welcomeTitle">${esc(L('welcome_title'))}</h2>
          <p class="view-sub">${esc(L('welcome_sub'))}</p>
          <div class="w-actions">
            <button class="tool-btn primary big" onclick="showSections()">
              <span>${esc(L('welcome_enter'))}</span><span class="w-arrow" aria-hidden="true">→</span>
            </button>
            <details class="welcome-guide">
              <summary>${esc(L('guide_explore'))}</summary>
              <ol>
                <li>${esc(L('guide_way'))}</li>
                <li>${esc(L('guide_chapter'))}</li>
                <li>${esc(L('guide_verse'))}</li>
              </ol>
            </details>
          </div>
          <div class="w-foot">${esc(L('welcome_foot'))}</div>
        </div>
        <section class="welcome-stage" aria-label="${esc(L(state.shared ? 'shared_label' : 'verse_of_day'))}">
          <svg class="welcome-wheel" viewBox="0 0 320 320" fill="none" aria-hidden="true" focusable="false">
            <circle cx="160" cy="160" r="132" stroke="currentColor" stroke-width="1.2"/>
            <circle cx="160" cy="160" r="111" stroke="currentColor" stroke-width=".8"/>
            <circle cx="160" cy="160" r="39" stroke="currentColor" stroke-width="1.2"/>
            <circle cx="160" cy="160" r="13" stroke="currentColor" stroke-width="1.2"/>
            <path d="M160 28v264M28 160h264M66.7 66.7l186.6 186.6M253.3 66.7 66.7 253.3" stroke="currentColor" stroke-width="1"/>
            <path d="m160 21 4 7-4 7-4-7 4-7Zm0 264 4 7-4 7-4-7 4-7ZM21 160l7-4 7 4-7 4-7-4Zm264 0 7-4 7 4-7 4-7-4Z" fill="currentColor" opacity=".45"/>
          </svg>
          <div id="wDay" class="welcome-day-slot" aria-live="polite"></div>
        </section>
      </section>
    </div>`;
  const paint = (dv, shared)=>{
    if(!dv || state.view!=='welcome' || !DATA || !DATA[dv.ci]) return;
    const c = DATA[dv.ci], v = App.library.verse(dv);
    const part = App.library.entryAt(c.themes[dv.ti], dv.si).part;
    const el = document.getElementById('wDay'); if(!el) return;
    el.innerHTML = `<div class="w-day fade-in" role="button" tabindex="0"
          aria-label="${esc(L('verse'))} ${esc(fmtNL(v.n))}: ${esc(T(part.titles))}. ${esc(L('open_verse'))}"
          onclick="App.reader.open(${dv.ci},${dv.ti},${dv.si},'book',null,this)">
          <div class="wd-label">${esc(shared ? L('shared_label') : L('verse_of_day'))}</div>
          <div class="vnum">${esc(L('verse'))} ${esc(fmtNL(v.n))}</div>
          <div class="m-topic"><span class="mt-lab">${esc(L('verse_topic'))}:</span> ${esc(T(part.titles))}</div>
          <div class="padas" lang="sa">${App.reader.padaBlock(v)}</div>
          <div class="vhint">${shared ? esc(L('shared_hint')) : esc(T(v.paras))}</div>
          <div class="wd-open"><span>${esc(L('open_verse'))}</span><span aria-hidden="true">→</span></div>
        </div>`;
  };
  if(state.shared){ loadChapter(state.shared.ci+1).then(()=>paint(state.shared, true)).catch(gitaLoadFail); }
  else {
    const sp = daySpec();
    loadChapter(sp.ch).then(()=>paint(App.library.location(sp.id), false)).catch(gitaLoadFail);
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
  App.session.update({view:'sections', chapter:null, theme:null, section:null, shared:null}); persistView(); renderCrumbs();
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
      ${btn('learn',   esc(L('opt_learn_s')), `App.learn.show(${ci})`,   esc(L('opt_learn_d')))}
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
  App.session.update({view:'chapter', chapter:ci,
    section:state.section || Math.ceil(ch.num/6), theme:at});
  persistView(); renderCrumbs();
  const themeSec = (at != null) ? numL(at+1) : '';
  const body = ch.themes.map((t,ti)=>{
    // openModal/sutraAt index within this theme, not across the chapter.
    let themeSi = 0;
    const verseCards = t.parts.map(p=>{
      const s = p.sutras[0];
      const si = themeSi++;
      /* The paraphrase is printed whole, not cut at 90 characters (the cut
         lived here until 2026-10-18): a reader working through the theme map
         stays in the chapter and wants the complete thought under each
         title — the longest paraphrase in the corpus is ~190 characters,
         four or five card lines. Clicking a card still opens the sheet for
         the Sanskrit and the word-by-word reading. */
      return `<div class="mini" role="button" tabindex="0" onclick="App.reader.open(${ci},${ti},${si},'theme',null,this)">
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


/* Views owns route-level rendering and address persistence. */
App.views = Object.freeze({
  renderCrumbs,
  persist: persistView,
  hash: viewHash,
  home: goHome,
  welcome: showWelcome,
  sections: showSections,
  chapters: showChapters,
  chapter: showChapter,
  verses: showVerses,
  breadcrumbs: wayCrumbs,
  wayName,
  chapterTitle: chTitle,
  modeSwitch
});
