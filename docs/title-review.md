# Title and description advisories — review worksheet

Snapshot of 2026-11-04, from `python3 source/audit_titles.py --markdown`. Re-run it after
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

## name-not-in-verse — first person: the verse is spoken by this person (39)

### 1.t2 · theme title names Duryodhana, absent from these verses
Verses 1.04–1.09

> Duryodhana sizes up both armies

*the verse says:* Here are heroes, great archers, equals of Bhīma and Arjuna in war: Yuyudhāna, Virāṭa, and Drupada, the great chariot-warrior. And Dhṛṣṭaketu, Cekitāna, the valiant king of Kāśī, Purujit, Kuntibhoja, and Śaibya, the bull among men. The mighty Yudhāmanyu and the valiant Uttamaujas, the son of Subhadrā, and the sons of Draupadī — all great chariot-warriors. But know, O best of the twice-born, those who are distinguished among us — the leaders of my army; …

☐ keep   ☐ revise   ☐ fix

### 1.07 · title names Duryodhana, absent from the verse
Verse 1.07

> Duryodhana names his own commanders

*the verse says:* But know, O best of the twice-born, those who are distinguished among us — the leaders of my army; I name them to you for your information.

☐ keep   ☐ revise   ☐ fix

### 1.09 · title names Duryodhana, absent from the verse
Verse 1.09

> Warriors ready to die for Duryodhana

*the verse says:* And many other heroes, ready to give up their lives for my sake, armed with various weapons, all skilled in war.

☐ keep   ☐ revise   ☐ fix

### 1.t3 · theme desc names Duryodhana, absent from these verses
Verses 1.10–1.11

> Duryodhana compares the forces, then orders every division to hold position and protect Bhīṣma.

*the verse says:* Insufficient is that strength of ours, guarded by Bhīṣma; sufficient is this strength of theirs, guarded by Bhīma. Stationed at all the approaches, take your places in your divisions — and above all, protect Bhīṣma alone, all of you.

☐ keep   ☐ revise   ☐ fix

### 3.t6 · theme desc names Kṛṣṇa, absent from these verses
Verses 3.22–3.26

> Kṛṣṇa acts although he needs nothing, lest the world fall apart. The wise likewise support others through example without disturbing their understanding.

*the verse says:* For me, O Pārtha, there is nothing to be done in the three worlds, nothing unattained to be attained — yet I continue to act. If I did not engage in action ever, untiringly, then people would follow my path in all respects, O Pārtha. These worlds would perish if I did not perform action; I would be the maker of chaos and would destroy these creatures. As the unwise act, attached to action, O Bhārata, so should the wise act, unattached, desiring the …

☐ keep   ☐ revise   ☐ fix

### 3.t7 · theme desc names Kṛṣṇa, absent from these verses
Verses 3.27–3.30

> Ego claims to be the doer; the knower sees the guṇas at work. Do not unsettle partial knowers; surrender action to Kṛṣṇa and fight without fever.

*the verse says:* All actions are performed by the guṇas of prakṛti in every way; the one deluded by egoism thinks, “I am the doer.” But the knower of truth, O mighty-armed, knowing the distinction of the guṇas and actions, and that the guṇas move among the guṇas, does not become attached. Those deluded by the guṇas of prakṛti cling to actions born of the guṇas; the one of complete knowledge should not unsettle the dull-witted, partial knowers. Renouncing all actions in …

☐ keep   ☐ revise   ☐ fix

### 4.t3 · theme desc names Kṛṣṇa, absent from these verses
Verses 4.11–4.14

> People approach Kṛṣṇa through differing aims and worship. He establishes the fourfold order, yet remains the imperishable non-doer, untainted by action.

*the verse says:* In whatever way men approach me, in that same way I favour them; people follow my path in every way, O Pārtha. Those who desire the success of actions worship the gods here; indeed, in this human world success born of action comes quickly. The fourfold order was created by me according to the distinction of guṇas and actions; though I am its author, know me as the non-doer and imperishable. Actions do not stain me, nor have I any longing for the fruit …

☐ keep   ☐ revise   ☐ fix

### 5.t6 · theme desc names Kṛṣṇa, absent from these verses
Verses 5.24–5.29

> The inwardly joyful sage, free of desire and anger, reaches Brahman-nirvāṇa. Sense and breath discipline, and knowing Kṛṣṇa as everyone’s friend, bring peace.

