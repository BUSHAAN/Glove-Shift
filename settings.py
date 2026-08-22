import json
import os
import sys

import KeyboardInput as ki

DEFAULT_STEERING = 50
DEFAULT_SMOOTHING = 40
DEFAULT_HAND = "either"
VALID_HANDS = ("either", "left", "right")
DEFAULT_KEYS = dict(ki.DEFAULT_BINDS)


def settings_path():
    """settings.json next to the EXE when frozen, else project root."""
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "settings.json")


def asset_path(*parts):
    """Resolve a bundled asset (dev tree or PyInstaller _MEIPASS)."""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)


def load_settings():
    path = settings_path()
    data = {
        "steering": DEFAULT_STEERING,
        "smoothing": DEFAULT_SMOOTHING,
        "hand": DEFAULT_HAND,
        "keys": dict(DEFAULT_KEYS),
    }
    if not os.path.isfile(path):
        return data
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        if isinstance(raw, dict):
            if "steering" in raw:
                data["steering"] = _clamp_int(raw["steering"], 0, 100, DEFAULT_STEERING)
            if "smoothing" in raw:
                data["smoothing"] = _clamp_int(raw["smoothing"], 0, 100, DEFAULT_SMOOTHING)
            if "hand" in raw:
                data["hand"] = _normalize_hand(raw["hand"])
            if "keys" in raw:
                data["keys"] = _normalize_keys(raw["keys"])
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        pass
    return data


def save_settings(steering, smoothing, hand=DEFAULT_HAND, keys=None):
    path = settings_path()
    payload = {
        "steering": _clamp_int(steering, 0, 100, DEFAULT_STEERING),
        "smoothing": _clamp_int(smoothing, 0, 100, DEFAULT_SMOOTHING),
        "hand": _normalize_hand(hand),
        "keys": _normalize_keys(keys if keys is not None else DEFAULT_KEYS),
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.write("\n")
    except OSError:
        pass


def _normalize_hand(value):
    if isinstance(value, str) and value.lower() in VALID_HANDS:
        return value.lower()
    return DEFAULT_HAND


def _normalize_keys(value):
    result = dict(DEFAULT_KEYS)
    if not isinstance(value, dict):
        return result
    for action in ("accelerate", "brake", "left", "right"):
        key = value.get(action)
        if isinstance(key, str) and key in ki.SCAN_CODES:
            result[action] = key
    return result


def _clamp_int(value, lo, hi, default):
    try:
        return max(lo, min(hi, int(value)))
    except (TypeError, ValueError):
        return default
