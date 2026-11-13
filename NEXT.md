# NEXT.md — what is actually left

**Updated 2026-11-04.** Base `801a99f` — the merge of PR #72 on `main` (PR #70 was `2b33495`). Baseline measured by `python3 build.py` at that commit, not quoted from a chat log.

> The previous edition of this file (dated 2026-10-19) presented Phases A–E as future work. Almost all of it has since shipped, so it was misleading as a to-do list. Its full text and history are archived verbatim at [`docs/archive/NEXT-2026-10-19.md`](docs/archive/NEXT-2026-10-19.md); this file is only the remainder. If an item below is finished, delete it rather than appending a log — history belongs in `HANDOFF.md` §1 and `docs/archive/`.

---

## 0. Already shipped — do not re-plan these

Verified in source at `2b33495`, not assumed:

| Plan item | Where it lives | Evidence |
|---|---|---|
| A1 skip-to-content | `source/app.html:157` | `<a href="#view" class="skip-link" id="skipLink">` |
| A2 font preload | `source/app.html:22–23` | both WOFF2 files, `as="font" crossorigin` |
| A5 backup-age badge | `source/js/45-data.js:20` | `dataBackupLine()` → `backupLine` export |
| B spaced repetition | `source/js/20-learn.js` | `box`/`due`/`reps` validation, `srsDueChapter`, `srsDueAll`, `srsStreakCount` |
| C1 match highlight | `source/js/12-search.js:39` | `<mark class="srch-hl">` |
| C2 suggestions | **withdrawn 2026-11-04** | the floating listbox covered the live results and offered the reader's own past queries back; the field is a plain input again and Enter searches. Locks now guard the removal (`run_gita_app.js`, `tests/test_search.js`, 2 browser checks) |
| C3 fold fallback | `source/js/12-search.js:154–166` | `searchFoldAlternative()` + `search_meant` note |
| C4 recent searches | **withdrawn 2026-11-04** | `gitaRecent` is gone; nothing is stored. The zero-result screen keeps four real starters (2.47 · 4.7 · 18.66 · धर्मक्षेत्रे) |
| Semantic audit — every verse read | **shipped 2026-11-04** | all 700 verses of all 18 chapters read against the Sanskrit — Devanagari, IAST, literal (en/ne/hi), paraphrase (en/ne/hi), title, and every word row with its three glosses. The ledger is [`docs/semantic-audit.md`](docs/semantic-audit.md); nine findings in seven verses (1.04, 1.13, 1.24, 1.46, 2.10, 3.22, 5.12). `tests/test_semantic_audit.py` — 10 tests over all 700 verses |
| C5 empty state | `source/js/12-search.js:171` | `search_try` hint in en/ne/hi |
| D3 print stylesheet | `source/css/60-responsive.css:217` | `@media print` hides chrome, `break-inside:avoid` |
| D4 recently viewed | `source/js/50-reader.js:126–145` | `gitaRecentVerses` (sessionStorage, capped 6), `.m-recent` row |
| E1 FAQPage | `source/app.html:120` | FAQ rich results already eligible |
| E1 `Book` JSON-LD | `source/app.html` (third `ld+json` block) | own node at `#book`: Vyāsa, translator Dhruba, sa/en/ne/hi, `EBook`, free, `creditText`; `WebApplication.about` links by `@id`; the false `numberOfPages: 18` is gone; 8 new `check_site_health.py` checks (552 → 560) |
| D1 copy verse as rich text | `source/js/50-reader.js` (`verseShareHtml`, `copyVerseText`) | language-following verse + link as `text/html` beside `text/plain` via `ClipboardItem`, synchronous write for iOS, plain-text fallback; 3 `run_gita_app.js` assertions (937 → 940) |
| D2 word-gloss peek | `source/js/50-reader.js` (`openWordPeek`) + `50-reader-shell.css` | long-press (450 ms, cancelled by a 10 px move), tap, `Enter`/`Space`, right-click on a word row → all three glosses; `aria-expanded` + `Escape`; 3 assertions (940 → 943) |
| E2 chapter titles + descriptions | `source/build_gita.py` `CHAPTER_TOPICS` | 18 unique titles (≤60, longest 57) and descriptions (≤155, longest 153), each naming its chapter, verse count and three languages; guarded by `source/check_seo.py` (10 checks) and two `run_gita_app.js` assertions |

