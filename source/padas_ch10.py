# -*- coding: utf-8 -*-
"""padas_ch10.py — the pāda (quarter) division of every verse in chapter 10.

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
printed verbatim from ch10.json.
"""

GITA_CH10_PADAS = {
"10.01": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "भूय एव महाबाहो", "bhūya eva mahābāho", 8),
    ("p", "शृणु मे परमं वचः", "śṛṇu me paramaṃ vacaḥ", 8),
    ("p", "यत्तेऽहं प्रीयमाणाय", "yatte’haṃ prīyamāṇāya", 8),
    ("p", "वक्ष्यामि हितकाम्यया", "vakṣyāmi hitakāmyayā", 8),
],

"10.02": [
    ("p", "न मे विदुः सुरगणाः", "na me viduḥ suragaṇāḥ", 8),
    ("p", "प्रभवं न महर्षयः", "prabhavaṃ na maharṣayaḥ", 8),
    ("p", "अहमादिर्हि देवानां", "ahamādirhi devānāṃ", 8),
    ("p", "महर्षीणां च सर्वशः", "maharṣīṇāṃ ca sarvaśaḥ", 8),
],

"10.03": [
    ("p", "यो मामजमनादिं च", "yo māmajamanādiṃ ca", 8),
    ("p", "वेत्ति लोकमहेश्वरम्", "vetti lokamaheśvaram", 8),
    ("p", "असम्मूढः स मर्त्येषु", "asammūḍhaḥ sa martyeṣu", 8),
    ("p", "सर्वपापैः प्रमुच्यते", "sarvapāpaiḥ pramucyate", 8),
],

"10.04": [
    ("p", "बुद्धिर्ज्ञानमसम्मोहः", "buddhirjñānamasammohaḥ", 8),
    ("p", "क्षमा सत्यं दमः शमः", "kṣamā satyaṃ damaḥ śamaḥ", 8),
    ("p", "सुखं दुःखं भवोऽभावः", "sukhaṃ duḥkhaṃ bhavo’bhāvaḥ", 8),
    ("p", "भयं चाभयमेव च", "bhayaṃ cābhayameva ca", 8),
],

"10.05": [
    ("p", "अहिंसा समता तुष्टिः", "ahiṃsā samatā tuṣṭiḥ", 8),
    ("p", "तपो दानं यशोऽयशः", "tapo dānaṃ yaśo’yaśaḥ", 8),
    ("p", "भवन्ति भावा भूतानां", "bhavanti bhāvā bhūtānāṃ", 8),
    ("p", "मत्त एव पृथग्विधाः", "matta eva pṛthagvidhāḥ", 8),
],

"10.06": [
    ("p", "महर्षयः सप्त पूर्वे", "maharṣayaḥ sapta pūrve", 8),
    ("p", "चत्वारो मनवस्तथा", "catvāro manavastathā", 8),
    ("p", "मद्भावा मानसा जाताः", "madbhāvā mānasā jātāḥ", 8),
    ("p", "येषां लोक इमाः प्रजाः", "yeṣāṃ loka imāḥ prajāḥ", 8),
],

"10.07": [
    ("p", "एतां विभूतिं योगं च", "etāṃ vibhūtiṃ yogaṃ ca", 8),
    ("p", "मम यो वेत्ति तत्त्वतः", "mama yo vetti tattvataḥ", 8),
    ("p", "सोऽविकम्पेन योगेन", "so’vikampena yogena", 8),
    ("p", "युज्यते नात्र संशयः", "yujyate nātra saṃśayaḥ", 8),
],

"10.08": [
    ("p", "अहं सर्वस्य प्रभवः", "ahaṃ sarvasya prabhavaḥ", 8),
    ("p", "मत्तः सर्वं प्रवर्तते", "mattaḥ sarvaṃ pravartate", 8),
    ("p", "इति मत्वा भजन्ते मां", "iti matvā bhajante māṃ", 8),
    ("p", "बुधा भावसमन्विताः", "budhā bhāvasamanvitāḥ", 8),
],

