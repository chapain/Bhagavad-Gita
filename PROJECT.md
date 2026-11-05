# PROJECT.md — detailed decisions and history

> **Start with [`AGENTS.md`](AGENTS.md), not this file.** It is the concise
> current operating guide. Search this document for the feature, verse or
> decision involved when you need rationale and historical evidence.

`README.md` explains how to use the project. This file explains why the app is
the way it is and records settled decisions and mistakes that code alone cannot
show. It is intentionally comprehensive and should not be read front-to-back at
the start of every session.

---

## 0. Handoff snapshot (keep current; last touched 2026-11-04)

For a brand-new session: read §1–§10, then this box, then build.

### 2026-11-04 (sixteenth batch) — the whole book, read verse by verse

* **The semantic audit is finished: 700 of 700 verses.** Every verse of all
  eighteen chapters was read in the Devanagari, the IAST, the literal
  (en/ne/hi), the paraphrase (en/ne/hi), the title (en/ne/hi) and every word
  row with its three glosses. Chapters 1–12 were read first; 13–18 followed in
  the same pass, with the same rules, the same reading order and the same
  ledger format, so the two halves are comparable line for line. The ledger is
  `docs/semantic-audit.md`; `source/ch<N>.json` stayed canonical throughout.
* **Nine findings, seven verses, sixteen strings.** 1.04's Hindi row said
  "from Bhīma" for "equal to Bhīma" (F1); 1.13's English instrument rows
  disagreed with its own literal and read "kettledrums" twice (F2, F3);
  1.24's three paraphrases named a different addressee from the literal they
  paraphrased and said the chariot was *driven* where the verse says it was
  *placed* (F5); 1.46's first privative `अ` row was glossed "not" where the
  shape is the same privative the second one glossed "without" (F6); 2.10's
  Nepali literal and its three paraphrases named "O Dhṛtarāṣṭra" and dropped
  the "as if" the verse carries for `prahasann iva` (F7); 5.12's Nepali
  literal and its own word row ran two words together — "योगमा नस्थित" (F8);
  3.22's Nepali word row ran the negator into its word — "नप्राप्त", where the
  verse's own literal reads "न प्राप्त" (F9). Every other verse passed on
  first reading, in all three languages, literals and paraphrases included.
* **The findings cluster in four small places, and that is the useful
  result.** The vocative `bhārata` and the privative `a-` are two of them —
  each has a single canonical form and a single obvious misreading — and the
  instrument list of 1.13 and the one Hindi preposition of 1.04 are the other
  two. A word-row gloss that drifts away from its own verse's literal is the
  defect; the literal itself was never changed to suit a gloss. The two
  run-together negators (F8, F9) are typographic rather than semantic, and
  both were found by the class checks rather than by the reading.
* **The class checks now cover the whole book, not the first chapter.** Two
  different Sanskrit words may not carry one English gloss inside a verse —
  88 pairs survive, and each was read and accepted: the same lemma in another
  surface form (इदम् / इमम्), a synonym pair (एव / हि = "indeed"), or the
  house convention that a separate `न` row carries the negation (1.31, 15.10).
  All 88 are listed in the test, so a new pair is a finding and a fixed pair
  must be taken out. No row anywhere glosses a comparison with a preposition
  of departure (`से`); all 19 `सम`-family rows read "समान" in Nepali and in
  Hindi; no verse is missing a literal or a paraphrase in any language; no
  gloss is empty; no Latin survives in the Nepali or the Hindi; and no verse's
  literal duplicates its own paraphrase.
* **The pins grew with the reading.** `tests/test_semantic_audit.py` is now
  ten tests over all 700 verses: the reviewed rows *and* their literal and
  paraphrase context for all seven corrected verses, the duplicate-gloss rule
  with its reviewed-pair list, the instrument-row rule, the book-wide
  departure-preposition guard, the `समः` style, the book-wide guard against a
  Nepali negator run into its word, the ledger's own coverage of all eighteen
  chapters and 700 verses, and the three-language completeness check. A
  negative control confirms the duplicate-gloss rule rejects an unreviewed
  pair.
* **Counts:** 90 Python (4 more than 86), 937 assertions, 300 browser checks,
  230 UI strings, 13 search regressions. The browser suite still cannot run
  here — Playwright will not install in this sandbox — so that proof is CI's
  and the owner's, not ours. Two consecutive full builds are byte-identical
  across all 164 tracked files.

### 2026-11-04 (fifteenth batch) — the first chapter, read verse by verse

* **A semantic audit has started, and it is a ledger, not a pass.** Every verse
  of 1.01–1.20 was read in the Devanagari, the IAST, the literal (en/ne/hi),
  the paraphrase (en/ne/hi), the title (en/ne/hi) and every word row with its
  three glosses, against the Sanskrit and the edition's own prior verdicts.
  `docs/semantic-audit.md` records each verdict, the evidence and the decision
  before anything is edited — 20 verses, 18 clean on first reading, two
  corrected.
* **1.04 — a Hindi row said "from Bhīma" where the verse says "equal to
  Bhīma".** `भीम से` is the only row in the book whose English gloss starts
  with "to" while its Hindi uses `से`; the Nepali `भीमसँग` and the English
  "to Bhīma" were both right. The row is now `भीम के समान`. Sivananda
  ("equal in battle to Bhima and Arjuna"), Ramsukhdas ("भीम और अर्जुनके समान")
  and this edition's own Hindi literal all read a comparison, not a departure.
* **1.13 — the verse the earlier boundary pass had left open, now closed.**
  `docs/padachheda-verse-review.md` recorded "**but paṇava's ne/hi glosses are
  a collateral mismatch** … Do not label this verse's glosses fully verified",
  and `docs/padachheda-conflict-resolution.md` decided the Nepali and Hindi
  rows (drums, not trumpets). The **English** rows were never brought in line:
  they read bherī "kettledrums", paṇava "tabors", ānaka "kettledrums" while
  the literal read "drums, kettledrums, tabors" — two rows with the same word
  and neither matching. They now follow the literal, and the Hindi horn row
  follows its own literal ("तुरहियाँ", not the bare "गोमुख").
* **Two notes were closed with no change, and that is a decision too.** 1.15's
  `भीम` row reads as the adjective "terrific" while the literal reads Bhīma
  the name: both references read it the row's way ("the doer of terrible deeds"
  · "भयानक कर्म करनेवाले"), and the earlier pass had already accepted the
  literal's idiomatic "herculean deeds". 1.20's `ध्वजः` = "bannered" is terse
  but correct ("whose ensign was a monkey"), and the edition already uses that
  adjectival shape for 1.18's `बाहुः` = "armed".
* **The rules the audit found are now mechanical.** `tests/test_semantic_audit.py`
  pins the reviewed rows with their literal context, and enforces three
  checkable rules: two *different* words may not carry one gloss (the same
  word may — बलम् twice in 1.10 is correct), the English instrument rows must
  follow the English literal, and no row anywhere may gloss a comparison with a
  preposition of departure. Reintroducing either defect fails five of the six
  tests. The earlier snapshot `tests/fixtures/reference_conflicts.json` was
  amended deliberately for 1.13 and its test's docstring records why.
* **Counts:** 86 Python (6 new), 937 assertions, 300 browser checks, 230 UI
  strings, 13 search regressions. The browser suite still cannot run here.

### 2026-11-04 (fourteenth batch) — the floating listbox is withdrawn

* **The owner reported the panel and it was right to.** His screenshot showed the
  suggestion list floating over the search results, with a stray "Back to
  Chapter 1" pill on top of it, and his judgement was blunt: *"I don't think we
  need the recent searches dropdown is necessary."* Two separate defects were
  behind it. First, the listbox was `position:absolute` with `z-index:60` inside
  the sticky search field, so by design it hovered over the results it was meant
  to help find — and it opened on the **keystroke**, 220 ms before the live
  results rendered, so both were on screen together. Second, its first five rows
  were the reader's own past queries, offered back regardless of what was being
  typed — for the query "18" it listed 11.47, 11.4, 11., 11 and 18.76.
* **The recents were junk because every keystroke of one search was a search.**
  `doSearch()` called `recentSave(q)` on each debounced live search, so looking
  for 11.47 stored four separate "recent" queries: "11", "11.", "11.4" and
  "11.47". A history that records its own prefixes is not a history; it is a
  transcript of typing.
* **So the feature is removed, not restyled.** `15-suggest.js` (105 lines) is
  deleted and its entry dropped from `APP_JS_FILES`; with it go the combobox
  ARIA on the field, the `<ul role="listbox">`, the `.search-suggest` CSS, the
  `sugRender/sugKey/sugPick/sugBlur` exports, the `search_suggest_hint` and
  `search_recent` strings (×3 → 230), and the `gitaRecent` localStorage key.
  The field is a plain `<input type="search">` again, Enter searches, and
  nothing is written down. **Raising the z-index or shrinking the panel was
  rejected**: the owner asked for the dropdown to go, and a floating panel that
  still floats is the same defect wearing a different hat.
* **Search still works, and now shows nothing but the answer.** The live
  results, the chapter and theme groups and the folded second chance (C3) are
  untouched. The chips that remain are the four real starting points — 2.47,
  4.7, 18.66 and धर्मक्षेत्रे — and they appear **only on the zero-result
  screen**, where a suggestion is genuinely useful; a screen with hits carries
  no chip row at all.
* **The locks now guard the removal**, because a lock that only exists to
  celebrate a feature is a lock that will be deleted with it. Seven document
  assertions became five that the overlay cannot come back by accident (no
  `searchSuggest`, no `sugRender`/`sugKey`, no combobox ARIA, Enter still
  searches, no `gitaRecent` in the shell); the C2 builder test in
  `tests/test_search.js` became a test that the listbox and the stored queries
  are gone; the four C2 browser checks became two (no overlay covers the live
  results while typing; the field is a plain input that stores nothing).
  **Those two browser checks have not run here** — Playwright cannot be
  installed in this sandbox — so the lock moved 302 → 300 and CI owns the proof.
* **Counts:** 937 assertions, 300 browser checks, 230 UI strings, 13 search
  regressions.

### 2026-11-04 (thirteenth batch) — the other half: all 869 descriptions read

* The title pass (eleventh and twelfth batches) covered names, not the paragraphs
  under them. Asked whether the whole editorial layer was finished, the honest
  answer was "titles yes, descriptions no", so they were read: **700 verse
  descriptions and 169 theme descriptions**, every one against its verse, its
  range and — for themes — the parts inside it. **No factual defect found**: no
  wrong speaker, no wrong count, no verse described that its neighbour states.
* Screens that ran before the reading, so the reading was aimed rather than
  hopeful: descriptions that assert a **count** (43 of them, every one correct
  when recounted against the Sanskrit), **speaker attribution** at the 60 verses
  that open a speech (0 mismatches — the description never hands a verse to the
  wrong speaker), and desc-vs-title polarity (too noisy to mean anything: a
  description is a fuller sentence than its title, which is not a contradiction).
* The descriptions are **third person** ("He asks Kṛṣṇa…") while the literals are
  second — a deliberate split, not drift, and it holds across all 700.
* One line flagged for the owner's awareness and **not changed**: 9.32's list
  ("those of sinful birth, women, traders and labourers") is exactly what the
  Sanskrit prints, and the description states it no more strongly than the
  literal. The edition carries no commentary, so the faithful rendering stands.
* **What this pass does not prove:** the ~5,200 strings exist in three languages,
  but only the **English** was read semantically; the Nepali and Hindi were
  checked structurally (present, no Latin letters, no banned readings, no stubs —
  median length 0.82 and 0.87 of English, shortest 0.48 and that one is simply
  concise). A semantic read of ne/hi is the one piece of this layer still owed.
* Counts unchanged: 68 Python, 943 assertions, 560 site-health, 10 SEO, 9,658
  study, 50 advisories / 0 blocking, shell 373,731.

### 2026-11-04 (twelfth batch) — the king who was called "O King", and five theme titles narrower than their own descriptions

* **1.02 read as a vocative when it is a nominative.** The owner heard it at once
  — "it looks like it means Duryodhana goes to his guru and calls him 'hey rājā'".
  He was right, and the diagnosis was grammatical: `ācāryam upasaṅgamya rājā
  vacanam abravīt` (`duryodhanaḥ` is the subject; `rājā` is apposition), so it is
  "the king spoke these words", not "…O King". The tell is inside the edition:
  1.16 renders nominative `rājā` as "King Yudhiṣṭhira", and the real vocative
  `rājan` is "O king" in 11.09, 18.76 and 18.77 — 1.02 was the only slip. It was
  wrong twice over: not a vocative, *and* pointing at the wrong listener (in the
  paraphrase Duryodhana appears to call Droṇa "king", when his first words come
  in 1.03 and address him as `ācārya`). Fixed in all three languages in both the
  literal and the paraphrase; the paraphrase now ends "…and spoke:", handing off
  to 1.03. See §4.11.
