# Paraphrase-to-Sanskrit review (2026-11-22)

## Scope and status

Dhruba requested a new review of the flowing English, Nepali and Hindi
paraphrases, six chapters at a time, after the word-row/literal pass. The
paraphrase is freer than a literal: equivalent idioms, explanatory names and
ordinary compression are not by themselves defects. We compare the Sanskrit,
rows, reviewed literals and passage context; we correct substantive shifts,
not differences of wording for their own sake. Earlier work is recorded in
`literal-review-2026-11.md`, `semantic-audit.md`, and
`padachheda-literal-review-2026-11.md`.

**Batch 1: Chapters 1–6 (280 verses) read**, with the exception that 2.05's
interpretation is Dhruba's reserved decision: no part of that verse was
changed. **Chapters 7–18 remain to be read in this pass**, except for the
specific whole-book follow-ups listed below; those targeted checks do not make
those chapters reviewed. This is a human review, not proof of perfect semantic
fidelity. Different translations and contextual readings remain possible.

## Batch 1 — corrections

Only paraphrases changed; no Sanskrit, word rows or literals were edited.

- **1.10** removes the supplied concession and retains the insufficient /
  sufficient contrast rather than asserting the opposing army is numerically
  larger. This follows the existing edition's interpretation, not a resolution
  of the competing “unlimited/limited” reading. **1.11** keeps stationed
  troops, not an extra order to take positions or the ranking “above all”.
  **1.18** removes unsupported sequential “in turn”. **1.19** नभस् is sky,
  not the heavenly realm. **1.20** Hindi situates the action as battle is
  about to begin. **1.25** says these Kurus, not the entire clan. **1.29**
  gives the weakened limbs rather than just legs. **1.36** ne/hi call them
  aggressors, not established murderers. **1.46** keeps the weapon-bearing
  attackers and Arjuna's unarmed, unresisting condition.
- **2.07** Nepali uses consistent respectful address to Kṛṣṇa. **2.08** keeps
  a prosperous unrivalled earthly kingdom *and* sovereignty over gods; the
  ne/hi phrasing no longer suggests the gods rule Arjuna. **2.16** अन्तः is
  the truth/conclusion regarding both, not a dividing boundary; this follows
  the documented word-row/literal resolution. **2.21** Hindi retains the
  person who would be killed, not the person made to kill. **2.24** सनातन
  is everlasting, not merely ancient. **2.40** प्रत्यवाय is an adverse
  result, not an obstacle turning effort back. **2.42–43** puts the actual
  flowery speech in the speaker's mouth and retains rebirth as the fruit of
  action, plus both enjoyment and power. **2.45** निर्योगक्षेम retains
  acquisition and preservation, not substituted ego or possessiveness.
  **2.56–57** distinguish attachment and hatred from the narrower lust or
  merely being upset. **2.58** the tortoise comparison withdraws senses from
  their objects; the extra “first sign of danger” was not the point of the
  comparison. **2.65** it is the intellect of the serene mind that steadies.
- **3.02** keeps both “as if” comparisons; **3.03** does not add selflessness
  to the bare karma-yoga. **3.09** keeps action *other than sacrifice* as
  the binding category, not only explicitly selfish action: this revises the
  old test's exemption, not the owner's no-invented-selfishness rule.
  **3.10** beings and sacrifice are created together; what the latter grants
  is desires, not only necessities. **3.15** English now retains both links:
  action arises from Brahman and Brahman from the Imperishable, as the other
  languages did. **3.23** leaves its conditional open for 3.24 and presents
  the following “people follow my path” as a present statement, not its invented
  conditional result. **3.24** retains सङ्कर and the destruction of beings,
  with conditional force. **3.28** distinguishes non-attachment from denying
  all connection with action. **3.30** Nepali निर्मम is non-possessiveness;
  **3.36** Nepali retains the “as if forced” comparison.
- **4.10** many have reached his state, absorbed in and taking refuge in him,
  not an unqualified prediction about everyone who takes refuge. **4.16**
  अशुभ is evil/inauspiciousness rather than simply harm. **4.22** retains
  equality in success and failure in addition to freedom from opposites.
  **4.24** English retains the positive Brahman equivalences and the person
  reaching Brahman, rather than merely making sacrifice a path if the elements
  are viewed as Brahman. **4.28** yoga is not narrowed to meditation; study
  *and* knowledge remain, respecting the earlier reference-conflict ruling.
  **4.38** one perfected in yoga is not just someone ready for it.
