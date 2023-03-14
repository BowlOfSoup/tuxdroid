# ==============================================================================
# Sound flash resource.
# ==============================================================================

# This resource depends of the following resources :
# - resourceTuxDriver

# ------------------------------------------------------------------------------
# Declaration of the resource "sound_flash".
# ------------------------------------------------------------------------------
class TDSResourceSoundFlash(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "sound_flash"
        self.comment = "Resource to manage the sound flash of Tux Droid."
        self.fileName = RESOURCE_FILENAME
        self.__reflashMutex = threading.Lock()

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    def reflash(self, myTracks):
        """Reflash the sound memory of Tux Droid.
        @param myTracks: Track paths list. (Internet URLs or/and local paths)
        @return: True or False.
        """
        if not resourceTuxDriver.getDonglePlugged():
            return False
        def async():
            self.__reflashMutex.acquire()
            tracks = ""
            trackFiles = myTracks.split("|")
            origTf = []
            for path in trackFiles:
                p, ext = os.path.splitext(path)
                if ext.lower() != '.wav':
                    self.__reflashMutex.release()
                    return False
                retryCount = 0
                while True:
                    if retryCount > 5:
                        break
                    filesCacheManager.createFileCache(path)
                    if cFile != None:
                        break
                    retryCount += 1
                if cFile != None:
                    origTf.append(cFile.getOutputFilePath())
                else:
                    self.__reflashMutex.release()
                    return False
            for track in origTf:
                tracks += track + '|'
            tracks = tracks[:-1]
            resourceTuxDriver.reflashSoundMemory(tracks)
            self.__reflashMutex.release()
        t = threading.Thread(target = async)
        t.start()
        return True

# Create an instance of the resource
resourceSoundFlash = TDSResourceSoundFlash("resourceSoundFlash")
# Register the resource into the resources manager
resourcesManager.addResource(resourceSoundFlash)

# ------------------------------------------------------------------------------
# Declaration of the service "play".
# ------------------------------------------------------------------------------
class TDSServiceSoundFlashPlay(TDSService):

    def configure(self):
        self.parametersDict = {
            'track' : 'uint8',
            'volume' : 'float',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "play"
        self.comment = "Play a sound from the flash."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.playSound(parameters['track'],
            parameters['volume']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        contentStruct['root']['data'] = {'cmd_answer' : 0}
        return headersStruct, contentStruct

# Register the service into the resource
resourceSoundFlash.addService(TDSServiceSoundFlashPlay)

# ------------------------------------------------------------------------------
# Declaration of the service "reflash".
# ------------------------------------------------------------------------------
class TDSServiceSoundFlashReflash(TDSService):

    def configure(self):
        self.parametersDict = {
            'tracks' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_RESTRICTED
        self.exclusiveExecution = False
        self.name = "reflash"
        self.comment = "Reflash the sound flash memory."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceSoundFlash.reflash(parameters['tracks']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        contentStruct['root']['data'] = {'cmd_answer' : 0}
        return headersStruct, contentStruct

# Register the service into the resource
resourceSoundFlash.addService(TDSServiceSoundFlashReflash)