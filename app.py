import sys
import time
import VirtualSteering as vs
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from PyQt6.QtCore import QTimer


class MyWindow(QWidget):
    steering_state = False

    def __init__(self):
        super().__init__()
        self.initUI()
        app.aboutToQuit.connect(self.cleanup)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_steering)

        self.pTime = 0

    def initUI(self):
        self.setWindowTitle("Glove Shift")
        self.setFixedWidth(300)
        self.setFixedHeight(100)

        self.button = QPushButton("Start Steering!")
        self.button.clicked.connect(self.handle_button_click)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def handle_button_click(self):
        if not self.steering_state:
            if not vs.start_camera():
                QMessageBox.critical(
                    self,
                    "Camera Error",
                    "Could not access the camera. Please check if it is connected or used by another app.",
                )
                return

            self.steering_state = True
            self.button.setText("Stop Steering!")
            self.pTime = time.time()
            self.timer.start(30)
        else:
            self.stop_steering()

    def update_steering(self):
        if not self.steering_state:
            return

        cTime = time.time()
        fps = 1 / (cTime - self.pTime) if cTime != self.pTime else 0
        self.pTime = cTime

        if not vs.steering(fps):
            self.stop_steering()
            QMessageBox.warning(
                self,
                "Camera Disconnected",
                "The webcam stopped providing frames. Steering has been stopped and all keys were released.",
            )

    def stop_steering(self):
        self.steering_state = False
        self.button.setText("Start Steering!")
        self.timer.stop()
        vs.stop_camera()

    def cleanup(self):
        self.steering_state = False
        self.timer.stop()
        vs.cleanup()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
