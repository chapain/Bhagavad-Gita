# -*- coding: utf-8 -*-
"""padas_ch1.py — the pāda (quarter) division of every verse in chapter 1.

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
printed verbatim from ch1.json.
"""

GITA_CH1_PADAS = {
"1.01": [
    ("s", "धृतराष्ट्र उवाच।", "dhṛtarāṣṭra uvāca"),
    ("p", "धर्मक्षेत्रे कुरुक्षेत्रे", "dharmakṣetre kurukṣetre", 8),
    ("p", "समवेता युयुत्सवः", "samavetā yuyutsavaḥ", 8),
    ("p", "मामकाः पाण्डवाश्चैव", "māmakāḥ pāṇḍavāścaiva", 8),
    ("p", "किमकुर्वत सञ्जय", "kimakurvata sañjaya", 8),
],

"1.02": [
    ("s", "सञ्जय उवाच।", "sañjaya uvāca"),
    ("p", "दृष्ट्वा तु पाण्डवानीकं", "dṛṣṭvā tu pāṇḍavānīkaṃ", 8),
    ("p", "व्यूढं दुर्योधनस्तदा", "vyūḍhaṃ duryodhanastadā", 8),
    ("p", "आचार्यमुपसङ्गम्य", "ācāryamupasaṅgamya", 8),
    ("p", "राजा वचनमब्रवीत्", "rājā vacanamabravīt", 8),
],

"1.03": [
    ("p", "पश्यैतां पाण्डुपुत्राणाम्", "paśyaitāṃ pāṇḍuputrāṇām", 8),
    ("p", "आचार्य महतीं चमूम्", "ācārya mahatīṃ camūm", 8),
    ("p", "व्यूढां द्रुपदपुत्रेण", "vyūḍhāṃ drupadaputreṇa", 8),
    ("p", "तव शिष्येण धीमता", "tava śiṣyeṇa dhīmatā", 8),
],

"1.04": [
    ("p", "अत्र शूरा महेष्वासाः", "atra śūrā maheṣvāsāḥ", 8),
    ("p", "भीमार्जुनसमा युधि", "bhīmārjunasamā yudhi", 8),
    ("p", "युयुधानो विराटश्च", "yuyudhāno virāṭaśca", 8),
    ("p", "द्रुपदश्च महारथः", "drupadaśca mahārathaḥ", 8),
],

"1.05": [
    ("p", "धृष्टकेतुश्चेकितानः", "dhṛṣṭaketuścekitānaḥ", 8),
    ("p", "काशीराजश्च वीर्यवान्", "kāśīrājaśca vīryavān", 8),
    ("p", "पुरुजित्कुन्तिभोजश्च", "purujitkuntibhojaśca", 8),
    ("p", "शैब्यश्च नरपुङ्गवः", "śaibyaśca narapuṅgavaḥ", 8),
],

"1.06": [
    ("p", "युधामन्युश्च विक्रान्त", "yudhāmanyuśca vikrānta", 8),
    ("p", "उत्तमौजाश्च वीर्यवान्", "uttamaujāśca vīryavān", 8),
    ("p", "सौभद्रो द्रौपदेयाश्च", "saubhadro draupadeyāśca", 8),
    ("p", "सर्व एव महारथाः", "sarva eva mahārathāḥ", 8),
],

"1.07": [
    ("p", "अस्माकं तु विशिष्टा ये", "asmākaṃ tu viśiṣṭā ye", 8),
    ("p", "तान्निबोध द्विजोत्तम", "tānnibodha dvijottama", 8),
    ("p", "नायका मम सैन्यस्य", "nāyakā mama sainyasya", 8),
    ("p", "संज्ञार्थं तान्ब्रवीमि ते", "saṃjñārthaṃ tānbravīmi te", 8),
],

"1.08": [
    ("p", "भवान्भीष्मश्च कर्णश्च", "bhavānbhīṣmaśca karṇaśca", 8),
    ("p", "कृपश्च समितिञ्जयः", "kṛpaśca samitiñjayaḥ", 8),
    ("p", "अश्वत्थामा विकर्णश्च", "aśvatthāmā vikarṇaśca", 8),
    ("p", "सौमदत्तिस्तथैव च", "saumadattistathaiva ca", 8),
],

"1.09": [
    ("p", "अन्ये च बहवः शूराः", "anye ca bahavaḥ śūrāḥ", 8),
    ("p", "मदर्थे त्यक्तजीविताः", "madarthe tyaktajīvitāḥ", 8),
    ("p", "नानाशस्त्रप्रहरणाः", "nānāśastrapraharaṇāḥ", 8),
    ("p", "सर्वे युद्धविशारदाः", "sarve yuddhaviśāradāḥ", 8),
],

"1.10": [
    ("p", "अपर्याप्तं तदस्माकं", "aparyāptaṃ tadasmākaṃ", 8),
    ("p", "बलं भीष्माभिरक्षितम्", "balaṃ bhīṣmābhirakṣitam", 8),
    ("p", "पर्याप्तं त्विदमेतेषां", "paryāptaṃ tvidameteṣāṃ", 8),
    ("p", "बलं भीमाभिरक्षितम्", "balaṃ bhīmābhirakṣitam", 8),
],

"1.11": [
    ("p", "अयनेषु च सर्वेषु", "ayaneṣu ca sarveṣu", 8),
    ("p", "यथाभागमवस्थिताः", "yathābhāgamavasthitāḥ", 8),
    ("p", "भीष्ममेवाभिरक्षन्तु", "bhīṣmamevābhirakṣantu", 8),
    ("p", "भवन्तः सर्व एव हि", "bhavantaḥ sarva eva hi", 8),
],

"1.12": [
    ("p", "तस्य सञ्जनयन्हर्षं", "tasya sañjanayanharṣaṃ", 8),
    ("p", "कुरुवृद्धः पितामहः", "kuruvṛddhaḥ pitāmahaḥ", 8),
    ("p", "सिंहनादं विनद्योच्चैः", "siṃhanādaṃ vinadyoccaiḥ", 8),
    ("p", "शङ्खं दध्मौ प्रतापवान्", "śaṅkhaṃ dadhmau pratāpavān", 8),
],

"1.13": [
    ("p", "ततः शङ्खाश्च भेर्यश्च", "tataḥ śaṅkhāśca bheryaśca", 8),
    ("p", "पणवानकगोमुखाः", "paṇavānakagomukhāḥ", 8),
    ("p", "सहसैवाभ्यहन्यन्त", "sahasaivābhyahanyanta", 8),
    ("p", "स शब्दस्तुमुलोऽभवत्", "sa śabdastumulo’bhavat", 8),
],

"1.14": [
    ("p", "ततः श्वेतैर्हयैर्युक्ते", "tataḥ śvetairhayairyukte", 8),
    ("p", "महति स्यन्दने स्थितौ", "mahati syandane sthitau", 8),
    ("p", "माधवः पाण्डवश्चैव", "mādhavaḥ pāṇḍavaścaiva", 8),
    ("p", "दिव्यौ शङ्खौ प्रदध्मतुः", "divyau śaṅkhau pradadhmatuḥ", 8),
],

"1.15": [
    ("p", "पाञ्चजन्यं हृषीकेशः", "pāñcajanyaṃ hṛṣīkeśaḥ", 8),
    ("p", "देवदत्तं धनञ्जयः", "devadattaṃ dhanañjayaḥ", 8),
    ("p", "पौण्ड्रं दध्मौ महाशङ्खं", "pauṇḍraṃ dadhmau mahāśaṅkhaṃ", 8),
    ("p", "भीमकर्मा वृकोदरः", "bhīmakarmā vṛkodaraḥ", 8),
],

"1.16": [
    ("p", "अनन्तविजयं राजा", "anantavijayaṃ rājā", 8),
    ("p", "कुन्तीपुत्रो युधिष्ठिरः", "kuntīputro yudhiṣṭhiraḥ", 8),
    ("p", "नकुलः सहदेवश्च", "nakulaḥ sahadevaśca", 8),
    ("p", "सुघोषमणिपुष्पकौ", "sughoṣamaṇipuṣpakau", 8),
],

"1.17": [
    ("p", "काश्यश्च परमेष्वासः", "kāśyaśca parameṣvāsaḥ", 8),
    ("p", "शिखण्डी च महारथः", "śikhaṇḍī ca mahārathaḥ", 8),
    ("p", "धृष्टद्युम्नो विराटश्च", "dhṛṣṭadyumno virāṭaśca", 8),
    ("p", "सात्यकिश्चापराजितः", "sātyakiścāparājitaḥ", 8),
],

"1.18": [
    ("p", "द्रुपदो द्रौपदेयाश्च", "drupado draupadeyāśca", 8),
    ("p", "सर्वशः पृथिवीपते", "sarvaśaḥ pṛthivīpate", 8),
    ("p", "सौभद्रश्च महाबाहुः", "saubhadraśca mahābāhuḥ", 8),
    ("p", "शङ्खान्दध्मुः पृथक्पृथक्", "śaṅkhāndadhmuḥ pṛthakpṛthak", 8),
],

"1.19": [
    ("p", "स घोषो धार्तराष्ट्राणां", "sa ghoṣo dhārtarāṣṭrāṇāṃ", 8),
    ("p", "हृदयानि व्यदारयत्", "hṛdayāni vyadārayat", 8),
    ("p", "नभश्च पृथिवीं चैव", "nabhaśca pṛthivīṃ caiva", 8),
    ("p", "तुमुलो व्यनुनादयन्", "tumulo vyanunādayan", 8),
],

"1.20": [
    ("p", "अथ व्यवस्थितान्दृष्ट्वा", "atha vyavasthitāndṛṣṭvā", 8),
    ("p", "धार्तराष्ट्रान् कपिध्वजः", "dhārtarāṣṭrān kapidhvajaḥ", 8),
    ("p", "प्रवृत्ते शस्त्रसम्पाते", "pravṛtte śastrasampāte", 8),
    ("p", "धनुरुद्यम्य पाण्डवः", "dhanurudyamya pāṇḍavaḥ", 8),
],

"1.21": [
    ("p", "हृषीकेशं तदा वाक्यम्", "hṛṣīkeśaṃ tadā vākyam", 8),
    ("p", "इदमाह महीपते", "idamāha mahīpate", 8),
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "सेनयोरुभयोर्मध्ये", "senayorubhayormadhye", 8),
    ("p", "रथं स्थापय मेऽच्युत", "rathaṃ sthāpaya me’cyuta", 8),
],

