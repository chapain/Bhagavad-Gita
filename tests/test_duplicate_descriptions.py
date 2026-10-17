#!/usr/bin/env python3
"""Phase 2.2 — duplicate verse descriptions, locked at the data level.

A verse's part description that is word-for-word the verse's own literal,
in the same language, is a copy. The renderers must show nothing for it
(the build-time .vd rule on the generated
chapter pages) — the source text and the built data keep every description
regardless, and check_study_structure.py still requires all of them.

So this test locks the DATA-level contract, not the rendering:

  * every verse now carries its own summary description (rewritten
    2026-10-14 for all 18 chapters), so the baseline is ZERO copies in
    every language — any new copy is a regression of the summary design;
  * no two verses may share one summary within a language;
  * duplication is judged per language — a verse may be a copy in one
    language and distinct in another (checked on synthetic data, since the
    real corpus no longer has any copy to point at);
  * no description or literal may be emptied to manufacture "distinctness"
    (suppression is a display decision, never a content deletion).
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(n):
    raw = (ROOT / "data" / f"ch{n}.js").read_text(encoding="utf-8")
    return json.loads(raw[raw.index("=") + 1:].rstrip().rstrip(";"))


def _parts():
    out = []
    for n in range(1, 19):
        for theme in _load(n)["themes"]:
            for part in theme["parts"]:
                out.append((part["sutras"][0], part))
    return out


def _is_copy(desc, lit):
    """The exact-copy rule partDesc() applies, per language."""
    return desc.strip() == lit.strip()


def _dup_ids(lang):
    return {v["n"] for v, p in _parts()
            if _is_copy(p["descs"][lang], v["lits"][lang])}


class TestDuplicateDescriptions(unittest.TestCase):
    def test_baseline_counts_2026_10_14(self):
        self.assertEqual(len(_parts()), 700, "every part holds exactly one verse")
        for lang in ("en", "ne", "hi"):
            self.assertEqual(sorted(_dup_ids(lang)), [],
                             f"{lang}: descriptions that merely repeat the translation")

    def test_no_summary_is_shared_between_verses(self):
        for lang in ("en", "ne", "hi"):
            seen = {}
            for v, p in _parts():
                d = p["descs"][lang].strip()
                if d in seen:
                    self.fail(f"{lang}: {v['n']} repeats the summary of {seen[d]}")
                seen[d] = v["n"]

    def test_data_keeps_every_description_and_literal(self):
        for v, p in _parts():
            for lang in ("en", "ne", "hi"):
                self.assertTrue(p["descs"][lang].strip(),
                                f"{v['n']} {lang} description emptied in data")
                self.assertTrue(v["lits"][lang].strip(),
                                f"{v['n']} {lang} literal emptied in data")

    def test_duplication_is_judged_per_language(self):
        lit = {"en": "Arjuna sat down.", "ne": "अर्जुन बसे।", "hi": "अर्जुन बैठ गए।"}
        # identical text (ignoring edge whitespace) is a copy…
        for lang, text in lit.items():
            self.assertTrue(_is_copy(text, text))
            self.assertTrue(_is_copy("  " + text + "\n", text))
        # …a summary is not…
        self.assertFalse(_is_copy("He sinks down, the bow slipping from his hand.", lit["en"]))
        # …and the comparison never crosses languages.
        self.assertFalse(_is_copy(lit["en"], lit["ne"]))
        self.assertFalse(_is_copy(lit["ne"], lit["hi"]))


if __name__ == "__main__":
    unittest.main()
