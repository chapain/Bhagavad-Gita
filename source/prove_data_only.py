# -*- coding: utf-8 -*-
"""prove_data_only.py — prove the app publishes the chapter data as written.

Run this whenever you want to re-confirm that editing a content field is enough:

    python3 source/prove_data_only.py

For each kind of content it makes one temporary edit, rebuilds, and checks that
its marker reached the published shell or chapter payload. Each file is restored
byte-for-byte, and the final build must return to the original artifact hash.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable or "python3"
INDEX = os.path.join(ROOT, "index.html")
DATA_DIR = os.path.join(ROOT, "data")
MARK = "PROOF-DATA-WINS"


def artifacts():
    paths = [INDEX] + [os.path.join(DATA_DIR, f"ch{n}.js") for n in range(1, 19)]
    return [p for p in paths if os.path.exists(p)]


def artifact_text():
    return "".join(open(p, encoding="utf-8").read() for p in artifacts())


def digest():
    h = hashlib.sha256()
    for path in artifacts():
        with open(path, "rb") as f:
            h.update(f.read())
    return h.hexdigest()[:12]


def build():
    result = subprocess.run([PY, "build.py", "--fast"], cwd=ROOT,
                            capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr


def verses(chapter):
    return [v for theme in chapter["themes"]
            for part in theme["parts"] for v in part["sutras"]]


def chapter_case(number, label, edit):
    """Return a case that edits one chapter JSON record and restores its bytes."""
    def run_case():
        path = os.path.join(HERE, f"ch{number}.json")
        original = open(path, "rb").read()
        try:
            chapter = json.loads(original)
            edit(chapter)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(chapter, f, ensure_ascii=False, indent=2)
                f.write("\n")
            built, output = build()
            shown = built and MARK in artifact_text()
            moved = digest() != BASELINE
            return built and shown and moved, (
                "edit appeared in the published chapter data" if shown
                else ("build failed: " + output[-800:] if not built
                      else "edit did NOT appear in the published artifacts"))
        finally:
            with open(path, "wb") as f:
                f.write(original)
    return label, run_case


def prepend_to_verse(chapter, ref, field, value):
    verse = next(v for v in verses(chapter) if v["n"] == ref)
    old = verse[field]
    verse[field] = value + old


def update_word(chapter, ref, old, replacement):
    verse = next(v for v in verses(chapter) if v["n"] == ref)
    for segment in verse["flow"]:
        for word in segment.get("words", []):
            if word[2] == old:
                word[2] = replacement
                return
    raise ValueError(f"{ref}: word gloss {old!r} not found")


CASES = []
CASES.append(chapter_case(16, "the verse text", lambda c:
    prepend_to_verse(c, "16.03", "d", MARK + " ")))
CASES.append(chapter_case(16, "a pāda in the popup", lambda c:
    next(p for p in next(v for v in verses(c) if v["n"] == "16.03")["flow"]
         if p["k"] == "p").__setitem__("d", MARK)))
CASES.append(chapter_case(16, "a word meaning", lambda c:
    update_word(c, "16.03", "vigour", MARK)))
CASES.append(chapter_case(16, "an English translation", lambda c:
    next(v for v in verses(c) if v["n"] == "16.03")["lits"].__setitem__("en", MARK)))
CASES.append(chapter_case(16, "a Nepali translation", lambda c:
    next(v for v in verses(c) if v["n"] == "16.03")["lits"].__setitem__("ne", MARK)))
CASES.append(chapter_case(16, "a Hindi theme title", lambda c:
    c["themes"][0]["titles"].__setitem__("hi", MARK)))
CASES.append(chapter_case(16, "a chapter name", lambda c:
    c["names"].__setitem__("hi", MARK)))


def edit_ui():
    path = os.path.join(HERE, "i18n_ui.py")
    original = open(path, "rb").read()
    old = b'"literal": "Literal"'
    if original.count(old) != 1:
        raise RuntimeError("could not uniquely locate the English UI string")
    try:
        with open(path, "wb") as f:
            f.write(original.replace(old, b'"literal": "' + MARK.encode() + b'"', 1))
        built, output = build()
        shown = built and MARK in artifact_text()
        moved = digest() != BASELINE
        return built and shown and moved, (
            "edit appeared in the published shell" if shown
            else ("build failed: " + output[-800:] if not built
                  else "edit did NOT appear in the published artifacts"))
    finally:
        with open(path, "wb") as f:
            f.write(original)


def main():
    global BASELINE
    ok, output = build()
    if not ok:
        sys.exit("the project does not currently build:\n" + output[-1500:])
    BASELINE = digest()
    print(f"baseline build (index.html + data/) = {BASELINE}\n")

    results = []
    for label, run_case in CASES:
        try:
            passed, detail = run_case()
        except Exception as exc:
            passed, detail = False, f"{type(exc).__name__}: {exc}"
        results.append((label, passed, detail))
    try:
        passed, detail = edit_ui()
    except Exception as exc:
        passed, detail = False, f"{type(exc).__name__}: {exc}"
    results.append(("interface wording", passed, detail))

    built, output = build()
    final = digest() if built else "build failed"
    print("=" * 68)
    allok = built
    for label, passed, detail in results:
        print(f"  {'PASS' if passed else 'FAIL'}  {label}")
        if not passed:
            print(f"        {detail}")
        allok &= passed
    print(f"\n  restored build = {final} "
          f"({'matches baseline' if final == BASELINE else 'DOES NOT MATCH — investigate'})")
    allok &= final == BASELINE
    print("=" * 68)
    print("\nCONCLUSION: each chapter's source JSON and the UI dictionary are published "
          "as written." if allok else "\nSOMETHING IS WRONG — see the FAIL lines above.")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
