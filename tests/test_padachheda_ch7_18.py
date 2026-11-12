"""Pins reviewed word splits, not machine-inferred semantic equivalence.

11.47's Hindi literal conflict remains documented, not certified as agreement.
"""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEWED = json.loads(r'''{
  "11.37": {
    "sequence": [
      [
        "तत्",
        "tat",
        "that",
        "त्यो",
        "वह"
      ],
      [
        "परम्",
        "param",
        "beyond both",
        "दुवैभन्दा पर",
        "दोनों से परे"
      ]
    ],
    "lits": {
      "en": "Why should they not bow to you, O great soul, greater than Brahmā, the primal creator — O infinite Lord of gods, abode of the universe, you are the imperishable, being and non-being and beyond both.",
      "ne": "हे महात्मा, आदि सृष्टिकर्ता ब्रह्माभन्दा पनि ठूलो तपाईंलाई तिनीहरूले किन नझुकून् — हे देवताहरूका अनन्त स्वामी, ब्रह्माण्डका आश्रय, तपाईं नै अविनाशी, सत् र असत् र दुवैभन्दा पर हुनुहुन्छ?",
      "hi": "हे महात्मा, आदि सृष्टिकर्ता ब्रह्मा से भी श्रेष्ठ आपको वे क्यों न झुकें — हे देवों के अनन्त स्वामी, जगत् के आश्रय, आप ही अविनाशी, सत् और असत् और दोनों से परे हैं?"
    },
    "flow_text": [
      [
        "कस्माच्च ते न नमेरन्महात्मन्",
        "kasmācca te na nameranmahātman"
      ],
      [
        "गरीयसे ब्रह्मणोऽप्यादिकर्त्रे",
        "garīyase brahmaṇo’pyādikartre"
      ],
      [
        "अनन्त देवेश जगन्निवास",
        "ananta deveśa jagannivāsa"
      ],
      [
        "त्वमक्षरं सदसत्तत्परं यत्",
        "tvamakṣaraṃ sadasattatparaṃ yat"
      ]
    ]
  },
  "11.47": {
    "sequence": [
      [
        "त्वत्",
        "tvat",
        "than you",
        "तिमीभन्दा",
        "तुझसे"
      ],
      [
        "अन्येन",
        "anyena",
        "by another",
        "अरूद्वारा",
        "अन्य द्वारा"
      ]
    ],
    "lits": {
      "en": "The Blessed Lord said: By my grace, Arjuna, I have shown you this supreme form by my own power — the luminous, universal, infinite, primeval form that none but you has ever seen.",
      "ne": "श्रीभगवान्ले भन्नुभयो: हे अर्जुन, मैले कृपाले आफ्नै शक्तिले तिमीलाई यो परम रूप देखाएँ — तेजोमय, विश्वरूपी, अनन्त, आदिम रूप — जुन तिमीबाहेक अरू कसैले कहिल्यै देखेको छैन।",
      "hi": "श्री भगवान् ने कहा: हे अर्जुन, मैंने कृपा करके अपनी शक्ति से तुझे यह परम रूप दिखाया — तेजोमय, विश्व-रूपी, अनन्त, आदिम रूप — जिसे तेरे सिवा पहले किसी ने नहीं देखा।"
    },
    "flow_text": [
      [
        "श्रीभगवानुवाच।",
        "śrībhagavānuvāca"
      ],
      [
        "मया प्रसन्नेन तवार्जुनेदं",
        "mayā prasannena tavārjunedaṃ"
      ],
      [
        "रूपं परं दर्शितमात्मयोगात्",
        "rūpaṃ paraṃ darśitamātmayogāt"
      ],
      [
        "तेजोमयं विश्वमनन्तमाद्यं",
        "tejomayaṃ viśvamanantamādyaṃ"
      ],
      [
        "यन्मे त्वदन्येन न दृष्टपूर्वम्",
        "yanme tvadanyena na dṛṣṭapūrvam"
      ]
    ]
  },
  "11.48": {
    "sequence": [
      [
        "त्वत्",
        "tvat",
        "than you",
        "तिमीभन्दा",
        "तुझसे"
      ],
      [
        "अन्येन",
        "anyena",
        "by another",
        "अरूद्वारा",
        "अन्य द्वारा"
      ]
    ],
    "lits": {
      "en": "Not by the study of the Vedas and sacrifices, nor by gifts, rites or fierce austerities, can I be seen in this form in the world of men — by any but you, O prince of the Kurus.",
      "ne": "हे कुरुप्रवीर, वेदको अध्ययन, यज्ञ, दान, अनुष्ठान वा कठोर तपस्या — कुनै पनि विधिबाट, मानव लोकमा, तिमीबाहेक अरू कसैले मलाई यस रूपमा देख्न सक्दैन।",
      "hi": "हे कुरुप्रवीर, वेदों के अध्ययन, यज्ञ, दान, अनुष्ठान या घोर तपस्या से — किसी भी उपाय से, मनुष्य-लोक में, तुझे छोड़कर कोई मुझे इस रूप में नहीं देख सकता।"
    },
    "flow_text": [
      [
        "न वेदयज्ञाध्ययनैर्न दानैर्",
        "na vedayajñādhyayanairna dānair"
      ],
      [
        "न च क्रियाभिर्न तपोभिरुग्रैः",
        "na ca kriyābhirna tapobhirugraiḥ"
      ],
      [
        "एवंरूपः शक्य अहं नृलोके",
        "evaṃrūpaḥ śakya ahaṃ nṛloke"
      ],
      [
        "द्रष्टुं त्वदन्येन कुरुप्रवीर",
        "draṣṭuṃ tvadanyena kurupravīra"
      ]
    ]
  },
  "16.03": {
    "sequence": [
      [
        "न",
        "na",
        "not",
        "न",
        "नहीं"
      ],
      [
        "अतिमानिता",
        "atimānitā",
        "excessive pride",
        "अत्यधिक अभिमान",
        "अत्यधिक अभिमान"
      ]
    ],
    "lits": {
      "en": "— vigour, forgiveness, fortitude, purity, freedom from malice and from pride — these belong to one born to the divine destiny, O Bhārata.",
      "ne": "— तेज, क्षमा, धैर्य, शुद्धता, द्वेषरहितता र अभिमानरहितता — यी हे भारत, दैवी सम्पत्ति भएर जन्मेकाका चिह्न हुन्।",
      "hi": "— तेज, क्षमा, धैर्य, शुद्धता, द्वेष-रहितता और अभिमान-रहितता — ये, हे भारत, दैवी सम्पदा से जन्मे की पहचान हैं।"
    },
    "flow_text": [
      [
        "तेजः क्षमा धृतिः शौचम्",
        "tejaḥ kṣamā dhṛtiḥ śaucam"
      ],
      [
        "अद्रोहो नातिमानिता",
        "adroho nātimānitā"
      ],
      [
        "भवन्ति सम्पदं दैवीम्",
        "bhavanti sampadaṃ daivīm"
      ],
      [
        "अभिजातस्य भारत",
        "abhijātasya bhārata"
      ]
    ]
  },
  "18.17": {
    "sequence": [
      [
        "न",
        "na",
        "not",
        "न",
        "नहीं"
      ],
      [
        "अहंकृतः",
        "ahaṁkṛtaḥ",
        "egoistic",
        "अहंकारयुक्त",
        "अहंकारयुक्त"
      ]
    ],
    "lits": {
      "en": "He whose mind is free from ego, whose intellect is not stained — though he slays these worlds, he slays not, nor is bound.",
      "ne": "जसको मन अहंकाररहित छ, जसको बुद्धि दागिएको छैन — उसले यी लोकहरूलाई मारे पनि, ऊ मार्दैन, न बाँधिन्छ।",
      "hi": "जिसका मन अहंकार से रहित है, जिसकी बुद्धि लिप्त नहीं है — वह इन लोकों को मारकर भी नहीं मारता, और न बँधता है।"
    },
    "flow_text": [
      [
        "यस्य नाहंकृतो भावो",
        "yasya nāhaṃkṛto bhāvo"
      ],
      [
        "बुद्धिर्यस्य न लिप्यते",
        "buddhiryasya na lipyate"
      ],
      [
        "हत्वापि स इमांल्लोकान्",
        "hatvāpi sa imāṃllokān"
      ],
      [
        "न हन्ति न निबध्यते",
        "na hanti na nibadhyate"
      ]
    ]
  },
  "18.47": {
    "sequence": [
      [
        "कुर्वन्",
        "kurvan",
        "doing",
        "गर्दै",
        "करते हुए"
      ],
      [
        "न",
        "na",
        "not",
        "न",
        "नहीं"
      ],
      [
        "आप्नोति",
        "āpnoti",
        "incurs",
        "प्राप्त गर्दछ",
        "प्राप्त करता है"
      ],
      [
        "किल्बिषम्",
        "kilbiṣam",
        "sin",
        "पाप",
        "पाप"
      ]
    ],
    "lits": {
      "en": "Better is one's own dharma, though imperfect, than another's well-performed; doing the work born of his own nature, a man incurs no sin.",
      "ne": "आफ्नो धर्म, यद्यपि दोषपूर्ण, पराया सुसम्पन्न धर्मभन्दा राम्रो; आफ्नै स्वभावबाट जन्मेको काम गर्दा मानिस पापमा लाग्दैन।",
      "hi": "अपना धर्म, यद्यपि दोषयुक्त, पराए सुसम्पन्न धर्म से अच्छा है; अपने स्वभाव से उत्पन्न कर्म करने से मनुष्य पाप नहीं करता।"
    },
    "flow_text": [
      [
        "श्रेयान्स्वधर्मो विगुणः",
        "śreyānsvadharmo viguṇaḥ"
      ],
      [
        "परधर्मात्स्वनुष्ठितात्",
        "paradharmātsvanuṣṭhitāt"
      ],
      [
        "स्वभावनियतं कर्म",
        "svabhāvaniyataṃ karma"
      ],
      [
        "कुर्वन्नाप्नोति किल्बिषम्",
        "kurvannāpnoti kilbiṣam"
      ]
    ]
  },
  "18.76": {
    "sequence": [
      [
        "मुहुः",
        "muhuḥ",
        "again",
        "फेरि",
        "फिर"
      ],
      [
        "मुहुः",
        "muhuḥ",
        "again (repeated: repeatedly)",
        "फेरि (दोहोरिएर: बारम्बार)",
        "फिर (दोहराकर: बार-बार)"
      ]
    ],
    "lits": {
      "en": "Remembering again and again this wondrous, holy dialogue of Keśava and Arjuna, O king, I rejoice again and again.",
      "ne": "हे राजन्, केशव र अर्जुनको यो अद्भुत, पवित्र संवाद बारम्बार सम्झेर, म बारम्बार रमाउँछु।",
      "hi": "हे राजन्, केशव और अर्जुन के इस अद्भुत, पवित्र संवाद को बार-बार स्मरण करके, मैं बार-बार हर्षित होता हूँ।"
    },
    "flow_text": [
      [
        "राजन् संस्मृत्य संस्मृत्य",
        "rājan saṃsmṛtya saṃsmṛtya"
      ],
      [
        "संवादमिममद्भुतम्",
        "saṃvādamimamadbhutam"
      ],
      [
        "केशवार्जुनयोः पुण्यं",
        "keśavārjunayoḥ puṇyaṃ"
      ],
      [
        "हृष्यामि च मुहुर्मुहुः",
        "hṛṣyāmi ca muhurmuhuḥ"
      ]
    ]
  }
}
''')


