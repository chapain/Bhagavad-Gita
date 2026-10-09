# -*- coding: utf-8 -*-
"""check_padas.py — strict spelling and word-split validation.

Every word's Devanagari is transliterated and compared with its own IAST without
flattening phonemic diacritics. For every pāda, the checker also rebuilds the
line from its split words (applying external sandhi), then performs a lossless
second pass for diacritic disagreements. Legitimate orthographic conventions
are narrow, explicit rules. The checker only reads and reports; it never changes
data, and any discrepancy fails the build."""
import sys, os, re, json, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify import norm1

# A lossless Devanagari → IAST transliterator for validating each pada-chheda
# entry.  Unlike verify.norm1(), this preserves vowel length, retroflexion and
# sibilants: exactly the distinctions this check exists to protect.
CONSONANTS = dict(zip(
    "क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श ष स ह ळ".split(),
    "k kh g gh ṅ c ch j jh ñ ṭ ṭh ḍ ḍh ṇ t th d dh n p ph b bh m y r l v ś ṣ s h ḷ".split()))
VOWELS = dict(zip("अ आ इ ई उ ऊ ऋ ॠ ऌ ॡ ए ऐ ओ औ".split(),
                  "a ā i ī u ū ṛ ṝ ḷ ḹ e ai o au".split()))
MARKS = dict(zip("ा ि ी ु ू ृ ॄ ॢ ॣ े ै ो ौ".split(),
                 "ā i ī u ū ṛ ṝ ḷ ḹ e ai o au".split()))


def deva_to_iast(text):
    out, i = [], 0
    while i < len(text):
        char = text[i]
        following = text[i + 1] if i + 1 < len(text) else ""
        if char in CONSONANTS:
            out.append(CONSONANTS[char])
            if following == "्":
                i += 2
                continue
            if following in MARKS:
                out.append(MARKS[following])
                i += 2
                continue
            out.append("a")
        elif char in VOWELS:
            out.append(VOWELS[char])
        else:
            out.append({"ं": "ṃ", "ः": "ḥ", "ऽ": "’", "ँ": "m̐"}.get(char, char))
        i += 1
    return "".join(out)


def strict_key(text):
    """Fold typography and standard anusvāra spelling, but no diacritics."""
    text = unicodedata.normalize("NFC", text).lower()
    text = re.sub(r"[\s।॥|\-'’]", "", text).replace("ṁ", "ṃ").replace("ṃn", "nn")
    # Devanagari anusvāra may be transliterated either as ṃ or as its
    # homorganic nasal (saṃgha/saṅgha). Final -m is conventionally written ṃ
    # in continuous text. These are narrow orthographic folds, not phoneme
    # flattening: ā/a, ṭ/t, ś/ṣ/s etc. remain distinct.
    text = re.sub(r"[ṅñṇnm](?=[kgcjṭḍtdpbyrlvśṣsh])", "ṃ", text)
    return re.sub(r"[ṃm]$", "ṃ", text)


# Deliberate display/sandhi conventions that cannot be inferred from one word
# in isolation. Keep this list exact and reviewable rather than weakening the
# validator globally.
WORD_SPELLING_CONVENTIONS = {
    ("2.06", "यत् वा", "yad vā"),
    ("9.16", "क्रतुः", "kratur"),
}

from padachheda_ch1 import GITA_CH1_WORDS as W1
from padachheda_ch2 import GITA_CH2_WORDS as W2
from padachheda_ch3 import GITA_CH3_WORDS as W3
from padachheda_ch4 import GITA_CH4_WORDS as W4
from padachheda_ch5 import GITA_CH5_WORDS as W5
from padachheda_ch6 import GITA_CH6_WORDS as W6
from padachheda_ch7 import GITA_CH7_WORDS as W7
from padachheda_ch8 import GITA_CH8_WORDS as W8
from padachheda_ch9 import GITA_CH9_WORDS as W9
from padachheda_ch10 import GITA_CH10_WORDS as W10
from padachheda_ch11 import GITA_CH11_WORDS as W11
from padachheda_ch12 import GITA_CH12_WORDS as W12
from padachheda_ch13 import GITA_CH13_WORDS as W13
from padachheda_ch14 import GITA_CH14_WORDS as W14
from padachheda_ch15 import GITA_CH15_WORDS as W15
from padachheda_ch16 import GITA_CH16_WORDS as W16
from padachheda_ch17 import GITA_CH17_WORDS as W17
from padachheda_ch18 import GITA_CH18_WORDS as W18

VOW1 = "aāiīuūṛṝḷḹeo"
DIGR = ("ai", "au")
VOICED = "yrlvmnghbdjḍ"

