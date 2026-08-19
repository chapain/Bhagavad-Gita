# -*- coding: utf-8 -*-
"""padas_ch13.py — the pāda (quarter) division of every verse in chapter 13.

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
printed verbatim from ch13.json.
"""

GITA_CH13_PADAS = {
"13.01": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "इदं शरीरं कौन्तेय", "idaṃ śarīraṃ kaunteya", 8),
    ("p", "क्षेत्रमित्यभिधीयते", "kṣetramityabhidhīyate", 8),
    ("p", "एतद्यो वेत्ति तं प्राहुः", "etadyo vetti taṃ prāhuḥ", 8),
    ("p", "क्षेत्रज्ञ इति तद्विदः", "kṣetrajña iti tadvidaḥ", 8),
],

"13.02": [
    ("p", "क्षेत्रज्ञं चापि मां विद्धि", "kṣetrajñaṃ cāpi māṃ viddhi", 8),
    ("p", "सर्वक्षेत्रेषु भारत", "sarvakṣetreṣu bhārata", 8),
    ("p", "क्षेत्रक्षेत्रज्ञयोर्ज्ञानं", "kṣetrakṣetrajñayorjñānaṃ", 8),
    ("p", "यत्तज्ज्ञानं मतं मम", "yattajjñānaṃ mataṃ mama", 8),
],

"13.03": [
    ("p", "तत्क्षेत्रं यच्च यादृक्च", "tatkṣetraṃ yacca yādṛkca", 8),
    ("p", "यद्विकारि यतश्च यत्", "yadvikāri yataśca yat", 8),
    ("p", "स च यो यत्प्रभावश्च", "sa ca yo yatprabhāvaśca", 8),
    ("p", "तत्समासेन मे शृणु", "tatsamāsena me śṛṇu", 8),
],

"13.04": [
    ("p", "ऋषिभिर्बहुधा गीतं", "ṛṣibhirbahudhā gītaṃ", 8),
    ("p", "छन्दोभिर्विविधैः पृथक्", "chandobhirvividhaiḥ pṛthak", 8),
    ("p", "ब्रह्मसूत्रपदैश्चैव", "brahmasūtrapadaiścaiva", 8),
    ("p", "हेतुमद्भिर्विनिश्चितैः", "hetumadbhirviniścitaiḥ", 8),
],

"13.05": [
    ("p", "महाभूतान्यहङ्कारो", "mahābhūtānyahaṅkāro", 8),
    ("p", "बुद्धिरव्यक्तमेव च", "buddhiravyaktameva ca", 8),
    ("p", "इन्द्रियाणि दशैकं च", "indriyāṇi daśaikaṃ ca", 8),
    ("p", "पञ्च चेन्द्रियगोचराः", "pañca cendriyagocarāḥ", 8),
],

"13.06": [
    ("p", "इच्छा द्वेषः सुखं दुःखं", "icchā dveṣaḥ sukhaṃ duḥkhaṃ", 8),
    ("p", "सङ्घातश्चेतना धृतिः", "saṅghātaścetanā dhṛtiḥ", 8),
    ("p", "एतत्क्षेत्रं समासेन", "etatkṣetraṃ samāsena", 8),
    ("p", "सविकारमुदाहृतम्", "savikāramudāhṛtam", 8),
],

"13.07": [
    ("p", "अमानित्वमदम्भित्वमहिंसा", "amānitvamadambhitvamahiṃsā", 11),
    ("p", "क्षान्तिरार्जवम्", " kṣāntirārjavam", 5),
    ("p", "आचार्योपासनं शौचं", "ācāryopāsanaṃ śaucaṃ", 8),
    ("p", "स्थैर्यमात्मविनिग्रहः", "sthairyamātmavinigrahaḥ", 8),
],

"13.08": [
    ("p", "इन्द्रियार्थेषु वैराग्यम्", "indriyārtheṣu vairāgyam", 8),
    ("p", "अनहङ्कार एव च", "anahaṅkāra eva ca", 8),
    ("p", "जन्ममृत्युजराव्याधि", "janmamṛtyujarāvyādhi", 8),
    ("p", "दुःखदोषानुदर्शनम्", "duḥkhadoṣānudarśanam", 8),
],

