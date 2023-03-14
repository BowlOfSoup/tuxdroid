#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

# ------------------------------------------------------------------------------
# Refresh the task bar. Window.
# ------------------------------------------------------------------------------
def __refreshTaskBarWin32():
    """Refresh the task bar. Window.
    """
    import win32api
    import win32gui
    import win32con
    def FW(x, y):
        return win32gui.FindWindowEx(x, 0, y, "")
    # Get TaskBar handle
    hWnd = win32gui.FindWindowEx(
        FW(FW(FW(0, "Shell_TrayWnd"), "TrayNotifyWnd"), "SysPager"),
        0,
        "ToolbarWindow32",
        None)
    # Get TaskBar area
    rect = win32gui.GetClientRect(hWnd)
    width = rect[2]
    height = rect[3]
    # Refresh TaskBar with a simulation of the mouse moving
    for x in range(width / 4):
        for y in range(height / 4):
            xx = x * 4
            yy = y * 4
            win32api.SendMessage(
                hWnd,
                win32con.WM_MOUSEMOVE,
                0,
                yy * 65536 + xx)

# ------------------------------------------------------------------------------
# Refresh the task bar. Unix.
# ------------------------------------------------------------------------------
def __refreshTaskBarUnix():
    """Refresh the task bar. Unix.
    """
    pass

# ------------------------------------------------------------------------------
# Refresh the task bar.
# ------------------------------------------------------------------------------
def refreshTaskBar():
    """Refresh the task bar.
    """
    try:
        if os.name == "nt":
            __refreshTaskBarWin32()
        else:
            __refreshTaskBarUnix()
    except:
        pass

