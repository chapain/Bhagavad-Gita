# -*- coding: utf-8 -*-
"""padas_ch7.py — the pāda (quarter) division of every verse in chapter 7.

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
printed verbatim from ch7.json.
"""

GITA_CH7_PADAS = {
"7.01": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "मय्यासक्तमनाः पार्थ", "mayyāsaktamanāḥ pārtha", 8),
    ("p", "योगं युञ्जन्मदाश्रयः", "yogaṃ yuñjanmadāśrayaḥ", 8),
    ("p", "असंशयं समग्रं मां", "asaṃśayaṃ samagraṃ māṃ", 8),
    ("p", "यथा ज्ञास्यसि तच्छृणु", "yathā jñāsyasi tacchṛṇu", 8),
],

"7.02": [
    ("p", "ज्ञानं तेऽहं सविज्ञानम्", "jñānaṃ te’haṃ savijñānam", 8),
    ("p", "इदं वक्ष्याम्यशेषतः", "idaṃ vakṣyāmyaśeṣataḥ", 8),
    ("p", "यज्ज्ञात्वा नेह भूयोऽन्यज्", "yajjñātvā neha bhūyo’nyaj", 8),
    ("p", "ज्ञातव्यमवशिष्यते", "jñātavyamavaśiṣyate", 8),
],

"7.03": [
    ("p", "मनुष्याणां सहस्रेषु", "manuṣyāṇāṃ sahasreṣu", 8),
    ("p", "कश्चिद्यतति सिद्धये", "kaścidyatati siddhaye", 8),
    ("p", "यततामपि सिद्धानां", "yatatāmapi siddhānāṃ", 8),
    ("p", "कश्चिन्मां वेत्ति तत्त्वतः", "kaścinmāṃ vetti tattvataḥ", 8),
],

"7.04": [
    ("p", "भूमिरापोऽनलो वायुः", "bhūmirāpo’nalo vāyuḥ", 8),
    ("p", "खं मनो बुद्धिरेव च", "khaṃ mano buddhireva ca", 8),
    ("p", "अहङ्कार इतीयं मे", "ahaṅkāra itīyaṃ me", 8),
    ("p", "भिन्ना प्रकृतिरष्टधा", "bhinnā prakṛtiraṣṭadhā", 8),
],

"7.05": [
    ("p", "अपरेयमितस्त्वन्यां", "apareyamitastvanyāṃ", 8),
    ("p", "प्रकृतिं विद्धि मे पराम्", "prakṛtiṃ viddhi me parām", 8),
    ("p", "जीवभूतां महाबाहो", "jīvabhūtāṃ mahābāho", 8),
    ("p", "ययेदं धार्यते जगत्", "yayedaṃ dhāryate jagat", 8),
],

"7.06": [
    ("p", "एतद्योनीनि भूतानि", "etadyonīni bhūtāni", 8),
    ("p", "सर्वाणीत्युपधारय", "sarvāṇītyupadhāraya", 8),
    ("p", "अहं कृत्स्नस्य जगतः", "ahaṃ kṛtsnasya jagataḥ", 8),
    ("p", "प्रभवः प्रलयस्तथा", "prabhavaḥ pralayastathā", 8),
],

"7.07": [
    ("p", "मत्तः परतरं नान्यत्", "mattaḥ parataraṃ nānyat", 8),
    ("p", "किञ्चिदस्ति धनञ्जय", "kiñcidasti dhanañjaya", 8),
    ("p", "मयि सर्वमिदं प्रोतं", "mayi sarvamidaṃ protaṃ", 8),
    ("p", "सूत्रे मणिगणा इव", "sūtre maṇigaṇā iva", 8),
],

"7.08": [
    ("p", "रसोऽहमप्सु कौन्तेय", "raso’hamapsu kaunteya", 8),
    ("p", "प्रभास्मि शशिसूर्ययोः", "prabhāsmi śaśisūryayoḥ", 8),
    ("p", "प्रणवः सर्ववेदेषु", "praṇavaḥ sarvavedeṣu", 8),
    ("p", "शब्दः खे पौरुषं नृषु", "śabdaḥ khe pauruṣaṃ nṛṣu", 8),
],

"7.09": [
    ("p", "पुण्यो गन्धः पृथिव्यां च", "puṇyo gandhaḥ pṛthivyāṃ ca", 8),
    ("p", "तेजश्चास्मि विभावसौ", "tejaścāsmi vibhāvasau", 8),
    ("p", "जीवनं सर्वभूतेषु", "jīvanaṃ sarvabhūteṣu", 8),
    ("p", "तपश्चास्मि तपस्विषु", "tapaścāsmi tapasviṣu", 8),
],

