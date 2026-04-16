import streamlit as st
import sys
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.styles import SHARED_CSS
from utils.helpers import (
    extract_audio_from_video,
    clean_youtube_url, split_audio_ffmpeg, transcribe_chunks,
    summarize_text, make_pdf, make_docx, TABLE_COLUMNS,
    markdown_table_to_html, TABLE_CSS
)

st.set_page_config(
    page_title="Video Summarizer · Suma AI Hub",
    page_icon="🎬",
    layout="centered"
)
st.markdown(SHARED_CSS, unsafe_allow_html=True)

anthropic_key = st.session_state.get("anthropic_key", "")
openai_key = st.session_state.get("openai_key", "")

if not anthropic_key:
    try: anthropic_key = st.secrets["ANTHROPIC_API_KEY"]
    except: pass
if not openai_key:
    try: openai_key = st.secrets["OPENAI_API_KEY"]
    except: pass


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🎬 Video <span class="accent">Summarizer</span></h1>
    <p class="subtitle">Use a YouTube URL or upload an MP4 · Audio extracted automatically · Transcribed & summarized</p>
</div>
""", unsafe_allow_html=True)

# ── Input tabs ─────────────────────────────────────────────────────────────────
st.markdown('<div class="step-label">Step 1 — Choose Input</div>', unsafe_allow_html=True)
tab_yt, tab_mp4 = st.tabs(["▶ YouTube Video", "📁 Upload MP4"])

video_file = None
yt_url = ""

# ── YouTube Tab ────────────────────────────────────────────────────────────────
with tab_yt:
    st.markdown("""
<div class="about-box">
    <b>ℹ️ How to use YouTube videos with this app</b><br/><br/>
    Due to YouTube's server restrictions, direct URL downloading is blocked on cloud platforms.
    Follow these simple steps to get your YouTube audio into the app:
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-radius:12px;
            padding:1.4rem 1.8rem; margin-bottom:1rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:1.05rem;
                color:#c9a96e; margin-bottom:0.8rem; font-weight:600;">
        ⭐ Method 1 — 4K Video Downloader (Recommended)
    </div>
    <div style="font-size:0.85rem; color:#888; line-height:1.9;">
        <b style="color:#b8a88a;">Step 1</b> — Download <b>4K Video Downloader</b> free from 4kdownload.com<br/>
        <b style="color:#b8a88a;">Step 2</b> — Open app and click <b>Paste Link</b><br/>
        <b style="color:#b8a88a;">Step 3</b> — Select <b>Extract Audio</b> → Format: <b>MP3</b> → Download<br/>
        <b style="color:#b8a88a;">Step 4</b> — Upload the MP3 in the Audio Summarizer page
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-radius:12px;
            padding:1.4rem 1.8rem; margin-bottom:1rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:1.05rem;
                color:#c9a96e; margin-bottom:0.8rem; font-weight:600;">
        🌐 Method 2 — Online Audio Extractor
    </div>
    <div style="font-size:0.85rem; color:#888; line-height:1.9;">
        <b style="color:#b8a88a;">Step 1</b> — Go to yt1s.com or ytmp3.cc in your browser<br/>
        <b style="color:#b8a88a;">Step 2</b> — Paste your YouTube URL and download as <b>MP3</b><br/>
        <b style="color:#b8a88a;">Step 3</b> — Upload the MP3 in the Audio Summarizer page
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-radius:12px;
            padding:1.4rem 1.8rem; margin-bottom:1rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:1.05rem;
                color:#c9a96e; margin-bottom:0.8rem; font-weight:600;">
        🎬 Method 3 — Download MP4 and Upload Below
    </div>
    <div style="font-size:0.85rem; color:#888; line-height:1.9;">
        <b style="color:#b8a88a;">Step 1</b> — Download the video as <b>MP4</b> using 4K Video Downloader<br/>
        <b style="color:#b8a88a;">Step 2</b> — Switch to the <b>Upload MP4</b> tab above<br/>
        <b style="color:#b8a88a;">Step 3</b> — Upload the MP4 — audio extracted and summarized automatically
    </div>
</div>
""", unsafe_allow_html=True)

    # Shortcut button to Audio Summarizer
    st.markdown(" ")
    if st.button("🎙️ Go to Audio Summarizer → Upload MP3 there", key="goto_audio"):
        st.switch_page("pages/2_Audio_Summarizer.py")

    # Paste URL helper — clean and show
    st.markdown("---")
    st.markdown(
        "<small style='color:#555'>💡 Paste your YouTube URL below to get the clean single-video link "
        "you can use with any of the methods above:</small>",
        unsafe_allow_html=True
    )
    raw_url = st.text_input(
        "Paste YouTube URL to clean it",
        placeholder="https://www.youtube.com/watch?v=...&list=...",
        help="Strips playlist and extra parameters — gives you a clean single video URL"
    )
    if raw_url and raw_url.strip():
        cleaned = clean_youtube_url(raw_url.strip())
        st.success(f"✅ Clean video URL: `{cleaned}`")
        st.markdown(
            "<small style='color:#555'>Copy this clean URL and use it with any method above.</small>",
            unsafe_allow_html=True
        )


# ── MP4 Upload Tab ─────────────────────────────────────────────────────────────
with tab_mp4:
    st.markdown("""
<div class="about-box">
    Upload an <b>MP4, MOV, MKV or WEBM</b> video file. The audio is extracted automatically
    using ffmpeg, then transcribed and summarized. Works with any video downloaded from
    YouTube, Vimeo, or recorded locally.
</div>
""", unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload video file",
        type=["mp4", "mov", "mkv", "webm"],
        help="Audio will be extracted automatically using ffmpeg."
    )
    if video_file:
        file_size_mb = video_file.size / (1024 * 1024)
        st.markdown(
            f'<span class="file-pill">🎬 {video_file.name} · {file_size_mb:.1f} MB</span>',
            unsafe_allow_html=True
        )


# ── Options + Process (only for MP4 upload) ───────────────────────────────────
if video_file:
    st.markdown("---")
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

    st.markdown('<div class="step-label">Step 3 — Process</div>', unsafe_allow_html=True)

    if st.button("🚀 Extract Audio · Transcribe · Summarize"):
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.markdown("**Extracting audio from video file…**")
            progress_bar.progress(0.05)

            tmp_dir = tempfile.mkdtemp()
            suffix = Path(video_file.name).suffix
            tmp_video = os.path.join(tmp_dir, f"video{suffix}")
            with open(tmp_video, "wb") as f:
                f.write(video_file.read())
            audio_path = extract_audio_from_video(tmp_video)

            progress_bar.progress(0.20)
            status_text.markdown("**Audio extracted. Splitting into chunks if needed…**")

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
            if summary_style == "Structured table":
                st.markdown(TABLE_CSS, unsafe_allow_html=True)
                st.markdown(markdown_table_to_html(summary), unsafe_allow_html=True)
            else:
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
                    st.download_button(
                        "⬇️ Summary (.docx)", data=docx_bytes,
                        file_name="summary.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

            st.download_button(
                "⬇️ Full Transcript (.txt)", data=transcript,
                file_name="transcript.txt", mime="text/plain"
            )

            if show_transcript:
                st.markdown("---")
                st.markdown("#### 📄 Full Transcript")
                st.markdown(f'<div class="output-box">{transcript}</div>', unsafe_allow_html=True)

            # Cleanup
            if audio_path and os.path.exists(audio_path):
                try: os.unlink(audio_path)
                except: pass

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
