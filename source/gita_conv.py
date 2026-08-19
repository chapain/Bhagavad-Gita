# -*- coding: utf-8 -*-
"""gita_conv.py — shared ITRANS/IAST/Devanagari converters and pāda splitting for the Gita."""
import re

VOW = {"a","A","i","I","u","U","R^i","R^I","L^i","L^I","e","ai","o","au"}
TOKENS = ["R^I","R^i","L^I","L^i","~N","~n","Th","Dh","kh","gh","ch","Ch","jh","th","dh","ph","bh","sh","Sh",
          "ai","au","\\-",".n",".h",".a","||","~","A","I","U","E","O","C","D","H","M","N","R","S","T","G","K","Q","Z","F","L",
          "a","i","u","e","o","k","g","c","j","t","d","p","b","m","y","r","l","v","s","h","n","f","q","z","x","|"]
TOKENS.sort(key=len, reverse=True)

def tokenize(s):
    toks=[];i=0
    while i<len(s):
        for p in TOKENS:
            if s.startswith(p,i): toks.append(p);i+=len(p);break
        else: toks.append(s[i]);i+=1
    return toks

def syll(t):
    return sum(1 for x in t if x in VOW)

IAST_VOW = set("aāiīuūṛṝḷḹeo")
def syll_iast(t):
    """Count syllables in an IAST string. Every vowel letter is one syllable;
    the digraphs ai and au are single (diphthong) syllables."""
    n = 0; i = 0; L = len(t)
    while i < L:
        c = t[i]
        if c in IAST_VOW:
            n += 1
            if c == 'a' and i + 1 < L and t[i+1] in ('i', 'u'):
                i += 2; continue
        i += 1
    return n

def join(toks):
    return "".join(toks)

