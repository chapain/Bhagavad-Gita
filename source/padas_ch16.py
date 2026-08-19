# -*- coding: utf-8 -*-
"""padas_ch16.py — the pāda (quarter) division of every verse in chapter 16.

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
printed verbatim from ch16.json.
"""

GITA_CH16_PADAS = {
"16.01": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "अभयं सत्त्वसंशुद्धिर्", "abhayaṃ sattvasaṃśuddhir", 8),
    ("p", "ज्ञानयोगव्यवस्थितिः", "jñānayogavyavasthitiḥ", 8),
    ("p", "दानं दमश्च यज्ञश्च", "dānaṃ damaśca yajñaśca", 8),
    ("p", "स्वाध्यायस्तप आर्जवम्", "svādhyāyastapa ārjavam", 8),
],

"16.02": [
    ("p", "अहिंसा सत्यमक्रोधस्", "ahiṃsā satyamakrodhas", 8),
    ("p", "त्यागः शान्तिरपैशुनम्", "tyāgaḥ śāntirapaiśunam", 8),
    ("p", "दया भूतेष्वलोलुप्त्वं", "dayā bhūteṣvaloluptvaṃ", 8),
    ("p", "मार्दवं ह्रीरचापलम्", "mārdavaṃ hrīracāpalam", 8),
],

"16.03": [
    ("p", "तेजः क्षमा धृतिः शौचम्", "tejaḥ kṣamā dhṛtiḥ śaucam", 8),
    ("p", "अद्रोहो नातिमानिता", "adroho nātimānitā", 8),
    ("p", "भवन्ति सम्पदं दैवीम्", "bhavanti sampadaṃ daivīm", 8),
    ("p", "अभिजातस्य भारत", "abhijātasya bhārata", 8),
],

"16.04": [
    ("p", "दम्भो दर्पोऽतिमानश्च", "dambho darpo’timānaśca", 8),
    ("p", "क्रोधः पारुष्यमेव च", "krodhaḥ pāruṣyameva ca", 8),
    ("p", "अज्ञानं चाभिजातस्य", "ajñānaṃ cābhijātasya", 8),
    ("p", "पार्थ सम्पदमासुरीम्", "pārtha sampadamāsurīm", 8),
],

"16.05": [
    ("p", "दैवी सम्पद्विमोक्षाय", "daivī sampadvimokṣāya", 8),
    ("p", "निबन्धायासुरी मता", "nibandhāyāsurī matā", 8),
    ("p", "मा शुचः", "mā śucaḥ", 3),
    ("p", "सम्पदं दैवीमभिजातोऽसि पाण्डव", " sampadaṃ daivīmabhijāto’si pāṇḍava", 13),
],

"16.06": [
    ("p", "द्वौ भूतसर्गौ लोकेऽस्मिन्", "dvau bhūtasargau loke’smin", 8),
    ("p", "दैव आसुर एव च", "daiva āsura eva ca", 8),
    ("p", "दैवो विस्तरशः प्रोक्त", "daivo vistaraśaḥ prokta", 8),
    ("p", "आसुरं पार्थ मे शृणु", "āsuraṃ pārtha me śṛṇu", 8),
],

"16.07": [
    ("p", "प्रवृत्तिं च निवृत्तिं च", "pravṛttiṃ ca nivṛttiṃ ca", 8),
    ("p", "जना न विदुरासुराः", "janā na vidurāsurāḥ", 8),
    ("p", "न शौचं नापि चाचारो", "na śaucaṃ nāpi cācāro", 8),
    ("p", "न सत्यं तेषु विद्यते", "na satyaṃ teṣu vidyate", 8),
],

"16.08": [
    ("p", "असत्यमप्रतिष्ठं ते", "asatyamapratiṣṭhaṃ te", 8),
    ("p", "जगदाहुरनीश्वरम्", "jagadāhuranīśvaram", 8),
    ("p", "अपरस्परसम्भूतं", "aparasparasambhūtaṃ", 8),
    ("p", "किमन्यत्कामहैतुकम्", "kimanyatkāmahaitukam", 8),
],

