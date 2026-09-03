#!/usr/bin/env python3
"""check_site_health.py — the faults found in the 2026-09-01 audit, locked shut.

Every check here corresponds to a real defect that shipped and that NO existing
suite caught, because the other suites read the app document (run_gita_app.js)
or the data (check_padas / check_paraphrase / check_seo). Nothing read the
generated CHAPTER pages, the CSS, or the <head> block. Since 2026-09-01 this
file also owns the share-link contract that verify_share_pages.py used to
cover, now that verse links are chapter anchors rather than 700 v/ pages.

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
    ok(imgs == [f"{SITE_BASE}/og-card.png"], f"{label}: og:image must be og-card.png, got {imgs}")
    ok(cards == ["summary_large_image"], f"{label}: twitter:card must be summary_large_image")
    # the declared dimensions must describe the image actually referenced
    ok(meta_values(page, "property", "og:image:width") == ["1200"], f"{label}: og:image:width")
    ok(meta_values(page, "property", "og:image:height") == ["630"], f"{label}: og:image:height")

# ------------------------------------------------ drill options must be fair
# Three ways a multiple-choice question quietly stops testing anything:
#   - two options render identically (looks like a bug, and is one)
#   - a distractor is already visible in the split, so it is eliminable at a
#     glance and the question is easier than it looks
#   - a distractor means the same as the answer, so two options are both right
# Measured before the fix: 0.7% duplicate, 2.4% leaked. Now 0 of 5000.
# Assert the guard STATEMENTS, not just that the identifiers appear somewhere —
# a substring check passed even after the guards were deleted, because the
# variable names still occurred in the surrounding lines.
ok("if(shownForms[x[0]]) return;" in idx,
   "a distractor already shown in the split must be rejected")
ok("if(seenOpt[x[0]]) return;" in idx,
   "two distractors must never be the same word")
ok("if(x[2] === c.w[2]) return;" in idx,
   "a distractor must not share the answer's meaning")
ok(idx.count("seenOpt[x[0]] = 1") == 1,
   "each accepted distractor must be recorded, or duplicates slip back in")

# Switching language mid-drill used to fall through setLang's generic restore:
# with state.theme set that lands on showVerses() and the drill vanishes.
# Switching language mid-drill used to fall through setLang's generic restore:
# with state.theme set that lands on showVerses() and the drill vanishes — the
# owner hit exactly this. It must re-enter the learn path, and lrRelang returns
# to the SAME theme rather than the chapter's path home.
ok("else if(state.view === 'learn'){ lrRelang(state.chapter); }" in idx,
   "setLang must re-enter the learn path, not drop the reader into showVerses")
ok("function lrRelang(" in idx, "the learn path needs a language-switch re-entry point")
ok("state.lrAt = {kind:'theme'" in idx, "the drilled theme must be recorded for re-entry")
ok("state.lrAt = {kind:'story'" in idx, "the story step must be recorded for re-entry")


# --------------------------------------------- learn drills must be answerable
# The cloze used to blank the word out of the RECITED line. Sanskrit sandhi
# means the dictionary form usually is not there literally (पश्य + एताम् ->
# पश्यैतां), so .replace() missed 52% of words and failed SILENTLY: the line
# rendered whole, the question asked what was missing when nothing was, and
# every option was equally arbitrary. It must blank a word from the AUTHORED
# word-split instead, which is data and always correct.
ok("lr-split" in idx, "the cloze must render the authored word-split")
ok("c.q.d.replace(c.w[0]" not in idx,
   "the cloze must never blank by string-replacing the sandhi'd line")
ok("lr-cue" in idx, "the recited line must still be shown as the cue")
# (superseded 2026-09-01 by the three explicit checks above, which cover form,
#  meaning AND on-screen visibility — the single combined filter missed the
#  duplicate-option and answer-leak cases entirely.)
# options are shown as the first pada, so two verses sharing one (6.15/6.28)
# would render identical choices with one marked wrong
ok("_full(o)!==mine" in idx,
   "which-verse distractors must be whole verses, distinct from the answer")
ok("const _full = v => v.d;" in idx, "the theme drill must offer whole verses")


# ------------------------------------------------------- sheet navigation
# Prev/Next died silently once every "part" became a single verse: partBounds()
# returned {start:n, end:n}, so in thematic study BOTH buttons were disabled on
# every verse in the app. And the reading modes opened the sheet with mode
# 'read', which navSutra() never handled — it hit `else return`, so the buttons
# did nothing at all. Neither failure threw; nothing caught them. Hence these.
ok("function themeBounds(" in idx, "the theme range must be computed from the THEME")
ok("partBounds" not in idx,
   "partBounds is gone — parts are one verse each, so it disabled every button")
ok("state.mode === 'read'" in idx, "navSutra must handle the reading modes")
ok("state.cStart" in idx and "state.cEnd" in idx,
   "read mode needs chapter bounds to clamp Prev/Next")
ok("state.mode==='read'" in idx, "the sheet needs a nav row for read mode")
# read mode is chapter-scoped; book mode (search/favourites) stays all 700
ok("Lof(state.gpos-state.cStart+1, state.cEnd-state.cStart+1)" in idx,
   "the read counter must read 'verse N of <chapter length>'")
ok("Lof(state.gpos+1, VERSES.length)" in idx,
   "search/favourites must still range over all 700")

# "part" is dead vocabulary: themes are granular now and hold verses directly.
_ui = read("source", "i18n_ui.py")
ok("Themes and parts" not in _ui, "no user-facing copy may still say 'parts'")
ok("भागहरूमा" not in _ui and "भागों में" not in _ui,
   "the Nepali/Hindi copy must not say 'parts' either")


# --------------------------------------------- the cloze must not leak its answer
# The recited pāda was printed under the word-split as a cue. Measured against
# the real data it gave the answer away in 6,069 of 6,394 questions — either
# literally (मामकाः inside मामकाः पाण्डवाश्चैव) or all but one letter (कुर्वत
# inside किमकुर्वत). Suppressing it "when the word is literally present" fixed
# only half. The cue is gone: the surrounding words of the split are the
# context, which is the recall actually being tested.
# (lr-cue survives in free practice, where the IAST is shown AFTER the reader
#  has finished — a reward, not a hint. What must not exist is a cue inside the
#  cloze question itself.)
ok("${c.q.d}</div>`" not in idx,
   "the cloze must not print the recited line as a cue")
ok("c.q.d.indexOf(c.w[0]) < 0" not in idx,
   "the half-measure cue guard must be gone, not merely narrowed")

# An ordering correction must clear the moment the reader gets it right, or it
# reads as though the new, correct answer were also wrong.
ok("if(fb) fb.innerHTML = '';" in idx,
   "a correct ordering tap must clear any standing correction")


# ------------------------------- every surface must carry the brand colours
# Owner 2026-09-02: "every page must represent our colours". The app had ZERO
# gradients and ONE accent bar — every card was a --paper box with a grey
# outline, so the saffron and teal accents inside had nothing to belong to.
# The house idiom is a 3px brand edge on a card's leading side: saffron for
# something you act on, teal for something already yours.
_SURFACES = (".card", ".theme", ".res-card", ".mode-box", ".lr-step", ".lr-chip",
             ".lr-q", ".pl-mode", ".lr-word", ".lr-finis", ".lr-opt", ".lr-qbox",
             ".lr-chip2", ".lr-slot")
for _sel in _SURFACES:
    _body = " ".join(" ".join(m.split()) for m in
        re.findall(r"(?<![\w.-])" + re.escape(_sel) + r"\{[^}]*\}", idx_nofont, re.S))
    ok(_body != "", f"{_sel} must exist")
    ok("--saffron" in _body or "--teal" in _body,
       f"{_sel} paints a surface but carries no brand colour")
# The edge in --saffron-soft measures 1.25:1 on --paper: invisible, and so not
# an edge at all. The resting state must be the real saffron.
# scope this to the LEADING edge: --saffron-soft is legitimate elsewhere
# (underlines, hover fills), it is only wrong as the house edge.
ok("border-left:2px solid var(--saffron-soft)" not in idx
   and "border-left:3px solid var(--saffron-soft)" not in idx,
   "a resting brand edge must be --saffron (2.47:1), not --saffron-soft (1.25:1)")
# Width-agnostic: the owner tuned 3px -> 2px for restraint ("not gaudy, Apple
# style"), and this check must not fight a future adjustment. What matters is
# that the edge EXISTS across the app and stays a hairline, not a stripe.
_edges = re.findall(r"border-left:(\d)px solid var\(--(?:saffron|teal)\)", idx)
ok(len(_edges) >= 6, "the house edge must be applied across the app's surfaces")
ok(all(int(w) <= 2 for w in _edges),
   f"the brand edge must stay a hairline; found widths {sorted(set(_edges))}")


# ------------------------------------------ a retry must not be a free guess
# Options were shuffled once at build time, so a requeued question returned
# with the four verses in the SAME positions — and the reader already knew
# which one was wrong. In Play, where the question comes back immediately,
# that made the retry a 1-in-3 guess (owner 2026-09-02).
ok("if(it.kind === 'pick' && it._seen) it.opts = lrShuffle(it.opts);" in idx,
   "a re-shown question must re-shuffle its options")
# Shuffling the ARRAY is what keeps lrPick honest: it reads it.opts[i].ok, and
# .ok travels with the option object, so the answer cannot desync.
ok("const it = LQ[LQi], o = it.opts[i];" in idx,
   "lrPick must resolve the answer through the option object, not a stored index")


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
ok("L('learn_retry')" in idx and idx.count('"learn_retry"') == 3,
   "the retry button must say what it does, in all three languages")
ok("learn_continue" not in idx, "the vague 'Continue' string is retired")


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
ok(_os is not None and "var(--saffron-dark)" in _os.group(0),
   "the verse number under an option is a number — saffron like the rest")
# Play's endless game has no progress to show
ok("const single = LQ.length === 1 && LQback;" in idx,
   "a one-item queue must not render a 0%-forever progress bar")


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


# ---------------------------------------------------------------- Play
# lrRun is shared by the learn path and Play. Its footer must follow the
# caller: Play passed ci=0 and so offered "back to chapter", which dropped the
# reader into chapter 1 from a game spanning the whole Gītā (owner 2026-09-01).
ok("var LQback = null;" in idx, "the drill footer needs a caller-supplied target")
ok("{fn:'showPlay()', label:'play_title'}" in idx,
   "Play must send the drill footer back to the Play menu")
ok("LQback\n      ? backFoot(LQback.fn, L(LQback.label))" in idx,
   "lrPaint must honour the caller's back target when one is given")
# A front door onto the drill engine, reachable from the tool row at any time.
# Unscored and unsaved by design: Learn by heart is the path with progress and
# gating, Play is the shuffle you drop into (owner 2026-09-01).
ok('id="playBtnTool"' in idx, "Play must sit in the tool row beside Random and Favorites")
for _f in ("function showPlay(", "function plStart(", "function plNext(", "function plPool("):
    ok(_f in idx, f"Play needs {_f.split('(')[0].split()[-1]}()")
ok(idx.count('"play"') == 3, "the Play label must exist in all three languages")
ok("PL.scope === 'ch'" in idx, "Play must offer a single-chapter scope")
# Mode 1: four verse PAIRS in the Gita open with an identical first pada
# (3.35/18.47, 6.15/6.28, 9.34/18.65, 16.07/18.30). Two identical options with
# one marked wrong is the same fault already fixed in the theme drills.
ok("plFull(o)!==mine" in idx,
   "Play mode 1 options must be whole verses, and distinct from the answer")
ok("plP0" not in idx, "Play must not offer first pādas as options")
ok("const plFull = v => v.d;" in idx, "a Play option is the whole verse")
# Mode 2: near misses from the same chapter. Random numbers from elsewhere are
# given away by chapter recognition alone and test nothing.
ok("o.n.split('.')[0] === s.n.split('.')[0]" in idx,
   "Play mode 2 distractors must be near misses from the same chapter")
ok("pool.length < 4" in idx, "Play must refuse a pool too small to build options")
# Play holds its question in the queue; a language switch must return to its menu.
# A language switch must REBUILD the question in the new language, not quit the
# game — only the prompt, the note and the numerals were language-bound, and
# all three are derivable from the verse (owner 2026-09-02).
ok("else if(state.view === 'play'){ if(PL.q && PL.mode) plNext(PL.q); else showPlay(); }" in idx,
   "setLang must rebuild the open Play question, not drop the reader to the menu")
ok("function plNext(keep)" in idx, "plNext must accept a question to rebuild")
# All THREE modes must record it — a bare substring passed with mode 1 gutted,
# because modes 2 and 3 still matched.
ok(idx.count("PL.q = {n:s.n, ord:") == 3,
   "each Play mode must record its verse and option order for rebuilding")


# ------------------------------------ free practice must actually shuffle
# The pādas were rendered straight from FP.order — their natural sequence — so
# there was nothing to put in order and the whole mode was a no-op (owner
# 2026-09-01). A display order is now dealt ONCE per verse and held in state:
# shuffling inside the paint would move the chips on every tap, and the answer
# check must keep using the TRUE index, not the displayed position.
ok("FP.deal = deal;" in idx, "free practice must deal a shuffled display order")
ok("(FP.deal||FP.order.map((_,i)=>i)).map(ix=>" in idx,
   "free-practice chips must render from the dealt order")
ok("deal.some((ix,k)=>ix!==k)" in idx,
   "the deal must reject the identity permutation, which looks like the bug")
_paint = re.search(r"function lrFreePaint\(\)\{[\s\S]*?\n\}", idx)
ok(_paint is not None and "lrShuffle" not in _paint.group(0),
   "lrFreePaint must not reshuffle — the chips would move on every tap")


# ------------------------------- every verse drilled; free practice at the end
# The quarter drill ran on one random verse per theme, leaving 478 of the 700
# never practised that way. It now runs on every verse (owner 2026-09-01).
ok("vs.forEach(qv=>{" in idx, "the quarter drill must cover every verse of the theme")
ok("const qv = vs[Math.floor(Math.random()*vs.length)];" not in idx,
   "the quarter drill must not sample a single verse per theme")
# Free practice: unlimited, unscored, outside the queue engine.
for _f in ("function lrFree(", "function lrFreePick(", "function lrFreePaint(", "function lrFreeTap("):
    ok(_f in idx, f"free practice needs {_f.split('(')[0].split()[-1]}()")
ok("learn_shuffle" in idx and idx.count('"learn_shuffle"') == 3,
   "the shuffle button must exist in all three languages")
ok("guard++ < 12" in idx, "shuffle must not hand back the same verse twice running")
# and the completion screen must offer the chapter, not the path
ok("onclick=\"showRead(${ci},'full')\">${esc(L('back_chapter_one'))}" in idx,
   "the theme completion screen must offer 'back to chapter'")
ok(idx.count("L('learn_back_path')") == 0,
   "'back to the path' is retired — every exit goes to the chapter")


# ------------------------------------------- ordering drills must test recall
# The verse-order chips used to read "1.1 · King Dhṛtarāṣṭra asks…". Printing
# the number turns recall into sorting integers, which tests nothing — the
# owner caught it at ch1.t1 (2026-09-01). The paraphrase alone is the cue, and
# it is unique across all 700 verses at that length.
ok("label: T(s.paras).slice(0, 64)" in idx,
   "verse-order chips must be the paraphrase alone")
ok("fmtNL(s.n)+' \u00b7 '+T(s.paras)" not in idx,
   "verse-order chips must not print the verse number")
# Reordering the four pādas of a śloka: every verse has exactly four, all
# distinct, so the drill is always fair.
ok("learn_qorder" in idx, "the quarter-order drill must exist")
ok(idx.count('"learn_qorder"') == 3, "learn_qorder must exist in all three languages")
ok("chips: qq.map((q,i)=>({id:i, label:q.d, deva:1}))" in idx,
   "quarter chips must carry the Devanagari flag")
ok(".lr-chip2.dv{" in idx, "Devanagari chips need the Sanskrit face")
ok(".lr-slot.dv{" in idx, "a placed Devanagari chip must keep the Sanskrit face")


# ------------------------------------ the learn path must feel like the app
# Owner 2026-09-01: the drill's footer said "back to path" and led to the learn
# home — a half-step nobody asked for. Every footer inside the learn path now
# returns to the CHAPTER, which is what a chapter card opens. Exactly one
# "back to the path" survives, on the completion screen, where it is right.
ok(idx.count("L('back_chapter_one')") >= 3,
   "learn views must return to the chapter, not the path home")
ok(idx.count('"back_chapter_one"') == 3,
   "back_chapter_one must exist in all three languages")

# The drill's chrome must match the app's, or it reads as a bolted-on quiz.
_cta = re.search(r"\.lr-cta\{[^}]*\}", idx_nofont, re.S)
ok(_cta is not None, ".lr-cta must exist")
if _cta:
    for _p in ("font-size:.85rem", "padding:8px 16px", "font-weight:700"):
        ok(_p in _cta.group(0), f".lr-cta must match .tool-btn on {_p}")
_ghost = re.search(r"\.lr-ghost\{[^}]*\}", idx_nofont, re.S)
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
# A theme's verse range (1.1-1.3) is a verse NUMBER and must look like one.
# All four render sites used --ink-soft, so the range sank into the prose
# while every other number in the app is saffron (owner 2026-09-01).
for _sel, _want in ((r"\.th-flow h3 \.rng", "--saffron-dark"),
                    (r"\.lr-thread \.rg", "--saffron-dark")):
    _m = re.search(_sel + r"\{[^}]*\}", idx_nofont, re.S)
    ok(_m is not None, f"index.html must style {_sel}")
    if _m:
        ok(f"color:var({_want})" in _m.group(0), f"{_sel} must be {_want}, not muted")
for _sel in (r"ol\.themes \.rng", r"h2\.th \.rng"):
    _m = re.search(_sel + r"\{[^}]*\}", css, re.S)
    ok(_m is not None, f"chapter.css must style {_sel}")
    if _m:
        ok("var(--saffron)" in _m.group(0), f"{_sel} must be saffron, not muted")

# The work-in-progress note on the welcome screen, in all three languages.
ok('class="w-wip"' in idx, "the welcome screen must carry the work-in-progress note")
ok(idx.count('"wip"') == 3, "the wip string must exist in en, ne and hi")


# ------------------------------------------------------ chrome consistency
# The theme toggle sits in the same pill row as the language buttons and must
# hover identically. It used to get a faint --chip-hover wash and keep its
# saffron text, so the icon went saffron-on-saffron and the control felt dead
# next to its neighbours.
_lb = re.search(r"\.lang-btn:hover\{([^}]*)\}", idx_nofont)
_tb = re.search(r"\.theme-btn:hover\{([^}]*)\}", idx_nofont)
ok(_lb is not None and _tb is not None, "both hover rules must exist")
if _lb and _tb:
    norm = lambda d: {p.strip() for p in d.split(";") if p.strip()}
    ok(norm(_lb.group(1)) == norm(_tb.group(1)),
       f"theme-btn hover must match lang-btn hover exactly "
       f"(lang={sorted(norm(_lb.group(1)))} theme={sorted(norm(_tb.group(1)))})")
ok("--chip-hover" not in (_tb.group(1) if _tb else ""),
   "the theme button must not fall back to the faint --chip-hover wash")
# the sun/moon glyph is stroke:currentColor, so the hover colour must be set
# or the icon stays saffron on a saffron fill
ok("color:var(--on-saffron)" in (_tb.group(1) if _tb else ""),
   "theme-btn hover must set a text colour, or the icon vanishes into the fill")

# The "How would you like to receive this chapter?" caption must NOT be the
# same saffron as the pills it labels — a caption that looks pressable is a
# lie, and --saffron-dark measured 3.34:1 on white, under the AA floor.
_ml = re.search(r"\.mode-lbl\{([^}]*)\}", idx_nofont)
ok(_ml is not None, ".mode-lbl rule must exist")
if _ml:
    ok("--saffron" not in _ml.group(1),
       "the mode caption must not reuse the pills' saffron")
    ok("var(--ink-soft)" in _ml.group(1),
       "the mode caption should be --ink-soft (AA in both themes)")


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


# ---------------------------------------- every view must name itself
# showVerses was the only view in the app with no heading: the theme's name
# appeared in the crumb trail and then nowhere on the page, so the reader
# arrived at a description with no subject (owner 2026-09-02).
_sv = re.search(r"function showVerses\([^)]*\)\{[\s\S]*?\n\}", idx)
ok(_sv is not None, "showVerses must exist")
if _sv:
    ok('class="view-title fade-in">${esc(T(t.titles))}' in _sv.group(0),
       "the theme page must show the theme's title, not only its description")
# .rng is scoped to .th-flow h3; beside a view title it would inherit 1.7rem
ok(".view-title .rng{" in idx,
   "a range beside a view title needs its own size, or it shouts over the name")


# ------------------------------------------ [hidden] must actually hide
# The word grid carried the hidden attribute but opened on arrival: [hidden] is
# only display:none at the UA default, and .lr-words sets display:grid, which
# silently wins. Any element rendered with [hidden] whose class also sets a
# display needs an explicit [hidden] guard (owner 2026-09-02).
ok(".lr-words[hidden]{ display:none; }" in idx,
   "a collapsed word grid needs an explicit [hidden] rule to beat display:grid")
_hidden_classes = set()
for _m in re.finditer(r'class="([a-z0-9 _-]+)"[^>]*\shidden', idx):
    _hidden_classes.update(_m.group(1).split())
for _c in sorted(_hidden_classes):
    _has_display = any("display:" in _r for _r in
        re.findall(r"(?<![\w.-])\." + re.escape(_c) + r"\{[^}]*\}", idx_nofont, re.S))
    if _has_display:
        ok(f".{_c}[hidden]" in idx,
           f".{_c} is rendered hidden but sets display — it needs a [hidden] guard")


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
ok(len(idx) < 230000, f"the shell should stay lean; it is {len(idx)} bytes")


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
        ok(open(src, "rb").read() == open(os.path.join(ROOT, FONT), "rb").read(),
           f"published {FONT} must match source/fonts/")
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


# --------------------------------------- corrupt localStorage must not brick
# JSON.parse succeeding does not mean the shape is right: a stored 'null', '5'
# or '{}' parses fine and then throws on .includes(), which runs on every verse
# modal — one bad write would make every verse unopenable with no way back.
ok("Array.isArray(a)" in idx, "favLoad must verify it got an array")
ok("typeof o !== 'object'" in idx, "favNoteLoad must verify it got an object")


# ------------------------------------------- v/ retired, shares go to chapters
# The 700 per-verse pages were retired 2026-09-01 (GitHub's web uploader caps
# at 100 files). Verse links now target /chapter/N/#vN.NN.
ok(not os.path.isdir(os.path.join(ROOT, "v")), "v/ must stay retired")
ok("root + '/chapter/'" in idx,
   "the app's share button must build /chapter/N/#vN.NN links")
ok("/v/' +" not in idx, "the app must not build /v/ share links any more")
# every verse must be reachable at its advertised anchor, or shares 404 silently
import json as _json
for n in range(1, 19):
    page = read("chapter", str(n), "index.html")
    ids = set(re.findall(r'<div class="v" id="(v\d+\.\d+)">', page))
    # ch<N>.json keys the verses by bare number ("1", "2", ...); the page
    # anchors use the padded chapter.verse form (v2.01), same as every URL.
    with open(os.path.join(ROOT, "source", f"ch{n}.json"), encoding="utf-8") as f:
        want = {f"v{n}.{int(k):02d}" for k in _json.load(f)["verses"]}
    ok(ids == want, f"chapter/{n}: anchor set != verses in ch{n}.json "
                    f"(missing {sorted(want - ids)[:3]})")
    # a verse anchor inside a folded <details> is unreachable without this
    ok("d.open = true" in page, f"chapter/{n}: must open the folded block on a deep link")
    ok('id="det-' in page, f"chapter/{n}: <details> blocks need stable ids")
# old links must still land somewhere useful
ok("/v/" in read("404.html"), "404.html must forward retired /v/ links")


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
ok(len(re.findall(r"<h1[\s>]", idx)) == 1,
   f"index.html must have exactly one <h1>, found {len(re.findall(r'<h1[\s>]', idx))}")
ok('aria-live="polite"' in idx, "index.html must expose a polite live region")
ok("announceView()" in idx, "view changes must be announced to assistive tech")
ok(".sr-only{" in idx, "the live region needs its visually-hidden class")


# ------------------------------------------------------------ 9. no dead code
# Not a user-facing fault, but it is how rot starts.
defs = set(re.findall(r"function\s+([A-Za-z_$][\w$]*)\s*\(", idx_nofont))
dead = sorted(d for d in defs if len(re.findall(r"\b" + re.escape(d) + r"\b", idx_nofont)) < 2)
ok(not dead, f"dead functions in index.html: {dead}")


# ----------------------------------------------- retired per-verse card cards
# The 2026-09-01 decision: no img/v/ ever again.
ok(not os.path.isdir(os.path.join(ROOT, "img", "v")), "img/v/ must stay retired")
stale = [p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
         if "/img/v/" in open(p, encoding="utf-8").read()]
ok(not stale, f"pages still reference retired img/v/ cards: {stale[:3]}")


print(f"site-health checks: {checks}")
print(f"failures:           {len(errors)}")
for e in errors:
    print("  ! " + e)
print("RESULT:", "ALL GREEN" if not errors else "FAILURES", flush=True)
sys.exit(1 if errors else 0)
