# HANDOFF.md — current status and roadmap (lean)

**New AI session: read [`AGENTS.md`](AGENTS.md) first.** This file is the *current* handover — last 3 months + roadmap. Older detailed evidence is archived in `docs/archive/`. Search this file for the feature or verse, not front-to-back. `PROJECT.md` holds rationale.

| | |
|---|---|
| Last updated | 2026-11-04 |
| Updated by | Arena session `arena/77480584-bhagavad-gita` |
| Base commit | `24111f9` on `arena/77480584-bhagavad-gita` (review fixes 1, 2, 5, 8, 9) |
| Owner | Dhruba Chapain, Pokhara |
| Live site | https://chapain.github.io/Bhagavad-Gita/ |
| Archived | `docs/archive/HANDOFF-2026-09-10-19.md` (329KB, 2427 lines) |

> **Maintenance rule (2026-10-19):** Keep this file lean (<100KB). Update §1 and §6 only when status/roadmap actually changes. Detailed per-fix evidence goes to `docs/archive/` yearly slices, not here. Durable rules → `AGENTS.md`, rationale → `PROJECT.md`. If work is done, don't append — archive.

---

## 1. Where we are (concise)

- **Search reaches ideas; notes belong to the verse (2026-11-04, branch `arena/77480584-bhagavad-gita`).** Search indexed the verse line, IAST and paraphrase only — a chapter name (“Sankhya”), a theme title or one glossed word (“not hating”) returned nothing. `verseSearchText()` now also carries the verse title (×3 languages) and every word gloss; a `SEARCH_PASSAGES` index holds the 18 chapters and 169 themes; results group as Verses/Themes/Chapters under one total that adds both (`hits.length + passages.length`); a gloss-only hit says which word matched. Notes used to be written only on saved cards and were deleted by `removeFav()` — now every verse has a note field in the sheet, saved as you type, listed in Saved whether the verse is a favourite or not, and the `gitaFavNotes` storage key/backup schema is unchanged. i18n +7 → 224 strings ×3. **CI was false-green:** it called `source/browser_checks.py` (root file) and ended with `|| echo`, and installed Playwright after `build.py` (which detects the suite with `import playwright`); now Playwright installs first, `build.py` gates on the real suite, nothing swallows the exit code, and `source/prove_data_only.py` runs.

- **Phase 5.4 data export/import done (2026-10-19).** Favourites, notes, Learn progress were localStorage-only — cleared browser lost months. New `source/js/45-data.js` (9794 bytes trimmed) + `32-data.css`, view `#data`, footer + welcome link, versioned schema v1 `{version, app, exportedAt, data:{favs[], favNotes{}, learn{}}}`, validation + merge (favs union, notes overwrite, learn themes+held union, story max). i18n +19 keys (183→202 en/ne/hi), no Latin residue. Tests: `test_source_modules` allows `45-data.js`, `run_gita_app.js` 832 assertions, `tests/test_data_backup.js`.

- **Minor build nits (2026-10-19) — fixed.** ResourceWarnings closed with `with`, icons canonical in `icons/`, manifest/SW/chapter og:image → `icons/`, sitemap stable (last commit date). `og-card.png` 283KB→119KB (Pillow optimize, 57% saving). CI `.github/workflows/ci.yml` now runs full `build.py` + Playwright browser checks, Pillow for share-art.

- **Shell size:** 334,897 (Phase A–E) → 350,392 → **363,141 chars / 385,851 bytes / 105,035 gzip**. Cap moved twice on 2026-11-04, both times with the arithmetic at the check: 360,000 → 370,000 for A5 + C3 (+4,799) and → **375,000** for C2 (+7,086, after trimming 6,723 of its own code first). Measured, not assumed: `45-data.js` is only 13,228 chars, so lazy-loading it would win less than the bump while changing boot order, SW precache and the browser suite, which cannot run in this sandbox. Sitting at ~12.5KB headroom now; if it drops under 5KB again, split `20-learn.js` (34,114) or `10-library.js` (33,548), not the data module.

- **Current build:** `python3 build.py` ALL GREEN — 60 Python, **934 document assertions**, 506 site-health, 9,658 study, 17 migration, **13 search**, 700 theme-cards, backup; Playwright browser suite (**300 checks**) is run by `build.py` itself and fails the build.

## 2. Resume in five minutes

1. Read §1, §6, §7 here, then `PROJECT.md` §8.
2. Run `python3 build.py` — must pass, `git status` clean after (deterministic).
3. Agree next item with owner, work in small batches. Show evidence: verse + word list + 390px screenshot.
4. Before ending, update this file (§1, §6) only if status/roadmap changed. Archive old evidence to `docs/archive/`, don't append endlessly. Commit locally; push only with owner approval.

## 3. Map — what to edit

Everything browser loads is **generated** by `source/build_gita.py`. Never hand-edit `index.html`, `data/`, `chapter/`, `sw.js`, `404.html`.

