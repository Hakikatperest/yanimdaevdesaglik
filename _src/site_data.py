# -*- coding: utf-8 -*-
"""Yanımda Evde Sağlık — site veri katmanı."""

SITE = {
    "name": "Yanımda Evde Sağlık",
    "legal": "Yanımda Evde Sağlık Hizmetleri",
    "domain": "https://yanimdaevdesaglik.com",
    "phone_display": "0551 844 82 95",
    "phone_tel": "+905518448295",
    "wa": "905518448295",
    "instagram": "https://www.instagram.com/evdesaglikyanimda",
    "hours": "7/24",
    "region": "İstanbul Avrupa Yakası",
    "tagline": "Hemşire ekibimiz kapınızda",
}

# Kullanıcının paylaştığı 3 gerçek konum (Google Haritalar embed pb parametreleri)
BRANCHES = [
    {
        "slug": "beylikduzu",
        "title": "Beylikdüzü",
        "lat": 41.01310584526859, "lng": 28.63295008620971,
        "pb": "!1m18!1m12!1m3!1d3010.5552907102465!2d28.63295008620971!3d41.01310584526859!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14b55f6f04282aa9%3A0xd0639eae5e8cff51!2zWWFuxLFtZGEgRXZkZSBTYcSfbMSxayBcIEJFWUzEsEtEw5xaw5w!5e0!3m2!1str!2str!4v1787307429595!5m2!1str!2str",
    },
    {
        "slug": "esenyurt",
        "title": "Esenyurt",
        "lat": 41.034541943940376, "lng": 28.67465068621654,
        "pb": "!1m18!1m12!1m3!1d3009.5755147077275!2d28.67465068621654!3d41.034541943940376!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14caa10ca8dce07f%3A0xdcdd2110e9693b13!2zWWFuxLFtZGEgZXZkZSBzYcSfbMSxayBoaXptZXRsZXJp!5e0!3m2!1str!2str!4v1787307480539!5m2!1str!2str",
    },
    {
        "slug": "bahcesehir",
        "title": "Bahçeşehir",
        "lat": 41.071857841627505, "lng": 28.65959998622892,
        "pb": "!1m18!1m12!1m3!1d3007.8689186427036!2d28.65959998622892!3d41.071857841627505!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14b5593343a0182d%3A0x5220acaf132e0948!2zWWFuxLFtZGEgRXZkZSBTYcSfbMSxayBcIEJBSMOHRcWeRUjEsFI!5e0!3m2!1str!2str!4v1787307533991!5m2!1str!2str",
    },
]

# --- Sayfa üretilecek ilçeler -------------------------------------------------
DISTRICTS = [
    {"name": "Esenyurt",     "slug": "esenyurt",     "branch": "esenyurt",   "il": "İstanbul"},
    {"name": "Beylikdüzü",   "slug": "beylikduzu",   "branch": "beylikduzu", "il": "İstanbul"},
    {"name": "Avcılar",      "slug": "avcilar",      "branch": "beylikduzu", "il": "İstanbul"},
    {"name": "Büyükçekmece", "slug": "buyukcekmece", "branch": "beylikduzu", "il": "İstanbul"},
    {"name": "Başakşehir",   "slug": "basaksehir",   "branch": "bahcesehir", "il": "İstanbul"},
]

# Sayfa açılmayan ama hizmet verilen bölgeler (anasayfa / bölge listesinde görünür)
EXTRA_AREAS = ["Hadımköy", "Boğazköy", "Silivri", "Çatalca", "Küçükçekmece", "Bahçelievler"]

# Mahalle kaydı olmayan ama aranan semtler
SEMTLER = [
    {"name": "Bahçeşehir", "district": "Başakşehir",   "note": "Bahçeşehir 1. Kısım ve 2. Kısım"},
    {"name": "Kıraç",      "district": "Esenyurt",     "note": "Fatih, Namık Kemal ve çevre mahalleler"},
    {"name": "Beykent",    "district": "Büyükçekmece", "note": "Pınartepe ve çevresi"},
    {"name": "Haramidere", "district": "Esenyurt",     "note": "Sanayi ve Güzelyurt hattı"},
    {"name": "Ispartakule","district": "Başakşehir",   "note": "Bahçeşehir 2. Kısım sınırı"},
    {"name": "Kayaşehir",  "district": "Başakşehir",   "note": "Kayabaşı Mahallesi"},
]

# "evde serum" için de ayrı sayfa açılacak yüksek talepli konumlar
SERUM_LOCATIONS = [
    "Bahçeşehir", "Esenkent", "Kıraç", "Kumburgaz", "Yakuplu", "Gürpınar",
    "Adnan Kahveci", "Kavaklı", "Beykent", "Mimarsinan", "Ambarlı", "Yeşilkent",
    "Başak", "Kayaşehir", "Haramidere", "Mehterçeşme", "Saadetdere", "Cihangir",
]

