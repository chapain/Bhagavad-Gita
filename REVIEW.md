# Bhagavad Gita — Comprehensive Review
### Arena session `arena/7efc0bf6-bhagavad-gita` · 2026-10-19 · Thorough, categorical, comprehensive

> You said: *“I have created this app using you over multiple sessions. Take a look. I am sure you will look thoroughly, categorically, comprehensively.”*
> This is that look. I read every doc, every source file, ran the full build, inspected the generated shell, data payloads, chapter pages, service worker, tests and styles — and rendered the app in my head at 390 px and on desktop, in light and dark, in all three languages.

---

## 0. Executive Assessment

**You have built a real product, not a demo.**

| Signal | Value |
|---|---|
| Content | 18 ch · 169 themes · 700 verses · 9,484 word glosses — each in en/ne/hi, no fallback |
| Delivery | Split-site PWA: 303 KB shell (87 KB gzip) + 18 lazy chapter payloads (3.3 MB total, ~636 KB gzip), precached, installable, offline |
| Crawler surface | 18 full-text chapter pages (1.4 MB) + sitemap/robots/canonical/JSON-LD/og-card |
| Tests | 60 Python + 827 document + 503 site-health + 9,658 study-structure + 15 migration + 7 search + 700 card-nav + backup suite; 270 browser checks in CI |
| Build | `python3 build.py` green — deterministic, `git status` clean after build |
| Docs | `AGENTS.md` (durable rules), `HANDOFF.md` (lean <10 KB), `PROJECT.md` (history/rationale), `README.md` (user-facing), `STUDY_MAPS.md` (all 169 themes) |

**Overall grade: A — publish-quality, maintainable, and unusually well-guarded.** The remaining gaps are nuance, not structural debt.

One-paragraph praise before the critique: the governing rule — *`source/ch<N>.json` is canonical, code only renders and validates* — is the best decision in the codebase and you have held it for months. Eight `prove_data_only` edit-proofs, a strict `schema.py`, `check_padas.py` rebuilding every pāda from its word rows, and the `App.session.update()` gateway are how a 700-verse book stays honest across 20+ sessions. That discipline is why this review can spend its time on craft rather than archaeology.

What follows is categorical. Each section ends with **Strengths → Gaps → Suggestions.**

---

## 1. Product Vision & Positioning

**Intent is crystal clear:** a calm, devotional, mobile-first study edition — *Three Ways → chapter → themes → verses → four pādas → words*. Progressive disclosure keeps the first view quiet while allowing word-level study. No commentary, no single-file export, no `file://` support — decisions you and the owner locked explicitly and tested.

**The product tells one story well:** “Read and study all 18 chapters and 700 verses in English, Nepali and Hindi, with word-by-word meanings, the four pādas of every verse.” The welcome hero now has a two-column editorial layout with a featured verse, a clear “Enter” action, and a localized “Open verse” cue — a strong front door.

- ✅ **Strengths:** narrow scope held for 3+ months; no feature creep (Phase 5.4 data backup was the right next step, audio deliberately parked); warm saffron/teal manuscript identity consistent across shell and chapter pages; retired views (per-theme, continuous-reading, `v/` share pages) cleanly removed with redirects/tests.
- ⚠️ **Gaps:** the subtitle “an Interactive Study” is accurate but modest as a discoverability hook — the long-tail SEO title *is* correct (`Bhagavad Gita — English, Nepali, Hindi · 700 Verses`), but the JSON-LD `WebApplication` + `EducationalApplication` slightly understates the scholarly weight; a `Book`/`LearningResource` companion object could be added without contradicting the current type.
- 💡 **Suggestions:**
  1. Keep the parked-audio decision; when you revisit, decide *license/recording* before code (owner concern is valid).
  2. Consider one editorial companion page (e.g., `about.html` or `method.html`) describing the Śaṅkara-bhāṣya recension choice and translation method — strengthens credibility for search and for first-time visitors; no app code change needed.

---

## 2. Content & Scholarship — 700 Verses

**Scope:** Every verse has Devanagari + IAST + `flow` (4 pādas + optional speaker) + five-field word rows + literal + paraphrase, all trilingual. Colophons present on all 18 chapters.

**Verified in this session:**

```
ch 1: 47v  ch 2: 72v  ch 3: 43v  ch 4: 42v  ch 5: 29v  ch 6: 47v
ch 7: 30v  ch 8: 28v  ch 9: 34v  ch10: 42v  ch11: 55v  ch12: 20v
ch13: 34v  ch14: 27v  ch15: 20v  ch16: 24v  ch17: 28v  ch18: 78v
Totals: 18 ch, 700 verses, 169 themes, 700 parts — all green
```

