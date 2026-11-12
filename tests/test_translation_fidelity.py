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
import collections
import json
import re
import unicodedata
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
    ("6.44", "Vedic"),        # वेद row (chapter 6 has none); शब्दब्रह्म is the
                              # word-Brahman, and "the Vedic word" names it plainly
}


# ------------------------------------------------- D: term substitution (data)
#
# `term (explanation)` exemptions — read on 2026-11-12, each against its verse.
# None of them substitutes a doctrinal word for a gloss of it; the parenthesis
# there is a name-pair or an additive note, which is what the entry says.
TERM_PAIR_EXEMPT = {
    # a name and the name it glosses: the literal uses one of the two, and
    # neither is a claim the verse does not make. Recompute with
    # python3 -m unittest and add a reading here — never a regex.
    ("1.15", "वृकोदरः"),   # "Vṛkodara (Bhīma)" — the literal says Bhīma
    ("1.20", "पाण्डवः"),   # "the son of Pāṇḍu (Arjuna)" — the literal says "the
                            # Pāṇḍava", the verse's own word; naming Arjuna is a
                            # reader's help, not the verse's claim
    ("2.09", "गुडाकेशः"),  # "Guḍākeśa (Arjuna)" — the literal says Guḍākeśa
    ("3.05", "प्रकृति"),   # "of nature (prakṛti)" — the literal says prakṛti
    ("3.10", "पतिः"),      # "the Lord (Prajāpati)" — the literal says Prajāpati
    ("15.01", "अश्वत्थम्"),  # "the sacred fig (world-tree)" — the literal says aśvattha
    # a fragment row: the word is सुहृद् split across two rows and the literal
    # says "well-wishers", the second half
    ("1.27", "हृदः"),
    # "(repeated: each his own)" — the second पृथक् row carries a note on the
    # repetition; the literal says "each his own", the note's content
    ("1.18", "पृथक्"),
}

# An explanation that describes the text rather than explaining the word: a note
# to the reader, so the literal is not required to echo it. Read 2026-11-12.
TERM_NOTE_NOT_EXPLANATION = {
    ("1.18", "पृथक्"),    # "(repeated: each his own)" — a note on the repetition
    ("1.20", "पाण्डवः"),  # "(Arjuna)" — the literal keeps "the Pāṇḍava"
    ("15.01", "अश्वत्थम्"),  # "(world-tree)" — a name for the tree; the literal
                              # keeps aśvattha, the verse's own word
}

# A row whose term the literal omits because the literal is rendering the
# Sanskrit's own compound: अनार्यजुष्टम् is "practised by the un-Āryan", and the
# English literal reads "unworthy of an Āryan" — जुष्टम् ("resorted to, practised
# by") is carried by "unworthy of", not by a separate word. The Nepali and Hindi
# carry it twice over (आर्य-अयोग्य / अनार्य-अयोग्य, अभ्यास गरिएको / सेवित); the
# English is the one that compresses, and its compression was read here.
TERM_IN_COMPOUND = {("2.02", "जुष्टम्")}

# Rows whose own head gloss the English literal does not carry, measured over all
# 9,389 rows on 2026-11-12. Every one was read as synonymy (see the census test);
# the exact number is pinned so any rewrite that moves it is red and has to be
# read. It may fall as the house normalises a gloss, never rise silently.
ROW_LITERAL_CENSUS = 1022


def _fold_diacritics(word):
    """`Guḍākeśa` and `Gudākeśa` fold together; `Bhīma` and `Bhīṣma` do not."""
    folded = unicodedata.normalize("NFD", word.lower())
    return "".join(ch for ch in folded if not unicodedata.combining(ch))


SKT_CASE_ENDINGS = ("bhyām", "bhyas", "bhyaḥ", "ānām", "eṣu", "asya", "āya",
                    "ena", "āt", "āḥ", "aiḥ", "oḥ", "ām", "au", "ī", "ū", "ā",
                    "aḥ", "am", "as", "e", "i", "u", "a")


