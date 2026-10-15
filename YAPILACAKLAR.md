# Kelime Kampı: durum ve yapılacaklar

Son güncelleme: 15 Ekim 2026

## Şu anki durum

- **Yerel sürüm:** bu klasör. `baslat.bat` ile http://localhost:8765 adresinde açılır. Derleme çıktısı yalnızca `index.html`.
- **İçerik hedefleri:** ~25 okuma, ~15 cloze, diğer YDS tipleri 20+; cümlede kullanım YDS/B2–C1 ağırlıklı genişletildi.
- **Çevrimdışı:** Google Fonts yok; sistem yazı tipleri. PWA (`manifest.webmanifest`, `sw.js`) http(s) üzerinde.
- **Tema:** üst çubuktaki düğme sistem / açık / koyu.
- **Deneme:** tam 80 soru veya kısa 40 soru; YÖKDİL alan filtresi; son denemelerde çıkan parçalar mümkün olduğunca tekrarlanmaz.
- **claude.ai:** ilerleme `kamp` + `kamp_prog` + `kamp_maps` + `kamp_hist` kayıtlarına bölünür; 180 KB üzeri parçada uyarı. Claude düğmeleri yerelde çevrimdışı örnek cümle gösterir.

## Kontrol

```bash
python kaynak/derle.py
python kaynak/review_content.py
python kaynak/test_kampi.py
```

## Yayın

GitHub’a yükleme bu oturumda atlandı (git komutu onaylanmadı). İstersen bir sonraki adımda depoyu başlatıp Pages’i açarız.
- Depoya Oxford PDF koyma
