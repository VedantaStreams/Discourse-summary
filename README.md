# 🎙️ Discourse Summarizer

A Streamlit webapp that transcribes long MP3 discourses (up to 1.5h+) and summarizes them using **OpenAI Whisper** + **Claude API**.

---

## 🚀 Setup & Run

### 1. Prerequisites

Make sure you have **Python 3.9+** and **ffmpeg** installed.

**Install ffmpeg:**
- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt install ffmpeg`
- Windows: Download from https://ffmpeg.org/download.html and add to PATH

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ `openai-whisper` will also download PyTorch (~2GB) if not already installed.

### 3. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🔑 API Key

Get your **Anthropic API key** at [console.anthropic.com](https://console.anthropic.com) and paste it in the sidebar when the app opens.

---

## 🧠 How It Works

```
MP3 Upload
   ↓
Split into 10-min chunks (pydub)
   ↓
Transcribe each chunk (Whisper — runs locally)
   ↓
Combine transcript
   ↓
Summarize with Claude API (claude-sonnet-4)
   ↓
Display summary + download buttons
```

---

## ⚙️ Options (Sidebar)

| Setting | Options | Notes |
|---|---|---|
| Whisper Model | tiny, base, small, medium, large | `small` = fast+decent, `medium` = best balance |
| Summary Style | Bullet points, Paragraphs, Executive brief, Academic digest | Choose based on your needs |
| Show Transcript | On/Off | View the full raw transcription |

---

## 📁 Output

- **Summary** — displayed in the app, downloadable as `.txt`
- **Transcript** — downloadable as `.txt`

---

## 💡 Tips

- For a 1.5h MP3, transcription takes ~5–15 min depending on Whisper model and your CPU/GPU
- If you have an NVIDIA GPU, Whisper will use it automatically (much faster)
- Use `medium` model for best accuracy on accented or technical speech
