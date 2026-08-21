# yanimdaevdesaglik.com

İstanbul Avrupa Yakası evde sağlık / evde serum hizmeti sitesi. Statik HTML, GitHub Pages.

## Yapı

    _src/            kaynak (sitede yayınlanmaz, robots.txt'te kapalı)
      build.py       üretici script
      site_data.py   işletme bilgisi, ilçeler, hizmetler, serumlar
      flagship.py    büyük semtler için elle yazılmış içerik
      content.py     mahalle sayfaları için varyasyon havuzları
      posts.py       Bilgi Merkezi yazıları
      icons.py       inline SVG ikon seti
      templates/     Jinja2 şablonları
      data/          resmî il-ilçe-mahalle listesi
    assets/          css, js, üretilmiş görseller
    images/          orijinal görseller (elle yüklenen)
    <slug>/index.html  üretilen sayfalar

## Yeniden üretmek

    python3 _src/build.py

Script `_src`, `assets`, `images`, `.git` dışındaki her şeyi siler ve baştan üretir.
Elle HTML düzenlemeyin — düzenleme `_src/` içinde yapılır.

## Sayfa sayısı

- 5 ilçe × 2 (evde sağlık + evde serum)
- 97 mahalle + 6 semt (evde sağlık) · yüksek talepli 24 konum ayrıca evde serum
- 8 hizmet + 15 serum tedavisi sayfası
- 6 bilgi merkezi yazısı + kurumsal sayfalar

## Bağımlılıklar

python3, jinja2, Pillow