"16.09": [
    ("p", "एतां दृष्टिमवष्टभ्य", "etāṃ dṛṣṭimavaṣṭabhya", 8),
    ("p", "नष्टात्मानोऽल्पबुद्धयः", "naṣṭātmāno’lpabuddhayaḥ", 8),
    ("p", "प्रभवन्त्युग्रकर्माणः", "prabhavantyugrakarmāṇaḥ", 8),
    ("p", "क्षयाय जगतोऽहिताः", "kṣayāya jagato’hitāḥ", 8),
],

"16.10": [
    ("p", "काममाश्रित्य दुष्पूरं", "kāmamāśritya duṣpūraṃ", 8),
    ("p", "दम्भमानमदान्विताः", "dambhamānamadānvitāḥ", 8),
    ("p", "मोहाद्गृहीत्वाऽसद्ग्राहान्", "mohādgṛhītvā’sadgrāhān", 8),
    ("p", "प्रवर्तन्तेऽशुचिव्रताः", "pravartante’śucivratāḥ", 8),
],

"16.11": [
    ("p", "चिन्तामपरिमेयां च", "cintāmaparimeyāṃ ca", 8),
    ("p", "प्रलयान्तामुपाश्रिताः", "pralayāntāmupāśritāḥ", 8),
    ("p", "कामोपभोगपरमा", "kāmopabhogaparamā", 8),
    ("p", "एतावदिति निश्चिताः", "etāvaditi niścitāḥ", 8),
],

"16.12": [
    ("p", "आशापाशशतैर्बद्धाः", "āśāpāśaśatairbaddhāḥ", 8),
    ("p", "कामक्रोधपरायणाः", "kāmakrodhaparāyaṇāḥ", 8),
    ("p", "ईहन्ते कामभोगार्थम्", "īhante kāmabhogārtham", 8),
    ("p", "अन्यायेनार्थसञ्चयान्", "anyāyenārthasañcayān", 8),
],

"16.13": [
    ("p", "इदमद्य मया लब्धम्", "idamadya mayā labdham", 8),
    ("p", "इदं प्राप्स्ये मनोरथम्", "idaṃ prāpsye manoratham", 8),
    ("p", "इदमस्तीदमपि मे", "idamastīdamapi me", 8),
    ("p", "भविष्यति पुनर्धनम्", "bhaviṣyati punardhanam", 8),
],

"16.14": [
    ("p", "असौ मया हतः शत्रुर्", "asau mayā hataḥ śatrur", 8),
    ("p", "हनिष्ये चापरानपि", "haniṣye cāparānapi", 8),
    ("p", "ईश्वरोऽहमहं भोगी", "īśvaro’hamahaṃ bhogī", 8),
    ("p", "सिद्धोऽहं बलवान्सुखी", "siddho’haṃ balavānsukhī", 8),
],

"16.15": [
    ("p", "आढ्योऽभिजनवानस्मि", "āḍhyo’bhijanavānasmi", 8),
    ("p", "कोऽन्योऽस्ति सदृशो मया", "ko’nyo’sti sadṛśo mayā", 8),
    ("p", "यक्ष्ये दास्यामि मोदिष्य", "yakṣye dāsyāmi modiṣya", 8),
    ("p", "इत्यज्ञानविमोहिताः", "ityajñānavimohitāḥ", 8),
],

"16.16": [
    ("p", "अनेकचित्तविभ्रान्ता", "anekacittavibhrāntā", 8),
    ("p", "मोहजालसमावृताः", "mohajālasamāvṛtāḥ", 8),
    ("p", "प्रसक्ताः कामभोगेषु", "prasaktāḥ kāmabhogeṣu", 8),
    ("p", "पतन्ति नरकेऽशुचौ", "patanti narake’śucau", 8),
],

