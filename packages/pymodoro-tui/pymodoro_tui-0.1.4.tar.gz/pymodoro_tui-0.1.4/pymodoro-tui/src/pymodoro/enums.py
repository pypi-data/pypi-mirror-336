from enum import Enum


class Phases(str, Enum):
    FOCUS = "FOCUS"
    BREAK = "BREAK"


class Themes(str, Enum):
    FOCUS = "focus"
    BREAK = "break"
