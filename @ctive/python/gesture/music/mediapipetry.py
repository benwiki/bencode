from math import hypot

import cv2
import mediapipe as mp
import numpy as np
import pygame as pg

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


# pg.mixer.init(frequency=44100, size=-16, channels=1)

# size = 44100

# # A function that generates a beautiful sound
# def f(x):
#     return (np.sin(x/((x%1000)+1)) + np.sin(x/((x%2000)+1)) + np.sin(x/((x%3000)+1)) + np.sin(x/((x%4000)+1)) + np.sin(x/((x%5000)+1)) + np.sin(x/((x%6000)+1)) + np.sin(x/((x%7000)+1)) + np.sin(x/((x%8000)+1)) + np.sin(x/((x%9000)+1)) + np.sin(x/((x%10000)+1)) + np.sin(x/((x%11000)+1)) + np.sin(x/((x%12000)+1)) + np.sin(x/((x%13000)+1)) + np.sin(x/((x%14000)+1)) + np.sin(x/((x%15000)+1)) + np.sin(x/((x%16000)+1)) + np.sin(x/((x%17000)+1)) + np.sin(x/((x%18000)+1)) + np.sin(x/((x%19000)+1)) + np.sin(x/((x%20000)+1)) + np.sin(x/((x%21000)+1)) + np.sin(x/((x%22000)+1)) + np.sin(x/((x%23000)+1)) + np.sin(x/((x%24000)+1)) + np.sin(x/((x%25000)+1)) + np.sin(x/((x%26000)+1)) + np.sin(x/((x%27000)+1)) + np.sin(x/((x%28000)+1)) + np.sin(x/((x%29000)+1)) + np.sin(x/((x%30000)+1)) + np.sin(x/((x%31000)+1)) + np.sin(x/((x%32000)+1)) + np.sin(x/((x%33000)+1)) + np.sin(x/((x%34000)+1)) + np.sin(x/((x%35000)+1)) + np.sin(x/((x%36000)+1)) + np.sin(x/((x%37000)+1)) + np.sin(x/((x%38000)+1)))

# # buffer = np.random.randint(-32768, 32767, size*3)
# buffer = np.array([f(x) for x in range(size)])
# buffer = np.repeat(buffer.reshape(size, 1), 2, axis = 1)

# sound = pg.sndarray.make_sound(buffer)

