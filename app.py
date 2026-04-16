import streamlit as st
import base64
from pathlib import Path
from utils.styles import SHARED_CSS

st.set_page_config(
    page_title="Suma AI Hub",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(SHARED_CSS, unsafe_allow_html=True)


# ── Load images ────────────────────────────────────────────────────────────────
def img_b64(path: str, mime: str = "image/jpeg") -> str:
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

om_path = Path(__file__).parent / "Om.jpeg"
om_tag = f'<img class="om" src="{img_b64(str(om_path))}" alt="Om"/>' if om_path.exists() else '<div style="font-size:2.5rem">🕉️</div>'

headshot_path = Path(__file__).parent / "headshot.jpeg"
if headshot_path.exists():
    avatar_tag = f'<img class="bio-avatar" src="{img_b64(str(headshot_path))}" alt="Dr. Suma Rajashankar"/>'
else:
    avatar_tag = '<div class="bio-avatar-placeholder">SR</div>'


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
<div style="text-align:center; padding: 0.5rem 0 0.2rem;">
    {avatar_tag}
    <p class="bio-name-small">Dr. Suma Rajashankar</p>
    <p class="bio-role-small">Senior Data Scientist · AI Engineer</p>
    <div class="bio-link"><a href="About" target="_self">✦ About Me & Full Bio</a></div>
</div>
<hr class="bio-divider"/>
""", unsafe_allow_html=True)

    st.markdown("### ⚙️ API Keys")

    try:
        anthropic_key = st.secrets["ANTHROPIC_API_KEY"]
        st.success("✅ Anthropic key loaded")
    except Exception:
        anthropic_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")

    try:
        openai_key = st.secrets["OPENAI_API_KEY"]
        st.success("✅ OpenAI key loaded")
    except Exception:
        openai_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")

    st.session_state["anthropic_key"] = anthropic_key
    st.session_state["openai_key"] = openai_key

    st.markdown("---")
    st.markdown("<small style='color:#444'>🕉️ Suma AI Hub · Built with Streamlit, Whisper & Claude</small>", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    {om_tag}
    <h1>Suma <span class="accent">AI Hub</span></h1>
    <p class="subtitle">Transcribe · Summarize · Export · Audio · Video · Documents</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="quote-block">
    <div class="quote-text">
        "Renounce your ego" is the Lord's only request;<br>
        "And I will make you God" is the promise.
    </div>
    <div class="quote-author">— Swami Chinmayananda</div>
</div>
""", unsafe_allow_html=True)

# ── About box ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-box">
    <b>Welcome to Suma AI Hub</b> — a personal AI-powered platform for transcribing and summarizing
    spiritual discourses, lectures, and educational content. Upload <b>audio files</b> (MP3, WAV, M4A)
    or <b>video files</b> (MP4) or paste a <b>YouTube link</b> — get back a clean transcript, structured
    summary, or a beautifully formatted table of key insights. Export everything as <b>PDF or Word</b>.
    Use the navigation on the left to get started.
</div>
""", unsafe_allow_html=True)

# ── Navigation cards ───────────────────────────────────────────────────────────
st.markdown("## Choose a Tool")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background:#111; border:1px solid #2a2a2a; border-top: 3px solid #c9a96e;
                border-radius:12px; padding:1.2rem; text-align:center; min-height:140px;">
        <div style="font-size:1.8rem; margin-bottom:0.4rem;">🎙️</div>
        <div style="font-family:'Cormorant Garamond',serif; font-size:1.1rem; color:#e8e0d4; margin-bottom:0.4rem;">Audio Summarizer</div>
        <div style="font-size:0.78rem; color:#666;">Upload 1–5 MP3/WAV/M4A files or one long recording</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#111; border:1px solid #2a2a2a; border-top: 3px solid #c9a96e;
                border-radius:12px; padding:1.2rem; text-align:center; min-height:140px;">
        <div style="font-size:1.8rem; margin-bottom:0.4rem;">🎬</div>
        <div style="font-family:'Cormorant Garamond',serif; font-size:1.1rem; color:#e8e0d4; margin-bottom:0.4rem;">Video Summarizer</div>
        <div style="font-size:0.78rem; color:#666;">Paste a YouTube URL or upload an MP4 file</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background:#111; border:1px solid #2a2a2a; border-top: 3px solid #c9a96e;
                border-radius:12px; padding:1.2rem; text-align:center; min-height:140px;">
        <div style="font-size:1.8rem; margin-bottom:0.4rem;">📄</div>
        <div style="font-family:'Cormorant Garamond',serif; font-size:1.1rem; color:#e8e0d4; margin-bottom:0.4rem;">Document Combiner</div>
        <div style="font-size:0.78rem; color:#666;">Merge multiple transcripts into one beautiful document</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/><small style='color:#333'>Use the sidebar navigation (☰) to open each tool.</small>", unsafe_allow_html=True)
