# -*- coding: utf-8 -*-
"""audit_titles.py — check every theme/verse title and description against the
verses it actually represents.

Prompted by two real defects the owner found by reading (2026-09-02/03):

  1.10  title "Their force is shielded by Bhīṣma"
        The Sanskrit says asmākam (OURS) is guarded by Bhīṣma and eteṣām
        (THEIRS) by Bhīma. The title reverses the sides — Duryodhana is
        speaking about his own army. The DESCRIPTION was right; only the
        title, which was rewritten later, was wrong.

  1.09  Nepali title "मरिन तयार" — not a valid infinitive; should be मर्न.

Both were introduced when titles were rewritten in bulk, and neither was
catchable by any existing suite: the pāda checker validates Sanskrit against
its word-split, the paraphrase checker compares two English strings to each
other, and nothing compared a TITLE to its VERSE.

Every check here is mechanical and evidence-based — it reads the Sanskrit and
the literal translation and flags a contradiction. It reports; it never edits.
A finding is a candidate for human review, not proof of error: Sanskrit drops
pronouns freely and a title may legitimately summarise rather than restate.

    python3 audit_titles.py            # the report build.py prints
    python3 audit_titles.py --markdown # a review worksheet, triaged by evidence
                                       # (snapshot kept in docs/title-review.md)
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- load ----
def load():
    chapters = []
    for n in range(1, 19):
        raw = io.open(os.path.join(ROOT, "data", "ch%d.js" % n), encoding="utf-8").read()
        obj = json.loads(raw[raw.index("=") + 1:].rstrip().rstrip(";"))
        chapters.append(obj)
    return chapters


# ------------------------------------------------------------- helpers ----
# Names that matter and are easy to confuse by one keystroke. Each entry maps
# an English spelling to the IAST fragments that prove it is in the verse.
NAMES = {
    "Bhīṣma":      ["bhīṣma"],
    "Bhīma":       ["bhīma"],          # NOT bhīṣma — the 1.10 error
    "Droṇa":       ["droṇa"],
    "Drupada":     ["drupada"],
    "Kṛpa":        ["kṛpa"],
    "Karṇa":       ["karṇa"],
    "Arjuna":      ["arjuna", "pārtha", "dhanañjaya", "kaunteya", "kirīṭī",
                    "savyasācin", "guḍākeśa", "bhārata", "paramtapa", "parantapa"],
    "Kṛṣṇa":       ["kṛṣṇa", "keśava", "govinda", "madhusūdana", "janārdana",
                    "hṛṣīkeśa", "acyuta", "vāsudeva", "mādhava", "śrībhagavān"],
    "Sañjaya":     ["sañjaya"],
    "Dhṛtarāṣṭra": ["dhṛtarāṣṭra"],
    "Duryodhana":  ["duryodhana", "rājan"],
    "Yudhiṣṭhira": ["yudhiṣṭhira", "dharmarāja"],
    "Abhimanyu":   ["saubhadra", "abhimanyu"],   # "son of Subhadrā"
    "Vyāsa":       ["vyāsa"],
    "Nārada":      ["nārada"],
    "Indra":       ["indra", "vāsava", "śakra"],
    "Viṣṇu":       ["viṣṇu"],
    "Śaṅkara":     ["śaṅkara"],
    "Yama":        ["yama"],
    "Varuṇa":      ["varuṇa"],
    "Agni":        ["agni", "pāvaka", "vahni"],
    "Vāyu":        ["vāyu", "marut", "pavana", "anila"],
    "Prahlāda":    ["prahlāda"],
    "Garuḍa":      ["garuḍa", "vainateya"],
    "Vāsuki":      ["vāsuki"],
    "Meru":        ["meru"],
    "Rāma":        ["rāma"],
    "Prajāpati":   ["prajāpati"],
    "Manu":        ["manu"],
    "Ikṣvāku":     ["ikṣvāku"],
    "Vivasvān":    ["vivasvān", "vivasvate", "vivasvataḥ"],
}

# Possessive / person markers, English side and their Sanskrit evidence.
OURS   = ["asmāka", "asmad", "naḥ ", "nas ", "mama", "me "]
THEIRS = ["eteṣāṃ", "eteṣam", "teṣāṃ", "teṣam", "tasya", "tad", "amī"]

SPEAKERS = {
    "śrībhagavān": "Kṛṣṇa", "arjuna": "Arjuna",
    "sañjaya": "Sañjaya", "dhṛtarāṣṭra": "Dhṛtarāṣṭra",
}


# The literal translations use epithets freely — "Hṛṣīkeśa blew Pāñcajanya"
# IS Kṛṣṇa, "the son of Subhadrā" IS Abhimanyu. Matching a bare name against
# the text produced 38 false positives before this.
EPITHETS_EN = {
    "Kṛṣṇa":     ["hṛṣīkeśa", "keśava", "govinda", "madhusūdana", "janārdana",
                  "acyuta", "vāsudeva", "mādhava", "the blessed lord", "the lord",
                  "lord of yoga", "hari", "viṣṇu"],
    "Arjuna":    ["pārtha", "dhanañjaya", "kaunteya", "gudākeśa", "guḍākeśa",
                  "kirīṭī", "savyasācin", "the pāṇḍava", "son of kuntī",
                  "son of pāṇḍu", "bhārata", "scorcher of foes", "mighty-armed"],
    "Duryodhana": ["the king", "son of dhṛtarāṣṭra", "his teacher", "prince",
                   "evil-minded"],
    "Droṇa":     ["his teacher", "the teacher", "the ācārya", "ācārya"],
    "Abhimanyu": ["son of subhadrā", "subhadrā"],
    "Yama":      ["death", "the ruler of the dead"],
    "Agni":      ["fire"],
    "Vāyu":      ["wind"],
    "Indra":     ["vāsava", "lord of the gods"],
    "Sañjaya":   ["sañjaya said"],
    "Vivasvān":  ["the sun", "sun-god"],
}


def norm(s):
    return (s or "").lower()


def possessive_side(text, name):
    """Return which army/person a nearby possessive assigns to name.

    The marker can precede the name ("ours, guarded by Bhīṣma") or follow it
    ("Bhīṣma guards our army"). Keep the match inside one clause so it cannot
    cross a semicolon and borrow the other side's marker.
    """
    marker = r"(our|ours|my|mine|their|theirs|his|her)"
    name = re.escape(name.lower())
    patterns = (
        r"\b" + marker + r"\b[^.;]{0,60}" + name,
        name + r"[^.;]{0,60}\b" + marker + r"\b",
    )
    for pattern in patterns:
        m = re.search(pattern, text)
        if m:
            return "our" if m.group(1) in {"our", "ours", "my", "mine"} else "their"
    return None


def strip_diacritics(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()


# ------------------------------------------------------------- checks -----
def audit():
    chapters = load()
    findings = []

    def flag(kind, ref, detail, title, evidence):
        findings.append(dict(kind=kind, ref=ref, detail=detail,
                             title=title, evidence=evidence))

    for ch in chapters:
        speaker_run = None
        for t in ch["themes"]:
            verses = [s for p in t["parts"] for s in p["sutras"]]
            t_iast = " ".join(v["t"] for v in verses)
            t_lit = " ".join(v["lits"]["en"] for v in verses)

            # ---- THEME title/desc: named person must appear in the theme ----
            for field, text in (("theme title", t["titles"]["en"]),
                                ("theme desc", t["descs"]["en"])):
                for name, frags in NAMES.items():
                    if name in text:
                        if not any(f in norm(t_iast) for f in frags):
                            # allow it if the literal names them, by name or epithet
                            _lt = strip_diacritics(t_lit)
                            _ep = [strip_diacritics(e) for e in EPITHETS_EN.get(name, [])]
                            if strip_diacritics(name) not in _lt and \
                               not any(e in _lt for e in _ep):
                                flag("name-not-in-verse",
                                     "%d.t%d" % (ch["num"], ch["themes"].index(t) + 1),
                                     "%s names %s, absent from these verses" % (field, name),
                                     text, verses[0]["n"] + "–" + verses[-1]["n"])

            # ---- per-verse checks ----
            for p in t["parts"]:
                for v in p["sutras"]:
                    ref = v["n"]
                    iast = norm(v["t"])
                    lit = v["lits"]["en"]
                    title = p["titles"]["en"]
                    desc = p["descs"]["en"]

                    # 1. a name in the title must be in THIS verse
                    for name, frags in NAMES.items():
                        if name in title:
                            _l = strip_diacritics(lit)
                            _ep = [strip_diacritics(e) for e in EPITHETS_EN.get(name, [])]
                            if not any(f in iast for f in frags) and \
                               strip_diacritics(name) not in _l and \
                               not any(e in _l for e in _ep):
                                flag("name-not-in-verse", ref,
                                     "title names %s, absent from the verse" % name,
                                     title, lit[:110])

                    # 2. possessive inversion — the 1.10 class
                    tl = norm(title)
                    has_our = re.search(r"\b(our|ours|my|mine)\b", tl)
                    has_their = re.search(r"\b(their|theirs|his|her)\b", tl)
                    if has_our or has_their:
                        ev_ours = any(x in iast for x in OURS)
                        ev_theirs = any(x in iast for x in THEIRS)
                        # only meaningful when the verse contrasts BOTH
                        if ev_ours and ev_theirs:
                            # compare against the literal, which was authored
                            # directly from the Sanskrit
                            ll = norm(lit)
                            for name, frags in NAMES.items():
                                if name not in title:
                                    continue
                                # Find each name's side independently in both the
                                # title and literal. A title can correctly mention
                                # BOTH "our" and "their" armies, so a single
                                # has_our flag cannot stand for every named person.
                                said = possessive_side(tl, name)
                                side = possessive_side(ll, name)
                                if said and side and side != said:
                                    flag("possessive-inverted", ref,
                                         "title says '%s' but the verse puts %s on '%s'"
                                         % (said, name, side),
                                         title, lit[:130])

                    # 3. speaker attribution
                    spk = None
                    for f in (v.get("flow") or []):
                        if f.get("k") == "s":
                            key = re.sub(r"\s*uv[aā]ca.*", "", f.get("t", "")).strip().lower()
                            spk = SPEAKERS.get(key)
                            break
                    for text, field in ((title, "title"), (desc, "desc")):
                        m = re.search(r"\b(Kṛṣṇa|Arjuna|Sañjaya|Dhṛtarāṣṭra)\b"
                                      r"\s+(says|asks|answers|replies|said|declares|speaks)", text)
                        if m and spk and m.group(1) != spk:
                            flag("speaker-mismatch", ref,
                                 "%s attributes speech to %s; the verse marks %s"
                                 % (field, m.group(1), spk),
                                 text, lit[:110])

                    # 4. numbers in the title must appear in the verse
                    NUMWORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                                "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                                "twelve": 12, "sixteen": 16, "eighteen": 18}
                    for w, n in NUMWORDS.items():
                        # only when used as a count: "the three paths", "two kinds".
                        # Bare "one" is usually the pronoun ("one is not reborn").
                        if not re.search(r"\b(the\s+)?%s\s+\w+s\b" % w, tl):
                            continue
                        if w == "one":
                            continue
                        if not re.search(r"\b(%s|%d)\b" % (w, n), norm(lit)):
                                flag("number-unsupported", ref,
                                     "title says '%s' but the verse does not" % w,
                                     title, lit[:110])

                    # 5. negation flip — title asserts what the verse denies
                    tneg = bool(re.search(r"\b(not|never|no|nor|cannot|neither)\b", tl))
                    lneg = bool(re.search(
                        r"\b(not|never|no|none|nor|cannot|neither|without|free from|"
                        r"un\w+|destroyed|indestructible|imperishable|unable|"
                        r"nothing|hell|end)\b", norm(lit)))
                    if tneg and not lneg:
                        flag("negation-unsupported", ref,
                             "title negates; the verse does not", title, lit[:110])

    # ---- structural checks: objectively true or false, no judgement ----
    for ch in chapters:
        flat = [(p["sutras"][0]["n"], p["titles"]["en"], p["descs"]["en"])
                for t in ch["themes"] for p in t["parts"]]
        for i in range(len(flat) - 1):
            if strip_diacritics(flat[i][2]) == strip_diacritics(flat[i + 1][2]):
                flag("adjacent-duplicate", flat[i][0],
                     "description identical to %s" % flat[i + 1][0], flat[i][2], "")
            if strip_diacritics(flat[i][1]) == strip_diacritics(flat[i + 1][1]):
                flag("adjacent-duplicate", flat[i][0],
                     "title identical to %s" % flat[i + 1][0], flat[i][1], "")
        for t in ch["themes"]:
            for p in t["parts"]:
                ref = p["sutras"][0]["n"]
                me = "%s.%d" % (ref.split(".")[0], int(ref.split(".")[1]))
                # a description citing a DIFFERENT verse is almost always text
                # that drifted from its neighbour
                for m in re.findall(r"\b(\d{1,2}\.\d{1,2})\b", p["descs"]["en"]):
                    mm = "%s.%d" % (m.split(".")[0], int(m.split(".")[1]))
                    if mm != me:
                        flag("desc-cites-other-verse", ref,
                             "description cites %s" % m, p["descs"]["en"][:90], "")
                for k in ("titles", "descs"):
                    for L in ("en", "ne", "hi"):
                        if not p[k].get(L):
                            flag("missing-language", ref, "%s/%s empty" % (k, L), "", "")
            for k in ("titles", "descs"):
                for L in ("en", "ne", "hi"):
                    if not t[k].get(L):
                        flag("missing-language", "ch%d" % ch["num"],
                             "theme %s/%s empty" % (k, L), t["titles"]["en"], "")

    return findings


# Categories that produced ZERO false positives in the 2026-09-03 sweep and so
# are safe to fail a build on. The looser heuristics (name-not-in-verse,
# number-unsupported, negation-unsupported) stay as advisories: they surfaced
# real defects but also flag legitimate paraphrase, so a human must read them.
STRICT = ("possessive-inverted", "adjacent-duplicate",
          "desc-cites-other-verse", "missing-language")


# ------------------------------------------------------------ worksheet ----
# `--markdown` prints the advisories as a review worksheet instead of a report.
# It exists because "50 advisories" is not a task anyone starts: the list has to
# be triaged first, and the triage is mechanical. Two facts decide most items:
#
#   * the verse is spoken in the FIRST PERSON, so a summary that names the
#     speaker (Kṛṣṇa for most of the book, Duryodhana in 1.1–1.11) is correct
#     even though the IAST never contains that name — Sanskrit drops pronouns;
#   * a "number" title ("The three qualities") summarises an enumeration, and
#     the verse names the three things without saying the word "three".
#
# Neither fact makes a finding wrong; it only says which items a human can skim
# and which need a careful read. The worksheet never edits anything.

FIRST_PERSON = re.compile(r"\b(I|I'm|I'll|my|mine|me|we|our|ours|us)\b")
# A vocative in the literal ("O Bhārata", "O Dhanañjaya") means the verse is
# being spoken TO someone — and in this poem that speaker is Kṛṣṇa, who is the
# person most often named in a summary that the IAST never names.
VOCATIVE = re.compile(r"\bO\s+[A-ZĀĪŪṚṢṬḌṆṄÑŚ]")


def _worksheet(findings, chapters):
    lit = {}          # "2.47" -> English literal
    theme_vs = {}     # "2.t3" -> [verse refs]
    for ch in chapters:
        for ti, th in enumerate(ch["themes"], 1):
            vs = [s for p in th["parts"] for s in p["sutras"]]
            for v in vs:
                lit[v["n"]] = v["lits"]["en"]
            theme_vs["%d.t%d" % (ch["num"], ti)] = [v["n"] for v in vs]

    def refs_of(ref):
        if ref in lit:
            return [ref]
        return theme_vs.get(ref, [])

    def triage(x):
        """(label, the verses' own words) — evidence, never a verdict."""
        rs = refs_of(x["ref"])
        text = " ".join(lit.get(r, "") for r in rs)
        if x["kind"] == "number-unsupported":
            return ("the verse lists the things but never says the number", text)
        if FIRST_PERSON.search(text):
            return ("first person: the verse is spoken by this person", text)
        if VOCATIVE.search(text):
            return ("the verse addresses its listener (“O …”): the named speaker is the one talking", text)
        if x["ref"].count(".t"):
            return ("theme summary across %d verses: check the scene" % len(rs), text)
        return ("no first person in the verse: read by hand", text)

    buckets = {}
    for x in findings:
        label, text = triage(x)
        buckets.setdefault((x["kind"], label), []).append((x, text))

    # Which rows of the compact table below carry an advisory. A title can be
    # flagged by two kinds at once, so this is a list, not a flag. Theme
    # advisories (1.t4, 18.t4) cover several verses and so have no single row
    # to sit beside; they get their own table further down.
    flagged = {}
    for x in findings:
        _ch, _, _v = x["ref"].partition(".")
        if _v.isdigit():          # a verse ref ("2.47"), never a theme ("1.t4")
            flagged.setdefault(x["ref"], []).append(x["kind"])

    out = []
    import datetime
    out.append("# Title and description advisories — review worksheet\n")
    out.append("Snapshot of %s, from `python3 source/audit_titles.py --markdown`. Re-run it after"
               % datetime.date.today().isoformat())
    out.append("any change to `source/ch*.json`; this file is a worklist, not site content.\n")
    out.append("**An advisory is a candidate for review, not a finding of error.** Sanskrit")
    out.append("drops pronouns freely and a title may legitimately summarise rather than")
    out.append("restate. The one class that *fails* the build is possessive inversion")
    out.append("(the 1.10 defect: “Their force is shielded by Bhīṣma” when the Sanskrit says")
    out.append("*ours* is) — that is blocking, and it is not in this list.\n")
    out.append("Each item shows what the verse actually says, so the decision can be made")
    out.append("without opening the app. Triage labels are mechanical:\n")
    out.append("* **first person** — the verse is spoken by that person, so naming the")
    out.append("  speaker in a summary is correct (Kṛṣṇa speaks in the first person for most")
    out.append("  of the book; Duryodhana in 1.1–1.11). Skim these.\n")
    out.append("* **lists the things, never the number** — “The three qualities” for sattva,")
    out.append("  rajas and tamas. Count the items in the verse; the title is usually right.\n")
    out.append("* **theme summary / read by hand** — the ones worth real attention.\n")
    out.append("---\n")

    # ---- the compact worksheet: all 700 titles, one row each ----
    # The prose below is a list of problems. A quarterly read-through is not a
    # problem list: it is every title, in order, with a place to tick. So the
    # table carries all 700 rows (not only the flagged ones) — a title with no
    # advisory still gets a row, because the read-through is the point and the
    # advisories only say where to look first. Tick columns stay blank: a
    # decision is the owner's, and this script never edits a title.
    out.append("## The worksheet — 700 titles, one row each\n")
    out.append("Every verse title in the edition, chapter by chapter, with the verse's own")
    out.append("English literal beside it. **Tick one of the last three columns per row.**")
    out.append("A ⚑ in the first column means that verse has an advisory — its row already")
    out.append("carries the evidence, so the ticker does not need to open anything else; the")
    out.append("reason it was flagged is noted under each chapter. No ⚑ means no mechanical")
    out.append("doubt was found, which is not the same as a good title — that is what the")
    out.append("read-through is for.\n")
    out.append("This table is generated, so do not edit it by hand: it prints blank boxes")
    out.append("again on the next run. Ticks are working notes, not a change to a title, and")
    out.append("nothing here writes to `source/ch*.json`. Keep the boxes in a copy if you")
    out.append("want them to survive a regeneration.\n")

    for ch in chapters:
        n = ch["num"]
        rows = [(p["sutras"][0]["n"], p) for t in ch["themes"] for p in t["parts"]]
        first, last = rows[0][0], rows[-1][0]
        nflag = sum(1 for ref, _ in rows if flagged.get(ref))
        out.append("### Chapter %d — %s · verses %s–%s · %d titles, %d flagged\n"
                   % (n, ch["names"]["en"], first, last, len(rows), nflag))
        out.append("| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |")
        out.append("|---|---|---|---|:-:|:-:|:-:|")
        for ref, p in rows:
            title = p["titles"]["en"].replace("|", "\\|")
            lit = p["sutras"][0]["lits"]["en"].replace("|", "\\|")
            if len(lit) > 200:
                lit = lit[:197].rsplit(" ", 1)[0] + " …"
            marks = flagged.get(ref, [])
            out.append("| %s | %s | %s | %s | ☐ | ☐ | ☐ |"
                       % ("⚑" if marks else "", ref, title, lit))
        out.append("")
        for ref, p in rows:
            for kind in sorted(set(flagged.get(ref, []))):
                out.append("* ⚑ **%s** — %s. Advisory text: “%s”"
                           % (ref, kind.replace("-", " "), p["titles"]["en"]))
        if nflag:
            out.append("")
        out.append("")

    # ---- theme-level advisories: they span verses, so they get their own list ----
    out.append("## Theme titles and descriptions (not in the table above)\n")
    out.append("A theme advisory covers a run of verses and so has no single row. They are")
    out.append("all of one class — the summary names a speaker whom the verses address or")
    out.append("who is speaking, and Sanskrit drops the pronoun — so they are listed here")
    out.append("once, with the verse range, rather than repeated in the prose below.\n")
    for (kind, label) in sorted(buckets, key=lambda k: (k[0], -len(buckets[k]))):
        theme_items = [(x, t) for x, t in buckets[(kind, label)]
                       if not x["ref"].partition(".")[2].isdigit()]
        if not theme_items:
            continue
        out.append("### %s — %s (%d)\n" % (kind, label, len(theme_items)))
        out.append("| ☐ | Ref | Title or description | Verses | keep | revise | fix |")
        out.append("|---|---|---|:-:|:-:|:-:|")
        for x, text in theme_items:
            rs = refs_of(x["ref"])
            rng = "%s–%s" % (rs[0], rs[-1]) if len(rs) > 1 else (rs[0] if rs else "—")
            out.append("|  | %s | %s | %s | ☐ | ☐ | ☐ |"
                       % (x["ref"], x["title"].replace("|", "\\|"), rng))
        out.append("")

    # ---- verse-level advisories in full: title, evidence, the verse's words ----
    out.append("---\n")
    out.append("## Verse advisories in full\n")
    out.append("The 10 verse-level advisories with the verse's own words, grouped by triage")
    out.append("label. Their rows are already flagged in the table above; this section is the")
    out.append("evidence for each verdict.\n")

    for (kind, label) in sorted(buckets, key=lambda k: (k[0], -len(buckets[k]))):
        items = [(x, t) for x, t in buckets[(kind, label)]
                 if x["ref"].partition(".")[2].isdigit()]
        if not items:
            continue
        out.append("## %s — %s (%d)\n" % (kind, label, len(items)))
        for x, text in items:
            rs = refs_of(x["ref"])
            out.append("### %s · %s" % (x["ref"], x["detail"]))
            if rs:
                out.append("Verses %s–%s" % (rs[0], rs[-1]) if len(rs) > 1 else "Verse %s" % rs[0])
            out.append("")
            out.append("> %s" % x["title"])
            out.append("")
            if text:
                shown = text if len(text) < 460 else text[:457].rsplit(" ", 1)[0] + " …"
                out.append("*the verse says:* %s" % shown)
                out.append("")
            out.append("☐ keep   ☐ revise   ☐ fix")
            out.append("")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    f = audit()
    if "--markdown" in sys.argv:
        print(_worksheet(f, load()))
        hard = [x for x in f if x["kind"] in STRICT]
        sys.exit(1 if hard else 0)
    by = {}
    for x in f:
        by.setdefault(x["kind"], []).append(x)
    print("findings: %d\n" % len(f))
    for kind in sorted(by):
        print("== %s (%d)" % (kind, len(by[kind])))
        for x in by[kind]:
            print("  %-7s %s" % (x["ref"], x["detail"]))
            print("          title: %s" % x["title"])
            print("          verse: %s" % x["evidence"])
        print()
    hard = [x for x in f if x["kind"] in STRICT]
    print("advisory: %d   blocking: %d" % (len(f) - len(hard), len(hard)))
    sys.exit(1 if hard else 0)
