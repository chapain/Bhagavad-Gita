#!/usr/bin/env python3
"""tests/test_translation_fidelity.py — whole-book audits driven from the rows.

The owner's standard: "not just name presence or whatever — check through all 700
verses and make sure the translation represents the Sanskrit verse, not less not
more." Three classes are mechanically checkable without a reader:

    A. nothing added        a literal (or paraphrase) names something no word row
                            accounts for — the "more" half of the standard.
    B. cross-language lag   one language renders a verse less completely than both
                            the others, or than its own literal. This is the class
                            that catches 12.03 (Hindi paraphrase ending
                            "…कभी न बदलने वाला," with अचलम् and ध्रुवम् dropped)
                            with no human reading.
    C. parity               negation, number, name and vocative must survive in
                            every literal, not only the one an editor was reading.

Every check reads `flow[].words[]` first and the verse text (`v['d']`) never.
That is not style: the avagraha in 3.07's `नियम्यारभतेऽर्जुन` elides the initial
अ, so `'अर्जुन' in v['d']` is False while the row reads अर्जुन — the trap that
hid F12 from the first whole-book pass.

**What these checks cannot do.** They count tokens; they do not read. A pass says
a string did not lose a negation *marker*, not that the clause still means the
same thing. Where a language carries a negation inside a lexicon word (अचल =
not-moving, निर्दोष = fault-less) the counter accepts the lexical form listed in
NEGATION_LEXICON; adding to that list is a reading decision and needs the same
evidence as any verdict. Where a check is still too noisy to be green, its
findings are locked in a baseline below with the reason, so that a NEW hit is red
even while the old ones are still owed a verdict. A baseline may shrink freely.
Growing one needs a row in docs/semantic-audit.md first.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = list(range(1, 19))
LANGUAGES = ("en", "ne", "hi")
GLOSS = {"en": 2, "ne": 3, "hi": 4}   # row index of each language's gloss


def all_verses():
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


# --------------------------------------------------------------- tokenising

def deva_word(word):
    """Python's \\b does not bound Devanagari: न in नियम्य is not the negator."""
    return r"(?<![\u0900-\u097F])" + re.escape(word) + r"(?![\u0900-\u097F])"


EN_WORD = re.compile(r"[A-Za-zāīūṛṝḷṃḥśṣṭḍṇñĀĪŪ’']+")
SENTENCE = re.compile(r"(?<=[.!?])\s+|—|;|:")

EN_STOP = set("""
a an the of to in on at by for with from into onto as than then that this these
those it its his her their our your my me him them us we you they he she i
is are was were be been being am do does did has have had shall will would
can could may might must not no nor or and but so if when where which who whom
whose what how why there here now also even very own same such both each other
others all any some one more most only just yet still again once
""".split())


def deva_tokens(text):
    if not text:
        return []
    return [p for p in re.split(r"[\s,;:!?।“”\"()—–\-.]+", text) if p]


# ------------------------------------------------------------- A: nothing added

# Words the English may use without a row of their own: the syntactic glue of the
# sentence. A person, a place, a scripture or an epithet is not glue.
GLUE = EN_STOP | set("""
lord god gods self one's oneself himself herself itself themselves ourselves
o how nothing none neither without cannot nor
""".split())

def name_key(word):
    """One key for a name however the sentence inflects it: Pāṇḍu / Pāṇḍu's /
    Pāṇḍavas / Pāṇḍavas' fold together by dropping the possessive and a plural
    -s. Diacritics are kept, so Bhīma and Bhīṣma never fold together."""
    key = word.lower().strip("’'")
    key = re.sub(r"’s$|'s$|’$|'$", "", key)
    if key.endswith("s") and len(key) > 3:
        key = key[:-1]
    return key


def capitalised_names(text):
    """Capitalised words that are not sentence-initial and not glue."""
    out = set()
    for sentence in SENTENCE.split(text or ""):
        for word in EN_WORD.findall(sentence)[1:]:
            if word[0].isupper() and word.lower() not in GLUE:
                out.add(word)
    return out


def row_vocabulary(verses, languages):
    """Every name the rows of these verses spell, folded by name_key."""
    return {name_key(w) for verse in verses for row in rows_of(verse)
            for lang in languages for w in EN_WORD.findall(row[GLOSS[lang]])}


