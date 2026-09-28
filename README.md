# 💀 HoodReads — Books from the Hood

> **Goodreads, but from the hood.**  
> Unfiltered, funny, bite-sized street summaries of classic literature and heavy engineering books, formatted for Twitter / X threads.

Stop falling asleep reading 600-page monographs. **HoodReads** deconstructs world classics and complex tech bibles (like Martin Kleppmann's *Designing Data-Intensive Applications*) into hilarious 3-4 page sub-topics narrated in raw, punchy street slang.

Zero paid LLM API required. Fully autonomous, thread-aware, state-tracked Twitter/X publishing engine with rich terminal previews.

---

## ⚡ Features

- **Street-Level Wisdom**: Complex ideas explained in 3-5 punchy street sentences + a takeaway punchline.
- **Bite-Sized Sub-Topics**: Heavy books are broken down by 3-4 page sections (`sf. 3-6`, `sf. 11-14`), not 50-page blobs.
- **Twitter V2 & Thread Engine**: Automatically packs content into strict <= 280-character thread chunks (`1/2 🧵`, `2/2`).
- **DRY-RUN Terminal Mode**: Beautiful CLI UI powered by `rich` to preview cards without needing Twitter API keys.
- **Zero API Bills**: Runs standalone with curated book datasets, or easily extensible with your own books.

---

## 📚 The Hood Catalog

| ID | Book | Author | Sub-Topics / Episodes | Vibe |
| :--- | :--- | :--- | :---: | :--- |
| `ddia` | **Designing Data-Intensive Applications** | Martin Kleppmann | 46 episodes | The 600-page distributed systems bible turned into street survival tactics. |
| `suc_ve_ceza` | **Crime and Punishment** | Fyodor Dostoyevski | 6 episodes | Raskolnikov thinks he's Napoleon, axes a pawnbroker, suffers severe paranoia. |
| `donusum` | **The Metamorphosis** | Franz Kafka | 4 episodes | Man wakes up as a giant cockroach and still stresses about missing the 7 AM train. |
| `1984` | **1984** | George Orwell | 5 episodes | Big Brother surveillance state where even holding hands feels like carrying C4. |
| `yabanci` | **The Stranger** | Albert Camus | 4 episodes | Slurps ice cream at mom's funeral, gets annoyed by the beach sun and shoots a guy. |
| `kucuk_prens` | **The Little Prince** | Antoine de Saint-Exupéry | 4 episodes | Little prince planet-hops while laughing at how utterly stupid adults are. |

---

## 🚀 Quickstart

```bash
# 1. Clone & Setup Virtualenv
git clone https://github.com/alisenn/hoodreads.git
cd hoodreads
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🕹️ CLI Usage

### 1. View Library
```bash
python main.py list
```

### 2. Terminal Preview (No API Key Required)
```bash
# Preview first 4 sub-topics of DDIA
python main.py preview ddia --limit 4

# Preview specific chapter (e.g. Chapter 1: Reliability & Scalability)
python main.py preview ddia --chapter 1

# Preview classic fiction
python main.py preview donusum
```

### 3. Post Next Episode (Dry-Run / Live)
```bash
# Dry-run terminal simulation (default)
python main.py tweet

# Live tweet to real Twitter account (reads keys from .env)
python main.py tweet --live
```

### 4. Switch Active Reading Target
```bash
python main.py set-book ddia --chapter 1
```

---

## ⚙️ Twitter API Configuration (Optional)

Copy `.env.example` to `.env` and fill in your Twitter Developer Portal keys:

```ini
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

If keys are absent, HoodReads gracefully falls back to **DRY-RUN** simulation mode.

---

## 🧪 Testing

```bash
.venv/bin/pytest -v
```

---

## 📄 License

MIT © [alisenn](https://github.com/alisenn)
