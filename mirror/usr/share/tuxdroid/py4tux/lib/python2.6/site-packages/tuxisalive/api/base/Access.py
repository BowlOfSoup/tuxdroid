# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import time

from ApiBaseChildResource import ApiBaseChildResource
from const.ConstAccess import *
from const.ConstClient import *

# ------------------------------------------------------------------------------
# Class to control the resource access.
# ------------------------------------------------------------------------------
class Access(ApiBaseChildResource):
    """Class to control the resource access. When you have your level to
    CLIENT_LEVEL_RESTRICTED, you need to acquiring and releasing the resource.
    It mechanism is needed for the synchronization of the resource access by the
    programs which want using Tuxdroid.
    CLIENT_LEVEL_FREE, CLIENT_LEVEL_ROOT and CLIENT_LEVEL_ANONYME don't have
    this restriction.
    When you make a tux gadget, you must to use the CLIENT_LEVEL_RESTRICTED level.
    (Only by convention ;) )
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
    # To acquiring the resource access.
    # --------------------------------------------------------------------------
    def acquire(self, priorityLevel = ACCESS_PRIORITY_NORMAL):
        """To acquiring the resource access.
        Need for CLIENT_LEVEL_RESTRICTED level.
        Don't forget to release the access after !!!
        Not available for CLIENT_LEVEL_ANONYME level.
        @param priorityLevel: (ACCESS_PRIORITY_LOW|ACCESS_PRIORITY_NORMAL|
                              ACCESS_PRIORITY_HIGH|ACCESS_PRIORITY_CRITICAL)
        @return: the success of the acquiring.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        parameters = {
            'priority_level' : priorityLevel,
        }
        cmd = "access/acquire?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Wait that the resource can be acquired.
    # --------------------------------------------------------------------------
    def waitAcquire(self, timeout, priorityLevel = ACCESS_PRIORITY_NORMAL):
        """Wait that the resource can be acquired.
        Need for CLIENT_LEVEL_RESTRICTED level.
        Don't forget to release the access after !!!
        @param timeout: maximal delay to wait.
        @param priorityLevel: (ACCESS_PRIORITY_LOW|ACCESS_PRIORITY_NORMAL|
                              ACCESS_PRIORITY_HIGH|ACCESS_PRIORITY_CRITICAL)
        @return: the success of the acquiring.
        """
        tBegin = time.time()
        while (not self.acquire(priorityLevel)):
            if (time.time() - tBegin) >= timeout:
                return False
            time.sleep(1.0)
        return True

    # --------------------------------------------------------------------------
    # To releasing the resource access.
    # --------------------------------------------------------------------------
    def release(self):
        """To releasing the resource access.
        Need for CLIENT_LEVEL_RESTRICTED level.
        Not available for CLIENT_LEVEL_ANONYME level.
        @return: the success of the command.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        cmd = "access/release?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # To force the acquisition of the resource by a specified client.
    # --------------------------------------------------------------------------
    def forcingAcquire(self, idClient):
        """To force the acquisition of the resource by a specified client.
        Only available for CLIENT_LEVEL_ROOT level.
        @param idClient: idx of the client.
        @return: the success of the command.
        """
        if self.getServer().getClientLevel() != CLIENT_LEVEL_ROOT:
            return False
        parameters = {
            'id_client' : idClient,
        }
        cmd = "access/forcing_acquire?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # To force the releasing of the resource.
    # --------------------------------------------------------------------------
    def forcingRelease(self):
        """To force the releasing of the resource.
        Only available for CLIENT_LEVEL_ROOT level.
        @return: the success of the command.
        """
        if self.getServer().getClientLevel() != CLIENT_LEVEL_ROOT:
            return False
        cmd = "access/forcing_release?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # To lock the resource access.
    # --------------------------------------------------------------------------
    def lock(self):
        """To lock the resource access. After it, nobody will can
        acquiring the resource.
        Only available for CLIENT_LEVEL_ROOT level.
        @return: the success of the command.
        """
        if self.getServer().getClientLevel() != CLIENT_LEVEL_ROOT:
            return False
        cmd = "access/lock?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # To unlock the resource access.
    # --------------------------------------------------------------------------
    def unLock(self):
        """To unlock the resource access.
        Only available for CLIENT_LEVEL_ROOT level.
        @return: the success of the command.
        """
        if self.getServer().getClientLevel() != CLIENT_LEVEL_ROOT:
            return False
        cmd = "access/unlock?"
        return self._sendCommandBooleanResult(cmd)
