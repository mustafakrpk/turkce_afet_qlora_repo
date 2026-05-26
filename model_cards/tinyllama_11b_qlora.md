# Model Kartı — TinyLlama-1.1B QLoRA (Türkçe Afet Tweet Sınıflandırma)

## Genel Bilgi
- **Temel model:** TinyLlama/TinyLlama-1.1B-Chat-v1.0 (1.1B parametre)
- **Yöntem:** QLoRA (4-bit NF4, çift kuantizasyon, bf16 hesaplama)
- **Görev:** 5 sınıflı Türkçe afet tweet sınıflandırma
- **Geliştiren:** Mustafa Kırpık — Selçuk Üniv., BDM Dönem Projesi (2026)

## Eğitim
- **Veri:** 793 elle etiketlenmiş tweet (633/80/80), seed=42, stratified
- **LoRA:** r=16, α=32, dropout=0.05, hedef: q/k/v/o_proj
- **Eğitilebilir parametre:** 4.5M (%0.41)
- **Hiperparametre:** 3 epoch, efektif batch 16, lr 2e-4, cosine, warmup 0.03
- **Donanım:** Colab T4 | **Süre:** ~1697 s | **Tepe GPU:** 3.29 GB

## Sonuçlar (test, n=80)
| Metrik | Değer |
|---|---|
| Accuracy | 0.925 |
| Macro-F1 | 0.908 |
| Weighted-F1 | 0.921 |
| Çıkarım | 960 ms/tweet |
| Ayrıştırma hatası | 0/80 |

**Sınıf bazlı F1:** Yardım 0.95 · Kayıp 0.95 · Altyapı 0.95 · Bağış 0.74 · Diğer 0.95

## Öne Çıkanlar
En iyi modele (Qwen2.5) neredeyse eşdeğer başarıyı (~%35 daha düşük GPU belleğiyle) sağlar — **verimlilik açısından en dengeli seçenek.** Yardım Talebi'nde yüksek recall (0.97).

## Sınırlılıklar
Bağış/Koordinasyon sınıfında recall düşüktür (0.64); bu sınıf Yardım Talebi ile karışır. Tek seed (42) ile raporlanmıştır.

## Etik
Yalnızca akademik amaç. Veriler anonimleştirildi. Karar destek aracıdır; insan onayı esastır.
