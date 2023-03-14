# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from lib.Helper import Helper
from ApiBaseChildResource import ApiBaseChildResource
from const.ConstServer import SW_NAME_EXTERNAL_STATUS

# ------------------------------------------------------------------------------
# Class to control the events.
# ------------------------------------------------------------------------------
class Event(ApiBaseChildResource):
    """Class to control the events.
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
        self.handler = self.getEventsHandler()
        # Initialize the helper
        Helper.__init__(self)

    # --------------------------------------------------------------------------
    # Deprecated ...
    # --------------------------------------------------------------------------
    def setDelay(self, delay = 0.1):
        """Deprecated ...
        """
        pass

    # --------------------------------------------------------------------------
    # Use external events.
    # --------------------------------------------------------------------------
    def useExternalEvents(self):
        """Use external events.
        """
        self._syndicateEvent(SW_NAME_EXTERNAL_STATUS)