"1.22": [
    ("p", "यावदेतान्निरीक्षेऽहं", "yāvadetānnirīkṣe’haṃ", 8),
    ("p", "योद्धुकामानवस्थितान्", "yoddhukāmānavasthitān", 8),
    ("p", "कैर्मया सह योद्धव्यम्", "kairmayā saha yoddhavyam", 8),
    ("p", "अस्मिन् रणसमुद्यमे", "asmin raṇasamudyame", 8),
],

"1.23": [
    ("p", "योत्स्यमानानवेक्षेऽहं", "yotsyamānānavekṣe’haṃ", 8),
    ("p", "य एतेऽत्र समागताः", "ya ete’tra samāgatāḥ", 8),
    ("p", "धार्तराष्ट्रस्य दुर्बुद्धेर्", "dhārtarāṣṭrasya durbuddher", 8),
    ("p", "युद्धे प्रियचिकीर्षवः", "yuddhe priyacikīrṣavaḥ", 8),
],

"1.24": [
    ("s", "सञ्जय उवाच।", "sañjaya uvāca"),
    ("p", "एवमुक्तो हृषीकेशो", "evamukto hṛṣīkeśo", 8),
    ("p", "गुडाकेशेन भारत", "guḍākeśena bhārata", 8),
    ("p", "सेनयोरुभयोर्मध्ये", "senayorubhayormadhye", 8),
    ("p", "स्थापयित्वा रथोत्तमम्", "sthāpayitvā rathottamam", 8),
],

