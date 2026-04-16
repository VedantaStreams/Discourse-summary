import streamlit as st
import base64
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from utils.styles import SHARED_CSS

st.set_page_config(
    page_title="Reverence & Gratitude · Suma AI Hub",
    page_icon="🙏",
    layout="centered"
)
st.markdown(SHARED_CSS, unsafe_allow_html=True)

# ── Load Om image ──────────────────────────────────────────────────────────────
def img_b64(path: str, mime: str = "image/jpeg") -> str:
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

om_path = Path(__file__).parent.parent / "Om.jpeg"
om_tag = f'<img class="om" src="{img_b64(str(om_path))}" alt="Om"/>' if om_path.exists() else "🕉️"

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    {om_tag}
    <h1>With <span class="accent">Reverence & Gratitude</span></h1>
</div>
""", unsafe_allow_html=True)

# ── Divider line ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 0.5rem 0 1.5rem;">
    <div style="font-size:1.5rem; color:#c9a96e; letter-spacing:4px;">✦ ✦ ✦</div>
</div>
""", unsafe_allow_html=True)

# ── Main content block ─────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:660px; margin: 0 auto;">

    <div style="background:#111; border:1px solid #2a2a2a; border-left:3px solid #c9a96e;
                border-radius:12px; padding:2rem 2.2rem; margin-bottom:2rem;">

        <div style="font-family:'Cormorant Garamond',serif; font-size:1.05rem;
                    color:#c9a96e; font-weight:600; letter-spacing:0.5px; margin-bottom:1.2rem;">
            🔹 Pranāms & Gratitude
        </div>

        <div style="font-size:0.95rem; color:#aaa; line-height:1.9; font-style:italic;">
            I offer my humble pran&#257;ms and heartfelt gratitude to
            <span style="color:#c9a96e; font-style:normal; font-weight:500;">
                P&#363;jya Swami Apar&#257;jit&#257;nandaj&#299;
            </span>
            and
            <span style="color:#c9a96e; font-style:normal; font-weight:500;">
                P&#363;jya Sw&#257;m&#299; &#346;ara&#7751;&#257;nanda j&#299;
            </span>.
        </div>

        <div style="font-size:0.93rem; color:#888; line-height:1.9; margin-top:1rem;">
            Their teachings, guidance, and unwavering dedication to the
            <span style="color:#b8a88a;">Guru&#8211;&#346;i&#7779;ya Parampar&#257;</span>
            continue to inspire and shape this humble effort.
        </div>

    </div>

    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <div style="font-size:1.5rem; color:#2a2a2a; letter-spacing:6px;">— &#8212; —</div>
    </div>

    <div style="background:#0d0d0d; border:1px solid #1e1e1e; border-radius:12px;
                padding:1.5rem 2rem; text-align:center;">
        <div style="font-family:'Cormorant Garamond',serif; font-style:italic;
                    font-size:1.05rem; color:#c9a96e; line-height:1.8;">
            "Renounce your ego" is the Lord's only request;<br/>
            "And I will make you God" is the promise.
        </div>
        <div style="font-size:0.82rem; color:#666; line-height:1.8; margin-top:0.8rem;
                    font-style:italic; letter-spacing:0.3px;">
            <em>Aha&#7749;k&#257;ra tyajati iti Eva Bhagavat&#257;h pr&#257;rthan&#257;;</em><br/>
            <em>Tava&#257;ha&#7749;k&#257;ra tyajana&#257;t, Aha&#7749; tv&#257;&#7749; deva&#7745; karomi iti vacana&#7745;.</em>
        </div>
        <div style="font-size:0.75rem; color:#444; margin-top:0.5rem; letter-spacing:0.3px;">
            — Sanskrit transliteration of Swami Chinmayananda's teaching
        </div>
        <div style="font-family:'Cormorant Garamond',serif; font-size:1rem;
                    color:#c9a96e; font-style:italic; margin-top:0.8rem;">
            — <em>Swami Chinmayananda</em>
        </div>
    </div>

</div>
""", unsafe_allow_html=True)

# ── Bottom lotus ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem;">
    <div style="font-size:1.2rem; color:#2a2a2a; letter-spacing:8px;">🪷 🕉️ 🪷</div>
</div>
""", unsafe_allow_html=True)
