# -*- coding: utf-8 -*-
"""padas_ch3.py — the pāda (quarter) division of every verse in chapter 3.

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
printed verbatim from ch3.json.
"""

GITA_CH3_PADAS = {
"3.01": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "ज्यायसी चेत्कर्मणस्ते", "jyāyasī cetkarmaṇaste", 8),
    ("p", "मता बुद्धिर्जनार्दन", "matā buddhirjanārdana", 8),
    ("p", "तत्किं कर्मणि घोरे मां", "tatkiṃ karmaṇi ghore māṃ", 8),
    ("p", "नियोजयसि केशव", "niyojayasi keśava", 8),
],

"3.02": [
    ("p", "व्यामिश्रेणेव वाक्येन", "vyāmiśreṇeva vākyena", 8),
    ("p", "बुद्धिं मोहयसीव मे", "buddhiṃ mohayasīva me", 8),
    ("p", "तदेकं वद निश्चित्य", "tadekaṃ vada niścitya", 8),
    ("p", "येन श्रेयोऽहमाप्नुयाम्", "yena śreyo’hamāpnuyām", 8),
],

"3.03": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "लोकेऽस्मिन्द्विविधा निष्ठा", "loke’smindvividhā niṣṭhā", 8),
    ("p", "पुरा प्रोक्ता मयानघ", "purā proktā mayānagha", 8),
    ("p", "ज्ञानयोगेन साङ्ख्यानां", "jñānayogena sāṅkhyānāṃ", 8),
    ("p", "कर्मयोगेन योगिनाम्", "karmayogena yoginām", 8),
],

"3.04": [
    ("p", "न कर्मणामनारम्भान्", "na karmaṇāmanārambhān", 8),
    ("p", "नैष्कर्म्यं पुरुषोऽश्नुते", "naiṣkarmyaṃ puruṣo’śnute", 8),
    ("p", "न च सन्न्यसनादेव", "na ca sannyasanādeva", 8),
    ("p", "सिद्धिं समधिगच्छति", "siddhiṃ samadhigacchati", 8),
],

"3.05": [
    ("p", "न हि कश्चित्क्षणमपि", "na hi kaścitkṣaṇamapi", 8),
    ("p", "जातु तिष्ठत्यकर्मकृत्", "jātu tiṣṭhatyakarmakṛt", 8),
    ("p", "कार्यते ह्यवशः कर्म", "kāryate hyavaśaḥ karma", 8),
    ("p", "सर्वः प्रकृतिजैर्गुणैः", "sarvaḥ prakṛtijairguṇaiḥ", 8),
],

"3.06": [
    ("p", "कर्मेन्द्रियाणि संयम्य", "karmendriyāṇi saṃyamya", 8),
    ("p", "य आस्ते मनसा स्मरन्", "ya āste manasā smaran", 8),
    ("p", "इन्द्रियार्थान्विमूढात्मा", "indriyārthānvimūḍhātmā", 8),
    ("p", "मिथ्याचारः स उच्यते", "mithyācāraḥ sa ucyate", 8),
],

"3.07": [
    ("p", "यस्त्विन्द्रियाणि मनसा", "yastvindriyāṇi manasā", 8),
    ("p", "नियम्यारभतेऽर्जुन", "niyamyārabhate’rjuna", 8),
    ("p", "कर्मेन्द्रियैः कर्मयोगम्", "karmendriyaiḥ karmayogam", 8),
    ("p", "असक्तः स विशिष्यते", "asaktaḥ sa viśiṣyate", 8),
],

"3.08": [
    ("p", "नियतं कुरु कर्म त्वं", "niyataṃ kuru karma tvaṃ", 8),
    ("p", "कर्म ज्यायो ह्यकर्मणः", "karma jyāyo hyakarmaṇaḥ", 8),
    ("p", "शरीरयात्रापि च ते", "śarīrayātrāpi ca te", 8),
    ("p", "न प्रसिध्येदकर्मणः", "na prasidhyedakarmaṇaḥ", 8),
],

