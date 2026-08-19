# -*- coding: utf-8 -*-
"""padas_ch8.py — the pāda (quarter) division of every verse in chapter 8.

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
printed verbatim from ch8.json.
"""

GITA_CH8_PADAS = {
"8.01": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "किं तद्ब्रह्म किमध्यात्मं", "kiṃ tadbrahma kimadhyātmaṃ", 8),
    ("p", "कि कर्म पुरुषोत्तम", "ki karma puruṣottama", 8),
    ("p", "अधिभूतं च किं प्रोक्तम्", "adhibhūtaṃ ca kiṃ proktam", 8),
    ("p", "अधिदैवं किमुच्यते", "adhidaivaṃ kimucyate", 8),
],

"8.02": [
    ("p", "अधियज्ञः कथं कोऽत्र", "adhiyajñaḥ kathaṃ ko’tra", 8),
    ("p", "देहेऽस्मिन्मधुसूदन", "dehe’sminmadhusūdana", 8),
    ("p", "प्रयाणकाले च कथं", "prayāṇakāle ca kathaṃ", 8),
    ("p", "ज्ञेयोऽसि नियतात्मभिः", "jñeyo’si niyatātmabhiḥ", 8),
],

"8.03": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "अक्षरं ब्रह्म परमं", "akṣaraṃ brahma paramaṃ", 8),
    ("p", "स्वभावोऽध्यात्ममुच्यते", "svabhāvo’dhyātmamucyate", 8),
    ("p", "भूतभावोद्भवकरो", "bhūtabhāvodbhavakaro", 8),
    ("p", "विसर्गः कर्मसंज्ञितः", "visargaḥ karmasaṃjñitaḥ", 8),
],

"8.04": [
    ("p", "अधिभूतं क्षरो भावः", "adhibhūtaṃ kṣaro bhāvaḥ", 8),
    ("p", "पुरुषश्चाधिदैवतम्", "puruṣaścādhidaivatam", 8),
    ("p", "अधियज्ञोऽहमेवात्र", "adhiyajño’hamevātra", 8),
    ("p", "देहे देहभृतां वर", "dehe dehabhṛtāṃ vara", 8),
],

"8.05": [
    ("p", "अन्तकाले च मामेव", "antakāle ca māmeva", 8),
    ("p", "स्मरन्मुक्त्वा कलेवरम्", "smaranmuktvā kalevaram", 8),
    ("p", "यः प्रयाति स मद्भावं", "yaḥ prayāti sa madbhāvaṃ", 8),
    ("p", "याति नास्त्यत्र संशयः", "yāti nāstyatra saṃśayaḥ", 8),
],

"8.06": [
    ("p", "यं यं वापि स्मरन्भावं", "yaṃ yaṃ vāpi smaranbhāvaṃ", 8),
    ("p", "त्यजत्यन्ते कलेवरम्", "tyajatyante kalevaram", 8),
    ("p", "तं तमेवैति कौन्तेय", "taṃ tamevaiti kaunteya", 8),
    ("p", "सदा तद्भावभावितः", "sadā tadbhāvabhāvitaḥ", 8),
],

"8.07": [
    ("p", "तस्मात्सर्वेषु कालेषु", "tasmātsarveṣu kāleṣu", 8),
    ("p", "मामनुस्मर युध्य च", "māmanusmara yudhya ca", 8),
    ("p", "मय्यर्पितमनोबुद्धिर्", "mayyarpitamanobuddhir", 8),
    ("p", "मामेवैष्यस्यसंशयः", "māmevaiṣyasyasaṃśayaḥ", 8),
],

"8.08": [
    ("p", "अभ्यासयोगयुक्तेन", "abhyāsayogayuktena", 8),
    ("p", "चेतसा नान्यगामिना", "cetasā nānyagāminā", 8),
    ("p", "परमं पुरुषं दिव्यं", "paramaṃ puruṣaṃ divyaṃ", 8),
    ("p", "याति पार्थानुचिन्तयन्", "yāti pārthānucintayan", 8),
],

"8.09": [
    ("p", "कविं पुराणमनुशासितारम्", "kaviṃ purāṇamanuśāsitāram", 11),
    ("p", "अणोरणीयांसमनुस्मरेद्यः", "aṇoraṇīyāṃsamanusmaredyaḥ", 11),
    ("p", "सर्वस्य धातारमचिन्त्यरूपम्", "sarvasya dhātāramacintyarūpam", 11),
    ("p", "आदित्यवर्णं तमसः परस्तात्", "ādityavarṇaṃ tamasaḥ parastāt", 11),
],

