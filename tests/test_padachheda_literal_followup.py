"""Targeted regressions for the 2026-11-22 word-row/literal follow-up."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verse(number):
    chapter = int(number.split('.')[0])
    data = json.loads((ROOT / 'source' / f'ch{chapter}.json').read_text())
    return next(v for theme in data['themes'] for part in theme['parts']
                for v in part['sutras'] if v['n'] == number)


def row(v, word):
    matches = [r for f in v['flow'] for r in f['words'] if r[0] == word]
    assert len(matches) == 1, (v['n'], word)
    return matches[0]


class PadachhedaLiteralFollowup(unittest.TestCase):
    def test_cross_verse_absolutives_remain_dependent(self):
        for n, word, following in (('1.20', 'उद्यम्य', '1.21'),
                                   ('1.24', 'स्थापयित्वा', '1.25')):
            v, next_v = verse(n), verse(following)
            self.assertTrue(row(v, word)[2].startswith('having '))
            self.assertTrue(any(r[0] in ('आह', 'उवाच') for f in next_v['flow']
                                for r in f['words']))
            for lang in ('en', 'ne', 'hi'):
                with self.subTest(verse=n, lang=lang):
                    self.assertTrue(v['lits'][lang].endswith('—'))
        self.assertIn('raising his bow', verse('1.20')['lits']['en'])
        self.assertIn('राखेर', verse('1.24')['lits']['ne'])
        self.assertIn('रखकर', verse('1.24')['lits']['hi'])

    def test_english_participles_have_plausible_actors(self):
        self.assertIn('What pleasure would be ours in slaying', verse('1.36')['lits']['en'])
        self.assertIn('when one has seen the Supreme, even that taste departs',
                      verse('2.59')['lits']['en'])

    def test_sukha_and_bhoga_are_distinct_in_1_32(self):
        v = verse('1.32')
        self.assertEqual(row(v, 'सुखानि')[3:], ['सुखहरू', 'सुख'])
        self.assertEqual(row(v, 'भोगैः')[3:], ['भोगहरूले', 'भोगों से'])
        for lang, first, later in (('ne', 'न सुखहरू', 'भोगको'),
                                   ('hi', 'न सुख', 'भोगों से')):
            with self.subTest(lang=lang):
                self.assertIn(first, v['lits'][lang])
                self.assertIn(later, v['lits'][lang])

    def test_niyatam_is_context_sensitive(self):
        self.assertEqual(row(verse('1.44'), 'नियतम्')[2:],
                         ['certainly', 'निश्चित रूपमा', 'निश्चित रूप से'])
        self.assertEqual(row(verse('3.08'), 'नियतम्')[3:], ['विहित', 'विहित'])
        self.assertIn('निश्चित रूप से', verse('1.44')['lits']['hi'])

    def test_2_02_hindi_does_not_reverse_arya_qualifier(self):
        v = verse('2.02')
        self.assertEqual(row(v, 'अनार्य')[4], 'आर्य-अयोग्य')
        self.assertIn('आर्य को न शोभने वाली', v['lits']['hi'])

    def test_2_30_and_2_32_hindi_grammar(self):
        self.assertIn('तुझे किसी भी प्राणी के लिए शोक नहीं करना चाहिए', verse('2.30')['lits']['hi'])
        self.assertIn('अनायास प्राप्त', verse('2.32')['lits']['hi'])
        self.assertNotIn('आफैं', verse('2.32')['lits']['hi'])

    def test_2_36_ne_keeps_many(self):
        v = verse('2.36')
        self.assertEqual(row(v, 'बहून्')[3], 'धेरै')
        self.assertIn('धेरै नभन्नुपर्ने कुराहरू', v['lits']['ne'])

    def test_2_41_ne_retains_irresolution(self):
        v = verse('2.41')
        self.assertEqual(row(v, 'अव्यवसायिनाम्')[3], 'अनिश्चयीहरूका')
        self.assertIn('अनिश्चयीहरूका', v['lits']['ne'])

    def test_2_57_uses_hating_not_recoiling(self):
        v = verse('2.57')
        self.assertEqual(row(v, 'द्वेष्टि')[2], 'hates')
        for lang, expected in (('en', 'nor hates'), ('ne', 'न द्वेष गर्छ'),
                               ('hi', 'न द्वेष करता है')):
            with self.subTest(lang=lang):
                self.assertIn(expected, v['lits'][lang])

    def test_2_69_first_clause_does_not_borrow_the_sage(self):
        v = verse('2.69')
        self.assertEqual(row(v, 'संयमी')[2], 'the disciplined one')
        self.assertEqual(row(v, 'मुनेः')[2], 'sage')
        for lang, first in (('en', 'the disciplined one is awake'),
                            ('ne', 'त्यसमा संयमी जाग्छ'),
                            ('hi', 'उसमें संयमी जागता है')):
            with self.subTest(lang=lang):
                self.assertIn(first, v['lits'][lang])

    def test_inexhaustible_and_indestructible_stay_distinct_when_paired(self):
        first, second = verse('2.17'), verse('2.21')
        self.assertEqual(row(first, 'अव्ययस्य')[3:], ['अक्षयको', 'अक्षय का'])
        self.assertEqual(row(first, 'अविनाशि')[3:], ['अविनाशी', 'अविनाशी'])
        self.assertEqual(row(second, 'अव्ययम्')[4], 'अक्षय')
        self.assertEqual(row(second, 'अविनाशिनम्')[4], 'अविनाशी को')

    def test_contextual_word_glosses(self):
        expected = {
            ('2.16', 'अन्तः'): 'the truth (conclusion)',
            ('3.29', 'कर्मसु'): 'in actions',
            ('3.39', 'अनलेन'): 'by fire (like fire here)',
            ('4.11', 'भजामि'): 'I favour, I receive',
            ('5.07', 'सर्वभूतात्मभूतात्मा'): 'whose self has become the self of all beings',
            ('6.09', 'सुहृत्'): 'well-wisher',
            ('6.09', 'द्वेष्य'): 'one who is hated',
            ('6.42', 'दुर्लभतरम्'): 'harder to obtain',
            ('7.13', 'एभ्यः'): 'than these',
            ('8.09', 'कविम्'): 'the seer',
            ('8.20', 'परः'): 'beyond',
            ('8.20', 'तस्मात्'): 'than that',
        }
        for (n, word), gloss in expected.items():
            with self.subTest(verse=n, word=word):
                self.assertEqual(row(verse(n), word)[2], gloss)

    def test_new_literal_findings(self):
        fragments = {
            '3.05': ('helpless', 'असहाय', 'असहाय'),
            '3.12': ('to them', 'तिनीहरूलाई', 'उन्हें'),
            '3.25': ('desiring the welfare', 'गर्न चाहने', 'करना चाहने'),
            '3.26': ('the wise one', 'ज्ञानीले', 'ज्ञानी'),
            '4.03': ('today', 'आज', 'आज'),
            '4.08': ('evil-doers', 'दुष्कर्मी', 'दुष्कर्मियों'),
            '4.19': ('actions are burnt', 'कर्महरू ज्ञानाग्निले जलेका', 'कर्म ज्ञानाग्नि से दग्ध'),
            '5.07': ('self of all beings', 'सबै प्राणीको आत्मा बनेको', 'सब प्राणियों की आत्मा बन गई'),
            '6.09': ('those hated', 'घृणा गरिएका', 'जिनसे घृणा की जाती है'),
            '6.15': ('supreme nirvāṇa', 'परम निर्वाण', 'परम निर्वाण'),
            '6.20': ('mind, restrained', 'संयत मन', 'संयत मन'),
            '6.21': ('beyond the senses', 'इन्द्रियभन्दा पर', 'इन्द्रियों से परे'),
            '6.26': ('Wherever', 'जहाँ-जहाँ', 'जहाँ-जहाँ'),
            '6.42': ('harder to obtain', 'अझ कठिन', 'और भी दुर्लभ'),
            '6.46': ('men of action', 'कर्मीभन्दा', 'कर्मियों से'),
            '7.03': ('perfected who strive', 'प्रयत्न गर्ने सिद्धहरूमध्ये', 'प्रयत्न करने वाले सिद्धों में'),
            '7.23': ('devotees indeed come', 'भक्तहरू पनि', 'भक्त भी'),
            '7.30': ('adhibhūta, adhidaiva and adhiyajña', 'अधिभूत, अधिदैव र अधियज्ञ', 'अधिभूत, अधिदैव और अधियज्ञ'),
            '8.03': ('supreme Brahman', 'परम ब्रह्म', 'परम ब्रह्म'),
            '8.10': ('breath properly fixed', 'प्राण राम्ररी स्थिर', 'प्राण को भली-भाँति स्थिर'),
            '8.26': ('held to be', 'मानिन्छन्', 'माने जाते हैं'),
            '8.28': ('knowing all this', 'यो सबै जानेर', 'यह सब जानकर'),
            '9.29': ('hated', 'घृणित', 'घृणित'),
        }
        for n, values in fragments.items():
            for lang, value in zip(('en', 'ne', 'hi'), values):
                with self.subTest(verse=n, lang=lang):
                    self.assertIn(value, verse(n)['lits'][lang])
        self.assertIn('straight and unmoving', verse('6.13')['lits']['en'])
        self.assertIn('एकाग्र मन से', verse('8.08')['lits']['hi'])
        self.assertIn('my inmost self trembling', verse('11.24')['lits']['en'])
        self.assertNotIn('abiding in that', verse('6.31')['lits']['en'])


if __name__ == '__main__':
    unittest.main()
