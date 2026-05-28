# Veri Hazırlığı

## Kaynak ve Etiketleme
Ham tweet'ler Kaggle'daki açık **"Turkey Earthquake Relief Tweets Dataset"** (Ulku Tuncer Küçüktaş, 2023)
veri setinden alınmıştır:
https://www.kaggle.com/datasets/ulkutuncerkucuktas/turkey-earthquake-relief-tweets-dataset

Bu havuzdan seçilen **793 tweet, beş operasyonel sınıfa elle etiketlendi.** Ham metin Kaggle kaynağından
gelirken, 5 sınıflı etiketler tümüyle bu çalışmaya özgüdür. Etiketleme sınıf tanımlarına bağlı kalınarak
manuel yapıldı; bu, yüksek etiket kalitesi sağladı.

## Dürüstlük Beyanı
Erken aşamada kural tabanlı **zayıf etiketleme** ve az örnekli sınıflar için **sentetik üretim**
de denendi (`src/exploratory/`). Ancak etiket kalitesi ve değerlendirme bütünlüğü için nihai
çalışmada **793 örneklik elle etiketli set** tercih edildi; zayıf/sentetik veriler kullanılmadı.

## Sınıf Dağılımı
| 0 Yardım | 1 Kayıp | 2 Altyapı | 3 Bağış | 4 Diğer | Toplam |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 289 | 98 | 100 | 105 | 201 | 793 |

## Ön İşleme
URL ve `@kullanıcı` anonimleştirme, boşluk normalizasyonu. Türkçe karakter, hashtag, emoji korundu.

## Bölme
%80/10/10 stratified → 633 / 80 / 80 · `seed=42` (tekrarlanabilir).
Test dağılımı: Yardım 29, Kayıp 10, Altyapı 10, Bağış 11, Diğer 20.