"1.25": [
    ("p", "भीष्मद्रोणप्रमुखतः", "bhīṣmadroṇapramukhataḥ", 8),
    ("p", "सर्वेषां च महीक्षिताम्", "sarveṣāṃ ca mahīkṣitām", 8),
    ("p", "उवाच पार्थ पश्यैतान्", "uvāca pārtha paśyaitān", 8),
    ("p", "समवेतान्कुरूनिति", "samavetānkurūniti", 8),
],

"1.26": [
    ("p", "तत्रापश्यत्स्थितान्पार्थः", "tatrāpaśyatsthitānpārthaḥ", 8),
    ("p", "पितॄनथ पितामहान्", "pitṝnatha pitāmahān", 8),
    ("p", "आचार्यान्मातुलान्भ्रातॄन्", "ācāryānmātulānbhrātṝn", 8),
    ("p", "पुत्रान्पौत्रान्सखींस्तथा", "putrānpautrānsakhīṃstathā", 8),
],

"1.27": [
    ("p", "श्वशुरान्सुहृदश्चैव", "śvaśurānsuhṛdaścaiva", 8),
    ("p", "सेनयोरुभयोरपि", "senayorubhayorapi", 8),
    ("p", "तान्समीक्ष्य स कौन्तेयः", "tānsamīkṣya sa kaunteyaḥ", 8),
    ("p", "सर्वान्बन्धूनवस्थितान्", "sarvānbandhūnavasthitān", 8),
],

