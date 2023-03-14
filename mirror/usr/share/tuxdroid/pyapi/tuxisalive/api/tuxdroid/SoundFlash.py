# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxDriver import *

# ------------------------------------------------------------------------------
# Class to control the sound flash memory of Tux Droid.
# ------------------------------------------------------------------------------
class SoundFlash(ApiBaseChildResource):
    """Class to control the sound flash memory of Tux Droid.
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
    # Play a sound from the internal memory.
    # --------------------------------------------------------------------------
    def playAsync(self, track, volume = 100.0):
        """Play a sound from the internal memory.
        @param track: index of the sound.
        @param volume: volume (0.0 .. 100.0)
        @return: the success of the command.
        """
        if not self._checkObjectType('track', track, "int"):
            return False
        if not self._checkObjectType('volume', volume, "float"):
            return False
        parameters = {
            'track' : track,
            'volume' : volume,
        }
        cmd = "sound_flash/play?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Play a sound from the internal memory.
    # --------------------------------------------------------------------------
    def play(self, track, volume = 100.0):
        """Play a sound from the internal memory.
        @param track: index of the sound.
        @param volume: volume (0.0 .. 100.0)
        @return: the success of the command.
        """
        if self.playAsync(track, volume):
            if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
                return True
            trackName = "TRACK_%.3d" % track
            self._waitFor(ST_NAME_AUDIO_FLASH_PLAY, trackName, 0.2)
            value = self._requestOne(ST_NAME_AUDIO_FLASH_PLAY)
            if value == trackName:
                self._waitFor(ST_NAME_AUDIO_FLASH_PLAY, "STOP", 70.0)
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Reflash the sound flash memory.
    # --------------------------------------------------------------------------
    def reflash(self, wavList):
        """Reflash the sound flash memory.
        Only available for CLIENT_LEVEL_RESTRICTED and CLIENT_LEVEL_ROOT
        levels.
        @param wavList: wave file path list.
        @return: (SOUND_REFLASH_NO_ERROR|SOUND_REFLASH_ERROR_PARAMETERS|
                  SOUND_REFLASH_ERROR_RF_OFFLINE|SOUND_REFLASH_ERROR_WAV|
                  SOUND_REFLASH_ERROR_USB)
        """
        if self.getServer().getClientLevel() not in [CLIENT_LEVEL_RESTRICTED,
            CLIENT_LEVEL_ROOT]:
            return SOUND_REFLASH_ERROR_PARAMETERS
        if not self._checkObjectType('wavList', wavList, "list"):
            return SOUND_REFLASH_ERROR_PARAMETERS
        if len(wavList) <= 0:
            return SOUND_REFLASH_ERROR_PARAMETERS
        tracks = ""
        for wav in wavList:
            if not self._checkObjectType('wav', wav, "str"):
                return SOUND_REFLASH_ERROR_PARAMETERS
            tracks = "%s%s|" % (tracks, wav)
        tracks = tracks[:-1]
        parameters = {
            'tracks' : tracks,
        }
        cmd = "sound_flash/reflash?"
        if not self._sendCommandBooleanResult(cmd, parameters):
            return SOUND_REFLASH_ERROR_PARAMETERS
        else:
            if self._waitFor(ST_NAME_SOUND_REFLASH_END, SSV_NDEF, 5.0):
                self._waitFor(ST_NAME_SOUND_REFLASH_END, None, 150.0)
            return self._requestOne(ST_NAME_SOUND_REFLASH_END)
