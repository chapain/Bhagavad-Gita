# HANDOFF.md — start here

**New AI session (Arena or any other): read this file first.** It is the short,
*current* status: where the work stands, what was found, what to do next.
`PROJECT.md` is the long history — read its **§8 “Working with the owner”**
before you talk to the owner.

| | |
|---|---|
| Last updated | 2026-10-11 (UTC) |
| Updated by | Arena session on branch `arena/cbe968bc-bhagavad-gita` |
| Base commit | `e1db2d8a` on `main` (PR #27 merged, batch 16 present) |
| Owner | Dhruba Chapain, Pokhara |
| Live site | https://chapain.github.io/Bhagavad-Gita/ |

> **Rule for every session:** before you stop, update §1, tick boxes in §6 and
> add one line to §8. Keep this file short; long history belongs in PROJECT.md.

---

## 1. Where we are

- **Batch 16 (partial chapter 12, verses 12.01–12.04):** PR #26 merged at `28a802a`; batch-15 content verified on `main`. Four verses reviewed, two `paryupāsate` NE/HI overrides at 12.01 and 12.03. This was the state before batch 17; evidence and exhaustive word ledger are in `/home/user/evidence/batch16/`.
- **Batch 17 (Phase 2.1, 2026-10-11):** all 29 verses of chapter 5 and the remaining 16 verses of chapter 12 reviewed. **45/45 verse verdicts** recorded (26 confirmed, 18 with corrections, 12.19 flagged); 23 NE/HI-only word overrides and 568 unchanged word occurrences enumerated (587 pāda rows plus the speaker-word rows for both 5.01 and 5.02). Chapter 5 and chapter 12 are now complete. Overall verse-review ledger: **591/700**, with 109 verses remaining in chapters 1, 13 and 17. The phrase-level mapping in 12.19 `yena kenacit` remains unresolved; 5.09 `dhārayan` and 5.24 `tathā` are retained with explicit rationales. No owner holds were changed. Source commit `406c766` is pushed to the assigned branch; [PR #28](https://github.com/chapain/Bhagavad-Gita/pull/28) is open to `main` for Dhruba to review. Worksheets, occurrence ledger, assertions and browser evidence are in `/home/user/evidence/batch17/` (outside Git).


- **2026-10-09 — Phase 1 complete (steps 1.1–1.9).** Step 1.4 made
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
- **Step 1.8 done — §7.1 implemented.** The UI framework now says **तीन मार्ग**
  and the three cards/tabs are prefixed **कर्ममार्ग · भक्तिमार्ग · ज्ञानमार्ग** in
  all three languages: 25 values in `i18n_ui.py`, every key kept (202 per
  language), the wayName comment and `browser_checks.py:328` reworded to the
  mārga name, and no verse-level निष्ठा touched (3.3, 5.17, 17.1, 18.50 and the
  glosses keep it). The decision, its rationale and the exact string list live
  in §7.1; evidence (before/after plus 390 px hi/ne/en shots) is in the PR.
- **Verification:** `python3 build.py` passes with the §4 Playwright setup —
  9,366 word checks and 2,800 line checks (0 flags), 2,100 paraphrase pairs,
  6 SEO, 572 site-health, 9,658 study-structure, 19 Python tests, 802 document
  assertions, 15 + 7 Node tests and all 162 browser checks. The rebuild changed
  only `index.html` and the `sw.js` cache id; `git status` is clean afterwards.
- **GitHub (verified 2026-10-09):** PR #12 is **merged** (03:30 UTC) into `main`
  at `0828287`, which is this session’s base, and it carries `18b6074` and
  `681d12c`; `source/i18n_ui.py` on `main` already reads “तीन मार्ग” and
  “कर्ममार्ग”, so step 1.8 is not repeated. PR #12 does **not** contain the §7.2
  decision (the owner gave it after the merge), so this session’s first commit
  writes it into the repo.
- **Step 1.9 done — §7.2 implemented.** 18.66’s paraphrase now reads
  Śaṅkara’s *sarvadharmān* — all dharma and adharma, the sense of doership
  itself — instead of “all other paths”, in en/ne/hi; 15.7 carries the *aṃśa
  iva* hedge (“As if an eternal portion of myself…” / मानौं / मानो) in the
  three paraphrases and in the 15.7 theme/verse copy (`gita_data15.py`,
  `themes_ne.py`, `themes_hi.py`, and the `STUDY_MAPS.md` line that quotes
  it). Literals untouched; overlap with the literal fell for all six pairs
  (worst 72.4 %), global max still 79.8 %. Exact strings in §7.2 and the PR.
- **Verification (step 1.9):** `python3 build.py` green with the §4 Playwright
  setup — strict word/line checks (0 flags), 2,100 paraphrase pairs, 6 SEO,
  572 site-health, 9,658 study-structure, 19 Python tests, 802 document
  assertions, 15 + 7 Node tests, 162 browser checks. Generated churn:
  `data/ch15.js`, `data/ch18.js`, `chapter/15/`, `chapter/18/`, `sw.js` cache
  id (the `v/` share pages were retired on 2026-09-01). `git status` clean.
- **GitHub (verified 2026-10-09):** PR #13 is **merged** into `main` at `9db111e`,
  carrying `ad1f752`, `5c71004` and `d8a57f9`; the 18.66 and 15.7 lines on `main`
  match §7.2, so step 1.9 is not repeated.
- **2.1 batch 1 done — `te` = “they”.** The 26 verses in §5.2 now have five-field
  word entries: nominative तिनीहरू (ne) / वे (hi), not तिम्रो / तुम्हारा (“your”).
  Audit §3 `te` count 26 → 0; 9,366 / 9,484 unchanged. Generated churn: `data/`
  for chapters 1, 2, 3, 5, 7, 8, 9, 10, 12, 13, 16, and `sw.js`.
- **2.1 batch 2 done — `me`, `param`, `bhūtāni`, `yogam`.** `me` = “to me” (tell /
  show / offer) now reads मलाई / मुझे in 2.7, 5.1, 6.30, 9.26, 11.4 and in 11.45’s
  *darśaya me*, while 11.45’s *mano me* keeps मेरो / मेरा as its own entry — one
  verse, two forms. `param` 2.12 → भविष्यमा / भविष्य में (was परम “supreme”),
  `bhūtāni` 9.25 → भूतहरू / भूत (was प्राणीहरू; its own pāda says भूतपूजक), and
  `yogam` 11.8 → ऐश्वर्य (en “sovereignty”, and the verse’s own literal). 6.30 and
  `yogam` were the two owner calls; he left both to craft, so §5.2 records why
  6.30 follows the corpus dative and 10.7 keeps योग. Audit §3 `me` 16 → 10;
  9,366 / 9,484 unchanged. Generated churn: `data/ch2, ch5, ch6, ch9, ch11` +
  `sw.js` cache id.
- **2.1 batch 3 done — `tat` and `yat`.** Added 21 contextual entries across
  chapters 1, 2, 3, 9, 11, 13, 15 and 17; only Nepali/Hindi word fields changed.
  Audit §3 remains `te` 0 / `me` 10; 9,366 / 9,484 unchanged. Full build and
  162 browser checks pass.
- **2.1 batch 4 done — `bhīma`, `kutaḥ`, `sattvam`.** Six inline five-field
  entries in chapters 1, 2, 10, 13, 18; all 19 occurrences reviewed, 13 kept.
  Śaṅkara’s 18.40 “being” includes non-living things, so it uses जीव वा जड वस्तु /
  जीव या जड़ वस्तु, not just प्राणी. Audit §3 before/after `te` 0 / `me` 10;
  9,366 verse words / 9,484 glosses unchanged. Full build including 162 browser
  checks green; 12 mobile ne/hi sheets read back. Next: the remaining forms
  in the 674-form pool; owner picks the next slice.

- **2.1 batch 5 done — `arjuna`, `samāḥ` (2026-10-11).** Dhruba flagged
  1.04 pāda 2; editorial judgement was delegated after checking all four word
  entries against the split, English word glosses and en/ne/hi literals. Added
  two five-field overrides in `source/padachheda_ch1.py`: `arjuna` “and Arjuna”
  → र अर्जुन / और अर्जुन and `samāḥ` “equal” → समान / समान. Its 22 other
  `arjuna` vocatives and 6.41 `samāḥ` “years” remain correct as-is (§5.2).
  Appendix A §3 before/after `te` 0 / `me` 10; 9,366 / 9,484 unchanged.
- **Verification (batch 5):** full build green: strict pāda check 2,800/0,
  2,100 paraphrase pairs, 6 SEO, 572 site-health, 9,658 study-structure,
  19 Python tests, 802 document assertions, 15 + 7 Node tests and all 162
  Playwright browser checks. Six 390 × 844 ne/hi screenshots of 1.04, 2.02 and
  10.41 (chapters 1, 2 and 10) were captured and read back; 1.04 contains the
  new meanings, the other two visually confirm settled batch-4 overrides.
  Screenshots: `/home/user/evidence/batch5/`.
- **Full repository zip:** `/home/user/Bhagavad-Gita-phase2.1-batch5.zip`.
- **GitHub (verified 2026-10-11):** PR #18 is **merged** (04:18 UTC) into `main`
  at `5d8cdfe`, which is this session's base.

- **2.1 batch 6 done — `me` = "to me" cleanup (2026-10-11).** The remaining
  10 audit-flagged `me` = "to me" verses were checked against each verse's
  Sanskrit text and en/ne/hi literal translation. 9 entries across 8 verses
  needed NE मेरो→मलाई / HI मेरा→मुझे; 2 were correctly possessive and left
  alone: 9.29 (*na me dveṣyo'sti* — translation says मेरा) and 18.69 pāda 1
  (*kaścinme priyakṛttamaḥ* — translation says मेरो सेवा). Five-field overrides
  in `padachheda_ch12.py` (6 entries: 12.14–12.17, 12.19, 12.20) and
  `padachheda_ch18.py` (3 entries: 18.64, 18.65, 18.69 pāda 2). All 84 `mām`,
  24 `mama` and 20 `mayi` occurrences verified correct and left alone.
  Appendix A §3 before `te` 0 / `me` 10; after `te` 0 / `me` 2;
  9,366 / 9,484 unchanged.
- **Verification (batch 6):** full build green: strict pāda check 2,800/0,
  2,100 paraphrase pairs, 6 SEO, 572 site-health, 9,658 study-structure,
  19 Python tests, 802 document assertions, 15 + 7 Node tests and all 162
  Playwright browser checks. Six 390 × 844 ne/hi screenshots of 12.14, 18.65
  and 9.29 (chapters 12, 18 and 9) captured and read back; 12.14 and 18.65
  show मलाई/मुझे, 9.29 confirms मेरो/मेरा (possessive, left alone).
  Screenshots: `/home/user/evidence/batch6/`.

- **2.1 batches 7–9 done — chapters 4, 14 and 16 read verse by verse
  (2026-10-11).** One chapter per batch, judged on the flagged-instance counts
  of the sweep (ch4 334 of 571 word entries, ch14 158 of 323, ch16 124 of 290).
  Each of the 93 verses was read with its en/ne/hi literals and every word
  checked for (a) English gloss vs the verse in context, (b) Nepali meaning vs
  the Nepali literal, (c) Hindi meaning vs the Hindi literal. **43 five-field
  overrides** were needed: 24 in `padachheda_ch4.py`, 8 in
  `padachheda_ch14.py` and 11 in `padachheda_ch16.py`; only word[3]/word[4]
  changed. Full table in §5.2. Clear contradictions fixed include person and
  tense mismatches that the ambiguity scan alone cannot see (`viduḥ` “knew” vs
  present जान्छन् in 4.02, `veda` “know” vs 1sg in 4.05, `paśyet` “sees” vs
  past-habitual देख्थ्यो in 4.18, `san` “being” vs हुआ हुआ in 4.06, `janmani`
  “in birth / after birth” sharing one “after birth” gloss in 16.20) and
  shared-form clashes (`param` “earlier” receiving “supreme” in 4.04, `sevayā`
  “by service” receiving “by practice” in 4.34, `guṇebhyaḥ` receiving “beyond
  the guṇas” in 14.19). All the remaining flagged occurrences (572: 313 / 147 /
  112) were read and are listed verse by verse in the PR. **Owner flags (left
  as-is, out of scope of a word-gloss change):** 4.09 `eti` whose *English*
  gloss “goes” contradicts the verse (*naiti māmeti* = “he comes to me”)
  although its Nepali/Hindi आउँछ/आता है are right; 4.42 `ātmanaḥ` “of the Self”
  vs आत्माको;
  16.10 `mada` whose shared NE gloss carries a stray parenthetical,
  “घमण्ड (ले)”; 16.13–14 `abhimāna` in the compound *abhimānāśrayaṁ* not split
  as its own word. Note for later batches: `sarva`, `param`/`paraḥ`,
  `paryupāsate`, `sevayā`, `tamaḥ`, `san`, `bhavataḥ`, `viduḥ`, `veda`, `me`
  and `janmani` are shared forms whose remaining occurrences in other chapters
  still need their own per-occurrence overrides.
- **Verification (batches 7–9):** full Playwright build green: strict pāda
  check 2,800/0, 2,100 paraphrase pairs, 6 SEO, 572 site-health, 9,658
  study-structure, 19 Python tests, 802 document assertions, 15 + 7 Node tests
  and all 162 browser checks. Appendix A run from both a pristine `7de6723`
  worktree and the working tree: **byte-identical** (`te` 0 / `me` 2;
  9,366 / 9,484; §3 674/4,532). Sixteen 390 × 844 ne/hi sheets for 4.02, 4.05,
  4.06, 4.34, 14.19, 14.23, 16.06 and 16.20 (chapters 4, 14 and 16) captured
  and read back with the changed word's pāda expanded; every sheet shows the
  new meaning (the boxed toolbar labels are the known sandbox font artifact).
  Screenshots: `/home/user/evidence/batch7/`.

- **2.1 batch 10 done — chapter 18 read verse by verse (2026-10-11).** The
  remaining-chapter pool with the highest flag count (482 of 986 word
  instances, 78 verses). Every verse was read with its en/ne/hi literal and
  every word checked for (a) English gloss vs the verse in context, (b) Nepali
  meaning vs the Nepali literal, (c) Hindi meaning vs the Hindi literal.
  **20 five-field overrides** in `padachheda_ch18.py` (word[3]/word[4] only):
  `kavayaḥ` 18.02 (the wise ≠ poets); `tyajet` 18.08 (indicative, not “must”)
  and `labhet` 18.08; `me` = “from me” at 18.13 / 18.36 / 18.50 (NE मेरो→मबाट /
  HI मेरा→मुझसे); `tathā` 18.14 (list “and”, not “thus”); `kṛtsnavat` 18.22 (NE
  “as if not all” reversed → सबैझैं); `ebhiḥ` 18.40 (ablative “from”, not “by”);
  `brahmakarma` 18.42 (NE ब्रह्मको→ब्राह्मणको); `pravṛttiḥ` 18.46 (origin ≠
  tendency → स्रोत); `te` = “to you” at 18.63 / 18.65 and “by you” at 18.67;
  `iṣṭaḥ` 18.64 (dear ≠ worshipped, where 18.70 keeps पूजित); `tasmāt` = “than
  him” ×2 at 18.69 (not “therefore”); `matiḥ` 18.70 / 18.78 (opinion ≠
  intellect → मत, matching 18.06 `matam`); `bhūtiḥ` 18.78 (glory ≠ prosperity,
  which collided with `śrīḥ` in the same pāda). The remaining ~460 flagged
  occurrences were read and left alone; settled keeps include `me` possessive
  (18.04/06/64/70/77), `mayi` (18.68), `tathā` correlative (18.50/63), `niṣṭhā`
  18.50 (protected by §7.1) and `padam` स्थान (corpus-consistent). **Owner
  flags (not word-gloss fixes):** 4.16 has the *identical* `kavayaḥ` defect
  (left for the ch-4 revisit per “one chapter per batch”); 18.53’s ne/hi
  *literals* say the opposite of the Sanskrit for *nirmamaḥ* (“not giving up
  ‘mine’”); `tathā` “also/and” and `matiḥ`/`pravṛttiḥ` shared forms still need
  per-occurrence work in chs 1, 7–11, 13, 17. Appendix A before/after
  identical (`te` 0 / `me` 2; 9,366 / 9,484; §3 674/4,532). Full Playwright
  build green (2,800/0 pāda, 2,100 paraphrase, 6 SEO, 572 site-health, 9,658
  study, 19 Py tests, 802 doc assertions, 15 + 7 Node, 162 browser). Twelve
  390 × 844 ne/hi sheets for 18.02, 18.42, 18.69, 18.78 (ch18) plus 4.16 and
  16.20 (cross-chapter renders) captured and read back. Screenshots:
  `/home/user/evidence/batch10/`. GitHub: PR #21 from
  `arena/207086dc-bhagavad-gita` — https://github.com/chapain/Bhagavad-Gita/pull/21.

- **2.1 batch 11 done — chapter 2 read verse by verse (2026-10-11).** The
  remaining-chapter pool with the highest flag count (428 flagged instances,
  72 verses, all read against en/ne/hi literals). **69 five-field overrides**
  in `padachheda_ch2.py` (word[3]/word[4] only) across 41 verses; the other
  31 verses confirmed with reasons. Clear contradictions fixed include wrong
  case (11 `enam` “this” → यसलाई/इसे, where 2.23’s own literals say यसलाई/इसे;
  `sarvān` ×2 dative/genitive → accusative सबै/सब; `tāni` “them” ती/वे →
  तिनीहरूलाई/उन्हें; `duḥkhe`/`alābhau`/`ajayau`/`duṣkṛte` locative → bare),
  wrong person/mood (`vijānītaḥ` imperative जान/जानो → जान्दछन्/जानते हैं;
  `bhaviṣyāmaḥ` हुने थियौं → हुनेछौं; four `-syasi` futures’ passive प्राप्त
  होगा → active प्राप्त करोगे), backwards readings (`nivartate` “departs”
  फर्कन्छ/लौटता है → जान्छ/चला जाता है; `uparatam` शान्त → भागेको/भागा हुआ;
  `niryogakṣemaḥ` लाभ-हानि → लाभ-स्वामित्व), and adverb/adjective and
  sense clashes (`nityam` “eternal” सधैँ/सदा → नित्य/नित्य; `dhruvam` “certain”
  नित्य → निश्चित; `śreyaḥ` “better” कल्याण → राम्रो/अच्छा at 2.05 and
  उत्तम/बढ़कर at 2.31; `tataḥ` “than that” → त्योभन्दा/उससे; `sarva` “of all”
  हे सबै → सबै/सब). Full 62-key table in §5.2; the per-verse ledger (41
  corrected / 31 confirmed) is in this PR. Settled keeps include `tathā`
  correlative (thus/so ×4 — ch2 has no and/also use), `param` 2.59,
  `kutaḥ` 2.66, `padam` 2.51, `yogam` 2.53, `bhūtāni` “beings” (2.28/30/69),
  `nityam` “always” (2.26/30), `sarvaśaḥ` “fully” 2.68, `bhūtvā` “having
  become” 2.48, and `yujyasva` “devote yourself” 2.50 — each the contrast
  that proves its fixed sibling. **Owner flags (not fixed, out of chapter
  scope):** `mā` → नगर (“don’t do”) is wrong in *every* occurrence — 11.34,
  11.49×2, 16.05, 18.66 (`mā śucaḥ`/`mā vyathiṣṭhāḥ`) — left for revisit
  batches (ch16/18 passed review without catching it); `śucaḥ`’s indicative
  शोक गर्छौ likewise; EN-gloss slips (`tu` “indeed” for adversative but,
  2.57 `dveṣṭi` “reviles”, loose nominatives for locatives/genitives) are
  preserved per the hard rules. Appendix A before/after identical (`te` 0 /
  `me` 2; 9,366 / 9,484; §3 674/4,532); lockstep data diff 138 leaves (69
  flow + 69 padas mirror), only words[3]/words[4]. Full Playwright build
  green (2,800/0 pāda, 2,100 paraphrase, 6 SEO, 572 site-health, 9,658
  study, 19 Py tests, 802 doc assertions, 15 + 7 Node, 162 browser). Twenty
  390 × 844 ne/hi full sheets (2.03/06/12/19/23/33/38/47/59/72) captured,
  113 rendered-string assertions across all 41 touched verses pass, six
  crops read back. Screenshots: `/home/user/evidence/batch11/`.

- **2.1 batch 12 done — chapters 11 and 15 read verse by verse (2026-10-11).**
  First two-chapter batch under the ~75-verse budget (55 + 20 verses; every
  verse read against its en/ne/hi literals). **72 five-field overrides**
  (word[3]/word[4] only): **ch11 62 in 37 verses** (18 confirmed as-is),
  **ch15 10 in 8 verses** (12 confirmed as-is). Ch11 fixed wrong case
  (dative `te` “to you” ×10 तिम्रो/तुम्हारा → तिमीलाई/तुझे; `tvām` “into you”
  ×2 → तिमीमा/तुममें, goal of *viśanti*; `gām`/`deham`/`tapasā` missing case
  markers; comparative ablative `brahmaṇaḥ` ब्रह्मको/ब्रह्म का → ब्रह्माभन्दा/
  ब्रह्मा से; `ṛte` + bare `tvām` → तिमी/तेरे), wrong person/tense/mood
  (`manyase`/`icchasi` 3rd→2nd ps; `asi` “you were” छौ/हो → थियौं/थे),
  wrong case on vocatives (`deva`/`devam`/`īśam`/`aprameyam`), the owner-flag
  `mā` → नगर at **11.34 and 11.49×2** (→ न; 16.05/18.66 stay for revisit),
  and sense clashes (`bhava` “of coming into being” होऊ/बनो → उत्पत्ति;
  `antaram` भेद “difference” → बीचको स्थान; `soḍhum` सहन “bear” → क्षमा गर्न;
  `tapantam` बल्ने intransitive → पोल्ने; opaque transliterations `uṣmapāḥ`,
  `sūtaputraḥ`, `prapitāmahaḥ`; nonexistent NE form काँप्दो → काँप्ने).
  Ch15 fixed `enam` “this” उसलाई/उसे → यसलाई/इसे, sequential `tataḥ`
  त्यसैले/इसलिए → त्यसपछि/तब, the owner-flag `pravṛttiḥ` “the course” प्रवृत्ति →
  प्रवाह/धारा (flowing stream per the literals; ≠ the 18.46 स्रोत fix),
  `īśvaraḥ` “the lord” of the body ईश्वर → स्वामी (15.17’s divine sense kept),
  `acetasaḥ` अचेतन “unconscious” → समझ नभएका/समझ न होने वाले, opaque
  `vaiśvānaraḥ` → पाचक अग्नि, and superlative `uttamaḥ` उच्च → परम (15.18’s
  comparative kept). Full tables in §5.2; per-verse ledger in this PR.
  Settled keeps prove each fix: correlative/quotative `tathā`/`iti`,
  possessive `tava`/`me`, `padam` स्थान (batch-10 settle), `nivartante`
  “they return” (mirror of 2.59’s “departs” fix), `adhiṣṭhāya` अधिकार at 15.09
  (mirror of 4.06’s fix), voice-neutral infinitives, optative `syāt`,
  Krishna register तिमी/तुम. **Owner flag (not a word gloss):** the 11.44 NE
  literal renders *praṇidhāya* as “शरीर थपथपाउँछु” (“pats the body”) instead
  of prostrating; the HI literal (पसारता) is right — literal-level slip left
  for Dhruba. Appendix A before/after identical (`te` 0 / `me` 2; 9,366 /
  9,484; §3 674/4,532); lockstep diff only ch11/ch15 data + sw.js cache id.
  Full Playwright build green (2,800/0 pāda, 2,100 paraphrase, 6 SEO, 572
  site-health, 9,658 study, 19 Py, 802 doc, 15 + 7 Node, 162 browser). Eight
  390 × 844 ne/hi full sheets (11.34/37/39/49, 15.04/11/13/14) with 34
  rendered-string assertions. Screenshots: `/home/user/evidence/batch12/`.


- **2026-10-11 — Batch 13 cleared and completed (chapters 3 + 7).** PR #23’s
  merge into `main` at `1b7b83c` was checked by content before this batch; no
  batches 1–12 were repeated. The Appendix A baseline was reproduced and the
  pre-edit full §4 build was green before touching source. All 43 chapter-3
  and 30 chapter-7 verses were checked word by word against the English,
  Nepali and Hindi literals. **51 inline five-field overrides** (32 in ch3,
  19 in ch7; only word[3]/word[4]); full verdict/reason worksheets and the
  exhaustive unchanged-occurrence lists are in §5.2 / `/home/user/evidence/batch13/`.
  Interpretive holds remain for Dhruba; the ch7 `tathā` “also/and” carry-forward
  is resolved at 7.06. Appendix A before/after identical (`te` 0 / `me` 2;
  9,366 / 9,484; §3 674/4,532). Full build passed all 162 browser checks;
  102 rendered-string assertions passed; 16 Nepali/Hindi 390 × 844 screenshots
  show the changed pādas expanded. Full-repo zip:
  `/home/user/downloads/Bhagavad-Gita-700-titles.zip` (byte-identical round trip).
  [PR #24](https://github.com/chapain/Bhagavad-Gita/pull/24) is open from
  `arena/39ceb621-bhagavad-gita` to `main`, containing source-review commit
  `a3e4b54`. No other batch or Phase 2 item was started. The 11.44
  *praṇidhāya* literal “शरीर थपथपाउँछु” remains Dhruba’s decision — remind
  him, do not fix it.

- **2026-10-11 — Batch 14 done (chapters 6 + 8).** PR #24 was confirmed
  **merged** on GitHub and re-verified by *content* on `main` (state MERGED,
  10:59:37 UTC, merge commit `05dc983` = the tip of `origin/main`; both batch-13
  commits `a3e4b54` and `918f4eb` are real ancestors, the 51 overrides are in
  `source/padachheda_ch3.py` / `_ch7.py`, and the rendered `data/ch3.js` and
  `data/ch7.js` carry the new NE/HI in both the `flow` and `padas` mirrors with
  no non-`word[3]`/`word[4]` leaf touched). The clone was
  shallow, so `git fetch --unshallow` was run before ancestry checks. Appendix A
  was reproduced and the pre-edit full §4 build was green before any source
  edit. **All 47 chapter-6 and 28 chapter-8 verses were read against their
  English, Nepali and Hindi literals. 27 inline five-field overrides** (18 in
  ch6, 9 in ch8; only word[3]/word[4]) across 23 verses; 52 verses confirmed
  as-is. Full tables in §5.2; worksheets, changed-word tables, the exhaustive
  unchanged-occurrence list (1,011 occurrences) and the open holds are in
  `/home/user/evidence/batch14/chapter6-review-worksheet.md` and
  `chapter8-review-worksheet.md`. Appendix A before/after **byte-identical**
  (`te` 0 / `me` 2; 9,366 / 9,484; §3 674/4,532). Full §4 build green: 2,800/0
  pāda, 2,100 paraphrase, 6 SEO, 572 site-health, 9,658 study, 19 Python tests,
  802 document assertions, 15 + 7 Node tests and all **162 browser checks**;
  **54 rendered-string assertions** passed and **94 390 × 844 ne/hi sheets**
  (46 full sheets + 48 changed-pāda crops) were captured. The **6.36 `matiḥ`
  carry-forward is resolved** (मत, matching 18.06/18.70/18.78); the additive
  `tathā` at 8.25 is resolved too. **Owner flags carried or raised here:** 4.16
  `kavayaḥ` still open; `mā`/`śucaḥ` at 16.05 and 18.66 still open; 6.13
  `dhārayan` NE धानेर (non-standard form); 6.29’s *English literal* adds “— he
  attains the Supreme”, which the verse does not say; **8.10’s verse text reads
  “सम्य क्स तं” / “samya ksa taṃ” where the sandhi should be सम्यक् स तं /
  samyak sa taṃ** — verse text is out of a word-gloss batch, so it is reported,
  not fixed. Source-review commit `2076740` from the prior Arena branch was
  merged via [PR #25](https://github.com/chapain/Bhagavad-Gita/pull/25) at
  `e09f31e`; its content was verified before batch 15. The prior full-repo zip
  `/home/user/downloads/Bhagavad-Gita-700-titles.zip` passed a byte-identical
  `diff -r` round trip. No other batch or Phase 2 item was started.


- **2.1 batch 15 done — chapters 9+10 (2026-10-11).** PR #25 from batch 14
  was verified merged at `e09f31e`; Appendix A and the full pre-edit §4 build
  were reproduced before touching source. All 34 + 42 verses were read word by
  word against Sanskrit, pāda splits and en/ne/hi literals. **103 five-field
  NE/HI-only overrides** (19 ch9, 84 ch10) across 45 corrected verses; 30
  verses confirmed as-is with reasons; 9.34 flagged and left untouched. The
  exhaustive unchanged-occurrence ledgers list 426 + 478 = **904 occurrences**
  in `/home/user/evidence/batch15/chapter9-review-worksheet.md` and
  `chapter10-review-worksheet.md`. Appendix A is byte-identical before/after.
  The final full build is green; 206 structural rendered-string assertions and
  388 indexed mobile screenshots (12 full sheets, 188 changed-pāda contexts,
  188 crops) are in `/home/user/evidence/batch15/`. Reviewed ledger:
  **542/700**; remaining **158 verses** in chapters 1, 5, 12, 13 and 17. No
  second batch or other Phase 2 work started. The open source/interpretation
  holds remain in `/home/user/evidence/batch15/holds.json` and §6; the additive
  `tathā` carries in chapters 9 and 10 are resolved. Implementation commit
  `f36602a` is pushed only to the assigned branch; [PR #26](https://github.com/chapain/Bhagavad-Gita/pull/26)
  is open to `main` for Dhruba to review and merge.

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

- **FIXED (2.1 batch 1, 2026-10-09).** `te` = “they” was rendered तिम्रो/तुम्हारा
  (“your”) in 26 verses; they now read तिनीहरू / वे. The verses: 1.33, 2.6, 3.13,
  3.31, 5.19, 5.22, 7.12, 7.14, 7.28–30, 8.17, 9.20–21, 9.23–24, 9.29, 9.32,
  10.10, 12.2, 12.4, 12.20, 13.25, 13.34, 16.8, 16.17.
- **FIXED (2.1 batch 2, 2026-10-09).** `me` = “to me” rendered मेरो/मेरा where the
  sense is tell / show / offer *to me*: 2.7, 5.1, 9.26, 11.4, 11.45. Those now
  carry `["मे", "me", "to me", "मलाई", "मुझे"]` — the corpus dative, already used 9×
  for “to me” via `mām`.
  - **6.30 also fixed.** It was the borderline one: *sa ca me na praṇaśyati*,
    “he is not lost to me”. The owner left the call to craft (2026-10-09). The
    possessive मेरो made the pāda read “my … is not lost”, which the verse does
    not say, so it follows the same dative as the rest of the batch. Argument
    *for* keeping it: the parallel pāda renders तस्य (“for him”) as त्यसको. If a
    future session flips 6.30 back, audit §3 returns to 11 verses.
  - Not errors, kept: *sa me priyaḥ* (12.14–20, 18.64–69), where मेरो प्रिय is good
    Nepali, and 9.29 (*na me dveṣyo ’sti*). Audit §3 `me`: 16 → 10 verses.
  - In 11.45, *mano me* (“my mind”) and *darśaya me* (“show to me”) both became
    मेरो while the English was right for both. *mano me* now has its own
    five-field entry `["मे", "me", "my", "मेरो", "मेरा"]` beside *darśaya me*’s
    मलाई / मुझे, so the two occurrences no longer share one form.
- **FIXED (2.1 batch 2).** `param` “hereafter” rendered परम (“supreme”) in 2.12;
  now `["परम्", "param", "hereafter", "भविष्यमा", "भविष्य में"]`, matching the verse’s
  own ne/hi literal (“भविष्यमा पनि…” / “भविष्य में भी…”). 2.59 keeps परम (“the
  Supreme”) — correct there.
- **FIXED (2.1 batch 2).** `bhūtāni` “spirits” rendered प्राणीहरू (“living beings”)
  in 9.25; now भूतहरू / भूत, matching भूतेज्याः → भूतपूजकहरू in the same pāda and the
  verse’s literal (“भूतका पूजक भूतमा” / “भूतों के पूजक भूतों को”). 9.5 / 9.6 keep
  प्राणीहरू (“beings”) — correct there.
- **PARTLY FIXED (2.1 batch 2).** `yogam` rendered योग (“traditional but opaque”)
  in 10.7 and 11.8. **11.8 fixed** → `["योगम्", "yogam", "sovereignty", "ऐश्वर्य",
  "ऐश्वर्य"]`: the English says “sovereignty” *and* the verse’s own ne/hi literal
  says “मेरो दिव्य ऐश्वर्य हेर” / “मेरा दिव्य ऐश्वर्य देख”, so योग contradicted both on
  the same sheet. **10.7 deliberately kept as योग**: its ne *and* hi literals say
  “मेरो यो विभूति र योगलाई…” / “मेरी इस विभूति और योग को…”, so योग is the consistent
  reading there; making it शक्ति would set the word list against its own literal.
  Note 9.5 has the identical phrase *paśya me yogam aiśvaram* with en “yoga” and
  योग in its literal — per-verse five-field entries are exactly why 9.5 and 11.8
  may differ.

- **FIXED (2.1 batch 3, 2026-10-09) — `tat`.** 3.01 “then” now uses
  `त्यसो भए / तो`; 17.23 and 17.25 “Tat” in *oṃ tat sat* use `तत् / तत्`,
  preserving the mantra syllable rather than translating it as “that”.
  **Deliberately kept:** the 73 “that” entries, whose `tat` is demonstrative or
  correlative; 14.07 and 14.08 “it”, where `tat` is anaphoric; and 3.02, where
  `tad ekam` means “that one [thing]” and `त्यो / वह` follows the Sanskrit,
  although the existing English word gloss says “therefore”. The English gloss
  remains unchanged and that mismatch is out of scope.
- **FIXED (2.1 batch 3, 2026-10-09) — `yat`.** 1.45 “because” → `किनभने / क्योंकि`;
  15.06 “where” → `जहाँ / जहाँ`; both 15.08 “when / and when” → `जब / जब`;
  2.07 and 13.03×3 “what” → `के / क्या`; 17.03 “as his” → `जस्तो / जैसी`,
  matching “जस्तो उसको श्रद्धा / जैसी उसकी श्रद्धा”. **Judgement calls:** the
  11 “whatever” entries at 3.21×2, 9.27×5, 10.41×2, 11.07 and 11.42 were
  checked individually. Nepali becomes `जे` at 3.21, 9.27, 11.07 and 11.42,
  matching those literals; 10.41 keeps `जुन` in `जुन-जुन प्राणी`. Hindi keeps
  `जो` throughout, matching `जो / जो-जो` in the verse renderings. 18.60 “what”
  keeps `जुन / जो`: it is a relative clause, not a question. All 55 “which” uses
  keep `जुन / जो` as relative pronouns. The `11.07` “whatever” entry is the
  eleventh instance (omitted from the initial parenthetical list).

**FIXED (2.1 batch 4, 2026-10-10) — `bhīma`, `kutaḥ`, `sattvam`.** All 19
occurrences were checked against their own pāda, English word gloss and verse
literal; six entries changed (word[0–2] untouched):

| Verse | Form / English | Old NE / HI | New NE / HI |
|---|---|---|---|
| 1.04 | `bhīma` “to Bhīma” (equal to Bhīma and Arjuna) | भयानक / भयंकर | भीमसँग / भीम से |
| 1.10 | `bhīma` “by Bhīma” (force guarded by him) | भयानक / भयंकर | भीमले / भीम द्वारा |
| 2.02 | `kutaḥ` “whence” (where from?) | कसरी / कैसे | कहाँबाट / कहाँ से |
| 10.41 | `sattvam` “being” (glorious one) | सत्त्व / सत्त्व | प्राणी / प्राणी |
| 13.26 | `sattvam` “being” (moving or unmoving) | सत्त्व / सत्त्व | प्राणी / प्राणी |
| 18.40 | `sattvam` “being” (any entity under the guṇas) | सत्त्व / सत्त्व | जीव वा जड वस्तु / जीव या जड़ वस्तु |

**Deliberately left alone (13 instances):** `bhīma` 1.15 (“terrific”,
भयानक/भयंकर fits *bhīmakarmā*); `kutaḥ` 2.66 (“where”, but the verse says
“how can there be happiness?”, so कसरी/कैसे follows the literal), 4.31
(“how then”), 11.43 (“how then”); `sattvam` 10.36 (“goodness”, सत्त्व),
14.05, 14.06, 14.09, 14.10×3, 14.11 and 17.01 (all refer to the sattva
guṇa). The English word gloss in 2.66 stays out of scope. 18.40’s broader
rendering follows Śaṅkara’s *sattvam* = “entity, living creatures … or
non-living things” (https://www.bhagavad-gita.us/bhagavad-gita-18-40/);
10.41 and 13.26 follow their existing ne/hi literals (“प्राणी”). Owner
delegated the choices to editorial judgement after requesting research.

**FIXED (2.1 batch 5, 2026-10-11) — `arjuna`, `samāḥ`.** Dhruba reported
1.04 pāda 2. The word split and each word's English gloss were checked against
the Sanskrit verse and all three verse literals. The English literal says
“equals of Bhīma and Arjuna in war”; Nepali says “युद्धमा भीम र अर्जुनका समान”;
Hindi says “युद्ध में भीम और अर्जुन के समान”. Two context-specific entries were
added inline to `padachheda_ch1.py`; only word[3] and word[4] changed:

| Verse | Form / English | Old NE / HI | New NE / HI |
|---|---|---|---|
| 1.04 | `arjuna` “and Arjuna” | हे अर्जुन / हे अर्जुन | र अर्जुन / और अर्जुन |
| 1.04 | `samāḥ` “equal” | वर्षहरू / वर्ष | समान / समान |

All four entries of the pāda were checked in order: `bhīma` “to Bhīma” keeps
the batch-4 `भीमसँग / भीम से`; `arjuna` “and Arjuna” now follows the local
coordination; `samāḥ` “equal” no longer receives the shared “years” gloss; and
`yudhi` “in war” correctly remains युद्धमा / युद्ध में. Sanskrit word forms,
English word glosses, verse text, pādas, literals and paraphrases are unchanged.

**Deliberately left alone (23 occurrences of the two forms reviewed):**
`samāḥ` 6.41 means “years” and correctly keeps `वर्षहरू / वर्ष`. `arjuna` at
2.02, 2.45, 3.07, 4.05, 4.09, 4.37, 6.16, 6.32, 6.46, 7.16, 7.26, 8.16,
8.27, 9.19, 10.32, 10.39, 10.42, 11.47, 11.54, 18.09, 18.34 and 18.61 is
vocative “O Arjuna”; `हे अर्जुन` remains correct. 1.04 is the sole `arjuna`
occurrence glossed “and Arjuna”.

Appendix A §3 remains `te` = 0 verses / `me` = 10 verses before and after;
9,366 verse words and 9,484 total glosses are unchanged. The full Playwright
build passed all 162 browser checks. Six 390 × 844 Nepali/Hindi screenshots
were read back for 1.04, 2.02 and 10.41 (chapters 1, 2 and 10); 1.04 shows
both new meanings, while 2.02 and 10.41 show the settled batch-4 overrides as
cross-chapter render checks. Small boxed toolbar labels are a sandbox font
artifact, not a content issue. Generated churn: `data/ch1.js`, `sw.js` cache
id, and `sitemap.xml` lastmod dates (2026-10-11).

**FIXED (2.1 batch 6, 2026-10-11) — `me` = "to me" cleanup.** Each of the
10 audit-flagged verses was checked against its Sanskrit text and own en/ne/hi
literal translation. 9 entries across 8 verses needed NE मेरो→मलाई /
HI मेरा→मुझे:

| Verse | Form / English | Old NE / HI | New NE / HI |
|---|---|---|---|
| 12.14 | `me` "to me" | मेरो / मेरा | मलाई / मुझे |
| 12.15 | `me` "to me" | मेरो / मेरा | मलाई / मुझे |
| 12.16 | `me` "to me" | मेरो / मेरा | मलाई / मुझे |
| 12.17 | `me` "to me" | मेरो / मेरा | मलाई / मुझे |
| 12.19 | `me` "to me" | मेरो / मेरा | मलाई / मुझे |
| 12.20 | `me` "to me" | मेरो / मेरा | मलाई / मुझे |
| 18.64 | `me` "to me" | मेरो / मेरा | मलाई / मुझे |
| 18.65 | `me` "to me" | मेरो / मेरा | मलाई / मुझे |
| 18.69 | `me` "to me" (pāda 2) | मेरो / मेरा | मलाई / मुझे |

**Deliberately left alone (2 entries in 2 verses):**
- 9.29 *na me dveṣyo'sti na priyaḥ* — the Nepali literal says "कोही मेरा प्रिय
  वा अप्रिय छैन" (possessive मेरा), not मलाई. Word NE=मेरो is correct.
- 18.69 pāda 1 *kaścinme priyakṛttamaḥ* — the Nepali literal says "मेरो सेवा
  गर्ने" (possessive मेरो), not मलाई. Word NE=मेरो is correct.

All 84 `mām` occurrences (all मलाई/मुझे), all 24 `mama` (all मेरो/मेरा), and
all 20 `mayi` (NE ममा / HI मुझमें, consistent with the verse translations)
were verified and left alone. Generated churn: `data/ch9.js`, `data/ch12.js`,
`data/ch18.js`, `sw.js` cache id.

**Fix path (no code change needed):** write five-field entries inline in
`padachheda_ch<N>.py`, e.g. `["ते", "te", "they", "तिनीहरू", "वे"]`. Batches
1–6 cover `te`, `me` (dative and possessive), `param`, `bhūtāni`, `yogam`,
`tat`, `yat`, `bhīma`, `kutaḥ`, `sattvam`, `arjuna` and `samāḥ`. Next:
the remaining forms in the 674-form pool; the owner picks each slice.

**FIXED (2.1 batches 7–9, 2026-10-11) — chapters 4, 14 and 16, verse by
verse.** One chapter per batch; all 93 verses were read with their en/ne/hi
literals and every word entry checked against the verse in context. 43
overrides were needed (24 / 8 / 11); 572 further flagged occurrences were read
and left alone (313 / 147 / 112), each listed verse by verse in the PR.
Only word[3] and word[4] changed in every case; the Devanagari, IAST and
English glosses are untouched.

| Verse | Form / English | Old NE / HI | New NE / HI | Why |
|---|---|---|---|---|
| 4.02 | `viduḥ` “knew” | जान्छन् / जानते हैं | जाने / जाना | literal जाने / जाना (past) |
| 4.03 | `te` “to you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | “I have declared this ancient yoga **to you**” |
| 4.04 | `aparam` “later” | अर्को / दूसरा | पछिको / पीछे का | *aparaṁ janma* = later birth |
| 4.04 | `bhavataḥ` “your” | उत्पन्न हुन्छन् / उत्पन्न होते हैं | तिम्रो / तेरा | global gloss is 14.17’s *bhava* sense |
| 4.04 | `param` “earlier” | परम / परम | पहिलेको / पहले का | *paraṁ janma* = earlier birth |
| 4.05 | `veda` “know” | जान्दछ / जानता है | जान्दछु / जानता हूँ | *aham veda* = 1sg |
| 4.06 | `san` ×2 “being” | भएको / हुआ हुआ | भएको / होते हुए | हुआ हुआ was ungrammatical |
| 4.06 | `adhiṣṭhāya` “resorting to” | अधिकार गरेर / अधिष्ठित होकर | आश्रय गरेर / अधिष्ठित होकर | अधिकार = authority, wrong sense |
| 4.06 | `ātma` “my own” | आत्मा / आत्मा | आफ्नै / अपनी | *ātma-māyayā* = my own māyā |
| 4.08 | `yuge` ×2 “in age / after age” | युगपछि / युग-युग | युग-युगमा / युग-युग | *yuge yuge* = age after age |
| 4.16 | `te` “to you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | “I shall tell **to you**” |
| 4.18 | `paśyet` “sees” | देख्थ्यो / देखता | देख्छ / देखता | potential, not past-habitual |
| 4.21 | `sarva` “all” | हे सबै / हे सब | सबै / सब | stray vocative particle |
| 4.22 | `yadṛcchā` “by chance, unsought” | आफैं / अनायास | अनायास / अनायास | आफैं = “by itself” |
| 4.25 | `paryupāsate` “worship, serve” | अनुसरण गर्छन् / अनुसरण करते हैं | पूजा गर्छन् / पूजा करते हैं | “worship with sacrifice” |
| 4.34 | `sevayā` “by service” | अभ्यासद्वारा / अभ्यास से | सेवाद्वारा / सेवा से | अभ्यास = practice, wrong sense |
| 4.34 | `te` “you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | “will teach **you**” |
| 4.34 | `jñāninaḥ` “the wise” | ज्ञानीका / ज्ञानी के | ज्ञानीहरू / ज्ञानी | तत्त्वदर्शिनः plural, nominative |
| 4.36 | `tamaḥ` “the worst” | तम / तम | सबैभन्दा / सबसे | *tamaḥ* here is the superlative suffix |
| 4.40 | `paraḥ` “the next” | परम / परम | परलोक / परलोक | *para-loka* sense |
| 4.42 | `enam` “this” | उसलाई / उसे | यसलाई / इसे | *enam* is near-deictic |
| 14.03 | `tataḥ` “from that” | त्यसैले / इसलिए | त्यसबाट / उसी से | “born **from that**” |
| 14.06 | `tatra` “of these” | त्यहाँ / वहाँ | तीमध्ये / उनमें | locative of the three guṇas |
| 14.14 | `tu` “indeed” | तर / पर | नै / ही | emphatic, not adversative |
| 14.16 | `rajasaḥ` “of rajas” | रजबाट / रज से | रजको / रज का | *rajasaḥ phalam* = fruit of rajas |
| 14.17 | `tamasaḥ` “of tamas” | तमको / तम का | तमबाट / तम से | ablative: “knowledge arises **from** tamas” |
| 14.19 | `guṇebhyaḥ` “than the guṇas” | गुणभन्दा पर / गुणों से परे | गुणहरूबाहेक / गुणों के अतिरिक्त | “no doer **other than** the guṇas” |
| 14.19 | `param` “what is beyond” | परम / परम | परको / परे का | *guṇebhyaḥ param* |
| 14.23 | `vartante` “act” | रहन्छन् / रहते हैं | क्रियाशील छन् / कर्म करते हैं | the guṇas act, the witness does not |
| 16.03/16.04 | `sampadam` “the endowment” | सम्पत्तिमा / सम्पदा को | सम्पत्ति / सम्पदा को | accusative object of भवन्ति |
| 16.06 | `me` “from me” | मेरो / मेरा | मबाट / मुझसे | *śṛṇu me* = “hear **from me**” |
| 16.07 | `nivṛttim` “renunciation” | अकर्म / अकर्म | नगर्नुपर्ने / अकर्तव्य | विधि = what should not be done |
| 16.10 | `pravartante` “they act” | सुरु हुन्छन् / आरम्भ होते हैं | कर्म गर्छन् / कर्म करते हैं | प्रवृत्ति = engaging in action |
| 16.15 | `mayā` “me” | मद्वारा / मेरे द्वारा | मजस्तो / मेरे समान | *sadṛśaḥ mayā* = “like me” |
| 16.17 | `yajante` “they perform sacrifices” | पूजा गर्छन् / पूजते हैं | यज्ञ गर्छन् / यज्ञ करते हैं | यज्ञ, not general worship |
| 16.20 | `janmani` ×2 “in birth / after birth” | जन्मपछि / जन्म के बाद | जन्म-जन्म / जन्म-जन्म | *janmani janmani* = birth after birth |
| 16.21 | `tathā` “and” | त्यसरी / वैसे ही | र / और | joining a list of three |
| 16.23 | `vartate` “acts” | रहन्छ / रहता है | कर्म गर्छ / कर्म करता है | अशास्त्रविधि = acts by desire |

**Deliberately left alone (572 flagged occurrences read in full; per-verse
list in the PR):** the shared forms that stay correct in these three chapters
are led by `na` (ch4 14), `api` (10), `karma` (10), `eva` (8), `jñāna` (8),
`brahma` (7), `saḥ` (6), `mām` (6), `apare` (6), `karma`/`karmāṇi`,
`juhvati`, `yajñāḥ`, `iti`, `hi`, `yaḥ`, `tathā`, `jñātvā`, `iha`, `agnau`,
`yoga`, `jñānam`, and in ch14/ch16 `guṇa`, `prakṛti`, `kāma`, `krodha`,
`lobha`, `buddhi`, `ātmā`, `śraddhā` and the whole demoniac catalogue
(`dambha`, `darpa`, `krodha`, `pāruṣya`, `ajñāna`, `aśuci`, `narādhamāḥ` …),
where the shared one-meaning-per-form gloss already follows the verse. Two
structural faults found while reading are **not** word-gloss changes and are
flagged for the owner rather than fixed: 4.09 `eti`’s English gloss “goes”
against the verse’s own *naiti māmeti* (“he comes to me”) — its Nepali/Hindi
are correct; 4.42 `ātmanaḥ`
“of the Self” vs आत्माको; 16.10 `mada`’s shared NE gloss carries a stray
parenthetical, “घमण्ड (ले)”; 16.13–14 `abhimāna` is inside the compound
*abhimānāśrayaṁ* and is not split as its own word.

**FIXED (2.1 batch 10, 2026-10-11) — chapter 18 verse by verse.** All 78
verses were read with their en/ne/hi literals; 20 overrides (word[3]/word[4]
only), ~460 further flagged occurrences read and left alone. The fixes and
why:

| Verse | Form / English | Old NE / HI | New NE / HI | Why |
|---|---|---|---|---|
| 18.02 | `kavayaḥ` “the wise” | कविहरू / कवि | ज्ञानीहरू / ज्ञानी | कवि = poets; the literal says ज्ञानी |
| 18.08 | `tyajet` “one gives up” | त्याग्नुपर्छ / त्यागे | त्याग्छ / त्यागता है | descriptive, not “must”; HI literal present |
| 18.08 | `labhet` “gains” | पाउँथ्यो / पाता | पाउँछ / पाता | past-habitual vs the verse’s present |
| 18.13 | `me` “from me” | मेरो / मेरा | मबाट / मुझसे | *nibodha me* = learn from me |
| 18.14 | `tathā` “and” | त्यसरी / वैसे ही | र / और | list conjunction, not “thus” |
| 18.22 | `kṛtsnavat` “as if the whole” | सबै होइनझैं / सब कुछ की तरह | सबैझैं / सब कुछ की तरह | NE said the opposite (“as if not all”) |
| 18.36 | `me` “from me” | मेरो / मेरा | मबाट / मुझसे | *śṛṇu me* = hear from me |
| 18.40 | `ebhiḥ` “from these” | यिनीहरूद्वारा / इनसे | यिनीहरूबाट / इनसे | ablative “free from”, not instrumental |
| 18.42 | `brahmakarma` “duty of the brāhmaṇa” | ब्रह्मको कर्तव्य / ब्राह्मण का कर्तव्य | ब्राह्मणको कर्तव्य / ब्राह्मण का कर्तव्य | NE said “of Brahman” |
| 18.46 | `pravṛttiḥ` “the origin” | प्रवृत्ति / प्रवृत्ति | स्रोत / स्रोत | प्रवृत्ति = tendency; literal says स्रोत |
| 18.50 | `me` “from me” | मेरो / मेरा | मबाट / मुझसे | *nibodha me* = learn from me |
| 18.63 | `te` “to you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | *ākhyātaṃ te* = declared to you |
| 18.64 | `iṣṭaḥ` “dear” | पूजित / पूजित | प्रिय / प्रिय | 18.70 keeps पूजित (“worshipped”) |
| 18.65 | `te` “to you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | *satyaṃ te pratijāne* |
| 18.67 | `te` “by you” | तिम्रो / तुम्हारा | तिमीद्वारा / तुम्हारे द्वारा | gerundive agent, not possessive |
| 18.69 ×2 | `tasmāt` “than him” | त्यसकारण / इसलिए | उसभन्दा / उससे | ablative of comparison |
| 18.70 | `matiḥ` “opinion” | बुद्धि / बुद्धि | मत / मत | intellect ≠ opinion; 18.06 `matam` is मत |
| 18.78 | `matiḥ` “judgment” | बुद्धि / बुद्धि | मत / मत | same as 18.70 |
| 18.78 | `bhūtiḥ` “glory” | समृद्धि / समृद्धि | वैभव / वैभव | collided with `śrīḥ` (also समृद्धि) |

**Deliberately left alone:** `me` possessive 18.04 / 18.06 / 18.64 / 18.70 /
18.77 (मेरो/मेरा matches each literal); `mayi` 18.68 (ममा, settled in batch 6);
`tathā` correlative 18.50 / 18.63; `niṣṭhā` 18.50 (protected by §7.1); `padam`
स्थान (corpus-consistent with 2.51 / 15.04 / 15.05); `te` possessive 18.59 /
18.64 / 18.72; `iṣṭaḥ` 18.70 (“worshipped”, matches its literal); `tasmāt`
“therefore” elsewhere correct.

**Owner flags from batch 10 (not fixed, out of a word-gloss change):** 4.16
carries the *same* `kavayaḥ` = “poets” defect as 18.02 — left for the chapter-4
revisit because the standing rule is one chapter per batch (evidence in the
batch-10 screenshots); 18.53’s ne/hi *literals* render *nirmamaḥ* backwards
(“not giving up ‘mine’”) while the word gloss निर्मम is right; shared forms
`tathā` “also/and” (chs 1, 7–11, 13, 17), `matiḥ` 6.36 and `pravṛttiḥ` 15.04
still need their per-occurrence overrides in their own chapter batches.

**FIXED (2.1 batch 11, 2026-10-11) — chapter 2 verse by verse.** All 72
verses read with en/ne/hi literals; 69 overrides (word[3]/word[4] only) in
41 verses, 31 verses confirmed as-is. The fixes and why (×N = same fix at
N spots in the verse):

| Verse | Form / English | Old NE / HI | New NE / HI | Why |
|---|---|---|---|---|
| 2.03, 2.47×3 | `mā` “not” | नगर / मत | न / मत | नगर = “don’t do”; verbs are go/be |
| 2.05 | `śreyaḥ` “better” | कल्याण / कल्याण | राम्रो / अच्छा | comparative, not noun “welfare” |
| 2.06 | `naḥ` “for us” | हामी / हम | हामीलाई / हमें | dative, not nominative |
| 2.06 | `dhārtarāṣṭrāḥ` | धृतराष्ट्र का पुत्रहरूले / … | धृतराष्ट्रका पुत्रहरू / … | Hindi का + stray ergative ले |
| 2.12 | `bhaviṣyāmaḥ` “shall we exist” | हुने थियौं / होंगे | हुनेछौं / होंगे | हुने थियौं ungrammatical |
| 2.12 | `ataḥ` “from now” | त्यसैले / इसलिए | अबदेखि / अब से | temporal, not “therefore” |
| 2.15 | `yam` “whom” | जुन / जिसे | जसलाई / जिसे | person accusative, literal जसलाई |
| 2.19×2, 2.21, 2.23×3, 2.25, 2.26, 2.29×3 | `enam` “this” | उसलाई / उसे | यसलाई / इसे | near-deictic; 2.23 literals say यसलाई/इसे |
| 2.19 | `vijānītaḥ` “know” | जान / जानो | जान्दछन् / जानते हैं | imperative → 3rd-pl indicative |
| 2.20, 2.35 | `bhūtvā` “having been” | भएर / बनकर | भएर / होकर | बनकर = “having become” (cf. 2.48 kept) |
| 2.21 | `nityam` “eternal” | सधैँ / सदा | नित्य / नित्य | adjective, not adverb (cf. 2.26/30 kept) |
| 2.26, 2.33 | `atha` “but” | अनि / फिर | तर / किन्तु | “and/then” ≠ but; literals तर/किन्तु |
| 2.27 | `dhruvam` “certain” | नित्य / नित्य | निश्चित / निश्चित | certain ≠ eternal; literal निश्चित |
| 2.28×2 | `avyakta` “unmanifest” | अव्यक्तलाई / अव्यक्त को | अव्यक्त / अव्यक्त | compound member, not dative |
| 2.28 | `madhyāni` “in the middle” | मध्यका / मध्य के | बीचमा / मध्य में | locative, not genitive |
| 2.31 | `śreyaḥ` “better” | कल्याण / कल्याण | उत्तम / बढ़कर | comparative; literal उत्तम/बढ़कर |
| 2.33 | `tataḥ` “then” | त्यसैले / इसलिए | त्यसपछि / तो | if…then correlative; HI literal तो |
| 2.33, 2.38, 2.53 `avāpsyasi` + 2.37 `prāpsyasi` | “you will …” | … / प्राप्त होगा | … / प्राप्त करोगे | passive “will be obtained” → active 2nd-ps |
| 2.34 | `bhūtāni` “people” | प्राणीहरू / प्राणी | मानिसहरू / लोग | literals मानिसहरू/लोग |
| 2.34 | `atiricyate` “is greater” | बढी हुन्छ / श्रेष्ठ होता है | बढी हुन्छ / अधिक होता है | श्रेष्ठ = “best”, wrong polarity |
| 2.35 | `uparatam` “retreated” | शान्त / शान्त | भागेको / भागा हुआ | peaceful ≠ fled; literal भागेको |
| 2.36 | `tataḥ` “than that” | त्यसैले / इसलिए | त्योभन्दा / उससे | ablative of comparison |
| 2.38 | `duḥkhe` “pain” | दुःखमा / दुःख में | दुःख / दुःख | accusative dual, not locative |
| 2.38 | `alābhau` “and loss” | अलाभमा / अलाभ में | हानि / हानि | locative + non-gain ≠ loss; literal हानि |
| 2.38 | `ajayau` “and defeat” | पराजयमा / पराजय में | पराजय / पराजय | accusative dual, not locative |
| 2.38 | `tataḥ` “then” | त्यसैले / इसलिए | त्यसपछि / तब | sequential; literals त्यसपछि/तब |
| 2.38 | `yujyasva` “engage” | समर्पित होऊ / समर्पित हो | लाग / लग जा | engage in battle ≠ devote (cf. 2.50 kept) |
| 2.39 | `te` “to you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | dative; literal तिमीलाई |
| 2.39, 2.42 | `imām` “this” (f.acc) | यो / इस | यो / यह | direct object, not oblique |
| 2.40 | `bhayāt` “fear” (from) | डरले / भय से | डरबाट / भय से | separation, not cause (cf. 2.35 kept) |
| 2.42 | `yām` “which” (f.acc) | जुन / जिस | जुन / जिसे | accusative relative, not oblique |
| 2.45 | `niryogakṣemaḥ` | लाभ-हानिभन्दा पर / … | लाभ-स्वामित्वभन्दा पर / … | kṣema = keeping, not loss (हानि) |
| 2.49 | `anviccha` “seek” | खोज / चाह | खोज / खोज | चाह = “want”; HI literal खोज |
| 2.49 | `phalahetavaḥ` “motive-seeking” | फलको खोजी गर्ने / फल के कारण | फलको खोजी गर्ने / फल चाहने वाले | persons, not “because of fruit” |
| 2.50 | `duṣkṛte` “and bad deeds” | दुष्कर्ममा / दुष्कर्म में | दुष्कर्म / दुष्कर्म | accusative dual, not locative |
| 2.54×2 | `kim` “how” | के / क्या | कसरी / कैसे | interrogative of manner; literals agree |
| 2.55, 2.71 | `sarvān` “all” | सबैलाई / सबको | सबै / सब | accusative, not dative/genitive |
| 2.58 | `sarvaśaḥ` “from all sides” | सबै प्रकारले / सब प्रकार से | चारैतिरबाट / चारों ओर से | spatial; literals agree (cf. 2.68 kept) |
| 2.59 | `nivartate` “departs” | फर्कन्छ / लौटता है | जान्छ / चला जाता है | both said “returns” — backwards |
| 2.60 / 2.67 | `haranti`/`harati` “carry away” | बोक्छन्/बोक्छ / … | लैजान्छन्/लैजान्छ / … | shoulder-carry ≠ seize away; literal हरेर लैजान्छ |
| 2.61 | `tāni` “them” | ती / वे | तिनीहरूलाई / उन्हें | accusative, not nominative |
| 2.64 | `ātmavaśyaiḥ` “self-controlled” | आत्मसंयमीहरूद्वारा / आत्म-संयमी | आत्मवश / आत्म-संयमी | qualifies senses, not “by people” |
| 2.65 | `sarva` “of all” | हे सबै / हे सब | सबै / सब | stray vocative (same as 4.21) |
| 2.70 | `yam` “whom” | जुन / जिसे | जसमा / जिसमें | destination “into whom”; literals agree |
| 2.71 | `carati` “moves” | गर्छ / करता है | विचरण गर्छ / विचरता है | “does” ≠ moves; literals agree |
| 2.72 | `sthitiḥ` “the state” | स्थिरता / स्थिरता | अवस्था / अवस्था | state ≠ steadiness; literals अवस्था |

**Deliberately left alone in ch2 (every other word read):** the settled
keeps above plus `te` possessive (2.07/34/47/52/53) and “they” 2.06,
`tathā` thus/so, `tat`/`yat`/`kutaḥ`/`param`/`yogam`/`me` from batches
1–4, `yadṛcchayā` “of its own accord” 2.32 (आफैं fits this sense, unlike
4.22), `kaśmalam` मोह 2.02 (Skt मोह = swoon/faintness), `tu` तर/पर where
the verse is adversative although EN says “indeed” (2.05/14/17/64),
`arth`e/`vedeṣu`/`śarīre`/`muneḥ`/`duḥkhānām`/`asya` where NE/HI case is
right although the EN gloss is loose, `manogatān` मनका 2.55 and `manāḥ`
जसको मन 2.56 (match literals), `saṁharate` तान्छ 2.58, `gatim` गति 2.43,
`antaḥ` अन्त्य 2.16, `cetasām` 2.44, `viṣayāḥ`/`bhava` 2.45, `arhasi`
योग्य 2.25–31 (not-proper ≈ ought-not), and the 2.54 optatives (literals
use present). EN-gloss slips are out of scope and preserved.

**Owner flags from batch 11 (not fixed, out of chapter scope):** `mā` →
नगर (“don’t do”) is wrong in *every* occurrence — 11.34 (*mā
vyathiṣṭhāḥ*), 11.49×2, 16.05 and 18.66 (*mā śucaḥ*) — none pairs with a
“do” verb; ch16/18 passed verse-by-verse review without catching it, so
all five need revisit-batch overrides to न/मत. `śucaḥ`’s indicative शोक
गर्छौ/शोक करता है (16.05/18.66, imperative “grieve!” under *mā*) belongs
to the same revisit. EN-only slips preserved: `tu` “indeed” for
adversative but (2.05/14/17/64), 2.57 `dveṣṭi` “reviles” (hates), and the
loose nominative EN glosses listed above.

**FIXED (2.1 batch 12, 2026-10-11) — chapters 11 and 15 verse by verse.**
All 55 verses of ch 11 and all 20 of ch 15 read with en/ne/hi literals;
62 overrides in 37 ch11 verses (18 confirmed as-is) and 10 in 8 ch15
verses (12 confirmed as-is); word[0–2], EN glosses, verse text, pādas and
paraphrases untouched. Chapter 11 (×N = same fix at N spots):

| Verse | Form / English | Old NE / HI | New NE / HI | Why |
|---|---|---|---|---|
| 11.01 | `mat` “by my” | मेरो / मेरा | मलाई / मुझे | *mad-anugrahāya* = grace *toward me*; NE literal दयाले…तिमीलाई |
| 11.02 | `bhava` “of coming into being” | होऊ / बनो | उत्पत्ति / उत्पत्ति | noun “origin” in *bhavāpyayau*, not imperative “be!” |
| 11.03, 11.04 | `ātmānam` “yourself” | आत्मालाई / आत्मा को | आफूलाई / अपने को | reflexive accusative “yourself”, not “the Self” |
| 11.04 | `manyase` “you think” | सोच्छौ / सोचता है | सोच्छौ / सोचते हो | 2nd person; HI had 3rd |
| 11.04 | `tataḥ` “then” | त्यसैले / इसलिए | त्यसपछि / तो | if…then correlative (cf. 2.33) |
| 11.05, 11.40 | `atha` “and” | अनि / फिर | र / और | “and”, not “then/afterwards” |
| 11.05 | `sahasraśaḥ` “by thousands” | हजारौं / हज़ारों से | हजारौं / हज़ारों | distributive “by thousands”; से reads as source |
| 11.06, 11.26 | `tathā` “also” | त्यसरी / वैसे ही | पनि / भी | additive “also”, not “thus” |
| 11.07 | `adya` “now” | आज / आज | अब / अब | discourse “now”, not calendar “today” |
| 11.07 | `icchasi` “you wish” | चाहन्छौ / चाहता है | चाहन्छौ / चाहते हो | 2nd person |
| 11.08, 11.31, 11.37, 11.39×2, 11.40×2, 11.49 | `te` “to you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | dative (cf. 2.39, 4.03); possessive kept elsewhere |
| 11.09, 11.14 | `tataḥ` “then” | त्यसैले / इसलिए | त्यसपछि / तब | sequential (cf. 2.38); literals agree at 11.14 |
| 11.11 | `devam` “the God” | देवतालाई / देव को | देवता / देव | accusative object of *paśyāmi*, not dative |
| 11.12 | `divi` “in the sky” | स्वर्गमा / स्वर्ग में | आकाशमा / आकाश में | physical sky of a thousand suns; literals आकाश |
| 11.12 | `bhāsaḥ` “the splendour” | किरणहरू / किरणें | तेज / तेज | splendour ≠ rays (11.30 “the rays” kept किरण) |
| 11.15, 11.44, 11.45 | `deva` “O God” | देवताका / देवों के | हे देवता / हे देव | vocative; old gloss was genitive “of the gods” |
| 11.15 | `tathā` “and” | त्यसरी / वैसे ही | र / और | conjunctive in a list |
| 11.15 | `īśam` “the Lord” | हे प्रभु / हे प्रभु | प्रभुलाई / ईश को | accusative object of *paśyāmi*, not vocative |
| 11.17 | `aprameyam` “immeasurable” | हे अप्रमेय / हे अप्रमेय | अप्रमेय / अप्रमेय | stray vocative हे on a predicate |
| 11.18 | `me` “by me” | मेरो / मेरा | मबाट / मुझसे | ablative agent of *mataḥ* “deemed by me” |
| 11.19 | `tapantam` “burning” | बल्ने / जलता हुआ | पोल्ने / जलाता हुआ | transitive “scorching the world”; literals transitive |
| 11.20 | `dyāvāpṛthivyoḥ` “of heaven and earth” | स्वर्ग र पृथ्वीको / स्वर्ग और पृथ्वी का | आकाश र पृथ्वीको / आकाश और पृथ्वी का | sky-and-earth of the vision; literals आकाश |
| 11.20 | `antaram` “space between” | भेद / भेद | बीचको स्थान / बीच का स्थान | भेद = “difference”; here the spatial interval |
| 11.21, 11.26 | `tvām` “into you / you” | तिमीलाई / तुम्हें | तिमीमा / तुममें | goal of *viśanti* “they enter” = locative |
| 11.22 | `uṣmapāḥ` “the ancestors” | उष्मापाहरू / उष्माप | पितृहरू / पितर | opaque transliteration; literals say पितृ |
| 11.24 | `pravyathitāntarātmā` | काँप्दो हृदय भएको / काँपते हृदय वाला | काँप्ने हृदय भएको / काँपते हृदय वाला | काँप्दो is not a Nepali form; HI unchanged |
| 11.26 | `sūtaputraḥ` | सूतपुत्र / सूतपुत्र | सारथिको छोरा कर्ण / सारथि का पुत्र कर्ण | opaque; the verse means Karṇa, literals agree |
| 11.26 | `yodhamukhyaiḥ` | प्रमुख योद्धाहरूद्वारा / प्रमुख योद्धाओं से | प्रमुख योद्धाहरूसँग / प्रमुख योद्धाओं से | comitative “with”, not instrumental; HI kept |
| 11.28 | `nadīnām` “of the rivers” | नदीहरूका / नदियों में | नदीहरूका / नदियों की | genitive, not locative |
| 11.31 | `me` “me” | मेरो / मेरा | मलाई / मुझे | object of *ākhyāhi* “tell me” |
| 11.31 | `pravṛttim` “workings” | प्रवृत्ति / प्रवृत्ति | क्रियाहरू / गतियाँ | “your workings/movings”, not “tendency” (≠ 15.04) |
| 11.32 | `tvām` “you” (*ṛte*) | तिमीलाई / तुम्हें | तिमी / तेरे | *ṛte* + bare/oblique “without you” |
| 11.34 | `tathā` “also” | त्यसरी / वैसे ही | र / और | additive in a list (karṇaṃ tathā anyān) |
| 11.34 | `mā` “do not” | नगर / मत | न / मत | owner flag: नगर = “don’t do”; verb is *vyathiṣṭhāḥ* |
| 11.49×2 | `mā` “do not / nor” | नगर / मत | न / न | owner flag; nominal predicates (vyathā, vimūḍhabhāva) |
| 11.36 | `anurajyate` “is delighted” | रम्छ / रमता है | आनन्दित हुन्छ / रमता है | NE duplicated *prahṛṣyati*’s रम्छ; HI kept |
| 11.37 | `garīyase` “to the greater” | महान्लाई / महान् को | महानलाई / महान को | misspelt conjunct न्ल; orthography only |
| 11.37 | `brahmaṇaḥ` “than Brahmā” | ब्रह्मको / ब्रह्म का | ब्रह्माभन्दा / ब्रह्मा से | comparative ablative (cf. 18.69) |
| 11.39 | `prapitāmahaḥ` “the great grandsire” | पितामह / पितामह | महान् पितामह / महान् पितामह | *pra-* = “great”; literals say महान् पितामह |
| 11.41 | `prasabham` “rashly” | बलपूर्वक / बलपूर्वक | हतारमा / उतावली में | “in haste”, not “by force”; literals agree |
| 11.41 | `yat` “which” | जुन / जो | जे / जो | correlative with 11.42’s “whatever”; NE literal जे-जे; HI जो kept |
| 11.42 | `asi` “you were” | छौ / हो | थियौं / थे | past tense of “you were dishonoured” |
| 11.42 | `ekaḥ` “alone” | एक / एक | एक्लै / अकेले | “alone”, not the numeral “one” |
| 11.44 | `soḍhum` “to forgive” | सहन / सहन | क्षमा गर्न / क्षमा करना | “to bear” ≠ “to forgive”; literals agree |
| 11.47 | `tava` “to you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | dative of *darśitam tava*; literals agree |
| 11.51 | `prakṛtim` “to my own nature” | प्रकृतिलाई / प्रकृति को | स्वभावमा / स्वभाव में | own disposition, not nature-the-world; literals स्वभाव |
| 11.53 | `tapasā` “by austerity” | तपस्या / तपस्या से | तपस्याद्वारा / तपस्या से | NE alone lacked the instrumental its 3 siblings carry |

Chapter 15:

| Verse | Form / English | Old NE / HI | New NE / HI | Why |
|---|---|---|---|---|
| 15.03 | `enam` “this” | उसलाई / उसे | यसलाई / इसे | near-deictic “this aśvattha” (cf. batches 7/11) |
| 15.04 | `tataḥ` “then” | त्यसैले / इसलिए | त्यसपछि / तब | sequential “then seek”; literals agree |
| 15.04 | `pravṛttiḥ` “the course” | प्रवृत्ति / प्रवृत्ति | प्रवाह / धारा | owner flag: flowing course/stream per literals; ≠ 18.46’s स्रोत |
| 15.08 | `īśvaraḥ` “the lord” | ईश्वर / ईश्वर | स्वामी / स्वामी | the soul as lord *of the body*, not God; literals स्वामी (15.17 kept) |
| 15.11 | `acetasaḥ` “lacking understanding” | अचेतन / अचेत | समझ नभएका / समझ न होने वाले | अचेतन = “unconscious”; literals say समझ |
| 15.13 | `gām` “the earth” | पृथ्वीलाई / पृथ्वी को | पृथ्वीमा / पृथ्वी में | *āviśya* “entering” takes locative in NE/HI; literals agree |
| 15.14 | `vaiśvānaraḥ` “the fire of digestion” | वैश्वानर / वैश्वानर | पाचक अग्नि / पाचक अग्नि | opaque transliteration; literals पाचक अग्नि |
| 15.14 | `deham` “in the body” | शरीर / शरीर | शरीरमा / शरीर में | *āśritaḥ* + acc = dwelling *in*; literals locative |
| 15.15 | `sarvaiḥ` “all” | सबैले / सबसे | सबै / सबसे | instrumental with passive *vedyaḥ*; NE ले = agent clash |
| 15.17 | `uttamaḥ` “the highest” | उच्च / उच्च | परम / परम | superlative title; literals परम पुरुष (15.18 comparative kept) |

**Deliberately left alone in ch11/ch15 (every other word read):** the
settled keeps above plus correlative/quotative `tathā` (11.23/28/29/46)
and `iti` (11.04/21/41×2, 15.17, 15.20), possessive `te`/`tava`/`me`
(11.15/31/47 तिम्रो; 11.47 `me` “my” मेरो), `tvām` “of you” 11.44 and
`tena`/`caturbhujena` 11.46 (batch-11 2.43 principle), `devam` dative
11.14, imperative `bhava` 11.33, `arhasi` योग्य 11.44, `mayā` मद्वारा,
`pramādāt`, `viśvam` विश्व 11.19, `bhūyaḥ` फेरि 11.39, `prakīrtyā` 11.36,
voice-neutral infinitives `draṣṭum`/`jñātum`/`praveṣṭum` (11.04/47/53/54),
`śakyaḥ` सक्ने/सकता (11.48/53/54), optative `syāt` होला/हो (11.12, 15.20),
transliterated vocatives (janārdana, parantapa, kurupravīra, kaunteya),
Krishna register तिमी/तुम; in ch15 also `tathā` manner “thus” 15.03,
`padam` स्थान 15.04/05 (batch-10 settle), `nivartante` “they return” 15.06
(mirror of 2.59’s “departs” fix), `yat` relative/when/where (15.06/08/12),
`īśvaraḥ` divine sense 15.17 (mirror of 15.08’s fix), `enam` “him”
anaphoric 15.11×2, `adhiṣṭhāya` अधिकार 15.09 (mirror of 4.06’s fix),
comparative `uttamaḥ` 15.18, `tam` “it” 15.01, and EN-only slips (loose
“from which” for locative *yasmin* 15.04, “of you” for dative 11.44).

**Owner flags from batch 12 (not fixed):** the 11.44 **NE literal** renders
*praṇidhāya* as “शरीर थपथपाउँछु” (“I pat the body”) where the verse means
prostrating (HI literal पसारता is right) — a literal-level slip, not a word
gloss; left for Dhruba. Carry-forward list now shorter: `mā`/`śucaḥ`
16.05/18.66, `kavayaḥ` 4.16, `matiḥ` 6.36 and `tathā` “also/and” in chs
1, 7–10, 13, 17 (the ch11 and ch15 shares are fixed here; `pravṛttiḥ`
15.04 is fixed here).

**FIXED (2.1 batch 13, 2026-10-11) — chapters 3 and 7 (43 + 30 = 73 verses).** Every English, Nepali and Hindi literal and every speaker/pāda word entry was read against its context. The full worksheets below record every verse’s word list, the pre-change NE/HI meanings, the three literal translations, verdict and reason: `/home/user/evidence/batch13/chapter3-review-worksheet.md` and `chapter7-review-worksheet.md`. **51 inline five-field overrides** in `padachheda_ch3.py` and `padachheda_ch7.py` (32 + 19), touching only `word[3]` / `word[4]`; 38 verses have corrections, 6 of those also carry an explicit owner hold, 32 are fully confirmed without an override, and 3 are hold-only. Verse text, IAST, English glosses, padas, titles and paraphrases were untouched.

Chapter 3 changed-word table:

| Verse / word position | Form / English gloss | Old NE / HI | New NE / HI | Translation evidence and reason |
|---|---|---|---|---|
| 3.04 P2 #3 | `aśnute` “attains” | अनुभव गर्दछ / भोगता है | प्राप्त गर्छ / प्राप्त करता है | NE literal says the man does not `पाउँदैन` freedom from action; HI says `प्राप्त नहीं होता`. These support “attains/obtains”, not the old experiential `अनुभव गर्दछ` / “enjoys” `भोगता है`. |
| 3.08 P2 #4 | `akarmaṇaḥ` “than inaction” | अकर्मको / अकर्म का | अकर्मभन्दा / अकर्म से | The comparative is explicit: NE `कर्म अकर्मभन्दा श्रेष्ठ` and HI `कर्म अकर्म से श्रेष्ठ`; old genitive `अकर्मको / अकर्म का` did not mark “than”. |
| 3.08 P4 #3 | `akarmaṇaḥ` “through inaction” | अकर्मको / अकर्म का | अकर्मले / अकर्म से | This second occurrence is the means in `even the body’s maintenance is not [possible] through inaction`: NE `अकर्मले ... निर्वाह ... हुँदैन`, HI `अकर्म से ... निर्वाह ... नहीं`. The old genitive was wrong; the two occurrences need distinct case-appropriate senses. |
| 3.09 P2 #4 | `bandhanaḥ` “bound” | बाँध्ने / बाँधने वाला | बाँधिएको / बँधा हुआ | The local predicate describes the world as bound: NE `संसार कर्मले बाँधिएको छ`, HI `यह संसार ... कर्म से बँधा हुआ है`. Old `बाँध्ने / बाँधने वाला` made it an agent (“one who binds”), contradicting both. |
| 3.11 P2 #1 | `te` “those” | तिम्रो / तुम्हारा | ती / वे | In `te devāḥ`, `te` is the plural demonstrative “those” referring to the gods. The literals name `देवताहरू / देवताओं`; old `तिम्रो / तुम्हारा` was possessive “your”, not a demonstrative. |
| 3.12 P1 #1 | `iṣṭān` “desired” | इच्छितहरूलाई / इच्छितों को | चाहेका / वांछित | The word qualifies `bhogān` (“enjoyments”): NE says `चाहेका भोगहरू` and HI `वांछित भोग`. Old `इच्छितहरूलाई / इच्छितों को` substantivized the adjective and mismatched the object. |
| 3.12 P3 #4 | `ebhyaḥ` “to them” | तीभन्दा पर / इनसे परे | तिनीहरूलाई / उन्हें | The clause concerns not returning what the gods gave: NE `बदलामा नदिने`, HI `बदले में न देने`. Here `ebhyaḥ` is “to them”; old `तीभन्दा पर / इनसे परे` (“beyond them”) reversed the relation. |
| 3.13 P2 #2 | `sarva` “all” | हे सबै / हे सब | सबै / सब | In `sarva-kilbiṣaiḥ`, “all” modifies sins. The literal says `सबै पापबाट / सब पापों से`; old `हे सबै / हे सब` was a vocative, not the quantifier. |
| 3.14 P4 #2 | `karma` “from action” | कर्म / कर्म | कर्मबाट / कर्म से | The source gloss is ablative “from action”; both literals give the source phrase `कर्मबाट / कर्म से उत्पन्न`. Old bare `कर्म` omitted that relation. |
| 3.15 P1 #2 | `brahma` “from Brahman” | ब्रह्म / ब्रह्म | ब्रह्मबाट / ब्रह्म से | The first `brahma` is the source of action: NE `कर्म ब्रह्मबाट ... उत्पन्न`, HI `कर्म ब्रह्म से ... उत्पन्न`. Old bare `ब्रह्म` omitted “from”; the later nominative `brahma` is a different occurrence and stays as-is. |
| 3.15 P3 #2 | `sarva` “all” | हे सबै / हे सब | सबै / सब | This is the first part of `sarvagataṃ brahma` (“all-pervading Brahman”), not a vocative. Both literals say `सर्वव्यापी ब्रह्म`; old `हे सबै / हे सब` addressed “all” and was incompatible with the compound. |
| 3.18 P3 #3 | `asya` “of him” | यसको / इसका | उसको / उसका | The pronoun is third-person “his/of him”: NE `उसका निम्ति`, HI `उसके लिए`; old `यसको / इसका` was proximal “this”. |
| 3.18 P3 #4 | `sarva` “all” | हे सबै / हे सब | सबै / सब | Here `sarva` quantifies beings in `sarvabhūteṣu`; the literals express the negative as “any being” (`कुनै प्राणीमाथि / किसी प्राणी पर`). Old `हे सबै / हे सब` was a vocative and could not fit the compound or the negative clause. |
| 3.20 P4 #3 | `arhasi` “you should” | योग्य छौ / योग्य हो | पर्छ / चाहिए | The sentence says to act for lokasaṅgraha: NE `कर्म गर्नुपर्छ`, HI `कर्म करना चाहिए`. Old `योग्य छौ / योग्य हो` means “are worthy/fit”, not the obligation expressed by the two literals. |
| 3.23 P1 #5 | `varteyam` “I should engage” | गर्नुपर्छ / लगूँ | लागूँ / लगूँ | The optative is inside a “if I did not engage in action” condition: NE `यदि म ... कर्म नगरें`, HI `यदि मैं ... कर्म न करूँ`. Old NE `गर्नुपर्छ` turned the conditional into “must do”; HI `लगूँ` already matched, and is retained. |
| 3.24 P2 #2 | `kuryām` “I should perform” | गर्नुपर्छ / करूँ | गरूँ / करूँ | The first-person optative is conditional, not an instruction: NE `यदि मैले कर्म नगरें भने`, HI `यदि मैं कर्म न करूँ तो`. Old NE `गर्नुपर्छ` imposed obligation; `गरूँ / करूँ` preserves the first-person subjunctive/optative used by the literals. |
| 3.26 P3 #2 | `sarva` “all” | हे सबै / हे सब | सबै / सब | The word modifies actions (`sarva-karmāṇi`); literals say `सबै कर्म / सब कर्म`. Old `हे सबै / हे सब` was a vocative. |
| 3.28 P3 #3 | `vartante` “move, act” | रहन्छन् / रहते हैं | विचरण गर्छन् / विचरण करते हैं | In `guṇā guṇeṣu vartante`, the literals explicitly use “move/wander”: NE `विचरण गर्छन्`, HI `विचरण करने`. Old `रहन्छन् / रहते हैं` meant “remain”, not the verb used by the translations. |
| 3.31 P4 #4 | `karmabhiḥ` “from actions” | कर्महरूले / कर्मों से | कर्मबाट / कर्मों से | The sentence says the followers are released even from karma-bondage: NE `कर्मबन्धनबाट ... मुक्त`, HI `कर्म-बन्धन से ... मुक्त`. Old NE `कर्महरूले` made the actions the agent (“by actions”); corrected NE marks “from”. HI `कर्मों से` already carries the source sense and stays unchanged. |
| 3.32 P3 #1 | `sarva` “all” | हे सबै / हे सब | सबै / सब | In `sarva-jñāna`, “all” modifies knowledge; literals give `सबै ज्ञानबाट / सब ज्ञान से`. Old `हे सबै / हे सब` was a vocative. |
| 3.33 P1 #1 | `sadṛśam` “according to, in conformity with” | बराबर / बराबर | अनुसार / अनुसार | The phrase says action is in conformity with one’s nature: NE `स्वभावअनुसार`, HI `स्वभाव के अनुसार`. Old `बराबर / बराबर` means “equal”, not “according to”. |
| 3.33 P1 #3 | `svasyāḥ` “of one's own” | आफ्नैको / अपनी का | आफ्नै / अपने | The possessive modifies one’s own nature: NE `आफ्नै स्वभाव`, HI `अपने स्वभाव`. Old `आफ्नैको / अपनी का` was malformed in both languages and did not fit the following noun. |
| 3.34 P4 #3 | `asya` “of him” | यसको / इसका | उसको / उसका | The obstacles are “his” impediments: NE says `उसका बाटो`, HI `उसके मार्ग`. Old `यसको / इसका` was the wrong proximal pronoun. |
| 3.35 P3 #4 | `śreyaḥ` “is better” | कल्याण / कल्याण | राम्रो / अच्छा | The comparative is rendered directly as `राम्रो` and `अच्छा` in the literals (“own dharma ... is better”); old `कल्याण` means welfare/good, but did not mark the comparison. |
| 3.36 P4 #3 | `niyojitaḥ` “driven, compelled” | प्रेरित / प्रेरित | बाध्य / बाध्य | Arjuna asks what compels action against one’s will: NE `बलले जबरजस्ती गरिएर`, HI `बल से बाध्य होकर`. Old `प्रेरित` repeated the preceding “driven/inspired” idea and missed this passive “compelled” force. |
| 3.37 P4 #2 | `enam` “this” | उसलाई / उसे | यसलाई / इसे | The object is “this” desire/anger as enemy: NE `यसलाई नै ... शत्रु`, HI `इसे ही ... शत्रु`. Old `उसलाई / उसे` changed the near demonstrative to “that person”. |
| 3.41 P3 #3 | `enam` “this” | उसलाई / उसे | यसलाई / इसे | The object is the present evil to be cast off; literals say `यस पापीलाई` and `इस पापी को`. Old `उसलाई / उसे` was anaphorically too remote; “this one” is explicit. |
| 3.41 P4 #2 | `vijñāna` “and discrimination” | साक्षात्कार / साक्षात्कार | विवेक / विवेक | The full literal pairs knowledge with `विवेक` in both NE and HI. Old `साक्षात्कार` means realization/experience and is not the discrimination named by the source gloss or these translations. |
| 3.42 P2 #2 | `param` “higher” | परम / परम | श्रेष्ठ / श्रेष्ठ | Here `param` is the comparative “higher/superior” in the senses hierarchy; both literals say `श्रेष्ठ`. Old `परम` suggested “supreme/absolute” rather than “higher than the senses”. |
| 3.42 P4 #2 | `buddheḥ` “than the intellect” | बुद्धिको / बुद्धि की | बुद्धिभन्दा / बुद्धि से | The ablative is comparative (“than the intellect”): NE `बुद्धिभन्दा`, HI `बुद्धि से`. Old genitive `बुद्धिको / बुद्धि की` did not express the comparison. |
| 3.43 P1 #2 | `buddheḥ` “than the intellect” | बुद्धिको / बुद्धि की | बुद्धिभन्दा / बुद्धि से | The same comparative ablative appears in `buddheḥ param`; literals say `बुद्धिभन्दा पर` and `बुद्धि से परे`. Old `बुद्धिको / बुद्धि की` was genitive, not “than”. |
| 3.43 P1 #3 | `param` “beyond” | परम / परम | परे / परे | In `buddheḥ param`, this means “beyond”, not the adjective “supreme”: NE `बुद्धिभन्दा परको`, HI `बुद्धि से परे`. Old `परम` changed the relationship. |

Chapter 7 changed-word table:

| Verse / word position | Form / English gloss | Old NE / HI | New NE / HI | Translation evidence and reason |
|---|---|---|---|---|
| 7.02 P1 #2 | `te` “to you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | This `te` is the second-person dative “to you”: NE `म तिमीलाई ... बताउनेछु`, HI `मैं तुझे ... बताऊँगा`. Old `तिम्रो / तुम्हारा` was possessive. |
| 7.05 P1 #3 | `itaḥ` “than this” | यहाँबाट / यहाँ से | यसभन्दा / इससे | The comparison is “higher than this [lower nature]”: NE `यसभन्दा परको`, HI `इससे परे`. Old `यहाँबाट / यहाँ से` meant “from here”; the referent is this nature, not a place. |
| 7.06 P1 #1 | `etat` “these” | यो / यह | यी / इन | The demonstrative points to the two natures and therefore is plural in the literals: `यी दुई प्रकृतिहरू` / `इन दोनों प्रकृतियों`. Old singular `यो / यह` mismatched both number and referent. |
| 7.06 P4 #3 | `tathā` “also” | त्यसरी / वैसे ही | पनि / भी | In `prabhavaḥ pralayaḥ tathā`, the word adds “also/and”: the literals have `उत्पत्ति र विनाश पनि` / `उत्पत्ति और विनाश भी`. Old `त्यसरी / वैसे ही` was manner (“thus”), not additive. |
| 7.08 P4 #3 | `pauruṣam` “the manliness” | आफ्नो क्षमता / अपनी क्षमता | पौरुष / पौरुष | The literal translations use the technical noun `पौरुष` in men; old `आफ्नो क्षमता / अपनी क्षमता` means “one’s own ability” and did not match the source word “manliness/virility”. |
| 7.12 P1 #4 | `sāttvikāḥ` “sāttvic” | सात्त्विकहरू / सात्त्विक | सात्त्विक / सात्त्विक | Here the adjective qualifies `bhāvāḥ` (“states”): NE literal lists `सात्त्विक ... अवस्थाहरू`, HI `सात्त्विक ... अवस्थाएँ`. Old NE `सात्त्विकहरू` made the adjective into “sattvic people”; HI `सात्त्विक` already agreed and is retained. |
| 7.12 P2 #1 | `rājasāḥ` “rājasic” | राजसहरू / राजस | राजस / राजस | This is the adjective “rājasic” in the list of states: NE literal `राजस ... अवस्थाहरू`, HI `राजस ... अवस्थाएँ`. Old NE `राजसहरू` made it a plural noun; HI `राजस` already agreed. |
| 7.12 P2 #2 | `tāmasāḥ` “tāmasic” | तामसहरू / तामस | तामस / तामस | This is the adjective “tāmasic” in the list of states: NE literal `तामस ... अवस्थाहरू`, HI `तामस ... अवस्थाएँ`. Old NE `तामसहरू` made it a plural noun; HI `तामस` already agreed. |
| 7.13 P4 #3 | `param` “beyond” | परम / परम | परे / परे | This means beyond the three guṇas, not “supreme”: NE says `तिनभन्दा पर`, HI `उनसे परे`. Old `परम` was a different sense. |
| 7.17 P3 #3 | `jñāninaḥ` “to the wise” | ज्ञानीका / ज्ञानी के | ज्ञानीका निम्ति / ज्ञानी के लिए | The clause is “I am dear to the wise”: NE `ज्ञानीका निम्ति`, HI `ज्ञानी के लिए`. Old `ज्ञानीका / ज्ञानी के` lacked the “for/to” relation in both word-level forms. |
| 7.20 P3 #1 | `tam` “this” | उसलाई / उसे | यो / इस | The first of the repeated `tam` pair is proximal “this” in “this or that method”: NE `यो ... वा`, HI `इस ... या`. Old `उसलाई / उसे` was a personal object pronoun. |
| 7.20 P3 #2 | `tam` “this” | उसलाई / उसे | त्यो / उस | The second of the pair is distal “that”: NE `त्यो`, HI `उस` in `यो वा त्यो विधि / इस या उस विधि`. Old `उसलाई / उसे` was again an object pronoun and did not preserve the contrast. |
| 7.21 P4 #1 | `tām` “that” | त्यो / उसे | त्यो / उस | This feminine demonstrative modifies `śraddhām` (“faith”): NE `त्यो श्रद्धा`, HI `उस श्रद्धा`. Old Hindi `उसे` meant “to her/it” as an object pronoun, not “that” as a determiner; Nepali `त्यो` already matched. |
| 7.22 P3 #3 | `tataḥ` “from it” | त्यसैले / इसलिए | त्यसबाट / उससे | The literal says the worshipper obtains desires “from it”: NE `त्यसबाट`, HI `उससे`. Old `त्यसैले / इसलिए` was causal “therefore”, not source/origin. |
| 7.24 P2 #3 | `abuddhayaḥ` “the unintelligent” | अबुद्धिहरू / अबुद्धि | अबुद्धिहरू / अज्ञानी | The subject is people who do not understand: both literals say `अज्ञानी` (NE `अज्ञानीहरू`). The old Hindi `अबुद्धि` was an abstract noun (“lack of intellect”), not the plural people named by the source; NE `अबुद्धिहरू` is retained. |
| 7.25 P1 #3 | `prakāśaḥ` “manifest” | प्रकाश / प्रकाश | प्रकट / प्रकट | The predicate is “manifest/revealed”: NE `प्रकट हुँदिनँ`, HI `प्रकट नहीं होता`. Old `प्रकाश` is the noun “light”, not the predicate in these literals. |
| 7.25 P1 #4 | `sarvasya` “to all” | सबैको / सबका | सबैलाई / सबको | In `na prakāśaḥ sarvasya`, the sense is “not manifest to everyone”: NE `सबैलाई`, HI `सबको`. Old `सबैको / सबका` was possessive/genitive. |
| 7.26 P1 #1 | `veda` “I know” | जान्दछ / जानता है | जान्दछु / जानता हूँ | The speaker is first person: NE `म ... जान्दछु`, HI `मैं ... जानता हूँ`. Old `जान्दछ / जानता है` was third-person singular. |
| 7.27 P4 #1 | `sarge` “at birth” | सृष्टिमा / सृष्टि में | जन्ममा / जन्म में | The context is the birth into delusion caused by the pairs of desire/aversion; both literals say `जन्ममा / जन्म में`. Old `सृष्टिमा / सृष्टि में` meant “in creation”, not “at birth”. |

**Interpretive holds / owner flags (not changed):** `te` 3.01 (NE `तिम्रो`, HI `तुम्हारा`; “by you” vs “in your view” is not a clear contradiction across the literal idioms); `tat` 3.02 (keep the NE/HI demonstrative `त्यो / वह` for *tad ekam* “that one thing”; the EN gloss “therefore” is left untouched); `anyatra` 3.09 (NE `बाहेक` is explicit “except”; HI `के अतिरिक्त` can be read more than one way, while the full literal says `छोड़कर`); `matvā` 3.28 (EN “having known” and the literals “knowing” vs current “thinking”; reserved for Dhruba); `aśanaḥ` in *mahāśanaḥ* 3.37 (“insatiable” vs “all-devouring”); `parām` 7.05 (technical `परा प्रकृति` vs “higher/supreme”); `teṣām` 7.17 (Sanskrit genitive “of them” vs literal “among them”). In 7.17 `mama` was confirmed in a prior batch and is **not reopened**. At 7.24, retain `param` + `bhāvam` as “higher nature” / technical `परा प्रकृति` pending Dhruba; at 7.30, leave doctrinal `adhibhūta`, `adhidaivam` and `adhiyajñam` as-is. Per the standing instruction, the 11.44 Nepali literal `शरीर थपथपाउँछु` for *praṇidhāya* is also still Dhruba’s decision; remind him, do not fix it.

**Every occurrence examined and left alone** (speaker and pāda words, in worksheet order; `P# / #` identifies pāda / word position; `[flag]` identifies a deliberate hold; `mama` 7.17 was previously verified and not reopened):

**Chapter 3:**
- `3.01` — S#1 `arjunaḥ`; S#2 `uvāca`; P1#1 `jyāyasī`; P1#2 `cet`; P1#3 `karmaṇaḥ`; P1#4 `te` [flag — unchanged]; P2#1 `matā`; P2#2 `buddhiḥ`; P2#3 `janārdana`; P3#1 `tat`; P3#2 `kim`; P3#3 `karmaṇi`; P3#4 `ghore`; P3#5 `mām`; P4#1 `niyojayasi`; P4#2 `keśava`
- `3.02` — P1#1 `vyāmiśreṇa`; P1#2 `iva`; P1#3 `vākyena`; P2#1 `buddhim`; P2#2 `mohayasi`; P2#3 `iva`; P2#4 `me`; P3#1 `tat` [flag — unchanged]; P3#2 `ekam`; P3#3 `vada`; P3#4 `niścitya`; P4#1 `yena`; P4#2 `śreyaḥ`; P4#3 `aham`; P4#4 `āpnuyām`
- `3.03` — S#1 `śrībhagavān`; S#2 `uvāca`; P1#1 `loke`; P1#2 `asmin`; P1#3 `dvividhā`; P1#4 `niṣṭhā`; P2#1 `purā`; P2#2 `proktā`; P2#3 `mayā`; P2#4 `anagha`; P3#1 `jñānayogena`; P3#2 `sāṅkhyānām`; P4#1 `karmayogena`; P4#2 `yoginām`
- `3.04` — P1#1 `na`; P1#2 `karmaṇām`; P1#3 `anārambhāt`; P2#1 `naiṣkarmyam`; P2#2 `puruṣaḥ`; P3#1 `na`; P3#2 `ca`; P3#3 `sannyasanāt`; P3#4 `eva`; P4#1 `siddhim`; P4#2 `samadhigacchati`
- `3.05` — P1#1 `na`; P1#2 `hi`; P1#3 `kaścit`; P1#4 `kṣaṇam`; P1#5 `api`; P2#1 `jātu`; P2#2 `tiṣṭhati`; P2#3 `akarmakṛt`; P3#1 `kāryate`; P3#2 `hi`; P3#3 `avaśaḥ`; P3#4 `karma`; P4#1 `sarvaḥ`; P4#2 `prakṛti`; P4#3 `jaiḥ`; P4#4 `guṇaiḥ`
- `3.06` — P1#1 `karma`; P1#2 `indriyāṇi`; P1#3 `saṁyamya`; P2#1 `yaḥ`; P2#2 `āste`; P2#3 `manasā`; P2#4 `smaran`; P3#1 `indriya`; P3#2 `arthān`; P3#3 `vimūḍha`; P3#4 `ātmā`; P4#1 `mithyācāraḥ`; P4#2 `saḥ`; P4#3 `ucyate`
- `3.07` — P1#1 `yaḥ`; P1#2 `tu`; P1#3 `indriyāṇi`; P1#4 `manasā`; P2#1 `niyamya`; P2#2 `ārabhate`; P2#3 `arjuna`; P3#1 `karma`; P3#2 `indriyaiḥ`; P3#3 `karma`; P3#4 `yogam`; P4#1 `asaktaḥ`; P4#2 `saḥ`; P4#3 `viśiṣyate`
- `3.08` — P1#1 `niyatam`; P1#2 `kuru`; P1#3 `karma`; P1#4 `tvam`; P2#1 `karma`; P2#2 `jyāyaḥ`; P2#3 `hi`; P3#1 `śarīrayātrā`; P3#2 `api`; P3#3 `ca`; P3#4 `te`; P4#1 `na`; P4#2 `prasidhyet`
- `3.09` — P1#1 `yajña`; P1#2 `arthāt`; P1#3 `karmaṇaḥ`; P1#4 `anyatra` [flag — unchanged]; P2#1 `lokaḥ`; P2#2 `ayam`; P2#3 `karma`; P3#1 `tat`; P3#2 `artham`; P3#3 `karma`; P3#4 `kaunteya`; P4#1 `mukta`; P4#2 `saṅgaḥ`; P4#3 `samācara`
- `3.10` — P1#1 `saha`; P1#2 `yajñāḥ`; P1#3 `prajāḥ`; P1#4 `sṛṣṭvā`; P2#1 `purā`; P2#2 `uvāca`; P2#3 `prajā`; P2#4 `patiḥ`; P3#1 `anena`; P3#2 `prasaviṣyadhvam`; P4#1 `eṣaḥ`; P4#2 `vaḥ`; P4#3 `astu`; P4#4 `iṣṭa`; P4#5 `kāmadhuk`
- `3.11` — P1#1 `devān`; P1#2 `bhāvayata`; P1#3 `anena`; P2#2 `devāḥ`; P2#3 `bhāvayantu`; P2#4 `vaḥ`; P3#1 `parasparam`; P3#2 `bhāvayantaḥ`; P4#1 `śreyaḥ`; P4#2 `param`; P4#3 `avāpsyatha`
- `3.12` — P1#2 `bhogān`; P1#3 `hi`; P1#4 `vaḥ`; P1#5 `devāḥ`; P2#1 `dāsyante`; P2#2 `yajña`; P2#3 `bhāvitāḥ`; P3#1 `taiḥ`; P3#2 `dattān`; P3#3 `apradāya`; P4#1 `yaḥ`; P4#2 `bhuṅkte`; P4#3 `stenaḥ`; P4#4 `eva`; P4#5 `saḥ`
- `3.13` — P1#1 `yajña`; P1#2 `śiṣṭa`; P1#3 `aśinaḥ`; P1#4 `santaḥ`; P2#1 `mucyante`; P2#3 `kilbiṣaiḥ`; P3#1 `bhuñjate`; P3#2 `te`; P3#3 `tu`; P3#4 `agham`; P3#5 `pāpāḥ`; P4#1 `ye`; P4#2 `pacanti`; P4#3 `ātma`; P4#4 `kāraṇāt`
- `3.14` — P1#1 `annāt`; P1#2 `bhavanti`; P1#3 `bhūtāni`; P2#1 `parjanyāt`; P2#2 `anna`; P2#3 `sambhavaḥ`; P3#1 `yajñāt`; P3#2 `bhavati`; P3#3 `parjanyaḥ`; P4#1 `yajñaḥ`; P4#3 `samudbhavaḥ`
- `3.15` — P1#1 `karma`; P1#3 `udbhavam`; P1#4 `viddhi`; P2#1 `brahma`; P2#2 `akṣara`; P2#3 `samudbhavam`; P3#1 `tasmāt`; P3#3 `gatam`; P3#4 `brahma`; P4#1 `nityam`; P4#2 `yajñe`; P4#3 `pratiṣṭhitam`
- `3.16` — P1#1 `evam`; P1#2 `pravartitam`; P1#3 `cakram`; P2#1 `na`; P2#2 `anuvartayati`; P2#3 `iha`; P2#4 `yaḥ`; P3#1 `agha`; P3#2 `āyuḥ`; P3#3 `indriya`; P3#4 `ārāmaḥ`; P4#1 `mogham`; P4#2 `pārtha`; P4#3 `saḥ`; P4#4 `jīvati`
- `3.17` — P1#1 `yaḥ`; P1#2 `tu`; P1#3 `ātma`; P1#4 `ratiḥ`; P1#5 `eva`; P1#6 `syāt`; P2#1 `ātma`; P2#2 `tṛptaḥ`; P2#3 `ca`; P2#4 `mānavaḥ`; P3#1 `ātmani`; P3#2 `eva`; P3#3 `ca`; P3#4 `santuṣṭaḥ`; P4#1 `tasya`; P4#2 `kāryam`; P4#3 `na`; P4#4 `vidyate`
- `3.18` — P1#1 `na`; P1#2 `eva`; P1#3 `tasya`; P1#4 `kṛtena`; P1#5 `arthaḥ`; P2#1 `na`; P2#2 `akṛtena`; P2#3 `iha`; P2#4 `kaścana`; P3#1 `na`; P3#2 `ca`; P3#5 `bhūteṣu`; P4#1 `kaścit`; P4#2 `artha`; P4#3 `vyapāśrayaḥ`
- `3.19` — P1#1 `tasmāt`; P1#2 `asaktaḥ`; P1#3 `satatam`; P2#1 `kāryam`; P2#2 `karma`; P2#3 `samācara`; P3#1 `asaktaḥ`; P3#2 `hi`; P3#3 `ācaran`; P3#4 `karma`; P4#1 `param`; P4#2 `āpnoti`; P4#3 `pūruṣaḥ`
- `3.20` — P1#1 `karmaṇā`; P1#2 `eva`; P1#3 `hi`; P1#4 `saṁsiddhim`; P2#1 `āsthitāḥ`; P2#2 `janakādayaḥ`; P3#1 `loka`; P3#2 `saṅgraham`; P3#3 `eva`; P3#4 `api`; P4#1 `sampaśyan`; P4#2 `kartum`
- `3.21` — P1#1 `yat`; P1#2 `yat`; P1#3 `ācarati`; P1#4 `śreṣṭhaḥ`; P2#1 `tat`; P2#2 `tat`; P2#3 `eva`; P2#4 `itaraḥ`; P2#5 `janaḥ`; P3#1 `saḥ`; P3#2 `yat`; P3#3 `pramāṇam`; P3#4 `kurute`; P4#1 `lokaḥ`; P4#2 `tat`; P4#3 `anuvartate`
- `3.22` — P1#1 `na`; P1#2 `me`; P1#3 `pārtha`; P1#4 `asti`; P1#5 `kartavyam`; P2#1 `triṣu`; P2#2 `lokeṣu`; P2#3 `kiñcana`; P3#1 `na`; P3#2 `anavāptam`; P3#3 `avāptavyam`; P4#1 `varte`; P4#2 `eva`; P4#3 `ca`; P4#4 `karmaṇi`
- `3.23` — P1#1 `yadi`; P1#2 `hi`; P1#3 `aham`; P1#4 `na`; P2#1 `jātu`; P2#2 `karmaṇi`; P2#3 `atandritaḥ`; P3#1 `mama`; P3#2 `vartma`; P3#3 `anuvartante`; P4#1 `manuṣyāḥ`; P4#2 `pārtha`; P4#3 `sarvaśaḥ`
- `3.24` — P1#1 `utsīdeyuḥ`; P1#2 `ime`; P1#3 `lokāḥ`; P2#1 `na`; P2#3 `karma`; P2#4 `cet`; P2#5 `aham`; P3#1 `saṅkarasya`; P3#2 `ca`; P3#3 `kartā`; P3#4 `syām`; P4#1 `upahanyām`; P4#2 `imāḥ`; P4#3 `prajāḥ`
- `3.25` — P1#1 `saktāḥ`; P1#2 `karmaṇi`; P1#3 `avidvāṁsaḥ`; P2#1 `yathā`; P2#2 `kurvanti`; P2#3 `bhārata`; P3#1 `kuryāt`; P3#2 `vidvān`; P3#3 `tathā`; P3#4 `asaktaḥ`; P4#1 `cikīrṣuḥ`; P4#2 `loka`; P4#3 `saṅgraham`
- `3.26` — P1#1 `na`; P1#2 `buddhi`; P1#3 `bhedam`; P1#4 `janayet`; P2#1 `ajñānām`; P2#2 `karma`; P2#3 `saṅginām`; P3#1 `joṣayet`; P3#3 `karmāṇi`; P4#1 `vidvān`; P4#2 `yuktaḥ`; P4#3 `samācaran`
- `3.27` — P1#1 `prakṛteḥ`; P1#2 `kriyamāṇāni`; P2#1 `guṇaiḥ`; P2#2 `karmāṇi`; P2#3 `sarvaśaḥ`; P3#1 `ahaṅkāra`; P3#2 `vimūḍha`; P3#3 `ātmā`; P4#1 `kartā`; P4#2 `aham`; P4#3 `iti`; P4#4 `manyate`
- `3.28` — P1#1 `tattvavit`; P1#2 `tu`; P1#3 `mahā`; P1#4 `bāho`; P2#1 `guṇa`; P2#2 `karma`; P2#3 `vibhāgayoḥ`; P3#1 `guṇāḥ`; P3#2 `guṇeṣu`; P4#1 `iti`; P4#2 `matvā` [flag — unchanged]; P4#3 `na`; P4#4 `sajjate`
- `3.29` — P1#1 `prakṛteḥ`; P1#2 `guṇa`; P1#3 `sammūḍhāḥ`; P2#1 `sajjante`; P2#2 `guṇa`; P2#3 `karmasu`; P3#1 `tān`; P3#2 `akṛtsna`; P3#3 `vidaḥ`; P3#4 `mandān`; P4#1 `kṛtsnavit`; P4#2 `na`; P4#3 `vicālayet`
- `3.30` — P1#1 `mayi`; P1#2 `sarvāṇi`; P1#3 `karmāṇi`; P2#1 `sannyasya`; P2#2 `adhyātma`; P2#3 `cetasā`; P3#1 `nirāśīḥ`; P3#2 `nirmamaḥ`; P3#3 `bhūtvā`; P4#1 `yudhyasva`; P4#2 `vigata`; P4#3 `jvaraḥ`
- `3.31` — P1#1 `ye`; P1#2 `me`; P1#3 `matam`; P1#4 `idam`; P1#5 `nityam`; P2#1 `anutiṣṭhanti`; P2#2 `mānavāḥ`; P3#1 `śraddhāvantaḥ`; P3#2 `anasūyantaḥ`; P4#1 `mucyante`; P4#2 `te`; P4#3 `api`
- `3.32` — P1#1 `ye`; P1#2 `tu`; P1#3 `etat`; P1#4 `abhyasūyantaḥ`; P2#1 `na`; P2#2 `anutiṣṭhanti`; P2#3 `me`; P2#4 `matam`; P3#2 `jñāna`; P3#3 `vimūḍhān`; P3#4 `tān`; P4#1 `viddhi`; P4#2 `naṣṭān`; P4#3 `acetasaḥ`
- `3.33` — P1#2 `ceṣṭate`; P2#1 `prakṛteḥ`; P2#2 `jñānavān`; P2#3 `api`; P3#1 `prakṛtim`; P3#2 `yānti`; P3#3 `bhūtāni`; P4#1 `nigrahaḥ`; P4#2 `kim`; P4#3 `kariṣyati`
- `3.34` — P1#1 `indriyasya`; P1#2 `indriyasya`; P1#3 `arthe`; P2#1 `rāga`; P2#2 `dveṣau`; P2#3 `vyavasthitau`; P3#1 `tayoḥ`; P3#2 `na`; P3#3 `vaśam`; P3#4 `āgacchet`; P4#1 `tau`; P4#2 `hi`; P4#4 `paripanthinau`
- `3.35` — P1#1 `śreyān`; P1#2 `sva`; P1#3 `dharmaḥ`; P1#4 `viguṇaḥ`; P2#1 `para`; P2#2 `dharmāt`; P2#3 `svanuṣṭhitāt`; P3#1 `sva`; P3#2 `dharme`; P3#3 `nidhanam`; P4#1 `para`; P4#2 `dharmaḥ`; P4#3 `bhaya`; P4#4 `āvahaḥ`
- `3.36` — S#1 `arjunaḥ`; S#2 `uvāca`; P1#1 `atha`; P1#2 `kena`; P1#3 `prayuktaḥ`; P1#4 `ayam`; P2#1 `pāpam`; P2#2 `carati`; P2#3 `pūruṣaḥ`; P3#1 `anicchan`; P3#2 `api`; P3#3 `vārṣṇeya`; P4#1 `balāt`; P4#2 `iva`
- `3.37` — S#1 `śrībhagavān`; S#2 `uvāca`; P1#1 `kāmaḥ`; P1#2 `eṣaḥ`; P1#3 `krodhaḥ`; P1#4 `eṣaḥ`; P2#1 `rajaḥ`; P2#2 `guṇa`; P2#3 `samudbhavaḥ`; P3#1 `mahā`; P3#2 `aśanaḥ` [flag — unchanged]; P3#3 `mahā`; P3#4 `pāpmā`; P4#1 `viddhi`; P4#3 `iha`; P4#4 `vairiṇam`
- `3.38` — P1#1 `dhūmena`; P1#2 `āvriyate`; P1#3 `vahniḥ`; P2#1 `yathā`; P2#2 `ādarśaḥ`; P2#3 `malena`; P2#4 `ca`; P3#1 `yathā`; P3#2 `ulbena`; P3#3 `āvṛtaḥ`; P3#4 `garbhaḥ`; P4#1 `tathā`; P4#2 `tena`; P4#3 `idam`; P4#4 `āvṛtam`
- `3.39` — P1#1 `āvṛtam`; P1#2 `jñānam`; P1#3 `etena`; P2#1 `jñāninaḥ`; P2#2 `nitya`; P2#3 `vairiṇā`; P3#1 `kāma`; P3#2 `rūpeṇa`; P3#3 `kaunteya`; P4#1 `duḥ`; P4#2 `pūreṇa`; P4#3 `analena`; P4#4 `ca`
- `3.40` — P1#1 `indriyāṇi`; P1#2 `manaḥ`; P1#3 `buddhiḥ`; P2#1 `asya`; P2#2 `adhiṣṭhānam`; P2#3 `ucyate`; P3#1 `etaiḥ`; P3#2 `vimohayati`; P3#3 `eṣaḥ`; P4#1 `jñānam`; P4#2 `āvṛtya`; P4#3 `dehinam`
- `3.41` — P1#1 `tasmāt`; P1#2 `tvam`; P1#3 `indriyāṇi`; P1#4 `ādau`; P2#1 `niyamya`; P2#2 `bharata`; P2#3 `ṛṣabha`; P3#1 `pāpmānam`; P3#2 `prajahihi`; P4#1 `jñāna`; P4#3 `nāśanam`
- `3.42` — P1#1 `indriyāṇi`; P1#2 `parāṇi`; P1#3 `āhuḥ`; P2#1 `indriyebhyaḥ`; P2#3 `manaḥ`; P3#1 `manasaḥ`; P3#2 `tu`; P3#3 `parā`; P3#4 `buddhiḥ`; P4#1 `yaḥ`; P4#3 `parataḥ`; P4#4 `tu`; P4#5 `saḥ`
- `3.43` — P1#1 `evam`; P1#4 `buddhvā`; P2#1 `saṁstabhya`; P2#2 `ātmānam`; P2#3 `ātmanā`; P3#1 `jahi`; P3#2 `śatrum`; P3#3 `mahā`; P3#4 `bāho`; P4#1 `kāma`; P4#2 `rūpam`; P4#3 `dur`; P4#4 `āsadam`

Chapter 3 audit list: 614 speaker/pāda word occurrences total; 582 explicitly listed as unchanged/held, in addition to the changed-word table above.

**Chapter 7:**
- `7.01` — S#1 `śrībhagavān`; S#2 `uvāca`; P1#1 `mayi`; P1#2 `āsakta`; P1#3 `manāḥ`; P1#4 `pārtha`; P2#1 `yogam`; P2#2 `yuñjan`; P2#3 `madāśrayaḥ`; P3#1 `asaṁśayam`; P3#2 `samagram`; P3#3 `mām`; P4#1 `yathā`; P4#2 `jñāsyasi`; P4#3 `tat`; P4#4 `śṛṇu`
- `7.02` — P1#1 `jñānam`; P1#3 `aham`; P1#4 `savijñānam`; P2#1 `idam`; P2#2 `vakṣyāmi`; P2#3 `aśeṣataḥ`; P3#1 `yat`; P3#2 `jñātvā`; P3#3 `na`; P3#4 `iha`; P3#5 `bhūyaḥ`; P3#6 `anyat`; P4#1 `jñātavyam`; P4#2 `avaśiṣyate`
- `7.03` — P1#1 `manuṣyāṇām`; P1#2 `sahasreṣu`; P2#1 `kaścit`; P2#2 `yatati`; P2#3 `siddhaye`; P3#1 `yatatām`; P3#2 `api`; P3#3 `siddhānām`; P4#1 `kaścit`; P4#2 `mām`; P4#3 `vetti`; P4#4 `tattvataḥ`
- `7.04` — P1#1 `bhūmiḥ`; P1#2 `āpaḥ`; P1#3 `analaḥ`; P1#4 `vāyuḥ`; P2#1 `kham`; P2#2 `manaḥ`; P2#3 `buddhiḥ`; P2#4 `eva`; P2#5 `ca`; P3#1 `ahaṅkāraḥ`; P3#2 `iti`; P3#3 `iyam`; P3#4 `me`; P4#1 `bhinnā`; P4#2 `prakṛtiḥ`; P4#3 `aṣṭadhā`
- `7.05` — P1#1 `aparā`; P1#2 `iyam`; P1#4 `tu`; P1#5 `anyām`; P2#1 `prakṛtim`; P2#2 `viddhi`; P2#3 `me`; P2#4 `parām` [flag — unchanged]; P3#1 `jīvabhūtām`; P3#2 `mahābāho`; P4#1 `yayā`; P4#2 `idam`; P4#3 `dhāryate`; P4#4 `jagat`
- `7.06` — P1#2 `yonīni`; P1#3 `bhūtāni`; P2#1 `sarvāṇi`; P2#2 `iti`; P2#3 `upadhāraya`; P3#1 `aham`; P3#2 `kṛtsnasya`; P3#3 `jagataḥ`; P4#1 `prabhavaḥ`; P4#2 `pralayaḥ`
- `7.07` — P1#1 `mattaḥ`; P1#2 `parataram`; P1#3 `na`; P1#4 `anyat`; P2#1 `kiñcit`; P2#2 `asti`; P2#3 `dhanañjaya`; P3#1 `mayi`; P3#2 `sarvam`; P3#3 `idam`; P3#4 `protam`; P4#1 `sūtre`; P4#2 `maṇigaṇāḥ`; P4#3 `iva`
- `7.08` — P1#1 `rasaḥ`; P1#2 `aham`; P1#3 `apsu`; P1#4 `kaunteya`; P2#1 `prabhā`; P2#2 `asmi`; P2#3 `śaśisūryayoḥ`; P3#1 `praṇavaḥ`; P3#2 `sarvavedeṣu`; P4#1 `śabdaḥ`; P4#2 `khe`; P4#4 `nṛṣu`
- `7.09` — P1#1 `puṇyaḥ`; P1#2 `gandhaḥ`; P1#3 `pṛthivyām`; P1#4 `ca`; P2#1 `tejaḥ`; P2#2 `ca`; P2#3 `asmi`; P2#4 `vibhāvasau`; P3#1 `jīvanam`; P3#2 `sarvabhūteṣu`; P4#1 `tapaḥ`; P4#2 `ca`; P4#3 `asmi`; P4#4 `tapasviṣu`
- `7.10` — P1#1 `bījam`; P1#2 `mām`; P1#3 `sarvabhūtānām`; P2#1 `viddhi`; P2#2 `pārtha`; P2#3 `sanātanam`; P3#1 `buddhiḥ`; P3#2 `buddhimatām`; P3#3 `asmi`; P4#1 `tejaḥ`; P4#2 `tejasvinām`; P4#3 `aham`
- `7.11` — P1#1 `balam`; P1#2 `balavatām`; P1#3 `ca`; P1#4 `aham`; P2#1 `kāmarāgavivarjitam`; P3#1 `dharmāviruddhaḥ`; P3#2 `bhūteṣu`; P4#1 `kāmaḥ`; P4#2 `asmi`; P4#3 `bharatarṣabha`
- `7.12` — P1#1 `ye`; P1#2 `ca`; P1#3 `eva`; P1#5 `bhāvāḥ`; P2#3 `ca`; P2#4 `ye`; P3#1 `mattaḥ`; P3#2 `eva`; P3#3 `iti`; P3#4 `tān`; P3#5 `viddhi`; P4#1 `na`; P4#2 `tu`; P4#3 `aham`; P4#4 `teṣu`; P4#5 `te`; P4#6 `mayi`
- `7.13` — P1#1 `tribhiḥ`; P1#2 `guṇamayaiḥ`; P1#3 `bhāvaiḥ`; P2#1 `ebhiḥ`; P2#2 `sarvam`; P2#3 `idam`; P2#4 `jagat`; P3#1 `mohitam`; P3#2 `na`; P3#3 `abhijānāti`; P4#1 `mām`; P4#2 `ebhyaḥ`; P4#4 `avyayam`
- `7.14` — P1#1 `daivī`; P1#2 `hi`; P1#3 `eṣā`; P1#4 `guṇamayī`; P2#1 `mama`; P2#2 `māyā`; P2#3 `duratyayā`; P3#1 `mām`; P3#2 `eva`; P3#3 `ye`; P3#4 `prapadyante`; P4#1 `māyām`; P4#2 `etām`; P4#3 `taranti`; P4#4 `te`
- `7.15` — P1#1 `na`; P1#2 `mām`; P1#3 `duṣkṛtinaḥ`; P1#4 `mūḍhāḥ`; P2#1 `prapadyante`; P2#2 `narādhamāḥ`; P3#1 `māyayā`; P3#2 `apahṛtajñānāḥ`; P4#1 `āsuram`; P4#2 `bhāvam`; P4#3 `āśritāḥ`
- `7.16` — P1#1 `caturvidhāḥ`; P1#2 `bhajante`; P1#3 `mām`; P2#1 `janāḥ`; P2#2 `sukṛtinaḥ`; P2#3 `arjuna`; P3#1 `ārtaḥ`; P3#2 `jijñāsuḥ`; P3#3 `arthārthī`; P4#1 `jñānī`; P4#2 `ca`; P4#3 `bharatarṣabha`
- `7.17` — P1#1 `teṣām` [flag — unchanged]; P1#2 `jñānī`; P1#3 `nityayuktaḥ`; P2#1 `ekabhaktiḥ`; P2#2 `viśiṣyate`; P3#1 `priyaḥ`; P3#2 `hi`; P3#4 `atyartham`; P4#1 `aham`; P4#2 `saḥ`; P4#3 `ca`; P4#4 `mama` [prior verified; not reopened]; P4#5 `priyaḥ`
- `7.18` — P1#1 `udārāḥ`; P1#2 `sarve`; P1#3 `eva`; P1#4 `ete`; P2#1 `jñānī`; P2#2 `tu`; P2#3 `ātmā`; P2#4 `eva`; P2#5 `me`; P2#6 `matam`; P3#1 `āsthitaḥ`; P3#2 `saḥ`; P3#3 `hi`; P3#4 `yuktātmā`; P4#1 `mām`; P4#2 `eva`; P4#3 `anuttamām`; P4#4 `gatim`
- `7.19` — P1#1 `bahūnām`; P1#2 `janmanām`; P1#3 `ante`; P2#1 `jñānavān`; P2#2 `mām`; P2#3 `prapadyate`; P3#1 `vāsudevaḥ`; P3#2 `sarvam`; P3#3 `iti`; P4#1 `saḥ`; P4#2 `mahātmā`; P4#3 `sudurlabhaḥ`
- `7.20` — P1#1 `kāmaiḥ`; P1#2 `taiḥ`; P1#3 `taiḥ`; P1#4 `hṛtajñānāḥ`; P2#1 `prapadyante`; P2#2 `anyadevatāḥ`; P3#3 `niyamam`; P3#4 `āsthāya`; P4#1 `prakṛtyā`; P4#2 `niyatāḥ`; P4#3 `svayā`
- `7.21` — P1#1 `yaḥ`; P1#2 `yaḥ`; P1#3 `yām`; P1#4 `yām`; P1#5 `tanum`; P1#6 `bhaktaḥ`; P2#1 `śraddhayā`; P2#2 `arcitum`; P2#3 `icchati`; P3#1 `tasya`; P3#2 `tasya`; P3#3 `acalām`; P3#4 `śraddhām`; P4#2 `eva`; P4#3 `vidadhāmi`; P4#4 `aham`
- `7.22` — P1#1 `saḥ`; P1#2 `tayā`; P1#3 `śraddhayā`; P1#4 `yuktaḥ`; P2#1 `tasya`; P2#2 `ārādhanam`; P2#3 `īhate`; P3#1 `labhate`; P3#2 `ca`; P3#4 `kāmān`; P4#1 `mayā`; P4#2 `eva`; P4#3 `vihitān`; P4#4 `hi`; P4#5 `tān`
- `7.23` — P1#1 `antavat`; P1#2 `tu`; P1#3 `phalam`; P1#4 `teṣām`; P2#1 `tat`; P2#2 `bhavati`; P2#3 `alpamedhasām`; P3#1 `devān`; P3#2 `devayajaḥ`; P3#3 `yānti`; P4#1 `madbhaktāḥ`; P4#2 `yānti`; P4#3 `mām`; P4#4 `api`
- `7.24` — P1#1 `avyaktam`; P1#2 `vyaktim`; P1#3 `āpannam`; P2#1 `manyante`; P2#2 `mām`; P3#1 `param` [flag — unchanged]; P3#2 `bhāvam` [flag — unchanged]; P3#3 `ajānantaḥ`; P4#1 `mama`; P4#2 `avyayam`; P4#3 `anuttamam`
- `7.25` — P1#1 `na`; P1#2 `aham`; P2#1 `yogamāyā`; P2#2 `samāvṛtaḥ`; P3#1 `mūḍhaḥ`; P3#2 `ayam`; P3#3 `na`; P3#4 `abhijānāti`; P4#1 `lokaḥ`; P4#2 `mām`; P4#3 `ajam`; P4#4 `avyayam`
- `7.26` — P1#2 `aham`; P1#3 `samatītāni`; P2#1 `vartamānāni`; P2#2 `ca`; P2#3 `arjuna`; P3#1 `bhaviṣyāṇi`; P3#2 `ca`; P3#3 `bhūtāni`; P4#1 `mām`; P4#2 `tu`; P4#3 `veda`; P4#4 `na`; P4#5 `kaścana`
- `7.27` — P1#1 `icchā`; P1#2 `dveṣa`; P1#3 `samutthena`; P2#1 `dvandvamohena`; P2#2 `bhārata`; P3#1 `sarvabhūtāni`; P3#2 `sammoham`; P4#2 `yānti`; P4#3 `parantapa`
- `7.28` — P1#1 `yeṣām`; P1#2 `tu`; P1#3 `antagatam`; P1#4 `pāpam`; P2#1 `janānām`; P2#2 `puṇyakarmaṇām`; P3#1 `te`; P3#2 `dvandvamohanirmuktāḥ`; P4#1 `bhajante`; P4#2 `mām`; P4#3 `dṛḍhavratāḥ`
- `7.29` — P1#1 `jarā`; P1#2 `maraṇa`; P1#3 `mokṣāya`; P2#1 `mām`; P2#2 `āśritya`; P2#3 `yatanti`; P2#4 `ye`; P3#1 `te`; P3#2 `brahma`; P3#3 `tat`; P3#4 `viduḥ`; P3#5 `kṛtsnam`; P4#1 `adhyātmam`; P4#2 `karma`; P4#3 `ca`; P4#4 `akhilam`
- `7.30` — P1#1 `sa`; P1#2 `adhibhūta` [flag — unchanged]; P1#3 `adhidaivam` [flag — unchanged]; P1#4 `mām`; P2#1 `sa`; P2#2 `adhiyajñam` [flag — unchanged]; P2#3 `ca`; P2#4 `ye`; P2#5 `viduḥ`; P3#1 `prayāṇakāle`; P3#2 `api`; P3#3 `ca`; P3#4 `mām`; P4#1 `te`; P4#2 `viduḥ`; P4#3 `yuktacetasaḥ`

Chapter 7 audit list: 418 speaker/pāda word occurrences total; 399 explicitly listed as unchanged/held, in addition to the changed-word table above.

**Carry-forward resolved in this chapter batch:** 7.06 `tathā` “also/and” is now `पनि / भी`, matching `उत्पत्ति र विनाश पनि / उत्पत्ति और विनाश भी` (old “thus” manner words were `त्यसरी / वैसे ही`). Its remaining shares in chapters 1, 8–10, 13 and 17 must wait for those chapters’ own batches. Carry-forward flags still open elsewhere: 4.16 `kavayaḥ`, 6.36 `matiḥ`, 16.05 and 18.66 `mā` / `śucaḥ`. No other chapter’s occurrence was changed here.

Appendix A audit is byte-identical before/after: **9,366 verse words / 9,484 glosses; §3 674 forms / 4,532 instances; `te` 0 / `me` 2**. The complete output is in `/home/user/evidence/batch13/appendix-a-after.txt`, equal to both `/home/user/evidence/appendix-a-pre-edit.txt` and `/home/user/evidence/appendix-a-baseline.txt`.

**Verification:** full §4 build green — strict pāda 2,800 / 0, all 2,100 paraphrase pairs, SEO 6, site-health 572, study 9,658, 19 Python tests, 802 document assertions, 15 + 7 Node tests and all **162 browser checks**. Playwright rendered-string assertions passed **102/102** (51 overrides × NE/HI). **16 screenshots** (four verses per chapter, both languages, 390 × 844) show the changed pāda expanded; evidence and index: `/home/user/evidence/batch13/screenshots/`, `rendered-string-assertions.json`, `screenshot-index.json`. Full build log: `/home/user/evidence/batch13/full-build.log`.

Full-repo checkpoint zip (outside Git): `/home/user/downloads/Bhagavad-Gita-700-titles.zip`; unzipped tree verified byte-identical with `diff -r` (tracked repository files; `.git` excluded).


**FIXED (2.1 batch 14, 2026-10-11) — chapters 6 and 8, verse by verse.** All 47
verses of chapter 6 and all 28 of chapter 8 were read word by word against
their English, Nepali and Hindi literals. **27 inline five-field overrides**
(18 in ch6, 9 in ch8; only `word[3]`/`word[4]`) across 23 verses; the other 52
verses are confirmed with reasons. Every verdict, the pre-change meanings and
the literal translations are in `/home/user/evidence/batch14/`:
`chapter6-review-worksheet.md`, `chapter8-review-worksheet.md`,
`fixes.json`, `reasons.json`, `holds.json`, `rendered-string-assertions.json`,
`screenshots/`. The **exhaustive unchanged-occurrence list** (1,011
occurrences; 625 in ch6, 386 in ch8, speaker lines included) is the appendix of
each worksheet.

Chapter 6 changed-word table (×N = same fix at N spots in the verse):

| Verse | Form / English | Old NE / HI | New NE / HI | Why |
|---|---|---|---|---|
| 6.04 | `sarva` “all” | हे सबै / हे सब | सबै / सब | In *sarva-saṅkalpa-sannyāsī* it quantifies intentions; literals सबै सङ्कल्प / सब संकल्पों. Stray vocative, same defect class as 2.65/3.13/4.21/4.26 |
| 6.06 | `varteta` “would abide” | बस्नुपर्छ / रहे | रहन्छ / रहता है | Optative read as an obligation; literals “आत्मा शत्रुझैं … रहन्छ” / “… रहता है” (present) |
| 6.11 | `ātmanaḥ` “his own” | आत्माको / आत्मा का | आफ्नो / अपना | *sthiraṃ āsanam ātmanaḥ* = a seat for himself; literals “आफ्ना निम्ति” / “अपने लिए” |
| 6.18 | `sarva` “all” | हे सबै / हे सब | सबै / सब | Quantifier in *sarvakāmebhyaḥ*; literals सबै कामनाका विषयहरूप्रति / सब कामनाओं के विषयों से |
| 6.19 | `yoginaḥ` “of the yogi” | योगीहरू / योगी | योगीको / योगी का | Genitive singular in *yogino yatacittasya*; literals “योगीको यही उपमा” / “योगी का दृष्टान्त” |
| 6.22 | `tataḥ` “than that” | त्यसैले / इसलिए | त्यसभन्दा / उससे | Ablative of comparison in *nādhikaṃ tataḥ*; literals “अरू कुनै लाभ श्रेष्ठ लाग्दैन” / “श्रेष्ठ नहीं लगता” |
| 6.24 | `sarvān` “all” | सबैलाई / सबको | सबै / सब | Bare accusative object of *tyaktvā*; literals “सबै कामनाहरूलाई … त्यागेर” / “सब कामनाओं को … त्यागकर” |
| 6.26 ×2 | `tataḥ` “from there” | त्यसैले / इसलिए | त्यसबाट / उससे | Correlative *yato yato … tato tato*; literals “त्यहीबाट फर्काएर” / “उसी से उसे लौटाकर” |
| 6.28 | `aśnute` “attains” | अनुभव गर्दछ / भोगता है | प्राप्त गर्छ / प्राप्त करता है | Literals “अनन्त सुख … प्राप्त गर्छ” / “प्राप्त होता है”; same fix as 3.04 |
| 6.34 | `pramāthi` “turbulent” | चञ्चल / चंचल | आवेगी / आवेगी | Had duplicated `cañcalam`’s gloss in the same pāda; literals “चञ्चल, आवेगी, …” / “चंचल, आवेगी, …” |
| 6.36 | `matiḥ` “opinion” | बुद्धि / बुद्धि | मत / मत | **Carry-forward flag from batch 13 closed.** Literals “भन्ने मेरो धारणा छ” / “मेरा यह मत है”; corpus already uses मत at 18.06/70/78 |
| 6.39 | `arhasi` “you should” | योग्य छौ / योग्य हो | पर्छ / चाहिए | Request, not “you are worthy”; literals “मेट्नुपर्छ” / “दूर करना चाहिए” (same as 3.20) |
| 6.43 | `tataḥ` “from there” | त्यसैले / इसलिए | त्यहीँबाट / वहीं से | *tato bhūyaḥ* = “from there again”; literals “त्यहीँबाट … फेरि” / “वहीं से … फिर” |
| 6.44 | `hriyate` “is carried” | लैजान्छ / ले जाया जाता है | तानिन्छ / ले जाया जाता है | Passive rendered as active “he leads”; NE literal “अघि बढ्छ” |
| 6.44 | `avaśaḥ` “involuntarily” | असहाय / असहाय | अनिच्छाले / अनिच्छा से | Literals “अनिच्छाले पनि” / “अनिच्छा से भी”, not “helpless” |
| 6.45 | `tataḥ` “then” | त्यसैले / इसलिए | त्यसपछि / तब | Sequential; literals “त्यसपछि” / “तब” (cf. 2.38) |
| 6.47 | `me` “in my view” | मेरो / मेरा | मेरो दृष्टिमा / मेरी दृष्टि में | *sa me … mataḥ*; literals “मेरो दृष्टिमा … मान्छु” / “मेरी दृष्टि में … मानता हूँ” |

Chapter 8 changed-word table:

| Verse | Form / English | Old NE / HI | New NE / HI | Why |
|---|---|---|---|---|
| 8.06 | `eti` “goes” | आउँछ / आता है | जान्छ / जाता है | Both literals say the opposite direction (“उसी अवस्थामा ऊ जान्छ” / “उसी अवस्था को प्राप्त होता है”) |
| 8.11 | `te` “to you” | तिम्रो / तुम्हारा | तिमीलाई / तुझे | Dative in *tad te padaṃ … pravakṣye*; literals “म तिमीलाई … भन्नेछु” / “मैं तुझे … कहूँगा” |
| 8.14 | `yoginaḥ` “yogi” | योगीहरू / योगी | योगीको / योगी का | Genitive singular *nityayuktasya yoginaḥ*; literals “सधैं युक्त योगीका निम्ति” / “सदा-युक्त योगी के लिए” (same defect as 6.19) |
| 8.20 | `paraḥ` “other” | परम / परम | पर / परे | *paras-tasmāt tu bhāvo ’nyaḥ* = “beyond that”; literals “यस अव्यक्तभन्दा पर अर्को” / “इस अव्यक्त से परे एक और” |
| 8.20 | `tasmāt` “beyond that” | त्यसकारण / इसलिए | त्यसभन्दा / उससे | Ablative inside *paras-tasmāt*; literals mark it भन्दा / से |
| 8.22 | `yasya` “in whom” | जसको / जिसका | जसमा / जिसमें | Locative of *yasyāntaḥsthāni bhūtāni*; literals “जसमा सबै प्राणी बस्छन्” / “जिसमें सब प्राणी रहते हैं” |
| 8.24 | `tatra` “by that path” | त्यहाँ / वहाँ | त्यस मार्गबाट / उस मार्ग से | Refers to the path just named, not a place; literals “त्यस मार्गबाट” / “उस मार्ग से” |
| 8.25 | `tathā` “also” | त्यसरी / वैसे ही | पनि / भी | List conjunction *dhūmo rātris tathā kṛṣṇaḥ*; manner “thus” was wrong (cf. 7.06, 11.34) |
| 8.25 | `tatra` “by that path” | त्यहाँ / वहाँ | त्यस मार्गबाट / उस मार्ग से | Same defect and fix as 8.24 |

**Deliberately left alone (52 of 75 verses confirmed as-is; every word read).**
Keeps that prove the fixes: `sarva` quantifier elsewhere (6.24/6.30, 8.07/8.18/8.22/8.27/8.28),
`tathā` manner “likewise” 6.07 (त्यसरी/वैसे ही, correct there), `tatra` locative 6.12/6.43 and
8.18 (“there”, correct), `tataḥ` causal/sequential keeps, `me` possessive 6.30 (batch-2 settle),
6.36/6.39/6.47 keeps as recorded, `tāta` 6.40 (a genuine vocative that keeps हे),
`avaśaḥ` 8.19 असहाय (correct: the beings dissolve helplessly), `ātmanaḥ` 8.12 आत्माको
(“his own breath”, matching its literals), `yoginaḥ` 8.23 योगीहरू (genuine plural there),
`brahmaṇaḥ` 8.17 ब्रह्मको (genuine genitive, unlike the comparative ablatives fixed at
11.37/18.69), `paraḥ` 8.22 परम (supreme Person, correct), voice-neutral infinitives
(`chettum` 6.39, `avāptum` 6.36), Krishna register तिमी/तुम, and the technical terms
अध्यात्म / अधिभूत / अधिदैव / अधियज्ञ / अधिदैवत (8.01–8.04, 8.14) kept as the literals keep them.

**Open carries after this batch:** 4.16 `kavayaḥ` (कविहरू/कवि — should be ज्ञानीहरू/ज्ञानी
like 18.02); `mā` → नगर and `śucaḥ` → शोक गर्छौ at 16.05 and 18.66 (wrong in every
occurrence); the additive `tathā` now lives only in chapters 1 (1.26, 1.34), 9 (9.32,
9.33), 10 (10.06, 10.13, 10.35), 13 (13.18) and 17 (17.07, 17.26) — 10 occurrences, for
those chapters’ own batches. **8.10’s verse text** (“सम्य क्स तं” / “samya ksa taṃ”, should
be सम्यक् स तं / samyak sa taṃ) is a text fix outside this batch’s scope — reported, not
changed. The 11.44 *praṇidhāya* literal decision still belongs to Dhruba.

Appendix A audit is byte-identical before/after: **9,366 verse words / 9,484 glosses;
§3 674 forms / 4,532 instances; `te` 0 / `me` 2** — `/home/user/evidence/batch14/appendix-a-before.txt`
and `appendix-a-after.txt` are equal to each other and to the batch-13 baseline.

**Verification:** full §4 build green — strict pāda 2,800 / 0, all 2,100 paraphrase pairs,
SEO 6, site-health 572, study 9,658, 19 Python tests, 802 document assertions, 15 + 7 Node
tests and all **162 browser checks**. Playwright rendered-string assertions passed
**54/54** (27 overrides × NE/HI, asserted structurally as “the word’s own Devanagari followed
by the new meaning” inside the expanded pāda). **94 sheets** (46 full 390 × 844 ne/hi sheets +
48 changed-pāda crops) are in `/home/user/evidence/batch14/screenshots/`, indexed by
`rendered-string-assertions.json`. Full build log: `/home/user/evidence/batch14/full-build.log`.


**FIXED (2.1 batch 15, 2026-10-11) — chapters 9 and 10, verse by verse.**
The pre-edit audit and full §4 build were reproduced after verifying PR #25's
merge at `e09f31e`. All 34 chapter-9 and 42 chapter-10 verses were checked
word by word against Sanskrit, each pāda split, and EN/NE/HI literals. **103
five-field overrides** changed only word[3]/word[4] (19 in ch9, 84 in ch10),
across 45 corrected verses; 30 verses are confirmed with a reason, and 9.34 is
flagged without a source edit. The worksheets in
`/home/user/evidence/batch15/chapter9-review-worksheet.md` and
`chapter10-review-worksheet.md` record all verdicts and reasons and enumerate
every one of the **904 unchanged speaker/pāda occurrences** (426 + 478).
Their scope guards confirm no Sanskrit/IAST, English gloss, verse text, pāda,
literal, paraphrase, speaker structure or other data leaf changed.

Chapter 9 fixes include dative `te` (9.01), the locative/demonstrative pair
`dharmasya`/`asya` (9.03), destination `prakṛtim` and object `tāni` (9.07),
`avaṣṭabhya`, the group `bhūtagrāmam`, and `vaśāt` (9.08), plus context-specific
lexical/case fixes through 9.32–33. The additive `tathā` is now `पनि / भी` at
9.32 and 9.33; `tathā` at 9.06 remains the correct correlative “so”. **9.34
remains flagged:** verse text has `युक्त्वैवम्` / `yuktvaivam`, while its split
word record says `एव` / `eva` and glosses “(एवम्) indeed”. Correcting that
requires a source/text edit outside this batch's word-field scope.

Chapter 10 fixes include the additive `tathā` at 10.06, 10.13 and 10.35;
respectful address to Kṛṣṇa in 10.13–18; dative/benefactive and object forms;
wrong person, mood, lexical sense and case; and explicit locatives for the
“among” vibhūti lists (especially 10.21–37). This is **not** a blanket
conversion of genitives: real genitives such as `devānām` and `maharṣīṇām` in
10.02 remain genitive, while explicit “among” contexts use locative forms.
`viṣṭabhya` at 10.42 retains NE `धानेर` because the local literal supports
“having supported”; it is not the separate 6.13 `dhārayan` orthography hold.

The batch resolves the `tathā` carries at 9.32–33 and 10.06/10.13/10.35. With
7.06 and 8.25 already resolved, the remaining additive uses are 1.26, 1.34,
13.18, 17.07 and 17.26. All other owner holds remain intact; see
`/home/user/evidence/batch15/holds.json`. Appendix A before/after is byte-
identical (9,366 verse words / 9,484 glosses; §3 674 / 4,532; `te` 0 / `me` 2;
SHA-256 `87d5ad0f989e09dc8f94c15ea11cd7813e96638f951449c3a5b5e03355158a4e`).
The full §4 build passed 2,800 pādas / 0 flags, 2,100 paraphrase pairs, 6 SEO,
572 site-health checks / 0 failures, 9,658 study checks, 19 Python tests, 802
document assertions, 15 + 7 Node tests and all 162 browser checks; it ended
`OK: index.html is fresh`. Structural Playwright checks passed **206/206**
(103 overrides × NE/HI). Evidence: 12 full 390 × 844 sheets (three per
chapter/language), 188 aligned contexts and 188 changed-pāda crops, all
indexed under `/home/user/evidence/batch15/`. This revision has no
`.m-scroll`, so `#modal` is the actual scroller; all 188 pāda contexts were
positioned as close as scroll range allows, with 54 boundary clamps recorded
in the index (the direct crops remain the exact expanded pāda boxes).

**Batch 16 carry:** 12.01 and 12.03 `paryupāsate` (EN “worship”) now use पूजा गर्छन् / पूजा करते हैं rather than अनुसरण गर्छन् / अनुसरण करते हैं. 12.02 and 12.04 confirmed. See `/home/user/evidence/batch16/chapter12-review-worksheet.md` for occurrence-by-occurrence decisions. At that point no other chapter-12 verses had been reviewed; batch 17 below completes chapter 12. Owner flags stayed open.

**FIXED (2.1 batch 17, 2026-10-11) — complete chapter 5 and remaining chapter 12.** All 29 verses of chapter 5 and 12.05–12.20 were reviewed against Sanskrit, exact pāda splits, all word entries and EN/NE/HI literals. **23 NE/HI-only word overrides** across 18 verses; 26 verses confirmed without changes; 12.19 flagged and retained. The two worksheets give a verdict and reason for every verse and list every word tuple. The exhaustive ledger covers **587 pāda-word occurrences + 4 speaker words = 591**, including all **568 unchanged occurrences**; the two expected 5.01 speaker words are included, and the two unchanged 5.02 speaker words are also enumerated for completeness (so the total is two above the 589-row pāda + 5.01 count). Source edits touch only NE/HI word fields in `source/padachheda_ch5.py` and `source/padachheda_ch12.py`; generated-data assertions confirm English, Sanskrit/IAST, verse text, pāda splits, literals, paraphrases and non-target entries are unchanged.

Reviewed-context notes: 5.09 `dhārayan` NE धानेर is retained with its local contextual rationale and is distinct from owner-held 6.13; 5.24 `tathā` is correctly “likewise” here; 12.18 `tathā` remains “so/likewise”. At 12.19 `yena kenacit`, the phrase-level sense is clear but the split-token mapping cannot be resolved without guessing, so the word rows stay untouched and flagged. Outstanding additive `tathā` remains at 1.26, 1.34, 13.18, 17.07 and 17.26. All owner holds and other carry-forward flags are preserved; see `/home/user/evidence/batch17/fixes-reasons-holds.md`.

Appendix A output is byte-identical before and after (SHA-256 `87d5ad0f989e09dc8f94c15ea11cd7813e96638f951449c3a5b5e03355158a4e`). The full §4 build passed: 2,800 pādas / 0 flags; 2,100 paraphrase pairs; 6 SEO; 572 site-health / 0 failures; 9,658 study checks; 19 Python tests; 802 document assertions; 15 + 7 Node tests; all 162 browser checks. Structural word-row assertions passed for all 23 overrides. Browser evidence: 12 full 390×844 sheets and all 42 changed-pāda crops (21 pādas × NE/HI); 14 scroll-boundary clamps recorded. The actual scroller was `#modal` because this checkout has no `.m-scroll`. Evidence and logs are in `/home/user/evidence/batch17/`.

The ledger is now **591/700 verses**; 109 remain in chapters 1, 13 and 17. This session stops after batch 17; no Phase 2.2 or other §6 task was started.

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
  - **Decided 2026-10-09 — see §7.2:** both are revised to the Śaṅkara reading
    in en/ne/hi (step 1.9). 18.66: no “other paths” — all dharma *and* adharma,
    the sense of doership itself; the refuge-and-promise half stays. 15.7: the
    hedge “as if an eternal portion” in the paraphrases and in the 15.7 theme
    title/desc; the literals stay literal. The 6.47 title is a separate,
    still-open bullet.
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

**Phase 1 — Correctness (1–2 days)** · **complete** (1.1–1.9 done, 2026-10-09)
- [x] 1.1 Fix the verse text in 7.12 and 9.13 (source and matching pāda lines).
- [x] 1.2 Fix word-list spellings: 11.27–29, 17.6, 1.1 and 2.14.
- [x] 1.3 Fix 13.27’s IAST spelling and update its Nepali/Hindi gloss keys.
- [x] 1.4 Add a strict validator that fails the build. Check each word’s
      Devanagari against its own IAST, and each pāda line against its word
      split, without flattening diacritics. Appendix A §1–2 is the starting point.
- [x] 1.5 Search: NFD plus explicit spelling folds; fix singular/plural result wording.
- [x] 1.6 Fix the `LICENSE.md` counts (9,484 / 169 / 700); removed the stale README editor section (editor not restored).
- [x] 1.7 Fix the Hindi grammar in the 2.47 paraphrase (की → के आलस्य).
- [x] 1.8 Replace “तीन निष्ठा / निष्ठाएँ” with the owner’s मार्ग wording (decided
      2026-10-09, spec in §7.1; value-only i18n change, keys and 202 count kept).
- [x] 1.9 Revise the 18.66 and 15.7 paraphrases to the owner’s Śaṅkara-aligned
      wording (decided 2026-10-09, spec in §7.2; en/ne/hi paraphrases plus the
      15.7 theme/verse copy; literals untouched).

**Phase 2 — Meaning** · in progress (2.1 batches 1–17; complete verse-by-verse
reviews now cover chapters 2–12, 14–16 and 18; chapters 1, 13 and 17 remain)
- [ ] 2.1 Context-correct Nepali/Hindi meanings via five-field entries (§5.2) —
      **in progress — batches 1–17 done** (`te` batch 1; `me`, `param`, `bhūtāni`,
      `yogam` batch 2; `tat`, `yat` batch 3; `bhīma`, `kutaḥ`, `sattvam` batch 4;
      `arjuna`, `samāḥ` batch 5; `me` = “to me” batch 6; ch4 batch 7 (24), ch14
      batch 8 (8), ch16 batch 9 (11), ch18 batch 10 (20), ch2 batch 11 (69),
      ch11+15 batch 12 (62 + 10), ch3+7 batch 13 (32 + 19), ch6+8 batch 14
      (18 + 9), ch9+10 batch 15 (19 + 84), ch12.01–.04 batch 16 (2), and full
      ch5 + ch12.05–.20 batch 17 (12 + 11)). **410 of 9,366 verse-word instances**
      have per-verse overrides from the full chapter-review batches (**486
      five-field entries corpus-wide**). Remaining chapters: 1, 13 and 17
      (**109 verses**). Open carries: 4.16 `kavayaḥ`; additive `tathā` at 1.26,
      1.34, 13.18, 17.07 and 17.26; `mā` / `śucaḥ` at 16.05 / 18.66 (approval
      required); and 9.34 source/split mismatch (flagged, not edited). `matiḥ`
      6.36 and additive `tathā` 7.06, 8.25, 9.32–33, 10.06/10.13/10.35 are
      resolved; 5.24 and 12.18 `tathā` were checked as non-additive “likewise”.
      Owner holds: 6.13 `dhārayan` NE धानेर; 6.29 English literal; 8.10 text
      (fix only with approval in its own small commit); 11.44 `praṇidhāya` literal
      (remind Dhruba; do not change). Other carry-forward flags and full details:
      §5.2 and `/home/user/evidence/batch17/fixes-reasons-holds.md`.
- [ ] 2.1x **Verse-by-verse verification of all 700 verses** (standing owner
      requirement, started 2026-10-11). Reviewed so far: **591/700 verses** —
      chapters 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16 and 18 (ch2
      72/72, ch3 43/43, ch4 42/42, ch5 29/29, ch6 47/47, ch7 30/30, ch8 28/28,
      ch9 34/34, ch10 42/42, ch11 55/55, ch12 20/20, ch14 27/27, ch15 20/20,
      ch16 24/24, ch18 78/78). Every reviewed verse has its word entries,
      EN/NE/HI literals, verdict (confirmed / corrected / flagged) and reason.
      Per-verse ledgers: ch4/14/16 in PR #20, ch18 in PR #21, ch2 in PR #22,
      ch11+15 in PR #23, ch3+7 in PR #24, ch6+8 in `/home/user/evidence/batch14/`,
      ch9+10 in `/home/user/evidence/batch15/`, 12.01–.04 in
      `/home/user/evidence/batch16/`, and ch5 + 12.05–.20 in
      `/home/user/evidence/batch17/`. **109 verses remain in chapters 1, 13 and
      17.** Nothing in the corpus may be called verified until all 700 are.
      No Phase 2.2 or other §6 item was started in batch 17.
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

Phase 1 is selected (2026-10-08). §7.1 and §7.2 are decided; §7.3–§7.7 remain open.
Numbering follows the old list, so “§7.1” and “§7.2” mean the same choices as
before.

### 7.1 “तीन निष्ठा” → “तीन मार्ग” — **DECIDED (owner, 2026-10-09)** · **IMPLEMENTED** (step 1.8, 2026-10-09)

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

**Evidence.** Before/after of every changed string, plus 390 px shots
of the Hindi and Nepali welcome tagline, the sections landing (three cards) and
a chapter page showing the way crumb, and one English sections landing to show
the Devanagari prefix. Then `grep -rn "तीन निष्ठा\|कर्मनिष्ठा\|भक्तिनिष्ठा\|ज्ञाननिष्ठा" source/
run_gita_app.js browser_checks.py README.md` must be empty.

### 7.2 Paraphrases of 18.66 and 15.7 — **DECIDED (owner, 2026-10-09)** · **IMPLEMENTED** (step 1.9, 2026-10-09)

**Decision.** Both paraphrases are revised, and both follow Śaṅkara. The
literal translations are not touched: the hedge and the gloss are
interpretation and belong in the paraphrase and the theme/verse descriptions,
so `gita_data15.py`’s header claim “Aligned to the Śaṅkara-bhāṣya readings”
becomes true again and is kept.

**18.66** (`gita_data18.py:254`, en paraphrase). The current “Give up all other
paths and surrender to me alone. I will release you from all sin — do not
grieve.” leans on “other paths”, as if one path were being chosen among
several. Śaṅkara reads *sarvadharmān parityajya* as all dharma *and* adharma —
every claim of doing, the sense of agency itself — not a menu of paths. The
English paraphrase is rewritten to that sense, keeping the refuge-and-promise
half of the verse. **Parity:** the Nepali (`translations_ne.py:1382`, “अरू सबै
बाटो छोडेर…”) and Hindi (`translations_hi.py:1382`, “दूसरे सब मार्ग छोड़कर…”)
paraphrases carry the same lean and are reworded with it — in Hindi
especially, now that मार्ग is the UI’s word for the three ways (§7.1).

**15.7** (`gita_data15.py:52`, en paraphrase). The current “An eternal spark of
myself becomes the living soul in this world; …” adds a particle-image the
verse does not have. Śaṅkara insists on *aṃśa iva* — “as if a part”, the self
being indivisible and the “portion” figurative. Rewritten with the hedge (“As
if an eternal portion of myself, …”). **Parity:** the ne/hi paraphrases
(`translations_ne.py:1120`, `translations_hi.py:1120`) already say अंश but
lack the hedge — it is added there too (मानौं / मानो); and the un-hedged theme
title/desc in `gita_data15.py:17–18` (“The eternal portion” / “An eternal
portion of Kṛṣṇa carries…”) rest on the same reading, so they are hedged or
reworded consistently, with the ne/hi mirrors in `themes_ne.py` /
`themes_hi.py` kept in step.

**Out of scope.** The 6.47 title “Most yoked” (separate §5.3 bullet; locked by
`study_map_contract.json` / `check_study_structure.py`, so it needs its own
decision); the 10.41–42 “spark” imagery in `STUDY_MAPS.md` and `gita_data10.py`
(different verse, correct as is); verse text, pādas and word lists; and
everything step 1.8 touched.

**Constraints and bookkeeping.** `source/check_paraphrase.py` caps
paraphrase↔literal overlap at 80 % (global max 79.8 % before this step): the
rewritten pairs must stay under it and still read as paraphrase, not copy. No
exact-text assertion quotes these strings (verified in `run_gita_app.js`,
`browser_checks.py`, `study_map_contract.json`); re-grep after rewording and,
if any appears, update it to the new string keeping its strength. Rebuild with
`build.py`; the expected generated churn is `data/ch15.js`, `data/ch18.js`,
`v/15.7/`, `v/18.66/` (og:description) and the `sw.js` cache id. Commit source
and generated files together.

**Evidence required.** Before/after of every changed string in every language
touched; 390 px screenshots of the 18.66 and 15.7 verse sheets in en, ne and
hi with the paraphrase visible, read back from the images (no truncation, no
leftover “spark” / “other paths”); the §4 browser setup, with the sandbox font
caveat from step 1.8 (small UI labels may render as boxes — not an app bug).

**As implemented (step 1.9).**
- 18.66 en: “Let go of all dharma and adharma alike, every sense of being the
  doer, and surrender to me alone. I will release you from all sin — do not
  grieve.” · ne: “धर्म र अधर्म सबै — आफू कर्ता हुँ भन्ने भाव नै — छोडेर केवल ममा
  समर्पण गर। …” · hi: “धर्म और अधर्म सब — अपने कर्ता होने का भाव ही — छोड़कर केवल
  मुझ में समर्पण कर। …” (the promise half unchanged in all three).
- 15.7 en: “As if an eternal portion of myself, the living soul in this world
  draws to itself the five senses and the mind, which rest in nature.” · ne:
  “यस संसारको जीवात्मा मानौं मेरै नित्य अंश हो; …” · hi: “इस संसार का जीवात्मा
  मानो मेरा ही नित्य अंश है; …”. Theme desc: “The living soul — as if an eternal
  portion of Kṛṣṇa — carries…” (ne/hi: “जीव — मानौं/मानो कृष्णको/कृष्ण का सनातन
  अंश — …”); verse title “As if an eternal portion” (ne/hi “मानौं/मानो नित्य
  अंश”); verse desc “As if an eternal portion of me, the living soul … draws…”.
- Overlap after: 18.66 en 60.5 / ne 67.3 / hi 66.3 %; 15.7 en 72.4 / ne 55.1 /
  hi 59.9 %. No assertion quoted the old strings. The `v/` pages no longer
  exist, so the generated churn was `data/ch15.js`, `data/ch18.js`,
  `chapter/15/`, `chapter/18/` and `sw.js`.

### 7.3–7.7 Still waiting on the owner

3. OK to add Śaṅkara notes (source: Mahadeva Sastry, 1897)?
4. Where audio would come from (licence, who records it).
5. OK to merge “Verses with translation” and “Study guide” into one view?
6. OK to delete the dead files in §5.7?
7. `PROJECT.md` §8 asks every session to deliver the full repo zip. With GitHub
   as the checkpoint, is that still wanted?

## 8. Session log (newest first, one line each)

- 2026-10-11 · `arena/cbe968bc-bhagavad-gita` · Phase 2.1 batch 17 (chapter 5 + 12.05–12.20): reviewed 45 verses/180 pādas and 591 word occurrences; 23 NE/HI-only corrections across 18 verses, 26 confirmed, 12.19 flagged, and 568 unchanged occurrences exhaustively listed. Appendix A byte-identical; full §4 build green (162 browser checks); 12 full 390×844 sheets + 42 changed-pāda crops with 14 boundary clamps; evidence in `/home/user/evidence/batch17/`. Ledger 591/700; 109 remain in chapters 1, 13 and 17. Owner holds preserved. Source commit `406c766` pushed to the assigned branch; [PR #28](https://github.com/chapain/Bhagavad-Gita/pull/28) open to `main` (PR number recorded in second commit `9b50b43`). The final `/home/user/downloads/Bhagavad-Gita-700-titles.zip` was refreshed from this worktree and passed byte-identical extraction comparison with `diff -r` excluding `.git`. No second batch or Phase 2.2 work.

- 2026-10-11 · `arena/ce051313-bhagavad-gita` · batch 16: PR #26 merged; four verses (12.01–12.04) reviewed, two NE/HI-only changes. Pre/post full build green and audit byte-identical; chapter-12 remaining verses left unreviewed at that time. Evidence in `/home/user/evidence/batch16/`. Owner decisions held. PR #27 opened for Dhruba to merge; no second batch.


- 2026-10-11 · `arena/9704c065-bhagavad-gita` · Phase 2.1 batch 15 (chs 9+10):
  verified PR #25 merged to `main` at `e09f31e`; reproduced Appendix A and the
  green pre-edit §4 build. Reviewed all 76 verses against Sanskrit, pāda splits
  and EN/NE/HI literals; 103 NE/HI-only five-field overrides (19+84), 30 verses
  confirmed with reasons, 9.34 flagged, and 904 unchanged occurrences exhaustively
  listed in the two worksheets. Appendix A is byte-identical (SHA-256
  `87d5ad0f989e09dc8f94c15ea11cd7813e96638f951449c3a5b5e03355158a4e`). Final
  §4 build green (2,800/0 pāda; 2,100 paraphrase; 6 SEO; 572 site-health; 9,658
  study; 19 Py; 802 doc; 15+7 Node; 162 browser). Structural rendered-string
  assertions 206/206; 388 screenshots indexed (12 full sheets, 188 pāda
  contexts, 188 crops). The base lacks `.m-scroll`; `#modal` was positioned and
  its 54 scroll-boundary clamps are recorded in the screenshot index. Ledger:
  542/700; 158 remain in chs 1, 5,
  12, 13, 17. Existing owner holds are preserved; only additive `tathā` at
  9.32/33 and 10.06/13/35 resolved. Source commit `f36602a` is pushed only to
  the assigned branch; [PR #26](https://github.com/chapain/Bhagavad-Gita/pull/26)
  is open to `main` for Dhruba to review and merge. After this PR-number
  recording commit, `/home/user/downloads/Bhagavad-Gita-700-titles.zip` was
  refreshed and its extraction passed byte-identical `diff -r` with `.git`
  excluded. No second batch.

- 2026-10-11 · `arena/20d19a48-bhagavad-gita` · Phase 2.1 batch 14 (chs 6+8),
  PR #25: confirmed PR #24's merge by content at `05dc983` (the clone was shallow,
  so `git fetch --unshallow` was needed); reproduced Appendix A and passed the
  baseline §4 build green before any source edit. Reviewed all 47 + 28 verses
  against their en/ne/hi literals; **27 NE/HI-only overrides** (18 ch6 + 9 ch8)
  across 23 verses, the other 52 confirmed with reasons — worksheets, changed-word
  tables and the exhaustive unchanged-occurrence list (1,011 occurrences) in §5.2.
  Closed the 6.36 `matiḥ` carry-forward (मत) and fixed the additive `tathā` at 8.25;
  all other carry-forward flags and owner holds untouched. Appendix A
  byte-identical (9,366 / 9,484; §3 674 / 4,532; `te` 0 / `me` 2). Final §4 build
  green: all 162 browser checks passed, with 54 rendered-string assertions and 94
  390 × 844 ne/hi sheets (46 full sheets + 48 changed-pāda crops). Source verifier
  and `git diff --check` passed; ledger now records **466/700 verses reviewed**.
  Full-repo zip `/home/user/downloads/Bhagavad-Gita-700-titles.zip` round-tripped
  byte-identically with `diff -r`. Source commit `2076740` pushed only to this
  branch; [PR #25](https://github.com/chapain/Bhagavad-Gita/pull/25) open from
  `arena/20d19a48-bhagavad-gita` to `main`. Open flags reported: 8.10 verse text (सम्य क्स तं / samya ksa taṃ
  → सम्यक् स तं / samyak sa taṃ), 6.13 NE धानेर, 6.29’s English literal, 4.16
  `kavayaḥ`, `mā` / `śucaḥ` 16.05 / 18.66, and the 11.44 *praṇidhāya* reminder.

- 2026-10-11 · `arena/39ceb621-bhagavad-gita` · Phase 2.1 batch 13 (chs 3+7),
  [PR #24](https://github.com/chapain/Bhagavad-Gita/pull/24): confirmed PR #23's
  merge by content at `1b7b83c`; reproduced Appendix A and passed the baseline
  §4 build before source edits. Reviewed all 73 verses vs en/ne/hi literals;
  51 NE/HI-only overrides (32+19), with worksheets, rationale, changed-word
  tables and exhaustive unchanged-occurrence lists in §5.2. Resolved only the
  ch7 7.06 `tathā` carry-forward; other carry-forward flags and owner holds
  remain untouched. Appendix A identical (9,366 / 9,484; §3 674 / 4,532;
  `te` 0 / `me` 2). Final §4 build green: all 162 browser checks passed,
  with 102 rendered-string assertions and 16 390 × 844 screenshots. Source
  verifier and
  `git diff --check` passed; ledger records 391/700 verses reviewed. Full-repo
  zip `/home/user/downloads/Bhagavad-Gita-700-titles.zip` round-tripped
  byte-identically with `diff -r`. Source commit `a3e4b54` pushed only to this
  branch; PR #24 open to `main`. No further batch or Phase 2 work started.

- 2026-10-11 · `arena/bd59979f-bhagavad-gita` · Phase 2.1 batch 12 (chs 11+15):
  verified PR #22 merged at `5c82e69` on `main`; audit reproduced (`te` 0 /
  `me` 2; 9,366 / 9,484; §3 674/4,532) and baseline full build green. First
  two-chapter batch (~75-verse budget): all 55 verses of ch 11 and all 20 of
  ch 15 read against en/ne/hi literals. 72 five-field overrides (word[3]/
  word[4] only): ch11 62 in 37 verses (te-to-you ×10, tvām-into-you ×2,
  mā-owner-flag 11.34+11.49×2, tathā-and/also ×3, tataḥ ×3, atha ×2, deva-
  vocative ×3, devam/īśam/aprameyam case, manyase/icchasi/asi person+tense,
  bhava-origin, antaram, soḍhum, tapantam, uṣmapāḥ, sūtaputraḥ,
  prapitāmahaḥ, prasabham, yat-correlative, ekaḥ, brahmaṇaḥ-comparative,
  garīyase-spelling, prakṛtim, tapasā, yodhamukhyaiḥ, nadīnām, pravṛttim,
  divi, bhāsaḥ, dyāvāpṛthivyoḥ, pravyathitāntarātmā-form, ātmānam ×2,
  me ×2, tava), ch15 10 in 8 verses (enam-this, tataḥ-sequential,
  pravṛttiḥ-course owner flag → प्रवाह/धारा, īśvaraḥ-lord-of-body → स्वामी,
  acetasaḥ, gām, vaiśvānaraḥ, deham, sarvaiḥ, uttamaḥ-superlative); 30
  verses confirmed with keeps recorded (padam settle, nivartante mirror,
  adhiṣṭhāya mirror, īśvaraḥ divine mirror, quotative iti, optative syāt,
  voice-neutral infinitives, Krishna register). Flagged for owner: 11.44 NE
  literal “शरीर थपथपाउँछु” for praṇidhāya (literal-level, HI right);
  mā/śucaḥ 16.05/18.66 + kavayaḥ 4.16 + matiḥ 6.36 + tathā chs 1/7–10/13/17
  remain on the revisit list. Audit after identical; lockstep diff only
  ch11/ch15 data + sw.js. Full Playwright build green (2,800/0, 2,100
  paraphrase, 6 SEO, 572 health, 9,658 study, 19 Py, 802 doc, 15+7 Node,
  162 browser). Eight 390×844 ne/hi full sheets (11.34/37/39/49, 15.04/11/
  13/14) + 34 render assertions + 34 crops. Screenshots:
  `/home/user/evidence/batch12/`. Churn: source+data ch11/ch15 + sw.js
  cache id. PR #23 (this PR). Stop before the next batch.

- 2026-10-11 · `arena/e4875989-bhagavad-gita` · Phase 2.1 batch 11 (ch 2):
  verified PR #21 merged at `c637597` on `main`; unshallowed; batch-10
  content re-verified (ch18 24 five-field, corpus 139, 9,366/9,484, audit
  `te` 0 / `me` 2, §3 674/4,532) and baseline full build green. Read all 72
  verses of ch 2 against en/ne/hi literals; 69 five-field overrides in 41
  verses (mā×4, śreyaḥ-better×2, naḥ-for-us, dhārtarāṣṭrāḥ, bhaviṣyāmaḥ,
  ataḥ-from-now, yam×2, enam×11, vijānītaḥ, bhūtvā-been×2, nityam-eternal,
  atha×2, dhruvam, avyakta×2, madhyāni, tataḥ×3, -syasi×4, bhūtāni-people,
  atiricyate, uparatam, duḥkhe/alābhau/ajayau, yujyasva-engage, te-to-you,
  imām×2, bhayāt-from, yām, niryogakṣemaḥ, anviccha, phalahetavaḥ,
  duṣkṛte, kim-how×2, sarvān×2, sarvaśaḥ-sides, nivartate, haranti/harati,
  tāni, ātmavaśyaiḥ, sarva-of-all, carati, sthitiḥ); 31 verses confirmed
  with keeps recorded (incl. §7.1-neutral `tathā`, batch-2/4 settled
  `param`/`kutaḥ`/`padam`). Flagged for owner: `mā`→नगर wrong in all 5
  other occurrences (11.34, 11.49×2, 16.05, 18.66) + `śucaḥ` indicative,
  for revisit batches; EN-only slips preserved. Audit after identical;
  lockstep 138 leaves (69+69 mirror), only words[3]/words[4]. Full
  Playwright build green (2,800/0, 2,100 paraphrase, 6 SEO, 572 health,
  9,658 study, 19 Py, 802 doc, 15+7 Node, 162 browser). Twenty 390×844
  ne/hi full sheets + 113 render assertions + 6 crops read back.
  Screenshots: `/home/user/evidence/batch11/`. Churn: source+data ch2 +
  sw.js cache id. PR #22 (this PR). Stop before the next batch.

- 2026-10-11 · `arena/207086dc-bhagavad-gita` · Phase 2.1 batch 10 (ch 18):
  verified PR #20 merged at `9a56dea` on `main`; unshallowed; audit reproduced
  (`te` 0 / `me` 2; 9,366 / 9,484; §3 674/4,532). Read all 78 verses of ch 18
  against en/ne/hi literals; 20 five-field overrides (kavayaḥ, tyajet, labhet,
  me-from ×3, tathā-and, kṛtsnavat, ebhiḥ, brahmakarma, pravṛttiḥ, te-to ×2,
  te-by, iṣṭaḥ-dear, tasmāt-than ×2, matiḥ ×2, bhūtiḥ), ~460 flagged occurrences
  read and left; keeps recorded (incl. §7.1 `niṣṭhā`). Flagged for owner: 4.16
  same `kavayaḥ` defect, 18.53 backwards ne/hi literals for *nirmamaḥ*, and the
  `tathā`/`matiḥ`/`pravṛttiḥ` shared-form pool. Full Playwright build green
  (2,800/0, 2,100 paraphrase, 6 SEO, 572 health, 9,658 study, 19 Py, 802 doc,
  15+7 Node, 162 browser); audit after identical. Twelve 390×844 ne/hi sheets
  (18.02/42/69/78 + 4.16 + 16.20) captured and read back. Churn: data/ch18.js +
  sw.js cache id. PR #21: https://github.com/chapain/Bhagavad-Gita/pull/21.
  Stop before the next batch.

- 2026-10-11 · `arena/5afb9e8c-bhagavad-gita` · Phase 2.1 batches 7–9:
  verified PR #19 merged at `7de6723` on `main` (batch 6 content re-verified:
  9 five-field `me` = “to me” entries at 12.14–12.17/19/20 and 18.64/65/69, and
  the 2 possessive keeps); unshallowed before ancestry checks; ran the
  Appendix A audit. New standing task from the owner: **verify all 700 verses
  one by one**, a chapter per batch. Read all 42 verses of chapter 4, then all
  27 of chapter 14, then all 24 of chapter 16 against their en/ne/hi literals;
  wrote 22 + 8 + 11 five-field overrides (43 total) and read and left the
  remaining 572 flagged occurrences with reasons. Audit run from a pristine
  `7de6723` worktree and from the working tree is byte-identical (`te` 0 /
  `me` 2; 9,366 / 9,484; §3 674/4,532) — every fix is per-occurrence and
  nothing global moved in these chapters. Full Playwright build green
  (strict 2,800/0, 2,100 paraphrase pairs, 6 SEO, 572 site-health, 9,658
  study-structure, 19 Python tests, 802 document assertions, 15 + 7 Node
  tests, all 162 browser checks). Sixteen 390 × 844 ne/hi sheets across
  chapters 4, 14 and 16 captured and read back with the changed pāda expanded.
  Generated churn: `data/ch4, ch14, ch16` + `sw.js` cache id. PR #20:
  https://github.com/chapain/Bhagavad-Gita/pull/20. Stop before the next batch.
- 2026-10-11 · `arena/a84af58b-bhagavad-gita` · Phase 2.1 batch 6
  (`me` = "to me" cleanup): verified PR #18 merged at `5d8cdfe` on `main`;
  unshallowed before ancestry checks; verified batch 5 on `origin/main` (two
  five-field overrides at 1.04, 9,366 / 9,484 counts, audit `te` 0 / `me` 10).
  Inspected the remaining pool; selected `me` = "to me" + NE मेरो (10 audit-
  flagged verses). Each checked against its Sanskrit text and own en/ne/hi
  literal translation: 9 entries across 8 verses needed मलाई/मुझे; 2 left
  alone (9.29 possessive, 18.69 pāda 1 possessive). All 84 `mām`, 24 `mama`
  and 20 `mayi` verified correct. Audit §3 before `te` 0 / `me` 10;
  after `te` 0 / `me` 2; 9,366 / 9,484 unchanged. Full Playwright build green
  incl. 162 browser checks. Six 390 × 844 ne/hi screenshots for 12.14, 18.65
  and 9.29 across chapters 12, 18 and 9; all show correct meanings.
  Generated churn: `data/ch9, ch12, ch18` + `sw.js` cache id. PR #19:
  https://github.com/chapain/Bhagavad-Gita/pull/19. Full repository zip:
  `/home/user/Bhagavad-Gita-phase2.1-batch6.zip`. Stop before the next batch.

- 2026-10-11 · `arena/afa097ba-bhagavad-gita` · Phase 2.1 batch 5
  (`arjuna`, `samāḥ`): verified PR #17 merged; unshallowed before ancestry
  checks and content-verified batch 4 on `origin/main` (six exact entries, all
  13 deliberate keeps, 9,366 / 9,484 counts). Dhruba flagged 1.04 pāda 2 and
  delegated editorial judgement after the four-word pāda was checked against
  its Sanskrit split, English word glosses and en/ne/hi literals. Added two
  five-field overrides: `arjuna` “and Arjuna” → र अर्जुन / और अर्जुन and
  `samāḥ` “equal” → समान / समान. All 22 other `arjuna` vocatives and 6.41
  `samāḥ` “years” were deliberately kept; both occurrences of each form were
  checked. Lockstep generated-data diff: only word[3]/word[4] changed in the
  mirrored flow+padas records; text, split, English and prose untouched. Audit
  §3 before/after `te` 0 / `me` 10; 9,366 / 9,484 unchanged. Full Playwright
  build green incl. 162 browser checks. Six 390 × 844 ne/hi screenshots for
  1.04, 2.02 and 10.41 across chapters 1, 2 and 10 captured/read back; 1.04
  shows new meanings, 2.02/10.41 visually confirm settled batch-4 overrides.
  Implementation commit `733393a`; PR #18:
  https://github.com/chapain/Bhagavad-Gita/pull/18. Full repository zip:
  `/home/user/Bhagavad-Gita-phase2.1-batch5.zip`. Stop before the next batch.

- 2026-10-10 · `arena/dc2baaac-bhagavad-gita` · Phase 2.1 batch 4: PR #16
  merged; unshallowed before ancestry checks; verified all 21 batch-3 five-field
  entries and 9,366 / 9,484 counts on main by content. Owner delegated scope
  and calls after review of the remaining pool. Six entries changed for
  `bhīma`, `kutaḥ`, `sattvam`; all 19 occurrences reviewed, 13 deliberately
  kept (§5.2). Audit §3 before/after `te` 0, `me` 10. Lockstep data diff: only
  24 mirrored `words[3]`/`words[4]` leaves changed. Full build green incl. 162
  browser checks; twelve 390×844 ne/hi sheets across chapters 1, 2, 10, 13,
  18 captured and read back. Full repo zip:
  `/home/user/Bhagavad-Gita-phase2.1-batch4.zip`. PR #17:
  https://github.com/chapain/Bhagavad-Gita/pull/17. Stop before batch 5.

- 2026-10-09 · `arena/e1647b45-bhagavad-gita` · Phase 2.1 batch 3
  (`tat`, `yat`): verified PR #15 merged and matched batch-2 source content on
  `main` (requested 6/1/1/1/1 entries); unshallowed the clone, then checked
  `origin/main` ancestry. Added 21 AST-located five-field entries across
  chapters 1, 2, 3, 9, 11, 13, 15 and 17. All `tat` “that” uses (73), 3.02
  “therefore”, 14.07/14.08 “it”, all 55 `yat` “which” uses, 10.41×2
  “whatever”, and 18.60 “what” were deliberately kept; other judgement calls
  and the 11.07 “whatever” entry (omitted from the prompt parenthetical) are in
  §5.2. Appendix A §3 before/after unchanged (`te` 0; `me` 10); 9,366 / 9,484
  counts unchanged. Lockstep data comparison: only `words[3]`/`words[4]`
  changed (42 mirrored leaves). Full build green incl. 162 browser checks; 20
  390×844 ne/hi sheets read back across chapters 1, 3, 9, 13, 15 and 17.
  Generated `data/ch1, ch2, ch3, ch9, ch11, ch13, ch15, ch17` + `sw.js`.
  Implementation commit `80cf25e`; PR #16:
  https://github.com/chapain/Bhagavad-Gita/pull/16. Full repo zip:
  `/home/user/Bhagavad-Gita-phase2.1-batch3.zip`.

- 2026-10-09 · `arena/778427cd-bhagavad-gita` · Phase 2.1 batch 2 (`me`, param,
  bhūtāni, yogam): verified PR #14 merged at `0ea44a3` (carrying `ee2e9af`), so
  batch 1 was not repeated — the 26 `te` five-field entries are on `main` and
  audit §3 `te` = 0. Added 10 five-field entries by AST span (some `["मे", "me",
  "to me"]` strings are duplicated in a file, so no invented `old`): `me` “to me”
  → मलाई / मुझे at 2.7, 5.1, 6.30, 9.26, 11.4 and 11.45-*darśaya*; 11.45-*mano*
  pinned मेरो / मेरा; `param` 2.12 → भविष्यमा / भविष्य में; `bhūtāni` 9.25 →
  भूतहरू / भूत; `yogam` 11.8 → ऐश्वर्य. `yogam` 10.7 kept as योग (its own literal
  says योग). The two owner calls (6.30, yogam) came back “use your best
  intelligence”, so craft decided both and §5.2 records the reasoning. Audit §3
  `me` 16 → 10 (9.29 + the *sa me priyaḥ* set stay by design); 9,366 / 9,484
  unchanged; a lockstep walk of every data leaf shows only `words[3]`/`words[4]`
  moved (36 leaves = 9 edits × 2 languages × the flow+padas mirror), so no verse
  text, pāda, English gloss, title or paraphrase changed. Full build green incl.
  162 browser checks; 20 390 px ne/hi sheets for 2.07, 2.12, 5.01, 6.30, 9.25,
  9.26, 11.04, 11.08 and 11.45 (both `me`) read back clean across chapters 2, 5,
  6, 9 and 11. Generated churn: `data/ch2, ch5, ch6, ch9, ch11` + `sw.js` cache
  id. Stopped before batch 3 (owner picks the slice).

- 2026-10-09 · `arena/431645f7-bhagavad-gita` · Phase 2.1 batch 1 (`te`): verified
  PR #13 merged at `9db111e` (carrying `ad1f752`, `5c71004`, `d8a57f9`), so 1.9 was not
  repeated. Five-field entries for the 26 §5.2 verses: nominative तिनीहरू / वे; all 26
  read “they” in context, none “your”. Audit §3 `te` 26 → 0; 9,366 / 9,484 unchanged.
  Full build green incl. 162 browser checks; 390 px ne/hi sheets for 1.33, 9.21,
  16.08 and 13.25 read back. Stopped before batch 2 (`me`).

- 2026-10-09 · `arena/a27b2d91-bhagavad-gita` · Phase 1 step 1.9: verified PR #12
  merged at 03:30 UTC (`0828287`, carrying `18b6074` + `681d12c`), so 1.8 was
  not repeated. First commit wrote the owner’s §7.2 decision (and §1/§5.3/§6
  annotations) into HANDOFF.md. Then re-aligned the 18.66 paraphrase (all dharma
  and adharma, the sense of doership — no “other paths”) and the 15.7 paraphrase
  (*aṃśa iva* hedge, “spark” gone) in en/ne/hi, hedging the 15.7 theme/verse copy
  in `gita_data15.py`, `themes_ne.py`, `themes_hi.py` and the `STUDY_MAPS.md`
  quote; literals untouched; all six overlaps fell (worst 72.4 %). Build green
  incl. 162 browser checks; 390 px en/ne/hi sheets for both verses read back
  clean. **Phase 1 complete.** Stopped before Phase 2 (owner picks the item).

- 2026-10-09 · `arena/7d566d9b-bhagavad-gita` · Phase 1 step 1.8: verified PR #11
  merged at 02:43 UTC (`5010648`, carrying `b5a5bcd`), so step 1.7 was not
  repeated. First commit wrote the owner’s §7.1 decision (and §1/§5.3/§6
  annotations) into HANDOFF.md, which PR #11 could not carry. Then implemented
  §7.1: 25 value-only strings in `i18n_ui.py` (तीन मार्ग; कर्ममार्ग / भक्तिमार्ग /
  ज्ञानमार्ग in en/ne/hi; Hindi sections_sub re-agreed to masculine मार्ग), keys
  and the 202 count untouched, wayName() comment and browser_checks.py:328
  reworded; verse-level निष्ठा (3.3, 5.17, 17.1, 18.50, glosses, themes) left
  alone. Build green incl. 162 browser checks; 390 px hi/ne/en shots read back
  clean; the §7.1 grep now empty. Stopped before 1.9 (§7.2 still open).

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
