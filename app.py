import sys
import time
import VirtualSteering as vs
import settings as app_settings
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSlider,
    QComboBox,
    QMessageBox,
)
from PyQt6.QtCore import QTimer, Qt

HAND_OPTIONS = [
    ("Either hand", "either"),
    ("Left hand", "left"),
    ("Right hand", "right"),
]


class MyWindow(QWidget):
    steering_state = False

    def __init__(self):
        super().__init__()
        saved = app_settings.load_settings()
        vs.set_sensitivity(saved["steering"], saved["smoothing"])
        vs.set_hand_preference(saved["hand"])

        self.initUI(saved)
        app.aboutToQuit.connect(self.cleanup)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_steering)

        self.pTime = 0

    def initUI(self, saved):
        self.setWindowTitle("Glove Shift")
        self.setFixedWidth(340)
        self.setMinimumHeight(220)

        self.button = QPushButton("Start Steering!")
        self.button.clicked.connect(self.handle_button_click)

        self.hand_combo = QComboBox()
        for label, value in HAND_OPTIONS:
            self.hand_combo.addItem(label, value)
        hand_index = max(
            0,
            next(
                (i for i, (_, v) in enumerate(HAND_OPTIONS) if v == saved["hand"]),
                0,
            ),
        )
        self.hand_combo.setCurrentIndex(hand_index)
        self.hand_combo.currentIndexChanged.connect(self.on_hand_changed)

        hand_row = QHBoxLayout()
        hand_row.addWidget(QLabel("Hand"))
        hand_row.addWidget(self.hand_combo)

        self.steering_slider = QSlider(Qt.Orientation.Horizontal)
        self.steering_slider.setRange(0, 100)
        self.steering_slider.setValue(saved["steering"])
        self.steering_value = QLabel(str(saved["steering"]))
        self.steering_value.setMinimumWidth(28)
        self.steering_slider.valueChanged.connect(self.on_sensitivity_changed)

        self.smoothing_slider = QSlider(Qt.Orientation.Horizontal)
        self.smoothing_slider.setRange(0, 100)
        self.smoothing_slider.setValue(saved["smoothing"])
        self.smoothing_value = QLabel(self._smoothing_label(saved["smoothing"]))
        self.smoothing_value.setMinimumWidth(72)
        self.smoothing_slider.valueChanged.connect(self.on_sensitivity_changed)

        steering_row = QHBoxLayout()
        steering_row.addWidget(QLabel("Steering sensitivity"))
        steering_row.addWidget(self.steering_slider)
        steering_row.addWidget(self.steering_value)

        smoothing_row = QHBoxLayout()
        smoothing_row.addWidget(QLabel("Smoothing"))
        smoothing_row.addWidget(self.smoothing_slider)
        smoothing_row.addWidget(self.smoothing_value)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addLayout(hand_row)
        layout.addLayout(steering_row)
        layout.addLayout(smoothing_row)
        self.setLayout(layout)

    @staticmethod
    def _smoothing_label(smoothing):
        frames = vs.get_sensitivity()["debounce_frames"]
        return f"{smoothing} ({frames}f)"

    def _persist(self):
        app_settings.save_settings(
            self.steering_slider.value(),
            self.smoothing_slider.value(),
            self.hand_combo.currentData(),
        )

    def on_hand_changed(self, _index=None):
        vs.set_hand_preference(self.hand_combo.currentData())
        self._persist()

    def on_sensitivity_changed(self, _value=None):
        steering = self.steering_slider.value()
        smoothing = self.smoothing_slider.value()
        vs.set_sensitivity(steering, smoothing)
        self.steering_value.setText(str(steering))
        self.smoothing_value.setText(self._smoothing_label(smoothing))
        self._persist()

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
