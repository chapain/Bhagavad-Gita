# -*- coding: utf-8 -*-
"""sandhi.py — external sandhi joiner for Devanagari (used to join pada-chheda words
back into the verse's written form, matching the source text readings)."""

VOW = "अआइईउऊऋॠऌॡएऐओऔ"
SIGN = "ािीुूृॄेैोौ"
CONS = "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ"
SIGN_VOW = {"ा":"आ","ि":"इ","ी":"ई","ु":"उ","ू":"ऊ","ृ":"ऋ","ॄ":"ॠ","े":"ए","ै":"ऐ","ो":"ओ","ौ":"औ"}
VOW_SIGN = {"अ":"","आ":"ा","इ":"ि","ई":"ी","उ":"ु","ऊ":"ू","ऋ":"ृ","ॠ":"ॄ","ए":"े","ऐ":"ै","ओ":"ो","औ":"ौ"}

def _final_vowel(a):
    """return (final_vowel, consonant_before) or (None, None) if ends in consonant/virāma."""
    if not a: return None, None
    c = a[-1]
    if c in SIGN:
        return SIGN_VOW[c], (a[-2] if len(a) > 1 else "")
    if c in VOW:
        return c, ""
    return None, None  # ends in consonant (implicit a) or virāma

def _join_vowel_sandhi(a, b):
    """a ends in a vowel (sign or independent); b starts with a vowel."""
    fv, cons = _final_vowel(a)
    # b's leading vowel
    bv = b[0]
    if bv in SIGN:  # shouldn't happen
        return a + " " + b
    # strip leading vowel of b (keep rest)
    brest = b[1:] if bv in VOW else b

    def out(newvow):  # rebuild a with new final vowel, then brest
        if cons:
            return a[:-1] + VOW_SIGN.get(newvow, "") + brest
        return a[:-1] + newvow + brest

    # ---- आ (ā) + vowel (sign ा or independent आ) ----
    if fv == "आ":
        if bv == "अ": return out("आ")
        if bv == "आ": return out("आ")
        if bv == "इ": return out("ए")     # ā+i → e (as in this text: dṛṣṭvā+imam → dṛṣṭvemam)
        if bv == "ई": return out("ए")
        if bv == "उ": return out("ओ")
        if bv == "ऊ": return out("ओ")
        if bv == "ऋ": return out("अर्")
        if bv == "ए": return out("ऐ")
        if bv == "ओ": return out("औ")
        return a + " " + b
    # ---- अ (a) + vowel ----
    if fv == "अ":
        if bv == "अ": return out("आ")
        if bv == "आ": return out("आ")
        if bv == "इ": return out("ए")
        if bv == "ई": return out("ए")
        if bv == "उ": return out("ओ")
        if bv == "ऊ": return out("ओ")
        if bv == "ऋ": return out("अर्")
        if bv == "ए": return out("ऐ")
        if bv == "ऐ": return out("ऐ")
        if bv == "ओ": return out("औ")
        if bv == "औ": return out("औ")
        return a + " " + b
    # ---- इ/ई (i/ī) + vowel ----
    if fv in ("इ","ई"):
        if bv == "अ": return out("य")
        if bv == "आ": return out("या")
        if bv in ("इ","ई"): return out("ई")   # i+i → ī (as written: bhavati+iti → bhavatīti)
        if bv == "उ": return out("यु")
        if bv == "ऊ": return out("यू")
        if bv == "ऋ": return out("यृ")
        if bv == "ए": return out("ये")
        if bv == "ऐ": return out("यै")
        if bv == "ओ": return out("यो")
        if bv == "औ": return out("यौ")
        return a + " " + b
    # ---- उ/ऊ (u/ū) + vowel ----
    if fv in ("उ","ऊ"):
        if bv == "अ": return out("व")
        if bv == "आ": return out("वा")
        if bv in ("उ","ऊ"): return out("ऊ")
        if bv == "ऋ": return out("वृ")
        if bv == "ए": return out("वे")
        if bv == "ऐ": return out("वै")
        if bv == "ओ": return out("वो")
        if bv == "औ": return out("वौ")
        return a + " " + b
    # ---- ऋ/ॠ (ṛ) + vowel ----
    if fv in ("ऋ","ॠ"):
        if bv == "अ": return out("र")
        if bv == "आ": return out("रा")
        if bv in ("ऋ","ॠ"): return out("ऋ")
        return a + " " + b
    # ---- ए (e) + vowel ----
    if fv == "ए":
        if bv == "अ": return a + "ऽ" + brest       # e+a → e' (avagraha): me+acyuta → me'cyuta
        if bv == "ए": return out("ए")
        if bv == "ऐ": return out("ऐ")
        if bv == "आ": return a + brest             # e+ā → e+ā
        if bv == "इ": return out("ए")
        return a + " " + b
    # ---- ओ (o) + vowel ----
    if fv == "ओ":
        if bv == "अ": return a + "ऽ" + brest
        if bv == "ओ": return out("ओ")
        return a + " " + b
    # ---- ऐ (ai) + vowel ----
    if fv == "ऐ":
        if bv == "अ": return out("आ")
        if bv == "ऐ": return out("ऐ")
        if bv == "आ": return out("आ")
        return a + " " + b
    # ---- औ (au) + vowel ----
    if fv == "औ":
        if bv == "अ": return out("आ")
        return a + " " + b
    return a + " " + b

