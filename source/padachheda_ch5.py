# -*- coding: utf-8 -*-
"""padachheda_ch5.py — per-pāda pada-chheda (word splits) for all 29 verses of Gita Chapter 5.

Structure: verse_number -> {
    "s": [[deva_word, iast, meaning], ...]   # speaker line words (if any)
    0..3: [[deva_word, iast, meaning], ...]  # the four pādas
}
Readings aligned to the Śaṅkara-bhāṣya edition."""

GITA_CH5_WORDS = {
1: {"s": [["अर्जुनः", "arjunaḥ", "Arjuna"],
          ["उवाच", "uvāca", "said"]],
    0: [["सन्न्यासम्", "sannyāsam", "renunciation"],
        ["कर्मणाम्", "karmaṇām", "of actions"],
        ["कृष्ण", "kṛṣṇa", "O Kṛṣṇa"]],
    1: [["पुनः", "punaḥ", "again, also"],
        ["योगम्", "yogam", "yoga"],
        ["च", "ca", "and"],
        ["शंससि", "śaṁsasi", "you praise"]],
    2: [["यत्", "yat", "which"],
        ["श्रेयः", "śreyaḥ", "the better"],
        ["एतयोः", "etayoḥ", "of the two"],
        ["एकम्", "ekam", "one"]],
    3: [["तत्", "tat", "that"],
        ["मे", "me", "to me"],
        ["ब्रूहि", "brūhi", "tell"],
        ["सुनिश्चितम्", "suniścitam", "decisively, for certain"]]},

2: {"s": [
    ["श्रीभगवान्", "śrībhagavān", "the Blessed Lord"],
    ["उवाच", "uvāca", "said"]
],
    0: [
    ["सन्न्यासः", "sannyāsaḥ", "renunciation"], ["कर्मयोगः", "karmayogaḥ", "karma-yoga"],
        ["च", "ca", "and"]],
    1: [
    ["निःश्रेयसकरौ", "niḥśreyasakarau", "leading to the highest good"],
        ["उभौ", "ubhau", "both"]],
    2: [
    ["तयोः", "tayoḥ", "of the two"], ["तु", "tu", "but"],
        ["कर्मसन्न्यासात्", "karmasannyāsāt", "than the renunciation of action"]],
    3: [
    ["कर्मयोगः", "karmayogaḥ", "karma-yoga"], ["विशिष्यते", "viśiṣyate", "excels"]]
},
3: {"s": [],
    0: [
    ["ज्ञेयः", "jñeyaḥ", "to be known"], ["सः", "saḥ", "he"],
        ["नित्यसन्न्यासी", "nityasannyāsī", "ever-renouncing"]],
    1: [
    ["यः", "yaḥ", "who"], ["न", "na", "neither"], ["द्वेष्टि", "dveṣṭi", "hates"],
        ["न", "na", "nor"], ["काङ्क्षति", "kāṅkṣati", "desires"]],
    2: [
    ["निर्द्वन्द्वः", "nirdvandvaḥ", "free from the pairs of opposites"],
        ["हि", "hi", "indeed"], ["महाबाहो", "mahābāho", "O mighty-armed one"]],
    3: [
    ["सुखम्", "sukham", "easily"], ["बन्धात्", "bandhāt", "from bondage"],
        ["प्रमुच्यते", "pramucyate", "is released"]]
},
4: {"s": [],
    0: [
    ["साङ्ख्ययोगौ", "sāṅkhyayogau", "sāṅkhya and yoga"],
        ["पृथक्", "pṛthak", "as different"], ["बालाः", "bālāḥ", "the childish"]],
    1: [
    ["प्रवदन्ति", "pravadanti", "declare"], ["न", "na", "not"],
        ["पण्डिताः", "paṇḍitāḥ", "the wise"]],
    2: [
    ["एकम्", "ekam", "one"], ["अपि", "api", "even"],
        ["आस्थितः", "āsthitaḥ", "established in"], ["सम्यक्", "samyak", "rightly"]],
    3: [
    ["उभयोः", "ubhayoḥ", "of both"], ["विन्दते", "vindate", "attains"],
        ["फलम्", "phalam", "the fruit"]]
},
5: {"s": [],
    0: [["यत्", "yat", "which"],
        ["साङ्ख्यैः", "sāṅkhyaiḥ", "by the sāṅkhyas"],
        ["प्राप्यते", "prāpyate", "is attained"],
        ["स्थानम्", "sthānam", "state"]],
    1: [["तत्", "tat", "that"],
        ["योगैः", "yogaiḥ", "by the yogis"],
        ["अपि", "api", "also"],
        ["गम्यते", "gamyate", "is reached"]],
    2: [["एकम्", "ekam", "as one"],
        ["साङ्ख्यम्", "sāṅkhyam", "sāṅkhya"],
        ["च", "ca", "and"],
        ["योगम्", "yogam", "yoga"],
        ["च", "ca", "and"]],
    3: [["यः", "yaḥ", "who"],
        ["पश्यति", "paśyati", "sees"],
        ["सः", "saḥ", "he"],
        ["पश्यति", "paśyati", "sees"]]},

6: {"s": [],
    0: [
    ["सन्न्यासः", "sannyāsaḥ", "renunciation"], ["तु", "tu", "but"],
        ["महाबाहो", "mahābāho", "O mighty-armed one"]],
    1: [
    ["दुःखम्", "duḥkham", "hard, difficult"], ["आप्तुम्", "āptum", "to attain"],
        ["अयोगतः", "ayogataḥ", "without yoga"]],
    2: [
    ["योगयुक्तः", "yogayuktaḥ", "devoted to yoga"], ["मुनिः", "muniḥ", "the sage"],
        ["ब्रह्म", "brahma", "Brahman"]],
    3: [
    ["नचिरेण", "nacireṇa", "before long"], ["अधिगच्छति", "adhigacchati", "attains"]]
},
7: {"s": [],
    0: [["योगयुक्तः", "yogayuktaḥ", "devoted to yoga"],
        ["विशुद्धात्मा", "viśuddhātmā", "of pure soul"]],
    1: [["विजितात्मा", "vijitātmā", "self-conquered"],
        ["जितेन्द्रियः", "jitendriyaḥ", "senses conquered"]],
    2: [["सर्वभूतात्मभूतात्मा", "sarvabhūtātmabhūtātmā", "the Self of all beings"]],
    3: [["कुर्वन्", "kurvan", "acting"],
        ["अपि", "api", "though"],
        ["न", "na", "not"],
        ["लिप्यते", "lipyate", "is stained"]]},

8: {"s": [],
    0: [["न", "na", "not"],
        ["एव", "eva", "at all"],
        ["किञ्चित्", "kiñcit", "anything"],
        ["करोमि", "karomi", "I do"],
        ["इति", "iti", "thus"]],
    1: [["युक्तः", "yuktaḥ", "the yoked one"],
        ["मन्येत", "manyeta", "should think"],
        ["तत्त्ववित्", "tattvavit", "the knower of truth"]],
    2: [["पश्यन्", "paśyan", "seeing"],
        ["शृण्वन्", "śṛṇvan", "hearing"],
        ["स्पृशन्", "spṛśan", "touching"],
        ["जिघ्रन्", "jighran", "smelling"]],
    3: [["अश्नन्", "aśnan", "eating"],
        ["गच्छन्", "gacchan", "moving, going"],
        ["स्वपन्", "svapan", "sleeping"],
        ["श्वसन्", "śvasan", "breathing"]]},

9: {"s": [],
    0: [
    ["प्रलपन्", "pralapan", "speaking"], ["विसृजन्", "visṛjan", "giving up"],
        ["गृह्णन्", "gṛhṇan", "holding, taking"]],
    1: [
    ["उन्मिषन्", "unmiṣan", "opening the eyes"],
        ["निमिषन्", "nimiṣan", "closing the eyes"], ["अपि", "api", "even"]],
    2: [
    ["इन्द्रियाणि", "indriyāṇi", "the senses"],
        ["इन्द्रियार्थेषु", "indriyārtheṣu", "among the sense-objects"]],
    3: [
    ["वर्तन्ते", "vartante", "move, act"], ["इति", "iti", "thus"],
        ["धारयन्", "dhārayan", "holding, thinking"]]
},
10: {"s": [],
     0: [["ब्रह्मणि", "brahmaṇi", "in Brahman"],
         ["आधाय", "ādhāya", "having placed, offered"],
         ["कर्माणि", "karmāṇi", "actions"]],
     1: [["सङ्गम्", "saṅgam", "attachment"],
         ["त्यक्त्वा", "tyaktvā", "having renounced"],
         ["करोति", "karoti", "acts, performs"],
         ["यः", "yaḥ", "who"]],
     2: [["लिप्यते", "lipyate", "is stained"],
         ["न", "na", "not"],
         ["सः", "saḥ", "he"],
         ["पापेन", "pāpena", "by sin"]],
     3: [["पद्मपत्रम्", "padmapatram", "a lotus leaf"],
         ["इव", "iva", "as, like"],
         ["अम्भसा", "ambhasā", "by water"]]},

11: {"s": [],
     0: [["कायेन", "kāyena", "with the body"],
         ["मनसा", "manasā", "with the mind"],
         ["बुद्ध्या", "buddhyā", "with the intellect"]],
     1: [["केवलैः", "kevalaiḥ", "alone, merely"],
         ["इन्द्रियैः", "indriyaiḥ", "with the senses"],
         ["अपि", "api", "even"]],
     2: [["योगिनः", "yoginaḥ", "the yogis"],
         ["कर्म", "karma", "actions"],
         ["कुर्वन्ति", "kurvanti", "perform"]],
     3: [["सङ्गम्", "saṅgam", "attachment"],
         ["त्यक्त्वा", "tyaktvā", "having abandoned"],
         ["आत्मशुद्धये", "ātmaśuddhaye", "for the purification of the self"]]},

12: {"s": [],
    0: [
    ["युक्तः", "yuktaḥ", "the one established in yoga"],
        ["कर्मफलम्", "karmaphalam", "the fruit of action"],
        ["त्यक्त्वा", "tyaktvā", "having renounced"]],
    1: [
    ["शान्तिम्", "śāntim", "peace"], ["आप्नोति", "āpnoti", "attains"],
        ["नैष्ठिकीम्", "naiṣṭhikīm", "abiding, lasting"]],
    2: [
    ["अयुक्तः", "ayuktaḥ", "the one not established in yoga"],
        ["कामकारेण", "kāmakāreṇa", "by desire-driven impulse"]],
    3: [
    ["फले", "phale", "to the fruit"], ["सक्तः", "saktaḥ", "attached"],
        ["निबध्यते", "nibadhyate", "is bound"]]
},
13: {"s": [],
    0: [
    ["सर्वकर्माणि", "sarvakarmāṇi", "all actions"], ["मनसा", "manasā", "in the mind"]],
    1: [
    ["सन्न्यस्य", "sannyasya", "having renounced"], ["आस्ते", "āste", "dwells"],
        ["सुखम्", "sukham", "happily"], ["वशी", "vaśī", "the self-controlled one"]],
    2: [
    ["नवद्वारे", "navadvāre", "in the nine-gated"], ["पुरे", "pure", "city"],
        ["देही", "dehī", "the embodied one"]],
    3: [
    ["न", "na", "neither"], ["एव", "eva", "indeed"], ["कुर्वन्", "kurvan", "acting"],
        ["न", "na", "nor"], ["कारयन्", "kārayan", "causing to act"]]
},
14: {"s": [],
     0: [["न", "na", "not"],
         ["कर्तृत्वम्", "kartṛtvam", "agency, doership"],
         ["न", "na", "nor"],
         ["कर्माणि", "karmāṇi", "actions"]],
     1: [["लोकस्य", "lokasya", "for the world"],
         ["सृजति", "sṛjati", "creates"],
         ["प्रभुः", "prabhuḥ", "the Lord"]],
     2: [["न", "na", "nor"],
         ["कर्मफलसंयोगम्", "karmaphalasaṁyogam", "the connection with the fruit of action"]],
     3: [["स्वभावः", "svabhāvaḥ", "nature"],
         ["तु", "tu", "indeed"],
         ["प्रवर्तते", "pravartate", "acts, moves"]]},

15: {"s": [],
     0: [["न", "na", "not"],
         ["आदत्ते", "ādatte", "accepts, takes"],
         ["कस्यचित्", "kasyacit", "of anyone"],
         ["पापम्", "pāpam", "sin"]],
     1: [["न", "na", "nor"],
         ["च", "ca", "and"],
         ["एव", "eva", "indeed"],
         ["सुकृतम्", "sukṛtam", "merit, good deed"],
         ["विभुः", "vibhuḥ", "the all-pervading One"]],
     2: [["अज्ञानेन", "ajñānena", "by ignorance"],
         ["आवृतम्", "āvṛtam", "veiled, enveloped"],
         ["ज्ञानम्", "jñānam", "knowledge"]],
     3: [["तेन", "tena", "thereby"],
         ["मुह्यन्ति", "muhyanti", "are deluded"],
         ["जन्तवः", "jantavaḥ", "beings"]]},

16: {"s": [],
     0: [["ज्ञानेन", "jñānena", "by knowledge"],
         ["तु", "tu", "but"],
         ["तत्", "tat", "that"],
         ["अज्ञानम्", "ajñānam", "ignorance"]],
     1: [["येषाम्", "yeṣām", "of those"],
         ["नाशितम्", "nāśitam", "destroyed"],
         ["आत्मनः", "ātmanaḥ", "of the Self"]],
     2: [["तेषाम्", "teṣām", "of them"],
         ["आदित्यवत्", "ādityavat", "like the sun"],
         ["ज्ञानम्", "jñānam", "knowledge"]],
     3: [["प्रकाशयति", "prakāśayati", "illumines, reveals"],
         ["तत्परम्", "tatparam", "the Supreme"]]},

17: {"s": [],
     0: [["तद्बुद्धयः", "tadbuddhayaḥ", "whose intellect is in that"],
         ["तदात्मानः", "tadātmānaḥ", "whose self is in that"]],
     1: [["तन्निष्ठाः", "tanniṣṭhāḥ", "established in that"],
         ["तत्परायणाः", "tatparāyaṇāḥ", "intent on that"]],
     2: [["गच्छन्ति", "gacchanti", "they go"],
         ["अपुनरावृत्तिम्", "apunarāvṛttim", "to non-return, no rebirth"]],
     3: [["ज्ञान", "jñāna", "by knowledge"],
         ["निर्धूत", "nirdhūta", "washed away"],
         ["कल्मषाः", "kalmaṣāḥ", "whose sins"]]},

18: {"s": [],
    0: [
    ["विद्या", "vidyā", "learning"], ["विनय", "vinaya", "and humility"],
        ["सम्पन्ने", "sampanne", "endowed with"]],
    1: [
    ["ब्राह्मणे", "brāhmaṇe", "in a brāhmaṇa"], ["गवि", "gavi", "in a cow"],
        ["हस्तिनि", "hastini", "in an elephant"]],
    2: [
    ["शुनि", "śuni", "in a dog"], ["च", "ca", "and"], ["एव", "eva", "even"],
        ["श्वपाके", "śvapāke", "in an outcaste"], ["च", "ca", "and"]],
    3: [
    ["पण्डिताः", "paṇḍitāḥ", "the wise"], ["समदर्शिनः", "samadarśinaḥ", "of equal vision"]]
},
19: {"s": [],
     0: [["इह", "iha", "here"],
         ["एव", "eva", "itself"],
         ["तैः", "taiḥ", "by them"],
         ["जितः", "jitaḥ", "conquered"],
         ["सर्गः", "sargaḥ", "the world of birth and death"]],
     1: [["येषाम्", "yeṣām", "whose"],
         ["साम्ये", "sāmye", "in equanimity"],
         ["स्थितम्", "sthitam", "resting, established"],
         ["मनः", "manaḥ", "mind"]],
     2: [["निर्दोषम्", "nirdoṣam", "spotless, flawless"],
         ["हि", "hi", "indeed"],
         ["समम्", "samam", "equal"],
         ["ब्रह्म", "brahma", "Brahman"]],
     3: [["तस्मात्", "tasmāt", "therefore"],
         ["ब्रह्मणि", "brahmaṇi", "in Brahman"],
         ["ते", "te", "they"],
         ["स्थिताः", "sthitāḥ", "established"]]},

20: {"s": [],
     0: [["न", "na", "not"],
         ["प्रहृष्येत्", "prahṛṣyet", "would rejoice"],
         ["प्रियम्", "priyam", "the pleasant, dear"],
         ["प्राप्य", "prāpya", "having obtained"]],
     1: [["न", "na", "nor"],
         ["उद्विजेत्", "udvijet", "would be perturbed"],
         ["प्राप्य", "prāpya", "having obtained"],
         ["च", "ca", "and"],
         ["अप्रियम्", "apriyam", "the unpleasant"]],
     2: [["स्थिरबुद्धिः", "sthirabuddhiḥ", "of steady intellect"],
         ["असम्मूढः", "asammūḍhaḥ", "undeluded"]],
     3: [["ब्रह्मवित्", "brahmavit", "the knower of Brahman"],
         ["ब्रह्मणि", "brahmaṇi", "in Brahman"],
         ["स्थितः", "sthitaḥ", "established, abiding"]]},

21: {"s": [],
     0: [["बाह्य", "bāhya", "external"],
         ["स्पर्शेषु", "sparśeṣu", "in contacts"],
         ["असक्त", "asakta", "unattached"],
         ["आत्मा", "ātmā", "whose self"]],
     1: [["विन्दति", "vindati", "finds"],
         ["आत्मनि", "ātmani", "in the Self"],
         ["यत्", "yat", "which"],
         ["सुखम्", "sukham", "happiness"]],
     2: [["सः", "saḥ", "he"],
         ["ब्रह्म", "brahma", "of Brahman"],
         ["योग", "yoga", "with the yoga"],
         ["युक्तात्मा", "yuktātmā", "joined in self"]],
     3: [["सुखम्", "sukham", "bliss"],
         ["अक्षयम्", "akṣayam", "imperishable"],
         ["अश्नुते", "aśnute", "enjoys"]]},

22: {"s": [],
    0: [
    ["ये", "ye", "which"], ["हि", "hi", "indeed"],
        ["संस्पर्शजाः", "saṁsparśajāḥ", "born of contact"],
        ["भोगाः", "bhogāḥ", "enjoyments, pleasures"]],
    1: [
    ["दुःखयोनयः", "duḥkhayonayaḥ", "sources of sorrow"], ["एव", "eva", "only"],
        ["ते", "te", "they"]],
    2: [
    ["आदि", "ādi", "beginning"], ["अन्तवन्तः", "antavantaḥ", "having an end"],
        ["कौन्तेय", "kaunteya", "O son of Kuntī"]],
    3: [
    ["न", "na", "not"], ["तेषु", "teṣu", "in them"], ["रमते", "ramate", "delights"],
        ["बुधः", "budhaḥ", "the wise"]]
},
23: {"s": [],
     0: [["शक्नोति", "śaknoti", "is able"],
         ["इह", "iha", "here"],
         ["एव", "eva", "itself"],
         ["यः", "yaḥ", "who"],
         ["सोढुम्", "soḍhum", "to endure"]],
     1: [["प्राक्", "prāk", "before"],
         ["शरीर", "śarīra", "of the body"],
         ["विमोक्षणात्", "vimokṣaṇāt", "from the release"]],
     2: [["काम", "kāma", "of desire"],
         ["क्रोध", "krodha", "and anger"],
         ["उद्भवम्", "udbhavam", "born of"],
         ["वेगम्", "vegam", "the impulse, urge"]],
     3: [["सः", "saḥ", "he"],
         ["युक्तः", "yuktaḥ", "yoked, disciplined"],
         ["सः", "saḥ", "he"],
         ["सुखी", "sukhī", "happy"],
         ["नरः", "naraḥ", "man"]]},

24: {"s": [],
     0: [["यः", "yaḥ", "who"],
         ["अन्तःसुखः", "antaḥsukhaḥ", "happy within"],
         ["अन्तरारामः", "antarārāmaḥ", "delighting within"]],
     1: [["तथा", "tathā", "likewise"],
         ["अन्तर्ज्योतिः", "antarjyotiḥ", "illumined within"],
         ["एव", "eva", "indeed"],
         ["यः", "yaḥ", "who"]],
     2: [["सः", "saḥ", "that"],
         ["योगी", "yogī", "yogi"],
         ["ब्रह्मनिर्वाणम्", "brahmanirvāṇam", "Brahman-nirvāṇa"]],
     3: [["ब्रह्मभूतः", "brahmabhūtaḥ", "become Brahman"],
         ["अधिगच्छति", "adhigacchati", "attains"]]},

25: {"s": [],
    0: [
    ["लभन्ते", "labhante", "attain"],
        ["ब्रह्मनिर्वाणम्", "brahmanirvāṇam", "Brahman-nirvāṇa"]],
    1: [
    ["ऋषयः", "ṛṣayaḥ", "the seers"], ["क्षीण", "kṣīṇa", "destroyed"],
        ["कल्मषाः", "kalmaṣāḥ", "whose sins"]],
    2: [
    ["छिन्न", "chinna", "cut"], ["द्वैधाः", "dvaidhāḥ", "whose doubts"],
        ["यत", "yata", "controlled"], ["आत्मानः", "ātmānaḥ", "whose selves"]],
    3: [
    ["सर्वभूतहिते", "sarvabhūtahite", "in the welfare of all beings"],
        ["रताः", "ratāḥ", "delighting"]]
},
26: {"s": [],
    0: [
    ["काम", "kāma", "of desire"], ["क्रोध", "krodha", "and anger"],
        ["वियुक्तानाम्", "viyuktānām", "of those free from"]],
    1: [
    ["यतीनाम्", "yatīnām", "of the ascetics"], ["यत", "yata", "controlled"],
        ["चेतसाम्", "cetasām", "whose thoughts"]],
    2: [
    ["अभितः", "abhitaḥ", "on every side"],
        ["ब्रह्मनिर्वाणम्", "brahmanirvāṇam", "Brahman-nirvāṇa"]],
    3: [
    ["वर्तते", "vartate", "is present"],
        ["विदितात्मनाम्", "viditātmanām", "of those who know the Self"]]
},
27: {"s": [],
     0: [["स्पर्शान्", "sparśān", "the contacts, sense-objects"],
         ["कृत्वा", "kṛtvā", "having made"],
         ["बहिः", "bahiḥ", "outside"],
         ["बाह्यान्", "bāhyān", "external"]],
     1: [["चक्षुः", "cakṣuḥ", "the vision, gaze"],
         ["च", "ca", "and"],
         ["एव", "eva", "indeed"],
         ["अन्तरे", "antare", "between"],
         ["भ्रुवोः", "bhruvoḥ", "the eyebrows"]],
     2: [["प्राणापानौ", "prāṇāpānau", "the out-breath and in-breath"],
         ["समौ", "samau", "equal, balanced"],
         ["कृत्वा", "kṛtvā", "having made"]],
     3: [["नासा", "nāsā", "of the nostrils"],
         ["अभ्यन्तर", "abhyantara", "within"],
         ["चारिणौ", "cāriṇau", "moving"]]},

28: {"s": [],
    0: [
    ["यत", "yata", "controlled"], ["इन्द्रिय", "indriya", "senses"],
        ["मनः", "manaḥ", "mind"], ["बुद्धिः", "buddhiḥ", "intellect"]],
    1: [
    ["मुनिः", "muniḥ", "the sage"], ["मोक्ष", "mokṣa", "of liberation"],
        ["परायणः", "parāyaṇaḥ", "intent on"]],
    2: [
    ["विगत", "vigata", "gone, free from"], ["इच्छा", "icchā", "desire"],
        ["भय", "bhaya", "fear"], ["क्रोधः", "krodhaḥ", "anger"]],
    3: [
    ["यः", "yaḥ", "who"], ["सदा", "sadā", "always"],
        ["मुक्तः", "muktaḥ", "freed, liberated"], ["एव", "eva", "indeed"],
        ["सः", "saḥ", "he"]]
},
29: {"s": [],
     0: [["भोक्तारम्", "bhoktāram", "the enjoyer"],
         ["यज्ञ", "yajña", "of sacrifices"],
         ["तपसाम्", "tapasām", "and austerities"]],
     1: [["सर्व", "sarva", "of all"],
         ["लोक", "loka", "the worlds"],
         ["महेश्वरम्", "maheśvaram", "the great Lord"]],
     2: [["सुहृदम्", "suhṛdam", "the friend"],
         ["सर्वभूतानाम्", "sarvabhūtānām", "of all beings"]],
     3: [["ज्ञात्वा", "jñātvā", "having known"],
         ["माम्", "mām", "me"],
         ["शान्तिम्", "śāntim", "peace"],
         ["ऋच्छति", "ṛcchati", "attains"]]},
}
