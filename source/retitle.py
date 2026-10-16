# -*- coding: utf-8 -*-
"""retitle.py — safely update a chapter's theme titles in all three languages.

Theme titles are stored together in source/ch<N>.json under `titles.en/ne/hi`.
This helper changes only those fields; descriptions, parts, ranges and verse
content remain untouched.

Guarantees
----------
* a chapter must already contain all three title languages;
* every requested theme index must exist and may be changed only once per call;
* each title is capped at 52 characters, matching the card-width review rule;
* dry=True validates the requested update without writing the file.

Usage: from retitle import apply_titles; apply_titles(12, [(idx, en, ne, hi), ...])
       where idx is zero-based.
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


def check(ch):
    """Return [(idx, en, ne, hi)] and verify every theme has three titles."""
    chapter = _load(ch)
    out = []
    for idx, theme in enumerate(chapter["themes"]):
        titles = theme.get("titles", {})
        if set(titles) != set(LANGS):
            raise ValueError(f"chapter {ch} theme {idx + 1}: titles must contain en/ne/hi")
        out.append((idx, titles["en"], titles["ne"], titles["hi"]))
    return out


def apply_titles(ch, rows, dry=False):
    """rows: [(idx, en, ne, hi)] — zero-based theme indexes."""
    rows = list(rows)
    chapter = _load(ch)
    themes = chapter["themes"]
    seen = set()
    for row in rows:
        if len(row) != 4:
            raise ValueError("each row must be (idx, en, ne, hi)")
        idx, *values = row
        if not isinstance(idx, int) or not 0 <= idx < len(themes):
            raise SystemExit(f"no theme {idx!r} in chapter {ch}")
        if idx in seen:
            raise SystemExit(f"theme {idx + 1} appears more than once in this update")
        seen.add(idx)
        for lang, value in zip(LANGS, values):
            if not isinstance(value, str) or len(value) > MAXLEN:
                length = len(value) if isinstance(value, str) else "non-string"
                raise SystemExit(f"invalid/too long ({length}>{MAXLEN}) ch{ch} theme{idx + 1} {lang}: {value}")
        if set(themes[idx].get("titles", {})) != set(LANGS):
            raise SystemExit(f"chapter {ch} theme {idx + 1}: titles must contain en/ne/hi")

    for idx, en, ne, hi in rows:
        themes[idx]["titles"].update({"en": en, "ne": ne, "hi": hi})
    if rows and not dry:
        _write(ch, chapter)
    return len(rows)
