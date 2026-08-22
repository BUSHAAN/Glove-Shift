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
    QFormLayout,
    QLabel,
    QSlider,
    QComboBox,
    QMessageBox,
    QGroupBox,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
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
        vs.set_camera_index(saved["camera"])

        self._key_combos = {}
        self.initUI(saved)
        app.aboutToQuit.connect(self.cleanup)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_steering)
        self.pTime = 0

    def initUI(self, saved):
        self.setWindowTitle("Glove Shift")
        self.setFixedWidth(400)
        self.setMinimumHeight(420)

        icon_path = app_settings.asset_path("images", "icon.png")
        if os.path.isfile(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Primary action always visible
        self.button = QPushButton("Start Steering!")
        self.button.setMinimumHeight(36)
        self.button.clicked.connect(self.handle_button_click)

        tabs = QTabWidget()
        tabs.addTab(self._build_setup_tab(saved), "Setup")
        tabs.addTab(self._build_controls_tab(saved), "Controls")
        tabs.addTab(self._build_guide_tab(), "Guide")

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)
        layout.addWidget(self.button)
        layout.addWidget(tabs)
        self.setLayout(layout)

    def _build_setup_tab(self, saved):
        page = QWidget()
        form = QFormLayout()
        form.setSpacing(10)
        form.setContentsMargins(8, 12, 8, 8)

        self.camera_combo = QComboBox()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setFixedWidth(72)
        self.refresh_btn.clicked.connect(self.refresh_cameras)
        self._populate_cameras(saved["camera"])
        self.camera_combo.currentIndexChanged.connect(self.on_camera_changed)

        camera_row = QHBoxLayout()
        camera_row.addWidget(self.camera_combo, stretch=1)
        camera_row.addWidget(self.refresh_btn)

        self.hand_combo = QComboBox()
        for label, value in HAND_OPTIONS:
            self.hand_combo.addItem(label, value)
        hand_index = next(
            (i for i, (_, v) in enumerate(HAND_OPTIONS) if v == saved["hand"]),
            0,
        )
        self.hand_combo.setCurrentIndex(hand_index)
        self.hand_combo.currentIndexChanged.connect(self.on_hand_changed)

        form.addRow("Camera", camera_row)
        form.addRow("Hand", self.hand_combo)

        hint = QLabel("Choose your camera and hand, then press Start Steering.")
        hint.setWordWrap(True)
        hint.setStyleSheet("color: gray;")

        page_layout = QVBoxLayout()
        page_layout.addLayout(form)
        page_layout.addWidget(hint)
        page_layout.addStretch(1)
        page.setLayout(page_layout)
        return page

    def _build_controls_tab(self, saved):
        page = QWidget()
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(8, 12, 8, 8)
        page_layout.setSpacing(12)

        # Sensitivity group
        sens_box = QGroupBox("Sensitivity")
        sens_form = QFormLayout()
        sens_form.setSpacing(8)

        self.steering_slider = QSlider(Qt.Orientation.Horizontal)
        self.steering_slider.setRange(0, 100)
        self.steering_slider.setValue(saved["steering"])
        self.steering_value = QLabel(str(saved["steering"]))
        self.steering_value.setMinimumWidth(28)
        self.steering_slider.valueChanged.connect(self.on_sensitivity_changed)
        steer_row = QHBoxLayout()
        steer_row.addWidget(self.steering_slider)
        steer_row.addWidget(self.steering_value)

        self.smoothing_slider = QSlider(Qt.Orientation.Horizontal)
        self.smoothing_slider.setRange(0, 100)
        self.smoothing_slider.setValue(saved["smoothing"])
        self.smoothing_value = QLabel(self._smoothing_label(saved["smoothing"]))
        self.smoothing_value.setMinimumWidth(56)
        self.smoothing_slider.valueChanged.connect(self.on_sensitivity_changed)
        smooth_row = QHBoxLayout()
        smooth_row.addWidget(self.smoothing_slider)
        smooth_row.addWidget(self.smoothing_value)

        sens_form.addRow("Steering", steer_row)
        sens_form.addRow("Smoothing", smooth_row)
        sens_box.setLayout(sens_form)

        # Key mapping group
        keys_box = QGroupBox("Key mapping")
        keys_form = QFormLayout()
        keys_form.setSpacing(8)
        for label, action in ACTION_LABELS:
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
            keys_form.addRow(label, combo)

        reset_btn = QPushButton("Reset to WASD")
        reset_btn.clicked.connect(self.reset_keybinds)
        keys_form.addRow("", reset_btn)
        keys_box.setLayout(keys_form)

        page_layout.addWidget(sens_box)
        page_layout.addWidget(keys_box)
        page_layout.addStretch(1)
        page.setLayout(page_layout)
        return page

    def _build_guide_tab(self):
        page = QWidget()
        page_layout = QVBoxLayout()
        page_layout.setContentsMargins(8, 12, 8, 8)

        self.gesture_label = QLabel()
        self.gesture_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.gesture_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )
        self._load_gesture_image()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.gesture_label)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        page_layout.addWidget(scroll)
        page.setLayout(page_layout)
        return page

    def _populate_cameras(self, preferred_index=0):
        self.camera_combo.blockSignals(True)
        self.camera_combo.clear()
        cameras = vs.list_cameras()
        if not cameras:
            self.camera_combo.addItem("No camera found", 0)
            self.camera_combo.setEnabled(False)
        else:
            self.camera_combo.setEnabled(True)
            for cam in cameras:
                self.camera_combo.addItem(cam["name"], cam["index"])
            match = next(
                (
                    i
                    for i in range(self.camera_combo.count())
                    if self.camera_combo.itemData(i) == preferred_index
                ),
                0,
            )
            self.camera_combo.setCurrentIndex(match)
            vs.set_camera_index(self.camera_combo.currentData())
        self.camera_combo.blockSignals(False)

    def refresh_cameras(self):
        preferred = self.camera_combo.currentData()
        if preferred is None:
            preferred = vs.get_camera_index()
        was_running = self.steering_state
        if was_running:
            self.stop_steering()
        self._populate_cameras(preferred)
        self._persist()
        if was_running:
            self.handle_button_click()

    def _load_gesture_image(self):
        path = app_settings.asset_path("images", "Gesture_Controls_New.png")
        if not os.path.isfile(path):
            self.gesture_label.setText("Gesture_Controls_New.png not found in images/")
            return
        pixmap = QPixmap(path)
        if pixmap.isNull():
            self.gesture_label.setText("Could not load gesture guide image.")
            return
        scaled = pixmap.scaledToWidth(360, Qt.TransformationMode.SmoothTransformation)
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

    def _selected_camera(self):
        data = self.camera_combo.currentData()
        return int(data) if data is not None else 0

    def _persist(self):
        app_settings.save_settings(
            self.steering_slider.value(),
            self.smoothing_slider.value(),
            self.hand_combo.currentData(),
            self._current_keybinds(),
            self._selected_camera(),
        )

    def on_camera_changed(self, _index=None):
        index = self._selected_camera()
        vs.set_camera_index(index)
        self._persist()
        if self.steering_state:
            vs.stop_camera()
            if not vs.start_camera(index):
                self.stop_steering()
                QMessageBox.critical(
                    self,
                    "Camera Error",
                    f"Could not open Camera {index}. Pick another device or click Refresh.",
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
            index = self._selected_camera()
            vs.set_camera_index(index)
            if not vs.start_camera(index):
                QMessageBox.critical(
                    self,
                    "Camera Error",
                    "Could not access the selected camera. Try Refresh or pick another device.",
                )
                return

            self.steering_state = True
            self.button.setText("Stop Steering!")
            self.camera_combo.setEnabled(False)
            self.refresh_btn.setEnabled(False)
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
        has_camera = (
            self.camera_combo.count() > 0
            and self.camera_combo.itemText(0) != "No camera found"
        )
        self.camera_combo.setEnabled(has_camera)
        self.refresh_btn.setEnabled(True)

    def cleanup(self):
        self.steering_state = False
        self.timer.stop()
        vs.cleanup()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
