# import necessary packages

import os

import cv2
import mediapipe as mp
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from tensorflow.keras.models import load_model

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model
model = load_model('mp_hand_gesture')

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)

import time

state = {}

# Global variables to manage program state and confirmation
program_state = {
    "current_line": "",
    "command_buffer": None,
    "last_gesture": "",
    "confirmation_start": None,
    "confirmed": False,
}

# Mapping gestures to programming constructs
gesture_commands = {
    "okay": lambda: start_or_end_statement(),
    "peace": lambda: function_declaration_or_call(),
    "thumbs up": lambda: modify_numeric_value(1),
    "thumbs down": lambda: modify_numeric_value(-1),
    "call me": lambda: variable_declaration_or_call(),
    "stop": lambda: end_loop_or_function(),
    "rock": lambda: conditional_statement(),
    "live long": lambda: loop_construct(),
    "fist": lambda: logical_operation(),
}

# Time required to hold the confirmation gesture (in seconds)
CONFIRMATION_TIME = 2

def start_or_end_statement():
    if program_state["current_line"]:
        # print(f"Executing line: {program_state['current_line']}")
        execute_line(program_state["current_line"])
        program_state["current_line"] = ""
    else:
        program_state["current_line"] = "Start Statement: "

def function_declaration_or_call():
    if "Start Statement" in program_state["current_line"]:
        program_state["current_line"] += "|def"
    else:
        program_state["current_line"] += "|call"

def modify_numeric_value(change):
    program_state["current_line"] += f"|{change:+}"

def variable_declaration_or_call():
    if "Start Statement" in program_state["current_line"]:
        program_state["current_line"] += "|let"
    else:
        program_state["current_line"] += "|var"

def end_loop_or_function():
    program_state["current_line"] += "|end"

def conditional_statement():
    program_state["current_line"] += "|if"

def loop_construct():
    program_state["current_line"] += "|loop"

def logical_operation():
    program_state["current_line"] += "|and"


def main(gesture: str):
    confirm_gesture(gesture)

    if gesture != program_state["last_gesture"]:
        program_state["last_gesture"] = gesture
        if gesture in gesture_commands:
            program_state["command_buffer"] = gesture_commands[gesture]
    
    execute_buffered_command()

def confirm_gesture(gesture):
    if gesture == "smile":
        if not program_state["confirmation_start"]:
            program_state["confirmation_start"] = time.time()
        elif time.time() - program_state["confirmation_start"] > CONFIRMATION_TIME:
            program_state["confirmed"] = True
    else:
        program_state["confirmation_start"] = None
        program_state["confirmed"] = False

def execute_buffered_command():
    global state
    if state != program_state:
        print(program_state)
        state = program_state.copy()
    if program_state["command_buffer"] and program_state["confirmed"]:
        program_state["command_buffer"]()
        program_state["command_buffer"] = None
        program_state["confirmed"] = False

def execute_line(line):
    print("Executing line:", line)
    pieces = line.split("|")
    for piece in pieces:
        match piece:
            case "def":
                print("Defining function")
            case "call":
                print("Calling function")
            case "let":
                print("Declaring variable")
            case "var":
                print("Calling variable")
            case "end":
                print("Ending loop/function")
            case "if":
                print("Conditional statement")
            case "loop":
                print("Looping")
            case "and":
                print("Logical operation")
            case _ if piece.startswith("+") or piece.startswith("-"):
                print("Modifying numeric value by", piece)
            case _:
                print("Unknown command:", piece)


# The rest of your code remains the samw


# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # print('\033[F'+' '*70, end='')

    # Read each frame from the webcam
    _, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)
    
    className = ''

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])
            # print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]

    # show the prediction on the frame
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow("Output", frame) 

    if cv2.waitKey(1) == ord('q'):
        break

    main(className)

# release the webcam and destroy all active windows
cap.release()

cv2.destroyAllWindows()