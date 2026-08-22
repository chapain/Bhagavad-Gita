# -*- coding: utf-8 -*-
"""padas_ch9.py — the pāda (quarter) division of every verse in chapter 9.

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
printed verbatim from ch9.json.
"""

GITA_CH9_PADAS = {
"9.01": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "इदं तु ते गुह्यतमं", "idaṃ tu te guhyatamaṃ", 8),
    ("p", "प्रवक्ष्याम्यनसूयवे", "pravakṣyāmyanasūyave", 8),
    ("p", "ज्ञानं विज्ञानसहितं", "jñānaṃ vijñānasahitaṃ", 8),
    ("p", "यज्ज्ञात्वा मोक्ष्यसेऽशुभात्", "yajjñātvā mokṣyase’śubhāt", 8),
],

"9.02": [
    ("p", "राजविद्या राजगुह्यं", "rājavidyā rājaguhyaṃ", 8),
    ("p", "पवित्रमिदमुत्तमम्", "pavitramidamuttamam", 8),
    ("p", "प्रत्यक्षावगमं धर्म्यं", "pratyakṣāvagamaṃ dharmyaṃ", 8),
    ("p", "सुसुखं कर्तुमव्ययम्", "susukhaṃ kartumavyayam", 8),
],

"9.03": [
    ("p", "अश्रद्दधानाः पुरुषा", "aśraddadhānāḥ puruṣā", 8),
    ("p", "धर्मस्यास्य परन्तप", "dharmasyāsya parantapa", 8),
    ("p", "अप्राप्य मां निवर्तन्ते", "aprāpya māṃ nivartante", 8),
    ("p", "मृत्युसंसारवर्त्मनि", "mṛtyusaṃsāravartmani", 8),
],

"9.04": [
    ("p", "मया ततमिदं सर्वं", "mayā tatamidaṃ sarvaṃ", 8),
    ("p", "जगदव्यक्तमूर्तिना", "jagadavyaktamūrtinā", 8),
    ("p", "मत्स्थानि सर्वभूतानि", "matsthāni sarvabhūtāni", 8),
    ("p", "न चाहं तेष्ववस्थितः", "na cāhaṃ teṣvavasthitaḥ", 8),
],

"9.05": [
    ("p", "न च मत्स्थानि भूतानि", "na ca matsthāni bhūtāni", 8),
    ("p", "पश्य मे योगमैश्वरम्", "paśya me yogamaiśvaram", 8),
    ("p", "भूतभृन्न च भूतस्थो", "bhūtabhṛnna ca bhūtastho", 8),
    ("p", "ममात्मा भूतभावनः", "mamātmā bhūtabhāvanaḥ", 8),
],

"9.06": [
    ("p", "यथाकाशस्थितो नित्यं", "yathākāśasthito nityaṃ", 8),
    ("p", "वायुः सर्वत्रगो महान्", "vāyuḥ sarvatrago mahān", 8),
    ("p", "तथा सर्वाणि भूतानि", "tathā sarvāṇi bhūtāni", 8),
    ("p", "मत्स्थानीत्युपधारय", "matsthānītyupadhāraya", 8),
],

"9.07": [
    ("p", "सर्वभूतानि कौन्तेय", "sarvabhūtāni kaunteya", 8),
    ("p", "प्रकृतिं यान्ति मामिकाम्", "prakṛtiṃ yānti māmikām", 8),
    ("p", "कल्पक्षये पुनस्तानि", "kalpakṣaye punastāni", 8),
    ("p", "कल्पादौ विसृजाम्यहम्", "kalpādau visṛjāmyaham", 8),
],

"9.08": [
    ("p", "प्रकृतिं स्वामवष्टभ्य", "prakṛtiṃ svāmavaṣṭabhya", 8),
    ("p", "विसृजामि पुनः पुनः", "visṛjāmi punaḥ punaḥ", 8),
    ("p", "भूतग्राममिमं कृत्स्नम्", "bhūtagrāmamimaṃ kṛtsnam", 8),
    ("p", "अवशं प्रकृतेर्वशात्", "avaśaṃ prakṛtervaśāt", 8),
],

