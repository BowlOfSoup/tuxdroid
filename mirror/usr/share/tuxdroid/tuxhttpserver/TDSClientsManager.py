# -*- coding: utf-8 -*-

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

import socket
import threading
import time
import random

try:
    from hashlib import md5
except:
    from md5 import md5

from util.logger import *

from TDSClient import TDSClient
from TDSConfiguration import *
from TDSClientLevels import *

# Formated PING command
_PING_CMD = "PING\n" + "".join(" " * 123)
# Formated ALLOWED command
_ALLOWED_CMD = "ALLOWED\n" + "".join(" " * 120)
# Formated DISALLOWED command
_DISALLOWED_CMD = "DISALLOWED\n" + "".join(" " * 117)

# ------------------------------------------------------------------------------
# Tux Droid Server : Client manager.
# ------------------------------------------------------------------------------
class TDSClientsManager(object):
    """Tux Droid Server : Client manager.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, accessManager, host = TDS_CONF_HOST_ADDRESS,
        port = TDS_RAW_DATA_PORT):
        """Constructor.
        @accessManager: Access Manager object.
        @param host: Host IP to listen.
                     Example : '127.0.0.1' for local loop only.
                     Example : '192.168.0.1' for local network only.
                     Example : '' for internet access.
        @param port: TCP port to listen.
        """
        self.__cliLst = []
        self.__cliMutex = threading.Lock()
        self.__socket = None
        self.__host = host
        self.__port = port
        self.__runLst = False
        self.__runLstThread = None
        self.__runLstMutex = threading.Lock()
        self.__runPing = False
        self.__runPingThread = None
        self.__runPingMutex = threading.Lock()
        self.__onClientAdded = None
        self.__onClientRemoved = None
        self.__defaultExcludedEventsList = []
        self.__restrictedEventsList = []
        self.__accessManager = accessManager
        self.__logger = SimpleLogger(TDS_FILENAME_CLIENTS_LOG)
        self.__logger.setTarget(TDS_CONF_LOG_TARGET)
        self.__logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.__logger.resetLog()
        self.__logger.logInfo("-----------------------------------------------")
        self.__logger.logInfo("TDSClientsManager%s" % __version__)
        self.__logger.logInfo("Author : %s" % __author__)
        self.__logger.logInfo("Licence : %s" % __licence__)
        self.__logger.logInfo("-----------------------------------------------")

    # --------------------------------------------------------------------------
    # Register a callback function to the "On client added" event.
    # --------------------------------------------------------------------------
    def registerOnClientAddedCallBack(self, funct):
        """Register a callback function to the "On client added" event.
        @param funct: Function pointer. The function must accept one parameter.
                      Example :
                      def onClientAdded(idClient):
                          print idClient
        """
        self.__onClientAdded = funct

    # --------------------------------------------------------------------------
    # Register a callback function to the "On client removed" event.
    # --------------------------------------------------------------------------
    def registerOnClientRemovedCallBack(self, funct):
        """Register a callback function to the "On client removed" event.
        @param funct: Function pointer. The function must accept one parameter.
                      Example :
                      def onClientRemoved(idClient):
                          print idClient
        """
        self.__onClientRemoved = funct

    # --------------------------------------------------------------------------
    # Add an event in the default excluded list.
    # --------------------------------------------------------------------------
    def addDefaultExcludedEvent(self, eventName):
        """Add an event in the default excluded list.
        @param eventName: Event name.
        """
        self.__defaultExcludedEventsList.append(eventName)

    # --------------------------------------------------------------------------
    # Remove an event from the default excluded list.
    # --------------------------------------------------------------------------
    def removeDefaultExludedEvent(self, eventName):
        """Remove an event from the default excluded list.
        @param eventName: Event name.
        """
        try:
            self.__defaultExcludedEventsList.remove(eventName)
        except:
            pass

    # --------------------------------------------------------------------------
    # Add event in the restricted events list.
    # --------------------------------------------------------------------------
    def addRestrictedEvent(self, eventName):
        """Add event in the restricted events list.
        Only for the RESTRICTED clients. The client need to have the access
        priority to receive these events. (Typically head, left, right buttons)
        @param eventName: Event name.
        """
        self.__restrictedEventsList.append(eventName)

    # --------------------------------------------------------------------------
    # Check if a client exists.
    # --------------------------------------------------------------------------
    def clientExists(self, id):
        """Check if a client exists.
        @param id: Id client.
        @return: True or False.
        """
        self.__cliMutex.acquire()
        result = False
        for cli in self.__cliLst:
            if cli['id'] == id:
                result = True
                break
        self.__cliMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the level of a client.
    # --------------------------------------------------------------------------
    def getClientLevel(self, id):
        """Get the level of a client.
        @param id: Id client.
        @return: The client level or None.
        """
        self.__cliMutex.acquire()
        result = None
        for cli in self.__cliLst:
            if cli['id'] == id:
                result = cli['level']
                break
        self.__cliMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the name of a client.
    # --------------------------------------------------------------------------
    def getClientName(self, id):
        """Get the name of a client.
        @param id: Id client.
        @return: The client name or None.
        """
        self.__cliMutex.acquire()
        result = None
        for cli in self.__cliLst:
            if cli['id'] == id:
                result = cli['name']
                break
        self.__cliMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get a client object.
    # --------------------------------------------------------------------------
    def getClient(self, id):
        """Get a client object.
        @param id: Id client.
        @return: The client object or None.
        """
        self.__cliMutex.acquire()
        result = None
        for cli in self.__cliLst:
            if cli['id'] == id:
                result = cli['object']
                break
        self.__cliMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the informations about the clients.
    # --------------------------------------------------------------------------
    def getClientsInfo(self):
        """Get the informations about the clients.
        @return: The informations about the clients.
        """
        self.__cliMutex.acquire()
        infoStruct = []
        for cli in self.__cliLst:
            infoStruct.append({
                'name' : cli['name'],
                'level' : getClientLevelName(cli['level']),
                'type' : cli['type'],
            })
        self.__cliMutex.release()
        return infoStruct

    # --------------------------------------------------------------------------
    # Start the server.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the server.
        @return: The success of the server start. True or False.
        """
        # Exit the function if the server is already started
        if self.__getRunLst():
            return True
        # Create the server socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            # Bind the socket
            self.__socket.bind((self.__host, self.__port))
            # Set the socket to listen mode
            self.__socket.listen(50)
            #Run the listen loop and the ping loop
            self.__runLstThread = threading.Thread(target = self.__listenLoop)
            self.__runLstThread.start()
            self.__runPingThread = threading.Thread(target = self.__pingLoop)
            self.__runPingThread.start()
            time.sleep(0.1)
            # Server successfuly started
            self.__logger.logInfo("Server successfully started (%s:%d)" % (
                self.__host, self.__port))
            return True
        except socket.timeout:
            self.__setRunLst(False)
            # Failed to start the server
            self.__logger.logError("Failed to start the server (%s:%d) : %s" % (
                self.__host, self.__port, "Socket.timeout"))
            return False
        except socket.error:
            self.__setRunLst(False)
            # Failed to start the server
            self.__logger.logError("Failed to start the server (%s:%d) : %s" % (
                self.__host, self.__port, "Socket.error"))
            return False
        except:
            self.__setRunLst(False)
            # Failed to start the server
            self.__logger.logError("Failed to start the server (%s:%d) : %s" % (
                self.__host, self.__port, "Unexpected error"))
            return False

    # --------------------------------------------------------------------------
    # Stop the server.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the server.
        """
        # If the server don't runs then exit the function
        if not self.__getRunLst():
            return
        # Stop the listen loop
        self.__setRunLst(False)
        # Stop the ping loop
        self.__setRunPing(False)
        # Close all clients
        self.__clearClients()
        # Close the server socket
        self.__socket.close()
        time.sleep(0.1)
        # Ensure that the threads have been stopped
        if self.__runLstThread.isAlive():
            self.__runLstThread._Thread__stop()
        if self.__runPingThread.isAlive():
            self.__runPingThread.join()
        self.__logger.logInfo("Server successfully stopped")

    # --------------------------------------------------------------------------
    # Wait that the server has stopped.
    # --------------------------------------------------------------------------
    def waitStop(self):
        """Wait that the server has stopped.
        """
        while self.__getRunLst():
            time.sleep(0.5)
        time.sleep(0.5)

    # --------------------------------------------------------------------------
    # Get the log file path.
    # --------------------------------------------------------------------------
    def getLogFilePath(self):
        """Get the log file path.
        @return: The log file path.
        """
        return self.__logger.getLogFilePath()

    # --------------------------------------------------------------------------
    # Get the state of the listening loop.
    # --------------------------------------------------------------------------
    def __getRunLst(self):
        """Get the state of the listening loop.
        @return: True or False.
        """
        self.__runLstMutex.acquire()
        result = self.__runLst
        self.__runLstMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the state of the listening loop.
    # --------------------------------------------------------------------------
    def __setRunLst(self, value = True):
        """Set the state of the listening loop.
        @param value: New value (True or False)
        """
        self.__runLstMutex.acquire()
        self.__runLst = value
        self.__runLstMutex.release()

    # --------------------------------------------------------------------------
    # Get the state of the ping loop.
    # --------------------------------------------------------------------------
    def __getRunPing(self):
        """Get the state of the ping loop.
        @return: True or False.
        """
        self.__runPingMutex.acquire()
        result = self.__runPing
        self.__runPingMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the state of the ping loop.
    # --------------------------------------------------------------------------
    def __setRunPing(self, value = True):
        """Set the state of the ping loop.
        @param value: New value (True or False)
        """
        self.__runPingMutex.acquire()
        self.__runPing = value
        self.__runPingMutex.release()

    # --------------------------------------------------------------------------
    # Check if a ROOT client is already connected.
    # --------------------------------------------------------------------------
    def __rootClientExists(self):
        """Check if a ROOT client is already connected.
        @return: True or False.
        """
        self.__cliMutex.acquire()
        result = False
        for cli in self.__cliLst:
            if cli['level'] == TDS_CLIENT_LEVEL_ROOT:
                result = True
                break
        self.__cliMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Generate a single id.
    # --------------------------------------------------------------------------
    def generateSingleId(self, baseString = None):
        """Generate a single id.
        @baseString: Base string. (default None)
        @return: The single id.
        """
        if baseString == None:
            baseString = str(time.time() + random.random())
        md5H = md5()
        md5H.update(baseString)
        id = md5H.hexdigest()
        return id

    # --------------------------------------------------------------------------
    # Add a REST client.
    # --------------------------------------------------------------------------
    def addRESTClient(self, clientName, clientLevel):
        """Add a REST client.
        @clientName: Client name.
        @clientLevel: Client level.
        @return: The id client or None.
        """
        # Can't add client when the server is not really started
        # (While the server is closing, client could attempt to connect)
        if not self.__getRunLst():
            return
        # Check clientLevel (only one root client)
        if clientLevel == TDS_CLIENT_LEVEL_ROOT:
            if self.__rootClientExists():
                return None
        self.__cliMutex.acquire()
        # Create a md5 hash of the socket address in order to make an unique
        # identifier for the client.
        id = self.generateSingleId()
        # Create a dictionary for the client configuration
        cliConf = {
            'connection' : None,
            'address' : None,
            'id' : id,
            'object' : None,
            'level' : clientLevel,
            'name' : clientName,
            'type' : 'HTTP/REST',
        }
        # Create a client object
        cliConf['object'] = TDSClient(self.__accessManager, self, id,
            clientLevel, None)
        # Insert the default excluded events in the client
        for eventName in self.__defaultExcludedEventsList:
            cliConf['object'].addExcludedEvent(eventName)
        # Set the restricted events list in the client
        cliConf['object'].setRestrictedEventsList(self.__restrictedEventsList)
        # Add the client to the list
        self.__cliLst.append(cliConf)
        self.__cliMutex.release()
        # Call the "On client added" event
        if self.__onClientAdded != None:
            self.__onClientAdded(id)
        self.__logger.logInfo("New REST client added (%s)" % id)
        return id

    # --------------------------------------------------------------------------
    # Add a new client in the clients list.
    # --------------------------------------------------------------------------
    def __addClient(self, connection, address):
        """Add a new client in the clients list.
        @param connection: Client socket.
        @param address: Client address.
        """
        # Can't add client when the server is not really started
        # (While the server is closing, client could attempt to connect)
        if not self.__getRunLst():
            return
        # Create a md5 hash of the socket address in order to make an unique
        # identifier for the client.
        id = self.generateSingleId(str(address[0]) + str(address[1]))
        self.__cliMutex.acquire()
        # Create a dictionary for the client configuration
        cliConf = {
            'connection' : connection,
            'address' : address,
            'id' : id,
            'object' : None,
            'level' : -1,
            'name' : "None",
            'type' : 'TCP/IP'
        }
        # Create a 128 bytes length string with the id client.
        idToSend = id + "\n" + "".join(" " * (127 - len(id)))
        try:
            # Send the identifer to the client
            connection.send(idToSend)
            # Read the client name and level
            data = connection.recv(128).split('\n')
            clientName = data[0]
            clientLevel = int(data[1])
            # Check clientLevel (only one root client)
            if clientLevel == TDS_CLIENT_LEVEL_ROOT:
                self.__cliMutex.release()
                if self.__rootClientExists():
                    # Notify the client that it is not allowed
                    connection.send(_DISALLOWED_CMD)
                    return
                self.__cliMutex.acquire()
            clientDelay = 0.1
            if len(data) >= 3:
                try:
                    clientDelay = float(data[2])
                except:
                    pass
            # Create a client object
            cliConf['object'] = TDSClient(self.__accessManager, self, id,
                clientLevel, clientDelay)
            cliConf['level'] = clientLevel
            cliConf['name'] = clientName
            # Insert the default excluded events in the client
            for eventName in self.__defaultExcludedEventsList:
                cliConf['object'].addExcludedEvent(eventName)
            # Set the restricted events list in the client
            cliConf['object'].setRestrictedEventsList(self.__restrictedEventsList)
        except:
            self.__cliMutex.release()
            return
        # Notify the client that it is allowed
        connection.send(_ALLOWED_CMD)
        # Add the client to the list
        self.__cliLst.append(cliConf)
        self.__cliMutex.release()
        # Call the "On client added" event
        if self.__onClientAdded != None:
            self.__onClientAdded(id)
        self.__logger.logInfo("New TCP/IP client added (%s)" % id)

    # --------------------------------------------------------------------------
    # Remove a REST client from the clients list.
    # --------------------------------------------------------------------------
    def removeRESTClient(self, clientId):
        """Remove a REST client from the clients list.
        @param clientId: Id of the REST client.
        """
        self.__cliMutex.acquire()
        client = None
        for cli in self.__cliLst:
            if cli['id'] == clientId:
                if cli['address'] == None:
                    client = cli
                    break
        self.__cliMutex.release()
        if client != None:
            self.__removeClient(client)

    # --------------------------------------------------------------------------
    # Remove a client from the clients list.
    # --------------------------------------------------------------------------
    def __removeClient(self, client):
        """Remove a client from the clients list.
        @param client: Client structure.
        """
        self.__cliMutex.acquire()
        removedId = None
        # Search the client address in the registered clients
        for cli in self.__cliLst:
            if cli == client:
                if cli['address'] != None:
                    cli['connection'].close()
                self.__cliLst.remove(cli)
                removedId = cli['id']
                cli['object'].destroy()
                break
        self.__cliMutex.release()
        # If the client has been removed then call the "On client removed" event
        if removedId != None:
            if self.__onClientRemoved != None:
                self.__onClientRemoved(removedId)
        self.__logger.logInfo("Client removed (%s)" % removedId)

    # --------------------------------------------------------------------------
    # Clear the clients list.
    # --------------------------------------------------------------------------
    def __clearClients(self):
        """Clear the clients list.
        """
        self.__cliMutex.acquire()
        removedId = None
        # Search the client address in the registered clients
        for cli in self.__cliLst:
            if cli['address'] != None:
                cli['connection'].close()
            cli['object'].destroy()
        self.__cliLst = []
        self.__cliMutex.release()

    # --------------------------------------------------------------------------
    # Socket listening loop.
    # --------------------------------------------------------------------------
    def __listenLoop(self):
        """Socket listening loop.
        """
        self.__setRunLst(True)
        while self.__getRunLst():
            try:
                connection, address = self.__socket.accept()
                # If the client socket is valid then add it to the clients list
                if (connection != None) and (address != None):
                    self.__addClient(connection, address)
            except:
                pass

    # --------------------------------------------------------------------------
    # Ping loop.
    # --------------------------------------------------------------------------
    def __pingLoop(self):
        """Ping loop.
        """
        self.__setRunPing(True)
        while self.__getRunPing():
            aClientHasRemoved = False
            self.__cliMutex.acquire()
            # Ping all clients
            for cli in self.__cliLst:
                if cli['address'] == None:
                    # Check REST client activity
                    delay = cli['object'].getLastTansactionDelay()
                    if delay >= 8.0:
                        self.__cliMutex.release()
                        # The REST client seems to be disconnected
                        self.__logger.logInfo("REST client not responding (%s)" % \
                            cli['id'])
                        self.__removeClient(cli)
                        aClientHasRemoved = True
                        self.__cliMutex.acquire()
                        break
                    continue
                try:
                    # Send the PING command
                    cli['connection'].send(_PING_CMD)
                    # Read the client response
                    data = cli['connection'].recv(128)
                except:
                    self.__cliMutex.release()
                    # If an error occuring during the client ping then remove it
                    # from the clients list
                    self.__logger.logInfo("TCP/IP client socket error (%s)" % \
                        cli['id'])
                    self.__removeClient(cli)
                    aClientHasRemoved = True
                    self.__cliMutex.acquire()
                    break
                if data != "PONG":
                    self.__cliMutex.release()
                    # If the client response is invalid then remove it from the
                    # clients list
                    self.__logger.logInfo("TCP/IP client not responding (%s)" % \
                        cli['id'])
                    self.__removeClient(cli)
                    aClientHasRemoved = True
                    self.__cliMutex.acquire()
                    break
            self.__cliMutex.release()
            # Wait 2 seconds beetwen the next ping cycle is no client has been
            # removed
            if not aClientHasRemoved:
                time.sleep(2.)

    # --------------------------------------------------------------------------
    # Send a message to the connected clients.
    # --------------------------------------------------------------------------
    def notify(self, message, clientId = None):
        """Send a message to the connected clients.
        @param message: Message to notify. The maximal size of a message is 127
                        characters.
        """
        # Regularize the message length (0 > correct size < 128)
        if len(message) > 127:
            message = message[:126]
        if len(message) == 0:
            message = "NOTIFY"
        message = message + "\n" + "".join(" " * (127 - len(message)))
        self.__logger.logDebug("Notified : (%s)" % message)
        self.__cliMutex.acquire()
        if clientId == None:
            # Send the message to all registered clients
            for cli in self.__cliLst:
                if cli['address'] == None:
                    continue
                try:
                    cli['connection'].send(message)
                except:
                    # No special action if the client connection is broken, it will
                    # be removed by the "ping" loop
                    pass
            # Can't sent another message while 100 msec
            time.sleep(0.1)
        else:
            for cli in self.__cliLst:
                if cli['address'] == None:
                    continue
                if cli['id'] == clientId:
                    try:
                        cli['connection'].send(message)
                    except:
                        # No special action if the client connection is broken, it will
                        # be removed by the "ping" loop
                        pass
                    break
        self.__cliMutex.release()

    # --------------------------------------------------------------------------
    # Push events in the clients stack.
    # --------------------------------------------------------------------------
    def pushEvents(self, events = []):
        """Push events in the clients stack.
        @events: Events list.
        """
        self.__cliMutex.acquire()
        for cli in self.__cliLst:
            try:
                cli['object'].pushEvents(events)
            except:
                pass
        self.__cliMutex.release()
