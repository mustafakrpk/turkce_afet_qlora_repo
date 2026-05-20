# Veri Hazırlığı Pipeline'ı

## Genel Bakış

Bu projenin veri pipeline'ı 5 ana adımdan oluşur:

```
1. Ham veri yükleme       (503 + 47.079 örnek)
2. Zayıf etiketleme       (47k tweet için regex+bağlam kuralları)
3. Sentetik üretim        (az sınıflar için template-based)
4. Master dataset birleştirme + dengeleme
5. Train/Val/Test split   (stratified, sentetik yalnız train'de)
```

## 1. Ham Veri Kaynakları

| Kaynak | Boyut | Etiket Durumu |
|:-------|------:|:--------------|
| `tweets_etiketli.xlsx` | 503 | Manuel etiketli (Toraman + Kaggle birleşimi) |
| `depremGun5_düzenlendi.xlsx` | 47.079 | Hepsi `label=4` (ham, gerçekte 5 sınıf) |

### Manuel etiketli setin sınıf dağılımı

```
0 (yardim_talebi):       289
4 (diger_ilgisiz):       201
3 (bagis_koordinasyon):    8
2 (altyapi_hasari):        1
1 (kayip_bildirimi):       0   ← yok!
```

Ciddi sınıf dengesizliği nedeniyle ek veri kaynakları gerekti.

## 2. Zayıf Etiketleme (Weak Labeling)

47k ham tweet'i 5 sınıfa otomatik atamak için Türkçe afet domain'ine özel **kural tabanlı sınıflandırıcı** yazıldı (`src/weak_labeler_v2.py`).

### v1 → v2 iterasyonu

**v1** (basit keyword sayımı): Manuel kontrolde çok sayıda yanlış pozitif:
- "Allah" geçen dualar yardım sınıfına gidiyordu
- "Geçmişimiz yıkıldı" gibi **metaforik** ifadeler altyapı hasarına gidiyordu
- Sadece "AHBAP" geçen eleştiri tweet'leri bağış olarak işaretleniyordu

**v2** düzeltmeleri:
1. **Kombinasyon zorunluluğu:** "yardım" tek başına yetmez; "yardım+edin/bekliyor/lazım"
2. **Metafor filtresi:** "geçmişim/hayaller/dünyam yıkıldı" → diğer sınıfı
3. **Bağlam bayrakları:**
   - `is_siyasi` (AKP, CHP, hükümet, iktidar, ...) → yardım/altyapı skorlarını kır
   - `is_dua` (Allah rahmet, mekanı cennet, ...) → tüm skorları kır
   - `has_metafor` → altyapı skorunu yok et
4. **Telefon + adres bonusu:** Acil yardım çağrılarının tipik formu → yardım skorunu +2

### v2 Çıktısı (47k → 5 sınıf)

```
diger_ilgisiz      : 40.228  (85.45%)
yardim_talebi      :  6.079  (12.91%)
bagis_koordinasyon :    416  ( 0.88%)
kayip_bildirimi    :    246  ( 0.52%)
altyapi_hasari     :    110  ( 0.23%)
```

**Manuel kalite kontrol:** Her sınıftan 6'şar rastgele örnek incelendi. Tahmini doğruluk: **%70-80** (pseudo-label için kabul edilebilir).

## 3. Sentetik Veri Üretimi

Az örnekli sınıflar için template-based üreteç (`src/synth_generator.py`):

### Üretim Setleri

- **44 Türk ismi** (Ahmet Yılmaz, Şeyma Tunç, Pelin Güneş, ...)
- **10 şehir × 3-8 ilçe** (Hatay/Antakya, Maraş/Onikişubat, Adıyaman/Gölbaşı, ...)
- **20 mahalle adı**, **16 sokak/cadde** template
- **15 KAYIP** + **20 ALTYAPI** + **20 BAGIS** template

### Üretim Hacmi

```python
gen_kayip(568)    # 568 sentetik kayıp tweet
gen_altyapi(692)  # 692 sentetik altyapı tweet
gen_bagis(403)    # 403 sentetik bağış tweet
# TOPLAM: 1663 sentetik örnek
```

