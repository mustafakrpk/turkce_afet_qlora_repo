# Veri

**Kaynak:** Kaggle — [Turkey Earthquake Relief Tweets Dataset](https://www.kaggle.com/datasets/ulkutuncerkucuktas/turkey-earthquake-relief-tweets-dataset) (Ulku Tuncer Küçüktaş, 2023).

Bu havuzdan seçilen **793 tweet, beş sınıfa elle etiketlendi.** Ham metin Kaggle kaynağından gelir;
5 sınıflı etiketler (`label_id` 0–4) tümüyle bu çalışmaya özgüdür.

`train.csv` / `val.csv` / `test.csv` bu 793 setin **%80/10/10 stratified** bölünmesidir (633 / 80 / 80), `seed=42`.
Kolonlar: `tweet`, `label_id`.

| Sınıf | 0 Yardım | 1 Kayıp | 2 Altyapı | 3 Bağış | 4 Diğer | Toplam |
|-------|:---:|:---:|:---:|:---:|:---:|:---:|
| Sayı | 289 | 98 | 100 | 105 | 201 | 793 |