"3.09": [
    ("p", "यज्ञार्थात्कर्मणोऽन्यत्र", "yajñārthātkarmaṇo’nyatra", 8),
    ("p", "लोकोऽयं कर्मबन्धनः", "loko’yaṃ karmabandhanaḥ", 8),
    ("p", "तदर्थं कर्म कौन्तेय", "tadarthaṃ karma kaunteya", 8),
    ("p", "मुक्तसङ्गः समाचर", "muktasaṅgaḥ samācara", 8),
],

"3.10": [
    ("p", "सहयज्ञाः प्रजाः सृष्ट्वा", "sahayajñāḥ prajāḥ sṛṣṭvā", 8),
    ("p", "पुरोवाच प्रजापतिः", "purovāca prajāpatiḥ", 8),
    ("p", "अनेन प्रसविष्यध्वम्", "anena prasaviṣyadhvam", 8),
    ("p", "एष वोऽस्त्विष्टकामधुक्", "eṣa vo’stviṣṭakāmadhuk", 8),
],

"3.11": [
    ("p", "देवान्भावयतानेन", "devānbhāvayatānena", 8),
    ("p", "ते देवा भावयन्तु वः", "te devā bhāvayantu vaḥ", 8),
    ("p", "परस्परं भावयन्तः", "parasparaṃ bhāvayantaḥ", 8),
    ("p", "श्रेयः परमवाप्स्यथ", "śreyaḥ paramavāpsyatha", 8),
],

"3.12": [
    ("p", "इष्टान्भोगान्हि वो देवा", "iṣṭānbhogānhi vo devā", 8),
    ("p", "दास्यन्ते यज्ञभाविताः", "dāsyante yajñabhāvitāḥ", 8),
    ("p", "तैर्दत्तानप्रदायैभ्यो", "tairdattānapradāyaibhyo", 8),
    ("p", "यो भुङ्क्ते स्तेन एव सः", "yo bhuṅkte stena eva saḥ", 8),
],

"3.13": [
    ("p", "यज्ञशिष्टाशिनः सन्तो", "yajñaśiṣṭāśinaḥ santo", 8),
    ("p", "मुच्यन्ते सर्वकिल्बिषैः", "mucyante sarvakilbiṣaiḥ", 8),
    ("p", "भुञ्जते ते त्वघं पापा", "bhuñjate te tvaghaṃ pāpā", 8),
    ("p", "ये पचन्त्यात्मकारणात्", "ye pacantyātmakāraṇāt", 8),
],

"3.14": [
    ("p", "अन्नाद्भवन्ति भूतानि", "annādbhavanti bhūtāni", 8),
    ("p", "पर्जन्यादन्नसम्भवः", "parjanyādannasambhavaḥ", 8),
    ("p", "यज्ञाद्भवति पर्जन्यो", "yajñādbhavati parjanyo", 8),
    ("p", "यज्ञः कर्मसमुद्भवः", "yajñaḥ karmasamudbhavaḥ", 8),
],

"3.15": [
    ("p", "कर्म ब्रह्मोद्भवं विद्धि", "karma brahmodbhavaṃ viddhi", 8),
    ("p", "ब्रह्माक्षरसमुद्भवम्", "brahmākṣarasamudbhavam", 8),
    ("p", "तस्मात्सर्वगतं ब्रह्म", "tasmātsarvagataṃ brahma", 8),
    ("p", "नित्यं यज्ञे प्रतिष्ठितम्", "nityaṃ yajñe pratiṣṭhitam", 8),
],

"3.16": [
    ("p", "एवं प्रवर्तितं चक्रं", "evaṃ pravartitaṃ cakraṃ", 8),
    ("p", "नानुवर्तयतीह यः", "nānuvartayatīha yaḥ", 8),
    ("p", "अघायुरिन्द्रियारामो", "aghāyurindriyārāmo", 8),
    ("p", "मोघं पार्थ स जीवति", "moghaṃ pārtha sa jīvati", 8),
],

"3.17": [
    ("p", "यस्त्वात्मरतिरेव स्याद्", "yastvātmaratireva syād", 8),
    ("p", "आत्मतृप्तश्च मानवः", "ātmatṛptaśca mānavaḥ", 8),
    ("p", "आत्मन्येव च सन्तुष्टस्", "ātmanyeva ca santuṣṭas", 8),
    ("p", "तस्य कार्यं न विद्यते", "tasya kāryaṃ na vidyate", 8),
],

