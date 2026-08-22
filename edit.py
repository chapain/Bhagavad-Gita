#!/usr/bin/env python3
"""edit.py — edit the Gita app's content in your browser, on your own computer.

    python3 edit.py

Opens http://127.0.0.1:8765 with the whole app plus an "Edit" button on every
verse, theme and part. Change something, press Save, and it writes the real
source file in source/ and rebuilds index.html.

This is a LOCAL tool. It binds to 127.0.0.1, so nothing outside your machine can
reach it, and it is not part of the file you share with anyone. The published
index.html has no editing in it at all.

Safety:
  * every save is validated first — if the pādas no longer spell the verse, or a
    syllable count is wrong, the save is refused and you are told why;
  * the previous version of each file is kept in source/.backup/;
  * files are re-emitted from parsed data, never patched with pattern matching.

Press Ctrl+C to stop.
"""
import http.server
import json
import os
import socketserver
import subprocess
import sys
import threading
import urllib.parse
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "source")
PY = sys.executable or "python3"
PORT = 8765
sys.path.insert(0, SRC)

import dataio as D  # noqa: E402


# --------------------------------------------------------------- content ----
def collect():
    """Everything editable, as one JSON-able blob."""
    from gita_data import CHAPTERS
    out = {"chapters": [], "ui": D.load_ui(), "chapter_i18n": D.load_chapter_i18n()}
    for (num, name, deva, count, blurb) in CHAPTERS:
        verses = D.load_verses(num)
        padas = D.load_padas(num)
        words = D.load_words(num)
        out["chapters"].append({
            "num": num, "name": name, "deva": deva, "count": count, "blurb": blurb,
            "verses": {k: {"deva": v["deva"], "iast": v["iast"]} for k, v in verses.items()},
            "padas": {r: [list(x) for x in rows] for r, rows in padas.items()},
            "words": {str(v): {str(k): [list(w) for w in ws] for k, ws in e.items()}
                      for v, e in words.items()},
            "themes_en": [[t, d, [list(p) for p in ps]] for (t, d, ps) in D.load_themes_en(num)],
            "trans_en": {str(k): list(v) for k, v in D.load_trans_en(num).items()},
            "themes_ne": [[t, d, [list(p) for p in ps]]
                          for (t, d, ps) in (D.load_themes_i18n("ne").get(num) or [])],
            "themes_hi": [[t, d, [list(p) for p in ps]]
                          for (t, d, ps) in (D.load_themes_i18n("hi").get(num) or [])],
        })
    out["trans_ne"] = {k: list(v) for k, v in D.load_trans("ne").items()}
    out["trans_hi"] = {k: list(v) for k, v in D.load_trans("hi").items()}
    out["gloss_ne"] = D.load_gloss("ne")
    out["gloss_hi"] = D.load_gloss("hi")
    return out


def rebuild(full=False):
    cmd = [PY, "build.py"] + ([] if full else ["--fast"])
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr)


# ----------------------------------------------------------------- saves ----
def _snapshot(paths):
    """Copy the given source files aside so a rejected save can be undone."""
    keep = {}
    for p in paths:
        full = os.path.join(SRC, p)
        if os.path.exists(full):
            with open(full, "rb") as f:
                keep[full] = f.read()
    return keep


def _rollback(keep):
    for full, blob in keep.items():
        with open(full, "wb") as f:
            f.write(blob)


def _touched(kind, ch):
    """Which source files a change of this kind rewrites."""
    gd = "gita_data.py" if ch == 1 else f"gita_data{ch}.py"
    return {
        "verse": [f"ch{ch}.json"],
        "verse_all": [f"ch{ch}.json", f"padas_ch{ch}.py"],
        "padas": [f"padas_ch{ch}.py"],
        "words": [f"padachheda_ch{ch}.py"],
        "trans_en": [gd],
        "themes_en": [gd],
        "trans_ne": ["translations_ne.py"], "trans_hi": ["translations_hi.py"],
        "themes_ne": ["themes_ne.py"], "themes_hi": ["themes_hi.py"],
        "gloss_ne": ["gloss_ne.py"], "gloss_hi": ["gloss_hi.py"],
        "chapter_i18n": ["i18n_chapters.py"],
        "ui": ["i18n_ui.py"],
    }.get(kind, [])


