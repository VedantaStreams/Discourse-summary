# 🕉️ Suma AI Hub

A multi-page AI-powered platform for transcribing and summarizing spiritual discourses, lectures, and educational content. Built with Streamlit, OpenAI Whisper API, and Anthropic Claude.

---

## 📁 Project Structure

```
sumaaihub/
├── app.py                        ← Main home page & navigation
├── pages/
│   ├── 1_Audio_Summarizer.py    ← Upload MP3/WAV/M4A (up to 5 files)
│   ├── 2_Video_Summarizer.py    ← YouTube URL or MP4 upload
│   ├── 3_Document_Combiner.py   ← Merge multiple transcripts
│   └── 4_About.py               ← Full bio page
├── utils/
│   ├── styles.py                ← Shared CSS styles
│   └── helpers.py               ← Transcription, summarization, export logic
├── Om.jpeg                       ← Om symbol (required)
├── headshot.jpeg                 ← Your photo (required for sidebar)
├── requirements.txt
└── README.md
```

> ⚠️ Both `Om.jpeg` and `headshot.jpeg` must be uploaded to your GitHub repo alongside `app.py`.

---

## ✨ Features

| Page | What it does |
|---|---|
| 🏠 **Home** | Welcome page with navigation cards |
| 🎙️ **Audio Summarizer** | Upload 1–5 MP3/WAV/M4A segments, transcribe in order, summarize |
| 🎬 **Video Summarizer** | Paste YouTube URL or upload MP4, auto-extract audio, transcribe & summarize |
| 📄 **Document Combiner** | Upload multiple .txt transcripts, merge & optionally re-summarize |
| 👤 **About** | Full bio of Dr. Suma Rajashankar |

---

## 🎯 Output Styles

- **Bullet highlights** — grouped bullet points under thematic headers
- **Main takeaways** — top 8–10 numbered takeaways
- **Detailed paragraphs** — full prose summary
- **Executive brief** — concise 300-word brief
- **Academic digest** — structured with Overview, Arguments, Conclusions
- **Structured table** — user-selectable columns:
  - Main Point (verbatim)
  - Explanation
  - Example from discourse
  - Personal Reflection (blank for reader)

---

## 📥 Export Formats

- `.txt` — plain text (always available)
- `.pdf` — formatted PDF via ReportLab
- `.docx` — Word document via python-docx

---

## 🔑 API Keys Required

| Key | Where | Used for |
|---|---|---|
| **Anthropic API Key** | [console.anthropic.com](https://console.anthropic.com) | Claude summarization |
| **OpenAI API Key** | [platform.openai.com](https://platform.openai.com) | Whisper transcription |

---

## ☁️ Deploy on Streamlit Cloud

### 1. Push all files to GitHub
Make sure ALL files are in your repo including `Om.jpeg` and `headshot.jpeg`.

### 2. Deploy
- Go to [share.streamlit.io](https://share.streamlit.io)
- Select repo, set main file to `app.py`
- Add Secrets:

```toml
ANTHROPIC_API_KEY = "sk-ant-xxxxxxxx"
OPENAI_API_KEY = "sk-xxxxxxxx"
```

### 3. Custom domain (optional)
Point `summarizer.sumaaihub.com` to your Streamlit app via Namecheap DNS CNAME record.

---

## 💰 Estimated Cost Per Session

| Task | Cost |
|---|---|
| 20 min audio transcription | ~$0.12 |
| 1.5 hr audio transcription | ~$0.54 |
| Claude summarization (any length) | ~$0.01–$0.05 |
| YouTube video (30 min) | ~$0.18 |

---

## 📦 Dependencies

```
streamlit       — web framework
anthropic       — Claude API
openai          — Whisper API
yt-dlp          — YouTube audio download
reportlab       — PDF export
python-docx     — Word export
```

Audio splitting and video extraction use `ffmpeg` — pre-installed on Streamlit Cloud.
