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
# Declaration of the resource "access".
# ==============================================================================
class TDSResourceAccess(TDSResource):
    """Resource access class.
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
        self.name = "access"
        self.comment = "Resource to manage the access to the robot resources."
        self.fileName = RESOURCE_FILENAME

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Acquire the access to the robot resources.
    # --------------------------------------------------------------------------
    def acquireAccess(self, idClient, priorityLevel):
        """Acquire the access to the robot resources.
        - This function only affects the RESTRICTED clients
        @param idClient: Id client.
        @param priorityLevel: Priority level.
            0 : LOW
            1 : NORMAL
            2 : HIGH
            3 : CRITICAL
        @return: True or False
        """
        client = clientsManager.getClient(idClient)
        if client == None:
            return False
        return client.acquireAccess(priorityLevel)

    # --------------------------------------------------------------------------
    # Release the access to the robot resources.
    # --------------------------------------------------------------------------
    def releaseAccess(self, idClient):
        """Release the access to the robot resources.
        - This function only affects the RESTRICTED clients
        @param idClient: Id client.
        """
        accessManager.releaseAccess(idClient)

    # --------------------------------------------------------------------------
    # Forcing to release the access to the robot resources.
    # --------------------------------------------------------------------------
    def forcingReleaseAccess(self):
        """Forcing to release the access to the robot resources.
        - This function only affects the RESTRICTED clients
        - This function should be called by only the ROOT client
        """
        accessManager.releaseAccess()

    # --------------------------------------------------------------------------
    # Forcing to acquire the access to the robot resources.
    # --------------------------------------------------------------------------
    def forcingAcquireAccess(self, idClient, priorityLevel):
        """Forcing to acquire the access to the robot resources.
        - This function only affects the RESTRICTED clients
        - This function should be called by only the ROOT client
        @param idClient: Id client.
        @param priorityLevel: Priority level.
            0 : LOW
            1 : NORMAL
            2 : HIGH
            3 : CRITICAL
        @return: True or False
        """
        accessManager.releaseAccess()
        return accessManager.acquireAccess(idClient, priorityLevel)

    # --------------------------------------------------------------------------
    # Lock the access to the robot resources.
    # --------------------------------------------------------------------------
    def lockAccess(self):
        """Lock the access to the robot resources.
        - This function only affects the RESTRICTED clients
        - This function should be called by only the ROOT client
        """
        accessManager.setLocked(True)

    # --------------------------------------------------------------------------
    # Lock the access to the robot resources.
    # --------------------------------------------------------------------------
    def unlockAccess(self):
        """Lock the access to the robot resources.
        - This function only affects the RESTRICTED clients
        - This function should be called by only the ROOT client
        """
        accessManager.setLocked(False)

# Create an instance of the resource
resourceAccess = TDSResourceAccess("resourceAccess")
# Register the resource into the resources manager
resourcesManager.addResource(resourceAccess)

# ==============================================================================
# ******************************************************************************
# SERVICES DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the service "acquire".
# ==============================================================================
class TDSServiceAccessAcquire(TDSService):
    """Acquire the access to the robot resources.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'priority_level' : 'int',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_RESTRICTED
        self.exclusiveExecution = False
        self.name = "acquire"
        self.comment = "Acquire the access to the robot resources."

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
        if not resourceAccess.acquireAccess(id, parameters['priority_level']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAccess.addService(TDSServiceAccessAcquire)

# ==============================================================================
# Declaration of the service "release".
# ==============================================================================
class TDSServiceAccessRelease(TDSService):
    """Release the access to the robot resources.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_RESTRICTED
        self.exclusiveExecution = False
        self.name = "release"
        self.comment = "Release the access to the robot resources."

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
        resourceAccess.releaseAccess(id)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAccess.addService(TDSServiceAccessRelease)

# ==============================================================================
# Declaration of the service "forcing_release".
# ==============================================================================
class TDSServiceAccessForcingRelease(TDSService):
    """Forcing to release the access to the robot resources.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ROOT
        self.exclusiveExecution = False
        self.name = "forcing_release"
        self.comment = "Forcing to release the access to the robot resources."

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
        resourceAccess.forcingReleaseAccess()
        return headersStruct, contentStruct

# Register the service into the resource
resourceAccess.addService(TDSServiceAccessForcingRelease)

# ==============================================================================
# Declaration of the service "forcing_acquire".
# ==============================================================================
class TDSServiceAccessForcingAcquire(TDSService):
    """Forcing to acquire the access to the robot resources.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'id_client' : 'string',
            'priority_level' : 'int',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ROOT
        self.exclusiveExecution = False
        self.name = "forcing_acquire"
        self.comment = "Forcing to acquire the access to the robot resources."

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
        if not resourceAccess.forcingAcquireAccess(parameters['id_client'],
            parameters['priority_level']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceAccess.addService(TDSServiceAccessForcingAcquire)

# ==============================================================================
# Declaration of the service "lock".
# ==============================================================================
class TDSServiceAccessLock(TDSService):
    """Lock the access to the robot resources.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ROOT
        self.exclusiveExecution = False
        self.name = "lock"
        self.comment = "Lock the access to the robot resources."

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
        resourceAccess.lockAccess()
        return headersStruct, contentStruct

# Register the service into the resource
resourceAccess.addService(TDSServiceAccessLock)

# ==============================================================================
# Declaration of the service "unlock".
# ==============================================================================
class TDSServiceAccessUnlock(TDSService):
    """Unlock the access to the robot resources.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ROOT
        self.exclusiveExecution = False
        self.name = "unlock"
        self.comment = "Unlock the access to the robot resources."

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
        resourceAccess.unlockAccess()
        return headersStruct, contentStruct

# Register the service into the resource
resourceAccess.addService(TDSServiceAccessUnlock)
