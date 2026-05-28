# Model Kartı — Gemma-4-E2B QLoRA (Türkçe Afet Tweet Sınıflandırma)

## Genel Bilgi
- **Temel model:** google/gemma-4-E2B-it (5B ham parametre, ~2B efektif — MatFormer/MoE, multimodal)
- **Yöntem:** QLoRA (4-bit, Unsloth, fp16 — T4 bf16 desteklemediği için)
- **Görev:** 5 sınıflı Türkçe afet tweet sınıflandırma (yalnızca metin; ses/görüntü kuleleri kullanılmadı)
- **Geliştiren:** Mustafa Kırpık — Selçuk Üniv., BDM Dönem Projesi (2026)

## Eğitim
- **Veri:** Kaggle "Turkey Earthquake Relief Tweets" (Küçüktaş, 2023) havuzundan 793 tweet, elle 5 sınıfa etiketlendi (633/80/80), seed=42, stratified
- **Pipeline:** Unsloth `FastModel` + TRL `SFTTrainer` (T4'te Gemma'nın fp16 kararsızlığı için Unsloth gerekli)
- **LoRA:** r=16, α=32, dropout=0.0, hedef: `q/k/v/o_proj` + `gate_proj/up_proj/down_proj` (Unsloth Gemma önerisi)
- **Eğitilebilir parametre:** 31.04M (%0.60) — diğer modellerin yaklaşık 7 katı
- **Hiperparametre:** 3 epoch, efektif batch 16, lr 2e-4, cosine, warmup 0.03
- **Donanım:** Colab T4 | **Süre:** ~718 s (tüm modeller arasında en hızlı) | **Tepe GPU:** 9.73 GB

## Sonuçlar (test, n=80)
| Metrik | Değer |
|---|---|
| Accuracy | 0.788 |
| Macro-F1 | 0.740 |
| Weighted-F1 | 0.765 |
| Çıkarım | 1798 ms/tweet |
| Ayrıştırma hatası | 0/80 |

**Sınıf bazlı F1:** Yardım 0.86 · Kayıp 0.46 · Altyapı 0.91 · Bağış 0.76 · Diğer 0.71

## Önemli Bulgular ve Açıklama
Bu, çalışmadaki **en büyük model olmasına rağmen TinyLlama (1.1B) ve Qwen2.5 (1.5B)'in gerisinde kalmıştır.** Eğitim sırasında klasik aşırı uydurma sinyali gözlenmiştir: train loss 0.003'e düşerken val loss 3.82'de kalmıştır.

Olası nedenler:
1. **Genişletilmiş LoRA hedefleri** — Unsloth'un Gemma için önerdiği 7 modül, daha küçük modellerde kullanılan 4 modüle göre çok daha fazla eğitilebilir parametre üretti (31M vs ~4M); küçük veride hızlı aşırı uydurma.
2. **Multimodal mimari** — Gemma-4 metin+görüntü+ses için tasarlandı; saf metin sınıflandırma için optimum değil.
3. **fp16 emülasyonu** — T4 bf16 desteklemediği için Unsloth fp16'ya geçti; numerik kararlılık ödün verildi.
4. **Ortak hiperparametre** — LR/epoch tüm modellere aynı uygulandı; Gemma için modele özel ayarlamayla skor muhtemelen artırılabilir.

**Spesifik hata deseni:** Kayıp Bildirimi'nde recall yalnızca 0.30 (10'da 3 yakalandı). Diğer/İlgisiz örneklerinin 6'sı yanlışlıkla Bağış/Koordinasyon'a atandı.

Bu sonuç projenin değerli bir bulgusudur: **küçük veri rejiminde "daha büyük her zaman daha iyi" değildir.**

## Sınırlılıklar
Hiperparametre ortak reçeteden alınmıştır; Gemma-4'e özel optimizasyon (epoch=1-2, lr=1e-4, dar LoRA hedefi) ile sonuç iyileştirilebilir. Tek seed (42). Yalnızca metin modu kullanıldı.

## Etik
Yalnızca akademik amaç. Veriler anonimleştirildi. Karar destek aracıdır; insan onayı esastır.
