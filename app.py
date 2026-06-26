import streamlit as st
from streamlit_webrtc import RTCConfiguration, webrtc_streamer

from processor import FaceExpressionProcessor


RTC_CONFIG = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


st.set_page_config(
    page_title="Face Expression Detector",
    page_icon=":smile:",
    layout="centered",
)

st.title("Real-Time Face Expression Detection")
st.caption("Powered by DeepFace, WebRTC, and OpenCV")

st.markdown(
    """
**Ekspresi yang bisa dideteksi:**
Happy, Sad, Angry, Fear, Surprise, Disgust, dan Neutral.
"""
)

st.divider()

webrtc_streamer(
    key="face-expression",
    video_processor_factory=FaceExpressionProcessor,
    rtc_configuration=RTC_CONFIG,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

st.divider()
st.markdown(
    "<small>Made with Streamlit, DeepFace, and OpenCV</small>",
    unsafe_allow_html=True,
)
