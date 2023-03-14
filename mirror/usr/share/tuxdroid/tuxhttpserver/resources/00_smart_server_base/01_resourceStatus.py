#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

SW_NAME_EXTERNAL_STATUS = "external_status"

# ==============================================================================
# ******************************************************************************
# RESOURCE DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the resource "status".
# ==============================================================================
class TDSResourceStatus(TDSResource):
    """Resource status class.
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
        self.name = "status"
        self.comment = "Resource to manage the statuses and events."
        self.fileName = RESOURCE_FILENAME

        # Registering the "external" status in the events handler
        eventsHandler.insert(SW_NAME_EXTERNAL_STATUS)
        # Registering the "external" status in the default excluded events list
        clientsManager.addDefaultExcludedEvent(SW_NAME_EXTERNAL_STATUS)

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Get the last events from a client stack.
    # --------------------------------------------------------------------------
    def getEvents(self, idClient):
        """Get the last events from a client stack.
        - This function only affect the HTTP/REST clients.
        @param idClient: Id client.
        @return: The events from the client stack as list.
        """
        client = clientsManager.getClient(idClient)
        if client == None:
            return []
        return client.popEvents()

    # --------------------------------------------------------------------------
    # Request the current state of a status.
    # --------------------------------------------------------------------------
    def requestOne(self, statusName):
        """Request the current state of a status.
        @param statusName: Name of the status.
        @return: The current state of the status as dictionary.
        """
        eventHandler = eventsHandler.getEventHandler(statusName)
        if eventHandler == None:
            return None
        else:
            stateStruct = eventHandler.getLastState()
            if stateStruct != None:
                state = {
                    'name' : statusName,
                    'value' : stateStruct[0],
                    'delay' : stateStruct[1],
                }
            else:
                state = {
                    'name' : statusName,
                    'value' : '',
                    'delay' : 0.0,
                }
            return state

    # --------------------------------------------------------------------------
    # Request the current state of all statuses.
    # --------------------------------------------------------------------------
    def requestAll(self):
        """Request the current state of all statuses.
        @return: The current state of all statuses as dictionary.
        """
        eventsNameList = eventsHandler.getEventsNameList()
        states = []
        for eventName in eventsNameList:
            state = self.requestOne(eventName)
            if state != None:
                states.append(state)
        return states

    # --------------------------------------------------------------------------
    # Send a free status.
    # --------------------------------------------------------------------------
    def sendStatus(self, name, value):
        """Send a free status.
        - This function inject a status in the events handler. This kind of
        statuses are handled in the special event handler named
        "SW_NAME_EXTERNAL_STATUS" because their names are not knowed by the
        server.
        @param name: Status name.
        @param value: Status value.
        """
        statusStruct = {}
        statusStruct['name'] = SW_NAME_EXTERNAL_STATUS
        statusStruct['value'] = "%s|%s" % (name, value)
        statusStruct['delay'] = 0.0
        statusStruct['type'] = "string"
        def async():
            eventsHandler.emit(statusStruct['name'], (statusStruct['value'],
                float(statusStruct['delay'])))
            clientsManager.pushEvents([statusStruct,])
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Publish events through the events handler.
    # --------------------------------------------------------------------------
    def publishEvents(self, sendToClients, eventName, eventValues = []):
        """Publish events through the events handler.
        @param sendToClients: Send or not the the api clients.
        @param eventName: Event name.
        @param eventValues: Values as string array.
        """
        def async():
            values = ""
            for value in eventValues:
                values += value + ":"
            if len(values) > 0:
                values = values[:-1]
            eventStruct = {
                'name' : eventName,
                'value' : values,
                'delay' : "0.0",
                'type' : "string"
            }
            if sendToClients:
                clientsManager.pushEvents([eventStruct,])
            eventsHandler.emit(eventName, (values, 0.0))
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Add an event in the excluded events list of a client.
    # --------------------------------------------------------------------------
    def addExcludedEvent(self, idClient, eventName):
        """Add an event in the excluded events list of a client.
        - The effect is that the event/status will be anymore sent to this
        client.
        @idClient: Client id.
        @eventName: Status/event name.
        """
        def async():
            client = clientsManager.getClient(idClient)
            if client != None:
                client.addExcludedEvent(eventName)
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Remove an event from the excluded events list of a client.
    # --------------------------------------------------------------------------
    def removeExcludedEvent(self, idClient, eventName):
        """Remove an event from the excluded events list of a client.
        @idClient: Client id.
        @eventName: Status/event name.
        """
        def async():
            client = clientsManager.getClient(idClient)
            if client != None:
                client.removeExcludedEvent(eventName)
        t = threading.Thread(target = async)
        t.start()

# Create an instance of the resource
resourceStatus = TDSResourceStatus("resourceStatus")
# Register the resource into the resources manager
resourcesManager.addResource(resourceStatus)

# ==============================================================================
# ******************************************************************************
# SERVICES DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the service "events".
# ==============================================================================
class TDSServiceStatusEvents(TDSService):
    """Get the last events from a client stack.
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
        self.name = "events"
        self.comment = "Get the last events from a client stack."

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
        events = resourceStatus.getEvents(id)
        if len(events) > 0:
            i = 0
            for event in events:
                data_name = "data|%d" % i
                i += 1
                contentStruct['root'][data_name] = event
        return headersStruct, contentStruct