"3.18": [
    ("p", "नैव तस्य कृतेनार्थो", "naiva tasya kṛtenārtho", 8),
    ("p", "नाकृतेनेह कश्चन", "nākṛteneha kaścana", 8),
    ("p", "न चास्य सर्वभूतेषु", "na cāsya sarvabhūteṣu", 8),
    ("p", "कश्चिदर्थव्यपाश्रयः", "kaścidarthavyapāśrayaḥ", 8),
],

"3.19": [
    ("p", "तस्मादसक्तः सततं", "tasmādasaktaḥ satataṃ", 8),
    ("p", "कार्यं कर्म समाचर", "kāryaṃ karma samācara", 8),
    ("p", "असक्तो ह्याचरन्कर्म", "asakto hyācarankarma", 8),
    ("p", "परमाप्नोति पूरुषः", "paramāpnoti pūruṣaḥ", 8),
],

"3.20": [
    ("p", "कर्मणैव हि संसिद्धिम्", "karmaṇaiva hi saṃsiddhim", 8),
    ("p", "आस्थिता जनकादयः", "āsthitā janakādayaḥ", 8),
    ("p", "लोकसङ्ग्रहमेवापि", "lokasaṅgrahamevāpi", 8),
    ("p", "सम्पश्यन्कर्तुमर्हसि", "sampaśyankartumarhasi", 8),
],

"3.21": [
    ("p", "यद्यदाचरति श्रेष्ठस्", "yadyadācarati śreṣṭhas", 8),
    ("p", "तत्तदेवेतरो जनः", "tattadevetaro janaḥ", 8),
    ("p", "स यत्प्रमाणं कुरुते", "sa yatpramāṇaṃ kurute", 8),
    ("p", "लोकस्तदनुवर्तते", "lokastadanuvartate", 8),
],

"3.22": [
    ("p", "न मे पार्थास्ति कर्तव्यं", "na me pārthāsti kartavyaṃ", 8),
    ("p", "त्रिषु लोकेषु किञ्चन", "triṣu lokeṣu kiñcana", 8),
    ("p", "नानवाप्तमवाप्तव्यं", "nānavāptamavāptavyaṃ", 8),
    ("p", "वर्त एव च कर्मणि", "varta eva ca karmaṇi", 8),
],

"3.23": [
    ("p", "यदि ह्यहं न वर्तेयं", "yadi hyahaṃ na varteyaṃ", 8),
    ("p", "जातु कर्मण्यतन्द्रितः", "jātu karmaṇyatandritaḥ", 8),
    ("p", "मम वर्त्मानुवर्तन्ते", "mama vartmānuvartante", 8),
    ("p", "मनुष्याः पार्थ सर्वशः", "manuṣyāḥ pārtha sarvaśaḥ", 8),
],

"3.24": [
    ("p", "उत्सीदेयुरिमे लोका", "utsīdeyurime lokā", 8),
    ("p", "न कुर्यां कर्म चेदहम्", "na kuryāṃ karma cedaham", 8),
    ("p", "सङ्करस्य च कर्ता स्याम्", "saṅkarasya ca kartā syām", 8),
    ("p", "उपहन्यामिमाः प्रजाः", "upahanyāmimāḥ prajāḥ", 8),
],

"3.25": [
    ("p", "सक्ताः कर्मण्यविद्वांसो", "saktāḥ karmaṇyavidvāṃso", 8),
    ("p", "यथा कुर्वन्ति भारत", "yathā kurvanti bhārata", 8),
    ("p", "कुर्याद्विद्वांस्तथाऽसक्तश्", "kuryādvidvāṃstathā’saktaś", 8),
    ("p", "चिकीर्षुर्लोकसङ्ग्रहम्", "cikīrṣurlokasaṅgraham", 8),
],

