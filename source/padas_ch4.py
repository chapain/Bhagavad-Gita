# -*- coding: utf-8 -*-
"""padas_ch4.py — the pāda (quarter) division of every verse in chapter 4.

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
printed verbatim from ch4.json.
"""

GITA_CH4_PADAS = {
"4.01": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "इमं विवस्वते योगं", "imaṃ vivasvate yogaṃ", 8),
    ("p", "प्रोक्तवानहमव्ययम्", "proktavānahamavyayam", 8),
    ("p", "विवस्वान्मनवे प्राह", "vivasvānmanave prāha", 8),
    ("p", "मनुरिक्ष्वाकवेऽब्रवीत्", "manurikṣvākave’bravīt", 8),
],

"4.02": [
    ("p", "एवं परम्पराप्राप्तम्", "evaṃ paramparāprāptam", 8),
    ("p", "इमं राजर्षयो विदुः", "imaṃ rājarṣayo viduḥ", 8),
    ("p", "स कालेनेह महता", "sa kāleneha mahatā", 8),
    ("p", "योगो नष्टः परन्तप", "yogo naṣṭaḥ parantapa", 8),
],

"4.03": [
    ("p", "स एवायं मया तेऽद्य", "sa evāyaṃ mayā te’dya", 8),
    ("p", "योगः प्रोक्तः पुरातनः", "yogaḥ proktaḥ purātanaḥ", 8),
    ("p", "भक्तोऽसि मे सखा चेति", "bhakto’si me sakhā ceti", 8),
    ("p", "रहस्यं ह्येतदुत्तमम्", "rahasyaṃ hyetaduttamam", 8),
],

"4.04": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "अपरं भवतो जन्म", "aparaṃ bhavato janma", 8),
    ("p", "परं जन्म विवस्वतः", "paraṃ janma vivasvataḥ", 8),
    ("p", "कथमेतद्विजानीयां", "kathametadvijānīyāṃ", 8),
    ("p", "त्वमादौ प्रोक्तवानिति", "tvamādau proktavāniti", 8),
],

"4.05": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "बहूनि मे व्यतीतानि", "bahūni me vyatītāni", 8),
    ("p", "जन्मानि तव चार्जुन", "janmāni tava cārjuna", 8),
    ("p", "तान्यहं वेद सर्वाणि", "tānyahaṃ veda sarvāṇi", 8),
    ("p", "न त्वं वेत्थ परन्तप", "na tvaṃ vettha parantapa", 8),
],

"4.06": [
    ("p", "अजोऽपि सन्नव्ययात्मा", "ajo’pi sannavyayātmā", 8),
    ("p", "भूतानामीश्वरोऽपि सन्", "bhūtānāmīśvaro’pi san", 8),
    ("p", "प्रकृतिं स्वामधिष्ठाय", "prakṛtiṃ svāmadhiṣṭhāya", 8),
    ("p", "सम्भवाम्यात्ममायया", "sambhavāmyātmamāyayā", 8),
],

"4.07": [
    ("p", "यदा यदा हि धर्मस्य", "yadā yadā hi dharmasya", 8),
    ("p", "ग्लानिर्भवति भारत", "glānirbhavati bhārata", 8),
    ("p", "अभ्युत्थानमधर्मस्य", "abhyutthānamadharmasya", 8),
    ("p", "तदात्मानं सृजाम्यहम्", "tadātmānaṃ sṛjāmyaham", 8),
],

"4.08": [
    ("p", "परित्राणाय साधूनां", "paritrāṇāya sādhūnāṃ", 8),
    ("p", "विनाशाय च दुष्कृताम्", "vināśāya ca duṣkṛtām", 8),
    ("p", "धर्मसंस्थापनार्थाय", "dharmasaṃsthāpanārthāya", 8),
    ("p", "सम्भवामि युगे युगे", "sambhavāmi yuge yuge", 8),
],

"4.09": [
    ("p", "जन्म कर्म च मे दिव्यम्", "janma karma ca me divyam", 8),
    ("p", "एवं यो वेत्ति तत्त्वतः", "evaṃ yo vetti tattvataḥ", 8),
    ("p", "त्यक्त्वा देहं पुनर्जन्म", "tyaktvā dehaṃ punarjanma", 8),
    ("p", "नैति मामेति सोऽर्जुन", "naiti māmeti so’rjuna", 8),
],

