import sys
import cv2
import HandTrackingModule as htm
import KeyboardInput as ki

wCam, hCam = 384, 288
CAMERA_INDEX = 0
_camera_index = CAMERA_INDEX
_MAX_CAMERA_PROBE = 8

# User-facing sensitivity (0–100). Defaults match prior hard-coded feel.
_steering_ui = 50
_smoothing_ui = 40
_debounce_frames = 3
_tilt_enter_left = 20
_tilt_enter_right = -25
_tilt_exit_left = 10
_tilt_exit_right = -12

cap = None
detector = None
_window_ready = False

_pending_keys = ()
_pending_count = 0
_active_keys = ()
_active_steer = None  # "left" | "right" | None

# "either" | "left" | "right" — which hand(s) may drive input
_hand_preference = "either"

# Logical action → physical key id (see KeyboardInput.SCAN_CODES)
_keybinds = {
    "accelerate": "w",
    "brake": "s",
    "left": "a",
    "right": "d",
}


def get_hand_preference():
    return _hand_preference


def set_hand_preference(hand):
    """Accept either, left, or right. Invalid values fall back to either."""
    global _hand_preference
    hand = (hand or "either").lower()
    if hand not in ("either", "left", "right"):
        hand = "either"
    if hand != _hand_preference:
        _hand_preference = hand
        _reset_debounce()


def get_keybinds():
    return dict(_keybinds)


def set_keybinds(binds):
    """
    Update action→key mapping. Expected keys:
    accelerate, brake, left, right (physical ids from KeyboardInput.SCAN_CODES).
    """
    global _keybinds
    updated = dict(_keybinds)
    for action in ("accelerate", "brake", "left", "right"):
        if action in binds and binds[action] in ki.SCAN_CODES:
            updated[action] = binds[action]
    if updated != _keybinds:
        _clear_input()
        _keybinds = updated
        ki.set_bound_keys(_keybinds.values())


# Keep KeyboardInput release_all in sync with defaults
ki.set_bound_keys(_keybinds.values())


