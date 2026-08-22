import cv2
import HandTrackingModule as htm
import KeyboardInput as ki

wCam, hCam = 384, 288
CAMERA_INDEX = 0
DEBOUNCE_FRAMES = 3
# Tilt hysteresis: enter turn past these, stay in turn until returning inside exit band
TILT_ENTER_LEFT = 20
TILT_ENTER_RIGHT = -25
TILT_EXIT_LEFT = 10
TILT_EXIT_RIGHT = -12

cap = None
detector = None
_window_ready = False

_pending_keys = ()
_pending_count = 0
_active_keys = ()
_active_steer = None  # "left" | "right" | None


def start_camera(camera_index=CAMERA_INDEX):
    """Open the webcam for the steering loop. Returns True on success."""
    global cap, detector, _window_ready

    if cap is not None and cap.isOpened():
        return True

    stop_camera()

    new_cap = cv2.VideoCapture(camera_index)
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
    """Press/release WASD to match the desired key set."""
    desired = set(keys)
    for key in ("w", "a", "s", "d"):
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

    if _pending_count >= DEBOUNCE_FRAMES:
        _active_keys = normalized
        _pending_count = 0

    _apply_keys(_active_keys)


def _steer_from_tilt(tilt):
    """Map index–pinky height delta to left/right with hysteresis."""
    global _active_steer

    if _active_steer == "left":
        if tilt < TILT_EXIT_LEFT:
            _active_steer = None
    elif _active_steer == "right":
        if tilt > TILT_EXIT_RIGHT:
            _active_steer = None

    if _active_steer is None:
        if tilt > TILT_ENTER_LEFT:
            _active_steer = "left"
        elif tilt < TILT_ENTER_RIGHT:
            _active_steer = "right"

    return _active_steer


def _keys_for_gesture(drive, steer):
    keys = []
    if drive == "accelerate":
        keys.append("w")
    elif drive == "brake":
        keys.append("s")
    if steer == "left":
        keys.append("a")
    elif steer == "right":
        keys.append("d")
    return keys


def _classify_gesture(lm_list):
    """
    Return (drive, steer_hint) for a right hand, or None if not a right hand.
    drive: 'accelerate' | 'brake' | 'neutral'
    """
    thumb_tip_x = lm_list[4][1]
    index_base_x, index_base_y = lm_list[5][1], lm_list[5][2]
    mid_base_y = lm_list[9][2]
    mid_tip_y = lm_list[12][2]
    pinky_base_x, pinky_base_y = lm_list[17][1], lm_list[17][2]

    # Right hand: index base left of pinky base (mirrored webcam view)
    if index_base_x >= pinky_base_x:
        return None

    thumb_out = index_base_x < thumb_tip_x
    mid_extended = mid_base_y < mid_tip_y

    if thumb_out:
        drive = "brake"
    elif mid_extended:
        drive = "accelerate"
    else:
        drive = "neutral"

    tilt = index_base_y - pinky_base_y
    return drive, tilt


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
            "Use right hand",
            (10, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 165, 255),
            2,
        )
        _show_frame(img)
        return True

    drive, tilt = classified
    steer = _steer_from_tilt(tilt)
    keys = _keys_for_gesture(drive, steer)
    _commit_keys(keys)

    label = drive
    if steer:
        label = f"{drive} + {steer}"
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
