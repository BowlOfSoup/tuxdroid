# ==============================================================================
# Attitune manager resource.
# ==============================================================================

from util.attitunes.AttitunesContainer import AttitunesContainer
from util.misc.tuxPaths import USER_BASE_PATH
from util.logger.SimpleLogger import *

# Attitune manager events/statuses
ST_NAME_AM_CONTAINER_DEPLOYED = "attitune_manager_container_deployed"
ST_NAME_AM_CONTAINER_ERROR = "attitune_manager_container_error"
ST_NAME_AM_ATTITUNE_LOADED = "attitune_manager_attitune_loaded"
ST_NAME_AM_ATTITUNE_UNLOADED = "attitune_manager_attitune_unloaded"
ST_NAME_AM_ATTITUNE_STARTING = "attitune_manager_attitune_starting"
ST_NAME_AM_ATTITUNE_STOPPED = "attitune_manager_attitune_stopped"

# Attitune manager events/statuses list
SW_NAME_ATTITUNE_MANAGER = [
    ST_NAME_AM_CONTAINER_DEPLOYED, # Is sent to clients
    ST_NAME_AM_CONTAINER_ERROR, # Is not sent to clients
    ST_NAME_AM_ATTITUNE_LOADED, # Is not sent to clients
    ST_NAME_AM_ATTITUNE_UNLOADED, # Is not sent to clients
    ST_NAME_AM_ATTITUNE_STARTING, # Is sent to clients
    ST_NAME_AM_ATTITUNE_STOPPED, # Is sent to clients
]

