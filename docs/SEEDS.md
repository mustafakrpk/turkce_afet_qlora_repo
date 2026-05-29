# Seed Kullanımı ve Tekrarlanabilirlik

Bu proje, hocanın zorunlu raporlama gereksinimlerini karşılamak amacıyla aşağıdaki seed değerleriyle çalıştırılmıştır:

## Sabit Seed'ler
| Bölge | Seed | Amaç |
|-------|:----:|------|
| Veri bölme (train/val/test) | **42** | Tüm modeller aynı bölünmeyi kullanır (adil karşılaştırma) |
| Birinci eğitim koşusu | **42** | Ana sonuçlar bu seed ile |
| İkinci eğitim koşusu | **123** | Çok-seed ortalama±std için |
| Üçüncü eğitim koşusu | **2023** | Çok-seed ortalama±std için |

## Uygulama Detayları
- Python `random.seed(SEED)`, `numpy.random.seed(SEED)`, `torch.manual_seed(SEED)` çağrıları.
- TRL `SFTConfig(seed=SEED)` ile dataloader karıştırması ve optimizer init'i sabitlenir.
- LoRA adaptör başlatması: torch seed'ine bağlı (model.add_adapter sırasında).
- Test seti dağılımı her seed'de aynıdır (split seed=42 sabit).

## Çok-Seed Sonuçları
- Her model için 3 seed (42 + 123 + 2023) ile eğitim yapılır.
- Test setinde Accuracy ve Macro-F1 ölçülür.
- Rapor edilen değer: **ortalama ± standart sapma** (Tablo 4'te ana satırlar).
- Tek-seed sonuçlar yalnızca seed=42 olarak kullanılmıştır; çok-seed değerleri varsa onlar tercih edilir.

## Yeniden Çalıştırma
Tüm sonuçları yeniden üretmek için (sıra önemli değildir, her notebook bağımsız):
```bash
notebooks/02_zero_shot_baseline.ipynb        # zero-shot baseline (TinyLlama)
notebooks/03_fine_tuning_tinyllama.ipynb     # TinyLlama QLoRA
notebooks/04_fine_tuning_smollm2.ipynb       # SmolLM2 QLoRA
notebooks/05_fine_tuning_qwen25.ipynb        # Qwen2.5 QLoRA
notebooks/06_fine_tuning_gemma4.ipynb        # Gemma-4 QLoRA (Unsloth)
notebooks/07_zero_shot_smollm2_qwen.ipynb    # SmolLM2 + Qwen zero-shot
notebooks/08_few_shot_qwen.ipynb             # Qwen2.5 few-shot
notebooks/09_multiseed_standart.ipynb        # SmolLM2/TinyLlama/Qwen × seed 123, 2023 (self-resuming)
notebooks/10_multiseed_gemma4.ipynb          # Gemma × seed 123, 2023 (Unsloth)
```
