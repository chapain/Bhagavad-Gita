# -*- coding: utf-8 -*-
"""padas_ch11.py — the pāda (quarter) division of every verse in chapter 11.

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
printed verbatim from ch11.json.
"""

GITA_CH11_PADAS = {

"11.01": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "मदनुग्रहाय परमं", "madanugrahāya paramaṃ", 9),
    ("p", "गुह्यमध्यात्मसंज्ञितम्", "guhyamadhyātmasaṃjñitam", 8),
    ("p", "यत्त्वयोक्तं वचस्तेन", "yattvayoktaṃ vacastena", 8),
    ("p", "मोहोऽयं विगतो मम", "moho’yaṃ vigato mama", 8),
],

"11.02": [
    ("p", "भवाप्ययौ हि भूतानां", "bhavāpyayau hi bhūtānāṃ", 8),
    ("p", "श्रुतौ विस्तरशो मया", "śrutau vistaraśo mayā", 8),
    ("p", "त्वत्तः कमलपत्राक्ष", "tvattaḥ kamalapatrākṣa", 8),
    ("p", "माहात्म्यमपि चाव्ययम्", "māhātmyamapi cāvyayam", 8),
],

"11.03": [
    ("p", "एवमेतद्यथात्थ त्वम्", "evametadyathāttha tvam", 8),
    ("p", "आत्मानं परमेश्वर", "ātmānaṃ parameśvara", 8),
    ("p", "द्रष्टुमिच्छामि ते रूपम्", "draṣṭumicchāmi te rūpam", 8),
    ("p", "ऐश्वरं पुरुषोत्तम", "aiśvaraṃ puruṣottama", 8),
],

"11.04": [
    ("p", "मन्यसे यदि तच्छक्यं", "manyase yadi tacchakyaṃ", 8),
    ("p", "मया द्रष्टुमिति प्रभो", "mayā draṣṭumiti prabho", 8),
    ("p", "योगेश्वर ततो मे त्वं", "yogeśvara tato me tvaṃ", 8),
    ("p", "दर्शयात्मानमव्ययम्", "darśayātmānamavyayam", 8),
],

"11.05": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "पश्य मे पार्थ रूपाणि", "paśya me pārtha rūpāṇi", 8),
    ("p", "शतशोऽथ सहस्रशः", "śataśo’tha sahasraśaḥ", 8),
    ("p", "नानाविधानि दिव्यानि", "nānāvidhāni divyāni", 8),
    ("p", "नानावर्णाकृतीनि च", "nānāvarṇākṛtīni ca", 8),
],

"11.06": [
    ("p", "पश्यादित्यान्वसून्रुद्रान्", "paśyādityānvasūnrudrān", 8),
    ("p", "अश्विनौ मरुतस्तथा", "aśvinau marutastathā", 8),
    ("p", "बहून्यदृष्टपूर्वाणि", "bahūnyadṛṣṭapūrvāṇi", 8),
    ("p", "पश्याश्चर्याणि भारत", "paśyāścaryāṇi bhārata", 8),
],

"11.07": [
    ("p", "इहैकस्थं जगत्कृत्स्नं", "ihaikasthaṃ jagatkṛtsnaṃ", 8),
    ("p", "पश्याद्य सचराचरम्", "paśyādya sacarācaram", 8),
    ("p", "मम देहे गुडाकेश", "mama dehe guḍākeśa", 8),
    ("p", "यच्चान्यद्द्रष्टुमिच्छसि", "yaccānyaddraṣṭumicchasi", 8),
],

"11.08": [
    ("p", "न तु मां शक्यसे द्रष्टुम्", "na tu māṃ śakyase draṣṭum", 8),
    ("p", "अनेनैव स्वचक्षुषा", "anenaiva svacakṣuṣā", 8),
    ("p", "दिव्यं ददामि ते चक्षुः", "divyaṃ dadāmi te cakṣuḥ", 8),
    ("p", "पश्य मे योगमैश्वरम्", "paśya me yogamaiśvaram", 8),
],

