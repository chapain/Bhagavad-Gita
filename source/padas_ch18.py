# -*- coding: utf-8 -*-
"""padas_ch18.py — the pāda (quarter) division of every verse in chapter 18.

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
printed verbatim from ch18.json.
"""

GITA_CH18_PADAS = {
"18.01": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "संन्यासस्य महाबाहो", "saṃnyāsasya mahābāho", 8),
    ("p", "तत्त्वमिच्छामि वेदितुम्", "tattvamicchāmi veditum", 8),
    ("p", "त्यागस्य च हृषीकेश", "tyāgasya ca hṛṣīkeśa", 8),
    ("p", "पृथक्केशिनिषूदन", "pṛthakkeśiniṣūdana", 8),
],

"18.02": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "काम्यानां कर्मणां न्यासं", "kāmyānāṃ karmaṇāṃ nyāsaṃ", 8),
    ("p", "संन्यासं कवयो विदुः", "saṃnyāsaṃ kavayo viduḥ", 8),
    ("p", "सर्वकर्मफलत्यागं", "sarvakarmaphalatyāgaṃ", 8),
    ("p", "प्राहुस्त्यागं विचक्षणाः", "prāhustyāgaṃ vicakṣaṇāḥ", 8),
],

"18.03": [
    ("p", "त्याज्यं दोषवदित्येके", "tyājyaṃ doṣavadityeke", 8),
    ("p", "कर्म प्राहुर्मनीषिणः", "karma prāhurmanīṣiṇaḥ", 8),
    ("p", "यज्ञदानतपःकर्म", "yajñadānatapaḥkarma", 8),
    ("p", "न त्याज्यमिति चापरे", "na tyājyamiti cāpare", 8),
],

"18.04": [
    ("p", "निश्चयं शृणु मे तत्र", "niścayaṃ śṛṇu me tatra", 8),
    ("p", "त्यागे भरतसत्तम", "tyāge bharatasattama", 8),
    ("p", "त्यागो हि पुरुषव्याघ्र", "tyāgo hi puruṣavyāghra", 8),
    ("p", "त्रिविधः संप्रकीर्तितः", "trividhaḥ saṃprakīrtitaḥ", 8),
],

"18.05": [
    ("p", "यज्ञदानतपःकर्म", "yajñadānatapaḥkarma", 8),
    ("p", "न त्याज्यं कार्यमेव तत्", "na tyājyaṃ kāryameva tat", 8),
    ("p", "यज्ञो दानं तपश्चैव", "yajño dānaṃ tapaścaiva", 8),
    ("p", "पावनानि मनीषिणाम्", "pāvanāni manīṣiṇām", 8),
],

"18.06": [
    ("p", "एतान्यपि तु कर्माणि", "etānyapi tu karmāṇi", 8),
    ("p", "सङ्गं त्यक्त्वा फलानि च", "saṅgaṃ tyaktvā phalāni ca", 8),
    ("p", "कर्तव्यानीति मे पार्थ", "kartavyānīti me pārtha", 8),
    ("p", "निश्चितं मतमुत्तमम्", "niścitaṃ matamuttamam", 8),
],

"18.07": [
    ("p", "नियतस्य तु संन्यासः", "niyatasya tu saṃnyāsaḥ", 8),
    ("p", "कर्मणो नोपपद्यते", "karmaṇo nopapadyate", 8),
    ("p", "मोहात्तस्य परित्यागस्", "mohāttasya parityāgas", 8),
    ("p", "तामसः परिकीर्तितः", "tāmasaḥ parikīrtitaḥ", 8),
],

"18.08": [
    ("p", "दुःखमित्येव यत्कर्म", "duḥkhamityeva yatkarma", 8),
    ("p", "कायक्लेशभयात्त्यजेत्", "kāyakleśabhayāttyajet", 8),
    ("p", "स कृत्वा राजसं त्यागं", "sa kṛtvā rājasaṃ tyāgaṃ", 8),
    ("p", "नैव त्यागफलं लभेत्", "naiva tyāgaphalaṃ labhet", 8),
],

"18.09": [
    ("p", "कार्यमित्येव यत्कर्म", "kāryamityeva yatkarma", 8),
    ("p", "नियतं क्रियतेऽर्जुन", "niyataṃ kriyate’rjuna", 8),
    ("p", "सङ्गं त्यक्त्वा फलं चैव", "saṅgaṃ tyaktvā phalaṃ caiva", 8),
    ("p", "स त्यागः सात्त्विको मतः", "sa tyāgaḥ sāttviko mataḥ", 8),
],