*the verse says:* He who is happy within, who delights within, who is illumined within — that yogi, become Brahman, attains to Brahman-nirvāṇa. The seers whose sins are destroyed, whose doubts are cut, whose selves are controlled, who delight in the welfare of all beings — they attain Brahman-nirvāṇa. For the ascetics free from desire and anger, whose thoughts are controlled, who know the Self — Brahman-nirvāṇa is present all around. Turning the sense-objects outward, …

☐ keep   ☐ revise   ☐ fix

### 6.t3 · theme desc names Kṛṣṇa, absent from these verses
Verses 6.10–6.15

> Prepare a quiet seat, hold the body upright and still the mind. With fearlessness, restraint and attention on Kṛṣṇa, meditation leads to peace.

*the verse says:* Let the yogi constantly discipline himself, abiding in a solitary place, alone, with mind and self controlled, free from desire and possessiveness. Establishing in a pure spot a steady seat for himself, neither too high nor too low, covered with cloth, a deer-skin and kuśa grass, making the mind one-pointed, restraining the activities of the mind and the senses, seated on that seat, let him practise yoga for the purification of the self. Holding body, …

☐ keep   ☐ revise   ☐ fix

### 6.t7 · theme desc names Kṛṣṇa, absent from these verses
Verses 6.29–6.32

> Seeing the Self in all and all in Kṛṣṇa, the yogi lives in unity. Regard another’s pleasure and pain as your own: this is the highest yoga.

*the verse says:* Seeing the Self in all beings and all beings in the Self, one who sees the same in everything — he attains the Supreme. He who sees me everywhere and sees everything in me — for him I am not lost, and he is not lost to me. Established in unity, the yogi who worships me abiding in all beings — abiding in that, he lives in me, whatever his way of life. He who, through the likeness of the self, sees the same everywhere, in pleasure and in pain — he is …

☐ keep   ☐ revise   ☐ fix

### 6.t11 · theme desc names Kṛṣṇa, absent from these verses
Verses 6.45–6.47

> Effort over many births brings perfection. Be a yogi; among yogis Kṛṣṇa esteems highest the one who worships him with faith and an inwardly devoted heart.

*the verse says:* But the yogi who strives with effort, purified of sin, perfected gradually through many births, then reaches the highest state. The yogi is greater than the ascetic, deemed greater than the man of knowledge, and greater than the man of rites; therefore be a yogi, O Arjuna. And among all yogis, he who, full of faith, worships me with his inmost self established in me — him I deem the most yoked, in my view.

☐ keep   ☐ revise   ☐ fix

### 7.t2 · theme desc names Kṛṣṇa, absent from these verses
Verses 7.04–7.07

> The lower nature has eight aspects; the higher sustains life. Both give rise to beings, and everything rests on Kṛṣṇa like pearls on one thread.

*the verse says:* Earth, water, fire, air, ether, mind, intellect and egoism — thus is my nature divided eightfold. This is the lower nature; but know my other nature, higher than this, O mighty-armed one — the life-element, by which the world is upheld. Know that these two natures are the womb of all beings; I am the origin and also the dissolution of the whole world. There is nothing whatever higher than me, O Dhanañjaya; all this is strung on me, like a row of gems …

☐ keep   ☐ revise   ☐ fix

### 7.t3 · theme desc names Kṛṣṇa, absent from these verses
Verses 7.08–7.11

> Taste, light, fragrance, life, wisdom and strength reveal Kṛṣṇa’s presence. Even desire, when not opposed to dharma, belongs to this account.

*the verse says:* I am the taste in waters, O son of Kuntī; I am the radiance of the moon and the sun; the sacred syllable Om in all the Vedas; the sound in ether; the manliness in men. I am the pure fragrance of the earth and the heat of fire; the life of all beings and the austerity of the ascetics. Know me as the eternal seed of all beings; I am the intelligence of the intelligent, the splendour of the splendid. And I am the strength of the strong, devoid of desire …

☐ keep   ☐ revise   ☐ fix

### 7.t4 · theme desc names Kṛṣṇa, absent from these verses
Verses 7.12–7.15

> The guṇas arise from Kṛṣṇa yet conceal him from the deluded. His māyā is hard to cross; refuge in him opens the way beyond it.

