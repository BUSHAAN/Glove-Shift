import os
import sys
import time

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision


# Landmark edge list for drawing (MediaPipe hand topology)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (0, 9), (9, 10), (10, 11), (11, 12),
    (0, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17),
]


def _model_path():
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "models", "hand_landmarker.task")


class handDetector:
    def __init__(
        self,
        mode=False,
        maxHands=1,
        modelComplexity=1,
        detectionCon=0.5,
        trackCon=0.5,
    ):
        # mode/modelComplexity kept for call-site compatibility with older API
        del mode, modelComplexity
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.results = None
        self._timestamp_ms = 0

        model_path = _model_path()
        if not os.path.isfile(model_path):
            raise FileNotFoundError(
                f"Hand landmarker model not found at '{model_path}'. "
                "Download it from MediaPipe and place it under models/."
            )

        options = vision.HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=model_path),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=maxHands,
            min_hand_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon,
        )
        self.hands = vision.HandLandmarker.create_from_options(options)

    def findHands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

        self._timestamp_ms += 33
        self.results = self.hands.detect_for_video(mp_image, self._timestamp_ms)

        if draw and self.results.hand_landmarks:
            for hand_landmarks in self.results.hand_landmarks:
                self._draw_landmarks(img, hand_landmarks)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        del draw
        lm_list = []
        if not self.results or not self.results.hand_landmarks:
            return lm_list
        if handNo >= len(self.results.hand_landmarks):
            return lm_list

        h, w, _ = img.shape
        for idx, lm in enumerate(self.results.hand_landmarks[handNo]):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append([idx, cx, cy])
        return lm_list

    @staticmethod
    def _draw_landmarks(img, landmarks):
        h, w, _ = img.shape
        points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
        for a, b in HAND_CONNECTIONS:
            cv2.line(img, points[a], points[b], (0, 255, 0), 2)
        for point in points:
            cv2.circle(img, point, 4, (0, 0, 255), cv2.FILLED)


def main():
    p_time = 0
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot access camera. Check your privacy settings.")
        return

    detector = handDetector()
    while True:
        success, img = cap.read()
        if not success:
            break
        img = detector.findHands(img)
        lm_list = detector.findPosition(img)
        if lm_list:
            print(lm_list[4])

        c_time = time.time()
        fps = 1 / (c_time - p_time) if c_time != p_time else 0
        p_time = c_time
        img = cv2.flip(img, 1)
        cv2.putText(
            img,
            "FPS:" + str(int(fps)),
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3,
        )
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