def _sanskrit_head(iast):
    """One key per Sanskrit word across its case forms: the stem with the ending
    stripped. Deliberately crude — a long ending is tried before a short one, and
    a stem shorter than three characters is left whole."""
    word = (iast or "").strip().replace("’", "'")
    for ending in SKT_CASE_ENDINGS:
        if word.endswith(ending) and len(word) - len(ending) >= 3:
            return word[:-len(ending)]
    return word


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

    def test_nothing_added_no_lane_asserts_selfishness_the_sanskrit_lacks(self):
        """The owner's ruling, 2026-11-12: "we cannot add anything that's not
        there in the sanskrit."

        सङ्कल्प is resolve/planning — Śaṅkara: "expectation, anticipation, of
        results"; Sivananda: "the imagining faculty … that makes plans for the
        future". It is never *selfishness*, which no Sanskrit word in 6.02,
        4.19, 6.04, 6.24, 12.16 or 14.25 states. सर्वारम्भ is "undertakings",
        not "selfish undertakings". The old house gloss asserted the motive
        anyway; eighteen strings were corrected.

        The check that found the remaining four was this rule's own class
        sweep, not a reading of those verses: 3.15 निःस्वार्थ for a verse with
        no काम, and निःस्वार्थ / "selfish" added to the bare कर्मयोग of 3.03,
        5.02 and 13.24. Paraphrases of verses that DO say काम keep the sense
        (3.09 names the alternative to यज्ञ; 18.02 काम्यानाम्); the short
        exemptions below are exactly those, listed so a later pass does not
        delete a reading the Sanskrit supports."""
        # Paraphrases whose Sanskrit names desire outright, so the paraphrase may.
        kama_allowed = {("3.09", "en"), ("3.09", "ne"), ("3.09", "hi")}
        hits = set()
        for verse in self.verses:
            for kind in ("lits", "paras"):
                for language in LANGUAGES:
                    text = verse[kind][language]
                    if ("selfish" in text) if language == "en" else ("स्वार्थ" in text):
                        hits.add((verse["n"], language))
        self.assertEqual(sorted(hits - kama_allowed), [],
                         "a lane asserts a selfish motive no word of the verse states")
        for number, language in sorted(kama_allowed):
            # 3.09 is the one verse where the paraphrase's contrast is the
            # Sanskrit's own: "except action for the sake of sacrifice" says the
            # alternative is desire-led action, and काम appears in no row of it,
            # so the exemption is the यज्ञ row plus a reading, not a token.
            self.assertIn("यज्ञ", [r[0] for r in rows_of(load_verse(number))])
        # one consistent house gloss for सङ्कल्प, and the rows carry no motive
        for number in ("6.02", "4.19", "6.04", "6.24"):
            for row in rows_of(load_verse(number)):
                if row[0].startswith("सङ्कल्प"):
                    self.assertNotIn("selfish", row[2],
                                     f"{number} {row[0]} still glosses the motive")
        self.assertEqual([r[2] for r in rows_of(load_verse("4.19"))
                          if r[0] == "सङ्कल्प"], ["resolve"])
    def test_no_lane_is_written_in_the_other_language(self):
        """A real defect caught by eye, not by a check: 6.44's Hindi paraphrase
        was written in Nepali (`ऊ … अघि बढ्छ … पुग्छ`) while claiming the hi lane.
        It passed every gate — the overlap was 0.491 because a Nepali sentence
        shares little with a Hindi literal — and only the before/after dump for
        the commit message exposed it.

        The markers below are function words that are native to one language and
        do not occur in the other's Gītā register. Verified at zero hits across
        all 700 verses x 2 lanes x 2 languages before being pinned. They are a
        contamination net, not a language model: a short lane with no marker
        could still be wrong, and this test cannot see that."""
        nepali_markers = ("छ", "छन्", "हरू", "तिमी", "भए", "भयो", "गर्छ", "गर्नु",
                          "कोही", "उसले", "हुँदैन", "भन्नुभयो", "गरेर", "गर्दै",
                          "छैन", "सक्दैन", "हुँदै", "पर्छ", "दिन्छ", "भन्छ")
        hindi_markers = ("है", "हैं", "नहीं", "वाला", "वाले", "किन्तु", "हुआ",
                         "हुई", "गया", "गई", "था", "थी", "जिस", "उसी", "मुझे",
                         "करता", "करते", "होता", "होते", "और", "भी")

        def occurs(text, word):
            return re.search(r"(?<![\u0900-\u097F])" + re.escape(word) +
                             r"(?![\u0900-\u097F])", text) is not None

        for verse in self.verses:
            for kind in ("lits", "paras"):
                for word in nepali_markers:
                    self.assertFalse(occurs(verse[kind]["hi"], word),
                                     f"{verse['n']} {kind}.hi looks Nepali: {word}")
                for word in hindi_markers:
                    self.assertFalse(occurs(verse[kind]["ne"], word),
                                     f"{verse['n']} {kind}.ne looks Hindi: {word}")



    # ------------------------------------------------------ D: term substitution
    #
    # The class the semantic audit named and left open: a literal that replaces
    # the word its own row glosses with a different one. It carries no name, no
    # number and no negator, so every check above passes it. Both defects the
    # 2026-11-12 reading found belong here —
    #
    #   4.32  ब्रह्मणः  "of Brahman (the Vedas)"    -> literal "the scriptures"
    #   6.44  शब्दब्रह्म "the word-Brahman (Vedas)"  -> literal "the mere word of the Vedas"
    #
    # — and neither a token scan of the glosses nor a stemmed alignment recovers
    # them: "scripture" and "Veda" are both in the house vocabulary elsewhere, so
    # a book-wide vocabulary test licenses the very substitution it should catch.
    # What does recover them is the house's own mark of a *term*: a parenthetical.

    def test_a_gloss_term_with_an_explanation_reaches_its_literal(self):
        """A row gloss shaped `term (explanation)` names a term and explains it.

        The literal must carry the term. Carrying only the explanation is the
        4.32/6.44 defect: the translation has quietly swapped the word for a
        gloss of it. This rule is true of both known defects retrospectively
        ("of Brahman (the Vedas)" -> "the scriptures"; "the word-Brahman (Vedas)"
        -> "the mere word of the Vedas").

        **What it cannot see.** Only 68 of the 9,389 rows carry a parenthetical.
        A row glossed with a bare synonym — "duty" for धर्म, "nature" for
        प्रकृति — leaves no term mark and is invisible here. This check is a
        floor under the substitution class, not a proof of fidelity.
        """
        hits = []
        for verse in self.verses:
            for row in rows_of(verse):
                match = PARENTHETICAL.match(row[2] or "")
                if not match:
                    continue
                term = _en_gloss_stems(match.group(1))
                if not term:
                    continue
                if not _literal_has_any(verse["lits"]["en"], term):
                    hits.append((verse["n"], row[0], row[2]))
        # Each entry below was read against its verse on 2026-11-12. Every one is
        # a name-pair or an additive note, not a substitution of a doctrinal term;
        # the reason is in TERM_PAIR_EXEMPT so a new kind of hit is red.
        exempt = TERM_PAIR_EXEMPT | TERM_IN_COMPOUND
        self.assertEqual([h for h in hits if h[:2] not in exempt], [],
                         "a literal drops the term its own row glosses")

    def test_every_term_pair_exemption_is_still_a_real_pair(self):
        """The exemptions are read, not assumed: the row must still be shaped
        `term (explanation)` and the literal must still name the one the gloss
        explains — the pair itself, not the term the check wants."""
        for number, deva in sorted(TERM_PAIR_EXEMPT):
            verse = load_verse(number)
            rows = [r for r in rows_of(verse) if r[0] == deva]
            self.assertTrue(rows, f"{number} {deva} is no longer a row")
            gloss = rows[-1][2]
            match = PARENTHETICAL.match(gloss or "")
            self.assertIsNotNone(match, f"{number} {deva} lost its parenthetical")
            if (number, deva) in TERM_NOTE_NOT_EXPLANATION:
                continue
            # The exemption's own claim: the literal uses one of the pair.
            pair = _en_gloss_stems(match.group(1)) | _en_gloss_stems(match.group(2))
            self.assertTrue(_literal_has_any(verse["lits"]["en"], pair),
                            f"{number} {deva}: the literal uses neither half of the pair")

    def test_a_name_is_spelled_the_way_the_verses_rows_spell_it(self):
        """`Gudākeśa` in 1.24 against `Guḍākeśa` in that verse's own row and in
        three other verses (2.09, 10.20, 11.07). Devanagari गुडाकेश has the
        retroflex ḍ, so the row is right and 1.24's literal dropped it.

        The comparison is name-against-gloss, not name-against-IAST: a row's
        IAST is inflected (`guḍākeśena`, `guḍākeśaḥ`) while a literal's name is
        nominative, so the only fair check is whether the house writes *this*
        name this way anywhere in its own glosses. A spelling the glosses use is
        licensed; a respelling they never use is the finding.

        Deliberately narrow. It cannot see a name the rows never gloss in
        English (the whole of an addressee's IAST may be a bare word), it says
        nothing about whether the name is the right one, and case differences
        alone are the house's convention (`Kaunteya` in a literal, `kaunteya`
        in a gloss) rather than a disagreement. `Bharata` for भारत is licensed
        because the row that glosses it already writes "Bharata", and `Brāhmī`
        because `brāhmī` has no retroflex to lose — ṛ is inherent in ब्राह्मी.
        """
        # folded gloss spelling -> the exact spellings the house uses
        house = collections.defaultdict(set)
        for verse in self.verses:
            for row in rows_of(verse):
                for word in EN_WORD.findall(row[2] or ""):
                    if word[:1].isupper():
                        house[_fold_diacritics(word)].add(word)
        hits = []
        for verse in self.verses:
            local = collections.defaultdict(set)
            for row in rows_of(verse):
                for word in EN_WORD.findall(row[2] or ""):
                    if word[:1].isupper():
                        local[_fold_diacritics(word)].add(word)
            if not local:
                continue
            for word in EN_WORD.findall(verse["lits"]["en"]):
                word = word.strip("’'")
                if len(word) < 4 or not word[:1].isupper():
                    continue
                if word.lower() in EN_STOP or word in GLUE:
                    continue
                spellings = local.get(_fold_diacritics(word))
                if spellings and word not in spellings:
                    hits.append((verse["n"], word, sorted(spellings)))
        # 1.24 `Gudākeśa` was this check's only finding; it is corrected and a
        # revert is red, because the old spelling is not in the house's glosses.
        self.assertEqual(hits, [],
                         "a name is spelled differently from its own gloss")

    def test_the_one_two_four_literal_spells_gudakesa_with_the_retroflex(self):
        """1.24. The row is `guḍākeśena` and its gloss "by Guḍākeśa"; 2.09, 10.20
        and 11.07 spell the same name the same way. Devanagari गुडाकेश is
        retroflex ḍ, so the literal's `Gudākeśa` was the only dental spelling in
        the book — a letter short, not a different name. Pinned in all four lanes
        the name reaches."""
        verse = load_verse("1.24")
        self.assertIn("Guḍākeśa", verse["lits"]["en"])
        self.assertNotIn("Gudākeśa", verse["lits"]["en"])
        self.assertIn("गुडाकेश", verse["lits"]["ne"])
        self.assertIn("गुडाकेश", verse["lits"]["hi"])
        self.assertEqual([r[2] for r in rows_of(verse) if r[1] == "guḍākeśena"],
                         ["by Guḍākeśa (Arjuna)"])
        # and the spelling the rest of the book uses is the one now in 1.24
        for number in ("2.09", "10.20", "11.07"):
            rows = [r for r in rows_of(load_verse(number)) if "guḍākeś" in r[1]]
            self.assertTrue(rows, number)
            self.assertTrue(any("Guḍākeśa" in r[2] for r in rows), number)

    def test_the_row_to_literal_substitution_census_is_measured(self):
        """The census behind this class, kept honest and kept visible.

        For every row, does the English literal carry the row's own (bare) head
        gloss — or a head gloss the same Sanskrit word carries anywhere in the
        book? On 2026-11-12 that was **1,022 rows in 515 verses** that carry
        neither. All 1,022 are synonymy, not substitution: the literal renders
        दृष्ट्वा "having seen" as "seeing", युयुत्सवः "desiring to fight" as
        "eager for battle", अभिरक्षितम् "protected" as "guarded". None of them
        was edited, and none can be found by this rule — which is why the
        census is asserted as a *measured ceiling* rather than as zero.

        The check that does find substitution is the parenthetical one above:
        the house's own marker that a gloss is `term (explanation)`.

        **What this cannot see.** Everything a synonym can hide. If a literal
        swaps a word for a near-synonym the rows never pair it with, this number
        does not move and the parenthetical rule does not fire. That is exactly
        why the per-verse ledger, not this file, remains the fidelity record.
        """
        census = 0
        for verse in self.verses:
            carried = set()
            for word in EN_WORD.findall(verse["lits"]["en"]):
                carried |= _fold_en(word.lower().strip("’'"))
            for row in rows_of(verse):
                head = _en_gloss_stems(_row_term(row[2]))
                if not head:
                    continue
                if carried & head:
                    continue
                census += 1
        self.assertEqual(census, ROW_LITERAL_CENSUS,
                         "the row-to-literal substitution census moved; read the "
                         "new rows before changing this number")