"11.09": [
    ("s", "सञ्जय उवाच।", "sañjaya uvāca"),
    ("p", "एवमुक्त्वा ततो राजन्", "evamuktvā tato rājan", 8),
    ("p", "महायोगेश्वरो हरिः", "mahāyogeśvaro hariḥ", 8),
    ("p", "दर्शयामास पार्थाय", "darśayāmāsa pārthāya", 8),
    ("p", "परमं रूपमैश्वरम्", "paramaṃ rūpamaiśvaram", 8),
],

"11.10": [
    ("p", "अनेकवक्त्रनयनम्", "anekavaktranayanam", 8),
    ("p", "अनेकाद्भुतदर्शनम्", "anekādbhutadarśanam", 8),
    ("p", "अनेकदिव्याभरणं", "anekadivyābharaṇaṃ", 8),
    ("p", "दिव्यानेकोद्यतायुधम्", "divyānekodyatāyudham", 8),
],

"11.11": [
    ("p", "दिव्यमाल्याम्बरधरं", "divyamālyāmbaradharaṃ", 8),
    ("p", "दिव्यगन्धानुलेपनम्", "divyagandhānulepanam", 8),
    ("p", "सर्वाश्चर्यमयं देवम्", "sarvāścaryamayaṃ devam", 8),
    ("p", "अनन्तं विश्वतोमुखम्", "anantaṃ viśvatomukham", 8),
],

"11.12": [
    ("p", "दिवि सूर्यसहस्रस्य", "divi sūryasahasrasya", 8),
    ("p", "भवेद्युगपदुत्थिता", "bhavedyugapadutthitā", 8),
    ("p", "यदि भाः सदृशी सा स्याद्", "yadi bhāḥ sadṛśī sā syād", 8),
    ("p", "भासस्तस्य महात्मनः", "bhāsastasya mahātmanaḥ", 8),
],

"11.13": [
    ("p", "तत्रैकस्थं जगत्कृत्स्नं", "tatraikasthaṃ jagatkṛtsnaṃ", 8),
    ("p", "प्रविभक्तमनेकधा", "pravibhaktamanekadhā", 8),
    ("p", "अपश्यद्देवदेवस्य", "apaśyaddevadevasya", 8),
    ("p", "शरीरे पाण्डवस्तदा", "śarīre pāṇḍavastadā", 8),
],

"11.14": [
    ("p", "ततः स विस्मयाविष्टो", "tataḥ sa vismayāviṣṭo", 8),
    ("p", "हृष्टरोमा धनञ्जयः", "hṛṣṭaromā dhanañjayaḥ", 8),
    ("p", "प्रणम्य शिरसा देवं", "praṇamya śirasā devaṃ", 8),
    ("p", "कृताञ्जलिरभाषत", "kṛtāñjalirabhāṣata", 8),
],

"11.15": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "पश्यामि देवांस्तव देव देहे", "paśyāmi devāṃstava deva dehe", 11),
    ("p", "सर्वांस्तथा भूतविशेषसङ्घान्", "sarvāṃstathā bhūtaviśeṣasaṅghān", 11),
    ("p", "ब्रह्माणमीशं कमलासनस्थम्", "brahmāṇamīśaṃ kamalāsanastham", 11),
    ("p", "ऋषींश्च सर्वानुरगांश्च दिव्यान्", "ṛṣīṃśca sarvānuragāṃśca divyān", 11),
],

"11.16": [
    ("p", "अनेकबाहूदरवक्त्रनेत्रं", "anekabāhūdaravaktranetraṃ", 11),
    ("p", "पश्यामि त्वा सर्वतोऽनन्तरूपम्", "paśyāmi tvā sarvato’nantarūpam", 11),
    ("p", "नान्तं न मध्यं न पुनस्तवादिं", "nāntaṃ na madhyaṃ na punastavādiṃ", 11),
    ("p", "पश्यामि विश्वेश्वर विश्वरूप", "paśyāmi viśveśvara viśvarūpa", 11),
],

