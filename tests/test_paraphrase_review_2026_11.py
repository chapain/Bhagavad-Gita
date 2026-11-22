"""Focused regressions for the trilingual paraphrase review, not a semantic oracle."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verse(number):
    chapter = int(number.split('.')[0])
    data = json.loads((ROOT / 'source' / f'ch{chapter}.json').read_text())
    return next(v for theme in data['themes'] for part in theme['parts']
                for v in part['sutras'] if v['n'] == number)


class ParaphraseReview(unittest.TestCase):
    def assert_phrases(self, number, phrases):
        for language, phrase in zip(('en', 'ne', 'hi'), phrases):
            with self.subTest(verse=number, language=language):
                self.assertIn(phrase, verse(number)['paras'][language])

    def test_contrast_and_conditional(self):
        self.assert_phrases('1.10', ('is sufficient', 'सेना पर्याप्त छ', 'सेना पर्याप्त है'))
        self.assertNotIn('though shielded', verse('1.10')['paras']['en'])
        self.assert_phrases('3.23', ('people follow my path', 'मानिसहरू सबै प्रकारले मेरो बाटो', 'लोग हर प्रकार से मेरा मार्ग'))
        self.assertNotIn('give up their duties', verse('3.23')['paras']['en'])
        self.assert_phrases('3.24', ('cause confusion', 'सङ्करको कारण', 'संकर का कारण'))
        self.assert_phrases('6.16', ('stay awake too much', 'धेरै जाग्नेको', 'अत्यधिक जागने वाले'))

    def test_key_words_and_relationships(self):
        self.assert_phrases('2.16', ('truth of both', 'दुवैको सत्य', 'दोनों का सत्य'))
        self.assert_phrases('2.40', ('no adverse result', 'न उल्टो फल हुन्छ', 'कोई विपरीत फल नहीं'))
        self.assert_phrases('2.45', ('acquire and preserve', 'प्राप्ति र रक्षाको', 'प्राप्ति और रक्षा की'))
        self.assert_phrases('2.57', ('hateful toward', 'द्वेष गर्दैन', 'द्वेष नहीं करता'))
        self.assert_phrases('12.17', ('nor hates', 'न द्वेष', 'न द्वेष'))
        self.assert_phrases('2.65', ('intellect of the serene', 'बुद्धि छिट्टै स्थिर', 'बुद्धि शीघ्र स्थिर'))
        self.assertIn('Brahman itself of the Imperishable', verse('3.15')['paras']['en'])
        self.assert_phrases('5.07', ('self of all beings', 'सबै प्राणीको आत्मा बनेको', 'सब प्राणियों की आत्मा बन गई'))
        self.assert_phrases('6.09', ('those who are hated', 'घृणा गरिएका व्यक्ति', 'जिनसे द्वेष किया जाता है'))
        self.assert_phrases('6.14', ('chaste', 'ब्रह्मचर्यको व्रत', 'ब्रह्मचर्य-व्रत'))
        self.assert_phrases('6.46', ('person of action', 'कर्मी', 'कर्मी'))
        self.assert_phrases('13.24', ('by the self', 'आत्मैले', 'आत्मा के ही द्वारा'))
        for number in ('3.03', '5.02', '13.24'):
            self.assertNotIn('selfless', verse(number)['paras']['en'])

    def test_separate_verses_keep_their_own_clauses(self):
        self.assert_phrases('6.21', ('intellect grasps', 'बुद्धिले ग्रहण', 'बुद्धि से ग्रहण'))
        self.assert_phrases('6.21', ('from the truth', 'सत्यबाट', 'सत्य से'))
        self.assert_phrases('6.22', ('no greater gain', 'अरू कुनै लाभ ठूलो', 'कोई और लाभ बड़ा'))
        self.assert_phrases('6.23', ('Know this separation', 'योग जान', 'योग जान'))
        for language, phrase in (('en', 'know that as yoga'), ('ne', 'त्यही योग हो'), ('hi', 'वही योग है')):
            self.assertNotIn(phrase, verse('6.22')['paras'][language])
        for language, phrase in (('en', 'mouth'), ('ne', 'मुखतिर'), ('hi', 'मुँह')):
            self.assertNotIn(phrase, verse('11.26')['paras'][language])
        self.assert_phrases('11.27', ('mouths', 'मुखभित्र', 'मुखों'))
        self.assert_phrases('12.18', ('honour and dishonour', 'आदर होस् वा अपमान', 'आदर हो या अपमान'))
        self.assert_phrases('12.19', ('praise', 'निन्दा', 'निन्दा'))

    def test_sense_objects_and_timing(self):
        self.assert_phrases('2.58', ('senses from their objects', 'इन्द्रियलाई विषयबाट', 'इन्द्रियों को विषयों से'))
        self.assertNotIn('danger', verse('2.58')['paras']['en'])
        self.assert_phrases('5.23', ('before leaving the body', 'शरीर छोड्नुअघि', 'शरीर छोड़ने से पहले'))
        self.assert_phrases('6.17', ('sleep and waking', 'निद्रा र जागरण', 'नींद और जागने'))


if __name__ == '__main__':
    unittest.main()
