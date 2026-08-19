# -*- coding: utf-8 -*-
"""padas_ch5.py — the pāda (quarter) division of every verse in chapter 5.

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
printed verbatim from ch5.json.
"""

GITA_CH5_PADAS = {
"5.01": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "सन्न्यासं कर्मणां कृष्ण", "sannyāsaṃ karmaṇāṃ kṛṣṇa", 8),
    ("p", "पुनर्योगं च शंससि", "punaryogaṃ ca śaṃsasi", 8),
    ("p", "यच्छ्रेय एतयोरेकं", "yacchreya etayorekaṃ", 8),
    ("p", "तन्मे ब्रूहि सुनिश्चितम्", "tanme brūhi suniścitam", 8),
],

"5.02": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "सन्न्यासः कर्मयोगश्च", "sannyāsaḥ karmayogaśca", 8),
    ("p", "निःश्रेयसकरावुभौ", "niḥśreyasakarāvubhau", 8),
    ("p", "तयोस्तु कर्मसन्न्यासात्", "tayostu karmasannyāsāt", 8),
    ("p", "कर्मयोगो विशिष्यते", "karmayogo viśiṣyate", 8),
],

"5.03": [
    ("p", "ज्ञेयः स नित्यसन्न्यासी", "jñeyaḥ sa nityasannyāsī", 8),
    ("p", "यो न द्वेष्टि न काङ्क्षति", "yo na dveṣṭi na kāṅkṣati", 8),
    ("p", "निर्द्वन्द्वो हि महाबाहो", "nirdvandvo hi mahābāho", 8),
    ("p", "सुखं बन्धात्प्रमुच्यते", "sukhaṃ bandhātpramucyate", 8),
],

"5.04": [
    ("p", "साङ्ख्ययोगौ पृथग्बालाः", "sāṅkhyayogau pṛthagbālāḥ", 8),
    ("p", "प्रवदन्ति न पण्डिताः", "pravadanti na paṇḍitāḥ", 8),
    ("p", "एकमप्यास्थितः सम्य", "ekamapyāsthitaḥ samya", 8),
    ("p", "गुभयोर्विन्दते फलम्", "gubhayorvindate phalam", 8),
],

"5.05": [
    ("p", "यत्साङ्ख्यैः प्राप्यते स्थानं", "yatsāṅkhyaiḥ prāpyate sthānaṃ", 8),
    ("p", "तद्योगैरपि गम्यते", "tadyogairapi gamyate", 8),
    ("p", "एकं साङ्ख्यं च योगं च", "ekaṃ sāṅkhyaṃ ca yogaṃ ca", 8),
    ("p", "यः पश्यति स पश्यति", "yaḥ paśyati sa paśyati", 8),
],

"5.06": [
    ("p", "सन्न्यासस्तु महाबाहो", "sannyāsastu mahābāho", 8),
    ("p", "दुःखमाप्तुमयोगतः", "duḥkhamāptumayogataḥ", 8),
    ("p", "योगयुक्तो मुनिर्ब्रह्म", "yogayukto munirbrahma", 8),
    ("p", "नचिरेणाधिगच्छति", "nacireṇādhigacchati", 8),
],

"5.07": [
    ("p", "योगयुक्तो विशुद्धात्मा", "yogayukto viśuddhātmā", 8),
    ("p", "विजितात्मा जितेन्द्रियः", "vijitātmā jitendriyaḥ", 8),
    ("p", "सर्वभूतात्मभूतात्मा", "sarvabhūtātmabhūtātmā", 8),
    ("p", "कुर्वन्नपि न लिप्यते", "kurvannapi na lipyate", 8),
],

"5.08": [
    ("p", "नैव किञ्चित्करोमीति", "naiva kiñcitkaromīti", 8),
    ("p", "युक्तो मन्येत तत्त्ववित्", "yukto manyeta tattvavit", 8),
    ("p", "पश्यञ्शृण्वन्स्पृशञ्जिघ्र", "paśyañśṛṇvanspṛśañjighra", 8),
    ("p", "न्नश्नन्गच्छन्स्वपञ्श्वसन्", "nnaśnangacchansvapañśvasan", 8),
],

"5.09": [
    ("p", "प्रलपन् विसृजन्गृह्ण", "pralapan visṛjangṛhṇa", 8),
    ("p", "न्नुन्मिषन्निमिषन्नपि", "nnunmiṣannimiṣannapi", 8),
    ("p", "इन्द्रियाणीन्द्रियार्थेषु", "indriyāṇīndriyārtheṣu", 8),
    ("p", "वर्तन्त इति धारयन्", "vartanta iti dhārayan", 8),
],

