# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import threading
import time

from ApiBaseChild import ApiBaseChild
from lib.TcpIpClient import TcpIpClient
from lib.HttpRequester import HttpRequester
from const.ConstApi import ST_NAME_API_CONNECT
from const.ConstClient import CLIENT_LEVELS
from const.ConstClient import CLIENT_LEVEL_FREE
from const.ConstClient import CLIENT_LEVEL_ANONYME
from const.ConstServer import SW_NAME_EXTERNAL_STATUS

# ------------------------------------------------------------------------------
# Class to make a connection to the HTTP/TCPIP server.
# ------------------------------------------------------------------------------
class ApiBaseServer(ApiBaseChild):
    """Class to make a connection to the HTTP/TCPIP server.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, apiBase, host = '127.0.0.1', port = 270):
        """Constructor of the class.
        @param apiBase: ApiBase parent object.
        @param host: host of the server.
        @param port: port of the server.
        """
        ApiBaseChild.__init__(self, apiBase)
        # Server field
        self.__host = host
        self.__port = port
        self.__cmdUrlMutex = threading.Lock()
        # Client field
        self.__clientName = "MyName"
        self.__clientPasswd = None
        self.__clientId = "0"
        self.__cmdUrl = "0/"
        self.__clientLevel = CLIENT_LEVEL_FREE
        # Sender field
        self.__sender = HttpRequester(self.__host, self.__port)
        # Connection field
        self.__conn = None
        # Syndicated events list
        self.__syndicatedEventsList = []

    # --------------------------------------------------------------------------
    # destructor of the class.
    # --------------------------------------------------------------------------
    def destroy(self):
        """destructor of the class.
        """
        self.disconnect()

    # --------------------------------------------------------------------------
    # Get the server address.
    # --------------------------------------------------------------------------
    def getAddress(self):
        """Get the server address.
        @return: A string. "http://<host>:<port>/"
        """
        return "http://%s:%d" % (self.__host, self.__port)

    # --------------------------------------------------------------------------
    # Get the client level of the API instance.
    # --------------------------------------------------------------------------
    def getClientLevel(self):
        """Get the client level of the API instance.
        @return: the client level
        """
        return self.__clientLevel

    # --------------------------------------------------------------------------
    # Return the state of connection to the server.
    # --------------------------------------------------------------------------
    def getConnected(self):
        """Return the state of connection to the server.
        """
        if self.__conn == None:
            return False
        else:
            return self.__conn.getConnected()

    # --------------------------------------------------------------------------
    # Wait until the client was connected to the server.
    # --------------------------------------------------------------------------
    def waitConnected(self, timeout = 99999999999.):
        """Wait until the client was connected to the server.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if self.__conn == None:
            return False
        else:
            return self.__conn.waitConnected(timeout)

    # --------------------------------------------------------------------------
    # Wait until the client was disconnected from the server.
    # --------------------------------------------------------------------------
    def waitDisconnected(self, timeout = 99999999999.):
        """Wait until the client was disconnected from the server.
        @param timeout: maximal delay to wait.
        @return: the state of the wait result.
        """
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if self.__conn == None:
            return False
        else:
            return self.__conn.waitDisconnected(timeout)

    # --------------------------------------------------------------------------
    # Register a callback on the connected event.
    # --------------------------------------------------------------------------
    def registerEventOnConnected(self, funct, idx = None):
        """Register a callback on the connected event.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        nIdx = self._registerEvent(ST_NAME_API_CONNECT, "True", funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the connected event.
    # --------------------------------------------------------------------------
    def unregisterEventOnConnected(self, idx):
        """Unregister a callback from the connected event.
        @param idx: index from a previous register.
        """
        self._unregisterEvent(ST_NAME_API_CONNECT, idx)

    # --------------------------------------------------------------------------
    # Register a callback on the disconnected event.
    # --------------------------------------------------------------------------
    def registerEventOnDisconnected(self, funct, idx = None):
        """Register a callback on the disconnected event.
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        nIdx = self._registerEvent(ST_NAME_API_CONNECT, "False", funct, idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from the disconnected event.
    # --------------------------------------------------------------------------
    def unregisterEventOnDisconnected(self, idx):
        """Unregister a callback from the disconnected event.
        @param idx: index from a previous register.
        """
        self._unregisterEvent(ST_NAME_API_CONNECT, idx)

    # --------------------------------------------------------------------------
    # Send a request to the server.
    # --------------------------------------------------------------------------
    def request(self, cmd, varStruct = {}, varResult = {}, forceExec = False,
        complexeXml = False):
        """Send a request to the server.
        @param cmd: formated command in an url.
        @param varStruct: structure definition of the requested values.
        @param varResult: returned values in a structure.
        @param forceExec: force the sending of the command when the client is not yet
                         connected.
        @return: the success of the request.
        """
        if not forceExec:
            if not self.getConnected():
                return False

        def getValueFromStructure(struct, valuePath):
            pathList = valuePath.split(".")
            node = struct
            result = None
            for i, p in enumerate(pathList):
                # Current node in path is valid
                if node.has_key(p):
                    # Path : leaf
                    if i == len(pathList) - 1:
                        # Return the value of the matched path
                        result = node[p]
                        return result
                    # Path : node
                    else:
                        node = node[p]
                # Invalid path
                else:
                    return result
            return result

        # Completing the command
        cmd = "%s%s" % (self.__cmdUrl, cmd)
        # Send the request and get the xml structure
        xmlStruct = self.__sender.request(cmd, "GET", complexeXml)
        # Check server run and the command success
        if xmlStruct['result'] != "Success":
            return False
        # Get values from paths
        if len(varStruct.keys()) > 0:
            for valueName in varStruct.keys():
                valuePath = varStruct[valueName]
                value = getValueFromStructure(xmlStruct, valuePath)
                varResult[valueName] = value
        else:
            for key in xmlStruct.keys():
                varResult[key] = xmlStruct[key]
        return True

    # --------------------------------------------------------------------------
    # Get the HTTP server version.
    # --------------------------------------------------------------------------
    def getVersion(self):
        """Get the HTTP server version.
        @return: the version of the HTTP server.
        """
        varStruct = {
            "version" : "data0.version",
        }
        varResult = {}
        if self.request("server/version?", varStruct, varResult):
            return varResult["version"]
        else:
            return ""

    # --------------------------------------------------------------------------
    # Attempt to connect to the server.
    # --------------------------------------------------------------------------
    def connect(self, level, name, passwd = ""):
        """Attempt to connect to the server.
        @param level: requested level of the client.
        @param name: name of the client.
        @param passwd: password of the client.
        @return: the success of the connection.
        """
        # If already connected - Success
        if self.getConnected():
            return True
        # If client level is invalid - Failed
        if level not in CLIENT_LEVELS:
            return False
        self.__clientLevel = level
        # If client level is ANONYME - Failed
        if level == CLIENT_LEVEL_ANONYME:
            return False
        # Check name type
        if not self._checkObjectType('name', name, 'str'):
            return False
        # Create the connection
        self.__clientName = name
        self.__clientPasswd = passwd
        if self.__conn == None:
            self.__conn = TcpIpClient(self.__clientName, self.__clientLevel,
                0.0)
            self.__conn.registerOnNotificationCallBack(self.__onClientMessage)
            self.__conn.registerOnConnectedCallBack(self.__onClientConnected)
            self.__conn.registerOnDisconnectedCallBack(self.__onClientDisconnected)
        self.__conn.connect(self.__host, self.__port + 1)
        return self.__conn.waitConnected(2.0)

    # --------------------------------------------------------------------------
    # Disconnect the client from the server.
    # --------------------------------------------------------------------------
    def disconnect(self):
        """Disconnect the client from the server.
        """
        # If already disconnected - Success
        if not self.getConnected():
            return True
        if self.__conn != None:
            self.__conn.disconnect()
        return True

    # --------------------------------------------------------------------------
    # Change the target server address.
    # --------------------------------------------------------------------------
    def changeServer(self, host, port = 270):
        """Change the target server address.
        @host: Host address of the target server.
        @port: Port of the target server.
        """
        autoConn = False
        if self.__conn != None:
            if self.__conn.getAutoConnected():
                autoConn = True
            self.__conn.disconnect()
        time.sleep(1.0)
        self.__host = host
        self.__port = port
        self.__sender.setServerAddress(self.__host, self.__port)
        if autoConn:
            self.autoConnect(self.__clientLevel, self.__clientName)

    # --------------------------------------------------------------------------
    # Start the automatic connection/reconnection loop with the server.
    # --------------------------------------------------------------------------
    def autoConnect(self, level, name, passwd = ""):
        """Start the automatic connection/reconnection loop with the server.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param level: requested level of the client.
        @param name: name of the client.
        @param passwd: password of the client.
        """
        # Check name type
        if not self._checkObjectType('name', name, 'str'):
            return False
        self.__clientName = name
        self.__clientPasswd = passwd
        self.__clientLevel = level
        if self.__conn != None:
            if self.__conn.getAutoConnected():
                return
        else:
            self.__conn = TcpIpClient(self.__clientName, self.__clientLevel,
                0.0)
            self.__conn.registerOnNotificationCallBack(self.__onClientMessage)
            self.__conn.registerOnConnectedCallBack(self.__onClientConnected)
            self.__conn.registerOnDisconnectedCallBack(self.__onClientDisconnected)
        self.__conn.autoConnect(self.__host, self.__port + 1)

    # --------------------------------------------------------------------------
    # Event on client connected.
    # --------------------------------------------------------------------------
    def __onClientConnected(self, identifier):
        self.__clientId = identifier
        self.__cmdUrl = "%s/" % self.__clientId
        self.getEventsHandler().getEventHandler(ST_NAME_API_CONNECT).emit("True",
            0.0)
        # Get all the status from the server and update the events handler
        struct = self.__sender.request('%sstatus/request_all?' % self.__cmdUrl)
        statusesCount = struct['data_count']
        for index in range(statusesCount):
            if struct['data%d' % index]['value'] != " ":
                eventHandler = self.getEventsHandler().getEventHandler(struct['data%d' % index]['name'])
                if eventHandler != None:
                    eventHandler.emit(struct['data%d' % index]['value'], 0.0)
        self.updateSyndicatedEvents()
        print "API is connected to [%s:%s]" % (self.__host, self.__port)

    # --------------------------------------------------------------------------
    # Event on client disconnected.
    # --------------------------------------------------------------------------
    def __onClientDisconnected(self):
        self.__clientId = "0"
        self.__cmdUrl = "%s/" % self.__clientId
        self.getEventsHandler().getEventHandler(ST_NAME_API_CONNECT).emit("False",
            0.0)
        print "API is disconnected from [%s:%s]" % (self.__host, self.__port)

    # --------------------------------------------------------------------------
    # Event on client message.
    # --------------------------------------------------------------------------
    def __onClientMessage(self, message):
        eventStruct = message.split('|')
        stName = eventStruct[0]
        stValue = eventStruct[1]
        stDelay = float(eventStruct[3])
        # If the status is external, parse-it
        if stName == SW_NAME_EXTERNAL_STATUS:
            pList = stValue.split("|")
            if len(pList) > 0:
                self.getEventsHandler().getEventHandler("all").emit(*pList)
        else:
            self.getEventsHandler().emit(stName, (stValue, stDelay))

    # --------------------------------------------------------------------------
    # Update the syndicated events to the server.
    # --------------------------------------------------------------------------
    def updateSyndicatedEvents(self):
        """Update the syndicated events to the server.
        """
        for eventName in self.__syndicatedEventsList:
            cmd = "status/register_event?event_name=%s" % eventName
            self.request(cmd, {}, {})

    # --------------------------------------------------------------------------
    # Syndicate this api to an event.
    # --------------------------------------------------------------------------
    def syndicate(self, eventName):
        """Syndicate this api to an event.
        @param eventName: Event/status name.
        """
        if eventName not in self.__syndicatedEventsList:
            cmd = "status/register_event?event_name=%s" % eventName
            self.request(cmd, {}, {})
            self.__syndicatedEventsList.append(eventName)

    # --------------------------------------------------------------------------
    # Un-syndicate this api from an event.
    # --------------------------------------------------------------------------
    def unSyndicate(self, eventName):
        """Un-syndicate this api from an event.
        @param eventName: Event/status name.
        """
        if eventName in self.__syndicatedEventsList:
            cmd = "status/unregister_event?event_name=%s" % eventName
            self.request(cmd, {}, {})
            self.__syndicatedEventsList.remove(eventName)
