# -*- coding: utf-8 -*-
"""padas_ch6.py — the pāda (quarter) division of every verse in chapter 6.

This is plain data: what you write here is what the app shows in the verse
popup's quarter boxes. Nothing is recalculated at build time.

Each verse maps to a list of entries in reading order:

    "1.01": [
        ("s", devanagari, iast),
        ("p", devanagari, iast, syllables),
        ...
    ]

    ("p", devanagari, iast, syllables)   a pāda
    ("s", devanagari, iast)              a speaker line, e.g. श्रीभगवानुवाच

Speakers appear where the verse puts them — usually first, but in 1.21 and 1.28
between the two halves, and the app renders them in the order given here.

TO CORRECT A SPLIT: move a word from one pāda to its neighbour, in both the
Devanagari and the IAST, and adjust the two syllable counts. The build checks
that the pādas still spell the verse and that the counts match, and stops with
a clear message if they do not.

The flowing verse you read on the page does not come from this file — that is
printed verbatim from ch6.json.
"""

GITA_CH6_PADAS = {
"6.01": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "अनाश्रितः कर्मफलं", "anāśritaḥ karmaphalaṃ", 8),
    ("p", "कार्यं कर्म करोति यः", "kāryaṃ karma karoti yaḥ", 8),
    ("p", "स सन्न्यासी च योगी च", "sa sannyāsī ca yogī ca", 8),
    ("p", "न निरग्निर्न चाक्रियः", "na niragnirna cākriyaḥ", 8),
],

"6.02": [
    ("p", "यं सन्न्यासमिति प्राहुर्", "yaṃ sannyāsamiti prāhur", 8),
    ("p", "योगं तं विद्धि पाण्डव", "yogaṃ taṃ viddhi pāṇḍava", 8),
    ("p", "न ह्यसन्न्यस्तसङ्कल्पो", "na hyasannyastasaṅkalpo", 8),
    ("p", "योगी भवति कश्चन", "yogī bhavati kaścana", 8),
],

"6.03": [
    ("p", "आरुरुक्षोर्मुनेर्योगं", "ārurukṣormuneryogaṃ", 8),
    ("p", "कर्म कारणमुच्यते", "karma kāraṇamucyate", 8),
    ("p", "योगारूढस्य तस्यैव", "yogārūḍhasya tasyaiva", 8),
    ("p", "शमः कारणमुच्यते", "śamaḥ kāraṇamucyate", 8),
],

"6.04": [
    ("p", "यदा हि नेन्द्रियार्थेषु", "yadā hi nendriyārtheṣu", 8),
    ("p", "न कर्मस्वनुषज्जते", "na karmasvanuṣajjate", 8),
    ("p", "सर्वसङ्कल्पसन्न्यासी", "sarvasaṅkalpasannyāsī", 8),
    ("p", "योगारूढस्तदोच्यते", "yogārūḍhastadocyate", 8),
],

"6.05": [
    ("p", "उद्धरेदात्मनात्मानं", "uddharedātmanātmānaṃ", 8),
    ("p", "नात्मानमवसादयेत्", "nātmānamavasādayet", 8),
    ("p", "आत्मैव ह्यात्मनो बन्धुर्", "ātmaiva hyātmano bandhur", 8),
    ("p", "आत्मैव रिपुरात्मनः", "ātmaiva ripurātmanaḥ", 8),
],

"6.06": [
    ("p", "बन्धुरात्मात्मनस्तस्य", "bandhurātmātmanastasya", 8),
    ("p", "येनात्मैवात्मना जितः", "yenātmaivātmanā jitaḥ", 8),
    ("p", "अनात्मनस्तु शत्रुत्वे", "anātmanastu śatrutve", 8),
    ("p", "वर्तेतात्मैव शत्रुवत्", "vartetātmaiva śatruvat", 8),
],

"6.07": [
    ("p", "जितात्मनः प्रशान्तस्य", "jitātmanaḥ praśāntasya", 8),
    ("p", "परमात्मा समाहितः", "paramātmā samāhitaḥ", 8),
    ("p", "शीतोष्णसुखदुःखेषु", "śītoṣṇasukhaduḥkheṣu", 8),
    ("p", "तथा मानापमानयोः", "tathā mānāpamānayoḥ", 8),
],

"6.08": [
    ("p", "ज्ञानविज्ञानतृप्तात्मा", "jñānavijñānatṛptātmā", 8),
    ("p", "कूटस्थो विजितेन्द्रियः", "kūṭastho vijitendriyaḥ", 8),
    ("p", "युक्त इत्युच्यते योगी", "yukta ityucyate yogī", 8),
    ("p", "समलोष्टाश्मकाञ्चनः", "samaloṣṭāśmakāñcanaḥ", 8),
],

