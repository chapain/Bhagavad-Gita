# -*- coding: utf-8 -*-
"""check_padas.py — verify the word-by-word splits against the pādas.

For every pāda in padas_ch*.py, this rebuilds the pāda from the individual words
listed in padachheda_ch*.py (applying external sandhi) and checks the two agree.
It is how a typo in a word split gets caught. It only reads and reports; it never
changes your data."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify import norm1
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
checked = 0
for ch, W, jf in CHS:
    d = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), jf)))
    for vno, vd in sorted(W.items()):
        rows = PADAS[f"{ch}.{int(vno):02d}"]
        ptxt = [r[2].strip() for r in rows if r[0] == "p"]
        for p in (0, 1, 2, 3):
            if p >= len(ptxt): continue
            wl = vd.get(p, [])
            if not wl: continue
            checked += 1
            T = norm1(ptxt[p].replace(" ", ""))
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
print("pādas checked:", checked, "| residual flags:", len(flags))
for f in flags:
    print(f)
