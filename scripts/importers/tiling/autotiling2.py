r"""Tile Chrome windows in Windows 10.

For running correct pip:
C:\Users\hchall\Local Settings\Application Data\Programs\Python\Python37
\Scripts

Possible TODO: command shell with more modes, set max windows, etc.
"""

import pywinauto
from pywinauto import application
from win32api import GetSystemMetrics
from time import sleep
import keyboard
import win32gui

startapps = pywinauto.findwindows.find_elements(title_re=".*Dive")
managed_window_handles = [child.handle for child in startapps]
apps = []
for handle in managed_window_handles:
    try:
        apps.append(application.Application().connect(handle=handle))
    except Exception:
        pass

# Starts from 0,0 in top-left
screenx, screeny = (GetSystemMetrics(0), GetSystemMetrics(1))

max_windows = 6

#TO DO LIST:
# Need to figure out keyboard pausing



# Moves new windows in the following shapes:
all_positions = {


    0:  {
        "x": screenx * (1/4),
        "y": screeny * (0),
        "w": screenx * (1/4),
        "h": screeny * (1/2),
        },

    1:  {
        "x": screenx * (1/2),
        "y": screeny * (0),
        "w": screenx * (1/4),
        "h": screeny * (1/2),
        },

    2:  {
        "x": screenx * (3/4),
        "y": screeny * (0),
        "w": screenx * (1/4),
        "h": screeny * (1/2),
        },


    3:  {
        "x": screenx * (1/4),
        "y": screeny * (1/2),
        "w": screenx * (1/4),
        "h": screeny * (1/2),
        },

    4:  {
        "x": screenx * (1/2),
        "y": screeny * (1/2),
        "w": screenx * (1/4),
        "h": screeny * (1/2),
        },

    5:  {
        "x": screenx * (3/4),
        "y": screeny * (1/2),
        "w": screenx * (1/4),
        "h": screeny * (1/2),
        },
    }
# Dict of positions
keep_running = True
while keep_running:
    keyboard.start_recording()



    all_windows = pywinauto.findwindows.find_elements(title_re=".*Dive")
    for handle in list(set([spec.handle for spec in all_windows]) - set(managed_window_handles)):
        try:
            apps.append(application.Application().connect(handle=handle))
            managed_window_handles.append(handle)
        except Exception:
            pass

    #Cycle Take 2
    for i,app in enumerate(apps):
        if i<max_windows:
            apps[i].window(handle=managed_window_handles[i]).set_focus()
    sleep(5)

    for i,app in enumerate(apps):
        if i>=max_windows:
            apps[i],apps[i-max_windows]=(apps[i-max_windows],apps[i])
            managed_window_handles[i],managed_window_handles[i-max_windows]=(managed_window_handles[i-max_windows],managed_window_handles[i])


    # Tile windows correctly
    for i, (handle, app) in enumerate(zip(managed_window_handles, apps)):
        try:
            positions = all_positions 

            if(i > max_windows):
                i=i-max_windows

            xpos = int(positions[i]["x"])
            ypos = int(positions[i]["y"])
            width = int(positions[i]["w"])
            height = int(positions[i]["h"])

            app.window(handle=handle).move_window(
                x=xpos, y=ypos, width=width, height=height)
        except Exception:
            pass  # Window died after checking for dead windows


    # Check keyboard input
    keys_pressed = keyboard.stop_recording()
    actual_keys = [press.name for press in keys_pressed]
    print(keys_pressed)
    nums = [str(val) for val in list(range(0, 10))]
    max_set = False
    if ("ctrl" in actual_keys and "space" in actual_keys):
        print("activated key")
        while not max_set:
            keyboard.start_recording()
            sleep(0.2)
            keys_pressed = keyboard.stop_recording()
            actual_keys = [press.name for press in keys_pressed]
            for key in actual_keys:
                if key in nums:
                    max_windows = int(key) if int(key) > 0 else 10
                    max_set = True
                    break
                elif key == "esc":
                    keep_running = False
                    break
