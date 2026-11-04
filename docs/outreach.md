# Outreach kit (NEXT.md E3)

The site is built and indexed-ish; what is missing is *people arriving*. E3 is
execution, not code. This file is the kit: what is already done, what only
Dhruba can do, and copy you can paste after reading it once.

**Drafts are drafts.** They are written in the first person because you post
them. Change any word that is not how you talk; a post that sounds like a
marketing department reads worse than a short honest one.

Sources: `PROJECT.md` §10 (discoverability), `README.md` → "Then get the link
seen", `NEXT.md` E3/E4.

---

## 0. Publish before you point anyone at it

As of 2026-11-04 two commits are local only — the module split and the
provenance page. The live site does **not** have `method/` yet. So:

1. `python3 build.py` → all green (937 assertions, 552 site-health, 60 Python).
2. Push, wait for the Pages build, then open
   <https://chapain.github.io/Bhagavad-Gita/> in a **private window** and check:
   the app opens; the footer says “How this edition was made”; that page opens;
   a chapter page opens; `…/method/` opens directly.
3. Only then post. A post that lands on a 404 (or on yesterday's build) wastes
   the one first impression a small subreddit gives you.

## 1. Repo topics (E3-a) — one item is still open

GitHub → the repo → **About** (gear icon) → Topics. Currently 11 topics, and
two things are wrong:

* `triligual` is a typo. Replace it with `trilingual` — a misspelt topic
  matches no search.
* `hindi` is missing, although the edition is in three languages.

Keep the rest (`bhagavad-gita`, `gita`, `nepali`, `sanskrit`,
`word-by-word-meaning`, `hinduism`, `thematic-breakdowns`,
`bhagavad-gita-english-nepali-hindi`, `bhagavadgita-nepali`,
`nepali-bhagavad-gita`). Do not add unrelated tech tags to farm impressions —
GitHub topic pages are browseable, and a wrong tag just annoys the people who
follow it.

> An AI session tried to set these with `gh repo edit` on 2026-11-04 and got
> HTTP 403: the token can read the repo but cannot edit its topics. This one
> needs the web UI or a token with administration scope.

While you are on that page, the **description** (“Study and Learn Srimad
Bhagavad Gita”) is fine but says nothing searchable. Optional replacement:

> A free offline study edition of the Bhagavad Gita — 700 verses in English,
> नेपाली and हिन्दी with word-by-word meanings, a literal translation and a
> paraphrase. No account, no tracking.

## 2. Where to post — one genuine post each, then stop

Order matters: post where the audience is smallest and most specific first, so
an early discussion can teach you what to say in the bigger room.

**Before each post:** read that community's rules on self-promotion. They differ
and they are enforced. If a sub requires prior participation, participate for a
week first — a drive-by link from a new account is removed, and deservedly so.

### r/bhagavadgita — the most receptive room

Title: `I built a free offline Gita study edition (700 verses, English/Nepali/Hindi, word-by-word) — would like your criticism`

Body:

> I have been building a study edition of the Gita for a while and it is now
> something I am not embarrassed to share: all 18 chapters and 700 verses, in
> English, नेपाली and हिन्दी. Each verse opens in its four pādas with the
> Sanskrit, word-by-word meanings, a literal translation and a plain-prose
> paraphrase. It installs to the home screen and works with no connection —
> which mattered to me because I read on a phone with patchy data.
>
> It follows the Śaṅkara-bhāṣya recension (where traditions differ, the bhāṣya
> reading is printed — e.g. 1.8 reads *saumadattis tathaiva ca*). There is
> deliberately no commentary: I did not want to put an argument between the
> reader and the verse.
>
> Two honest disclosures: it is a personal edition, not a critical one, and AI
> tools were used under my direction to draft translations and check the
> code — every verse was reviewed by me, and the whole method is written up on
> the site rather than hidden.
>
> Link: https://chapain.github.io/Bhagavad-Gita/
>
> I would rather hear what is wrong with it than what is nice about it —
> especially the Nepali and Hindi wording.

### r/Hinduism — same project, different framing

Title: `A trilingual study edition of the Gita that works offline (free, no account, no tracking)`

Body: the r/bhagavadgita text, but lead with the reading practice rather than
the engineering, and cut the second paragraph to one sentence. This sub is
larger and less tolerant of self-promotion; if the rules require flair or a
weekly thread, use it. Do not post the same day as the other sub.

### r/Nepal — only if you are comfortable being a Nepali builder in public

Title: `मैले नेपालीमा पनि पढ्न मिल्ने भगवद्गीता एप बनाएँ — इन्टरनेट नभए पनि चल्छ`

Body (Nepali, short): what it is, that it works offline, that it is free, that
Nepali and Hindi are included, the link. Mention Pokhara. Expect the question
“why not an app store app?” — answer: it installs from the browser, works
offline, and needs no store, no account and no permissions.

### Quora — the highest-yield single item

Find the existing question *“Where can I read the Bhagavad Gita word-by-word in
Nepali?”* (or a close variant) and **answer it properly** before linking:

> The word-by-word reading is the part most Gita sites skip, so here is how I
> would approach it, and what I built for exactly this.
>
> Take 2.47, the verse everyone quotes. Its four pādas are:
>
> कर्मण्येवाधिकारस्ते मा फलेषु कदाचन ।
> मा कर्मफलहेतुर्भूर् मा ते सङ्गोऽस्त्वकर्मणि ॥
>
> Word by word, pāda by pāda: *karmaṇi* — in action; *eva* — indeed;
> *adhikāraḥ* — the right; *te* — your. *mā* — not; *phaleṣu* — in the fruits;
> *kadācana* — ever. *mā* — not; *karma-phala* — of the fruit of action;
> *hetuḥ* — the motive; *bhūḥ* — be. *mā* — not; *te* — your; *saṅgaḥ* —
> attachment; *astu* — let be; *akarmaṇi* — in inaction.
>
> Read that way the verse stops being a slogan and becomes an instruction about
> where your responsibility ends: the right is over the act, and the four “not”s
> close both escapes — the fruit as a motive, and inaction as a hiding place.
> It is also why a literal line and a paraphrase should be read together: the
> literal keeps you honest about the Sanskrit, the paraphrase tells you what it
> is doing.
>
> If it helps, I keep a free edition that does this for all 700 verses in
> English, Nepali and Hindi, with the pādas and the word rows for every verse,
> and it works offline: https://chapain.github.io/Bhagavad-Gita/ — the method
> page explains which recension is followed and how the splits were made.
> Corrections welcome; I would rather fix a gloss than defend it.

(Those word rows are copied from `source/ch2.json`, not from memory: the build
reconstructs every pāda from them, so they are exactly the words the app shows.)

### Nepali Facebook / Viber groups — the highest-reach, lowest-signal channel

One share, in Nepali, with the **live link** (never a screenshot):

> भगवद्गीता अब नेपाली, हिन्दी र अङ्ग्रेजीमा — ७०० श्लोक, चार पाद, शब्दार्थ,
> शब्दशः अनुवाद र सरल भावानुवाद सहित। इन्टरनेट नभए पनि चल्छ, खाता चाहिँदैन, कुनै
> विज्ञापन वा ट्र्याकिङ छैन। निःशुल्क: https://chapain.github.io/Bhagavad-Gita/
>
> यो मैले आफैँका लागि बनाएको संस्करण हो — गल्ती देख्नुभयो भने जनाउनुहोस्,
> सुधार्छु।

Do not post the same message in five groups on the same day, and do not DM
strangers the link.

## 3. The monthly ritual (not daily)

E3 says *repeat monthly, not daily*, and that is the whole discipline. One line
a month, so it never becomes spam and you never burn a community:

| Month | One act | Done |
|---|---|---|
| 2026-11 | Publish, fix the two topics, post r/bhagavadgita | ☐ |
| 2026-12 | Quora answer (the word-by-word question) | ☐ |
| 2027-01 | r/Hinduism (only if the first post was received well) | ☐ |
| 2027-02 | One Nepali Facebook/Viber group | ☐ |
| 2027-03 | r/Nepal | ☐ |
| 2027-04 | Nothing. Read the Search Console numbers instead. | ☐ |

Never the same sub twice in a row; never three channels in one week.

## 4. How you will know it worked — without analytics

There is no analytics on the site, and that is a feature, not an oversight. So:

* **Google Search Console** is the real instrument: *Performance* →
  impressions, clicks, average position, and the **queries** people actually
  typed. This is the only place that shows whether the long tail (this app's
  whole strategy) is being reached. Check it monthly, not weekly; indexing and
  ranking move in weeks.
* **GitHub → Insights → Traffic** shows *referring sites* and views for the
  **repository** — not the site. If a Reddit post works, you will see reddit.com
  in the referrers, which is a real signal even though it measures repo visits.
* **Nothing else.** Referral traffic to the app itself is invisible by design.
  You will not see the forty people who read a verse and left. That is the
  price of “no analytics”, and it is the right price for a scripture app.

Do not add analytics to measure a launch. See §5.

## 5. E4 — analytics: recommendation is **no**

If you want it anyway, the honest version: **Cloudflare Web Analytics** or
**Plausible**, both cookie-free and consent-banner-free, one script. What it
would tell you: which chapters/verses are opened most, which language is chosen
most, where search fails.

Why I would still say no:

1. The app's promise is *no account, no tracking, no server*; the provenance
   page says it in three languages and the build would then be publishing a
   lie — so analytics and that sentence cannot both ship unchanged.
2. Search Console already covers the question that matters for growth
   (“are people finding me, and for what?”).
3. A scripture app is not a funnel. The numbers you would get are interesting
   once and then never again.

If you ever do add it, it is one commit that **also** edits `source/method.html`
(English, Nepali and Hindi) and the check that reads those sections — not a
script dropped into the head.

## 6. What not to do

* No second account, no vote requests, no “please upvote so this reaches
  people”. It is the fastest way to lose the room and the account.
* No screenshots instead of links — the app's own share panel already copies
  the link and the verse text (`Share` in a verse's ⋯ menu).
* No “official”, “authentic”, “the best” — this is one author's study edition
  that follows the Śaṅkara-bhāṣya recension, and it says so.
* No promising what is not there: there is no audio and no commentary, by
  decision.
* If someone finds a real error: fix it, reply once, thank them. Do not debate
  the verse in the comments — point at the method page and move on.
