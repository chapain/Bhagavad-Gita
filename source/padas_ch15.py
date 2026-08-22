# -*- coding: utf-8 -*-
"""padas_ch15.py — the pāda (quarter) division of every verse in chapter 15.

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
printed verbatim from ch15.json.
"""

GITA_CH15_PADAS = {
"15.01": [
    ("s", "श्रीभगवानुवाच।", "śrībhagavānuvāca"),
    ("p", "ऊर्ध्वमूलमधःशाखम्", "ūrdhvamūlamadhaḥśākham", 8),
    ("p", "अश्वत्थं प्राहुरव्ययम्", "aśvatthaṃ prāhuravyayam", 8),
    ("p", "छन्दांसि यस्य पर्णानि", "chandāṃsi yasya parṇāni", 8),
    ("p", "यस्तं वेद स वेदवित्", "yastaṃ veda sa vedavit", 8),
],

"15.02": [
    ("p", "अधश्चोर्ध्वं प्रसृतास्तस्य शाखा", "adhaścordhvaṃ prasṛtāstasya śākhā", 11),
    ("p", "गुणप्रवृद्धा विषयप्रवालाः", "guṇapravṛddhā viṣayapravālāḥ", 11),
    ("p", "अधश्च मूलान्यनुसन्ततानि", "adhaśca mūlānyanusantatāni", 11),
    ("p", "कर्मानुबन्धीनि मनुष्यलोके", "karmānubandhīni manuṣyaloke", 11),
],

"15.03": [
    ("p", "न रूपमस्येह तथोपलभ्यते", "na rūpamasyeha tathopalabhyate", 12),
    ("p", "नान्तो न चादिर्न च सम्प्रतिष्ठा", "nānto na cādirna ca sampratiṣṭhā", 11),
    ("p", "अश्वत्थमेनं सुविरूढमूलम्", "aśvatthamenaṃ suvirūḍhamūlam", 11),
    ("p", "असङ्गशस्त्रेण दृढेन छित्त्वा", "asaṅgaśastreṇa dṛḍhena chittvā", 11),
],

"15.04": [
    ("p", "ततः पदं तत्परिमार्गितव्यं", "tataḥ padaṃ tatparimārgitavyaṃ", 11),
    ("p", "यस्मिन्गता न निवर्तन्ति भूयः", "yasmingatā na nivartanti bhūyaḥ", 11),
    ("p", "तमेव चाद्यं पुरुषं प्रपद्ये", "tameva cādyaṃ puruṣaṃ prapadye", 11),
    ("p", "यतः प्रवृत्तिः प्रसृता पुराणी", "yataḥ pravṛttiḥ prasṛtā purāṇī", 11),
],

"15.05": [
    ("p", "निर्मानमोहा जितसङ्गदोषा", "nirmānamohā jitasaṅgadoṣā", 11),
    ("p", "अध्यात्मनित्या विनिवृत्तकामाः", "adhyātmanityā vinivṛttakāmāḥ", 11),
    ("p", "द्वन्द्वैर्विमुक्ताः सुखदुःखसंज्ञैर्", "dvandvairvimuktāḥ sukhaduḥkhasaṃjñair", 11),
    ("p", "गच्छन्त्यमूढाः पदमव्ययं तत्", "gacchantyamūḍhāḥ padamavyayaṃ tat", 11),
],

"15.06": [
    ("p", "न तद्भासयते सूर्यो", "na tadbhāsayate sūryo", 8),
    ("p", "न शशाङ्को न पावकः", "na śaśāṅko na pāvakaḥ", 8),
    ("p", "यद्गत्वा न निवर्तन्ते", "yadgatvā na nivartante", 8),
    ("p", "तद्धाम परमं मम", "taddhāma paramaṃ mama", 8),
],

"15.07": [
    ("p", "ममैवांशो जीवलोके", "mamaivāṃśo jīvaloke", 8),
    ("p", "जीवभूतः सनातनः", "jīvabhūtaḥ sanātanaḥ", 8),
    ("p", "मनःषष्ठानीन्द्रियाणि", "manaḥṣaṣṭhānīndriyāṇi", 8),
    ("p", "प्रकृतिस्थानि कर्षति", "prakṛtisthāni karṣati", 8),
],

"15.08": [
    ("p", "शरीरं यदवाप्नोति", "śarīraṃ yadavāpnoti", 8),
    ("p", "यच्चाप्युत्क्रामतीश्वरः", "yaccāpyutkrāmatīśvaraḥ", 8),
    ("p", "गृहीत्वैतानि संयाति", "gṛhītvaitāni saṃyāti", 8),
    ("p", "वायुर्गन्धानिवाशयात्", "vāyurgandhānivāśayāt", 8),
],

"15.09": [
    ("p", "श्रोत्रं चक्षुः स्पर्शनं च", "śrotraṃ cakṣuḥ sparśanaṃ ca", 8),
    ("p", "रसनं घ्राणमेव च", "rasanaṃ ghrāṇameva ca", 8),
    ("p", "अधिष्ठाय मनश्चायं", "adhiṣṭhāya manaścāyaṃ", 8),
    ("p", "विषयानुपसेवते", "viṣayānupasevate", 8),
],

"15.10": [
    ("p", "उत्क्रामन्तं स्थितं वापि", "utkrāmantaṃ sthitaṃ vāpi", 8),
    ("p", "भुञ्जानं वा गुणान्वितम्", "bhuñjānaṃ vā guṇānvitam", 8),
    ("p", "विमूढा नानुपश्यन्ति", "vimūḍhā nānupaśyanti", 8),
    ("p", "पश्यन्ति ज्ञानचक्षुषः", "paśyanti jñānacakṣuṣaḥ", 8),
],

"15.11": [
    ("p", "यतन्तो योगिनश्चैनं", "yatanto yoginaścainaṃ", 8),
    ("p", "पश्यन्त्यात्मन्यवस्थितम्", "paśyantyātmanyavasthitam", 8),
    ("p", "यतन्तोऽप्यकृतात्मानो", "yatanto’pyakṛtātmāno", 8),
    ("p", "नैनं पश्यन्त्यचेतसः", "nainaṃ paśyantyacetasaḥ", 8),
],

"15.12": [
    ("p", "यदादित्यगतं तेजो", "yadādityagataṃ tejo", 8),
    ("p", "जगद्भासयतेऽखिलम्", "jagadbhāsayate’khilam", 8),
    ("p", "यच्चन्द्रमसि यच्चाग्नौ", "yaccandramasi yaccāgnau", 8),
    ("p", "तत्तेजो विद्धि मामकम्", "tattejo viddhi māmakam", 8),
],

"15.13": [
    ("p", "गामाविश्य च भूतानि", "gāmāviśya ca bhūtāni", 8),
    ("p", "धारयाम्यहमोजसा", "dhārayāmyahamojasā", 8),
    ("p", "पुष्णामि चौषधीः सर्वाः", "puṣṇāmi cauṣadhīḥ sarvāḥ", 8),
    ("p", "सोमो भूत्वा रसात्मकः", "somo bhūtvā rasātmakaḥ", 8),
],

"15.14": [
    ("p", "अहं वैश्वानरो भूत्वा", "ahaṃ vaiśvānaro bhūtvā", 8),
    ("p", "प्राणिनां देहमाश्रितः", "prāṇināṃ dehamāśritaḥ", 8),
    ("p", "प्राणापानसमायुक्तः", "prāṇāpānasamāyuktaḥ", 8),
    ("p", "पचाम्यन्नं चतुर्विधम्", "pacāmyannaṃ caturvidham", 8),
],

"15.15": [
    ("p", "सर्वस्य चाहं हृदि सन्निविष्टो", "sarvasya cāhaṃ hṛdi sanniviṣṭo", 11),
    ("p", "मत्तः स्मृतिर्ज्ञानमपोहनं च", "mattaḥ smṛtirjñānamapohanaṃ ca", 11),
    ("p", "वेदैश्च सर्वैरहमेव वेद्यो", "vedaiśca sarvairahameva vedyo", 11),
    ("p", "वेदान्तकृद्वेदविदेव चाहम्", "vedāntakṛdvedavideva cāham", 11),
],

"15.16": [
    ("p", "द्वाविमौ पुरुषौ लोके", "dvāvimau puruṣau loke", 8),
    ("p", "क्षरश्चाक्षर एव च", "kṣaraścākṣara eva ca", 8),
    ("p", "क्षरः सर्वाणि भूतानि", "kṣaraḥ sarvāṇi bhūtāni", 8),
    ("p", "कूटस्थोऽक्षर उच्यते", "kūṭastho’kṣara ucyate", 8),
],

"15.17": [
    ("p", "उत्तमः पुरुषस्त्वन्यः", "uttamaḥ puruṣastvanyaḥ", 8),
    ("p", "परमात्मेत्युदाहृतः", "paramātmetyudāhṛtaḥ", 8),
    ("p", "यो लोकत्रयमाविश्य", "yo lokatrayamāviśya", 8),
    ("p", "बिभर्त्यव्यय ईश्वरः", "bibhartyavyaya īśvaraḥ", 8),
],

"15.18": [
    ("p", "यस्मात्क्षरमतीतोऽहम्", "yasmātkṣaramatīto’ham", 8),
    ("p", "अक्षरादपि चोत्तमः", "akṣarādapi cottamaḥ", 8),
    ("p", "अतोऽस्मि लोके वेदे च", "ato’smi loke vede ca", 8),
    ("p", "प्रथितः पुरुषोत्तमः", "prathitaḥ puruṣottamaḥ", 8),
],

"15.19": [
    ("p", "यो मामेवमसम्मूढो", "yo māmevamasammūḍho", 8),
    ("p", "जानाति पुरुषोत्तमम्", "jānāti puruṣottamam", 8),
    ("p", "स सर्वविद्भजति मां", "sa sarvavidbhajati māṃ", 8),
    ("p", "सर्वभावेन भारत", "sarvabhāvena bhārata", 8),
],

"15.20": [
    ("p", "इति गुह्यतमं शास्त्रम्", "iti guhyatamaṃ śāstram", 8),
    ("p", "इदमुक्तं मयानघ", "idamuktaṃ mayānagha", 8),
    ("p", "एतद्बुद्ध्वा बुद्धिमान्स्यात्", "etadbuddhvā buddhimānsyāt", 8),
    ("p", "कृतकृत्यश्च भारत", "kṛtakṛtyaśca bhārata", 8),
],

}
