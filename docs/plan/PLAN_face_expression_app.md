# 🎭 Face Expression Detection App
**Stack:** Python · OpenCV · DeepFace · Streamlit · streamlit-webrtc  
**Target Deploy:** [streamlit.app](https://streamlit.app) (free tier)

---

## 📁 Struktur Project

```
face-expression-app/
├── app.py                  # Main Streamlit app
├── processor.py            # Logic WebRTC + DeepFace
├── requirements.txt        # Dependencies
├── packages.txt            # System packages (untuk Streamlit Cloud)
└── README.md
```

---

## 📦 Dependencies

### `requirements.txt`
```
streamlit==1.35.0
streamlit-webrtc==0.47.6
deepface==0.0.93
opencv-python-headless==4.9.0.80
tf-keras==2.16.0
av==11.0.0
numpy==1.26.4
```

> ⚠️ Pakai `opencv-python-headless` bukan `opencv-python` — wajib untuk cloud deploy (no GUI).

### `packages.txt`
```
libgl1
libglib2.0-0
ffmpeg
```

> File ini dibaca Streamlit Cloud untuk install system-level packages via `apt`.

---

## 🧠 Logic Flow

```
Browser Webcam
     │
     ▼
streamlit-webrtc (WebRTC)
     │  (frame per frame via aiortc)
     ▼
VideoProcessorBase (processor.py)
     │  recv(frame) → numpy array
     ▼
DeepFace.analyze()
     │  → dominant_emotion, emotion scores
     ▼
cv2.putText() → bounding box + label
     │
     ▼
Return frame ke browser
```

---

## 📝 File by File

### `processor.py`
```python
import av
import cv2
import numpy as np
from deepface import DeepFace
from streamlit_webrtc import VideoProcessorBase

class FaceExpressionProcessor(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        try:
            results = DeepFace.analyze(
                img,
                actions=["emotion"],
                enforce_detection=False,
                silent=True
            )

            for face in results:
                region = face["region"]
                x, y, w, h = region["x"], region["y"], region["w"], region["h"]
                emotion = face["dominant_emotion"]
                score = face["emotion"][emotion]

                # Bounding box
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 100), 2)

                # Label ekspresi + confidence
                label = f"{emotion.upper()} ({score:.1f}%)"
                cv2.putText(
                    img, label, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 100), 2
                )

        except Exception:
            pass  # Skip frame jika tidak ada wajah

        return av.VideoFrame.from_ndarray(img, format="bgr24")
```

---

### `app.py`
```python
import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
from processor import FaceExpressionProcessor

# Config STUN server (wajib untuk Streamlit Cloud)
RTC_CONFIG = RTCConfiguration({
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
})

# --- UI ---
st.set_page_config(
    page_title="Face Expression Detector",
    page_icon="🎭",
    layout="centered"
)

st.title("🎭 Real-Time Face Expression Detection")
st.caption("Powered by DeepFace + WebRTC")

st.markdown("""
**Ekspresi yang bisa dideteksi:**  
😊 Happy · 😢 Sad · 😠 Angry · 😨 Fear · 😮 Surprise · 🤢 Disgust · 😐 Neutral
""")

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
    "<small>Made with ❤️ using Streamlit · DeepFace · OpenCV</small>",
    unsafe_allow_html=True
)
```

---

## 🚀 Cara Run Lokal

```bash
# 1. Buat virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

> Pertama kali run, DeepFace akan otomatis download model weights (~100MB). Tunggu sebentar.

---

## ☁️ Deploy ke Streamlit Cloud

1. Push semua file ke **GitHub repo** (public/private sama-sama bisa)
2. Buka [streamlit.app](https://streamlit.app) → **New app**
3. Pilih repo → set **Main file path:** `app.py`
4. Klik **Deploy**
5. Tunggu build selesai (~3-5 menit pertama kali)

> ✅ `packages.txt` dan `requirements.txt` akan otomatis dibaca oleh Streamlit Cloud.

---

## ⚠️ Catatan Penting

| Issue | Solusi |
|---|---|
| Webcam tidak jalan di cloud | Pastikan pakai `streamlit-webrtc`, bukan `cv2.VideoCapture` |
| Model lambat load pertama | Normal, DeepFace download weights sekali saja |
| Error `libGL` di cloud | Sudah diatasi via `packages.txt` + `opencv-python-headless` |
| Frame processing lambat | Set `async_processing=True` di `webrtc_streamer` |
| Deploy gagal dependency conflict | Pin versi di `requirements.txt` seperti contoh di atas |

---

## 🔧 Opsional: Upgrade Ideas

- [ ] Tambah **sidebar** untuk pilih model backend DeepFace (`opencv`, `retinaface`, `mtcnn`)
- [ ] Tambah **chart bar** confidence semua ekspresi (pakai `st.bar_chart`)
- [ ] Simpan **screenshot** frame + hasil deteksi
- [ ] **Multi-face** support (sudah otomatis, DeepFace return list)
- [ ] Tambah filter **minimum confidence** via slider

---

*Plan ini siap dieksekusi langsung di VS Code. Ikuti urutan: buat file → install deps → run lokal → push ke GitHub → deploy.*
