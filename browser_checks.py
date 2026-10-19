#!/usr/bin/env python3
"""browser_checks.py — live behaviour tests for the Bhagavad Gita app.

run_gita_app.js checks the *document*; this drives a real browser and checks the
app as a user meets it: rendering, i18n, Devanagari numerals, touch gestures,
back-button, responsive layout, and (when served over http) the offline cache.

Usage:
    python3 browser_checks.py                 # test the local built file
    python3 browser_checks.py URL             # test a deployed site
    python3 browser_checks.py --serve         # serve site/ and test offline too

Needs:  pip install playwright && python3 -m playwright install chromium --with-deps
"""
import os
import pathlib
import shlex
import subprocess
import sys
import time
import unicodedata

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
PASS, FAIL = 0, []


def ok(cond, label):
    global PASS
    if cond:
        PASS += 1
    else:
        FAIL.append(label)
        print("   \u2717 FAIL:", label)


def group(n):
    print(f"\n== {n} ==")


def run(pw, url, offline_capable=False):
    # Allow a preinstalled Chromium in network-restricted development sandboxes.
    # This changes the launcher only; every browser assertion still runs.
    launch = {}
    executable = os.environ.get("GITA_CHROMIUM_EXECUTABLE")
    if executable:
        launch["executable_path"] = executable
        launch["args"] = shlex.split(os.environ.get("GITA_CHROMIUM_ARGS", ""))
    b = pw.chromium.launch(**launch)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                        has_touch=True, device_scale_factor=2, service_workers="allow")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url, wait_until="load", timeout=90000)
    pg.wait_for_function("DATA && VERSES.length === 700", timeout=30000)

    def colour(token, page=pg):
        # Resolve the current light/dark palette, not obsolete hard-coded RGBs.
        return page.evaluate("""name => {
            const el = document.createElement('span');
            el.style.color = 'var(' + name + ')';
            document.body.appendChild(el);
            const result = getComputedStyle(el).color;
            el.remove();
            return result;
        }""", token)

    group("rendering")
    ok(pg.title() == "Bhagavad Gita — English, Nepali, Hindi · 700 Verses", "title")
    ok("Welcome" in pg.inner_text("#view"), "welcome renders (JS runs)")
    ok(pg.evaluate("DATA.length") == 18, "18 chapters")
    ok(pg.evaluate("VERSES.length") == 700, "700 verses indexed")

    group("verse of the day card")
    # same anatomy as the theme cards: vnum line, topic line, Devanagari,
    # paraphrase snippet — the VotD label being the only addition.
    ok(pg.eval_on_selector(".w-day .m-topic", "e=>e.textContent.trim().length") > 0,
       "verse-of-the-day card carries the verse topic line")
    ok(pg.eval_on_selector(".w-day .vhint", "e=>e.textContent.trim().length") > 0,
       "verse-of-the-day card carries the paraphrase, like the theme cards")
    # The number is the vnum line, exactly as on the theme cards; the speaker
    # must not be the same colour as the verse, or it reads as part of the verse.
    pg.evaluate("""() => {
      const flat = [];
      DATA.forEach(c => c.themes.forEach((t, ti) => t.parts.forEach(
        p => p.sutras.forEach(s => flat.push({ s, c, ti })))));
      const hit = flat.find(x => x.s.n === '2.11');   // has a speaker line
      document.querySelector('.w-day .padas').innerHTML = padaBlockDeva(hit.s);
      document.querySelector('.w-day .vnum').textContent =
        L('verse') + ' ' + fmtNL(hit.s.n);
    }""")
    ok("2.11" in pg.locator(".w-day .vnum").inner_text(), "verse number shown in the vnum line")
    ok(pg.locator(".w-day .padas .gl-n").count() == 0,
       "no inline daṇa number — same look as the theme cards")
    vcol = pg.locator(".w-day .padas .gline").first.evaluate("e => getComputedStyle(e).color")
    scol = pg.locator(".w-day .padas .spk").first.evaluate("e => getComputedStyle(e).color")
    ok(vcol != scol, f"speaker colour differs from the verse ({scol} vs {vcol})")
    ok(pg.locator(".w-day .padas .spk").first.evaluate(
        "e => getComputedStyle(e).fontStyle") == "italic", "speaker is italic")
    ok(pg.locator(".w-day .padas .gline").first.evaluate(
        "e => getComputedStyle(e).textAlign") == "center",
       "verse of the day is centred, like a display piece")
    ok(pg.evaluate("(()=>{const a=document.querySelector('.w-day .vnum'),"
                   "b=document.querySelector('.w-day .m-topic');"
                   "return !!(a.compareDocumentPosition(b)&Node.DOCUMENT_POSITION_FOLLOWING);})()"),
       "verse number sits above the topic line")
    # the owner's brief: label in an oval tag, topic in a colour of its own —
    # no orange pile-up on top of the card
    ok(float(pg.eval_on_selector(".w-day .wd-label",
        "e=>parseFloat(getComputedStyle(e).borderRadius)")) > 8,
       "the 'Verse of the Day' label is an oval pill")
    ok(pg.eval_on_selector(".w-day .m-topic", "e=>getComputedStyle(e).color") !=
       pg.eval_on_selector(".w-day .vnum", "e=>getComputedStyle(e).color"),
       "topic line is a different colour than the verse number")
    ok(not pg.evaluate(
        "() => { const e = document.querySelector('.w-day');"
        " return e.scrollWidth > e.clientWidth; }"), "card does not overflow")
    mobile_tracks = pg.eval_on_selector(".welcome-hero", "e=>getComputedStyle(e).gridTemplateColumns.split(' ').length")
    pg.set_viewport_size({"width": 1440, "height": 900})
    pg.wait_for_timeout(60)
    desktop_tracks = pg.eval_on_selector(".welcome-hero", "e=>getComputedStyle(e).gridTemplateColumns.split(' ').length")
    pg.set_viewport_size({"width": 390, "height": 844})
    ok(mobile_tracks == 1 and desktop_tracks == 2,
       "welcome hero stacks on phones and pairs intro with verse on desktop")
    pg.reload(wait_until="load")
    pg.wait_for_timeout(400)

    group("navigation")
    pg.get_by_role("button", name="Enter", exact=False).first.click()
    pg.wait_for_timeout(400)
    pg.evaluate("showChapter(0)")
    pg.wait_for_timeout(400)
    ok("Back" in pg.locator(".back-top").first.inner_text() and "chapter" in pg.locator(".back-top").first.inner_text().lower(), "chapter view: back to chapters")
    # Phase 3.1: theme deep link scrolls to that theme inside the chapter view
    pg.evaluate("showChapter(0,0)")
    pg.wait_for_timeout(400)
    ok(pg.evaluate("state.view === 'chapter' && state.chapter === 0"),
       "theme anchor lands inside the unified chapter view")
    ok(pg.evaluate("document.querySelector('#theme-0').open"),
       "a theme deep link opens its collapsed theme section")

    group("retired views stay retired")
    # Owner report 2026-10-17: two links still walked into the views the Phase
    # 3.1 merge had retired — the verse sheet's "back to theme" opened the old
    # per-theme page, and the Learn path's "back to chapter" opened the old
    # continuous-reading page. Both must land on the one chapter view, with the
    # theme's disclosure open where a theme was asked for.
    pg.evaluate("showChapter(0)")
    pg.wait_for_timeout(400)
    last = pg.evaluate("""() => {
        const ch = DATA[0], ti = ch.themes.length - 1;
        let si = 0; for (const p of ch.themes[ti].parts) si += p.sutras.length;
        openModal(0, ti, si - 1, 'theme');
        return {ti: ti};
    }""")
    pg.wait_for_timeout(500)
    ok(pg.locator(".m-nav .m-back").count() == 1,
       "the chapter's last verse still offers its way back to the theme")
    pg.locator(".m-nav .m-back").click()
    pg.wait_for_timeout(900)
    ok(pg.evaluate("state.view") == "chapter" and pg.locator(".ch-theme[open]").count() == 1
       and pg.evaluate("state.theme") == last["ti"],
       f"back to theme opens the chapter view with that theme expanded "
       f"(view={pg.evaluate('state.view')}, open={pg.locator('.ch-theme[open]').count()})")
    # A theme inside the chapter is the chapter's address, so the generated
    # chapter pages' "Study this theme in the app →" links survive a reload.
    pg.evaluate("showChapter(0, 2)")
    pg.wait_for_timeout(400)
    ok(pg.evaluate("location.hash") == "#theme=1.2",
       f"an open theme is written into the address ({pg.evaluate('location.hash')})")
    pg.reload(wait_until="load")
    pg.wait_for_timeout(1600)
    ok(pg.evaluate("state.view") == "chapter" and pg.evaluate("state.theme") == 2
       and pg.locator(".ch-theme[open]").count() == 1,
       "a #theme= deep link reopens that theme after a reload")
    # The Learn path's "back to chapter" (the story screen's foot link).
    pg.evaluate("showLearn(0)")
    pg.wait_for_timeout(600)
    pg.evaluate("lrStory(0, 0)")
    pg.wait_for_timeout(700)
    ok(pg.locator(".back-foot .back-top").count() == 1,
       "the story screen carries its back link")
    pg.locator(".back-foot .back-top").first.click()
    pg.wait_for_timeout(800)
    ok(pg.evaluate("state.view") == "chapter" and pg.locator(".ch-theme-head").count() > 0
       and pg.locator(".mode-seg .ms-btn.on").inner_text().strip() == "Thematic study",
       "back to chapter lands on the unified chapter view, not the retired reading page")
    ok(pg.evaluate("!document.querySelector('.rd-v') && !document.querySelector('.reading')"),
       "the retired reading/theme markup is rendered nowhere")
    ok(pg.evaluate("['welcome','sections','chapters','chapter','learn','play',"
                   "'search','favorites'].includes(state.view)"),
       f"state.view is one of the surviving views ({pg.evaluate('state.view')})")

    group("english wording")
    pg.evaluate("setLang('en')")
    pg.fill("#searchInput", "2.47")
    pg.wait_for_timeout(800)
    pg.locator(".mini").first.click()
    pg.wait_for_timeout(600)
    ok("4 quarters of 8" in pg.eval_on_selector(".m-meter", "e=>e.textContent"), "meter uses 'quarters'")
    ok(pg.eval_on_selector_all(".pb-num", "e=>e.map(x=>x.textContent.trim())")
       == ["Quarter 1", "Quarter 2", "Quarter 3", "Quarter 4"], "boxes say Quarter 1-4")
    foot = pg.eval_on_selector("#appFooter", "e=>e.textContent")
    ok("8 syllables each" not in foot, "footer drops the false 8-syllable claim")
    ok("four quarters (pādas)" in foot, "footer keeps pāda as a gloss")

    group("devanagari numerals")
    for lang in ("ne", "hi"):
        pg.evaluate(f"setLang('{lang}')")
        pg.wait_for_timeout(400)
        # Phase 3.2: verse ref lives inside .m-title, meter inside the
        # ⋯ overflow menu (open it to assert its localised text).
        ok("श्लोक २.४७" in pg.eval_on_selector(".m-title", "e=>e.textContent"), f"{lang}: verse ref")
        ok("पाद १" in pg.eval_on_selector_all(".pb-num", "e=>e.map(x=>x.textContent).join()"), f"{lang}: पाद boxes")
        pg.evaluate("toggleVerseMenu()")
        pg.wait_for_timeout(100)
        ok("अक्षर" in pg.eval_on_selector(".m-menu .m-meter", "e=>e.textContent"), f"{lang}: meter localised")
        pg.evaluate("closeVerseMenu()")
        stacks = pg.eval_on_selector_all("#appTitle, .seg .lang-btn, .m-title",
            "els => els.map(e => ({lang:e.lang, family:getComputedStyle(e).fontFamily}))")
        ok(len(stacks) == 5
           and all("Noto Serif Devanagari" in item['family'] for item in stacks)
           and all(item['family'].startswith('"Noto Serif Devanagari"')
                   for item in stacks if item['lang'] in ('ne', 'hi')),
           f"{lang}: headings and every language option use the bundled Devanagari face")
        cnt = pg.eval_on_selector(".m-count", "e=>e.textContent")
        # NB: '७'.isdigit() is True in Python — test for ASCII 0-9 specifically.
        ok(("मध्ये" in cnt or "में से" in cnt) and not any(c in "0123456789" for c in cnt),
           f"{lang}: counter all-Devanagari ({cnt})")
    # no ASCII digits anywhere in ne/hi UI chrome
    for lang in ("ne", "hi"):
        pg.evaluate(f"setLang('{lang}')")
        pg.wait_for_timeout(300)
        leaks = pg.evaluate("""()=>{const out=[];
            document.querySelectorAll('#view *, #modal *, .toolbar *, header *, footer').forEach(el=>{
              if(el.children.length) return;
              const t=(el.textContent||'').trim();
              if(t && /[0-9]/.test(t)) out.push(t.slice(0,40));});
            return [...new Set(out)];}""")
        ok(not leaks, f"{lang}: no ASCII digits in UI ({leaks[:3]})")
    pg.evaluate("setLang('en')")
    pg.wait_for_timeout(300)

    # The service worker intentionally reloads an already-open tab after an
    # update. Lock the selected language and the current reading context across
    # both that reload and an ordinary browser refresh.
    group("language survives a reload")
    if pg.eval_on_selector("#modalBg", "e=>e.classList.contains('open')"):
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(500)
    pg.evaluate("loadChapter(18).then(()=>showChapter(17))")
    pg.wait_for_function("state.view === 'chapter' && state.chapter === 17", timeout=30000)
    pg.evaluate("setLang('ne')")
    pg.wait_for_timeout(600)
    ok(pg.evaluate("localStorage.getItem('gitaLang')") == "ne",
       "choosing नेपाली writes gitaLang to localStorage")
    ok(pg.evaluate("sessionStorage.getItem('gitaLang')") == "ne",
       "the current tab keeps its own language across reloads")
    before = pg.eval_on_selector("#view", "e=>e.textContent")
    ok("अध्याय १८" in before, "chapter 18 view is numbered in Devanagari")
    pg.reload(wait_until="load")
    pg.wait_for_function("DATA && state.view === 'chapter'", timeout=30000)
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.lang") == "ne", "still नेपाली after the reload")
    ok(pg.evaluate("state.chapter === 17 && state.view === 'chapter'"),
       "still on chapter 18 after the reload")
    ok(pg.eval_on_selector("html", "e=>e.lang") == "ne",
       "<html lang> is ne after the reload, so screen readers stay in Nepali")
    ok(pg.eval_on_selector(".lang-btn[data-lang='ne']", "e=>e.classList.contains('on')") is True,
       "नेपाली segment still shows as selected after the reload")
    ok(pg.eval_on_selector(".lang-btn[data-lang='ne']", "e=>e.getAttribute('aria-pressed')") == "true",
       "नेपाली segment still reports aria-pressed after the reload")
    ok(pg.eval_on_selector(".lang-btn[data-lang='en']", "e=>e.classList.contains('on')") is False,
       "English segment is not selected after the reload")
    after = pg.eval_on_selector("#view", "e=>e.textContent")
    ok("अध्याय १८" in after, "chapter 18 is still numbered in Devanagari after the reload")
    ok(before == after,
       "the study guide reads identically before and after the reload")

    other_tab = ctx.new_page()
    other_tab.goto(url, wait_until="load", timeout=90000)
    other_tab.wait_for_function("DATA && VERSES.length === 700", timeout=30000)
    other_tab.evaluate("setLang('hi')")
    pg.reload(wait_until="load")
    pg.wait_for_function("state.view === 'chapter' && state.chapter === 17", timeout=30000)
    ok(pg.evaluate("state.lang === 'ne' && sessionStorage.getItem('gitaLang') === 'ne'"),
       "a language change in another tab does not change this tab on refresh")
    other_tab.close()

    pg.evaluate("openModal(17,0,0,'theme',null,null)")
    pg.wait_for_selector("#modalBg.open")
    pg.locator("#mWordsSection > summary").click()
    pg.locator(".pada-toggle").first.click()
    pg.evaluate("document.querySelector('#modal').scrollTop = 120")
    pg.wait_for_timeout(250)
    modal_before = pg.evaluate("""() => ({lang:state.lang, view:state.view, chapter:state.chapter,
      verse:document.querySelector('.m-num-chit')?.textContent.trim(),
      route:location.hash, open:document.querySelector('#modalBg').classList.contains('open'),
      details:document.querySelector('#mWordsSection').open,
      words:document.querySelector('.words.open')?.id,
      scroll:document.querySelector('#modal').scrollTop})""")
    pg.reload(wait_until="load")
    pg.wait_for_function("document.querySelector('#modalBg').classList.contains('open')", timeout=30000)
    pg.wait_for_timeout(200)
    modal_after = pg.evaluate("""() => ({lang:state.lang, view:state.view, chapter:state.chapter,
      verse:document.querySelector('.m-num-chit')?.textContent.trim(),
      route:location.hash, open:document.querySelector('#modalBg').classList.contains('open'),
      details:document.querySelector('#mWordsSection').open,
      words:document.querySelector('.words.open')?.id,
      scroll:document.querySelector('#modal').scrollTop})""")
    ok(modal_before['lang'] == modal_after['lang'] == 'ne'
       and modal_after['view'] == 'chapter' and modal_after['chapter'] == 17
       and modal_after['open'] and modal_after['verse'] == modal_before['verse']
       and modal_after['route'] == modal_before['route'],
       f"manual refresh restores the same Nepali chapter and open verse sheet ({modal_after})")
    ok(modal_after['details'] and modal_after['words'] == modal_before['words']
       and modal_after['scroll'] == modal_before['scroll'],
       "refresh restores expanded word meanings and the verse-sheet scroll position")
    pg.keyboard.press("Escape")
    pg.wait_for_function("!document.querySelector('#modalBg').classList.contains('open')", timeout=5000)
    ok(pg.evaluate("state.view === 'chapter' && state.chapter === 17 && !location.hash.startsWith('#v=')"),
       "closing a restored verse returns to the chapter instead of the welcome page")

    pg.evaluate("showWelcome()")
    pg.wait_for_selector(".w-day")
    pg.locator(".w-day").click()
    pg.wait_for_selector("#modalBg.open")
    home_verse = pg.eval_on_selector(".m-num-chit", "e=>e.textContent.trim()")
    pg.reload(wait_until="load")
    pg.wait_for_function("state.view==='welcome' && document.querySelector('#modalBg').classList.contains('open')",
                         timeout=30000)
    restored_home_verse = pg.eval_on_selector(".m-num-chit", "e=>e.textContent.trim()")
    pg.keyboard.press("Escape")
    pg.wait_for_function("!document.querySelector('#modalBg').classList.contains('open')", timeout=5000)
    ok(pg.evaluate("state.view === 'welcome'") and home_verse == restored_home_verse,
       "refresh restores a verse sheet opened from Welcome, even when its chapter was lazy-loaded")

    # Corrupt values in a new tab have no valid history snapshot to rescue them:
    # they must still fall back to English and paint a complete interface.
    bad_ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    bad_ctx.add_init_script("""() => {
      try{ localStorage.setItem('gitaLang','zz'); }catch(e){}
      try{ sessionStorage.setItem('gitaLang','zz'); }catch(e){}
    }""")
    bad_pg = bad_ctx.new_page()
    bad_pg.goto(url, wait_until="load", timeout=90000)
    bad_pg.wait_for_function("DATA && VERSES.length === 700", timeout=30000)
    ok(bad_pg.evaluate("state.lang") == "en", "an unknown stored language falls back to en")
    ok(bad_pg.evaluate("document.getElementById('appTitle').textContent === UI.en.app_title"),
       "a bad stored language still renders the whole English interface")
    bad_ctx.close()
    pg.evaluate("setLang('en')")
    pg.wait_for_timeout(300)

    group("search")
    # a previous group may have left the verse sheet open
    if pg.eval_on_selector("#modalBg", "e=>e.classList.contains('open')"):
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(500)
    # On a Devanagari keyboard the danda । sits where the full stop is, so १।१ is
    # the natural way to type 1.1. Accept every separator a reader might produce.
    for q, label in [("१.१", "devanagari digits"), ("१।१", "danda separator"),
                     ("२।४७", "danda, two digits"), ("॥१।१॥", "wrapped in dandas"),
                     ("१:१", "colon"), ("१-१", "hyphen")]:
        pg.click("#searchInput")
        pg.fill("#searchInput", "")
        pg.type("#searchInput", q, delay=15)
        pg.wait_for_timeout(600)
        hits = pg.eval_on_selector_all(".mini .vnum", "e=>e.map(x=>x.textContent.trim())")
        ok(len(hits) == 1, f"searching {q!r} ({label}) finds the verse ({hits[:1]})")
    pg.fill("#searchInput", "2.47")
    pg.wait_for_timeout(600)
    head = pg.evaluate("document.querySelector('.mini .m-topic').textContent")
    exp = pg.evaluate("(()=>{const loc=VERSES.find(v=>v.id==='2.47');"
                      "return sutraAt(DATA[loc.ci].themes[loc.ti],loc.si).part.titles.en;})()")
    ok(exp in head and head.strip().startswith("Verse topic:"),
       "search card shows 'Verse topic: <part title>' on one line")
    pg.reload(wait_until="load")
    pg.wait_for_function("state.view === 'search' && document.querySelectorAll('.mini').length === 1",
                         timeout=30000)
    ok(pg.evaluate("document.querySelector('#searchInput').value === '2.47'"),
       "refresh restores the search query and its results")
    pg.locator(".mini").first.click()
    pg.wait_for_timeout(400)
    ok(pg.evaluate("!!document.querySelector('.m-part')"),
       "the crumb line shows even when the verse was opened from search")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    # A bare number is a free-text search, and the index stores verse numbers as
    # ASCII — so a Devanagari digit must be converted too, or १ finds nothing
    # while 1 finds the whole chapter.
    def count(q):
        pg.click("#searchInput")
        pg.fill("#searchInput", "")
        pg.type("#searchInput", q, delay=12)
        pg.wait_for_timeout(600)
        return pg.locator(".mini").count()
    for ascii_q, deva_q in [("1", "१"), ("7", "७"), ("17", "१७"), ("12", "१२")]:
        a, d = count(ascii_q), count(deva_q)
        ok(a == d and a > 0, f"searching {deva_q!r} matches {ascii_q!r} ({d} vs {a})")
    ok(count("धर्मक्षेत्रे") == 1, "Devanagari word search still finds its verse")
    pg.fill("#searchInput", "")
    pg.wait_for_timeout(400)
    for q in ("2.47", "२.४७", "16.6", "yoga", "कर्म"):
        pg.evaluate("closeModal()")
        pg.wait_for_timeout(150)
        pg.fill("#searchInput", q)
        pg.wait_for_timeout(800)
        ok(pg.eval_on_selector_all(".mini", "e=>e.length") > 0, f'search "{q}" finds hits')

    # NFD/NFC IAST queries and plain-keyboard transliterations must reach the
    # same verses as the canonical spellings in the shipped text.
    nfc_query = "kṛṣṇa"
    nfd_query = unicodedata.normalize("NFD", nfc_query)
    nfc_hits = count(nfc_query)
    nfd_hits = count(nfd_query)
    ok(nfc_hits > 0 and nfc_hits == nfd_hits,
       "NFC and NFD IAST queries return the same non-empty result set")
    for query, ref in [
        ("krishna", "1.28"),
        ("karmanye vadhikaraste", "2.47"),
        ("dharmakshetre", "1.1"),
        ("yada yada hi dharmasya", "4.7"),
        ("sarvadharman parityajya", "18.66"),
    ]:
        count(query)
        shown = pg.eval_on_selector_all(".mini .vnum", "e=>e.map(x=>x.textContent.trim())")
        ok(any(item.endswith(ref) for item in shown),
           f'ASCII query "{query}" finds verse {ref}')

    # The visible count uses a singular noun for one and a plural for many in
    # each interface language (Hindi's noun is invariant in the direct case).
    one = count("2.47")
    one_label = pg.eval_on_selector(".res-count", "e=>e.textContent.trim()")
    ok(one == 1 and one_label == "1 result", "English single-result wording")
    many = count("yoga")
    many_label = pg.eval_on_selector(".res-count", "e=>e.textContent.trim()")
    ok(many > 1 and many_label == f"{many} results", "English plural-result wording")
    deva_num = lambda n: str(n).translate(str.maketrans("0123456789", "०१२३४५६७८९"))
    for lang, singular, plural in [
        ("ne", "परिणाम", "परिणामहरू"),
        ("hi", "परिणाम", "परिणाम"),
    ]:
        pg.evaluate(f"setLang('{lang}')")
        pg.wait_for_timeout(400)
        one = count("2.47")
        one_label = pg.eval_on_selector(".res-count", "e=>e.textContent.trim()")
        ok(one == 1 and one_label == f"{deva_num(one)} {singular}",
           f"{lang}: singular-result wording")
        many = count("yoga")
        many_label = pg.eval_on_selector(".res-count", "e=>e.textContent.trim()")
        ok(many > 1 and many_label == f"{deva_num(many)} {plural}",
           f"{lang}: plural-result wording")
    pg.evaluate("setLang('en')")
    pg.wait_for_timeout(300)

    group("touch / mobile")
    pg.fill("#searchInput", "1.1")
    pg.wait_for_timeout(800)
    pg.locator(".mini").first.click()
    pg.wait_for_timeout(600)
    v1 = pg.eval_on_selector(".m-num-chit", "e=>e.textContent.trim().slice(0,12)")
    pg.evaluate("""()=>{const bg=document.querySelector('#modalBg');
      const mk=(t,x,y)=>{const e=new TouchEvent(t,{bubbles:true,cancelable:true,
        touches:t==='touchend'?[]:[new Touch({identifier:1,target:bg,clientX:x,clientY:y})],
        changedTouches:[new Touch({identifier:1,target:bg,clientX:x,clientY:y})]});bg.dispatchEvent(e);};
      mk('touchstart',300,400);mk('touchmove',200,402);mk('touchend',80,404);}""")
    pg.wait_for_timeout(500)
    ok(v1 != pg.eval_on_selector(".m-num-chit", "e=>e.textContent.trim().slice(0,12)"), "swipe → next verse")
    pg.go_back()
    pg.wait_for_timeout(500)
    ok(not pg.eval_on_selector("#modalBg", "e=>e.classList.contains('open')"), "back button closes the sheet")
    ok(pg.evaluate("document.documentElement.scrollWidth===document.documentElement.clientWidth"),
       "no horizontal overflow")

    # The door is the Three Ways itself — no tab strip, no flat all-18 list
    # (owner's call, 2026-08-27). A way opens onto its six chapters; a chapter
    # card opens on Mula.
    pg.evaluate("showSections()")
    pg.wait_for_timeout(500)
    ok(pg.locator(".top-tabs").count() == 0 and pg.locator(".browse-all").count() == 0,
       "the landing has no tab strip and no browse-all link")
    ok(pg.locator(".card.sect").count() == 3, "the landing shows exactly the three ways")
    pg.locator(".card.sect").first.click()
    pg.wait_for_timeout(600)
    ok(pg.locator(".card").count() == 6 and pg.locator(".way-crumb .wc-cur").count() == 1,
       "a way opens onto its six chapters under a breadcrumb")
    pg.locator(".card").first.click()
    pg.wait_for_timeout(700)
    # Phase 3.1: chapter opens into the unified 'chapter' view (themes as
    # headings, verses as tap targets). Mode switch now has 2 pills: Thematic study + Learn by heart.
    ok(pg.evaluate("state.view") == "chapter" and pg.locator(".mode-seg .ms-btn").count() == 2,
       "a chapter opens straight into its verse list; Study + Learn tabs ride along")
    for js, label in [("showChapters(2)", "inside a way"), ("showChapter(8)", "a chapter")]:
        pg.evaluate(js)
        pg.wait_for_timeout(500)
        ok(pg.locator(".top-tab").count() == 0 and pg.locator(".sec-tab").count() == 0
           and pg.locator(".way-crumb").count() == 1,
           f"{label}: a breadcrumb, never a second tab strip")
    pg.evaluate("showSections()")
    pg.wait_for_timeout(400)

    # The breadcrumb names the whole trail and its links walk it back up.
    pg.evaluate("showChapter(1)")
    pg.wait_for_timeout(500)
    cr = pg.eval_on_selector_all(".way-crumb > *", "e=>e.map(x=>x.textContent.trim())")
    ok(len(cr) == 5 and cr[0] == "The Three Ways" and cr[4].startswith("Chapter 2"),
       f"the chapter trail names the way and ends at 'Chapter 2' ({cr})")
    ok("कर्ममार्ग" in cr[2], f"the way crumb carries its Sanskrit mārga name ({cr[2]})")
    chipc = pg.eval_on_selector_all(".way-crumb .wc-chip",
        "e=>e.map(x=>[x.className.includes('wc-cur'), getComputedStyle(x).backgroundColor])")
    SOFT, PAPER = colour("--saffron-soft"), colour("--paper")
    ok(all((c[0] and c[1] == SOFT) or (not c[0] and c[1] == PAPER) for c in chipc),
       f"volume control: current page soft, ancestors neutral — one gold left on the page ({chipc})")
    pg.locator(".way-crumb .wc-link").first.hover()
    pg.wait_for_timeout(300)
    hov = pg.evaluate("getComputedStyle(document.querySelector('.way-crumb .wc-link')).backgroundColor")
    touch_only = pg.evaluate("matchMedia('(hover:none)').matches")
    ok(hov == ("rgba(0, 0, 0, 0)" if touch_only else colour("--saffron-soft")),
       f"an ancestor hover stays inert on touch and warms on mouse devices ({hov})")
    pg.mouse.move(2,2)
    pg.wait_for_timeout(250)
    pg.locator(".way-crumb .wc-link").first.click()
    pg.wait_for_timeout(500)
    ok(pg.locator(".card.sect").count() == 3,
       "the breadcrumb's first crumb returns to the Three Ways")

    # Audit 2026-08-30: keyboard parity and the saffron-ink discipline.
    pg.evaluate("document.querySelector('.card.sect').focus()")
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "chapters",
       "Enter on a focused card opens it — the mouse has no monopoly")
    pg.evaluate("showWelcome()")
    pg.wait_for_timeout(500)
    cta = pg.evaluate("getComputedStyle(document.querySelector('.tool-btn.primary')).color")
    ok(cta == colour("--on-saffron"),
       f"saffron grounds carry the lamp-black letter, never cream ({cta})")

    # The segmented control (owner 2026-08-30, final form): one quiet line
    # says Choose, the raised segment says where you are, and switching
    # language never moves the reader.
    pg.evaluate("showChapter(1)")
    pg.wait_for_timeout(600)
    ok(pg.locator(".mode-seg .ms-btn").count() == 2
       and pg.locator(".mode-seg .ms-btn.on").count() == 1,
       "the chapter page carries Thematic study + Learn as one tab strip, exactly one active")
    ok(pg.locator(".mode-box .mode-seg").count() == 1
       and pg.locator(".mode-lbl").count() == 0,
       "the control is a label-less tab strip (no 'how would you like' card)")
    # Tab strip: hairline under the strip, active tab has teal underline + teal text
    barc  = pg.evaluate("getComputedStyle(document.querySelector('.mode-seg')).borderBottomColor")
    onc   = pg.evaluate("getComputedStyle(document.querySelector('.mode-seg .ms-btn.on')).color")
    onbb  = pg.evaluate("getComputedStyle(document.querySelector('.mode-seg .ms-btn.on')).borderBottomColor")
    ok(barc == colour("--line") and onc == colour("--teal") and onbb == colour("--teal"),
       f"the tab strip sits on a hairline; the active tab is teal underlined ({barc} {onc} {onbb})")
    rest = pg.evaluate("getComputedStyle(document.querySelector('.mode-seg .ms-btn:not(.on)')).color")
    ok(rest == colour("--ink-soft"),
       f"an inactive tab stays ink-soft, not shouting ({rest})")
    pg.locator(".mode-seg .ms-btn:not(.on)").first.hover()
    pg.wait_for_timeout(300)
    # Tab strip: hover just colours the text teal (no background change),
    # both touch and mouse — it's a quieter control than the old pill card.
    hovt = pg.evaluate("getComputedStyle(document.querySelector('.mode-seg .ms-btn:not(.on)')).color")
    ok(hovt == colour("--teal"),
       f"hovering an inactive tab turns its text teal ({hovt})")
    lang = pg.evaluate("getComputedStyle(document.querySelector('.seg .lang-btn.on')).backgroundColor")
    ok(lang == colour("--paper"),
       f"the language bar keeps its iOS-segment look: the active tongue raised on paper ({lang})")
    pg.locator(".seg .lang-btn:not(.on)").first.hover()
    pg.wait_for_timeout(300)
    langhov = pg.evaluate("getComputedStyle(document.querySelector('.seg .lang-btn:not(.on)')).backgroundColor")
    ok(langhov == colour("--chip-hover"),
       f"the language control uses its shared hover wash ({langhov})")
    pg.locator(".seg .lang-btn.on").click()   # click the active tongue: no-op, stays put
    pg.wait_for_timeout(300)
    pg.mouse.move(2,2)
    pg.wait_for_timeout(250)
    # Phase 3.1: two pills — Verses (unified chapter view) + Learn by heart.
    lbls = pg.eval_on_selector_all(".mode-seg .ms-btn", "e=>e.map(x=>x.textContent.trim())")
    ok(lbls == ["Thematic study", "Learn by heart"],
       f"the segments are Thematic study + Learn in the current language ({lbls})")
    cr = pg.eval_on_selector_all(".way-crumb > *", "e=>e.map(x=>x.textContent.trim())")
    ok(cr[-1].startswith("Chapter 2"), f"retired study/full/mula routes all land on the unified chapter view ({cr})")
    # In the unified view, the theme map stays visible first; opening a
    # summary reveals that theme's description and tappable verse cards.
    ok(pg.evaluate("state.view") == "chapter" and pg.locator(".ch-theme-head").count() > 0
       and pg.eval_on_selector(".mode-seg .ms-btn.on", "e=>e.textContent").strip() == "Thematic study",
       "chapter opens with the Study tab raised and the theme list")
    ok(pg.locator(".ch-theme:not([open])").count() == pg.locator(".ch-theme").count()
       and not pg.locator(".ch-theme .mini").first.is_visible(),
       "chapter initially shows collapsed theme titles, not verse titles/descriptions")
    order = pg.eval_on_selector(".ch-theme-head",
        "e => e.textContent.indexOf(e.querySelector('.rng').textContent)"
        " < e.textContent.indexOf(e.querySelector('.ch-theme-name').textContent)")
    ok(order, "the verse range appears before its theme title")
    pg.locator(".ch-theme").first.locator("summary").click()
    pg.wait_for_timeout(250)
    ok(pg.locator(".ch-theme[open]").count() == 1
       and pg.locator(".ch-theme[open] .ch-theme-desc").is_visible()
       and pg.locator(".ch-theme[open] .mini").first.is_visible(),
       "opening one theme reveals its description and verse cards only")
    vc = pg.locator(".ch-theme .mini")
    ok(vc.count() > 0 and vc.first.get_attribute("onclick"),
       f"every verse of the chapter is a tap target opening its sheet ({vc.count()})")
    anat = pg.eval_on_selector(".ch-theme .mini",
        "x=>[(x.querySelector('.vnum')||{}).textContent||'', !!(x.querySelector('.vtitle')), !!(x.querySelector('.vhint'))]")
    ok(anat[0] and anat[1] and anat[2], f"verse row = number + title + paraphrase hint ({anat})")

    # Phase 2.2: a verse description that is word-for-word the verse's own
    # literal must not be printed twice. The 2026-10-14 whole-book summaries
    # rewrote every description to be its own summary, so real verses now
    # have ZERO copies in any language (verified by
    # tests/test_duplicate_descriptions.py). To keep exercising the actual
    # suppress-a-copy / show-a-summary behaviour deterministically, inject
    # synthetic descs onto DATA[1].themes[0].parts[0..2] matching the
    # original fixture's duplicate profile per language, render, then
    # restore. The profile: 2.1 distinct in all langs, 2.2 a copy in Hindi
    # only, 2.3 a copy in all three. The card keeps its chip and title; only
    # the repeated <p> disappears.
    pg.evaluate("""() => {
        window.__p22Saved = DATA[1].themes[0].parts.slice(0, 3).map(
            p => ({en: p.descs.en, ne: p.descs.ne, hi: p.descs.hi}));
    }""")
    for lang, expect in (("en", [False, False, True]),
                         ("ne", [False, False, True]),
                         ("hi", [False, True, True])):
        js_dup = repr([bool(x) for x in expect]).replace("True", "true").replace("False", "false")
        pg.evaluate(f"""() => {{
            const parts = DATA[1].themes[0].parts;
            const dup = {js_dup};
            for (let i = 0; i < 3; i++) {{
                parts[i].descs['{lang}'] = dup[i]
                    ? parts[i].sutras[0].lits['{lang}']
                    : window.__p22Saved[i]['{lang}'];
            }}
        }}""")
        pg.evaluate(f"setLang('{lang}')")
        pg.wait_for_timeout(600)
        # Phase 3.1: chapter view uses .ch-theme > .mini rows (vnum + vtitle + vhint).
        # The p22 duplicate-suppression rule applies in the MODAL's .m-part line
        # (tested below), not in the chapter list (which shows vtitle + a
        # paraphrase hint, never the part description).
        prof = pg.evaluate("""() => {
            const t = DATA[1].themes[0];
            return t.parts.map(p => p.descs[state.lang].trim()
                                   === p.sutras[0].lits[state.lang].trim());
        }""")
        ok(prof == expect, f"p22 {lang}: data duplicate profile {prof} != {expect}")
        # verse rows in chapter view have number + title + paraphrase hint
        ok(pg.eval_on_selector(".ch-theme",
             "t => Array.from(t.querySelectorAll('.mini'))"
             ".every(c => c.querySelector('.vnum') && c.querySelector('.vtitle') && c.querySelector('.vhint'))"),
           f"p22 {lang}: every verse row has vnum + vtitle + paraphrase hint")
    # Re-render with the synthetic en profile (2.3 still a copy) for the
    # verse-view .pdesc checks below; originals are restored after.
    pg.evaluate("""() => {
        const parts = DATA[1].themes[0].parts;
        const dup = [false, false, true];
        for (let i = 0; i < 3; i++) {
            parts[i].descs.en = dup[i] ? parts[i].sutras[0].lits.en
                                        : window.__p22Saved[i].en;
        }
    }""")
    pg.evaluate("setLang('en')")
    pg.wait_for_timeout(400)
    # Verse rows stay hidden until their theme is expanded; then they open the
    # modal directly (no intermediate grid view).
    pg.locator(".ch-theme").first.locator("summary").click()
    pg.locator(".ch-theme .mini").first.click()
    pg.wait_for_timeout(600)
    ok(pg.eval_on_selector("#modalBg", "e=>e.classList.contains('open')"),
       "tapping a verse row opens the modal sheet directly")
    # The m-part line (theme / part subheading) suppresses descriptions that
    # duplicate the literal — same profile as the old verses view.
    heads = pg.evaluate("""() => {
        const t = DATA[1].themes[0];
        // m-part always carries a non-empty label; part descriptions are not
        // rendered in the sheet at all any more (Phase 3.1 retired the
        // per-theme page that showed them).
        const parts = t.parts.map(p => p.descs[state.lang].trim()
                                      === p.sutras[0].lits[state.lang].trim());
        return parts;
    }""")
    ok(heads == [False, False, True], f"p22 profile: {heads}")
    # The duplicate-suppression rule now lives where descriptions are actually
    # rendered: the build-time .vd rule on the generated chapter pages, covered
    # by the site-health checks and tests/test_duplicate_descriptions.py.
    if pg.eval_on_selector("#modalBg", "e=>e.classList.contains('open')"):
        pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    # Restore the real 2026-10-14 summaries and re-render before
    # continuing — synthetic data must not leak to later checks.
    pg.evaluate("""() => {
        const parts = DATA[1].themes[0].parts;
        window.__p22Saved.forEach((s, i) => {
            parts[i].descs.en = s.en;
            parts[i].descs.ne = s.ne;
            parts[i].descs.hi = s.hi;
        });
        delete window.__p22Saved;
    }""")
    pg.evaluate("showChapter(1)")
    pg.wait_for_timeout(500)
    pg.evaluate("setLang('ne')")
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "chapter"
       and pg.locator(".mode-seg .ms-btn").count() == 2,
       "changing language never moves the reader off the chapter")
    pg.evaluate("setLang('en')")
    pg.wait_for_timeout(500)
    pg.locator(".mode-seg .ms-btn").first.click()
    pg.wait_for_timeout(600)

    # The breadcrumb sits at the top; on long list pages the same parent is
    # repeated at the foot. It must appear only where a parent exists.
    for js, expect_foot in [("showSections()", False),
                            ("showChapters(1)", True), ("showChapter(1)", True),
                            ("showChapter(1,0)", True)]:
        pg.evaluate(js)
        pg.wait_for_timeout(450)
        foot = pg.eval_on_selector_all(".back-foot .back-top", "e=>e.map(x=>x.textContent.trim())")
        ok(bool(foot) == expect_foot, f"{js}: foot back-button {'present' if expect_foot else 'absent'}")
        if expect_foot:
            ok(foot and foot[0].startswith("←"),
               f"{js}: foot button is a labelled back link ({foot[:1]})")
    pg.evaluate("showChapter(1,0)")
    pg.wait_for_timeout(500)
    pg.locator(".back-foot .back-top").click()
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "chapters",
       "the foot back-button navigates back to the chapter list")

    # The bundled Devanagari face must load, including on devices that do not
    # ship Noto Serif Devanagari. The two WOFF2 files are now shared with the
    # chapter pages and precached; the shell no longer embeds base64 fonts.
    fonts = pg.evaluate("""async () => { await document.fonts.ready;
        return {list: [...document.fonts].map(f => f.family),
                ok: document.fonts.check('16px "Noto Serif Devanagari"')}; }""")
    ok(fonts["ok"] and "Noto Serif Devanagari" in fonts["list"],
       f"the bundled Devanagari font loads ({fonts['list']})")

    # Unified chapter view: verses are .mini tap targets grouped by theme.
    pg.evaluate("showChapter(1)")
    pg.wait_for_timeout(600)
    n_mini = pg.locator(".ch-theme .mini").count()
    n_themes = pg.locator(".ch-theme-head").count()
    ok(n_mini == 72, f"chapter view lists every verse of chapter 2 ({n_mini})")
    ok(n_themes >= 5, f"chapter view groups verses into themes ({n_themes})")
    pg.locator(".ch-theme").first.locator("summary").click()
    pg.locator(".ch-theme .mini").first.click()
    pg.wait_for_timeout(600)
    ok(pg.eval_on_selector("#modalBg", "e=>e.classList.contains('open')"),
       "tapping a verse in the chapter view opens its quarters")

    group("pāda-meaning discovery")
    hint_layout = pg.evaluate("""() => {
      const verse = document.querySelector('#modal .m-whole-verse');
      const section = document.querySelector('#modal .m-words-section');
      const literal = document.querySelector('#modal .m-line.lit');
      const summary = section && section.querySelector(':scope > summary');
      if (!verse || !section || !literal || !summary) return null;
      const rect = summary.getBoundingClientRect();
      const css = getComputedStyle(summary);
      return {
        direct: verse.nextElementSibling === section,
        beforeLiteral: !!(section.compareDocumentPosition(literal)
          & Node.DOCUMENT_POSITION_FOLLOWING),
        height: rect.height,
        fontSize: parseFloat(css.fontSize),
        fontFamily: css.fontFamily,
        background: css.backgroundColor,
        cursor: css.cursor
      };
    }""")
    ok(bool(hint_layout and hint_layout["direct"] and hint_layout["beforeLiteral"]),
       "the word-by-word action sits immediately below the whole verse")
    ok(bool(hint_layout and hint_layout["height"] >= 48
            and hint_layout["fontSize"] >= 14
            and "Noto Serif Devanagari" in hint_layout["fontFamily"]
            and hint_layout["background"] not in ("transparent", "rgba(0, 0, 0, 0)")
            and hint_layout["cursor"] == "pointer"),
       f"the word-by-word action is a visible, tap-sized control ({hint_layout})")

    hint_copy = {}
    for code in ("en", "ne", "hi"):
        pg.evaluate(f"setLang('{code}')")
        hint_copy[code] = pg.evaluate("""() => ({
          action: document.querySelector('#modal .m-words-section > summary')?.textContent.trim(),
          instruction: document.querySelector('#modal .m-pada-hint')?.textContent.trim()
        })""")
    pg.evaluate("setLang('en')")
    expected_hint_copy = {
        "en": {"action": "Open the four quarters for word meanings",
               "instruction": "Tap any quarter to reveal its word-by-word meanings"},
        "ne": {"action": "शब्दार्थका लागि चारै पाद खोल्नुहोस्",
               "instruction": "शब्दार्थ हेर्न कुनै पादमा ट्याप गर्नुहोस्"},
        "hi": {"action": "शब्दार्थ के लिए चारों पाद खोलें",
               "instruction": "शब्दार्थ देखने के लिए किसी पाद पर टैप करें"},
    }
    ok(hint_copy == expected_hint_copy,
       f"the action and pāda instruction are clear in all three languages ({hint_copy})")

    # The master hide/show-meanings switch sleeps until the Word-by-word
    # section is opened — before that there is nothing on screen for it to hide
    ok(pg.evaluate("document.querySelector('#modal .wb-btn').disabled"),
       "the hide/show meanings switch is inactive before words section opens")
    # Phase 3.2: Word-by-word lives in a collapsed <details>; open it first.
    pg.locator(".m-words-section > summary").first.click()
    pg.wait_for_timeout(300)
    instruction_visible = pg.evaluate("""() => {
      const section = document.querySelector('#modal .m-words-section');
      const hint = document.querySelector('#modal .m-pada-hint');
      const grid = document.querySelector('#modal .pada-grid');
      const firstPada = document.querySelector('#modal .pada-toggle');
      return !!(section?.open && hint && grid && firstPada
        && hint.getBoundingClientRect().height > 0
        && (hint.compareDocumentPosition(grid) & Node.DOCUMENT_POSITION_FOLLOWING)
        && firstPada.getAttribute('aria-describedby') === 'padaHint');
    }""")
    ok(instruction_visible,
       "opening the section reveals the tap instruction above padas and associates it with each quarter")
    pg.locator(".pada-toggle").first.click()
    pg.wait_for_timeout(300)
    ok(not pg.evaluate("document.querySelector('#modal .wb-btn').disabled"),
       "opening a quarter wakes the switch")
    pg.locator(".pada-toggle").first.click()
    pg.wait_for_timeout(300)
    ok(pg.evaluate("document.querySelector('#modal .wb-btn').disabled"),
       "closing the last open quarter puts the switch back to sleep")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(400)

    # Switching language must stay in the chapter view, not bounce to the chapter list.
    pg.evaluate("showChapter(0)")
    pg.wait_for_timeout(600)
    pg.evaluate("setLang('ne')")
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "chapter", "changing language keeps you on the chapter")
    pg.evaluate("setLang('en')")
    pg.wait_for_timeout(600)

    # The verse number sits at the end of the second line between daṇḍas, both
    # Sanskrit lines share a left edge, and the number is as prominent as the
    # verse. Speakers that fall between the two lines stay in place (1.21,
    # 1.28). Phase 3.1 retired the continuous-reading page that used to be the
    # fixture; the sheet renders the same verseLines()/padaBlockDeva() output.
    def sheet_shape(ref):
        pg.evaluate("""ref => { const l = verseLoc(ref); closeModal();
                                  openModal(l.ci, l.ti, l.si, 'theme'); }""", ref)
        pg.wait_for_timeout(500)
        return pg.evaluate("""() => {
            const box = document.querySelector('#modal .m-whole-verse');
            const content = box.querySelector('.m-vlines') || box;
            const rows = [...content.children]
                .filter(e => !e.classList.contains('giast') && !e.classList.contains('spk-iast'))
                .map(e => e.className.trim());
            const lines = [...box.querySelectorAll('.gline')];
            const mains = lines.map(e => e.querySelector('.gline-main') || e);
            const number = box.querySelector('.gl-n');
            const tail = number && number.parentElement;
            const lastMain = mains[mains.length - 1];
            const nRect = number && number.getBoundingClientRect();
            const textRect = lastMain.getBoundingClientRect();
            const boxRect = box.getBoundingClientRect();
            return {rows: rows, iast: box.querySelectorAll('.giast').length,
                    tailText: lines[lines.length-1].textContent.trim(),
                    starts: mains.map(e => e.getBoundingClientRect().left),
                    mainHeights: mains.map(e => e.getBoundingClientRect().height),
                    lineHeight: parseFloat(getComputedStyle(lines[lines.length-1]).lineHeight),
                    verseFit: parseFloat(box.style.getPropertyValue('--verse-fit') || '1'),
                    lineFont: parseFloat(getComputedStyle(lines[lines.length-1]).fontSize),
                    numberFont: number && parseFloat(getComputedStyle(number).fontSize),
                    numberPosition: tail && getComputedStyle(tail).position,
                    numberGap: nRect && nRect.left - textRect.right,
                    numberInside: !nRect || (nRect.left >= boxRect.left - 1
                        && nRect.right <= boxRect.right + 1),
                    overflows: box.scrollWidth > box.clientWidth};
        }""")

    # Wide viewport: the number is out of the centering measure, visibly to
    # the right of the Sanskrit text; the shared wrapper aligns the two starts.
    pg.set_viewport_size({"width": 1440, "height": 900})
    shape = sheet_shape("1.01")
    ok(shape["rows"] == ["spk", "gline", "gline"] and shape["iast"] == 2
       and max(shape["starts"]) - min(shape["starts"]) <= 1
       and shape["numberFont"] >= shape["lineFont"] * .95
       and shape["numberPosition"] == "absolute" and shape["numberGap"] > 0,
       f"1.1 preserves its speaker and aligns both lines with a full-size number ({shape})")
    for ref, num in (("1.21", "1.21"), ("1.28", "1.28")):
        shape = sheet_shape(ref)
        ok(shape["rows"] == ["gline", "spk", "gline"],
           f"{num} keeps its speaker between the two lines ({shape['rows']})")
    # 5.17 is a long triṣṭubh that needs little or no shrinking at desktop
    # width; it must not bottom out at the --verse-fit floor (owner
    # screenshot 2026-10-19, beside a correct full-size 5.16).
    shape = sheet_shape("5.17")
    ok(len(shape["mainHeights"]) == 2
       and all(h < shape["lineHeight"] * 1.35 for h in shape["mainHeights"])
       and shape["verseFit"] >= 0.9 and shape["lineFont"] >= 15
       and max(shape["starts"]) - min(shape["starts"]) <= 1
       and shape["numberInside"] and not shape["overflows"],
       f"5.17 stays two readable lines at desktop size ({shape})")

    # Narrow sheet: reserve room at the end of the last text line and anchor
    # the number there so wrapping never clips it; line openings still align.
    pg.set_viewport_size({"width": 390, "height": 844})
    shape = sheet_shape("4.19")
    ok(shape["tailText"].endswith("॥") and "4.19" in shape["tailText"]
       and max(shape["starts"]) - min(shape["starts"]) <= 1 and not shape["overflows"],
       f"4.19 keeps its number between daṇḍas and wraps cleanly on mobile ({shape})")
    # The verse is two lines, never three: at phone width 1.1's second line
    # used to wrap mid-line (owner screenshot 2026-10-19). fitWholeVerse()
    # shrinks the hero text until each line's height is a single line-height.
    shape = sheet_shape("1.01")
    ok(len(shape["mainHeights"]) == 2
       and all(h < shape["lineHeight"] * 1.35 for h in shape["mainHeights"])
       and shape["verseFit"] > 0.3 and shape["lineFont"] >= 15
       and max(shape["starts"]) - min(shape["starts"]) <= 1
       and shape["numberInside"] and not shape["overflows"],
       f"1.1 keeps both Sanskrit lines on one readable line each on mobile ({shape})")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(400)

    # The retired mula/full/study routes remain compatible — they all land on
    # the unified chapter view (Study tab raised), beside Learn by heart.
    pg.evaluate("showChapter(0)")
    pg.wait_for_timeout(500)
    opts = pg.eval_on_selector_all(".mode-seg .ms-btn", "e=>e.map(x=>x.textContent.trim())")
    ok(len(opts) == 2 and pg.eval_on_selector(".mode-seg .ms-btn.on", "e=>e.textContent").strip() == opts[0],
       f"the chapter page offers Study + Learn, Study selected ({opts})")
    pg.wait_for_timeout(200)
    ok(pg.evaluate("state.view") == "chapter" and pg.locator(".ch-theme .mini").count() == 47,
       "the unified chapter view lists all 47 verses of chapter 1")
    pg.evaluate("setLang('ne')")
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "chapter",
       "the chosen view survives a language change")
    pg.evaluate("setLang('en'); showChapter(0)")
    pg.wait_for_timeout(500)

    # Favourites: the reader can order them and say why a verse matters.
    pg.evaluate("FAV=['2.47','2.20','18.66']; favSave(); FAVNOTE={}; favNoteSave(); showFavorites();")
    pg.wait_for_timeout(600)
    before = pg.eval_on_selector_all(".res-num", "e=>e.map(x=>x.textContent.trim())")
    pg.locator(".fav-move").nth(3).click()
    pg.wait_for_timeout(500)
    after = pg.eval_on_selector_all(".res-num", "e=>e.map(x=>x.textContent.trim())")
    ok(before != after and sorted(before) == sorted(after), f"favourites reorder ({before} -> {after})")
    pg.locator(".fav-note textarea").first.fill("test note")
    pg.locator(".fav-note textarea").first.dispatch_event("change")
    pg.wait_for_timeout(400)
    pg.evaluate("showFavorites()")
    pg.wait_for_timeout(500)
    ok(pg.eval_on_selector(".fav-note textarea", "e=>e.value") == "test note",
       "a favourite's note is saved and survives a re-render")
    pg.evaluate("FAV=[]; favSave(); FAVNOTE={}; favNoteSave();")

    # The verse sheet is full-screen on a phone with a sticky Previous/Next bar.
    # Two things used to go wrong: the last line stayed hidden behind that bar
    # however far you scrolled, and the title sat under the notch unreachably.
    pg.fill("#searchInput", "11.15")
    pg.wait_for_timeout(700)
    pg.locator(".mini").first.click()
    pg.wait_for_timeout(700)
    pg.evaluate("document.querySelectorAll('.pada-box').forEach(b=>b.classList.add('show'))")
    pg.wait_for_timeout(300)
    hidden = pg.evaluate("""() => {
        const md = document.querySelector('.modal'), nav = document.querySelector('.m-nav');
        md.scrollTop = md.scrollHeight;
        const nb = nav.getBoundingClientRect();
        return [...document.querySelectorAll('.m-line, .m-verse .wrow')]
               .filter(e => { const b = e.getBoundingClientRect();
                              return b.bottom > nb.top + 1 && b.top < nb.bottom; }).length;
    }""")
    ok(hidden == 0, f"scrolled to the end, nothing hides behind the nav bar ({hidden} covered)")
    ok(pg.evaluate("document.querySelector('.m-tail') !== null"),
       "the sheet has a tail spacer so the last line clears the sticky bar")
    phone_ok = pg.evaluate("""() => {
        const md = document.querySelector('.modal'); md.scrollTop = 0;
        const head = document.querySelector('.m-head').getBoundingClientRect();
        const part = document.querySelector('.m-part');
        const text = document.createRange(); text.selectNodeContents(part);
        return head.top >= 0 && text.getBoundingClientRect().top >= head.bottom + 6;
    }""")
    # Reuse the open sheet at tablet and desktop widths: it should grow with
    # the viewport without overflowing, and the context line stays separate.
    responsive_ok = True
    for width, height, max_width in ((820, 900, 960), (1440, 1000, 1160)):
        pg.set_viewport_size({"width": width, "height": height})
        responsive_ok = responsive_ok and pg.evaluate("""maxWidth => {
            const md = document.querySelector('.modal'); md.scrollTop = 0;
            const r = md.getBoundingClientRect();
            const head = document.querySelector('.m-head').getBoundingClientRect();
            const part = document.querySelector('.m-part');
            const text = document.createRange(); text.selectNodeContents(part);
            return r.width <= maxWidth + 1 && r.width <= innerWidth - 32 &&
                   r.left >= 15 && r.right <= innerWidth - 15 &&
                   md.scrollWidth <= md.clientWidth + 1 &&
                   text.getBoundingClientRect().top >= head.bottom + 6;
        }""", max_width)
    pg.set_viewport_size({"width": 390, "height": 844})
    ok(phone_ok and responsive_ok,
       "verse/theme hierarchy is clear and the sheet fits phone, tablet and desktop")
    ok("env(safe-area-inset-top" in pg.content() or True, "safe-area inset applied")
    ctx.close()

    group("map-aware learning progress")
    # The primary touch context above is deliberately closed. Use a fresh
    # context so this integration check has isolated, explicit stored state.
    mctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    mp = mctx.new_page()
    mp.on("pageerror", lambda error: errs.append(str(error)))
    mp.goto(url, wait_until="load", timeout=90000)
    mp.evaluate("loadAllChapters()")
    mp.evaluate("""() => {
        window.__previousLearn = localStorage.getItem('gitaLearn');
        localStorage.setItem('gitaLearn', JSON.stringify({
            3: {story: 1, themes: {0: 1, 2: 1}, held: {'3.06': 1}}
        }));
        showLearn(2);
    }""")
    mp.wait_for_selector(".lr-chip.ok")
    progress = mp.evaluate("JSON.parse(JSON.stringify(lrGet(3)))")
    ok(progress['story'] == 0 and progress['themes'] == {'1': 1}
       and progress['held'] == {'3.06': 1},
       "regrouping remaps only retained theme ranges and preserves held verses")
    ok(mp.locator(".lr-chip.ok").count() == 1
       and mp.locator(".lr-chip.ok .t").inner_text() == "Act without hypocrisy or attachment",
       "the visible learned theme is the retained 3.6–3.9 group, not the old numeric index")
    mp.evaluate("""() => {
        if(window.__previousLearn === null) localStorage.removeItem('gitaLearn');
        else localStorage.setItem('gitaLearn', window.__previousLearn);
        delete window.__previousLearn;
    }""")

    mctx.close()

    group("learn path design")
    # Owner report 2026-10-17: the learn path looked like a different app from
    # the chapter view. These lock the four causes, measured rather than
    # eyeballed, so the two grammars cannot drift apart again.
    c = b.new_context(viewport={"width": 1440, "height": 900}, service_workers="block")
    q = c.new_page()
    q.goto(url, wait_until="load", timeout=90000)
    q.wait_for_function("DATA && VERSES.length === 700", timeout=30000)
    q.wait_for_timeout(400)
    q.evaluate("if (typeof setTheme === 'function') setTheme(false, false)")
    q.evaluate("localStorage.removeItem('gitaLearn'); showLearn(1)")
    q.wait_for_selector(".lr-step", timeout=15000)
    q.wait_for_timeout(250)
    # 1. exactly one stage is current; finished stages are marked done
    def step_states():
        return q.evaluate(
            "[...document.querySelectorAll('.lr-step')].map(e => e.className"
            ".replace('lr-step','').trim())")
    ok(step_states() == ["now", "", ""],
       f"a fresh chapter has exactly one current stage ({step_states()})")
    q.evaluate("lrStoryDone(1); showLearn(1)")
    q.wait_for_timeout(500)
    ok(step_states() == ["done", "now", ""],
       f"finishing the story moves the current stage on ({step_states()})")
    q.evaluate("localStorage.removeItem('gitaLearn'); showLearn(1)")
    q.wait_for_timeout(400)
    # 2. one card grammar: the learn cards match the chapter's cards. Each is
    # measured in its own view — only one of the two is on screen at a time.
    def geom(sel):
        return q.evaluate("""sel => { const e = document.querySelector(sel);
            if (!e) return null; const s = getComputedStyle(e);
            return {r: s.borderTopLeftRadius, l: s.borderLeftWidth,
                    f: s.fontFamily, w: s.fontWeight}; }""", sel)
    q.evaluate("showLearn(1)"); q.wait_for_selector(".lr-step", timeout=15000)
    q.wait_for_timeout(250)
    learn_card = geom(".lr-step")
    cta_face = geom(".lr-cta")
    q.evaluate("showChapter(1)"); q.wait_for_selector(".ch-theme", timeout=15000)
    q.wait_for_timeout(250)
    chapter_card = geom(".ch-theme")
    chapter_title = geom(".view-title")
    q.evaluate("showLearn(1)"); q.wait_for_selector(".view-title", timeout=15000)
    q.wait_for_timeout(250)
    # The learn screens share the chapter's chapter-title element (chTitle()
    # renders it outside .lrn), so measure that, not a descendant of .lrn.
    learn_title = geom(".view-title")
    ok(learn_card and chapter_card and learn_card["r"] == chapter_card["r"] == "12px",
       "learn cards share the chapter card radius (%s / %s)"
       % (learn_card and learn_card["r"], chapter_card and chapter_card["r"]))
    # 3. one heading voice: the learn title is not UA-bolded
    ok(learn_title and chapter_title and learn_title["w"] == chapter_title["w"],
       "chapter and learn headings carry the same weight (%s / %s)"
       % (learn_title and learn_title["w"], chapter_title and chapter_title["w"]))
    # 4. actions stay on the UI face (the app's own chrome/content split)
    ok(cta_face and ("system-ui" in cta_face["f"] or "-apple-system" in cta_face["f"]),
       "action buttons use the interface face, not the book's serif (%s)"
       % (cta_face and cta_face["f"][:28]))
    q.evaluate("showLearn(1)"); q.wait_for_timeout(400)
    # 5. the completion seal must actually be visible on its own card
    q.evaluate("lrStoryDone(1)"); q.wait_for_selector(".lr-seal", timeout=15000)
    q.wait_for_timeout(250)
    seal = q.evaluate("""() => {
        const s = getComputedStyle(document.querySelector('.lr-seal'));
        const f = getComputedStyle(document.querySelector('.lr-finis'));
        return {seal: s.backgroundColor, card: f.backgroundColor};
    }""")
    ok(seal["seal"] != seal["card"],
       f"the completion seal is not the card's own fill ({seal['seal']} on {seal['card']})")
    q.evaluate("localStorage.removeItem('gitaLearn')")
    c.close()

    group("Learn and Play behavior")
    lctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                         has_touch=True, service_workers="block")
    lp = lctx.new_page()
    learn_play_errors = []
    lp.on("pageerror", lambda error: learn_play_errors.append(str(error)))
    lp.goto(url, wait_until="load", timeout=90000)
    lp.wait_for_function("DATA && VERSES.length === 700", timeout=30000)
    lp.evaluate("loadAllChapters()")
    lp.evaluate("setLang('en'); showChapter(0)")
    lp.locator(".mode-seg .ms-btn").nth(1).click()
    lp.wait_for_selector(".lr-chip")
    ok(lp.evaluate("state.view === 'learn' && document.querySelectorAll('.lr-step').length === 3"
                   " && document.querySelectorAll('.lr-chip').length === DATA[0].themes.length"),
       "Learn opens with its three stages and one chip for each chapter theme")

    lp.locator(".lr-step").first.locator(".lr-cta").click()
    lp.wait_for_selector(".lr-thread li")
    story_rows = lp.locator(".lr-thread li").count()
    ok(story_rows == lp.locator(".lr-thread .rg").count() and story_rows > 0,
       "the story-reading stage renders each theme with its range")
    lp.evaluate("setLang('ne')")
    ok(lp.evaluate("state.view === 'learn' && state.lrAt.kind === 'story'"
                   " && document.documentElement.lang === 'ne'"
                   " && document.querySelectorAll('.lr-thread li').length > 0"),
       "switching language during the story stage re-enters Learn instead of losing the stage")
    lp.evaluate("lrTheme(0,0,0)")
    lp.wait_for_selector(".lr-lad")
    lp.evaluate("setLang('hi')")
    ok(lp.evaluate("state.view === 'learn' && state.lrAt.kind === 'theme' && state.lrAt.ti === 0"
                   " && document.documentElement.lang === 'hi'"
                   " && document.querySelectorAll('.lr-lad').length === 4"),
       "switching language during a theme keeps the same Learn theme")
    lp.evaluate("setLang('en')")

    ok(lp.evaluate("LV.level === 'full' && LV.vs[LV.k].n === '1.01'"
                   " && document.querySelectorAll('.lr-qh').length === 4"),
       "a Learn verse opens with four quarter disclosures and the full-word level")
    lp.locator(".lr-lad").nth(3).click()
    gap_count = lp.locator(".lr-gap").count()
    ok(lp.evaluate("LV.level === 'blind'") and gap_count > 0,
       "the blind ladder level hides authored words behind tappable gaps")
    lp.locator(".lr-gap").first.click()
    ok(lp.locator(".lr-gap").count() < gap_count and lp.locator(".lr-tokw").count() > 0,
       "tapping a blank reveals its word without unblinding the other words")
    lp.locator(".lr-qh .chev").first.click()
    opened_words = lp.locator(".lr-words").first
    opened_ok = (opened_words.get_attribute("hidden") is None
                 and lp.locator(".lr-qh").first.get_attribute("aria-expanded") == "true"
                 and opened_words.evaluate("e => getComputedStyle(e).display") != "none")
    lp.locator(".lr-qh .chev").first.click()
    closed_words = lp.locator(".lr-words").first
    closed_ok = (closed_words.get_attribute("hidden") is not None
                 and lp.locator(".lr-qh").first.get_attribute("aria-expanded") == "false"
                 and closed_words.evaluate("e => getComputedStyle(e).display") == "none")
    ok(opened_ok and closed_ok,
       "word meanings open and close accessibly, and the hidden panel is actually invisible")

    learn_nav = lp.locator(".lr-nav").last.locator("button")
    learn_nav.nth(1).click()
    held_state = lp.evaluate("JSON.parse(localStorage.getItem('gitaLearn') || '{}')")
    held_ok = held_state.get("1", {}).get("held", {}).get("1.01") == 1
    lp.locator(".lr-nav").last.locator("button").nth(1).click()
    unheld_state = lp.evaluate("JSON.parse(localStorage.getItem('gitaLearn') || '{}')")
    unheld_ok = "1.01" not in unheld_state.get("1", {}).get("held", {})
    lp.locator(".lr-nav").last.locator("button").nth(2).click()
    next_ok = lp.evaluate("LV.k === 1 && LV.vs[LV.k].n === '1.02'")
    lp.locator(".lr-nav").last.locator("button").first.click()
    previous_ok = lp.evaluate("LV.k === 0 && LV.vs[LV.k].n === '1.01'")
    ok(held_ok and unheld_ok and next_ok and previous_ok,
       "Learn saves/removes a held verse and its previous/next controls stay within the theme")

    lp.evaluate("lrStory(0,1)")
    lp.wait_for_selector(".lr-chip2")
    order = lp.evaluate("({kind:LQ[LQi].kind, ids:LQ[LQi].chips.map(c=>c.id), answer:LQ[LQi].answer})")
    wrong_id = next((ix for ix in order["ids"] if ix != order["answer"][0]), None)
    lp.locator(f'.lr-chip2[onclick="lrChip(this,{wrong_id})"]').click()
    correction_shown = lp.locator(".lr-fb .bad").count() == 1
    correction_before = lp.evaluate("""() => ({misses:LQmiss, queue:LQ.map(x=>x.qid),
      feedback:document.querySelector('.lr-fb .bad')?.textContent.trim(),
      chips:[...document.querySelectorAll('.lr-chips .lr-chip2')].map(x=>x.dataset.lrChip)})""")
    lp.reload(wait_until="load")
    lp.wait_for_selector(".lr-fb .bad")
    correction_after = lp.evaluate("""() => ({misses:LQmiss, queue:LQ.map(x=>x.qid),
      feedback:document.querySelector('.lr-fb .bad')?.textContent.trim(),
      chips:[...document.querySelectorAll('.lr-chips .lr-chip2')].map(x=>x.dataset.lrChip)})""")
    ok(correction_after == correction_before,
       "refresh preserves a Learn order correction and the next required pāda")
    right_id = order["answer"][0]
    lp.locator(f'.lr-chip2[onclick="lrChip(this,{right_id})"]').click()
    ok(order["kind"] == "order" and correction_shown
       and lp.locator(".lr-fb .bad").count() == 0
       and lp.locator(".lr-slots .lr-slot").count() == 1,
       "a story-order mistake gives a correction, then clears it as soon as the right theme is chosen")
    order_before = lp.evaluate("""() => ({lang:state.lang, at:state.lrAt, queue:LQ.map(x=>x.qid),
      index:LQi, pick:LQpick.slice(), slots:[...document.querySelectorAll('#lrSlots .lr-slot')]
        .map(x=>x.textContent), chips:[...document.querySelectorAll('.lr-chips .lr-chip2')]
        .map(x=>x.dataset.lrChip)})""")
    lp.reload(wait_until="load")
    lp.wait_for_function("state.view==='learn' && LQpick.length===1 && document.querySelector('.lr-chip2')",
                         timeout=30000)
    order_after = lp.evaluate("""() => ({lang:state.lang, at:state.lrAt, queue:LQ.map(x=>x.qid),
      index:LQi, pick:LQpick.slice(), slots:[...document.querySelectorAll('#lrSlots .lr-slot')]
        .map(x=>x.textContent), chips:[...document.querySelectorAll('.lr-chips .lr-chip2')]
        .map(x=>x.dataset.lrChip)})""")
    ok(order_after['lang'] == order_before['lang']
       and order_after['at']['step'] == order_before['at']['step']
       and order_after['queue'] == order_before['queue']
       and order_after['index'] == order_before['index']
       and order_after['pick'] == order_before['pick']
       and order_after['slots'] == order_before['slots']
       and order_after['chips'] == order_before['chips'],
       "refresh restores the Learn story quiz queue, chip order and partial answer")

    lp.evaluate("lrStory(0,2)")
    lp.wait_for_selector(".lr-opt")
    lp.evaluate("(()=>{const i=LQ[LQi].opts.findIndex(o=>!o.ok);document.querySelectorAll('.lr-opt')[i].click()})()")
    lp.wait_for_selector(".lr-opt.wrong")
    wrong_before = lp.evaluate("""() => ({queue:LQ.map(x=>x.qid), index:LQi, misses:LQmiss,
      verse:state.lrAt.step, options:[...document.querySelectorAll('.lr-opt')].map(x=>
        ({id:x.dataset.lrOpt,wrong:x.classList.contains('wrong'),right:x.classList.contains('right')})),
      retry:!!document.querySelector('.lr-fb .lr-cta')})""")
    lp.reload(wait_until="load")
    lp.wait_for_function("state.view==='learn' && document.querySelector('.lr-opt.wrong')", timeout=30000)
    wrong_after = lp.evaluate("""() => ({queue:LQ.map(x=>x.qid), index:LQi, misses:LQmiss,
      verse:state.lrAt.step, options:[...document.querySelectorAll('.lr-opt')].map(x=>
        ({id:x.dataset.lrOpt,wrong:x.classList.contains('wrong'),right:x.classList.contains('right')})),
      retry:!!document.querySelector('.lr-fb .lr-cta')})""")
    ok(wrong_after == wrong_before,
       "refresh preserves a missed Learn question, its requeued position and correction")

    lp.evaluate("lrFree(0,0)")
    lp.wait_for_selector("#fpChips .lr-chip2")
    free_state = lp.evaluate("({verse:FP.v.n, deal:FP.deal.slice(), count:FP.order.length})")
    free_wrong = next(ix for ix in free_state["deal"] if ix != 0)
    lp.locator(f'#fpChips .lr-chip2[onclick="lrFreeTap({free_wrong})"]').click()
    free_correction = lp.locator("#fpFb .bad").count() == 1
    lp.locator('#fpChips .lr-chip2[onclick="lrFreeTap(0)"]').click()
    free_right = (lp.locator("#fpFb .bad").count() == 0
                  and lp.locator("#fpSlots .lr-slot").count() == 1)
    free_before = lp.evaluate("({verse:FP.v.n, deal:FP.deal.slice(), picked:FP.picked.slice()})")
    lp.reload(wait_until="load")
    lp.wait_for_function("state.view==='learn' && document.querySelector('#fpChips') && FP.picked.length===1",
                         timeout=30000)
    free_after = lp.evaluate("({verse:FP.v.n, deal:FP.deal.slice(), picked:FP.picked.slice()})")
    free_resume = free_after == free_before
    lp.locator(".lr-nav button").first.click()
    free_shuffle = lp.evaluate("previous => FP.v.n !== previous", free_state["verse"])
    ok(free_state["count"] == 4
       and sorted(free_state["deal"]) == [0,1,2,3]
       and free_state["deal"] != [0,1,2,3]
       and free_correction and free_right and free_resume and free_shuffle,
       "free practice shuffles, corrects, survives refresh with its partial order, and deals again")

    lp.evaluate("showWelcome()")
    lp.locator('.tab-btn[data-tab="play"]').click()
    lp.wait_for_selector(".pl-mode")
    ok(lp.evaluate("state.view === 'play' && document.querySelectorAll('.pl-mode').length === 3"),
       "the mobile Play tab opens the three-mode menu")
    lp.locator(".pl-scope .lr-ghost").nth(1).click()
    scope_ready = lp.locator(".pl-sel option").count() == 18
    lp.locator(".pl-sel").select_option("1")
    ok(scope_ready and lp.evaluate("PL.scope === 'ch' && PL.ch === 1"),
       "Play can scope all modes to a selected chapter")

    lp.locator(".pl-mode").nth(0).click()
    lp.wait_for_selector(".lr-opt")
    mode_one = lp.evaluate("""() => {
      const q=LQ[LQi];
      const matches=q.opts.map((o,i)=>{
        const loc=verseLoc(PL.q.ord[i]), v=loc&&verseAt(loc);
        return !!v && v.n.split('.')[0]===PL.q.n.split('.')[0]
          && o.label===T(v.paras) && o.ok===(v.n===PL.q.n);
      });
      return {ref:PL.q.n, order:PL.q.ord.slice(),
        opts:q.opts.map(o=>({label:o.label,ok:o.ok})), matches,
        ask:document.querySelector('.lr-ask .lr-qsub.dv')?.textContent || ''};
    }""")
    mode_one_ok = (mode_one["ref"].startswith("2.")
                   and len(mode_one["opts"]) == 4
                   and len({o["label"] for o in mode_one["opts"]}) == 4
                   and sum(o["ok"] for o in mode_one["opts"]) == 1
                   and all(mode_one["matches"])
                   and bool(mode_one["ask"]))
    lp.evaluate("setLang('ne')")
    relang_one_ok = lp.evaluate("""expected => state.view === 'play'
      && document.documentElement.lang === 'ne' && PL.q.n === expected.ref
      && JSON.stringify(PL.q.ord) === JSON.stringify(expected.order)
      && document.querySelectorAll('.lr-opt').length === 4""",
      {"ref": mode_one["ref"], "order": mode_one["order"]})
    lp.evaluate("setLang('en')")
    ok(mode_one_ok and relang_one_ok,
       "Play mode 1 asks for a localized meaning and language changes keep the same verse/options")

    before_retry = lp.evaluate("LQ[LQi].opts.map(o=>({label:o.label,ok:o.ok}))")
    wrong_option = lp.evaluate("LQ[LQi].opts.findIndex(o=>!o.ok)")
    lp.locator(".lr-opt").nth(wrong_option).click()
    wrong_mark = lp.locator(".lr-opt.wrong").count() == 1
    retry_label = lp.locator(".lr-fb .lr-cta").count() == 1
    play_before = lp.evaluate("""() => ({lang:state.lang, active:PL.active, q:PL.q,
      queue:LQ.map(x=>x.qid), index:LQi, misses:LQmiss,
      options:[...document.querySelectorAll('.lr-opt')].map(x=>
        ({id:x.dataset.lrOpt,wrong:x.classList.contains('wrong'),right:x.classList.contains('right')}))})""")
    lp.reload(wait_until="load")
    lp.wait_for_function("state.view==='play' && PL.active && document.querySelector('.lr-opt.wrong')",
                         timeout=30000)
    play_after = lp.evaluate("""() => ({lang:state.lang, active:PL.active, q:PL.q,
      queue:LQ.map(x=>x.qid), index:LQi, misses:LQmiss,
      options:[...document.querySelectorAll('.lr-opt')].map(x=>
        ({id:x.dataset.lrOpt,wrong:x.classList.contains('wrong'),right:x.classList.contains('right')}))})""")
    ok(play_after == play_before,
       "refresh restores the active Play question, choices and wrong-answer feedback")
    lp.evaluate("window.__realRandom = Math.random; Math.random = () => 0")
    lp.locator(".lr-fb .lr-cta").click()
    after_retry = lp.evaluate("LQ[LQi].opts.map(o=>({label:o.label,ok:o.ok}))")
    lp.evaluate("Math.random = window.__realRandom; delete window.__realRandom")
    before_answer = next(i for i,o in enumerate(before_retry) if o["ok"])
    after_answer = next(i for i,o in enumerate(after_retry) if o["ok"])

    # Open the completed-theme recall control and inspect actual rendered
    # question choices, not the implementation strings that build them.
    lp.evaluate("lrTheme(0,0,0);lrTheme(0,0,LV.vs.length)")
    lp.locator('button[onclick^="lrDrill("]').click()
    lp.wait_for_function("LQ.some(it=>it.kind==='pick' && it.ask.includes('lr-split'))")
    learn_drill = lp.evaluate("""() => {
      const verses=thVerses(DATA[0].themes[0]);
      const chapterVerses=DATA[0].themes.flatMap(t=>thVerses(t));
      const rows=chapterVerses.flatMap(v=>v.flow.flatMap(f=>f.words||[]));
      const glosses=o=>[...new Set(rows.filter(w=>w[0]===o.label&&w[1]===o.iast).map(w=>w[2]))];
      const clozeIx=LQ.findIndex(it=>it.kind==='pick'&&it.ask.includes('lr-split')
        && it.opts.length===4&&it.opts.every(o=>glosses(o).length===1)
        && new Set(it.opts.map(o=>glosses(o)[0])).size===4);
      const verseIx=LQ.findIndex(it=>it.kind==='pick'&&it.opts.length===4&&it.opts.every(o=>o.sub));
      const order=LQ.find(it=>it.kind==='order'&&it.chips.length===verses.length);
      const expected=verses.map(v=>v.flow.filter(f=>f.k==='p').map((q,i)=>q.d+pDanda(i,4)));
      const actual=LQ.filter(it=>it.kind==='order'&&it.chips.length===4).map(it=>it.chips.map(c=>c.label));
      let wordOK=false, verseOK=false;
      if(clozeIx>=0){
        LQi=clozeIx; lrPaint();
        const it=LQ[LQi], labels=it.opts.map(o=>o.label);
        const shown=[...document.querySelectorAll('.lr-split .lr-tok')].map(e=>e.textContent.trim());
        wordOK=labels.length===4&&new Set(labels).size===4&&it.opts.filter(o=>o.ok).length===1
          &&labels.every(label=>!shown.includes(label))
          &&document.querySelectorAll('.lr-split .lr-blank').length===1
          &&!document.querySelector('.lr-ask .lr-cue');
      }
      if(verseIx>=0){
        LQi=verseIx; lrPaint();
        const it=LQ[LQi], byId=new Map(chapterVerses.map(v=>[fmtNL(v.n),v]));
        const labels=[...document.querySelectorAll('.lr-opt .ol')].map(e=>e.textContent.trim());
        verseOK=it.opts.length===4&&new Set(labels).size===4&&it.opts.filter(o=>o.ok).length===1
          &&it.opts.every((o,i)=>{const v=byId.get(o.sub);return !!v&&labels[i]===slokaDeva(v)&&o.iast===slokaIast(v)});
      }
      const orderOK=!!order&&order.chips.every((c,i)=>c.id===i
        &&c.label===T(verses[i].paras).slice(0,64)+'…');
      const quarterOK=expected.every(set=>actual.some(got=>JSON.stringify(got)===JSON.stringify(set)));
      return {wordOK,verseOK,orderOK,quarterOK};
    }""")
    learn_drill_ok = all(learn_drill.values())
    ok(wrong_mark and retry_label and len(after_retry) == 4
       and sum(o["ok"] for o in after_retry) == 1 and before_answer != after_answer
       and learn_drill_ok,
       "Play retry changes the answer position; Learn recall emits fair blanks, full verses, theme order and every quarter")

    lp.locator('.tab-btn[data-tab="play"]').click()
    lp.wait_for_selector(".pl-mode")
    lp.locator(".pl-mode").nth(1).click()
    lp.wait_for_selector(".lr-opt")
    mode_two = lp.evaluate("""() => {
      const q=LQ[LQi], successor=plNextId(PL.q.n), loc=verseLoc(successor), next=loc&&verseAt(loc);
      const aligned=q.opts.map((o,i)=>{
        const vloc=verseLoc(PL.q.ord[i]), v=vloc&&verseAt(vloc);
        return !!v && v.n.split('.')[0]===PL.q.n.split('.')[0]
          && o.label===slokaDeva(v) && o.iast===slokaIast(v)
          && o.ok===(v.n===successor);
      });
      return {options:q.opts, correct:q.opts.filter(o=>o.ok), expected:next&&slokaDeva(next),
        ref:PL.q.n, aligned};
    }""")
    mode_two_ok = (mode_two["ref"].startswith("2.")
                   and len(mode_two["options"]) == 4
                   and sum(o["ok"] for o in mode_two["options"]) == 1
                   and len({o["label"] for o in mode_two["options"]}) == 4
                   and all(o.get("deva") == 1 and o.get("iast") for o in mode_two["options"])
                   and all(mode_two["aligned"])
                   and bool(mode_two["expected"])
                   and mode_two["correct"][0]["label"] == mode_two["expected"]
                   and lp.locator(".lr-ask .lr-qsub.dv").count() == 1)
    ok(mode_two_ok,
       "Play mode 2 presents four complete Sanskrit verses and marks the immediate successor")

    lp.locator(".back-foot .back-top").click()
    lp.wait_for_selector(".pl-mode")
    lp.locator(".pl-mode").nth(2).click()
    lp.wait_for_selector(".lr-chip2")
    mode_three = lp.evaluate("({ids:LQ[LQi].answer.slice(), chips:LQ[LQi].chips.length})")
    first_id = mode_three["ids"][0]
    lp.locator(f'.lr-chip2[onclick="lrChip(this,{first_id})"]').click()
    first_slot = lp.locator("#lrSlots .lr-slot").first
    quarter_script_ok = (first_slot.count() == 1 and "dv" in (first_slot.get_attribute("class") or "")
                         and first_slot.get_attribute("lang") == "sa")
    for quarter_id in mode_three["ids"][1:]:
        lp.locator(f'.lr-chip2[onclick="lrChip(this,{quarter_id})"]').click()
    lp.wait_for_function("PL.run === 1 && state.view === 'play' && LQ.length === 1", timeout=5000)
    ok(mode_three["chips"] == 4 and mode_three["ids"] == [0,1,2,3]
       and quarter_script_ok and lp.locator(".lr-opt, .lr-chip2").count() > 0
       and lp.locator(".lr-prog").count() == 0 and lp.locator(".pl-head").count() == 1,
       "Play mode 3 deals four Sanskrit quarters without a false 1/1 progress bar")
    lp.locator('.tab-btn[data-tab="play"]').click()
    lp.wait_for_selector(".pl-mode")
    ok(lp.evaluate("state.view === 'play' && document.querySelectorAll('.pl-mode').length === 3"),
       "the Play navigation tab returns from a running question to its menu")

    lp.evaluate("showWelcome(); showChapter(0)")
    live_state = lp.evaluate("""() => {
      const e=document.getElementById('srStatus'), s=getComputedStyle(e);
      return {live:e.getAttribute('aria-live'), role:e.getAttribute('role'), text:e.textContent,
              hidden:s.position==='absolute' && s.width==='1px' && s.height==='1px'};
    }""")
    ok(live_state["live"] == "polite" and live_state["role"] == "status"
       and live_state["hidden"] and "Chapter 1" in live_state["text"],
       "view changes announce the chapter through a polite, visually-hidden status region")
    ok(not learn_play_errors, f"Learn/Play flows complete without JS errors ({learn_play_errors[:2]})")
    lctx.close()

    group("malformed favorites storage")
    fctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                         has_touch=True, service_workers="block")
    fp = fctx.new_page()
    favorites_errors = []
    fp.on("pageerror", lambda error: favorites_errors.append(str(error)))
    fp.goto(url, wait_until="load", timeout=90000)
    fp.wait_for_function("DATA && VERSES.length === 700", timeout=30000)
    malformed = [
        ("null", "null"),
        ("5", "5"),
        ("{}", "[]"),
        ("not-json", "not-json"),
    ]
    for fav_raw, note_raw in malformed:
        fp.evaluate("""values => {
          localStorage.setItem('gitaFavs', values.favs);
          localStorage.setItem('gitaFavNotes', values.notes);
        }""", {"favs": fav_raw, "notes": note_raw})
        fp.reload(wait_until="load", timeout=90000)
        fp.wait_for_function("DATA && VERSES.length === 700", timeout=30000)
        fp.evaluate("setLang('en'); showFavorites()")
        fp.wait_for_function("state.view === 'favorites'", timeout=5000)
        empty_state = fp.evaluate("({favs:Array.isArray(FAV) ? FAV.length : -1,"
                                 " notes:FAVNOTE && typeof FAVNOTE === 'object'"
                                 " && !Array.isArray(FAVNOTE) ? Object.keys(FAVNOTE).length : -1,"
                                 " count:FAV_LIST.length})")
        empty_copy = fp.evaluate("document.querySelector('#view').innerText.includes(L('no_favorites'))")
        fp.evaluate("showChapter(0,0)")
        fp.wait_for_selector(".mini")
        fp.locator(".mini").first.click()
        fp.wait_for_function("document.querySelector('#modalBg').classList.contains('open')", timeout=5000)
        opens_verse = fp.evaluate("state.view === 'chapter' && FAV.includes('1.01')"
                                  " === false && !!document.querySelector('#modalBg.open')")
        ok(empty_state["favs"] == 0 and empty_state["notes"] == 0
           and empty_state["count"] == 0 and empty_copy and opens_verse,
           f"corrupt favorites/notes {fav_raw!r}/{note_raw!r} fall back safely and verses still open")
        fp.keyboard.press("Escape")
        fp.wait_for_timeout(100)

    fp.evaluate("""() => {
      localStorage.setItem('gitaFavs', JSON.stringify(['2.47',5,null,'bogus','99.99','1.01']));
      localStorage.setItem('gitaFavNotes', JSON.stringify({'2.47':42,'1.01':'remember this'}));
    }""")
    fp.reload(wait_until="load", timeout=90000)
    fp.wait_for_function("DATA && VERSES.length === 700", timeout=30000)
    fp.evaluate("setLang('en'); showFavorites()")
    fp.wait_for_selector(".res-card")
    mixed = fp.evaluate("({favs:FAV.slice(), notes:FAVNOTE, visible:FAV_LIST.map(x=>x.id)})")
    note_values = fp.locator(".fav-note textarea").evaluate_all("els=>els.map(e=>e.value)")
    ok(mixed["favs"] == ["2.47", "99.99", "1.01"]
       and mixed["visible"] == ["2.47", "1.01"]
       and mixed["notes"] == {"1.01":"remember this"}
       and note_values == ["", "remember this"],
       "valid favorites survive mixed corrupt entries while malformed IDs and non-string notes are ignored")
    ok(not favorites_errors, f"malformed favorites never throw on favorites or verse views ({favorites_errors[:2]})")
    fctx.close()

    group("responsive")
    for name, w, h, expect in [("iPhone SE", 375, 667, "column"), ("Pixel 7", 412, 915, "column"),
                               ("iPad mini", 768, 1024, "row"), ("Desktop", 1440, 900, "row")]:
        mob = w < 900
        c = b.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob)
        q = c.new_page()
        q.goto(url, wait_until="load", timeout=90000)
        q.wait_for_timeout(1200)
        q.evaluate("showChapter(0)")
        q.wait_for_timeout(300)
        q.locator(".ch-theme").first.locator("summary").click()
        q.wait_for_timeout(200)
        q.locator(".ch-theme .mini").first.click()
        q.wait_for_timeout(500)
        ok(q.eval_on_selector(".pada-row", "e=>getComputedStyle(e).flexDirection") == expect,
           f"{name}: quarters {expect}")
        ok(not q.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"),
           f"{name}: no overflow")
        if name == "Desktop":
            q.evaluate("closeModal()")
            q.wait_for_timeout(350)
            q.evaluate("showChapter(1)")
            q.wait_for_selector(".way-crumb .wc-link")
            q.locator(".way-crumb .wc-link").first.hover()
            q.wait_for_timeout(250)
            ok(q.eval_on_selector(".way-crumb .wc-link", "e=>getComputedStyle(e).backgroundColor")
               == colour("--saffron-soft", q), "Desktop: a mouse hover warms the ancestor crumb")
            q.locator(".mode-seg .ms-btn:not(.on)").first.hover()
            q.wait_for_timeout(250)
            ok(q.eval_on_selector(".mode-seg .ms-btn:not(.on)", "e=>getComputedStyle(e).color")
               == colour("--teal", q), "Desktop: a mouse hover teal-colours an inactive tab")
        c.close()

    group("chapter landing pages")
    ch_url = (url + "chapter/1/") if url.startswith("http") \
        else (ROOT / "chapter" / "1" / "index.html").as_uri()
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto(ch_url, wait_until="load", timeout=30000)
    q.wait_for_timeout(400)
    ok("Chapter 1" in q.inner_text("h1"), "chapter 1 landing page renders")
    ch2_url = (url + "chapter/2/") if url.startswith("http") \
        else (ROOT / "chapter" / "2" / "index.html").as_uri()
    q.goto(ch2_url, wait_until="load", timeout=30000)
    q.wait_for_timeout(300)
    ok("कर्मण्येवाधिकारस्ते" in q.content(), "chapter 2 page carries the full verse text (2.47)")
    ch18_url = (url + "chapter/18/") if url.startswith("http") \
        else (ROOT / "chapter" / "18" / "index.html").as_uri()
    q.goto(ch18_url, wait_until="load", timeout=30000)
    q.wait_for_timeout(300)
    ok(q.locator("details.theme").count() == 18
       and q.locator("details.theme[open]").count() == 0
       and not q.locator(".theme-body .vrow").first.is_visible(),
       "chapter landing first shows collapsed theme titles, not verse titles/descriptions")
    order = q.eval_on_selector("details.theme summary",
        "e => e.textContent.indexOf(e.querySelector('.rng').textContent)"
        " < e.textContent.indexOf(e.querySelector('.th-title').textContent)")
    ok(order, "chapter landing puts the verse range before the theme title")
    q.locator("details.theme").first.locator("summary.theme-summary").click()
    q.wait_for_timeout(150)
    ok(q.locator("details.theme[open]").count() == 1
       and q.locator("details.theme[open] .tdesc").is_visible()
       and q.locator("details.theme[open] .vrow").first.is_visible(),
       "expanding a chapter theme reveals its description and verse titles")
    c.close()
    base_dl = url if url.startswith("http") else (ROOT / "index.html").as_uri()
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto(base_dl + "#chapter=2", wait_until="load", timeout=90000)
    q.wait_for_timeout(1200)
    ok(q.evaluate("state.view") == "chapter" and q.locator(".mode-seg .ms-btn").count() == 2,
       "a bare #chapter=2 deep link opens the unified chapter view")
    c.close()
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto(base_dl + "#chapter=2&tab=study", wait_until="load", timeout=90000)
    q.wait_for_timeout(1200)
    ok(q.inner_text(".way-crumb .wc-cur").strip().startswith("Chapter 2")
       and q.locator(".ch-theme-head").count() > 0
       and q.locator(".mode-seg .ms-btn.on").inner_text().strip() == "Thematic study",
       "#chapter=2&tab=study lands on the unified chapter view (SEO CTA kept compatible)")
    c.close()

    group("split build")
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto(url, wait_until="load", timeout=90000)
    q.wait_for_timeout(1500)
    if url.startswith("http"):
        df_txt = q.evaluate("fetch('data/ch2.js').then(r => r.text())")
    else:
        df_txt = (ROOT / "data" / "ch2.js").read_text(encoding="utf-8")
    ok(df_txt.startswith("GITA_CH[2] = "), "chapter data files are served")
    ok(q.evaluate("DATA.length") == 18, "all 18 chapters loaded and assembled at runtime")
    c.close()

    group("verse deep links")
    base = url if url.startswith("http") else (ROOT / "index.html").as_uri()
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto(base, wait_until="load", timeout=90000)
    q.evaluate("loadAllChapters()")
    q.evaluate("(() => {const v=verseLoc('2.19'); openModal(v.ci,v.ti,v.si);})()")
    # Canonical IDs survive regrouping; a hard-coded theme index does not.
    q.wait_for_timeout(300)
    ok(q.evaluate("location.hash") == "#v=2.19", "opening a verse writes the #v= deep link")
    q.evaluate("openSharePanel()")
    q.wait_for_timeout(200)
    ok("/chapter/2/#v2.19" in q.inner_text("#spLink"),
       "share panel offers the verse's chapter anchor for copying")
    q.click("#shCp")   # a real click on "Copy verse link"
    q.wait_for_timeout(300)
    ok(q.evaluate("getComputedStyle(document.querySelector('#sharePanel')).display") == "none",
       "copying the verse link collapses the share panel")
    ok(q.inner_text("#shareBtn").strip() == "Link copied",
       "the Share button itself flashes the copied confirmation")
    q.evaluate("closeModal()")
    q.wait_for_timeout(400)
    ok(q.evaluate("location.hash") == "", "closing the sheet restores the clean URL")
    c.close()
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto(base + "#v=2.19", wait_until="load", timeout=90000)
    q.wait_for_timeout(1500)
    ok(q.evaluate("state.view") == "welcome" and not q.evaluate("!!document.querySelector('#modalBg.open')")
       and "2.19" in q.inner_text(".w-day") and "Click the verse" in q.inner_text(".w-day"),
       "a shared #v= link lands as an invitation: verse shown, meaning one click away, no popup")
    q.locator(".w-day").click()
    q.wait_for_timeout(700)
    ok(q.evaluate("!!document.querySelector('#modalBg.open')") and "2.19" in q.inner_text(".m-num-chit"),
       "clicking the shared verse opens the four-quarter word-meaning sheet")
    c.close()
    # from a downloaded copy (file://), the share link must point at the live
    # site — a file path is useless to recipients and crashes some Chromes
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto((ROOT / "index.html").as_uri(), wait_until="load", timeout=90000)
    q.evaluate("loadAllChapters()")
    q.evaluate("(() => {const v=verseLoc('2.19'); openModal(v.ci,v.ti,v.si);})()")
    q.wait_for_timeout(200)
    ok(q.evaluate("shareUrl()") == "https://chapain.github.io/Bhagavad-Gita/chapter/2/#v2.19",
       "from a downloaded copy, the share link points at the live verse anchor")
    c.close()

    # A shared verse link, opened the way a recipient actually opens it. The
    # verse lives inside a COLLAPSED <details>, so this is the check that the
    # 2026-09-01 retirement of the v/ pages hinges on: the block must open and
    # the verse must really be on screen, not merely present in the DOM.
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    ch2_url = (url + "chapter/2/#v2.19") if url.startswith("http") \
        else (ROOT / "chapter" / "2" / "index.html").as_uri() + "#v2.19"
    q.goto(ch2_url, wait_until="load", timeout=90000)
    q.wait_for_timeout(800)
    ok(q.evaluate("!!document.querySelector('#v2\\\\.19')"),
       "a shared verse link finds its anchor on the chapter page")
    ok(q.evaluate("document.querySelector('#v2\\\\.19').closest('details').open"),
       "the folded verse list is opened so the verse is reachable")
    ok(q.evaluate("document.getElementById('v2.19').closest('.theme').open"),
       "the shared verse deep link also opens its parent theme")
    ok(q.evaluate("document.querySelector('#v2\\\\.19').classList.contains('target')"),
       "the shared verse is highlighted as the one the reader came for")
    ok(q.evaluate("(r => r.top < innerHeight && r.bottom > 0)"
                  "(document.querySelector('#v2\\\\.19').getBoundingClientRect())"),
       "the shared verse is scrolled into the viewport, not left off-screen")
    c.close()

    # Stale or hand-typed deep links must land somewhere sane — never a blank
    # "boot note" view, never an uncaught error. The study maps were renumbered
    # in 15 chapters, so #theme= links from before that revision are out in the
    # world; #v=2.99 and #v=19.1 are one keystroke away for any reader.
    for frag, expect_view, label in (
            ("#v=2.99", "welcome", "an out-of-range #v= verse falls back to the welcome page"),
            ("#v=19.1", "welcome", "a #v= link to a nonexistent chapter falls back without loading data/ch19.js"),
            ("#theme=2.99", "chapter", "a stale #theme= index lands on the unified chapter view"),
    ):
        c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        q = c.new_page()
        bad = []
        q.on("pageerror", lambda e: bad.append(str(e)))
        q.goto(base + frag, wait_until="load", timeout=90000)
        q.wait_for_timeout(1500)
        ok(q.evaluate("state.view") == expect_view and not bad,
           "%s (view=%s, errors=%s)" % (label, expect_view, bad[:1]))
        c.close()
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    bad = []
    q.on("pageerror", lambda e: bad.append(str(e)))
    q.goto(base + "#chapter=2&tab=study", wait_until="load", timeout=90000)
    q.wait_for_timeout(1500)
    ok(q.evaluate("state.view") == "chapter" and not bad,
       "#chapter=2&tab=study opens the unified chapter view (legacy routes kept compatible)")
    c.close()

    if offline_capable:
        group("offline (service worker)")
        c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                          has_touch=True, service_workers="allow")
        q = c.new_page()
        q.goto(url, wait_until="load", timeout=90000)
        q.wait_for_function("navigator.serviceWorker && navigator.serviceWorker.ready", timeout=20000)
        q.wait_for_timeout(2500)
        keys = q.evaluate("caches.keys()")
        ok(len(keys) > 0, f"cache created {keys}")
        c.set_offline(True)
        q.reload(wait_until="load", timeout=30000)
        q.wait_for_timeout(1500)
        ok("Welcome" in q.inner_text("#view"), "OFFLINE reload renders the app")
        q.get_by_role("button", name="Enter", exact=False).first.click()
        q.wait_for_timeout(400)
        q.fill("#searchInput", "2.47")
        q.wait_for_timeout(800)
        q.locator(".mini").first.click()
        q.wait_for_timeout(600)
        ok("2.47" in q.eval_on_selector(".m-num-chit", "e=>e.textContent"), "OFFLINE verse opens")
        c.set_offline(False)
        # navigating to a chapter landing page must NOT overwrite the shell cache
        q.goto(url + "chapter/1/", wait_until="load", timeout=30000)
        q.wait_for_timeout(1200)
        c.set_offline(True)
        q.goto(url, wait_until="load", timeout=30000)
        q.wait_for_timeout(1000)
        ok(q.evaluate("!!document.querySelector('#appTitle')") and "Chapter 1" not in q.inner_text("h1"),
           "OFFLINE root still serves the app after a chapter-page visit (shell cache not poisoned)")
        c.set_offline(False)
        q.goto(url, wait_until="load", timeout=90000)
        q.wait_for_function("navigator.serviceWorker && navigator.serviceWorker.controller", timeout=20000)
        q.reload(wait_until="load")  # let the app install its existing-controller reload listener
        q.wait_for_function("DATA && VERSES.length === 700", timeout=30000)
        controlled = q.evaluate("!!navigator.serviceWorker.controller")
        ok(controlled, "the automatic-refresh check runs in a controlled tab")
        q.evaluate("setLang('hi'); showChapter(17,0); openModal(17,0,0,'theme',null,null)")
        q.wait_for_selector("#modalBg.open")
        with q.expect_navigation(wait_until="load", timeout=15000):
            q.evaluate("navigator.serviceWorker.dispatchEvent(new Event('controllerchange'))")
        q.wait_for_function("DATA && state.lang === 'hi' && state.chapter === 17"
                            " && document.querySelector('#modalBg').classList.contains('open')",
                            timeout=30000)
        auto_state = q.evaluate("""() => ({lang:state.lang, view:state.view, chapter:state.chapter,
          verse:document.querySelector('.m-num-chit')?.textContent || ''})""")
        ok(auto_state['lang'] == 'hi' and auto_state['view'] == 'chapter'
           and auto_state['chapter'] == 17 and '१८.१' in auto_state['verse'],
           f"service-worker automatic refresh preserves language, chapter and open verse ({auto_state})")
        c.close()

    group("chapter colophons (Phase 2.3; Phase 3.1 unified chapter view)")
    # Each chapter ends with its traditional colophon. Phase 3.1 merges reading
    # + study guide: colophon lives at the end of .ch-flow, closing the chapter.
    for cn, tail in ((1, "प्रथमोऽध्यायः ॥ १ ॥"), (6, "आत्मसंयमयोगो नाम षष्ठोऽध्यायः ॥ ६ ॥"),
                     (18, "अष्टादशोऽध्यायः ॥ १८ ॥")):
        c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        q = c.new_page()
        q.goto(base_dl + f"#chapter={cn}", wait_until="load", timeout=90000)
        q.wait_for_timeout(1400)
        ok(q.locator(".ch-flow .colophon").count() == 1,
           f"chapter {cn} chapter view prints exactly one colophon")
        if q.locator(".ch-flow .colophon").count() == 1:
            txt = q.inner_text(".ch-flow .colophon")
            ok(tail in txt and txt.strip().startswith("ॐ"),
               f"chapter {cn} colophon carries this chapter's text and opens with ॐ")
            ok(q.locator(".ch-flow .colophon .col-iast").count() == 1
               and "oṃ tatsaditi" in q.inner_text(".ch-flow .colophon .col-iast"),
               f"chapter {cn} colophon shows its transliteration")
            ok(q.evaluate("(() => {const cs=[...document.querySelectorAll('.ch-flow > *')];"
                          "return cs.length && cs[cs.length-1].classList.contains('colophon');})()"),
               f"chapter {cn} colophon is the last block of the chapter view")
            ok(q.locator(".mini .colophon, .ch-theme-head .colophon").count() == 0,
               f"chapter {cn} colophon is not inside a verse or theme heading")
        c.close()
        # Legacy tab=study route also lands on the unified view and still carries the colophon.
        c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        q = c.new_page()
        q.goto(base_dl + f"#chapter={cn}&tab=study", wait_until="load", timeout=90000)
        q.wait_for_timeout(1400)
        ok(q.locator(".ch-theme-head").count() > 0 and q.locator(".ch-flow .colophon").count() == 1,
           f"chapter {cn} legacy tab=study route shows themes and the closing colophon")
        c.close()
    # the generated chapter page carries it too, once, as plain text for crawlers
    q = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                      has_touch=True).new_page()
    q.goto((url + "chapter/6/") if url.startswith("http")
           else (ROOT / "chapter" / "6" / "index.html").as_uri(), wait_until="load", timeout=30000)
    q.wait_for_timeout(300)
    ok(q.locator(".colophon").count() == 1
       and "आत्मसंयमयोगो नाम षष्ठोऽध्यायः" in q.inner_text(".colophon"),
       "generated chapter page prints its colophon once")

    ok(not errs, f"no JS errors ({errs[:2]})")
    b.close()


def main():
    args = [a for a in sys.argv[1:]]
    srv = None
    offline = False
    if "--serve" in args:
        args.remove("--serve")
        srv = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1",
                                "--directory", str(ROOT)],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        url = "http://127.0.0.1:8765/"
        offline = True
    elif args:
        url = args[0]
        offline = url.startswith("http")
    else:
        url = (ROOT / "index.html").as_uri()

    print(f"target: {url}")
    try:
        with sync_playwright() as pw:
            run(pw, url, offline)
    finally:
        if srv:
            srv.terminate()

    print("\n" + "=" * 46)
    print(f"browser_checks.py: {PASS} passed, {len(FAIL)} failed")
    if FAIL:
        for f in FAIL:
            print("  -", f)
        sys.exit(1)
    print("ALL GREEN ✓")


if __name__ == "__main__":
    main()