"4.10": [
    ("p", "वीतरागभयक्रोधा", "vītarāgabhayakrodhā", 8),
    ("p", "मन्मया मामुपाश्रिताः", "manmayā māmupāśritāḥ", 8),
    ("p", "बहवो ज्ञानतपसा", "bahavo jñānatapasā", 8),
    ("p", "पूता मद्भावमागताः", "pūtā madbhāvamāgatāḥ", 8),
],

"4.11": [
    ("p", "ये यथा मां प्रपद्यन्ते", "ye yathā māṃ prapadyante", 8),
    ("p", "तांस्तथैव भजाम्यहम्", "tāṃstathaiva bhajāmyaham", 8),
    ("p", "मम वर्त्मानुवर्तन्ते", "mama vartmānuvartante", 8),
    ("p", "मनुष्याः पार्थ सर्वशः", "manuṣyāḥ pārtha sarvaśaḥ", 8),
],

"4.12": [
    ("p", "काङ्क्षन्तः कर्मणां सिद्धिं", "kāṅkṣantaḥ karmaṇāṃ siddhiṃ", 8),
    ("p", "यजन्त इह देवताः", "yajanta iha devatāḥ", 8),
    ("p", "क्षिप्रं हि मानुषे लोके", "kṣipraṃ hi mānuṣe loke", 8),
    ("p", "सिद्धिर्भवति कर्मजा", "siddhirbhavati karmajā", 8),
],

"4.13": [
    ("p", "चातुर्वर्ण्यं मया सृष्टं", "cāturvarṇyaṃ mayā sṛṣṭaṃ", 8),
    ("p", "गुणकर्मविभागशः", "guṇakarmavibhāgaśaḥ", 8),
    ("p", "तस्य कर्तारमपि मां", "tasya kartāramapi māṃ", 8),
    ("p", "विद्ध्यकर्तारमव्ययम्", "viddhyakartāramavyayam", 8),
],

"4.14": [
    ("p", "न मां कर्माणि लिम्पन्ति", "na māṃ karmāṇi limpanti", 8),
    ("p", "न मे कर्मफले स्पृहा", "na me karmaphale spṛhā", 8),
    ("p", "इति मां योऽभिजानाति", "iti māṃ yo’bhijānāti", 8),
    ("p", "कर्मभिर्न स बध्यते", "karmabhirna sa badhyate", 8),
],

"4.15": [
    ("p", "एवं ज्ञात्वा कृतं कर्म", "evaṃ jñātvā kṛtaṃ karma", 8),
    ("p", "पूर्वैरपि मुमुक्षुभिः", "pūrvairapi mumukṣubhiḥ", 8),
    ("p", "कुरु कर्मैव तस्मात्त्वं", "kuru karmaiva tasmāttvaṃ", 8),
    ("p", "पूर्वैः पूर्वतरं कृतम्", "pūrvaiḥ pūrvataraṃ kṛtam", 8),
],

"4.16": [
    ("p", "किं कर्म किमकर्मेति", "kiṃ karma kimakarmeti", 8),
    ("p", "कवयोऽप्यत्र मोहिताः", "kavayo’pyatra mohitāḥ", 8),
    ("p", "तत्ते कर्म प्रवक्ष्यामि", "tatte karma pravakṣyāmi", 8),
    ("p", "यज्ज्ञात्वा मोक्ष्यसेऽशुभात्", "yajjñātvā mokṣyase’śubhāt", 8),
],

"4.17": [
    ("p", "कर्मणो ह्यपि बोद्धव्यं", "karmaṇo hyapi boddhavyaṃ", 8),
    ("p", "बोद्धव्यं च विकर्मणः", "boddhavyaṃ ca vikarmaṇaḥ", 8),
    ("p", "अकर्मणश्च बोद्धव्यं", "akarmaṇaśca boddhavyaṃ", 8),
    ("p", "गहना कर्मणो गतिः", "gahanā karmaṇo gatiḥ", 8),
],

