import ctypes

# Logical action → default physical key
DEFAULT_BINDS = {
    "accelerate": "w",
    "brake": "s",
    "left": "a",
    "right": "d",
}

# Physical key id → USB HID scan code (Set 1)
SCAN_CODES = {
    "w": 0x11,
    "a": 0x1E,
    "s": 0x1F,
    "d": 0x20,
    "i": 0x17,
    "j": 0x24,
    "k": 0x25,
    "l": 0x26,
    "q": 0x10,
    "e": 0x12,
    "z": 0x2C,
    "x": 0x2D,
    "c": 0x2E,
    "space": 0x39,
    "shift": 0x2A,
    "ctrl": 0x1D,
    "up": 0x48,
    "down": 0x50,
    "left_arrow": 0x4B,
    "right_arrow": 0x4D,
}

EXTENDED_KEYS = frozenset({"up", "down", "left_arrow", "right_arrow"})

# UI labels for the remapping combos
KEY_CHOICES = [
    ("W", "w"),
    ("A", "a"),
    ("S", "s"),
    ("D", "d"),
    ("I", "i"),
    ("J", "j"),
    ("K", "k"),
    ("L", "l"),
    ("Q", "q"),
    ("E", "e"),
    ("Z", "z"),
    ("X", "x"),
    ("C", "c"),
    ("Space", "space"),
    ("Shift", "shift"),
    ("Ctrl", "ctrl"),
    ("↑ Arrow", "up"),
    ("↓ Arrow", "down"),
    ("← Arrow", "left_arrow"),
    ("→ Arrow", "right_arrow"),
]

PUL = ctypes.POINTER(ctypes.c_ulong)

# Currently bound physical keys (values of the action map)
_bound_keys = list(DEFAULT_BINDS.values())


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


def set_bound_keys(physical_keys):
    """Tell release_all which physical keys may currently be held."""
    global _bound_keys
    _bound_keys = list(dict.fromkeys(physical_keys))


def _flags(key, releasing=False):
    flags = 0x0008  # KEYEVENTF_SCANCODE
    if key in EXTENDED_KEYS:
        flags |= 0x0001  # KEYEVENTF_EXTENDEDKEY
    if releasing:
        flags |= 0x0002  # KEYEVENTF_KEYUP
    return flags


def press_key(key):
    if key not in SCAN_CODES:
        return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, SCAN_CODES[key], _flags(key), 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(key):
    if key not in SCAN_CODES:
        return
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, SCAN_CODES[key], _flags(key, releasing=True), 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_all():
    for key in _bound_keys:
        release_key(key)
