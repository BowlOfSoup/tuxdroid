# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Class to control a mouth/eyes body part of Tux Droid.
# ------------------------------------------------------------------------------
class MouthEyes(ApiBaseChildResource):
    """Class to control a mouth/eyes body part of Tux Droid.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, apiBase, apiBaseServer, positionStName, mvmRemStName,
        partName):
        """Constructor of the class.
        @param apiBase: ApiBase parent object.
        @param apiBaseServer: ApiBaseServer object.
        @param positionStName: Position status name.
        @param mvmRemStName: Remaining movements status name.
        @param partName: Body part name <"mouth"|"eyes">
        """
        ApiBaseChildResource.__init__(self, apiBase, apiBaseServer)
        # Body part field
        self.__positionStName = positionStName
        self.__mvmRemStName = mvmRemStName
        self.__partName = partName

    # --------------------------------------------------------------------------
    # Open this body part.
    # --------------------------------------------------------------------------
    def open(self):
        """Open this body part.
        """
        cmd = "%s/open?" % self.__partName
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Close this body part.
    # --------------------------------------------------------------------------
    def close(self):
        """Close this body part.
        """
        cmd = "%s/close?" % self.__partName
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Stop the movement of this body part.
    # --------------------------------------------------------------------------
    def off(self):
        """Stop the movement of this body part.
        """
        cmd = "%s/off?" % self.__partName
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Move this body part.
    # --------------------------------------------------------------------------
    def onAsync(self, count, finalState = SSV_NDEF):
        """Move this body part.
        (asynchronous)
        @param count: number of movements.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        @return: the success of the command.
        """
        if not self._checkObjectType('count', count, "int"):
            return False
        if not self._checkObjectType('finalState', finalState, "str"):
            return False
        if finalState not in SSV_MOUTHEYES_POSITIONS:
            return False
        parameters = {
            'count' : count,
            'final_state' : finalState,
        }
        cmd = "%s/on?" % self.__partName
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Move this body part.
    # --------------------------------------------------------------------------
    def on(self, count, finalState = SSV_NDEF):
        """Move this body part.
        @param count: number of movements.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        @return: the success of the command.
        """
        if not self._checkObjectType('count', count, "int"):
            return False
        if not self._checkObjectType('finalState', finalState, "str"):
            return False
        if finalState not in SSV_MOUTHEYES_POSITIONS:
            return False
        timeout = count * 1.0
        ret = self.onAsync(count, finalState)
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitMovingOff(timeout)
        return ret

    # --------------------------------------------------------------------------
    # Move this body part during a number of seconds.
    # --------------------------------------------------------------------------
    def onDuringAsync(self, duration, finalState = SSV_NDEF):
        """Move this body part during a number of seconds.
        @param duration: duration time in seconds.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        @return: the success of the command.
        """
        if not self._checkObjectType('duration', duration, "float"):
            return False
        if not self._checkObjectType('finalState', finalState, "str"):
            return False
        if finalState not in SSV_MOUTHEYES_POSITIONS:
            return False
        parameters = {
            'duration' : duration,
            'final_state' : finalState,
        }
        cmd = "%s/on_during?" % self.__partName
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Move this body part during a number of seconds.
    # --------------------------------------------------------------------------
    def onDuring(self, duration, finalState = SSV_NDEF):
        """Move this body part during a number of seconds.
        @param duration: duration time in seconds.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        @return: the success of the command.
        """
        if not self._checkObjectType('duration', duration, "float"):
            return False
        if not self._checkObjectType('finalState', finalState, "str"):
            return False
        if finalState not in SSV_MOUTHEYES_POSITIONS:
            return False
        timeout = 2.0 * duration
        ret = self.onDuringAsync(duration, finalState)
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitMovingOff(timeout)
        return ret

    # --------------------------------------------------------------------------
    # Get the position of the body part.
    # --------------------------------------------------------------------------
    def getPosition(self):
        """Get the position of the body part.
        @return: (SSV_NDEF|SSV_OPEN|SSV_CLOSE)
        """
        value = self._requestOne(self.__positionStName)
        if value not in SSV_MOUTHEYES_POSITIONS:
            return SSV_NDEF
        else:
            return value

    # --------------------------------------------------------------------------
    # Get the moving state of this body part.
    # --------------------------------------------------------------------------
    def getMovingState(self):
        """Get the moving state of this body part.
        @return: a boolean.
        """
        value = self._requestOne(self.__mvmRemStName)
        if value in [None, "0"]:
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Wait that this body part don't move.
    # --------------------------------------------------------------------------
    def waitMovingOff(self, timeout):
        """Wait that this body part don't move.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self.getMovingState():
            return True
        return self._waitFor(self.__mvmRemStName, "0", timeout)

    # --------------------------------------------------------------------------
    # Wait a specific position of this body part.
    # --------------------------------------------------------------------------
    def waitPosition(self, position, timeout):
        """Wait a specific position of this body part.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param position: position to wait.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if position not in SSV_MOUTHEYES_POSITIONS:
            return False
        if self.getPosition() == position:
            return True
        return self._waitFor(self.__positionStName, position, timeout)