def apply_change(kind, payload):
    """Write one change. Returns (ok, message).

    The change is written, then the build's own validators run. If they reject
    it, the file is put back exactly as it was — so a bad edit never survives.
    """
    ch = int(payload.get("ch", 0) or 0)
    undo = _snapshot(_touched(kind, ch))

    if kind == "verse":
        D.save_verse(ch, payload["v"], payload["deva"], payload["iast"])

    elif kind == "verse_all":
        # The verse text and its pādas describe the same words, so they must
        # change together — editing one alone always fails validation.
        D.save_verse(ch, payload["v"], payload["deva"], payload["iast"])
        data = D.load_padas(ch)
        data[payload["ref"]] = [tuple(r) for r in payload["rows"]]
        D.save_padas(ch, data)

    elif kind == "padas":
        data = D.load_padas(ch)
        data[payload["ref"]] = [tuple(r) for r in payload["rows"]]
        D.save_padas(ch, data)

    elif kind == "words":
        data = D.load_words(ch)
        v = int(payload["v"])
        entry = {"s": [list(w) for w in payload["words"].get("s", [])]}
        for k in range(4):
            entry[k] = [list(w) for w in payload["words"].get(str(k), [])]
        data[v] = entry
        D.save_words(ch, data)

    elif kind == "trans_en":
        themes = D.load_themes_en(ch)
        tr = dict(D.load_trans_en(ch))
        tr[int(payload["v"])] = (payload["lit"], payload["para"])
        D.save_gita_data(ch, themes, tr)

    elif kind in ("trans_ne", "trans_hi"):
        lang = kind.split("_")[1]
        tr = dict(D.load_trans(lang))
        tr[payload["ref"]] = (payload["lit"], payload["para"])
        D.save_trans(lang, tr)

    elif kind == "themes_en":
        tr = D.load_trans_en(ch)
        themes = [(t, d, [tuple(p) for p in ps]) for (t, d, ps) in payload["themes"]]
        D.save_gita_data(ch, themes, tr)

    elif kind in ("themes_ne", "themes_hi"):
        lang = kind.split("_")[1]
        all_t = dict(D.load_themes_i18n(lang))
        all_t[ch] = [(t, d, [tuple(p) for p in ps]) for (t, d, ps) in payload["themes"]]
        D.save_themes_i18n(lang, all_t)

    elif kind in ("gloss_ne", "gloss_hi"):
        lang = kind.split("_")[1]
        g = dict(D.load_gloss(lang))
        g[payload["word"]] = payload["meaning"]
        D.save_gloss(lang, g)

    elif kind == "chapter_i18n":
        D.save_chapter_i18n(payload["data"])

    elif kind == "ui":
        ui = D.load_ui()
        ui[payload["lang"]][payload["key"]] = payload["value"]
        D.save_ui(ui)

    else:
        return False, f"unknown change type: {kind}"

    ok, log = rebuild(full=False)
    if not ok:
        _rollback(undo)
        rebuild(full=False)          # put index.html back too
        tail = "\n".join(l.strip() for l in log.splitlines() if l.strip().startswith("✗"))
        return False, ("Not saved — this change would break the data:\n\n" +
                       (tail or log[-700:]) +
                       "\n\nYour file was left exactly as it was.")
    return True, "Saved and rebuilt."


# ---------------------------------------------------------------- server ----
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, *a):
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/content":
            try:
                return self._json({"ok": True, "data": collect()})
            except Exception as e:
                return self._json({"ok": False, "error": str(e)}, 500)
        if path == "/api/build":
            ok, log = rebuild(full=True)
            return self._json({"ok": ok, "log": log[-4000:]})
        if path in ("/", "/edit", "/editor"):
            self.path = "/editor.html"
        return super().do_GET()

    def do_POST(self):
        if urllib.parse.urlparse(self.path).path != "/api/save":
            return self._json({"ok": False, "error": "not found"}, 404)
        try:
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n).decode("utf-8"))
            ok, msg = apply_change(req["kind"], req["payload"])
            return self._json({"ok": ok, "message": msg})
        except Exception as e:
            return self._json({"ok": False, "message": f"{type(e).__name__}: {e}"}, 500)


def main():
    if not os.path.exists(os.path.join(ROOT, "editor.html")):
        sys.exit("editor.html not found next to edit.py")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        url = f"http://127.0.0.1:{PORT}/"
        print(f"\n  Gita content editor running at {url}")
        print("  Local only — nothing outside this computer can reach it.")
        print("  Backups of every changed file go to source/.backup/")
        print("  Press Ctrl+C to stop.\n")
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  stopped.")


if __name__ == "__main__":
    main()
