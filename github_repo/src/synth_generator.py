"""
Sentetik Türkçe Afet Tweet Üreteci
====================================
Template-based üretim — az örnekli sınıflar için (kayip, altyapi, bagis).
Final raporda bu sentetik verinin oluşturduğu limitation dürüstçe belirtilecek.
"""
import random


# -----------------------------------------------------------------------------
# Kaynak listeler
# -----------------------------------------------------------------------------
ISIMLER = [
    "Ahmet Yılmaz", "Mehmet Demir", "Fatma Şahin", "Ayşe Kaya", "Ali Çelik",
    "Hatice Arslan", "Emine Doğan", "Hasan Koç", "Mustafa Yıldız", "Zeynep Aksoy",
    "İbrahim Polat", "Hüseyin Çakır", "Elif Öztürk", "Murat Şimşek", "Cemil Türk",
    "Selma Korkmaz", "Yusuf Çetin", "Esra Avcı", "Burak Erdoğan", "Sevgi Acar",
    "Okan Güneş", "Buket Aydın", "Kerem Yalçın", "Pınar Kurt", "Erkan Bulut",
    "Nihal Erdem", "Caner Özkan", "Şeyma Tunç", "Tolga Yavuz", "Beyza Karaca",
    "Furkan Acar", "Melike Kılıç", "Onur Türkoğlu", "Gülşen Sarı", "Berkay Yıldırım",
    "Cansu Kavlak", "Eda Polat", "Burak Aydemir", "Şevval Gültekin", "Enes Çulhacıoğlu",
    "Muhammet Sarı", "Pelin Güneş", "Dilan Polat", "Abdülsamet Erdağlı",
]

SEHIRLER_ILCELER = [
    ("Kahramanmaraş", ["Onikişubat", "Dulkadiroğlu", "Pazarcık", "Elbistan", "Türkoğlu", "Afşin", "Andırın"]),
    ("Hatay", ["Antakya", "İskenderun", "Defne", "Samandağ", "Kırıkhan", "Reyhanlı", "Dörtyol", "Belen"]),
    ("Adıyaman", ["Merkez", "Kahta", "Besni", "Gölbaşı", "Tut"]),
    ("Gaziantep", ["Şahinbey", "Şehitkamil", "Nurdağı", "İslahiye", "Nizip"]),
    ("Malatya", ["Yeşilyurt", "Battalgazi", "Doğanşehir", "Akçadağ"]),
    ("Osmaniye", ["Merkez", "Düziçi", "Kadirli"]),
    ("Diyarbakır", ["Bağlar", "Yenişehir", "Kayapınar"]),
    ("Şanlıurfa", ["Haliliye", "Karaköprü", "Eyyübiye"]),
    ("Kilis", ["Merkez", "Polateli", "Elbeyli"]),
    ("Adana", ["Seyhan", "Yüreğir", "Çukurova"]),
]

MAHALLELER = [
    "Sümerler Mh.", "Hayrullah Mh.", "Mimar Sinan Mh.", "Yavuz Selim Mh.",
    "Atatürk Mh.", "Cumhuriyet Mh.", "İnönü Mh.", "Yeşilköy Mh.",
    "Kurtuluş Mh.", "Bahçelievler Mh.", "Yenimahalle", "Yıldız Mh.",
    "Barbaros Mh.", "Fevzipaşa Mh.", "Şehit Kemal Mh.", "Ekinci Mh.",
    "İsmetpaşa Mh.", "Hisarpaşa Mh.", "Yenidoğan Mh.", "Karşıyaka Mh.",
]

SOKAKLAR = [
    "726. Sokak", "1845. Sokak", "Atatürk Caddesi", "İnönü Bulvarı",
    "Cumhuriyet Caddesi", "Borsa Caddesi", "Gazi Bulvarı", "Mevlana Sokak",
    "Yıldırım Sokak", "Şehit Onbaşı Sokak", "12. Sokak", "85. Sokak",
    "Defne Sokak", "Çamlık Sokak", "Çağrı Sokak", "Sümer Caddesi",
]


def _telefon():
    return f"05{random.randint(30, 59):02d} {random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}"


def _adres():
    sehir, ilceler = random.choice(SEHIRLER_ILCELER)
    ilce = random.choice(ilceler)
    mh = random.choice(MAHALLELER)
    sk = random.choice(SOKAKLAR)
    no = random.randint(1, 200)
    apt = random.choice(["", f"{random.choice(['Yıldız', 'Gül', 'Çiçek', 'Doğa', 'Asel', 'Hisar'])} Apt.", "Sitesi", ""])
    if apt:
        return f"{sehir} {ilce} {mh} {sk} No:{no} {apt} Kat:{random.randint(1, 8)}"
    return f"{sehir} {ilce} {mh} {sk} No:{no}"


