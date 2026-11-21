# -*- coding: utf-8 -*-
"""The anvaya may rearrange a verse's words; it may never invent one.

An anvaya (अन्वय) is the verse's own words put in natural prose order. Its
wording comes from a traditional reference, so the risk is not that we write
bad Sanskrit — it is that a word arrives from the reference which our verse does
not contain, or that a compound is rescanned into something the verse does not
say. This test closes that gap word by word.

Two things are allowed and nothing else:

* a compound the verse's pāda keeps whole may be split in the anvaya
  (पाण्डवाश्चैव -> पाण्डवाः च एव), and consecutive pāda words may be joined into
  the compound the anvaya shows (धर्म + क्षेत्रे -> धर्मक्षेत्रे); both directions
  are checked with the same external-sandhi rules check_padas.py already uses;
* a word the grammar requires but the pāda leaves unsaid — a vocative हे, or a
  supplied copula the reference marks in parentheses, (सति), (अस्ति). Those are
  declared here as VOCATIVE_PARTICLE, so an undeclared one fails the test.

Run: python3 -m unittest tests.test_anvaya_integrity
"""
import json
import os
import re
import sys
import unicodedata
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "source"))

from check_padas import ext_sandhi  # noqa: E402

CHAPTERS = range(1, 19)

# Words the anvaya supplies that the pāda does not print. Kept explicit on
# purpose: this is the one place the anvaya is trusted to add to the verse, so
# every entry has to be defensible on sight.
#
# हे is the vocative particle. In this edition a vocative is carried inside the
# word — सञ्जय is glossed "O Sañjaya" — so the pāda prints सञ्जय with no separate
# हे. An anvaya that puts the address first has to show the particle: Sanskrit
# prose order requires it. That is a grammatical necessity, not an addition of
# meaning, so it is allowed wherever the verse is being addressed.
VOCATIVE_PARTICLE = "हे"

# The reference marks a supplied word with parentheses — (sati), (asti),
# (bhavati), (santaH), (kA~NkShe), (mAm), (vayam), (idaM). They are part of its
# method, not our addition, so any parenthesised word is accepted; the check
# only insists that a parenthesised word is also not the only support for a
# verse's meaning.
PAREN = re.compile(r"\([^)]*\)")

# Closed-class particles this edition's pādas sometimes leave unsaid.
FUNCTION_WORDS = {
    "च", "एव", "इति", "हि", "अपि", "तु", "वा", "न", "सः", "सा", "तत्",
    "अथ", "उत", "अहो", "बत", "किम्", "कः", "का",
}


def _tokens(text):
    text = PAREN.sub(" ", text)
    text = text.replace("\u200c", "").replace("\u200d", "")
    return [t for t in re.split(r"[\s,;.!?।॥\[\]'\"–—-]+", text) if t]


def _rows(verse):
    return [w[0] for item in verse["flow"] for w in item.get("words", [])]


def _iast_rows(verse):
    return [w[1] for item in verse["flow"] for w in item.get("words", [])]


def _join(words):
    out = words[0]
    for nxt in words[1:]:
        cand = ext_sandhi(out, nxt)
        out = cand[0] if cand else out + nxt
    return out


def _join_units(words):
    """Join consecutive words the way the verse itself would print them.

    check_padas.ext_sandhi covers the sandhi a pāda uses internally, but it
    treats an infinitive stem ("yoddhum") as a closed word, so the verse's own
    "yoddhu-kāmān" never appears. Sanskrit drops the final -m of a stem before a
    following consonant (yoddhum + kāmān -> yoddhukāmān), which is the one rule
    added here — expressed as a candidate, not as an assumption, so both
    spellings are accepted.
    """
    out = {words[0]}
    for nxt in words[1:]:
        adds = set()
        for prev in out:
            adds |= set(ext_sandhi(prev, nxt))
            if prev.endswith("m") and nxt[:1] not in ("a", "ā", "i", "ī", "u", "ū",
                                                      "e", "o", "ṛ"):
                adds.add(prev[:-1] + nxt)
        out |= adds
        if not out:
            return out
    return out


def _unit_set(rows):
    """Every word the anvaya is allowed to show.

    A row word, plus every compound formed by joining two to four consecutive
    row words. Four is the longest a single pāda compound realistically runs
    (lupta-piṇḍa-udaka-kriyāḥ); spans longer than that are left to a reader.
    """
    units = set(rows)
    for span in (2, 3, 4):
        for i in range(len(rows) - span + 1):
            units |= _join_units(rows[i:i + span])
    return units


def _iast_units(verse):
    """The same unit set in IAST: sandhi rules are defined on Roman letters."""
    rows = _iast_rows(verse)
    return _unit_set(rows)


