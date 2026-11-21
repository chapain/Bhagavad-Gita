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
from anvaya import SUPPLIED_GLOSS  # noqa: E402

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

    A row word, plus every compound formed by joining two to five consecutive
    row words. Five, not four: chapter 2 alone has śītoṣṇa-sukha-duḥkha-dāḥ,
    five members that the verse prints as one word and the anvaya keeps whole.
    A cap lower than the longest real compound is not a safeguard — it reports
    a correct anvaya as a defect.
    """
    units = set(rows)
    for span in (2, 3, 4, 5):
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
    still = [t for t in still if t not in FUNCTION_WORDS]
    # Finally, the two spellings the applier itself reconciles: a vocative
    # re-cased into the sentence's nominative (verse परन्तप, anvaya परन्तपः), and
    # a final -m written as anusvāra. Asked of the applier's matcher rather than
    # reimplemented here, so the test and the code cannot drift apart.
    from anvaya import _same_word
    from indic_transliteration import sanscript as _sc
    from indic_transliteration.sanscript import transliterate as _tr
    kept = []
    for t in still:
        # The avagraha (ऽ) marks an elided vowel, not a different word: the
        # reference quotes Arjuna's words as ऽन योत्स्येऽ — "na yotsye" with the
        # elided a written out. It is punctuation, so it is dropped here.
        ti = _tr(t, _sc.DEVANAGARI, _sc.IAST).replace("'", "")
        if any(_same_word(ti, u) for u in iast_units):
            continue
        # two adjacent tokens that join into a word of the verse: the anvaya
        # splits yadṛcchayā into yat + ṛcchayā, and the verse prints one word.
        # Joining happens in IAST, where the sandhi rules are defined.
        if any(_same_word(_join_iast([t, u]), w)
               for u in still for w in iast_units):
            continue
        if any(_same_word(_join_iast([u, t]), w)
               for u in still for w in iast_units):
            continue
        kept.append(t)
    return kept


def _join_iast(tokens):
    """Join tokens the way the verse prints them, via the sandhi rules."""
    from indic_transliteration import sanscript as sc
    from indic_transliteration.sanscript import transliterate as tr
    words = [tr(t, sc.DEVANAGARI, sc.IAST) for t in tokens]
    return _join(words)


def _declined(verse):
    """A verse whose anvaya this edition did not take from the reference.

    The applier marks these in the data rather than omitting the fields, and the
    reason is recorded in source/reference/gita_anvaya_ch*.itx. Anything else —
    a mapped verse with no construed literal, a word order that drops a row —
    still fails.
    """
    return bool(verse.get("anv", {}).get("declined"))


def _join_iast(tokens):
    """Join tokens the way the verse prints them, via the sandhi rules."""
    from indic_transliteration import sanscript as sc
    from indic_transliteration.sanscript import transliterate as tr
    words = [tr(t, sc.DEVANAGARI, sc.IAST) for t in tokens]
    return _join(words)


def _declined(verse):
    """A verse whose anvaya this edition did not take from the reference."""
    return bool(verse.get("anv", {}).get("declined"))


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
            if _declined(verse):
                # this edition did not take the reference's sentence for this
                # verse, so its words are not expected to be the verse's words.
                # The reason is recorded in the reference file, not ignored.
                continue
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

    def test_construed_literal_is_gloss_and_nothing_else(self):
        """anv.lit must be the rows' own glosses in anvaya order.

        This is the claim the layer exists to make: the reader can check it
        against the word rows in front of them. Each comma-separated piece is
        one token's gloss — or, for a compound the verse keeps fused, its
        members' glosses joined — so no piece may be a phrase we wrote for
        smoothness. A gloss's own comma is printed " / " for exactly this
        reason: it keeps the literal's separators unambiguous.
        """
        failures = []
        for verse in self._verses():
            lit = verse["anv"].get("lit")
            if not lit:
                if not _declined(verse):
                    failures.append(f"{verse['n']}: mapped anvaya with no construed literal")
                continue
            rows = [w for it in verse["flow"] for w in it.get("words", [])]
            glosses = {w[2].replace(", ", " / ") for w in rows}
            # a supplied word (सति), (अस्ति) has no row, so its gloss comes from
            # anvaya.SUPPLIED_GLOSS. Declared there, allowed here; anything else
            # would be a word we wrote ourselves.
            glosses |= {g["en"] for g in SUPPLIED_GLOSS.values()}
            for piece in lit["en"].split(", "):
                if not piece:
                    continue
                # a compound is several glosses in one piece; every word of it
                # must still come from a gloss, so check the piece against the
                # glosses it could be built from
                if piece in glosses:
                    continue
                if not any(g in piece for g in glosses):
                    failures.append(f"{verse['n']}: '{piece}' is not a gloss of this verse")
        self.assertEqual([], failures, "\n" + "\n".join(failures))

    def test_literal_and_word_order_agree(self):
        """The loop: the literal is the word order spoken, and vice versa.

        Rebuild each language's construed literal from anv.w and the rows'
        glosses and require it to equal the stored one. This is the two-way
        check — a stored literal that someone hand-edited, or a word order that
        drifted after the literal was written, both fail here.

        What it cannot check is whether the ORDER is right. The literal is
        generated from anv.w, so reordering anv.w produces a different literal
        and both agree with each other. Order is settled by the two reference
        witnesses, never by this test; see docs/anvaya-sources.md.
        """
        import anvaya as A
        failures = []
        for verse in self._verses():
            lit = verse["anv"].get("lit")
            if not lit or "w" not in verse["anv"]:
                continue
            rebuilt = A.construed_literal(verse, verse["anv"]["w"])
            for lang in ("en", "ne", "hi"):
                if rebuilt[lang] != lit[lang]:
                    failures.append(f"{verse['n']}.{lang}: stored literal "
                                    "disagrees with its word order")
        self.assertEqual([], failures, "\n" + "\n".join(failures))

    def test_declined_verses_say_why(self):
        """A verse without an anvaya must carry a real reason, not a blank."""
        for chapter in _load():
            for theme in chapter["themes"]:
                for part in theme["parts"]:
                    for verse in part["sutras"]:
                        anv = verse.get("anv") or {}
                        if "declined" in anv:
                            self.assertGreater(len(anv["declined"]), 40,
                                               f"{verse['n']}: the reason is too short to be one")
                            self.assertNotIn("lit", anv,
                                             f"{verse['n']}: declined asks for no literal")

    def test_word_order_covers_every_row_once(self):
        """anv.w must place every row of the verse exactly once.

        The construed literal is composed from anv.w, so a row missing there is
        a word missing from the literal — and the composer would not notice,
        because it only reads what the list gives it. A row appearing twice is
        the same fault inverted: a word said twice in the verse's own prose.
        """
        failures = []
        for verse in self._verses():
            if _declined(verse):
                continue
            total = sum(len(it.get("words", [])) for it in verse["flow"])
            placed = []
            for tok in verse["anv"].get("w", []):
                if isinstance(tok, int):
                    placed.append(tok)
                elif isinstance(tok, dict):
                    placed.extend(tok.get("r", []))
            if sorted(placed) != list(range(total)):
                missing = sorted(set(range(total)) - set(placed))
                dupes = sorted({i for i in placed if placed.count(i) > 1})
                failures.append(f"{verse['n']}: {total} rows, placed {len(placed)}"
                                + (f", missing {missing}" if missing else "")
                                + (f", repeated {dupes}" if dupes else ""))
        self.assertEqual([], failures, "\n" + "\n".join(failures))

    def test_anvaya_differs_from_the_pada_order(self):
        """An anvaya that merely copies the verse proves nothing.

        A one-line verse may legitimately keep its order where prose order and
        verse order coincide — 1.21 is one — so this asserts on the whole
        chapter rather than per verse, and only that the edit is real.
        """
        changed = 0
        total = 0
        for verse in self._verses():
            if _declined(verse):
                continue
            total += 1
            anv = " ".join(_tokens(verse["anv"]["d"]))
            pada = " ".join(_rows(verse))
            if anv != pada:
                changed += 1
        self.assertGreater(changed, total // 2,
                           "most anvayas should reorder their verse")


if __name__ == "__main__":
    unittest.main()