# --- Hizmetler ----------------------------------------------------------------
SERVICES = [
    {
        "slug": "7-24-evde-saglik",
        "title": "7/24 Evde Sağlık Hizmeti",
        "short": "Gece yarısı da dahil, günün her saati evinize hemşire.",
        "icon": "clock",
        "kw": "7/24 evde sağlık hizmeti",
        "lead": "Hastalık saat gözetmez. Yanımda Evde Sağlık ekibi hafta sonu, resmî tatil ve gece saatleri dahil olmak üzere günün 24 saati Esenyurt, Beylikdüzü, Avcılar, Büyükçekmece ve Başakşehir'de evinize gelir.",
        "sections": [
            ("Hangi durumlarda 7/24 çağrılır?", [
                "Gece bastıran bulantı, kusma ve ishalde sıvı kaybını yerinde durdurmak için",
                "Ateşin yükseldiği, evde ilaçla düşmediği durumlarda",
                "Migren veya şiddetli baş ağrısı krizinde",
                "Hekimin başlattığı antibiyotik/serum tedavisinin gece dozunda",
                "Sonda tıkanması, çıkması gibi bekletilemeyecek durumlarda",
                "Pansumanın kanaması, ıslanması ya da kirlenmesi hâlinde",
            ]),
            ("Çağrıdan sonra ne oluyor?", [
                "Telefonda şikâyet, yaş, kronik hastalık ve kullanılan ilaçlar sorulur",
                "Hekim istemi/reçete varsa fotoğrafı istenir, yoksa yönlendirme yapılır",
                "Size en yakın ekip (Beylikdüzü, Esenyurt veya Bahçeşehir) yönlendirilir",
                "Ekip malzemesiyle birlikte adrese gelir, uygulama evde tamamlanır",
                "Uygulama sonrası atıklar tıbbi atık kutusunda geri götürülür",
            ]),
        ],
        "faq": [
            ("Gece 03.00'te de geliyor musunuz?", "Evet. 7/24 çalışan bir nöbet sistemimiz var; gece saatlerinde de aynı numaradan ulaşabilirsiniz."),
            ("Hafta sonu ve resmî tatillerde hizmet var mı?", "Var. Cumartesi, pazar ve resmî tatiller dahil kesintisiz çalışıyoruz."),
            ("Ne kadar sürede geliyorsunuz?", "Süre bulunduğunuz mahalleye ve o anki ekip yoğunluğuna göre değişir. Aradığınızda size gerçekçi bir varış saati söylenir."),
        ],
    },
    {
        "slug": "evde-serum-hizmeti",
        "title": "Evde Serum Hizmeti",
        "short": "Damar yolu açılması ve serum takılması, kendi yatağınızda.",
        "icon": "drop",
        "kw": "evde serum hizmeti",
        "lead": "Hastane kuyruğunda saatlerce beklemek yerine serumunuzu evinizde alabilirsiniz. Damar yolu deneyimli hemşirelerimiz tarafından açılır, serum hekim isteminde belirtilen hızda gider ve uygulama boyunca yanınızda kalınır.",
        "sections": [
            ("Evde serum kimlere uygundur?", [
                "Ayakta duramayacak kadar halsiz olan, hastaneye gitmesi zor hastalara",
                "Kusma ya da ishal nedeniyle sıvı kaybı yaşayanlara",
                "Bağışıklığı düşük olduğu için hastane ortamından uzak durması gerekenlere",
                "Yaşlı, yatağa bağımlı ve engelli bireylere",
                "Damar yolu zor bulunan, tekrar tekrar denenmesini istemeyen kişilere",
            ]),
            ("Uygulama nasıl ilerliyor?", [
                "Tansiyon, nabız ve ateş ölçülerek başlanır",
                "Uygun kol seçilir, steril şartlarda damar yolu açılır",
                "Serum hekimin belirlediği akış hızına ayarlanır",
                "Uygulama boyunca hemşire evde bekler, reaksiyon takibi yapılır",
                "Serum bitince damar yolu kapatılır, atıklar toplanır",
            ]),
        ],
        "faq": [
            ("Serumu siz mi getiriyorsunuz?", "Hekim isteminde yazan serum ve ilaçlar sizde yoksa temin süreci için telefonda yönlendirme yapılır. Uygulama malzemeleri (branül, set, flaster, eldiven) ekiple birlikte gelir."),
            ("Reçetesiz serum takılır mı?", "Hayır. Serum ve içine eklenen ilaçlar hekim istemi olmadan uygulanmaz. Hekim değerlendirmesi olmayan durumlarda önce muayene için yönlendirme yapılır."),
            ("Bir serum ne kadar sürer?", "İçeriğine ve akış hızına göre genellikle 30 ile 90 dakika arasında değişir."),
        ],
    },
    {
        "slug": "evde-enjeksiyon",
        "title": "Evde Enjeksiyon Hizmeti",
        "short": "Kas içi, cilt altı ve damar içi enjeksiyon uygulaması.",
        "icon": "syringe",
        "kw": "evde enjeksiyon",
        "lead": "İğne için her gün sağlık ocağına gitmek zorunda değilsiniz. Hekiminizin yazdığı kas içi (İM), cilt altı (SC) ve damar içi (İV) enjeksiyonlar evinizde, doğru teknikle ve steril şartlarda uygulanır.",
        "sections": [
            ("En sık uygulanan enjeksiyonlar", [
                "Antibiyotik iğneleri (günlük veya belirli aralıklarla)",
                "Ağrı kesici ve kas gevşetici enjeksiyonlar",
                "B12, demir ve hekimin uygun gördüğü vitamin uygulamaları",
                "Kan sulandırıcı (düşük molekül ağırlıklı heparin) cilt altı iğneleri",
                "Doğurganlık tedavisi kapsamında hekimin planladığı iğneler",
                "Kortizon ve alerji tedavisinde kullanılan enjeksiyonlar",
            ]),
            ("Neden evde yaptırmak daha güvenli?", [
                "Enjeksiyon sonrası dinlenme süresini kendi evinizde geçirirsiniz",
                "Bekleme salonundaki enfeksiyon riskine girmezsiniz",
                "Aynı bölgeye tekrar tekrar yapılmaması için uygulama noktası kayıt altında tutulur",
                "Reaksiyon gelişirse hemşire ilk dakikalarda yanınızdadır",
            ]),
        ],
        "faq": [
            ("İlacı ben mi almalıyım?", "Evet, hekiminizin yazdığı ilacı eczaneden temin etmeniz gerekir. Enjektör, eldiven, pamuk ve tıbbi atık kutusu ekiple birlikte gelir."),
            ("Kalçadan iğne yapıyor musunuz?", "Evet. Kas içi enjeksiyonlar doğru anatomik nokta belirlenerek uygulanır."),
            ("Kan sulandırıcı iğneyi öğretiyor musunuz?", "Hasta ya da yakını isterse uygulama adım adım gösterilir; ancak sorumluluk hekim planına göre yürütülür."),
        ],
    },
    {
        "slug": "evde-glutatyon",
        "title": "Evde Glutatyon Takviyesi",
        "short": "Hekim değerlendirmesi sonrası glutatyon içeren serum uygulaması.",
        "icon": "sparkle",
        "kw": "evde glutatyon",
        "lead": "Glutatyon, vücutta doğal olarak bulunan bir antioksidandır. Damar yolundan glutatyon içeren takviye uygulaması, yalnızca hekim değerlendirmesi ve istemi doğrultusunda, uygun görülen kişilere evde yapılabilir.",
        "sections": [
            ("Uygulamadan önce mutlaka bilinmesi gerekenler", [
                "Glutatyon uygulaması bir hastalık tedavisi değildir; hekim uygun görmedikçe yapılmaz",
                "Astım öyküsü olanlarda dikkatle değerlendirilir",
                "Gebelik ve emzirme döneminde hekim onayı olmadan uygulanmaz",
                "Böbrek ve karaciğer hastalığı olanlarda mutlaka hekime danışılmalıdır",
                "İlk uygulamada reaksiyon takibi için hemşire evde bekler",
            ]),
            ("Uygulama akışı", [
                "Hekim istemi ve varsa güncel tahlil sonuçları kontrol edilir",
                "Tansiyon ve nabız ölçülür",
                "Damar yolu açılır, karışım hekim isteminde yazan hızda verilir",
                "Uygulama boyunca ve sonrasında kısa süre gözlem yapılır",
            ]),
        ],
        "faq": [
            ("Cilt beyazlatır mı?", "Bu konuda kesin ve genel geçer bir sonuç vaadi verilemez. Glutatyon uygulaması bir estetik sonuç garantisi değildir; hekiminizin değerlendirmesi esastır."),
            ("Kaç seans gerekir?", "Seans sayısı ve aralığı kişiye göre hekim tarafından belirlenir. Standart bir kür sayısı vaadinde bulunmuyoruz."),
            ("Reçetesiz yaptırabilir miyim?", "Hayır. Hekim istemi olmayan hiçbir damar içi uygulama yapılmaz."),
        ],
    },
    {
        "slug": "evde-multivitamin",
        "title": "Evde Multivitamin Takviyesi",
        "short": "Hekimin uygun gördüğü vitamin-mineral karışımlarının damar yolundan uygulanması.",
        "icon": "leaf",
        "kw": "evde multivitamin",
        "lead": "Yoğun tempo, hastalık sonrası toparlanma dönemi ya da eksikliği tahlille gösterilmiş vitaminler için hekiminizin planladığı multivitamin karışımı damar yolundan evinizde uygulanabilir.",
        "sections": [
            ("Hangi durumlarda gündeme gelir?", [
                "Kan tahlilinde gösterilmiş vitamin veya mineral eksikliğinde",
                "Uzun süren hastalık sonrası halsizlik döneminde",
                "Ağızdan alım yeterli olmadığında ya da emilim sorunu varsa",
                "Hekimin ameliyat sonrası toparlanma planında öngördüğü hâllerde",
            ]),
            ("Uygulama öncesi hazırlık", [
                "Güncel kan tahlili sonuçlarınızı hazır bulundurun",
                "Kullandığınız tüm ilaç ve takviyeleri ekibe bildirin",
                "Aç karnına uygulama önerilmez, hafif bir şeyler yemiş olun",
                "Bilinen ilaç alerjilerinizi mutlaka söyleyin",
            ]),
        ],
        "faq": [
            ("Tahlilim yoksa yapılır mı?", "Hekim gerekli görürse önce tahlil ister. Eksikliği gösterilmemiş takviyeyi kendi başımıza önermiyoruz."),
            ("Ne kadar sürer?", "Karışımın içeriğine göre çoğunlukla 45-90 dakika arasında sürer."),
            ("Aynı gün işe dönebilir miyim?", "Çoğu kişide engel yoktur, ancak uygulama sonrası kısa bir dinlenme önerilir."),
        ],
    },
    {
        "slug": "sonda-takma-degistirme",
        "title": "Sonda Takma ve Değiştirme",
        "short": "İdrar sondası takma, değiştirme ve bakım hizmeti.",
        "icon": "shield",
        "kw": "evde sonda takma",
        "lead": "İdrar sondası (foley kateter) takılması, süresi dolan sondanın değiştirilmesi ve sonda bakımı; hastanın hastaneye taşınmasına gerek kalmadan evde, steril şartlarda yapılır.",
        "sections": [
            ("Ne zaman değiştirilmeli?", [
                "Hekimin belirlediği sürenin dolmasıyla (genellikle belirli haftalık aralıklarla)",
                "İdrar akışının azalması, tıkanma şüphesi olduğunda",
                "İdrarda renk değişikliği, koku ya da çökelti fark edildiğinde",
                "Sonda çevresinden kaçak olduğunda",
                "Balon söndüğü için sonda yerinden çıktığında",
            ]),
            ("Evde bakım için hasta yakınına anlatılanlar", [
                "İdrar torbasının her zaman mesane seviyesinin altında tutulması",
                "Torbanın dolmadan boşaltılması ve boşaltma ucuna dokunulmaması",
                "Günlük temizlik ve sonda giriş bölgesinin kontrolü",
                "Ateş, yanma, bulanık idrar gibi enfeksiyon belirtilerinin fark edilmesi",
            ]),
        ],
        "faq": [
            ("Kadın ve erkek hastalara uygulanıyor mu?", "Evet, her iki hasta grubuna da uygulanır. Talebiniz olursa uygun cinsiyette sağlık personeli yönlendirilmeye çalışılır."),
            ("Sonda malzemesini siz mi getiriyorsunuz?", "Hekimin belirlediği numara ve tipteki sonda için telefonda bilgi verilir; uygulama malzemeleri ekiple gelir."),
            ("Ağrılı bir işlem mi?", "Kısa süreli rahatsızlık hissedilebilir. İşlem kayganlaştırıcı ile ve acele edilmeden yapılır."),
        ],
    },
    {
        "slug": "nazogastrik-sonda",
        "title": "Nazogastrik Sonda Takma Hizmeti",
        "short": "NG sonda takılması, değiştirilmesi ve beslenme eğitimi.",
        "icon": "tube",
        "kw": "nazogastrik sonda takma",
        "lead": "Ağızdan beslenemeyen hastalarda burundan mideye uzanan nazogastrik (NG) sonda, deneyimli hemşireler tarafından evde takılır ve belirlenen aralıklarla değiştirilir. Hasta yakınına beslenme uygulaması adım adım gösterilir.",
        "sections": [
            ("Hangi hastalarda kullanılır?", [
                "Felç sonrası yutma güçlüğü (disfaji) gelişen hastalarda",
                "Bilinci kapalı ya da yatağa bağımlı hastalarda",
                "İleri evre nörolojik hastalıklarda",
                "Ağızdan yeterli kalori alamayan hastalarda",
            ]),
            ("Takıldıktan sonra dikkat edilecekler", [
                "Her beslenmeden önce sondanın yerinde olduğunun kontrol edilmesi",
                "Beslenme sırasında hastanın baş kısmının yükseltilmesi",
                "Beslenme sonrası sondanın su ile yıkanması",
                "Öksürük, morarma, nefes darlığı görülürse beslenmenin durdurulması",
                "Burun kanadında bası yarası oluşmaması için tespit noktasının değiştirilmesi",
            ]),
        ],
        "faq": [
            ("Yerinde olup olmadığını nasıl anlarız?", "Hemşire takarken kontrol yöntemini hasta yakınına gösterir. Şüphe hâlinde beslenme yapılmadan bize ulaşmanız gerekir."),
            ("Ne sıklıkla değişir?", "Sondanın cinsine ve hekimin planına göre değişir; ekip size takvim bırakır."),
            ("Beslenmeyi biz yapabilir miyiz?", "Evet. Uygulama, hasta yakınına birebir gösterilir ve ilk beslenme gözetim altında yapılır."),
        ],
    },
    {
        "slug": "pansuman",
        "title": "Evde Pansuman Hizmeti",
        "short": "Ameliyat yarası, yatak yarası ve kronik yara bakımı.",
        "icon": "bandage",
        "kw": "evde pansuman",
        "lead": "Ameliyat sonrası yara, yanık, diyabetik ayak, bası (yatak) yarası ve kronik yaralarda pansuman; yaranın durumu değerlendirilerek uygun malzeme ile evde yapılır.",
        "sections": [
            ("En sık bakılan yara tipleri", [
                "Ameliyat kesisi ve dikiş yeri bakımı, dikiş alımı",
                "Bası (yatak) yaraları — evre değerlendirmesi ile birlikte",
                "Diyabetik ayak yaraları",
                "Yanık pansumanı",
                "Enfekte olmuş, akıntılı yaralar",
                "Dren ve kolostomi bölgesi bakımı",
            ]),
            ("Pansuman sırasında ne yapılır?", [
                "Eski örtü çıkarılır, yara boyutu ve görünümü kaydedilir",
                "Yara uygun solüsyonla temizlenir",
                "Gerekiyorsa ölü doku temizliği için hekime yönlendirme yapılır",
                "Yaraya uygun örtü seçilir ve kapatılır",
                "Bir sonraki pansuman tarihi hasta yakınına yazılı bırakılır",
            ]),
        ],
        "faq": [
            ("Dikiş alıyor musunuz?", "Hekimin belirlediği tarih geldiyse dikiş alımı evde yapılabilir."),
            ("Malzemeyi kim temin ediyor?", "Yara tipine göre gereken örtü/solüsyon listesi telefonda bildirilir; standart pansuman malzemesi ekiple gelir."),
            ("Yatak yarası ilerlerse ne olur?", "Yara ilerliyorsa fotoğraf takibi yapılır ve gecikmeden hekim değerlendirmesine yönlendirilirsiniz."),
        ],
    },
]

