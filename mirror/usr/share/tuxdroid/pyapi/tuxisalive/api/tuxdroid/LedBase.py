# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import time

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Base class to control a led.
# ------------------------------------------------------------------------------
class LedBase(ApiBaseChildResource):
    """Base class to control a led.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, apiBase, apiBaseServer, ledName):
        """Constructor of the class.
        @param apiBase: ApiBase parent object.
        @param apiBaseServer: ApiBaseServer object.
        @param ledName: Name of the led. <"left"|"right"|"both">
        """
        ApiBaseChildResource.__init__(self, apiBase, apiBaseServer)
        if ledName == "both":
            self.__ledNamex = LED_NAME_BOTH
        elif ledName == "left":
            self.__ledNamex = LED_NAME_LEFT
        elif ledName == "right":
            self.__ledNamex = LED_NAME_RIGHT

    # --------------------------------------------------------------------------
    # Change the intensity of the led.
    # --------------------------------------------------------------------------
    def __changeIntensity(self, fxType, intensity):
        """Change the intensity of the led.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @param intensity: intensity of the led (0.0 .. 1.0)
        @return: the success of the command.
        """
        if not self._checkObjectType('fxType', fxType, "int"):
            return False
        if not self._checkObjectType('intensity', intensity, "float"):
            return False
        if fxType == LFX_NONE:
            parameters = {
                'intensity' : intensity,
                'leds' : self.__ledNamex,
            }
            cmd = "leds/on?"
        else:
            if fxType == LFX_FADE:
                fxStep = 10
            elif fxType == LFX_STEP:
                fxStep = 3
            fxCType = LFXEX_GRADIENT_NBR
            parameters = {
                'fx_speed' : 0.5,
                'fx_step' : fxStep,
                'fx_type' : fxCType,
                'intensity' : intensity,
                'leds' : self.__ledNamex,
            }
            cmd = "leds/set?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Set the intensity of the led.
    # --------------------------------------------------------------------------
    def setIntensity(self, intensity):
        """Set the intensity of the led.
        @param intensity: intensity of the led (0.0 .. 1.0)
        @return: the success of the command.
        """
        return self.__changeIntensity(LFX_NONE, intensity)

    # --------------------------------------------------------------------------
    # Set the led state to ON.
    # --------------------------------------------------------------------------
    def on(self, fxType = LFX_NONE):
        """Set the led state to ON.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        return self.__changeIntensity(fxType, 1.0)

    # --------------------------------------------------------------------------
    # Set the led state to OFF.
    # --------------------------------------------------------------------------
    def off(self, fxType = LFX_NONE):
        """Set the led state to OFF.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        return self.__changeIntensity(fxType, 0.0)

    # --------------------------------------------------------------------------
    # Make a pulse effect with the led.
    # --------------------------------------------------------------------------
    def blinkDuringAsync(self, speed, duration, fxType = LFX_NONE):
        """Make a pulse effect with the led.
        @param speed: speed of the state changing.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @param duration: duration of the effect.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        if not self._checkObjectType('speed', speed, "int"):
            return False
        if not self._checkObjectType('duration', duration, "float"):
            return False
        if not self._checkObjectType('fxType', fxType, "int"):
            return False
        if speed not in SPV_SPEED_VALUES:
            return False
        perSec = speed
        count = int(duration * perSec * 2)
        delay = 1.0 / perSec
        if fxType == LFX_NONE:
            parameters = {
                'leds' : self.__ledNamex,
                'count' : count,
                'delay' : delay,
            }
            cmd = "leds/blink?"
        else:
            if fxType == LFX_FADE:
                fxStep = 10
            elif fxType == LFX_STEP:
                fxStep = 2
            fxCType = LFXEX_GRADIENT_NBR
            fxSpeed = delay / 3.0
            parameters = {
                'count' : count,
                'fx_speed' : fxSpeed,
                'fx_step' : fxStep,
                'fx_type' : fxCType,
                'leds' : self.__ledNamex,
                'max_intensity' : 1.0,
                'min_intensity' : 0.0,
                'period' : delay,
            }
            cmd = "leds/pulse?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Make a pulse effect with the led.
    # --------------------------------------------------------------------------
    def blinkDuring(self, speed, duration, fxType = LFX_NONE):
        """Make a pulse effect with the led.
        @param speed: speed of the state changing.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @param duration: duration of the effect.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        ret = self.blinkDuringAsync(speed, duration, fxType)
        if ret:
            time.sleep(duration)
        return ret

    # --------------------------------------------------------------------------
    # Make a pulse effect with the led.
    # --------------------------------------------------------------------------
    def blinkAsync(self, speed, count, fxType = LFX_NONE):
        """Make a pulse effect with the led.
        @param speed: speed of the state changing.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @param count: number of blinks.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        if not self._checkObjectType('speed', speed, "int"):
            return False
        if not self._checkObjectType('count', count, "int"):
            return False
        if not self._checkObjectType('fxType', fxType, "int"):
            return False
        if speed not in SPV_SPEED_VALUES:
            return False
        count = count * 2
        delay = 1.0 / speed
        if fxType == LFX_NONE:
            parameters = {
                'leds' : self.__ledNamex,
                'count' : count,
                'delay' : delay,
            }
            cmd = "leds/blink?"
        else:
            if fxType == LFX_FADE:
                fxStep = 10
            elif fxType == LFX_STEP:
                fxStep = 2
            fxCType = LFXEX_GRADIENT_NBR
            fxSpeed = delay / 3.0
            parameters = {
                'count' : count,
                'fx_speed' : fxSpeed,
                'fx_step' : fxStep,
                'fx_type' : fxCType,
                'leds' : self.__ledNamex,
                'max_intensity' : 1.0,
                'min_intensity' : 0.0,
                'period' : delay,
            }
            cmd = "leds/pulse?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Make a pulse effect with the led.
    # --------------------------------------------------------------------------
    def blink(self, speed, count, fxType = LFX_NONE):
        """Make a pulse effect with the led.
        @param speed: speed of the state changing.
        (SPV_VERYSLOW|SPV_SLOW|SPV_NORMAL|SPV_FAST|SPV_VERYFAST)
        @param count: number of blinks.
        @param fxType: type of the transition effect.
                      (LFX_NONE|LFX_FADE|LFX_STEP)
        @return: the success of the command.
        """
        ret = self.blinkAsync(speed, count, fxType)
        if ret:
            delay = 1.0 / speed
            duration = delay * count
            time.sleep(duration)
        return ret

    # --------------------------------------------------------------------------
    # Get the state of the led.
    # --------------------------------------------------------------------------
    def getState(self):
        """Get the state of the led.
        @return: (SSV_ON|SSV_OFF|SSV_CHANGING)
        """
        result = SSV_OFF
        if self.__ledNamex == LED_NAME_LEFT:
            result = self._requestOne(ST_NAME_LEFT_LED)
        elif self.__ledNamex == LED_NAME_RIGHT:
            result = self._requestOne(ST_NAME_RIGHT_LED)
        else:
            value = self._requestOne(ST_NAME_LEFT_LED)
            value1 = self._requestOne(ST_NAME_RIGHT_LED)
            if value == value1:
                result = value
        return result
