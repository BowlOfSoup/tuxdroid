# ==============================================================================
# Macro resource.
# ==============================================================================

# This resource depends of the following resources :
# - resourceTuxDriver
# - resourceTuxOSL

# ------------------------------------------------------------------------------
# Declaration of the resource "macro".
# ------------------------------------------------------------------------------
class TDSResourceMacro(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "macro"
        self.comment = "Resource to manage the macro commands."
        self.fileName = RESOURCE_FILENAME
        
    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def playMacro(self, macro):
        """Play a macro text.
        @param macro: Macro text.
        @return: True or False.
        """
        if not resourceTuxDriver.getDonglePlugged():
            return False
        resourceTuxOSL.clearAll()
        resourceTuxDriver.clearAll()
        macro = macro.replace("|", "\n")
        macro = resourceTuxOSL.reencodeTTSTextInMacro(macro)
        if len(macro) <= 16384:
            resourceTuxDriver.executeMacro(macro)
            resourceTuxOSL.executeMacro(macro)
        else:
            return False
        return True
        
    def stopMacro(self):
        """Stop the current played macro.
        """
        def async():
            resourceTuxOSL.clearAll()
            resourceTuxDriver.clearAll()
        t = threading.Thread(target = async)
        t.start()

# Create an instance of the resource
resourceMacro = TDSResourceMacro("resourceMacro")
# Register the resource into the resources manager
resourcesManager.addResource(resourceMacro)

# ------------------------------------------------------------------------------
# Declaration of the service "play".
# ------------------------------------------------------------------------------
class TDSServiceMacroPlay(TDSService):

    def configure(self):
        self.parametersDict = {
            'macro' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "play"
        self.comment = "Play a macro."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceMacro.playMacro(parameters['macro']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceMacro.addService(TDSServiceMacroPlay)

# ------------------------------------------------------------------------------
# Declaration of the service "stop".
# ------------------------------------------------------------------------------
class TDSServiceMacroStop(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop"
        self.comment = "Stop a macro."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceMacro.stopMacro():
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceMacro.addService(TDSServiceMacroStop)