# A proper name in an English *literal* that appears in no row of its own verse.
# The literal is the semantic standard, so each of these was read against its
# rows. Every one is reachable from a row under another spelling or a compound
# split across rows; none is a finding. A name NOT in this list is a finding.
LITERAL_NAME_BASELINE = {
    ("1.12", "Bhīṣma"),         # कुरुवृद्धः पितामहः row, "grandsire of the Kurus"
    ("1.20", "Dhārtarāṣṭras"),  # धार्तराष्ट्रान् row
    ("1.20", "Pāṇḍava"),        # कपिध्वजः row: the ape-bannered Pāṇḍava
    ("1.21", "Acyuta"),         # अच्युत row is the same address
    ("1.24", "Gudākeśa"),       # गुडाकेश row
    ("2.02", "Āryan"),          # आर्य row ("noble"); the reading keeps the name
    ("2.42", "Vedas"),          # वेदवादरताः row carries वेद
    ("2.72", "Brāhmī"),         # ब्राह्मी स्थितिः row
    ("8.16", "Kaunteya"),       # कौन्तेय row
    ("10.28", "Kāmadhuk"),      # कामधुक् row, the cow of wishes
    ("10.37", "Uśanā"),         # उशना row
    ("11.35", "Arjuna"),        # अर्जुन row
    ("11.48", "Vedas"),         # वेद row
    ("11.55", "Pāṇḍava"),       # पाण्डव row
}

# A proper name in an English *paraphrase* that is in neither the verse's literal
# nor any row of its whole chapter: the paraphrase explaining by naming. Reported
# to the owner as the "more" list, not rewritten here. A new one is red, and
# clearing one from this set is how it gets fixed.
PARAPHRASE_NAME_BASELINE = {
    ("1.01", "Kurukṣetra"),   # the plain name of the field, for a reader new to it
    ("1.16", "Endless"),      # conch names spelled out one by one from
    ("1.16", "Sweet"),        # अनन्तविजय, सुघोष, मणिपुष्पक
    ("1.16", "Toned"),
    ("1.16", "Jewel"),
    ("1.16", "Blossom"),
    ("1.20", "Hanumān"),      # कपिध्वज "ape-bannered" named in the paraphrase
    ("3.10", "Creator"),      # प्रजापतिः row = "the Lord of creatures"
    ("3.15", "Absolute"),     # ब्रह्म glossed "Brahman" — an interpretive noun
    ("4.01", "King"),         # विवस्वान् row = "Vivasvān"; "king" is a gloss
    ("4.25", "Absolute"),     # as 3.15
    ("8.01", "Kṛṣṇa"),        # the addressee named where the literal keeps "O Lord"
    ("8.11", "Vedic"),        # वेद row
    ("9.20", "Vedic"),        # वेद row
    ("10.23", "Kubera"),      # धनेश row = "the lord of wealth"
    ("10.25", "Himalaya"),    # हिमालय row in the Nepali/Hindi, not the English
    ("10.29", "Ananta"),      # अनन्त row in the Sanskrit word itself
    ("12.01", "Absolute"),    # ब्रह्म — interpretive noun, as 3.15
    ("12.05", "Absolute"),    # as 12.01
    ("13.23", "Person"),      # पुरुष glossed "person"; capitalised by the sentence
    ("13.26", "Arjuna"),      # the literal drops an address the paraphrase keeps
    ("15.18", "Puruṣottama"),  # पुरुषोत्तम row
    ("15.19", "Arjuna"),      # as 13.26
    ("15.20", "Arjuna"),      # as 13.26
    ("16.05", "Arjuna"),      # as 13.26
    ("16.22", "Arjuna"),      # as 13.26
    ("18.13", "Vedānta"),     # वेदान्त row
}


# -------------------------------------------------- B: cross-language lag

def items(text):
    """Clause/item count of a rendering; a dash-bounded list counts item by item."""
    body = (text or "").strip().strip("“”\"' ")
    body = re.sub(r"[—–]", "|", body)
    return len([p for p in re.split(r"[,;:।?!|]", body) if p.strip()])