"7.10": [
    ("p", "बीजं मां सर्वभूतानां", "bījaṃ māṃ sarvabhūtānāṃ", 8),
    ("p", "विद्धि पार्थ सनातनम्", "viddhi pārtha sanātanam", 8),
    ("p", "बुद्धिर्बुद्धिमतामस्मि", "buddhirbuddhimatāmasmi", 8),
    ("p", "तेजस्तेजस्विनामहम्", "tejastejasvināmaham", 8),
],

"7.11": [
    ("p", "बलं बलवतां चाहं", "balaṃ balavatāṃ cāhaṃ", 8),
    ("p", "कामरागविवर्जितम्", "kāmarāgavivarjitam", 8),
    ("p", "धर्माविरुद्धो भूतेषु", "dharmāviruddho bhūteṣu", 8),
    ("p", "कामोऽस्मि भरतर्षभ", "kāmo’smi bharatarṣabha", 8),
],

"7.12": [
    ("p", "ये चैव सात्त्विका भावा", "ye caiva sāttvikā bhāvā", 8),
    ("p", "राजसास्तमसाश्च ये", "rājasāstamasāśca ye", 8),
    ("p", "मत्त एवेति तान्विद्धि", "matta eveti tānviddhi", 8),
    ("p", "न त्वहं तेषु ते मयि", "na tvahaṃ teṣu te mayi", 8),
],

"7.13": [
    ("p", "त्रिभिर्गुणमयैर्भावैर्", "tribhirguṇamayairbhāvair", 8),
    ("p", "एभिः सर्वमिदं जगत्", "ebhiḥ sarvamidaṃ jagat", 8),
    ("p", "मोहितं नाभिजानाति", "mohitaṃ nābhijānāti", 8),
    ("p", "मामेभ्यः परमव्ययम्", "māmebhyaḥ paramavyayam", 8),
],

"7.14": [
    ("p", "दैवी ह्येषा गुणमयी", "daivī hyeṣā guṇamayī", 8),
    ("p", "मम माया दुरत्यया", "mama māyā duratyayā", 8),
    ("p", "मामेव ये प्रपद्यन्ते", "māmeva ye prapadyante", 8),
    ("p", "मायामेतां तरन्ति ते", "māyāmetāṃ taranti te", 8),
],

"7.15": [
    ("p", "न मां दुष्कृतिनो मूढाः", "na māṃ duṣkṛtino mūḍhāḥ", 8),
    ("p", "प्रपद्यन्ते नराधमाः", "prapadyante narādhamāḥ", 8),
    ("p", "माययापहृतज्ञाना", "māyayāpahṛtajñānā", 8),
    ("p", "आसुरं भावमाश्रिताः", "āsuraṃ bhāvamāśritāḥ", 8),
],

"7.16": [
    ("p", "चतुर्विधा भजन्ते मां", "caturvidhā bhajante māṃ", 8),
    ("p", "जनाः सुकृतिनोऽर्जुन", "janāḥ sukṛtino’rjuna", 8),
    ("p", "आर्तो जिज्ञासुरर्थार्थी", "ārto jijñāsurarthārthī", 8),
    ("p", "ज्ञानी च भरतर्षभ", "jñānī ca bharatarṣabha", 8),
],

"7.17": [
    ("p", "तेषां ज्ञानी नित्ययुक्त", "teṣāṃ jñānī nityayukta", 8),
    ("p", "एकभक्तिर्विशिष्यते", "ekabhaktirviśiṣyate", 8),
    ("p", "प्रियो हि ज्ञानिनोऽत्यर्थम्", "priyo hi jñānino’tyartham", 8),
    ("p", "अहं स च मम प्रियः", "ahaṃ sa ca mama priyaḥ", 8),
],

"7.18": [
    ("p", "उदाराः सर्व एवैते", "udārāḥ sarva evaite", 8),
    ("p", "ज्ञानी त्वात्मैव मे मतम्", "jñānī tvātmaiva me matam", 8),
    ("p", "आस्थितः स हि युक्तात्मा", "āsthitaḥ sa hi yuktātmā", 8),
    ("p", "मामेवानुत्तमां गतिम्", "māmevānuttamāṃ gatim", 8),
],

"7.19": [
    ("p", "बहूनां जन्मनामन्ते", "bahūnāṃ janmanāmante", 8),
    ("p", "ज्ञानवान्मां प्रपद्यते", "jñānavānmāṃ prapadyate", 8),
    ("p", "वासुदेवः सर्वमिति", "vāsudevaḥ sarvamiti", 8),
    ("p", "स महात्मा सुदुर्लभः", "sa mahātmā sudurlabhaḥ", 8),
],

"7.20": [
    ("p", "कामैस्तैस्तैर्हृतज्ञानाः", "kāmaistaistairhṛtajñānāḥ", 8),
    ("p", "प्रपद्यन्तेऽन्यदेवताः", "prapadyante’nyadevatāḥ", 8),
    ("p", "तं तं नियममास्थाय", "taṃ taṃ niyamamāsthāya", 8),
    ("p", "प्रकृत्या नियताः स्वया", "prakṛtyā niyatāḥ svayā", 8),
],