"18.10": [
    ("p", "न द्वेष्ट्यकुशलं कर्म", "na dveṣṭyakuśalaṃ karma", 8),
    ("p", "कुशले नानुषज्जते", "kuśale nānuṣajjate", 8),
    ("p", "त्यागी सत्त्वसमाविष्टो", "tyāgī sattvasamāviṣṭo", 8),
    ("p", "मेधावी छिन्नसंशयः", "medhāvī chinnasaṃśayaḥ", 8),
],

"18.11": [
    ("p", "न हि देहभृता शक्यं", "na hi dehabhṛtā śakyaṃ", 8),
    ("p", "त्यक्तुं कर्माण्यशेषतः", "tyaktuṃ karmāṇyaśeṣataḥ", 8),
    ("p", "यस्तु कर्मफलत्यागी", "yastu karmaphalatyāgī", 8),
    ("p", "स त्यागीत्यभिधीयते", "sa tyāgītyabhidhīyate", 8),
],

"18.12": [
    ("p", "अनिष्टमिष्टं मिश्रं च", "aniṣṭamiṣṭaṃ miśraṃ ca", 8),
    ("p", "त्रिविधं कर्मणः फलम्", "trividhaṃ karmaṇaḥ phalam", 8),
    ("p", "भवत्यत्यागिनां प्रेत्य", "bhavatyatyāgināṃ pretya", 8),
    ("p", "न तु संन्यासिनां क्वचित्", "na tu saṃnyāsināṃ kvacit", 8),
],

"18.13": [
    ("p", "पञ्चैतानि महाबाहो", "pañcaitāni mahābāho", 8),
    ("p", "कारणानि निबोध मे", "kāraṇāni nibodha me", 8),
    ("p", "सांख्ये कृतान्ते प्रोक्तानि", "sāṃkhye kṛtānte proktāni", 8),
    ("p", "सिद्धये सर्वकर्मणाम्", "siddhaye sarvakarmaṇām", 8),
],

"18.14": [
    ("p", "अधिष्ठानं तथा कर्ता", "adhiṣṭhānaṃ tathā kartā", 8),
    ("p", "करणं च पृथग्विधम्", "karaṇaṃ ca pṛthagvidham", 8),
    ("p", "विविधाश्च पृथक्चेष्टा", "vividhāśca pṛthakceṣṭā", 8),
    ("p", "दैवं चैवात्र पञ्चमम्", "daivaṃ caivātra pañcamam", 8),
],

"18.15": [
    ("p", "शरीरवाङ्मनोभिर्यत्", "śarīravāṅmanobhiryat", 8),
    ("p", "कर्म प्रारभते नरः", "karma prārabhate naraḥ", 8),
    ("p", "न्याय्यं वा विपरीतं वा", "nyāyyaṃ vā viparītaṃ vā", 8),
    ("p", "पञ्चैते तस्य हेतवः", "pañcaite tasya hetavaḥ", 8),
],

"18.16": [
    ("p", "तत्रैवं सति कर्तारम्", "tatraivaṃ sati kartāram", 8),
    ("p", "आत्मानं केवलं तु यः", "ātmānaṃ kevalaṃ tu yaḥ", 8),
    ("p", "पश्यत्यकृतबुद्धित्वान्", "paśyatyakṛtabuddhitvān", 8),
    ("p", "न स पश्यति दुर्मतिः", "na sa paśyati durmatiḥ", 8),
],

"18.17": [
    ("p", "यस्य नाहंकृतो भावो", "yasya nāhaṃkṛto bhāvo", 8),
    ("p", "बुद्धिर्यस्य न लिप्यते", "buddhiryasya na lipyate", 8),
    ("p", "हत्वापि स इमांल्लोकान्", "hatvāpi sa imāṃllokān", 8),
    ("p", "न हन्ति न निबध्यते", "na hanti na nibadhyate", 8),
],

"18.18": [
    ("p", "ज्ञानं ज्ञेयं परिज्ञाता", "jñānaṃ jñeyaṃ parijñātā", 8),
    ("p", "त्रिविधा कर्मचोदना", "trividhā karmacodanā", 8),
    ("p", "करणं कर्म कर्तेति", "karaṇaṃ karma karteti", 8),
    ("p", "त्रिविधः कर्मसंग्रहः", "trividhaḥ karmasaṃgrahaḥ", 8),
],

"18.19": [
    ("p", "ज्ञानं कर्म च कर्ता च", "jñānaṃ karma ca kartā ca", 8),
    ("p", "त्रिधैव गुणभेदतः", "tridhaiva guṇabhedataḥ", 8),
    ("p", "प्रोच्यते गुणसंख्याने", "procyate guṇasaṃkhyāne", 8),
    ("p", "यथावच्छृणु तान्यपि", "yathāvacchṛṇu tānyapi", 8),
],