* **Five theme titles did not speak for their spans.** The owner asked whether
  theme titles represent the essence of *all* their verses, citing 1.10–1.11,
  where the theme title echoed the 1.11 part title. All 169 were read against
  their ranges, their parts and — the sharpest test — their own descriptions:
  * **1.10–1.11** "Guard Bhīṣma above all" named only 1.11 while its description
    began "Duryodhana compares the forces, then orders…". Now "Both armies
    weighed; Bhīṣma must be guarded". A first draft named Duryodhana and the
    auditor immediately flagged it — correctly: he is the *speaker*, not named in
    1.10–1.11 — so the name stays in the description, which already carries that
    benign advisory, rather than adding a second.
  * **8.16–8.19** "Even Brahmā's world returns in cosmic cycles" restated 8.16
    with a suffix; now "Brahmā's day and night: worlds appear and dissolve",
    which is what 8.17–8.19 actually do.
  * **17.23–17.27** reordered 17.23's own words; now "Om, Tat, Sat: the words that
    make an act sacred", covering 17.24–17.27.
  * **17.07** and **17.28**, both single-verse themes, were near-verbatim copies of
    their only part title. Now "Threefold food, sacrifice, austerity and gift" and
    "Without faith, an act counts for nothing".
  * Everything else stands, including 2.19–2.21, which is allowlisted as
    deliberately identical to its part title. Closest calls left alone, with
    reasons: 7.01–7.03 ("…one in a thousand" adds 7.03), 7.28–7.30, 2.26–2.30
    (titles genuinely extend their first verse), 6.20–6.23 and 5.06–5.10 (the
    image in the last verse names the whole run — a real heading, not a narrow one).
* **The pins that caught it, and what had to move.** The stale-literal test, the
  worksheet snapshot test and the two chapter-17 assertions all failed on the
  first build — which meant the guards were doing their jobs rather than being
  quietly satisfied. Regenerated `docs/title-review.md` from the generator (never
  hand-edited) and updated the five `STUDY_MAPS.md` lines plus the two JS pins to
  the new approved wording. Advisories returned to exactly **50 / 0 blocking**.
* **Counts:** 68 Python, 943 assertions, 560 site-health, 10 SEO, 9,658 study,
  13 search. No interface string, no shell character (373,731 of 375,000).

### 2026-11-04 (eleventh batch) — the book read against itself, and two claims counted

* **The 700 titles were read against their verses, all of them.** Every verse
  title in chapters 1–18 was compared with its Sanskrit, its literal and its
  paraphrase; the 56 titles that assert a **count** were recounted one by one,
  and every title naming a speaker was checked against who is actually speaking.
  No title misstates its verse. The auditor's 50 advisories are a **counting
  prompt, not an error list**: the 42 `name-not-in-verse` hits are speaker-named
  titles (“Duryodhana…”) and theme titles summarising the speaker's own words,
  and the 8 `number-unsupported` hits are right when counted — 1.15 three
  conches, 8.23 two times, 13.24 three paths, 14.05 three guṇas, 14.18 three
  destinies, 16.04 six marks, 18.12 three fruits, 18.29 threefold intellect and
  fortitude. **1.44 stands**: the title states what Arjuna is arguing, the
  literal keeps `iti anuśuśruma` (“thus have we heard”), and all three
  descriptions already carry the hedge. Rewriting the title would flatten a
  voice the text itself qualifies.
* **Nothing compared the printed Devanagari with its own transliteration.** This
  is the batch's one real defect, found by mutation rather than by reading:
  appending a syllable to a pāda's `d` failed **no check at all**. Every check
  read `t` — `build_gita.py` derives each pāda's stored count `n` from `t`,
  `check_site_health.py` recomputes the method page's figures from `n`, and the
  word rows are compared word by word — so the line the reader actually sees was
  the one link in that chain nobody tested. A mistyped matra, a dropped visarga
  or a vowel length written short in `d` could ship while every counter stayed
  green. `check_padas.py` now transliterates each pāda's `d` and requires it to
  equal its `t` under the same folds the word check uses: **2,800 lines, 0
  flags**. Proof of bite, three mutations: an extra syllable trips this guard
  *and* the metre count; a dropped visarga — which costs no syllable — trips only
  this one; `ś → ṣ` trips it, so vowel length and sibilants are live, not folded
  away.
* **The metre is now counted at the reader-visible end too.** The method page
  tells the reader 644 verses are anuṣṭubh at 8/8/8/8, 51 are triṣṭubh at
  11/11/11/11, and five are irregular and named one by one. Those figures were
  already pinned by site-health, but only against the stored counts `n`, which in
  turn come from `t`. `check_padas.py` now counts akṣaras from the printed `d`
  itself and pins both the totals and the **names** of the five irregular verses,
  which were previously only counted, never identified. Reproduced independently
  before being wired: 11.01 `9/8/8/8` (33), 2.29 `11/12/11/11`, 8.10
  `11/11/11/12`, 15.03 `12/11/11/11` (all 45), 2.06 `12/12/11/11` (46) — exactly
  the totals §4.3 states, so the documentation was right as written.
* **One sentence was left alone on purpose.** The method page says the titles
  “are still being re-read against their verses one by one”. That describes the
  owner's own review, not the text, and only he can retire it — an AI pass is not
  a reason to tell a reader the author has finished reading.
* **Counts unchanged:** 68 Python, 943 assertions, 560 site-health, 10 SEO,
  9,658 study, 13 search, 50 advisories / 0 blocking. No interface string, no
  generated page and no shell character moved (373,731 of 375,000).

### 2026-11-04 (tenth batch) — 18 doors into the book, and a book that says what it is

* **Chapter titles became editorial copy.** Eighteen pages shared one formula,
  `Bhagavad Gita Chapter N — {name}`, with one generic description between them;
  a crawler reads that as one weak page repeated. Each now has its own topic and
  blurb (`CHAPTER_TOPICS` in `build_gita.py`), measured at ≤57 characters for a
  title and ≤153 for a description, 18/18 unique. The choice was **topic-forward**
  because name-forward cannot fit: chapter 13's traditional name alone is 31
  characters, leaving no room for a topic *and* a verse count inside 60. The
  Sanskrit name did not leave — it is the `<h1>`, the og:title, the page body,
  and the first words of every description in Devanagari, which Nepali and Hindi
  readers both recognise. `og:title` and `twitter:title` deliberately keep the
  name form: a share card should read as a name, not a query.
* **The structured data was lying and nothing read it.** `WebApplication` carried
  an inline `Book` with no author, no translator, and `"numberOfPages": 18` — the
  chapter count wearing a page count's name. `Book` is now its own node (`#book`,
  linked by `@id`): Vyāsa by traditional attribution (stated in `creditText`),
  translator Dhruba Chapain, `sa/en/ne/hi`, `EBook`, free, copyright notice, and
  “18 chapters and 700 verses” in the **description**, because schema.org has no
  verses property and a false field is worse than a sentence. `check_site_health.py`
  had zero JSON-LD checks — a malformed block fails nothing a reader can see — so
  it gained eight (552 → 560), including “no node claims a page count”.
* **Copy verse follows the reader's language** (owner's choice): Devanagari, IAST
  only where the app shows it (English), the literal in the current language, and
  the chapter-page link — as `text/html` via `ClipboardItem` so a paste keeps its
  shape, with the old plain-text path as fallback for browsers without it. The
  paraphrase is deliberately not copied: a verse in a chat, not an essay.
* **The word peek went on the rows, not the verse line** — the brief asked for a
  long-press on a word in the live verse. That is not honestly implementable: the
  printed verse is sandhi-joined (2.47 prints `कर्मण्येवाधिकारस्ते` as one token
  while its words are `कर्मणि / एव / अधिकारः / ते`), so a touched token has no
  single word behind it, and splitting the printed line to make it tappable would
  invent a boundary the text does not print. The gesture lives on the word rows,
  which carry the true split, and reveals the two languages the reader is not
  reading. Tap, `Enter`/`Space`, right-click and `Escape` all reach it, so it is an
  accelerator rather than the only door. Each row carries its own `data-words`
  because a verse has four pāda containers plus speaker lines and a single global
  would be overwritten by whichever rendered last.
* **The shell cap is the binding constraint again.** D1 + D2 took it 365,393 →
  373,731 against a 375,000 cap: **1,269 characters**. Two rounds of trimming the
  comments I had just written bought back ~850, which is the lesson — rationale
  belongs here, in PROJECT.md, not in every page load. The next feature needs a
  real trim or a deliberate, measured cap raise; it must not slip in under a
  comment.
* **Counts:** 937 assertions, 300 browser checks, 230 UI strings, 560 site-health,
  10 SEO checks, 86 Python, 13 search regressions. D1's clipboard behaviour and
  D2's touch gesture are **not proven here** — both need a real browser, so CI and
  the owner's phone own that.

### 2026-11-04 (ninth batch) — the worksheet becomes a column of ticks

* The seventh batch produced the right triage in the wrong shape for the job it
  was written for. It printed 50 advisories as 490 lines of prose, and the task
  attached to it is a **quarterly read-through of all 700 titles**. Nobody reads
  700 titles from a list of 50 problems: the problems are where a reader should
  *start*, not what he should read.
* `audit_titles.py --markdown` now emits both, in order:
  `| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |`, one
  row per title, grouped chapter by chapter with the chapter name and its verse
  range. A ⚑ in the first column marks the 10 verses that do carry an advisory,
  and each flagged verse is named with its advisory kind under its chapter, so a
  row is self-explanatory without scrolling to a second section.
* **All 700 rows, not only the flagged ones.** A title with no mechanical doubt
  still gets a tick, because the read-through exists to catch what no check can:
  a correct but dull title, a summary that misses the verse's turn. The 40
  theme-level advisories (`1.t4` and friends) cover runs of verses and so have no
  single row; they are a separate small table with their own ticks.
* **Prose is now the minority of the file.** The 10 verse-level advisories keep
  their “*the verse says:*” evidence in a closing section, grouped by triage
  label; the 40 theme items are table rows. 490 → 1,025 lines, but 700 of those
  lines are the tickable rows — the prose roughly halved.
* **Read-only, and now provably so.** `tests/test_title_worksheet.py` (8 checks)
  re-reads the snapshot against `data/ch*.json`: 700 unique rows in canonical
  order, every title byte-identical, every literal byte-identical (or a genuine
  prefix when truncated), ⚑ exactly equal to the audit's verse-level refs, 50
  advisories, 0 blocking, 18 chapter headings, three tick boxes on every row, and
  the snapshot equal to the generator's own output. A future edit to a title
  therefore cannot leave a worksheet claiming to show it. Nothing writes to
  `source/ch*.json`; the decisions remain the owner's.
* Python tests 60 → 68; every other count unchanged (937 document, 552 health,
  9,658 study, 17 migration, 13 search, 700 cards). `48-reader-view.js` is
  corrected from 188 to **184** lines in `HANDOFF.md` (three places), the
  eighth-batch entry below, and the dated comment in `check_site_health.py` —
  prose only, no build effect.

### 2026-11-04 (eighth batch) — the reader keeps its sheet and gives up its paint

* `50-reader.js` was 604 lines against a 700-line module guard. Nothing was broken,
  but every future reader change — a note affordance, a share option, one more
  control in the ⋯ menu — would have paid that debt first, and the earlier fix for
  the same problem (2026-11-04, fifth batch) had already shown the seam: the guard
  binds long before the character cap ever does.
* Split along the seam that was actually there: **presentation** vs **the sheet**.
  `48-reader-view.js` (184 lines) now holds the pāda block, `fitWholeVerse`'s
  measure-and-shrink loop, `setVerseView` and its expansion toggle, reader text
  size, the ⋯ menu and the word-meaning switches — plus `verseViewState`, because
  every one of those functions reads it. `50-reader.js` (426) keeps opening and
  closing the sheet, `fillModal` and its note field, the history plumbing, sharing
  and `navSutra`.
* **The note field did not move, and that is the point.** It is not a view: it is
  written by `fillModal`, grown to its saved text, and read back on save, so moving
  it would have meant an accessor and a new owner for state that is already one
  coherent job. Splitting a file is not worth breaking a boundary.
* No function was rewritten, no line reordered: the moved code is byte-identical
  text in a new file that loads earlier, so the browser still receives one inline
  script and the service worker still precaches one shell. The 937 document
  assertions are static analysis, so the moved functions were also driven in a
  real DOM under jsdom (installed outside the repo, evidence for the session and
  never a dependency): 42 checks over both card shapes and their roles, the
  quarter toggles and the master meaning switch, the text-size scale and its
  readout, the ⋯ menu, the share panel and next-verse navigation. That proves
  wiring, not layout or touch — the 302 browser checks still own those.
  Shell 365,000 → 365,393 characters; the delta is the new header comment. Cap
  unchanged at 375,000.
