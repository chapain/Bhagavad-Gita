# PROJECT.md — everything needed to pick this up cold

If you are an assistant resuming this project with nothing but the repository,
read this file first. `README.md` explains how to *use* the project; this file
explains *why it is the way it is*, and records decisions and mistakes that the
code alone cannot tell you.

---

## 1. What this is

A Bhagavad Gita study app, published at
**https://chapain.github.io/Bhagavad-Gita/**. It is a **split site**: a light
`index.html` shell (~120 KB gzipped) plus one data file per chapter
(`data/ch<N>.js`, 18 files) that the shell loads in parallel at startup and the
service worker precaches. First paint arrives after ~120 KB instead of ~5 MB,
and editing one verse invalidates one small file, not the whole app. After the
first visit the service worker has every file, so the app is fully offline and
installable ("Add to Home Screen").

The app is shared **by link**. There is no all-in-one file: the owner retired
the WhatsApp/download single-file deliverable on 2026-08-24 ("I don't care
about the whatsapp. i can simply share the link to the site"). A split app
cannot run from `file://` — browsers block `fetch`/XHR of local files — so if a
single shareable file is ever wanted again, it must be re-added as a separate
generated artefact (it was `gita-standalone.html`, removed here); do not try to
open the split site from a downloaded folder.

*Decision history:* until 2026-08-24 the deliverable was one standalone
`index.html`. The owner first lifted the one-file condition, then dropped
file-sharing entirely, so the split site is now the sole artefact. Everything
is generated; nothing is edited by hand.

Owner: Dhruba Chapain. Licence: none — all rights reserved.

**Content:** 18 chapters · 182 themes · 558 parts · 700 verses, each with
Devanagari, IAST, a four-pāda division, word-by-word meanings, a literal
translation and a paraphrase, in **English, Nepali and Hindi**.

**Features:** trilingual switching, global search, favourites (orderable, each
with a private note), random verse, verse popup with 2×2 pāda boxes and
pada-chheda toggles, continuous chapter reading, keyboard navigation, welcome
screen, the three ways (niṣṭhā), dark mode.

**The Devanagari font is embedded** as a base64 woff2 data URI, built at compile
time by `_font_face()` in `build_gita.py` from `source/fonts/*.woff2`. Do not
remove it: the CSS asks for "Noto Serif Devanagari", and on any device that does
not ship it (older Android, most Windows) the conjuncts — क्ष, द्ध, ङ्ग — break
apart or show as boxes. The author's own phone has the font, so he would never
see the failure. Subset to the Devanagari block: ~42 KB regular + ~46 KB bold,
about 2% of the file. SIL Open Font License 1.1, see `source/fonts/OFL-*.txt`.

---

## 2. The one rule that governs everything

> **The code renders data. It never generates or repairs it.**

The app's content is finished, so nothing is derived at build time. Every
displayed string is read from a data file in `source/` and printed as-is. If
something is wrong on screen, the fix is always a data edit, never a code change.

This was a deliberate migration, and it is *proven*, not assumed:

* `source/prove_data_only.py` edits each kind of content in turn and confirms the
  change reaches `index.html`.
* The old ITRANS→Devanagari converter and metre-splitter (`gita_conv.py`), the
  freeze tool (`freeze_padas.py`), the override workaround (`pada_overrides.py`)
  and an unused `sandhi.py` were all **deleted**.
  `run_gita_app.js` asserts they stay deleted and that the builder never calls
  `iast_to_deva`, `to_deva`, `split_half_padas`, `snap_pair` or `parse_verse`.

**Do not reintroduce derivation.** Two separate multi-verse bugs came from it.

---

## 3. Layout

```
index.html            the app SHELL — GENERATED, never edit by hand
data/ch*.js           18 per-chapter data files — GENERATED (loaded by the shell)
sw.js, manifest, icons/
sitemap.xml, robots.txt   GENERATED — crawler files (see §10)
chapter/ + chapter.css    GENERATED — 18 SEO landing pages (see §10)
build.py              build + verify (cross-platform, IDE-friendly)
rebuild.sh            same, as a shell script
run_gita_app.js       524 assertions on the built document      (needs node)
browser_checks.py     106 live-browser checks                 (needs playwright)
edit.py               local browser-based content editor
editor.html           its interface
source/
  ch*.json            verse Devanagari + IAST            <- the running verse
  padas_ch*.py        the four pādas of every verse      <- the popup boxes
  padachheda_ch*.py   word-by-word split + English gloss
  gloss_ne/hi.py      Nepali/Hindi word meanings, keyed by IAST
  gita_data*.py       English themes, parts, translations
  themes_ne/hi.py     Nepali/Hindi themes and parts
  translations_ne/hi.py
  i18n_chapters.py    chapter names/blurbs (ne, hi)
  i18n_ui.py          91 UI strings × 3 languages
  build_gita.py       the builder + the manual-edit audit
  dataio.py           safe read/write of every data file (used by edit.py)
  verify.py           norm1() and syll_iast() — used ONLY to check data
  check_padas.py      rebuilds each pāda from its words via sandhi
  check_paraphrase.py every paraphrase differs enough from its literal
  prove_data_only.py  proves the build renders rather than generates
```

**Build:** `python3 build.py` (or `--fast` to skip tests, `--serve` for :8000).
It clears `__pycache__` first — a stale cache once made an edit appear to do
nothing.

---

## 4. Editorial decisions — settled, do not relitigate

**4.1 The running verse is printed verbatim from `ch*.json`.**
The text is stored as `।`-separated segments: two verse lines, plus a speaker
where there is one. They render in order — which is why 1.21 and 1.28 correctly
show `अर्जुन उवाच` *between* the two lines. Nothing is re-joined.

**4.2 Pāda boxes show the verse as printed; word lists show the pre-sandhi form.**
So 4.33 pāda 1 ends `…yajñāj` (as the verse reads) while its word list says
`yajñāt` (the real word). Asked to "restore the originals" in the pāda text, we
decided **no**, because 8.20 disproves any uniform rule: `anyaḥ` + `avyaktaḥ` →
`anyo’vyakto` merges two vowels, so restoring both sides gives 8+9 = 17
syllables in a half-line that must be 16. A rule that works nine times and
breaks the tenth is worse than none.

**4.3 Metre.** Every anuṣṭubh (32 syllables) divides 8/8/8/8; every triṣṭubh (44)
divides 11/11/11/11. Five verses are genuinely irregular and are correct as they
stand: **11.01** (33), **2.29 / 8.10 / 15.03** (45), **2.06** (46). In each, the
extra syllable sits on a pāda that is a complete phrase.

**4.4 An avagraha belongs at the START of the pāda whose word lost the vowel.**
8.20 reads `…bhāvo’nyo` | `’vyakto…`, never `…bhāvo’nyo’` | `vyakto…`.

**4.5 `nacireṇa` (5.06) is one word** — "before long". Do not split it as
`na` | `cireṇa` to force 8/8; the pāda is already right at 8/8.

**4.6 `ṃs` vs `ns`.** 13 verses write `ांस्` → `ṃs` (before a dental); 4 write
`ान्स्` → `ns` (before `स्व`/`स्य`). Both are correct and each matches its own
Devanagari. 14.21 is `caitāṃs`, not `caitāns`.

**4.7 Dark mode is warm, never pure black or white.** Devanagari has fine strokes
that shimmer at maximum contrast. The suite fails the build if `#000` or `#fff`
appears in the dark block.

**4.8 Naming.** Breadcrumbs read `Chapter <n> · <name>` and `Theme <n> · <title>`,
never a bare title. Devanagari puts the destination before the verb, so
interpolated labels need per-language templates (`{x}मा फर्कनुहोस्`).

**4.9 Credit and AI disclosure.** The footer credit names the author; the AI
disclosure lives in `LICENSE.md` ("AI disclosure") and the README — not in the
visible footer. The owner chose this placement on 2026-08-24 (disclosed, but
not prominent). The test suite locks both the footer wording *and* the presence
of the LICENSE section, so neither the credit nor the disclosure can drift
silently. Do not remove the LICENSE section without the owner's say-so.

---

## 5. The build's manual-edit audit

`build_gita.py` stops the build if a source file says something the app would not
show. Each check was added after a real bug and each was verified by planting the
error it is meant to catch:

| # | catches |
|---|---|
| 1  | pādas that no longer spell the verse in `ch*.json`; wrong syllable counts |
| 1b | a pāda starting with a consonant stranded from the previous pāda |
| 1c | stray leading/trailing/double spaces in pāda text |
| 1d | anuṣṭubh not 8/8/8/8, triṣṭubh not 11/11/11/11 |
| 1e | an avagraha dangling at the end of a pāda |
| 1f | `-aḥ` before a voiced consonant (should be `-o`) |
| 2  | a verse with no Nepali or Hindi translation (would silently show English) |
| 3  | `ne`/`hi` theme files not mirroring the English structure |
| 4  | a verse no part's range covers, making it unreachable |

`check_padas.py` separately rebuilds each pāda from its word list via external
sandhi: **2800 pādas, 0 residual flags**.

`check_paraphrase.py` measures how much each flowing paraphrase overlaps its
own literal, and fails at **80%**. A paraphrase that just swaps a word or two
leaves the second column saying nothing new. Current medians: en 59%, ne 63%,
hi 63%; the highest single pair is 80%.

**Green means consistent, not correct.** These checks cannot tell that `naśnan`
is not a Sanskrit word. Only reading catches that.

---

## 6. The editor

`python3 edit.py` → `http://127.0.0.1:8765`. Six tabs covering every editable
field. Local-only (binds `127.0.0.1`); none of it ships in `index.html`.

**Design rules, learned from breaking things:**

* Never regex-patch a data file. Import the module, edit the dict, re-emit the
  whole file, re-import and compare. `dataio.py` does this for all 15 writers.
* A rejected save is **rolled back** — the file is restored byte-for-byte.
* The verse text and its pādas must change **together** (`verse_all`), because
  editing one alone always fails validation. There is also a per-verse
  find/replace that updates the verse and every quarter at once.
* Backups go to `source/.backup/`.

---

## 7. Mistakes already made — do not repeat

* **Regex on file structure destroyed data.** A pattern meant to match a verse
  number matched a pāda index instead, writing 17.19's words onto verse 9 and
  creating phantom verse `0` entries. Recovery was only cheap because a good zip
  existed. **Parse and re-emit; never pattern-match structure.**
* **Fixing one instance of a bug class without enumerating the class.** The
  binary pāda-join flag was "fixed" for 16.1 while 92 other verses stayed broken.
  After fixing anything, scan all 700.
* **Assuming a sandhi rule is uniform.** Twice a plausible-looking Sanskrit
  correction was wrong: `naśnan` for `aśnan` (5.08) and the same in 5.09 — the
  `n` doubles and *both* belong to the previous pāda. Check the word list.
* **Restoring text from memory.** A "reverted" Nepali paraphrase came back
  subtly reworded and passed every check. Use `source/.backup/` or the zip.
* **Trusting a test that never ran.** Several times a mutation test appeared to
  pass because the file was restored before the build read it, or because `grep`
  missed the output. Confirm the failure actually appears.
* **Changing counts breaks hard-coded totals** in `run_gita_app.js` (themes,
  parts, UI keys) and its header comment.
* **`/tmp` is wiped by sandbox resets.** Reinstall playwright with
  `pip install playwright && python3 -m playwright install chromium --with-deps`.
* Do not recommend Google Drive for hosting. Do not call Netlify Drop
  "no account needed". WhatsApp's in-app viewer does not run JavaScript.

---

## 8. Working with the owner

Dhruba reads the app closely and has caught **twelve** content errors the
automated checks could not — including both pāda-join bugs, the 5.08/5.09
gemination, the 8.20 avagraha placement, and the 1.15 missing sandhi that then
turned up in ten more verses.

Practical consequences:

* When he reports something, **verify it against the source before agreeing** —
  but assume it is probably right; the record strongly favours him.
* Show the evidence: print the verse, the word list, the syllable counts.
* Never invent an `old` string when patching. `grep -n` first, then
  `assert s.count(old) == 1` before replacing.
* Screenshot at 390 px and read the actual rendered text. Automated tests have
  passed through mislabelled titles, dead buttons and words broken mid-line.
* He prefers batches he can spot-check over one long unattended run.

---

## 9. State at the time of writing

*Verified 2026-08-24 on a clean sandbox after resuming from a crash:*

* **Split build** (2026-08-24, standalone retired): `index.html` =
  **`7443c7be6204`**, a **116 KB gzipped shell** that loads 18
  `data/ch<N>.js` files in parallel at startup and boots when all arrive.
  `sw.js` = **`1e8af1526877`**, cache `gita-7227d0e5f4c4`, precaches the shell
  **and all 18 data files** — fully offline after the first visit. There is no
  `gita-standalone.html` any more; the app is shared by link. **Not yet
  uploaded** — publish `index.html`, `sw.js`, `manifest.webmanifest`,
  `sitemap.xml`, `robots.txt`, `chapter.css`, the `data/` folder, the
  `chapter/` folder, and the icons.
* Earlier discoverability work (still in place): long-tail `<title>`, canonical
  + JSON-LD, `sitemap.xml` (19 URLs) + `robots.txt`, **18 full-text chapter
  pages** (`chapter/<n>/` + `chapter.css`), `#chapter=N` deep-link routing,
  the SW shell-cache guard, the dormant `source/gsc_token.txt` mechanism, the
  footer credit naming the author (AI disclosure in LICENSE.md + README,
  §4.9), and the `colophon.itrans` remnants
  removed (see §10).
* Live site https://chapain.github.io/Bhagavad-Gita/ confirmed at
  **`b839cd7103e6`** (the previous build, without the SEO tags). Recheck with
  `curl -sL https://chapain.github.io/Bhagavad-Gita/ | sha256sum`.
* GitHub repo is clean: the 7 stale `source/` files (`gita_conv.py`,
  `pada_overrides.py`, `freeze_padas.py`, `sandhi.py`, `bg.itx`,
  `gita_shankarabhashya.itx`, `shankara_verses.json`) all return 404 —
  deleted. `.gitignore` is present. `source/` is in sync (86 files + `fonts/`
  with 3 = 89 files, 118 total in the repo including `.gitignore`).
* Full suite green: **524 assertions + 106 browser checks (incl. offline SW) +
  2800 pādas + 2100 paraphrase pairs**, and `prove_data_only.py` passes all 7
  cases against the published build.
* Upload method: unzip → select everything *inside* → **Add file → Upload files**
  → Commit. Uploading never deletes; removed files must be deleted by hand, or
  delete the `source/` directory first and re-upload it.

---

## 10. Discoverability (Google / SEO)

The app was invisible in search — a `site:` query found nothing. What was added
and why:

* **`<link rel="canonical">` + JSON-LD `WebApplication`** in the head, built
  from `__BASE__` like the og: tags. The JSON-LD is deliberately `WebApplication`
  with Dhruba as `author`, not `Book` — the Gita's authorship is Vyasa's; this is
  a study *edition*, and the structured data should not claim otherwise.
* **`sitemap.xml` and `robots.txt`** are generated at build time (never checked
  in by hand) so `lastmod` always matches the build and the URLs follow
  `SITE_BASE`. They publish alongside `index.html`.
* **18 chapter pages** (`chapter/<n>/index.html` + one shared `chapter.css`)
  are generated from the same `data` the app renders — each is the **full
  readable chapter**: name in three languages, blurb, theme list with anchors,
  and every verse printed as-is (Devanagari, IAST, literal translation in all
  three languages, English paraphrase) with per-verse `id="v<ch.n>"` anchors,
  plus CTAs that deep-link into the app via `index.html#chapter=<n>` (hash
  routing in the boot script). This is the discoverability layer: static,
  crawlable text for long-tail queries ("bhagavad gita chapter 2 in nepali",
  verse-level searches), while the app itself is the interactive split site.
  Publishing them is optional for the app but they are listed in the sitemap.
* **The site is a split build** (see §1): shell + `data/ch*.js`, no all-in-one
  file. The service worker precaches every data file, so after the first visit
  the app is fully offline and installable. The test suite and
  `check_paraphrase.py` read the published `data/ch*.js` directly, and
  `prove_data_only.py` checks the union of the shell and all data files, so
  the published bytes are what gets verified — there is no separate copy to
  drift.
* **The `<title>` targets the long tail** — "Bhagavad Gita — English, Nepali,
  Hindi · 700 Verses". The `<h1>`, manifest name and JSON-LD keep the branding
  "Interactive Study"; this split is deliberate. The suite locks the exact
  title in two places (`run_gita_app.js`, `browser_checks.py`).
* **Search Console verification** is supported by a placeholder: put the token
  (the `content` value of Google's meta tag — it is public, not a secret) in
  `source/gsc_token.txt` and rebuild; the tag appears. No file → no tag.
* **SW shell-cache guard:** the service worker stores a navigation response as
  `./index.html` only when the URL *is* the app root — otherwise visiting a
  chapter page would poison the offline fallback. There is a live browser
  check for exactly this.
* **`robots.txt` on a sub-path is advisory for Google.** Google only reads
  `github.io/robots.txt` (GitHub's, which allows everything). The real channel
  is **Google Search Console**: verify the property
  `https://chapain.github.io/Bhagavad-Gita/`, submit `sitemap.xml`, then use
  *URL inspection → Request indexing*. Until that is done, none of the above
  matters much.
* **hreflang is deliberately absent.** All three languages live at one URL
  (in-page switching); hreflang requires distinct URLs and would be wrong here.
  The `og:locale:alternate` tags already cover the sharing case.
* **Realistic strategy.** The head term "bhagavad gita" belongs to Wikipedia
  and the big Gita sites. The winnable queries are the long tail this app
  uniquely answers — *bhagavad gita in nepali*, *भगवद्गीता नेपाली अनुवाद*,
  *gita word-by-word meaning* — plus backlinks (GitHub repo topics, Reddit
  r/Hinduism / r/bhagavadgita, Quora, Facebook groups for Nepali readers).
* **Title and description are branding decisions** — the suite locks the exact
  `<title>`; changing it means updating `run_gita_app.js` and
  `browser_checks.py` deliberately, together with this file.