"8.10": [
    ("p", "प्रयाणकाले मनसाचलेन", "prayāṇakāle manasācalena", 11),
    ("p", "भक्त्या युक्तो योगबलेन चैव", "bhaktyā yukto yogabalena caiva", 11),
    ("p", "भ्रुवोर्मध्ये प्राणमावेश्य सम्यक्", "bhruvormadhye prāṇamāveśya samyak", 11),
    ("p", "स तं परं पुरुषमुपैति दिव्यम्", "sa taṃ paraṃ puruṣamupaiti divyam", 12),
],

"8.11": [
    ("p", "यदक्षरं वेदविदो वदन्ति", "yadakṣaraṃ vedavido vadanti", 11),
    ("p", "विशन्ति यद्यतयो वीतरागाः", "viśanti yadyatayo vītarāgāḥ", 11),
    ("p", "यदिच्छन्तो ब्रह्मचर्यं चरन्ति", "yadicchanto brahmacaryaṃ caranti", 11),
    ("p", "तत्ते पदं सङ्ग्रहेण प्रवक्ष्ये", "tatte padaṃ saṅgraheṇa pravakṣye", 11),
],

"8.12": [
    ("p", "सर्वद्वाराणि संयम्य", "sarvadvārāṇi saṃyamya", 8),
    ("p", "मनो हृदि निरुध्य च", "mano hṛdi nirudhya ca", 8),
    ("p", "मूर्ध्न्याधायात्मनः प्राणम्", "mūrdhnyādhāyātmanaḥ prāṇam", 8),
    ("p", "आस्थितो योगधारणाम्", "āsthito yogadhāraṇām", 8),
],

"8.13": [
    ("p", "ओमित्येकाक्षरं ब्रह्म", "omityekākṣaraṃ brahma", 8),
    ("p", "व्याहरन्मामनुस्मरन्", "vyāharanmāmanusmaran", 8),
    ("p", "यः प्रयाति त्यजन्देहं", "yaḥ prayāti tyajandehaṃ", 8),
    ("p", "स याति परमां गतिम्", "sa yāti paramāṃ gatim", 8),
],

"8.14": [
    ("p", "अनन्यचेताः सततं", "ananyacetāḥ satataṃ", 8),
    ("p", "यो मां स्मरति नित्यशः", "yo māṃ smarati nityaśaḥ", 8),
    ("p", "तस्याहं सुलभः पार्थ", "tasyāhaṃ sulabhaḥ pārtha", 8),
    ("p", "नित्ययुक्तस्य योगिनः", "nityayuktasya yoginaḥ", 8),
],

"8.15": [
    ("p", "मामुपेत्य पुनर्जन्म", "māmupetya punarjanma", 8),
    ("p", "दुःखालयमशाश्वतम्", "duḥkhālayamaśāśvatam", 8),
    ("p", "नाप्नुवन्ति महात्मानः", "nāpnuvanti mahātmānaḥ", 8),
    ("p", "संसिद्धिं परमां गताः", "saṃsiddhiṃ paramāṃ gatāḥ", 8),
],

"8.16": [
    ("p", "आ ब्रह्मभुवनाल्लोकाः", "ā brahmabhuvanāllokāḥ", 8),
    ("p", "पुनरावर्तिनोऽर्जुन", "punarāvartino’rjuna", 8),
    ("p", "मामुपेत्य तु कौन्तेय", "māmupetya tu kaunteya", 8),
    ("p", "पुनर्जन्म न विद्यते", "punarjanma na vidyate", 8),
],

"8.17": [
    ("p", "सहस्रयुगपर्यन्तम्", "sahasrayugaparyantam", 8),
    ("p", "अहर्यद्ब्रह्मणो विदुः", "aharyadbrahmaṇo viduḥ", 8),
    ("p", "रात्रिं युगसहस्रान्तां", "rātriṃ yugasahasrāntāṃ", 8),
    ("p", "तेऽहोरात्रविदो जनाः", "te’horātravido janāḥ", 8),
],

"8.18": [
    ("p", "अव्यक्ताद्व्यक्तयः सर्वाः", "avyaktādvyaktayaḥ sarvāḥ", 8),
    ("p", "प्रभवन्त्यहरागमे", "prabhavantyaharāgame", 8),
    ("p", "रात्र्यागमे प्रलीयन्ते", "rātryāgame pralīyante", 8),
    ("p", "तत्रैवाव्यक्तसंज्ञके", "tatraivāvyaktasaṃjñake", 8),
],

"8.19": [
    ("p", "भूतग्रामः स एवायं", "bhūtagrāmaḥ sa evāyaṃ", 8),
    ("p", "भूत्वा भूत्वा प्रलीयते", "bhūtvā bhūtvā pralīyate", 8),
    ("p", "रात्र्यागमेऽवशः पार्थ", "rātryāgame’vaśaḥ pārtha", 8),
    ("p", "प्रभवत्यहरागमे", "prabhavatyaharāgame", 8),
],

