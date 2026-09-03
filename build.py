#!/usr/bin/env python3
"""build.py — rebuild the app and verify it. Cross-platform alternative to rebuild.sh.

Use this from an IDE (Antigravity, VS Code, PyCharm…) where a .sh file cannot be
launched directly: just press Run on this file, or:

    python3 build.py            build + verify   (what you normally want)
    python3 build.py --fast     build only, skip the tests
    python3 build.py --serve    build, verify, then serve locally at :8000

It runs, in order:
    1. source/build_gita.py   regenerates index.html from source/
    2. source/check_padas.py  verifies every pāda reconstructs from its split words
    2b. source/check_paraphrase.py  every paraphrase differs enough from its literal
    2c. source/check_seo.py   sitemap + robots proof (local; add --live to fetch the site)
    2d. source/check_site_health.py  chapter pages, CSS vars, og tags, SW, a11y
    2e. source/audit_titles.py  every title/desc against its own verse
    3. run_gita_app.js        553 assertions on the built document        (needs node)
    4. browser_checks.py      141 live-browser checks                 (needs playwright)

Steps 3 and 4 are skipped with a warning if node / playwright are missing — the
build itself still completes.
"""
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "source")
PY = sys.executable or "python3"

FAST = "--fast" in sys.argv
SERVE = "--serve" in sys.argv


def run(cmd, cwd, label, tail=None, optional=False):
    """Run a command; print its tail. Returns True on success."""
    print(f"\n--- {label} ---")
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    except FileNotFoundError:
        msg = f"({label} skipped — {cmd[0]} not installed)"
        print(msg if optional else f"ERROR: {msg}")
        return optional
    out = (p.stdout or "") + (p.stderr or "")
    lines = out.strip().splitlines()
    print("\n".join(lines[-tail:] if tail else lines))
    if p.returncode != 0 and not optional:
        print(f"\n*** {label} FAILED (exit {p.returncode}) ***")
        return False
    return True


def clear_pycache():
    """Delete every __pycache__ under the project.

    Python caches compiled source files, and a stale cache can make an edit you
    just made to a source/*.py file appear to have no effect. Clearing it first
    means a hand edit always takes effect on the very next build.
    """
    for dirpath, dirnames, _ in os.walk(ROOT):
        for d in list(dirnames):
            if d == "__pycache__":
                shutil.rmtree(os.path.join(dirpath, d), ignore_errors=True)
                dirnames.remove(d)


def main():
    if not os.path.isdir(SRC):
        sys.exit(f"source/ not found next to {__file__}")

    clear_pycache()
    if not run([PY, "build_gita.py"], SRC, "build", tail=4):
        sys.exit(1)

    if FAST:
        print("\nOK: index.html rebuilt (tests skipped: --fast)")
        return

    ok = True
    ok &= run([PY, "check_padas.py"], SRC, "pāda check", tail=1)
    ok &= run([PY, "check_paraphrase.py"], SRC, "paraphrase check", tail=5)

    # Sitemap/robots proof. Local-only by default so a build never needs the
    # network; run  SEO_LIVE=1 python3 build.py  to also fetch the published
    # sitemap and diff it against the build (that is what catches the
    # "Search Console says Couldn't fetch" class of problem).
    seo = [PY, "check_seo.py"] + (["--live"] if os.environ.get("SEO_LIVE") else [])
    ok &= run(seo, SRC, "sitemap / robots proof", tail=4)

    # The generated CHAPTER pages, the CSS and the <head> block — the parts no
    # other suite reads. Every assertion here is a fault that actually shipped.
    ok &= run([PY, "check_site_health.py"], SRC, "site health", tail=6)

    # Titles and descriptions read against the verses they represent. Blocks
    # only on possessive inversion (the 1.10 class, zero false positives);
    # everything else is advisory and printed for a human to read.
    ok &= run([PY, "audit_titles.py"], SRC, "titles vs verses", tail=3)

    node = shutil.which("node")
    if node:
        ok &= run([node, "run_gita_app.js"], ROOT, "document tests", tail=6)
    else:
        print("\n--- document tests ---\n(skipped — node not installed)")

    try:
        import playwright  # noqa: F401
        args = [PY, "browser_checks.py"] + (["--serve"] if not SERVE else ["--serve"])
        ok &= run(args, ROOT, "browser tests", tail=3, optional=True)
    except ImportError:
        print("\n--- browser tests ---")
        print("(skipped — pip install playwright && python3 -m playwright install chromium)")

    print()
    if ok:
        print("OK: index.html is fresh — commit and push to publish.")
    else:
        print("Build finished, but a check FAILED — see above.")
        sys.exit(1)

    if SERVE:
        import http.server
        import socketserver
        os.chdir(ROOT)
        print("\nServing http://localhost:8000/  (Ctrl+C to stop)")
        with socketserver.TCPServer(("", 8000), http.server.SimpleHTTPRequestHandler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nstopped.")


if __name__ == "__main__":
    main()
