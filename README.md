# 🕉️ Discourse Summarizer

A beautiful Streamlit webapp for transcribing and summarizing spiritual discourses, lectures, and talks. Upload one long MP3 or multiple shorter segments — the app transcribes them in order using **OpenAI Whisper API** and summarizes using **Anthropic Claude API**.

---

## ✨ Features

- 🎧 Upload **1 long audio file** or **up to 4 shorter segments**
- 🗣️ Transcription via **OpenAI Whisper API** (fast, cloud-based, no local GPU needed)
- 🤖 Summarization via **Anthropic Claude** (multiple summary styles)
- ⬇️ Download both the **summary** and the **full transcript** as `.txt` files
- 🕉️ Beautiful dark UI with Om symbol, spiritual quote, and about section

---

## 🚀 How It Works

```
Upload 1 long MP3  —OR—  Upload 2–4 shorter segments
            ↓
Split any files over 25MB into chunks (ffmpeg)
            ↓
Transcribe all parts in order via OpenAI Whisper API
            ↓
Combine into one full transcript
            ↓
Summarize with Claude API (Anthropic)
            ↓
Display summary + download both summary & transcript
```

---

## 📁 Project Files

```
discourse-summarizer/
├── app.py              ← Main Streamlit app
├── Om.jpeg             ← Om symbol image (shown in header)
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

> ⚠️ Make sure `Om.jpeg` is in the **same folder** as `app.py` on GitHub. The app loads it automatically.

---

## 🔑 API Keys Required

| Key | Where to get it | Used for |
|---|---|---|
| **Anthropic API Key** | [console.anthropic.com](https://console.anthropic.com) | Summarization via Claude |
| **OpenAI API Key** | [platform.openai.com](https://platform.openai.com) | Transcription via Whisper API |

---

## 💰 Cost Per Session

| Audio Length | Whisper API | Claude API | Total |
|---|---|---|---|
| 20 minutes | ~$0.12 | ~$0.02 | ~$0.14 |
| 1 hour | ~$0.36 | ~$0.03 | ~$0.39 |
| 1.5 hours | ~$0.54 | ~$0.05 | ~$0.59 |

---

## 🖥️ Run Locally

### 1. Install ffmpeg
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

Opens at `http://localhost:8501`. Paste both API keys in the sidebar.

---

## ☁️ Deploy on Streamlit Cloud

### 1. Push all files to GitHub
Make sure these files are in your repo:
- `app.py`
- `Om.jpeg`
- `requirements.txt`

### 2. Go to Streamlit Cloud
- Visit [share.streamlit.io](https://share.streamlit.io)
- Click **"Create app"**
- Select your GitHub repo, set main file to `app.py`
- Click **"Advanced settings"** → **"Secrets"**

### 3. Add API keys in Secrets
```toml
ANTHROPIC_API_KEY = "sk-ant-xxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
```

### 4. Deploy
Click **Deploy** — live in under a minute.

---

## ⚙️ App Options (Sidebar)

| Setting | Options |
|---|---|
| **Summary Style** | Concise (bullets), Detailed (paragraphs), Executive brief, Academic digest |
| **Show Transcript on Page** | Toggle to display the full transcript on screen (always downloadable) |

---

## 📥 Downloads

After processing you will see two download buttons:

- **⬇️ Download Summary (.txt)** — the AI-generated summary
- **⬇️ Download Transcript (.txt)** — the full word-for-word transcription

---

## 📦 Dependencies

```
streamlit      — web app framework
anthropic      — Claude API for summarization
openai         — Whisper API for transcription
```

No PyTorch, no pydub, no local AI models required. Audio splitting uses `ffmpeg` which is pre-installed on Streamlit Cloud.
