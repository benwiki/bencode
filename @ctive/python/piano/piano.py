
import os
import time
from threading import Thread

import pygame as pg
from pynput import keyboard

dir_path = os.path.dirname(os.path.realpath(__file__))
sound_path = '/sounds/'


def get_filenames(path: str) -> list[str]:
    return next(os.walk(path))[2]


def on_press(key):
    try:
        if key == keyboard.Key.esc:
            quit()
        elif key == keyboard.Key.backspace:
            key = '*'
        elif key == keyboard.Key.shift_r:
            key = '#'
        elif key == keyboard.Key.tab:
            key = '@'
        else:
            key = key.char
        print(key, mapping[key])
        threads[key] = Thread(target=play_notes, args=(
            dir_path + sound_path + f'{mapping[key]}.ogg', 0.0))
        threads[key].start()
        threads[key].join()
    except Exception:
        pass


pg.mixer.init()
pg.init()
pg.mixer.set_num_channels(len(get_filenames(dir_path+sound_path)))


def play_notes(notePath, duration):
    time.sleep(duration)  # make a pause
    pg.mixer.Sound(notePath).play()
    time.sleep(duration)  # Let the sound play
    print(notePath)  # To see which note is now playing


threads: dict[str, Thread] = {}

keylines = [line.strip().split(';')
            for line in open(f"{dir_path}/keys.txt", encoding='utf-8')]
mapping = {key: val for key, val in keylines}

with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()
