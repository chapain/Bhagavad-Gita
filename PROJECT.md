# PROJECT.md — everything needed to pick this up cold

If you are an assistant resuming this project with nothing but the repository,
read this file first. `README.md` explains how to *use* the project; this file
explains *why it is the way it is*, and records decisions and mistakes that the
code alone cannot tell you.

---

## 1. What this is

A Bhagavad Gita study app. The deliverable is **one standalone `index.html`**
(~5 MB) that works offline and can be sent to friends over WhatsApp. It is also
published at **https://chapain.github.io/Bhagavad-Gita/**.

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
index.html            the app — GENERATED, never edit by hand
sw.js, manifest, icons/
build.py              build + verify (cross-platform, IDE-friendly)
rebuild.sh            same, as a shell script
run_gita_app.js       413 assertions on the built document      (needs node)
browser_checks.py     41 live-browser checks                 (needs playwright)
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
  i18n_ui.py          89 UI strings × 3 languages
  build_gita.py       the builder + the manual-edit audit
  dataio.py           safe read/write of every data file (used by edit.py)
  verify.py           norm1() and syll_iast() — used ONLY to check data
  check_padas.py      rebuilds each pāda from its words via sandhi
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

* `index.html` = **`0add281058fd`**, `sw.js` cache matches.
* Live site was last confirmed at `57799836af9e` — **behind by the 11 sandhi
  fixes**. Check `curl -sL https://chapain.github.io/Bhagavad-Gita/ | sha256sum`.
* `build.py`: **413 assertions + 41 browser checks + 2800 pādas, all green.**
* `.gitignore` exists locally but is **missing on GitHub** (Finder hides
  dotfiles; Cmd+Shift+. reveals them).
* Upload method: unzip → select everything *inside* → **Add file → Upload files**
  → Commit. Uploading never deletes; removed files must be deleted by hand, or
  delete the `source/` directory first and re-upload it.
