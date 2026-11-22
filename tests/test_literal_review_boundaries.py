"""Regression checks for the 2026-11-22 deferred literal review."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verses():
    result = {}
    for chapter in range(1, 19):
        data = json.loads((ROOT / 'source' / f'ch{chapter}.json').read_text())
        for theme in data['themes']:
            for part in theme['parts']:
                for verse in part['sutras']:
                    result[verse['n']] = verse
    return result


class LiteralReviewBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verses = verses()

    def test_sorrow_union_and_knowing_belong_to_6_23(self):
        for lang, know, disconnection in (
            ('en', 'Know', 'disconnection'),
            ('ne', 'जान्नुपर्छ', 'विच्छेद'),
            ('hi', 'जानना चाहिए', 'विच्छेद'),
        ):
            with self.subTest(lang=lang):
                self.assertNotIn(disconnection, self.verses['6.22']['lits'][lang])
                self.assertIn(disconnection, self.verses['6.23']['lits'][lang])
                self.assertIn(know, self.verses['6.23']['lits'][lang])

    def test_entry_into_mouths_belongs_to_11_27(self):
        # प्रमुख contains मुख as a substring, but is not the word for mouths.
        for lang, mouth in (('en', 'mouth'), ('ne', 'मुखहरूमा'), ('hi', 'मुखों में')):
            with self.subTest(lang=lang):
                self.assertNotIn(mouth, self.verses['11.26']['lits'][lang])
                self.assertIn(mouth, self.verses['11.27']['lits'][lang])

    def test_knowledge_pointer_in_4_34(self):
        self.assertIn('त्यो तत्त्वज्ञानलाई', self.verses['4.34']['lits']['ne'])
        self.assertIn('उस तत्त्व-ज्ञान को', self.verses['4.34']['lits']['hi'])

    def test_only_pronoun_referent_parentheticals_remain(self):
        found = [(v['n'], lang) for v in self.verses.values()
                 for lang, text in v['lits'].items() if '(' in text or ')' in text]
        self.assertEqual(found, [('3.42', 'en'), ('3.42', 'ne'), ('3.42', 'hi')])
        for lang, marker in (('en', '(the Self)'), ('ne', '(आत्मा)'), ('hi', '(आत्मा)')):
            self.assertIn(marker, self.verses['3.42']['lits'][lang])
        self.assertIn('साङ्ख्य', self.verses['18.13']['lits']['ne'])
        self.assertIn('सांख्य', self.verses['18.13']['lits']['hi'])

    def test_both_3_02_iva_rows_are_comparisons(self):
        rows = [r for f in self.verses['3.02']['flow'] for r in f['words'] if r[0] == 'इव']
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][2:], ['as if', 'झैँ', 'के समान'])
        self.assertEqual(rows[0][3:], ['झैँ', 'के समान'])


if __name__ == '__main__':
    unittest.main()