def _apply_sensitivity_mapping(steering, smoothing):
    """Map UI 0–100 values to tilt thresholds and debounce frames."""
    global _steering_ui, _smoothing_ui
    global _debounce_frames
    global _tilt_enter_left, _tilt_enter_right, _tilt_exit_left, _tilt_exit_right

    steering = max(0, min(100, int(steering)))
    smoothing = max(0, min(100, int(smoothing)))

    _steering_ui = steering
    _smoothing_ui = smoothing

    # Higher steering sensitivity → smaller tip needed (40px → 8px)
    enter_left = 40 - (32 * steering) / 100.0
    # Keep historical left/right asymmetry (~20 vs 25)
    enter_right_mag = enter_left * 1.25

    _tilt_enter_left = enter_left
    _tilt_enter_right = -enter_right_mag
    _tilt_exit_left = enter_left * 0.5
    _tilt_exit_right = -enter_right_mag * 0.5

    # Higher smoothing → more debounce frames (1–8); 40 → 3
    _debounce_frames = max(1, min(8, 1 + (smoothing * 7) // 100))


def get_sensitivity():
    """Return current UI sensitivity values and derived debounce frames."""
    return {
        "steering": _steering_ui,
        "smoothing": _smoothing_ui,
        "debounce_frames": _debounce_frames,
    }


def set_sensitivity(steering, smoothing):
    """Update sensitivity live. Resets debounce when smoothing changes."""
    global _smoothing_ui
    prev_smoothing = _smoothing_ui
    _apply_sensitivity_mapping(steering, smoothing)
    if _smoothing_ui != prev_smoothing:
        _reset_debounce()


# Initialize derived thresholds from defaults
_apply_sensitivity_mapping(_steering_ui, _smoothing_ui)


def _capture_backend():
    # DirectShow is more reliable for open/probe on Windows multi-cam setups
    if sys.platform == "win32":
        return cv2.CAP_DSHOW
    return cv2.CAP_ANY


def _windows_camera_names():
    """
    Best-effort friendly names via Windows PnP (Camera class).
    Order often matches DirectShow / OpenCV CAP_DSHOW indices, but is not guaranteed.
    """
    if sys.platform != "win32":
        return []
    try:
        import subprocess

        completed = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Get-PnpDevice -Class Camera -Status OK -ErrorAction SilentlyContinue "
                "| Select-Object -ExpandProperty FriendlyName",
            ],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
        names = []
        for line in (completed.stdout or "").splitlines():
            name = line.strip()
            if name:
                names.append(name)
        return names
    except (OSError, subprocess.SubprocessError, subprocess.TimeoutExpired):
        return []


def list_cameras(max_check=_MAX_CAMERA_PROBE):
    """
    Probe camera indices and return [{"index": int, "name": str}, ...].
    On Windows, prefers PnP friendly names when available.
    """
    found = []
    backend = _capture_backend()
    for i in range(max_check):
        cap_probe = cv2.VideoCapture(i, backend)
        try:
            if not cap_probe.isOpened():
                continue
            ok, _frame = cap_probe.read()
            if ok:
                found.append({"index": i, "name": f"Camera {i}"})
        finally:
            cap_probe.release()

    friendly = _windows_camera_names()
    if friendly and found:
        for offset, cam in enumerate(found):
            if offset < len(friendly):
                cam["name"] = f"{friendly[offset]} ({cam['index']})"
            else:
                cam["name"] = f"Camera {cam['index']}"
    return found


def get_camera_index():
    return _camera_index


def set_camera_index(index):
    """Set preferred camera index (applied on next start_camera)."""
    global _camera_index
    try:
        _camera_index = max(0, int(index))
    except (TypeError, ValueError):
        _camera_index = CAMERA_INDEX


def start_camera(camera_index=None):
    """Open the webcam for the steering loop. Returns True on success."""
    global cap, detector, _window_ready, _camera_index

    if camera_index is not None:
        set_camera_index(camera_index)

    if cap is not None and cap.isOpened():
        return True

    stop_camera()

    new_cap = cv2.VideoCapture(_camera_index, _capture_backend())
    if not new_cap.isOpened():
        new_cap.release()
        return False

    new_cap.set(3, wCam)
    new_cap.set(4, hCam)
    cap = new_cap

    if detector is None:
        detector = htm.handDetector(detectionCon=0.9)

    _reset_debounce()
    _window_ready = False
    return True


def stop_camera():
    """Release keys, close the preview, and free the webcam."""
    global cap, _window_ready

    _clear_input()
    if cap is not None:
        cap.release()
        cap = None
    cv2.destroyAllWindows()
    _window_ready = False


def cleanup():
    stop_camera()


def _reset_debounce():
    global _pending_keys, _pending_count, _active_keys, _active_steer
    _pending_keys = ()
    _pending_count = 0
    _active_keys = ()
    _active_steer = None


def _clear_input():
    """Release all simulated keys and reset debounce state."""
    ki.release_all()
    _reset_debounce()


def _show_frame(img):
    global _window_ready
    winname = "Image"
    if not _window_ready:
        cv2.namedWindow(winname)
        cv2.moveWindow(winname, 50, 10)
        _window_ready = True
    cv2.imshow(winname, img)
    cv2.waitKey(1)


def _apply_keys(keys):
    """Press/release currently bound physical keys to match the desired set."""
    desired = set(keys)
    for key in _keybinds.values():
        if key in desired:
            ki.press_key(key)
        else:
            ki.release_key(key)


def _commit_keys(keys):
    """Debounce: apply a new key set only after N consistent frames."""
    global _pending_keys, _pending_count, _active_keys

    normalized = tuple(sorted(keys))
    if normalized == _active_keys:
        _pending_keys = normalized
        _pending_count = 0
        _apply_keys(_active_keys)
        return

    if normalized == _pending_keys:
        _pending_count += 1
    else:
        _pending_keys = normalized
        _pending_count = 1

    if _pending_count >= _debounce_frames:
        _active_keys = normalized
        _pending_count = 0

    _apply_keys(_active_keys)


def _steer_from_tilt(tilt):
    """Map index–pinky height delta to left/right with hysteresis."""
    global _active_steer

    if _active_steer == "left":
        if tilt < _tilt_exit_left:
            _active_steer = None
    elif _active_steer == "right":
        if tilt > _tilt_exit_right:
            _active_steer = None

    if _active_steer is None:
        if tilt > _tilt_enter_left:
            _active_steer = "left"
        elif tilt < _tilt_enter_right:
            _active_steer = "right"

    return _active_steer


def _keys_for_gesture(drive, steer):
    keys = []
    if drive == "accelerate":
        keys.append(_keybinds["accelerate"])
    elif drive == "brake":
        keys.append(_keybinds["brake"])
    if steer == "left":
        keys.append(_keybinds["left"])
    elif steer == "right":
        keys.append(_keybinds["right"])
    return keys


def _detect_handedness(lm_list):
    """
    Infer left/right from landmark layout in the mirrored webcam view.
    Right: index base left of pinky base; Left: the opposite.
    """
    index_base_x = lm_list[5][1]
    pinky_base_x = lm_list[17][1]
    if index_base_x < pinky_base_x:
        return "right"
    if index_base_x > pinky_base_x:
        return "left"
    return None


def _classify_gesture(lm_list):
    """
    Return (hand, drive, tilt) for a usable hand, or None if rejected.
    drive: 'accelerate' | 'brake' | 'neutral'
    """
    hand = _detect_handedness(lm_list)
    if hand is None:
        return None
    if _hand_preference != "either" and hand != _hand_preference:
        return None

    thumb_tip_x = lm_list[4][1]
    index_base_x, index_base_y = lm_list[5][1], lm_list[5][2]
    mid_base_y = lm_list[9][2]
    mid_tip_y = lm_list[12][2]
    pinky_base_y = lm_list[17][2]

    # Thumb-out is mirrored for left vs right in the flipped webcam frame
    if hand == "right":
        thumb_out = index_base_x < thumb_tip_x
    else:
        thumb_out = index_base_x > thumb_tip_x

    mid_extended = mid_base_y < mid_tip_y

    if thumb_out:
        drive = "brake"
    elif mid_extended:
        drive = "accelerate"
    else:
        drive = "neutral"

    # Tilt sign is opposite for left vs right in the mirrored webcam frame.
    # Do not reuse one formula for both hands.
    if hand == "right":
        tilt = index_base_y - pinky_base_y
    else:
        tilt = pinky_base_y - index_base_y
    return hand, drive, tilt


def _rejected_hand_message():
    if _hand_preference == "right":
        return "Use right hand"
    if _hand_preference == "left":
        return "Use left hand"
    return "Show a hand"


def steering(fps):
    """
    Process one camera frame and update keyboard input.
    Returns True while the camera is healthy, False if it should stop
    (not started, disconnect, or read failure).
    """
    global cap

    if cap is None or not cap.isOpened():
        _clear_input()
        return False

    success, img = cap.read()
    if not success or img is None:
        _clear_input()
        return False

    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lm_list = detector.findPosition(img)
    img = cv2.flip(img, 1)
    cv2.putText(
        img,
        "FPS:" + str(int(fps)),
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )

    if len(lm_list) == 0:
        _clear_input()
        cv2.putText(
            img,
            "No hand",
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 165, 255),
            2,
        )
        _show_frame(img)
        return True

    classified = _classify_gesture(lm_list)
    if classified is None:
        _clear_input()
        cv2.putText(
            img,
            _rejected_hand_message(),
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 165, 255),
            2,
        )
        _show_frame(img)
        return True

    hand, drive, tilt = classified
    steer = _steer_from_tilt(tilt)
    keys = _keys_for_gesture(drive, steer)
    _commit_keys(keys)

    label = f"{drive} ({hand[0].upper()})"
    if steer:
        label = f"{drive} + {steer} ({hand[0].upper()})"
    cv2.putText(
        img,
        label,
        (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2,
    )
    _show_frame(img)
    return True
