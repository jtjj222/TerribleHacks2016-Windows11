#!/usr/bin/python3

# New from Microsoft - Windows 11
# Keylogging functionality based off https://github.com/boppreh/keyboard
# and https://github.com/ajinabraham/Xenotix-Python-Keylogger

import keyboard
from plyer import notification
import re

import sys
import traceback
from functools import wraps
from multiprocessing import Process, Queue

words = [
    (["linux", "ubuntu", "fedora", "open.source", "free.software", "richard.stallman"],
     lambda: on_linux()),
    (["windows.*sucks", "microsoft.*sucks", "fuck.microsoft", "microsoft.*bad"],
     lambda: on_windows_bad())
]

key_buffer = ""


def main():
    global words, tts
    print("Welcome to Windows 11!")

    for (wl, action) in words:
        for i, word in enumerate(wl):
            wl[i] = re.compile(word)

    keyboard.on_press(on_keypress)

    print("Microsoft Loves You!")

    keyboard.wait('')

    tts.stop()
    say("Windows 11 has encountered an unexpected error and needs to close.")


def on_keypress(evt):
    global key_buffer
    if len(evt.name) is 1:
        key_buffer += evt.name.lower()
    else:
        key_buffer += " "
        check_buffer()
    if len(key_buffer) > 50:
        key_buffer = key_buffer[1:]


def check_buffer():
    global words, key_buffer
    for (wl, action) in words:
        for word in wl:
            if word.search(key_buffer):
                action()
                key_buffer = ""


def on_linux():
    keyboard.press_and_release('ctrl+w')
    notify("Microsoft™ Advanced Business Model Threat Protection",
           "Microsoft has detected a threat and has cleaned your computer. Your credit card has been charged for this service.")


def on_windows_bad():
    for i in range(0,50): keyboard.press_and_release("backspace")
    notify("Microsoft™ Idea Piracy Protection Activated",
           "Microsoft™ Idea Piracy Protection has protected you from unlawfully using Microsoft's intellectual property")
    say("Please remember that microsoft loves you.")


def notify(title, msg):
    notification.notify(title=title, message=msg)


def _say_process(msg):
    import pyttsx
    tts = pyttsx.init()
    tts.setProperty('rate', 150)
    tts.say(msg)
    tts.runAndWait()

def say(msg):
    p = Process(target=_say_process, args=(msg,))
    p.start()
    p.join()


if __name__=="__main__":
    main()