* The same batch put `PROJECT.md` back under its own ceiling: it had reached
  190.6 KB, so the 15 October batches moved verbatim to
  `docs/archive/PROJECT-2026-10.md`, leaving this §0 with the current month and
  §1–§10 untouched. All 24 batches were verified present exactly once.

### 2026-11-04 (seventh batch) — the 50 advisories, triaged instead of repeated

* `build.py` has printed “advisory: 50” for weeks. A number on a screen is not a task,
  so `audit_titles.py --markdown` now triages them mechanically and prints a worksheet:
  39 are **first person** (the verse *is* the named person speaking — Kṛṣṇa for most of
  the book, Duryodhana in 1.1–1.11 — so a summary naming him is right even though the
  IAST cannot contain the name), 1 addresses its listener by vocative, 8 are
  **enumeration titles** that name how many things a verse lists without the verse ever
  saying the number (“The three qualities” for sattva/rajas/tamas), and 2 are theme
  summaries that needed a scene read. The triage is evidence, never a verdict: each item
  prints the verse's own literal beside the title.
* I read the three that the mechanics could not settle (1.t4 across 1.11–1.13, 18.t4
  across 18.18–18.22, and the 13.24-class number titles) against their verses, and all
  are correct as written — the description that “Bhīṣma's roar heartens Duryodhana” is
  right, because “him” carries across the theme boundary from 1.11.
* **Nothing in `source/ch*.json` changed.** These are editorial decisions and the owner's
  to make; the worksheet (`docs/title-review.md`) exists so those decisions start from
  three items instead of fifty.

### 2026-11-04 (sixth batch) — the provenance page, and the numbers on it that cannot drift

* **REVIEW §20 item 5, shipped as a static page rather than an app view.** `method/`
  (source: `source/method.html`) is generated with the rest of the site: no JavaScript,
  self-contained CSS, three language sections in one page (English · नेपाली · हिन्दी) with
  anchor links. Three reasons it is static. A provenance page has to read for a crawler
  and for a reader whose JavaScript failed. It costs the shell nothing while the shell
  has 10 KB of cap headroom. And a directory URL ends in `/` like every sitemap entry,
  which `check_seo.py` requires — a `method.html` URL would get a 301 from GitHub Pages
  on every crawl.
* **Every sentence that makes a claim is traceable.** The recension paragraph comes from
  README (`Śaṅkara-bhāṣya`, the 1.8 example) plus this file's 13.34 finding; the
  translation paragraph from §4 and HANDOFF 7.2/7.3 (18.66 and 15.7 settled on the
  Śaṅkara reading; commentary deliberately absent); the splitting paragraph from 4.2, 4.3
  and 4.4 (4.33's `…yajñāj` against its word `yajñāt`; 8.20's avagraha at the head of the
  next pāda); provenance and licence from `LICENSE.md`; the privacy paragraph from the
  code (no account, no analytics, no server, no outbound fetch — grep, not assumption).
  Nothing on the page is a claim the repository cannot back.
* **The page's numbers are recomputed from the data on every build.** 700 verses, 2,800
  pādas, 9,484 word meanings, 644 anuṣṭubh / 51 triṣṭubh / 5 irregular, chapter 13's 34:
  `check_site_health.py` recalculates each from `source/ch*.json` and fails if the page
  disagrees — in English digits and in Devanagari numerals, in all three sections. The
  three quotations are checked against the verse they cite (1.8 must still read
  `saumadattis tathaiva ca`; 4.33's first pāda must still end `yajñāj` while its word row
  says `yajñāt`; 8.20 must still split its avagraha across the pāda break). A provenance
  page that drifts is worse than none, so this one cannot drift: 46 new site-health
  checks, 506 → 552.
