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

    if not dry_run:
        _write_chapter(path, data)
    print(f"\n{Path(path).name}: {applied} anvaya applied"
          + ("" if not dry_run else "  (dry run — nothing written)"))
    if skipped:
        for verse_id, why in skipped:
            print(f"  skipped {verse_id}: {why}")
    return applied


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        raise SystemExit(__doc__)
    apply_chapter(int(args[0]), dry_run="--dry-run" in sys.argv)