"9.09": [
    ("p", "न च मां तानि कर्माणि", "na ca māṃ tāni karmāṇi", 8),
    ("p", "निबध्नन्ति धनञ्जय", "nibadhnanti dhanañjaya", 8),
    ("p", "उदासीनवदासीनम्", "udāsīnavadāsīnam", 8),
    ("p", "असक्तं तेषु कर्मसु", "asaktaṃ teṣu karmasu", 8),
],

"9.10": [
    ("p", "मयाध्यक्षेण प्रकृतिः", "mayādhyakṣeṇa prakṛtiḥ", 8),
    ("p", "सूयते सचराचरम्", "sūyate sacarācaram", 8),
    ("p", "हेतुनानेन कौन्तेय", "hetunānena kaunteya", 8),
    ("p", "जगद्विपरिवर्तते", "jagadviparivartate", 8),
],

"9.11": [
    ("p", "अवजानन्ति मां मूढा", "avajānanti māṃ mūḍhā", 8),
    ("p", "मानुषीं तनुमाश्रितम्", "mānuṣīṃ tanumāśritam", 8),
    ("p", "परं भावमजानन्तो", "paraṃ bhāvamajānanto", 8),
    ("p", "मम भूतमहेश्वरम्", "mama bhūtamaheśvaram", 8),
],

"9.12": [
    ("p", "मोघाशा मोघकर्माणो", "moghāśā moghakarmāṇo", 8),
    ("p", "मोघज्ञाना विचेतसः", "moghajñānā vicetasaḥ", 8),
    ("p", "राक्षसीमासुरीं चैव", "rākṣasīmāsurīṃ caiva", 8),
    ("p", "प्रकृतिं मोहिनीं श्रिताः", "prakṛtiṃ mohinīṃ śritāḥ", 8),
],

"9.13": [
    ("p", "महात्मनस्तु मां पार्थ", "mahātmanastu māṃ pārtha", 8),
    ("p", "दैवीं प्रकृतिमाश्रिताः", "daivīṃ prakṛtimāśritāḥ", 8),
    ("p", "भजन्त्यनन्यमनसो", "bhajantyananyamanaso", 8),
    ("p", "ज्ञात्वा भूतादिमव्ययम्", "jñātvā bhūtādimavyayam", 8),
],

"9.14": [
    ("p", "सततं कीर्तयन्तो मां", "satataṃ kīrtayanto māṃ", 8),
    ("p", "यतन्तश्च दृढव्रताः", "yatantaśca dṛḍhavratāḥ", 8),
    ("p", "नमस्यन्तश्च मां भक्त्या", "namasyantaśca māṃ bhaktyā", 8),
    ("p", "नित्ययुक्ता उपासते", "nityayuktā upāsate", 8),
],

"9.15": [
    ("p", "ज्ञानयज्ञेन चाप्यन्ये", "jñānayajñena cāpyanye", 8),
    ("p", "यजन्तो मामुपासते", "yajanto māmupāsate", 8),
    ("p", "एकत्वेन पृथक्त्वेन", "ekatvena pṛthaktvena", 8),
    ("p", "बहुधा विश्वतोमुखम्", "bahudhā viśvatomukham", 8),
],

"9.16": [
    ("p", "अहं क्रतुरहं यज्ञः", "ahaṃ kraturahaṃ yajñaḥ", 8),
    ("p", "स्वधाहमहमौषधम्", "svadhāhamahamauṣadham", 8),
    ("p", "मन्त्रोऽहमहमेवाज्यम्", "mantro’hamahamevājyam", 8),
    ("p", "अहमग्निरहं हुतम्", "ahamagnirahaṃ hutam", 8),
],

"9.17": [
    ("p", "पिताहमस्य जगतो", "pitāhamasya jagato", 8),
    ("p", "माता धाता पितामहः", "mātā dhātā pitāmahaḥ", 8),
    ("p", "वेद्यं पवित्रमोङ्कार", "vedyaṃ pavitramoṅkāra", 8),
    ("p", "ऋक्साम यजुरेव च", "ṛksāma yajureva ca", 8),
],

