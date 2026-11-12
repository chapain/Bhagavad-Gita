# Title and description advisories — review worksheet

Snapshot of 2026-11-12, from `python3 source/audit_titles.py --markdown`. Re-run it after
any change to `source/ch*.json`; this file is a worklist, not site content.

**An advisory is a candidate for review, not a finding of error.** Sanskrit
drops pronouns freely and a title may legitimately summarise rather than
restate. The one class that *fails* the build is possessive inversion
(the 1.10 defect: “Their force is shielded by Bhīṣma” when the Sanskrit says
*ours* is) — that is blocking, and it is not in this list.

Each item shows what the verse actually says, so the decision can be made
without opening the app. Triage labels are mechanical:

* **first person** — the verse is spoken by that person, so naming the
  speaker in a summary is correct (Kṛṣṇa speaks in the first person for most
  of the book; Duryodhana in 1.1–1.11). Skim these.

* **lists the things, never the number** — “The three qualities” for sattva,
  rajas and tamas. Count the items in the verse; the title is usually right.

* **theme summary / read by hand** — the ones worth real attention.

---

## The worksheet — 700 titles, one row each

Every verse title in the edition, chapter by chapter, with the verse's own
English literal beside it. **Tick one of the last three columns per row.**
A ⚑ in the first column means that verse has an advisory — its row already
carries the evidence, so the ticker does not need to open anything else; the
reason it was flagged is noted under each chapter. No ⚑ means no mechanical
doubt was found, which is not the same as a good title — that is what the
read-through is for.

This table is generated, so do not edit it by hand: it prints blank boxes
again on the next run. Ticks are working notes, not a change to a title, and
nothing here writes to `source/ch*.json`. Keep the boxes in a copy if you
want them to survive a regeneration.

### Chapter 1 — Arjuna Viṣāda Yoga · verses 1.01–1.47 · 47 titles, 3 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 1.01 | Dhṛtarāṣṭra asks what they did | Dhṛtarāṣṭra said: On the field of dharma, the field of the Kurus, assembled and eager for battle — my people and the sons of Pāṇḍu — what did they do, O Sañjaya? | ☐ | ☐ | ☐ |
|  | 1.02 | Duryodhana approaches Droṇa | Sañjaya said: Seeing the Pāṇḍava army drawn up in battle-array, Duryodhana then approached his teacher, and the king spoke these words. | ☐ | ☐ | ☐ |
|  | 1.03 | Behold the Pāṇḍava army | Behold, O teacher, this great army of the sons of Pāṇḍu, arrayed for battle by the son of Drupada, your wise disciple. | ☐ | ☐ | ☐ |
|  | 1.04 | Heroes and master bowmen | Here are heroes, great archers, equals of Bhīma and Arjuna in war: Yuyudhāna, Virāṭa, and Drupada, the great chariot-warrior. | ☐ | ☐ | ☐ |
|  | 1.05 | More Pāṇḍava champions | And Dhṛṣṭaketu, Cekitāna, the valiant king of Kāśi, Purujit, Kuntibhoja, and Śaibya, the bull among men. | ☐ | ☐ | ☐ |
|  | 1.06 | Abhimanyu and the warriors | The mighty Yudhāmanyu and the valiant Uttamaujas, the son of Subhadrā, and the sons of Draupadī — all great chariot-warriors. | ☐ | ☐ | ☐ |
| ⚑ | 1.07 | Duryodhana names his own commanders | But know, O best of the twice-born, those who are distinguished among us — the leaders of my army; I name them to you for your information. | ☐ | ☐ | ☐ |
|  | 1.08 | Bhīṣma, Karṇa, Kṛpa, Aśvatthāmā and others | You yourself, Bhīṣma, Karṇa, Kṛpa the conqueror in battle, Aśvatthāmā, Vikarṇa, and the son of Somadatta as well. | ☐ | ☐ | ☐ |
| ⚑ | 1.09 | Warriors ready to die for Duryodhana | And many other heroes, ready to give up their lives for my sake, armed with various weapons, all skilled in war. | ☐ | ☐ | ☐ |
|  | 1.10 | Bhīṣma guards our army; Bhīma guards theirs | Insufficient is that strength of ours, guarded by Bhīṣma; sufficient is this strength of theirs, guarded by Bhīma. | ☐ | ☐ | ☐ |
|  | 1.11 | Protect Bhīṣma above all | Stationed at all the approaches, take your places in your divisions — and above all, protect Bhīṣma alone, all of you. | ☐ | ☐ | ☐ |
|  | 1.12 | Bhīṣma roars and blows his conch | To gladden him, the grandsire of the Kurus, the glorious Bhīṣma, roared a lion's roar and blew his conch loudly. | ☐ | ☐ | ☐ |
|  | 1.13 | Conches, drums and horns together | Then conches, drums, kettledrums, tabors and horns were suddenly struck together — that sound became tumultuous. | ☐ | ☐ | ☐ |
|  | 1.14 | Kṛṣṇa and Arjuna sound their conches | Then, standing in a great chariot yoked with white horses, Mādhava and the son of Pāṇḍu blew their divine conches. | ☐ | ☐ | ☐ |
| ⚑ | 1.15 | Three conches: Pāñcajanya, Devadatta, Pauṇḍra | Hṛṣīkeśa blew Pāñcajanya; Dhanañjaya blew Devadatta; and Bhīma, the doer of herculean deeds, blew the great conch Pauṇḍra. | ☐ | ☐ | ☐ |
|  | 1.16 | Yudhiṣṭhira, Nakula and Sahadeva sound their conches | King Yudhiṣṭhira, son of Kuntī, blew Anantavijaya; Nakula and Sahadeva blew Sughoṣa and Maṇipuṣpaka. | ☐ | ☐ | ☐ |
|  | 1.17 | Kāśī’s king, Śikhaṇḍī and other heroes | And the king of Kāśī, the supreme archer, Śikhaṇḍī the great chariot-warrior, Dhṛṣṭadyumna, Virāṭa, and the unconquered Sātyaki. | ☐ | ☐ | ☐ |
|  | 1.18 | Drupada, Draupadī’s sons, and Abhimanyu sound theirs | Drupada and the sons of Draupadī, O lord of the earth, and the mighty-armed son of Subhadrā — all blew their conches, each his own. | ☐ | ☐ | ☐ |
|  | 1.19 | The uproar shatters Kaurava hearts | That uproar shattered the hearts of the sons of Dhṛtarāṣṭra, resounding tumultuously through the sky and the earth. | ☐ | ☐ | ☐ |
|  | 1.20 | Arjuna raises his bow as battle nears | Then, seeing the Dhārtarāṣṭras stationed in array, as the clash of weapons was about to begin, the Pāṇḍava, whose banner bore the ape, raised his bow. | ☐ | ☐ | ☐ |
|  | 1.21 | Place my chariot between the armies | O lord of the earth, he then spoke this word to Hṛṣīkeśa: “Place my chariot between the two armies, O Acyuta.” | ☐ | ☐ | ☐ |
|  | 1.22 | Let me see whom I must fight | “So that I may see those standing here eager for battle — with whom I must contend in this great enterprise of war.” | ☐ | ☐ | ☐ |
|  | 1.23 | Those who came to please Duryodhana | “I wish to see those who are to fight, who have gathered here — desiring to please the evil-minded son of Dhṛtarāṣṭra in battle.” | ☐ | ☐ | ☐ |
|  | 1.24 | Kṛṣṇa places the chariot between the armies | Sañjaya said: Thus addressed by Guḍākeśa, Hṛṣīkeśa, O descendant of Bharata, placed that best of chariots between the two armies. | ☐ | ☐ | ☐ |
|  | 1.25 | Behold the assembled Kurus | Before Bhīṣma, Droṇa, and all the rulers of the earth, he said: “O Pārtha, behold these Kurus assembled here.” | ☐ | ☐ | ☐ |
|  | 1.26 | Arjuna sees teachers and relatives | There Arjuna saw stationed: fathers, grandfathers, teachers, maternal uncles, brothers, sons, grandsons, and friends as well. | ☐ | ☐ | ☐ |
|  | 1.27 | Kinsmen and friends stand on both sides | Fathers-in-law and well-wishers in both armies — seeing all these kinsmen stationed there, the son of Kuntī… | ☐ | ☐ | ☐ |
|  | 1.28 | My own kin stand ready to fight | Overwhelmed with profound compassion and grieving, he spoke — Arjuna said: “Seeing these my own people, O Kṛṣṇa, standing here eager for battle…” | ☐ | ☐ | ☐ |
|  | 1.29 | My limbs fail | “My limbs fail, my mouth dries up, trembling runs through my body, and my hair stands on end.” | ☐ | ☐ | ☐ |
|  | 1.30 | The Gāṇḍīva slips from my hand | “The Gāṇḍīva slips from my hand, my skin burns; I cannot stand still, and my mind reels.” | ☐ | ☐ | ☐ |
|  | 1.31 | No good comes from killing one's kin | “And I see inauspicious omens, O Keśava; nor do I see any good in killing my own kinsmen in battle.” | ☐ | ☐ | ☐ |
|  | 1.32 | Of what use is a kingdom? | “I do not desire victory, O Kṛṣṇa, nor kingdom nor pleasures. Of what use is a kingdom to us, O Govinda — what use are enjoyments, or even life?” | ☐ | ☐ | ☐ |
|  | 1.33 | Those he sought a kingdom for stand in battle | “Those for whose sake we desired kingdom, enjoyments and pleasures — they stand here in battle, having given up their lives and wealth.” | ☐ | ☐ | ☐ |
|  | 1.34 | Teachers, fathers, sons | “Teachers, fathers, sons, and likewise grandfathers, maternal uncles, fathers-in-law, grandsons, brothers-in-law and other relatives.” | ☐ | ☐ | ☐ |
|  | 1.35 | Not even for the three worlds | “I do not wish to kill them, even if they kill me, O Madhusūdana — not even for the sovereignty of the three worlds, let alone for the sake of this earth.” | ☐ | ☐ | ☐ |
|  | 1.36 | Only sin would follow | “Slaying the sons of Dhṛtarāṣṭra, what pleasure would be ours, O Janārdana? Sin alone would take hold of us for killing these aggressors.” | ☐ | ☐ | ☐ |
|  | 1.37 | We should not kill our own kin | “Therefore we should not kill our kinsmen, the sons of Dhṛtarāṣṭra; for how, having slain our own people, could we be happy, O Mādhava?” | ☐ | ☐ | ☐ |
|  | 1.38 | Greed blinds them to the crime | “Though these men, their minds overcome by greed, see no fault in destroying the family and no crime in treachery toward friends…” | ☐ | ☐ | ☐ |
|  | 1.39 | Seeing family ruin, turn away from sin | “But how can we not know — we who see the fault of family-destruction — that we must turn back from this sin, O Janārdana?” | ☐ | ☐ | ☐ |
|  | 1.40 | When dharma is lost | “With the destruction of the family, the eternal family-duties are lost; and when dharma is lost, adharma overwhelms the whole family.” | ☐ | ☐ | ☐ |
|  | 1.41 | Adharma leads to varṇa mixing | “From the rise of adharma, O Kṛṣṇa, the women of the family become corrupted; and from corrupted women, O Vārṣṇeya, arises the mixing of classes.” | ☐ | ☐ | ☐ |
|  | 1.42 | Hell for the family and its ancestors | “This mixing leads to hell for the destroyers of the family and for the family itself; their ancestors fall, deprived of the offerings of rice and water.” | ☐ | ☐ | ☐ |
|  | 1.43 | Family and social duties are destroyed | “By these faults of the family-destroyers, which cause the mixing of classes, the eternal duties of the community and the family are destroyed.” | ☐ | ☐ | ☐ |
|  | 1.44 | Lost family dharma leads to hell | “For men whose family-duties are destroyed, O Janārdana, there is said to be a certain abode in hell — thus have we heard.” | ☐ | ☐ | ☐ |
|  | 1.45 | Alas, what a great sin | “Alas! What a great sin we have resolved to commit — driven by greed for kingdom and pleasure, we are ready to kill our own kin.” | ☐ | ☐ | ☐ |
|  | 1.46 | Better to be killed unarmed and unresisting | “If the sons of Dhṛtarāṣṭra, weapons in hand, should kill me in battle — me unarmed and unresisting — that would be better for me.” | ☐ | ☐ | ☐ |
|  | 1.47 | Arjuna sits down, setting aside his bow and arrows | Sañjaya said: Having spoken thus on the battlefield, Arjuna sat down on the seat of the chariot, casting aside his bow and arrows, his mind overwhelmed with grief. | ☐ | ☐ | ☐ |

* ⚑ **1.07** — name not in verse. Advisory text: “Duryodhana names his own commanders”
* ⚑ **1.09** — name not in verse. Advisory text: “Warriors ready to die for Duryodhana”
* ⚑ **1.15** — number unsupported. Advisory text: “Three conches: Pāñcajanya, Devadatta, Pauṇḍra”


### Chapter 2 — Sāṅkhya Yoga · verses 2.01–2.72 · 72 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 2.01 | Seeing Arjuna in tears | Sañjaya said: Seeing him thus overcome with pity, his eyes filled with tears and agitation — the sorrowing Arjuna — Madhusūdana spoke these words. | ☐ | ☐ | ☐ |
|  | 2.02 | Where has this weakness come from? | The Blessed Lord said: Whence has come upon you, in this hour of peril, this dejection — unworthy of an Āryan, closing the door of heaven, and bringing disgrace, O Arjuna? | ☐ | ☐ | ☐ |
|  | 2.03 | Cast off this faintness and arise | Yield not to unmanliness, O Pārtha — it does not become you. Cast off this petty faintness of heart and arise, O scorcher of foes! | ☐ | ☐ | ☐ |
|  | 2.04 | How can I strike Bhīṣma and Droṇa? | Arjuna said: How shall I strike Bhīṣma and Droṇa in battle with my arrows, O Madhusūdana — they who are worthy of worship, O slayer of foes? | ☐ | ☐ | ☐ |
|  | 2.05 | Better to beg than kill revered teachers | Better to eat alms-food even here in this world than to slay these noble, great-souled teachers. Killing these very teachers — even for the sake of wealth and desires — I would taste pleasures … | ☐ | ☐ | ☐ |
|  | 2.06 | Victory or defeat—which is better? | Nor do we know which is better for us — to conquer them or be conquered. The very sons of Dhṛtarāṣṭra stand before us; killing them, we should not care to live. | ☐ | ☐ | ☐ |
|  | 2.07 | Teach me, I am your disciple | My nature is overcome by weak compassion; my mind is confused about duty. I ask you: tell me for certain what is good — I am your disciple; teach me, I have taken refuge in you. | ☐ | ☐ | ☐ |
|  | 2.08 | This grief no kingdom could drive away | I do not see what could drive away this grief that dries up my senses — even if I won an unrivaled kingdom on earth or lordship over the gods. | ☐ | ☐ | ☐ |
|  | 2.09 | I will not fight, he said | Sañjaya said: O scorcher of foes, having spoken thus to Hṛṣīkeśa, Arjuna said to Govinda, 'I will not fight' — and fell silent. | ☐ | ☐ | ☐ |
|  | 2.10 | Kṛṣṇa speaks as if smiling | To him, as he grieved between the two armies, Hṛṣīkeśa, as if smiling, spoke these words, O descendant of Bharata. | ☐ | ☐ | ☐ |
|  | 2.11 | You grieve where no grief is due | The Blessed Lord said: You grieve for those who should not be grieved for, yet speak words of wisdom. The wise grieve neither for the living nor for the dead. | ☐ | ☐ | ☐ |
|  | 2.12 | Neither we nor these kings cease to exist | Never was there a time I did not exist, nor you, nor these rulers of men; nor will any of us ever cease to be hereafter. | ☐ | ☐ | ☐ |
|  | 2.13 | Childhood, youth, old age | As the embodied soul passes in this body through childhood, youth and old age, so it passes into another body; the wise are not deluded by this. | ☐ | ☐ | ☐ |
|  | 2.14 | Cold and heat come and go | The contacts of the senses with their objects, O son of Kuntī, give cold and heat, pleasure and pain; they come and go, impermanent — endure them, O Bhārata. | ☐ | ☐ | ☐ |
|  | 2.15 | The steady one is fit for immortality | The man whom these cannot disturb, O bull among men — the wise one who is equal in pleasure and pain — he is fit for immortality. | ☐ | ☐ | ☐ |
|  | 2.16 | The unreal has no being | The unreal has no being; the real never ceases to be. The truth of both is seen by the seers of the essence. | ☐ | ☐ | ☐ |
|  | 2.17 | The imperishable pervades all | Know that to be imperishable by which all this is pervaded. No one can bring about the destruction of that inexhaustible one. | ☐ | ☐ | ☐ |
|  | 2.18 | The bodies end, the Self does not | These bodies of the eternal, indestructible, immeasurable embodied Self are said to have an end; therefore fight, O Bhārata. | ☐ | ☐ | ☐ |
|  | 2.19 | The Self neither kills nor is killed | Whoever thinks the Self is the killer, and whoever thinks it is killed — neither truly knows: it does not kill, nor is it killed. | ☐ | ☐ | ☐ |
|  | 2.20 | The Self is never born and never dies | It is never born, never dies; having been, it will never again cease to be. Unborn, eternal, everlasting and ancient — it is not slain when the body is slain. | ☐ | ☐ | ☐ |
|  | 2.21 | Who then can kill, or cause killing? | Knowing this Self to be imperishable, eternal, unborn and inexhaustible — how, O Pārtha, can any man cause another to be killed, or kill? | ☐ | ☐ | ☐ |
|  | 2.22 | As one casts off worn-out clothes | As a man casts off worn-out clothes and puts on new ones, so the embodied Self casts off worn-out bodies and enters new ones. | ☐ | ☐ | ☐ |
|  | 2.23 | No weapon cuts the Self | Weapons do not cut it, fire does not burn it, water does not wet it, wind does not dry it. | ☐ | ☐ | ☐ |
|  | 2.24 | The Self is eternal and unmoving | It cannot be cut, burned, wetted, or dried. Eternal, all-pervading, fixed, immovable, and everlasting is it. | ☐ | ☐ | ☐ |
|  | 2.25 | The Self is unmanifest and unchanging | It is said to be unmanifest, unthinkable, and unchanging. Knowing it thus, you have no cause to grieve. | ☐ | ☐ | ☐ |
|  | 2.26 | Even with birth and death, do not grieve | But even if you think the Self is perpetually born and perpetually dies, O mighty-armed one, even then you should not grieve. | ☐ | ☐ | ☐ |
|  | 2.27 | Birth and death are certain | For death is certain for the born, and birth is certain for the dead. Therefore, in an unavoidable matter, you should not grieve. | ☐ | ☐ | ☐ |
|  | 2.28 | Unmanifest beginning and end | All beings are unmanifest in their beginning, manifest in their middle, and unmanifest again in their end. What is there to lament, O Bhārata? | ☐ | ☐ | ☐ |
|  | 2.29 | The Self is wondrous, yet hard to know | One sees the Self as a wonder, another speaks of it as a wonder, another hears of it as a wonder — and even having heard, no one truly knows it. | ☐ | ☐ | ☐ |
|  | 2.30 | Grieve for no being | The embodied Self in the body of everyone is eternally inviolable, O Bhārata. Therefore you should not grieve for any being. | ☐ | ☐ | ☐ |
|  | 2.31 | Nothing better than a righteous war | Considering also your own dharma, you should not waver; for a kṣatriya, nothing is better than a righteous war. | ☐ | ☐ | ☐ |
|  | 2.32 | An open gate to heaven | Blessed are the kṣatriyas, O Pārtha, who find such a war — come to them of its own accord — an open door to heaven. | ☐ | ☐ | ☐ |
|  | 2.33 | Abandoning dharma you incur sin | But if you do not wage this righteous war, then, abandoning your own dharma and your glory, you will incur sin. | ☐ | ☐ | ☐ |
|  | 2.34 | Your lasting shame | People will speak of your everlasting disgrace; and for one held in honour, disgrace is worse than death. | ☐ | ☐ | ☐ |
|  | 2.35 | Warriors will mistake retreat for fear | The great warriors will think you fled the battle out of fear; and those who held you in high regard will think little of you. | ☐ | ☐ | ☐ |
|  | 2.36 | Enemies will mock your strength | Your enemies will speak many unutterable words, slandering your strength. What could be more painful than that? | ☐ | ☐ | ☐ |
|  | 2.37 | Slain, you win heaven | Slain, you will win heaven; victorious, you will enjoy the earth. Therefore arise, O son of Kuntī, resolved to fight. | ☐ | ☐ | ☐ |
|  | 2.38 | Make pleasure and pain the same | Making pleasure and pain, gain and loss, victory and defeat the same, then fight — and you will incur no sin. | ☐ | ☐ | ☐ |
|  | 2.39 | Now hear the wisdom of yoga | This wisdom of sāṅkhya has been declared to you, O Pārtha. Now hear the wisdom of yoga; joined with it, you will cast off the bondage of karma. | ☐ | ☐ | ☐ |
|  | 2.40 | No effort is ever lost | Here there is no loss of effort, nor any contrary result. Even a little of this dharma protects one from great fear. | ☐ | ☐ | ☐ |
|  | 2.41 | A resolute intellect has one aim | The intellect of the resolute is single and one-pointed here, O joy of the Kurus; but the intellects of the irresolute branch out endlessly. | ☐ | ☐ | ☐ |
|  | 2.42 | The flowery words of the Vedas | The unwise, delighting in the flowery words of the Vedas, declare that there is nothing else — addicted to ritual and enjoyment, O Pārtha. | ☐ | ☐ | ☐ |
|  | 2.43 | Full of craving, longing for heaven | Desire-filled, heaven-seeking, they promise birth and karma as their fruit, and preach many special rites for the sake of pleasure and power. | ☐ | ☐ | ☐ |
|  | 2.44 | No samādhi for the scattered | For those attached to pleasure and power, whose minds are carried away by such words, the one-pointed intellect of samādhi does not arise. | ☐ | ☐ | ☐ |
|  | 2.45 | Rise above the three guṇas | The Vedas deal with the three guṇas; rise above the three guṇas, O Arjuna — free from the pairs of opposites, ever established in sattva, beyond gain and keeping, self-possessed. | ☐ | ☐ | ☐ |
|  | 2.46 | The well and the flood | As much use as a well is when water floods everywhere, so much is all the Veda for a brāhmaṇa of understanding. | ☐ | ☐ | ☐ |
|  | 2.47 | Your right: action, not fruit; don’t cling to inaction | Your right is to action alone, never to its fruits. Let not the fruits of action be your motive, nor let your attachment be to inaction. | ☐ | ☐ | ☐ |
|  | 2.48 | Evenness is called yoga | Established in yoga, perform your actions, casting off attachment, O Dhanañjaya; equal in success and failure — this evenness is called yoga. | ☐ | ☐ | ☐ |
|  | 2.49 | Action is far inferior to buddhi-yoga | Action is far inferior to the yoga of discernment, O Dhanañjaya. Seek refuge in the intellect; pitiful are those who act for results. | ☐ | ☐ | ☐ |
|  | 2.50 | Yoga is skill in action | One joined to the intellect leaves behind here both good deeds and bad. Therefore devote yourself to yoga — yoga is skill in action. | ☐ | ☐ | ☐ |
|  | 2.51 | Freed from the bonds of birth | The wise, united with the intellect and renouncing the fruits of their actions, are freed from the bonds of birth and reach the place beyond all ill. | ☐ | ☐ | ☐ |
|  | 2.52 | Beyond the mire of delusion | When your intellect crosses beyond the mire of delusion, you will grow indifferent to what has been heard and what is yet to be heard. | ☐ | ☐ | ☐ |
|  | 2.53 | The intellect stands firm in samādhi | When your intellect, bewildered by the scriptures, stands firm and unmoved in samādhi, then you will attain yoga. | ☐ | ☐ | ☐ |
|  | 2.54 | Arjuna asks the marks of steady wisdom | Arjuna said: What is the description of the man of steady wisdom, established in samādhi, O Keśava? How does the steady-minded one speak, how sit, how move? | ☐ | ☐ | ☐ |
|  | 2.55 | Content in the Self alone | The Blessed Lord said: When one casts off all desires of the mind, O Pārtha, and is content in the Self alone through the Self — then one is called steady in wisdom. | ☐ | ☐ | ☐ |
|  | 2.56 | The muni of steady wisdom | One whose mind is untroubled in sorrow and free from longing in joy, from whom passion, fear and anger have departed — that one is the steady-minded sage. | ☐ | ☐ | ☐ |
|  | 2.57 | Neither rejoicing nor recoiling | One who is without affection everywhere, who neither rejoices nor recoils on meeting good or evil — that one's wisdom is firmly set. | ☐ | ☐ | ☐ |
|  | 2.58 | Like a tortoise drawing in its limbs | When, like a tortoise drawing in its limbs from all sides, one withdraws the senses from their objects — that one's wisdom is firmly set. | ☐ | ☐ | ☐ |
|  | 2.59 | Craving ends when the Supreme is seen | The objects fall away from the self-controlled one, but the taste for them remains; and when the Supreme is seen, even that taste departs. | ☐ | ☐ | ☐ |
|  | 2.60 | The mind following the senses loses its wisdom | Even for the striving sage, O son of Kuntī, the turbulent senses forcibly carry away the mind. | ☐ | ☐ | ☐ |
|  | 2.61 | Reining in the senses | Having restrained them all, the disciplined one should sit intent on Me; for one whose senses are under control, wisdom is firmly set. | ☐ | ☐ | ☐ |
|  | 2.62 | Brooding breeds desire, desire breeds anger | Brooding on sense objects breeds attachment to them; from attachment arises desire; from desire arises anger. | ☐ | ☐ | ☐ |
|  | 2.63 | Anger brings delusion and ruin | From anger comes delusion; from delusion, confusion of memory; from broken memory, the ruin of understanding; and from that ruin, one is destroyed. | ☐ | ☐ | ☐ |
|  | 2.64 | The self-controlled attain serenity | But one who moves among objects with the senses mastered, free from attraction and aversion, self-controlled — that one attains serenity. | ☐ | ☐ | ☐ |
|  | 2.65 | In peace, all suffering ends | In serenity, all sorrows cease for that one; for the mind of the serene is quickly established in steadiness. | ☐ | ☐ | ☐ |
|  | 2.66 | No peace, no happiness | There is no wisdom for the undisciplined, no meditation for the unsteady; and without meditation there is no peace — how can there be happiness without peace? | ☐ | ☐ | ☐ |
|  | 2.67 | As wind carries a boat | For the mind that follows the wandering senses carries away the understanding, as the wind carries a boat on the waters. | ☐ | ☐ | ☐ |
|  | 2.68 | The senses fully drawn back | Therefore, O mighty-armed one, one whose senses are wholly withdrawn from their objects — that one's wisdom is firmly set. | ☐ | ☐ | ☐ |
|  | 2.69 | Night for all beings | What is night for all beings is the waking time for the disciplined sage; what is waking for beings is night for the sage who sees. | ☐ | ☐ | ☐ |
|  | 2.70 | As waters enter the ocean | As the waters enter the ocean, which remains unmoved though filled from every side, so the sage whom all desires enter remains at peace — not the one who lusts for desires. | ☐ | ☐ | ☐ |
|  | 2.71 | Without longing, without ego | The man who casts off all desires and moves without longing, without possessiveness, without ego — that one attains peace. | ☐ | ☐ | ☐ |
|  | 2.72 | The Brāhmī state ends delusion | This is the Brāhmī state, O Pārtha; attaining it, one is no longer deluded. Resting in it even at the end, one reaches Brahman-nirvāṇa. | ☐ | ☐ | ☐ |