if __name__ == "__main__":
    unittest.main()


# ------------------------- D: the term a gloss names, carried into the literal
#
# The class these four checks cover was the last mechanical hole the semantic
# audit named: a literal that *substitutes* the word its own row glosses. It uses
# no name, number or negator, so every other check in this file and in
# test_semantic_audit.py passed it. Both defects the 2026-11-12 sweep found by
# eye belong to it:
#
#   4.32  ब्रह्मणः  row "of Brahman (the Vedas)"
#                   literal "the scriptures"            — the gloss replaced its headword
#   6.44  शब्दब्रह्म row "the word-Brahman (Vedas)"
#                   literal "the mere word of the Vedas" — same substitution
#
# **What these checks can see.** A row whose gloss carries a parenthetical is a
# *term plus explanation* — the house's own mark for "this is the word, this is
# what it means". The literal must carry the term; carrying only the explanation
# is the defect. Retrospectively, that rule is true of 4.32 and 6.44.
#
# **What they cannot see.** A row glossed with a bare synonym ("duty" for धर्म)
# is invisible: nothing here knows that "duty" and "righteousness" are the same
# Sanskrit word, and the house uses both. A substitution expressed through a
# synonym pair the rows never record leaves no trace. Nothing here reads a verb,
# a case relation or a tense. This is a floor on substitution, not a proof of
# fidelity — the per-verse ledger is still the record.