def create_complex_sound(freq, length, sample_rate=44100):
    t: np.ndarray = np.arange(length) / sample_rate  # Time array

    # Fundamental frequency sine wave
    buffer = np.zeros(t.shape)

    # Add harmonics
    harmonics = [-36, -24, -12, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Define the harmonics you want (these are the first four)
    harmonics_amplitude = [0, 2, 0.2, 0.8, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1]  # Define their relative amplitudes

    for h, amp in zip(harmonics, harmonics_amplitude):
        buffer += amp * np.sin(2 * np.pi * (freq * 2 ** (h / 12)) * t)

    # Ensure it's in range -1 to 1
    buffer /= np.max(np.abs(buffer))

    return buffer.astype(np.float32)


def create_beautiful_sound(freq, length, sample_rate=44100):
    t = np.linspace(0, length / sample_rate, num=length)

    # Fundamental frequency sine wave
    buffer = 0.5 * np.sin(2 * np.pi * freq * t)

    # Add a gentle vibrato
    vibrato_freq = 5  # Vibrato frequency in Hz
    vibrato_magnitude = 10  # Vibrato magnitude in Hz
    buffer *= np.sin(2 * np.pi * vibrato_freq * t) * vibrato_magnitude + 1

    # Add a touch of randomness
    buffer += 0.02 * np.random.randn(length)

    # Envelope (Attack, Decay, Sustain, Release)
    attack_length = int(sample_rate * 0.01)  # 0.01 seconds
    decay_length = int(sample_rate * 0.2)    # 0.2 seconds
    sustain_level = 0.7  # Sustain level (0-1)
    release_length = int(sample_rate * 0.3)  # 0.3 seconds

    envelope = np.concatenate([
        np.linspace(0, 1, attack_length),  # Attack
        np.linspace(1, sustain_level, decay_length),  # Decay
        sustain_level * np.ones(length - attack_length - decay_length - release_length),  # Sustain
        np.linspace(sustain_level, 0, release_length)  # Release
    ])

    # Apply envelope
    buffer *= envelope

    # Normalize the sound
    buffer /= np.max(np.abs(buffer))

    return buffer.astype(np.float32)

def create_growl(freq, length, sample_rate=44100):
    t = np.linspace(0, length / sample_rate, num=length)
    
    # Start with a basic waveform - a square wave can be good for growls
    waveform = np.sign(np.sin(2 * np.pi * freq * t))

    # Add harmonics to the square wave to make it richer
    # This is a simple form of distortion/saturation
    for harmonic in range(2, 5):
        waveform += (1.0 / harmonic) * np.sign(np.sin(2 * np.pi * (freq * harmonic) * t))
    
    # Modulate the waveform with a low-frequency oscillator to get that "wobble"
    lfo_rate = 30  # LFO rate in Hz
    lfo_magnitude = 0.5
    lfo = lfo_magnitude * np.sin(2 * np.pi * lfo_rate * t)

    # Apply LFO to frequency modulation
    modulated_waveform = np.sign(np.sin(2 * np.pi * (freq + freq * lfo) * t))

    # Apply a filter sweep (a simple form of it)
    # In actual sound design, this would be a resonant filter sweep like a bandpass
    filter_sweep = np.linspace(0.1, 0.5, num=length)
    growl = modulated_waveform * filter_sweep

    # Envelope (Attack, Decay, Sustain, Release) - quick attack, long sustain, quick release
    attack_length = int(sample_rate * 0.01)
    decay_length = int(sample_rate * 0.1)
    sustain_level = 0.8
    release_length = int(sample_rate * 0.1)
    envelope = np.concatenate([
        np.linspace(0, 1, attack_length),
        np.linspace(1, sustain_level, decay_length),
        sustain_level * np.ones(length - attack_length - decay_length - release_length),
        np.linspace(sustain_level, 0, release_length)
    ])

    # Apply envelope
    growl *= envelope

    # Normalize the sound
    growl /= np.max(np.abs(growl))

    return growl.astype(np.float32)

# pg.mixer.init(size=32)
pg.mixer.init(44100, 32, 1, 1024)

# buffer = create_complex_sound(110, 44100*10)
# sound = pg.mixer.Sound(buffer)
# sound.play()

# while True:
#     # Wait for sound to finish playing
#     pg.time.wait(int(sound.get_length() * 1000))
#     # Play again
#     sound.play()

def get_sound(freq: float):
    buffer = np.sin(2 * np.pi * np.arange(44100*4) * freq / 44100).astype(np.float32)
    return pg.mixer.Sound(buffer)

def play_sounds(sounds: list[pg.mixer.Sound]):
    for sound in sounds:
        sound.play()

def stop_sounds(sounds: list[pg.mixer.Sound]):
    for sound in sounds:
        sound.fadeout(100)

note_order = {
    'C': 0,
    'C#': 1,
    'D': 2,
    'D#': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'G': 7,
    'G#': 8,
    'A': 9,
    'A#': 10,
    'B': 11
}

def note_to_freq(note: str):
    """Converts a note in the format <base>-<octave> to a frequency in Hz"""
    noteparts = note.split('-')
    if len(noteparts) != 2:
        raise ValueError('Note must be in format <base>-<octave>, e.g. C#-4')
    base = noteparts[0]
    octave = int(noteparts[1])
    return 261.63 * 2 ** ((note_order[base]) / 12 + (octave - 5))

def chord_to_freqs(chord: str):
    """Converts a chord in the format <note>/<note>/... to a list of frequencies in Hz"""
    notes = chord.split(' ')
    return [note_to_freq(note) for note in notes]

def get_chord(chord: str):
    """Converts a chord in the format <note>/<note>/... to a list of pygame sounds"""
    return [get_sound(freq) for freq in chord_to_freqs(chord)]


chords = [
    get_chord('C-4 E-4 B-4 D-5 E-5 G-5'),
    get_chord('A-4'),
    get_chord('C-5'),
    get_chord('E-5'),
    # get_chord('C-3 A-4 C-5 E-5'),
    get_chord('G-3 F-4 A-4 B-4 D-4 G-5'),
]

def set_chord(n: int | None):
    # if n:
    #     sound.play()
    # return
    for i, chord in enumerate(chords):
        if i == n:
            play_sounds(chord)
        else:
            stop_sounds(chord)

left1 = mp_drawing.DrawingSpec(color=(255,0,0), thickness=2, circle_radius=2)
left2 = mp_drawing.DrawingSpec(color=(0,0,200), thickness=2, circle_radius=2)
right1 = mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
right2 = mp_drawing.DrawingSpec(color=(0,200,0), thickness=2, circle_radius=2)

cap = cv2.VideoCapture(0)

sound_playing = 0
# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)
        
        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
        
        # Recolor image back to BGR for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Draw face landmarks
        # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.HAND_CONNECTIONS)
        
        # # Right hand
        # mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
        #                           left1, left2)
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                  right1, right2)
        # Left Hand
        if results.right_hand_landmarks:
            # sound.play()
            # continue
            x = results.right_hand_landmarks.landmark[8].x
            y = results.right_hand_landmarks.landmark[8].y
            if hypot(x - 0.5, y - 0.5) < 0.1:
                sound_playing = 4
                set_chord(4)
            elif y > 0.5 and x > 0.5:
                sound_playing = 0
                set_chord(0)
            elif y > 0.5 and x < 0.5 and sound_playing != 1:
                sound_playing = 1
                set_chord(1)
            elif y < 0.5 and x < 0.5 and sound_playing != 2:
                sound_playing = 2
                set_chord(2)
            elif y < 0.5 and x > 0.5 and sound_playing != 3:
                sound_playing = 3
                set_chord(3)
        else:
            # continue
            sound_playing = None
            set_chord(None)
        # Pose Detections
        # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                        
        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

