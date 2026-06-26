# Face Expression Detection App

Real-time facial expression detection in the browser, built with Streamlit, streamlit-webrtc, OpenCV, and DeepFace.

**🔗 Live demo:** https://face-expression-detection-app-createdbyakbarfdlh.streamlit.app/

## Features

- Detects facial expressions live from your webcam.
- Browser-based via WebRTC — works on Streamlit Cloud where `cv2.VideoCapture` does not.
- Draws colored, per-emotion boxes and labels on the video stream.
- Recognizes 7 emotions: happy, sad, angry, fear, surprise, disgust, and neutral.
- Optimized for smoothness: analysis runs every few frames on a downscaled image, with results cached in between.

## Tech Stack

| Layer      | Tool                              |
| ---------- | --------------------------------- |
| UI         | Streamlit                         |
| Streaming  | streamlit-webrtc (WebRTC)         |
| Detection  | DeepFace + TensorFlow (tf-keras)  |
| Imaging    | OpenCV (headless)                 |

> Dependency pins in `requirements.txt` target Python 3.12.

## Project Structure

```text
.
├── app.py            # Streamlit UI
├── processor.py      # WebRTC video frame processor (DeepFace inference + overlay)
├── requirements.txt  # Python dependencies
├── packages.txt      # System packages for Streamlit Cloud
└── README.md
```

## Run Locally

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
python3 -m pip install -r requirements.txt

# 3. Launch
streamlit run app.py
```

The first run is slower because DeepFace downloads its model weights once.

## Deploy to Streamlit Cloud

1. Push the project to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app from the repo.
3. Set **Main file path** to `app.py`.
4. Click **Deploy**.

Streamlit Cloud reads `requirements.txt` for Python packages and `packages.txt` for system libraries automatically.

## Notes

- Keep `opencv-python-headless` (not `opencv-python`) for cloud deployments.
- Webcam access requires browser permission.
- Processing happens in your session — video is not stored.

## Credits

Created by [Akbar Fadilah](https://muhamadakbarfadilah.my.id/) · Founder & Co-Founder at [Afda Technology Solutions](https://afdatech.com/)
