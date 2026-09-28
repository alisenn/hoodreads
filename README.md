# 💀 HoodReads — Books from the Hood

> **Goodreads, but from the hood.**  
> Kitapları sıkılmadan, 3-4 sayfalık alt başlıklarla ve sokak ağzıyla terminalinden adım adım oku.

Ağır teknik kitapları ve dünya klasiklerini okurken uyuyakalmaya son. **HoodReads**, Martin Kleppmann'ın 600 sayfalık *Designing Data-Intensive Applications* kitabı gibi devasa eserleri ve klasikleri her biri **3-4 sayfalık alt başlıklara (`sf. 3-6`, `sf. 11-14`)** bölüp, komik ve vurucu bir sokak diliyle terminalinde okumanı sağlar.

Dışarıdan API, Twitter veya hesap bağlama derdi yok. Yalnızca sen, terminalin ve saf sokak bilgisi.

---

## ⚡ Özellikler

- **3-4 Sayfalık Hap Başlıklar**: 50 sayfalık bloklar yerine konuyu alt başlık alt başlık anlatır.
- **İnteraktif Terminal Okuyucu**: `Enter` / `n` basarak sonraki alt başlığa geç, `p` ile geri dön, dilediğinde çık. İlerlemen otomatik kaydedilir.
- **Günün Sokak Dersi**: Her parçanın sonunda konunun ana fikrini tek cümleyle kafana kazır.
- **Sıfır Bağımlılık / Çevrimdışı**: İnternet bağlantısı, API anahtarı veya hesap gerektirmez.

---

## 📚 Kütüphane

| ID | Kitap | Yazar | Alt Başlıklar |
| :--- | :--- | :--- | :---: |
| `ddia` | **Designing Data-Intensive Applications** | Martin Kleppmann | 46 alt başlık |
| `suc_ve_ceza` | **Suç ve Ceza** | Fyodor Dostoyevski | 6 bölüm |
| `donusum` | **Dönüşüm** | Franz Kafka | 4 bölüm |
| `1984` | **1984** | George Orwell | 5 bölüm |
| `yabanci` | **Yabancı** | Albert Camus | 4 bölüm |
| `kucuk_prens` | **Küçük Prens** | Antoine de Saint-Exupéry | 4 bölüm |

---

## 🚀 Hızlı Başlangıç

```bash
# 1. Ortamı kur
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🕹️ Komutlar

### 1. İnteraktif Okuyucu Modu (Tavsiye Edilen 🔥)
Kitabı açar; `Enter` tuşuna basarak alt başlıkları adım adım okursun:
```bash
python main.py interactive
```

### 2. Tek Bir Alt Başlık Oku ve İlerle
Her çalıştırdığında sıradaki 3-4 sayfalık konuyu ekrana basar ve bir sonrakine geçer:
```bash
python main.py read
```

### 3. Kütüphaneni ve İlerlemeni Gör
```bash
python main.py list
```

### 4. İstediğin Kitaba veya Bölüme Geç
```bash
python main.py set-book ddia --chapter 1
```

### 5. Önizleme
```bash
# DDIA 1. Ana Bölümün tüm alt başlıklarını gör
python main.py preview ddia --chapter 1

# İlk 3 alt başlığı gör
python main.py preview ddia --limit 3
```

---

## 🧪 Testler

```bash
.venv/bin/pytest -v
```

---

## 📄 Lisans

MIT © [alisenn](https://github.com/alisenn)
