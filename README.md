# Türkçe Afet Tweet Sınıflandırması — QLoRA Fine-Tuningnn

> **5-sınıflı Türkçe afet tweet sınıflandırması için Küçük Dil Modelleri (SLM) ile QLoRA fine-tuning benchmark çalışması.**

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg)](https://pytorch.org/)
[![Transformers](https://img.shields.io/badge/🤗_Transformers-4.44-yellow.svg)](https://huggingface.co/docs/transformers)
[![License](https://img.shields.io/badge/license-Academic-green.svg)](LICENSE)

**Öğrenci:** Mustafa Kırpık · **Ders:** Büyük Dil Modelleri (BDM) · **Üniversite:** Selçuk Üniversitesi · **Dönem:** 2025-2026 Bahar

**Koordinasyon:** Bu proje Saliha Göçergi'nin **LoRA** çalışmasıyla koordineli olarak yürütülmektedir. Aynı veri seti, aynı modeller, aynı seed'ler kullanılarak **LoRA vs QLoRA başarı/kaynak karşılaştırması** yapılmıştır.

---

## 📋 İçindekiler

- [Problem Tanımı](#problem-tanımı)
- [Veri Seti](#veri-seti)
- [Yöntem](#yöntem)
- [Sonuçlar](#sonuçlar)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Proje Yapısı](#proje-yapısı)
- [Model Kartları](#model-kartları)
- [Bilinen Limitasyonlar](#bilinen-limitasyonlar)
- [Etik Beyan](#etik-beyan)
- [Atıflar](#atıflar)

---

## Problem Tanımı

2023 Kahramanmaraş depremleri sırasında Twitter'da paylaşılan tweet'lerin otomatik olarak **5 operasyonel sınıfa** ayrılması:

| ID  | Sınıf                | Açıklama                                 |
| :-: | :------------------- | :--------------------------------------- |
|  0  | `yardim_talebi`      | Acil yardım, kurtarma, malzeme talebi    |
|  1  | `kayip_bildirimi`    | İletişim kesilen / kayıp kişi aramaları  |
|  2  | `altyapi_hasari`     | Yıkık bina, kapalı yol, şebeke kesintisi |
|  3  | `bagis_koordinasyon` | Bağış, IBAN, gönüllü, lojistik           |
|  4  | `diger_ilgisiz`      | Haber, taziye, eleştiri, off-topic       |

**Motivasyon:** Sosyal medyada dakikalar içinde paylaşılan milyonlarca tweet'in **kısıtlı donanım kaynaklarında** çalışabilen küçük dil modelleriyle hızla kategorize edilmesi, afet yönetiminde **karar destek mekanizmasına** veri sağlar.

---

## Veri Seti

İki kaynaklı **hibrit veri seti** kullanılmıştır:

| Kaynak                                          |  Boyut | Açıklama                                                            |
| :---------------------------------------------- | -----: | :------------------------------------------------------------------ |
| Toraman et al. (2023) "Tweets Under the Rubble" |  ~1000 | Manuel etiketli akademik veri                                       |
| Kaggle "Türkiye Deprem Yardımlaşma"             |   ~500 | Topluluk veri                                                       |
| `depremGun5` (ham, yeniden etiketlendi)         | 47.079 | Bu proje kapsamında **zayıf etiketlenmiş** (regex+bağlam kuralları) |
| Sentetik (template-based)                       |  1.663 | Az örnekli sınıflar için (kayıp, altyapı, bağış)                    |

### Final Dağılım (12.400 örnek)

```
                    train    val   test
yardim_talebi       4000     500   500
diger_ilgisiz       3989     498   499
altyapi_hasari      778      11    11
kayip_bildirimi     754      23    23
bagis_koordinasyon  720      40    40
─────────────────────────────────────────
TOPLAM             10241   1072  1073
```

**Önemli:** Sentetik veri **sadece TRAIN setinde** kullanılmıştır. VAL ve TEST gerçek dağılımı korur (metrik bütünlüğü).

Veri hazırlığının detayları için bkz. [`docs/VERI_HAZIRLIGI.md`](docs/VERI_HAZIRLIGI.md).

---

## Yöntem

### QLoRA (Quantized Low-Rank Adaptation)

- **4-bit NormalFloat (NF4)** quantization
- **Double Quantization (DQ)** — sabitleri de quantize ederek ek ~%10 bellek kazancı
- **Paged Optimizers** — OOM koruması için CPU-GPU bellek yönlendirmesi
- **LoRA r=16, α=32**, target_modules=`[q_proj, k_proj, v_proj, o_proj]`

### Modeller

| Model                 | Parametre | HuggingFace ID                        |
| :-------------------- | --------: | :------------------------------------ |
| SmolLM2-360M-Instruct |      360M | `HuggingFaceTB/SmolLM2-360M-Instruct` |
| TinyLlama-1.1B-Chat   |      1.1B | `TinyLlama/TinyLlama-1.1B-Chat-v1.0`  |
| Qwen2.5-1.5B-Instruct |      1.5B | `Qwen/Qwen2.5-1.5B-Instruct`          |
| Gemma-2-2B-it         |      2.6B | `google/gemma-2-2b-it`                |

### Hiperparametreler

```yaml
epochs: 3
batch_size: 8
gradient_accumulation: 2
max_seq_length: 256
optimizer: paged_adamw_8bit
lr_scheduler: cosine
warmup_ratio: 0.05
seeds: [42, 123, 2023] # 3 seed → mean ± std
```

---

## Sonuçlar

> _Final sonuçlar fine-tuning tamamlandıktan sonra eklenecektir._

### Standart Sonuç Tablosu (placeholder)

| Model          | Yöntem    |  Accuracy |  Macro-F1 | Weighted-F1 | Train (s) | Inference (ms) | GPU (GB) |
| :------------- | :-------- | --------: | --------: | ----------: | --------: | -------------: | -------: |
| SmolLM2-360M   | Zero-shot |       TBD |       TBD |         TBD |         — |            TBD |      TBD |
| SmolLM2-360M   | QLoRA     | TBD ± TBD | TBD ± TBD |   TBD ± TBD |       TBD |            TBD |      TBD |
| TinyLlama-1.1B | Zero-shot |       TBD |       TBD |         TBD |         — |            TBD |      TBD |
| TinyLlama-1.1B | QLoRA     | TBD ± TBD | TBD ± TBD |   TBD ± TBD |       TBD |            TBD |      TBD |
| Qwen2.5-1.5B   | Zero-shot |       TBD |       TBD |         TBD |         — |            TBD |      TBD |
| Qwen2.5-1.5B   | QLoRA     | TBD ± TBD | TBD ± TBD |   TBD ± TBD |       TBD |            TBD |      TBD |
| Gemma-2-2B     | Zero-shot |       TBD |       TBD |         TBD |         — |            TBD |      TBD |
| Gemma-2-2B     | QLoRA     | TBD ± TBD | TBD ± TBD |   TBD ± TBD |       TBD |            TBD |      TBD |

### LoRA vs QLoRA Karşılaştırması

Bu çalışmanın benchmark makalesine ana katkısı, Saliha Göçergi'nin LoRA sonuçlarıyla yapılacak doğrudan karşılaştırmadır:

| Boyut           | LoRA (Saliha) | QLoRA (bu repo) |
| :-------------- | :------------ | :-------------- |
| Accuracy (mean) | TBD           | TBD             |
| Macro-F1 (mean) | TBD           | TBD             |
| Peak GPU bellek | TBD GB        | TBD GB          |
| Eğitim süresi   | TBD s         | TBD s           |

---

## Kurulum

### Gereksinimler

- Python 3.10+
- CUDA-uyumlu GPU (en az 8 GB VRAM)
- ~5 GB disk alanı (modeller için)

### Adımlar

```bash
git clone https://github.com/<username>/turkce-afet-tweet-qlora.git
cd turkce-afet-tweet-qlora

pip install -r requirements.txt
```

---

## Kullanım

### 1. Veri Hazırlığı

```bash
# Ham veriden weak labeling + sentetik üretim + split
python src/weak_labeler_v2.py
python src/synth_generator.py
python src/build_dataset.py
```

Çıktı: `data/train.csv`, `data/val.csv`, `data/test.csv`

### 2. Fine-Tuning (Colab veya yerel GPU)

Notebook olarak: `notebooks/QLoRA_FineTuning.ipynb`

Hücreleri sırayla çalıştır. Çıktılar `outputs/` altına:

- `all_results.json` — tüm koşuların ham sonuçları
- `summary_per_run.csv` — her koşunun metrikleri
- `summary_mean_std.csv` — model bazında ortalama±std
- `confusion_matrices.png` — her model için CM
- `errors_<model>.csv` — başarısız örnekler

### 3. Inference (Eğitilmiş Modeli Kullanma)

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import PeftModel

base_model = AutoModelForSequenceClassification.from_pretrained(
    "Qwen/Qwen2.5-1.5B-Instruct", num_labels=5
)
model = PeftModel.from_pretrained(base_model, "outputs/Qwen2.5-1.5B_seed42_adapter")
tokenizer = AutoTokenizer.from_pretrained("outputs/Qwen2.5-1.5B_seed42_adapter")

text = "Antakya'da kuzenime ulaşamıyoruz, lütfen yardım edin!"
inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
pred = model(**inputs).logits.argmax(-1).item()
print(["yardim_talebi", "kayip_bildirimi", "altyapi_hasari",
       "bagis_koordinasyon", "diger_ilgisiz"][pred])
```

---

## Proje Yapısı

```
turkce-afet-tweet-qlora/
├── README.md                    # Bu dosya
├── requirements.txt             # Python bağımlılıkları
├── LICENSE                      # Akademik kullanım lisansı
├── .gitignore                   # Git ignored
│
├── data/                        # Veri setleri (CSV)
│   ├── train.csv                # 10.241 örnek
│   ├── val.csv                  # 1.072 örnek
│   ├── test.csv                 # 1.073 örnek
│   └── README.md                # Veri açıklamaları
│
├── notebooks/                   # Çalıştırılabilir notebook'lar
│   └── QLoRA_FineTuning.ipynb   # Ana pipeline
│
├── src/                         # Kaynak kod
│   ├── weak_labeler_v2.py       # Kural tabanlı zayıf etiketleyici
│   ├── synth_generator.py       # Sentetik veri üreteci
│   └── build_dataset.py         # Birleştirme + split scripti
│
├── outputs/                     # Eğitim çıktıları
│   ├── all_results.json
│   ├── summary_*.csv
│   ├── confusion_matrices.png
│   ├── errors_*.csv
│   └── <model>_seed<N>_adapter/ # PEFT adaptörleri
│
├── model_cards/                 # Her model için Markdown kart
│   ├── MODELCARD_SmolLM2-360M.md
│   ├── MODELCARD_TinyLlama-1.1B.md
│   ├── MODELCARD_Qwen2.5-1.5B.md
│   └── MODELCARD_Gemma-2-2B.md
│
└── docs/                        # Ek dokümantasyon
    ├── VERI_HAZIRLIGI.md        # Veri pipeline'ı detayları
    ├── HATA_ANALIZI.md          # Hatalı örnekler analizi
    └── ETIK.md                  # Etik değerlendirme
```

---

## Model Kartları

Her fine-tuned model için detaylı kart `model_cards/` altında bulunmaktadır. Şablon:

- **Temel model + lisans**
- **Eğitim verisi** (kaynak, boyut, dil, lisans)
- **Hiperparametreler**
- **Performans metrikleri** (accuracy, F1, latency, VRAM)
- **Bilinen limitasyonlar ve bias riskleri**
- **Çalıştırma gereksinimleri**

---

## Bilinen Limitasyonlar

1. **Weak labeling kalitesi:** 47k ham tweet için kural tabanlı zayıf etiketleme uygulandı (~%70-80 tahmini doğruluk). Pseudo-label gürültüsü model performansını etkileyebilir.
2. **Sentetik veri bias'ı:** Template-based üretilen 1663 örnek, modelin pattern'lere fazla uyma riski yaratabilir. Sentetik veri **sadece train**'de kullanıldı.
3. **Twitter demografik bias:** Twitter kullanıcıları yaş, eğitim, kentsel/kırsal dağılım açısından genel nüfusu temsil etmez.
4. **Sınıf dengesizliği:** Gerçek dünyada `diger_ilgisiz` çok daha baskın. Test seti gerçek dağılımı yansıtır ancak az sınıflar (altyapı, kayıp) küçük örnekleme dayanır.
5. **Off-topic karışıklık:** Ekonomik kriz, başka afetler gibi tweet'ler yanlış sınıflandırılabilir.

---

## Etik Beyan

- **Bağlamsal Bütünlük:** Toplanan veriler **sadece akademik amaçlarla** kullanılmıştır. Çalışma sonunda kişisel veriler (mention'lar, telefon numaraları) anonimleştirilmiştir.
- **Karar Destek Aracı:** Bu sistem **tek başına karar verici değildir**. İnsan operatörlere yardımcı bir araç olarak tasarlanmıştır.
- **Yanlış Bilgilendirme:** Sahte yardım çağrılarına karşı doğrulama mekanizmaları gereklidir.

---

## Atıflar

Bu projede kullanılan kaynaklar:

```bibtex
@article{toraman2023tweets,
  title={Tweets Under the Rubble: Detection of Messages Calling for Help in Earthquake Disaster},
  author={Toraman, Cagri and others},
  journal={arXiv preprint arXiv:2302.13403},
  year={2023}
}

@article{dettmers2023qlora,
  title={QLoRA: Efficient Finetuning of Quantized LLMs},
  author={Dettmers, Tim and Pagnoni, Artidoro and Holtzman, Ari and Zettlemoyer, Luke},
  journal={NeurIPS},
  year={2023}
}

@article{hu2021lora,
  title={LoRA: Low-Rank Adaptation of Large Language Models},
  author={Hu, Edward J and others},
  journal={ICLR},
  year={2022}
}
```

---

## Lisans

Bu proje **akademik kullanım** içindir. Detaylar için bkz. [LICENSE](LICENSE).

---

## İletişim

- **Geliştirici:** Mustafa Kırpık (Selçuk Üniversitesi, BDM 2025-26)
- **Koordinasyon:** Saliha Göçergi (LoRA çalışması)
- **Ders sorumlusu:** [Hocanın adı]

---

_Son güncelleme: 20 Mayıs 2026_
