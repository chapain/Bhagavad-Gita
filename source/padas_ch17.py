# -*- coding: utf-8 -*-
"""padas_ch17.py — the pāda (quarter) division of every verse in chapter 17.

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
printed verbatim from ch17.json.
"""

GITA_CH17_PADAS = {
"17.01": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "ये शास्त्रविधिमुत्सृज्य", "ye śāstravidhimutsṛjya", 8),
    ("p", "यजन्ते श्रद्धयान्विताः", "yajante śraddhayānvitāḥ", 8),
    ("p", "तेषां निष्ठा तु का कृष्ण", "teṣāṃ niṣṭhā tu kā kṛṣṇa", 8),
    ("p", "सत्त्वमाहो रजस्तमः", "sattvamāho rajastamaḥ", 8),
],

"17.02": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "त्रिविधा भवति श्रद्धा", "trividhā bhavati śraddhā", 8),
    ("p", "देहिनां सा स्वभावजा", "dehināṃ sā svabhāvajā", 8),
    ("p", "सात्त्विकी राजसी चैव", "sāttvikī rājasī caiva", 8),
    ("p", "तामसी चेति तां शृणु", "tāmasī ceti tāṃ śṛṇu", 8),
],

"17.03": [
    ("p", "सत्त्वानुरूपा सर्वस्य", "sattvānurūpā sarvasya", 8),
    ("p", "श्रद्धा भवति भारत", "śraddhā bhavati bhārata", 8),
    ("p", "श्रद्धामयोऽयं पुरुषः", "śraddhāmayo’yaṃ puruṣaḥ", 8),
    ("p", "यो यच्छ्रद्धः स एव सः", "yo yacchraddhaḥ sa eva saḥ", 8),
],

"17.04": [
    ("p", "यजन्ते सात्त्विका देवान्", "yajante sāttvikā devān", 8),
    ("p", "यक्षरक्षांसि राजसाः", "yakṣarakṣāṃsi rājasāḥ", 8),
    ("p", "प्रेतान्भूतगणांश्चान्ये", "pretānbhūtagaṇāṃścānye", 8),
    ("p", "यजन्ते तामसा जनाः", "yajante tāmasā janāḥ", 8),
],

"17.05": [
    ("p", "अशास्त्रविहितं घोरं", "aśāstravihitaṃ ghoraṃ", 8),
    ("p", "तप्यन्ते ये तपो जनाः", "tapyante ye tapo janāḥ", 8),
    ("p", "दम्भाहङ्कारसंयुक्ताः", "dambhāhaṅkārasaṃyuktāḥ", 8),
    ("p", "कामरागबलान्विताः", "kāmarāgabalānvitāḥ", 8),
],

"17.06": [
    ("p", "कर्शयन्तः शरीरस्थं", "karśayantaḥ śarīrasthaṃ", 8),
    ("p", "भूतग्राममचेतसः", "bhūtagrāmamacetasaḥ", 8),
    ("p", "मां चैवान्तःशरीरस्थं", "māṃ caivāntaḥśarīrasthaṃ", 8),
    ("p", "तान्विद्ध्यासुरनिश्चयान्", "tānviddhyāsuraniścayān", 8),
],

"17.07": [
    ("p", "आहारस्त्वपि सर्वस्य", "āhārastvapi sarvasya", 8),
    ("p", "त्रिविधो भवति प्रियः", "trividho bhavati priyaḥ", 8),
    ("p", "यज्ञस्तपस्तथा दानं", "yajñastapastathā dānaṃ", 8),
    ("p", "तेषां भेदमिमं शृणु", "teṣāṃ bhedamimaṃ śṛṇu", 8),
],

"17.08": [
    ("p", "आयुःसत्त्वबलारोग्य", "āyuḥsattvabalārogya", 8),
    ("p", "सुखप्रीतिविवर्धनाः", "sukhaprītivivardhanāḥ", 8),
    ("p", "रस्याः स्निग्धाः स्थिरा हृद्याः", "rasyāḥ snigdhāḥ sthirā hṛdyāḥ", 8),
    ("p", "आहाराः सात्त्विकप्रियाः", "āhārāḥ sāttvikapriyāḥ", 8),
],

"17.09": [
    ("p", "कट्वम्ललवणात्युष्ण", "kaṭvamlalavaṇātyuṣṇa", 8),
    ("p", "तीक्ष्णरूक्षविदाहिनः", "tīkṣṇarūkṣavidāhinaḥ", 8),
    ("p", "आहारा राजसस्येष्टाः", "āhārā rājasasyeṣṭāḥ", 8),
    ("p", "दुःखशोकामयप्रदाः", "duḥkhaśokāmayapradāḥ", 8),
],