*the verse says:* And whatever states there are, of sattva, rajas or tamas — know them all as from me alone; yet I am not in them, they are in me. Deluded by these states made of the three guṇas, this entire world does not know me, who am beyond them, imperishable. This divine māyā of mine, consisting of the guṇas, is hard to overcome; but those who take refuge in me alone cross beyond this māyā. The wrong-doers, the deluded, the lowest of men do not resort to me; …

☐ keep   ☐ revise   ☐ fix

### 7.t6 · theme desc names Kṛṣṇa, absent from these verses
Verses 7.20–7.23

> Desire draws people to other deities. Kṛṣṇa steadies their faith and grants the fruit, but that fruit ends; his own devotees come to him.

*the verse says:* Those whose knowledge is stolen by desires resort to other deities, following this or that rite, constrained by their own nature. Whatever divine form a devotee desires to worship with faith, I render that very faith of his steady. United with that faith, he engages in the worship of that deity, and from it obtains his desires — which are verily ordained by me. But the fruit of those worshippers is limited; the fruit belongs to the small-minded. The …

☐ keep   ☐ revise   ☐ fix

### 7.t8 · theme desc names Kṛṣṇa, absent from these verses
Verses 7.28–7.30

> Freed from duality, the steadfast worship Kṛṣṇa. Seeking release from ageing and death, they know Brahman, all of adhyātma and action, and know him even at death.

*the verse says:* But those men of good deeds whose sins have come to an end — freed from the delusion of the pairs of opposites — worship me with firm vows. Those who, striving for freedom from old age and death, take refuge in me — they know Brahman, the entire adhyātma, and all action. Those who know me along with the elements, the deities and the sacrifice — even at the time of death, with minds established, they know me.

☐ keep   ☐ revise   ☐ fix

### 8.t2 · theme desc names Kṛṣṇa, absent from these verses
Verses 8.05–8.10

> The final remembered state directs departure. Therefore remember Kṛṣṇa while acting; steady practice, devotion and yogic concentration prepare the last moment.

*the verse says:* Whoever, at the end, leaves the body remembering me alone — he attains my being; there is no doubt of this. Whatever state one remembers at the end while leaving the body — to that state one goes, ever pervaded by that thought. Therefore remember me at all times and fight; with mind and intellect offered to me, you will surely come to me, without doubt. United with the yoga of practice, with a mind that goes nowhere else — one reaches the supreme …

☐ keep   ☐ revise   ☐ fix

### 8.t3 · theme desc names Kṛṣṇa, absent from these verses
Verses 8.11–8.15

> For the imperishable goal, restrain the body’s gates and depart uttering Om. Constant, single-minded remembrance makes Kṛṣṇa easy to reach, without return.

*the verse says:* That which the knowers of the Vedas call the imperishable, which the desireless ascetics enter, desiring which they practise celibacy — that goal I shall declare to you briefly. Restraining all the gates of the body, confining the mind in the heart, fixing the life-breath in the head, established in yogic concentration — — uttering the single syllable Om, the Brahman, and remembering me — he who departs, giving up the body, reaches the supreme goal. He …

☐ keep   ☐ revise   ☐ fix

### 8.t5 · theme desc names Kṛṣṇa, absent from these verses
Verses 8.20–8.22

> Beyond the dissolving unmanifest is the eternal, imperishable goal. It is Kṛṣṇa’s supreme abode, reached through undivided devotion, with no return.

*the verse says:* But beyond this unmanifest is another unmanifest, eternal — which, when all beings perish, does not perish. That unmanifest is called the imperishable; they call it the supreme goal; reaching which they do not return — that is my supreme abode. That supreme Person, O Pārtha, is attainable by devotion to him alone; in him all beings dwell, and by him all this is pervaded.

☐ keep   ☐ revise   ☐ fix

### 9.t2 · theme desc names Kṛṣṇa, absent from these verses
Verses 9.04–9.08

> All beings rest in Kṛṣṇa, who remains beyond containment. Through prakṛti they dissolve and appear again, as the cycles of creation unfold.

*the verse says:* By me this whole world is pervaded in my unmanifest form; all beings rest in me, but I am not contained in them. And beings do not rest in me — behold my divine yoga! I sustain all beings yet stand apart, and my self is the origin of beings. As the vast wind, ever moving, abides in space, so all beings abide in me — know this. All beings, O son of Kuntī, return to my prakṛti at the end of a kalpa; at the beginning of a kalpa I send them forth again. …