"9.18": [
    ("p", "गतिर्भर्ता प्रभुः साक्षी", "gatirbhartā prabhuḥ sākṣī", 8),
    ("p", "निवासः शरणं सुहृत्", "nivāsaḥ śaraṇaṃ suhṛt", 8),
    ("p", "प्रभवः प्रलयः स्थानं", "prabhavaḥ pralayaḥ sthānaṃ", 8),
    ("p", "निधानं बीजमव्ययम्", "nidhānaṃ bījamavyayam", 8),
],

"9.19": [
    ("p", "तपाम्यहमहं वर्षं", "tapāmyahamahaṃ varṣaṃ", 8),
    ("p", "निगृह्णाम्युत्सृजामि च", "nigṛhṇāmyutsṛjāmi ca", 8),
    ("p", "अमृतं चैव मृत्युश्च", "amṛtaṃ caiva mṛtyuśca", 8),
    ("p", "सदसच्चाहमर्जुन", "sadasaccāhamarjuna", 8),
],

"9.20": [
    ("p", "त्रैविद्या मां सोमपाः पूतपापा", "traividyā māṃ somapāḥ pūtapāpā", 11),
    ("p", "यज्ञैरिष्ट्वा स्वर्गतिं प्रार्थयन्ते", "yajñairiṣṭvā svargatiṃ prārthayante", 11),
    ("p", "ते पुण्यमासाद्य सुरेन्द्रलोकम्", "te puṇyamāsādya surendralokam", 11),
    ("p", "अश्नन्ति दिव्यान्दिवि देवभोगान्", "aśnanti divyāndivi devabhogān", 11),
],

"9.21": [
    ("p", "ते तं भुक्त्वा स्वर्गलोकं विशालं", "te taṃ bhuktvā svargalokaṃ viśālaṃ", 11),
    ("p", "क्षीणे पुण्ये मर्त्यलोकं विशन्ति", "kṣīṇe puṇye martyalokaṃ viśanti", 11),
    ("p", "एवं त्रयीधर्ममनुप्रपन्ना", "evaṃ trayīdharmamanuprapannā", 11),
    ("p", "गतागतं कामकामा लभन्ते", "gatāgataṃ kāmakāmā labhante", 11),
],

"9.22": [
    ("p", "अनन्याश्चिन्तयन्तो मां", "ananyāścintayanto māṃ", 8),
    ("p", "ये जनाः पर्युपासते", "ye janāḥ paryupāsate", 8),
    ("p", "तेषां नित्याभियुक्तानां", "teṣāṃ nityābhiyuktānāṃ", 8),
    ("p", "योगक्षेमं वहाम्यहम्", "yogakṣemaṃ vahāmyaham", 8),
],

"9.23": [
    ("p", "येऽप्यन्यदेवताभक्ता", "ye’pyanyadevatābhaktā", 8),
    ("p", "यजन्ते श्रद्धयान्विताः", "yajante śraddhayānvitāḥ", 8),
    ("p", "तेऽपि मामेव कौन्तेय", "te’pi māmeva kaunteya", 8),
    ("p", "यजन्त्यविधिपूर्वकम्", "yajantyavidhipūrvakam", 8),
],

"9.24": [
    ("p", "अहं हि सर्वयज्ञानां", "ahaṃ hi sarvayajñānāṃ", 8),
    ("p", "भोक्ता च प्रभुरेव च", "bhoktā ca prabhureva ca", 8),
    ("p", "न तु मामभिजानन्ति", "na tu māmabhijānanti", 8),
    ("p", "तत्त्वेनातश्च्यवन्ति ते", "tattvenātaścyavanti te", 8),
],

"9.25": [
    ("p", "यान्ति देवव्रता देवान्", "yānti devavratā devān", 8),
    ("p", "पितॄन्यान्ति पितृव्रताः", "pitṝnyānti pitṛvratāḥ", 8),
    ("p", "भूतानि यान्ति भूतेज्या", "bhūtāni yānti bhūtejyā", 8),
    ("p", "यान्ति मद्याजिनोऽपि माम्", "yānti madyājino’pi mām", 8),
],

