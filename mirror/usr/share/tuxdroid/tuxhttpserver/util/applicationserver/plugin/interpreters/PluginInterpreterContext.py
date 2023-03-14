#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

# ------------------------------------------------------------------------------
# PluginInterpreterContext class.
# ------------------------------------------------------------------------------
class PluginInterpreterContext(object):
    """PluginInterpreterContext class.
    """

    # --------------------------------------------------------------------------
    # Contructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, interpreterClass, interpreterExecution):
        """Contructor of the class.
        @param parent: Parent plugin.
        @param interpreterClass: Interpreter class.
        @param interpreterExecution: Interpreter execution.
        """
        self.__parentPlugin = parent
        self.__pluginInterpreter = interpreterClass()
        self.__pluginInterpreter.setOnPluginStartedCallback(self.__onInterpreterStarted)
        self.__pluginInterpreter.setOnPluginStoppedCallback(self.__onInterpreterStopped)
        self.__pluginInterpreter.setOnNotificationThrowedCallback(self.__onInterpreterNotification)
        self.__pluginInterpreter.setWorkingPath(self.__parentPlugin.getWorkingPath())
        self.__pluginInterpreter.setExecutable(interpreterExecution)
        self.__pluginInterpreter.setSplashScreen(self.__parentPlugin.getDescription().getSplashScreenFile())
        self.__pluginInstanceParameters = {}
        self.__pluginInstanceCommand = ""
        self.__pluginInstanceIsDaemon = False
        # Callbacks
        self.__onPluginNotificationCallback = None
        self.__onPluginMessageCallback = None
        self.__onPluginErrorCallback = None
        self.__onPluginTraceCallback = None
        self.__onPluginResultCallback = None
        self.__onPluginActuationCallback = None
        self.__onPluginStartingCallback = None
        self.__onPluginStoppedCallback = None

    # --------------------------------------------------------------------------
    # Set the instance parameters.
    # --------------------------------------------------------------------------
    def setInstanceParameters(self, parameters):
        """Set the instance parameters.
        @param parameters: Parameters as dictionary.
        """
        self.__pluginInstanceParameters = parameters
        self.__pluginInterpreter.setParameters(parameters)

    # --------------------------------------------------------------------------
    # Get the instance parameters.
    # --------------------------------------------------------------------------
    def getInstanceParameters(self):
        """Get the instance parameters.
        @return: A dictionary.
        """
        return self.__pluginInstanceParameters

    # --------------------------------------------------------------------------
    # Get the parent plugin.
    # --------------------------------------------------------------------------
    def getParentPlugin(self):
        """Get the parent plugin.
        @return: A Plugin object.
        """
        return self.__parentPlugin

    # --------------------------------------------------------------------------
    # Get the host uuid.
    # --------------------------------------------------------------------------
    def getHostUuid(self):
        """Get the host uuid.
        @return: A string.
        """
        if self.__pluginInstanceParameters.has_key('uuid'):
            return self.__pluginInstanceParameters['uuid']
        else:
            return self.__parentPlugin.getDescription().getUuid()

    # --------------------------------------------------------------------------
    # Set the instance command name.
    # --------------------------------------------------------------------------
    def setInstanceCommandName(self, command):
        """Set the instance command name.
        @param command: Command name.
        """
        self.__pluginInstanceCommand = command

    # --------------------------------------------------------------------------
    # Get the instance command name.
    # --------------------------------------------------------------------------
    def getInstanceCommandName(self):
        """Get the instance command name.
        @return: A string.
        """
        return self.__pluginInstanceCommand

    # --------------------------------------------------------------------------
    # Set if the instance is a daemon or not.
    # --------------------------------------------------------------------------
    def setInstanceIsDaemon(self, isDaemon):
        """Set if the instance is a daemon or not.
        @param isDaemon: Is daemon or not.
        """
        self.__pluginInstanceIsDaemon = isDaemon

    # --------------------------------------------------------------------------
    # Get if the instance is a daemon or not.
    # --------------------------------------------------------------------------
    def instanceIsDaemon(self):
        """Get if the instance is a daemon or not.
        @return: A boolean.
        """
        return self.__pluginInstanceIsDaemon

    # --------------------------------------------------------------------------
    # Execute the interpreter.
    # --------------------------------------------------------------------------
    def run(self):
        """Execute the interpreter.
        """
        self.__pluginInterpreter.run(self.__pluginInstanceCommand,
            self.__pluginInstanceIsDaemon)

    # --------------------------------------------------------------------------
    # Abort the execution of the interpreter.
    # --------------------------------------------------------------------------
    def abort(self):
        """Abort the execution of the interpreter.
        """
        self.__pluginInterpreter.abort()

    # --------------------------------------------------------------------------
    # Send event to the plugin. (Daemon mode)
    # --------------------------------------------------------------------------
    def sendEvent(self, eventName, eventValues = []):
        """Send event to the plugin. (Daemon mode)
        @eventName: Event name.
        @eventValues: Event values list.
        """
        self.__pluginInterpreter.sendEvent(eventName, eventValues)

    # --------------------------------------------------------------------------
    # Get if the interpreter run or not.
    # --------------------------------------------------------------------------
    def isRun(self):
        """Get if the interpreter run or not.
        @return: A boolean.
        """
        return self.__pluginInterpreter.isRun()

    # --------------------------------------------------------------------------
    # Set the plugin notification event callback.
    # --------------------------------------------------------------------------
    def setOnPluginNotificationCallback(self, funct):
        """Set the plugin notification event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginNotification(pluginInterpreterContext, messageId, *args):
            pass
        """
        self.__onPluginNotificationCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin message event callback.
    # --------------------------------------------------------------------------
    def setOnPluginMessageCallback(self, funct):
        """Set the plugin message event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginMessage(pluginInterpreterContext, message):
            pass
        """
        self.__onPluginMessageCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin error event callback.
    # --------------------------------------------------------------------------
    def setOnPluginErrorCallback(self, funct):
        """Set the plugin error event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginError(pluginInterpreterContext, *messagesList):
            pass
        """
        self.__onPluginErrorCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin trace event callback.
    # --------------------------------------------------------------------------
    def setOnPluginTraceCallback(self, funct):
        """Set the plugin trace event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginTrace(pluginInterpreterContext, *messagesList):
            pass
        """
        self.__onPluginTraceCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin result event callback.
    # --------------------------------------------------------------------------
    def setOnPluginResultCallback(self, funct):
        """Set the plugin result event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginResult(pluginInterpreterContext, pluginResult):
            pass
        """
        self.__onPluginResultCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin actuation event callback.
    # --------------------------------------------------------------------------
    def setOnPluginActuationCallback(self, funct):
        """Set the plugin actuation event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginActuation(pluginInterpreterContext, *messagesList):
            pass
        """
        self.__onPluginActuationCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin starting event callback.
    # --------------------------------------------------------------------------
    def setOnPluginStartingCallback(self, funct):
        """Set the plugin starting event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginStarting(pluginInterpreterContext):
            pass
        """
        self.__onPluginStartingCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin stopped event callback.
    # --------------------------------------------------------------------------
    def setOnPluginStoppedCallback(self, funct):
        """Set the plugin stopped event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginStopped(pluginInterpreterContext):
            pass
        """
        self.__onPluginStoppedCallback = funct

    # --------------------------------------------------------------------------
    # Event on plugin interpreter started.
    # --------------------------------------------------------------------------
    def __onInterpreterStarted(self):
        """Event on plugin interpreter started.
        """
        if self.__onPluginStartingCallback != None:
            self.__onPluginStartingCallback(self)

    # --------------------------------------------------------------------------
    # Event on plugin interpreter stopped.
    # --------------------------------------------------------------------------
    def __onInterpreterStopped(self):
        """Event on plugin interpreter stopped.
        """
        if self.__onPluginStoppedCallback != None:
            self.__onPluginStoppedCallback(self)

    # --------------------------------------------------------------------------
    # Event on plugin interpreter notification.
    # --------------------------------------------------------------------------
    def __onInterpreterNotification(self, messageId, *args):
        """Event on plugin interpreter notification.
        @param messageId: Message identifiant as string.
        @param args: Arguments of the notification.
        """
        messageId = messageId.lower()
        if messageId == "message":
            language = self.__pluginInstanceParameters['language']
            if self.__onPluginMessageCallback != None:
                self.__onPluginMessageCallback(self,
                    self.getParentPlugin().tr2(language, *args))
        elif messageId == "trace":
            if self.__onPluginTraceCallback != None:
                self.__onPluginTraceCallback(self, *args)
        elif messageId == "error":
            if self.__onPluginErrorCallback != None:
                self.__onPluginErrorCallback(self, *args)
        elif messageId == "check_result":
            if self.__onPluginResultCallback != None:
                if len(args) > 0:
                    if args[0] == "true":
                        checkResult = True
                    else:
                        checkResult = False
                else:
                    checkResult = False
                self.__onPluginResultCallback(self, checkResult)
        elif messageId == "actuation":
            if self.__onPluginActuationCallback != None:
                self.__onPluginActuationCallback(self, *args)
        else:
            if self.__onPluginNotificationCallback != None:
                self.__onPluginNotificationCallback(self, messageId, *args)