"4.18": [
    ("p", "कर्मण्यकर्म यः पश्येद्", "karmaṇyakarma yaḥ paśyed", 8),
    ("p", "अकर्मणि च कर्म यः", "akarmaṇi ca karma yaḥ", 8),
    ("p", "स बुद्धिमान्मनुष्येषु", "sa buddhimānmanuṣyeṣu", 8),
    ("p", "स युक्तः कृत्स्नकर्मकृत्", "sa yuktaḥ kṛtsnakarmakṛt", 8),
],

"4.19": [
    ("p", "यस्य सर्वे समारम्भाः", "yasya sarve samārambhāḥ", 8),
    ("p", "कामसङ्कल्पवर्जिताः", "kāmasaṅkalpavarjitāḥ", 8),
    ("p", "ज्ञानाग्निदग्धकर्माणं", "jñānāgnidagdhakarmāṇaṃ", 8),
    ("p", "तमाहुः पण्डितं बुधाः", "tamāhuḥ paṇḍitaṃ budhāḥ", 8),
],

"4.20": [
    ("p", "त्यक्त्वा कर्मफलासङ्गं", "tyaktvā karmaphalāsaṅgaṃ", 8),
    ("p", "नित्यतृप्तो निराश्रयः", "nityatṛpto nirāśrayaḥ", 8),
    ("p", "कर्मण्यभिप्रवृत्तोऽपि", "karmaṇyabhipravṛtto’pi", 8),
    ("p", "नैव किञ्चित्करोति सः", "naiva kiñcitkaroti saḥ", 8),
],

"4.21": [
    ("p", "निराशीर्यतचित्तात्मा", "nirāśīryatacittātmā", 8),
    ("p", "त्यक्तसर्वपरिग्रहः", "tyaktasarvaparigrahaḥ", 8),
    ("p", "शारीरं केवलं कर्म", "śārīraṃ kevalaṃ karma", 8),
    ("p", "कुर्वन्नाप्नोति किल्बिषम्", "kurvannāpnoti kilbiṣam", 8),
],

"4.22": [
    ("p", "यदृच्छालाभसन्तुष्टो", "yadṛcchālābhasantuṣṭo", 8),
    ("p", "द्वन्द्वातीतो विमत्सरः", "dvandvātīto vimatsaraḥ", 8),
    ("p", "समः सिद्धावसिद्धौच", "samaḥ siddhāvasiddhauca", 8),
    ("p", "कृत्वापि न निबध्यते", "kṛtvāpi na nibadhyate", 8),
],

"4.23": [
    ("p", "गतसङ्गस्य मुक्तस्य", "gatasaṅgasya muktasya", 8),
    ("p", "ज्ञानावस्थितचेतसः", "jñānāvasthitacetasaḥ", 8),
    ("p", "यज्ञायाचरतः कर्म", "yajñāyācarataḥ karma", 8),
    ("p", "समग्रं प्रविलीयते", "samagraṃ pravilīyate", 8),
],

"4.24": [
    ("p", "ब्रह्मार्पणं ब्रह्म हविर्", "brahmārpaṇaṃ brahma havir", 8),
    ("p", "ब्रह्माग्नौ ब्रह्मणा हुतम्", "brahmāgnau brahmaṇā hutam", 8),
    ("p", "ब्रह्मैव तेन गन्तव्यं", "brahmaiva tena gantavyaṃ", 8),
    ("p", "ब्रह्मकर्मसमाधिना", "brahmakarmasamādhinā", 8),
],

"4.25": [
    ("p", "दैवमेवापरे यज्ञं", "daivamevāpare yajñaṃ", 8),
    ("p", "योगिनः पर्युपासते", "yoginaḥ paryupāsate", 8),
    ("p", "ब्रह्माग्नावपरे यज्ञं", "brahmāgnāvapare yajñaṃ", 8),
    ("p", "यज्ञेनैवोपजुह्वति", "yajñenaivopajuhvati", 8),
],