### Chapter 3 — Karma Yoga · verses 3.01–3.43 · 43 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 3.01 | Why engage me in this dreadful action? | Arjuna said: If, O Janārdana, wisdom is considered by you to be superior to action, then why, O Keśava, do you engage me in this dreadful action? | ☐ | ☐ | ☐ |
|  | 3.02 | Tell me one thing decisively | With words that appear equivocal you seem to confuse my intellect. Tell me one thing decisively, by which I may attain the good. | ☐ | ☐ | ☐ |
|  | 3.03 | Knowledge for some, action for others | The Blessed Lord said: In this world a twofold path of steadfastness was declared by me of old, O sinless one: the yoga of knowledge for the Sāṅkhyas, and the yoga of action for the yogis. | ☐ | ☐ | ☐ |
|  | 3.04 | Not by abstaining | Not by the non-performance of actions does one attain freedom from action, nor by mere renunciation alone does one reach perfection. | ☐ | ☐ | ☐ |
|  | 3.05 | No one can sit idle | Indeed no one ever remains actionless even for a moment; everyone is made to act, helpless, by the guṇas born of prakṛti. | ☐ | ☐ | ☐ |
|  | 3.06 | Organs of action restrained, mind on sense-objects | He who, restraining the organs of action, sits recollecting sense objects in his mind — that deluded one is called a hypocrite. | ☐ | ☐ | ☐ |
|  | 3.07 | He who acts unattached excels | But he who, O Arjuna, controlling the senses by the mind, undertakes karma-yoga with the organs of action, unattached — he excels. | ☐ | ☐ | ☐ |
|  | 3.08 | Do the allotted duty | Perform your prescribed action, for action is superior to inaction; even the maintenance of the body would not be accomplished by inaction. | ☐ | ☐ | ☐ |
|  | 3.09 | Act for sacrifice alone | The world is bound by action, except action performed for the sake of sacrifice; for that purpose, O son of Kuntī, perform action free from attachment. | ☐ | ☐ | ☐ |
|  | 3.10 | Prajāpati made beings with sacrifice | Having created creatures together with sacrifice from the beginning, Prajāpati declared: “By this shall you prosper; may this be to you the cow of desires.” | ☐ | ☐ | ☐ |
|  | 3.11 | Nourish one another to attain the highest good | With this nourish the gods, and may the gods nourish you; nourishing one another, you shall attain the highest good. | ☐ | ☐ | ☐ |
|  | 3.12 | He who enjoys without giving is a thief | Nourished by sacrifice, the gods will give you the joys you desire; he who enjoys what they have given without offering back to them is verily a thief. | ☐ | ☐ | ☐ |
|  | 3.13 | Sacrificial remnants free one from sin | The good who eat the remnants of sacrifice are released from all sins; but the wicked who cook for their own sake verily eat sin. | ☐ | ☐ | ☐ |
|  | 3.14 | From food, from rain, from sacrifice | Beings arise from food; food arises from rain; rain arises from sacrifice; sacrifice arises from action. | ☐ | ☐ | ☐ |
|  | 3.15 | Action arises from Brahman | Know that action arises from Brahman, and Brahman from the Imperishable; therefore the all-pervading Brahman is ever established in sacrifice. | ☐ | ☐ | ☐ |
|  | 3.16 | Who does not follow the wheel lives in vain | He who does not follow here this wheel thus set in motion, whose life is sin, delighting in the senses — lives in vain, O Pārtha. | ☐ | ☐ | ☐ |
|  | 3.17 | For him there is nothing left to do | But the man who rejoices only in the Self, is gratified with the Self, and is content in the Self alone — for him there is nothing to do. | ☐ | ☐ | ☐ |
|  | 3.18 | Nothing to gain or lose | For him there is no purpose in what has been done or not done, nor does he depend on any being for any purpose. | ☐ | ☐ | ☐ |
|  | 3.19 | Therefore act, unattached | Therefore, always perform the action that is your duty, unattached; for performing action without attachment, a man attains the Supreme. | ☐ | ☐ | ☐ |
|  | 3.20 | Janaka attained perfection by action | Indeed by action alone did Janaka and others attain perfection; even having regard for the welfare of the world, you should act. | ☐ | ☐ | ☐ |
|  | 3.21 | As the great one does, so do others | Whatever the best person does, that indeed the common person does; whatever he makes the standard, the world follows. | ☐ | ☐ | ☐ |
|  | 3.22 | Nothing I need, yet I act | For me, O Pārtha, there is nothing to be done in the three worlds, nothing unattained to be attained — yet I continue to act. | ☐ | ☐ | ☐ |
|  | 3.23 | All would follow my example | If I did not engage in action ever, untiringly, then people would follow my path in all respects, O Pārtha. | ☐ | ☐ | ☐ |
|  | 3.24 | These worlds would perish | These worlds would perish if I did not perform action; I would be the maker of chaos and would destroy these creatures. | ☐ | ☐ | ☐ |
|  | 3.25 | Act as the unwise do—but without attachment | As the unwise act, attached to action, O Bhārata, so should the wise act, unattached, desiring the welfare of the world. | ☐ | ☐ | ☐ |
|  | 3.26 | Do not unsettle the ignorant | Let him not create disturbance in the minds of the ignorant who are attached to action; acting himself with devotion, let him make them do all actions. | ☐ | ☐ | ☐ |
|  | 3.27 | The guṇas are the doers | All actions are performed by the guṇas of prakṛti in every way; the one deluded by egoism thinks, “I am the doer.” | ☐ | ☐ | ☐ |
|  | 3.28 | Qualities act on qualities | But the knower of truth, O mighty-armed, knowing the distinction of the guṇas and actions, and that the guṇas move among the guṇas, does not become attached. | ☐ | ☐ | ☐ |
|  | 3.29 | Let the knower not disturb them | Those deluded by the guṇas of prakṛti cling to actions born of the guṇas; the one of complete knowledge should not unsettle the dull-witted, partial knowers. | ☐ | ☐ | ☐ |
|  | 3.30 | Renouncing all actions in me, fight | Renouncing all actions in me, with the mind fixed on the Self, being free from desire and from possessiveness, fight — free from fever. | ☐ | ☐ | ☐ |
|  | 3.31 | Those who follow it are freed | Those men who always follow this teaching of mine with faith, without finding fault, are released even from the bondage of action. | ☐ | ☐ | ☐ |
|  | 3.32 | Those who find fault and do not follow are lost | But those who, finding fault, do not follow this teaching of mine — know them as deprived of all wisdom, ruined, and without understanding. | ☐ | ☐ | ☐ |
|  | 3.33 | Even the wise follow their nature | Even a man of knowledge acts according to his own nature; beings follow their nature — what will restraint accomplish? | ☐ | ☐ | ☐ |
|  | 3.34 | Attraction and aversion lie in wait | Attachment and aversion are fixed regarding the object of each sense; let one not come under their power, for they are one's waylayers. | ☐ | ☐ | ☐ |
|  | 3.35 | Better one's own dharma, though flawed | Better is one's own dharma, though defective, than another's well-performed; death in one's own dharma is better — another's dharma brings fear. | ☐ | ☐ | ☐ |
|  | 3.36 | Arjuna asks what drives a man to sin | Arjuna said: Then, impelled by what, O Vārṣṇeya, does a man commit evil, even against his will, as though forced by power? | ☐ | ☐ | ☐ |
|  | 3.37 | Desire and anger, the all-consuming enemy | The Blessed Lord said: It is desire, it is anger, born of the rajo-guṇa; all-devouring, greatly sinful — know this as the enemy here. | ☐ | ☐ | ☐ |
|  | 3.38 | Smoke, dust, and the embryo's covering | As fire is enveloped by smoke, and a mirror by dust, and an embryo by its membrane, so is this covered by that (desire). | ☐ | ☐ | ☐ |
|  | 3.39 | Desire, insatiable as fire, covers wisdom | Wisdom is covered by this constant enemy of the wise, having the form of desire, which is insatiable, O son of Kuntī, like fire. | ☐ | ☐ | ☐ |
|  | 3.40 | Its seat: senses, mind, intellect | The senses, the mind and the intellect are said to be its seat; covering wisdom by these, it deludes the embodied soul. | ☐ | ☐ | ☐ |
|  | 3.41 | Rein in the senses first | Therefore, O bull of the Bhāratas, first controlling the senses, cast off this sinner, the destroyer of knowledge and discrimination. | ☐ | ☐ | ☐ |
|  | 3.42 | Higher than the intellect is he | They say the senses are higher; higher than the senses is the mind; higher than the mind is the intellect; but higher than the intellect is He (the Self). | ☐ | ☐ | ☐ |
|  | 3.43 | Slay the enemy | Thus knowing Him who is beyond the intellect, restraining the self by the Self, O mighty-armed one, slay the enemy having the form of desire, so difficult to conquer. | ☐ | ☐ | ☐ |


