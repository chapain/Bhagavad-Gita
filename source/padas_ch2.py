# -*- coding: utf-8 -*-
"""padas_ch2.py — the pāda (quarter) division of every verse in chapter 2.

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
printed verbatim from ch2.json.
"""

GITA_CH2_PADAS = {
"2.01": [
    ("s", "सञ्जय उवाच।", "sañjaya uvāca"),
    ("p", "तं तथा कृपयाविष्टम्", "taṃ tathā kṛpayāviṣṭam", 8),
    ("p", "अश्रुपूर्णाकुलेक्षणम्", "aśrupūrṇākulekṣaṇam", 8),
    ("p", "विषीदन्तमिदं वाक्यम्", "viṣīdantamidaṃ vākyam", 8),
    ("p", "उवाच मधुसूदनः", "uvāca madhusūdanaḥ", 8),
],

"2.02": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "कुतस्त्वा कश्मलमिदं", "kutastvā kaśmalamidaṃ", 8),
    ("p", "विषमे समुपस्थितम्", "viṣame samupasthitam", 8),
    ("p", "अनार्यजुष्टमस्वर्ग्यम्", "anāryajuṣṭamasvargyam", 8),
    ("p", "अकीर्तिकरमर्जुन", "akīrtikaramarjuna", 8),
],

"2.03": [
    ("p", "क्लैब्यं मा स्म गमः पार्थ", "klaibyaṃ mā sma gamaḥ pārtha", 8),
    ("p", "नैतत्त्वय्युपपद्यते", "naitattvayyupapadyate", 8),
    ("p", "क्षुद्रं हृदयदौर्बल्यं", "kṣudraṃ hṛdayadaurbalyaṃ", 8),
    ("p", "त्यक्त्वोत्तिष्ठ परन्तप", "tyaktvottiṣṭha parantapa", 8),
],

"2.04": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "कथं भीष्ममहं सङ्ख्ये", "kathaṃ bhīṣmamahaṃ saṅkhye", 8),
    ("p", "द्रोणं च मधुसूदन", "droṇaṃ ca madhusūdana", 8),
    ("p", "इषुभिः प्रतियोत्स्यामि", "iṣubhiḥ pratiyotsyāmi", 8),
    ("p", "पूजार्हावरिसूदन", "pūjārhāvarisūdana", 8),
],

"2.05": [
    ("p", "गुरूनहत्वा हि महानुभावान्", "gurūnahatvā hi mahānubhāvān", 11),
    ("p", "श्रेयो भोक्तुं भैक्षमपीह लोके", "śreyo bhoktuṃ bhaikṣamapīha loke", 11),
    ("p", "हत्वार्थकामांस्तु गुरूनिहैव", "hatvārthakāmāṃstu gurūnihaiva", 11),
    ("p", "भुञ्जीय भोगान् रुधिरप्रदिग्धान्", "bhuñjīya bhogān rudhirapradigdhān", 11),
],

"2.06": [
    ("p", "न चैतद्विद्मः कतरन्नो गरीयः", "na caitadvidmaḥ kataranno garīyaḥ", 12),
    ("p", "यद्वा जयेम यदि वा नो जयेयुः", "yadvā jayema yadi vā no jayeyuḥ", 12),
    ("p", "यानेव हत्वा न जिजीविषामः", "yāneva hatvā na jijīviṣāmaḥ", 11),
    ("p", "तेऽवस्थिताः प्रमुखे धार्तराष्ट्राः", "te’vasthitāḥ pramukhe dhārtarāṣṭrāḥ", 11),
],

"2.07": [
    ("p", "कार्पण्यदोषोपहतस्वभावः", "kārpaṇyadoṣopahatasvabhāvaḥ", 11),
    ("p", "पृच्छामि त्वां धर्मसम्मूढचेताः", "pṛcchāmi tvāṃ dharmasammūḍhacetāḥ", 11),
    ("p", "यच्छ्रेयः स्यान्निश्चितं ब्रूहि तन्मे", "yacchreyaḥ syānniścitaṃ brūhi tanme", 11),
    ("p", "शिष्यस्तेऽहं शाधि मां त्वां प्रपन्नम्", "śiṣyaste’haṃ śādhi māṃ tvāṃ prapannam", 11),
],