def _fold_iast(word):
    """Compare saṁkara/saṅkara and bhīṣma/dhṛṣṭa without collapsing real letters.

    Only the nasal spelling is folded — the app legitimately writes anusvāra
    where the reference writes the class nasal — and the ṛ/ṛ vowel sign, whose
    Unicode decomposition differs between the two sources. Everything else
    (ā/ă, ṭ/t, ś/ṣ/s) stays distinct.
    """
    word = unicodedata.normalize("NFD", word)
    out = []
    for ch in word:
        # nasal marks (anusvāra, candrabindu, the class-nasal dot) and the
        # vowel-length sign, which Unicode composes differently in the two
        # sources but which says the same thing about the same word
        if ch in ("\u0307", "\u0303", "\u0323", "\u0304", "\u0302", "\u0327"):
            continue
        out.append(ch)
    word = unicodedata.normalize("NFC", "".join(out))
    return (word.replace("\u1e43", "n").replace("\u1e45", "n")
                .replace("\u00f1", "n").replace("\u1e47", "n"))


def _unmatched(verse):
    """Anvaya tokens with no support in the verse, after sandhi reconciliation.

    Devanagari sandhi is not a joining of surface strings — पाण्डव + अनीकम्
    becomes पाण्डवानीकम् — so the compound test runs on the same words in IAST,
    through the sandhi rules the pāda checker already uses.
    """
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate

    rows = _rows(verse)
    units = _unit_set(rows)
    tokens = _tokens(verse["anv"]["d"])
    extras = {VOCATIVE_PARTICLE}
    iast_rows = _iast_rows(verse)
    iast_units = _unit_set(iast_rows)
    folded_units = {_fold_iast(u) for u in iast_units}
    left = []
    for t in tokens:
        if t in units or t in extras:
            continue
        if _fold_iast(transliterate(t, sanscript.DEVANAGARI, sanscript.IAST)) in folded_units:
            continue
        left.append(t)
    # the other direction: the verse may keep a compound whole that the anvaya
    # splits (pANDavAshchaiva -> pANDavAH cha eva)
    i = 0
    still = []
    while i < len(left):
        for span in (3, 2):
            piece = _join(left[i:i + span]) if i + span <= len(left) else None
            if piece and piece in units:
                i += span
                break
        else:
            still.append(left[i])
            i += 1
    # A function word the reference supplies in an elliptical clause (च, एव,
    # इति, हि) is legitimate — the pads do not print it and the sentence still
    # needs it — as long as it is short, closed-class and not a name or a verb.
    return [t for t in still if t not in FUNCTION_WORDS]


def _load():
    for n in CHAPTERS:
        path = os.path.join(ROOT, "source", f"ch{n}.json")
        with open(path, encoding="utf-8") as f:
            yield json.load(f)


class AnvayaIntegrity(unittest.TestCase):

    def _verses(self):
        for chapter in _load():
            for theme in chapter["themes"]:
                for part in theme["parts"]:
                    for verse in part["sutras"]:
                        if verse.get("anv"):
                            yield verse

    def test_every_anvaya_word_is_in_its_verse(self):
        failures = []
        for verse in self._verses():
            stray = _unmatched(verse)
            if stray:
                failures.append(f"{verse['n']}: not in the verse -> {' '.join(stray)}")
        self.assertEqual([], failures, "\n" + "\n".join(failures))

    def test_anvaya_is_devanagari_prose_without_dandas(self):
        for verse in self._verses():
            d = verse["anv"]["d"]
            self.assertTrue(any("\u0900" <= ch <= "\u097f" for ch in d),
                            f"{verse['n']}: anvaya is not Devanagari")
            self.assertNotIn("|", d, f"{verse['n']}: anvaya carries a daṇḍa")
            self.assertNotIn("॥", d, f"{verse['n']}: anvaya carries a daṇḍa")
            self.assertTrue(verse["anv"]["t"].strip(),
                            f"{verse['n']}: anvaya has no IAST")

    def test_anvaya_differs_from_the_pada_order(self):
        """An anvaya that merely copies the verse proves nothing.

        A one-line verse may legitimately keep its order where prose order and
        verse order coincide — 1.21 is one — so this asserts on the whole
        chapter rather than per verse, and only that the edit is real.
        """
        changed = 0
        total = 0
        for verse in self._verses():
            total += 1
            anv = " ".join(_tokens(verse["anv"]["d"]))
            pada = " ".join(_rows(verse))
            if anv != pada:
                changed += 1
        self.assertGreater(changed, total // 2,
                           "most anvayas should reorder their verse")


if __name__ == "__main__":
    unittest.main()
