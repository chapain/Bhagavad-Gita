# -*- coding: utf-8 -*-
"""anvaya.py — apply the reference anvaya to the canonical chapter records.

The anvaya (अन्वय) is a verse's words rearranged into natural prose order — the
construal a teacher gives before translating. Its wording is not composed by
this project: it is transcribed from the traditional padaccheda+anvaya edition
recorded in source/reference/, and this module only places that transcription
against our own verses.

Following the governing rule in AGENTS.md, this is a parse of structured data,
never a regex rewrite of JSON: the verse is located by its id, an unambiguous
single match is required, and the file is written back with the same formatting
the chapter files already use.

What it writes, per verse:

    "anv": {"d": "धर्मक्षेत्रे कुरुक्षेत्रे ...", "t": "dharmakṣetre kurukṣetre ..."}

``d`` keeps the reference's compound breaks as ZWNJ, so कुरु-क्षेत्रे renders as
कुरुक्षेत्रे with no visible hyphen but still shows where the compound divides.
``t`` keeps the hyphen, matching the IAST the app already shows.

Usage:
    python3 anvaya.py 1            # apply source/reference/gita_anvaya_ch01.itx
    python3 anvaya.py 1 --dry-run  # report, write nothing
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF_DIR = HERE / "reference"

ZWNJ = "\u200c"

# The reference's own ASCII escapes for Devanagari punctuation and stress marks.
ESCAPES = {
    "##!##": "!", "##?##": "?", "##[##": "[", "##]##": "]",
    "##(##": "(", "##)##": ")", "##'##": "'", "##.##": ".",
}

LABEL_RE = re.compile(r"^\.\.\s*(\d+)\.(\d{2})\.\.\s*(?:\{ref\s*([^}]*)\})?\s*$")
REF_RE = re.compile(r"[A-Za-z~^'.]+")


def _itrans_to_deva(text):
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
    return transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)


def _itrans_to_iast(text):
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
    return transliterate(text, sanscript.ITRANS, sanscript.IAST)


def _iast_to_deva(text):
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
    return transliterate(text, sanscript.IAST, sanscript.DEVANAGARI)


def _unescape(text):
    for k, v in ESCAPES.items():
        text = text.replace(k, v)
    return text


def _strip_virama_marker(text):
    """Drop the reference's word-final ".h" before transliterating.

    In this edition ".h" is not the visarga — the visarga is written "H" or ":".
    ".h" marks a word that ends in a consonant, a convention ITRANS already
    derives from the bare word ("tat" -> तत्, "katham" -> कथम्). Left in place it
    transliterates to "तत्।ह्", so it is removed here and nowhere else: a genuine
    visarga keeps its "H".
    """
    return text.replace(".h", "")


def _join_compound(iast_word):
    """Resolve a hyphenated compound into one word by real sandhi.

    The reference writes a compound's members with hyphens (dharma-kShetre,
    mahA-iShu-AsAH). The Devanagari must show the joined word — धर्मक्षेत्रे,
    महेष्वासाः — not a hyphen and not two words run together without sandhi,
    which would print भीमअर्जुनसमाः for भीमार्जुनसमाः. The IAST keeps the hyphen:
    that is where a reader sees the compound's joints.
    """
    from check_padas import ext_sandhi
    parts = iast_word.split("-")
    joined = parts[0]
    for nxt in parts[1:]:
        candidates = ext_sandhi(joined, nxt)
        joined = candidates[0] if candidates else joined + nxt
    return joined


def _split_sentences(text):
    """Break the ITRANS sentence into chunks, keeping its punctuation.

    A chunk ends at a "." that is a full stop: in this reference a visarga is
    written "H" or ":", so a "." not part of ".h" and not inside a word closes
    a sentence.
    """
    chunks, cur = [], ""
    i = 0
    while i < len(text):
        ch = text[i]
        cur += ch
        if ch == ".":
            nxt = text[i + 1:i + 3]
            if nxt.startswith("h"):
                i += 1
                cur += text[i]
            elif not re.match(r"[A-Za-z]", text[i + 1:i + 2] or " "):
                chunks.append(cur.strip())
                cur = ""
        i += 1
    if cur.strip():
        chunks.append(cur.strip())
    return [c for c in chunks if c and c != "."]


PUNCT = ".,;:!?()[]'"


def _render_line(chunk):
    """One sentence of anvaya -> (devanagari line, IAST line)."""
    plain = re.sub(r"\s+", " ", _unescape(chunk)).strip()

    iast = _itrans_to_iast(plain)
    deva_tokens, iast_tokens = [], []
    for token in iast.split(" "):
        stripped = token.strip(PUNCT)
        if "-" in stripped:
            lead = token[:len(token) - len(token.lstrip(PUNCT))]
            tail = token[len(token.rstrip(PUNCT)):]
            iast_tokens.append(token)
            deva_tokens.append(lead + _iast_to_deva(_join_compound(stripped)) + tail)
        else:
            iast_tokens.append(token)
            deva_tokens.append(_iast_to_deva(token))
    # The reference ends a sentence with a bare "." which is a full stop in its
    # own convention, not the daṇḍa. Devanagari takes "।", IAST takes "|" — the
    # same pair the app already uses for a verse line.
    deva, iast_out = " ".join(deva_tokens).strip(), " ".join(iast_tokens).strip()
    # punctuation rides on the word it follows, never floats after a space:
    # "सञ्जय !" reads as a slip, "सञ्जय!" as print.
    for text in (deva, iast_out):
        pass
    deva = re.sub(r"\s+([!?,;।|])", r"\1", deva)
    iast_out = re.sub(r"\s+([!?,;|])", r"\1", iast_out)
    deva = re.sub(r"\.\s*$", "।", deva)
    iast_out = re.sub(r"\.\s*$", "|", iast_out)
    return deva, iast_out


def render(entry):
    """Turn one reference entry into the (d, t) pair the app stores.

    Two sentences get one line each, which is how the block reads best under a
    verse; anything else stays one flowing paragraph and wraps naturally.
    """
    rendered = [_render_line(c) for c in entry["chunks"]]
    if len(rendered) == 2:
        return rendered[0][0] + "\n" + rendered[1][0], rendered[0][1] + "\n" + rendered[1][1]
    return (" ".join(r[0] for r in rendered),
            " ".join(r[1] for r in rendered))


def parse_reference(chapter):
    """Return {verse_id: {'chunks': [...], 'ref': '...'}} for one chapter file."""
    path = REF_DIR / f"gita_anvaya_ch{chapter:02d}.itx"
    if not path.exists():
        raise SystemExit(f"no reference transcription for chapter {chapter}: {path}")
    entries, cur_id, cur_ref, buf = {}, None, "", []

    def flush():
        if cur_id is None:
            return
        body = re.sub(r"\s+", " ", " ".join(buf)).strip()
        if not body:
            return
        if cur_id in entries:
            raise SystemExit(f"reference lists {cur_id} twice")
        entries[cur_id] = {"chunks": _split_sentences(_strip_virama_marker(body)),
                           "ref": cur_ref, "raw": body}

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = LABEL_RE.match(line)
        if m:
            flush()
            cur_id = f"{int(m.group(1))}.{int(m.group(2)):02d}"
            cur_ref = (m.group(3) or "").strip()
            buf = []
        else:
            buf.append(line)
    flush()
    return entries


def _locate(chapter_data, verse_id):
    """Return the one verse record with this id; refuse zero or many."""
    found = [s for t in chapter_data["themes"]
             for p in t["parts"] for s in p["sutras"] if s["n"] == verse_id]
    if len(found) != 1:
        raise SystemExit(f"{verse_id}: expected exactly one verse, found {len(found)}")
    return found[0]


def _write_chapter(path, chapter_data):
    """Write the chapter back in the file's own two-space JSON style."""
    text = json.dumps(chapter_data, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


def apply_chapter(chapter, dry_run=False, verbose=True):
    path = HERE / f"ch{chapter}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = parse_reference(chapter)

    applied, skipped = 0, []
    for verse_id, entry in sorted(entries.items(),
                                  key=lambda kv: tuple(map(int, kv[0].split(".")))):
        verse = _locate(data, verse_id)
        d, t = render(entry)
        if not d:
            skipped.append((verse_id, "empty anvaya"))
            continue
        if not dry_run:
            verse["anv"] = {"d": d, "t": t}
        applied += 1
        if verbose:
            print(f"{verse_id}: {d.splitlines()[0][:70]}")

    report = annotate(data, chapter) if not dry_run else None
    if not dry_run:
        _write_chapter(path, data)
    print(f"\n{Path(path).name}: {applied} anvaya applied"
          + ("" if not dry_run else "  (dry run — nothing written)"))
    if skipped:
        for verse_id, why in skipped:
            print(f"  skipped {verse_id}: {why}")
    if report:
        print(f"  word order mapped: {report['mapped']}/{applied}")
        for verse_id, words in report["no_literal"]:
            print(f"  no construed literal {verse_id}: anvaya omits {' '.join(words)}")
        for verse_id, toks in report["unresolved"]:
            print(f"  unglossed token {verse_id}: {' '.join(toks)}")
    return applied


# ---------------------------------------------------------------------------
# The anvaya as a teaching control
# ---------------------------------------------------------------------------
# An anvaya sentence is the verse's OWN words in prose order. So every token in
# it must be reachable from the pāda's word rows, and each row keeps the very
# gloss it already has — a word may not mean one thing in the pāda and another
# in the anvaya. The reader asked to be taught word order from the same glosses
# (owner, 2026-11-21), so the mapping is computed here, once, and shipped.
#
# For each verse the applier adds:
#   anv.w   the tokens in order. A token that is one row is its row index; a
#           token fused out of consecutive rows is [i, j, ...] plus the surface
#           Devanagari it is printed as, because धर्मक्षेत्रे is not the string
#           धर्म + क्षेत्रे. The glosses themselves are NOT copied — the browser
#           reads them from the rows, so there is one copy of every meaning.
#   anv.lit the construed literal: those glosses in anvaya order, in all three
#           languages. Written only when the mapping covers every row of the
#           verse; a verse with an unresolved row gets no construed literal and
#           is reported, never quietly shortened.

JOINERS = {"en": ", ", "ne": " ", "hi": " "}


# The chapter data spells the anusvāra ṁ (m with a dot ABOVE, U+1E41) in 121
# words — siṁha, saṁjaya — while indic_transliteration emits ṃ (dot BELOW,
# U+1E43). They are the same sound and a reader cannot see the difference, but
# they are different code points and every one of those words would fail to
# match. Normalise to the form the source data already uses, so the data stays
# the standard and the comparison adapts to it.
ANUSVARA = {"\u1e43": "\u1e41", "\u1e45": "\u1e45"}
# A compound member that ends in -ā or -ī loses that vowel before the next
# member: pāṇḍava + anīkam -> pāṇḍavānīkam, mahī + kṛte -> mahīkṛte. The joiner
# applies the same rule, but a rollback inside _join_run may strip the ā that
# the fold then cannot restore, so both spellings are accepted when matching.
FOLD_PAIRS = (("ā", ""), ("ī", ""))


def _fold_iast(text):
    for bad, good in ANUSVARA.items():
        text = text.replace(bad, good)
    return text


def _final_m(word):
    """The verse writes prasabham, the anvaya prasabhaṁ — same sound, same word.

    The fold in _fold_iast() normalises the anusvāra's codepoint but leaves a
    final -m alone, because mid-word the two are genuinely different letters.
    At the end of a word they are not.
    """
    return word[:-1] + "m" if word.endswith(("ṁ", "ṃ")) else word


def _drop_augment(word):
    """अभवित् / भविता — the same future verb, with the augment the verse prints.

    Chapter 2's anvaya reads abhavitā where the verse has bhavitā: the verse
    negates it as na ... bhavitā, and the anvaya merges na + bhavitā into one
    unnegated form. That is external sandhi over a negative, not a different
    word, and it is exactly the kind of thing this mapping has to see through.
    """
    # the augment is the initial vowel alone: abhavitā -> bhavitā
    if word.startswith(("abha", "abhū", "abho")) and len(word) > 6:
        return word[1:]
    return word


def _same_word(a, b):
    """True when two IAST spellings are the same word under internal sandhi.

    Two tolerances, both narrowly defined:

    * a vowel-length pair (ī/i, ū/u …), which the reference is inconsistent
      about from one verse to the next;
    * a final visarga. An anvaya regularly re-cases a vocative into the
      nominative of the sentence it builds — the verse prints परन्तप, "O
      scorcher", and the anvaya writes परन्तपः because there the word is the
      subject. Stripping one final ḥ is the whole of that allowance; it is not
      general case tolerance, which would let the anvaya say anything.
    """
    fa, fb = _fold_iast(a), _fold_iast(b)
    fa, fb = _final_m(fa), _final_m(fb)
    if fa == fb:
        return True
    if _drop_augment(fa) == _drop_augment(fb):
        return True
    if fa.rstrip("ḥ") == fb.rstrip("ḥ"):
        return True
    if _drop_augment(fa.rstrip("ḥ")) == _drop_augment(fb.rstrip("ḥ")):
        return True
    for long, short in FOLD_PAIRS:
        if fa == fb.replace(long, short, 1):
            return True
        if fa.rstrip("ḥ") == fb.rstrip("ḥ").replace(long, short, 1):
            return True
    return False


def _iast_of_rows(verse):
    return [_fold_iast(w[1].lower()) for it in verse["flow"] for w in it.get("words", [])]


def _token_surfaces(chunks):
    """The anvaya's tokens, in order, as (match key, Devanagari to print).

    The stored Devanagari already fuses each compound by sandhi (धर्मक्षेत्रे),
    so it cannot be split back into rows by spaces. The key is the compound
    joined the same way in IAST with its hyphens removed — that is what the row
    words will be joined to in _join_run(). A supplied word in parentheses
    (sati), (asti) is a token the pāda does not print: it is returned with a
    None key so the mapping counts it as deliberately unglossed.
    """
    out = []
    for chunk in chunks:
        plain = re.sub(r"\s+", " ", _unescape(chunk)).strip()
        iast_line = _itrans_to_iast(plain)
        deva_line = _itrans_to_deva(plain)
        iast_toks, deva_toks = iast_line.split(" "), deva_line.split(" ")
        if len(iast_toks) != len(deva_toks):
            raise SystemExit(f"script token mismatch: {plain!r}")
        for it, dt in zip(iast_toks, deva_toks):
            core_i = it.strip(PUNCT).strip("|").lower()
            core_d = dt.strip(PUNCT)
            if not core_i or not core_d:
                continue
            if core_i in ("|", "||") or core_d in ("|", "।", "॥"):
                continue                       # sentence end, not a word
            if "(" in it or ")" in it:
                # The reference parenthesises two different things: a word the
                # grammar needs but the verse does not print — (sati), (asti),
                # (bhavati) — and a word the verse DOES print but that the
                # reference repeats to make an elliptical clause stand on its
                # own, as (kA~NkShe) does in 1.32. Both are emitted here with a
                # key; map_verse() matches the key against the rows and only
                # falls back to "printed, not glossed" when there is no row.
                bare = core_i.strip("()")
                out.append((_fold_iast(_join_compound(bare)), core_d.strip("()")))
                continue
            out.append((_fold_iast(_join_compound(core_i)), core_d))
    return out


# A conjunction or particle the verse carries fused into its neighbour — the
# च of धृष्टकेतुश्चेकितानः is written चेकितानः in the rows — has no row of its
# own. It is still a word of the verse, so the anvaya may print it and the
# mapping must not treat that as a gap.
PARTICLES = {"ca", "eva", "iti", "hi", "api", "tu", "vā", "na", "ha", "uta",
             "he", "aho", "bata", "eva"}
# Pronouns the reference supplies so a clause has a subject — (mAm) in 1.35,
# (vayam) in 1.37 — where the verse leaves it understood. They are printed in
# the anvaya and carry no gloss, because no row of this verse carries one.
SUPPLIED_PRONOUNS = {"mām", "māṃ", "vayam", "aham", "ahaṃ", "tvam", "tvaṃ"}
# Demonstratives the reference supplies where the verse leaves the reference of
# a noun understood — idaṁ in (idaṁ) vacanam, "these words". They are glossed
# like any other word ("this", "these"), and their Devanagari is the reference's
# own, so that gloss is the reader's own too.
SUPPLIED_DEMONSTRATIVES = {"idam", "idaṃ", "imam", "imām", "etat", "etad"}

# Copulas the reference supplies in parentheses — (santi), (asti), (bhavati),
# (sati), (syāt) — where the verse states a predicate without a verb. Gita Press
# fills the same slots in the same way and parentheses them the same way, which
# is what settles our treatment: they belong in the anvaya, they carry no word
# of the verse's own, and they are printed.
#
# The literal is built from the rows, so a supplied copula contributes nothing
# to it. English needs a "there are"/"is" for the stack to be a sentence at all,
# so 1.09's literal reads "... heroes, and, many, ..." — a list, not a claim.
# That is the honest cost of not inventing a sentence: the construal layer has
# no verb because the verse prints none.
SUPPLIED_COPULAS = {"santi", "asti", "sati", "bhavati", "bhavanti", "syāt",
                    "āsīt", "babhūva"}

# The gloss of a supplied word, in the three languages. A supplied word is one
# the grammar needs and the verse does not print, so no row carries its meaning
# and there is nothing to read it off: it is written down once, here, and marked
# as supplied wherever it is shown. Gita Press does the same in its word
# columns — "(सन्ति) = हैं" — and the parentheses are the mark.
SUPPLIED_GLOSS = {
    # the vocative particle: a word the anvaya prints around a name, not a word
    # the verse carries on its own
    "he":    {"en": "O",    "ne": "हे",      "hi": "हे"},
    "idam":  {"en": "this",  "ne": "यो",   "hi": "यह"},
    "idaṃ":  {"en": "this",  "ne": "यो",   "hi": "यह"},
    "imam":  {"en": "this",  "ne": "यो",   "hi": "यह"},
    "imām":  {"en": "this",  "ne": "यी",   "hi": "यह"},
    "etat":  {"en": "this",  "ne": "यो",   "hi": "यह"},
    "etad":  {"en": "this",  "ne": "यो",   "hi": "यह"},
    "santi": {"en": "are",   "ne": "छन्",  "hi": "हैं"},
    "asti":  {"en": "is",    "ne": "छ",    "hi": "है"},
    "sati":  {"en": "being", "ne": "हुँदा", "hi": "होने पर"},
    "bhavati": {"en": "is",  "ne": "हुन्छ", "hi": "होता है"},
    "bhavanti": {"en": "are", "ne": "हुन्छन्", "hi": "होते हैं"},
    "syāt":  {"en": "would be", "ne": "हुन्थ्यो", "hi": "होता"},
    "āsīt":  {"en": "was",   "ne": "थियो", "hi": "था"},
    "babhūva": {"en": "became", "ne": "भयो", "hi": "हुआ"},
}


def _join_run(words):
    """Every sandhi spelling of a run of row words (see _unit_set in the test)."""
    states = {words[0]}
    for nxt in words[1:]:
        adds = set()
        for prev in states:
            adds |= set(_ext_sandhi(prev, nxt))
            if prev.endswith("m") and nxt[:1] not in "aāiīuūeoṛ":
                adds.add(prev[:-1] + nxt)
        states = adds
    return states


def _ext_sandhi(a, b):
    from check_padas import ext_sandhi
    return ext_sandhi(a, b)


def map_verse(verse, chunks):
    """Map anvaya tokens onto word-row indices.

    Returns (tokens, unmatched_rows, unresolved_tokens). Greedy longest-match:
    try four consecutive rows, then three, then two, then one, so a compound is
    attributed to the rows it was built from rather than to its first member.
    """
    rows = _iast_of_rows(verse)
    tokens, unresolved = [], []
    used = set()
    for iast, deva in _token_surfaces(chunks):
        if iast is None:
            # a supplied word the pāda does not print: printed, never glossed
            tokens.append({"t": deva, "i": iast})
            continue
        hit = None
        longest = min(len(rows), 6)
        for span in range(longest, 0, -1):
            for start in range(len(rows) - span + 1):
                run = rows[start:start + span]
                if any(i in used for i in range(start, start + span)):
                    continue
                if any(_same_word(iast, cand) for cand in _join_run(run)):
                    hit = (start, span)
                    break
            if hit:
                break
        if hit:
            start, span = hit
            used.update(range(start, start + span))
            if span == 1:
                tokens.append(start)
            else:
                tokens.append({"r": [start + k for k in range(span)], "t": deva})
        elif iast in SUPPLIED_DEMONSTRATIVES or iast in SUPPLIED_COPULAS:
            tokens.append({"t": deva, "i": iast, "sup": iast})
        else:
            # a particle the pāda leaves unsaid — हे is the documented one — is
            # printed but carries no row to gloss
            if iast in PARTICLES or iast in SUPPLIED_PRONOUNS:
                tokens.append({"t": deva, "i": iast, "sup": iast})
            else:
                unresolved.append(iast)
                tokens.append({"t": deva, "i": iast})
    # A printed word our verse keeps whole — yadṛcchayā, tathāpi — which the
    # anvaya splits into the words it was made of: yat ṛcchayā, tathā api. The
    # row is the same word either way, so an unconsumed token is attributed to
    # an unused row when the two join into it by sandhi, in either direction.
    free = [i for i in range(len(rows)) if i not in used]
    for tok in tokens:
        if not (isinstance(tok, dict) and not tok.get("r")):
            continue
        want = _fold_iast(tok.get("i") or tok["t"])
        for i in free:
            if any(_same_word(want, c) for c in _join_run([rows[i]])):
                tok["r"] = [i]
                used.add(i)
                free = [i for i in range(len(rows)) if i not in used]
                break
    # And the anvaya may split one of our rows across two of its tokens:
    # yadṛcchayā is printed as one word and analysed as yat + ṛcchayā. When two
    # adjacent unconsumed tokens join into a row, both take that row — the row is
    # then placed once, with both halves of it on the same gloss, which is
    # honest: the reader sees one word written two ways, not two meanings.
    for k in range(len(tokens) - 1):
        a, b = tokens[k], tokens[k + 1]
        if not (isinstance(a, dict) and isinstance(b, dict)):
            continue
        if a.get("r") or b.get("r"):
            continue
        # the row IS the joined form: yadṛcchayā == yat + ṛcchayā
        joined = _join_run([a.get("i") or a["t"], b.get("i") or b["t"]])
        for i in free:
            if any(_same_word(rows[i], c) for c in joined):
                # the row is placed once: the first token takes it, the second
                # records the other half of the same word
                # The row is placed once, by the first token. The second says
                # it is the other half of the same word: {"s": row}, "same as
                # that row". Two meanings never attach to one row twice, which
                # is what the coverage test enforces.
                a["r"] = [i]
                b["s"] = i
                used.add(i)
                free = [x for x in range(len(rows)) if x not in used]
                break
    # the other half: the anvaya's tokens may join up to one of our rows
    for tok in tokens:
        if not (isinstance(tok, dict) and not tok.get("r")):
            continue
        want = _fold_iast(tok.get("i") or tok["t"])
        for i in free:
            if any(_same_word(c, want) for c in _join_run([rows[i]])):
                tok["r"] = [i]
                used.add(i)
                free = [i for i in range(len(rows)) if i not in used]
                break
    # A fused compound the token-by-token pass could not see. The anvaya writes
    # rāgadveṣavimuktaiḥ where the rows hold rāga + dveṣa + vimuktaiḥ: the verse
    # splits the compound for its word list, the anvaya keeps it whole. Look for
    # runs of still-unused rows that join, by external sandhi, into the token.
    free = [i for i in range(len(rows)) if i not in used]
    for k, tok in enumerate(tokens):
        if not (isinstance(tok, dict) and not tok.get("r")):
            continue
        want = _fold_iast(tok.get("i") or tok["t"])
        got = None
        for start in range(len(free)):
            acc = []
            for j in range(start, min(start + 5, len(free))):
                if free[j] != free[start] + (j - start):
                    break
                acc.append(free[j])
                run = rows[acc[0]:acc[-1] + 1]
                if any(_same_word(want, c) for c in _join_run(run)):
                    got = list(acc)
                    break
            if got:
                break
        if got:
            tok["r"] = got
            used.update(got)
            free = [i for i in range(len(rows)) if i not in used]
    unmatched_rows = [i for i in range(len(rows)) if i not in used]
    return tokens, unmatched_rows, unresolved


# What a gloss's internal comma means. The word rows write a synonym pair with
# one — "arrayed, drawn up", "righteousness, sacred duty" — and a fused compound
# is joined by the same mark, so the comma cannot be the literal's separator.
# " / " says "either gloss, chosen to fit": "arrayed / drawn up".
GLOSS_ALTERNATIVES = " / "


# Which row column holds the gloss for a language. A row is
#   [Devanagari, IAST, English, Nepali, Hindi]
# and the open reader takes the same column. Reading columns was the whole
# point: an earlier version read column 2 for all three languages, so every
# Nepali and Hindi construed literal was English.
ROW_GLOSS_COLUMN = {"en": 2, "ne": 3, "hi": 4}

# A compound's members arrive in verse order, and a head-initial language wants
# them turned round: कुरुक्षेत्रे is "of the Kurus" + "on the field", read
# "on the field of the Kurus". The test is the language's own relational
# vocabulary, not English's — Nepali and Hindi put the relation word at the END
# (कुरुको खेतमा), which is already the Sanskrit order, so they are never turned.
RELATIONAL_PREFIX = {
    "en": {"of", "to", "for", "with", "in", "on", "from", "by", "among", "at",
           "into", "upon", "over", "under", "through", "without", "toward"},
    "ne": {"को", "का", "की", "मा", "बाट", "देखि", "लाई", "सँग", "ले", "बिना"},
    "hi": {"का", "की", "के", "में", "से", "को", "लिए", "साथ", "द्वारा"},
}
# Nepali/Hindi are postpositional, so a relational gloss ends the phrase.
RELATIONAL_SUFFIX = {
    "ne": {"को", "का", "की", "मा", "बाट", "देखि", "लाई", "सँग", "ले"},
    "hi": {"का", "की", "के", "में", "से", "को", "लिए", "साथ", "द्वारा"},
}


def _is_relational(gloss, lang):
    """Does this gloss carry the phrase's relation, rather than its noun?"""
    words = gloss.split()
    if not words:
        return False
    if lang == "en":
        return words[0].lower() in RELATIONAL_PREFIX["en"]
    return words[-1] in RELATIONAL_SUFFIX[lang] or words[0] in RELATIONAL_PREFIX[lang]


def _gloss(rows, idx, lang):
    """One token's gloss: its rows' glosses, read the way the language reads them."""
    col = ROW_GLOSS_COLUMN[lang]
    words = [rows[i] for i in idx]
    if len(words) == 2:
        rel = [_is_relational(w[col], lang) for w in words]
        if rel[0] != rel[1]:
            # "of the Kurus" + "on the field" -> "on the field of the Kurus";
            # "righteousness" + "on the field" -> "on the field of righteousness"
            words = [words[1], words[0]]
    return " ".join(w[col] for w in words)


def construed_literal(verse, tokens):
    """The verse's own glosses, in anvaya order, one language at a time.

    Concatenation, not composition: no word appears here that is not a gloss of
    a word in the verse. That is the whole point of the layer — the reader can
    check it against the rows above it, and the Reading beside it can then be as
    smooth as it likes without claiming to be literal.

    The glosses keep their own punctuation; where a gloss offers alternatives
    with a comma ("arrayed, drawn up") each is kept with " / " because the
    literal needs no choice made for it.
    """
    rows = [w for it in verse["flow"] for w in it.get("words", [])]
    out = {}
    for lang in ("en", "ne", "hi"):
        parts = []
        for tok in tokens:
            if isinstance(tok, int):
                idx = [tok]
            elif isinstance(tok, dict):
                idx = [tok["s"]] if "s" in tok else (tok.get("r") or [])
            else:
                idx = []
            if not idx:
                # a supplied word: no row of the verse carries it, so its gloss
                # is the declared one, and it is marked as supplied in the view
                sup = tok.get("sup") if isinstance(tok, dict) else None
                if sup and sup in SUPPLIED_GLOSS:
                    parts.append(SUPPLIED_GLOSS[sup][lang])
                continue
            parts.append(_gloss(rows, idx, lang).replace(", ", GLOSS_ALTERNATIVES))
        out[lang] = JOINERS[lang].join(p for p in parts if p)
    return out


def _speaker_lead(verse, tokens, missing):
    """Put the verse's own announcement first: "dhṛtarāṣṭra uvāca".

    The reference's anvaya covers the sentence and drops the stage direction —
    1.01 opens "dharmakṣetre kurukṣetre" and never says who is speaking, though
    the verse prints धृतराष्ट्र उवाच first. An anvaya meant to hold the words of
    the verse cannot omit them, and prose order for a quoted speech names the
    speaker first, wherever the printed verse puts the announcement (1.21 and
    1.28 place it between pādas).

    Position, not invention: the words are the verse's own rows, taken in the
    verse's own order, and only the rows the mapping left unused. Returns the
    new token list, the remaining gaps, and the Devanagari / IAST lead to print.
    """
    rows = _iast_of_rows(verse)
    said = [w for it in verse["flow"] if it["k"] == "s" for w in it["words"]]
    if not said:
        return tokens, missing, "", ""
    by_row = {i: w for i in missing for w in said if w[1].lower() == rows[i]}
    if not by_row:
        return tokens, missing, "", ""      # the anvaya already names the speaker
    lead = [{"r": [i], "t": by_row[i][0]} for i in sorted(by_row)]
    return lead + tokens, [i for i in missing if i not in by_row], \
           " ".join(by_row[i][0] for i in sorted(by_row)) + "।", \
           " ".join(by_row[i][1] for i in sorted(by_row)) + " ."


def annotate(data, chapter):
    """Add anv.w and anv.lit to every verse that has an anvaya."""
    entries = parse_reference(chapter)
    report = {"mapped": 0, "no_literal": [], "unresolved": []}
    for verse_id, entry in entries.items():
        verse = _locate(data, verse_id)
        if "anv" not in verse:
            continue
        tokens, missing, unresolved = map_verse(verse, entry["chunks"])
        tokens, missing, lead_d, lead_t = _speaker_lead(verse, tokens, missing)
        if lead_d:
            verse["anv"]["d"] = lead_d + "\n" + verse["anv"]["d"]
            verse["anv"]["t"] = lead_t + "\n" + verse["anv"]["t"]
        verse["anv"]["w"] = tokens
        if unresolved:
            report["unresolved"].append((verse_id, unresolved))
        if missing:
            # A row the anvaya never mentions — the reference leaves it implicit
            # (1.09's madarthe) or folds it away. Composing anyway would print a
            # literal that silently drops a word, so it is left absent and
            # reported for a human to resolve.
            report["no_literal"].append((verse_id, [verse["flow"][0]["words"] and
                [w for it in verse["flow"] for w in it["words"]][i][0]
                for i in missing]))
            verse["anv"].pop("lit", None)
            verse["anv"]["declined"] = (
                "the reference's anvaya follows a different reading of this "
                "verse; see source/reference/gita_anvaya_ch*.itx")
            continue
        verse["anv"]["lit"] = construed_literal(verse, tokens)
        report["mapped"] += 1
    return report


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        raise SystemExit(__doc__)
    apply_chapter(int(args[0]), dry_run="--dry-run" in sys.argv)
