"""
Master Dataset Builder
======================
Ham + zayıf etiketli + sentetik verileri birleştirir, dengeler, 80/10/10 split yapar.

Çalıştırma:
    python src/build_dataset.py --seed 42

Çıktılar:
    data/train.csv
    data/val.csv
    data/test.csv
"""
import argparse
import re
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

import sys
sys.path.insert(0, str(Path(__file__).parent))
from weak_labeler_v2 import classify_tweet_v2
from synth_generator import gen_kayip, gen_altyapi, gen_bagis


LABEL_NAMES = {
    0: 'yardim_talebi', 1: 'kayip_bildirimi', 2: 'altyapi_hasari',
    3: 'bagis_koordinasyon', 4: 'diger_ilgisiz'
}

# Hedef dengeli dağılım
TARGET = {
    0: 5000,   # yardim_talebi
    1: 800,    # kayip_bildirimi
    2: 800,    # altyapi_hasari
    3: 800,    # bagis_koordinasyon
    4: 5000,   # diger_ilgisiz
}


def clean_text(text: str) -> str:
    """Minimal Türkçe ön işleme: URL kaldır, mention anonimleştir, çoklu boşluk."""
    if not isinstance(text, str):
        return ""
    t = text.strip()
    t = re.sub(r"http\S+|www\.\S+", " ", t)
    t = re.sub(r"@\w+", "[USER]", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def to_int_label(x):
    """Etiket sütununu int 0-4'e çevir."""
    try:
        v = int(x)
        if 0 <= v <= 4:
            return v
    except (ValueError, TypeError):
        x_str = str(x).strip().upper()
        mp = {'YARDIM_TALEBI': 0, 'KAYIP_BILDIRIMI': 1, 'ALTYAPI_HASARI': 2,
              'BAGIS_KOORDINASYON': 3, 'DIGER': 4, 'DIGER_ILGISIZ': 4, 'İLGİSİZ': 4}
        return mp.get(x_str)
    return None


def main(args):
    print(f"Seed: {args.seed}")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # =========================================================================
    # 1) Gold dataset (manuel etiketli)
    # =========================================================================
    print("\n[1/5] Gold dataset yükleniyor...")
    df_gold = pd.read_excel(args.gold_path)
    df_gold = df_gold[['text', 'label_name']].dropna()
    df_gold['label'] = df_gold['label_name'].apply(to_int_label)
    df_gold = df_gold.dropna(subset=['label'])
    df_gold['label'] = df_gold['label'].astype(int)
    df_gold = df_gold[['text', 'label']].copy()
    df_gold['source'] = 'gold'
    print(f"  Gold: {len(df_gold)} örnek")

    # =========================================================================
    # 2) Pseudo dataset (47k zayıf etiketli)
    # =========================================================================
    print("\n[2/5] Pseudo dataset (47k) zayıf etiketleyiciyle işleniyor...")
    df_pseudo_raw = pd.read_excel(args.pseudo_path)
    results = [classify_tweet_v2(t) for t in df_pseudo_raw['text']]
    df_pseudo = pd.DataFrame({
        'text': df_pseudo_raw['text'],
        'label': [r[0] for r in results],
        'source': 'pseudo'
    })
    print(f"  Pseudo: {len(df_pseudo)} örnek")

    # =========================================================================
    # 3) Birleştir, dublicate temizle, ön işle
    # =========================================================================
    print("\n[3/5] Birleştiriliyor + dublicate temizleniyor...")
    combined = pd.concat([df_gold, df_pseudo], ignore_index=True)
    combined['text_norm'] = combined['text'].astype(str).str.strip().str.lower()
    before = len(combined)
    combined = combined.drop_duplicates(subset='text_norm', keep='first')
    combined = combined[combined['text'].astype(str).str.len() >= 10].reset_index(drop=True)
    combined = combined.drop(columns=['text_norm'])
    print(f"  {before} → {len(combined)} (duplicate + short text filtered)")

    # =========================================================================
    # 4) Dengeleme + sentetik üretim
    # =========================================================================
    print("\n[4/5] Dengeleniyor + sentetik üretiliyor...")
    parts = []
    for lbl, hedef in TARGET.items():
        subset = combined[combined['label'] == lbl]
        if len(subset) > hedef:
            # Gold öncelikli tutulur
            gold_part = subset[subset['source']=='gold']
            pseudo_part = subset[subset['source']=='pseudo']
            keep_gold = gold_part.sample(min(len(gold_part), hedef), random_state=args.seed)
            remaining = hedef - len(keep_gold)
            keep_pseudo = pseudo_part.sample(min(len(pseudo_part), remaining), random_state=args.seed) if remaining > 0 else pd.DataFrame()
            sampled = pd.concat([keep_gold, keep_pseudo])
            parts.append(sampled)
        else:
            parts.append(subset)

    current = pd.concat(parts, ignore_index=True)

    # Sentetik üretim
    synth_rows = []
    for lbl, hedef in TARGET.items():
        mevcut = (current['label']==lbl).sum()
        eksik = hedef - mevcut
        if eksik <= 0:
            continue
        if lbl == 1:
            texts = gen_kayip(eksik, seed=args.seed)
        elif lbl == 2:
            texts = gen_altyapi(eksik, seed=args.seed)
        elif lbl == 3:
            texts = gen_bagis(eksik, seed=args.seed)
        else:
            continue
        for t in texts:
            synth_rows.append({'text': t, 'label': lbl, 'source': 'synthetic'})

    synth_df = pd.DataFrame(synth_rows)
    final = pd.concat([current, synth_df], ignore_index=True)
    final = final.sample(frac=1, random_state=args.seed).reset_index(drop=True)

    # Cleaning
    final['text'] = final['text'].apply(clean_text)
    final = final[final['text'].str.len() >= 10].reset_index(drop=True)
    final['label_name'] = final['label'].map(LABEL_NAMES)

    print(f"  Final: {len(final)} örnek")
    print(final['label_name'].value_counts())

    # =========================================================================
    # 5) Train/Val/Test split (sentetik sadece train'de)
    # =========================================================================
    print("\n[5/5] Train/Val/Test split (sentetik yalnız train'de)...")
    synth = final[final['source']=='synthetic']
    real = final[final['source']!='synthetic']

    train_real, temp = train_test_split(real, test_size=0.2,
                                         stratify=real['label'], random_state=args.seed)
    val, test = train_test_split(temp, test_size=0.5,
                                  stratify=temp['label'], random_state=args.seed)
    train = pd.concat([train_real, synth], ignore_index=True).sample(
        frac=1, random_state=args.seed).reset_index(drop=True)

    print(f"  TRAIN: {len(train)} | VAL: {len(val)} | TEST: {len(test)}")

    # Kaydet
    cols = ['text', 'label', 'label_name', 'source']
    train[cols].to_csv(out_dir / 'train.csv', index=False)
    val[cols].to_csv(out_dir / 'val.csv', index=False)
    test[cols].to_csv(out_dir / 'test.csv', index=False)
    print(f"\n✓ Kaydedildi: {out_dir}/train.csv, val.csv, test.csv")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--gold-path', default='data/raw/tweets_etiketli.xlsx')
    p.add_argument('--pseudo-path', default='data/raw/depremGun5_düzenlendi.xlsx')
    p.add_argument('--out-dir', default='data')
    p.add_argument('--seed', type=int, default=42)
    args = p.parse_args()
    main(args)
