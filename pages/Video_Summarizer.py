import streamlit as st
import sys
import os
import tempfile
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.styles import SHARED_CSS
from utils.helpers import (
    extract_audio_from_video, download_youtube_audio,
    split_audio_ffmpeg, transcribe_chunks,
    summarize_text, make_pdf, make_docx, TABLE_COLUMNS
)

st.set_page_config(page_title="Video Summarizer · Suma AI Hub", page_icon="🎬", layout="centered")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

anthropic_key = st.session_state.get("anthropic_key", "")
openai_key = st.session_state.get("openai_key", "")

if not anthropic_key:
    try: anthropic_key = st.secrets["ANTHROPIC_API_KEY"]
    except: pass
if not openai_key:
    try: openai_key = st.secrets["OPENAI_API_KEY"]
    except: pass

st.markdown("""
<div class="hero">
    <h1>🎬 Video <span class="accent">Summarizer</span></h1>
    <p class="subtitle">Paste a YouTube URL or upload an MP4 · Audio extracted automatically · Transcribed & summarized</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="about-box">
    Provide a <b>YouTube URL</b> or upload an <b>MP4 video file</b>. The app automatically extracts
    the audio, transcribes it via OpenAI Whisper API, and summarizes it with Claude.
    No manual audio extraction needed.
</div>
""", unsafe_allow_html=True)

# ── Input tabs ─────────────────────────────────────────────────────────────────
st.markdown('<div class="step-label">Step 1 — Choose Input</div>', unsafe_allow_html=True)
tab_yt, tab_mp4 = st.tabs(["▶ YouTube URL", "📁 Upload MP4"])

audio_path = None
source_label = ""

with tab_yt:
    yt_url = st.text_input(
        "Paste YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="The video must be publicly accessible."
    )
    if yt_url:
        source_label = f"YouTube: {yt_url[:60]}..."

with tab_mp4:
    video_file = st.file_uploader(
        "Upload MP4 video file",
        type=["mp4", "mov", "mkv", "webm"],
        help="Audio will be extracted automatically using ffmpeg."
    )
    if video_file:
        file_size_mb = video_file.size / (1024 * 1024)
        st.markdown(f'<span class="file-pill">🎬 {video_file.name} · {file_size_mb:.1f} MB</span>', unsafe_allow_html=True)
        source_label = video_file.name

has_input = (yt_url if 'yt_url' in dir() else "") or video_file

if has_input:
    st.markdown("---")

    # ── Options ────────────────────────────────────────────────────────────────
    st.markdown('<div class="step-label">Step 2 — Output Options</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        summary_style = st.selectbox(
            "Summary style",
            ["Bullet highlights", "Main takeaways", "Detailed paragraphs",
             "Executive brief", "Academic digest", "Structured table"],
        )
    with col2:
        output_format = st.selectbox("Download format", ["TXT", "PDF", "DOCX"])

    selected_columns = []
    if summary_style == "Structured table":
        st.markdown("**Select table columns:**")
        cols = list(TABLE_COLUMNS.keys())
        selected_columns = st.multiselect(
            "Choose columns to include", cols, default=cols
        )
        if not selected_columns:
            st.warning("Please select at least one column.")

    show_transcript = st.checkbox("Show full transcript on page", value=False)
    st.markdown("---")

    if not anthropic_key or not openai_key:
        st.warning("⚠️ Please enter both API keys in the sidebar of the main page.")
        st.stop()

    # ── Process ────────────────────────────────────────────────────────────────
    st.markdown('<div class="step-label">Step 3 — Process</div>', unsafe_allow_html=True)
    if st.button("🚀 Extract Audio · Transcribe · Summarize"):
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Extract audio
            if yt_url and yt_url.strip():
                status_text.markdown("**Downloading audio from YouTube…** (this may take a minute)")
                progress_bar.progress(0.05)
                audio_path = download_youtube_audio(yt_url.strip())
            elif video_file:
                status_text.markdown("**Extracting audio from video file…**")
                progress_bar.progress(0.05)
                tmp_dir = tempfile.mkdtemp()
                suffix = Path(video_file.name).suffix
                tmp_video = os.path.join(tmp_dir, f"video{suffix}")
                with open(tmp_video, "wb") as f:
                    f.write(video_file.read())
                audio_path = extract_audio_from_video(tmp_video)

            progress_bar.progress(0.20)
            status_text.markdown("**Audio ready. Splitting into chunks if needed…**")

            chunks = split_audio_ffmpeg(audio_path)
            progress_bar.progress(0.25)

            transcript = transcribe_chunks(chunks, openai_key, progress_bar, status_text)
            progress_bar.progress(0.80)

            status_text.markdown("**Transcription done! Summarizing with Claude…**")
            summary = summarize_text(transcript, summary_style, selected_columns, anthropic_key)
            progress_bar.progress(1.0)
            status_text.markdown("✅ **Done!**")

            st.markdown("---")
            st.markdown('<div class="step-label">Results</div>', unsafe_allow_html=True)

            st.markdown("#### 📝 Summary")
            st.markdown(f'<div class="output-box">{summary}</div>', unsafe_allow_html=True)

            st.markdown(" ")
            dc1, dc2, dc3 = st.columns(3)
            title = "Video Discourse Summary"

            with dc1:
                st.download_button("⬇️ Summary (.txt)", data=summary,
                                   file_name="summary.txt", mime="text/plain")
            if output_format == "PDF":
                pdf_bytes = make_pdf(title, summary)
                with dc2:
                    st.download_button("⬇️ Summary (.pdf)", data=pdf_bytes,
                                       file_name="summary.pdf", mime="application/pdf")
            if output_format == "DOCX":
                docx_bytes = make_docx(title, summary)
                with dc3:
                    st.download_button("⬇️ Summary (.docx)", data=docx_bytes,
                                       file_name="summary.docx",
                                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

            st.download_button("⬇️ Full Transcript (.txt)", data=transcript,
                               file_name="transcript.txt", mime="text/plain")

            if show_transcript:
                st.markdown("---")
                st.markdown("#### 📄 Full Transcript")
                st.markdown(f'<div class="output-box">{transcript}</div>', unsafe_allow_html=True)

            # Cleanup
            if audio_path and os.path.exists(audio_path):
                try: os.unlink(audio_path)
                except: pass

        except Exception as e:
            st.error(f"❌ Error: {e}")
