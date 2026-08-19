# -*- coding: utf-8 -*-
"""padas_ch14.py — the pāda (quarter) division of every verse in chapter 14.

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
printed verbatim from ch14.json.
"""

GITA_CH14_PADAS = {
"14.01": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "परं भूयः प्रवक्ष्यामि", "paraṃ bhūyaḥ pravakṣyāmi", 8),
    ("p", "ज्ञानानां ज्ञानमुत्तमम्", "jñānānāṃ jñānamuttamam", 8),
    ("p", "यज्ज्ञात्वा मुनयः सर्वे", "yajjñātvā munayaḥ sarve", 8),
    ("p", "परां सिद्धिमितो गताः", "parāṃ siddhimito gatāḥ", 8),
],

"14.02": [
    ("p", "इदं ज्ञानमुपाश्रित्य", "idaṃ jñānamupāśritya", 8),
    ("p", "मम साधर्म्यमागताः", "mama sādharmyamāgatāḥ", 8),
    ("p", "सर्गेऽपि नोपजायन्ते", "sarge’pi nopajāyante", 8),
    ("p", "प्रलये न व्यथन्ति च", "pralaye na vyathanti ca", 8),
],

"14.03": [
    ("p", "मम योनिर्महद्ब्रह्म", "mama yonirmahadbrahma", 8),
    ("p", "तस्मिन्गर्भं दधाम्यहम्", "tasmingarbhaṃ dadhāmyaham", 8),
    ("p", "सम्भवः सर्वभूतानां", "sambhavaḥ sarvabhūtānāṃ", 8),
    ("p", "ततो भवति भारत", "tato bhavati bhārata", 8),
],

"14.04": [
    ("p", "सर्वयोनिषु कौन्तेय", "sarvayoniṣu kaunteya", 8),
    ("p", "मूर्तयः सम्भवन्ति याः", "mūrtayaḥ sambhavanti yāḥ", 8),
    ("p", "तासां ब्रह्म महद्योनिर्", "tāsāṃ brahma mahadyonir", 8),
    ("p", "अहं बीजप्रदः पिता", "ahaṃ bījapradaḥ pitā", 8),
],

"14.05": [
    ("p", "सत्त्वं रजस्तम इति", "sattvaṃ rajastama iti", 8),
    ("p", "गुणाः प्रकृतिसम्भवाः", "guṇāḥ prakṛtisambhavāḥ", 8),
    ("p", "निबध्नन्ति महाबाहो", "nibadhnanti mahābāho", 8),
    ("p", "देहे देहिनमव्ययम्", "dehe dehinamavyayam", 8),
],

"14.06": [
    ("p", "तत्र सत्त्वं निर्मलत्वात्", "tatra sattvaṃ nirmalatvāt", 8),
    ("p", "प्रकाशकमनामयम्", "prakāśakamanāmayam", 8),
    ("p", "सुखसङ्गेन बध्नाति", "sukhasaṅgena badhnāti", 8),
    ("p", "ज्ञानसङ्गेन चानघ", "jñānasaṅgena cānagha", 8),
],

"14.07": [
    ("p", "रजो रागात्मकं विद्धि", "rajo rāgātmakaṃ viddhi", 8),
    ("p", "तृष्णासङ्गसमुद्भवम्", "tṛṣṇāsaṅgasamudbhavam", 8),
    ("p", "तन्निबध्नाति कौन्तेय", "tannibadhnāti kaunteya", 8),
    ("p", "कर्मसङ्गेन देहिनम्", "karmasaṅgena dehinam", 8),
],

"14.08": [
    ("p", "तमस्त्वज्ञानजं विद्धि", "tamastvajñānajaṃ viddhi", 8),
    ("p", "मोहनं सर्वदेहिनाम्", "mohanaṃ sarvadehinām", 8),
    ("p", "प्रमादालस्यनिद्राभिस्", "pramādālasyanidrābhis", 8),
    ("p", "तन्निबध्नाति भारत", "tannibadhnāti bhārata", 8),
],

"14.09": [
    ("p", "सत्त्वं सुखे सञ्जयति", "sattvaṃ sukhe sañjayati", 8),
    ("p", "रजः कर्मणि भारत", "rajaḥ karmaṇi bhārata", 8),
    ("p", "ज्ञानमावृत्य तु तमः", "jñānamāvṛtya tu tamaḥ", 8),
    ("p", "प्रमादे सञ्जयत्युत", "pramāde sañjayatyuta", 8),
],

