# ==============================================================================
# Eyes resource.
# ==============================================================================

# This resource depends of the following resources :
# - resourceTuxDriver

# ------------------------------------------------------------------------------
# Declaration of the resource "eyes".
# ------------------------------------------------------------------------------
class TDSResourceEyes(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "eyes"
        self.comment = "Resource to control the eyes of Tux Droid."
        self.fileName = RESOURCE_FILENAME

# Create an instance of the resource
resourceEyes = TDSResourceEyes("resourceEyes")
# Register the resource into the resources manager
resourcesManager.addResource(resourceEyes)

# ------------------------------------------------------------------------------
# Declaration of the service "open".
# ------------------------------------------------------------------------------
class TDSServiceEyesOpen(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "open"
        self.comment = "Open the eyes."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.openEyes():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceEyes.addService(TDSServiceEyesOpen)

# ------------------------------------------------------------------------------
# Declaration of the service "close".
# ------------------------------------------------------------------------------
class TDSServiceEyesClose(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "close"
        self.comment = "Close the eyes."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.closeEyes():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceEyes.addService(TDSServiceEyesClose)

# ------------------------------------------------------------------------------
# Declaration of the service "on".
# ------------------------------------------------------------------------------
class TDSServiceEyesOn(TDSService):

    def configure(self):
        self.parametersDict = {
            'count' : 'uint8',
            'final_state' : '<NDEF|OPEN|CLOSE>',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "on"
        self.comment = "Perform a movement of the eyes."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.eyesOn(parameters['count'],
            parameters['final_state']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceEyes.addService(TDSServiceEyesOn)

# ------------------------------------------------------------------------------
# Declaration of the service "on_during".
# ------------------------------------------------------------------------------
class TDSServiceEyesOnDuring(TDSService):

    def configure(self):
        self.parametersDict = {
            'duration' : 'float',
            'final_state' : '<NDEF|OPEN|CLOSE>',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "on_during"
        self.comment = "Perform a movement of the eyes."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.eyesOnDuring(parameters['duration'],
            parameters['final_state']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceEyes.addService(TDSServiceEyesOnDuring)

# ------------------------------------------------------------------------------
# Declaration of the service "off".
# ------------------------------------------------------------------------------
class TDSServiceEyesOff(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "off"
        self.comment = "Stop the movement of the eyes."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.eyesOff():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceEyes.addService(TDSServiceEyesOff)