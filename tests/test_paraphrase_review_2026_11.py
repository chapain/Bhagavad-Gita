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

    def test_second_batch_meaning_and_context(self):
        self.assert_phrases('7.16', ('seeker of wealth', 'सम्पत्ति चाहने', 'धन चाहने'))
        self.assert_phrases('7.17', ('The wise one', 'तीमध्ये ज्ञानी', 'उनमें ज्ञानी'))
        self.assert_phrases('8.02', ('who is adhiyajña', 'को हुनुहुन्छ र कसरी', 'कौन है और कैसे'))
        self.assert_phrases('8.06', ('ever absorbed', 'सधैं त्यही भावमा', 'सदा उसी भाव में'))
        self.assert_phrases('8.09', ('seer and ruler', 'द्रष्टा र शासक', 'द्रष्टा और शासक'))
        self.assert_phrases('8.11', ('celibacy', 'ब्रह्मचर्य', 'ब्रह्मचर्य'))
        self.assert_phrases('9.12', ('deluding', 'भ्रममा पार्ने', 'भ्रम में डालने'))
        self.assert_phrases('9.19', ('immortality and death', 'अमरत्व र मृत्यु', 'अमरत्व और मृत्यु'))
        self.assert_phrases('10.06', ('sharing my nature', 'मेरो स्वभाव भएका', 'मेरे स्वभाव वाले'))
        self.assert_phrases('10.28', ('power of procreation', 'सन्तान उत्पन्न गराउने', 'सन्तान उत्पन्न कराने'))
        self.assert_phrases('10.35', ('Mārgaśīrṣa', 'मार्गशीर्ष', 'मार्गशीर्ष'))
        self.assert_phrases('10.38', ('seeking victory', 'विजय चाहने', 'जीत चाहने'))
        self.assert_phrases('11.33', ('be merely the instrument', 'माध्यम बन', 'माध्यम बन'))
        self.assert_phrases('11.34', ('other warrior-heroes', 'अरू वीर योद्धाहरू', 'दूसरे वीर योद्धाओं'))
        self.assert_phrases('11.38', ('you pervade', 'तपाईंले सम्पूर्ण', 'आप पूरे ब्रह्माण्ड में व्याप्त'))
        self.assert_phrases('11.42', ('in jest', 'मजाकमा', 'मज़ाक में'))
        self.assert_phrases('12.11', ('my yoga', 'मेरो योग', 'मेरे योग'))
        self.assert_phrases('12.13', ('forgiving', 'क्षमाशील', 'क्षमा करता'))
        self.assertIn('अनन्य भक्ति', verse('11.54')['paras']['hi'])
        self.assertNotIn('only as you have seen', verse('11.53')['paras']['en'])
        self.assertIn('give rise to the body', verse('14.20')['paras']['en'])
        self.assertIn('बुद्धि-योग', verse('18.57')['paras']['hi'])

    def test_third_batch_and_targeted_followups(self):
        self.assert_phrases('13.15', ('cannot be known', 'जान्न सकिँदैन', 'जाना नहीं जा सकता'))
        self.assertIn('as though divided', verse('13.16')['paras']['en'])
        self.assert_phrases('13.25', ('do not know in this way', 'यसरी नजानेका', 'इस तरह न जानकर'))
        self.assert_phrases('13.28', ('by the self', 'आत्माद्वारा', 'आत्मा से आत्मा'))
        self.assert_phrases('13.34', ('liberation of beings', 'प्राणीहरूको मुक्ति', 'प्राणियों की मुक्ति'))
        self.assert_phrases('14.24', ('directed at him', 'आफ्नो प्रशंसा', 'अपनी प्रशंसा'))
        self.assert_phrases('14.25', ('sides of friend and foe', 'शत्रुका पक्ष', 'शत्रु के पक्षों'))
        self.assertIn('fit to become Brahman', verse('14.26')['paras']['en'])
        self.assertIn('fit to become Brahman', verse('18.53')['paras']['en'])
        self.assert_phrases('15.14', ('in-breath and out-breath', 'आउने र जाने श्वास', 'साँसों के आने-जाने'))
        self.assert_phrases('16.17', ('in name only', 'नाममात्रका', 'नाम के ही'))
        self.assert_phrases('16.18', ("others' bodies", 'अरूको शरीरमा', 'दूसरों के शरीरों में'))
        self.assert_phrases('17.10', ('rotting or stale', 'कुहिएको, बासी', 'सड़ा, बासी'))
        self.assert_phrases('18.08', ('fear of bodily suffering', 'शारीरिक कष्टको डरले', 'शारीरिक पीड़ा से डरकर'))
        self.assert_phrases('18.10', ('free from doubt', 'सन्देहरहित', 'संदेह से मुक्त'))
        self.assert_phrases('18.15', ('your body', 'शरीरले', 'शरीर से'))
        self.assert_phrases('18.25', ('loss, injury', 'क्षति, हिंसा', 'नुकसान, हिंसा'))
        self.assert_phrases('18.44', ('śūdra’s natural work', 'शूद्रको स्वाभाविक काम', 'शूद्र का स्वाभाविक काम'))
        self.assertIn('through the self', verse('2.55')['paras']['en'])
        self.assertIn('delusion of the pairs', verse('7.28')['paras']['en'])
        self.assert_phrases('5.27', ('in-breath and out-breath', 'आउने र जाने श्वास', 'आती-जाती साँस'))

    def test_sense_objects_and_timing(self):
        self.assert_phrases('2.58', ('senses from their objects', 'इन्द्रियलाई विषयबाट', 'इन्द्रियों को विषयों से'))
        self.assertNotIn('danger', verse('2.58')['paras']['en'])
        self.assert_phrases('5.23', ('before leaving the body', 'शरीर छोड्नुअघि', 'शरीर छोड़ने से पहले'))
        self.assert_phrases('6.17', ('sleep and waking', 'निद्रा र जागरण', 'नींद और जागने'))


if __name__ == '__main__':
    unittest.main()
