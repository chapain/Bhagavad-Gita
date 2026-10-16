# -*- coding: utf-8 -*-
"""reverse.py — safely update one-verse part titles in all three languages.

Sibling of retitle.py, which updates theme titles. Part titles are keyed by the
verse ID in source/ch<N>.json, so edits cannot drift when a theme is regrouped.
Only `titles.en/ne/hi` changes; descriptions, ranges, verse text and translations
are left untouched.

Usage: from reverse import check, apply_verse_titles
        apply_verse_titles(2, [("2.23", en, ne, hi), ...])
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAXLEN = 52
LANGS = ("en", "ne", "hi")


def _path(ch):
    if not isinstance(ch, int) or not 1 <= ch <= 18:
        raise ValueError(f"chapter must be 1–18, got {ch!r}")
    return HERE / f"ch{ch}.json"


def _load(ch):
    return json.loads(_path(ch).read_text(encoding="utf-8"))


def _write(ch, chapter):
    _path(ch).write_text(json.dumps(chapter, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")


def _parts(chapter):
    out = []
    for theme in chapter["themes"]:
        for part in theme["parts"]:
            if len(part["sutras"]) != 1:
                raise ValueError("each part must contain exactly one verse")
            out.append((part["sutras"][0]["n"], part))
    return out


def check(ch):
    """Return [(ref, en, ne, hi)] and verify the part-title maps are complete."""
    chapter = _load(ch)
    out = []
    for ref, part in _parts(chapter):
        titles = part.get("titles", {})
        if set(titles) != set(LANGS):
            raise ValueError(f"{ref}: titles must contain en/ne/hi")
        out.append((ref, titles["en"], titles["ne"], titles["hi"]))
    return out


def apply_verse_titles(ch, rows, dry=False):
    """rows: [(verse_ref, en, ne, hi)] — e.g. ("2.23", "...", "...", "...")."""
    rows = list(rows)
    chapter = _load(ch)
    by_ref = {ref: part for ref, part in _parts(chapter)}
    seen = set()
    for row in rows:
        if len(row) != 4:
            raise ValueError("each row must be (verse_ref, en, ne, hi)")
        ref, *values = row
        if ref not in by_ref:
            raise SystemExit(f"chapter {ch} has no verse {ref}")
        if ref in seen:
            raise SystemExit(f"verse {ref} appears more than once in this update")
        seen.add(ref)
        for lang, value in zip(LANGS, values):
            if not isinstance(value, str) or len(value) > MAXLEN:
                length = len(value) if isinstance(value, str) else "non-string"
                raise SystemExit(f"invalid/too long ({length}>{MAXLEN}) {ref} {lang}: {value}")
        if set(by_ref[ref].get("titles", {})) != set(LANGS):
            raise SystemExit(f"{ref}: titles must contain en/ne/hi")

    for ref, en, ne, hi in rows:
        by_ref[ref]["titles"].update({"en": en, "ne": ne, "hi": hi})
    if rows and not dry:
        _write(ch, chapter)
    return len(rows)
