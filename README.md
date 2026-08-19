# Bhagavad Gita — Interactive Study

**Live app → https://chapain.github.io/Bhagavad-Gita/**

A complete, offline-capable study edition of the Bhagavad Gītā — **18 chapters, 700
verses** — aligned to the Śaṅkara-bhāṣya readings, in **English · नेपाली · हिन्दी**,
with word-by-word meanings for every word in all three languages.

Open the link, then use your browser menu → **Add to Home Screen**. It installs like an
app and works with no internet connection.

---

## What it does

- **Browse** chapters → themes → parts → verses, or start from the three yogas
  (कर्मयोग 1–6 · भक्तियोग 7–12 · ज्ञानयोग 13–18).
- **Every verse in its four quarters (pādas)** — Devanagari, IAST transliteration,
  a literal translation and a flowing paraphrase.
- **Tap any quarter** for pada-cheda: each word on its own line with its meaning
  in the language you're reading.
- **Switch language live** (English / नेपाली / हिन्दी) — titles, translations, word
  meanings and interface all follow, with Devanagari numerals in ne/hi.
- **Search** all 700 verses by number (`2.47` or `२.४७`), Sanskrit, or translation.
- **Favourites**, **random verse**, **verse of the day**.
- **Mobile-first**: swipe between verses, hardware back button closes the verse sheet,
  safe-area insets, works offline after the first visit.

## Content

| | |
|---|---|
| Chapters · verses | 18 · 700 |
| Themes · parts | 182 · 559 |
| Word-instances glossed | 9,480 — each with English, Nepali **and** Hindi meanings |
| Languages | English, नेपाली, हिन्दी (no English fallback anywhere) |

---

## Repository layout

```
index.html              the built app — GENERATED, do not edit
manifest.webmanifest    PWA manifest (Add to Home Screen)
sw.js                   service worker (offline cache)
icons + og-card.png     app icons and link-preview card

source/                 ← edit here
  build_gita.py           the builder: writes index.html
  gita_data*.py           verse text, themes and parts (English)
  themes_ne.py            Nepali theme/part titles + descriptions
  themes_hi.py            Hindi theme/part titles + descriptions
  translations_ne.py      Nepali literal + paraphrase for all 700 verses
  translations_hi.py      Hindi literal + paraphrase for all 700 verses
  gloss_ne.py             Nepali word-meanings
  gloss_hi.py             Hindi word-meanings
  padachheda_ch*.py       per-pāda word splits, chapter by chapter
  i18n_ui.py              interface strings (en/ne/hi)
  ch*.json                Devanagari + IAST verse text
  gita_conv.py            ITRANS → Devanagari/IAST conversion, metre detection
  check_padas.py          pāda verification

rebuild.sh              build + run both test suites
run_gita_app.js         362 assertions on the built document
browser_checks.py       41 live-browser checks (rendering, i18n, touch, offline)
```

`index.html` is a **single-file application**: the app shell and all content compile
into one document. That is deliberate — it makes the app work offline immediately and
lets it be shared as a single file. Gzipped it transfers as ~670 KB.

---

## Building

```bash
python3 build.py        # works anywhere, including from an IDE's Run button
bash rebuild.sh         # same thing, if you have a shell
```

`build.py` exists because a `.sh` file cannot be launched directly from most IDEs.
Both do the same work. Options:

```bash
python3 build.py            build + verify   (what you normally want)
python3 build.py --fast     build only, skip the tests
python3 build.py --serve    build, verify, then serve at http://localhost:8000
```

### Fixing content

Edit the file in `source/`, then run `python3 build.py`. Never edit `index.html`.

| what you want to fix | file |
|---|---|
| how a verse splits into its four pādas | `source/padachheda_ch*.py` |
| a word's meaning (ne/hi) | `source/gloss_ne.py`, `source/gloss_hi.py` |
| a translation | `source/translations_ne.py`, `source/translations_hi.py` |
| theme/part titles and ranges | `source/gita_data*.py` (en), `themes_ne.py`, `themes_hi.py` |
| the Devanagari or IAST of a verse | `source/ch*.json` |

The verse as you read it on screen is printed **verbatim** from `source/ch*.json`.
The text is stored as segments separated by `।` — two verse lines, plus a speaker
where there is one — and the app carries those segments through untouched, in order.
So fixing a verse is a one-line edit to the JSON, and the display is guaranteed to
match it. The four-pāda split shown inside the verse popup is separate data
(`source/padachheda_ch*.py`) and does not affect the flowing verse.
| interface wording | `source/i18n_ui.py` |

`check_padas.py` runs on every build and re-derives each pāda from its split words
using external sandhi, so a mistake in `padachheda_ch*.py` is caught immediately:

```
pādas checked: 2800 | residual flags: 0
```

If a check fails, the build says so and exits non-zero — fix the source and run again.

That runs the builder, regenerates `index.html` and `site/`, then executes both test
suites. A clean run reports:

```
source-integrity issues: NONE ✓
pādas checked: 2800 | residual flags: 0
run_gita_app.js: 362 assertions passed, 0 failed      ALL GREEN ✓
browser_checks.py: 41 passed, 0 failed                ALL GREEN ✓
```

`browser_checks.py` needs Playwright (skipped automatically if absent):

```bash
pip install playwright && python3 -m playwright install chromium --with-deps
python3 browser_checks.py --serve                     # test locally, incl. offline
python3 browser_checks.py https://chapain.github.io/Bhagavad-Gita/
```

### What the tests cover

**`run_gita_app.js`** — 18 chapters · 700 verses · 182 themes · 559 parts; trilingual
coverage with no English fallback; script purity (no Latin residue in ne/hi fields);
every pāda's words present; metre badges; the mobile layer; Devanagari-numeral rules;
Open Graph tags, manifest and service-worker invariants; and content regression locks
on specific verses.

**`browser_checks.py`** — drives a real browser: rendering, navigation, English
wording, Devanagari numerals, search in both scripts, swipe and back-button, four
viewport sizes, and a genuine offline reload with the network disconnected.

---

## Editing content

Never edit `index.html`. To change a theme title, a translation or a word meaning,
edit the matching file in `source/` and run `bash rebuild.sh`.

The count locks in `run_gita_app.js` are intentional: if you add or remove a theme or
part, the suite fails until you update the expected number. That is the check catching
your change, not a bug — update the lock deliberately.

To publish: upload the built files (`index.html`, `manifest.webmanifest`, `sw.js`, and
the icons) to the repository root. GitHub Pages serves them within a minute or two.
Note that Pages sets a 10-minute cache, so hard-refresh to see an update immediately.

---

## Text

Verse text follows the **Śaṅkara-bhāṣya** recension. Where a variant reading exists the
bhāṣya reading is used — for example BG 1.8 reads *saumadattis tathaiva ca*, not the
*jayadrathaḥ* variant.

Metres are detected from syllable counts: 644 verses are anuṣṭubh (4 quarters of 8),
51 are triṣṭubh (4 of 11), and 5 are irregular.

---

Created by **Dhruba Chapain**, Pokhara, Nepal.

© 2026 Dhruba Chapain. All rights reserved.

ॐ तत् सत्
