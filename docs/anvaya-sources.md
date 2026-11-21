# Where the anvaya comes from, and what may be claimed about it

Two reference sources were considered. One is usable as a working witness; one
is not usable at all. The distinction matters because the anvaya is the only
layer of this edition that claims to show the verse's own words in prose order,
and that claim has to rest on something a reader could in principle check.

## Sanskrit Documents' *anvayasandhivigraha* — the witness in use

`sanskritdocuments.org/doc_giitaa/gitAanvayasandhivigraha.itx`, complete for all
700 verses, retyped by Sunder Hattangadi. Each verse carries a saṃhitā-pāṭha
line, a padaccheda line and an anvaya line. Parenthesised words are the
editor's own supplied words.

This is what `source/reference/gita_anvaya_ch*.itx` transcribes, and therefore
what `source/anvaya.py` reads. It is a *labour*, not a translation: it adds no
interpretation of its own, which is what makes it usable as a check on the
verse rather than as a source of doctrine.

**Its licence forbids redistribution.** The transcription under
`source/reference/` is kept for provenance and for the build; it is not
republished in `docs/` or in the generated site. Anyone reusing this repository
must not lift it out and republish it either.

## Gita Press, *Gita-Padachchheda-Anvaya* (book code 17)

Examined 2026-11-21 at the owner's suggestion. A scanned copy is on the Internet
Archive (`archive.org/details/20221128_20221128_1327`), item size 139 MB, with
DJvu text and hOCR derivatives. Gita Press's own catalogue lists the edition as
still in print at ₹70, and the Press is an active publisher.

**It is not copyright-free, and the owner's hunch on that point does not hold.**
Jayadayal Goyandka died on 17 April 1965. Under the Indian Copyright Act (as
amended in 2012) the term for a literary work is the author's life plus sixty
years, counted from the start of the calendar year following death — so his
works entered the public domain on **1 January 2026**, not before. Even now that
the term has run, only Goyandka's own text is free; the Press's later editorial
matter, arrangement and typography are separate. And a scan is a copy of a
particular *edition*, whose typography and layout the publisher can still claim.

So: **Gita Press is not a source we may copy from, and it is not added to the
build.** It was read as a witness to compare our treatment against, which is a
different act from transcribing it.

### What the comparison settled

Three questions we had left open were answered by looking at how the book does
it. These are conventional, not proprietary — the same conventions appear in
every padachheda-anvaya edition in every Indian language — so following them
takes nothing from Gita Press.

1. **The word-meaning pair is the unit.** Each page prints two columns headed
   `अन्वयः शब्दार्थः अन्वयः शब्दार्थः` — anvaya word, then its meaning, then the
   next anvaya word. This is exactly the toggle we are building: the anvaya
   order and the word meanings are one view, not two. It confirms the design.

2. **The speaker announcement leads the anvaya.** The book's 1.01 begins
   `धृतराष्ट्र बोले` — "Dhṛtarāṣṭra said" — before `सञ्जय = हे संजय!`. Our
   transcribed reference omits the stage direction entirely, which had left the
   speaker's two rows with no place in the anvaya. The book's practice confirms
   restoring them at the head, which `_speaker_lead()` now does.

3. **Elliptical copulas are supplied and printed in parentheses.** The book
   prints `(सन्ति) = हैं` in 1.09, `(सन्ति) = हैं` again in 1.06, and `(सति)`
   in 1.20 — the same three verses where our mapping had reported an unglossed
   `santi`/`asti`/`sati`. Confirms `SUPPLIED_COPULAS` and `SUPPLIED_GLOSS`.

**And one correction to our own earlier claim.** We had recorded that the
world's padachheda-anvaya editions give *word meanings in anvaya order*. Gita
Press does not: its word columns follow the **anvaya's** order of words, but the
Hindi meanings it prints sit beside them in pairs, not as a running sentence,
and its running Hindi is a full translation, not a construal. So the
construed-literal layer is **our** device, not a reproduction of a traditional
one, and it should not be presented as though tradition hands it to us. It
stands on its own argument: it makes the literal's claim checkable.
