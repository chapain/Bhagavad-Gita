# -*- coding: utf-8 -*-
"""retitle.py — rewrite theme TITLES in all three languages, safely.

Why this exists
---------------
The theme titles were written as labels for someone already looking at the
verses. The learning path asks them to do a different job: strung together in
sequence they must tell the chapter's story, unaided, from memory. Chapter 12
read "Question / Unmanifest Path / I Swiftly Deliver Them / If You Cannot /
Dear Devotee / Equal in All" — deliver whom? if I cannot what? Half of the 202
titles lean on a dangling pronoun or are too terse to stand alone.

What it changes
---------------
ONLY the theme title (element 0 of each theme tuple). Descriptions, parts,
verse ranges and every translation are left untouched — this is a naming pass,
not an editorial one.

Guarantees
----------
* the three languages must already agree on theme COUNT, or it refuses to run
* a title is only replaced when the expected old value matches, so a stale
  patch can never silently overwrite the wrong theme
* the caller's build validators still run afterwards; this writes nothing that
  `python3 build.py` cannot check

Usage:  from retitle import apply_titles;  apply_titles(12, ROWS)
        where ROWS = [(idx, en, ne, hi), ...] with idx 0-based.
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MAXLEN = 52          # titles ride in cards and crumbs; past this they wrap badly


def _load():
    import importlib
    import themes_ne, themes_hi
    importlib.reload(themes_ne)
    importlib.reload(themes_hi)
    return themes_ne.THEMES_NE, themes_hi.THEMES_HI


def _mod(ch):
    """Chapter 1's themes live in gita_data.py; 2-18 in gita_data<N>.py."""
    return "gita_data" if ch == 1 else "gita_data%d" % ch


def _en_themes(ch):
    import importlib
    m = importlib.import_module(_mod(ch))
    importlib.reload(m)
    return getattr(m, "CH%d_THEMES" % ch)


def check(ch):
    """Report the three languages agree, and hand back the current titles."""
    ne, hi = _load()
    en = _en_themes(ch)
    assert len(en) == len(ne[ch]) == len(hi[ch]), (
        "theme count differs: en=%d ne=%d hi=%d" % (len(en), len(ne[ch]), len(hi[ch])))
    return [(i, en[i][0], ne[ch][i][0], hi[ch][i][0]) for i in range(len(en))]


def apply_titles(ch, rows, dry=False):
    """rows: [(idx, en, ne, hi)] — 0-based theme index."""
    cur = {i: (e, n, h) for (i, e, n, h) in check(ch)}
    for (i, en, ne, hi) in rows:
        for lang, val in (("en", en), ("ne", ne), ("hi", hi)):
            if len(val) > MAXLEN:
                raise SystemExit("too long (%d>%d) ch%d theme%d %s: %s"
                                 % (len(val), MAXLEN, ch, i + 1, lang, val))
        if i not in cur:
            raise SystemExit("no theme %d in chapter %d" % (i + 1, ch))

    targets = [
        (os.path.join(HERE, _mod(ch) + ".py"), 0),
        (os.path.join(HERE, "themes_ne.py"), 1),
        (os.path.join(HERE, "themes_hi.py"), 2),
    ]
    news = {0: {}, 1: {}, 2: {}}
    for (i, en, ne, hi) in rows:
        news[0][i], news[1][i], news[2][i] = en, ne, hi

    for path, slot in targets:
        with io.open(path, encoding="utf-8") as f:
            src = f.read()
        # The i18n stores hold every chapter in one dict, so a title string can
        # legitimately recur in another chapter ("Arjuna's Question" appears in
        # 2, 3 and 4). Narrow the search to THIS chapter's block before editing.
        if slot == 0:
            lo, hi_ = 0, len(src)
        else:
            m = re.search(r"^ *%d: \[" % ch, src, re.M)
            if not m:
                raise SystemExit("chapter %d block not found in %s" % (ch, path))
            nxt = re.search(r"^ *\d+: \[", src[m.end():], re.M)
            lo = m.start()
            hi_ = m.end() + (nxt.start() if nxt else len(src) - m.end())
        block = src[lo:hi_]
        for (i, _, _, _) in rows:
            old = cur[i][slot]
            new = news[slot][i]
            if old == new:
                continue
            # A theme tuple opens at exactly 4 spaces of indentation; its PART
            # tuples are nested deeper. Several themes share a title with their
            # own first part ("Behold These Kurus", "The Lord's Rebuke"), so
            # matching the bare string is ambiguous — anchor on the indent.
            found = None
            for q in ('"', "'"):
                pat = re.compile(r"^    \(\s*" + q + re.escape(old) + q + r"\s*,", re.M)
                hits = pat.findall(block)
                if len(hits) == 1:
                    found = (pat, q); break
                if len(hits) > 1:
                    raise SystemExit("ch%d theme%d %s: %d theme-level matches for %r"
                                     % (ch, i + 1, ["en","ne","hi"][slot], len(hits), old))
            if not found:
                raise SystemExit("ch%d theme%d %s: no theme-level match for %r"
                                 % (ch, i + 1, ["en","ne","hi"][slot], old))
            pat, q = found
            esc = new.replace("\\", "\\\\").replace(q, "\\" + q)
            block = pat.sub("    (" + q + esc + q + ",", block, count=1)
        src = src[:lo] + block + src[hi_:]
        if not dry:
            with io.open(path, "w", encoding="utf-8") as f:
                f.write(src)
    return len(rows)
