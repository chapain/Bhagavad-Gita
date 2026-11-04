"""Pin manually reviewed split glosses against their literal context.

Semantic reasoning is in docs/padachheda-review.md; these snapshots detect
changes to either side of that review, not semantic equivalence by algorithm.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEWED = json.loads(r'''{
  "1.18": {
    "rows": [
      [
        "पृथक्",
        "pṛthak",
        "separately",
        "छुट्टै",
        "पृथक्"
      ],
      [
        "पृथक्",
        "pṛthak",
        "separately (repeated: each his own)",
        "छुट्टै (दोहोरिएर: आ-आफ्नो)",
        "पृथक् (दोहराकर: अपने-अपने)"
      ]
    ],
    "lits": {
      "en": "Drupada and the sons of Draupadī, O lord of the earth, and the mighty-armed son of Subhadrā — all blew their conches, each his own.",
      "ne": "द्रुपद र द्रौपदीका छोराहरू, हे पृथ्वीपति, र महाबाहु सुभद्रापुत्र — सबैले आ-आफ्ना शङ्ख बजाए।",
      "hi": "द्रुपद और द्रौपदी के पुत्र, हे पृथ्वीपति, और महाबाहु सुभद्रा-पुत्र — सब ने अपने-अपने शंख बजाए।"
    }
  },
  "2.06": {
    "rows": [
      [
        "यत्",
        "yat",
        "whether",
        "कि",
        "कि"
      ],
      [
        "वा",
        "vā",
        "or",
        "वा",
        "या"
      ]
    ],
    "lits": {
      "en": "Nor do we know which is better for us — to conquer them or be conquered. The very sons of Dhṛtarāṣṭra stand before us; killing them, we should not care to live.",
      "ne": "र हामीलाई थाहा छैन कि हाम्रा निम्ति के राम्रो — तिनलाई जित्नु वा तिनीसँग पराजित हुनु। धृतराष्ट्रका छोराहरू नै हाम्रो अगाडि उभिएका छन्; तिनलाई मारेपछि हामी जिउन चाहँदैनौं।",
      "hi": "और हम नहीं जानते कि हमारे लिए क्या अच्छा है — इन्हें जीतना या इनसे पराजित होना। धृतराष्ट्र के ये पुत्र ही हमारे सामने खड़े हैं; इन्हें मारकर हम जीना नहीं चाहेंगे।"
    }
  },
  "2.39": {
    "rows": [
      [
        "तु",
        "tu",
        "but",
        "तर",
        "पर"
      ]
    ],
    "lits": {
      "en": "This wisdom of sāṅkhya has been declared to you, O Pārtha. Now hear the wisdom of yoga; joined with it, you will cast off the bondage of karma.",
      "ne": "हे पार्थ, यो साङ्ख्य बुद्धि तिमीलाई भनियो। अब योगबुद्धि सुन; यससँग जोडिएर तिमी कर्मबन्धन त्याग्नेछौ।",
      "hi": "हे पार्थ, यह सांख्य-बुद्धि तुझसे कही गई। अब योग-बुद्धि सुन; इससे युक्त होकर तू कर्म-बन्धन से छूट जाएगा।"
    }
  },
  "2.57": {
    "rows": [
      [
        "तत्",
        "tat",
        "this",
        "यो",
        "यह"
      ],
      [
        "तत्",
        "tat",
        "that (repeated: whatever comes)",
        "त्यो (दोहोरिएर: जे आए पनि)",
        "वह (दोहराकर: जो भी मिले)"
      ]
    ],
    "lits": {
      "en": "One who is without affection everywhere, who neither rejoices nor recoils on meeting good or evil — that one's wisdom is firmly set.",
      "ne": "जो सर्वत्र आसक्तिरहित छ, शुभ वा अशुभ पाएर न रम्छ न रिसाउँछ — त्यसको बुद्धि दृढ स्थापित हुन्छ।",
      "hi": "जो सर्वत्र स्नेहरहित है, शुभ या अशुभ पाकर न हर्षित होता है न विमुख — उसकी बुद्धि दृढ़ स्थापित है।"
    }
  },
  "9.30": {
    "rows": [
      [
        "सम्यक्",
        "samyak",
        "rightly",
        "ठीकसँग",
        "ठीक तरह से"
      ],
      [
        "व्यवसितः",
        "vyavasitaḥ",
        "resolved",
        "संकल्प गरेको",
        "संकल्प किया हुआ"
      ]
    ],
    "lits": {
      "en": "Even if a man of very evil conduct worships me with single-minded devotion, he is to be regarded as good, for he is rightly resolved.",
      "ne": "अति दुष्ट आचरणको मानिसले पनि यदि एकनिष्ठ भक्तिले मेरो पूजा गर्छ भने, ऊ असल नै मानिनुपर्छ, किनकि उसको संकल्प ठीक छ।",
      "hi": "अति दुष्ट आचरण वाला पुरुष भी यदि एकनिष्ठ भक्ति से मेरी पूजा करता है, तो वह साधु ही माना जाना चाहिए, क्योंकि उसका संकल्प ठीक है।"
    }
  },
  "13.32": {
    "rows": [
      [
        "सर्वत्र",
        "sarvatra",
        "everywhere",
        "सर्वत्र",
        "सर्वत्र"
      ],
      [
        "अवस्थितः",
        "avasthitaḥ",
        "present",
        "रहेको",
        "स्थित"
      ]
    ],
    "lits": {
      "en": "As the all-pervading space is not stained, being subtle, so the Self, present in every body, is not stained.",
      "ne": "जसरी सर्वव्यापी आकाश, सूक्ष्म भएर, दागिँदैन, त्यसरी नै हरेक शरीरमा रहेको आत्मा दागिँदैन।",
      "hi": "जैसे सर्वव्यापी आकाश, सूक्ष्म होने के कारण, लिप्त नहीं होता, वैसे ही हर शरीर में स्थित आत्मा लिप्त नहीं होती।"
    }
  }
}
''')


class PadachhedaGlossTests(unittest.TestCase):
    def test_reviewed_glosses_and_literal_context(self):
        for number, expected in REVIEWED.items():
            with self.subTest(verse=number):
                chapter = json.loads((ROOT / "source" / f"ch{number.split('.')[0]}.json").read_text())
                verses = [v for theme in chapter["themes"] for part in theme["parts"]
                          for v in part["sutras"] if v["n"] == number]
                self.assertEqual(len(verses), 1)
                verse = verses[0]
                self.assertEqual(verse["lits"], expected["lits"])
                # Require the whole reviewed sequence, not just words anywhere
                # in the verse (tat/pṛthak occur twice, in this exact order).
                matches = sum(
                    item["words"][i:i + len(expected["rows"])] == expected["rows"]
                    for item in verse["flow"] if item["k"] == "p"
                    for i in range(len(item["words"]))
                )
                self.assertEqual(matches, 1)

    def test_sarve_before_eva_has_outside_sandhi_form(self):
        chapter = json.loads((ROOT / "source" / "ch1.json").read_text())
        for number in ("1.06", "1.11"):
            verse = next(v for theme in chapter["themes"] for part in theme["parts"]
                         for v in part["sutras"] if v["n"] == number)
            sequence = [["सर्वे", "sarve", "all", "सबै", "सब"],
                        ["एव", "eva", "indeed", "नै", "ही"]]
            self.assertTrue(any(
                item["words"][i:i + 2] == sequence
                for item in verse["flow"] for i in range(len(item["words"]))
            ), number)
            self.assertIn("sarva eva", verse["t"])

    def test_no_space_joined_rows_or_tv_fragments(self):
        for path in sorted((ROOT / "source").glob("ch[0-9]*.json")):
            chapter = json.loads(path.read_text())
            for theme in chapter["themes"]:
                for part in theme["parts"]:
                    for verse in part["sutras"]:
                        for item in verse["flow"]:
                            for row in item["words"]:
                                with self.subTest(verse=verse["n"], row=row[:2]):
                                    self.assertEqual(len(row[0].split()), 1)
                                    self.assertEqual(len(row[1].split()), 1)
                                    self.assertNotEqual(row[0], "त्व्")
                                    self.assertNotEqual(row[1], "tv")


if __name__ == "__main__":
    unittest.main()