"11.17": [
    ("p", "किरीटिनं गदिनं चक्रिणं च", "kirīṭinaṃ gadinaṃ cakriṇaṃ ca", 11),
    ("p", "तेजोराशिं सर्वतोदीप्तिमन्तम्", "tejorāśiṃ sarvatodīptimantam", 11),
    ("p", "पश्यामि त्वां दुर्निरीक्ष्यं समन्ताद्", "paśyāmi tvāṃ durnirīkṣyaṃ samantād", 11),
    ("p", "दीप्तानलार्कद्युतिमप्रमेयम्", "dīptānalārkadyutimaprameyam", 11),
],

"11.18": [
    ("p", "त्वमक्षरं परमं वेदितव्यं", "tvamakṣaraṃ paramaṃ veditavyaṃ", 11),
    ("p", "त्वमस्य विश्वस्य परं निधानम्", "tvamasya viśvasya paraṃ nidhānam", 11),
    ("p", "त्वमव्ययः शाश्वतधर्मगोप्ता", "tvamavyayaḥ śāśvatadharmagoptā", 11),
    ("p", "सनातनस्त्वं पुरुषो मतो मे", "sanātanastvaṃ puruṣo mato me", 11),
],

"11.19": [
    ("p", "अनादिमध्यान्तमनन्तवीर्यम्", "anādimadhyāntamanantavīryam", 11),
    ("p", "अनन्तबाहुं शशिसूर्यनेत्रम्", "anantabāhuṃ śaśisūryanetram", 11),
    ("p", "पश्यामि त्वां दीप्तहुताशवक्त्रं", "paśyāmi tvāṃ dīptahutāśavaktraṃ", 11),
    ("p", "स्वतेजसा विश्वमिदं तपन्तम्", "svatejasā viśvamidaṃ tapantam", 11),
],

"11.20": [
    ("p", "द्यावापृथिव्योरिदमन्तरं हि", "dyāvāpṛthivyoridamantaraṃ hi", 11),
    ("p", "व्याप्तं त्वयैकेन दिशश्च सर्वाः", "vyāptaṃ tvayaikena diśaśca sarvāḥ", 11),
    ("p", "दृष्ट्वाद्भुतं रूपमिदं तवोग्रं", "dṛṣṭvādbhutaṃ rūpamidaṃ tavograṃ", 11),
    ("p", "लोकत्रयं प्रव्यथितं महात्मन्", "lokatrayaṃ pravyathitaṃ mahātman", 11),
],

"11.21": [
    ("p", "अमी हि त्वा सुरसङ्घा विशन्ति", "amī hi tvā surasaṅghā viśanti", 11),
    ("p", "केचिद्भीताः प्राञ्जलयो गृणन्ति", "kecidbhītāḥ prāñjalayo gṛṇanti", 11),
    ("p", "स्वस्तीत्युक्त्वा महर्षिसिद्धसङ्घाः", "svastītyuktvā maharṣisiddhasaṅghāḥ", 11),
    ("p", "स्तुवन्ति त्वां स्तुतिभिः पुष्कलाभिः", "stuvanti tvāṃ stutibhiḥ puṣkalābhiḥ", 11),
],

"11.22": [
    ("p", "रुद्रादित्या वसवो ये च साध्या", "rudrādityā vasavo ye ca sādhyā", 11),
    ("p", "विश्वेऽश्विनौ मरुतश्चोष्मपाश्च", "viśve’śvinau marutaścoṣmapāśca", 11),
    ("p", "गन्धर्वयक्षासुरसिद्धसङ्घा", "gandharvayakṣāsurasiddhasaṅghā", 11),
    ("p", "वीक्षन्ते त्वां विस्मिताश्चैव सर्वे", "vīkṣante tvāṃ vismitāścaiva sarve", 11),
],

