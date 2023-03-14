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

import os
import threading
import time

from util.misc.systemPaths import systemPaths

# Levels
LOG_LEVEL_DEBUG             = 0
LOG_LEVEL_INFO              = 1
LOG_LEVEL_WARNING           = 2
LOG_LEVEL_ERROR             = 3
LOG_LEVEL_NONE              = 4
# Targets
LOG_TARGET_FILE             = 0
LOG_TARGET_SHELL            = 1
LOG_TARGET_BOTH             = 2
LOG_TARGET_NONE             = 3
# Global log file flag
LOG_GLOBAL_FILE             = False

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# Simple logger for python.
# ------------------------------------------------------------------------------
class SimpleLogger(object):
    """Simple logger for python.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, appName, logPath = None):
        """Constructor of the class.
        @param appName: name of the application.
        @param logPath: Output path of the log file.
        """
        self.__level = LOG_LEVEL_ERROR
        self.__target = LOG_TARGET_BOTH

        self.__appName = appName
        # Find the log path
        if (logPath == None) or (not os.path.isdir(logPath)):
            if os.name == 'nt':
                self.__logPath = os.path.join(os.environ['ALLUSERSPROFILE'],
                    "Kysoh", "Tux Droid", "logs")
                if not os.path.isdir(self.__logPath):
                    os.makedirs(self.__logPath)
            else:
                path = systemPaths.getLogPath()
                if not os.path.isdir(path):
                    os.makedirs(path, mode=0755)
                self.__logPath = path
        else:
            self.__logPath = logPath

        self.__logName = "%s.log" % self.__appName
        self.__logFileName = os.path.join(self.__logPath, self.__logName)
        self.__logMutex = threading.Lock()

    # --------------------------------------------------------------------------
    # Get the log file path.
    # --------------------------------------------------------------------------
    def getLogFilePath(self):
        """Get the log file path.
        @return : The path to the log file.
        """
        return self.__logFileName

    # --------------------------------------------------------------------------
    # Set the log level.
    # --------------------------------------------------------------------------
    def setLevel(self, level):
        """Set the log level.
        @param level: (LOG_LEVEL_DEBUG|LOG_LEVEL_INFO|LOG_LEVEL_WARNING
                      LOG_LEVEL_ERROR|LOG_LEVEL_NONE)
        """
        self.__level = level

    # --------------------------------------------------------------------------
    # Set the log target.
    # --------------------------------------------------------------------------
    def setTarget(self, target):
        """Set the log target.
        @param target: (LOG_TARGET_FILE|LOG_TARGET_SHELL|LOG_TARGET_BOTH
                       LOG_TARGET_NONE)
        """
        self.__target = target

    # --------------------------------------------------------------------------
    # Reset the log file.
    # --------------------------------------------------------------------------
    def resetLog(self):
        """Reset the log file.
        """
        try:
            f = open(self.__logFileName, 'w')
            f.close()
        except:
            pass

    # --------------------------------------------------------------------------
    # Reset the global log file.
    # --------------------------------------------------------------------------
    def resetGlobalLogFile(self, activate = True):
        """Reset the global log file.
        """
        global LOG_GLOBAL_FILE
        LOG_GLOBAL_FILE = activate
        if LOG_GLOBAL_FILE:
            try:
                f = open(os.path.join(self.__logPath, "all.log"), 'w')
                f.close()
            except:
                pass

    # --------------------------------------------------------------------------
    # Put a message in the log.
    # --------------------------------------------------------------------------
    def __putLog(self, msgType, msgString):
        """Put a message in the log.
        """
        message = "[%s] at (%s) : %s" % (msgType, self.__getTimeInfo(), msgString)

        if self.__target in [LOG_TARGET_FILE, LOG_TARGET_BOTH]:
            if os.path.isfile(self.__logFileName):
                self.__logMutex.acquire()
                try:
                    f = open(self.__logFileName, 'a')
                    try:
                        f.write(message + "\n")
                    finally:
                        f.close()
                except:
                    pass
                if LOG_GLOBAL_FILE:
                    try:
                        f = open(os.path.join(self.__logPath, "all.log"), 'a')
                        try:
                            f.write(message + "\n")
                        finally:
                            f.close()
                    except:
                        pass
                self.__logMutex.release()
        if self.__target in [LOG_TARGET_SHELL, LOG_TARGET_BOTH]:
            print message

    # --------------------------------------------------------------------------
    # Get the current time.
    # --------------------------------------------------------------------------
    def __getTimeInfo(self):
        """Get the current time.
        """
        now = time.localtime()
        timeInfo = "%.4d/%.2d/%.2d %.2d:%.2d:%.2d" % (now[0], now[1], now[2],
            now[3], now[4], now[5])
        return timeInfo

    # --------------------------------------------------------------------------
    # Insert an error message in the log file.
    # --------------------------------------------------------------------------
    def logError(self, message):
        """Insert an error message in the log file.
        @param message: message to log.
        """
        if self.__level > LOG_LEVEL_ERROR:
            return
        self.__putLog("Error", message)

    # --------------------------------------------------------------------------
    # Insert a warning message in the log file.
    # --------------------------------------------------------------------------
    def logWarning(self, message):
        """Insert a warning message in the log file.
        @param message: message to log.
        """
        if self.__level > LOG_LEVEL_WARNING:
            return
        self.__putLog("Warning", message)

    # --------------------------------------------------------------------------
    # Insert an info message in the log file.
    # --------------------------------------------------------------------------
    def logInfo(self, message):
        """Insert an info message in the log file.
        @param message: message to log.
        """
        if self.__level > LOG_LEVEL_INFO:
            return
        self.__putLog("Info", message)

    # --------------------------------------------------------------------------
    # Insert a debug message in the log file.
    # --------------------------------------------------------------------------
    def logDebug(self, message):
        """Insert a debug message in the log file.
        @param message: message to log.
        """
        if self.__level > LOG_LEVEL_DEBUG:
            return
        self.__putLog("Debug", message)
