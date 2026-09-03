# PROJECT.md — everything needed to pick this up cold

If you are an assistant resuming this project with nothing but the repository,
read this file first. `README.md` explains how to *use* the project; this file
explains *why it is the way it is*, and records decisions and mistakes that the
code alone cannot tell you.

---

## 0. Handoff snapshot (keep current; last touched 2026-09-01)

For a brand-new session: read §1–§10, then this box, then build.

* **Study one at a time + resume (owner 2026-09-01).** The owner asked to
  paginate Mūla, Full and the themes page to one item per screen. Two of the
  three were already built and the third would have hurt, so what shipped is:
  - **The sheet ALREADY did one-verse-at-a-time** with Prev/Next and a counter,
    in three scopes (theme / book / favourites). The gap was not the feature,
    it was the DOOR: nothing on the reading pages said so, and a reader had to
    already know that tapping a verse starts a walk. Mūla and Full now carry a
    "Study one verse at a time →" button that opens the chapter's first verse
    in **'book'** mode — all 700, so Next crosses the chapter edge (2.72 → 3.01)
    instead of dead-ending. Continuous reading is untouched; this only adds a
    door beside it.
  - **The themes page was deliberately NOT paginated.** It is a table of
    contents — 18 short headings whose job is to be scanned. Paginating it
    would mean clicking Next 14 times to reach theme 15, turning a map into a
    corridor. Chapters 13–17 average 2.4 verses per theme; the overview is the
    point.
  - **Resume, the thing that was actually missing.** The app had no memory of
    position at all — only gitaFavs / gitaFavNotes / gitaTheme existed — so a
    reader crossing 700 verses over weeks returned to the welcome screen with
    no idea where they stopped. Progress is now recorded in `fillModal()`, the
    single choke point every route into a verse passes through, so the mark
    follows the reader through the chapter rather than recording only where
    they entered. The welcome screen offers "Continue from 6.12 →" with the
    topic and a quiet "start over". Suppressed when the reader arrives on a
    shared verse — that verse is what they came for.
  Same hardening as the favourites: a successful `JSON.parse` still has to
  yield the expected shape, and a stale or hand-edited verse id resolves to
  null via `verseLocByN()` rather than stranding the reader. Verified against
  9 corrupt payloads. UI strings 101 → 106 in all three languages.

* **Second pass: DESCRIPTIONS audited too — 3 more errors (owner 2026-09-03).**
  The owner's point: a wrong description is worse than a wrong title, because
  it is a full sentence a reader will trust. So the same neighbour-comparison
  test was run over all 700 verse descriptions and all 222 theme titles AND
  descriptions, not just titles.
  - **1.27 desc** said "Fathers, teachers, brothers, sons and friends" — that
    is **1.26**. This verse is fathers-in-law and well-wishers.
  - **2.31 desc** said "blessed are those to whom such a war comes unsought" —
    that is **2.32**. This verse is "look to your own dharma and do not waver".
  - **18.70 desc** merged **18.69**'s sentence with **18.71**'s, describing
    neither. The verse is about STUDYING the dialogue as a sacrifice of
    knowledge.
  **The theme layer came back clean** — all 27 flagged themes were checked by
  hand against their verses and every one was correct. The abstraction is the
  point of a theme title ("The Cycles of Creation" shares no word with its
  verses and should not).
  **Four structural checks added and made BLOCKING**, each verified by mutation:
  - `adjacent-duplicate` — a title or description identical to its neighbour's,
    which is the signature of copy-paste drift
  - `desc-cites-other-verse` — a description naming a verse number that is not
    its own
  - `missing-language` — any title or description empty in en/ne/hi
  - `possessive-inverted` — the 1.10 class
  Everything else stays advisory (33 findings, all read and judged correct):
  epithets, abstractions and shared vocabulary between adjacent verses produce
  false positives that only a human can dismiss.
  **Running total across both passes: 15 real defects in published text.** All
  15 were introduced by bulk rewrites, and none were catchable by the existing
  suites, which compare Sanskrit to its word-split and English to other
  English. The lesson worth keeping: after any bulk edit of prose, re-verify
  the prose against the SOURCE it describes, not against itself.