"2.08": [
    ("p", "न हि प्रपश्यामि ममापनुद्यात्", "na hi prapaśyāmi mamāpanudyāt", 11),
    ("p", "यच्छोकमुच्छोषणमिन्द्रियाणाम्", "yacchokamucchoṣaṇamindriyāṇām", 11),
    ("p", "अवाप्य भूमावसपत्नमृद्धं", "avāpya bhūmāvasapatnamṛddhaṃ", 11),
    ("p", "राज्यं सुराणामपि चाधिपत्यम्", "rājyaṃ surāṇāmapi cādhipatyam", 11),
],

"2.09": [
    ("s", "सञ्जय उवाच।", "sañjaya uvāca"),
    ("p", "एवमुक्त्वा हृषीकेशं", "evamuktvā hṛṣīkeśaṃ", 8),
    ("p", "गुडाकेशः परन्तप", "guḍākeśaḥ parantapa", 8),
    ("p", "न योत्स्य इति गोविन्दम्", "na yotsya iti govindam", 8),
    ("p", "उक्त्वा तूष्णीं बभूव ह", "uktvā tūṣṇīṃ babhūva ha", 8),
],

"2.10": [
    ("p", "तमुवाच हृषीकेशः", "tamuvāca hṛṣīkeśaḥ", 8),
    ("p", "प्रहसन्निव भारत", "prahasanniva bhārata", 8),
    ("p", "सेनयोरुभयोर्मध्ये", "senayorubhayormadhye", 8),
    ("p", "विषीदन्तमिदं वचः", "viṣīdantamidaṃ vacaḥ", 8),
],

"2.11": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "अशोच्यानन्वशोचस्त्वं", "aśocyānanvaśocastvaṃ", 8),
    ("p", "प्रज्ञावादांश्च भाषसे", "prajñāvādāṃśca bhāṣase", 8),
    ("p", "गतासूनगतासूंश्च", "gatāsūnagatāsūṃśca", 8),
    ("p", "नानुशोचन्ति पण्डिताः", "nānuśocanti paṇḍitāḥ", 8),
],

"2.12": [
    ("p", "न त्वेवाहं जातु नासं", "na tvevāhaṃ jātu nāsaṃ", 8),
    ("p", "न त्वं नेमे जनाधिपाः", "na tvaṃ neme janādhipāḥ", 8),
    ("p", "न चैव न भविष्यामः", "na caiva na bhaviṣyāmaḥ", 8),
    ("p", "सर्वे वयमतः परम्", "sarve vayamataḥ param", 8),
],

"2.13": [
    ("p", "देहिनोऽस्मिन्यथा देहे", "dehino’sminyathā dehe", 8),
    ("p", "कौमारं यौवनं जरा", "kaumāraṃ yauvanaṃ jarā", 8),
    ("p", "तथा देहान्तरप्राप्तिर्", "tathā dehāntaraprāptir", 8),
    ("p", "धीरस्तत्र न मुह्यति", "dhīrastatra na muhyati", 8),
],

"2.14": [
    ("p", "मात्रास्पर्शास्तु कौन्तेय", "mātrāsparśāstu kaunteya", 8),
    ("p", "शीतोष्णसुखदुःखदाः", "śītoṣṇasukhaduḥkhadāḥ", 8),
    ("p", "आगमापायिनोऽनित्यास्", "āgamāpāyino’nityās", 8),
    ("p", "तांस्तितिक्षस्व भारत", "tāṃstitikṣasva bhārata", 8),
],

"2.15": [
    ("p", "यं हि न व्यथयन्त्येते", "yaṃ hi na vyathayantyete", 8),
    ("p", "पुरुषं पुरुषर्षभ", "puruṣaṃ puruṣarṣabha", 8),
    ("p", "समदुःखसुखं धीरं", "samaduḥkhasukhaṃ dhīraṃ", 8),
    ("p", "सोऽमृतत्वाय कल्पते", "so’mṛtatvāya kalpate", 8),
],

"2.16": [
    ("p", "नासतो विद्यते भावो", "nāsato vidyate bhāvo", 8),
    ("p", "नाभावो विद्यते सतः", "nābhāvo vidyate sataḥ", 8),
    ("p", "उभयोरपि दृष्टोऽन्तस्", "ubhayorapi dṛṣṭo’ntas", 8),
    ("p", "त्वनयोस्तत्त्वदर्शिभिः", "tvanayostattvadarśibhiḥ", 8),
],

"2.17": [
    ("p", "अविनाशि तु तद्विद्धि", "avināśi tu tadviddhi", 8),
    ("p", "येन सर्वमिदं ततम्", "yena sarvamidaṃ tatam", 8),
    ("p", "विनाशमव्ययस्यास्य", "vināśamavyayasyāsya", 8),
    ("p", "न कश्चित्कर्तुमर्हति", "na kaścitkartumarhati", 8),
],