"3.26": [
    ("p", "न बुद्धिभेदं जनयेद्", "na buddhibhedaṃ janayed", 8),
    ("p", "अज्ञानां कर्मसङ्गिनाम्", "ajñānāṃ karmasaṅginām", 8),
    ("p", "जोषयेत्सर्वकर्माणि", "joṣayetsarvakarmāṇi", 8),
    ("p", "विद्वान्युक्तः समाचरन्", "vidvānyuktaḥ samācaran", 8),
],

"3.27": [
    ("p", "प्रकृतेः क्रियमाणानि", "prakṛteḥ kriyamāṇāni", 8),
    ("p", "गुणैः कर्माणि सर्वशः", "guṇaiḥ karmāṇi sarvaśaḥ", 8),
    ("p", "अहङ्कारविमूढात्मा", "ahaṅkāravimūḍhātmā", 8),
    ("p", "कर्ताहमिति मन्यते", "kartāhamiti manyate", 8),
],

"3.28": [
    ("p", "तत्त्ववित्तु महाबाहो", "tattvavittu mahābāho", 8),
    ("p", "गुणकर्मविभागयोः", "guṇakarmavibhāgayoḥ", 8),
    ("p", "गुणा गुणेषु वर्तन्ते", "guṇā guṇeṣu vartante", 8),
    ("p", "इति मत्वा न सज्जते", "iti matvā na sajjate", 8),
],

"3.29": [
    ("p", "प्रकृतेर्गुणसम्मूढाः", "prakṛterguṇasammūḍhāḥ", 8),
    ("p", "सज्जन्ते गुणकर्मसु", "sajjante guṇakarmasu", 8),
    ("p", "तानकृत्स्नविदो मन्दान्", "tānakṛtsnavido mandān", 8),
    ("p", "कृत्स्नविन्न विचालयेत्", "kṛtsnavinna vicālayet", 8),
],

"3.30": [
    ("p", "मयि सर्वाणि कर्माणि", "mayi sarvāṇi karmāṇi", 8),
    ("p", "सन्न्यस्याध्यात्मचेतसा", "sannyasyādhyātmacetasā", 8),
    ("p", "निराशीर्निर्ममो भूत्वा", "nirāśīrnirmamo bhūtvā", 8),
    ("p", "युध्यस्व विगतज्वरः", "yudhyasva vigatajvaraḥ", 8),
],

"3.31": [
    ("p", "ये मे मतमिदं नित्यम्", "ye me matamidaṃ nityam", 8),
    ("p", "अनुतिष्ठन्ति मानवाः", "anutiṣṭhanti mānavāḥ", 8),
    ("p", "श्रद्धावन्तोऽनसूयन्तो", "śraddhāvanto’nasūyanto", 8),
    ("p", "मुच्यन्ते तेऽपि कर्मभिः", "mucyante te’pi karmabhiḥ", 8),
],

"3.32": [
    ("p", "ये त्वेतदभ्यसूयन्तो", "ye tvetadabhyasūyanto", 8),
    ("p", "नानुतिष्ठन्ति मे मतम्", "nānutiṣṭhanti me matam", 8),
    ("p", "सर्वज्ञानविमूढांस्तान्", "sarvajñānavimūḍhāṃstān", 8),
    ("p", "विद्धि नष्टानचेतसः", "viddhi naṣṭānacetasaḥ", 8),
],

"3.33": [
    ("p", "सदृशं चेष्टते स्वस्याः", "sadṛśaṃ ceṣṭate svasyāḥ", 8),
    ("p", "प्रकृतेर्ज्ञानवानपि", "prakṛterjñānavānapi", 8),
    ("p", "प्रकृतिं यान्ति भूतानि", "prakṛtiṃ yānti bhūtāni", 8),
    ("p", "निग्रहः किं करिष्यति", "nigrahaḥ kiṃ kariṣyati", 8),
],

"3.34": [
    ("p", "इन्द्रियस्येन्द्रियस्यार्थे", "indriyasyendriyasyārthe", 8),
    ("p", "रागद्वेषौ व्यवस्थितौ", "rāgadveṣau vyavasthitau", 8),
    ("p", "तयोर्न वशमागच्छेत्", "tayorna vaśamāgacchet", 8),
    ("p", "तौ ह्यस्य परिपन्थिनौ", "tau hyasya paripanthinau", 8),
],