"13.09": [
    ("p", "असक्तिरनभिष्वङ्गः", "asaktiranabhiṣvaṅgaḥ", 8),
    ("p", "पुत्रदारगृहादिषु", "putradāragṛhādiṣu", 8),
    ("p", "नित्यं च समचित्तत्वम्", "nityaṃ ca samacittatvam", 8),
    ("p", "इष्टानिष्टोपपत्तिषु", "iṣṭāniṣṭopapattiṣu", 8),
],

"13.10": [
    ("p", "मयि चानन्ययोगेन", "mayi cānanyayogena", 8),
    ("p", "भक्तिरव्यभिचारिणी", "bhaktiravyabhicāriṇī", 8),
    ("p", "विविक्तदेशसेवित्वम्", "viviktadeśasevitvam", 8),
    ("p", "अरतिर्जनसंसदि", "aratirjanasaṃsadi", 8),
],

"13.11": [
    ("p", "अध्यात्मज्ञाननित्यत्वं", "adhyātmajñānanityatvaṃ", 8),
    ("p", "तत्त्वज्ञानार्थदर्शनम्", "tattvajñānārthadarśanam", 8),
    ("p", "एतज्ज्ञानमिति प्रोक्तम्", "etajjñānamiti proktam", 8),
    ("p", "अज्ञानं यदतोऽन्यथा", "ajñānaṃ yadato’nyathā", 8),
],

"13.12": [
    ("p", "ज्ञेयं यत्तत्प्रवक्ष्यामि", "jñeyaṃ yattatpravakṣyāmi", 8),
    ("p", "यज्ज्ञात्वामृतमश्नुते", "yajjñātvāmṛtamaśnute", 8),
    ("p", "अनादिमत्परं ब्रह्म", "anādimatparaṃ brahma", 8),
    ("p", "न सत्तन्नासदुच्यते", "na sattannāsaducyate", 8),
],

"13.13": [
    ("p", "सर्वतःपाणिपादं तत्", "sarvataḥpāṇipādaṃ tat", 8),
    ("p", "सर्वतोक्षिशिरोमुखम्", "sarvatokṣiśiromukham", 8),
    ("p", "सर्वतःश्रुतिमल्लोके", "sarvataḥśrutimalloke", 8),
    ("p", "सर्वमावृत्य तिष्ठति", "sarvamāvṛtya tiṣṭhati", 8),
],

"13.14": [
    ("p", "सर्वेन्द्रियगुणाभासं", "sarvendriyaguṇābhāsaṃ", 8),
    ("p", "सर्वेन्द्रियविवर्जितम्", "sarvendriyavivarjitam", 8),
    ("p", "असक्तं सर्वभृच्चैव", "asaktaṃ sarvabhṛccaiva", 8),
    ("p", "निर्गुणं गुणभोक्तृ च", "nirguṇaṃ guṇabhoktṛ ca", 8),
],

"13.15": [
    ("p", "बहिरन्तश्च भूतानाम्", "bahirantaśca bhūtānām", 8),
    ("p", "अचरं चरमेव च", "acaraṃ carameva ca", 8),
    ("p", "सूक्ष्मत्वात्तदविज्ञेयं", "sūkṣmatvāttadavijñeyaṃ", 8),
    ("p", "दूरस्थं चान्तिके च तत्", "dūrasthaṃ cāntike ca tat", 8),
],

"13.16": [
    ("p", "अविभक्तं च भूतेषु", "avibhaktaṃ ca bhūteṣu", 8),
    ("p", "विभक्तमिव च स्थितम्", "vibhaktamiva ca sthitam", 8),
    ("p", "भूतभर्तृ च तज्ज्ञेयं", "bhūtabhartṛ ca tajjñeyaṃ", 8),
    ("p", "ग्रसिष्णु प्रभविष्णु च", "grasiṣṇu prabhaviṣṇu ca", 8),
],

"13.17": [
    ("p", "ज्योतिषामपि तज्ज्योतिस्", "jyotiṣāmapi tajjyotis", 8),
    ("p", "तमसः परमुच्यते", "tamasaḥ paramucyate", 8),
    ("p", "ज्ञानं ज्ञेयं ज्ञानगम्यं", "jñānaṃ jñeyaṃ jñānagamyaṃ", 8),
    ("p", "हृदि सर्वस्य विष्ठितम्", "hṛdi sarvasya viṣṭhitam", 8),
],