"2.18": [
    ("p", "अन्तवन्त इमे देहा", "antavanta ime dehā", 8),
    ("p", "नित्यस्योक्ताः शरीरिणः", "nityasyoktāḥ śarīriṇaḥ", 8),
    ("p", "अनाशिनोऽप्रमेयस्य", "anāśino’prameyasya", 8),
    ("p", "तस्माद्युध्यस्व भारत", "tasmādyudhyasva bhārata", 8),
],

"2.19": [
    ("p", "य एनं वेत्ति हन्तारं", "ya enaṃ vetti hantāraṃ", 8),
    ("p", "यश्चैनं मन्यते हतम्", "yaścainaṃ manyate hatam", 8),
    ("p", "उभौ तौ न विजानीतो", "ubhau tau na vijānīto", 8),
    ("p", "नायं हन्ति न हन्यते", "nāyaṃ hanti na hanyate", 8),
],

"2.20": [
    ("p", "न जायते म्रियते वा कदाचिन्", "na jāyate mriyate vā kadācin", 11),
    ("p", "नायं भूत्वा भविता वा न भूयः", "nāyaṃ bhūtvā bhavitā vā na bhūyaḥ", 11),
    ("p", "अजो नित्यः शाश्वतोऽयं पुराणो", "ajo nityaḥ śāśvato’yaṃ purāṇo", 11),
    ("p", "न हन्यते हन्यमाने शरीरे", "na hanyate hanyamāne śarīre", 11),
],

"2.21": [
    ("p", "वेदाविनाशिनं नित्यं", "vedāvināśinaṃ nityaṃ", 8),
    ("p", "य एनमजमव्ययम्", "ya enamajamavyayam", 8),
    ("p", "कथं स पुरुषः पार्थ", "kathaṃ sa puruṣaḥ pārtha", 8),
    ("p", "कं घातयति हन्ति कम्", "kaṃ ghātayati hanti kam", 8),
],

"2.22": [
    ("p", "वासांसि जीर्णानि यथा विहाय", "vāsāṃsi jīrṇāni yathā vihāya", 11),
    ("p", "नवानि गृह्णाति नरोऽपराणि", "navāni gṛhṇāti naro’parāṇi", 11),
    ("p", "तथा शरीराणि विहाय जीर्णान्य्", "tathā śarīrāṇi vihāya jīrṇāny", 11),
    ("p", "अन्यानि संयाति नवानि देही", "anyāni saṃyāti navāni dehī", 11),
],

"2.23": [
    ("p", "नैनं छिन्दन्ति शस्त्राणि", "nainaṃ chindanti śastrāṇi", 8),
    ("p", "नैनं दहति पावकः", "nainaṃ dahati pāvakaḥ", 8),
    ("p", "न चैनं क्लेदयन्त्यापो", "na cainaṃ kledayantyāpo", 8),
    ("p", "न शोषयति मारुतः", "na śoṣayati mārutaḥ", 8),
],

"2.24": [
    ("p", "अच्छेद्योऽयमदाह्योऽयम्", "acchedyo’yamadāhyo’yam", 8),
    ("p", "अक्लेद्योऽशोष्य एव च", "akledyo’śoṣya eva ca", 8),
    ("p", "नित्यः सर्वगतः स्थाणुर्", "nityaḥ sarvagataḥ sthāṇur", 8),
    ("p", "अचलोऽयं सनातनः", "acalo’yaṃ sanātanaḥ", 8),
],

"2.25": [
    ("p", "अव्यक्तोऽयमचिन्त्योऽयम्", "avyakto’yamacintyo’yam", 8),
    ("p", "अविकार्योऽयमुच्यते", "avikāryo’yamucyate", 8),
    ("p", "तस्मादेवं विदित्वैनं", "tasmādevaṃ viditvainaṃ", 8),
    ("p", "नानुशोचितुमर्हसि", "nānuśocitumarhasi", 8),
],

"2.26": [
    ("p", "अथ चैनं नित्यजातं", "atha cainaṃ nityajātaṃ", 8),
    ("p", "नित्यं वा मन्यसे मृतम्", "nityaṃ vā manyase mṛtam", 8),
    ("p", "तथापि त्वं महाबाहो", "tathāpi tvaṃ mahābāho", 8),
    ("p", "नैवं शोचितुमर्हसि", "naivaṃ śocitumarhasi", 8),
],

