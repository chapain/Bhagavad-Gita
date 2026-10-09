# HANDOFF.md — start here

**New AI session (Arena or any other): read this file first.** It is the short,
*current* status: where the work stands, what was found, what to do next.
`PROJECT.md` is the long history — read its **§8 “Working with the owner”**
before you talk to the owner.

| | |
|---|---|
| Last updated | 2026-10-09 (UTC) |
| Updated by | Arena session on branch `arena/7d566d9b-bhagavad-gita` |
| Base commit | `5010648` on `main` (merge of PR #11, step 1.7) |
| Owner | Dhruba Chapain, Pokhara |
| Live site | https://chapain.github.io/Bhagavad-Gita/ |

> **Rule for every session:** before you stop, update §1, tick boxes in §6 and
> add one line to §8. Keep this file short; long history belongs in PROJECT.md.

---

## 1. Where we are

- **2026-10-09 — Phase 1 steps 1.1–1.7 complete.** Step 1.4 made
  `source/check_padas.py` a build-failing strict validator. It losslessly
  transliterates all 9,366 word entries and compares each word’s Devanagari
  with its own IAST; it also checks all 2,800 pādas against their word splits
  and runs a second, diacritic-preserving line check.
- The validator’s conventions remain explicit and narrow: anusvāra/homorganic
  nasal spelling, final anusvāra, 2.06 `यत् वा` / `yad vā`, and 9.16 visarga
  sandhi `क्रतुः` / `kratur`. Its checks preserve vowel length, retroflexion,
  and ś/ṣ/s. Regression tests prove 13.27 `avinaśyantam` passes while the
  incorrect `avināśyantam` fails; do not reverse the short-a correction.
- Step 1.5 gives search a mark-preserving NFD key plus a separate, documented
  ASCII fallback over the IAST field only (see §5.4). Search and favorites use
  singular/plural count labels in English, Nepali and Hindi.
- Step 1.6 corrected `LICENSE.md` to the verified counts: **9,484** word
  glosses (9,366 verse words + 118 speaker words), **169** themes and **700**
  parts (was 9,480 / 182 / 558). It also removed the README “Editing in your
  browser” section, which documented `edit.py` and `editor.html`; neither file
  exists, and the editor is not restored. The README’s “202 UI strings” figure
  moved into the “Fixing content” table so the document test still holds.
- Step 1.7 fixed the one Hindi grammar fault Dhruba had caught in the 2.47
  paraphrase (`translations_hi.py`): “कुछ न करने **की** आलस्य में” → “**के** आलस्य में”,
  since आलस्य is masculine and is governed by में (oblique). Cross-checked against
  `ch2.json` (मा ते सङ्गोऽस्त्वकर्मणि) and the `padachheda_ch2.py` split
  (सङ्गः = attachment, अकर्मणि = in inaction). The “आलस्य” gloss of अकर्मणि is
  the paraphrase’s own interpretive word, left as it was; the 390 px Hindi
  render was re-shot and reads correctly.
- **GitHub (verified 2026-10-09):** PR #11 is **merged** (02:43 UTC) into `main`
  at `5010648`, which is this session’s base, and it carries step 1.7’s commit
  `b5a5bcd`; `source/translations_hi.py` on `main` already reads “कुछ न करने के
  आलस्य”, so step 1.7 is not repeated. PR #11 does **not** contain the §7.1
  decision (the previous session recorded it after the merge and could no longer
  push), so this session’s first commit writes it into the repo.
- **Verification (step 1.7):** `python3 build.py` passed: 9,366 strict word checks, 2,800
  strict line and reconstruction checks (0 flags), 2,100 paraphrase pairs,
  6 SEO checks, 572 site-health checks, 9,658 study-structure checks, 19 Python
  tests, 802 document assertions, 15 learning-map migration tests and 7 search
  regression tests. That session set up Playwright + `@sparticuz/chromium` per
  §4, so the 162 browser checks ran and passed too; the rebuild touched only
  `data/ch2.js` and the `sw.js` cache id (a paraphrase-text change).
- **§7.1 is decided** (owner, 2026-10-09): the UI framework wording “तीन निष्ठा /
  तीन निष्ठाएँ” becomes **तीन मार्ग**, and the three cards/tabs are prefixed
  **कर्ममार्ग · भक्तिमार्ग · ज्ञानमार्ग**. The full spec, rationale, spelling
  decisions and out-of-scope list are in §7.1; step 1.8 implements it and no
  verse-level निष्ठा is touched.
- **Next:** finish step 1.8 (§7.1) in this session, then stop. Step 1.9 (the
  18.66 and 15.7 paraphrases) stays blocked on §7.2. Other editorial decisions
  remain listed in §7.

## 2. Resume in five minutes

1. Read §1, §6 and §7 here, then `PROJECT.md` §8.
2. Run `python3 build.py`. It must pass, and `git status` must be clean afterwards
   (the build is deterministic).
3. Save Appendix A as `/tmp/audit.py` and run `python3 /tmp/audit.py` from the
   repo root. It lists the open data errors; its output shrinks as they are fixed.
4. Agree the next item with the owner, then work in small batches he can
   spot-check. For every change, show evidence: the verse, the word list and a
   390 px screenshot.
5. Before ending, update this file (§1, §6, §8), commit and push to your session
   branch, and open or refresh a pull request to `main`. New sessions start from
   `main`, so this file reaches them only after it is merged.

## 3. Map — what to edit

Everything the browser loads is **generated** by `source/build_gita.py`.
**Never hand-edit** `index.html`, `data/`, `chapter/`, `v/`, `sw.js` or `404.html`.
Edit `source/`, rebuild, and commit the source and the generated files together.

| Content | File |
|---|---|
| Verse text (Devanagari + IAST) | `source/ch<N>.json` |
| Pāda (quarter) split of each verse | `source/padas_ch<N>.py` |
| Word split + English word meanings | `source/padachheda_ch<N>.py` |
| Nepali / Hindi word meanings | `source/gloss_ne.py`, `source/gloss_hi.py` — keyed by IAST form only (see §5.2) |
| English titles, literal, paraphrase, descriptions, themes | `source/gita_data.py`, `source/gita_data<N>.py` |
| Nepali / Hindi literal + paraphrase | `source/translations_ne.py`, `source/translations_hi.py` |
| Nepali / Hindi theme and verse titles | `source/themes_ne.py`, `source/themes_hi.py` |
| UI strings (en/ne/hi) | `source/i18n_ui.py`, `source/i18n_chapters.py` |
| All app HTML/CSS/JS | inside `source/build_gita.py` (one Python string, about lines 493–4072) |

Gotchas:
- `source/learn_block.py` is **not used**. It is imported at `build_gita.py:42`
  but never applied; the real Learn/Play code lives inside `build_gita.py`, and
  the two copies have drifted apart. Editing `learn_block.py` changes nothing.
- **Per-word override already exists.** `i18n_word()` (`build_gita.py:141`)
  keeps any word entry written with five fields, `[deva, iast, en, ne, hi]`,
  instead of looking up the dictionaries. Use it for context-correct meanings.
- `source/verify.py:norm1()` strips diacritics before comparing, and
  `check_padas.py` uses it. That is why the errors in §5.1 passed every check.

## 4. Build and test

```bash
python3 build.py          # build + all checks (~7 s without the browser step)
python3 build.py --fast   # build only
```

The browser step (162 checks) runs only when `playwright` is importable.
`playwright install chromium` is blocked in the Arena sandbox; this works instead.
Nothing below is committed, so redo it for each new sandbox:

```bash
python3 -m venv /home/user/.venv && /home/user/.venv/bin/pip install -q playwright pillow
mkdir -p /home/user/.cache/tools && cd /home/user/.cache/tools && npm i -s @sparticuz/chromium@153
echo "import c from '@sparticuz/chromium'; console.log(await c.executablePath());" > getexe.mjs
node getexe.mjs           # unpacks the browser to /tmp/chromium
node -e "const z=require('zlib'),f=require('fs');f.writeFileSync('/tmp/al2023.tar',z.brotliDecompressSync(f.readFileSync('node_modules/@sparticuz/chromium/bin/al2023.tar.br')))"
mkdir -p /tmp/al2023x && tar -xf /tmp/al2023.tar -C /tmp/al2023x
cd /home/user/Bhagavad-Gita
export LD_LIBRARY_PATH=/tmp/al2023x/lib:/tmp GITA_CHROMIUM_EXECUTABLE=/tmp/chromium \
       GITA_CHROMIUM_ARGS="--no-sandbox --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --disable-dev-shm-usage"
/home/user/.venv/bin/python build.py      # now includes the browser checks
```

Do not add `--single-process` or `--no-zygote`: they crash on a second browser
context. To preview the app, serve the repo root with
`python3 -m http.server 8000 --bind 0.0.0.0`.

## 5. Findings (verified 2026-10-08)

Re-check the numbers with Appendix A.

### 5.1 Text errors (Phase 1)

| Verse | Wrong | Right | Fix in |
|---|---|---|---|
| 7.12 | राजसास्तमसाश्च / rājasāstamasāśca | राजसास्तामसाश्च / rājasāstāmasāśca | `ch7.json`, `padas_ch7.py` (the app's own word split already has तामसाः) |
| 9.13 | महात्मनस्तु / mahātmanastu | महात्मानस्तु / mahātmānastu | `ch9.json`, `padas_ch9.py` (the split already has महात्मानः) |
| 11.27, 11.28, 11.29 | वक्राणि (“crooked”) | वक्त्राणि (“mouths”); the IAST is already vaktrāṇi | `padachheda_ch11.py` |
| 17.6 | कर्षयन्तः | कर्शयन्तः; the IAST is already karśayantaḥ | `padachheda_ch17.py` |
| 13.27 | IAST `avināśyantam` (long ā) | `avinaśyantam` (short a); Devanagari अविनश्यन्तम् and the verse line/pāda already use short a | `padachheda_ch13.py`, `gloss_ne.py`, `gloss_hi.py` (fixed in step 1.3) |
| 1.1 | समवेता | समवेताः; the IAST is already samavetāḥ | `padachheda_ch1.py` |
| 2.14 | आपायिनः | अपायिनः (āgama + apāyinaḥ) | `padachheda_ch2.py` |

Also:
- Anusvāra is spelled ṃ in verse text but ṁ in word lists. Pick one.
- Chapter colophons exist only for chapters 1–2 (the `"colophon"` field in
  `ch1.json` and `ch2.json`). They start with a broken `Oं` (should be ॐ) and
  are never shown in the app.

### 5.2 Nepali/Hindi word meanings ignore context (Phase 2)

`build_gita.py:144` does `GLOSS_NE.get(i, en)`: one meaning per IAST form,
whatever the verse. 674 forms carry more than one English sense (4,532 of the
9,366 verse-word instances), yet each gets a single Nepali/Hindi meaning.
Clear errors:

- **`te` = “they” → तिम्रो/तुम्हारा (“your”)** in 26 verses: 1.33, 2.6, 3.13,
  3.31, 5.19, 5.22, 7.12, 7.14, 7.28–30, 8.17, 9.20–21, 9.23–24, 9.29, 9.32,
  10.10, 12.2, 12.4, 12.20, 13.25, 13.34, 16.8, 16.17.
- **`me` = “to me” → मेरो/मेरा** where the sense is tell / show / offer *to me*:
  2.7, 5.1, 9.26, 11.4, 11.45 (6.30 borderline).
  - Not errors: *sa me priyaḥ* (12.14–20, 18.64–69), where मेरो प्रिय is good Nepali.
  - In 11.45, *mano me* (“my mind”) and *darśaya me* (“show to me”) both
    become मेरो, while the English is right for both.
- `param` “hereafter” → परम (“supreme”) in 2.12.
- `bhūtāni` “spirits” → प्राणीहरू (“living beings”) in 9.25.
- `yogam` “sovereignty/power” → योग in 10.7 and 11.8. This rendering is
  traditional but opaque.

**Fix path (no code change needed):** write five-field entries inline in
`padachheda_ch<N>.py`, e.g. `["ते", "te", "they", "तिनीहरू", "वे"]`. Only two
such entries exist today. Start with te, me, param, bhūtāni, yogam, tat and yat,
then work through the rest of the 674 forms.

### 5.3 Interpretation and framing (owner decides)

- **“तीन निष्ठा / तीन निष्ठाएँ”** clashes with 3.3 *loke ’smin dvividhā niṣṭhā*
  (two) and with Śaṅkara, whose commentary rests on exactly two.
  - Where: UI keys `welcome_sub`, `welcome_foot`, `sections_title` and
    `sections_sub` in `i18n_ui.py` (ne + hi). The English “Three Ways” is milder.
  - Suggestion: keep the three groups of six chapters but call them
    ṣaṭkas/kāṇḍas (Madhusūdana: karma · upāsanā · jñāna, or tvam · tat · asi).
  - **Decided 2026-10-09 — see §7.1:** the UI keeps the three six-chapter groups
    but says **तीन मार्ग** and prefixes the cards **कर्ममार्ग / भक्तिमार्ग /
    ज्ञानमार्ग**; the ṣaṭka/kāṇḍa naming was not taken. Implemented in step 1.8
    as a value-only i18n change (25 strings, keys and the 202-key count
    unchanged). Verse-level निष्ठा — 3.3 द्विविधा निष्ठा, 5.17 तन्निष्ठाः, 17.1,
    18.50, their glosses and the theme prose — stays exactly as it is.
- **Paraphrases that lean away from Śaṅkara:**
  - 18.66 “Give up all other paths” (`gita_data18.py:254`). Śaṅkara reads it as
    all dharma *and* adharma, i.e. all action.
  - 15.7 “An eternal spark of myself” (`gita_data15.py:52`). Śaṅkara insists on
    *aṃśa iva*, “as if a part”. That file's header claims alignment with the
    Śaṅkara-bhāṣya.
  - The 6.47 title “Most yoked” is a calque.
- **2.47 Hindi paraphrase:** “कुछ न करने की आलस्य” → “के आलस्य”, since आलस्य is
  masculine (`translations_hi.py:194`). (Fixed in step 1.7.)
- **Duplicate descriptions:** 593 of 700 English verse descriptions are
  identical to the literal translation (Nepali 566, Hindi 592), so the Study
  guide repeats itself.
- **No Śaṅkara explanation anywhere.** Suggestion: short notes on about 25 pivot
  verses, drawn from A. Mahadeva Sastry's 1897 English translation of the
  bhāṣya (public domain).

### 5.4 Search (Phase 1 step 1.5 complete)

The search matcher now NFD-normalizes its exact key, so NFC and NFD IAST
queries compare equally without deleting combining marks. A separate fallback
is used only for queries with no combining diacritics and compares against the
IAST verse field only, not its translations. Its explicit equivalences are
ā/ī/ū with a/aa, i/ee, u/oo; ṛ/ri; ś/ṣ/sh; ṇ/n; and c/ch. Both keys ignore
whitespace. This restores ASCII searches such as “krishna”, “karmanye
vadhikaraste”, “dharmakshetre”, “yada yada hi dharmasya” and “sarvadharman
parityajya”. Marked IAST queries stay exact, so they can still distinguish
short/long vowels, ś/ṣ and dental/retroflex consonants. These search folds are
separate from — and do not weaken — the strict data validator.

`doSearch()` and favorites now render `resultCountLabel()`: singular/plural
nouns are selected for English, Nepali and Hindi, including the visible “1
result” rather than “1 results”. Results remain in canonical verse order;
ranking was not part of step 1.5.

### 5.5 UX at phone width (390 px)

- **Chrome:** the header and toolbar take about 315 px (37 % of the screen).
  In English, “Favorites” wraps onto its own row.
- **Chapter page:**
  - The breadcrumb wraps to three lines and mixes scripts (“Chapter 2 · अर्थ”).
  - “Verses with translation” has no theme headings or verse titles, and
    “Study guide” has no Sanskrit.
  - Proposal: one merged view (themes as headings, verses beneath) with
    “Learn by heart” as a button, and no mode chooser.
- **Verse sheet:**
  - The controls (metre, text size, share, favourite) sit above the verse.
  - The verse is never shown whole on a phone; it appears as four “Quarter” boxes.
  - Word meanings are a list about 1,000 px tall. Proposal: interlinear, with
    each meaning under its word.
  - A disabled “Hide meanings” button, a dangling “·”, and IAST daṇḍas showing as “|”.
- **Play:** it promises “Hear a śloka” (`play_sub`) but there is no audio
  anywhere. One button label is a lowercase “home”.

### 5.6 Learning design

Good: the story comes first; the memory ladder (full → first words → half
hidden → from the heart); pāda reordering; missed items come back.

Missing:
- audio;
- review across days (“Mark held” never fades);
- recall drills (every drill is multiple choice or reordering);
- the ladder hides split dictionary forms, not the chanted line;
- an on-ramp for beginners (“Start here”, “Gītā in 18 verses”);
- export/backup. Personal notes already exist (on favourites, stored as
  `gitaFavNotes`), but favourites, notes and Learn progress live only in this
  browser's `localStorage`, and a cleared browser loses them.

### 5.7 Code and docs

- `build_gita.py` is 4,772 lines, with about 3,580 lines of HTML/CSS/JS in one
  Python string, 151 global JS functions and inline `onclick` handlers.
- About 180 checks assert exact source text, e.g.
  `"if(shownForms[x[0]]) return;" in idx` in `check_site_health.py` and many
  `html.includes(...)` calls in `run_gita_app.js`. They break on any refactor,
  yet missed the content errors. Replace them gradually with behaviour tests
  and strict data validators.
- **Dead or stale files:**
  - `source/learn_block.py`: about 100 lines have drifted from the real copy.
  - `source/dataio.py`: nothing imports it.
  - `shoot_choose.py`: screenshots a page that has been retired.
  - `UPLOAD.md`: stale (“222 themes”).
  - `README.md` documented `edit.py` and `editor.html`, which do not exist
    (section removed in step 1.6). `UPLOAD.md` and `PROJECT.md` still mention
    the editor.
- **Wrong counts (fixed in step 1.6):** `LICENSE.md` said 9,480 word glosses, 182 themes
  and 558 parts. The verified figures are 9,484 (9,366 verse words + 118 speaker
  words), 169 and 700.
- **Data:**
  - One verse's content is spread over about ten source files.
  - `data/ch*.js` is 5.3 MB raw (663 KB gzip), and all of it is fetched
    shortly after first paint.
  - 43 % is redundant (`padas` duplicates `flow`, `lines` repeats `d`/`t`,
    `meter` repeats `mt`, and descriptions duplicate the literals). Without it
    the data is 3.0 MB.

## 6. Plan — status board (tick as you go)

**Phase 1 — Correctness (1–2 days)** · in progress (1.1–1.7 done)
- [x] 1.1 Fix the verse text in 7.12 and 9.13 (source and matching pāda lines).
- [x] 1.2 Fix word-list spellings: 11.27–29, 17.6, 1.1 and 2.14.
- [x] 1.3 Fix 13.27’s IAST spelling and update its Nepali/Hindi gloss keys.
- [x] 1.4 Add a strict validator that fails the build. Check each word’s
      Devanagari against its own IAST, and each pāda line against its word
      split, without flattening diacritics. Appendix A §1–2 is the starting point.
- [x] 1.5 Search: NFD plus explicit spelling folds; fix singular/plural result wording.
- [x] 1.6 Fix the `LICENSE.md` counts (9,484 / 169 / 700); removed the stale README editor section (editor not restored).
- [x] 1.7 Fix the Hindi grammar in the 2.47 paraphrase (की → के आलस्य).
- [ ] 1.8 Replace “तीन निष्ठा / निष्ठाएँ” with the owner’s मार्ग wording — decided
      2026-10-09, full spec in §7.1 (in progress in this session).
- [ ] 1.9 Revisit the 18.66 and 15.7 paraphrases after the owner’s decision (§7.2 — still open).

**Phase 2 — Meaning**
- [ ] 2.1 Context-correct Nepali/Hindi meanings via five-field entries (§5.2).
- [ ] 2.2 Drop duplicate descriptions (show nothing rather than a copy).
- [ ] 2.3 Colophons for all 18 chapters, shown at the end of each chapter.
- [ ] 2.4 A “Start here” page and a “Gītā in 18 verses” path.
- [ ] 2.5 Śaṅkara notes on about 25 pivot verses.

**Phase 3 — Simplify the UI**
- [ ] 3.1 One chapter view: themes as headings, verses beneath.
- [ ] 3.2 Verse sheet: the whole verse first, then the meaning, interlinear
      words, and the controls in a “⋯” menu.
- [ ] 3.3 Slim header and a bottom tab bar.

**Phase 4 — Simplify the code**
- [ ] 4.1 Split `build_gita.py` into `app.html`, `app.css` and `app.js` templates.
- [ ] 4.2 Delete the dead files in §5.7 (with the owner's OK).
- [ ] 4.3 One data file per chapter holding everything about each verse; drop
      the redundant fields.
- [ ] 4.4 Behaviour tests instead of source-string checks.

**Phase 5 — Grow**
- [ ] 5.1 Audio: one recitation per verse, loaded only when needed, with pāda timings.
- [ ] 5.2 Spaced review across days.
- [ ] 5.3 Recall drills; a ladder on the chanted line.
- [ ] 5.4 Export/import of favourites, notes and Learn progress (notes on
      favourites already exist).

## 7. Decisions

Phase 1 is selected (2026-10-08). §7.1 is decided; §7.2–§7.7 remain open.
Numbering follows the old list, so “§7.1” and “§7.2” mean the same choices as
before.

### 7.1 “तीन निष्ठा” → “तीन मार्ग” — **DECIDED (owner, 2026-10-09)** · status: pending implementation by step 1.8

**Decision.** The three six-chapter groups keep their shape, but the UI calls
them **mārga**, not niṣṭhā. The Nepali and Hindi framework wording becomes
**तीन मार्ग**, and the three section cards and their tabs are prefixed
**कर्ममार्ग · भक्तिमार्ग · ज्ञानमार्ग** in *all three* languages — the English
cards keep their “· The Way of Karma/Bhakti/Jñāna” suffix, and the English body
text keeps “The Three Ways” / “Way of …”. This is a **value-only i18n change**:
every key stays and the key count stays at **202** (`run_gita_app.js:102`
asserts it).

**Why.** निष्ठा is the Gītā’s own verse-level word: 3.3 *loke ’smin dvividhā
niṣṭhā* says **two**, and 5.17 *tanniṣṭhāḥ*, 17.1 *teṣāṃ niṣṭhā tu kā kṛṣṇa*
and 18.50 *niṣṭhā jñānasya yā parā* use it of one person’s steadfastness. A UI
that announces “three niṣṭhās” contradicts the text it frames (and Śaṅkara,
whose bhāṣya rests on exactly two). मार्ग makes no such claim, and `guide_way`
already read “एउटा मार्ग छानेर…”, so the UI becomes self-consistent. The §5.3
ṣaṭka/kāṇḍa suggestion was considered and **not** taken: it renames the
six-chapter divisions instead of dropping the wrong word, and ṣaṭka is
unfamiliar to this app’s readers.

**Spelling (owner-approved).** Joined tatsama compounds in stem form —
**भक्तिमार्ग**, *not* the sandhi form भक्तमार्ग — matching the existing lists
“कर्म, भक्ति और ज्ञान”. मार्ग (masculine) in both Nepali and Hindi.

**Scope — 25 values in `source/i18n_ui.py`.**
- **EN** (3): only the Devanagari prefix of `sec_karma` → “कर्ममार्ग · The Way
  of Karma”, `sec_bhakti` → “भक्तिमार्ग · The Way of Bhakti”, `sec_jnana` →
  “ज्ञानमार्ग · The Way of Jñāna”.
- **NE** (11) and **HI** (11): `welcome_sub`, `welcome_foot`, `sections_title`,
  `sections_sub`, `sec_karma`, `sec_bhakti`, `sec_jnana`, `tab_karma`,
  `tab_bhakti`, `tab_jnana`, `back_ways`.
- Hindi `sections_sub` must agree with masculine मार्ग: “गीता के अठारह अध्याय
  तीन **मार्गों** में — कर्म, भक्ति और ज्ञान — एक **अगले** में परिपक्व **होते
  हुए**।” Nepali keeps its own construction (“तीन मार्गमा — …”).
- Unchanged on purpose: EN `welcome_sub`/`welcome_foot` (“three ways”),
  `sections_title` “The Three Ways”, `tab_*` “Way of …”, and `guide_way`.

**Out of scope — no verse-level निष्ठा is touched.** `ch3.json` 3.3 “द्विविधा
निष्ठा”, `ch5.json` 5.17 “तन्निष्ठाः”, the `niṣṭhā` and `tanniṣṭhāḥ` entries in
`gloss_ne.py` / `gloss_hi.py`, the 17.1 and 18.50 verse texts, pādas and
padachheda, and the theme prose about 3.3 or the three guṇas.

**Downstream bookkeeping, same change.** The comment at `build_gita.py`
~3377 (“the trail carries the Sanskrit niṣṭhā name … ‘कर्मनिष्ठा · The Way of
Karma’”) must quote the new card text, and `browser_checks.py:328` must assert
`"कर्ममार्ग" in cr[2]` with the message reworded to the mārga name — same
strength, new string. Generated files (`index.html`, `data/`, `chapter/`,
`sw.js`, `404.html`) are never hand-edited; `build.py` rebuilds them.

**Evidence required.** Before/after of every changed string, plus 390 px shots
of the Hindi and Nepali welcome tagline, the sections landing (three cards) and
a chapter page showing the way crumb, and one English sections landing to show
the Devanagari prefix. Then `grep -rn "तीन निष्ठा\|कर्मनिष्ठा\|भक्तिनिष्ठा\|ज्ञाननिष्ठा" source/
run_gita_app.js browser_checks.py README.md` must be empty.

### 7.2 Paraphrases of 18.66 and 15.7 — **OPEN (blocks step 1.9)**

How should the paraphrases of 18.66 (“Give up all other paths”) and 15.7 (“An
eternal spark of myself”) be revised, if at all? See §5.3: Śaṅkara reads 18.66
as all dharma *and* adharma, and insists on *aṃśa iva*, “as if a part”, for
15.7, whose file header claims alignment with the bhāṣya. Do not start 1.9
until the owner answers.

### 7.3–7.7 Still waiting on the owner

3. OK to add Śaṅkara notes (source: Mahadeva Sastry, 1897)?
4. Where audio would come from (licence, who records it).
5. OK to merge “Verses with translation” and “Study guide” into one view?
6. OK to delete the dead files in §5.7?
7. `PROJECT.md` §8 asks every session to deliver the full repo zip. With GitHub
   as the checkpoint, is that still wanted?

## 8. Session log (newest first, one line each)

- 2026-10-09 · `arena/f0f811fe-bhagavad-gita` · Phase 1 step 1.7: fixed the
  2.47 Hindi paraphrase in `translations_hi.py` — “कुछ न करने की आलस्य में” →
  “के आलस्य में” (आलस्य masculine, oblique before में), cross-checked against
  `ch2.json` and the `padachheda_ch2.py` split; no other Hindi line contains
  “की आलस्य”. Verified PR #10 merged at 02:14 UTC; latest `main` is `6ee58aa`
  (this session’s base), so 1.6 was not repeated. Full build green including
  162 browser checks (Playwright + sparticuz chromium per §4); 390 px Hindi
  render of the sheet re-shot. Stopped before 1.8 pending the owner’s §7.1
  wording choice.

- 2026-10-09 · `arena/a1d5250c-bhagavad-gita` · Phase 1 step 1.6: verified PR #9 merged
  at 02:08 UTC and `main` at `e89b78c` containing step 1.5 (`d2df966`, `f0d765d`), so no
  step 1.5 work repeated. LICENSE.md now says 9,484 / 169 / 700 (were 9,480 / 182 / 558).
  Removed the README editor section (edit.py/editor.html do not exist). Removing it
  dropped the only “202 UI strings” line, which `run_gita_app.js` checks in README;
  moved the figure into the Fixing-content table. Build green (802 document assertions,
  19 Python tests, 15 + 7 Node tests). Stopped before 1.7.
- 2026-10-09 · `arena/d4cdfd5b-bhagavad-gita` · Phase 1 step 1.5: NFD exact
  search plus an explicit ASCII fallback scoped to verse IAST; marked queries keep
  Sanskrit distinctions. Fixed singular/plural count nouns in en/ne/hi and added
  7 focused Node regressions. Build green (802 document assertions); separate
  Playwright/Chromium run passed 162 browser checks. Verified PR #8 merged and latest
  `main` at `bd4f5c3`; pushed commit `d2df966` and opened PR #9 to `main`
  (https://github.com/chapain/Bhagavad-Gita/pull/9). Stopped before 1.6.
- 2026-10-09 · `arena/42b88b5d-bhagavad-gita` · Phase 1 step 1.4: added
  build-failing strict checks for 9,366 Devanagari/IAST word pairs and 2,800
  pāda/word-split lines, with narrow explicit sandhi/spelling conventions and
  regression tests preserving 13.27’s short `a`. Full available build green;
  browser checks skipped (Playwright unavailable). Verified PR #7 merged and
  latest `main` at `3ccb222`. Stopped before 1.5.
- 2026-10-08 · `arena/d05a372a-bhagavad-gita` · Phase 1 step 1.3: corrected
  13.27’s word-list IAST from `avināśyantam` to `avinaśyantam` and renamed the
  Nepali/Hindi gloss keys. The verse line and Devanagari were already correct.
  Full build green (150 browser checks); audit no longer reports 13.27. The
  390 × 844 screenshot and rendered Nepali/Hindi glosses were checked. PRs #5
  and #6 are merged; Pages for latest `main` (`21933ff`) built successfully;
  live 7.12, 9.13 and 11.27 word list verified. Stopped before 1.4 pending the
  owner’s go-ahead.
- 2026-10-08 · `arena/46a0836b-bhagavad-gita` · Phase 1 step 1.2: fixed 11.27–29
  (वक्त्राणि), 17.6 (कर्शयन्तः), 1.1 (समवेताः) and 2.14 (अपायिनः) in the word
  lists. Commit 1491dae was not on GitHub or in this repo, so the fixes were
  reapplied. Full build green (150 browser checks); 390 px evidence for all four.
  PR #5 was already merged; its Pages deploy was still queued at 14:44 UTC.
  Stopped before step 1.3.
- 2026-10-08 · `arena/b1caed3e-bhagavad-gita` · Phase 1 step 1.1: corrected the
  Devanagari and IAST text of 7.12 and 9.13 in source and pāda data; rebuilt
  generated outputs. Full build green, including 150 Chromium checks; both
  verses and their word lists visually checked at 390 × 844 px.
- 2026-10-08 · `arena/07dc9c71-bhagavad-gita` · Full review (code, data, docs,
  tests, 390 px browser tour in en/ne/hi). Created HANDOFF.md and added a
  pointer at the top of PROJECT.md. No app changes.

---

## Appendix A — `audit.py`

Run it from the repo root. It uses only the Python standard library and takes
about a second. Expected output at `0f3a182` (before step 1.1):
- §1 lists 1.1, 2.6, 2.14, 11.27–29, 13.27 and 17.6. The 2.6 line (यत् वा /
  yad vā) is a harmless spelling convention.
- §2 lists 7.12, 9.13 and 13.27.
- §3 reports 674 forms (4,532 instances), 26 `te` verses and 16 `me` verses
  (see §5.2 for which `me` verses are real errors).
- §4 reports 593, 566 and 592.

```python
# audit.py — reproduces the review numbers from the SHIPPED data (data/ch*.js).
import collections, json, re, unicodedata

C = dict(zip("क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण त थ द ध न प फ ब भ म य र ल व श ष स ह ळ".split(),
             "k kh g gh ṅ c ch j jh ñ ṭ ṭh ḍ ḍh ṇ t th d dh n p ph b bh m y r l v ś ṣ s h ḷ".split()))
V = dict(zip("अ आ इ ई उ ऊ ऋ ॠ ए ऐ ओ औ".split(), "a ā i ī u ū ṛ ṝ e ai o au".split()))
M = dict(zip("ा ि ी ु ू ृ ॄ े ै ो ौ".split(), "ā i ī u ū ṛ ṝ e ai o au".split()))

def deva2iast(s):                      # strict: no diacritic flattening
    out, i = [], 0
    while i < len(s):
        c, n = s[i], s[i + 1] if i + 1 < len(s) else ""
        if c in C:
            out.append(C[c])
            if n == "्": i += 2; continue
            if n in M: out.append(M[n]); i += 2; continue
            out.append("a")
        elif c in V: out.append(V[c])
        else: out.append({"ं": "ṃ", "ः": "ḥ", "ऽ": "’"}.get(c, c))
        i += 1
    return "".join(out)

def key(s):                            # fold only harmless spelling conventions
    s = re.sub(r"[\s।॥|'’-]", "", s).replace("ṁ", "ṃ").replace("ṃn", "nn")
    s = re.sub(r"[ṅñṇnm](?=[kgcjṭḍtdpbyrlvśṣsh])", "ṃ", s)   # संघ = saṅgha
    return re.sub(r"[ṃm]$", "ṃ", s)

flat = lambda s: unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()

def load(n):
    s = open(f"data/ch{n}.js", encoding="utf-8").read()
    return json.loads(s[s.index("=") + 1:].strip().rstrip(";"))

verses = [(v, p) for n in range(1, 19) for t in load(n)["themes"]
          for p in t["parts"] for v in p["sutras"]]
pada_words = [(v["n"], w) for v, _ in verses for f in v["flow"] if f["k"] == "p"
              for w in f.get("words", [])]
print(f"verses {len(verses)} · verse-word instances {len(pada_words)}")

print("\n1) word list: Devanagari disagrees with its own IAST")
for vn, w in pada_words:
    a, b = key(deva2iast(w[0])), key(w[1])
    ends = a[-1:] in "ḥrs" and b[-1:] in "ḥrs"           # kratuḥ / kratur = sandhi, fine
    if a != b and not (ends and a[:-1] == b[:-1]):
        print("  ", vn, w[0], w[1])

print("\n2) verse line disagrees with its own word split (hidden by diacritic flattening)")
for v, _ in verses:
    for f in v["flow"]:
        if f["k"] != "p": continue
        line = key(f["t"])
        for w in f.get("words", []):
            core = key(w[1])[1:-2]                 # skip sandhi zones at both ends
            if len(core) >= 4 and core not in line and flat(core) in flat(line):
                print("  ", v["n"], "line:", f["t"], "| split word:", w[1])

print("\n3) Nepali/Hindi meanings that cannot follow context")
by = collections.defaultdict(list)
for vn, w in pada_words: by[w[1]].append((vn, w))
amb = {k: x for k, x in by.items() if len({w[2] for _, w in x}) > 1}
print(f"   {len(amb)} IAST forms have >1 English sense ({sum(map(len, amb.values()))} instances)")
for form, en, bad in (("te", "they", "तिम्रो"), ("me", "to me", "मेरो")):
    hits = sorted({vn for vn, w in by[form] if w[2].startswith(en) and w[3] == bad},
                  key=lambda s: tuple(map(int, s.split("."))))
    print(f"   {form} = '{en}…' but NE = {bad}: {len(hits)} verses: {', '.join(hits)}")

print("\n4) verse 'description' identical to the literal translation")
for L in ("en", "ne", "hi"):
    same = sum(1 for v, p in verses if p["descs"][L].strip() == v["lits"][L].strip())
    print(f"   {L}: {same}/700")
```
