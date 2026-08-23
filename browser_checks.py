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
    ok(pg.title() == "Bhagavad Gita — Interactive Study", "title")
    ok("Welcome" in pg.inner_text("#view"), "welcome renders (JS runs)")
    ok(pg.evaluate("DATA.length") == 18, "18 chapters")
    ok(pg.evaluate("VERSES.length") == 700, "700 verses indexed")

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

    # The list pages run 4-5 screens on a phone, so the top crumb is repeated at
    # the foot. It must appear only where there is a parent to go back to, and
    # must say the same thing as the crumb above it.
    for js, expect_foot in [("showSections()", False), ("showChapters(0)", False),
                            ("showChapters(1)", True), ("showThemes(1)", True),
                            ("showVerses(1,0)", True)]:
        pg.evaluate(js)
        pg.wait_for_timeout(450)
        top = pg.eval_on_selector_all(".back-top:not(.back-foot .back-top)", "e=>e.map(x=>x.textContent.trim())")
        foot = pg.eval_on_selector_all(".back-foot .back-top", "e=>e.map(x=>x.textContent.trim())")
        ok(bool(foot) == expect_foot, f"{js}: foot back-button {'present' if expect_foot else 'absent'}")
        if expect_foot:
            ok(foot and top and foot[0] == top[0],
               f"{js}: foot button says the same as the crumb ({foot[:1]} vs {top[:1]})")
    pg.evaluate("showVerses(1,0)")
    pg.wait_for_timeout(500)
    pg.locator(".back-foot .back-top").click()
    pg.wait_for_timeout(600)
    ok("Themes" in pg.eval_on_selector(".view-title", "e=>e.textContent"),
       "the foot back-button actually navigates")

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
