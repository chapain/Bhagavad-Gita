# -*- coding: utf-8 -*-
"""build_gita.py — builds the interactive Bhagavad Gita study app (text-only, 4-pāda format)."""
import json, os, re, sys, shutil, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_ui import UI
from schema import validate_chapters
from verify import norm1, syll_iast

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(os.path.abspath(__file__))
GITA_DIR = ROOT  # the project folder itself — build publishes the app in place
os.makedirs(GITA_DIR, exist_ok=True)

# ---------------- the chapter data ----------------
# One JSON file is the source of truth for each chapter. The build validates
# these records and publishes them; it does not assemble verse content from
# parallel Python modules.
def load_chapters():
    chapters = []
    for num in range(1, 19):
        path = os.path.join(BASE, f"ch{num}.json")
        try:
            with open(path, encoding="utf-8") as f:
                chapter = json.load(f)
        except (OSError, json.JSONDecodeError) as exc:
            raise SystemExit(f"source/ch{num}.json: {exc}")
        chapters.append(chapter)
    schema_errors = validate_chapters(chapters)
    if schema_errors:
        raise SystemExit("canonical chapter schema failed:\n" +
                         "\n".join(f"  - {error}" for error in schema_errors))
    return chapters

data = load_chapters()
total = sum(len(part["sutras"]) for ch in data for theme in ch["themes"] for part in theme["parts"])
print("verses embedded:", total)

# verify pāda structure from the canonical typed flow
print("\n--- pāda verification ---")
for ch in data:
    for theme in ch["themes"]:
        for part in theme["parts"]:
            for v in part["sutras"]:
                pads = [x for x in v["flow"] if x["k"] == "p"]
                counts = [x["n"] for x in pads]
                has_speaker = any(x["k"] == "s" for x in v["flow"])
                print(f"{v['n']}: pādas={counts}" + ("  [SPK]" if has_speaker else ""))

# verify source integrity: flow concat == source
def normstr(x): return x.replace(" ","").replace("|","").replace("।","").replace("॥","").replace("’","")
bad_src = []
for ch in data:
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                full = "".join(x['t'] for x in v['flow'])
                if normstr(full) != normstr(v['t']):
                    bad_src.append(v['n'])
print("\nsource-integrity issues:", bad_src if bad_src else "NONE ✓")

# verify every pāda has words
miss = 0
for ch in data:
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                for it in v["flow"]:
                    if it["k"]=="p" and not it.get("words"):
                        miss += 1
print("pādas missing word data:", miss)

# ---------------------------------------------------------------------------
# Manual-edit audit. Every piece of content is meant to be hand-editable, and a
# hand edit must never be silently ignored. This stops the build if a source
# file says something the app would not show.
# ---------------------------------------------------------------------------
problems = []

# Structural shape, field types, ranges, language maps and nested word rows
# are rejected by schema.validate_chapters() before this semantic audit runs.
# 0. d/t must remain segmentable for the reading view; verseLines() derives
#    display rows from these strings and places speaker rows by the IAST marker.
for ch in data:
    for theme in ch["themes"]:
        for part in theme["parts"]:
            for verse in part["sutras"]:
                deva = [x.strip() for x in verse["d"].split("।") if x.strip()]
                iast = [x.strip() for x in verse["t"].split("।") if x.strip()]
                if len(deva) != len(iast):
                    problems.append(f"{verse['n']}: d/t must contain matching danda-separated segments")
                elif sum(not t.endswith("uvāca") for t in iast) != 2:
                    problems.append(f"{verse['n']}: d/t must contain exactly two verse lines")

# 1. the pādas stored beside each verse must still spell its IAST text, and
#    their syllable counts must add up. This catches accidental edits to the
#    combined source record before that data is published.
_sq = lambda x: re.sub(r"[\s|।॥’']", "", norm1(x))
for ch in data:
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                pads = [x for x in v["flow"] if x["k"] == "p"]
                joined = _sq("".join(x["t"] for x in pads))
                # the verse's own IAST, minus any speaker line
                body = " ".join(seg for seg in v["t"].split("।")
                                if not seg.strip().endswith("uvāca"))
                if joined != _sq(body):
                    problems.append(
                        f"source/ch{ch['num']}.json: the pādas of {v['n']} do not reconstruct "
                        f"the verse's IAST.\n      verse : {_sq(body)}\n      pādas : {joined}")
                for x in pads:
                    real = syll_iast(x["t"])
                    if real != x["n"]:
                        problems.append(
                            f"source/ch*.json: {v['n']} pāda \"{x['t']}\" is marked {x['n']} "
                            f"syllables but has {real} — fix the number.")

# 1b. a pāda must not begin with a consonant stranded from the previous pāda's
#     last word (16.19: "…aśubhā" | "nāsurīṣveva" instead of "…aśubhān" |
#     "āsurīṣveva"). Both spell the verse, so check 1 cannot see it; the tell is
#     that the pāda stops one letter short of its own last word.
_CONS = "kgcjtdpbnmrlsvyh\u015b\u1e63\u1e47\u1e6d\u1e0d\u00f1\u1e45"
for ch in data:
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                pads = [x for x in v["flow"] if x["k"] == "p"]
                wl_by_i = [x.get("words") or [] for x in pads]
                for i in range(len(pads) - 1):
                    wl = wl_by_i[i]
                    if not wl:
                        continue
                    last = norm1(wl[-1][1]).replace(" ", "")
                    text = norm1(pads[i]["t"]).replace(" ", "")
                    nxt = norm1(pads[i + 1]["t"]).replace(" ", "")
                    if not last or last[-1] not in _CONS:
                        continue
                    if text.endswith(last):
                        continue
                    if text.endswith(last[:-1]) and nxt[:1] == last[-1]:
                        problems.append(
                            f"source/ch*.json: {v['n']} pāda {i+1} ends one letter short of its "
                            f"last word '{wl[-1][1]}' — the '{last[-1]}' is stranded at the "
                            f"start of pāda {i+2}. Move it back.\n"
                            f"      pāda {i+1}: {pads[i]['t']}\n"
                            f"      pāda {i+2}: {pads[i+1]['t']}")

# 1c. typography of the pāda text itself: no stray space at either end and no
#     double space. These are invisible in HTML, so nothing else would catch
#     them, but they live in your data files and travel with copied text.
for ch in data:
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                for it in v["flow"]:
                    for fld, what in (("d", "Devanagari"), ("t", "IAST")):
                        txt = it.get(fld, "")
                        if txt != txt.strip():
                            problems.append(f"source/ch*.json: {v['n']} has a stray space at the "
                                            f"start or end of its {what}: {txt!r}")
                        elif "  " in txt:
                            problems.append(f"source/ch*.json: {v['n']} has a double space in its "
                                            f"{what}: {txt!r}")

# 1d. metre: an anuṣṭubh verse (32 syllables) must divide 8/8/8/8 and a triṣṭubh
#     (44) must divide 11/11/11/11. A pāda that is short or long by one is almost
#     always a boundary placed inside a word — the fault behind 17.28 and the
#     twelve verses that began with a consonant stranded from the pāda before.
for ch in data:
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                pads = [x for x in v["flow"] if x["k"] == "p"]
                counts = [x["n"] for x in pads]
                total = sum(counts)
                if len(counts) != 4:
                    continue
                want = 8 if total == 32 else (11 if total == 44 else None)
                if want and any(c != want for c in counts):
                    problems.append(
                        f"source/ch*.json: {v['n']} is {total} syllables, so each pāda should be "
                        f"{want}, but they are {counts} — a boundary is inside a word.")