* **Reaching it exposed a real worker bug.** `method/` is linked from the app footer
  (`method_link`, ×3 → 232 strings, labelled by `applyStatic()` so the link follows the
  reader's language), from all 18 chapter footers, from `sitemap.xml`, and from the
  worker's precache. That last one did not work: PR #68's navigation branch consulted the
  cache only for the root and for `/chapter/N/`, so a *precached* page still fell through
  to the honest 504. The branch now serves an exact-URL cache hit for any in-scope
  navigation and stores what the reader actually visited under its own address. It never
  substitutes one page for another, and an unvisited chapter still returns the 504.
  `tests/test_offline_navigation.js` now runs `install` against a fake cache and proves
  the four cases: precached page opens offline, visited page opens offline, unvisited
  chapter 504s, unknown page 504s.
* **What is not proven here.** The 302 browser checks cannot run in this sandbox, and two
  of them are PR #68's offline navigations, which now sit beside changed worker code. The
  simulated worker test is the local evidence; CI is the real proof. Also unverified
  locally: how the three language sections read on a 390 px phone, which is a design
  question for the owner's eye, not a check.
* **Counts:** 937 assertions, 302 browser checks, 232 UI strings, 552 site-health, 60
  Python, 13 search regressions. Shell 364,612 → 365,000 chars / 387,782 bytes /
  105,531 gzip; the method page itself is 26 KB (precached, outside the shell cap).

### 2026-11-04 (fifth batch) — the room the next feature needs, cut out of the source

* **The cap was never the binding constraint — the module guard was.** The shell
  sits at 363,141 characters under a 375,000 cap (11,859 of room, 11.6KB), but
  `tests/test_source_modules.py` refuses any source module over 700 lines, and
  `10-library.js` stood at 677 with `20-learn.js` at 686. A 5KB feature —
  roughly 100 lines at these modules' density — would have failed the guard days
  before it troubled the cap. Raising the cap would have fixed the wrong number;
  it stays at 375,000, unchanged.
* **Two splits, both measured first.** The search screen (`onSearchInput` through
  `clearSearch`, 204 lines) moved whole into a new `12-search.js`; free practice
  (`FP`, `lrFree`, `lrFreeCh`, `lrFreePick`, `lrFreePaint`, `lrFreeTap`, 97 lines)
  moved whole into a new `27-learn-free.js`. That is 10-library 677 → 477 lines
  (223 of room) and 20-learn 686 → 589 (111 of room). The next tightest module is
  now `50-reader.js` at 604 — noted here so the next session does not rediscover
  it: its candidate is the sheet's note field, and it is *not* a free move,
  because the modal state lives beside it.
* **What did not move, and why that is the point.** No verse data, no CSS, no
  view, no route, no string. The build still emits one inline script and one
  style, fetched once and precached by the same worker; boot order in
  `APP_JS_FILES` changed only by insertion (12 after 10, 27 after 25), so nothing
  that ran before runs later. The proof is textual: the built script differs from
  the previous one by the two module headers and two accessors, and by nothing
  else — every moved line is byte-identical in its new address.
* **The ownership guard fired once and was right.** The search screen walked
  `VERSES` by name, which is exactly what the single-owner rule forbids. Rather
  than exempt the new file, `10-library.js` gained `versesMatching(match)`: the
  index owner hands the caller each verse's location, searchable text and folded
  text, and the query rules stay in the search module. `srchAnnounced()` does the
  same for the other direction — `announceView()` used to read `SRCH_HITS` and
  `SRCH_NOTE` directly; now the results' owner answers the question. Both follow
  the rule already in AGENTS.md: add the accessor in the owning module.
* **What was actually run.** Full `build.py`: 60 Python tests, 934 document
  assertions, 700 card-nav, 17 progress, 13 search regressions, 2,100 paraphrase
  pairs, backup and offline routing — all green. Beyond the build, the shipped
  shell was executed in a real DOM (`jsdom`, installed outside the repository, so
  it is evidence rather than a dependency): 21 checks drove the *moved* code —
  numbered search `2.47`, free text, a gloss-only hit, the C3 relaxed-query note
  and its announcement through `srchAnnounced()`, `clearSearch`, and free
  practice from paint to four chips to a completed verse to the next deal, and
  the suggestion combobox reading `recentLoad()` from its new home. This
  says nothing about layout, touch or the phone tab bar; those still need the
  browser suite, which cannot run in this sandbox, so 302 browser checks remain
  CI's to prove.
* **Counts:** 934 assertions, 302 browser checks, 231 UI strings unchanged; the
  shell grew 1,471 characters to 364,612 chars / 387,326 bytes / 105,412 gzip,
  all of it comments and accessors, and 13 source modules are now listed.

### 2026-11-04 — offline chapter pages keep their identity

* The service worker promised to cache visited chapter pages but navigations were
  never stored: any offline navigation got the app shell, even at a chapter URL.
  It now caches successful same-origin chapter navigations under their own request,
  keeps the root shell separate, and returns an honest 504 offline page for an
  unvisited chapter or other uncached navigation. Failed HTTP responses cannot
  overwrite a good cache; a cache write failure does not hide a live response.
* `tests/test_offline_navigation.js` executes the generated worker with simulated
  network and cache; two browser checks cover a real visited and unvisited chapter
  offline. These browser checks are not locally verified without Playwright.
  Counts: 934 assertions, 302 browser checks, 231 UI strings; the shell is
  unchanged at 363,141 chars / 385,851 bytes / 105,035 gzip.

### 2026-11-04 (second batch) — the furniture behind the sheet, and the share art

* **A tab list with no tabs, twice.** `modeSwitch()` wrapped the read/learn
  buttons in `role="tablist"` while they carried `aria-pressed` (a toggle, not a
  tab), and the phone `.tabbar` declared `role="tablist"` with `role="tab"`
  buttons that change the *page* — there are no tabpanels, and Random is not even
  a destination. Both are now honest: the mode switch is `role="group"` with two
  pressed buttons; the bar is a `nav` whose current destination carries
  `aria-current="page"` (set by `syncTabs()`, styled by
  `.tab-btn[aria-current="page"]`). A browser check asserts no tab list exists
  without tabs.
* **The bottom bar stayed focusable behind the sheet.** `setAppInert()` covered
  `header`, `.toolbar`, `.wrap`, `footer` — everything except `nav.tabbar`, which
  the CSS merely dimmed (`pointer-events:none; opacity:.4`) and so kept in the Tab
  order and in the screen-reader tree. Added; a browser check asserts all five
  regions are inert while the sheet is open and released after it closes.
* **`img/share-art.jpg` was committed and referenced by nothing.** 44,653 bytes,
  960×504, repainted by `build.py` whenever Pillow exists, `og:image` pointing at
  `icons/og-card.png`. It now earns its place as the preview inside the share
  panel, *after* the copy actions, with `width`/`height` (no layout shift),
  `loading="lazy"`, `alt=""` (the panel text carries the meaning) and
  `onerror="this.remove()"` so an offline miss leaves no broken frame. A browser
  check reads `naturalWidth ≥ 900`, so the test proves the picture actually
  loads — the first time this asset has been exercised at all.
* **“Review complete for today” was false.** The welcome badge counts due verses
  across all 18 chapters (`srsDueAll`), but a review session serves at most seven
  verses of *one* chapter (`lrReview` → `ids.slice(0,7)`), then said the day was
  done. Now `srsFinishReview()` re-counts: if anything is still due it says how
  many and offers “Continue review” (`srs_review_more`, new key ×3 → 225 UI
  strings), and only claims completion when nothing is due anywhere. One shared
  `srsDueLabel()` feeds both the badge and the finish screen so the two can never
  disagree, and `srsDueAll()` now starts with the **most overdue** chapter
  (`firstDue`) rather than the lowest chapter number.
* **`prove_data_only.py` is reachable from the build.** It ran in CI since item
  1, but not from `build.py`; `python3 build.py --prove` now runs it after the
  checks (it edits source files, rebuilds and restores them, so it stays opt-in
  locally and unconditional in CI).
* **Two repository guards fired, and both were right.** `tests/test_source_modules.py`
  refuses any module over 700 lines, and C2 had pushed `10-library.js` to 772;
  it is now 674, with the suggestion code in its own `15-suggest.js` (103). The
  same file also enforces single ownership of mutable state, which rejected the
  new module reading `VERSES` by name — correctly, by the same rule that keeps
  `LV`, `PL` and `LQ` from leaking between modules. `10-library.js` now offers
  `versesForChapter(ci)` and the suggestions go through it.
* **Counts:** 934 assertions, 300 browser checks, 231 UI strings, shell 363,141
  chars / 385,851 bytes / 105,035 gzip. Both totals keep their drift locks, so a
  stale number fails the run instead of quietly blessing three documents.

### 2026-11-04 — suggestions that are actually a combobox

* **C2 — search now helps before you commit to a guess.** Typing two characters
  opens a listbox of at most ten rows, built from three sources in the order a
  reader wants them: the last five searches that are not the current query, up
  to three chapter titles matched by name (folded, so `sankh` finds Sāṅkhya
  Yoga), and up to two verse numbers their digits could still become (`2.4` →
  2.4, 2.40 … 2.47; Devanagari digits work through `digitNorm`). Rows carry
  their own kind label, so the list stays **flat** — one index for ↑/↓ instead
  of nested groups — and each row says whether it is a Recent, a Chapter or a
  Verse.
* **It is a real combobox, not a div that looks like one.** The previous batch
  refused a fake tablist; the same rule applies here. The field is
  `role="combobox"` with `aria-autocomplete="list"`, `aria-controls` naming the
  `<ul role="listbox">`, and `aria-expanded` kept in step by the code that
  shows and hides it. The active row is announced through
  `aria-activedescendant` + `aria-selected`, never by a CSS class alone. One
  new string (`search_suggest_hint`, ×3 → 231 UI strings) describes the keys;
  the row kinds reuse `search_recent`, `chapters` and `verses` rather than
  adding three more. ne/hi say एन्टर/एस्केप as words, not Latin key names — the
  Latin-residue check caught my first attempt using “Enter” and “Escape”.
* **Keys cannot do two things at once.** `sugKey()` returns true when it
  consumed the key, and the markup is `if(App.library.sugKey(event))return;`
  before the Enter-to-search call, so Enter on a highlighted row opens that row
  and Enter on a plain field still searches. Escape closes the list first and
  leaves the view alone. Choosing a chapter row navigates to the chapter and
  clears the field; choosing a recent or a verse row runs that search.
* **Coverage.** `tests/test_search.js` executes the emitted builders with no
  DOM: one character and whitespace offer nothing, a word the book lacks offers
  nothing, `2.4` offers at most two numbers that all start with the digits
  typed, `2.47` offers exactly itself, १७-digit input suggests the same verses,
  chapter 19 does not exist, recents cap at five, the list never exceeds ten,
  and the query is never offered back as a recent. Four browser checks were
  added for what only a real browser can prove — that the list opens with
  rows, hangs under the field inside a 390px viewport, moves exactly one
  selection with the arrows, and clears its ARIA state on Escape. **Those four
  have not run here**: Playwright cannot be installed in this sandbox, so the
  lock moved 296 → 300 and CI is the real proof.
* **The cap moved once more, and the comment says why.** C2 costs 7,086
  characters (355,407 → 362,493 before the module split below took it to
  363,141), leaving 7.5KB of the 370,000 cap — under the
  5KB floor the previous batch set itself. The code was trimmed first (a
  duplicated `.sr-only` rule, a group wrapper the flat listbox did not need),
  then the cap went 370,000 → 375,000 for a real 12.5KB reserve. No module
  split: the lazy-load candidates need the browser suite re-locked, and that
  suite cannot run here.
* **Counts:** 934 assertions, 300 browser checks, 231 UI strings, shell 363,141
  chars / 385,851 bytes / 105,035 gzip. Search regressions 12 → 13.

### 2026-11-04 — the backup nobody found; the vowel that found nothing

Two gaps, both measured before they were fixed, and one cap decision taken on
numbers rather than on the pressure of a full file.

* **A5 — export/import existed and nobody knew.** The backup controls live on
  the `#data` screen, reachable from the welcome footer; a reader who learned a
  chapter and never opened that screen had no hint that their progress was one
  cleared cache away from gone. The Learn path now carries one muted line under
  the progress meter — `backup_never` / `backup_today` / `backup_yesterday` /
  `backup_n_days` (5 new keys ×3, 230 UI strings) — reading the same
  `gitaBackupAt` stamp the badge uses, compared as **calendar days**
  (`Date.UTC(y,m,d)`) so a DST shift cannot say "0 days ago" the morning after a
  backup. It is a real button that opens the data screen, and it renders nothing
  at all for a first visitor with nothing to lose: a warning about protecting
  data that does not exist is noise. `tests/test_data_backup.js` runs the
  emitted helper against a fixed clock with an injected `Date`, covering today,
  yesterday, three days, the empty-first-visit case, saved-but-never-backed-up,
  and a corrupted future stamp (clamped to today, never "-2 days ago").
* **C3 — a marked query that missed said nothing at all.** Search deliberately
  keeps a query carrying diacritics exact, so a/ā, t/ṭ and ś/ṣ stay
  distinguishable — correct, but it means one wrong vowel is a blank screen. The
  measured cases: `sankhyā` → 0 hits (plain `sankhya` → 3), `karmanyā` → 0 (7),
  `arjunā` → 0 (36), `sanjayā` → 0 (14). The brief proposed a "did you mean"
  line; that is the worse shape here, because the plain reading is not a
  suggestion to confirm, it is the answer the reader is looking for. So
  `searchFoldAlternative()` offers a folded second chance **only** when the
  exact pass returns nothing, and the app renders those real results under their
  real count, with one line saying the exact form was not found
  (`search_meant`, ×3). A query already plain returns `null`, so the escape
  hatch can never fire twice or loop, and `SRCH_NOTE` is module-scoped and reset
  per search so a stale note can never describe the current results.
  `tests/test_search.js` proves it is a genuine rescue — zero exact hits and
  hits once folded, for all three words — rather than asserting a string exists.
* **C5 was already shipped** and was dropped from the batch after checking:
  `10-library.js` already renders `no_results` *plus* a `search_try` hint (2.47,
  dharmakṣetra, a phrase from the translation) and suggestion chips, in all
  three languages. The backlog entry describing it as "prints only
  `no_results`" was stale; nothing was rebuilt.
* **The shell cap moved on the arithmetic, and the reason is written at the
  check.** The batch adds 4,799 characters (350,608 → 355,407), taking the shell
  to 98.7% of the old 360,000 cap. The measured alternative was lazy-loading
  `source/js/45-data.js` — the whole module is 13,228 characters, so it buys
  less than the bump while changing boot order, the SW precache and the browser
  suite that cannot run in this sandbox. Cap 360,000 → 370,000, leaving ~14.6KB;
  `check_site_health.py` records the measurement and names the two modules to
  split (`20-learn.js` 34,114 · `10-library.js` 33,548) if headroom falls under
  5KB again.
* **Counts:** 925 assertions, 296 browser checks, 230 UI strings, shell 355,407
  chars / 377,877 bytes / 102,584 gzip. Search regressions 11 → 12.

### 2026-11-04 — search reaches ideas; a note belongs to its verse

* **The search index remembered the words and forgot the ideas.** It held the
  Devanagari line, its IAST, the paraphrase and (since v2) nothing else, so a
  reader who typed a chapter name, a theme title or a single glossed word got
  “no results” from a corpus that plainly contains it. `verseSearchText()` now
  also indexes the verse title (all three languages) and every word gloss
  (`w[2..4]`), and a new `SEARCH_PASSAGES` index carries the 18 chapter names/
  subtitles/Devanagari lines and the 169 theme titles/descriptions. Results are
  grouped — Verses, Themes, Chapters — under one count that adds both kinds
  (`hits.length + passages.length`); a group head appears only when more than one
  kind answered, so `2.47` still looks exactly as it did. A verse card that
  answered on a gloss the card does not display says so (`word: अद्वेष्टा — not
  hating`). `searchFoldKey()` also strips any residual combining mark, so plain
  ASCII reaches ṅ/ṭ/ḍ/ḥ/ṃ/ñ — “Sankhya” finds Sāṅkhya Yoga. The priced trade-off
  is the index growing to ~843 KB of strings, which is why a common query costs
  12–50 ms in jsdom; it is built once with the data, not per keystroke.
* **Notes were a side-effect of favouriting, and un-favouriting deleted them.**
  `FAVNOTE` was keyed per verse but written only from the saved cards, and
  `removeFav()` erased the entry with the favourite. Now every verse opens a
  `<details class="m-note">` field in the sheet (`App.library.note/setNote`), the
  note is saved as it is typed, and Saved lists every note — saved or not — as a
  read-only `.note-card`, including on the empty-favourites screen. The storage
  key stays `gitaFavNotes` on purpose: the shipped backup schema and
  `45-data.js` import/export keep working with no migration path to get wrong.
* **Strings:** +7 → 224 UI strings in en/ne/hi (`note_label`, `note_ph`,
  `notes_title`, `search_in_chapters`, `search_in_themes`, `search_in_verses`,
  `search_word_match`). The note wording now matches the verse field already
  shipped in the data: टिप्पणी, not टिपोट.
* **CI was configured to be green.** It called `source/browser_checks.py` (the
  file is at the repo root) and ended the step with `|| echo "browser checks
  skipped or failed"`, so the Playwright suite had never gated a build. It also
  installed Playwright *after* `build.py`, which detects the browser suite with
  `import playwright` — so the build itself reported “browser tests skipped”.
  Playwright now installs first, `build.py` runs the real suite
  (`browser_checks.py --serve`, service worker included), nothing swallows the
  exit code, and `source/prove_data_only.py` runs as its own step.
* **Counts:** 60 Python, **892 assertions** on the document, 286 browser checks,
  506 site-health, 9,658 study-structure, 11 search regressions (was 8).
  `TOTAL_ASSERTIONS` said 832 while the suite printed 867 — reconciled here, and
  the constant is now compared with `PASS + FAIL` so it cannot bless a stale
  number in three files again. `browser_checks.py` got the same lock
  (`EXPECTED_CHECKS`), which is how the real total turned out to be **286**, not
  the 270 three documents claimed: the suite had already drifted seven checks
  (270 + 9 added here = 279), and nothing had ever run it.
* **What the first real browser run found.** Making CI honest turned the suite
  red three times, and each red was a stale check, not a broken app: four checks
  read `.pb-num`/`.pada-row` straight after opening a verse although the
  2026-11-03 card opens on the whole verse and needs one tap for the quarters;
  “no sibling bar” was spelled as “no `.reader-copy` child other than the card
  contains the hint”, true only while `#verseContent` was a direct child of
  `.reader-copy` (it now sits in `#verseContainer`); and “Play retry changes the
  answer position” compared option indexes with `Math.random` pinned to 0 even
  though retry is `LQi++` and the missed question is re-queued — a coincidence,
  not a promise. All three now assert what the app actually promises, and the
  reader sheet's one intended disclosure (the note field) is allowed by name
  instead of failing the “no disclosure card” rule.
  Shell 347,934 chars / 369,749 bytes / 99,694 gzip; README said “about 83 KB”.
* **Shell cap 350,000 → 360,000.** Search v3 and the note field add ~13 KB and
  left 2 KB of headroom, which is not headroom. Raised deliberately, with the
  reason written at the check, in the spirit of the earlier 250→290→320→350
  raises: the cap catches accidental bloat, it does not freeze the UI.
* **Left alone, on purpose:** `img/share-art.jpg` is unreferenced; `srsDueAll()`
  and `App.learn.openDue()` disagree on first chapter and the 7-verse cap;
  `modeSwitch()` has `role="tablist"` with no `role="tab"`; `nav.tabbar` is
  missing from `setAppInert()`. Reported, not fixed in this change.

### 2026-11-03 — the verse card explains its own two states

* Dhruba: the whole-verse hint “▾ ४ पाद” was too terse, and the expanded card
  said nothing about what a pāda does. Both instructions are now real
  sentences, localized in English, Nepali and Hindi, drawn from the two
  existing UI keys (`click_hint_pada`, `click_pada_meanings` — still **217
  keys** × 3, no new strings): EN “Tap this verse to reveal all four pādas” /
  “Tap a pāda to see its word-by-word meanings”, NE “चारै पाद हेर्न यो
  श्लोकमा ट्याप गर्नुहोस्” / “शब्दार्थ हेर्न कुनै पादमा ट्याप गर्नुहोस्”, HI
  “चारों पाद देखने के लिए इस श्लोक पर टैप करें” / “शब्दार्थ देखने के लिए
  किसी पाद पर टैप करें”.
* Both live INSIDE `#verseContent`, the single node that converts between the
  two shapes. The whole-verse hint dropped its absolute corner position and
  the “▾” glyph: it is now a quiet right-aligned capsule in the card's flow
  (so a wrapped Nepali/Hindi sentence can never overlap the Sanskrit lines),
  and it is the card's accessible name. The expanded card gained one plain
  line, `.pada-meanings-hint`, directly above the pāda grid; it carries no
  button, link, role or disclosure and the in-card ↩ stays. No sibling bar,
  hint card or action control returned.
* `aria-describedby` unchanged and still unique: pāda toggles point at
  `#padaHint`, speaker rows at `#wordsHint`; the new hint needs no id.
  Keyboard conversion (Enter/Space), pāda word toggles, master hide/show,
  session restoration of the expanded shape, reader sizing, navigation and
  share/save are untouched; browser checks re-expand after each `setLang()`.
* The two new assertions were folded into the existing card-control check and
  the same-node conversion check, so the suite stays at **270 browser
  checks**; the harness (Playwright) is not installable in this sandbox, so
  the same structure and interaction assertions were run under jsdom (60/60)
  plus the full `python3 build.py` (832 document assertions, ALL GREEN).
  `index.html`, `sw.js` and `sitemap.xml` regenerated.

### October 2026 and earlier — archived

The detailed batch notes from 2026-10-08 to 2026-10-18 (15 batches,
112.6 KB — including the 78.5 KB recovered study-guide record) are in
[`docs/archive/PROJECT-2026-10.md`](docs/archive/PROJECT-2026-10.md). Nothing was
edited in the move; this box keeps the current month's batches and the rationale
that still governs the app is in §1–§10 below.

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
file-sharing entirely, so the split site is now the sole artefact. Published
artifacts are generated from source; never edit the outputs by hand.

Owner: Dhruba Chapain. Licence: none — all rights reserved.

**Content:** 18 chapters · 169 themes · 700 parts · 700 verses, each with
Devanagari, IAST, a four-pāda division, word-by-word meanings, a literal
translation and a paraphrase, in **English, Nepali and Hindi**. All chapter
content is canonical in `source/ch1.json` … `source/ch18.json`, one compact file
per chapter; display lines and meter labels are derived from those fields.

**Features:** trilingual switching, global search, favourites (orderable, each
with a private note), random verse, verse popup with 2×2 pāda boxes and
pada-chheda toggles, continuous chapter reading, keyboard navigation, welcome
screen, the three ways (niṣṭhā), dark mode.

**The Devanagari font ships as real WOFF2 files** (regular and bold), published
beside the app and chapter stylesheet and copied from `source/fonts/` during the
build. Do not remove them: on devices without "Noto Serif Devanagari" (older
Android, most Windows), conjuncts — क्ष, द्ध, ङ्ग — break apart or show as boxes.
The subset fonts are about 42 KB regular + 46 KB bold. SIL Open Font License 1.1;
see `source/fonts/OFL-*.txt`.

---

## 2. The one rule that governs everything

> **The chapter JSON is canonical; code builds it and derives presentation-only values.**

The build compiles each chapter source into the generated chapter payload and
pages. The browser derives the reader's display segments from the verse's
`d`/`t` strings and the meter badge from the `flow` pāda counts. Those are
presentation conveniences, not alternate content: Sanskrit, translations,
glosses, story text, and the pāda segmentation are authored data, never
synthesized or silently repaired by code.

This is mutation-proven, not assumed:

* `source/prove_data_only.py` performs eight temporary edits across chapter JSON
  and UI wording, checks each marker reaches the generated artifact, restores
  the bytes and verifies the baseline artifact hash.
* The old ITRANS→Devanagari converter and metre-splitter (`gita_conv.py`), the
  freeze tool (`freeze_padas.py`), the override workaround (`pada_overrides.py`)
  and the unused `sandhi.py` were deleted. `run_gita_app.js` keeps those retired
  generator paths out of the build.

Do not reintroduce content generation or parallel stored copies of derived
values. Keep the single canonical field and validate it; any presentation rule
must preserve the text exactly and have behavior tests.

---

## 3. Layout

```
index.html            generated app shell — never edit by hand
data/ch<N>.js         18 compact generated chapter payloads, loaded on demand
sw.js, manifest, icons/
sitemap.xml, robots.txt   generated shell/offline and crawler files
chapter/ + chapter.css    generated chapter landing pages
build.py              full build + checks (cross-platform, IDE-friendly)
rebuild.sh            same, as a shell script
run_gita_app.js       892 assertions on the built document and data (needs node)
browser_checks.py     286 browser checks (needs Playwright)
source/
  ch1.json … ch18.json one compact canonical content file per chapter
  app.html             app document template (build-time placeholders)
  css/*.css            ordered feature styles, concatenated into index.html
  js/*.js              ordered feature runtime, concatenated into index.html
  i18n_ui.py           224 UI strings × 3 languages
  study_map_contract.json all 18 reviewed maps + legacy-progress migration
  build_gita.py        assembles templates + chapter data; enforces source schema
  verify.py            IAST normalization and syllable helpers used for checks
  check_padas.py       reconstructs each pāda from nested flow word rows
  check_paraphrase.py  ensures every paraphrase differs from its literal
  check_translations.py safety checks on published translation fields
  check_study_structure.py approved story maps, verse titles and ranges
  prove_data_only.py   8 edit/restore proofs from source through build
```

**Build:** `python3 build.py` (`--fast` skips tests; `--serve` starts a local
server). It clears `__pycache__` first, so a stale compiled file cannot mask an
edit. Browser checks run when Playwright and a compatible Chromium are installed.

---

## 4. Editorial decisions — settled, do not relitigate

**4.1 The running verse is derived from canonical `d`/`t` in `source/ch<N>.json`.**
The browser splits both strings on `।`, pairs the segments in order and marks a
speaker when the IAST segment ends in `uvāca`. Each verse yields two non-speaker
lines; 1.21 and 1.28 correctly keep `अर्जुन उवाच` *between* them. No text is
re-joined or re-sandhied.

**4.2 Pāda boxes show the verse as printed; word lists show the pre-sandhi form.**
The four pādas, syllable counts, five-field word rows and any speaker rows live
in that verse's single ordered `flow` array. So 4.33 pāda 1 ends `…yajñāj` (as
the verse reads) while its word list says
`yajñāt` (the real word). Asked to "restore the originals" in the pāda text, we
decided **no**, because 8.20 disproves any uniform rule: `anyaḥ` + `avyaktaḥ` →
`anyo’vyakto` merges two vowels, so restoring both sides gives 8+9 = 17
syllables in a half-line that must be 16. A rule that works nine times and
breaks the tenth is worse than none.

