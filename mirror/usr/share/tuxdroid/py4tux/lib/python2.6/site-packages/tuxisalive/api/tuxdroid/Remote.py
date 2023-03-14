# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Class the control the state of the remote buttons.
# ------------------------------------------------------------------------------
class Remote(ApiBaseChildResource):
    """Class the control the state of the remote buttons.
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
    # Return the state of the remote buttons.
    # --------------------------------------------------------------------------
    def getState(self):
        """Return the state of the remote buttons.
        """
        return self._requestOne(ST_NAME_REMOTE_BUTTON)

    # --------------------------------------------------------------------------
    # Wait until the remote was pressed.
    # --------------------------------------------------------------------------
    def waitPressed(self, timeout, key):
        """Wait until the remote was pressed.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @param key: key to wiat.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if not key in REMOTE_KEY_LIST:
            return False
        if self.getState() == key:
            return True
        return self._waitFor(ST_NAME_REMOTE_BUTTON, key, timeout)

    # --------------------------------------------------------------------------
    # Wait until the remote was released.
    # --------------------------------------------------------------------------
    def waitReleased(self, timeout):
        """Wait until the remote was released.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if self.getState() == K_RELEASED:
            return True
        return self._waitFor(ST_NAME_REMOTE_BUTTON, K_RELEASED, timeout)

    # --------------------------------------------------------------------------
    # Register a callback on the pressed event.
    # --------------------------------------------------------------------------
    def registerEventOnPressed(self, funct, key, idx = None):
        """Register a callback on the pressed event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @param key: remote key.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(ST_NAME_REMOTE_BUTTON, key, funct, idx)
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
        self._unregisterEvent(ST_NAME_REMOTE_BUTTON, idx)

    # --------------------------------------------------------------------------
    # Register a callback on the released event.
    # --------------------------------------------------------------------------
    def registerEventOnReleased(self, funct, idx = None):
        """Register a callback on the released event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(ST_NAME_REMOTE_BUTTON, K_RELEASED, funct,
            idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the released event.
    # --------------------------------------------------------------------------
    def unregisterEventOnReleased(self, idx):
        """Unregister a callback from the released event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(ST_NAME_REMOTE_BUTTON, idx)