"14.10": [
    ("p", "रजस्तमश्चाभिभूय", "rajastamaścābhibhūya", 8),
    ("p", "सत्त्वं भवति भारत", "sattvaṃ bhavati bhārata", 8),
    ("p", "रजः सत्त्वं तमश्चैव", "rajaḥ sattvaṃ tamaścaiva", 8),
    ("p", "तमः सत्त्वं रजस्तथा", "tamaḥ sattvaṃ rajastathā", 8),
],

"14.11": [
    ("p", "सर्वद्वारेषु देहेऽस्मिन्", "sarvadvāreṣu dehe’smin", 8),
    ("p", "प्रकाश उपजायते", "prakāśa upajāyate", 8),
    ("p", "ज्ञानं यदा तदा विद्याद्", "jñānaṃ yadā tadā vidyād", 8),
    ("p", "विवृद्धं सत्त्वमित्युत", "vivṛddhaṃ sattvamityuta", 8),
],

"14.12": [
    ("p", "लोभः प्रवृत्तिरारम्भः", "lobhaḥ pravṛttirārambhaḥ", 8),
    ("p", "कर्मणामशमः स्पृहा", "karmaṇāmaśamaḥ spṛhā", 8),
    ("p", "रजस्येतानि जायन्ते", "rajasyetāni jāyante", 8),
    ("p", "विवृद्धे भरतर्षभ", "vivṛddhe bharatarṣabha", 8),
],

"14.13": [
    ("p", "अप्रकाशोऽप्रवृत्तिश्च", "aprakāśo’pravṛttiśca", 8),
    ("p", "प्रमादो मोह एव च", "pramādo moha eva ca", 8),
    ("p", "तमस्येतानि जायन्ते", "tamasyetāni jāyante", 8),
    ("p", "विवृद्धे कुरुनन्दन", "vivṛddhe kurunandana", 8),
],

"14.14": [
    ("p", "यदा सत्त्वे प्रवृद्धे तु", "yadā sattve pravṛddhe tu", 8),
    ("p", "प्रलयं याति देहभृत्", "pralayaṃ yāti dehabhṛt", 8),
    ("p", "तदोत्तमविदां लोकान्", "tadottamavidāṃ lokān", 8),
    ("p", "अमलान्प्रतिपद्यते", "amalānpratipadyate", 8),
],

"14.15": [
    ("p", "रजसि प्रलयं गत्वा", "rajasi pralayaṃ gatvā", 8),
    ("p", "कर्मसङ्गिषु जायते", "karmasaṅgiṣu jāyate", 8),
    ("p", "तथा प्रलीनस्तमसि", "tathā pralīnastamasi", 8),
    ("p", "मूढयोनिषु जायते", "mūḍhayoniṣu jāyate", 8),
],

"14.16": [
    ("p", "कर्मणः सुकृतस्याहुः", "karmaṇaḥ sukṛtasyāhuḥ", 8),
    ("p", "सात्त्विकं निर्मलं फलम्", "sāttvikaṃ nirmalaṃ phalam", 8),
    ("p", "रजसस्तु फलं दुःखम्", "rajasastu phalaṃ duḥkham", 8),
    ("p", "अज्ञानं तमसः फलम्", "ajñānaṃ tamasaḥ phalam", 8),
],

"14.17": [
    ("p", "सत्त्वात्सञ्जायते ज्ञानं", "sattvātsañjāyate jñānaṃ", 8),
    ("p", "रजसो लोभ एव च", "rajaso lobha eva ca", 8),
    ("p", "प्रमादमोहौ तमसो", "pramādamohau tamaso", 8),
    ("p", "भवतोऽज्ञानमेव च", "bhavato’jñānameva ca", 8),
],

"14.18": [
    ("p", "ऊर्ध्वं गच्छन्ति सत्त्वस्था", "ūrdhvaṃ gacchanti sattvasthā", 8),
    ("p", "मध्ये तिष्ठन्ति राजसाः", "madhye tiṣṭhanti rājasāḥ", 8),
    ("p", "जघन्यगुणवृत्तस्था", "jaghanyaguṇavṛttasthā", 8),
    ("p", "अधो गच्छन्ति तामसाः", "adho gacchanti tāmasāḥ", 8),
],

