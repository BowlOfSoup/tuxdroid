# -*- coding: utf-8 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from ctypes import *
import os

from util.logger import *

# Error codes list
E_TUXOSL_BEGIN                = 256
E_TUXOSL_NOERROR              = 0
E_TUXOSL_PARSERISDISABLED     = E_TUXOSL_BEGIN
E_TUXOSL_INVALIDCOMMAND       = E_TUXOSL_BEGIN + 1
E_TUXOSL_STACKOVERFLOW        = E_TUXOSL_BEGIN + 2
E_TUXOSL_BADWAVFILE           = E_TUXOSL_BEGIN + 3
E_TUXOSL_FILEERROR            = E_TUXOSL_BEGIN + 4
E_TUXOSL_INVALIDIDENTIFIER    = E_TUXOSL_BEGIN + 5
E_TUXOSL_INVALIDNAME          = E_TUXOSL_BEGIN + 6
E_TUXOSL_INVALIDPARAMETER     = E_TUXOSL_BEGIN + 7
E_TUXOSL_BUSY                 = E_TUXOSL_BEGIN + 8
E_TUXOSL_NODEVICE             = E_TUXOSL_BEGIN + 9
E_TUXOSL_BABTTS               = E_TUXOSL_BEGIN + 10
E_TUXOSL_PORTAUDIO            = E_TUXOSL_BEGIN + 11
E_TUXOSL_NOTRUNNING           = E_TUXOSL_BEGIN + 12
E_TUXOSL_TTSENGINENOTFOUND    = E_TUXOSL_BEGIN + 13

# Identifiers list of the statuses
SW_ID_OSL_SYMBOLIC_VERSION          = 0
SW_ID_OSL_GENERAL_SOUND_STATE       = 1
SW_ID_OSL_WAV_VOLUME                = 2
SW_ID_OSL_TTS_VOLUME                = 3
SW_ID_OSL_TTS_PITCH                 = 4
SW_ID_OSL_TTS_LOCUTOR               = 5
SW_ID_OSL_WAV0_SOUND_STATE          = 6
SW_ID_OSL_WAV0_PAUSE_STATE          = 7
SW_ID_OSL_WAV0_STOP                 = 8
SW_ID_OSL_WAV1_SOUND_STATE          = 9
SW_ID_OSL_WAV1_PAUSE_STATE          = 10
SW_ID_OSL_WAV1_STOP                 = 11
SW_ID_OSL_WAV2_SOUND_STATE          = 12
SW_ID_OSL_WAV2_PAUSE_STATE          = 13
SW_ID_OSL_WAV2_STOP                 = 14
SW_ID_OSL_WAV3_SOUND_STATE          = 15
SW_ID_OSL_WAV3_PAUSE_STATE          = 16
SW_ID_OSL_WAV3_STOP                 = 17
SW_ID_OSL_TTS0_SOUND_STATE          = 18
SW_ID_OSL_TTS0_PAUSE_STATE          = 19
SW_ID_OSL_TTS0_STOP                 = 20
SW_ID_OSL_TTS0_VOICE_LOADED         = 21
SW_ID_OSL_TTS0_SPEAK_STATUS         = 22
SW_ID_OSL_TTS0_VOICE_LIST           = 23
SW_ID_OSL_WAV_CHANNEL_START         = 24

