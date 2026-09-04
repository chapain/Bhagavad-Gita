# -*- coding: utf-8 -*-
"""build_gita.py — builds the interactive Bhagavad Gita study app (text-only, 4-pāda format)."""
import json, os, re, sys, shutil, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gita_data import CHAPTERS, CH1_THEMES, CH1_TRANSLATIONS
from gita_data2 import CH2_THEMES, CH2_TRANSLATIONS
from gita_data3 import CH3_THEMES, CH3_TRANSLATIONS
from gita_data4 import CH4_THEMES, CH4_TRANSLATIONS
from gita_data5 import CH5_THEMES, CH5_TRANSLATIONS
from gita_data6 import CH6_THEMES, CH6_TRANSLATIONS
from gita_data7 import CH7_THEMES, CH7_TRANSLATIONS
from gita_data8 import CH8_THEMES, CH8_TRANSLATIONS
from gita_data9 import CH9_THEMES, CH9_TRANSLATIONS
from gita_data10 import CH10_THEMES, CH10_TRANSLATIONS
from gita_data11 import CH11_THEMES, CH11_TRANSLATIONS
from gita_data12 import CH12_THEMES, CH12_TRANSLATIONS
from gita_data13 import CH13_THEMES, CH13_TRANSLATIONS
from gita_data14 import CH14_THEMES, CH14_TRANSLATIONS
from gita_data15 import CH15_THEMES, CH15_TRANSLATIONS
from gita_data16 import CH16_THEMES, CH16_TRANSLATIONS
from gita_data17 import CH17_THEMES, CH17_TRANSLATIONS
from gita_data18 import CH18_THEMES, CH18_TRANSLATIONS
from padachheda_ch1 import GITA_CH1_WORDS
from padachheda_ch2 import GITA_CH2_WORDS
from padachheda_ch3 import GITA_CH3_WORDS
from padachheda_ch4 import GITA_CH4_WORDS
from padachheda_ch5 import GITA_CH5_WORDS
from padachheda_ch6 import GITA_CH6_WORDS
from padachheda_ch7 import GITA_CH7_WORDS
from padachheda_ch8 import GITA_CH8_WORDS
from padachheda_ch9 import GITA_CH9_WORDS
from padachheda_ch10 import GITA_CH10_WORDS
from padachheda_ch11 import GITA_CH11_WORDS
from padachheda_ch12 import GITA_CH12_WORDS
from padachheda_ch13 import GITA_CH13_WORDS
from padachheda_ch14 import GITA_CH14_WORDS
from padachheda_ch15 import GITA_CH15_WORDS
from padachheda_ch16 import GITA_CH16_WORDS
from padachheda_ch17 import GITA_CH17_WORDS
from padachheda_ch18 import GITA_CH18_WORDS
from i18n_ui import UI
from learn_block import LEARN_JS, LEARN_CSS
from i18n_chapters import CHAPTER_NAMES_NE, CHAPTER_NAMES_HI, CHAPTER_SUBS_NE, CHAPTER_SUBS_HI
from gloss_ne import GLOSS_NE
from gloss_hi import GLOSS_HI
from translations_ne import TRANS_NE
from translations_hi import TRANS_HI
from themes_ne import THEMES_NE
from themes_hi import THEMES_HI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GITA_DIR = ROOT  # the project folder itself — build publishes the app in place
os.makedirs(GITA_DIR, exist_ok=True)

# ---------------- the verse data ----------------
# Everything the app shows is read from the data files in this folder. Nothing
# is derived. verify.py holds two helpers used only to CHECK your data.
from verify import norm1, syll_iast

# The pāda (quarter) division of all 700 verses, as plain data.
PADAS = {}
for _n in range(1, 19):
    _m = __import__(f"padas_ch{_n}")
    PADAS.update(getattr(_m, f"GITA_CH{_n}_PADAS"))


def build_padas(ref):
    """Return a verse's flow — its speaker lines and pādas — read from padas_ch*.py."""
    rows = PADAS.get(ref)
    if not rows:
        raise SystemExit(f"padas_ch*.py: no entry for verse {ref}")
    flow = []
    for row in rows:
        if row[0] == "p":
            _, d, t, n = row
            flow.append({"k": "p", "d": d, "t": t, "n": n})
        else:
            _, d, t = row
            flow.append({"k": "s", "d": d, "t": t})
    return flow


def meter_of(flow):
    """Metre badge, from the frozen syllable counts."""
    pads = [x for x in flow if x["k"] == "p"]
    total = sum(x["n"] for x in pads)
    n = len(pads)
    if total == 32:
        return ("anuṣṭubh · 32 syllables · 4 pādas of 8",
                {"name": "anustubh", "irr": 0, "total": 32, "n": 4, "per": 8})
    if total == 44:
        return ("triṣṭubh · 44 syllables · 4 pādas of 11",
                {"name": "trishtubh", "irr": 0, "total": 44, "n": 4, "per": 11})
    if total == 22 and n == 2:
        return ("triṣṭubh · 22 syllables · 2 pādas of 11",
                {"name": "trishtubh", "irr": 0, "total": 22, "n": 2, "per": 11})
    if total == 33 and n == 4:
        return ("anuṣṭubh (irregular) · 33 syllables · 4 pādas",
                {"name": "anustubh", "irr": 1, "total": 33, "n": 4, "per": 0})
    return (f"{total} syllables · {n} pādas",
            {"name": "", "irr": 0, "total": total, "n": n, "per": 0})

# ---------------- load chapters ----------------
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
CH_SOURCES = [
    {"num": 1, "json": "ch1.json", "themes": CH1_THEMES, "trans": CH1_TRANSLATIONS, "words": GITA_CH1_WORDS},
    {"num": 2, "json": "ch2.json", "themes": CH2_THEMES, "trans": CH2_TRANSLATIONS, "words": GITA_CH2_WORDS},
    {"num": 3, "json": "ch3.json", "themes": CH3_THEMES, "trans": CH3_TRANSLATIONS, "words": GITA_CH3_WORDS},
    {"num": 4, "json": "ch4.json", "themes": CH4_THEMES, "trans": CH4_TRANSLATIONS, "words": GITA_CH4_WORDS},
    {"num": 5, "json": "ch5.json", "themes": CH5_THEMES, "trans": CH5_TRANSLATIONS, "words": GITA_CH5_WORDS},
    {"num": 6, "json": "ch6.json", "themes": CH6_THEMES, "trans": CH6_TRANSLATIONS, "words": GITA_CH6_WORDS},
    {"num": 7, "json": "ch7.json", "themes": CH7_THEMES, "trans": CH7_TRANSLATIONS, "words": GITA_CH7_WORDS},
    {"num": 8, "json": "ch8.json", "themes": CH8_THEMES, "trans": CH8_TRANSLATIONS, "words": GITA_CH8_WORDS},
    {"num": 9, "json": "ch9.json", "themes": CH9_THEMES, "trans": CH9_TRANSLATIONS, "words": GITA_CH9_WORDS},
    {"num": 10, "json": "ch10.json", "themes": CH10_THEMES, "trans": CH10_TRANSLATIONS, "words": GITA_CH10_WORDS},
    {"num": 11, "json": "ch11.json", "themes": CH11_THEMES, "trans": CH11_TRANSLATIONS, "words": GITA_CH11_WORDS},
    {"num": 12, "json": "ch12.json", "themes": CH12_THEMES, "trans": CH12_TRANSLATIONS, "words": GITA_CH12_WORDS},
    {"num": 13, "json": "ch13.json", "themes": CH13_THEMES, "trans": CH13_TRANSLATIONS, "words": GITA_CH13_WORDS},
    {"num": 14, "json": "ch14.json", "themes": CH14_THEMES, "trans": CH14_TRANSLATIONS, "words": GITA_CH14_WORDS},
    {"num": 15, "json": "ch15.json", "themes": CH15_THEMES, "trans": CH15_TRANSLATIONS, "words": GITA_CH15_WORDS},
    {"num": 16, "json": "ch16.json", "themes": CH16_THEMES, "trans": CH16_TRANSLATIONS, "words": GITA_CH16_WORDS},
    {"num": 17, "json": "ch17.json", "themes": CH17_THEMES, "trans": CH17_TRANSLATIONS, "words": GITA_CH17_WORDS},
    {"num": 18, "json": "ch18.json", "themes": CH18_THEMES, "trans": CH18_TRANSLATIONS, "words": GITA_CH18_WORDS},
]
chapter_data = {}
for cs in CH_SOURCES:
    j = json.load(open(os.path.join(BASE, cs["json"]), encoding="utf-8"))
    chapter_data[cs["num"]] = {"verses": j["verses"], **cs}

# ---------------- build data ----------------
# Nepali ergative for speaker subjects: "X said" is "X-ले भने", so speaker names
# in उवाच lines take the -ले ending in Nepali (धृतराष्ट्रले, सञ्जयले, अर्जुनले, श्रीभगवान्ले).
NE_SPEAKER = {
    "धृतराष्ट्र": "धृतराष्ट्रले",
    "सञ्जय": "सञ्जयले",
    "सञ्जयः": "सञ्जयले",
    "अर्जुन": "अर्जुनले",
    "अर्जुनः": "अर्जुनले",
    "श्रीभगवान्": "श्रीभगवान्ले",
}
def i18n_word(w):
    if len(w) >= 5: return w
    d, i, en = w[0], w[1], w[2]
    return [d, i, en, GLOSS_NE.get(i, en), GLOSS_HI.get(i, en)]

def i18n_words(wl):
    return [i18n_word(w) for w in wl]


def verse_lines(deva, iast):
    """Display lines for the running verse, taken verbatim from the source JSON.

    Every verse in source/ch*.json is written as segments separated by `।`:
    either two verse lines, or a speaker followed by two verse lines (and in
    1.21 / 1.28 the speaker sits *between* the two lines). We simply carry the
    segments through untouched, so what the app shows is exactly what the
    source says. Fix a verse by editing the JSON — nothing here re-derives it.

    The pāda division shown in the verse popup is separate data, read from
    padas_ch*.py; it does not affect these lines.
    """
    ds = [x.strip() for x in deva.split("।") if x.strip()]
    ts = [x.strip() for x in iast.split("।") if x.strip()]
    assert len(ds) == len(ts), f"deva/iast segment mismatch: {deva!r}"
    out = []
    for d, t in zip(ds, ts):
        spk = t.endswith("uvāca")
        out.append({"k": "s" if spk else "l", "d": d, "t": t})
    assert sum(1 for x in out if x["k"] == "l") == 2, f"expected 2 verse lines: {deva!r}"
    return out

def i18n_speaker_words(wl):
    # श्रीभगवान् (the Blessed Lord) takes the Nepali honorific verb: उवाच → भन्नुभयो
    honorific = any(w[0] == "श्रीभगवान्" for w in wl)
    out = []
    for w in wl:
        d, i, en = w[0], w[1], w[2]
        ne = NE_SPEAKER.get(d, w[3] if len(w) >= 5 else GLOSS_NE.get(i, en))
        if honorific and d == "उवाच":
            ne = "भन्नुभयो"
        hi = w[4] if len(w) >= 5 else GLOSS_HI.get(i, en)
        out.append([d, i, en, ne, hi])
    return out

data = []
for (num, name, deva, count, blurb) in CHAPTERS:
    ch = {"num": num, "name": name, "deva": deva, "sub": blurb, "verses": count, "themes": [],
          "names": {"en": name, "ne": CHAPTER_NAMES_NE.get(num, name), "hi": CHAPTER_NAMES_HI.get(num, name)},
          "subs": {"en": blurb, "ne": CHAPTER_SUBS_NE.get(num, blurb), "hi": CHAPTER_SUBS_HI.get(num, blurb)}}
    src = chapter_data.get(num)
    if src:
        verses = src["verses"]
        trans = src["trans"]
        words = src["words"]
        tne = THEMES_NE.get(num) or []
        thi = THEMES_HI.get(num) or []
        for ti, (t_title, t_desc, parts) in enumerate(src["themes"]):
            tp = []
            for pj, (p_title, p_desc, start, end) in enumerate(parts):
                s = int(start.split(".")[1]); e = int(end.split(".")[1])
                vs = []
                for n in range(s, e + 1):
                    key = str(n)
                    v = verses[key]
                    lit, para = trans[n]
                    trn = TRANS_NE.get(f"{num}.{n:02d}") or (lit, para)
                    trh = TRANS_HI.get(f"{num}.{n:02d}") or (lit, para)
                    ref = f"{num}.{n:02d}"
                    flow = build_padas(ref)
                    meter, mt = meter_of(flow)
                    pd = {"flow": flow, "padas": [x for x in flow if x["k"] == "p"],
                          "speakers": [x for x in flow if x["k"] == "s"],
                          "meter": meter, "mt": mt}
                    # attach per-pāda word splits (pada-chheda) from hand-built data
                    wd = words.get(n, {})
                    pidx = 0
                    for it in pd["flow"]:
                        if it["k"] == "p":
                            it["words"] = i18n_words(wd.get(pidx, []))
                            pidx += 1
                        elif it["k"] == "s":
                            it["words"] = i18n_speaker_words(wd.get("s", []))
                    vs.append({"n": f"{num}.{n:02d}", "d": v["deva"], "t": v["iast"],
                               "lines": verse_lines(v["deva"], v["iast"]),
                               "flow": pd["flow"], "padas": pd["padas"], "speakers": pd["speakers"],
                               "meter": pd["meter"], "mt": pd["mt"],
                               "lits": {"en": lit, "ne": trn[0], "hi": trh[0]},
                               "paras": {"en": para, "ne": trn[1], "hi": trh[1]}})
                ptn = (tne[ti][2][pj] if ti < len(tne) and pj < len(tne[ti][2]) else None)
                pth = (thi[ti][2][pj] if ti < len(thi) and pj < len(thi[ti][2]) else None)
                tp.append({"title": p_title, "desc": p_desc, "range": f"{start}–{end}", "sutras": vs,
                           "titles": {"en": p_title, "ne": (ptn[0] if ptn else p_title), "hi": (pth[0] if pth else p_title)},
                           "descs": {"en": p_desc, "ne": (ptn[1] if ptn else p_desc), "hi": (pth[1] if pth else p_desc)}})
            ttn = tne[ti] if ti < len(tne) else None
            tth = thi[ti] if ti < len(thi) else None
            ch["themes"].append({"title": t_title, "desc": t_desc, "parts": tp,
                                 "range": f"{parts[0][2]}–{parts[-1][3]}",
                                 "titles": {"en": t_title, "ne": (ttn[0] if ttn else t_title), "hi": (tth[0] if tth else t_title)},
                                 "descs": {"en": t_desc, "ne": (ttn[1] if ttn else t_desc), "hi": (tth[1] if tth else t_desc)}})
    data.append(ch)

total = sum(len(part["sutras"]) for t in data for th in t["themes"] for part in th["parts"]) if data else 0
print("verses embedded:", total)

# verify pāda structure
print("\n--- pāda verification ---")
for ch in data:
    if not ch["themes"]: continue
    for t in ch["themes"]:
        for p in t["parts"]:
            for v in p["sutras"]:
                pad = v["padas"]
                counts = [x["n"] for x in pad]
                print(f"{v['n']}: pādas={counts} ({v['meter']})" + ("  [SPK]" if v['speakers'] else ""))

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

