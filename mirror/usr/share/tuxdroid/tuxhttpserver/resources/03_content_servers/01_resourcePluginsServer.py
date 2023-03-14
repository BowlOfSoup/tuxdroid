# ==============================================================================
# Plugin server resource.
# ==============================================================================

from util.applicationserver.plugin.PluginsContainer import PluginsContainer
from util.applicationserver.plugin.Plugin import SUPPORTED_LANGUAGES_LIST
from util.misc.tuxPaths import TUXDROID_LANGUAGE
from util.misc.tuxPaths import TUXDROID_DEFAULT_LOCUTOR
from util.logger.SimpleLogger import *

# Plugins server events/statuses
ST_NAME_PS_CONTAINER_DEPLOYED = "plugins_server_container_deployed"
ST_NAME_PS_CONTAINER_ERROR = "plugins_server_container_error"
ST_NAME_PS_PLUGIN_LOADED = "plugins_server_plugin_loaded"
ST_NAME_PS_PLUGIN_UNLOADED = "plugins_server_plugin_unloaded"
ST_NAME_PS_PLUGIN_STARTED = "plugins_server_plugin_started"
ST_NAME_PS_PLUGIN_STOPPED = "plugins_server_plugin_stopped"

# Plugins server events/statuses list
SW_NAME_PLUGINS_SERVER = [
    ST_NAME_PS_CONTAINER_DEPLOYED,
    ST_NAME_PS_CONTAINER_ERROR,
    ST_NAME_PS_PLUGIN_LOADED,
    ST_NAME_PS_PLUGIN_UNLOADED,
    ST_NAME_PS_PLUGIN_STARTED,
    ST_NAME_PS_PLUGIN_STOPPED,
]

