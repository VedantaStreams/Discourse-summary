import streamlit as st
import sys
import os
import tempfile
import requests
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
    <p class="subtitle">Extract audio · Transcribe · Summarize · All in one place</p>
</div>
""", unsafe_allow_html=True)

# ── Helper: fetch audio via Cobalt API ─────────────────────────────────────────
def fetch_via_cobalt(url: str) -> tuple:
    """Try to fetch audio via Cobalt API. Returns (audio_path, error_message)."""
    try:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": url,
            "downloadMode": "audio",
            "audioFormat": "mp3",
            "audioBitrate": "128"
        }
        resp = requests.post(
            "https://api.cobalt.tools/",
            json=payload,
            headers=headers,
            timeout=30
        )
        if resp.status_code != 200:
            return None, f"Cobalt API returned status {resp.status_code}."

        data = resp.json()
        status = data.get("status", "")

        if status in ("tunnel", "redirect"):
            audio_url = data.get("url", "")
            if not audio_url:
                return None, "No audio URL returned by Cobalt."
            audio_resp = requests.get(audio_url, timeout=180, stream=True)
            if audio_resp.status_code == 200:
                tmp_dir = tempfile.mkdtemp()
                audio_path = os.path.join(tmp_dir, "yt_audio.mp3")
                with open(audio_path, "wb") as f:
                    for chunk in audio_resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                return audio_path, None
            else:
                return None, f"Audio download failed: HTTP {audio_resp.status_code}."
        elif status == "error":
            err = data.get("error", {}).get("code", "unknown")
            return None, f"Cobalt error: {err}"
        else:
            return None, f"Unexpected Cobalt response: {status}"

    except requests.exceptions.Timeout:
        return None, "Request timed out. Try again."
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to Cobalt API."
    except Exception as e:
        return None, str(e)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-label">Step 1 — Choose Input</div>', unsafe_allow_html=True)
tab_yt, tab_mp4 = st.tabs(["▶ YouTube Video", "📁 Upload MP4"])

audio_ready_path = None


# ══════════════════════════════════════════════════════════════════════════════
# YOUTUBE TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_yt:

    st.markdown("""
<div class="about-box">
    Choose how to get your YouTube audio. <b>Option A</b> tries automatic extraction.
    <b>Option B</b> lets you paste a URL from an external tool and upload the audio directly here.
</div>
""", unsafe_allow_html=True)

    # placeholder to keep replace unique
    yt_tab_a, yt_tab_b = st.tabs([
        "⚡ Option A — Auto Extract",
        "🛠️ Option B — Manual + Upload Here"
    ])

    # ── OPTION A ──────────────────────────────────────────────────────────────
    with yt_tab_a:
        st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #c9a96e;
            border-radius:10px; padding:0.9rem 1.3rem; margin-bottom:1rem;">
    <div style="font-size:0.82rem; color:#888; line-height:1.8;">
        🔹 Uses <b style="color:#b8a88a;">Cobalt API</b> — free, no key needed<br/>
        🔹 Works with <b style="color:#b8a88a;">public YouTube videos</b> only<br/>
        🔹 If this fails, switch to <b style="color:#b8a88a;">Option B</b>
    </div>
</div>
""", unsafe_allow_html=True)

        yt_url_a = st.text_input(
            "Paste YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            key="yt_url_a"
        )

        if yt_url_a and yt_url_a.strip():
            cleaned_a = clean_youtube_url(yt_url_a.strip())
            if cleaned_a != yt_url_a.strip():
                st.info(f"ℹ️ Playlist removed — using: `{cleaned_a}`")

            if st.button("🎵 Auto Extract Audio", key="btn_cobalt"):
                with st.spinner("Fetching audio via Cobalt…"):
                    path, err = fetch_via_cobalt(cleaned_a)
                    if path:
                        size_mb = os.path.getsize(path) / (1024 * 1024)
                        st.success(f"✅ Audio fetched! ({size_mb:.1f} MB) — scroll down to transcribe.")
                        st.session_state["video_audio_path"] = path
                    else:
                        st.error(f"❌ {err}")
                        st.warning("👉 Switch to **Option B** tab to use a manual method.")

    # ── OPTION B ──────────────────────────────────────────────────────────────
    with yt_tab_b:
        st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #c9a96e;
            border-radius:10px; padding:0.9rem 1.3rem; margin-bottom:1rem;">
    <div style="font-size:0.82rem; color:#888; line-height:1.8;">
        Use any external tool to get the audio from YouTube, then
        <b style="color:#b8a88a;">upload the MP3 directly below</b>.
        The transcription and summary will appear here in this page — no need to go to Audio Summarizer.
    </div>