"2.27": [
    ("p", "जातस्य हि ध्रुवो मृत्युर्", "jātasya hi dhruvo mṛtyur", 8),
    ("p", "ध्रुवं जन्म मृतस्य च", "dhruvaṃ janma mṛtasya ca", 8),
    ("p", "तस्मादपरिहार्येऽर्थे", "tasmādaparihārye’rthe", 8),
    ("p", "न त्वं शोचितुमर्हसि", "na tvaṃ śocitumarhasi", 8),
],

"2.28": [
    ("p", "अव्यक्तादीनि भूतानि", "avyaktādīni bhūtāni", 8),
    ("p", "व्यक्तमध्यानि भारत", "vyaktamadhyāni bhārata", 8),
    ("p", "अव्यक्तनिधनान्येव", "avyaktanidhanānyeva", 8),
    ("p", "तत्र का परिदेवना", "tatra kā paridevanā", 8),
],

"2.29": [
    ("p", "आश्चर्यवत्पश्यति कश्चिदेनम्", "āścaryavatpaśyati kaścidenam", 11),
    ("p", "आश्चर्यवद्वदति तथैव चान्यः", "āścaryavadvadati tathaiva cānyaḥ", 12),
    ("p", "आश्चर्यवच्चैनमन्यः शृणोति", "āścaryavaccainamanyaḥ śṛṇoti", 11),
    ("p", "श्रुत्वाप्येनं वेद न चैव कश्चित्", "śrutvāpyenaṃ veda na caiva kaścit", 11),
],

"2.30": [
    ("p", "देही नित्यमवध्योऽयं", "dehī nityamavadhyo’yaṃ", 8),
    ("p", "देहे सर्वस्य भारत", "dehe sarvasya bhārata", 8),
    ("p", "तस्मात्सर्वाणि भूतानि", "tasmātsarvāṇi bhūtāni", 8),
    ("p", "न त्वं शोचितुमर्हसि", "na tvaṃ śocitumarhasi", 8),
],

"2.31": [
    ("p", "स्वधर्ममपि चावेक्ष्य", "svadharmamapi cāvekṣya", 8),
    ("p", "न विकम्पितुमर्हसि", "na vikampitumarhasi", 8),
    ("p", "धर्म्याद्धि युद्धाच्छ्रेयोऽन्यत्", "dharmyāddhi yuddhācchreyo’nyat", 8),
    ("p", "क्षत्रियस्य न विद्यते", "kṣatriyasya na vidyate", 8),
],

"2.32": [
    ("p", "यदृच्छया चोपपन्नं", "yadṛcchayā copapannaṃ", 8),
    ("p", "स्वर्गद्वारमपावृतम्", "svargadvāramapāvṛtam", 8),
    ("p", "सुखिनः क्षत्रियाः पार्थ", "sukhinaḥ kṣatriyāḥ pārtha", 8),
    ("p", "लभन्ते युद्धमीदृशम्", "labhante yuddhamīdṛśam", 8),
],

"2.33": [
    ("p", "अथ चेत्त्वमिमं धर्म्यं", "atha cettvamimaṃ dharmyaṃ", 8),
    ("p", "सङ्ग्रामं न करिष्यसि", "saṅgrāmaṃ na kariṣyasi", 8),
    ("p", "ततः स्वधर्मं कीर्तिं च", "tataḥ svadharmaṃ kīrtiṃ ca", 8),
    ("p", "हित्वा पापमवाप्स्यसि", "hitvā pāpamavāpsyasi", 8),
],

"2.34": [
    ("p", "अकीर्तिं चापि भूतानि", "akīrtiṃ cāpi bhūtāni", 8),
    ("p", "कथयिष्यन्ति तेऽव्ययाम्", "kathayiṣyanti te’vyayām", 8),
    ("p", "सम्भावितस्य चाकीर्तिर्", "sambhāvitasya cākīrtir", 8),
    ("p", "मरणादतिरिच्यते", "maraṇādatiricyate", 8),
],

"2.35": [
    ("p", "भयाद्रणादुपरतं", "bhayādraṇāduparataṃ", 8),
    ("p", "मंस्यन्ते त्वां महारथाः", "maṃsyante tvāṃ mahārathāḥ", 8),
    ("p", "येषां च त्वं बहुमतो", "yeṣāṃ ca tvaṃ bahumato", 8),
    ("p", "भूत्वा यास्यसि लाघवम्", "bhūtvā yāsyasi lāghavam", 8),
],