def split_half_padas(toks, target=None):
    total = syll(toks)
    if target is None: target = total // 2
    cnt = 0
    for i,t in enumerate(toks):
        if t in VOW: cnt += 1
        if cnt == target:
            j = i+1
            while j < len(toks) and toks[j] in (".n",".h","M","H"): j += 1
            return toks[:j], toks[j:], total
    return toks[:len(toks)//2], toks[len(toks)//2:], total

CONS = {"k":"क","kh":"ख","g":"ग","gh":"घ","~N":"ङ","ch":"च","Ch":"छ","j":"ज","jh":"झ","~n":"ञ",
        "T":"ट","Th":"ठ","D":"ड","Dh":"ढ","N":"ण","t":"त","th":"थ","d":"द","dh":"ध","n":"न",
        "p":"प","ph":"फ","b":"ब","bh":"भ","m":"म","y":"य","r":"र","l":"ल","v":"व",
        "sh":"श","Sh":"ष","s":"स","h":"ह","L":"ळ"}
VOWD = {"a":"अ","A":"आ","i":"इ","I":"ई","u":"उ","U":"ऊ","R^i":"ऋ","R^I":"ॠ","L^i":"ऌ","L^I":"ॡ",
        "e":"ए","ai":"ऐ","o":"ओ","au":"औ"}
VSIGN = {"A":"ा","i":"ि","I":"ी","u":"ु","U":"ू","R^i":"ृ","R^I":"ॄ","L^i":"ॢ","L^I":"ॣ",
         "e":"े","ai":"ै","o":"ो","au":"ौ"}

def to_deva(s):
    toks=tokenize(s);out=[]
    for i,t in enumerate(toks):
        if t in CONS:
            out.append(CONS[t]); nxt=toks[i+1] if i+1<len(toks) else None
            if nxt is None or (nxt not in VOWD and nxt not in ("H",".h","M",".n",".a")): out.append("्")
        elif t in VOWD:
            prev=toks[i-1] if i>0 else None
            if prev in CONS:
                if t!="a": out.append(VSIGN[t])
            else: out.append(VOWD[t])
        elif t in ("H",".h"): out.append("ः")
        elif t in ("M",".n"): out.append("ं")
        elif t==".a": out.append("ऽ")
        elif t=="|": out.append(" । ")
        elif t=="||": out.append(" ॥ ")
        elif t=="\\-": out.append(" ")
        else: out.append(t)
    return "".join(out)

def to_iast(s):
    # placeholder to protect cch (Ch) from the ch→c pass
    s = s.replace("Ch", "ⓒ")
    m=[("R^I","ṝ"),("R^i","ṛ"),("L^I","ḹ"),("L^i","ḷ"),("~N","ṅ"),("~n","ñ"),
       ("Th","ṭh"),("Dh","ḍh"),("ch","c"),("kh","kh"),("gh","gh"),("jh","jh"),
       ("th","th"),("dh","dh"),("ph","ph"),("bh","bh"),("sh","ś"),("Sh","ṣ"),
       ("ai","ai"),("au","au"),(".n","ṃ"),(".h","ḥ"),(".a","’"),
       ("A","ā"),("I","ī"),("U","ū"),("T","ṭ"),("D","ḍ"),("N","ṇ"),
       ("M","ṃ"),("H","ḥ"),("a","a"),("i","i"),("u","u"),("e","e"),("o","o"),
       ("k","k"),("g","g"),("c","c"),("j","j"),("t","t"),("d","d"),("p","p"),
       ("b","b"),("m","m"),("y","y"),("r","r"),("l","l"),("v","v"),("s","s"),
       ("h","h"),("n","n"),("q","q"),("x","kṣ"),("f","f"),("z","z"),("\\-"," "),("~",""),("|","।")]
    for a,b in m: s=s.replace(a,b)
    s = s.replace("ⓒ", "ch")
    return s

CONS_D = {"k":"क","kh":"ख","g":"ग","gh":"घ","ṅ":"ङ","c":"च","ch":"छ","j":"ज","jh":"झ","ñ":"ञ",
          "ṭ":"ट","ṭh":"ठ","ḍ":"ड","ḍh":"ढ","ṇ":"ण","t":"त","th":"थ","d":"द","dh":"ध","n":"न",
          "p":"प","ph":"फ","b":"ब","bh":"भ","m":"म","y":"य","r":"र","l":"ल","v":"व",
          "ś":"श","ṣ":"ष","s":"स","h":"ह","ḷ":"ळ","kṣ":"क्ष"}
VOWI_D = {"a":"अ","ā":"आ","i":"इ","ī":"ई","u":"उ","ū":"ऊ","ṛ":"ऋ","ṝ":"ॠ","ḷ":"ऌ","ḹ":"ॡ",
          "e":"ए","ai":"ऐ","o":"ओ","au":"औ"}
VSIGN_D = {"ā":"ा","i":"ि","ī":"ी","u":"ु","ū":"ू","ṛ":"ृ","ṝ":"ॄ","ḷ":"ॢ","ḹ":"ॣ",
           "e":"े","ai":"ै","o":"ो","au":"ौ"}
IAST_TOKENS = ["kṣ","ṭh","ḍh","kh","gh","ch","jh","th","dh","ph","bh","ś","ṣ","ṭ","ḍ","ṇ","ṅ","ñ",
               "ai","au","ā","ī","ū","ṛ","ṝ","ḷ","ḹ","ṃ","ḥ","ṁ","’","a","i","u","e","o",
               "k","g","c","j","t","d","p","b","m","y","r","l","v","s","h","n","q","f","z"]
IAST_TOKENS.sort(key=len, reverse=True)
def itok(s):
    toks=[];i=0
    while i<len(s):
        for p in IAST_TOKENS:
            if s.startswith(p,i): toks.append(p);i+=len(p);break
        else: toks.append(s[i]);i+=1
    return toks
def iast_to_deva(s):
    toks=itok(s);out=[]
    for i,t in enumerate(toks):
        if t in CONS_D:
            out.append(CONS_D[t]); nxt=toks[i+1] if i+1<len(toks) else None
            if nxt is None or (nxt not in VOWI_D and nxt not in ("ṃ","ḥ","ṁ","’")):
                out.append("्")
        elif t in VOWI_D:
            prev=toks[i-1] if i>0 else None
            if prev in CONS_D:
                if t!="a": out.append(VSIGN_D[t])
            else: out.append(VOWI_D[t])
        elif t in ("ṃ","ṁ"): out.append("ं")
        elif t=="ḥ": out.append("ः")
        elif t=="’": out.append("ऽ")
        elif t==" ": out.append(" ")
        else: out.append(t)
    return "".join(out)

def norm1(s):
    return (s.replace("ā","a").replace("ī","i").replace("ū","u").replace("ṛ","r").replace("ṝ","r")
              .replace("ḷ","l").replace("ḹ","l").replace("ṅ","n").replace("ñ","n").replace("ṭ","t")
              .replace("ḍ","d").replace("ṇ","n").replace("ś","s").replace("ṣ","s").replace("ṃ","m")
              .replace("ṁ","m").replace("ḥ","h").replace("’","'").replace("kṣ","x").lower())

def _sandhi_variants(wn):
    """Generate sandhi-tolerant variants of a normalized word (for boundary matching)."""
    out = [wn]
    if wn.endswith("h"):            # final visarga
        for c in "srno":
            out.append(wn[:-1] + c)
        out.append(wn[:-1])
        out.append(wn[:-1] + "o'")  # ḥ + a → o' (e.g. akledyaḥ+aśoṣyaḥ → akledyo'śoṣyaḥ)
        out.append(wn[:-1] + "o")
        if wn.endswith("ah"):
            out.append(wn[:-2] + "o'")  # aḥ + a → o' (adharmaḥ+abhibhavati → adharmo'bhibhavati)
            out.append(wn[:-2] + "o")
        out.append(wn[:-1] + "ms")  # ḥ → ṃs before s/t (anityāḥ+tān → anityāṁstān)
    if wn.endswith("m"):            # final anusvāra → nasal before n/m
        out.append(wn[:-1] + "n")
    if wn.endswith("t"):            # t → n before n (kadācit → kadācin); t → d before voiced; t → c/cc before ś/ch
        out.append(wn[:-1] + "n")
        out.append(wn[:-1] + "d")
        out.append(wn[:-1] + "c")
        out.append(wn[:-1] + "cc")
    if wn.endswith("d"):
        out.append(wn[:-1] + "n")
    if wn.endswith("n"):            # n → ṃś before c/ch ; n → ṃs before s
        out.append(wn[:-1] + "mś")
        out.append(wn[:-1] + "ms")
        out.append(wn[:-1] + "m")
    if wn.endswith("i"):            # i + a → y (jīrṇāni+anyāni → jīrṇānyanyāni)
        out.append(wn[:-1] + "y")
    if len(wn) > 1:
        out.append(wn[1:])          # first char sandhi-altered (leading vowel merges with prev)
        out.append(wn[1:-1] + "s")
        out.append(wn[1:-1] + "n")
        out.append(wn[1:-1] + "r")
        out.append(wn[1:-1] + "c")
        out.append(wn[1:-1] + "cc")
    # de-dup
    seen = set(); uniq = []
    for o in out:
        if o and o not in seen: seen.add(o); uniq.append(o)
    return uniq

def snap_pair(p1_ia, p2_ia, lastA_ia, firstB_ia):
    """Snap the pāda boundary to a word boundary: find the cut where the text ends with the
    last word of pāda A and begins with the first word of pāda B (sandhi-tolerant)."""
    combined = p1_ia + p2_ia
    cnorm = norm1(combined)
    start = len(norm1(p1_ia))
    lastCands = _sandhi_variants(norm1(lastA_ia))
    firstCands = _sandhi_variants(norm1(firstB_ia))
    best = None   # (end, dist)
    for la in lastCands:
        idx = 0
        while True:
            j = cnorm.find(la, idx)
            if j < 0:
                break
            end = j + len(la)
            if end >= start - 15:     # generous window: the word boundary may be far from the metre point
                rest = cnorm[end:].lstrip(" ")
                for fb in firstCands:
                    if rest.startswith(fb):
                        dist = abs(end - start)
                        if best is None or dist < best[1]:
                            best = (end, dist)
                        break
            idx = j + 1
    if best:
        end = best[0]
        return combined[:end], combined[end:]
    return p1_ia, p2_ia

def parse_verse(itrans, words=None):
    """Split a verse into flow (speakers + pādas), snapping pādas to word boundaries."""
    if words is None: words = {}
    segs = re.split(r'(\s*\|\s*)', itrans.strip())
    groups = []
    cur = ""
    for s in segs:
        if s.strip() == "|":
            groups.append(cur); cur = ""
        else:
            cur += (" " + s if cur else s)
    if cur.strip(): groups.append(cur)

    flow = []
    total = 0
    pidx = 0
    for g in groups:
        g = g.strip()
        if not g: continue
        if g.endswith("uvAcha"):
            flow.append({"k": "s",
                         "d": to_deva(g).replace(" । ","।").strip() + "।",
                         "t": to_iast(g).strip()})
            continue
        toks = tokenize(g)
        p1t, p2t, halfn = split_half_padas(toks)
        p1_ia = to_iast(join(p1t)).strip()
        p2_ia = to_iast(join(p2t)).strip()
        total += halfn
        if pidx < 4 and pidx in words and (pidx + 1) in words:
            wA = words.get(pidx, [])
            wB = words.get(pidx + 1, [])
            if wA and wB:
                p1_ia, p2_ia = snap_pair(p1_ia, p2_ia, wA[-1][1], wB[0][1])
        d1 = iast_to_deva(p1_ia).strip()
        d2 = iast_to_deva(p2_ia).strip()
        # A pāda boundary can fall *inside* a word: the metre breaks mid-compound,
        # e.g. 16.1  sattvasaṃśuddhir | jñānayogavyavasthitiḥ. When the first half
        # ends on a virāma (halanta) the consonant must join what follows, so the
        # display must NOT insert a space. Record it here — the renderer cannot
        # tell, and a space would break the word.
        joins = d1.endswith("\u094d")
        flow.append({"k": "p", "d": d1, "t": p1_ia, "n": syll_iast(p1_ia), "j": 1 if joins else 0})
        flow.append({"k": "p", "d": d2, "t": p2_ia, "n": syll_iast(p2_ia)})
        pidx += 2

    padas = [x for x in flow if x["k"] == "p"]
    speakers = [x for x in flow if x["k"] == "s"]
    n = len(padas)
    if total == 32: meter = "anuṣṭubh · 32 syllables · 4 pādas of 8"
    elif total == 44: meter = "triṣṭubh · 44 syllables · 4 pādas of 11"
    elif total == 22 and n == 2: meter = "triṣṭubh · 22 syllables · 2 pādas of 11"
    elif total == 33 and n == 4: meter = "anuṣṭubh (irregular) · 33 syllables · 4 pādas"
    else: meter = f"{total} syllables · {n} pādas"
    # structured form so the app can render the badge in en/ne/hi at runtime.
    # name: '' | 'anustubh' | 'trishtubh';  irr: irregular flag;  per: syllables
    # per pāda (0 = uneven, so the "of N" clause is dropped).
    if total == 32:            mt = {"name": "anustubh",  "irr": 0, "total": 32,    "n": 4, "per": 8}
    elif total == 44:          mt = {"name": "trishtubh", "irr": 0, "total": 44,    "n": 4, "per": 11}
    elif total == 22 and n == 2: mt = {"name": "trishtubh", "irr": 0, "total": 22,  "n": 2, "per": 11}
    elif total == 33 and n == 4: mt = {"name": "anustubh", "irr": 1, "total": 33,   "n": 4, "per": 0}
    else:                      mt = {"name": "",          "irr": 0, "total": total, "n": n, "per": 0}
    return {"flow": flow, "padas": padas, "speakers": speakers, "total": total, "meter": meter, "mt": mt}
