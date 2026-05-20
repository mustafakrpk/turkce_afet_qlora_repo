# Etik Değerlendirme

## Bağlamsal Bütünlük (Contextual Integrity)

Twitter'da paylaşılan tweet'ler **kamuya açık** olsalar da, depremzedelerin yardım çağrıları belirli bir bağlam (acil durum) için paylaşılmıştır. Bu verilerin **afet yönetimi dışındaki amaçlarla** kullanılması (örn. ticari profilleme, hedefli reklam) etik dışıdır.

**Aldığımız önlemler:**
- Mention'lar (`@kullanici`) `[USER]` ile değiştirilerek anonimleştirildi
- Tüm telefon numaraları ve adresler — analitik amaç dışında — yayınlanan veri setinde tutulmuyor
- Çalışma sonunda ham veriler proje teslim sürecinde imha edilecektir

## Algoritmik Önyargı ve Temsiliyet

Twitter kullanıcı tabanı **tüm Türkiye toplumunu temsil etmez**:

- Yaş dağılımı: ağırlıklı 18-45 yaş
- Coğrafi: kentsel kullanıcılar baskın
- Dil yetkinliği: yazılı Türkçe okur-yazarlığı gerektirir
- Teknolojiye erişim: depremden zarar görmüş bölgelerde **internet kesintisi** nedeniyle bazı çağrılar sistemde temsil edilmez

**Sonuç:** Bu model **tek başına karar verici değildir**. İnsan operatörlere yardımcı bir karar destek aracı olarak konumlandırılmıştır. Otomatik kararların hayati sonuçları olabilecek durumlarda (örn. kurtarma ekibi yönlendirme), insan onayı zorunludur.

## Yanlış Bilgilendirme Riski

Afet dönemlerinde sosyal medyada **kasıtlı sahte yardım çağrıları** ve **manipülatif içerikler** dolaşır. Bu çalışmadaki model, içeriğin **doğruluğunu** değil, **operasyonel sınıfını** tespit eder. 

**Öneri:** Üretim ortamında doğrulama mekanizmaları (örn. konum doğrulama, kaynak güvenirliği skorlaması) ile entegre edilmelidir.

## Sentetik Veri Beyanı

Eğitim setinde 1.663 örnek (~%16) **template-based sentetik veri**dir. Bu örneklerdeki:
- İsimler gerçek Türk isimleri olabilir ama **kişiyle ilişkisizdir**
- Adresler gerçek mahalle/sokak adları olabilir ama **rastgele kombinasyondur**
- Telefon numaraları gerçek format ama **rastgele rakamlardır**

Sentetik örneklerin **VAL/TEST setlerinde olmaması**, model değerlendirmesinin gerçek dağılım üzerinden yapılmasını sağlar.

## Zayıf Etiketleme Beyanı

47.079 ham tweet kural tabanlı zayıf etiketleyici (`weak_labeler_v2.py`) ile etiketlenmiştir. Manuel kontrolde tahmini doğruluk **%70-80**. Bu **gürültülü etiket** model performansına yansır ve raporun **limitations** bölümünde dürüstçe belirtilmiştir.

## Açık Kaynak ve Reproducibility

- Tüm kod, veri pipeline'ı ve hiperparametreler GitHub'da açık
- Seed=42 ile tüm split ve eğitim sonuçları yeniden üretilebilir
- Model adaptörleri ve sonuç dosyaları paylaşılır

## Kullanım Tavsiyeleri

✅ **Uygun kullanımlar:**
- Afet sonrası ilk saatlerde tweet akışını sınıflara ayırma
- Karar destek panelleri için sınıf bazlı filtreleme
- Akademik karşılaştırma çalışmaları

❌ **Uygunsuz kullanımlar:**
- Otomatik kurtarma ekibi yönlendirme (insan onayı olmadan)
- Ticari pazarlama amacıyla kullanıcı profilleme
- Sahte/gerçek çağrı ayrımı (model bunu öğrenmemiştir)
- Genel olarak duygu analizi veya kullanıcı duygu durumu tahmini

## Çatışan Çıkar Beyanı

Bu çalışma akademik bir dönem projesidir, finansman kaynağı yoktur. Yazarın hiçbir kuruluşla çıkar ilişkisi bulunmamaktadır.
