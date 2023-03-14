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
# Declaration of the resource "client".
# ==============================================================================
class TDSResourceClient(TDSResource):
    """Resource client class.
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
        self.name = "client"
        self.comment = "Resource to manage the clients."
        self.fileName = RESOURCE_FILENAME

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Create a new client.
    # --------------------------------------------------------------------------
    def createClient(self, clientName, clientLevel):
        """Create a new client.
        @clientName: Client name.
        @clientLevel: Client level.
            -1 : ANONYMOUS
            0  : FREE
            1  : RESTRICTED
            2  : ROOT
        @return: The id of the new client or -1 if fail.
        """
        if clientLevel == TDS_CLIENT_LEVEL_ANONYMOUS:
            return -1
        idClient = clientsManager.addRESTClient(clientName, clientLevel)
        return idClient

    # --------------------------------------------------------------------------
    # Destroy a client.
    # --------------------------------------------------------------------------
    def destroyClient(self, idClient):
        """Destroy a client.
        - This function only affect the HTTP/REST clients.
        @idClient: Client id.
        """
        clientsManager.removeRESTClient(idClient)

    # --------------------------------------------------------------------------
    # Get the clients listing with their informations.
    # --------------------------------------------------------------------------
    def listing(self):
        """Get the clients listing with their informations.
        @return: A dictionary.
        """
        clientsInfo = clientsManager.getClientsInfo()
        result = {}
        for i, clientInfo in enumerate(clientsInfo):
            nodeName = "data|%d" % i
            result[nodeName] = clientInfo
        return result

# Create an instance of the resource
resourceClient = TDSResourceClient("resourceClient")
# Register the resource into the resources manager
resourcesManager.addResource(resourceClient)

# ==============================================================================
# ******************************************************************************
# SERVICES DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the service "create".
# ==============================================================================
class TDSServiceClientCreate(TDSService):
    """Create a client.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'name' : 'string',
            'level' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "create"
        self.comment = "Create a client."

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
        idClient = resourceClient.createClient(parameters['name'],
            parameters['level'])
        if idClient == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = {}
            contentStruct['root']['data']['client_id'] = idClient
        return headersStruct, contentStruct

# Register the service into the resource
resourceClient.addService(TDSServiceClientCreate)

# ==============================================================================
# Declaration of the service "destroy".
# ==============================================================================
class TDSServiceClientDestroy(TDSService):
    """Destroy a client.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_FREE
        self.exclusiveExecution = False
        self.name = "destroy"
        self.comment = "Destroy a client."

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
        resourceClient.destroyClient(id)
        return headersStruct, contentStruct

# Register the service into the resource
resourceClient.addService(TDSServiceClientDestroy)

# ==============================================================================
# Declaration of the service "listing".
# ==============================================================================
class TDSServiceClientListing(TDSService):
    """Get the clients listing with their informations.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_FREE
        self.exclusiveExecution = False
        self.name = "listing"
        self.comment = "Get the clients listing with their informations."

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
        contentStruct['root']['data'] =  resourceClient.listing()
        return headersStruct, contentStruct

# Register the service into the resource
resourceClient.addService(TDSServiceClientListing)
