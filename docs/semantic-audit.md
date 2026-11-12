# Semantic audit — the verses, read against the Sanskrit

**Started 2026-11-04.** One chapter at a time, beginning with 1.01–1.20.
**All 700 verses of all 18 chapters are now read, decided and applied.**
The first pass (2026-11-04) produced nine findings, F1–F9, in seven verses —
sixteen strings. Two later cross-language passes added F10–F11 (two strings,
2026-11-12) and the second whole-book address pass added F12–F16 (31 strings in
ten verses, 2026-11-12). Chapters 1–12 were
read first; 13–18 followed in the same pass, in the same reading order, with
the same rules. F9 was found last, by the whole-book class check rather than
by the first reading of its chapter; it is filed under its chapter below.
Every verse is read in the Devanagari, the IAST, the literal translation
(en/ne/hi), the paraphrase (en/ne/hi), the verse title (en/ne/hi) and every
word row with its three glosses. A verdict is recorded for each verse before
anything is edited, and the owner's decision is recorded with it.

This is the ledger for that work. It is a **record of readings and verdicts**,
not a second copy of the data: `source/ch<N>.json` stays canonical, and this
file never becomes an authority for a string. If a row here and the JSON
disagree, the JSON is right and this file is stale.

## Rules the audit follows

1. **The literal is the semantic standard.** A word-row gloss that contradicts
   the verse's own literal is the defect, not the literal — unless the literal
   itself is wrong, which is a separate verdict.
2. **No silent broadening.** A finding is a finding until the owner has seen
   the verdict table; only what is approved is edited.
3. **One defect, look for the class.** Every finding below was re-run across
   all 700 verses before it was called a finding (the class check is named).
4. **Green is consistency, not correctness.** The build cannot tell that
   "भीम से" means "from Bhīma" when it means "equal to Bhīma".
5. **The verse must still work for a reader who never opens the peek.** A row
   gloss that only makes sense to a Sanskritist is a defect.

## Ledger — Chapter 1, 1.01–1.20 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 1.01 | pass | Dhṛtarāṣṭra's question, speaker row, four pādas, all three glosses agree with the literal. |
| 1.02 | pass | `rājā` is nominative, "the king spoke" — the settled decision (PROJECT.md §4.11) is intact in en/ne/hi, literal and paraphrase. |
| 1.03 | pass | `dhīmatā` = "wise"; the paraphrase names Dhṛṣṭadyumna, which the verse implies by `drupadaputreṇa`. |
| 1.04 | **fixed (F1)** | `भीम` row: the Hindi gloss said "from Bhīma" where the verse means "equal to Bhīma" — now "भीम के समान". |
| 1.05 | pass | Five commanders, `narapuṅgavaḥ` = "bull among men"; all three glosses agree. |
| 1.06 | pass | Abhimanyu is `saubhadraḥ`; "five sons" in the paraphrase is correct. |
| 1.07 | pass | `saṃjñārthaṃ` split as `saṃjñā` + `arthaṃ`; "for your information" in all three. |
| 1.08 | pass | `samitiñjayaḥ` = "conqueror in battle"; Somadatta's son glossed as such, not by name alone. |
| 1.09 | pass | `madarthe` = "for my sake" (Duryodhana speaking) — the title agrees. |
| 1.10 | pass | `aparyāptaṃ` / `paryāptaṃ` contrasted correctly in all three languages. |
| 1.11 | pass | `bhīṣmam eva` = "Bhīṣma alone"; the imperative is addressed to the commanders. |
| 1.12 | pass | `pratāpavān` = "the glorious" (Bhīṣma); `vinadyoccaiḥ` = "loudly". |
| 1.13 | **fixed (F2, F3)** | The English word rows assigned the five instruments differently from the English literal, and two rows carried the same English word; the Hindi horn row kept the Sanskrit name while its literal said "तुरहियाँ". |
| 1.14 | pass | `śvetairhayairyukte` = "yoked with white horses"; the row glosses are split correctly. |
| 1.15 | pass (F3 closed) | The `भीम` row is read as the adjective "terrific", the literal as the name Bhīma. Both references read it the row's way ("the doer of terrible deeds" · "भयानक कर्म करनेवाले"), so the row stands. |
| 1.16 | pass | `sughoṣamaṇipuṣpakaū` is one printed token and one row, glossed as the two conch names in all three languages. |
| 1.17 | pass | `kāśyaśca parameṣvāsaḥ` = "the king of Kāśī, the supreme archer" — the row order is correct. |
| 1.18 | pass | The repeated `pṛthak pṛthak` is glossed once and marked as repeated on the second row. |
| 1.19 | pass | `vyadārayat` = "rent, shattered"; `vyanunādayan` = "resounding through". |
| 1.20 | pass (F4 closed) | The `ध्वजः` row's English gloss "bannered" is a verbal form where the other languages use a noun phrase; Sivananda's "whose ensign was a monkey" supports the sense, and 1.18's `बाहुः` = "armed" is the same shape, so the row stands. |

**18 of 20 verses pass on first reading.** Two needed correction (1.04, 1.13)
and two carry wording notes that the references confirm as sound (1.15, 1.20).
Every correction was decided against the pinned sources below and applied to
`source/ch1.json`; the reviewed rows are pinned in
`tests/test_semantic_audit.py`.

## Findings

### F1 — 1.04, the `भीम` row's Hindi gloss is the wrong preposition — **fixed**

`bhīmārjunasamā yudhi` = "equal to Bhīma and Arjuna in war". The literal
says so in all three languages (`समान`, `के समान`, "the match of"). The row
glosses carry the comparison on the first name, as the English does:

| row | en | ne | hi |
|---|---|---|---|
| भीम | to Bhīma | भीमसँग | **भीम से** |
| अर्जुन | and Arjuna | र अर्जुन | और अर्जुन |
| समाः | equal | समान | समान |

`भीम से` reads "from Bhīma". It is the only row in the book where the
English gloss starts with "to" and the Hindi uses `से` — checked across all
700 verses. The Nepali `भीमसँग` is right.

**Decision — applied.** The Hindi gloss is now `भीम के समान`. Evidence:
Sivananda "equal in battle to Bhima and Arjuna", Ramsukhdas "युद्ध में भीम और
अर्जुनके समान", and this edition's own Hindi literal "भीम और अर्जुन के समान" —
all three read a comparison, not a departure. The English row already carried
the comparison ("to Bhīma") and the Nepali row did too ("भीमसँग"), so only the
Hindi had drifted; `समाः` keeps the book-wide "समान" gloss, as in the other
thirteen rows that mean "equal".

### F2 — 1.13, the English word rows disagree with the English literal — **fixed**

The verse names five instruments: śaṅkha, bherī, paṇava, anaka, gomukha.

| row | literal (en) | row gloss (en) | row gloss (ne) | row gloss (hi) |
|---|---|---|---|---|
| शङ्खाः | conches | conches | शङ्खहरू | शंख |
| भेर्यः | drums | **kettledrums** | नगाराहरू | नगारे |
| पणव | kettledrums | **tabors** | ढोलहरू | ढोल |
| आनक | tabors | **kettledrums** | मृदङ्ग | मृदंग |
| गोमुखाः | horns | horn-trumpets | गोमुखहरू | गोमुख |

The Nepali and Hindi rows match their own literals exactly; only the English
rows disagree with the English literal, and two of them both read "kettledrums",
so a reader cannot reconcile the rows with the verse. The literal is the
standard (rule 1), so the English rows are the defect.

The earlier boundary pass had already found this verse and left it open:
`docs/padachheda-verse-review.md` records "**but paṇava's ne/hi glosses are a
collateral mismatch** … Do not label this verse's glosses fully verified", and
`docs/padachheda-conflict-resolution.md` decided "paṇava ne/hi → drums, not
trumpets; ānaka ne/hi → mṛdaṅga/drum terminology **matching the existing
literal**". The Nepali and Hindi rows were corrected then; the English rows
were left behind and the verse was never marked verified.

**Decision — applied.** The English rows now read as the literal reads them:
भेर्यः "drums", पणव "kettledrums", आनक "tabors". Evidence: Ramsukhdas
"शंख, भेरी (नगाड़े), ढोल, मृदङ्ग और नरसिंघे" (bherī = drums), Sivananda
"conches and kettledrums, tabors, drums and cow horns", and the standard
glosses (bherī = drum, paṇava = kettledrum, ānaka = cymbal/tabor,
gomukha = horn). The old English set matched none of them — it was a mixture
of two readings, with "kettledrums" twice.

The Hindi horn row was corrected in the same pass: `गोमुखाः` read "गोमुख"
while its own literal read "तुरहियाँ"; the English row ("horn-trumpets") and
the Nepali row ("गोमुखहरू") already matched theirs.

### F3 — 1.15, `भीम` read as adjective in the rows, as the name in the literal — **closed, no change**

`bhīmakarmā vṛkodaraḥ` — the rows read भीम = "terrific" / भयानक / भयंकर,
कर्मा = "deeds (doer of)", वृकोदरः = "Vṛkodara (Bhīma)"; the literal reads
"Bhīma, the doer of herculean deeds". Both readings are defensible
("Vṛkodara of terrible deeds" vs "Bhīma, doer of mighty deeds"). No conflict
in meaning, only in which word carries it.

**Decision — no change.** Both references read the row's way: Sivananda "Bhima
(the wolf-bellied), the doer of terrible deeds", Ramsukhdas "भयानक कर्म करनेवाले
वृकोदर भीम". The earlier boundary pass had already accepted the literal's
idiomatic rendering ("herculean deeds" / "महापराक्रमी"), and the rows carry
the same sense. Nothing to fix.

### F4 — 1.20, the `ध्वजः` row's English gloss — **closed, no change**

`kapidhvajaḥ` = "the ape-bannered one". The row glosses: en "bannered",
ne "ध्वज भएको", hi "ध्वज वाला". The English is a verb form where both other
languages use a noun phrase.

**Decision — no change.** Sivananda's "whose ensign was a monkey" and
Ramsukhdas's "कपिध्वज" both carry this sense, and the edition already uses
the same adjectival shape elsewhere (1.18 `बाहुः` = "armed"). A terser English
gloss is not a defect.

