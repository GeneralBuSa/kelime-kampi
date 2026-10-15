# Kelime Kampı

YDS ve YÖKDİL'e hazırlananlar için ücretsiz, reklamsız, kâr amacı gütmeyen bir İngilizce çalışma oyunu. Tek bir HTML dosyası; internet bağlantısı, hesap ya da kurulum gerektirmez. İlerlemen yalnızca kendi tarayıcında saklanır.

## Neler var?

- **4.447 kelime** (A1 → C1 ve YDS/YÖKDİL akademik kelimeleri), Türkçe anlamları, kelime türü, birçok kelimede eş anlamlı ve seçili YDS kelimelerinde IPA
- **Aralıklı tekrar:** Bildiğin kelimeleri seyrek, zorlandıklarını sık sorar
- **Önce test, sonra tekrar:** "Bilmiyorum / emin değilim" diye işaretlediğin ya da yanlış yaptığın sorular turun sonunda tekrar sorulur
- **Kelime modları:** öğrenme kartları, İngilizce↔Türkçe, yazarak hatırlama, eşleştirme, hız turu, eş anlam avı, kelime ve cümle dikte
- **Kelime derinliği:** kelime aileleri (decide → decision → decisive), karıştırılan kelimeler (affect/effect), kalıplar (conduct research)
- **48 gramer konusu**, A1'den C1'e ve YDS'de sık sorulan konular; Türkçe konu anlatımı ve toplam 358 soru (konu başına 7–8)
- **9 YDS soru tipi:** okuma parçası (~25), cloze (~15), diğer tipler 20+; YÖKDİL sağlık / sosyal / fen alanı seçilebilir
- **Okuma soru kökleri:** ana fikir, ayrıntı, çıkarım ve bağlamda kelimenin yanında başlık bulma, yazarın tutumu, "değildir / çıkarılamaz" ve yazarın amacı; her parçada en az bir tane
- **Okurken kelimeye dokun:** okuma ve paragraf metinlerinde bilmediğin kelimeye dokununca anlamı açılır (çekimli biçimlerde de: *declined* → decline), tek dokunuşla listene eklenir; deneme sınavında kapalıdır
- **Hata analizi:** her yanlış bir tuzak türüne bağlanır (zaman uyumu, bağlaçlar, koşul, edilgen, edatlar, bağlamda kelime, okuma kökleri…); İlerlemem'de en zayıf türler, somut öneri ve o türden 12 soruluk tur; her turun ve denemenin sonunda "yanlışların en çok …" özeti
- **Deneme sınavı:** 80 soru / 180 dakika (her doğru 1,25 puan), 40 soru / 90 dakika veya 20 soru / 45 dakika (gerçek sınavla aynı tempo); duraklatıp sonra devam; bölüm bölüm sonuç
- **Zayıf nokta antrenmanı:** İlerlemem’de tek düğmeyle bugünkü zayıf tip/konu/kelimelerden 15 soru
- **Yanlış defteri:** düz metin indir veya yazdır
- **Kendi kelime listen**, sınav tarihine göre **günlük plan**, **rozetler**, haftalık özet ve zayıf noktaların
- İlerlemeyi **.json dosyası olarak yedekleme ve geri yükleme**
- İsteğe bağlı **yerel tekrar bildirimi** (varsayılan kapalı; sunucuya gitmez) ve isteğe bağlı **API anahtarı** (varsayılan boş; hesaba/yedeğe yazılmaz)

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

Betik verileri doğrular (boşluk sayısı, şık sayısı, doğru cevabın şıklar arasında olmaması vb.), `index.html`'i günceller ve `sw.js` içindeki önbellek sürümünü kendiliğinden yeniler. Göndermeden önce şu kontrolleri de çalıştır:

```bash
python kaynak/review_content.py
python kaynak/test_kampi.py
node kaynak/test_kampi.mjs
```

