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
E_TUXDRV_BEGIN                      = 256
E_TUXDRV_NOERROR                    = 0
E_TUXDRV_PARSERISDISABLED           = E_TUXDRV_BEGIN
E_TUXDRV_INVALIDCOMMAND             = E_TUXDRV_BEGIN + 1
E_TUXDRV_STACKOVERFLOW              = E_TUXDRV_BEGIN + 2
E_TUXDRV_FILEERROR                  = E_TUXDRV_BEGIN + 3
E_TUXDRV_BADWAVFILE                 = E_TUXDRV_BEGIN + 4
E_TUXDRV_INVALIDIDENTIFIER          = E_TUXDRV_BEGIN + 5
E_TUXDRV_INVALIDNAME                = E_TUXDRV_BEGIN + 6
E_TUXDRV_INVALIDPARAMETER           = E_TUXDRV_BEGIN + 7
E_TUXDRV_BUSY                       = E_TUXDRV_BEGIN + 8
E_TUXDRV_WAVSIZEEXCEDED             = E_TUXDRV_BEGIN + 9

# Identifiers list of the statuses
SW_ID_FLIPPERS_POSITION             = 0
SW_ID_FLIPPERS_REMAINING_MVM        = 1
SW_ID_SPINNING_DIRECTION            = 2
SW_ID_SPINNING_REMAINING_MVM        = 3
SW_ID_LEFT_WING_BUTTON              = 4
SW_ID_RIGHT_WING_BUTTON             = 5
SW_ID_HEAD_BUTTON                   = 6
SW_ID_REMOTE_BUTTON                 = 7
SW_ID_MOUTH_POSITION                = 8
SW_ID_MOUTH_REMAINING_MVM           = 9
SW_ID_EYES_POSITION                 = 10
SW_ID_EYES_REMAINING_MVM            = 11
SW_ID_DESCRIPTOR_COMPLETE           = 12
SW_ID_RF_STATE                      = 13
SW_ID_DONGLE_PLUG                   = 14
SW_ID_CHARGER_STATE                 = 15
SW_ID_BATTERY_LEVEL                 = 16
SW_ID_BATTERY_STATE                 = 17
SW_ID_LIGHT_LEVEL                   = 18
SW_ID_LEFT_LED_STATE                = 19
SW_ID_RIGHT_LED_STATE               = 20
SW_ID_CONNECTION_QUALITY            = 21
SW_ID_AUDIO_FLASH_PLAY              = 22
SW_ID_AUDIO_GENERAL_PLAY            = 23
SW_ID_FLASH_PROG_CURR_TRACK         = 24
SW_ID_FLASH_PROG_LAST_TRACK_SIZE    = 25
SW_ID_TUXCORE_SYMBOLIC_VERSION      = 26
SW_ID_TUXAUDIO_SYMBOLIC_VERSION     = 27
SW_ID_FUXUSB_SYMBOLIC_VERSION       = 28
SW_ID_FUXRF_SYMBOLIC_VERSION        = 29
SW_ID_TUXRF_SYMBOLIC_VERSION        = 30
SW_ID_DRIVER_SYMBOLIC_VERSION       = 31
SW_ID_SOUND_REFLASH_BEGIN           = 32
SW_ID_SOUND_REFLASH_END             = 33
SW_ID_SOUND_REFLASH_CURRENT_TRACK   = 34
SW_ID_EYES_MOTOR_ON                 = 35
SW_ID_MOUTH_MOTOR_ON                = 36
SW_ID_FLIPPERS_MOTOR_ON             = 37
SW_ID_SPIN_LEFT_MOTOR_ON            = 38
SW_ID_SPIN_RIGHT_MOTOR_ON           = 39
SW_ID_FLASH_SOUND_COUNT             = 40

