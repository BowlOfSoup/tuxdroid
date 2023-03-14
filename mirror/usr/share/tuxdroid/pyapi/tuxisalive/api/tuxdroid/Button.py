# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.lib.Helper import Helper
from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from const.ConstTuxDriver import *
from Switch import Switch
from Remote import Remote

# ------------------------------------------------------------------------------
# Class to control the state of the Tux Droid buttons.
# ------------------------------------------------------------------------------
class Button(ApiBaseChildResource):
    """Class to control the state of the Tux Droid buttons.
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
        self.left = Switch(apiBase, apiBaseServer, ST_NAME_LEFT_BUTTON)
        """Left flipper switch.
        @see: Switch
        """
        self.right = Switch(apiBase, apiBaseServer, ST_NAME_RIGHT_BUTTON)
        """Right flipper switch.
        @see: Switch
        """
        self.head = Switch(apiBase, apiBaseServer, ST_NAME_HEAD_BUTTON)
        """Head switch.
        @see: Switch
        """
        self.remote = Remote(apiBase, apiBaseServer)
        """Remote.
        @see: Remote
        """
        Helper.__init__(self)
