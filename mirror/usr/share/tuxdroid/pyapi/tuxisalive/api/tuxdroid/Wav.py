# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxOsl import *

# ------------------------------------------------------------------------------
# Class to play a wave files.
# ------------------------------------------------------------------------------
class Wav(ApiBaseChildResource):
    """Class to play a wave files.
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
    # Play a wave file.
    # --------------------------------------------------------------------------
    def playAsync(self, waveFile, begin = 0.0, end = 0.0):
        """Play a wave file.
        @param waveFile: wave file to play.
        @param begin: start seconds.
        @param end: stop seconds.
        @return: the success of the command.
        """
        if not self._checkObjectType('waveFile', waveFile, 'str'):
            return False
        if not self._checkObjectType('begin', begin, 'float'):
            return False
        if not self._checkObjectType('end', end, 'float'):
            return False
        parameters = {
            'path' : waveFile,
            'begin' : begin,
            'end' : end
        }
        cmd = "wav/play?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Play a wave file.
    # --------------------------------------------------------------------------
    def play(self, waveFile, begin = 0.0, end = 0.0):
        """Play a wave file.
        @param waveFile: wave file to play.
        @param begin: start seconds.
        @param end: stop seconds.
        @return: the success of the command.
        """
        if not self.playAsync(waveFile, begin, end):
            return False
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return True
        if not self._waitFor(ST_NAME_WAV_CHANNEL_START, None, 1.0):
            return False
        value = self._requestOne(ST_NAME_WAV_CHANNEL_START)
        try:
            channel = int(value)
        except:
            return False
        endStName = WAV_CHANNELS_NAME_LIST[channel]
        if self._requestOne(endStName) == "OFF":
            self._waitFor(endStName, "ON", 1.0)
        return self._waitFor(endStName, "OFF", 600.0)

    # --------------------------------------------------------------------------
    # Stop the current wave file.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the current wave file.
        @return: the success of the command.
        """
        cmd = "wav/stop?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Set the pause state of the wave player.
    # --------------------------------------------------------------------------
    def setPause(self, value = True):
        """Set the pause state of the wave player.
        @param value: True or False.
        @return: the success of the command.
        """
        # Check the value var type
        if not self._checkObjectType('value', value, 'bool'):
            return False
        if value:
            pause = "True"
        else:
            pause = "False"
        parameters = {
            'value' : pause,
        }
        cmd = "wav/pause?"
        return self._sendCommandBooleanResult(cmd, parameters)