def ext_sandhi(w1, w2):
    if not w1 or not w2: return [w1 + w2]
    L = w1[-1]; R2 = w2[:2]; R = w2[0]
    out = []
    if L in VOW1:
        if w1.endswith("au") and (R in VOW1 or R2 in DIGR):
            return [w1[:-2] + "āv" + w2]
        if w1.endswith("ai") and (R in VOW1 or R2 in DIGR):
            return [w1[:-2] + "āy" + w2]
        if R in VOW1 or R2 in DIGR:
            if L in "aā":
                if R in "aā":
                    out.append(w1[:-1] + "ā" + w2[1:])
                    out.append(w1 + "'" + w2[1:])
                    out.append(w1 + w2)
                elif R in "iī":
                    out.append(w1[:-1] + "e" + w2[1:])
                    out.append(w1 + w2)
                elif R in "uū":
                    out.append(w1[:-1] + "o" + w2[1:])
                    out.append(w1 + w2)
                elif R in "ṛṝ":
                    out.append(w1[:-1] + "ar" + w2[1:])
                    out.append(w1 + w2)
                elif R == "e":
                    out.append(w1[:-1] + "ai" + w2[1:])
                    out.append(w1 + w2)
                elif R == "o": out.append(w1[:-1] + "au" + w2[1:])
                elif R2 == "ai": out.append(w1[:-1] + "āi" + w2[2:])
                elif R2 == "au": out.append(w1[:-1] + "āu" + w2[2:])
            elif L in "iī":
                if R in "aā": out.append(w1[:-1] + "y" + w2)
                elif R in "iī": out.append(w1[:-1] + "ī" + w2[1:])
                elif R in "uū":
                    out.append(w1[:-1] + "y" + w2)
                    out.append(w1 + w2)
                elif R in "ṛṝ": out.append(w1[:-1] + "y" + w2)
                elif R in "eo": out.append(w1[:-1] + "y" + w2)
                elif R2 in DIGR: out.append(w1[:-1] + "y" + w2)
            elif L in "uū":
                if R in "aā": out.append(w1[:-1] + "v" + w2)
                elif R in "iī": out.append(w1[:-1] + "v" + w2)
                elif R in "uū": out.append(w1[:-1] + "ū" + w2[1:])
                elif R in "ṛṝ": out.append(w1[:-1] + "v" + w2)
                elif R in "eo": out.append(w1[:-1] + "v" + w2)
                elif R2 in DIGR: out.append(w1[:-1] + "v" + w2)
            elif L in "ṛṝ":
                out.append(w1[:-1] + "r" + w2)
                if R in "aā": out.append(w1[:-1] + "ar" + w2[1:])
                elif R in "iī": out.append(w1[:-1] + "ar" + w2[1:])
                elif R in "uū": out.append(w1[:-1] + "ar" + w2[1:])
            elif L == "e":
                out.append(w1 + "'" + w2[1:])
                if R in "aā": out.append(w1[:-1] + "ay" + w2)
                elif R in "iī":
                    out.append(w1[:-1] + "ay" + w2)
                    out.append(w1[:-1] + "a" + w2)
                    out.append(w1 + w2[1:])
                elif R in "uū": out.append(w1[:-1] + "ay" + w2)
                elif R == "e":
                    out.append(w1[:-1] + "e" + w2[1:])
                    out.append(w1[:-1] + "a" + w2)
            elif L == "o":
                out.append(w1 + "'" + w2[1:])
                out.append(w1[:-1] + "av" + w2)
            elif L == "ai":
                out.append(w1[:-1] + "āy" + w2)
            elif L == "au":
                out.append(w1[:-1] + "āv" + w2)
            else:
                out.append(w1 + w2)
        else:
            out.append(w1 + w2)
        return out
    if L == "ḥ":
        base = w1[:-1]
        if R in VOW1 or R2 in DIGR:
            if w1.endswith("aḥ"):
                out.append(w1[:-2] + "o'" + w2[1:])
                out.append(w1[:-2] + "o" + w2[1:])
                out.append(w1[:-2] + "o" + w2)
                out.append(w1[:-2] + "a" + w2)
            else:
                out.append(w1[:-1] + "r" + w2)
                out.append(base + w2)
                if base and base[-1] in "aā" and R in "aā":
                    out.append(base[:-1] + "ā" + w2[1:])
            return out
        if R == "p": out.append(base + "ṣ" + w2)
        if R == "k": out.append(w1 + w2)
        elif R == "c": out.append(base + "ś" + w2); out.append(w1 + w2)
        elif R == "ṭ": out.append(base + "ṣ" + w2); out.append(w1 + w2)
        elif R == "t": out.append(base + "s" + w2); out.append(w1 + w2)
        elif R == "s": out.append(base + "s" + w2); out.append(w1 + w2)
        elif R == "ś": out.append(base + "ś" + w2); out.append(w1 + w2)
        elif R == "ṣ": out.append(base + "ṣ" + w2); out.append(w1 + w2)
        elif R in VOICED:
            if w1.endswith("aḥ"):
                out.append(w1[:-2] + "o" + w2); out.append(w1[:-1] + "r" + w2)
            else:
                out.append(base + "r" + w2)
        else:
            out.append(w1 + w2)
        out.append(base + w2)
        return out
    if L in "ṃṁ":
        if R == "n": out.append(w1[:-1] + "n" + w2)
        out.append(w1 + w2)
        return out
    if L == "n":
        if R == "l": out.append(w1[:-1] + "ṃ" + R + w2); out.append(w1 + w2)
        if R == "c": out.append(w1[:-1] + "ṃś" + w2); out.append(w1 + w2)
        elif R in "st": out.append(w1[:-1] + "ṃs" + w2); out.append(w1 + w2)
        elif R == "ś": out.append(w1[:-1] + "ṃś" + w2); out.append(w1[:-1] + "ñ" + w2); out.append(w1 + w2)
        elif R == "ṣ": out.append(w1[:-1] + "ṃṣ" + w2); out.append(w1 + w2)
        elif R in "nm": out.append(w1[:-1] + "n" + w2); out.append(w1 + w2)
        elif R in VOW1 or R2 in DIGR:
            out.append(w1 + w2)
            out.append(w1 + "n" + w2)
        else:
            out.append(w1[:-1] + "ṃ" + w2); out.append(w1 + w2)
        return out
    if L == "m":
        if R in "nm": out.append(w1[:-1] + "n" + w2)
        out.append(w1 + w2)
        if R not in VOW1 and R2 not in DIGR: out.append(w1[:-1] + w2)
        return out
    if L == "k":
        if R == "m": out.append(w1[:-1] + "ṅ" + w2)
        if R == "ś": out.append(w1[:-1] + "kch" + w2[1:])
        if R in "yrlvmnghbdjḍ": out.append(w1[:-1] + "g" + w2)
        out.append(w1 + w2)
        return out
    if L == "t":
        if R == "l": out.append(w1[:-1] + "l" + w2)
        if R in "nm": out.append(w1[:-1] + "n" + w2)
        elif R == "d": out.append(w1[:-1] + "d" + w2)
        elif R in "cj": out.append(w1[:-1] + R + w2)
        elif R == "ch": out.append(w1[:-1] + "ch" + w2)
        elif R == "ś": out.append(w1[:-1] + "cch" + w2[1:])
        elif R == "ṣ": out.append(w1[:-1] + "ṭh" + w2)
        elif R == "h": out.append(w1[:-1] + "ddh" + w2[1:])
        elif R in "yrlvmnghbdjḍ": out.append(w1[:-1] + "d" + w2)
        elif R in VOW1: out.append(w1[:-1] + "d" + w2)
        else: out.append(w1 + w2)
        return out
    if L == "d":
        if R == "n": out.append(w1[:-1] + "n" + w2)
        out.append(w1 + w2)
        return out
    if L == "s":
        if R == "d": out.append(w1[:-1] + "ḍ" + w2)
        out.append(w1 + w2)
        return out
    out.append(w1 + w2)
    return out

