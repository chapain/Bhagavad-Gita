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

**The licence is narrower than "forbids redistribution", and it has to be read
exactly.** The file's header says the text is

> prepared by volunteers and is to be used for personal study and research. The
> file is not to be copied or reposted for promotion of any website or
> individuals or for commercial purpose without permission.

Three things follow, and they are not the same thing:

* **Not commercial use without permission.** This app is free and carries no
  advertising, so it is inside the permission-free space — but it is, on the
  plain words of the notice, *reposting* the file, which is the act the notice
  names. The permission clause exists precisely for this case, and the notice
  gives an address for corrections that also serves as the route to ask.
* **Not reposting "for promotion of any website or individuals".** The clause
  is aimed at people who lift the file to promote their own site. We are not
  doing that, but the wording is broad enough that we should not lean on our
  own reading of it.
* **Therefore: ask.** The transcription under `source/reference/` is kept for
  provenance and build input, it is never rendered into `docs/` or the
  generated site, and every anvaya in the app is stored as our own Devanagari
  inside `source/ch<N>.json` rather than served from the `.itx`.

**The right next step is a permission request to sanskritdocuments.org** (the
address in the file is `sanskrit at cheerful dot com`) before the anvaya of all
700 verses is published. If permission is refused, the anvaya layer cannot ship
as prose and the fallback is to keep it out of the built site while the word
rows remain — a decision for the owner, not for the build.

## Gita Press, *Gita-Padachchheda-Anvaya* (book code 17)

Examined 2026-11-21 at the owner's suggestion. A scanned copy is on the Internet
Archive (`archive.org/details/20221128_20221128_1327`), item size 139 MB, with
DJvu text and hOCR derivatives. Gita Press's own catalogue lists the edition as
still in print at ₹70, and the Press is an active publisher.

**On copyright, the owner's hunch is right — every word of it.** Jayadayal
Goyandka died on 17 April 1965. Under the Indian Copyright Act the term for a
literary work is the author's life plus sixty years, counted from the start of
the calendar year following death, so his writings entered the public domain on
**1 January 2026**. As of today (21 November 2026) the text of the
*Padachchheda-Anvaya* edition is out of copyright.

What that does **not** cover is the Press's later editorial additions and the
typography and layout of any particular printing. And a scan is a reproduction
of one printing. So the rule is narrow but workable: **Goyandka's text may be
used; a particular scan's pages may not be republished as pages.** We read the
text and write our own; we do not copy its pages or its running Hindi.

(Gita's own *anvaya* convention — anvaya, padachheda, word-meanings — predates
every printed edition; it is how the text has been taught orally for centuries.
What is attributable to Goyandka is his specific wording and glosses.)

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
