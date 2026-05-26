# Model Kartı — Qwen2.5-1.5B QLoRA (Türkçe Afet Tweet Sınıflandırma)

## Genel Bilgi
- **Temel model:** Qwen/Qwen2.5-1.5B-Instruct (1.5B parametre)
- **Yöntem:** QLoRA (4-bit NF4, çift kuantizasyon, bf16 hesaplama)
- **Görev:** 5 sınıflı Türkçe afet tweet sınıflandırma
- **Geliştiren:** Mustafa Kırpık — Selçuk Üniv., BDM Dönem Projesi (2026)

## Eğitim
- **Veri:** 793 elle etiketlenmiş tweet (633/80/80), seed=42, stratified
- **LoRA:** r=16, α=32, dropout=0.05, hedef: q/k/v/o_proj
- **Eğitilebilir parametre:** 4.36M (%0.28)
- **Hiperparametre:** 3 epoch, efektif batch 16, lr 2e-4, cosine, warmup 0.03
- **Donanım:** Colab T4 | **Süre:** ~2151 s | **Tepe GPU:** 5.07 GB

## Sonuçlar (test, n=80) — EN İYİ MODEL
| Metrik | Değer |
|---|---|
| Accuracy | 0.925 |
| Macro-F1 | **0.914** |
| Weighted-F1 | 0.925 |
| Çıkarım | 1120 ms/tweet |
| Ayrıştırma hatası | 0/80 |

**Sınıf bazlı F1:** Yardım 0.95 · Kayıp 0.89 · Altyapı 1.00 · Bağış 0.78 · Diğer 0.95

## Öne Çıkanlar
En yüksek Macro-F1 (0.914) ve en düşük doğrulama kaybı. Altyapı Hasarı'nda kusursuz (F1 1.00), Yardım Talebi'nde tam recall (1.00). Güçlü Türkçe/çok dilli ön eğitiminin etkisi belirgin.

## Sınırlılıklar
En yüksek GPU belleğini kullanır (5.07 GB). Bağış/Koordinasyon yine en zayıf sınıf (0.78). Tek seed (42).

## Etik
Yalnızca akademik amaç. Veriler anonimleştirildi. Karar destek aracıdır; insan onayı esastır.
