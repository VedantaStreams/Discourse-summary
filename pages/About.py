import streamlit as st
import base64
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from utils.styles import SHARED_CSS

st.set_page_config(page_title="About · Suma AI Hub", page_icon="🕉️", layout="centered")
st.markdown(SHARED_CSS, unsafe_allow_html=True)

def img_b64(path: str, mime: str = "image/jpeg") -> str:
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"

om_path = Path(__file__).parent.parent / "Om.jpeg"
headshot_path = Path(__file__).parent.parent / "headshot.jpeg"

om_tag = f'<img class="om" src="{img_b64(str(om_path))}" alt="Om"/>' if om_path.exists() else "🕉️"

if headshot_path.exists():
    hs_src = img_b64(str(headshot_path))
    headshot_html = f'<img src="{hs_src}" alt="Dr. Suma Rajashankar" style="width:180px;height:180px;border-radius:50%;object-fit:cover;border:3px solid #c9a96e;display:block;margin:0 auto 1rem;box-shadow:0 0 28px rgba(201,169,110,0.35);"/>'
else:
    headshot_html = '<div style="width:160px;height:160px;border-radius:50%;background:#1e1e1e;border:2px solid #c9a96e;display:flex;align-items:center;justify-content:center;font-family:Cormorant Garamond,serif;font-size:2rem;color:#c9a96e;margin:0 auto 1rem;">SR</div>'

st.markdown(f"""
<div class="hero">
    {om_tag}
    <h1>About <span class="accent">Dr. Suma Rajashankar</span></h1>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center; padding: 1.5rem 0 0.5rem;">
    {headshot_html}
    <div style="font-family:'Cormorant Garamond',serif; font-size:1.8rem; font-weight:600; color:#e8e0d4;">Dr. Suma Rajashankar</div>
    <div style="font-size:0.85rem; color:#c9a96e; letter-spacing:0.8px; text-transform:uppercase; margin-top:0.3rem;">
        Senior Data Scientist / AI Engineer · Capital One
    </div>
</div>
<hr style="border-color:#1e1e1e; margin: 1.2rem 0;"/>
""", unsafe_allow_html=True)

# ── Bio paragraphs ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="max-width:680px; margin: 0 auto; font-size:0.95rem; color:#999; line-height:1.85;">

<p>Dr. Suma Rajashankar holds a <b style="color:#b8a88a;">PhD in Physics</b> from the Indian Institute
of Science and completed her postdoctoral research at <b style="color:#b8a88a;">Stony Brook University</b>.
She went on to serve as an <b style="color:#b8a88a;">Assistant Professor</b> at Northern Illinois
University, where she taught across Electrical and Industrial Engineering disciplines for over
<b style="color:#b8a88a;">15 years</b>, shaping the academic journeys of countless students.</p>

<p>In a bold and purposeful career transition, she moved into <b style="color:#b8a88a;">AI and Data Science</b>
six years ago, contributing to impactful work at <b style="color:#b8a88a;">Discover Financial Services</b>
and currently at <b style="color:#b8a88a;">Capital One</b>. Her expertise spans
<b style="color:#b8a88a;">Generative AI</b>, Speech Recognition technologies, and
<b style="color:#b8a88a;">Responsible AI</b>, where she has played a key role in developing guardrails
for enterprise-scale AI engineering platforms.</p>

<p>Beyond her professional pursuits, Dr. Rajashankar has a deep and abiding interest in philosophy,
particularly the study of <b style="color:#b8a88a;">Vedanta</b>. She has been closely associated with
the <b style="color:#b8a88a;">Chinmaya Mission</b> for over two decades and finds great joy in the
systematic study of the Upanishads, the Bhagavad Gita, and traditional Prakarana Granthas, reflecting
a lifelong commitment to inner growth and inquiry.</p>

<p>Driven by a passion for both knowledge and mentorship, she actively guides working professionals
through <b style="color:#b8a88a;">AIML and AIDL programs</b> in collaboration with the
<b style="color:#b8a88a;">University of Texas at Austin</b> and <b style="color:#b8a88a;">Great Learning</b>,
helping them navigate and excel in the evolving AI landscape.</p>

</div>
<hr style="border-color:#1e1e1e; margin: 1.5rem auto; max-width:680px;"/>
""", unsafe_allow_html=True)

# ── Stats ──────────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns(3)
for col, num, label in [
    (c1, "350+", "Professionals Mentored"),
    (c2, "400+", "Hours of AI/ML Instruction"),
    (c3, "4.75–5.0", "Mentor Rating (4 Years)"),
]:
    with col:
        st.markdown(f"""
        <div style="background:#111; border:1px solid #2a2a2a; border-top:3px solid #c9a96e;
                    border-radius:10px; padding:1.2rem; text-align:center;">
            <div style="font-family:'Cormorant Garamond',serif; font-size:2rem; font-weight:600; color:#c9a96e;">{num}</div>
            <div style="font-size:0.75rem; color:#666; text-transform:uppercase; letter-spacing:0.5px;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Quote with styled Swamiji name ────────────────────────────────────────────
st.markdown("""
<hr style="border-color:#1e1e1e; margin: 1.5rem 0;"/>
<div style="text-align:center; padding: 0.5rem 0 1.5rem;">
    <div style="font-family:'Cormorant Garamond',serif; font-style:italic; font-size:1.15rem; color:#c9a96e; line-height:1.8;">
        "Renounce your ego" is the Lord's only request;<br/>
        "And I will make you God" is the promise.
    </div>
    <div style="font-family:'Cormorant Garamond',serif; font-size:1.05rem; color:#c9a96e;
                font-style:italic; letter-spacing:0.5px; margin-top:0.6rem;">
        — <em>Swami Chinmayananda</em>
    </div>
</div>
""", unsafe_allow_html=True)