# Names list of the statuses
ST_NAME_OSL_SOUND_STATE     = 'general_sound_state'
ST_NAME_SPEAK_STATUS        = 'tts_0_speak_status'
ST_NAME_TTS_SOUND_STATE     = 'tts_0_sound_state'
ST_NAME_VOICE_LIST          = 'tts_0_voice_list'
ST_NAME_WAV_CHANNEL_START   = 'tts_wav_channel_start'
ST_NAME_WAV_0_SOUND_STATE   = 'wav_0_sound_state'
ST_NAME_WAV_1_SOUND_STATE   = 'wav_1_sound_state'
ST_NAME_WAV_2_SOUND_STATE   = 'wav_2_sound_state'
ST_NAME_WAV_3_SOUND_STATE   = 'wav_3_sound_state'
ST_NAME_OSL_SYMB_VER        = 'osl_symbolic_version'
ST_NAME_WAV_VOLUME          = 'wav_volume'
ST_NAME_TTS_VOLUME          = 'tts_volume'
ST_NAME_TTS_PITCH           = 'tts_pitch'
ST_NAME_TTS_LOCUTOR         = 'tts_locutor'
ST_NAME_WAV_0_PAUSE_STATE   = 'wav_0_pause_state'
ST_NAME_WAV_0_STOP          = 'wav_0_stop'
ST_NAME_WAV_1_PAUSE_STATE   = 'wav_1_pause_state'
ST_NAME_WAV_1_STOP          = 'wav_1_stop'
ST_NAME_WAV_2_PAUSE_STATE   = 'wav_2_pause_state'
ST_NAME_WAV_2_STOP          = 'wav_2_stop'
ST_NAME_WAV_3_PAUSE_STATE   = 'wav_3_pause_state'
ST_NAME_WAV_3_STOP          = 'wav_3_stop'
ST_NAME_TTS_PAUSE_STATE     = 'tts_0_pause_state'
ST_NAME_TTS_STOP            = 'tts_0_stop'
ST_NAME_TTS_VOICE_LOADED    = 'tts_0_voice_loaded'
SW_NAME_OSL = [
    ST_NAME_OSL_SYMB_VER,
    ST_NAME_OSL_SOUND_STATE,
    ST_NAME_WAV_VOLUME,
    ST_NAME_TTS_VOLUME,
    ST_NAME_TTS_PITCH,
    ST_NAME_TTS_LOCUTOR,
    ST_NAME_WAV_0_SOUND_STATE,
    ST_NAME_WAV_0_PAUSE_STATE,
    ST_NAME_WAV_0_STOP,
    ST_NAME_WAV_1_SOUND_STATE,
    ST_NAME_WAV_1_PAUSE_STATE,
    ST_NAME_WAV_1_STOP,
    ST_NAME_WAV_2_SOUND_STATE,
    ST_NAME_WAV_2_PAUSE_STATE,
    ST_NAME_WAV_2_STOP,
    ST_NAME_WAV_3_SOUND_STATE,
    ST_NAME_WAV_3_PAUSE_STATE,
    ST_NAME_WAV_3_STOP,
    ST_NAME_TTS_SOUND_STATE,
    ST_NAME_TTS_PAUSE_STATE,
    ST_NAME_TTS_STOP,
    ST_NAME_TTS_VOICE_LOADED,
    ST_NAME_SPEAK_STATUS,
    ST_NAME_VOICE_LIST,
    ST_NAME_WAV_CHANNEL_START,
]

# Locutors languages dictionary
TUX_OSL_ACAPELA_LOCUTORS_BY_LANGUAGE_COUNTRY_DICT = {
    'en_US' : ["Ryan", "Heather"],
    'en_GB' : ["Graham", "Lucy"],
    'fr' : ["Bruno", "Julie"],
    'de' : ["Klaus", "Sarah"],
    'nl_BE' : ["Sofie"],
    'nl' : ["Femke"],
    'ar' : ["Salma"],
    'da' : ["Mette"],
    'no' : ["Kari"],
    'pt' : ["Celia"],
    'sv' : ["Erik", "Emma"],
    'it' : ["Chiara"],
    'es' : ["Maria"],
}

