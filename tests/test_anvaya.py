"""Regression checks for the incrementally reviewed anvaya display."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AnvayaTests(unittest.TestCase):
    def test_reviewed_first_verse_and_unreviewed_verse(self):
        chapter = json.loads((ROOT / 'source/ch1.json').read_text(encoding='utf-8'))
        verses = [v for t in chapter['themes'] for p in t['parts'] for v in p['sutras']]
        self.assertEqual(verses[0]['anvaya'],
                         'सञ्जय! धर्मक्षेत्रे कुरुक्षेत्रे युयुत्सवः समवेताः मामकाः पाण्डवाः च एव किम् अकुर्वत?')
        self.assertNotIn('anvaya', verses[1])

    def test_reader_places_optional_unboxed_sanskrit_before_literal(self):
        reader = (ROOT / 'source/js/50-reader.js').read_text(encoding='utf-8')
        container = reader.index('class="m-verse-box-container"')
        anvaya = reader.index('s.anvaya ?', container)
        literal = reader.index('class="m-line lit"', anvaya)
        self.assertLess(container, anvaya)
        self.assertLess(anvaya, literal)
        self.assertIn('lang="sa"', reader[anvaya:literal])
        self.assertIn('esc(s.anvaya)', reader[anvaya:literal])


if __name__ == '__main__':
    unittest.main()
