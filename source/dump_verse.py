#!/usr/bin/env python3
"""dump_verse.py — audit helper. For one or more verses print everything a
reviewer needs side by side:

    Sanskrit (deva + iast, with speaker segment clearly marked)
    EN / NE / HI literal + paraphrase
    word rows (five fields each: deva, iast, en, ne, hi) incl. speaker rows

Usage:
    python3 source/dump_verse.py 4.1 4.2 5.10-5.12      # verses or ranges
    python3 source/dump_verse.py 4                       # whole chapter

Read-only; works straight off the source files, not the built data.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from translations_ne import TRANS_NE
from translations_hi import TRANS_HI
from gloss_ne import GLOSS_NE
from gloss_hi import GLOSS_HI
import importlib

NE_SPEAKER = {
    "धृतराष्ट्र": "धृतराष्ट्रले",
    "सञ्जय": "सञ्जयले",
    "सञ्जयः": "सञ्जयले",
    "अर्जुन": "अर्जुनले",
    "अर्जुनः": "अर्जुनले",
    "श्रीभगवान्": "श्रीभगवान्ले",
}
HI_SPEAKER_FALLBACK = {  # same mapping build step will carry
    "धृतराष्ट्र": "धृतराष्ट्र",
    "सञ्जय": "संजय",
    "सञ्जयः": "संजय",
    "अर्जुन": "अर्जुन",
    "अर्जुनः": "अर्जुन",
    "श्रीभगवान्": "श्रीभगवान्",
}

_en_cache, _word_cache = {}, {}


def en_trans(ch):
    if ch not in _en_cache:
        mod = importlib.import_module("gita_data" if ch == 1 else f"gita_data{ch}")
        _en_cache[ch] = getattr(mod, f"CH{ch}_TRANSLATIONS")
    return _en_cache[ch]


def words(ch):
    if ch not in _word_cache:
        mod = importlib.import_module(f"padachheda_ch{ch}")
        _word_cache[ch] = getattr(mod, f"GITA_CH{ch}_WORDS")
    return _word_cache[ch]


def i18n_word(w, speaker_line=False):
    """Reproduce build_gita.i18n_word / i18n_speaker_words behaviour."""
    d, i, en = w[0], w[1], w[2]
    if speaker_line:
        honorific = d == "श्रीभगवान्"
        ne = NE_SPEAKER.get(d, w[3] if len(w) >= 5 else GLOSS_NE.get(i, en))
        hi = w[4] if len(w) >= 5 else GLOSS_HI.get(i, en)
        return d, i, en, ne, hi, honorific
    ne = w[3] if len(w) >= 5 else GLOSS_NE.get(i, en)
    hi = w[4] if len(w) >= 5 else GLOSS_HI.get(i, en)
    return d, i, en, ne, hi, False


def dump(vid):
    ch_s, v_s = vid.split(".")
    ch, v = int(ch_s), int(v_s)
    js = json.load(open(os.path.join(BASE, f"ch{ch}.json"), encoding="utf-8"))
    verse = js["verses"].get(v_s) or js["verses"].get(str(int(v_s)))
    if verse is None:
        print(f"### {vid}: NO SUCH VERSE")
        return
    print(f"\n{'='*78}\n### {vid}\n{'='*78}")
    segs = [s.strip() for s in verse["deva"].split("।") if s.strip()]
    isegs = [s.strip() for s in verse["iast"].split("।") if s.strip()]
    for d, t in zip(segs, isegs):
        tag = "SPK" if t.endswith("uvāca") else "   "
        print(f"[SKT {tag}] {d}")
        print(f"[iast   ] {t}")
    ten = en_trans(ch).get(v, ("<missing>", "<missing>"))
    tne = TRANS_NE.get(vid, ("<missing>", "<missing>"))
    thi = TRANS_HI.get(vid, ("<missing>", "<missing>"))
    for lang, pair in (("EN", ten), ("NE", tne), ("HI", thi)):
        print(f"[{lang} lit ] {pair[0]}")
        print(f"[{lang} para] {pair[1]}")
    vw = words(ch).get(v)
    if not vw:
        print("[words  ] <no word rows>")
        return
    spk = vw.get("s", [])
    honorific_any = any(w[0] == "श्रीभगवान्" for w in spk)
    if spk:
        print("[speaker ]")
        for w in spk:
            d, i, en, ne, hi, hon = i18n_word(w, speaker_line=True)
            if honorific_any and d == "उवाच":
                ne = "भन्नुभयो"
            print(f"    {d} | {i} | {en} | {ne} | {hi}")
    for pada in sorted(k for k in vw if k != "s"):
        print(f"[pāda {pada}  ]")
        for w in vw[pada]:
            d, i, en, ne, hi, _ = i18n_word(w)
            print(f"    {d} | {i} | {en} | {ne} | {hi}")


def expand(arg):
    """'4' -> whole chapter; '5.10-5.12' -> range; '4.7' -> single."""
    if "." not in arg:
        js = json.load(open(os.path.join(BASE, f"ch{arg}.json"), encoding="utf-8"))
        return [f"{arg}.{k}" for k in sorted(js["verses"], key=int)]
    m = re.match(r"^(\d+)\.(\d+)-(?:\d+\.)?(\d+)$", arg)
    if m:
        c, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return [f"{c}.{n}" for n in range(a, b + 1)]
    return [arg]


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: dump_verse.py <verse|chapter|range> [...]")
    for arg in sys.argv[1:]:
        for vid in expand(arg):
            dump(vid)


if __name__ == "__main__":
    main()
