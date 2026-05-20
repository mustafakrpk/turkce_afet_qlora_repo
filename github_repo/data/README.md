# Veri Klasörü

Bu klasör, modelin eğitim, doğrulama ve test setlerini içerir.

## Dosyalar

| Dosya | Satır sayısı | Açıklama |
|:------|-------------:|:---------|
| `train.csv` | 10.241 | Eğitim seti (gold + pseudo + sentetik) |
| `val.csv` | 1.072 | Doğrulama seti (gold + pseudo, sentetik YOK) |
| `test.csv` | 1.073 | Test seti (gold + pseudo, sentetik YOK) |

## Kolonlar

| Kolon | Tip | Açıklama |
|:------|:----|:---------|
| `text` | str | Temizlenmiş tweet metni |
| `label` | int | 0-4 arası sınıf etiketi |
| `label_name` | str | Sınıfın insan-okunabilir adı |
| `source` | str | `gold` / `pseudo` / `synthetic` |

## Sınıf Dağılımları

```
                  train    val   test
yardim_talebi      4000    500   500
diger_ilgisiz      3989    498   499
altyapi_hasari      778     11    11
kayip_bildirimi     754     23    23
bagis_koordinasyon  720     40    40
```

## Veri Kaynakları

- **Gold (manuel etiketli):** Toraman et al. (2023) + Kaggle Türkiye Deprem Yardımlaşma (toplam 464 örnek)
- **Pseudo (zayıf etiketli):** `depremGun5` ham 47k tweet, kural tabanlı sınıflandırıcı ile etiketlendi (10.273 örnek seçildi)
- **Synthetic (template-based):** Sadece az örnekli sınıflar için (1.663 örnek)

## Önemli Kurallar

⚠️ **Sentetik veri SADECE TRAIN setinde** kullanılır. Val/test gerçek dağılımı korur.

Detaylar için bkz. [`../docs/VERI_HAZIRLIGI.md`](../docs/VERI_HAZIRLIGI.md).
