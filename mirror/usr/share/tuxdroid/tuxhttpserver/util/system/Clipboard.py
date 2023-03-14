#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

if os.name == 'nt':
    import win32clipboard
    import win32con

# ------------------------------------------------------------------------------
# Class to control the clipboard.
# ------------------------------------------------------------------------------
class Clipboard(object):
    """Class to control the clipboard.
    """

    # --------------------------------------------------------------------------
    # Get the last copied text in the clipboard.
    # --------------------------------------------------------------------------
    def getText():
        """Get the last copied text in the clipboard.
        @return: A string.
        """
        if os.name == 'nt':
            win32clipboard.OpenClipboard()
            try:
                text = win32clipboard.GetClipboardData(win32con.CF_TEXT)
            except:
                text = ""
            win32clipboard.CloseClipboard()
            return text
        else:
            return ""

    getText = staticmethod(getText)
