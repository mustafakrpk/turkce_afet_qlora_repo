# Veri

793 elle etiketlenmiş Türkçe deprem tweet'i, 5 sınıf. Bu klasördeki `train.csv` / `val.csv` / `test.csv`,
793 örneklik setin **%80/10/10 stratified** bölünmesidir (633 / 80 / 80), `seed=42`.

Kolonlar: `tweet`, `label_id` (0–4).

| Sınıf | 0 Yardım | 1 Kayıp | 2 Altyapı | 3 Bağış | 4 Diğer | Toplam |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| Sayı | 289 | 98 | 100 | 105 | 201 | 793 |

> Gerçek CSV'ler Google Drive `bdm_proje/data/processed/` altındadır; bu repoya kendi setinizi kopyalayın.
