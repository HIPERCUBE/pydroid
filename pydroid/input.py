import _adb

KEY_HOME = "KEYCODE_HOME"
KEY_BACK = "KEYCODE_BACK"
KEY_MENU = "KEYCODE_MENU"


def tap(x, y):
    _adb.shell("input tap " + x + " " + y)
    pass


def swipe(x1, y1, x2, y2, duration=None):
    command = "input swipe " + x1 + " " + y1 + " " + x2 + " " + y2
    if duration:
        command += " " + str(duration)
    _adb.shell(command)


def text(txt):
    _adb.shell("input keyevent " + txt)
    pass


def key_event(key):
    _adb.shell("input keyevent " + key)
    pass