"17.10": [
    ("p", "यातयामं गतरसं", "yātayāmaṃ gatarasaṃ", 8),
    ("p", "पूति पर्युषितं च यत्", "pūti paryuṣitaṃ ca yat", 8),
    ("p", "उच्छिष्टमपि चामेध्यं", "ucchiṣṭamapi cāmedhyaṃ", 8),
    ("p", "भोजनं तामसप्रियम्", "bhojanaṃ tāmasapriyam", 8),
],

"17.11": [
    ("p", "अफलाकाङ्क्षिभिर्यज्ञः", "aphalākāṅkṣibhiryajñaḥ", 8),
    ("p", "विधिदृष्टो य इज्यते", "vidhidṛṣṭo ya ijyate", 8),
    ("p", "यष्टव्यमेवेति मनः", "yaṣṭavyameveti manaḥ", 8),
    ("p", "समाधाय स सात्त्विकः", "samādhāya sa sāttvikaḥ", 8),
],

"17.12": [
    ("p", "अभिसन्धाय तु फलं", "abhisandhāya tu phalaṃ", 8),
    ("p", "दम्भार्थमपि चैव यत्", "dambhārthamapi caiva yat", 8),
    ("p", "इज्यते भरतश्रेष्ठ", "ijyate bharataśreṣṭha", 8),
    ("p", "तं यज्ञं विद्धि राजसम्", "taṃ yajñaṃ viddhi rājasam", 8),
],

"17.13": [
    ("p", "विधिहीनमसृष्टान्नं", "vidhihīnamasṛṣṭānnaṃ", 8),
    ("p", "मन्त्रहीनमदक्षिणम्", "mantrahīnamadakṣiṇam", 8),
    ("p", "श्रद्धाविरहितं यज्ञं", "śraddhāvirahitaṃ yajñaṃ", 8),
    ("p", "तामसं परिचक्षते", "tāmasaṃ paricakṣate", 8),
],

"17.14": [
    ("p", "देवद्विजगुरुप्राज्ञपूजनं", "devadvijaguruprājñapūjanaṃ", 11),
    ("p", "शौचमार्जवम्", " śaucamārjavam", 5),
    ("p", "ब्रह्मचर्यमहिंसा च", "brahmacaryamahiṃsā ca", 8),
    ("p", "शारीरं तप उच्यते", "śārīraṃ tapa ucyate", 8),
],

"17.15": [
    ("p", "अनुद्वेगकरं वाक्यं", "anudvegakaraṃ vākyaṃ", 8),
    ("p", "सत्यं प्रियहितं च यत्", "satyaṃ priyahitaṃ ca yat", 8),
    ("p", "स्वाध्यायाभ्यसनं चैव", "svādhyāyābhyasanaṃ caiva", 8),
    ("p", "वाङ्मयं तप उच्यते", "vāṅmayaṃ tapa ucyate", 8),
],

"17.16": [
    ("p", "मनःप्रसादः सौम्यत्वं", "manaḥprasādaḥ saumyatvaṃ", 8),
    ("p", "मौनमात्मविनिग्रहः", "maunamātmavinigrahaḥ", 8),
    ("p", "भावसंशुद्धिरित्येतत्", "bhāvasaṃśuddhirityetat", 8),
    ("p", "तपो मानसमुच्यते", " tapo mānasamucyate", 8),
],

"17.17": [
    ("p", "श्रद्धया परया तप्तं", "śraddhayā parayā taptaṃ", 8),
    ("p", "तपस्तत्त्रिविधं नरैः", "tapastattrividhaṃ naraiḥ", 8),
    ("p", "अफलाकाङ्क्षिभिर्युक्तैः", "aphalākāṅkṣibhiryuktaiḥ", 8),
    ("p", "सात्त्विकं परिचक्षते", "sāttvikaṃ paricakṣate", 8),
],

"17.18": [
    ("p", "सत्कारमानपूजार्थं", "satkāramānapūjārthaṃ", 8),
    ("p", "तपो दम्भेन चैव यत्", "tapo dambhena caiva yat", 8),
    ("p", "क्रियते तदिह प्रोक्तं", "kriyate tadiha proktaṃ", 8),
    ("p", "राजसं चलमध्रुवम्", "rājasaṃ calamadhruvam", 8),
],

