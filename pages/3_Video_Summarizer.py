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
    <p class="subtitle">Extract audio from YouTube or upload MP4 · Transcribe · Summarize</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN INPUT TABS — YouTube or MP4
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="step-label">Step 1 — Choose Input</div>', unsafe_allow_html=True)
tab_yt, tab_mp4 = st.tabs(["▶ YouTube Video", "📁 Upload MP4"])

audio_file_for_processing = None


# ══════════════════════════════════════════════════════════════════════════════
# YOUTUBE TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_yt:

    st.markdown("""
<div class="about-box">
    Choose how you want to extract audio from YouTube below.
    <b>Option A</b> uses the Cobalt API (automatic, no extra app needed).
    <b>Option B</b> guides you through a manual download if Option A does not work.
</div>
""", unsafe_allow_html=True)

    # ── Sub-tabs for YouTube method ────────────────────────────────────────────
    yt_tab_a, yt_tab_b = st.tabs([
        "⚡ Option A — Auto via Cobalt API",
        "🛠️ Option B — Manual Download Guide"
    ])

    # ── OPTION A — Cobalt API ──────────────────────────────────────────────────
    with yt_tab_a:
        st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #c9a96e;
            border-radius:10px; padding:1rem 1.4rem; margin-bottom:1rem;">
    <div style="font-size:0.82rem; color:#888; line-height:1.8;">
        🔹 <b style="color:#b8a88a;">No API key needed</b> — Cobalt is free and open source<br/>
        🔹 Works with <b style="color:#b8a88a;">public YouTube videos</b><br/>
        🔹 Does <b style="color:#b8a88a;">not work</b> with private, age-restricted, or live videos
    </div>
</div>
""", unsafe_allow_html=True)

        yt_url_a = st.text_input(
            "Paste YouTube URL",
            placeholder="https://www.youtube.com/watch?v=...",
            key="yt_url_a",
            help="Playlist links are cleaned automatically — just paste as-is."
        )

        if yt_url_a and yt_url_a.strip():
            cleaned_url = clean_youtube_url(yt_url_a.strip())
            if cleaned_url != yt_url_a.strip():
                st.info(f"ℹ️ Playlist removed — using: `{cleaned_url}`")

            if st.button("🎵 Fetch Audio Automatically", key="fetch_cobalt"):
                with st.spinner("Connecting to Cobalt API and fetching audio…"):
                    try:
                        headers = {
                            "Accept": "application/json",
                            "Content-Type": "application/json"
                        }
                        payload = {
                            "url": cleaned_url,
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
                            st.error(f"❌ Cobalt API error {resp.status_code}. Try Option B instead.")
                            st.stop()

                        data = resp.json()
                        status = data.get("status", "")

                        if status in ("tunnel", "redirect"):
                            audio_url = data.get("url", "")
                            if not audio_url:
                                st.error("❌ No audio URL returned. Try Option B.")
                                st.stop()

                            st.info("⬇️ Downloading audio…")
                            audio_resp = requests.get(audio_url, timeout=120, stream=True)
                            if audio_resp.status_code == 200:
                                tmp_dir = tempfile.mkdtemp()
                                audio_path = os.path.join(tmp_dir, "yt_audio.mp3")
                                with open(audio_path, "wb") as f:
                                    for chunk in audio_resp.iter_content(chunk_size=8192):
                                        f.write(chunk)
                                size_mb = os.path.getsize(audio_path) / (1024 * 1024)
                                st.success(f"✅ Audio fetched! ({size_mb:.1f} MB) — scroll down to transcribe.")
                                st.session_state["yt_audio_path"] = audio_path
                            else:
                                st.error(f"❌ Download failed: HTTP {audio_resp.status_code}. Try Option B.")

                        elif status == "error":
                            err = data.get("error", {}).get("code", "unknown")
                            st.error(f"❌ Cobalt error: {err}. Switch to Option B.")

                        else:
                            st.error(f"❌ Unexpected response. Switch to Option B.")

                    except requests.exceptions.Timeout:
                        st.error("❌ Request timed out. Try again or switch to Option B.")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Could not connect to Cobalt API. Check internet or try Option B.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}. Try Option B.")

        if st.session_state.get("yt_audio_path") and \
           os.path.exists(st.session_state.get("yt_audio_path", "")):
            size_mb = os.path.getsize(st.session_state["yt_audio_path"]) / (1024 * 1024)
            st.markdown(f"""
<div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #c9a96e;
            border-radius:8px; padding:0.8rem 1.2rem; margin-top:0.5rem;">
    <span style="color:#c9a96e; font-size:0.85rem;">✅ Audio ready</span>
    <span style="color:#555; font-size:0.8rem; margin-left:1rem;">{size_mb:.1f} MB · scroll down to transcribe</span>
