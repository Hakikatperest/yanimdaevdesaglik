# Yapılacaklar / kullanıcı brief'i

## 1. Kendi ağzınla yeniden yazılacak metinler
Aşağıdakiler **v1** olarak yazıldı; marka sesi ve E-E-A-T için kendi cümlelerinle değiştirilmeli.
Metni verdiğinde ilgili dosyaya yerleştirip `python3 _src/build.py` çalıştırmak yeterli.

| Sayfa | Dosya | Ne isteniyor |
|---|---|---|
| Anasayfa hero + "Neden bizi arıyorlar" | `_src/templates/home.html` | 1 paragraf giriş + 6 kısa madde, kendi üslubunla |
| Hakkımızda | `_src/build.py` → `write("hakkimizda"…)` | Kuruluş hikâyesi, ekip, kaç yıldır, kaç hasta — **gerçek rakam** |
| 6 Bilgi Merkezi yazısı | `_src/posts.py` | Gövdeler yazıldı; kendi vaka örneklerini ekle (birinci elden deneyim = AI aramalarında görünürlük için kritik) |
| 12 büyük semt sayfası | `_src/flagship.py` | `context` paragrafları — o bölgede gerçekten yaşadığın vakaları yaz |

## 2. Teyit edilmesi gerekenler
- [ ] **2. harita konumu**: koordinat (41.0345, 28.6747) Esenyurt'a düşüyor, sayfalarda "Esenyurt" olarak etiketlendi. Doğru mu?
- [ ] Hadımköy ve Boğazköy **Arnavutköy** ilçesinde. Hizmet bölgesi listesinde olduğu için semt sayfası açıldı, ilçe sayfası açılmadı — doğru mu?
- [ ] Varış süresi: hiçbir sayfada dakika vaadi yok ("aradığınızda gerçekçi süre söylenir" deniyor). Belirli bölgeler için gerçek süre vermek istersen söyle, ekleyeyim.
- [ ] Fiyat bilgisi hiçbir yerde yok. Eklenecek mi?

## 3. Eksik varlıklar
- [ ] Logo (şu an SVG artı işareti üretildi)
- [ ] Ekip / uygulama fotoğrafları — mevcut 2 görsel her sayfada dönüyor, 4-6 görsel daha iyi olur
- [ ] Gerçek müşteri yorumu / referans (schema'da `AggregateRating` bilinçli olarak YOK — uydurma puan koyulmadı)

## 4. Yayın sonrası
- [ ] Google Search Console'a `yanimdaevdesaglik.com` ekle, sitemap gönder
- [ ] **Google İşletme Profili** (3 konum için ayrı ayrı) — yerel aramada ve AI yanıtlarında en büyük etken
- [ ] Instagram bio'ya site linki
- [ ] 4-6 hafta sonra GSC'den mahalle sayfalarının indekslenme oranına bak. İndekslenmeyenler varsa
      o katmanı budarız (ölçeklendirilmiş içerik riski) — bu yüzden mahalle sayfaları tek şablondan
      değil, 6 farklı giriş / 5 farklı vaka / 5 farklı gerekçe havuzundan üretiliyor.

## 5. Bilinçli kararlar (değiştirmeden önce sor)
- Hiçbir sayfada **"reçetesiz serum takarız"** demiyoruz — hepsinde hekim istemi şartı yazıyor.
- Acil tablolar (göğüs ağrısı, nefes darlığı, bilinç kaybı) için **112'ye yönlendirme** var.
- Glutatyon sayfasında **cilt beyazlatma sonucu vaat edilmiyor**.
- Her sayfanın altında tıbbi sorumluluk uyarısı var (`DISCLAIMER`).
Bunlar hem hasta güvenliği hem sağlık hizmeti reklam mevzuatı açısından bilinçli konuldu.