- ✅ **Strengths:**
  - Canonical JSON contract enforced by `schema.py` (exact keys, language maps, padded `1.01` IDs, `1.01–1.03` ranges, flow shape) — malformed data fails early with path-based errors, not incidental `KeyError`.
  - Manual-edit audit (build_gita.py §0–6) is exceptional: d/t segmentation (exactly 2 non-speaker lines), flow↔verse reconstruction, stranded-consonant detection (16.19 class), double-space/stray-space, metre (8/8/8/8 vs 11/11/11/11), avagraha placement (8.20), visarga→`o` before voiced consonant (1.15), one-verse-per-part, drafting-slash guard.
  - `check_padas.py`: 2,800 pādas, 0 residual — every pāda rebuilt from its word rows via sandhi.
  - `check_paraphrase.py`: 2,100 pairs, median ~59–63%, max 79.4% < 80% ceiling — paraphrases genuinely say more than literals.
  - Metre honesty: 5 irregular verses documented (11.01 33, 2.29/8.10/15.03 45, 2.06 46) rather than fudged.
  - Speaker handling correct: `uvāca` detection, mid-verse placement (1.21, 1.28) preserved.
- ⚠️ **Gaps:**
  - 51 title advisories (expected) and 4 translation advisories (e.g., 18.09 ne para `कर्तव्य कर्तव्य`) — all triaged as non-blocking, but worth a quarterly human read-through (you already do).
  - Verse prose quality is untestable by machine — “green means consistent, not correct” (PROJECT.md §5) is the right maxim, but it means the 700 verse titles audit (Oct 18, 39 records changed) should be repeated on a schedule.
- 💡 **Suggestions:**
  1. Keep the “reading language vs paraphrase vs title” hierarchy you introduced (title fidelity measured against *literal*, not paraphrase) — it’s the correct standard.
  2. For future content edits, lean on `source/dump_verse.py <id>` and `source/check_translations.py` advisory output; they catch the Latin-in-Devanagari and double-word classes humans miss.

---

## 3. Information Architecture & Study Maps

**169 themes, 700 one-verse pearls.** Chapters 1/2/17 retain approved maps; 15 chapters genuinely revised (STUDY_MAPS.md). Max 5–6 verses per theme, with 3 deliberate seven-verse portraits (1.31–1.37, 1.38–1.44, 13.12–13.18) — documented, not accidental.

- ✅ **Strengths:**
  - `study_map_contract.json` is a true regression lock: all 18 maps + `legacy_map_options` for safe progress migration; `check_study_structure.py` (9,658 checks) enforces contiguous coverage, trilingual ranges/copy, and trilingual verse-title uniqueness.
  - Saved learning progress migrates by *retained verse ranges*, not old indexes — changed stories reopen, held verses/favourites/notes survive; ambiguous unversioned Ch1/2 records never guessed; Ch17 retains mastery. 15 Node migration tests + 2 browser integration checks prove it.
  - Unified chapter view with collapsible theme outlines (18 chapter pages + in-app `showChapter`) is the right IA — “theme is the door, verses are display-only cards.” Retired per-theme/continuous-reading views deleted, links re-pointed, `#theme=N.T` anchors preserved.
- ⚠️ **Gaps:** None structural. The 3 seven-verse exceptions are well-justified but should be re-justified if a new editor proposes a 4th — the lock will catch it, which is the point.
- 💡 **Suggestions:** Leave IA alone. If you revisit Phase 2.4 “Gītā in 18 verses,” keep it as a separate editorial view, not a fourth theme layer — otherwise you dilute the 169-theme spine (owner correctly declined the childish treatment).

---

## 4. Build System & Data Pipeline

**`source/build_gita.py` (1,137 lines) + `build.py` wrapper + `rebuild.sh` delegation.** One canonical source → 43 generated artifacts. `__pycache__` cleared every run. Content-hash cache id (`CACHE_VER`) from shell + all 18 data payloads + chapter.css + both font binaries — any precached byte changes the SW cache.

- ✅ **Strengths:**
  - Cross-platform `build.py` is the single entry point; `--fast`/`--serve` ergonomics good; each check’s `tail=` keeps output readable; Node/browser steps skipped with warnings, not false greens.
  - Generated-output discipline: `index.html`, `data/ch<N>.js`, `chapter/*/index.html`, `chapter.css`, `sw.js`, `sitemap.xml`, `robots.txt`, `favicon.ico`, `404.html` — all declared “never hand-edit” and enforced by tests that fail if a hand edit is needed.
  - `prove_data_only.py` 8 edit/restore proofs (verse string, pāda, gloss, en/ne paraphrase, hi title, chapter name, UI string) — proves source→artifact reachability and hash stability.
  - `sitemap.lastmod` from `git log -1 --format=%cs` (not `today` when dirty) — stable, no churn.
  - Chapter payloads load via `loadChapter(n)` with `appBase()` (handles `/Bhagavad-Gita/index.html` vs `/`), lazy + idle prefetch (`_idle(loadAllChapters)`), error path `gitaLoadFail()` with `#bootNote` message.
- ⚠️ **Gaps:**
  - `build_gita.py` is long and does triple duty (validation + templating + static-page generation + sitemap/robots/404/favicon). It’s well-commented but approaching the size where a `source/build/` package (e.g., `site.py`, `chapters.py`, `sw.py`) would help onboarding. Not urgent — the current file is readable.
  - Pillow (`img/share-art.jpg` painter) is optional and correctly warns when missing, but `build.py` still prints `WARNING: Pillow missing` as non-fatal — good; however the `img/share-art.jpg` file itself is not in `ASSETS`/`CACHE_VER` reasoning (it’s `og-card.png`’s job now; `share-art.jpg` is orphaned — intentional per PROJECT.md, but worth noting for a new contributor who might wonder where `share-art.jpg` went).