</div>
""", unsafe_allow_html=True)
            audio_file_for_processing = st.session_state["yt_audio_path"]


    # ── OPTION B — Manual Guide ────────────────────────────────────────────────
    with yt_tab_b:

        st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #c9a96e;
            border-radius:10px; padding:1rem 1.4rem; margin-bottom:1.2rem;">
    <div style="font-size:0.82rem; color:#888; line-height:1.8;">
        Use this option if Option A fails — private videos, age-restricted content,
        or region-blocked videos. All methods below work on your Mac.
    </div>
</div>
""", unsafe_allow_html=True)

        # URL cleaner
        raw_url_b = st.text_input(
            "Paste your YouTube URL to get a clean link",
            placeholder="https://www.youtube.com/watch?v=...&list=...",
            key="yt_url_b",
            help="Strips playlist parameters so you can use it in the tools below."
        )
        if raw_url_b and raw_url_b.strip():
            cleaned_b = clean_youtube_url(raw_url_b.strip())
            st.success(f"✅ Clean URL: `{cleaned_b}`")
            st.caption("Copy this URL and use it with any method below.")

        st.markdown(" ")

        # Method 1
        st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-radius:10px;
            padding:1.2rem 1.5rem; margin-bottom:0.8rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:1rem;
                color:#c9a96e; margin-bottom:0.6rem; font-weight:600;">
        ⭐ Method 1 — 4K Video Downloader (Best quality)
    </div>
    <div style="font-size:0.83rem; color:#888; line-height:1.85;">
        <b style="color:#b8a88a;">1.</b> Download free from
        <a href="https://www.4kdownload.com" target="_blank" style="color:#c9a96e;">4kdownload.com</a><br/>
        <b style="color:#b8a88a;">2.</b> Paste URL → click <b>Paste Link</b><br/>
        <b style="color:#b8a88a;">3.</b> Choose <b>Extract Audio</b> → Format: <b>MP3</b> → Download<br/>
        <b style="color:#b8a88a;">4.</b> Upload the MP3 in the <b>Audio Summarizer</b> page
    </div>
</div>
""", unsafe_allow_html=True)

        # Method 2
        st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-radius:10px;
            padding:1.2rem 1.5rem; margin-bottom:0.8rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:1rem;
                color:#c9a96e; margin-bottom:0.6rem; font-weight:600;">
        🌐 Method 2 — Cobalt Browser (No install needed)
    </div>
    <div style="font-size:0.83rem; color:#888; line-height:1.85;">
        <b style="color:#b8a88a;">1.</b> Open
        <a href="https://cobalt.tools" target="_blank" style="color:#c9a96e;">cobalt.tools</a>
        in your browser<br/>
        <b style="color:#b8a88a;">2.</b> Paste your YouTube URL → select <b>Audio only</b> → Download<br/>
        <b style="color:#b8a88a;">3.</b> Upload the MP3 in the <b>Audio Summarizer</b> page
    </div>
</div>
""", unsafe_allow_html=True)

        # Method 3
        st.markdown("""
<div style="background:#111; border:1px solid #2a2a2a; border-radius:10px;
            padding:1.2rem 1.5rem; margin-bottom:0.8rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:1rem;
                color:#c9a96e; margin-bottom:0.6rem; font-weight:600;">
        🎬 Method 3 — Download MP4 and Upload Below
    </div>
    <div style="font-size:0.83rem; color:#888; line-height:1.85;">
        <b style="color:#b8a88a;">1.</b> Download the video as <b>MP4</b> using any tool<br/>
        <b style="color:#b8a88a;">2.</b> Switch to the <b>📁 Upload MP4</b> main tab above<br/>
        <b style="color:#b8a88a;">3.</b> Upload MP4 — audio extracted and summarized automatically
    </div>
</div>
""", unsafe_allow_html=True)

        st.markdown(" ")
        if st.button("🎙️ Go to Audio Summarizer", key="goto_audio"):
            st.switch_page("pages/2_Audio_Summarizer.py")


# ══════════════════════════════════════════════════════════════════════════════
# MP4 UPLOAD TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_mp4:
    st.markdown("""
<div class="about-box">
    Upload an <b>MP4, MOV, MKV or WEBM</b> video file. Audio is extracted automatically
    using ffmpeg, then transcribed and summarized. Works with any video downloaded
    from YouTube, Vimeo, or recorded locally.
</div>
""", unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload video file",
        type=["mp4", "mov", "mkv", "webm"],
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
                    st.session_state["mp4_audio_path"] = extracted
                    size_mb = os.path.getsize(extracted) / (1024 * 1024)
                    st.success(f"✅ Audio extracted! ({size_mb:.1f} MB) — scroll down to transcribe.")
                except Exception as e:
                    st.error(f"❌ Error extracting audio: {str(e)}")

    if st.session_state.get("mp4_audio_path") and \
       os.path.exists(st.session_state.get("mp4_audio_path", "")):
        audio_file_for_processing = st.session_state["mp4_audio_path"]


# ══════════════════════════════════════════════════════════════════════════════
# SHARED: OPTIONS + TRANSCRIPTION + RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if audio_file_for_processing:
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

    st.markdown('<div class="step-label">Step 3 — Transcribe & Summarize</div>', unsafe_allow_html=True)

    if st.button("🚀 Transcribe & Summarize", key="process_video"):
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.markdown("**Preparing audio chunks…**")
            progress_bar.progress(0.05)

            chunks = split_audio_ffmpeg(audio_file_for_processing)
            progress_bar.progress(0.15)

            transcript = transcribe_chunks(chunks, openai_key, progress_bar, status_text)
            progress_bar.progress(0.80)

            status_text.markdown("**Transcription done! Summarizing with Claude…**")
            summary = summarize_text(transcript, summary_style, selected_columns, anthropic_key)
            progress_bar.progress(1.0)
            status_text.markdown("✅ **Done!**")

            # Clear audio from session
            st.session_state.pop("yt_audio_path", None)
            st.session_state.pop("mp4_audio_path", None)

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

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