</div>
""", unsafe_allow_html=True)

        # URL cleaner
        raw_url_b = st.text_input(
            "Paste your YouTube URL here (to get a clean link)",
            placeholder="https://www.youtube.com/watch?v=...&list=...",
            key="yt_url_b",
            help="Strips playlist parameters — copy the clean URL into any tool below."
        )
        if raw_url_b and raw_url_b.strip():
            cleaned_b = clean_youtube_url(raw_url_b.strip())
            st.success(f"✅ Clean URL ready to copy: `{cleaned_b}`")
            st.caption("Copy this URL and use it in any of the tools below to download the audio.")

        st.markdown(" ")

        # Tool guide
        st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-radius:10px;
            padding:1.1rem 1.4rem; margin-bottom:0.7rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:0.95rem;
                color:#c9a96e; margin-bottom:0.6rem; font-weight:600;">
        ⭐ Tool 1 — cobalt.tools (Browser, no install)
    </div>
    <div style="font-size:0.82rem; color:#888; line-height:1.85;">
        <b style="color:#b8a88a;">1.</b> Open
        <a href="https://cobalt.tools" target="_blank" style="color:#c9a96e;">cobalt.tools</a>
        in a new browser tab<br/>
        <b style="color:#b8a88a;">2.</b> Paste the clean URL above → select <b>Audio only</b> → Download MP3<br/>
        <b style="color:#b8a88a;">3.</b> Upload the MP3 below ↓
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-radius:10px;
            padding:1.1rem 1.4rem; margin-bottom:0.7rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:0.95rem;
                color:#c9a96e; margin-bottom:0.6rem; font-weight:600;">
        🖥️ Tool 2 — 4K Video Downloader (Mac/PC app)
    </div>
    <div style="font-size:0.82rem; color:#888; line-height:1.85;">
        <b style="color:#b8a88a;">1.</b> Download free from
        <a href="https://www.4kdownload.com" target="_blank"
           style="color:#c9a96e;">4kdownload.com</a><br/>
        <b style="color:#b8a88a;">2.</b> Paste URL → <b>Paste Link</b> → <b>Extract Audio</b>
        → Format: <b>MP3</b> → Download<br/>
        <b style="color:#b8a88a;">3.</b> Upload the MP3 below ↓
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown(" ")

        # ── MP3 Upload in Option B ─────────────────────────────────────────────
        st.markdown("""
<div style="font-size:0.85rem; color:#c9a96e; font-weight:500; margin-bottom:0.4rem;">
    ⬆️ Upload your downloaded MP3 here — transcription appears below
</div>
""", unsafe_allow_html=True)

        uploaded_mp3 = st.file_uploader(
            "Upload MP3 from YouTube",
            type=["mp3", "m4a", "wav", "ogg"],
            key="manual_mp3_upload",
            help="Upload the audio file you downloaded using cobalt.tools or 4K Video Downloader."
        )

        if uploaded_mp3:
            file_size_mb = uploaded_mp3.size / (1024 * 1024)
            st.markdown(
                f'<span class="file-pill">🎵 {uploaded_mp3.name} · {file_size_mb:.1f} MB</span>',
                unsafe_allow_html=True
            )
            # Save to temp and store in session
            tmp_dir = tempfile.mkdtemp()
            suffix = Path(uploaded_mp3.name).suffix
            tmp_path = os.path.join(tmp_dir, f"manual_audio{suffix}")
            with open(tmp_path, "wb") as f:
                f.write(uploaded_mp3.read())
            st.session_state["video_audio_path"] = tmp_path
            st.success("✅ Audio uploaded and ready — scroll down to transcribe.")


# ══════════════════════════════════════════════════════════════════════════════
# MP4 UPLOAD TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_mp4:
    st.markdown("""
