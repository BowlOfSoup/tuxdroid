# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Class to control the state of a switch.
# ------------------------------------------------------------------------------
class Switch(ApiBaseChildResource):
    """Class to control the state of a switch.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, apiBase, apiBaseServer, switchStName):
        """Constructor of the class.
        @param apiBase: ApiBase parent object.
        @param apiBaseServer: ApiBaseServer object.
        @param switchStName: Name of the switch.
            <ST_NAME_LEFT_BUTTON|ST_NAME_RIGHT_BUTTON|ST_NAME_HEAD_BUTTON>
        """
        ApiBaseChildResource.__init__(self, apiBase, apiBaseServer)
        self.__switchStName = switchStName

    # --------------------------------------------------------------------------
    # Return the state of the switch.
    # --------------------------------------------------------------------------
    def getState(self):
        """Return the state of the switch.
        @return: True or False.
        """
        value = self._requestOne(self.__switchStName)
        if value != None:
            return eval(value)
        return False

    # --------------------------------------------------------------------------
    # Wait until the switch was pressed.
    # --------------------------------------------------------------------------
    def waitPressed(self, timeout):
        """Wait until the switch was pressed.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if self.getState():
            return True
        return self._waitFor(self.__switchStName, "True", timeout)

    # --------------------------------------------------------------------------
    # Wait until the switch was released.
    # --------------------------------------------------------------------------
    def waitReleased(self, timeout):
        """Wait until the switch was released.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if not self.getState():
            return True
        return self._waitFor(self.__switchStName, "False", timeout)

    # --------------------------------------------------------------------------
    # Register a callback on the pressed event.
    # --------------------------------------------------------------------------
    def registerEventOnPressed(self, funct, idx = None):
        """Register a callback on the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(self.__switchStName, "True", funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the pressed event.
    # --------------------------------------------------------------------------
    def unregisterEventOnPressed(self, idx):
        """Unregister a callback from the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(self.__switchStName, idx)

    # --------------------------------------------------------------------------
    # Register a callback on the pressed event.
    # --------------------------------------------------------------------------
    def registerEventOnReleased(self, funct, idx = None):
        """Register a callback on the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(self.__switchStName, "False", funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the pressed event.
    # --------------------------------------------------------------------------
    def unregisterEventOnReleased(self, idx):
        """Unregister a callback from the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(self.__switchStName, idx)
