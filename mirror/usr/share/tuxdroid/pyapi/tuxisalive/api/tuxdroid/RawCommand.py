# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource

# ------------------------------------------------------------------------------
# Class to send a raw commands to Tux Droid.
# ------------------------------------------------------------------------------
class RawCommand(ApiBaseChildResource):
    """Class to send a raw commands to Tux Droid.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, apiBase, apiBaseServer):
        """Constructor of the class.
        @param apiBase: ApiBase parent object.
        @param apiBaseServer: ApiBaseServer object.
        """
        ApiBaseChildResource.__init__(self, apiBase, apiBaseServer)

    # --------------------------------------------------------------------------
    # Send a raw command to Tux Droid.
    # --------------------------------------------------------------------------
    def send(self, b0, b1, b2, b3, b4):
        """Send a raw command to tuxdroid.
        """
        if not self._checkObjectType('b0', b0, "int"):
            return False
        if not self._checkObjectType('b1', b1, "int"):
            return False
        if not self._checkObjectType('b2', b2, "int"):
            return False
        if not self._checkObjectType('b3', b3, "int"):
            return False
        if not self._checkObjectType('b4', b4, "int"):
            return False
        raw = "0.0:RAW_CMD:0x%.2x:0x%.2x:0x%.2x:0x%.2x:0x%.2x" % (b0, b1, b2,
            b3, b4)
        parameters = {
            'macro' : raw,
        }
        cmd = "macro/play?"
        return self._sendCommandBooleanResult(cmd, parameters)