"5.10": [
    ("p", "ब्रह्मण्याधाय कर्माणि", "brahmaṇyādhāya karmāṇi", 8),
    ("p", "सङ्गं त्यक्त्वा करोति यः", "saṅgaṃ tyaktvā karoti yaḥ", 8),
    ("p", "लिप्यते न स पापेन", "lipyate na sa pāpena", 8),
    ("p", "पद्मपत्रमिवाम्भसा", "padmapatramivāmbhasā", 8),
],

"5.11": [
    ("p", "कायेन मनसा बुद्ध्या", "kāyena manasā buddhyā", 8),
    ("p", "केवलैरिन्द्रियैरपि", "kevalairindriyairapi", 8),
    ("p", "योगिनः कर्म कुर्वन्ति", "yoginaḥ karma kurvanti", 8),
    ("p", "सङ्गं त्यक्त्वात्मशुद्धये", "saṅgaṃ tyaktvātmaśuddhaye", 8),
],

"5.12": [
    ("p", "युक्तः कर्मफलं त्यक्त्वा", "yuktaḥ karmaphalaṃ tyaktvā", 8),
    ("p", "शान्तिमाप्नोति नैष्ठिकीम्", "śāntimāpnoti naiṣṭhikīm", 8),
    ("p", "अयुक्तः कामकारेण", "ayuktaḥ kāmakāreṇa", 8),
    ("p", "फले सक्तो निबध्यते", "phale sakto nibadhyate", 8),
],

"5.13": [
    ("p", "सर्वकर्माणि मनसा", "sarvakarmāṇi manasā", 8),
    ("p", "सन्न्यस्यास्ते सुखं वशी", "sannyasyāste sukhaṃ vaśī", 8),
    ("p", "नवद्वारे पुरे देही", "navadvāre pure dehī", 8),
    ("p", "नैव कुर्वन्न कारयन्", "naiva kurvanna kārayan", 8),
],

"5.14": [
    ("p", "न कर्तृत्वं न कर्माणि", "na kartṛtvaṃ na karmāṇi", 8),
    ("p", "लोकस्य सृजति प्रभुः", "lokasya sṛjati prabhuḥ", 8),
    ("p", "न कर्मफलसंयोगं", "na karmaphalasaṃyogaṃ", 8),
    ("p", "स्वभावस्तु प्रवर्तते", "svabhāvastu pravartate", 8),
],

"5.15": [
    ("p", "नादत्ते कस्यचित्पापं", "nādatte kasyacitpāpaṃ", 8),
    ("p", "न चैव सुकृतं विभुः", "na caiva sukṛtaṃ vibhuḥ", 8),
    ("p", "अज्ञानेनावृतं ज्ञानं", "ajñānenāvṛtaṃ jñānaṃ", 8),
    ("p", "तेन मुह्यन्ति जन्तवः", "tena muhyanti jantavaḥ", 8),
],

"5.16": [
    ("p", "ज्ञानेन तु तदज्ञानं", "jñānena tu tadajñānaṃ", 8),
    ("p", "येषां नाशितमात्मनः", "yeṣāṃ nāśitamātmanaḥ", 8),
    ("p", "तेषामादित्यवज्ज्ञानं", "teṣāmādityavajjñānaṃ", 8),
    ("p", "प्रकाशयति तत्परम्", "prakāśayati tatparam", 8),
],

"5.17": [
    ("p", "तद्बुद्धयस्तदात्मानस्", "tadbuddhayastadātmānas", 8),
    ("p", "तन्निष्ठास्तत्परायणाः", "tanniṣṭhāstatparāyaṇāḥ", 8),
    ("p", "गच्छन्त्यपुनरावृत्तिं", "gacchantyapunarāvṛttiṃ", 8),
    ("p", "ज्ञाननिर्धूतकल्मषाः", "jñānanirdhūtakalmaṣāḥ", 8),
],

"5.18": [
    ("p", "विद्याविनयसम्पन्ने", "vidyāvinayasampanne", 8),
    ("p", "ब्राह्मणे गवि हस्तिनि", "brāhmaṇe gavi hastini", 8),
    ("p", "शुनि चैव श्वपाके च", "śuni caiva śvapāke ca", 8),
    ("p", "पण्डिताः समदर्शिनः", "paṇḍitāḥ samadarśinaḥ", 8),
],

"5.19": [
    ("p", "इहैव तैर्जितः सर्गो", "ihaiva tairjitaḥ sargo", 8),
    ("p", "येषां साम्ये स्थितं मनः", "yeṣāṃ sāmye sthitaṃ manaḥ", 8),
    ("p", "निर्दोषं हि समं ब्रह्म", "nirdoṣaṃ hi samaṃ brahma", 8),
    ("p", "तस्माद्ब्रह्मणि ते स्थिताः", "tasmādbrahmaṇi te sthitāḥ", 8),
],

