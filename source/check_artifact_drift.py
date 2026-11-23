# -*- coding: utf-8 -*-
"""check_artifact_drift.py — prove the committed tree reproduces itself.

`AGENTS.md` states the rule: generated output is never hand-edited; you change
`source/`, rebuild, and keep the resulting output diff with its source. Nothing
enforced the second half. PR #98 (2026-11-23) changed `शोभादैन` → `शोभा दिँदैन`
and `शत्रुतापन` → `शत्रुतापक` in `source/ch{2,4,7,9,10,18}.json` and regenerated
the chapter pages, but never rebuilt `data/ch*.js`. CI stayed green, because
`build.py` regenerates `data/` in the runner and then tests the *fresh* copy —
it never compared that copy with what was committed. The static chapter pages
said शत्रुतापक while the app shell still said शत्रुतापन: the same verse, two
answers, and the wrong one on the reader's phone.

The test
--------
Run after a build, with `source/` clean. Every generated artifact on disk is
then exactly what the committed sources produce, so comparing each one against
its committed copy answers the only question that matters:

    does the commit reproduce itself, byte for byte?

A difference means the committed artifact and the committed source disagree — a
reader gets one text from the static page and another from the app. Nothing is
inferred from "the tree is dirty": an uncommitted artifact edit is not drift
(the build overwrites it), and an uncommitted source edit is not judged at all,
because a contributor halfway through an edit is not a defect. In that case the
check says so and passes.

Two artifacts are deliberately left out, for stated reasons rather than
convenience:

- `sw.js` carries a version hash over the other artifacts, so it is only ever a
  symptom of their drift, never a cause of its own.
- `sitemap.xml` stamps each page with the date of the commit that last touched
  it (`_lastmod`), a date that cannot exist before the commit is made. It is
  therefore always one commit behind itself and can never match pre-commit.
  It also carries no reader-visible text: a stale date there cannot show the
  wrong scripture to anyone, unlike a stale `data/ch*.js` or chapter page.

Neither omission needs full history, so this check is shallow-clone safe:
`git show HEAD:<path>` reads the tree of the checked-out commit.

Exit status: 0 clean (or nothing provable), 1 drift.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ARTIFACT_FILES = ["index.html", "chapter.css", "robots.txt", "404.html",
                  "manifest.webmanifest"]
ARTIFACT_DIRS = ["data", "chapter", "method"]
SUFFIXES = (".html", ".js", ".txt", ".webmanifest")
# Excluded on purpose — see the module docstring: sw.js is a hash over the
# others (a symptom), sitemap.xml stamps commit dates that do not exist yet.
EXCLUDED = {"sw.js", "sitemap.xml"}


def git(*args):
    """Run git in the project root. Returns (ok, stdout) — never raises."""
    try:
        p = subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True,
                           timeout=120)
        return p.returncode == 0, p.stdout
    except Exception:
        return False, b""


def artifacts():
    """Every generated file that has a committed copy, repo-relative."""
    paths = []
    for name in ARTIFACT_FILES:
        if os.path.exists(os.path.join(ROOT, name)):
            paths.append(name)
    for d in ARTIFACT_DIRS:
        for dirpath, _, files in os.walk(os.path.join(ROOT, d)):
            for f in files:
                if f.endswith(SUFFIXES):
                    rel = os.path.relpath(os.path.join(dirpath, f), ROOT)
                    paths.append(rel.replace(os.sep, "/"))
    return sorted(set(paths))


def main():
    if not git("rev-parse", "--is-inside-work-tree")[0]:
        print("artifact drift: SKIPPED — not a git work tree")
        return 0

    # Uncommitted source edits make this comparison meaningless: the build
    # reflects work in progress, not the commit. Say so and stay out of the way.
    _, dirty_src = git("status", "--porcelain", "--untracked-files=all", "--",
                       "source/")
    if dirty_src.strip():
        n = len([l for l in dirty_src.decode().splitlines() if l.strip()])
        print(f"artifact drift: SKIPPED — {n} source file(s) have uncommitted "
              f"edits, so the build does not represent the commit yet")
        return 0

    if git("rev-parse", "--is-shallow-repository")[1].strip() == b"true":
        print("artifact drift: (shallow clone — fine here: this compares "
              "against the checked-out tree, not against history)")

    drift, checked = [], 0
    for rel in artifacts():
        ok, committed = git("show", f"HEAD:{rel}")
        if not ok:
            continue                      # new/untracked artifact: nothing to compare
        checked += 1
        with open(os.path.join(ROOT, rel), "rb") as fh:
            if fh.read() != committed:
                drift.append(rel)

    if not drift:
        print(f"artifact drift: {checked} generated files reproduce from their "
              f"committed source, byte for byte")
        return 0

    print(f"\nartifact drift: {len(drift)} of {checked} committed artifacts are "
          f"BEHIND their source:")
    for rel in drift:
        print(f"  - {rel}")
    print("\nThe committed artifact and the committed `source/` disagree, so the "
          "static pages and the app show different text. Rebuild and commit the "
          "output with its source (AGENTS.md: 'keep the resulting output diff "
          "with its source'):")
    print("\n    python3 build.py && git add -A && git commit\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
