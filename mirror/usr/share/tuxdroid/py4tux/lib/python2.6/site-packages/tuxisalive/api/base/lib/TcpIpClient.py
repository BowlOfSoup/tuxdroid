# -*- coding: utf-8 -*-

#    Copyleft (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import socket
import threading
import time

# ------------------------------------------------------------------------------
# TCP/IP client
# ------------------------------------------------------------------------------
class TcpIpClient(object):
    """TCP/IP client Class.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, name, level, eventsDelay):
        """Constructor.
        @param host: Host address of the server.
        @param port: Host port of the server.
        """
        self.__name = name
        self.__level = level
        self.__socket = None
        self.__run = False
        self.__runThread = None
        self.__runMutex = threading.Lock()
        self.__onNotification = None
        self.__onConnected = None
        self.__onDisconnected = None
        self.__notifyThreadsList = []
        self.__ntlMutex = threading.Lock()
        self.__id = "0"
        self.__eventsDelay = eventsDelay
        self.__autoConMutex = threading.Lock()
        self.__autoConFlag = False

    # --------------------------------------------------------------------------
    # Get the indentifier of the client.
    # --------------------------------------------------------------------------
    def getId(self):
        """Get the indentifier of the client.
        @return: The identifier if connected ortherwise '0' as string.
        """
        return self.__id

    # --------------------------------------------------------------------------
    # Register a callback function to the "On notification" event.
    # --------------------------------------------------------------------------
    def registerOnNotificationCallBack(self, funct):
        """Register a callback function to the "On notification" event.
        @param funct: Function pointer. The function must accept one parameter.
                      Example :
                      def onNotification(message):
                          print message
        """
        self.__onNotification = funct

    # --------------------------------------------------------------------------
    # Register a callback function to the "On connected" event.
    # --------------------------------------------------------------------------
    def registerOnConnectedCallBack(self, funct):
        """Register a callback function to the "On connected" event.
        @param funct: Function pointer. The function must accept one parameter.
                      Example :
                      def onConnected(identifier):
                          print "Client connected with identifier :", identifier
        """
        self.__onConnected = funct

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def registerOnDisconnectedCallBack(self, funct):
        """Register a callback function to the "On disconnected" event.
        @param funct: Function pointer.
                      Example :
                      def onDisconnected():
                          print "Client disconnected"
        """
        self.__onDisconnected = funct

    # --------------------------------------------------------------------------
    # Connect the client.
    # --------------------------------------------------------------------------
    def connect(self, host = '127.0.0.1', port = 271):
        """Connect the client.
        @return: The success of the client start.
        """
        # Exit the function if the client is already started
        if self.__getRun():
            return True
        # Create the client socket
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set the socket to blocking mode before to connect it to the server
        self.__socket.setblocking(1)
        try:
            # Connect the client to the server
            self.__socket.connect((host, port))
            # Read my client identifier
            self.__id = self.__socket.recv(128).split('\n')[0]
            self.__socket.send("%s\n%d\n%f\n" % (self.__name, self.__level,
                self.__eventsDelay))
            ack = self.__socket.recv(128).split('\n')[0]
            if ack != "ALLOWED":
                self.__setRun(False)
                self.__socket.setblocking(0)
                # Client is not authorized (typically ROOT level)
                return False
        except socket.timeout:
            self.__setRun(False)
            self.__socket.setblocking(0)
            # Failed to connect the client to the server
            return False
        except socket.error:
            self.__setRun(False)
            self.__socket.setblocking(0)
            # Failed to connect the client to the server
            return False
        # Set the socket to unblocking mode
        self.__socket.setblocking(0)
        # Set the socket timeout to 100 msec
        self.__socket.settimeout(0.1)
        self.__setRun(True)
        # Call the "On connected" event
        if self.__onConnected != None:
            t = threading.Thread(target = self.__onConnected, args = (self.__id,))
            t.start()
        # Start the message listening loop
        self.__runThread = threading.Thread(target = self.__runLoop)
        self.__runThread.start()
        time.sleep(0.1)
        # The client is successfuly connected to the server
        return True

    # --------------------------------------------------------------------------
    # Set the auto-start flag value.
    # --------------------------------------------------------------------------
    def __setAutoStartRun(self, value):
        """Set the auto-start flag value.
        @param value: Flag value.
        """
        self.__autoConMutex.acquire()
        self.__autoConFlag = value
        self.__autoConMutex.release()

    # --------------------------------------------------------------------------
    # Get the auto-start flag value.
    # --------------------------------------------------------------------------
    def __getAutoStartRun(self):
        """Get the auto-start flag value.
        @return: The the auto-start flag value.
        """
        self.__autoConMutex.acquire()
        result = self.__autoConFlag
        self.__autoConMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Auto-start loop.
    # --------------------------------------------------------------------------
    def __autoStartLoop(self, host = '127.0.0.1', port = 271):
        """Auto-start loop.
        @param host: Server host ip.
        @param port: Server port.
        """
        self.__setAutoStartRun(True)
        while self.__getAutoStartRun():
            self.connect(host, port)
            time.sleep(1.0)

    # --------------------------------------------------------------------------
    # Start the auto-connection.
    # --------------------------------------------------------------------------
    def autoConnect(self, host = '127.0.0.1', port = 271):
        """Start the auto-connection.
        @param host: Server host ip.
        @param port: Server port.
        """
        t = threading.Thread(target = self.__autoStartLoop, args = (host, port))
        t.start()

    # --------------------------------------------------------------------------
    # Stop the auto-connection loop.
    # --------------------------------------------------------------------------
    def __autoConnectStop(self):
        """Stop the auto-connection loop.
        """
        self.__setAutoStartRun(False)
        time.sleep(0.1)

    # --------------------------------------------------------------------------
    # Wait that the client was connected.
    # --------------------------------------------------------------------------
    def waitConnected(self, timeout = 10.0):
        """Wait that the client was connected.
        @param timeout: Maximal time to wait.
        @return: Is connected or not as boolean.
        """
        count = int(timeout * 10)
        while not self.__getRun():
            count -= 1
            time.sleep(0.1)
            if count == 0:
                return False
        return True

    # --------------------------------------------------------------------------
    # Get the connection state of the client.
    # --------------------------------------------------------------------------
    def getConnected(self):
        """Get the connection state of the client.
        @return: True or False.
        """
        return self.__getRun()

    def getAutoConnected(self):
        return self.__getAutoStartRun()

    # --------------------------------------------------------------------------
    # Disconnect the client.
    # --------------------------------------------------------------------------
    def disconnect(self):
        """Disconnect the client.
        """
        # Stop the auto start loop
        self.__autoConnectStop()
        # Stop the message listening loop
        self.__setRun(False)
        # Ensure that the thread of the message listening loop has been closed
        if self.__runThread != None:
            if self.__runThread.isAlive():
                if not self.__runThread.join(5.0):
                    self.__runThread._Thread__stop()

    # --------------------------------------------------------------------------
    # Add thread in the threaded messages list.
    # --------------------------------------------------------------------------
    def __addNotifyThread(self, thread):
        """Add thread in the threaded messages list.
        @param thread: Thread to be added.
        """
        self.__ntlMutex.acquire()
        self.__notifyThreadsList.append(thread)
        self.__ntlMutex.release()

    # --------------------------------------------------------------------------
    # Wait that the client was disconnected.
    # --------------------------------------------------------------------------
    def waitDisconnected(self, timeout = 10.0):
        """Wait that the client was disconnected.
        @param timeout: Maximal time to wait.
        @return: Is connected or not as boolean.
        """
        count = int(timeout * 10)
        while self.__getRun():
            count -= 1
            time.sleep(0.1)
            if count == 0:
                return False
        return True

    # --------------------------------------------------------------------------
    # Clean the closed thread from the threaded messages list.
    # --------------------------------------------------------------------------
    def __cleanNotifyThreadList(self):
        """Clean the closed thread from the threaded messages list in order to
        avoiding a memory leak issue.
        """
        self.__ntlMutex.acquire()
        newLst = []
        for t in self.__notifyThreadsList:
            if t.isAlive():
                newLst.append(t)
        self.__notifyThreadsList = newLst
        self.__ntlMutex.release()

    # --------------------------------------------------------------------------
    # Stop all threads from the threaded messages list.
    # --------------------------------------------------------------------------
    def __stopNotifyThreadList(self):
        """Stop all threads from the threaded messages list.
        """
        self.__ntlMutex.acquire()
        for t in self.__notifyThreadsList:
            if t.isAlive():
                # Wait for a hypothetical self closing of the thread
                if not t.join(0.1):
                    # Otherwise, kill it
                    t._Thread__stop()
        self.__ntlMutex.release()

    # --------------------------------------------------------------------------
    # Get the connection state of the client.
    # --------------------------------------------------------------------------
    def __getRun(self):
        """Get the connection state of the client.
        @return: True or False.
        """
        self.__runMutex.acquire()
        result = self.__run
        self.__runMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the connection state of the client.
    # --------------------------------------------------------------------------
    def __setRun(self, value = True):
        """Set the connection state of the client.
        @param value: New value (True or False)
        """
        self.__runMutex.acquire()
        self.__run = value
        self.__runMutex.release()

    # --------------------------------------------------------------------------
    # Loop listening message.
    # --------------------------------------------------------------------------
    def __runLoop(self):
        """Loop listening message.
        """
        self.__setRun(True)
        while self.__getRun():
            # Remove the closed threads from the threads list (garbage cleaning)
            self.__cleanNotifyThreadList()
            try:
                # Wait a message from the server. (timeout at 100msec, defined
                # in the function "start()")
                data = self.__socket.recv(128)
                # Invalid frame size : server error
                if len(data) != 128:
                    time.sleep(0.01)
                    break
                # Extract the message from the frame
                data = data.split('\n')[0]
                # If the message is valid
                if len(data) != 0:
                    # It's a PING
                    if data == "PING":
                        # Responding to the server
                        self.__socket.send("PONG")
                        time.sleep(0.001)
                        continue
                    # It a notification message
                    else:
                        if self.__onNotification != None:
                            # Call the "On notification" event through a thread
                            # Store the thread in the threads list in order to
                            # stop all threads at the client closure
                            t = threading.Thread(target = self.__onNotification,
                                args = (data,))
                            self.__addNotifyThread(t)
                            t.start()
                        time.sleep(0.001)
                        continue
            except socket.timeout:
                time.sleep(0.001)
                # No message from the server ...
                continue
            except socket.error:
                time.sleep(0.01)
                # Server connection was broken, exit the loop !
                break
            except:
                time.sleep(0.01)
                # Unexpected error, should never happen ...
                continue
        # The client must be disconnected
        try:
            self.__socket.close()
        except:
            pass
        self.__setRun(False)
        # Call the "On disconnected" event and reset the client identifier
        if self.__id != "0":
            if self.__onDisconnected != None:
                self.__onDisconnected()
            self.__id = "0"