**4.3 Metre.** Every anuṣṭubh (32 syllables) divides 8/8/8/8; every triṣṭubh (44)
divides 11/11/11/11. Five verses are genuinely irregular and are correct as they
stand: **11.01** (33), **2.29 / 8.10 / 15.03** (45), **2.06** (46). In each, the
extra syllable sits on a pāda that is a complete phrase. The UI derives its
meter badge from the syllable counts in `flow`; neither a separate `mt` tuple nor
a meter label is stored in verse data.

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

**4.10 Part titles must be readable headlines, never raw verse openings.**
Found 2026-08-26 (owner spotted "Karmaṇy-Evādhikāras Te" heading the 2.47
search card while its siblings read like sentences): a part title is a short
readable line in each language ("Action Alone, Not the Fruits" / "कर्ममा मात्र
अधिकार, फलमा होइन" / "कर्म में मात्र अधिकार, फल में नहीं"). A full-class audit
(every part title in all three languages compared against its own verse's
opening) found exactly this one defect; single *terms* like राजविद्या /
"ज्ञानयज्ञ" / "ब्रह्मभूत" are genuine words and stay, as do proper names in
IAST (Bhīṣma, Sāttvic, Puruṣottama) — the established style.

**4.11 `rājā` in 1.02 is nominative — Duryodhana, never a vocative.** The verse
runs `ācāryam upasaṅgamya rājā vacanam abravīt`: the subject is `duryodhanaḥ`, and
`rājā` is apposition — "the king Duryodhana spoke". It shipped as "...spoke these
words, O King", which reads as though Sañjaya address Dhṛtarāṣṭra and, in the
paraphrase, as though Duryodhana addressed *Droṇa* as king (the owner heard this
immediately, 2026-11-04). The edition's own style proves the distinction: 1.16
renders the same nominative `rājā` as "King Yudhiṣṭhira", while the true vocatives
`rājan` in 11.09, 18.76 and 18.77 are "O king". Corrected in en/ne/hi, literal
and paraphrase; the paraphrase now ends "…and spoke:", handing off to Duryodhana's
first words in 1.03. Do not restore the vocative.

**4.12 A theme title must speak for its whole span, not one verse of it.** Found
2026-11-04: the 1.10–1.11 theme was titled "Guard Bhīṣma above all" while its own
description began "Duryodhana compares the forces…" — the title named only 1.11
and left 1.10 unrepresented (the owner spotted the echo of the 1.11 part title).
All 169 theme titles were then read against their verse ranges and their own
descriptions; five were rewording problems and were fixed (1.10–1.11, 8.16–8.19,
17.07, 17.23–17.27, 17.28). The test: a theme title must not restate a part title
inside it, and must not be narrower than its own description. 2.19–2.21 stays
deliberately identical to its part title — see `SAME_TITLE_ALLOWED` in
`check_study_structure.py`; the whole theme *is* that one doctrine.

**Independent title reading (started 2026-11-05):** The 2026-11-04 pass did not ask, for every entry in all three languages, whether a theme title covers the *whole* span in the terms of its own description or whether each localized verse-title claim is actually in that verse. The durable ledger is [`docs/title-audit.md`](docs/title-audit.md); it records the original and proposed title, verdict, evidence and outcome, with each chapter table preceding its canonical edit. The initial endpoint through Chapter 10 is complete (100/169 themes, 414/700 verse titles); The request was then expanded to Chapters 11–18. The expanded independent title audit is complete: all **169/169 themes and 700/700 verse titles** (869 title records) were read in English, Nepali and Hindi. Twenty-two title records were corrected, always after the relevant verdict table: sixteen in Chapters 1–9, one each in Chapters 12–14, and three in Chapter 18. Chapters 8, 10, 11 and 15–17 passed without edits.

The semantic standard is the Sanskrit and this edition’s own Devanagari/IAST plus en/ne/hi literals: a title must not add or contradict a claim absent from its own verse; a neighboring verse cannot supply missing evidence. Theme titles must concisely represent the full span, description and parts. The literal is never changed to make a title fit. Overlap queues prompt a reading only; zero overlap is not a defect, and a title that passes is cleared. No external or AI-corrected dataset was treated as primary authority; generated files were rebuilt from `source/ch<N>.json`, never hand-edited.

The 50-advisory / 0-blocking worksheet lock was preserved. Chapter 8.23’s “two times” advisory was read as a contextual false positive: the verse contrasts return and non-return, with the following verses naming both paths. Chapter 18.29’s “three” advisory is also a contextual false positive: the Sanskrit says *tri-vidham* and all three literals explicitly say “threefold.” An interim Chapter 6 title that named Kṛṣṇa triggered the mechanical name-presence advisory although the range speaks in the first person; that candidate was rejected in favour of a title that avoids unnecessary name inference. Neither validators nor assertion locks were weakened. `source/check_study_structure.py` prints a report-only pointer to the human ledger without changing its returned advisory list. Four added tests currently pin all 22 corrected trilingual title records, exact ledger coverage across all 18 chapters (169 themes / 700 verses), PROJECT scope, and that pointer; ledger coverage is pinned across the full book. Final verification for the expanded scope: `python3 build.py` ALL GREEN; `python3 build.py --prove` PASS; 94 Python tests, 937 document assertions, 560 site-health checks, 9,658 study checks, and 50 title advisories / 0 blocking. At the initial Chapter 10 checkpoint, two consecutive full builds were byte-identical across 42 files (SHA-256 `2504c66f7bb6e597a0470effc779efd761a8ae49f2c2b02a8e28661db3d19b61`); deterministic double-build verification was not repeated after the expanded audit. Browser tests were skipped because Playwright/Chromium is unavailable; no browser/live verification was performed. SEO proof was local-only; Pillow was missing, so share art was not repainted.

--- 

## 5. The build's manual-edit audit

`source/build_gita.py` stops the build if a source file says something the app
would not show, or if the compact source contract is violated. The audit now
runs directly on the chapter JSON; there are no parallel English-only theme,
translation, gloss or pāda modules.

| check | catches |
|---|---|
| compact schema | extra/duplicate chapter, theme, part, verse or flow fields; in particular `name`/`sub`, English `title`/`desc`, and cached `lines`/`padas`/`speakers`/`meter`/`mt` |
| display segments | mismatched `d`/`t` danda segments or a verse that does not yield exactly two non-speaker lines |
| flow reconstruction | pādas that no longer spell the verse IAST (speaker rows excluded), missing/incorrect syllable counts, or incomplete word rows |
| pāda typography | a consonant stranded across a boundary, stray edge/double spaces, incorrect anuṣṭubh/triṣṭubh counts, or an avagraha at the wrong edge |
| transliteration | an unapplied `-aḥ` before a voiced consonant |
| language maps | empty or English-fallback en/ne/hi names, summaries, titles, descriptions, literals or paraphrases |
| verse coverage | any verse missing from all parts or duplicated across parts; every one-verse part must still contain exactly one verse |
| editorial titles | drafting slashes or a raw Sanskrit opening used as a part headline |

`check_padas.py` separately rebuilds each pāda from its nested word rows via
sandhi: **2,800 pādas, 0 residual flags**. It also closes the one link the chain
above never tested — the printed line itself. It transliterates each pāda's
Devanagari `d` and requires it to equal that pāda's IAST `t` (**2,800 lines, 0
flags**; before this, an extra syllable in a `d` failed nothing), and it counts
akṣaras from `d` to confirm the metre and the **five named irregular verses** that
the method page publishes. The approved study-map audit remains
separate and pins the 169 themes, 700 verse titles, and ranges in all languages.

