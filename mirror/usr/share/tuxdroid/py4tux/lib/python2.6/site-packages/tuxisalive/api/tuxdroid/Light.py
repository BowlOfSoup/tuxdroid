# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Class to interact with the light sensor.
# ------------------------------------------------------------------------------
class Light(ApiBaseChildResource):
    """Class to interact with the light sensor.
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
    # Register a callback on the light level event.
    # --------------------------------------------------------------------------
    def registerEventOnLightChange(self, funct, idx = None):
        """Register a callback on the light level event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        self._syndicateEvent(ST_NAME_LIGHT_LEVEL)
        nIdx = self._registerEvent(ST_NAME_LIGHT_LEVEL, None, funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the the light level event.
    # --------------------------------------------------------------------------
    def unregisterEventOnLightChange(self, idx):
        """Unregister a callback from the light level event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(ST_NAME_LIGHT_LEVEL, idx)

    # --------------------------------------------------------------------------
    # Return the current level of the light.
    # --------------------------------------------------------------------------
    def getLevel(self):
        """Return the current level of the light.
        @return: A float.
        """
        self._syndicateEvent(ST_NAME_LIGHT_LEVEL)
        value = self._requestOne(ST_NAME_LIGHT_LEVEL)
        if value != None:
            return eval(value)
        return 0.0