# Register the service into the resource
resourceStatus.addService(TDSServiceStatusEvents)

# ==============================================================================
# Declaration of the service "request_one".
# ==============================================================================
class TDSServiceStatusRequestOne(TDSService):
    """Request the current state of a status.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'status_name' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "request_one"
        self.comment = "Request the current state of a status."

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
        state = resourceStatus.requestOne(parameters['status_name'])
        if state == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = state
        return headersStruct, contentStruct

# Register the service into the resource
resourceStatus.addService(TDSServiceStatusRequestOne)

# ==============================================================================
# Declaration of the service "request_all".
# ==============================================================================
class TDSServiceStatusRequestAll(TDSService):
    """Request the current state of all statuses.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "request_all"
        self.comment = "Request the current state of all statuses."

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
        states = resourceStatus.requestAll()
        i = 0
        for state in states:
            dataName = "data|%d" % i
            i += 1
            contentStruct['root'][dataName] = state
        return headersStruct, contentStruct

# Register the service into the resource
resourceStatus.addService(TDSServiceStatusRequestAll)

# ==============================================================================
# Declaration of the service "send".
# ==============================================================================
class TDSServiceStatusSend(TDSService):
    """Send a free status.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'name' : 'string',
            'value' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "send"
        self.comment = "Send a free status."

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
        resourceStatus.sendStatus(parameters['name'], parameters['value'])
        return headersStruct, contentStruct

# Register the service into the resource
resourceStatus.addService(TDSServiceStatusSend)

# ==============================================================================
# Declaration of the service "register_event".
# ==============================================================================
class TDSServiceStatusRegisterEvent(TDSService):
    """Add an event in the registered events list of the client.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'event_name' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_FREE
        self.exclusiveExecution = False
        self.name = "register_event"
        self.comment = "Add an event in the registered events list of the client."

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
        resourceStatus.removeExcludedEvent(id, parameters['event_name'])
        return headersStruct, contentStruct

# Register the service into the resource
resourceStatus.addService(TDSServiceStatusRegisterEvent)

# ==============================================================================
# Declaration of the service "unregister_event".
# ==============================================================================
class TDSServiceStatusUnregisterEvent(TDSService):
    """Remove an event from the registered events list of the client.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'event_name' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_FREE
        self.exclusiveExecution = False
        self.name = "unregister_event"
        self.comment = "Remove an event from the registered events list of the client."

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
        resourceStatus.addExcludedEvent(id, parameters['event_name'])
        return headersStruct, contentStruct

# Register the service into the resource
resourceStatus.addService(TDSServiceStatusUnregisterEvent)
