# What to upload — 2026-09-01 (Learn by heart + theme rework)

**39 files. One drag. Well under GitHub's 100-file web limit.**

Everything else on the site is already identical to this build — I diffed all
52 published files against the live site; 13 are unchanged and listed at the
bottom so you can leave them alone.

---

## Upload these

### 3 root files

| File | Why it changed |
|---|---|
| `index.html` | Learn by heart, mūla retired, sheet navigation, saffron ranges, the work-in-progress note |
| `sw.js` | new cache version `gita-8e01c2463744` — without this, returning visitors keep the old app |
| `chapter.css` | theme ranges are saffron now |

### 2 folders

| Folder | Files | Why |
|---|---|---|
| `chapter/` | 18 | theme splits changed every chapter page |
| `data/` | 18 | 222 themes now (was 202) — the app reads these |

**How:** `Add file` → `Upload files` → drag the 3 root files **and** the
`chapter` and `data` folders together → Commit.

`data/` must go with the rest. The app loads a chapter's themes from
`data/chN.js`; if the shell is new but the data is old, the theme counts
disagree and chapters render wrong.

---

## Do NOT upload

Build inputs and tooling — they can live in the repo, but they are not part of
the published site:

`source/`, `build.py`, `rebuild.sh`, `browser_checks.py`, `run_gita_app.js`,
`edit.py`, `editor.html`, `shoot_*.py`, `PROJECT.md`, `README.md`,
`LICENSE.md`, `UPLOAD.md`

---

## Unchanged — leave them alone (13 files)

`404.html` · `sitemap.xml` · `robots.txt` · `manifest.webmanifest` ·
`og-card.png` · `noto-deva-regular.woff2` · `favicon.ico` · `icon-192.png` ·
`icon-512.png` · `icon-maskable-512.png` · `apple-touch-icon.png` ·
`img/share-art.jpg` · `google13a355facca610af.html`

---

## After it publishes

1. **Hard-refresh.** Pages caches ~10 minutes, and the service worker needs a
   reload to pick up `gita-8e01c2463744`. If you see the old app, close every
   tab of the site and reopen.
2. Open a chapter — the chooser should show **three** pills:
   Verses with translation · Study guide · **Learn by heart**.
3. Tap **Learn by heart** on **chapter 12** (8 themes, the shortest complete
   walk). Story first, then the verses.
4. Check a theme range like **1.1–1.3** — it should be saffron, not grey.
5. The welcome screen should carry the work-in-progress note under the footer.

---

## Is the drill ready for all 18 chapters?

Yes — verified, not assumed:

* **222 themes, 700 verses**, every verse in exactly one theme
* **1,594 questions** generatable; **zero** themes that generate none
* Every question has **4 valid options** — no shortages anywhere
* **Zero** non-terminating drill queues, simulated at a 50% error rate
* Story stage scales: chapters with 10+ themes get all four steps, smaller ones
  get read → whole-chain

Suites: **644** document assertions · **420** site-health checks · 2,800 pādas ·
2,100 paraphrase pairs — all green.

**Known and deliberate:** the Nepali and Hindi teaching copy in the learn path
and the retitled themes is a first draft. It is grammatical, but it should
sound like a teacher rather than a translation — worth your ear. Everything is
editable in `editor.html` → "Themes & parts", which validates and rolls back a
bad save.