"6.09": [
    ("p", "सुहृन्मित्रार्युदासीन", "suhṛnmitrāryudāsīna", 8),
    ("p", "मध्यस्थद्वेष्यबन्धुषु", "madhyasthadveṣyabandhuṣu", 8),
    ("p", "साधुष्वपि च पापेषु", "sādhuṣvapi ca pāpeṣu", 8),
    ("p", "समबुद्धिर्विशिष्यते", "samabuddhirviśiṣyate", 8),
],

"6.10": [
    ("p", "योगी युञ्जीत सततम्", "yogī yuñjīta satatam", 8),
    ("p", "आत्मानं रहसि स्थितः", "ātmānaṃ rahasi sthitaḥ", 8),
    ("p", "एकाकी यतचित्तात्मा", "ekākī yatacittātmā", 8),
    ("p", "निराशीरपरिग्रहः", "nirāśīraparigrahaḥ", 8),
],

"6.11": [
    ("p", "शुचौ देशे प्रतिष्ठाप्य", "śucau deśe pratiṣṭhāpya", 8),
    ("p", "स्थिरमासनमात्मनः", "sthiramāsanamātmanaḥ", 8),
    ("p", "नात्युच्छ्रितं नातिनीचं", "nātyucchritaṃ nātinīcaṃ", 8),
    ("p", "चैलाजिनकुशोत्तरम्", "cailājinakuśottaram", 8),
],

"6.12": [
    ("p", "तत्रैकाग्रं मनः कृत्वा", "tatraikāgraṃ manaḥ kṛtvā", 8),
    ("p", "यतचित्तेन्द्रियक्रियः", "yatacittendriyakriyaḥ", 8),
    ("p", "उपविश्यासने युञ्ज्याद्", "upaviśyāsane yuñjyād", 8),
    ("p", "योगमात्मविशुद्धये", "yogamātmaviśuddhaye", 8),
],

"6.13": [
    ("p", "समं कायशिरोग्रीवं", "samaṃ kāyaśirogrīvaṃ", 8),
    ("p", "धारयन्नचलं स्थिरः", "dhārayannacalaṃ sthiraḥ", 8),
    ("p", "सम्प्रेक्ष्य नासिकाग्रं स्वं", "samprekṣya nāsikāgraṃ svaṃ", 8),
    ("p", "दिशश्चानवलोकयन्", "diśaścānavalokayan", 8),
],

"6.14": [
    ("p", "प्रशान्तात्मा विगतभीर्", "praśāntātmā vigatabhīr", 8),
    ("p", "ब्रह्मचारिव्रते स्थितः", "brahmacārivrate sthitaḥ", 8),
    ("p", "मनः संयम्य मच्चित्तो", "manaḥ saṃyamya maccitto", 8),
    ("p", "युक्त आसीत मत्परः", "yukta āsīta matparaḥ", 8),
],

"6.15": [
    ("p", "युञ्जन्नेवं सदात्मानं", "yuñjannevaṃ sadātmānaṃ", 8),
    ("p", "योगी नियतमानसः", "yogī niyatamānasaḥ", 8),
    ("p", "शान्तिं निर्वाणपरमां", "śāntiṃ nirvāṇaparamāṃ", 8),
    ("p", "मत्संस्थामधिगच्छति", "matsaṃsthāmadhigacchati", 8),
],

"6.16": [
    ("p", "नात्यश्नतस्तु योगोऽस्ति", "nātyaśnatastu yogo’sti", 8),
    ("p", "न चैकान्तमनश्नतः", "na caikāntamanaśnataḥ", 8),
    ("p", "न चातिस्वप्नशीलस्य", "na cātisvapnaśīlasya", 8),
    ("p", "जाग्रतो नैव चार्जुन", "jāgrato naiva cārjuna", 8),
],

"6.17": [
    ("p", "युक्ताहारविहारस्य", "yuktāhāravihārasya", 8),
    ("p", "युक्तचेष्टस्य कर्मसु", "yuktaceṣṭasya karmasu", 8),
    ("p", "युक्तस्वप्नावबोधस्य", "yuktasvapnāvabodhasya", 8),
    ("p", "योगो भवति दुःखहा", "yogo bhavati duḥkhahā", 8),
],