### Chapter 4 — Jñāna-Karma-Sannyāsa Yoga · verses 4.01–4.42 · 42 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 4.01 | Taught to Vivasvān | The Blessed Lord said: I declared this imperishable yoga to Vivasvān; Vivasvān communicated it to Manu; Manu proclaimed it to Ikṣvāku. | ☐ | ☐ | ☐ |
|  | 4.02 | In time this yoga was lost | Thus received in succession, the royal sages came to know it; but in the long course of time, this yoga was lost, O scorcher of foes. | ☐ | ☐ | ☐ |
|  | 4.03 | I declare that ancient yoga to you | This same ancient yoga is now declared to you by me, because you are my devotee and friend — truly, this is the supreme secret. | ☐ | ☐ | ☐ |
|  | 4.04 | Arjuna asks how that can be | Arjuna said: Later is your birth, and earlier the birth of Vivasvān; how then am I to understand that you taught it in the beginning? | ☐ | ☐ | ☐ |
|  | 4.05 | I know all our past births | The Blessed Lord said: Many births of mine have passed, and of yours too, O Arjuna; I know them all, but you do not know them, O scorcher of foes. | ☐ | ☐ | ☐ |
|  | 4.06 | I come into being by my own māyā | Though unborn, though the imperishable Self, though the Lord of beings — resorting to my own prakṛti, I come into being through my own māyā. | ☐ | ☐ | ☐ |
|  | 4.07 | Whenever dharma declines | Whenever, O Bhārata, there is a decline of dharma and a rise of adharma, then I bring myself into being. | ☐ | ☐ | ☐ |
|  | 4.08 | To protect the righteous | For the protection of the good, for the destruction of the evil-doers, for the establishment of dharma, I take birth age after age. | ☐ | ☐ | ☐ |
|  | 4.09 | Knowing this, one is not reborn | He who thus knows in truth my divine birth and action — having abandoned the body, he is not born again; he comes to me, O Arjuna. | ☐ | ☐ | ☐ |
|  | 4.10 | Free from attachment, fear and anger | Free from attachment, fear and anger, filled with me, taking refuge in me, many — purified by the austerity of knowledge — have attained my state. | ☐ | ☐ | ☐ |
|  | 4.11 | As they approach me, so I respond | In whatever way men approach me, in that same way I favour them; people follow my path in every way, O Pārtha. | ☐ | ☐ | ☐ |
|  | 4.12 | Those who want quick fruit worship gods | Those who desire the success of actions worship the gods here; indeed, in this human world success born of action comes quickly. | ☐ | ☐ | ☐ |
|  | 4.13 | The fourfold order was created by me | The fourfold order was created by me according to the distinction of guṇas and actions; though I am its author, know me as the non-doer and imperishable. | ☐ | ☐ | ☐ |
|  | 4.14 | Actions do not taint me | Actions do not stain me, nor have I any longing for the fruit of action; he who knows me thus is not bound by actions. | ☐ | ☐ | ☐ |
|  | 4.15 | The ancients acted so | Knowing this, the ancient seekers of liberation performed action; therefore you too perform action, as was done before by the ancients. | ☐ | ☐ | ☐ |
|  | 4.16 | Even the wise are bewildered here | What is action, what is inaction — even the wise are bewildered here; I shall declare to you that action, knowing which you will be released from evil. | ☐ | ☐ | ☐ |
|  | 4.17 | The mystery of action | Indeed the nature of action must be understood, and of forbidden action too, and of inaction; mysterious is the course of action. | ☐ | ☐ | ☐ |
|  | 4.18 | Inaction in action, action in inaction | He who sees inaction in action, and action in inaction, is intelligent among men; he is engaged in yoga and performs all actions. | ☐ | ☐ | ☐ |
|  | 4.19 | Actions burned in the fire of knowledge | Whose undertakings are all free from desire and resolve, and whose actions are burnt by the fire of knowledge — him the wise call a man of learning. | ☐ | ☐ | ☐ |
|  | 4.20 | Though acting, he does nothing | Having abandoned attachment to the fruit of action, ever content, without any support — though engaged in action, he verily does nothing. | ☐ | ☐ | ☐ |
|  | 4.21 | Owning nothing, he incurs no sin | Free from desire, with the mind and self controlled, having given up all possessions, performing only bodily action, he does not incur sin. | ☐ | ☐ | ☐ |
|  | 4.22 | Content with what comes | Content with what comes unsought, beyond the pairs of opposites, free from envy, equal in success and failure — even acting, he is not bound. | ☐ | ☐ | ☐ |
|  | 4.23 | Actions of the freed one dissolve | The actions of one free from attachment, liberated, whose mind is established in knowledge and who acts for sacrifice — they dissolve entirely. | ☐ | ☐ | ☐ |
|  | 4.24 | Brahman is the ladle, Brahman the oblation | The ladle is Brahman, the oblation is Brahman, offered in the fire of Brahman by Brahman; Brahman alone is reached by him who is absorbed in the action of Brahman. | ☐ | ☐ | ☐ |
|  | 4.25 | Sacrifice to the gods, and into Brahman | Some yogis worship the gods through sacrifice; others offer the sacrifice itself, by sacrifice, into the fire of Brahman. | ☐ | ☐ | ☐ |
|  | 4.26 | Senses offered into the fires of restraint | Some offer hearing and the other senses into the fires of restraint; others offer sound and the other sense-objects into the fires of the senses. | ☐ | ☐ | ☐ |
|  | 4.27 | All action offered in the fire of yoga | And others offer all the activities of the senses and of the vital breaths into the fire of the yoga of self-restraint, kindled by knowledge. | ☐ | ☐ | ☐ |
|  | 4.28 | Sacrifices of wealth, austerity, yoga and study | Others perform the sacrifices of wealth, austerity, yoga, and scriptural study and knowledge — ascetics of firm vows. | ☐ | ☐ | ☐ |
|  | 4.29 | Breath offered to breath | Some offer the up-breath into the down-breath, and the down-breath into the up-breath, checking the courses of the breaths, devoted to breath-control. | ☐ | ☐ | ☐ |
|  | 4.30 | Breath offered into breath, sins consumed | Others, with regulated diet, offer the vital breaths into the vital breaths; all these are knowers of sacrifice, whose sins are consumed by sacrifice. | ☐ | ☐ | ☐ |
|  | 4.31 | Not even this world for the non-sacrificer | Tasting the nectar of the remnant of sacrifice, they reach the eternal Brahman; this world is not for the non-sacrificer, how then the next, O best of the Kurus? | ☐ | ☐ | ☐ |
|  | 4.32 | All sacrifices are born of action | Thus manifold sacrifices are set forth in the mouth of Brahman; know them all as born of action — knowing this, you shall be released. | ☐ | ☐ | ☐ |
|  | 4.33 | Knowledge-sacrifice excels material sacrifice | The sacrifice of knowledge is better than the sacrifice of material things, O scorcher of foes; all action, in its entirety, O Pārtha, culminates in knowledge. | ☐ | ☐ | ☐ |
|  | 4.34 | Approach a teacher, ask, serve | Know that wisdom through prostration, by questioning, and by service; the knowers of truth who have seen reality will instruct you. | ☐ | ☐ | ☐ |
|  | 4.35 | You will see all beings in the Self | Knowing that, O son of Pāṇḍu, you will not again fall under delusion; by it you will see all beings without exception in the Self, and also in me. | ☐ | ☐ | ☐ |
|  | 4.36 | The boat of knowledge | Even if you are the most sinful of all sinners, you shall cross all evil by the boat of knowledge alone. | ☐ | ☐ | ☐ |
|  | 4.37 | The fire of wisdom | As the kindled fire reduces fuel to ashes, O Arjuna, so does the fire of knowledge reduce all actions to ashes. | ☐ | ☐ | ☐ |
|  | 4.38 | Nothing purifies like knowledge | Indeed, nothing here is as purifying as knowledge; one perfected in yoga finds it in the Self in time, of himself. | ☐ | ☐ | ☐ |
|  | 4.39 | The faithful attains knowledge | The faithful man, intent on it, with senses subdued, attains knowledge; and having attained knowledge, he soon reaches supreme peace. | ☐ | ☐ | ☐ |
|  | 4.40 | The doubting soul perishes | But the ignorant man without faith, full of doubt, perishes; for the doubting soul there is neither this world, nor the next, nor happiness. | ☐ | ☐ | ☐ |
|  | 4.41 | Knowledge destroys doubt; actions do not bind | Actions do not bind him who has renounced actions through yoga, whose doubt is destroyed by knowledge, who is self-possessed, O Dhanañjaya. | ☐ | ☐ | ☐ |
|  | 4.42 | Cut the doubt and take your stand | Therefore, cut this doubt about the Self, born of ignorance and dwelling in your heart, with the sword of knowledge; stand firm in yoga — arise, O Bhārata! | ☐ | ☐ | ☐ |


### Chapter 5 — Karma-Sannyāsa Yoga · verses 5.01–5.29 · 29 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 5.01 | Arjuna asks: renounce or act? | Arjuna said: You praise renunciation of actions, O Kṛṣṇa, and also the yoga of action; tell me for certain which one of the two is better. | ☐ | ☐ | ☐ |
|  | 5.02 | Both lead to the good — but yoga excels | The Blessed Lord said: Both renunciation and karma-yoga lead to the supreme good; but of the two, karma-yoga is superior to the renunciation of action. | ☐ | ☐ | ☐ |
|  | 5.03 | He who neither hates nor longs is free | He is to be known as ever-renouncing who neither hates nor longs; free from the pairs of opposites, O mighty-armed one, he is easily released from bondage. | ☐ | ☐ | ☐ |
|  | 5.04 | Only children call sāṅkhya and yoga different | The childish, not the wise, speak of sāṅkhya and yoga as different; one who is rightly established in even one of them attains the fruit of both. | ☐ | ☐ | ☐ |
|  | 5.05 | The same goal | The state attained by the sāṅkhyas is also reached by the yogis; he who sees sāṅkhya and yoga as one — he truly sees. | ☐ | ☐ | ☐ |
|  | 5.06 | Renunciation is hard without yoga | But renunciation, O mighty-armed one, is hard to attain without yoga; the sage endowed with yoga reaches Brahman before long. | ☐ | ☐ | ☐ |
|  | 5.07 | The Self of all beings | Devoted to karma-yoga, of pure soul, self-conquered, senses conquered, the Self of all beings — though acting, he is not stained. | ☐ | ☐ | ☐ |
|  | 5.08 | “I do nothing at all” | “I do nothing at all” — thus should the knower of truth think, while seeing, hearing, touching, smelling, eating, moving, sleeping, breathing, | ☐ | ☐ | ☐ |
|  | 5.09 | The senses among their objects | speaking, giving up, holding, opening and closing the eyes — holding that the senses move among the objects of the senses. | ☐ | ☐ | ☐ |
|  | 5.10 | The lotus leaf | He who acts, offering all actions to Brahman and abandoning attachment, is not stained by sin, just as a lotus leaf is not wetted by water. | ☐ | ☐ | ☐ |
|  | 5.11 | Action for self-purification | The yogis perform action by body, mind, intellect, or even by the senses alone, having abandoned attachment, for the purification of the self. | ☐ | ☐ | ☐ |
|  | 5.12 | Peace through giving up the fruit | The one established in yoga, giving up the fruit of action, attains lasting peace; the one not established, impelled by desire, attached to the fruit, becomes bound. | ☐ | ☐ | ☐ |
|  | 5.13 | The city of nine gates | Having mentally renounced all actions, the self-controlled embodied one dwells happily in the city of nine gates, neither acting nor causing others to act. | ☐ | ☐ | ☐ |
|  | 5.14 | The Lord creates no doership | The Lord neither creates agency nor actions for the world, nor the connection of action with its fruit; it is nature that acts. | ☐ | ☐ | ☐ |
|  | 5.15 | He takes on neither sin nor merit | The all-pervading One neither accepts the sin nor the merit of anyone; knowledge is enveloped by ignorance, and thereby beings are deluded. | ☐ | ☐ | ☐ |
|  | 5.16 | Knowledge reveals like the sun | But for those whose ignorance is destroyed by the knowledge of the Self, that knowledge shines forth like the sun, revealing the Supreme. | ☐ | ☐ | ☐ |
|  | 5.17 | Intellect, self and refuge all in that | With their intellect in that, their self in that, steadfast in that, and that as their highest goal — they reach the state of no return, their sins cleansed by knowledge. | ☐ | ☐ | ☐ |
|  | 5.18 | The sage sees the same in all | The wise look equally on a brāhmaṇa endowed with learning and humility, a cow, an elephant, a dog, and even an outcaste. | ☐ | ☐ | ☐ |
|  | 5.19 | Equanimity conquers the world of birth and death | Here itself the world of birth and death is conquered by those whose minds rest in equanimity; Brahman is flawless and equal; therefore they are established in Brahman. | ☐ | ☐ | ☐ |
|  | 5.20 | He neither rejoices nor is disturbed | He does not rejoice on obtaining what is dear, nor is he perturbed on obtaining what is not dear; with steady intellect, undeluded, the knower of Brahman abides in Brahman. | ☐ | ☐ | ☐ |
|  | 5.21 | The joy within | With the self unattached to external contacts, he finds the happiness that is in the Self; joined with the yoga of Brahman, he enjoys bliss that is imperishable. | ☐ | ☐ | ☐ |
|  | 5.22 | Contact-born pleasures are wombs of pain | Indeed, the pleasures born of contact with the senses are only wombs of sorrow; they have a beginning and an end, O son of Kuntī — the wise do not rejoice in them. | ☐ | ☐ | ☐ |
|  | 5.23 | He who withstands desire and anger | He who, even here, before the release of the body, is able to endure the impulse born of desire and anger — he is yoked in yoga, he is a happy man. | ☐ | ☐ | ☐ |
|  | 5.24 | Whose joy is within | He who is happy within, who delights within, who is illumined within — that yogi, become Brahman, attains to Brahman-nirvāṇa. | ☐ | ☐ | ☐ |
|  | 5.25 | Sages with dispelled doubts reach Brahman-nirvāṇa | The seers whose sins are destroyed, whose doubts are cut, whose selves are controlled, who delight in the welfare of all beings — they attain Brahman-nirvāṇa. | ☐ | ☐ | ☐ |
|  | 5.26 | Free from desire and anger | For the ascetics free from desire and anger, whose thoughts are controlled, who know the Self — Brahman-nirvāṇa is present all around. | ☐ | ☐ | ☐ |
|  | 5.27 | Breath, gaze, and stillness | Turning the sense-objects outward, fixing the vision between the eyebrows, making the out-breath and in-breath flow evenly within the nostrils — | ☐ | ☐ | ☐ |
|  | 5.28 | Free of craving, fear and anger | — with senses, mind and intellect controlled, the sage intent on liberation, free from desire, fear and anger — he is ever free. | ☐ | ☐ | ☐ |
|  | 5.29 | Knowing me, friend of all beings, he attains peace | Knowing me as the enjoyer of sacrifices and austerities, the great Lord of all the worlds, the friend of all beings — he attains peace. | ☐ | ☐ | ☐ |


### Chapter 6 — Dhyāna Yoga · verses 6.01–6.47 · 47 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 6.01 | He who acts without fruit-seeking: renouncer and yogi | The Blessed Lord said: He who performs his bounden action without depending on its fruit — he is both a renouncer and a yogi, not he who is without fire and without rites. | ☐ | ☐ | ☐ |
|  | 6.02 | Renunciation is yoga | That which they call renunciation, know that to be yoga, O son of Pāṇḍu; for none becomes a yogi who has not renounced resolve. | ☐ | ☐ | ☐ |
|  | 6.03 | Action for the ascending, stillness for the ascended | For the sage who wishes to ascend in yoga, action is said to be the means; for him who has ascended, quiescence is said to be the means. | ☐ | ☐ | ☐ |
|  | 6.04 | Clinging to nothing, he has risen in yoga | When one is attached neither to sense-objects nor to actions, having abandoned every resolve — then he is said to have ascended in yoga. | ☐ | ☐ | ☐ |
|  | 6.05 | The Self is the friend and the enemy of the Self | Let one raise the self by the Self and not degrade the self; for the Self alone is the friend of the self, and the Self alone is the enemy of the self. | ☐ | ☐ | ☐ |
|  | 6.06 | Friend if conquered, enemy if not | For him who has conquered the self by the Self, the Self is a friend; but for him who has not conquered the self, the Self abides as an enemy, hostile. | ☐ | ☐ | ☐ |
|  | 6.07 | The self-conquered is at peace | The self-conquered, tranquil one is established in the Self — equal in cold and heat, pleasure and pain, honour and dishonour. | ☐ | ☐ | ☐ |
|  | 6.08 | A clod, a stone, and gold alike | He who is satisfied with knowledge and realization, unmoved, with senses conquered, to whom a lump of earth, a stone and gold are alike — he is called a yoked one. | ☐ | ☐ | ☐ |
|  | 6.09 | Equal to friend and foe | He who is the same toward well-wishers, friends, foes, the indifferent, neutrals, the hateful, kinsmen, the righteous and even sinners — he excels. | ☐ | ☐ | ☐ |
|  | 6.10 | Alone, in solitude | Let the yogi constantly discipline himself, abiding in a solitary place, alone, with mind and self controlled, free from desire and possessiveness. | ☐ | ☐ | ☐ |
|  | 6.11 | A clean place, neither too high nor too low | Establishing in a pure spot a steady seat for himself, neither too high nor too low, covered with cloth, a deer-skin and kuśa grass, | ☐ | ☐ | ☐ |
|  | 6.12 | Calm the mind and senses | making the mind one-pointed, restraining the activities of the mind and the senses, seated on that seat, let him practise yoga for the purification of the self. | ☐ | ☐ | ☐ |
|  | 6.13 | Body, head and neck erect | Holding body, head and neck steady and unmoving, gazing at the tip of his own nose, not looking about, | ☐ | ☐ | ☐ |
|  | 6.14 | Calm and fearless | with a serene mind, fearless, firm in the vow of brahmacarya, the mind controlled, thoughts resting on me — let the yoked one sit, devoted to me. | ☐ | ☐ | ☐ |
|  | 6.15 | The yogi attains the peace that rests in me | Thus disciplining himself always, the yogi of controlled mind attains the peace of nirvāṇa that abides in me. | ☐ | ☐ | ☐ |
|  | 6.16 | Yoga is not attained through extremes | Verily yoga is not attained by him who eats too much nor by him who does not eat at all, nor by him who sleeps too much nor by him who keeps awake too much, O Arjuna. | ☐ | ☐ | ☐ |
|  | 6.17 | Moderate in food, sleep and work | For him who is temperate in food and recreation, temperate in his efforts, temperate in sleep and waking, yoga becomes the destroyer of sorrow. | ☐ | ☐ | ☐ |
|  | 6.18 | When the mind rests in the Self | When the well-trained mind rests in the Self alone, free from longing for all objects of desire — then one is said to be yoked. | ☐ | ☐ | ☐ |
|  | 6.19 | As a lamp in a windless place | As a lamp placed in a windless spot does not flicker — this simile is declared of a yogi of controlled mind, practising yoga of the Self. | ☐ | ☐ | ☐ |
|  | 6.20 | Beholding the Self, content in the Self | That in which, by the practice of yoga, the mind comes to rest, and beholding the Self by the self, one is content in the Self alone — | ☐ | ☐ | ☐ |
|  | 6.21 | A joy the senses cannot reach | — that which, being apprehended by the intellect beyond the senses, one knows as boundless joy, and established in which one never departs from the truth — | ☐ | ☐ | ☐ |
|  | 6.22 | No gain is counted greater than this | — having gained which one deems no other gain superior, in which one is not disturbed even by great sorrow — that state is known as yoga, the sundering of union with sorrow. | ☐ | ☐ | ☐ |
|  | 6.23 | Practise with resolve and an undiscouraged mind | That yoga, the disconnection of union with sorrow, should be practised with determination, with an undiscouraged mind. | ☐ | ☐ | ☐ |
|  | 6.24 | Abandon all desires born of intention | Abandoning without exception all desires born of resolve, restraining the whole group of senses on every side by the mind alone — | ☐ | ☐ | ☐ |
|  | 6.25 | Slowly, gradually, let him come to rest | — slowly, gradually, let him come to rest through the intellect held firm by resolve; and fixing the mind on the Self alone, let him think of nothing else. | ☐ | ☐ | ☐ |
|  | 6.26 | Wherever the mind wanders, bring it back | From whatever cause the wavering, unsteady mind wanders away, from that alone let him withdraw it and bring it under the control of the Self. | ☐ | ☐ | ☐ |
|  | 6.27 | Supreme bliss comes to the stainless | Supreme bliss verily comes to this yogi whose mind is peaceful, whose passion is stilled, who is become Brahman, free from stain. | ☐ | ☐ | ☐ |
|  | 6.28 | The purified reach bliss | Thus constantly disciplining the self, the yogi, freed from stain, easily attains the endless joy of union with Brahman. | ☐ | ☐ | ☐ |
|  | 6.29 | The Self in all beings | The one whose mind is united in yoga, seeing equally everywhere, sees the Self dwelling in all beings and all beings in the Self. | ☐ | ☐ | ☐ |
|  | 6.30 | I am never lost to him | He who sees me everywhere and sees everything in me — for him I am not lost, and he is not lost to me. | ☐ | ☐ | ☐ |
|  | 6.31 | He lives in me, whatever his way | Established in unity, the yogi who worships me abiding in all beings — abiding in that, he lives in me, whatever his way of life. | ☐ | ☐ | ☐ |
|  | 6.32 | He who feels all as his own | He who, through the likeness of the self, sees the same everywhere, in pleasure and in pain — he is deemed the supreme yogi, O Arjuna. | ☐ | ☐ | ☐ |
|  | 6.33 | Arjuna: the mind is too restless for this | Arjuna said: This yoga of equanimity declared by you, O Madhusūdana — I see no firm foundation for it, because of restlessness. | ☐ | ☐ | ☐ |
|  | 6.34 | The mind is restless as the wind | Verily the mind is restless, turbulent, strong and unyielding, O Kṛṣṇa; I think it is as hard to restrain as the wind. | ☐ | ☐ | ☐ |
|  | 6.35 | By practice and detachment | The Blessed Lord said: Undoubtedly the mind is restless and hard to restrain, O mighty-armed one; but it is restrained, O son of Kuntī, by practice and by dispassion. | ☐ | ☐ | ☐ |
|  | 6.36 | For the unrestrained, yoga is hard | Yoga is hard to attain, I think, for one whose self is unrestrained; but for the self-controlled one who strives by the proper means, it is attainable. | ☐ | ☐ | ☐ |
|  | 6.37 | Arjuna asks what befalls one who fails | Arjuna said: He who, full of faith but unable to control himself, whose mind has fallen away from yoga — not attaining perfection in yoga — what end does he reach, O Kṛṣṇa? | ☐ | ☐ | ☐ |
|  | 6.38 | Lost like a torn cloud | Falling from both, does he not perish like a riven cloud, O mighty-armed one, without support, deluded on the path of Brahman? | ☐ | ☐ | ☐ |
|  | 6.39 | This doubt you must dispel | This doubt of mine you should dispel wholly, O Kṛṣṇa; no other than you is found to destroy this doubt. | ☐ | ☐ | ☐ |
|  | 6.40 | No doer of good comes to grief | The Blessed Lord said: O Pārtha, neither in this world nor in the next is there destruction for him; for none who does good, my son, goes to evil. | ☐ | ☐ | ☐ |
|  | 6.41 | Born again in a pure house | Having attained the worlds of the righteous and dwelt there for immemorial years, he who fell from yoga is born again in the house of the pure and prosperous. | ☐ | ☐ | ☐ |
|  | 6.42 | Or in a family of yogis | Or he is born into a family of wise yogis; truly a birth like this is very hard to obtain in this world. | ☐ | ☐ | ☐ |
|  | 6.43 | He regains spiritual insight from a past life | There he regains the understanding of his former body, O son of the Kurus, and from there he strives again for perfection. | ☐ | ☐ | ☐ |
|  | 6.44 | Carried onward by former practice | By that very former practice he is carried along, even in spite of himself; even the one who merely wishes to know yoga transcends the word-Brahman. | ☐ | ☐ | ☐ |
|  | 6.45 | Perfected through many births | But the yogi who strives with effort, purified of sin, perfected gradually through many births, then reaches the highest state. | ☐ | ☐ | ☐ |
|  | 6.46 | The yogi is greater than the ascetic | The yogi is greater than the ascetic, deemed greater than the man of knowledge, and greater than the man of rites; therefore be a yogi, O Arjuna. | ☐ | ☐ | ☐ |
|  | 6.47 | Most yoked: he who worships me with faith | And among all yogis, he who, full of faith, worships me with his inmost self established in me — him I deem the most yoked, in my view. | ☐ | ☐ | ☐ |