"10.09": [
    ("p", "मच्चित्ता मद्गतप्राणाः", "maccittā madgataprāṇāḥ", 8),
    ("p", "बोधयन्तः परस्परम्", "bodhayantaḥ parasparam", 8),
    ("p", "कथयन्तश्च मां नित्यं", "kathayantaśca māṃ nityaṃ", 8),
    ("p", "तुष्यन्ति च रमन्ति च", "tuṣyanti ca ramanti ca", 8),
],

"10.10": [
    ("p", "तेषां सततयुक्तानां", "teṣāṃ satatayuktānāṃ", 8),
    ("p", "भजतां प्रीतिपूर्वकम्", "bhajatāṃ prītipūrvakam", 8),
    ("p", "ददामि बुद्धियोगं तं", "dadāmi buddhiyogaṃ taṃ", 8),
    ("p", "येन मामुपयान्ति ते", "yena māmupayānti te", 8),
],

"10.11": [
    ("p", "तेषामेवानुकम्पार्थं", "teṣāmevānukampārthaṃ", 8),
    ("p", "अहमज्ञानजं तमः", "ahamajñānajaṃ tamaḥ", 8),
    ("p", "नाशयाम्यात्मभावस्थः", "nāśayāmyātmabhāvasthaḥ", 8),
    ("p", "ज्ञानदीपेन भास्वता", "jñānadīpena bhāsvatā", 8),
],

"10.12": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "परं ब्रह्म परं धाम", "paraṃ brahma paraṃ dhāma", 8),
    ("p", "पवित्रं परमं भवान्", "pavitraṃ paramaṃ bhavān", 8),
    ("p", "पुरुषं शाश्वतं दिव्यं", "puruṣaṃ śāśvataṃ divyaṃ", 8),
    ("p", "आदिदेवमजं विभुम्", "ādidevamajaṃ vibhum", 8),
],

"10.13": [
    ("p", "आहुस्त्वामृषयः सर्वे", "āhustvāmṛṣayaḥ sarve", 8),
    ("p", "देवर्षिर्नारदस्तथा", "devarṣirnāradastathā", 8),
    ("p", "असितो देवलो व्यासः", "asito devalo vyāsaḥ", 8),
    ("p", "स्वयं चैव ब्रवीषि मे", "svayaṃ caiva bravīṣi me", 8),
],

"10.14": [
    ("p", "सर्वमेतदृतं मन्ये", "sarvametadṛtaṃ manye", 8),
    ("p", "यन्मां वदसि केशव", "yanmāṃ vadasi keśava", 8),
    ("p", "न हि ते भगवन्व्यक्तिं", "na hi te bhagavanvyaktiṃ", 8),
    ("p", "विदुर्देवा न दानवाः", "vidurdevā na dānavāḥ", 8),
],

"10.15": [
    ("p", "स्वयमेवात्मनात्मानं", "svayamevātmanātmānaṃ", 8),
    ("p", "वेत्थ त्वं पुरुषोत्तम", "vettha tvaṃ puruṣottama", 8),
    ("p", "भूतभावन भूतेश", "bhūtabhāvana bhūteśa", 8),
    ("p", "देवदेव जगत्पते", "devadeva jagatpate", 8),
],

"10.16": [
    ("p", "वक्तुमर्हस्यशेषेण", "vaktumarhasyaśeṣeṇa", 8),
    ("p", "दिव्या ह्यात्मविभूतयः", "divyā hyātmavibhūtayaḥ", 8),
    ("p", "याभिर्विभूतिभिर्लोकान्", "yābhirvibhūtibhirlokān", 8),
    ("p", "इमांस्त्वं व्याप्य तिष्ठसि", " imāṃstvaṃ vyāpya tiṣṭhasi", 8),
],

"10.17": [
    ("p", "कथं विद्यामहं योगिन्", "kathaṃ vidyāmahaṃ yogin", 8),
    ("p", "त्वां सदा परिचिन्तयन्", " tvāṃ sadā paricintayan", 8),
    ("p", "केषु केषु च भावेषु", "keṣu keṣu ca bhāveṣu", 8),
    ("p", "चिन्त्योऽसि भगवन्मया", "cintyo’si bhagavanmayā", 8),
],