"11.23": [
    ("p", "रूपं महत्ते बहुवक्त्रनेत्रं", "rūpaṃ mahatte bahuvaktranetraṃ", 11),
    ("p", "महाबाहो बहुबाहूरुपादम्", "mahābāho bahubāhūrupādam", 11),
    ("p", "बहूदरं बहुदंष्ट्राकरालं", "bahūdaraṃ bahudaṃṣṭrākarālaṃ", 11),
    ("p", "दृष्ट्वा लोकाः प्रव्यथितास्तथाहम्", "dṛṣṭvā lokāḥ pravyathitāstathāham", 11),
],

"11.24": [
    ("p", "नभःस्पृशं दीप्तमनेकवर्णं", "nabhaḥspṛśaṃ dīptamanekavarṇaṃ", 11),
    ("p", "व्यात्ताननं दीप्तविशालनेत्रम्", "vyāttānanaṃ dīptaviśālanetram", 11),
    ("p", "दृष्ट्वा हि त्वां प्रव्यथितान्तरात्मा", "dṛṣṭvā hi tvāṃ pravyathitāntarātmā", 11),
    ("p", "धृतिं न विन्दामि शमं च विष्णो", "dhṛtiṃ na vindāmi śamaṃ ca viṣṇo", 11),
],

"11.25": [
    ("p", "दंष्ट्राकरालानि च ते मुखानि", "daṃṣṭrākarālāni ca te mukhāni", 11),
    ("p", "दृष्ट्वैव कालानलसन्निभानि", "dṛṣṭvaiva kālānalasannibhāni", 11),
    ("p", "दिशो न जाने न लभे च शर्म", "diśo na jāne na labhe ca śarma", 11),
    ("p", "प्रसीद देवेश जगन्निवास", "prasīda deveśa jagannivāsa", 11),
],

"11.26": [
    ("p", "अमी च त्वां धृतराष्ट्रस्य पुत्राः", "amī ca tvāṃ dhṛtarāṣṭrasya putrāḥ", 11),
    ("p", "सर्वे सहैवावनिपालसङ्घैः", "sarve sahaivāvanipālasaṅghaiḥ", 11),
    ("p", "भीष्मो द्रोणः सूतपुत्रस्तथासौ", "bhīṣmo droṇaḥ sūtaputrastathāsau", 11),
    ("p", "सहास्मदीयैरपि योधमुख्यैः", "sahāsmadīyairapi yodhamukhyaiḥ", 11),
],

"11.27": [
    ("p", "वक्त्राणि ते त्वरमाणा विशन्ति", "vaktrāṇi te tvaramāṇā viśanti", 11),
    ("p", "दंष्ट्राकरालानि भयानकानि", "daṃṣṭrākarālāni bhayānakāni", 11),
    ("p", "केचिद्विलग्ना दशनान्तरेषु", "kecidvilagnā daśanāntareṣu", 11),
    ("p", "सन्दृश्यन्ते चूर्णितैरुत्तमाङ्गैः", "sandṛśyante cūrṇitairuttamāṅgaiḥ", 11),
],

"11.28": [
    ("p", "यथा नदीनां बहवोऽम्बुवेगाः", "yathā nadīnāṃ bahavo’mbuvegāḥ", 11),
    ("p", "समुद्रमेवाभिमुखा द्रवन्ति", "samudramevābhimukhā dravanti", 11),
    ("p", "तथा तवामी नरलोकवीरा", "tathā tavāmī naralokavīrā", 11),
    ("p", "विशन्ति वक्त्राण्यभिविज्वलन्ति", "viśanti vaktrāṇyabhivijvalanti", 11),
],

