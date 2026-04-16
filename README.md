# 🕉️ Discourse Summarizer · Suma AI Hub

A beautiful, multi-page AI-powered platform for transcribing and summarizing spiritual discourses,
lectures, and educational content. Built with **Streamlit**, **OpenAI Whisper API**, and **Anthropic Claude**.

---

## ✨ Features

- 🎙️ **Audio Summarizer** — Upload 1–5 MP3/WAV/M4A segments, transcribed in order and summarized together
- 🎬 **Video Summarizer** — Paste a YouTube URL or upload an MP4; audio extracted automatically via ffmpeg and yt-dlp
- 📄 **Document Combiner** — Merge multiple transcripts into one unified document with optional re-summarization
- 👤 **About Page** — Full bio of Dr. Suma Rajashankar with impact stats and Swamiji's quote
- 📊 **Excel-style structured table** — 4-column table with gold headers, alternating rows, horizontal scroll
- 🔤 **English transliteration** — Sanskrit and regional language terms retained with English meaning in parentheses
- ⬇️ **Export as TXT, PDF, or DOCX**
- 🌑 **Elegant dark UI** — Om symbol, Swami Chinmayananda quote in gold italic, personal headshot in sidebar
- 🔹 **Reverence & Gratitude** — Acknowledgement to Pūjya Swami Aparājitānandajī and Pūjya Swāmī Śaraṇānanda jī

---

## 📁 Project Structure

```
sumaaihub/
├── app.py                        ← Home page (Discourse Summarizer title + navigation cards)
├── pages/
│   ├── Audio_Summarizer.py      ← Audio upload & summarization tool
│   ├── Video_Summarizer.py      ← YouTube URL & MP4 video tool
│   ├── Document_Combiner.py     ← Merge & summarize multiple transcripts
│   └── About.py                 ← Full bio page for Dr. Suma Rajashankar
├── utils/
│   ├── helpers.py               ← Transcription, summarization, table rendering, PDF/DOCX export
│   └── styles.py                ← Shared CSS styles across all pages
├── .streamlit/
│   └── config.toml              ← Dark theme config for Streamlit Cloud
├── Om.jpeg                      ← Om symbol displayed in page header (required)
├── headshot.jpeg                ← Dr. Suma Rajashankar's photo in sidebar (required)
├── requirements.txt             ← Python dependencies
└── README.md                    ← This file
```

> ⚠️ **Both `Om.jpeg` and `headshot.jpeg` must be present** in the root of your GitHub repo.
> The app loads them automatically — no code changes needed.

---

## 🖥️ App Layout

### Main Page (`app.py`)
- 🕉️ Om symbol + **Discourse Summarizer** title
- Swami Chinmayananda quote in gold italic serif font
- Welcome description of the platform
- 3 clickable navigation cards with buttons → Audio Summarizer, Video Summarizer, Document Combiner

### Left Sidebar (shown on all pages)
- Dr. Suma Rajashankar's **circular headshot** centered at top
- Name + **Senior Data Scientist / AI Engineer** in gold uppercase
- Clickable **"✦ About Me & Full Bio"** link → opens full About page
- API key inputs (auto-loaded from Streamlit Secrets on cloud deployment)
- 🔹 **Reverence & Gratitude** section acknowledging Pūjya Swami Aparājitānandajī and Pūjya Swāmī Śaraṇānanda jī

---

## 🎯 Output Styles

| Style | Description |
|---|---|
| **Bullet highlights** | Key points grouped under bold thematic headers |
| **Main takeaways** | Top 8–10 numbered takeaways, one per line |
| **Detailed paragraphs** | Full prose summary covering all major themes |
| **Executive brief** | Crisp 300-word brief with key message and action items |
| **Academic digest** | Structured: Overview, Arguments, Evidence, Conclusions, Notable Quotes |
| **Structured table** | Excel-style 4-column table — user selects which columns to include |

### 🔤 English Transliteration (all styles)
All summary styles instruct Claude to retain Sanskrit and regional language terms
and add their English meaning in parentheses immediately after. For example:

> *"The Ātman (the Self) is described as beyond the reach of Māyā (illusion).
> The Jīva (individual soul) must turn inward through Viveka (discernment)..."*

---

### 📊 Structured Table Columns (user selectable)

| Column | Content |
|---|---|
| **Main Point (verbatim)** | Key point as spoken, word for word |
| **Explanation** | What the point means in plain language |
| **Example from discourse** | Any example given; otherwise N/A |
| **Personal Reflection** | Left blank for the reader to fill in |

The table renders as a proper Excel-style HTML table with:
- Gold column headers in uppercase
- Alternating dark row colors
- Hover highlight on rows
- Horizontal scroll for wide tables

