from time import sleep

import pyautogui

# import tkinter as tk
# win = tk.Tk()
# win.title("Mouse Position")
# win.geometry("300x100")
# label = tk.Label(win, text="Mouse Position")
# label.pack()
# while True:
#     x, y = pyautogui.position()
#     label.config(text=f"X: {x}, Y: {y}")
#     win.update()


screenWidth, screenHeight = (
    pyautogui.size()
)  # Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
currentMouseX, currentMouseY = (
    pyautogui.position()
)  # Returns two integers, the x and y of the mouse cursor's current position.
sleep(2)
time = 0.5
click = True
for i in range(202, 249):
    # pyautogui.moveTo(850, 120)  # Move the mouse to the x, y coordinates 100, 150.
    # pyautogui.click()
    # sleep(0.3)
    # pyautogui.moveTo(1050, 300)  # Move the mouse to the x, y coordinates 100, 150.
    # pyautogui.tripleClick()
    # sleep(0.1)
    # pyautogui.typewrite(f"channel-{i}-role")
    # sleep(0.3)
    # pyautogui.moveTo(360, 285)
    # pyautogui.moveTo(360, 335)
    # pyautogui.moveTo(360, 430)
    # pyautogui.moveTo(360, 480)
    pyautogui.moveTo(360, 570)
    if click: pyautogui.click()
    sleep(time)
    # Go to "Voice"
    pyautogui.moveTo(1200, 500)
    if click: pyautogui.click()
    # sleep(time)
    # Go to text field
    pyautogui.typewrite("\t")
    # pyautogui.moveTo(830, 610)
    # pyautogui.click()
    # sleep(time)
    pyautogui.typewrite(f"channel-{i}")
    sleep(time)
    # Go to "private channel"
    pyautogui.moveTo(1200, 680)
    if click: pyautogui.click()
    sleep(time)
    # Go to "next"
    pyautogui.moveTo(1170, 800)
    if click: pyautogui.click()
    sleep(time)
    pyautogui.typewrite(f"channel-{i}-role")
    sleep(time)
    # Go to the top role
    pyautogui.moveTo(705, 463)
    if click: pyautogui.click()
    sleep(time)
    # Go to "create channel"
    pyautogui.moveTo(1150, 830)
    if click: pyautogui.click()
    sleep(time*2)