### Chapter 7 — Jñāna-Vijñāna Yoga · verses 7.01–7.30 · 30 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 7.01 | Hear how to know me fully | The Blessed Lord said: With the mind attached to me, O Pārtha, practising yoga and taking refuge in me — how, without doubt, you will know me in full, that listen. | ☐ | ☐ | ☐ |
|  | 7.02 | Realization, not mere knowledge | I shall declare to you this knowledge together with its realization, without remainder; knowing which, nothing further remains to be known here. | ☐ | ☐ | ☐ |
|  | 7.03 | One in thousands strives | Among thousands of men, one perchance strives for perfection; and among those who strive, one perchance knows me in truth. | ☐ | ☐ | ☐ |
|  | 7.04 | My nature divided eightfold | Earth, water, fire, air, ether, mind, intellect and egoism — thus is my nature divided eightfold. | ☐ | ☐ | ☐ |
|  | 7.05 | The higher nature that sustains the world | This is the lower nature; but know my other nature, higher than this, O mighty-armed one — the life-element, by which the world is upheld. | ☐ | ☐ | ☐ |
|  | 7.06 | The womb of all beings | Know that these two natures are the womb of all beings; I am the origin and also the dissolution of the whole world. | ☐ | ☐ | ☐ |
|  | 7.07 | Strung on me like pearls on a thread | There is nothing whatever higher than me, O Dhanañjaya; all this is strung on me, like a row of gems on a thread. | ☐ | ☐ | ☐ |
|  | 7.08 | The taste in water, the light in sun and moon | I am the taste in waters, O son of Kuntī; I am the radiance of the moon and the sun; the sacred syllable Om in all the Vedas; the sound in ether; the manliness in men. | ☐ | ☐ | ☐ |
|  | 7.09 | The fragrance of earth, the heat in fire | I am the pure fragrance of the earth and the heat of fire; the life of all beings and the austerity of the ascetics. | ☐ | ☐ | ☐ |
|  | 7.10 | The eternal seed of all beings | Know me, O Pārtha, as the eternal seed of all beings; I am the intelligence of the intelligent, the splendour of the splendid. | ☐ | ☐ | ☐ |
|  | 7.11 | Desire not opposed to dharma | And I am the strength of the strong, devoid of desire and attachment; and in beings I am desire that is not opposed to dharma, O bull of the Bhāratas. | ☐ | ☐ | ☐ |
|  | 7.12 | They are in me, I am not in them | And whatever states there are, of sattva, rajas or tamas — know them all as from me alone; yet I am not in them, they are in me. | ☐ | ☐ | ☐ |
|  | 7.13 | The world does not know me | Deluded by these states made of the three guṇas, this entire world does not know me, who am beyond them, imperishable. | ☐ | ☐ | ☐ |
|  | 7.14 | Take refuge in me to cross my difficult māyā | This divine māyā of mine, consisting of the guṇas, is hard to overcome; but those who take refuge in me alone cross beyond this māyā. | ☐ | ☐ | ☐ |
|  | 7.15 | The evildoers do not come to me | The wrong-doers, the deluded, the lowest of men do not resort to me; robbed of knowledge by māyā, they cling to a demoniac nature. | ☐ | ☐ | ☐ |
|  | 7.16 | Four kinds worship me | Four kinds of men of good deeds worship me, O Arjuna: the afflicted, the seeker of knowledge, the seeker of wealth, and the wise, O bull of the Bhāratas. | ☐ | ☐ | ☐ |
|  | 7.17 | The wise one is dearest | Of them, the man of knowledge, ever yoked, of single devotion, is the best; for I am extremely dear to the wise, and he is dear to me. | ☐ | ☐ | ☐ |
|  | 7.18 | The wise one is my very Self | Noble are all these; but the wise one is my very self, in my opinion; for he, self-possessed, is established in me, the supreme goal. | ☐ | ☐ | ☐ |
|  | 7.19 | At the end of many births | At the end of many births, the man of wisdom resorts to me, thinking 'Vāsudeva is all'; that great soul is very rare. | ☐ | ☐ | ☐ |
|  | 7.20 | Deprived of discernment | Those whose knowledge is stolen by desires resort to other deities, following this or that rite, constrained by their own nature. | ☐ | ☐ | ☐ |
|  | 7.21 | I make a devotee's faith unshakeable | Whatever divine form a devotee desires to worship with faith, I render that very faith of his steady. | ☐ | ☐ | ☐ |
|  | 7.22 | The desires are granted | United with that faith, he engages in the worship of that deity, and from it obtains his desires — which are verily ordained by me. | ☐ | ☐ | ☐ |
|  | 7.23 | Finite fruit for the finite-minded | But the fruit of those worshippers is limited; the fruit belongs to the small-minded. The worshippers of the gods go to the gods; my devotees come to me. | ☐ | ☐ | ☐ |
|  | 7.24 | The unwise think me manifest | The unintelligent, not knowing my higher nature — imperishable and unsurpassed — think of me, the unmanifest, as one who has taken on manifestation. | ☐ | ☐ | ☐ |
|  | 7.25 | Veiled by my Yoga-Māyā | I am not manifest to all, being enveloped by yoga-māyā; this deluded world does not know me, the unborn, the imperishable. | ☐ | ☐ | ☐ |
|  | 7.26 | I know all beings; none knows me | I know, O Arjuna, the beings that have passed, that exist now, and that are to come; but no one knows me. | ☐ | ☐ | ☐ |
|  | 7.27 | Deluded by the pairs of opposites | By the delusion of the pairs of opposites, arising from desire and aversion, O Bhārata, all beings go to delusion at birth, O scorcher of foes. | ☐ | ☐ | ☐ |
|  | 7.28 | Whose sin has ended, freed from the pairs | But those men of good deeds whose sins have come to an end — freed from the delusion of the pairs of opposites — worship me with firm vows. | ☐ | ☐ | ☐ |
|  | 7.29 | Striving for freedom, they know Brahman | Those who, striving for freedom from old age and death, take refuge in me — they know Brahman, the entire adhyātma, and all action. | ☐ | ☐ | ☐ |
|  | 7.30 | They know me even at the hour of death | Those who know me along with the elements, the deities and the sacrifice — even at the time of death, with minds established, they know me. | ☐ | ☐ | ☐ |


### Chapter 8 — Akṣara-Brahma Yoga · verses 8.01–8.28 · 28 titles, 1 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 8.01 | Brahman, adhyātma, action, adhibhūta, adhidaiva? | Arjuna said: What is that Brahman, what is adhyātma, what is action, O best of men? What is declared adhibhūta, and what is called adhidaiva? | ☐ | ☐ | ☐ |
|  | 8.02 | Who is adhiyajña? How is Kṛṣṇa known at death? | Who and how is adhiyajña here in this body, O Madhusūdana? And how are you to be known at the time of death by the self-controlled? | ☐ | ☐ | ☐ |
|  | 8.03 | Brahman, adhyātma, karma | The Blessed Lord said: The imperishable is the supreme Brahman; one's own nature is called adhyātma; the creative impulse that brings forth beings is called karma. | ☐ | ☐ | ☐ |
|  | 8.04 | Adhibhūta, adhidaiva, adhiyajña | Adhibhūta is the perishable nature; the Puruṣa is adhidaivata; I myself am adhiyajña here in the body, O best of the embodied. | ☐ | ☐ | ☐ |
|  | 8.05 | He who remembers me at the end | Whoever, at the end, leaves the body remembering me alone — he attains my being; there is no doubt of this. | ☐ | ☐ | ☐ |
|  | 8.06 | Whatever state one remembers at death | Whatever state one remembers at the end while leaving the body — to that state one goes, O son of Kuntī, ever pervaded by that thought. | ☐ | ☐ | ☐ |
|  | 8.07 | Therefore remember me and fight | Therefore remember me at all times and fight; with mind and intellect offered to me, you will surely come to me, without doubt. | ☐ | ☐ | ☐ |
|  | 8.08 | With mind unwavering | United with the yoga of practice, with a mind that goes nowhere else, O Pārtha — one reaches the supreme divine Person, contemplating him. | ☐ | ☐ | ☐ |
|  | 8.09 | The ancient seer, subtler than the atom | He who meditates on the ancient seer, the ruler, subtler than the subtle, the support of all, of inconceivable form, radiant as the sun, beyond darkness — | ☐ | ☐ | ☐ |
|  | 8.10 | At death, with the breath between the brows | — at the time of death, with an unwavering mind, united with devotion and the power of yoga, breath fixed between the brows — he reaches that supreme divine Person. | ☐ | ☐ | ☐ |
|  | 8.11 | That which the Vedas call imperishable | That which the knowers of the Vedas call the imperishable, which the desireless ascetics enter, desiring which they practise celibacy — that goal I shall declare to you briefly. | ☐ | ☐ | ☐ |
|  | 8.12 | Closing the gates, fixing the breath | Restraining all the gates of the body, confining the mind in the heart, fixing the life-breath in the head, established in yogic concentration — | ☐ | ☐ | ☐ |
|  | 8.13 | Uttering Om, the single syllable | — uttering the single syllable Om, the Brahman, and remembering me — he who departs, giving up the body, reaches the supreme goal. | ☐ | ☐ | ☐ |
|  | 8.14 | Easily reached by one who remembers me always | He who always remembers me, with a single mind, ever — for that ever-yoked yogi I am easy to reach, O Pārtha. | ☐ | ☐ | ☐ |
|  | 8.15 | No rebirth in this impermanent house of sorrow | Having reached me, the great souls do not return to birth — the abode of sorrow, impermanent — they have attained the highest perfection. | ☐ | ☐ | ☐ |
|  | 8.16 | Even Brahmā's world returns | From the world of Brahmā down, all worlds return again, O Arjuna; but reaching me, O Kaunteya, there is no rebirth. | ☐ | ☐ | ☐ |
|  | 8.17 | A thousand ages are one day | Those who know Brahmā's day to end in a thousand yugas, and the night to end in a thousand — they know day and night. | ☐ | ☐ | ☐ |
|  | 8.18 | At daybreak all emerge, at nightfall dissolve | From the unmanifest all manifest things arise at the coming of day; at the coming of night they dissolve into the unmanifest. | ☐ | ☐ | ☐ |
|  | 8.19 | At Brahmā's dawn, beings rise; at night, they dissolve | This same host of beings, arising again and again, dissolves at the coming of night, O Pārtha, and arises at the coming of day. | ☐ | ☐ | ☐ |
|  | 8.20 | Another unmanifest, eternal | But beyond this unmanifest is another unmanifest, eternal — which, when all beings perish, does not perish. | ☐ | ☐ | ☐ |
|  | 8.21 | Reaching it, they do not return | That unmanifest is called the imperishable; they call it the supreme goal; reaching which they do not return — that is my supreme abode. | ☐ | ☐ | ☐ |
|  | 8.22 | Attained by devotion alone | That supreme Person, O Pārtha, is attainable by devotion to him alone; in him all beings dwell, and by him all this is pervaded. | ☐ | ☐ | ☐ |
| ⚑ | 8.23 | The two times of departure | Now I shall declare, O bull of the Bhāratas, the time in which yogis, departing, do not return, and the time in which they return. | ☐ | ☐ | ☐ |
|  | 8.24 | Fire, light, day, the bright fortnight | Fire, light, day, the bright fortnight, the six months of the northern course — departing by that path, the knowers of Brahman go to Brahman. | ☐ | ☐ | ☐ |
|  | 8.25 | Smoke, night, the dark fortnight | Smoke, night, the dark fortnight, the six months of the southern course — attaining the lunar light by that path, the yogi returns. | ☐ | ☐ | ☐ |
|  | 8.26 | The two eternal paths | These two paths, bright and dark, are the eternal paths of the world; by one, one goes without return, by the other one returns again. | ☐ | ☐ | ☐ |
|  | 8.27 | Knowing both, no yogi is deluded | Knowing these two paths, O Pārtha, the yogi is never deluded; therefore, at all times be united in yoga, O Arjuna. | ☐ | ☐ | ☐ |
|  | 8.28 | Beyond fruits of Vedas, sacrifice, austerity and gifts | Whatever fruit of merit is declared in the Vedas, sacrifices, austerities and gifts — the yogi, knowing all this, transcends it all and reaches the supreme primeval abode. | ☐ | ☐ | ☐ |

* ⚑ **8.23** — number unsupported. Advisory text: “The two times of departure”


### Chapter 9 — Rāja-Vidyā-Rāja-Guhya Yoga · verses 9.01–9.34 · 34 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 9.01 | The supreme secret | The Blessed Lord said: To you, who do not find fault, I will declare this profoundest secret — knowledge together with its realization; knowing which, you shall be freed from evil. | ☐ | ☐ | ☐ |
|  | 9.02 | The royal knowledge | This is the royal knowledge, the royal secret, the supreme purifier, directly perceived, righteous, very easy to practise, and imperishable. | ☐ | ☐ | ☐ |
|  | 9.03 | The faithless return to death and rebirth | The men without faith in this dharma, O scorcher of foes, not reaching me, return to the path of death and rebirth. | ☐ | ☐ | ☐ |
|  | 9.04 | All pervaded by me | By me this whole world is pervaded in my unmanifest form; all beings rest in me, but I am not contained in them. | ☐ | ☐ | ☐ |
|  | 9.05 | The divine yoga | And beings do not rest in me — behold my divine yoga! I sustain all beings yet stand apart, and my self is the origin of beings. | ☐ | ☐ | ☐ |
|  | 9.06 | As wind in space | As the vast wind, ever moving, abides in space, so all beings abide in me — know this. | ☐ | ☐ | ☐ |
|  | 9.07 | The revolving creation | All beings, O son of Kuntī, return to my prakṛti at the end of a kalpa; at the beginning of a kalpa I send them forth again. | ☐ | ☐ | ☐ |
|  | 9.08 | Again and again I create | Taking hold of my own prakṛti, I send forth again and again this whole host of beings, helpless under the power of nature. | ☐ | ☐ | ☐ |
|  | 9.09 | Unbound by action | These actions do not bind me, O Dhanañjaya, for I sit as one indifferent, unattached to these actions. | ☐ | ☐ | ☐ |
|  | 9.10 | Under my direction | Under my supervision, prakṛti brings forth the moving and the unmoving; for this reason, O son of Kuntī, the world revolves. | ☐ | ☐ | ☐ |
|  | 9.11 | The deluded despise me | The deluded, not knowing my supreme being, despise me wearing a human form. | ☐ | ☐ | ☐ |
|  | 9.12 | Vain hopes, vain works, vain knowledge | Of vain hopes, vain works and vain knowledge, senseless — they cling to the deluding, demoniac and asuric nature. | ☐ | ☐ | ☐ |
|  | 9.13 | The great souls know me as imperishable | But the great souls, O Pārtha, taking refuge in the divine nature, worship me with undivided mind, knowing me as the imperishable source of beings. | ☐ | ☐ | ☐ |
|  | 9.14 | Ever glorifying me, firm in vows | Always glorifying me, striving with firm vows, bowing to me with devotion, ever united — they worship me. | ☐ | ☐ | ☐ |
|  | 9.15 | The sacrifice of knowledge | And others worship me with the sacrifice of knowledge, worshipping me as the one, as the distinct, as the manifold facing everywhere. | ☐ | ☐ | ☐ |
|  | 9.16 | I am the sacrifice | I am the rite, I am the sacrifice, I am the oblation to the ancestors, I am the herb; I am the mantra, I am the butter, I am the fire, I am the offering. | ☐ | ☐ | ☐ |
|  | 9.17 | I am father and mother | I am the father and mother of this world, its supporter and grandsire; I am the object of knowledge, the purifier, the syllable Om, and the Ṛk, Sāma and Yajus. | ☐ | ☐ | ☐ |
|  | 9.18 | I am everything | I am the goal, the sustainer, the lord, the witness, the abode, the refuge and the friend; the origin, dissolution, ground, treasure and eternal seed. | ☐ | ☐ | ☐ |
|  | 9.19 | I send and withhold the rain | I give heat; I send and withhold the rain; I am immortality and also death; I am the real and the unreal, O Arjuna. | ☐ | ☐ | ☐ |
|  | 9.20 | Soma drinkers seek heaven | The knowers of the three Vedas, drinking soma, purified of sin, worshipping me by sacrifice, pray for the path to heaven; attaining the world of Indra, they enjoy the divine pleasures of the gods … | ☐ | ☐ | ☐ |
|  | 9.21 | Merit spent, they fall back to earth | Having enjoyed the vast world of heaven, when their merit is exhausted they return to the world of mortals; thus, following the dharma of the three Vedas, desiring desires, they come and go. | ☐ | ☐ | ☐ |
|  | 9.22 | I bear the welfare of my devotees | To those who worship me, ever united, thinking of me alone — for them, ever devoted, I myself carry what they lack and preserve what they have. | ☐ | ☐ | ☐ |
|  | 9.23 | Even those who worship other gods | Even those who, devoted to other deities, worship them with faith — they worship me alone, O son of Kuntī, though not in the prescribed way. | ☐ | ☐ | ☐ |
|  | 9.24 | I am the enjoyer of all sacrifices | For I alone am the enjoyer and lord of all sacrifices; but they do not know me in truth, and so they fall. | ☐ | ☐ | ☐ |
|  | 9.25 | Each reaches the object they worship | The worshippers of the gods go to the gods; the worshippers of the ancestors go to the ancestors; the worshippers of the spirits go to the spirits; but my worshippers come to me. | ☐ | ☐ | ☐ |
|  | 9.26 | A leaf, a flower, fruit or water | Whoever offers me with devotion a leaf, a flower, a fruit or water — I accept that offering of the pure-hearted. | ☐ | ☐ | ☐ |
|  | 9.27 | Whatever you do, offer it to me | Whatever you do, whatever you eat, whatever you offer, whatever you give, whatever austerity you perform, O son of Kuntī — do it as an offering to me. | ☐ | ☐ | ☐ |
|  | 9.28 | The fruit of renunciation | Thus you shall be freed from the bonds of actions, which bear good and evil fruit; with the self yoked in renunciation, liberated, you shall come to me. | ☐ | ☐ | ☐ |
|  | 9.29 | Equal to all | I am the same to all beings; none is dear or hated by me; but those who worship me with devotion — they are in me, and I am in them. | ☐ | ☐ | ☐ |
|  | 9.30 | Even a grave sinner, if wholly devoted, is righteous | Even if a man of very evil conduct worships me with single-minded devotion, he is to be regarded as good, for he is rightly resolved. | ☐ | ☐ | ☐ |
|  | 9.31 | My devotee never perishes | Quickly he becomes righteous of soul and attains lasting peace; know this for certain, O son of Kuntī: my devotee never perishes. | ☐ | ☐ | ☐ |
|  | 9.32 | All who take refuge reach the supreme goal | For those who take refuge in me, O Pārtha — even those of sinful birth, women, traders and labourers — they too reach the supreme goal. | ☐ | ☐ | ☐ |
|  | 9.33 | Having come to this fleeting world, worship me | How much more then the holy brāhmaṇas and the devoted royal sages! Having come to this impermanent, joyless world, worship me. | ☐ | ☐ | ☐ |
|  | 9.34 | Fix your mind on me | Fix your mind on me, be my devotee, offer to me, bow to me — thus yoking the self to me, intent on me, you shall surely come to me. | ☐ | ☐ | ☐ |


