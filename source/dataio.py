# -*- coding: utf-8 -*-
"""dataio.py — read and write the source data files safely.

Every editable thing in the app lives in a plain Python dict or a JSON file.
This module loads them, lets you change them, and writes them back.

THE SAFETY RULES (learned the hard way — a regex-based edit once wrote one
verse's words onto another verse):

  1. Never patch file text with a regex. Import the module, get the real dict,
     change it, and re-emit the WHOLE file from that dict.
  2. Back up the file before overwriting, into source/.backup/.
  3. After writing, re-import and compare. If the file no longer parses, or the
     data does not match what we meant to write, restore the backup and raise.

Nothing here validates meaning — that is the build's job. This module only
guarantees that what you asked to store is exactly what ends up on disk.
"""
import importlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(HERE, ".backup")
if HERE not in sys.path:
    sys.path.insert(0, HERE)


# ---------------------------------------------------------------- helpers ---
def _esc(x):
    return str(x).replace("\\", "\\\\").replace('"', '\\"')


def _fresh(modname):
    """Import a module, discarding any cached copy."""
    if modname in sys.modules:
        del sys.modules[modname]
    return importlib.import_module(modname)


def _backup(path):
    os.makedirs(BACKUP, exist_ok=True)
    if os.path.exists(path):
        shutil.copy2(path, os.path.join(BACKUP, os.path.basename(path)))


def _restore(path):
    b = os.path.join(BACKUP, os.path.basename(path))
    if os.path.exists(b):
        shutil.copy2(b, path)