# 1e. an avagraha (ऽ / ’) marks an elided initial vowel, so it belongs at the
#     START of the pāda whose word lost that vowel, never dangling at the end of
#     the pāda before (8.20 ...bhāvo’nyo | ’vyakto..., not ...bhāvo’nyo’ | vyakto...).
for ch in data:
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                for it in v["flow"]:
                    if it["k"] != "p":
                        continue
                    if it["t"].endswith("\u2019") or it["d"].endswith("\u0951") or it["d"].endswith("\u093d"):
                        problems.append(
                            f"source/ch*.json: {v['n']} ends a pāda with an avagraha: {it['t']!r}. "
                            f"It marks the next word's elided vowel, so move it to the start "
                            f"of the following pāda.")

# 1f. unapplied sandhi: a word ending -aḥ becomes -o before a voiced consonant
#     (1.15 hṛṣīkeśaḥ devadattaṃ should read hṛṣīkeśo devadattaṃ). Leaving the
#     visarga is a transcription slip, not a variant reading.
_VOICED = set("gjdbnmyrlvh\u1e45\u00f1\u1e47\u1e0d")
for ch in data:
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                for m in re.finditer(r"(\w*a\u1e25)\s+([a-z\u0101\u012b\u016b\u1e5b\u1e5d\u1e37\u1e45\u00f1\u1e6d\u1e0d\u1e47\u015b\u1e63\u1e43\u1e25])", v["t"]):
                    if m.group(2) in _VOICED:
                        good = m.group(1)[:-2] + "o"
                        problems.append(
                            f"ch*.json: {v['n']} has '{m.group(1)} {m.group(2)}...' — before a "
                            f"voiced consonant the visarga becomes o, so this should read "
                            f"'{good} {m.group(2)}...'.")

# 2. every text is present in all three languages; non-English fields may not
#    silently fall back to English.
LANGS = ("en", "ne", "hi")
def check_language_map(obj, field, where):
    values = obj.get(field, {})
    if set(values) != set(LANGS):
        problems.append(f"{where}: {field} must contain en/ne/hi")
        return
    for lang in LANGS:
        if not isinstance(values[lang], str) or not values[lang].strip():
            problems.append(f"{where}: empty {lang} {field}")
        elif lang != "en" and values[lang] == values["en"]:
            problems.append(f"{where}: {lang} {field} falls back to English")

for ch in data:
    check_language_map(ch, "names", f"chapter {ch['num']}")
    check_language_map(ch, "subs", f"chapter {ch['num']}")
    for ti, theme in enumerate(ch["themes"], 1):
        where = f"chapter {ch['num']} theme {ti}"
        check_language_map(theme, "titles", where)
        check_language_map(theme, "descs", where)
        for pi, part in enumerate(theme["parts"], 1):
            pwhere = f"{where} part {pi}"
            check_language_map(part, "titles", pwhere)
            check_language_map(part, "descs", pwhere)
            for verse in part["sutras"]:
                check_language_map(verse, "lits", verse["n"])
                check_language_map(verse, "paras", verse["n"])

# 3. verse ranges are read from the same chapter file as the verse content;
#    require the exact verse sequence so a missing or repeated record cannot
#    disappear silently during rendering.

# 4. every verse must sit in exactly one part (a bad range in source/ch*.json
#    silently drops or duplicates verses)
for ch in data:
    if not ch["themes"]: continue
    seen = {}
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                seen[v["n"]] = seen.get(v["n"], 0) + 1
    dupes = sorted(k for k, c in seen.items() if c > 1)
    expected = {f"{ch['num']}.{i:02d}" for i in range(1, ch["verses"] + 1)}
    missing = sorted(expected - set(seen))
    if dupes:   problems.append(f"chapter {ch['num']}: verses appear in more than one part: {dupes[:5]} — check the records in source/ch{ch['num']}.json")
    if missing: problems.append(f"chapter {ch['num']}: verses in ch{ch['num']}.json are in no part, so they are unreachable: {missing[:5]} — check the records in source/ch{ch['num']}.json")

# 6. every part must hold exactly one verse (2026-08-26: a part IS a verse;
#    its title is the verse's own name, shown wherever the verse is shown).
#    Staged per chapter as the batches land — extend CONVERTED each batch.
CONVERTED = set(range(1, 19))
for ch in data:
    if ch["num"] not in CONVERTED: continue
    for ti, t in enumerate(ch["themes"]):
        for pi, p in enumerate(t["parts"]):
            if len(p["sutras"]) != 1:
                problems.append(f"chapter {ch['num']} theme {ti+1} part {pi+1} holds "
                                f"{len(p['sutras'])} verses — every part must hold exactly one")
#    drafting slashes (found 2026-08-26: "Karmaṇy-Evādhikāras Te" as a part
#    title, and "… / the Traveler" as a theme title). Short genuine terms
#    that happen to be a verse's first word (ज्ञानयज्ञ, ब्रह्मभूत) are fine —
#    the defect class is long meaningless truncations, so Devanagari titles
#    are only checked from 12 chars, IAST from 8.
def _tstrip(x): return re.sub(r'[\s।॥’\-—.]', '', x).lower()
for ch in data:
    for ti, t in enumerate(ch["themes"]):
        for lang, tt in t["titles"].items():
            if ' / ' in tt:
                problems.append(f"chapter {ch['num']} theme {ti+1} [{lang}] title has a drafting slash: {tt!r}")
        for pi, p in enumerate(t["parts"]):
            first = p["sutras"][0]
            d, iast = _tstrip(first["d"]), _tstrip(first["t"])
            for lang, tt in p["titles"].items():
                ts = _tstrip(tt)
                if ' / ' in tt:
                    problems.append(f"chapter {ch['num']} theme {ti+1} part {pi+1} [{lang}] title has a drafting slash: {tt!r}")
                # verbatim Sanskrit openings (title wholly inside the verse's
                # devanagari, or matching the IAST) are the defect; translated
                # headings that merely share a first word are fine (4.13 ne/hi).
                if (len(ts) >= 12 and d.startswith(ts)) or (len(ts) >= 8 and iast.startswith(ts)):
                    problems.append(f"chapter {ch['num']} theme {ti+1} part {pi+1} [{lang}] title is the raw opening of its verse, not a headline: {tt!r}")

if problems:
    print("\nMANUAL-EDIT AUDIT FAILED")
    for x in problems: print("  ✗", x)
    raise SystemExit(1)
print("manual-edit audit: NONE ✓")