☐ keep   ☐ revise   ☐ fix

### 9.t6 · theme desc names Kṛṣṇa, absent from these verses
Verses 9.20–9.25

> Heaven’s pleasures end when merit is spent. Kṛṣṇa supplies what devotees lack and protects what they have; worship shapes the destination, and his devotees come to him.

*the verse says:* The knowers of the three Vedas, drinking soma, purified of sin, worshipping me by sacrifice, pray for the path to heaven; attaining the world of Indra, they enjoy the divine pleasures of the gods in heaven. Having enjoyed the vast world of heaven, when their merit is exhausted they return to the world of mortals; thus, following the dharma of the three Vedas, desiring desires, they come and go. To those who worship me, ever united, thinking of me alone …

☐ keep   ☐ revise   ☐ fix

### 9.t8 · theme desc names Kṛṣṇa, absent from these verses
Verses 9.30–9.34

> Past wrongdoing or birth does not bar devoted refuge. Kṛṣṇa closes with the same four instructions found in 18.65: fix your mind, be devoted, worship and bow.

*the verse says:* Even if a man of very evil conduct worships me with single-minded devotion, he is to be regarded as good, for he is rightly resolved. Quickly he becomes righteous of soul and attains lasting peace; know this for certain, O son of Kuntī: my devotee never perishes. For those who take refuge in me, O Pārtha — even those of sinful birth, women, traders and labourers — they too reach the supreme goal. How much more then the holy brāhmaṇas and the devoted …

☐ keep   ☐ revise   ☐ fix

### 10.t2 · theme desc names Kṛṣṇa, absent from these verses
Verses 10.04–10.07

> The varied qualities of beings, great seers and ancient Manus arise from Kṛṣṇa. Knowing this glory brings unwavering yoga.

*the verse says:* Intellect, knowledge, freedom from delusion, forbearance, truth, self-control, calm — pleasure, pain, birth, death, fear and fearlessness, non-violence, equanimity, contentment, austerity, generosity, fame and infamy — these various states of beings arise from me alone. The seven great seers, the four ancient Manus, born of my mind — from them come the beings of this world. He who knows in truth this glory and power of mine is united to me by …

☐ keep   ☐ revise   ☐ fix

### 10.t3 · theme desc names Kṛṣṇa, absent from these verses
Verses 10.08–10.11

> Knowing Kṛṣṇa as the source, devotees rejoice together in him. He gives discerning yoga and lights the lamp that dispels ignorance.

*the verse says:* I am the source of all; everything proceeds from me. Knowing this, the wise worship me, filled with devotion. Their thoughts on me, their lives given to me, enlightening one another, always speaking of me — they are content and rejoice. To them, ever devoted, worshipping me with love, I give the yoga of discernment, by which they come to me. Out of compassion for them, dwelling in their hearts, I destroy the darkness born of ignorance with the shining …

☐ keep   ☐ revise   ☐ fix

### 10.t5 · theme desc names Arjuna, absent from these verses
Verses 10.16–10.18

> Arjuna asks for the glories that pervade the world and the forms in which to contemplate Kṛṣṇa. He is never satisfied with hearing this nectar.

*the verse says:* Tell me without omission your divine glories, by which you abide, pervading these worlds. How shall I know you, O yogi, contemplating you always? And in what states are you to be thought of, O Lord? Tell me again, in detail, your yoga and your glory, O Janārdana; I am never satiated with hearing your nectar.

☐ keep   ☐ revise   ☐ fix

### 10.t7 · theme desc names Kṛṣṇa, absent from these verses
Verses 10.24–10.26

> Priest, commander, ocean, seer, Om, japa, Himālaya and tree become signs of Kṛṣṇa’s presence, alongside celestial sages and the perfected.

*the verse says:* Among priests, O Pārtha, know me as the chief, Bṛhaspati; among generals I am Skanda; among waters I am the ocean. Among the great seers I am Bhṛgu; among words I am the single syllable Om; among sacrifices I am the japa-sacrifice; among the immovable I am the Himālaya. Among all trees I am the aśvattha; among the divine sages, Nārada; among the gandharvas, Citraratha; among the perfected, the sage Kapila.

☐ keep   ☐ revise   ☐ fix

### 10.t11 · theme desc names Kṛṣṇa, absent from these verses
Verses 10.39–10.42