"11.29": [
    ("p", "यथा प्रदीप्तं ज्वलनं पतङ्गा", "yathā pradīptaṃ jvalanaṃ pataṅgā", 11),
    ("p", "विशन्ति नाशाय समृद्धवेगाः", "viśanti nāśāya samṛddhavegāḥ", 11),
    ("p", "तथैव नाशाय विशन्ति लोकास्", "tathaiva nāśāya viśanti lokās", 11),
    ("p", "तवापि वक्त्राणि समृद्धवेगाः", "tavāpi vaktrāṇi samṛddhavegāḥ", 11),
],

"11.30": [
    ("p", "लेलिह्यसे ग्रसमानः समन्ताल्", "lelihyase grasamānaḥ samantāl", 11),
    ("p", "लोकान्समग्रान्वदनैर्ज्वलद्भिः", "lokānsamagrānvadanairjvaladbhiḥ", 11),
    ("p", "तेजोभिरापूर्य जगत्समग्रं", "tejobhirāpūrya jagatsamagraṃ", 11),
    ("p", "भासस्तवोग्राः प्रतपन्ति विष्णो", "bhāsastavogrāḥ pratapanti viṣṇo", 11),
],

"11.31": [
    ("p", "आख्याहि मे को भवानुग्ररूपो", "ākhyāhi me ko bhavānugrarūpo", 11),
    ("p", "नमोऽस्तु ते देववर प्रसीद", "namo’stu te devavara prasīda", 11),
    ("p", "विज्ञातुमिच्छामि भवन्तमाद्यं", "vijñātumicchāmi bhavantamādyaṃ", 11),
    ("p", "न हि प्रजानामि तव प्रवृत्तिम्", "na hi prajānāmi tava pravṛttim", 11),
],

"11.32": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "कालोऽस्मि लोकक्षयकृत्प्रवृद्धो", "kālo’smi lokakṣayakṛtpravṛddho", 11),
    ("p", "लोकान्समाहर्तुमिह प्रवृत्तः", "lokānsamāhartumiha pravṛttaḥ", 11),
    ("p", "ऋतेऽपि त्वा न भविष्यन्ति सर्वे", "ṛte’pi tvā na bhaviṣyanti sarve", 11),
    ("p", "येऽवस्थिताः प्रत्यनीकेषु योधाः", "ye’vasthitāḥ pratyanīkeṣu yodhāḥ", 11),
],

"11.33": [
    ("p", "तस्मात्त्वमुत्तिष्ठ यशो लभस्व", "tasmāttvamuttiṣṭha yaśo labhasva", 11),
    ("p", "जित्वा शत्रून्भुङ्क्ष्व राज्यं समृद्धम्", "jitvā śatrūnbhuṅkṣva rājyaṃ samṛddham", 11),
    ("p", "मयैवैते निहताः पूर्वमेव", "mayaivaite nihatāḥ pūrvameva", 11),
    ("p", "निमित्तमात्रं भव सव्यसाचिन्", "nimittamātraṃ bhava savyasācin", 11),
],

"11.34": [
    ("p", "द्रोणं च भीष्मं च जयद्रथं च", "droṇaṃ ca bhīṣmaṃ ca jayadrathaṃ ca", 11),
    ("p", "कर्णं तथान्यानपि योधवीरान्", "karṇaṃ tathānyānapi yodhavīrān", 11),
    ("p", "मया हतांस्त्वं जहि मा व्यथिष्ठा", "mayā hatāṃstvaṃ jahi mā vyathiṣṭhā", 11),
    ("p", "युध्यस्व जेतासि रणे सपत्नान्", "yudhyasva jetāsi raṇe sapatnān", 11),
],

"11.35": [
    ("s", "सञ्जय उवाच।", "sañjaya uvāca"),
    ("p", "एतच्छ्रुत्वा वचनं केशवस्य", "etacchrutvā vacanaṃ keśavasya", 11),
    ("p", "कृताञ्जलिर्वेपमानः किरीटी", "kṛtāñjalirvepamānaḥ kirīṭī", 11),
    ("p", "नमस्कृत्वा भूय एवाह कृष्णं", "namaskṛtvā bhūya evāha kṛṣṇaṃ", 11),
    ("p", "सगद्गदं भीतभीतः प्रणम्य", "sagadgadaṃ bhītabhītaḥ praṇamya", 11),
],

