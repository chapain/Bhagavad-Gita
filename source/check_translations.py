#!/usr/bin/env python3
"""check_translations.py — a dependency-free safety net over all 2,100 renderings.

Every blocking rule here is a fault that actually shipped in this project, or a
Nepali rule the corpus already follows everywhere but one place (1.09). Nothing
here needs a dictionary, the network or a browser:

    python3 check_translations.py        # run after build_gita.py

  1. banned strings     — readings already ruled out, with the verse that taught
                          us. (जुताइएको: the जुत्- root does not exist in Nepali
                          — जोत्नु / नार्नु do; see HANDOFF §5.2.)
  2. shape              — for all three languages: not empty, no Latin letters in
                          Devanagari text, no double spaces, no space before a
                          danda, balanced “ ”, terminal punctuation present.
  3. duplication        — the same word twice in a row with nothing between them.
                          Hyphenated reduplication (जे-जे, कुन-कुन) and
                          comma-separated lists (थाहा, थाहा पाइने कुरा) are Nepali,
                          so only bare repetition counts — the 1.15 class, where a
                          whole conch name was printed twice.
  4. advisories (never blocking) — X-को + लागि/निम्ति, where Nepali writing guides
                          prescribe the आ-form (जानकारीका लागि, not जानकारीको लागि;
                          मेरा निम्ति, not मेरो निम्ति). Both forms are in everyday
                          use, so this is printed for a human, not enforced.

Advisories are how the corpus stays honest about what has *not* been settled —
they are the reason this file can be strict about 1-3 without pretending the
whole translation is clean.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
LANGS = ("en", "ne", "hi")
DEV_WORD = re.compile(r"[\u0900-\u097F]+")

# ---- 1. readings already ruled out ------------------------------------------
# (string, why, where it came from — keep this list short and specific)
BANNED = [
    ("जुताइएको",
     "the जुत्- root is not Nepali: जोत्नु / नार्नु are (Brihat Shabdakosh: "
     "नार्नु = बग्गीमा घोडा जोत्नु; जुताउनु/जुताइएको are absent from the dictionary)",
     "1.14 Nepali literal, fixed 2026-10-15"),
    ("सौमदत्तिका छोरा",
     "सौमदत्तिः already means 'the son of Somadatta' — adding छोरा gives a "
     "grandson; the verse's own gloss says 'son of Somadatta (Bhūriśravā)' and "
     "the Hindi line reads सोमदत्त का पुत्र",
     "1.08 Nepali literal + paraphrase, fixed 2026-10-15"),
    ("मृदङ्ग र सिंहनादहरू",
     "गोमुखाः is a horn-trumpet, not a lion's roar; the word gloss says "
     "गोमुखहरू and that roar belongs to 1.12 (सिंहनादं विनद्य)",
     "1.13 Nepali literal, fixed 2026-10-15"),
    ("नासिने र नासिने",
     "क्षर and अक्षर are perishable and imperishable, not two perishables",
     "15.16 Nepali paraphrase, fixed 2026-10-16 batch 3"),
    ("नकुभल्याउने",
     "unclear rendering of अपैशुनम्; use an explicit absence of slander",
     "16.02 Nepali paraphrase, fixed 2026-10-16 batch 3"),
    ("लोभ, क्रोध र लालच",
     "कामः क्रोधः लोभः distinguishes desire, anger and greed; two words for "
     "greed erase कामः",
     "16.21 Nepali paraphrase, fixed 2026-10-16 batch 3"),
    ("अनन्य त्यागी",
     "अत्यागिनाम् means non-renouncers, not single-minded renouncers",
     "18.12 Nepali literal, fixed 2026-10-16 batch 3"),
]

# ---- 3. reviewed exceptions to the duplication rule --------------------------
# Bare repetition that has been read and left alone on purpose. Each needs a
# reason and a verse, so an allowlist never becomes a hiding place.
DUP_ALLOW = [
    ("4.11", "ne", "lit", "जसरी जसरी",
     "correlative reduplication (जसरी जसरी … त्यसरी); the corpus writes the "
     "same class hyphenated elsewhere (जे-जे, जब-जब, जुन-जुन), so this is "
     "punctuation, not a repeat"),
    ("11.44", "hi", "lit", "मित्र मित्र",
     "the Sanskrit is elliptical — सखेव सख्युः, 'a friend to a friend' — so the "
     "repetition is the verse (NE keeps मित्रले मित्रलाई)"),
    ("11.44", "hi", "para", "दोस्त दोस्त",
     "same ellipse, सरल-अर्थ register"),
    ("18.09", "ne", "para", "कर्तव्य कर्तव्य",
     "the reduplication carries the Hindi/Nepali 'duty is duty' sense of "
     "कार्यमित्येव; queued for the chapter-18 batch (README of the batch is in "
     "PROJECT.md §0), not silently kept"),
]

# ---- 4. advisory: the आ-form Nepali writing guides prescribe ------------------
# "लागि/निम्ति/निमित्त शब्दका अगाडि सधैँ आकार प्रयोग गर्ने… (मेरो लागि/जानकारीको
# लागि नलेख्ने)" — sahityapost.com, नेपाली भाषा लेखनमा ध्यान दिनुपर्ने स-साना
# कुराहरू. The possessive suffix is को for consonant-final stems and रो/नो/यो
# elsewhere (मेरो, हाम्रो, आफ्नो), so all four श-class endings are watched.
# Both forms are in everyday use on ne.wikipedia (उसको लागि 8 /
# उसका लागि 7; जसको लागि 64 / जसका लागि 84), so this stays advice.
AA_FORM = re.compile(r"([\u0900-\u097F]+(?:को|रो|नो|यो))\s+(लागि|निम्ति|निमित्त)")
AA_SUGGEST = {"को": "का", "रो": "रा", "नो": "ना", "यो": "या"}


def load_pages():
    pages = []
    for n in range(1, 19):
        p = os.path.join(DATA_DIR, f"ch{n}.js")
        if not os.path.exists(p):
            sys.exit(f"data/ch{n}.js not found — run build_gita.py first")
        src = open(p, encoding="utf-8").read()
        m = re.match(r"^GITA_CH\[(\d+)\] = (\{.*\});\n$", src, re.S)
        if not m or int(m.group(1)) != n:
            sys.exit(f"data/ch{n}.js is malformed")
        pages.append(json.loads(m.group(2)))
    return pages


def pairs(pages):
    """(verse, lang, kind, text) for every shipped literal and paraphrase."""
    for c in pages:
        for t in c["themes"]:
            for p in t["parts"]:
                for v in p["sutras"]:
                    for lang in LANGS:
                        yield v["n"], lang, "lit", v["lits"][lang]
                        yield v["n"], lang, "para", v["paras"][lang]
                        # word arrays are [deva, iast, en, ne, hi]
                        for blk in (*v["flow"], *v.get("speakers", []), *v["padas"]):
                            for w in blk["words"]:
                                yield v["n"], "ne", "gloss", w[3]
                                yield v["n"], "hi", "gloss", w[4]


def scan(rows):
    """Run every rule over (verse, lang, kind, text) rows. Returns (bad, advisories)."""
    bad = []
    advisories = []

    # 1. banned strings
    for verse, lang, kind, text in rows:
        for s, why, origin in BANNED:
            if s in text:
                bad.append(f"{verse} {lang} {kind}: banned {s!r} — {why} [{origin}]")

    # 2. shape
    for verse, lang, kind, text in rows:
        t = text.strip()
        where = f"{verse} {lang} {kind}"
        if not t:
            bad.append(f"{where}: empty")
            continue
        if kind == "gloss":
            # a word meaning is a fragment, not a sentence: check the shape it
            # shares with the rest (no Latin, no doubled space) and stop
            if re.search(r"[A-Za-z]", t):
                bad.append(f"{where}: Latin letters inside a Nepali/Hindi word meaning: {t[:60]!r}")
            if "  " in t:
                bad.append(f"{where}: double space")
            continue
        if lang != "en" and re.search(r"[A-Za-z]", t):
            bad.append(f"{where}: Latin letters inside Devanagari text: {t[:60]!r}")
        if "  " in t:
            bad.append(f"{where}: double space")
        if re.search(r"\s[।॥]", t):
            bad.append(f"{where}: space before a danda")
        if t.count("“") != t.count("”"):
            bad.append(f"{where}: unbalanced quotation marks")
        # Trailing punctuation is required — a rendering that stops on a word
        # is truncated (1.15's Hindi literal ended with no verb and no mark).
        # A comma / colon / dash means the sentence continues into the next
        # verse (18.51 continues into 18.52), so that is an advisory, not a fault.
        tail = t.rstrip("”\"’'«»")
        if not tail or not re.search(r"[।॥?!.,;:…—]$", tail):
            bad.append(f"{where}: ends without punctuation: …{t[-30:]!r}")
        # (a trailing comma / colon / dash is how a verse that continues into
        # the next one ends; 215 of them ship, all deliberate, so nothing is
        # printed for them)

    # 3. duplication — a word, or a run of up to three words, printed twice in
    # a row with nothing but whitespace between the two runs. That is the 1.15
    # class (a whole conch name printed twice) and the 18.27 class. Legitimate
    # Nepali is untouched: "अज्ञान ज्ञान" is two different words, comma-separated
    # "थाहा, थाहा पाइने कुरा" is a list, and "जे-जे" is a hyphenated reduplication.
    allow = {(v, l, k, phrase) for v, l, k, phrase, _ in DUP_ALLOW}
    for verse, lang, kind, text in rows:
        toks = list(DEV_WORD.finditer(text))
        words = [m.group() for m in toks]
        for n in (1, 2, 3):
            for i in range(len(words) - 2 * n + 1):
                if words[i:i + n] != words[i + n:i + 2 * n]:
                    continue
                if any(len(w) < 2 for w in words[i:i + n]):
                    continue
                # only whitespace inside each run and between the two runs
                gaps = [text[toks[j].end():toks[j + 1].start()]
                        for j in range(i, i + 2 * n - 1)]
                if any(g.strip() for g in gaps):
                    continue
                phrase = " ".join(words[i:i + n])
                allowed = next((a[3] for a in DUP_ALLOW
                                if (verse, lang, kind) == a[:3] and phrase in a[3]), None)
                if allowed:
                    advisories.append(
                        f"{verse} {lang} {kind}: reviewed repetition kept ({allowed})")
                    continue
                bad.append(f"{verse} {lang} {kind}: {phrase!r} printed twice in a "
                           f"row — 1.15/18.27 class: {text[:80]!r}")

    # 4. advisory only
    for verse, lang, kind, text in rows:
        if lang != "ne":
            continue
        for m in AA_FORM.finditer(text):
            word = m.group(1)
            suffix = next(s for s in AA_SUGGEST if word.endswith(s))
            suggestion = word[:-len(suffix)] + AA_SUGGEST[suffix]
            advisories.append(
                f"{verse} {kind}: {m.group(0)!r} — Nepali writing guides prescribe "
                f"the आ-form before {m.group(2)} ({suggestion} {m.group(2)})")

    return bad, advisories


def main():
    pages = load_pages()
    rows = list(pairs(pages))
    bad, advisories = scan(rows)
    print(f"translation strings checked: {len(rows)}")
    for a in advisories:
        print(f"  advisory: {a}")
    if bad:
        print(f"\nFAILURES ({len(bad)}):")
        for b in bad:
            print(f"  {b}")
        sys.exit(1)
    print(f"failures: 0   advisories: {len(advisories)}")
    print("RESULT: ALL GREEN")


if __name__ == "__main__":
    main()
