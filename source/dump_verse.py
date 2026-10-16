#!/usr/bin/env python3
"""dump_verse.py — read-only audit helper for the canonical chapter JSON.

For one or more verses print everything a reviewer needs side by side:

    Sanskrit (Devanagari + IAST, with speaker segments marked)
    EN / NE / HI literal + paraphrase
    word rows (five fields each: deva, iast, en, ne, hi)

Usage:
    python3 source/dump_verse.py 4.1 4.2 5.10-5.12      # verses or ranges
    python3 source/dump_verse.py 4                       # whole chapter

All content comes from the same source/ch<N>.json file used by the build.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))


def load_chapter(ch):
    path = os.path.join(BASE, f"ch{ch}.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def all_verses(chapter):
    return [v for theme in chapter["themes"]
            for part in theme["parts"] for v in part["sutras"]]


def find_verse(ch, vid):
    return next((v for v in all_verses(load_chapter(ch)) if v["n"] == vid), None)


def dump(vid):
    ch = int(vid.split(".")[0])
    verse = find_verse(ch, vid)
    if verse is None:
        print(f"### {vid}: NO SUCH VERSE")
        return
    print(f"\n{'='*78}\n### {vid}\n{'='*78}")
    deva = [s.strip() for s in verse["d"].split("।") if s.strip()]
    iast = [s.strip() for s in verse["t"].split("।") if s.strip()]
    for d, t in zip(deva, iast):
        tag = "SPK" if t.endswith("uvāca") else "   "
        print(f"[SKT {tag}] {d}")
        print(f"[iast   ] {t}")
    for lang in ("en", "ne", "hi"):
        print(f"[{lang.upper()} lit ] {verse['lits'][lang]}")
        print(f"[{lang.upper()} para] {verse['paras'][lang]}")
    pidx = 0
    for item in verse["flow"]:
        if item["k"] == "s":
            label = "speaker"
        else:
            pidx += 1
            label = f"pāda {pidx}"
        print(f"[{label:<8}]")
        for word in item.get("words", []):
            print("    " + " | ".join(word))


def expand(arg):
    """'4' -> whole chapter; '5.10-5.12' -> range; '4.7' -> single."""
    if "." not in arg:
        ch = int(arg)
        if not 1 <= ch <= 18:
            return []
        return [v["n"] for v in all_verses(load_chapter(ch))]
    m = re.match(r"^(\d+)\.(\d+)-(?:\d+\.)?(\d+)$", arg)
    if m:
        ch, start, end = map(int, m.groups())
        return [f"{ch}.{n:02d}" for n in range(start, end + 1)]
    m = re.match(r"^(\d+)\.(\d+)$", arg)
    if not m:
        return []
    ch, verse = map(int, m.groups())
    return [f"{ch}.{verse:02d}"]


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: dump_verse.py <verse|chapter|range> [...]")
    for arg in sys.argv[1:]:
        refs = expand(arg)
        if not refs:
            print(f"### {arg}: INVALID CHAPTER / VERSE / RANGE")
            continue
        for vid in refs:
            dump(vid)


if __name__ == "__main__":
    main()
