# ==============================================================================
# Flippers resource.
# ==============================================================================

# This resource depends of the following resources :
# - resourceTuxDriver

# ------------------------------------------------------------------------------
# Declaration of the resource "flippers".
# ------------------------------------------------------------------------------
class TDSResourceFlippers(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "flippers"
        self.comment = "Resource to control the flippers of Tux Droid."
        self.fileName = RESOURCE_FILENAME

# Create an instance of the resource
resourceFlippers = TDSResourceFlippers("resourceFlippers")
# Register the resource into the resources manager
resourcesManager.addResource(resourceFlippers)

# ------------------------------------------------------------------------------
# Declaration of the service "up".
# ------------------------------------------------------------------------------
class TDSServiceFlippersUp(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "up"
        self.comment = "Up the flippers."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.upFlippers():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceFlippers.addService(TDSServiceFlippersUp)

# ------------------------------------------------------------------------------
# Declaration of the service "down".
# ------------------------------------------------------------------------------
class TDSServiceFlippersDown(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "down"
        self.comment = "Down the flippers."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.downFlippers():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceFlippers.addService(TDSServiceFlippersDown)

# ------------------------------------------------------------------------------
# Declaration of the service "on".
# ------------------------------------------------------------------------------
class TDSServiceFlippersOn(TDSService):

    def configure(self):
        self.parametersDict = {
            'count' : 'uint8',
            'final_state' : '<NDEF|UP|DOWN>',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "on"
        self.comment = "Perform a movement of the flippers."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.flippersOn(parameters['count'],
            parameters['final_state']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceFlippers.addService(TDSServiceFlippersOn)

# ------------------------------------------------------------------------------
# Declaration of the service "on_during".
# ------------------------------------------------------------------------------
class TDSServiceFlippersOnDuring(TDSService):

    def configure(self):
        self.parametersDict = {
            'duration' : 'float',
            'final_state' : '<NDEF|UP|DOWN>',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "on_during"
        self.comment = "Perform a movement of the flippers."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.flippersOnDuring(parameters['duration'],
            parameters['final_state']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceFlippers.addService(TDSServiceFlippersOnDuring)

# ------------------------------------------------------------------------------
# Declaration of the service "off".
# ------------------------------------------------------------------------------
class TDSServiceFlippersOff(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "off"
        self.comment = "Stop the movement of the flippers."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.flippersOff():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceFlippers.addService(TDSServiceFlippersOff)

# ------------------------------------------------------------------------------
# Declaration of the service "speed".
# ------------------------------------------------------------------------------
class TDSServiceFlippersSpeed(TDSService):

    def configure(self):
        self.parametersDict = {
            'value' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "speed"
        self.comment = "Set the speed of the flippers."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.setFlippersSpeed(parameters['value']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceFlippers.addService(TDSServiceFlippersSpeed)