"16.17": [
    ("p", "आत्मसम्भाविताः स्तब्धा", "ātmasambhāvitāḥ stabdhā", 8),
    ("p", "धनमानमदान्विताः", "dhanamānamadānvitāḥ", 8),
    ("p", "यजन्ते नामयज्ञैस्ते", "yajante nāmayajñaiste", 8),
    ("p", "दम्भेनाविधिपूर्वकम्", "dambhenāvidhipūrvakam", 8),
],

"16.18": [
    ("p", "अहङ्कारं बलं दर्पं", "ahaṅkāraṃ balaṃ darpaṃ", 8),
    ("p", "कामं क्रोधं च संश्रिताः", "kāmaṃ krodhaṃ ca saṃśritāḥ", 8),
    ("p", "मामात्मपरदेहेषु", "māmātmaparadeheṣu", 8),
    ("p", "प्रद्विषन्तोऽभ्यसूयकाः", "pradviṣanto’bhyasūyakāḥ", 8),
],

"16.19": [
    ("p", "तानहं द्विषतः क्रूरान्", "tānahaṃ dviṣataḥ krūrān", 8),
    ("p", "संसारेषु नराधमान्", "saṃsāreṣu narādhamān", 8),
    ("p", "क्षिपाम्यजस्रमशुभान्", "kṣipāmyajasramaśubhā", 8),
    ("p", "आसुरीष्वेव योनिषु", "nāsurīṣveva yoniṣu", 8),
],

"16.20": [
    ("p", "आसुरीं योनिमापन्ना", "āsurīṃ yonimāpannā", 8),
    ("p", "मूढा जन्मनि जन्मनि", "mūḍhā janmani janmani", 8),
    ("p", "मामप्राप्यैव कौन्तेय", "māmaprāpyaiva kaunteya", 8),
    ("p", "ततो यान्त्यधमां गतिम्", "tato yāntyadhamāṃ gatim", 8),
],

"16.21": [
    ("p", "त्रिविधं नरकस्येदं", "trividhaṃ narakasyedaṃ", 8),
    ("p", "द्वारं नाशनमात्मनः", "dvāraṃ nāśanamātmanaḥ", 8),
    ("p", "कामः क्रोधस्तथा लोभस्", "kāmaḥ krodhastathā lobhas", 8),
    ("p", "तस्मादेतत्त्रयं त्यजेत्", "tasmādetattrayaṃ tyajet", 8),
],

"16.22": [
    ("p", "एतैर्विमुक्तः कौन्तेय", "etairvimuktaḥ kaunteya", 8),
    ("p", "तमोद्वारैस्त्रिभिर्नरः", "tamodvāraistribhirnaraḥ", 8),
    ("p", "आचरत्यात्मनः श्रेयस्", "ācaratyātmanaḥ śreyas", 8),
    ("p", "ततो याति परां गतिम्", "tato yāti parāṃ gatim", 8),
],

"16.23": [
    ("p", "यः शास्त्रविधिमुत्सृज्य", "yaḥ śāstravidhimutsṛjya", 8),
    ("p", "वर्तते कामकारतः", "vartate kāmakārataḥ", 8),
    ("p", "न स सिद्धिमवाप्नोति", "na sa siddhimavāpnoti", 8),
    ("p", "न सुखं न परां गतिम्", "na sukhaṃ na parāṃ gatim", 8),
],

"16.24": [
    ("p", "तस्माच्छास्त्रं प्रमाणं ते", "tasmācchāstraṃ pramāṇaṃ te", 8),
    ("p", "कार्याकार्यव्यवस्थितौ", "kāryākāryavyavasthitau", 8),
    ("p", "ज्ञात्वा शास्त्रविधानोक्तं", "jñātvā śāstravidhānoktaṃ", 8),
    ("p", "कर्म कर्तुमिहार्हसि", "karma kartumihārhasi", 8),
],

}
