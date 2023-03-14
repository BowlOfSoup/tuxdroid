# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is a portage of the java package write by "Yoran Brault"
#    "com.kysoh.tuxdroid.gadget.framework.gadget"

import os
import sys
import traceback
import random
import threading
import time

ENVIRONEMENT_PREFIX = "tgp_"

# ------------------------------------------------------------------------------
# This class is the base class helper for builder python plugins.
# ------------------------------------------------------------------------------
class SimplePlugin(object):
    """This class is the base class helper for builder python plugins.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        self.__configuration = None
        self.__command = None
        self.__runMutex = threading.Lock()
        self.__run = False
        self.__stdInThread = None

    # --------------------------------------------------------------------------
    # On plugin stop event. Must be overrided
    # --------------------------------------------------------------------------
    def onPluginStop(self):
        """On plugin stop event. Must be overrided
        """
        pass

    # --------------------------------------------------------------------------
    # On plugin event. Must be overrided
    # --------------------------------------------------------------------------
    def onPluginEvent(self, eventName, eventValues):
        """On plugin event. Must be overrided
        """
        pass

    # --------------------------------------------------------------------------
    # Stop the plugin.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the plugin.
        """
        if self.__stdInThread != None:
            if self.__stdInThread.isAlive():
                self.__stdInThread._Thread__stop()
        self.onPluginStop()
        self.throwNotification("plugin", "exit")

    # --------------------------------------------------------------------------
    # Set the run flag value.
    # --------------------------------------------------------------------------
    def __setRun(self, value):
        """Set the run flag value.
        @param value: Flag value. <True|False>
        """
        self.__runMutex.acquire()
        self.__run = value
        self.__runMutex.release()

    # --------------------------------------------------------------------------
    # Get the run flag value.
    # --------------------------------------------------------------------------
    def __getRun(self):
        """Get the run flag value.
        @return: True or False.
        """
        self.__runMutex.acquire()
        result = self.__run
        self.__runMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Stdin polling loop.
    # --------------------------------------------------------------------------
    def __stdInLoop(self):
        """Stdin polling loop.
        """
        while self.__getRun():
            line = sys.stdin.readline()
            if line.lower().find("stop") == 0:
                self.onPluginStop()
                self.__setRun(False)
            elif line.lower().find("event") == 0:
                sltLine = line.split(":")
                # Get event name
                if len(sltLine) > 1:
                    eventName = sltLine[1]
                    # Get event values
                    eventValues = []
                    if len(sltLine) > 2:
                        for value in sltLine[2:]:
                            eventValues.append(value)
                    # Callback
                    t = threading.Thread(target = self.onPluginEvent,
                        args = (eventName, eventValues))
                    t.start()
            time.sleep(0.1)

    # --------------------------------------------------------------------------
    # Get the configuration object.
    # --------------------------------------------------------------------------
    def configuration(self):
        """Get the configuration object.
        @return: A SimplePluginConfiguration object.
        """
        return self.__configuration

    # --------------------------------------------------------------------------
    # Get the command of the gagdet.
    # --------------------------------------------------------------------------
    def getCommand(self):
        """Get the command of the gagdet.
        @return: A string.
        """
        return self.__command

    # --------------------------------------------------------------------------
    # Set the command of the gagdet.
    # --------------------------------------------------------------------------
    def setCommand(self, command):
        """Set the command of the gagdet.
        @param command: The command of the gagdet.
        """
        self.__command = command

    # --------------------------------------------------------------------------
    # Get if the platform is Windows or not.
    # --------------------------------------------------------------------------
    def isWindows(self):
        """Get if the platform is Windows or not.
        @return: A boolean.
        """
        return os.name == "nt"

    # --------------------------------------------------------------------------
    # Load the environement data to the plugin parameters.
    # --------------------------------------------------------------------------
    def __loadEnvironementData(self):
        """Load the environement data to the plugin parameters.
        """
        if self.__configuration == None:
            return
        # Extract configuration object class names
        baseConfClassName = "_SimplePluginConfiguration"
        confClassName = str(self.__configuration.__class__)
        confClassName = confClassName.split("'")[1].split(".")[1]
        confClassName = "_" + confClassName
        # Filtering the fields of the configuration object
        confFields = dir(self.__configuration)
        filteredFileds = []
        for field in confFields:
            if field.find(baseConfClassName) == 0:
                filteredFileds.append([field[len(baseConfClassName):].lower(),
                    field])
            if field.find(confClassName) == 0:
                filteredFileds.append([field[len(confClassName):].lower(),
                    field])
        # Fill the configuration parameters with the environement values
        self.throwTrace("Loading environement")
        for key in os.environ:
            fKey = key.lower()
            if fKey.find(ENVIRONEMENT_PREFIX) == 0:
                environName = fKey[len(ENVIRONEMENT_PREFIX):]
                for field in filteredFileds:
                    if field[0][2:] == environName:
                        # Get the value in the configuration object
                        paramName = field[1]
                        paramValue = getattr(self.__configuration, paramName)
                        paramType = str(type(paramValue))
                        paramType = paramType.split("'")[1]
                        # Get the value in the os environ
                        environValue = os.environ[key]
                        self.throwTrace("   " + field[0][2:] + ":" + environValue);
                        # Check parameters type
                        if paramType == 'str':
                            pass
                        elif paramType == 'int':
                            try:
                                environValue = int(environValue)
                            except:
                                # Environ value type not match with the parameter
                                self.throwError("", True)
                                continue
                        elif paramType == 'float':
                            try:
                                environValue = float(environValue)
                            except:
                                # Environ value type not match with the parameter
                                self.throwError("", True)
                                continue
                        elif paramType == 'bool':
                            if environValue == "true":
                                environValue = True
                            else:
                                environValue = False
                        else:
                            # Unknow parameter type
                            self.throwError("Unknow parameter type (%s)" % paramType)
                            continue
                        # Set the environment value to the parameter
                        setattr(self.__configuration, paramName, environValue)

    # --------------------------------------------------------------------------
    # Starting point of the plugin.
    # --------------------------------------------------------------------------
    def boot(self, arguments, configuration):
        """Starting point of the plugin.
        @param arguments:
        """
        try:
            if len(arguments) > 0:
                self.__command = arguments[0]
                self.__configuration = configuration
                self.__loadEnvironementData()
                self.__setRun(True)
                if self.__configuration.isDaemon():
                    self.__stdInThread = threading.Thread(
                        target = self.__stdInLoop)
                    self.__stdInThread.start()
                self.start()
                if not self.__configuration.isDaemon():
                    self.onPluginStop()
        except:
            self.throwError("Error on plugin boot", True)

    # --------------------------------------------------------------------------
    # Start method of the plugin. Must be overrided.
    # --------------------------------------------------------------------------
    def start(self):
        """Start method of the plugin. (Must be overrided)
        """
        pass

    # --------------------------------------------------------------------------
    # Get the full path of a file located in the "state" directory of a deployed
    # plugin.
    # --------------------------------------------------------------------------
    def __getStateFile(self, fileName):
        """Get the full path of a file located in the "state" directory of a
        deployed plugin.
        @param fileName: Base file name.
        @return: A full file path.
        """
        path = "states"
        if not os.path.isdir(path):
            try:
                os.makedirs(path)
            except:
                return None
        return os.path.join(path, fileName)

    # --------------------------------------------------------------------------
    # Read a serialized object from a file.
    # --------------------------------------------------------------------------
    def readState(self, fileName):
        """Read a serialized object from a file.
        @param fileName: File name of the serialized object.
        @return: An object or None if fail.
        """
        sessionFile = self.__getStateFile(fileName)
        if sessionFile == None:
            return None
        if not os.path.isfile(sessionFile):
            return None
        try:
            f = open(sessionFile, "r")
            state = eval(f.read())
            f.close()
        except:
            return None
        return state

    # --------------------------------------------------------------------------
    # Write a file with a serialized object.
    # --------------------------------------------------------------------------
    def writeState(self, myObject, fileName):
        """Write a file with a serialized object.
        @param myObject: Object to serialize.
        @param fileName: File name of the serialized object.
        """
        sessionFile = self.__getStateFile(fileName)
        try:
            f = open(sessionFile, "w")
            f.write(str(myObject))
            f.close()
        except:
            pass

    # --------------------------------------------------------------------------
    # Write a pid file.
    # --------------------------------------------------------------------------
    def writePid(self, pid):
        """Write a pid file.
        @param pid: Process id.
        """
        fileName = str(random.random()).replace('.', '') + ".pid"
        sessionFile = self.__getStateFile(fileName)
        try:
            f = open(sessionFile, "w")
            f.write(str(pid))
            f.close()
        except:
            pass

    # --------------------------------------------------------------------------
    # Throw a generic notification to the framework.
    # --------------------------------------------------------------------------
    def throwNotification(self, messageId, *args):
        """Throw a generic notification to the framework.
        @param messageId: Message Id.
        @param args: List of objects.
        """
        stringBuffer = messageId
        for arg in args:
            stringBuffer += " '"
            stringBuffer += str(arg).replace("'", "\\'")
            stringBuffer += "'"
        sys.stdout.write(stringBuffer + "\n")
        sys.stdout.flush()

    # --------------------------------------------------------------------------
    # Throw a message to the framework.
    # --------------------------------------------------------------------------
    def throwMessage(self, content, *args):
        """Throw a message to the framework.
        @param content: Content of the message.
        @param args: Arguments for the message.
        """
        tmp = [content,]
        for arg in args:
            tmp.append(arg)
        self.throwNotification("message", *tmp)

    # --------------------------------------------------------------------------
    # Throw a trace message to the framework.
    # --------------------------------------------------------------------------
    def throwTrace(self, message):
        """Throw a trace message to the framework.
        @param message: Throwed message.
        """
        if not self.__configuration.isTraces():
            return
        self.throwNotification("trace", message)

    # --------------------------------------------------------------------------
    # Throw the result of the "check" command to the framework.
    # --------------------------------------------------------------------------
    def throwResult(self, result):
        """Throw the result of the "check" command to the framework.
        @param result: A boolean.
        """
        if result:
            resultValue = "true"
        else:
            resultValue = "false"
        self.throwNotification("check_result", resultValue)

    # --------------------------------------------------------------------------
    # Throw an actuation to the framework.
    # --------------------------------------------------------------------------
    def throwActuation(self, content, *args):
        """Throw an actuation to the framework.
        @param content: Content of the message.
        @param args: Arguments for the message.
        """
        tmp = [content,]
        for arg in args:
            tmp.append(arg)
        self.throwNotification("actuation", *tmp)

    # --------------------------------------------------------------------------
    # Throw an error message to the plugins server.
    # --------------------------------------------------------------------------
    def throwError(self, message, force = False):
        """Throw an error message to the plugins server.
        @param message: Thowed message if the plugin don't want to be traced.
            - if the plugin is traced, the traceback will be sent instead of the
            message.
        @param force: For to send the traceback. Default False.
        """
        if not force:
            if self.__configuration.isTraces():
                message = self.__formatException()
        else:
            message = self.__formatException()
        message = message.split("\n")
        self.throwNotification("error", *message)

    # --------------------------------------------------------------------------
    # Get the formated traceback of the last exception.
    # --------------------------------------------------------------------------
    def __formatException(self):
        """Get the formated traceback of the last exception.
        @return: A string.
        """
        fList = traceback.format_exception(sys.exc_info()[0],
                    sys.exc_info()[1],
                    sys.exc_info()[2])
        result = ""
        for line in fList:
            result += line
        return result
