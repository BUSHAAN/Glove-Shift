import os
import sys
import time

import VirtualSteering as vs
import settings as app_settings
import KeyboardInput as ki
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
    QGroupBox,
    QScrollArea,
    QSizePolicy,
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QIcon

HAND_OPTIONS = [
    ("Either hand", "either"),
    ("Left hand", "left"),
    ("Right hand", "right"),
]

ACTION_LABELS = [
    ("Accelerate", "accelerate"),
    ("Brake / reverse", "brake"),
    ("Steer left", "left"),
    ("Steer right", "right"),
]


class MyWindow(QWidget):
    steering_state = False

    def __init__(self):
        super().__init__()
        saved = app_settings.load_settings()
        vs.set_sensitivity(saved["steering"], saved["smoothing"])
        vs.set_hand_preference(saved["hand"])
        vs.set_keybinds(saved["keys"])

        self._key_combos = {}
        self.initUI(saved)
        app.aboutToQuit.connect(self.cleanup)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_steering)
        self.pTime = 0

    def initUI(self, saved):
        self.setWindowTitle("Glove Shift")
        self.setFixedWidth(380)
        self.setMinimumHeight(520)

        icon_path = app_settings.asset_path("images", "icon.png")
        if os.path.isfile(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.button = QPushButton("Start Steering!")
        self.button.clicked.connect(self.handle_button_click)

        # Hand preference
        self.hand_combo = QComboBox()
        for label, value in HAND_OPTIONS:
            self.hand_combo.addItem(label, value)
        hand_index = next(
            (i for i, (_, v) in enumerate(HAND_OPTIONS) if v == saved["hand"]),
            0,
        )
        self.hand_combo.setCurrentIndex(hand_index)
        self.hand_combo.currentIndexChanged.connect(self.on_hand_changed)

        hand_row = QHBoxLayout()
        hand_row.addWidget(QLabel("Hand"))
        hand_row.addWidget(self.hand_combo)

        # Sensitivity
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

        # Key remapping
        keys_box = QGroupBox("Key mapping")
        keys_layout = QVBoxLayout()
        for label, action in ACTION_LABELS:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            combo = QComboBox()
            for display, key_id in ki.KEY_CHOICES:
                combo.addItem(display, key_id)
            current = saved["keys"].get(action, ki.DEFAULT_BINDS[action])
            idx = next(
                (i for i, (_, kid) in enumerate(ki.KEY_CHOICES) if kid == current),
                0,
            )
            combo.setCurrentIndex(idx)
            combo.currentIndexChanged.connect(self.on_keybinds_changed)
            self._key_combos[action] = combo
            row.addWidget(combo)
            keys_layout.addLayout(row)

        reset_btn = QPushButton("Reset to WASD")
        reset_btn.clicked.connect(self.reset_keybinds)
        keys_layout.addWidget(reset_btn)
        keys_box.setLayout(keys_layout)

        # Gesture cheat sheet
        guide_box = QGroupBox("Gesture guide")
        guide_layout = QVBoxLayout()
        self.gesture_label = QLabel()
        self.gesture_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gesture_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self._load_gesture_image()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.gesture_label)
        scroll.setMinimumHeight(200)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        guide_layout.addWidget(scroll)
        guide_box.setLayout(guide_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addLayout(hand_row)
        layout.addLayout(steering_row)
        layout.addLayout(smoothing_row)
        layout.addWidget(keys_box)
        layout.addWidget(guide_box)
        self.setLayout(layout)

    def _load_gesture_image(self):
        path = app_settings.asset_path("images", "Gesture_Controls_New.png")
        if not os.path.isfile(path):
            self.gesture_label.setText("Gesture_Controls_New.png not found in images/")
            return
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.gesture_label.setText("Could not load gesture guide image.")
            return
        scaled = pixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation)
        self.gesture_label.setPixmap(scaled)

    @staticmethod
    def _smoothing_label(smoothing):
        frames = vs.get_sensitivity()["debounce_frames"]
        return f"{smoothing} ({frames}f)"

    def _current_keybinds(self):
        return {
            action: combo.currentData()
            for action, combo in self._key_combos.items()
        }

    def _persist(self):
        app_settings.save_settings(
            self.steering_slider.value(),
            self.smoothing_slider.value(),
            self.hand_combo.currentData(),
            self._current_keybinds(),
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

    def on_keybinds_changed(self, _index=None):
        vs.set_keybinds(self._current_keybinds())
        self._persist()

    def reset_keybinds(self):
        for action, default_key in ki.DEFAULT_BINDS.items():
            combo = self._key_combos[action]
            idx = next(
                (i for i, (_, kid) in enumerate(ki.KEY_CHOICES) if kid == default_key),
                0,
            )
            combo.blockSignals(True)
            combo.setCurrentIndex(idx)
            combo.blockSignals(False)
        vs.set_keybinds(dict(ki.DEFAULT_BINDS))
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