def _write_verified(path, text, modname, attr, expect):
    """Write text, then re-import and confirm the data matches `expect`."""
    _backup(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    try:
        got = getattr(_fresh(modname), attr)
        if got != expect:
            raise ValueError(f"{os.path.basename(path)}: written data does not match")
    except Exception:
        _restore(path)
        _fresh(modname)
        raise


# ------------------------------------------------------------ ch*.json ------
def load_verses(ch):
    p = os.path.join(HERE, f"ch{ch}.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)["verses"]


def save_verse(ch, vno, deva, iast):
    """Update one verse's Devanagari and IAST in ch*.json."""
    p = os.path.join(HERE, f"ch{ch}.json")
    with open(p, encoding="utf-8") as f:
        doc = json.load(f)
    key = str(int(vno))
    if key not in doc["verses"]:
        raise KeyError(f"ch{ch}.json has no verse {key}")
    doc["verses"][key]["deva"] = deva.strip()
    doc["verses"][key]["iast"] = iast.strip()
    _backup(p)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(p, encoding="utf-8") as f:
        back = json.load(f)["verses"][key]
    if back["deva"] != deva.strip() or back["iast"] != iast.strip():
        _restore(p)
        raise ValueError("verse write-back mismatch")


# --------------------------------------------------------- padas_ch*.py -----
def load_padas(ch):
    return getattr(_fresh(f"padas_ch{ch}"), f"GITA_CH{ch}_PADAS")


def save_padas(ch, data):
    """data: {"17.28": [("p", deva, iast, n) | ("s", deva, iast), ...], ...}"""
    modname = f"padas_ch{ch}"
    path = os.path.join(HERE, f"{modname}.py")
    head = open(path, encoding="utf-8").read().split(f"GITA_CH{ch}_PADAS = {{")[0]
    out = [head, f"GITA_CH{ch}_PADAS = {{\n"]
    for ref in sorted(data, key=lambda r: int(r.split(".")[1])):
        out.append(f'"{ref}": [\n')
        for row in data[ref]:
            if row[0] == "p":
                out.append(f'    ("p", "{_esc(row[1])}", "{_esc(row[2])}", {int(row[3])}),\n')
            else:
                out.append(f'    ("s", "{_esc(row[1])}", "{_esc(row[2])}"),\n')
        out.append("],\n\n")
    out.append("}\n")
    expect = {r: [tuple(x) for x in rows] for r, rows in data.items()}
    _write_verified(path, "".join(out), modname, f"GITA_CH{ch}_PADAS", expect)


# ---------------------------------------------------- padachheda_ch*.py -----
def load_words(ch):
    return getattr(_fresh(f"padachheda_ch{ch}"), f"GITA_CH{ch}_WORDS")


def save_words(ch, data):
    """data: {verse_no: {"s": [[d,i,en],...], 0..3: [[d,i,en],...]}}"""
    modname = f"padachheda_ch{ch}"
    path = os.path.join(HERE, f"{modname}.py")
    head = open(path, encoding="utf-8").read().split(f"GITA_CH{ch}_WORDS = {{")[0]
    out = [head, f"GITA_CH{ch}_WORDS = {{\n"]

    def wl(lst, ind):
        if not lst:
            return ""
        return (",\n" + " " * ind).join(
            "[" + ", ".join(f'"{_esc(c)}"' for c in w) + "]" for w in lst)

    for vno in sorted(data, key=lambda k: int(k)):
        d = data[vno]
        out.append(f'{int(vno)}: {{"s": [' + wl(d.get("s", []), 10) + "],\n")
        for k in range(4):
            out.append(f"    {k}: [" + wl(d.get(k, d.get(str(k), [])), 8) + "]"
                       + ("," if k < 3 else "}") + "\n")
        out.append("\n")
    out.append("}\n")
    text = "".join(out).replace("}\n\n", "},\n\n")
    expect = {int(v): {(k if k == "s" else int(k)): [list(w) for w in ws]
                       for k, ws in d.items()} for v, d in data.items()}
    _write_verified(path, text, modname, f"GITA_CH{ch}_WORDS", expect)


# ------------------------------------------- gloss_ne.py / gloss_hi.py ------
def load_gloss(lang):
    return getattr(_fresh(f"gloss_{lang}"), f"GLOSS_{lang.upper()}")


def save_gloss(lang, data):
    modname = f"gloss_{lang}"
    path = os.path.join(HERE, f"{modname}.py")
    head = open(path, encoding="utf-8").read().split(f"GLOSS_{lang.upper()} = {{")[0]
    out = [head, f"GLOSS_{lang.upper()} = {{\n"]
    for k in sorted(data):
        out.append(f'"{_esc(k)}": "{_esc(data[k])}",\n')
    out.append("}\n")
    _write_verified(path, "".join(out), modname, f"GLOSS_{lang.upper()}", dict(data))


# ------------------------------- translations_ne.py / translations_hi.py ----
def load_trans(lang):
    return getattr(_fresh(f"translations_{lang}"), f"TRANS_{lang.upper()}")


def save_trans(lang, data):
    """data: {"1.01": (literal, paraphrase), ...}"""
    modname = f"translations_{lang}"
    path = os.path.join(HERE, f"{modname}.py")
    head = open(path, encoding="utf-8").read().split(f"TRANS_{lang.upper()} = {{")[0]
    out = [head, f"TRANS_{lang.upper()} = {{\n"]
    for ref in sorted(data, key=lambda r: (int(r.split(".")[0]), int(r.split(".")[1]))):
        lit, para = data[ref]
        out.append(f'"{ref}": ("{_esc(lit)}",\n         "{_esc(para)}"),\n')
    out.append("}\n")
    expect = {r: tuple(v) for r, v in data.items()}
    _write_verified(path, "".join(out), modname, f"TRANS_{lang.upper()}", expect)


# ----------------------------------- themes_ne.py / themes_hi.py ------------
def load_themes_i18n(lang):
    return getattr(_fresh(f"themes_{lang}"), f"THEMES_{lang.upper()}")


def save_themes_i18n(lang, data):
    """data: {ch: [(title, desc, [(ptitle, pdesc, start, end), ...]), ...]}"""
    modname = f"themes_{lang}"
    NAME = f"THEMES_{lang.upper()}"
    path = os.path.join(HERE, f"{modname}.py")
    head = open(path, encoding="utf-8").read().split(f"{NAME} = {{")[0]
    out = [head, f"{NAME} = {{\n"]
    for ch in sorted(data, key=int):
        out.append(f"{int(ch)}: [\n")
        for (title, desc, parts) in data[ch]:
            out.append(f' ("{_esc(title)}", "{_esc(desc)}",\n  [')
            out.append(",\n   ".join(
                f'("{_esc(a)}", "{_esc(b)}", "{_esc(c)}", "{_esc(d)}")'
                for (a, b, c, d) in parts))
            out.append("]),\n")
        out.append("],\n")
    out.append("}\n")
    expect = {int(c): [(t, d, [tuple(p) for p in ps]) for (t, d, ps) in v]
              for c, v in data.items()}
    _write_verified(path, "".join(out), modname, NAME, expect)


# ------------------------------------------------- gita_data*.py (English) --
def _gd(ch):
    return "gita_data" if int(ch) == 1 else f"gita_data{int(ch)}"


def load_themes_en(ch):
    return getattr(_fresh(_gd(ch)), f"CH{int(ch)}_THEMES")


def load_trans_en(ch):
    return getattr(_fresh(_gd(ch)), f"CH{int(ch)}_TRANSLATIONS")


def save_gita_data(ch, themes, translations):
    """Rewrite the THEMES and TRANSLATIONS blocks of gita_data*.py, keeping
    everything else in the file (chapter 1 also holds CHAPTERS) untouched."""
    ch = int(ch)
    modname = _gd(ch)
    path = os.path.join(HERE, f"{modname}.py")
    src = open(path, encoding="utf-8").read()

    tkey, xkey = f"CH{ch}_THEMES = [", f"CH{ch}_TRANSLATIONS = {{"
    ti, xi = src.index(tkey), src.index(xkey)
    tend = src.index("\n]\n", ti) + 3
    xend = src.index("\n}\n", xi) + 3

    tblock = [f"CH{ch}_THEMES = [\n"]
    for (title, desc, parts) in themes:
        tblock.append(f'    ("{_esc(title)}",\n     "{_esc(desc)}",\n     [')
        tblock.append(",\n      ".join(
            f'("{_esc(a)}", "{_esc(b)}", "{_esc(c)}", "{_esc(d)}")'
            for (a, b, c, d) in parts))
        tblock.append("]),\n")
    tblock.append("]\n")

    xblock = [f"CH{ch}_TRANSLATIONS = {{\n"]
    for n in sorted(translations, key=int):
        lit, para = translations[n]
        xblock.append(f'{int(n)}: ("{_esc(lit)}",\n    "{_esc(para)}"),\n')
    xblock.append("}\n")

    if ti < xi:
        new = src[:ti] + "".join(tblock) + src[tend:xi] + "".join(xblock) + src[xend:]
    else:
        new = src[:xi] + "".join(xblock) + src[xend:ti] + "".join(tblock) + src[tend:]

    _backup(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    try:
        m = _fresh(modname)
        got_t = [(t, d, [tuple(p) for p in ps])
                 for (t, d, ps) in getattr(m, f"CH{ch}_THEMES")]
        want_t = [(t, d, [tuple(p) for p in ps]) for (t, d, ps) in themes]
        got_x = {int(k): tuple(v) for k, v in getattr(m, f"CH{ch}_TRANSLATIONS").items()}
        want_x = {int(k): tuple(v) for k, v in translations.items()}
        if got_t != want_t or got_x != want_x:
            raise ValueError(f"{modname}.py: written data does not match")
    except Exception:
        _restore(path)
        _fresh(modname)
        raise


# -------------------------------------------------- i18n_chapters / ui ------
def load_chapter_i18n():
    m = _fresh("i18n_chapters")
    return {"names_ne": m.CHAPTER_NAMES_NE, "names_hi": m.CHAPTER_NAMES_HI,
            "subs_ne": m.CHAPTER_SUBS_NE, "subs_hi": m.CHAPTER_SUBS_HI}


def save_chapter_i18n(d):
    path = os.path.join(HERE, "i18n_chapters.py")
    head = open(path, encoding="utf-8").read().split("CHAPTER_NAMES_NE = {")[0]
    out = [head]
    for var, key in (("CHAPTER_NAMES_NE", "names_ne"), ("CHAPTER_NAMES_HI", "names_hi"),
                     ("CHAPTER_SUBS_NE", "subs_ne"), ("CHAPTER_SUBS_HI", "subs_hi")):
        out.append(f"{var} = {{\n")
        for n in sorted(d[key], key=int):
            out.append(f' {int(n)}: "{_esc(d[key][n])}",\n')
        out.append("}\n\n")
    _backup(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(out))
    try:
        m = _fresh("i18n_chapters")
        for var, key in (("CHAPTER_NAMES_NE", "names_ne"), ("CHAPTER_NAMES_HI", "names_hi"),
                         ("CHAPTER_SUBS_NE", "subs_ne"), ("CHAPTER_SUBS_HI", "subs_hi")):
            if {int(k): v for k, v in getattr(m, var).items()} != \
               {int(k): v for k, v in d[key].items()}:
                raise ValueError("i18n_chapters.py: written data does not match")
    except Exception:
        _restore(path)
        _fresh("i18n_chapters")
        raise


def load_ui():
    return _fresh("i18n_ui").UI


def save_ui(ui):
    path = os.path.join(HERE, "i18n_ui.py")
    src = open(path, encoding="utf-8").read()
    head = src.split("UI = {")[0]
    tail = src[src.index("\n}\n", src.index("UI = {")) + 3:]
    out = [head, "UI = {\n"]
    for lang in ("en", "ne", "hi"):
        out.append(f' "{lang}": {{\n')
        for k, v in ui[lang].items():
            out.append(f'  "{_esc(k)}": "{_esc(v)}",\n')
        out.append(" },\n")
    out.append("}\n")
    _write_verified(path, "".join(out) + tail, "i18n_ui", "UI",
                    {l: dict(ui[l]) for l in ui})