- **5.02** does not add selflessness to bare karma-yoga. **5.03** en/hi keep
  neither hating nor longing. **5.07** follows the reviewed compound: the
  self has become the self of all beings, not merely seeing oneself in them.
  **5.19** retains the context of overcoming birth here, not conquering the
  world in a worldly sense. **5.23** the impulse must be endured before the
  body is left, not merely “right now”.
- **6.01** retains both fire and action, not just rituals. **6.07** restores
  the established relation to the Self/परमात्मा and honour/dishonour; the
  alternative reading of परमात्मा as one's own higher Self is recorded in
  `literal-review-2026-11.md` and was not silently adopted here. **6.08**
  retains knowledge and realization. **6.09** distinguishes well-wishers,
  friends, indifferent and neutral persons, and those hated; the earlier
  restored contrast of righteous and sinners remains. **6.14** ne/hi retain
  the vow of brahmacarya. **6.16** excessive wakefulness is not “never sleep”;
  **6.17** waking and recreation remain alongside food, work and sleep.
  **6.20** restores आत्मना, seeing the Self by the self. **6.21** ne/hi
  restore the intellect and the distinction between being established in the
  joy and not moving from *truth*. **6.22** no longer borrows 6.23's “know
  that as yoga/end of sorrow”, and says no *greater* gain rather than nothing
  else matters. **6.23** now states knowing the separation from union with
  sorrow as yoga, and practice with resolve and an undiscouraged mind.
  **6.31** retains being established in unity; **6.41** the household is
  prosperous, not merely fortunate; **6.46** कर्मी is a person of action,
  not necessarily a ritualist.

## Whole-book class screens and targeted follow-ups

- As with the earlier literal boundary audit, compare adjacent verses rather
  than assuming a paraphrase has the same boundary. The known 6.22/23 and
  11.26/27 cases were checked explicitly in all three languages. **11.26**'s
  three paraphrases also carried entry into the mouths from 11.27; this is now
  kept in 11.27 alone. **12.18**'s paraphrases used praise/blame from 12.19
  for मानापमान (honour/dishonour); both verses now retain their own pairs.
  A reproducible spelling-limited candidate screen is
  `python3 source/audit_paraphrase_boundaries.py`; it covers 700 verses and
  682 within-chapter adjacencies. Before these final boundary repairs it
  surfaced 74 ne and 45 hi candidates; the candidates were checked, with
  12.18 the clear additional hit. The remainder include contextual names,
  same-topic repetition and generic words. The final counts are 73/44. The
  screen uses a tail and rare exact row-gloss tokens, does not screen English,
  and misses paraphrases using different words (including 6.22 and 11.26);
  it is not a proof that other leaks are absent.
- An exact word-row द्वेष्टि scan found **2.57, 5.03, 12.17, 14.22, 18.10**.
  The previous reviewed distinction of hate from sadness was also missing at
  **12.17 en/hi**, corrected as a targeted follow-up; 14.22/18.10 use
  contextual resentment/dislike. A Sanskrit-text मानापमान scan found only
  **6.07, 12.18, 14.25**; 14.25 already has honour/disgrace. Exact screens
  find **प्रत्यवाय** only in 2.40, **निर्योगक्षेम** only in 2.45,
  **ब्रह्मचारि** only in 6.14, **कर्मिभ्य** only in 6.46, and
  **योगयज्ञ** only in 4.28. Exact spellings cannot cover inflection variants
  or synonyms. The 6.09 द्वेष्य screen also finds 9.29, where the paraphrase
  is contextual; the 1.10 अभिरक्षितम् row occurs only there, twice.
- A full text search for English `selfless` found the previously documented
  13.24 paraphrase lead. **13.24** now gives the yoga of action without adding
  that word, and, like **6.20**, keeps आत्मना “by the self” in all three
  paraphrases. This is a targeted correction, not a complete Chapter 13 review.
  3.03 and 5.02 were similarly narrowed to the words of their verses; the
  `selfish`/स्वार्थ test was strengthened after the 3.09 exemption was removed.
- Other previously noted paraphrase leads, including **10.28**'s “among
  procreators” and **13.15**'s “hard to grasp” versus unknowable, remain for
  the later six-chapter batches. Their presence illustrates the limit of this
  first batch and its screens; no later chapter is marked complete.

Regressions in `tests/test_paraphrase_review_2026_11.py` pin selected
relationships, conditionals, negatives, timing and verse boundaries. The
reference-conflict fixture changes only the affected paraphrases of 3.30, 4.28
and 6.09; prior word-row/literal decisions remain. The overlap guard is a
format/independence check, not semantic validation.
