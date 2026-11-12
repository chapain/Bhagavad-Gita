"""Semantic-audit regressions: the verdicts of docs/semantic-audit.md, pinned.

The audit reads verses against the Sanskrit and records a verdict for each one
before anything is edited. These tests pin what that reading decided, so a
later edit to either side of a reviewed verdict is detected instead of being
assumed harmless. They are snapshots of human judgement, not a semantic
algorithm: nothing here can tell that a gloss is *wrong*, only that it moved
without the ledger moving with it.

**Scope: the whole book.** All 700 verses of chapters 1-18 have now been read
in one pass (see `docs/semantic-audit.md`), so these pins cover every edit that
reading produced - F1-F9, sixteen strings in seven verses - and the class
checks run over every verse of the book.

Rules from the audit that are enforced mechanically, because they are checkable:

1. A word row's gloss must not contradict the verse's own literal (AGENTS.md:
   the literal is the semantic standard). The instrument rows of 1.13 broke
   this and are now pinned.
2. A row that carries a comparison ("to X") must not be glossed with a
   preposition of departure in Hindi (`से` = from). 1.04's `भीम` row did
   exactly that, and it was the only such row in the book.
3. Two *different* Sanskrit words inside one verse may not carry one English
   gloss, because the reader cannot then tell the rows apart - the defect
   1.13 had. The same word may repeat with the same gloss (बलम् twice in
   1.10 is correct). Every pair that survives this rule was read during the
   audit and is listed in REVIEWED_SAME_GLOSS: a pair that is not listed is a
   finding, and a listed pair that no longer exists must be taken out.
4. In the Nepali, the negator "न" is a prefix of a *verb* (नजान्ने, नपाएर,
   नहेर्दै) and is written apart from a *nominal* (न स्थित, न प्राप्त). A
   row or literal that runs the two together has produced a word that does not
   exist - the defect in 5.12 and 3.22.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = list(range(1, 19))


def all_verses():
    """Every verse of the book, in chapter and verse order."""
    out = []
    for number in CHAPTERS:
        chapter = json.loads((ROOT / "source" / f"ch{number}.json").read_text())
        for theme in chapter["themes"]:
            for part in theme["parts"]:
                out.extend(part["sutras"])
    return out


def rows_of(verse):
    return [row for item in verse["flow"] for row in item["words"]]


def load_verse(number):
    for verse in all_verses():
        if verse["n"] == number:
            return verse
    raise AssertionError(number)


# The verses read so far. The ledger and this list must agree.
AUDITED = [verse["n"] for verse in all_verses()]

# Rows whose glosses the audit read word by word, with the verse literal they
# were read against. Every corrected verse is pinned in full; the others are
# covered by the rule tests below.
REVIEWED = {
    "1.04": {
        "rows": [
            ["भीम", "bhīma", "to Bhīma", "भीमसँग", "भीम के समान"],
            ["अर्जुन", "arjuna", "and Arjuna", "र अर्जुन", "और अर्जुन"],
            ["समाः", "samāḥ", "equal", "समान", "समान"],
        ],
        "lits": {
            "en": "Here are heroes, great archers, equals of Bhīma and Arjuna in war: Yuyudhāna, Virāṭa, and Drupada, the great chariot-warrior.",
            "ne": "यहाँ वीरहरू, महान् धनुर्धारीहरू छन् — युद्धमा भीम र अर्जुनका समान: युयुधान, विराट, र महारथी द्रुपद।",
            "hi": "यहाँ वीर हैं, महान धनुर्धारी, युद्ध में भीम और अर्जुन के समान: युयुधान, विराट, और महारथी द्रुपद।",
        },
    },
    "1.13": {
        "rows": [
            ["शङ्खाः", "śaṅkhāḥ", "conches", "शङ्खहरू", "शंख"],
            ["भेर्यः", "bheryaḥ", "drums", "नगाराहरू", "नगारे"],
            ["पणव", "paṇava", "kettledrums", "ढोलहरू", "ढोल"],
            ["आनक", "ānaka", "tabors", "मृदङ्ग", "मृदंग"],
            ["गोमुखाः", "gomukhāḥ", "horn-trumpets", "गोमुखहरू", "तुरहियाँ"],
        ],
        "lits": {
            "en": "Then conches, drums, kettledrums, tabors and horns were suddenly struck together — that sound became tumultuous.",
            "ne": "त्यसपछि शङ्ख, नगारा, ढोल, मृदङ्ग र गोमुखहरू एकैसाथ बजे — त्यो ध्वनि भयङ्कर बन्यो।",
            "hi": "तब शंख, नगाड़े, ढोल, मृदंग और तुरहियाँ एक साथ बज उठीं — वह ध्वनि भयानक हो गई।",
        },
    },
    "1.24": {
        # F5: the three paraphrases named a different addressee from the
        # literal, and the English one said the chariot was driven, not placed.
        "rows": [
            ["भारत", "bhārata", "O descendant of Bharata", "हे भारत", "हे भारत"],
            ["स्थापयित्वा", "sthāpayitvā", "having placed", "राखेर", "रखकर"],
        ],
        "lits": {
            "en": "Sañjaya said: Thus addressed by Gudākeśa, Hṛṣīkeśa, O descendant of Bharata, placed that best of chariots between the two armies.",
            "ne": "सञ्जयले भने: गुडाकेशद्वारा यसरी सम्बोधित भएर, हृषीकेशले, हे भरतवंशी, त्यो उत्तम रथ दुवै सेनाको बीचमा राखे।",
            "hi": "संजय ने कहा: गुडाकेश द्वारा ऐसा कहे जाने पर, हृषीकेश ने, हे भरतवंशी, उस उत्तम रथ को दोनों सेनाओं के बीच रखा।",
        },
        "paras": {
            "en": "Sañjaya continues: “So ordered by Arjuna, O descendant of Bharata, Kṛṣṇa placed the finest chariot between the two armies.”",
            "ne": "सञ्जय अगाडि भन्छन्: “अर्जुनको आदेश पाएर, हे भरतवंशी, कृष्णले उत्तम रथ दुवै सेनाको बीचमा राखे।”",
            "hi": "संजय आगे कहते हैं: “अर्जुन की आज्ञा पाकर, हे भरतवंशी, कृष्ण ने उत्तम रथ को दोनों सेनाओं के बीच रखा।”",
        },
    },
    "1.46": {
        # F6: the first privative `अ` row read "not" where the shape is the
        # same privative as the second one, which read "without".
        "rows": [
            ["अ", "a", "without", "बिना", "बिना"],
            ["प्रतीकारम्", "pratīkāram", "resisting", "रोकथाम", "रोकथाम"],
            ["अ", "a", "without", "बिना", "बिना"],
            ["शस्त्रम्", "śastram", "weapons (unarmed)", "शस्त्र", "शस्त्र"],
        ],
        "lits": {
            "en": "“If the sons of Dhṛtarāṣṭra, weapons in hand, should kill me in battle — me unarmed and unresisting — that would be better for me.”",
            "ne": "“यदि धृतराष्ट्रका छोराहरू, हातमा हतियार लिएर, युद्धमा मलाई मार्छन् — मलाई निःशस्त्र र प्रतिरोधरहित — त्यो मेरा लागि राम्रो हुनेछ।”",
            "hi": "“यदि धृतराष्ट्र के पुत्र, हाथ में शस्त्र लिए, युद्ध में मुझे मारें — मुझे निहत्थे और बिना प्रतिरोध — वह मेरे लिए बेहतर होगा।”",
        },
    },
    "2.10": {
        # F7: the paraphrase addressed "O Dhṛtarāṣṭra" and dropped the
        # "as if" that the literal carries for `prahasann iva`.
        "rows": [
            ["प्रहसन्", "prahasan", "smiling", "मुस्कुराउँदै", "मुस्कुराता हुआ"],
            ["इव", "iva", "as if", "झैँ", "के समान"],
            ["भारत", "bhārata", "O descendant of Bharata", "हे भारत", "हे भारत"],
        ],
        "lits": {
            "en": "To him, as he grieved between the two armies, Hṛṣīkeśa, as if smiling, spoke these words, O descendant of Bharata.",
            "ne": "दुवै सेनाको बीचमा शोक गरिरहेका उनलाई, हे भरतवंशी, हृषीकेशले जस्तो मुस्कुराएझैं यी वचन बोले।",
            "hi": "दोनों सेनाओं के बीच शोक करते हुए उसे, हे भरतवंशी, हृषीकेश ने मानो मुस्कुराकर ये वचन कहे।",
        },
        "paras": {
            "en": "Sañjaya adds: “Then, O descendant of Bharata, as Arjuna sat sorrowing between the two armies, Kṛṣṇa smiled as if and spoke to him.”",
            "ne": "सञ्जय थप्छन्: “त्यसपछि, हे भरतवंशी, दुवै सेनाको बीचमा शोकमा बसेका अर्जुनलाई कृष्णले जस्तो मुस्कुराएर भने।”",
            "hi": "संजय आगे कहते हैं: “तब, हे भरतवंशी, दोनों सेनाओं के बीच शोक में बैठे अर्जुन को कृष्ण ने जैसे मुस्कुराकर कहा।”",
        },
    },
    "3.22": {
        # F9: the Nepali word-row gloss ran the negator into its word -
        # "नप्राप्त", where the verse's own literal reads "न प्राप्त".
        "rows": [
            ["अनवाप्तम्", "anavāptam", "unattained", "न प्राप्त", "अप्राप्त"],
            ["अवाप्तव्यम्", "avāptavyam", "to be attained", "प्राप्त गर्नुपर्ने", "प्राप्त करने योग्य"],
        ],
        "lits": {
            "en": "For me, O Pārtha, there is nothing to be done in the three worlds, nothing unattained to be attained — yet I continue to act.",
            "ne": "हे पार्थ, मेरा निम्ति तीनै लोकमा गर्नुपर्ने केही छैन, न प्राप्त गर्न बाँकी केही छ — तैपनि म कर्ममा लागिरहन्छु।",
            "hi": "हे पार्थ, मेरे लिए तीनों लोकों में करने को कुछ नहीं है, न प्राप्त करने को अप्राप्त कुछ है — फिर भी मैं कर्म में लगा रहता हूँ।",
        },
    },
    "5.12": {
        # F8: the Nepali literal and the Nepali word-row gloss both ran two
        # words together - "योगमा नस्थित".
        "rows": [
            ["अयुक्तः", "ayuktaḥ", "the one not established in yoga", "योगमा न स्थित", "योग में स्थित नहीं"],
        ],
        "lits": {
            "en": "The one established in yoga, giving up the fruit of action, attains lasting peace; the one not established, impelled by desire, attached to the fruit, becomes bound.",
            "ne": "योगमा स्थित व्यक्तिले कर्मफल त्यागेर स्थायी शान्ति पाउँछ; योगमा न स्थित, इच्छाले प्रेरित, फलमा आसक्त व्यक्ति बाँधिन्छ।",
            "hi": "योग में स्थित व्यक्ति कर्म-फल का त्याग करके स्थायी शान्ति पाता है; योग में न स्थित, इच्छा से प्रेरित, फल में आसक्त व्यक्ति बँध जाता है।",
        },
    },
}

# Pairs of *different* Sanskrit words in one verse that carry one English
# gloss, and that the audit read and accepted. Each was checked in place:
# either the same lemma in a different surface form (इदम् / इमम्), or a
# synonym pair between which the reader loses nothing (एव / हि = "indeed"),
# or the house convention that a separate `न` row carries the negation and the
# negated verb keeps its plain gloss (1.31, 15.10).
REVIEWED_SAME_GLOSS = {
    ("1.28", ("इदम्", "इमम्"), "this"),
    ("16.13", ("इदम्", "इमम्"), "this"),
    ("1.29", ("मम", "मे"), "my"),
    ("1.31", ("अनुपश्यामि", "पश्यामि"), "i see"),
    ("1.35", ("कृते", "हेतोः"), "for the sake of"),
    ("1.42", ("एव", "हि"), "indeed"),
    ("1.42", ("कुल", "कुलस्य"), "of the family"),
    ("1.45", ("अहो", "बत"), "alas"),
    ("2.03", ("न", "मा"), "not"),
    ("2.05", ("तु", "हि"), "indeed"),
    ("2.05", ("एव", "हि"), "indeed"),
    ("2.09", ("इति", "एवम्"), "thus"),
    ("2.17", ("अस्य", "इदम्"), "this"),
    ("2.19", ("अयम्", "एनम्"), "this (self)"),
    ("2.25", ("अयम्", "एनम्"), "this"),
    ("2.27", ("ध्रुवः", "ध्रुवम्"), "certain"),
    ("2.35", ("त्वम्", "त्वाम्"), "you"),
    ("2.39", ("इमाम्", "एषा"), "this"),
    ("2.40", ("अस्ति", "विद्यते"), "is"),
    ("2.54", ("का", "किम्"), "what"),
    ("2.62", ("अभिजायते", "सञ्जायते"), "is born"),
    ("2.72", ("एनाम्", "एषा"), "this"),
    ("3.15", ("उद्भवम्", "समुद्भवम्"), "arising"),
    ("3.17", ("आत्म", "आत्मनि"), "in the self"),
    ("3.18", ("कश्चन", "कश्चित्"), "any"),
    ("3.24", ("इमाः", "इमे"), "these"),
    ("3.37", ("एनम्", "एषः"), "this"),
    ("3.38", ("आवृतः", "आवृतम्"), "covered"),
    ("3.42", ("परम्", "परा"), "higher"),
    ("4.03", ("अयम्", "एतत्"), "this"),
    ("4.05", ("वेत्थ", "वेद"), "know"),
    ("4.06", ("आत्म", "स्वाम्"), "my own"),
    ("4.12", ("सिद्धिः", "सिद्धिम्"), "success"),
    ("6.05", ("आत्मा", "आत्मानम्"), "the self"),
    ("6.05", ("आत्मा", "आत्मानम्"), "the self"),
    ("6.23", ("तम्", "सः"), "that"),
    ("6.39", ("अस्य", "एतत्"), "this"),
    ("6.40", ("एव", "हि"), "indeed"),
    ("6.42", ("एव", "हि"), "indeed"),
    ("6.44", ("एव", "हि"), "indeed"),
    ("7.05", ("इदम्", "इयम्"), "this"),
    ("7.14", ("एताम्", "एषा"), "this"),
    ("7.18", ("एव", "हि"), "indeed"),
    ("8.15", ("उपेत्य", "गताः"), "having reached"),
    ("8.17", ("युगसहस्रान्ताम्", "सहस्रयुगपर्यन्तम्"), "ending in a thousand yugas"),
    ("8.19", ("अयम्", "सः"), "this"),
    ("8.23", ("कालम्", "काले"), "time"),
    ("9.05", ("मम", "मे"), "my"),
    ("9.09", ("कर्मसु", "कर्माणि"), "actions"),
    ("9.23", ("यजन्ति", "यजन्ते"), "worship"),
    ("9.24", ("एव", "हि"), "indeed"),
    ("9.30", ("एव", "हि"), "indeed"),
    ("9.32", ("अपि", "तथा"), "also"),
    ("10.12", ("परमम्", "परम्"), "supreme"),
    ("10.15", ("आत्मानम्", "स्वयम्"), "yourself"),
    ("10.42", ("इदम्", "एतेन"), "this"),
    ("11.05", ("अथ", "च"), "and"),
    ("11.12", ("भाः", "भासः"), "the splendour"),
    ("11.12", ("भवेत्", "स्यात्"), "would be"),
    ("11.15", ("च", "तथा"), "and"),
    ("11.15", ("च", "तथा"), "and"),
    ("11.35", ("नमस्कृत्वा", "प्रणम्य"), "having bowed"),
    ("11.40", ("सर्वः", "सर्वम्"), "all"),
    ("11.41", ("सखा", "सखे"), "friend"),
    ("11.49", ("मम", "मे"), "my"),
    ("11.50", ("पुनः", "भूयः"), "again"),
    ("11.52", ("रूपम्", "रूपस्य"), "form"),
    ("12.14", ("मयि", "मे"), "to me"),
    ("13.01", ("इदम्", "एतत्"), "this"),
    ("13.18", ("च", "तथा"), "and"),
    ("13.19", ("अपि", "एव"), "indeed"),
    ("13.30", ("ततः", "तदा"), "then"),
    ("15.10", ("अनुपश्यन्ति", "पश्यन्ति"), "they see"),
    ("15.20", ("इदम्", "एतत्"), "this"),
    ("16.06", ("आसुरः", "आसुरम्"), "the demoniac"),
    ("17.02", ("ताम्", "सा"), "that"),
    ("17.03", ("श्रद्धः", "श्रद्धा"), "faith"),
    ("17.26", ("प्रयुज्यते", "युज्यते"), "is used"),
    ("17.27", ("अभिधीयते", "उच्यते"), "is called"),
    ("18.02", ("कवयः", "विचक्षणाः"), "the wise"),
    ("18.14", ("च", "तथा"), "and"),
    ("18.14", ("च", "तथा"), "and"),
    ("18.14", ("च", "तथा"), "and"),
    ("18.18", ("त्रिविधः", "त्रिविधा"), "threefold"),
    ("18.45", ("लभते", "विन्दति"), "attains"),
    ("18.45", ("संसिद्धिम्", "सिद्धिम्"), "perfection"),
    ("18.48", ("दोषेण", "सदोषम्"), "with fault"),
    ("18.65", ("माम्", "मे"), "to me"),
    ("18.68", ("परमम्", "पराम्"), "supreme"),
}

LATIN = re.compile(r"[A-Za-z]")


class SemanticAuditTests(unittest.TestCase):
    def test_the_ledger_records_every_chapter_of_the_book(self):
        """The ledger is the record of the reading; it must cover all 18
        chapters, and each chapter's ranges must cover that chapter's verses."""
        ledger = (ROOT / "docs" / "semantic-audit.md").read_text()
        headings = re.findall(
            r"^## Ledger — Chapter (\d+), (\d+)\.(\d+)–(\d+)\.(\d+)",
            ledger, re.M)
        self.assertTrue(headings, "the ledger has no chapter headings")
        covered = {}
        for chapter, lo_a, lo_b, hi_a, hi_b in headings:
            chapter = int(chapter)
            lo, hi = int(lo_a) * 100 + int(lo_b), int(hi_a) * 100 + int(hi_b)
            covered.setdefault(chapter, []).append((lo, hi))
        for chapter in CHAPTERS:
            with self.subTest(chapter=chapter):
                self.assertIn(chapter, covered,
                              f"chapter {chapter} has no ledger section")
                spans = sorted(covered[chapter])
                self.assertEqual(spans[0][0], chapter * 100 + 1)
                self.assertEqual(spans[-1][1],
                                 chapter * 100 + len([v for v in all_verses()
                                                      if v["n"].startswith(f"{chapter}.")]))

    def test_the_ledger_accounts_for_all_700_verses(self):
        ledger = (ROOT / "docs" / "semantic-audit.md").read_text()
        self.assertIn("| **Total** | **700** |", ledger)
        self.assertEqual(len(AUDITED), 700)
        self.assertEqual(len(set(AUDITED)), 700)

    def test_reviewed_rows_and_literal_context(self):
        for number, expected in REVIEWED.items():
            with self.subTest(verse=number):
                verse = load_verse(number)
                self.assertEqual(verse["lits"], expected["lits"])
                if "paras" in expected:
                    self.assertEqual(verse["paras"], expected["paras"])
                rows = rows_of(verse)
                for expected_row in expected["rows"]:
                    self.assertIn(expected_row, rows,
                                  f"{number}: reviewed row {expected_row[0]} moved")

    def test_every_duplicate_english_gloss_pair_is_reviewed(self):
        """1.13 had two rows both reading 'kettledrums' while its literal read
        'drums, kettledrums, tabors' — the reader could not reconcile them.
        The same word repeating (बलम् twice in 1.10) is allowed; two different
        Sanskrit words may not carry one gloss unless the audit accepted it."""
        for verse in all_verses():
            seen = {}
            for row in rows_of(verse):
                gloss = row[2].strip().lower()
                if gloss in seen:
                    if seen[gloss] == row[0]:
                        continue
                    key = (verse["n"], tuple(sorted((seen[gloss], row[0]))), gloss)
                    self.assertIn(key, REVIEWED_SAME_GLOSS,
                                  f"{verse['n']}: {seen[gloss]} and {row[0]} "
                                  f"are different words glossed '{row[2]}'")
                else:
                    seen[gloss] = row[0]

    def test_reviewed_duplicate_pairs_still_exist(self):
        """A reviewed pair that has been fixed must be taken out of the list,
        so the list cannot quietly keep an allowance alive."""
        for number, words, gloss in REVIEWED_SAME_GLOSS:
            with self.subTest(verse=number, gloss=gloss):
                rows = rows_of(load_verse(number))
                glossed = {r[0] for r in rows
                           if r[2].strip().lower() == gloss}
                self.assertTrue(set(words) <= glossed,
                                f"{number}: reviewed pair {words} no longer "
                                f"both read '{gloss}'")

    def test_english_instrument_rows_follow_the_english_literal(self):
        """The rule that caught 1.13: the instrument rows are read in the same
        order as the verse's own English literal lists them."""
        verse = load_verse("1.13")
        rows = rows_of(verse)
        instruments = ["conches", "drums", "kettledrums", "tabors", "horn-trumpets"]
        self.assertEqual([r[2] for r in rows if r[2] in instruments
                          or r[0] in ("शङ्खाः", "भेर्यः", "पणव", "आनक", "गोमुखाः")],
                         instruments)
        for gloss in ("drums", "kettledrums", "tabors"):
            self.assertIn(gloss, verse["lits"]["en"],
                          f"the literal must still name the {gloss}")

    def test_no_row_uses_a_preposition_of_departure_for_a_comparison(self):
        """Book-wide class guard for 1.04: the only row whose English gloss
        began 'to ' while its Hindi gloss used `से` ('from Bhīma')."""
        for path in sorted((ROOT / "source").glob("ch[0-9]*.json")):
            chapter = json.loads(path.read_text())
            for theme in chapter["themes"]:
                for part in theme["parts"]:
                    for verse in part["sutras"]:
                        for row in rows_of(verse):
                            with self.subTest(verse=verse["n"], row=row[0]):
                                if row[2].startswith("to "):
                                    self.assertNotIn(" से", row[4],
                                                     f"{verse['n']} {row[0]}: "
                                                     "'to X' glossed with 'from'")

    def test_rows_meaning_equal_keep_the_book_wide_style(self):
        """समः/समाः in the sense of 'equal' is glossed 'समान' in ne and hi
        everywhere in the book (11 rows). 1.04 must not be the place that
        breaks the pattern; the homograph in 6.41 means 'years' and is not."""
        seen = 0
        for path in sorted((ROOT / "source").glob("ch[0-9]*.json")):
            chapter = json.loads(path.read_text())
            for theme in chapter["themes"]:
                for part in theme["parts"]:
                    for verse in part["sutras"]:
                        for row in rows_of(verse):
                            if row[2] == "equal":
                                seen += 1
                                with self.subTest(verse=verse["n"], row=row[0]):
                                    self.assertEqual(row[3], "समान")
                                    self.assertEqual(row[4], "समान")
        self.assertGreaterEqual(seen, 10)

    def test_the_nepali_negator_is_never_run_into_its_word(self):
        """F8/F9 class guard, run over the whole book: in the Nepali, "न"
        prefixes a *verb* (नजान्ने, नपाएर, नहेर्दै) and stands apart from a
        *nominal* (न स्थित, न प्राप्त). 5.12 and 3.22 both had the two run
        together, so the word did not exist. The mechanical form of the check:
        a Nepali token that begins with an attached "न" while the same word
        also occurs in the book with "न" written apart."""
        tokens = set()
        apart = set()
        for verse in all_verses():
            texts = [verse["lits"]["ne"], verse["paras"]["ne"]]
            texts.extend(row[3] for row in rows_of(verse))
            for text in texts:
                words = [w.strip("।॥,.!?")
                         for w in re.split(r"[\s,;:।“”\"()—–-]+", text)]
                words = [w for w in words if w]
                tokens.update(words)
                apart.update(zip(words, words[1:]))
        for token in sorted(tokens):
            if len(token) > 2 and re.match(r"^न[क-ह]", token):
                with self.subTest(token=token):
                    self.assertNotIn(("न", token[1:]), apart,
                                     f"'{token}' runs the negator into its word")
        # the two spellings the audit rejected, named so that a repair of the
        # whole book cannot quietly bring them back
        for verse in all_verses():
            texts = [verse["lits"]["ne"], verse["paras"]["ne"]]
            texts.extend(row[3] for row in rows_of(verse))
            for text in texts:
                with self.subTest(verse=verse["n"]):
                    self.assertNotIn("योगमा नस्थित", text)
                    self.assertNotIn("नप्राप्त", text)

    def test_every_verse_carries_all_three_languages(self):
        """The class checks the audit ran over all 700 verses: no verse is
        missing a literal or a paraphrase in any language, no gloss is empty,
        and no Latin residue survives in the Nepali or the Hindi."""
        for verse in all_verses():
            with self.subTest(verse=verse["n"]):
                for key in ("lits", "paras"):
                    for language in ("en", "ne", "hi"):
                        self.assertTrue(verse.get(key, {}).get(language, "").strip(),
                                        f"{verse['n']} {key}.{language} is empty")
                for row in rows_of(verse):
                    for index, language in ((1, "iast"), (2, "en"),
                                            (3, "ne"), (4, "hi")):
                        self.assertTrue(str(row[index]).strip(),
                                        f"{verse['n']} {row[0]}: {language} gloss is empty")
                    for index, language in ((3, "ne"), (4, "hi")):
                        self.assertIsNone(LATIN.search(row[index]),
                                          f"{verse['n']} {row[0]}: Latin residue "
                                          f"in the {language} gloss")


if __name__ == "__main__":
    unittest.main()