# --- Serum tedavileri ---------------------------------------------------------
SERUMS = [
    {
        "slug": "bulanti-kusma-serumu", "title": "Bulantı ve Kusma İçin Serum",
        "kw": "bulantı kusma serumu",
        "lead": "Durmayan kusma, kısa sürede sıvı ve elektrolit kaybına yol açar. Hekim istemi doğrultusunda uygulanan sıvı desteği ve bulantı kesici ilaçlar, kaybı yerine koymayı ve kusmayı durdurmayı hedefler.",
        "when": ["Peş peşe kusma ve ağızdan hiçbir şey tutamama", "Gıda zehirlenmesi şüphesi", "Mide virüsü (gastroenterit)", "Ağız kuruluğu, idrar miktarında azalma", "Ayağa kalkınca baş dönmesi"],
        "content": ["Sıvı-elektrolit desteği (izotonik veya hekimin uygun gördüğü sıvı)", "Hekimin seçtiği bulantı kesici (antiemetik) ilaç", "Gerekirse mide koruyucu"],
        "care": ["Kanlı ya da kahve telvesi görünümlü kusma varsa vakit kaybetmeden acile başvurun", "Şiddetli karın ağrısı kusmaya eşlik ediyorsa hekim muayenesi şarttır", "Bebek ve küçük çocuklarda sıvı kaybı çok hızlı ilerler, mutlaka hekime gösterin"],
    },
    {
        "slug": "agri-kesicili-serum", "title": "Ağrı Kesicili Serum",
        "kw": "ağrı kesicili serum",
        "lead": "Ağızdan alınan ilacın etki etmediği ya da bulantı nedeniyle tutulamadığı ağrılarda, hekimin uygun gördüğü ağrı kesici damar yolundan sıvı içinde verilebilir.",
        "when": ["Ağızdan ilacın işe yaramadığı şiddetli ağrı", "Kusma nedeniyle hap alamama", "Ameliyat sonrası ağrı dönemi", "Böbrek taşı ağrısında hekim yönlendirmesiyle", "Kas-iskelet kaynaklı şiddetli ağrılar"],
        "content": ["Hekimin seçtiği damar içi ağrı kesici", "Taşıyıcı sıvı", "Gerekirse mide koruyucu"],
        "care": ["Ağrının nedeni bilinmiyorsa önce tanı gerekir; ağrı kesici tanıyı geciktirebilir", "Göğüs ağrısı, ani ve en şiddetli baş ağrısı, karında sertlik acil durumdur", "Böbrek yetmezliği ve mide kanaması öyküsü mutlaka bildirilmelidir"],
    },
    {
        "slug": "ishal-serumu", "title": "İshal İçin Serum",
        "kw": "ishal serumu",
        "lead": "Günde çok sayıda sulu dışkılama, vücuttan hızla su ve tuz kaybettirir. Serum tedavisi bu kaybı yerine koymayı, tansiyon düşmesi ve halsizliği önlemeyi hedefler.",
        "when": ["Günde 4-5 ve üzeri sulu dışkılama", "Ağızdan sıvı alamama", "Ağız kuruluğu, çökmüş göz, idrarın azalması", "Yaşlı hastada ishal", "Uzun süren yolcu ishali"],
        "content": ["Sıvı-elektrolit desteği", "Hekim uygun görürse bulantı kesici", "Gerekirse potasyum/elektrolit düzenlemesi"],
        "care": ["Kanlı ishal ve yüksek ateş varsa mutlaka hekim değerlendirmesi gerekir", "İshal kesici ilaçlar her ishalde uygun değildir, hekime sormadan kullanmayın", "Bebeklerde ve 65 yaş üstünde sıvı kaybı hızlı ilerler"],
    },
    {
        "slug": "alerji-serumu", "title": "Alerji İçin Serum",
        "kw": "alerji serumu",
        "lead": "Kaşıntı, kurdeşen ve yaygın döküntü gibi alerjik tablolarda hekimin uygun gördüğü antihistaminik ve kortizon içeren tedavi damar yolundan uygulanabilir.",
        "when": ["Vücuda yayılan kurdeşen ve kaşıntı", "İlaç ya da besin sonrası gelişen döküntü", "Göz kapağı, dudak şişmesi (hekim değerlendirmesiyle)", "Ağızdan alınan alerji ilacının yetmediği durumlar"],
        "content": ["Hekimin seçtiği antihistaminik", "Gerekirse kortizon", "Taşıyıcı sıvı"],
        "care": ["Nefes darlığı, boğazda tıkanma hissi, ses kısıklığı, bayılma varsa bu bir ACİL durumdur — 112'yi arayın", "Daha önce anafilaksi geçirdiyseniz mutlaka bildirin", "Alerjiye neden olan madde biliniyorsa uzak durulması esastır"],
    },
    {
        "slug": "migren-serumu", "title": "Migren İçin Serum",
        "kw": "migren serumu",
        "lead": "Migren atağında ışık ve ses hassasiyeti yüzünden hastaneye gitmek başlı başına bir işkenceye dönüşür. Hekimin planladığı tedavi, karanlık ve sessiz kendi odanızda uygulanabilir.",
        "when": ["Ağızdan ilacın kestiği noktayı geçmiş atak", "Bulantı-kusmanın eşlik ettiği migren", "24 saati aşan, geçmeyen atak", "Işık ve sese dayanamama"],
        "content": ["Hekimin seçtiği ağrı kesici", "Bulantı kesici (antiemetik)", "Sıvı desteği", "Hekim uygun görürse magnezyum"],
        "care": ["Hayatınızın en şiddetli baş ağrısı ise ve aniden başladıysa acile gidin", "Ağrıya güçsüzlük, konuşma bozukluğu, çift görme eşlik ediyorsa acil değerlendirme gerekir", "Sık atak varsa koruyucu tedavi için nöroloji hekimine başvurun"],
    },
    {
        "slug": "regl-agrisi-serumu", "title": "Regl Ağrısı İçin Serum",
        "kw": "regl ağrısı serumu",
        "lead": "Adet sancısının işe, okula ve günlük hayata engel olduğu noktada; hekimin uygun gördüğü ağrı kesici ve kasılma çözücü tedavi evde damar yolundan uygulanabilir.",
        "when": ["Ağızdan ağrı kesicinin yetmediği sancı", "Bulantı-kusmanın eşlik ettiği adet ağrısı", "Ağrı nedeniyle ayakta duramama", "Bayılma hissi ve terleme"],
        "content": ["Hekimin seçtiği ağrı kesici", "Gerekirse kasılma çözücü (antispazmodik)", "Sıvı desteği", "Bulantı varsa antiemetik"],
        "care": ["Her ay artan, gittikçe şiddetlenen sancı endometriozis gibi nedenlerle ilgili olabilir; kadın hastalıkları hekimine görünün", "Ateşle birlikte olan pelvik ağrı enfeksiyon işareti olabilir", "Gebelik ihtimali varsa mutlaka önceden bildirin"],
    },
    {
        "slug": "enfeksiyon-virus-serumu", "title": "Enfeksiyon ve Virüs Salgınları İçin Serum",
        "kw": "enfeksiyon serumu",
        "lead": "Salgın dönemlerinde dolu bekleme salonları, hem hastayı hem de çevresini riske atar. Hekim tanısı konmuş enfeksiyonlarda destek tedavisi ve reçeteli antibiyotik uygulaması evde yapılabilir.",
        "when": ["Hekimin başlattığı damar içi antibiyotik tedavisinin devamı", "Yüksek ateşle seyreden viral tablolar", "Bağışıklığı düşük hastalarda hastane ortamından kaçınma ihtiyacı", "Salgın döneminde evde izolasyon"],
        "content": ["Reçeteli antibiyotik (yalnızca hekim istemiyle)", "Sıvı-elektrolit desteği", "Ateş düşürücü", "Hekim uygun görürse vitamin desteği"],
        "care": ["Antibiyotik virüslere etki etmez; gereksiz kullanım direnç oluşturur", "Tedavi yarıda kesilmemeli, hekimin verdiği gün sayısı tamamlanmalıdır", "Nefes darlığı, bilinç bulanıklığı, morarma varsa acil servise gidin"],
    },
    {
        "slug": "halsizlik-serumu", "title": "Halsizlik İçin Serum",
        "kw": "halsizlik serumu",
        "lead": "Dinlenmekle geçmeyen halsizliğin altında sıvı kaybı, vitamin eksikliği ya da geçirilmiş bir enfeksiyon olabilir. Hekim değerlendirmesinden sonra uygun görülen sıvı ve vitamin desteği evde uygulanır.",
        "when": ["Hastalık sonrası toparlanamama", "Yoğun tempo ve uykusuzluk sonrası tükenmişlik", "Tahlille gösterilmiş vitamin/mineral eksikliği", "İştahsızlıkla birlikte giden güçsüzlük"],
        "content": ["Sıvı-elektrolit desteği", "Hekim uygun görürse B grubu vitaminler", "Gerekirse magnezyum ve C vitamini"],
        "care": ["Uzun süren halsizlik anemi, tiroid hastalığı, diyabet gibi nedenlerin habercisi olabilir; tahlil yaptırın", "Serum, uykusuzluğun ve beslenme düzensizliğinin yerine geçmez", "Kalp ve böbrek hastalığı olanlarda sıvı miktarı hekim tarafından ayarlanmalıdır"],
    },
    {
        "slug": "grip-serumu", "title": "Grip İçin Serum",
        "kw": "grip serumu",
        "lead": "Yüksek ateş, kas ağrısı ve halsizlikle giden grip tablosunda; ateş düşürücü, ağrı kesici ve sıvı desteği hekim istemine göre evde uygulanabilir.",
        "when": ["38,5 °C üzerinde seyreden ateş", "Yaygın kas ve eklem ağrısı", "Ağızdan sıvı almakta zorlanma", "İş gücü kaybına neden olan şiddetli grip tablosu"],
        "content": ["Ateş düşürücü ve ağrı kesici", "Sıvı-elektrolit desteği", "Hekim uygun görürse C vitamini"],
        "care": ["Grip viral bir hastalıktır; antibiyotik gerekip gerekmediğine hekim karar verir", "Nefes darlığı, göğüs ağrısı ve morarma zatürre habercisi olabilir", "65 yaş üstü, gebe ve kronik hastalarda grip daha ağır seyredebilir"],
    },
    {
        "slug": "bas-donmesi-serumu", "title": "Baş Dönmesi İçin Serum",
        "kw": "baş dönmesi serumu",
        "lead": "Baş dönmesinin nedeni iç kulak kaynaklı olabileceği gibi tansiyon, sıvı kaybı ya da kansızlık da olabilir. Hekim değerlendirmesi sonrası uygun görülen tedavi evde verilebilir.",
        "when": ["Etrafın döndüğü hissiyle birlikte bulantı-kusma", "Ayağa kalkarken kararma ve dengesizlik", "Sıvı kaybına bağlı baş dönmesi", "Hekim tanısı konmuş vertigo atağı"],
        "content": ["Hekimin seçtiği baş dönmesi ilacı", "Bulantı kesici", "Sıvı-elektrolit desteği"],
        "care": ["Baş dönmesine konuşma bozukluğu, yüzde kayma, kolda güçsüzlük eşlik ediyorsa 112'yi arayın — inme belirtisi olabilir", "İlk kez ve şiddetli başlayan baş dönmesi mutlaka hekimde değerlendirilmelidir", "Tekrarlayan vertigo için KBB ve nöroloji takibi gerekir"],
    },
    {
        "slug": "soguk-alginligi-serumu", "title": "Soğuk Algınlığı İçin Serum",
        "kw": "soğuk algınlığı serumu",
        "lead": "Soğuk algınlığı çoğunlukla kendiliğinden geçer; ancak halsizlik, ateş ve iştahsızlık günlük hayatı durdurduğunda hekimin uygun gördüğü destek tedavisi evde uygulanabilir.",
        "when": ["Burun akıntısı, hapşırık ve boğaz yanmasına eşlik eden şiddetli halsizlik", "Ağızdan yeterli sıvı alamama", "Ateşin evdeki ilaçlarla düşmemesi", "İş ya da sınav öncesi hızla toparlanma ihtiyacı"],
        "content": ["Sıvı desteği", "Ateş düşürücü / ağrı kesici", "Hekim uygun görürse C vitamini ve çinko"],
        "care": ["Şikâyetler 10 günden uzun sürüyor ya da düzelirken kötüleşiyorsa hekime başvurun", "Kulak ağrısı, yüz ağrısı ve koyu renkli balgam bakteriyel enfeksiyon işareti olabilir", "Antibiyotik soğuk algınlığında yarar sağlamaz"],
    },
    {
        "slug": "ates-dusurucu-serum", "title": "Ateş İçin Serum",
        "kw": "ateş düşürücü serum",
        "lead": "Evde ilaçla düşmeyen ateşte, hem ateşi düşürmek hem de terlemeyle kaybedilen sıvıyı yerine koymak için hekim istemi doğrultusunda damar yolundan tedavi uygulanır.",
        "when": ["38,5 °C üzeri, ilaçla düşmeyen ateş", "Ateşle birlikte titreme ve terleme", "Ağızdan ilaç alamayacak kadar bulantılı olma", "Yaşlı hastada ateş yükselmesi"],
        "content": ["Damar içi ateş düşürücü", "Sıvı-elektrolit desteği", "Hekim gerekli görürse reçeteli antibiyotik"],
        "care": ["Ateşe ense sertliği, döküntü, bilinç bulanıklığı eşlik ediyorsa ACİL servise gidin", "3 aydan küçük bebeklerde her ateş acil değerlendirme gerektirir", "Ateşin nedeni bulunmadan tekrarlayan ateş düşürücü uygulaması tanıyı geciktirir"],
    },
    {
        "slug": "bogaz-agrisi-serumu", "title": "Boğaz Ağrısı İçin Serum",
        "kw": "boğaz ağrısı serumu",
        "lead": "Yutkunamayacak kadar şiddetli boğaz ağrısında ağızdan ilaç almak bile zorlaşır. Hekim değerlendirmesi sonrası ağrı kesici, ödem çözücü ve gerekiyorsa antibiyotik damar yolundan verilebilir.",
        "when": ["Yutkunmayı engelleyen şiddetli boğaz ağrısı", "Ateşle birlikte bademcik şişliği", "Ağızdan ilaç ve sıvı alamama", "Hekim tanısı konmuş bakteriyel farenjit/tonsillit"],
        "content": ["Ağrı kesici ve ateş düşürücü", "Hekim uygun görürse kortizon (ödem için)", "Reçeteli antibiyotik", "Sıvı desteği"],
        "care": ["Ağzını açamama, salya akması, nefes almakta zorlanma acil durumdur", "Boğaz ağrısının bakteriyel olup olmadığına hekim karar verir", "Antibiyotik gerekiyorsa süre tamamlanmalıdır"],
    },
    {
        "slug": "oksuruk-serumu", "title": "Öksürük İçin Serum",
        "kw": "öksürük serumu",
        "lead": "Gece uyutmayan, göğsü ağrıtan inatçı öksürükte; hekimin belirlediği tedavi ve sıvı desteği ile solunum yolunun rahatlaması hedeflenir.",
        "when": ["Gece boyu süren, uyku bölen öksürük", "Kuru ve boğazı yakan öksürük atakları", "Öksürükten kaynaklı göğüs ve karın kası ağrısı", "Hekim tanısı konmuş bronşit tablosu"],
        "content": ["Hekimin seçtiği öksürük tedavisi", "Sıvı desteği", "Gerekirse ateş düşürücü", "Hekim uygun görürse reçeteli antibiyotik"],
        "care": ["Kanlı balgam, nefes darlığı ve morarma varsa acil değerlendirme gerekir", "3 haftadan uzun süren öksürük mutlaka araştırılmalıdır (akciğer filmi)", "Astım ve KOAH hastalarında tedavi hekim tarafından ayrıca planlanır"],
    },
    {
        "slug": "vucut-agrilari-serumu", "title": "Vücut Ağrıları İçin Serum",
        "kw": "vücut ağrıları serumu",
        "lead": "Enfeksiyon, aşırı yorgunluk ya da grip tablosuyla gelen yaygın kas-eklem ağrılarında hekimin uygun gördüğü ağrı kesici ve sıvı desteği evde uygulanabilir.",
        "when": ["Griple birlikte gelen yaygın kas ağrısı", "Aşırı efor sonrası kas tutulması", "Ağızdan ağrı kesicinin yetersiz kalması", "Halsizliğin eşlik ettiği yaygın ağrı"],
        "content": ["Damar içi ağrı kesici", "Sıvı-elektrolit desteği", "Hekim uygun görürse magnezyum ve B vitamini"],
        "care": ["Ağrıya koyu renkli idrar eşlik ediyorsa kas yıkımı olabilir, acil değerlendirme gerekir", "Tek bir bacakta şişlik ve ağrı pıhtı belirtisi olabilir", "Uzun süren yaygın ağrılar için romatoloji değerlendirmesi gerekebilir"],
    },
]

DISCLAIMER = ("Bu sayfadaki bilgiler yalnızca bilgilendirme amaçlıdır; hekim muayenesi, tanı ve tedavinin "
              "yerine geçmez. Tüm damar içi uygulamalar hekim istemi ve reçetesi doğrultusunda, ilgili sağlık "
              "mevzuatına uygun şekilde yapılır. Acil durumlarda 112'yi arayınız.")