PARENTHETICAL = re.compile(r"^(.*?)\s*\(([^)]*)\)\s*$")


def _en_gloss_stems(gloss_text):
    """Content-word stems of an English gloss."""
    out = set()
    for word in EN_WORD.findall(gloss_text or ""):
        low = word.lower().strip("’'")
        if low in EN_STOP or low in EN_NUMBER_WORDS:
            continue
        if len(low) <= 1:
            continue
        out.add(_en_stem(low))
    return out


# The numbers the book spells in words; a numeral is a class check of its own
# (test_parity_numbers_in_the_literals), so they are not "content" here.
EN_NUMBER_WORDS = set("""one two three four five six seven eight nine ten eleven
twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty
thirty forty fifty sixty seventy eighty ninety hundred thousand million
first second third fourth fifth sixth seventh eighth ninth tenth eleventh
twelfth half twice once""".split())

_EN_SUFFIX = ("ations", "ation", "ments", "ment", "nesses", "ness", "ingly", "ings",
              "ing", "ies", "ied", "ed", "es", "ly", "er", "ers", "est", "al",
              "ic", "ous", "ive", "ful", "less", "able", "ible", "ance", "ence",
              "ity", "ties", "s")


def _en_stem(word):
    """A small suffix stripper, not a stemmer.

    It is deliberately conservative: a stem that is too short merges unrelated
    words (guṇas/guṇa is wanted; "self"/"selves" is not). Where it under-strips,
    the effect is a duplicate hit, which the census read; where it over-strips,
    it could hide a substitution, so the minimum base is four characters.
    """
    for suffix in _EN_SUFFIX:
        if not word.endswith(suffix) or word.endswith(("ss", "ee", "ll")):
            continue
        base = word[:-len(suffix)]
        if len(base) >= 4:
            return base + ("y" if suffix in ("ies", "ied") else "")
    return word