def end_kind(text):
    body = (text or "").strip().rstrip("”\"’'")
    if not body:
        return "empty"
    if body[-1] in ".!?।":
        return "end"
    if body[-1] in ",;":
        return "comma"
    if body[-1] in "—–-":
        return "dash"
    return "other"


def truncated_lanes(verse, kind):
    """One lane stops mid-phrase, while the same lane's own literal and both
    sibling renderings all end a sentence. That is 12.03 exactly: the Hindi
    paraphrase ended "…कभी न बदलने वाला," where its literal ended
    "…नित्य — की पूजा करते हैं," plus a full stop."""
    bad = []
    for lang in LANGUAGES:
        if end_kind(verse[kind][lang]) not in ("comma", "dash", "other"):
            continue
        siblings = [end_kind(verse[kind][o]) for o in LANGUAGES if o != lang]
        if all(s == "end" for s in siblings) and end_kind(verse["lits"][lang]) == "end":
            bad.append((verse["n"], kind, lang, end_kind(verse[kind][lang])))
    return bad


def item_ratio(verse, lang, kind="paras"):
    literal = items(verse["lits"][lang])
    return items(verse[kind][lang]) / literal if literal else 1.0


# Lag floor: a paraphrase that keeps under this share of its own literal's clause
# items, where both sibling paraphrases keep at least twice as much, is lagging.
LAG_FLOOR = 0.4
# Locked lag findings. Each is a paraphrase that compresses hard on purpose; the
# English lane does this most, because English has no -कर clause chains. Locked so
# a NEW gap is red while these stay a known, reported set. Clearing one from the
# list is how it gets tightened.
LAG_BASELINE = {
    ("2.51", "hi"),   # one long Hindi sentence for three clauses; all content kept
    ("3.06", "en"),   # "keeps the hands idle but lets the mind dwell on pleasures"
    ("3.21", "en"),   # two English sentences for four clauses
    ("3.28", "en"),   # guṇas/actions compressed to one clause
    ("3.31", "en"),
    ("3.35", "en"),
    ("3.36", "en"),
    ("4.31", "en"),
    ("5.05", "en"),   # sāṅkhya/yoga named by their sense, not by the word
    ("5.22", "en"),
    ("6.06", "en"),
    ("8.05", "en"),
    ("10.27", "en"),
    ("10.39", "en"),
    ("11.20", "en"),
    ("18.08", "en"),
    ("18.71", "en"),
}


# ------------------------------------------------------------- C: parity

NE_STANDING = {"न", "नै", "बिना", "रहित", "छैन", "छैनन्", "कहिल्यै", "नहुने",
               "हुन्न", "अभाव", "नपर्ने", "नगरी", "नगरे", "नभई", "नभए", "होइन", "होइनन्"}
NE_SUFFIX = ("दैन", "दैनन्", "दिनँ", "दिनुहुन्न", "एन", "एनन्", "इनँ", "इनन्",
             "्यैन", "छैन", "नहुन्", "नपरोस्", "नहोस्",
             # the second-person and simple-past endings the list above misses:
             # पाउनेछैनौ (2.38), पर्नेछैनौ (4.35), थिएनौ (2.12), लडेनौ (2.33).
             # Each is a one-token closed form, not a stem; all four were read.
             "छैनौ", "एनौ", "ेनौ")