"8.20": [
    ("p", "परस्तस्मात्तु भावोऽन्यो", "parastasmāttu bhāvo’nyo", 8),
    ("p", "ऽव्यक्तोऽव्यक्तात्सनातनः", "’vyakto’vyaktātsanātanaḥ", 8),
    ("p", "यः स सर्वेषु भूतेषु", "yaḥ sa sarveṣu bhūteṣu", 8),
    ("p", "नश्यत्सु न विनश्यति", "naśyatsu na vinaśyati", 8),
],

"8.21": [
    ("p", "अव्यक्तोऽक्षर इत्युक्तस्", "avyakto’kṣara ityuktas", 8),
    ("p", "तमाहुः परमां गतिम्", "tamāhuḥ paramāṃ gatim", 8),
    ("p", "यं प्राप्य न निवर्तन्ते", "yaṃ prāpya na nivartante", 8),
    ("p", "तद्धाम परमं मम", "taddhāma paramaṃ mama", 8),
],

"8.22": [
    ("p", "पुरुषः स परः पार्थ", "puruṣaḥ sa paraḥ pārtha", 8),
    ("p", "भक्त्या लभ्यस्त्वनन्यया", "bhaktyā labhyastvananyayā", 8),
    ("p", "यस्यान्तःस्थानि भूतानि", "yasyāntaḥsthāni bhūtāni", 8),
    ("p", "येन सर्वमिदं ततम्", "yena sarvamidaṃ tatam", 8),
],

"8.23": [
    ("p", "यत्र काले त्वनावृत्तिम्", "yatra kāle tvanāvṛttim", 8),
    ("p", "आवृत्तिं चैव योगिनः", "āvṛttiṃ caiva yoginaḥ", 8),
    ("p", "प्रयाता यान्ति तं कालं", "prayātā yānti taṃ kālaṃ", 8),
    ("p", "वक्ष्यामि भरतर्षभ", "vakṣyāmi bharatarṣabha", 8),
],

"8.24": [
    ("p", "अग्निर्ज्योतिरहः शुक्लः", "agnirjyotirahaḥ śuklaḥ", 8),
    ("p", "षण्मासा उत्तरायणम्", "ṣaṇmāsā uttarāyaṇam", 8),
    ("p", "तत्र प्रयाता गच्छन्ति", "tatra prayātā gacchanti", 8),
    ("p", "ब्रह्म ब्रह्मविदो जनाः", "brahma brahmavido janāḥ", 8),
],

"8.25": [
    ("p", "धूमो रात्रिस्तथा कृष्णः", "dhūmo rātristathā kṛṣṇaḥ", 8),
    ("p", "षण्मासा दक्षिणायनम्", "ṣaṇmāsā dakṣiṇāyanam", 8),
    ("p", "तत्र चान्द्रमसं ज्योतिर्", "tatra cāndramasaṃ jyotir", 8),
    ("p", "योगी प्राप्य निवर्तते", "yogī prāpya nivartate", 8),
],

"8.26": [
    ("p", "शुक्लकृष्णे गती ह्येते", "śuklakṛṣṇe gatī hyete", 8),
    ("p", "जगतः शाश्वते मते", "jagataḥ śāśvate mate", 8),
    ("p", "एकया यात्यनावृत्तिम्", "ekayā yātyanāvṛttim", 8),
    ("p", "अन्ययावर्तते पुनः", "anyayāvartate punaḥ", 8),
],

"8.27": [
    ("p", "नैते सृती पार्थ जानन्", "naite sṛtī pārtha jānan", 8),
    ("p", "योगी मुह्यति कश्चन", "yogī muhyati kaścana", 8),
    ("p", "तस्मात्सर्वेषु कालेषु", "tasmātsarveṣu kāleṣu", 8),
    ("p", "योगयुक्तो भवार्जुन", "yogayukto bhavārjuna", 8),
],

"8.28": [
    ("p", "वेदेषु यज्ञेषु तपःसु चैव", "vedeṣu yajñeṣu tapaḥsu caiva", 11),
    ("p", "दानेषु यत्पुण्यफलं प्रदिष्टम्", "dāneṣu yatpuṇyaphalaṃ pradiṣṭam", 11),
    ("p", "अत्येति तत्सर्वमिदं विदित्वा", "atyeti tatsarvamidaṃ viditvā", 11),
    ("p", "योगी परं स्थानमुपैति चाद्यम्", "yogī paraṃ sthānamupaiti cādyam", 11),
],

}