* **Titles audited against their verses — 12 factual errors found and fixed
  (owner 2026-09-03).** The owner spotted two by reading; a mechanical audit of
  all 222 themes and 700 verse titles against the Sanskrit and the literal
  translations found ten more. `source/audit_titles.py` now runs on every build.
  **The errors, all introduced by the bulk title rewrites:**
  - **1.10 — possessive inverted.** "Their force is shielded by Bhīṣma", but
    the verse says `asmākam` (OURS) is guarded by Bhīṣma and `eteṣām` (THEIRS)
    by **Bhīma**. Duryodhana is speaking about his own army. The DESCRIPTION
    was right all along — only the later-rewritten title was wrong.
  - **1.08 — wrong name.** Titled "…Kṛpa, Droṇa"; the verse names Aśvatthāmā,
    Vikarṇa and Somadatta's son. Droṇa is addressed in 1.02, not listed here.
  - **1.42 / 1.43 — swapped.** 1.42 is the consequence (hell, fallen ancestors),
    1.43 the cause (eternal duties destroyed). The titles were the wrong way round.
  - **4.26 / 4.27 — swapped.** "The fire of knowledge" belongs to the verse
    about the fire of yoga, not the one about fires of restraint.
  - **4.30, 4.32, 4.33 — each described a NEIGHBOURING verse.** 4.30 is
    breath-into-breath, not "knowledge burns all karma".
  - **8.02 — wrong terms.** Titled "Adhyātma and Karma"; the verse asks about
    **adhiyajña** and how the Lord is known at the hour of death.
  - **18.42/18.43/18.44 — the varṇa run was offset by one.** Each title named
    the varṇa of the NEXT verse: 18.42 lists only the brāhmaṇa's duties,
    18.43 the kṣatriya's, 18.44 the vaiśya's and śūdra's.
  - **18.60 — wrong subject.** "The Lord within" is 18.61; 18.60 is about your
    own nature compelling you.
  **How they were found, and what generalises.** Five mechanical checks, run
  against the Sanskrit (`t`) and the literal (`lits.en`) rather than against
  other English text — which is why the existing suites missed all of this: the
  pāda checker validates Sanskrit against its word-split, and the paraphrase
  checker compares two English strings to EACH OTHER. Nothing had ever compared
  a title to its verse.
  The single most productive check was **neighbour comparison**: score a
  title's content words against its own verse, then against the two verses
  either side. If a neighbour scores decisively higher, the title has drifted.
  That one test surfaced the swaps and the varṇa offset, which no amount of
  reading a title in isolation would reveal.
  **What blocks vs advises.** Only `possessive-inverted` fails a build — it had
  zero false positives across all 700. The other four categories flag
  legitimate paraphrase too (an epithet IS the person: Hṛṣīkeśa is Kṛṣṇa, "the
  son of Subhadrā" is Abhimanyu; "one" is usually a pronoun, not a count), so
  they print as advisories for a human to read. 33 advisories remain, all
  reviewed and judged correct. Tuning the name check to understand epithets cut
  false positives from 38 to 23.
  **Also confirmed sound:** 700 verses contiguous and in order in all 18
  chapters, every part holding exactly one verse, no title merely restating its
  own description, and 2.01's description ("Kṛṣṇa speaks") correct despite the
  speaker-mismatch flag — Sañjaya narrates THAT Kṛṣṇa spoke.

* **All 700 verse titles cleaned (owner 2026-09-02).** Same pass as the theme
  titles, one level down. Two problems:
  - **86 failed the standalone test** — a dangling pronoun ("That I May See
    Them", "Weapons Do Not Cut It") or too terse to mean anything alone
    ("Unbreakable, Unburnable", "The virtues"). Rewritten from the verse's own
    literal translation, not from the old title.
  - **7 were exact duplicates** of another verse's title book-wide. That is a
    real defect, not just untidiness: two drill options could render
    identically with one marked wrong. **Now 0.**
  **Case:** the owner left the choice to me. I picked sentence case to match
  the theme titles — then saw the chapter read with MIXED casing, because only
  90 of 700 were being touched. Mixing is worse than either choice, so all 700
  were converted mechanically (647 changed). The converter protects proper
  nouns, Sanskrit terms and doctrinal capitals — Self, Brahman, Yoga-Māyā,
  Om Tat Sat, every deity and place name — via an explicit keep-list, and
  restores a capital after sentence breaks. 16 hyphenated compounds kept a
  stray inner capital ("Even-Minded", "Self-Controlled") and were lowered by
  hand, except Monkey-Bannered and Yoga-Māyā, which earn theirs.
  **What "a flowing river" actually means here, recorded for future passes:**
  nobody reads 700 titles in sequence. A reader sees ONE in the verse sheet, or
  the 3-9 inside a theme. So the standard is "does each stand alone, and do the
  few within a theme cohere" — the Gita's overall arc is carried by the 222
  THEME titles, which were made deliberately. Chapter 12 now reads end to end
  as one continuous movement.
  Tooling: `source/reverse.py`, sibling of retitle.py. It proves the three
  languages agree on part count AND that every part's verse ref matches across
  them before touching anything, then anchors each edit on the full part tuple
  (title + desc + ref + ref) so a stale patch cannot hit the wrong verse.
  **A mutation-testing trap worth remembering:** two mutations "escaped" the
  new guards, and both times the guard was right — I was mutating `p.title`, a
  legacy field the app no longer renders. The app reads `p.titles.en`. When a
  mutation passes, check you changed the field that is actually used.

* **The theme page had no title (owner 2026-09-02).** `showVerses()` rendered
  the theme's description and its verse grid, but never its NAME — the title
  appeared in the crumb trail and then nowhere on the page, so the reader
  arrived at a description with no subject. It was the only view in the app
  missing a heading; swept all 15 view functions to confirm (favourites uses
  `res-head`, the finish screens `lr-finis`, the drill its progress label, and
  showChapters is a grid of named cards, so crumbs alone are fair there).
  Added in the same shape the learn path already uses: title, range, then the
  description. The range needed its own rule — `.rng` is scoped to
  `.th-flow h3`, so beside a `.view-title` it would have inherited 1.7rem and
  shouted over the theme's name.

* **Word meanings opened on arrival in "meet the verses" (owner 2026-09-02).**
  The grid was rendered WITH the `hidden` attribute and `lrTog()` toggled it
  correctly, so the markup and the JS were both right — but `[hidden]` is only
  `display:none` in the UA stylesheet, and `.lr-words{ display:grid }` is an
  author rule, which wins. The attribute was silently inert.
  Fixed with an explicit `.lr-words[hidden]{ display:none; }`. Now each pāda
  stays closed until tapped, which is what the drill intends — seeing every
  gloss at once is reading, not recall.
  A **generic** guard was added alongside the specific one: it walks every
  element rendered with `[hidden]`, checks whether its class sets a `display`,
  and demands a matching `[hidden]` rule. That catches this class of bug
  anywhere it appears next, not just here. Only `.lr-words` was affected today.

* **The shell no longer inlines its fonts either — 305 KB -> 188 KB, -38%
  (owner 2026-09-02).** chapter.css was de-base64'd on 2026-09-01, but
  index.html still carried BOTH weights inline: **116 KB for 85 KB of font**,
  since base64 inflates binary by 33%. And the 400 weight was **byte-identical**
  (sha256 verified) to noto-deva-regular.woff2 already published beside it for
  the chapter pages — so every visitor downloaded those 40.7 KB twice.
  The original justification was "no second round-trip on first paint". That
  reasoning inverted as the shell grew: nothing renders until the whole
  document arrives, so 116 KB of font in the HTML was DELAYING first paint, not
  protecting it. As files they fetch in parallel, and the app and the 18
  chapter pages now share one cache entry for the regular weight.
  Two things this needed that are easy to miss: the **bold** weight is newly
  published, so it had to be added to the service worker's ASSETS or offline
  would lose it; and `CACHE_VER` now hashes BOTH faces, so swapping either one
  invalidates the cache instead of stranding readers on a stale copy.
  A build-order trap: `_font_face()` runs at line ~3293, before `SITE_DIR`
  exists at 3345 — it writes to `GITA_DIR`, which is the same directory and is
  defined at line 52.
* **Lazy-loading the learn/play code was considered and REJECTED (2026-09-02).**
  It is 51 KB, 17% of the shell — a third of what the font fix returned for
  free — and splitting it would add a file to the upload set, a loader, a race
  if the reader taps Play before it arrives, and new service-worker failure
  modes. Revisit only if the shell passes ~250 KB again.

* **A language switch no longer quits the game (owner 2026-09-02).** Play
  dropped the reader back to its menu mid-question. That was my own earlier
  decision, made on the assumption that a queued question could not survive the
  switch — but only THREE things in a Play question are language-bound: the
  prompt, the note, and the numerals. The verses and pādas are Devanagari in
  every language.
  So the question is rebuilt rather than abandoned. `PL.q` records the verse id
  and the option ORDER; `plNext(keep)` regenerates the identical question with
  its strings re-resolved. Verified across all three modes: same verse, same
  four options, same order, and the streak counter survives. If no question is
  open it still falls back to the menu.
  **Guard weakness, again:** asserting `"PL.q = {n:s.n, ord:" in idx` passed
  with mode 1 gutted, because modes 2 and 3 still matched. It now requires the
  count to be exactly 3. That is the fourth time a substring check has been too
  loose — when a pattern repeats per branch, assert the COUNT.

* **A retry re-shuffles its options (owner 2026-09-02).** The owner asked
  whether the red clears when the question comes back. It does — `lrPaint()`
  rebuilds the buttons with `innerHTML`, so no `.right`/`.wrong` class survives.
  But tracing it exposed a real weakness: options were shuffled ONCE at build
  time, so a requeued question returned with the four verses in the **same
  positions**, and the reader already knew which one was wrong. In Play, where
  the same question comes straight back, that made the retry a 1-in-3 guess
  rather than recall.
  A re-shown question now re-shuffles. Shuffling the ARRAY rather than just the
  render is what keeps it correct: `lrPick()` reads `it.opts[i].ok`, and `.ok`
  travels with the option object, so the answer cannot desync from its index.
  Verified over 20,000 simulated retries: **0 wrong picks ever flagged correct**,
  and the answer lands in the same slot 25.4% of the time — chance, as it
  should be.

* **The verdict is shown, not narrated (owner 2026-09-02).** Asked to mark a
  wrong choice in red with a cross instead of printing "Not quite." underneath
  — a better idea than the wording change it replaced, because a tick and a
  cross say it faster than prose and in every language at once.
  - The chosen option now carries a **✓ in teal** or a **✕ in red** in its
    right edge, with a matching wash. New palette tokens `--danger-soft` and
    `--on-danger` in both themes.
  - **The dimming is gone.** `opacity:.75` on a wrong answer made the mistake
    harder to read, which is backwards: the mistake is the thing worth studying.
  - The feedback line drops the verdict and keeps only what the reader cannot
    see — the correct verse and its meaning.
  - The button now says what pressing it DOES: **"Select again"** /
    फेरि चयन गर्नुहोस् / फिर चयन करें. Verified against the queue: in Play the
    same question genuinely returns, and in a multi-question drill the missed
    item is requeued and comes back later — the same promise either way.
    `learn_continue` was deleted rather than left orphaned.
  Contrast checked per theme: white on the light red is 5.44:1, but only
  **3.14:1** on the dark theme's lighter red, so `--on-danger` supplies dark ink
  there instead (5.90:1).
  **Three attempts to get the guard right**, worth recording: a bare
  `"--danger-soft" in idx` passed with the fill deleted (the token also appears
  in the palette); scoping to the rule then matched the SHARED
  `.lr-opt.right, .lr-opt.wrong{...}` declaration instead of the standalone one.
  When several rules share a selector fragment, take the specific one.

* **Verdict wording in ne/hi (owner 2026-09-02).** The drill answered भयो। /
  हुआ। ("it happened") and पुगेन। / पूरा नहीं। ("not enough") — grammatical, but
  translated-sounding. Now the plain words a speaker actually uses: **ठीक!** for
  right, **गलत।** (ne) / **ग़लत।** (hi) for wrong. Hindi takes the nuqta, Nepali
  does not.
  These live in `lrPick()`, which Play and the Learn drill share, so both speak
  the same way — right, since a verdict should not change vocabulary depending
  on which screen you are on. The ORDERING drills keep their own phrasing
  (यही हो धागो। "that's the thread", अहँ — अब आउने हो "not yet — next comes"),
  because reordering is not a right/wrong verdict but a running correction.

* **Play's subtitle rewritten (owner 2026-09-02).** "Nothing is scored,
  nothing is saved" was explaining an absence — a designer's note, not an
  invitation. Now: *"Three ways to test yourself. Play as long as you like.
  Enjoy learning the Gītā 🙏"* in all three languages.
  Worth recording since it breaks a pattern: this 🙏 is the **only emoji in the
  app**. Every other symbol is typographic (← ↑ ✕ — " "). The owner chose it
  deliberately over ॐ or plain words. If more are ever added, they should be as
  sparing — one warm mark at the end of an invitation reads as human; emoji
  scattered through a scripture app would not.

* **The house edge slimmed to 2px (owner 2026-09-02: "not gaudy, Apple
  style").** All 17 edges went 3px → 2px. At 3 it reads as a highlighter
  stripe and the page starts to look like a dashboard; at 2 it registers as
  craft. The tone is unchanged — width does not affect contrast, so the edge
  still measures 2.47:1 (light) and 7.03:1 (dark) against --paper. The
  restraint IS the design.
  The health check was rewritten width-agnostic: it now asserts the edge exists
  across the app **and stays ≤2px**, so a future tweak cannot quietly fatten it
  back into a stripe. Two of my own guards had to be fixed here — one hardcoded
  3px, the other banned --saffron-soft anywhere rather than only on the leading
  edge, where it is the one place it is wrong.

* **A house idiom, so every screen carries the brand (owner 2026-09-02:
  "every page must represent our colours").** Audited all 258 painting rules:
  141 used a brand colour, **117 did not** — and the app had **zero gradients
  and one accent bar** in its entire stylesheet. Every card was a --paper box
  with a grey outline, so the saffron and teal accents INSIDE them had nothing
  to belong to. That, not the Play screen alone, was the blandness.
  The idiom: **a 3px brand edge on a card's leading side.** Saffron = something
  you act on (chapter cards, themes, path steps, options, mode cards, quarter
  chips). Teal = something already yours (search results, placed chips, the
  question frame, the completion seal). Cheap, quiet, reads in both themes, and
  never shouts over the scripture.
  Applied to all 14 surfaces: .card .theme .res-card .mode-box .welcome .w-day
  .lr-step .lr-chip .lr-q .lr-word .lr-opt .lr-qbox .lr-chip2 .lr-slot .pl-mode
  .lr-finis — the last of which now sits on a teal wash, since finishing a
  theme is the one moment of arrival in the app.
  **A measurement that changed the design:** the edge began as --saffron-soft,
  which is **1.25:1 on --paper** — an edge nobody can see is not an edge. The
  resting state is the full --saffron (2.47:1 light, 7.03:1 dark) and hover
  deepens to --saffron-dark rather than introducing colour. Verified all new
  hovers are still cancelled in the touch block.

* **The question screen was flat white (owner: "all black and white, too
  bland", 2026-09-01).** Three causes, all real:
  - **Options were --paper on a --paper card**, so every boundary vanished.
    The question card is --cream now and the options keep --paper. That is only
    a **1.06:1** step, nowhere near enough on its own, so the options also gain
    a shadow — the lift, not the fill, is what separates them.
  - **The prompt read as more prose.** It now sits in a saffron-soft band
    behind a 3px saffron rule: this is the question, everything else is answer.
  - **A 0%-forever progress bar.** Play's queue holds ONE item, so the bar sat
    empty and the counter read "1 / 1". A single-item queue with a caller
    back-target (i.e. Play) now shows the run label alone.
  Also: the verse number under an option is saffron like every other number in
  the app, and a wrong answer uses **--danger** rather than a darker saffron —
  the verdict has to be unmistakable, not a 1px hue shift.
  **Two things I got wrong on the way, worth recording.** I "fixed" the dark
  correct-answer border to --teal-mid on a contrast calculation that used the
  LIGHT palette's hex; the dark theme already redefines --teal to #8FC1CE,
  which measures 8.77:1. Reverted. And my own earlier guard demanded
  .lr-qbox match .card on --paper, which the fix deliberately breaks — the
  guard is now scoped to .lr-step, which genuinely is a card. Check what a
  variable resolves to IN THE THEME you are reasoning about.

* **Hover stuck on touch across the whole learn path and Play (owner
  2026-09-01).** On a phone a `:hover` state persists after the tap, so the last
  card or chip you touched keeps looking selected — the owner saw phantom
  selections in Play. The app already solves this with an
  `@media (hover:none)` block that cancels each hover and answers it with an
  `:active` state, **but that block listed only the components that existed
  when it was written.** Every learn-path and Play class was added later and
  was never included. All 11 are now cancelled, with 7 given `:active`
  feedback so a tap still responds.
  A selected scope pill keeps its saffron under `:hover` inside that block —
  it is STATE, not hover, and must not be flattened with the rest.
  **A lesson about the check, not the code:** the first version of the guard
  asked whether the class NAME appeared in the touch block. It passed with the
  rule deleted, because the name still occurred nearby. It now matches the full
  hover SELECTOR (`.lr-opt:hover`). Second time this exact weakness has slipped
  through — assert the statement, never the identifier.
* **Play chrome aligned with the app (owner 2026-09-01).** `.pl-mode` now
  matches `.card` on background, radius, padding and shadow; `.pl-sel` matches
  `.tool-btn` geometry and its teal; the mode title weight matches the app's
  card headings. Play already used `view-title` / `view-sub`, so the text
  hierarchy was correct.

* **Play's drill footer sent the reader to chapter 1 (owner 2026-09-01).**
  `lrRun` is shared by the learn path and Play, and its footer was hardcoded to
  `showRead(LQci,'full')` — "back to chapter". Play passes `ci=0`, so from a
  game spanning the whole Gītā the only exit dropped you into chapter 1.
  `lrRun` now takes an optional back target: Play supplies
  `{fn:'showPlay()', label:'play_title'}`, and the three learn-path call sites
  pass nothing and keep "back to chapter", which is right for them. Verified
  that only one of the four call sites supplies a target.

* **Multiple-choice options are whole verses, not first pādas (owner
  2026-09-01).** Both the Play "name the verse" mode and the theme drill's
  "which verse says this?" offered the opening line only. A first pāda is not a
  verse, and choosing between four fragments is a shallower task than choosing
  between four ślokas. Both now show the complete verse (66-134 characters,
  average 86), and the option lays out stacked — verse full width, its number
  underneath — instead of the two competing for one line.
  **A welcome consequence:** full verses are unique book-wide (verified across
  all 700), whereas four PAIRS share a first pāda — 3.35/18.47, 6.15/6.28,
  9.34/18.65, 16.07/18.30. The identical-option guard that case required is now
  redundant, though it stays in place and is still asserted. Re-verified over
  5,000 draws: 0 duplicate options, 0 shortages.

* **Play added — a front door onto the drill engine (owner 2026-09-01).**
  A button in the tool row beside Random and Favorites, reachable from any
  screen including the welcome page. Three modes, a scope chooser (whole Gītā
  or one chapter), and an endless one-question-at-a-time loop.
  **Deliberately unscored and unsaved.** Learn by heart is the path — gated,
  with progress; Play is the shuffle you drop into. If Play began tracking
  progress the two features would blur and neither would be clear.
  It reuses `lrRun`/`lrPaint`/`lrPick`/`lrChip` wholesale, so it is ~150 lines
  rather than a second engine, and it inherits the requeue-on-miss behaviour
  already mutation-tested.
  Two data findings shaped the modes, both verified over 4,000 simulated draws
  (0 duplicate options, 0 shortages):
  - **Mode 1 (number → verse).** Options are first pādas, and **four verse
    PAIRS in the Gītā open identically** — 3.35/18.47, 6.15/6.28, 9.34/18.65,
    16.07/18.30. Distractors are filtered by opening line, or two options would
    render the same with one marked wrong. Same fault already fixed twice in
    the theme drills.
  - **Mode 2 (verse → number).** Distractors are **near misses from the same
    chapter**, sorted by distance from the true verse. Random numbers from
    elsewhere are given away by chapter recognition alone and test nothing;
    verified all 4,000 draws drew same-chapter distractors.
    Noted honestly: this mode tests indexing rather than meaning. It earns its
    place because citing "as it says in 2.47" is a real skill, but it is a
    different kind of knowing from the other two.
  - **Mode 3** reuses the pāda-reorder drill; all 700 verses have exactly four
    distinct quarters, so it is always fair.
  A language switch mid-question returns to the Play menu, since the queued
  question was built from the old language's strings; scope and mode are
  remembered. 17 new UI strings in all three languages (**165 total**).

* **Free practice never shuffled (owner 2026-09-01).** The pādas were rendered
  straight from `FP.order` — their natural sequence — so the reader was asked
  to put four already-ordered lines in order. The mode did nothing. The queue
  drill shuffles at render (`lrShuffle(it.chips)`); free practice simply never
  got the same treatment.
  Fixed by dealing a display order **once per verse** and holding it in
  `FP.deal`. Shuffling inside `lrFreePaint()` would have looked correct in a
  static test but moved every chip on every tap, since the paint re-runs after
  each answer. The tap check still validates against the TRUE index, not the
  displayed position. A guard rejects the identity permutation — a 1-in-24
  chance of dealing 0,1,2,3 would look exactly like the original bug and send
  us chasing it again. Verified over 500 draws: **0 natural-order deals, 23 of
  24 possible arrangements seen**, and neither the paint nor the tap handler
  reshuffles.

* **Cloze cue REMOVED outright; stale drill feedback fixed (owner
  2026-09-01).** Two reports, both correct.
  - **The cue was still leaking.** Suppressing it "when the answer is literally
    in the line" caught only half the cases. `अकुर्वत` is not literally inside
    `किमकुर्वत सञ्जय`, but **कुर्वत — six of its seven characters — is**, so
    the guard passed and the answer sat on screen. Measured properly:
    **6,069 of 6,394 questions leak** either literally (3,035) or all but a
    letter (3,034). Only **325** would keep a cue that genuinely helps.
    A hint that helps 5% and gives the game away 95% of the time is not worth
    saving, so the recited line is gone from the cloze entirely. The
    surrounding words of the split are the context — supplying the missing word
    of a pāda you know IS the recall being tested. (`lr-cue` survives only in
    free practice, where the IAST appears AFTER you finish: a reward, not a
    hint.)
    **The lesson, third time in this feature:** each fix here has created the
    next bug. The recited line was added to solve sandhi, then leaked; the
    literal-presence guard was added to solve the leak, then leaked again on
    near-matches. Measure the fix against all 6,394 cases before shipping it,
    not against the one example that prompted it.
  - **A correction never cleared.** `lrChip()` wrote "not there yet — next
    comes X" on a wrong tap but never cleared it on a right one, so the
    message stayed for the rest of the question and read as though the new,
    correct answer were also wrong. It now clears the moment the reader is
    right. Free practice was already safe — `lrFreeTap()` re-renders the panel.

* **Cloze cue no longer gives away the answer (owner 2026-09-01).** The
  recited pāda is shown under the word-split as a cue. That is right when
  sandhi transforms the word — पश्य + एताम् becomes पश्यैतां, so the line helps
  without telling. But in **47.5% of pādas (3,035 of 6,394) the dictionary form
  survives unchanged**: the owner was asked which word was missing from
  `? + पाण्डवाः + च + एव` with `मामकाः पाण्डवाश्चैव` printed directly beneath.
  The cue is now rendered **only when the answer is not literally present** in
  the line. 3,359 questions keep their cue, 3,035 lose it, **0 leaks remain**.
  Worth noting the shape of this bug: the cue was added to FIX the earlier
  sandhi problem, and in fixing it created the opposite one. The general
  lesson, now recorded: a hint that is correct for the hard cases can be a
  giveaway in the easy ones — check both halves of the split.

* **Every verse drilled; free practice added (owner 2026-09-01).**
  - **Coverage.** The pāda-order drill ran on ONE random verse per theme, so
    **478 of the 700 verses were never practised that way**. It now runs on
    every verse of the theme. Drill items **1,816 → 2,294**. A 3-verse theme
    now asks 10 questions (3 meaning→verse, 3 cloze, 3 pāda-order, 1
    verse-order) instead of 7.
  - **Free practice.** After a theme is held, the reader may keep going for as
    long as they like: a random verse from that theme with its four pādas
    shuffled, reorder it, then pull another. Deliberately **outside the queue
    engine** — nothing scored, nothing required, no progress written. Practice,
    not examination; a wrong tap just shakes and names the next pāda.
    The shuffle avoids handing back the same verse twice running (guarded, and
    verified over 300 draws: even distribution, zero immediate repeats). A
    single-verse theme cannot hang — the guard caps at 12 attempts.
  - **"Back to the path" is fully retired.** The theme completion screen said
    it; it now says **"back to chapter"** like every other exit in the learn
    path. The i18n key `learn_back_path` was deleted rather than left orphaned.
  New keys: `learn_free`, `learn_free_d`, `learn_shuffle`, `learn_free_go`,
  `learn_done_free` in all three languages; one retired. **148 total.**

* **Verse-order drill fixed; pāda-order drill added (owner 2026-09-01).**
  - **The bug.** Verse-order chips read `1.1 · King Dhṛtarāṣṭra asks…`. With the
    number printed on every chip the task is sorting integers, not recalling
    scripture — the owner caught it at ch1.t1 and was right that it "is not a
    drill". The chip is now the paraphrase alone. Checked first that this is
    fair: all 700 paraphrases are unique at 64 characters, so nothing becomes
    ambiguous by dropping the number.
  - **The addition.** Reorder the four pādas of one verse, within its theme —
    the owner's suggestion, and the way a śloka is actually committed to
    memory. Verified the data supports it everywhere: **every one of the 700
    verses has exactly four quarters, and no verse has two identical ones**, so
    the drill is always answerable and never ambiguous. One verse per theme,
    chosen at random, so a long theme does not become a grind of near-identical
    questions. **222 quarter drills, one per theme; total items 1,594 → 1,816.**
  - Devanagari chips needed their own face: the Latin default renders conjuncts
    too small to compare. `.lr-chip2.dv` and `.lr-slot.dv` carry the Sanskrit
    font, and `lrChip()` propagates the class when a chip is placed — otherwise
    a pāda dropped back to the Latin face the moment you answered.
  New key `learn_qorder` in all three languages (144 total).

* **Learn-path footers and chrome aligned with the app (owner 2026-09-01).**
  - **Back-links.** Inside the learn path the footer said "back to path" and
    led to the learn home — a half-step the reader never asked for, and it
    disagreed with the learn home's own footer, which said "back to chapters".
    All four footers now read **"back to chapter"** and call
    `showRead(ci,'full')`, which is exactly what a chapter card opens, so the
    mode-box stays visible and the three ways remain one click away. The one
    surviving "back to the path" is on the completion screen, where it is
    correct. New key `back_chapter_one` in all three languages (143 total).
  - **Chrome.** The drill had quietly grown its own design language: buttons at
    .9rem/11px 20px against the app's .85rem/8px 16px, panels on --cream where
    every card in the app is --paper with a 1px shadow, and hovers that changed
    only the border where the app also warms the background. `.lr-cta` and
    `.lr-ghost` now mirror `.tool-btn` and `.tool-btn.primary` property for
    property; `.lr-step`, `.lr-qbox` and `.lr-q` mirror `.card`. Zero --cream
    left in the learn CSS.
  All of it asserted in check_site_health.py (437 checks) and mutation-tested.
  **Process note, fourth occurrence — and the rule finally worked.** Re-injecting
  learn_block by slicing between sentinels duplicated the shell AGAIN
  (`VERSE_TEXT has already been declared`). Recovered from `.backup/`, then
  applied the identical edits **directly to the injected copy** in
  build_gita.py, which built clean first time. Do not re-inject. Edit in place.

* **Language switch mid-drill now returns to the same theme (owner
  2026-09-01).** The owner reported that changing language during a drill threw
  them onto the theme page. Reproduced exactly: with the guard removed,
  `setLang()` with `state.view='learn'` and `state.theme=3` falls through to
  the generic restore and calls **`showVerses(11,3)`** — the theme page. The
  guard added earlier already prevented that, so what the owner hit was an
  older zip built before the fix; the live site does not have the learn path
  at all yet.
  **Improved anyway.** Returning to the chapter's path home was still a long
  walk back. `state.lrAt` now records which sub-view is active
  (`{kind:'theme',ti}` or `{kind:'story',step}`) and `lrRelang()` re-enters
  there. The half-answered QUESTION is genuinely unrecoverable — its options
  were generated from the old language's strings — but the theme is not, so it
  restarts that instead of the whole chapter.
  Verified by executing the real `setLang()` against each learn sub-state:
  drilling a theme -> `lrTheme(ci,ti,0)`, mid-story -> `lrStory(ci,0)`, path
  home -> `showLearn(ci)`, and a normal themes page still -> `showThemes(ci)`.
  **Process note, third occurrence:** re-injecting learn_block by restoring the
  `.before-learn` snapshot destroyed every later edit (mūla removal, retitles,
  saffron ranges, wip note) because that snapshot predates them. Recovered from
  `.backup/build_gita.py`, which is written fresh before each change. The rule
  is now: edit the INJECTED copy in build_gita.py directly, and only ever
  re-inject from a snapshot taken in the same session.

* **Theme verse-ranges made saffron; work-in-progress note added
  (owner 2026-09-01).**
  - The range beside a theme title (1.1-1.3) is a verse NUMBER and must read as
    one. All four render sites had it at --ink-soft, so it sank into the
    description text while every other number in the app is saffron. Now
    saffron at weight 600 in: the Study-view theme cards, the learn-path story
    thread, and both chapter.css rules (`ol.themes .rng`, `h2.th .rng`).
    Weight 600 because at .78rem colour alone is thin — --saffron-dark measures
    only 3.28:1 on white, under the AA floor for small text, so the extra
    weight is carrying real load, not decoration.
  - **A trap worth remembering:** `build_gita.py` holds an INJECTED COPY of the
    learn_block CSS. Editing `source/learn_block.py` alone changed nothing in
    the build — the fix had to go into the injected copy too. Anything touching
    learn CSS must check both, or re-inject from the module.
  - New `wip` string in all three languages, shown under the welcome footer:
    "A work in progress — still building, still fixing, and dedicated to making
    the Gītā easier to study." Set as the quietest thing on the screen
    (--ink-soft, italic, hairline rule above) so it reads as an aside from the
    author rather than a warning about the text. UI strings 141 -> 142.

* **The 9v, remaining 8v and all twelve 6v themes examined; five split
  (owner 2026-09-01).** Gita 216 -> 222. Largest theme is now 8 verses.
  - **ch4 [4.34-4.42], the largest in the Gita, -> 3.** 4.34-35 (go to the wise
    and ask) | 4.36-41 (knowledge burns all actions to ashes) | **4.42** — the
    chapter's closing command, ending `yogam ātiṣṭhottiṣṭha bhārata`, **two
    imperatives** back to back.
  - **ch2 [2.54-2.61] -> 2. A correction of my own earlier call:** last pass I
    left this whole, claiming the `prajñā pratiṣṭhitā` refrain ran 2.55-58.
    Checking the Sanskrit, the refrain sits at **2.57, 2.58 AND 2.61** — it does
    not end at 58, so that argument was wrong. 2.59 raises a genuinely new
    problem (`rasa`, the lingering taste) which 2.60-61 answer. Split there.
  - **ch8 [8.23-8.28] -> 2.** 8.27 turns from the two paths to Arjuna himself:
    `yogayukto bhavārjuna`.
  - **ch11 [11.35-11.40] -> 2.** 11.35 is Sañjaya narrating; 11.36 opens
    Arjuna's hymn. Speaker change.
  - **ch18 [18.23-18.28] -> 2.** Three kinds of *action* and three kinds of
    *agent* — the same twin-triad shape already split at 18.29-35.
  **Ten left whole**, and the reasons are worth keeping because they are the
  standing criteria for any future pass:
  - **Grammatical (hard no):** ch5 [5.07-5.12] — 5.08-09 are ONE Sanskrit
    sentence; ch6 [6.10-6.15] — 6.11-14 are one; ch6 [6.18-6.23] — 6.20-23 are
    one. Cutting inside a single period is wrong at any length.
  - **Unbroken enumeration:** ch10 [10.21-26] and [10.27-34], ch4 [4.25-4.30].
    No turn, no imperative, no seal — any cut would be arbitrary.
  - **Single taxonomy:** ch18 [18.07-12] three abandonments, [18.13-18] five
    causes. The list IS the unit.
  - **One continuous argument:** ch6 [6.27-6.32], ch11 [11.09-11.14].
  Distribution of themes over 4 verses is now 5v:21, 6v:10, 7v:3, 8v:1.

* **The six 7-verse themes examined; three split (owner 2026-09-01).**
  Gita 213 -> 216.
  - **ch2 [2.47-2.53] -> 2.** The most famous passage in the Gita carried two
    different teachings. 2.47-48 is karma-yoga (act without claiming the fruit,
    `samatvaṃ yoga ucyate`); **2.49 pivots to buddhi-yoga** — "action is far
    inferior to the yoga of discernment, take refuge in the intellect" — and
    2.50-53 all develop buddhi. Different faculty, different teaching.
  - **ch2 [2.62-2.68] -> 2.** 2.62-63 is the ladder of ruin (brooding ->
    attachment -> desire -> anger -> delusion -> destruction). **2.64 opens
    with `tu`** — "BUT one who moves among objects with senses mastered" — an
    explicit reversal into the remedy.
  - **ch18 [18.29-18.35] -> 2.** Two complete triads that had been fused:
    18.30-32 are the three kinds of *buddhi*, 18.33-35 the three kinds of
    *dhṛti*. The old title ("Intellect and resolve, by the guṇas") admitted it
    was naming two things.
  **Three left whole, deliberately:**
  - **ch6 [6.37-6.43]** — Arjuna asks (37-39), Kṛṣṇa answers (40-43). Same
    shape as ch12.t1 and ch5.t1, which were also left whole: splitting a
    question from its answer breaks the dialogue.
  - **ch7 [7.24-7.30]** — one continuous argument (I am veiled -> the deluded
    do not know me -> but the pure-hearted do). The `tu` at 7.28 completes the
    same thought rather than starting a new subject.
  - **ch18 [18.49-18.55]** — **18.51-53 are grammatically ONE Sanskrit
    sentence spanning three verses** (visible as the run-on dashes in the
    translation). Cutting inside it would break a single period. Hard no.
  After: 700 verses in exactly one theme each, 0 themes without drill items,
  0 duplicate titles within a chapter in any of the three languages.
  Distribution of themes over 4 verses is now 5v:19, 6v:12, 7v:3, 8v:2, 9v:1.

* **The five 8-verse themes examined; three split (owner 2026-09-01).**
  Gita 207 -> 213. Each cut is a seam the text marks itself:
  - **ch2 [2.39-2.46] -> 5 themes**, to the owner's grouping: 2.39-40 (now hear
    the wisdom of yoga) | 2.41 (one-pointed or endlessly branching) | 2.42-44
    (the flowery words of the Veda-lovers) | **2.45** (rise above the three
    guṇas — `nistraiguṇyo bhavārjuna`, an imperative turned back on Arjuna) |
    **2.46** (a well is little use in a flood — the image that closes it).
  - **ch10 [10.35-10.42] -> 2 themes.** 10.40 explicitly halts the enumeration
    ("there is **no end** to my glories... this is but a summary") and 10.42
    seals it ("I support this whole world with **one fragment**").
  - **ch18 [18.05-18.12] -> 2 themes.** 18.05-06 are the ruling, closing with
    "this is my certain and best conviction"; 18.07 opens a formal taxonomy
    (tāmasa / rājasa / sāttvika). Ruling, then classification.
  **Two left whole, deliberately:**
  - **ch2 [2.54-2.61]** — four consecutive verses end with the same refrain,
    `prajñā pratiṣṭhitā`. The refrain IS the structure; cutting mid-litany
    would destroy the thing that makes it memorable.
  - **ch10 [10.27-10.34]** — eight verses of unbroken enumeration with no turn,
    no imperative, no seal. Any cut would be arbitrary.
  Caught by the guards during this pass: the Hindi ch18 retitle would have
  produced two themes named 'त्याग के तीन प्रकार' in one chapter — the
  duplicate-title check refused the write. Fixed by position.
  After: 700 verses in exactly one theme each, 0 themes without drill items,
  0 identical titles within a chapter in any of the three languages.

* **Thematic re-audit of all 700 verses (owner 2026-09-01).** Swept every one
  of the 204 themes for hidden beats using the signals that marked 12.8 and
  12.20: a speaker change inside a theme, an imperative addressed to Arjuna at
  a theme tail, themes of 6+ verses, and a chapter's closing verse buried in a
  multi-verse theme. **Most themes were already right** — 6 genuine candidates
  out of 204, and the owner accepted 2 of them. The rest of the signal hits
  were noise: the imperative regex fires on vocatives (bhārata, kaunteya) in
  ordinary sentences, and most speaker changes are legitimate question/answer
  pairs that belong together (ch2.t16, ch5.t1, ch12.t1, ch17.t1). Splitting
  those would fragment the story rather than clarify it.
  **Applied, to the owner's exact specification — Gita 204 -> 207:**
  - **ch18 end, 7 verses -> 3 themes.** It carried three speakers and three
    movements welded into one: Kṛṣṇa's final question + Arjuna's answer
    (18.72-73), Sañjaya's testimony (18.74-77), and the benediction (18.78).
    18.73 — "my delusion is destroyed... I will do your word" — is the verse
    the whole Gītā exists to produce, and it was buried mid-theme.
  - **ch9 end, 3 verses -> 2 themes.** 9.34 (manmanā bhava madbhakto) stands
    alone: it is the chapter's closing instruction in four verbs, and Kṛṣṇa
    repeats three of its four pādas verbatim at 18.65 as his final word.
    Verified the two verses share their opening line.
  - **ch11.49-51 left unchanged** at the owner's instruction, though it shows
    the same three-voice pattern.
  **A caution recorded for future passes:** chapter 12 now carries 8 themes for
  20 verses. Split freely enough and the theme layer stops being a story and
  becomes a second verse index. The value is in FEW, well-marked beats — the
  test is whether the titles still read as a narrative chain when strung
  together, not whether every notable verse has its own heading.
  After the splits: 700 verses still in exactly one theme each, 0 themes
  generating no drill items, 0 identical titles within a chapter.

* **12.20 given its own theme (owner 2026-09-01).** Chapter 12 now has 8
  themes, the Gita 204. Like 12.8 this is a seam the text itself marks, and
  three signals agree:
  - **`yathoktam`** — "as it has been declared" — points BACK over the whole
    chapter, so the verse is a summation, not another item in the portrait.
  - **`atīva me priyāḥ`** — "EXCEEDINGLY dear". Every earlier verse of the
    portrait ends `sa me priyaḥ`, plain. Only 12.20 takes the superlative.
  - It is the **last verse of the chapter**, and it closes it.
  Buried as the tail of "Equal in honour and dishonour" it read as one more
  quality among many. It is the seal: "Follow this immortal dharma and be
  dearest to me."
  Count locks updated 203 -> 204 in run_gita_app.js, PROJECT.md, README.md.
  Verified after the split: 700 verses still fall in exactly one theme each,
  0 themes generate no drill items, 0 identical titles within any chapter.
  Chapter 12 now reads as a complete arc — question, the harder path, the
  promise, **the direct command**, the concessions, the portrait, the
  equanimity, **the seal**.

* **All 203 theme titles rewritten to stand alone (owner 2026-09-01).** The
  titles were labels for someone already looking at the verses; the learning
  path needs them to carry the chapter's story ALONE, in sequence. **90 of 202
  failed the standalone test; now 1** (a false positive of the heuristic —
  "Arjuna's limbs fail him" is a complete sentence).
  Rules: no dangling pronoun ("I Swiftly Deliver Them" -> "I swiftly deliver my
  devotees"), finish the clause ("If You Cannot" -> "If you cannot fix your
  mind on me"), name the actor ("The Question" -> "Arjuna asks: manifest or
  unmanifest?"), sentence case (these are beats in a chain, not headings),
  <= 52 chars so they still fit a card and can still be memorised. Longest is
  now 48; average 5.6 words. All three languages moved together — 0 gaps.
  **A drill-specific constraint discovered while doing it:** the "what comes
  next" question shows four titles side by side, so near-identical titles in
  one chapter blur into each other. Chapter 18 enumerates many triads and
  initially produced "Knowledge, action and agent are threefold" beside
  "Action and agent, each threefold". Retitled to name the SUBJECT rather than
  repeat "threefold". Five near-pairs remain and are deliberate — they are
  question/answer or problem/solution beats (ch8 "Arjuna asks eight questions"
  / "Kṛṣṇa answers the eight questions"), which is exactly how the story runs.
  Zero identical titles within any chapter.
* **12.8 given its own theme (owner 2026-09-01).** Chapter 12 now has 7 themes,
  the Gita 203. The owner judged the verse too valuable to sit as the tail of
  "I swiftly deliver my devotees" — and the grammar agrees: 12.6-7 are third
  person and descriptive ("those who... for them"), while **12.8 switches to
  the imperative, spoken directly to Arjuna** (mayy eva mana ādhatsva — "place
  your mind in me"). 12.9 then answers it ("if you CANNOT"), so 12.8 is the
  hinge of the chapter: the direct instruction, and everything after it is a
  concession to those who cannot follow it. New theme: "Give me your mind and
  your intellect". Count locks updated: 202 -> 203 themes in run_gita_app.js,
  PROJECT.md and README.md.
  Tooling: `source/retitle.py`. It refuses to run unless the three languages
  agree on theme count, scopes the search to the chapter's own block (titles
  recur across chapters), and anchors on **4-space indentation** so a theme is
  never confused with a part that shares its title — several do
  ("Behold These Kurus", "The Lord's Rebuke", "Bhīṣma's Lion-roar"). Titles
  only; descriptions, ranges and translations untouched. All editable
  afterwards in editor.html -> "Themes & parts".

* **Learn-by-heart audit #2 (2026-09-01) — three more defects, all silent.**
  Asked to re-examine the whole feature. The story drill and the verse-ordering
  drill came back clean (0 duplicate theme titles within a chapter, 0 duplicate
  ordering chips, single-verse themes correctly skip the ordering question).
  Three real faults in the multiple-choice options, measured over 3,000
  simulated questions:
  1. **Duplicate options (0.7%).** Distractors were filtered against the ANSWER
     but never against EACH OTHER, so the same word could render twice —
     e.g. योगी occurs 12× in chapter 6's pool, उवाच 9× in chapter 2's.
  2. **Answer leaked (2.4%).** A distractor already visible in the word-split
     is eliminable at a glance, so the question silently got easier.
  3. **Switching language mid-drill destroyed the drill.** `setLang()` had no
     'learn' branch, so it fell through to the generic restore: with
     state.theme set that lands on `showVerses()` and the reader's question
     just disappears. Now re-enters at the path's home — the only safe rebuild,
     since a half-answered question's options were built from the old
     language's strings. Progress is already saved, so nothing is lost.
  After the fix: **0 duplicates, 0 leaks, 0 questions with fewer than 4 options
  over 5,000 simulations.**
  **A lesson about the tests themselves:** the first version of these guards
  asserted `"shownForms[x[0]]" in idx` — and mutation testing showed it PASSED
  with the guard deleted, because the identifier still occurred on neighbouring
  lines. Assert the whole statement (`if(shownForms[x[0]]) return;`), never a
  bare identifier. Two of three mutations escaped until this was fixed.
* **Theme titles — pass 1 of 18 chapters done (owner 2026-09-01).** The titles
  were written as labels for a reader already looking at the verses; the
  learning path needs them to carry the chapter's story ALONE, in sequence.
  Chapter 12 read "Question / Unmanifest Path / I Swiftly Deliver Them / If You
  Cannot / ..." — deliver whom? if I cannot what? Rewritten to stand alone:
  "Arjuna asks: manifest or unmanifest? / The unmanifest path is harder /
  I swiftly deliver my devotees / If you cannot fix your mind on me / The
  devotee who is dear to me / Equal in honour and dishonour."
  Rules: no dangling pronoun, finish the clause, name the actor, sentence case
  (these are beats in a chain, not headings), <= 52 chars so they still fit a
  card and can still be memorised. **90 of the remaining 196 titles still fail
  the standalone test** — chapters 1, 4, 11, 13, 17 and 18 are the worst.
  Tooling: `source/retitle.py` — refuses to run unless the three languages
  agree on theme count, and replaces a title only when the old value matches
  exactly once inside that chapter's block, so a stale patch cannot overwrite
  the wrong theme. Titles only; descriptions, ranges and translations untouched.
  All of it is editable afterwards in `editor.html` -> "Themes & parts", which
  validates and rolls back a bad save.

* **Cloze drill rewritten — it was wrong for half the Gītā (owner found it,
  2026-09-01).** The owner was drilled on 1.3 pāda 1 and reported: nothing was
  missing from the line, the options made no sense, and clicking one was
  accepted as correct. All true, and worse than it looked.
  **Cause:** the cloze blanked the chosen word out of the RECITED line with
  `.replace()`. Sanskrit sandhi means the dictionary form usually is NOT there
  literally — पश्य + एताम् fuses to **पश्यैतां**, महतीम् is written **महतीं**,
  उभयोः surfaces inside **सेनयोरुभयोर्**. The replace found nothing, the code
  fell back to the untouched line, and the question rendered with nothing
  blanked. Measured: **3,378 of 6,456 cloze words (52.3%) were unanswerable**,
  and every one of them failed SILENTLY — no error, no throw, so no test saw it.
  **Fix:** blank a word from the **authored word-split**, which is data and
  always correct, and show the recited line underneath as the cue. The reader
  now sees `पश्य + [?] + पाण्डु + पुत्राणाम्` above `पश्यैतां पाण्डुपुत्राणाम्` —
  a real question with one right answer, and it teaches the sandhi as a bonus.
  **0 unanswerable of 6,394.**
  **A second bug found while checking:** options are rendered as the verse's
  first pāda, and **6.15 / 6.28 open with the identical line**
  (युञ्जन्नेवं सदात्मानं) — so two visually identical choices could appear with
  one marked wrong. Distractors are now filtered by first pāda, and cloze
  distractors must differ from the answer in **both form and meaning**.
  All of it asserted in check_site_health.py and mutation-tested.
  **Process note, repeated offence:** re-injecting the block by splicing
  between two string indices duplicated the whole shell AGAIN
  (`VERSE_TEXT has already been declared`). The rule already written here was
  ignored. To re-apply learn_block changes: restore
  `.backup/build_gita.py.before-learn`, then run the single clean patch that
  asserts each anchor occurs exactly once. Never splice by index.

* **"Verses only" retired · "Learn by heart" added (owner 2026-09-01).**
  The chooser was three reading modes; it is now a student's arc —
  **Read it · Study it · Learn it by heart.**
  - **Mūla removed.** The root text with no meaning served a reciter, not a
    student, and cost a third of the chooser for a mode that taught nothing.
    `'mula'` survives as a silent ALIAS: `showRead()` maps it to `'full'` and
    the `#chapter=N&tab=mula` regex still accepts it, so every link already
    shared keeps working. 5 orphaned i18n keys and 2 dead CSS rules removed.
    Nothing indexed broke — the 18 crawler pages only ever linked `tab=study`.
  - **Learn by heart** (`source/learn_block.py`, ~430 lines, injected into the
    shell). Two stages, and the order IS the pedagogy: **the story first**
    (a chapter's themes in sequence are its plot — learn the spine and every
    verse afterwards has somewhere to hang), **then the verses**, theme by
    theme. Everything is RECALL, never re-reading: a miss is requeued and
    comes round again, so a run ends only when the queue is genuinely empty.
    1,584 drill items across all 202 themes, zero themes generating nothing.
    The story stage scales — chapters of 10+ themes earn all four steps,
    smaller ones get read → whole-chain, because drilling four stages over six
    themes is ceremony, not teaching.
    Progress: ONE `gitaLearn` key for all 18 chapters, hardened like the
    favourites (validated against 9 corrupt payloads). Local to one browser,
    and the UI says so rather than letting someone lose work silently.
  **Two real bugs the suite caught, both mine:** `var(--card)` does not exist
  in this app's palette (it is `--cream` / `--paper`) — the undefined-variable
  guard added after the 2026-09-01 audit caught it immediately, which is
  exactly why that check exists. And a `?????` blank placeholder tripped the
  "no nullish coalescing" lint; it is em-dashes now.
  **A process note worth keeping:** a splice that removed text between two
  anchors silently DUPLICATED a region of the shell, and `node --check` found
  it (`VERSE_TEXT has already been declared`). Recovered from
  `.backup/build_gita.py.before-learn` and re-applied in one clean pass with an
  idempotency guard. Never splice by index into the builder; append at a unique
  anchor and assert the anchor occurs exactly once.
  UI strings 96 → 141 in all three languages. **Nepali and Hindi teaching copy
  is a first draft and wants the owner's ear** — it must sound like a teacher,
  not a translation.

* **Sheet navigation repaired (owner 2026-09-01).** Prev/Next was dead in
  three of the four ways into a verse, and had been failing silently:
  - **Thematic study:** `partBounds()` returned the enclosing PART's range.
    That was correct when a part grouped several verses, but parts are now one
    verse each (700 parts for 700 verses), so it returned `{start:n, end:n}` —
    a range of one — and **both buttons were disabled on every verse in the
    app**. Replaced with `themeBounds()`, which spans the whole theme, as the
    "← Back to theme" affordance always implied.
  - **Verses only / Verses with translation:** these opened the sheet with
    `mode:'read'`, which `navSutra()` never handled — it fell through to
    `else return`, so the buttons did nothing. `read` is now a real mode,
    **scoped to the chapter**: Prev/Next walk that chapter and stop at its
    edges. Owner's call, and the right one — the chapter is the unit a reader
    actually inhabits ("I'm reading chapter 12", never "verse 412 of 700"),
    the counter means something ("verse 12 of 20"), and nobody is silently
    relocated into the next chapter by pressing Next. Search and favourites
    keep ranging over all 700, because those lists are not chapter-scoped.
  Neither failure raised an error, which is why nothing caught them; both are
  now asserted in check_site_health.py and mutation-tested.
* **"Part" retired from the interface (owner 2026-09-01).** Themes are granular
  now and hold verses directly, so the word means nothing to a reader. The one
  visible string (`opt_study_d`) was reworded in all three languages. The
  internal `t.parts` container is deliberately LEFT ALONE: renaming it reaches
  the data pipeline, the builder and every verifier for zero visible gain.
  The CSS class names (`.part-head`, `.ptitle`) are likewise invisible.

* **Chrome polish, 2026-09-01 (owner).** Two things, both one-line fixes with
  a reason worth keeping:
  - **The theme toggle hovered differently from the language buttons** beside
    it. `.theme-btn:hover` overrode the shared `.lang-btn:hover` with a faint
    `--chip-hover` wash and, critically, never changed `color` — and since
    `.ic` is `stroke:currentColor`, the sun/moon glyph stayed saffron on a
    saffron fill, so the control looked dead next to its neighbours. It now
    inherits the same `--saffron-dark` / `--on-saffron` pair. Resting state is
    unchanged (still saffron). A test asserts the two hover declarations are
    byte-equal, so they cannot drift apart again.
  - **"How would you like to receive this chapter?" was `--saffron-dark`** —
    the exact colour of the pills it labels, which made a plain caption look
    pressable. It also measured **3.34:1 on white, under the 4.5:1 AA floor**.
    Now `--ink-soft`: **7.75:1 light / 6.22:1 dark**, and saffron once again
    means "you can press this". Contrast computed, not eyeballed.

* **Devanagari font extracted from chapter.css (2026-09-01).** It was a
  base64 data: URI inside the stylesheet: **60,602 B, 93% font** — and the
  browser re-downloaded all of it for the chapter pages even though
  `index.html` already carries the identical bytes inline. Base64 also inflates
  binary by ~33%. Now published as a real file, `noto-deva-regular.woff2` at
  the site root, fetched once and shared by all 18 chapter pages.
  **chapter.css: 60,602 -> 4,996 B (-92%).** A reader opening three chapter
  pages transfers 46,700 B instead of 181,806 B (**-74%**), and zero on
  subsequent pages.
  Three details that make it correct, each now asserted:
  - CSS resolves `url()` against the STYLESHEET, not the page. chapter.css
    lives at the site root, so a BARE filename is right for every
    `/chapter/N/` page. A leading `/` would break on a GitHub *project* page
    (the site is under `/Bhagavad-Gita/`), and `../` would break too — the
    check rejects both forms.
  - The font is a network request now, so it MUST be precached or chapter
    pages lose their Devanagari offline. Added to `ASSETS`.
  - It is a precached binary, so `CACHE_VER` hashes its BYTES; swapping or
    subsetting the face invalidates the cache instead of stranding readers on
    the old one.
  `index.html` deliberately KEEPS its inlined copy: it is the app shell, and a
  separate request there would cost a round-trip on first paint.

* **Deep audit, 2026-09-01 (round 2) — four more fixes, and a clean bill.**
  A full pass over data, security, JS robustness and semantics. What was found:
  1. **Corrupt localStorage could brick the app.** `favLoad()` guarded
     `JSON.parse` but not the RESULT's type: a stored `null`, `5` or `{}`
     parses fine and then throws on `.includes()` — which runs on every verse
     modal. One bad write (devtools, a sync bug, a shared device) would make
     every verse unopenable, with no recovery but clearing storage. Both
     loaders now validate shape and drop malformed entries while keeping the
     valid ones. Verified against 8 corrupt payloads.
  2. **`browser_checks.py` still tested the deleted v/ pages** — 141 live
     checks would have failed hard on the next machine with Playwright. Now it
     tests what actually matters for the new scheme: that a shared link opens
     the folded `<details>`, highlights the verse, AND scrolls it into the
     viewport (present-in-DOM is not the same as visible).
  3. **Heading levels skipped h1 → h3** on all 18 chapter pages; theme headings
     are now `<h2>`. Styling byte-identical (the `.th` class does the work);
     dead `h3.th` selectors removed.
  4. Stale docstring referencing the deleted `verify_share_pages.py`.
  **Confirmed clean, with evidence:** 700 verses exactly, no duplicates, all
  700 present in both Nepali and Hindi translations (0 missing) with 3993 gloss
  terms each; chapter 13 has 34 verses, which is correct — the 35-verse
  recension would total 701, and this edition's 34 is what makes 700. XSS:
  `esc()` is correct and the only user-authored field (favourite notes) is
  escaped — tested with four real breakout payloads, all neutralised; the
  search query is never echoed into the DOM, and all three `location.hash`
  readers use strict anchored regexes. Service worker: skips cross-origin and
  non-GET, never caches opaque or non-200 responses, and only stores the app
  root as the offline shell. Sitemap matches disk exactly (19/19). No secrets.
  Only one dead function existed in 85 and it is gone.
  Suites now: **376** site-health checks, **557** document assertions, 2800
  pādas, 2100 paraphrase pairs, 6 SEO checks — every fix mutation-tested.

* **v/ RETIRED — verse links now go to /chapter/N/#vN.NN (owner 2026-09-01).**
  The 700 per-verse pages worked, but publishing them was the problem: GitHub's
  web uploader refuses more than 100 files at a time, so every republish meant
  seven manual drag-and-drops. (Worth knowing: this is a WEB-UI limit only —
  `git push` sends all 700 as one 754 KB commit. The owner publishes through
  the browser, so the limit is real for him.) The repo went 930 → 230 files.
  A shared verse now points at its anchor on the chapter page, which already
  carried the full verse in Devanagari, IAST and all three languages, and was
  already indexed. Three things had to be true for this to work, and each is
  now locked by a test:
  1. **The anchor must exist.** `check_site_health.py` cross-checks all 700
     anchors against `ch*.json` — a missing or renamed one fails the build.
  2. **The verse must be VISIBLE.** Every verse sits inside a collapsed
     `<details>`; a browser cannot scroll to an element with no layout box, so
     a naive deep link would have silently landed at the top of the page. Each
     block now has an id (`det-N`) and an inline script opens the enclosing one
     on load and on `hashchange`, then highlights the verse (`.v.target`,
     saffron ring). Progressive enhancement: JS off, the page is still complete
     and `:target` still styles the verse.
  3. **Old links must not die.** Links already sent to people are permanent.
     `404.html` parses a retired `/v/N.NN/` path and `location.replace()`s to
     `/chapter/N/#vN.NN`, so every link ever shared still lands on its verse.
  **THE TRADE, stated plainly:** the link preview is now the CHAPTER's, not the
  verse's — every verse in chapter 2 previews as "Chapter 2 — Sāṅkhya Yoga".
  The verse no longer appears in the WhatsApp card. This is the second time the
  preview has been downgraded to save weight/effort (the 700 card images went
  on the same day); the owner chose it knowingly both times. If per-verse
  previews are ever wanted again, the only honest route on GitHub Pages is to
  bring back per-verse HTML — and then publish with `git push`, not the web
  uploader, or the same pain returns.
  `source/verify_share_pages.py` was deleted — its entire subject is gone. Its
  guarantees live on in `check_site_health.py` (320 checks) and
  `run_gita_app.js` (557 assertions), both mutation-tested against this change.

* **Whole-site audit, 2026-09-01 — nine faults found and fixed.** None had
  been caught by the 553 document assertions, the 700-page share audit or the
  data checks, because every existing suite reads the APP document, the SHARE
  pages or the DATA. Nothing read the generated CHAPTER pages, the CSS, or the
  `<head>`. In order of severity:
  1. **`chapter.css` declared `--soft` while 12 rules used `var(--ink-soft)`.**
     An undefined custom property fails silently, so every muted line
     (breadcrumb, IAST, verse description, theme range, paraphrase) rendered at
     full `--ink` on all 18 pages, in both themes. The design's whole visual
     hierarchy was gone and no test could see it. Renamed to `--ink-soft`,
     matching the app's own palette.
  2. **`index.html` declared `og:image` and `twitter:card` TWICE, conflicting**
     (`icon-512.png` + `summary`, then `og-card.png` + `summary_large_image`).
     Crawlers take the FIRST `og:image`, so the homepage previewed with the
     square app icon while the `1200×630` dimensions described the other file —
     a mismatch some crawlers reject outright. Now exactly one of each.
  3. **Chapter pages violated the numbering doctrine 700×** — `2.01 ↗` and
     ranges `2.01–2.03`, on the 18 pages Google actually indexes, while the
     doctrine was locked only on the share pages. Replaced the fragile
     `.replace(".0", ".")` trick with real `_dnum()` / `_drange()` helpers.
     URLs, ids and anchors deliberately KEEP the padded form.
  4. **`chapter.css` was never precached** while the manifest and README both
     promise "Works offline" — a chapter page reloaded offline rendered as an
     unstyled wall of text. Added to `ASSETS`, and `CACHE_VER` now hashes
     `CHAPTER_CSS` too (it is precached, so it must invalidate the cache;
     the CSS block had to move ABOVE the hash for that to be possible).
  5. **No `404.html`.** Every stale share link was a dead end on GitHub's
     generic page. The new one is noindex and recovers `#v=` / `#chapter=`
     from the dead path, so an out-of-date verse link still lands on its verse.
  6. **Sanskrit was unmarked on chapter pages** — Devanagari in bare `<div>`s,
     so screen readers pronounced it with an English voice. Now `lang="sa"`
     (and `lang="sa-Latn"` on the IAST), matching what the v/ pages already did.
  7. **Two `<h1>` in the app**; the welcome heading became `<h2>` (`.view-title`
     was already doing all the styling, so nothing moved visually).
  8. **No live region** — a screen-reader user heard silence on every view
     change in a single-page app that never navigates. Added `#srStatus`
     (`role=status`, polite) driven by `announceView()`, hooked into
     `scrollViewTop()`, which already dedupes on a view signature so it fires
     exactly once per real change.
  9. **One dead function** (`chLabel`, unreferenced among 85) — removed.
  **Still open, deliberately:** `chapter.css` embeds the same 54 KB Devanagari
  woff2 that `index.html` already inlines, byte-identical. It is 93% of that
  file and cannot be shared between them while both are inlined. Extracting it
  to a real `.woff2` would make it cacheable across all 19 pages and cut
  chapter.css from 58 KB to 4 KB — deferred because it changes the upload set.
* **New lock: `source/check_site_health.py` (262 checks).** Every fault above,
  asserted. Validated by MUTATION TESTING: each fix was reverted one at a time
  and the suite had to fail — the first pass caught only 7 of 9, which exposed
  two holes worth recording. (a) Checking CSS variables as a UNION of `:root`
  and the dark `@media` block let fault #1 walk right back in, because the
  other palette still defined the name; each palette is now checked
  independently. (b) A missing file threw a traceback instead of reporting,
  which would have masked every later check; `read()` now records a failure and
  continues. Wired into `build.py` and `rebuild.sh` alongside the share audit.

* **Per-verse share cards RETIRED (owner, 2026-09-01).** The 700 painted
  cards `img/v/N.NN.jpg` are gone — they took the repo from ~3 MB to 60+ MB
  for a link thumbnail, which broke the working-session size budget (128 MB).
  Every `v/N.NN/` page now uses the site's single card `og-card.png`
  (1200×630), the same face `index.html` and the chapter pages already show.
  The verse itself still travels in the preview as TEXT (og:title = number +
  topic, og:description = the two pādas + the literal + the click line), so a
  shared link still reads as that verse. `img/share-art.jpg` (52 KB) is still
  painted at build time and remains orphaned.
  **Live cleanup needed:** DELETE the `img/v/` folder on the live site
  (700 stale files) and re-upload `v/` (700 pages, new og tags). Repo is now
  ~19 MB (mostly `source/` + `data/`); the published site is a few MB.
* **Live sync (verified 2026-08-31):** the live site matches local
  byte-for-byte — `index.html`, `sw.js`, `img/share-art.jpg` and all **700
  `v/` share pages**, except the `img/v/` cards now retired above.
* **Verified 2026-08-31 (cold reproof):** `python3 build.py` → 2800 pādas
  0 residual + 2100 paraphrase pairs OK + check_seo 6/6 + **553** document
  assertions; `browser_checks.py --serve` (playwright reinstalled) → **141**
  live-browser checks — all green, offline SW included. New independent
  audit `source/verify_share_pages.py` cross-checks all 700 `v/` pages
  against `ch*.json` (Devanagari body), self-consistency (dir/URL/redirect/
  canonical/og:title number) and the artwork (960×504): **0 mismatches**.
  `img/share-art.jpg` re-confirmed present. Screenshot-verified the shared
  link flow at 390px: `v/N.NN/` bounces into the app and lands on the
  invitation "SHARED VERSE" card with the click-line.
* **Code hygiene (2026-08-31):** fixed the stale comment header on the v/
  pages in `build_gita.py` — it still claimed "NO og:image" while the code
  ships `img/share-art.jpg` (the round-2 decision). Comment-only; no output
  change (SW cache hash identical).
* **Delivery rule (owner, 2026-08-31): ALWAYS hand over the TOTAL repo zip**
  (`downloads/Bhagavad-Gita-700-titles.zip`, rebuilt and re-proven
  byte-identical with `diff -r` after unzipping). It is his crash checkpoint:
  if a session dies, the next one starts from the zip + this file.
* **Design system now in force (volume-controlled 2026-08-31, "too much
  orange"): one gold per page** — gold = the decision you're IN (the raised
  tray segment). Trail steps down: current page = soft saffron pill,
  ancestors = neutral hairline pills; hover warms one step. The tray wears
  the card hairline; its saffron lives in the question line and segments.
  Saffron ground always gets the lamp-black letter (`--on-saffron`). The
  header language bar keeps its iOS segment look with the warm hover.
  Study guide: theme box is the door, verses are display-only cards. No
  intermediary choice page.
* **Suites:** `python3 build.py` → source checks + `run_gita_app.js`
  (553 assertions) + `browser_checks.py` (141 checks). The doc-locks fail
  loudly if counts/keys drift from the docs — update them together.
* **Sandbox quirks:** playwright must be reinstalled every session
  (`pip install -q playwright && python3 -m playwright install --with-deps
  chromium`); local http servers die between turns (restart
  `python3 -m http.server 8000 --bind 0.0.0.0`); `/tmp` is wiped.
* **Owner protocol:** call him Dhruba or brother (never "bhai"); argue with
  him when best practice says so; verify every claim with a tool before
  stating it; write decisions here the moment they are made.

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

**Content:** 18 chapters · 222 themes · 700 parts · 700 verses, each with
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
run_gita_app.js       553 assertions on the built document      (needs node)
browser_checks.py     141 live-browser checks                 (needs playwright)
edit.py               local browser-based content editor
editor.html           its interface
source/
  ch*.json            verse Devanagari + IAST            <- the running verse
  padas_ch*.py        the four pādas of every verse      <- the popup boxes
  padachheda_ch*.py   word-by-word split + English gloss
  check_seo.py        sitemap/robots proof (local, or --live)
  gloss_ne/hi.py      Nepali/Hindi word meanings, keyed by IAST
  gita_data*.py       English themes, parts, translations
  themes_ne/hi.py     Nepali/Hindi themes and parts
  translations_ne/hi.py
  i18n_chapters.py    chapter names/blurbs (ne, hi)
  i18n_ui.py          165 UI strings × 3 languages
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

**4.10 Part titles must be readable headlines, never raw verse openings.**
Found 2026-08-26 (owner spotted "Karmaṇy-Evādhikāras Te" heading the 2.47
search card while its siblings read like sentences): a part title is a short
readable line in each language ("Action Alone, Not the Fruits" / "कर्ममा मात्र
अधिकार, फलमा होइन" / "कर्म में मात्र अधिकार, फल में नहीं"). A full-class audit
(every part title in all three languages compared against its own verse's
opening) found exactly this one defect; single *terms* like राजविद्या /
"ज्ञानयज्ञ" / "ब्रह्मभूत" are genuine words and stay, as do proper names in
IAST (Bhīṣma, Sāttvic, Puruṣottama) — the established style.

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
| 5  | a part/theme title that is a raw verbatim opening of its verse (not a
     headline) or carries a drafting slash — added 2026-08-26 after the
     700-verse title audit; short genuine terms that share a first word
     (ज्ञानयज्ञ, ब्रह्मभूत, 4.13's translated first-person titles) pass by design |

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
* **Title and description are branding decisions** — the suite locks the exact
  `<title>`; changing it means updating `run_gita_app.js` and
  `browser_checks.py` deliberately, together with this file.