"2.36": [
    ("p", "अवाच्यवादांश्च बहून्", "avācyavādāṃśca bahūn", 8),
    ("p", "वदिष्यन्ति तवाहिताः", "vadiṣyanti tavāhitāḥ", 8),
    ("p", "निन्दन्तस्तव सामर्थ्यं", "nindantastava sāmarthyaṃ", 8),
    ("p", "ततो दुःखतरं नु किम्", "tato duḥkhataraṃ nu kim", 8),
],

"2.37": [
    ("p", "हतो वा प्राप्स्यसि स्वर्गं", "hato vā prāpsyasi svargaṃ", 8),
    ("p", "जित्वा वा भोक्ष्यसे महीम्", "jitvā vā bhokṣyase mahīm", 8),
    ("p", "तस्मादुत्तिष्ठ कौन्तेय", "tasmāduttiṣṭha kaunteya", 8),
    ("p", "युद्धाय कृतनिश्चयः", "yuddhāya kṛtaniścayaḥ", 8),
],

"2.38": [
    ("p", "सुखदुःखे समे कृत्वा", "sukhaduḥkhe same kṛtvā", 8),
    ("p", "लाभालाभौ जयाजयौ", "lābhālābhau jayājayau", 8),
    ("p", "ततो युद्धाय युज्यस्व", "tato yuddhāya yujyasva", 8),
    ("p", "नैवं पापमवाप्स्यसि", "naivaṃ pāpamavāpsyasi", 8),
],

"2.39": [
    ("p", "एषा तेऽभिहिता साङ्ख्ये", "eṣā te’bhihitā sāṅkhye", 8),
    ("p", "बुद्धिर्योगे त्विमां शृणु", "buddhiryoge tvimāṃ śṛṇu", 8),
    ("p", "बुद्ध्या युक्तो यया पार्थ", "buddhyā yukto yayā pārtha", 8),
    ("p", "कर्मबन्धं प्रहास्यसि", "karmabandhaṃ prahāsyasi", 8),
],

"2.40": [
    ("p", "नेहाभिक्रमनाशोऽस्ति", "nehābhikramanāśo’sti", 8),
    ("p", "प्रत्यवायो न विद्यते", "pratyavāyo na vidyate", 8),
    ("p", "स्वल्पमप्यस्य धर्मस्य", "svalpamapyasya dharmasya", 8),
    ("p", "त्रायते महतो भयात्", "trāyate mahato bhayāt", 8),
],

"2.41": [
    ("p", "व्यवसायात्मिका बुद्धिर्", "vyavasāyātmikā buddhir", 8),
    ("p", "एकेह कुरुनन्दन", "ekeha kurunandana", 8),
    ("p", "बहुशाखा ह्यनन्ताश्च", "bahuśākhā hyanantāśca", 8),
    ("p", "बुद्धयोऽव्यवसायिनाम्", "buddhayo’vyavasāyinām", 8),
],

"2.42": [
    ("p", "यामिमां पुष्पितां वाचं", "yāmimāṃ puṣpitāṃ vācaṃ", 8),
    ("p", "प्रवदन्त्यविपश्चितः", "pravadantyavipaścitaḥ", 8),
    ("p", "वेदवादरताः पार्थ", "vedavādaratāḥ pārtha", 8),
    ("p", "नान्यदस्तीति वादिनः", "nānyadastīti vādinaḥ", 8),
],

"2.43": [
    ("p", "कामात्मानः स्वर्गपरा", "kāmātmānaḥ svargaparā", 8),
    ("p", "जन्मकर्मफलप्रदाम्", "janmakarmaphalapradām", 8),
    ("p", "क्रियाविशेषबहुलां", "kriyāviśeṣabahulāṃ", 8),
    ("p", "भोगैश्वर्यगतिं प्रति", "bhogaiśvaryagatiṃ prati", 8),
],

"2.44": [
    ("p", "भोगैश्वर्यप्रसक्तानां", "bhogaiśvaryaprasaktānāṃ", 8),
    ("p", "तयापहृतचेतसाम्", "tayāpahṛtacetasām", 8),
    ("p", "व्यवसायात्मिका बुद्धिः", "vyavasāyātmikā buddhiḥ", 8),
    ("p", "समाधौ न विधीयते", "samādhau na vidhīyate", 8),
],

