#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

# ==============================================================================
# ******************************************************************************
# RESOURCE DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the resource "server".
# ==============================================================================
class TDSResourceServer(TDSResource):
    """Resource server class.
    """

    # ==========================================================================
    # Inherited methods from TDSResource
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Configure the resource.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the resource.
        """
        self.name = "server"
        self.comment = "Resource to manage the server."
        self.fileName = RESOURCE_FILENAME

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Stop the server.
    # --------------------------------------------------------------------------
    def stopServer(self):
        """Stop the server.
        """
        httpServer.stop()

    # --------------------------------------------------------------------------
    # Restart the server.
    # --------------------------------------------------------------------------
    def restartServer(self):
        """Restart the server.
        """
        # TODO: Restart on linux
        if os.name == 'nt':
            t = threading.Thread(target = os.system,
                args = ["smart_server_restart.exe",])
            t.start()

    # --------------------------------------------------------------------------
    # Get the server version.
    # --------------------------------------------------------------------------
    def getVersion(self):
        """Get the server version.
        @return: The server version.
        """
        return serverVersion

# Create an instance of the resource
resourceServer = TDSResourceServer("resourceServer")
# Register the resource into the resources manager
resourcesManager.addResource(resourceServer)

# ==============================================================================
# ******************************************************************************
# SERVICES DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the service "stop".
# ==============================================================================
class TDSServiceServerStop(TDSService):

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "stop"
        self.comment = "Stop the server."

    # --------------------------------------------------------------------------
    # Execute the service.
    # --------------------------------------------------------------------------
    def execute(self, id, parameters):
        """Execute the service.
        @param id: Client identifier.
        @param parameters: Request parameters.
        @return: The headers as list and the content dictionary of the request
            answer.
        """
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceServer.stopServer()
        return headersStruct, contentStruct

# Register the service into the resource
resourceServer.addService(TDSServiceServerStop)

# ==============================================================================
# Declaration of the service "restart".
# ==============================================================================
class TDSServiceServerRestart(TDSService):

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "restart"
        self.comment = "Restart the server."

    # --------------------------------------------------------------------------
    # Execute the service.
    # --------------------------------------------------------------------------
    def execute(self, id, parameters):
        """Execute the service.
        @param id: Client identifier.
        @param parameters: Request parameters.
        @return: The headers as list and the content dictionary of the request
            answer.
        """
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceServer.restartServer()
        return headersStruct, contentStruct

# Register the service into the resource
resourceServer.addService(TDSServiceServerRestart)

# ==============================================================================
# Declaration of the service "version".
# ==============================================================================
class TDSServiceServerVersion(TDSService):

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "version"
        self.comment = "Get the server version."

    # --------------------------------------------------------------------------
    # Execute the service.
    # --------------------------------------------------------------------------
    def execute(self, id, parameters):
        """Execute the service.
        @param id: Client identifier.
        @param parameters: Request parameters.
        @return: The headers as list and the content dictionary of the request
            answer.
        """
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        data = {'version' : resourceServer.getVersion()}
        contentStruct['root']['data'] = data
        return headersStruct, contentStruct

# Register the service into the resource
resourceServer.addService(TDSServiceServerVersion)
