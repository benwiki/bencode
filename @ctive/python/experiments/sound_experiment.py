#!/usr/bin/env python3
"""
Play a file continously, and exit gracefully on signal

Based on https://github.com/steveway/papagayo-ng/blob/working_vol/SoundPlayer.py

@author Guy Sheffer (GuySoft) <guysoft at gmail dot com>
"""
import math
import os
import signal
import threading
import time
from colorsys import hsv_to_rgb

import pyaudio
import pygame
from pydub import AudioSegment
from pydub.utils import make_chunks

pygame.init()

# RATE = 44100
# WIDTH = int((1/30) * RATE)
# HEIGHT = 600

# fullscreen
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
# WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
print(WIDTH, HEIGHT)

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

  def play(self) :
    """
    Just another name for self.start()
    """
    self.start()

  def stop(self) :
    """
    Stop playback. 
    """
    self.loop = False
    
    
class PlayerLoop(threading.Thread) :
  """
  A simple class based on PyAudio and pydub to play in a loop in the backgound
  """

  def __init__(self,filepath,loop=True) :
    """
    Initialize `PlayerLoop` class.

    PARAM:
        -- filepath (String) : File Path to wave file.
        -- loop (boolean)    : True if you want loop playback. 
                               False otherwise.
    """
    super(PlayerLoop, self).__init__()
    self.filepath = os.path.abspath(filepath)
    self.loop = loop

  def run(self):
    # Open an audio segment
    sound = AudioSegment.from_file(self.filepath)
    player = pyaudio.PyAudio()
    
    stream = player.open(format = player.get_format_from_width(sound.sample_width),
        channels = sound.channels,
        rate = sound.frame_rate,
        output = True)

    # PLAYBACK LOOP
    start = 0
    length = sound.duration_seconds
    volume = 100.0
    playchunk = sound[start*1000.0:(start+length)*1000.0] - (60 - (60 * (volume/100.0)))
    millisecondchunk = 50 / 1000.0
    
    while self.loop :
        self.time = start
        chunks = make_chunks(playchunk, millisecondchunk*1000)
        red_change = 1
        red_shade = 0
        yellow_shade = 0
        white_shade = 0
        for i, chunks in enumerate(chunks):
            screen.fill((0,0,0))
            self.time += millisecondchunk
            data = chunks._data
            stream.write(data)
            len_data = len(data)
            ratio = WIDTH / HEIGHT
            constant = HEIGHT * WIDTH / len_data
            w = math.sqrt(constant * ratio)  # ; h = math.sqrt(constant / ratio)
            unit = int(WIDTH / w)
            score = 0
            for i, v in enumerate(data):
                # r, g, b = map(lambda x: int(x * 255), hsv_to_rgb(v/1000, 1, 1))
                # # print(v, r, g, b)
                # color = (r, g, b)
                v2 = int(math.pow(v/255, 8) * 255)
                score += v2
                color = (max(red_shade, white_shade, v2), max(int(yellow_shade), white_shade, v2), max(white_shade, v2))

                # pygame.draw.circle(screen, color, ((i * constant) // CHUNK, (i * constant) % CHUNK), 5)
                # pygame.draw.circle(screen, color, ((i * constant) // SCREEN_HEIGHT, (i * constant) % SCREEN_HEIGHT), 5)
                j = i + 0.5
                # pygame.draw.circle(screen, color, ((i * w) % WIDTH, ((i * w) // WIDTH) * h), base/2)
                # pygame.draw.circle(screen, color, ((j * WIDTH / unit) % WIDTH, ((j * WIDTH / unit) // WIDTH) * HEIGHT / unit), base/2)
                pygame.draw.rect(screen, color, pygame.Rect(
                    (j * WIDTH / unit) % WIDTH,
                    ((j * WIDTH / unit) // WIDTH) * HEIGHT / unit,
                    WIDTH / unit + 1,
                    HEIGHT / unit + 1
                ))
            if score > 290000:  #len_data * 255 * red_rate:
                red_shade = min(255, red_shade + red_change)
            else:
                red_shade = max(0, red_shade - red_change)
            if score < 249000 and red_shade > 160:
                yellow_shade = min(255, yellow_shade + 20)
            else:
                yellow_shade = max(0, yellow_shade - 0.3)
            if score > 370000:
                white_shade = 200
                red_shade = max(0, red_shade - 20)
            else:
                white_shade = max(0, white_shade - 25)
            # print(score, red_shade, yellow_shade, white_shade)
            if not self.loop:
                break
            if self.time >= start+length:
                break
            pygame.display.flip()

    stream.close()
    player.terminate()


  def play(self) :
    """
    Just another name for self.start()
    """
    self.start()

  def stop(self) :
    """
    Stop playback. 
    """
    self.loop = False
    
    
def play_audio_background(audio_file):
    """
    Play audio file in the background, accept a SIGINT or SIGTERM to stop
    """
    killer = GracefulKiller()
    player = PlayerLoop(audio_file)
    player.play()
    print(os.getpid())
    while True:      
        time.sleep(0.5)
        # print("doing something in a loop ...")
        if killer.kill_now:
            break
    player.stop()
    print("End of the program. I was killed gracefully :)")
    return
        


if __name__ == '__main__':
    # import argparse
    # parser = argparse.ArgumentParser(add_help=True, description="Play a file continously, and exit gracefully on signal")
    # parser.add_argument('audio_file', type=str, help='The Path to the audio file (mp3, wav and more supported)')
    # args = parser.parse_args()
    
    play_audio_background("music.mp3")
    