# The closed class of Devanagari negative VERB forms the suffix scan above cannot
# reach. A Nepali negative verb does not carry a negative participle; it changes
# stem and ending (गर्दिनँ, देख्दैनन्, लडेनौ, सक्दैनौ) or is a prohibitive/optative
# with a fused न (नगर, नसोचोस्). Listed whole, token-exact, never as a suffix: a
# `न…` prefix rule was tried and threw 644 false hits (नगरा "kettledrum",
# नमस्कार, नरक, नित्य …), which is why this is a list and not a pattern.
#
# Every entry below occurs in this corpus (700 verses × literal + paraphrase) and
# was read in its sentence before it was listed. The count is deliberately small:
# each form earns its place by clearing a locked baseline pair, and the verse it
# clears is named beside it.
NE_NEG_VERB = {
    "होइन",            # copular negative — "the childish, NOT the wise" (5.04)
    "होइनन्",          # its plural (2.04, 18.40)
    "चाहन्नँ",         # "I do not wish" (1.32, 1.35)
    "सक्दैनौ",         # "you cannot" (11.08, 12.09)
    "जान्दैनौ",        # "you do not know" (4.05)
    "नजान्ने",         # "how should we not know" (1.39)
    "नगर",             # prohibitive "do not do" — शोक नगर (16.05, 18.66)
    "नगरें",           # "if I did not act" (3.24; also 3.23)
    "नगरोस्",          # "let him not unsettle" (3.29)
    "नसोचोस्",         # "let him not think" (6.25)
    "नपारोस्",         # "let him not create" (3.26)
    "नसुन्यौ",         # "if you do not listen" (18.58)
    "नचाहेको",         # "what you do not wish" (18.60)
    "नजाने",           # "a mind that goes nowhere else" (8.08)
    "नडराइकन",         # "without fearing" (11.34)
}
HI_STANDING = {"न", "नहीं", "मत", "बिना", "विना", "बगैर", "रहित", "कभी",
               "कदापि", "अभाव", "निर्"}
EN_NEGATION = re.compile(
    r"\b(not|no|never|nothing|none|neither|nor|without|cannot|nowhere)\b|n’t\b|n't\b",
    re.I)

# Devanagari words whose negation is lexical: the marker lives inside the word, so
# a literal using one negates without a न token. Each was read before it was
# listed; this is a reading decision, not a token trick.
NEGATION_LEXICON = (
    "अचल", "अच्युत", "अक्षर", "अक्षय", "अनन्त", "अनश्वर", "अविनाशी", "अव्यक्त",
    "अनिर्देश्य", "अचिन्त्य", "अनित्य", "असम्भव", "अभय", "अमृत", "असत्", "अनृत",
    "निर्दोष", "निर्भय", "निर्मल", "निराकार", "निरन्तर", "निर्विकार", "निर्विकल्प",
    "निर्लिप्त", "निष्काम", "निष्पाप", "निःसन्देह", "निःशुल्क", "अनासक्त",
)

# Sanskrit rows that carry the negation explicitly (a separate न/मा row). The
# house style puts the negator in its own row, so these are the verses where every
# literal is obliged to negate.
NEGATOR_ROWS = {"न", "मा", "नैव", "न हि", "न च"}

# Sanskrit rows that themselves carry a negated word or privative prefix. Their
# glosses name the negation, and every literal must too — but the token may be
# inside the Devanagari word, so NEGATION_LEXICON is what makes the check fair.
NEGATED_ROWS = set(NEGATION_LEXICON) | {"अपर्याप्त", "अपराध", "अशुभ", "असुर",
                                        "अज्ञान", "अन्धकार", "अमङ्गल"}

# Locked literal-negation findings: verse, language. Every remaining pair was read
# in this pass and the reason it stays is written beside it. A pair whose lane now
# negates is caught by test_every_negation_baseline_row_is_still_real and must be
# dropped, not explained away.
#
# What this list used to hold, and no longer does: seventeen pairs were locked
# only because `negation_count` could not read a Nepali negative VERB (चाहन्नँ
# "I do not wish", नगर "do not", सक्दैनौ "you cannot"). The closed list
# NE_NEG_VERB above now reads those forms token-exactly, and each of the
# seventeen was cleared by reading its three literals. 26 pairs → 6.
NEGATION_BASELINE_ROWS = {
    # English renders न as a lexical negative the counter does not list:
    ("12.07", "en"),   # "I swiftly become the deliverer" — न चिरात् "not after long"
    ("14.23", "en"),   # "unshaken by the guṇas" for न विचाल्यते
    ("16.03", "en"),   # "freedom from malice" for नातिमानिता; ने/हि use -रहितता
    ("16.03", "ne"),   # द्वेषरहितता / अभिमानरहितता: the negation is inside -रहित
    # Hindi renders the same verse's नातिमानिता with a privative अ-
    ("16.03", "hi"),
    ("12.07", "hi"),   # न चिरात् = "शीघ्र ही" — a positive idiom, same clause kept
}

NEGATION_BASELINE_TWO_LANE = {
    ("14.23", "en"),   # "not is shaken" said as "unshaken"/"unconcerned"
}

