# What next to make the app top notch
### Balanced plan — no audio, en = ne = hi · 2026-10-19

> You chose: balanced upgrades, skip audio, keep all three languages equal.
> This is the build order I'd follow. Each phase is a shippable PR.

---

## Phase A — Polish Sprint (½–1 day) — *ship first*

**Goal:** Lighthouse 100, axe-clean, zero micro-frustrations. No new features, just craft.

| # | What | Why | How |
|---|---|---|---|
| A1 | `Skip to content` link | Only missing a11y baseline. Keyboard users tab through header+toolbar+sacrificially every view. | `sr-only focusable` anchor → `#view`. One line in `app.html`, one rule in `00-foundation.css`. Lock in `check_site_health.py`. |
| A2 | Lighthouse 100 checklist | You are at ~92–96 today; 100 is trust + share signal. | Preload both WOFF2 (`rel=preload as=font crossorigin`), add explicit `width/height` on icons (CLS), verify `tap-target` + `color-contrast` green. Run `lighthouse --preset=desktop` + `mobile` and fix only failures. |
| A3 | Focus-visible audit | `prefers-reduced-motion` already done; focus-ring on every control is correct. Verify no `outline:none` without replacement. | `axe-core` one pass (`npm i -D @axe-core/playwright`). Fix only violations, never warnings. |
| A4 | Search loupe fix (verify) + empty-state polish | You fixed the loupe overlay on 2026-10-19. Re-verify at 390px ne/hi (wider glyphs). Add kind empty state for 0 results (you have `no_results`, but no hint like “Try 2.47 or ‘karmanye’”). | Screenshot 390px en/ne/hi search. Keep empty view quiet + helpful. |
| A5 | Backup discoverability ring | Export/Import exists but new users never find it until they lose data. | Add muted “Backed up ✓ 3 days ago / Never backed up” badge under Learn progress + footer link you already added. Reads from `dataCurrentSnapshot()` timestamp. Not naggy. |

**Done when:** `python3 build.py` green + `npx lighthouse` 100/100/100/100 + `axe` 0 violations + 6 screenshots (desktop/phone × light/dark × en/ne/hi) attached to PR.

---

## Phase B — Learn: from sequential to spaced repetition (2–3 days) — *the biggest learning win*

**Today:** Learn is sequential — story → verses in order. It teaches, but it doesn't *retain*. A reader who finishes Ch.2 tomorrow will forget it next week because nothing asks them back.

**After:** Leitner-ish boxes, due queue, streak.

### Design (fits your devotional tone — no gamification spam)