# -----------------------------------------------------------------------------
# KAYIP_BILDIRIMI TEMPLATE'LERİ
# -----------------------------------------------------------------------------
KAYIP_TEMPLATES = [
    "{name} isimli yakınımıza {addr} adresinde ulaşamıyoruz. Gören duyan haber versin lütfen. İletişim: {phone}",
    "ACİL! {name} ve ailesinden 2 gündür haber alamıyoruz. {addr} bölgesinde. Bilgisi olan iletişime geçsin.",
    "{addr} adresinden {name}'a ulaşamıyoruz. Telefonu kapalı. Tanıyan var mı?",
    "Kuzenim {name} {addr} adresinde, depremden sonra haber alamadık. Yardım edin lütfen.",
    "Arkadaşım {name}'a ulaşamıyoruz. Son bilinen konum: {addr}. Bilen varsa {phone} numarasını arasın.",
    "HALA KAYIP! {name} - {addr}. Ailesi arıyor, gören olur mu lütfen paylaşır mısınız?",
    "{name} 24 saattir kayıp. {addr} civarında olabilir. Bilgisi olan {phone} ile irtibata geçsin.",
    "Kız kardeşim {name}'dan haber yok, telefonu açmıyor. Adres: {addr}. Allah rızası için yardım.",
    "TEYİTLİ - {name} ailesi {addr} adresinde, enkaz altında olabilir. İletişim kuramıyoruz.",
    "{name} dün gece evden çıkmış, ailesi haber alamıyor. {addr} bölgesinde aranıyor. {phone}",
    "Akrabamız {name} {addr} adresinde ikamet ediyordu. Halen ulaşamıyoruz, durumu bilen var mı?",
    "Babam {name} {addr} adresinde, 36 saattir haber alamadık. Bölgedeki son durum nedir bilen yok mu?",
    "Annem {name} ile telefon görüşmemiz kesildi. {addr} adresinde. Lütfen yayın, görenler {phone}'u arasın.",
    "Komşumuz {name} ailesi {addr} adresinde, depremden bu yana ulaşamıyoruz, yardım edin.",
    "Yeğenim {name} - {addr} - 48 saattir kayıp. Hastane kayıtlarında da yok. Lütfen RT.",
]

# -----------------------------------------------------------------------------
# ALTYAPI_HASARI TEMPLATE'LERİ
# -----------------------------------------------------------------------------
ALTYAPI_TEMPLATES = [
    "{sehir} {ilce} bölgesinde {bina_sayi} {kat} katlı bina yıkıldı. Ekipler arama-kurtarma çalışmasına başladı.",
    "{sehir} merkezde elektrik kesintisi devam ediyor, internet ve telefon hatları çalışmıyor.",
    "{sehir} {ilce} - {sokak} caddesinde köprü çökmüş, yol tamamen kapalı, ulaşım sağlanamıyor.",
    "Şu an {sehir} {ilce}'de su ve doğalgaz kesintisi var, evler ısıtılamıyor.",
    "{sehir}'de viyadük hasar gördü, geçişler durduruldu. Alternatif güzergahlar kullanılmalı.",
    "{sehir} {ilce}'de baz istasyonu çöktü, şebeke yok, iletişim sağlanamıyor.",
    "ACİL DUYURU: {sehir} havalimanı kapalı, uçuşlar iptal edildi. Yardım uçakları alternatif noktalara yönlendirildi.",
    "{sehir} {ilce} bölgesinde {bina_sayi} apartman tamamen yıkılmış durumda, enkaz kaldırma sürüyor.",
    "{sehir} hastanesi kısmen hasar gördü, hastalar başka illere sevk ediliyor.",
    "{sehir} {ilce}'ye giden ana yol çökmüş, sadece iş makinesiyle ulaşılabiliyor.",
    "{sehir}'de tünel hasar görmüş, geçici olarak kapatıldı. Yetkililer çalışma yapıyor.",
    "{sehir} {ilce} bölgesinde çok sayıda bina yıkıldı, altyapı tamamen çöktü.",
    "{sehir}'de elektrik şebekesi hasarlı, tüm ilçede karanlık. AYEDAŞ ekipleri sahada.",
    "{sehir} {ilce}'de doğalgaz hattı patladı, bölge tahliye ediliyor.",
    "{sehir} merkezde internet altyapısı çöktü, fiber kablolar hasarlı, onarım sürüyor.",
    "{sehir} {ilce} - 8 katlı binanın 3 katı çökmüş, ekipler arama yapıyor.",
    "{sehir}'de iletişim hatları tamamen kesik, GSM operatörleri uydu üzerinden destek sağlıyor.",
    "{sehir} {ilce} okul binası ağır hasarlı, yıkılma riski olduğundan tahliye edildi.",
    "{sehir} otogarı hasar gördü, ulaşım geçici olarak {alt_sehir}'e kaydırıldı.",
    "{sehir} {ilce} bölgesinde su şebekesi çöktü, içme suyu tankerlerle dağıtılıyor.",
]

