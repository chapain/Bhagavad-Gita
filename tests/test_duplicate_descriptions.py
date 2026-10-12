#!/usr/bin/env python3
"""Phase 2.2 — duplicate verse descriptions, locked at the data level.

A verse's part description that is word-for-word the verse's own literal,
in the same language, is a copy. The renderers must show nothing for it
(partDesc() in source/build_gita.py and the .vd rule on the generated
chapter pages) — the source text and the built data keep every description
regardless, and check_study_structure.py still requires all of them.

So this test locks the DATA-level contract, not the rendering:

  * the baseline count of duplicates per language (content state as of
    2026-10-12); if a description is later rewritten, these numbers are
    updated deliberately, like the other corpus counts;
  * duplication is judged per language — a verse may be a copy in one
    language and distinct in another;
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


def _dup_ids(lang):
    return {v["n"] for v, p in _parts()
            if p["descs"][lang].strip() == v["lits"][lang].strip()}


class TestDuplicateDescriptions(unittest.TestCase):
    def test_baseline_counts_2026_10_12(self):
        self.assertEqual(len(_parts()), 700, "every part holds exactly one verse")
        self.assertEqual(len(_dup_ids("en")), 593)
        self.assertEqual(len(_dup_ids("ne")), 566)
        self.assertEqual(len(_dup_ids("hi")), 592)

    def test_data_keeps_every_description_and_literal(self):
        for v, p in _parts():
            for lang in ("en", "ne", "hi"):
                self.assertTrue(p["descs"][lang].strip(),
                                f"{v['n']} {lang} description emptied in data")
                self.assertTrue(v["lits"][lang].strip(),
                                f"{v['n']} {lang} literal emptied in data")

    def test_duplication_is_judged_per_language(self):
        en, ne, hi = _dup_ids("en"), _dup_ids("ne"), _dup_ids("hi")
        # a copy in all three languages
        for v in ("2.03", "2.05"):
            self.assertIn(v, en & ne & hi)
        # distinct in all three languages
        self.assertNotIn("2.01", en | ne | hi)
        # a copy in English + Nepali, distinct in Hindi
        self.assertIn("2.30", en & ne)
        self.assertNotIn("2.30", hi)
        # a copy in Hindi only
        for v in ("2.02", "4.01"):
            self.assertIn(v, hi - en - ne)
        # a copy in English + Hindi, distinct in Nepali
        self.assertIn("1.13", en & hi)
        self.assertNotIn("1.13", ne)
        # a copy in Nepali + Hindi, distinct in English
        self.assertIn("18.78", ne & hi)
        self.assertNotIn("18.78", en)


if __name__ == "__main__":
    unittest.main()