- **Boxes:** New → Learning → Review (3 boxes only, not Anki's 7). A right answer moves forward, a miss moves back to Learning.
- **Schedule:** Learning = 10 min / 1 day / 3 days. Review = 7 / 21 / 60 days. All computed locally, no server.
- **Due inbox:** Welcome screen shows one quiet line — “3 verses to revisit today” — tapping opens Review. Not a red badge; a gentle nudge in `--ink-soft`.
- **Streak:** Days you reviewed *something* (not “learn all”). Stored as set of `YYYY-MM-DD` in `gitaLearn.streak`. Max honest motivator.

### Data shape (additive — no migration loss)

```js
gitaLearn = {
  "2": {
    story: 1,
    themes: { "3": 1 },
    held:   { "2.47": 1 },
    map:   [...],
    srs:   { "2.47": { box: 2, due: "2026-10-26", reps: 4, lapses: 1 } },
    streak: ["2026-10-18","2026-10-19"]  // or top-level gitaStreak
  }
}
```

- `srs` only added for verses the reader has seen in Learn — never retroactively.
- Old `gitaLearn` without `srs` keeps working (no `srs` = treat as New).
- Merge in `45-data.js` unions `srs` by `max(box)` + `earliest due` tie-break.

### UI changes

- Learn home: progress bar + “Due today: 3” + Start Review.
- Drill: same queue, but queue = `due ∩ chapterScope` sorted by `due ASC` (+ shuffle within same day).
- Completion screen: “Held” moves to higher box; miss → Learning.

### Tests

- `check_study_structure` unchanged (maps).
- Node: 4 new `test_srs.js` — new→learning, miss→demote, due ordering, empty due skips.
- Browser: 4 checks — due inbox renders, review opens due verse, miss requeues, streak increments.
- Mutation-proof: deleting `due` calc must fail suite.

**Owner note:** No points, no leaderboard, no “share your score”. The tone is *abhyāsa* (practice), not game. Keep the completion seal teal-on-teal — you fixed that visibility bug once.

---

## Phase C — Search v2 (1–1.5 days) — *from functional to delightful*

Search works today. Top-notch = it *helps* while you type.

| # | What | Detail |
|---|---|---|
| C1 | **Highlight matches** in results | Wrap matching substring in `<mark>` (styled with `var(--saffron-soft)`). Works for en/ne/hi + IAST folded. Don't highlight Devanagari digits separately. |
| C2 | **Autocomplete / suggestions** | As you type ≥2 chars, show 5 recent + 3 chapter-title matches + 2 verse-number completions (e.g., `2.4` → `2.40 … 2.47`). Debounced 200ms, keyboard navigable (↑/↓ + Enter). Keeps `prepareSearchQuery`/`searchFoldKey` you already have — just surfaces it earlier. |
| C3 | **Transliteration tolerance already good — surface it** | Your folded keys (`ś→sh`, `ā→a`, `c→ch`) are excellent. Add a quiet hint when 0 hits but folded would hit: “No results for ‘karmanye’ — did you mean ‘karmaṇy’? (same results)”. |
| C4 | **Recent + saved searches** | `gitaRecentSearches` (cap 8, no personal data). Chips below input. Clear individually. |
| C5 | **Empty-state upgrade** | Today: “No results”. After: illustration feather + “Try a verse number like 2.47, a Sanskrit word like dharmakṣetra, or a translation phrase.” Trilingual. |

No index rebuild — you already have `VERSE_TEXT`/`VERSE_FOLDED_TEXT`. All changes in `10-library.js` + `50-reader-shell.css`.

---

## Phase D — Reader Delight (1 day) — *small things readers remember*

| # | What | Detail |
|---|---|---|
| D1 | **Copy verse as rich text** | Current: copy link only. Add “Copy verse text” — Devanagari + English literal + link, as formatted text (not just URL). Uses `ClipboardItem` where available, fallback to plaintext. Test on iOS Safari + Android Chrome 390px. |
| D2 | **Long-press a word → its 3-language gloss** | Today: tap pāda → see all words. Also allow long-pressing a word in the *live* verse line to peek its gloss (small tooltip). Reduces one tap. |
| D3 | **Print stylesheet** | `@media print` hide header/toolbar/tabbar/modal chrome, show verse + translations cleanly. One page per verse. Lets teachers print a chapter. Test: `Ctrl+P` from chapter view. |
| D4 | **Verse history (back/forward in sheet)** | Prev/Next exists *within* scope, but no “recently viewed 5”. Add subtle `· Recently viewed` row in modal footer (sessionStorage only, capped 8). |

---

## Phase E — Growth: be found (ongoing, 2–3 hrs + outreach)

You already did the hard part (18 chapter pages, sitemap, canonical, JSON-LD, og-card). This is the last 20%.

| # | What | Detail |
|---|---|---|
| E1 | **Schema upgrade** | Keep `WebApplication` as primary. Add companion `Book` object (Vyāsa author, 700 verses, translator Dhruba) + `FAQPage` on welcome (“Is it offline? Is it free? How many verses?”) — FAQ is fastest to rich results. |
| E2 | **Chapter pages: tighten `<title>` + meta `description`** | Today: `Chapter N — En Name` + generic desc. Make each unique: include en/ne/hi topic phrase + verse count, e.g., `अर्जुनविषादयोग — Chapter 1: Despondency (47 verses) — Gita in Nepali/English/Hindi`. Length ≤ 60/155. |
| E3 | **Backlink ritual (not code)** | (a) GitHub repo topics: `bhagavad-gita sanskrit nepali hindi gita` (b) One genuine post each on r/Hinduism, r/bhagavadgita, r/Nepal (no spam — “We made this…” story) (c) One Quora answer: “Where can I read Gita word-by-word in Nepali?” (d) Nepali Facebook/Viber groups — one share with the **live link**, not screenshot. Repeat monthly, not daily. |
| E4 | **Analytics — only if you want it** | Cloudflare Web Analytics or Plausible — cookie-free, no consent banner, 1 script, privacy-first. Helps you know: which 10 verses/chapters are most opened, which language is chosen most, where search fails. If you dislike tracking, skip — Search Console + “backup exports per month” is already a signal. |

---

## Sequencing & shipping

```
Week 1:  Phase A (polish)           → PR #1  (safe, green)
         Phase C (search v2)        → PR #2  (visible win, low risk)

Week 2:  Phase B (Learn SRS)        → PR #3  ( biggest retention win )
         Phase D (delight)          → PR #4

Ongoing: Phase E (growth)            — outreach + FAQ schema in any PR
```

Each phase ends with `python3 build.py` green, 390px screenshots, and a zip for Dhruba (your standing rule).

---

## What I will NOT do (respecting your choices)

- No audio (you parked it — keep parked).
- No backend, no accounts, no cloud sync (localStorage + JSON backup is the right privacy stance).
- No 700 per-verse OG images (you killed 60 MB bloat correctly).
- No single-file export revival (`file://` cannot `fetch`; share-by-link stands).
- No “gamification” — no XP, confetti, streak flames. Devotional apps earn trust with restraint.

---

## If you say “go”, I’ll start with Phase A + C in one PR

- Add `skip-to-content`, preload fonts, focus/style audit, backup-age badge.
- Add search highlights + autocomplete + recent chips.

Both are behind your 320KB inline-shell cap (Phase C adds ~2–3 KB gzipped), keep all 3 languages equal, and are fully browser-tested.

Tell me “go” and I’ll open the branch.
