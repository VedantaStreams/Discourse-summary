# 🕉️ Wisdom Distiller · vedantadhara.com

*Śravaṇa · Manana · Nididhyāsana*

An AI-powered platform for transcribing and summarizing spiritual discourses,
lectures, and educational content. Built with **Streamlit**, **OpenAI Whisper API**,
and **Anthropic Claude**.

---

## ✨ Features

- 🎙️ **Audio Summarizer** — Upload 1–5 MP3/WAV/M4A segments, transcribed in order and summarized together
- 🎬 **Video Summarizer** — Upload MP4 or extract YouTube audio via 4K Video Downloader
- 📄 **Document Combiner** — Merge multiple transcripts into one unified document
- 🌐 **Language Translation** — Translate output into Hindi, Kannada, Telugu, or Tamil
- 📊 **Excel-style structured table** — 4-column table with gold headers and alternating rows
- 🔤 **Sanskrit transliteration** — Sanskrit terms retained with English meaning in parentheses
- ⬇️ **Export as TXT, PDF, or DOCX**
- 🌑 **Elegant dark UI** — Om symbol, Swami Chinmayānanda quote in gold italic
- 🙏 **Reverence & Gratitude** — Dedicated page honouring Pūjya Swami Aparājitānandajī and Pūjya Swāmī Śaraṇānanda jī
- 📱 **Get the App** — Instructions for iPhone, Android, API setup, and sharing

---

## 📁 Project Structure

```
vedantadhara/
├── app.py                               ← Home page
├── pages/
│   ├── 1_Reverence_and_Gratitude.py    ← Pranāms & Gratitude
│   ├── 2_Audio_Summarizer.py           ← Audio upload & summarization
│   ├── 3_Document_Combiner.py          ← Merge & summarize transcripts
│   ├── 4_Video_Summarizer.py           ← Video & YouTube audio tool
│   ├── 5_About.py                      ← About page
│   └── 6_Get_the_App.py                ← Mobile & sharing guide
├── utils/
│   ├── helpers.py                      ← Transcription, summarization, translation, export
│   └── styles.py                       ← Shared CSS styles
├── .streamlit/
│   └── config.toml                     ← Dark theme config
├── Om.jpeg                             ← Om symbol (required)
├── headshot.jpeg                       ← Profile photo (required)
├── requirements.txt
└── README.md
```

---

## 🖥️ Sidebar Navigation

```
🏠  Home
🙏  Reverence And Gratitude
🎙️  Audio Summarizer
📄  Document Combiner
🎬  Video Summarizer
👤  About
📱  Get The App
```

---

## 🎯 Output Styles

| Style | Description |
|---|---|
| **Bullet highlights** | Key points grouped under bold thematic headers |
| **Main takeaways** | Top 8–10 numbered takeaways |
| **Detailed paragraphs** | Full prose summary |
| **Executive brief** | Crisp 300-word brief |
| **Academic digest** | Overview, Arguments, Evidence, Conclusions |
| **Structured table** | Excel-style 4-column table (user selects columns) |

### 📊 Structured Table Columns

| Column | Content |
|---|---|
| **Main Point (verbatim)** | Key point as spoken |
| **Explanation** | Plain language meaning |
| **Example from discourse** | Any example given; otherwise N/A |
| **Personal Reflection** | Left blank for the reader |

---

## 🌐 Language Translation

All three summarizer pages support translation of both transcript and summary into:

- 🇮🇳 Hindi (हिन्दी)
- 🇮🇳 Kannada (ಕನ್ನಡ)
- 🇮🇳 Telugu (తెలుగు)
- 🇮🇳 Tamil (தமிழ்)

Sanskrit terms are preserved in their original form across all languages.

---

## 📥 Export Formats

| Format | Notes |
|---|---|
| `.txt` | Always available |
| `.pdf` | Select PDF before processing |
| `.docx` | Select DOCX before processing |

Both **summary** and **full transcript** are always downloadable separately.

---

## 🔑 API Keys Required

| Key | Where to get it | Used for |
|---|---|---|
| **Anthropic API Key** | [console.anthropic.com](https://console.anthropic.com) | Claude summarization & translation |
| **OpenAI API Key** | [platform.openai.com](https://platform.openai.com) | Whisper transcription |

### Usage Policy
This app is offered as a free resource. Each user may use the app up to **5 times**
using the shared access provided. After 5 uses, users are requested to set up their
own API keys. Both are free to start and cost only a few cents per session.

---

## 💰 Estimated Cost Per Session

| Task | Whisper API | Claude API | Total |
|---|---|---|---|
| 20 min audio | ~$0.12 | ~$0.02 | ~$0.14 |
| 1 hour audio | ~$0.36 | ~$0.03 | ~$0.39 |
| 1.5 hour audio | ~$0.54 | ~$0.05 | ~$0.59 |

---

## 🖥️ Run Locally

### 1. Install ffmpeg
```bash
brew install ffmpeg        # macOS
sudo apt install ffmpeg    # Ubuntu/Debian
winget install ffmpeg      # Windows
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run
```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## ☁️ Deploy on Streamlit Cloud

### 1. Push all files to GitHub

### 2. Deploy
- Visit [share.streamlit.io](https://share.streamlit.io)
- Select repo, set main file to `app.py`
- Add Secrets:

```toml
ANTHROPIC_API_KEY = "sk-ant-xxxxxxxx"
OPENAI_API_KEY = "sk-xxxxxxxx"
```

### 3. Custom Domain
Point `app.vedantadhara.com` to your Streamlit app:
- Streamlit → app Settings → Custom domain → enter `app.vedantadhara.com`
- Copy the CNAME Streamlit provides
- In Namecheap → Advanced DNS → add CNAME record
- Wait 10–30 minutes for DNS propagation

---

## 📦 Dependencies

```
streamlit       — web framework
anthropic       — Claude API
openai          — Whisper API
reportlab       — PDF export
python-docx     — Word export
```

Audio splitting uses `ffmpeg` — pre-installed on Streamlit Cloud.
No PyTorch, no pydub, no local AI models required.

---

## 👤 About

Suma Rajashankar holds a PhD in Physics from the Indian Institute of Science
and completed postdoctoral research at Stony Brook University. She served as
an Assistant Professor at Northern Illinois University for over 18 years.
Wishing to broaden her horizons beyond academia, she transitioned into the
corporate world — bringing her academic foundation into AI and Data Science,
contributing to impactful work at Discover Financial Services and currently
at Capital One.

She considers herself a humble and earnest seeker on the spiritual path, and
a devoted student of Vedanta, blessed to be closely associated with the
Chinmaya Mission. This platform was built in a spirit of service — to make
the wisdom of sacred discourses a little more accessible through the tools
of modern AI.

*With pranāms* 🙏

---

## 🔧 Troubleshooting

| Error | Fix |
|---|---|
| `ModuleNotFoundError: utils` | Ensure `utils/` folder exists with `helpers.py` and `styles.py` |
| HTML showing as raw text | Check `unsafe_allow_html=True` in every `st.markdown()` call |
| `ffmpeg not found` | Add `packages.txt` with `ffmpeg` to repo root |
| App slow to load first time | First deploy installs packages — wait 2–3 minutes |
| Table shows as plain text | Select "Structured table" style before processing |
| API key error (400) | Go to console.anthropic.com → Billing → add credits |
| Pages in wrong order | Rename files with number prefix: `1_`, `2_`, `3_` etc. |
