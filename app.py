import streamlit as st
import tempfile
import os
import math
import time
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Discourse Summarizer",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Dark background */
.stApp {
    background-color: #0f0f0f;
    color: #e8e0d4;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    color: #e8e0d4;
}

/* Hero header */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #2a2a2a;
    margin-bottom: 2rem;
}
.hero h1 {
    font-size: 2.8rem;
    letter-spacing: -0.5px;
    margin-bottom: 0.3rem;
    color: #e8e0d4;
}
.hero p {
    font-size: 1rem;
    color: #888;
    font-weight: 300;
    letter-spacing: 0.5px;
}
.accent { color: #c9a96e; }

/* Upload area */
[data-testid="stFileUploader"] {
    border: 1.5px dashed #333;
    border-radius: 12px;
    padding: 1rem;
    background: #161616;
    transition: border-color 0.3s;
}
[data-testid="stFileUploader"]:hover {
    border-color: #c9a96e;
}

/* Buttons */
.stButton > button {
    background: #c9a96e !important;
    color: #0f0f0f !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    transition: opacity 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e0d4 !important;
    border-radius: 8px !important;
}

/* Text input */
.stTextInput > div > div > input {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e0d4 !important;
    border-radius: 8px !important;
}

/* Progress */
.stProgress > div > div {
    background: #c9a96e !important;
}

/* Info / success / warning boxes */
.stAlert {
    border-radius: 10px !important;
    border-left: 3px solid #c9a96e !important;
    background: #161616 !important;
    color: #e8e0d4 !important;
}

/* Transcript / summary box */
.output-box {
    background: #161616;
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
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 0.2rem 0.9rem;
    font-size: 0.78rem;
    color: #c9a96e;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}

/* Divider */
hr {
    border-color: #1e1e1e !important;
    margin: 1.8rem 0 !important;
}

/* Download button */
[data-testid="stDownloadButton"] > button {
    background: #1e1e1e !important;
    color: #c9a96e !important;
    border: 1px solid #c9a96e !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    width: 100%;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #c9a96e !important;
    color: #0f0f0f !important;
}

/* Checkbox */
.stCheckbox > label {
    color: #888 !important;
    font-size: 0.88rem !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #111 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎙️ Discourse <span class="accent">Summarizer</span></h1>
    <p>Upload a long MP3 · Get a clear, structured summary · Powered by Whisper + Claude</p>
</div>
""", unsafe_allow_html=True)


# ── Sidebar: API Key ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Get your key at console.anthropic.com",
    )
    st.markdown("---")
    whisper_model = st.selectbox(
        "Whisper Model",
        ["tiny", "base", "small", "medium", "large"],
        index=2,
        help="Larger = more accurate but slower. 'small' or 'medium' recommended for long audio.",
    )
    summary_style = st.selectbox(
        "Summary Style",
        ["Concise (bullet points)", "Detailed (paragraphs)", "Executive brief", "Academic digest"],
        index=0,
    )
    show_transcript = st.checkbox("Show full transcript", value=False)
    st.markdown("---")
    st.markdown("<small style='color:#555'>Built with Streamlit · Whisper · Claude</small>", unsafe_allow_html=True)


# ── Helper functions ───────────────────────────────────────────────────────────

def split_audio(path: str, chunk_minutes: int = 10) -> list[str]:
    """Split MP3 into chunks to handle large files and Whisper limits."""
    from pydub import AudioSegment
    audio = AudioSegment.from_mp3(path)
    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []
    total = len(audio)
    n = math.ceil(total / chunk_ms)
    base = Path(path).stem
    tmp_dir = tempfile.mkdtemp()
    for i in range(n):
        start = i * chunk_ms
        end = min((i + 1) * chunk_ms, total)
        chunk = audio[start:end]
        chunk_path = os.path.join(tmp_dir, f"{base}_chunk_{i+1}.mp3")
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks


def transcribe_chunks(chunks: list[str], model_name: str, progress_bar, status_text) -> str:
    """Transcribe each chunk with Whisper and concatenate."""
    import whisper
    model = whisper.load_model(model_name)
    full_transcript = []
    for i, chunk_path in enumerate(chunks):
        status_text.markdown(f"**Transcribing** chunk {i+1} of {len(chunks)}…")
        progress_bar.progress((i + 1) / len(chunks) * 0.7)  # 0–70% for transcription
        result = model.transcribe(chunk_path)
        full_transcript.append(result["text"].strip())
        os.unlink(chunk_path)  # cleanup chunk
    return "\n\n".join(full_transcript)


def summarize_transcript(transcript: str, style: str, api_key: str) -> str:
    """Send transcript to Claude API for summarization."""
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

    # If transcript is very long, chunk-summarize then final summarize
    max_chars = 150_000  # ~100k tokens safe limit
    if len(transcript) > max_chars:
        parts = [transcript[i:i+max_chars] for i in range(0, len(transcript), max_chars)]
        partial_summaries = []
        client = anthropic.Anthropic(api_key=api_key)
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
            messages=[{
                "role": "user",
                "content": f"{prompt}\n\nHere are section summaries of the full discourse:\n\n{combined}"
            }],
        )
        return final_msg.content[0].text
    else:
        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": f"{prompt}\n\n{transcript}"}],
        )
        return msg.content[0].text


# ── Main UI ────────────────────────────────────────────────────────────────────

st.markdown('<div class="step-label">Step 1 — Upload</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Drop your MP3 here",
    type=["mp3", "m4a", "wav", "ogg"],
    help="Supports MP3, M4A, WAV, OGG. Recommended: MP3.",
)

if uploaded_file:
    duration_hint = st.text_input(
        "Approximate duration (optional, for display only)",
        placeholder="e.g. 1h 32min",
    )
    file_size_mb = uploaded_file.size / (1024 * 1024)
    st.markdown(
        f"<small style='color:#666'>📁 {uploaded_file.name} · {file_size_mb:.1f} MB</small>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    if not api_key:
        st.warning("⚠️ Please enter your Anthropic API key in the sidebar to continue.")
    else:
        st.markdown('<div class="step-label">Step 2 — Process</div>', unsafe_allow_html=True)
        run_btn = st.button("🚀 Transcribe & Summarize")

        if run_btn:
            # ── Save upload to temp file ──
            suffix = Path(uploaded_file.name).suffix
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            try:
                # ── Transcription ──
                st.markdown('<div class="step-label">Transcription</div>', unsafe_allow_html=True)
                progress_bar = st.progress(0)
                status_text = st.empty()
                status_text.markdown("**Splitting audio** into chunks…")
                time.sleep(0.3)

                chunks = split_audio(tmp_path, chunk_minutes=10)
                progress_bar.progress(0.05)

                transcript = transcribe_chunks(chunks, whisper_model, progress_bar, status_text)
                progress_bar.progress(0.75)

                status_text.markdown("**Transcription complete!** Sending to Claude…")
                time.sleep(0.3)

                # ── Summarization ──
                summary = summarize_transcript(transcript, summary_style, api_key)
                progress_bar.progress(1.0)
                status_text.markdown("✅ **Done!**")

                st.markdown("---")
                st.markdown('<div class="step-label">Step 3 — Results</div>', unsafe_allow_html=True)

                # Summary output
                st.markdown("#### 📝 Summary")
                st.markdown(f'<div class="output-box">{summary}</div>', unsafe_allow_html=True)

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

                # Optionally show transcript
                if show_transcript:
                    st.markdown("---")
                    st.markdown("#### 📄 Full Transcript")
                    st.markdown(f'<div class="output-box">{transcript}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

else:
    st.markdown("""
    <div style="text-align:center; color:#444; padding: 2rem 0; font-size:0.9rem;">
        No file uploaded yet.<br>
        <span style="font-size:0.8rem;">Supports MP3 · M4A · WAV · OGG</span>
    </div>
    """, unsafe_allow_html=True)
