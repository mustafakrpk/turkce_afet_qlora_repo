"""
Weak Labeler v2 — Sıkılaştırılmış Kurallar
============================================
v1'deki sorunlar:
  - "yardım" tek kelimesi yardım_talebi'ne çekiyor (siyasi yorumlar yanlış pozitif)
  - "yıkıldı" metaforik kullanım (geçmiş, hayaller) altyapı_hasarı'na gidiyor
  - "AHBAP" tek başına bağış sınıfı sayılıyor (eleştiri tweet'leri)

v2 düzeltmeleri:
  1. MIN_SCORE eşiği: bir sınıfa atanabilmek için skor >=2 olmalı (genelde)
  2. Metafor filtresi: altyapı_hasarı için somut yer/sayı/adres ipucu zorunlu
  3. Bağlam filtresi: siyasi/dua/eleştiri sinyalleri varsa skoru kıs
  4. Kombinasyon zorunluluğu: "yardım" tek değil, "yardım+lazım/edin/bekliyor" gibi
"""
import re

# -----------------------------------------------------------------------------
# REGEX PATTERNS — kombinasyon zorunlulukları
# -----------------------------------------------------------------------------

# YARDIM_TALEBI — somut talep + nesne gerekli
YARDIM_PATTERNS = [
    # "yardım + edin/bekliyor/gerekli/ihtiyaç"
    r"yard[ıi]m\s+(edin|bekliy|gerek|ihtiya|göndr|gönd|laz[ıi]m|isteyen)",
    r"yardimedin|yardimlazim",
    # Doğrudan acil ifadeler
    r"acil\s+(yard[ıi]m|vinç|vinc|kepçe|kepce|ekip|destek|t[ıi]bbi|m[uü]dah|kurtarma)",
    r"l[uü]tfen\s+(yard[ıi]m|duyur|yay|payla)",
    # Kurtarma operasyonu
    r"ses\s+(var|geliyor|al[ıi]nd|duyul)",
    r"sismik\s+dinleme",
    r"enkaz\s+(alt[ıi]nda|alti)",
    r"alt[ıi]nda\s+(kal|insan|ses|aile|hay|göç|gocu)",
    r"hayat\s+var",
    r"canl[ıi]\s+var",
    # Malzeme talebi — ihtiyaç maddesi + lazım/ihtiyaç
    r"(çad[ıi]r|cadir|battaniye|g[ıi]da|[ıi]s[ıi]t[ıi]c[ıi]|soba|yakacak|yiyecek|"
    r"su|[ıi]la[çc]|mama|bebek\s+bez|kıyafet|kiyafet|mont|kömür|odun)\s+"
    r"(laz[ıi]m|ihtiya|gerek|gönd|yetiş|gerekli)",
    # Sosyal yayma çağrısı — yardım çağrılarının tipik formu
    r"yayar\s+m[ıi]s[ıi]n[ıi]z",
    r"rt\s+yapar\s+m[ıi]s[ıi]n[ıi]z",
    r"duyurur\s+m[ıi]s[ıi]n[ıi]z",
    # Vinç/kepçe + lazım/lutfen
    r"(vin[çc]|kep[çc]e|i[şs]\s+makin|operat[öo]r)\s+(laz[ıi]m|gerek|ihtiya)",
    # Kurtarın/yardım edin direkt komut
    r"\bkurtar[ıi]n\b",
]

# KAYIP_BILDIRIMI — somut "ulaşamıyorum" sinyalleri
KAYIP_PATTERNS = [
    r"ula[şs][ıi]l?am[ıi]yor(uz|um|lar)?",
    r"ula[şs]am[ıi]yor(uz|um)",
    r"ula[şs]amad[ıi](k|m)",
    r"haber\s+alam(ad|[ıi]yor)",
    r"telefon\s+(a[çc]m[ıi]yor|kapal[ıi])",
    r"telefonuna\s+(ula[şs]|cevap)",
    r"ileti[şs]im\s+(kurulam|kuram|sa[ğg]lana)",
    r"haberi\s+olan\s+(var\s+m[ıi]|bilen)",
    r"g[öo]ren\s+(var\s+m[ıi]|olan)",
    r"tan[ıi]yan\s+var\s+m[ıi]",
    r"bilgi(si)?\s+olan",
    r"\bkayb[ıi]m(\s|ız)",
    r"kayboldu(\s|\.)",
    r"nerede\s+oldu[ğg]u(nu|nuz)",
    r"yak[ıi]n[ıi]\s+ar[ıi]yor",
]

