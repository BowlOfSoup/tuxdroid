# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource
from tuxisalive.api.base.const.ConstClient import *
from const.ConstTuxOsl import *

# ------------------------------------------------------------------------------
# Class to use the text to speech engine.
# ------------------------------------------------------------------------------
class TTS(ApiBaseChildResource):
    """Class to use the text to speech engine.
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
        self.__locutor = "Ryan"
        self.__pitch = 100

    # --------------------------------------------------------------------------
    # Get the voices list.
    # --------------------------------------------------------------------------
    def getVoices(self):
        """Get the voices list.
        @return: The voices list.
        """
        result = []
        cmd = "tts/voices?"
        ret, varResult = self._sendCommandFullResult(cmd)
        if ret:
            dataCount = varResult["data_count"]
            for i in range(dataCount):
                dataName = "data%d" % i
                result.append(varResult[dataName]["locutor"][:-2])
        return result

    # --------------------------------------------------------------------------
    # Set the pitch of the locutor.
    # --------------------------------------------------------------------------
    def setPitch(self, pitch):
        """Set the pitch of the locutor.
        @param pitch: (50 .. 200)
        """
        if not self._checkObjectType('pitch', pitch, 'int'):
            return
        self.__pitch = pitch

    # --------------------------------------------------------------------------
    # Get the pitch of the locutor.
    # --------------------------------------------------------------------------
    def getPitch(self):
        """Get the pitch of the locutor.
        @return: the pitch of the locutor.
        """
        return self.__pitch

    # --------------------------------------------------------------------------
    # Set the locutor.
    # --------------------------------------------------------------------------
    def setLocutor(self, locutor):
        """Set the locutor.
        @param locutor: name of the locutor.
        """
        if not self._checkObjectType('locutor', locutor, 'str'):
            return
        self.__locutor = locutor

    # --------------------------------------------------------------------------
    # Get the locutor.
    # --------------------------------------------------------------------------
    def getLocutor(self):
        """Get the locutor.
        @return: the name of the locutor.
        """
        return self.__locutor

    # --------------------------------------------------------------------------
    # Read a text with the text to speak engine.
    # --------------------------------------------------------------------------
    def speakAsync(self, text, locutor = None, pitch = None):
        """Read a text with the text to speak engine.
        @param text: text to speak.
        @param locutor: name of the locutor.
        @param pitch: pitch (50 .. 200)
        @return: the success of the command.
        """
        # Check the text var type
        if not self._checkObjectType('text', text, 'str'):
            return False
        # Set the locutor
        if locutor != None:
            self.setLocutor(locutor)
        # Set the pitch
        if pitch != None:
            self.setPitch(pitch)
        # Fixe the text
        text = self._reencodeText(text, True)
        # Perform the speech
        parameters = {
            'text' : text,
            'locutor' : self.getLocutor(),
            'pitch' : self.getPitch(),
        }
        cmd = "tts/speak?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Read a text with the text to speak engine.
    # --------------------------------------------------------------------------
    def speak(self, text, locutor = None, pitch = None):
        """Read a text with the text to speak engine.
        @param text: text to speak.
        @param locutor: name of the locutor.
        @param pitch: pitch (50 .. 200)
        @return: the success of the command.
        """
        if self.speakAsync(text, locutor, pitch):
            if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
                return True
            if not self._waitFor(ST_NAME_TTS_SOUND_STATE, "ON", 3.0):
                return False
            self._waitFor(ST_NAME_TTS_SOUND_STATE, "OFF", 600.0)
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Push a text in the TTS stack.
    # --------------------------------------------------------------------------
    def speakPush(self, text, locutor = None, pitch = None):
        """Push a text in the TTS stack.
        @param text: text to speak.
        @param locutor: name of the locutor.
        @param pitch: pitch (50 .. 200)
        @return: the success of the command.
        """
        # Check the text var type
        if not self._checkObjectType('text', text, 'str'):
            return False
        # Set the locutor
        if locutor != None:
            self.setLocutor(locutor)
        # Set the pitch
        if pitch != None:
            self.setPitch(pitch)
        # Fixe the text
        text = self._reencodeText(text, True)
        # Perform the speech
        parameters = {
            'text' : text,
            'locutor' : self.getLocutor(),
            'pitch' : self.getPitch(),
        }
        cmd = "tts/stack_speak?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Stop the current speech and flush the TTS stack.
    # --------------------------------------------------------------------------
    def speakFlush(self):
        """Stop the current speech and flush the TTS stack.
        @return: the success of the command.
        """
        cmd = "tts/stack_flush?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Skip the current speech from TTS stack.
    # --------------------------------------------------------------------------
    def speakNext(self):
        """Skip the current speech from TTS stack.
        @return: the success of the command.
        """
        cmd = "tts/stack_next?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Stop the current speech.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the current speech.
        @return: the success of the command.
        """
        cmd = "tts/stop?"
        return self._sendCommandBooleanResult(cmd)

    # --------------------------------------------------------------------------
    # Set the pause state of the tts engine.
    # --------------------------------------------------------------------------
    def setPause(self, value = True):
        """Set the pause state of the tts engine.
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
        cmd = "tts/pause?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Register a callback on the voice list event.
    # --------------------------------------------------------------------------
    def registerEventOnVoiceList(self, funct, idx = None):
        """Register a callback on the voice list event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(ST_NAME_VOICE_LIST, None, funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the voice list event.
    # --------------------------------------------------------------------------
    def unregisterEventOnVoiceList(self, idx):
        """Unregister a callback from the voice list event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(ST_NAME_VOICE_LIST, idx)

    # --------------------------------------------------------------------------
    # Register a callback on the sound on event.
    # --------------------------------------------------------------------------
    def registerEventOnSoundOn(self, funct, idx = None):
        """Register a callback on the sound on event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(ST_NAME_TTS_SOUND_STATE, "ON", funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the sound on event.
    # --------------------------------------------------------------------------
    def unregisterEventOnSoundOn(self, idx):
        """Unregister a callback from the sound on event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(ST_NAME_TTS_SOUND_STATE, idx)

    # --------------------------------------------------------------------------
    # Register a callback on the sound off event.
    # --------------------------------------------------------------------------
    def registerEventOnSoundOff(self, funct, idx = None):
        """Register a callback on the sound off event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return -1
        nIdx = self._registerEvent(ST_NAME_TTS_SOUND_STATE, "OFF", funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the sound off event.
    # --------------------------------------------------------------------------
    def unregisterEventOnSoundOff(self, idx):
        """Unregister a callback from the sound off event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param idx: index from a previous register.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return
        self._unregisterEvent(ST_NAME_TTS_SOUND_STATE, idx)
