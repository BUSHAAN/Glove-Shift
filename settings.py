import json
import os
import sys

DEFAULT_STEERING = 50
DEFAULT_SMOOTHING = 40


def settings_path():
    """settings.json next to the EXE when frozen, else project root."""
    if getattr(sys, "frozen", False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "settings.json")


def load_settings():
    path = settings_path()
    data = {"steering": DEFAULT_STEERING, "smoothing": DEFAULT_SMOOTHING}
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
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        pass
    return data


def save_settings(steering, smoothing):
    path = settings_path()
    payload = {
        "steering": _clamp_int(steering, 0, 100, DEFAULT_STEERING),
        "smoothing": _clamp_int(smoothing, 0, 100, DEFAULT_SMOOTHING),
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
            f.write("\n")
    except OSError:
        pass


def _clamp_int(value, lo, hi, default):
    try:
        return max(lo, min(hi, int(value)))
    except (TypeError, ValueError):
        return default
