# -*- coding: utf-8 -*-
"""padas_ch12.py — the pāda (quarter) division of every verse in chapter 12.

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
printed verbatim from ch12.json.
"""

GITA_CH12_PADAS = {
"12.01": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "एवं सततयुक्ता ये", "evaṃ satatayuktā ye", 8),
    ("p", "भक्तास्त्वां पर्युपासते", "bhaktāstvāṃ paryupāsate", 8),
    ("p", "ये चाप्यक्षरमव्यक्तं", "ye cāpyakṣaramavyaktaṃ", 8),
    ("p", "तेषां के योगवित्तमाः", "teṣāṃ ke yogavittamāḥ", 8),
],

"12.02": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "मय्यावेश्य मनो ये मां", "mayyāveśya mano ye māṃ", 8),
    ("p", "नित्ययुक्ता उपासते", "nityayuktā upāsate", 8),
    ("p", "श्रद्धया परयोपेताः", "śraddhayā parayopetāḥ", 8),
    ("p", "ते मे युक्ततमा मताः", "te me yuktatamā matāḥ", 8),
],

"12.03": [
    ("p", "ये त्वक्षरमनिर्देश्यं", "ye tvakṣaramanirdeśyaṃ", 8),
    ("p", "अव्यक्तं पर्युपासते", "avyaktaṃ paryupāsate", 8),
    ("p", "सर्वत्रगमचिन्त्यं च", "sarvatragamacintyaṃ ca", 8),
    ("p", "कूटस्थमचलं ध्रुवम्", "kūṭasthamacalaṃ dhruvam", 8),
],

"12.04": [
    ("p", "सन्नियम्येन्द्रियग्रामं", "sanniyamyendriyagrāmaṃ", 8),
    ("p", "सर्वत्र समबुद्धयः", "sarvatra samabuddhayaḥ", 8),
    ("p", "ते प्राप्नुवन्ति मामेव", "te prāpnuvanti māmeva", 8),
    ("p", "सर्वभूतहिते रताः", "sarvabhūtahite ratāḥ", 8),
],

"12.05": [
    ("p", "क्लेशोऽधिकतरस्तेषां", "kleśo’dhikatarasteṣāṃ", 8),
    ("p", "अव्यक्तासक्तचेतसाम्", "avyaktāsaktacetasām", 8),
    ("p", "अव्यक्ता हि गतिर्दुःखं", "avyaktā hi gatirduḥkhaṃ", 8),
    ("p", "देहवद्भिरवाप्यते", "dehavadbhiravāpyate", 8),
],

"12.06": [
    ("p", "ये तु सर्वाणि कर्माणि", "ye tu sarvāṇi karmāṇi", 8),
    ("p", "मयि सन्न्यस्य मत्पराः", "mayi sannyasya matparāḥ", 8),
    ("p", "अनन्येनैव योगेन", "ananyenaiva yogena", 8),
    ("p", "मां ध्यायन्त उपासते", "māṃ dhyāyanta upāsate", 8),
],

"12.07": [
    ("p", "तेषामहं समुद्धर्ता", "teṣāmahaṃ samuddhartā", 8),
    ("p", "मृत्युसंसारसागरात्", "mṛtyusaṃsārasāgarāt", 8),
    ("p", "भवामि न चिरात्पार्थ", "bhavāmi na cirātpārtha", 8),
    ("p", "मय्यावेशितचेतसाम्", "mayyāveśitacetasām", 8),
],

"12.08": [
    ("p", "मय्येव मन आधत्स्व", "mayyeva mana ādhatsva", 8),
    ("p", "मयि बुद्धिं निवेशय", "mayi buddhiṃ niveśaya", 8),
    ("p", "निवसिष्यसि मय्येव", "nivasiṣyasi mayyeva", 8),
    ("p", "अत ऊर्ध्वं न संशयः", "ata ūrdhvaṃ na saṃśayaḥ", 8),
],

"12.09": [
    ("p", "अथ चित्तं समाधातुं", "atha cittaṃ samādhātuṃ", 8),
    ("p", "न शक्नोषि मयि स्थिरम्", "na śaknoṣi mayi sthiram", 8),
    ("p", "अभ्यासयोगेन ततो", "abhyāsayogena tato", 8),
    ("p", "मामिच्छाप्तुं धनञ्जय", "māmicchāptuṃ dhanañjaya", 8),
],

"12.10": [
    ("p", "अभ्यासेऽप्यसमर्थोऽसि", "abhyāse’pyasamartho’si", 8),
    ("p", "मत्कर्मपरमो भव", "matkarmaparamo bhava", 8),
    ("p", "मदर्थमपि कर्माणि", "madarthamapi karmāṇi", 8),
    ("p", "कुर्वन्सिद्धिमवाप्स्यसि", "kurvansiddhimavāpsyasi", 8),
],

