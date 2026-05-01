import streamlit as st
import base64
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.styles import SHARED_CSS

st.set_page_config(
    page_title="Wisdom Distiller · Suma AI Hub",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(SHARED_CSS, unsafe_allow_html=True)


# Extra button styling for nav cards
st.markdown("""
<style>
div[data-testid="column"] .stButton > button {
    background: transparent !important;
    color: #c9a96e !important;
    border: 1px solid #c9a96e !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    padding: 0.35rem 1rem !important;
    margin-top: 0.6rem;
    width: 100%;
    transition: all 0.2s !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: #c9a96e !important;
    color: #0a0a0a !important;
}
</style>
""", unsafe_allow_html=True)


# ── Load images ────────────────────────────────────────────────────────────────
def img_b64(path: str, mime: str = "image/jpeg") -> str:
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

om_path = Path(__file__).parent / "Om.jpeg"
gurudev_path = Path(__file__).parent / "gurudev.jpeg"
om_tag = f'<img class="om" src="{img_b64(str(om_path))}" alt="Om"/>' if om_path.exists() else '<div style="font-size:2.5rem">🕉️</div>'

headshot_path = Path(__file__).parent / "headshot.jpeg"
gurudev_path = Path(__file__).parent / "gurudev.jpeg"
if gurudev_path.exists():
    gd_src = img_b64(str(gurudev_path))
    gurudev_tag = f'<img src="{gd_src}" alt="Pujya Swami Chinmayananda" style="width:130px;height:150px;object-fit:cover;object-position:top;border-radius:8px;border:2px solid #c9a96e;box-shadow:0 0 20px rgba(201,169,110,0.3);"/>'
else:
    gurudev_tag = ''
if headshot_path.exists():
    hs_src = img_b64(str(headshot_path))
    avatar_tag = f'''
<img src="{hs_src}" alt="Suma Rajashankar"
     style="width:110px;height:110px;border-radius:50%;object-fit:cover;
            border:3px solid #c9a96e;display:block;margin:0 auto 0.6rem;
            box-shadow:0 0 20px rgba(201,169,110,0.3);"/>'''
else:
    avatar_tag = '<div class="bio-avatar-placeholder">SR</div>'


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
<div style="text-align:center; padding: 0.8rem 0 0.4rem;">
    {avatar_tag}
    <p style="font-family:'Cormorant Garamond',serif; font-size:1.05rem; font-weight:600;
              color:#e8e0d4; margin:0 0 0.15rem;">Suma Rajashankar</p>
    <p style="font-size:0.72rem; color:#c9a96e; letter-spacing:0.4px;
              text-transform:uppercase; margin:0 0 0.5rem;">
        Senior Data Scientist / AI Engineer
    </p>
    <div style="font-size:0.78rem;">
        <a href="About" target="_self"
           style="color:#c9a96e; text-decoration:none; border-bottom:1px dashed #c9a96e;">
            ✦ About Me &amp; Full Bio
        </a>
    </div>
</div>
<hr style="border-color:#1e1e1e; margin:0.8rem 0;"/>
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

    # ── Reverence & Gratitude ──────────────────────────────────────────────────
    st.markdown("""
<div style="background:#0d0d0d; border-left:2px solid #c9a96e; padding:0.8rem 1rem; border-radius:6px; margin-bottom:0.5rem;">
    <div style="font-size:0.78rem; color:#c9a96e; font-weight:500; letter-spacing:0.4px; margin-bottom:0.5rem;">
        🔹 With Reverence and Gratitude
    </div>
    <div style="font-size:0.75rem; color:#777; line-height:1.75; font-style:italic;">
        I offer my humble pran&#257;ms and heartfelt gratitude to
        P&#363;jya Swami Apar&#257;jit&#257;nandaj&#299; and
        P&#363;jya Sw&#257;m&#299; &#346;ara&#7751;&#257;nanda j&#299;.
        Their teachings, guidance, and unwavering dedication to the
        Guru&#8211;&#346;i&#7779;ya Parampar&#257; continue to inspire
        and shape this humble effort.
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<small style='color:#444'>🕉️ Suma AI Hub · Built with Streamlit, Whisper & Claude</small>", unsafe_allow_html=True)


# ── Main page Hero ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    {om_tag}
    <h1>Wisdom <span class="accent">Distiller</span></h1>
    <div style="font-family:'Cormorant Garamond',serif; font-style:italic;
                font-size:1.05rem; color:#c9a96e; letter-spacing:1px; margin:0.3rem 0 0.1rem;">
        &#x15A;rava&#x1E47;a &middot; Manana &middot; Nididhy&#x101;sana
    </div>
    <div style="font-size:0.82rem; color:#555; letter-spacing:0.8px; margin-bottom:0.2rem;">
        &#x936;&#x94D;&#x930;&#x935;&#x923; &middot; &#x92E;&#x928;&#x928; &middot; &#x928;&#x93F;&#x926;&#x93F;&#x927;&#x94D;&#x92F;&#x93E;&#x938;&#x928;
    </div>
    <div style="font-size:0.75rem; color:#3a3a3a; font-style:italic; letter-spacing:0.5px;">
        Listening &middot; Reflection &middot; Contemplation
    </div>
    <p class="subtitle" style="margin-top:0.6rem;">Transcribe · Summarize · Export · Audio · Video · Documents</p>
</div>
""", unsafe_allow_html=True)

# ── Bold tagline ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 2rem 1rem 1rem; max-width: 720px; margin: 0 auto;">
    <div style="font-family:'Cormorant Garamond',serif; font-size:1.6rem;
                font-weight:600; line-height:1.4; color:#e8e0d4; margin-bottom:1rem;">
        Distill the wisdom of sacred discourses into
        <span style="color:#c9a96e;">clear, lasting insights.</span>
    </div>
    <div style="font-size:1rem; color:#777; line-height:1.8; max-width:560px;
                margin-bottom:1.5rem;">
        Upload your spiritual discourses — in audio or video — and receive a beautifully structured transcript, summary, and table of key teachings, with Sanskrit terms transliterated into English. Output is available in <b style='color:#b8a88a;'>English (default)</b>, <b style='color:#b8a88a;'>Hindi</b>, <b style='color:#b8a88a;'>Kannada</b>, <b style='color:#b8a88a;'>Telugu</b>, and <b style='color:#b8a88a;'>Tamil</b>.
    </div>
    <div style="display:flex; gap:1.5rem; flex-wrap:wrap; align-items:center;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="color:#c9a96e; font-size:1rem;">✦</span>
            <span style="font-size:0.85rem; color:#666;">AI-Powered Transcription</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="color:#c9a96e; font-size:1rem;">✦</span>
            <span style="font-size:0.85rem; color:#666;">Sanskrit Transliteration</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="color:#c9a96e; font-size:1rem;">✦</span>
            <span style="font-size:0.85rem; color:#666;">Export as PDF or Word</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="color:#c9a96e; font-size:1rem;">✦</span>
            <span style="font-size:0.85rem; color:#666;">5 Language Outputs</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Quote with Gurudev photo ──────────────────────────────────────────────────
st.markdown(f"""
<div class="quote-block">
    <div style="display:flex; align-items:center; justify-content:center;
                gap:2rem; flex-wrap:wrap;">
        <div style="flex-shrink:0; text-align:center;">
            {gurudev_tag}
            <div style="font-size:0.72rem; color:#555; margin-top:6px;
                        font-style:italic; letter-spacing:0.3px;">
                Pūjya Swāmī Chinmayānanda
            </div>
        </div>
        <div style="flex:1; min-width:260px; text-align:left;">
            <div class="quote-text" style="text-align:left;">
                "Renounce your ego" is the Lord's only request;<br>
                "And I will make you God" is the promise.
            </div>
            <div style="font-family:'Cormorant Garamond',serif; font-size:1.05rem;
                        color:#c9a96e; font-style:italic; letter-spacing:0.5px; margin-top:0.5rem;">
                — <em>Pūjya Swāmī Chinmayānanda</em>
            </div>
            <div style="font-size:0.75rem; color:#555; margin-top:0.2rem;
                        font-style:italic; letter-spacing:0.3px;">
                (Pūjya Swāmī Chinmayānanda — the Bliss of Pure Consciousness)
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── About box ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-box">
    <b>Welcome to Wisdom Distiller</b> — an AI-powered platform for transcribing and summarizing
    spiritual discourses, lectures, and educational content. Upload <b>audio files</b> (MP3, WAV, M4A)
    or <b>video files</b> (MP4) or paste a <b>YouTube link</b> — get back a clean transcript, structured
    summary, or a beautifully formatted table of key insights. Export everything as <b>PDF or Word</b>.
    Click any tool below to get started.
</div>
""", unsafe_allow_html=True)

# ── Navigation cards with buttons ─────────────────────────────────────────────
st.markdown("## Choose a Tool")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background:#111; border:1px solid #2a2a2a; border-top:3px solid #c9a96e;
                border-radius:12px; padding:1.2rem; text-align:center; min-height:140px;">
        <div style="font-size:1.8rem; margin-bottom:0.4rem;">🎙️</div>
        <div style="font-family:'Cormorant Garamond',serif; font-size:1.1rem; color:#e8e0d4; margin-bottom:0.4rem;">Audio Summarizer</div>
        <div style="font-size:0.78rem; color:#666;">Upload 1–5 MP3/WAV/M4A files or one long recording</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🎙️ Open Audio Summarizer", key="btn_audio"):
        st.switch_page("pages/2_Audio_Summarizer.py")

with col2:
    st.markdown("""
    <div style="background:#111; border:1px solid #2a2a2a; border-top:3px solid #c9a96e;
                border-radius:12px; padding:1.2rem; text-align:center; min-height:140px;">
        <div style="font-size:1.8rem; margin-bottom:0.4rem;">🎬</div>