# Names list of the statuses
ST_NAME_HEAD_BUTTON                 = 'head_button'
ST_NAME_LEFT_BUTTON                 = 'left_wing_button'
ST_NAME_RIGHT_BUTTON                = 'right_wing_button'
ST_NAME_REMOTE_BUTTON               = 'remote_button'
ST_NAME_MOUTH_POSITION              = 'mouth_position'
ST_NAME_MOUTH_RM                    = 'mouth_remaining_movements'
ST_NAME_EYES_POSITION               = 'eyes_position'
ST_NAME_EYES_RM                     = 'eyes_remaining_movements'
ST_NAME_FLIPPERS_POSITION           = 'flippers_position'
ST_NAME_FLIPPERS_RM                 = 'flippers_remaining_movements'
ST_NAME_SPINNING_DIRECTION          = 'spinning_direction'
ST_NAME_SPINNING_RM                 = 'spinning_remaining_movements'
ST_NAME_DONGLE_PLUG                 = 'dongle_plug'
ST_NAME_RADIO_STATE                 = 'radio_state'
ST_NAME_LEFT_LED                    = 'left_led_state'
ST_NAME_RIGHT_LED                   = 'right_led_state'
ST_NAME_CONNECTION_QUALITY          = 'connection_quality'
ST_NAME_AUDIO_FLASH_PLAY            = 'audio_flash_play'
ST_NAME_FLASH_PROG_END              = 'sound_reflash_end'
ST_NAME_EYES_MOTOR_ON               = 'eyes_motor_on'
ST_NAME_MOUTH_MOTOR_ON              = 'mouth_motor_on'
ST_NAME_FLIPPERS_MOTOR_ON           = 'flippers_motor_on'
ST_NAME_SPIN_LEFT_MOTOR_ON          = 'spin_left_motor_on'
ST_NAME_SPIN_RIGHT_MOTOR_ON         = 'spin_right_motor_on'
ST_NAME_DRIVER_SYMB_VER             = 'driver_symbolic_version'
ST_NAME_TUXCORE_SYMB_VER            = 'tuxcore_symbolic_version'
ST_NAME_TUXAUDIO_SYMB_VER           = 'tuxaudio_symbolic_version'
ST_NAME_FUXUSB_SYMB_VER             = 'fuxusb_symbolic_version'
ST_NAME_FUXRF_SYMB_VER              = 'fuxrf_symbolic_version'
ST_NAME_TUXRF_SYMB_VER              = 'tuxrf_symbolic_version'
ST_NAME_FLASH_SOUND_COUNT           = 'sound_flash_count'
ST_NAME_BATTERY_LEVEL               = 'battery_level'
ST_NAME_BATTERY_STATE               = 'battery_state'
ST_NAME_CHARGER_STATE               = 'charger_state'
ST_NAME_LIGHT_LEVEL                 = 'light_level'
ST_NAME_DESCRIPTOR_COMPLETE         = 'descriptor_complete'
ST_NAME_AUDIO_GENERAL_PLAY          = 'audio_general_play'
ST_NAME_FLASH_PROG_CURRENT_TRACK    = 'flash_programming_current_track'
ST_NAME_FLASH_PROG_LAST_TRACK_SIZE  = 'flash_programming_current_track'
ST_NAME_FLASH_PROG_BEGIN            = 'sound_reflash_begin'
SW_NAME_DRIVER = [
    ST_NAME_FLIPPERS_POSITION,
    ST_NAME_FLIPPERS_RM,
    ST_NAME_SPINNING_DIRECTION,
    ST_NAME_SPINNING_RM,
    ST_NAME_LEFT_BUTTON,
    ST_NAME_RIGHT_BUTTON,
    ST_NAME_HEAD_BUTTON,
    ST_NAME_REMOTE_BUTTON,
    ST_NAME_MOUTH_POSITION,
    ST_NAME_MOUTH_RM,
    ST_NAME_EYES_POSITION,
    ST_NAME_EYES_RM,
    ST_NAME_DESCRIPTOR_COMPLETE,
    ST_NAME_RADIO_STATE,
    ST_NAME_DONGLE_PLUG,
    ST_NAME_CHARGER_STATE,
    ST_NAME_BATTERY_LEVEL,
    ST_NAME_BATTERY_STATE,
    ST_NAME_LIGHT_LEVEL,
    ST_NAME_LEFT_LED,
    ST_NAME_RIGHT_LED,
    ST_NAME_CONNECTION_QUALITY,
    ST_NAME_AUDIO_FLASH_PLAY,
    ST_NAME_AUDIO_GENERAL_PLAY,
    ST_NAME_FLASH_PROG_CURRENT_TRACK,
    ST_NAME_FLASH_PROG_LAST_TRACK_SIZE,
    ST_NAME_TUXCORE_SYMB_VER,
    ST_NAME_TUXAUDIO_SYMB_VER,
    ST_NAME_FUXUSB_SYMB_VER,
    ST_NAME_FUXRF_SYMB_VER,
    ST_NAME_TUXRF_SYMB_VER,
    ST_NAME_DRIVER_SYMB_VER,
    ST_NAME_FLASH_PROG_CURRENT_TRACK,
    ST_NAME_FLASH_PROG_BEGIN,
    ST_NAME_FLASH_PROG_END,
    ST_NAME_EYES_MOTOR_ON,
    ST_NAME_MOUTH_MOTOR_ON,
    ST_NAME_FLIPPERS_MOTOR_ON,
    ST_NAME_SPIN_LEFT_MOTOR_ON,
    ST_NAME_SPIN_RIGHT_MOTOR_ON,
    ST_NAME_FLASH_SOUND_COUNT,
]

