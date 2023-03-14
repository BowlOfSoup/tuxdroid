# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Class to interact with the battery states and level.
# ------------------------------------------------------------------------------
class Battery(ApiBaseChildResource):
    """Class to interact with the battery states and level.
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
    # Register a callback on the battery level event.
    # --------------------------------------------------------------------------
    def registerEventOnLevelChange(self, funct, idx = None):
        """Register a callback on the battery level event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        self._syndicateEvent(ST_NAME_BATTERY_LEVEL)
        nIdx = self._registerEvent(ST_NAME_BATTERY_LEVEL, None, funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the battery level event.
    # --------------------------------------------------------------------------
    def unregisterEventOnLevelChange(self, idx):
        """Unregister a callback from the battery level event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(ST_NAME_BATTERY_LEVEL, idx)

    # --------------------------------------------------------------------------
    # Register a callback on the battery state event.
    # --------------------------------------------------------------------------
    def registerEventOnStateChange(self, funct, idx = None):
        """Register a callback on the battery state event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        self._syndicateEvent(ST_NAME_BATTERY_STATE)
        nIdx = self._registerEvent(ST_NAME_BATTERY_STATE, None, funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the battery state event.
    # --------------------------------------------------------------------------
    def unregisterEventOnStateChange(self, idx):
        """Unregister a callback from the battery state event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(ST_NAME_BATTERY_STATE, idx)

    # --------------------------------------------------------------------------
    # Return the current level of the battery.
    # --------------------------------------------------------------------------
    def getLevel(self):
        """Return the current level of the battery.
        @return: A float.
        """
        self._syndicateEvent(ST_NAME_BATTERY_LEVEL)
        value = self._requestOne(ST_NAME_BATTERY_LEVEL)
        if value != None:
            return eval(value) / 1000.0
        return 0.0

    # --------------------------------------------------------------------------
    # Return the current state of the battery.
    # --------------------------------------------------------------------------
    def getState(self):
        """Return the current state of the battery.
        @return: The battery state.
            <BATTERY_STATE_FULL|BATTERY_STATE_HIGH|BATTERY_STATE_LOW|
             BATTERY_STATE_EMPTY>
        """
        self._syndicateEvent(ST_NAME_BATTERY_STATE)
        value = self._requestOne(ST_NAME_BATTERY_STATE)
        if value != None:
            return value
        return BATTERY_STATE_EMPTY