"4.26": [
    ("p", "श्रोत्रादीनीन्द्रियाण्यन्ये", "śrotrādīnīndriyāṇyanye", 8),
    ("p", "संयमाग्निषु जुह्वति", "saṃyamāgniṣu juhvati", 8),
    ("p", "शब्दादीन्विषयानन्य", "śabdādīnviṣayānanya", 8),
    ("p", "इन्द्रियाग्निषु जुह्वति", "indriyāgniṣu juhvati", 8),
],

"4.27": [
    ("p", "सर्वाणीन्द्रियकर्माणि", "sarvāṇīndriyakarmāṇi", 8),
    ("p", "प्राणकर्माणि चापरे", "prāṇakarmāṇi cāpare", 8),
    ("p", "आत्मसंयमयोगाग्नौ", "ātmasaṃyamayogāgnau", 8),
    ("p", "जुह्वति ज्ञानदीपिते", "juhvati jñānadīpite", 8),
],

"4.28": [
    ("p", "द्रव्ययज्ञास्तपोयज्ञा", "dravyayajñāstapoyajñā", 8),
    ("p", "योगयज्ञास्तथापरे", "yogayajñāstathāpare", 8),
    ("p", "स्वाध्यायज्ञानयज्ञाश्च", "svādhyāyajñānayajñāśca", 8),
    ("p", "यतयः संशितव्रताः", "yatayaḥ saṃśitavratāḥ", 8),
],

"4.29": [
    ("p", "अपाने जुह्वति प्राणं", "apāne juhvati prāṇaṃ", 8),
    ("p", "प्राणेऽपानं तथापरे", "prāṇe’pānaṃ tathāpare", 8),
    ("p", "प्राणापानगती रुद्ध्वा", "prāṇāpānagatī ruddhvā", 8),
    ("p", "प्राणायामपरायणाः", "prāṇāyāmaparāyaṇāḥ", 8),
],

"4.30": [
    ("p", "अपरे नियताहाराः", "apare niyatāhārāḥ", 8),
    ("p", "प्राणान्प्राणेषु जुह्वति", "prāṇānprāṇeṣu juhvati", 8),
    ("p", "सर्वेऽप्येते यज्ञविदो", "sarve’pyete yajñavido", 8),
    ("p", "यज्ञक्षपितकल्मषाः", "yajñakṣapitakalmaṣāḥ", 8),
],

"4.31": [
    ("p", "यज्ञशिष्टामृतभुजो", "yajñaśiṣṭāmṛtabhujo", 8),
    ("p", "यान्ति ब्रह्म सनातनम्", "yānti brahma sanātanam", 8),
    ("p", "नायं लोकोऽस्त्ययज्ञस्य", "nāyaṃ loko’styayajñasya", 8),
    ("p", "कुतोऽन्यः कुरुसत्तम", "kuto’nyaḥ kurusattama", 8),
],

"4.32": [
    ("p", "एवं बहुविधा यज्ञा", "evaṃ bahuvidhā yajñā", 8),
    ("p", "वितता ब्रह्मणो मुखे", "vitatā brahmaṇo mukhe", 8),
    ("p", "कर्मजान्विद्धि तान्सर्वान्", "karmajānviddhi tānsarvān", 8),
    ("p", "एवं ज्ञात्वा विमोक्ष्यसे", "evaṃ jñātvā vimokṣyase", 8),
],

"4.33": [
    ("p", "श्रेयान्द्रव्यमयाद्यज्ञा", "śreyāndravyamayādyajñā", 8),
    ("p", "ज्ज्ञानयज्ञः परन्तप", "jjñānayajñaḥ parantapa", 8),
    ("p", "सर्वं कर्माखिलं पार्थ", "sarvaṃ karmākhilaṃ pārtha", 8),
    ("p", "ज्ञाने परिसमाप्यते", "jñāne parisamāpyate", 8),
],

"4.34": [
    ("p", "तद्विद्धि प्रणिपातेन", "tadviddhi praṇipātena", 8),
    ("p", "परिप्रश्नेन सेवया", "paripraśnena sevayā", 8),
    ("p", "उपदेक्ष्यन्ति ते ज्ञानं", "upadekṣyanti te jñānaṃ", 8),
    ("p", "ज्ञानिनस्तत्त्वदर्शिनः", "jñāninastattvadarśinaḥ", 8),
],