# 1. the pādas must still spell the verse, and their syllable counts must
#    add up. This is what keeps padas_ch*.py honest against ch*.json: the two
#    files repeat the same text, so the build proves they still agree.
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
                        f"padas_ch*.py: the pādas of {v['n']} no longer spell the verse in "
                        f"ch{ch['num']}.json — if you edited one, edit the other too.\n"
                        f"      verse : {_sq(body)}\n"
                        f"      pādas : {joined}")
                for x in pads:
                    real = syll_iast(x["t"])
                    if real != x["n"]:
                        problems.append(
                            f"padas_ch*.py: {v['n']} pāda \"{x['t']}\" is marked {x['n']} "
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
                            f"padas_ch*.py: {v['n']} pāda {i+1} ends one letter short of its "
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
                            problems.append(f"padas_ch*.py: {v['n']} has a stray space at the "
                                            f"start or end of its {what}: {txt!r}")
                        elif "  " in txt:
                            problems.append(f"padas_ch*.py: {v['n']} has a double space in its "
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
                        f"padas_ch*.py: {v['n']} is {total} syllables, so each pāda should be "
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
                            f"padas_ch*.py: {v['n']} ends a pāda with an avagraha: {it['t']!r}. "
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

# 2. no translation may fall back to English
fb_ne = [v["n"] for ch in data for t in ch["themes"] for p in t["parts"] for v in p["sutras"]
         if not TRANS_NE.get(v["n"])]
fb_hi = [v["n"] for ch in data for t in ch["themes"] for p in t["parts"] for v in p["sutras"]
         if not TRANS_HI.get(v["n"])]
if fb_ne: problems.append(f"{len(fb_ne)} verses have no Nepali translation, so they "
                          f"would show English: {fb_ne[:5]} — add them to translations_ne.py")
if fb_hi: problems.append(f"{len(fb_hi)} verses have no Hindi translation, so they "
                          f"would show English: {fb_hi[:5]} — add them to translations_hi.py")

# 3. ne/hi theme files must mirror the English structure, or the builder pairs
#    them positionally and silently shows English
for ch in data:
    num = ch["num"]
    en_themes = ch["themes"]
    for lang, TH, fname in (("ne", THEMES_NE, "themes_ne.py"), ("hi", THEMES_HI, "themes_hi.py")):
        tl = TH.get(num) or []
        if len(tl) != len(en_themes):
            problems.append(f"{fname}: chapter {num} has {len(tl)} themes but English "
                            f"has {len(en_themes)} — they must match one-for-one")
            continue
        for ti, th in enumerate(en_themes):
            if len(tl[ti][2]) != len(th["parts"]):
                problems.append(f"{fname}: chapter {num} theme {ti+1} has {len(tl[ti][2])} "
                                f"parts but English has {len(th['parts'])}")

# 4. every verse must sit in exactly one part (a bad range in gita_data*.py
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
    if dupes:   problems.append(f"chapter {ch['num']}: verses appear in more than one part: {dupes[:5]} — check the ranges in gita_data{ch['num']}.py")
    if missing: problems.append(f"chapter {ch['num']}: verses in ch{ch['num']}.json are in no part, so they are unreachable: {missing[:5]} — check the ranges in gita_data{ch['num']}.py")

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

# ---------------- HTML template (4-pāda display) ----------------
HTML = r"""<!DOCTYPE html>
<!--
  Bhagavad Gita — an Interactive Study
  GENERATED FILE — do not edit by hand.

  This file is built from the sources in  source/  by:
      bash rebuild.sh          (runs source/build_gita.py, then both test suites)

  Edit the data, not this file:
      source/gita_data*.py     verse text, themes and parts (English)
      source/themes_ne.py      Nepali theme/part titles
      source/themes_hi.py      Hindi theme/part titles
      source/gloss_ne.py       Nepali word-meanings
      source/gloss_hi.py       Hindi word-meanings
      source/padachheda_ch*.py per-pada word splits
      source/i18n_ui.py        interface strings (en/ne/hi)

  Created by Dhruba Chapain, Pokhara, Nepal.  All rights reserved.
  AI tools were used in making this app, under the author's direction; the
  content was reviewed, corrected and approved by him.  See LICENSE.md.
  https://github.com/chapain/Bhagavad-Gita
-->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#1A5648" id="themeColor">
<script>
/* Runs before the page paints, so a dark-mode user never sees a white flash.
   Order of preference: a choice they made here, else the phone's own setting.
   localStorage is wrapped because some in-app browsers (WhatsApp, Facebook)
   throw on access — the app must still work there, just without remembering. */
(function(){
  var saved = null;
  try{ saved = localStorage.getItem('gitaTheme'); }catch(e){}
  var sysDark = false;
  try{ sysDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches; }catch(e){}
  var dark = (saved === 'dark') || (saved === null && sysDark);
  if(dark) document.documentElement.setAttribute('data-theme','dark');
})();
</script>
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Gita">
<meta name="format-detection" content="telephone=no">
<meta name="author" content="Dhruba Chapain">
<meta name="description" content="Bhagavad Gita — interactive trilingual study edition (English · नेपाली · हिन्दी), 18 chapters, 700 verses, offline.">

<!-- Link preview (WhatsApp, Messenger, Facebook, Telegram, X…).
     Absolute URLs are required: chat apps fetch these from their own servers.
     Harmless when the file is opened locally — the tags are simply ignored. -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bhagavad Gita — an Interactive Study">
<meta property="og:title" content="Bhagavad Gita — an Interactive Study · 700 verses, trilingual">
<meta property="og:description" content="All 18 chapters in English · नेपाली · हिन्दी, with word-by-word meanings for every verse. Works offline.">
<meta property="og:url" content="__BASE__/">
<!-- EXACTLY ONE og:image and ONE twitter:card. Both were once declared twice
     with conflicting values (icon-512.png + summary, then og-card.png +
     summary_large_image). Crawlers take the FIRST og:image, so the homepage
     previewed with the square app icon while the 1200×630 width/height tags
     described the second image — the mismatch made some crawlers drop the
     card entirely. og-card.png is the site's one face; the square icon is for
     the manifest, never for a link preview. -->
<meta property="og:image" content="__BASE__/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ॐ श्रीमद्भगवद्गीता — Bhagavad Gita, 700 verses">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="ne_NP">
<meta property="og:locale:alternate" content="hi_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Bhagavad Gita — an Interactive Study · 700 verses, trilingual">
<meta name="twitter:description" content="All 18 chapters in English · नेपाली · हिन्दी, with word-by-word meanings. Works offline.">
<meta name="twitter:image" content="__BASE__/og-card.png">

<!-- Search engines. The canonical URL tells Google this is the one address of
     the app; the JSON-LD describes what it is in a form no crawler can get
     wrong by mis-rendering the page. Absolute URLs via __BASE__, like og:url.
     The GSC placeholder is replaced with the Search Console verification meta
     tag when source/gsc_token.txt exists; otherwise it is removed. -->
<!--GSC-->
<link rel="canonical" href="__BASE__/">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Bhagavad Gita — an Interactive Study",
  "alternateName": "श्रीमद्भगवद्गीता",
  "url": "__BASE__/",
  "description": "Read and study all 18 chapters and 700 verses of the Bhagavad Gita in English, Nepali and Hindi, with word-by-word meanings, the four pādas of every verse, themes, search and favourites. Works offline.",
  "applicationCategory": "EducationalApplication",
  "operatingSystem": "Any web browser",
  "browserRequirements": "Requires JavaScript",
  "inLanguage": ["en", "ne", "hi"],
  "isAccessibleForFree": true,
  "author": {
    "@type": "Person",
    "name": "Dhruba Chapain",
    "address": {"@type": "PostalAddress", "addressLocality": "Pokhara", "addressCountry": "NP"}
  },
  "sameAs": "https://github.com/chapain/Bhagavad-Gita"
}
</script>

<!-- Icons: relative paths, so they resolve on any host or sub-path. -->
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<title>Bhagavad Gita — English, Nepali, Hindi · 700 Verses</title>
<style>
__FONTS__
  /* ---- colour tokens -------------------------------------------------
     Light is the default. The dark theme below overrides these same names,
     so every rule keeps using var(--x) and nothing else has to change.
     --on-accent is the text colour that sits on saffron/teal fills; it stays
     near-cream in both themes because both fills stay dark enough for it.  */
  :root{ --saffron:#E8912C; --saffron-dark:#C97A20; --saffron-soft:#FBE3C0; --teal:#1A5648; --teal-mid:#2A7A68;
         --teal-soft:#E6EFE8; --cream:#FFF8EC; --ink:#2A2118; --ink-soft:#5C5142; --paper:#FFFFFF; --line:#E7D9C2;
         --on-accent:#FFF8EC; --on-saffron:#2A2118; --hdr-a:#1A5648; --hdr-b:#226B5A; --hdr-c:#2A806C; --hdr-sub:#C5DDD4;
         --toolbar:#FDF3E0; --field:#FFFFFF; --muted:#9AA0A6; --danger:#C0392B; --danger-soft:#FBE6E3; --on-danger:#FFFFFF;
         --shadow:42,33,24; --scrim:rgba(15,42,52,.72); --fade:255,248,236;
         --chip:rgba(255,248,236,.12); --chip-hover:rgba(255,248,236,.25); --chip-line:rgba(255,248,236,.35); }

  /* ---- dark theme ----------------------------------------------------
     Warm, not neutral: a dark brown-black keeps the manuscript feel rather
     than looking like a generic app. Never pure black and never pure white —
     Devanagari has fine strokes, and maximum contrast makes them shimmer.
     Saffron and teal are both lifted, because the light-mode values go muddy
     against a dark ground.                                                */
  html{ color-scheme: light; }
  html[data-theme="dark"]{
    color-scheme: dark;
    /* Apple-dark discipline: accents muted a notch, text never glaring.
       The old #E8912C/#7FD4E8 pair neon'd against the warm black. */
    --saffron:#E1953A; --saffron-dark:#C8862F; --saffron-soft:#43301A;
    --teal:#8FBEB0; --teal-mid:#A8D0C4; --teal-soft:#1A2E28;
    --cream:#16120D; --paper:#201A13; --ink:#E9DCC3; --ink-soft:#A79A80; --line:#382D20;
    --on-accent:#1A1209; --on-saffron:#1A1209; --hdr-a:#0E2A24; --hdr-b:#143832; --hdr-c:#1A4840; --hdr-sub:#C5DDD4;
    --toolbar:#1E1811; --field:#2A2219; --muted:#8A7F6E; --danger:#E86B5C; --danger-soft:#3A211C; --on-danger:#1A1209;
    --shadow:0,0,0; --scrim:rgba(0,0,0,.78); --fade:23,19,14;
    --chip:rgba(242,231,213,.10); --chip-hover:rgba(242,231,213,.20); --chip-line:rgba(242,231,213,.28);
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  body{ font-family:"Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif; color:var(--ink);
        line-height:1.55; display:flex; flex-direction:column; min-height:100vh;}
  /* Quiet devotion (owner 2026-09-04): sandalwood on the paper, a peacock
     feather as a watermark. Opacity is the whole design — if you notice it
     first, it is too loud. pointer-events:none so it never steals a tap. */
  body{ background:
        radial-gradient(900px 420px at 50% -60px, rgba(232,145,44,.07), transparent 62%),
        var(--cream); }
  html[data-theme="dark"] body{ background:
        radial-gradient(900px 420px at 50% -60px, rgba(225,149,58,.08), transparent 62%),
        var(--cream); }
  .atm{ position:fixed; inset:0; pointer-events:none; z-index:0; overflow:hidden; }
  header, .toolbar, .wrap, footer{ position:relative; z-index:1; }
  .atm-wisp{ position:absolute; bottom:-12%; width:260px; height:72%;
             left:50%; margin-left:-130px;
             background:radial-gradient(ellipse at 50% 88%, rgba(196,154,108,.22), transparent 68%);
             filter:blur(32px); opacity:.5;
             animation:atmRise 32s ease-in-out infinite; }
  .atm-wisp.b{ left:36%; margin-left:-110px; width:220px; opacity:.32; animation-delay:-11s; }
  .atm-wisp.c{ left:64%; margin-left:-100px; width:200px; opacity:.28; animation-delay:-19s; }
  @keyframes atmRise{
    0%,100%{ transform:translateY(0) scaleX(1); }
    50%{ transform:translateY(-6%) scaleX(1.06); }
  }
  .atm-feather{ position:absolute; right:max(8px, env(safe-area-inset-right,0px));
                top:28%; width:86px; height:210px; opacity:.12; color:var(--teal); }
  html[data-theme="dark"] .atm-wisp{ opacity:.18; }
  html[data-theme="dark"] .atm-feather{ opacity:.14; color:var(--saffron); }
  @media (max-width:640px){ .atm-feather{ width:64px; height:156px; opacity:.09; } }


  header{ background:var(--hdr-a); color:var(--hdr-sub);
          padding:24px 20px; }
  .header-inner{ max-width:1180px; margin:0 auto; display:flex; align-items:center; gap:16px; flex-wrap:wrap;}
  .header-inner .om{ font-family:Georgia,serif; font-size:1.7rem; color:var(--saffron);}
  .header-inner h1{ font-family:Georgia,serif; font-size:1.4rem;}
  .header-inner .tag{ color:var(--hdr-sub); font-size:.9rem; margin-left:auto; text-align:right;}
  .langbar{ display:flex; gap:8px; margin-left:auto; align-items:center;}
  /* iOS-style segmented control: one translucent track, the active language
     raised as a neutral segment — chrome stays quiet, no orange in the header */
  /* Language bar: the owner's iOS-segment look, restored 2026-08-30 after the
     chip experiment ("revert to previous looks") — but the hover keeps the
     warming the chip pass taught it: saffron-dark fill, lamp-black letter. */
  .seg{ display:flex; gap:2px; background:var(--chip); border:1px solid var(--chip-line); border-radius:999px; padding:3px; }
  .seg .lang-btn{ background:transparent; border:none; color:var(--hdr-sub); padding:6px 14px; border-radius:999px; cursor:pointer; font-size:.85rem; font-weight:600; transition:background-color .15s, color .15s; }
  .seg .lang-btn:hover{ background:var(--saffron-dark); color:var(--on-saffron); }
  .seg .lang-btn.on{ background:var(--paper); color:var(--ink); font-weight:700; box-shadow:0 1px 3px rgba(0,0,0,.28); }
  .lang-btn{ background:var(--chip); color:var(--hdr-sub); border:1px solid var(--chip-line); padding:6px 14px; border-radius:999px; cursor:pointer; font-size:.85rem; font-weight:600; transition:background-color .15s, color .15s;}
  .lang-btn:hover{ background:var(--saffron-dark); color:var(--on-saffron);}
  /* the theme toggle lives in the language bar; it must not stretch like the
     language buttons do on mobile, so it opts out of flex:1 and stays square */
  .theme-btn{ flex:0 0 auto !important; min-width:40px; padding:6px 12px; font-size:1.05rem; line-height:1; color:var(--saffron); border-color:var(--chip-line);}
  /* Owner 2026-09-01: the theme toggle must hover exactly like the language
     buttons. It used to get a faint --chip-hover wash and keep its saffron
     text colour, so the icon sat saffron-on-saffron and the button felt dead
     next to its neighbours. Inheriting .lang-btn:hover gives it the same
     --saffron-dark fill; --on-saffron drives the icon too, because .ic is
     stroke:currentColor. Only the resting colour stays saffron. */
  .theme-btn:hover{ background:var(--saffron-dark); color:var(--on-saffron);}
  @media (max-width:640px){ .langbar{ width:100%; justify-content:center; margin-left:0;} .seg{ flex:1; } .seg .lang-btn{ flex:1; text-align:center;} }
  .header-inner .tag b{ color:var(--saffron); font-family:Georgia,serif; font-size:1.15rem;}
  .wrap{ max-width:1180px; margin:0 auto; padding:22px 20px 60px; width:100%; flex:1;}
  .crumbs{ display:flex; align-items:center; gap:8px; font-size:.9rem; color:var(--ink-soft); margin-bottom:18px; flex-wrap:wrap;}
  /* Search/Favorites show one .back-top button (see renderCrumbs), so .crumbs is
     just its wrapper. Long chapter names ellipsise rather than wrap. */
  .crumbs .back-top{ margin:0 0 4px; max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
  /* Visually hidden but readable by assistive tech — used by #srStatus. */
  .sr-only{ position:absolute; width:1px; height:1px; padding:0; margin:-1px;
            overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0; }
  .view-title{ font-family:Georgia,serif; font-size:1.7rem; color:var(--ink); margin-bottom:6px;}
  .view-sub{ color:var(--ink-soft); font-size:.98rem; margin-bottom:22px; max-width:880px;}
  .grid{ display:grid; gap:20px; }
  .grid.chapters{ grid-template-columns:repeat(auto-fill, minmax(250px,1fr)); }
  .grid.themes{ grid-template-columns:repeat(auto-fill, minmax(260px,1fr)); }
  .grid.verses{ grid-template-columns:repeat(auto-fill, minmax(300px,1fr)); gap:14px; }
  .card{ background:var(--paper); border:1px solid var(--line); border-radius:16px; padding:16px 18px;
         box-shadow:0 1px 2px rgba(var(--shadow),.05); cursor:pointer; transition:.18s; display:flex; flex-direction:column;}
  .card:hover{ border-color:var(--saffron); box-shadow:0 4px 14px rgba(var(--shadow),.10);}
  /* ---- the house idiom (owner 2026-09-02: "every page must represent our
     colours"). Until now every surface in the app was a --paper box with a grey
     outline: the saffron and teal accents inside had nothing to belong to.
     A 2px brand hairline on the leading side of a card costs nothing, reads in
     both themes, and ties a screen together without shouting over the
     scripture. 2px, not 3: at 3 it reads as a highlighter stripe and the page
     starts to look like a dashboard (owner 2026-09-02: "not gaudy, Apple
     style"). The restraint is the point.
     Saffron = something you act on. Teal = something already yours. */
  .edge-s{ border-left:2px solid var(--saffron); }
  .edge-t{ border-left:2px solid var(--teal); }
  .card{ border-left:2px solid var(--saffron); }
  .card:hover{ border-left-color:var(--saffron-dark); }
  .theme{ border-left:2px solid var(--saffron); }
  .theme:hover{ border-left-color:var(--saffron-dark); }
  .res-card{ border-left:2px solid var(--teal); }
  .res-card:hover{ border-left-color:var(--teal); }
  .mode-box{ border-left:2px solid var(--saffron); }
  .welcome .w-day{ border-left:2px solid var(--saffron); }
  .card .chip{ align-self:flex-start; background:var(--saffron-soft); color:var(--saffron-dark); font-weight:700; font-size:.72rem;
               letter-spacing:.1em; text-transform:uppercase; padding:4px 10px; border-radius:999px; margin-bottom:8px;}
  .card .chip.locked{ background:var(--muted);}
  /* The three ways of receiving a chapter live ON the chapter page as an
     iOS-style segmented control — the same grammar as the language pills in
     the header (owner 2026-08-30: the intermediary choice page "was just
     making things weirder"). One quiet line above says Choose; the raised
     segment says where you are. Content-area variant of .seg: paper track,
     hairline border, teal raise — no orange, chrome stays quiet. */
  /* The instruction and the control live in one hairline tray (owner
     2026-08-30: "put the choose and the three options in a box, and make it
     instructive"). Same body as every card — paper, hairline, 16px radius —
     so the chrome reads as one quiet object set apart from the scripture. */
  .mode-box{ background:var(--paper); border:1px solid var(--line); border-radius:16px;
             padding:14px 18px; margin:0 0 18px; display:flex; flex-direction:column;
             gap:10px; align-items:flex-start; box-shadow:0 1px 2px rgba(var(--shadow),.05); }
  /* Owner 2026-09-01: this caption used to be --saffron-dark, the exact colour
     of the pills underneath it, so a non-interactive question looked clickable
     — and on white it measured 3.34:1, under the 4.5:1 AA floor. --ink-soft
     reads as a quiet caption and passes AA in both themes (7.75:1 / 6.22:1),
     leaving saffron to mean "you can press this". */
  .mode-lbl{ font-size:.9rem; color:var(--ink-soft); font-weight:600; }

  /* ---------- Play ---------- */
  /* The scope row is the same segmented-pill grammar as the chapter chooser:
     soft pill = an option, gold pill = where you are (PROJECT.md, mode-box). */
  .pl-scope{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin:4px 0 22px;}
  .pl-scope .pl-lb{ font-family:system-ui,sans-serif; font-size:.74rem; letter-spacing:.14em;
                    text-transform:uppercase; color:var(--ink-soft);}
  .pl-scope .lr-ghost.on{ background:var(--saffron); border-color:var(--saffron);
                          color:var(--on-saffron);}
  /* matches .tool-btn geometry so the select sits level with the pills */
  .pl-sel{ padding:8px 16px; border-radius:999px; border:1px solid var(--line);
           background:var(--paper); color:var(--teal); font-family:inherit;
           font-weight:700; font-size:.85rem; max-width:100%; cursor:pointer;
           transition:.15s;}
  .pl-sel:hover{ border-color:var(--saffron);}
  .pl-modes{ display:grid; gap:11px; grid-template-columns:repeat(auto-fit,minmax(240px,1fr));}
  /* same shape as .card: --paper, 16px radius, 1px shadow, saffron on hover */
  .pl-mode{ display:flex; gap:13px; align-items:flex-start; text-align:left; padding:16px 18px;
            border-radius:16px; background:var(--paper); border:1px solid var(--line);
            border-left:2px solid var(--saffron);
            box-shadow:0 1px 2px rgba(var(--shadow),.05); cursor:pointer;
            font-family:inherit; transition:.18s;}
  .pl-mode:hover{ border-color:var(--saffron); border-left-color:var(--saffron-dark);
                  box-shadow:0 4px 14px rgba(var(--shadow),.10); transform:translateY(-2px);}
  .pl-mode .n{ flex:0 0 30px; height:30px; border-radius:50%; display:grid; place-items:center;
               background:var(--saffron-soft); color:var(--saffron-dark);
               font-family:system-ui,sans-serif; font-weight:700; font-size:.85rem;}
  .pl-mode .b{ flex:1; min-width:0;}
  .pl-mode .b b{ display:block; font-size:1.06rem; font-weight:700; color:var(--ink);
                 margin-bottom:4px;}
  .pl-mode .b span{ display:block; color:var(--ink-soft); font-size:.86rem; line-height:1.5;}
  @media (max-width:640px){ .pl-modes{ grid-template-columns:1fr;} .pl-sel{ flex:1 0 100%;} }

  /* ---------- Learn by heart ---------- */
  .lrn{ max-width:760px; }
  .lr-k{ font-family:system-ui,sans-serif; font-size:.68rem; letter-spacing:.2em;
         text-transform:uppercase; color:var(--ink-soft); margin-bottom:4px;}
  /* Owner 2026-09-01: the drill must not look like a different app. These
     mirror .tool-btn / .tool-btn.primary exactly — same padding, weight, size
     and hover — so a button here behaves like a button anywhere else. */
  .lr-cta{ background:var(--saffron); border:1px solid var(--saffron);
           color:var(--on-saffron); font-weight:700; font-size:.85rem;
           padding:8px 16px; border-radius:999px; cursor:pointer;
           font-family:inherit; transition:.15s;}
  .lr-cta:hover{ background:var(--saffron-dark); border-color:var(--saffron-dark);}
  .lr-ghost{ background:var(--paper); border:1px solid var(--line); color:var(--teal);
             font-weight:700; font-size:.85rem; padding:8px 16px; border-radius:999px;
             cursor:pointer; font-family:inherit; transition:.15s;}
  .lr-ghost:hover:not(:disabled){ border-color:var(--saffron); background:var(--saffron-soft);}
  .lr-ghost:disabled{ opacity:.35; cursor:default;}
  .lr-ghost.sm{ font-size:.76rem; padding:7px 13px;}

  .lr-prog{ height:5px; border-radius:3px; background:var(--line); overflow:hidden; margin-top:8px;}
  .lr-prog i{ display:block; height:100%; background:var(--saffron); border-radius:3px;
              transition:width .45s cubic-bezier(.2,.8,.2,1);}
  .lr-progl{ font-family:system-ui,sans-serif; font-size:.74rem; color:var(--ink-soft); margin:7px 0 18px;}

  /* matches .card: --paper, 16px radius, the same 1px shadow */
  .lr-step{ display:flex; gap:14px; padding:16px 18px; border-radius:16px; margin-bottom:13px;
            background:var(--paper); border:1px solid var(--line);
            border-left:2px solid var(--saffron);
            box-shadow:0 1px 2px rgba(var(--shadow),.05); transition:.18s;}
  /* the step you are on wears the full saffron edge; a finished one turns teal */
  .lr-step.now{ border-color:var(--saffron); border-left-color:var(--saffron-dark);}
  .lr-step.done{ border-left-color:var(--teal);}
  .lr-step.locked{ opacity:.55;}
  .lr-badge{ flex:0 0 30px; height:30px; border-radius:50%; display:grid; place-items:center;
             background:var(--saffron-soft); color:var(--saffron-dark);
             font-family:system-ui,sans-serif; font-weight:700; font-size:.84rem;}
  .lr-step.now .lr-badge{ background:var(--saffron); color:var(--on-saffron);}
  .lr-step.done .lr-badge{ background:var(--teal); color:var(--on-accent);}
  .lr-body{ flex:1; min-width:0;}
  .lr-body h3{ margin:1px 0 5px; font-size:1.06rem; font-weight:700; color:var(--ink);}
  .lr-body p{ margin:0 0 11px; color:var(--ink-soft); font-size:.88rem; line-height:1.55;}

  .lr-grid{ display:grid; gap:8px; grid-template-columns:repeat(auto-fill,minmax(196px,1fr));}
  .lr-chip{ display:flex; align-items:center; gap:9px; text-align:left; padding:10px 12px;
            border-radius:12px; background:var(--paper); border:1px solid var(--line);
            border-left:2px solid var(--saffron);
            cursor:pointer; font-family:inherit; transition:.15s;}
  .lr-chip:hover{ border-color:var(--saffron); box-shadow:0 4px 14px rgba(var(--shadow),.10);}
  .lr-chip.ok{ border-color:var(--teal); border-left-color:var(--teal); background:var(--teal-soft);}
  .lr-chip .n{ flex:0 0 22px; height:22px; border-radius:50%; display:grid; place-items:center;
               background:var(--saffron-soft); font-size:.7rem; font-family:system-ui,sans-serif;
               color:var(--saffron-dark);}
  .lr-chip.ok .n{ background:var(--teal); color:var(--on-accent); font-weight:700;}
  .lr-chip .t{ flex:1; font-size:.85rem; line-height:1.3;}
  .lr-chip .v{ font-family:system-ui,sans-serif; font-size:.7rem; color:var(--ink-soft);}

  .lr-foot{ display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-top:16px;
            font-family:system-ui,sans-serif; font-size:.74rem; color:var(--ink-soft);}

  .lr-thread{ list-style:none; margin:16px 0 0; padding:0;}
  .lr-thread li{ display:flex; gap:13px; padding:12px 13px; border-radius:13px; position:relative;}
  .lr-thread li:not(:last-child):after{ content:''; position:absolute; left:28px; top:42px;
            bottom:-2px; width:2px; background:var(--line);}
  .lr-thread .bead{ flex:0 0 26px; height:26px; border-radius:50%; display:grid; place-items:center;
            background:var(--saffron-soft); color:var(--saffron-dark); z-index:1;
            font-family:system-ui,sans-serif; font-size:.75rem; font-weight:700;}
  .lr-thread b{ font-weight:700; font-size:1rem; color:var(--ink);}
  .lr-thread .rg{ font-family:system-ui,sans-serif; font-size:.7rem; color:var(--saffron-dark); font-weight:600; margin-left:7px;}
  .lr-thread p{ margin:4px 0 0; color:var(--ink-soft); font-size:.86rem; line-height:1.5;}

  .lr-vnum{ font-family:system-ui,sans-serif; font-size:1.3rem; font-weight:700;
            color:var(--saffron-dark); margin:10px 0 12px;}
  .lr-quarters{ display:flex; flex-direction:column; gap:9px;}
  .lr-q{ border-radius:16px; background:var(--paper); border:1px solid var(--line);
         border-left:2px solid var(--saffron);
         box-shadow:0 1px 2px rgba(var(--shadow),.05); overflow:hidden; transition:.18s;}
  .lr-q.open{ border-color:var(--saffron); border-left-color:var(--saffron-dark);}
  .lr-qh{ display:flex; gap:12px; align-items:center; width:100%; text-align:left;
          padding:14px 16px; background:none; border:none; cursor:pointer; font-family:inherit;}
  .lr-qh .pip{ flex:0 0 25px; height:25px; border-radius:50%; display:grid; place-items:center;
          background:var(--saffron-soft); color:var(--saffron-dark);
          font-family:system-ui,sans-serif; font-size:.73rem; font-weight:700;}
  .lr-q.open .pip{ background:var(--saffron); color:var(--on-saffron);}
  .lr-qh .tx{ flex:1; min-width:0;}
  .lr-qh .dv{ display:block; font-family:"Noto Serif Devanagari",Georgia,serif;
              font-size:1.12rem; line-height:1.7;}
  .lr-qh .ia{ display:block; font-size:.78rem; font-style:italic; color:var(--ink-soft); margin-top:2px;}
  .lr-qh .chev{ color:var(--ink-soft); transition:transform .22s;}
  .lr-q.open .chev{ transform:rotate(180deg); color:var(--saffron);}
  /* [hidden] is only display:none at the UA default, so ANY explicit display
     silently defeats it — the word grid was open on arrival despite carrying
     the attribute (owner 2026-09-02). Restore it explicitly. */
  .lr-words[hidden]{ display:none; }
  .lr-words{ display:grid; gap:8px; padding:2px 16px 16px;
             grid-template-columns:repeat(auto-fill,minmax(148px,1fr));}
  .lr-word{ padding:9px 11px; border-radius:10px; background:var(--paper);
            border:1px solid var(--line); border-left:2px solid var(--saffron);}
  .lr-word .d{ display:block; font-family:"Noto Serif Devanagari",Georgia,serif;
               font-size:1rem; color:var(--saffron-dark);}
  .lr-word .i{ display:block; font-size:.71rem; font-style:italic; color:var(--ink-soft); margin:1px 0 3px;}
  .lr-word .m{ display:block; font-size:.84rem; line-height:1.4;}
  .lr-mean{ margin-top:14px; padding:14px 16px; border-radius:14px;
            background:var(--saffron-soft); border:1px solid var(--line);}
  .lr-mean .lb{ display:block; font-family:system-ui,sans-serif; font-size:.65rem;
                letter-spacing:.18em; text-transform:uppercase; color:var(--saffron-dark); margin-bottom:5px;}

  .lr-nav{ display:flex; align-items:center; gap:11px; flex-wrap:wrap; margin-top:20px;}
  .lr-hint{ flex:1; text-align:center; font-family:system-ui,sans-serif;
            font-size:.76rem; color:var(--ink-soft);}

  /* The question card sits on --cream so the --paper options READ as raised
     cards on top of it. Both were --paper, so every boundary vanished and the
     screen went flat white (owner 2026-09-01). */
  .lr-qbox{ padding:18px; border-radius:16px; background:var(--cream);
            border:1px solid var(--line); border-left:2px solid var(--saffron);
            box-shadow:0 1px 2px rgba(var(--shadow),.05);}
  /* the question is the loudest thing on the screen, and saffron-soft under a
     saffron rule marks it as the prompt rather than more prose */
  .lr-ask{ font-size:1.06rem; line-height:1.6; margin:-2px -4px 16px; padding:12px 14px;
           border-radius:12px; background:var(--saffron-soft);
           border-left:2px solid var(--saffron); color:var(--ink);}
  .pl-head{ margin:6px 0 14px !important; color:var(--saffron-dark) !important;
            font-weight:700; letter-spacing:.1em; text-transform:uppercase;}
  .lr-qsub{ margin-top:10px; padding:12px 14px; border-radius:11px; background:var(--paper);
            border:1px solid var(--line); color:var(--ink-soft); font-size:.92rem; line-height:1.6;}
  .lr-qsub.dv{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.1rem; color:var(--ink);}
  .lr-split{ margin-top:11px; padding:14px; border-radius:11px; background:var(--paper);
             border:1px solid var(--line); display:flex; flex-wrap:wrap; gap:7px;
             align-items:center; justify-content:center;}
  .lr-tok{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.1rem;}
  .lr-plus{ color:var(--ink-soft); font-size:.8rem;}
  .lr-blank{ display:inline-grid; place-items:center; min-width:52px; padding:2px 12px;
             border-radius:8px; background:var(--saffron-soft); color:var(--saffron-dark);
             border:2px dashed var(--saffron); font-weight:700; font-size:1.1rem;}
  .lr-cue{ margin-top:8px; text-align:center; font-family:"Noto Serif Devanagari",Georgia,serif;
           font-size:.95rem; color:var(--ink-soft);}
  .lr-opts{ display:grid; gap:9px;}
  /* Options are whole ślokas now (66-134 characters), so they stack: the verse
     takes the full width and its number sits underneath, instead of the two
     competing for one line (owner 2026-09-01). */
  /* --paper on --cream is only a 1.06:1 step, so the SHADOW does the lifting,
     not the fill: without it the options dissolve into the question card. */
  .lr-opt{ display:flex; flex-direction:column; align-items:flex-start; gap:4px;
           text-align:left; width:100%;
           padding:13px 15px; border-radius:12px; background:var(--paper);
           border:1px solid var(--line); border-left:2px solid var(--saffron);
           cursor:pointer; font-family:inherit;
           box-shadow:0 1px 3px rgba(var(--shadow),.10); transition:.15s;}
  .lr-opt:hover:not(:disabled){ border-color:var(--saffron); background:var(--saffron-soft);}
  .lr-opt:disabled{ cursor:default;}
  .lr-opt .ol{ width:100%; font-size:.96rem; line-height:1.5; color:var(--ink);}
  .lr-opt .ol.dv{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.04rem;
                  line-height:1.85;}
  /* the verse number under an option is a NUMBER — saffron, like every other
     verse number in the app */
  .lr-opt .os{ font-family:system-ui,sans-serif; font-size:.74rem; font-weight:700;
               color:var(--saffron-dark);}
  /* the verdict must be unmistakable at a glance, not a 1px border change */
  /* The verdict is carried by the OPTION, not by a line of prose underneath
     (owner 2026-09-02). A tick and a cross in the leading edge, plus the fill,
     say it faster than any wording — and in every language at once. */
  .lr-opt.right, .lr-opt.wrong{ position:relative; padding-right:44px;}
  .lr-opt.right::after, .lr-opt.wrong::after{
      position:absolute; right:13px; top:50%; transform:translateY(-50%);
      width:22px; height:22px; border-radius:50%; display:grid; place-items:center;
      font-family:system-ui,sans-serif; font-size:.82rem; font-weight:700;
      line-height:1;}
  .lr-opt.right{ border-color:var(--teal); border-left-color:var(--teal);
                 border-width:2px; background:var(--teal-soft);
                 box-shadow:0 2px 10px rgba(var(--shadow),.14);}
  .lr-opt.right::after{ content:"\2713"; background:var(--teal); color:var(--on-accent);}
  /* the chosen wrong answer must read as wrong at a glance: red fill, red edge,
     a cross. No dimming — opacity made the mistake harder to study, which is
     backwards, since the mistake is the thing worth looking at. */
  .lr-opt.wrong{ border-color:var(--danger); border-left-color:var(--danger);
                 border-width:2px; background:var(--danger-soft); box-shadow:none;}
  /* --on-danger, not #FFF: the dark theme's red is light (#E86B5C), where white
     measures only 3.14:1. Each palette supplies the ink its own red needs. */
  .lr-opt.wrong::after{ content:"\2715"; background:var(--danger); color:var(--on-danger);}

  .lr-chips{ display:flex; flex-wrap:wrap; gap:8px;}
  .lr-chip2{ padding:11px 15px; border-radius:12px; background:var(--paper);
             border:1px solid var(--line); border-left:2px solid var(--saffron);
             cursor:pointer; font-family:inherit;
             font-size:.87rem; text-align:left; max-width:100%; transition:.15s;}
  .lr-chip2:hover:not(:disabled){ border-color:var(--saffron); background:var(--saffron-soft);}
  .lr-chip2.used{ opacity:.3; cursor:default; border-left-color:var(--teal);}
  /* Quarter chips carry Devanagari and need the Sanskrit face at a readable
     size — the Latin default renders the conjuncts too small to compare. */
  .lr-chip2.dv{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.05rem;
                line-height:1.75;}
  .lr-chip2.shake{ animation:lrshk .34s; border-color:var(--saffron-dark);}
  @keyframes lrshk{ 0%,100%{transform:none} 22%{transform:translateX(-6px)} 66%{transform:translateX(6px)} }
  .lr-slots{ display:flex; flex-direction:column; gap:6px; margin-bottom:13px;}
  .lr-slot{ padding:10px 13px; border-radius:12px; background:var(--teal-soft);
            border:1px solid var(--teal); border-left:2px solid var(--teal);
            font-size:.87rem;}
  .lr-slot.dv{ font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.02rem;}

  .lr-fb{ margin-top:14px;}
  .lr-fb .good{ color:var(--teal); font-weight:700; font-size:.92rem;}
  .lr-fb .bad{ color:var(--saffron-dark); font-weight:700; font-size:.92rem;}
  .lr-fb .nt{ margin:10px 0 13px; padding:12px 14px; border-radius:11px; background:var(--paper);
              border:1px solid var(--line); color:var(--ink-soft); font-size:.88rem; line-height:1.6;}

  /* the seal screen earns a teal wash — this is the one moment of arrival */
  .lr-finis{ text-align:center; padding:40px 18px; border-radius:18px;
             background:var(--teal-soft); border:1px solid var(--teal);}
  .lr-seal{ width:58px; height:58px; margin:0 auto 16px; border-radius:50%; display:grid;
            place-items:center; background:var(--teal-soft); color:var(--teal); font-size:1.6rem;}
  .lr-finis h2{ margin:0 0 8px; font-size:1.35rem; color:var(--ink);}
  .lr-finis p{ color:var(--ink-soft); max-width:50ch; margin:0 auto 16px; line-height:1.65;}
  .lr-finis .lr-all{ color:var(--saffron-dark); font-weight:700;}
  .lr-finis .lr-cta,.lr-finis .lr-ghost{ margin:5px;}

  @media (max-width:640px){
    .lr-grid{ grid-template-columns:1fr;}
    .lr-words{ grid-template-columns:repeat(auto-fill,minmax(124px,1fr));}
    .lr-nav .lr-cta,.lr-nav .lr-ghost{ flex:1;}
    .lr-hint{ flex:1 0 100%; order:3;}
  }

  /* Owner 2026-08-30, second pass: every chooser in the app speaks ONE chip
     grammar — soft pill = an option, gold pill = where you are, hover = the
     door warming to saffron-dark. The segments ARE crumbs now; the paper
     track retired because the pills carry their own round boundary. */
  .mode-seg{ display:flex; gap:8px; flex-wrap:wrap; max-width:100%; }
  .mode-seg .ms-btn{ background:var(--saffron-soft); border:none; color:var(--saffron-dark);
             border-radius:999px; padding:7px 16px; cursor:pointer; font-size:.86rem;
             font-weight:700; font-family:inherit; transition:color .15s, background-color .15s; }
  .mode-seg .ms-btn:hover, .mode-seg .ms-btn:focus-visible{ background:var(--saffron-dark);
             color:var(--on-saffron); outline:none; }
  .mode-seg .ms-btn.on{ background:var(--saffron); color:var(--on-saffron);
             box-shadow:0 1px 3px rgba(var(--shadow),.25); }
  .mode-seg .ms-btn.on:hover{ background:var(--saffron); color:var(--on-saffron); }
  /* purana chapter view: clean hairline cards; saffron only for numbers */
  .th-flow .theme{ background:var(--paper); border:1px solid var(--line); border-radius:12px;
                   padding:16px 18px; margin:0 0 14px; cursor:pointer; transition:border-color .15s; }
  .th-flow .theme:hover{ border-color:var(--saffron); }
  .th-flow h3{ font-family:Georgia,serif; color:var(--teal); font-size:1.05rem; margin:0 0 6px; }
  /* Owner 2026-09-01: the verse range is a verse NUMBER and must read as one.
     It was --ink-soft, so it sank into the description text while every other
     number in the app is saffron. Weight 600 because at .78rem the colour
     alone is thin on white (--saffron-dark measures 3.28:1 there). */
  .th-flow h3 .rng{ color:var(--saffron-dark); font-weight:600; font-size:.78rem; margin-left:8px; white-space:nowrap; }
  /* the same range beside a view title: it must not inherit the 1.7rem
     heading size, or the number shouts louder than the theme's name */
  .view-title .rng{ color:var(--saffron-dark); font-weight:600; font-size:.8rem;
                    margin-left:10px; white-space:nowrap; vertical-align:.32em; }
  .th-flow .tdesc{ margin:0 0 6px; color:var(--ink-soft); font-size:.92rem; line-height:1.6; }
  .vcards{ margin-top:12px; display:grid; grid-template-columns:repeat(auto-fill, minmax(240px,1fr)); gap:12px; }
  /* display-only: same card body, but no pointer, no hover lift — an object
     to read, not a button to press */
  .vcard{ cursor:default; }
  .vcard:hover{ border-color:var(--line); box-shadow:0 1px 2px rgba(var(--shadow),.05); }
  .vcard h3{ font-size:1rem; }   /* the theme title outranks its verses */
  .chdeva{ color:var(--saffron-dark); font-family:"Noto Serif Devanagari",Georgia,serif; font-size:1.05rem; }
  .card h3{ font-family:Georgia,serif; font-size:1.15rem; color:var(--teal);}
  .card p{ color:var(--ink-soft); font-size:.86rem; flex:1;}
  .card .meta{ margin-top:10px; font-size:.8rem; color:var(--ink-soft); font-weight:600;}
  .card .go{ margin-top:10px; color:var(--teal); font-weight:700; font-size:.88rem;}
  .card .soon{ margin-top:10px; color:var(--muted); font-weight:600; font-size:.85rem; font-style:italic;}
  .part{ margin-bottom:26px;}
  .part-head{ display:flex; align-items:baseline; gap:12px; border-bottom:3px solid var(--saffron); padding-bottom:8px; margin-bottom:14px; flex-wrap:wrap;}
  .part-head .pnum{ font-family:Georgia,serif; font-weight:700; color:var(--saffron-dark); font-size:1.05rem;}
  .part-head .ptitle{ font-family:Georgia,serif; font-size:1.25rem; color:var(--teal); font-weight:700;}
  .part-head .pdesc{ color:var(--ink-soft); font-size:.86rem; margin-left:auto;}
  .mini{ background:var(--paper); border:1px solid var(--line); border-radius:12px; padding:11px 14px; cursor:pointer;
         transition:.15s; box-shadow:0 4px 12px rgba(var(--shadow),.06);}
  .mini:hover{ border-color:var(--saffron); box-shadow:0 4px 12px rgba(var(--shadow),.10);}
  .mini .vnum, .w-day .vnum{ font-family:Georgia,serif; font-weight:700; color:var(--saffron-dark); font-size:.98rem; margin-bottom:5px; letter-spacing:.03em;}
  /* The topic line is quiet metadata, not a headline: same soft colour as its
     "Verse topic" prefix, so the Devanagari below stays the star of the card. */
  .mini .m-topic, .w-day .m-topic{ font-family:Georgia,serif; font-weight:600; color:var(--ink-soft); font-size:.9rem; margin-bottom:7px; line-height:1.35;}
  .mini .mt-lab, .w-day .mt-lab{ font-weight:400; font-style:italic; color:var(--ink-soft); font-size:.8rem; margin-right:2px;}
  .mini .padas, .w-day .padas{ font-family:"Noto Serif Devanagari", Georgia, serif; color:var(--teal); font-size:1.02rem; line-height:1.5; background:var(--cream); border-radius:8px; padding:7px 9px;}
  .mini .padas .spk, .w-day .padas .spk{ display:block; color:var(--saffron-dark); font-size:.82rem; font-style:italic; margin-bottom:2px;}
  .mini .padas .gline, .w-day .padas .gline{ display:block; line-height:1.6;}
  .mini .padas .gp, .w-day .padas .gp{ display:inline;}
  .mini .vhint, .w-day .vhint{ color:var(--ink-soft); font-size:.78rem; font-style:italic; line-height:1.4; margin-top:6px;}
  .share-panel{ display:none; flex-direction:column; align-items:flex-start; gap:8px; margin:10px 0 0;
    background:var(--cream); border:1px solid var(--line); border-radius:14px; padding:12px 14px;}
  .sp-hint{ font-size:.85rem; color:var(--ink-soft); line-height:1.5;}
  .sp-link{ width:100%; font-size:.76rem; color:var(--teal); background:var(--paper);
    border:1px dashed var(--line); border-radius:8px; padding:7px 9px; word-break:break-all;}
  .sp-copy{ background:var(--saffron); color:var(--on-saffron); border:none; border-radius:999px;
    padding:9px 18px; font-weight:700; font-size:.85rem; cursor:pointer;}
  .back-top{ display:inline-block; margin:4px 0 16px; background:none; border:1px solid var(--teal); color:var(--teal);
             font-weight:700; padding:8px 18px; border-radius:999px; cursor:pointer; font-size:.9rem;}
  .back-top:hover{ background:var(--teal); color:var(--on-accent);}
  /* the same back button repeated at the end of a long list, so a reader who has
     scrolled to the bottom does not have to scroll all the way up again */
  /* left, not centred: this is the same button as the crumb at the top of the
     page, so it sits on the same left edge as every heading and card. A back
     affordance is an escape hatch, not a call to action — findable, not loud. */
  .back-foot{ margin:26px 0 4px; padding-top:20px; border-top:1px solid var(--line);}

  /* ---- favourites: ordering + a personal note ---- */
  .fav-tools{ display:inline-flex; gap:6px; align-items:center; margin-left:auto;}
  .fav-move{ background:none; border:1px solid var(--line); color:var(--teal); border-radius:8px;
             width:30px; height:30px; font-weight:700; cursor:pointer; line-height:1; padding:0;}
  .fav-move:hover:not(:disabled){ border-color:var(--teal); background:var(--teal-soft);}
  .fav-move:disabled{ opacity:.3; cursor:default;}
  .fav-note{ margin-top:9px; display:flex; gap:8px; align-items:flex-start;}
  .fav-note label{ font-size:.74rem; font-weight:700; color:var(--ink-soft); text-transform:uppercase;
                   letter-spacing:.04em; padding-top:7px; flex:0 0 auto;}
  .fav-note textarea{ flex:1; border:1px solid var(--line); border-radius:8px; padding:5px 9px;
                      font:inherit; font-size:.88rem; background:var(--cream); color:var(--ink);
                      resize:none; overflow:hidden; min-height:34px;}
  .fav-note textarea:focus{ outline:none; border-color:var(--saffron); background:var(--paper);}

  /* ---- continuous reading ---- */
  /* mūla: the verses run closer together, the way a printed pāṭha is set */
  .reading{ background:var(--paper); border:1px solid var(--line); border-radius:14px; padding:14px 18px 6px;}
  /* the speaker is named only when the voice changes, so it must stand out */
  .rd-spk{ font-family:"Noto Serif Devanagari",Georgia,serif; color:var(--saffron-dark);
           font-weight:700; font-size:1rem; margin:20px 0 8px; padding-bottom:5px;
           border-bottom:2px solid var(--saffron-soft);}
  .rd-deva .rd-spk{ margin:6px 0 8px;}
  .rd-v:first-child .rd-spk, .rd-spk:first-child{ margin-top:4px;}
  .rd-v{ padding:12px 0 14px; border-bottom:1px solid var(--line); cursor:pointer; position:relative;}
  .rd-v:last-child{ border-bottom:none;}
  .rd-v:hover{ background:var(--cream);}
  .rd-n{ font-family:Georgia,serif; font-weight:700; color:var(--saffron-dark); font-size:.82rem;}
  .rd-deva{ font-family:"Noto Serif Devanagari",Georgia,serif; color:var(--teal);
            font-size:1.12rem; line-height:1.85; margin-bottom:5px;}
  .rd-tr{ color:var(--ink-soft); font-size:.95rem; line-height:1.6;}
  /* quiet labels name each translation, so the two voices never blur */
  .rd-lb{ color:var(--ink-soft); font-size:.74rem; font-weight:700; letter-spacing:.05em;
          text-transform:uppercase; margin:8px 0 2px; opacity:.8; }
  .rd-lb:first-of-type{ margin-top:6px; }
  /* the paraphrase is the flowing read — set lighter and italic under the
     literal, so the eye gets "what it says" then "what it means" */
  .rd-par{ color:var(--ink-soft); font-size:.88rem; line-height:1.55; font-style:italic; margin-top:3px;}
  .back-foot .back-top{ margin:0;}
  .mini-crumb{ display:flex; gap:10px; margin:2px 0 16px; flex-wrap:wrap;}
  .mini-crumb .bc-btn{ background:var(--paper); border:1px solid var(--line); border-radius:12px; cursor:pointer;
             display:flex; flex-direction:column; align-items:flex-start; gap:1px; padding:8px 14px; transition:.15s;}
  .mini-crumb .bc-btn:hover{ border-color:var(--saffron); background:var(--saffron-soft);}
  .mini-crumb .bc-num{ font-weight:700; color:var(--teal); font-size:.95rem;}
  .mini-crumb .bc-name{ color:var(--ink-soft); font-size:.8rem;}
  .mini-crumb .bc-cur{ background:var(--saffron-soft); border:1px solid var(--saffron); border-radius:12px;
             display:flex; flex-direction:column; align-items:flex-start; gap:1px; padding:8px 14px;}
  .mini-crumb .bc-cur .bc-num{ color:var(--saffron-dark);}
  .mini-crumb .bc-sep{ align-self:center; color:var(--line); font-weight:800; font-size:1rem; padding:0 2px;}

  /* the breadcrumb: quiet names, not a second strip of pills */
  /* The running head. Intellect: ancestors recede (soft ink, regular weight),
     separators are the faintest thing on the line, and the current page is
     the darkest — the eye lands on "where you are" without being told.
     Eyes: hover speaks the app's one accent language (saffron), never a
     second hue; Devanagari in the trail renders in the embedded serif. */
  /* The trail as chips (owner 2026-08-30: "not prominent … chapter1, chapter2
     style"). Chips are how this app labels structure, so the map reads in the
     project's own vocabulary — but with one refinement: ancestors wear the
     saffron-SOFT pill of the chapter list (doors you can walk back through)
     while the current page wears the gold-leaf chip, the same metal as the
     raised segment in the tray. Soft = door, gold = where you stand.
     No uppercase/letter-spacing here: the crumbs mix Latin and Devanagari,
     and tracking strains the mātrā flow. */
  .way-crumb{ display:flex; flex-wrap:wrap; align-items:center; gap:8px; margin:2px 0 18px;
              font-family:"Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, "Noto Serif Devanagari", sans-serif; }
  /* Volume control (owner 2026-08-31: "too much orange"): one gold per page.
     Gold = the decision you're IN (the raised segment in the tray). The trail
     steps down: current page = soft pill, ancestors = neutral hairline pills —
     prominent by size and shape, not by hue. Hover still warms, one step. */
  .wc-chip{ background:var(--paper); color:var(--ink-soft); border:1px solid var(--line); border-radius:999px;
            padding:7px 16px; font-size:.88rem; font-weight:700; font-family:inherit; line-height:1.4;
            transition:background-color .15s, color .15s, border-color .15s; }
  button.wc-chip{ cursor:pointer; }
  button.wc-chip:hover, button.wc-chip:focus-visible{ background:var(--saffron-soft); color:var(--saffron-dark);
            border-color:var(--saffron-soft); outline:none; }
  .wc-chip.wc-cur{ background:var(--saffron-soft); color:var(--saffron-dark); border-color:var(--saffron-soft); }
  .wc-sep{ color:var(--muted); font-size:.78rem; }

  .welcome{ text-align:center; padding:44px 12px 30px; max-width:860px; margin:0 auto;}
  .welcome .w-om{ font-size:3.6rem; color:var(--saffron); line-height:1; margin-bottom:14px;}
  .welcome .view-title{ font-size:2rem;}
  .welcome .tool-btn.big{ font-size:1.02rem; padding:14px 36px; margin-top:20px;}
  .welcome .w-foot{ color:var(--ink-soft); font-size:.9rem; margin-top:30px; letter-spacing:.05em;}
  /* The work-in-progress note. Deliberately the quietest thing on the screen:
     --ink-soft, small, and set off by a hairline rule so it reads as an aside
     from the author rather than a warning about the text. */
  .welcome .w-wip{ max-width:46ch; margin:16px auto 0; padding-top:14px;
                   border-top:1px solid var(--line); color:var(--ink-soft);
                   font-size:.82rem; line-height:1.6; font-style:italic;}
  .welcome .w-day{ max-width:560px; margin:26px auto 6px; background:var(--paper); border:1px solid var(--line); border-radius:16px;
                   padding:18px 22px; cursor:pointer; box-shadow:0 1px 2px rgba(var(--shadow),.05); transition:.18s; text-align:left;}
  .welcome .w-day:hover{ border-color:var(--saffron); box-shadow:0 4px 14px rgba(var(--shadow),.10);}
  /* A small oval tag, not a headline — the card already has a saffron frame,
     so the label wears the soft variant and lets the verse number lead. */
  .welcome .wd-label{ display:table; margin:0 auto 12px; background:var(--saffron-soft); color:var(--saffron-dark);
    font-family:Georgia,serif; font-weight:700; font-size:.78rem; letter-spacing:.1em; text-transform:uppercase;
    border-radius:999px; padding:6px 18px; }
  /* the welcome card is a display piece, not a list item — centre it, while
     the search/theme grids stay left-aligned for reading */
  .welcome .w-day .vnum, .welcome .w-day .m-topic,
  .welcome .w-day .padas, .welcome .w-day .vhint{ text-align:center; }
  /* The speaker is not part of the verse, so it must not read as verse text.
     Saffron + italic everywhere else in the app — match that here. */
  /* Verse number set inside the closing daṇḍas, as a printed edition does. */
  .gl-n{ font-family:Georgia,serif; font-weight:700; color:var(--saffron-dark); font-size:.8rem;}

  .grid.sections{ grid-template-columns:repeat(auto-fill, minmax(270px,1fr));}
  .card.sect h3{ font-family:"Noto Serif Devanagari", Georgia, serif; font-size:1.32rem;}
  .card.sect p{ font-size:.92rem;}


  .toolbar{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; padding:12px 20px; background:var(--toolbar); border-bottom:2px solid var(--line);}
  .toolbar .searchwrap{ display:flex; align-items:center; gap:6px; flex:1; min-width:240px; max-width:640px;}
  .toolbar input[type=search]{ flex:1; padding:9px 14px; border:1px solid var(--line); border-radius:999px; font-size:.92rem; background:var(--field); color:var(--ink); outline:none;}
  .toolbar input[type=search]:focus{ border-color:var(--saffron);}
  /* inline stroke icons: sized and coloured by the surrounding text, so they
     behave like glyphs, not pictures — and follow both themes for free */
  .ic{ width:1.05em; height:1.05em; display:inline-block; vertical-align:-.18em; margin-right:6px;
       fill:none; stroke:currentColor; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }
  .ic.fill{ fill:currentColor; }
  .sw-field{ position:relative; flex:1; display:flex; }
  .sw-field input[type=search]{ width:100%; padding-left:36px; }
  .sw-ic{ position:absolute; left:13px; top:50%; transform:translateY(-50%);
          color:var(--ink-soft); display:flex; pointer-events:none; }
  .sw-ic .ic{ width:15px; height:15px; margin:0; }
  .sw-x{ position:absolute; right:7px; top:50%; transform:translateY(-50%); width:30px; height:30px;
         border:none; border-radius:50%; background:transparent; color:var(--ink-soft);
         display:none; align-items:center; justify-content:center; cursor:pointer; padding:0; }
  .sw-x .ic{ margin:0; width:15px; height:15px; }
  .sw-x:hover{ background:var(--saffron-soft); color:var(--saffron-dark); }
  .sw-field.has-x .sw-x{ display:flex; }
  .sw-field.has-x input[type=search]{ padding-right:40px; }
  .sw-field input[type=search]::-webkit-search-cancel-button{ -webkit-appearance:none; display:none; }
  ::selection{ background:var(--saffron-soft); color:var(--ink); }
  .tool-btn{ background:var(--paper); border:1px solid var(--line); color:var(--teal); font-weight:700; font-size:.85rem; padding:8px 16px; border-radius:999px; cursor:pointer; transition:.15s;}
  .tool-btn:hover{ border-color:var(--saffron); background:var(--saffron-soft);}
  .tool-btn.primary{ background:var(--saffron); border-color:var(--saffron); color:var(--on-saffron);}
  .tool-btn.primary:hover{ background:var(--saffron-dark);}
  .fav-btn{ background:var(--saffron-soft); border:1px solid var(--saffron); color:var(--saffron-dark); font-weight:700; font-size:.8rem; padding:4px 12px; border-radius:999px; cursor:pointer; margin-left:10px;}
  .fav-btn.saved{ background:var(--saffron); color:var(--on-accent);}
  .res-head{ font-family:Georgia,serif; font-size:1.25rem; color:var(--teal); margin-bottom:4px;}
  .res-count{ color:var(--ink-soft); font-size:.9rem; margin-bottom:16px;}
  .res-card{ background:var(--paper); border:1px solid var(--line); border-radius:12px; padding:12px 16px; margin-bottom:12px; cursor:pointer; transition:.15s;}
  .res-card:hover{ border-color:var(--saffron); box-shadow:0 4px 12px rgba(var(--shadow),.08);}
  .res-top{ display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; margin-bottom:6px;}
  .res-num{ font-family:Georgia,serif; font-weight:700; color:var(--saffron-dark);}
  .res-title{ font-weight:600; color:var(--teal); font-size:.9rem;}
  .res-deva{ font-family:"Noto Serif Devanagari", Georgia, serif; color:var(--teal); font-size:1rem; line-height:1.55; background:var(--cream); border-radius:8px; padding:7px 10px; margin-bottom:6px;}
  .res-lit{ color:var(--ink-soft); font-size:.88rem; line-height:1.5;}
  .res-remove{ margin-left:auto; background:none; border:1px solid var(--line); color:var(--ink-soft); font-size:.72rem; font-weight:700; padding:3px 10px; border-radius:999px; cursor:pointer;}
  .res-remove:hover{ border-color:var(--danger); color:var(--danger);}
  .modal-bg{ position:fixed; inset:0; background:var(--scrim); display:none; align-items:center; justify-content:center; z-index:50; padding:20px;}
  .modal-bg.open{ display:flex;}
  .modal{ background:var(--cream); border-radius:20px; max-width:820px; width:100%; max-height:92vh; overflow-y:auto;
          box-shadow:0 24px 60px rgba(0,0,0,.35); border:1px solid var(--line); position:relative; padding:24px 30px 28px;}
  .modal .m-close{ position:sticky; top:0; float:right; background:var(--saffron); color:var(--on-saffron); border:none; width:38px;
                   height:38px; border-radius:50%; font-size:1.1rem; cursor:pointer; font-weight:700; margin:-8px -12px 0 0;}
  .m-num{ font-family:Georgia,serif; font-size:1.4rem; color:var(--saffron-dark); font-weight:700;}
  .m-part{ color:var(--teal); font-size:.88rem; font-weight:600; margin-bottom:2px;}
  .m-meter{ display:inline-block; background:var(--teal-soft); color:var(--teal); font-size:.78rem; font-weight:700;
            padding:3px 12px; border-radius:999px; margin:6px 0 12px; letter-spacing:.03em;}
  .m-verse{ background:var(--paper); border:1px solid var(--line); border-radius:14px; padding:16px 18px; margin:6px 0 4px;}
  .m-verse .spk{ font-family:"Noto Serif Devanagari", Georgia, serif; color:var(--saffron-dark); font-size:1.15rem;
                 font-style:italic; margin-bottom:8px; border-bottom:1px dashed var(--line); padding-bottom:6px;}
  .m-verse .spk .iast{ font-family:Georgia, serif; font-size:.85rem; color:var(--ink-soft); margin-left:10px;}
  .m-verse table{ width:100%; border-collapse:collapse;}
  .m-verse td{ vertical-align:top; padding:3px 2px;}
  .m-verse td.pnum{ width:26px; font-family:Georgia,serif; color:var(--saffron-dark); font-weight:700; font-size:.9rem; padding-top:6px;}
  .m-verse td.pd{ font-family:"Noto Serif Devanagari", Georgia, serif; font-size:1.35rem; color:var(--teal); line-height:1.7; padding-right:14px;}
  .m-verse td.pi{ font-style:italic; color:var(--ink-soft); font-size:.92rem; padding-top:8px;}
  .m-verse td.pi .danda{ color:var(--saffron-dark); font-weight:700;}
  .m-verse tr.pair td.pd{ padding-bottom:4px;}
  .m-verse tr.spkrow td.pd.spk{ font-family:'Noto Serif Devanagari', Georgia, serif; color:var(--saffron-dark); font-style:italic; padding:8px 2px 10px; border-bottom:1px dashed var(--line); font-size:1.1rem;}
  .m-verse tr.spkrow td.pd.spk .iast{ font-family:Georgia, serif; font-size:.85rem; color:var(--ink-soft); margin-left:10px;}
  .m-verse .spk-line:hover{ background:var(--saffron-soft);}
  .m-verse .spk-main{ border-bottom:1px dotted var(--saffron); }
  .m-verse .words{ display:none; margin-top:6px; background:var(--cream); border:1px solid var(--line); border-radius:8px; padding:8px 12px; min-width:0; max-width:100%;}
  .m-verse .words.open{ display:block;}
  .m-verse .words.mean-off .wmean{ display:none;}
  .m-verse .wrow{ padding:3px 0; border-bottom:1px dotted var(--line); min-width:0; max-width:100%;}
  .m-verse .wrow:last-child{ border-bottom:none;}
  .m-verse .wrow .wdeva{ font-family:'Noto Serif Devanagari', Georgia, serif; color:var(--teal); font-size:1.12rem; overflow-wrap:anywhere; word-break:break-word;}
  .m-verse .wrow .wiast{ font-style:italic; color:var(--ink-soft); font-size:.88rem; margin-left:10px; overflow-wrap:anywhere; word-break:break-word;}
  .m-verse .wrow .wmean{ display:block; color:var(--ink); font-size:.9rem; margin-left:14px; margin-top:1px; overflow-wrap:anywhere; word-break:break-word;}
  .words-bar{ display:flex; align-items:center; gap:10px; margin-bottom:10px; flex-wrap:wrap;}
  .words-bar .wb-hint{ color:var(--ink-soft); font-size:.78rem; font-style:italic;}
  .words-bar .wb-btn{ background:var(--teal); color:var(--on-accent); border:none; padding:4px 14px; border-radius:999px; cursor:pointer; font-size:.8rem; font-weight:600;}
  .words-bar .wb-btn:hover{ background:var(--teal-mid);}
  .words-bar .wb-btn:disabled{ opacity:.45; cursor:default; }
  .words-bar .wb-btn:disabled:hover{ background:var(--teal); }
  /* four pāda boxes in a 2x2 grid */
  .m-verse .pada-grid{ display:flex; flex-direction:column; gap:12px;}
  .m-verse .pada-row{ display:flex; gap:12px;}
  .m-verse .pada-box{ flex:1 1 0; min-width:0; max-width:100%; background:var(--paper); border:1px solid var(--line); border-radius:12px; padding:10px 14px; cursor:pointer; transition:border-color .15s, background .15s;}
  .m-verse .pada-box .pb-top{ display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; gap:8px;}
  .m-verse .pada-box .pb-num{ font-family:Georgia,serif; font-weight:700; color:var(--saffron-dark); font-size:.85rem; white-space:nowrap;}

  .m-verse .pada-box .pb-deva{ font-family:'Noto Serif Devanagari', Georgia, serif; color:var(--teal); font-size:1.3rem; line-height:1.7; cursor:pointer; overflow-wrap:anywhere; word-break:break-word;}
  .m-verse .pada-box:hover{ background:var(--saffron-soft); border-color:var(--saffron);}
  .m-verse .pada-box .pb-iast{ font-style:italic; color:var(--ink-soft); font-size:.88rem; overflow-wrap:anywhere; word-break:break-word;}
  .m-verse .spk-mid{ margin:2px 0;}
  .m-verse .spk-line{ margin:6px 0; font-family:'Noto Serif Devanagari', Georgia, serif; color:var(--saffron-dark); font-style:italic; font-size:1.05rem; cursor:pointer; border-radius:6px; padding:2px 4px;}
  .m-verse .spk-line .iast{ font-family:Georgia, serif; font-size:.85rem; color:var(--ink-soft); margin-left:10px;}
  .m-line{ margin-top:14px;}
  .m-line .lb{ display:inline-block; background:var(--teal); color:var(--on-accent); font-size:.72rem; font-weight:700;
               letter-spacing:.08em; text-transform:uppercase; padding:3px 10px; border-radius:999px; margin-bottom:5px;}
  .m-line .lt{ color:var(--ink); font-size:1rem;}
  .m-line.para .lb{ background:var(--saffron); color:var(--on-saffron);}
  .m-nav{ display:flex; justify-content:space-between; align-items:center; margin-top:22px; gap:10px;}
  .m-tail{ display:none;}   /* only needed where .m-nav is sticky (phones) */
  .m-nav button{ background:var(--teal); color:var(--on-accent); border:none; padding:10px 18px; border-radius:999px; cursor:pointer; font-weight:600; font-size:.9rem;}
  .m-nav button:hover{ background:var(--teal-mid);} .m-nav button:disabled{ opacity:.35; cursor:default;}
  .m-nav .m-random{ margin:0 auto; background:var(--saffron); color:var(--on-saffron); border:none; padding:12px 26px; border-radius:999px; cursor:pointer; font-weight:700; font-size:.98rem; font-family:"Noto Serif Devanagari", Georgia, serif;}
  .m-nav .m-random:hover{ background:var(--saffron-dark);}
  .m-nav .m-back{ background:var(--teal-soft); color:var(--teal); border:1px solid var(--teal); padding:10px 18px; border-radius:999px; cursor:pointer; font-weight:700; font-size:.9rem;}
  .m-nav .m-back:hover{ background:var(--teal); color:var(--on-accent);}

  .m-count{ color:var(--ink-soft); font-size:.85rem; font-weight:600;}
  footer{ text-align:center; color:var(--ink-soft); font-size:.82rem; padding:18px 20px 26px; border-top:1px solid var(--line);}
  /* plain inline text — no flex gap, or the <b> would push the comma away */
  footer .credit{ margin-top:10px; padding-top:10px; border-top:1px dashed var(--line);
                  font-size:.8rem; color:var(--ink-soft); display:block; text-align:center;}
  footer .credit b{ color:var(--teal); font-weight:700;}
  footer .credit.attrib{ margin-top:6px; padding-top:6px; border-top:none;
                  font-size:.72rem; line-height:1.55; color:var(--muted); max-width:62ch;
                  margin-left:auto; margin-right:auto;}
  footer .credit.attrib a{ color:var(--muted); text-decoration:underline;}
  .fade-in{ animation:fadein .28s ease;} @keyframes fadein{ from{opacity:0; transform:translateY(6px);} to{opacity:1; transform:none;} }
  @media (max-width:640px){ .modal{ padding:16px 16px 20px;} .m-verse td.pd{ font-size:1.12rem;} }

  /* ==================== MOBILE / TOUCH (Android · iOS) ==================== */
  html{ -webkit-text-size-adjust:100%; text-size-adjust:100%; }
  body{ -webkit-tap-highlight-color:rgba(232,145,44,.18); overscroll-behavior-y:none; }
  button, .card, .mini, .res-card, .pada-box, .spk-line, .lang-btn{ -webkit-tap-highlight-color:transparent; touch-action:manipulation; }
  /* modern basics: visible keyboard focus, and stillness for those who ask */
  :focus-visible{ outline:2px solid var(--saffron); outline-offset:2px; }
  @media (prefers-reduced-motion: reduce){
    *, *::before, *::after{ animation:none !important; transition:none !important; }
  }
  input, button, select, textarea{ font-family:inherit; }
  /* iOS zooms any input whose font-size is < 16px on focus */
  .toolbar input[type=search]{ font-size:16px; }
  .modal, .wrap{ -webkit-overflow-scrolling:touch; }
  /* Hover lifts are a mouse idiom — on touch they STICK after a tap, so the
     last thing you touched keeps looking selected. Every hover in the app must
     be cancelled here and answered with an :active state instead, or a phone
     shows a phantom selection (owner 2026-09-01).
     This block covered only the original components; the learn path and Play
     were added later and were never listed, which is exactly why their chips
     and cards stayed lit after a tap. */
  @media (hover:none){
    .card:hover, .mini:hover, .res-card:hover, .mini-crumb .bc-btn:hover, .welcome .w-day:hover{ transform:none; box-shadow:0 6px 18px rgba(var(--shadow),.08); }
    .card:active, .mini:active, .res-card:active, .welcome .w-day:active{ transform:scale(.985); border-color:var(--saffron); }
    .tool-btn:active, .lang-btn:active, .m-nav button:active{ filter:brightness(.93); }
    .pada-box:hover{ background:var(--paper); border-color:var(--line); }
    .pada-box:active{ background:var(--saffron-soft); border-color:var(--saffron); }
    .m-verse .spk-line:hover{ background:none; }

    /* ---- learn path + Play: cancel every hover, answer with :active ---- */
    .lr-cta:hover{ background:var(--saffron); border-color:var(--saffron); }
    .lr-cta:active{ background:var(--saffron-dark); border-color:var(--saffron-dark); }
    .lr-ghost:hover:not(:disabled){ background:var(--paper); border-color:var(--line); }
    .lr-ghost:active:not(:disabled){ background:var(--saffron-soft); border-color:var(--saffron); }
    .lr-chip:hover{ border-color:var(--line); box-shadow:none; transform:none; }
    .lr-chip:active{ border-color:var(--saffron); }
    .lr-chip.ok:hover{ border-color:var(--teal); }
    .lr-opt:hover:not(:disabled){ background:var(--paper); border-color:var(--line); }
    .lr-opt:active:not(:disabled){ background:var(--saffron-soft); border-color:var(--saffron); }
    .lr-chip2:hover:not(:disabled){ background:var(--paper); border-color:var(--line); }
    .lr-chip2:active:not(:disabled){ background:var(--saffron-soft); border-color:var(--saffron); }
    .lr-q:hover{ border-color:var(--line); }
    .lr-qh:hover{ background:none; }
    .pl-mode:hover{ border-color:var(--line); box-shadow:0 1px 2px rgba(var(--shadow),.05); transform:none; }
    .pl-mode:active{ border-color:var(--saffron); transform:scale(.985); }
    .pl-sel:hover{ border-color:var(--line); }
    .pl-sel:active{ border-color:var(--saffron); }
    /* a selected scope must still read as selected — it is state, not hover */
    .pl-scope .lr-ghost.on:hover{ background:var(--saffron); border-color:var(--saffron); }
  }

  @media (max-width:760px){
    /* ---- header ---- */
    header{ padding:12px 14px calc(10px + env(safe-area-inset-bottom,0px));
            padding-left:calc(14px + env(safe-area-inset-left,0px)); padding-right:calc(14px + env(safe-area-inset-right,0px));
            padding-top:calc(12px + env(safe-area-inset-top,0px)); }
    .header-inner{ gap:10px; }
    .header-inner .om{ font-size:1.5rem; }
    .header-inner h1{ font-size:1.05rem; line-height:1.3; }
    #appSub{ display:none; }
    .header-inner .tag{ display:none; }
    .langbar{ width:100%; gap:8px; margin-left:0; }
    .lang-btn{ flex:1; padding:9px 6px; font-size:.82rem; min-height:40px; }
    .mode-box{ padding:12px 14px; }
    .mode-seg .ms-btn{ padding:9px 14px; font-size:.82rem; min-height:40px; }

    /* ---- toolbar: sticky so search / home stay reachable ---- */
    .toolbar{ position:sticky; top:0; z-index:30; gap:8px; padding:9px 12px;
              padding-left:calc(12px + env(safe-area-inset-left,0px)); padding-right:calc(12px + env(safe-area-inset-right,0px));
              box-shadow:0 2px 10px rgba(var(--shadow),.07); }
    .toolbar .searchwrap{ order:-1; width:100%; flex:1 0 100%; max-width:none; min-width:0; }
    .toolbar input[type=search]{ min-height:42px; }
    .toolbar .tool-btn{ flex:1; min-height:40px; padding:9px 8px; font-size:.82rem; white-space:nowrap; }

    /* ---- content ---- */
    .wrap{ padding:16px 14px 40px; padding-left:calc(14px + env(safe-area-inset-left,0px)); padding-right:calc(14px + env(safe-area-inset-right,0px)); }
    .view-title{ font-size:1.35rem; }
    .view-sub{ font-size:.92rem; margin-bottom:16px; }
    .crumbs{ font-size:.84rem; gap:6px; margin-bottom:14px; }
    .way-crumb{ gap:6px; }
    .wc-chip{ padding:7px 13px; font-size:.8rem; min-height:34px; }
    .toolbar input[type=search]{ font-size:16px; }  /* iOS zooms on focus below 16px */
    .crumbs .back-top{ font-size:.82rem; padding:7px 14px; min-height:36px; }
    .grid{ gap:12px; }
    .grid.chapters, .grid.themes, .grid.verses, .grid.sections{ grid-template-columns:1fr; }
    .vcards{ grid-template-columns:1fr; }
    .card{ padding:14px 16px; border-radius:14px; }
    .card h3{ font-size:1.08rem; }
    .card.sect h3{ font-size:1.2rem; }
    .part-head{ gap:6px; }
    .part-head .ptitle{ font-size:1.1rem; }
    .part-head .pdesc{ margin-left:0; flex:1 0 100%; }
    .mini .padas, .w-day .padas{ font-size:1.06rem; }
    .back-top{ min-height:44px; }
    .mini-crumb{ gap:6px; }
    .mini-crumb .bc-btn, .mini-crumb .bc-cur{ padding:7px 10px; }
    .mini-crumb .bc-name{ font-size:.74rem; }

    /* ---- welcome ---- */
    .welcome{ padding:26px 4px 20px; }
    .welcome .w-om{ font-size:2.8rem; }
    .welcome .view-title{ font-size:1.55rem; }
    .welcome .tool-btn.big{ width:100%; padding:15px 20px; font-size:1rem; min-height:50px; }
    .welcome .w-day{ padding:16px 16px; }
    /* ---- verse modal: full-screen sheet ---- */
    .modal-bg{ padding:0; align-items:stretch; }
    .modal{ max-width:none; width:100%; max-height:none; height:100%; border-radius:0; border:none;
            border-top:1px solid var(--line);
            /* top padding clears the notch/status bar — without the inset the
               first line of a verse hides behind it and cannot be scrolled to */
            padding-top:calc(14px + env(safe-area-inset-top,0px));
            padding-bottom:calc(26px + env(safe-area-inset-bottom,0px));
            padding-left:calc(14px + env(safe-area-inset-left,0px));
            padding-right:calc(14px + env(safe-area-inset-right,0px));
            overscroll-behavior:contain; }
    .modal .m-close{ position:fixed; top:calc(10px + env(safe-area-inset-top,0px));
                     right:calc(12px + env(safe-area-inset-right,0px)); float:none; margin:0; z-index:5;
                     width:44px; height:44px; font-size:1.2rem; box-shadow:0 4px 14px rgba(0,0,0,.3); }
    .m-num{ font-size:1.15rem; padding-right:52px; }
    .fav-btn{ margin-left:0; margin-top:8px; display:inline-block; padding:7px 14px; min-height:36px; }
    .m-part{ font-size:.82rem; }
    .m-verse{ padding:12px 12px; }
    .words-bar .wb-btn{ min-height:34px; padding:6px 14px; }
    /* pādas stack one per row — two side by side is unreadable on a phone */
    .m-verse .pada-row{ flex-direction:column; gap:10px; }
    .m-verse .pada-grid{ gap:10px; }
    .m-verse .pada-box{ padding:10px 12px; }
    .m-verse .pada-box .pb-deva{ font-size:1.24rem; }
    .m-verse .wrow{ padding:5px 0; }
    .m-line .lt{ font-size:.98rem; }
    /* nav bar pinned to the bottom of the sheet, thumb-reachable */
    /* A sticky bar floats above the content, so the sheet ends with a spacer
       (.m-tail) tall enough for the last line to clear it when fully scrolled.
       Without it the paraphrase stays hidden behind Previous/Next. */
    .m-tail{ display:block; height:76px; }
    .m-nav{ position:sticky; bottom:0; margin:18px -14px 0;
            margin-bottom:calc(-26px - env(safe-area-inset-bottom,0px));
            padding:10px 14px calc(10px + env(safe-area-inset-bottom,0px));
            background:var(--cream);
            box-shadow:0 -10px 16px -8px rgba(var(--shadow),.28);
            border-top:1px solid var(--line); gap:8px; }
    .m-nav button{ min-height:46px; padding:11px 14px; font-size:.9rem; flex:1; }
    .m-nav .m-count{ flex:0 0 auto; font-size:.8rem; text-align:center; }
    .m-nav .m-random{ flex:1 1 100%; min-height:50px; }
    .m-nav .m-back{ flex:1; }
    footer{ font-size:.78rem; padding:16px 16px calc(22px + env(safe-area-inset-bottom,0px)); }
  }

  @media (max-width:380px){
    .header-inner h1{ font-size:.98rem; }
    .lang-btn{ font-size:.76rem; padding:9px 4px; }
    .m-verse .pada-box .pb-deva{ font-size:1.16rem; }
    .toolbar .tool-btn{ font-size:.76rem; }
  }

  /* landscape phones: keep the sheet scrollable, shrink vertical padding */
  @media (max-width:900px) and (orientation:landscape) and (max-height:520px){
    header{ padding-top:8px; padding-bottom:8px; }
    .modal{ padding-top:10px; }
    .welcome{ padding-top:16px; }
  }

  @media (prefers-reduced-motion:reduce){
    *{ animation-duration:.001ms !important; transition-duration:.001ms !important; }
  }

  /* ---- no-JavaScript fallback (WhatsApp / Gmail in-app viewers) ---- */
  .ns-box{ max-width:640px; margin:10px auto 40px; background:var(--paper);
           border:1px solid var(--saffron); border-radius:16px; padding:22px 22px 24px;
           box-shadow:0 8px 22px rgba(var(--shadow),.10); }
  .ns-box .ns-om{ font-size:2.6rem; color:var(--saffron); text-align:center; line-height:1; margin-bottom:6px; }
  .ns-box h2{ font-family:Georgia,serif; color:var(--teal); font-size:1.25rem; text-align:center; margin-bottom:12px; }
  .ns-box p{ color:var(--ink); font-size:.95rem; margin-bottom:10px; }
  .ns-box .ns-how{ background:var(--saffron-soft); border-radius:10px; padding:10px 12px; }
  .ns-box hr{ border:none; border-top:2px dashed var(--line); margin:14px 0; }
  .ns-box p[lang]{ font-size:.92rem; color:var(--ink-soft); }
</style>
</head>
<body>

<div class="atm" aria-hidden="true">
  <div class="atm-wisp"></div>
  <div class="atm-wisp b"></div>
  <div class="atm-wisp c"></div>
  <svg class="atm-feather" viewBox="0 0 80 200" fill="none">
    <path d="M40 198 C40 140 40 96 40 64" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
    <ellipse cx="40" cy="46" rx="22" ry="38" stroke="currentColor" stroke-width="1.1"/>
    <ellipse cx="40" cy="40" rx="12" ry="20" stroke="currentColor" stroke-width="1"/>
    <circle cx="40" cy="36" r="5.5" fill="currentColor" opacity=".35"/>
    <path d="M40 84 C28 70 22 52 24 38" stroke="currentColor" stroke-width=".7" opacity=".7"/>
    <path d="M40 84 C52 70 58 52 56 38" stroke="currentColor" stroke-width=".7" opacity=".7"/>
  </svg>
</div>

<header>
  <div class="header-inner">
    <span class="om">ॐ</span>
    <div>
      <h1 id="appTitle">Bhagavad Gita — an Interactive Study</h1>
      <div id="appSub" style="font-size:.82rem; color:var(--hdr-sub);">श्रीमद्भगवद्गीता · chapters → themes → subthemes → verses · each verse in its 4 pādas</div>
    </div>
    <div class="tag"><span id="tagVerses">18 chapters · 700 verses · study edition</span></div>
    <div class="langbar" id="langbar">
      <div class="seg">
        <button class="lang-btn on" data-lang="en" onclick="setLang('en')">English</button>
        <button class="lang-btn" data-lang="ne" onclick="setLang('ne')">नेपाली</button>
        <button class="lang-btn" data-lang="hi" onclick="setLang('hi')">हिन्दी</button>
      </div>
      <button class="lang-btn theme-btn" id="themeBtn" onclick="toggleTheme()" aria-label="Toggle dark mode"><span id="themeIcon"><svg class="ic" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></span></button>
    </div>
  </div>
</header>

<div class="toolbar">
  <button class="tool-btn" onclick="goHome()" id="homeBtn"><svg class="ic" viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg><span id="homeLbl">Home</span></button>
  <div class="searchwrap">
    <div class="sw-field">
      <span class="sw-ic"><svg class="ic" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg></span>
      <input type="search" id="searchInput" placeholder="…" aria-label="search" oninput="onSearchInput(this.value)" onkeydown="if(event.key==='Enter')doSearch()">
      <button type="button" class="sw-x" id="clearBtn" onclick="clearSearch()"><svg class="ic" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
    </div>
  </div>
  <button class="tool-btn" onclick="randomVerse()" id="randomBtn"><svg class="ic" viewBox="0 0 24 24"><path d="M16 3h5v5"/><path d="M21 3 4 20"/><path d="M21 16v5h-5"/><path d="m15 15 6 6"/><path d="m4 4 5 5"/></svg><span id="randLbl">Random</span></button>
  <button class="tool-btn" onclick="showPlay()" id="playBtnTool"><svg class="ic" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="8.5" cy="8.5" r="1.4" fill="currentColor"/><circle cx="15.5" cy="15.5" r="1.4" fill="currentColor"/><circle cx="15.5" cy="8.5" r="1.4" fill="currentColor"/><circle cx="8.5" cy="15.5" r="1.4" fill="currentColor"/></svg><span id="playLbl">Play</span></button>
  <button class="tool-btn" onclick="showFavorites()" id="favBtnTool"><svg class="ic" viewBox="0 0 24 24"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg><span id="favLbl">Favorites</span></button>
</div>

<div class="wrap">
  <nav class="crumbs" id="crumbs"></nav>
  <!-- Announces each view change to screen readers. The app never reloads, so
       without this a reader who taps "Chapter 2" hears silence: the heading
       changed but focus did not move. Polite, so it never interrupts. -->
  <p id="srStatus" role="status" aria-live="polite" class="sr-only"></p>
  <main id="view"><div id="bootNote" style="padding:46px 20px;text-align:center;color:var(--ink-soft);font-size:.95rem;">ॐ Loading the 700 verses…</div></main>

  <!-- Shown only when JavaScript is disabled — e.g. the in-app file viewers of
       WhatsApp / Gmail / some file managers, which render HTML without running
       scripts. Without this the page would look blank between header & footer. -->
  <noscript>
    <div class="ns-box">
      <div class="ns-om">ॐ</div>
      <h2>Please open this file in a browser</h2>
      <p>This is a complete offline app, so it needs JavaScript to display the
         700 verses. The app viewer you are using right now does not run it.</p>
      <p class="ns-how"><b>How to open it:</b> tap the <b>⋮</b> / <b>share</b> icon
         and choose <b>“Open in browser”</b> — or save the file, then open it from
         your Files app with Chrome or Safari.</p>
      <hr>
      <p lang="ne"><b>नेपाली:</b> कृपया यो फाइल <b>ब्राउजरमा</b> खोल्नुहोस्।
         माथिको <b>⋮</b> मा थिचेर <b>“Open in browser”</b> रोज्नुहोस्, वा फाइल सेभ गरेर
         Chrome अथवा Safari बाट खोल्नुहोस्। यो एप चल्न JavaScript चाहिन्छ।</p>
      <p lang="hi"><b>हिन्दी:</b> कृपया इस फ़ाइल को <b>ब्राउज़र में</b> खोलें।
         ऊपर <b>⋮</b> दबाकर <b>“Open in browser”</b> चुनें, या फ़ाइल सेव करके
         Chrome या Safari से खोलें। इस ऐप को चलने के लिए JavaScript आवश्यक है।</p>
    </div>
  </noscript>
</div>

<footer>
  <div id="appFooter">ॐ · A study edition of the Bhagavad Gita — every verse shown in its traditional four quarters (pādas), with Sanskrit, transliteration, word-by-word meanings, a literal translation and a flowing paraphrase.</div>
  <!-- Credit lives in its own element: applyStatic() replaces #appFooter's
       textContent on every language switch and would otherwise wipe it. -->
  <div class="credit">Created by <b>Dhruba Chapain</b>, Pokhara, Nepal.</div>
  <!-- OFL clause 2 asks that the copyright notice travel with the font. It is
       preserved inside the embedded woff2 metadata, but a reader cannot
       "easily view" that, so it is stated here in the page as well. -->
  <div class="credit attrib">Sanskrit text of the Bhagavad Gītā: public domain.
    Translations, word meanings and commentary &copy; 2026 Dhruba Chapain.
    Typeface: Noto Serif Devanagari, &copy; 2022 The Noto Project Authors,
    <a href="https://openfontlicense.org" target="_blank" rel="noopener">SIL Open Font License 1.1</a>.</div>
</footer>

<div class="modal-bg" id="modalBg" onclick="if(event.target===this)closeModal()">
  <div class="modal" id="modal"></div>
</div>

<script>
let DATA = null;
/* The verses arrive from data/ch<N>.js — one file per chapter, loaded by the
   script tags at the end of <body>. The loader assembles DATA and boots the
   app when the last one lands. */
const GITA_CH = {};
__DATALOADER__
const UI = __UI__;
const state = { chapter:null, theme:null, idx:0, lang:'en', view:'welcome', section:null, shared:null };
function T(o){ return o ? (o[state.lang] || o.en || o) : ''; }
function L(k){ const u = UI[state.lang] || UI.en; return (u[k] !== undefined) ? u[k] : k; }
function Lof(cur,tot){ const rev=['ne','hi'].includes(state.lang);
  const c = numL(cur), t = numL(tot);   // numL → Devanagari digits in ne/hi
  return rev ? `${t} ${L('of')} ${c}` : `${c} ${L('of')} ${t}`; }
/* Inline stroke icons. Emoji in UI chrome render differently on every OS and
   read as dated; currentColor strokes match the type and follow both themes. */
const ICONS = {
  home:'<svg class="ic" viewBox="0 0 24 24"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/></svg>',
  star:'<svg class="ic" viewBox="0 0 24 24"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
  starF:'<svg class="ic fill" viewBox="0 0 24 24"><path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1-5.4-2.9-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
  shuffle:'<svg class="ic" viewBox="0 0 24 24"><path d="M16 3h5v5"/><path d="M21 3 4 20"/><path d="M21 16v5h-5"/><path d="m15 15 6 6"/><path d="m4 4 5 5"/></svg>',
  search:'<svg class="ic" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.8-3.8"/></svg>',
  moon:'<svg class="ic" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
  sun:'<svg class="ic" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M19.1 4.9l-1.8 1.8M6.7 17.3l-1.8 1.8"/></svg>',
  eye:'<svg class="ic" viewBox="0 0 24 24"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>',
  eyeOff:'<svg class="ic" viewBox="0 0 24 24"><path d="m3 3 18 18"/><path d="M10.6 5.1A11 11 0 0 1 12 5c6.5 0 10 7 10 7a17.7 17.7 0 0 1-3 3.9M6.6 6.6A16.8 16.8 0 0 0 2 12s3.5 7 10 7a10 10 0 0 0 4.4-1"/></svg>'
};
function applyStatic(){ $('#appTitle').textContent = L('app_title'); $('#appSub').textContent = L('app_sub');
  $('#tagVerses').textContent = L('tag_sub'); $('#appFooter').textContent = L('footer');
  $('#clearBtn').setAttribute('aria-label', L('clear'));
  $('#randLbl').textContent = L('random'); $('#favLbl').textContent = L('favorites');
  $('#homeLbl').textContent = L('home');
  $('#searchInput').placeholder = L('search_ph');
  { const pb = $('#playLbl'); if(pb) pb.textContent = L('play'); }
  searchX(); }
function setLang(l){ state.lang = l; try{ document.documentElement.lang = l; }catch(e){}
  document.querySelectorAll('.lang-btn').forEach(b=>b.classList.toggle('on', b.dataset.lang===l));
  applyStatic();
  // Remember which verse the modal is showing: doSearch()/showFavorites()
  // below null out state.chapter/state.theme while re-rendering the
  // background view, which would otherwise leave the open modal stale.
  const modalOpen = $('#modalBg').classList.contains('open');
  const mCh = state.chapter, mTh = state.theme, mIdx = state.idx;
  if(state.view === 'welcome'){ showWelcome(); }
  else if(state.view === 'sections'){ showSections(); }
  else if(state.view === 'search'){ doSearch(); }
  else if(state.view === 'favorites'){ showFavorites(); }
  else if(state.view === 'read'){ showRead(state.chapter, state.readMode); }
  /* The learn path renders its own views and holds drill state in module
     vars, so it must NOT fall through to the generic chapter/theme restore
     below: with state.theme set that lands on showVerses() and the reader's
     drill simply disappears mid-question. Re-enter at the path's home — the
     only place that can safely rebuild in the new language, since a
     half-answered question's options were built from the old strings.
     Progress is already saved. */
  else if(state.view === 'learn'){ lrRelang(state.chapter); }
  /* Play rebuilds the question it is showing, in the new language, rather than
     quitting the game: PL.q holds the verse and the option order, and only the
     prompt, the note and the numerals were language-bound. If no question is
     open, fall back to the menu. */
  else if(state.view === 'play'){ if(PL.q && PL.mode) plNext(PL.q); else showPlay(); }
  else {
    const ch = state.chapter, th = state.theme;
    if(ch == null){ if(state.section) showChapters(state.section); else showSections(); }
    else if(th == null) showThemes(ch);
    else { showVerses(ch, th); }
  }
  if(modalOpen && mCh != null && mTh != null){
    state.chapter = mCh; state.theme = mTh; state.idx = mIdx;
    fillModal();
  }
}
const $ = s => document.querySelector(s);
const crumbs = $('#crumbs'), view = $('#view');

// ---------- global verse index (search / favorites / random) ----------
const VERSES = [];
function buildIndex(){
  DATA.forEach((ch, ci)=> ch.themes.forEach((t, ti)=>{
    t.parts.forEach(p=> p.sutras.forEach((s, k)=> VERSES.push({ id:s.n, norm:fmtN(s.n), ci, ti, si:flatIndex(t,p,k) })));
  }));
}
function verseLoc(id){ return VERSES.find(v=>v.id===id); }
function verseAt(loc){ const t = DATA[loc.ci].themes[loc.ti]; return sutraAt(t, loc.si).s; }
function normTxt(s){ return String(s||'').toLowerCase().replace(/[\u0300-\u036f]/g,''); }
function fmtN(n){ const m = String(n).split('.'); return m.length===2 ? (parseInt(m[0],10)+'.'+parseInt(m[1],10)) : String(n); }
function fmtRange(r){ const parts = String(r).split(/[–-]/).map(x=>x.trim()?fmtN(x):x); return (parts.length===2 && parts[0]===parts[1]) ? parts[0] : parts.join('–'); }
function digitNorm(s){ return String(s).replace(/[०-९]/g, d => '0123456789'['०१२३४५६७८९'.indexOf(d)]); }
function devaDigits(s){ return String(s).replace(/[0-9]/g, d => '०१२३४५६७८९'[d]); }
function numL(n){ return (state.lang==='ne'||state.lang==='hi') ? devaDigits(n) : String(n); }
/* Display-only variants of fmtN / fmtRange: identical text, but with Devanagari
   digits in ne/hi. The plain fmtN/fmtRange stay ASCII because VERSES[].norm and
   the search matcher compare against them. */
function fmtNL(n){ return numL(fmtN(n)); }
function fmtRangeL(r){ return numL(fmtRange(r)); }
function vn2(n){ return fmtNL(n.split('.')[0] + '.' + parseInt(n.split('.')[1],10)); }
function chaptersRange(a, b){ return L('range_chapters').replace('{a}', numL(a)).replace('{b}', numL(b)); }
/* Meter badge, built at render time so it follows the language (and uses
   Devanagari digits in ne/hi). Falls back to the baked English string. */
function meterText(s){
  const m = s && s.mt;
  if(!m) return s ? s.meter : '';
  const bits = [];
  if(m.name){
    let nm = L(m.name === 'anustubh' ? 'meter_anustubh' : 'meter_trishtubh');
    if(m.irr) nm += ' (' + L('meter_irregular') + ')';
    bits.push(nm);
  }
  bits.push(L('meter_syllables').replace('{n}', numL(m.total)));
  bits.push(m.per
    ? L('meter_padas_of').replace('{n}', numL(m.n)).replace('{k}', numL(m.per))
    : L('meter_padas').replace('{n}', numL(m.n)));
  return bits.join(' · ');
}
function verseSearchText(v){
  return normTxt(v.n + ' ' + fmtN(v.n) + ' ' + v.d + ' ' + v.t + ' ' + v.lits.en + ' ' + v.lits.ne + ' ' + v.lits.hi
    + ' ' + v.paras.en + ' ' + v.paras.ne + ' ' + v.paras.hi + ' ' + T(v.lits));
}
const VERSE_TEXT = [];
function buildVerseText(){ DATA.forEach(ch=> ch.themes.forEach(t=> t.parts.forEach(p=> p.sutras.forEach(s=> VERSE_TEXT.push(verseSearchText(s)))))); }

// ---------- search ----------
let searchTimer = null;
function onSearchInput(v){ clearTimeout(searchTimer); searchTimer = setTimeout(doSearch, 220); searchX(); }
/* the in-field ✕ exists only while there is text to clear — the modern
   pattern; a standing "Clear" button was dead chrome on an empty field */
function searchX(){ const f = document.querySelector('.sw-field');
  if(f) f.classList.toggle('has-x', ($('#searchInput').value || '').length > 0); }
function doSearch(){
  const q = ($('#searchInput').value || '').trim();
  if(!q){ clearSearch(); return; }
  rememberOrigin();
  state.view = 'search'; state.chapter = null; state.theme = null; renderCrumbs();
  const nq = normTxt(q);
  /* Accept whatever separator the reader's keyboard gives. On a Devanagari
     layout the danda । sits where the full stop is, so १।१ is the natural way to
     type 1.1; also allow : - / , the double danda, and stray surrounding dandas. */
  const num = digitNorm(q).replace(/^[\s।॥]+|[\s।॥]+$/g, '')
                          .match(/^(\d{1,2})[.।॥:\-\/,\s]+(\d{1,2})$/);
  let hits;
  if(num){
    const target = parseInt(num[1],10) + '.' + parseInt(num[2],10);
    hits = VERSES.filter(loc => loc.norm === target);
    if(hits.length === 0){
      const c = parseInt(num[1],10), v = parseInt(num[2],10);
      let msg = '';
      if(c >= 1 && c <= 18){
        const cnt = DATA[c-1].verses;
        if(v < 1 || v > cnt) msg = L('oob_verse').replace('{ch}', numL(c)).replace('{n}', numL(cnt));
      } else {
        msg = L('oob_chapter');
      }
      if(msg){
        view.innerHTML = `<div class="res-head fade-in">${esc(L('search_results'))}</div>
          <div class="res-count fade-in">${numL(0)} ${esc(L('results'))}</div>
          <div class="view-sub fade-in">${esc(msg)}</div>`;
        return;
      }
    }
  } else {
    /* Free text. The index holds verse numbers as ASCII ("1.1"), so a query in
       Devanagari digits — १, १७ — has to be converted too, or typing १ finds
       nothing while 1 finds the whole chapter. Try both forms. */
    const nqd = normTxt(digitNorm(q).replace(/[।॥]/g, '.'));
    hits = [];
    VERSES.forEach((loc, i)=>{
      const t = VERSE_TEXT[i];
      if(t.includes(nq) || (nqd !== nq && t.includes(nqd))) hits.push(loc);
    });
  }
  if(hits.length === 0){
    view.innerHTML = `<div class="res-head fade-in">${esc(L('search_results'))}</div>
      <div class="res-count fade-in">${numL(0)} ${esc(L('results'))}</div>
      <div class="view-sub fade-in">${esc(L('no_results'))}</div>`;
    return;
  }
  SRCH_HITS = hits;
  view.innerHTML = `<div class="res-head fade-in">${esc(L('search_results'))}</div>
    <div class="res-count fade-in">${numL(hits.length)} ${esc(L('results'))}</div>
    <div class="grid verses fade-in">${hits.map((loc,i)=>{
      const ch = DATA[loc.ci], v = verseAt(loc);
      const th = ch.themes[loc.ti]; const part = sutraAt(th, loc.si).part;
      const pi = th.parts.indexOf(part);
      return `<div class="mini" role="button" tabindex="0" onclick="openModal(${loc.ci},${loc.ti},${loc.si},'search',${i})">
        <div class="vnum">${esc(L('verse'))} ${esc(fmtNL(v.n))}</div>
        <div class="m-topic"><span class="mt-lab">${esc(L('verse_topic'))}:</span> ${esc(T(part.titles))}</div>
        <div class="padas">${padaBlockDeva(v)}</div>
        <div class="vhint">${esc(T(v.paras).slice(0,80))}…</div>
      </div>`;}).join('')}</div>`;
}
function clearSearch(){
  $('#searchInput').value = '';
  searchX();
  goToOrigin();
}

// ---------- favorites (localStorage with in-memory fallback) ----------
let FAV = [], FAVNOTE = {};
// ---------- dark mode ----------
// The <head> script has already applied the theme. These functions handle the
// toggle, keep the button label and the browser chrome colour in step, and
// follow the phone's setting until the reader overrides it.
function themeIsDark(){ return document.documentElement.getAttribute('data-theme') === 'dark'; }
function paintTheme(){
  const dark = themeIsDark();
  const icon = $('#themeIcon'); if(icon) icon.innerHTML = dark ? ICONS.sun : ICONS.moon;
  const btn = $('#themeBtn');
  if(btn) btn.setAttribute('aria-label', dark ? L('theme_light') : L('theme_dark'));
  // colour the phone's status bar / address bar to match
  const mc = document.getElementById('themeColor');
  if(mc) mc.setAttribute('content', dark ? '#0E2A24' : '#1A5648');
}
function setTheme(dark, remember){
  if(dark) document.documentElement.setAttribute('data-theme','dark');
  else document.documentElement.removeAttribute('data-theme');
  if(remember){ try{ localStorage.setItem('gitaTheme', dark ? 'dark' : 'light'); }catch(e){} }
  paintTheme();
}
function toggleTheme(){ setTheme(!themeIsDark(), true); }
// If the reader has never chosen, keep following the phone as it changes
// (e.g. an automatic switch at sunset).
try{
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  const onSys = e => { let saved=null; try{ saved=localStorage.getItem('gitaTheme'); }catch(_){}
                       if(saved === null) setTheme(e.matches, false); };
  if(mq.addEventListener) mq.addEventListener('change', onSys);
  else if(mq.addListener) mq.addListener(onSys);
}catch(e){}

/* JSON.parse succeeding does NOT mean we got the shape we want: a stored
   'null', '5' or '{}' parses fine and then explodes on the first .indexOf /
   .includes — and FAV.includes() runs on every verse modal, so one bad write
   (a sync bug, a shared-device mishap, a hand-edited devtools value) would
   brick the app on every verse with no way back except clearing storage.
   Validate the TYPE, not just the parse, and fall back to empty. */
function favNoteLoad(){
  try{
    const o = JSON.parse(localStorage.getItem('gitaFavNotes') || '{}');
    if(!o || typeof o !== 'object' || Array.isArray(o)) return {};
    const out = {};
    for(const k in o) if(typeof o[k] === 'string') out[k] = o[k];
    return out;
  }catch(e){ return {}; }
}
function favNoteSave(){ try{ localStorage.setItem('gitaFavNotes', JSON.stringify(FAVNOTE)); }catch(e){} }
function favLoad(){
  try{
    const a = JSON.parse(localStorage.getItem('gitaFavs') || '[]');
    /* keep only well-formed verse ids, so a corrupt entry cannot poison the
       favourites list or render a broken card */
    return Array.isArray(a) ? a.filter(x => typeof x === 'string' && /^\d{1,2}\.\d{1,2}$/.test(x)) : [];
  }catch(e){ return []; }
}
FAV = favLoad(); FAVNOTE = favNoteLoad();
function favSave(){ try{ localStorage.setItem('gitaFavs', JSON.stringify(FAV)); }catch(e){} }
function toggleFav(id){
  const i = FAV.indexOf(id);
  if(i >= 0) FAV.splice(i,1); else FAV.push(id);
  favSave();
  const b = document.getElementById('favBtn');
  if(b){ const on = FAV.includes(id); b.innerHTML = (on ? ICONS.starF : ICONS.star) + esc(L(on ? 'saved_verse' : 'save_verse')); b.classList.toggle('saved', on); }
  if(state.view === 'favorites') showFavorites();
}
/* Search and Favorites are "detours": they replace the main view but the reader
   should still be able to get back to whatever they were reading. Before either
   takes over, remember the browsing position so renderCrumbs() can offer it as a
   real trail. Only recorded when leaving an actual browsing view, so repeatedly
   tapping Favorites doesn't overwrite the origin with itself. */
function rememberOrigin(){
  if(['welcome','sections','chapters','themes','verses'].includes(state.view)){
    state.origin = { view: state.view, section: state.section,
                     chapter: state.chapter, theme: state.theme };
  }
}
function goToOrigin(){
  const o = state.origin;
  if(!o){ showSections(); return; }
  $('#searchInput').value = '';
  if(o.view === 'welcome') showWelcome();
  else if(o.view === 'sections') showSections();
  else if(o.view === 'verses' && o.chapter != null && o.theme != null) showVerses(o.chapter, o.theme);
  else if(o.view === 'themes' && o.chapter != null) showThemes(o.chapter);
  else if(o.section != null) showChapters(o.section);
  else showSections();
}
function showFavorites(){
  rememberOrigin();
  state.view = 'favorites'; state.chapter = null; state.theme = null; renderCrumbs();
  const saved = FAV.map(verseLoc).filter(Boolean);
  FAV_LIST = saved;
  if(saved.length === 0){
    view.innerHTML = `<div class="res-head fade-in">${esc(L('favorites'))}</div>
      <div class="view-sub fade-in">${esc(L('no_favorites'))}</div>`;
    return;
  }
  view.innerHTML = `<div class="res-head fade-in">${esc(L('favorites'))}</div>
    <div class="res-count fade-in">${numL(saved.length)} ${esc(L('results'))}</div>
    ${saved.map((loc,i)=>{
      const ch = DATA[loc.ci], v = verseAt(loc);
      const note = FAVNOTE[v.n] || '';
      return `<div class="res-card" onclick="openModal(${loc.ci},${loc.ti},${loc.si},'fav',${i})">
        <div class="res-top"><span class="res-num">${esc(fmtNL(v.n))}</span><span class="res-title">${esc(T(ch.names))}</span>
        <span class="fav-tools" onclick="event.stopPropagation()">
          <button class="fav-move" onclick="moveFav(${i},-1)" ${i===0?'disabled':''} aria-label="up">${L('fav_up')}</button>
          <button class="fav-move" onclick="moveFav(${i},1)" ${i===saved.length-1?'disabled':''} aria-label="down">${L('fav_down')}</button>
          <button class="res-remove" onclick="removeFav('${esc(v.n)}')">${esc(L('remove_fav'))}</button>
        </span></div>
        <div class="res-deva">${padaBlockDeva(v)}</div>
        <div class="res-lit">${esc(T(v.lits))}</div>
        <div class="fav-note" onclick="event.stopPropagation()">
          <label>${esc(L('fav_note'))}</label>
          <textarea rows="1" placeholder="${esc(L('fav_note_ph'))}"
            oninput="this.style.height='auto';this.style.height=this.scrollHeight+'px'"
            onchange="setFavNote('${esc(v.n)}', this.value)">${esc(note)}</textarea>
        </div>
      </div>`;}).join('')}`;
  // grow each note box to fit what is already written
  view.querySelectorAll('.fav-note textarea').forEach(t=>{
    if(t.value){ t.style.height='auto'; t.style.height=t.scrollHeight+'px'; }
  });
}
function removeFav(id){
  const i = FAV.indexOf(id);
  if(i>=0){ FAV.splice(i,1); favSave(); }
  if(FAVNOTE[id]){ delete FAVNOTE[id]; favNoteSave(); }
  showFavorites();
}
/* Favourites are a personal collection, so the reader orders them and can say
   why a verse matters. Both are stored beside the list itself. */
function moveFav(i, d){
  const j = i + d;
  if(j < 0 || j >= FAV.length) return;
  [FAV[i], FAV[j]] = [FAV[j], FAV[i]];
  favSave(); showFavorites();
}
function setFavNote(id, text){
  text = (text||'').trim();
  if(text) FAVNOTE[id] = text; else delete FAVNOTE[id];
  favNoteSave();
}

// ---------- random verse ----------
function randomVerse(){
  const v = VERSES[Math.floor(Math.random()*VERSES.length)];
  openModal(v.ci, v.ti, v.si, 'random');
}

function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function vCount(t){ return t.parts.reduce((a,p)=>a+p.sutras.length,0); }

function crumb(label, action, isLast){
  const b = document.createElement('button'); b.textContent = label;
  // Long chapter names are truncated with CSS; keep the full text available as a
  // tooltip on hover and to screen readers. Truncation is visual only.
  b.title = label; b.setAttribute('aria-label', label);
  if(isLast){ b.className='cur'; b.disabled=true; } else b.onclick = action;
  return b;
}
/* On phones the header scrolls away, so a deeper view would otherwise open
   mid-page. Jump to the top whenever we actually move to a different view. */
let LAST_VIEW_SIG = null;
function scrollViewTop(){
  const sig = [state.view, state.section, state.chapter, state.theme].join('|');
  if(sig === LAST_VIEW_SIG) return;
  LAST_VIEW_SIG = sig;
  announceView();
  if(state.keepScroll) return;
  try{ window.scrollTo({top:0, behavior:'auto'}); }catch(e){ window.scrollTo(0,0); }
}
/* Speak the new view to screen readers. This app never navigates, so the only
   signal a non-sighted reader gets is this live region — the same signature
   scrollViewTop already dedupes on, so it fires exactly once per real change
   and stays silent when a re-render lands on the same place. */
function announceView(){
  const el = document.getElementById('srStatus');
  if(!el) return;
  let msg = '';
  try{
    const ch = (state.chapter != null && DATA[state.chapter]) ? DATA[state.chapter] : null;
    if(state.view === 'welcome')        msg = L('welcome_title');
    else if(state.view === 'search')    msg = L('search_results');
    else if(state.view === 'favorites') msg = L('favorites');
    else if(state.view === 'verses' && ch && state.theme != null)
      msg = `${L('chapter')} ${numL(ch.num)} · ${T(ch.themes[state.theme].titles)}`;
    else if(ch) msg = `${L('chapter')} ${numL(ch.num)} · ${T(ch.names)}`;
    else if(state.section) msg = L('sections_title');
  }catch(e){}
  if(msg) el.textContent = msg;
}
/* Search and Favorites are "detours" off the browsing hierarchy. Rather than a
   breadcrumb trail, they show a single back button naming the page the reader came
   from — the same control and wording as the app's "← Back to themes" / "← Back to
   chapters" buttons, so Favorites is not a special case. Nothing becomes
   unreachable: that destination carries its own back button, so the hierarchy is
   walked one level at a time. */
/* These lists run four to five screens on a phone, and the only way back used to
   be the crumb at the very top. backFoot() repeats that one button at the end —
   same destination, same wording, so there is nothing new to learn. */
function backFoot(onclick, label){
  return `<div class="back-foot"><button class="back-top" onclick="${onclick}">${esc(label)}</button></div>`;
}

/* Theme ranges arrive padded (2.01-2.03); humans read 2.1-2.3 (PROJECT.md).
   The builder has _drange() for the static pages; the app needs it at runtime. */
function _drangeJS(r){
  r = String(r||'');
  r = r.replace(/(\d+)\.0*(\d+)\s*[–-]\s*(\d+)\.0*(\d+)/g, function(m,a,b,c,d){
    const x = a+'.'+parseInt(b,10), y = c+'.'+parseInt(d,10);
    return x===y ? x : x+'–'+y;
  });
  return r.replace(/(\d+)\.0*(\d+)/g, function(m,a,b){ return a+'.'+parseInt(b,10); });
}

/* ==================== Learn by heart ==================== */
/* ---------------- progress ----------------
   One key for all 18 chapters. Hardened like the favourites: a parse that
   succeeds still has to yield the shape we expect, or one bad value would
   throw on every render with no way back but clearing site data. */
function lrAll(){
  try{
    const o = JSON.parse(localStorage.getItem('gitaLearn') || 'null');
    if(!o || typeof o !== 'object' || Array.isArray(o)) return {};
    const out = {};
    for(const k in o){
      if(!/^\d{1,2}$/.test(k)) continue;
      const c = o[k];
      if(!c || typeof c !== 'object' || Array.isArray(c)) continue;
      const th = {};
      if(c.themes && typeof c.themes === 'object' && !Array.isArray(c.themes))
        for(const t in c.themes) if(/^\d+$/.test(t) && c.themes[t] === 1) th[t] = 1;
      out[k] = {story: c.story === 1 ? 1 : 0, themes: th};
    }
    return out;
  }catch(e){ return {}; }
}
function lrGet(n){ const a = lrAll(); return a[n] || {story:0, themes:{}}; }
function lrPut(n, o){
  const a = lrAll(); a[n] = o;
  try{ localStorage.setItem('gitaLearn', JSON.stringify(a)); }catch(e){}
}
function lrReset(n){
  if(!confirm(L('learn_restart_q'))) return;
  const a = lrAll(); delete a[n];
  try{ localStorage.setItem('gitaLearn', JSON.stringify(a)); }catch(e){}
  showLearn(state.chapter);
}
function fmt(s, o){ return String(s).replace(/\{(\w+)\}/g, (m,k)=> k in o ? o[k] : m); }

const lrShuffle = a => { a = a.slice();
  for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a; };
const lrSample = (arr,n) => lrShuffle(arr).slice(0,n);
/* every verse of a theme, flattened — parts are one verse each now, but the
   container is still there, so never assume */
function thVerses(t){ const out=[]; t.parts.forEach(p=>p.sutras.forEach(s=>out.push(s))); return out; }

/* ---------------- the path ---------------- */
function showLearn(ci){
  rememberOrigin();
  state.view='learn'; state.chapter=ci; state.lrAt = null;
  state.section = state.section || Math.ceil(DATA[ci].num/6);
  state.theme=null; renderCrumbs();
  const ch = DATA[ci], p = lrGet(ch.num);
  const total = ch.themes.length, done = Object.keys(p.themes).length;
  const pct = Math.round((p.story + done) / (1 + total) * 100);

  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'),'showSections()'],
      [wayName(Math.ceil(ch.num/6)), `showChapters(${Math.ceil(ch.num/6)})`],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, null]])}
    ${chTitle(ch)}
    ${modeSwitch(ci)}
    <div class="lrn fade-in">
      <div class="view-sub">${esc(fmt(L('learn_sub'),{}))}</div>
      <div class="lr-prog"><i style="width:${pct}%"></i></div>
      <div class="lr-progl">${esc(fmt(L('learn_walked'),{p:numL(pct)}))}</div>

      <div class="lr-step ${p.story?'done':'now'}">
        <div class="lr-badge">${p.story?'✓':numL(1)}</div>
        <div class="lr-body">
          <h3>${esc(L('learn_s1'))}</h3>
          <p>${esc(fmt(L('learn_s1_d'),{n:numL(total)}))}</p>
          <button class="lr-cta" onclick="lrStory(${ci},0)">
            ${esc(p.story?L('learn_again'):L('learn_begin'))}</button>
        </div>
      </div>

      <div class="lr-step ${p.story?(done===total?'done':'now'):'locked'}">
        <div class="lr-badge">${(p.story&&done===total)?'✓':numL(2)}</div>
        <div class="lr-body">
          <h3>${esc(L('learn_s2'))}</h3>
          <p>${p.story ? esc(fmt(L('learn_s2_d'),{a:numL(done),b:numL(total)}))
                       : esc(L('learn_s2_locked'))}</p>
          ${p.story ? `<div class="lr-grid">${ch.themes.map((t,ti)=>`
            <button class="lr-chip${p.themes[ti]?' ok':''}" onclick="lrTheme(${ci},${ti},0)">
              <span class="n">${p.themes[ti]?'✓':numL(ti+1)}</span>
              <span class="t">${esc(T(t.titles))}</span>
              <span class="v">${numL(vCount(t))}</span>
            </button>`).join('')}</div>`
          : `<button class="lr-ghost" onclick="lrSkip(${ci})">${esc(L('learn_skip'))}</button>`}
        </div>
      </div>

      <div class="lr-foot">
        <span>${esc(L('learn_local'))}</span>
        ${(p.story||done)?`<button class="lr-ghost sm" onclick="lrReset(${ch.num})">${esc(L('learn_restart'))}</button>`:''}
      </div>
    </div>` + backFoot(`showChapters(${state.section||0})`, L('back_chapters'));
  scrollViewTop();
}
/* Re-enter the learn path in the new language, as near as possible to where
   the reader was. The current QUESTION is unrecoverable — it was generated
   from the old language's strings — but the theme or the story step is not,
   so restart that rather than the whole chapter. */
function lrRelang(ci){
  const at = state.lrAt;
  if(at && at.kind === 'theme' && DATA[ci] && DATA[ci].themes[at.ti]) return lrTheme(ci, at.ti, 0);
  if(at && at.kind === 'story') return lrStory(ci, 0);
  showLearn(ci);
}
function lrSkip(ci){ const n=DATA[ci].num, p=lrGet(n); p.story=1; lrPut(n,p); showLearn(ci); }

/* ---------------- stage 1: the story ----------------
   Small chapters get read -> whole chain. Larger ones earn the middle two
   steps; drilling four stages over six themes is ceremony, not teaching. */
function lrPlan(ch){ return ch.themes.length >= 10 ? [0,1,2,3] : [0,3]; }

function lrStory(ci, step){
  state.view='learn'; state.chapter=ci; state.theme=null;
  state.lrAt = {kind:'story', step:step};
  const ch = DATA[ci], th = ch.themes, plan = lrPlan(ch);
  const k = plan.indexOf(step), n = plan.length;
  if(step === 0) return lrStoryRead(ci, ch, th, k+1, n);

  let items;
  if(step === 1){
    const groups = [];
    for(let i=0;i<th.length;i+=4) groups.push(th.slice(i,i+4).map((t,j)=>({t,i:i+j})));
    items = groups.filter(g=>g.length>1).map(g=>({kind:'order',
      ask: esc(fmt(L('learn_order_few'),{n:numL(g.length)})),
      chips: g.map(x=>({id:x.i, label:T(x.t.titles)})),
      answer: g.map(x=>x.i)}));
  } else if(step === 2){
    items = th.slice(0,-1).map((t,i)=>{
      const right = th[i+1];
      const wrong = lrSample(th.filter((_,j)=>j!==i+1&&j!==i), 3);
      return {kind:'pick',
        ask: esc(fmt(L('learn_after'),{t:T(t.titles)})),
        opts: lrShuffle([right,...wrong]).map(x=>({label:T(x.titles), ok:x===right})),
        note: esc(T(right.descs))};
    });
  } else {
    items = [{kind:'order',
      ask: esc(fmt(L('learn_order_all'),{n:numL(th.length)})),
      chips: th.map((t,i)=>({id:i, label:T(t.titles)})),
      answer: th.map((_,i)=>i)}];
  }
  const nxt = plan[k+1];
  lrRun(ci, items, fmt(L('learn_step'),{a:numL(k+1),b:numL(n)}),
    nxt === undefined ? ()=>lrStoryDone(ci) : ()=>lrStory(ci, nxt));
}

function lrStoryRead(ci, ch, th, k, n){
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'),'showSections()'],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, `showLearn(${ci})`],
      [L('learn_s1'), null]])}
    <div class="lrn fade-in">
      <div class="lr-k">${esc(fmt(L('learn_step'),{a:numL(k),b:numL(n)}))}</div>
      <h2 class="view-title">${esc(fmt(L('learn_read_h'),{n:numL(ch.num)}))}</h2>
      <div class="view-sub">${esc(L('learn_read_d'))}</div>
      <ol class="lr-thread">${th.map((t,i)=>`
        <li><span class="bead">${numL(i+1)}</span>
          <div><b>${esc(T(t.titles))}</b>
            <span class="rg">${esc(_drangeJS(t.range))}</span>
            <p>${esc(T(t.descs))}</p></div></li>`).join('')}</ol>
      <div class="lr-nav">
        <button class="lr-cta" onclick="lrStory(${ci},${lrPlan(ch)[1]})">${esc(L('learn_read_go'))}</button>
      </div>
    </div>` + backFoot(`showRead(${ci},'full')`, L('back_chapter_one'));
  scrollViewTop();
}
function lrStoryDone(ci){
  const ch = DATA[ci], p = lrGet(ch.num); p.story = 1; lrPut(ch.num, p);
  view.innerHTML = `<div class="lrn fade-in"><div class="lr-finis">
      <div class="lr-seal">✓</div>
      <h2>${esc(fmt(L('learn_story_done'),{n:numL(ch.num)}))}</h2>
      <p>${esc(L('learn_story_done_d'))}</p>
      <button class="lr-cta" onclick="showLearn(${ci})">${esc(L('learn_to_verses'))}</button>
    </div></div>`;
  scrollViewTop();
}

/* ---------------- stage 2: the verses of one theme ---------------- */
function lrTheme(ci, ti, k){
  state.view='learn'; state.chapter=ci; state.theme=ti;
  /* Remember the sub-view. A language switch cannot re-render a half-answered
     question — its options were built from the old language's strings — but it
     CAN put the reader back at the top of the same theme rather than at the
     chapter's path home, which is a far shorter walk back. */
  state.lrAt = {kind:'theme', ti:ti};
  const ch = DATA[ci], t = ch.themes[ti], vs = thVerses(t);
  if(k < vs.length) return lrMeet(ci, ti, k, vs);
  lrDrill(ci, ti, vs);
}
function lrMeet(ci, ti, k, vs){
  const ch = DATA[ci], t = ch.themes[ti], s = vs[k], last = k === vs.length-1;
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'),'showSections()'],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, `showLearn(${ci})`],
      [T(t.titles), null]])}
    <div class="lrn fade-in">
      <div class="lr-k">${esc(L('learn_meet'))} · ${numL(k+1)} / ${numL(vs.length)}</div>
      <h2 class="view-title">${esc(T(t.titles))}</h2>
      <div class="lr-vnum">${esc(fmtNL(s.n))}</div>
      <div class="lr-quarters">${(s.flow||[]).filter(f=>f.k==='p').map((q,qi)=>`
        <div class="lr-q" id="lrq${qi}">
          <button class="lr-qh" onclick="lrTog(${qi})" aria-expanded="false" aria-controls="lrw${qi}">
            <span class="pip">${numL(qi+1)}</span>
            <span class="tx"><span class="dv" lang="sa">${q.d}</span>
              <span class="ia" lang="sa-Latn">${esc(q.t)}</span></span>
            <span class="chev">▾</span>
          </button>
          <div class="lr-words" id="lrw${qi}" hidden>${(q.words||[]).map(w=>`
            <div class="lr-word">
              <span class="d" lang="sa">${w[0]}</span>
              <span class="i" lang="sa-Latn">${esc(w[1])}</span>
              <span class="m">${esc(state.lang==='ne'?(w[3]||w[2]):state.lang==='hi'?(w[4]||w[2]):w[2])}</span>
            </div>`).join('')}</div>
        </div>`).join('')}</div>
      <div class="lr-mean"><span class="lb">${esc(L('in_other_words'))}</span>
        <div>${esc(T(s.paras))}</div></div>
      <div class="lr-nav">
        <button class="lr-ghost" onclick="lrTheme(${ci},${ti},${k-1})" ${k?'':'disabled'}>${esc(L('previous'))}</button>
        <span class="lr-hint">${esc(L('learn_meet_hint'))}</span>
        <button class="lr-cta" onclick="lrTheme(${ci},${ti},${k+1})">
          ${esc(last?L('learn_recall'):L('learn_next_verse'))}</button>
      </div>
    </div>` + backFoot(`showRead(${ci},'full')`, L('back_chapter_one'));
  scrollViewTop();
}
function lrTog(i){
  const box = document.getElementById('lrq'+i), w = document.getElementById('lrw'+i);
  if(!box||!w) return;
  const open = box.classList.toggle('open');
  w.hidden = !open;
  const b = box.querySelector('.lr-qh'); if(b) b.setAttribute('aria-expanded', open);
}

/* Is a word worth blanking? Judge the gloss by its CONTENT word: an early
   filter on /^(the|of|and)/ threw away "of all sacrifices" and "the great
   elements" — the best words in those verses — leaving four verses in the
   Gita with no cloze at all. */
function lrMeaty(w){
  if(!w || !w[0] || !w[2]) return false;
  if(w[0].length < 4) return false;
  const core = String(w[2]).replace(/^(?:the|of|a|an|to|in|by|for|from|with|O)\s+/i,'').trim();
  if(core.length < 4) return false;
  return !/^(and|but|indeed|also|too|not|even|alone|thus|so)$/i.test(core);
}
function lrDrill(ci, ti, vs){
  const ch = DATA[ci], t = ch.themes[ti];
  const pool = [], others = [];
  ch.themes.forEach(x=>thVerses(x).forEach(s=>{
    others.push(s);
    (s.flow||[]).forEach(f=>(f.words||[]).forEach(w=>{ if(lrMeaty(w)) pool.push(w); }));
  }));
  const items = [];
  vs.forEach(s=>{
    /* meaning -> verse. Distractors come from the same CHAPTER so the choice
       turns on what the verse says, not on which line looks unfamiliar. */
    /* Options are shown as the verse's FIRST PADA, so a distractor whose first
       pada is identical to the answer would render two indistinguishable
       choices with one marked wrong. 6.15 and 6.28 open with the same line
       (युञ्जन्नेवं सदात्मानं) — rare, but it must never happen. */
    /* Options are WHOLE VERSES, not opening lines — a first pāda is not a
       verse, and picking between four fragments is a shallower task than
       picking between four ślokas (owner 2026-09-01). Full verses are also
       unique book-wide, where four pairs share a first pāda. */
    const _full = v => v.d;
    const mine = _full(s);
    const wrong = lrSample(others.filter(o=>o.n!==s.n && _full(o)!==mine), 3);
    items.push({kind:'pick',
      ask: esc(L('learn_which')) + `<div class="lr-qsub">${esc(T(s.paras))}</div>`,
      opts: lrShuffle([s].concat(wrong)).map(o=>
        ({label: _full(o), sub: fmtNL(o.n), deva:1, ok:o===s})),
      note: `${esc(fmtNL(s.n))} — ${esc(T(s.lits))}`});

    /* Cloze on the AUTHORED WORD-SPLIT, never by blanking the recited line.
       Sanskrit sandhi means the dictionary form usually does NOT appear
       literally in the pada: पश्य + एताम् fuses to पश्यैतां, महतीम् is written
       महतीं, and उभयोः surfaces inside सेनयोरुभयोर्. A .replace() on the line
       missed 52% of words and failed SILENTLY — the line rendered intact, so
       the question read "which word is missing?" with nothing missing and
       every option equally arbitrary (owner hit this at 1.3, 2026-09-01).
       The word-split is authored data and always correct: hide a word THERE,
       and show the recited line beneath as the cue that ties it back. */
    const qs = (s.flow||[]).filter(f=>f.k==='p');
    const cands = [];
    qs.forEach(function(q,qi){
      const ws = q.words||[];
      if(ws.length < 2) return;                    // nothing to hide it among
      ws.forEach(function(w,wi){ if(lrMeaty(w)) cands.push({q:q,qi:qi,w:w,wi:wi,ws:ws}); });
    });
    if(cands.length){
      const c = cands[Math.floor(Math.random()*cands.length)];
      const split = c.ws.map(function(w,i){ return i===c.wi
        ? '<span class="lr-blank">?</span>'
        : '<span class="lr-tok">'+w[0]+'</span>'; }).join('<span class="lr-plus">+</span>');
      /* Distractors must be wrong AND non-obvious. Three separate traps:
         - same surface form as the answer, or same meaning -> not a distractor
         - a form ALREADY VISIBLE in the split is eliminable at a glance, so it
           silently makes the question easier (2.4% of questions before this)
         - two distractors identical to each other renders the same option
           twice (0.7% before this) — which looks like a bug, and is one */
      const shownForms = {};
      c.ws.forEach(function(x){ shownForms[x[0]] = 1; });
      const seenOpt = {};
      seenOpt[c.w[0]] = 1;
      const dw = [];
      lrShuffle(pool).forEach(function(x){
        if(dw.length >= 3) return;
        if(x[2] === c.w[2]) return;          // same meaning
        if(shownForms[x[0]]) return;         // already on screen
        if(seenOpt[x[0]]) return;            // duplicate option
        seenOpt[x[0]] = 1; dw.push(x);
      });
      items.push({kind:'pick',
        ask: esc(fmt(L('learn_missing'),{q:numL(c.qi+1), v:fmtNL(s.n)}))
             /* NO recited-line cue. It was added to help where sandhi
                transforms a word, but measured against the real data it gives
                the answer away in 6,069 of 6,394 questions — either literally
                (मामकाः inside मामकाः पाण्डवाश्चैव) or all but a letter
                (कुर्वत inside किमकुर्वत). Only 325 would keep a cue that
                genuinely helps, which is not worth a 95% leak.
                The surrounding words of the split ARE the context: supplying
                the missing word of a pāda you know is exactly the recall being
                tested (owner caught both leaks, 2026-09-01). */
             + `<div class="lr-split" lang="sa">${split}</div>`,
        opts: lrShuffle([c.w].concat(dw)).map(function(o){
                return {label:o[0], sub:o[1], deva:1, ok:o===c.w}; }),
        note: `<b lang="sa">${esc(c.w[0])}</b> (${esc(c.w[1])}) — ${esc(c.w[2])}`});
    }
  });
  /* Reorder the verses of the theme. The chip must NOT carry the verse number:
     printing "1.1 / 1.2 / 1.3" turns recall into sorting integers, which tests
     nothing (owner spotted this at ch1.t1, 2026-09-01). The paraphrase alone is
     the cue — verified unique across all 700 verses at this length. */
  if(vs.length > 1) items.push({kind:'order',
    ask: esc(fmt(L('learn_vorder'),{t:T(t.titles)})),
    chips: vs.map((s,i)=>({id:i, label: T(s.paras).slice(0, 64) + '…'})),
    answer: vs.map((_,i)=>i)});

  /* Reorder the four quarters — for EVERY verse of the theme, not a sample.
     Every verse in the Gītā has exactly four, all textually distinct, so the
     drill is always fair, and putting a śloka back together pāda by pāda is
     how it is actually committed to memory. Doing one verse per theme left
     478 of the 700 never practised this way (owner 2026-09-01). */
  vs.forEach(qv=>{
    const qq = (qv.flow||[]).filter(f=>f.k==='p');
    if(qq.length > 2) items.push({kind:'order',
      ask: esc(fmt(L('learn_qorder'),{v:fmtNL(qv.n)})),
      chips: qq.map((q,i)=>({id:i, label:q.d, deva:1})),
      answer: qq.map((_,i)=>i)});
  });

  lrRun(ci, lrShuffle(items), T(t.titles), ()=>{
    const p = lrGet(ch.num); p.themes[ti] = 1; lrPut(ch.num, p);
    const nxt = ch.themes.findIndex((_,i)=>!lrGet(ch.num).themes[i]);
    view.innerHTML = `<div class="lrn fade-in"><div class="lr-finis">
        <div class="lr-seal">✓</div>
        <h2>${esc(T(t.titles))}</h2>
        <p>${esc(fmt(L('learn_theme_done_d'),{n:numL(vs.length)+' '+(vs.length===1?L('verse'):L('verses'))}))}</p>
        ${nxt>=0 ? `<button class="lr-cta" onclick="lrTheme(${ci},${nxt},0)">${esc(L('learn_next_theme'))}</button>`
                 : `<p class="lr-all">${esc(fmt(L('learn_all_done'),{n:numL(ch.num)}))}</p>`}
        <button class="lr-ghost" onclick="lrFree(${ci},${ti})">${esc(L('learn_free_go'))}</button>
        <button class="lr-ghost" onclick="showRead(${ci},'full')">${esc(L('back_chapter_one'))}</button>
      </div></div>`;
    scrollViewTop();
  });
}

/* ---------------- free practice ----------------
   After a theme is held, the reader may keep going for as long as they like:
   one verse from this theme with its four pādas shuffled, reorder, then pull
   another. Deliberately OUTSIDE the queue engine — nothing is scored, nothing
   is required, and leaving costs nothing. Practice, not examination. */
var FP = {ci:0, ti:0, v:null, order:[], deal:[], picked:[]};
function lrFree(ci, ti){
  state.view='learn'; state.chapter=ci; state.theme=ti;
  state.lrAt = {kind:'theme', ti:ti};
  FP.ci = ci; FP.ti = ti;
  lrFreePick();
}
function lrFreePick(){
  const ch = DATA[FP.ci], t = ch.themes[FP.ti], vs = thVerses(t);
  /* avoid handing back the same verse twice running when the theme has
     more than one to choose from */
  let v = vs[Math.floor(Math.random()*vs.length)];
  if(vs.length > 1 && FP.v){
    let guard = 0;
    while(v.n === FP.v.n && guard++ < 12) v = vs[Math.floor(Math.random()*vs.length)];
  }
  FP.v = v; FP.picked = [];
  FP.order = (v.flow||[]).filter(f=>f.k==='p');
  /* The pādas must appear SHUFFLED or there is nothing to put in order — they
     were rendering in their natural sequence, which made the whole mode a
     no-op (owner 2026-09-01). Shuffle a display order ONCE per verse and keep
     it in state: reshuffling inside the paint would move the chips on every
     tap. Guard against the identity permutation, which would look like the
     bug even though the code was right. */
  const n = FP.order.length;
  let deal = FP.order.map((_,i)=>i);
  for(let guard=0; guard<20; guard++){
    deal = lrShuffle(FP.order.map((_,i)=>i));
    if(n < 2 || deal.some((ix,k)=>ix!==k)) break;
  }
  FP.deal = deal;
  lrFreePaint();
}
function lrFreePaint(){
  const ch = DATA[FP.ci], t = ch.themes[FP.ti], v = FP.v;
  const done = FP.picked.length === FP.order.length;
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'),'showSections()'],
      [`${L('chapter')} ${numL(ch.num)} · ${L('opt_learn_g')}`, `showLearn(${FP.ci})`],
      [T(t.titles), null]])}
    <div class="lrn fade-in">
      <div class="lr-k">${esc(L('learn_free'))}</div>
      <h2 class="view-title">${esc(T(t.titles))}</h2>
      <div class="view-sub">${esc(L('learn_free_d'))}</div>
      <div class="lr-qbox">
        <div class="lr-ask">${esc(fmt(L('learn_qorder'),{v:fmtNL(v.n)}))}</div>
        <div class="lr-slots" id="fpSlots">${FP.picked.map((ix,k)=>
          `<span class="lr-slot dv" lang="sa">${numL(k+1)}. ${esc(FP.order[ix].d)}</span>`).join('')}</div>
        <div class="lr-chips" id="fpChips">${(FP.deal||FP.order.map((_,i)=>i)).map(ix=>
          FP.picked.indexOf(ix) >= 0 ? '' :
          `<button class="lr-chip2 dv" lang="sa" onclick="lrFreeTap(${ix})">${esc(FP.order[ix].d)}</button>`
        ).join('')}</div>
        <div class="lr-fb" id="fpFb">${done
          ? `<div class="good">${esc(L('learn_thread_ok'))}</div>
             <div class="lr-cue" lang="sa-Latn">${esc(v.t)}</div>`
          : ''}</div>
      </div>
      <div class="lr-nav">
        <button class="lr-cta" onclick="lrFreePick()">${esc(L('learn_shuffle'))}</button>
        <span class="lr-hint">${esc(fmtNL(v.n))}</span>
        <button class="lr-ghost" onclick="showRead(${FP.ci},'full')">${esc(L('learn_done_free'))}</button>
      </div>
    </div>` + backFoot(`showRead(${FP.ci},'full')`, L('back_chapter_one'));
  scrollViewTop();
}
function lrFreeTap(i){
  const want = FP.picked.length;               // the next pāda in true order
  if(i === want){
    FP.picked.push(i);
    lrFreePaint();
  }else{
    /* wrong pāda: shake the chip, say which one comes next, and let them try
       again. No score, no penalty — this is the mode for playing. */
    const btns = document.querySelectorAll('#fpChips .lr-chip2');
    btns.forEach(b=>{ if(b.getAttribute('onclick') === 'lrFreeTap(' + i + ')'){
      b.classList.add('shake'); setTimeout(()=>b.classList.remove('shake'), 380); }});
    const fb = document.getElementById('fpFb');
    if(fb) fb.innerHTML = `<div class="bad">${esc(L('learn_nextis'))} ` +
      `<b class="dv" lang="sa">${esc(FP.order[want].d)}</b></div>`;
  }
}

/* ---------------- Play ----------------
   A front door onto the drill engine that needs no path, no progress and no
   commitment: open it from the tool row at any time, pick a scope and a mode,
   and answer as long as you like. Deliberately UNSCORED and unsaved — Learn by
   heart is the path with gating and progress; Play is the shuffle you drop
   into. If Play started tracking progress the two would blur (owner 2026-09-01).
   Everything here reuses lrRun/lrPaint/lrPick/lrChip. */
var PL = {scope:'all', ch:0, mode:0, run:0, q:null};

function showPlay(){
  rememberOrigin();
  state.view='play'; state.chapter=null; state.theme=null; renderCrumbs();
  view.innerHTML = `
    <div class="lrn fade-in">
      <h2 class="view-title">${esc(L('play_title'))}</h2>
      <div class="view-sub">${esc(L('play_sub'))}</div>

      <div class="pl-scope">
        <span class="pl-lb">${esc(L('play_scope'))}</span>
        <button class="lr-ghost${PL.scope==='all'?' on':''}" onclick="plScope('all')">${esc(L('play_all'))}</button>
        <button class="lr-ghost${PL.scope==='ch'?' on':''}" onclick="plScope('ch')">${esc(L('play_ch'))}</button>
        ${PL.scope==='ch' ? `<select class="pl-sel" onchange="PL.ch=+this.value;showPlay()">
            ${DATA.map((c,i)=>`<option value="${i}"${i===PL.ch?' selected':''}>${esc(L('chapter'))} ${numL(c.num)} · ${esc(T(c.names))}</option>`).join('')}
          </select>` : ''}
      </div>

      <div class="pl-modes">
        ${[[1,'play_m1','play_m1_d'],[2,'play_m2','play_m2_d'],[3,'play_m3','play_m3_d']].map(([m,t,d])=>`
          <button class="pl-mode" onclick="plStart(${m})">
            <span class="n">${numL(m)}</span>
            <span class="b"><b>${esc(L(t))}</b><span>${esc(L(d))}</span></span>
          </button>`).join('')}
      </div>
    </div>` + backFoot('showWelcome()', L('home_plain'));
  scrollViewTop();
}
function plScope(s){ PL.scope = s; showPlay(); }

/* The pool Play draws from: the whole book, or one chapter. */
function plPool(){
  const out = [];
  DATA.forEach((c,ci)=>{
    if(PL.scope === 'ch' && ci !== PL.ch) return;
    c.themes.forEach(t=>thVerses(t).forEach(s=>out.push(s)));
  });
  return out;
}
/* An option is a WHOLE VERSE, never its opening line: a first pāda is not a
   verse, and choosing between four fragments is a different (easier, shallower)
   task than choosing between four ślokas — owner 2026-09-01.
   A welcome consequence: full verses are unique book-wide (verified across all
   700), whereas four PAIRS share a first pāda — 3.35/18.47, 6.15/6.28,
   9.34/18.65, 16.07/18.30 — so the identical-option guard that case needed is
   no longer required. It stays as an assertion in the health checks. */
const plFull = v => v.d;

function plStart(mode){
  PL.mode = mode; PL.run = 0; PL.q = null;
  plNext();
}
/* One question at a time, drawn fresh — an endless game, not a finite queue. */
function plNext(keep){
  const pool = plPool();
  if(pool.length < 4){ showPlay(); return; }
  /* `keep` rebuilds the question that is already on screen — used when the
     reader switches language mid-game. Only the ASK, the NOTE and the numerals
     are language-bound; the verses and pādas are Devanagari either way, so the
     question is fully derivable from the verse id plus the option order we
     stored. Quitting to the menu for a language change was needless
     (owner 2026-09-02). */
  const s = keep ? (pool.find(v=>v.n === keep.n) || pool[Math.floor(Math.random()*pool.length)])
                 : pool[Math.floor(Math.random()*pool.length)];
  let item;

  if(PL.mode === 1){
    /* Given the number, choose the verse. Distractors must not share the
       answer's opening line: four verse PAIRS in the Gita open identically
       (3.35/18.47, 6.15/6.28, 9.34/18.65, 16.07/18.30), which would render two
       indistinguishable options with one marked wrong. */
    const mine = plFull(s);
    const ordered = keep ? keep.ord.map(n=>pool.find(v=>v.n===n)).filter(Boolean)
                         : null;
    const four = (ordered && ordered.length===4) ? ordered
               : lrShuffle([s].concat(lrSample(pool.filter(o=>o.n!==s.n && plFull(o)!==mine), 3)));
    PL.q = {n:s.n, ord:four.map(o=>o.n)};
    item = {kind:'pick',
      ask: esc(fmt(L('play_q1'),{v:fmtNL(s.n)})),
      opts: four.map(o=>({label:plFull(o), deva:1, ok:o===s})),
      note: `${esc(fmtNL(s.n))} — ${esc(T(s.lits))}`};

  }else if(PL.mode === 2){
    /* Given the verse, choose its number. Distractors are NEAR MISSES from the
       same chapter — random numbers from elsewhere would be given away by
       chapter recognition alone, testing nothing. */
    const same = pool.filter(o=>o.n.split('.')[0] === s.n.split('.')[0] && o.n !== s.n);
    const near = same.sort((a,b)=>
      Math.abs(parseInt(a.n.split('.')[1],10) - parseInt(s.n.split('.')[1],10)) -
      Math.abs(parseInt(b.n.split('.')[1],10) - parseInt(s.n.split('.')[1],10))).slice(0,6);
    const ordered2 = keep ? keep.ord.map(n=>pool.find(v=>v.n===n)).filter(Boolean) : null;
    const four2 = (ordered2 && ordered2.length===4) ? ordered2
                : lrShuffle([s].concat(lrSample(near.length >= 3 ? near : pool.filter(o=>o.n!==s.n), 3)));
    PL.q = {n:s.n, ord:four2.map(o=>o.n)};
    item = {kind:'pick',
      ask: esc(L('play_q2')) + `<div class="lr-qsub dv" lang="sa">${s.d}</div>`,
      opts: four2.map(o=>({label:fmtNL(o.n), ok:o===s})),
      note: `${esc(fmtNL(s.n))} — ${esc(T(s.lits))}`};

  }else{
    const qq = (s.flow||[]).filter(f=>f.k==='p');
    PL.q = {n:s.n, ord:[]};
    item = {kind:'order',
      ask: esc(fmt(L('learn_qorder'),{v:fmtNL(s.n)})),
      chips: qq.map((q,i)=>({id:i, label:q.d, deva:1})),
      answer: qq.map((_,i)=>i)};
  }
  /* A one-item run: when it finishes, deal another. That is the endless game. */
  lrRun(0, [item], L('play_title') + (PL.run ? ' · ' + fmt(L('play_round'),{n:numL(PL.run)}) : ''),
        ()=>{ PL.run++; plNext(); },
        {fn:'showPlay()', label:'play_title'});
}

/* ---------------- the drill engine ----------------
   One queue. A miss is not a failure: it goes to the back and comes round
   again, and the run ends only when the queue is genuinely empty. */
var LQ=[], LQi=0, LQmiss=0, LQdone=null, LQlab='', LQpick=[], LQci=0;
/* Where the queue's footer should lead. The learn path is inside a chapter;
   Play is not — it passed ci=0 and so offered "back to chapter", which sent the
   reader to chapter 1 from a game that spans the whole Gītā (owner
   2026-09-01). */
var LQback = null;
function lrRun(ci, items, label, done, back){
  LQci=ci; LQback=back||null; LQ=items.slice(); LQi=0; LQmiss=0; LQlab=label; LQdone=done; lrPaint();
}
function lrPaint(){
  if(LQi >= LQ.length) return LQdone();
  const it = LQ[LQi]; LQpick = [];
  /* A one-item queue (Play) has no progress to show: the bar would sit at 0%
     forever and the counter would read "1 / 1". Show the run's streak instead,
     which is the only number that means anything in an endless game
     (owner 2026-09-01). */
  const single = LQ.length === 1 && LQback;
  const pct = Math.round(LQi/LQ.length*100);
  const head = single
    ? `<div class="lr-progl pl-head">${esc(LQlab)}</div>`
    : `<div class="lr-prog"><i style="width:${pct}%"></i></div>
       <div class="lr-progl">${esc(LQlab)} · ${numL(LQi+1)} / ${numL(LQ.length)}${
         LQmiss?' · '+esc(fmt(L('learn_revisit'),{n:numL(LQmiss)})):''}</div>`;
  /* Re-shuffle the options every time the question is painted. They were
     shuffled once at build time, so a requeued question came back with the
     four verses in the SAME positions — and the reader already knew which one
     was wrong, making the retry a 1-in-3 guess rather than recall. Shuffling
     the ARRAY (not just the render) keeps lrPick's index honest, since it
     looks the answer up by position (owner 2026-09-02). */
  if(it.kind === 'pick' && it._seen) it.opts = lrShuffle(it.opts);
  it._seen = 1;
  const body = it.kind === 'pick'
    ? `<div class="lr-ask">${it.ask}</div>
       <div class="lr-opts">${it.opts.map((o,i)=>`
         <button class="lr-opt" onclick="lrPick(${i})">
           <span class="ol${o.deva?' dv':''}"${o.deva?' lang="sa"':''}>${o.deva?o.label:esc(o.label)}</span>
           ${o.sub?`<span class="os">${esc(o.sub)}</span>`:''}
         </button>`).join('')}</div>`
    : `<div class="lr-ask">${it.ask}</div>
       <div class="lr-slots" id="lrSlots"></div>
       <div class="lr-chips">${lrShuffle(it.chips).map(c=>`
         <button class="lr-chip2${c.deva?' dv':''}"${c.deva?' lang="sa"':''} onclick="lrChip(this,${c.id})">${esc(c.label)}</button>`).join('')}</div>`;
  view.innerHTML = `<div class="lrn fade-in">${head}
    <div class="lr-qbox">${body}<div class="lr-fb" id="lrFb"></div></div>
    </div>` + (LQback
      ? backFoot(LQback.fn, L(LQback.label))
      : backFoot(`showRead(${LQci},'full')`, L('back_chapter_one')));
  scrollViewTop();
}
function lrPick(i){
  const it = LQ[LQi], o = it.opts[i];
  document.querySelectorAll('.lr-opt').forEach((b,k)=>{
    b.disabled = true;
    if(it.opts[k].ok) b.classList.add('right');
    else if(k === i) b.classList.add('wrong');
  });
  const fb = document.getElementById('lrFb');
  if(o.ok){
    fb.innerHTML = `<div class="good">${esc(L('learn_yes'))}</div>`;
    LQi++; setTimeout(lrPaint, 620);
  }else{
    LQmiss++; LQ.push(it);
    /* The tick and cross on the options already say right and wrong, so the
       feedback line drops the verdict and keeps only what the reader cannot
       see: the correct verse and its meaning. The button says what pressing it
       DOES — in Play the same question returns, so "select again" is literally
       true; in a multi-question drill the missed item is requeued and comes
       back later, which is the same promise. (owner 2026-09-02) */
    fb.innerHTML = (it.note?`<div class="nt">${it.note}</div>`:'')
      + `<button class="lr-cta" onclick="LQi++;lrPaint()">${esc(L('learn_retry'))}</button>`;
  }
}
function lrChip(el, id){
  const it = LQ[LQi], want = it.answer[LQpick.length];
  const fb = document.getElementById('lrFb');
  if(id === want){
    /* Clear any standing "not there yet" the moment the reader gets it right.
       Without this the correction stays on screen for the rest of the question
       and reads as though the new, correct answer were also wrong
       (owner 2026-09-01). */
    if(fb) fb.innerHTML = '';
    LQpick.push(id); el.disabled = true; el.classList.add('used');
    /* carry the chip's script class through, or a Devanagari pāda drops back
       to the Latin face the moment it is placed */
    const dv = el.classList.contains('dv') ? ' dv' : '';
    document.getElementById('lrSlots').insertAdjacentHTML('beforeend',
      `<span class="lr-slot${dv}"${dv?' lang="sa"':''}>${numL(LQpick.length)}. ${esc(el.textContent.trim())}</span>`);
    if(LQpick.length === it.answer.length){
      fb.innerHTML = `<div class="good">${esc(L('learn_thread_ok'))}</div>`;
      LQi++; setTimeout(lrPaint, 700);
    }
  }else{
    LQmiss++;
    el.classList.add('shake'); setTimeout(()=>el.classList.remove('shake'), 380);
    const r = it.chips.find(c=>c.id===want);
    fb.innerHTML = `<div class="bad">${esc(L('learn_nextis'))} <b>${esc(r?r.label:'')}</b></div>`;
  }
}

function renderCrumbs(){
  scrollViewTop();
  crumbs.innerHTML='';
  if(state.view!=='search' && state.view!=='favorites') return;
  const o = state.origin || { view:'welcome' };
  const clear = fn => { $('#searchInput').value=''; fn(); };

  let label, action;
  if(o.view === 'welcome'){
    label = L('home_plain');            action = ()=>clear(showWelcome);
  } else if(o.chapter != null && o.theme != null && o.view === 'verses'){
    // Name each level as what it is — "Theme 1 · The Royal Secret", not just the
    // title, which can echo the chapter name (ch.9's theme 1 is "राजगुह्य", the
    // chapter "राजविद्या राजगुह्य योग"). Matches the verse modal's own wording.
    const ch = DATA[o.chapter];
    label = `${L('theme_sg')} ${numL(o.theme+1)} · ${T(ch.themes[o.theme].titles)}`;
    action = ()=>clear(()=>showVerses(o.chapter, o.theme));
  } else if(o.chapter != null){
    const ch = DATA[o.chapter];
    label = `${L('chapter')} ${numL(ch.num)} · ${T(ch.names)}`;
    action = ()=>clear(()=>showThemes(o.chapter));
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
  /* The Three Ways is the door; there is no flat all-18 list. Every chapter
     list lives inside its way, so the niṣṭhā framing is never skipped. */
  state.view='chapters'; state.section=section; state.chapter=null; state.theme=null; renderCrumbs();
  const list = DATA.filter(ch => ch.num >= (section-1)*6+1 && ch.num <= section*6);
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'), 'showSections()'], [wayName(section), null]])}
    <div class="grid chapters fade-in">
      ${list.map(ch=>{
        const ci = DATA.indexOf(ch);
        return `<div class="card" role="button" tabindex="0" onclick="showRead(${ci},'full')">
          <span class="chip">${L('chapter')} ${numL(ch.num)}</span>
          <h3>${esc(T(ch.names))}</h3>
          <p>${esc(T(ch.subs))}</p>
          <div class="meta">${numL(ch.verses)} ${L('verses')}</div>
          <div class="go">${L('open_chapter')}</div>
        </div>`;}).join('')}
    </div>` + backFoot('showSections()', L('back_ways'));
}

function dayVerse(){
  const d = new Date();
  const dayNum = d.getFullYear()*10000 + (d.getMonth()+1)*100 + d.getDate();
  return VERSES[dayNum % VERSES.length];
}
function goHome(){
  if($('#modalBg').classList.contains('open')) closeModal();
  $('#searchInput').value = '';
  state.origin = null;
  showWelcome();
}
function showWelcome(){
  state.view='welcome'; state.chapter=null; state.theme=null; state.section=null; renderCrumbs();
  view.innerHTML = `
    <div class="welcome fade-in">
      <div class="w-om">ॐ</div>
      <!-- h2, not h1: #appTitle in the banner is this document's single h1.
           .view-title carries all the styling, so this is semantics only. -->
      <h2 class="view-title">${esc(L('welcome_title'))}</h2>
      <p class="view-sub">${esc(L('welcome_sub'))}</p>
      ${(()=>{ const sv = state.shared; const dv = sv || dayVerse(); const c = DATA[dv.ci], v = verseAt(dv);
        const part = sutraAt(c.themes[dv.ti], dv.si).part;
        return `<div class="w-day fade-in" role="button" tabindex="0" onclick="openModal(${dv.ci},${dv.ti},${dv.si},'book')">
          <div class="wd-label">${esc(sv ? L('shared_label') : L('verse_of_day'))}</div>
          <div class="vnum">${esc(L('verse'))} ${esc(fmtNL(v.n))}</div>
          <div class="m-topic"><span class="mt-lab">${esc(L('verse_topic'))}:</span> ${esc(T(part.titles))}</div>
          <div class="padas">${padaBlockDeva(v)}</div>
          <div class="vhint">${sv ? esc(L('shared_hint')) : esc(T(v.paras).slice(0,80)) + '…'}</div>
        </div>`; })()}
      <button class="tool-btn primary big" onclick="showSections()">${esc(L('welcome_enter'))}</button>
      <div class="w-foot">${esc(L('welcome_foot'))}</div>
      <!-- Owner 2026-09-01: say plainly that the app is still being built.
           Placed after the footer line so it reads as a quiet note, not a
           disclaimer competing with the invitation to enter. -->
      <p class="w-wip">${esc(L('wip'))}</p>
    </div>`;
}
function sectionCard(k, chip, title, desc){
  return `<div class="card sect" role="button" tabindex="0" onclick="showChapters(${k})">
    <span class="chip">${esc(chip)}</span>
    <h3>${esc(title)}</h3>
    <p>${esc(desc)}</p>
    <div class="go">${esc(L('open_chapters'))}</div>
  </div>`;
}
function showSections(){
  state.view='sections'; state.chapter=null; state.theme=null; state.section=null; state.shared=null; renderCrumbs();
  view.innerHTML = `
    <div class="view-title fade-in">${esc(L('sections_title'))}</div>
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
  return `<nav class="way-crumb fade-in" aria-label="breadcrumb">` + items.map((it,i)=>{
    const last = i === items.length - 1;
    const sep = i ? `<span class="wc-sep" aria-hidden="true">›</span>` : '';
    if(!last) return sep + `<button class="wc-chip wc-link" onclick="${it[1]}">${esc(it[0])}</button>`;
    return sep + `<span class="wc-chip wc-cur" aria-current="page">${esc(it[0])}</span>`;
  }).join('') + `</nav>`;
}
function wayName(k){ /* the trail carries the Sanskrit niṣṭhā name, as the
  landing cards do — "कर्मनिष्ठा · The Way of Karma" — so the map is always
  rooted in the tradition, in every language */ return L('sec_'+['','karma','bhakti','jnana'][k]); }
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
  const m = state.view === 'themes' ? 'study'
          : state.view === 'learn'  ? 'learn'
          : (state.readMode || 'full');
  const btn = (mode, lab, fn, tip) =>
    `<button class="ms-btn${m === mode ? ' on' : ''}" title="${tip}" aria-label="${tip}" onclick="${fn}">${lab}</button>`;
  return `<div class="mode-box fade-in">
    <div class="mode-lbl">${esc(L('choose_title'))}</div>
    <div class="mode-seg" role="group" aria-label="${esc(L('choose_title'))}">
      ${btn('full',  esc(L('opt_full')),    `showRead(${ci},'full')`,  esc(L('opt_full_d')))}
      ${btn('study', esc(L('opt_study_s')), `showThemes(${ci})`,       esc(L('opt_study_d')))}
      ${btn('learn', esc(L('opt_learn_s')), `showLearn(${ci})`,        esc(L('opt_learn_d')))}
    </div>
  </div>`;
}
function chTitle(ch){ return `<div class="view-title fade-in"><span class="chdeva">${ch.deva}</span> · ${esc(T(ch.names))}</div>`; }
function showThemes(ci){
  state.view='themes'; state.chapter=ci; state.section = state.section || Math.ceil(DATA[ci].num/6); state.theme=null; renderCrumbs();
  const ch = DATA[ci];
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'), 'showSections()'], [wayName(Math.ceil(ch.num/6)), `showChapters(${Math.ceil(ch.num/6)})`], [`${L('chapter')} ${numL(ch.num)} · ${L('opt_study_g')}`, null]])}
    ${chTitle(ch)}
    ${modeSwitch(ci)}
    <div class="view-sub fade-in">${esc(T(ch.subs))} — ${L('pick_theme')}</div>
    <div class="th-flow fade-in">
      ${ch.themes.map((t,ti)=>{
        /* Owner 2026-08-30: the theme stays a door; its verses become
           display-only cards in the chapter-list grammar — a tap target
           nested inside a tap target was an ambiguity too many. Word-by-word
           lives one level deeper, in the verse grid. */
        const cards = t.parts.map(p=>
          `<div class="card vcard">
            <span class="chip">${vn2(p.sutras[0].n)}</span>
            <h3>${esc(T(p.titles))}</h3>
            <p>${esc(T(p.descs))}</p></div>`).join('');
        return `<div class="theme" role="button" tabindex="0" onclick="showVerses(${ci},${ti})">
          <h3>${esc(T(t.titles))}<span class="rng">${fmtRangeL(t.range)}</span></h3>
          <p class="tdesc">${esc(T(t.descs))}</p>
          <div class="vcards">${cards}</div>
        </div>`; }).join('')}
    </div>` + backFoot(`showChapters(${state.section||0})`, L('back_chapters'));
}

/* ---------- continuous reading ----------
   The chapter -> theme -> part -> verse structure is right for study, but the
   Gita is also something you sit and read straight through. This shows one
   chapter as flowing text: speaker, verse, translation, nothing else. Tapping a
   verse still opens the popup with its quarters and word meanings. */
function showRead(ci, mode){
  rememberOrigin();
  /* Owner 2026-09-01: "Verses only" (mūla) was retired. This is a LEARNING
     app — the root text with no meaning served the reciter, not the student,
     and it cost a third of the chooser for a mode that taught nothing. 'mula'
     is still accepted as an alias so links already shared keep working; it
     simply lands on 'full'. */
  if(mode === 'mula') mode = 'full';
  state.readMode = mode || state.readMode || 'full';
  state.view='read'; state.chapter=ci; state.section = state.section || Math.ceil(DATA[ci].num/6); state.theme=null; renderCrumbs();
  const ch = DATA[ci];
  const all = [];
  ch.themes.forEach((t,ti)=>t.parts.forEach(p=>p.sutras.forEach((sv,si)=>
    all.push({sv, ti, idx: flatIndex(t,p,si)}))));
  let lastSpeaker = '';
  const body = all.map(({sv,ti,idx})=>{
    /* Render sv.lines in the order the source gives them, so a speaker that sits
       BETWEEN the two lines stays there (1.21, 1.28) instead of being hoisted to
       the top. Show the speaker only when the voice changes — losing track of who
       is talking changes the meaning of a dialogue. */
    let li = 0, inner = '';
    for(const x of sv.lines){
      if(x.k === 's'){
        const name = x.d.replace(/।\s*$/, '');
        if(name !== lastSpeaker){ lastSpeaker = name; inner += `<div class="rd-spk">${name}</div>`; }
      } else {
        // the verse number belongs at the end of the second line, between the
        // daṇḍas, as printed editions set it
        const tail = li ? `॥ <span class="rd-n">${esc(fmtNL(sv.n))}</span> ॥` : '।';
        inner += `<div class="gline">${x.d}${tail}</div>`;
        li++;
      }
    }
    return `<div class="rd-v" role="button" tabindex="0" onclick="openModal(${ci},${ti},${idx},'read')">
      <div class="rd-deva">${inner}</div>
      ${state.readMode === 'full' ? `<div class="rd-lb">${esc(L('literal'))}:</div><div class="rd-tr">${esc(T(sv.lits))}</div><div class="rd-lb">${esc(L('in_other_words'))}:</div><div class="rd-par">${esc(T(sv.paras))}</div>` : ''}
    </div>`;
  }).join('');
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'), 'showSections()'], [wayName(Math.ceil(ch.num/6)), `showChapters(${Math.ceil(ch.num/6)})`], [`${L('chapter')} ${numL(ch.num)} · ${L('opt_full_g')}`, null]])}
    ${chTitle(ch)}
    ${modeSwitch(ci)}
    <div class="view-sub fade-in">${esc(L('read_sub'))}</div>
    <div class="reading ${state.readMode} fade-in">${body}</div>` + backFoot(`showChapters(${state.section||0})`, L('back_chapters'));
}

function flatIndex(t,p,s){ let idx=0; for(const pp of t.parts){ if(pp===p) return idx+s; idx+=pp.sutras.length; } return idx; }
function sutraAt(t,i){ for(const p of t.parts){ if(i < p.sutras.length) return {s:p.sutras[i], part:p}; i-=p.sutras.length; } return {s:t.parts[t.parts.length-1].sutras[0], part:t.parts[t.parts.length-1]}; }

// pāda display: Devanagari block with pādas on separate lines (speakers inline)
function pDanda(i, total){
  if(total === 2) return (i===0) ? '।' : '॥';
  return (i%4===1)?'।':((i%4===3)?'॥':'');
}
/* The running verse is rendered verbatim from the source JSON.
   v.lines is the list of `।`-separated segments as they appear in
   source/ch*.json: two verse lines, plus a speaker where the source has one
   (in 1.21 and 1.28 the speaker falls between the two lines, and it renders
   in place because we never reorder). Nothing is re-joined or re-derived, so
   the display cannot drift from the source. To correct a verse, edit the JSON.
   The pāda split is still shown in the modal's 2x2 boxes; that data is
   separate and untouched. */
function padaBlockDeva(s, withNum){
  /* withNum puts the verse number inside the closing daṇḍas of the final line
     — ॥ १.२५ ॥ — the way a printed edition sets it, instead of on a line of
     its own below. Same construction as the reading view's rd-n. */
  const ls = (s.lines || []), last = ls.reduce((a,it,i)=> it.k === 's' ? a : i, -1);
  let html = '', li = 0;
  for(let i = 0; i < ls.length; i++){
    const it = ls[i];
    if(it.k === 's'){ html += `<span class="spk">${it.d}</span>`; continue; }
    const tail = li
      ? (withNum && i === last ? `॥ <span class="gl-n">${esc(fmtNL(s.n))}</span> ॥` : '॥')
      : '।';
    html += `<div class="gline">${it.d}${tail}</div>`;
    li++;
  }
  return html;
}

function showVerses(ci,ti){
  state.view='verses'; state.chapter=ci; state.theme=ti; renderCrumbs();
  const ch = DATA[ci], t = ch.themes[ti];
  const blocks = t.parts.map((p,pi)=>`
    <div class="part fade-in">
      <div class="part-head">
        <span class="ptitle">${esc(T(p.titles))}</span>
        <span class="pdesc">${esc(T(p.descs))}</span>
      </div>
      <div class="grid verses">
        ${p.sutras.map((s,si)=>`
          <div class="mini" role="button" tabindex="0" onclick="openModal(${ci},${ti},${flatIndex(t,p,si)},'theme')">
            <div class="vnum">${L('verse')} ${fmtNL(s.n)}</div>
            <div class="padas">${padaBlockDeva(s)}</div>
            <div class="vhint">${esc(T(s.paras).slice(0,80))}…</div>
          </div>`).join('')}
      </div>
    </div>`).join('');
  view.innerHTML = `
    ${wayCrumbs([[L('sections_title'), 'showSections()'], [wayName(Math.ceil(ch.num/6)), `showChapters(${Math.ceil(ch.num/6)})`], [`${L('chapter')} ${numL(ch.num)} · ${L('opt_study_g')}`, `showThemes(${ci})`], [`${L('theme_sg')} ${numL(ti+1)} · ${T(t.titles)}`, null]])}
    <!-- Owner 2026-09-02: this was the ONLY view in the app with no heading —
         the theme's name appeared in the crumb trail and then nowhere on the
         page itself, so the reader arrived at a description with no subject.
         Same shape as the learn path's theme screen: title, then range, then
         the description. -->
    <div class="view-title fade-in">${esc(T(t.titles))}<span class="rng">${fmtRangeL(t.range)}</span></div>
    <div class="view-sub fade-in">${esc(T(t.descs))}</div>
    <div class="view-sub fade-in">${numL(vCount(t))} ${vCount(t)===1?L('verse'):L('verses')}. ${L('click_hint')}.</div>
    ${blocks}` + backFoot(`showThemes(${ci})`, L('back_themes'));
}

let SRCH_HITS = [], FAV_LIST = [];
/* The verse range a reader walks in thematic study: the WHOLE theme.
   Until 2026-09-01 this returned the enclosing part's bounds, which was right
   when a part grouped several verses. Parts are now one verse each (700 parts
   for 700 verses), so it returned {start:n, end:n} — a range of one — and
   Prev/Next were disabled on every verse in the app. The theme is the unit. */
function themeBounds(t){
  let n = 0; for(const p of t.parts) n += p.sutras.length;
  return {start:0, end:Math.max(0, n-1)};
}
function openModal(ci,ti,si, mode, navIdx){
  mode = mode || 'theme';
  state.chapter=ci; state.theme=ti; state.idx=si; state.mode=mode;
  state.gpos = VERSES.findIndex(e => e.ci===ci && e.ti===ti && e.si===si);
  if(state.gpos < 0) state.gpos = 0;
  if(mode === 'theme'){
    const b = themeBounds(DATA[ci].themes[ti]);
    state.pStart = b.start; state.pEnd = b.end;
  } else if(mode === 'read'){
    /* Tapped from "Verses only" / "Verses with translation". The reader is in
       a CHAPTER, so Prev/Next walk that chapter and stop at its edges — the
       counter then means something ("verse 12 of 20") and nobody is silently
       relocated into the next chapter. Search and favourites still range over
       all 700, because those lists are not chapter-scoped.
       Until 2026-09-01 'read' reached navSutra()'s `else return` and both
       buttons simply did nothing. */
    state.cStart = VERSES.findIndex(e => e.ci === ci);
    state.cEnd = state.cStart;
    while(state.cEnd + 1 < VERSES.length && VERSES[state.cEnd + 1].ci === ci) state.cEnd++;
  } else if(mode === 'search'){ mode = 'book'; }
  else if(mode === 'fav'){ state.navList = FAV_LIST; state.navIdx = navIdx || 0; }
  state.mode = mode;
  fillModal(); $('#modalBg').classList.add('open'); document.body.style.overflow='hidden';
  pushModalHistory();
  /* every verse has an address: the sheet writes #v=2.47 so the open verse
     can be shared and restored; the history entry keeps the old URL, so back
     restores it for free */
  try{ history.replaceState({gitaModal:true}, '', '#v=' + sutraAt(DATA[ci].themes[ti], si).s.n); }catch(e){}
}
function closeModal(){
  const wasOpen = $('#modalBg').classList.contains('open');
  $('#modalBg').classList.remove('open'); document.body.style.overflow='';
  if(wasOpen) popModalHistory();
}
/* ---------- share a verse: native share sheet where available, else copy ---------- */
function shareUrl(){
  /* When the app runs from a downloaded copy (file://), a file path is
     useless to the recipient — and feeding one to the native share sheet
     crashes some Chromes. Share the live site's address instead (the og:url
     tag carries it), so shares from ANY copy land on the public verse. */
  const og = document.querySelector('meta[property="og:url"]');
  const root = (og ? og.content : 'https://chapain.github.io/Bhagavad-Gita/').replace(/\/$/, '');
  /* Owner 2026-09-01: shares point at the verse's anchor on its CHAPTER page
     (/chapter/N/#vN.NN). The 700 one-per-verse v/ pages are gone — GitHub's
     web uploader caps at 100 files, so republishing them was seven manual
     drags every time. The chapter page already carries the full verse in all
     four scripts and is already indexed; its inline script opens the folded
     <details> and highlights the verse, so the link still lands on the verse.
     Trade-off: the link PREVIEW is the chapter's, not the verse's. */
  const n = sutraAt(DATA[state.chapter].themes[state.theme], state.idx).s.n;
  return root + '/chapter/' + n.split('.')[0] + '/#v' + n;
}
function openSharePanel(){
  $('#spLink').textContent = shareUrl();
  const p = $('#sharePanel');
  p.style.display = (p.style.display === 'flex') ? 'none' : 'flex';
}
function copyVerseLink(){
  const t = $('#spLink').textContent;
  function copied(){
    /* Job done — collapse the panel right away and flash the confirmation on
       the Share button itself, so the reader is straight back on the verse. */
    const p = $('#sharePanel'); if(p) p.style.display = 'none';
    const sh = $('#shareBtn');
    if(sh){ sh.textContent = L('link_copied');
      setTimeout(function(){ sh.textContent = L('share'); }, 1600); }
  }
  try { navigator.clipboard.writeText(t).then(copied, copied); }
  catch(e){ const ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta);
    ta.select(); try{ document.execCommand('copy'); }catch(e2){} ta.remove(); copied(); }
}
/* ---------- mobile: Android hardware / iOS swipe "back" closes the verse sheet ---------- */
let MODAL_HIST = false, MODAL_POPPING = false;
function pushModalHistory(){
  if(MODAL_HIST) return;
  try{ history.pushState({gitaModal:true}, ''); MODAL_HIST = true; }catch(e){}
}
function popModalHistory(){
  if(!MODAL_HIST) return;
  MODAL_HIST = false;
  if(MODAL_POPPING) return;               // we got here *from* popstate — nothing to unwind
  try{ history.back(); }catch(e){}
}
window.addEventListener('popstate', ()=>{
  if($('#modalBg').classList.contains('open')){
    MODAL_POPPING = true; closeModal(); MODAL_POPPING = false;
  }
});

function fillModal(){
  const ch = DATA[state.chapter], t = ch.themes[state.theme];
  const {s, part} = sutraAt(t, state.idx);
  let partIdx = 0; { let acc = 0;
    for(let pi=0; pi<t.parts.length; pi++){ const len = t.parts[pi].sutras.length;
      if(state.idx >= acc && state.idx < acc+len){ partIdx = pi; break; } acc += len; } }
  if(state.gpos == null) state.gpos = Math.max(0, VERSES.findIndex(e => e.ci===state.chapter && e.ti===state.theme && e.si===state.idx));
  // split flow: top speakers, mid speakers (between pāda 2 and 3), and the 4 pādas
  let topS = [], midS = [], pads = [];
  for(const it of s.flow){
    if(it.k==='s'){ (pads.length < 2 ? topS : midS).push(it); }
    else pads.push(it);
  }
  const LI = {en:0, ne:1, hi:2}[state.lang] || 0;
  function wordsHtml(it){
    return (it.words||[]).map(w=>`<div class="wrow"><span class="wdeva">${w[0]}</span><span class="wiast">${esc(w[1])}</span><span class="wmean">${esc(w[2+LI] || w[2])}</span></div>`).join('');
  }
  function spkHtml(list){
    return list.map(x=>`
      <div class="spk-line" onclick="toggleWords(this)">
        <span class="spk-main">${x.d} <span class="iast">${esc(x.t)}</span></span>
        <div class="words">${wordsHtml(x)}</div>
      </div>`).join('');
  }
  function boxHtml(pad, idx, total){
    return `<div class="pada-box" onclick="toggleWords(this)">
      <div class="pb-top">
        <span class="pb-num">${esc(L('pada_label'))} ${numL(idx+1)}</span>
      </div>
      <div class="pb-deva">${pad.d}${pDanda(idx,total)}</div>
      <div class="pb-iast">${esc(pad.t)}</div>
      <div class="words">${wordsHtml(pad)}</div>
    </div>`;
  }
  $('#modal').innerHTML = `
    <button class="m-close" onclick="closeModal()">✕</button>
    <div class="m-num">${L('verse')} ${fmtNL(s.n)} · ${esc(T(ch.names))}
      <button class="fav-btn" id="shareBtn" onclick="openSharePanel()">${L('share')}</button>
      <button class="fav-btn${FAV.includes(s.n)?' saved':''}" id="favBtn" onclick="toggleFav('${s.n}')">${FAV.includes(s.n)?ICONS.starF:ICONS.star}${esc(FAV.includes(s.n)?L('saved_verse'):L('save_verse'))}</button></div>
    <div class="share-panel" id="sharePanel">
      <div class="sp-hint">${L('share_hint')}</div>
      <div class="sp-link" id="spLink"></div>
      <button class="sp-copy" id="shCp" onclick="copyVerseLink()">${L('copy_link')}</button>
    </div>
    <div class="m-part">${esc(L('theme_sg'))} ${numL(state.theme+1)} · ${esc(T(t.titles))} » ${esc(T(part.titles))}</div>
    <div class="m-meter">${esc(meterText(s))}</div>
    <div class="m-verse">
      <div class="words-bar">
        <span class="wb-hint">${L('click_hint_pada')} ·</span>
        <button class="wb-btn" onclick="toggleAllMeanings(this)" disabled>${ICONS.eyeOff}<span>${L('hide_meanings')}</span></button>
      </div>
      ${spkHtml(topS)}
      <div class="pada-grid">
        <div class="pada-row">${boxHtml(pads[0],0,pads.length)}${boxHtml(pads[1],1,pads.length)}</div>
        ${midS.length ? `<div class="spk-mid">${spkHtml(midS)}</div>` : ''}
        ${pads.length===4 ? `<div class="pada-row">${boxHtml(pads[2],2,4)}${boxHtml(pads[3],3,4)}</div>` : ''}
      </div>
    </div>
    <div class="m-line"><span class="lb">${L('literal')}</span><div class="lt">${esc(T(s.lits))}</div></div>
    <div class="m-line para"><span class="lb">${L('in_other_words')}</span><div class="lt">${esc(T(s.paras))}</div></div>
    <div class="m-tail" aria-hidden="true"></div>
    <div class="m-nav">
      ${state.mode==='random'
        ? `<button class="m-random" onclick="randomVerse()">${ICONS.shuffle}<span>${esc(L('next_random'))}</span></button>`
        : state.mode==='theme'
          ? `<button onclick="navSutra(-1)" ${state.idx>state.pStart?'':'disabled'}>${L('previous')}</button>
             <span class="m-count">${Lof(state.idx-state.pStart+1, state.pEnd-state.pStart+1)}</span>
             ${state.idx===state.pEnd
               ? `<button class="m-back" onclick="backToTheme()">${esc(L('back_to_theme'))}</button>`
               : `<button onclick="navSutra(1)">${L('next')}</button>`}`
          : state.mode==='read'
          ? `<button onclick="navSutra(-1)" ${state.gpos>state.cStart?'':'disabled'}>${L('previous')}</button>
             <span class="m-count">${Lof(state.gpos-state.cStart+1, state.cEnd-state.cStart+1)}</span>
             <button onclick="navSutra(1)" ${state.gpos<state.cEnd?'':'disabled'}>${L('next')}</button>`
          : state.mode==='book'
          ? `<button onclick="navSutra(-1)" ${state.gpos>0?'':'disabled'}>${L('previous')}</button>
             <span class="m-count">${Lof(state.gpos+1, VERSES.length)}</span>
             <button onclick="navSutra(1)" ${state.gpos<VERSES.length-1?'':'disabled'}>${L('next')}</button>`
          : `<button onclick="navSutra(-1)" ${(state.navIdx||0)>0?'':'disabled'}>${L('previous')}</button>
             <span class="m-count">${Lof((state.navIdx||0)+1, state.navList?state.navList.length:1)}</span>
             <button onclick="navSutra(1)" ${(state.navIdx||0) < (state.navList?state.navList.length-1:0)?'':'disabled'}>${L('next')}</button>`}
    </div>`;
}
// toggle pada-chheda (word split) open/closed on the clicked element's box/line
function toggleWords(el){
  const cont = el.closest('.pada-box, .spk-line');
  if(!cont) return;
  const words = cont.querySelector('.words');
  if(!words) return;
  const open = words.classList.toggle('open');
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
    btn.innerHTML = ICONS.eyeOff + `<span>${esc(L('hide_meanings'))}</span>`;
    document.querySelectorAll('#modal .words').forEach(w=>w.classList.remove('mean-off'));
  }
}
// toggle meaning visibility across all word-splits in the modal
function toggleAllMeanings(btn){
  const hide = btn.dataset.state !== 'hidden';   // meanings start visible → first click hides
  btn.dataset.state = hide ? 'hidden' : 'shown';
  btn.innerHTML = (hide ? ICONS.eye : ICONS.eyeOff) + `<span>${esc(L(hide ? 'show_meanings' : 'hide_meanings'))}</span>`;
  document.querySelectorAll('#modal .words').forEach(w=>{
    w.classList.toggle('mean-off', hide);
  });
}
function navSutra(d){
  if(state.mode === 'theme'){
    const n = state.idx + d;
    if(n < state.pStart || n > state.pEnd) return;
    state.idx = n;
  } else if(state.mode === 'read'){
    const n = (state.gpos || 0) + d;
    if(n < state.cStart || n > state.cEnd) return;
    state.gpos = n;
    const loc = VERSES[n];
    state.chapter = loc.ci; state.theme = loc.ti; state.idx = loc.si;
  } else if(state.mode === 'book'){
    state.gpos = Math.max(0, Math.min(VERSES.length-1, (state.gpos || 0) + d));
    const loc = VERSES[state.gpos];
    state.chapter = loc.ci; state.theme = loc.ti; state.idx = loc.si;
  } else if((state.mode === 'fav') && state.navList){
    const k = (state.navIdx || 0) + d;
    if(k < 0 || k >= state.navList.length) return;
    state.navIdx = k;
    const loc = state.navList[k];
    state.chapter = loc.ci; state.theme = loc.ti; state.idx = loc.si;
  } else return;
  state.gpos = VERSES.findIndex(e => e.ci===state.chapter && e.ti===state.theme && e.si===state.idx);
  if(state.gpos < 0) state.gpos = 0;
  fillModal();
  const m = $('#modal'); if(m) m.scrollTo({top:0, behavior:'smooth'});
}
function backToTheme(){ closeModal(); showVerses(state.chapter, state.theme); }
document.addEventListener('keydown', e=>{
  /* Keyboard parity (audit 2026-08-30): the tappable divs carry role="button"
     tabindex="0"; Enter/Space must do what the tap does. */
  if((e.key==='Enter' || e.key===' ') && document.activeElement
     && document.activeElement.matches && document.activeElement.matches('[role="button"]')){
    e.preventDefault(); document.activeElement.click(); return;
  }
  if(!$('#modalBg').classList.contains('open')) return;
  if(e.key==='Escape') closeModal();
  if(state.mode==='random') return;
  if(e.key==='ArrowLeft') navSutra(-1);
  if(e.key==='ArrowRight') navSutra(1);
});

/* ---------- mobile: horizontal swipe inside the verse sheet = prev / next ---------- */
(function(){
  const bg = $('#modalBg'); if(!bg) return;
  let x0=null, y0=null, t0=0, lock=null;
  bg.addEventListener('touchstart', e=>{
    if(e.touches.length!==1){ x0=null; return; }
    x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; t0 = Date.now(); lock = null;
  }, {passive:true});
  bg.addEventListener('touchmove', e=>{
    if(x0==null || e.touches.length!==1) return;
    const dx = e.touches[0].clientX - x0, dy = e.touches[0].clientY - y0;
    if(lock===null && (Math.abs(dx) > 12 || Math.abs(dy) > 12)) lock = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
  }, {passive:true});
  bg.addEventListener('touchend', e=>{
    if(x0==null || lock!=='x'){ x0=null; return; }
    const dx = (e.changedTouches[0].clientX - x0);
    const dt = Date.now() - t0;
    x0 = null;
    if(dt > 800 || Math.abs(dx) < 60) return;
    if(state.mode === 'random') return;
    navSutra(dx < 0 ? 1 : -1);              // swipe left → next, swipe right → previous
  }, {passive:true});
})();
/* Offline support when served over http(s): the service worker caches the app so
   it opens with no connection and "Add to Home Screen" behaves like a real app.
   Deliberately skipped for file:// (WhatsApp/Drive downloads) — SWs are not
   allowed there and would throw. Failure is always non-fatal. */
if ('serviceWorker' in navigator && location.protocol.indexOf('http') === 0) {
  window.addEventListener('load', function(){
    navigator.serviceWorker.register('sw.js').catch(function(){ /* offline cache unavailable — app still works */ });
  });
}
function gitaBoot(){
  buildIndex();
  buildVerseText();
  applyStatic();
  paintTheme();
  /* Deep links: the chapter landing pages (and shared messages) can open a
     specific verse — index.html#v=2.47 — or a whole chapter (#chapter=7). */
  (function(){
    var v = /^#v=([1-9][0-9]?\.[0-9]{1,2})$/.exec(location.hash || '');
    if (v) { var hp = v[1].split('.');
      var loc = verseLoc(hp[0] + '.' + (hp[1].length === 1 ? '0' + hp[1] : hp[1]));
      /* Owner 2026-08-31: a shared verse lands as an INVITATION, not a popup —
         the verse is shown on the welcome page with "click to see the
         meanings"; the four-pāda sheet opens when the receiver clicks. */
      if (loc) { state.shared = loc; showWelcome(); return; } }
    var tm = /^#theme=([1-9]|1[0-8])\.([0-9]+)$/.exec(location.hash || '');
    if (tm) { const ci = parseInt(tm[1], 10) - 1, ti = parseInt(tm[2], 10);
      if (DATA[ci] && DATA[ci].themes[ti]) { showVerses(ci, ti); return; } }
    var m = /^#chapter=([1-9]|1[0-8])(&tab=(mula|full|study))?$/.exec(location.hash || '');
    if(m){ const ci = parseInt(m[1], 10) - 1; const tb = m[3];
      if(tb === 'study'){ showThemes(ci); } else if(tb){ showRead(ci, tb); } else { showRead(ci, 'full'); } } else { showWelcome(); }
  })();
}
</script>
__DATASCRIPTS__
</body>
</html>
"""

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
_font_css = _font_face()
data_js = [f"GITA_CH[{ch['num']}] = {json.dumps(ch, ensure_ascii=False)};\n" for ch in data]

_loader = (
    "window.__gitaLoaded = function(){\n"
    f"  if (DATA || Object.keys(GITA_CH).length < {len(data)}) return;\n"
    "  DATA = [];\n"
    f"  for (var n = 1; n <= {len(data)}; n++) DATA.push(GITA_CH[n]);\n"
    "  gitaBoot();\n"
    "};\n"
    "function gitaLoadFail(){ var b = document.getElementById('bootNote');\n"
    "  if (b) b.textContent = 'Could not load the verse data. Check your connection and reload.'; }")
_tags = "\n".join(
    f'<script src="data/ch{ch["num"]}.js" onload="__gitaLoaded()" onerror="gitaLoadFail()"></script>'
    for ch in data)

shell = (HTML
         .replace("__FONTS__", _font_css)
         .replace("__UI__", _ui_js)
         .replace("__DATALOADER__", _loader)
         .replace("__DATASCRIPTS__", _tags))

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
   identical — source/check_chapter_css.py now fails the build if they drift. */
:root{ --paper:#FFF8EC; --ink:#2A2118; --ink-soft:#6B5D4F; --accent:#1A5648;
       --saffron:#B45A24; --card:#FFFCF4; --line:#E6D9C3; }
@media (prefers-color-scheme:dark){
  :root{ --paper:#1F1A14; --ink:#EDE3D0; --ink-soft:#B0A28C; --accent:#8FBEB0;
         --saffron:#DE8F52; --card:#272018; --line:#3B3227; }
}
*{ box-sizing:border-box; }
body{ margin:0; background:var(--paper); color:var(--ink);
      font:17px/1.65 Georgia,"Noto Serif Devanagari",serif; }
main{ max-width:680px; margin:0 auto; padding:26px 20px 10px; }
.crumb{ font-size:.85rem; color:var(--ink-soft); margin:0 0 18px; }
.crumb a{ color:var(--accent); text-decoration:none; }
h1{ font-size:1.55rem; line-height:1.3; margin:0 0 4px; color:var(--accent); }
.deva{ font-family:"Noto Serif Devanagari",serif; font-size:1.25rem;
       margin:2px 0 16px; color:var(--saffron); }
.blurb{ margin:0 0 14px; }
.blurb span{ display:block; font-size:.95rem; color:var(--ink-soft); margin-top:4px; }
.verse{ margin:18px 0; padding:16px 18px; background:var(--card);
        border:1px solid var(--line); border-radius:14px; }
.verse blockquote{ margin:0; font-family:"Noto Serif Devanagari",serif;
        font-size:1.12rem; line-height:2; }
.verse figcaption{ margin-top:10px; font-size:.82rem; color:var(--ink-soft); }
h2{ font-size:1.05rem; margin:24px 0 10px; color:var(--accent); }
ol.themes{ margin:0; padding-left:22px; }
ol.themes li{ margin:6px 0; }
ol.themes .rng{ color:var(--saffron); font-weight:600; font-size:.8rem; white-space:nowrap; }
.cta{ display:inline-block; margin:26px 0 8px; padding:13px 22px;
      background:var(--accent); color:#FFF8EC; border-radius:12px;
      text-decoration:none; font-weight:700; font-size:1.02rem; }
footer{ max-width:680px; margin:0 auto; padding:20px 20px 34px;
        font-size:.85rem; color:var(--ink-soft); }
footer a{ color:var(--accent); text-decoration:none; }
ol.toc a{ color:var(--ink); text-decoration:none; border-bottom:1px dotted var(--ink-soft); }
section.theme{ margin:26px 0; }
h2.th{ font-size:1.02rem; color:var(--accent); margin:20px 0 10px;
       border-bottom:1px solid var(--line); padding-bottom:6px; }
h2.th .rng{ color:var(--saffron); font-weight:600; font-size:.8rem; margin-left:8px;
       white-space:nowrap; }
.v{ margin:16px 0 22px; }
.vnum{ font-size:.78rem; font-weight:700; color:var(--saffron); letter-spacing:.04em; }
.vnum a{ color:inherit; text-decoration:none; border-bottom:1px dotted var(--saffron); }
.vdev{ font-family:"Noto Serif Devanagari",serif; font-size:1.14rem; line-height:2;
       margin:2px 0 3px; }
.viast{ font-style:italic; color:var(--ink-soft); font-size:.85rem; margin:0 0 7px; }
.vtr{ margin:4px 0; font-size:.95rem; }
.vtr .para{ display:block; color:var(--ink-soft); font-size:.9rem; margin-top:2px; }
@media (prefers-color-scheme:dark){ .cta{ color:#1F1A14; background:var(--saffron); } }
/* purana chapter page: clean hairline cards; saffron only for numbers */
.np{ color:var(--ink-soft); font-size:.9rem; margin:0 0 6px; }
section.theme{ background:var(--card); border:1px solid var(--line); border-radius:12px;
               padding:16px 18px; margin:14px 0; transition:border-color .15s; }
section.theme:hover{ border-color:var(--saffron); }
.th-link{ text-decoration:none; }
.th-link h2.th{ margin:0 0 6px; border-bottom:none; padding-bottom:0; }
.th-link:hover h2.th{ color:var(--saffron); }
.tdesc{ margin:0 0 6px; color:var(--ink-soft); font-size:.95rem; }
.vrows{ margin-top:6px; }
a.vrow{ display:block; padding:10px 8px; border-top:1px solid var(--line);
        text-decoration:none; border-radius:8px; }
a.vrow:hover{ background:var(--paper); }
.vrow .vt{ color:var(--accent); font-weight:700; font-size:.9rem; }
.vrow .vt b{ color:var(--saffron); margin-right:6px; }
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
summary{ cursor:pointer; color:var(--saffron); font-weight:700; font-size:.88rem; }
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
  e.waitUntil(caches.open(CACHE)
    .then(c => c.addAll(ASSETS))
    .then(() => self.skipWaiting())
    .catch(() => self.skipWaiting()));   // a missing optional asset must not abort install
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
        .catch(() => caches.match('./index.html').then(r => r || caches.match('./')))
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
    }).catch(() => hit))
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
    _desc = (f"Read Chapter {_n} of the Bhagavad Gita ({_en}) — all {_nverses} verses "
             f"in Sanskrit with translations in English, Nepali and Hindi.")
    # Purana-style chapter page: each theme is a narrative beat whose title
    # links into the app's theme view; the full text stays folded in a
    # <details> so the eye gets the story and the crawler gets every word.
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
        _rows = "".join(
            f'<a class="vrow" href="#v{_h.escape(str(_p2["sutras"][0]["n"]))}">'
            f'<div class="vt"><b>{_h.escape(_dnum(_p2["sutras"][0]["n"]))}</b>'
            f'{_h.escape(_p2["titles"]["en"])}</div>'
            f'<div class="vd">{_h.escape(_p2["descs"]["en"])}</div></a>'
            for _p2 in _t["parts"])
        _sections.append(
            f'  <section class="theme" id="theme-{_i}">\n'
            f'    <a class="th-link" href="../../index.html#theme={_n}.{_i - 1}">'
            f'<h2 class="th">{_h.escape(_t["titles"]["en"])}'
            f'<span class="rng">{_h.escape(_drange(_t["range"]))}</span></h2></a>\n'
            f'    <p class="tdesc">{_h.escape(_t["descs"]["en"])}</p>\n'
            f'    <div class="vrows">{_rows}</div>\n'
            f'    <details id="det-{_i}"><summary>Read the verses</summary>\n'
            + "\n".join("    " + v for v in _vblocks) +
            '\n    </details>\n  </section>')
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
<title>Bhagavad Gita Chapter {_n} — {_h.escape(_en)} | Sanskrit, English, Nepali, Hindi</title>
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
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Bhagavad Gita Chapter {_n} — {_h.escape(_en)}">
<meta name="twitter:description" content="{_h.escape(_desc)}">
<meta name="twitter:image" content="{SITE_BASE}/og-card.png">
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
  <p><a class="cta" href="../../index.html#chapter={_n}&tab=study">Study chapter {_n} in the app — word-by-word meanings →</a></p>
  <p class="np">{_nverses} verses · {len(_ch["themes"])} themes — tap a theme's title to study it in the app.</p>
{_text}
  <p><a class="cta" href="../../index.html#chapter={_n}&tab=study">Study chapter {_n} in the app — word-by-word meanings →</a></p>
</main>
<footer>
  <a href="../../">← Bhagavad Gita — an Interactive Study</a><br>
  Sanskrit text: public domain · Translations © 2026 Dhruba Chapain<br>
  Created by <b>Dhruba Chapain</b>, Pokhara, Nepal.
</footer>
<script>
/* A shared verse link is /chapter/N/#vN.NN, and every verse lives inside a
   COLLAPSED <details>. Without this the reader would land on a verse the
   browser cannot scroll to, because it has no layout box while folded.
   Open the enclosing block, then scroll — and repeat on hashchange, so
   moving between verses on an already-open page behaves the same.
   Progressive enhancement: with JS off the page is still complete, the
   reader just expands "Read the verses" by hand. */
(function(){{
  function reveal(){{
    var h = location.hash;
    if(!h || h.charAt(1) !== 'v') return;
    var el;
    try{{ el = document.querySelector(h); }}catch(e){{ return; }}
    if(!el) return;
    var d = el.closest('details');
    if(d && !d.open) d.open = true;
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


# sitemap.xml + robots.txt — the crawler-facing pair. Generated rather than
# checked in, so lastmod always matches the build and the URLs follow
# SITE_BASE. Honest note: on a GitHub *project* page Google only reads
# github.io/robots.txt, so this robots.txt is advisory for Google (Search
# Console is the real channel); other crawlers do read it. The sitemap is
# what gets submitted in Search Console.
import datetime as _dt
_today = _dt.date.today().isoformat()
_urls = [f'  <url>\n    <loc>{SITE_BASE}/</loc>\n    <lastmod>{_today}</lastmod>\n    <priority>1.0</priority>\n  </url>']
for _ch in data:
    _urls.append(f'  <url>\n    <loc>{SITE_BASE}/chapter/{_ch["num"]}/</loc>\n    <lastmod>{_today}</lastmod>\n    <priority>0.8</priority>\n  </url>')
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
    a.href = '{SITE_BASE}/chapter/' + m[1] + '/#v' + m[1] + '.' + m[2];
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
    for n in ("favicon.ico", "icon-192.png", "icon-512.png",
              "icon-maskable-512.png", "apple-touch-icon.png", "og-card.png"):
        src = os.path.join(ICON_SRC, n)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(SITE_DIR, n)); copied += 1
print(f"site/: index.html + manifest + sw.js (cache {CACHE_VER}) + sitemap + robots + {copied} icons  ->  {SITE_DIR}")