"1.28": [
    ("p", "कृपया परयाविष्टो", "kṛpayā parayāviṣṭo", 8),
    ("p", "विषीदन्निदमब्रवीत्", "viṣīdannidamabravīt", 8),
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "दृष्ट्वेमं स्वजनं कृष्ण", "dṛṣṭvemaṃ svajanaṃ kṛṣṇa", 8),
    ("p", "युयुत्सुं समुपस्थितम्", "yuyutsuṃ samupasthitam", 8),
],

"1.29": [
    ("p", "सीदन्ति मम गात्राणि", "sīdanti mama gātrāṇi", 8),
    ("p", "मुखं च परिशुष्यति", "mukhaṃ ca pariśuṣyati", 8),
    ("p", "वेपथुश्च शरीरे मे", "vepathuśca śarīre me", 8),
    ("p", "रोमहर्षश्च जायते", "romaharṣaśca jāyate", 8),
],

"1.30": [
    ("p", "गाण्डीवं स्रंसते हस्तात्", "gāṇḍīvaṃ sraṃsate hastāt", 8),
    ("p", "त्वक्चैव परिदह्यते", "tvakcaiva paridahyate", 8),
    ("p", "न च शक्नोम्यवस्थातुं", "na ca śaknomyavasthātuṃ", 8),
    ("p", "भ्रमतीव च मे मनः", "bhramatīva ca me manaḥ", 8),
],

"1.31": [
    ("p", "निमित्तानि च पश्यामि", "nimittāni ca paśyāmi", 8),
    ("p", "विपरीतानि केशव", "viparītāni keśava", 8),
    ("p", "न च श्रेयोऽनुपश्यामि", "na ca śreyo’nupaśyāmi", 8),
    ("p", "हत्वा स्वजनमाहवे", "hatvā svajanamāhave", 8),
],

