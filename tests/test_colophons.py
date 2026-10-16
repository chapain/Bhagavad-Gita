#!/usr/bin/env python3
"""Phase 2.3 — the chapter colophons, locked at the data level.

Every chapter ends with its traditional colophon (*iti … adhyāyaḥ*). It lives in
`source/ch<N>.json`, travels into the built `data/ch<N>.js`, and is printed by
the app's reading view and by the generated `chapter/N/index.html`.

What this test pins, so a later edit cannot quietly break it:

  * all 18 chapters carry a colophon, with Devanagari and IAST;
  * the Devanagari opens with ॐ (U+0950) — never a Latin capital O, which is
    the defect the two pre-existing colophons (ch1, ch2) shipped with;
  * no Latin capital O anywhere in either field (this is what was wrong);
  * the frame is word-for-word identical in all 18 — only the name and the
    ordinal vary — so the text stays one formula, not eighteen improvisations;
  * each colophon names its own chapter: the yoga name matches that chapter's
    Devanagari name in `source/ch<N>.json`, and the ordinal + number match the
    chapter number;
  * the generated chapter page prints that chapter's colophon, once;
  * adding the colophon did not disturb the verses: 700 of them, all with a
    literal and a description in three languages (the Phase 2.2 contract is
    checked in its own test file and is not duplicated here).
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The two characters this test exists for.
OM = "\u0950"          # ॐ DEVANAGARI OM
LATIN_OM = "\u004F"    # O LATIN CAPITAL LETTER O — the defect

FRAME_DEVA_END = "\u0936\u094d\u0930\u0940\u0915\u0943\u0937\u094d\u0923\u093e\u0930\u094d\u091c\u0941\u0928\u0938\u0902\u0935\u093e\u0926\u0947 "  # "…saṃvāde "
FRAME_IAST_END = "saṃvāde "

DEVA_ORDINALS = ["प्रथम", "द्वितीय", "तृतीय", "चतुर्थ", "पञ्चम", "षष्ठ", "सप्तम", "अष्टम",
                 "नवम", "दशम", "एकादश", "द्वादश", "त्रयोदश", "चतुर्दश", "पञ्चदश", "षोडश",
                 "सप्तदश", "अष्टादश"]
DEVA_DIGITS = ["१", "२", "३", "४", "५", "६", "७", "८", "९", "१०", "११", "१२", "१३", "१४",
               "१५", "१६", "१७", "१८"]
IAST_ORDINALS = ["prathama", "dvitīya", "tṛtīya", "caturtha", "pañcama", "ṣaṣṭha", "saptama",
                 "aṣṭama", "navama", "daśama", "ekādaśa", "dvādaśa", "trayodaśa", "caturdaśa",
                 "pañcadaśa", "ṣoḍaśa", "saptadaśa", "aṣṭādaśa"]


def _load(n):
    raw = (ROOT / "data" / f"ch{n}.js").read_text(encoding="utf-8")
    return json.loads(raw[raw.index("=") + 1:].rstrip().rstrip(";"))


def _json(n):
    return json.loads((ROOT / "source" / f"ch{n}.json").read_text(encoding="utf-8"))


class TestColophonData(unittest.TestCase):
    def test_every_chapter_has_a_colophon(self):
        for n in range(1, 19):
            for where, d in (("source", _json(n)), ("built data", _load(n))):
                c = d.get("colophon")
                self.assertIsInstance(c, dict, f"ch{n}: no colophon in {where}")
                self.assertTrue(c["deva"].strip(), f"ch{n}: empty deva in {where}")
                self.assertTrue(c["iast"].strip(), f"ch{n}: empty iast in {where}")

    def test_source_and_built_agree(self):
        for n in range(1, 19):
            self.assertEqual(_json(n)["colophon"], _load(n)["colophon"],
                             f"ch{n}: built colophon differs from source")

    def test_om_is_the_devanagari_letter_not_a_latin_o(self):
        for n in range(1, 19):
            c = _load(n)["colophon"]
            self.assertTrue(c["deva"].startswith(OM), f"ch{n}: deva does not open with ॐ")
            self.assertTrue(c["iast"].startswith("oṃ"), f"ch{n}: iast does not open with oṃ")
            self.assertNotIn(LATIN_OM, c["deva"], f"ch{n}: Latin capital O in the Devanagari")
            self.assertNotIn(LATIN_OM, c["iast"], f"ch{n}: Latin capital O in the IAST")

    def test_one_formula_for_all_eighteen(self):
        devas = [_load(n)["colophon"]["deva"] for n in range(1, 19)]
        iasts = [_load(n)["colophon"]["iast"] for n in range(1, 19)]
        heads = {d.split(FRAME_DEVA_END)[0] for d in devas}
        iheads = {t.split(FRAME_IAST_END)[0] for t in iasts}
        self.assertEqual(len(heads), 1, f"frames differ: {heads}")
        self.assertEqual(len(iheads), 1, f"IAST frames differ: {iheads}")
        for n, (d, t) in enumerate(zip(devas, iasts), 1):
            self.assertIn("नाम", d, f"ch{n}: 'nāma' missing")
            # the name ends in the Devanagari letter O before "nāma" (…योगो नाम…)
            self.assertIn("\u094b नाम ", d, f"ch{n}: the name is not in the -o before nāma")
            self.assertTrue(d.endswith(f"॥ {DEVA_DIGITS[n - 1]} ॥"), f"ch{n}: wrong closing number")
            self.assertIn("o’dhyāyaḥ", t, f"ch{n}: iast tail missing")

    def test_each_colophon_names_its_own_chapter(self):
        for n in range(1, 19):
            chapter = _load(n)
            c = chapter["colophon"]
            deva_name = chapter["deva"]
            # ch6 is listed as "आत्मसंयमयोग / ध्यानयोग"; the colophon uses the
            # first (the standard colophon reading) — that is the point of the check.
            self.assertTrue(deva_name.split(" / ")[0] in c["deva"],
                            f"ch{n}: colophon does not carry the chapter's own name")
            self.assertIn(DEVA_ORDINALS[n - 1], c["deva"], f"ch{n}: wrong ordinal")
            # visarga sandhi: the ordinal's final -a + visarga becomes -o
            # (prathama + o'dhyāyaḥ → prathamo'dhyāyaḥ)
            self.assertIn(IAST_ORDINALS[n - 1][:-1] + "o", c["iast"],
                          f"ch{n}: wrong IAST ordinal")
            self.assertTrue(c["iast"].endswith(f"।। {n}।।"), f"ch{n}: wrong IAST number")

    def test_verses_are_untouched_by_the_colophon(self):
        total, no_lit = 0, []
        for n in range(1, 19):
            d = _load(n)
            self.assertEqual(set(d) - {"colophon"},
                             {"num", "deva", "verses", "themes", "names", "subs"},
                             f"ch{n}: an unexpected top-level key appeared")
            for theme in d["themes"]:
                for part in theme["parts"]:
                    for s in part["sutras"]:
                        total += 1
                        if not (s["lits"]["en"] and s["paras"]["en"] and s["d"]):
                            no_lit.append(s["n"])
                        self.assertNotIn("colophon", s, f"{s['n']}: colophon leaked into a verse")
        self.assertEqual(total, 700, "every verse is still present")
        self.assertEqual(no_lit, [], "no verse lost its text or translations")


class TestColophonOnGeneratedPages(unittest.TestCase):
    def test_each_chapter_page_prints_its_own_colophon_once(self):
        for n in range(1, 19):
            page = (ROOT / "chapter" / str(n) / "index.html").read_text(encoding="utf-8")
            c = _load(n)["colophon"]
            self.assertEqual(page.count('class="colophon"'), 1,
                             f"chapter/{n}: expected exactly one colophon block")
            self.assertIn(c["deva"], page, f"chapter/{n}: colophon Devanagari missing")
            self.assertIn(c["iast"], page, f"chapter/{n}: colophon IAST missing")
            # the colophon must sit after the verses and before the closing call to action
            self.assertGreater(page.index('class="colophon"'), page.index('id="theme-1"'),
                               f"chapter/{n}: colophon printed before the verses")
            self.assertGreater(page.rindex('class="cta"'), page.index('class="colophon"'),
                               f"chapter/{n}: colophon printed after the closing CTA")
            # and no other chapter's colophon may appear on it
            for other in range(1, 19):
                if other != n:
                    self.assertNotIn(_load(other)["colophon"]["deva"], page,
                                     f"chapter/{n}: carries chapter {other}'s colophon")


if __name__ == "__main__":
    unittest.main()