NUMBER_FORMS = {
    "two": ("दुई", "दुवै", "दो", "दोनों"),
    "three": ("तीन", "तीनों", "तीनै"),
    "four": ("चार",), "five": ("पाँच", "पांच"), "six": ("छह", "छः"),
    "seven": ("सात",), "eight": ("आठ",), "nine": ("नौ",), "ten": ("दस",),
    "twelve": ("बाह्र", "बारह"), "fourteen": ("चौध", "चौदह"),
    "hundred": ("सय", "सौ"),
    "thousand": ("हजार", "हज़ार", "सहस्र", "हजारौं", "हजारों"),
}

# Locked number findings. The defect this rule is built to catch is 16.21's
# "three" (काम, क्रोध, लोभ) going missing; every entry below is instead a
# rendering effect the audit read and accepted, where the number is still
# carried in the language the sentence actually uses:
#   * the numeral lives inside the word the row itself gives (चतुर्भुज "four-armed",
#     अश्विनौ "the two Aśvins" said as अश्विनीकुमार, षण्मासाः "six months")
#   * "of the two" is already implied by a dual/collective the strict numeral
#     forms above do not list (दुवै/दोनों vs दुई/दो).
# A new pair is red; removing a pair is how it gets tightened.
NUMBER_BASELINE = {
    "3.34", "8.24", "8.25", "11.06", "11.46", "13.05", "18.70",
}

# The Devanagari address rules. Two honest limits, both measured, both locked:
#
#  1. A row glosses a word, a literal renders a phrase. भूतेश is हे भूतेश in the
#     row and "देवताका स्वामी" in the Nepali sentence; अप्रतिमप्रभाव is
#     "अतुल प्रभाव भएका" and not the compound. The address is in the literal, the
#     *word* is not — so a strict substring test flags the paraphrase that is
#     right. Those verses are locked here.
#  2. The Nepali rows spell the address in its Sanskrit form (हे परन्तप) while
#     the Nepali literal uses the natural form (शत्रुतापन). Same address, two
#     spellings; also locked.
#
# The rule that found F12-F16 and 3.07 is the English one below, which compares
# the row's own English address, and it is green with an 11-entry baseline of
# rows whose English gloss is a translation rather than an epithet.
VOCATIVE_BASELINE = {
    "1.03", "1.18", "1.24", "2.03", "2.04", "2.09", "2.10", "2.15",
    "3.28", "3.43", "4.02", "4.05", "4.33", "4.35", "6.02", "7.27", "9.03",
    "10.14", "10.15", "10.17", "10.40", "11.25", "11.31", "11.37", "11.40",
    "11.43", "11.46", "11.55", "14.22", "16.05", "18.41",
}

# English addresses whose row's English gloss is a translation rather than an
# epithet ("O infallible one"), so a plain substring test is the wrong test.
EN_VOCATIVE_BASELINE = {
    ("1.21", "अच्युत"), ("2.04", "अरिसूदन"), ("3.28", "बाहो"),
    ("3.41", "ऋषभ"), ("6.43", "कुरुनन्दन"), ("8.16", "कौन्तेय"),
    ("11.37", "जगन्निवास"), ("11.45", "जगन्निवास"), ("11.46", "सहस्रबाहो"),
    ("11.46", "विश्वमूर्ते"), ("11.55", "पाण्डव"),
}

def negation_count(text, lang):
    if lang == "en":
        return len(EN_NEGATION.findall(text or ""))
    total = 0
    for word in re.split(r"[\s,;:!?।“”\"()—–\-’']+", text or ""):
        if not word:
            continue
        if lang == "ne":
            if word in NE_STANDING or word in NE_NEG_VERB or word.endswith(NE_SUFFIX):
                total += 1
        else:
            if word in HI_STANDING or "नहीं" in word:
                total += 1
    for word in NEGATION_LEXICON:
        total += len(re.findall(deva_word(word), text or ""))
    return total


def vocative_rows(verse):
    return [row for row in rows_of(verse) if row[GLOSS["en"]].startswith("O ")]


def fold_deva(text):
    """Fold only the spellings the sources themselves mix."""
    return (text or "").replace("़", "").replace("न्त", "ंत").replace("न्द", "ंद")