# ------------------------------------------------------------------------------
# Declaration of the resource "attitune_manager".
# ------------------------------------------------------------------------------
class TDSResourceAttituneManager(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "attitune_manager"
        self.comment = "Resource to manage the attitunes container."
        self.fileName = RESOURCE_FILENAME
        self.__attituneMutex = threading.Lock()
        self.__attituneRunMutex = threading.Lock()
        self.__attituneRunFlag = False
        self.__attituneRunName = "0"
        # Create a gadgets container
        self.__attitunesContainer = AttitunesContainer()
        self.__attitunesContainer.setOnDirectoryDeployedCallback(self.__onDirectoryDeployed)
        self.__attitunesContainer.setOnDirectoryUndeployedCallback(self.__onDirectoryUndeployed)
        self.__attitunesContainer.setOnAttituneDeployedCallback(self.__onAttituneDeployed)
        self.__attitunesContainer.setOnAttituneUndeployedCallback(self.__onAttituneUndeployed)
        self.__attitunesContainer.setOnAttituneDeploymentErrorCallback(self.__onAttituneDeploymentError)
        # Registering the attitune manager statuses.
        for statusName in SW_NAME_ATTITUNE_MANAGER:
            eventsHandler.insert(statusName)
        # Create a logger
        self.logger = SimpleLogger("attitune_manager")
        self.logger.resetLog()
        self.logger.setLevel(LOG_LEVEL_DEBUG)
        self.logger.setTarget(LOG_TARGET_FILE)
        self.logger.logInfo("-----------------------------------------------")
        self.logger.logInfo("Tux Droid Attitune Manager")
        self.logger.logInfo("Licence : GPL")
        self.logger.logInfo("-----------------------------------------------")
        # Get the attitunes path
        attitunesPath = os.path.join(TDS_DEFAULT_CONTENT_PATH, "attitunes")
        DirectoriesAndFilesTools.MKDirs(attitunesPath)
        self.logger.logInfo("Add directory in the container [%s]." %\
                attitunesPath)
        self.__attitunesContainer.addDirectory(attitunesPath)
        self.logger.logInfo("Deploy the attitunes container.")
        self.__attitunesContainer.deploy()
        self.logger.logInfo("Attitunes container is deployed.")

    def stop(self):
        self.logger.logInfo("Undeploy the attitunes container")
        self.__attitunesContainer.undeploy()

    # --------------------------------------------------------------------------
    # Attitunes container events
    # --------------------------------------------------------------------------

    def __onDirectoryDeployed(self, observerName):
        self.logger.logInfo("Directory deployed [%s]" % observerName)
        self.__publishEvents(True, ST_NAME_AM_CONTAINER_DEPLOYED, ["True",])

    def __onDirectoryUndeployed(self, observerName):
        self.logger.logInfo("Directory undeployed [%s]" % observerName)
        self.__publishEvents(True, ST_NAME_AM_CONTAINER_DEPLOYED, ["False",])

    def __onAttituneDeployed(self, attitune, attituneWorkingPath):
        self.logger.logDebug("Attitune deployed [%s] to [%s]" % (
            attitune.getDescription().getName(), attituneWorkingPath))
        self.__publishEvents(False, ST_NAME_AM_ATTITUNE_LOADED,
            [attitune.getDescription().getName(),])

    def __onAttituneDeploymentError(self, observerName, attituneFileName, message):
        messagesList = [
            observerName,
            attituneFileName,
            message,
        ]
        self.logger.logWarning("Attitune deployment error [%s, %s] to (%s)" % (
            observerName, attituneFileName, message))
        self.__publishEvents(False, ST_NAME_AM_CONTAINER_ERROR, messagesList)

    def __onAttituneUndeployed(self, attitune, attituneWorkingPath):
        self.logger.logDebug("Attitune undeployed [%s] to [%s]" % (
            attitune.getDescription().getName(), attituneWorkingPath))
        self.__publishEvents(False, ST_NAME_AM_ATTITUNE_UNLOADED,
            [attitune.getDescription().getName(),])

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

    def __isAttituneRun(self):
        self.__attituneRunMutex.acquire()
        isRun = self.__attituneRunFlag
        self.__attituneRunMutex.release()
        return isRun

    def isAttituneRun(self):
        return self.__isAttituneRun()

    def __setAttituneRun(self, isRun):
        self.__attituneRunMutex.acquire()
        self.__attituneRunFlag = isRun
        self.__attituneRunMutex.release()

    def __setAttituneRunName(self, name):
        self.__attituneRunMutex.acquire()
        self.__attituneRunName = name
        self.__attituneRunMutex.release()

    def getAttituneRunName(self):
        self.__attituneRunMutex.acquire()
        result = self.__attituneRunName
        self.__attituneRunMutex.release()
        return result

    def __attituneStartingLoop(self, attitune, duration):
        self.__setAttituneRunName(attitune.getDescription().getName())
        self.__setAttituneRun(True)
        duration += 0.5
        timeout = int(duration * 10)
        self.logger.logInfo("Attitune starting [%s]" % (
            attitune.getDescription().getName(),))
        self.__publishEvents(True, ST_NAME_AM_ATTITUNE_STARTING,
            [attitune.getDescription().getName(),])
        while self.__isAttituneRun():
            timeout -= 1
            time.sleep(0.1)
            if timeout == 0:
                break
        self.__setAttituneRunName("0")
        self.__setAttituneRun(False)
        self.logger.logInfo("Attitune stopped [%s]" % (
            attitune.getDescription().getName(),))
        self.__publishEvents(True, ST_NAME_AM_ATTITUNE_STOPPED,
            [attitune.getDescription().getName(),])

    # --------------------------------------------------------------------------
    # Shared methods
    # --------------------------------------------------------------------------

    def publishEvents(self, sendToClients, eventName, eventValues = []):
        """
        """
        self.__publishEvents(sendToClients, eventName, eventValues)

    def getAttitunesContainer(self):
        """Get the attitunes container.
        @return: The attitunes container.
        """
        return self.__attitunesContainer

    def insertAttituneInContainer(self, attFilename):
        """Insert an attitune in the container.
        @param attFilename: ATT attitune file name.
        @return: The success.
        - attFilename can be a local file or an external file (URL)
        """
        # Check that the attitune manager is started
        if not self.__attitunesContainer.isDeployed():
            return False
        # Get the user attitunes directory
        directoryContentObservers = self.__attitunesContainer.getDirectoryContentObservers()
        if len(directoryContentObservers) == 0:
            return False
        directory = None
        for directoryContentObserver in directoryContentObservers:
            if directoryContentObserver.getName() == "userAttitunes":
                directory = directoryContentObserver.getDirectory()
                break
        if directory == None:
            return False
        # Check the file extension
        if attFilename.lower().rfind(".att") == -1:
            return False
        # Create a cached file with the attitune file
        cFile = filesCacheManager.createFileCache(attFilename)
        # If the attitune can't be cached then FAIL
        if cFile == None:
            return False
        # Copy the attitune in the container directory
        result = True
        import shutil
        try:
            attName = os.path.split(attFilename)[-1]
            attName = os.path.join(directory, attName)
            shutil.copy(cFile.getOutputFilePath(), attName)
        except:
            result = False
        filesCacheManager.destroyFileCache(cFile)
        self.__attitunesContainer.check()
        return result

    def removeAttituneFromContainer(self, attituneName):
        """Remove an attitune from the attitunes container.
        @param attituneName: Attitune name.
        @return: The success.
        """
        # Check that the attitune manager is started
        if not self.__attitunesContainer.isDeployed():
            return False
        for attitune in self.__attitunesContainer.getAttitunes():
            if attitune.getDescription().getName() == attituneName:
                attFile = attitune.getAttFile()
                # Remove the att file
                DirectoriesAndFilesTools.RMFile(attFile)
                self.__attitunesContainer.check()
                return True
        return False

    def playAttitune(self, name, begin):
        """Play an attitune.
        @param name: Attitune name.
        @param begin: Begining position.
        @return: True or False.
        """
        if not resourceTuxDriver.getDonglePlugged():
            return False
        attituneExists = False
        attitunes = self.getAttitunesContainer().getAttitunes()
        reencodedName = name
        try:
            tmp = reencodedName.decode("latin-1")
            reencodedName = tmp.encode("utf-8")
        except:
            pass
        for attitune in attitunes:
            if attitune.getDescription().getName() in [name, reencodedName]:
                attituneExists = True
                break
        if not attituneExists:
            return False
        def async():
            self.__attituneMutex.acquire()
            if self.__isAttituneRun():
                self.__setAttituneRun(False)
                self.__setAttituneRunName("0")
                resourceTuxOSL.clearAll()
                resourceTuxDriver.clearAll()
                time.sleep(0.2)
            macro = attitune.getMacro(begin)
            macro = resourceTuxOSL.reencodeTTSTextInMacro(macro)
            if len(macro) <= 16384:
                resourceTuxDriver.executeMacro(macro)
                resourceTuxOSL.executeMacro(macro)
                duration = attitune.getDescription().getDuration() - begin
                if duration > 0.0:
                    t = threading.Thread(target = self.__attituneStartingLoop,
                        args = (attitune, duration))
                    t.start()
            self.__attituneMutex.release()
        t = threading.Thread(target = async)
        t.start()
        return True

    def playAttituneSync(self, name, begin):
        """Play an attitune.
        @param name: Attitune name.
        @param begin: Begining position.
        @return: True or False.
        """
        if not resourceTuxDriver.getDonglePlugged():
            return False
        attituneExists = False
        attitunes = self.getAttitunesContainer().getAttitunes()
        reencodedName = name
        try:
            tmp = reencodedName.decode("latin-1")
            reencodedName = tmp.encode("utf-8")
        except:
            pass
        for attitune in attitunes:
            if attitune.getDescription().getName() in [name, reencodedName]:
                attituneExists = True
                break
        if not attituneExists:
            return False
        self.__attituneMutex.acquire()
        if self.__isAttituneRun():
            self.__setAttituneRun(False)
            self.__setAttituneRunName("0")
            resourceTuxOSL.clearAll()
            resourceTuxDriver.clearAll()
            time.sleep(0.2)
        macro = attitune.getMacro(begin)
        macro = resourceTuxOSL.reencodeTTSTextInMacro(macro)
        if len(macro) <= 16384:
            resourceTuxDriver.executeMacro(macro)
            resourceTuxOSL.executeMacro(macro)
            duration = attitune.getDescription().getDuration() - begin
            if duration > 0.0:
                self.__attituneStartingLoop(attitune, duration)
        self.__attituneMutex.release()
        return True

    def stopAttitune(self):
        """Stop the current played attitune.
        """
        def async():
            self.__attituneMutex.acquire()
            self.__setAttituneRun(False)
            self.__setAttituneRunName("0")
            resourceTuxOSL.clearAll()
            resourceTuxDriver.clearAll()
            time.sleep(0.2)
            self.__attituneMutex.release()
        t = threading.Thread(target = async)
        t.start()

    def getAttitunesNameByObserversList(self, observersList):
        """
        """
        attitunes = self.getAttitunesContainer().getAttitunes()
        namesList = []
        for attitune in attitunes:
            if attitune.getObserverName() in observersList:
                namesList.append(attitune.getDescription().getName())
        namesList.sort()
        return namesList

    def getAttitunesDictAll(self):
        """
        """
        if self.getAttituneRunName() == "1":
            self.__setAttituneRunName("0")
        result = {}
        count = 0
        namesList = self.getAttitunesNameByObserversList(["attitunes", "userAttitunes"])
        for attName in namesList:
            attitune = self.getAttitunesContainer().getAttitune(attName)
            result["attitune_%d_name" % count] = attName
            cat = attitune.getDescription().getCategory().lower()
            result["attitune_%d_icon" % count] = "/data/web_interface/common/img/att_icon_%s.png" % cat
            count += 1
        result['count'] = count
        return result

    def checkForUpdates(self):
        """
        """
        self.__attitunesContainer.check()
        self.__setAttituneRunName("1")

# Create an instance of the resource
resourceAttituneManager = TDSResourceAttituneManager("resourceAttituneManager")
# Register the resource into the resources manager
resourcesManager.addResource(resourceAttituneManager)

# ------------------------------------------------------------------------------
# Declaration of the service "attitunes_infos".
# ------------------------------------------------------------------------------
class TDSServiceAttituneManagerAttitunesInfos(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "attitunes_infos"
        self.comment = "Get the informations from all attitunes."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        attitunes = resourceAttituneManager.getAttitunesContainer().getAttitunes()
        attitunesNameList = []
        for attitune in attitunes:
            attitunesNameList.append(attitune.getDescription().getName())
        attitunesNameList.sort()
        for i, attituneName in enumerate(attitunesNameList):
            attitune = resourceAttituneManager.getAttitunesContainer().getAttitune(attituneName)
            d_name = "data|%.3d" % i
            structure = attitune.getDescription().getDictionary()
            contentStruct['root'][d_name] = structure
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttituneManager.addService(TDSServiceAttituneManagerAttitunesInfos)

# ------------------------------------------------------------------------------
# Declaration of the service "start_attitune_by_name".
# ------------------------------------------------------------------------------
class TDSServiceAttituneManagerStartAttituneByName(TDSService):

    def configure(self):
        self.parametersDict = {
            'name' : 'string',
            'begin' : 'float',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "start_attitune_by_name"
        self.comment = "Start an attitune by it name."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        name = parameters['name']
        begin = parameters['begin']
        if not resourceAttituneManager.playAttitune(name, begin):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttituneManager.addService(TDSServiceAttituneManagerStartAttituneByName)

# ------------------------------------------------------------------------------
# Declaration of the service "stop_attitune".
# ------------------------------------------------------------------------------
class TDSServiceAttituneManagerStopAttitune(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop_attitune"
        self.comment = "Stop the current played attitune."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceAttituneManager.stopAttitune()
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttituneManager.addService(TDSServiceAttituneManagerStopAttitune)

# ------------------------------------------------------------------------------
# Declaration of the service "insert_attitune".
# ------------------------------------------------------------------------------
class TDSServiceAttituneManagerInsertAttitune(TDSService):

    def configure(self):
        self.parametersDict = {
            'path' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "insert_attitune"
        self.comment = "Insert an attitune in the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceAttituneManager.insertAttituneInContainer(
            parameters['path']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttituneManager.addService(TDSServiceAttituneManagerInsertAttitune)

# ------------------------------------------------------------------------------
# Declaration of the service "remove_attitune".
# ------------------------------------------------------------------------------
class TDSServiceAttituneManagerRemoveAttitune(TDSService):

    def configure(self):
        self.parametersDict = {
            'name' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "remove_attitune"
        self.comment = "Remove an attitune from the container."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceAttituneManager.removeAttituneFromContainer(
            parameters['name']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttituneManager.addService(TDSServiceAttituneManagerRemoveAttitune)

# ------------------------------------------------------------------------------
# Declaration of the service "get_attitunes_data".
# ------------------------------------------------------------------------------
class TDSServiceAttituneManagerGetAttitunesData(TDSService):

    def configure(self):
        self.parametersDict = {
            'filter' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "get_attitunes_data"
        self.comment = "Get attitunes data."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        filter = parameters['filter']
        if filter == 'all_attitunes':
            contentStruct['root']['data'] = resourceAttituneManager.getAttitunesDictAll()
        else:
            pass
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttituneManager.addService(TDSServiceAttituneManagerGetAttitunesData)

# ------------------------------------------------------------------------------
# Declaration of the service "get_current_playing_attitune".
# ------------------------------------------------------------------------------
class TDSServiceAttituneManagerGetCurrentPlayingAttitune(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "get_current_playing_attitune"
        self.comment = "Get the current playing attitune name."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        name = resourceAttituneManager.getAttituneRunName()
        contentStruct['root']['name'] = name
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttituneManager.addService(TDSServiceAttituneManagerGetCurrentPlayingAttitune)