# ---------------- app templates (HTML / CSS / JS) ----------------
# Feature-sized source files are concatenated in this explicit order, then
# inlined into the same single shell as before. They are authoring boundaries,
# not browser modules: no bundler, extra request or runtime loader is involved.
def _read_template(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as _f:
        return _f.read()

def _read_templates(folder, names):
    return "".join(_read_template(os.path.join(folder, name)) for name in names)

HTML = _read_template("app.html")
APP_CSS_FILES = (
    "00-foundation.css", "10-play.css", "20-learn.css",
    "30-favorites.css", "40-welcome.css", "50-reader-shell.css",
    "60-responsive.css",
)
APP_JS_FILES = (
    "00-core.js", "10-library.js", "20-learn.js", "30-play.js",
    "35-drills.js", "40-views.js", "50-reader.js", "60-runtime.js",
)
APP_CSS = _read_templates("css", APP_CSS_FILES)
APP_JS = _read_templates("js", APP_JS_FILES)

# ---------------- embedded Devanagari font ----------------
# The app asked for "Noto Serif Devanagari" but shipped no font, so on any device
# without it installed (older Android, most Windows) the conjuncts — क्ष, द्ध,
# ङ्ग — break apart or show as boxes. The reader would see a broken page and we
# would never know. These are subset to the Devanagari block only: ~42 KB each,
# about 2% of the file, and they guarantee every reader sees the same text.
# Noto Serif Devanagari, SIL Open Font License 1.1 — see source/fonts/OFL-*.txt
def _font_face():
    """Publish both weights as REAL FILES and reference them by URL.

    They were inlined as base64, which cost 116 KB — 38% of the whole shell —
    for 85 KB of actual font, because base64 inflates binary by 33%. Worse, the
    400 weight was byte-identical to noto-deva-regular.woff2 already published
    beside it for the chapter pages, so every visitor downloaded those same
    40.7 KB twice (owner 2026-09-02).

    Inlining was originally justified as "no second round-trip on first paint".
    That reasoning inverted as the shell grew: nothing renders until the whole
    HTML arrives, so 116 KB of font in the document DELAYS first paint rather
    than protecting it. As files they are fetched in parallel, cached once
    across every page, and revalidated independently of the app.

    font-display:swap means text is readable immediately in a fallback serif
    and reflows when the face lands — the same trade the chapter pages already
    make. Both files are precached by the service worker, so this costs nothing
    offline.
    """
    faces = []
    for weight, fname in ((400, "noto-deva-regular.woff2"), (700, "noto-deva-bold.woff2")):
        path = os.path.join(BASE, "fonts", fname)
        if not os.path.exists(path):
            print(f"WARNING: {fname} missing — Devanagari will fall back to a system font")
            continue
        # GITA_DIR, not SITE_DIR: this runs at line ~3293, before SITE_DIR is
        # defined. They are the same directory in this repo.
        shutil.copyfile(path, os.path.join(GITA_DIR, fname))
        # index.html sits at the site root, so a bare filename resolves for it
        # and for the service worker's './' precache entries alike.
        faces.append(
            '  @font-face{ font-family:"Noto Serif Devanagari"; font-style:normal;\n'
            f'    font-weight:{weight}; font-display:swap;\n'
            f'    src:url("{fname}") format("woff2"); }}')
    return "\n".join(faces)

# ---- one artefact: the split site ------------------------------------------
# A light shell (index.html) + one data file per chapter (data/ch<N>.js) that
# the shell loads at startup and the service worker precaches. First paint
# arrives after ~120 KB instead of ~5 MB, and editing one verse invalidates one
# small file, not the whole app. The owner retired the all-in-one file
# (2026-08-24): the site is shared by link, and the service worker still makes
# it fully offline after the first visit.
_ui_js = json.dumps(UI, ensure_ascii=False)
# Historical verse-range maps protect saved learning progress during regrouping.
# Current chapter content still comes exclusively from the source data above.
with open(os.path.join(BASE, "study_map_contract.json"), encoding="utf-8") as _mf:
    _legacy_maps = json.load(_mf)["legacy_map_options"]
_legacy_maps_js = json.dumps(_legacy_maps, ensure_ascii=False, separators=(",", ":"))
_font_css = _font_face()
data_js = [f"GITA_CH[{ch['num']}] = {json.dumps(ch, ensure_ascii=False)};\n" for ch in data]

_ch_len = "[" + ",".join(str(ch["verses"]) for ch in data) + "]"
_loader = (
    f"const CH_LEN = {_ch_len};\n"
    "const _chWait = {};\n"
    "function appBase(){\n"
    "  var path = location.pathname || '/';\n"
    "  if (/\\/index\\.html$/i.test(path)) path = path.replace(/\\/index\\.html$/i, '/');\n"
    "  else if (path.charAt(path.length-1) !== '/') path += '/';\n"
    "  return location.origin + path;\n"
    "}\n"
    "function loadChapter(n){\n"
    "  n = +n;\n"
    "  if (GITA_CH[n] && GITA_CH[n].themes) return Promise.resolve();\n"
    "  if (_chWait[n]) return _chWait[n];\n"
    "  _chWait[n] = new Promise(function(resolve, reject){\n"
    "    var s = document.createElement('script');\n"
    "    s.src = appBase() + 'data/ch' + n + '.js';\n"
    "    s.onload = function(){ assembleData(); resolve(); };\n"
    "    s.onerror = function(){ gitaLoadFail(); reject(new Error('data/ch' + n + '.js failed to load')); };\n"
    "    document.head.appendChild(s);\n"
    "  });\n"
    "  return _chWait[n];\n"
    "}\n"
    "function loadAllChapters(){\n"
    "  var ps = []; for (var n = 1; n <= 18; n++) ps.push(loadChapter(n));\n"
    "  return Promise.all(ps);\n"
    "}\n"
    "function gitaLoadFail(){ var b = document.getElementById('bootNote');\n"
    "  if (b) b.textContent = 'Could not load the verse data. Check your connection and reload.'; }\n"
    "window.__gitaLoaded = function(){};\n"
)
_tags = "<script>gitaBoot();</script>"

# Icon substitution — single source for each SVG so the shell stays lean
# (same path reused by toolbar buttons, bottom tab bar, and dark-mode toggle).
def _icon_svg(slug):
    return {"home":'<svg class="ic" viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg>',
            "search":'<svg class="ic" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>',
            "shuffle":'<svg class="ic" viewBox="0 0 24 24"><path d="M16 3h5v5"/><path d="M21 3 4 20"/><path d="M21 16v5h-5"/><path d="m15 15 6 6"/><path d="m4 4 5 5"/></svg>',
            "play":'<svg class="ic" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="8.5" cy="8.5" r="1.4" fill="currentColor"/><circle cx="15.5" cy="15.5" r="1.4" fill="currentColor"/><circle cx="15.5" cy="8.5" r="1.4" fill="currentColor"/><circle cx="8.5" cy="15.5" r="1.4" fill="currentColor"/></svg>',
            "star":'<svg class="ic" viewBox="0 0 24 24"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
            "moon":'<svg class="ic" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
            "clearx":'<svg class="ic" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>'}[slug]
# Fill the concatenated CSS/JS templates before inserting them into the HTML
# shell. app.html owns the newline before </style>; remove the final CSS
# module's EOF newline so it does not add a blank line to the document.
_app_css = APP_CSS[:-1] if APP_CSS.endswith("\n") else APP_CSS
_app_css = _app_css.replace("__FONTS__", _font_css)
_app_js = (APP_JS
           .replace("__UI__", _ui_js)
           .replace("__LR_LEGACY_JSON__", _legacy_maps_js)
           .replace("__DATALOADER__", _loader))
# Keep the source file's conventional single EOF newline while preserving the
# original blank line before </script> in the generated shell.
_app_js += "\n"
shell = HTML.replace("__APP_CSS__", _app_css).replace("__APP_JS__", _app_js)
for _slug, _key in (("home","__ICON_HOME__"),("search","__ICON_SEARCH__"),
                    ("shuffle","__ICON_SHUFFLE__"),("play","__ICON_PLAY__"),
                    ("star","__ICON_STAR__"),("moon","__ICON_MOON__"),
                    ("clearx","__ICON_CLEARX__")):
    shell = shell.replace(_key, _icon_svg(_slug))
shell = shell.replace("__DATASCRIPTS__", _tags)

# ---- site base URL, used only for the absolute og:image / og:url ----
# Override with:  SITE_BASE=https://user.github.io/repo python3 build_gita.py
SITE_BASE = os.environ.get("SITE_BASE", "https://chapain.github.io/Bhagavad-Gita").rstrip("/")
shell = shell.replace("__BASE__", SITE_BASE)

# Optional Google Search Console verification. The token is not secret — it
# ships inside the public page — so it lives in a plain file: paste the value
# of the google-site-verification meta tag into source/gsc_token.txt and
# rebuild. No file (or an empty one) → no tag is emitted.
_gsc_path = os.path.join(BASE, "gsc_token.txt")
_gsc = open(_gsc_path, encoding="utf-8").read().strip().strip('"') if os.path.exists(_gsc_path) else ""
if _gsc:
    _gsc_tag = f'<meta name="google-site-verification" content="{_gsc}">\n'
else:
    _gsc_tag = ""
shell = shell.replace("<!--GSC-->\n", _gsc_tag)

out = shell
path = os.path.join(GITA_DIR, "index.html")
with open(path, "w", encoding="utf-8") as f:
    f.write(out)
print("written:", path, round(len(out)/1024), "KB shell")
_datadir = os.path.join(GITA_DIR, "data")
os.makedirs(_datadir, exist_ok=True)
for _ch, _js in zip(data, data_js):
    with open(os.path.join(_datadir, f"ch{_ch['num']}.js"), "w", encoding="utf-8") as f:
        f.write(_js)
print(f"written: {len(data_js)} chapter data files under {_datadir}/")

# ---------------- web-app files (published alongside index.html) ----------------
SITE_DIR = GITA_DIR          # in this repo the root *is* the published site
os.makedirs(SITE_DIR, exist_ok=True)

import base64 as _b64
import html as _h

# The Devanagari face is published as a REAL FILE, not inlined as base64.
# It used to be a data: URI inside chapter.css, which made that one stylesheet
# 58 KB — 93% font — and, worse, the browser had to re-download the whole thing
# for the chapter pages even though index.html already carries the identical
# bytes inline. Base64 also inflates binary by ~33%. As a file it is fetched
# ONCE and reused across all 18 chapter pages, and chapter.css drops to ~4 KB.
# index.html keeps its own inlined copy on purpose: it is the app shell, and a
# separate request there would cost a round-trip on first paint.
# font-display:swap so the text is readable before the face arrives.
_FONT_FILE = "noto-deva-regular.woff2"
_ch_font_path = os.path.join(BASE, "fonts", _FONT_FILE)
_ch_font = ""
if os.path.exists(_ch_font_path):
    shutil.copyfile(_ch_font_path, os.path.join(SITE_DIR, _FONT_FILE))
    # chapter.css lives at the site root, so a bare relative URL resolves for
    # every /chapter/N/ page without any depth juggling.
    _ch_font = ('@font-face{font-family:"Noto Serif Devanagari";font-style:normal;'
                'font-weight:400;font-display:swap;'
                f'src:url("{_FONT_FILE}") format("woff2");}}')
else:
    print(f"WARNING: {_FONT_FILE} missing — chapter pages fall back to a system serif")

# One shared stylesheet for all 18 pages (cached after the first visit).
# Warm dark mode like the app — never pure black or white (PROJECT.md §4.7).
CHAPTER_CSS = _ch_font + """
/* The muted tone is --ink-soft, spelled exactly as in the app's own palette.
   It was declared as --soft here for one build while all 12 rules below asked
   for var(--ink-soft): the variable resolved to nothing and every muted line
   (breadcrumb, IAST, verse description, theme range, paraphrase) fell back to
   full --ink, flattening the hierarchy on all 18 pages. Keep the two names
   identical — source/check_site_health.py (CSS-var guard) now fails the build
   if they drift. */
:root{ --paper:#FFF8EC; --ink:#2A2118; --ink-soft:#5C5142; --accent:#1A5648;
       --saffron:#E8912C; --saffron-dark:#C97A20; --saffron-text:#875519; --card:#FFFFFF; --line:#E7D9C2; }
@media (prefers-color-scheme:dark){
  :root{ --paper:#16120D; --ink:#E9DCC3; --ink-soft:#A79A80; --accent:#8FBEB0;
         --saffron:#E1953A; --saffron-dark:#C8862F; --saffron-text:#D0AA70; --card:#201A13; --line:#382D20; }
}
*{ box-sizing:border-box; }
body{ margin:0; background:var(--paper); color:var(--ink);
      font:17px/1.65 Georgia,"Noto Serif Devanagari",serif; }
main{ max-width:680px; margin:0 auto; padding:26px 20px 10px; }
.crumb{ font-size:.85rem; color:var(--ink-soft); margin:0 0 18px; }
.crumb a{ color:var(--accent); text-decoration:none; }
h1{ font-size:1.55rem; line-height:1.3; margin:0 0 4px; color:var(--accent); }
.deva{ font-family:"Noto Serif Devanagari",serif; font-size:1.25rem;
       margin:2px 0 16px; color:var(--accent); overflow-wrap:anywhere; word-break:normal; }
.blurb{ margin:0 0 14px; }
.blurb span{ display:block; font-size:.95rem; color:var(--ink-soft); margin-top:4px; }
.verse{ margin:18px 0; padding:16px 18px; background:var(--card);
        border:1px solid var(--line); border-radius:14px; }
.verse blockquote{ margin:0; font-family:"Noto Serif Devanagari",serif;
        font-size:1.12rem; line-height:2; overflow-wrap:anywhere; word-break:normal; }
.verse figcaption{ margin-top:10px; font-size:.82rem; color:var(--ink-soft); }
h2{ font-size:1.05rem; margin:24px 0 10px; color:var(--accent); }
ol.themes{ margin:0; padding-left:22px; }
ol.themes li{ margin:6px 0; }
ol.themes .rng{ color:var(--ink-soft); font-weight:500; font-size:.8rem; white-space:nowrap; }
.cta{ display:inline-block; margin:18px 0 10px; padding:10px 22px;
      background:var(--saffron); color:#2A2118; border-radius:999px;
      text-decoration:none; font-weight:700; font-size:.92rem; }
footer{ max-width:680px; margin:0 auto; padding:20px 20px 34px;
        font-size:.85rem; color:var(--ink-soft); }
footer a{ color:var(--accent); text-decoration:none; }
ol.toc a{ color:var(--ink); text-decoration:none; border-bottom:1px dotted var(--ink-soft); }
details.theme{ background:var(--card); border:1px solid var(--line); border-radius:12px;
               margin:14px 0; transition:border-color .15s; }
details.theme:hover{ border-color:var(--saffron); }
summary.theme-summary{ cursor:pointer; color:var(--accent); font-size:1rem; line-height:1.5;
                       list-style-position:inside; padding:12px 16px; }
summary.theme-summary::marker{ color:var(--saffron-text); }
h2.th{ display:inline; font-size:1.02rem; color:var(--accent); margin:0;
       border:0; padding:0; }
h2.th .rng{ color:var(--saffron-text); font-weight:700; font-size:.82rem; margin-right:8px;
            white-space:nowrap; }
.theme-body{ padding:0 16px 16px; }
.th-open{ display:inline-block; margin:10px 0 4px; color:var(--accent); font-size:.86rem;
          text-decoration:none; border-bottom:1px dotted var(--accent); }
.th-open:hover{ color:var(--saffron-text); border-color:var(--saffron-text); }
.v{ margin:16px 0 22px; }
.vnum{ font-size:.78rem; font-weight:700; color:var(--saffron-text); letter-spacing:.04em; }
.vnum a{ color:inherit; text-decoration:none; border-bottom:1px dotted var(--saffron-text); }
.vdev{ font-family:"Noto Serif Devanagari",serif; font-size:1.14rem; line-height:1.85;
       margin:2px 0 3px; color:var(--accent); overflow-wrap:anywhere; word-break:normal; }
.viast{ font-style:italic; color:var(--ink-soft); font-size:.85rem; margin:0 0 7px; }
.vtr{ margin:4px 0; font-size:.95rem; }
.vtr .para{ display:block; color:var(--ink-soft); font-size:.9rem; margin-top:2px; }
@media (prefers-color-scheme:dark){ .cta{ color:#1A1209; background:var(--saffron); } }
/* Chapter pages begin with theme titles and ranges; details reveal summaries. */
.np{ color:var(--ink-soft); font-size:.9rem; margin:0 0 6px; }
details.theme[open] > summary.theme-summary{ border-bottom:1px solid var(--line); }
.tdesc{ margin:8px 0 6px; color:var(--ink-soft); font-size:.95rem; }
.vrows{ margin-top:6px; }
a.vrow{ display:block; padding:10px 8px; border-top:1px solid var(--line);
        text-decoration:none; border-radius:8px; }
a.vrow:hover{ background:var(--paper); }
.vrow .vt{ color:var(--accent); font-weight:700; font-size:.9rem; }
.vrow .vt b{ color:var(--saffron-text); margin-right:6px; }
.vrow .vd{ color:var(--ink-soft); font-size:.85rem; margin-top:2px; line-height:1.5; }
/* The verse a shared link points at. Also matches :target so it still reads
   as "the one you came for" when JS is off and the reader expands by hand. */
.v.target, .v:target{ background:var(--card); border-radius:12px;
        box-shadow:0 0 0 2px var(--saffron); padding:12px 14px; margin:12px -14px;
        scroll-margin-top:24px; }
@media (prefers-reduced-motion:no-preference){
  html{ scroll-behavior:smooth; }
}
details{ margin:4px 0 0; }
summary{ cursor:pointer; color:var(--saffron-text); font-weight:600; font-size:.88rem; }
/* Phase 2.3: the chapter colophon closes the page's text. Same restraint as in
   the app: a hairline rule, soft ink, the Devanagari with its transliteration. */
.colophon{ margin:22px 0 10px; padding-top:14px; border-top:1px solid var(--line);
           color:var(--ink-soft); font-family:"Noto Serif Devanagari",Georgia,serif;
           font-size:.93rem; line-height:1.8; }
.colophon .col-iast{ display:block; margin-top:6px; font-family:Georgia,"Noto Serif Devanagari",serif;
           font-style:italic; font-size:.85rem; line-height:1.6; }
"""

# cache version — bump automatically from the content hash of EVERY precached
# artefact (shell + all data files + chapter.css) so any change invalidates the
# old service-worker cache. chapter.css is in the hash because it is in ASSETS:
# leaving it out would let a stylesheet-only fix ship while readers keep being
# served the previous CSS from a cache that never expires. Anything added to
# ASSETS must be added here too.
# The font is a precached BINARY, so it is hashed by content too: if the face
# is ever swapped or subset, the cache must invalidate or readers keep the old
# one forever. Anything added to ASSETS must be added here.
# Both weights are precached binaries now, so both must invalidate the cache.
_font_bytes = b""
for _fn in ("noto-deva-regular.woff2", "noto-deva-bold.woff2"):
    _fp = os.path.join(BASE, "fonts", _fn)
    if os.path.exists(_fp):
        _font_bytes += open(_fp, "rb").read()
CACHE_VER = hashlib.sha256(
    (out + "".join(data_js) + CHAPTER_CSS).encode("utf-8") + _font_bytes).hexdigest()[:12]

manifest = {
    "name": "Bhagavad Gita — an Interactive Study",
    "short_name": "Gita",
    "description": "All 18 chapters, 700 verses in English · नेपाली · हिन्दी, with word-by-word meanings. Works offline.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "any",
    "background_color": "#FFF8EC",
    "theme_color": "#1A5648",
    "lang": "en",
    "dir": "ltr",
    "categories": ["books", "education", "lifestyle"],
    "author": "Dhruba Chapain, Pokhara, Nepal",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}
with open(os.path.join(SITE_DIR, "manifest.webmanifest"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

SW = """/* sw.js — offline cache for the Bhagavad Gita study app.
   Strategy: cache-first for the shell (the app is one static file and never
   changes between deploys), with a network revalidation for navigations so a
   new deploy is picked up on the next visit. */
const CACHE = 'gita-%%VER%%';
/* chapter.css is precached even though the app itself never loads it: a reader
   who arrives on a /chapter/N/ landing page and later opens it offline would
   otherwise get an unstyled wall of text, while the manifest and README both
   promise "Works offline". The chapter PAGES stay out of the precache on
   purpose (18 of them, ~1.3 MB) — the runtime handler below caches whichever
   ones the reader actually visits, and now their stylesheet and its Devanagari
   font are always there. The font is a real file rather than a data: URI, so
   it is fetched once and shared by all 18 pages — but that also means it is a
   network request, which offline would fail without this line. */
const ASSETS = ['./', './index.html', './manifest.webmanifest',
                './icon-192.png', './icon-512.png', './icon-maskable-512.png',
                './apple-touch-icon.png', './favicon.ico', './chapter.css',
                './noto-deva-regular.woff2', './noto-deva-bold.woff2',
                %%DATAASSETS%%];

self.addEventListener('install', e => {
  /* addAll() is atomic — if even one optional asset 404s nothing is cached,
     while install still "succeeds" and the app silently loses its offline
     promise. Add each URL on its own: one bad asset costs that asset, not
     the whole cache, and install still never aborts. */
  e.waitUntil(caches.open(CACHE)
    .then(c => Promise.all(ASSETS.map(u => c.add(u).catch(() => undefined))))
    .then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;   // never touch cross-origin requests

  // The service worker script itself MUST come from the network every time, or
  // the browser can never discover a new worker and the cache pins itself
  // forever across deploys (typical "stuck SW" bug).
  if (url.pathname.endsWith('/sw.js') || url.pathname.endsWith('\\sw.js')) {
    e.respondWith(fetch(req).catch(() => caches.match(req)));
    return;
  }

  if (req.mode === 'navigate') {
    // network-first for the page itself, so updates land; fall back to cache offline.
    // Only the app root is stored as the shell: caching any other page (e.g. a
    // /chapter/N/ landing page) as './index.html' would poison the offline fallback.
    e.respondWith(
      fetch(req)
        .then(res => {
          const u = new URL(req.url), root = new URL('./', location.href).pathname;
          if (u.pathname === root || u.pathname === root + 'index.html') {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put('./index.html', copy));
          }
          return res; })
        .catch(() => caches.match('./index.html').then(r => r || caches.match('./'))
          .then(r => r || new Response(
            '<!doctype html><meta charset="utf-8"><title>Offline</title>' +
            '<p>You are offline and this page is not cached yet. Reconnect and reload.</p>',
            { status: 504, headers: { 'Content-Type': 'text/html; charset=utf-8' } })))
    );
    return;
  }
  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      if (res && res.status === 200 && res.type === 'basic') {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
      }
      return res;
    }).catch(() => hit || new Response('', { status: 504, statusText: 'Offline' })))
  );
});
""".replace("%%VER%%", CACHE_VER) \
   .replace("%%DATAASSETS%%", ", ".join(f"'./data/ch{ch['num']}.js'" for ch in data))
with open(os.path.join(SITE_DIR, "sw.js"), "w", encoding="utf-8") as f:
    f.write(SW)

# ---------------- chapter landing pages (SEO satellites) ----------------
# Eighteen small static pages, one per chapter, rendered purely from the same
# `data` the app displays — no new content, no derivation. They give search
# engines lightweight, keyword-rich entry points ("bhagavad gita chapter 2 in
# nepali") and hand the reader to the full app through a #chapter=N deep link.
# The app itself is the split site: a shell plus data/ch<N>.js per chapter.
with open(os.path.join(SITE_DIR, "chapter.css"), "w", encoding="utf-8") as f:
    f.write(CHAPTER_CSS)

for _ch in data:
    _n = _ch["num"]
    _en = _ch["names"]["en"]
    _url = f"{SITE_BASE}/chapter/{_n}/"
    _nverses = _ch["verses"]
    # Phase 2.3: the closing colophon for this chapter (from source/ch<N>.json).
    _col = _ch.get("colophon") or {}
    _col_html = ""
    if _col.get("deva"):
        _col_html = (f'  <div class="colophon" lang="sa">{_h.escape(_col["deva"])}'
                     f'<span class="col-iast" lang="sa-Latn">'
                     f'{_h.escape(_col.get("iast", ""))}</span></div>')
    _desc = (f"Read Chapter {_n} of the Bhagavad Gita ({_en}) — all {_nverses} verses "
             f"in Sanskrit with translations in English, Nepali and Hindi.")
    # Each theme is a native disclosure: its range and title stay visible as
    # an outline, while the description and verse titles appear on expansion.
    # The full text remains in a nested <details> for progressive disclosure.
    # ---- doctrine numbers (PROJECT.md): humans read 1.1, never 1.01 --------
    # URLs, ids and anchors keep the padded data form (v1.01) so they stay
    # sortable and stable; only the TEXT a reader sees is unpadded. The old
    # `.replace(".0", ".")` trick was doing this by luck, not by rule.
    def _dnum(_x):
        _c, _v = str(_x).split(".")
        return f"{_c}.{int(_v)}"
    def _drange(_r):
        # "1.01–1.03" -> "1.1–1.3"; a single verse is "2.10" not "2.10–2.10"
        for _sep in ("–", "-"):
            if _sep in _r:
                _a, _b = _r.split(_sep, 1)
                _a, _b = _dnum(_a.strip()), _dnum(_b.strip())
                return _a if _a == _b else _a + "–" + _b
        return _dnum(_r)

    _sections = []
    for _i, _t in enumerate(_ch["themes"], 1):
        _vblocks = []
        for _p in _t["parts"]:
            for _s in _p["sutras"]:
                _para = _s["paras"].get("en", "")
                _vblocks.append(
                    f'<div class="v" id="v{_h.escape(str(_s["n"]))}">'
                    f'<div class="vnum"><a href="../../index.html#v={_h.escape(str(_s["n"]))}" '
                    f'title="Study this verse in the app">{_h.escape(_dnum(_s["n"]))} ↗</a></div>'
                    f'<div class="vdev" lang="sa">{_h.escape(_s["d"])}</div>'
                    f'<div class="viast" lang="sa-Latn">{_h.escape(_s["t"])}</div>'
                    f'<div class="vtr">{_h.escape(_s["lits"]["en"])}'
                    + (f'<span class="para">{_h.escape(_para)}</span>' if _para else "")
                    + f'</div>'
                    f'<div class="vtr" lang="ne">{_h.escape(_s["lits"]["ne"])}</div>'
                    f'<div class="vtr" lang="hi">{_h.escape(_s["lits"]["hi"])}</div>'
                    f'</div>')
        _rows = []
        for _p2 in _t["parts"]:
            # Phase 2.2: a verse description that is word-for-word the
            # verse's own English literal is a copy — the line is left
            # out of the page rather than printed twice. Distinct
            # descriptions keep the .vd line as before.
            _vd = _p2["descs"]["en"].strip()
            _row = (f'<a class="vrow" href="#v{_h.escape(str(_p2["sutras"][0]["n"]))}">'
                    f'<div class="vt"><b>{_h.escape(_dnum(_p2["sutras"][0]["n"]))}</b>'
                    f'{_h.escape(_p2["titles"]["en"])}</div>')
            if _vd != _p2["sutras"][0]["lits"]["en"].strip():
                _row += f'<div class="vd">{_h.escape(_p2["descs"]["en"])}</div>'
            _rows.append(_row + "</a>")
        _rows = "".join(_rows)
        _sections.append(
            f'  <details class="theme" id="theme-{_i}">\n'
            f'    <summary class="theme-summary"><h2 class="th">'
            f'<span class="rng">{_h.escape(_drange(_t["range"]))}</span> '
            f'<span class="th-title">{_h.escape(_t["titles"]["en"])}</span></h2></summary>\n'
            f'    <div class="theme-body">\n'
            f'      <a class="th-open" href="../../index.html#theme={_n}.{_i - 1}">Study this theme in the app →</a>\n'
            f'      <p class="tdesc">{_h.escape(_t["descs"]["en"])}</p>\n'
            f'      <div class="vrows">{_rows}</div>\n'
            f'      <details id="det-{_i}"><summary>Read the verses</summary>\n'
            + "\n".join("    " + v for v in _vblocks) +
            '\n      </details>\n    </div>\n  </details>')
    _text = "\n".join(_sections)
    _ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": f"Bhagavad Gita — Chapter {_n}: {_en}",
        "url": _url,
        "description": _desc,
        "inLanguage": ["en", "ne", "hi"],
        "isPartOf": {"@type": "WebApplication",
                     "name": "Bhagavad Gita — an Interactive Study",
                     "url": f"{SITE_BASE}/"},
    }, ensure_ascii=False, indent=2)
    _page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bhagavad Gita Chapter {_n} — {_h.escape(_en)}</title>
<meta name="description" content="{_h.escape(_desc)}">
<meta name="author" content="Dhruba Chapain">
<link rel="canonical" href="{_url}">
<meta property="og:type" content="website">
<meta property="og:title" content="Bhagavad Gita Chapter {_n} — {_h.escape(_en)}">
<meta property="og:description" content="{_h.escape(_desc)}">
<meta property="og:url" content="{_url}">
<meta property="og:site_name" content="Bhagavad Gita — an Interactive Study">
<meta property="og:image" content="{SITE_BASE}/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Bhagavad Gita Chapter {_n} — {_h.escape(_en)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Bhagavad Gita Chapter {_n} — {_h.escape(_en)}">
<meta name="twitter:description" content="{_h.escape(_desc)}">
<meta name="twitter:image" content="{SITE_BASE}/og-card.png">
<meta name="twitter:image:alt" content="Bhagavad Gita Chapter {_n} — {_h.escape(_en)}">
<link rel="icon" href="../../favicon.ico" sizes="any">
<link rel="stylesheet" href="../../chapter.css">
<script type="application/ld+json">
{_ld}
</script>
</head>
<body>
<main>
  <p class="crumb"><a href="../../">Bhagavad Gita</a> › Chapter {_n}</p>
  <h1>Chapter {_n} — {_h.escape(_en)}</h1>
  <p class="deva" lang="sa">{_ch["deva"]}</p>
  <p class="blurb">{_h.escape(_ch["subs"]["en"])}
    <span lang="ne">{_h.escape(_ch["subs"]["ne"])}</span>
    <span lang="hi">{_h.escape(_ch["subs"]["hi"])}</span></p>
  <p><a class="cta" href="../../index.html#chapter={_n}&tab=study">Enter chapter {_n} →</a></p>
  <p class="np">{_nverses} verses · {len(_ch["themes"])} themes — expand a theme to see its verse titles and descriptions.</p>
{_text}
{_col_html}
  <p><a class="cta" href="../../index.html#chapter={_n}&tab=study">Enter chapter {_n} →</a></p>
</main>
<footer>
  <a href="../../">← Bhagavad Gita — an Interactive Study</a><br>
  Sanskrit text: public domain · Translations © 2026 Dhruba Chapain<br>
  Created by <b>Dhruba Chapain</b>, Pokhara, Nepal.
</footer>
<script>
/* Shared verse links land inside two collapsed disclosures: the theme, and
   the full-text verse list. Open every enclosing block before scrolling so the
   target has a layout box; repeat on hashchange for in-page navigation.
   Without JS the student can expand both layers by hand. */
(function(){{
  function reveal(){{
    var h = location.hash;
    if(!h || h.charAt(1) !== 'v') return;
    var el;
    try{{ el = document.getElementById(decodeURIComponent(h.slice(1))); }}catch(e){{ return; }}
    if(!el) return;
    var d = el.closest('details');
    while(d){{
      d.open = true;
      d = d.parentElement ? d.parentElement.closest('details') : null;
    }}
    document.querySelectorAll('.v.target').forEach(function(n){{ n.classList.remove('target'); }});
    el.classList.add('target');
    el.scrollIntoView({{block:'center'}});
  }}
  if(document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', reveal);
  else reveal();
  window.addEventListener('hashchange', reveal);
}})();
</script>
</body>
</html>
"""
    _dir = os.path.join(SITE_DIR, "chapter", str(_n))
    os.makedirs(_dir, exist_ok=True)
    with open(os.path.join(_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(_page)
print(f"chapter pages: {len(data)} full-text chapters written under {os.path.join(SITE_DIR, 'chapter')}/ + chapter.css")

# ---------------- per-verse share pages RETIRED (owner 2026-09-01) --------
# There were 700 of them (v/N.NN/index.html), one per verse, existing only to
# carry per-verse Open Graph tags — social crawlers run no JS and never see a
# #fragment. They worked, but they made publishing miserable: GitHub's web
# uploader refuses more than 100 files at a time, so every republish meant
# seven manual drag-and-drops. (git push has no such limit, but the owner
# publishes through the browser.)
#
# They are replaced by a redirect: share links now point at
#   /chapter/N/#vN.NN
# which already exists, already contains the full verse — Devanagari, IAST and
# all three translations — and is already indexed. The chapter page's inline
# script opens the enclosing <details> and highlights the verse, so a shared
# link still lands ON the verse rather than at the top of the page.
#
# THE TRADE, stated plainly: the link PREVIEW is now the chapter's, not the
# verse's. Every verse in chapter 2 previews as "Chapter 2 — Sāṅkhya Yoga".
# The verse itself no longer appears in the WhatsApp card. That is the price
# of never touching the web uploader again, and the owner chose it knowingly.
#
# Old v/ links already sent to people keep working: 404.html recovers the
# verse number from the dead path and forwards to the app. Delete the v/
# folder on the live site whenever convenient — nothing breaks either way.
import shutil as _sh
_vdir_old = os.path.join(SITE_DIR, "v")
if os.path.isdir(_vdir_old):
    _sh.rmtree(_vdir_old)
    print("share pages: v/ removed — verse links now go to /chapter/N/#vN.NN")
else:
    print("share pages: none (verse links go to /chapter/N/#vN.NN)")

# ---------------- share artwork img/share-art.jpg (owner 2026-09-01) ------
# One painted face for the site, not 700. If PIL or the bundled fonts are
# missing in some future environment, warn and continue — every page still
# carries its full text tags and og-card.png.
try:
    from PIL import Image, ImageDraw, ImageFont
    _HAVE_PIL = True
except ImportError:
    _HAVE_PIL = False
    print("WARNING: Pillow missing — share art skipped (img/share-art.jpg not repainted)")

if _HAVE_PIL:
    # The ONE share artwork — the site's own face for every preview
    # (owner's call 2026-09-01: light repo over 700 painted cards).
    _FW = os.path.join(BASE, "fonts")
    _deva_f  = lambda px: ImageFont.truetype(os.path.join(_FW, "share-deva.ttf"), px)
    _lat_f   = lambda px: ImageFont.truetype(os.path.join(_FW, "share-latin.ttf"), px)
    _latb_f  = lambda px: ImageFont.truetype(os.path.join(_FW, "share-latin-bold.ttf"), px)
    _CREAM, _INK, _TEAL, _SAF, _SAFD, _SOFTL = "#FFF8EC", "#2A2118", "#1A5648", "#E8912C", "#C97A20", "#5C5142"

    def _wrap(draw, text, font, maxw):
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=font) <= maxw: cur = t
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        return lines

    _artdir = os.path.join(SITE_DIR, "img")
    os.makedirs(_artdir, exist_ok=True)
    _a = Image.new("RGB", (1200, 630), _CREAM); _ad = ImageDraw.Draw(_a)
    _ad.rectangle([28, 28, 1171, 601], outline=_SAF, width=3)
    _ad.rectangle([40, 40, 1159, 150], fill=_TEAL)
    _ad.text((70, 58), "ॐ", font=_deva_f(58), fill=_SAF)
    _ad.text((150, 66), "Bhagavad Gita — an Interactive Study", font=_latb_f(40), fill=_CREAM)
    _ad.text((150, 112), "श्रीमद्भगवद्गीता · १८ अध्याय · ७०० श्लोक", font=_deva_f(24), fill="#C5DDD4")
    _t = "श्रीमद्भगवद्गीता"; _w = _ad.textlength(_t, font=_deva_f(64))
    _ad.text(((1200 - _w) / 2, 240), _t, font=_deva_f(64), fill=_INK)
    _t = "Every verse in its four quarters, with word-by-word meanings"
    _w = _ad.textlength(_t, font=_lat_f(28))
    _ad.text(((1200 - _w) / 2, 352), _t, font=_lat_f(28), fill=_TEAL)
    _ad.line([(420, 412), (780, 412)], fill="#E7D9C2", width=2)
    _t = "Sanskrit · English · Nepali · Hindi"; _w = _ad.textlength(_t, font=_lat_f(26))
    _ad.text(((1200 - _w) / 2, 444), _t, font=_lat_f(26), fill=_SOFTL)
    _t = "chapain.github.io/Bhagavad-Gita"; _w = _ad.textlength(_t, font=_lat_f(24))
    _ad.text(((1200 - _w) / 2, 540), _t, font=_lat_f(24), fill=_SAFD)
    _a = _a.resize((960, 504), Image.LANCZOS)
    _a.save(os.path.join(_artdir, "share-art.jpg"), "JPEG", quality=80, optimize=True)
    print("share art: img/share-art.jpg painted (the one face for every preview)")


# sitemap.xml + robots.txt — the crawler-facing pair. URLs follow SITE_BASE.
# lastmod is the CONTENT-CHANGE date of each published page: today while the
# page is being rewritten in this working tree, otherwise the date of the last
# commit that touched it. Stamping every URL with the build date made the
# field a weak signal (a no-op rebuild moved all 19 dates) — Google ignores
# lastmod that is consistently inaccurate. Honest note: on a GitHub *project*
# page Google only reads github.io/robots.txt, so this robots.txt is advisory
# for Google (Search Console is the real channel); other crawlers do read it.
# The sitemap is what gets submitted in Search Console.
import datetime as _dt
import subprocess as _sp

def _lastmod(rel):
    try:
        _st = _sp.run(['git', 'status', '--porcelain', '--', rel],
                      cwd=ROOT, capture_output=True, text=True, timeout=10)
        if _st.stdout.strip():
            return _dt.date.today().isoformat()
        _lg = _sp.run(['git', 'log', '-1', '--format=%cs', '--', rel],
                      cwd=ROOT, capture_output=True, text=True, timeout=10)
        return _lg.stdout.strip() or _dt.date.today().isoformat()
    except Exception:
        return _dt.date.today().isoformat()

_urls = [f'  <url>\n    <loc>{SITE_BASE}/</loc>\n    <lastmod>{_lastmod("index.html")}</lastmod>\n    <priority>1.0</priority>\n  </url>']
for _ch in data:
    _rel = f'chapter/{_ch["num"]}/index.html'
    _urls.append(f'  <url>\n    <loc>{SITE_BASE}/chapter/{_ch["num"]}/</loc>\n    <lastmod>{_lastmod(_rel)}</lastmod>\n    <priority>0.8</priority>\n  </url>')
SITEMAP = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(_urls) + '\n'
           '</urlset>\n')
with open(os.path.join(SITE_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(SITEMAP)
ROBOTS = ('User-agent: *\n'
          'Allow: /\n'
          '\n'
          f'Sitemap: {SITE_BASE}/sitemap.xml\n')
with open(os.path.join(SITE_DIR, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(ROBOTS)

# ---------------- 404.html (owner 2026-09-01) ------------------------------
# GitHub Pages serves this for any unknown path. Without it a stale share link
# (an old v/N.NN/ that no longer exists, a mistyped chapter) is a dead end with
# no way back into the app. It recovers a #v=N.NN or #chapter=N fragment when
# the path carries one, so an out-of-date verse link still lands on its verse.
# noindex: this page must never enter the index. Self-contained — if the CSS or
# the app were also missing, the message still reads.
NOT_FOUND = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, follow">
<title>Page not found — Bhagavad Gita</title>
<link rel="icon" href="/Bhagavad-Gita/favicon.ico" sizes="any">
<style>
  :root{{ --paper:#FFF8EC; --ink:#2A2118; --ink-soft:#6B5D4F; --accent:#1A5648; --saffron:#B45A24; }}
  @media (prefers-color-scheme:dark){{
    :root{{ --paper:#1F1A14; --ink:#EDE3D0; --ink-soft:#B0A28C; --accent:#8FBEB0; --saffron:#DE8F52; }}
  }}
  body{{ margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
        background:var(--paper); color:var(--ink); text-align:center;
        font:17px/1.65 Georgia,serif; padding:24px; }}
  .om{{ font-size:3rem; color:var(--saffron); margin:0 0 6px; }}
  h1{{ font-size:1.4rem; color:var(--accent); margin:0 0 10px; }}
  p{{ color:var(--ink-soft); margin:0 0 22px; }}
  a.cta{{ display:inline-block; padding:13px 22px; background:var(--accent); color:#FFF8EC;
         border-radius:12px; text-decoration:none; font-weight:700; }}
</style>
</head>
<body>
<main>
  <p class="om" lang="sa">ॐ</p>
  <h1>This page has moved on</h1>
  <p>The verse you wanted is still here — the address just isn't.</p>
  <p><a class="cta" id="home" href="{SITE_BASE}/">Open the Bhagavad Gita →</a></p>
</main>
<script>
/* If the dead URL still names a verse or chapter, carry it into the app so the
   reader lands where they meant to go instead of on the welcome page. */
(function(){{
  var p = location.pathname, a = document.getElementById('home');
  /* An old share link: /v/2.47/. Those 700 pages were retired on 2026-09-01,
     but the links are out in the world forever — forward them to the verse's
     new home on its chapter page so nobody hits a dead end. */
  var m = p.match(/\\/v\\/(\\d+)\\.(\\d+)\\/?$/);
  if (m) {{
    a.href = '{SITE_BASE}/chapter/' + m[1] + '/#v' + m[1] + '.' + ('0' + m[2]).slice(-2);
    a.textContent = 'Read Bhagavad Gita ' + m[1] + '.' + parseInt(m[2], 10) + ' \u2192';
    location.replace(a.href);
    return;
  }}
  var c = p.match(/\\/chapter\\/(\\d+)\\/?$/);
  if (c) a.href = '{SITE_BASE}/#chapter=' + c[1];
}})();
</script>
</body>
</html>
"""
with open(os.path.join(SITE_DIR, "404.html"), "w", encoding="utf-8") as f:
    f.write(NOT_FOUND)
print("404.html: written (recovers #v= / #chapter= from dead links)")

# index.html + icons
dst = os.path.join(SITE_DIR, "index.html")
if os.path.abspath(dst) != os.path.abspath(path):
    shutil.copyfile(path, dst)
ICON_SRC = os.path.join(GITA_DIR, "icons")
copied = 0
if os.path.isdir(ICON_SRC):
    for n in ("icon-192.png", "icon-512.png",
              "icon-maskable-512.png", "apple-touch-icon.png", "og-card.png"):
        src = os.path.join(ICON_SRC, n)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(SITE_DIR, n)); copied += 1

# favicon.ico is GENERATED from icons/fav{16,32,48}.png — one ICO with three
# PNG frames. The old checked-in file carried only a 16×16 frame, so taskbar
# and bookmark views of the site were a blurry tiny glyph. PNG frames inside
# an ICO are supported everywhere that matters (Vista+, every current browser).
import struct as _struct
_fav = []
for _fn, _px in (("fav16.png", 16), ("fav32.png", 32), ("fav48.png", 48)):
    with open(os.path.join(ICON_SRC, _fn), "rb") as _f:
        _fav.append((_px, _f.read()))
_blob = _struct.pack("<HHH", 0, 1, len(_fav))
_off = 6 + 16 * len(_fav)
for _px, _png in _fav:
    _blob += _struct.pack("<BBBBHHII", _px, _px, 0, 0, 1, 32, len(_png), _off)
    _off += len(_png)
for _px, _png in _fav:
    _blob += _png
with open(os.path.join(SITE_DIR, "favicon.ico"), "wb") as _f:
    _f.write(_blob)
copied += 1
print(f"site/: index.html + manifest + sw.js (cache {CACHE_VER}) + sitemap + robots + {copied} icons  ->  {SITE_DIR}")
