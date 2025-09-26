import sys
import time
import cv2
import VirtualSteering as vs
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)
from PyQt6.QtCore import QTimer


class MyWindow(QWidget):
    steering_state = False

    def __init__(self):
        super().__init__()
        self.initUI()
        app.aboutToQuit.connect(self.cleanup)

        # Timer for steering loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_steering)

        self.pTime = 0  # Track FPS

    def initUI(self):
        self.setWindowTitle("Virtual Steering")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.button = QPushButton("Start Steering!")
        self.button.clicked.connect(self.handle_button_click)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def handle_button_click(self):
        if not self.steering_state:
            # Check camera before starting
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                QMessageBox.critical(
                    self,
                    "Camera Error",
                    "Could not access the camera. Please check if it is connected or used by another app."
                )
                cap.release()
                return
            cap.release()

            self.steering_state = True
            self.button.setText("Stop Steering!")
            self.pTime = time.time()

            # Start timer -> calls update_steering() every 30ms
            self.timer.start(30)

        else:
            self.stop_steering()

    def update_steering(self):
        if not self.steering_state:
            return

        cTime = time.time()
        fps = 1 / (cTime - self.pTime) if cTime != self.pTime else 0
        self.pTime = cTime

        vs.steering(fps)

    def stop_steering(self):
        self.steering_state = False
        self.button.setText("Start Steering!")
        self.timer.stop()

    def cleanup(self):
        self.stop_steering()
        vs.cleanup()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
