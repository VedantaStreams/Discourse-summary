import streamlit as st
import tempfile
import os
import math
import time
import subprocess
import base64
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Discourse Summarizer",
    page_icon="🕉️",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #0a0a0a; color: #e8e0d4; }

/* Hero */
.hero {
    text-align: center;
    padding: 2rem 0 0.5rem;
    border-bottom: 1px solid #2a2a2a;
    margin-bottom: 0.5rem;
}
.hero img.om {
    width: 80px;
    height: 80px;
    object-fit: contain;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 18px rgba(201,169,110,0.5));
}
.hero h1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 600;
    letter-spacing: 1px;
    color: #e8e0d4;
    margin: 0 0 0.2rem;
}
.hero .subtitle {
    font-size: 0.9rem;
    color: #666;
    font-weight: 300;
    letter-spacing: 0.5px;
    margin-bottom: 0.8rem;
}
.accent { color: #c9a96e; }

/* Quote */
.quote-block {
    text-align: center;
    padding: 1rem 2rem 1.5rem;
    border-bottom: 1px solid #1e1e1e;
    margin-bottom: 1.8rem;
}
.quote-text {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.1rem;
    color: #c9a96e;
    line-height: 1.7;
}
.quote-author {
    font-size: 0.78rem;
    color: #555;
    letter-spacing: 0.8px;
    margin-top: 0.4rem;
    text-transform: uppercase;
}

/* About section */
.about-box {
    background: #111;
    border: 1px solid #1e1e1e;
    border-left: 3px solid #c9a96e;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.8rem;
    font-size: 0.88rem;
    color: #999;
    line-height: 1.7;
}
.about-box b { color: #c9a96e; }

/* File uploader */
[data-testid="stFileUploader"] {
    border: 1.5px dashed #2a2a2a;
    border-radius: 12px;
    padding: 1rem;
    background: #111;
}
[data-testid="stFileUploader"]:hover { border-color: #c9a96e; }

/* Buttons */
.stButton > button {
    background: #c9a96e !important;
    color: #0a0a0a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.95rem !important;
    transition: opacity 0.2s !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e0d4 !important;
    border-radius: 8px !important;
}

/* Text input */
.stTextInput > div > div > input {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e0d4 !important;
    border-radius: 8px !important;
}

/* Progress */
.stProgress > div > div { background: #c9a96e !important; }

/* Alerts */
.stAlert {
    border-radius: 10px !important;
    border-left: 3px solid #c9a96e !important;
    background: #111 !important;
    color: #e8e0d4 !important;
}

/* Output box */
.output-box {
    background: #111;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    margin-top: 1rem;
    line-height: 1.7;
    color: #d4c9b8;
    font-size: 0.95rem;
    white-space: pre-wrap;
    max-height: 420px;
    overflow-y: auto;
}

/* Step labels */
.step-label {
    display: inline-block;
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 0.2rem 0.9rem;
    font-size: 0.78rem;
    color: #c9a96e;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* File pills */
.file-pill {
    display: inline-block;
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 0.3rem 0.8rem;
    font-size: 0.82rem;
    color: #c9a96e;
    margin: 0.2rem 0.2rem 0.2rem 0;
}

hr { border-color: #1e1e1e !important; margin: 1.8rem 0 !important; }

/* Download buttons */
[data-testid="stDownloadButton"] > button {
    background: #161616 !important;
    color: #c9a96e !important;
    border: 1px solid #c9a96e !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    width: 100%;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #c9a96e !important;
    color: #0a0a0a !important;
}

/* Checkbox */
.stCheckbox > label { color: #888 !important; font-size: 0.88rem !important; }

/* Sidebar */
[data-testid="stSidebar"] { background: #0d0d0d !important; }

/* Bio section */
.bio-header {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #c9a96e;
    letter-spacing: 0.5px;
    margin-bottom: 0.3rem;
}
.bio-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #e8e0d4;
    margin-bottom: 0.1rem;
}
.bio-role {
    font-size: 0.78rem;
    color: #c9a96e;
    letter-spacing: 0.5px;
    margin-bottom: 0.8rem;
    text-transform: uppercase;
}
.bio-text {
    font-size: 0.82rem;
    color: #888;
    line-height: 1.75;
}
.bio-text b { color: #b8a88a; }
.bio-divider {
    border: none;
    border-top: 1px solid #1e1e1e;
    margin: 0.8rem 0;
}
.bio-stat {
    display: flex;
    align-items: baseline;
    gap: 6px;
    margin: 0.3rem 0;
}
.bio-stat-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #c9a96e;
}
.bio-stat-label {
    font-size: 0.75rem;
    color: #666;
}
</style>
""", unsafe_allow_html=True)


# ── Load Om image as base64 ────────────────────────────────────────────────────
def load_image_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

om_b64 = ""
om_path = Path(__file__).parent / "Om.jpeg"
if om_path.exists():
    om_b64 = load_image_base64(str(om_path))
    om_img_tag = f'<img class="om" src="data:image/jpeg;base64,{om_b64}" alt="Om"/>'
else:
    om_img_tag = '<div style="font-size:3rem;margin-bottom:0.3rem;">🕉️</div>'


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    {om_img_tag}
    <h1>Discourse <span class="accent">Summarizer</span></h1>
    <p class="subtitle">Upload one long MP3 or multiple segments · Get a unified transcript & summary</p>
</div>
""", unsafe_allow_html=True)

# ── Quote ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="quote-block">
    <div class="quote-text">
        "Renounce your ego" is the Lord's only request;<br>
        "And I will make you God" is the promise.
    </div>
    <div class="quote-author">— Swami Chinmayananda</div>
</div>
""", unsafe_allow_html=True)

# ── About section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-box">
    <b>What this app does:</b><br>
    Upload an audio recording of a spiritual discourse, lecture, or talk — in MP3, M4A, WAV, or OGG format.
    The app will <b>transcribe</b> the full audio using OpenAI's Whisper API and then <b>summarize</b> it using
    Anthropic's Claude AI. You can upload a <b>single long file</b> or <b>up to 4 shorter segments</b> which
    will be stitched together in order. Both the <b>summary</b> and the <b>full transcript</b> can be
    downloaded as text files.
</div>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:

    # ── About Me ───────────────────────────────────────────────────────────────
    st.markdown("""
<div class="bio-header">🕉️ About Me</div>
<div class="bio-name">Dr. Suma Rajashankar</div>
<div class="bio-role">Senior Data Scientist · AI Engineer · Capital One</div>
<div class="bio-text">
    Dr. Suma Rajashankar holds a <b>PhD in Physics</b> from the Indian Institute of Science
    and completed her postdoctoral research at <b>Stony Brook University</b>. She went on to
    serve as an <b>Assistant Professor</b> at Northern Illinois University, where she taught
    across Electrical and Industrial Engineering disciplines for over <b>15 years</b>, shaping
    the academic journeys of countless students.
    <hr class="bio-divider"/>
    In a bold and purposeful career transition, she moved into <b>AI and Data Science</b>
    six years ago, contributing to impactful work at <b>Discover Financial Services</b> and
    currently at <b>Capital One</b>. Her expertise spans <b>Generative AI</b>, Speech Recognition
    technologies, and <b>Responsible AI</b>, where she has played a key role in developing
    guardrails for enterprise-scale AI engineering platforms.
    <hr class="bio-divider"/>
    Beyond her professional pursuits, Dr. Rajashankar has a deep and abiding interest in
    philosophy, particularly the study of <b>Vedanta</b>. She has been closely associated with
    the <b>Chinmaya Mission</b> for over two decades and finds great joy in the systematic study
    of the Upanishads, the Bhagavad Gita, and traditional Prakarana Granthas, reflecting a
    lifelong commitment to inner growth and inquiry.
    <hr class="bio-divider"/>
    Driven by a passion for both knowledge and mentorship, she actively guides working
    professionals through <b>AIML and AIDL programs</b> in collaboration with the
    <b>University of Texas at Austin</b> and <b>Great Learning</b>, helping them navigate
    and excel in the evolving AI landscape.
</div>
<br/>
<div class="bio-header" style="font-size:0.85rem; margin-bottom:0.6rem;">Impact at a Glance</div>
<div class="bio-stat"><span class="bio-stat-num">350+</span><span class="bio-stat-label">professionals mentored</span></div>
<div class="bio-stat"><span class="bio-stat-num">400+</span><span class="bio-stat-label">hours of AI/ML instruction</span></div>
<div class="bio-stat"><span class="bio-stat-num">4.75–5.0</span><span class="bio-stat-label">mentor rating over 4 years</span></div>
<hr class="bio-divider"/>
""", unsafe_allow_html=True)

    # ── Settings ───────────────────────────────────────────────────────────────
    st.markdown("### ⚙️ Settings")

    # Anthropic API key
    try:
        anthropic_key = st.secrets["ANTHROPIC_API_KEY"]
        st.success("✅ Anthropic key loaded")
    except Exception:
        anthropic_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            help="Get your key at console.anthropic.com",
        )

    # OpenAI API key
    try:
        openai_key = st.secrets["OPENAI_API_KEY"]
        st.success("✅ OpenAI key loaded")
    except Exception:
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Used for Whisper transcription. Get at platform.openai.com",
        )

    st.markdown("---")
    summary_style = st.selectbox(
        "Summary Style",
        ["Concise (bullet points)", "Detailed (paragraphs)", "Executive brief", "Academic digest"],
        index=0,
    )
    show_transcript = st.checkbox("Show full transcript on page", value=False)
    st.markdown("---")
    st.markdown("<small style='color:#444'>Built with Streamlit · OpenAI Whisper API · Claude</small>", unsafe_allow_html=True)


# ── Helper functions ───────────────────────────────────────────────────────────

CHUNK_MB = 24

def get_audio_duration_seconds(path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def split_audio_ffmpeg(path: str) -> list:
    file_size_mb = os.path.getsize(path) / (1024 * 1024)
    if file_size_mb <= CHUNK_MB:
        return [path]

    duration = get_audio_duration_seconds(path)
    n_chunks = math.ceil(file_size_mb / CHUNK_MB)
    chunk_duration = math.ceil(duration / n_chunks)
    tmp_dir = tempfile.mkdtemp()
    chunks = []

    for i in range(n_chunks):
        start = i * chunk_duration
        chunk_path = os.path.join(tmp_dir, f"chunk_{i+1}.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-i", path,
             "-ss", str(start), "-t", str(chunk_duration),
             "-acodec", "libmp3lame", "-q:a", "4", chunk_path],
            capture_output=True
        )
        if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 0:
            chunks.append(chunk_path)
    return chunks


def prepare_all_chunks(uploaded_files: list) -> list:
    all_chunks = []
    tmp_dir = tempfile.mkdtemp()
    for i, uploaded_file in enumerate(uploaded_files):
        suffix = Path(uploaded_file.name).suffix
        tmp_path = os.path.join(tmp_dir, f"file_{i+1}{suffix}")
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.read())
        file_chunks = split_audio_ffmpeg(tmp_path)
        all_chunks.extend(file_chunks)
    return all_chunks


def transcribe_with_openai(chunks: list, openai_key: str, progress_bar, status_text) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    full_transcript = []

    for i, chunk_path in enumerate(chunks):
        status_text.markdown(f"**Transcribing** part {i+1} of {len(chunks)} via Whisper API…")
        progress_bar.progress(0.05 + (i + 1) / len(chunks) * 0.65)
        with open(chunk_path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        full_transcript.append(response.strip())
        if os.path.exists(chunk_path):
            try:
                os.unlink(chunk_path)
            except Exception:
                pass

    return "\n\n".join(full_transcript)


def summarize_transcript(transcript: str, style: str, anthropic_key: str) -> str:
    import anthropic

    style_prompts = {
        "Concise (bullet points)": (
            "Summarize the following discourse using clear bullet points. "
            "Group related ideas under short bold headers. Be concise."
        ),
        "Detailed (paragraphs)": (
            "Write a detailed, well-structured summary of the following discourse in prose paragraphs. "
            "Cover all major themes, arguments, and conclusions."
        ),
        "Executive brief": (
            "Write a crisp executive brief (max 300 words) of the following discourse. "
            "Lead with the key message, then cover main points and any action items."
        ),
        "Academic digest": (
            "Produce an academic-style digest of the following discourse. "
            "Include: Overview, Key Arguments, Evidence/Examples, Conclusions, and Notable Quotes."
        ),
    }

    prompt = style_prompts.get(style, style_prompts["Concise (bullet points)"])
    client = anthropic.Anthropic(api_key=anthropic_key)

    max_chars = 150_000
    if len(transcript) > max_chars:
        parts = [transcript[i:i+max_chars] for i in range(0, len(transcript), max_chars)]
        partial_summaries = []
        for part in parts:
            msg = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[{"role": "user", "content": f"Summarize this section of a longer discourse:\n\n{part}"}],
            )
            partial_summaries.append(msg.content[0].text)
        combined = "\n\n".join(partial_summaries)
        final_msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": f"{prompt}\n\nHere are section summaries of the full discourse:\n\n{combined}"}],
        )
        return final_msg.content[0].text
    else:
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": f"{prompt}\n\n{transcript}"}],
        )
        return msg.content[0].text


# ── Main UI ────────────────────────────────────────────────────────────────────

st.markdown('<div class="step-label">Step 1 — Upload</div>', unsafe_allow_html=True)
st.markdown(
    "<small style='color:#555'>Upload a single long file <b>or</b> up to 4 shorter segments — "
    "transcribed in order and summarized together.</small>",
    unsafe_allow_html=True
)
st.markdown(" ")

uploaded_files = st.file_uploader(
    "Drop your audio file(s) here",
    type=["mp3", "m4a", "wav", "ogg"],
    accept_multiple_files=True,
    help="Upload 1 to 4 audio files. They will be processed in the order shown.",
)

if uploaded_files:
    total_size_mb = sum(f.size for f in uploaded_files) / (1024 * 1024)
    pills_html = "".join(
        f'<span class="file-pill">📁 {f.name} · {f.size / (1024*1024):.1f} MB</span>'
        for f in uploaded_files
    )
    st.markdown(
        f"{pills_html}<br><small style='color:#444'>{len(uploaded_files)} file(s) · {total_size_mb:.1f} MB total</small>",
        unsafe_allow_html=True
    )

    if len(uploaded_files) > 4:
        st.warning("⚠️ Maximum 4 files at a time. Please remove some files.")
    else:
        st.markdown("---")

        if not anthropic_key or not openai_key:
            st.warning("⚠️ Please enter both API keys in the sidebar to continue.")
        else:
            st.markdown('<div class="step-label">Step 2 — Process</div>', unsafe_allow_html=True)
            run_btn = st.button("🚀 Transcribe & Summarize")

            if run_btn:
                try:
                    st.markdown('<div class="step-label">Processing</div>', unsafe_allow_html=True)
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    status_text.markdown(f"**Preparing** {len(uploaded_files)} file(s)…")
                    progress_bar.progress(0.03)

                    all_chunks = prepare_all_chunks(uploaded_files)
                    status_text.markdown(f"**Sending** {len(all_chunks)} part(s) to Whisper API…")
                    progress_bar.progress(0.05)

                    transcript = transcribe_with_openai(all_chunks, openai_key, progress_bar, status_text)
                    progress_bar.progress(0.75)

                    status_text.markdown("**Transcription complete!** Sending to Claude…")
                    time.sleep(0.3)

                    summary = summarize_transcript(transcript, summary_style, anthropic_key)
                    progress_bar.progress(1.0)
                    status_text.markdown("✅ **Done!**")

                    st.markdown("---")
                    st.markdown('<div class="step-label">Step 3 — Results</div>', unsafe_allow_html=True)

                    # ── Summary ──
                    st.markdown("#### 📝 Summary")
                    st.markdown(f'<div class="output-box">{summary}</div>', unsafe_allow_html=True)

                    # ── Download buttons: Summary + Transcript ──
                    st.markdown(" ")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "⬇️ Download Summary (.txt)",
                            data=summary,
                            file_name="summary.txt",
                            mime="text/plain",
                        )
                    with col2:
                        st.download_button(
                            "⬇️ Download Transcript (.txt)",
                            data=transcript,
                            file_name="transcript.txt",
                            mime="text/plain",
                        )

                    # ── Optional: show full transcript on page ──
                    if show_transcript:
                        st.markdown("---")
                        st.markdown("#### 📄 Full Transcript")
                        st.markdown(f'<div class="output-box">{transcript}</div>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"❌ Error: {e}")

else:
    st.markdown("""
    <div style="text-align:center; color:#333; padding: 2rem 0; font-size:0.9rem;">
        No files uploaded yet.<br>
        <span style="font-size:0.8rem; color:#2a2a2a;">Single long file · or up to 4 segments · MP3 · M4A · WAV · OGG</span>
    </div>
    """, unsafe_allow_html=True)