# Callback type defines
TUX_OSL_STATUS_CALLBACK = CFUNCTYPE(None, c_char_p)
TUX_OSL_BUFFER_CALLBACK = CFUNCTYPE(c_int, c_int, c_char_p)

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# libtuxosl wrapper class.
# ------------------------------------------------------------------------------
class TuxOSL(object):
    """libtuxosl wrapper class.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, library_path = None):
        """Constructor.
        @param library_path: Path of libtuxosl library. (Default None)
        """
        self.__logger = SimpleLogger("libtuxosl_wrapper")
        self.__logger.setTarget(LOG_TARGET_FILE)
        self.__logger.setLevel(LOG_LEVEL_INFO)
        self.__logger.resetLog()
        self.__logger.logInfo("-----------------------------------------------")
        self.__logger.logInfo("libtuxosl wrapper v%s" % __version__)
        self.__logger.logInfo("Author : %s" % __author__)
        self.__logger.logInfo("Licence : %s" % __licence__)
        self.__logger.logInfo("-----------------------------------------------")
        if library_path == None:
            mPath, mFile = os.path.split(__file__)
            if os.name == 'nt':
                library_path = os.path.join(mPath, "libtuxosl.dll")
            else:
                library_path = os.path.join(mPath, "libtuxosl.so")
        self.__logger.logInfo("Libtuxosl path : (%s)" % library_path)
        self.__callback_container = []
        self.tux_osl_lib = None
        if os.path.isfile(library_path):
            try:
                self.tux_osl_lib = CDLL(library_path)
                self.__logger.logInfo("The shared library was found.")
            except:
                self.tux_osl_lib = None
                txt = "Error on handling the library in your application."
                self.__logger.logError(txt)
                return
            self.__logger.logInfo("Initialize the library")
            self.tux_osl_lib.TuxOSL_InitModule()
        else:
            txt = "Path (%s) not found !" % library_path
            self.__logger.logError(txt)
            txt = "The shared library was not handled in your application."
            self.__logger.logError(txt)
        self.__started = False
        self.__startedMutex = threading.Lock()
        self.__startingMutex = threading.Lock()

    # --------------------------------------------------------------------------
    # Register a callback function to the "status" event.
    # --------------------------------------------------------------------------
    def SetStatusCallback(self, funct = None):
        """Register a callback function to the "status" event.
        @param funct: Pointer to the function.
        """
        if self.tux_osl_lib == None:
            return

        if funct == None:
            return

        cb = TUX_OSL_STATUS_CALLBACK(funct)
        self.__callback_container.append(cb)
        self.tux_osl_lib.TuxOSL_SetStatusCallback(cb)
        return

    # --------------------------------------------------------------------------
    # Register a callback function to the "TTS buffer" event.
    # --------------------------------------------------------------------------
    def SetTTSBufferCallback(self, funct = None):
        """Register a callback function to the "TTS buffer" event.
        @param funct: Pointer to the function.
        """
        if self.tux_osl_lib == None:
            return

        if funct == None:
            return

        cb = TUX_OSL_BUFFER_CALLBACK(funct)
        self.__callback_container.append(cb)
        self.tux_osl_lib.TuxOSL_SetTTSBufferCallback(cb)
        return

    # --------------------------------------------------------------------------
    # Start libtuxosl.
    # --------------------------------------------------------------------------
    def Start(self, tts_engine_path):
        """Start libtuxosl.
        @param tts_engine_path: TTS engine path (Not yet used)
        @return: The success of the starting.
        """
        self.__startingMutex.acquire()
        if self.getStarted():
            self.__startingMutex.release()
            return E_TUXOSL_NOERROR

        if self.tux_osl_lib == None:
            self.__startingMutex.release()
            return E_TUXOSL_NOTRUNNING

        try:
            ret = self.tux_osl_lib.TuxOSL_Start(c_char_p(tts_engine_path))
        except:
            ret = E_TUXOSL_PORTAUDIO

        if ret == E_TUXOSL_NOERROR:
            self.__logger.logInfo("Libtuxosl successfuly started.")
            self.__setStarted(True)
            voicesList = self.GetStatusValue(SW_ID_OSL_TTS0_VOICE_LIST)
            self.__logger.logInfo(voicesList[:-1])
        else:
            self.__setStarted(False)
            self.__logger.logError("Libtuxosl can't start : code(%d) expl(%s)."\
                % (ret, self.StrError(ret)))
        self.__startingMutex.release()
        return ret

    # --------------------------------------------------------------------------
    # Set the run state of tuxosl.
    # --------------------------------------------------------------------------
    def __setStarted(self, value):
        """Set the run state of tuxosl.
        @param value: State.
        """
        self.__startedMutex.acquire()
        self.__started = value
        self.__startedMutex.release()

    # --------------------------------------------------------------------------
    # Get the run state of tuxosl.
    # --------------------------------------------------------------------------
    def getStarted(self):
        """Get the run state of tuxosl.
        @return: The state.
        """
        self.__startedMutex.acquire()
        result = self.__started
        self.__startedMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Stop libtuxosl.
    # --------------------------------------------------------------------------
    def Stop(self):
        """Stop libtuxosl.
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return

        self.__logger.logInfo("Stop the library.")
        self.__setStarted(False)
        self.tux_osl_lib.TuxOSL_Stop()

    # --------------------------------------------------------------------------
    # Get the log file path.
    # --------------------------------------------------------------------------
    def getLogFilePath(self):
        """Get the log file path.
        @return: The log file path.
        """
        return self.__logger.getLogFilePath()

    # --------------------------------------------------------------------------
    # Perform a command through libtuxosl.
    # --------------------------------------------------------------------------
    def PerformCommand(self, delay, command):
        """Perform a command through libtuxosl.
        @param delay: Delay before the command execution.
        @param command: Command to execute.
        @return: The success of the command performing.
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return E_TUXOSL_PARSERISDISABLED

        ret = self.tux_osl_lib.TuxOSL_PerformCommand(c_double(delay),
            c_char_p(command))

        self.__logger.logDebug("Perform the cmd : cmd(%s) delay (%f)" % \
            (command, delay))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        return ret

    # --------------------------------------------------------------------------
    # Perform the content of a macro commands file through libtuxosl.
    # --------------------------------------------------------------------------
    def PerformMacroFile(self, file_path = ""):
        """Perform the content of a macro commands file through libtuxosl.
        @param file_path: Macro commands file path.
        @return: The success of the performing.
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return E_TUXOSL_PARSERISDISABLED

        ret = self.tux_osl_lib.TuxOSL_PerformMacroFile(c_char_p(file_path))

        self.__logger.logDebug("Perform a macro : path(%s)" % file_path)
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        return ret

    # --------------------------------------------------------------------------
    # Perform a macro commands through libtuxosl.
    # --------------------------------------------------------------------------
    def PerformMacroText(self, macro = ""):
        """Perform a macro commands through libtuxosl.
        @param macro: Macro commands text.
        @return: The success of the performing.
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return E_TUXOSL_PARSERISDISABLED

        ret = self.tux_osl_lib.TuxOSL_PerformMacroText(c_char_p(macro))

        self.__logger.logDebug("Perform a macro text : -->")
        for line in macro.split('\n'):
            self.__logger.logDebug("%s" % line)
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        return ret

    # --------------------------------------------------------------------------
    # Clear the stack of delayed commands.
    # --------------------------------------------------------------------------
    def ClearCommandStack(self):
        """Clear the stack of delayed commands.
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return

        self.tux_osl_lib.TuxOSL_ClearCommandStack()

        self.__logger.logDebug("Clear the commands stack")

        return

    # --------------------------------------------------------------------------
    # Get the identifier of a status.
    # --------------------------------------------------------------------------
    def GetStatusId(self, name = "osl_symbolic_version"):
        """Get the identifier of a status.
        @param name: Status name.
        @return: The identifier as Integer.
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return -1

        idc = c_int(0)
        idcp = pointer(idc)
        ret = self.tux_osl_lib.TuxOSL_GetStatusId(c_char_p(name), idcp)

        self.__logger.logDebug("Get status id : (%s) -> (%d)" % (name,
            idc.value))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        if ret != E_TUXOSL_NOERROR:
            idc.value = -1

        return idc.value

    # --------------------------------------------------------------------------
    # Get the name of a status.
    # --------------------------------------------------------------------------
    def GetStatusName(self, id = 0):
        """Get the name of a status.
        @param id: Identifier of the status.
        @return: The name of the status or "UNDEFINED".
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return "UNDEFINED"

        result = " " * 256
        ret = self.tux_osl_lib.TuxOSL_GetStatusName(c_int(id),
            c_char_p(result))
        result = result.replace(" ", "")

        self.__logger.logDebug("Get status name : (%d) -> (%s)" % (id,
            result))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        if ret == E_TUXOSL_NOERROR:
            return result
        else:
            return "UNDEFINED"

    # --------------------------------------------------------------------------
    # Set the level of the internal logger of the libtuxdriver library.
    # --------------------------------------------------------------------------
    def SetLogLevel(self, level = LOG_LEVEL_INFO):
        """Set the level of the internal logger of the libtuxdriver library.
        @param level: (LOG_LEVEL_DEBUG|LOG_LEVEL_INFO|LOG_LEVEL_WARNING
                      LOG_LEVEL_ERROR|LOG_LEVEL_NONE)
        """
        self.__logger.setLevel(level)

    # --------------------------------------------------------------------------
    # Get the state of a status.
    # --------------------------------------------------------------------------
    def GetStatusState(self, id = 0):
        """Get the state of a status.
        @param id: Identifier of the status.
        @return: The state of the status or "UNDEFINED".
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return "UNDEFINED"

        result = " " * 256
        ret = self.tux_osl_lib.TuxOSL_GetStatusState(c_int(id),
            c_char_p(result))
        result = result.replace(" ", "")

        self.__logger.logDebug("Get status state : (%d) -> (%s)" % (id,
            result))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        if ret == E_TUXOSL_NOERROR:
            return result
        else:
            return "UNDEFINED"

    # --------------------------------------------------------------------------
    # Get the value of a status.
    # --------------------------------------------------------------------------
    def GetStatusValue(self, id = 0):
        """Get the value of a status.
        @param id: Identifier of the status.
        @return: The value of the status or "UNDEFINED".
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return "UNDEFINED"

        result = " " * 256
        ret = self.tux_osl_lib.TuxOSL_GetStatusValue(c_int(id),
            c_char_p(result))
        result = result.replace(" ", "")

        self.__logger.logDebug("Get status value : (%d) -> (%s)" % (id,
            result))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        if ret == E_TUXOSL_NOERROR:
            return result
        else:
            return "UNDEFINED"

    # --------------------------------------------------------------------------
    # Get the state of all statuses.
    # --------------------------------------------------------------------------
    def GetAllStatusState(self):
        """Get the state of all statuses.
        @return: The state of all statuses.
        """
        if (self.tux_osl_lib == None) or not self.getStarted():
            return ""

        result = " " * 8182
        self.tux_osl_lib.TuxOSL_GetAllStatusState(c_char_p(result))
        result = result.replace(" ", "")

        self.__logger.logDebug("Get all statuses state : -->")
        for line in result.split("\n"):
            self.__logger.logDebug(line)

        return result

    # --------------------------------------------------------------------------
    # Tokenize the state of a status.
    # --------------------------------------------------------------------------
    def TokenizeStatus(self, status = ""):
        """Tokenize the state of a status.
        @param status: The state of the status.
        @return: A tokens list.
        """
        if self.tux_osl_lib == None:
            return []

        result = status.split(":")
        if len(result) == 1:
            if result[0] == '':
                result = []
        return result

    # --------------------------------------------------------------------------
    # Get the structure of a status.
    # --------------------------------------------------------------------------
    def GetStatusStruct(self, status = ""):
        """Get the structure of a status.
        @param status: The state of the status.
        @return: The structure of a status.
        """
        result = {
            'name' : "None",
            'value' : None,
            'delay' : 0.0,
            'type' : 'string'
        }

        if self.tux_osl_lib == None:
            return result

        status_s = self.TokenizeStatus(status)
        if len(status_s) != 4:
            self.__logger.logError("Error in status structure : (%s)" % status)
            return result

        result['name'] = status_s[0]
        result['delay'] = status_s[3]
        result['type'] = status_s[1]

        if status_s[1] in ['uint8', 'int8', 'int', 'float', 'bool']:
            result['value'] = eval(status_s[2])
        elif status_s[1] == 'string':
            result['value'] = status_s[2]

        return result

    # --------------------------------------------------------------------------
    # Get the explanation of an error code.
    # --------------------------------------------------------------------------
    def StrError(self, error_code):
        """Get the explanation of an error code.
        @param error_code: Error code.
        @return: The explanation as String.
        """
        if self.tux_osl_lib == None:
            return "Shared library not found"

        if not self.getStarted():
            return "Tuxosl is not started"

        result = self.tux_osl_lib.TuxOSL_StrError(c_int(error_code))

        return c_char_p(result).value
