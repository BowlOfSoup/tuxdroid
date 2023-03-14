# ==============================================================================
# Mouth resource.
# ==============================================================================

# This resource depends of the following resources :
# - resourceTuxDriver

# ------------------------------------------------------------------------------
# Declaration of the resource "mouth".
# ------------------------------------------------------------------------------
class TDSResourceMouth(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "mouth"
        self.comment = "Resource to control the mouth of Tux Droid."
        self.fileName = RESOURCE_FILENAME

# Create an instance of the resource
resourceMouth = TDSResourceMouth("resourceMouth")
# Register the resource into the resources manager
resourcesManager.addResource(resourceMouth)

# ------------------------------------------------------------------------------
# Declaration of the service "open".
# ------------------------------------------------------------------------------
class TDSServiceMouthOpen(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "open"
        self.comment = "Open the mouth."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.openMouth():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceMouth.addService(TDSServiceMouthOpen)

# ------------------------------------------------------------------------------
# Declaration of the service "close".
# ------------------------------------------------------------------------------
class TDSServiceMouthClose(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "close"
        self.comment = "Close the mouth."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.closeMouth():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceMouth.addService(TDSServiceMouthClose)

# ------------------------------------------------------------------------------
# Declaration of the service "on".
# ------------------------------------------------------------------------------
class TDSServiceMouthOn(TDSService):

    def configure(self):
        self.parametersDict = {
            'count' : 'uint8',
            'final_state' : '<NDEF|OPEN|CLOSE>',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "on"
        self.comment = "Perform a movement of the mouth."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.mouthOn(parameters['count'],
            parameters['final_state']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceMouth.addService(TDSServiceMouthOn)

# ------------------------------------------------------------------------------
# Declaration of the service "on_during".
# ------------------------------------------------------------------------------
class TDSServiceMouthOnDuring(TDSService):

    def configure(self):
        self.parametersDict = {
            'duration' : 'float',
            'final_state' : '<NDEF|OPEN|CLOSE>',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "on_during"
        self.comment = "Perform a movement of the mouth."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.mouthOnDuring(parameters['duration'],
            parameters['final_state']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceMouth.addService(TDSServiceMouthOnDuring)

# ------------------------------------------------------------------------------
# Declaration of the service "off".
# ------------------------------------------------------------------------------
class TDSServiceMouthOff(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "off"
        self.comment = "Stop the movement of the mouth."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.mouthOff():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceMouth.addService(TDSServiceMouthOff)