| Content | File |
|---|---|
| Verse text (Deva+IAST) | `source/ch<N>.json` |
| Word split + glosses | `source/ch<N>.json` flow |
| UI strings (231 keys ×3) | `source/i18n_ui.py` |
| App HTML/CSS/JS | `source/app.html`, `source/css/*.css`, `source/js/*.js` (order in `build_gita.py`) |
| Data backup | `source/js/45-data.js`, `source/css/32-data.css` |
| Reviewed maps | `source/study_map_contract.json` |
| Checks | `source/check_*.py`, `tests/test_source_modules.py` |

## 4. Build and test

```bash
python3 build.py          # build + all checks (60 Python, 934 doc, 506 health, 9658 study, 17 migration, 13 search, 700 cards, backup, 300 browser)
python3 build.py --fast   # build only
node run_gita_app.js      # 934 assertions
node tests/test_data_backup.js
```

Browser checks need Playwright — skipped in sandbox, report when skipped.

## 6. Plan — status board (current roadmap)

- [x] **Phases 1–4:** source modularization, frozen interfaces, session gateway, architecture contracts
- [x] **Minor build nits (4):** ResourceWarnings, icons canonical, sitemap stable, CI full build
- [x] **Phase 5.4:** data export/import — favs, notes, Learn progress backup (versioned JSON, #data view, footer+welcome link)
- [x] **Shell lean:** cap 295k→320k for 5.4, trimmed 311,813→310,251 chars, og-card 283KB→119KB
- [x] **#1 Memory files:** archived HANDOFF 329KB→8KB lean (<100KB), yearly slices in `docs/archive/`
- [x] **#2 Shell creep:** trimmed data module (11366→9794 bytes), stable under 320k
- [x] **Public polish (2026-10-19):** CI full + Playwright, Pillow share-art, welcome backup discoverability
- [ ] **Phase 2.4 "Start here / Gītā in 18 verses":** declined by owner as childish — not planned
- [ ] **Phase 5.1 audio:** licence/recording decision, parked until 5.4 done (now done, still parked per owner)

Next suggested: keep HANDOFF lean (<100KB), watch shell if >350k lazy-load data module.

### Next session — fresh eyes (owner approved 2026-10-19)
After a break, look with fresh eyes at UX/content nuances invisible when deep in code:
- **Content:** verse titles (54-char limit), paraphrase clarity vs Śaṅkara, study maps contract
- **UX:** first-time flow (welcome → Three Ways → chapter → verse), Learn path stages, mobile 390px, bottom tab bar, search loupe
- **Perf:** chapter pages 1.4MB total, data/ 3.3MB lazy-loaded, og-card 119KB, shell 310k — trim if needed, no bundler

If work is done, don't append — archive. This file stays lean.

## 7. Decisions (active)

### 7.1 “तीन निष्ठा” → “तीन मार्ग” — DECIDED (owner, 2026-10-09) · IMPLEMENTED
UI keeps three six-chapter groups as मार्ग (karma/bhakti/jnana), not निष्ठा. निष्ठा belongs to verses (3.3 dvividhā).

### 7.2 Paraphrases 18.66 and 15.7 — DECIDED (owner, 2026-10-09) · IMPLEMENTED
Both revised to Śaṅkara reading.

### 7.3 Śaṅkara notes on ~25 pivot verses — DECIDED (owner, 2026-10-12): NOT ADOPTED
Public domain bhāṣya available, but not added as UI.

### 7.4 Data backup — DECIDED (owner, 2026-10-19) · IMPLEMENTED
Phase 5.4 before audio. Versioned JSON export/import with merge. Footer link + #data view. No commentary, no audio yet.

### 7.5 Icons canonical — DECIDED (2026-10-19) · IMPLEMENTED
`icons/` is single source of truth, root duplicates removed, only `favicon.ico` at root.

## 8. Session log (last 20, newest first)

- 2026-11-04 · `arena/187d5ce8-bhagavad-gita` · **C2 search suggestions.** Two characters open a real ARIA combobox (role=combobox + listbox + aria-activedescendant + aria-expanded), at most ten flat rows: 5 recent, 3 chapter titles matched by name, 2 verse numbers the digits could become (`2.4` → 2.4/2.40; Devanagari digits too). ↑/↓ move exactly one selection, Enter opens the highlighted row and cannot double as a submit, Escape closes the list only; a chapter row navigates instead of searching. One new string `search_suggest_hint` (231), row kinds reuse search_recent/chapters/verses. 13 search regressions (builders tested without a DOM) + 4 browser checks (**not run here** — Playwright cannot install; CI proves them). Shell 355,407 → 363,141, cap 370,000 → 375,000 after trimming the code first. Counts 934 assertions / 300 browser checks.
- 2026-11-04 · `arena/187d5ce8-bhagavad-gita` · **A5 backup discoverability + C3 folded second chance.** The Learn path says how long ago you last exported (today / yesterday / N days ago, calendar days so DST cannot produce "0 days ago"), reads the existing `gitaBackupAt` stamp and opens the data screen, and stays silent for a visitor with nothing saved (`backup_*`, 5 keys ×3 → 230 strings). A diacritic query that found nothing now gets one plain-reading retry and shows the real results under their real count — `sankhyā` 0→3, `arjunā` 0→36, `karmanyā` 0→7 — with `search_meant` saying why (`searchFoldAlternative()`, fires only on zero, never loops). C5 was verified as already shipped (hint + chips) and dropped. Cap 360,000 → 370,000 on the measured arithmetic (+4,799 chars; lazy-loading `45-data.js` would win only 13,228). Counts 925 assertions / 296 browser checks, 12 search regressions, shell 355,407 chars.
- 2026-11-04 · `arena/77480584-bhagavad-gita` · **Review fixes 3, 4, 6, 7.** The bottom bar is a nav with `aria-current` instead of a tab list, and — with the skip link — it is now inert while the sheet is open; read/learn is a group of pressed buttons; `img/share-art.jpg` is finally referenced, as the share-panel preview (browser check reads `naturalWidth ≥ 900`); the SRS finish screen stops claiming “complete for today” while chapters still have dues and starts with the most overdue chapter (`srs_review_more`, 225 strings); `build.py --prove` runs `prove_data_only.py`. Counts 908 assertions / 296 browser checks, shell 350,392 chars.
- 2026-11-04 · `arena/77480584-bhagavad-gita` · **Review fixes 1, 2, 5, 8, 9.** CI made honest (Playwright before build, `--serve` at the root path, no `|| echo`, `prove_data_only.py` step); search now indexes chapter names, theme titles, verse titles and word glosses with grouped results (`Sankhya` → Sāṅkhya Yoga, `not hating` → 12.13 with the word named); notes are per-verse, saved as typed, listed in Saved and survive un-favouriting (`gitaFavNotes` unchanged); ne/hi copy pass within the granted scope; docs/counts reconciled (832→892 assertions, 270→286 browser checks, 217→224 strings, 83→97 KB gzip) and `TOTAL_ASSERTIONS` now fails the suite when it drifts from what actually ran. Shell 347,934 chars, cap 350k→360k.
- 2026-10-19 · `arena/7aa49440-bhagavad-gita` · **Public polish — make app better.** CI full build + Playwright, Pillow share-art, og-card.png 283KB→119KB (57% saving), welcome data link for backup discoverability, trim data module 11366→9794 bytes. Shell 310,251 chars / 330,279 bytes. Full build ALL GREEN.
- 2026-10-19 · `arena/7aa49440-bhagavad-gita` · **Memory monolith killed (#1).** HANDOFF 329KB/2427 lines → archived to docs/archive/HANDOFF-2026-09-10-19.md, new lean 8.1KB/108 lines (<100KB), AGENTS.md updated, docs/archive/README.md policy.
- 2026-10-19 · `arena/7aa49440-bhagavad-gita` · **Phase 5.4 data export/import — close data-loss risk.** 45-data.js + 32-data.css, #data view, footer link, schema v1, merge logic, i18n 183→202, tests, CI. Shell 311,813 chars, cap 295k→320k. Full build ALL GREEN (60 Python, 827 doc, 503 health, 9658 study). Pushed.
- 2026-10-19 · `arena/7aa49440-bhagavad-gita` · **Minor build nits fixed.** ResourceWarnings with `with`, icons canonical in `icons/`, sitemap stable (last commit date), CI added. Assertions 776→783 then 827 after 5.4. Full build ALL GREEN. Pushed.
- 2026-10-19 · `arena/6417e38d-bhagavad-gita` · Source modularization Phases 1–4 complete, search field loupe fix, verse number gap fix, verse-fit measurement fix. Shell 294,676 chars. Browser 276 checks. Base `8417f03` merge of PR #56.
- 2026-10-18 · `arena/defbe426-bhagavad-gita` · All 700 verse titles re-audited, welcome hero refresh, 39 verse records changed, 54-char limit. PR #53 open.
- 2026-10-18 · `arena/4c434d4a-bhagavad-gita` · Theme-title audit 169/169 read, 6 fixed, 2 title advisories added. Python 49→53. PR #48 open.
- 2026-10-17 · `arena/404f7e7e-bhagavad-gita` · Retired per-theme and continuous-reading views, re-pointed links. Assertions 786→776, browser 233→241. PR #48.
- 2026-10-16 · `arena/2468aa99-bhagavad-gita` · Translation-audit follow-ups 6 cases researched against Śaṅkara bhāṣya.
- 2026-10-15 · `arena/7aa49440-bhagavad-gita` · Translation audit batch 3 (ch13-18), 211 verses, 188 renderings. PR #42.
- 2026-10-14 · `arena/812cd592-bhagavad-gita` · Whole-book summaries recovered and landed.
- 2026-10-12 · `arena/b6677bff-bhagavad-gita` · Phase 2.2 duplicate descriptions dropped, render-time suppression.
- 2026-10-11 · batch 19 · Final source review ch13 and 17, 62 verses, 42 overrides.
- 2026-10-09 · Decided तीन मार्ग, paraphrases 18.66/15.7.
- 2026-09-01 · v/ share pages retired (700 pages), redirect to /chapter/N/#vN.NN, 404.html recovers.

Older entries archived in `docs/archive/HANDOFF-2026-09-10-19.md`.
