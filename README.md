# Türkçe Afet Tweet Sınıflandırması — QLoRA Tabanlı İnce Ayar

5 sınıflı Türkçe afet tweet sınıflandırması için Küçük Dil Modellerinin (SLM) **QLoRA** ile ince ayarlanması ve karşılaştırmalı benchmark'ı.

> **BDM Dönem Projesi** · Mustafa Kırpık (Selçuk Üniversitesi) · Mayıs 2026
> Koordinasyon: Saliha Göçergi (LoRA çalışması) — birlikte **LoRA vs QLoRA** karşılaştırması.

## 🎯 Görev

2023 Kahramanmaraş depremlerine ait Türkçe tweet'lerin beş operasyonel sınıfa ayrılması:

| ID | Sınıf | Açıklama |
|----|-------|----------|
| 0 | Yardım Talebi | Acil yardım, kurtarma, malzeme çağrısı |
| 1 | Kayıp Bildirimi | Ulaşılamayan / kayıp kişi aramaları |
| 2 | Altyapı Hasarı | Yıkık bina, kapalı yol, şebeke kesintisi |
| 3 | Bağış/Koordinasyon | Bağış, IBAN, gönüllü, lojistik |
| 4 | Diğer/İlgisiz | Haber, taziye, eleştiri, off-topic |

## 📊 Veri

- **793 elle etiketlenmiş** gerçek tweet (Yardım 289 · Kayıp 98 · Altyapı 100 · Bağış 105 · Diğer 201)
- Bölme: **%80/10/10 stratified** → 633 / 80 / 80, `seed=42`
- *Not:* Zayıf etiketleme + sentetik üretim denendi; etiket kalitesi için **elle etiketli set** tercih edildi (`src/` altındaki üreticiler keşif amaçlıdır, nihai çalışmada kullanılmamıştır).

## 🚀 Yöntem

- **QLoRA:** 4-bit NF4 + çift kuantizasyon + bf16 hesaplama
- **LoRA:** r=16, α=32, dropout=0.05, hedef `q/k/v/o_proj`
- **Üretken SFT:** model tweet'e karşılık kategori adını üretir (`apply_chat_template`)
- 3 epoch · efektif batch 16 · lr 2e-4 · cosine · Colab T4

## 🏆 Sonuçlar (test, n=80, seed=42)

| Model | Yöntem | Accuracy | Macro-F1 | Weighted-F1 | Peak GPU |
|-------|--------|:--------:|:--------:|:-----------:|:--------:|
| TinyLlama-1.1B | Zero-shot | 0.262 | 0.094 | 0.125 | — |
| SmolLM2-360M | QLoRA | 0.662 | 0.588 | 0.663 | 1.81 GB |
| **TinyLlama-1.1B** | **QLoRA** | **0.925** | **0.908** | **0.921** | 3.29 GB |
| **Qwen2.5-1.5B** ⭐ | **QLoRA** | **0.925** | **0.914** | **0.925** | 5.07 GB |

**Sınıf bazlı F1 (QLoRA):**

| Sınıf | SmolLM2 | TinyLlama | Qwen2.5 |
|-------|:-------:|:---------:|:-------:|
| Yardım | 0.85 | 0.95 | 0.95 |
| Kayıp | 0.38 | 0.95 | 0.89 |
| Altyapı | 0.59 | 0.95 | 1.00 |
| Bağış | 0.42 | 0.74 | 0.78 |
| Diğer | 0.70 | 0.95 | 0.95 |

### Temel bulgular
- **Zero-shot çöküyor (Macro-F1 0.094) → QLoRA çarpıcı iyileşme (0.914).**
- **Ölçek + doygunluk:** 360M→1.1B büyük sıçrama; 1.1B→1.5B marjinal (≈1B'de doygunluk).
- **Verimlilik:** TinyLlama, Qwen'e ~eşit skoru %35 daha az GPU ile sağlıyor.
- **Bağış/Koordinasyon** her modelde en zayıf — Yardım Talebi ile semantik örtüşme.
- QLoRA tepe belleği **1.8–5.1 GB** (full fine-tune 20+ GB isterdi).

## 📁 Yapı

```
├── data/                 # train/val/test (793 elle etiketli setten)
├── notebooks/            # zero-shot + QLoRA ince ayar notebook'ları
├── model_cards/          # 3 modelin model kartları
├── src/                  # yardımcı betikler (keşifsel üreticiler dahil)
├── docs/                 # VERI_HAZIRLIGI.md, ETIK.md
└── requirements.txt
```

## 🔁 Tekrarlanabilirlik
Tüm bölünmeler ve eğitim `seed=42` ile sabitlenmiştir. Modeller HuggingFace'ten doğrudan yüklenir.

## 🔜 Gelecek
Gemma-4-E2B (4. model, Unsloth ile) · 3 seed ortalama±std · few-shot · tam LoRA–QLoRA karşılaştırması.

## ⚖️ Etik
Akademik amaçlı; kullanıcı etiketleri anonimleştirildi. Karar destek aracıdır, insan onayı esastır.

## 📚 Kaynaklar
Toraman et al. (2023) *Tweets Under the Rubble* · Dettmers et al. (2023) *QLoRA* · Hu et al. (2022) *LoRA*
