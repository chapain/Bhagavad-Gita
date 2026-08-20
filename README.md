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
  padas_ch*.py            the four pādas of every verse
  i18n_ui.py              interface strings (en/ne/hi)
  ch*.json                Devanagari + IAST verse text
  i18n_chapters.py        chapter names and blurbs (ne/hi)
  verify.py               two helpers used to check your data
  check_padas.py          verifies word splits against the pādas
  prove_data_only.py      proves the build renders data, never generates it

rebuild.sh              build + run both test suites
run_gita_app.js         394 assertions on the built document
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

**Every part of the app is meant to be corrected by hand.** Edit the file in
`source/`, run `python3 build.py`, and the app shows exactly what you wrote.
Never edit `index.html` — it is generated and your change would be overwritten.

| what you want to fix | file |
|---|---|
| the Devanagari or IAST of a verse | `source/ch*.json` |
| where a verse divides into pādas | `source/padas_ch*.py` |
| the word-by-word split and its English meanings | `source/padachheda_ch*.py` |
| a word's meaning in Nepali / Hindi | `source/gloss_ne.py`, `source/gloss_hi.py` |
| a verse translation (en) | `source/gita_data*.py` |
| a verse translation (ne / hi) | `source/translations_ne.py`, `source/translations_hi.py` |
| chapter names | `source/i18n_chapters.py` |
| theme and part titles, blurbs, verse ranges (en) | `source/gita_data*.py` |
| theme and part titles, blurbs (ne / hi) | `source/themes_ne.py`, `source/themes_hi.py` |
| interface wording (buttons, labels) | `source/i18n_ui.py` |

#### The verse you read

Printed **verbatim** from `source/ch*.json`. The text is stored as segments
separated by `।` — two verse lines, plus a speaker where there is one — and the
app carries those segments through untouched, in order. Nothing is re-joined or
re-derived, so the display cannot drift from the file. Fix a verse by editing
that one line of JSON.

#### The pāda split

The four quarter-boxes in the verse popup. This is **plain data** in
`source/padas_ch*.py` — one entry per verse, read straight through:

```python
"16.03": [
    ("p", "तेजः क्षमा धृतिः शौचम्", "tejaḥ kṣamā dhṛtiḥ śaucam", 8),
    ("p", "अद्रोहो नातिमानिता",      "adroho nātimānitā",        8),
    ("p", "भवन्ति सम्पदं दैवीम्",     "bhavanti sampadaṃ daivīm", 8),
    ("p", "अभिजातस्य भारत",         "abhijātasya bhārata",      8),
],
```

`("p", devanagari, iast, syllables)` is a pāda; `("s", devanagari, iast)` is a
speaker line. They render in the order written, which is why the speaker in 1.21
and 1.28 correctly appears between the two halves.

To move a boundary, move the word in both the Devanagari and the IAST and adjust
the two syllable counts. The build then checks that the pādas still spell the
verse in `ch*.json` and that every count is right, and stops with a clear message
if not — so the two files cannot drift apart.

#### The build checks that your edit took effect

Every build runs a **manual-edit audit** and stops if a source file says
something the app would not show:

* a verse with no Nepali or Hindi translation, which would silently show English
* an `ne`/`hi` theme file whose structure does not mirror the English one
* a verse that no part's range covers, making it unreachable in the app
* pādas in `padas_ch*.py` that no longer spell the verse in `ch*.json`
* a pāda whose syllable count does not match its text

```
pāda overrides applied: 1 ✓
manual-edit audit: NONE ✓
```

`build.py` also clears `__pycache__` before every build, so an edit can never be
masked by a stale compiled copy of a source file.

#### Dark mode

The app follows the phone's own light/dark setting. A ☾ / ☀ button in the
language bar overrides it, and that choice is remembered.

It is presentation only — no data file is involved. The colours live in two
blocks at the top of the CSS in `source/build_gita.py`: `:root` for light and
`html[data-theme="dark"]` for dark. Both define the same token names, so every
rule just uses `var(--x)` and nothing else changes.

Two deliberate choices, worth keeping if you edit the palette:

* **warm, not neutral** — a dark brown-black keeps the manuscript feel rather
  than looking like a generic app;
* **never pure black or pure white** — Devanagari has fine strokes, and maximum
  contrast makes them shimmer. The test suite fails the build if `#000` or
  `#fff` appears in the dark block.

All verse text passes WCAG AA in both themes (measured: 10.1:1 Devanagari,
7.3:1 transliteration, 15.1:1 translation on dark).

#### Proving the app only renders data

If you want to satisfy yourself that nothing is being generated any more:

```
cd source
python3 prove_data_only.py
```

It runs two opposite experiments and restores everything afterwards:

1. **Breaks the generator** — replaces the four functions that used to produce
   displayed text with ones returning the word `SABOTAGED`, then rebuilds. If the
   app still generated anything, `index.html` would change. It does not: the file
   comes out byte-identical and the word never appears.
2. **Changes the data** — edits one pāda in `padas_ch16.py` and rebuilds. The new
   text appears in `index.html`, so the data file wins and is not overwritten.

```
  PASS  generator broken -> output unchanged
  PASS  data changed -> output changes
  CONCLUSION: the app renders the data files; it does not generate them.
```

The quickest informal version of the same check: note the hash printed by
`build.py`, edit any data file, rebuild, and confirm the hash moved and your
words are on the page.

#### No code generates content

The app's content is complete, so the build does not derive anything — it reads
the data files and renders them. The old ITRANS converter and metre-splitter
(`gita_conv.py`), the freeze tool (`freeze_padas.py`), the override workaround
(`pada_overrides.py`) and the unused `sandhi.py` have all been **deleted**, along
with the raw `.itx` source texts they were built from. The test suite asserts
they stay gone and that the builder never calls a conversion function.

What remains is small and only ever *checks* your data:

| file | what it does |
|---|---|
| `verify.py` | flattens IAST accents and counts syllables, so the build can compare your pādas against `ch*.json` |
| `check_padas.py` | rebuilds each pāda from its word split to catch a typo in `padachheda_ch*.py` |
| `prove_data_only.py` | edits each kind of data in turn and proves the change reaches the page |

None of them can change what the app shows.

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
