# -*- coding: utf-8 -*-
import _adb
import threading

__event_listener = None


class EventListener(threading.Thread):
    def __init__(self, on_touch_start=None, on_touch=None, on_touch_end=None):
        super(EventListener, self).__init__()
        self.on_touch_start = on_touch_start
        self.on_touch = on_touch
        self.on_touch_end = on_touch_end
        self.process = None

    def run(self):
        self.process = _adb.shell('getevent -lt')

        touch_x = 0
        while True:
            line = self.process.stdout.readline().split()
            if line.__len__() < 5:
                continue

            if line[4] == 'BTN_TOUCH':
                if line[5] == 'DOWN' and self.on_touch_start is not None:
                    self.on_touch_start()
                if line[5] == 'UP' and self.on_touch_end is not None:
                    self.on_touch_end()
            if line[4] == 'ABS_MT_POSITION_X' and self.on_touch is not None:
                touch_x = int(line[5], 16)
            if line[4] == 'ABS_MT_POSITION_Y' and self.on_touch is not None:
                touch_y = int(line[5], 16)
                self.on_touch(touch_x, touch_y)

            if not line:
                break

    def __del__(self):
        self.process.kill()


def start_listener(on_touch_start=None, on_touch=None, on_touch_end=None, background=True):
    global __event_listener
    __event_listener = EventListener(on_touch_start, on_touch, on_touch_end)

    if background:
        __event_listener.start()
    else:
        __event_listener.run()


def stop_listener():
    global __event_listener
    __event_listener.__del__()


def listen_on_click(on_click):
    last_touch = {'x': 0, 'y': 0}
    is_stop = {'value': False}

    def on_touch(x, y):
        last_touch['x'] = x
        last_touch['y'] = y

    def stop():
        stop_listener()
        on_click(last_touch['x'], last_touch['y'])
        is_stop['value'] = True

    start_listener(on_touch=on_touch,
                   on_touch_end=stop,
                   background=True)

    while True:
        if is_stop['value']:
            return


def touch(x, y):
    _adb.shell('input tap ' + str(x) + ' ' + str(y))
    pass


def drag(start_x, start_y, end_x, end_y):
    _adb.shell('input swipe ' + str(start_x) + ' ' + str(start_y) + ' ' + str(end_x) + ' ' + str(end_y))
    pass


def pinch_zoom(focus_x, focus_y, zoom_level, zoom_in=True):
    # TODO : Not working
    input_device = _adb.get_input_device_touch()
    zoom = zoom_level * 50

    _touch_start_end(input_device)
    for i in range(0, zoom / 10):
        if zoom_in:
            _touch(input_device, focus_x + 100 + i * 10, focus_y + 100 + i * 10)
            _touch(input_device, focus_x - 100 - i * 10, focus_y - 100 - i * 10)
        else:
            _touch(input_device, focus_x + zoom + 100 - i * 10, focus_y + zoom + 100 - i * 10)
            _touch(input_device, focus_x - zoom - 100 + i * 10, focus_y - zoom - 100 + i * 10)

    _touch_start_end(input_device)


def _touch_start_end(input_device):
    _adb.shell('sendevent ' + input_device + ': 0003 0039 000001ff')
    _adb.shell('sendevent ' + input_device + ': 0001 014a 00000001')
    _adb.shell('sendevent ' + input_device + ': 0001 0145 00000001')


def _touch(input_device, x, y):
    _adb.shell('sendevent ' + input_device + ': 0003 0035 ' + ('%08X' % x))
    _adb.shell('sendevent ' + input_device + ': 0003 0036 ' + ('%08X' % y))
