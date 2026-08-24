#!/usr/bin/env python3
"""check_paraphrase.py — every flowing paraphrase must earn its place.

Each verse carries two prose renderings per language: a close literal and a
flowing paraphrase. If the paraphrase merely swaps a word or two, the second
column is dead weight on the page. This check measures character-level overlap
between the two strings and fails when any pair is too similar.

    python3 check_paraphrase.py

Threshold: 80%. Typical healthy medians are ~59% (en) and ~63% (ne/hi).
Reads the built data/ch*.js files, so run it after build_gita.py.
"""
import difflib
import json
import os
import re
import statistics
import sys

LIMIT = 0.80
LANGS = ("en", "ne", "hi")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")


def norm(s):
    """Strip wrapping quotes and collapse whitespace, so only wording counts."""
    return re.sub(r"\s+", " ", s.strip().strip('\u201c\u201d"\''))


def load_data():
    """Assemble the chapter list from the published data/ch<N>.js files."""
    data = []
    for n in range(1, 19):
        p = os.path.join(DATA_DIR, f"ch{n}.js")
        if not os.path.exists(p):
            sys.exit(f"data/ch{n}.js not found — run build_gita.py first")
        src = open(p, encoding="utf-8").read()
        m = re.match(r"^GITA_CH\[(\d+)\] = (\{.*\});\n$", src, re.S)
        if not m or int(m.group(1)) != n:
            sys.exit(f"data/ch{n}.js is malformed")
        data.append(json.loads(m.group(2)))
    return data


def main():
    data = load_data()
    verses = [v for c in data for t in c["themes"]
              for p in t["parts"] for v in p["sutras"]]

    bad = []
    for lang in LANGS:
        ratios = []
        for v in verses:
            r = difflib.SequenceMatcher(
                None, norm(v["lits"][lang]), norm(v["paras"][lang])).ratio()
            ratios.append(r)
            if r >= LIMIT:
                bad.append((lang, v["n"], r))
        print(f"  {lang}: {len(verses)} verses, median overlap "
              f"{statistics.median(ratios):.1%}, max {max(ratios):.1%}")

    if bad:
        print(f"\nFAIL: {len(bad)} paraphrase(s) at or above {LIMIT:.0%} "
              f"overlap with their literal:")
        for lang, n, r in sorted(bad, key=lambda x: -x[2]):
            print(f"  [{lang}] {n}  {r:.0%}")
        sys.exit(1)

    print(f"OK: all {len(verses) * len(LANGS)} paraphrase pairs below "
          f"{LIMIT:.0%} overlap")


if __name__ == "__main__":
    main()
