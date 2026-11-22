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
                         'धृतराष्ट्र उवाच — सञ्जय! धर्मक्षेत्रे कुरुक्षेत्रे युयुत्सवः समवेताः मामकाः पाण्डवाः च एव किम् अकुर्वत?')
        self.assertEqual(verses[0]['anvaya_iast'],
                         'dhṛtarāṣṭra uvāca — sañjaya! dharmakṣetre kurukṣetre yuyutsavaḥ samavetāḥ māmakāḥ pāṇḍavāḥ ca eva kim akurvata?')
        self.assertEqual(verses[1]['anvaya'],
                         'सञ्जय उवाच — तदा राजा दुर्योधनः तु व्यूढं पाण्डवानीकं दृष्ट्वा आचार्यम् उपसङ्गम्य वचनम् अब्रवीत्।')
        self.assertEqual(len([v for v in verses if 'anvaya' in v]), 47)
        self.assertLess(verses[20]['anvaya'].index('आह'), verses[20]['anvaya'].index('अर्जुन उवाच'))
        self.assertLess(verses[27]['anvaya'].index('अब्रवीत्'), verses[27]['anvaya'].index('अर्जुन उवाच'))
        self.assertIn('महत्पापं', verses[44]['anvaya'])
        self.assertIn('सङ्ख्ये', verses[46]['anvaya'])

    def test_chapter_two_keeps_each_verse_and_its_own_words(self):
        chapter = json.loads((ROOT / 'source/ch2.json').read_text(encoding='utf-8'))
        verses = [v for t in chapter['themes'] for p in t['parts'] for v in p['sutras']]
        self.assertEqual(len([v for v in verses if 'anvaya' in v]), 72)
        self.assertNotIn('कामात्मानः', verses[41]['anvaya'])
        self.assertIn('कामात्मानः', verses[42]['anvaya'])
        self.assertNotIn('प्रवदन्ति', verses[42]['anvaya'])
        self.assertIn('आत्मनि एव आत्मना', verses[54]['anvaya'])
        self.assertIn('इव', verses[66]['anvaya'])
        self.assertIn('यद्वत्', verses[69]['anvaya'])

    def test_chapter_three_draft_corrections(self):
        chapter = json.loads((ROOT / 'source/ch3.json').read_text(encoding='utf-8'))
        verses = [v for t in chapter['themes'] for p in t['parts'] for v in p['sutras']]
        self.assertEqual(len([v for v in verses if 'anvaya' in v]), 43)
        self.assertIn('सन्न्यसनात्', verses[3]['anvaya'])
        self.assertNotIn('सन्ति', verses[26]['anvaya'])
        self.assertIn('चेत्', verses[23]['anvaya'])
        self.assertEqual(verses[37]['anvaya'].count('यथा'), 2)
        self.assertIn('आवृतः', verses[37]['anvaya'])

    def test_chapter_four_draft_corrections(self):
        chapter = json.loads((ROOT / 'source/ch4.json').read_text(encoding='utf-8'))
        verses = [v for t in chapter['themes'] for p in t['parts'] for v in p['sutras']]
        self.assertEqual(len([v for v in verses if 'anvaya' in v]), 42)
        self.assertIn('भक्तः सखा च असि इति', verses[2]['anvaya'])
        self.assertEqual(verses[5]['anvaya'].count('अपि'), 2)
        self.assertIn('ज्ञानावस्थितचेतसः', verses[22]['anvaya'])
        self.assertIn('ब्रह्मार्पणं', verses[23]['anvaya'])
        self.assertNotIn('सन्ति', verses[27]['anvaya'])

    def test_chapter_five_draft_corrections(self):
        chapter = json.loads((ROOT / 'source/ch5.json').read_text(encoding='utf-8'))
        verses = [v for t in chapter['themes'] for p in t['parts'] for v in p['sutras']]
        self.assertEqual(len([v for v in verses if 'anvaya' in v]), 29)
        self.assertEqual(verses[0]['anvaya'].count('शंससि'), 1)
        self.assertIn('इव', verses[9]['anvaya'])
        self.assertIn('अक्षयम्', verses[20]['anvaya'])
        self.assertEqual(verses[23]['anvaya'].count('यः'), 2)
        self.assertEqual(verses[26]['anvaya'].count('कृत्वा'), 2)

    def test_chapter_six_draft_corrections(self):
        chapter = json.loads((ROOT / 'source/ch6.json').read_text(encoding='utf-8'))
        verses = [v for t in chapter['themes'] for p in t['parts'] for v in p['sutras']]
        self.assertEqual(len([v for v in verses if 'anvaya' in v]), 47)
        self.assertIn('असन्न्यस्तसङ्कल्पः', verses[1]['anvaya'])
        self.assertEqual(verses[5]['anvaya'].count('एव'), 2)
        self.assertIn('एकाकी', verses[9]['anvaya'])
        self.assertIn('स्वं नासिकाग्रं', verses[12]['anvaya'])
        self.assertEqual(verses[20]['anvaya'].count('यत्र'), 2)
        self.assertIn('एतत् हि', verses[41]['anvaya'])
        self.assertIn('सः', verses[43]['anvaya'])

    def test_reader_places_optional_unboxed_sanskrit_before_literal(self):
        reader = (ROOT / 'source/js/50-reader.js').read_text(encoding='utf-8')
        container = reader.index('class="m-verse-box-container"')
        anvaya = reader.index('s.anvaya ?', container)
        literal = reader.index('class="m-line lit"', anvaya)
        self.assertLess(container, anvaya)
        self.assertLess(anvaya, literal)
        self.assertIn('lang="sa"', reader[anvaya:literal])
        self.assertIn('esc(s.anvaya)', reader[anvaya:literal])
        self.assertIn("L('anvaya')", reader[anvaya:literal])
        self.assertIn("state.lang === 'en' && s.anvaya_iast", reader[anvaya:literal])
        self.assertIn('lang="sa-Latn"', reader[anvaya:literal])
        self.assertIn('esc(s.anvaya_iast)', reader[anvaya:literal])

    def test_heading_localized_and_speaker_kept(self):
        import sys
        sys.path.insert(0, str(ROOT / 'source'))
        from i18n_ui import UI
        self.assertEqual(UI['en']['anvaya'], 'Anvaya')
        self.assertEqual(UI['ne']['anvaya'], 'अन्वयः')
        self.assertEqual(UI['hi']['anvaya'], 'अन्वयः')
        for num in range(1, 19):
            chapter = json.loads((ROOT / f'source/ch{num}.json').read_text(encoding='utf-8'))
            for theme in chapter['themes']:
                for part in theme['parts']:
                    for verse in part['sutras']:
                        if 'anvaya' in verse:
                            for row in verse['flow']:
                                if row['k'] == 's':
                                    self.assertIn(row['d'].rstrip('। '), verse['anvaya'], verse['n'])


if __name__ == '__main__':
    unittest.main()
