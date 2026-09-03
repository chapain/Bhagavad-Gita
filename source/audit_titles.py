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
                                # find which side the literal puts this name on
                                m = re.search(
                                    r"(ours?|theirs?|our|their)[^.;]{0,60}" +
                                    re.escape(name.lower()), ll)
                                if not m:
                                    m = re.search(
                                        re.escape(name.lower()) + r"[^.;]{0,60}(ours?|theirs?)",
                                        ll)
                                if m:
                                    side = "our" if "our" in m.group(0) else "their"
                                    said = "our" if has_our else "their"
                                    if side != said:
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


if __name__ == "__main__":
    f = audit()
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