"6.18": [
    ("p", "यदा विनियतं चित्तम्", "yadā viniyataṃ cittam", 8),
    ("p", "आत्मन्येवावतिष्ठते", "ātmanyevāvatiṣṭhate", 8),
    ("p", "निःस्पृहः सर्वकामेभ्यो", "niḥspṛhaḥ sarvakāmebhyo", 8),
    ("p", "युक्त इत्युच्यते तदा", "yukta ityucyate tadā", 8),
],

"6.19": [
    ("p", "यदा दीपो निवातस्थो", "yadā dīpo nivātastho", 8),
    ("p", "नेङ्गते सोपमा स्मृता", "neṅgate sopamā smṛtā", 8),
    ("p", "योगिनो यतचित्तस्य", "yogino yatacittasya", 8),
    ("p", "युञ्जतो योगमात्मनः", "yuñjato yogamātmanaḥ", 8),
],

"6.20": [
    ("p", "यत्रोपरमते चित्तं", "yatroparamate cittaṃ", 8),
    ("p", "निरुद्धं योगसेवया", "niruddhaṃ yogasevayā", 8),
    ("p", "यत्र चैवात्मनात्मानं", "yatra caivātmanātmānaṃ", 8),
    ("p", "पश्यन्नात्मनि तुष्यति", "paśyannātmani tuṣyati", 8),
],

"6.21": [
    ("p", "सुखमात्यन्तिकं यत्तद्", "sukhamātyantikaṃ yattad", 8),
    ("p", "बुद्धिग्राह्यमतीन्द्रियम्", "buddhigrāhyamatīndriyam", 8),
    ("p", "वेत्ति यत्र न चैवायं", "vetti yatra na caivāyaṃ", 8),
    ("p", "स्थितश्चलति तत्त्वतः", "sthitaścalati tattvataḥ", 8),
],

"6.22": [
    ("p", "यं लब्ध्वा चापरं लाभं", "yaṃ labdhvā cāparaṃ lābhaṃ", 8),
    ("p", "मन्यते नाधिकं ततः", "manyate nādhikaṃ tataḥ", 8),
    ("p", "यस्मिन्स्थितो न दुःखेन", "yasminsthito na duḥkhena", 8),
    ("p", "गुरुणापि विचाल्यते", "guruṇāpi vicālyate", 8),
],

"6.23": [
    ("p", "तं विद्याद्दुःखसंयोग", "taṃ vidyādduḥkhasaṃyoga", 8),
    ("p", "वियोगं योगसंज्ञितम्", "viyogaṃ yogasaṃjñitam", 8),
    ("p", "स निश्चयेन योक्तव्यो", "sa niścayena yoktavyo", 8),
    ("p", "योगोऽनिर्विण्णचेतसा", "yogo’nirviṇṇacetasā", 8),
],

"6.24": [
    ("p", "सङ्कल्पप्रभवान्कामांस्", "saṅkalpaprabhavānkāmāṃs", 8),
    ("p", "त्यक्त्वा सर्वानशेषतः", "tyaktvā sarvānaśeṣataḥ", 8),
    ("p", "मनसैवेन्द्रियग्रामं", "manasaivendriyagrāmaṃ", 8),
    ("p", "विनियम्य समन्ततः", "viniyamya samantataḥ", 8),
],

"6.25": [
    ("p", "शनैः शनैरुपरमेद्", "śanaiḥ śanairuparamed", 8),
    ("p", "बुद्ध्या धृतिगृहीतया", "buddhyā dhṛtigṛhītayā", 8),
    ("p", "आत्मसंस्थं मनः कृत्वा", "ātmasaṃsthaṃ manaḥ kṛtvā", 8),
    ("p", "न किञ्चिदपि चिन्तयेत्", "na kiñcidapi cintayet", 8),
],

"6.26": [
    ("p", "यतो यतो निश्चरति", "yato yato niścarati", 8),
    ("p", "मनश्चञ्चलमस्थिरम्", "manaścañcalamasthiram", 8),
    ("p", "ततस्ततो नियम्यैत", "tatastato niyamyaita", 8),
    ("p", "दात्मन्येव वशं नयेत्", "dātmanyeva vaśaṃ nayet", 8),
],

"6.27": [
    ("p", "प्रशान्तमनसं ह्येनं", "praśāntamanasaṃ hyenaṃ", 8),
    ("p", "योगिनं सुखमुत्तमम्", "yoginaṃ sukhamuttamam", 8),
    ("p", "उपैति शान्तरजसं", "upaiti śāntarajasaṃ", 8),
    ("p", "ब्रह्मभूतमकल्मषम्", "brahmabhūtamakalmaṣam", 8),
],

