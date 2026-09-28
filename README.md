# 📚 Sokak Ağzıyla Kitap Özeti Botu (Twitter / X)

Kitapları daha az sıkıcı hale getirmek ve herkesin anlayacağı şekilde kafaya sokmak için tasarlanmış **"Sokak Ağzıyla Kitap Botu"**.

Dünya klasiklerini ve popüler kitapları baştan sona bölümlere ayırır, her bölümü 3-5 cümlelik komik sokak ağzıyla anlatır ve Twitter'a (X) seri/thread olarak paylaşır.

Dışarıdan pahalı bir yapay zeka API'sine ihtiyaç duymadan, önceden hazırlanmış zengin sokak kütüphanesiyle veya asistanınızla ürettiğiniz yeni kitaplarla **ücretsiz ve tam kontrolde** çalışır.

---

## 🎯 Özellikler

- **Mizahi & Sokak Ağzı Anlatım**: Her bölüm 3-5 vurucu ve komik sokak cümlesi + günün hayat dersi ile özetlenir.
- **Twitter Thread / Tek Tweet Uyumu**: Twitter'ın 280 karakter limitine göre otomatik hesaplama yapar. Uzun bölümleri kesintisiz thread (`1/2 🧵`, `2/2`) haline getirir.
- **Sıralı İlerleme (State Tracking)**: Hangi kitabın kaçıncı bölümünde kalındığını `data/state.json` içinde hatırlar; her çalıştığında sonraki bölüme geçer, kitap bitince bir sonrakine geçer.
- **DRY-RUN (Simülasyon) Modu**: Twitter API anahtarınız olmasa bile terminalde renkli panel arayüzüyle tüm tweetleri önizleyebilirsiniz.
- **Canlı Twitter Modu**: `.env` dosyasına Twitter API v2 anahtarlarınızı ekleyerek gerçek hesabınıza tweet attırabilirsiniz.

---

## 🚀 Başlangıç

### 1. Bağımlılıkları Yükleyin

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 💻 Kullanım Komutları

### 1. Kütüphanedeki Kitapları Listele
```bash
python main.py list
```

### 2. Bir Kitabın Sokak Ağzı Özetini Baştan Sona Oku
```bash
python main.py preview suc_ve_ceza
# veya
python main.py preview donusum
python main.py preview 1984
python main.py preview yabanci
python main.py preview kucuk_prens
```

### 3. Sıradaki Bölümü Tweetle (Simülasyon / Dry-Run)
Herhangi bir API key olmadan terminalde canlı tweet önizlemesi yapar:
```bash
python main.py tweet
```

### 4. Gerçek Twitter Hesabına Tweet Atma (Canlı)
`.env` dosyasını yapılandırdıktan sonra:
```bash
python main.py tweet --live
```

### 5. Aktif Kitabı veya Bölümü Değiştirme
```bash
python main.py set-book 1984 --chapter 1
```

---

## 📦 Mevcut Başlangıç Kitapları

1. **Suç ve Ceza (Fyodor Dostoyevski)** — Aşırı zekiyim triplerine girip tefeci teyzeyi indiren Raskolnikov'un vicdan azabıyla kafayı yeme serüveni.
2. **Dönüşüm (Franz Kafka)** — Sabah kalkıp devasa bir böceğe dönüşen ama hala "işe nasıl yetişecem" diye dertlenen plazacı ruhlu Gregor'un dramı.
3. **1984 (George Orwell)** — Her köşede mobese gibi Büyük Birader'in dikildiği, aşık olmanın bile vatan hainliği sayıldığı distopik kabus.
4. **Yabancı (Albert Camus)** — Annesi vefat ettiğinde dondurma yiyip ertesi gün plajda güneşe sinirlenip adam vuran iflah olmaz gamsız Meursault.
5. **Küçük Prens (Antoine de Saint-Exupéry)** — Uçağı çöle düşen pilot ile gezegen gezegen gezip "büyükler harbi kafasız" diyen sarı saçlı veledin felsefesi.

---

## ➕ Yeni Kitap Ekleme

Yeni kitap eklemek için `data/books/<kitap_id>.json` dosyası oluşturmanız veya asistanınıza *"Bana X kitabını sokak ağzıyla bölüm bölüm çıkar"* demeniz yeterlidir. JSON formatı:

```json
{
  "id": "yeni_kitap",
  "title": "Kitap Adı",
  "author": "Yazar",
  "tagline": "Tek cümlelik komik özet",
  "chapters": [
    {
      "chapter_num": 1,
      "title": "Bölüm 1: Başlık",
      "content": "3-5 cümlelik sokak anlatımı...",
      "key_takeaway": "Kısa ders"
    }
  ]
}
```

---

## 🧪 Testleri Çalıştırma

```bash
.venv/bin/pytest -v
```
