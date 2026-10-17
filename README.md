# Bhagavad Gita — Interactive Study

> **Resuming this project after a break — or handing it to someone else?**
> Read **[PROJECT.md](PROJECT.md)** first. It records the one rule that governs
> the codebase, the editorial decisions already settled (and why), every build
> check and the bug that caused it, and the mistakes not to repeat. The test
> suite verifies that its facts stay accurate.


**Live app → https://chapain.github.io/Bhagavad-Gita/**

A complete, offline-capable study edition of the Bhagavad Gītā — **18 chapters, 700
verses** — aligned to the Śaṅkara-bhāṣya readings, in **English · नेपाली · हिन्दी**,
with word-by-word meanings for every word in all three languages.

Open the link, then use your browser menu → **Add to Home Screen**. It installs like an
app and works with no internet connection.

---

## What it does

- **Browse** chapters → themes → verses, or start from the three ways
  (कर्मयोग 1–6 · भक्तियोग 7–12 · ज्ञानयोग 13–18). Each chapter opens with a
  collapsible theme outline, with the verse range before the title; expand a
  theme to reveal its description and verse titles.
- **Every verse in its four quarters (pādas)** — Devanagari, IAST transliteration,
  a literal translation and a flowing paraphrase.
- **Study word by word** — open the four-quarter control directly below a verse,
  then tap any quarter to reveal its words and meanings in the language you're reading.
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
| Themes · parts | 169 · 700 |
| Word-instances glossed | 9,484 — each with English, Nepali **and** Hindi meanings |
| Languages | English, नेपाली, हिन्दी (no English fallback anywhere) |

---

## Repository layout

```
index.html              the built app — GENERATED, do not edit
manifest.webmanifest    PWA manifest (Add to Home Screen)
sw.js                   service worker (offline cache)
icons + og-card.png     app icons and link-preview card
404.html                not-found page; recovers #v= / #chapter= deep links
chapter.css             shared stylesheet for the 18 chapter pages (4 KB)
noto-deva-regular.woff2 Devanagari face for the chapter pages — a real file,
                        fetched once and shared by all 18 (was inlined as
                        base64, which made chapter.css 60 KB)
chapter/N/              full-text landing page per chapter (crawler-facing)
                        Verse links are /chapter/N/#vN.NN — the page opens
                        the theme and verse disclosures, then highlights that verse.

source/                 ← edit here
  build_gita.py           builds the app and validates canonical chapter data
  schema.py               strict chapter JSON keys, types, IDs, ranges and flow shape
  app.html / app.css / app.js  shell templates; CSS and JS stay inline
  ch1.json … ch18.json    one compact canonical content file per chapter
  i18n_ui.py              interface strings (en/ne/hi; 183 keys each)
  study_map_contract.json  all 18 reviewed maps + safe legacy-progress data
  verify.py               shared text/transliteration helpers
  check_padas.py          verifies word splits against the pādas
  check_paraphrase.py     paraphrases must not echo their literals
  check_translations.py   banned readings, shape, words printed twice
  prove_data_only.py      proves source edits reach the built artifacts
  check_seo.py            sitemap/robots proof (`--live` also fetches the site)
  check_site_health.py    chapter pages, CSS vars, og: tags, offline, a11y
  check_study_structure.py approved story maps, trilingual pearls, theme sizes

tests/                   mutation and regression checks
rebuild.sh              delegates to build.py (the same full validations)
run_gita_app.js         776 assertions on the built document
browser_checks.py       251 live-browser checks (Learn/Play, storage, i18n, touch, offline)
```

`index.html` remains a **single-shell split site**. Its document, stylesheet and
client runtime are maintained as `source/app.html`, `source/app.css` and
`source/app.js`; `source/build_gita.py` fills their build-time placeholders and
inlines the CSS and JavaScript, so the browser makes no extra shell-asset
requests. The shell is about 72 KB gzipped and loads the verses from 18
`data/ch<N>.js` files in parallel; the service worker precaches them. After the
first visit everything is cached, so the app runs offline and installs to the
home screen. Share it by link.

---

## The study-guide map

Themes carry the chapter's story; verse cards are its individual pearls.
All **18 chapter maps have been reviewed**: Chapters 1, 2 and 17 keep their
approved maps, and the other 15 have genuine structural revisions. The book
has **169 themes and 700 one-verse parts**. Most themes hold no more than six
verses; three seven-verse arguments/portraits stay together deliberately.