"17.19": [
    ("p", "मूढग्राहेणात्मनो", "mūḍhagrāheṇātmano", 7),
    ("p", "यत् पीडया क्रियते तपः", " yat pīḍayā kriyate tapaḥ", 9),
    ("p", "परस्योत्सादनार्थं", "parasyotsādanārthaṃ", 7),
    ("p", "वातत्तामसमुदाहृतम्", " vātattāmasamudāhṛtam", 9),
],

"17.20": [
    ("p", "दातव्यमिति यद्दानं", "dātavyamiti yaddānaṃ", 8),
    ("p", "दीयतेऽनुपकारिणे", "dīyate’nupakāriṇe", 8),
    ("p", "देशे काले च पात्रे च", "deśe kāle ca pātre ca", 8),
    ("p", "तद्दानं सात्त्विकं स्मृतम्", "taddānaṃ sāttvikaṃ smṛtam", 8),
],

"17.21": [
    ("p", "यत्तु प्रत्युपकारार्थं", "yattu pratyupakārārthaṃ", 8),
    ("p", "फलमुद्दिश्य वा पुनः", "phalamuddiśya vā punaḥ", 8),
    ("p", "दीयते च परिक्लिष्टं", "dīyate ca parikliṣṭaṃ", 8),
    ("p", "तद्दानं राजसं स्मृतम्", "taddānaṃ rājasaṃ smṛtam", 8),
],

"17.22": [
    ("p", "अदेशकाले यद्दानं", "adeśakāle yaddānaṃ", 8),
    ("p", "अपात्रेभ्यश्च दीयते", "apātrebhyaśca dīyate", 8),
    ("p", "असत्कृतमवज्ञातं", "asatkṛtamavajñātaṃ", 8),
    ("p", "तत्तामसमुदाहृतम्", "tattāmasamudāhṛtam", 8),
],

"17.23": [
    ("p", "ओं तत्सदिति निर्देशः", "oṃ tatsaditi nirdeśaḥ", 8),
    ("p", "ब्रह्मणस्त्रिविधः स्मृतः", "brahmaṇastrividhaḥ smṛtaḥ", 8),
    ("p", "ब्राह्मणास्तेन वेदाश्च", "brāhmaṇāstena vedāśca", 8),
    ("p", "यज्ञाश्च विहिताः पुरा", "yajñāśca vihitāḥ purā", 8),
],

"17.24": [
    ("p", "तस्मादोमित्युदाहृत्य", "tasmādomityudāhṛtya", 8),
    ("p", "यज्ञदानतपःक्रियाः", "yajñadānatapaḥkriyāḥ", 8),
    ("p", "प्रवर्तन्ते विधानोक्ताः", "pravartante vidhānoktāḥ", 8),
    ("p", "सततं ब्रह्मवादिनाम्", "satataṃ brahmavādinām", 8),
],

"17.25": [
    ("p", "तदित्यनभिसन्धाय", "tadityanabhisandhāya", 8),
    ("p", "फलं यज्ञतपःक्रियाः", "phalaṃ yajñatapaḥkriyāḥ", 8),
    ("p", "दानक्रियाश्च विविधाः", "dānakriyāśca vividhāḥ", 8),
    ("p", "क्रियन्ते मोक्षकाङ्क्षिभिः", "kriyante mokṣakāṅkṣibhiḥ", 8),
],

"17.26": [
    ("p", "सद्भावे साधुभावे च", "sadbhāve sādhubhāve ca", 8),
    ("p", "सदित्येतत्प्रयुज्यते", "sadityetatprayujyate", 8),
    ("p", "प्रशस्ते कर्मणि तथा", "praśaste karmaṇi tathā", 8),
    ("p", "सच्छब्दः पार्थ युज्यते", "sacchabdaḥ pārtha yujyate", 8),
],

"17.27": [
    ("p", "यज्ञे तपसि दाने च", "yajñe tapasi dāne ca", 8),
    ("p", "स्थितिः सदिति चोच्यते", "sthitiḥ saditi cocyate", 8),
    ("p", "कर्म चैव तदर्थीयं", "karma caiva tadarthīyaṃ", 8),
    ("p", "सदित्येवाभिधीयते", "sadityevābhidhīyate", 8),
],

"17.28": [
    ("p", "अश्रद्धया हुतं", "aśraddhayā hutaṃ", 6),
    ("p", "दत्तंतपस्तप्तं कृतं च यत्", " dattaṃtapastaptaṃ kṛtaṃ ca yat", 10),
    ("p", "असदित्युच्यते पार्थ", "asadityucyate pārtha", 8),
    ("p", "न च तत्प्रेत्य नो इह", "na ca tatpretya no iha", 8),
],

}
