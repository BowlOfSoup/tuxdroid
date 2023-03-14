# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Class to control the flippers.
# ------------------------------------------------------------------------------
class Flippers(ApiBaseChildResource):
    """Class to control the flippers.
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
    # Check speed value.
    # --------------------------------------------------------------------------
    def __checkSpeed(self, speed):
        """Check speed value.
        """
        if speed < SPV_VERYSLOW:
            speed = SPV_VERYSLOW
        elif speed > SPV_VERYFAST:
            speed = SPV_VERYFAST
        return speed

    # --------------------------------------------------------------------------
    # Set the flippers to up.
    # --------------------------------------------------------------------------
    def up(self):
        """Set the flippers to up.
        """
        cmd = "flippers/up?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Set the flippers to down.
    # --------------------------------------------------------------------------
    def down(self):
        """Set the flippers to down.
        """
        cmd = "flippers/down?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Stop the flippers movement.
    # --------------------------------------------------------------------------
    def off(self):
        """Stop the flippers movement.
        """
        cmd = "flippers/off?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Set the speed of the flippers movement.
    # --------------------------------------------------------------------------
    def setSpeed(self, speed):
        """Set the speed of the flippers movement.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not self._checkObjectType('speed', speed, "int"):
            return False
        speed = self.__checkSpeed(speed)
        parameters = {
            'value' : speed,
        }
        cmd = "flippers/speed?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Move the flippers.
    # --------------------------------------------------------------------------
    def onAsync(self, count, finalState = SSV_UP, speed = SPV_VERYFAST):
        """Move the flippers.
        @param count: number of movements.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_UP|SSV_DOWN)
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not self._checkObjectType('count', count, "int"):
            return False
        if not self._checkObjectType('finalState', finalState, "str"):
            return False
        if finalState not in SSV_FLIPPERS_POSITIONS:
            return False
        parameters = {
            'count' : count,
            'final_state' : finalState,
        }
        cmd = "flippers/on?"
        ret = self._sendCommandBooleanResult(cmd, parameters)
        if ret:
            ret = self.setSpeed(speed)
        return ret

    # --------------------------------------------------------------------------
    # Move the flippers.
    # --------------------------------------------------------------------------
    def on(self, count, finalState = SSV_UP, speed = SPV_VERYFAST):
        """Move the flippers.
        @param count: number of movements.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_UP|SSV_DOWN)
        @param speed: speed of the movement.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        timeout = count * 1.0
        ret = self.onAsync(count, finalState, speed)
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitMovingOff(timeout)
        return ret

    # --------------------------------------------------------------------------
    # Move the flippers during a number of seconds.
    # --------------------------------------------------------------------------
    def onDuringAsync(self, duration, finalState = SSV_UP, speed = SPV_VERYFAST):
        """Move the flippers during a number of seconds.
        @param duration: duration time in seconds.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_UP|SSV_DOWN)
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not self._checkObjectType('duration', duration, "float"):
            return False
        if not self._checkObjectType('finalState', finalState, "str"):
            return False
        if finalState not in SSV_FLIPPERS_POSITIONS:
            return False
        parameters = {
            'duration' : duration,
            'final_state' : finalState,
        }
        cmd = "flippers/on_during?"
        ret = self._sendCommandBooleanResult(cmd, parameters)
        if ret:
            ret = self.setSpeed(speed)
        return ret

    # --------------------------------------------------------------------------
    # Move the flippers during a number of seconds.
    # --------------------------------------------------------------------------
    def onDuring(self, duration, finalState = SSV_UP, speed = SPV_VERYFAST):
        """Move the flippers during a number of seconds.
        @param duration: duration time in seconds.
        @param finalState: requested state after the movement.
                            (SSV_NDEF|SSV_UP|SSV_DOWN)
        @param speed: speed of the movement.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        timeout = 2.0 * duration
        ret = self.onDuringAsync(duration, finalState, speed)
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitMovingOff(timeout)
        return ret

    # --------------------------------------------------------------------------
    # Get the position of the flippers.
    # --------------------------------------------------------------------------
    def getPosition(self):
        """Get the position of the flippers.
        @return: (SSV_NDEF|SSV_UP|SSV_DOWN)
        """
        value = self._requestOne(ST_NAME_FLIPPERS_POSITION)
        if value not in SSV_FLIPPERS_POSITIONS:
            return SSV_NDEF
        else:
            return value

    # --------------------------------------------------------------------------
    # Get the moving state of the flippers.
    # --------------------------------------------------------------------------
    def getMovingState(self):
        """Get the moving state of the flippers.
        @return: a boolean.
        """
        value = self._requestOne(ST_NAME_FLIPPERS_MOTOR_ON)
        if value in [None, "False"]:
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Wait that the flippers don't move.
    # --------------------------------------------------------------------------
    def waitMovingOff(self, timeout):
        """Wait that the flippers don't move.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        return self._waitFor(ST_NAME_FLIPPERS_MOTOR_ON, "False", timeout)

    # --------------------------------------------------------------------------
    # Wait a specific position of the flippers.
    # --------------------------------------------------------------------------
    def waitPosition(self, position, timeout):
        """Wait a specific position of the flippers.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param position: Flippers position. <SSV_NDEF|SSV_UP|SSV_DOWN>
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if position not in SSV_FLIPPERS_POSITIONS:
            return False
        if self.getPosition() == position:
            return True
        return self._waitFor(ST_NAME_FLIPPERS_POSITION, position, timeout)
