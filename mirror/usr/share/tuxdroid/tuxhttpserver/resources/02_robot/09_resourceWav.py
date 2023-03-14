# ==============================================================================
# Wav resource.
# ==============================================================================

# This resource depends of the following resources:
# - resourceTuxOSL

# ------------------------------------------------------------------------------
# Declaration of the resource "wav".
# ------------------------------------------------------------------------------
class TDSResourceWav(TDSResource):

    def configure(self):
        self.name = "wav"
        self.comment = "Resource to manage the wave files playing."
        self.fileName = RESOURCE_FILENAME

# Create an instance of the resource
resourceWav = TDSResourceWav("resourceWav")
# Register the resource into the resources manager
resourcesManager.addResource(resourceWav)

# ------------------------------------------------------------------------------
# Declaration of the service "play".
# ------------------------------------------------------------------------------
class TDSServiceWavPlay(TDSService):

    def configure(self):
        self.parametersDict = {
            'path' : 'string',
            'begin' : 'float',
            'end' : 'float',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "play"
        self.comment = "Play a wave file (Sample rate : 8000, Mono, U8)."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        idx = resourceTuxOSL.wavPlay(parameters['path'], parameters['begin'],
            parameters['end'])
        if idx == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : idx}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceWav.addService(TDSServiceWavPlay)

# ------------------------------------------------------------------------------
# Declaration of the service "pause".
# ------------------------------------------------------------------------------
class TDSServiceWavPause(TDSService):

    def configure(self):
        self.parametersDict = {
            'value' : '<True|False>',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "pause"
        self.comment = "Set the pause state of the wave player."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxOSL.wavPause(parameters['value']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceWav.addService(TDSServiceWavPause)

# ------------------------------------------------------------------------------
# Declaration of the service "stop".
# ------------------------------------------------------------------------------
class TDSServiceWavStop(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop"
        self.comment = "Stop the wave player."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxOSL.wavStop():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceWav.addService(TDSServiceWavStop)
