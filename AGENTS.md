# AGENTS.md — read this first

This is the short, durable guide for a new AI or human contributor. Read it
before changing anything. It records current rules, not session history. Search
`HANDOFF.md` for recent work/roadmap items and `PROJECT.md` for the rationale
behind a feature or settled decision; do not read both archives front-to-back.

## Product

This is Dhruba Chapain's complete offline Bhagavad Gita study edition: 18
chapters, 700 verses, English / नेपाली / हिन्दी, with Sanskrit, IAST, four
pādas, word meanings, literal translations and paraphrases. Preserve its calm,
devotional, mobile-first character and warm saffron/teal manuscript identity.

The reading path is intentional: **Three Ways → chapter → themes → verses →
four pādas → words**. Progressive disclosure keeps the first view quiet while
allowing word-level study. Do not add commentary or revive a single-file
edition unless Dhruba explicitly changes those decisions. The deliverable is
the GitHub Pages link and installable PWA.

Dhruba reviews language and design closely. Verify reports against the source,
show evidence, and respectfully push back when good craft requires it. Never
silently broaden a content edit. Call him Dhruba or brother, never “bhai”.

## Governing rule

> `source/ch1.json` … `source/ch18.json` are canonical. Code renders and
> validates that content; it must not invent, rewrite or store parallel copies
> of Sanskrit, translations, glosses or pāda segmentation.

Parse structured data; never regex-rewrite JSON. Locate exact values and require
one unambiguous match. When one defect is found, inspect all 700 verses for the
same class. Green tests prove consistency, not textual correctness: read and
render the affected verse.

## Edit here

- All chapter/verse content: `source/ch<N>.json`
- Shell, design and behavior: `source/app.html`, `source/app.css`, `source/app.js`
- Trilingual interface wording: `source/i18n_ui.py`
- Reviewed maps/progress migration: `source/study_map_contract.json`
- Build, schema and checks: `source/build_gita.py`, `source/schema.py`,
  `source/check_*.py`

## Never hand-edit generated output

`index.html`, `data/ch*.js`, `chapter/*/index.html`, `chapter.css`, `sw.js`,
`sitemap.xml`, `robots.txt`, root fonts/icons and `404.html` are generated.
Change `source/`, rebuild, and keep the resulting output diff with its source.

The app is an inline shell plus 18 chapter payloads. The service worker
precaches it for offline use. Static chapter pages are the crawler-facing full
text and provide verse anchors; shares point to `/chapter/N/#vN.NN`. Do not
restore 700 share pages or promise `file://` operation.

## Current design contracts

- One unified chapter view: collapsed theme outlines expand to verse cards. Do
  not restore retired per-theme or continuous-reading views.
- A verse opens as a sheet. Canonical `d`/`t` produces two non-speaker display
  lines; `flow` supplies four pādas, speakers and five-field word rows.
- Word meanings are disclosed directly below the whole verse, before the
  literal and paraphrase. Keep the control obvious and keyboard accessible.
- English shows IAST; Nepali and Hindi intentionally hide it.
- Language, route, reader state and Learn/Play state survive refresh where
  applicable. Do not break session restoration when changing a view.
- On phones, Search stays in the sticky top bar; the five destinations use the
  bottom tab bar; the verse sheet is full-screen.
- Dark mode stays warm: no pure `#000` or `#fff`. Keep bundled Devanagari fonts.
- Every UI key and content map must be complete in en/ne/hi; never conceal a
  missing localization with English fallback.
- Before changing a disputed reading, search both archives for its verse number
  or phrase. Preserve owner-settled wording unless explicitly reopened.

## Build and verification

```bash
python3 build.py          # build plus all available checks
python3 build.py --fast   # build only; insufficient before delivery
python3 build.py --serve  # build, verify, then serve locally
```

A full run checks schema, 2,800 pādas, 2,100 paraphrase pairs, translations,
SEO/site health, study maps, Python tests and built-document Node tests. Browser
checks run only with Playwright/Chromium; explicitly report when skipped. Then
review `git status` and both source/generated diffs. For visual changes, inspect
desktop and 390 px, light/dark, and every affected language.

## Using project memory

- `README.md`: user-facing features, build and publishing.
- `HANDOFF.md`: status archive, roadmap and unresolved decisions.
- `PROJECT.md`: rationale, editorial decisions, mistakes and history.
- `STUDY_MAPS.md`: approved thematic map.

At session start: check Git state/recent commits, run the full build, then read
only archive sections relevant to the task. Update this file only when a
**durable rule or architecture contract** changes. Update `HANDOFF.md` only
when status/roadmap evidence will help a future session; do not duplicate
routine build reports across files.