"7.21": [
    ("p", "यो यो यां यां तनुं भक्तः", "yo yo yāṃ yāṃ tanuṃ bhaktaḥ", 8),
    ("p", "श्रद्धयार्चितुमिच्छति", "śraddhayārcitumicchati", 8),
    ("p", "तस्य तस्याचलां श्रद्धां", "tasya tasyācalāṃ śraddhāṃ", 8),
    ("p", "तामेव विदधाम्यहम्", "tāmeva vidadhāmyaham", 8),
],

"7.22": [
    ("p", "स तया श्रद्धया युक्तस्", "sa tayā śraddhayā yuktas", 8),
    ("p", "तस्या राधनमीहते", "tasyā rādhanamīhate", 8),
    ("p", "लभते च ततः कामान्", "labhate ca tataḥ kāmān", 8),
    ("p", "मयैव विहितान्हि तान्", "mayaiva vihitānhi tān", 8),
],

"7.23": [
    ("p", "अन्तवत्तु फलं तेषां", "antavattu phalaṃ teṣāṃ", 8),
    ("p", "तद्भवत्यल्पमेधसाम्", "tadbhavatyalpamedhasām", 8),
    ("p", "देवान्देवयजो यान्ति", "devāndevayajo yānti", 8),
    ("p", "मद्भक्ता यान्ति मामपि", "madbhaktā yānti māmapi", 8),
],

"7.24": [
    ("p", "अव्यक्तं व्यक्तिमापन्नं", "avyaktaṃ vyaktimāpannaṃ", 8),
    ("p", "मन्यन्ते मामबुद्धयः", "manyante māmabuddhayaḥ", 8),
    ("p", "परं भावमजानन्तो", "paraṃ bhāvamajānanto", 8),
    ("p", "ममाव्ययमनुत्तमम्", "mamāvyayamanuttamam", 8),
],

"7.25": [
    ("p", "नाहं प्रकाशः सर्वस्य", "nāhaṃ prakāśaḥ sarvasya", 8),
    ("p", "योगमायासमावृतः", "yogamāyāsamāvṛtaḥ", 8),
    ("p", "मूढोऽयं नाभिजानाति", "mūḍho’yaṃ nābhijānāti", 8),
    ("p", "लोको मामजमव्ययम्", "loko māmajamavyayam", 8),
],

"7.26": [
    ("p", "वेदाहं समतीतानि", "vedāhaṃ samatītāni", 8),
    ("p", "वर्तमानानि चार्जुन", "vartamānāni cārjuna", 8),
    ("p", "भविष्याणि च भूतानि", "bhaviṣyāṇi ca bhūtāni", 8),
    ("p", "मां तु वेद न कश्चन", "māṃ tu veda na kaścana", 8),
],

"7.27": [
    ("p", "इच्छाद्वेषसमुत्थेन", "icchādveṣasamutthena", 8),
    ("p", "द्वन्द्वमोहेन भारत", "dvandvamohena bhārata", 8),
    ("p", "सर्वभूतानि सम्मोहं", "sarvabhūtāni sammohaṃ", 8),
    ("p", "सर्गे यान्ति परन्तप", "sarge yānti parantapa", 8),
],

"7.28": [
    ("p", "येषां त्वन्तगतं पापं", "yeṣāṃ tvantagataṃ pāpaṃ", 8),
    ("p", "जनानां पुण्यकर्मणाम्", "janānāṃ puṇyakarmaṇām", 8),
    ("p", "ते द्वन्द्वमोहनिर्मुक्ता", "te dvandvamohanirmuktā", 8),
    ("p", "भजन्ते मां दृढव्रताः", "bhajante māṃ dṛḍhavratāḥ", 8),
],

"7.29": [
    ("p", "जरामरणमोक्षाय", "jarāmaraṇamokṣāya", 8),
    ("p", "मामाश्रित्य यतन्ति ये", "māmāśritya yatanti ye", 8),
    ("p", "ते ब्रह्म तद्विदुः कृत्स्नम्", "te brahma tadviduḥ kṛtsnam", 8),
    ("p", "अध्यात्मं कर्म चाखिलम्", "adhyātmaṃ karma cākhilam", 8),
],

"7.30": [
    ("p", "साधिभूताधिदैवं मां", "sādhibhūtādhidaivaṃ māṃ", 8),
    ("p", "साधियज्ञं च ये विदुः", "sādhiyajñaṃ ca ye viduḥ", 8),
    ("p", "प्रयाणकालेऽपि च मां", "prayāṇakāle’pi ca māṃ", 8),
    ("p", "ते विदुर्युक्तचेतसः", "te viduryuktacetasaḥ", 8),
],

}
