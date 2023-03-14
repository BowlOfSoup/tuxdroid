# ==============================================================================
# Gadgets server resource.
# ==============================================================================

from util.applicationserver.gadget.GadgetsContainer import GadgetsContainer
from util.applicationserver.plugin.Plugin import SUPPORTED_LANGUAGES_LIST
from util.logger.SimpleLogger import *

# Gadgets server events/statuses
ST_NAME_GS_CONTAINER_DEPLOYED = "gadgets_server_container_deployed"
ST_NAME_GS_CONTAINER_ERROR = "gadgets_server_container_error"
ST_NAME_GS_GADGET_LOADED = "gadgets_server_gadget_loaded"
ST_NAME_GS_GADGET_UNLOADED = "gadgets_server_gadget_unloaded"

# Gadgets server events/statuses list
SW_NAME_GADGETS_SERVER = [
    ST_NAME_GS_CONTAINER_DEPLOYED,
    ST_NAME_GS_CONTAINER_ERROR,
    ST_NAME_GS_GADGET_LOADED,
    ST_NAME_GS_GADGET_UNLOADED,
]

# ------------------------------------------------------------------------------
# Declaration of the resource "gadgets_server".
# ------------------------------------------------------------------------------
class TDSResourceGadgetsServer(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "gadgets_server"
        self.comment = "Resource to manage the gadgets server."
        self.fileName = RESOURCE_FILENAME
        # Registering the gadgets server statuses.
        for statusName in SW_NAME_GADGETS_SERVER:
            eventsHandler.insert(statusName)
        # Create a logger
        self.logger = SimpleLogger("gadgets_server")
        self.logger.resetLog()
        self.logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.logger.setTarget(TDS_CONF_LOG_TARGET)
        self.logger.logInfo("-----------------------------------------------")
        self.logger.logInfo("Smart-core Gadgets Server")
        self.logger.logInfo("Licence : GPL")
        self.logger.logInfo("-----------------------------------------------")

    def startServer(self):
        # Create a gadgets container
        self.__gadgetsContainer = GadgetsContainer(resourcePluginsServer.getPluginsContainer())
        self.__gadgetsContainer.setOnDirectoryDeployedCallback(self.__onDirectoryDeployed)
        self.__gadgetsContainer.setOnDirectoryUndeployedCallback(self.__onDirectoryUndeployed)
        self.__gadgetsContainer.setOnGadgetDeployedCallback(self.__onGadgetDeployed)
        self.__gadgetsContainer.setOnGadgetDeploymentErrorCallback(self.__onGadgetDeploymentError)
        self.__gadgetsContainer.setOnGadgetUndeployedCallback(self.__onGadgetUndeployed)
        gadgetsPath = os.path.join(TDS_DEFAULT_CONTENT_PATH, "gadgets")
        DirectoriesAndFilesTools.MKDirs(gadgetsPath)
        self.logger.logInfo("Add directory in the container [%s]." %\
                gadgetsPath)
        self.__gadgetsContainer.addDirectory(gadgetsPath)
        self.logger.logInfo("Deploy the gadgets container.")
        self.__gadgetsContainer.deploy()
        self.logger.logInfo("Gadgets container is deployed.")

    def stop(self):
        self.logger.logInfo("Undeploy the gadgets container")
        self.__gadgetsContainer.undeploy()

    # --------------------------------------------------------------------------
    # Gadgets container events
    # --------------------------------------------------------------------------

    def __onDirectoryDeployed(self, observerName):
        self.logger.logInfo("Directory deployed [%s]" % observerName)
        self.__publishEvents(True, ST_NAME_GS_CONTAINER_DEPLOYED, ["True",])

    def __onDirectoryUndeployed(self, observerName):
        self.logger.logInfo("Directory undeployed [%s]" % observerName)
        self.__publishEvents(True, ST_NAME_GS_CONTAINER_DEPLOYED, ["False",])

    def __onGadgetDeployed(self, gadget, gadgetWorkingPath):
        uuid = gadget.getDescription().getUuid()
        pngUrl = '/%s/icon.png' % uuid
        resourcesManager.addFileToServe(gadget.getDescription().getIconFile(),
                pngUrl)
        scgName = os.path.split(gadget.getScgFile())[-1]
        gadgetDlUrl = '/gadgets/%s' % scgName
        resourcesManager.addFileToServe(gadget.getScgFile(), gadgetDlUrl)
        self.logger.logInfo("Gadget deployed [%s] to [%s]" % (
            gadget.getDescription().getName(), gadgetWorkingPath))
        self.__publishEvents(False, ST_NAME_GS_GADGET_LOADED, [uuid,])

    def __onGadgetDeploymentError(self, observerName, gadgetFileName, message):
        messagesList = [
            observerName,
            gadgetFileName,
            message,
        ]
        self.logger.logWarning("Gadget deployment error [%s, %s] to (%s)" % (
            observerName, gadgetFileName, message))
        self.__publishEvents(False, ST_NAME_GS_CONTAINER_ERROR, messagesList)

    def __onGadgetUndeployed(self, gadget, gadgetWorkingPath):
        uuid = gadget.getDescription().getUuid()
        pngUrl = '/%s/icon.png' % uuid
        resourcesManager.removeFileToServe(pngUrl)
        scgName = os.path.split(gadget.getScgFile())[-1]
        gadgetDlUrl = '/gadgets/%s' % scgName
        resourcesManager.removeFileToServe(gadgetDlUrl)
        self.logger.logInfo("Gadget undeployed [%s] to [%s]" % (
            gadget.getDescription().getName(), gadgetWorkingPath))
        self.__publishEvents(False, ST_NAME_GS_GADGET_UNLOADED, [uuid,])

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

    def getGadgetsContainer(self):
        """Get the gadgets container.
        @return: The gadgets container.
        """
        return self.__gadgetsContainer

    def insertGadgetInContainer(self, scgFilename):
        """Insert a gadget in the gadgets server container.
        @param scgFilename: SCG gadget file name.
        @return: The success.
        - scgFilename can be a local file or an external file (URL)
        - After the success of the gadget insertion the gadgets server will
          detected it.
        """
        # Check that the gadgets server is started
        if not self.__gadgetsContainer.isDeployed():
            return False
        # Check that the container directory is selected
        directories = self.__gadgetsContainer.getDirectories()
        if len(directories) == 0:
            return False
        directory = directories[-1]
        # Check the file extension
        if scgFilename.lower().rfind(".scg") == -1:
            return False
        # Create a cached file with the gadget file
        cFile = filesCacheManager.createFileCache(scgFilename)
        # If the gadget can't be cached then FAIL
        if cFile == None:
            return False
        # Copy the gadget in the container directory
        result = True
        import shutil
        try:
            scgName = os.path.split(scgFilename)[-1]
            scgName = os.path.join(directory, scgName)
            shutil.copy(cFile.getOutputFilePath(), scgName)
        except:
            result = False
        filesCacheManager.destroyFileCache(cFile)
        self.__gadgetsContainer.check()
        resourceUgcServer.createUgcFromGWC()
        resourceUgcServer.getUgcContainer().updateParentGadgets()
        return result

    def insertTemporaryServerGadgetInContainer(self, scgUrl):
        """Insert a gadget in the gadgets server container.
        @param scgUrl: SCG gadget file name.
        @return: The success.
        """
        # Check that the gadgets server is started
        if not self.__gadgetsContainer.isDeployed():
            return False
        # Check that the container directory is selected
        directories = self.__gadgetsContainer.getDirectories()
        if len(directories) == 0:
            return False
        directory = directories[-1]
        # Check the file extension
        if scgUrl.lower().rfind(".scg") == -1:
            return False
        # Get the gadget file content
        scgContent = resourcesManager.getServedFileContent(scgUrl)
        # Copy the gadget in the container directory
        result = True
        scgName = os.path.split(scgUrl)[-1]
        scgName = os.path.join(directory, scgName)
        f = open(scgName, "wb")
        f.write(scgContent)
        f.close()
        self.__gadgetsContainer.check()
        resourceUgcServer.createUgcFromGWC()
        resourceUgcServer.getUgcContainer().updateParentGadgets()
        return result

    def removeGadgetFromContainer(self, gadgetUuid):
        """Remove a gadget from the gadgets container.
        @param gadgetUuid: Gadget uuid.
        @return: The success.
        """
        # Check that the gadgets container is started
        if not self.__gadgetsContainer.isDeployed():
            return False
        for gadget in self.__gadgetsContainer.getGadgets():
            if gadget.getDescription().getUuid() == gadgetUuid:
                scgFile = gadget.getScgFile()
                # Remove the scg file
                DirectoriesAndFilesTools.RMFile(scgFile)
                self.__gadgetsContainer.check()
                # Remove children of this gadget
                resourceUgcServer.getUgcContainer().destroyUgcByParentGadgetUuid(gadgetUuid)
                return True
        return False

    def startGadget(self, gadgetUuid, command, parameters):
        """Start a gadget.
        @param gadgetUuid: Gadget uuid.
        @param command: Command.
        @param parameters: Parameters.
        @return: True or False.
        """
        gadget = self.__gadgetsContainer.getGadgetByUuid(gadgetUuid)
        if gadget != None:
            return gadget.start(command, parameters)
        else:
            return False

    def stopGadget(self, gadgetUuid):
        """Stop a gadget.
        @param gadgetUuid: Gadget uuid.
        """
        gadget = self.__gadgetsContainer.getGadgetByUuid(gadgetUuid)
        if gadget != None:
            gadget.stop()

    def getGadgetData(self, gadgetUuid, language):
        """Get the data of a gadget.
        @param gadgetUuid: Gadget uuid.
        @param language: Language.
        """
        gadget = self.__gadgetsContainer.getGadgetByUuid(gadgetUuid)
        if gadget != None:
            return gadget.getData(language)
        else:
            return None

# Create an instance of the resource
resourceGadgetsServer = TDSResourceGadgetsServer("resourceGadgetsServer")
# Register the resource into the resources manager
resourcesManager.addResource(resourceGadgetsServer)

# ------------------------------------------------------------------------------
# Declaration of the service "get_gadget_data".
# ------------------------------------------------------------------------------
class TDSServiceGadgetsServerGetGadgetData(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "get_gadget_data"
        self.comment = "Get the data of a gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        data = resourceGadgetsServer.getGadgetData(uuid, language)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
        return headersStruct, contentStruct

# Register the service into the resource
resourceGadgetsServer.addService(TDSServiceGadgetsServerGetGadgetData)

# ------------------------------------------------------------------------------
# Declaration of the service "get_online_gadgets_data".
# ------------------------------------------------------------------------------
class TDSServiceGadgetsServerGetOnlineGadgetsData(TDSService):

    def configure(self):
        self.parametersDict = {
            'filter' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "get_online_gadgets_data"
        self.comment = "Get the data of the online gadgets."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        filter = parameters['filter']
        language = parameters['language']
        gadgetsOnlineContainer = resourceGadgetsServer.getGadgetsContainer().getGadgetsOnlineContainer()
        gadgetsOnlineContainer.update()
        data = gadgetsOnlineContainer.getData(language, filter)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
        return headersStruct, contentStruct

# Register the service into the resource
resourceGadgetsServer.addService(TDSServiceGadgetsServerGetOnlineGadgetsData)


# ------------------------------------------------------------------------------
# Declaration of the service "start_gadget".
# ------------------------------------------------------------------------------
class TDSServiceGadgetsServerStartGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'command' : 'string',
            'parameters' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "start_gadget"
        self.comment = "Start a gadget."

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
        if not resourceGadgetsServer.startGadget(uuid, command, params):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceGadgetsServer.addService(TDSServiceGadgetsServerStartGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "stop_gadget".
# ------------------------------------------------------------------------------
class TDSServiceGadgetsServerStopGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop_gadget"
        self.comment = "Stop a gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        resourceGadgetsServer.stopGadget(uuid)
        gadget = resourceGadgetsServer.getGadgetsContainer().getGadgetByUuid(uuid)
        resourceTTS.stackRemoveByUuid(gadget.getParentPlugin().getDescription().getUuid())
        return headersStruct, contentStruct

# Register the service into the resource
resourceGadgetsServer.addService(TDSServiceGadgetsServerStopGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "stop_all".
# ------------------------------------------------------------------------------
class TDSServiceGadgetsServerStopAll(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop_all"
        self.comment = "Stop all started gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceGadgetsServer.getGadgetsContainer().stopAllGadgets()
        resourceTTS.stackFlushExceptedUuid("0")
        return headersStruct, contentStruct

# Register the service into the resource
resourceGadgetsServer.addService(TDSServiceGadgetsServerStopAll)

# ------------------------------------------------------------------------------
# Declaration of the service "insert_gadget".
# ------------------------------------------------------------------------------
class TDSServiceGadgetsServerInsertGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'path' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "insert_gadget"
        self.comment = "Insert a gadget in the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceGadgetsServer.insertGadgetInContainer(
            parameters['path']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceGadgetsServer.addService(TDSServiceGadgetsServerInsertGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "insert_gadget_sl".
# ------------------------------------------------------------------------------
class TDSServiceGadgetsServerInsertGadgetSL(TDSService):

    def configure(self):
        self.parametersDict = {
            'path' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "insert_gadget_sl"
        self.comment = "Insert the last generated gadget in the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceGadgetsServer.insertTemporaryServerGadgetInContainer(
            parameters['path']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceGadgetsServer.addService(TDSServiceGadgetsServerInsertGadgetSL)

# ------------------------------------------------------------------------------
# Declaration of the service "remove_gadget".
# ------------------------------------------------------------------------------
class TDSServiceGadgetsServerRemoveGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "remove_gadget"
        self.comment = "Remove a gadget from the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceGadgetsServer.removeGadgetFromContainer(
            parameters['uuid']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceGadgetsServer.addService(TDSServiceGadgetsServerRemoveGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "export_gadgets".
# ------------------------------------------------------------------------------
class TDSServiceGadgetsServerExportGadgets(TDSService):

    def configure(self):
        self.parametersDict = {
            'dest_path' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "export_gadgets"
        self.comment = "Export gadgets data to an external directory."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        destPath = parameters['dest_path']
        resourceGadgetsServer.getGadgetsContainer().exportGadgets(destPath)
        return headersStruct, contentStruct

# Register the service into the resource
resourceGadgetsServer.addService(TDSServiceGadgetsServerExportGadgets)

