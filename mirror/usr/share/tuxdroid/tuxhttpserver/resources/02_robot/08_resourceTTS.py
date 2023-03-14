# ==============================================================================
# TTS Resource
# ==============================================================================

# This resource depends of the following resources:
# - resourceTuxOSL

# TTS Stack events/statuses
ST_NAME_TTS_STACK_EMPTY = "tts_stack_empty"
ST_NAME_TTS_STACK_FILLING = "tts_stack_filling"

# TTS Stack events/statuses list
SW_NAME_TTS_STACK = [
    ST_NAME_TTS_STACK_EMPTY,
    ST_NAME_TTS_STACK_FILLING,
]

# ------------------------------------------------------------------------------
# Declaration of the resource "TTS".
# ------------------------------------------------------------------------------
class TDSResourceTTS(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "tts"
        self.comment = "Resource to manage the text to speech."
        self.fileName = RESOURCE_FILENAME
        # For the tts stack
        self.__stack = []
        self.__stackMutex = threading.Lock()
        self.__stackSFlag = False
        self.__stackThread = None
        self.__currentUuid = None
        self.__currentUuidMutex = threading.Lock()
        # Registering the TTS stack statuses only for server internal uses.
        for statusName in SW_NAME_TTS_STACK:
            eventsHandler.insert(statusName)

    def start(self):
        self.__stackThread = threading.Thread(target = self.__popStackLoop)
        self.__stackThread.start()

    def stop(self):
        self.__setStackStarted(False)
        if self.__stackThread != None:
            if self.__stackThread.isAlive():
                self.stackFlush()
                resourceTuxOSL.ttsStop()
                self.__stackThread.join()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    def __setStackStarted(self, value):
        self.__stackMutex.acquire()
        self.__stackSFlag = value
        self.__stackMutex.release()

    def __getStackStarted(self):
        self.__stackMutex.acquire()
        value = self.__stackSFlag
        self.__stackMutex.release()
        return value

    def __setCurrentUuid(self, uuid):
        self.__currentUuidMutex.acquire()
        self.__currentUuid = uuid
        self.__currentUuidMutex.release()

    def __getCurrentUuid(self):
        self.__currentUuidMutex.acquire()
        uuid = self.__currentUuid
        self.__currentUuidMutex.release()
        return uuid

    def __popStack(self):
        text = None
        locutor = None
        pitch = None
        uuid = None
        self.__stackMutex.acquire()
        if len(self.__stack) != 0:
            text, locutor, pitch, uuid = self.__stack.pop(0)
        self.__stackMutex.release()
        return text, locutor, pitch, uuid

    def __stackSize(self):
        self.__stackMutex.acquire()
        result = len(self.__stack)
        self.__stackMutex.release()
        return result

    def __popStackLoop(self):
        self.__setStackStarted(True)
        while self.__getStackStarted():
            text, locutor, pitch, uuid = self.__popStack()
            if text != None:
                self.__setCurrentUuid(uuid)
                resourceTuxOSL.ttsSpeak(text, locutor, pitch)
                if not eventsHandler.waitCondition(ST_NAME_TTS_SOUND_STATE,
                    ("ON", None), 3.0):
                    lastUuid = self.__getCurrentUuid()
                    self.__setCurrentUuid(None)
                    if not self.__checkForUuidFound(lastUuid):
                        eventsHandler.emit(ST_NAME_TTS_STACK_EMPTY, (lastUuid,
                            0.0))
                    continue
                eventsHandler.waitCondition(ST_NAME_TTS_SOUND_STATE, ("OFF",
                    None), 600.0)
                lastUuid = self.__getCurrentUuid()
                self.__setCurrentUuid(None)
                if not self.__checkForUuidFound(lastUuid):
                    eventsHandler.emit(ST_NAME_TTS_STACK_EMPTY, (lastUuid, 0.0))
            time.sleep(0.25)

    def __checkForUuidFound(self, uuid):
        result = False
        self.__stackMutex.acquire()
        for e in self.__stack:
            if e[3] == uuid:
                result = True
                break
        currentUuid = self.__getCurrentUuid()
        if currentUuid != None:
            if currentUuid == uuid:
                result = True
        self.__stackMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    def stackIsFilled(self, uuid):
        """Get if the stack contains texts from this uuid or not.
        @return: A boolean.
        """
        return self.__checkForUuidFound(uuid)

    def stackFlush(self):
        """Flush the TTS stack. (clear the pending speech)
        """
        uuidElementsList = []
        self.__stackMutex.acquire()
        for e in self.__stack:
            if e[3] not in uuidElementsList:
                uuidElementsList.append(e[3])
        currentUuid = self.__getCurrentUuid()
        if currentUuid != None:
            if currentUuid not in uuidElementsList:
                uuidElementsList.append(currentUuid)
        self.__stack = []
        self.__stackMutex.release()
        if len(uuidElementsList) > 0:
            resourceTuxOSL.ttsStop()
            eventsHandler.emit(ST_NAME_TTS_SOUND_STATE, ("OFF", 0.0))
            for uuid in uuidElementsList:
                eventsHandler.emit(ST_NAME_TTS_STACK_EMPTY, (uuid, 0.0))

    def stackRemoveByUuid(self, uuid):
        """Remove elements from the TTS stack.
        @param uuid: Uuid of the texts to remove.
        """
        haveUuidElement = False
        self.__stackMutex.acquire()
        newStack = []
        for e in self.__stack:
            if e[3] != uuid:
                newStack.append(e)
            else:
                haveUuidElement = True
        self.__stack = newStack
        if self.__currentUuid != None:
            if self.__currentUuid == uuid:
                haveUuidElement = True
        self.__stackMutex.release()
        if haveUuidElement:
            currentUuid = self.__getCurrentUuid()
            if currentUuid != None:
                if currentUuid == uuid:
                    resourceTuxOSL.ttsStop()
                    eventsHandler.emit(ST_NAME_TTS_SOUND_STATE, ("OFF", 0.0))
            eventsHandler.emit(ST_NAME_TTS_STACK_EMPTY, (uuid, 0.0))

    def stackFlushExceptedUuid(self, uuid):
        """Remove elements from the TTS stack excepted the ones from an uuid.
        @param uuid: Uuid.
        """
        uuidElementsList = []
        self.__stackMutex.acquire()
        for e in self.__stack:
            if e[3] != uuid:
                if e[3] not in uuidElementsList:
                    uuidElementsList.append(e[3])
        currentUuid = self.__getCurrentUuid()
        if currentUuid != None:
            if currentUuid not in uuidElementsList:
                if currentUuid != uuid:
                    uuidElementsList.append(currentUuid)
        newStack = []
        for e in self.__stack:
            if e[3] == uuid:
                newStack.append(e)
        self.__stack = newStack
        self.__stackMutex.release()
        if len(uuidElementsList) > 0:
            resourceTuxOSL.ttsStop()
            eventsHandler.emit(ST_NAME_TTS_SOUND_STATE, ("OFF", 0.0))
            for uuid in uuidElementsList:
                eventsHandler.emit(ST_NAME_TTS_STACK_EMPTY, (uuid, 0.0))

    def stackPush(self, text, locutor, pitch, uuid = "0"):
        """Push a speech in the stack.
        @param text: Text to speak.
        @param locutor: Locutor/voice.
        @param pitch: Pitch of the voice. <50..250>
        @param uuid: Uuid of the element which has pushed a text.
            Default "0"
        """
        if len(text) == 0:
            return
        def async():
            newFilling = not self.__checkForUuidFound(uuid)
            self.__stackMutex.acquire()
            if uuid != "0":
                indexToInsert = len(self.__stack)
                for i, e in enumerate(self.__stack):
                    if e[3] != uuid:
                        indexToInsert = i
                        break
                self.__stack.insert(indexToInsert,(text, locutor, pitch, uuid))
                if newFilling:
                    eventsHandler.emit(ST_NAME_TTS_STACK_FILLING, (uuid, 0.0))
                self.__stackMutex.release()
                if self.__getCurrentUuid() != uuid:
                    resourceTuxOSL.ttsStop()
            else:
                self.__stack.append((text, locutor, pitch, uuid))
                self.__stackMutex.release()
        t = threading.Thread(target = async)
        t.start()

    def stackNext(self):
        """Skip the current performed speech from the stack.
        """
        resourceTuxOSL.ttsStop()

# Create an instance of the resource
resourceTTS = TDSResourceTTS("resourceTTS")
# Register the resource into the resources manager
resourcesManager.addResource(resourceTTS)

# ------------------------------------------------------------------------------
# Declaration of the service "speak".
# ------------------------------------------------------------------------------
class TDSServiceTTSSpeak(TDSService):

    def configure(self):
        self.parametersDict = {
            'text' : 'string',
            'locutor' : 'string',
            'pitch' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "speak"
        self.comment = "Read a text with the text to speech engine."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceTTS.stackFlush()
        resourceTuxOSL.ttsSpeak(parameters['text'], parameters['locutor'],
            parameters['pitch'])
        return headersStruct, contentStruct

# Register the service into the resource
resourceTTS.addService(TDSServiceTTSSpeak)

# ------------------------------------------------------------------------------
# Declaration of the service "pause".
# ------------------------------------------------------------------------------
class TDSServiceTTSPause(TDSService):

    def configure(self):
        self.parametersDict = {
            'value' : '<True|False>',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "pause"
        self.comment = "Set the pause state of the current speech."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceTuxOSL.ttsPause(parameters['value'])
        return headersStruct, contentStruct

# Register the service into the resource
resourceTTS.addService(TDSServiceTTSPause)

# ------------------------------------------------------------------------------
# Declaration of the service "stop".
# ------------------------------------------------------------------------------
class TDSServiceTTSStop(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop"
        self.comment = "Stop the current speech."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceTTS.stackFlush()
        resourceTuxOSL.ttsStop()
        return headersStruct, contentStruct

# Register the service into the resource
resourceTTS.addService(TDSServiceTTSStop)
# Bind "stack_flush" to this service
resourcesManager.addBinding("tts/stack_flush", "tts", "stop")

# ------------------------------------------------------------------------------
# Declaration of the service "voices".
# ------------------------------------------------------------------------------
class TDSServiceTTSVoices(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "voices"
        self.comment = "Get the voice list."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        voices = resourceTuxOSL.ttsVoicesList()
        for i, voice in enumerate(voices):
            d_name = "data|%d" % i
            contentStruct['root'][d_name] = {'locutor' : voice,}
        return headersStruct, contentStruct

# Register the service into the resource
resourceTTS.addService(TDSServiceTTSVoices)

# ------------------------------------------------------------------------------
# Declaration of the service "stack_speak".
# ------------------------------------------------------------------------------
class TDSServiceTTSStackSpeak(TDSService):

    def configure(self):
        self.parametersDict = {
            'text' : 'string',
            'locutor' : 'string',
            'pitch' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stack_speak"
        self.comment = "Send a text in the TTS stack."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceTTS.stackPush(parameters['text'], parameters['locutor'],
            parameters['pitch'])
        return headersStruct, contentStruct

# Register the service into the resource
resourceTTS.addService(TDSServiceTTSStackSpeak)

# ------------------------------------------------------------------------------
# Declaration of the service "stack_next".
# ------------------------------------------------------------------------------
class TDSServiceTTSStackNext(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stack_next"
        self.comment = "Skip the current tts sentence in the stack."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceTTS.stackNext()
        return headersStruct, contentStruct

# Register the service into the resource
resourceTTS.addService(TDSServiceTTSStackNext)
