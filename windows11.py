#!/usr/bin/python3

# New from Microsoft - Windows 11
# Keylogging functionality based off https://github.com/boppreh/keyboard
# and https://github.com/ajinabraham/Xenotix-Python-Keylogger

import keyboard
import pyttsx
import threading
import re
from tendo import singleton

me = singleton.SingleInstance() # Make sure only one instance is run
tts = pyttsx.init()

tts_thread = threading.Thread(target=tts.startLoop)
tts_thread.start()

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
    tts.endLoop()
    tts_thread.join()
    say("Windows 11 has encountered an unexpected error and needs to close.")
    tts.runAndWait()


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
    say("Linux is a cancer that attaches itself in an intellectual property sense to everything it touches.")


def on_windows_bad():
    say("Please remember that microsoft loves you.")

def say(msg):
    global tts
    print(msg)
    tts.say(msg)


main()