class RemainingPadachhedaTests(unittest.TestCase):
    def test_reviewed_rows_preserve_literal_and_printed_context(self):
        for number, expected in REVIEWED.items():
            with self.subTest(verse=number):
                chapter = json.loads((ROOT / "source" / f"ch{number.split('.')[0]}.json").read_text())
                verse = next(v for t in chapter["themes"] for p in t["parts"]
                             for v in p["sutras"] if v["n"] == number)
                self.assertEqual(verse["lits"], expected["lits"])
                self.assertEqual([[f["d"], f["t"]] for f in verse["flow"]], expected["flow_text"])
                seq = expected["sequence"]
                self.assertEqual(sum(f["words"][i:i + len(seq)] == seq
                                     for f in verse["flow"] for i in range(len(f["words"]))), 1)

    def test_both_doing_not_incur_sin_clauses_have_explicit_na(self):
        for chapter_number, number in ((4, "4.21"), (18, "18.47")):
            chapter = json.loads((ROOT / "source" / f"ch{chapter_number}.json").read_text())
            verse = next(v for t in chapter["themes"] for p in t["parts"]
                         for v in p["sutras"] if v["n"] == number)
            self.assertEqual([w[1] for w in verse["flow"][-1]["words"]],
                             ["kurvan", "na", "āpnoti", "kilbiṣam"])

    def test_ledger_has_one_primary_verdict_per_canonical_verse(self):
        # Coverage only; this cannot prove the quality of an editorial judgment.
        text = (ROOT / "docs" / "padachheda-verse-review.md").read_text()
        first = text.split("## Batch 1 — 1.01–1.20")[1].split("## Exact corrections")[0]
        second = text.split("## Batch 2 — 1.21–6.47")[1].split("### Changed-row meanings")[0]
        third = text.split("## Batch 3 — 7.01–18.78")[1].split("### Final-batch semantic review")[0]
        actual = re.findall(r"^\| (\d+\.\d+) \|", first + second + third, re.M)
        expected = [v["n"] for c in range(1, 19)
                    for t in json.loads((ROOT / "source" / f"ch{c}.json").read_text())["themes"]
                    for p in t["parts"] for v in p["sutras"]]
        self.assertEqual(len(actual), 700)
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