# ALTYAPI_HASARI — metafor değil, somut yer bilgisi ile gelmeli
ALTYAPI_PATTERNS = [
    # Bina/yapı — gerçek hasar (esnek: yıkıl/yıkık/yıkılmış/çöktü/çöken/çökmüş)
    r"bina(lar)?\s+(y[ıi]k[ıi]l|[çc][öo]k|hasar)",
    r"(y[ıi]k[ıi]l|y[ıi]k[ıi]k|[çc][öo]k(t|m|en|s))\w*\s+bina",
    r"(y[ıi]k[ıi]l|[çc][öo]k(t|m|en))\w*\s+apartman",
    r"yerle\s+bir\s+(oldu|olmu[şs])",
    # Yol/köprü/altyapı somut
    r"yol(lar)?\s+(kapal[ıi]|[çc][öo]k|y[ıi]k[ıi]l|hasar|ge[çc][ıi]lm)",
    r"yol(lar)?\s+(tamamen|kapal[ıi])?\s*[çc][öo]k",
    r"k[öo]pr[uü](ler)?\s+(y[ıi]k[ıi]l|[çc][öo]k|hasar|kapal[ıi])",
    r"(y[ıi]k[ıi]l|[çc][öo]k(t|m|en))\w*\s+k[öo]pr[uü]",
    r"viyad[uü]k\s+(y[ıi]k|[çc][öo]k)",
    r"t[uü]nel(ler)?\s+(kapal[ıi]|[çc][öo]k|hasar)",
    r"havaalan[ıi]?\s+(kapal[ıi]|hasar)",
    r"havaliman[ıi]?\s+(kapal[ıi]|hasar)",
    # Şebeke/altyapı kesintisi
    r"elektrik(ler)?\s+(yok|kesik|kesinti|gelmiyo|gitti)",
    r"\bsu(\s|lar)?\s+(yok|kesinti|gelmiyo|kesil)",
    r"do[ğg]al?gaz\s+(yok|kesil|ka[çc]a)",
    r"internet\s+(yok|kesinti|gelmiyor|[çc]al[ıi][şs]m)",
    r"[şs]ebeke\s+(yok|kesil|[çc][öo]k)",
    r"baz\s+istasyon",
    r"hastane(ler)?(\s|nin|ye)\s+(y[ıi]k|[çc][öo]k|hasar)",
]

# BAGIS_KOORDINASYON — somut bağış/lojistik organizasyonu
BAGIS_PATTERNS = [
    # IBAN/hesap bilgisi
    r"iban\s*(no|num)?",
    r"\btr\d{2}\s*\d{4}",  # IBAN formatı
    r"hesap\s+(no|num|bilg)",
    # Organizasyonlar + somut aktivite
    r"(ahbap|k[ıi]z[ıi]lay|afad|akut|tider)(\s|\.)\s*(ba[ğg][ıi][şs]|yard[ıi]m\s+toplam|deposu|merkez|kampany|kol[ıi]|t[ıi]r)",
    r"ba[ğg][ıi][şs]\s+(kampany|toplam|merkez|noktas|i[çc]in|yapan|yapmak)",
    # Lojistik
    r"yard[ıi]m\s+(toplam|merkez|depo|noktas|kampany|g[öo]nder|yolla|kol[ıi])",
    r"toplama\s+(merkez|noktas)",
    r"depo(\s|su|muz)\s+(a[çc][ıi]ld|kurul|haz[ıi]r)",
    # Araç/tır/kargo bağışları
    r"t[ıi]r\s+(haz[ıi]r|geliyor|y[üu]kledik|dol|y[öo]nlendir|laz[ıi]m)",
    r"minib[üu]s\s+(doldur|haz[ıi]r|geliyor)",
    r"ara[çc]\s+(doldur|y[üu]klendi)",
    # Gönüllülük
    r"g[öo]n[üu]ll[üu]\s+(ar[ıi]yor|ihtiya|olabilec|olmak|kay[ıi]t|alma)",
    # Koli içeriği
    r"kol[ıi](ler)?(e|ye)\s+(ne|hangi|koyal[ıi]m|koyul|i[çc]ine)",
    r"yard[ıi]m\s+kol[ıi]s[ıi]",
]