def _fold_en(word):
    stems = {_en_stem(word)}
    stems |= {s[:-1] for s in list(stems) if len(s) > 4 and s.endswith("e")}
    return stems


def _loan_key(word):
    """One key for a Sanskrit loanword however the house writes it in English.

    `rajas` / `rajo` / `raja` fold together; so do `guṇa` / `guṇas` / `sattva` /
    `sattvic`, `veda` / `Vedas`, `prakṛti` / `prakṛtiḥ`. The fold is a consonant
    skeleton: diacritics off, the English suffix stripped, then the trailing
    vowel or sibilant off. It is deliberately narrow — `Bhīma` and `Bhīṣma` keep
    their different consonants, `Kaunteya` and `Kuntī` stay different words —
    because a fold wide enough to merge those would license any substitution.
    """
    stripped = _fold_diacritics(word).replace("ṃ", "m").replace("ḥ", "h")
    skeleton = _en_stem(stripped)
    return skeleton.rstrip("aeiouāīūsh").replace("ṃ", "m") or skeleton


def _literal_has_any(literal, words):
    """True when the literal carries one of these words, folded two ways: the
    English stem, and the loanword skeleton the glosses themselves use."""
    carried = set()
    for word in EN_WORD.findall(literal or ""):
        low = word.lower().strip("’'")
        carried |= _fold_en(low)
        carried.add(_loan_key(low))
    for stem in words:
        if stem in carried or _loan_key(stem) in carried:
            return True
    return False


# A row gloss's *head* is the words before its parenthetical; the parenthetical
# is the house explaining the term, not a second way to say it.
def _row_term(gloss):
    match = PARENTHETICAL.match(gloss or "")
    return (match.group(1) if match else gloss).strip()