"10.18": [
    ("p", "विस्तरेणात्मनो योगं", "vistareṇātmano yogaṃ", 8),
    ("p", "विभूतिं च जनार्दन", "vibhūtiṃ ca janārdana", 8),
    ("p", "भूयः कथय तृप्तिर्हि", "bhūyaḥ kathaya tṛptirhi", 8),
    ("p", "शृण्वतो नास्ति मेऽमृतम्", "śṛṇvato nāsti me’mṛtam", 8),
],

"10.19": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "हन्त ते कथयिष्यामि", "hanta te kathayiṣyāmi", 8),
    ("p", "दिव्या ह्यात्मविभूतयः", "divyā hyātmavibhūtayaḥ", 8),
    ("p", "प्राधान्यतः कुरुश्रेष्ठ", "prādhānyataḥ kuruśreṣṭha", 8),
    ("p", "नास्त्यन्तो विस्तरस्य मे", "nāstyanto vistarasya me", 8),
],

"10.20": [
    ("p", "अहमात्मा गुडाकेश", "ahamātmā guḍākeśa", 8),
    ("p", "सर्वभूताशयस्थितः", "sarvabhūtāśayasthitaḥ", 8),
    ("p", "अहमादिश्च मध्यं च", "ahamādiśca madhyaṃ ca", 8),
    ("p", "भूतानामन्त एव च", "bhūtānāmanta eva ca", 8),
],

"10.21": [
    ("p", "आदित्यानामहं विष्णुः", "ādityānāmahaṃ viṣṇuḥ", 8),
    ("p", "ज्योतिषां रविरंशुमान्", "jyotiṣāṃ raviraṃśumān", 8),
    ("p", "मरीचिर्मरुतामस्मि", "marīcirmarutāmasmi", 8),
    ("p", "नक्षत्राणामहं शशी", "nakṣatrāṇāmahaṃ śaśī", 8),
],

"10.22": [
    ("p", "वेदानां सामवेदोऽस्मि", "vedānāṃ sāmavedo’smi", 8),
    ("p", "देवानामस्मि वासवः", "devānāmasmi vāsavaḥ", 8),
    ("p", "इन्द्रियाणां मनश्चास्मि", "indriyāṇāṃ manaścāsmi", 8),
    ("p", "भूतानामस्मि चेतना", "bhūtānāmasmi cetanā", 8),
],

"10.23": [
    ("p", "रुद्राणां शङ्करश्चास्मि", "rudrāṇāṃ śaṅkaraścāsmi", 8),
    ("p", "वित्तेशो यक्षरक्षसाम्", "vitteśo yakṣarakṣasām", 8),
    ("p", "वसूनां पावकश्चास्मि", "vasūnāṃ pāvakaścāsmi", 8),
    ("p", "मेरुः शिखरिणामहम्", "meruḥ śikhariṇāmaham", 8),
],

"10.24": [
    ("p", "पुरोधसां च मुख्यं मां", "purodhasāṃ ca mukhyaṃ māṃ", 8),
    ("p", "विद्धि पार्थ बृहस्पतिम्", "viddhi pārtha bṛhaspatim", 8),
    ("p", "सेनानीनामहं स्कन्दः", "senānīnāmahaṃ skandaḥ", 8),
    ("p", "सरसामस्मि सागरः", "sarasāmasmi sāgaraḥ", 8),
],

"10.25": [
    ("p", "महर्षीणां भृगुरहं", "maharṣīṇāṃ bhṛgurahaṃ", 8),
    ("p", "गिरामस्म्येकमक्षरम्", "girāmasmyekamakṣaram", 8),
    ("p", "यज्ञानां जपयज्ञोऽस्मि", "yajñānāṃ japayajño’smi", 8),
    ("p", "स्थावराणां हिमालयः", "sthāvarāṇāṃ himālayaḥ", 8),
],