### Chapter 10 — Vibhūti Yoga · verses 10.01–10.42 · 42 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 10.01 | Hear again my supreme word | The Blessed Lord said: Hear again, O mighty-armed one, my supreme words, which I speak to you who are dear, wishing your good. | ☐ | ☐ | ☐ |
|  | 10.02 | Neither gods nor seers know my origin | Neither the hosts of gods nor the great seers know my origin; for I am the beginning of the gods and the great seers in every way. | ☐ | ☐ | ☐ |
|  | 10.03 | He who knows me unborn and beginningless | He who knows me as unborn, without beginning, the great Lord of the world — undeluded among mortals, he is freed from all sins. | ☐ | ☐ | ☐ |
|  | 10.04 | Intellect, knowledge, non-delusion | Intellect, knowledge, freedom from delusion, forbearance, truth, self-control, calm — pleasure, pain, birth, death, fear and fearlessness, | ☐ | ☐ | ☐ |
|  | 10.05 | All these states arise from me | non-violence, equanimity, contentment, austerity, generosity, fame and infamy — these various states of beings arise from me alone. | ☐ | ☐ | ☐ |
|  | 10.06 | The seven great seers | The seven great seers, the four ancient Manus, born of my mind — from them come the beings of this world. | ☐ | ☐ | ☐ |
|  | 10.07 | He who knows this glory is joined to me | He who knows in truth this glory and power of mine is united to me by unwavering yoga — of this there is no doubt. | ☐ | ☐ | ☐ |
|  | 10.08 | I am the origin of all; the wise worship me | I am the source of all; everything proceeds from me. Knowing this, the wise worship me, filled with devotion. | ☐ | ☐ | ☐ |
|  | 10.09 | Speaking of me, my devotees rejoice | Their thoughts on me, their lives given to me, enlightening one another, always speaking of me — they are content and rejoice. | ☐ | ☐ | ☐ |
|  | 10.10 | To them I give the yoga of understanding | To them, ever devoted, worshipping me with love, I give the yoga of discernment, by which they come to me. | ☐ | ☐ | ☐ |
|  | 10.11 | I destroy the darkness with the lamp of knowledge | Out of compassion for them, dwelling in their hearts, I destroy the darkness born of ignorance with the shining lamp of knowledge. | ☐ | ☐ | ☐ |
|  | 10.12 | You are the supreme Brahman | Arjuna said: You are the supreme Brahman, the supreme light, the supreme purifier; the eternal divine Person, the primal God, unborn and all-pervading. | ☐ | ☐ | ☐ |
|  | 10.13 | All the sages say so | Thus the seers call you — Nārada the divine sage, Asita, Devala, Vyāsa — and you yourself tell me. | ☐ | ☐ | ☐ |
|  | 10.14 | Neither gods nor demons know your manifestation | I hold all this you tell me as true, Keśava; indeed, neither gods nor demons, O Lord, know your manifestation. | ☐ | ☐ | ☐ |
|  | 10.15 | You alone know yourself by yourself | You yourself know yourself by yourself, O supreme Person — O source of beings, Lord of beings, God of gods, Lord of the world! | ☐ | ☐ | ☐ |
|  | 10.16 | Tell me of your divine glories | Tell me without omission your divine glories, by which you abide, pervading these worlds. | ☐ | ☐ | ☐ |
|  | 10.17 | In what forms shall I meditate on you? | How shall I know you, O yogi, contemplating you always? And in what states are you to be thought of, O Lord? | ☐ | ☐ | ☐ |
|  | 10.18 | I am never sated hearing your nectar | Tell me again, in detail, your yoga and your glory, O Janārdana; I am never satiated with hearing your nectar. | ☐ | ☐ | ☐ |
|  | 10.19 | Only the chief of my glories | The Blessed Lord said: Yes, I shall declare to you my divine glories — chiefly, O best of the Kurus; there is no end to my extent. | ☐ | ☐ | ☐ |
|  | 10.20 | I am the Self seated in the heart of all | I am the Self, O Guḍākeśa, dwelling in the hearts of all beings; I am the beginning, the middle, and the end of all beings. | ☐ | ☐ | ☐ |
|  | 10.21 | Viṣṇu, the sun, the moon | Among the Ādityas I am Viṣṇu; among the lights, the radiant sun; I am Marīci among the winds; I am the moon among the stars. | ☐ | ☐ | ☐ |
|  | 10.22 | Among the senses I am the mind | Among the Vedas I am the Sāma-veda; among the gods I am Indra; among the senses I am the mind; among beings I am consciousness. | ☐ | ☐ | ☐ |
|  | 10.23 | Śaṅkara, Kubera, fire, Meru | Among the Rudras I am Śaṅkara; among the yakṣas and rākṣasas, the lord of wealth; among the Vasus I am fire; among mountains, Meru. | ☐ | ☐ | ☐ |
|  | 10.24 | Bṛhaspati, Skanda, the ocean | Among priests, O Pārtha, know me as the chief, Bṛhaspati; among generals I am Skanda; among waters I am the ocean. | ☐ | ☐ | ☐ |
|  | 10.25 | Among words, the syllable Om | Among the great seers I am Bhṛgu; among words I am the single syllable Om; among sacrifices I am the japa-sacrifice; among the immovable I am the Himālaya. | ☐ | ☐ | ☐ |
|  | 10.26 | The aśvattha, Nārada, Kapila | Among all trees I am the aśvattha; among the divine sages, Nārada; among the gandharvas, Citraratha; among the perfected, the sage Kapila. | ☐ | ☐ | ☐ |
|  | 10.27 | Uccaiḥśravas, Airāvata, the king | Among horses know me as Uccaiḥśravas, born of nectar; among lordly elephants, Airāvata; among men, the king. | ☐ | ☐ | ☐ |
|  | 10.28 | The thunderbolt, Kāmadhuk, Vāsuki | Among weapons I am the thunderbolt; among cows I am Kāmadhuk; I am the lord of love among procreators; among serpents, Vāsuki. | ☐ | ☐ | ☐ |
|  | 10.29 | Ananta, Varuṇa, Aryaman, Yama | I am the infinite among serpents; Varuṇa among the waters; among the ancestors I am Aryaman; among rulers, Yama. | ☐ | ☐ | ☐ |
|  | 10.30 | Prahlāda, time, the lion, Garuḍa | Among the demons I am Prahlāda; among the calculators, time; among beasts I am the lion; among birds, Garuḍa. | ☐ | ☐ | ☐ |
|  | 10.31 | The wind, Rāma, the Ganges | Among purifiers I am the wind; among warriors I am Rāma; among fishes I am the makara; among streams I am the Ganges. | ☐ | ☐ | ☐ |
|  | 10.32 | The beginning, middle and end of all | Of creations I am the beginning, the middle, and also the end, O Arjuna; among the sciences I am the science of the Self; among debaters, the argument. | ☐ | ☐ | ☐ |
|  | 10.33 | Among letters, the letter a | Among letters I am the letter A; among compounds the dvandva; I am indeed inexhaustible time; I am the ordainer facing everywhere. | ☐ | ☐ | ☐ |
|  | 10.34 | I am all-devouring death | I am all-devouring death and the birth of all that will be; among women I am fame, fortune, speech, memory, wisdom, constancy and forbearance. | ☐ | ☐ | ☐ |
|  | 10.35 | The Bṛhat-sāma, the Gāyatrī, the spring | Among the Sāma-chants I am the Bṛhat-sāma; among metres the Gāyatrī; among months I am Mārgaśīrṣa; among seasons the spring. | ☐ | ☐ | ☐ |
|  | 10.36 | The dice of gamblers, the splendour of the splendid | I am the dice of the gamblers; I am the splendour of the splendid; I am victory, I am determination; I am the goodness of the good. | ☐ | ☐ | ☐ |
|  | 10.37 | Among the Pāṇḍavas, Arjuna | Among the Vṛṣṇis I am Vāsudeva; among the Pāṇḍavas, Arjuna; among the sages I am Vyāsa; among the poets, Uśanā the poet. | ☐ | ☐ | ☐ |
|  | 10.38 | The silence of secrets | I am the rod of the punishers; among those seeking victory I am policy; I am the silence of the secret; among the knowing I am knowledge. | ☐ | ☐ | ☐ |
|  | 10.39 | Whatever is the seed of all beings | And whatever is the seed of all beings, that I am, O Arjuna; no being, moving or unmoving, exists without me. | ☐ | ☐ | ☐ |
|  | 10.40 | There is no end to my glories | There is no end to my divine glories, O scorcher of foes; this is but a summary declared by me of the extent of my glory. | ☐ | ☐ | ☐ |
|  | 10.41 | Whatever is glorious is a spark of my splendour | Whatever being is glorious, radiant or powerful — know that to be born of a portion of my splendour. | ☐ | ☐ | ☐ |
|  | 10.42 | I support this whole world with one fragment | But what need, Arjuna, of this detailed knowledge? I stand supporting this whole world with one part of myself. | ☐ | ☐ | ☐ |


### Chapter 11 — Viśvarūpa-Darśana Yoga · verses 11.01–11.55 · 55 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 11.01 | My delusion is gone | Arjuna said: By your compassionate words about the supreme secret of the Self, my delusion is gone. | ☐ | ☐ | ☐ |
|  | 11.02 | I have heard how beings arise and pass | The origin and dissolution of beings have I heard from you in detail, O lotus-eyed one, and your infinite glory. | ☐ | ☐ | ☐ |
|  | 11.03 | I want to see your form | Even as you have described yourself, O supreme Lord, I long to see your cosmic form, O best of persons. | ☐ | ☐ | ☐ |
|  | 11.04 | If you think I can see it, show me | If you think it can be seen by me, O Lord, then show me your imperishable self, O Lord of yoga. | ☐ | ☐ | ☐ |
|  | 11.05 | Behold my hundreds and thousands of forms | The Blessed Lord said: Behold, O Pārtha, my forms by the hundred and thousand, of various kinds and colors. | ☐ | ☐ | ☐ |
|  | 11.06 | The Vasus, Rudras, Aśvins | Behold the Ādityas, the Vasus, the Rudras, the Aśvins and the Maruts; behold many wonders never seen before, O Bhārata. | ☐ | ☐ | ☐ |
|  | 11.07 | See the whole world in my body | Behold now the whole universe, moving and unmoving, gathered in one body here in mine, O Guḍākeśa — and whatever else you wish to see. | ☐ | ☐ | ☐ |
|  | 11.08 | I give you a divine eye | But you cannot see me with your own eye; I give you the divine eye — behold my divine sovereignty. | ☐ | ☐ | ☐ |
|  | 11.09 | The great Lord of yoga showed his form | Sañjaya said: Having spoken thus, O king, the great Lord of yoga, Hari, showed Pārtha his supreme divine form. | ☐ | ☐ | ☐ |
|  | 11.10 | Marvels beyond count | With countless faces and eyes, with countless wondrous sights, with countless divine ornaments and uplifted weapons, | ☐ | ☐ | ☐ |
|  | 11.11 | Infinite, facing everywhere, full of wonders | wearing divine garlands and robes, anointed with divine perfumes, full of all wonders — the infinite God, facing everywhere. | ☐ | ☐ | ☐ |
|  | 11.12 | Brighter than a thousand suns at once | If the splendour of a thousand suns were to rise at once in the sky, it might resemble the splendour of that great being. | ☐ | ☐ | ☐ |
|  | 11.13 | The whole universe in one place | There, in the body of the God of gods, the son of Pāṇḍu saw the whole universe, one yet divided into manifold forms. | ☐ | ☐ | ☐ |
|  | 11.14 | Hair on end, bowing with folded hands | Then, filled with wonder, his hair standing on end, Dhanañjaya bowed his head to the God and spoke with joined palms. | ☐ | ☐ | ☐ |
|  | 11.15 | I see all beings in your body | I see all the gods in your body, O God, and all the hosts of beings; Brahmā the Lord seated on the lotus, and all the seers and divine serpents. | ☐ | ☐ | ☐ |
|  | 11.16 | Infinite arms, no beginning, middle or end | I see you with countless arms, bellies, mouths and eyes — of endless form on every side; I see no end, no middle, no beginning of you, O Lord of the universe, O cosmic form. | ☐ | ☐ | ☐ |
|  | 11.17 | A blazing mass of radiance | I see you crowned, wielding mace and discus, a mass of light shining everywhere — hard to gaze upon, blazing like fire and sun, immeasurable. | ☐ | ☐ | ☐ |
|  | 11.18 | You are the imperishable, the supreme to be known | You are the imperishable, the supreme object of knowledge; you are the supreme refuge of this universe; you are the eternal guardian of dharma — the primal Person, so I deem you. | ☐ | ☐ | ☐ |
|  | 11.19 | Sun and moon for eyes | Without beginning, middle or end, of infinite power, with countless arms, with sun and moon for eyes — I see you blazing with fire-like mouths, scorching the whole world with your radiance. | ☐ | ☐ | ☐ |
|  | 11.20 | The three worlds tremble | The space between earth and heaven is filled by you alone, and all the directions; seeing your wondrous, terrible form, the three worlds are in anguish, O great soul. | ☐ | ☐ | ☐ |
|  | 11.21 | The hosts of gods enter you | The hosts of gods enter you; some, afraid, praise you with folded hands; the hosts of great seers and siddhas, saying 'may all be well', extol you with abundant hymns. | ☐ | ☐ | ☐ |
|  | 11.22 | Rudras, Ādityas, Vasus gaze in wonder | The Rudras, Ādityas, Vasus, Sādhyas, Viśve-devas, Aśvins, Maruts and the ancestors — the gandharvas, yakṣas, demons and siddhas — all gaze on you in wonder. | ☐ | ☐ | ☐ |
|  | 11.23 | Seeing your fearsome form, I tremble | Seeing your immense form, O mighty-armed one, with many mouths and eyes, many arms, thighs and feet, many bellies, many fearsome fangs, the worlds tremble — and so do I. | ☐ | ☐ | ☐ |
|  | 11.24 | Touching the sky, blazing with many colours | Touching the sky, blazing, of many colours, with gaping mouths and blazing wide eyes — seeing you, my inmost heart trembles; I find no firmness or peace, O Viṣṇu. | ☐ | ☐ | ☐ |
|  | 11.25 | Like the fire at the end of time | Seeing your terrible mouths with their fearful fangs, like the fire of the end of time, I do not know the directions, nor find any refuge; be gracious, O Lord of gods, abode of the world. | ☐ | ☐ | ☐ |
|  | 11.26 | The sons of Dhṛtarāṣṭra enter your mouths | All these sons of Dhṛtarāṣṭra, with the hosts of kings, enter your mouths — Bhīṣma, Droṇa, Karṇa, and the chief warriors of our side, | ☐ | ☐ | ☐ |
|  | 11.27 | Heads crushed between your teeth | hurrying, they enter your mouths, terrible and frightful with fangs; some are seen stuck between the teeth, their heads crushed. | ☐ | ☐ | ☐ |
|  | 11.28 | As rivers rush into the ocean | As the many rushing currents of rivers pour into the ocean, so these heroes of the mortal world enter your blazing mouths. | ☐ | ☐ | ☐ |
|  | 11.29 | As moths fly into a blazing fire | As moths fly with full speed into a blazing fire for their destruction, so these worlds fly into your mouths for their destruction. | ☐ | ☐ | ☐ |
|  | 11.30 | You lick up all the worlds | You lick up all the worlds with your flaming mouths, devouring them on every side; your terrible rays fill the whole universe, O Viṣṇu. | ☐ | ☐ | ☐ |
|  | 11.31 | Tell me who you are | Tell me who you are, O terrible form; I bow to you — be gracious, O best of gods! I long to know you, the primeval one; I do not understand your workings. | ☐ | ☐ | ☐ |
|  | 11.32 | I am time, destroyer of worlds | The Blessed Lord said: I am Time, the world-destroyer, grown mature; I have come to destroy these worlds — even without you, none of these warriors arrayed against you will remain. | ☐ | ☐ | ☐ |
|  | 11.33 | Be my instrument | Therefore arise and win glory; conquer your enemies and enjoy the thriving kingdom — they are already slain by me; be only the instrument, O Sāvyasācin. | ☐ | ☐ | ☐ |
|  | 11.34 | They are already slain by me | Slay Droṇa, Bhīṣma, Jayadratha, Karṇa and the other warrior-heroes — already killed by me; strike without fear, fight — you shall conquer your rivals in battle. | ☐ | ☐ | ☐ |
|  | 11.35 | Trembling, with faltering voice | Sañjaya said: Hearing these words of Keśava, the crowned Arjuna, trembling, folded his palms and, bowing again, spoke to Kṛṣṇa with faltering voice. | ☐ | ☐ | ☐ |
|  | 11.36 | The world rejoices in your glory | It is fitting, Hṛṣīkeśa, that the world rejoices and delights in your glory; the rākṣasas flee in fear in all directions, and the hosts of siddhas bow to you. | ☐ | ☐ | ☐ |
|  | 11.37 | Why should they not bow to you? | Why should they not bow to you, O great soul, greater than Brahmā, the primal creator — O infinite Lord of gods, abode of the universe, you are the imperishable, being and non-being and beyond both. | ☐ | ☐ | ☐ |
|  | 11.38 | You are the primal God, the ancient person | You are the primal God, the ancient Person, the supreme refuge of this universe; you are the knower and the known, the supreme abode; by you this universe is pervaded, O infinite form. | ☐ | ☐ | ☐ |
|  | 11.39 | You are Vāyu, Yama, Agni, the moon | You are wind, death, fire, Varuṇa, the moon, and the progenitor — and the great grandsire; I bow to you a thousand times — again and yet again I bow to you. | ☐ | ☐ | ☐ |
|  | 11.40 | Salutation on every side | I bow to you from the front and from behind; I bow to you on every side, O all! You are of infinite might and measureless vigour; you pervade all, and so you are all. | ☐ | ☐ | ☐ |
|  | 11.41 | Whatever I said, calling you “friend” | Whatever I said in rash familiarity — 'O Kṛṣṇa, O Yādava, O friend' — not knowing your majesty, whether in carelessness or in love, | ☐ | ☐ | ☐ |
|  | 11.42 | Whatever disrespect I showed in sport | and whatever disrespect I showed you in sport, rest, sitting or at meals, alone or before others, O Acyuta — that I beg you to forgive, O immeasurable one. | ☐ | ☐ | ☐ |
|  | 11.43 | Father of the world, teacher beyond compare | You are the father of this world, moving and unmoving; you are its supreme object of worship and the most venerable teacher; none equals you in the three worlds, how then could any surpass you, O … | ☐ | ☐ | ☐ |
|  | 11.44 | Forgive as a father forgives his son | Therefore, bowing and prostrating my body, I implore you, the adorable Lord, to forgive me as a father forgives his son, a friend his friend, and a lover his beloved, O God. | ☐ | ☐ | ☐ |
|  | 11.45 | Delighted, yet my mind trembles | Having seen what I never saw before, I am delighted, yet my mind trembles with fear; show me, O God, your gracious form — be merciful, O Lord of gods, O Lord of the universe. | ☐ | ☐ | ☐ |
|  | 11.46 | I long to see you crowned, with mace and discus | I long to see you as before — crowned, with mace and discus in hand; appear in that four-armed form, O thousand-armed, universal form. | ☐ | ☐ | ☐ |
|  | 11.47 | By my grace you have seen it | The Blessed Lord said: By my grace, Arjuna, I have shown you this supreme form by my own power — the luminous, universal, infinite, primeval form that none but you has ever seen. | ☐ | ☐ | ☐ |
|  | 11.48 | Not by Vedas or austerities can it be seen | Not by the study of the Vedas and sacrifices, nor by gifts, rites or fierce austerities, can I be seen in this form in the world of men — by any but you, O prince of the Kurus. | ☐ | ☐ | ☐ |
|  | 11.49 | Be not afraid or bewildered | Do not be afraid or bewildered at the sight of this terrible form of mine; free from fear, with a glad heart, behold once more this gracious form of mine. | ☐ | ☐ | ☐ |
|  | 11.50 | Vāsudeva shows his own form again | Sañjaya said: Having spoken thus to Arjuna, Vāsudeva again showed his own form, and the great soul comforted the frightened Arjuna, once more in his gracious appearance. | ☐ | ☐ | ☐ |
|  | 11.51 | Now I am composed and restored | Arjuna said: Seeing this your gracious human form, O Janārdana, I am now composed and restored to my own nature. | ☐ | ☐ | ☐ |
|  | 11.52 | Even the gods long to see this form | The Blessed Lord said: This form of mine that you have seen is very hard to see; even the gods ever long to see this form. | ☐ | ☐ | ☐ |
|  | 11.53 | Not by Vedas, austerity or gifts | I am not to be seen in this way through the Vedas, nor through austerity, nor through gifts, nor through worship; only in the way you have seen me can I be seen. | ☐ | ☐ | ☐ |
|  | 11.54 | By undivided devotion alone | But through single-pointed devotion I can be known, seen and entered in truth, O Arjuna, in this very form, O scorcher of foes. | ☐ | ☐ | ☐ |
|  | 11.55 | He who works for me comes to me | He who does my work, who holds me as the supreme goal, who is devoted to me, free from attachment, without enmity toward any being — he comes to me, O Pāṇḍava. | ☐ | ☐ | ☐ |