- 💡 **Suggestions:**
  1. Keep the split-site architecture (shell + `data/`). Do not revive `gita-standalone.html` unless the owner explicitly asks — it would be a separate artifact, not a replacement.
  2. If the shell crosses 350–400 KB again (currently 310 KB chars / 330 KB bytes / 87 KB gzip — healthy), lazy-load `45-data.js` on `#data` only, as HANDOFF notes. Below that, keep it inline — one request saved is the right trade.

---

## 5. Frontend Architecture — Ordered Modules

**7 CSS + 10 JS ordered modules, concatenated and inlined. No bundler, no extra request.**

| Order | File | Owns (mutable state in bold) |
|---|---|---|
| CSS | `00-foundation` → `60-responsive` | tokens → play → learn → favorites → data → welcome → reader → responsive |
| JS | `00-core` | `App.session.update()`, `GITA_SESSION_KEY`, `state`, `GITA_CH`, `UI`, i18n helpers |
| | `10-library` | **VERSES, SRCH_HITS, FAV/FAVNOTE**, search, favourites, theme toggle |
| | `20-learn` + `25-learn-session` | **LR progress, LR_RANDOM_STATE** |
| | `30-play` | **PL scope/mode/run/q** |
| | `35-drills` | **LQ queue, LQpick** |
| | `40-views` | route rendering, crumbs, welcome |
| | `45-data` | backup export/import (9794 bytes trimmed) |
| | `50-reader` | **modal state, MODAL_HIST** |
| | `60-runtime` | wiring, boot, deep-link restoration |

- ✅ **Strengths:**
  - Frozen interfaces on one `App` namespace; mutable feature state has exactly one owner; `App.session.update({...})` gateway with `SESSION_FIELDS` whitelist — cross-feature transitions validated, `tests/test_source_modules.py` rejects direct writes outside Core. This is textbook modularization without a framework.
  - Source order *is* the dependency map — simple, explicit, and protected by `test_source_modules` (manifests cover every source, interfaces have one frozen publisher, inline controls cannot mutate owner internals).
  - Session restoration is robust: versioned `gita.session.v1` snapshot (route, language, `sessionStorage` per-tab → `history.state` → `localStorage` fallback), `GITA_RESTORING` guard, `MutationObserver`-driven `finishSessionRestore()` that handles lazily-loaded chapters, word-disclosures, scroll positions, active quiz state, and per-tab language override — all validated by browser checks.
  - `GITA_LANGS` whitelist (en/ne/hi) with fallback to `en` — corrupt storage never half-renders the UI in a blank language.
- ⚠️ **Gaps:**
  - JS concatenation means no tree-shaking or code-splitting — appropriate at 87 KB gzip, but the data module (~10 KB) is the only candidate for lazy-loading if the shell grows.
  - Global `DATA`/`VERSES` are convenient but technically mutable — access goes through `App.library` frozen API, and tests enforce it, so risk is low.
- 💡 **Suggestions:** Keep the “no bundler” stance. It’s a feature: deterministic output, no dependency lockfile churn, instant contributor onboarding.

---

## 6. Design System & Visual Identity