"10.26": [
    ("p", "अश्वत्थः सर्ववृक्षाणां", "aśvatthaḥ sarvavṛkṣāṇāṃ", 8),
    ("p", "देवर्षीणां च नारदः", "devarṣīṇāṃ ca nāradaḥ", 8),
    ("p", "गन्धर्वाणां चित्ररथः", "gandharvāṇāṃ citrarathaḥ", 8),
    ("p", "सिद्धानां कपिलो मुनिः", "siddhānāṃ kapilo muniḥ", 8),
],

"10.27": [
    ("p", "उच्चैःश्रवसमश्वानां", "uccaiḥśravasamaśvānāṃ", 8),
    ("p", "विद्धि माममृतोद्भवम्", "viddhi māmamṛtodbhavam", 8),
    ("p", "ऐरावतं गजेन्द्राणां", "airāvataṃ gajendrāṇāṃ", 8),
    ("p", "नराणां च नराधिपम्", "narāṇāṃ ca narādhipam", 8),
],

"10.28": [
    ("p", "आयुधानामहं वज्रं", "āyudhānāmahaṃ vajraṃ", 8),
    ("p", "धेनूनामस्मि कामधुक्", "dhenūnāmasmi kāmadhuk", 8),
    ("p", "प्रजनश्चास्मि कन्दर्पः", "prajanaścāsmi kandarpaḥ", 8),
    ("p", "सर्पाणामस्मि वासुकिः", "sarpāṇāmasmi vāsukiḥ", 8),
],

"10.29": [
    ("p", "अनन्तश्चास्मि नागानां", "anantaścāsmi nāgānāṃ", 8),
    ("p", "वरुणो यादसामहम्", "varuṇo yādasāmaham", 8),
    ("p", "पितॄणामर्यमा चास्मि", "pitṝṇāmaryamā cāsmi", 8),
    ("p", "यमः संयमतामहम्", "yamaḥ saṃyamatāmaham", 8),
],

"10.30": [
    ("p", "प्रह्लादश्चास्मि दैत्यानां", "prahlādaścāsmi daityānāṃ", 8),
    ("p", "कालः कलयतामहम्", "kālaḥ kalayatāmaham", 8),
    ("p", "मृगाणां च मृगेन्द्रोऽहं", "mṛgāṇāṃ ca mṛgendro’haṃ", 8),
    ("p", "वैनतेयश्च पक्षिणाम्", "vainateyaśca pakṣiṇām", 8),
],

"10.31": [
    ("p", "पवनः पवतामस्मि", "pavanaḥ pavatāmasmi", 8),
    ("p", "रामः शस्त्रभृतामहम्", "rāmaḥ śastrabhṛtāmaham", 8),
    ("p", "झषाणां मकरश्चास्मि", "jhaṣāṇāṃ makaraścāsmi", 8),
    ("p", "स्रोतसामस्मि जाह्नवी", "srotasāmasmi jāhnavī", 8),
],

"10.32": [
    ("p", "सर्गाणामादिरन्तश्च", "sargāṇāmādirantaśca", 8),
    ("p", "मध्यं चैवाहमर्जुन", "madhyaṃ caivāhamarjuna", 8),
    ("p", "अध्यात्मविद्या विद्यानां", "adhyātmavidyā vidyānāṃ", 8),
    ("p", "वादः प्रवदतामहम्", "vādaḥ pravadatāmaham", 8),
],

"10.33": [
    ("p", "अक्षराणामकारोऽस्मि", "akṣarāṇāmakāro’smi", 8),
    ("p", "द्वन्द्वः सामासिकस्य च", "dvandvaḥ sāmāsikasya ca", 8),
    ("p", "अहमेवाक्षयः कालः", "ahamevākṣayaḥ kālaḥ", 8),
    ("p", "धाताहं विश्वतोमुखः", "dhātāhaṃ viśvatomukhaḥ", 8),
],

"10.34": [
    ("p", "मृत्युः सर्वहरश्चाहं", "mṛtyuḥ sarvaharaścāhaṃ", 8),
    ("p", "उद्भवश्च भविष्यताम्", "udbhavaśca bhaviṣyatām", 8),
    ("p", "कीर्तिः श्रीर्वाक्च नारीणां", "kīrtiḥ śrīrvākca nārīṇāṃ", 8),
    ("p", "स्मृतिर्मेधा धृतिः क्षमा", "smṛtirmedhā dhṛtiḥ kṣamā", 8),
],

