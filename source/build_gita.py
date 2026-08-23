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

if problems:
    print("\nMANUAL-EDIT AUDIT FAILED")
    for x in problems: print("  ✗", x)
    raise SystemExit(1)
print("manual-edit audit: NONE ✓")

# ---------------- HTML template (4-pāda display) ----------------
HTML = r"""<!DOCTYPE html>
<!--
  Bhagavad Gita — Interactive Study
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
  https://github.com/chapain/Bhagavad-Gita
-->
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#0F4C5C" id="themeColor">
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
<meta property="og:site_name" content="Bhagavad Gita — Interactive Study">
<meta property="og:title" content="Bhagavad Gita — 700 verses, trilingual">
<meta property="og:description" content="All 18 chapters in English · नेपाली · हिन्दी, with word-by-word meanings for every verse. Works offline.">
<meta property="og:url" content="__BASE__/">
<meta property="og:image" content="__BASE__/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ॐ श्रीमद्भगवद्गीता — Bhagavad Gita, 700 verses">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="ne_NP">
<meta property="og:locale:alternate" content="hi_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Bhagavad Gita — 700 verses, trilingual">
<meta name="twitter:description" content="All 18 chapters in English · नेपाली · हिन्दी, with word-by-word meanings. Works offline.">
<meta name="twitter:image" content="__BASE__/og-card.png">

<!-- Icons: relative paths, so they resolve on any host or sub-path. -->
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<title>Bhagavad Gita — Interactive Study</title>
<style>
__FONTS__
  /* ---- colour tokens -------------------------------------------------
     Light is the default. The dark theme below overrides these same names,
     so every rule keeps using var(--x) and nothing else has to change.
     --on-accent is the text colour that sits on saffron/teal fills; it stays
     near-cream in both themes because both fills stay dark enough for it.  */
  :root{ --saffron:#E8912C; --saffron-dark:#C97A20; --saffron-soft:#FBE3C0; --teal:#0F4C5C; --teal-mid:#1E6E7E;
         --teal-soft:#DDEFF2; --cream:#FFF8EC; --ink:#2A2118; --ink-soft:#5C5142; --paper:#FFFFFF; --line:#E7D9C2;
         --on-accent:#FFF8EC; --hdr-a:#0F4C5C; --hdr-b:#17566B; --hdr-c:#1E6E7E; --hdr-sub:#CDE7EE;
         --toolbar:#FDF3E0; --field:#FFFFFF; --muted:#9AA0A6; --danger:#C0392B;
         --shadow:42,33,24; --scrim:rgba(15,42,52,.72); --fade:255,248,236;
         --chip:rgba(255,248,236,.12); --chip-hover:rgba(255,248,236,.25); --chip-line:rgba(255,248,236,.35); }

  /* ---- dark theme ----------------------------------------------------
     Warm, not neutral: a dark brown-black keeps the manuscript feel rather
     than looking like a generic app. Never pure black and never pure white —
     Devanagari has fine strokes, and maximum contrast makes them shimmer.
     Saffron and teal are both lifted, because the light-mode values go muddy
     against a dark ground.                                                */
  html[data-theme="dark"]{
    --saffron:#F0A64A; --saffron-dark:#E8912C; --saffron-soft:#4A3418;
    --teal:#7FD4E8; --teal-mid:#9FE0EF; --teal-soft:#123039;
    --cream:#17130E; --paper:#211B14; --ink:#F2E7D5; --ink-soft:#B8A88F; --line:#3A2F22;
    --on-accent:#1A1209; --hdr-a:#0A2830; --hdr-b:#0D323C; --hdr-c:#123F4B; --hdr-sub:#CFE6EC;
    --toolbar:#1E1811; --field:#2A2219; --muted:#8A7F6E; --danger:#E86B5C;
    --shadow:0,0,0; --scrim:rgba(0,0,0,.78); --fade:23,19,14;
    --chip:rgba(242,231,213,.10); --chip-hover:rgba(242,231,213,.20); --chip-line:rgba(242,231,213,.28);
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  body{ font-family:"Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif; color:var(--ink);
        background:var(--cream); line-height:1.55; display:flex; flex-direction:column; min-height:100vh;}
  header{ background:linear-gradient(135deg, var(--hdr-a) 0%, var(--hdr-b) 55%, var(--hdr-c) 100%); color:var(--hdr-sub);
          padding:24px 20px; border-bottom:5px solid var(--saffron);}
  .header-inner{ max-width:1180px; margin:0 auto; display:flex; align-items:center; gap:16px; flex-wrap:wrap;}
  .header-inner .om{ font-family:Georgia,serif; font-size:1.7rem; color:var(--saffron);}
  .header-inner h1{ font-family:Georgia,serif; font-size:1.4rem;}
  .header-inner .tag{ color:var(--hdr-sub); font-size:.9rem; margin-left:auto; text-align:right;}
  .langbar{ display:flex; gap:6px; margin-left:auto;}
  .lang-btn{ background:var(--chip); color:var(--hdr-sub); border:2px solid var(--chip-line); padding:6px 14px; border-radius:999px; cursor:pointer; font-size:.85rem; font-weight:600;}
  .lang-btn:hover{ background:var(--chip-hover);}
  .lang-btn.on{ background:var(--saffron); border-color:var(--saffron); color:var(--on-accent);}
  /* the theme toggle lives in the language bar; it must not stretch like the
     language buttons do on mobile, so it opts out of flex:1 and stays square */
  .theme-btn{ flex:0 0 auto !important; min-width:40px; padding:6px 12px; font-size:1.05rem; line-height:1; color:var(--saffron); border-color:var(--chip-line);}
  .theme-btn:hover{ background:var(--chip-hover);}
  @media (max-width:640px){ .langbar{ width:100%; justify-content:center; margin-left:0;} .lang-btn{ flex:1; text-align:center;} }
  .header-inner .tag b{ color:var(--saffron); font-family:Georgia,serif; font-size:1.15rem;}
  .wrap{ max-width:1180px; margin:0 auto; padding:22px 20px 60px; width:100%; flex:1;}
  .crumbs{ display:flex; align-items:center; gap:8px; font-size:.9rem; color:var(--ink-soft); margin-bottom:18px; flex-wrap:wrap;}
  /* Search/Favorites show one .back-top button (see renderCrumbs), so .crumbs is
     just its wrapper. Long chapter names ellipsise rather than wrap. */
  .crumbs .back-top{ margin:0 0 4px; max-width:100%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
  .view-title{ font-family:Georgia,serif; font-size:1.7rem; color:var(--teal); margin-bottom:6px;}
  .view-sub{ color:var(--ink-soft); font-size:.98rem; margin-bottom:22px; max-width:880px;}
  .grid{ display:grid; gap:20px; }
  .grid.chapters{ grid-template-columns:repeat(auto-fill, minmax(250px,1fr)); }
  .grid.themes{ grid-template-columns:repeat(auto-fill, minmax(260px,1fr)); }
  .grid.verses{ grid-template-columns:repeat(auto-fill, minmax(300px,1fr)); gap:14px; }
  .card{ background:var(--paper); border:2px solid var(--line); border-radius:16px; padding:16px 18px;
         box-shadow:0 6px 18px rgba(var(--shadow),.08); cursor:pointer; transition:.18s; display:flex; flex-direction:column;}
  .card:hover{ transform:translateY(-4px); box-shadow:0 12px 26px rgba(var(--shadow),.14); border-color:var(--saffron);}
  .card .chip{ align-self:flex-start; background:var(--saffron); color:var(--on-accent); font-weight:700; font-size:.72rem;
               letter-spacing:.1em; text-transform:uppercase; padding:4px 10px; border-radius:999px; margin-bottom:8px;}
  .card .chip.locked{ background:var(--muted);}
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
  .mini{ background:var(--paper); border:2px solid var(--line); border-radius:12px; padding:11px 14px; cursor:pointer;
         transition:.15s; box-shadow:0 4px 12px rgba(var(--shadow),.06);}
  .mini:hover{ border-color:var(--saffron); transform:translateY(-3px); box-shadow:0 10px 20px rgba(var(--shadow),.12);}
  .mini .vnum{ font-family:Georgia,serif; font-weight:700; color:var(--saffron-dark); font-size:.95rem; margin-bottom:4px;}
  .mini .padas{ font-family:"Noto Serif Devanagari", Georgia, serif; color:var(--teal); font-size:1.02rem; line-height:1.5; background:var(--cream); border-radius:8px; padding:7px 9px;}
  .mini .padas .spk{ display:block; color:var(--saffron-dark); font-size:.82rem; font-style:italic; margin-bottom:2px;}
  .mini .padas .gline{ display:block; line-height:1.6;}
  .mini .padas .gp{ display:inline;}
  .mini .vhint{ color:var(--ink-soft); font-size:.78rem; font-style:italic; line-height:1.4; margin-top:6px;}
  .back-top{ display:inline-block; margin:4px 0 16px; background:none; border:2px solid var(--teal); color:var(--teal);
             font-weight:700; padding:8px 18px; border-radius:999px; cursor:pointer; font-size:.9rem;}
  .back-top:hover{ background:var(--teal); color:var(--on-accent);}
  /* the same back button repeated at the end of a long list, so a reader who has
     scrolled to the bottom does not have to scroll all the way up again */
  /* left, not centred: this is the same button as the crumb at the top of the
     page, so it sits on the same left edge as every heading and card. A back
     affordance is an escape hatch, not a call to action — findable, not loud. */
  .back-foot{ margin:26px 0 4px; padding-top:20px; border-top:2px solid var(--line);}

  /* ---- favourites: ordering + a personal note ---- */
  .fav-tools{ display:inline-flex; gap:6px; align-items:center; margin-left:auto;}
  .fav-move{ background:none; border:2px solid var(--line); color:var(--teal); border-radius:8px;
             width:30px; height:30px; font-weight:700; cursor:pointer; line-height:1; padding:0;}
  .fav-move:hover:not(:disabled){ border-color:var(--teal); background:var(--teal-soft);}
  .fav-move:disabled{ opacity:.3; cursor:default;}
  .fav-note{ margin-top:9px; display:flex; gap:8px; align-items:flex-start;}
  .fav-note label{ font-size:.74rem; font-weight:700; color:var(--ink-soft); text-transform:uppercase;
                   letter-spacing:.04em; padding-top:7px; flex:0 0 auto;}
  .fav-note textarea{ flex:1; border:2px solid var(--line); border-radius:8px; padding:5px 9px;
                      font:inherit; font-size:.88rem; background:var(--cream); color:var(--ink);
                      resize:none; overflow:hidden; min-height:34px;}
  .fav-note textarea:focus{ outline:none; border-color:var(--saffron); background:var(--paper);}

  /* ---- continuous reading ---- */
  .read-btn{ display:inline-block; margin:0 0 18px; background:var(--teal); color:var(--on-accent);
             border:none; padding:9px 20px; border-radius:999px; cursor:pointer; font-weight:700; font-size:.9rem;}
  .read-btn:hover{ background:var(--teal-mid);}
  .read-tabs{ display:flex; gap:8px; margin:0 0 16px; flex-wrap:wrap;}
  .read-tab{ background:var(--paper); border:2px solid var(--line); color:var(--teal); font-weight:700;
             font-size:.9rem; padding:9px 20px; border-radius:999px; cursor:pointer; min-height:44px;
             font-family:"Noto Serif Devanagari", Georgia, serif; transition:.15s;}
  .read-tab:hover{ border-color:var(--saffron); background:var(--saffron-soft);}
  .read-tab.on{ background:var(--saffron); border-color:var(--saffron); color:var(--on-accent);}
  /* mūla: the verses run closer together, the way a printed pāṭha is set */
  .reading.mula .rd-v{ padding:9px 0 10px;}
  .reading.mula .rd-deva{ margin-bottom:0;}
  .reading{ background:var(--paper); border:2px solid var(--line); border-radius:14px; padding:14px 18px 6px;}
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
  .back-foot .back-top{ margin:0;}
  .mini-crumb{ display:flex; gap:10px; margin:2px 0 16px; flex-wrap:wrap;}
  .mini-crumb .bc-btn{ background:var(--paper); border:2px solid var(--line); border-radius:12px; cursor:pointer;
             display:flex; flex-direction:column; align-items:flex-start; gap:1px; padding:8px 14px; transition:.15s;}
  .mini-crumb .bc-btn:hover{ border-color:var(--saffron); background:var(--saffron-soft); transform:translateY(-2px);}
  .mini-crumb .bc-num{ font-weight:700; color:var(--teal); font-size:.95rem;}
  .mini-crumb .bc-name{ color:var(--ink-soft); font-size:.8rem;}
  .mini-crumb .bc-cur{ background:var(--saffron-soft); border:2px solid var(--saffron); border-radius:12px;
             display:flex; flex-direction:column; align-items:flex-start; gap:1px; padding:8px 14px;}
  .mini-crumb .bc-cur .bc-num{ color:var(--saffron-dark);}
  .mini-crumb .bc-sep{ align-self:center; color:var(--line); font-weight:800; font-size:1rem; padding:0 2px;}

  .sec-tabs{ display:flex; gap:10px; flex-wrap:wrap; margin:2px 0 22px;}
  .sec-tab{ background:var(--paper); border:2px solid var(--line); color:var(--teal); font-weight:700; font-size:.95rem;
            padding:10px 20px; border-radius:12px; cursor:pointer; transition:.15s; font-family:"Noto Serif Devanagari", Georgia, serif;}
  .sec-tab:hover{ border-color:var(--saffron); background:var(--saffron-soft);}
  .sec-tab.on{ background:var(--saffron); border-color:var(--saffron); color:var(--on-accent);}
  .sec-tab .sec-range{ font-family:"Segoe UI", system-ui, sans-serif; font-size:.78rem; opacity:.85; margin-left:6px; font-weight:600;}

  .welcome{ text-align:center; padding:44px 12px 30px; max-width:860px; margin:0 auto;}
  .welcome .w-om{ font-size:3.6rem; color:var(--saffron); line-height:1; margin-bottom:14px;}
  .welcome .view-title{ font-size:2rem;}
  .welcome .tool-btn.big{ font-size:1.02rem; padding:14px 36px; margin-top:20px;}
  .welcome .w-foot{ color:var(--ink-soft); font-size:.9rem; margin-top:30px; letter-spacing:.05em;}
  .welcome .w-day{ max-width:560px; margin:26px auto 6px; background:var(--paper); border:2px solid var(--saffron); border-radius:16px;
                   padding:18px 22px; cursor:pointer; box-shadow:0 10px 26px rgba(var(--shadow),.12); transition:.18s; text-align:left;}
  .welcome .w-day:hover{ transform:translateY(-3px); box-shadow:0 16px 32px rgba(var(--shadow),.18);}
  .welcome .wd-label{ font-family:Georgia,serif; font-weight:700; color:var(--saffron-dark); font-size:1.05rem; margin-bottom:10px; text-align:center; letter-spacing:.04em;}
  .welcome .wd-verse{ font-family:"Noto Serif Devanagari", Georgia, serif; color:var(--teal); font-size:1.15rem; line-height:1.6; text-align:center;}
  .welcome .wd-ref{ color:var(--ink-soft); font-size:.88rem; text-align:center; margin-top:8px;}
  .welcome .wd-open{ color:var(--teal); font-weight:700; font-size:.9rem; text-align:center; margin-top:8px;}

  .grid.sections{ grid-template-columns:repeat(auto-fill, minmax(270px,1fr));}
  .card.sect{ border-top:6px solid var(--saffron);}
  .card.sect h3{ font-family:"Noto Serif Devanagari", Georgia, serif; font-size:1.32rem;}
  .card.sect p{ font-size:.92rem;}
  /* The alternative route, after the three cards: "or skip the grouping and see
     all eighteen". Centred because it is a terminal choice that closes the page —
     unlike a back button, which belongs on the left text edge. Styled as a quiet
     outlined pill so it matches the app's other buttons and stays lighter than
     the three cards above it; it used to be the only underlined text anywhere. */
  .sect-all{ margin-top:34px; text-align:center;}
  .sect-all .browse-all{ display:inline-block; color:var(--teal); font-size:.9rem; font-weight:600;
             cursor:pointer; border:2px solid var(--line); background:var(--paper);
             padding:10px 22px; border-radius:999px; min-height:44px; line-height:22px;
             transition:.15s;}
  .sect-all .browse-all:hover{ border-color:var(--teal); background:var(--teal-soft);}


  .toolbar{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; padding:12px 20px; background:var(--toolbar); border-bottom:2px solid var(--line);}
  .toolbar .searchwrap{ display:flex; align-items:center; gap:6px; flex:1; min-width:240px; max-width:640px;}
  .toolbar input[type=search]{ flex:1; padding:9px 14px; border:2px solid var(--line); border-radius:999px; font-size:.92rem; background:var(--field); color:var(--ink); outline:none;}
  .toolbar input[type=search]:focus{ border-color:var(--saffron);}
  .tool-btn{ background:var(--paper); border:2px solid var(--line); color:var(--teal); font-weight:700; font-size:.85rem; padding:8px 16px; border-radius:999px; cursor:pointer; transition:.15s;}
  .tool-btn:hover{ border-color:var(--saffron); background:var(--saffron-soft);}
  .tool-btn.primary{ background:var(--saffron); border-color:var(--saffron); color:var(--on-accent);}
  .tool-btn.primary:hover{ background:var(--saffron-dark);}
  .tool-btn.clear{ color:var(--ink-soft);}
  .fav-btn{ background:var(--saffron-soft); border:2px solid var(--saffron); color:var(--saffron-dark); font-weight:700; font-size:.8rem; padding:4px 12px; border-radius:999px; cursor:pointer; margin-left:10px;}
  .fav-btn.saved{ background:var(--saffron); color:var(--on-accent);}
  .res-head{ font-family:Georgia,serif; font-size:1.25rem; color:var(--teal); margin-bottom:4px;}
  .res-count{ color:var(--ink-soft); font-size:.9rem; margin-bottom:16px;}
  .res-card{ background:var(--paper); border:2px solid var(--line); border-radius:12px; padding:12px 16px; margin-bottom:12px; cursor:pointer; transition:.15s;}
  .res-card:hover{ border-color:var(--saffron); transform:translateY(-2px); box-shadow:0 8px 18px rgba(var(--shadow),.1);}
  .res-top{ display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; margin-bottom:6px;}
  .res-num{ font-family:Georgia,serif; font-weight:700; color:var(--saffron-dark);}
  .res-title{ font-weight:600; color:var(--teal); font-size:.9rem;}
  .res-deva{ font-family:"Noto Serif Devanagari", Georgia, serif; color:var(--teal); font-size:1rem; line-height:1.55; background:var(--cream); border-radius:8px; padding:7px 10px; margin-bottom:6px;}
  .res-lit{ color:var(--ink-soft); font-size:.88rem; line-height:1.5;}
  .res-remove{ margin-left:auto; background:none; border:2px solid var(--line); color:var(--ink-soft); font-size:.72rem; font-weight:700; padding:3px 10px; border-radius:999px; cursor:pointer;}
  .res-remove:hover{ border-color:var(--danger); color:var(--danger);}
  .modal-bg{ position:fixed; inset:0; background:var(--scrim); display:none; align-items:center; justify-content:center; z-index:50; padding:20px;}
  .modal-bg.open{ display:flex;}
  .modal{ background:var(--cream); border-radius:20px; max-width:820px; width:100%; max-height:92vh; overflow-y:auto;
          box-shadow:0 24px 60px rgba(0,0,0,.45); border:4px solid var(--saffron); position:relative; padding:24px 30px 28px;}
  .modal .m-close{ position:sticky; top:0; float:right; background:var(--saffron); color:var(--on-accent); border:none; width:38px;
                   height:38px; border-radius:50%; font-size:1.1rem; cursor:pointer; font-weight:700; margin:-8px -12px 0 0;}
  .m-num{ font-family:Georgia,serif; font-size:1.4rem; color:var(--saffron-dark); font-weight:700;}
  .m-part{ color:var(--teal); font-size:.88rem; font-weight:600; margin-bottom:2px;}
  .m-meter{ display:inline-block; background:var(--teal-soft); color:var(--teal); font-size:.78rem; font-weight:700;
            padding:3px 12px; border-radius:999px; margin:6px 0 12px; letter-spacing:.03em;}
  .m-verse{ background:var(--paper); border:2px solid var(--line); border-radius:14px; padding:16px 18px; margin:6px 0 4px;}
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
  /* four pāda boxes in a 2x2 grid */
  .m-verse .pada-grid{ display:flex; flex-direction:column; gap:12px;}
  .m-verse .pada-row{ display:flex; gap:12px;}
  .m-verse .pada-box{ flex:1 1 0; min-width:0; max-width:100%; background:var(--paper); border:2px solid var(--line); border-radius:12px; padding:10px 14px; cursor:pointer; transition:border-color .15s, background .15s;}
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
  .m-line.para .lb{ background:var(--saffron);}
  .m-nav{ display:flex; justify-content:space-between; align-items:center; margin-top:22px; gap:10px;}
  .m-tail{ display:none;}   /* only needed where .m-nav is sticky (phones) */
  .m-nav button{ background:var(--teal); color:var(--on-accent); border:none; padding:10px 18px; border-radius:999px; cursor:pointer; font-weight:600; font-size:.9rem;}
  .m-nav button:hover{ background:var(--teal-mid);} .m-nav button:disabled{ opacity:.35; cursor:default;}
  .m-nav .m-random{ margin:0 auto; background:var(--saffron); color:var(--on-accent); border:none; padding:12px 26px; border-radius:999px; cursor:pointer; font-weight:700; font-size:.98rem; font-family:"Noto Serif Devanagari", Georgia, serif;}
  .m-nav .m-random:hover{ background:var(--saffron-dark);}
  .m-nav .m-back{ background:var(--teal-soft); color:var(--teal); border:2px solid var(--teal); padding:10px 18px; border-radius:999px; cursor:pointer; font-weight:700; font-size:.9rem;}
  .m-nav .m-back:hover{ background:var(--teal); color:var(--on-accent);}

  .m-count{ color:var(--ink-soft); font-size:.85rem; font-weight:600;}
  footer{ text-align:center; color:var(--ink-soft); font-size:.82rem; padding:18px 20px 26px; border-top:2px solid var(--line);}
  /* plain inline text — no flex gap, or the <b> would push the comma away */
  footer .credit{ margin-top:10px; padding-top:10px; border-top:1px dashed var(--line);
                  font-size:.8rem; color:var(--ink-soft); display:block; text-align:center;}
  footer .credit b{ color:var(--teal); font-weight:700;}
  .fade-in{ animation:fadein .28s ease;} @keyframes fadein{ from{opacity:0; transform:translateY(6px);} to{opacity:1; transform:none;} }
  @media (max-width:640px){ .modal{ padding:16px 16px 20px;} .m-verse td.pd{ font-size:1.12rem;} }

  /* ==================== MOBILE / TOUCH (Android · iOS) ==================== */
  html{ -webkit-text-size-adjust:100%; text-size-adjust:100%; }
  body{ -webkit-tap-highlight-color:rgba(232,145,44,.18); overscroll-behavior-y:none; }
  button, .card, .mini, .res-card, .sec-tab, .pada-box, .spk-line, .lang-btn{ -webkit-tap-highlight-color:transparent; touch-action:manipulation; }
  input, button, select, textarea{ font-family:inherit; }
  /* iOS zooms any input whose font-size is < 16px on focus */
  .toolbar input[type=search]{ font-size:16px; }
  .modal, .wrap{ -webkit-overflow-scrolling:touch; }
  /* Hover lifts are a mouse idiom — on touch they stick after a tap */
  @media (hover:none){
    .card:hover, .mini:hover, .res-card:hover, .mini-crumb .bc-btn:hover, .welcome .w-day:hover{ transform:none; box-shadow:0 6px 18px rgba(var(--shadow),.08); }
    .card:active, .mini:active, .res-card:active, .welcome .w-day:active{ transform:scale(.985); border-color:var(--saffron); }
    .tool-btn:active, .lang-btn:active, .sec-tab:active, .m-nav button:active{ filter:brightness(.93); }
    .pada-box:hover{ background:var(--paper); border-color:var(--line); }
    .pada-box:active{ background:var(--saffron-soft); border-color:var(--saffron); }
    .m-verse .spk-line:hover{ background:none; }
  }

  @media (max-width:760px){
    /* ---- header ---- */
    header{ padding:12px 14px calc(10px + env(safe-area-inset-bottom,0px)); border-bottom-width:4px;
            padding-left:calc(14px + env(safe-area-inset-left,0px)); padding-right:calc(14px + env(safe-area-inset-right,0px));
            padding-top:calc(12px + env(safe-area-inset-top,0px)); }
    .header-inner{ gap:10px; }
    .header-inner .om{ font-size:1.5rem; }
    .header-inner h1{ font-size:1.05rem; line-height:1.3; }
    #appSub{ display:none; }
    .header-inner .tag{ display:none; }
    .langbar{ width:100%; gap:8px; margin-left:0; }
    .lang-btn{ flex:1; padding:9px 6px; font-size:.82rem; min-height:40px; }

    /* ---- toolbar: sticky so search / home stay reachable ---- */
    .toolbar{ position:sticky; top:0; z-index:30; gap:8px; padding:9px 12px;
              padding-left:calc(12px + env(safe-area-inset-left,0px)); padding-right:calc(12px + env(safe-area-inset-right,0px));
              box-shadow:0 2px 10px rgba(var(--shadow),.07); }
    .toolbar .searchwrap{ order:-1; width:100%; flex:1 0 100%; max-width:none; min-width:0; }
    .toolbar input[type=search]{ min-height:42px; }
    .toolbar .tool-btn{ flex:1; min-height:40px; padding:9px 8px; font-size:.82rem; white-space:nowrap; }
    .toolbar .tool-btn.clear{ flex:0 0 auto; }

    /* ---- content ---- */
    .wrap{ padding:16px 14px 40px; padding-left:calc(14px + env(safe-area-inset-left,0px)); padding-right:calc(14px + env(safe-area-inset-right,0px)); }
    .view-title{ font-size:1.35rem; }
    .view-sub{ font-size:.92rem; margin-bottom:16px; }
    .crumbs{ font-size:.84rem; gap:6px; margin-bottom:14px; }
    .crumbs .back-top{ font-size:.82rem; padding:7px 14px; min-height:36px; }
    .grid{ gap:12px; }
    .grid.chapters, .grid.themes, .grid.verses, .grid.sections{ grid-template-columns:1fr; }
    .card{ padding:14px 16px; border-radius:14px; }
    .card h3{ font-size:1.08rem; }
    .card.sect h3{ font-size:1.2rem; }
    .part-head{ gap:6px; }
    .part-head .ptitle{ font-size:1.1rem; }
    .part-head .pdesc{ margin-left:0; flex:1 0 100%; }
    .sec-tabs{ gap:8px; }
    .sec-tab{ flex:1 1 auto; padding:11px 14px; font-size:.9rem; min-height:44px; }
    .mini .padas{ font-size:1.06rem; }
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
    .welcome .wd-verse{ font-size:1.05rem; }

    /* ---- verse modal: full-screen sheet ---- */
    .modal-bg{ padding:0; align-items:stretch; }
    .modal{ max-width:none; width:100%; max-height:none; height:100%; border-radius:0; border:none;
            border-top:4px solid var(--saffron);
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
           border:2px solid var(--saffron); border-radius:16px; padding:22px 22px 24px;
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

<header>
  <div class="header-inner">
    <span class="om">ॐ</span>
    <div>
      <h1 id="appTitle">Bhagavad Gita — Interactive Study</h1>
      <div id="appSub" style="font-size:.82rem; color:var(--hdr-sub);">श्रीमद्भगवद्गीता · chapters → themes → subthemes → verses · each verse in its 4 pādas</div>
    </div>
    <div class="tag"><span id="tagVerses">18 chapters · 700 verses · study edition</span></div>
    <div class="langbar" id="langbar">
      <button class="lang-btn on" data-lang="en" onclick="setLang('en')">English</button>
      <button class="lang-btn" data-lang="ne" onclick="setLang('ne')">नेपाली</button>
      <button class="lang-btn" data-lang="hi" onclick="setLang('hi')">हिन्दी</button>
      <button class="lang-btn theme-btn" id="themeBtn" onclick="toggleTheme()" aria-label="Toggle dark mode"><span id="themeIcon">☾</span></button>
    </div>
  </div>
</header>

<div class="toolbar">
  <button class="tool-btn" onclick="goHome()" id="homeBtn">🏠 Home</button>
  <div class="searchwrap">
    <input type="search" id="searchInput" placeholder="🔍 …" aria-label="search" oninput="onSearchInput(this.value)" onkeydown="if(event.key==='Enter')doSearch()">
    <button class="tool-btn clear" onclick="clearSearch()" id="clearBtn">Clear</button>
  </div>
  <button class="tool-btn" onclick="randomVerse()" id="randomBtn">Random</button>
  <button class="tool-btn" onclick="showFavorites()" id="favBtnTool">☆ Favorites</button>
</div>

<div class="wrap">
  <nav class="crumbs" id="crumbs"></nav>
  <main id="view"></main>

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
  <div id="appFooter">ॐ · A study edition of the Bhagavad Gita — every verse shown in its traditional four quarters (pādas), with Devanagari, transliteration, word-by-word meanings, a literal translation and a flowing paraphrase.</div>
  <!-- Credit lives in its own element: applyStatic() replaces #appFooter's
       textContent on every language switch and would otherwise wipe it. -->
  <div class="credit">Created by <b>Dhruba Chapain</b>, Pokhara, Nepal.</div>
</footer>

<div class="modal-bg" id="modalBg" onclick="if(event.target===this)closeModal()">
  <div class="modal" id="modal"></div>
</div>

<script>
const DATA = __DATA__;
const UI = __UI__;
const state = { chapter:null, theme:null, idx:0, lang:'en', view:'welcome', section:null };
function T(o){ return o ? (o[state.lang] || o.en || o) : ''; }
function L(k){ const u = UI[state.lang] || UI.en; return (u[k] !== undefined) ? u[k] : k; }
function Lof(cur,tot){ const rev=['ne','hi'].includes(state.lang);
  const c = numL(cur), t = numL(tot);   // numL → Devanagari digits in ne/hi
  return rev ? `${t} ${L('of')} ${c}` : `${c} ${L('of')} ${t}`; }
function applyStatic(){ $('#appTitle').textContent = L('app_title'); $('#appSub').textContent = L('app_sub');
  $('#tagVerses').textContent = L('tag_sub'); $('#appFooter').textContent = L('footer');
  $('#clearBtn').textContent = L('clear');
  $('#randomBtn').textContent = L('random'); $('#favBtnTool').textContent = L('favorites');
  $('#homeBtn').textContent = L('home');
  $('#searchInput').placeholder = '🔍 ' + L('search_ph'); }
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
  else {
    const ch = state.chapter, th = state.theme;
    if(ch == null) showChapters(state.section || 0);
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
(function buildIndex(){
  DATA.forEach((ch, ci)=> ch.themes.forEach((t, ti)=>{
    t.parts.forEach(p=> p.sutras.forEach((s, k)=> VERSES.push({ id:s.n, norm:fmtN(s.n), ci, ti, si:flatIndex(t,p,k) })));
  }));
})();
function verseLoc(id){ return VERSES.find(v=>v.id===id); }
function verseAt(loc){ const t = DATA[loc.ci].themes[loc.ti]; return sutraAt(t, loc.si).s; }
function normTxt(s){ return String(s||'').toLowerCase().replace(/[\u0300-\u036f]/g,''); }
function fmtN(n){ const m = String(n).split('.'); return m.length===2 ? (parseInt(m[0],10)+'.'+parseInt(m[1],10)) : String(n); }
function fmtRange(r){ const parts = String(r).split('–').map(x=>x.trim()?fmtN(x):x); return (parts.length===2 && parts[0]===parts[1]) ? parts[0] : parts.join('–'); }
function digitNorm(s){ return String(s).replace(/[०-९]/g, d => '0123456789'['०१२३४५६७८९'.indexOf(d)]); }
function devaDigits(s){ return String(s).replace(/[0-9]/g, d => '०१२३४५६७८९'[d]); }
function numL(n){ return (state.lang==='ne'||state.lang==='hi') ? devaDigits(n) : String(n); }
/* Display-only variants of fmtN / fmtRange: identical text, but with Devanagari
   digits in ne/hi. The plain fmtN/fmtRange stay ASCII because VERSES[].norm and
   the search matcher compare against them. */
function fmtNL(n){ return numL(fmtN(n)); }
function fmtRangeL(r){ return numL(fmtRange(r)); }
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
(function(){ DATA.forEach(ch=> ch.themes.forEach(t=> t.parts.forEach(p=> p.sutras.forEach(s=> VERSE_TEXT.push(verseSearchText(s)))))); })();

// ---------- search ----------
let searchTimer = null;
function onSearchInput(v){ clearTimeout(searchTimer); searchTimer = setTimeout(doSearch, 220); }
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
      return `<div class="mini" onclick="openModal(${loc.ci},${loc.ti},${loc.si},'search',${i})">
        <div class="vnum">${esc(fmtNL(v.n))} · ${esc(T(ch.names))}</div>
        <div class="padas">${padaBlockDeva(v)}</div>
        <div class="vhint">${esc(T(v.lits))}</div>
      </div>`;}).join('')}</div>`;
}
function clearSearch(){
  $('#searchInput').value = '';
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
  const icon = $('#themeIcon'); if(icon) icon.textContent = dark ? '☀' : '☾';
  const btn = $('#themeBtn');
  if(btn) btn.setAttribute('aria-label', dark ? L('theme_light') : L('theme_dark'));
  // colour the phone's status bar / address bar to match
  const mc = document.getElementById('themeColor');
  if(mc) mc.setAttribute('content', dark ? '#0A2830' : '#0F4C5C');
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

function favNoteLoad(){ try{ return JSON.parse(localStorage.getItem('gitaFavNotes') || '{}'); }catch(e){ return {}; } }
function favNoteSave(){ try{ localStorage.setItem('gitaFavNotes', JSON.stringify(FAVNOTE)); }catch(e){} }
function favLoad(){ try{ return JSON.parse(localStorage.getItem('gitaFavs') || '[]'); }catch(e){ return []; } }
FAV = favLoad(); FAVNOTE = favNoteLoad();
function favSave(){ try{ localStorage.setItem('gitaFavs', JSON.stringify(FAV)); }catch(e){} }
function toggleFav(id){
  const i = FAV.indexOf(id);
  if(i >= 0) FAV.splice(i,1); else FAV.push(id);
  favSave();
  const b = document.getElementById('favBtn');
  if(b){ const on = FAV.includes(id); b.textContent = on ? L('saved_verse') : L('save_verse'); b.classList.toggle('saved', on); }
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
  if(!o){ showChapters(state.section || 0); return; }
  $('#searchInput').value = '';
  if(o.view === 'welcome') showWelcome();
  else if(o.view === 'sections') showSections();
  else if(o.view === 'verses' && o.chapter != null && o.theme != null) showVerses(o.chapter, o.theme);
  else if(o.view === 'themes' && o.chapter != null) showThemes(o.chapter);
  else showChapters(o.section || 0);
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
  if(state.keepScroll) return;
  try{ window.scrollTo({top:0, behavior:'auto'}); }catch(e){ window.scrollTo(0,0); }
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
  } else if(o.view === 'sections'){
    label = L('sections_title');        action = ()=>clear(showSections);
  } else {
    label = L('chapters');              action = ()=>clear(()=>showChapters(0));
  }

  const b = document.createElement('button');
  b.className = 'back-top';
  b.textContent = L('back_to_x').replace('{x}', label);
  b.title = b.textContent; b.setAttribute('aria-label', b.textContent);
  b.onclick = action;
  crumbs.appendChild(b);
}

function showChapters(section){
  if(section === undefined) section = state.section || 0;
  state.view='chapters'; state.section = section || null; state.chapter=null; state.theme=null; renderCrumbs();
  const list = section ? DATA.filter(ch => ch.num >= (section-1)*6+1 && ch.num <= section*6) : DATA;
  let html;
  if(section){
    html = `<button class="back-top" onclick="showSections()">${esc(L('back_ways'))}</button>
      ${sectionTabs()}`;
  } else {
    html = `<div class="view-title fade-in">${esc(L('choose_chapter'))}</div>
      <div class="view-sub fade-in">${esc(L('choose_chapter_sub'))}</div>`;
  }
  view.innerHTML = html + `
    <div class="grid chapters fade-in">
      ${list.map(ch=>{
        const ci = DATA.indexOf(ch);
        return `<div class="card" onclick="showThemes(${ci})">
          <span class="chip">${L('chapter')} ${numL(ch.num)}</span>
          <h3>${esc(T(ch.names))}</h3>
          <p>${esc(T(ch.subs))}</p>
          <div class="meta">${numL(ch.verses)} ${L('verses')}</div>
          <div class="go">${L('open_themes')}</div>
        </div>`;}).join('')}
    </div>` + (section ? backFoot('showSections()', L('back_ways')) : '');
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
      <h1 class="view-title">${esc(L('welcome_title'))}</h1>
      <p class="view-sub">${esc(L('welcome_sub'))}</p>
      ${(()=>{ const dv = dayVerse(); const c = DATA[dv.ci], v = verseAt(dv);
        return `<div class="w-day fade-in" onclick="openModal(${dv.ci},${dv.ti},${dv.si},'book')">
          <div class="wd-label">${esc(L('verse_of_day'))}</div>
          <div class="wd-verse">${padaBlockDeva(v)}</div>
          <div class="wd-ref">${esc(fmtNL(v.n))} · ${esc(T(c.names))}</div>
          <div class="wd-open">${esc(L('open_verse'))} →</div>
        </div>`; })()}
      <button class="tool-btn primary big" onclick="showSections()">${esc(L('welcome_enter'))}</button>
      <div class="w-foot">${esc(L('welcome_foot'))}</div>
    </div>`;
}
function sectionCard(k, chip, title, desc){
  return `<div class="card sect" onclick="showChapters(${k})">
    <span class="chip">${esc(chip)}</span>
    <h3>${esc(title)}</h3>
    <p>${esc(desc)}</p>
    <div class="go">${esc(L('open_themes'))}</div>
  </div>`;
}
function showSections(){
  state.view='sections'; state.chapter=null; state.theme=null; state.section=null; renderCrumbs();
  view.innerHTML = `
    <div class="view-title fade-in">${esc(L('sections_title'))}</div>
    <div class="view-sub fade-in">${esc(L('sections_sub'))}</div>
    <div class="grid sections fade-in">
      ${sectionCard(1, chaptersRange(1,6), L('sec_karma'), L('sec_karma_desc'))}
      ${sectionCard(2, chaptersRange(7,12), L('sec_bhakti'), L('sec_bhakti_desc'))}
      ${sectionCard(3, chaptersRange(13,18), L('sec_jnana'), L('sec_jnana_desc'))}
    </div>
    <div class="sect-all fade-in">
      <a class="browse-all" onclick="showChapters(0)">${esc(L('browse_all'))}</a>
    </div>`;
}
function sectionTabs(){
  const cur = state.section ? state.section : (state.chapter != null ? Math.ceil(DATA[state.chapter].num/6) : 0);
  const act = state.section || cur;
  return '<div class="sec-tabs fade-in">' + [1,2,3].map(k =>
    `<button class="sec-tab${act===k?' on':''}" title="${esc(L('sec_'+['','karma','bhakti','jnana'][k]+'_desc'))}" onclick="showChapters(${k})">${esc(L('tab_'+['','karma','bhakti','jnana'][k]))} <span class="sec-range">(${esc(chaptersRange((k-1)*6+1, k*6))})</span></button>`).join('') + '</div>';
}
function showThemes(ci){
  state.view='themes'; state.chapter=ci; state.theme=null; renderCrumbs();
  const ch = DATA[ci];
  view.innerHTML = `
    ${sectionTabs()}
    <button class="back-top" onclick="showChapters(${state.section||0})">${esc(L('back_chapters'))}</button>
    <div class="view-title fade-in">${esc(L('chapter'))} ${numL(ch.num)} · ${esc(T(ch.names))} — ${L('themes')}</div>
    <button class="read-btn" onclick="showRead(${ci})">${esc(L('read_chapter'))}</button>
    <div class="view-sub fade-in">${ch.deva} · ${esc(T(ch.subs))} — ${L('pick_theme')}</div>
    <div class="grid themes fade-in">
      ${ch.themes.map((t,ti)=>`
        <div class="card" onclick="showVerses(${ci},${ti})">
          <span class="chip">${vCount(t)===1?L('verse'):L('verses')} ${fmtRangeL(t.range)}</span>
          <h3>${esc(T(t.titles))}</h3>
          <p>${esc(T(t.descs))}</p>
          <div class="meta">${numL(t.parts.length)} ${L('part')} · ${numL(vCount(t))} ${vCount(t)===1?L('verse'):L('verses')}</div>
          <div class="go">${L('open_verses')}</div>
        </div>`).join('')}
        </div>` + backFoot(`showChapters(${state.section||0})`, L('back_chapters'));
}

/* ---------- continuous reading ----------
   The chapter -> theme -> part -> verse structure is right for study, but the
   Gita is also something you sit and read straight through. This shows one
   chapter as flowing text: speaker, verse, translation, nothing else. Tapping a
   verse still opens the popup with its quarters and word meanings. */
function showRead(ci, mode){
  rememberOrigin();
  // 'mula' — the root text alone, as a pāṭha is recited; 'full' — each verse
  // followed by its meaning. The reader is doing two different things.
  state.readMode = mode || state.readMode || 'mula';
  state.view='read'; state.chapter=ci; state.theme=null; renderCrumbs();
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
    return `<div class="rd-v" onclick="openModal(${ci},${ti},${idx},'read')">
      <div class="rd-deva">${inner}</div>
      ${state.readMode === 'full' ? `<div class="rd-tr">${esc(T(sv.lits))}</div>` : ''}
    </div>`;
  }).join('');
  view.innerHTML = `
    ${sectionTabs()}
    <button class="back-top" onclick="showThemes(${ci})">${esc(L('back_read'))}</button>
    <div class="view-title fade-in">${esc(L('read_title').replace('{ch}', `${L('chapter')} ${numL(ch.num)} · ${T(ch.names)}`))}</div>
    <div class="view-sub fade-in">${esc(L('read_sub'))}</div>
    <div class="read-tabs fade-in">
      <button class="read-tab${state.readMode==='mula'?' on':''}" onclick="showRead(${ci},'mula')">${esc(L('read_mula'))}</button>
      <button class="read-tab${state.readMode==='full'?' on':''}" onclick="showRead(${ci},'full')">${esc(L('read_full'))}</button>
    </div>
    <div class="reading ${state.readMode} fade-in">${body}</div>` + backFoot(`showThemes(${ci})`, L('back_read'));
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
function padaBlockDeva(s){
  let html = '', li = 0;
  for(const it of (s.lines || [])){
    if(it.k === 's') html += `<span class="spk">${it.d}</span>`;
    else { html += `<div class="gline">${it.d}${li ? '॥' : '।'}</div>`; li++; }
  }
  return html;
}

function showVerses(ci,ti){
  state.view='verses'; state.chapter=ci; state.theme=ti; renderCrumbs();
  const ch = DATA[ci], t = ch.themes[ti];
  const blocks = t.parts.map((p,pi)=>`
    <div class="part fade-in">
      <div class="part-head">
        <span class="pnum">${L('part')} ${numL(pi+1)}</span>
        <span class="ptitle">${esc(T(p.titles))}</span>
        <span class="pdesc">${esc(T(p.descs))} · ${numL(p.sutras.length)} ${p.sutras.length===1?L('verse'):L('verses')} (${fmtRangeL(p.range)})</span>
      </div>
      <div class="grid verses">
        ${p.sutras.map((s,si)=>`
          <div class="mini" onclick="openModal(${ci},${ti},${flatIndex(t,p,si)},'theme')">
            <div class="vnum">${L('verse')} ${fmtNL(s.n)}</div>
            <div class="padas">${padaBlockDeva(s)}</div>
            <div class="vhint">${esc(T(s.paras).slice(0,80))}…</div>
          </div>`).join('')}
      </div>
    </div>`).join('');
  view.innerHTML = `
    ${sectionTabs()}
    <button class="back-top" onclick="showThemes(${ci})">${esc(L('back_themes'))}</button>
    <div class="mini-crumb fade-in">
      <button class="bc-btn" onclick="showThemes(${ci})"><span class="bc-num">${esc(L('chapter'))} ${numL(ch.num)}</span><span class="bc-name">(${esc(T(ch.names))})</span></button>
      <span class="bc-sep">&gt;&gt;</span>
      <div class="bc-cur"><span class="bc-num">${esc(L('theme_sg'))} ${numL(ti+1)}</span><span class="bc-name">(${esc(T(t.titles))})</span></div>
    </div>
    <div class="view-title fade-in">${esc(T(t.titles))}</div>
    <div class="view-sub fade-in">${esc(T(t.descs))}</div>
    <div class="view-sub fade-in">${(t.parts.length===1 ? (vCount(t)===1 ? L('verse_across_part1') : L('verses_across_part1')) : L('verses_across_parts')).replace('{v}',numL(vCount(t))).replace('{p}',numL(t.parts.length))}. ${L('click_hint')}.</div>
    ${blocks}` + backFoot(`showThemes(${ci})`, L('back_themes'));
}

let SRCH_HITS = [], FAV_LIST = [];
function partBounds(t, si){
  let acc = 0;
  for(const p of t.parts){ const len = p.sutras.length;
    if(si >= acc && si < acc + len) return {start:acc, end:acc+len-1};
    acc += len; }
  return {start:0, end:0};
}
function openModal(ci,ti,si, mode, navIdx){
  mode = mode || 'theme';
  state.chapter=ci; state.theme=ti; state.idx=si; state.mode=mode;
  state.gpos = VERSES.findIndex(e => e.ci===ci && e.ti===ti && e.si===si);
  if(state.gpos < 0) state.gpos = 0;
  if(mode === 'theme'){
    const b = partBounds(DATA[ci].themes[ti], si);
    state.pStart = b.start; state.pEnd = b.end;
  } else if(mode === 'search'){ mode = 'book'; }
  else if(mode === 'fav'){ state.navList = FAV_LIST; state.navIdx = navIdx || 0; }
  state.mode = mode;
  fillModal(); $('#modalBg').classList.add('open'); document.body.style.overflow='hidden';
  pushModalHistory();
}
function closeModal(){
  const wasOpen = $('#modalBg').classList.contains('open');
  $('#modalBg').classList.remove('open'); document.body.style.overflow='';
  if(wasOpen) popModalHistory();
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
      <button class="fav-btn${FAV.includes(s.n)?' saved':''}" id="favBtn" onclick="toggleFav('${s.n}')">${FAV.includes(s.n)?L('saved_verse'):L('save_verse')}</button></div>
    ${state.mode==='theme' ? `<div class="m-part">${esc(L('theme_sg'))} ${numL(state.theme+1)} · ${esc(T(t.titles))} » ${esc(L('part'))} ${numL(partIdx+1)} · ${esc(T(part.titles))}</div>` : ''}
    <div class="m-meter">${esc(meterText(s))}</div>
    <div class="m-verse">
      <div class="words-bar">
        <span class="wb-hint">${L('click_hint_pada')} ·</span>
        <button class="wb-btn" onclick="toggleAllMeanings(this)">${L('hide_meanings')}</button>
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
        ? `<button class="m-random" onclick="randomVerse()">${esc(L('next_random'))}</button>`
        : state.mode==='theme'
          ? `<button onclick="navSutra(-1)" ${state.idx>state.pStart?'':'disabled'}>${L('previous')}</button>
             <span class="m-count">${Lof(state.idx-state.pStart+1, state.pEnd-state.pStart+1)}</span>
             ${state.idx===state.pEnd
               ? `<button class="m-back" onclick="backToTheme()">${esc(L('back_to_theme'))}</button>`
               : `<button onclick="navSutra(1)">${L('next')}</button>`}`
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
}
// toggle meaning visibility across all word-splits in the modal
function toggleAllMeanings(btn){
  const hide = btn.dataset.state !== 'hidden';   // meanings start visible → first click hides
  btn.dataset.state = hide ? 'hidden' : 'shown';
  btn.textContent = hide ? L('show_meanings') : L('hide_meanings');
  document.querySelectorAll('#modal .words').forEach(w=>{
    w.classList.toggle('mean-off', hide);
  });
}
function navSutra(d){
  if(state.mode === 'theme'){
    const n = state.idx + d;
    if(n < state.pStart || n > state.pEnd) return;
    state.idx = n;
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
applyStatic();
paintTheme();
showWelcome();
</script>
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
    import base64
    faces = []
    for weight, fname in ((400, "noto-deva-regular.woff2"), (700, "noto-deva-bold.woff2")):
        path = os.path.join(BASE, "fonts", fname)
        if not os.path.exists(path):
            print(f"WARNING: {fname} missing — Devanagari will fall back to a system font")
            continue
        with open(path, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode("ascii")
        faces.append(
            '  @font-face{ font-family:"Noto Serif Devanagari"; font-style:normal;\n'
            f'    font-weight:{weight}; font-display:swap;\n'
            f'    src:url(data:font/woff2;base64,{b64}) format("woff2"); }}')
    return "\n".join(faces)

out = HTML.replace("__FONTS__", _font_face()).replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__UI__", json.dumps(UI, ensure_ascii=False))

# ---- site base URL, used only for the absolute og:image / og:url ----
# Override with:  SITE_BASE=https://user.github.io/repo python3 build_gita.py
SITE_BASE = os.environ.get("SITE_BASE", "https://chapain.github.io/Bhagavad-Gita").rstrip("/")
out = out.replace("__BASE__", SITE_BASE)

path = os.path.join(GITA_DIR, "index.html")
with open(path, "w", encoding="utf-8") as f:
    f.write(out)
print("written:", path, round(len(out)/1024), "KB")

# ---------------- web-app files (published alongside index.html) ----------------
# Only meaningful when the app is hosted; ignored by a standalone file:// copy.
SITE_DIR = GITA_DIR          # in this repo the root *is* the published site
os.makedirs(SITE_DIR, exist_ok=True)

# cache version — bump automatically from the app's content hash so a rebuilt
# app always invalidates the old service-worker cache.
CACHE_VER = hashlib.sha256(out.encode("utf-8")).hexdigest()[:12]

manifest = {
    "name": "Bhagavad Gita — Interactive Study",
    "short_name": "Gita",
    "description": "All 18 chapters, 700 verses in English · नेपाली · हिन्दी, with word-by-word meanings. Works offline.",
    "start_url": "./",
    "scope": "./",
    "display": "standalone",
    "orientation": "any",
    "background_color": "#FFF8EC",
    "theme_color": "#0F4C5C",
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
const ASSETS = ['./', './index.html', './manifest.webmanifest',
                './icon-192.png', './icon-512.png', './icon-maskable-512.png',
                './apple-touch-icon.png', './favicon.ico'];

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
    // network-first for the page itself, so updates land; fall back to cache offline
    e.respondWith(
      fetch(req)
        .then(res => { const copy = res.clone();
                       caches.open(CACHE).then(c => c.put('./index.html', copy));
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
""".replace("%%VER%%", CACHE_VER)
with open(os.path.join(SITE_DIR, "sw.js"), "w", encoding="utf-8") as f:
    f.write(SW)

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
print(f"site/: index.html + manifest + sw.js (cache {CACHE_VER}) + {copied} icons  ->  {SITE_DIR}")