> Every being has Kṛṣṇa as its seed; his glories have no end. All splendour is a spark of him, and one part of him sustains the whole world.

*the verse says:* And whatever is the seed of all beings, that I am, O Arjuna; no being, moving or unmoving, exists without me. There is no end to my divine glories, O scorcher of foes; this is but a summary declared by me of the extent of my glory. Whatever being is glorious, radiant or powerful — know that to be born of a portion of my splendour. But what need, Arjuna, of this detailed knowledge? I stand supporting this whole world with one part of myself.

☐ keep   ☐ revise   ☐ fix

### 11.t9 · theme desc names Arjuna, absent from these verses
Verses 11.41–11.44

> Remembering careless words and casual treatment, Arjuna asks forgiveness. Before the father and teacher of the world, he prostrates and asks to be forgiven as a father forgives a son, or a friend a friend.

*the verse says:* Whatever I said in rash familiarity — 'O Kṛṣṇa, O Yādava, O friend' — not knowing your majesty, whether in carelessness or in love, and whatever disrespect I showed you in sport, rest, sitting or at meals, alone or before others, O Acyuta — that I beg you to forgive, O immeasurable one. You are the father of this world, moving and unmoving; you are its supreme object of worship and the most venerable teacher; none equals you in the three worlds, how …

☐ keep   ☐ revise   ☐ fix

### 11.t10 · theme desc names Arjuna, absent from these verses
Verses 11.45–11.46

> Joy and fear remain together. Arjuna asks for the familiar crowned, four-armed form with mace and discus, rather than the overwhelming universal form.

*the verse says:* Having seen what I never saw before, I am delighted, yet my mind trembles with fear; show me, O God, your gracious form — be merciful, O Lord of the universe. I long to see you as before — crowned, with mace and discus in hand; appear in that four-armed form, O thousand-armed, universal form.

☐ keep   ☐ revise   ☐ fix

### 12.t2 · theme desc names Kṛṣṇa, absent from these verses
Verses 12.06–12.08

> Kṛṣṇa swiftly delivers those who dedicate action and meditate on him. Fix mind and intellect in him: the promise is to dwell in him.

*the verse says:* But those who surrender all actions to me, intent on me, worshipping me with undivided yoga and meditating on me, — for them, whose minds are fixed on me, O Pārtha, I swiftly become the deliverer from the ocean of death and rebirth. Fix your mind on me alone; establish your intellect in me; then you shall live in me alone — of this there is no doubt.

☐ keep   ☐ revise   ☐ fix

### 12.t3 · theme desc names Kṛṣṇa, absent from these verses
Verses 12.09–12.12

> A graded path: if concentration is difficult, practise; if that is difficult, work for Kṛṣṇa. If needed, relinquish action’s fruits: renunciation brings peace.

*the verse says:* If you cannot fix your mind steadily on me, then practise the yoga of repetition — seek to reach me by practice, O Dhanañjaya. If you are unable to practise even that, be devoted to working for me; even performing actions for my sake, you shall attain perfection. If you cannot do even this, then, taking refuge in my yoga, renounce the fruit of all actions — with the self controlled. Better indeed is knowledge than practice; better than knowledge is …

☐ keep   ☐ revise   ☐ fix

### 13.t3 · theme desc names Kṛṣṇa, absent from these verses
Verses 13.12–13.18

> Beginningless Brahman pervades all, beyond senses and divisions, sustaining every being. It is the light of lights in every heart; knowing this leads to Kṛṣṇa’s being.

*the verse says:* I shall declare the object of knowledge, knowing which one tastes immortality — the beginningless supreme Brahman, which is called neither being nor non-being. With hands and feet everywhere, with eyes, heads and faces everywhere, with ears everywhere — it stands, pervading all in the world. Appearing with all the attributes of the senses, yet devoid of all senses; unattached, yet upholding all; without guṇas, yet enjoying the guṇas. It is within and …

☐ keep   ☐ revise   ☐ fix

### 14.t7 · theme desc names Kṛṣṇa, absent from these verses
Verses 14.26–14.27

> Unwavering devotion to Kṛṣṇa crosses the guṇas and makes one fit for Brahman. He is the basis of immortality, eternal dharma and absolute bliss.

*the verse says:* He who serves me with the unwavering yoga of devotion — transcending these guṇas, he becomes fit for Brahman. For I am the support of Brahman, of immortality and the imperishable, of eternal dharma and of absolute bliss.