"10.35": [
    ("p", "बृहत्साम तथा साम्नां", "bṛhatsāma tathā sāmnāṃ", 8),
    ("p", "गायत्री छन्दसामहम्", "gāyatrī chandasāmaham", 8),
    ("p", "मासानां मार्गशीर्षोऽहं", "māsānāṃ mārgaśīrṣo’haṃ", 8),
    ("p", "ऋतूनां कुसुमाकरः", "ṛtūnāṃ kusumākaraḥ", 8),
],

"10.36": [
    ("p", "द्यूतं छलयतामस्मि", "dyūtaṃ chalayatāmasmi", 8),
    ("p", "तेजस्तेजस्विनामहम्", "tejastejasvināmaham", 8),
    ("p", "जयोऽस्मि व्यवसायोऽस्मि", "jayo’smi vyavasāyo’smi", 8),
    ("p", "सत्त्वं सत्त्ववतामहम्", "sattvaṃ sattvavatāmaham", 8),
],

"10.37": [
    ("p", "वृष्णीनां वासुदेवोऽस्मि", "vṛṣṇīnāṃ vāsudevo’smi", 8),
    ("p", "पाण्डवानां धनञ्जयः", "pāṇḍavānāṃ dhanañjayaḥ", 8),
    ("p", "मुनीनामप्यहं व्यासः", "munīnāmapyahaṃ vyāsaḥ", 8),
    ("p", "कवीनामुशना कविः", "kavīnāmuśanā kaviḥ", 8),
],

"10.38": [
    ("p", "दण्डो दमयतामस्मि", "daṇḍo damayatāmasmi", 8),
    ("p", "नीतिरस्मि जिगीषताम्", "nītirasmi jigīṣatām", 8),
    ("p", "मौनं चैवास्मि गुह्यानां", "maunaṃ caivāsmi guhyānāṃ", 8),
    ("p", "ज्ञानं ज्ञानवतामहम्", "jñānaṃ jñānavatāmaham", 8),
],

"10.39": [
    ("p", "यच्चापि सर्वभूतानां", "yaccāpi sarvabhūtānāṃ", 8),
    ("p", "बीजं तदहमर्जुन", "bījaṃ tadahamarjuna", 8),
    ("p", "न तदस्ति विना यत्", "na tadasti vinā yat", 7),
    ("p", "स्यात् मया भूतं चराचरम्", "syāt mayā bhūtaṃ carācaram", 9),
],

"10.40": [
    ("p", "नान्तोऽस्ति मम दिव्यानां", "nānto’sti mama divyānāṃ", 8),
    ("p", "विभूतीनां परन्तप", "vibhūtīnāṃ parantapa", 8),
    ("p", "एष तूद्देशतः प्रोक्तः", "eṣa tūddeśataḥ proktaḥ", 8),
    ("p", "विभूतेर्विस्तरो मया", "vibhūtervistaro mayā", 8),
],

"10.41": [
    ("p", "यद्यद्विभूतिमत्सत्त्वं", "yadyadvibhūtimatsattvaṃ", 8),
    ("p", "श्रीमदूर्जितमेव वा", "śrīmadūrjitameva vā", 8),
    ("p", "तत्तदेवावगच्छ त्वं", "tattadevāvagaccha tvaṃ", 8),
    ("p", "मम तेजोंशसम्भवम्", "mama tejoṃśasambhavam", 8),
],

"10.42": [
    ("p", "अथवा बहुनैतेन", "athavā bahunaitena", 8),
    ("p", "किं ज्ञातेन तवार्जुन", "kiṃ jñātena tavārjuna", 8),
    ("p", "विष्टभ्याहमिदं कृत्स्नं", "viṣṭabhyāhamidaṃ kṛtsnaṃ", 8),
    ("p", "एकांशेन स्थितो जगत्", "ekāṃśena sthito jagat", 8),
],

}
