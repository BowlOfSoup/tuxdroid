# ==============================================================================
# Leds resource.
# ==============================================================================

# ------------------------------------------------------------------------------
# Declaration of the resource "leds".
# ------------------------------------------------------------------------------
class TDSResourceLeds(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "leds"
        self.comment = "Resource to control the blue leds of Tux Droid."
        self.fileName = RESOURCE_FILENAME

# Create an instance of the resource
resourceLeds = TDSResourceLeds("resourceLeds")
# Register the resource into the resources manager
resourcesManager.addResource(resourceLeds)

# ------------------------------------------------------------------------------
# Declaration of the service "blink".
# ------------------------------------------------------------------------------
class TDSServiceLedsBlink(TDSService):

    def configure(self):
        self.parametersDict = {
            'leds' : '<LED_BOTH|LED_RIGHT|LED_LEFT>',
            'count' : 'uint8',
            'delay' : 'float',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "blink"
        self.comment = "Perform a blinking a the blue leds."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.ledsBlink(parameters['leds'],
            parameters['count'], parameters['delay']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceLeds.addService(TDSServiceLedsBlink)

# ------------------------------------------------------------------------------
# Declaration of the service "off".
# ------------------------------------------------------------------------------
class TDSServiceLedsOff(TDSService):

    def configure(self):
        self.parametersDict = {
            'leds' : '<LED_BOTH|LED_RIGHT|LED_LEFT>',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "off"
        self.comment = "Turn off the blue leds."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.ledsOff(parameters['leds']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceLeds.addService(TDSServiceLedsOff)

# ------------------------------------------------------------------------------
# Declaration of the service "on".
# ------------------------------------------------------------------------------
class TDSServiceLedsOn(TDSService):

    def configure(self):
        self.parametersDict = {
            'leds' : '<LED_BOTH|LED_RIGHT|LED_LEFT>',
            'intensity' : 'float',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "on"
        self.comment = "Turn on the blue leds."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.ledsOn(parameters['leds'],
            parameters['intensity']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceLeds.addService(TDSServiceLedsOn)

# ------------------------------------------------------------------------------
# Declaration of the service "set".
# ------------------------------------------------------------------------------
class TDSServiceLedsSet(TDSService):

    def configure(self):
        self.parametersDict = {
            'leds' : '<LED_BOTH|LED_RIGHT|LED_LEFT>',
            'intensity' : 'float',
            'fx_type' : '<UNAFFECTED|LAST|NONE|DEFAULT|FADE_DURATION|FADE_RATE|GRADIENT_NBR|GRADIENT_DELTA>',
            'fx_speed' : 'float',
            'fx_step' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "set"
        self.comment = "Set the state of the leds."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.ledsSet(parameters['leds'],
            parameters['intensity'], parameters['fx_type'],
            parameters['fx_speed'], parameters['fx_step']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceLeds.addService(TDSServiceLedsSet)

# ------------------------------------------------------------------------------
# Declaration of the service "pulse".
# ------------------------------------------------------------------------------
class TDSServiceLedsPulse(TDSService):

    def configure(self):
        self.parametersDict = {
            'leds' : '<LED_BOTH|LED_RIGHT|LED_LEFT>',
            'min_intensity' : 'float',
            'max_intensity' : 'float',
            'count' : 'uint8',
            'period' : 'float',
            'fx_type' : '<UNAFFECTED|LAST|NONE|DEFAULT|FADE_DURATION|FADE_RATE|GRADIENT_NBR|GRADIENT_DELTA>',
            'fx_speed' : 'float',
            'fx_step' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "pulse"
        self.comment = "Set a pulsing effect to the leds."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceTuxDriver.ledsPulse(parameters['leds'],
            parameters['min_intensity'], parameters['max_intensity'],
            parameters['count'], parameters['period'], parameters['fx_type'],
            parameters['fx_speed'], parameters['fx_step']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        cmdRsp = {'cmd_answer' : 0}
        contentStruct['root']['data'] = cmdRsp
        return headersStruct, contentStruct

# Register the service into the resource
resourceLeds.addService(TDSServiceLedsPulse)