### Chapter 12 — Bhakti Yoga · verses 12.01–12.20 · 20 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 12.01 | Which knows yoga better? | Arjuna said: Those devotees who, ever united, worship you — and those who worship the imperishable unmanifest — which of these are the better knowers of yoga? | ☐ | ☐ | ☐ |
|  | 12.02 | Those ever-united in me are best in yoga | The Blessed Lord said: Those who, fixing their minds on me, ever united, worship me with supreme faith — them I deem the most yoked. | ☐ | ☐ | ☐ |
|  | 12.03 | Some worship the imperishable unmanifest | But those who worship the imperishable, the indefinable, the unmanifest — the all-pervading, unthinkable, unchanging, immovable, eternal — | ☐ | ☐ | ☐ |
|  | 12.04 | They too reach me | — controlling all the senses, of equal mind everywhere, rejoicing in the welfare of all beings — they too reach me. | ☐ | ☐ | ☐ |
|  | 12.05 | Greater is the toil of those set on the unmanifest | Greater is the toil of those whose minds are attached to the unmanifest; the unmanifest is hard to attain by embodied beings. | ☐ | ☐ | ☐ |
|  | 12.06 | Those who surrender all actions to me | But those who surrender all actions to me, intent on me, worshipping me with undivided yoga and meditating on me, | ☐ | ☐ | ☐ |
|  | 12.07 | I become their deliverer from the ocean of death | — for them, whose minds are fixed on me, O Pārtha, I swiftly become the deliverer from the ocean of death and rebirth. | ☐ | ☐ | ☐ |
|  | 12.08 | Fix your mind on me alone | Fix your mind on me alone; establish your intellect in me; then you shall live in me alone — of this there is no doubt. | ☐ | ☐ | ☐ |
|  | 12.09 | Then seek me by repeated practice | If you cannot fix your mind steadily on me, then practise the yoga of repetition — seek to reach me by practice, O Dhanañjaya. | ☐ | ☐ | ☐ |
|  | 12.10 | If not, work for my sake | If you are unable to practise even that, be devoted to working for me; even performing actions for my sake, you shall attain perfection. | ☐ | ☐ | ☐ |
|  | 12.11 | If not even that, renounce the fruit | If you cannot do even this, then, taking refuge in my yoga, renounce the fruit of all actions — with the self controlled. | ☐ | ☐ | ☐ |
|  | 12.12 | Fruit-renunciation beats meditation; peace follows | Better indeed is knowledge than practice; better than knowledge is meditation; better than meditation is renunciation of the fruit of action — for from renunciation comes peace, immediately. | ☐ | ☐ | ☐ |
|  | 12.13 | Hating no being, friendly and compassionate | He who hates no being, is friendly and compassionate, free from possessiveness and ego, equal in pleasure and pain, forgiving — | ☐ | ☐ | ☐ |
|  | 12.14 | Ever content, resolved, given to me | — ever content, a yogi, self-controlled, of firm resolve, mind and intellect offered to me — that devotee of mine is dear to me. | ☐ | ☐ | ☐ |
|  | 12.15 | Neither disturbs the world nor is disturbed by it | He by whom the world is not disturbed, and who is not disturbed by the world — freed from joy, anger, fear and anxiety — he is dear to me. | ☐ | ☐ | ☐ |
|  | 12.16 | Unattached, pure, capable, untroubled | He who is unattached, pure, capable, indifferent, free from anxiety, renouncing all undertakings — that devotee of mine is dear to me. | ☐ | ☐ | ☐ |
|  | 12.17 | Neither rejoicing nor hating | He who neither rejoices nor hates, neither grieves nor desires, renouncing good and evil — that devoted one is dear to me. | ☐ | ☐ | ☐ |
|  | 12.18 | Equal to friend and foe, honour and dishonour | Equal to friend and foe, to honour and dishonour, to cold and heat, pleasure and pain, free from attachment — | ☐ | ☐ | ☐ |
|  | 12.19 | Silent, satisfied with anything | — equal in blame and praise, silent, content with anything, homeless, of steady mind, full of devotion — that man is dear to me. | ☐ | ☐ | ☐ |
|  | 12.20 | They who follow this immortal dharma are dearest | But those who follow this immortal dharma, as declared, with faith, making me the supreme goal — those devotees are exceedingly dear to me. | ☐ | ☐ | ☐ |


### Chapter 13 — Kṣetra-Kṣetrajña-Vibhāga Yoga · verses 13.01–13.34 · 34 titles, 1 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 13.01 | The body is the field | The Blessed Lord said: This body, O son of Kuntī, is called the field; he who knows it, the wise call the knower of the field. | ☐ | ☐ | ☐ |
|  | 13.02 | Know me as the knower | Know me also as the knower of the field in all fields, O Bhārata; the knowledge of the field and its knower is deemed by me true knowledge. | ☐ | ☐ | ☐ |
|  | 13.03 | Hear in brief what the field is | What the field is, what it is like, what its modifications, from what it arises, and who he is and what his powers — hear all this from me in brief. | ☐ | ☐ | ☐ |
|  | 13.04 | Sung by the seers | Sung by the seers in many ways, in diverse meters, and in the aphorisms of Brahman, with reasons, well-decided — | ☐ | ☐ | ☐ |
|  | 13.05 | The elements of the field | — the great elements, ego, intellect, the unmanifest, the ten senses and the one, the five objects of the senses, | ☐ | ☐ | ☐ |
|  | 13.06 | Desire and aversion | — desire, aversion, pleasure, pain, the body, consciousness and constancy: this is the field, in brief, with its modifications. | ☐ | ☐ | ☐ |
|  | 13.07 | Humility, non-violence, service to the teacher | Humility, modesty, non-violence, forbearance, uprightness, service to the teacher, purity, steadfastness, self-control, | ☐ | ☐ | ☐ |
|  | 13.08 | Seeing the misery of birth | — dispassion toward the objects of the senses, absence of ego, and the perception of the evil of suffering in birth, death, old age and disease, | ☐ | ☐ | ☐ |
|  | 13.09 | Non-attachment and evenness | — non-attachment, non-clinging to son, wife and home, constant even-mindedness toward the pleasant and unpleasant, | ☐ | ☐ | ☐ |
|  | 13.10 | Unwavering devotion, delight in solitude | — unwavering devotion to me through undivided yoga, delight in solitude, distaste for the company of men, | ☐ | ☐ | ☐ |
|  | 13.11 | The aim of truth-knowledge | — constant commitment to Self-knowledge, and insight into the purpose of the knowledge of truth: this is declared knowledge; what is other than this is ignorance. | ☐ | ☐ | ☐ |
|  | 13.12 | The knowable declared | I shall declare the object of knowledge, knowing which one tastes immortality — the beginningless supreme Brahman, which is called neither being nor non-being. | ☐ | ☐ | ☐ |
|  | 13.13 | All hands, all feet | With hands and feet everywhere, with eyes, heads and faces everywhere, with ears everywhere — it stands, pervading all in the world. | ☐ | ☐ | ☐ |
|  | 13.14 | Without senses, yet the enjoyer | Appearing with all the attributes of the senses, yet devoid of all senses; unattached, yet upholding all; without guṇas, yet enjoying the guṇas. | ☐ | ☐ | ☐ |
|  | 13.15 | Within and without, far and near | It is within and without all beings; it is unmoving and moving; being subtle, it is unknowable — it is far away, and yet near. | ☐ | ☐ | ☐ |
|  | 13.16 | Undivided in the divided | It is undivided, yet appears as if divided among beings; know it as the supporter of beings, the devourer and the creator. | ☐ | ☐ | ☐ |
|  | 13.17 | The light of lights | It is the light of lights, declared beyond darkness — knowledge, the object of knowledge, and the goal of knowledge, seated in the heart of all. | ☐ | ☐ | ☐ |
|  | 13.18 | The field, knowledge and the knowable | Thus the field, knowledge and the knowable have been declared in brief; my devotee, knowing this, attains my being. | ☐ | ☐ | ☐ |
|  | 13.19 | Both prakṛti and puruṣa are beginningless | Know prakṛti and puruṣa both as beginningless; and know the modifications and the guṇas as born of prakṛti. | ☐ | ☐ | ☐ |
|  | 13.20 | Agency and enjoyment | Prakṛti is declared the cause in the agency of effect and cause; puruṣa is declared the cause of the enjoyment of pleasure and pain. | ☐ | ☐ | ☐ |
|  | 13.21 | Attachment to the guṇas causes birth | Puruṣa, seated in prakṛti, enjoys the guṇas born of prakṛti; attachment to the guṇas is the cause of birth in good and evil wombs. | ☐ | ☐ | ☐ |
|  | 13.22 | The witness and Lord | The witness, the approver, the sustainer, the enjoyer, the great Lord — and called the supreme Self: this supreme puruṣa in the body. | ☐ | ☐ | ☐ |
|  | 13.23 | Knowing these two, he is not born again | He who thus knows puruṣa and prakṛti with its guṇas — whatever his way of life, he is not born again. | ☐ | ☐ | ☐ |
| ⚑ | 13.24 | The three paths | Some see the Self within themselves by meditation, through their own mind; others by the yoga of knowledge; still others by the yoga of action. | ☐ | ☐ | ☐ |
|  | 13.25 | The path of hearing | Others, not knowing, worship after hearing from others; and they too cross beyond death, devoted to what they have heard. | ☐ | ☐ | ☐ |
|  | 13.26 | All beings arise from union of field and its knower | Whatever being is born, moving or unmoving — know it, O bull of the Bhāratas, to be from the union of the field and its knower. | ☐ | ☐ | ☐ |
|  | 13.27 | Seeing the Lord alike in all, he truly sees | He who sees the supreme Lord standing equally in all beings, not perishing as they perish — he truly sees. | ☐ | ☐ | ☐ |
|  | 13.28 | He does not harm the Self by the self | For seeing the Lord equally established everywhere, he does not harm the Self by the self; therefore he attains the supreme goal. | ☐ | ☐ | ☐ |
|  | 13.29 | Prakṛti acts, the Self does nothing | He who sees that all actions are performed by prakṛti, and the Self as the non-doer — he truly sees. | ☐ | ☐ | ☐ |
|  | 13.30 | The one in the many | When he sees the manifold states of beings resting in the One and spread out from it alone — then he attains Brahman. | ☐ | ☐ | ☐ |
|  | 13.31 | Without beginning or guṇas, it does not act | O son of Kuntī, because it is beginningless and without guṇas, this supreme Self is imperishable — though dwelling in the body, it neither acts nor is stained. | ☐ | ☐ | ☐ |
|  | 13.32 | As space is unstained | As the all-pervading space is not stained, being subtle, so the Self, present in every body, is not stained. | ☐ | ☐ | ☐ |
|  | 13.33 | The sun and the field | As the one sun illumines this whole world, so the knower of the field illumines the whole field, O Bhārata. | ☐ | ☐ | ☐ |
|  | 13.34 | Seeing field and knower apart brings freedom | Those who, with the eye of knowledge, see the distinction between the field and its knower, and the liberation from prakṛti — they reach the supreme. | ☐ | ☐ | ☐ |

* ⚑ **13.24** — number unsupported. Advisory text: “The three paths”


### Chapter 14 — Guṇa-Traya-Vibhāga Yoga · verses 14.01–14.27 · 27 titles, 2 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 14.01 | The highest knowledge | The Blessed Lord said: I will again declare the supreme knowledge, the best of all knowledges — knowing which all the sages have gone from here to the highest perfection. | ☐ | ☐ | ☐ |
|  | 14.02 | Like me: unborn at creation, untroubled at dissolution | Taking refuge in this knowledge, they attain unity with my being; they are not born at creation, nor are they troubled at dissolution. | ☐ | ☐ | ☐ |
|  | 14.03 | Brahman is my womb; I place the seed | My womb is the great Brahman; in it I place the seed — from that comes the birth of all beings, O Bhārata. | ☐ | ☐ | ☐ |
|  | 14.04 | All wombs, my seed | Whatever forms arise in any womb, O son of Kuntī — the great Brahman is their womb, and I am the father who gives the seed. | ☐ | ☐ | ☐ |
| ⚑ | 14.05 | The three qualities | Sattva, rajas and tamas — the qualities born of prakṛti — bind the imperishable embodied one in the body, O mighty-armed one. | ☐ | ☐ | ☐ |
|  | 14.06 | Sattva binds by happiness and knowledge | Of these, sattva, being pure, illumines and is free from disease; it binds by attachment to happiness and to knowledge, O sinless one. | ☐ | ☐ | ☐ |
|  | 14.07 | Rajas binds by attachment to action | Know rajas as of the nature of passion, born of thirst and attachment; it binds the embodied one by attachment to action, O son of Kuntī. | ☐ | ☐ | ☐ |
|  | 14.08 | Tamas binds by sloth and sleep | Know tamas as born of ignorance, deluding all embodied beings; it binds by heedlessness, sloth and sleep, O Bhārata. | ☐ | ☐ | ☐ |
|  | 14.09 | Each binds to its object | Sattva attaches to happiness, rajas to action, O Bhārata; tamas, covering knowledge, attaches to heedlessness. | ☐ | ☐ | ☐ |
|  | 14.10 | The guṇas overpower one another | O Bhārata, sattva arises by overpowering rajas and tamas; so rajas arises by overpowering sattva and tamas; and so tamas, overpowering both. | ☐ | ☐ | ☐ |
|  | 14.11 | When sattva grows | When the light of knowledge shines through all the gates of this body, then know that sattva has grown. | ☐ | ☐ | ☐ |
|  | 14.12 | When rajas grows | Greed, activity, the undertaking of works, restlessness and longing arise when rajas has grown, O bull of the Bhāratas. | ☐ | ☐ | ☐ |
|  | 14.13 | When tamas grows | Darkness, inertia, heedlessness and delusion arise when tamas has grown, O joy of the Kurus. | ☐ | ☐ | ☐ |
|  | 14.14 | Death in sattva | If the embodied one meets death when sattva prevails, he attains the pure worlds of the knowers of the highest. | ☐ | ☐ | ☐ |
|  | 14.15 | Death in rajas and tamas | Dying in rajas, one is born among those attached to action; dying in tamas, one is born in the wombs of the deluded. | ☐ | ☐ | ☐ |
|  | 14.16 | The fruits: purity, sorrow, ignorance | They say the fruit of good action is pure and sāttvic; the fruit of rajas is sorrow; the fruit of tamas is ignorance. | ☐ | ☐ | ☐ |
|  | 14.17 | Knowledge, greed and delusion, each in turn | From sattva arises knowledge; from rajas, greed; from tamas arise heedlessness and delusion, and also ignorance. | ☐ | ☐ | ☐ |
| ⚑ | 14.18 | The three destinies | Those established in sattva go upward; the rājasic stay in the middle; the tāmasic, sunk in the lowest qualities, go downward. | ☐ | ☐ | ☐ |
|  | 14.19 | Beyond the guṇas | When the seer perceives no agent other than the guṇas, and knows what is beyond them, he attains my being. | ☐ | ☐ | ☐ |
|  | 14.20 | Freed from the guṇas | Transcending these three guṇas that give rise to the body, freed from birth, death, old age and sorrow, the embodied one tastes immortality. | ☐ | ☐ | ☐ |
|  | 14.21 | The marks of the transcendent | Arjuna said: By what marks is he who has transcended these three guṇas known, O Lord? What is his conduct, and how does he transcend them? | ☐ | ☐ | ☐ |
|  | 14.22 | Neither hates them nor longs for them | The Blessed Lord said: He who neither hates illumination, activity and delusion when they arise, nor longs for them when they cease, O Pāṇḍava, | ☐ | ☐ | ☐ |
|  | 14.23 | Seated like a witness | — seated as one indifferent, unshaken by the guṇas, thinking 'the guṇas act' and abiding unmoved — | ☐ | ☐ | ☐ |
|  | 14.24 | Even in pleasure and pain; clod, stone and gold alike | — equal in pleasure and pain, self-abiding, to whom a clod, stone and gold are alike, equal to the pleasant and unpleasant, firm, equal in praise and blame — | ☐ | ☐ | ☐ |
|  | 14.25 | Equal in honour and dishonour | — equal in honour and dishonour, equal to friend and foe, renouncing all undertakings — he is said to have transcended the guṇas. | ☐ | ☐ | ☐ |
|  | 14.26 | Unwavering devotion carries one beyond | He who serves me with the unwavering yoga of devotion — transcending these guṇas, he becomes fit for Brahman. | ☐ | ☐ | ☐ |
|  | 14.27 | I am the support | For I am the support of Brahman, of immortality and the imperishable, of eternal dharma and of absolute bliss. | ☐ | ☐ | ☐ |

* ⚑ **14.05** — number unsupported. Advisory text: “The three qualities”
* ⚑ **14.18** — number unsupported. Advisory text: “The three destinies”


### Chapter 15 — Puruṣottama Yoga · verses 15.01–15.20 · 20 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 15.01 | The aśvattha tree | The Blessed Lord said: They speak of the imperishable aśvattha with its root above and branches below; the Vedas are its leaves — he who knows it is a knower of the Vedas. | ☐ | ☐ | ☐ |
|  | 15.02 | Branches spread above and below | Its branches spread above and below, nourished by the guṇas, with sense-objects as their shoots; and below its roots stretch down, binding to action in the world of men. | ☐ | ☐ | ☐ |
|  | 15.03 | Cut this rooted tree with detachment | Its true form is not perceived here, nor its end, nor its beginning, nor its support; having cut this firmly-rooted aśvattha with the strong axe of detachment, | ☐ | ☐ | ☐ |
|  | 15.04 | Seek the supreme goal | — then that state must be sought, going to which none returns; I take refuge in that primal Person from whom flows the ancient course. | ☐ | ☐ | ☐ |
|  | 15.05 | Free of pride and delusion, they reach it | Free from pride and delusion, having conquered the fault of attachment, ever established in the Self, desires turned away — freed from the pairs known as pleasure and pain, the undeluded reach … | ☐ | ☐ | ☐ |
|  | 15.06 | The supreme abode | Neither the sun nor the moon nor fire illumines that abode of mine; having gone there, none returns — that is my supreme abode. | ☐ | ☐ | ☐ |
|  | 15.07 | As if an eternal portion | An eternal portion of myself, become a living soul in the world of life, draws around itself the senses, of which the mind is the sixth, which abide in prakṛti. | ☐ | ☐ | ☐ |
|  | 15.08 | The wandering soul | When the lord of the body takes up a body, and when he departs from it, he goes taking these with him, as the wind carries fragrance from its seat. | ☐ | ☐ | ☐ |
|  | 15.09 | Enjoying through the senses | Presiding over hearing, touch, sight, taste and smell, and the mind, he enjoys the sense-objects. | ☐ | ☐ | ☐ |
|  | 15.10 | Who sees the soul, and who does not? | The deluded do not see him as he departs, dwells, or enjoys, or as he is joined with the guṇas; but those with the eye of knowledge see him. | ☐ | ☐ | ☐ |
|  | 15.11 | The striving yogis | The striving yogis see him established in the Self; but the undisciplined, though striving, do not see him, lacking true understanding. | ☐ | ☐ | ☐ |
|  | 15.12 | I am the light | The light in the sun, which illumines the whole world, and that in the moon and in fire — know that light as mine. | ☐ | ☐ | ☐ |
|  | 15.13 | I sustain all | Entering the earth I sustain all beings with my energy; becoming the sap-laden moon I nourish all herbs. | ☐ | ☐ | ☐ |
|  | 15.14 | The fire of digestion | Becoming the fire of digestion in the bodies of living beings, joined with the in-breath and out-breath, I cook the four kinds of food. | ☐ | ☐ | ☐ |
|  | 15.15 | In the heart of all | I am seated in the heart of all; from me come memory, knowledge and their removal; by all the Vedas I alone am to be known — I am the author of Vedānta and the knower of the Vedas. | ☐ | ☐ | ☐ |
|  | 15.16 | The perishable and the imperishable | There are two persons in this world: the perishable and the imperishable. The perishable is all beings; the unchanging is called the imperishable. | ☐ | ☐ | ☐ |
|  | 15.17 | The supreme person | But there is another, the supreme Person, called the supreme Self — the eternal Lord who, entering the three worlds, sustains them. | ☐ | ☐ | ☐ |
|  | 15.18 | Why I am Puruṣottama | Since I transcend the perishable and am higher than the imperishable, I am known in the world and in the Veda as the highest Person. | ☐ | ☐ | ☐ |
|  | 15.19 | The knower of the highest | He who, undeluded, knows me as the highest Person — knowing all, he worships me with all his being, O Bhārata. | ☐ | ☐ | ☐ |
|  | 15.20 | The secret teaching | Thus this most secret teaching has been declared by me, O sinless one; understanding this, one becomes wise and has accomplished all, O Bhārata. | ☐ | ☐ | ☐ |


