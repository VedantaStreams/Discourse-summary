import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.styles import SHARED_CSS

st.set_page_config(
    page_title="Get the App · Suma AI Hub",
    page_icon="📱",
    layout="centered"
)
st.markdown(SHARED_CSS, unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>📱 Get the <span class="accent">App</span></h1>
    <p class="subtitle">Use the Discourse Summarizer on your iPhone or Android</p>
</div>
""", unsafe_allow_html=True)


# ── Intro ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-box">
    The <b>Discourse Summarizer</b> is available as a web app that works beautifully
    on any device — iPhone, Android, tablet, or desktop. No app store download needed.
    Simply add it to your home screen and it works just like a native app.
    A dedicated mobile app is also coming soon.
</div>
""", unsafe_allow_html=True)


# ── Tabs for iPhone and Android ────────────────────────────────────────────────
tab_iphone, tab_android, tab_share = st.tabs([
    "🍎 iPhone",
    "🤖 Android",
    "🔗 Share with Mentees"
])


# ══════════════════════════════════════════════════════════════════════════════
# IPHONE TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_iphone:

    st.markdown(
        "<div style='font-family:Cormorant Garamond,serif; font-size:1.2rem;"
        " color:#c9a96e; font-weight:600; margin:1rem 0 0.5rem;'>"
        "Add to iPhone Home Screen (Recommended)</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a; border-radius:12px;"
        " padding:1.4rem 1.8rem; margin-bottom:1rem;'>"
        "<div style='font-size:0.84rem; color:#888; line-height:2;'>"
        "<b style='color:#b8a88a;'>Step 1.</b> Open <b>Safari</b> on your iPhone<br/>"
        "<b style='color:#b8a88a;'>Step 2.</b> Go to your Streamlit app URL<br/>"
        "<b style='color:#b8a88a;'>Step 3.</b> Tap the <b>Share button</b> "
        "(the square with an arrow at the bottom of Safari)<br/>"
        "<b style='color:#b8a88a;'>Step 4.</b> Scroll down and tap "
        "<b>Add to Home Screen</b><br/>"
        "<b style='color:#b8a88a;'>Step 5.</b> Tap <b>Add</b> in the top right<br/>"
        "<b style='color:#b8a88a;'>Step 6.</b> The app icon appears on your home screen!"
        "</div></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a;"
        " border-left:3px solid #c9a96e; border-radius:8px;"
        " padding:0.8rem 1.2rem; margin-bottom:1rem;'>"
        "<div style='font-size:0.82rem; color:#888; line-height:1.8;'>"
        "✅ Works offline for the UI<br/>"
        "✅ Looks and feels like a native app<br/>"
        "✅ No App Store download needed<br/>"
        "✅ Free forever<br/>"
        "✅ Always up to date automatically"
        "</div></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='font-family:Cormorant Garamond,serif; font-size:1.1rem;"
        " color:#c9a96e; font-weight:600; margin:1.5rem 0 0.5rem;'>"
        "Coming Soon — Native iPhone App</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a; border-radius:12px;"
        " padding:1.4rem 1.8rem; margin-bottom:1rem;'>"
        "<div style='font-size:0.84rem; color:#888; line-height:1.8;'>"
        "A dedicated <b style='color:#b8a88a;'>native iPhone app</b> built with Flutter "
        "is planned for the App Store. It will include:<br/><br/>"
        "&#x2022; Record audio directly on your phone<br/>"
        "&#x2022; Upload from Voice Memos or Files app<br/>"
        "&#x2022; Transcribe and summarize on the go<br/>"
        "&#x2022; Save summaries to your Notes app<br/><br/>"
        "<b style='color:#b8a88a;'>Interested in being notified when it launches?</b><br/>"
        "Send an email to "
        "<a href='mailto:vedantavani.manana@gmail.com'"
        " style='color:#c9a96e;'>vedantavani.manana@gmail.com</a>"
        " with subject: <i>App Notification</i>"
        "</div></div>",
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# ANDROID TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_android:

    st.markdown(
        "<div style='font-family:Cormorant Garamond,serif; font-size:1.2rem;"
        " color:#c9a96e; font-weight:600; margin:1rem 0 0.5rem;'>"
        "Add to Android Home Screen (Recommended)</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a; border-radius:12px;"
        " padding:1.4rem 1.8rem; margin-bottom:1rem;'>"
        "<div style='font-size:0.84rem; color:#888; line-height:2;'>"
        "<b style='color:#b8a88a;'>Step 1.</b> Open <b>Chrome</b> on your Android phone<br/>"
        "<b style='color:#b8a88a;'>Step 2.</b> Go to your Streamlit app URL<br/>"
        "<b style='color:#b8a88a;'>Step 3.</b> Tap the <b>three dots menu</b> "
        "(top right corner)<br/>"
        "<b style='color:#b8a88a;'>Step 4.</b> Tap <b>Add to Home screen</b><br/>"
        "<b style='color:#b8a88a;'>Step 5.</b> Tap <b>Add</b> to confirm<br/>"
        "<b style='color:#b8a88a;'>Step 6.</b> The app icon appears on your home screen!"
        "</div></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a;"
        " border-left:3px solid #c9a96e; border-radius:8px;"
        " padding:0.8rem 1.2rem; margin-bottom:1rem;'>"
        "<div style='font-size:0.82rem; color:#888; line-height:1.8;'>"
        "✅ Works on all Android phones and tablets<br/>"
        "✅ Looks and feels like a native app<br/>"
        "✅ No Play Store download needed<br/>"
        "✅ Free forever<br/>"
        "✅ Always up to date automatically"
        "</div></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='font-family:Cormorant Garamond,serif; font-size:1.1rem;"
        " color:#c9a96e; font-weight:600; margin:1.5rem 0 0.5rem;'>"
        "Coming Soon — Native Android App</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a; border-radius:12px;"
        " padding:1.4rem 1.8rem; margin-bottom:1rem;'>"
        "<div style='font-size:0.84rem; color:#888; line-height:1.8;'>"
        "A dedicated <b style='color:#b8a88a;'>native Android app</b> built with Flutter "
        "is planned for the Google Play Store. It will include:<br/><br/>"
        "&#x2022; Record audio directly on your phone<br/>"
        "&#x2022; Upload from any file manager or recorder<br/>"
        "&#x2022; Transcribe and summarize on the go<br/>"
        "&#x2022; Save summaries to Google Drive or Notes<br/><br/>"
        "<b style='color:#b8a88a;'>Interested in being notified when it launches?</b><br/>"
        "Send an email to "
        "<a href='mailto:vedantavani.manana@gmail.com'"
        " style='color:#c9a96e;'>vedantavani.manana@gmail.com</a>"
        " with subject: <i>App Notification</i>"
        "</div></div>",
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# SHARE WITH MENTEES TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_share:

    st.markdown(
        "<div style='font-family:Cormorant Garamond,serif; font-size:1.2rem;"
        " color:#c9a96e; font-weight:600; margin:1rem 0 0.5rem;'>"
        "Share with Your Mentees</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='about-box'>"
        "Share the Discourse Summarizer with your mentees, students, and fellow "
        "Vedanta seekers. They can use it on any device — phone, tablet, or desktop "
        "— with no download or installation required."
        "</div>",
        unsafe_allow_html=True
    )

    # Share options
    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a; border-radius:12px;"
        " padding:1.4rem 1.8rem; margin-bottom:0.8rem;'>"
        "<div style='font-family:Cormorant Garamond,serif; font-size:0.95rem;"
        " color:#c9a96e; font-weight:600; margin-bottom:0.6rem;'>&#x1F4E7; Share by Email</div>"
        "<div style='font-size:0.83rem; color:#888; line-height:1.8;'>"
        "Send your mentees this message:<br/><br/>"
        "<div style='background:#0d0d0d; border:1px solid #1e1e1e; border-radius:8px;"
        " padding:0.8rem 1rem; font-style:italic; color:#666; font-size:0.8rem;'>"
        "Dear [Name],<br/><br/>"
        "I would like to share a tool I have built for transcribing and summarizing "
        "spiritual discourses using AI. You can use it to get structured summaries "
        "of Vedanta lectures, Upanishad teachings, and other discourses.<br/><br/>"
        "Access it here: [your Streamlit URL]<br/><br/>"
        "On iPhone: open in Safari, tap Share, then Add to Home Screen.<br/>"
        "On Android: open in Chrome, tap the menu, then Add to Home Screen.<br/><br/>"
        "With pranams,<br/>"
        "Dr. Suma Rajashankar"
        "</div></div></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a; border-radius:12px;"
        " padding:1.4rem 1.8rem; margin-bottom:0.8rem;'>"
        "<div style='font-family:Cormorant Garamond,serif; font-size:0.95rem;"
        " color:#c9a96e; font-weight:600; margin-bottom:0.6rem;'>&#x1F4F1; Share via WhatsApp</div>"
        "<div style='font-size:0.83rem; color:#888; line-height:1.8;'>"
        "Simply send your Streamlit URL in WhatsApp. Recipients can:<br/>"
        "&#x2022; Open it directly in their mobile browser<br/>"
        "&#x2022; Add to Home Screen for a one-tap app experience<br/>"
        "&#x2022; Use it immediately with no signup required"
        "</div></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a; border-radius:12px;"
        " padding:1.4rem 1.8rem; margin-bottom:0.8rem;'>"
        "<div style='font-family:Cormorant Garamond,serif; font-size:0.95rem;"
        " color:#c9a96e; font-weight:600; margin-bottom:0.6rem;'>&#x2139;&#xFE0F; What your mentees need to know</div>"
        "<div style='font-size:0.83rem; color:#888; line-height:1.8;'>"
        "&#x2022; <b style='color:#b8a88a;'>No account needed</b> — open and use instantly<br/>"
        "&#x2022; <b style='color:#b8a88a;'>No download needed</b> — runs in the browser<br/>"
        "&#x2022; <b style='color:#b8a88a;'>Works on all devices</b> — iPhone, Android, desktop<br/>"
        "&#x2022; <b style='color:#b8a88a;'>Free to use</b> — no charges to users<br/>"
        "&#x2022; <b style='color:#b8a88a;'>Supports MP3, M4A, WAV, OGG</b> audio formats<br/>"
        "&#x2022; <b style='color:#b8a88a;'>Outputs in multiple formats</b> — bullets, table, PDF, Word"
        "</div></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div style='background:#111; border:1px solid #2a2a2a;"
        " border-left:3px solid #c9a96e; border-radius:8px;"
        " padding:0.8rem 1.2rem; margin-top:0.5rem;'>"
        "<div style='font-size:0.82rem; color:#888; line-height:1.8;'>"
        "Questions or feedback? Reach out at "
        "<a href='mailto:vedantavani.manana@gmail.com'"
        " style='color:#c9a96e;'>vedantavani.manana@gmail.com</a>"
        "</div></div>",
        unsafe_allow_html=True
    )