"6.28": [
    ("p", "युञ्जन्नेवं सदात्मानं", "yuñjannevaṃ sadātmānaṃ", 8),
    ("p", "योगी विगतकल्मषः", "yogī vigatakalmaṣaḥ", 8),
    ("p", "सुखेन ब्रह्मसंस्पर्शम्", "sukhena brahmasaṃsparśam", 8),
    ("p", "अत्यन्तं सुखमश्नुते", "atyantaṃ sukhamaśnute", 8),
],

"6.29": [
    ("p", "सर्वभूतस्थमात्मानं", "sarvabhūtasthamātmānaṃ", 8),
    ("p", "सर्वभूतानि चात्मनि", "sarvabhūtāni cātmani", 8),
    ("p", "ईक्षते योगयुक्तात्मा", "īkṣate yogayuktātmā", 8),
    ("p", "सर्वत्र समदर्शनः", "sarvatra samadarśanaḥ", 8),
],

"6.30": [
    ("p", "यो मां पश्यति सर्वत्र", "yo māṃ paśyati sarvatra", 8),
    ("p", "सर्वं च मयि पश्यति", "sarvaṃ ca mayi paśyati", 8),
    ("p", "तस्याहं न प्रणश्यामि", "tasyāhaṃ na praṇaśyāmi", 8),
    ("p", "स च मे न प्रणश्यति", "sa ca me na praṇaśyati", 8),
],

"6.31": [
    ("p", "सर्वभूतस्थितं यो मां", "sarvabhūtasthitaṃ yo māṃ", 8),
    ("p", "भजत्येकत्वमास्थितः", "bhajatyekatvamāsthitaḥ", 8),
    ("p", "सर्वथा वर्तमानोऽपि", "sarvathā vartamāno’pi", 8),
    ("p", "स योगी मयि वर्तते", "sa yogī mayi vartate", 8),
],

"6.32": [
    ("p", "आत्मौपम्येन सर्वत्र", "ātmaupamyena sarvatra", 8),
    ("p", "समं पश्यति योऽर्जुन", "samaṃ paśyati yo’rjuna", 8),
    ("p", "सुखं वा यदि वा दुःखं", "sukhaṃ vā yadi vā duḥkhaṃ", 8),
    ("p", "स योगी परमो मतः", "sa yogī paramo mataḥ", 8),
],

"6.33": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "योऽयं योगस्त्वया प्रोक्तः", "yo’yaṃ yogastvayā proktaḥ", 8),
    ("p", "साम्येन मधुसूदन", "sāmyena madhusūdana", 8),
    ("p", "एतस्याहं न पश्यामि", "etasyāhaṃ na paśyāmi", 8),
    ("p", "चञ्चलत्वात्स्थितिं स्थिराम्", "cañcalatvātsthitiṃ sthirām", 8),
],

"6.34": [
    ("p", "चञ्चलं हि मनः कृष्ण", "cañcalaṃ hi manaḥ kṛṣṇa", 8),
    ("p", "प्रमाथि बलवद्दृढम्", "pramāthi balavaddṛḍham", 8),
    ("p", "तस्याहं निग्रहं मन्ये", "tasyāhaṃ nigrahaṃ manye", 8),
    ("p", "वायोरिव सुदुष्करम्", "vāyoriva suduṣkaram", 8),
],

"6.35": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "असंशयं महाबाहो", "asaṃśayaṃ mahābāho", 8),
    ("p", "मनो दुर्निग्रहं चलम्", "mano durnigrahaṃ calam", 8),
    ("p", "अभ्यासेन तु कौन्तेय", "abhyāsena tu kaunteya", 8),
    ("p", "वैराग्येण च गृह्यते", "vairāgyeṇa ca gṛhyate", 8),
],

"6.36": [
    ("p", "असंयतात्मना योगो", "asaṃyatātmanā yogo", 8),
    ("p", "दुष्प्राप इति मे मतिः", "duṣprāpa iti me matiḥ", 8),
    ("p", "वश्यात्मना तु यतता", "vaśyātmanā tu yatatā", 8),
    ("p", "शक्योऽवाप्तुमुपायतः", "śakyo’vāptumupāyataḥ", 8),
],

"6.37": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "अयतिः श्रद्धयोपेतो", "ayatiḥ śraddhayopeto", 8),
    ("p", "योगाच्चलितमानसः", "yogāccalitamānasaḥ", 8),
    ("p", "अप्राप्य योगसंसिद्धिं", "aprāpya yogasaṃsiddhiṃ", 8),
    ("p", "कां गतिं कृष्ण गच्छति", "kāṃ gatiṃ kṛṣṇa gacchati", 8),
],

