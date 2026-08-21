# -*- coding: utf-8 -*-
"""Görsel kayıt defteri. Dosyalar images/ içinde; türevler assets/img/p/ altına üretilir.
Tüm görseller TAM BOY gösterilir (kırpma yok) ve tıklanınca arama başlatır."""

IMAGES = {
 "evde-saglik": {
   "file": "evde-saglik.webp",
   "alt": "Yanımda Evde Sağlık — hemşire evde yaşlı hastanın elini tutarken, 7/24 evde sağlık hizmeti",
   "cap": "Evde sağlık hizmeti — ekibimiz adresinize gelir",
 },
 "evde-saglik2": {
   "file": "evde-saglik2.webp",
   "alt": "7/24 evde sağlık hizmeti — hemşire evde hasta ziyaretinde, arayın hemen gelelim",
   "cap": "Arayın, hemen gelelim — 7/24 hizmet",
 },
 "7-24-evde-saglik": {
   "file": "7-24-evde-saglik.webp",
   "alt": "7/24 evde sağlık hizmeti çantası — evde özel formüllü serum hizmeti ve hizmet bölgeleri",
   "cap": "7/24 evde sağlık — hizmet verdiğimiz bölgeler",
 },
 "evde-serum": {
   "file": "evde-serum.webp",
   "alt": "Ev ortamında 7/24 evde serum hizmeti — halsizlik, ateş, mide bulantısı ve vücut ağrıları için serum",
   "cap": "Evde serum hizmeti — hekim istemi doğrultusunda",
 },
 "evde-serum-hizmeti": {
   "file": "evde-serum-hizmeti.webp",
   "alt": "Evde serum hizmeti — hastaya evinde serum takılırken, bağışıklığı güçlendiren destek tedavisi",
   "cap": "Evde serum uygulaması",
 },
 "evde-serum-yaptir": {
   "file": "evde-serum-yaptir.webp",
   "alt": "Evde serum yaptır — hemşire evde serum uygulaması yaparken, grip ve nezle için destek",
   "cap": "Hemşiremiz uygulama boyunca yanınızda kalır",
 },
 "evde-saglikci": {
   "file": "evde-saglikci.webp",
   "alt": "Evde sağlıkçı — grip, boğaz ağrısı ve yüksek ateşte evde özel formüllü serum hizmeti",
   "cap": "Grip ve soğuk algınlığında evde uygulama",
 },
 "evde-saglikci-numarasi": {
   "file": "evde-saglikci-numarasi.webp",
   "alt": "Evde sağlıkçı numarası — ateş, soğuk algınlığı, mide bulantısı ve baş ağrısı için evde serum hizmeti",
   "cap": "Hangi şikâyetlerde arıyorlar?",
 },
 "evde-saglik-hizmeti": {
   "file": "evde-saglik-hizmeti.webp",
   "alt": "Evde serum hizmeti — evin oturma odasında kurulmuş serum askısı ve serum seti",
   "cap": "Uygulama kendi evinizde yapılır",
 },
 "evde-saglik-iletisim": {
   "file": "evde-saglik-iletisim.webp",
   "alt": "Evde sağlık ve evde serum hizmeti iletişim — 7/24 çağrı hattı ve hizmet verilen ilçeler",
   "cap": "7/24 çağrı hattı",
 },
}

# --- sabit yerleşimler ---
HOME_HERO   = "evde-saglik"
HOME_MID    = "evde-saglik2"
HOME_SERUM  = "evde-serum"
HUB_SERVICE = "7-24-evde-saglik"
HUB_SERUM   = "evde-serum-hizmeti"
HUB_AREA    = "evde-saglikci-numarasi"
PAGE_ILETISIM = "evde-saglik-iletisim"
PAGE_HAKKIMIZDA = "evde-saglik2"

# hizmet sayfası -> görsel
SERVICE_IMG = {
 "7-24-evde-saglik":       "7-24-evde-saglik",
 "evde-serum-hizmeti":     "evde-serum-hizmeti",
 "evde-enjeksiyon":        "evde-serum-yaptir",
 "evde-glutatyon":         "evde-serum",
 "evde-multivitamin":      "evde-saglikci-numarasi",
 "sonda-takma-degistirme": "evde-saglik-hizmeti",
 "nazogastrik-sonda":      "evde-saglik",
 "pansuman":               "evde-saglik2",
}

# serum sayfalarında dönüşümlü kullanılacaklar
SERUM_POOL = ["evde-serum", "evde-serum-hizmeti", "evde-serum-yaptir",
              "evde-saglikci", "evde-saglikci-numarasi", "evde-saglik-hizmeti"]

# konum ve blog sayfalarında dönüşümlü kullanılacaklar (hepsi)
ROTATE = list(IMAGES.keys())