"11.36": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "स्थाने हृषीकेश तव प्रकीर्त्या", "sthāne hṛṣīkeśa tava prakīrtyā", 11),
    ("p", "जगत्प्रहृष्यत्यनुरज्यते च", "jagatprahṛṣyatyanurajyate ca", 11),
    ("p", "रक्षांसि भीतानि दिशो द्रवन्ति", "rakṣāṃsi bhītāni diśo dravanti", 11),
    ("p", "सर्वे नमस्यन्ति च सिद्धसङ्घाः", "sarve namasyanti ca siddhasaṅghāḥ", 11),
],

"11.37": [
    ("p", "कस्माच्च ते न नमेरन्महात्मन्", "kasmācca te na nameranmahātman", 11),
    ("p", "गरीयसे ब्रह्मणोऽप्यादिकर्त्रे", "garīyase brahmaṇo’pyādikartre", 11),
    ("p", "अनन्त देवेश जगन्निवास", "ananta deveśa jagannivāsa", 11),
    ("p", "त्वमक्षरं सदसत्तत्परं यत्", "tvamakṣaraṃ sadasattatparaṃ yat", 11),
],

"11.38": [
    ("p", "त्वमादिदेवः पुरुषः पुराणस्", "tvamādidevaḥ puruṣaḥ purāṇas", 11),
    ("p", "त्वमस्य विश्वस्य परं निधानम्", "tvamasya viśvasya paraṃ nidhānam", 11),
    ("p", "वेत्तासि वेद्यं च परं च धाम", "vettāsi vedyaṃ ca paraṃ ca dhāma", 11),
    ("p", "त्वया ततं विश्वमनन्तरूप", "tvayā tataṃ viśvamanantarūpa", 11),
],

"11.39": [
    ("p", "वायुर्यमोऽग्निर्वरुणः शशाङ्कः", "vāyuryamo’gnirvaruṇaḥ śaśāṅkaḥ", 11),
    ("p", "प्रजापतिस्त्वं प्रपितामहश्च", "prajāpatistvaṃ prapitāmahaśca", 11),
    ("p", "नमो नमस्तेऽस्तु सहस्रकृत्वः", "namo namaste’stu sahasrakṛtvaḥ", 11),
    ("p", "पुनश्च भूयोऽपि नमो नमस्ते", "punaśca bhūyo’pi namo namaste", 11),
],

"11.40": [
    ("p", "नमः पुरस्तादथ पृष्ठतस्ते", "namaḥ purastādatha pṛṣṭhataste", 11),
    ("p", "नमोऽस्तु ते सर्वत एव सर्व", "namo’stu te sarvata eva sarva", 11),
    ("p", "अनन्तवीर्यामितविक्रमस्त्वं", "anantavīryāmitavikramastvaṃ", 11),
    ("p", "सर्वं समाप्नोषि ततोऽसि सर्वः", "sarvaṃ samāpnoṣi tato’si sarvaḥ", 11),
],

"11.41": [
    ("p", "सखेति मत्वा प्रसभं यदुक्तं", "sakheti matvā prasabhaṃ yaduktaṃ", 11),
    ("p", "हे कृष्ण हे यादव हे सखेति", "he kṛṣṇa he yādava he sakheti", 11),
    ("p", "अजानता महिमानं तवेदं", "ajānatā mahimānaṃ tavedaṃ", 11),
    ("p", "मया प्रमादात्प्रणयेन वापि", "mayā pramādātpraṇayena vāpi", 11),
],

