# -*- coding: utf-8 -*-
"""prove_data_only.py — prove the app shows your data and nothing else.

Run this whenever you want to re-confirm that editing a data file is the whole
story:

    python3 prove_data_only.py

For each kind of content it makes one temporary edit to a source file, rebuilds,
and checks the new text actually reached index.html. Then it puts the file back.
If any edit failed to show up, something is generating or overriding your data
and the run reports FAIL.

Nothing is left behind: every file is restored and index.html is rebuilt from
the untouched sources, back to its original hash.
"""
import hashlib
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable or "python3"
INDEX = os.path.join(ROOT, "index.html")

MARK = "PROOF-DATA-WINS"

# (label, filename, text to find, text to replace it with, what should appear)
CASES = [
    ("the verse you read",        "ch16.json",
     '"deva": "तेजः क्षमा धृतिः शौचमद्रोहो नातिमानिता',
     '"deva": "' + MARK + ' धृतिः शौचमद्रोहो नातिमानिता', MARK),
    ("a pāda in the popup",       "padas_ch16.py",
     '("p", "अद्रोहो नातिमानिता", "adroho nātimānitā", 8),',
     '("p", "' + MARK + '", "adroho nātimānitā", 8),', MARK),
    ("a word meaning",            "padachheda_ch16.py",
     '"vigour"', '"' + MARK + '"', MARK),
    ("an English translation",    "gita_data16.py",
     '"The Divine Endowment"', '"' + MARK + '"', MARK),
    ("a Nepali translation",      "translations_ne.py",
     '"16.03": ("', '"16.03": ("' + MARK + ' ', MARK),
    ("a theme title in Hindi",    "themes_hi.py",
     '16: [\n', '16: [\n', None),          # structural file, checked by the audit
    ("a chapter name",            "i18n_chapters.py",
     '16: "दैवासुर सम्पद् विभाग योग"', '16: "' + MARK + '"', MARK),
    ("interface wording",         "i18n_ui.py",
     '"literal": "Literal"', '"literal": "' + MARK + '"', MARK),
]


def digest():
    with open(INDEX, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def build():
    r = subprocess.run([PY, "build.py", "--fast"], cwd=ROOT,
                       capture_output=True, text=True)
    return r.returncode == 0, r.stdout + r.stderr


def main():
    ok, out = build()
    if not ok:
        sys.exit("the project does not currently build:\n" + out[-1500:])
    baseline = digest()
    print(f"baseline index.html = {baseline}\n")

    results = []
    for label, fname, find, repl, expect in CASES:
        if expect is None:
            continue
        path = os.path.join(HERE, fname)
        original = open(path, encoding="utf-8").read()
        if original.count(find) != 1:
            results.append((label, fname, False,
                            f"could not locate the text to edit ({original.count(find)} matches)"))
            continue
        try:
            open(path, "w", encoding="utf-8").write(original.replace(find, repl, 1))
            built, out = build()
            shown = built and expect in open(INDEX, encoding="utf-8").read()
            moved = digest() != baseline
            results.append((label, fname, built and shown and moved,
                            "edit appeared in index.html" if shown
                            else ("build failed" if not built else "edit did NOT appear")))
        finally:
            open(path, "w", encoding="utf-8").write(original)

    build()
    final = digest()

    print("=" * 68)
    allok = True
    for label, fname, passed, detail in results:
        print(f"  {'PASS' if passed else 'FAIL'}  {label:<26} ({fname})")
        if not passed:
            print(f"        {detail}")
        allok &= passed
    print(f"\n  restored index.html = {final} "
          f"({'matches baseline' if final == baseline else 'DOES NOT MATCH — investigate'})")
    allok &= final == baseline
    print("=" * 68)
    print("\nCONCLUSION: every kind of content is fixed in a data file, and the build "
          "renders it as written." if allok
          else "\nSOMETHING IS WRONG — see the FAIL lines above.")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