## 4. Master Dataset Birleştirme

### Hedef Dağılım

| Sınıf | Önce | Hedef | Δ |
|:------|-----:|------:|---:|
| yardim_talebi | 5.564 | 5.000 | −564 (downsample) |
| kayip_bildirimi | 232 | 800 | +568 (sentetik) |
| altyapi_hasari | 108 | 800 | +692 (sentetik) |
| bagis_koordinasyon | 397 | 800 | +403 (sentetik) |
| diger_ilgisiz | 37.962 | 5.000 | −32.962 (downsample) |
| **TOPLAM** | **44.263** | **12.400** | |

### Cross-tab (Source × Label)

```
                    gold   pseudo  synthetic
yardim_talebi       262     4738         0
diger_ilgisiz       193     4807         0
bagis_koordinasyon    8      389       403
altyapi_hasari        1      107       692
kayip_bildirimi       0      232       568
```

### Duplicate Temizliği

Birleştirme sonrası `text` alanına göre 3.277 duplicate tespit edildi ve temizlendi.

## 5. Train/Val/Test Split

### Kritik Kural: Sentetik Veri SADECE TRAIN'de

Val/test'te sentetik veri olsa, modelin template pattern'lerini "öğrenmesi" gerçek dünya performansını şişirir. Test setinin gerçeği temsil etmesi şart.

### Strateji

```python
# 1. Sentetik veriyi ayır (sadece train için)
synth = df[df['source']=='synthetic']  # 1.663 örnek

# 2. Gerçek veriyi stratified split
real = df[df['source']!='synthetic']   # 10.723 örnek
train_real, temp = train_test_split(real, test_size=0.2,
                                    stratify=real['label'], random_state=42)
val, test = train_test_split(temp, test_size=0.5,
                             stratify=temp['label'], random_state=42)

# 3. Train = real_train + tüm sentetik
train = pd.concat([train_real, synth])
```

### Sonuç

| Split | Toplam | Gold | Pseudo | Synthetic |
|:-----:|-------:|-----:|-------:|----------:|
| TRAIN | 10.241 | 371 | 8.207 | 1.663 |
| VAL   | 1.072  | 48  | 1.024 | 0 |
| TEST  | 1.073  | 45  | 1.028 | 0 |

### Test Sınıf Dağılımı (Gerçeği Yansıtır)

```
yardim_talebi      : 500  (46.6%)
diger_ilgisiz      : 499  (46.5%)
bagis_koordinasyon :  40  ( 3.7%)
kayip_bildirimi    :  23  ( 2.1%)
altyapi_hasari     :  11  ( 1.0%)
```

Az sınıflarda örnek azlığı raporda **limitation** olarak belirtilmelidir.

## Ön İşleme Adımları

`build_dataset.py` her tweet'e aşağıdaki temizliği uygular:

```python
def clean_text(text):
    t = text.strip()
    t = re.sub(r"http\S+|www\.\S+", " ", t)   # URL temizliği
    t = re.sub(r"@\w+", "[USER]", t)           # Mention anonimleştirme
    t = re.sub(r"\s+", " ", t).strip()          # Çoklu boşluk
    return t
```

**Bilinçli korunan:**
- Türkçe karakterler (ğ, ç, ş, ö, ü, ı) — tokenizer'lar zaten halleder
- Hashtag'ler (#deprem gibi) — anlamsal değer taşır
- Emoji'ler — minor model perspektifinden noise ama context kayıbı yapmaz

**Atılan:**
- 10 karakterden kısa tweet'ler (14 örnek)
- Tam duplicate'ler (text bazında, 3.277 örnek)

## Reproducibility

Tüm split'ler `seed=42` ile gerçekleştirilir. Pipeline'ı yeniden çalıştırmak için:

```bash
python src/build_dataset.py --seed 42
```

Çıktı `data/train.csv`, `data/val.csv`, `data/test.csv` olarak yazılır.