`test_kampi.py` içerik hedeflerini ve verinin tutarlılığını, `test_kampi.mjs` ise uygulamanın gerçek fonksiyonlarını (puanlama, aralıklı tekrar, ilerleme birleştirme, okuma metni, kelime kökü bulma) `index.html`'den okuyarak sınar.

| Dosya | Biçim |
|---|---|
| `a1.txt` … `c1.txt`, `oxford.txt` | `kelime\|tür\|Türkçe anlam` (`oxford.txt` dördüncü sütunda seviye) |
| `yds.txt` | `kelime\|tür\|Türkçe anlam\|eş anlamlılar` |
| `sentences.txt` | `kelime\|cevap biçimi\|___ içeren cümle\|yanlış1;yanlış2;yanlış3\|Türkçe çeviri` |
| `grammar1.txt`, `grammar2.txt` | `# id\|seviye\|EN başlık\|TR başlık`, `>` açıklama, `=` yapı, `e` örnek, `?` soru |
| `grammar_drill.txt` | `# konu-id` başlığı altında ek sorular: `? cümle\|cevap\|yanlış1;yanlış2;yanlış3\|açıklama` |
| `exam_*.txt` | `## id\|tür\|seviye\|konu`, `P:` metin, `Q:` soru, `A:` doğru, `X:` yanlış (4 adet), `W:` açıklama. Okuma parçası 4–6 soru alır; soru kökü (başlık, tutum, değildir, amaç…) ve cloze / cümle tamamlama sorularının tuzak türü derlemede otomatik etiketlenir |
| `depth.txt` | `@fam`, `@conf`, `@coll` bölümleri |
| `ipa.txt` | `kelime\|IPA` |
| `synonyms.txt` | `kelime\|eş anlamlılar` (sözlükte eş anlamı yoksa doldurulur) |
| `sentences_more.txt` | `sentences.txt` ile aynı biçim |

Bir çeviri hatası, yanlış seviye ya da birden fazla doğru cevabı olan bir soru görürsen issue açman ya da düzeltme göndermen çok değerli.

## İçerik ve kaynaklar hakkında

- Türkçe anlamlar, örnek cümleler, gramer anlatımları, okuma parçaları ve tüm sorular bu proje için yazıldı. İçerik Claude (Anthropic) yardımıyla hazırlandı ve otomatik kontrollerden geçirildi (şık sayısı, boşluk, cevabın şıklarda tekrar etmemesi vb.), ancak henüz bir insan tarafından tek tek okunmadı; hata olabilir.
- Kelime ve gramer seviyeleri yaklaşıktır. Kamuya açık CEFR kaynakları (Oxford 3000/5000 listeleri, English Grammar Profile) yol gösterici olarak kullanıldı.
- Bu proje ÖSYM, Oxford University Press ya da Cambridge ile bağlantılı değildir. Çıkmış sınav soruları içermez. Gerçek sorular için ÖSYM'nin yayımladığı kitapçıklara bakabilirsin.
- "Claude'dan yeni cümleler", "Örnek cümle iste" ve "Claude doldursun" düğmeleri claude.ai üzerinde veya İlerlemem’e yapıştırdığın isteğe bağlı API anahtarıyla çalışır. Anahtar yoksa çevrimdışı örnek cümle ve hazır banka kullanılır. Tarayıcıdan doğrudan API çağrısı CORS yüzünden başarısız olabilir.

## Bilinen sınırlar

- İçerik bir insan tarafından tek tek okunmadı; hata görürsen issue açman ya da düzeltme göndermen çok değerli.
- Kelime kartlarındaki hazır örnek cümleler cümle bankasından ve okuma metinlerinden gelir; şu an kelimelerin yaklaşık üçte birinde var. Diğerlerinde kart "hazır örnek yok" der. `sentences_more.txt` büyüdükçe bu oran artar.
- Claude ile çalışan düğmeler bu sürümde gerçek bir claude.ai oturumunda ya da API anahtarıyla denenmedi.

## Lisans

Kod MIT lisansı ile paylaşılır (bkz. `LICENSE`).