"1.32": [
    ("p", "न काङ्क्षे विजयं कृष्ण", "na kāṅkṣe vijayaṃ kṛṣṇa", 8),
    ("p", "न च राज्यं सुखानि च", "na ca rājyaṃ sukhāni ca", 8),
    ("p", "किं नो राज्येन गोविन्द", "kiṃ no rājyena govinda", 8),
    ("p", "किं भोगैर्जीवितेन वा", "kiṃ bhogairjīvitena vā", 8),
],

"1.33": [
    ("p", "येषामर्थे काङ्क्षितं नः", "yeṣāmarthe kāṅkṣitaṃ naḥ", 8),
    ("p", "राज्यं भोगाः सुखानि च", "rājyaṃ bhogāḥ sukhāni ca", 8),
    ("p", "त इमेऽवस्थिता युद्धे", "ta ime’vasthitā yuddhe", 8),
    ("p", "प्राणांस्त्यक्त्वा धनानि च", "prāṇāṃstyaktvā dhanāni ca", 8),
],

"1.34": [
    ("p", "आचार्याः पितरः पुत्रास्", "ācāryāḥ pitaraḥ putrās", 8),
    ("p", "तथैव च पितामहाः", "tathaiva ca pitāmahāḥ", 8),
    ("p", "मातुलाः श्वशुराः पौत्राः", "mātulāḥ śvaśurāḥ pautrāḥ", 8),
    ("p", "श्यालाः सम्बन्धिनस्तथा", "śyālāḥ sambandhinastathā", 8),
],

"1.35": [
    ("p", "एतान्न हन्तुमिच्छामि", "etānna hantumicchāmi", 8),
    ("p", "घ्नतोऽपि मधुसूदन", "ghnato’pi madhusūdana", 8),
    ("p", "अपि त्रैलोक्यराज्यस्य", "api trailokyarājyasya", 8),
    ("p", "हेतोः किं नु महीकृते", "hetoḥ kiṃ nu mahīkṛte", 8),
],

"1.36": [
    ("p", "निहत्य धार्तराष्ट्रान्नः", "nihatya dhārtarāṣṭrānnaḥ", 8),
    ("p", "का प्रीतिः स्याज्जनार्दन", "kā prītiḥ syājjanārdana", 8),
    ("p", "पापमेवाश्रयेदस्मान्", "pāpamevāśrayedasmān", 8),
    ("p", "हत्वैतानाततायिनः", "hatvaitānātatāyinaḥ", 8),
],

"1.37": [
    ("p", "तस्मान्नार्हा वयं हन्तुं", "tasmānnārhā vayaṃ hantuṃ", 8),
    ("p", "धार्तराष्ट्रान्स्वबान्धवान्", "dhārtarāṣṭrānsvabāndhavān", 8),
    ("p", "स्वजनं हि कथं हत्वा", "svajanaṃ hi kathaṃ hatvā", 8),
    ("p", "सुखिनः स्याम माधव", "sukhinaḥ syāma mādhava", 8),
],

"1.38": [
    ("p", "यद्यप्येते न पश्यन्ति", "yadyapyete na paśyanti", 8),
    ("p", "लोभोपहतचेतसः", "lobhopahatacetasaḥ", 8),
    ("p", "कुलक्षयकृतं दोषं", "kulakṣayakṛtaṃ doṣaṃ", 8),
    ("p", "मित्रद्रोहे च पातकम्", "mitradrohe ca pātakam", 8),
],

"1.39": [
    ("p", "कथं न ज्ञेयमस्माभिः", "kathaṃ na jñeyamasmābhiḥ", 8),
    ("p", "पापादस्मान्निवर्तितुम्", "pāpādasmānnivartitum", 8),
    ("p", "कुलक्षयकृतं दोषं", "kulakṣayakṛtaṃ doṣaṃ", 8),
    ("p", "प्रपश्यद्भिर्जनार्दन", "prapaśyadbhirjanārdana", 8),
],