---

## 📥 Export Formats

| Format | Notes |
|---|---|
| `.txt` | Always available — plain text download |
| `.pdf` | Select PDF in "Download format" before processing |
| `.docx` | Select DOCX in "Download format" before processing |

Both **Summary** and **Full Transcript** are always downloadable separately after processing.

---

## 🔑 API Keys Required

| Key | Where to get it | Used for |
|---|---|---|
| **Anthropic API Key** | [console.anthropic.com](https://console.anthropic.com) | Claude summarization |
| **OpenAI API Key** | [platform.openai.com](https://platform.openai.com) | Whisper API transcription |

Both use pay-as-you-go pricing. A $5 credit on each is more than enough to get started.

---

## 💰 Estimated Cost Per Session

| Task | Whisper API | Claude API | Total |
|---|---|---|---|
| 20 min audio | ~$0.12 | ~$0.02 | ~$0.14 |
| 1 hour audio | ~$0.36 | ~$0.03 | ~$0.39 |
| 1.5 hour audio | ~$0.54 | ~$0.05 | ~$0.59 |
| YouTube video 30 min | ~$0.18 | ~$0.02 | ~$0.20 |

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

Opens at `http://localhost:8501`. Enter both API keys in the sidebar when the app opens.

---

## ☁️ Deploy on Streamlit Cloud

### 1. Push all files to GitHub
Make sure your repo contains exactly this structure:
```
app.py
pages/Audio_Summarizer.py
pages/Video_Summarizer.py
pages/Document_Combiner.py
pages/About.py
utils/helpers.py
utils/styles.py
.streamlit/config.toml
Om.jpeg
headshot.jpeg
requirements.txt
```

### 2. Go to Streamlit Cloud
- Visit [share.streamlit.io](https://share.streamlit.io)
- Click **"Create app"**
- Select your GitHub repo
- Set main file path to: `app.py`
- Click **"Advanced settings"** → **"Secrets"**

### 3. Add both API keys in Secrets
```toml
ANTHROPIC_API_KEY = "sk-ant-xxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxx"
```

### 4. Click Deploy
App goes live in under a minute at your Streamlit URL.

### 5. Custom Domain (optional)
To use a custom URL like `summarizer.sumaaihub.com`:
1. Buy domain at [namecheap.com](https://namecheap.com) (~$10–15/year)
2. Streamlit app → **⋮** → **Settings** → **Custom domain** → enter subdomain
3. Copy the CNAME value Streamlit provides
4. In Namecheap → **Advanced DNS** → add a CNAME record:
   - Host: `summarizer`
   - Value: paste CNAME from Streamlit
5. Wait 10–30 minutes for DNS to propagate

You can add unlimited subdomains for future apps at no extra cost:
```
summarizer.sumaaihub.com   ← this app
chatbot.sumaaihub.com      ← future app
tools.sumaaihub.com        ← future app
```

---

## 📦 Dependencies

```
streamlit       — web app framework
anthropic       — Claude API for summarization
openai          — Whisper API for transcription
yt-dlp          — YouTube audio download
reportlab       — PDF generation
python-docx     — Word document generation
```

Audio splitting and video extraction use `ffmpeg` — pre-installed on Streamlit Cloud.
No PyTorch, no pydub, no local AI models required.

---

## 🔧 Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError: utils` | Ensure `utils/` folder exists in repo with both `helpers.py` and `styles.py` |
| `pyaudioop` error | Remove `pydub` from requirements — app uses ffmpeg directly |
| App takes forever to load | First deploy installs packages — wait 2–3 minutes |
| YouTube download fails | Video may be private or geo-restricted — try another URL |
| Table shows as plain text | Select "Structured table" style before clicking Transcribe & Summarize |
| API key error (400) | Go to console.anthropic.com → Billing → add credits |
| Secrets not loading | Check Streamlit Secrets format — key names must match exactly |

---

## 👤 About the Creator

**Dr. Suma Rajashankar** is a Senior Data Scientist and AI Engineer at Capital One. She holds a PhD in Physics from the Indian Institute of Science and has over 15 years of academic teaching experience at Northern Illinois University. She has mentored 350+ professionals in AI/ML with a consistent rating of 4.75–5.0 over four years.

She is also a student of Vedanta through the Chinmaya Mission, and this platform was built in the spirit of making the wisdom of spiritual discourses more accessible through the tools of modern AI.

---

*Built with ❤️ and humble pranāms · Dr. Suma Rajashankar*
*Powered by OpenAI Whisper · Anthropic Claude · Streamlit*
