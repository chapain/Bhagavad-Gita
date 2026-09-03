# -*- coding: utf-8 -*-
"""check_seo.py — prove the sitemap/robots pair is fetchable, not guessed at.

Google Search Console's "Couldn't fetch" is a dead end: it never says *why*. So
instead of guessing, this file asks the same questions a crawler does, in the
order a crawler would hit them, and prints the actual byte it saw:

    1. sitemap.xml exists, is UTF-8 with no BOM, and parses as XML.
    2. every <loc> is an absolute https:// URL inside SITE_BASE, ends in "/",
       and points at a file that really exists in the site directory.
    3. robots.txt carries the exact `Sitemap:` line for that file.
    4. the classic submission typos are spelled out with the status each one
       gives — because "Couldn't fetch" almost always means one of *these*
       URLs was typed into the Search Console box, not the good one.

With no arguments it checks the local build only (no network). Add `--live` to
also fetch the published site and diff it against the local build.

It only reads and reports; it never changes your data.
"""
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(BASE)          # site files are generated straight into the repo root
LIVE = "--live" in sys.argv
NET = "--no-net" in sys.argv

# SITE_BASE is the single source of truth for the published origin + project path.
_m = re.search(r'SITE_BASE = os\.environ\.get\(\s*"SITE_BASE",\s*"([^"]+)"',
               open(os.path.join(BASE, "source", "build_gita.py"), encoding="utf-8").read())
SITE_BASE = (_m.group(1) if _m else "https://chapain.github.io/Bhagavad-Gita").rstrip("/")

NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
CHAPTERS = 18
fails, notes, passed = [], [], 0


def bad(msg):
    fails.append(msg)
    print("  FAIL  " + msg)


def ok(msg):
    global passed
    passed += 1
    print("  ok    " + msg)


def info(msg):
    notes.append(msg)
    print("  note  " + msg)


def local_path_for(url):
    """Map a published URL back to the file on disk that must exist for it."""
    rel = url[len(SITE_BASE):].lstrip("/")
    if not rel:
        return os.path.join(SITE, "index.html")
    return os.path.join(SITE, *rel.split("/"), "index.html")


