"""Reviewed boundary/gloss regressions; not an automated semantic oracle.

The literal and printed-pāda snapshots are review context, never runtime data.
6.19 context was updated by the sourced conflict-resolution pass; see its report.
See docs/padachheda-verse-review.md for grammatical and trilingual reasoning.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEWED = json.loads(r'''{
  "1.47": {
    "sequences": [
      [
        [
          "रथोपस्थे",
          "rathopasthe",
          "on the chariot-seat",
          "रथको आसनमा",
          "रथ के आसन पर"
        ]
      ]
    ],
    "lits": {
      "en": "Sañjaya said: Having spoken thus on the battlefield, Arjuna sat down on the seat of the chariot, casting aside his bow and arrows, his mind overwhelmed with grief.",
      "ne": "सञ्जयले भने: युद्धभूमिमा यसरी बोलेर, अर्जुन रथको आसनमा बसे, धनुष-बाण त्यागेर, मन शोकले भरिएको।",
      "hi": "संजय ने कहा: युद्धभूमि में ऐसा कहकर, अर्जुन रथ के आसन पर बैठ गया, धनुष-बाण त्यागकर, मन शोक से भरा हुआ।"
    },
    "flow_text": [
      [
        "सञ्जय उवाच।",
        "sañjaya uvāca"
      ],
      [
        "एवमुक्त्वार्जुनः सङ्ख्ये",
        "evamuktvārjunaḥ saṅkhye"
      ],
      [
        "रथोपस्थ उपाविशत्",
        "rathopastha upāviśat"
      ],
      [
        "विसृज्य सशरं चापं",
        "visṛjya saśaraṃ cāpaṃ"
      ],
      [
        "शोकसंविग्नमानसः",
        "śokasaṃvignamānasaḥ"
      ]
    ]
  },
  "2.12": {
    "sequences": [
      [
        [
          "तु",
          "tu",
          "but",
          "तर",
          "पर"
        ],
        [
          "एव",
          "eva",
          "indeed",
          "नै",
          "ही"
        ]
      ]
    ],
    "lits": {
      "en": "Never was there a time I did not exist, nor you, nor these rulers of men; nor will any of us ever cease to be hereafter.",
      "ne": "यस्तो कुनै समय थिएन जब म थिइनँ, न तिमी थिएनौ, न यी राजाहरू; र भविष्यमा पनि हामीमध्ये कोही अस्तित्वहीन हुनेछैन।",
      "hi": "ऐसा कोई समय नहीं था जब मैं नहीं था, न तू था, न ये राजा थे; और भविष्य में भी हममें से कोई नहीं रहेगा, ऐसा नहीं है।"
    },
    "flow_text": [
      [
        "न त्वेवाहं जातु नासं",
        "na tvevāhaṃ jātu nāsaṃ"
      ],
      [
        "न त्वं नेमे जनाधिपाः",
        "na tvaṃ neme janādhipāḥ"
      ],
      [
        "न चैव न भविष्यामः",
        "na caiva na bhaviṣyāmaḥ"
      ],
      [
        "सर्वे वयमतः परम्",
        "sarve vayamataḥ param"
      ]
    ]
  },
  "2.16": {
    "sequences": [
      [
        [
          "तु",
          "tu",
          "but",
          "तर",
          "पर"
        ],
        [
          "अनयोः",
          "anayoḥ",
          "of these two",
          "यी दुईका",
          "इन दोनों का"
        ]
      ]
    ],
    "lits": {
      "en": "The unreal has no being; the real never ceases to be. The truth of both is seen by the seers of the essence.",
      "ne": "असत्को अस्तित्व हुँदैन; सत् कहिल्यै अस्तित्वहीन हुँदैन। दुवैको अन्त्य तत्त्वदर्शीहरूले देखेका छन्।",
      "hi": "असत् का अस्तित्व नहीं है; सत् कभी अस्तित्वहीन नहीं होता। दोनों का यह तत्त्व तत्त्वदर्शियों ने देखा है।"
    },
    "flow_text": [
      [
        "नासतो विद्यते भावो",
        "nāsato vidyate bhāvo"
      ],
      [
        "नाभावो विद्यते सतः",
        "nābhāvo vidyate sataḥ"
      ],
      [
        "उभयोरपि दृष्टोऽन्तस्",
        "ubhayorapi dṛṣṭo’ntas"
      ],
      [
        "त्वनयोस्तत्त्वदर्शिभिः",
        "tvanayostattvadarśibhiḥ"
      ]
    ]
  },
  "2.19": {
    "sequences": [
      [
        [
          "न",
          "na",
          "not",
          "न",
          "नहीं"
        ],
        [
          "अयम्",
          "ayam",
          "this (Self)",
          "यो (आत्मा)",
          "यह (आत्मा)"
        ]
      ]
    ],
    "lits": {
      "en": "Whoever thinks the Self is the killer, and whoever thinks it is killed — neither truly knows: it does not kill, nor is it killed.",
      "ne": "जसले आत्मालाई मार्ने ठान्छ, र जसले आत्मा मारिन्छ भनी ठान्छ — दुवै साँच्चै बुझ्दैनन्: यसले न मार्छ न मारिन्छ।",
      "hi": "जो आत्मा को मारने वाला समझता है, और जो आत्मा मारा जाता है समझता है — दोनों सचमुच नहीं जानते: यह न मारता है, न मारा जाता है।"
    },
    "flow_text": [
      [
        "य एनं वेत्ति हन्तारं",
        "ya enaṃ vetti hantāraṃ"
      ],
      [
        "यश्चैनं मन्यते हतम्",
        "yaścainaṃ manyate hatam"
      ],
      [
        "उभौ तौ न विजानीतो",
        "ubhau tau na vijānīto"
      ],
      [
        "नायं हन्ति न हन्यते",
        "nāyaṃ hanti na hanyate"
      ]
    ]
  },
  "2.20": {
    "sequences": [
      [
        [
          "न",
          "na",
          "not",
          "न",
          "नहीं"
        ],
        [
          "अयम्",
          "ayam",
          "this (Self)",
          "यो (आत्मा)",
          "यह (आत्मा)"
        ]
      ]
    ],
    "lits": {
      "en": "It is never born, never dies; having been, it will never again cease to be. Unborn, eternal, everlasting and ancient — it is not slain when the body is slain.",
      "ne": "यो कहिल्यै जन्मँदैन, कहिल्यै मर्दैन; भएपछि यो फेरि कहिल्यै नहुने होइन। अजन्मा, नित्य, शाश्वत र पुरातन — शरीर मारिए पनि यो मारिँदैन।",
      "hi": "यह कभी जन्मता नहीं, कभी मरता नहीं; होकर यह फिर कभी न होने वाला नहीं है। अजन्मा, नित्य, शाश्वत और पुरातन — शरीर मारे जाने पर यह नहीं मारा जाता।"
    },
    "flow_text": [
      [
        "न जायते म्रियते वा कदाचिन्",
        "na jāyate mriyate vā kadācin"
      ],
      [
        "नायं भूत्वा भविता वा न भूयः",
        "nāyaṃ bhūtvā bhavitā vā na bhūyaḥ"
      ],
      [
        "अजो नित्यः शाश्वतोऽयं पुराणो",
        "ajo nityaḥ śāśvato’yaṃ purāṇo"
      ],
      [
        "न हन्यते हन्यमाने शरीरे",
        "na hanyate hanyamāne śarīre"
      ]
    ]
  },
  "2.40": {
    "sequences": [
      [
        [
          "न",
          "na",
          "not",
          "न",
          "नहीं"
        ],
        [
          "इह",
          "iha",
          "here",
          "यहाँ",
          "यहाँ"
        ]
      ]
    ],
    "lits": {
      "en": "Here there is no loss of effort, nor any contrary result. Even a little of this dharma protects one from great fear.",
      "ne": "यहाँ आरम्भको नाश हुँदैन, न उल्टो फल नै हुन्छ। यस धर्मको अलिकति पनि ठूलो भयबाट रक्षा गर्छ।",
      "hi": "यहाँ आरम्भ का नाश नहीं होता, न उल्टा फल ही होता है। इस धर्म का अल्प-सा भी अंश महान् भय से रक्षा करता है।"
    },
    "flow_text": [
      [
        "नेहाभिक्रमनाशोऽस्ति",
        "nehābhikramanāśo’sti"
      ],
      [
        "प्रत्यवायो न विद्यते",
        "pratyavāyo na vidyate"
      ],
      [
        "स्वल्पमप्यस्य धर्मस्य",
        "svalpamapyasya dharmasya"
      ],
      [
        "त्रायते महतो भयात्",
        "trāyate mahato bhayāt"
      ]
    ]
  },
  "2.41": {
    "sequences": [
      [
        [
          "एका",
          "ekā",
          "single",
          "एक",
          "एक"
        ],
        [
          "इह",
          "iha",
          "here",
          "यहाँ",
          "यहाँ"
        ]
      ]
    ],
    "lits": {
      "en": "The intellect of the resolute is single and one-pointed here, O joy of the Kurus; but the intellects of the irresolute branch out endlessly.",
      "ne": "हे कुरुनन्दन, यहाँ दृढनिश्चयीहरूको बुद्धि एक, एकाग्र हुन्छ; तर चञ्चलहरूका बुद्धिहरू अनन्त शाखामा फैलिन्छन्।",
      "hi": "हे कुरुनन्दन, यहाँ दृढ़निश्चयी की बुद्धि एक, एकाग्र होती है; किन्तु अनिश्चयी की बुद्धियाँ अनन्त शाखाओं में फैलती हैं।"
    },
    "flow_text": [
      [
        "व्यवसायात्मिका बुद्धिर्",
        "vyavasāyātmikā buddhir"
      ],
      [
        "एकेह कुरुनन्दन",
        "ekeha kurunandana"
      ],
      [
        "बहुशाखा ह्यनन्ताश्च",
        "bahuśākhā hyanantāśca"
      ],
      [
        "बुद्धयोऽव्यवसायिनाम्",
        "buddhayo’vyavasāyinām"
      ]
    ]
  },
  "4.21": {
    "sequences": [
      [
        [
          "कुर्वन्",
          "kurvan",
          "performing",
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
          "incurs, meets",
          "प्राप्त गर्दछ",
          "प्राप्त करता है"
        ]
      ]
    ],
    "lits": {
      "en": "Free from desire, with the mind and self controlled, having given up all possessions, performing only bodily action, he does not incur sin.",
      "ne": "आशा रहित, मन र आत्मा संयत गरेर, सबै परिग्रह त्यागेर, केवल शारीरिक कर्म गर्दा ऊ पापमा लाग्दैन।",
      "hi": "आशा से रहित, मन और आत्मा को संयत कर, सब परिग्रह त्यागकर, केवल शारीरिक कर्म करने से वह पाप को नहीं प्राप्त होता।"
    },
    "flow_text": [
      [
        "निराशीर्यतचित्तात्मा",
        "nirāśīryatacittātmā"
      ],
      [
        "त्यक्तसर्वपरिग्रहः",
        "tyaktasarvaparigrahaḥ"
      ],
      [
        "शारीरं केवलं कर्म",
        "śārīraṃ kevalaṃ karma"
      ],
      [
        "कुर्वन्नाप्नोति किल्बिषम्",
        "kurvannāpnoti kilbiṣam"
      ]
    ]
  },
  "4.26": {
    "sequences": [
      [
        [
          "अन्ये",
          "anye",
          "others",
          "अरूहरू",
          "अन्य"
        ]
      ]
    ],
    "lits": {
      "en": "Some offer hearing and the other senses into the fires of restraint; others offer sound and the other sense-objects into the fires of the senses.",
      "ne": "केहीले श्रवण आदि इन्द्रियहरूलाई संयमरूपी अग्निमा अर्पण गर्छन्; अरूले शब्द आदि विषयहरूलाई इन्द्रियरूपी अग्निमा अर्पण गर्छन्।",
      "hi": "कुछ लोग श्रवण आदि इन्द्रियों को संयम-रूप अग्नि में आहुति करते हैं; अन्य शब्द आदि विषयों को इन्द्रिय-रूप अग्नि में आहुति करते हैं।"
    },
    "flow_text": [
      [
        "श्रोत्रादीनीन्द्रियाण्यन्ये",
        "śrotrādīnīndriyāṇyanye"
      ],
      [
        "संयमाग्निषु जुह्वति",
        "saṃyamāgniṣu juhvati"
      ],
      [
        "शब्दादीन्विषयानन्य",
        "śabdādīnviṣayānanya"
      ],
      [
        "इन्द्रियाग्निषु जुह्वति",
        "indriyāgniṣu juhvati"
      ]
    ]
  },
  "5.16": {
    "sequences": [
      [
        [
          "तत्",
          "tat",
          "that (knowledge)",
          "त्यो (ज्ञान)",
          "वह (ज्ञान)"
        ],
        [
          "परम्",
          "param",
          "the Supreme",
          "परम तत्त्व",
          "परम तत्त्व"
        ]
      ]
    ],
    "lits": {
      "en": "But for those whose ignorance is destroyed by the knowledge of the Self, that knowledge shines forth like the sun, revealing the Supreme.",
      "ne": "तर जसको अज्ञान आत्मज्ञानले नष्ट भएको छ, तिनको त्यो ज्ञान सूर्यझैं चम्किएर परम तत्त्व प्रकट गर्छ।",
      "hi": "किन्तु जिनका अज्ञान आत्म-ज्ञान से नष्ट हो चुका है, उनका वह ज्ञान सूर्य के समान चमककर परम तत्त्व को प्रकट करता है।"
    },
    "flow_text": [
      [
        "ज्ञानेन तु तदज्ञानं",
        "jñānena tu tadajñānaṃ"
      ],
      [
        "येषां नाशितमात्मनः",
        "yeṣāṃ nāśitamātmanaḥ"
      ],
      [
        "तेषामादित्यवज्ज्ञानं",
        "teṣāmādityavajjñānaṃ"
      ],
      [
        "प्रकाशयति तत्परम्",
        "prakāśayati tatparam"
      ]
    ]
  },
  "6.19": {
    "sequences": [
      [
        [
          "न",
          "na",
          "not",
          "न",
          "नहीं"
        ],
        [
          "इङ्गते",
          "iṅgate",
          "flickers",
          "चलमलाउँछ",
          "डगमगाता है"
        ]
      ],
      [
        [
          "सा",
          "sā",
          "that (simile)",
          "त्यो (उपमा)",
          "वह (उपमा)"
        ]
      ]
    ],
    "lits": {
      "en": "As a lamp placed in a windless spot does not flicker — this simile is declared of a yogi of controlled mind, practising yoga of the Self.",
      "ne": "जसरी हावा नभएको ठाउँमा राखिएको बत्ती चलमलाउँदैन — संयत मनको, आत्मयोगको अभ्यास गर्ने योगीको यही उपमा भनिएको छ।",
      "hi": "जैसे हवा रहित स्थान में रखा दीपक नहीं डगमगाता — ऐसा ही संयत मन वाले, आत्म-योग का अभ्यास करने वाले योगी का दृष्टान्त कहा गया है।"
    },
    "flow_text": [
      [
        "यथा दीपो निवातस्थो",
        "yathā dīpo nivātastho"
      ],
      [
        "नेङ्गते सोपमा स्मृता",
        "neṅgate sopamā smṛtā"
      ],
      [
        "योगिनो यतचित्तस्य",
        "yogino yatacittasya"
      ],
      [
        "युञ्जतो योगमात्मनः",
        "yuñjato yogamātmanaḥ"
      ]
    ]
  },
  "6.39": {
    "sequences": [
      [
        [
          "त्वत्",
          "tvat",
          "than you",
          "तिमीभन्दा",
          "तुझसे"
        ],
        [
          "अन्यः",
          "anyaḥ",
          "other",
          "अरू",
          "अन्य"
        ]
      ]
    ],
    "lits": {
      "en": "This doubt of mine you should dispel wholly, O Kṛṣṇa; no other than you is found to destroy this doubt.",
      "ne": "हे कृष्ण, तपाईंले नै मेरो यो सन्देह पूर्ण रूपमा मेट्नुपर्छ; यो सन्देह नष्ट गर्ने तपाईंबाहेक अरू कोही देखिँदैन।",
      "hi": "हे कृष्ण, आपको ही मेरा यह सन्देह पूर्णतः दूर करना चाहिए; इस सन्देह को नष्ट करने वाला आपके अतिरिक्त और कोई नहीं दिखता।"
    },
    "flow_text": [
      [
        "एतन्मे संशयं कृष्ण",
        "etanme saṃśayaṃ kṛṣṇa"
      ],
      [
        "छेत्तुमर्हस्यशेषतः",
        "chettumarhasyaśeṣataḥ"
      ],
      [
        "त्वदन्यः संशयस्यास्य",
        "tvadanyaḥ saṃśayasyāsya"
      ],
      [
        "छेत्ता न ह्युपपद्यते",
        "chettā na hyupapadyate"
      ]
    ]
  }
}
''')


class ChapterOneToSixPadachhedaTests(unittest.TestCase):
    def test_reviewed_changes_keep_literal_and_printed_context(self):
        for number, expected in REVIEWED.items():
            with self.subTest(verse=number):
                chapter = json.loads((ROOT / "source" / f"ch{number.split('.')[0]}.json").read_text())
                verse = next(v for t in chapter["themes"] for p in t["parts"]
                             for v in p["sutras"] if v["n"] == number)
                self.assertEqual(verse["lits"], expected["lits"])
                self.assertEqual([[f["d"], f["t"]] for f in verse["flow"]],
                                 expected["flow_text"])
                for sequence in expected["sequences"]:
                    self.assertEqual(sum(
                        f["words"][i:i + len(sequence)] == sequence
                        for f in verse["flow"] for i in range(len(f["words"]))
                    ), 1)

    def test_negation_is_explicit_at_four_twenty_one(self):
        # Reconstruction alone accepted kurvan + āpnoti through optional
        # final-n doubling. The literal's negative must have its own row.
        chapter = json.loads((ROOT / "source" / "ch4.json").read_text())
        verse = next(v for t in chapter["themes"] for p in t["parts"]
                     for v in p["sutras"] if v["n"] == "4.21")
        self.assertEqual([w[1] for w in verse["flow"][-1]["words"]],
                         ["kurvan", "na", "āpnoti", "kilbiṣam"])


if __name__ == "__main__":
    unittest.main()
