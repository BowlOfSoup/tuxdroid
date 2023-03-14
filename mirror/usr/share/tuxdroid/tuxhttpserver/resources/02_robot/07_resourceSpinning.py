# ==============================================================================
# Spinning resource.
# ==============================================================================

# This resource depends of the following resources :
# - resourceTuxDriver

# ------------------------------------------------------------------------------
# Declaration of the resource "spinning".
# ------------------------------------------------------------------------------
class TDSResourceSpinning(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "spinning"
        self.comment = "Resource to control the spinning of Tux Droid."
        self.fileName = RESOURCE_FILENAME
        
# Create an instance of the resource
resourceSpinning = TDSResourceSpinning("resourceSpinning")
# Register the resource into the resources manager
resourcesManager.addResource(resourceSpinning)

# ------------------------------------------------------------------------------
# Declaration of the service "left_on".
# ------------------------------------------------------------------------------
class TDSServiceSpinningLeftOn(TDSService):

    def configure(self):
        self.parametersDict = {
            'count' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "left_on"
        self.comment = "Perform a rotation to the left."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.spinLeftOn(parameters['count']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceSpinning.addService(TDSServiceSpinningLeftOn)

# ------------------------------------------------------------------------------
# Declaration of the service "right_on".
# ------------------------------------------------------------------------------
class TDSServiceSpinningRightOn(TDSService):

    def configure(self):
        self.parametersDict = {
            'count' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "right_on"
        self.comment = "Perform a rotation to the right."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.spinRightOn(parameters['count']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceSpinning.addService(TDSServiceSpinningRightOn)

# ------------------------------------------------------------------------------
# Declaration of the service "left_on_during".
# ------------------------------------------------------------------------------
class TDSServiceSpinningLeftOnDuring(TDSService):

    def configure(self):
        self.parametersDict = {
            'duration' : 'float',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "left_on_during"
        self.comment = "Perform a rotation to the left."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.spinLeftOnDuring(parameters['duration']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceSpinning.addService(TDSServiceSpinningLeftOnDuring)

# ------------------------------------------------------------------------------
# Declaration of the service "right_on_during".
# ------------------------------------------------------------------------------
class TDSServiceSpinningRightOnDuring(TDSService):

    def configure(self):
        self.parametersDict = {
            'duration' : 'float',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "right_on_during"
        self.comment = "Perform a rotation to the right."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.spinRightOnDuring(parameters['duration']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceSpinning.addService(TDSServiceSpinningRightOnDuring)

# ------------------------------------------------------------------------------
# Declaration of the service "off".
# ------------------------------------------------------------------------------
class TDSServiceSpinningOff(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "off"
        self.comment = "Stop the rotation."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.spinningOff():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceSpinning.addService(TDSServiceSpinningOff)

# ------------------------------------------------------------------------------
# Declaration of the service "speed".
# ------------------------------------------------------------------------------
class TDSServiceSpinningSpeed(TDSService):

    def configure(self):
        self.parametersDict = {
            'value' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "speed"
        self.comment = "Set the speed of the rotation."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.setSpinningSpeed(parameters['value']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceSpinning.addService(TDSServiceSpinningSpeed)
