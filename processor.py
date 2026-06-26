import av
import cv2
from deepface import DeepFace
from streamlit_webrtc import VideoProcessorBase


# Emoji shown in the Streamlit UI legend.
EMOTION_EMOJI = {
    "happy": "😄",
    "sad": "😢",
    "angry": "😠",
    "fear": "😨",
    "surprise": "😲",
    "disgust": "🤢",
    "neutral": "😐",
}

# BGR colors (OpenCV) per emotion — mirrors the UI palette in app.py.
EMOTION_BGR = {
    "happy": (36, 191, 251),
    "sad": (250, 165, 96),
    "angry": (113, 113, 248),
    "fear": (250, 139, 167),
    "surprise": (211, 211, 34),
    "disgust": (153, 211, 52),
    "neutral": (184, 163, 148),
}
DEFAULT_BGR = (200, 200, 200)


def _draw_label(img, text, x, y, color):
    """Draw a filled label chip with text above the face box."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.62
    thickness = 2
    (tw, th), baseline = cv2.getTextSize(text, font, scale, thickness)

    pad_x, pad_y = 8, 6
    top = max(0, y - th - baseline - 2 * pad_y)
    cv2.rectangle(
        img,
        (x, top),
        (x + tw + 2 * pad_x, top + th + baseline + 2 * pad_y),
        color,
        -1,
    )
    cv2.putText(
        img,
        text,
        (x + pad_x, top + th + pad_y),
        font,
        scale,
        (20, 20, 20),
        thickness,
        cv2.LINE_AA,
    )


def _draw_rounded_box(img, x, y, x2, y2, color, thickness=2, r=14):
    """Draw a rectangle with rounded corners."""
    r = max(2, min(r, (x2 - x) // 2, (y2 - y) // 2))
    cv2.line(img, (x + r, y), (x2 - r, y), color, thickness)
    cv2.line(img, (x + r, y2), (x2 - r, y2), color, thickness)
    cv2.line(img, (x, y + r), (x, y2 - r), color, thickness)
    cv2.line(img, (x2, y + r), (x2, y2 - r), color, thickness)
    cv2.ellipse(img, (x + r, y + r), (r, r), 180, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - r, y + r), (r, r), 270, 0, 90, color, thickness)
    cv2.ellipse(img, (x + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)


class FaceExpressionProcessor(VideoProcessorBase):
    # Run the heavy DeepFace analysis once every N frames and reuse the
    # cached result on the frames in between. Boxes are still drawn every
    # frame, so the overlay stays smooth without re-running detection.
    ANALYZE_EVERY = 5
    # Cap the longest side fed to DeepFace; detection accuracy holds up at
    # this size while inference gets noticeably faster on large webcams.
    DETECT_MAX_SIDE = 480

    def __init__(self) -> None:
        self._frame_count = 0
        self._faces: list[tuple[int, int, int, int, str, float]] = []

    def _analyze(self, img):
        height, width = img.shape[:2]
        scale = min(1.0, self.DETECT_MAX_SIDE / max(height, width))
        small = (
            cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            if scale < 1.0
            else img
        )

        results = DeepFace.analyze(
            small,
            actions=["emotion"],
            enforce_detection=False,
            silent=True,
        )
        if isinstance(results, dict):
            results = [results]

        inv = 1.0 / scale
        faces = []
        for face in results:
            region = face.get("region", {})
            w = int(region.get("w", 0) * inv)
            h = int(region.get("h", 0) * inv)
            # DeepFace returns the whole frame as a "face" when none is found.
            if w == 0 or h == 0 or (w >= width and h >= height):
                continue

            x = max(0, int(region.get("x", 0) * inv))
            y = max(0, int(region.get("y", 0) * inv))
            x2 = min(width, x + w)
            y2 = min(height, y + h)
            emotion = face.get("dominant_emotion", "unknown")
            score = face.get("emotion", {}).get(emotion, 0.0)
            faces.append((x, y, x2, y2, emotion, score))
        return faces

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        if self._frame_count % self.ANALYZE_EVERY == 0:
            try:
                self._faces = self._analyze(img)
            except Exception:
                pass
        self._frame_count += 1

        for x, y, x2, y2, emotion, score in self._faces:
            color = EMOTION_BGR.get(emotion, DEFAULT_BGR)
            _draw_rounded_box(img, x, y, x2, y2, color, thickness=3)
            _draw_label(img, f"{emotion.upper()}  {score:.0f}%", x, y, color)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