"3.35": [
    ("p", "श्रेयान्स्वधर्मो विगुणः", "śreyānsvadharmo viguṇaḥ", 8),
    ("p", "परधर्मात्स्वनुष्ठितात्", "paradharmātsvanuṣṭhitāt", 8),
    ("p", "स्वधर्मे निधनं श्रेयः", "svadharme nidhanaṃ śreyaḥ", 8),
    ("p", "परधर्मो भयावहः", "paradharmo bhayāvahaḥ", 8),
],

"3.36": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "अथ केन प्रयुक्तोऽयं", "atha kena prayukto’yaṃ", 8),
    ("p", "पापं चरति पूरुषः", "pāpaṃ carati pūruṣaḥ", 8),
    ("p", "अनिच्छन्नपि वार्ष्णेय", "anicchannapi vārṣṇeya", 8),
    ("p", "बलादिव नियोजितः", "balādiva niyojitaḥ", 8),
],

"3.37": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "काम एष क्रोध एष", "kāma eṣa krodha eṣa", 8),
    ("p", "रजोगुणसमुद्भवः", "rajoguṇasamudbhavaḥ", 8),
    ("p", "महाशनो महापाप्मा", "mahāśano mahāpāpmā", 8),
    ("p", "विद्ध्येनमिह वैरिणम्", "viddhyenamiha vairiṇam", 8),
],

"3.38": [
    ("p", "धूमेनाव्रियते वह्निर्", "dhūmenāvriyate vahnir", 8),
    ("p", "यथादर्शो मलेन च", "yathādarśo malena ca", 8),
    ("p", "यथोल्बेनावृतो गर्भस्", "yatholbenāvṛto garbhas", 8),
    ("p", "तथा तेनेदमावृतम्", "tathā tenedamāvṛtam", 8),
],

"3.39": [
    ("p", "आवृतं ज्ञानमेतेन", "āvṛtaṃ jñānametena", 8),
    ("p", "ज्ञानिनो नित्यवैरिणा", "jñānino nityavairiṇā", 8),
    ("p", "कामरूपेण कौन्तेय", "kāmarūpeṇa kaunteya", 8),
    ("p", "दुष्पूरेणानलेन च", "duṣpūreṇānalena ca", 8),
],

"3.40": [
    ("p", "इन्द्रियाणि मनो बुद्धिर्", "indriyāṇi mano buddhir", 8),
    ("p", "अस्याधिष्ठानमुच्यते", "asyādhiṣṭhānamucyate", 8),
    ("p", "एतैर्विमोहयत्येष", "etairvimohayatyeṣa", 8),
    ("p", "ज्ञानमावृत्य देहिनम्", "jñānamāvṛtya dehinam", 8),
],

"3.41": [
    ("p", "तस्मात्त्वमिन्द्रियाण्यादौ", "tasmāttvamindriyāṇyādau", 8),
    ("p", "नियम्य भरतर्षभ", "niyamya bharatarṣabha", 8),
    ("p", "पाप्मानं प्रजहिह्येनं", "pāpmānaṃ prajahihyenaṃ", 8),
    ("p", "ज्ञानविज्ञाननाशनम्", "jñānavijñānanāśanam", 8),
],

"3.42": [
    ("p", "इन्द्रियाणि पराण्याहुर्", "indriyāṇi parāṇyāhur", 8),
    ("p", "इन्द्रियेभ्यः परं मनः", "indriyebhyaḥ paraṃ manaḥ", 8),
    ("p", "मनसस्तु परा बुद्धिर्", "manasastu parā buddhir", 8),
    ("p", "यो बुद्धेः परतस्तु सः", "yo buddheḥ paratastu saḥ", 8),
],

"3.43": [
    ("p", "एवं बुद्धेः परं बुद्ध्वा", "evaṃ buddheḥ paraṃ buddhvā", 8),
    ("p", "संस्तभ्यात्मानमात्मना", "saṃstabhyātmānamātmanā", 8),
    ("p", "जहि शत्रुं महाबाहो", "jahi śatruṃ mahābāho", 8),
    ("p", "कामरूपं दुरासदम्", "kāmarūpaṃ durāsadam", 8),
],

}
