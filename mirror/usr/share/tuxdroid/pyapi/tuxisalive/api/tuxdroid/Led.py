# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import time

from tuxisalive.api.base.lib.Helper import Helper
from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from LedBase import LedBase

# ------------------------------------------------------------------------------
# Class to control the blue leds.
# ------------------------------------------------------------------------------
class Led(ApiBaseChildResource):
    """Class to control the blue leds.
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
        self.left = LedBase(apiBase, apiBaseServer, "left")
        """Left blue led.
        @see: LedBase
        """
        self.right = LedBase(apiBase, apiBaseServer, "right")
        """Right blue led.
        @see: LedBase
        """
        self.both = LedBase(apiBase, apiBaseServer, "both")
        """Both blue leds.
        @see: LedBase
        """
        Helper.__init__(self)