"18.20": [
    ("p", "सर्वभूतेषु येनैकं", "sarvabhūteṣu yenaikaṃ", 8),
    ("p", "भावमव्ययमीक्षते", "bhāvamavyayamīkṣate", 8),
    ("p", "अविभक्तं विभक्तेषु", "avibhaktaṃ vibhakteṣu", 8),
    ("p", "तज्ज्ञानं विद्धि सात्त्विकम्", "tajjñānaṃ viddhi sāttvikam", 8),
],

"18.21": [
    ("p", "पृथक्त्वेन तु यज्ज्ञानं", "pṛthaktvena tu yajjñānaṃ", 8),
    ("p", "नानाभावान्पृथग्विधान्", "nānābhāvānpṛthagvidhān", 8),
    ("p", "वेत्ति सर्वेषु भूतेषु", "vetti sarveṣu bhūteṣu", 8),
    ("p", "तज्ज्ञानं विद्धि राजसम्", "tajjñānaṃ viddhi rājasam", 8),
],

"18.22": [
    ("p", "यत्तु कृत्स्नवदेकस्मिन्", "yattu kṛtsnavadekasmin", 8),
    ("p", "कार्ये सक्तमहैतुकम्", "kārye saktamahaitukam", 8),
    ("p", "अतत्त्वार्थवदल्पं च", "atattvārthavadalpaṃ ca", 8),
    ("p", "तत्तामसमुदाहृतम्", "tattāmasamudāhṛtam", 8),
],

"18.23": [
    ("p", "नियतं सङ्गरहितम्", "niyataṃ saṅgarahitam", 8),
    ("p", "अरागद्वेषतःकृतम्", "arāgadveṣataḥkṛtam", 8),
    ("p", "अफलप्रेप्सुना कर्म", "aphalaprepsunā karma", 8),
    ("p", "यत्तत्सात्त्विकमुच्यते", "yattatsāttvikamucyate", 8),
],

"18.24": [
    ("p", "यत्तु कामेप्सुना कर्म", "yattu kāmepsunā karma", 8),
    ("p", "साहंकारेण वा पुनः", "sāhaṃkāreṇa vā punaḥ", 8),
    ("p", "क्रियते बहुलायासं", "kriyate bahulāyāsaṃ", 8),
    ("p", "तद्राजसमुदाहृतम्", "tadrājasamudāhṛtam", 8),
],

"18.25": [
    ("p", "अनुबन्धं क्षयं हिंसाम्", "anubandhaṃ kṣayaṃ hiṃsām", 8),
    ("p", "अनपेक्ष्य च पौरुषम्", "anapekṣya ca pauruṣam", 8),
    ("p", "मोहादारभ्यते कर्म", "mohādārabhyate karma", 8),
    ("p", "यत्तत्तामसमुच्यते", "yattattāmasamucyate", 8),
],

"18.26": [
    ("p", "मुक्तसङ्गोऽनहंवादी", "muktasaṅgo’nahaṃvādī", 8),
    ("p", "धृत्युत्साहसमन्वितः", "dhṛtyutsāhasamanvitaḥ", 8),
    ("p", "सिद्ध्यसिद्ध्योर्निर्विकारः", "siddhyasiddhyornirvikāraḥ", 8),
    ("p", "कर्ता सात्त्विक उच्यते", "kartā sāttvika ucyate", 8),
],

"18.27": [
    ("p", "रागी कर्मफलप्रेप्सुर्", "rāgī karmaphalaprepsur", 8),
    ("p", "लुब्धो हिंसात्मकोऽशुचिः", "lubdho hiṃsātmako’śuciḥ", 8),
    ("p", "हर्षशोकान्वितः कर्ता", "harṣaśokānvitaḥ kartā", 8),
    ("p", "राजसः परिकीर्तितः", "rājasaḥ parikīrtitaḥ", 8),
],

"18.28": [
    ("p", "अयुक्तः प्राकृतः स्तब्धः", "ayuktaḥ prākṛtaḥ stabdhaḥ", 8),
    ("p", "शठो नैकृतिकोऽलसः", "śaṭho naikṛtiko’lasaḥ", 8),
    ("p", "विषादी दीर्घसूत्री च", "viṣādī dīrghasūtrī ca", 8),
    ("p", "कर्ता तामस उच्यते", "kartā tāmasa ucyate", 8),
],

"18.29": [
    ("p", "बुद्धेर्भेदं धृतेश्चैव", "buddherbhedaṃ dhṛteścaiva", 8),
    ("p", "गुणतस्त्रिविधं शृणु", "guṇatastrividhaṃ śṛṇu", 8),
    ("p", "प्रोच्यमानमशेषेण", "procyamānamaśeṣeṇa", 8),
    ("p", "पृथक्त्वेन धनंजय", "pṛthaktvena dhanaṃjaya", 8),
],