"13.18": [
    ("p", "इति क्षेत्रं तथा ज्ञानं", "iti kṣetraṃ tathā jñānaṃ", 8),
    ("p", "ज्ञेयं चोक्तं समासतः", "jñeyaṃ coktaṃ samāsataḥ", 8),
    ("p", "मद्भक्त एतद्विज्ञाय", "madbhakta etadvijñāya", 8),
    ("p", "मद्भावायोपपद्यते", "madbhāvāyopapadyate", 8),
],

"13.19": [
    ("p", "प्रकृतिं पुरुषं चैव", "prakṛtiṃ puruṣaṃ caiva", 8),
    ("p", "विद्ध्यनादी उभावपि", "viddhyanādī ubhāvapi", 8),
    ("p", "विकारांश्च गुणांश्चैव", "vikārāṃśca guṇāṃścaiva", 8),
    ("p", "विद्धि प्रकृतिसम्भवान्", "viddhi prakṛtisambhavān", 8),
],

"13.20": [
    ("p", "कार्यकरणकर्तृत्वेहेतुः", "kāryakaraṇakartṛtvehetuḥ", 10),
    ("p", "प्रकृतिरुच्यते", " prakṛtirucyate", 6),
    ("p", "पुरुषः सुखदुःखानां", "puruṣaḥ sukhaduḥkhānāṃ", 8),
    ("p", "भोक्तृत्वे हेतुरुच्यते", "bhoktṛtve heturucyate", 8),
],

"13.21": [
    ("p", "पुरुषः प्रकृतिस्थो हि", "puruṣaḥ prakṛtistho hi", 8),
    ("p", "भुङ्क्ते प्रकृतिजान्गुणान्", "bhuṅkte prakṛtijānguṇān", 8),
    ("p", "कारणं गुणसङ्गोऽस्य", "kāraṇaṃ guṇasaṅgo’sya", 8),
    ("p", "सदसद्योनिजन्मसु", "sadasadyonijanmasu", 8),
],

"13.22": [
    ("p", "उपद्रष्टानुमन्ता चभर्ता", "upadraṣṭānumantā cabhartā", 10),
    ("p", "भोक्ता महेश्वरः", " bhoktā maheśvaraḥ", 6),
    ("p", "परमात्मेति चाप्युक्तो", "paramātmeti cāpyukto", 8),
    ("p", "देहेऽस्मिन्पुरुषः परः", "dehe’sminpuruṣaḥ paraḥ", 8),
],

"13.23": [
    ("p", "य एवं वेत्ति पुरुषं", "ya evaṃ vetti puruṣaṃ", 8),
    ("p", "प्रकृतिं च गुणैः सह", "prakṛtiṃ ca guṇaiḥ saha", 8),
    ("p", "सर्वथा वर्तमानोऽपि", "sarvathā vartamāno’pi", 8),
    ("p", "न स भूयोऽभिजायते", "na sa bhūyo’bhijāyate", 8),
],

"13.24": [
    ("p", "ध्यानेनात्मनि पश्यन्ति", "dhyānenātmani paśyanti", 8),
    ("p", "केचिदात्मानमात्मना", "kecidātmānamātmanā", 8),
    ("p", "अन्ये साङ्ख्येन योगेन", "anye sāṅkhyena yogena", 8),
    ("p", "कर्मयोगेन चापरे", "karmayogena cāpare", 8),
],

"13.25": [
    ("p", "अन्ये त्वेवमजानन्तः", "anye tvevamajānantaḥ", 8),
    ("p", "श्रुत्वान्येभ्य उपासते", "śrutvānyebhya upāsate", 8),
    ("p", "तेऽपि चातितरन्त्येव", "te’pi cātitarantyeva", 8),
    ("p", "मृत्युं श्रुतिपरायणाः", "mṛtyuṃ śrutiparāyaṇāḥ", 8),
],

