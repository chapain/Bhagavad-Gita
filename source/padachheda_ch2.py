# -*- coding: utf-8 -*-
"""padachheda_ch2.py — per-pāda pada-chheda (word splits) for the 72 verses of Gita Chapter 2.
Structure: verse -> {"s": [[word, iast, meaning],...] (speaker line), 0..3: [[word, iast, meaning],...]}"""

GITA_CH2_WORDS = {
1: {"s": [
    ["सञ्जय", "sañjaya", "Sañjaya (the narrator)"],
    ["उवाच", "uvāca", "said"]
],
    0: [
    ["तम्", "tam", "him (Arjuna)"], ["तथा", "tathā", "thus"],
        ["कृपया", "kṛpayā", "with compassion"], ["आविष्टम्", "āviṣṭam", "overcome"]],
    1: [
    ["अश्रुपूर्ण", "aśrupūrṇa", "filled with tears"], ["आकुल", "ākula", "agitated"],
        ["ईक्षणम्", "īkṣaṇam", "eyes"]],
    2: [
    ["विषीदन्तम्", "viṣīdantam", "the grieving one"], ["इदम्", "idam", "this"],
        ["वाक्यम्", "vākyam", "words"]],
    3: [
    ["उवाच", "uvāca", "spoke"],
        ["मधुसूदनः", "madhusūdanaḥ", "Madhusūdana (Kṛṣṇa, slayer of Madhu)"]]
},
2: {"s": [
    ["श्रीभगवान्", "śrībhagavān", "the Blessed Lord"],
    ["उवाच", "uvāca", "said"]
],
    0: [
    ["कुतः", "kutaḥ", "whence"], ["त्वा", "tvā", "on you"],
        ["कश्मलम्", "kaśmalam", "faintness"], ["इदम्", "idam", "this"]],
    1: [
    ["विषमे", "viṣame", "in the perilous"], ["समुपस्थितम्", "samupasthitam", "come upon"]],
    2: [
    ["अनार्य", "anārya", "unworthy of the noble"], ["जुष्टम्", "juṣṭam", "practised (by)"],
        ["अस्वर्ग्यम्", "asvargyam", "not leading to heaven"]],
    3: [
    ["अकीर्तिकरम्", "akīrtikaram", "causing disgrace"], ["अर्जुन", "arjuna", "O Arjuna"]]
},
3: {"s": [],
    0: [["क्लैब्यम्","klaibyam","unmanliness"],["मा","mā","not"],["स्म","sma","indeed"],
        ["गमः","gamaḥ","go"],["पार्थ","pārtha","O Pārtha"]],
    1: [["न","na","not"],["एतत्","etat","this"],["त्वयि","tvayi","in you"],
        ["उपपद्यते","upapadyate","is becoming"]],
    2: [["क्षुद्रम्","kṣudram","petty"],["हृदय","hṛdaya","of heart"],
        ["दौर्बल्यम्","daurbalyam","weakness"]],
    3: [["त्यक्त्वा","tyaktvā","having abandoned"],["उत्तिष्ठ","uttiṣṭha","arise"],["परन्तप","parantapa","O scorcher of foes"]]},

4: {"s": [["अर्जुन","arjuna","Arjuna"],["उवाच","uvāca","said"]],
    0: [["कथम्","katham","how"],["भीष्मम्","bhīṣmam","Bhīṣma"],["अहम्","aham","I"],
        ["सङ्ख्ये","saṅkhye","in battle"]],
    1: [["द्रोणम्","droṇam","Droṇa"],["च","ca","and"],["मधुसूदन","madhusūdana","O Madhusūdana"]],
    2: [["इषुभिः","iṣubhiḥ","with arrows"],["प्रतियोत्स्यामि","pratiyotsyāmi","shall I fight against"]],
    3: [["पूजार्हौ","pūjārhau","worthy of worship"],["अरिसूदन","arisūdana","O slayer of enemies"]]},

5: {"s": [],
    0: [["गुरून्","gurūn","the teachers"],["अहत्वा","ahatvā","not having slain"],
        ["हि","hi","indeed"],["महानुभावान्","mahānubhāvān","the noble-minded"]],
    1: [["श्रेयः","śreyaḥ","better"],["भोक्तुम्","bhoktum","to live on"],
        ["भैक्षम्","bhaikṣam","alms"],["अपि","api","even"],["इह","iha","in this"],
        ["लोके","loke","world"]],
    2: [["हत्वा","hatvā","having slain"],["अर्थ","artha","for wealth"],["कामान्","kāmān","and desires"],
        ["तु","tu","indeed"],["गुरून्","gurūn","the teachers"],["इह","iha","here"],
        ["एव","eva","indeed"]],
    3: [["भुञ्जीय","bhuñjīya","I would enjoy"],["भोगान्","bhogān","pleasures"],
        ["रुधिर","rudhira","with blood"],["प्रदिग्धान्","pradigdhān","smeared"]]},

6: {"s": [],
    0: [["न","na","not"],["च","ca","and"],["एतत्","etat","this"],["विद्मः","vidmaḥ","we know"],
        ["कतरत्","katarat","which"],["नः","naḥ","for us"],["गरीयः","garīyaḥ","better"]],
    1: [["यत् वा","yad vā","whether"],["जयेम","jayema","we should conquer"],
        ["यदि","yadi","if"],["वा","vā","or"],["नः","naḥ","we"],["जयेयुः","jayeyuḥ","they should conquer"]],
    2: [["यान्","yān","whom"],["एव","eva","indeed"],["हत्वा","hatvā","having slain"],
        ["न","na","not"],["जिजीविषामः","jijīviṣāmaḥ","we would wish to live"]],
    3: [["ते","te","they"],["अवस्थिताः","avasthitāḥ","stand"],["प्रमुखे","pramukhe","in front"],
        ["धार्तराष्ट्राः","dhārtarāṣṭrāḥ","the sons of Dhṛtarāṣṭra"]]},

7: {"s": [],
    0: [["कार्पण्य","kārpaṇya","of weakness"],["दोष","doṣa","the defect"],
        ["उपहत","upahata","overcome"],["स्वभावः","svabhāvaḥ","my nature"]],
    1: [["पृच्छामि","pṛcchāmi","I ask"],["त्वाम्","tvām","you"],
        ["धर्म","dharma","of duty"],["सम्मूढ","sammūḍha","confused"],["चेताः","cetāḥ","mind"]],
    2: [["यत्","yat","what"],["श्रेयः","śreyaḥ","is good"],["स्यात्","syāt","may be"],
        ["निश्चितम्","niścitam","certainly"],["ब्रूहि","brūhi","tell"],["तत्","tat","that"],
        ["मे","me","to me"]],
    3: [["शिष्यः","śiṣyaḥ","a disciple"],["ते","te","your"],["अहम्","aham","I"],
        ["शाधि","śādhi","teach"],["माम्","mām","me"],["त्वाम्","tvām","you"],
        ["प्रपन्नम्","prapannam","I have taken refuge in"]]},

8: {"s": [],
    0: [
    ["न", "na", "not"], ["हि", "hi", "indeed"], ["प्रपश्यामि", "prapaśyāmi", "I see"],
        ["मम", "mama", "my"], ["अपनुद्यात्", "apanudyāt", "would remove"]],
    1: [
    ["यत्", "yat", "which"], ["शोकम्", "śokam", "grief"],
        ["उच्छोषणम्", "ucchoṣaṇam", "drying up"],
        ["इन्द्रियाणाम्", "indriyāṇām", "of the senses"]],
    2: [
    ["अवाप्य", "avāpya", "having obtained"], ["भूमौ", "bhūmau", "on earth"],
        ["असपत्नम्", "asapatnam", "without a rival"], ["ऋद्धम्", "ṛddham", "prosperous"]],
    3: [
    ["राज्यम्", "rājyam", "kingdom"], ["सुराणाम्", "surāṇām", "of the gods"],
        ["अपि", "api", "even"], ["च", "ca", "and"],
        ["आधिपत्यम्", "ādhipatyam", "lordship"]]
},
9: {"s": [
    ["सञ्जय", "sañjaya", "Sañjaya"],
    ["उवाच", "uvāca", "said"]
],
    0: [
    ["एवम्", "evam", "thus"], ["उक्त्वा", "uktvā", "having spoken"],
        ["हृषीकेशम्", "hṛṣīkeśam", "to Hṛṣīkeśa (Kṛṣṇa)"]],
    1: [
    ["गुडाकेशः", "guḍākeśaḥ", "Guḍākeśa (Arjuna)"],
        ["परन्तप", "parantapa", "O scorcher of foes"]],
    2: [
    ["न", "na", "not"], ["योत्स्ये", "yotsye", "I will fight"], ["इति", "iti", "thus"],
        ["गोविन्दम्", "govindam", "to Govinda (Kṛṣṇa)"]],
    3: [
    ["उक्त्वा", "uktvā", "having said"], ["तूष्णीम्", "tūṣṇīm", "silent"],
        ["बभूव", "babhūva", "became"], ["ह", "ha", "indeed"]]
},
10: {"s": [],
    0: [
    ["तम्", "tam", "him"], ["उवाच", "uvāca", "spoke to"],
        ["हृषीकेशः", "hṛṣīkeśaḥ", "Hṛṣīkeśa"]],
    1: [
    ["प्रहसन्", "prahasan", "smiling"], ["इव", "iva", "as if"],
        ["भारत", "bhārata", "O descendant of Bharata"]],
    2: [
    ["सेनयोः", "senayoḥ", "of the two armies"], ["उभयोः", "ubhayoḥ", "of both"],
        ["मध्ये", "madhye", "in the midst"]],
    3: [
    ["विषीदन्तम्", "viṣīdantam", "the grieving one"], ["इदम्", "idam", "this"],
        ["वचः", "vacaḥ", "speech"]]
},
11: {"s": [["श्रीभगवान्","śrībhagavān","the Blessed Lord"],["उवाच","uvāca","said"]],
    0: [["अशोच्यान्","aśocyān","those not to be grieved for"],["अन्वशोचः","anvaśocaḥ","you grieve"],
        ["त्वम्","tvam","you"]],
    1: [["प्रज्ञावादान्","prajñāvādān","words of wisdom"],["च","ca","and"],["भाषसे","bhāṣase","you speak"]],
    2: [["गतासून्","gatāsūn","the dead"],["अगतासून्","agatāsūn","the living"],["च","ca","and"]],
    3: [["न","na","not"],["अनुशोचन्ति","anuśocanti","they grieve"],["पण्डिताः","paṇḍitāḥ","the wise"]]},

12: {"s": [],
    0: [["न","na","not"],["त्वेव","tveva","indeed"],["अहम्","aham","I"],["जातु","jātu","ever"],
        ["न","na","not"],["आसम्","āsam","did exist"]],
    1: [["न","na","not"],["त्वम्","tvam","you"],["न","na","nor"],["इमे","ime","these"],
        ["जनाधिपाः","janādhipāḥ","rulers of men"]],
    2: [["न","na","not"],["च","ca","and"],["एव","eva","indeed"],["न","na","not"],
        ["भविष्यामः","bhaviṣyāmaḥ","shall we exist"]],
    3: [["सर्वे","sarve","all"],["वयम्","vayam","we"],["अतः","ataḥ","from now"],
        ["परम्","param","hereafter"]]},

13: {"s": [],
    0: [["देहिनः","dehinaḥ","of the embodied one"],["अस्मिन्","asmin","in this"],
        ["यथा","yathā","as"],["देहे","dehe","in the body"]],
    1: [["कौमारम्","kaumāram","childhood"],["यौवनम्","yauvanam","youth"],["जरा","jarā","old age"]],
    2: [["तथा","tathā","so"],["देहान्तर","dehāntara","another body"],
        ["प्राप्तिः","prāptiḥ","the obtaining"]],
    3: [["धीरः","dhīraḥ","the wise one"],["तत्र","tatra","therein"],
        ["न","na","not"],["मुह्यति","muhyati","is deluded"]]},

14: {"s": [],
    0: [["मात्रा","mātrā","sense-objects"],["स्पर्शाः","sparśāḥ","contacts"],
        ["तु","tu","indeed"],["कौन्तेय","kaunteya","O son of Kuntī"]],
    1: [["शीत","śīta","cold"],["उष्ण","uṣṇa","heat"],["सुख","sukha","pleasure"],
        ["दुःख","duḥkha","pain"],["दाः","dāḥ","giving"]],
    2: [["आगम","āgama","coming"],["आपायिनः","apāyinaḥ","going"],
        ["अनित्याः","anityāḥ","impermanent"]],
    3: [["तान्","tān","them"],["तितिक्षस्व","titikṣasva","endure"],
        ["भारत","bhārata","O Bhārata"]]},

15: {"s": [],
    0: [["यम्","yam","whom"],["हि","hi","indeed"],["न","na","not"],
        ["व्यथयन्ति","vyathayanti","disturb"],["एते","ete","these"]],
    1: [["पुरुषम्","puruṣam","the person"],["पुरुषर्षभ","puruṣarṣabha","O bull among men"]],
    2: [["सम","sama","equal"],["दुःख","duḥkha","in pain"],["सुखम्","sukham","and pleasure"],
        ["धीरम्","dhīram","the wise"]],
    3: [["सः","saḥ","that one"],["अमृतत्वाय","amṛtatvāya","for immortality"],
        ["कल्पते","kalpate","is fit"]]},

16: {"s": [],
    0: [["न","na","not"],["असतः","asataḥ","of the unreal"],["विद्यते","vidyate","is"],
        ["भावः","bhāvaḥ","being"]],
    1: [["न","na","not"],["अभावः","abhāvaḥ","non-being"],["विद्यते","vidyate","is"],
        ["सतः","sataḥ","of the real"]],
    2: [["उभयोः","ubhayoḥ","of both"],["अपि","api","indeed"],["दृष्टः","dṛṣṭaḥ","seen"],
        ["अन्तः","antaḥ","the end"]],
    3: [["त्वनयोः","tvanayoḥ","of these two"],["तत्त्वदर्शिभिः","tattvadarśibhiḥ","by the seers of truth"]]},

17: {"s": [],
    0: [["अविनाशि","avināśi","imperishable"],["तु","tu","indeed"],["तत्","tat","that"],
        ["विद्धि","viddhi","know"]],
    1: [["येन","yena","by which"],["सर्वम्","sarvam","all"],["इदम्","idam","this"],
        ["ततम्","tatam","pervaded"]],
    2: [["विनाशम्","vināśam","destruction"],["अव्ययस्य","avyayasya","of the inexhaustible"],
        ["अस्य","asya","this"]],
    3: [["न","na","not"],["कश्चित्","kaścit","anyone"],["कर्तुम्","kartum","to bring about"],
        ["अर्हति","arhati","is able"]]},

18: {"s": [],
    0: [["अन्तवन्तः","antavantaḥ","having an end"],["इमे","ime","these"],["देहाः","dehāḥ","bodies"]],
    1: [["नित्यस्य","nityasya","of the eternal"],["उक्ताः","uktāḥ","are said"],
        ["शरीरिणः","śarīriṇaḥ","of the embodied"]],
    2: [["अनाशिनः","anāśinaḥ","of the indestructible"],["अप्रमेयस्य","aprameyasya","of the immeasurable"]],
    3: [["तस्मात्","tasmāt","therefore"],["युध्यस्व","yudhyasva","fight"],
        ["भारत","bhārata","O Bhārata"]]},

19: {"s": [],
    0: [["यः","yaḥ","who"],["एनम्","enam","this (Self)"],["वेत्ति","vetti","knows"],
        ["हन्तारम्","hantāram","the killer"]],
    1: [["यः","yaḥ","who"],["च","ca","and"],["एनम्","enam","this"],
        ["मन्यते","manyate","thinks"],["हतम्","hatam","killed"]],
    2: [["उभौ","ubhau","both"],["तौ","tau","those"],["न","na","not"],
        ["विजानीतः","vijānītaḥ","know"]],
    3: [["नायम्","nāyam","this one does not"],["हन्ति","hanti","kill"],
        ["न","na","nor"],["हन्यते","hanyate","is killed"]]},

20: {"s": [],
    0: [["न","na","not"],["जायते","jāyate","is born"],["म्रियते","mriyate","dies"],
        ["वा","vā","or"],["कदाचित्","kadācit","ever"]],
    1: [["नायम्","nāyam","this one is not"],["भूत्वा","bhūtvā","having been"],
        ["भविता","bhavitā","will be"],["वा","vā","or"],["न","na","not"],
        ["भूयः","bhūyaḥ","again"]],
    2: [["अजः","ajaḥ","unborn"],["नित्यः","nityaḥ","eternal"],["शाश्वतः","śāśvataḥ","everlasting"],
        ["अयम्","ayam","this"],["पुराणः","purāṇaḥ","ancient"]],
    3: [["न","na","not"],["हन्यते","hanyate","is killed"],["हन्यमाने","hanyamāne","when killed"],
        ["शरीरे","śarīre","the body"]]},

21: {"s": [],
    0: [["वेद","veda","knows"],["अविनाशिनम्","avināśinam","the imperishable"],
        ["नित्यम्","nityam","eternal"]],
    1: [["यः","yaḥ","who"],["एनम्","enam","this"],["अजम्","ajam","unborn"],
        ["अव्ययम्","avyayam","inexhaustible"]],
    2: [["कथम्","katham","how"],["सः","saḥ","that"],["पुरुषः","puruṣaḥ","person"],
        ["पार्थ","pārtha","O Pārtha"]],
    3: [["कम्","kam","whom"],["घातयति","ghātayati","causes to kill"],
        ["हन्ति","hanti","kills"],["कम्","kam","whom"]]},

22: {"s": [],
    0: [
    ["वासांसि", "vāsāṁsi", "garments"], ["जीर्णानि", "jīrṇāni", "worn out"],
        ["यथा", "yathā", "as"], ["विहाय", "vihāya", "having cast off"]],
    1: [
    ["नवानि", "navāni", "new"], ["गृह्णाति", "gṛhṇāti", "takes"],
        ["नरः", "naraḥ", "a man"], ["अपराणि", "aparāṇi", "others"]],
    2: [
    ["तथा", "tathā", "so"], ["शरीराणि", "śarīrāṇi", "bodies"],
        ["विहाय", "vihāya", "having cast off"], ["जीर्णानि", "jīrṇāni", "worn out"]],
    3: [
    ["अन्यानि", "anyāni", "other"], ["संयाति", "saṁyāti", "goes to"],
        ["नवानि", "navāni", "new"], ["देही", "dehī", "the embodied one"]]
},
23: {"s": [],
    0: [["न","na","not"],["एनम्","enam","this"],["छिन्दन्ति","chindanti","cut"],
        ["शस्त्राणि","śastrāṇi","weapons"]],
    1: [["न","na","not"],["एनम्","enam","this"],["दहति","dahati","burns"],
        ["पावकः","pāvakaḥ","fire"]],
    2: [["न","na","not"],["च","ca","and"],["एनम्","enam","this"],
        ["क्लेदयन्ति","kledayanti","wet"],["आपः","āpaḥ","waters"]],
    3: [["न","na","not"],["शोषयति","śoṣayati","dries"],["मारुतः","mārutaḥ","the wind"]]},

24: {"s": [],
    0: [["अच्छेद्यः","acchedyaḥ","uncuttable"],["अयम्","ayam","this"],["अदाह्यः","adāhyaḥ","unburnable"],
        ["अयम्","ayam","this"]],
    1: [["अक्लेद्यः","akledyaḥ","unwettable"],["अशोष्यः","aśoṣyaḥ","undryable"],
        ["एव","eva","indeed"],["च","ca","and"]],
    2: [["नित्यः","nityaḥ","eternal"],["सर्वगतः","sarvagataḥ","all-pervading"],
        ["स्थाणुः","sthāṇuḥ","fixed"]],
    3: [["अचलः","acalaḥ","immovable"],["अयम्","ayam","this"],["सनातनः","sanātanaḥ","everlasting"]]},

25: {"s": [],
    0: [["अव्यक्तः","avyaktaḥ","unmanifest"],["अयम्","ayam","this"],["अचिन्त्यः","acintyaḥ","unthinkable"],
        ["अयम्","ayam","this"]],
    1: [["अविकार्यः","avikāryaḥ","unchanging"],["अयम्","ayam","this"],["उच्यते","ucyate","is said"]],
    2: [["तस्मात्","tasmāt","therefore"],["एवम्","evam","thus"],["विदित्वा","viditvā","having known"],
        ["एनम्","enam","this"]],
    3: [["न","na","not"],["अनुशोचितुम्","anuśocitum","to grieve"],
        ["अर्हसि","arhasi","you ought"]]},

26: {"s": [],
    0: [["अथ","atha","but"],["च","ca","and"],["एनम्","enam","this"],
        ["नित्यजातम्","nityajātam","ever-born"]],
    1: [["नित्यम्","nityam","always"],["वा","vā","or"],["मन्यसे","manyase","you think"],
        ["मृतम्","mṛtam","dead"]],
    2: [["तथापि","tathāpi","even then"],["त्वम्","tvam","you"],["महाबाहो","mahābāho","O mighty-armed one"]],
    3: [["न","na","not"],["एवम्","evam","thus"],["शोचितुम्","śocitum","to grieve"],
        ["अर्हसि","arhasi","you ought"]]},

27: {"s": [],
    0: [["जातस्य","jātasya","of the born"],["हि","hi","indeed"],["ध्रुवः","dhruvaḥ","certain"],
        ["मृत्युः","mṛtyuḥ","death"]],
    1: [["ध्रुवम्","dhruvam","certain"],["जन्म","janma","birth"],["मृतस्य","mṛtasya","of the dead"],
        ["च","ca","and"]],
    2: [["तस्मात्","tasmāt","therefore"],["अपरिहार्ये","aparihārye","in the unavoidable"],
        ["अर्थे","arthe","matter"]],
    3: [["न","na","not"],["त्वम्","tvam","you"],["शोचितुम्","śocitum","to grieve"],
        ["अर्हसि","arhasi","you ought"]]},

28: {"s": [],
    0: [["अव्यक्त","avyakta","unmanifest"],["आदीनि","ādīni","beginning with"],
        ["भूतानि","bhūtāni","beings"]],
    1: [["व्यक्त","vyakta","manifest"],["मध्यानि","madhyāni","in the middle"],
        ["भारत","bhārata","O Bhārata"]],
    2: [["अव्यक्त","avyakta","unmanifest"],["निधनानि","nidhanāni","ending in"],
        ["एव","eva","indeed"]],
    3: [["तत्र","tatra","therein"],["का","kā","what"],["परिदेवना","paridevanā","lamentation"]]},

29: {"s": [],
    0: [["आश्चर्यवत्","āścaryavat","as a wonder"],["पश्यति","paśyati","sees"],
        ["कश्चित्","kaścit","someone"],["एनम्","enam","this (Self)"]],
    1: [["आश्चर्यवत्","āścaryavat","as a wonder"],["वदति","vadati","speaks of"],
        ["तथा","tathā","thus"],["एव","eva","indeed"],["च","ca","and"],["अन्यः","anyaḥ","another"]],
    2: [["आश्चर्यवत्","āścaryavat","as a wonder"],["च","ca","and"],["एनम्","enam","this"],
        ["अन्यः","anyaḥ","another"],["शृणोति","śṛṇoti","hears"]],
    3: [["श्रुत्वा","śrutvā","having heard"],["अपि","api","even"],["एनम्","enam","this"],
        ["वेद","veda","knows"],["न","na","not"],["च","ca","and"],["एव","eva","indeed"],
        ["कश्चित्","kaścit","anyone"]]},

30: {"s": [],
    0: [["देही","dehī","the embodied one"],["नित्यम्","nityam","always"],
        ["अवध्यः","avadhyaḥ","inviolable"],["अयम्","ayam","this"]],
    1: [["देहे","dehe","in the body"],["सर्वस्य","sarvasya","of everyone"],
        ["भारत","bhārata","O Bhārata"]],
    2: [["तस्मात्","tasmāt","therefore"],["सर्वाणि","sarvāṇi","all"],
        ["भूतानि","bhūtāni","beings"]],
    3: [["न","na","not"],["त्वम्","tvam","you"],["शोचितुम्","śocitum","to grieve"],
        ["अर्हसि","arhasi","you ought"]]},

31: {"s": [],
    0: [["स्वधर्मम्","svadharmam","your own duty"],["अपि","api","also"],["च","ca","and"],
        ["अवेक्ष्य","avekṣya","considering"]],
    1: [["न","na","not"],["विकम्पितुम्","vikampitum","to waver"],
        ["अर्हसि","arhasi","you ought"]],
    2: [["धर्म्यात्","dharmyāt","than the righteous"],["हि","hi","indeed"],
        ["युद्धात्","yuddhāt","than war"],["श्रेयः","śreyaḥ","better"],
        ["अन्यत्","anyat","other"]],
    3: [["क्षत्रियस्य","kṣatriyasya","of a warrior"],["न","na","not"],
        ["विद्यते","vidyate","is there"]]},

32: {"s": [],
    0: [["यदृच्छया","yadṛcchayā","of its own accord"],["च","ca","and"],["उपपन्नम्","upapannam","come"]],
    1: [["स्वर्गद्वारम्","svargadvāram","the door of heaven"],["अपावृतम्","apāvṛtam","open"]],
    2: [["सुखिनः","sukhinaḥ","happy"],["क्षत्रियाः","kṣatriyāḥ","the warriors"],
        ["पार्थ","pārtha","O Pārtha"]],
    3: [["लभन्ते","labhante","they obtain"],["युद्धम्","yuddham","war"],
        ["ईदृशम्","īdṛśam","such"]]},

33: {"s": [],
    0: [["अथ","atha","but"],["चेत्","cet","if"],["त्वम्","tvam","you"],
        ["इमम्","imam","this"],["धर्म्यम्","dharmyam","righteous"]],
    1: [["सङ्ग्रामम्","saṅgrāmam","war"],["न","na","not"],["करिष्यसि","kariṣyasi","you will wage"]],
    2: [["ततः","tataḥ","then"],["स्वधर्मम्","svadharmam","your own duty"],
        ["कीर्तिम्","kīrtim","glory"],["च","ca","and"]],
    3: [["हित्वा","hitvā","having abandoned"],["पापम्","pāpam","sin"],["अवाप्स्यसि","avāpsyasi","you will incur"]]},
34: {"s": [],
    0: [
    ["अकीर्तिम्", "akīrtim", "disgrace"], ["च", "ca", "and"], ["अपि", "api", "also"],
        ["भूतानि", "bhūtāni", "people"]],
    1: [
    ["कथयिष्यन्ति", "kathayiṣyanti", "will speak of"], ["ते", "te", "your"],
        ["अव्ययाम्", "avyayām", "everlasting"]],
    2: [
    ["सम्भावितस्य", "sambhāvitasya", "of one held in honour"], ["च", "ca", "and"],
        ["अकीर्तिः", "akīrtiḥ", "dishonour"]],
    3: [
    ["मरणात्", "maraṇāt", "than death"], ["अतिरिच्यते", "atiricyate", "is greater"]]
},
35: {"s": [],
    0: [["भयात्","bhayāt","from fear"],["रणात्","raṇāt","from battle"],
        ["उपरतम्","uparatam","retreated"]],
    1: [["मंस्यन्ते","maṁsyante","they will think"],["त्वाम्","tvām","you"],
        ["महारथाः","mahārathāḥ","the great warriors"]],
    2: [["येषाम्","yeṣām","by whom"],["च","ca","and"],["त्वम्","tvam","you"],
        ["बहुमतः","bahumataḥ","highly regarded"]],
    3: [["भूत्वा","bhūtvā","having been"],["यास्यसि","yāsyasi","you will go to"],
        ["लाघवम्","lāghavam","triviality"]]},

36: {"s": [],
    0: [
    ["अवाच्य", "avācya", "unutterable"], ["वादान्", "vādān", "words"], ["च", "ca", "and"],
        ["बहून्", "bahūn", "many"]],
    1: [
    ["वदिष्यन्ति", "vadiṣyanti", "they will speak"], ["तव", "tava", "your"],
        ["अहिताः", "ahitāḥ", "enemies"]],
    2: [
    ["निन्दन्तः", "nindantaḥ", "slandering"], ["तव", "tava", "your"],
        ["सामर्थ्यम्", "sāmarthyam", "ability"]],
    3: [
    ["ततः", "tataḥ", "than that"], ["दुःखतरम्", "duḥkhataram", "more painful"],
        ["नु", "nu", "indeed"], ["किम्", "kim", "what"]]
},
37: {"s": [],
    0: [["हतः","hataḥ","slain"],["वा","vā","or"],["प्राप्स्यसि","prāpsyasi","you will obtain"],
        ["स्वर्गम्","svargam","heaven"]],
    1: [["जित्वा","jitvā","having conquered"],["वा","vā","or"],["भोक्ष्यसे","bhokṣyase","you will enjoy"],
        ["महीम्","mahīm","the earth"]],
    2: [["तस्मात्","tasmāt","therefore"],["उत्तिष्ठ","uttiṣṭha","arise"],
        ["कौन्तेय","kaunteya","O son of Kuntī"]],
    3: [["युद्धाय","yuddhāya","for battle"],["कृतनिश्चयः","kṛtaniścayaḥ","resolved"]]},

38: {"s": [],
    0: [["सुख","sukha","pleasure"],["दुःखे","duḥkhe","pain"],["समे","same","equal"],
        ["कृत्वा","kṛtvā","having made"]],
    1: [["लाभ","lābha","gain"],["अलाभौ","alābhau","and loss"],["जय","jaya","victory"],
        ["अजयौ","ajayau","and defeat"]],
    2: [["ततः","tataḥ","then"],["युद्धाय","yuddhāya","for battle"],
        ["युज्यस्व","yujyasva","engage"]],
    3: [["न","na","not"],["एवम्","evam","thus"],["पापम्","pāpam","sin"],
        ["अवाप्स्यसि","avāpsyasi","you will incur"]]},

39: {"s": [],
    0: [["एषा","eṣā","this"],["ते","te","to you"],["अभिहिता","abhihitā","declared"],
        ["साङ्ख्ये","sāṅkhye","in sāṅkhya"]],
    1: [["बुद्धिः","buddhiḥ","the wisdom"],["योगे","yoge","in yoga"],["त्व्","tv","but"],
        ["इमाम्","imām","this"],["शृणु","śṛṇu","hear"]],
    2: [["बुद्ध्या","buddhyā","with this intellect"],["युक्तः","yuktaḥ","joined"],
        ["यया","yayā","by which"],["पार्थ","pārtha","O Pārtha"]],
    3: [["कर्मबन्धम्","karmabandham","the bondage of action"],
        ["प्रहास्यसि","prahāsyasi","you will cast off"]]},

40: {"s": [],
    0: [["नेह","neha","not here"],["अभिक्रम","abhikrama","effort"],["नाशः","nāśaḥ","loss"],
        ["अस्ति","asti","is"]],
    1: [["प्रत्यवायः","pratyavāyaḥ","contrary result"],["न","na","not"],
        ["विद्यते","vidyate","is"]],
    2: [["स्वल्पम्","svalpam","a little"],["अपि","api","even"],["अस्य","asya","of this"],
        ["धर्मस्य","dharmasya","of this practice"]],
    3: [["त्रायते","trāyate","protects"],["महतः","mahataḥ","from great"],
        ["भयात्","bhayāt","fear"]]},

41: {"s": [],
    0: [
    ["व्यवसायात्मिका", "vyavasāyātmikā", "resolute"],
        ["बुद्धिः", "buddhiḥ", "the intellect"]],
    1: [
    ["एकेह", "ekeha", "single, here"], ["कुरुनन्दन", "kurunandana", "O joy of the Kurus"]],
    2: [
    ["बहुशाखाः", "bahuśākhāḥ", "many-branched"], ["हि", "hi", "indeed"],
        ["अनन्ताः", "anantāḥ", "endless"], ["च", "ca", "and"]],
    3: [
    ["बुद्धयः", "buddhayaḥ", "the intellects"],
        ["अव्यवसायिनाम्", "avyavasāyinām", "of the irresolute"]]
},
42: {"s": [],
    0: [["याम्","yām","which"],["इमाम्","imām","this"],["पुष्पिताम्","puṣpitām","flowery"],
        ["वाचम्","vācam","speech"]],
    1: [["प्रवदन्ति","pravadanti","they proclaim"],["अविपश्चितः","avipaścitaḥ","the unwise"]],
    2: [["वेदवादरताः","vedavādaratāḥ","delighting in Vedic words"],
        ["पार्थ","pārtha","O Pārtha"]],
    3: [["न","na","not"],["अन्यत्","anyat","other"],["अस्ति","asti","is"],
        ["इति","iti","thus"],["वादिनः","vādinaḥ","proclaiming"]]},

43: {"s": [],
    0: [["कामात्मानः","kāmātmānaḥ","desire-filled"],["स्वर्गपराः","svargaparāḥ","heaven-seeking"]],
    1: [["जन्म","janma","birth"],["कर्म","karma","and action"],["फल","phala","result"],
        ["प्रदाम्","pradām","giving"]],
    2: [["क्रिया","kriyā","ritual"],["विशेष","viśeṣa","many kinds"],["बहुलाम्","bahulām","abundant"]],
    3: [["भोग","bhoga","pleasure"],["ऐश्वर्य","aiśvarya","and power"],["गतिम्","gatim","leading to"],
        ["प्रति","prati","toward"]]},

44: {"s": [],
    0: [["भोग","bhoga","pleasure"],["ऐश्वर्य","aiśvarya","power"],["प्रसक्तानाम्","prasaktānām","of those attached"]],
    1: [["तया","tayā","by that"],["अपहृत","apahṛta","carried away"],["चेतसाम्","cetasām","of whose minds"]],
    2: [["व्यवसायात्मिका","vyavasāyātmikā","resolute"],["बुद्धिः","buddhiḥ","the intellect"]],
    3: [["समाधौ","samādhau","in absorption"],["न","na","not"],["विधीयते","vidhīyate","is established"]]},

45: {"s": [],
    0: [["त्रैगुण्य","traiguṇya","the three qualities"],["विषयाः","viṣayāḥ","dealing with"],
        ["वेदाः","vedāḥ","the Vedas"]],
    1: [["निस्त्रैगुण्यः","nistraiguṇyaḥ","beyond the three qualities"],["भव","bhava","be"],
        ["अर्जुन","arjuna","O Arjuna"]],
    2: [["निर्द्वन्द्वः","nirdvandvaḥ","free from duality"],["नित्यसत्त्वस्थः","nityasattvasthaḥ","ever established in sattva"]],
    3: [["निर्योगक्षेमः","niryogakṣemaḥ","free from gain and keeping"],
        ["आत्मवान्","ātmavān","self-possessed"]]},

46: {"s": [],
    0: [["यावान्","yāvān","as much"],["अर्थः","arthaḥ","use"],["उदपाने","udapāne","in a well"]],
    1: [["सर्वतः","sarvataḥ","everywhere"],["सम्प्लुतोदके","samplutodake","in a flooded water"]],
    2: [["तावान्","tāvān","so much"],["सर्वेषु","sarveṣu","in all"],
        ["वेदेषु","vedeṣu","the Vedas"]],
    3: [["ब्राह्मणस्य","brāhmaṇasya","of the brāhmaṇa"],["विजानतः","vijānataḥ","of the knowing"]]},

47: {"s": [],
    0: [
    ["कर्मणि", "karmaṇi", "in action"], ["एव", "eva", "indeed"],
        ["अधिकारः", "adhikāraḥ", "the right"], ["ते", "te", "your"]],
    1: [
    ["मा", "mā", "not"], ["फलेषु", "phaleṣu", "in the fruits"],
        ["कदाचन", "kadācana", "ever"]],
    2: [
    ["मा", "mā", "not"], ["कर्मफल", "karmaphala", "of the fruit of action"],
        ["हेतुः", "hetuḥ", "the motive"], ["भूः", "bhūḥ", "be"], ["मा", "mā", "not"]],
    3: [
    ["ते", "te", "your"], ["सङ्गः", "saṅgaḥ", "attachment"], ["अस्तु", "astu", "let be"],
        ["अकर्मणि", "akarmaṇi", "in inaction"]]
},
48: {"s": [],
    0: [["योगस्थः","yogasthaḥ","established in yoga"],["कुरु","kuru","perform"],
        ["कर्माणि","karmāṇi","actions"]],
    1: [["सङ्गम्","saṅgam","attachment"],["त्यक्त्वा","tyaktvā","having abandoned"],
        ["धनञ्जय","dhanañjaya","O Dhanañjaya"]],
    2: [["सिद्ध्यसिद्ध्योः","siddhyasiddhyoḥ","in success and failure"],
        ["समः","samaḥ","equal"],["भूत्वा","bhūtvā","having become"]],
    3: [["समत्वम्","samatvam","evenness"],["योगः","yogaḥ","yoga"],
        ["उच्यते","ucyate","is called"]]},

49: {"s": [],
    0: [["दूरेण","dūreṇa","far"],["हि","hi","indeed"],["अवरम्","avaram","inferior"],
        ["कर्म","karma","action"]],
    1: [["बुद्धियोगात्","buddhiyogāt","than the yoga of discernment"],
        ["धनञ्जय","dhanañjaya","O Dhanañjaya"]],
    2: [["बुद्धौ","buddhau","in the intellect"],["शरणम्","śaraṇam","refuge"],
        ["अन्विच्छ","anviccha","seek"]],
    3: [["कृपणाः","kṛpaṇāḥ","pitiable"],["फलहेतवः","phalahetavaḥ","motive-seeking"]]},

50: {"s": [],
    0: [
    ["बुद्धियुक्तः", "buddhiyuktaḥ", "joined to the intellect"],
        ["जहाति", "jahāti", "leaves"], ["इह", "iha", "here"]],
    1: [
    ["उभे", "ubhe", "both"], ["सुकृत", "sukṛta", "good"],
        ["दुष्कृते", "duṣkṛte", "and bad deeds"]],
    2: [
    ["तस्मात्", "tasmāt", "therefore"], ["योगाय", "yogāya", "to yoga"],
        ["युज्यस्व", "yujyasva", "devote yourself"]],
    3: [
    ["योगः", "yogaḥ", "yoga"], ["कर्मसु", "karmasu", "in actions"],
        ["कौशलम्", "kauśalam", "skill"]]
},
51: {"s": [],
    0: [
    ["कर्मजम्", "karmajam", "born of action"],
        ["बुद्धियुक्ताः", "buddhiyuktāḥ", "joined to the intellect"],
        ["हि", "hi", "indeed"]],
    1: [
    ["फलम्", "phalam", "the fruit"], ["त्यक्त्वा", "tyaktvā", "having renounced"],
        ["मनीषिणः", "manīṣiṇaḥ", "the wise"]],
    2: [
    ["जन्मबन्ध", "janmabandha", "of the bond of birth"],
        ["विनिर्मुक्ताः", "vinirmuktāḥ", "freed"]],
    3: [
    ["पदम्", "padam", "the state"], ["गच्छन्ति", "gacchanti", "they reach"],
        ["अनामयम्", "anāmayam", "beyond all ill"]]
},
52: {"s": [],
    0: [
    ["यदा", "yadā", "when"], ["ते", "te", "your"],
        ["मोहकलिलम्", "mohakalilam", "the mire of delusion"]],
    1: [
    ["बुद्धिः", "buddhiḥ", "the intellect"],
        ["व्यतितरिष्यति", "vyatitariṣyati", "will cross beyond"]],
    2: [
    ["तदा", "tadā", "then"], ["गन्तासि", "gantāsi", "you will go to"],
        ["निर्वेदम्", "nirvedam", "indifference"]],
    3: [
    ["श्रोतव्यस्य", "śrotavyasya", "of what is to be heard"],
        ["श्रुतस्य", "śrutasya", "of what is heard"], ["च", "ca", "and"]]
},
53: {"s": [],
    0: [["श्रुति","śruti","of scripture"],["विप्रतिपन्ना","vipratipannā","bewildered"],
        ["ते","te","your"]],
    1: [["यदा","yadā","when"],["स्थास्यति","sthāsyati","will stand"],
        ["निश्चला","niścalā","unmoved"]],
    2: [["समाधौ","samādhau","in absorption"],["अचला","acalā","motionless"],
        ["बुद्धिः","buddhiḥ","the intellect"]],
    3: [["तदा","tadā","then"],["योगम्","yogam","yoga"],["अवाप्स्यसि","avāpsyasi","you will attain"]]},

54: {"s": [["अर्जुन","arjuna","Arjuna"],["उवाच","uvāca","said"]],
    0: [["स्थितप्रज्ञस्य","sthitaprajñasya","of the steady-wisdom"],["का","kā","what"],
        ["भाषा","bhāṣā","description"]],
    1: [["समाधिस्थस्य","samādhisthasya","of one established in samādhi"],
        ["केशव","keśava","O Keśava"]],
    2: [["स्थितधीः","sthitadhīḥ","the steady-minded"],["किम्","kim","what"],
        ["प्रभाषेत","prabhāṣeta","would speak"]],
    3: [["किम्","kim","how"],["आसीत","āsīta","would sit"],["व्रजेत","vrajeta","would move"],
        ["किम्","kim","how"]]},

55: {"s": [
    ["श्रीभगवान्", "śrībhagavān", "the Blessed Lord"],
    ["उवाच", "uvāca", "said"]
],
    0: [
    ["प्रजहाति", "prajahāti", "casts off"], ["यदा", "yadā", "when"],
        ["कामान्", "kāmān", "desires"]],
    1: [
    ["सर्वान्", "sarvān", "all"], ["पार्थ", "pārtha", "O Pārtha"],
        ["मनोगतान्", "manogatān", "in the mind"]],
    2: [
    ["आत्मनि", "ātmani", "in the Self"], ["एव", "eva", "alone"],
        ["आत्मना", "ātmanā", "by the Self"], ["तुष्टः", "tuṣṭaḥ", "content"]],
    3: [
    ["स्थितप्रज्ञः", "sthitaprajñaḥ", "steady in wisdom"], ["तदा", "tadā", "then"],
        ["उच्यते", "ucyate", "is called"]]
},
56: {"s": [],
    0: [["दुःखेषु","duḥkheṣu","in sorrows"],["अनुद्विग्न","anudvigna","untroubled"],
        ["मनाः","manāḥ","mind"]],
    1: [["सुखेषु","sukheṣu","in pleasures"],["विगतस्पृहः","vigataspṛhaḥ","free from longing"]],
    2: [["वीत","vīta","free from"],["राग","rāga","passion"],["भय","bhaya","fear"],
        ["क्रोधः","krodhaḥ","anger"]],
    3: [["स्थितधीः","sthitadhīḥ","steady-minded"],["मुनिः","muniḥ","sage"],
        ["उच्यते","ucyate","is called"]]},

57: {"s": [],
    0: [
    ["यः", "yaḥ", "who"], ["सर्वत्र", "sarvatra", "everywhere"],
        ["अनभिस्नेहः", "anabhisnehaḥ", "without affection"]],
    1: [
    ["तत् तत्", "tat tat", "this and that"], ["प्राप्य", "prāpya", "obtaining"],
        ["शुभ", "śubha", "good"], ["अशुभम्", "aśubham", "and evil"]],
    2: [
    ["न", "na", "not"], ["अभिनन्दति", "abhinandati", "rejoices"], ["न", "na", "not"],
        ["द्वेष्टि", "dveṣṭi", "reviles"]],
    3: [
    ["तस्य", "tasya", "his"], ["प्रज्ञा", "prajñā", "wisdom"],
        ["प्रतिष्ठिता", "pratiṣṭhitā", "is established"]]
},
58: {"s": [],
    0: [["यदा","yadā","when"],["संहरते","saṁharate","draws in"],["च","ca","and"],
        ["अयम्","ayam","this"]],
    1: [["कूर्मः","kūrmaḥ","tortoise"],["अङ्गानि","aṅgāni","limbs"],["इव","iva","like"],
        ["सर्वशः","sarvaśaḥ","from all sides"]],
    2: [["इन्द्रियाणि","indriyāṇi","the senses"],["इन्द्रियार्थेभ्यः","indriyārthebhyaḥ","from the sense objects"]],
    3: [["तस्य","tasya","his"],["प्रज्ञा","prajñā","wisdom"],["प्रतिष्ठिता","pratiṣṭhitā","is established"]]},

59: {"s": [],
    0: [
    ["विषयाः", "viṣayāḥ", "the sense objects"],
        ["विनिवर्तन्ते", "vinivartante", "fall away"]],
    1: [
    ["निराहारस्य", "nirāhārasya", "of the abstaining"],
        ["देहिनः", "dehinaḥ", "of the embodied one"]],
    2: [
    ["रसवर्जम्", "rasavarjam", "except the taste"], ["रसः", "rasaḥ", "the taste"],
        ["अपि", "api", "even"], ["अस्य", "asya", "of him"]],
    3: [
    ["परम्", "param", "the Supreme"], ["दृष्ट्वा", "dṛṣṭvā", "having seen"],
        ["निवर्तते", "nivartate", "departs"]]
},
60: {"s": [],
    0: [["यततः","yatataḥ","of the striving"],["हि","hi","indeed"],["अपि","api","even"],
        ["कौन्तेय","kaunteya","O son of Kuntī"]],
    1: [["पुरुषस्य","puruṣasya","of the person"],["विपश्चितः","vipaścitaḥ","of the wise"]],
    2: [["इन्द्रियाणि","indriyāṇi","the senses"],["प्रमाथीनि","pramāthīni","turbulent"]],
    3: [["हरन्ति","haranti","carry away"],["प्रसभम्","prasabham","by force"],
        ["मनः","manaḥ","the mind"]]},

61: {"s": [],
    0: [["तानि","tāni","them"],["सर्वाणि","sarvāṇi","all"],["संयम्य","saṁyamya","having restrained"]],
    1: [["युक्तः","yuktaḥ","disciplined"],["आसीत","āsīta","should sit"],
        ["मत्परः","matparaḥ","intent on Me"]],
    2: [["वशे","vaśe","in the control"],["हि","hi","indeed"],["यस्य","yasya","of whom"],
        ["इन्द्रियाणि","indriyāṇi","the senses"]],
    3: [["तस्य","tasya","his"],["प्रज्ञा","prajñā","wisdom"],["प्रतिष्ठिता","pratiṣṭhitā","is established"]]},

62: {"s": [],
    0: [["ध्यायतः","dhyāyataḥ","of one brooding"],["विषयान्","viṣayān","on sense objects"],
        ["पुंसः","puṁsaḥ","of a person"]],
    1: [["सङ्गः","saṅgaḥ","attachment"],["तेषु","teṣu","to them"],
        ["उपजायते","upajāyate","arises"]],
    2: [["सङ्गात्","saṅgāt","from attachment"],["सञ्जायते","sañjāyate","is born"],
        ["कामः","kāmaḥ","desire"]],
    3: [["कामात्","kāmāt","from desire"],["क्रोधः","krodhaḥ","anger"],
        ["अभिजायते","abhijāyate","is born"]]},

63: {"s": [],
    0: [["क्रोधात्","krodhāt","from anger"],["भवति","bhavati","comes"],
        ["सम्मोहः","sammohaḥ","delusion"]],
    1: [["सम्मोहात्","sammohāt","from delusion"],["स्मृतिविभ्रमः","smṛtivibhramaḥ","confusion of memory"]],
    2: [["स्मृतिभ्रंशात्","smṛtibhraṁśāt","from broken memory"],["बुद्धिनाशः","buddhināśaḥ","ruin of understanding"]],
    3: [["बुद्धिनाशात्","buddhināśāt","from the ruin of understanding"],
        ["प्रणश्यति","praṇaśyati","one is destroyed"]]},

64: {"s": [],
    0: [["राग","rāga","attachment"],["द्वेष","dveṣa","aversion"],["वियुक्तैः","viyuktaiḥ","free from"],
        ["तु","tu","indeed"]],
    1: [["विषयान्","viṣayān","among objects"],["इन्द्रियैः","indriyaiḥ","with the senses"],
        ["चरन्","caran","moving"]],
    2: [["आत्मवश्यैः","ātmavaśyaiḥ","self-controlled"],["विधेयात्मा","vidheyātmā","the disciplined one"]],
    3: [["प्रसादम्","prasādam","serenity"],["अधिगच्छति","adhigacchati","attains"]]},

65: {"s": [],
    0: [["प्रसादे","prasāde","in serenity"],["सर्व","sarva","of all"],
        ["दुःखानाम्","duḥkhānām","sorrows"]],
    1: [["हानिः","hāniḥ","the destruction"],["अस्य","asya","of him"],["उपजायते","upajāyate","arises"]],
    2: [["प्रसन्नचेतसः","prasannacetasaḥ","of the serene-minded"],["हि","hi","indeed"],
        ["आशु","āśu","quickly"]],
    3: [["बुद्धिः","buddhiḥ","the intellect"],["पर्यवतिष्ठते","paryavatiṣṭhate","is established"]]},

66: {"s": [],
    0: [["न","na","not"],["अस्ति","asti","is"],["बुद्धिः","buddhiḥ","wisdom"],
        ["अयुक्तस्य","ayuktasya","of the undisciplined"]],
    1: [["न","na","not"],["च","ca","and"],["अयुक्तस्य","ayuktasya","of the undisciplined"],
        ["भावना","bhāvanā","meditation"]],
    2: [["न","na","not"],["च","ca","and"],["अभावयतः","abhāvayataḥ","of one without meditation"],
        ["शान्तिः","śāntiḥ","peace"]],
    3: [["अशान्तस्य","aśāntasya","of the peaceless"],["कुतः","kutaḥ","where"],
        ["सुखम्","sukham","happiness"]]},

67: {"s": [],
    0: [["इन्द्रियाणाम्","indriyāṇām","of the senses"],["हि","hi","indeed"],
        ["चरताम्","caratām","wandering"]],
    1: [["यत्","yat","which"],["मनः","manaḥ","the mind"],["अनुविधीयते","anuvidhīyate","follows"]],
    2: [["तत्","tat","that"],["अस्य","asya","of him"],["हरति","harati","carries away"],
        ["प्रज्ञाम्","prajñām","the understanding"]],
    3: [["वायुः","vāyuḥ","the wind"],["नावम्","nāvam","a boat"],["इव","iva","as"],
        ["अम्भसि","ambhasi","on the waters"]]},

68: {"s": [],
    0: [
    ["तस्मात्", "tasmāt", "therefore"], ["यस्य", "yasya", "of whom"],
        ["महाबाहो", "mahābāho", "O mighty-armed one"]],
    1: [
    ["निगृहीतानि", "nigṛhītāni", "restrained"], ["सर्वशः", "sarvaśaḥ", "fully"]],
    2: [
    ["इन्द्रियाणि", "indriyāṇi", "the senses"],
        ["इन्द्रियार्थेभ्यः", "indriyārthebhyaḥ", "from the sense objects"]],
    3: [
    ["तस्य", "tasya", "his"], ["प्रज्ञा", "prajñā", "wisdom"],
        ["प्रतिष्ठिता", "pratiṣṭhitā", "is established"]]
},
69: {"s": [],
    0: [["या","yā","which"],["निशा","niśā","night"],["सर्वभूतानाम्","sarvabhūtānām","of all beings"]],
    1: [["तस्याम्","tasyām","in that"],["जागर्ति","jāgarti","is awake"],
        ["संयमी","saṁyamī","the disciplined one"]],
    2: [["यस्याम्","yasyām","in which"],["जाग्रति","jāgrati","are awake"],
        ["भूतानि","bhūtāni","beings"]],
    3: [["सा","sā","that"],["निशा","niśā","night"],["पश्यतः","paśyataḥ","for the seeing"],
        ["मुनेः","muneḥ","sage"]]},

70: {"s": [],
    0: [["आपूर्यमाणम्","āpūryamāṇam","being filled"],["अचल","acala","unmoved"],
        ["प्रतिष्ठम्","pratiṣṭham","established"]],
    1: [["समुद्रम्","samudram","the ocean"],["आपः","āpaḥ","waters"],
        ["प्रविशन्ति","praviśanti","enter"],["यद्वत्","yadvat","as"]],
    2: [["तद्वत्","tadvat","so"],["कामाः","kāmāḥ","desires"],["यम्","yam","whom"],
        ["प्रविशन्ति","praviśanti","enter"],["सर्वे","sarve","all"]],
    3: [["सः","saḥ","he"],["शान्तिम्","śāntim","peace"],["आप्नोति","āpnoti","attains"],
        ["न","na","not"],["कामकामी","kāmakāmī","the desirer of desires"]]},

71: {"s": [],
    0: [["विहाय","vihāya","having abandoned"],["कामान्","kāmān","desires"],
        ["यः","yaḥ","who"],["सर्वान्","sarvān","all"]],
    1: [["पुमान्","pumān","a person"],["चरति","carati","moves"],["निःस्पृहः","niḥspṛhaḥ","free from longing"]],
    2: [["निर्ममः","nirmamaḥ","without possessiveness"],["निरहङ्कारः","nirahaṅkāraḥ","without ego"]],
    3: [["सः","saḥ","he"],["शान्तिम्","śāntim","peace"],["अधिगच्छति","adhigacchati","attains"]]},

72: {"s": [],
    0: [["एषा","eṣā","this"],["ब्राह्मी","brāhmī","of Brahman"],["स्थितिः","sthitiḥ","the state"],
        ["पार्थ","pārtha","O Pārtha"]],
    1: [["न","na","not"],["एनाम्","enām","this"],["प्राप्य","prāpya","having attained"],
        ["विमुह्यति","vimuhyati","is deluded"]],
    2: [["स्थित्वा","sthitvā","abiding"],["अस्याम्","asyām","in this"],
        ["अन्तकाले","antakāle","at the end-time"],["अपि","api","even"]],
    3: [["ब्रह्मनिर्वाणम्","brahmanirvāṇam","liberation in Brahman"],
        ["ऋच्छति","ṛcchati","attains"]]},
}
