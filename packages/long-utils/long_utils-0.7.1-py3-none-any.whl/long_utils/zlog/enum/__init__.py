import enum


class TextDisplayMethod(enum.IntEnum):
    default = 0
    highlight = 1
    underline = 4
    flicker = 5
    reverse_display = 7
    invisible = 8


class TextForeground(enum.IntEnum):
    black = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    purplish_red = 35
    turquoise_blue = 36
    white = 37


class TextBackground(enum.IntEnum):
    black = 40
    red = 41
    green = 42
    yellow = 43
    blue = 44
    purplish_red = 45
    turquoise_blue = 46
    white = 47