# Log levels
LOG_LEVEL_DEBUG             = 0
LOG_LEVEL_INFO              = 1
LOG_LEVEL_WARNING           = 2
LOG_LEVEL_ERROR             = 3
LOG_LEVEL_NONE              = 4

# Log targets
LOG_TARGET_TUX              = 0
LOG_TARGET_SHELL            = 1

# Callback type defines
TUX_DRIVER_STATUS_CALLBACK = CFUNCTYPE(None, c_char_p)
TUX_DRIVER_SIMPLE_CALLBACK = CFUNCTYPE(None)

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# libtuxdriver wrapper class.
# ------------------------------------------------------------------------------
class TuxDrv(object):
    """Tuxdriver wrapper class.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, library_path = None):
        """Constructor.
        @param library_path: Path of libtuxdriver library. (Default None)
        """
        self.__logger = SimpleLogger("libtuxdriver_wrapper")
        self.__logger.setTarget(LOG_TARGET_FILE)
        self.__logger.setLevel(LOG_LEVEL_INFO)
        self.__logger.resetLog()
        self.__logger.logInfo("-----------------------------------------------")
        self.__logger.logInfo("libtuxdriver wrapper v%s" % __version__)
        self.__logger.logInfo("Author : %s" % __author__)
        self.__logger.logInfo("Licence : %s" % __licence__)
        self.__logger.logInfo("-----------------------------------------------")
        if library_path == None:
            mPath, mFile = os.path.split(__file__)
            if os.name == 'nt':
                library_path = os.path.join(mPath, "libtuxdriver.dll")
            else:
                library_path = os.path.join(mPath, "libtuxdriver.so")
        self.__logger.logInfo("Libtuxdriver path : (%s)" % library_path)
        self.__callback_container = []
        self.tux_driver_lib = None
        if os.path.isfile(library_path):
            try:
                self.tux_driver_lib = CDLL(library_path)
                self.__logger.logInfo("The shared library was found.")
            except:
                self.tux_driver_lib = None
                txt = "Error on handling the library in your application."
                self.__logger.logError(txt)
        else:
            txt = "Path (%s) not found !" % library_path
            self.__logger.logError(txt)
            txt = "The shared library was not handled in your application."
            self.__logger.logError(txt)

    # --------------------------------------------------------------------------
    # Register a callback function to the "status" event.
    # --------------------------------------------------------------------------
    def SetStatusCallback(self, funct = None):
        """Register a callback function to the "status" event.
        @param funct: Pointer to the function.
        """
        if self.tux_driver_lib == None:
            return

        if funct == None:
            return

        cb = TUX_DRIVER_STATUS_CALLBACK(funct)
        self.__callback_container.append(cb)
        self.tux_driver_lib.TuxDrv_SetStatusCallback(cb)
        return

    # --------------------------------------------------------------------------
    # Register a callback function to the "end of cycle" event.
    # --------------------------------------------------------------------------
    def SetEndCycleCallback(self, funct = None):
        """Register a callback function to the "end of cycle" event.
        @param funct: Pointer to the function.
        """
        if self.tux_driver_lib == None:
            return

        if funct == None:
            return

        cb = TUX_DRIVER_SIMPLE_CALLBACK(funct)
        self.__callback_container.append(cb)
        self.tux_driver_lib.TuxDrv_SetEndCycleCallback(cb)
        return

    # --------------------------------------------------------------------------
    # Register a callback function to the "dongle connected" event.
    # --------------------------------------------------------------------------
    def SetDongleConnectedCallback(self, funct = None):
        """Register a callback function to the "dongle connected" event.
        @param funct: Pointer to the function.
        """
        if self.tux_driver_lib == None:
            return

        if funct == None:
            return

        cb = TUX_DRIVER_SIMPLE_CALLBACK(funct)
        self.__callback_container.append(cb)
        self.tux_driver_lib.TuxDrv_SetDongleConnectedCallback(cb)
        return

    # --------------------------------------------------------------------------
    # Register a callback function to the "dongle disconnected" event.
    # --------------------------------------------------------------------------
    def SetDongleDisconnectedCallback(self, funct = None):
        """Register a callback function to the "dongle disconnected" event.
        @param funct: Pointer to the function.
        """
        if self.tux_driver_lib == None:
            return

        if funct == None:
            return

        cb = TUX_DRIVER_SIMPLE_CALLBACK(funct)
        self.__callback_container.append(cb)
        self.tux_driver_lib.TuxDrv_SetDongleDisconnectedCallback(cb)
        return

    # --------------------------------------------------------------------------
    # Start libtuxdriver.
    # --------------------------------------------------------------------------
    def Start(self):
        """Start libtuxdriver.
        """
        if self.tux_driver_lib == None:
            return

        self.__logger.logInfo("Start the library.")
        self.tux_driver_lib.TuxDrv_Start()
        self.__logger.logInfo("The library has been stopped.")

    # --------------------------------------------------------------------------
    # Stop libtuxdriver.
    # --------------------------------------------------------------------------
    def Stop(self):
        """Stop libtuxdriver.
        """
        if self.tux_driver_lib == None:
            return

        self.__logger.logInfo("Stop the library.")
        self.tux_driver_lib.TuxDrv_Stop()

    # --------------------------------------------------------------------------
    # Get the log file path.
    # --------------------------------------------------------------------------
    def getLogFilePath(self):
        """Get the log file path.
        @return: The log file path.
        """
        return self.__logger.getLogFilePath()

    # --------------------------------------------------------------------------
    # Perform a command through libtuxdriver.
    # --------------------------------------------------------------------------
    def PerformCommand(self, delay, command):
        """Perform a command through libtuxdriver.
        @param delay: Delay before the command execution.
        @param command: Command to execute.
        @return: The success of the command performing.
        """
        if self.tux_driver_lib == None:
            return E_TUXDRV_PARSERISDISABLED

        try:
            ret = self.tux_driver_lib.TuxDrv_PerformCommand(c_double(delay),
                    c_char_p(command))
        except:
            ret = E_TUXDRV_NOERROR

        self.__logger.logDebug("Perform the cmd : cmd(%s) delay (%f)" % \
            (command, delay))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        return ret

    # --------------------------------------------------------------------------
    # Perform the content of a macro commands file through libtuxdriver.
    # --------------------------------------------------------------------------
    def PerformMacroFile(self, file_path = ""):
        """Perform the content of a macro commands file through libtuxdriver.
        @param file_path: Macro commands file path.
        @return: The success of the performing.
        """
        if self.tux_driver_lib == None:
            return E_TUXDRV_PARSERISDISABLED

        ret = self.tux_driver_lib.TuxDrv_PerformMacroFile(c_char_p(file_path))

        self.__logger.logDebug("Perform a macro : path(%s)" % file_path)
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        return ret

    # --------------------------------------------------------------------------
    # Perform a macro commands through libtuxdriver.
    # --------------------------------------------------------------------------
    def PerformMacroText(self, macro = ""):
        """Perform a macro commands through libtuxdriver.
        @param macro: Macro commands text.
        @return: The success of the performing.
        """
        if self.tux_driver_lib == None:
            return E_TUXDRV_PARSERISDISABLED

        ret = self.tux_driver_lib.TuxDrv_PerformMacroText(c_char_p(macro))

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
        if self.tux_driver_lib == None:
            return

        self.tux_driver_lib.TuxDrv_ClearCommandStack()

        self.__logger.logDebug("Clear the commands stack")

        return

    # --------------------------------------------------------------------------
    # Write a tracks list in the sound flash memory.
    # --------------------------------------------------------------------------
    def SoundReflash(self, tracks = ""):
        """Write a tracks list in the sound flash memory.
        @param tracks: Tracks list.
        @return: The success of the writing.
        """
        if self.tux_driver_lib == None:
            return E_TUXDRV_BUSY

        ret = self.tux_driver_lib.TuxDrv_SoundReflash(c_char_p(tracks))

        self.__logger.logDebug("Sound refash : -->")
        for line in tracks.split("\n"):
            self.__logger.logDebug(line)
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        return ret

    # --------------------------------------------------------------------------
    # Get the identifier of a status.
    # --------------------------------------------------------------------------
    def GetStatusId(self, name = "battery_level"):
        """Get the identifier of a status.
        @param name: Status name.
        @return: The identifier as Integer.
        """
        if self.tux_driver_lib == None:
            return -1

        idc = c_int(0)
        idcp = pointer(idc)
        ret = self.tux_driver_lib.TuxDrv_GetStatusId(c_char_p(name), idcp)

        self.__logger.logDebug("Get status id : (%s) -> (%d)" % (name,
            idc.value))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        if ret != E_TUXDRV_NOERROR:
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
        if self.tux_driver_lib == None:
            return "UNDEFINED"

        result = " " * 256
        ret = self.tux_driver_lib.TuxDrv_GetStatusName(c_int(id),
            c_char_p(result))
        result = result.replace(" ", "")

        self.__logger.logDebug("Get status name : (%d) -> (%s)" % (id,
            result))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        if ret == E_TUXDRV_NOERROR:
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
        if self.tux_driver_lib == None:
            return

        self.tux_driver_lib.TuxDrv_SetLogLevel(c_uint8(level))
        self.__logger.setLevel(level)

    # --------------------------------------------------------------------------
    # Set the target of the internal logger of the libtuxdriver library.
    # --------------------------------------------------------------------------
    def SetLogTarget(self, target = LOG_TARGET_SHELL):
        """Set the target of the internal logger of the libtuxdriver library.
        @param target: (LOG_TARGET_TUX|LOG_TARGET_SHELL)
        """
        if self.tux_driver_lib == None:
            return

        self.tux_driver_lib.TuxDrv_SetLogTarget(c_uint8(target))

    # --------------------------------------------------------------------------
    # Get the state of a status.
    # --------------------------------------------------------------------------
    def GetStatusState(self, id = 0):
        """Get the state of a status.
        @param id: Identifier of the status.
        @return: The state of the status or "UNDEFINED".
        """
        if self.tux_driver_lib == None:
            return "UNDEFINED"

        result = " " * 256
        ret = self.tux_driver_lib.TuxDrv_GetStatusState(c_int(id),
            c_char_p(result))
        result = result.replace(" ", "")

        self.__logger.logDebug("Get status state : (%d) -> (%s)" % (id,
            result))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        if ret == E_TUXDRV_NOERROR:
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
        if self.tux_driver_lib == None:
            return "UNDEFINED"

        result = " " * 256
        ret = self.tux_driver_lib.TuxDrv_GetStatusValue(c_int(id),
            c_char_p(result))
        result = result.replace(" ", "")

        self.__logger.logDebug("Get status value : (%d) -> (%s)" % (id,
            result))
        self.__logger.logDebug("Returned : code(%s) expl(%s)" % (str(ret),
            self.StrError(ret)))

        if ret == E_TUXDRV_NOERROR:
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
        if self.tux_driver_lib == None:
            return ""

        result = " " * 8182
        self.tux_driver_lib.TuxDrv_GetAllStatusState(c_char_p(result))
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
        if self.tux_driver_lib == None:
            return []

        result = status.split(":")
        if len(result) == 1:
            if result[0] == '':
                result = []
        return result

    # --------------------------------------------------------------------------
    # Reset the motor positions of Tux.
    # --------------------------------------------------------------------------
    def ResetPositions(self):
        """Reset the motor positions of Tux.
        """
        if self.tux_driver_lib == None:
            return

        try:
            self.tux_driver_lib.TuxDrv_ResetPositions()
        except:
            pass

        self.__logger.logDebug("Reset the motor positions.")

        return

    # --------------------------------------------------------------------------
    # Reset the dongle state.
    # --------------------------------------------------------------------------
    def ResetDongle(self):
        """Reset the dongle state.
        """
        if self.tux_driver_lib == None:
            return

        self.tux_driver_lib.TuxDrv_ResetDongle()

        self.__logger.logDebug("Reset the dongle.")

        return

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

        if self.tux_driver_lib == None:
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
        if self.tux_driver_lib == None:
            return "Shared library not found"

        ### BUG : ###################################################################
        # On Linux 64 bits, this function line crash the API.
        #
        # I don't know why, but the function c_char_p with the value retourned
        # by the driver cause a segmentation fault on 64bits OS.
        #
        ##########

        result = self.tux_driver_lib.TuxDrv_StrError(c_int(error_code))

        # BUG : # return c_char_p(result).value
        return 0