# ------------------------------------------------------------------------------
# Declaration of the resource "plugins_server".
# ------------------------------------------------------------------------------
class TDSResourcePluginsServer(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "plugins_server"
        self.comment = "Resource to manage the plugins server."
        self.fileName = RESOURCE_FILENAME
        # Create a plugins container
        self.__pluginsContainer = PluginsContainer()
        self.__pluginsContainer.setOnDirectoryDeployedCallback(self.__onDirectoryDeployed)
        self.__pluginsContainer.setOnDirectoryUndeployedCallback(self.__onDirectoryUndeployed)
        self.__pluginsContainer.setOnPluginDeployedCallback(self.__onPluginDeployed)
        self.__pluginsContainer.setOnPluginDeploymentErrorCallback(self.__onPluginDeploymentError)
        self.__pluginsContainer.setOnPluginUndeployedCallback(self.__onPluginUndeployed)
        # Registering the plugins server statuses.
        for statusName in SW_NAME_PLUGINS_SERVER:
            eventsHandler.insert(statusName)
        # Create a logger
        self.logger = SimpleLogger("plugins_server")
        self.logger.resetLog()
        self.logger.setLevel(LOG_LEVEL_DEBUG)
        self.logger.setTarget(TDS_CONF_LOG_TARGET)
        self.logger.logInfo("-----------------------------------------------")
        self.logger.logInfo("Smart-core Plugins Server")
        self.logger.logInfo("Licence : GPL")
        self.logger.logInfo("-----------------------------------------------")
        # Create the plugins locales
        splitedLC = TUXDROID_LANGUAGE.split("_")
        language = splitedLC[0]
        if len(splitedLC) > 1:
            country = splitedLC[1]
        else:
            country = language.upper()
        locutor = TUXDROID_DEFAULT_LOCUTOR
        pitch = 130
        self.logger.logInfo("Set plugins locales [%s:%s:%s:%s]." % (
            language, country, locutor, pitch))
        self.__pluginsContainer.setLocales(language, country, locutor, pitch)
        # Get the plugins path
        pluginsPath = os.path.join(TDS_DEFAULT_CONTENT_PATH, "plugins")
        DirectoriesAndFilesTools.MKDirs(pluginsPath)
        self.logger.logInfo("Add directory in the container [%s]." %\
                pluginsPath)
        self.__pluginsContainer.addDirectory(pluginsPath)
        self.logger.logInfo("Deploy the plugins container.")
        self.__pluginsContainer.deploy()
        self.logger.logInfo("Plugins container is deployed.")

    def stop(self):
        self.logger.logInfo("Undeploy the plugins container")
        self.__pluginsContainer.undeploy()

    # --------------------------------------------------------------------------
    # Plugins container events
    # --------------------------------------------------------------------------

    def __onDirectoryDeployed(self, observerName):
        self.logger.logInfo("Directory deployed [%s]" % observerName)
        self.__publishEvents(True, ST_NAME_PS_CONTAINER_DEPLOYED, ["True",])

    def __onDirectoryUndeployed(self, observerName):
        self.logger.logInfo("Directory undeployed [%s]" % observerName)
        self.__publishEvents(True, ST_NAME_PS_CONTAINER_DEPLOYED, ["False",])

    def __onPluginDeployed(self, plugin, pluginWorkingPath):
        uuid = plugin.getDescription().getUuid()
        pngUrl = '/%s/icon.png' % uuid
        resourcesManager.addFileToServe(plugin.getDescription().getIconFile(),
                pngUrl)
        scpName = os.path.split(plugin.getScpFile())[-1]
        pluginDlUrl = '/plugins/%s' % scpName
        resourcesManager.addFileToServe(plugin.getScpFile(), pluginDlUrl)
        plugin.setOnPluginNotificationCallback(self.__onPluginNotification)
        plugin.setOnPluginMessageCallback(self.__onPluginMessage)
        plugin.setOnPluginErrorCallback(self.__onPluginError)
        plugin.setOnPluginTraceCallback(self.__onPluginTrace)
        plugin.setOnPluginResultCallback(self.__onPluginResult)
        plugin.setOnPluginActuationCallback(self.__onPluginActuation)
        plugin.setOnPluginStartingCallback(self.__onPluginStarting)
        plugin.setOnPluginStoppedCallback(self.__onPluginStopped)
        pluginAttPath = os.path.join(pluginWorkingPath, "resources",
            "attitunes")
        if os.path.isdir(pluginAttPath):
            resourceAttituneManager.getAttitunesContainer().addDirectory(
                pluginAttPath, uuid)
        pluginTtsFixesPath = os.path.join(pluginWorkingPath, "resources",
            "tts_fixes")
        ttsFixer.addPoDirectory(pluginTtsFixesPath)
        self.logger.logDebug("Plugin deployed [%s] to [%s]" % (
            plugin.getDescription().getName(), pluginWorkingPath))
        self.__publishEvents(False, ST_NAME_PS_PLUGIN_LOADED, [uuid,])

    def __onPluginDeploymentError(self, observerName, pluginFileName, message):
        messagesList = [
            observerName,
            pluginFileName,
            message,
        ]
        self.logger.logWarning("Plugin deployment error [%s, %s] to (%s)" % (
            observerName, pluginFileName, message))
        self.__publishEvents(False, ST_NAME_PS_CONTAINER_ERROR, messagesList)

    def __onPluginUndeployed(self, plugin, pluginWorkingPath):
        uuid = plugin.getDescription().getUuid()
        pngUrl = '/%s/icon.png' % uuid
        resourcesManager.removeFileToServe(pngUrl)
        scpName = os.path.split(plugin.getScpFile())[-1]
        pluginDlUrl = '/plugins/%s' % scpName
        resourcesManager.removeFileToServe(pluginDlUrl)
        pluginAttPath = os.path.join(pluginWorkingPath, "resources",
            "attitunes")
        if os.path.isdir(pluginAttPath):
            resourceAttituneManager.getAttitunesContainer().removeDirectory(
                pluginAttPath)
        self.logger.logDebug("Plugin undeployed [%s] to [%s]" % (
            plugin.getDescription().getName(), pluginWorkingPath))
        self.__publishEvents(False, ST_NAME_PS_PLUGIN_UNLOADED, [uuid,])

    # --------------------------------------------------------------------------
    # Plugin events
    # --------------------------------------------------------------------------

    def __onPluginNotification(self, pluginInterpreterContext, messageId, *args):
        messageStr = ""
        for message in args:
            messageStr += message
        plugin = pluginInterpreterContext.getParentPlugin()
        self.logger.logDebug("Plugin NOTIFICATION [%s] (%s : %s)" % (
            plugin.getDescription().getName(), messageId, messageStr))
        command = plugin.getCommand(pluginInterpreterContext.getInstanceCommandName())
        if command.isNotifier():
            if messageId == "start":
                resourceRobotContentInteractions.getPguContextsManager().createPguContext(
                    pluginInterpreterContext)
            elif messageId == "stop":
                resourceRobotContentInteractions.getPguContextsManager().setContextIsComplete(
                    pluginInterpreterContext)

    def __onPluginMessage(self, pluginInterpreterContext, message):
        locutor = pluginInterpreterContext.getInstanceParameters()['locutor']
        pitch = pluginInterpreterContext.getInstanceParameters()['pitch']
        plugin = pluginInterpreterContext.getParentPlugin()
        self.logger.logDebug("Plugin MESSAGE [%s] (%s)" % (
            plugin.getDescription().getName(), message))
        resourceRobotContentInteractions.getPguContextsManager().insertMessage(
            pluginInterpreterContext,
            message,
            locutor,
            int(pitch)
        )

    def __onPluginError(self, pluginInterpreterContext, *messagesList):
        messageStr = ""
        for message in messagesList:
            messageStr += message
        plugin = pluginInterpreterContext.getParentPlugin()
        self.logger.logError("Plugin ERROR [%s] (%s)" % (
            plugin.getDescription().getName(), messageStr))

    def __onPluginTrace(self, pluginInterpreterContext, *messagesList):
        messageStr = ""
        for message in messagesList:
            messageStr += message
        if messageStr.lower().find("   password:") != -1:
            messageStr = "   password:********"
        plugin = pluginInterpreterContext.getParentPlugin()
        self.logger.logDebug("Plugin TRACE [%s] (%s)" % (
            plugin.getDescription().getName(), messageStr))

    def __onPluginResult(self, pluginInterpreterContext, pluginResult):
        plugin = pluginInterpreterContext.getParentPlugin()
        if str(pluginResult).lower() == "true":
            resourceRobotContentInteractions.getPguContextsManager().createPguContext(
                pluginInterpreterContext)
        self.logger.logDebug("Plugin RESULT [%s] (%s)" % (
            plugin.getDescription().getName(), str(pluginResult)))

    def __onPluginActuation(self, pluginInterpreterContext, *messagesList):
        messageStr = ""
        for message in messagesList:
            messageStr += " " + message
        plugin = pluginInterpreterContext.getParentPlugin()
        self.logger.logDebug("Plugin ACTUATION [%s] (%s)" % (
            plugin.getDescription().getName(), messageStr))
        actuationName = messagesList[0]
        arguments = messagesList[1:]
        if actuationName == "playAttitune":
            resourceRobotContentInteractions.getPguContextsManager().insertAttitune(
                pluginInterpreterContext,
                arguments[0]
            )
        else:
            resourceRobotContentInteractions.getPguContextsManager().insertActuation(
                pluginInterpreterContext,
                actuationName,
                arguments
            )

    def __onPluginStarting(self, pluginInterpreterContext):
        plugin = pluginInterpreterContext.getParentPlugin()
        self.__publishEvents(False, ST_NAME_PS_PLUGIN_STARTED,
            [plugin.getDescription().getUuid(),])
        params = copy.deepcopy(pluginInterpreterContext.getInstanceParameters())
        if params.has_key('password'):
            params['password'] = '********'
        if params.has_key('Password'):
            params['Password'] = '********'
        self.logger.logInfo("Plugin starting [%s] (%s)" % (
            plugin.getDescription().getName(), str(params)))
        command = plugin.getCommand(pluginInterpreterContext.getInstanceCommandName())
        if (not command.isNotifier()) and (command.getName() == "run"):
            resourceRobotContentInteractions.getPguContextsManager().createPguContext(
                pluginInterpreterContext)

    def __onPluginStopped(self, pluginInterpreterContext):
        plugin = pluginInterpreterContext.getParentPlugin()
        command = plugin.getCommand(pluginInterpreterContext.getInstanceCommandName())
        if not command.isNotifier():
            resourceRobotContentInteractions.getPguContextsManager().setContextIsComplete(
                pluginInterpreterContext)
        self.__publishEvents(False, ST_NAME_PS_PLUGIN_STOPPED,
            [plugin.getDescription().getUuid(),])
        self.logger.logInfo("Plugin stopped [%s]" % (
                plugin.getDescription().getName()))

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    def __publishEvents(self, sendToClients, eventName, eventValues = []):
        def async():
            values = ""
            for value in eventValues:
                values += value + ":"
            if len(values) > 0:
                values = values[:-1]
            eventStruct = {
                'name' : eventName,
                'value' : values,
                'delay' : "0.0",
                'type' : "string"
            }
            if sendToClients:
                clientsManager.pushEvents([eventStruct,])
            eventsHandler.emit(eventName, (values, 0.0))
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Shared methods
    # --------------------------------------------------------------------------

    def getPluginsContainer(self):
        """Get the plugins container.
        @return: The plugins container.
        """
        return self.__pluginsContainer

    def insertPluginInContainer(self, scpFilename):
        """Insert a plugin in the plugins server container.
        @param scpFilename: SCP plugin file name.
        @return: The success.
        - scpFilename can be a local file or an external file (URL)
        - After the success of the plugin insertion the plugins server will
          detected it.
        """
        # Check that the plugins server is started
        if not self.__pluginsContainer.isDeployed():
            return False
        # Check that the container directory is selected
        directories = self.__pluginsContainer.getDirectories()
        if len(directories) == 0:
            return False
        directory = directories[-1]
        # Check the file extension
        if scpFilename.lower().rfind(".scp") == -1:
            return False
        # Create a cached file with the plugin file
        cFile = filesCacheManager.createFileCache(scpFilename)
        # If the plugin can't be cached then FAIL
        if cFile == None:
            return False
        # Copy the plugin in the container directory
        result = True
        import shutil
        try:
            scpName = os.path.split(scpFilename)[-1]
            scpName = os.path.join(directory, scpName)
            shutil.copy(cFile.getOutputFilePath(), scpName)
        except:
            result = False
        filesCacheManager.destroyFileCache(cFile)
        self.__pluginsContainer.check()
        return result

    def removePluginFromContainer(self, pluginUuid):
        """Remove a plugin from the plugins container.
        @param pluginUuid: Plugin uuid.
        @return: The success.
        """
        # Check that the plugins container is started
        if not self.__pluginsContainer.isDeployed():
            return False
        for plugin in self.__pluginsContainer.getPlugins():
            if plugin.getDescription().getUuid() == pluginUuid:
                scpFile = plugin.getScpFile()
                # Remove the scp file
                DirectoriesAndFilesTools.RMFile(scpFile)
                self.__pluginsContainer.check()
                return True
        return False

    def startPlugin(self, pluginUuid, command, parameters):
        """Start a plugin.
        @param pluginUuid: Plugin uuid.
        @param command: Command.
        @param parameters: Parameters.
        @return: True or False.
        """
        plugin = self.__pluginsContainer.getPluginByUuid(pluginUuid)
        if plugin != None:
            plugin
            return plugin.start(command, parameters)
        else:
            return False

    def stopPlugin(self, pluginUuid):
        """Stop a plugin.
        @param pluginUuid: Plugin uuid.
        """
        plugin = self.__pluginsContainer.getPluginByUuid(pluginUuid)
        if plugin != None:
            plugin.stop()

    def getPluginData(self, pluginUuid, language):
        """Get the data of a plugin.
        @param pluginUuid: Plugin uuid.
        @param language: Language.
        """
        plugin = self.__pluginsContainer.getPluginByUuid(pluginUuid)
        if plugin != None:
            return plugin.getData(language)
        else:
            return None

# Create an instance of the resource
resourcePluginsServer = TDSResourcePluginsServer("resourcePluginsServer")
# Register the resource into the resources manager
resourcesManager.addResource(resourcePluginsServer)

# ------------------------------------------------------------------------------
# Declaration of the service "get_plugin_data".
# ------------------------------------------------------------------------------
class TDSServicePluginsServerGetPluginData(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "get_plugin_data"
        self.comment = "Get the data of a plugin."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        data = resourcePluginsServer.getPluginData(uuid, language)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
        return headersStruct, contentStruct

# Register the service into the resource
resourcePluginsServer.addService(TDSServicePluginsServerGetPluginData)


# ------------------------------------------------------------------------------
# Declaration of the service "start_plugin".
# ------------------------------------------------------------------------------
class TDSServicePluginsServerStartPlugin(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'command' : 'string',
            'parameters' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "start_plugin"
        self.comment = "Start a plugin."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        command = parameters['command']
        params = {}
        splParams = parameters['parameters'].split("|")
        for paramStruct in splParams:
            param = paramStruct.split("=")
            if len(param) == 2:
                params[param[0]] = param[1]
        t = threading.Thread(target = resourcePluginsServer.startPlugin,
            args = (uuid, command, params))
        t.start()
        return headersStruct, contentStruct

# Register the service into the resource
resourcePluginsServer.addService(TDSServicePluginsServerStartPlugin)

# ------------------------------------------------------------------------------
# Declaration of the service "stop_plugin".
# ------------------------------------------------------------------------------
class TDSServicePluginsServerStopPlugin(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop_plugin"
        self.comment = "Stop a plugin."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        resourcePluginsServer.stopPlugin(uuid)
        resourceTTS.stackRemoveByUuid(uuid)
        return headersStruct, contentStruct

# Register the service into the resource
resourcePluginsServer.addService(TDSServicePluginsServerStopPlugin)

# ------------------------------------------------------------------------------
# Declaration of the service "stop_all".
# ------------------------------------------------------------------------------
class TDSServicePluginsServerStopAll(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop_all"
        self.comment = "Stop all started plugins."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourcePluginsServer.getPluginsContainer().stopAllPlugins()
        resourceTTS.stackFlushExceptedUuid("0")
        return headersStruct, contentStruct

# Register the service into the resource
resourcePluginsServer.addService(TDSServicePluginsServerStopAll)

# ------------------------------------------------------------------------------
# Declaration of the service "insert_plugin".
# ------------------------------------------------------------------------------
class TDSServicePluginsServerInsertPlugin(TDSService):

    def configure(self):
        self.parametersDict = {
            'path' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "insert_plugin"
        self.comment = "Insert a plugin in the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourcePluginsServer.insertPluginInContainer(
            parameters['path']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourcePluginsServer.addService(TDSServicePluginsServerInsertPlugin)

# ------------------------------------------------------------------------------
# Declaration of the service "remove_plugin".
# ------------------------------------------------------------------------------
class TDSServicePluginsServerRemovePlugin(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "remove_plugin"
        self.comment = "Remove a plugin from the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourcePluginsServer.removePluginFromContainer(
            parameters['uuid']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourcePluginsServer.addService(TDSServicePluginsServerRemovePlugin)