"14.19": [
    ("p", "नान्यं गुणेभ्यः कर्तारं", "nānyaṃ guṇebhyaḥ kartāraṃ", 8),
    ("p", "यदा द्रष्टानुपश्यति", "yadā draṣṭānupaśyati", 8),
    ("p", "गुणेभ्यश्च परं वेत्ति", "guṇebhyaśca paraṃ vetti", 8),
    ("p", "मद्भावं सोऽधिगच्छति", "madbhāvaṃ so’dhigacchati", 8),
],

"14.20": [
    ("p", "गुणानेतानतीत्य त्रीन्", "guṇānetānatītya trīn", 8),
    ("p", "देही देहसमुद्भवान्", "dehī dehasamudbhavān", 8),
    ("p", "जन्ममृत्युजरादुःखैर्", "janmamṛtyujarāduḥkhair", 8),
    ("p", "विमुक्तोऽमृतमश्नुते", "vimukto’mṛtamaśnute", 8),
],

"14.21": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "कैर्लिङ्गैस्त्रीन्गुणानेतान्", "kairliṅgaistrīnguṇānetān", 8),
    ("p", "अतीतो भवति प्रभो", "atīto bhavati prabho", 8),
    ("p", "किमाचारः कथं चैतां", "kimācāraḥ kathaṃ caitāṃ", 8),
    ("p", "स्त्रीन्गुणानतिवर्तते", "strīnguṇānativartate", 8),
],

"14.22": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "प्रकाशं च प्रवृत्तिं च", "prakāśaṃ ca pravṛttiṃ ca", 8),
    ("p", "मोहमेव च पाण्डव", "mohameva ca pāṇḍava", 8),
    ("p", "न द्वेष्टि सम्प्रवृत्तानि", "na dveṣṭi sampravṛttāni", 8),
    ("p", "न निवृत्तानि काङ्क्षति", "na nivṛttāni kāṅkṣati", 8),
],

"14.23": [
    ("p", "उदासीनवदासीनो", "udāsīnavadāsīno", 8),
    ("p", "गुणैर्यो न विचाल्यते", "guṇairyo na vicālyate", 8),
    ("p", "गुणा वर्तन्त इत्येव", "guṇā vartanta ityeva", 8),
    ("p", "योऽवतिष्ठति नेङ्गते", "yo’vatiṣṭhati neṅgate", 8),
],

"14.24": [
    ("p", "समदुःखसुखः स्वस्थः", "samaduḥkhasukhaḥ svasthaḥ", 8),
    ("p", "समलोष्टाश्मकाञ्चनः", "samaloṣṭāśmakāñcanaḥ", 8),
    ("p", "तुल्यप्रियाप्रियो धीरस्", "tulyapriyāpriyo dhīras", 8),
    ("p", "तुल्यनिन्दात्मसंस्तुतिः", "tulyanindātmasaṃstutiḥ", 8),
],

"14.25": [
    ("p", "मानापमानयोस्तुल्यस्", "mānāpamānayostulyas", 8),
    ("p", "तुल्यो मित्रारिपक्षयोः", "tulyo mitrāripakṣayoḥ", 8),
    ("p", "सर्वारम्भपरित्यागी", "sarvārambhaparityāgī", 8),
    ("p", "गुणातीतः स उच्यते", "guṇātītaḥ sa ucyate", 8),
],

"14.26": [
    ("p", "मां च योऽव्यभिचारेण", "māṃ ca yo’vyabhicāreṇa", 8),
    ("p", "भक्तियोगेन सेवते", "bhaktiyogena sevate", 8),
    ("p", "स गुणान्समतीत्यैतान्", "sa guṇānsamatītyaitān", 8),
    ("p", "ब्रह्मभूयाय कल्पते", "brahmabhūyāya kalpate", 8),
],

"14.27": [
    ("p", "ब्रह्मणो हि प्रतिष्ठाहम्", "brahmaṇo hi pratiṣṭhāham", 8),
    ("p", "अमृतस्याव्ययस्य च", "amṛtasyāvyayasya ca", 8),
    ("p", "शाश्वतस्य च धर्मस्य", "śāśvatasya ca dharmasya", 8),
    ("p", "सुखस्यैकान्तिकस्य च", "sukhasyaikāntikasya ca", 8),
],

}