`check_paraphrase.py` measures how much each flowing paraphrase overlaps its
own literal and fails at **80%**. Current medians are en 59.0%, ne 62.4%, hi
63.1%; the highest pair is 79.8%.

**Green means consistent, not correct.** These checks cannot tell that `naśnan`
is not a Sanskrit word. Only reading catches that.

---

## 6. Editing source data

There is no browser-based content editor in this repository. The canonical
sources are `source/ch1.json` through `source/ch18.json`, one compact chapter
record per file. The top-level keys are `num`, `deva`, `verses`, `names`,
`subs`, `themes` and `colophon`. A theme holds `range`, trilingual `titles` and
`descs`, and `parts`; a part holds the same maps plus its `sutras`; a verse holds
only `n`, `d`, `t`, `flow`, `lits` and `paras`.

Each `flow` is ordered. A pāda item stores `k: "p"`, `d`, `t`, its syllable
count `n`, and five-field word rows; a speaker item stores `k: "s"`, `d`, `t`
and its word rows. The browser derives the reader lines from `d`/`t` and the
meter badge from the pāda counts. They are not stored twice. The build enforces
the exact schema so deleted redundant fields cannot silently return.

Edit the source JSON, run `python3 build.py`, and review the result. Do not hand
edit `index.html`, `data/ch<N>.js`, service-worker files or generated chapter
pages. `source/prove_data_only.py` runs eight edit-and-restore experiments for
verse text, a pāda, glosses, translations, a theme title, a chapter name and UI
wording; each must reach the output, and the restored build must match its
baseline hash.

---

## 7. Mistakes already made — do not repeat

* **Regex on file structure destroyed data.** A pattern meant to match a verse
  number matched a pāda index instead, writing 17.19's words onto verse 9 and
  creating phantom verse `0` entries. Recovery was only cheap because a good zip
  existed. **Parse and re-emit; never pattern-match structure.**
* **Fixing one instance of a bug class without enumerating the class.** The
  binary pāda-join flag was "fixed" for 16.1 while 92 other verses stayed broken.
  After fixing anything, scan all 700.
* **Persisting the route but not the preferences.** The app restored *where* the
  reader was from `sessionStorage['gita.route']`, while the reading language was
  never written down anywhere — so its own service-worker reload dropped a नेपाली
  reader back to English on the correct page (2026-10-14, §0). When something
  survives a reload by design, enumerate everything the reader had chosen —
  language, theme, reader size, progress — and check each one is actually stored.
  Two of the three preferences were; nobody had ever listed them side by side.
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
* Call him **Dhruba or brother — never "bhai"** (he corrected this once).
* **Do not follow him blindly**: when he proposes a change, weigh it against
  best practice and argue back if the craft disagrees (standing order,
  2026-08-30). He has reversed his own designs twice and thanked the push.
* **Always deliver the total repo zip**, never a partial one (standing
  order, 2026-08-31) — it is the checkpoint a new session rebuilds from.
* Write every decision into this file the moment it is made; the zip plus
  this file is the entire crash-recovery story.

---

## 9. State at the time of writing

*Verified 2026-08-26: local source was re-synced to GitHub and brought to the
state that exactly reproduces the live site — `python3 build.py` now rebuilds
every published file byte-identically (only `sitemap.xml`'s `lastmod` carries
the build date).*

