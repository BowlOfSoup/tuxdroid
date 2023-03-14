# ==============================================================================
# Attitune resource.
# ==============================================================================

# This resource depends of the following resources :
# - resourceTuxDriver
# - resourceTuxOSL

from util.attitunes.AttitunesFileReader import *

# ------------------------------------------------------------------------------
# Declaration of the resource "attitune".
# ------------------------------------------------------------------------------
class TDSResourceAttitune(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "attitune"
        self.comment = "Resource to manage the playing of attitune files."
        self.fileName = RESOURCE_FILENAME
        self.__attituneMutex = threading.Lock()
        self.__currentAttitune = None
        
    def stop(self):
        if self.__currentAttitune != None:
            self.__currentAttitune.destroy()
            
    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    def loadAttitune(self, fileName):
        """Load an attitune file.
        @param fileName: File name path of the attitune. (internet URL or local)
        @return: True or False.
        """
        # Check the file extension
        if fileName.lower().rfind(".att") == -1:
            return False
        self.__attituneMutex.acquire()
        # Create a cached file with the attitune file
        cFile = filesCacheManager.createFileCache(fileName)
        # If the attitune can't be cached then FAIL
        if cFile == None:
            self.__attituneMutex.release()
            return False
        # If an attitune is currently loaded in the attitunes reader then
        # destroy it.
        if self.__currentAttitune != None:
            self.__currentAttitune.destroy()
        # Load the attitune in the attitunes reader.
        self.__currentAttitune = AttitunesFileReader(cFile.getOutputFilePath())
        # If the attitune is invalid the FAIL
        if not self.__currentAttitune.getValid():
            self.__currentAttitune = None
            self.__attituneMutex.release()
            return False
        self.__attituneMutex.release()
        # Success !
        return True
        
    def playAttitune(self, begin):
        """Play the current loaded attitune file.
        @param begin: Begining position.
        @return: True or False.
        """
        if not resourceTuxDriver.getDonglePlugged():
            return False
        self.__attituneMutex.acquire()
        if self.__currentAttitune != None:
            resourceTuxOSL.clearAll()
            resourceTuxDriver.clearAll()
            macro = self.__currentAttitune.toMacro(begin)
            macro = resourceTuxOSL.reencodeTTSTextInMacro(macro)
            if len(macro) <= 16384:
                resourceTuxDriver.executeMacro(macro)
                resourceTuxOSL.executeMacro(macro)
            else:
                self.__attituneMutex.release()
                return False
        else:
            self.__attituneMutex.release()
            return False
        self.__attituneMutex.release()
        return True
        
    def stopAttitune(self):
        """Stop the current played attitune.
        """
        def async():
            self.__attituneMutex.acquire()
            if self.__currentAttitune != None:
                resourceTuxOSL.clearAll()
                resourceTuxDriver.clearAll()
            self.__attituneMutex.release()
        t = threading.Thread(target = async)
        t.start()

# Create an instance of the resource
resourceAttitune = TDSResourceAttitune("resourceAttitune")
# Register the resource into the resources manager
resourcesManager.addResource(resourceAttitune)

# ------------------------------------------------------------------------------
# Declaration of the service "load".
# ------------------------------------------------------------------------------
class TDSServiceAttituneLoad(TDSService):

    def configure(self):
        self.parametersDict = {
            'path' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "load"
        self.comment = "Load an attitune."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceAttitune.loadAttitune(parameters['path']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttitune.addService(TDSServiceAttituneLoad)

# ------------------------------------------------------------------------------
# Declaration of the service "play".
# ------------------------------------------------------------------------------
class TDSServiceAttitunePlay(TDSService):

    def configure(self):
        self.parametersDict = {
            'begin' : 'float',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "play"
        self.comment = "Play an attitune."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceAttitune.playAttitune(parameters['begin']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttitune.addService(TDSServiceAttitunePlay)

# ------------------------------------------------------------------------------
# Declaration of the service "load_and_play".
# ------------------------------------------------------------------------------
class TDSServiceAttituneLoadPlay(TDSService):

    def configure(self):
        self.parametersDict = {
            'path' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "load_and_play"
        self.comment = "Load and play an attitune."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceAttitune.loadAttitune(parameters['path']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            if not resourceAttitune.playAttitune(0.0):
                contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttitune.addService(TDSServiceAttituneLoadPlay)

# ------------------------------------------------------------------------------
# Declaration of the service "stop".
# ------------------------------------------------------------------------------
class TDSServiceAttituneStop(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop"
        self.comment = "Stop the played attitune."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceAttitune.stopAttitune()
        return headersStruct, contentStruct

# Register the service into the resource
resourceAttitune.addService(TDSServiceAttituneStop)