So `REVIEW.md` §20's "High value" list was also out of date; it is annotated there now.

---

## 1. Remaining, in value order

### A2/A3 — axe sweep *(the axe half is done; Lighthouse still owed)*
**0 axe violations** is now a check, not a hope: `browser_checks.py` loads vendored
axe-core 4.14.0 (`tests/axe.min.js`, MPL-2.0, no npm, no bundler) in the browser CI
already installs and requires zero WCAG 2.0/2.1/2.2 A+AA violations on welcome,
the reader sheet, search, learn, favorites, the chapter view and the method page.
The first run of that sweep found three real defects (two `aria-label`s that
dropped their own visible text from the accessible name, and a 4.49:1 link on the
method page); they were fixed in `source/`, not suppressed. Lighthouse's numeric
100/100 is still unmeasured and still drifts with Chrome versions — the numeric
target is not a requirement, so treat it as an optional extra rather than a gate.

---

## 2. Owner-only — say so, don't attempt

- **GitHub topics:** `triligual` → `trilingual`, add `hindi`. The API returns 403 ("Resource not accessible by integration"); only the About → gear UI works.
- **E3 — post the kit in `docs/outreach.md`:** r/bhagavadgita, r/Hinduism, r/Nepal, one Quora answer, one Nepali group. The drafts and cadence are written; nothing has been posted.
- **E4 — analytics:** the recommendation on record is **skip**. Search Console answers the growth question, and adding a script would falsify the provenance page's "no analytics" sentence in the same commit.
- **`docs/title-review.md`:** 700 rows with tick boxes, generated by `python3 source/audit_titles.py --markdown`. It is Dhruba's read-through. Machine checks keep titles consistent; only reading keeps them honest. Never tick or edit a title for him.

---

## 3. Standing constraints (they bind every item above)

- `source/ch1.json` … `ch18.json` are canonical. Code renders and validates; it never invents or duplicates text.
- Never hand-edit generated files (`index.html`, `data/ch*.js`, `chapter/*/`, `method/index.html`, `chapter.css`, `sw.js`, `sitemap.xml`, `robots.txt`, `404.html`, fonts/icons). Change `source/`, run `python3 build.py`, keep both diffs together.
- **JS module guard is 700 lines and never moves.** Next tightest at this commit: `20-learn.js` 589, `50-reader.js` 546, `10-library.js` 475, `48-reader-view.js` 184. Split along a real seam (presentation vs the state that owns it) and list new files in `APP_JS_FILES` sorted.
- Shell cap **375,000 chars** (currently **365,940 — 9,060 of room**), enforced in `source/check_site_health.py`. The audit's own text corrections moved it by 61 characters; it is still the 700-line module guard that binds first. The cap stopped being the binding constraint on 2026-11-04, when the withdrawn suggestion listbox freed 7,852 characters; the 700-line module guard binds first again.
- Nepali and Hindi UI strings contain no Latin characters.
- Counts stay synchronized across code, README, PROJECT.md, HANDOFF.md, build.py and docs. Never print a success line unless the command actually succeeded.
- Browser checks are **346** over http (337 over file://). They now run in this sandbox too
  via a vendored Chromium (`GITA_CHROMIUM_EXECUTABLE`); CI remains the authority.

---

## 4. Not doing — settled, don't revive

Audio (parked until a licence/recording decision) · backend, accounts, cloud sync · 700 per-verse share pages or painted cards · single-file `file://` edition · gamification (points, leaderboards, streak flames). The tone is *abhyāsa* — practice, not a game.
