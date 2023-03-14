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
# Declaration of the resource "menu".
# ==============================================================================
class TDSResourceMenu(TDSResource):
    """Resource menu class.
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
        self.name = "menu"
        self.comment = "Menu resource."
        self.fileName = RESOURCE_FILENAME

# Create an instance of the resource
resourceMenu = TDSResourceMenu("resourceMenu")
# Register the resource into the resources manager
resourcesManager.addResource(resourceMenu)

# ==============================================================================
# ******************************************************************************
# SERVICES DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the service "index".
# ==============================================================================
class TDSServiceMenuIndex(TDSService):
    """Main menu of the server.
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
        self.name = "index"
        self.comment = "Main menu of the server."
        self.haveXsl = True
        self.xslPath = "/data/web_interface/server_menu/xsl/menu.xsl"

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
        contentStruct = {'root' : self.__createXmlIndex()}
        return headersStruct, contentStruct

    # --------------------------------------------------------------------------
    # Create xml data dict for the menu index.
    # --------------------------------------------------------------------------
    def __createXmlIndex(self):
        """Create xml data dict for the menu index.
        @return: The xml content as dictionary.
        """
        contentStruct = {
            'title' : 'Tux Droid Server V %s' % serverVersion,
            'section' : 'Index',
            'items' : {
                'Resources' : '/menu/resources?resource_name=index',
                'Logs' : '/menu/logs?log_name=index',
                'Clients' : '/menu/clients?',
            }
        }
        return contentStruct

# Register the service into the resource
resourceMenu.addService(TDSServiceMenuIndex)
# Bind the debug index url to this service
resourcesManager.addBinding("debug", "menu", "index")