"12.11": [
    ("p", "अथैतदप्यशक्तोऽसि", "athaitadapyaśakto’si", 8),
    ("p", "कर्तुं मद्योगमाश्रितः", "kartuṃ madyogamāśritaḥ", 8),
    ("p", "सर्वकर्मफलत्यागं", "sarvakarmaphalatyāgaṃ", 8),
    ("p", "ततः कुरु यतात्मवान्", "tataḥ kuru yatātmavān", 8),
],

"12.12": [
    ("p", "श्रेयो हि ज्ञानमभ्यासात्", "śreyo hi jñānamabhyāsāt", 8),
    ("p", "ज्ञानाद्ध्यानं विशिष्यते", " jñānāddhyānaṃ viśiṣyate", 8),
    ("p", "ध्यानात्कर्मफलत्यागस्", "dhyānātkarmaphalatyāgas", 8),
    ("p", "त्यागाच्छान्तिरनन्तरम्", "tyāgācchāntiranantaram", 8),
],

"12.13": [
    ("p", "अद्वेष्टा सर्वभूतानां", "adveṣṭā sarvabhūtānāṃ", 8),
    ("p", "मैत्रः करुण एव च", "maitraḥ karuṇa eva ca", 8),
    ("p", "निर्ममो निरहङ्कारः", "nirmamo nirahaṅkāraḥ", 8),
    ("p", "समदुःखसुखः क्षमी", "samaduḥkhasukhaḥ kṣamī", 8),
],

"12.14": [
    ("p", "सन्तुष्टः सततं योगी", "santuṣṭaḥ satataṃ yogī", 8),
    ("p", "यतात्मा दृढनिश्चयः", "yatātmā dṛḍhaniścayaḥ", 8),
    ("p", "मय्यर्पितमनोबुद्धिर्", "mayyarpitamanobuddhir", 8),
    ("p", "यो मद्भक्तः स मे प्रियः", "yo madbhaktaḥ sa me priyaḥ", 8),
],

"12.15": [
    ("p", "यस्मान्नोद्विजते लोको", "yasmānnodvijate loko", 8),
    ("p", "लोकान्नोद्विजते च यः", "lokānnodvijate ca yaḥ", 8),
    ("p", "हर्षामर्षभयोद्वेगैर्", "harṣāmarṣabhayodvegair", 8),
    ("p", "मुक्तो यः स च मे प्रियः", "mukto yaḥ sa ca me priyaḥ", 8),
],

"12.16": [
    ("p", "अनपेक्षः शुचिर्दक्ष", "anapekṣaḥ śucirdakṣa", 8),
    ("p", "उदासीनो गतव्यथः", "udāsīno gatavyathaḥ", 8),
    ("p", "सर्वारम्भपरित्यागी", "sarvārambhaparityāgī", 8),
    ("p", "यो मद्भक्तः स मे प्रियः", "yo madbhaktaḥ sa me priyaḥ", 8),
],

"12.17": [
    ("p", "यो न हृष्यति न द्वेष्टि", "yo na hṛṣyati na dveṣṭi", 8),
    ("p", "न शोचति न काङ्क्षति", "na śocati na kāṅkṣati", 8),
    ("p", "शुभाशुभपरित्यागी", "śubhāśubhaparityāgī", 8),
    ("p", "भक्तिमान्यः स मे प्रियः", "bhaktimānyaḥ sa me priyaḥ", 8),
],

"12.18": [
    ("p", "समः शत्रौ च मित्रे च", "samaḥ śatrau ca mitre ca", 8),
    ("p", "तथा मानापमानयोः", "tathā mānāpamānayoḥ", 8),
    ("p", "शीतोष्णसुखदुःखेषु", "śītoṣṇasukhaduḥkheṣu", 8),
    ("p", "समः सङ्गविवर्जितः", "samaḥ saṅgavivarjitaḥ", 8),
],

"12.19": [
    ("p", "तुल्यनिन्दास्तुतिर्मौनी", "tulyanindāstutirmaunī", 8),
    ("p", "सन्तुष्टो येन केनचित्", "santuṣṭo yena kenacit", 8),
    ("p", "अनिकेतः स्थिरमतिर्", "aniketaḥ sthiramatir", 8),
    ("p", "भक्तिमान्मे प्रियो नरः", "bhaktimānme priyo naraḥ", 8),
],

"12.20": [
    ("p", "ये तु धर्म्यामृतमिदं", "ye tu dharmyāmṛtamidaṃ", 8),
    ("p", "यथोक्तं पर्युपासते", "yathoktaṃ paryupāsate", 8),
    ("p", "श्रद्दधाना मत्परमाः", "śraddadhānā matparamāḥ", 8),
    ("p", "भक्तास्तेऽतीव मे प्रियाः", "bhaktāste’tīva me priyāḥ", 8),
],

}