"1.40": [
    ("p", "कुलक्षये प्रणश्यन्ति", "kulakṣaye praṇaśyanti", 8),
    ("p", "कुलधर्माः सनातनाः", "kuladharmāḥ sanātanāḥ", 8),
    ("p", "धर्मे नष्टे कुलं कृत्स्नम्", "dharme naṣṭe kulaṃ kṛtsnam", 8),
    ("p", "अधर्मोऽभिभवत्युत", "adharmo’bhibhavatyuta", 8),
],

"1.41": [
    ("p", "अधर्माभिभवात्कृष्ण", "adharmābhibhavātkṛṣṇa", 8),
    ("p", "प्रदुष्यन्ति कुलस्त्रियः", "praduṣyanti kulastriyaḥ", 8),
    ("p", "स्त्रीषु दुष्टासु वार्ष्णेय", "strīṣu duṣṭāsu vārṣṇeya", 8),
    ("p", "जायते वर्णसङ्करः", "jāyate varṇasaṅkaraḥ", 8),
],

"1.42": [
    ("p", "सङ्करो नरकायैव", "saṅkaro narakāyaiva", 8),
    ("p", "कुलघ्नानां कुलस्य च", "kulaghnānāṃ kulasya ca", 8),
    ("p", "पतन्ति पितरो ह्येषां", "patanti pitaro hyeṣāṃ", 8),
    ("p", "लुप्तपिण्डोदकक्रियाः", "luptapiṇḍodakakriyāḥ", 8),
],

"1.43": [
    ("p", "दोषैरेतैः कुलघ्नानां", "doṣairetaiḥ kulaghnānāṃ", 8),
    ("p", "वर्णसङ्करकारकैः", "varṇasaṅkarakārakaiḥ", 8),
    ("p", "उत्साद्यन्ते जातिधर्माः", "utsādyante jātidharmāḥ", 8),
    ("p", "कुलधर्माश्च शाश्वताः", "kuladharmāśca śāśvatāḥ", 8),
],

"1.44": [
    ("p", "उत्सन्नकुलधर्माणां", "utsannakuladharmāṇāṃ", 8),
    ("p", "मनुष्याणां जनार्दन", "manuṣyāṇāṃ janārdana", 8),
    ("p", "नरके नियतं वासो", "narake niyataṃ vāso", 8),
    ("p", "भवतीत्यनुशुश्रुम", "bhavatītyanuśuśruma", 8),
],

"1.45": [
    ("p", "अहो बत महत्पापं", "aho bata mahatpāpaṃ", 8),
    ("p", "कर्तुं व्यवसिता वयम्", "kartuṃ vyavasitā vayam", 8),
    ("p", "यद्राज्यसुखलोभेन", "yadrājyasukhalobhena", 8),
    ("p", "हन्तुं स्वजनमुद्यताः", "hantuṃ svajanamudyatāḥ", 8),
],

"1.46": [
    ("p", "यदि मामप्रतीकारम्", "yadi māmapratīkāram", 8),
    ("p", "अशस्त्रं शस्त्रपाणयः", "aśastraṃ śastrapāṇayaḥ", 8),
    ("p", "धार्तराष्ट्रा रणे हन्युस्", "dhārtarāṣṭrā raṇe hanyus", 8),
    ("p", "तन्मे क्षेमतरं भवेत्", "tanme kṣemataraṃ bhavet", 8),
],

"1.47": [
    ("s", "सञ्जय उवाच।", "sañjaya uvāca"),
    ("p", "एवमुक्त्वार्जुनः सङ्ख्ये", "evamuktvārjunaḥ saṅkhye", 8),
    ("p", "रथोपस्थ उपाविशत्", "rathopastha upāviśat", 8),
    ("p", "विसृज्य सशरं चापं", "visṛjya saśaraṃ cāpaṃ", 8),
    ("p", "शोकसंविग्नमानसः", "śokasaṃvignamānasaḥ", 8),
],

}