"18.30": [
    ("p", "प्रवृत्तिं च निवृत्तिं च", "pravṛttiṃ ca nivṛttiṃ ca", 8),
    ("p", "कार्याकार्ये भयाभये", "kāryākārye bhayābhaye", 8),
    ("p", "बन्धं मोक्षं च या वेत्ति", "bandhaṃ mokṣaṃ ca yā vetti", 8),
    ("p", "बुद्धिः सा पार्थ सात्त्विकी", "buddhiḥ sā pārtha sāttvikī", 8),
],

"18.31": [
    ("p", "यया धर्ममधर्मं च", "yayā dharmamadharmaṃ ca", 8),
    ("p", "कार्यं चाकार्यमेव च", "kāryaṃ cākāryameva ca", 8),
    ("p", "अयथावत्प्रजानाति", "ayathāvatprajānāti", 8),
    ("p", "बुद्धिः सा पार्थ राजसी", "buddhiḥ sā pārtha rājasī", 8),
],

"18.32": [
    ("p", "अधर्मं धर्ममिति या", "adharmaṃ dharmamiti yā", 8),
    ("p", "मन्यते तमसावृता", "manyate tamasāvṛtā", 8),
    ("p", "सर्वार्थान्विपरीतांश्च", "sarvārthānviparītāṃśca", 8),
    ("p", "बुद्धिः सा पार्थ तामसी", "buddhiḥ sā pārtha tāmasī", 8),
],

"18.33": [
    ("p", "धृत्या यया धारयते", "dhṛtyā yayā dhārayate", 8),
    ("p", "मनःप्राणेन्द्रियक्रियाः", "manaḥprāṇendriyakriyāḥ", 8),
    ("p", "योगेनाव्यभिचारिण्या", "yogenāvyabhicāriṇyā", 8),
    ("p", "धृतिः सा पार्थ सात्त्विकी", "dhṛtiḥ sā pārtha sāttvikī", 8),
],

"18.34": [
    ("p", "यया तु धर्मकामार्थान्", "yayā tu dharmakāmārthān", 8),
    ("p", "धृत्या धारयतेऽर्जुन", "dhṛtyā dhārayate’rjuna", 8),
    ("p", "प्रसङ्गेन फलाकाङ्क्षी", "prasaṅgena phalākāṅkṣī", 8),
    ("p", "धृतिः सा पार्थ राजसी", "dhṛtiḥ sā pārtha rājasī", 8),
],

"18.35": [
    ("p", "यया स्वप्नं भयं शोकं", "yayā svapnaṃ bhayaṃ śokaṃ", 8),
    ("p", "विषादं मदमेव च", "viṣādaṃ madameva ca", 8),
    ("p", "न विमुञ्चति दुर्मेधा", "na vimuñcati durmedhā", 8),
    ("p", "धृतिः सा तामसी मता", "dhṛtiḥ sā tāmasī matā", 8),
],

"18.36": [
    ("p", "सुखं त्विदानीं त्रिविधं", "sukhaṃ tvidānīṃ trividhaṃ", 8),
    ("p", "शृणु मे भरतर्षभ", "śṛṇu me bharatarṣabha", 8),
    ("p", "अभ्यासाद्रमते यत्र", "abhyāsādramate yatra", 8),
    ("p", "दुःखान्तं च निगच्छति", "duḥkhāntaṃ ca nigacchati", 8),
],

"18.37": [
    ("p", "यत्तदग्रे विषमिव", "yattadagre viṣamiva", 8),
    ("p", "परिणामेऽमृतोपमम्", "pariṇāme’mṛtopamam", 8),
    ("p", "तत्सुखं सात्त्विकं प्रोक्तम्", "tatsukhaṃ sāttvikaṃ proktam", 8),
    ("p", "आत्मबुद्धिप्रसादजम्", "ātmabuddhiprasādajam", 8),
],

"18.38": [
    ("p", "विषयेन्द्रियसंयोगाद्", "viṣayendriyasaṃyogād", 8),
    ("p", "यत्तदग्रेऽमृतोपमम्", "yattadagre’mṛtopamam", 8),
    ("p", "परिणामे विषमिव", "pariṇāme viṣamiva", 8),
    ("p", "तत्सुखं राजसं स्मृतम्", "tatsukhaṃ rājasaṃ smṛtam", 8),
],

"18.39": [
    ("p", "यदग्रे चानुबन्धे च", "yadagre cānubandhe ca", 8),
    ("p", "सुखं मोहनमात्मनः", "sukhaṃ mohanamātmanaḥ", 8),
    ("p", "निद्रालस्यप्रमादोत्थं", "nidrālasyapramādotthaṃ", 8),
    ("p", "तत्तामसमुदाहृतम्", "tattāmasamudāhṛtam", 8),
],

