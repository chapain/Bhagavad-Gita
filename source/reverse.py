# -*- coding: utf-8 -*-
"""reverse.py — rewrite VERSE titles (part titles) in all three languages.

Sibling of retitle.py, which does theme titles. Same guarantees, different
target: element 0 of each PART tuple rather than each THEME tuple.

Why this exists
---------------
Verse titles are what a reader sees in the verse sheet, in the Study-guide
cards, and as the 3-9 titles inside a theme. 86 of the 700 lean on a dangling
pronoun ("That I May See Them", "Weapons Do Not Cut It") or are too terse to
mean anything alone ("Unbreakable, Unburnable"), and 7 are exact duplicates of
another verse's title — which is a real defect, since two drill options can
then render identically.

Guarantees
----------
* the three languages must already agree on part COUNT, or it refuses to run
* a title is replaced only where the expected old value matches EXACTLY ONCE
  inside that chapter's block, so a stale patch cannot overwrite the wrong verse
* PART tuples are matched by their verse ref, not by position, so a theme split
  cannot silently shift the target
* titles only; descriptions, ranges, verse text and translations are untouched

Usage:  from reverse import check, apply_verse_titles
        apply_verse_titles(2, [("2.23", en, ne, hi), ...])
"""
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MAXLEN = 52          # same cap as theme titles: fits a card, stays memorable


def _mod(ch):
    """Chapter 1's data lives in gita_data.py; 2-18 in gita_data<N>.py."""
    return "gita_data" if ch == 1 else "gita_data%d" % ch


def _en_themes(ch):
    import importlib
    m = importlib.import_module(_mod(ch))
    importlib.reload(m)
    return getattr(m, "CH%d_THEMES" % ch)


def _load_i18n():
    import importlib
    import themes_ne, themes_hi
    importlib.reload(themes_ne)
    importlib.reload(themes_hi)
    return themes_ne.THEMES_NE, themes_hi.THEMES_HI


def check(ch):
    """Return [(ref, en, ne, hi)] for every verse of the chapter, after
    proving the three languages describe the same parts in the same order."""
    ne, hi = _load_i18n()
    en = _en_themes(ch)
    assert len(en) == len(ne[ch]) == len(hi[ch]), (
        "theme count differs: en=%d ne=%d hi=%d" % (len(en), len(ne[ch]), len(hi[ch])))
    out = []
    for ti in range(len(en)):
        pe, pn, ph = en[ti][2], ne[ch][ti][2], hi[ch][ti][2]
        assert len(pe) == len(pn) == len(ph), (
            "ch%d theme%d part count differs: en=%d ne=%d hi=%d"
            % (ch, ti + 1, len(pe), len(pn), len(ph)))
        for pi in range(len(pe)):
            ref = pe[pi][2]
            assert pn[pi][2] == ref and ph[pi][2] == ref, (
                "ch%d theme%d part%d ref mismatch: en=%s ne=%s hi=%s"
                % (ch, ti + 1, pi + 1, ref, pn[pi][2], ph[pi][2]))
            out.append((ref, pe[pi][0], pn[pi][0], ph[pi][0]))
    return out


def apply_verse_titles(ch, rows, dry=False):
    """rows: [(verse_ref, en, ne, hi)] — e.g. ("2.23", "...", "...", "...")."""
    cur = {ref: (e, n, h) for (ref, e, n, h) in check(ch)}
    for (ref, en, ne, hi) in rows:
        if ref not in cur:
            raise SystemExit("ch%d has no verse %s" % (ch, ref))
        for lang, val in (("en", en), ("ne", ne), ("hi", hi)):
            if len(val) > MAXLEN:
                raise SystemExit("too long (%d>%d) %s %s: %s"
                                 % (len(val), MAXLEN, ref, lang, val))

    targets = [(os.path.join(HERE, _mod(ch) + ".py"), 0),
               (os.path.join(HERE, "themes_ne.py"), 1),
               (os.path.join(HERE, "themes_hi.py"), 2)]
    news = {0: {}, 1: {}, 2: {}}
    for (ref, en, ne, hi) in rows:
        news[0][ref], news[1][ref], news[2][ref] = en, ne, hi

    for path, slot in targets:
        src = io.open(path, encoding="utf-8").read()
        # The i18n stores hold every chapter in one dict, so narrow to this
        # chapter's block before touching anything.
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

        for (ref, _, _, _) in rows:
            old = cur[ref][slot]
            new = news[slot][ref]
            if old == new:
                continue
            # Anchor on the PART tuple: ("Title", "desc", "<ref>", "<ref>").
            # Matching the ref as well as the title makes it impossible to hit
            # a same-named title belonging to another verse.
            found = None
            for q in ('"', "'"):
                # The description may itself contain an apostrophe
                # ("The grandsire's lion-roar"), so match it by its own
                # delimiter rather than a shared quote class.
                dq = r"(?:\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')"
                pat = re.compile(
                    r"\(\s*" + q + re.escape(old) + q +
                    r"\s*,\s*" + dq + r"\s*,\s*"
                    r"(?:'|\")" + re.escape(ref) + r"(?:'|\")\s*,\s*"
                    r"(?:'|\")" + re.escape(ref) + r"(?:'|\")\s*\)", re.S)
                hits = pat.findall(block)
                if len(hits) == 1:
                    found = (pat, q)
                    break
                if len(hits) > 1:
                    raise SystemExit("%s %s: %d matches for %r — ambiguous"
                                     % (ref, ["en", "ne", "hi"][slot], len(hits), old))
            if not found:
                raise SystemExit("%s %s: no match for %r"
                                 % (ref, ["en", "ne", "hi"][slot], old))
            pat, q = found
            esc = new.replace("\\", "\\\\").replace(q, "\\" + q)

            def _sub(m, _q=q, _e=esc):
                whole = m.group(0)
                # replace only the FIRST quoted field of the tuple
                return re.sub(r"\(\s*" + _q + r"(?:[^" + _q + r"]|\\.)*?" + _q,
                              "(" + _q + _e + _q, whole, count=1)

            block = pat.sub(_sub, block, count=1)

        src = src[:lo] + block + src[hi_:]
        if not dry:
            io.open(path, "w", encoding="utf-8").write(src)
    return len(rows)