`STUDY_MAPS.md` gives every storyline, range and before/after count. The exact
reviewed maps are regression-locked in `source/study_map_contract.json`.
Changing the thread does not change Sanskrit, translations, word meanings,
or the existing trilingual verse titles/descriptions and verse identities.

Saved learning progress follows retained verse ranges, not old theme indexes.
When a map changes, the new story needs reviewing; held verses, favourites and
notes survive. `source/check_study_structure.py --explain` lists the longer
passages, and the Python/Node mutation tests prove the preservation/migration
contracts reject regressions.

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

**All chapter content now lives in one canonical JSON file per chapter.** Edit
`source/ch<N>.json`, run `python3 build.py`, and the app and chapter pages are
rebuilt from that data. Never edit `index.html` or `data/ch<N>.js` by hand;
both are generated.

| what you want to fix | file |
|---|---|
| chapter names and summaries; themes/parts, titles and descriptions; verse text, translations, word glosses, pāda flow and colophon | `source/ch<N>.json` |
| interface wording (buttons and labels; 183 UI strings in each of three languages) | `source/i18n_ui.py` |
| shell structure, styling and client behavior | `source/app.html`, `source/app.css`, `source/app.js` |
| approved story maps and safe legacy-progress migration | `source/study_map_contract.json` |

The canonical schema deliberately has one copy of each value. Chapter names and
themes/parts use localized maps; English is not copied into separate `name`,
`sub`, `title` or `desc` fields. Each verse stores only `n`, `d`, `t`, `flow`,
`lits` and `paras`: display lines, speaker order and meter are derived from
those fields at runtime.

#### The verse you read

Each verse's `d` and `t` fields are its canonical Devanagari and IAST strings.
The app splits both on the danda `।`, pairs the segments in order and displays
them without joining, re-sandhi or other text reconstruction. An IAST segment
ending in `uvāca` is rendered as a speaker; it stays exactly where it occurs,
including the mid-verse position in 1.21 and 1.28. Every verse must yield two
non-speaker lines, and the build rejects mismatched Devanagari/IAST segments.
To correct a verse, edit its `d` and `t` strings in its chapter JSON.

#### The pāda split

The popup's four quarter-boxes and word-by-word glosses come from that same
verse's ordered `flow` array. A pāda item has its Devanagari, IAST, syllable
count, and five-field word rows (`deva`, `iast`, English, Nepali, Hindi):

```json
"flow": [
  {
    "k": "p",
    "d": "तेजः क्षमा धृतिः शौचम्",
    "t": "tejaḥ kṣamā dhṛtiḥ śaucam",
    "n": 8,
    "words": [["तेजः", "tejaḥ", "vigour", "तेज", "तेज"], ["क्षमा", "kṣamā", "forgiveness", "क्षमा", "क्षमा"]]
  }
]
```

Speaker items use `"k": "s"` and omit the syllable count. Both kinds appear in
`flow` in display order; the speaker's glosses live there too. To move a pāda
boundary, move the text in both scripts, adjust its `n`, and move the affected
word rows. The build checks that the pādas reconstruct the verse IAST, each
syllable count matches, and the word rows remain complete. The meter badge is
computed from these pāda counts; it is not a second stored value.

#### The build checks that your edit took effect

Every build validates that:

* the chapter/theme/part/verse records match the compact schema, with no
  duplicate labels or cached display fields;
* all translations and descriptions are present in English, Nepali and Hindi;
* every verse belongs to exactly one part and all 700 verse references resolve;
* the verse strings split into matching display segments and speakers;
* pāda text, word glosses and syllable counts agree.

`source/prove_data_only.py` also performs eight edit-and-restore proofs: a change
to chapter JSON must appear in the published data, and restoring the source
must restore the original build hash. `build.py` clears `__pycache__` before
every build so stale Python bytecode cannot hide an edit.

#### Dark mode

The app follows the phone's own light/dark setting. A ☾ / ☀ button in the
language bar overrides it, and that choice is remembered.

It is presentation only — no data file is involved. The colours live in two
blocks at the top of `source/app.css`: `:root` for light and
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

To verify that canonical edits reach the published artifacts, run:

```
python3 source/prove_data_only.py
```

It performs eight temporary edit-and-restore experiments: a verse string, a pāda,
a word gloss, English and Nepali translations, a Hindi theme title, a chapter
name, and an interface string. Each edit must appear in the built output and
change its content hash; after restoration, the final hash must match the
baseline byte-for-byte.