"18.40": [
    ("p", "न तदस्ति पृथिव्यां वा", "na tadasti pṛthivyāṃ vā", 8),
    ("p", "दिवि देवेषु वा पुनः", "divi deveṣu vā punaḥ", 8),
    ("p", "सत्त्वं प्रकृतिजैर्मुक्तं", "sattvaṃ prakṛtijairmuktaṃ", 8),
    ("p", "यदेभिः स्यात्त्रिभिर्गुणैः", "yadebhiḥ syāttribhirguṇaiḥ", 8),
],

"18.41": [
    ("p", "ब्राह्मणक्षत्रियविशां", "brāhmaṇakṣatriyaviśāṃ", 8),
    ("p", "शूद्राणां च परंतप", "śūdrāṇāṃ ca paraṃtapa", 8),
    ("p", "कर्माणि प्रविभक्तानि", "karmāṇi pravibhaktāni", 8),
    ("p", "स्वभावप्रभवैर्गुणैः", "svabhāvaprabhavairguṇaiḥ", 8),
],

"18.42": [
    ("p", "शमो दमस्तपः शौचं", "śamo damastapaḥ śaucaṃ", 8),
    ("p", "क्षान्तिरार्जवमेव च", "kṣāntirārjavameva ca", 8),
    ("p", "ज्ञानं विज्ञानमास्तिक्यं", "jñānaṃ vijñānamāstikyaṃ", 8),
    ("p", "ब्रह्मकर्म स्वभावजम्", "brahmakarma svabhāvajam", 8),
],

"18.43": [
    ("p", "शौर्यं तेजो धृतिर्दाक्ष्यं", "śauryaṃ tejo dhṛtirdākṣyaṃ", 8),
    ("p", "युद्धे चाप्यपलायनम्", "yuddhe cāpyapalāyanam", 8),
    ("p", "दानमीश्वरभावश्च", "dānamīśvarabhāvaśca", 8),
    ("p", "क्षात्रं कर्म स्वभावजम्", "kṣātraṃ karma svabhāvajam", 8),
],

"18.44": [
    ("p", "कृषिगौरक्ष्यवाणिज्यं", "kṛṣigaurakṣyavāṇijyaṃ", 8),
    ("p", "वैश्यकर्म स्वभावजम्", "vaiśyakarma svabhāvajam", 8),
    ("p", "परिचर्यात्मकं कर्म", "paricaryātmakaṃ karma", 8),
    ("p", "शूद्रस्यापि स्वभावजम्", "śūdrasyāpi svabhāvajam", 8),
],

"18.45": [
    ("p", "स्वे स्वे कर्मण्यभिरतः", "sve sve karmaṇyabhirataḥ", 8),
    ("p", "संसिद्धिं लभते नरः", "saṃsiddhiṃ labhate naraḥ", 8),
    ("p", "स्वकर्मनिरतः सिद्धिं", "svakarmanirataḥ siddhiṃ", 8),
    ("p", "यथा विन्दति तच्छृणु", "yathā vindati tacchṛṇu", 8),
],

"18.46": [
    ("p", "यतः प्रवृत्तिर्भूतानां", "yataḥ pravṛttirbhūtānāṃ", 8),
    ("p", "येन सर्वमिदं ततम्", "yena sarvamidaṃ tatam", 8),
    ("p", "स्वकर्मणा तमभ्यर्च्य", "svakarmaṇā tamabhyarcya", 8),
    ("p", "सिद्धिं विन्दति मानवः", "siddhiṃ vindati mānavaḥ", 8),
],

"18.47": [
    ("p", "श्रेयान्स्वधर्मो विगुणः", "śreyānsvadharmo viguṇaḥ", 8),
    ("p", "परधर्मात्स्वनुष्ठितात्", "paradharmātsvanuṣṭhitāt", 8),
    ("p", "स्वभावनियतं कर्म", "svabhāvaniyataṃ karma", 8),
    ("p", "कुर्वन्नाप्नोति किल्बिषम्", "kurvannāpnoti kilbiṣam", 8),
],

"18.48": [
    ("p", "सहजं कर्म कौन्तेय", "sahajaṃ karma kaunteya", 8),
    ("p", "सदोषमपि न त्यजेत्", "sadoṣamapi na tyajet", 8),
    ("p", "सर्वारम्भा हि दोषेण", "sarvārambhā hi doṣeṇa", 8),
    ("p", "धूमेनाग्निरिवावृताः", "dhūmenāgnirivāvṛtāḥ", 8),
],

"18.49": [
    ("p", "असक्तबुद्धिः सर्वत्र", "asaktabuddhiḥ sarvatra", 8),
    ("p", "जितात्मा विगतस्पृहः", "jitātmā vigataspṛhaḥ", 8),
    ("p", "नैष्कर्म्यसिद्धिं परमां", "naiṣkarmyasiddhiṃ paramāṃ", 8),
    ("p", "संन्यासेनाधिगच्छति", "saṃnyāsenādhigacchati", 8),
],

