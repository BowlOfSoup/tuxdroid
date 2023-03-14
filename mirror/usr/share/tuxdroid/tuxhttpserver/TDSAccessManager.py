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

import threading

TDAC_ACCESS_RELEASED        = None

ACCESS_PRIORITY_LOW         = 0
ACCESS_PRIORITY_NORMAL      = 1
ACCESS_PRIORITY_HIGH        = 2
ACCESS_PRIORITY_CRITICAL    = 3

ACCESS_PRIORITIES = [
    ACCESS_PRIORITY_LOW,
    ACCESS_PRIORITY_NORMAL,
    ACCESS_PRIORITY_HIGH,
    ACCESS_PRIORITY_CRITICAL,
]

# ------------------------------------------------------------------------------
# Tux Droid Server : Access manager.
# ------------------------------------------------------------------------------
class TDSAccessManager(object):
    """Tux Droid Server : Access manager.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__currentAllowedUser = TDAC_ACCESS_RELEASED
        self.__allowedUserMutex = threading.Lock()
        self.__currentPriorityLevel = ACCESS_PRIORITY_LOW
        self.__priorityLevelMutex = threading.Lock()
        self.__locked = False
        self.__lockMutex = threading.Lock()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getCurrentAllowedUser(self):
        self.__allowedUserMutex.acquire()
        result = self.__currentAllowedUser
        self.__allowedUserMutex.release()
        return result

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __setCurrentAllowedUser(self, idUser):
        self.__allowedUserMutex.acquire()
        self.__currentAllowedUser = idUser
        self.__allowedUserMutex.release()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getCurrentPriorityLevel(self):
        self.__priorityLevelMutex.acquire()
        result = self.__currentPriorityLevel
        self.__priorityLevelMutex.release()
        return result

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __setCurrentPriorityLevel(self, priorityLevel):
        self.__priorityLevelMutex.acquire()
        self.__currentPriorityLevel = priorityLevel
        self.__priorityLevelMutex.release()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getLocked(self):
        self.__lockMutex.acquire()
        result = self.__locked
        self.__lockMutex.release()
        return result

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def setLocked(self, value = True):
        self.__lockMutex.acquire()
        self.__locked = value
        self.__lockMutex.release()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def acquireAccess(self, idUser, priorityLevel):
        # Priority level not found
        if priorityLevel not in ACCESS_PRIORITIES:
            return False
        # If the resource access is locked by the root then fail
        if self.getLocked():
            return False
        else:
            # Get currents
            currentPriorityLevel = self.getCurrentPriorityLevel()
            currentAllowedUser = self.getCurrentAllowedUser()
            # If the access is released or client already have the access
            if (currentAllowedUser == TDAC_ACCESS_RELEASED) or \
            (currentAllowedUser == idUser) or \
            (priorityLevel > currentPriorityLevel):
                self.__setCurrentAllowedUser(idUser)
                self.__setCurrentPriorityLevel(priorityLevel)
                return True
            else:
                return False

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def releaseAccess(self, idUser = None):
        if (self.getCurrentAllowedUser() == idUser) or \
           (idUser == None):
            self.__setCurrentAllowedUser(TDAC_ACCESS_RELEASED)
            self.__setCurrentPriorityLevel(ACCESS_PRIORITY_LOW)

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def checkAccess(self, idUser, priorityLevel):
        # Priority level not found
        if priorityLevel not in ACCESS_PRIORITIES:
            return False
        # If the resource access is locked by the root then fail
        if self.getLocked():
            return False
        else:
            # Get currents
            currentPriorityLevel = self.getCurrentPriorityLevel()
            currentAllowedUser = self.getCurrentAllowedUser()
            # If the access is released or client already have the access
            if (currentAllowedUser == TDAC_ACCESS_RELEASED) or \
            (currentAllowedUser == idUser) or \
            (priorityLevel > currentPriorityLevel):
                return True
            else:
                return False

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def checkUserHaveAccess(self, idUser):
        # If the resource access is locked by the root then fail
        if self.getLocked():
            return False
        else:
            # Get current
            currentAllowedUser = self.getCurrentAllowedUser()
            # If the access is released or client already have the access
            if (currentAllowedUser == TDAC_ACCESS_RELEASED) or \
            (currentAllowedUser == idUser):
                return True
            else:
                return False