### Chapter 16 — Daivāsura-Sampad-Vibhāga Yoga · verses 16.01–16.24 · 24 titles, 1 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 16.01 | Fearlessness and purity | The Blessed Lord said: Fearlessness, purity of heart, steadfastness in knowledge and yoga, charity, self-control, sacrifice, study of scripture, austerity and uprightness, | ☐ | ☐ | ☐ |
|  | 16.02 | Non-violence and truth | — non-violence, truth, freedom from anger, renunciation, peace, absence of slander, compassion toward beings, non-covetousness, gentleness, modesty and steadiness — | ☐ | ☐ | ☐ |
|  | 16.03 | Vigour and forgiveness | — vigour, forgiveness, fortitude, purity, freedom from malice and from pride — these belong to one born to the divine destiny, O Bhārata. | ☐ | ☐ | ☐ |
| ⚑ | 16.04 | Six marks of the demoniac | Hypocrisy, arrogance, self-conceit, anger, harshness and ignorance belong to one born to the demoniac destiny, O Pārtha. | ☐ | ☐ | ☐ |
|  | 16.05 | Liberation and bondage | The divine endowment leads to liberation, the demoniac to bondage — grieve not, O Pāṇḍava, for you are born to the divine destiny. | ☐ | ☐ | ☐ |
|  | 16.06 | The two creations | There are two creations of beings in this world — the divine and the demoniac; the divine has been described at length — now hear from me of the demoniac, O Pārtha. | ☐ | ☐ | ☐ |
|  | 16.07 | Without truth or purity | The demoniac do not know right action or renunciation; there is no purity, no conduct, no truth in them. | ☐ | ☐ | ☐ |
|  | 16.08 | The godless world-view | They say the world is unreal, without foundation, without a Lord — produced by mutual union, born of lust — what else? | ☐ | ☐ | ☐ |
|  | 16.09 | The ruined souls | Holding this view, these ruined souls of little understanding perform cruel deeds, enemies of the world, for its destruction. | ☐ | ☐ | ☐ |
|  | 16.10 | Insatiable desire, hypocrisy and pride | Given to insatiable desire, full of hypocrisy, pride and arrogance, holding false views through delusion, they act with impure resolves. | ☐ | ☐ | ☐ |
|  | 16.11 | Cares that end only in death | Given to boundless cares ending only in death, intent on the enjoyment of desires, thinking 'this is all' — | ☐ | ☐ | ☐ |
|  | 16.12 | The fetters of hope | — bound by hundreds of fetters of hope, given to desire and anger, they strive to amass wealth by unjust means for the gratification of lust. | ☐ | ☐ | ☐ |
|  | 16.13 | This I gained; more shall be mine | 'This I gained today; this wish I shall fulfil; this wealth is mine — and more shall be mine,' they think — | ☐ | ☐ | ☐ |
|  | 16.14 | I am the lord | 'I have slain this enemy, and I will slay others too; I am the lord, I am the enjoyer, I am accomplished, powerful and happy,' | ☐ | ☐ | ☐ |
|  | 16.15 | Who else is like me? | 'I am rich and well-born; who else is like me? I will sacrifice, I will give, I will rejoice' — thus deluded by ignorance. | ☐ | ☐ | ☐ |
|  | 16.16 | The net of delusion | Bewildered by many thoughts, wrapped in the net of delusion, devoted to sensual pleasures, they fall into a foul hell. | ☐ | ☐ | ☐ |
|  | 16.17 | Sacrifice in name only | Self-conceited, stubborn, filled with the pride of wealth, they perform sacrifices in name only, with hypocrisy, not according to the rule. | ☐ | ☐ | ☐ |
|  | 16.18 | Hatred toward the Lord | Filled with ego, power, pride, desire and anger, hating me in their own and in others' bodies, these malicious beings — | ☐ | ☐ | ☐ |
|  | 16.19 | Cast again and again | — these evil, cruel haters, the vilest of men, I cast again and again into demoniac wombs in the rounds of rebirth. | ☐ | ☐ | ☐ |
|  | 16.20 | The lowest state | Entering a demoniac womb, deluded birth after birth, never reaching me, they sink to the lowest state, O son of Kuntī. | ☐ | ☐ | ☐ |
|  | 16.21 | The three gates of hell | Threefold is this gate of hell, the destroyer of the self: desire, anger and greed — therefore abandon these three. | ☐ | ☐ | ☐ |
|  | 16.22 | Freed from the gates | Freed from these three gates of darkness, O son of Kuntī, a man works for his own good and attains the supreme goal. | ☐ | ☐ | ☐ |
|  | 16.23 | Casting scripture aside | He who, casting aside the ordinance of scripture, acts by the impulse of desire — he attains neither perfection, nor happiness, nor the supreme goal. | ☐ | ☐ | ☐ |
|  | 16.24 | Let scripture be your guide | Therefore let the scripture be your authority in determining what is to be done and not done; knowing what is ordained by the scripture, act here accordingly. | ☐ | ☐ | ☐ |

* ⚑ **16.04** — number unsupported. Advisory text: “Six marks of the demoniac”


### Chapter 17 — Śraddhā-Traya-Vibhāga Yoga · verses 17.01–17.28 · 28 titles, 0 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 17.01 | Faithful worship while setting aside scripture's rule | Arjuna said: Those who, casting aside the ordinance of scripture, worship with faith — what is their state, O Kṛṣṇa? Is it sattva, rajas or tamas? | ☐ | ☐ | ☐ |
|  | 17.02 | The threefold faith | The Blessed Lord said: The faith of embodied beings is threefold, born of their own nature — sāttvic, rājasic and tāmasic; hear of it. | ☐ | ☐ | ☐ |
|  | 17.03 | Faith shapes the person | The faith of each is according to his nature, O Bhārata; a man is made of his faith — as is his faith, so is he. | ☐ | ☐ | ☐ |
|  | 17.04 | Whom each worships | The sāttvic worship the gods; the rājasic the yakṣas and rākṣasas; and others — the tāmasic — worship ghosts and the hosts of spirits. | ☐ | ☐ | ☐ |
|  | 17.05 | Austerity not prescribed by scripture | The men who practise terrible austerities not ordained by scripture, full of hypocrisy and ego, impelled by the force of desire and attachment, | ☐ | ☐ | ☐ |
|  | 17.06 | Torturing me within | — foolishly tormenting the elements of the body and also me dwelling within the body — know them as of demoniac resolves. | ☐ | ☐ | ☐ |
|  | 17.07 | Food, sacrifice, austerity and giving are threefold | Food, too, dear to each, is threefold; and sacrifice, austerity and gifts — hear their distinction. | ☐ | ☐ | ☐ |
|  | 17.08 | The sāttvic food | Foods that increase life, purity, strength, health, joy and cheer — savoury, smooth, firm and agreeable — are dear to the sāttvic. | ☐ | ☐ | ☐ |
|  | 17.09 | The rājasic food | Foods that are bitter, sour, salty, very hot, pungent, dry and burning — causing pain, grief and disease — are dear to the rājasic. | ☐ | ☐ | ☐ |
|  | 17.10 | The tāmasic food | Stale, tasteless, putrid and leftover food, and impure leavings — such food is dear to the tāmasic. | ☐ | ☐ | ☐ |
|  | 17.11 | The sāttvic sacrifice | The sacrifice ordained by scripture, offered without desire for fruit by those who think 'this must be performed' — that is sāttvic. | ☐ | ☐ | ☐ |
|  | 17.12 | The rājasic sacrifice | But the sacrifice offered seeking fruit and for the sake of display, O best of the Bhāratas — know that as rājasic. | ☐ | ☐ | ☐ |
|  | 17.13 | The tāmasic sacrifice | The sacrifice without rule, without food-gifts, without mantra, without fees, devoid of faith — is declared tāmasic. | ☐ | ☐ | ☐ |
|  | 17.14 | Austerity of the body | Worship of the gods, the twice-born, teachers and the wise; purity, uprightness, chastity and non-violence — this is the austerity of the body. | ☐ | ☐ | ☐ |
|  | 17.15 | Austerity of speech | Speech that causes no distress, that is truthful, pleasant and beneficial, and the regular study of scripture — this is the austerity of speech. | ☐ | ☐ | ☐ |
|  | 17.16 | Austerity of the mind | Serenity of mind, gentleness, silence, self-control, and purity of heart — this is called the austerity of the mind. | ☐ | ☐ | ☐ |
|  | 17.17 | The sāttvic austerity | This threefold austerity, performed with supreme faith by the steadfast, without desire for fruit — is declared sāttvic. | ☐ | ☐ | ☐ |
|  | 17.18 | The rājasic austerity | Austerity performed for honour, reverence and worship, and with hypocrisy — is here declared rājasic, unstable and transitory. | ☐ | ☐ | ☐ |
|  | 17.19 | The tāmasic austerity | Austerity performed with foolish obstinacy, with self-torture, or to ruin another — is declared tāmasic. | ☐ | ☐ | ☐ |
|  | 17.20 | The sāttvic gift | The gift given because it ought to be given, to one who can do nothing in return, at the right place and time, to a worthy person — is deemed sāttvic. | ☐ | ☐ | ☐ |
|  | 17.21 | The rājasic gift | But the gift given expecting a return, or seeking fruit again, or reluctantly — is deemed rājasic. | ☐ | ☐ | ☐ |
|  | 17.22 | The tāmasic gift | The gift given at the wrong place and time, to unworthy persons, without respect and with contempt — is declared tāmasic. | ☐ | ☐ | ☐ |
|  | 17.23 | Om Tat Sat: Brahman's threefold designation | Om Tat Sat — this is the threefold designation of Brahman; by it were ordained of old the brāhmaṇas, the Vedas and the sacrifices. | ☐ | ☐ | ☐ |
|  | 17.24 | Om: beginning prescribed sacred acts | Therefore, uttering Om, the acts of sacrifice, gift and austerity ordained by rule are begun, ever, by the knowers of Brahman. | ☐ | ☐ | ☐ |
|  | 17.25 | Tat: without desire for fruit | Uttering Tat, without desiring fruit, are the acts of sacrifice, austerity and the various acts of giving performed by seekers of liberation. | ☐ | ☐ | ☐ |
|  | 17.26 | Sat: reality and goodness | Sat is used in the sense of reality and goodness, and also in auspicious works, O Pārtha. | ☐ | ☐ | ☐ |
|  | 17.27 | Firmness is also Sat | Steadfastness in sacrifice, austerity and giving is also called Sat; and action for the sake of that is called Sat. | ☐ | ☐ | ☐ |
|  | 17.28 | Faithless acts are Asat | Whatever is offered or given without faith, whatever austerity is practised and whatever action is done without faith — is called Asat, O Pārtha; it is naught here or hereafter. | ☐ | ☐ | ☐ |


### Chapter 18 — Mokṣa-Sannyāsa Yoga · verses 18.01–18.78 · 78 titles, 2 flagged

| ☐ | Verse | Title | The verse says (literal) | keep | revise | fix |
|---|---|---|---|:-:|:-:|:-:|
|  | 18.01 | Arjuna asks how sannyāsa differs from tyāga | Arjuna said: I wish to know the truth of renunciation, O mighty-armed one, and of abandonment, O Hṛṣīkeśa, and the difference between the two, O slayer of Keśin. | ☐ | ☐ | ☐ |
|  | 18.02 | Sannyāsa drops desire-led acts; tyāga drops all fruits | The Blessed Lord said: The wise call the giving up of desired actions renunciation; the abandonment of all fruits of action the wise call tyāga. | ☐ | ☐ | ☐ |
|  | 18.03 | The schools of thought | Some wise men say action is to be given up as evil; others say sacrifice, gift and austerity are not to be given up. | ☐ | ☐ | ☐ |
|  | 18.04 | Tyāga is of three kinds | Hear my certain conclusion on tyāga, O best of the Bhāratas; for tyāga, O tiger among men, is declared to be of three kinds. | ☐ | ☐ | ☐ |
|  | 18.05 | Sacrifice, gift and austerity are not to be given up | The acts of sacrifice, gift and austerity are not to be given up; they must be performed, for they purify even the wise. | ☐ | ☐ | ☐ |
|  | 18.06 | Perform these acts unattached; renounce their fruits | But even these actions should be performed, giving up attachment and the fruits, O Pārtha — this is my certain and best conviction. | ☐ | ☐ | ☐ |
|  | 18.07 | Giving up duty through delusion is tāmasic | The renunciation of prescribed action is not proper; abandoning it through delusion is declared tāmasic. | ☐ | ☐ | ☐ |
|  | 18.08 | Giving it up from fear of pain is rājasic | He who gives up action because it brings pain, from fear of bodily suffering — performing the rājasic abandonment, he does not gain the fruit of renunciation. | ☐ | ☐ | ☐ |
|  | 18.09 | Doing it because it ought to be done | But the prescribed action done because it ought to be done, O Arjuna, giving up attachment and fruit — that is deemed sāttvic abandonment. | ☐ | ☐ | ☐ |
|  | 18.10 | Unpleasant acts not hated, pleasant ones not clung to | The sāttvic renouncer, endowed with sattva and firm understanding, with doubts cut away, neither hates unpleasant action nor clings to pleasant. | ☐ | ☐ | ☐ |
|  | 18.11 | No one can give up all action | Indeed, the embodied one cannot give up all actions entirely; but he who gives up the fruit of action is called a true renouncer. | ☐ | ☐ | ☐ |
| ⚑ | 18.12 | Three kinds of fruit | The threefold fruit of action — pleasant, unpleasant and mixed — comes after death to the non-renouncer; but never to the renouncer. | ☐ | ☐ | ☐ |
|  | 18.13 | Learn the five causes | Learn from me, O mighty-armed one, these five causes for the accomplishment of all actions, declared in the philosophy of the end of action: | ☐ | ☐ | ☐ |
|  | 18.14 | Destiny, the fifth cause | — the seat, the agent, the instruments of various kinds, the various separate efforts, and destiny, the fifth. | ☐ | ☐ | ☐ |
|  | 18.15 | Whatever action a person undertakes | Whatever action a man undertakes with body, speech or mind — rightly or wrongly — these five are its causes. | ☐ | ☐ | ☐ |
|  | 18.16 | Seeing the Self alone as the doer is mistaken | That being so, he who — wrong-minded and with imperfect understanding — sees the Self alone as the agent, does not truly see. | ☐ | ☐ | ☐ |
|  | 18.17 | Ego-free, he neither kills nor is bound | He whose mind is free from ego, whose intellect is not stained — though he slays these worlds, he slays not, nor is bound. | ☐ | ☐ | ☐ |
|  | 18.18 | Knowledge, action, agent | Knowledge, the known and the knower — the threefold impulse to action; the instrument, the act and the agent — the threefold basis of action. | ☐ | ☐ | ☐ |
|  | 18.19 | Knowledge, action, agent: threefold by the guṇas | Knowledge, action and agent are declared threefold by the distinction of the guṇas — hear them as they are in the enumeration of the guṇas. | ☐ | ☐ | ☐ |
|  | 18.20 | The sāttvic knowledge | That knowledge by which one sees one imperishable being in all beings, undivided in the divided — know that as sāttvic. | ☐ | ☐ | ☐ |
|  | 18.21 | Rājasic knowledge sees beings as separate | But the knowledge that sees manifold and separate beings in all beings — know that as rājasic. | ☐ | ☐ | ☐ |
|  | 18.22 | Irrational, clinging to a part | And the knowledge that clings to one single effect as if it were the whole, without reason, without truth, trivial — is declared tāmasic. | ☐ | ☐ | ☐ |
|  | 18.23 | Sāttvic action seeks no fruit | Action done as prescribed, without attachment, without desire or aversion, by one who seeks no fruit — is declared sāttvic. | ☐ | ☐ | ☐ |
|  | 18.24 | Rājasic action serves desire | But action done with great effort, by one seeking the fulfilment of desires or full of ego — is declared rājasic. | ☐ | ☐ | ☐ |
|  | 18.25 | Done in delusion | Action begun through delusion, heedless of consequence, of ruin and injury, and of one's own capacity — is declared tāmasic. | ☐ | ☐ | ☐ |
|  | 18.26 | The sāttvic agent | The agent free from attachment, free from ego, firm and zealous, unmoved by success and failure — is declared sāttvic. | ☐ | ☐ | ☐ |
|  | 18.27 | The rājasic agent | The agent full of passion, longing for the fruit of action, greedy, cruel, impure, moved by joy and sorrow — is declared rājasic. | ☐ | ☐ | ☐ |
|  | 18.28 | Deceitful, lazy, stubborn | The agent undisciplined, vulgar, obstinate, deceitful, malicious, lazy, despondent and procrastinating — is declared tāmasic. | ☐ | ☐ | ☐ |
| ⚑ | 18.29 | Three kinds of intellect and fortitude | Hear the threefold distinction of intellect and fortitude, declared fully and separately, by the guṇas, O Dhanañjaya. | ☐ | ☐ | ☐ |
|  | 18.30 | The sāttvic intellect | O Pārtha, the intellect that knows action and inaction, right and wrong, fear and fearlessness, bondage and liberation — is sāttvic. | ☐ | ☐ | ☐ |
|  | 18.31 | The rājasic intellect | The intellect by which one understands dharma and adharma, and what ought and ought not to be done, incorrectly — that, O Pārtha, is rājasic. | ☐ | ☐ | ☐ |
|  | 18.32 | Wrapped in darkness | O Pārtha, the intellect that, enveloped in darkness, takes wrong for right and sees all things perversely — is tāmasic. | ☐ | ☐ | ☐ |
|  | 18.33 | The sāttvic fortitude | The unwavering fortitude by which one holds, through yoga, the activities of the mind, breath and senses — that, O Pārtha, is sāttvic. | ☐ | ☐ | ☐ |
|  | 18.34 | The rājasic fortitude | But the fortitude by which one holds to duty, pleasure and wealth, attached and desiring fruit — that, O Arjuna, is rājasic, O Pārtha. | ☐ | ☐ | ☐ |
|  | 18.35 | Holds on to sleep and fear | The fortitude by which a dull man does not give up sleep, fear, grief, despair and arrogance — that, O Pārtha, is tāmasic. | ☐ | ☐ | ☐ |
|  | 18.36 | The threefold happiness | Hear now from me, O bull of the Bhāratas, the threefold happiness — that in which one rejoices by practice and reaches the end of suffering. | ☐ | ☐ | ☐ |
|  | 18.37 | Poison at first, nectar at the end | That which is like poison at first and nectar at the end — born of the clarity of the intellect concerning the Self — is declared sāttvic happiness. | ☐ | ☐ | ☐ |
|  | 18.38 | Sweet at first, poison at last | The happiness from the contact of the senses with their objects, nectar at first and poison at the end — is declared rājasic. | ☐ | ☐ | ☐ |
|  | 18.39 | Delusive from beginning to end | The happiness that deludes the soul at first and at the end, born of sleep, sloth and heedlessness — is declared tāmasic. | ☐ | ☐ | ☐ |
|  | 18.40 | No one free of the guṇas | There is no being on earth, nor among the gods in heaven, free from these three guṇas born of prakṛti. | ☐ | ☐ | ☐ |
|  | 18.41 | The fourfold duties | The duties of brāhmaṇas, kṣatriyas, vaiśyas and śūdras are divided according to the qualities born of their own nature, O scorcher of foes. | ☐ | ☐ | ☐ |
|  | 18.42 | The brāhmaṇa's duty, born of his nature | Tranquillity, self-control, austerity, purity, patience, uprightness, knowledge, wisdom and faith — the duty of the brāhmaṇa, born of his nature. | ☐ | ☐ | ☐ |
|  | 18.43 | The kṣatriya's duty, born of his nature | Valour, splendour, fortitude, skill, not fleeing in battle, generosity and lordship — the duty of the kṣatriya, born of his nature. | ☐ | ☐ | ☐ |
|  | 18.44 | The vaiśya's and the śūdra's duty | Agriculture, cattle-rearing and trade — the duty of the vaiśya, born of his nature; and service — the duty of the śūdra. | ☐ | ☐ | ☐ |
|  | 18.45 | Perfection through duty | Devoted to his own duty, a man attains perfection — hear how one who delights in his own work attains perfection. | ☐ | ☐ | ☐ |
|  | 18.46 | Worship the source through one's own work | Worshipping, through his own duty, the source of all beings, by whom all this is pervaded — a man attains perfection. | ☐ | ☐ | ☐ |
|  | 18.47 | One's own duty is better | Better is one's own dharma, though imperfect, than another's well-performed; doing the work born of his own nature, a man incurs no sin. | ☐ | ☐ | ☐ |
|  | 18.48 | All undertakings have defects | One should not abandon one's natural work, O son of Kuntī, though it be faulty; for all undertakings are covered with fault, as fire with smoke. | ☐ | ☐ | ☐ |
|  | 18.49 | Attaining freedom from action | With intellect unattached everywhere, self-conquered and free from desire, one attains the supreme perfection of freedom from action through renunciation. | ☐ | ☐ | ☐ |
|  | 18.50 | How one reaches Brahman | Learn from me in brief, O son of Kuntī, how one who has attained this perfection reaches Brahman — that supreme state of knowledge. | ☐ | ☐ | ☐ |
|  | 18.51 | Renouncing sense-objects, desire and aversion | Endowed with pure intellect, restraining the self with fortitude, giving up sound and the other objects, casting aside desire and aversion, | ☐ | ☐ | ☐ |
|  | 18.52 | Solitude, little food, restrained speech | — dwelling in solitude, eating little, controlling speech, body and mind, ever engaged in meditation and contemplation, taking refuge in dispassion, | ☐ | ☐ | ☐ |
|  | 18.53 | Freed from ego, power and possessiveness | — free from ego, power, pride, desire, anger and possessiveness, tranquil, no longer claiming 'mine' — such a one becomes fit for Brahman. | ☐ | ☐ | ☐ |
|  | 18.54 | The Brahman-realised one neither grieves nor desires | Become Brahman, serene of soul, he neither grieves nor desires; equal to all beings, he attains supreme devotion to me. | ☐ | ☐ | ☐ |
|  | 18.55 | Devotion reveals me in truth | By that devotion he knows me in truth, who and what I am; knowing me in truth, he enters me immediately. | ☐ | ☐ | ☐ |
|  | 18.56 | By my grace, the eternal state | Performing all actions ever, taking refuge in me, he attains the eternal, imperishable state by my grace. | ☐ | ☐ | ☐ |
|  | 18.57 | Surrender all actions to me | Surrendering all actions to me in thought, making me supreme, resorting to the yoga of discernment, always fix your mind on me. | ☐ | ☐ | ☐ |
|  | 18.58 | If from ego you will not listen, you perish | With your mind on me, you shall cross all difficulties by my grace; but if from ego you will not listen, you shall be destroyed. | ☐ | ☐ | ☐ |
|  | 18.59 | Your nature will drive you | If, relying on ego, you think 'I will not fight' — vain is your resolve; your nature will compel you. | ☐ | ☐ | ☐ |
|  | 18.60 | Your own nature will compel you | Bound, O son of Kuntī, by your own action born of your nature, what through delusion you do not wish to do — that you will do helplessly. | ☐ | ☐ | ☐ |
|  | 18.61 | The Lord in every heart | The Lord dwells in the heart of all beings, O Arjuna, causing all beings to revolve by his māyā, as if mounted on a machine. | ☐ | ☐ | ☐ |
|  | 18.62 | Take refuge in him with all your being | Take refuge in him alone with all your being, O Bhārata; by his grace you shall attain supreme peace and the eternal abode. | ☐ | ☐ | ☐ |
|  | 18.63 | Reflect on it fully, then do as you will | Thus I have declared to you the knowledge, more secret than the secret; reflect on it fully, and do as you will. | ☐ | ☐ | ☐ |
|  | 18.64 | The most secret | Hear again my supreme word, the most secret of all: you are dearly loved by me, so I speak for your good. | ☐ | ☐ | ☐ |
|  | 18.65 | Fix your mind on me, be my devotee | Fix your mind on me, be my devotee, offer to me, bow to me — you shall surely come to me; I promise you truly, for you are dear to me. | ☐ | ☐ | ☐ |
|  | 18.66 | Abandon all dharmas | Abandon all dharmas and take refuge in me alone; I will free you from all sins — grieve not. | ☐ | ☐ | ☐ |
|  | 18.67 | Who should not receive this teaching | This is never to be spoken by you to one without austerity, nor to the faithless, nor to one who does not serve, nor to one who reviles me. | ☐ | ☐ | ☐ |
|  | 18.68 | The teacher's reward | He who teaches this supreme secret to my devotees with supreme devotion — having given me his highest love, he shall without doubt come to me alone. | ☐ | ☐ | ☐ |
|  | 18.69 | No one dearer | None among men does me greater service than he; and none shall be dearer to me on earth than he. | ☐ | ☐ | ☐ |
|  | 18.70 | The reward of studying | And he who studies this sacred dialogue of ours — by him I am worshipped with the sacrifice of knowledge; so I deem. | ☐ | ☐ | ☐ |
|  | 18.71 | The faithful listener is freed | Even the man who hears it with faith, without carping — freed, he attains the auspicious worlds of the virtuous. | ☐ | ☐ | ☐ |
|  | 18.72 | The Lord's question | Has this been heard by you, O Pārtha, with a one-pointed mind? Has the delusion of ignorance been destroyed, O Dhanañjaya? | ☐ | ☐ | ☐ |
|  | 18.73 | My delusion is gone; I will do your word | Arjuna said: Destroyed is my delusion; I have gained memory by your grace, O Acyuta; I stand firm, my doubt gone — I will do your word. | ☐ | ☐ | ☐ |
|  | 18.74 | Thus I heard this wondrous dialogue | Sañjaya said: Thus I heard the wondrous, thrilling dialogue of Vāsudeva and the great-souled Pārtha. | ☐ | ☐ | ☐ |
|  | 18.75 | The grace of Vyāsa | By the grace of Vyāsa I heard this supreme secret, this yoga, from Kṛṣṇa, the Lord of yoga, as he himself spoke. | ☐ | ☐ | ☐ |
|  | 18.76 | The joy of remembering | Remembering again and again this wondrous, holy dialogue of Keśava and Arjuna, O king, I rejoice again and again. | ☐ | ☐ | ☐ |
|  | 18.77 | Remembering that form, I rejoice again | And remembering again and again that most wondrous form of Hari, my wonder is great, O king — and I rejoice again and again. | ☐ | ☐ | ☐ |
|  | 18.78 | Where Kṛṣṇa and Arjuna are | Wherever Kṛṣṇa, the Lord of yoga, and Pārtha, the archer, are — there are prosperity, victory, glory and unfailing prudence; so I deem. | ☐ | ☐ | ☐ |