def _join_visarga(a, b):
    base = a[:-1]
    bv = b[0]
    # visarga before a vowel → र् + vowel (or ओऽ for अ after उ/ऊ — handled below)
    if bv in VOW:
        # o' occurs when visarga follows उ/ऊ/ओ and next is अ
        prev = a[-2] if len(a) > 1 else ""
        if bv == "अ" and prev in "ुूो" or (bv == "अ" and prev == "" and False):
            return base + "ो" + "ऽ" + b[1:]
        if bv == "अ" and prev in "ो":  # o + ḥ + a
            return base + "ो" + "ऽ" + b[1:]
        return base + "र्" + b
    # visarga before a voiced consonant → ओ (in this text's readings: hṛṣīkeśo devadattaṃ)
    if bv in "गघजझडढदधबभयरलवह":
        return base + "ो" + b
    # visarga before क/ख/प/फ → स् ; च/छ → श् ; ट/ठ → ष् ; त/थ → स् (text usually keeps visarga though)
    if bv in "कखपफतथचछटठस":
        return base + "स्" + b
    # otherwise keep
    return a + " " + b

def _join_viccheda(a, b):
    """a ends in a consonant with virāma (्)."""
    base = a[:-2] if len(a) >= 2 and a[-1] == "्" else a[:-1]
    lastc = a[-2] if len(a) >= 2 and a[-1] == "्" else a[-1]
    bv = b[0]
    # म् handled elsewhere; here non-m virāma consonants
    if bv in VOW:
        # t/n before vowel → d/n (voiced), as in yāvat+etān → yāvadetān
        if lastc == "त्"[-1] and a.endswith("त्"):
            return a[:-2] + "द्" + b
        if a.endswith("न्"):
            return a + b      # n stays before vowel? sarvān+... keep n+space? text: sarvAnbandhUn joined
        if a.endswith("क्"):
            return a + b
        return a + b
    # consonant + consonant: join without space (compounds), keep virāma
    return a + b  # e.g. pṛthak+pṛthak → pṛthakpṛthak; sarvān+bandhūn → sarvānbandhūn

def join_dev(a, b):
    if not a: return b
    if not b: return a
    # final म्
    if a.endswith("म्"):
        base = a[:-2]
        if b[0] in VOW:
            return base + "म" + VOW_SIGN[b[0]] + b[1:]
        return base + "ं " + b
    # final visarga
    if a.endswith("ः"):
        return _join_visarga(a, b)
    # final consonant with virāma (non-m)
    if a.endswith("्") and len(a) >= 2:
        return _join_viccheda(a, b)
    # final vowel (sign or independent)
    fv, cons = _final_vowel(a)
    if fv is not None:
        if b[0] in VOW:
            return _join_vowel_sandhi(a, b)
        # vowel + consonant: join without space in compounds (pāṇḍu+putrāṇām → pāṇḍuputrāṇām)
        return a + b
    # final consonant (implicit अ)
    if a[-1] in CONS:
        if b[0] in VOW:
            # implicit a + vowel → sign coalescence
            return a + VOW_SIGN[_a_plus(b[0])] + b[1:]
        return a + b   # consonant + consonant → join (compound)
    return a + " " + b

def _a_plus(v):
    return {"अ":"आ","आ":"आ","इ":"ए","ई":"ए","उ":"ओ","ऊ":"ओ","ऋ":"अर्","ए":"ऐ","ऐ":"ऐ","ओ":"औ","औ":"औ"}[v]

def join_words(words):
    """Join a list of Devanagari words with external sandhi (in order)."""
    out = words[0]
    for w in words[1:]:
        out = join_dev(out, w)
    return out
