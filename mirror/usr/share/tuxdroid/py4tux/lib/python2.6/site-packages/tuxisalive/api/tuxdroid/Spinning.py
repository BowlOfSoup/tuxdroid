# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Class to control the spinning movements.
# ------------------------------------------------------------------------------
class Spinning(ApiBaseChildResource):
    """Class to control the spinning movements.
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
    # Check the speed value.
    # --------------------------------------------------------------------------
    def __checkSpeed(self, speed):
        """Check the speed value.
        """
        if speed < SPV_VERYSLOW:
            speed = SPV_VERYSLOW
        elif speed > SPV_VERYFAST:
            speed = SPV_VERYFAST
        return speed

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
        cmd = "spinning/speed?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Stop the spinning movement.
    # --------------------------------------------------------------------------
    def off(self):
        """Stop the spinning movement.
        @return: the success of the command.
        """
        cmd = "spinning/off?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Move the robot to the left.
    # --------------------------------------------------------------------------
    def leftOnAsync(self, turns, speed = SPV_VERYFAST):
        """Move the robot to the left.
        @param turns: number of turns as float.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not self._checkObjectType('turns', turns, "float"):
            return False
        count = int(turns * 4)
        if (count == 0):
            count = 1
        if (count > 255):
            count = 255
        parameters = {
            'count' : count,
        }
        cmd = "spinning/left_on?"
        ret = self._sendCommandBooleanResult(cmd, parameters)
        if ret:
            ret = self.setSpeed(speed)
        return ret

    # --------------------------------------------------------------------------
    # Move the robot to the right.
    # --------------------------------------------------------------------------
    def rightOnAsync(self, turns, speed = SPV_VERYFAST):
        """Move the robot to the right.
        @param turns: number of turns as float.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not self._checkObjectType('turns', turns, "float"):
            return False
        count = int(turns * 4)
        if (count == 0):
            count = 1
        if (count > 255):
            count = 255
        parameters = {
            'count' : count,
        }
        cmd = "spinning/right_on?"
        ret = self._sendCommandBooleanResult(cmd, parameters)
        if ret:
            ret = self.setSpeed(speed)
        return ret

    # --------------------------------------------------------------------------
    # Move the robot to the left.
    # --------------------------------------------------------------------------
    def leftOn(self, turns, speed = SPV_VERYFAST):
        """Move the robot to the left.
        @param turns: number of turns.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        timeout = turns * 5.0
        ret = self.leftOnAsync(turns, speed)
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitLeftMovingOff(timeout)
        return ret

    # --------------------------------------------------------------------------
    # Move the robot to the right.
    # --------------------------------------------------------------------------
    def rightOn(self, turns, speed = SPV_VERYFAST):
        """Move the robot to the right.
        @param turns: number of turns.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        timeout = turns * 5.0
        ret = self.rightOnAsync(turns, speed)
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitRightMovingOff(timeout)
        return ret

    # --------------------------------------------------------------------------
    # Turn the robot to the left during a number of seconds.
    # --------------------------------------------------------------------------
    def leftOnDuringAsync(self, duration, speed = SPV_VERYFAST):
        """Turn the robot to the left during a number of seconds.
        @param duration: duration of the rotation.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not self._checkObjectType('duration', duration, "float"):
            return False
        parameters = {
            'duration' : duration,
        }
        cmd = "spinning/left_on_during?"
        ret = self._sendCommandBooleanResult(cmd, parameters)
        if ret:
            ret = self.setSpeed(speed)
        return ret

    # --------------------------------------------------------------------------
    # Turn the robot to the right during a number of seconds.
    # --------------------------------------------------------------------------
    def rightOnDuringAsync(self, duration, speed = SPV_VERYFAST):
        """Turn the robot to the right during a number of seconds.
        @param duration: duration of the rotation.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        if not self._checkObjectType('duration', duration, "float"):
            return False
        parameters = {
            'duration' : duration,
        }
        cmd = "spinning/right_on_during?"
        ret = self._sendCommandBooleanResult(cmd, parameters)
        if ret:
            ret = self.setSpeed(speed)
        return ret

    # --------------------------------------------------------------------------
    # Turn the robot to the left during a number of seconds.
    # --------------------------------------------------------------------------
    def leftOnDuring(self, duration, speed = SPV_VERYFAST):
        """Turn the robot to the left during a number of seconds.
        @param duration: duration of the rotation.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        timeout = duration * 2.0
        ret = self.leftOnDuringAsync(duration, speed)
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitLeftMovingOff(timeout)
        return ret

    # --------------------------------------------------------------------------
    # Turn the robot to the left during a number of seconds.
    # --------------------------------------------------------------------------
    def rightOnDuring(self, duration, speed = SPV_VERYFAST):
        """Turn the robot to the left during a number of seconds.
        @param duration: duration of the rotation.
        @param speed: speed of the rotation.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @return: the success of the command.
        """
        timeout = duration * 2.0
        ret = self.rightOnDuringAsync(duration, speed)
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return ret
        if ret:
            ret = self.waitRightMovingOff(timeout)
        return ret

    # --------------------------------------------------------------------------
    # Get the left rotation state of the robot.
    # --------------------------------------------------------------------------
    def getLeftMovingState(self):
        """Get the left rotation state of the robot.
        @return: a boolean.
        """
        value = self._requestOne(ST_NAME_SPIN_LEFT_MOTOR_ON)
        if value in [None, "False"]:
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Get the right rotation state of the robot.
    # --------------------------------------------------------------------------
    def getRightMovingState(self):
        """Get the right rotation state of the robot.
        @return: a boolean.
        """
        value = self._requestOne(ST_NAME_SPIN_RIGHT_MOTOR_ON)
        if value in [None, "False"]:
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Wait that the robot don't turn to the left.
    # --------------------------------------------------------------------------
    def waitLeftMovingOff(self, timeout):
        """Wait that the robot don't turn to the left.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        return self._waitFor(ST_NAME_SPIN_LEFT_MOTOR_ON, "False" , timeout)

    # --------------------------------------------------------------------------
    # Wait that the robot don't turn to the right.
    # --------------------------------------------------------------------------
    def waitRightMovingOff(self, timeout):
        """Wait that the robot don't turn to the right.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        return self._waitFor(ST_NAME_SPIN_RIGHT_MOTOR_ON, "False" , timeout)
