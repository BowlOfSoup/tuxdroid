# ==============================================================================
# UGC (User Gadgets Server) server resource.
# ==============================================================================

from util.applicationserver.ugc.UgcContainer import UgcContainer
from util.applicationserver.gadget.GadgetGenerator import GadgetGenerator
from util.applicationserver.plugin.Plugin import SUPPORTED_LANGUAGES_LIST
from util.logger.SimpleLogger import *

# UGC server events/statuses
ST_NAME_US_CONTAINER_DEPLOYED = "ugc_server_container_deployed"
ST_NAME_US_CONTAINER_ERROR = "ugc_server_container_error"
ST_NAME_US_UGC_LOADED = "ugc_server_ugc_loaded"
ST_NAME_US_UGC_UNLOADED = "ugc_server_ugc_unloaded"

# UGC server events/statuses list
SW_NAME_UGC_SERVER = [
    ST_NAME_US_CONTAINER_DEPLOYED,
    ST_NAME_US_CONTAINER_ERROR,
    ST_NAME_US_UGC_LOADED,
    ST_NAME_US_UGC_UNLOADED,
]

# ------------------------------------------------------------------------------
# Declaration of the resource "ugc_server".
# ------------------------------------------------------------------------------
class TDSResourceUgcServer(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "ugc_server"
        self.comment = "Resource to manage the UGC server."
        self.fileName = RESOURCE_FILENAME
        # Registering the UGC server statuses.
        for statusName in SW_NAME_UGC_SERVER:
            eventsHandler.insert(statusName)
        # Create a logger
        self.logger = SimpleLogger("ugc_server")
        self.logger.resetLog()
        self.logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.logger.setTarget(TDS_CONF_LOG_TARGET)
        self.logger.logInfo("-----------------------------------------------")
        self.logger.logInfo("Smart-core User Gadgets Server")
        self.logger.logInfo("Licence : GPL")
        self.logger.logInfo("-----------------------------------------------")

    def startServer(self, ugcPath):
        # Create a UGC container and start the UGC server
        self.__ugcContainer = UgcContainer(resourceGadgetsServer.getGadgetsContainer())
        self.__ugcContainer.setOnUgcDeployedCallback(self.__onUgcDeployed)
        self.__ugcContainer.setOnUgcDeploymentErrorCallback(self.__onUgcDeploymentError)
        self.__ugcContainer.setOnUgcUndeployedCallback(self.__onUgcUndeployed)
        self.logger.logInfo("Set directory in the UGC container [%s]." % ugcPath)
        self.__ugcContainer.setDirectory(ugcPath)
        self.logger.logInfo("Deploy the UGC container.")
        self.__ugcContainer.check()
        self.logger.logInfo("UGC container is deployed.")
        # Create UGC objects from gadgets without children
        self.createUgcFromGWC()

    # --------------------------------------------------------------------------
    # UGC container events
    # --------------------------------------------------------------------------

    def __onUgcDeployed(self, ugc, ugcFile):
        uuid = ugc.getDescription().getUuid()
        ugcName = os.path.split(ugc.getUgcFile())[-1]
        ugcDlUrl = '/ugcs/%s' % ugcName
        resourcesManager.addFileToServe(ugc.getUgcFile(), ugcDlUrl)
        self.logger.logInfo("UGC deployed [%s] to [%s]" % (
            ugc.getDescription().getName(), ugcFile))
        self.__publishEvents(False, ST_NAME_US_UGC_LOADED, [uuid,])
        self.insertAlertsInScheduler(ugc)
        if ugc.getDescription().onDemandIsActivated() == "true":
            resourceRobotContentInteractions.getPguContextsManager().insertOnDemand(ugc)

    def __onUgcDeploymentError(self, observerName, ugcFile, message):
        messagesList = [
            observerName,
            ugcFile,
            message,
        ]
        self.logger.logWarning("UGC deployment error [%s, %s] to (%s)" % (
            observerName, ugcFile, message))
        self.__publishEvents(False, ST_NAME_US_CONTAINER_ERROR, messagesList)

    def __onUgcUndeployed(self, ugc, ugcFile):
        uuid = ugc.getDescription().getUuid()
        ugcName = os.path.split(ugc.getUgcFile())[-1]
        ugcDlUrl = '/ugcs/%s' % ugcName
        resourcesManager.removeFileToServe(ugcDlUrl)
        self.logger.logInfo("UGC undeployed [%s] from [%s]" % (
            ugc.getDescription().getName(), ugcFile))
        self.__publishEvents(False, ST_NAME_US_UGC_UNLOADED, [uuid,])
        self.deleteAlertsFromScheduler(ugc)
        resourceRobotContentInteractions.getPguContextsManager().removeOnDemand(ugc)
        ugc.stop()

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

    def getUgcContainer(self):
        """Get the UGC container.
        @return: The UGC container.
        """
        return self.__ugcContainer

    def createUgcFromGWC(self):
        """Create UGC objects from gadgets without children.
        """
        for gadget in resourceGadgetsServer.getGadgetsContainer().getGadgets():
            gadgetUuid = gadget.getDescription().getUuid()
            haveUgcChild = False
            for ugc in self.__ugcContainer.getUgcs():
                uPGadgetUuid = ugc.getParentGadget().getDescription().getUuid()
                if gadgetUuid == uPGadgetUuid:
                    haveUgcChild = True
                    break
            if not haveUgcChild:
                ugcUrl, uuid = GadgetGenerator.generateUgcFromGadget(gadget,
                    self.__ugcContainer, self.__ugcContainer.getLanguage(),
                    resourcesManager)
                self.insertTemporaryServedUgcInContainer(ugcUrl)
                time.sleep(0.015)

    def removeGadgetsWithoutChildren(self):
        """Remove the gadgets without UGC children.
        """
        for gadget in resourceGadgetsServer.getGadgetsContainer().getGadgets():
            gadgetUuid = gadget.getDescription().getUuid()
            haveUgcChild = False
            for ugc in self.__ugcContainer.getUgcs():
                uPGadgetUuid = ugc.getParentGadget().getDescription().getUuid()
                if gadgetUuid == uPGadgetUuid:
                    haveUgcChild = True
                    break
            if not haveUgcChild:
                resourceGadgetsServer.removeGadgetFromContainer(gadgetUuid)

    def insertUgcInContainer(self, ugcFilename):
        """Insert an ugc in the UGC server container.
        @param ugcFilename: UGC file name.
        @return: The success.
        - ugcFilename can be a local file or an external file (URL)
        """
        directory = self.__ugcContainer.getDirectory()
        # Check the file extension
        if ugcFilename.lower().rfind(".ugc") == -1:
            return False
        # Create a cached file with the ugc file
        cFile = filesCacheManager.createFileCache(ugcFilename)
        # If the ugc can't be cached then FAIL
        if cFile == None:
            return False
        # Copy the ugc in the container directory
        result = True
        import shutil
        try:
            ugcName = os.path.split(ugcFilename)[-1]
            ugcName = os.path.join(directory, ugcName)
            shutil.copy(cFile.getOutputFilePath(), ugcName)
        except:
            result = False
        filesCacheManager.destroyFileCache(cFile)
        self.__ugcContainer.check()
        return result

    def insertTemporaryServedUgcInContainer(self, ugcUrl):
        """Insert an ugc in the UGC container.
        @param ugcUrl: UGC file name.
        @return: The success.
        """
        directory = self.__ugcContainer.getDirectory()
        # Check the file extension
        if ugcUrl.lower().rfind(".ugc") == -1:
            return False
        # Get the ugc file content
        ugcContent = resourcesManager.getServedFileContent(ugcUrl)
        # Copy the ugc in the container directory
        result = True
        ugcName = os.path.split(ugcUrl)[-1]
        ugcName = os.path.join(directory, ugcName)
        f = open(ugcName, "wb")
        f.write(ugcContent)
        f.close()
        self.__ugcContainer.check()
        return result

    def removeUgcFromContainer(self, ugcUuid):
        """Remove an ugc from the UGC container.
        @param ugcUuid: UGC uuid.
        @return: The success.
        """
        for ugc in self.__ugcContainer.getUgcs():
            if ugc.getDescription().getUuid() == ugcUuid:
                ugcFile = ugc.getUgcFile()
                # Remove the ugc file
                DirectoriesAndFilesTools.RMFile(ugcFile)
                self.__ugcContainer.check()
                self.removeGadgetsWithoutChildren()
                return True
        return False

    def startUgc(self, ugcUuid, command, parameters):
        """Start an ugc.
        @param ugcUuid: UGC uuid.
        @param command: Command.
        @param parameters: Parameters.
        @return: True or False.
        """
        ugc = self.__ugcContainer.getUgcByUuid(ugcUuid)
        if ugc != None:
            return ugc.start(command, parameters)
        else:
            return False

    def stopUgc(self, ugcUuid):
        """Stop an ugc.
        @param ugcUuid: UGC uuid.
        """
        ugc = self.__ugcContainer.getUgcByUuid(ugcUuid)
        if ugc != None:
            ugc.stop()

    def getUgcData(self, ugcUuid, language):
        """Get the data of an ugc.
        @param ugcUuid: UGC uuid.
        @param language: Language.
        """
        ugc = self.__ugcContainer.getUgcByUuid(ugcUuid)
        if ugc != None:
            return ugc.getData(language)
        else:
            return None

    def insertAlertsInScheduler(self, ugc):
        """Insert activated ugc alerts in the scheduler.
        @param ugc: UGC object.
        """
        for ugcTask in ugc.getTasks():
            if not ugcTask.isActivated():
                continue
            parentTask = ugc.getParentGadget().getTask(ugcTask.getName())
            if parentTask == None:
                continue
            command = "resourceUgcServer.startUgc"
            arguments = (
                ugc.getDescription().getUuid(),
                parentTask.getCommand(),
                {
                    'startedBy' : 'scheduler',
                })
            data = {
                'commandType' : 'ugc_start',
                'uuid' : ugc.getDescription().getUuid(),
                'command' : parentTask.getCommand(),
                'parameters' : {
                    'startedBy' : 'scheduler',
                },
            }
            date = ugcTask.getDateDict()
            hoursBegin = ugcTask.getTimeDict(ugcTask.getHoursBegin())
            hoursEnd = ugcTask.getTimeDict(ugcTask.getHoursEnd())
            delay = ugcTask.getTimeDict(ugcTask.getDelay())
            taskId, taskName = resourceScheduler.createTask(
                command,
                arguments,
                parentTask.getType(),
                ugcTask.getName(),
                ugcTask.getWeekMask(),
                [date['year'], date['month'], date['day']],
                [hoursBegin['hour'], hoursBegin['minute'], hoursBegin['second']],
                [hoursEnd['hour'], hoursEnd['minute'], hoursEnd['second']],
                [delay['hour'], delay['minute'], delay['second']],
                data)
            ugcTask.setTaskId1(taskId)
            parentCommand = ugc.getCommand(parentTask.getCommand())
            if parentCommand != None:
                if parentCommand.isDaemon() and \
                   parentTask.getType() == "DAILY AT":
                    command = "resourceUgcServer.stopUgc"
                    arguments = (ugc.getDescription().getUuid(),)
                    data = {
                        'commandType' : 'ugc_stop',
                        'uuid' : ugc.getDescription().getUuid(),
                    }
                    taskId, taskName = resourceScheduler.createTask(
                        command,
                        arguments,
                        parentTask.getType(),
                        ugcTask.getName(),
                        ugcTask.getWeekMask(),
                        [date['year'], date['month'], date['day']],
                        [hoursEnd['hour'], hoursEnd['minute'], hoursEnd['second']],
                        [hoursEnd['hour'], hoursEnd['minute'], hoursEnd['second']],
                        [delay['hour'], delay['minute'], delay['second']],
                        data)
                    ugcTask.setTaskId2(taskId)

    def deleteAlertsFromScheduler(self, ugc):
        """Delete activated ugc alerts from the scheduler.
        @param ugc: UGC object.
        """
        for ugcTask in ugc.getTasks():
            if ugcTask.getTaskId1() != None:
                resourceScheduler.removeTask(ugcTask.getTaskId1())
            if ugcTask.getTaskId2() != None:
                resourceScheduler.removeTask(ugcTask.getTaskId2())

# Create an instance of the resource
resourceUgcServer = TDSResourceUgcServer("resourceUgcServer")
# Register the resource into the resources manager
resourcesManager.addResource(resourceUgcServer)

# ------------------------------------------------------------------------------
# Declaration of the service "get_ugc_data".
# ------------------------------------------------------------------------------
class TDSServiceUgcServerGetUgcData(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "get_ugc_data"
        self.comment = "Get the data of an ugc."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        data = resourceUgcServer.getUgcData(uuid, language)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
        return headersStruct, contentStruct

# Register the service into the resource
resourceUgcServer.addService(TDSServiceUgcServerGetUgcData)


# ------------------------------------------------------------------------------
# Declaration of the service "start_ugc".
# ------------------------------------------------------------------------------
class TDSServiceUgcServerStartUgc(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'command' : 'string',
            'parameters' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "start_ugc"
        self.comment = "Start an ugc."

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
        if not resourceUgcServer.startUgc(uuid, command, params):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceUgcServer.addService(TDSServiceUgcServerStartUgc)

# ------------------------------------------------------------------------------
# Declaration of the service "stop_ugc".
# ------------------------------------------------------------------------------
class TDSServiceUgcServerStopUgc(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop_ugc"
        self.comment = "Stop an ugc."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        resourceUgcServer.stopUgc(uuid)
        ugc = resourceUgcServer.getUgcContainer().getUgcByUuid(uuid)
        resourceTTS.stackRemoveByUuid(ugc.getParentGadget().getParentPlugin().getDescription().getUuid())
        return headersStruct, contentStruct

# Register the service into the resource
resourceUgcServer.addService(TDSServiceUgcServerStopUgc)

# ------------------------------------------------------------------------------
# Declaration of the service "stop_all".
# ------------------------------------------------------------------------------
class TDSServiceUgcServerStopAll(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop_all"
        self.comment = "Stop all started ugc."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceUgcServer.getUgcContainer().stopAllUgcs()
        resourceTTS.stackFlushExceptedUuid("0")
        return headersStruct, contentStruct

# Register the service into the resource
resourceUgcServer.addService(TDSServiceUgcServerStopAll)

# ------------------------------------------------------------------------------
# Declaration of the service "insert_ugc".
# ------------------------------------------------------------------------------
class TDSServiceUgcServerInsertUgc(TDSService):

    def configure(self):
        self.parametersDict = {
            'path' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "insert_ugc"
        self.comment = "Insert an ugc in the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceUgcServer.insertUgcInContainer(
            parameters['path']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceUgcServer.addService(TDSServiceUgcServerInsertUgc)

# ------------------------------------------------------------------------------
# Declaration of the service "insert_ugc_sl".
# ------------------------------------------------------------------------------
class TDSServiceUgcServerInsertUgcSL(TDSService):

    def configure(self):
        self.parametersDict = {
            'path' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "insert_ugc_sl"
        self.comment = "Insert the last generated ugc in the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceUgcServer.insertTemporaryServedUgcInContainer(
            parameters['path']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceUgcServer.addService(TDSServiceUgcServerInsertUgcSL)

# ------------------------------------------------------------------------------
# Declaration of the service "remove_ugc".
# ------------------------------------------------------------------------------
class TDSServiceUgcServerRemoveUgc(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "remove_ugc"
        self.comment = "Remove an ugc from the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceUgcServer.removeUgcFromContainer(
            parameters['uuid']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceUgcServer.addService(TDSServiceUgcServerRemoveUgc)