"13.26": [
    ("p", "यावत्सञ्जायते किञ्चित्", "yāvatsañjāyate kiñcit", 8),
    ("p", "सत्त्वं स्थावरजङ्गमम्", "sattvaṃ sthāvarajaṅgamam", 8),
    ("p", "क्षेत्रक्षेत्रज्ञसंयोगात्", "kṣetrakṣetrajñasaṃyogāt", 8),
    ("p", "तद्विद्धि भरतर्षभ", "tadviddhi bharatarṣabha", 8),
],

"13.27": [
    ("p", "समं सर्वेषु भूतेषु", "samaṃ sarveṣu bhūteṣu", 8),
    ("p", "तिष्ठन्तं परमेश्वरम्", "tiṣṭhantaṃ parameśvaram", 8),
    ("p", "विनश्यत्स्वविनश्यन्तं", "vinaśyatsvavinaśyantaṃ", 8),
    ("p", "यः पश्यति स पश्यति", "yaḥ paśyati sa paśyati", 8),
],

"13.28": [
    ("p", "समं पश्यन्हि सर्वत्र", "samaṃ paśyanhi sarvatra", 8),
    ("p", "समवस्थितमीश्वरम्", "samavasthitamīśvaram", 8),
    ("p", "न हिनस्त्यात्मनात्मानं", "na hinastyātmanātmānaṃ", 8),
    ("p", "ततो याति परां गतिम्", "tato yāti parāṃ gatim", 8),
],

"13.29": [
    ("p", "प्रकृत्यैव च कर्माणि", "prakṛtyaiva ca karmāṇi", 8),
    ("p", "क्रियमाणानि सर्वशः", "kriyamāṇāni sarvaśaḥ", 8),
    ("p", "यः पश्यति तथात्मानम्", "yaḥ paśyati tathātmānam", 8),
    ("p", "अकर्तारं स पश्यति", "akartāraṃ sa paśyati", 8),
],

"13.30": [
    ("p", "यदा भूतपृथग्भावम्", "yadā bhūtapṛthagbhāvam", 8),
    ("p", "एकस्थमनुपश्यति", "ekasthamanupaśyati", 8),
    ("p", "तत एव च विस्तारं", "tata eva ca vistāraṃ", 8),
    ("p", "ब्रह्म सम्पद्यते तदा", "brahma sampadyate tadā", 8),
],

"13.31": [
    ("p", "अनादित्वान्निर्गुणत्वात्", "anāditvānnirguṇatvāt", 8),
    ("p", "परमात्मायमव्ययः", "paramātmāyamavyayaḥ", 8),
    ("p", "शरीरस्थोऽपि कौन्तेय", "śarīrastho’pi kaunteya", 8),
    ("p", "न करोति न लिप्यते", "na karoti na lipyate", 8),
],

"13.32": [
    ("p", "यथा सर्वगतं सौक्ष्म्याद्", "yathā sarvagataṃ saukṣmyād", 8),
    ("p", "आकाशं नोपलिप्यते", "ākāśaṃ nopalipyate", 8),
    ("p", "सर्वत्रावस्थितो देहे", "sarvatrāvasthito dehe", 8),
    ("p", "तथात्मा नोपलिप्यते", "tathātmā nopalipyate", 8),
],

"13.33": [
    ("p", "यथा प्रकाशयत्येकः", "yathā prakāśayatyekaḥ", 8),
    ("p", "कृत्स्नं लोकमिमं रविः", "kṛtsnaṃ lokamimaṃ raviḥ", 8),
    ("p", "क्षेत्रं क्षेत्री तथा कृत्स्नं", "kṣetraṃ kṣetrī tathā kṛtsnaṃ", 8),
    ("p", "प्रकाशयति भारत", "prakāśayati bhārata", 8),
],

"13.34": [
    ("p", "क्षेत्रक्षेत्रज्ञयोरेवमन्तरं", "kṣetrakṣetrajñayorevamantaraṃ", 11),
    ("p", "ज्ञानचक्षुषा", " jñānacakṣuṣā", 5),
    ("p", "भूतप्रकृतिमोक्षं च", "bhūtaprakṛtimokṣaṃ ca", 8),
    ("p", "ये विदुर्यान्ति ते परम्", "ye viduryānti te param", 8),
],

}