<div class="about-box">
    Upload an <b>MP4, MOV, MKV or WEBM</b> video file. Audio is extracted automatically
    using ffmpeg, then transcribed and summarized right here on this page.
</div>
""", unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload video file",
        type=["mp4", "mov", "mkv", "webm"],
        key="mp4_upload",
        help="Audio will be extracted automatically."
    )

    if video_file:
        file_size_mb = video_file.size / (1024 * 1024)
        st.markdown(
            f'<span class="file-pill">🎬 {video_file.name} · {file_size_mb:.1f} MB</span>',
            unsafe_allow_html=True
        )
        if st.button("🎵 Extract Audio from Video", key="extract_mp4"):
            with st.spinner("Extracting audio from video…"):
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
# SHARED PIPELINE — shown once audio is ready from ANY source
# ══════════════════════════════════════════════════════════════════════════════
audio_ready_path = st.session_state.get("video_audio_path", "")
if audio_ready_path and os.path.exists(audio_ready_path):

    st.markdown("---")

    # Show audio status bar
    size_mb = os.path.getsize(audio_ready_path) / (1024 * 1024)
    st.markdown(f"""
<div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #c9a96e;
            border-radius:8px; padding:0.7rem 1.2rem; margin-bottom:1rem;
            display:flex; align-items:center; gap:1rem;">
    <span style="color:#c9a96e; font-size:0.85rem;">🎵 Audio ready</span>
    <span style="color:#555; font-size:0.8rem;">{size_mb:.1f} MB</span>
    <span style="color:#444; font-size:0.8rem;">→ Configure options below and transcribe</span>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="step-label">Step 2 — Output Options</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        summary_style = st.selectbox(
            "Summary style",
            ["Bullet highlights", "Main takeaways", "Detailed paragraphs",
             "Executive brief", "Academic digest", "Structured table"],
            key="vid_style"
        )
    with col2:
        output_format = st.selectbox(
            "Download format", ["TXT", "PDF", "DOCX"],
            key="vid_format"
        )

    selected_columns = []
    if summary_style == "Structured table":
        st.markdown("**Select table columns:**")
        cols = list(TABLE_COLUMNS.keys())
        selected_columns = st.multiselect(
            "Choose columns to include", cols, default=cols,
            key="vid_cols"
        )
        if not selected_columns:
            st.warning("Please select at least one column.")

    show_transcript = st.checkbox("Show full transcript on page", value=False, key="vid_show_tr")
    st.markdown("---")

    if not anthropic_key or not openai_key:
        st.warning("⚠️ Please enter both API keys in the sidebar of the main page.")
        st.stop()

    st.markdown('<div class="step-label">Step 3 — Transcribe & Summarize</div>', unsafe_allow_html=True)

    if st.button("🚀 Transcribe & Summarize", key="vid_process"):
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
            summary = summarize_text(transcript, summary_style, selected_columns, anthropic_key)
            progress_bar.progress(1.0)
            status_text.markdown("✅ **Done!**")

            # Clear audio from session after processing
            st.session_state.pop("video_audio_path", None)

            st.markdown("---")
            st.markdown('<div class="step-label">Results</div>', unsafe_allow_html=True)

            # ── Transcript ────────────────────────────────────────────────────
            st.markdown("#### 📄 Full Transcript")
            st.markdown(f'<div class="output-box">{transcript}</div>', unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download Transcript (.txt)",
                data=transcript,
                file_name="transcript.txt",
                mime="text/plain",
                key="dl_transcript"
            )

            st.markdown("---")

            # ── Summary ───────────────────────────────────────────────────────
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
                st.download_button(
                    "⬇️ Summary (.txt)", data=summary,
                    file_name="summary.txt", mime="text/plain",
                    key="dl_summary_txt"
                )
            if output_format == "PDF":
                pdf_bytes = make_pdf(title, summary)
                with dc2:
                    st.download_button(
                        "⬇️ Summary (.pdf)", data=pdf_bytes,
                        file_name="summary.pdf", mime="application/pdf",
                        key="dl_summary_pdf"
                    )
            if output_format == "DOCX":
                docx_bytes = make_docx(title, summary)
                with dc3:
                    st.download_button(
                        "⬇️ Summary (.docx)", data=docx_bytes,
                        file_name="summary.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="dl_summary_docx"
                    )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
