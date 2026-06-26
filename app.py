import streamlit as st
from streamlit_webrtc import RTCConfiguration, WebRtcMode, webrtc_streamer

from processor import EMOTION_EMOJI, FaceExpressionProcessor


RTC_CONFIG = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


st.set_page_config(
    page_title="Face Expression Detector",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
/* Hide default Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* App background */
.stApp {
    background: radial-gradient(1200px 600px at 50% -10%, #1b2735 0%, #0b1220 55%, #060912 100%);
}

/* Hero */
.hero {
    text-align: center;
    padding: 2.4rem 1rem 1.4rem 1rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0;
    background: linear-gradient(90deg, #6ee7b7 0%, #38bdf8 50%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    color: #94a3b8;
    font-size: 1.05rem;
    margin-top: 0.6rem;
}

/* Pill badges under hero */
.badges {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.badge {
    background: rgba(148, 163, 184, 0.12);
    border: 1px solid rgba(148, 163, 184, 0.25);
    color: #cbd5e1;
    padding: 0.28rem 0.75rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Glass card */
.card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 18px;
    padding: 1.2rem 1.3rem;
    backdrop-filter: blur(6px);
}
.card h3 {
    margin-top: 0;
    color: #e2e8f0;
    font-size: 1.05rem;
}

/* Emotion chips */
.chips {
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
}
.chip {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 0.75rem;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.03);
    border-left: 4px solid var(--c);
    color: #e2e8f0;
    font-weight: 600;
    font-size: 0.92rem;
}
.chip .emoji { font-size: 1.25rem; }

/* Steps */
.steps { color: #cbd5e1; padding-left: 1.1rem; margin: 0; }
.steps li { margin-bottom: 0.5rem; line-height: 1.4; }

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
    padding: 1.4rem 0 0.6rem 0;
}
.footer a { color: #38bdf8; text-decoration: none; font-weight: 600; }
.footer a:hover { text-decoration: underline; }

/* Tighten video container */
video {
    border-radius: 16px !important;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.45);
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Emotion metadata (shared color palette with the video overlay)
# ---------------------------------------------------------------------------
EMOTION_COLORS = {
    "happy": "#fbbf24",
    "sad": "#60a5fa",
    "angry": "#f87171",
    "fear": "#a78bfa",
    "surprise": "#22d3ee",
    "disgust": "#34d399",
    "neutral": "#94a3b8",
}


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Panel Kontrol")
    st.caption("Atur pengalaman deteksi ekspresi kamu.")

    st.markdown("#### Cara Pakai")
    st.markdown(
        """
<ol class="steps">
  <li>Klik tombol <b>START</b> pada jendela video.</li>
  <li>Izinkan akses kamera saat browser meminta.</li>
  <li>Hadapkan wajah ke kamera dengan pencahayaan cukup.</li>
  <li>Lihat label ekspresi muncul secara real-time.</li>
</ol>
""",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("#### Tips")
    st.markdown(
        "- Gunakan cahaya dari depan, bukan dari belakang.\n"
        "- Pastikan wajah tidak tertutup.\n"
        "- Satu atau beberapa wajah didukung sekaligus."
    )

    st.divider()
    st.caption("🔒 Pemrosesan berjalan langsung di sesi kamu — video tidak disimpan.")


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="hero">
  <h1>Real-Time Face Expression Detection</h1>
  <p>Deteksi ekspresi wajah secara langsung lewat kamera kamu — cepat, privat, dan akurat.</p>
  <div class="badges">
    <span class="badge">⚡ Real-Time</span>
    <span class="badge">🧠 DeepFace</span>
    <span class="badge">📹 WebRTC</span>
    <span class="badge">🖼️ OpenCV</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Main layout: video + emotion legend
# ---------------------------------------------------------------------------
col_video, col_info = st.columns([2, 1], gap="large")

with col_video:
    st.markdown("#### 📷 Live Camera")
    webrtc_streamer(
        key="face-expression",
        mode=WebRtcMode.SENDRECV,
        video_processor_factory=FaceExpressionProcessor,
        rtc_configuration=RTC_CONFIG,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

with col_info:
    chips = "".join(
        f'<div class="chip" style="--c:{EMOTION_COLORS[name]}">'
        f'<span class="emoji">{emoji}</span>{name.title()}</div>'
        for name, emoji in EMOTION_EMOJI.items()
    )
    st.markdown(
        f"""
<div class="card">
  <h3>Ekspresi yang Terdeteksi</h3>
  <div class="chips">{chips}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="footer">
  Created by <a href="https://muhamadakbarfadilah.my.id/" target="_blank">Akbar Fadilah</a>
  &middot;
  Founder &amp; Co-Founder at <a href="https://afdatech.com/" target="_blank">Afda Technology Solutions</a>
</div>
""",
    unsafe_allow_html=True,
)