"2.45": [
    ("p", "त्रैगुण्यविषया वेदा", "traiguṇyaviṣayā vedā", 8),
    ("p", "निस्त्रैगुण्यो भवार्जुन", "nistraiguṇyo bhavārjuna", 8),
    ("p", "निर्द्वन्द्वो नित्यसत्त्वस्थो", "nirdvandvo nityasattvastho", 8),
    ("p", "निर्योगक्षेम आत्मवान्", "niryogakṣema ātmavān", 8),
],

"2.46": [
    ("p", "यावानर्थ उदपाने", "yāvānartha udapāne", 8),
    ("p", "सर्वतः सम्प्लुतोदके", "sarvataḥ samplutodake", 8),
    ("p", "तावान्सर्वेषु वेदेषु", "tāvānsarveṣu vedeṣu", 8),
    ("p", "ब्राह्मणस्य विजानतः", "brāhmaṇasya vijānataḥ", 8),
],

"2.47": [
    ("p", "कर्मण्येवाधिकारस्ते", "karmaṇyevādhikāraste", 8),
    ("p", "मा फलेषु कदाचन", "mā phaleṣu kadācana", 8),
    ("p", "मा कर्मफलहेतुर्भूर्", "mā karmaphalaheturbhūr", 8),
    ("p", "मा ते सङ्गोऽस्त्वकर्मणि", "mā te saṅgo’stvakarmaṇi", 8),
],

"2.48": [
    ("p", "योगस्थः कुरु कर्माणि", "yogasthaḥ kuru karmāṇi", 8),
    ("p", "सङ्गं त्यक्त्वा धनञ्जय", "saṅgaṃ tyaktvā dhanañjaya", 8),
    ("p", "सिद्ध्यसिद्ध्योः समो भूत्वा", "siddhyasiddhyoḥ samo bhūtvā", 8),
    ("p", "समत्वं योग उच्यते", "samatvaṃ yoga ucyate", 8),
],

"2.49": [
    ("p", "दूरेण ह्यवरं कर्म", "dūreṇa hyavaraṃ karma", 8),
    ("p", "बुद्धियोगाद्धनञ्जय", "buddhiyogāddhanañjaya", 8),
    ("p", "बुद्धौ शरणमन्विच्छ", "buddhau śaraṇamanviccha", 8),
    ("p", "कृपणाः फलहेतवः", "kṛpaṇāḥ phalahetavaḥ", 8),
],

"2.50": [
    ("p", "बुद्धियुक्तो जहातीह", "buddhiyukto jahātīha", 8),
    ("p", "उभे सुकृतदुष्कृते", "ubhe sukṛtaduṣkṛte", 8),
    ("p", "तस्माद्योगाय युज्यस्व", "tasmādyogāya yujyasva", 8),
    ("p", "योगः कर्मसु कौशलम्", "yogaḥ karmasu kauśalam", 8),
],

"2.51": [
    ("p", "कर्मजं बुद्धियुक्ता हि", "karmajaṃ buddhiyuktā hi", 8),
    ("p", "फलं त्यक्त्वा मनीषिणः", "phalaṃ tyaktvā manīṣiṇaḥ", 8),
    ("p", "जन्मबन्धविनिर्मुक्ताः", "janmabandhavinirmuktāḥ", 8),
    ("p", "पदं गच्छन्त्यनामयम्", "padaṃ gacchantyanāmayam", 8),
],

"2.52": [
    ("p", "यदा ते मोहकलिलं", "yadā te mohakalilaṃ", 8),
    ("p", "बुद्धिर्व्यतितरिष्यति", "buddhirvyatitariṣyati", 8),
    ("p", "तदा गन्तासि निर्वेदं", "tadā gantāsi nirvedaṃ", 8),
    ("p", "श्रोतव्यस्य श्रुतस्य च", "śrotavyasya śrutasya ca", 8),
],

"2.53": [
    ("p", "श्रुतिविप्रतिपन्ना ते", "śrutivipratipannā te", 8),
    ("p", "यदा स्थास्यति निश्चला", "yadā sthāsyati niścalā", 8),
    ("p", "समाधावचला बुद्धिस्", "samādhāvacalā buddhis", 8),
    ("p", "तदा योगमवाप्स्यसि", "tadā yogamavāpsyasi", 8),
],

"2.54": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "स्थितप्रज्ञस्य का भाषा", "sthitaprajñasya kā bhāṣā", 8),
    ("p", "समाधिस्थस्य केशव", "samādhisthasya keśava", 8),
    ("p", "स्थितधीः किं प्रभाषेत", "sthitadhīḥ kiṃ prabhāṣeta", 8),
    ("p", "किमासीत व्रजेत किम्", "kimāsīta vrajeta kim", 8),
],