def address_survives(core, literal):
    core = fold_deva(core.strip())
    literal = fold_deva(literal)
    if not core or core in literal:
        return True
    for token in deva_tokens(literal):
        if len(core) >= 5 and len(token) >= 5 and (
                token.startswith(core[:-1]) or core.startswith(token[:-1])):
            return True
    return False


class WholeBookFidelity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.verses = all_verses()
        cls.chapters = {}
        for number in CHAPTERS:
            chapter = json.loads((ROOT / "source" / f"ch{number}.json").read_text())
            cls.chapters[number] = [v for theme in chapter["themes"]
                                    for part in theme["parts"] for v in part["sutras"]]

    def test_the_corpus_is_the_whole_book(self):
        self.assertEqual(len(self.verses), 700)
        self.assertEqual(len({v["n"] for v in self.verses}), 700)

    # ---------------------------------------------------------- A: nothing added

    def test_nothing_added_name_in_a_literal_comes_from_the_rows(self):
        """Every proper name an English literal speaks must be reachable from the
        verse's own rows. A literal that names a person, place or scripture the
        Sanskrit does not is adding, however true the statement may be."""
        hits = set()
        for verse in self.verses:
            row_words = row_vocabulary([verse], LANGUAGES)
            for word in capitalised_names(verse["lits"]["en"]):
                if name_key(word) in row_words:
                    continue
                hits.add((verse["n"], word))
        self.assertEqual(sorted(hits - LITERAL_NAME_BASELINE), [],
                         "a literal names something no word row accounts for")

    def test_nothing_added_name_in_a_paraphrase_is_in_the_literal_or_rows(self):
        """The paraphrase may not introduce a name its own literal keeps back.
        This is "no explanatory gloss inside something presenting as literal" in
        its checkable form. Findings are locked and reported, not silently kept."""
        hits = set()
        for verse in self.verses:
            chapter = verse["n"].split(".")[0]
            row_words = row_vocabulary(self.chapters[int(chapter)], LANGUAGES)
            literal = {name_key(w) for w in EN_WORD.findall(verse["lits"]["en"])}
            for word in capitalised_names(verse["paras"]["en"]):
                base = name_key(word)
                if base in literal or base in row_words:
                    continue
                hits.add((verse["n"], word))
        self.assertEqual(sorted(hits - PARAPHRASE_NAME_BASELINE), [],
                         "a paraphrase names something its literal and rows do not")

    def test_the_name_baselines_have_no_stale_rows(self):
        """An allowance must not outlive the string it allowed."""
        for number, word in LITERAL_NAME_BASELINE:
            literal = load_verse(number)["lits"]["en"]
            self.assertIn(name_key(word),
                          {name_key(w) for w in EN_WORD.findall(literal)},
                          f"{number} no longer says {word}")
        for number, word in PARAPHRASE_NAME_BASELINE:
            verse = load_verse(number)
            chapter = int(number.split(".")[0])
            row_words = row_vocabulary(self.chapters[chapter], LANGUAGES)
            literal = {name_key(w) for w in EN_WORD.findall(verse["lits"]["en"])}
            self.assertNotIn(name_key(word), literal)
            self.assertNotIn(name_key(word), row_words)

    def test_every_negation_baseline_row_is_still_real(self):
        """Each locked negation pair must still be a place where the rule fires.
        A stale pair would hide the next dropped negation."""
        for number, lang in NEGATION_BASELINE_ROWS:
            verse = load_verse(number)
            self.assertTrue(any(r[0].strip() in NEGATOR_ROWS for r in rows_of(verse)),
                            f"{number} no longer has a negator row")
            self.assertEqual(negation_count(verse["lits"][lang], lang), 0,
                             f"{number} {lang} now negates; drop the pair")
        for number, lang in NEGATION_BASELINE_TWO_LANE:
            verse = load_verse(number)
            counts = {l: (negation_count(verse["lits"][l], l),
                          negation_count(verse["paras"][l], l)) for l in LANGUAGES}
            self.assertEqual(counts[lang], (0, 0),
                             f"{number} {lang} negates now; drop the pair")
            self.assertTrue(all(min(counts[o]) >= 1 for o in LANGUAGES if o != lang),
                            f"{number} {lang}: a sibling stopped negating")

    def test_every_number_baseline_verse_still_has_a_row_numeral(self):
        for number in NUMBER_BASELINE:
            verse = load_verse(number)
            wanted = set()
            for row in rows_of(verse):
                gloss = row[GLOSS["en"]].lower()
                for word in NUMBER_FORMS:
                    if re.search(r"\b" + word + r"\b", gloss):
                        wanted.add(word)
            self.assertTrue(wanted, f"{number} has no numbered row; drop it")
            still_missing = any(
                not any(form in verse["lits"][lang] for form in NUMBER_FORMS[word])
                for word in wanted for lang in ("ne", "hi"))
            self.assertTrue(still_missing,
                            f"{number} now carries every numeral; drop it")

    def test_every_vocative_baseline_verse_still_has_an_address(self):
        for number in VOCATIVE_BASELINE:
            verse = load_verse(number)
            deva = [row for row in rows_of(verse)
                    for lang in ("ne", "hi") if row[GLOSS[lang]].startswith("हे ")]
            self.assertTrue(deva, f"{number} has no Devanagari address row; drop it")
        for number, sa in EN_VOCATIVE_BASELINE:
            verse = load_verse(number)
            self.assertIn(sa, [row[0] for row in rows_of(verse)],
                          f"{number} no longer carries the address {sa}")

    def test_the_exemptions_do_not_cover_the_names_they_must_not(self):
        """A guard on the baselines themselves: the glossary of the house style
        may not grow into a hole that hides an invented name."""
        self.assertLess(len(LITERAL_NAME_BASELINE), 20)
        self.assertLess(len(PARAPHRASE_NAME_BASELINE), 35)

    # ------------------------------------------------------ B: cross-language lag

    def test_lag_no_lane_stops_mid_phrase_where_siblings_end_a_sentence(self):
        """The 12.03 shape, run over all 700 verses and all three languages."""
        bad = []
        for verse in self.verses:
            for kind in ("lits", "paras"):
                bad.extend(truncated_lanes(verse, kind))
        self.assertEqual(bad, [],
                         "a rendering stops mid-phrase where its siblings do not")

    def test_lag_no_paraphrase_carries_far_less_than_its_literal(self):
        """A paraphrase carrying under LAG_FLOOR of its own literal's clause items,
        where both sibling paraphrases carry at least twice as much, renders less
        than the verse for the same passage."""
        lagging = set()
        for verse in self.verses:
            ratios = {lang: item_ratio(verse, lang) for lang in LANGUAGES}
            for lang in LANGUAGES:
                others = [ratios[o] for o in LANGUAGES if o != lang]
                if ratios[lang] < LAG_FLOOR and min(others) > 2 * ratios[lang]:
                    lagging.add((verse["n"], lang))
        self.assertEqual(sorted(lagging - LAG_BASELINE), [],
                         "one paraphrase is far shorter than its literal and both siblings")

    def test_lag_baseline_entries_are_still_lagging(self):
        """Removing a baseline row is how a paraphrase gets tightened; a stale row
        would hide a real one."""
        for number, lang in LAG_BASELINE:
            verse = load_verse(number)
            ratios = {l: item_ratio(verse, l) for l in LANGUAGES}
            others = [ratios[o] for o in LANGUAGES if o != lang]
            self.assertLess(ratios[lang], min(others),
                            f"{number} {lang} is no longer the short lane")

    # ----------------------------------------------------------------- C: parity

    def test_parity_negation_when_the_sanskrit_negates(self):
        """A verse with an explicit न/मा row must negate in all three literals:
        15.16's dropped negation, stated from the rows instead of from a banned
        reading."""
        missing = set()
        for verse in self.verses:
            rows = rows_of(verse)
            if not any(row[0].strip() in NEGATOR_ROWS for row in rows):
                continue
            for lang in LANGUAGES:
                if negation_count(verse["lits"][lang], lang) == 0:
                    missing.add((verse["n"], lang))
        self.assertEqual(sorted(missing - NEGATION_BASELINE_ROWS), [],
                         "the Sanskrit negates but a literal carries no negation")

    def test_parity_negation_where_two_lanes_negate(self):
        """When the Sanskrit row itself is a negator (न/मा/नैव) and both siblings
        negate in both their literal and their paraphrase, the third lane negating
        in neither has dropped the negation.

        The negator-row condition is what makes this a fidelity rule instead of a
        search for negative particles: without it, 15 verses flag where English
        merely lacks a "not" that Nepali happens to spell with a negative verb.
        With it the rule has six hits, all read, all a negation the language
        carries by other means."""
        missing = set()
        for verse in self.verses:
            if not any(row[0].strip() in NEGATOR_ROWS for row in rows_of(verse)):
                continue
            counts = {lang: (negation_count(verse["lits"][lang], lang),
                             negation_count(verse["paras"][lang], lang))
                      for lang in LANGUAGES}
            for lang in LANGUAGES:
                others = [counts[o] for o in LANGUAGES if o != lang]
                if counts[lang] == (0, 0) and all(min(o) >= 1 for o in others):
                    missing.add((verse["n"], lang))
        self.assertEqual(sorted(missing - NEGATION_BASELINE_TWO_LANE), [],
                         "one language negates nowhere while both others negate twice")

    def test_parity_numbers_in_the_literals(self):
        """A row that glosses a number obliges both Devanagari literals to carry
        that number. A paraphrase may compress it; a literal may not lose it.

        The unit is the verse, not the row: a verse may word the same number in two
        rows (सेनयोः "of the two armies" and उभयोः "of both"), and one rendering of
        "two" satisfies both."""
        missing = set()
        for verse in self.verses:
            wanted = set()
            for row in rows_of(verse):
                gloss = row[GLOSS["en"]].lower()
                for word in NUMBER_FORMS:
                    if re.search(r"\b" + word + r"\b", gloss) and not (
                            "one's" in gloss or "one who" in gloss or "no one" in gloss):
                        wanted.add(word)
            for word in wanted:
                for lang in ("ne", "hi"):
                    if not any(form in verse["lits"][lang] for form in NUMBER_FORMS[word]):
                        missing.add(verse["n"])
        self.assertEqual(sorted(missing - NUMBER_BASELINE), [],
                         "a number the row glosses is absent from a literal")

    def test_parity_every_english_vocative_row_reaches_the_literal(self):
        """F12-F16 as a live rule: an "O X" row must have its X in the English
        literal. Driven from rows, so 3.07's avagraha cannot hide its address."""
        missing = set()
        for verse in self.verses:
            literal = verse["lits"]["en"].lower()
            for row in vocative_rows(verse):
                core = re.sub(r"\s*\([^)]*\)", "", row[GLOSS["en"]])[2:].strip()
                if core and core.lower() not in literal:
                    missing.add((verse["n"], row[0]))
        self.assertEqual(sorted(missing - EN_VOCATIVE_BASELINE), [],
                         "an English address row is missing from its literal")

    def test_parity_every_devanagari_vocative_row_reaches_the_literal(self):
        """The same rule in ne/hi, against the row's own address rather than the
        Sanskrit stem: भूतेश is rendered प्राणीका स्रोत in the Nepali row."""
        missing = set()
        for verse in self.verses:
            for row in rows_of(verse):
                for lang in ("ne", "hi"):
                    gloss = row[GLOSS[lang]]
                    if not gloss.startswith("हे "):
                        continue
                    if not address_survives(gloss[3:], verse["lits"][lang]):
                        missing.add(verse["n"])
        self.assertEqual(sorted(missing - VOCATIVE_BASELINE), [],
                         "an address the row carries is missing from the literal")

    def test_the_vocative_rules_cannot_pass_vacuously(self):
        """If the rows stopped marking addresses, both vocative rules would pass
        while checking nothing."""
        addresses = [(verse["n"], row[0]) for verse in self.verses
                     for row in vocative_rows(verse)]
        self.assertGreaterEqual(len(addresses), 130)
        self.assertIn(("3.07", "अर्जुन"), addresses)
        self.assertNotIn("अर्जुन", load_verse("3.07")["d"])
        deva = [(verse["n"], lang) for verse in self.verses for row in rows_of(verse)
                for lang in ("ne", "hi") if row[GLOSS[lang]].startswith("हे ")]
        self.assertGreaterEqual(len(deva), 200)


if __name__ == "__main__":
    unittest.main()
