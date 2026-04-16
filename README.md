# 🎙️ Discourse Summarizer

A Streamlit webapp that transcribes long MP3 discourses (up to 1.5h+) and summarizes them using **OpenAI Whisper API** (for transcription) + **Claude API** (for summarization).

---

## 🚀 How It Works

```
Upload MP3
    ↓
Split into chunks under 25MB (pydub)
    ↓
Send each chunk to OpenAI Whisper API (fast, cloud-based transcription)
    ↓
Combine full transcript
    ↓
Send transcript to Claude API (Anthropic)
    ↓
Display summary + download buttons
```

---

## 🔑 API Keys Required

You need **two** API keys:

| Key | Where to get it | Used for |
|---|---|---|
| **Anthropic API Key** | [console.anthropic.com](https://console.anthropic.com) | Summarization via Claude |
| **OpenAI API Key** | [platform.openai.com](https://platform.openai.com) | Transcription via Whisper API |

Both services offer pay-as-you-go pricing. A $5 credit on each is more than enough to get started.

---

## 💰 Cost Per Session

| Step | Cost |
|---|---|
| Whisper API transcription (20 min audio) | ~$0.12 |
| Whisper API transcription (1.5 hr audio) | ~$0.54 |
| Claude summarization (any length) | ~$0.01 – $0.05 |

**Total for a 1.5h discourse: under $0.60**

---

## 🖥️ Run Locally

### 1. Prerequisites
Make sure you have **Python 3.9+** and **ffmpeg** installed.

**Install ffmpeg:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
winget install ffmpeg
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

When running locally, paste your API keys directly in the **sidebar** of the app.

---

## ☁️ Deploy on Streamlit Cloud

### 1. Push to GitHub
Upload `app.py` and `requirements.txt` to a GitHub repository.

### 2. Deploy on Streamlit Cloud
- Go to [share.streamlit.io](https://share.streamlit.io)
- Click **"Create app"**
- Select your GitHub repo and set main file to `app.py`
- Click **"Advanced settings"** → **"Secrets"**

### 3. Add your API keys in Secrets
```toml
ANTHROPIC_API_KEY = "sk-ant-xxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
```

### 4. Deploy
Click **Deploy** — the app will be live in under a minute at a public URL like:
```
https://yourname-discourse-summarizer.streamlit.app
```

---

## ⚙️ App Options (Sidebar)

| Setting | Options | Notes |
|---|---|---|
| Summary Style | Concise (bullets), Detailed (paragraphs), Executive brief, Academic digest | Choose based on your needs |
| Show Transcript | On/Off | View the full raw transcription below the summary |

---

## 📁 Output

- **Summary** — displayed in the app, downloadable as `.txt`
- **Transcript** — downloadable as `.txt`

---

## 📦 Dependencies

```
streamlit      — web app framework
anthropic      — Claude API for summarization
openai         — Whisper API for transcription
pydub          — audio splitting for large files
```

No PyTorch or local AI models required — everything runs in the cloud.

---

## 💡 Tips

- Whisper API supports MP3, M4A, WAV, and OGG formats
- Files larger than 25MB are automatically split into chunks before transcription
- For very long discourses (1.5h+), transcription takes about 1–3 minutes
- Set a **spending limit** on both API accounts to avoid unexpected charges
