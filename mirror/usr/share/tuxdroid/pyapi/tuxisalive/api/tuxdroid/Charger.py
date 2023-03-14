# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Class to interact with the charger states.
# ------------------------------------------------------------------------------
class Charger(ApiBaseChildResource):
    """Class to interact with the charger states.
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
    # Register a callback on the charger state event.
    # --------------------------------------------------------------------------
    def registerEventOnStateChange(self, funct, idx = None):
        """Register a callback on the charger state event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(ST_NAME_CHARGER_STATE, None, funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the charger state event.
    # --------------------------------------------------------------------------
    def unregisterEventOnStateChange(self, idx):
        """Unregister a callback from the charger state event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(ST_NAME_CHARGER_STATE, idx)

    # --------------------------------------------------------------------------
    # Return the current state of the charger.
    # --------------------------------------------------------------------------
    def getState(self):
        """Return the current state of the charger.
        @return: The charger state.
            <CHARGER_STATE_UNPLUGGED|CHARGER_STATE_CHARGING|
             CHARGER_STATE_PLUGGED_NO_POWER|CHARGER_STATE_TRICKLE|
             CHARGER_STATE_INHIBITED>
        """
        value = self._requestOne(ST_NAME_CHARGER_STATE)
        if value != None:
            return value
        return CHARGER_STATE_UNPLUGGED

    # --------------------------------------------------------------------------
    # Get if the charger is connected or not.
    # --------------------------------------------------------------------------
    def getConnected(self):
        """Get if the charger is connected or not.
        @return: True or False.
        """
        if self.getState() != CHARGER_STATE_UNPLUGGED:
            return True
        else:
            return False