"4.35": [
    ("p", "यज्ज्ञात्वा न पुनर्मोहम्", "yajjñātvā na punarmoham", 8),
    ("p", "एवं यास्यसि पाण्डव", "evaṃ yāsyasi pāṇḍava", 8),
    ("p", "येन भूतान्यशेषेण", "yena bhūtānyaśeṣeṇa", 8),
    ("p", "द्रक्ष्यस्यात्मन्यथो मयि", "drakṣyasyātmanyatho mayi", 8),
],

"4.36": [
    ("p", "अपि चेदसि पापेभ्यः", "api cedasi pāpebhyaḥ", 8),
    ("p", "सर्वेभ्यः पापकृत्तमः", "sarvebhyaḥ pāpakṛttamaḥ", 8),
    ("p", "सर्वं ज्ञानप्लवेनैव", "sarvaṃ jñānaplavenaiva", 8),
    ("p", "वृजिनं सन्तरिष्यसि", "vṛjinaṃ santariṣyasi", 8),
],

"4.37": [
    ("p", "यथैधांसि समिद्धोऽग्निर्", "yathaidhāṃsi samiddho’gnir", 8),
    ("p", "भस्मसात्कुरुतेऽर्जुन", "bhasmasātkurute’rjuna", 8),
    ("p", "ज्ञानाग्निः सर्वकर्माणि", "jñānāgniḥ sarvakarmāṇi", 8),
    ("p", "भस्मसात्कुरुते तथा", "bhasmasātkurute tathā", 8),
],

"4.38": [
    ("p", "न हि ज्ञानेन सदृशं", "na hi jñānena sadṛśaṃ", 8),
    ("p", "पवित्रमिह विद्यते", "pavitramiha vidyate", 8),
    ("p", "तत्स्वयं योगसंसिद्धः", "tatsvayaṃ yogasaṃsiddhaḥ", 8),
    ("p", "कालेनात्मनि विन्दति", "kālenātmani vindati", 8),
],

"4.39": [
    ("p", "श्रद्धावांल्लभते ज्ञानं", "śraddhāvāṃllabhate jñānaṃ", 8),
    ("p", "तत्परः संयतेन्द्रियः", "tatparaḥ saṃyatendriyaḥ", 8),
    ("p", "ज्ञानं लब्ध्वा परां शान्तिम्", "jñānaṃ labdhvā parāṃ śāntim", 8),
    ("p", "अचिरेणाधिगच्छति", "acireṇādhigacchati", 8),
],

"4.40": [
    ("p", "अज्ञश्चाश्रद्दधानश्च", "ajñaścāśraddadhānaśca", 8),
    ("p", "संशयात्मा विनश्यति", "saṃśayātmā vinaśyati", 8),
    ("p", "नायं लोकोऽस्ति न परो", "nāyaṃ loko’sti na paro", 8),
    ("p", "न सुखं संशयात्मनः", "na sukhaṃ saṃśayātmanaḥ", 8),
],

"4.41": [
    ("p", "योगसन्न्यस्तकर्माणं", "yogasannyastakarmāṇaṃ", 8),
    ("p", "ज्ञानसञ्छिन्नसंशयम्", "jñānasañchinnasaṃśayam", 8),
    ("p", "आत्मवन्तं न कर्माणि", "ātmavantaṃ na karmāṇi", 8),
    ("p", "निबध्नन्ति धनञ्जय", "nibadhnanti dhanañjaya", 8),
],

"4.42": [
    ("p", "तस्मादज्ञानसम्भूतं", "tasmādajñānasambhūtaṃ", 8),
    ("p", "हृत्स्थं ज्ञानासिनात्मनः", "hṛtsthaṃ jñānāsinātmanaḥ", 8),
    ("p", "छित्त्वैनं संशयं योग", "chittvainaṃ saṃśayaṃ yoga", 8),
    ("p", "मातिष्ठोत्तिष्ठ भारत", "mātiṣṭhottiṣṭha bhārata", 8),
],

}
