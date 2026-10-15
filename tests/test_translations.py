#!/usr/bin/env python3
"""tests/test_translations.py — locks the translation checker itself.

A checker that cannot fail is decoration. These tests feed it the three faults
that shipped (1.14 जुताइएको, 1.08 सौमदत्तिका छोरा, 1.13 सिंहनादहरू, 1.15's
duplicated word) and prove it catches each one, then run it over the real
corpus and require silence.
"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "source"))

import check_translations as ct  # noqa: E402


def row(text, verse="9.99", lang="ne", kind="lit"):
    return (verse, lang, kind, text)


class RulesCatchRealFaults(unittest.TestCase):
    def test_banned_reading_is_caught(self):
        for bad_text in ("त्यसपछि, सेता घोडाले जुताइएको विशाल रथमा उभिएर।",
                         "र सौमदत्तिका छोरा पनि।",
                         "मृदङ्ग र सिंहनादहरू एकैसाथ बजे।"):
            bad, _ = ct.scan([row(bad_text)])
            self.assertTrue(bad, f"checker missed: {bad_text}")

    def test_repeated_word_is_caught(self):
        bad, _ = ct.scan([row("र महाशङ्ख पौण्ड्र महाशङ्ख पौण्ड्र बजाए।")])
        self.assertTrue(bad)

    def test_latin_inside_devanagari_is_caught(self):
        bad, _ = ct.scan([row("सेता घोडा jute रथमा।")])
        self.assertTrue(bad)

    def test_truncated_string_is_caught(self):
        bad, _ = ct.scan([row("महाशङ्ख पौण्ड्र बजाया")])
        self.assertTrue(bad)

    def test_legitimate_nepali_passes(self):
        for good in ("महाभारत जे-जे गर्छौ, जे-जे खान्छौ।",       # hyphen reduplication
                     "काम गर्न लगाउने तीन: थाहा, थाहा पाइने कुरा।",  # listing
                     "जसरी पिता छोरालाई, मित्रले मित्रलाई क्षमा गर्छ।",
                     "र अरू धेरै वीरहरू, मेरा निम्ति जीवन दिन तयार।",
                     "So I deem."):                                # English terminal
            bad, _ = ct.scan([row(good, lang="ne" if not good[0].isascii() else "en")])
            self.assertEqual(bad, [], f"false positive on: {good}")


class ShippedCorpusIsGreen(unittest.TestCase):
    def test_full_corpus_has_no_failures(self):
        rows = list(ct.pairs(ct.load_pages()))
        self.assertGreater(len(rows), 2000)
        bad, _ = ct.scan(rows)
        self.assertEqual(bad, [], "\n".join(bad))


if __name__ == "__main__":
    unittest.main()