* ⚑ **18.12** — number unsupported. Advisory text: “Three kinds of fruit”
* ⚑ **18.29** — number unsupported. Advisory text: “Three kinds of intellect and fortitude”


## Theme titles and descriptions (not in the table above)

A theme advisory covers a run of verses and so has no single row. They are
all of one class — the summary names a speaker whom the verses address or
who is speaking, and Sanskrit drops the pronoun — so they are listed here
once, with the verse range, rather than repeated in the prose below.

### name-not-in-verse — first person: the verse is spoken by this person (37)

| ☐ | Ref | Title or description | Verses | keep | revise | fix |
|---|---|---|:-:|:-:|:-:|
|  | 1.t2 | Duryodhana sizes up both armies | 1.04–1.09 | ☐ | ☐ | ☐ |
|  | 1.t3 | Duryodhana compares the forces, then orders every division to hold position and protect Bhīṣma. | 1.10–1.11 | ☐ | ☐ | ☐ |
|  | 3.t6 | Kṛṣṇa acts although he needs nothing, lest the world fall apart. The wise likewise support others through example without disturbing their understanding. | 3.22–3.26 | ☐ | ☐ | ☐ |
|  | 3.t7 | Ego claims to be the doer; the knower sees the guṇas at work. Do not unsettle partial knowers; surrender action to Kṛṣṇa and fight without fever. | 3.27–3.30 | ☐ | ☐ | ☐ |
|  | 4.t3 | People approach Kṛṣṇa through differing aims and worship. He establishes the fourfold order, yet remains the imperishable non-doer, untainted by action. | 4.11–4.14 | ☐ | ☐ | ☐ |
|  | 5.t6 | The inwardly joyful sage, free of desire and anger, reaches Brahman-nirvāṇa. Sense and breath discipline, and knowing Kṛṣṇa as everyone’s friend, bring peace. | 5.24–5.29 | ☐ | ☐ | ☐ |
|  | 6.t3 | Prepare a quiet seat, hold the body upright and still the mind. With fearlessness, restraint and attention on Kṛṣṇa, meditation leads to peace. | 6.10–6.15 | ☐ | ☐ | ☐ |
|  | 6.t7 | Seeing the Self in all and all in Kṛṣṇa, the yogi lives in unity. Regard another’s pleasure and pain as your own: this is the highest yoga. | 6.29–6.32 | ☐ | ☐ | ☐ |
|  | 6.t11 | Effort over many births brings perfection. Be a yogi; among yogis Kṛṣṇa esteems highest the one who worships him with faith and an inwardly devoted heart. | 6.45–6.47 | ☐ | ☐ | ☐ |
|  | 7.t2 | The lower nature has eight aspects; the higher sustains life. Both give rise to beings, and everything rests on Kṛṣṇa like pearls on one thread. | 7.04–7.07 | ☐ | ☐ | ☐ |
|  | 7.t3 | Taste, light, fragrance, life, wisdom and strength reveal Kṛṣṇa’s presence. Even desire, when not opposed to dharma, belongs to this account. | 7.08–7.11 | ☐ | ☐ | ☐ |
|  | 7.t4 | The guṇas arise from Kṛṣṇa yet conceal him from the deluded. His māyā is hard to cross; refuge in him opens the way beyond it. | 7.12–7.15 | ☐ | ☐ | ☐ |
|  | 7.t6 | Desire draws people to other deities. Kṛṣṇa steadies their faith and grants the fruit, but that fruit ends; his own devotees come to him. | 7.20–7.23 | ☐ | ☐ | ☐ |
|  | 7.t8 | Freed from duality, the steadfast worship Kṛṣṇa. Seeking release from ageing and death, they know Brahman, all of adhyātma and action, and know him even at death. | 7.28–7.30 | ☐ | ☐ | ☐ |
|  | 8.t2 | The final remembered state directs departure. Therefore remember Kṛṣṇa while acting; steady practice, devotion and yogic concentration prepare the last moment. | 8.05–8.10 | ☐ | ☐ | ☐ |
|  | 8.t3 | For the imperishable goal, restrain the body’s gates and depart uttering Om. Constant, single-minded remembrance makes Kṛṣṇa easy to reach, without return. | 8.11–8.15 | ☐ | ☐ | ☐ |
|  | 8.t5 | Beyond the dissolving unmanifest is the eternal, imperishable goal. It is Kṛṣṇa’s supreme abode, reached through undivided devotion, with no return. | 8.20–8.22 | ☐ | ☐ | ☐ |
|  | 9.t2 | All beings rest in Kṛṣṇa, who remains beyond containment. Through prakṛti they dissolve and appear again, as the cycles of creation unfold. | 9.04–9.08 | ☐ | ☐ | ☐ |
|  | 9.t6 | Heaven’s pleasures end when merit is spent. Kṛṣṇa supplies what devotees lack and protects what they have; worship shapes the destination, and his devotees come to him. | 9.20–9.25 | ☐ | ☐ | ☐ |
|  | 9.t8 | Past wrongdoing or birth does not bar devoted refuge. Kṛṣṇa closes with the same four instructions found in 18.65: fix your mind, be devoted, worship and bow. | 9.30–9.34 | ☐ | ☐ | ☐ |
|  | 10.t2 | The varied qualities of beings, great seers and ancient Manus arise from Kṛṣṇa. Knowing this glory brings unwavering yoga. | 10.04–10.07 | ☐ | ☐ | ☐ |
|  | 10.t3 | Knowing Kṛṣṇa as the source, devotees rejoice together in him. He gives discerning yoga and lights the lamp that dispels ignorance. | 10.08–10.11 | ☐ | ☐ | ☐ |
|  | 10.t5 | Arjuna asks for the glories that pervade the world and the forms in which to contemplate Kṛṣṇa. He is never satisfied with hearing this nectar. | 10.16–10.18 | ☐ | ☐ | ☐ |
|  | 10.t7 | Priest, commander, ocean, seer, Om, japa, Himālaya and tree become signs of Kṛṣṇa’s presence, alongside celestial sages and the perfected. | 10.24–10.26 | ☐ | ☐ | ☐ |
|  | 10.t11 | Every being has Kṛṣṇa as its seed; his glories have no end. All splendour is a spark of him, and one part of him sustains the whole world. | 10.39–10.42 | ☐ | ☐ | ☐ |
|  | 11.t9 | Remembering careless words and casual treatment, Arjuna asks forgiveness. Before the father and teacher of the world, he prostrates and asks to be forgiven as a father forgives a son, or a friend a friend. | 11.41–11.44 | ☐ | ☐ | ☐ |
|  | 11.t10 | Joy and fear remain together. Arjuna asks for the familiar crowned, four-armed form with mace and discus, rather than the overwhelming universal form. | 11.45–11.46 | ☐ | ☐ | ☐ |
|  | 12.t2 | Kṛṣṇa swiftly delivers those who dedicate action and meditate on him. Fix mind and intellect in him: the promise is to dwell in him. | 12.06–12.08 | ☐ | ☐ | ☐ |
|  | 12.t3 | A graded path: if concentration is difficult, practise; if that is difficult, work for Kṛṣṇa. If needed, relinquish action’s fruits: renunciation brings peace. | 12.09–12.12 | ☐ | ☐ | ☐ |
|  | 13.t3 | Beginningless Brahman pervades all, beyond senses and divisions, sustaining every being. It is the light of lights in every heart; knowing this leads to Kṛṣṇa’s being. | 13.12–13.18 | ☐ | ☐ | ☐ |
|  | 14.t7 | Unwavering devotion to Kṛṣṇa crosses the guṇas and makes one fit for Brahman. He is the basis of immortality, eternal dharma and absolute bliss. | 14.26–14.27 | ☐ | ☐ | ☐ |
|  | 15.t4 | Light, nourishment, digestion, memory, knowledge and forgetfulness arise from Kṛṣṇa. Seated in every heart, he is the one to be known through the Vedas. | 15.12–15.15 | ☐ | ☐ | ☐ |
|  | 15.t5 | Beyond the perishable and imperishable stands the sustaining Supreme Person. Knowing Kṛṣṇa as Puruṣottama brings wholehearted worship and completes this secret teaching. | 15.16–15.20 | ☐ | ☐ | ☐ |
|  | 18.t12 | The Brahman-realised one is serene, equal to all, without grief or craving. Supreme devotion reveals Kṛṣṇa in truth and leads into him. | 18.54–18.55 | ☐ | ☐ | ☐ |
|  | 18.t13 | Resting in Kṛṣṇa, dedicate every act and cross difficulties by grace. An ego-driven refusal to fight is vain: one’s own nature still compels action. | 18.56–18.60 | ☐ | ☐ | ☐ |
|  | 18.t15 | Out of love, Kṛṣṇa gives the supreme secret: fix your mind on him, worship and bow. Take refuge in him alone; he promises freedom from all sin. | 18.64–18.66 | ☐ | ☐ | ☐ |
|  | 18.t16 | Do not give this teaching to one who lacks austerity or devotion, refuses to listen, or finds fault with Kṛṣṇa. Devoted teaching, study and faithful hearing are honoured; even the listener is freed. | 18.67–18.71 | ☐ | ☐ | ☐ |

### name-not-in-verse — theme summary across 2 verses: check the scene (1)

| ☐ | Ref | Title or description | Verses | keep | revise | fix |
|---|---|---|:-:|:-:|:-:|
|  | 1.t4 | Bhīṣma’s roar and conch hearten Duryodhana; the Kaurava instruments sound together. | 1.12–1.13 | ☐ | ☐ | ☐ |

### name-not-in-verse — the verse addresses its listener (“O …”): the named speaker is the one talking (1)

| ☐ | Ref | Title or description | Verses | keep | revise | fix |
|---|---|---|:-:|:-:|:-:|
|  | 4.t10 | The doubter perishes: neither this world, nor the next, nor happiness. Renunciation through yoga and the sword of knowledge cut bondage: Kṛṣṇa calls Arjuna to rise. | 4.40–4.42 | ☐ | ☐ | ☐ |

### name-not-in-verse — theme summary across 5 verses: check the scene (1)

| ☐ | Ref | Title or description | Verses | keep | revise | fix |
|---|---|---|:-:|:-:|:-:|
|  | 18.t4 | After naming the impulse and basis of action, Kṛṣṇa classifies knowledge: seeing the one, seeing separate beings, or clinging to a fragment as the whole. | 18.18–18.22 | ☐ | ☐ | ☐ |

---

## Verse advisories in full

The 10 verse-level advisories with the verse's own words, grouped by triage
label. Their rows are already flagged in the table above; this section is the
evidence for each verdict.

## name-not-in-verse — first person: the verse is spoken by this person (2)

### 1.07 · title names Duryodhana, absent from the verse

> Duryodhana names his own commanders

*the verse says:* But know, O best of the twice-born, those who are distinguished among us — the leaders of my army; I name them to you for your information.

☐ keep   ☐ revise   ☐ fix

### 1.09 · title names Duryodhana, absent from the verse

> Warriors ready to die for Duryodhana

*the verse says:* And many other heroes, ready to give up their lives for my sake, armed with various weapons, all skilled in war.

☐ keep   ☐ revise   ☐ fix


## number-unsupported — the verse lists the things but never says the number (8)

### 1.15 · title says 'three' but the verse does not

> Three conches: Pāñcajanya, Devadatta, Pauṇḍra

*the verse says:* Hṛṣīkeśa blew Pāñcajanya; Dhanañjaya blew Devadatta; and Bhīma, the doer of herculean deeds, blew the great conch Pauṇḍra.

☐ keep   ☐ revise   ☐ fix

### 8.23 · title says 'two' but the verse does not

> The two times of departure

*the verse says:* Now I shall declare, O bull of the Bhāratas, the time in which yogis, departing, do not return, and the time in which they return.

☐ keep   ☐ revise   ☐ fix

### 13.24 · title says 'three' but the verse does not

> The three paths

*the verse says:* Some see the Self within themselves by meditation, through their own mind; others by the yoga of knowledge; still others by the yoga of action.

☐ keep   ☐ revise   ☐ fix

### 14.05 · title says 'three' but the verse does not

> The three qualities

*the verse says:* Sattva, rajas and tamas — the qualities born of prakṛti — bind the imperishable embodied one in the body, O mighty-armed one.

☐ keep   ☐ revise   ☐ fix

### 14.18 · title says 'three' but the verse does not

> The three destinies

*the verse says:* Those established in sattva go upward; the rājasic stay in the middle; the tāmasic, sunk in the lowest qualities, go downward.

☐ keep   ☐ revise   ☐ fix

### 16.04 · title says 'six' but the verse does not

> Six marks of the demoniac

*the verse says:* Hypocrisy, arrogance, self-conceit, anger, harshness and ignorance belong to one born to the demoniac destiny, O Pārtha.

☐ keep   ☐ revise   ☐ fix

### 18.12 · title says 'three' but the verse does not

> Three kinds of fruit

*the verse says:* The threefold fruit of action — pleasant, unpleasant and mixed — comes after death to the non-renouncer; but never to the renouncer.

☐ keep   ☐ revise   ☐ fix

### 18.29 · title says 'three' but the verse does not

> Three kinds of intellect and fortitude

*the verse says:* Hear the threefold distinction of intellect and fortitude, declared fully and separately, by the guṇas, O Dhanañjaya.

☐ keep   ☐ revise   ☐ fix