# Negative / downweight signals — varsa skoru kır
SIYASI_PATTERNS = [
    r"ak\s*parti|akp|chp|mhp|hdp|[ıi]yi\s+parti|deva",
    r"iktidar|muhalefet|h[üu]k[uü]met(in|i\s+ele[şs])",
    r"siya(si|set)",
    r"oy\s+ver|se[çc]im",
]

DUA_PATTERNS = [
    r"allah\s+(rahmet|raz[ıi]|bela)",
    r"rahmet\s+eylesin|mekan[ıi]\s+cennet|nur\s+i[çc]inde",
    r"ba[şs][ıi]n[ıi]?\s+sa[ğg]olsun",
    r"taziye",
    r"can[ıi]m[ıi]z\s+sa[ğg]",
    r"ya\s+rab[bi]|rab+im",
]

METAFOR_PATTERNS = [
    r"ge[çc]mi[şs](im|imiz)?\s+y[ıi]k[ıi]ld",
    r"hayal(im|imiz|ler|leri)?\s+y[ıi]k[ıi]l",
    r"d[üu]nyam(\s|[ıi]z)?\s+y[ıi]k[ıi]ld",
    r"y[üu]re[ğg]im(\s|iz)?\s+y[ıi]k[ıi]l",
    r"benlik\s+y[ıi]k[ıi]ld",
    r"y[ıi]k[ıi]ld[ıi]\s+i[çc]im",
]