"11.42": [
    ("p", "यच्चावहासार्थमसत्कृतोऽसि", "yaccāvahāsārthamasatkṛto’si", 11),
    ("p", "विहारशय्यासनभोजनेषु", "vihāraśayyāsanabhojaneṣu", 11),
    ("p", "एकोऽथवाप्यच्युत तत्समक्षं", "eko’thavāpyacyuta tatsamakṣaṃ", 11),
    ("p", "तत्क्षामये त्वामहमप्रमेयम्", "tatkṣāmaye tvāmahamaprameyam", 11),
],

"11.43": [
    ("p", "पितासि लोकस्य चराचरस्य", "pitāsi lokasya carācarasya", 11),
    ("p", "त्वमस्य पूज्यश्च गुरुर्गरीयान्", "tvamasya pūjyaśca gururgarīyān", 11),
    ("p", "न त्वत्समोऽस्त्यभ्यधिकः कुतोऽन्यो", "na tvatsamo’styabhyadhikaḥ kuto’nyo", 11),
    ("p", "लोकत्रयेऽप्यप्रतिमप्रभाव", "lokatraye’pyapratimaprabhāva", 11),
],

"11.44": [
    ("p", "तस्मात्प्रणम्य प्रणिधाय कायं", "tasmātpraṇamya praṇidhāya kāyaṃ", 11),
    ("p", "प्रसादये त्वामहमीशमीड्यम्", "prasādaye tvāmahamīśamīḍyam", 11),
    ("p", "पितेव पुत्रस्य सखेव सख्युः", "piteva putrasya sakheva sakhyuḥ", 11),
    ("p", "प्रियः प्रियायार्हसि देव सोढुम्", "priyaḥ priyāyārhasi deva soḍhum", 11),
],

"11.45": [
    ("p", "अदृष्टपूर्वं हृषितोऽस्मि दृष्ट्वा", "adṛṣṭapūrvaṃ hṛṣito’smi dṛṣṭvā", 11),
    ("p", "भयेन च प्रव्यथितं मनो मे", "bhayena ca pravyathitaṃ mano me", 11),
    ("p", "तदेव मे दर्शय देव रूपं", "tadeva me darśaya deva rūpaṃ", 11),
    ("p", "प्रसीद देवेश जगन्निवास", "prasīda deveśa jagannivāsa", 11),
],

"11.46": [
    ("p", "किरीटिनं गदिनं चक्रहस्तम्", "kirīṭinaṃ gadinaṃ cakrahastam", 11),
    ("p", "इच्छामि त्वां द्रष्टुमहं तथैव", "icchāmi tvāṃ draṣṭumahaṃ tathaiva", 11),
    ("p", "तेनैव रूपेण चतुर्भुजेन", "tenaiva rūpeṇa caturbhujena", 11),
    ("p", "सहस्रबाहो भव विश्वमूर्ते", "sahasrabāho bhava viśvamūrte", 11),
],

"11.47": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "मया प्रसन्नेन तवार्जुनेदं", "mayā prasannena tavārjunedaṃ", 11),
    ("p", "रूपं परं दर्शितमात्मयोगात्", "rūpaṃ paraṃ darśitamātmayogāt", 11),
    ("p", "तेजोमयं विश्वमनन्तमाद्यं", "tejomayaṃ viśvamanantamādyaṃ", 11),
    ("p", "यन्मे त्वदन्येन न दृष्टपूर्वम्", "yanme tvadanyena na dṛṣṭapūrvam", 11),
],

"11.48": [
    ("p", "न वेदयज्ञाध्ययनैर्न दानैर्", "na vedayajñādhyayanairna dānair", 11),
    ("p", "न च क्रियाभिर्न तपोभिरुग्रैः", "na ca kriyābhirna tapobhirugraiḥ", 11),
    ("p", "एवंरूपः शक्य अहं नृलोके", "evaṃrūpaḥ śakya ahaṃ nṛloke", 11),
    ("p", "द्रष्टुं त्वदन्येन कुरुप्रवीर", "draṣṭuṃ tvadanyena kurupravīra", 11),
],

