# -*- coding: utf-8 -*-
from subprocess import Popen, PIPE, STDOUT


def shell(command):
    return Popen('adb shell ' + command, stdout=PIPE, stderr=STDOUT, shell=False)


def get_input_device(device):
    p = shell('getevent')
    last_device = None
    while True:
        line = p.stdout.readline().split()
        if line.__len__() < 2:
            continue

        if line[0] == 'add' and line[1] == 'device':
            last_device = line[3]
        if line[0] == 'name:' and line[1].replace('"', '') in device:
            return last_device


def get_input_device_touch():
    device_name = ['touch_dev', 'sec_touchscreen', 'synaptics_ts']
    return get_input_device(device_name)