"18.50": [
    ("p", "सिद्धिं प्राप्तो यथा ब्रह्म", "siddhiṃ prāpto yathā brahma", 8),
    ("p", "तथाप्नोति निबोध मे", "tathāpnoti nibodha me", 8),
    ("p", "समासेनैव कौन्तेय", "samāsenaiva kaunteya", 8),
    ("p", "निष्ठा ज्ञानस्य या परा", "niṣṭhā jñānasya yā parā", 8),
],

"18.51": [
    ("p", "बुद्ध्या विशुद्धया युक्तो", "buddhyā viśuddhayā yukto", 8),
    ("p", "धृत्यात्मानं नियम्य च", "dhṛtyātmānaṃ niyamya ca", 8),
    ("p", "शब्दादीन्विषयांस्त्यक्त्वा", "śabdādīnviṣayāṃstyaktvā", 8),
    ("p", "रागद्वेषौ व्युदस्य च", "rāgadveṣau vyudasya ca", 8),
],

"18.52": [
    ("p", "विविक्तसेवी लघ्वाशी", "viviktasevī laghvāśī", 8),
    ("p", "यतवाक्कायमानसः", "yatavākkāyamānasaḥ", 8),
    ("p", "ध्यानयोगपरो नित्यं", "dhyānayogaparo nityaṃ", 8),
    ("p", "वैराग्यं समुपाश्रितः", "vairāgyaṃ samupāśritaḥ", 8),
],

"18.53": [
    ("p", "अहंकारं बलं दर्पं", "ahaṃkāraṃ balaṃ darpaṃ", 8),
    ("p", "कामं क्रोधं परिग्रहम्", "kāmaṃ krodhaṃ parigraham", 8),
    ("p", "विमुच्य निर्ममः शान्तो", "vimucya nirmamaḥ śānto", 8),
    ("p", "ब्रह्मभूयाय कल्पते", "brahmabhūyāya kalpate", 8),
],

"18.54": [
    ("p", "ब्रह्मभूतः प्रसन्नात्मा", "brahmabhūtaḥ prasannātmā", 8),
    ("p", "न शोचति न काङ्क्षति", "na śocati na kāṅkṣati", 8),
    ("p", "समः सर्वेषु भूतेषु", "samaḥ sarveṣu bhūteṣu", 8),
    ("p", "मद्भक्तिं लभते पराम्", "madbhaktiṃ labhate parām", 8),
],

"18.55": [
    ("p", "भक्त्या मामभिजानाति", "bhaktyā māmabhijānāti", 8),
    ("p", "यावान्यश्चास्मि तत्त्वतः", "yāvānyaścāsmi tattvataḥ", 8),
    ("p", "ततो मां तत्त्वतो ज्ञात्वा", "tato māṃ tattvato jñātvā", 8),
    ("p", "विशते तदनन्तरम्", "viśate tadanantaram", 8),
],

"18.56": [
    ("p", "सर्वकर्माण्यपि सदा", "sarvakarmāṇyapi sadā", 8),
    ("p", "कुर्वाणो मद्व्यपाश्रयः", "kurvāṇo madvyapāśrayaḥ", 8),
    ("p", "मत्प्रसादादवाप्नोति", "matprasādādavāpnoti", 8),
    ("p", "शाश्वतं पदमव्ययम्", "śāśvataṃ padamavyayam", 8),
],

"18.57": [
    ("p", "चेतसा सर्वकर्माणि", "cetasā sarvakarmāṇi", 8),
    ("p", "मयि संन्यस्य मत्परः", "mayi saṃnyasya matparaḥ", 8),
    ("p", "बुद्धियोगमुपाश्रित्य", "buddhiyogamupāśritya", 8),
    ("p", "मच्चित्तः सततं भव", "maccittaḥ satataṃ bhava", 8),
],

"18.58": [
    ("p", "मच्चित्तः सर्वदुर्गाणि", "maccittaḥ sarvadurgāṇi", 8),
    ("p", "मत्प्रसादात्तरिष्यसि", "matprasādāttariṣyasi", 8),
    ("p", "अथ चेत्त्वमहंकारान्", "atha cettvamahaṃkārān", 8),
    ("p", "न श्रोष्यसि विनङ्क्ष्यसि", "na śroṣyasi vinaṅkṣyasi", 8),
],

"18.59": [
    ("p", "यद्यहंकारमाश्रित्य", "yadyahaṃkāramāśritya", 8),
    ("p", "न योत्स्य इति मन्यसे", "na yotsya iti manyase", 8),
    ("p", "मिथ्यैष व्यवसायस्ते", "mithyaiṣa vyavasāyaste", 8),
    ("p", "प्रकृतिस्त्वां नियोक्ष्यति", "prakṛtistvāṃ niyokṣyati", 8),
],

