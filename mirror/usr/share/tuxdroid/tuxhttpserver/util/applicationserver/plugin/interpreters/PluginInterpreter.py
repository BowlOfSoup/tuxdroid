#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import subprocess
import threading
import time

# ------------------------------------------------------------------------------
# Plugin interpreter class.
# ------------------------------------------------------------------------------
class PluginInterpreter(object):
    """Plugin interpreter class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        self.__shellEnv = {}
        self.__workingPath = None
        self.__executable = None
        self.__runMutex = threading.Lock()
        self.__workMutex = threading.Lock()
        self.__run = False
        self.__process = None
        self.__pid = None
        self.__daemon = False
        self.__splashScreen = None
        self.__onPluginStartedCallback = None
        self.__onPluginStoppedCallback = None
        self.__onNotificationThrowedCallback = None

    # --------------------------------------------------------------------------
    # Prepare the shell commands list.
    # --------------------------------------------------------------------------
    def prepareCommand(self):
        """Prepare the shell commands list.
        Prepare the shell commands list.
        @return: A shell commands as list.
        """
        return []

    # --------------------------------------------------------------------------
    # Set the parameters list which will passed to the plugin through the os
    # environment variables.
    # --------------------------------------------------------------------------
    def setParameters(self, parameters):
        """Set the parameters list which will passed to the plugin through the
        os environment variables.
        @param parameters: Parameters as dictionary.
        """
        self.__shellEnv = {}
        for key in parameters.keys():
            self.__shellEnv[str("tgp_%s" % key)] = str(parameters[key])
        for key in os.environ:
            self.__shellEnv[key] = os.environ[key]

    # --------------------------------------------------------------------------
    # Set the working path (cwd) of the interpreter.
    # --------------------------------------------------------------------------
    def setWorkingPath(self, workingPath):
        """Set the working path (cwd) of the interpreter.
        @param workingPath: Working path.
        """
        self.__workingPath = workingPath

    # --------------------------------------------------------------------------
    # Get the working path (cwd) of the interpreter.
    # --------------------------------------------------------------------------
    def getWorkingPath(self):
        """Get the working path (cwd) of the interpreter.
        @return: A directory path.
        """
        return self.__workingPath

    # --------------------------------------------------------------------------
    # Set the splash screen image.
    # --------------------------------------------------------------------------
    def setSplashScreen(self, splashScreen):
        """Set the splash screen image.
        @param splashScreen: Splash screen image path.
        """
        self.__splashScreen = splashScreen

    # --------------------------------------------------------------------------
    # Get the splash screen image.
    # --------------------------------------------------------------------------
    def getSplashScreen(self):
        """Get the splash screen image.
        @return: A string.
        """
        return self.__splashScreen

    # --------------------------------------------------------------------------
    # Set the executable.
    # --------------------------------------------------------------------------
    def setExecutable(self, executable):
        """Set the executable.
        @param executable: Executable as string.
        """
        self.__executable = executable

    # --------------------------------------------------------------------------
    # Get the executable.
    # --------------------------------------------------------------------------
    def getExecutable(self):
        """Get the executable.
        @return: A string.
        """
        return self.__executable

    # --------------------------------------------------------------------------
    # Set the plugin started event callback.
    # --------------------------------------------------------------------------
    def setOnPluginStartedCallback(self, funct):
        """Set the plugin started event callback.
        @param funct: Function pointer.
        Function prototype:
        def onInterpreterStarted():
            pass
        """
        self.__onPluginStartedCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin stopped event callback.
    # --------------------------------------------------------------------------
    def setOnPluginStoppedCallback(self, funct):
        """Set the plugin stopped event callback.
        @param funct: Function pointer.
        Function prototype:
        def onInterpreterStopped():
            pass
        """
        self.__onPluginStoppedCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin notification event callback.
    # --------------------------------------------------------------------------
    def setOnNotificationThrowedCallback(self, funct):
        """Set the plugin notification event callback.
        @param funct: Function pointer.
        Function prototype:
        def onInterpreterNotification(messageId, *args):
            pass
        """
        self.__onNotificationThrowedCallback = funct

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
    # Get if the interpreter is running or not.
    # --------------------------------------------------------------------------
    def isRun(self):
        """Get if the interpreter is running or not.
        @return: True or False.
        """
        return self.__getRun()

    # --------------------------------------------------------------------------
    # Start the interpreter.
    # --------------------------------------------------------------------------
    def run(self, command, daemon = False):
        """Start the interpreter.
        @param command: Plugin command.
        @param daemon: Is daemon or not.
        """
        self.__workMutex.acquire()
        if self.__getRun():
            self.__workMutex.release()
            return
        self.__setRun(True)
        self.__daemon = daemon
        shellCommand = self.prepareCommand()
        shellCommand.append(command)
        shellEnv = self.__shellEnv
        if self.__daemon:
            shellEnv['tgp_daemon'] = 'true'
        shellCwd = self.__workingPath
        while True:
            try:
                self.__process = subprocess.Popen(
                    shellCommand,
                    stdin = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    stderr = subprocess.STDOUT,
                    cwd = self.__workingPath,
                    env = self.__shellEnv)
                break
            except:
                time.sleep(0.1)
        if os.name == 'nt':
            self.__pid = self.__process._handle
        else:
            self.__pid = self.__process.pid
        t = threading.Thread(target = self.__stdOutLoop)
        t.start()
        time.sleep(0.1)
        self.__workMutex.release()

    # --------------------------------------------------------------------------
    # Abort the current execution of the interpreter.
    # --------------------------------------------------------------------------
    def abort(self):
        """Abort the current execution of the interpreter.
        """
        def killMe():
            if os.name == 'nt':
                import win32api
                try:
                    win32api.TerminateProcess(int(self.__pid), -1)
                except:
                    pass
            else:
                os.system("kill -3 -15 -9 " + str(self.__pid))
        self.__workMutex.acquire()
        if not self.__getRun():
            self.__workMutex.release()
            return
        if self.__daemon:
            try:
                self.__process.stdin.write("STOP\n")
                self.__process.stdin.flush()
            except:
                pass
            timeout = 5.0
            while self.__process.poll() == None:
                timeout -= 0.1
                time.sleep(0.1)
                if timeout <= 0.0:
                    killMe()
                    break
            self.__setRun(False)
            if self.__onPluginStoppedCallback != None:
                self.__onPluginStoppedCallback()
        else:
            killMe()
            self.__setRun(False)
        self.__workMutex.release()

    # --------------------------------------------------------------------------
    # Send event to the plugin. (Daemon mode)
    # --------------------------------------------------------------------------
    def sendEvent(self, eventName, eventValues = []):
        """Send event to the plugin. (Daemon mode)
        @eventName: Event name.
        @eventValues: Event values list.
        """
        if not self.__getRun():
            return
        if not self.__daemon:
            return
        eventString = "event:"
        eventString += eventName
        for value in eventValues:
            eventString += ":" + str(value)
        try:
            self.__process.stdin.write("%s\n" % eventString)
            self.__process.stdin.flush()
        except:
            pass

    # --------------------------------------------------------------------------
    # Loop to handling the stdout messages.
    # --------------------------------------------------------------------------
    def __stdOutLoop(self):
        """Loop to handling the stdout messages.
        """
        if self.__onPluginStartedCallback != None:
            self.__onPluginStartedCallback()
        while self.__getRun():
            line = self.__process.stdout.readline()
            if os.name == 'nt':
                try:
                    tmp = line.decode("latin-1", "ignore")
                    line = tmp.encode("utf-8", "ignore")
                except:
                    pass
            if len(line) == 0:
                self.__setRun(False)
                if self.__onPluginStoppedCallback != None:
                    self.__onPluginStoppedCallback()
            else:
                line = line[:-1]
                if len(line) == 0:
                    continue
                if line[-1] == "\r":
                    line = line[:-1]
                if line.lower().find("plugin") == 0:
                    if line.lower().find("'exit'") != -1:
                        self.abort()
                if self.__getRun():
                    args = line.split(" '")
                    if len(args) > 0:
                        messageId = args.pop(0)
                        for i, arg in enumerate(args):
                            if len(arg) > 0:
                                if arg[-1] == "'":
                                    args[i] = arg[:-1]
                        if self.__onNotificationThrowedCallback != None:
                            self.__onNotificationThrowedCallback(messageId,
                                *args)
        if self.__process != None:
            # Close PIPE's
            try:
                if self.__process.stdin != None:
                    self.__process.stdin.close()
            except:
                pass
            try:
                if self.__process.stdout != None:
                    self.__process.stdout.close()
            except:
                pass
        if os.name != 'nt':
            try:
                # Avoid zombies child process on Linux
                os.wait()
            except:
                pass