def status(url, timeout=15):
    """Return (code, content_type, nbytes) or (0, error, 0) if unreachable."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (gita-seo-check)"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return r.status, r.headers.get("content-type", ""), len(body)
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("content-type", ""), 0
    except Exception as e:                                    # noqa: BLE001
        return 0, str(e)[:60], 0


def check_local():
    print("\n--- sitemap.xml (local build) ---")
    path = os.path.join(SITE, "sitemap.xml")
    if not os.path.exists(path):
        bad("sitemap.xml is missing — run: python3 build.py")
        return
    raw = open(path, "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        bad("sitemap.xml starts with a UTF-8 BOM — some parsers reject it")
    else:
        ok("no BOM, %d bytes" % len(raw))
    if not raw.startswith(b"<?xml version=\"1.0\" encoding=\"UTF-8\"?>"):
        bad("sitemap.xml does not open with the exact UTF-8 XML declaration")
    else:
        ok("opens with the UTF-8 XML declaration")
    try:
        locs = [u.find("s:loc", NS).text for u in ET.fromstring(raw).findall("s:url", NS)]
    except ET.ParseError as e:
        bad("sitemap.xml does not parse as XML: %s" % e)
        return
    ok("parses as XML — %d <url> entries" % len(locs))

    if len(locs) != CHAPTERS + 1:
        bad("expected %d URLs (root + %d chapters), found %d" % (CHAPTERS + 1, CHAPTERS, len(locs)))
    if locs[0] != SITE_BASE + "/":
        bad("first <loc> is %r, expected %r" % (locs[0], SITE_BASE + "/"))
    for i, loc in enumerate(locs):
        if not loc.startswith("https://"):
            bad("<loc> #%d is not absolute https: %r" % (i + 1, loc))
        elif not loc.startswith(SITE_BASE + "/"):
            bad("<loc> #%d is outside SITE_BASE (%s): %r" % (i + 1, SITE_BASE, loc))
        if not loc.endswith("/"):
            bad("<loc> #%d does not end in '/': %r — Google will fetch it and get a 301" % (i + 1, loc))
        f = local_path_for(loc)
        if not os.path.exists(f):
            bad("<loc> #%d has no file on disk: %s" % (i + 1, os.path.relpath(f, SITE)))
    if not fails:
        ok("all %d <loc> are absolute, inside %s, and backed by a real file" % (len(locs), SITE_BASE))

    print("\n--- robots.txt (local build) ---")
    rpath = os.path.join(SITE, "robots.txt")
    if not os.path.exists(rpath):
        bad("robots.txt is missing — run: python3 build.py")
    else:
        rtxt = open(rpath, encoding="utf-8").read()
        want = "Sitemap: %s/sitemap.xml" % SITE_BASE
        if want in rtxt:
            ok("carries the exact line: %s" % want)
        else:
            bad("robots.txt has no `%s` line (found: %r)" % (want, rtxt.strip()))
        if "Disallow" in rtxt and not re.search(r"Disallow:\s*$", rtxt):
            bad("robots.txt disallows something — check it is not blocking the crawler")
        else:
            ok("nothing is disallowed")

    print("\n--- the URLs a crawler could be sent (submit the FIRST one only) ---")
    print("  GOOD  %s/sitemap.xml            <- this is the one for Search Console" % SITE_BASE)
    print("  BAD   %s/sitemap.xml/           trailing slash  -> 404 on GitHub Pages" % SITE_BASE)
    print("  BAD   %s/sitemap.xml            project path dropped -> 404" % SITE_BASE.rsplit("/", 1)[0])
    print("  BAD   %s/Sitemap.xml            capital S -> 404 (GitHub Pages is case-sensitive)" % SITE_BASE)
    info("if Search Console shows \"Couldn't fetch\", first check which of the four you typed.")


def check_live():
    print("\n--- live site (%s) ---" % SITE_BASE)
    url = "%s/sitemap.xml" % SITE_BASE
    code, ctype, n = status(url)
    if code != 200:
        bad("GET %s -> %s (Search Console would say \"Couldn't fetch\")" % (url, code or "unreachable"))
        return
    if "xml" not in ctype:
        bad("%s is served as %r, not application/xml" % (url, ctype))
    else:
        ok("GET -> 200, content-type: %s, %d bytes" % (ctype, n))

    with urllib.request.urlopen(urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (gita-seo-check)"}), timeout=15) as r:
        live_raw = r.read()
    local_raw = open(os.path.join(SITE, "sitemap.xml"), "rb").read()
    if live_raw == local_raw:
        ok("live sitemap is byte-identical to the local build")
    else:
        ll = [u.find("s:loc", NS).text for u in ET.fromstring(live_raw).findall("s:url", NS)]
        nl = [u.find("s:loc", NS).text for u in ET.fromstring(local_raw).findall("s:url", NS)]
        lm = re.search(r"<lastmod>([\d-]+)</lastmod>", live_raw.decode("utf-8"))
        info("live sitemap is STALE — %d URLs, lastmod %s. Local build has %d URLs."
             % (len(ll), lm.group(1) if lm else "?", len(nl)))
        info("push the built sitemap.xml (and the rest of the build) to make it match.")

    rcode, rctype, _ = status("%s/robots.txt" % SITE_BASE)
    if rcode == 200 and "text/plain" in rctype:
        ok("robots.txt -> 200, %s" % rctype)
    else:
        bad("robots.txt -> %s / %r" % (rcode, rctype))

    print("\n--- every <loc> in the LIVE sitemap, fetched ---")
    for loc in [u.find("s:loc", NS).text for u in ET.fromstring(live_raw).findall("s:url", NS)]:
        c, _, _ = status(loc)
        if c == 200:
            global passed
            passed += 1
            print("  ok    200  %s" % loc)
        else:
            bad("%s -> %s (a 404 inside the sitemap makes Google distrust it)" % (loc, c))

    print("\n--- the typo variants, fetched for real ---")
    for u, why in (("%s/sitemap.xml/" % SITE_BASE, "trailing slash"),
                   ("%s/sitemap.xml" % SITE_BASE.rsplit("/", 1)[0], "project path dropped"),
                   ("%s/Sitemap.xml" % SITE_BASE, "capital S")):
        c, _, _ = status(u)
        print("  %s  %s  %s" % ("ok  " if c == 404 else "WARN", c, u + "  (" + why + ")"))
        if c != 404:
            info("%s returned %s, not 404 — unexpected, worth a look" % (u, c))


def main():
    print("check_seo.py — sitemap / robots proof")
    print("SITE_BASE: %s" % SITE_BASE)
    check_local()
    if LIVE:
        if NET:
            info("--no-net given, skipping the live fetch")
        else:
            check_live()
    else:
        info("local-only run. Add --live to also fetch the published site.")
    print()
    if fails:
        print("check_seo.py: %d FAILED, %d notes" % (len(fails), len(notes)))
        sys.exit(1)
    print("check_seo.py: all green — %d checks passed, %d notes" % (passed, len(notes)))


if __name__ == "__main__":
    main()