"2.55": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "प्रजहाति यदा कामान्", "prajahāti yadā kāmān", 8),
    ("p", "सर्वान्पार्थ मनोगतान्", "sarvānpārtha manogatān", 8),
    ("p", "आत्मन्येवात्मना तुष्टः", "ātmanyevātmanā tuṣṭaḥ", 8),
    ("p", "स्थितप्रज्ञस्तदोच्यते", "sthitaprajñastadocyate", 8),
],

"2.56": [
    ("p", "दुःखेष्वनुद्विग्नमनाः", "duḥkheṣvanudvignamanāḥ", 8),
    ("p", "सुखेषु विगतस्पृहः", "sukheṣu vigataspṛhaḥ", 8),
    ("p", "वीतरागभयक्रोधः", "vītarāgabhayakrodhaḥ", 8),
    ("p", "स्थितधीर्मुनिरुच्यते", "sthitadhīrmunirucyate", 8),
],

"2.57": [
    ("p", "यः सर्वत्रानभिस्नेह", "yaḥ sarvatrānabhisneha", 8),
    ("p", "स्तत्तत्प्राप्य शुभाशुभम्", "stattatprāpya śubhāśubham", 8),
    ("p", "नाभिनन्दति न द्वेष्टि", "nābhinandati na dveṣṭi", 8),
    ("p", "तस्य प्रज्ञा प्रतिष्ठिता", "tasya prajñā pratiṣṭhitā", 8),
],

"2.58": [
    ("p", "यदा संहरते चायं", "yadā saṃharate cāyaṃ", 8),
    ("p", "कूर्मोऽङ्गानीव सर्वशः", "kūrmo’ṅgānīva sarvaśaḥ", 8),
    ("p", "इन्द्रियाणीन्द्रियार्थेभ्यस्", "indriyāṇīndriyārthebhyas", 8),
    ("p", "तस्य प्रज्ञा प्रतिष्ठिता", "tasya prajñā pratiṣṭhitā", 8),
],

"2.59": [
    ("p", "विषया विनिवर्तन्ते", "viṣayā vinivartante", 8),
    ("p", "निराहारस्य देहिनः", "nirāhārasya dehinaḥ", 8),
    ("p", "रसवर्जं रसोऽप्यस्य", "rasavarjaṃ raso’pyasya", 8),
    ("p", "परं दृष्ट्वा निवर्तते", "paraṃ dṛṣṭvā nivartate", 8),
],

"2.60": [
    ("p", "यततो ह्यपि कौन्तेय", "yatato hyapi kaunteya", 8),
    ("p", "पुरुषस्य विपश्चितः", "puruṣasya vipaścitaḥ", 8),
    ("p", "इन्द्रियाणि प्रमाथीनि", "indriyāṇi pramāthīni", 8),
    ("p", "हरन्ति प्रसभं मनः", "haranti prasabhaṃ manaḥ", 8),
],

"2.61": [
    ("p", "तानि सर्वाणि संयम्य", "tāni sarvāṇi saṃyamya", 8),
    ("p", "युक्त आसीत मत्परः", "yukta āsīta matparaḥ", 8),
    ("p", "वशे हि यस्येन्द्रियाणि", "vaśe hi yasyendriyāṇi", 8),
    ("p", "तस्य प्रज्ञा प्रतिष्ठिता", "tasya prajñā pratiṣṭhitā", 8),
],

"2.62": [
    ("p", "ध्यायतो विषयान्पुंसः", "dhyāyato viṣayānpuṃsaḥ", 8),
    ("p", "सङ्गस्तेषूपजायते", "saṅgasteṣūpajāyate", 8),
    ("p", "सङ्गात्सञ्जायते कामः", "saṅgātsañjāyate kāmaḥ", 8),
    ("p", "कामात्क्रोधोऽभिजायते", "kāmātkrodho’bhijāyate", 8),
],

"2.63": [
    ("p", "क्रोधाद्भवति सम्मोहः", "krodhādbhavati sammohaḥ", 8),
    ("p", "सम्मोहात्स्मृतिविभ्रमः", "sammohātsmṛtivibhramaḥ", 8),
    ("p", "स्मृतिभ्रंशाद् बुद्धिनाशो", "smṛtibhraṃśād buddhināśo", 8),
    ("p", "बुद्धिनाशात्प्रणश्यति", "buddhināśātpraṇaśyati", 8),
],