"18.60": [
    ("p", "स्वभावजेन कौन्तेय", "svabhāvajena kaunteya", 8),
    ("p", "निबद्धः स्वेन कर्मणा", "nibaddhaḥ svena karmaṇā", 8),
    ("p", "कर्तुं नेच्छसि यन्मोहात्", "kartuṃ necchasi yanmohāt", 8),
    ("p", "करिष्यस्यवशोऽपि तत्", "kariṣyasyavaśo’pi tat", 8),
],

"18.61": [
    ("p", "ईश्वरः सर्वभूतानां", "īśvaraḥ sarvabhūtānāṃ", 8),
    ("p", "हृद्देशेऽर्जुन तिष्ठति", "hṛddeśe’rjuna tiṣṭhati", 8),
    ("p", "भ्रामयन्सर्वभूतानि", "bhrāmayansarvabhūtāni", 8),
    ("p", "यन्त्रारूढानि मायया", "yantrārūḍhāni māyayā", 8),
],

"18.62": [
    ("p", "तमेव शरणं गच्छ", "tameva śaraṇaṃ gaccha", 8),
    ("p", "सर्वभावेन भारत", "sarvabhāvena bhārata", 8),
    ("p", "तत्प्रसादात्परां शान्तिं", "tatprasādātparāṃ śāntiṃ", 8),
    ("p", "स्थानं प्राप्स्यसि शाश्वतम्", "sthānaṃ prāpsyasi śāśvatam", 8),
],

"18.63": [
    ("p", "इति ते ज्ञानमाख्यातं", "iti te jñānamākhyātaṃ", 8),
    ("p", "गुह्याद्गुह्यतरं मया", "guhyādguhyataraṃ mayā", 8),
    ("p", "विमृश्यैतदशेषेण", "vimṛśyaitadaśeṣeṇa", 8),
    ("p", "यथेच्छसि तथा कुरु", "yathecchasi tathā kuru", 8),
],

"18.64": [
    ("p", "सर्वगुह्यतमं भूयः", "sarvaguhyatamaṃ bhūyaḥ", 8),
    ("p", "शृणु मे परमं वचः", "śṛṇu me paramaṃ vacaḥ", 8),
    ("p", "इष्टोऽसि मे दृढमिति", "iṣṭo’si me dṛḍhamiti", 8),
    ("p", "ततो वक्ष्यामि ते हितम्", "tato vakṣyāmi te hitam", 8),
],

"18.65": [
    ("p", "मन्मना भव मद्भक्तो", "manmanā bhava madbhakto", 8),
    ("p", "मद्याजी मां नमस्कुरु", "madyājī māṃ namaskuru", 8),
    ("p", "मामेवैष्यसि सत्यं ते", "māmevaiṣyasi satyaṃ te", 8),
    ("p", "प्रतिजाने प्रियोऽसि मे", "pratijāne priyo’si me", 8),
],

"18.66": [
    ("p", "सर्वधर्मान्परित्यज्य", "sarvadharmānparityajya", 8),
    ("p", "मामेकं शरणं व्रज", "māmekaṃ śaraṇaṃ vraja", 8),
    ("p", "अहं त्वा सर्वपापेभ्यो", "ahaṃ tvā sarvapāpebhyo", 8),
    ("p", "मोक्षयिष्यामि मा शुचः", "mokṣayiṣyāmi mā śucaḥ", 8),
],

"18.67": [
    ("p", "इदं ते नातपस्काय", "idaṃ te nātapaskāya", 8),
    ("p", "नाभक्ताय कदाचन", "nābhaktāya kadācana", 8),
    ("p", "न चाशुश्रूषवे वाच्यं", "na cāśuśrūṣave vācyaṃ", 8),
    ("p", "न च मां योऽभ्यसूयति", "na ca māṃ yo’bhyasūyati", 8),
],

"18.68": [
    ("p", "य इमं परमं गुह्यं", "ya imaṃ paramaṃ guhyaṃ", 8),
    ("p", "मद्भक्तेष्वभिधास्यति", "madbhakteṣvabhidhāsyati", 8),
    ("p", "भक्तिं मयि परां कृत्वा", "bhaktiṃ mayi parāṃ kṛtvā", 8),
    ("p", "मामेवैष्यत्यसंशयः", "māmevaiṣyatyasaṃśayaḥ", 8),
],

"18.69": [
    ("p", "न च तस्मान्मनुष्येषु", "na ca tasmānmanuṣyeṣu", 8),
    ("p", "कश्चिन्मे प्रियकृत्तमः", "kaścinme priyakṛttamaḥ", 8),
    ("p", "भविता न च मे तस्माद्", "bhavitā na ca me tasmād", 8),
    ("p", "अन्यः प्रियतरो भुवि", "anyaḥ priyataro bhuvi", 8),
],