# ==============================================================================
# Declaration of the service "resources".
# ==============================================================================
class TDSServiceMenuResources(TDSService):
    """Resources menu.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'resource_name' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "resources"
        self.comment = "Resources menu."
        self.haveXsl = True
        self.xslPath = "/data/web_interface/server_menu/xsl/menu.xsl"

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
        if parameters['resource_name'] == 'index':
            contentStruct = {'root' : self.__createXmlIndex()}
        else:
            contentStruct = {
                'root' : self.__createXmlResource(parameters['resource_name'])
            }
        return headersStruct, contentStruct

    # --------------------------------------------------------------------------
    # Create xml data dict for the resources index.
    # --------------------------------------------------------------------------
    def __createXmlIndex(self):
        """Create xml data dict for the resources index.
        @return: The xml content as dictionary.
        """
        self.xslPath = "/data/web_interface/server_menu/xsl/menu_resources.xsl"
        contentStruct = {
            'title' : 'Tux Droid Server V %s' % serverVersion,
            'section' : 'Resources',
            'items' : {}
        }
        resourcesList = resourcesManager.getResourcesList()
        resourcePathsList = resourcesManager.getResourcePathsList()
        for path in resourcePathsList:
            path = os.path.basename(path)
            contentStruct['items']["Layer_%s" % path] = {}
            for resourceName in resourcesList:
                resource = resourcesManager.getResource(resourceName)
                resourcePath = os.path.basename(os.path.split(
                    resource.fileName)[-2])
                if resourcePath == path:
                    url = '?resource_name=%s' % resourceName
                    contentStruct['items']["Layer_%s" % path][resourceName] = url
        return contentStruct

    # --------------------------------------------------------------------------
    # Create xml data dict for a resource.
    # --------------------------------------------------------------------------
    def __createXmlResource(self, resourceName):
        """Create xml data dict for a resource.
        @resourceName: Name of the resource.
        @return: The xml content as dictionary.
        """
        self.xslPath = "/data/web_interface/server_menu/xsl/resource.xsl"
        resource = resourcesManager.getResource(resourceName)
        if resource == None:
            result = {}
        else:
            result = resource.getXmlStructure()
        result['title'] = 'Tux Droid Server V %s' % serverVersion
        result['section'] = 'Resource : %s' % resourceName
        # complete the url
        for service in result['services'].keys():
            address = TDS_CONF_HOST_ADDRESS
            if address == "":
                address = '127.0.0.1'
            cmdProt = 'http://%s:%d/<id_client>/%s/%s?%s' % (address,
                TDS_HTTP_PORT, resourceName, service,
                result['services'][service]['parameters'])
            result['services'][service]['commandPrototype'] = cmdProt
        return result

# Register the service into the resource
resourceMenu.addService(TDSServiceMenuResources)

# ==============================================================================
# Declaration of the service "logs".
# ==============================================================================
class TDSServiceMenuLogs(TDSService):
    """Logs menu.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'log_name' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "logs"
        self.comment = "Logs menu."
        self.haveXsl = True
        self.xslPath = "/data/web_interface/server_menu/xsl/menu.xsl"
        if os.name == 'nt':
            self.__logPath = os.path.join(os.environ['ALLUSERSPROFILE'],
                "Kysoh", "Tux Droid", "logs")
        else:
            from util.misc.systemPaths import systemPaths
            path = systemPaths.getLogPath()
            self.__logPath = path

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
        if parameters['log_name'] == 'index':
            contentStruct = {'root' : self.__createXmlIndex()}
        else:
            contentStruct = {
                'root' : self.__createXmlLog(parameters['log_name'])
            }
        return headersStruct, contentStruct

    # --------------------------------------------------------------------------
    # Create xml data dict for the logs index.
    # --------------------------------------------------------------------------
    def __createXmlIndex(self):
        """Create xml data dict for the logs index.
        @return: The xml content as dictionary.
        """
        self.xslPath = "/data/web_interface/server_menu/xsl/menu.xsl"
        contentStruct = {
            'title' : 'Tux Droid Server V %s' % serverVersion,
            'section' : 'Logs',
            'items' : {
                'Global_Server' : 'logs?log_name=%s' % TDS_FILENAME_TUXDROIDSERVER_LOG,
                'HTTP.REST_Server' : 'logs?log_name=%s' % TDS_FILENAME_HTTPSERVER_LOG,
                'Resources_manager' : 'logs?log_name=%s' % TDS_FILENAME_RESOURCES_LOG,
                'Clients_manager_TCP.IP_Server' : 'logs?log_name=%s' % TDS_FILENAME_CLIENTS_LOG,
                'Tux_driver' : 'logs?log_name=libtuxdriver_wrapper',
                'Tux_OSL' : 'logs?log_name=libtuxosl_wrapper',
                'Plugins_server' : 'logs?log_name=plugins_server',
                'Gadgets_server' : 'logs?log_name=gadgets_server',
                'UGC_server' : 'logs?log_name=ugc_server',
                'Attitune_manager' : 'logs?log_name=attitune_manager',
                'Scheduler' : 'logs?log_name=scs_scheduler',
            }
        }
        return contentStruct

    # --------------------------------------------------------------------------
    # Create xml data dict for a log.
    # --------------------------------------------------------------------------
    def __createXmlLog(self, logName):
        """Create xml data dict for a log.
        @param logName: Name of the log.
        @return: The xml content as dictionary.
        """
        self.xslPath = "/data/web_interface/server_menu/xsl/log.xsl"
        filePath = os.path.join(self.__logPath, "%s.log" % logName)
        if not os.path.isfile(filePath):
            return {}
        logText = open(filePath, 'r').read()
        logDict = {}
        for i, log in enumerate(logText.split('\n')):
            if log != '':
                logDict['log_%.5d' % i] = log
        contentStruct = {
            'data' : {
                'log_file_path' : filePath,
                'log_text' : logDict,
            }
        }
        return contentStruct

# Register the service into the resource
resourceMenu.addService(TDSServiceMenuLogs)

# ==============================================================================
# Declaration of the service "clients".
# ==============================================================================
class TDSServiceMenuClients(TDSService):
    """Clients index.
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
        self.name = "clients"
        self.comment = "Clients index."
        self.haveXsl = True
        self.xslPath = "/data/web_interface/server_menu/xsl/clients.xsl"

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
        contentStruct = {'root' : self.__createXmlIndex()}
        return headersStruct, contentStruct

    # --------------------------------------------------------------------------
    # Create xml data dict for the clients index.
    # --------------------------------------------------------------------------
    def __createXmlIndex(self):
        """Create xml data dict for the clients index.
        @return: The xml content as dictionary.
        """
        clientsInfo = clientsManager.getClientsInfo()
        clients = {}
        for i, clientInfo in enumerate(clientsInfo):
            clientInfo['name'] = clientInfo['name'].replace(' ', '')
            clientInfo['name'] = "client%.2d_%s" % (i, clientInfo['name'])
            clients[clientInfo['name']] = clientInfo
        contentStruct = {
            'title' : 'Tux Droid Server V %s' % serverVersion,
            'section' : 'Clients',
            'clients' : clients,
        }
        return contentStruct

# Register the service into the resource
resourceMenu.addService(TDSServiceMenuClients)
