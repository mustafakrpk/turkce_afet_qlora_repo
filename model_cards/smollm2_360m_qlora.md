# Model Kartı — SmolLM2-360M QLoRA (Türkçe Afet Tweet Sınıflandırma)

## Genel Bilgi
- **Temel model:** HuggingFaceTB/SmolLM2-360M-Instruct (360M parametre)
- **Yöntem:** QLoRA (4-bit NF4, çift kuantizasyon, bf16 hesaplama)
- **Görev:** 5 sınıflı Türkçe afet tweet sınıflandırma (üretken/instruction format)
- **Geliştiren:** Mustafa Kırpık — Selçuk Üniv., BDM Dönem Projesi (2026)

## Eğitim
- **Veri:** Kaggle "Turkey Earthquake Relief Tweets" (Küçüktaş, 2023) havuzundan 793 tweet, elle 5 sınıfa etiketlendi (633 eğitim / 80 doğrulama / 80 test), seed=42, stratified
- **LoRA:** r=16, α=32, dropout=0.05, hedef: q/k/v/o_proj
- **Eğitilebilir parametre:** 3.28M (%0.90)
- **Hiperparametre:** 3 epoch, efektif batch 16, lr 2e-4, cosine, warmup 0.03
- **Donanım:** Colab T4 | **Süre:** ~696 s | **Tepe GPU:** 1.81 GB

## Sonuçlar (test, n=80)
| Metrik | Değer |
|---|---|
| Accuracy | 0.662 |
| Macro-F1 | 0.588 |
| Weighted-F1 | 0.663 |
| Çıkarım | 1542 ms/tweet |
| Ayrıştırma hatası | 0/80 |

**Sınıf bazlı F1:** Yardım 0.85 · Kayıp 0.38 · Altyapı 0.59 · Bağış 0.42 · Diğer 0.70

## Sınırlılıklar
En küçük model olduğu için az örnekli sınıflarda (Kayıp, Bağış, Altyapı) belirgin biçimde zayıftır; bu sınıflar birbirine karışır. Üretim için önerilmez; benchmark'ta alt-sınır (lower bound) referansıdır.

## Etik
Yalnızca akademik amaç. Veriler anonimleştirildi. İnsan onayı olmadan tek başına karar verici değildir.
