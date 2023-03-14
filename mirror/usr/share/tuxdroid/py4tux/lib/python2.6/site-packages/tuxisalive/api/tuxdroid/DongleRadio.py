# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *

# ------------------------------------------------------------------------------
# Class to interact with the connection/disconnection of the radio/dongle.
# ------------------------------------------------------------------------------
class DongleRadio(ApiBaseChildResource):
    """Class to interact with the connection/disconnection of the radio/dongle.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, apiBase, apiBaseServer, stStName):
        """Constructor of the class.
        @param apiBase: ApiBase parent object.
        @param apiBaseServer: ApiBaseServer object.
        """
        ApiBaseChildResource.__init__(self, apiBase, apiBaseServer)
        self.__stStName = stStName

    # --------------------------------------------------------------------------
    # Get the state of the radio/dongle connection.
    # --------------------------------------------------------------------------
    def getConnected(self):
        """Get the state of the radio/dongle connection.
        @return: True or False.
        """
        value = self._requestOne(self.__stStName)
        if value != None:
            return eval(value)
        return False

    # --------------------------------------------------------------------------
    # Wait until the radio/dongle was connected.
    # --------------------------------------------------------------------------
    def waitConnected(self, timeout):
        """Wait until the radio/dongle was connected.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if self.getConnected():
            return True
        return self._waitFor(self.__stStName, "True", timeout)

    # --------------------------------------------------------------------------
    # Wait until the radio/dongle was disconnected.
    # --------------------------------------------------------------------------
    def waitDisconnected(self, timeout):
        """Wait until the radio/dongle was disconnected.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if not self.getConnected():
            return True
        return self._waitFor(self.__stStName, "False", timeout)

    # --------------------------------------------------------------------------
    # Register a callback on the connected event.
    # --------------------------------------------------------------------------
    def registerEventOnConnected(self, funct, idx = None):
        """Register a callback on the connected event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(self.__stStName, "True", funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the connected event.
    # --------------------------------------------------------------------------
    def unregisterEventOnConnected(self, idx):
        """Unregister a callback from the connected event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(self.__stStName, idx)

    # --------------------------------------------------------------------------
    # Register a callback on the disconnected event.
    # --------------------------------------------------------------------------
    def registerEventOnDisconnected(self, funct, idx = None):
        """Register a callback on the disconnected event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(self.__stStName, "False", funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the disconnected event.
    # --------------------------------------------------------------------------
    def unregisterEventOnDisconnected(self, idx):
        """Unregister a callback from the disconnected event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(self.__stStName, idx)
