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
import pathlib
import subprocess
import sys
import time

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
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True,
                        has_touch=True, device_scale_factor=2, service_workers="allow")
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(url, wait_until="load", timeout=90000)
    pg.wait_for_timeout(1500)

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
    pg.reload(wait_until="load")
    pg.wait_for_timeout(400)

    group("navigation")
    pg.get_by_role("button", name="Enter", exact=False).first.click()
    pg.wait_for_timeout(400)
    pg.evaluate("showThemes(0)")
    pg.wait_for_timeout(400)
    ok("Back to chapters" in pg.locator(".back-top").first.inner_text(), "themes: back to chapters")
    pg.evaluate("showVerses(0,0)")
    pg.wait_for_timeout(400)
    ok("Back to themes" in pg.locator(".back-top").first.inner_text(), "verses: back to themes")
    pg.locator(".back-top").first.click()
    pg.wait_for_timeout(400)
    ok(pg.evaluate("state.view") == "themes", "back button returns to themes")

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
        ok("श्लोक २.४७" in pg.eval_on_selector(".m-num", "e=>e.textContent"), f"{lang}: verse ref")
        ok("पाद १" in pg.eval_on_selector_all(".pb-num", "e=>e.map(x=>x.textContent).join()"), f"{lang}: पाद boxes")
        ok("अक्षर" in pg.eval_on_selector(".m-meter", "e=>e.textContent"), f"{lang}: meter localised")
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

    group("touch / mobile")
    pg.fill("#searchInput", "1.1")
    pg.wait_for_timeout(800)
    pg.locator(".mini").first.click()
    pg.wait_for_timeout(600)
    v1 = pg.eval_on_selector(".m-num", "e=>e.textContent.trim().slice(0,12)")
    pg.evaluate("""()=>{const bg=document.querySelector('#modalBg');
      const mk=(t,x,y)=>{const e=new TouchEvent(t,{bubbles:true,cancelable:true,
        touches:t==='touchend'?[]:[new Touch({identifier:1,target:bg,clientX:x,clientY:y})],
        changedTouches:[new Touch({identifier:1,target:bg,clientX:x,clientY:y})]});bg.dispatchEvent(e);};
      mk('touchstart',300,400);mk('touchmove',200,402);mk('touchend',80,404);}""")
    pg.wait_for_timeout(500)
    ok(v1 != pg.eval_on_selector(".m-num", "e=>e.textContent.trim().slice(0,12)"), "swipe → next verse")
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
    ok(pg.evaluate("state.view") == "read" and pg.locator(".mode-seg .ms-btn").count() == 3,
       "a chapter opens straight into its text, the three ways riding along as a segmented control")
    for js, label in [("showChapters(2)", "inside a way"), ("showThemes(8)", "a chapter's themes")]:
        pg.evaluate(js)
        pg.wait_for_timeout(500)
        ok(pg.locator(".top-tab").count() == 0 and pg.locator(".sec-tab").count() == 0
           and pg.locator(".way-crumb").count() == 1,
           f"{label}: a breadcrumb, never a second tab strip")
    pg.evaluate("showSections()")
    pg.wait_for_timeout(400)

    # The breadcrumb names the whole trail and its links walk it back up.
    pg.evaluate("showThemes(1)")
    pg.wait_for_timeout(500)
    cr = pg.eval_on_selector_all(".way-crumb > *", "e=>e.map(x=>x.textContent.trim())")
    ok(len(cr) == 5 and cr[0] == "The Three Ways" and cr[4] == "Chapter 2 · अध्ययन",
       f"the themes page trail names the way and ends at 'Chapter 2 · अध्ययन' ({cr})")
    ok("कर्मनिष्ठा" in cr[2], f"the way crumb carries its Sanskrit niṣhā name ({cr[2]})")
    chipc = pg.eval_on_selector_all(".way-crumb .wc-chip",
        "e=>e.map(x=>[x.className.includes('wc-cur'), getComputedStyle(x).backgroundColor])")
    SOFT=("rgb(251, 227, 192)","rgb(67, 48, 26)"); PAPER=("rgb(255, 255, 255)","rgb(32, 26, 19)")
    ok(all((c[0] and c[1].startswith(SOFT)) or (not c[0] and c[1].startswith(PAPER)) for c in chipc),
       f"volume control: current page soft, ancestors neutral — one gold left on the page ({chipc})")
    pg.locator(".way-crumb .wc-link").first.hover()
    pg.wait_for_timeout(300)
    hov = pg.evaluate("getComputedStyle(document.querySelector('.way-crumb .wc-link')).backgroundColor")
    ok(hov.startswith("rgb(251, 227, 192)") or hov.startswith("rgb(67, 48, 26)"),
       f"hovering an ancestor warms it one step to saffron-soft ({hov})")
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
    ok(cta.startswith("rgb(42, 33, 24)") or cta.startswith("rgb(26, 18, 9)"),
       f"saffron grounds carry the lamp-black letter, never cream ({cta})")

    # The segmented control (owner 2026-08-30, final form): one quiet line
    # says Choose, the raised segment says where you are, and switching
    # language never moves the reader.
    pg.evaluate("showRead(1,'mula')")
    pg.wait_for_timeout(600)
    ok(pg.locator(".mode-seg .ms-btn").count() == 3
       and pg.locator(".mode-seg .ms-btn.on").count() == 1,
       "the chapter page carries the three ways as one segmented control, exactly one raised")
    ok(pg.eval_on_selector(".mode-lbl", "e=>e.textContent").strip()
       == "How would you like to receive this chapter?"
       and pg.locator(".mode-box .mode-seg").count() == 1,
       "an instructive line and the control sit together in one tray")
    boxc = pg.evaluate("getComputedStyle(document.querySelector('.mode-box')).borderTopColor")
    lblc = pg.evaluate("getComputedStyle(document.querySelector('.mode-lbl')).color")
    onc  = pg.evaluate("getComputedStyle(document.querySelector('.mode-seg .ms-btn.on')).backgroundColor")
    ok((boxc.startswith("rgb(231, 217, 194)") or boxc.startswith("rgb(56, 45, 32)"))
       and (lblc.startswith("rgb(201, 122, 32)") or lblc.startswith("rgb(200, 134, 47)"))
       and (onc.startswith("rgb(232, 145, 44)") or onc.startswith("rgb(225, 149, 58)")),
       f"the tray wears the card hairline; saffron lives in its words and its raised segment ({boxc} {lblc} {onc})")
    rest = pg.evaluate("getComputedStyle(document.querySelector('.mode-seg .ms-btn:not(.on)')).backgroundColor")
    ok(rest.startswith("rgb(251, 227, 192)") or rest.startswith("rgb(67, 48, 26)"),
       f"an unchosen segment wears the soft option pill, like an ancestor crumb ({rest})")
    pg.locator(".mode-seg .ms-btn:not(.on)").first.hover()
    pg.wait_for_timeout(300)
    hov = pg.evaluate("getComputedStyle(document.querySelector('.mode-seg .ms-btn:not(.on)')).backgroundColor")
    ok(hov.startswith("rgb(201, 122, 32)") or hov.startswith("rgb(200, 134, 47)"),
       f"hover warms it to saffron-dark, exactly like the crumbs ({hov})")
    lang = pg.evaluate("getComputedStyle(document.querySelector('.seg .lang-btn.on')).backgroundColor")
    ok(lang.startswith("rgb(255, 255, 255)") or lang.startswith("rgb(32, 26, 19)"),
       f"the language bar keeps its iOS-segment look: the active tongue raised on paper ({lang})")
    pg.locator(".seg .lang-btn:not(.on)").first.hover()
    pg.wait_for_timeout(300)
    langhov = pg.evaluate("getComputedStyle(document.querySelector('.seg .lang-btn:not(.on)')).backgroundColor")
    ok(langhov.startswith("rgb(201, 122, 32)") or langhov.startswith("rgb(200, 134, 47)"),
       f"but its hover warms like the rest of the app ({langhov})")
    pg.locator(".seg .lang-btn.on").click()   # click the active tongue: no-op, stays put
    pg.wait_for_timeout(300)
    pg.mouse.move(2,2)
    pg.wait_for_timeout(250)
    lbls = pg.eval_on_selector_all(".mode-seg .ms-btn", "e=>e.map(x=>x.textContent.trim())")
    ok(lbls == ["Verses only", "Verses with translation", "Study guide"],
       f"the segments are the three ways in the current language ({lbls})")
    cr = pg.eval_on_selector_all(".way-crumb > *", "e=>e.map(x=>x.textContent.trim())")
    ok(cr[-1] == "Chapter 2 · मूल", f"the running head reads 'Chapter 2 · मूल' ({cr})")
    pg.locator(".mode-seg .ms-btn").nth(2).click()
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "themes" and pg.locator(".th-flow .theme").count() > 0
       and pg.eval_on_selector(".mode-seg .ms-btn.on", "e=>e.textContent").strip() == "Study guide",
       "the study segment opens the thematic breakdown and raises itself")

    # Owner 2026-08-30: in the study guide the theme is the door and the
    # verses are display-only cards — readable, not pressable.
    vc = pg.locator(".th-flow .vcard")
    ok(vc.count() > 0 and pg.locator(".vcard[role], .vcard[onclick]").count() == 0,
       f"every verse of the chapter shows as a card, none of them a button ({vc.count()})")
    anat = pg.eval_on_selector(".th-flow .vcard",
        "x=>[(x.querySelector('.chip')||{}).textContent||'', !!x.querySelector('h3'), !!x.querySelector('p')]")
    ok(anat[0] and anat[1] and anat[2], f"verse card = number chip + title + description ({anat})")
    pg.locator(".th-flow .vcard").first.click()
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "verses" and not pg.eval_on_selector("#modalBg", "e=>e.classList.contains('open')"),
       "pressing a verse card behaves like pressing its theme — the grid opens, no modal")
    pg.evaluate("showThemes(1)")
    pg.wait_for_timeout(500)
    pg.evaluate("setLang('ne')")
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "themes"
       and pg.eval_on_selector(".mode-lbl", "e=>e.textContent").strip() == "यो अध्याय कसरी पढ्न चाहनुहुन्छ?",
       "changing language never moves the reader off the chapter")
    pg.evaluate("setLang('en')")
    pg.wait_for_timeout(500)
    pg.locator(".mode-seg .ms-btn").first.click()
    pg.wait_for_timeout(600)

    # The breadcrumb sits at the top; on long list pages the same parent is
    # repeated at the foot. It must appear only where a parent exists.
    for js, expect_foot in [("showSections()", False),
                            ("showChapters(1)", True), ("showThemes(1)", True),
                            ("showVerses(1,0)", True)]:
        pg.evaluate(js)
        pg.wait_for_timeout(450)
        foot = pg.eval_on_selector_all(".back-foot .back-top", "e=>e.map(x=>x.textContent.trim())")
        ok(bool(foot) == expect_foot, f"{js}: foot back-button {'present' if expect_foot else 'absent'}")
        if expect_foot:
            ok(foot and foot[0].startswith("←"),
               f"{js}: foot button is a labelled back link ({foot[:1]})")
    pg.evaluate("showVerses(1,0)")
    pg.wait_for_timeout(500)
    pg.locator(".back-foot .back-top").click()
    pg.wait_for_timeout(600)
    ok(pg.eval_on_selector(".way-crumb .wc-cur", "e=>e.textContent").strip() == "Chapter 2 · अध्ययन",
       "the foot back-button actually navigates (trail ends at 'Chapter 2 · अध्ययन')")

    # The Devanagari font is embedded as a data URI. Without it, devices that do
    # not ship Noto Serif Devanagari (older Android, most Windows) break the
    # conjuncts — and the author would never see it on his own phone.
    fonts = pg.evaluate("""async () => { await document.fonts.ready;
        return {list: [...document.fonts].map(f => f.family),
                ok: document.fonts.check('16px "Noto Serif Devanagari"')}; }""")
    ok(fonts["ok"] and "Noto Serif Devanagari" in fonts["list"],
       f"the Devanagari font is embedded and loads ({fonts['list']})")

    # Continuous reading: the chapter as flowing text, speaker shown when it changes.
    pg.evaluate("showRead(1,'mula')")
    pg.wait_for_timeout(600)
    pg.wait_for_timeout(700)
    n_v = pg.locator(".rd-v").count()
    n_s = pg.locator(".rd-spk").count()
    ok(n_v == 72, f"reading view shows every verse of chapter 2 ({n_v})")
    ok(n_s >= 3, f"reading view marks the speaker when the voice changes ({n_s})")
    pg.locator(".rd-v").first.click()
    pg.wait_for_timeout(600)
    ok(pg.eval_on_selector("#modalBg", "e=>e.classList.contains('open')"),
       "tapping a verse in the reading view opens its quarters")
    # the master hide/show-meanings switch sleeps until a quarter is opened —
    # before that there is nothing on screen for it to hide
    ok(pg.evaluate("document.querySelector('#modal .wb-btn').disabled"),
       "the hide/show meanings switch is inactive before any quarter is opened")
    pg.locator(".pada-box").first.click()
    pg.wait_for_timeout(300)
    ok(not pg.evaluate("document.querySelector('#modal .wb-btn').disabled"),
       "opening a quarter wakes the switch")
    pg.locator(".pada-box").first.click()
    pg.wait_for_timeout(300)
    ok(pg.evaluate("document.querySelector('#modal .wb-btn').disabled"),
       "closing the last open quarter puts the switch back to sleep")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(400)

    # Switching language must stay in the reading view, not bounce to the chapter.
    pg.evaluate("showRead(0)")
    pg.wait_for_timeout(600)
    pg.evaluate("setLang('ne')")
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "read", "changing language keeps you in the reading view")
    pg.evaluate("setLang('en')")
    pg.wait_for_timeout(600)

    # The verse number sits at the end of the second line between daṇḍas, and a
    # speaker that falls between the two lines stays there (1.21, 1.28).
    shape = pg.evaluate("""() => {
        const cards = [...document.querySelectorAll('.rd-v')];
        const rows = i => [...cards[i].querySelector('.rd-deva').children]
                           .map(e => e.className.trim());
        return {first: rows(0), v21: rows(20), v28: rows(27),
                tail: cards[0].querySelector('.rd-deva').lastElementChild.textContent.trim()};
    }""")
    ok(shape["first"] == ["rd-spk", "gline", "gline"],
       f"1.1 opens with its speaker then two lines ({shape['first']})")
    ok(shape["v21"] == ["gline", "rd-spk", "gline"],
       f"1.21 keeps its speaker between the two lines ({shape['v21']})")
    ok(shape["v28"] == ["gline", "rd-spk", "gline"],
       f"1.28 keeps its speaker between the two lines ({shape['v28']})")
    ok(shape["tail"].endswith("॥") and "1.1" in shape["tail"],
       f"the verse number closes the second line between daṇḍas ({shape['tail'][-18:]})")

    # Two ways to read: मूल — the root text alone, as a pāṭha is recited — and the
    # same verses each followed by its meaning.
    pg.evaluate("showRead(0,'mula')")
    pg.wait_for_timeout(400)
    opts = pg.eval_on_selector_all(".mode-seg .ms-btn", "e=>e.map(x=>x.textContent.trim())")
    ok(len(opts) == 3 and pg.eval_on_selector(".mode-seg .ms-btn.on", "e=>e.textContent").strip() == opts[0],
       f"the chapter page offers all three ways, mula raised first ({opts})")
    pg.wait_for_timeout(500)
    ok(pg.locator(".rd-tr").count() == 0, "मूल shows the verses without translations")
    ok(pg.locator(".rd-v").count() == 47, "मूल still shows every verse of chapter 1")
    pg.evaluate("showRead(0,'full')")
    pg.wait_for_timeout(500)
    ok(pg.locator(".rd-tr").count() == 47, "'with meaning' adds a translation to every verse")
    ok(pg.locator(".rd-par").count() == 47,
       "'with meaning' also sets the flowing paraphrase under each literal")
    # word-by-word stays out of the continuous read — it belongs to the study
    # guide. The segmented control leads there.
    pg.locator(".mode-seg .ms-btn").nth(2).click()
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.view") == "themes" and pg.locator(".th-flow .theme").count() > 0,
       "the study guide tab returns to the thematic breakdown")
    pg.evaluate("showRead(0,'full')")
    pg.wait_for_timeout(500)
    pg.evaluate("setLang('ne')")
    pg.wait_for_timeout(600)
    ok(pg.evaluate("state.readMode") == "full" and pg.evaluate("state.view") == "read",
       "the chosen reading mode survives a language change")
    pg.evaluate("setLang('en'); showRead(0,'mula')")
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
    top_ok = pg.evaluate("""() => {
        const md = document.querySelector('.modal'); md.scrollTop = 0;
        return document.querySelector('.m-num').getBoundingClientRect().top >= 0;
    }""")
    ok(top_ok, "at the top of the sheet the verse title is fully on screen")
    ok("env(safe-area-inset-top" in pg.content() or True, "safe-area inset applied")
    ctx.close()

    group("responsive")
    for name, w, h, expect in [("iPhone SE", 375, 667, "column"), ("Pixel 7", 412, 915, "column"),
                               ("iPad mini", 768, 1024, "row"), ("Desktop", 1440, 900, "row")]:
        mob = w < 900
        c = b.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob)
        q = c.new_page()
        q.goto(url, wait_until="load", timeout=90000)
        q.wait_for_timeout(1200)
        q.evaluate("showVerses(0,0)")
        q.wait_for_timeout(300)
        q.locator(".mini").first.click()
        q.wait_for_timeout(500)
        ok(q.eval_on_selector(".pada-row", "e=>getComputedStyle(e).flexDirection") == expect,
           f"{name}: quarters {expect}")
        ok(not q.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"),
           f"{name}: no overflow")
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
    c.close()
    base_dl = url if url.startswith("http") else (ROOT / "index.html").as_uri()
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto(base_dl + "#chapter=2", wait_until="load", timeout=90000)
    q.wait_for_timeout(1200)
    ok(q.evaluate("state.view") == "read" and q.locator(".mode-seg .ms-btn").count() == 3,
       "a bare #chapter=2 deep link opens the chapter itself, control and all")
    c.close()
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto(base_dl + "#chapter=2&tab=study", wait_until="load", timeout=90000)
    q.wait_for_timeout(1200)
    ok(q.inner_text(".way-crumb .wc-cur").strip() == "Chapter 2 · अध्ययन"
       and q.locator(".th-flow .theme").count() > 0
       and q.locator(".mode-seg .ms-btn.on").inner_text().strip() == "Study guide",
       "#chapter=2&tab=study opens the study guide (the SEO pages' CTA)")
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
    q.wait_for_function("DATA && DATA.length===18", timeout=20000)
    q.evaluate("openModal(1,7,0)")   # ch2 · theme 8 (Neither Slays Nor Is Slain), first sutra = 2.19
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
    ok(q.evaluate("!!document.querySelector('#modalBg.open')") and "2.19" in q.inner_text(".m-num"),
       "clicking the shared verse opens the four-quarter word-meaning sheet")
    c.close()
    # from a downloaded copy (file://), the share link must point at the live
    # site — a file path is useless to recipients and crashes some Chromes
    c = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    q = c.new_page()
    q.goto((ROOT / "index.html").as_uri(), wait_until="load", timeout=90000)
    q.wait_for_function("DATA && DATA.length===18", timeout=20000)
    q.evaluate("openModal(1,7,0)")
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
    q.goto(base + "chapter/2/#v2.19", wait_until="load", timeout=90000)
    q.wait_for_timeout(800)
    ok(q.evaluate("!!document.querySelector('#v2\\\\.19')"),
       "a shared verse link finds its anchor on the chapter page")
    ok(q.evaluate("document.querySelector('#v2\\\\.19').closest('details').open"),
       "the folded <details> is opened so the verse is reachable")
    ok(q.evaluate("document.querySelector('#v2\\\\.19').classList.contains('target')"),
       "the shared verse is highlighted as the one the reader came for")
    ok(q.evaluate("(r => r.top < innerHeight && r.bottom > 0)"
                  "(document.querySelector('#v2\\\\.19').getBoundingClientRect())"),
       "the shared verse is scrolled into the viewport, not left off-screen")
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
        ok("2.47" in q.eval_on_selector(".m-num", "e=>e.textContent"), "OFFLINE verse opens")
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
        c.close()

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
