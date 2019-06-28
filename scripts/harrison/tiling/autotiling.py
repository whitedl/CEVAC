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

startapps = pywinauto.findwindows.find_elements(title_re=".*Chrome")
managed_window_handles = [child.handle for child in startapps]
apps = []
for handle in managed_window_handles:
    try:
        apps.append(application.Application().connect(handle=handle))
    except Exception:
        pass

# Starts from 0,0 in top-left
screenx, screeny = (GetSystemMetrics(0), GetSystemMetrics(1))

max_windows = 10

# Moves new windows in the following shapes:
'''
***************
*     *       *
*  0  *   1   *
*     *       *
***************
'''
positions_a = {
    0: {
        "x": screenx * (0),
        "y": screeny * (0),
        "w": screenx * (1 / 2),
        "h": screeny * (1),
    },
    1: {
        "x": screenx * (1 / 2),
        "y": screeny * (0),
        "w": screenx * (1 / 2),
        "h": screeny * (1),
    },
}

'''
***************
*     *   1   *
*  0  *********
*     *   2   *
***************
'''
positions_b = {
    0: {
        "x": screenx * (0),
        "y": screeny * (0),
        "w": screenx * (1 / 2),
        "h": screeny * (1),
    },
    1: {
        "x": screenx * (1 / 2),
        "y": screeny * (0),
        "w": screenx * (1 / 2),
        "h": screeny * (1 / 2),
    },
    2: {
        "x": screenx * (1 / 2),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 2),
        "h": screeny * (1 / 2),
    },
}

'''
***************
*     * 1 * 2 *
*  0  *********
*     * 3 * 4 *
***************
'''
positions_c = {
    0: {
        "x": screenx * (0),
        "y": screeny * (0),
        "w": screenx * (1 / 2),
        "h": screeny * (1),
    },
    1: {
        "x": screenx * (1 / 2),
        "y": screeny * (0),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    2: {
        "x": screenx * (3 / 4),
        "y": screeny * (0),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    3: {
        "x": screenx * (1 / 2),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    4: {
        "x": screenx * (3 / 4),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
}

'''
***************
* 1 *  0  * 2 *
***************
* 3 * 5*6 * 7 *
***************
'''
positions_d = {
    0: {
        "x": screenx * (1 / 4),
        "y": screeny * (0),
        "w": screenx * (1 / 2),
        "h": screeny * (1 / 2),
    },
    1: {
        "x": screenx * (0),
        "y": screeny * (0),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    2: {
        "x": screenx * (3 / 4),
        "y": screeny * (0),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    3: {
        "x": screenx * (0),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    4: {
        "x": screenx * (1 / 4),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    5: {
        "x": screenx * (2 / 4),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    6: {
        "x": screenx * (3 / 4),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
}

'''
***************
* 1 *  0  * 2 *
***************
*3*4*5*6*7*8*9*
***************
'''
positions_e = {
    0: {
        "x": screenx * (1 / 4),
        "y": screeny * (0),
        "w": screenx * (1 / 2),
        "h": screeny * (1 / 2),
    },
    1: {
        "x": screenx * (0),
        "y": screeny * (0),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    2: {
        "x": screenx * (3 / 4),
        "y": screeny * (0),
        "w": screenx * (1 / 4),
        "h": screeny * (1 / 2),
    },
    3: {
        "x": screenx * (0),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 7),
        "h": screeny * (1 / 2),
    },
    4: {
        "x": screenx * (1 / 7),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 7),
        "h": screeny * (1 / 2),
    },
    5: {
        "x": screenx * (2 / 7),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 7),
        "h": screeny * (1 / 2),
    },
    6: {
        "x": screenx * (3 / 7),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 7),
        "h": screeny * (1 / 2),
    },
    7: {
        "x": screenx * (4 / 7),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 7),
        "h": screeny * (1 / 2),
    },
    8: {
        "x": screenx * (5 / 7),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 7),
        "h": screeny * (1 / 2),
    },
    9: {
        "x": screenx * (6 / 7),
        "y": screeny * (1 / 2),
        "w": screenx * (1 / 7),
        "h": screeny * (1 / 2),
    },
}

# Dict of positions
all_positions = {
    0: positions_a,
    1: positions_a,
    2: positions_a,
    3: positions_b,
    4: positions_c,
    5: positions_c,
    6: positions_d,
    7: positions_d,
    8: positions_e,
    9: positions_e,
    10: positions_e,
}

keep_running = True
while keep_running:
    keyboard.start_recording()

    all_windows = pywinauto.findwindows.find_elements(title_re=".*Chrome")
    for handle in list(set([spec.handle for spec in all_windows]) - set(managed_window_handles)):
        try:
            apps.append(application.Application().connect(handle=handle))
            managed_window_handles.append(handle)
        except Exception:
            pass

    # Remove old/gone Windows
    while len(apps) > max_windows:
        apps[1].window(handle=managed_window_handles[1]).close()
        apps.remove(apps[1])
        managed_window_handles.remove(managed_window_handles[1])

    for i, handle in enumerate(managed_window_handles):
        if handle not in [spec.handle for spec in pywinauto.findwindows.find_elements(title_re=".*Chrome")]:
            apps.remove(apps[i])
            managed_window_handles.remove(managed_window_handles[i])

    # Tile windows correctly
    for i, (handle, app) in enumerate(zip(managed_window_handles, apps)):
        try:
            positions = all_positions[len(apps)]

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
