# Kelime Kampı

YDS ve YÖKDİL'e hazırlananlar için ücretsiz, reklamsız, kâr amacı gütmeyen bir İngilizce çalışma oyunu. Tek bir HTML dosyası; internet bağlantısı, hesap ya da kurulum gerektirmez. İlerlemen yalnızca kendi tarayıcında saklanır.

## Neler var?

- **4.447 kelime** (A1 → C1 ve YDS/YÖKDİL akademik kelimeleri), Türkçe anlamları, kelime türü, birçok kelimede eş anlamlı ve seçili YDS kelimelerinde IPA
- **Aralıklı tekrar:** Bildiğin kelimeleri seyrek, zorlandıklarını sık sorar
- **Önce test, sonra tekrar:** "Bilmiyorum / emin değilim" diye işaretlediğin ya da yanlış yaptığın sorular turun sonunda tekrar sorulur
- **Kelime modları:** öğrenme kartları, İngilizce↔Türkçe, yazarak hatırlama, eşleştirme, hız turu, eş anlam avı, kelime ve cümle dikte
- **Kelime derinliği:** kelime aileleri (decide → decision → decisive), karıştırılan kelimeler (affect/effect), kalıplar (conduct research)
- **48 gramer konusu**, A1'den C1'e ve YDS'de sık sorulan konular; her biri Türkçe konu anlatımı ve 5–6 soruyla
- **9 YDS soru tipi:** okuma parçası (~25), cloze (~15), diğer tipler 20+; YÖKDİL sağlık / sosyal / fen alanı seçilebilir
- **Deneme sınavı:** 80 soru / 180 dakika (her doğru 1,25 puan) veya 40 soruluk kısa deneme; duraklatıp sonra devam; bölüm bölüm sonuç
- **Kendi kelime listen**, sınav tarihine göre **günlük plan**, **rozetler**, haftalık özet ve zayıf noktaların
- İlerlemeyi **.json dosyası olarak yedekleme ve geri yükleme**

## Nasıl çalıştırılır?

**Windows:** `baslat.bat` dosyasına çift tıkla. Tarayıcın **http://localhost:8765** adresinde açılır. Kapatmak için siyah pencereyi kapat. (Python gerekir; yoksa `index.html` dosyasına çift tıklaman da yeterli.)

**macOS / Linux:** Terminalde klasörde `sh baslat.sh` çalıştır, ardından **http://localhost:8765** adresini aç.

**Kurulumsuz:** `index.html` dosyasını herhangi bir tarayıcıda açman da yeterli. Yazı tipleri sistem fontlarıdır; internet gerekmez. `localhost` veya GitHub Pages üzerinden açınca tarayıcı “ana ekrana ekle” (PWA) önerebilir.

> İlerleme her adres için ayrı saklanır. `localhost:8765` ile çift tıklayarak açtığın dosyanın kayıtları birbirinden ayrıdır. Taşımak için İlerlemem → **Yedeği indir** ve diğerinde **Yedekten geri yükle**.

## Katkıda bulunmak

Bütün içerik `kaynak/data/` altındaki düz metin dosyalarındadır. Düzenledikten sonra sayfayı yeniden üretmek için:

```bash
python kaynak/derle.py
```

Betik verileri doğrular (boşluk sayısı, şık sayısı, doğru cevabın şıklar arasında olmaması vb.) ve `index.html`'i günceller.

| Dosya | Biçim |
|---|---|
| `a1.txt` … `c1.txt`, `oxford.txt` | `kelime\|tür\|Türkçe anlam` (`oxford.txt` dördüncü sütunda seviye) |
| `yds.txt` | `kelime\|tür\|Türkçe anlam\|eş anlamlılar` |
| `sentences.txt` | `kelime\|cevap biçimi\|___ içeren cümle\|yanlış1;yanlış2;yanlış3\|Türkçe çeviri` |
| `grammar1.txt`, `grammar2.txt` | `# id\|seviye\|EN başlık\|TR başlık`, `>` açıklama, `=` yapı, `e` örnek, `?` soru |
| `exam_*.txt` | `## id\|tür\|seviye\|konu`, `P:` metin, `Q:` soru, `A:` doğru, `X:` yanlış (4 adet), `W:` açıklama |
| `depth.txt` | `@fam`, `@conf`, `@coll` bölümleri |
| `ipa.txt` | `kelime\|IPA` |
| `synonyms.txt` | `kelime\|eş anlamlılar` (sözlükte eş anlamı yoksa doldurulur) |
| `sentences_more.txt` | `sentences.txt` ile aynı biçim |

Bir çeviri hatası, yanlış seviye ya da birden fazla doğru cevabı olan bir soru görürsen issue açman ya da düzeltme göndermen çok değerli.

## İçerik ve kaynaklar hakkında

- Türkçe anlamlar, örnek cümleler, gramer anlatımları, okuma parçaları ve tüm sorular bu proje için yazıldı. İçerik Claude (Anthropic) yardımıyla hazırlandı ve elle kontrol edildi; yine de hata olabilir.
- Kelime ve gramer seviyeleri yaklaşıktır. Kamuya açık CEFR kaynakları (Oxford 3000/5000 listeleri, English Grammar Profile) yol gösterici olarak kullanıldı.
- Bu proje ÖSYM, Oxford University Press ya da Cambridge ile bağlantılı değildir. Çıkmış sınav soruları içermez. Gerçek sorular için ÖSYM'nin yayımladığı kitapçıklara bakabilirsin.
- "Claude'dan yeni cümleler", "Örnek cümle iste" ve "Claude doldursun" düğmeleri yalnızca sayfa claude.ai üzerinde açıldığında çalışır. Yerel kullanımda diğer her şey çalışır.

## Lisans

Kod MIT lisansı ile paylaşılır (bkz. `LICENSE`).