* **2026-08-31 — per-verse share pages v/N.N/ (owner: the WhatsApp preview
  "must display the verse", not the logo; asked for alternatives first —
  edge-prerender rejected as external infra, query-param tricks dead on
  static hosting, 700 images rejected at ~35 MB because it would poison the
  drag-drop flow; micro-pages are the only option that lives on pure GitHub
  Pages).** The build now writes 700 ~2.8 KB pages under `v/`: og:title =
  "Bhagavad Gita N.N · <part title>", og:description = the Devanagari + one
  English line + "Click the verse to see the word-by-word meanings.", NO
  og:image on purpose (the text card shows the verse; a logo thumbnail was
  the stupid part). Humans bounce via meta-refresh/JS into the invitation
  landing; crawlers keep the verse. Deliberately out of the sitemap (share
  endpoints, not content). `shareUrl()` now emits the v/ URL everywhere —
  panel, copy button, downloaded copies. ONE-TIME UPLOAD: the whole `v/`
  folder (700 files, one folder drag) plus `index.html` + `sw.js`.
  SECOND ROUND, same day (owner saw the text-only WhatsApp card: "just
  texts???"): 700 painted verse cards were tried (≈28 MB) and REJECTED by the
  owner for weight; his counter-proposal won — ONE painted artwork
  (`img/share-art.jpg`, 43 KB: teal header band with the site name, saffron
  double frame, the book's Devanagari name, the click-line promise) is the
  `og:image` for every v/ page; the verse itself rides in og:title/
  og:description as two pādas + the click line. `summary_large_image`.
  Human-facing numbers obey doctrine (1.1, never 1.01); URLs keep the padded
  data form. Upload set: `v/` (re-drag) + `img/` (one file) + `index.html` +
  `sw.js`.
  THIRD ROUND, 2026-08-31 (owner drove the link in WhatsApp, saw the empty
  card — "the top portion with the teal and information about the app is
  good. In the middle there must be the verse topic, verse number, the verse
  itself, the verse description, then a message to click for the
  word-meanings"): the one-artwork preview REVERSED. Every v/ page now
  carries its own painted card `img/v/N.NN.jpg`, following exactly that
  stack: teal band holding the app title, the Devanagari chapter/verse line
  AND the TRILINGUAL lineup (Trilingual · English · नेपाली · हिन्दी, drawn
  mixed-script — the Latin font has no Devanagari glyphs), then verse topic ->
  verse number -> the verse (two pādas) -> verse description (≤2 lines,
  ellipsis) -> the click-for-meanings line. Vertical slots are FIXED so
  nothing can collide; 700/700 audited with 0 edge overflows; the 600×315
  version was built first but the owner called it "not quality" and moved to
  FULL-RES 1200×630 (kept crisp when a platform upscales or renders high-DPI)
  at JPEG q=88 — ~95 KB avg, **~68 MB total**. The painter runs at every
  build (not behind a flag); fonts bundled at `source/fonts/share-*.ttf`
  (Pillow missing → warn and skip, og:image will 404 until regenerated).
  `share-art.jpg` is now orphaned (no v/ page references it). Doc-locks in
  `run_gita_app.js` + `source/verify_share_pages.py` updated (og:image =
  img/v/N.NN.jpg, 1200×630, card file exists; audit verifies all 700 cards +
  sizes). One-time upload: `img/v/` (700 files) re-drag + `index.html` +
  `sw.js`.
  FOURTH ROUND, 2026-08-31 (owner came back after the cards were LIVE: "i
  don't think i am happy with the aesthetics of the card… what do you
  think?", then — asked to steer — "maybe 1 devotional would be great…
  i'll let you be the judge of what truly captures the essence"). The flat
  cream + thin rules + small gray text read like a form, not a sacred text.
  I built four directions (editorial-teal / manuscript / elevated-band /
  dawn-gradient), the user gave me the mandate for the DEVOTIONAL MANUSCRIPT. Final
  card: aged-paper backdrop (subtle warmth gradient), double saffron-gold
  frame + corner diamonds, a centered ॐ medallion as the focal point flanked
  by silk rules, header (Devanagari title / English name / Trilingual · English
  · नेपाली · हिन्दी in gold) -> verse topic -> verse number -> the verse (two
  pādas) -> verse description (≤2 lines, ellipsis) -> teal click-for-meanings
  invitation. Vertical slots FIXED so nothing collides. 700/700 rebuilt,
  audited ALL GREEN (0 mismatches), overscan 0/700, browser checks pass.
  ~91 KB avg, **~65 MB total**. `share-art.jpg` still orphaned. The v/ pages
  still point at img/v/N.NN.jpg (unchanged URL — only the card artwork
  changed), so the ONE-TIME UPLOAD is again just `img/v/` (700 files re-drag,
  ids unchanged) — `v/`, `index.html`, `sw.js` carry no card art so they are
  already correct.
  FIFTH ROUND, 2026-09-01 (owner: "that simply bumped my site size from 2 or
  3 MB to 60+ MB… i have decided to let go of this idea"). The per-verse card
  idea is CLOSED. The painter loop is deleted from `build_gita.py` (only the
  single `img/share-art.jpg` painter remains), the v/ page template points
  og:image / twitter:image at `{SITE_BASE}/og-card.png` (1200×630,
  summary_large_image kept), and both doc-locks were inverted: `run_gita_app.js`
  and `source/verify_share_pages.py` now FAIL if any v/ page mentions
  `/img/v/` or if the `img/v/` directory reappears, and they check that
  `og-card.png` exists at 1200×630. Rebuilt: 700 pages, verifier ALL GREEN
  (0 mismatches), 553 document assertions pass. The lesson worth keeping:
  a per-item og:image is a 700× multiplier on repo weight — only pay it if
  the image carries information the og:title/og:description cannot.
* **2026-08-31 — a shared verse lands as an invitation (owner: "the link
  should display the verse and say click the verse to see the meaning").**
  `#v=N.N` no longer pops the sheet on load; it sets `state.shared` and the
  welcome page shows that verse in the VotD slot under a SHARED VERSE chip,
  with the hint line ("Click the verse to see the word-by-word meanings." /
  "शब्द-अर्थ हेर्न श्लोकमा क्लिक गर्नुहोस्।" / "शब्दार्थ देखने के लिए श्लोक पर
  क्लिक करें।" — keys `shared_label`/`shared_hint`, i18n now 101). One tap
  opens the four-pāda sheet. Entering the Gita clears the shared slot so the
  daily verse returns. Locked: landing shows verse + hint with no popup,
  click opens the sheet.
* **2026-08-30 — ONE chip grammar for every choice (owner: bigger crumbs;
  the study-style options and the language bar should read like the crumbs —
  soft when unchosen, gold when current, warming on hover; "the circular
  boundary makes them look like cleaner options").** Crumbs grew to .88rem
  (.8rem on phones). The mode segments retired their paper track and became
  chips; the language bar left its translucent iOS track for the same pills.
  Everywhere now: soft pill = an option, gold pill = where you are, hover =
  saffron-dark fill. Three choosers (trail, tray, header) finally rhyme.
  2026-08-31 volume control: ancestors neutral, current soft, tray
  hairline — locks updated to the stepped-down palette. The language bar
  tried the chip grammar for one round and was reverted on the owner's eye
  ("revert to previous looks") — iOS segment restored, but its hover keeps
  the warming (locked: active tongue raised on paper, hover saffron-dark).
* **2026-08-30 — study guide: theme is the door, verses are the display
  (owner: "let the theme be clickable, but not the verses … same box card
  style as the chapter list").** The verse rows inside the theme box were a
  tap target nested in a tap target — an ambiguity too many. Now each verse
  shows as a display-only `.card .vcard` (number chip in the saffron pill,
  serif title one notch below the theme title, description) in a responsive
  grid inside its theme; no pointer, no hover lift — the theme box stays
  the single door, and a press on a verse card simply bubbles to it.
  Word-by-word lives one level deeper in the verse grid. Locked by three
  checks (cards exist with chip+title+desc, none is a button, pressing one
  opens the grid, never the modal).
* **2026-08-30 — the two-eyed audit (owner: "look at everything, painter's
  eyes then programmer's").** Painter: four saffron grounds carried cream
  lettering at ~3:1 contrast — Enter-the-Gita CTA, the modal's Random, the
  ✕ close, the IN OTHER WORDS pill. One rule now governs them all:
  *saffron ground always gets the lamp-black letter* (`--on-saffron`, one
  value per theme). The grey "Hide meanings" was examined and acquitted —
  that is the sleeping disabled state, teal when awake. Programmer: the
  tappable divs (chapter/section cards, theme boxes, verse rows, result
  cards, VotD) now carry `role="button" tabindex="0"` and a global
  Enter/Space handler — the mouse no longer has a monopoly (locked by a
  check); the search field is 16px on mobile so iOS stops zooming on
  focus; trail chips grew to a 32px thumb target. Already-audited-and-clean
  list: theme-color meta synced by JS, prefers-reduced-motion, global
  saffron :focus-visible, Escape/arrows/swipe in the sheet, safe-area
  insets, sticky nav + tail spacer, no-JS fallback. Noted, not changed:
  Devanagari blocks could carry lang="sa" for screen readers someday.
* **2026-08-30 — the trail became chips (owner: "not prominent … chapter1,
  chapter2 style").** Taken, with one refinement argued and kept: chips are
  how this app labels structure, so ancestors wear the chapter-list's
  saffron-SOFT pill (a door you can walk back through — hover fills it
  saffron-dark) while the current page wears the gold-leaf chip, the same
  metal as the tray's raised segment (soft = door, gold = where you stand).
  Making every crumb solid gold was rejected in the entry: prominence
  everywhere is prominence nowhere. No uppercase/letter-spacing on these
  chips — the crumbs mix Latin and Devanagari and tracking strains the
  mātrā flow. Two browser checks lock the soft/gold split and the hover
  fill in both themes.
* **2026-08-30 — the saffron paint (owner handed over the brush: "give the
  box a saffron outline, change the text color, on hover and selection do
  something — you do what you like").** The tray is now the ONE saffron
  object on the chapter page: saffron frame, the instructive line in
  saffron-dark, hover warms an unchosen segment with the chip's
  saffron-soft wash, and the chosen way rises as gold leaf — `--saffron`
  ground with a new `--on-saffron` lamp-black letter (one variable per
  theme, so dark mode inverts correctly). Content cards keep their
  hairlines; the accent still means something. Two browser checks lock the
  frame/instruction/raise colours and the hover wash in both themes.
* **2026-08-30 — the tray (owner: "put the choose and the three options in
  a box, and instead of just choose, make it instructive").** The
  instruction and the segmented control now live in one hairline tray —
  same paper body, hairline and 16px radius as every card — so the chrome
  reads as one quiet object set apart from the scripture below. The line is
  the full question again (`choose_title` revived in place of
  `choose_short`: "How would you like to receive this chapter?" /
  "यो अध्याय कसरी पढ्न चाहनुहुन्छ?" / "इस अध्याय को आप कैसे पढ़ना चाहेंगे?"),
  because a sentence hosts and a word merely labels. Still 99 keys.
* **2026-08-30 — the intermediary choice page is RETIRED; the three ways
  ride on the chapter page as a segmented control (owner: "clicking the
  chapter and going into an intermediary choice page is just making things
  weirder … put these three choices in the structure like the language
  options, and on top of it say choose").** So: one quiet line — Choose /
  छान्नुहोस् / चुनें — above an iOS-style segmented control (`modeSwitch`),
  the same grammar as the language pills: paper track, hairline border, the
  active way raised in teal. Clicking a chapter card now opens the chapter
  itself (mula, "that is what a chapter is"); the segments move between
  Verses only / Verses with translation / Study guide without leaving the
  page; the descriptions ride in title/aria so the control stays quiet but
  never cryptic; bare `#chapter=N` deep links open the chapter directly and
  `&tab=` still pre-selects a segment (the SEO CTAs are untouched). The
  chapter page gained a proper heading (Devanagari name in saffron + Latin/
  Devanagari title) so the page knows its own name now that no choice page
  announces it. Running head reads "Chapter 2 · मूल" / "· अध्ययन" as one
  compound current crumb. i18n: −`choose_title`, −`crumb_choice`,
  +`choose_short`, +`opt_study_s` (still 99 keys). showChoose and the whole
  `.choose`/.opt CSS are gone from the generator.
* **2026-08-30 — the breadcrumb became a running head, and the lost door was
  found (owner: "not appealing to my eyes and my intellect"; and landing in a
  chapter left no way back to the choice page).** Two defects, one cure.
  Intellect: the trail now always ends at where the reader *is*. A last
  item may be a compound — live link + middle dot + current tail — so the
  chapter pages read "Chapter 2 · मूल" (owner's own wording) with the
  chapter half still a LIVE link back to the choice page (wayCrumbs used to
  render any last item as dead `.wc-cur` text, silently discarding its
  action — that was the missing door), and the choice page names itself:
  "… › Chapter 2 · Sāṅkhya Yoga › Choice of study style" (`crumb_choice`,
  ne "अध्ययन शैलीको छनोट", hi "अध्ययन शैली का चयन"). Same pass fixed a
  language-switch bug: setLang had no `choose` branch, so changing language
  on the choice page fell into showThemes — the study guide appeared out of
  nowhere; now the choice page re-renders as itself (locked by a check). The way crumb carries its niṣṭhā's Sanskrit name, as the landing
  cards do ("कर्मनिष्ठा · The Way of Karma"), in every language. Eyes:
  ancestors recede to `--ink-soft` at regular weight, separators are the
  faintest thing on the line, the current page is the darkest (`--ink`,
  bold) — the eye lands on "where you are" without being told — and hover
  speaks saffron, the app's one accent language, instead of the old teal
  bold mini-headlines that all shouted equally. `nav[aria-label]` +
  `aria-current="page"` for screen readers; Devanagari in the trail renders
  in the embedded serif. Locked by browser checks: trail shape, niṣṭhā
  name, and clicking the chapter crumb landing on the choice page.
* **2026-08-30 — the dropdown is gone; a chapter opens through a choice
  (owner's design).** The "View mode" select under the breadcrumb read like a
  form control in the middle of a reading flow. Now clicking a chapter card on
  the way-page lands on a quiet **choice page** with three doors —
  *मूल · Mula* (verses only), *With meaning* (verses + translations),
  *Study guide* (thematic breakdown) — and the chapter itself only appears
  after a door is picked. `showChoose(ci)` is view `choose`; the three options
  route to `showRead(ci,'mula'|'full')` / `showThemes(ci)`; `#chapter=N`
  alone lands on the choice, `&tab=mula|full|study` still opens a door
  directly (the SEO CTAs keep `&tab=study`); the breadcrumb's chapter crumb
  links back to the choice. i18n is now **99 keys** (+`choose_title`,
  `opt_mula`, `opt_mula_d`, `opt_full`, `opt_full_d`, `opt_study`,
  `opt_study_d`, `opt_mula_g`, `opt_full_g`, `opt_study_g`, `opt_go`;
  −`view_mode`).
  Second pass the same day (owner: "keep our consistency … the box card
  style which we use in chapter list display"): the three doors became
  **literal `.card` elements in the same grid as the chapter list** — the
  Devanagari word (मूल / अर्थ / अध्ययन) sits in the chapter chip's saffron
  pill, serif title, description, "Choose →" where the chapter card says
  "Open chapter →". The first pass's permanent gold frame and gold-leaf
  hover flood were retracted on the owner's call, and he was right: they
  were the loudest things in the app, and a threshold must not outshine the
  scripture. Now the doors obey the same contract as chapter cards —
  hairline `--line` at rest, saffron outline on hover — proven byte-identical
  by browser checks that read the real computed colours of both. Two
  deliberate micro-deviations, argued and kept: the deva chip drops the
  Latin habits (uppercase/letter-spacing strain mātrā flow, .72rem is too
  small for Devanagari) while keeping the pill's colours; and the doors stay
  `<button>`s (chapter cards are `<div>`s) so keyboard users get doors too,
  at zero visual cost. Same pass fixed a data scar: the hi choice strings
  had been copied from नेपाली — now genuine Hindi, and a suite lock
  (`copiedNeHi`) makes the copy impossible again.
  **Pending upload vs live, re-diffed 2026-08-31: only `index.html`,
  `sw.js`, `sitemap.xml`** — the owner uploaded the 18 chapter pages and
  `chapter.css` between rounds (verified byte-identical live). The old
  "22 files" figure was a cumulative sync gap, not a per-round delta;
  `downloads/upload-3-files.zip` carries exactly the three. (`sitemap.xml`
  is optional — same 19 URLs, fresher `lastmod`.)
* **2026-08-30 — the in-app chapter view became the purana view (owner's
  reading notes).** Verse rows now read title → description with a saffron
  verse number, the whole theme box is clickable, theme numbering is gone,
  and the glaring white headings dropped to `--ink-soft`. Six fixes, all
  locked by the browser suite.
* **Split build** (standalone retired 2026-08-24): `index.html` =
  **`4a7e8141f624`** (2026-08-26: share-from-file fix on top of the synced
  baseline `f39e4e509dd6`), a **116 KB gzipped shell** that loads 18
  `data/ch<N>.js` files in parallel at startup and boots when all arrive.
  `sw.js` cache `gita-cd8659fffded`, precaches the shell **and all 18 data
  files** — fully offline after the first visit. There is no
  `gita-standalone.html`; the app is shared by link. **Pending upload:
  `index.html` + `sw.js`** (the share fix).
* **Share redesigned** (2026-08-26, owner's direction): the Share button no
  longer calls navigator.share at all — it opens a quiet panel ("Like this
  verse? Copy the link and share it with friends." + the link + Copy button),
  i18n'd in all three languages. `shareUrl()` builds the link from `og:url`
  whenever the app is not on http(s), so even a downloaded copy shares the
  LIVE verse link (and the file:// crash path is gone with navigator.share).
  `index.html` = **`1f2c6ca253bd`**, cache `gita-e67014dc70bc`.
  **Pending upload: `index.html` + `sw.js`.**
* **Search results reformatted** (2026-08-26): result cards now mirror the
  verse-of-the-day card, headed by the verse's OWN part title (the one label
  that truly describes that verse — owner's addition), then Devanagari,
  translation, an unambiguous "Verse 2.47 · Chapter 2: Sāṅkhya Yoga" line,
  then "Open verse →". The old misleading top line ("3.5 Karma Yoga") is
  gone. The browser suite reads `.mini .m-ref` and checks the headline
  against the data. The 2.47 part-title defect ("Karmaṇy-Evādhikāras Te",
  §4.10) fixed in all three languages on top (data-only change — the shell
  `b4dc17d4c8c1` carries no data; cache `gita-b5bb39971923`).
  **Pending upload vs live: `index.html` + `sw.js` (part-title UI) +
  `data/ch2.js` (title fix).**
* **Verse cards unified** (2026-08-26, owner's "keep it simple and
  consistent"): the VotD and search cards now look exactly like the in-theme
  verse cards — *Verse N* line, Devanagari (plain, no inline daṇa number),
  80-char paraphrase snippet — plus the part title as headline (the one
  allowed addition) and the VotD label on the welcome card. No where-line, no
  chapter/theme/part numbers on cards (structure lives in the modal crumb).
  Dead CSS (wd-*, m-where, m-open) removed. Locked by browser checks on both
  cards and on the theme cards' anatomy.
* **700-verse part-title audit** (2026-08-26, owner's request now that part
  titles headline the cards): all 700 part titles read against their verses —
  clean after the 2.47 fix. One theme-title scar fixed: ch15 theme 2
  "… / the Traveler" → "The Path to the Supreme Abode" (en/ne/hi), content
  locks updated. The lesson is now audit check 5 (§5 table).
* **VotD card centred** (2026-08-26, owner's eye): the welcome card is a
  display piece, so its content is centred while the search/theme grids stay
  left-aligned for reading. **Headline-first order** on both cards (part title
  above the verse number — title → meta → body). Both locked by checks.
* **One verse = one part** (2026-08-26, owner's aim: titles that stick to
  memory — the terms Gita Purana / Gita Darshana / Gitopanishad are the
  owner's later layers, set aside for now): the word "part" is gone from the
  UI; every verse carries its own title in all three languages, shown in the
  theme view head, the modal crumb and the cards. **All 18 chapters converted
  (2026-08-27): 202 themes, 700 one-verse parts, 0 duplicate titles** — audit
  check 6 (`CONVERTED = set(range(1,19))`) now enforces one-verse parts
  everywhere. Theme splits follow story beats (ch1 18, ch2 18, ch3 12, ch18
  keeps the owner's fine-grained 15). Counts locks: 202 themes · 700 parts.
  (That earlier pending list is now closed — see the 2026-08-30 entry for the
  current one.)
* **Meter badge stays visible** (2026-08-26, owner's call after discussion):
  "anuṣṭubh · 32 syllables · 4 quarters of 8" remains in the verse sheet; it
  was considered for removal/conditional display but kept as-is.
* **Modal crumb now unconditional** (2026-08-26, owner spotted the drift):
  the "Theme N · … » Part N · …" line was gated on mode==='theme', so verses
  opened from search/VotD/random/favorites lost it. Same verse now reads the
  same from every entry path; locked by a browser check opening via search.
  Build `6aa0850ffcc8`, cache `gita-333f907fddca`.
  **Pending upload vs live: `index.html` + `sw.js`** (card restructure +
  crumb fix).
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
* Full suite green: **537 assertions + 116 browser checks (incl. offline SW) +
  2800 pādas + 2100 paraphrase pairs**, and `prove_data_only.py` passes all 7
  cases against the published build.
* Upload method: unzip → select everything *inside* → **Add file → Upload files**
  → Commit. Uploading never deletes; removed files must be deleted by hand, or
  delete the `source/` directory first and re-upload it.
* **2026-08-28 — third view option renamed (owner):** "Study Mode" in
  English, "अध्ययन शैली" in ne/hi — short labels win.
* **2026-08-28 — "Save" → "Add to favorites" (owner request).** Names the
  place, matches the toolbar's Favorites and Apple's own wording; saved state
  reads "In favorites" so the pair tells the story. Trilingual.
* **2026-08-28 — dark-mode rebalance + segmented control (owner: "colors a
  bit bright… more applish").** Dark accents were neon against the warm black
  (#E8912C orange, #7FD4E8 cyan, glaring cream text). Rebalanced to Apple-dark
  discipline: saffron #E1953A/#C8862F, teal #8FC1CE, ink #E9DCC3, softer
  hdr-sub. The scattered language pills became one iOS segmented control —
  translucent track, active language raised as a neutral paper segment; the
  orange left the header entirely.
* **2026-08-28 — the sleek pass (owner's Apple benchmark).** Removed the
  gaudy: header gradient flattened and its 5px orange rule dropped (colour
  contrast alone separates it); every 2px chrome border → 1px hairline; card
  top-strips and solid orange chips → soft tint-on-cream; page titles teal →
  ink (colour is for content and links); drop-shadows reduced to a whisper and
  all hover-lifts (translateY) removed — hover now only warms the hairline.
  The verse sheet's 4px saffron picture-frame became a hairline too. Structure
  untouched; 34 CSS rules.
* **2026-08-28 — second sweep: search ✕, share image, small polish (owner
  asked "what else?").** The standing "Clear" button became the modern
  in-field ✕ that appears only while the field has text (aria-labelled from
  `clear`); WebKit's own duplicate cancel button is suppressed. Added
  `og:image` (+`twitter:card`) so shared links carry the app icon on
  WhatsApp/Facebook. `::selection` now saffron. Audit conclusion: no tab
  strips remain anywhere — the language pills are a standard segmented
  control and stay.
* **2026-08-28 — chrome modernisation pass (owner request: "make it look
  not less than any other site").** (1) Dropdown: en label is now plain
  "Verses only"; the native OS arrow is gone — a custom chevron sits 14px
  inside the pill (teal in light, sky in dark). (2) Every emoji in the chrome
  (🏠 🔍 ☆ ★ 🎲 🙈  ☾ ☀) replaced with inline stroke SVGs that inherit
  `currentColor`, so they match the type and both themes and render
  identically on every OS. (3) Modern basics added: `:focus-visible` saffron
  outline and `prefers-reduced-motion` stillness. i18n strings are now
  emoji-free in all three languages.
* **2026-08-28 — the chapter tabs became a "View mode" chooser (owner
  request).** The stacked mūla/translation/study pills read like a menu; now
  one quiet line under the breadcrumb — *View mode: [ मूल · Mula (verses
  only) ▾ ]* — a native select styled as a pill, mula default, three options.
  New key `view_mode` (88 keys); the `.read-tab`/`.ch-tabs` CSS is gone. Also
  caught a Hindi gap from the label-polish round: hi `tab_study` had never
  received the "· विषयगत विभाजन" suffix — fixed. Suite: **524 assertions +
  121 browser checks.**
* **2026-08-27 — the meanings switch sleeps until needed (owner
  request).** In the verse sheet the 🙈/👁 hide-show-meanings button is
  disabled until a quarter is actually opened — before that there is no
  meaning on screen to hide. Closing the last open quarter puts it back
  to sleep and resets it to "hide". Suite: **522 assertions + 121
  browser checks.**
* **2026-08-27 — way-pills became a breadcrumb (owner request).** "Too many
  tabs" once inside a chapter: the karma/bhakti/jñāna pill strip is gone from
  every drill-down view, replaced by a quiet trail —
  `The Three Ways › Way of Karma › Chapter 2 · Sāṅkhya Yoga` — ancestors as
  links, current page last. It doubles as the page header, so the duplicate
  big titles (and the verses page's old mini-crumb) were dropped; only the
  mūla/meaning/study tab row remains as pills. Foot back-buttons kept for the
  long pages. Suite: 522 assertions + 118 browser checks.
* **2026-08-27 — part-count noise removed (owner request).** With every part
  holding exactly one verse since the big conversion, "3 verses across 3
  parts" and the theme cards' "3 Part · 3 verses" said the same number twice.
  Both now read just "3 verses". Keys −5 (`part`, `parts_postfix`,
  `verses_across_parts`, `verses_across_part1`, `verse_across_part1`) → 87.
  Suite: **522 assertions + 118 browser checks.**
* **2026-08-27 — label polish round (owner request).** Tab labels now carry
  their meaning: "मूल · Mula (verses only)", "Verses with translation",
  "Study guide · thematic breakdown" (ne/hi in step); on ≤560px the three
  pills stack full-width so the longer labels never squeeze. Mula's sub now
  says "tap any verse for **word-by-word** meanings". The VotD/search topic
  line is demoted to the same soft colour as its "Verse topic:" prefix — the
  Devanagari is the star of those cards, not the title.
* **2026-08-28 — second verification pass (owner: "the data cannot be
  wrong").** (a) Verse text: every Devanagari pāda and its IAST transliteration
  compared character-for-character against the Śaṅkara-source `chN.json`
  (normalising only orthographic conventions: daṇas, anusvara/halant,
  avagraha, pāda-boundary sandhi) — residual 0 for all 700 verses in both
  scripts; `check_padas.py` 2800/0; per-chapter coverage exact. (b) Editorial:
  a misplacement heuristic (description vs own-verse vs neighbour-verse
  overlap) flagged 12 parts whose descriptions borrowed a neighbouring verse's
  content (1.22, 1.32, 1.42, 1.43, 2.01, 2.04, 2.26, 3.39, 5.27, 11.05,
  13.10, 18.50) — each rewritten to its own verse, trilingually. Heuristic,
  dups, ellipses, latin-in-Devanagari all now report zero.
* **2026-08-28 — beauty pass on the purana chapter view (owner: "make it
  look beautiful").** Warmth returned without the old gaudiness: saffron
  left-accent on each theme card, saffron theme numbers, soft-saffron verse
  chips with teal titles, Devanagari chapter name in saffron; same accents on
  the static chapter pages. In-app chapter view restyled to the purana style
  (narrative blocks + clickable chips); `#theme=N.M` deep links added.
* **2026-08-28 — audit regression fixed (owner spotted "Kṛṣṇa Smiles"
  twice in ch2 while browsing Nepali).** Root cause: during the ch18 repair I
  restored `themes_ne.py`/`themes_hi.py` from the pre-audit zip, silently
  rolling back the ne/hi half of the audit (ch2/ch3 theme rewrites, 4.29 /
  10.05 titles, the Hindi ellipses, the एकagr fix) — and the first scan had
  also checked ne *titles* instead of descriptions, missing 11 Nepali
  ellipses. All re-applied; the final battery (dups / ellipses / latin-in-
  Devanagari / lowercase starts, all three languages, all 18 chapters) now
  reports CLEAN. Lesson logged: never restore a whole file over partial
  fixes; restore per-hunk.
* **2026-08-28 — complete editorial audit of all 700 parts / 202 themes
  (owner: "make it complete and categorical").** Every theme and part title
  and description in en/ne/hi was read against its verse's literal
  translation. Found and fixed: (a) ch2 T7–T18 and ch3 T6–T11 had theme
  headers duplicated from earlier themes, mismatching their verses — all 20
  rewritten trilingually; (b) 31 part descriptions ended mid-sentence in "…"
  (en) + 14 (hi) — completed to full sentences; (c) ~30 ch18 part
  descriptions were copies of the previous part — each rewritten to its own
  verse, trilingually; (d) wrong titles: 4.29 "The Guru's Grace" → "Breath
  Offered to Breath", 10.05 "The Seven Seers and Manus" → "All These States
  Arise from Me"; (e) spelling: "Kpa" → Kṛpa, "Pāṇava" → Pāṇḍava, "Gāṇīva" →
  Gāṇḍīva (1.30), "Dhṣadyumna/Virāa" → Dhṛṣṭadyumna/Virāṭa (1.17), "एकagr" →
  एकाग्र (ne/hi 2.44), comma in 8.26, lowercase-start descriptions (5.09,
  6.12, 6.14). Suite green after the pass.
* **2026-08-27 — the door is the Three Ways (owner request).** "Enter the
  Gita" now lands directly on the Three Ways — the top tab strip
  (Three Ways / All 18 Chapters) and the flat 18-chapter list are gone.
  Path: Ways → a way's six chapters → chapter tabs. Direct access to a
  chapter still exists via search, VotD, `#chapter=N` links and the SEO
  pages, so nothing is lost but the door is calmer. Keys −5 (`tab_ways`,
  `tab_all18`, `choose_chapter`, `choose_chapter_sub`, `browse_all`) → 92.
  Back-buttons and crumbs derive the way from the chapter number when no
  section is set. Suite: **532 assertions + 118 browser checks.**
* **2026-08-27 — chapter tabs: Mula / With meaning / Study guide (owner
  request).** Entering a chapter no longer lands on the themes page with a
  buried "read the whole chapter" button. Three peer tabs now sit at the top
  of every chapter view: **मूल · verses only** (default entry), **With
  meaning** (verse + literal + flowing paraphrase, *no* word-by-word — that
  stays in the verse sheet), **Study guide** (the themes/parts breakdown).
  `#chapter=N` deep links default to Mula and accept `&tab=study|full|mula`;
  the 18 SEO chapter pages' CTA now targets `&tab=study`. Keys:
  +`tab_study`, `read_sub_mula`, `open_chapter`, −`read_chapter`,
  −`read_title` → 97. Suite: **542 assertions + 124 browser checks.**
* **2026-08-27 — verse-card colour hierarchy + share wording (owner
  request).** (1) The VotD and search cards had three saffron elements stacked
  on top (label, part title, verse number) — the pile-up read as one orange
  blob. New anatomy: the VotD label is a small **oval pill** (saffron-soft
  background), the **verse number** leads in saffron, and the part title
  became a `Verse topic: …` line in **teal** (new `verse_topic` UI key, 96
  keys now) under the number — orange is metadata, teal is content. Locked by
  2 new browser checks (pill radius, topic ≠ number colour) + the rewritten
  order/headline checks; suite now **120**. (2) Share button wording: ne
  "साझा" → **"शेयर गर्नुहोस्"**, hi "साझा करें" → **"शेयर करें"** — the
  owner's ear rejected the Sanskrit register for a UI button.
* **2026-08-27 — share panel collapses on copy (owner request).** Clicking
  "Copy verse link" now hides `#sharePanel` immediately and flashes
  "Link copied" on the Share button (`#shareBtn`) for 1.6 s, instead of only
  relabelling the in-panel copy button. Both the clipboard path and the
  `execCommand` fallback collapse it. Locked by 2 new browser checks
  (suite now **118**): panel `display:none` after a real click on `#shCp`,
  and the Share-button confirmation text.

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
* **If Search Console says "Couldn't fetch", prove the file, don't guess.**
  The status is often stale or the submitted URL is wrong, and GSC never says
  which. `python3 source/check_seo.py --live` prints the real answers: the
  status code and `content-type` of the published `sitemap.xml`, the parse
  result, a fetch of every `<loc>` inside it, and the three near-miss URLs a
  submission box invites — all verified against the live site.
  What it found on 2026-08-30: `sitemap.xml` → **200, `application/xml`,
  2883 bytes**, 19 URLs, all 19 fetch 200, no BOM; while
  `sitemap.xml/` (trailing slash), `Sitemap.xml` (capital) and the
  path-dropped `https://chapain.github.io/sitemap.xml` are all **404**. So on
  this site the trailing-slash "fix" you read about online would *create* the
  error, and the file itself needs nothing. There is no `_config.yml`, so
  GitHub Pages is not running Jekyll here and a `.nojekyll` file would change
  nothing. What is left is Search Console itself: confirm the submitted URL is
  `https://chapain.github.io/Bhagavad-Gita/sitemap.xml`, run *URL inspection*
  on it, and give the status a few days to refresh.
* **hreflang is deliberately absent.** All three languages live at one URL
  (in-page switching); hreflang requires distinct URLs and would be wrong here.
  The `og:locale:alternate` tags already cover the sharing case.
* **Realistic strategy.** The head term "bhagavad gita" belongs to Wikipedia
  and the big Gita sites. The winnable queries are the long tail this app
  uniquely answers — *bhagavad gita in nepali*, *भगवद्गीता नेपाली अनुवाद*,
  *gita word-by-word meaning* — plus backlinks (GitHub repo topics, Reddit
  r/Hinduism / r/bhagavadgita, Quora, Facebook groups for Nepali readers).
  The execution kit for that half — drafts for each channel in the author's own
  voice, the monthly cadence, what not to do, and the fact that without
  analytics the honest instruments are Search Console and GitHub's referrer
  list — is `docs/outreach.md` (2026-11-04). It is a working document, not
  published site content.
* **Title and description are branding decisions** — the suite locks the exact
  `<title>`; changing it means updating `run_gita_app.js` and
  `browser_checks.py` deliberately, together with this file.