☐ keep   ☐ revise   ☐ fix

### 15.t4 · theme desc names Kṛṣṇa, absent from these verses
Verses 15.12–15.15

> Light, nourishment, digestion, memory, knowledge and forgetfulness arise from Kṛṣṇa. Seated in every heart, he is the one to be known through the Vedas.

*the verse says:* The light in the sun, which illumines the whole world, and that in the moon and in fire — know that light as mine. Entering the earth I sustain all beings with my energy; becoming the sap-laden moon I nourish all herbs. Becoming the fire of digestion in the bodies of living beings, joined with the in-breath and out-breath, I cook the four kinds of food. I am seated in the heart of all; from me come memory, knowledge and their removal; by all the Vedas …

☐ keep   ☐ revise   ☐ fix

### 15.t5 · theme desc names Kṛṣṇa, absent from these verses
Verses 15.16–15.20

> Beyond the perishable and imperishable stands the sustaining Supreme Person. Knowing Kṛṣṇa as Puruṣottama brings wholehearted worship and completes this secret teaching.

*the verse says:* There are two persons in this world: the perishable and the imperishable. The perishable is all beings; the unchanging is called the imperishable. But there is another, the supreme Person, called the supreme Self — the eternal Lord who, entering the three worlds, sustains them. Since I transcend the perishable and am higher than the imperishable, I am known in the world and in the Veda as the highest Person. He who, undeluded, knows me as the highest …

☐ keep   ☐ revise   ☐ fix

### 18.t12 · theme desc names Kṛṣṇa, absent from these verses
Verses 18.54–18.55

> The Brahman-realised one is serene, equal to all, without grief or craving. Supreme devotion reveals Kṛṣṇa in truth and leads into him.

*the verse says:* Become Brahman, serene of soul, he neither grieves nor desires; equal to all beings, he attains supreme devotion to me. By that devotion he knows me in truth, who and what I am; knowing me in truth, he enters me immediately.

☐ keep   ☐ revise   ☐ fix

### 18.t13 · theme desc names Kṛṣṇa, absent from these verses
Verses 18.56–18.60

> Resting in Kṛṣṇa, dedicate every act and cross difficulties by grace. An ego-driven refusal to fight is vain: one’s own nature still compels action.

*the verse says:* Performing all actions ever, taking refuge in me, he attains the eternal, imperishable state by my grace. Surrendering all actions to me in thought, making me supreme, resorting to the yoga of discernment, always fix your mind on me. With your mind on me, you shall cross all difficulties by my grace; but if from ego you will not listen, you shall be destroyed. If, relying on ego, you think 'I will not fight' — vain is your resolve; your nature will …

☐ keep   ☐ revise   ☐ fix

### 18.t15 · theme desc names Kṛṣṇa, absent from these verses
Verses 18.64–18.66

> Out of love, Kṛṣṇa gives the supreme secret: fix your mind on him, worship and bow. Take refuge in him alone; he promises freedom from all sin.

*the verse says:* Hear again my supreme word, the most secret of all: you are dearly loved by me, so I speak for your good. Fix your mind on me, be my devotee, offer to me, bow to me — you shall surely come to me; I promise you truly, for you are dear to me. Abandon all dharmas and take refuge in me alone; I will free you from all sins — grieve not.

☐ keep   ☐ revise   ☐ fix

### 18.t16 · theme desc names Kṛṣṇa, absent from these verses
Verses 18.67–18.71

> Do not give this teaching to one who lacks austerity or devotion, refuses to listen, or finds fault with Kṛṣṇa. Devoted teaching, study and faithful hearing are honoured; even the listener is freed.

*the verse says:* This is never to be spoken by you to one without austerity, nor to the faithless, nor to one who does not serve, nor to one who reviles me. He who teaches this supreme secret to my devotees with supreme devotion — having given me his highest love, he shall without doubt come to me alone. None among men does me greater service than he; and none shall be dearer to me on earth than he. And he who studies this sacred dialogue of ours — by him I am …

☐ keep   ☐ revise   ☐ fix


## name-not-in-verse — theme summary across 2 verses: check the scene (1)

### 1.t4 · theme desc names Duryodhana, absent from these verses
Verses 1.12–1.13

> Bhīṣma’s roar and conch hearten Duryodhana; the Kaurava instruments sound together.