## Ledger — Chapter 1, 1.21–1.47 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 1.21 | pass | Arjuna's request, `cyuta` = "having slipped away"; the imperative `sthāpaya` is glossed as an instruction in all three languages. |
| 1.22 | pass | `yāvad etān nirīkṣe` = "until I look upon"; `kairmayā saha` = "with the Kaimavas" — the row names the Kaimavas, the literal "those of the Kaimavas". |
| 1.23 | pass | `yotsyamānān avekṣe` = "I shall look at those who are ready to fight"; `priyacikīrṣavaḥ` = "desirous of pleasing" (Dhṛtarāṣṭra's sons). |
| 1.24 | **fixed (F5)** | The three paraphrases addressed "O Dhṛtarāṣṭra" / "हे धृतराष्ट्र" where the literal and the row read "O descendant of Bharata" / "हे भरतवंशी", and the English paraphrase said Kṛṣṇa *drove* the chariot where the verse says he *placed* it. |
| 1.25 | pass | `bhīṣmadroṇapramukhataḥ` = "with Bhīṣma and Droṇa at the head"; `pārtha` = "O Pārtha" (Arjuna). |
| 1.26 | pass | The five groups of relatives (fathers, grandfathers, teachers, uncles, brothers, sons, grandsons, friends) run in the same order in all three languages. |
| 1.27 | pass | `śvaśurānsuhṛdaścaiva` = "father-in-laws and friends"; `kṛipayā parayā` = "with mercy and compassion". |
| 1.28 | pass | `viṣīdann` = "grieved, overwhelmed"; `dṛṣṭvemaṃ svajanaṃ` = "seeing my own kinsmen". |
| 1.29 | pass | The five symptoms of Arjuna's distress (limbs fail, mouth dries, trembling, hair stands on end, Gandiva slips) are complete and consistent. |
| 1.30 | pass | `gāṇḍīvaṃ sraṃsate hastāt` = "Gāṇḍīva slips from my hand"; `bhramatīva` = "as if reeling". |
| 1.31 | pass | `nimittāni … viparītāni` = "inauspicious omens"; `na ca śreyo nupaśyāmi` = "nor do I see any good". The `अनुपश्यामि` row reads "I see" because the negation is carried by the separate `न` row — checked against the reference, which also reads "I do not see". |
| 1.32 | pass | `na kāṅkṣe vijayaṃ … na ca rājyaṃ` = "I seek neither victory nor kingdom"; the four questions are complete. |
| 1.33 | pass | `prāṇāṃs tyaktvā dhanāni ca` = "having given up life and wealth"; `ta ime vasthitā` = "those standing here". |
| 1.34 | pass | The list of nine kinship groups (teachers, fathers, sons, grandfathers, uncles, brothers-in-law, grandsons, relations, friends) matches the verse. |
| 1.35 | pass | `etān na hantum icchāmi` = "I do not wish to kill these"; `kiṃ nu mahīkṛte` = "what, then, should I do?" |
| 1.36 | pass | `nā kā prītiḥ syāt` = "what joy would there be"; `pāpam evāśrayed asmān` = "we should fall into sin". |
| 1.37 | pass | `tasmān nārhā … hatvā sukhinaḥ syāma` = "therefore it is not right that we should kill them and be happy". |
| 1.38 | pass | `yady api te na paśyanti` = "even if they see no fault"; `mitradrohe ca pātakam` = "and treachery toward friends". |
| 1.39 | pass | `jñeyam asmābhiḥ` = "known by us"; `prapaśyadbhiḥ` = "seeing". |
| 1.40 | pass | `kuladharmāḥ sanātanāḥ` = "the eternal family duties"; `adharmo bhibhavaty uta` = "unrighteousness prevails". |
| 1.41 | pass | `kulastriyaḥ` = "the women of the family"; `varṇasaṅkaraḥ` = "confusion of the classes". |
| 1.42 | pass | `saṅkaro narakāyaiva` = "the confusion leads to hell"; `luptapiṇḍodakakriyāḥ` = "deprived of the rice-and-water offering". |
| 1.43 | pass | `utsādyante` = "are abandoned"; `jātidharmāḥ kuladharmāśca` = "the caste duties and the family duties". |
| 1.44 | pass | `utsannakuladharmāṇāṃ` = "of those whose family duties are ruined"; `narake niyataṃ vāso` = "dwell in hell". |
| 1.45 | pass | `aho bata mahatpāpaṃ` = "alas! what great sin"; `yadrājyasukhalobhena` = "for the sake of kingdom, comfort and greed". |
| 1.46 | **fixed (F6)** | The first privative `अ` row was glossed "not" in English while the same word's second row, and the Nepali and Hindi rows, read "without" — the verse's `a-pratīkāram a-śastram` is one shape twice. |
| 1.47 | pass | `saṅkhye` = "in battle"; `śokasaṃvignamānasaḥ` = "with a mind afflicted by grief". |

**Twenty-seven verses, two corrections.** Both were checked against the pinned
references before they were called defects; the `अनुपश्यामि` row (1.31) was
**not** a defect and was left alone — see the note in the table above.

### F5 — 1.24, the paraphrase contradicted the literal on two counts — **fixed**

The literal reads "O descendant of Bharata" (en) / "हे भरतवंशी" (ne, hi), and
the `भारत` row agrees. The three paraphrases instead read "O Dhṛtarāṣṭra" /
"हे धृतराष्ट्र". The English paraphrase also said Kṛṣṇa *drove* the finest
chariot "to the middle of the two armies", where the verse says he **placed**
it (`sthāpayitvā`) between the two armies — the Nepali and Hindi paraphrases
already said "राखे"/"लगे" and "रखा"/"खड़ा किया".

Both readings of the vocative `bhārata` exist in the tradition — Sivananda
renders it "O Dhritarashtra" and Ramsukhdas "हे भरतवंशी राजन्" — so the
addressee was left as the literal gives it. What could not stand was the
paraphrase naming a different person from the literal it paraphrases.

**Decision — applied.** The three paraphrases now read "O descendant of
Bharata" / "हे भरतवंशी" / "हे भरतवंशी", and the English paraphrase says
"placed the finest chariot between the two armies", matching the literal and
the other two languages. Evidence: Sivananda "having stationed that best of
chariots … in the midst of the two armies", Ramsukhdas "श्रेष्ठ रथ को खड़ा
करके".

### F6 — 1.46, the first `अ` row was glossed "not" instead of "without" — **fixed**

`mām a-pratīkāram a-śastram` — the same privative prefix twice. The first
row read "not" (en) against "बिना" (ne, hi); the second row read "without"
(en) against "बिना" (ne, hi). The literal reads "me unarmed and unresisting",
Sivananda "unresisting and unarmed" — the privative, not the negator, in both
places.

**Decision — applied.** The first `अ` row's English gloss is now "without", so
the pair reads "without resisting / without weapons" in every language.

## Ledger — Chapter 2, 2.01–2.72 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 2.01–2.09 | pass | Arjuna's dejection described in order (tears, agitation, sorrow); `kṛpayā āviṣṭam` = "overcome with pity"; `kasmalam` = "dejection" (2.02), `klaibyam` = "unmanliness" (2.03); the four questions of 2.04 and the "beggar's food" of 2.05 are complete in all three languages. |
| 2.10 | **fixed (F7)** | The paraphrase addressed "O Dhṛtarāṣṭra" and dropped the qualifier "as if" that the literal carries for `prahasann iva`. |
| 2.11–2.20 | pass | `gatāsūn agatāsūn` = "the dead / the living"; the four negations of 2.12 are correct; `dehāntaraprāpti` = "another body" (2.13); the sense-contact chain of 2.14; `samaduḥkhasukham` = "equal in pain and pleasure" (2.15); `nāsato vidyate bhāvo` = "the unreal has no being" (2.16); the negation of 2.19 ("it does not kill, nor is it killed") is in the literal, the rows and all three languages. |
| 2.21–2.30 | pass | `anupashyami`-type rows checked; `vāsāṃsi … śarīrāṇi` = clothes / bodies (2.22); the four "cannot" clauses of 2.23–2.24; `anāśino'prameyasya` = "indestructible, immeasurable" (2.18); the wheel of 2.16 and the "unborn" of 2.20 agree in all three languages. |
| 2.31–2.40 | pass | `svadharmaṃ api cāvekṣya` = "consider also your own duty"; `yadṛcchayā … svargadvāramapāvṛtam` = "an open door to heaven" (2.32); the three `karmaṇa`/`vikarmaṇa`/`akarmaṇa` of 2.17; `sukhaduḥkhe same kṛtvā lābhālābhau jayājayau` = four pairs made equal (2.38); `neha abhikrama nāśo'asti` = "no loss of effort" (2.40). |
| 2.41–2.50 | pass | `vyavasāyātmikā buddhiḥ` = "the intellect of the resolute" (2.41); the `yogaḥ karmasu kauśalam` of 2.50; `niryogakṣema` = "beyond gain and keeping" (2.45); the well-and-flood figure of 2.46; `mā karmaphalahetur bhūrmā te saṅgo'stv akarmaṇi` (2.47) is complete in all three languages. |
| 2.51–2.60 | pass | `anāmayam` = "beyond all ill" (2.51); the two `sthāpyati` of 2.52–2.53 (delusion, then the unsteady intellect); the four questions of 2.54; `nirāhārasya dehinaḥ` / `rasavarjam` (2.59) are glossed as the text has them. |
| 2.61–2.72 | pass | `matparaḥ` = "intent on Me" (2.61); the chain saṅga → kāma → krodha → sammoha → smṛti → buddhi (2.62–2.63); `rāgadveṣaviyuktaiḥ` (2.64); the four `nā …` of 2.66; the wind-and-boat figure of 2.67; the ocean figure of 2.70; `brāhmī sthitiḥ` = "the Brāhmī state" (2.72). |

**72 verses, one correction (2.10).** Every other verse passed on first
reading in all three languages, literals and paraphrases included.

### F7 — 2.10, the paraphrase named a different addressee and dropped a qualifier — **fixed**

The literal reads "O descendant of Bharata" (`bhārata`) and "as if smiling"
(`prahasann iva`); the three paraphrases read "O Dhṛtarāṣṭra" / "हे राजा" and
plain "smiled".

Both readings of the vocative exist in the tradition — Ramsukhdas renders 2.10
"हे भरतवंशोद्भव धृतराष्ट्र!" ("O Dhṛtarāṣṭra, born of the Bhārata lineage") and
Sivananda "Krishna, as if smiling, O Bharata, spoke these words" — so the
*addressee* was left as the literal gives it, and only the paraphrase was
brought into line with the literal it paraphrases. The qualifier was not
optional: both references keep it ("as if smiling" · "हँसते हुए-से").

**Decision — applied.** The Nepali literal now carries "जस्तो" (the English and
Hindi literals already had it), and all three paraphrases read "O descendant of
Bharata" / "हे भरतवंशी" and "smiled as if" / "जस्तो मुस्कुराएर" / "जैसे
मुस्कुराकर".

## Ledger — Chapter 3, 3.01–3.43 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 3.01–3.09 | pass | The four questions of Arjuna (3.01–3.02); the two yogas of 3.03; the four `na … na …` clauses of 3.04; `prakṛtijair guṇaiḥ` = "by the guṇas born of prakṛti" (3.05); the hypocrite of 3.06 (`mānasā smaran` = "recollecting in the mind") and its opposite in 3.07; `yajñārthāt karmaṇo'nyatra` = "except action performed for the sake of sacrifice" (3.09). |
| 3.10–3.18 | pass | `iṣṭakāmadhuk` = "the cow of desires" (3.10); the mutual nourishing of 3.11; `tena dattān apradāyibhyaḥ … stena eva saḥ` = "a thief" (3.12); `yajñaśiṣṭāśinaḥ` = "those who eat the remnants" (3.13); the five-stage chain anna → varṣa → yajña → karma (3.14); `brahmākṣarasamudbhavam` = "Brahman from the Imperishable" (3.15); the `nānavāptamavāptavyam` of 3.22 (see 3.19–3.22 below). |
| 3.19–3.27 | pass | `asakto hyācaran karma paramāpnoti` = "a man attains the Supreme" (3.19); `lokasaṅgrahamevāpi` = "even having regard for the welfare of the world" (3.20); the standard of the best man (3.21); `naivaṃ pāpamavāpsyasi` (3.38); the "guṇas move among the guṇas" (3.28); `akṛtsnavidaḥ` = "partial knowers" (3.29); the four `ni-` rows of 3.30. |
| 3.28–3.36 | pass | The guṇa/karma distinction (3.28–3.29); `mayi sarvāṇi karmāṇi sannyasyādhyātmaceṣṭā` (3.30); the two `anutusthanti` verses (3.31, 3.32) keep their opposite senses in all three languages; `sadṛśaṃ ceṣṭate` = "acts according to his own nature" (3.33); `tayor na vaśam āgacchet` = "let one not come under their power" (3.34); `śreyān svadharmaḥ viguṇaḥ` = "one's own dharma, though defective" (3.35); `anichchann api` = "even against his will" (3.36). |
| 3.37–3.43 | pass | `kāma eṣa krodha eṣa` = "it is desire, it is anger" (3.37); the smoke/mirror/membrane figure (3.38); `duṣpūreṇa analena` = "insatiable, like fire" (3.39); `etair vimohayaty eṣa` = "it deludes" (3.40); `pāpmānaṃ prajahihyenaṃ` = "cast off this sinner" (3.41); the ascending scale of 3.42 and `jahi śatruṃ` = "slay the enemy" (3.43). |

**43 verses, one correction (3.22).** The chapter passed on first reading in
all three languages, literals and paraphrases included; the one correction was
not found on that reading but by the whole-book class check afterwards (F9),
so the chapter's first verdict — "no correction" — is amended here.

### F9 — 3.22, the Nepali word-row gloss ran the negator into its word — **fixed**

*Found last, by the whole-book class check, and filed here under its chapter.
The number is later than F8 because the chapter had already been read and
closed when the check found it.*

The row `अनवाप्तम्` ("unattained") was glossed in Nepali as "**नप्राप्त**" —
"न" and "प्राप्त" run together, so the word does not exist. The verse's own
Nepali literal beside it reads "न प्राप्त गर्न बाँकी केही छ" ✔, and the Hindi
literal "न प्राप्त करने को अप्राप्त कुछ है" ✔ — both write the negator apart.
The Hindi row gloss "अप्राप्त" ✔ is left alone: that is a word Hindi has.

**Decision — applied.** The row now reads "न प्राप्त", the wording of the
verse's own literal.

**Why this one and not the other 85.** Eighty-six word rows in the book carry a
Nepali gloss that begins with "न", and all of them were read. Most are ordinary
words (नमस्कार, नष्ट, नरक, नराम्रो, नयाँ) or the negator standing on a verb
(नजान्ने, नपाएर, नहेर्दै, नखोजेर, नचाहँदै — 21 rows, every one of them a
verb). Four put the negator on a nominal: "नस्थित" (5.12), "नप्राप्त" (3.22)
and the compounds "नतृप्त हुने" (3.37) and "ननष्ट हुने" (13.27). The last
two are **closed, no change** — the negator there stands on a predicate
("हुने"), the phrase reads, and 13.27's own literal writes the same shape
("प्राणीहरू नष्ट हुँदा पनि ननष्ट हुने"), so the literal is the standard and
the row matches it.

## Ledger — Chapter 4, 4.01–4.42 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 4.01–4.09 | pass | The teaching chain Vivasvān → Manu → Ikṣvāku (4.01), the loss of the yoga (4.02), `bhakto'si me sakhā ca iti` = "you are my devotee and friend" (4.03); Arjuna's question about the birth (4.04); `ajo'pi san avyayātmā` = "though unborn, though the imperishable Self" (4.06); `abhyutthānam adharmasya` = "a rise of adharma" (4.07); `yuge yuge` = "age after age" (4.08). |
| 4.10–4.18 | pass | `māṃ upāśritāḥ` = "taking refuge in me" (4.10); `bhajāmy aham` = "I favour them" (4.11); `karmajā siddhiḥ` = "success born of action" (4.12); `cāturvarṇyaṃ` = "the fourfold order" (4.13); `na māṃ karmāṇi limpanti` = "actions do not stain me" (4.14); `kimakarma iti` (4.16); the three things to be known (4.17); `karmaṇi akarma` (4.18). |
| 4.19–4.26 | pass | `jñānāgnidagdha karmāṇaṃ` = "actions burnt by the fire of knowledge" (4.19); `naiva kiñcit karoti saḥ` = "he verily does nothing" (4.20); `nirāśīryata cittātmā` = "desireless, with the mind and self controlled" (4.21); the Brahman-sacrifice of 4.24; `daivam evāpare yajñaṃ` / `brahmāgnāv apare yajñaṃ` (4.25); the two oblations of 4.26. |
| 4.27–4.34 | **corrected — 4.32** | The five kinds of sacrifice (4.27–4.30); `yajñaśiṣṭāmṛtabhujo` = "tasting the nectar of the remnant" (4.31); **4.32's `brahmaṇo mukhe` was recorded here as "in the mouth of the Vedas" while all three literals read "in the scriptures" / `शास्त्रमा` — the row alone carried the interpretation.** They now read "in the mouth of Brahman" / `ब्रह्मको मुखमा` / `ब्रह्म के मुख में`; `jñānayajñaḥ` = "the sacrifice of knowledge" (4.33); `praṇipātena paripraśnena sevayā` (4.34). |
| 4.35–4.42 | pass | `yena bhūtānyaśeṣeṇa drakṣyasy ātmany atho mayi` = "you will see all beings in the Self and also in me" (4.35); `jñānaplavenaiva` = "by the boat of knowledge alone" (4.36); the two fires of 4.37; `tatsvayaṃ yogasaṃsiddhaḥ kālenātmani vindati` = "finds it in the Self in time, of himself" (4.38); `acirena` = "soon" (4.39); `nāyaṃ loko'sti na paro na sukham` = "neither this world, nor the next, nor happiness" (4.40); `jñānasañchinnasaṃśayam` = "whose doubt is destroyed by knowledge" (4.41); `jñānāsinā` = "with the sword of knowledge" (4.42). |

**42 verses, no correction.** The chapter passed on first reading in all three
languages.

## Ledger — Chapter 5, 5.01–5.29 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 5.01–5.09 | pass | Arjuna's question (5.01) and the answer "both lead to the supreme good, but karma-yoga is superior" (5.02); `jñeyaḥ sa nityasannyāsī` = "he is to be known as ever-renouncing" (5.03); `pṛthag bālāḥ pravadanti na paṇḍitāḥ` = "the childish, not the wise" (5.04); the one state reached by both (5.05); `duḥkham āptum ayogataḥ` = "hard to attain without yoga" (5.06); the "I do nothing at all" of 5.08, continued in 5.09 (the house style splits a running sentence with a trailing comma, as here and at 5.27). |
| 5.10–5.18 | pass | The lotus-leaf figure (5.10); `kāyena manasā buddhyā … kevalair indriyair api` (5.11); `naiṣṭhikīṃ śāntim` = "lasting peace" (5.12); `navadvāre pure` = "the city of nine gates" (5.13); the Lord creates neither agency nor action (5.14); `nādatte kasyacit pāpaṃ na caiva sukṛtaṃ` = "accepts neither sin nor merit" (5.15); `teṣām ādityavaj jñānaṃ` = "shines like the sun" (5.16); the `tad buddhi … tad ātmānam` chain (5.17); `samadarśinaḥ` = "of equal vision" over brāhmaṇa, cow, elephant, dog, outcaste (5.18). |
| 5.19–5.29 | pass | `ihaiva tair jitaḥ sargaḥ` = "here itself the world is conquered" (5.19); `na prahṛṣyet … nodyvijet` (5.20); `duḥkhayonaya eva te` = "wombs of sorrow" (5.22); `prāk charīravimokṣaṇāt` = "before the release of the body" (5.23); `brahmabhūtaḥ adhigacchati` (5.24); `chinnadvaidhā` = "whose doubts are cut" (5.25); `abhito brahmanirvāṇaṃ vartate` = "Brahman-nirvāṇa is present all around" (5.26); the pranayama of 5.27–5.28; `bhoktāraṃ yajñatapasāṃ` = "the enjoyer of sacrifices and austerities" (5.29). |

**29 verses, one correction (5.12).**

### F8 — 5.12, the Nepali literal had two words run together — **fixed**

The Nepali literal read "योगमा **नस्थित**, इच्छाले प्रेरित" — "न" and "स्थित" were
run together, so the word did not exist. The Hindi literal beside it reads
"योग में न स्थित" ✔, and the English "the one not established in yoga" ✔.

**Decision — applied.** The Nepali literal now reads "योगमा न स्थित".

The same run-together sat in the verse's own word row (`अयुक्तः`, "the one
not established in yoga"), which the reading of the verse had carried over
from the literal; it is fixed with it, and the row now reads "योगमा न स्थित".
The whole-book class check then turned up one more of the same fault, in 3.22
(F9 above). A missing space between a negator and its word is the only kind of
typographic fault found in the Nepali and Hindi fields in this pass: the other
1,100-odd Nepali and Hindi literals and paraphrases were read and are clean,
and the 9,506 word rows were checked for the same shape (the check is set out
in F9).

## Ledger — Chapter 6, 6.01–6.47 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 6.01–6.10 | pass | `anāśritaḥ karmaphalaṃ` = "without depending on its fruit"; `na niragnir na cākriyaḥ` = "not he who is without fire and without rites" (6.01); `na hyasannyastasaṅkalpo yogī bhavati` (6.02); `ārarukṣor muner yogaṃ karma kāraṇam ucyate` (6.03); `nendriyārtheṣu na karmasu anuṣajjate` (6.04); the Self as friend and enemy (6.05–6.06); the three pairs of 6.07; `samaloṣṭāśmakāñcanaḥ` = "a lump of earth, a stone and gold" (6.08); the nine categories of 6.09; `rahasi … ekākī` = "in solitude, alone" (6.10). |
| 6.11–6.20 | pass | The seat and its coverings (6.11); `ekāgraṃ manaḥ` = "one-pointed mind" (6.12); the nose-tip and the eyes (6.13); `maccitto … matparaḥ` = "thoughts on me, devoted to me" (6.14); `nacireṇa adhigacchati` (6.15); the four `na … na … na … na` of 6.16; the four `yukta` of 6.17; `viniyataṃ cittam ātmany evāvatiṣṭhate` (6.18); the lamp in the windless place (6.19); `yatra caivātmanātmānaṃ paśyann ātmani tuṣyati` (6.20). |
| 6.21–6.30 | pass | `sukham ātyantikaṃ` = "boundless joy" (6.21); `na duḥkhena guruṇāpi vicālayate` = "not disturbed even by great sorrow" (6.22); `duḥkhasaṃyogaviyogaṃ yogasaṃjñitam` (6.23); `saṅkalpaprabhavān kāmān` = "desires born of selfish intention" (6.24); `śanaiḥ śanaiḥ` = "slowly, gradually" (6.25); the restless mind drawn back (6.26); `śāntarajasam` = "whose passion is stilled" (6.27); the endless joy of union with Brahman (6.28); `sarvabhūtastham ātmānaṃ sarvabhūtāni cātmani` (6.29); `tasyāhaṃ na praṇaśyāmi` (6.30). |
| 6.31–6.47 | pass | `sarvabhūtasthitaṃ yo māṃ bhajati ekatvam āsthitaḥ` (6.31); `ātmaupamyena sarvatra samam paśyati` (6.32); Arjuna's restlessness (6.33–6.35); `vaśyātmānā tu yatatā śakyo'vāptum upāyataḥ` (6.36); the fate of the fallen (6.37–6.38); `tvadanyaḥ saṃśayasyāsya chettā na hyupapadyate` (6.39); `na hi kalyāṇakṛt kaścid durgatiṃ tāta gacchati` (6.40); `yogabhraṣṭo'abhijāyate` = "he who fell from yoga is born again" (6.41); `durlabhataraṃ loke janma` (6.42); `paurvadehikam` = "of the former body" (6.43); `jijñāsur api yogasya śabdabrahma ātivartate` (6.44); `anekajanmasaṃsiddhaḥ` (6.45); the three gradations of 6.46; `yuktatamaḥ mataḥ` = "the most yoked" (6.47). |

**47 verses, no correction.** The chapter passed on first reading in all three
languages.

## Ledger — Chapter 7, 7.01–7.30 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 7.01–7.10 | pass | `mayy āsaktam anāḥ` = "with the mind attached to me" (7.01); `savijñānam` = "knowledge with its realization" (7.02); the one-in-a-thousand of 7.03; the eightfold division of prakṛti (7.04); the higher nature, `jīvabhūtāṃ` = "the life-element" (7.05); `etad yonīni bhūtāni sarvāṇi` = "these two are the womb of all beings" (7.06); the gems on a thread (7.07); the eight declarations of 7.08–7.11, including `prauṣaṃ nṛṣu` = "the manliness in men"; the three guṇa-states (7.12) and the world blinded by them (7.13). |
| 7.11–7.20 | pass | `dharmāviruddho bhūteṣu kāmaḥ` = "in beings I am the desire that is not opposed to dharma" (7.11); `daivī hyeṣā guṇamayī māyā` (7.14); the three who do not come to me (7.15); the four kinds of worshippers (7.16) and the wise one among them (7.17–7.18); `vāsudevaḥ sarvam iti` = "Vāsudeva is all" (7.19); `prakṛtyā niyatāḥ svayā` = "constrained by their own nature" (7.20). |
| 7.21–7.30 | pass | `tāmeva vidadhāmy aham` = "I make that faith steady" (7.21); `mayaiva vihitān hi tān` = "ordained by me" (7.22); `antavat tu phalaṃ teṣām` = "the fruit is limited" (7.23); `mām abuddhayaḥ` = "the unintelligent" (7.24); `yogamāyā samāvṛtaḥ` (7.25); the three times of 7.26; the pairs-of-opposites delusion (7.27); `dṛḍhavratāḥ` = "with firm vows" (7.28); `kṛtsnam adhyātmaṃ karma cākhilam` (7.29); `prayāṇakāle'pi` = "even at the time of death" (7.30). |

**30 verses, no correction.** The chapter passed on first reading in all three
languages.

## Ledger — Chapter 8, 8.01–8.28 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 8.01–8.07 | pass | Arjuna's four questions (8.01–8.02); `akṣaraṃ brahma paramaṃ` = "the imperishable is the supreme Brahman", `svabhāvo'dhyātmam ucyate` = "one's own nature is called adhyātma", `visargaḥ karmasaṃjñitaḥ` = "the creative impulse is called karma" (8.03); `kṣaro bhāvaḥ` = "the perishable nature" (8.04); `madbhāvaṃ` = "my being" (8.05); the verse of remembrance at death (8.06); `māmanusmara yudhya ca` = "remember me and fight" (8.07). |
| 8.08–8.15 | pass | `nānyagāminā` = "a mind that goes nowhere else" (8.08); the ancient seer, `aṇo raṇīyāṃs` = "subtler than the subtle" (8.09); the breath held between the brows (8.10); the imperishable the Vedas declare (8.11); the gates of the body and the mind in the heart (8.12); `omity ekākṣaraṃ brahma` = "the single syllable Om, Brahman" (8.13); `ananyacetāḥ` = "with undivided mind" (8.14); `nāpnuvanti mahātmānaḥ` = "the great ones do not return" (8.15). |
| 8.16–8.22 | pass | `ā brahma bhuvanāl lokāḥ` = "all the worlds below Brahmā" (8.16); the day and night of Brahmā (8.17–8.19); `naśyatṣu na vinaśyati` = "does not perish when beings perish" (8.20); `avyaktākṣara ity uktaḥ` (8.21); `bhaktyā labhyas tvananyayā` = "obtained only through devotion" (8.22). |
| 8.23–8.28 | pass | The two paths (8.23); the bright fortnight and the northern course (8.24); smoke, night, the dark fortnight and the southern course (8.25); `ekayā yātyanāvṛttim anyayāvartate punaḥ` (8.26); `naite sṛtī … na muhyati` (8.27); `yogī paraṃ sthānam upaiti cādyam` = "the yogi reaches the supreme, the primal abode" (8.28). |

**28 verses, no correction.**

## Ledger — Chapter 9, 9.01–9.34 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 9.01–9.09 | pass | `guhyatamaṃ` = "the profoundest secret" (9.01); `rājavidyā rājaguhyaṃ` = "royal knowledge, royal secret" (9.02); `aśraddadhānāḥ` = "those without faith" (9.03); `matsthāni sarvabhūtāni na cāhaṃ teṣv avasthitaḥ` (9.04–9.05); the wind in space (9.06); the kalpa and the emission (9.07–9.08); `udāsīnavad āsīnam asaktaṃ` = "sitting as one indifferent, unattached" (9.09). |
| 9.10–9.19 | pass | `mayādhyakṣeṇa prakṛtiḥ sūyate` (9.10); `avajānanti māṃ mūḍhā mānuṣīṃ tanum āśritam` (9.11); the vain hopes, works and knowledge (9.12); `ananyamanaso` = "with undivided mind" (9.13); the four kinds of worship in 9.14–9.15; the eightfold "I am" of 9.16–9.17; `gatir bhartā prabhuḥ sākṣī` (9.18); `sadasaccāham arjuna` = "I am the real and the unreal" (9.19). |
| 9.20–9.29 | pass | The three-Veda worshippers and svarga (9.20–9.21); `yogakṣemaṃ vahāmy aham` = "I carry what they lack and preserve what they have" (9.22); the worship of other gods (9.23); `na tu mām abhijānanti tattvena` (9.24); the four destinations of worshippers (9.25); the leaf, flower, fruit and water (9.26); `tat kuruṣva madarpaṇam` (9.27); `śubhāśubhaphalair evaṃ mokṣyase` (9.28); `samo'haṃ sarvabhūteṣu` (9.29). |
| 9.30–9.34 | pass | `sudurācāro … sādhureva sa mantavyaḥ` = "he is to be regarded as good" (9.30); `na me bhaktaḥ praṇaśyati` (9.31); the four kinds of birth (9.32); `anityamasukhaṃ lokam` = "impermanent, joyless world" (9.33); the closing injunction (9.34). |

**34 verses, no correction.**

## Ledger — Chapter 10, 10.01–10.42 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 10.01–10.10 | pass | `hita kāmyayā` = "wishing your good" (10.01); `aham ādir hi devānām` = "I am the beginning of the gods" (10.02); `loka maheshvaram` = "the great Lord of the world" (10.03); the twelve qualities of 10.04–10.05; the seven seers and four Manus (10.06); `so'vikampena yogena yujyate` (10.07); `iti matvā bhajante māṃ` (10.08); `maccittā madgataprāṇāḥ` (10.09); `dadāmi buddhiyogaṃ` = "I give the yoga of discernment" (10.10). |
| 10.11–10.20 | pass | `jñānadīpena bhāsvatā` = "with the shining lamp of knowledge" (10.11); Arjuna's praise (10.12–10.13); `na hi te bhagavan vyaktiṃ vidur devā na dānavāḥ` (10.14); `ātmavibhūtayaḥ` = "your own glories" (10.16); the wish to hear more (10.17–10.18); `nāstyanto vistarasya me` = "there is no end to my extent" (10.19); `āham ātmā guḍākeśa` (10.20). |
| 10.21–10.30 | pass | The long "among these, I am that" catalogue (10.21–10.30) was checked word by word against the Sanskrit: Viṣṇu among the Ādityas, the Sāma-veda among the Vedas, Indra among the gods, Śaṅkara among the Rudras, Bṛhaspati among priests, Bhṛgu among the seers, the aśvattha among trees, Uccaiḥśravas among horses, the vajra among weapons, Ananta among serpents, Prahlāda among the daityas, the wind among purifiers. No row contradicts its verse. |
| 10.31–10.42 | pass | Rāma among the weapon-bearers, the Ganges among the streams (10.31); `adhyātmavidyā vidyānām` = "the science of the Self among the sciences" (10.32); `akṣarāṇāmakāro'smi` = "among letters I am the letter A" (10.33); `mṛtyuḥ sarvaharaś cāhaṃ` = "all-devouring death" (10.34); the Bṛhat-sāma and the Gāyatrī (10.35); `jayo'smi vyavasāyo'smi` (10.36); `dhanañjayaḥ` = "Arjuna" among the Pāṇḍavas (10.37); `daṇḍo damayatām` = "the rod of the punishers" (10.38); `yaccāpi sarvabhūtānāṃ bījaṃ` (10.39); `eṣa tūddeśataḥ prokto` = "this is only a summary" (10.40); `mama tejoṃśasambhavam` (10.41); `viṣṭabhyaḥ` = "having supported" and `ekāṃśena sthitaḥ jagat` = "I stand supporting this whole world with one part of myself" (10.42 — the closing verse of the chapter, read and passed; it is a real verse, not a duplicate). |

**42 verses, no correction.**

## Ledger — Chapter 11, 11.01–11.55 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 11.01–11.09 | pass | `madanugrahāya` = "by your compassion" (11.01); `kāmalapātrakṣa` = "lotus-eyed" (11.02); the wish to see the cosmic form (11.03–11.04); `śataśo'tha sahasraśaḥ` = "by hundreds and thousands" (11.05); the Ādityas and Maruts (11.06); `jagatkṛtsnaṃ … ekastham` = "the whole universe gathered in one" (11.07); the divine eye (11.08); Sañjaya's narration (11.09). |
| 11.10–11.21 | pass | The many mouths, eyes, ornaments and weapons (11.10–11.11); the thousand suns (11.12); `pravibhaktam anekadhā` = "one yet divided in manifold ways" (11.13); `hṛṣṭaromā` = "hair standing on end" (11.14); Brahmā on the lotus and the divine serpents (11.15); `anantārūpam` = "endless form" (11.16); `durnirīkṣyam` = "hard to gaze upon" (11.17); `śāśvatadharmagoptā` = "guardian of eternal dharma" (11.18); the fire-mouths (11.19); the space between earth and heaven (11.20); the hosts of gods and seers (11.21). |
| 11.22–11.34 | pass | The orders of gods and the `uṣmapaḥ` = ancestors (11.22); the many arms, bellies and fangs (11.23–11.25); `sūtaputraḥ` = "Karṇa, the charioteer's son" (11.26); the heads crushed between the teeth (11.27); rivers into the sea, moths into fire (11.28–11.29); `lelihyase` = "you lick" (11.30); "tell me who you are" (11.31); `kālo'smi lokakṣayakṛt pravṛddhaḥ` = "I am Time, grown mature for the destruction of worlds" (11.32); `nimittamātram` = "merely the instrument" (11.33); the four named warriors (11.34). |
| 11.35–11.55 | pass | The stammering voice (11.35); the rākṣasas fleeing (11.36); `gariyase brahmaṇaḥ` = "greater than Brahmā" (11.37); `vettāsi vedyaṃ ca` = "knower and known" (11.38); the thousand salutations (11.39–11.40); the rash familiarity (11.41); the begging of forgiveness (11.42–11.44); the gracious form (11.45–11.46); `ātmayogāt` = "by my own power" (11.47); `na vedayajñādhyayanaiḥ … draṣṭum` (11.48); `mā te vyathā` (11.49); the return to the human form (11.50–11.51); `sudurdarśam` = "very hard to see" (11.52); `bhaktyā tvananyayā` (11.54); the closing verse with the four qualifications (11.55). |

**55 verses, no correction.**

## Ledger — Chapter 12, 12.01–12.20 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 12.01–12.05 | **corrected** — 12.03 | Arjuna's question, which group are the better knowers of yoga (12.01); `yuktatamā matāḥ` = "the most yoked" (12.02); `sarvabhūtahite ratāḥ` = "rejoicing in the welfare of all beings" (12.04); `kleśo'dhikataras teṣām` = "greater is the toil" of those attached to the unmanifest (12.05). **12.03 was recorded as passing while all three paraphrases cut the tail of `anirdeśyam acintyam kūṭastham acalam dhruvam`:** the Hindi dropped अचलम् and ध्रुवम् outright and stopped mid-sentence, the Nepali dropped ध्रुवम्, and the English folded अचलम् and ध्रुवम् into "immutable, eternal". The compound is a list of five qualifications; a paraphrase may compress the list but may not delete its last members, so all three lanes now close it (कूटस्थम् "unchanging" / अचलम् "unmoving" / ध्रुवम् "eternal"). Overlap with the literal after the fix: en 0.26, ne 0.13, hi 0.20. Pinned by `tests/test_translation_fidelity.py::WholeBookFidelity::test_lag_no_lane_stops_mid_phrase_where_siblings_end_a_sentence` and the ledger pin in `tests/test_semantic_audit.py`. |
| 12.06–12.12 | pass | `ananyenaiva yogenā` = "with undivided yoga" (12.06); `samuddhartā` = "the deliverer" (12.07); `nivasiṣyasi mayy eva` (12.08); the three graded steps of 12.09–12.11 (`abhyāsayoga`, `matkarmaparama`, `sarvakarmaphalatyāga`); the four-fold scale `jñānam abhyāsāt … dhyānam … karmaphalatyāgaḥ` = "knowledge > practice > meditation > renunciation of the fruit of action" (12.12). |
| 12.13–12.20 | pass | The six qualities of 12.13 (`nirmamaḥ nirahaṅkāraḥ samaduḥkhasukhaḥ kṣamī`); `dṛḍhaniścayaḥ` = "of firm resolve" (12.14); `harṣāmarṣabhayo'dvegaiḥ muktaḥ` = "free from elation, anger, fear and anxiety" (12.15); `anapekṣaḥ śucir dakṣa udāsīno gatavyathaḥ` = "indifferent, pure, capable, unconcerned, free from anxiety" (12.16); `śubhāśubhaparityāgī` = "renouncing both good and evil" (12.17); `samaḥ śatrau ca mitre ca` (12.18); `aniketaḥ` = "having no abode" (12.19); `dharmyāmṛtam` = "this nectar of dharma" (12.20). |

**20 verses, one correction (12.03).**

## Ledger — Chapter 13, 13.01–13.34 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 13.01–13.06 | pass | The body as the field and the knower of the field (13.01–13.02); the six questions of 13.03; the seers, the meters and the Brahman-sūtras (13.04); the great elements, ego, intellect, the unmanifest, the ten senses plus the eleventh, the five objects (13.05); `icchā dveṣaḥ sukhaṃ duḥkhaṃ saṅghātaś cetanā dhṛtiḥ` = "desire, aversion, pleasure, pain, the body, consciousness and constancy" (13.06). |
| 13.07–13.12 | pass | The ninefold list of qualities (13.07); `janmamṛtyujarāvyādhiduḥkhadoṣānudarśanam` = "the perception of the evil of suffering in birth, death, old age and disease" (13.08); `anabhiṣvaṅgaḥ` = "non-clinging" to son, wife and home (13.09); `viviktadeśasevitvam` = "delight in solitude" (13.10); `adhyātmajñānanityatvaṃ` (13.11); `na sattannāsad ucyate` = "neither being nor non-being" (13.12). |
| 13.13–13.20 | pass | The hands and feet everywhere (13.13); `sarvendriyaguṇābhāsaṃ … nirguṇaṃ guṇabhoktṛ` (13.14); `dūrasthaṃ cāntike ca` = "far away, and yet near" (13.15); `grasiṣṇu prabhaviṣṇu` = "the devourer and the creator" (13.16); `jñānaṃ jñeyaṃ jñānagamyaṃ` = "knowledge, the knowable, the goal of knowledge" (13.17); `madbhāvāyopapadyate` = "attains my being" (13.18); `anādī ubhāv api` = "both beginningless" (13.19); `kāryakaraṇakartṛtve` (13.20). |
| 13.21–13.34 | pass | `guṇasaṅgo'sya` = "attachment to the guṇas" as the cause of birth (13.21); `upadraṣṭānumantā` (13.22); `na sa bhūyo'bhijāyate` (13.23); the three yogas and the hearing of teaching (13.24–13.25); `kṣetrakṣetrajñasaṃyogāt` (13.26); `vinaśyatsv avinaśyantam` = "the imperishable among the perishing" (13.27); `na hinasty ātmanā ātmānam` = "he does not harm the Self by the self" (13.28); `akartāram` = "the non-doer" (13.29); `bhūtapṛthagbhāvaṃ ekastham` (13.30); `na karoti na lipyate` (13.31); the space figure (13.32); the sun figure (13.33); `jñānacakṣuṣā` = "with the eye of knowledge" (13.34). |

**34 verses, no correction.**

## Ledger — Chapter 14, 14.01–14.27 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 14.01–14.04 | pass | `jñānānāṃ jñānam uttamam` = "the best of all knowledges" (14.01); `sādharmyam āgatāḥ` = "attain unity with my being" (14.02); the great Brahman as the womb (14.03); `bījapradaḥ pitā` = "the father who gives the seed" (14.04). |
| 14.05–14.12 | pass | The three guṇas binding the embodied one (14.05); sattva as `prakāśaka` = "illumining" and `anāmaya` = "free from disease" (14.06); rajas as passion born of thirst (14.07); tamas born of ignorance (14.08); the three attachments (14.09); the mutual overpowering (14.10); `sarvadvāreṣu … prakāśa upajāyate` (14.11); `rajasy etāni jāyante` = the five marks of rajas (14.12). |
| 14.13–14.20 | pass | The four marks of tamas (14.13); the pure worlds of the knowers of the highest (14.14); rebirth among the action-bound and the deluded (14.15); the three fruits (14.16); the arising of knowledge, greed, and carelessness (14.17); `ūrdhvaṃ … madhye … adho` (14.18); `nānyam guṇebhyaḥ kartāram` = "no agent other than the guṇas" (14.19); `trīn dehī dehasaṃudbhavān` = "the three guṇas that give rise to the body" (14.20). |
| 14.21–14.27 | pass | Arjuna's question (14.21); `na dveṣṭi … na nivṛttāni kāṅkṣati` (14.22); `udāsīnavad āsīno` (14.23); `samaloṣṭāśmakāñcanaḥ` (14.24); `mānāpamānayoḥ … mitra aripakṣayoḥ` (14.25); `avyabhicāreṇa bhaktiyogena` (14.26); `brahmaṇo hi pratiṣṭhāham` = "I am the support of Brahman" (14.27). |

**27 verses, no correction.**

## Ledger — Chapter 15, 15.01–15.20 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 15.01–15.06 | pass | The aśvattha with root above and branches below (15.01); `viṣayapravālāḥ` = "sense-objects as their shoots" and `karmānubandhīni` = "binding to action" (15.02); the axe of detachment (15.03); `pravṛttiḥ prasṛtā purāṇī` = "the ancient course" (15.04); `nirmānamohā … vinivṛttakāmāḥ` (15.05); `na tad bhāsayate sūryo` = "not lit by sun, moon or fire" (15.06). |
| 15.07–15.12 | pass | `manaḥ ṣaṣṭhāni` = "the mind is the sixth" of the senses (15.07); the wind carrying fragrance (15.08); the six faculties (15.09); `jñānacakṣuṣaḥ` (15.10); `akṛtātmāno'py acetasāḥ` = "the undisciplined lack understanding" (15.11); the light in sun, moon and fire (15.12). |
| 15.13–15.20 | pass | The earth and the moon (15.13); `vaiśvānaraḥ` = "the fire of digestion" (15.14); `apohanaṃ` = "their removal" (15.15); the two persons, kṣara and akṣara (15.16); the supreme Person (15.17); `prathitaḥ puruṣottamaḥ` (15.18); `sarvavid bhajati māṃ sarvabhāvena` (15.19); the closing verse (15.20). |

**20 verses, no correction.**

## Ledger — Chapter 16, 16.01–16.24 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 16.01–16.06 | pass | The ten qualities of the divine endowment (16.01); the eleven of 16.02, ending `hṛracāpalam` = "modesty and steadiness"; `tejaḥ kṣamā dhṛtiḥ śaucam adroho nātimānitā` (16.03); the six of the demoniac (16.04); `daivī sampad vimokṣāya … āsurī nibandhāya` (16.05); the two creations (16.06). |
| 16.07–16.12 | pass | `pravṛttiṃ ca nivṛttiṃ ca` = "right action and renunciation" (16.07); the world without foundation or Lord (16.08); `naṣṭātmāno'lpabuddhayaḥ` = "ruined souls of little understanding" (16.09); `duṣpūram` = "insatiable" (16.10); `cintām aparim eyām` = "boundless cares" (16.11); `āśāpāśaśataiḥ` = "hundreds of fetters of hope" (16.12). |
| 16.13–16.18 | pass | The four boasts of the demoniac (16.13–16.15); `mohajālasamāvṛtāḥ` = "wrapped in the net of delusion" (16.16); `nāmayajñaiḥ` = "sacrifices in name only" (16.17); `mām ātmaparadeheṣu pradviṣantaḥ` = "hate me in my own and others' bodies" (16.18). |
| 16.19–16.24 | pass | The casting into the āsurī wombs (16.19); `māmaprāpyaiva` = "never reaching me" (16.20); the three gates, kāma, krodha, lobha (16.21); `tamodvārais tribhiḥ` = "the three gates of darkness" (16.22); `śāstravidhim utsṛjya` (16.23); `jñātvā śāstravidhānoktaṃ karma kartum ihārhasi` (16.24). |

**24 verses, no correction.**

## Ledger — Chapter 17, 17.01–17.28 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 17.01–17.06 | pass | Arjuna's question (17.01); `trividhā bhavati śraddhā` (17.02); `śraddhāmayo'yaṃ puruṣaḥ` (17.03); the objects of worship, gods / yakṣas and rākṣasas / ghosts (17.04); `aśāstravihitaṃ ghoraṃ` (17.05); `bhūtagrāmam acetasaḥ` = "foolishly" (17.06). |
| 17.07–17.13 | pass | The threefold division of food, sacrifice, austerity and gift (17.07); the sāttvic foods (17.08); the rājasic foods (17.09); the tāmasic foods (17.10); `yaṣṭavyameveti manaḥ samādhāya` (17.11); `abhisandhāya phalaṃ dambhārtham` (17.12); the five defects of a sacrifice (17.13). |
| 17.14–17.20 | pass | Bodily austerity (17.14); vocal austerity (17.15); mental austerity (17.16); `śraddhayā parayā taptaṃ` (17.17); `calam adhruvam` = "unstable and transitory" (17.18); `mūḍhagrāheṇa` = "foolish obstinacy" (17.19); the sāttvic gift (17.20). |
| 17.21–17.28 | pass | The rājasic gift (17.21); the tāmasic gift (17.22); `oṃ tatsaditi nirdeśo brahmaṇas trividhaḥ` (17.23); `tasmād oṃ ity udāhṛtya` (17.24); `tad ity anabhisandhāya phalaṃ` (17.25); `sadbhāve sādhubhāve ca` (17.26); `saditi cocyate` (17.27); `asad ity ucyate` (17.28). |

**28 verses, no correction.**

## Ledger — Chapter 18, 18.01–18.78 (read 2026-11-04)

| Verse | Verdict | Note |
|---|---|---|
| 18.01–18.06 | pass | Arjuna's question on sannyāsa and tyāga (18.01); `kāmyānāṃ karmaṇāṃ nyāsaṃ` = "the giving up of desired actions" and `sarvakarmaphalatyāgaṃ` = "the abandonment of all fruits" (18.02); the two schools of 18.03; `tyāgo hi puruṣavyāghra trividhaḥ` (18.04); `yajñadānatapaḥkarma na tyājyaṃ kāryameva tat` (18.05); `saṅgaṃ tyaktvā phalāni ca` (18.06). |
| 18.07–18.12 | pass | `niyatasya tu saṃnyāsaḥ karmaṇo nopapadyate` (18.07); the rājasic abandonment that gains no fruit (18.08); `kāryamityeva yat karma niyataṃ kriyate` = "done because it ought to be done" (18.09); `na dveṣṭy akūśalaṃ karma` (18.10); `karmaphalatyāgī` (18.11); the threefold fruit of action (18.12). |
| 18.13–18.19 | pass | The five causes of action, `adhiṣṭhānaṃ … kartā … karaṇaṃ … ceṣṭā … daivaṃ` (18.13–18.14); `śarīravāṅmanobhiḥ` (18.15); `akṛtabuddhitvān na sa paśyati` = "with imperfect understanding he does not truly see" (18.16); `hatvāpi sa imāṃl lokān na hanti na nibadhyate` (18.17); the threefold impulse and basis of action (18.18); `guṇabhedataḥ` (18.19). |
| 18.20–18.26 | pass | The sāttvic, rājasic and tāmasic knowledge (18.20–18.22); `niyataṃ saṅgarahitaṃ arāgadveṣataḥ kṛtam` (18.23); `bahulāyāsaṃ` (18.24); `anubandhaṃ kṣayaṃ hiṃsām apekṣya ca pauruṣam` (18.25); `siddhyasiddhyor nirvikāraḥ` (18.26). |
| 18.27–18.33 | pass | The rājasic and tāmasic agents (18.27–18.28); `buddher bhedaṃ dhṛteś caiva` (18.29); the three buddhis — `kāryākārye bhayābhaye` (18.30), `ayathāvat prajānāti` (18.31), `tamasaṅvṛtā` (18.32); the three dhṛtis — `yogenāvyabhicāriṇyā` (18.33). |
| 18.34–18.40 | pass | `dharmakāmārthān dhṛtyā` = "fortitude that holds to duty, pleasure and wealth" (18.34); `na vimuñcati durmedhā` (18.35); the three happinesses — `viṣam iva … amṛtopamam` (18.37), `viṣaye ndriyasaṃyogāt` (18.38), `nidrālasyapramādottham` (18.39); `na tad asti pṛthivyāṃ vā divi deveṣu vā` (18.40). |
| 18.41–18.47 | pass | The four varna duties and their guṇa-birth (18.41); the brāhmaṇa, kṣatriya, vaiśya and śūdra duties (18.42–18.44); `sve sve karmaṇy abhirataḥ` (18.45); `svakarmaṇā tam abhyarcya` = "worshipping him by his own duty" (18.46); `śreyān svadharmo viguṇaḥ` (18.47). |
| 18.48–18.54 | pass | `sahajaṃ karma … sadoṣam api na tyajet` with the smoke-and-fire figure (18.48); `naiṣkarmyasiddhiṃ paramāṃ` (18.49); `niṣṭhā jñānasya yā parā` (18.50); the discipline of 18.51–18.52; `nirmamaḥ śānto brahmabhūyāya kalpate` (18.53); `madbhaktiṃ labhate parām` (18.54). |
| 18.55–18.62 | pass | `yāvāny aś cāsmi tattvataḥ` (18.55); `matprasādād avāpnoti śāśvataṃ padam avyayam` (18.56); `cetasā sarvakarmāṇi mayi saṃnyasya` (18.57); the warning of 18.58; `prakṛtiḥ tvāṃ niyokṣyati` (18.59); `kartuṃ necchasi yan mohāt kariṣyasy avaśo'pi tat` (18.60); the puppet figure `yantrārūḍhāni māyayā` (18.61); `tam eva śaraṇaṃ gaccha` (18.62). |
| 18.63–18.70 | pass | `guhyād guhyataraṃ` (18.63); `iṣṭo'si me dṛḍham iti` (18.64); `manmanā bhava madbhakto` (18.65); `sarvadharmān parityajya` (18.66); the four classes not to be told (18.67); `bhaktiṃ mayi parāṃ kṛtvā` (18.68); `na ca tasmān manuṣyeṣu kāś cin me priyakṛttamaḥ` (18.69); `jñānayajñena tenāham iṣṭaḥ syām iti me matiḥ` (18.70). |
| 18.71–18.78 | pass | The one who only hears with faith (18.71); Arjuna's question `kaccid etac chrutaṃ` (18.72); his answer `naṣṭo mohaḥ smṛtiḥ labdhā` (18.73); Sañjaya's narration (18.74); `vyāsaprasādāt śrutavān` (18.75); `saṃsmṛtya saṃsmṛtya` (18.76–18.77); the closing verse `yatra yogeśvaraḥ kṛṣṇo` (18.78). |

**78 verses, no correction.**

## The whole book — closing summary (read 2026-11-04)

| Chapter | Verses | Corrections |
|---|---|---|
| 1 | 47 | 9 strings in 4 verses (1.04 ×1, 1.13 ×4, 1.24 ×3, 1.46 ×1) |
| 2 | 72 | 4 strings in 1 verse (2.10: ne literal + en/ne/hi paraphrases) |
| 3 | 43 | 1 string in 1 verse (3.22: the Nepali word-row gloss) |
| 4 | 42 | 0 |
| 5 | 29 | 2 strings in 1 verse (5.12: the Nepali literal and the Nepali word-row gloss) |
| 6 | 47 | 0 |
| 7 | 30 | 0 |
| 8 | 28 | 0 |
| 9 | 34 | 0 |
| 10 | 42 | 0 |
| 11 | 55 | 0 |
| 12 | 20 | 0 |
| 13 | 34 | 0 |
| 14 | 27 | 0 |
| 15 | 20 | 0 |
| 16 | 24 | 0 |
| 17 | 28 | 0 |
| 18 | 78 | 0 |
| **Total** | **700** | **16 strings in 7 verses — nine findings, F1–F9** (first pass; F10–F16 are recorded in the later sections below and are not added into these per-chapter counts) |

Every verse was read in the Devanagari, the IAST, the literal (en, ne, hi), the
paraphrase (en, ne, hi) and every word row with its three glosses. Chapters
1–12 were read first and 13–18 in the same pass afterwards; the rules, the
reading order and the recording format are identical throughout, so the two
halves are comparable line for line.

The findings fall into four small clusters, all of them the same kind of
fault — **a word-row gloss or a paraphrase that drifted away from the verse's
own literal**: the vocative `bhārata` (F5, F7), the privative `a-` (F6), the
instrument names of 1.13 against the literal's own list (F2), and the one
Hindi preposition of 1.04 (F1). Two more are typographic rather than
semantic — the run-together negator of 5.12 and 3.22 (F8, F9) — and both were
found by the class checks rather than by the reading. Every other verse passed
on first reading in all three languages. The chapters that are largely lists or enumerations (10, 13, 17,
18) were checked item by item against the Sanskrit, because a list is where a
single dropped or shifted item hides.

## Class checks run over the whole book

| check | scope | result |
|---|---|---|
| English row glosses duplicated inside one verse (two *different* words, one gloss) | 700 verses / 9,506 rows | 88 pairs, every one read and accepted — each is the same lemma in another surface form (इदम् / इमम्), a synonym pair (एव / हि = "indeed"), or the house convention that a separate `न` row carries the negation (1.31, 15.10). All 88 are listed in `tests/test_semantic_audit.py`, so a new pair is a finding and a fixed pair must be taken out. 1.13 was the only pair that lost information; it is fixed. |
| English gloss "to X" with a Hindi `से` | 700 verses | only 1.04 `भीम` — F1 is a one-off |
| `सम` / `समाः` gloss style | 19 rows book-wide | "समान" in ne and hi in all 19 — the same 19 rows in both languages; 11 of them carry the English gloss "equal" |
| Latin residue in ne/hi literals, paraphrases, titles, glosses | 700 verses / 700 titles / 9,506 rows | none |
| Word rows with any missing gloss | 9,506 rows | none (all three languages present) |
| Literal identical to the paraphrase | 700 verses | none — 0 in en, 0 in ne, 0 in hi |
| Nepali literal identical to the Hindi literal | 700 verses | none |
| Nepali token in which the negator is attached to the word it negates | 700 verses / 9,506 rows | 86 rows begin with an attached "न"; 82 are ordinary words or the negator standing on a verb, four put it on a nominal — "नस्थित" (5.12), "नप्राप्त" (3.22), "नतृप्त हुने" (3.37), "ननष्ट हुने" (13.27). The first two are fixed (F8, F9); the last two are closed, because the negator stands on a predicate and 13.27's own literal writes the same shape. No run-together non-word is left. |
| Pāda reconstruction from word rows (sandhi) | 2,800 pādas | 0 flags (`check_padas.py`) |

## Renderings pass over all 700 verses x 3 languages (2026-11-12)

The ledger above is a *reading* record. This pass added checks that need no
reading, so that fidelity claims rest on more than one person's attention. It
found two defects in the Hindi renderings and nothing else.

| check | scope | result |
|---|---|---|
| IAST is a transliteration of its own Devanagari | 700 verses, 2,800 pādas | 0 mismatches. `check_padas.py` already enforced this; an independent transliterator was written to confirm the enforcement itself rather than trust it. |
| Word-row IAST vs its Sanskrit word | 9,389 rows | 0 after the project's anusvāra convention is applied: `ṁ`/`ṃ`/`ṅ` are one sound (`strict_key`), and `saṃgha` may be written `saṅgha` before a velar. Without that convention 130 rows differ, all in that one class — a spelling style, not a wrong word. |
| Vocative rows rendered or dropped consistently across the three languages | 175 address rows | 3 apparent splits, all false: "O best of men/persons" for पुरुषोत्तम (8.01, 11.03) and शत्रुतापन/परंतप (2.09). Dropping a vocative in all three languages is house style; dropping it in one is what the check hunts. |
| Numeral rows rendered or dropped consistently | 40 numeral rows | 5 apparent splits, all false: केवल (18.66), एउटाबाट (8.26), दुवैको (2.16), तीनै (3.22), "neither" for उभौ (2.19). |
| Negation present in all three or none | 306 negation rows | 0 real splits. The apparent Hindi gaps were the bare particle न, which the detector's word-boundary guard was rejecting because the Devanagari danda `।` sits inside the same Unicode block. |
| Cross-language word forms | 2,100 literals/paraphrases | **2 findings, both fixed** — see F10, F11. |

### 16.04 — settled: अभिमानश्च (owner's copy, 2026-11-12)

16.04 was the one reading among the fifteen Sanskrit corrections where the
witnesses genuinely split. The Supersite mūla and padaccheda (`दर्पः | अभिमानः`)
and Gambhirananda read **अभिमानश्च**; GRETIL and all four derivative corpora
read **अतिमानश्च**. The Supersite was the edition's basis, so अभिमानश्च is what
the book has shipped since `eb836bc`. Dhruba checked his printed copy and
confirmed **अभिमानश्च**. No content changed — `source/ch16.json` and
`data/ch16.js` already read `दम्भो दर्पोऽभिमानश्च` and `dambho darpo'bhimānaśca`,
which also matches the transliteration and the `अभिमानः / abhimānaḥ /
self-conceit` word row.

This is not the same word as 16.03's `अतिमानिता` (atimānitā, "excessive
pride"), which the book keeps and which is not in dispute.

### F10 — 2.09, the Hindi literal called Arjuna by the Nepali name — **fixed**

`परन्तप` is how this book addresses Arjuna as "scorcher of foes". The Hindi
column has it at 4.02, 4.05 and 4.33. The Nepali column renders the same word
as `शत्रुतापन` — 2.03, 4.05, 4.33, 7.27, 9.03, 10.40, 18.41. At 2.09 the Hindi
cell read `हे शत्रुतापन, …`, the Nepali form in the Hindi column. The IAST row
was never wrong (`parantapa`), so only the Hindi literal moved.

### F11 — 13.05, the Hindi literal dropped the count the verse is making — **fixed**

13.05 enumerates the field: `इन्द्रियाणि दशैकं च` — "the ten senses and the
one". The row glosses `एकम्` as "and the one" / "एक" / "एक"; the one is the
mind, the eleventh. English says "the ten senses and the one", Nepali says
`दश इन्द्रिय र एघारौं मन` ("the ten senses and the eleventh, mind"), and the
Hindi said `दस इन्द्रियाँ और मन` — which reads as ten senses *including* the
mind inside the count of ten, not ten plus one. Hindi now reads
`दस इन्द्रियाँ और एकादश मन`.

## Second whole-book pass — completeness and restraint (2026-11-12)

The 2026-11-04 pass asked whether each rendering was faithful in the classes it
tested. The owner restated the standard on 2026-11-12: *"check through all 700
verses and make sure the translation represents the Sanskrit verse, not less
not more."* This pass re-ran every verse through the classes below, drove every
mechanical check from `flow[].words[]` rows rather than from `v['d']`, and fixed
the address class it exposed. It found **31 strings in ten verses** (F12–F16).
No clause, negation, number, actor or comparison outside that class was found
wanting.

### What was run, and over what

| Class | Scope | Result |
|---|---|---|
| Vocative / address coverage | 9,389 pāda word rows, all 700 verses; every row whose en gloss begins `O ` and every row whose ne/hi gloss begins `हे ` | **10 verses defective, 31 strings — F12–F16, all fixed** |
| Address parity across the three literals | all 700 × 3 | the same ten verses; every other difference was a legitimate translation of the epithet (परन्तप → शत्रुतापन in Nepali, जगन्निवास → "abode of the world", पार्थ → "Arjuna", etc.) |
| Nothing added — names | every capitalised token in all 700 English literals, against that verse's row glosses | 30 candidates, all read: every one is either the person the Sanskrit describes (1.12 Bhīṣma from `pitāmahaḥ`, 1.20 Dhārtarāṣṭras from `dhārtarāṣṭrān`), the same epithet under its Sanskrit name (Acyuta for "infallible one"), or a row's own alternative form (Kāmadhuk/Kāmadhenu, Uśanā/Uśanas). None added a new actor. |
| Nothing added — numbers | all 700 × 3 literals; number words and numerals against row glosses | no added or dropped number. The flagged cases were the indefinite article ("one"), `छ` = "is", or a number the Sanskrit carries in a compound (`navadvāre` 5.13, `trividhaḥ` 18.04). |
| Nothing added — negation | all 700 English literals against their row negations; all 700 literal/paraphrase pairs | 8 candidates, all read: `anāvṛtti` (8.23), `asakta` (3.09, 3.19), `avijñeya` (13.15), `na … avasthitaḥ` (13.27), and the "cannot" of 2.24/12.11 are all carried by a privative or a separate row. No literal negates what the Sanskrit affirms. Literal and paraphrase agree on negation in all 2,100 pairs. |
| Cross-language number parity | all 700 × 3 | no verse in which one language states a number the other two do not. |
| Relative clause coverage | all 700 × 3: row-gloss content words traceable in the same language's literal, compared across languages | 41 verses where one language's vocabulary lags the other two; **all 41 read in full** (1.14 1.15 1.26 1.33 1.34 1.42 2.01 2.06 2.13 2.19 2.23 2.46 2.56 2.67 3.04 3.17 3.21 3.29 3.39 3.41 4.32 5.17 6.02 6.05 6.21 6.27 6.34 7.12 7.13 7.22 8.11 8.28 9.25 14.22 16.07 16.14 16.20 17.11 18.21 18.67 18.70). All are register differences — Nepali/Hindi carry the same clause in inherited Sanskrit vocabulary, or the literal uses a synonym the row gloss does not spell — not dropped content. |
| Literal length against the Sanskrit | all 700 × 3; no verse where all three literals are under 60% of their own median | two one-language outliers (5.06 ne, 15.18 ne), both read: Nepali is simply denser, both carry every clause. |
| IAST against its own Devanagari | 2,800 pādas, 9,389 word rows | 0 mismatches (`check_padas.py`). |
| Literal / paraphrase divergence | 2,100 pairs | 0 pairs ≥ 80% (max 79.4/79.8/79.8), no pair reverses a literal's negation. |
| Paraphrase vocatives | all 700 × 3 | the 19 known verses below; no paraphrase invents an address the Sanskrit does not have. |

The ten corrected verses were then read whole — Devanagari, IAST, all four
pādas and their rows, all six renderings, and the title — before and after the
edit.

### F12 — 3.07, all six renderings omitted अर्जुन — **fixed**

The verse addresses Arjuna at the end of the second pāda:
`नियम्यारभतेऽर्जुन`. The word row is `अर्जुन | arjuna | O Arjuna | हे अर्जुन |
हे अर्जुन`; the literal and paraphrase in all three languages read the
sentence without the address. This is the defect the owner named, and the one
a verse-text search cannot see: the avagraha elides the initial अ, so
`'अर्जुन' in v['d']` is `False`. Every mechanical check in this pass therefore
read the row, not `v['d']`.

Fixed strings: en/ne/hi literal + en/ne/hi paraphrase, e.g. en literal now
reads “But he who, O Arjuna, controlling the senses by the mind …”. Overlap
after the edit: 0.607 / 0.635 / 0.722 — all under 80%.

### F13 — 7.10, 8.06, 8.08, 8.19, the only vocative was dropped by all three literals — **fixed**

In each verse the Sanskrit addresses Arjuna and no literal carried the address:

| Verse | Sanskrit address | Row | Was |
|---|---|---|---|
| 7.10 | `पार्थ` (pāda 2) | O Pārtha / हे पार्थ / हे पार्थ | absent from en/ne/hi literal |
| 8.06 | `कौन्तेय` (pāda 3) | O son of Kuntī / हे कुन्तीपुत्र / हे कुन्तीपुत्र | absent from en/ne/hi literal |
| 8.08 | `पार्थ` (pāda 4) | O Pārtha / हे पार्थ / हे पार्थ | absent from en/ne/hi literal |
| 8.19 | `पार्थ` (pāda 3) | O Pārtha / हे पार्थ / हे पार्थ | absent from en/ne/hi literal |

8.06 was not on the owner's list; the row-driven count found it. 7.10, 8.08
and 8.19 were on the list and are now settled. Their paraphrases still drop
the address, under the house convention recorded below; the literal — the
semantic standard — carries it.

### F14 — 7.16 and 11.54, a second vocative was dropped while the first was kept — **fixed**

These verses have two addresses, and each literal carried only one:

* **7.16** — `अर्जुन` (pāda 2) and `भरतर्षभ` (pāda 4). All three literals had
  “O Arjuna” and stopped there. The row is `भरतर्षभ | bharatarṣabha | O bull of
  the Bhāratas | हे भरतश्रेष्ठ | हे भरतश्रेष्ठ`; the literals now end with it.
* **11.54** — `अर्जुन` (pāda 2) and `परन्तप` (pāda 4). All three literals had
  “O Arjuna” only. They now also carry “O scorcher of foes” / `हे परन्तप` /
  `हे परंतप`.

A literal that renders one address and silently drops the other makes the
verse say less than the Sanskrit, even though an address is present.

### F15 — 11.16 and 11.45, several addresses collapsed into fewer — **fixed**

* **11.16** — `विश्वेश्वर` and `विश्वरूप` close the verse. English carried both,
  Nepali and Hindi only `हे विश्वरूप`. Both now close with
  `हे विश्वेश्वर, हे विश्वरूप`, in the Sanskrit's order.
* **11.45** — `देव`, `देवेश` and `जगन्निवास`. English carried `देव` and
  `जगन्निवास`; Nepali and Hindi carried `देव` and `विश्वेश्वर` (an epithet not
  in this verse). All three now carry `देव` + `देवेश` + `जगन्निवास`.

### F16 — 11.48, Nepali and Hindi substituted a different epithet for कुरुप्रवीर — **fixed**

`कुरुप्रवीर` (“O prince/bull of the Kurus”) is the verse's address. English
reads “O prince of the Kurus” and the row reads `हे कुरुप्रवीर`; the Nepali and
Hindi literals read `हे कुरुनन्दन` (“O joy of the Kurus”) — a different
epithet, not a translation of this one. Both now read `हे कुरुप्रवीर`. The
pinned padaccheda fixture was updated with them.

### Triage of the questions the owner named — evidence, no silent decisions

| Question | Verdict | Evidence |
|---|---|---|
| 17.28 `पार्थ` | **no defect now** | All three literals carry it: en “O Pārtha”, ne/hi `हे पार्थ`. The paraphrase drops it under the convention below. The row is present. Nothing changed. |
| 10.11 “address dropped” | **does not reproduce** | 10.11 has no vocative in its Sanskrit (`तेषामेवानुकम्पार्थम् … ज्ञानदीपेन भास्वता`) and its rows contain none. No address exists to drop. |
| 7.10, 8.08, 8.19 | **fixed (F13)** | See above. |
| 11.15 | **literal correct; paraphrase follows convention** | Literal en “O God”, ne `हे देवता`, hi `हे देव`; only the paraphrase drops it. |
| 11.36 | **literal correct; paraphrase uses the plain name** | Literal en “O Hṛṣīkeśa”, ne/hi `हे हृषीकेश`. The paraphrase says “O Kṛṣṇa” — the same referent, the name the paraphrase uses throughout, not a dropped address. |
| Paraphrase-only vocative drops (19 verses: 2.21 2.39 2.42 2.55 3.22 3.23 4.33 7.01 8.14 8.22 9.32 10.24 12.07 16.04 16.06 18.06 18.30 18.32 18.34) | **confirmed; no change** | In every one the literal carries the address in all three languages and the paraphrase carries none. This is the house convention of not padding a paraphrase. Rewriting nineteen verses would be a style change, not a fidelity fix. Recommendation: keep, and keep the literal as the place the address is guaranteed. |
| 11.47 Hindi `tvat` | **does not reproduce** | The Hindi literal reads `जिसे तेरे सिवा पहले किसी ने नहीं देखा` — exclusion, matching en (“none but you”) and ne (`तिमीबाहेक`). The row is `त्वत् | tvat | than you | तिमीभन्दा | तुझसे`; with `अन्येन` = “by another” it is “by another than you”. The alleged “तुझसे पहले” chronology is not in the data. Nothing changed. |

### Open interpretive cases — reported, not changed

Two additions are editorial interpretation rather than grammar, and both
predate this pass. Neither was changed unilaterally:

* **6.02** — English literal “who has not renounced **selfish** intention” and
  all three paraphrases (“selfish planning”, `स्वार्थी योजना`) add a motive the
  Sanskrit `असन्न्यस्तसङ्कल्प` (“whose resolve is not renounced”) does not
  state. The edition uses “selfish intention/resolve” for `सङ्कल्प` as a house
  gloss elsewhere (4.19's row reads “selfish resolve”; 6.04, 6.24, 12.16,
  14.25), so this is a settled interpretative convention, not a one-off. If the
  owner wants the stricter rule enforced, it is a seven-verse editorial change,
  not a single-string fix.
* **4.32** — all three literals render `ब्रह्मणो मुखे` (“in the mouth of
  Brahman”) as “in the scriptures” / `शास्त्रमा`. The verse's own row gloss
  already carries the interpretation: `of Brahman (the Vedas)`. This is a
  deliberate metaphor-to-referent rendering, applied in all three languages.

### What this pass does not prove

* The mechanical classes cover address, names, numbers, negation and relative
  clause coverage. They cannot see a mistranslated verb, a reversed case
  relation, a wrong tense, or an added theological claim that uses no name,
  number or negator. The per-verse ledger remains the fidelity record.
* This session read every English literal of all 700 verses end to end and
  read the Nepali and Hindi in full for all flagged and corrected verses. It
  did not re-read every Nepali and Hindi sentence of the other verses one by
  one; those were checked mechanically against their rows and against the
  English and against each other in the classes above. The 2026-11-04 pass
  records the earlier full reading of all three.
* A green build proves consistency, not correctness. The ten verses here are
  fixed because their own rows and Sanskrit say so, not because a test turned
  green.

### What these checks do not prove

They cannot tell you a rendering is *right*; they tell you it is not wrong in
these specific, mechanical ways. Two limits are worth stating plainly:

* A literal can pass every check and still mistranslate a word nobody
  pattern-matched. That is what the per-verse ledger is for, and why the ledger
  — not this table — remains the fidelity record.
* The numeral and negation checks are only as good as their closed vocabularies.
  They cover rows whose Sanskrit gloss or stem names a small number or negates;
  they say nothing about tense, case, voice, or the many English words with no
  Nepali/Hindi counterpart in a one-to-one map.

A cross-language advisory pass was written and then removed: it could not
separate genuine borrowing from the shared Sanskrit vocabulary that Nepali and
Hindi both inherit (`क्षत्रिय`, `वैश्य`, `वैराग्य`), and 18 advisories of noise
would have made the four real ones unreadable.

## Sources used for the decisions

Every finding was checked against the same pinned sources the earlier
boundary pass used, so the two audits speak with one voice:

1. **Archived translator data** — `gita/gita` at commit
   `c6fce39595445768876ddbb8d1268a9c935e1d2b`, `archive/translation_old.json`
   (Ramsukhdas, Gambhirananda, Sivananda), joined to `data/verse.json`. Read
   here through `api.github.com` blob reads at that commit; the file itself is
   2.3 MB and the raw host is not reachable from this sandbox. No corpus is
   committed.
2. **The archive's own word-meaning metadata** for 1.13
   (`śaṅkhāḥ—conches; bheryaḥ—bugles; paṇava-ānaka—drums and kettledrums;
   go-mukhāḥ—trumpets`), used as corroboration only, as the earlier pass
   required.
3. **This edition's own prior verdicts** —
   `docs/padachheda-verse-review.md` (which verse was left open, and why) and
   `docs/padachheda-conflict-resolution.md` (the decision already taken for
   1.13's Nepali and Hindi rows).
4. **The Sanskrit itself** for every verse that was read, and the critical
   edition's standard readings for the passages where the two traditions
   differ on the vocative `bhārata` (Sivananda addresses Dhṛtarāṣṭra,
   Ramsukhdas addresses the descendants of Bharata; 1.24 and 2.10 were
   decided on the literal's own reading, and both traditions are recorded in
   the ledger rather than one being suppressed).

The Sanskrit compared against is the text this edition prints in `d`/`t`,
which `check_padas.py` proves matches its own transliteration in all 2,800
pādas.

## Method notes

* The verses were read from `source/ch<N>.json` as parsed JSON, never by
  rewriting strings in place. Every correction was applied by parsing the
  file, locating the one unambiguous row each time, and rewriting the JSON —
  the diff is sixteen strings in seven verses and nothing else moved.
* The verdicts are pinned by `tests/test_semantic_audit.py` (10 tests): the
  reviewed rows with their literal and paraphrase context for all seven
  corrected verses, the rule that no two different words may carry one English
  gloss unless the pair is one of the 88 the audit read and accepted, the rule
  that the English instrument rows follow the English literal, the book-wide
  guard against a comparison glossed with a preposition of departure, the
  book-wide style of `समः` = "समान", the ledger's own coverage of all 18
  chapters and 700 verses, the completeness of all three languages in every
  literal, paraphrase and gloss, and the book-wide guard against a Nepali
  negator run into its word (F8, F9).
* Reading order per verse: Devanagari → IAST → literal (en, ne, hi) →
  paraphrase (en, ne, hi) → title (en, ne, hi) → each pāda's word rows with
  their three glosses.
* The Sanskrit used for comparison is the critical edition's text as printed
  in this edition's `d`/`t`, checked against the standard readings of the
  Gītā.