def normalize_tr(text: str) -> str:
    if not isinstance(text, str):
        return ""
    t = text.lower()
    t = t.replace("İ", "i").replace("I", "ı")
    t = re.sub(r"http\S+|www\.\S+", " ", t)
    t = re.sub(r"@\w+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


TELEFON_PATTERN = re.compile(r"(?:\+?90)?\s*0?5\d{2}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}")
ADRES_PATTERN = re.compile(r"\bmah(\.|alle)|sok(\.|ak)|cad(\.|de)|apt\.|apartman|\bblok\b|\bdaire\b", re.IGNORECASE)
# Şehir/ilçe adı listesi — somut yer ipucu için
KONUM_KEYWORDS = ["hatay", "antakya", "kahramanmaras", "kahramanmaraş", "maras", "maraş",
                  "ad[ıi]yaman", "elbistan", "pazarcik", "pazarcık", "gaziantep", "antep",
                  "nurdag", "nurdağ", "islahiye", "kilis", "osmaniye", "diyarbakir",
                  "diyarbakır", "urfa", "şanl[ıi]urfa", "samandağ", "samandag", "kirikhan",
                  "kırıkhan", "iskenderun", "defne", "dörtyol", "dortyol"]


def count_pattern_matches(text: str, patterns: list) -> int:
    cnt = 0
    for p in patterns:
        if re.search(p, text):
            cnt += 1
    return cnt


def has_konum(text: str) -> bool:
    for k in KONUM_KEYWORDS:
        if re.search(rf"\b{k}\b", text):
            return True
    return False


def classify_tweet_v2(text: str, min_score: int = 1) -> tuple:
    """
    v2 sınıflandırıcı — daha sıkı, bağlam farkındalıklı.
    Returns: (label_id, label_name, scores_dict, debug_info)
    """
    t = normalize_tr(text)
    if len(t) < 10:
        return 4, "diger_ilgisiz", {}, {"reason": "too_short"}

    # Bağlam bayrakları
    is_siyasi = count_pattern_matches(t, SIYASI_PATTERNS) >= 1
    is_dua = count_pattern_matches(t, DUA_PATTERNS) >= 1
    has_metafor = count_pattern_matches(t, METAFOR_PATTERNS) >= 1
    has_phone = bool(TELEFON_PATTERN.search(t))
    has_addr = bool(ADRES_PATTERN.search(t))
    has_loc = has_konum(t)

    scores = {
        0: count_pattern_matches(t, YARDIM_PATTERNS),
        1: count_pattern_matches(t, KAYIP_PATTERNS),
        2: count_pattern_matches(t, ALTYAPI_PATTERNS),
        3: count_pattern_matches(t, BAGIS_PATTERNS),
    }

    # GÜÇLENDİRMELER

    # Telefon + adres => yardım sinyali güçlü (yardım çağrılarının tipik formu)
    if has_phone and has_addr:
        scores[0] += 2

    # Telefon + somut konum => yardım sinyali
    elif has_phone and has_loc:
        scores[0] += 1

    # ZAYIFLATMALAR

    # Siyasi tweet ise yardım & altyapı skorlarını kır
    if is_siyasi:
        scores[0] = max(0, scores[0] - 2)
        scores[2] = max(0, scores[2] - 2)
        scores[3] = max(0, scores[3] - 1)

    # Dua tweet'i ise tüm skorları kır (genelde "diger" sınıfına ait)
    if is_dua:
        for k in scores:
            scores[k] = max(0, scores[k] - 1)

    # Metafor varsa altyapı skorunu yok et
    if has_metafor:
        scores[2] = 0

    # Altyapı sınıfı için: somut yer ipucu olmadan kabul etme
    if scores[2] > 0 and not (has_loc or has_addr):
        # Metaforik veya genel yorum — şüpheli
        scores[2] = max(0, scores[2] - 1)

    # KARAR

    max_score = max(scores.values())
    if max_score < min_score:
        return 4, "diger_ilgisiz", scores, {
            "siyasi": is_siyasi, "dua": is_dua, "metafor": has_metafor,
            "phone": has_phone, "addr": has_addr, "loc": has_loc,
        }

    # En yüksek skorlu sınıf (tie-break: 1 (kayıp) > 0 (yardım) > 2 > 3)
    # Bunun nedeni: kayıp daha nadir, eşitlikte ona öncelik ver
    priority = {1: 0, 0: 1, 2: 2, 3: 3}
    best = max(scores, key=lambda k: (scores[k], -priority[k]))

    label_names = {
        0: "yardim_talebi", 1: "kayip_bildirimi", 2: "altyapi_hasari",
        3: "bagis_koordinasyon", 4: "diger_ilgisiz",
    }
    return best, label_names[best], scores, {
        "siyasi": is_siyasi, "dua": is_dua, "metafor": has_metafor,
        "phone": has_phone, "addr": has_addr, "loc": has_loc,
    }


if __name__ == "__main__":
    test_samples = [
        ("ACİL VİNÇ VE KEPÇE LAZIM SES VAR ‼️ Mah. Sok. 05379290473", 0),
        ("Kardeşime ulaşamıyoruz Antakya Sümerler mahallesinde.", 1),
        ("Hatay'da yollar tamamen çökmüş, köprü yıkılmış", 2),
        ("AHBAP IBAN: TR12 0006 4000 0011 bağış kampanyası", 3),
        ("Allah rahmet eylesin, mekanı cennet olsun", 4),
        ("Bugün hava güzel, kahve içtim.", 4),
        # Önceki versiyonun hatalı çıkardıkları
        ("Geçmişimiz yıkıldı ama geleceğimizi sağlam inşa edeceğiz.", 4),
        ("AKP iktidarı yardımları geç gönderdi", 4),  # siyasi
        ("AFAD da bizim AHBAP da! Yanındayım", 4),  # sadece isim, bağış değil
        ("Allah belanızı versin yağmacı şerefsizler", 4),  # küfür/eleştiri
    ]
    for s, expected in test_samples:
        lbl_id, lbl_name, sc, dbg = classify_tweet_v2(s)
        marker = "✅" if lbl_id == expected else "❌"
        print(f"{marker} [pred={lbl_id} {lbl_name:20s} | exp={expected}] {s[:75]}")
        print(f"   skorlar={sc} debug={dbg}\n")
