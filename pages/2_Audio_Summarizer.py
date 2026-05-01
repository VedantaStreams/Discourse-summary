import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.styles import SHARED_CSS
from utils.helpers import (
    prepare_audio_chunks, transcribe_chunks,
    summarize_text, translate_text, make_pdf, make_docx,
    TABLE_COLUMNS, markdown_table_to_html, TABLE_CSS, LANGUAGES
)
import time

st.set_page_config(page_title="Audio Summarizer · Wisdom Distiller", page_icon="🎙️", layout="centered")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

anthropic_key = st.session_state.get("anthropic_key", "")
openai_key = st.session_state.get("openai_key", "")

# Fallback to secrets
if not anthropic_key:
    try: anthropic_key = st.secrets["ANTHROPIC_API_KEY"]
    except: pass
if not openai_key:
    try: openai_key = st.secrets["OPENAI_API_KEY"]
    except: pass

st.markdown("""
<div class="hero">
    <h1>🎙️ Audio <span class="accent">Summarizer</span></h1>
    <p class="subtitle">Upload up to 5 audio segments · Transcribe in order · Export summary</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="about-box">
    Upload a single long audio file <b>or</b> up to 5 shorter segments recorded in sequence.
    Files are transcribed in the order uploaded and combined into one unified summary.
    Supports <b>MP3, M4A, WAV, OGG</b>.
</div>
""", unsafe_allow_html=True)

# ── Upload ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="step-label">Step 1 — Upload Audio</div>', unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Drop audio file(s) here",
    type=["mp3", "m4a", "wav", "ogg"],
    accept_multiple_files=True,
    help="Upload 1–5 files in the correct order. Each is transcribed sequentially."
)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("⚠️ Maximum 5 files at a time.")
        st.stop()

    total_mb = sum(f.size for f in uploaded_files) / (1024 * 1024)
    pills = "".join(f'<span class="file-pill">📁 {f.name} · {f.size/(1024*1024):.1f}MB</span>' for f in uploaded_files)
    st.markdown(f"{pills}<br/><small style='color:#444'>{len(uploaded_files)} file(s) · {total_mb:.1f} MB total</small>", unsafe_allow_html=True)
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
            "Choose columns to include",
            cols,
            default=cols,
            help="Drag to reorder is not supported — columns appear in the order listed above."
        )
        if not selected_columns:
            st.warning("Please select at least one column.")

    with st.columns(2)[0]:
        output_language = st.selectbox(
            "Output language",
            list(LANGUAGES.keys()),
            key="audio_lang"
        )
    show_transcript = st.checkbox("Show full transcript on page", value=False)
    st.markdown("---")

    if not anthropic_key or not openai_key:
        st.warning("⚠️ Please enter both API keys in the sidebar of the main page.")
        st.stop()

    # ── Process ────────────────────────────────────────────────────────────────
    st.markdown('<div class="step-label">Step 3 — Process</div>', unsafe_allow_html=True)
    if st.button("🚀 Transcribe & Summarize"):
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.markdown("**Preparing audio chunks…**")
            progress_bar.progress(0.03)

            chunks = prepare_audio_chunks(uploaded_files)
            transcript = transcribe_chunks(chunks, openai_key, progress_bar, status_text)
            progress_bar.progress(0.75)

            status_text.markdown("**Transcription done! Summarizing with Claude…**")
            summary = summarize_text(transcript, summary_style, selected_columns, anthropic_key)
            progress_bar.progress(0.90)

            # Translate if needed
            target_lang = LANGUAGES.get(output_language)
            if target_lang:
                status_text.markdown(f"**Translating to {target_lang}...**")
                summary = translate_text(summary, target_lang, anthropic_key)
                transcript = translate_text(transcript, target_lang, anthropic_key)
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

            # ── Downloads ──────────────────────────────────────────────────────
            st.markdown(" ")
            dc1, dc2, dc3 = st.columns(3)

            title = "Discourse Summary"

            if output_format == "TXT" or True:  # always show txt
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

            # Always offer transcript download
            st.download_button("⬇️ Full Transcript (.txt)", data=transcript,
                               file_name="transcript.txt", mime="text/plain")

            if show_transcript:
                st.markdown("---")
                st.markdown("#### 📄 Full Transcript")
                st.markdown(f'<div class="output-box">{transcript}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")