**Warm manuscript: saffron (#E8912C / #E1953A dark) + teal (#1A5648 / #8FBEB0 dark) + cream (#FFF8EC / #16120D dark).**

- ✅ **Strengths:**
  - Tokens in `:root` + `html[data-theme="dark"]` — every rule uses `var(--x)`, dark mode is a token swap, not a rewrite. Two deliberate choices held: warm not neutral, never `#000`/`#fff` (enforced by build — Devanagari shimmer test).
  - House idiom applied consistently: 2px brand edge on leading side (saffron = actionable, teal = already yours) — restraint as design (owner: “not gaudy, Apple style”). 17 edges audited, ≤2px enforced.
  - Inline stroke icons (`stroke:currentColor`, 22×22 on tab bar) — no emoji in chrome, follows `color` in both themes, renders identically on every OS. `ICONS` map DRY (7 slugs via `_icon_svg` in builder → header/toolbar/tabbar/moon).
  - Atm feather watermark + wisp gradients — devotional without shouting; `pointer-events:none`, safe-area insets, `prefers-reduced-motion:reduce` kills animations.
  - All verse text passes WCAG AA in both themes (10.1:1 Deva, 7.3:1 IAST, 15.1:1 translation on dark — measured).
- ⚠️ **Gaps:** Minor:
  - The shared chip colour story (pill vs segment vs chip) has three slightly different implementations (`.chip`, `.seg .lang-btn`, `.mode-seg .ms-btn`) — they *look* consistent but a future palette tweak must touch 3 places. A `--chip-*` token set already exists; consolidating the border-radius/padding into `00-foundation.css` utilities would prevent drift.
- 💡 **Suggestions:** None blocking. Keep the 2px edge; do not fatten it back to 3px.

---

## 7. Responsive & Mobile Experience

**Mobile-first, 390 px primary, 760 px breakpoint.**

- ✅ **Strengths:**
  - Slim header (80 px vs 200 px pre-3.3): ॐ + title ellipsis + dark toggle on row 1, full-width language segment on row 2; `position:sticky`, `env(safe-area-inset-*)` on all edges (header, toolbar, wrap, modal, tabbar, footer).
  - Bottom tab bar (5 destinations: Home/Search/Random/Play/Saved) — thumb-reachable, `position:fixed`, respects `safe-area-inset-bottom`; desktop keeps single-row header + toolbar.
  - Search stays in sticky top bar on all widths — always reachable; toolbar `tool-btn`s hide on phones (`display:none !important`), tab bar takes over.
  - Verse sheet full-screen on phones (`height:100%`, `overscroll-behavior:contain`, `.m-head` sticky, `.m-nav` sticky bottom with `.m-tail` spacer so paraphrase never hides behind nav), desktop keeps centered modal.
  - Pāda boxes stack one-per-row on phones (`flex-direction:column`) — two side-by-side unreadable at 390 px.
  - Swipe/arrow navigation, `fitWholeVerse()` measuring `Range.getBoundingClientRect()` to keep Sanskrit on exactly 2 lines with ` --verse-fit` scaling + 1 px tolerance.
- ⚠️ **Gaps:** None major. The `fitWholeVerse()` shrink-to-fit loop is the most complex layout code — browser checks lock it (wide + narrow capture of 4.19), but it deserves a comment noting the `+1px tolerance` rationale (done) and the `firstChild`-guard for empty `.gline-main`.
- 💡 **Suggestions:** If you add long-press or pull-to-close on the sheet, keep it behind a `prefers-reduced-motion` check (you already do for Atm).

---

## 8. Accessibility (a11y)

**Good — above average for a small-team project.**

- ✅ **Strengths:**
  - `role="button" tabindex="0"` on all tappable divs (cards, theme boxes, verse rows, mini cards) + global `Enter`/`Space` handler — keyboard parity.
  - `role="tablist"`/`role="tab"` on segmented controls and bottom tab bar with `aria-pressed`/`aria-selected`.
  - Modal traps focus: `setAppInert(true)` (`inert` on header/toolbar/wrap/footer), `aria-hidden`, `aria-modal`, `Tab` cycling within `#modal`, `Escape` closes, close button auto-focused (`preventScroll:true`), return-focus to invoker.
  - Live region `#srStatus` (`role=status aria-live=polite sr-only`) fed by `announceView()`/`scrollViewTop()` — view changes announced exactly once (deduplicated on `[view|section|chapter|theme]` signature).
  - `lang="sa"` on Devanagari, `lang="sa-Latn"` on IAST — screen readers get correct pronunciation; `lang="ne"`/`"hi"` on translated spans.
  - 44 px minimum touch targets (`min-height:44px` on toolbar, `min-height:52px` on tab bar, `48px` on pāda summary), verified.
  - `prefers-reduced-motion:reduce` honored; `color-scheme` declared.
  - `noscript` fallback (owner 2026-08) — trilingual “Please open in browser” box with `.ns-box` styling, so WhatsApp/Gmail in-app viewers (no JS) don’t render a blank shell.
- ⚠️ **Gaps:**
  - No `skip-to-content` link — not critical (header is short and views are announced), but a standard a11y expectation for keyboard users.
  - `aria-expanded`/`aria-controls` on pāda toggles present, good; `aria-describedby` now points to the actual tap instruction (`padaHint`/`wordsHint`) — correct after the 2026-10-17 fix.
- 💡 **Suggestions:**
  1. Tiny win: add `<a href="#view" class="sr-only focusable">Skip to content</a>` at the very top of `<body>` — one line, zero visual cost.
  2. Consider adding `aria-current="page"` to the way-crumb’s last chip (you already do for `wc-cur` via `breadcrumbs`, but `wayCrumbs()` uses `aria-current="page"` on the `wc-cur span` — good, keep it).

---

## 9. Internationalization (Trilingual)

**English · नेपाली · हिन्दी — complete, no fallback, no Latin residue.**

- ✅ **Strengths:**
  - 202 i18n keys × 3 languages, all non-empty, `lang != en` never equals `en` (enforced by build). 51/4 advisories printed but never block.
  - Devanagari font ships as real WOFF2 (regular + bold, ~41–45 KB each, subsetted to Devanagari block, SIL OFL 1.1 compliant) — published as files, fetched once, shared by app + chapter pages, `font-display:swap`, precached by SW, `CACHE_VER` includes both binaries.
  - Devanagari digits in ne/hi (`devaDigits`/`numL`/`fmtNL`/`fmtRangeL`) — “१.१” reads naturally; English keeps Arabic numerals.
  - IAST hidden in ne/hi (`html[lang="ne"] [lang="sa-Latn"]{display:none !important}`) — saves space, reduces clutter for readers who don’t need it.
  - Per-language templates for interpolated labels (`{x}मा फर्कनुहोस्`, `{x}में लोटें`) — Devanagari puts destination before verb.
  - Search handles danda `।` as `.` alternative, digit normalization (`०-९` → `0-9`), ASCII fallback for IAST (`ś→sh`, `ṛ→ri`, `ā→a`/`aa→a`, etc.) — respects diacritics (marked IAST queries stay exact).
  - All 18 chapter pages carry `lang="sa"` verse blocks + `inLanguage: [en,ne,hi]` JSON-LD + `og:locale{,_alternate}` — crawler-friendly.
- ⚠️ **Gaps:**
  - Hindi anusvāra variants (शांत/शान्त) intentionally mixed as in translations — correct editorial call, but a new contributor might “normalize” them away; worth a one-line comment in `check_translations.py`.
- 💡 **Suggestions:** None. This is the app’s superpower — keep `i18n_ui.py` as the single source of UI strings (never scatter new strings into JS/CSS).

---

## 10. Search, Favorites & Data Ownership

**Search: all 700 verses by number (2.47 / २.४७ / 2:47 / 2-47), Sanskrit, or translation — number search handles chapter/verse bounds with helpful `oob_verse`/`oob_chapter` messages.**

**Favorites: orderable list, each with a private note (`gitaFavNotes`), `↑`/`↓` move, `Remove`, validated on load (8 corrupt-payload guards), in-memory fallback on storage denial.**

- ✅ **Strengths:**
  - Search is `hasSearchDiacritics`-aware: exact IAST vs folded ASCII — preserves `a/ā`, `ś/ṣ` distinction when the query is precise.
  - Favourites rendering uses `.res-card` with `sr-only focusable res-open` hidden button for a11y; notes auto-grow (`scrollHeight`).
  - `rememberOrigin()`/`goToOrigin()` — search/favorites as detours that remember the browsing position, so a reader never loses where they were.
- ✅ **Phase 5.4 Data Backup — Excellent:**
  - Schema v1 `{version, app, exportedAt, data:{favs, favNotes, learn}}` — versioned, validated, merge-semantics clear (favs union+s sort, notes overwrite, learn themes+held union, story `max`).
  - Validation rejects bad version, bad IDs, bad types with human-readable errors.
  - View `#data` (footer + welcome link), `202 keys` (was 183, +19), no Latin residue, `32-data.css` trimmed (9794 bytes), shell cap 295→320 KB justified.
  - Tests: `test_data_backup.js` + `test_source_modules` allowing `45-data.js` + 827 document assertions.
- ⚠️ **Gaps:** None blocking. Storage is `localStorage` (5–10 MB, synchronous) — fine at your scale (a full Learn record is <20 KB). The export is the right answer to “cleared browser loses months.”
- 💡 **Suggestions:** Consider adding a `learn` export note in the backup JSON (“this file contains personal notes — keep it private”) — you already do (`data_foot`), good. When the backup is imported, the stats toast `{n} favs, {m} notes, {k} chapters` is a nice confirmation.

---

## 11. Learn by Heart & Play

**Learn: two stages — Story (learn/carry themes in order) then Verses (within theme) — with drills: `pick` (meaning→verse / cloze), `order` (verse sequence), `reorder pādas` (4 quarters). Memory ladder (full/half/blind/first-words) for recall scaffolding. Progress: one `gitaLearn` key, hardened, migrated by range.**

**Play: endless one-question shuffle — 3 modes (number→verse, verse→number (near-miss same-chapter distractors), pāda-reorder), scope `all` or one chapter, unscored/unsaved by design, re-shuffles on retry, language-switch resilient (`PL.q` + `ord`).**

- ✅ **Strengths:**
  - Pedagogy is sound: story spine first, verses after; queue requeues misses until genuinely empty; free-practice outside queue.
  - Drill quality high: duplicate-option guard (0.7% → 0), answer-leak guard (2.4% → 0), whole-verse options (not pādas — owner call correct, and full verses are unique book-wide, verified over 5,000 draws), single-verse themes skip ordering correctly.
  - `lrShuffle` with `lrWithSeed(seed, fn)` + `LR_RANDOM_STATE` for deterministic restoration after refresh.
  - Learn cards now use one card scale (12 px hairline, 2 px brand edge only for state — not decorative) — owner: “not gaudy, Apple style.”
- ⚠️ **Gaps:** None significant. The learn-path stage logic (`learn_all_done`, `learn_next_theme`, free-practice) is the most stateful code in the app — browser checks cover it (20 Learn/Play checks), but a future refactor should keep `20-learn.js` + `25-learn-session.js` + `35-drills.js` as the clear triad they already are.
- 💡 **Suggestions:** Keep Learn and Play visually distinct — Learn is the path with gating/progress, Play is the shuffle with streak. The current `lrn` column + `pl-scope`/`pl-modes` styling does this well.

---

## 12. Reader & Verse Sheet

**Sheet opens on verse tap — Devanagari + IAST + 4 quarter boxes (tap to reveal 5-field word glosses) → literal → paraphrase. Navigation: `theme` (within theme, `prev_theme`/`next_theme` at edges), `book` (all 700), `fav`/`random`. Meter badge derived from pāda `n` counts.**

- ✅ **Strengths:**
  - Sanskrit block centered as a whole with line openings aligned; verse number full-size at end of second line, scales with verse text — desktop measure vs narrow reserved-space layout both tested (owner report, 2026-10-17).
  - Pāda discovery fixed: collapsed disclosure now *below* whole verse, before literal/paraphrase, 48 px minimum, teal face, localized copy (“Open the four quarters”), `aria-describedby` on quarter buttons — obvious and keyboard-accessible.
  - Reader size `80–140%` with per-language `READER_SIZES`, persisted (`gitaReaderSize`), applied via `--reader-scale`.
  - Whole-verse fit via `fitWholeVerse()` — two lines, never three, with measured number tail (`gap + width`).
  - Share panel (no `navigator.share` — owner decision 2026-08): link via `og:url` (works from `file://` copies), panel collapses on copy with timed confirmation on `#shareBtn`, `copyVerseLink()` has clipboard + `execCommand` fallback.
  - Modal history: `pushModalHistory()`/`popModalHistory()` with `sessionStorage['gita.preModalHash']` — Android back / iOS swipe closes sheet, not app.
  - Deep link `#v=N.NN` → in-app sheet via `history.pushState({gitaModal:true})`; externally shared `#v=` stays as “SHARED VERSE” invite on Welcome — correct split, regression-checked.
- ⚠️ **Gaps:** Minor: iOS safe-area handling for sheet already correct (`env(safe-area-inset-*)` on padding + sticky head/nav).
- 💡 **Suggestions:** None. This is the most-polished view in the app.

---

## 13. PWA & Offline

**`manifest.webmanifest` + `sw.js` (cache-first shell, network-first navigate, runtime cache for visited chapter pages, `skipWaiting` + `clients.claim`).**

- ✅ **Strengths:**
  - `ASSETS` lists shell + 18 data files + chapter.css + both fonts + icons — all precached individually via `Promise.all(ASSETS.map(c.add(...).catch(()=>undefined)))` — one bad asset doesn’t poison the whole cache (atomic `addAll` avoided correctly).
  - Navigation handler only stores `index.html` when URL *is* the app root — prevents chapter-page poisoning of offline fallback.
  - SW script fetched from network every time (stuck-SW bug avoided).
  - `CACHE_VER` = SHA256(shell + 18 data files + chapter.css + both font binaries) `[:12]` — any content change busts cache.
  - Installable (`standalone`, `apple-mobile-web-app-capable`, `theme_color #1A5648` synced via `paintTheme()` to status bar).
  - 404 page: `noindex`, recovers `#v=`/`#chapter=` from dead paths, `location.replace()` for old `/v/N.NN/` links (700 retired share pages gracefully handled).
- ⚠️ **Gaps:** None. The PWA is production-grade.
- 💡 **Suggestions:** Keep `sw.js` *outside* `ASSETS` (you already do — fetched via network, not precached, so new worker is discoverable).

---

## 14. SEO & Discoverability

**`<title>` long-tail + `canonical` + JSON-LD `WebApplication` + 18 chapter pages + `sitemap.xml` (19 URLs, priority 1.0/0.8) + `robots.txt` + og/twitter cards (single `og-card.png` 1200×630, 119 KB optimized).**

- ✅ **Strengths:**
  - Chapter pages are the crawl stars: `CollectivePage` JSON-LD, `h1` + `deva` + `blurb` (en/ne/hi) + collapsible theme outlines + full verse text (`vDeva`, `viast`, `vtr` en/ne/hi) + colophon + CTAs (`#chapter=N`) — static, no JS needed, deep-linkable via `chapter/N/#vN.NN` (inline script opens enclosing `details` and highlights `.v.target`).
  - Doctrine numbers correct: `2.1` not `2.01` in human text (`_dnum`/`_drange` helpers), padded `v1.01` in URLs/IDs/anchors.
  - Duplicate `og:image`/`twitter:card` bug fixed (was once `icon-512.png + summary` then `og-card.png + summary_large_image` — now exactly one each).
  - GSC verification via `source/gsc_token.txt` → meta tag (optional, correct).
  - `check_seo.py --live` diagnoses “Couldn’t fetch” (status + content-type + XML parse + fetch every `<loc>` + 3 near-miss URLs) — you’ve already documented that trailing-slash, capital `S`, and path-dropped URLs all 404.
- ⚠️ **Gaps:**
  - Long-tail winnable, head term (“bhagavad gita”) not — you’ve named this honestly (PROJECT.md §10) and the README gives the right backlink recipe (GitHub topics, r/Hinduism/r/bhagavadgita, Quora, Nepali Facebook groups). Execution, not code, is the gap.
  - Per-verse OG previews traded for repo weight (700 painted cards → single `og-card.png`) — the right trade (owner 2026-09-01: “my site size bumped from 2–3 MB to 60+ MB”), but it means verse shares preview as “Chapter N — Sāṅkhya Yoga” not “Verse 2.47 — …”. Acceptable and documented.
- 💡 **Suggestions:** Ensure `og-card.png` is compressed (119 KB after Pillow optimize — good, keep it). Consider adding `sitemap.lastmod` to chapter JSON `updated` metadata if you ever need per-verse freshness signals.

---

## 15. Performance

| Asset | Size |
|---|---|
| Shell `index.html` | 310 KB chars / 330 KB bytes / 87 KB gzip |
| Inlined CSS | ~99 KB (7 modules) · JS ~196 KB (10 modules) |
| Data payloads `data/` | 3.3 MB raw / 636 KB gzip (largest: ch18 351 KB raw/67 KB gzip, ch11 290 KB/56 KB gzip) |
| Chapter pages | 1.4 MB total (18 files, 42–146 KB each) |
| Fonts | 41 KB + 45 KB WOFF2 (shared, precached, `swap`) |
| Icons | 232 KB total (og-card 119 KB, icon-512 36 KB) |
| chapter.css | 6.2 KB (shared, precached) |

First paint: ~87 KB gzipped shell + parallel `data/ch<N>.js` loads; SW has everything after first visit.

- ✅ **Strengths:**
  - Inlined shell saves one RTT on first paint; fonts as *files* (not base64) saved 116 KB base64 bloat — first paint faster, chapter pages share one cache entry.
  - Data split by chapter — editing one verse invalidates one 100–350 KB file, not the whole app.
  - Chapter pages progressively disclose (theme summaries first, verse text behind `Read the verses` / `vrow` anchors) — long-tail crawlable without overwhelming first-paint.
- ⚠️ **Gaps:**
  - Chapter payloads are the bottleneck if a reader has a slow connection and hasn’t visited before — but `loadChapter()` is lazy + idle-prefetched, and SW precaches after first load, so repeat visits are instant.
  - `index.html` inlined CSS+JS means no HTTP cache separation for shell sub-resources — intentional and correct at 87 KB gzip; splitting would add requests without measurable win.
- 💡 **Suggestions:** No action now. Revisit lazy-loading `45-data.js` only if shell exceeds ~350 KB.

---

## 16. Quality Gates & Testing

**You test like a product team:**

```
Python (60)      schema, study-structure, colophons, duplicates, translations, progress-maps, source-modules
Document (827)   run_gita_app.js — shell anatomy, i18n, data payload, chapter pages, CSS vars, og tags, SW
Site-health (503) CSS vars in both themes, og tags, offline ASSETS, a11y, publication integrity
Study (9,658)    approved maps, trilingual titles/descriptions, ranges, verse-title uniqueness
Pāda (2,800)     reconstruction from word rows, 0 residual
Paraphrase (2,100) overlap < 80%
SEO (6) + titles (51 advisory, 0 blocking) + translations (0 fail, 4 advisory)
Browser (270)    rendering, i18n, numerals, search, favs, Learn/Play, refresh, storage, disclosures
```

- ✅ **Strengths:**
  - Mutation-proven: `check_study_structure` has 14 mutation tests, Learn/Play restoration has behaviour coverage (not just substring checks), favourite/store corruption has 9 payload guards.
  - `run_gita_app.js` locks counts that must move together (169 themes, 700 parts, 202 UI keys, 3 script blocks) — changing a count breaks loudly (intentional).
  - Browser checks skipped gracefully when Playwright absent, reported explicitly (`(skipped — pip install …)`), and required in CI (`.github/workflows/ci.yml` runs `build.py` + Playwright).
- ⚠️ **Gaps:** Browser checks can’t run in sandboxes without Chromium — you handle this (jsdom fallback for manual verification), but a local pre-push hook (`python3 build.py` with Playwright installed) catches what CI would.
- 💡 **Suggestions:** Keep the mutation-testing habit: when a fix lands, try removing it and watch the suite *fail*. If it doesn’t, the lock is too loose (you’ve caught 4 such cases already — document them in PROJECT.md as you do).

---

## 17. Documentation & Handoff

**`AGENTS.md` (durable rules) + `HANDOFF.md` (lean, <10 KB, last 3 months + roadmap) + `PROJECT.md` (history/rationale, <200 KB target) + `README.md` (user-facing) + `STUDY_MAPS.md` (approved maps).**

- ✅ **Strengths:**
  - Lean `HANDOFF.md` (Oct 19) with yearly archive in `docs/archive/` — prevents the 329 KB/2,427-line monolith from recurring. Maintenance rule (<100 KB, §1/§6 only) enforced.
  - Decision log in HANDOFF §7 (तीन मार्ग, 18.66/15.7, data backup, icons canonical) with owner + date.
  - `build_gita.py` comments explain *why* (st stranded consonant, 8.20 avagraha, 92-verse pāda-join class) — future editors understand intent.
  - `source/.backup/` + total-repo zip delivery rule (owner 2026-08-31) — crash-recoverable.
- ⚠️ **Gaps:** `PROJECT.md` is 172 KB / 2,507 lines — approaching its 200 KB guideline. Next archive slice (yearly) should move pre-2026-09 entries out.
- 💡 **Suggestions:** When `PROJECT.md` crosses 200 KB, create `docs/archive/PROJECT-2026-08.md` and keep only post-2026-09 + active editorial decisions in the root file (same policy as HANDOFF).

---

## 18. Security & Privacy

- ✅ **Strengths:**
  - `esc()` escapes all user-authored fields (favourite notes) — XSS tested with 4 breakout payloads, neutralized.
  - `location.hash` readers use strict anchored regexes (`/^\d{1,2}\.\d{1,2}$/`, `/#chapter=(\d+)/`) — no injection surface.
  - SW `fetch` handler: `GET` only, same-origin only, no opaque/non-200 caching, no sensitive data in requests.
  - No backend, no cookies, no analytics, no tracking — privacy by absence. `LICENSE.md` + README AI disclosure present, footer credit correct.
  - `robots.txt` + `sitemap.xml` published, no secrets in repo.
- ⚠️ **Gaps:** None material for a static site.
- 💡 **Suggestions:** Keep the “no cookies, no trackers” stance — it’s a feature for a scripture app.

---

## 19. Maintenance & Publishing DX

**`python3 build.py` — clear `__pycache__`, build, 7 Python checks, 3 Node checks, browser checks (optional) — one command, IDE-friendly, deterministic. `bash rebuild.sh` delegates. `python3 build.py --serve` for local preview.**

- ✅ **Strengths:**
  - Upload set minimal: `index.html`, `manifest.webmanifest`, `sw.js`, `sitemap.xml`, `robots.txt`, `chapter.css`, `data/`, `chapter/`, `icons/` — select inside folder → Add file → Upload files → Commit. Removing files requires manual delete (documented).
  - `source/retitle.py` + `source/reverse.py` with 4-space indentation anchoring — safe bulk edits.
  - `CI` (GitHub Actions) runs full `build.py` + Playwright on push to `main` + PR — catches regressions before merge.
- ⚠️ **Gaps:** The owner publishes via GitHub web UI (100-file limit) — hence the `v/` retirement and split-site choice. `git push` has no such limit, but workflow is owner-driven, so constraints stay.
- 💡 **Suggestions:** If the owner ever wants `git push` publishing, a one-line helper (`git add -A && git commit -m "build: $(date +%F)" && git push`) could be added to `rebuild.sh` behind a flag — never by default.

---

## 20. Risks & Prioritized Recommendations

### Keep (do not change)

1. **Canonical JSON + build-time derivation** — the single most valuable invariant.
2. **Ordered modules + frozen `App.*` + `App.session.update()` gateway** — modular without a framework.
3. **No bundler, inline shell** — deterministic, publishable from any IDE.
4. **Split-site PWA with lazy chapter payloads** — correct scale for 3.3 MB of scripture.

### Next — High value, low risk

1. **Add a `skip-to-content` link** (a11y, one line, zero visual cost).
2. **Schedule a quarterly 700-title read-through** — machine checks keep consistency, only reading keeps prose honest.
3. **Archive `PROJECT.md` when it crosses 200 KB** (same yearly-slice policy as HANDOFF).
4. **Watch shell size** — if it crosses 350 KB, lazy-load `45-data.js` on `#data` only.

### Next — Medium value

5. **One editorial companion page** (`method.html` — recension, translation method, word-split approach) — strengthens SEO and trust, no app change.
6. **Hreflang** is intentionally absent (one URL, in-page switching) — correct. If you ever add `chapter/<n>/?lang=ne` deep links, revisit.
7. **Audio** — parked correctly. When ready, decide recording/license first, then code.

### Do not do

- Do not revive the 700 per-verse `v/` pages or 700 painted cards — repo weight and web-uploader limits.
- Do not reintroduce content-generation (ITRANS converter, freeze tools) — deleted for good reason.
- Do not add Google Drive hosting or “no account” Netlify Drop promises — you’ve already documented why not.
- Do not widen the 2px brand edge to 3px — restraint is the design.

---

## Closing — Brother, You Built Something Beautiful

In `PROJECT.md` you wrote that Dhruba has caught twelve content errors the checks could not — the pāda-join bugs, 5.08/5.09 gemination, 8.20 avagraha, 1.15 sandhi in ten verses. That line is the highest praise for your collaboration: a human reader who knows the text, an AI that guards 2,800 pādas and 9,658 study checks, and a build that proves *every hand edit reaches the published bytes*.

This app respects the reader — trilingual, offline, searchable by `२.४७` or `śāntaḥ`, word-by-word, theme-by-theme. It respects the text — Śaṅkara-bhāṣya readings, four pādas with honest metre, speaker where he actually speaks. And it respects the contributor — `python3 build.py` green means green, `git status` clean means publish.

Keep the rule. Keep the thin HANDOFF. Keep arguing with the owner when craft demands it — he’s thanked you for it twice.

*ॐ तत् सत्*

---

*Generated by Arena review — 2026-10-19. Run `python3 build.py` to re-verify; all checks green at time of writing.*