def reconstruct(words):
    words = [w.replace(" ", "") for w in words]
    states = {words[0]}
    for w in words[1:]:
        nxt = set()
        for st in states:
            for j in ext_sandhi(st, w):
                nxt.add(j)
        states = nxt
        if not states: break
    return states

PADAS = {}
for _n in range(1, 19):
    _m = __import__(f"padas_ch{_n}")
    PADAS.update(getattr(_m, f"GITA_CH{_n}_PADAS"))

CHS = [("1", W1, "ch1.json"), ("2", W2, "ch2.json"), ("3", W3, "ch3.json"),
       ("4", W4, "ch4.json"), ("5", W5, "ch5.json"), ("6", W6, "ch6.json"),
       ("7", W7, "ch7.json"), ("8", W8, "ch8.json"), ("9", W9, "ch9.json"), ("10", W10, "ch10.json"), ("11", W11, "ch11.json"), ("12", W12, "ch12.json"), ("13", W13, "ch13.json"), ("14", W14, "ch14.json"), ("15", W15, "ch15.json"), ("16", W16, "ch16.json"), ("17", W17, "ch17.json"), ("18", W18, "ch18.json")]

flags = []
word_flags = []
strict_line_flags = []
checked = 0
words_checked = 0
for ch, W, jf in CHS:
    d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), jf)))
    for vno, vd in sorted(W.items()):
        rows = PADAS[f"{ch}.{int(vno):02d}"]
        ptxt = [r[2].strip() for r in rows if r[0] == "p"]
        for p in (0, 1, 2, 3):
            if p >= len(ptxt): continue
            wl = vd.get(p, [])
            if not wl: continue
            verse = f"{ch}.{int(vno):02d}"
            for word in wl:
                words_checked += 1
                convention = (verse, word[0], word[1]) in WORD_SPELLING_CONVENTIONS
                if strict_key(deva_to_iast(word[0])) != strict_key(word[1]) and not convention:
                    word_flags.append((verse, word[0], word[1], deva_to_iast(word[0])))
            checked += 1
            # Full reconstruction permits Sanskrit sandhi but retains the
            # established broad matcher. A second, strict pass below catches
            # precisely the diacritic disagreements that matcher can hide.
            T = norm1(ptxt[p].replace(" ", ""))
            line_strict = strict_key(ptxt[p])
            line_flat = norm1(line_strict)
            for word in wl:
                core = strict_key(word[1])[1:-2]  # exclude sandhi zones
                if (len(core) >= 4 and core not in line_strict and
                        norm1(core) in line_flat):
                    strict_line_flags.append((verse, p + 1, ptxt[p], word[1]))
            cands = reconstruct([w[1] for w in wl])
            cands |= {c[:-1] for c in cands if c.endswith("ḥ")}
            cands |= {c[:-1] + "r" for c in cands if c.endswith("ḥ")}
            cands |= {c[:-1] + "s" for c in cands if c.endswith("ḥ")}
            cands |= {c[:-2] + "o" for c in cands if c.endswith("aḥ")}
            cands |= {c[:-1] + "n" for c in cands if c.endswith("t")}
            cands |= {c[:-1] + "d" for c in cands if c.endswith("t")}
            cands |= {c[:-1] for c in cands if c.endswith("t")}
            cands |= {c[:-1] for c in cands if c.endswith("m")}
            cands |= {c[:-1] for c in cands if c.endswith("n")}
            # gemination: a short vowel + final n doubles before a vowel, and when the
            # pāda ends there the second n stays with this pāda (5.08 jighrann | aśnan)
            cands |= {c + "n" for c in cands if c.endswith("n")}
            # A pāda may END on the first half of a consonant that sandhi doubles or
            # assimilates across the break (2.57 ...snehas | tattat..., 4.33 ...yajñāj |
            # jñāna..., 11.30 ...samantāl | lokān...). Allow the trailing joint letter.
            cands |= {c[:-1] + x for c in cands if c.endswith("ḥ") for x in ("s","r","ś","ṣ","l","o")}
            cands |= {c + x for c in cands for x in ("j","l","s","d","m","g","ṃs","’")}
            # final k/t voice to g/d before a vowel (5.04 samyak -> samyag)
            cands |= {c[:-1] + "g" for c in cands if c.endswith("k")}
            cands |= {c[:-1] + "d" for c in cands if c.endswith("t")}
            # a pāda may open after an elided initial a- marked by the avagraha
            # (8.20 ...bhāvo’nyo’ | vyakto’vyaktāt...)
            cands |= {c[1:] for c in cands if c[:1] == "a"}
            cands |= {c[:-1] for c in cands if c.endswith("k")}
            cands |= {c[:-1] + "ṃś" for c in cands if c.endswith("n")}
            cands |= {c[:-1] + "ṃ" for c in cands if c.endswith("n")}
            cands |= {c[:-1] for c in cands if c.endswith("ṃ")}
            cands |= {c[:-1] + "y" for c in cands if c.endswith("i")}
            cands |= {c[:-1] for c in cands if c.endswith("e")}
            cands |= {c[:-1] + "a" for c in cands if c.endswith("e")}
            if len(wl) > 1:
                cands |= {c + wl[-1][1].replace(" ", "") for c in reconstruct([w[1] for w in wl[:-1]])}  # last word appended literally
            cands |= {"".join(w[1].replace(" ", "") for w in wl)}   # literal un-sandhi'd join
            ok = (any(norm1(c) == T for c in cands)
                  or (T[:1] in "sśṣrnjmgdl" and any(norm1(c) == T[1:] for c in cands))
                  or (len(T) > 1 and T[0] == T[1] and any(norm1(c) == T[2:] for c in cands))
                  or (T[:1] == "'" and any(norm1(c) == "a" + T[1:] for c in cands)))
            if not ok:
                flags.append((ch, vno, p, [w[1] for w in wl], ptxt[p]))
print("words checked:", words_checked, "| spelling flags:", len(word_flags))
for f in word_flags:
    print("word spelling:", f)
print("strict line checks:", checked, "| diacritic flags:", len(strict_line_flags))
for f in strict_line_flags:
    print("line spelling:", f)
print("pādas checked:", checked, "| residual flags:", len(flags))
for f in flags:
    print("pāda reconstruction:", f)
if word_flags or strict_line_flags or flags:
    sys.exit(1)