"9.26": [
    ("p", "पत्रं पुष्पं फलं तोयं", "patraṃ puṣpaṃ phalaṃ toyaṃ", 8),
    ("p", "यो मे भक्त्या प्रयच्छति", "yo me bhaktyā prayacchati", 8),
    ("p", "तदहं भक्त्युपहृतम्", "tadahaṃ bhaktyupahṛtam", 8),
    ("p", "अश्नामि प्रयतात्मनः", "aśnāmi prayatātmanaḥ", 8),
],

"9.27": [
    ("p", "यत्करोषि यदश्नासि", "yatkaroṣi yadaśnāsi", 8),
    ("p", "यज्जुहोषि ददासि यत्", "yajjuhoṣi dadāsi yat", 8),
    ("p", "यत्तपस्यसि कौन्तेय", "yattapasyasi kaunteya", 8),
    ("p", "तत्कुरुष्व मदर्पणम्", "tatkuruṣva madarpaṇam", 8),
],

"9.28": [
    ("p", "शुभाशुभफलैरेवं", "śubhāśubhaphalairevaṃ", 8),
    ("p", "मोक्ष्यसे कर्मबन्धनैः", "mokṣyase karmabandhanaiḥ", 8),
    ("p", "सन्न्यासयोगयुक्तात्मा", "sannyāsayogayuktātmā", 8),
    ("p", "विमुक्तो मामुपैष्यसि", "vimukto māmupaiṣyasi", 8),
],

"9.29": [
    ("p", "समोऽहं सर्वभूतेषु", "samo’haṃ sarvabhūteṣu", 8),
    ("p", "न मे द्वेष्योऽस्ति न प्रियः", "na me dveṣyo’sti na priyaḥ", 8),
    ("p", "ये भजन्ति तु मां भक्त्या", "ye bhajanti tu māṃ bhaktyā", 8),
    ("p", "मयि ते तेषु चाप्यहम्", "mayi te teṣu cāpyaham", 8),
],

"9.30": [
    ("p", "अपि चेत्सुदुराचारो", "api cetsudurācāro", 8),
    ("p", "भजते मामनन्यभाक्", "bhajate māmananyabhāk", 8),
    ("p", "साधुरेव स मन्तव्यः", "sādhureva sa mantavyaḥ", 8),
    ("p", "सम्यग्व्यवसितो हि सः", "samyagvyavasito hi saḥ", 8),
],

"9.31": [
    ("p", "क्षिप्रं भवति धर्मात्मा", "kṣipraṃ bhavati dharmātmā", 8),
    ("p", "शश्वच्छान्तिं निगच्छति", "śaśvacchāntiṃ nigacchati", 8),
    ("p", "कौन्तेय प्रतिजानीहि", "kaunteya pratijānīhi", 8),
    ("p", "न मे भक्तः प्रणश्यति", "na me bhaktaḥ praṇaśyati", 8),
],

"9.32": [
    ("p", "मां हि पार्थ व्यपाश्रित्य", "māṃ hi pārtha vyapāśritya", 8),
    ("p", "येऽपि स्युः पापयोनयः", "ye’pi syuḥ pāpayonayaḥ", 8),
    ("p", "स्त्रियो वैश्यास्तथा शूद्रास्", "striyo vaiśyāstathā śūdrās", 8),
    ("p", "तेऽपि यान्ति परां गतिम्", "te’pi yānti parāṃ gatim", 8),
],

"9.33": [
    ("p", "किं पुनर्ब्राह्मणाः पुण्या", "kiṃ punarbrāhmaṇāḥ puṇyā", 8),
    ("p", "भक्ता राजर्षयस्तथा", "bhaktā rājarṣayastathā", 8),
    ("p", "अनित्यमसुखं लोकम्", "anityamasukhaṃ lokam", 8),
    ("p", "इमं प्राप्य भजस्व माम्", "imaṃ prāpya bhajasva mām", 8),
],

"9.34": [
    ("p", "मन्मना भव मद्भक्तो", "manmanā bhava madbhakto", 8),
    ("p", "मद्याजी मां नमस्कुरु", "madyājī māṃ namaskuru", 8),
    ("p", "मामेवैष्यसि युक्त्वैवम्", "māmevaiṣyasi yuktvaivam", 8),
    ("p", "आत्मानं मत्परायणः", "ātmānaṃ matparāyaṇaḥ", 8),
],

}