"2.64": [
    ("p", "रागद्वेषवियुक्तैस्तु", "rāgadveṣaviyuktaistu", 8),
    ("p", "विषयानिन्द्रियैश्चरन्", "viṣayānindriyaiścaran", 8),
    ("p", "आत्मवश्यैर्विधेयात्मा", "ātmavaśyairvidheyātmā", 8),
    ("p", "प्रसादमधिगच्छति", "prasādamadhigacchati", 8),
],

"2.65": [
    ("p", "प्रसादे सर्वदुःखानां", "prasāde sarvaduḥkhānāṃ", 8),
    ("p", "हानिरस्योपजायते", "hānirasyopajāyate", 8),
    ("p", "प्रसन्नचेतसो ह्याशु", "prasannacetaso hyāśu", 8),
    ("p", "बुद्धिः पर्यवतिष्ठते", "buddhiḥ paryavatiṣṭhate", 8),
],

"2.66": [
    ("p", "नास्ति बुद्धिरयुक्तस्य", "nāsti buddhirayuktasya", 8),
    ("p", "न चायुक्तस्य भावना", "na cāyuktasya bhāvanā", 8),
    ("p", "न चाभावयतः शान्तिर्", "na cābhāvayataḥ śāntir", 8),
    ("p", "अशान्तस्य कुतः सुखम्", "aśāntasya kutaḥ sukham", 8),
],

"2.67": [
    ("p", "इन्द्रियाणां हि चरतां", "indriyāṇāṃ hi caratāṃ", 8),
    ("p", "यन्मनोऽनुविधीयते", "yanmano’nuvidhīyate", 8),
    ("p", "तदस्य हरति प्रज्ञां", "tadasya harati prajñāṃ", 8),
    ("p", "वायुर्नावमिवाम्भसि", "vāyurnāvamivāmbhasi", 8),
],

"2.68": [
    ("p", "तस्माद्यस्य महाबाहो", "tasmādyasya mahābāho", 8),
    ("p", "निगृहीतानि सर्वशः", "nigṛhītāni sarvaśaḥ", 8),
    ("p", "इन्द्रियाणीन्द्रियार्थेभ्यस्", "indriyāṇīndriyārthebhyas", 8),
    ("p", "तस्य प्रज्ञा प्रतिष्ठिता", "tasya prajñā pratiṣṭhitā", 8),
],

"2.69": [
    ("p", "या निशा सर्वभूतानां", "yā niśā sarvabhūtānāṃ", 8),
    ("p", "तस्यां जागर्ति संयमी", "tasyāṃ jāgarti saṃyamī", 8),
    ("p", "यस्यां जाग्रति भूतानि", "yasyāṃ jāgrati bhūtāni", 8),
    ("p", "सा निशा पश्यतो मुनेः", "sā niśā paśyato muneḥ", 8),
],

"2.70": [
    ("p", "आपूर्यमाणमचलप्रतिष्ठं", "āpūryamāṇamacalapratiṣṭhaṃ", 11),
    ("p", "समुद्रमापः प्रविशन्ति यद्वत्", "samudramāpaḥ praviśanti yadvat", 11),
    ("p", "तद्वत्कामा यं प्रविशन्ति सर्वे", "tadvatkāmā yaṃ praviśanti sarve", 11),
    ("p", "स शान्तिमाप्नोति न कामकामी", "sa śāntimāpnoti na kāmakāmī", 11),
],

"2.71": [
    ("p", "विहाय कामान्यः सर्वान्", "vihāya kāmānyaḥ sarvān", 8),
    ("p", "पुमांश्चरति निःस्पृहः", "pumāṃścarati niḥspṛhaḥ", 8),
    ("p", "निर्ममो निरहङ्कारः", "nirmamo nirahaṅkāraḥ", 8),
    ("p", "स शान्तिमधिगच्छति", "sa śāntimadhigacchati", 8),
],

"2.72": [
    ("p", "एषा ब्राह्मी स्थितिः पार्थ", "eṣā brāhmī sthitiḥ pārtha", 8),
    ("p", "नैनां प्राप्य विमुह्यति", "naināṃ prāpya vimuhyati", 8),
    ("p", "स्थित्वास्यामन्तकालेऽपि", "sthitvāsyāmantakāle’pi", 8),
    ("p", "ब्रह्मनिर्वाणमृच्छति", "brahmanirvāṇamṛcchati", 8),
],

}