"5.20": [
    ("p", "न प्रहृष्येत्प्रियं प्राप्य", "na prahṛṣyetpriyaṃ prāpya", 8),
    ("p", "नोद्विजेत्प्राप्य चाप्रियम्", "nodvijetprāpya cāpriyam", 8),
    ("p", "स्थिरबुद्धिरसम्मूढो", "sthirabuddhirasammūḍho", 8),
    ("p", "ब्रह्मविद्ब्रह्मणि स्थितः", "brahmavidbrahmaṇi sthitaḥ", 8),
],

"5.21": [
    ("p", "बाह्यस्पर्शेष्वसक्तात्मा", "bāhyasparśeṣvasaktātmā", 8),
    ("p", "विन्दत्यात्मनि यत्सुखम्", "vindatyātmani yatsukham", 8),
    ("p", "स ब्रह्मयोगयुक्तात्मा", "sa brahmayogayuktātmā", 8),
    ("p", "सुखमक्षयमश्नुते", "sukhamakṣayamaśnute", 8),
],

"5.22": [
    ("p", "ये हि संस्पर्शजा भोगा", "ye hi saṃsparśajā bhogā", 8),
    ("p", "दुःखयोनय एव ते", "duḥkhayonaya eva te", 8),
    ("p", "आद्यन्तवन्तः कौन्तेय", "ādyantavantaḥ kaunteya", 8),
    ("p", "न तेषु रमते बुधः", "na teṣu ramate budhaḥ", 8),
],

"5.23": [
    ("p", "शक्नोतीहैव यः सोढुं", "śaknotīhaiva yaḥ soḍhuṃ", 8),
    ("p", "प्राक्छरीरविमोक्षणात्", "prākcharīravimokṣaṇāt", 8),
    ("p", "कामक्रोधोद्भवं वेगं", "kāmakrodhodbhavaṃ vegaṃ", 8),
    ("p", "स युक्तः स सुखी नरः", "sa yuktaḥ sa sukhī naraḥ", 8),
],

"5.24": [
    ("p", "योऽन्तःसुखोऽन्तरारामस्", "yo’ntaḥsukho’ntarārāmas", 8),
    ("p", "तथान्तर्ज्योतिरेव यः", "tathāntarjyotireva yaḥ", 8),
    ("p", "स योगी ब्रह्मनिर्वाणं", "sa yogī brahmanirvāṇaṃ", 8),
    ("p", "ब्रह्मभूतोऽधिगच्छति", "brahmabhūto’dhigacchati", 8),
],

"5.25": [
    ("p", "लभन्ते ब्रह्मनिर्वाणम्", "labhante brahmanirvāṇam", 8),
    ("p", "ऋषयः क्षीणकल्मषाः", "ṛṣayaḥ kṣīṇakalmaṣāḥ", 8),
    ("p", "छिन्नद्वैधा यतात्मानः", "chinnadvaidhā yatātmānaḥ", 8),
    ("p", "सर्वभूतहिते रताः", "sarvabhūtahite ratāḥ", 8),
],

"5.26": [
    ("p", "कामक्रोधवियुक्तानां", "kāmakrodhaviyuktānāṃ", 8),
    ("p", "यतीनां यतचेतसाम्", "yatīnāṃ yatacetasām", 8),
    ("p", "अभितो ब्रह्मनिर्वाणं", "abhito brahmanirvāṇaṃ", 8),
    ("p", "वर्तते विदितात्मनाम्", "vartate viditātmanām", 8),
],

"5.27": [
    ("p", "स्पर्शान्कृत्वा बहिर्बाह्यांश्", "sparśānkṛtvā bahirbāhyāṃś", 8),
    ("p", "चक्षुश्चैवान्तरे भ्रुवोः", "cakṣuścaivāntare bhruvoḥ", 8),
    ("p", "प्राणापानौ समौ कृत्वा", "prāṇāpānau samau kṛtvā", 8),
    ("p", "नासाभ्यन्तरचारिणौ", "nāsābhyantaracāriṇau", 8),
],

"5.28": [
    ("p", "यतेन्द्रियमनोबुद्धिर्", "yatendriyamanobuddhir", 8),
    ("p", "मुनिर्मोक्षपरायणः", "munirmokṣaparāyaṇaḥ", 8),
    ("p", "विगतेच्छाभयक्रोधो", "vigatecchābhayakrodho", 8),
    ("p", "यः सदा मुक्त एव सः", "yaḥ sadā mukta eva saḥ", 8),
],

"5.29": [
    ("p", "भोक्तारं यज्ञतपसां", "bhoktāraṃ yajñatapasāṃ", 8),
    ("p", "सर्वलोकमहेश्वरम्", "sarvalokamaheśvaram", 8),
    ("p", "सुहृदं सर्वभूतानां", "suhṛdaṃ sarvabhūtānāṃ", 8),
    ("p", "ज्ञात्वा मां शान्तिमृच्छति", "jñātvā māṃ śāntimṛcchati", 8),
],

}
