import av
import cv2
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
                silent=True,
            )
        except Exception:
            return av.VideoFrame.from_ndarray(img, format="bgr24")

        if isinstance(results, dict):
            results = [results]

        height, width = img.shape[:2]
        for face in results:
            region = face.get("region", {})
            x = max(0, int(region.get("x", 0)))
            y = max(0, int(region.get("y", 0)))
            w = max(0, int(region.get("w", 0)))
            h = max(0, int(region.get("h", 0)))

            x2 = min(width, x + w)
            y2 = min(height, y + h)
            emotion = face.get("dominant_emotion", "unknown")
            score = face.get("emotion", {}).get(emotion, 0.0)

            cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 100), 2)

            label = f"{emotion.upper()} ({score:.1f}%)"
            label_origin = (x, max(24, y - 10))
            cv2.putText(
                img,
                label,
                label_origin,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 100),
                2,
            )

        return av.VideoFrame.from_ndarray(img, format="bgr24")
