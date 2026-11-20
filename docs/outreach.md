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

## 0. The site is live — verify it before you point anyone at it

**Status, 2026-11-20.** The published site is current, not pending. `main` is at
`ac7e50e` (the merge of PR #84); CI on that commit passed; the GitHub Pages
build for that same commit is `built`. So the live site *is* the audited commit,
and `method/` — the page a sceptical reader will look for — has been live since
the provenance release, not waiting on a push. This section previously said the
opposite (two local commits, no `method/`, 937/560/68 counts); that was true on
2026-11-04 and is false now.

Current numbers, measured on `ac7e50e` with `python3 build.py --prove`, not
quoted from memory:

| Check | Count |
|---|---|
| Python mutation/regression tests | 122 |
| Document assertions (`run_gita_app.js`) | 946 |
| Site-health checks | 560 |
| SEO checks | 10 |
| Study-map checks | 9,658 |
| Browser checks | 357 over http / 348 over `file://` — **CI only**, not runnable in this sandbox |

**The five-minute check.** Do it in a **private window**, because a cached
service worker will happily serve you last week's build and tell you nothing:

1. `python3 build.py --prove` → all green. If it is not green, do not post.
2. Open <https://chapain.github.io/Bhagavad-Gita/>. The app must open.
3. Scroll to the footer: “How this edition was made” must be there, and it must
   open — directly as `…/method/` too, not only through the link.
4. Open any chapter page (`…/chapter/2/`) and confirm the full text renders.
5. Switch to नेपाली, then हिन्दी: no English leaking into the interface.
6. Optional but worth it: install to the home screen and read one verse in
   airplane mode. If the offline path is broken, strangers will find out first.

7. Only then post. A post that lands on a 404 (or on yesterday's build) wastes
   the one first impression a small subreddit gives you.

**If you have commits that are not pushed yet,** push, wait for the Pages build
to report `built`, and repeat steps 2–6. Never announce a link you have not
opened yourself in that same session.

## 1. Repo topics (E3-a) — one item is still open

GitHub → the repo → **About** (gear icon) → Topics. Currently 11 topics (re-read
via the API on 2026-11-20 — `triligual` is still there and `hindi` is still
absent), and two things are wrong:

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

Lead with the reading practice, not the engineering, and keep the recension to
one sentence. This sub is larger and less tolerant of self-promotion; if the
rules require flair or a weekly thread, use it. Do not post the same day as the
other sub.

Body:

> Most Gita sites give you the verse and then a commentary. What I wanted for my
> own practice was the verse itself, laid out so it can be read slowly: the four
> pādas, the Sanskrit, word-by-word meanings, a literal translation and a plain
> paraphrase — and nothing arguing between me and the text.
>
> I have finished that for all 18 chapters and 700 verses in English, नेपाली and
> हिन्दी. It follows the Śaṅkara-bhāṣya recension and has no commentary, by
> choice. It installs to the home screen and reads with no connection — which
> matters to me because I read on a phone with patchy data.
>
> Two honest disclosures: this is a personal edition, not a critical one, and AI
> tools were used under my direction to draft translations and check the code —
> every verse was reviewed by me, and the method is written up on the site rather
> than hidden.
>
> Link: https://chapain.github.io/Bhagavad-Gita/
>
> Corrections are more useful to me than praise, especially on the Nepali and
> Hindi wording.

### r/Nepal — only if you are comfortable being a Nepali builder in public

Title: `मैले नेपालीमा पनि पढ्न मिल्ने भगवद्गीता एप बनाएँ — इन्टरनेट नभए पनि चल्छ`

Body (Nepali, ready to paste):

> नमस्ते,
>
> धेरै समयदेखि आफ्नै पढाइका लागि भगवद्गीताको एउटा अध्ययन संस्करण बनाइरहेको
> थिएँ। अहिले १८ वटै अध्याय र ७०० श्लोक तयार छन् — अङ्ग्रेजी, नेपाली र हिन्दी
> तीनै भाषामा।
>
> हरेक श्लोक चार पादमा खुल्छ: संस्कृत, शब्दार्थ, शब्दशः अनुवाद र सरल
> अर्थ। फोनको होम स्क्रिनमा राख्न मिल्छ, र इन्टरनेट नभए पनि पढ्न सकिन्छ — म
> आफैँ धेरै ठाउँमा कमजोर इन्टरनेटमा पढ्ने भएकाले यो मेरा लागि जरुरी थियो।
>
> पाठ शाङ्करभाष्यको परम्पराअनुसार राखिएको छ: जहाँ परम्परामा फरक पर्छ, भाष्यको
> पाठ नै छापिएको छ — जस्तै १.८ मा “सौमदत्तिस्तथैव च”। जानाजान कुनै टीका राखेको
> छैन; म श्लोक र पाठकबीच आफ्नो बहस राख्न चाहन्नँ।
>
> दुई कुरा खुलस्त भन्नुपर्छ। यो मेरो व्यक्तिगत संस्करण हो, विद्वान्हरूले सम्पादन
> गरेको संस्करण होइन। र यसमा AI साधनहरू मेरो निर्देशनमा प्रयोग भएका छन् —
> अनुवादको मस्यौदा र कोड जाँचका लागि; हरेक श्लोक मैले पढेर जाँचेको छु, र विधि
> साइटमै लेखिएको छ, लुकाइएको छैन।
>
> लिङ्क: https://chapain.github.io/Bhagavad-Gita/
>
> म पोखराबाट यो बनाइरहेको छु। तारिफभन्दा गल्ती सुन्न मन छ — विशेषगरी नेपाली र
> हिन्दी शब्दहरूमा। केही बिग्रिएको भेट्नुभयो भने यहीँ लेख्नुहोस्, सुधार्छु।

Expect “why not an app store app?” — keep this reply ready rather than repeating
it in the post:

> किन Play Store मा छैन? — ब्राउजरबाटै होम स्क्रिनमा राख्न मिल्छ, इन्टरनेट बिना
> चल्छ, र स्टोर, खाता वा अनुमति केही चाहिँदैन। एउटा श्लोक पढ्नका लागि ठूलो एप
> इन्स्टल गर्नु नपरोस् भन्ने पनि हो।

Two r/Nepal specifics: the audience will ask whether the Nepali is yours or
machine-drafted, so answer the same way the method page does (drafted with AI
tools under your direction, every verse reviewed by you) — a straight answer
costs nothing and a vague one reads badly. And do not lead with the technology;
lead with reading the Gita in Nepali on a phone with no data.

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
