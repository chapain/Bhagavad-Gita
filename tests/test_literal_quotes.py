#!/usr/bin/env python3
"""Curly quotation marks in every canonical literal and paraphrase."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def balanced_quotes(text):
    """Permit no quotes or paired quoted spans, but not nesting or doubled marks."""
    if "““" in text or "””" in text:
        return False
    open_quote = False
    for char in text:
        if char == "“":
            if open_quote:
                return False
            open_quote = True
        elif char == "”":
            if not open_quote:
                return False
            open_quote = False
    return not open_quote


class LiteralQuoteTests(unittest.TestCase):
    def test_quote_rule_rejects_bad_wrapping(self):
        for text in ('“word', 'word”', '”word“', '““word”',
                     '“word””', '“outer “inner” outer”'):
            with self.subTest(text=text):
                self.assertFalse(balanced_quotes(text))
        for text in ('plain', '“whole”', 'said: “words”', '“one” and “two”'):
            with self.subTest(text=text):
                self.assertTrue(balanced_quotes(text))

    def test_all_literal_and_paraphrase_strings(self):
        verse_count = string_count = 0
        for chapter in range(1, 19):
            data = json.loads((ROOT / 'source' / f'ch{chapter}.json').read_text())
            for theme in data['themes']:
                for part in theme['parts']:
                    for verse in part['sutras']:
                        verse_count += 1
                        for field in ('lits', 'paras'):
                            for lang in ('en', 'ne', 'hi'):
                                string_count += 1
                                text = verse[field][lang]
                                with self.subTest(verse=verse['n'], field=field, lang=lang):
                                    self.assertTrue(balanced_quotes(text), repr(text))
        self.assertEqual(verse_count, 700)
        self.assertEqual(string_count, 4200)