"11.49": [
    ("p", "मा ते व्यथा मा च विमूढभावो", "mā te vyathā mā ca vimūḍhabhāvo", 11),
    ("p", "दृष्ट्वा रूपं घोरमीदृङ्ममेदम्", "dṛṣṭvā rūpaṃ ghoramīdṛṅmamedam", 11),
    ("p", "व्यपेतभीः प्रीतमनाः पुनस्त्वं", "vyapetabhīḥ prītamanāḥ punastvaṃ", 11),
    ("p", "तदेव मे रूपमिदं प्रपश्य", "tadeva me rūpamidaṃ prapaśya", 11),
],

"11.50": [
    ("s", "सञ्जय उवाच।", "sañjaya uvāca"),
    ("p", "इत्यर्जुनं वासुदेवस्तथोक्त्वा", "ityarjunaṃ vāsudevastathoktvā", 11),
    ("p", "स्वकं रूपं दर्शयामास भूयः", "svakaṃ rūpaṃ darśayāmāsa bhūyaḥ", 11),
    ("p", "आश्वासयामास च भीतमेनं", "āśvāsayāmāsa ca bhītamenaṃ", 11),
    ("p", "भूत्वा पुनःसौम्यवपुर्महात्मा", "bhūtvā punaḥsaumyavapurmahātmā", 11),
],

"11.51": [
    ("s", "अर्जुन उवाच।", "arjuna uvāca"),
    ("p", "दृष्ट्वेदं मानुषं रूपं", "dṛṣṭvedaṃ mānuṣaṃ rūpaṃ", 8),
    ("p", "तव सौम्यं जनार्दन", "tava saumyaṃ janārdana", 8),
    ("p", "इदानीमस्मि संवृत्तः", "idānīmasmi saṃvṛttaḥ", 8),
    ("p", "सचेताः प्रकृतिं गतः", "sacetāḥ prakṛtiṃ gataḥ", 8),
],

"11.52": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "सुदुर्दर्शमिदं रूपं", "sudurdarśamidaṃ rūpaṃ", 8),
    ("p", "दृष्टवानसि यन्मम", "dṛṣṭavānasi yanmama", 8),
    ("p", "देवा अप्यस्य रूपस्य", "devā apyasya rūpasya", 8),
    ("p", "नित्यं दर्शनकाङ्क्षिणः", "nityaṃ darśanakāṅkṣiṇaḥ", 8),
],

"11.53": [
    ("p", "नाहं वेदैर्न तपसा", "nāhaṃ vedairna tapasā", 8),
    ("p", "न दानेन न चेज्यया", "na dānena na cejyayā", 8),
    ("p", "शक्य एवंविधो द्रष्टुं", "śakya evaṃvidho draṣṭuṃ", 8),
    ("p", "दृष्टवानसि मां यथा", "dṛṣṭavānasi māṃ yathā", 8),
],

"11.54": [
    ("p", "भक्त्या त्वनन्यया शक्य", "bhaktyā tvananyayā śakya", 8),
    ("p", "अहमेवंविधोऽर्जुन", "ahamevaṃvidho’rjuna", 8),
    ("p", "ज्ञातुं द्रष्टुं च तत्त्वेन", "jñātuṃ draṣṭuṃ ca tattvena", 8),
    ("p", "प्रवेष्टुं च परन्तप", "praveṣṭuṃ ca parantapa", 8),
],

"11.55": [
    ("p", "मत्कर्मकृन्मत्परमो", "matkarmakṛnmatparamo", 8),
    ("p", "मद्भक्तः सङ्गवर्जितः", "madbhaktaḥ saṅgavarjitaḥ", 8),
    ("p", "निर्वैरः सर्वभूतेषु", "nirvairaḥ sarvabhūteṣu", 8),
    ("p", "यः स मामेति पाण्डव", "yaḥ sa māmeti pāṇḍava", 8),
],

}
