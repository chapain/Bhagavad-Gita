# -*- coding: utf-8 -*-
"""verify.py — two small helpers the build uses to CHECK your data.

Nothing here generates anything the app displays. These functions exist only so
the build can tell you when a data file contradicts itself:

  norm1()      flattens IAST accents, so the pādas in padas_ch*.py can be
               compared against the verse in ch*.json
  syll_iast()  counts syllables, so the number you wrote next to a pāda can be
               checked against the pāda's actual text

If a check fails, the build stops and names the file and the verse. It never
rewrites your data.
"""

IAST_VOW = set("aāiīuūṛṝḷḹeoAĀIĪUŪṚṜḶḸEO")


def norm1(s):
    """Flatten IAST diacritics to bare ASCII, for tolerant comparison."""
    return (s.replace("ā", "a").replace("ī", "i").replace("ū", "u")
             .replace("ṛ", "r").replace("ṝ", "r").replace("ḷ", "l").replace("ḹ", "l")
             .replace("ṅ", "n").replace("ñ", "n").replace("ṭ", "t").replace("ḍ", "d")
             .replace("ṇ", "n").replace("ś", "s").replace("ṣ", "s").replace("ṃ", "m")
             .replace("ṁ", "m").replace("ḥ", "h").replace("’", "'")
             .replace("kṣ", "x").lower())


def syll_iast(t):
    """Count syllables in an IAST string.

    Every vowel letter is one syllable; the digraphs ai and au are single
    (diphthong) syllables.
    """
    n = 0
    i = 0
    L = len(t)
    while i < L:
        c = t[i]
        if c in IAST_VOW:
            n += 1
            if c == 'a' and i + 1 < L and t[i + 1] in ('i', 'u'):
                i += 1  # ai / au is one syllable
        i += 1
    return n