"18.70": [
    ("p", "अध्येष्यते च य इमं", "adhyeṣyate ca ya imaṃ", 8),
    ("p", "धर्म्यं संवादमावयोः", "dharmyaṃ saṃvādamāvayoḥ", 8),
    ("p", "ज्ञानयज्ञेन तेनाहम्", "jñānayajñena tenāham", 8),
    ("p", "इष्टः स्यामिति मे मतिः", "iṣṭaḥ syāmiti me matiḥ", 8),
],

"18.71": [
    ("p", "श्रद्धावाननसूयश्च", "śraddhāvānanasūyaśca", 8),
    ("p", "शृणुयादपि यो नरः", "śṛṇuyādapi yo naraḥ", 8),
    ("p", "सोऽपि मुक्तः शुभांल्लोकान्", "so’pi muktaḥ śubhāṃllokān", 8),
    ("p", "प्राप्नुयात्पुण्यकर्मणाम्", "prāpnuyātpuṇyakarmaṇām", 8),
],

"18.72": [
    ("p", "कच्चिदेतच्छ्रुतं पार्थ", "kaccidetacchrutaṃ pārtha", 8),
    ("p", "त्वयैकाग्रेण चेतसा", "tvayaikāgreṇa cetasā", 8),
    ("p", "कच्चिदज्ञानसंमोहः", "kaccidajñānasaṃmohaḥ", 8),
    ("p", "प्रणष्टस्ते धनंजय", "praṇaṣṭaste dhanaṃjaya", 8),
],

"18.73": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "नष्टो मोहः स्मृतिर्लब्धा", "naṣṭo mohaḥ smṛtirlabdhā", 8),
    ("p", "त्वत्प्रसादान्मयाच्युत", "tvatprasādānmayācyuta", 8),
    ("p", "स्थितोऽस्मि गतसंदेहः", "sthito’smi gatasaṃdehaḥ", 8),
    ("p", "करिष्ये वचनं तव", "kariṣye vacanaṃ tava", 8),
],

"18.74": [
    ("s", "सञ्जय उवाच।", "sañjaya uvāca"),
    ("p", "इत्यहं वासुदेवस्य", "ityahaṃ vāsudevasya", 8),
    ("p", "पार्थस्य च महात्मनः", "pārthasya ca mahātmanaḥ", 8),
    ("p", "संवादमिममश्रौषम्", "saṃvādamimamaśrauṣam", 8),
    ("p", "अद्भुतं रोमहर्षणम्", "adbhutaṃ romaharṣaṇam", 8),
],

"18.75": [
    ("p", "व्यासप्रसादाच्छ्रुतवान्", "vyāsaprasādācchrutavān", 8),
    ("p", "इमं गुह्यतमं परम्", "imaṃ guhyatamaṃ param", 8),
    ("p", "योगं योगेश्वरात्कृष्णात्", "yogaṃ yogeśvarātkṛṣṇāt", 8),
    ("p", "साक्षात्कथयतः स्वयम्", "sākṣātkathayataḥ svayam", 8),
],

"18.76": [
    ("p", "राजन् संस्मृत्य संस्मृत्य", "rājan saṃsmṛtya saṃsmṛtya", 8),
    ("p", "संवादमिममद्भुतम्", "saṃvādamimamadbhutam", 8),
    ("p", "केशवार्जुनयोः पुण्यं", "keśavārjunayoḥ puṇyaṃ", 8),
    ("p", "हृष्यामि च मुहुर्मुहुः", "hṛṣyāmi ca muhurmuhuḥ", 8),
],

"18.77": [
    ("p", "तच्च संस्मृत्य संस्मृत्य", "tacca saṃsmṛtya saṃsmṛtya", 8),
    ("p", "रूपमत्यद्भुतं हरेः", "rūpamatyadbhutaṃ hareḥ", 8),
    ("p", "विस्मयो मे महान्राजन्", "vismayo me mahānrājan", 8),
    ("p", "हृष्यामि च पुनः पुनः", "hṛṣyāmi ca punaḥ punaḥ", 8),
],

"18.78": [
    ("p", "यत्र योगेश्वरः कृष्णो", "yatra yogeśvaraḥ kṛṣṇo", 8),
    ("p", "यत्र पार्थो धनुर्धरः", "yatra pārtho dhanurdharaḥ", 8),
    ("p", "तत्र श्रीर्विजयो भूतिर्", "tatra śrīrvijayo bhūtir", 8),
    ("p", "ध्रुवा नीतिर्मतिर्मम", "dhruvā nītirmatirmama", 8),
],

}
