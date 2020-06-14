#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By Lexx Xell 2019

import time
import ctypes
from sys import argv

key_code = 0x0
key_presses_amount = 0

data_is_correct = False


# =========== БЛОК ИМИТАЦИИ НАЖАТИЯ КЛАВИШ ==============

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def KeyDown(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def KeyUp(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def press(key):
    KeyDown(key)
    time.sleep(0.5)
    KeyUp(key)
    time.sleep(0.5)

# =======================================================

def mass_press(key, val = 5, delay = 0.5):
    for i in range(val):
        press(key)
        time.sleep(delay)



if __name__ == '__main__':
    try:
        key_code = int(argv[1], 0)
        key_presses_amount = int(argv[2], 0)
        data_is_correct = True
    except:
        print('PLUGIN_ERROR: Transferred data is not correct!')
        print(argv)

    if data_is_correct == True:
        print(
    f'''
       ***   Event to key   ***
       Key code: {hex(key_code)}
       Key presses amount: {key_presses_amount}
    '''
        )
        mass_press(key_code, key_presses_amount)