"6.38": [
    ("p", "कच्चिन्नोभयविभ्रष्टश्", "kaccinnobhayavibhraṣṭaś", 8),
    ("p", "छिन्नाभ्रमिव नश्यति", "chinnābhramiva naśyati", 8),
    ("p", "अप्रतिष्ठो महाबाहो", "apratiṣṭho mahābāho", 8),
    ("p", "विमूढो ब्रह्मणः पथि", "vimūḍho brahmaṇaḥ pathi", 8),
],

"6.39": [
    ("p", "एतन्मे संशयं कृष्ण", "etanme saṃśayaṃ kṛṣṇa", 8),
    ("p", "छेत्तुमर्हस्यशेषतः", "chettumarhasyaśeṣataḥ", 8),
    ("p", "त्वदन्यः संशयस्यास्य", "tvadanyaḥ saṃśayasyāsya", 8),
    ("p", "छेत्ता न ह्युपपद्यते", "chettā na hyupapadyate", 8),
],

"6.40": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "पार्थ नैवेह नामुत्र", "pārtha naiveha nāmutra", 8),
    ("p", "विनाशस्तस्य विद्यते", "vināśastasya vidyate", 8),
    ("p", "न हि कल्याणकृत्कश्चिद्", "na hi kalyāṇakṛtkaścid", 8),
    ("p", "दुर्गतिं तात गच्छति", "durgatiṃ tāta gacchati", 8),
],

"6.41": [
    ("p", "प्राप्य पुण्यकृतां लोकान्", "prāpya puṇyakṛtāṃ lokān", 8),
    ("p", "उषित्वा शाश्वतीः समाः", "uṣitvā śāśvatīḥ samāḥ", 8),
    ("p", "शुचीनां श्रीमतां गेहे", "śucīnāṃ śrīmatāṃ gehe", 8),
    ("p", "योगभ्रष्टोऽभिजायते", "yogabhraṣṭo’bhijāyate", 8),
],

"6.42": [
    ("p", "अथवा योगिनामेव", "athavā yogināmeva", 8),
    ("p", "कुले भवति धीमताम्", "kule bhavati dhīmatām", 8),
    ("p", "एतद्धि दुर्लभतरं", "etaddhi durlabhataraṃ", 8),
    ("p", "लोके जन्म यदीदृशम्", "loke janma yadīdṛśam", 8),
],

"6.43": [
    ("p", "तत्र तं बुद्धिसंयोगं", "tatra taṃ buddhisaṃyogaṃ", 8),
    ("p", "लभते पौर्वदेहिकम्", "labhate paurvadehikam", 8),
    ("p", "यतते च ततो भूयः", "yatate ca tato bhūyaḥ", 8),
    ("p", "संसिद्धौ कुरुनन्दन", "saṃsiddhau kurunandana", 8),
],

"6.44": [
    ("p", "पूर्वाभ्यासेन तेनैव", "pūrvābhyāsena tenaiva", 8),
    ("p", "ह्रियते ह्यवशोऽपि सः", "hriyate hyavaśo’pi saḥ", 8),
    ("p", "जिज्ञासुरपि योगस्य", "jijñāsurapi yogasya", 8),
    ("p", "शब्दब्रह्मातिवर्तते", "śabdabrahmātivartate", 8),
],

"6.45": [
    ("p", "प्रयत्नाद्यतमानस्तु", "prayatnādyatamānastu", 8),
    ("p", "योगी संशुद्धकिल्बिषः", "yogī saṃśuddhakilbiṣaḥ", 8),
    ("p", "अनेकजन्मसंसिद्धस्", "anekajanmasaṃsiddhas", 8),
    ("p", "ततो याति परां गतिम्", "tato yāti parāṃ gatim", 8),
],

"6.46": [
    ("p", "तपस्विभ्योऽधिको योगी", "tapasvibhyo’dhiko yogī", 8),
    ("p", "ज्ञानिभ्योऽपि मतोऽधिकः", "jñānibhyo’pi mato’dhikaḥ", 8),
    ("p", "कर्मिभ्यश्चाधिको योगी", "karmibhyaścādhiko yogī", 8),
    ("p", "तस्माद्योगी भवार्जुन", "tasmādyogī bhavārjuna", 8),
],

"6.47": [
    ("p", "योगिनामपि सर्वेषां", "yogināmapi sarveṣāṃ", 8),
    ("p", "मद्गतेनान्तरात्मना", "madgatenāntarātmanā", 8),
    ("p", "श्रद्धावान्भजते यो मां", "śraddhāvānbhajate yo māṃ", 8),
    ("p", "स मे युक्ततमो मतः", "sa me yuktatamo mataḥ", 8),
],

}
