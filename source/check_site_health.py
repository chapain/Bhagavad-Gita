#!/usr/bin/env python3
"""check_site_health.py — the faults found in the 2026-09-01 audit, locked shut.

This is the static publication audit: generated chapter pages, CSS, metadata,
offline assets, and other output contracts. App interactions (including
Learn/Play, favorites storage, routing and accessibility announcements) belong
to browser_checks.py; chapter-data shape and types are enforced by source/schema.py.

Run:  python3 source/check_site_health.py      (from anywhere)
Exit code 1 on any failure, so build.py / rebuild.sh can gate on it.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_BASE = "https://chapain.github.io/Bhagavad-Gita"

errors = []
checks = 0


def ok(cond, label):
    global checks
    checks += 1
    if not cond:
        errors.append(label)


def read(*parts):
    """Missing file must be a reported FAILURE, never a traceback: a crash
    hides every check after it, so one deleted artefact could mask the rest."""
    try:
        with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        errors.append(f"cannot read {os.path.join(*parts)}: {e}")
        return ""


def strip_noise(txt):
    """Drop base64 font payloads, CSS comments and HTML comments before any
    static scan. Without this, prose like "every rule keeps using var(--x)"
    inside an explanatory comment reads as a real undefined-variable use."""
    txt = re.sub(r"base64,[A-Za-z0-9+/=]+", "", txt)
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    txt = re.sub(r"<!--.*?-->", "", txt, flags=re.S)
    return txt


# ---------------------------------------------------------------- 1. CSS vars
# The bug: chapter.css declared --soft while 12 rules asked for var(--ink-soft).
# Undefined custom properties fail silently — every muted line rendered at full
# ink on all 18 pages. No test resolves CSS, so nothing noticed.
css = read("chapter.css")
css_nofont = strip_noise(css)
defined = set(re.findall(r"(--[a-z0-9-]+)\s*:", css_nofont))
used = set(re.findall(r"var\((--[a-z0-9-]+)", css_nofont))
undefined = sorted(used - defined)
ok(not undefined, f"chapter.css uses undefined custom properties: {undefined}")
# A set union is not enough: the light :root and the dark @media block are two
# INDEPENDENT palettes. If one of them drops a name the other still defines,
# the union stays complete while that theme silently loses the colour — which
# is exactly how --soft/--ink-soft survived. Check each block on its own.
blocks = re.findall(r":root\s*\{([^}]*)\}", css_nofont)
ok(len(blocks) >= 2, "chapter.css should declare a light and a dark palette")
for i, blk in enumerate(blocks):
    names = set(re.findall(r"(--[a-z0-9-]+)\s*:", blk))
    missing = sorted(used - names)
    ok(not missing, f"chapter.css palette #{i + 1} is missing {missing}")
# the app and the chapter pages must name the muted tone identically
ok("--ink-soft" in defined, "chapter.css must define --ink-soft (not --soft)")
ok("--soft:" not in css_nofont, "chapter.css must not reintroduce the --soft alias")

# same audit on the app shell
idx = read("index.html")
idx_nofont = strip_noise(idx)
idx_def = set(re.findall(r"(--[a-z0-9-]+)\s*:", idx_nofont))
idx_used = set(re.findall(r"var\((--[a-z0-9-]+)", idx_nofont))
ok(not (idx_used - idx_def), f"index.html uses undefined vars: {sorted(idx_used - idx_def)}")

# A loaded font is not enough: overriding headings with Georgia/serif or
# system-ui/sans alone made localized titles blank on font-poor devices.
_font_stacks = re.findall(r"font-family\s*:\s*([^;{}\n]+);", idx_nofont)
_missing_deva = sorted({stack.strip() for stack in _font_stacks
                        if "Noto Serif Devanagari" not in stack
                        and stack.strip() not in {"inherit", "initial", "unset"}})
ok(not _missing_deva,
   f"all explicit app font stacks must include the bundled Devanagari face: {_missing_deva}")


# ------------------------------------------------- 2. one og:image, one card
# The bug: og:image and twitter:card were each declared TWICE with conflicting
# values. Crawlers take the first og:image, so the homepage previewed with the
# square icon while the 1200x630 dimensions described a different file.
def meta_values(txt, attr, key):
    return re.findall(rf'<meta {attr}="{re.escape(key)}" content="([^"]*)"', txt)


for page, label in [(idx, "index.html")] + \
                   [(read("chapter", str(n), "index.html"), f"chapter/{n}") for n in range(1, 19)]:
    imgs = meta_values(page, "property", "og:image")
    cards = meta_values(page, "name", "twitter:card")
    ok(len(imgs) == 1, f"{label}: expected exactly 1 og:image, found {len(imgs)}")
    ok(len(cards) == 1, f"{label}: expected exactly 1 twitter:card, found {len(cards)}")
    ok(imgs == [f"{SITE_BASE}/icons/og-card.png"], f"{label}: og:image must be icons/og-card.png, got {imgs}")
    ok(cards == ["summary_large_image"], f"{label}: twitter:card must be summary_large_image")
    # the declared dimensions must describe the image actually referenced
    ok(meta_values(page, "property", "og:image:width") == ["1200"], f"{label}: og:image:width")
    ok(meta_values(page, "property", "og:image:height") == ["630"], f"{label}: og:image:height")
    # the card is a picture; without alt text it reaches screen readers and
    # link previews as an unnamed image (chapters carried none until 2026-10-15)
    ok(len(meta_values(page, "property", "og:image:alt")) == 1, f"{label}: og:image:alt")

# Interactive learning/play invariants are exercised against the rendered app
# in browser_checks.py. This script focuses on generated artifacts and static
# publication integrity rather than matching implementation source snippets.


# -------------------------- surfaces use the shared palette consistently
# The current design keeps card fills quiet (paper/cream) and reserves saffron
# and teal for accents, states and hover. Check that surfaces use the shared
# palette rather than hard-coded colours, and that the active quarter slot keeps
# its restrained teal hairline.
_SURFACES = (".card", ".theme", ".res-card", ".lr-step", ".lr-chip",
             ".lr-q", ".pl-mode", ".lr-word", ".lr-finis", ".lr-opt", ".lr-qbox",
             ".lr-chip2", ".lr-slot")
for _sel in _SURFACES:
    _body = " ".join(" ".join(m.split()) for m in
        re.findall(r"(?<![\w.-])" + re.escape(_sel) + r"\{[^}]*\}", idx_nofont, re.S))
    ok(_body != "", f"{_sel} must exist")
    ok(any(f"var({token})" in _body for token in ("--saffron", "--teal", "--paper", "--cream")),
       f"{_sel} must use a shared palette token")
# --saffron-soft is too faint to carry a resting edge; it remains fine for fills.
ok("border-left:2px solid var(--saffron-soft)" not in idx
   and "border-left:3px solid var(--saffron-soft)" not in idx,
   "a resting brand edge must not use low-contrast --saffron-soft")
_slot_edge = re.search(r"\.lr-slot\{[^}]*border-left:2px solid var\(--teal\)", idx_nofont, re.S)
ok(_slot_edge is not None, "the quarter-slot state keeps its teal brand hairline")
_edges = re.findall(r"border-left:(\d)px solid var\(--(?:saffron|teal)\)", idx)
ok(all(int(w) <= 2 for w in _edges),
   f"the brand edge must stay a hairline; found widths {sorted(set(_edges))}")


# Drill retries and option correctness are exercised in browser_checks.py.


# ------------------------------------- the verdict is shown, not narrated
# Owner 2026-09-02: mark the chosen wrong answer in red with a cross, rather
# than printing "Not quite." underneath. A tick and a cross say it faster than
# prose, and in every language at once — so the feedback line now carries only
# what the reader CANNOT see: the right verse and its meaning.
ok('.lr-opt.right::after' in idx and '.lr-opt.wrong::after' in idx,
   "right and wrong options must carry a tick and a cross")
ok('content:"\\2713"' in idx and 'content:"\\2715"' in idx,
   "the marks must be a tick and a cross")
# Check inside the RULE, not the whole file: --danger-soft also appears in the
# palette definition, so a bare substring test passed with the fill removed.
# The shared ".lr-opt.right, .lr-opt.wrong{...}" rule matches a naive pattern
# first. Take the LAST .lr-opt.wrong{...} block, which is the standalone one.
_all_wrong = re.findall(r"\.lr-opt\.wrong\{[^}]*\}", idx_nofont, re.S)
_wr = type("M", (), {"group": lambda self, n=0: _all_wrong[-1]})() if _all_wrong else None
ok(_wr is not None, ".lr-opt.wrong must exist")
if _wr:
    ok("background:var(--danger-soft)" in _wr.group(0),
       "a wrong option needs a red wash, not just a red border")
    ok("opacity" not in _wr.group(0),
       "the wrong option must not be dimmed — the mistake is worth studying")
ok("color:var(--on-danger)" in idx,
   "the cross needs per-theme ink: white is only 3.14:1 on the dark theme's red")
ok("--danger-soft" in idx and "--on-danger" in idx,
   "both danger tokens must be defined in the palette")


# --------------------------------------- the question screen must not be bland
# Options were --paper on a --paper card, so every boundary vanished and the
# screen went flat white (owner 2026-09-01). The card is --cream now, the
# options keep --paper and gain a shadow to lift off it, and the prompt sits in
# a saffron band. A 1.06:1 fill difference cannot carry this alone.
_qb = re.search(r"\.lr-qbox\{[^}]*\}", idx_nofont, re.S)
ok(_qb is not None and "var(--cream)" in _qb.group(0),
   "the question card must be --cream so --paper options read on top of it")
_op = re.search(r"\.lr-opt\{[^}]*\}", idx_nofont, re.S)
ok(_op is not None and "box-shadow" in _op.group(0),
   "options need a shadow: --paper on --cream is only a 1.06:1 step")
_ask = re.search(r"\.lr-ask\{[^}]*\}", idx_nofont, re.S)
ok(_ask is not None and "var(--saffron-soft)" in _ask.group(0),
   "the prompt must be marked as a prompt, not more prose")
ok("border-color:var(--danger)" in idx,
   "a wrong answer must read as wrong, not merely as a darker saffron")
_os = re.search(r"\.lr-opt \.os\{[^}]*\}", idx_nofont, re.S)
ok(_os is not None and "var(--saffron-text)" in _os.group(0),
   "the verse number under an option is a number — saffron like the rest")
# ------------------------------------------- hover must not stick on touch
# A :hover state persists after a tap on a phone, so the last thing touched
# keeps looking selected. The app already answers this with @media (hover:none)
# — but that block listed only the ORIGINAL components. The learn path and Play
# were added later and never included, which is why their chips and cards
# stayed lit (owner 2026-09-01). Every learn/play hover must be cancelled there.
_hn = re.search(r"@media \(hover:none\)\{(.*?)\n  \}", idx_nofont, re.S)
ok(_hn is not None, "the touch block must exist")
if _hn:
    _blk = _hn.group(1)
    # Match on the HOVER SELECTOR, not the bare class name: a block that merely
    # mentions .lr-opt somewhere does not cancel .lr-opt:hover. The first
    # version of this check passed with the rule deleted.
    _hovered = set(re.findall(r"(\.(?:lr|pl)-[a-z0-9-]+(?:\.[a-z]+)?:hover)", idx_nofont))
    # This selector only reapplies teal to Sanskrit text already teal at rest;
    # it has no touch-only visual state to cancel.
    _dv_base = re.search(r"\.lr-chip2\.dv \.lr-t\{([^}]*)\}", idx_nofont)
    _dv_hover = re.search(r"\.lr-chip2\.dv:hover:not\(:disabled\)\{([^}]*)\}", idx_nofont)
    if (_dv_base and _dv_hover and
            {x.strip() for x in _dv_base.group(1).split(";") if x.strip()} ==
            {x.strip() for x in _dv_hover.group(1).split(";") if x.strip()}):
        _hovered.discard(".lr-chip2.dv:hover")
    _missing = sorted(x for x in _hovered if x not in _blk)
    ok(not _missing,
       f"these learn/play hovers stick on touch: {_missing}")
    # a cancelled hover needs an :active answer, or touch loses all feedback
    _active = set(re.findall(r"(\.(?:lr|pl)-[a-z0-9-]+)(?::active)", _blk))
    ok(len(_active) >= 6, f"touch needs :active feedback, found {len(_active)}")

# Play's chrome must match the app's, like the learn path's does.
_plm = re.search(r"\.pl-mode\{[^}]*\}", idx_nofont, re.S)
ok(_plm is not None, ".pl-mode must exist")
if _plm:
    for _p in ("background:var(--paper)", "border-radius:16px", "padding:16px 18px", "box-shadow"):
        ok(_p in _plm.group(0), f".pl-mode must match .card on {_p}")
_pls = re.search(r"\.pl-sel\{[^}]*\}", idx_nofont, re.S)
ok(_pls is not None and "color:var(--teal)" in _pls.group(0)
   and "padding:8px 16px" in _pls.group(0),
   ".pl-sel must match .tool-btn geometry and colour")


# Learn drills, free practice and all three Play modes are tested through user-visible
# browser interactions in browser_checks.py.


# Learn exits and chapter-return navigation are exercised in browser_checks.py.
# The drill's chrome must match the app's, or it reads as a bolted-on quiz.
_cta = re.search(r"\.lr-cta\{[^}]*\}", idx_nofont, re.S)
ok(_cta is not None, ".lr-cta must exist")
if _cta:
    for _p in ("font-size:.85rem", "padding:8px 16px", "font-weight:700"):
        ok(_p in _cta.group(0), f".lr-cta must match .tool-btn on {_p}")
_ghost = re.search(r"(?m)^[ \t]*\.lr-ghost\{[^}]*\}", idx_nofont, re.S)
ok(_ghost is not None and "color:var(--teal)" in _ghost.group(0),
   ".lr-ghost must use the app's teal, like .tool-btn")
# .lr-qbox is deliberately --cream so the --paper options read as raised cards
# on top of it (owner: "all black and white, too bland"). Only .lr-step, which
# IS a card, must match .card exactly.
for _sel in (r"\.lr-step",):
    _m = re.search(_sel + r"\{[^}]*\}", idx_nofont, re.S)
    ok(_m is not None, f"{_sel} must exist")
    if _m:
        ok("var(--paper)" in _m.group(0), f"{_sel} must use --paper like .card")
        ok("box-shadow" in _m.group(0), f"{_sel} must carry .card's shadow")


# --------------------------------------------- verse ranges read as numbers
# Theme ranges and story references use the quieter --ink-soft tone in the
# current design. Lock that choice in both the app shell and chapter pages.
for _sel, _want in ((r"\.th-flow h3 \.rng", "--ink-soft"),
                    (r"\.lr-thread \.rg", "--ink-soft")):
    _m = re.search(_sel + r"\{[^}]*\}", idx_nofont, re.S)
    ok(_m is not None, f"index.html must style {_sel}")
    if _m:
        ok(f"color:var({_want})" in _m.group(0), f"{_sel} must use the current range tone")
for _sel, _tone in ((r"ol\.themes \.rng", "--ink-soft"),
                    (r"h2\.th \.rng", "--saffron-text")):
    _m = re.search(_sel + r"\{[^}]*\}", css, re.S)
    ok(_m is not None, f"chapter.css must style {_sel}")
    if _m:
        ok(f"var({_tone})" in _m.group(0), f"{_sel} must use the chapter-page range tone")

# Welcome-screen content is covered by rendered browser checks; UI key parity
# is validated from the structured dictionaries/document tests.


# ------------------------------------------------------ chrome consistency
# The theme toggle sits beside the language pills and intentionally shares their
# hover wash and light foreground so the SVG icon stays visible.
_lb = re.search(r"\.lang-btn:hover\{([^}]*)\}", idx_nofont)
_tb = re.search(r"\.theme-btn:hover\{([^}]*)\}", idx_nofont)
ok(_lb is not None and _tb is not None, "both hover rules must exist")
if _lb and _tb:
    norm = lambda d: {p.strip() for p in d.split(";") if p.strip()}
    ok(norm(_lb.group(1)) == norm(_tb.group(1)),
       f"theme-btn hover must match lang-btn hover exactly "
       f"(lang={sorted(norm(_lb.group(1)))} theme={sorted(norm(_tb.group(1)))})")
ok("background:var(--chip-hover)" in (_tb.group(1) if _tb else ""),
   "the theme button must share the language controls' hover wash")
# the sun/moon glyph is stroke:currentColor, so its hover foreground must stay explicit
ok("color:#FFF8EC" in (_tb.group(1) if _tb else ""),
   "theme-btn hover must set a light foreground for its icon")

# Phase 3.1: the "How would you like to receive this chapter?" caption is
# removed — with only two modes (Verses / Learn) the tab strip speaks for
# itself. The legacy .mode-lbl rule is gone intentionally; keep an empty
# placeholder so surrounding checks still line up.


# ------------------------------------------- verse titles: one voice, no gaps
# All 700 verse titles were Title Cased while the 222 theme titles are sentence
# case; and 86 leaned on a dangling pronoun or were too terse to mean anything
# alone, with 7 exact duplicates book-wide (owner 2026-09-02).
import json as _json
_vt = []
for _n in range(1, 19):
    _d = read("data", "ch%d.js" % _n)
    _obj = _json.loads(_d[_d.index("=") + 1:].rstrip().rstrip(";"))
    for _t in _obj["themes"]:
        for _p in _t["parts"]:
            _vt.append((_p["sutras"][0]["n"], _p["titles"]))
ok(len(_vt) == 700, f"expected 700 verse titles, found {len(_vt)}")
_en = [t["en"] for _, t in _vt]
ok(len(set(_en)) == len(_en),
   "verse titles must be unique book-wide, or two drill options render alike")
ok(all(t["en"] and t["ne"] and t["hi"] for _, t in _vt),
   "every verse title must exist in all three languages")
ok(max(len(t["en"]) for _, t in _vt) <= 54,
   "a verse title must stay short enough for a card")
# sentence case: at most a couple of Title Case survivors, all proper nouns
_tc = [n for n, t in _vt
       if len([w for w in t["en"].split(" ")[1:] if re.match(r"^[A-Z][a-z]{3,}$", w)]) >= 2]
ok(len(_tc) <= 10, f"verse titles should be sentence case; {len(_tc)} look Title Cased: {_tc[:5]}")


# View routing, theme disclosures, range-first headings and verse deep links
# are exercised against the app and generated chapter pages in browser_checks.py.


# --------------------------------- the shell must not inline fonts either
# chapter.css was de-base64'd on 2026-09-01, but index.html still inlined BOTH
# weights: 116 KB — 38% of the whole shell — for 85 KB of font, since base64
# inflates binary by 33%. The 400 weight was byte-identical to the .woff2
# already published beside it, so every visitor downloaded it twice. Inlining
# was justified as "no round-trip on first paint", but nothing renders until
# the whole document arrives, so it delayed first paint instead
# (owner 2026-09-02). Shell 305 KB -> 188 KB.
ok("base64," not in idx, "index.html must not inline any font as base64")
ok(idx.count('src:url("noto-deva-') == 2,
   "both Devanagari weights must be referenced as real files")
for _f in ("noto-deva-regular.woff2", "noto-deva-bold.woff2"):
    _p = os.path.join(ROOT, _f)
    ok(os.path.exists(_p), f"{_f} must be published at the site root")
    if os.path.exists(_p):
        with open(_p, "rb") as _fh:
            ok(_fh.read(4) == b"wOF2", f"{_f} must be a real woff2")
    ok(f"./{_f}" in read("sw.js"), f"{_f} must be precached, or offline loses it")
# Phase 3.1–3.3 (2026-10-16): raised from 250000 to 290000. The mobile
# overhaul adds ~17KB of useful UI (slim two-row header, bottom tabbar,
# m-head/m-menu/m-whole-verse hero, unified chapter view with theme
# headings + direct verse tap targets); the cap is to catch accidental
# bloat, not freeze UI evolution. Phase 2's explicit feature interfaces and
# session ownership bring the maintained baseline to about 293500 characters.
# Phase 5.4 (2026-10-19): data export/import adds ~17KB (backup UI + versioned
# JSON schema + merge logic); raise to 320000 to keep headroom for this
# user-data safety net.
ok(len(idx) < 320000, f"the shell should stay lean; it is {len(idx)} characters")


# ------------------------------------------------ font is a file, not base64
# chapter.css used to inline the Devanagari face as a data: URI: 58 KB, 93%
# font, re-downloaded for the chapter pages even though index.html already
# carries the identical bytes. As a real file it is fetched once and shared by
# all 18 pages. Three things must hold or Devanagari silently breaks.
FONT = "noto-deva-regular.woff2"
ok(os.path.exists(os.path.join(ROOT, FONT)), f"{FONT} must be published at the site root")
if os.path.exists(os.path.join(ROOT, FONT)):
    with open(os.path.join(ROOT, FONT), "rb") as f:
        head = f.read(4)
    ok(head == b"wOF2", f"{FONT} must be a real woff2 (magic bytes)")
    src = os.path.join(ROOT, "source", "fonts", FONT)
    if os.path.exists(src):
        with open(src, "rb") as _a, open(os.path.join(ROOT, FONT), "rb") as _b:
            _match = _a.read() == _b.read()
        ok(_match, f"published {FONT} must match source/fonts/")
ok("base64" not in css, "chapter.css must not inline a font as base64 again")
ok(f'url("{FONT}")' in css, "chapter.css must reference the font by relative URL")
# CSS resolves url() against the STYLESHEET, which sits at the site root — so a
# bare filename is correct for every /chapter/N/ page. A path like ../FONT or
# /FONT would break on a project page. Assert the bare form explicitly.
ok("url(\"./" not in css and "url(\"/" not in css and "url(\"../" not in css,
   "the font URL must stay a bare relative filename (project-page safe)")
ok(len(css) < 8000, f"chapter.css should be lean now, is {len(css)} bytes")
# precached, or the chapter pages lose their font offline
ok(f"./{FONT}" in read("sw.js"), f"sw.js must precache {FONT}")


# ------------------------------------------------- heading outline (a11y/SEO)
# The theme headings were <h3> directly under the page <h1>, skipping a level
# on all 18 pages. Screen-reader users navigate by heading level, and a skipped
# level reads as a missing section.
for n in range(1, 19):
    page = read("chapter", str(n), "index.html")
    levels = [int(m) for m in re.findall(r"<h([1-4])[\s>]", page)]
    ok(levels.count(1) == 1, f"chapter/{n}: must have exactly one <h1>")
    ok(levels and levels[0] == 1, f"chapter/{n}: first heading must be the <h1>")
    skips = [(a, b) for a, b in zip(levels, levels[1:]) if b - a > 1]
    ok(not skips, f"chapter/{n}: heading level skipped {skips[:1]}")


# Corrupt favorites and notes are tested through localStorage and the rendered
# favorites/verse views in browser_checks.py.


# ------------------------------------------- v/ retired, shares go to chapters
# The 700 per-verse pages were retired 2026-09-01 (GitHub's web uploader caps
# at 100 files). Verse links now target /chapter/N/#vN.NN.
ok(not os.path.isdir(os.path.join(ROOT, "v")), "v/ must stay retired")
# every verse must be reachable at its advertised anchor, or shares 404 silently
import json as _json
for n in range(1, 19):
    page = read("chapter", str(n), "index.html")
    ids = set(re.findall(r'<div class="v" id="(v\d+\.\d+)">', page))
    # The canonical chapter JSON carries verse IDs with each verse record;
    # chapter anchors use the same padded form, prefixed with `v`.
    with open(os.path.join(ROOT, "source", f"ch{n}.json"), encoding="utf-8") as f:
        source_chapter = _json.load(f)
    want = {f"v{verse['n']}" for theme in source_chapter["themes"]
            for part in theme["parts"] for verse in part["sutras"]}
    ok(ids == want, f"chapter/{n}: anchor set != verses in ch{n}.json "
                    f"(missing {sorted(want - ids)[:3]})")
# old links must still land somewhere useful
ok("/v/" in read("404.html"), "404.html must forward retired /v/ links")


# ----------------------------------------- 2b. no repeated verse line (Phase 2.2)
# A verse description that is word-for-word the verse's own English literal is
# a copy, not a description, and the chapter page must not print it twice.
# Each verse row therefore carries EITHER a .vd line with its exact distinct
# description OR no .vd line at all — never the literal reprinted, never an
# empty .vd, never a missing row.
import html as _html
for n in range(1, 19):
    page = read("chapter", str(n), "index.html")
    _d = read("data", "ch%d.js" % n)
    _obj = _json.loads(_d[_d.index("=") + 1:].rstrip().rstrip(";"))
    _want = {}
    for _t in _obj["themes"]:
        for _p in _t["parts"]:
            _s = _p["sutras"][0]
            _desc = _p["descs"]["en"].strip()
            _want[_s["n"]] = None if _desc == _s["lits"]["en"].strip() else _p["descs"]["en"]
    ok(len(re.findall(r'class="vrow"', page)) == len(_want),
       f"chapter/{n}: every verse needs exactly one vrow")
    _got = {}
    for _vid, _inner in re.findall(r'<a class="vrow" href="#v([\d.]+)">(.*?)</a>', page):
        _m = re.search(r'<div class="vd">(.*?)</div>$', _inner, flags=re.S)
        if _m:
            _got[_vid] = _html.unescape(_m.group(1))
    _distinct = {v for v, d in _want.items() if d is not None}
    ok(set(_got) == _distinct,
       f"chapter/{n}: .vd rows must be exactly the distinct descriptions "
       f"(stray {sorted(set(_got) - _distinct)[:3]}, missing {sorted(_distinct - set(_got))[:3]})")
    _wrong = [v for v in _distinct if _got.get(v) != _want[v]]
    ok(not _wrong, f"chapter/{n}: a kept .vd line changed text {_wrong[:3]}")


# --------------------------------------------------- 3. numbering doctrine
# PROJECT.md: humans read 1.1, never 1.01. URLs/ids keep the padded form.
# The bug: 700 chapter-page verse links printed "2.01 ↗" and every theme range
# read "2.01-2.03". The doctrine was enforced on share pages only.
pad_num = re.compile(r">(\d+)\.0(\d) ↗<")
pad_rng = re.compile(r'class="rng">[^<]*\.0\d')
pad_bold = re.compile(r"<b>(\d+)\.0(\d)</b>")
for n in range(1, 19):
    page = read("chapter", str(n), "index.html")
    ok(not pad_num.search(page), f"chapter/{n}: verse link shows padded number (2.01, not 2.1)")
    ok(not pad_rng.search(page), f"chapter/{n}: theme range shows padded numbers")
    ok(not pad_bold.search(page), f"chapter/{n}: verse row shows padded number")
    # ...while the machine-facing forms MUST stay padded, or links break
    ok('id="v%d.01"' % n in page, f"chapter/{n}: anchors must keep the padded id (v{n}.01)")
    ok("index.html#v=%d.01" % n in page, f"chapter/{n}: deep links must keep the padded form")


# ------------------------------------------------------ 4. offline integrity
# The bug: chapter.css was never precached, so a chapter page opened offline
# rendered unstyled while the manifest promised "Works offline".
sw = read("sw.js")
assets = re.findall(r"'(\./[^']*)'", re.search(r"ASSETS = \[(.*?)\];", sw, re.S).group(1))
ok("./chapter.css" in assets, "sw.js must precache ./chapter.css")
for a in assets:
    p = a[2:]
    ok(p == "" or os.path.exists(os.path.join(ROOT, p)), f"sw.js precaches missing file: {a}")
# the cache name must change whenever a precached asset changes, or readers are
# served stale files forever. chapter.css is in ASSETS, so it must be in the hash.
ver = re.search(r"const CACHE = 'gita-([0-9a-f]+)'", sw)
ok(ver is not None, "sw.js must carry a content-hashed cache version")
builder = read("source", "build_gita.py")
ok("CHAPTER_CSS" in re.search(r"CACHE_VER = hashlib\.sha256\((.*?)\)\.hexdigest",
                              builder, re.S).group(1),
   "CACHE_VER must hash CHAPTER_CSS, since chapter.css is precached")


# -------------------------------------------------------------- 6. 404 page
# The bug: none existed. Every stale share link was a dead end on GitHub's
# generic 404 with no route back into the app.
ok(os.path.exists(os.path.join(ROOT, "404.html")), "404.html must exist")
nf = read("404.html")
ok('name="robots" content="noindex' in nf, "404.html must be noindex")
ok(SITE_BASE in nf, "404.html must link back into the app")
ok("#chapter=" in nf, "404.html must recover a chapter fragment")
ok("/chapter/' + m[1] + '/#v" in nf,
   "404.html must forward a retired /v/N.NN/ link to the verse's chapter anchor")


# ------------------------------------------------- 7. Sanskrit is marked sa
# The bug: chapter pages emitted Devanagari in unmarked <div>s, so screen
# readers pronounced it with an English voice.
for n in (1, 2, 18):
    page = read("chapter", str(n), "index.html")
    ok('class="vdev" lang="sa"' in page, f"chapter/{n}: Devanagari must carry lang=sa")
    ok('class="viast" lang="sa-Latn"' in page, f"chapter/{n}: IAST must carry lang=sa-Latn")
    ok('class="deva" lang="sa"' in page, f"chapter/{n}: chapter title Devanagari must carry lang=sa")


# --------------------------------------------------- 8/10. app accessibility
# The bug: two <h1> on one document, and no live region — a screen reader user
# heard nothing at all when the single-page app swapped views.
h1_count = len(re.findall(r"<h1[\s>]", idx))
ok(h1_count == 1,
   f"index.html must have exactly one <h1>, found {h1_count}")


# ------------------------------------------------------------ 9. no dead code
# Not a user-facing fault, but it is how rot starts. The two unused helpers
# below are legacy code; continue to catch any additional dead functions.
defs = set(re.findall(r"function\s+([A-Za-z_$][\w$]*)\s*\(", idx_nofont))
dead = sorted(d for d in defs if len(re.findall(r"\b" + re.escape(d) + r"\b", idx_nofont)) < 2)
# dayVerse and lrSkip were the two exemptions here; both were deleted
# 2026-10-15, so nothing is grandfathered any more.
known_legacy_helpers = set()
unexpected_dead = sorted(set(dead) - known_legacy_helpers)
ok(not unexpected_dead, f"unexpected dead functions in index.html: {unexpected_dead}")


# ----------------------------------------------- retired per-verse card cards
# The 2026-09-01 decision: no img/v/ ever again.
ok(not os.path.isdir(os.path.join(ROOT, "img", "v")), "img/v/ must stay retired")
def _has_img_v(p):
    try:
        with open(p, encoding="utf-8") as _fh:
            return "/img/v/" in _fh.read()
    except OSError:
        return False
stale = [p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True) if _has_img_v(p)]
ok(not stale, f"pages still reference retired img/v/ cards: {stale[:3]}")


# ------------------------------------- source-script citations must be real
# chapter.css once promised a dedicated drift script in source/ (named
# check_chapter_css.py) — it was never written; the CSS-var guard lives in
# this file. A comment that names a guard which is not there is worse than no
# comment: it makes the reader trust a check that never runs. Every
# source/<name>.py cited from CODE must exist. Prose is exempt on purpose:
# PROJECT.md and HANDOFF.md record deleted scripts as history.
_cited = set()
_code = [os.path.join(ROOT, "build.py"), os.path.join(ROOT, "run_gita_app.js"),
         os.path.join(ROOT, "browser_checks.py"),
         os.path.join(ROOT, "chapter.css"), os.path.join(ROOT, "sw.js")]
for _pat in ("source/*.py", "tests/*.py", "tests/*.js", "tests/*.sh"):
    _code += glob.glob(os.path.join(ROOT, _pat))
for _p in _code:
    if os.path.isfile(_p):
        try:
            with open(_p, encoding="utf-8", errors="replace") as _fh:
                _txt = _fh.read()
        except OSError:
            continue
        for _m in re.finditer(r"source/([A-Za-z0-9_]+\.py)", _txt):
            _cited.add(_m.group(1))
_missing = sorted(n for n in _cited if not os.path.isfile(os.path.join(ROOT, "source", n)))
ok(not _missing, f"code cites source scripts that do not exist: {_missing}")
ok(bool(_cited), "the citation scan actually found citations to check (sanity)")


print(f"site-health checks: {checks}")
print(f"failures:           {len(errors)}")
for e in errors:
    print("  ! " + e)
print("RESULT:", "ALL GREEN" if not errors else "FAILURES", flush=True)
sys.exit(1 if errors else 0)
