# HANDOFF.md — start here

**New AI session (Arena or any other): read this file first.** It is the short,
*current* status: where the work stands, what was found, what to do next.
`PROJECT.md` is the long history — read its **§8 “Working with the owner”**
before you talk to the owner.

| | |
|---|---|
| Last updated | 2026-10-08 (Asia/Kathmandu) |
| Updated by | Arena session on branch `arena/07dc9c71-bhagavad-gita` |
| Base commit | `a353afa` on `main` |
| Owner | Dhruba Chapain, Pokhara |
| Live site | https://chapain.github.io/Bhagavad-Gita/ |

> **Rule for every session:** before you stop, update §1, tick boxes in §6 and
> add one line to §8. Keep this file short; long history belongs in PROJECT.md.

---

## 1. Where we are

- **2026-10-08 — full review done** of code, data, docs and tests, plus a live
  browser tour at phone width (390 px) in English, Nepali and Hindi, light and
  dark. The findings are in §5.
- **No app code or data has been changed yet.** This session only added this
  file and a one-line pointer to it at the top of `PROJECT.md`.
- **Waiting on the owner:** which phase to start (§7). Recommended: **Phase 1**
  (correctness). It is small and safe, and every fix can be proven.
- At `a353afa` the build and every test suite pass, including 150 browser checks.

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

The browser step (150 checks) runs only when `playwright` is importable.
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
| 13.27 | IAST avināśyantam | avinaśyantam; the Devanagari अविनश्यन्तम् is right | `padachheda_ch13.py`, **and** rename the key at `gloss_ne.py:489` and `gloss_hi.py:489` |
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
- **Paraphrases that lean away from Śaṅkara:**
  - 18.66 “Give up all other paths” (`gita_data18.py:254`). Śaṅkara reads it as
    all dharma *and* adharma, i.e. all action.
  - 15.7 “An eternal spark of myself” (`gita_data15.py:52`). Śaṅkara insists on
    *aṃśa iva*, “as if a part”. That file's header claims alignment with the
    Śaṅkara-bhāṣya.
  - The 6.47 title “Most yoked” is a calque.
- **2.47 Hindi paraphrase:** “कुछ न करने की आलस्य” → “के आलस्य”, since आलस्य is
  masculine (`translations_hi.py:194`).
- **Duplicate descriptions:** 593 of 700 English verse descriptions are
  identical to the literal translation (Nepali 566, Hindi 592), so the Study
  guide repeats itself.
- **No Śaṅkara explanation anywhere.** Suggestion: short notes on about 25 pivot
  verses, drawn from A. Mahadeva Sastry's 1897 English translation of the
  bhāṣya (public domain).

### 5.4 Search bug (`build_gita.py:1890`)

`normTxt()` strips U+0300–036F but never calls `.normalize('NFD')`, so
precomposed ā/ṇ/ṣ are never stripped. As a result, “krishna”, “karmanye
vadhikaraste”, “dharmakshetre”, “yada yada hi dharmasya” and “sarvadharman
parityajya” all return **0 hits**.

- Fix: apply NFD first, then fold common spellings (sh ↔ ś/ṣ, ri ↔ ṛ, ch ↔ c,
  aa/ee/oo ↔ ā/ī/ū) and compare a spaceless key.
- Also: the result count says “1 results” because `doSearch` ignores
  `resultCountLabel()`, and results are not ranked.

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
  - `README.md` around line 141 documents `edit.py` and `editor.html`, which
    do not exist.
- **Wrong counts:** `LICENSE.md:25–26` says 9,480 word glosses, 182 themes and
  558 parts. The real figures are 9,484 (9,366 verse words + 118 speaker
  words), 169 and 700. README and PROJECT already say 169.
- **Data:**
  - One verse's content is spread over about ten source files.
  - `data/ch*.js` is 5.3 MB raw (663 KB gzip), and all of it is fetched
    shortly after first paint.
  - 43 % is redundant (`padas` duplicates `flow`, `lines` repeats `d`/`t`,
    `meter` repeats `mt`, and descriptions duplicate the literals). Without it
    the data is 3.0 MB.

## 6. Plan — status board (tick as you go)

**Phase 1 — Correctness (1–2 days)** · not started
- [ ] 1.1 Fix the text errors in §5.1, including the 13.27 gloss-key rename.
- [ ] 1.2 Add a strict validator that fails the build. Check each word's
      Devanagari against its own IAST, and each pāda line against its word
      split, without flattening diacritics. Appendix A §1–2 is the starting point.
- [ ] 1.3 Search: NFD plus spelling folds; fix “1 results”.
- [ ] 1.4 Replace “तीन निष्ठा / निष्ठाएँ” (wording from the owner).
- [ ] 1.5 Fix the 18.66 and 15.7 paraphrases and the 2.47 Hindi.
- [ ] 1.6 Fix the `LICENSE.md` counts; remove the README editor section (or restore the editor).

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

## 7. Decisions waiting on the owner

1. Which phase to start (recommended: Phase 1).
2. What replaces “तीन निष्ठा” (e.g. “तीन षट्क”, “तीन खण्ड”)?
3. OK to add Śaṅkara notes (source: Mahadeva Sastry, 1897)?
4. Where audio would come from (licence, who records it).
5. OK to merge “Verses with translation” and “Study guide” into one view?
6. OK to delete the dead files in §5.7?
7. `PROJECT.md` §8 asks every session to deliver the full repo zip. With GitHub
   as the checkpoint, is that still wanted?

## 8. Session log (newest first, one line each)

- 2026-10-08 · `arena/07dc9c71-bhagavad-gita` · Full review (code, data, docs,
  tests, 390 px browser tour in en/ne/hi). Created HANDOFF.md and added a
  pointer at the top of PROJECT.md. No app changes.

---

## Appendix A — `audit.py`

Run it from the repo root. It uses only the Python standard library and takes
about a second. Expected output at `a353afa`:
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
