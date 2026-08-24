# Licence and attribution

## What is yours

**© 2026 Dhruba Chapain. All rights reserved.**

Original to this project, and owned by the author:

* the English, Nepali and Hindi **translations** — literal and flowing — of all
  700 verses;
* the **word-by-word meanings** (9,480 word glosses in three languages);
* the **theme and part structure** — 182 themes and 558 parts, with their titles
  and descriptions in three languages;
* the **four-quarter (pāda) division** and the pada-chheda word splits as
  presented here;
* the **interface, code, design and build system**.

These are original works of authorship. Under Indian and international copyright
law a translation is a derivative work in which the translator holds copyright
independently, even when the underlying text is public domain.

## What is not yours, and why that is fine

### The Sanskrit text — public domain

The Bhagavad Gītā is roughly two millennia old and is in the **public domain**
worldwide. No one owns the verses themselves. Courts have said this plainly:
there is no copyright in scripture, only in a particular author's commentary,
translation or adaptation of it.

This project ships only the bare Sanskrit — Devanagari and IAST — with no
commentary from any modern edition.

### The typeface — SIL Open Font License 1.1

**Noto Serif Devanagari**, © 2022 The Noto Project Authors, subsetted to the
Devanagari block and embedded as woff2.

The OFL permits embedding, modification and redistribution, including in
commercial and paid software. Three conditions apply, and all three are met:

| OFL clause | requirement | how this project complies |
|---|---|---|
| 1 | the font may not be sold on its own | it is not; it is a component of an application |
| 2 | the copyright notice and licence must travel with the font | the notice is preserved in the embedded woff2 name table **and** shown in the page footer; the full licence text is at `source/fonts/OFL-NotoSerifDevanagari.txt` |
| 3 | no Reserved Font Name may be reused on a modified version | the Noto Devanagari OFL declares **no** Reserved Font Name, so the subset may keep the name |

Subsetting is a permitted modification. "Noto" is a Google trademark; this
project uses the name descriptively, to credit the font, which clause 4 allows.

## Verse source

The Devanagari and IAST were originally derived from a freely circulated ITRANS
encoding of the Gītā. Because such encodings are typically offered for personal
study rather than redistribution, the project has:

* removed the `itrans` field from all 700 verses — it was unused by the build;
* kept only the Devanagari and IAST, which are the public-domain scripture
  itself rather than any contributor's encoding.

The text has since been independently corrected against the tradition — sandhi,
anusvāra before dentals and palatals, avagraha placement, and speaker
attribution — so what ships is a checked text, not a copied file.

## If you publish this commercially

Nothing here blocks it. The Sanskrit is public domain, the font licence permits
commercial use, and everything else is your own work. Keep the footer
attribution in place and you remain compliant.