*the verse says:* To gladden him, the grandsire of the Kurus, the glorious Bhīṣma, roared a lion's roar and blew his conch loudly. Then conches, drums, kettledrums, tabors and horns were suddenly struck together — that sound became tumultuous.

☐ keep   ☐ revise   ☐ fix


## name-not-in-verse — the verse addresses its listener (“O …”): the named speaker is the one talking (1)

### 4.t10 · theme desc names Kṛṣṇa, absent from these verses
Verses 4.40–4.42

> The doubter perishes: neither this world, nor the next, nor happiness. Renunciation through yoga and the sword of knowledge cut bondage: Kṛṣṇa calls Arjuna to rise.

*the verse says:* But the ignorant man without faith, full of doubt, perishes; for the doubting soul there is neither this world, nor the next, nor happiness. Actions do not bind him who has renounced actions through yoga, whose doubt is destroyed by knowledge, who is self-possessed, O Dhanañjaya. Therefore, cut this doubt about the Self, born of ignorance and dwelling in your heart, with the sword of knowledge; stand firm in yoga — arise, O Bhārata!

☐ keep   ☐ revise   ☐ fix


## name-not-in-verse — theme summary across 5 verses: check the scene (1)

### 18.t4 · theme desc names Kṛṣṇa, absent from these verses
Verses 18.18–18.22

> After naming the impulse and basis of action, Kṛṣṇa classifies knowledge: seeing the one, seeing separate beings, or clinging to a fragment as the whole.

*the verse says:* Knowledge, the known and the knower — the threefold impulse to action; the instrument, the act and the agent — the threefold basis of action. Knowledge, action and agent are declared threefold by the distinction of the guṇas — hear them as they are in the enumeration of the guṇas. That knowledge by which one sees one imperishable being in all beings, undivided in the divided — know that as sāttvic. But the knowledge that sees manifold and separate …

☐ keep   ☐ revise   ☐ fix


## number-unsupported — the verse lists the things but never says the number (8)

### 1.15 · title says 'three' but the verse does not
Verse 1.15

> Three conches: Pāñcajanya, Devadatta, Pauṇḍra

*the verse says:* Hṛṣīkeśa blew Pāñcajanya; Dhanañjaya blew Devadatta; and Bhīma, the doer of herculean deeds, blew the great conch Pauṇḍra.

☐ keep   ☐ revise   ☐ fix

### 8.23 · title says 'two' but the verse does not
Verse 8.23

> The two times of departure

*the verse says:* Now I shall declare, O bull of the Bhāratas, the time in which yogis, departing, do not return, and the time in which they return.

☐ keep   ☐ revise   ☐ fix

### 13.24 · title says 'three' but the verse does not
Verse 13.24

> The three paths

*the verse says:* Some see the Self within themselves by meditation, through their own mind; others by the yoga of knowledge; still others by the yoga of action.

☐ keep   ☐ revise   ☐ fix

### 14.05 · title says 'three' but the verse does not
Verse 14.05

> The three qualities

*the verse says:* Sattva, rajas and tamas — the qualities born of prakṛti — bind the imperishable embodied one in the body, O mighty-armed one.

☐ keep   ☐ revise   ☐ fix

### 14.18 · title says 'three' but the verse does not
Verse 14.18

> The three destinies

*the verse says:* Those established in sattva go upward; the rājasic stay in the middle; the tāmasic, sunk in the lowest qualities, go downward.

☐ keep   ☐ revise   ☐ fix

### 16.04 · title says 'six' but the verse does not
Verse 16.04

> Six marks of the demoniac

*the verse says:* Hypocrisy, arrogance, pride, anger, harshness and ignorance — these belong to one born to the demoniac destiny, O Pārtha.

☐ keep   ☐ revise   ☐ fix

### 18.12 · title says 'three' but the verse does not
Verse 18.12

> Three kinds of fruit

*the verse says:* The threefold fruit of action — pleasant, unpleasant and mixed — comes after death to the non-renouncer; but never to the renouncer.

☐ keep   ☐ revise   ☐ fix

### 18.29 · title says 'three' but the verse does not
Verse 18.29

> Three kinds of intellect and fortitude

*the verse says:* Hear the threefold distinction of intellect and fortitude, declared fully and separately, by the guṇas, O Dhanañjaya.

☐ keep   ☐ revise   ☐ fix


