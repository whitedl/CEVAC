# Emergency Response Dashboard Tiling
## `autotiling.py`
Used to tile chrome windows on the emergency response dashboard. The python3 script
relies on the `pywinauto`, `win32api`, and `keyboard` libraries.
### Tiling
The program will tile windows as follows for varying window counts:
```
***************
*     *       *
*  0  *   1   *
*     *       *
***************

***************
*     *   1   *
*  0  *********
*     *   2   *
***************

***************
*     * 1 * 2 *
*  0  *********
*     * 3 * 4 *
***************

***************
* 1 *  0  * 2 *
***************
* 3 * 5*6 * 7 *
***************

***************
* 1 *  0  * 2 *
***************
*3*4*5*6*7*8*9*
***************
```
### Control
When `ctrl+space` is pressed, the script waits for the next number which
determines the maximum number of windows allowed on screen (1-9,0 is 10)

## `emergency_repsonse_startup.bat`
Follow [This link](https://www.computerhope.com/issues/ch000322.htm) to set this
script for startup. This script will will need to be modified for file locations,
but will launch `autotiling.py` and google chrome in app-mode. 
