import streamlit as st
import sys
import os
import tempfile
import subprocess
import math
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.styles import SHARED_CSS
from utils.helpers import (
    extract_audio_from_video,
    clean_youtube_url,
    split_audio_ffmpeg,
    transcribe_chunks,
    summarize_text,
    make_pdf,
    make_docx,
    TABLE_COLUMNS,
    markdown_table_to_html,
    TABLE_CSS
)

st.set_page_config(
    page_title="Video Summarizer · Suma AI Hub (Local)",
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
    <p class="subtitle">Paste a YouTube URL or upload MP4 · Audio extracted automatically · Transcribe · Summarize</p>
</div>
""", unsafe_allow_html=True)


# ── yt-dlp download function ───────────────────────────────────────────────────
def download_youtube_audio_local(url: str, status_text, progress_bar) -> str:
    """Download YouTube audio using yt-dlp — works locally on Mac."""
    url = clean_youtube_url(url)
    tmp_dir = tempfile.mkdtemp()
    output_template = os.path.join(tmp_dir, "yt_audio.%(ext)s")

    status_text.markdown("**Downloading audio from YouTube…** (this may take 1–2 minutes)")
    progress_bar.progress(0.10)

    result = subprocess.run(
        [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", "5",
            "--no-playlist",
            "--no-warnings",
            "-o", output_template,
            url
        ],
        capture_output=True,
        text=True,
        timeout=300
    )

    if result.returncode != 0:
        error = result.stderr[:400] if result.stderr else "Unknown error"
        raise RuntimeError(
            f"yt-dlp failed.\n\n"
            f"Details: {error}\n\n"
            f"Make sure yt-dlp is installed: run `pip install yt-dlp` in your terminal."
        )

    # Find the downloaded file
    for f in os.listdir(tmp_dir):
        if f.startswith("yt_audio"):
            return os.path.join(tmp_dir, f)

    raise FileNotFoundError(
        "Audio file not found after download. "
        "The video may be private, age-restricted, or region-blocked."
    )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-label">Step 1 — Choose Input</div>', unsafe_allow_html=True)
tab_yt, tab_mp4 = st.tabs(["▶ YouTube Video", "📁 Upload MP4"])


# ══════════════════════════════════════════════════════════════════════════════
# YOUTUBE TAB — FULLY AUTOMATIC via yt-dlp
# ══════════════════════════════════════════════════════════════════════════════
with tab_yt:
    st.markdown("""
<div class="about-box">
    Paste a YouTube URL — audio is downloaded and extracted <b>automatically</b>
    using yt-dlp running on your Mac. Works with public videos, playlists are
    cleaned automatically. Paste the full URL as-is.
</div>
""", unsafe_allow_html=True)

    yt_url = st.text_input(
        "Paste YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        key="yt_url_local",
        help="Playlist links are cleaned automatically — just paste as-is."
    )

    if yt_url and yt_url.strip():
        cleaned = clean_youtube_url(yt_url.strip())
        if cleaned != yt_url.strip():
            st.info(f"ℹ️ Playlist removed — using: `{cleaned}`")

        if st.button("🎵 Download & Extract Audio", key="btn_yt_local"):
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()

                audio_path = download_youtube_audio_local(
                    cleaned, status_text, progress_bar
                )
                size_mb = os.path.getsize(audio_path) / (1024 * 1024)
                progress_bar.progress(0.25)
                status_text.markdown(f"**Audio downloaded!** ({size_mb:.1f} MB) — ready to transcribe.")
                st.session_state["video_audio_path"] = audio_path
                st.success(f"✅ Audio ready ({size_mb:.1f} MB) — scroll down to transcribe.")

            except subprocess.TimeoutExpired:
                st.error("❌ Download timed out. The video may be too long.")
            except FileNotFoundError as e:
                st.error(f"❌ {str(e)}")
            except RuntimeError as e:
                st.error(f"❌ {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")


# ══════════════════════════════════════════════════════════════════════════════
# MP4 UPLOAD TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_mp4:
    st.markdown("""
<div class="about-box">
    Upload an <b>MP4, MOV, MKV or WEBM</b> video file. Audio is extracted
    automatically using ffmpeg, then transcribed and summarized.
</div>
""", unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload video file",
        type=["mp4", "mov", "mkv", "webm"],
        key="mp4_local",
        help="Audio extracted automatically."
    )

    if video_file:
        file_size_mb = video_file.size / (1024 * 1024)
        st.markdown(
            f'<span class="file-pill">🎬 {video_file.name} · {file_size_mb:.1f} MB</span>',
            unsafe_allow_html=True
        )
        if st.button("🎵 Extract Audio from Video", key="extract_mp4_local"):
            with st.spinner("Extracting audio…"):
                try:
                    tmp_dir = tempfile.mkdtemp()
                    suffix = Path(video_file.name).suffix
                    tmp_video = os.path.join(tmp_dir, f"video{suffix}")
                    with open(tmp_video, "wb") as f:
                        f.write(video_file.read())
                    extracted = extract_audio_from_video(tmp_video)
                    size_mb = os.path.getsize(extracted) / (1024 * 1024)
                    st.session_state["video_audio_path"] = extracted
                    st.success(f"✅ Audio extracted! ({size_mb:.1f} MB) — scroll down to transcribe.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


# ══════════════════════════════════════════════════════════════════════════════
# SHARED PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
audio_ready_path = st.session_state.get("video_audio_path", "")
if audio_ready_path and os.path.exists(audio_ready_path):

    st.markdown("---")
    size_mb = os.path.getsize(audio_ready_path) / (1024 * 1024)
    st.markdown(f"""
<div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #c9a96e;
            border-radius:8px; padding:0.7rem 1.2rem; margin-bottom:1rem;">
    <span style="color:#c9a96e; font-size:0.85rem;">🎵 Audio ready</span>
    <span style="color:#555; font-size:0.8rem; margin-left:1rem;">{size_mb:.1f} MB</span>
    <span style="color:#444; font-size:0.8rem;"> → configure options below</span>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="step-label">Step 2 — Output Options</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        summary_style = st.selectbox(
            "Summary style",
            ["Bullet highlights", "Main takeaways", "Detailed paragraphs",
             "Executive brief", "Academic digest", "Structured table"],
            key="vid_style_local"
        )
    with col2:
        output_format = st.selectbox(
            "Download format", ["TXT", "PDF", "DOCX"],
            key="vid_format_local"
        )

    selected_columns = []
    if summary_style == "Structured table":
        st.markdown("**Select table columns:**")
        cols = list(TABLE_COLUMNS.keys())
        selected_columns = st.multiselect(
            "Choose columns to include", cols, default=cols,
            key="vid_cols_local"
        )
        if not selected_columns:
            st.warning("Please select at least one column.")

    show_transcript = st.checkbox(
        "Show full transcript on page", value=False,
        key="vid_show_tr_local"
    )
    st.markdown("---")

    if not anthropic_key or not openai_key:
        st.warning("⚠️ Please enter both API keys in the sidebar.")
        st.stop()

    st.markdown('<div class="step-label">Step 3 — Transcribe & Summarize</div>', unsafe_allow_html=True)

    if st.button("🚀 Transcribe & Summarize", key="vid_process_local"):
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.markdown("**Splitting audio into chunks if needed…**")
            progress_bar.progress(0.05)

            chunks = split_audio_ffmpeg(audio_ready_path)
            progress_bar.progress(0.15)

            transcript = transcribe_chunks(chunks, openai_key, progress_bar, status_text)
            progress_bar.progress(0.80)

            status_text.markdown("**Transcription done! Summarizing with Claude…**")
            summary = summarize_text(
                transcript, summary_style, selected_columns, anthropic_key
            )
            progress_bar.progress(1.0)
            status_text.markdown("✅ **Done!**")

            st.session_state.pop("video_audio_path", None)

            st.markdown("---")
            st.markdown('<div class="step-label">Results</div>', unsafe_allow_html=True)

            # Transcript
            st.markdown("#### 📄 Full Transcript")
            st.markdown(
                f'<div class="output-box">{transcript}</div>',
                unsafe_allow_html=True
            )
            st.download_button(
                "⬇️ Download Transcript (.txt)",
                data=transcript,
                file_name="transcript.txt",
                mime="text/plain",
                key="dl_tr_local"
            )

            st.markdown("---")

            # Summary
            st.markdown("#### 📝 Summary")
            if summary_style == "Structured table":
                st.markdown(TABLE_CSS, unsafe_allow_html=True)
                st.markdown(markdown_table_to_html(summary), unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="output-box">{summary}</div>',
                    unsafe_allow_html=True
                )

            st.markdown(" ")
            dc1, dc2, dc3 = st.columns(3)
            title = "Video Discourse Summary"

            with dc1:
                st.download_button(
                    "⬇️ Summary (.txt)", data=summary,
                    file_name="summary.txt", mime="text/plain",
                    key="dl_sum_txt_local"
                )
            if output_format == "PDF":
                pdf_bytes = make_pdf(title, summary)
                with dc2:
                    st.download_button(
                        "⬇️ Summary (.pdf)", data=pdf_bytes,
                        file_name="summary.pdf", mime="application/pdf",
                        key="dl_sum_pdf_local"
                    )
            if output_format == "DOCX":
                docx_bytes = make_docx(title, summary)
                with dc3:
                    st.download_button(
                        "⬇️ Summary (.docx)", data=docx_bytes,
                        file_name="summary.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="dl_sum_docx_local"
                    )

            if show_transcript:
                st.markdown("---")
                st.markdown("#### 📄 Full Transcript")
                st.markdown(
                    f'<div class="output-box">{transcript}</div>',
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
