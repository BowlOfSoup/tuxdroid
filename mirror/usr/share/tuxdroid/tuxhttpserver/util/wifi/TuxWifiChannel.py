#    Copyright (C) 2009 KYSOH Sa
#    Remi Jocaille <remi.jocaille@kysoh.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from ctypes import *
import os

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# libtuxwifichannel wrapper class.
# ------------------------------------------------------------------------------
class TuxWifiChannel(object):
    """libtuxwifichannel wrapper class.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, library_path = None):
        """Constructor.
        @param library_path: Path of libtuxwifichannel library. (Default None)
        """
        if library_path == None:
            mPath, mFile = os.path.split(__file__)
            if os.name == 'nt':
                library_path = os.path.join(mPath, "libtuxwifichannel.dll")
            else:
                library_path = os.path.join(mPath, "libtuxwifichannel.so")
        self.tux_wifi_channel_lib = None
        if os.path.isfile(library_path):
            try:
                self.tux_wifi_channel_lib = CDLL(library_path)
            except:
                self.tux_wifi_channel_lib = None

    # --------------------------------------------------------------------------
    # Get the currently used wifi channel.
    # --------------------------------------------------------------------------
    def getCurrent(self, priorSSID = ""):
        """Get the currently used wifi channel.
        @param priorSSID: Network SSID to search in prior.
        @return: An integer or None.
        """
        if self.tux_wifi_channel_lib == None:
            return None
        try:
            channel = self.tux_wifi_channel_lib.get_wifi_channel(c_char_p(priorSSID))
            if channel == -1:
                channel = None
        except:
            channel = None
        return channel