#### Content is data; code only builds and validates it

The chapter JSON contains the complete Sanskrit, translations, theme/part text,
word rows and colophon. The app derives only display conveniences from that
source: danda-separated reader segments and the meter badge from pāda syllable
counts. It does not generate verse text, translations or glosses. The old ITRANS
converter, freeze/override tools and their raw `.itx` source texts are gone.

The remaining helpers are small and check data rather than rewrite its meaning:

| file | what it does |
|---|---|
| `verify.py` | normalizes IAST and counts syllables for validation |
| `check_padas.py` | rebuilds each pāda from the word rows nested in `flow` |
| `check_paraphrase.py` | fails if any flowing paraphrase overlaps its literal by 80% or more |
| `check_translations.py` | checks built data for banned readings, Latin/spacing issues and repeated words; reports reviewed आ-form advice without blocking |
| `prove_data_only.py` | edits representative source fields and proves they reach the generated artifacts |

The builder enforces the compact schema and fails if a redundant or derived
field reappears in canonical chapter data.

---

## Editing content

Never edit `index.html`. To change a theme title, a translation or a word meaning,
edit the matching file in `source/` and run `bash rebuild.sh`.

The count locks in `run_gita_app.js` are intentional: if you add or remove a theme or
part, the suite fails until you update the expected number. That is the check catching
your change, not a bug — update the lock deliberately.

To publish: upload the built files (`index.html`, `manifest.webmanifest`,
`sw.js`, `sitemap.xml`, `robots.txt`, `chapter.css`, the `data/` folder, the
`chapter/` folder, and the icons) to the repository root. GitHub Pages serves
them within a minute or two.
Note that Pages sets a 10-minute cache, so hard-refresh to see an update immediately.
Share the site **by link** — `https://chapain.github.io/Bhagavad-Gita/`. The
service worker caches everything on the first visit, so it works offline and
installs to the home screen after that. (The split site cannot run from a
downloaded folder or `file://`; there is no single-file export.)

---

## Being found on Google

The page carries everything a crawler needs — a keyword-targeted `<title>`,
canonical URL, JSON-LD description, 18 generated **full-text chapter pages**
(every verse as static, crawlable text), `sitemap.xml` and `robots.txt`. But on a GitHub project page none of that
substitutes for telling Google the site exists. One time, in a browser:

1. Open [Google Search Console](https://search.google.com/search-console) and
   sign in.
2. **Add property → URL prefix** → `https://chapain.github.io/Bhagavad-Gita/`
3. Verify with the **HTML tag**: copy the token (the `content="…"` value),
   paste it into `source/gsc_token.txt`, rebuild and publish — the build emits
   the meta tag automatically. (Or use their HTML-file-upload method instead:
   upload the verification file to the repository root; no rebuild needed.)
4. **Sitemaps** → submit `sitemap.xml` (the app + all 18 chapter pages).
5. **URL inspection** on the site address → **Request indexing**.

**If Search Console says "Couldn't fetch":** the status is usually stale, or
the URL you typed is not the file. Run `python3 source/check_seo.py --live` —
it prints the published status code and content-type, parses the XML, fetches
every URL inside it, and tests the near-miss spellings. On this site the file
is fine (200, `application/xml`) and `sitemap.xml/` with a trailing slash is a
**404**, so submit exactly `sitemap.xml` — no slash, no query string.

Then get the link seen: set the GitHub repo topics (`bhagavad-gita`, `hinduism`,
`sanskrit`, `nepali`), and share it where readers are — r/Hinduism,
r/bhagavadgita, Quora, and Nepali Facebook groups. Indexing takes days, not
minutes; rankings on the long tail (e.g. *bhagavad gita in nepali*) take weeks.

---

## Text

Verse text follows the **Śaṅkara-bhāṣya** recension. Where a variant reading exists the
bhāṣya reading is used — for example BG 1.8 reads *saumadattis tathaiva ca*, not the
*jayadrathaḥ* variant.

Metres are detected from syllable counts: 644 verses are anuṣṭubh (4 quarters of 8),
51 are triṣṭubh (4 of 11), and 5 are irregular.

---

Created by **Dhruba Chapain**, Pokhara, Nepal. Built with AI tools, used under
the author's direction; the content was reviewed, corrected and approved by him
(see `LICENSE.md`).

© 2026 Dhruba Chapain. All rights reserved.

ॐ तत् सत्