# -----------------------------------------------------------------------------
# BAGIS_KOORDINASYON TEMPLATE'LERİ
# -----------------------------------------------------------------------------
BAGIS_TEMPLATES = [
    "Deprem bölgesine bağış için: AHBAP Derneği İş Bankası IBAN: TR{iban}",
    "AFAD bağış kampanyasına destek olmak isteyenler için IBAN bilgileri açıklandı.",
    "Kızılay yardım kampanyası başladı. Bağış için: TR{iban} açıklama: deprem.",
    "Yardım kolisi hazırlayanlar lütfen: bebek bezi, ıslak mendil, pişik kremi, mama, battaniye koysun.",
    "{sehir} toplama merkezi açıldı. Adres: {addr}. Tıbbi malzeme, gıda, temizlik ürünleri kabul ediliyor.",
    "Gönüllüler aranıyor: {sehir} depo merkezinde koli hazırlama için. Başvuru: {phone}",
    "{sehir}'den {hedef_sehir}'a tır geliyor, doldurulacak malzemeler için irtibat: {phone}",
    "Bağışlarınız için Ahbap Derneği'nin tüm hesap bilgileri sosyal medya hesaplarında.",
    "Kan bağışı kampanyası: {sehir}'de Kızılay merkezleri 24 saat açık. Acil kan ihtiyacı var.",
    "Yardım toplama noktası: {addr}. Gönüllü ve fiziksel destek bekleniyor.",
    "Minibüsümüz {hedef_sehir} bölgesine hareket edecek. Bağışlanacak gıda ve battaniye için {phone}",
    "AKUT'a bağış için: TR{iban}. Tüm bağışlar afet bölgesine yönlendirilecektir.",
    "Tıbbi malzeme kampanyası: doktor önerili ilaçlar, sargı bezi, antiseptik aranıyor. Toplama: {addr}",
    "Üniversitemizde yardım toplama merkezi kuruldu. Gıda, kıyafet, oyuncak kabul ediliyor.",
    "Kira kampanyası: depremzedelere konut açmak isteyenler için koordinasyon yapılıyor. {phone}",
    "Kıyafet bağışı için kategorize edilmiş paketler hazırlayın: kadın/erkek/çocuk, yetişkin/bebek olarak ayırın.",
    "Lojistik destek: {sehir}'den {hedef_sehir}'a bağış aracı arıyoruz. Ücret karşılanır. {phone}",
    "AHBAP Derneği'nin {sehir} deposu açıldı, malzeme kabul ediyor, gönüllü çağrısı yapıldı.",
    "Bağış kampanyamıza katılmak isteyen vatandaşlarımız için IBAN: TR{iban} - Açıklama: Maraş.",
    "Kan ve plazma bağışı için: Tüm Türkiye Kızılay merkezleri yoğunluğa rağmen kabul devam ediyor.",
]


# -----------------------------------------------------------------------------
# Üretim fonksiyonları
# -----------------------------------------------------------------------------
def gen_kayip(n: int, seed: int = 42) -> list:
    random.seed(seed)
    out = []
    for _ in range(n):
        tmpl = random.choice(KAYIP_TEMPLATES)
        text = tmpl.format(
            name=random.choice(ISIMLER),
            addr=_adres(),
            phone=_telefon(),
        )
        out.append(text)
    return out


def gen_altyapi(n: int, seed: int = 42) -> list:
    random.seed(seed + 1)
    out = []
    for _ in range(n):
        sehir, ilceler = random.choice(SEHIRLER_ILCELER)
        ilce = random.choice(ilceler)
        sehir2, _ = random.choice(SEHIRLER_ILCELER)
        tmpl = random.choice(ALTYAPI_TEMPLATES)
        text = tmpl.format(
            sehir=sehir, ilce=ilce, alt_sehir=sehir2,
            sokak=random.choice(SOKAKLAR),
            bina_sayi=random.choice(["birkaç", "5", "10", "8", "12", "20"]),
            kat=random.choice(["3", "4", "5", "6", "8"]),
        )
        out.append(text)
    return out


def gen_bagis(n: int, seed: int = 42) -> list:
    random.seed(seed + 2)
    out = []
    for _ in range(n):
        sehir, _ = random.choice(SEHIRLER_ILCELER)
        sehir2, _ = random.choice(SEHIRLER_ILCELER)
        # IBAN benzeri rastgele 22 hane (gerçek IBAN değil)
        iban = " ".join(f"{random.randint(0, 9999):04d}" for _ in range(5)) + f" {random.randint(0, 99):02d}"
        tmpl = random.choice(BAGIS_TEMPLATES)
        text = tmpl.format(
            sehir=sehir, hedef_sehir=sehir2,
            addr=_adres(), phone=_telefon(), iban=iban,
        )
        out.append(text)
    return out


if __name__ == "__main__":
    print("=== KAYIP ÖRNEKLERİ ===")
    for t in gen_kayip(5):
        print(f"  • {t}")
    print("\n=== ALTYAPI ÖRNEKLERİ ===")
    for t in gen_altyapi(5):
        print(f"  • {t}")
    print("\n=== BAGIS ÖRNEKLERİ ===")
    for t in gen_bagis(5):
        print(f"  • {t}")
