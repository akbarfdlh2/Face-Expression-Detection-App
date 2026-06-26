# Face Expression Detection App

Real-time face expression detection app built with Python, Streamlit, streamlit-webrtc, OpenCV, and DeepFace.

The dependency pins in `requirements.txt` are compatible with Python 3.12.

## Features

- Detects facial expressions from the browser webcam.
- Uses WebRTC, so it works better for browser and Streamlit Cloud deployments than `cv2.VideoCapture`.
- Draws face boxes and expression labels on the live video stream.
- Supports common DeepFace emotion labels: happy, sad, angry, fear, surprise, disgust, and neutral.

## Project Structure

```text
.
├── app.py
├── processor.py
├── requirements.txt
├── packages.txt
└── README.md
```

## Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows, activate it with:

```bat
venv\Scripts\activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

The first run can take longer because DeepFace downloads model weights.

## Deploy To Streamlit Cloud

1. Push this project to GitHub.
2. Open `https://streamlit.app`.
3. Create a new app from the repository.
4. Set the main file path to `app.py`.
5. Deploy.

Streamlit Cloud will read `requirements.txt` for Python dependencies and `packages.txt` for system packages.

## Notes

- Keep `opencv-python-headless` for cloud deployment.
- Webcam access requires browser permission.
- If the first detection feels slow, wait for the DeepFace model load to finish.
