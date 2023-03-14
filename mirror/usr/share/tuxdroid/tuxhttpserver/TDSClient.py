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

from util.logger import *

from TDSClientLevels import *
from TDSConfiguration import *
from TDSAccessManager import *

# ------------------------------------------------------------------------------
# Tux Droid Server : Client class.
# ------------------------------------------------------------------------------
class TDSClient(object):
    """Tux Droid Server : Client class.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, accessManager, clientsManager, id, level, loopDelay = 0.1):
        """Constructor.
        @accessManager: Access manager object.
        @clientsManager: Clients manager object.
        @id: Id client.
        @level: Client level.
        @loopDelay: Delay between two events notifications.
                    0.0 : Full real time mode. (server -> client)
                    >0.0 : Quasi real time mode. (server -> client)
                    None : Client must asking the events stack.
                           (client <-> server)
        """
        self.__logger = SimpleLogger(TDS_FILENAME_CLIENTS_LOG)
        self.__logger.setTarget(TDS_CONF_LOG_TARGET)
        self.__logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.logger = self.__logger
        self.__lastTransactionTime = time.time()
        self.__id = id
        self.__level = level
        self.__accessManager = accessManager
        self.__restrictedEventsList = []
        if loopDelay == None:
            self.__eventsStack = TDSClientEventStackSlave(clientsManager, id,
                loopDelay)
        else:
            self.__eventsStack = TDSClientEventStackMaster(clientsManager, id,
                loopDelay)
        self.__clientsManager = clientsManager
        # Start the events stack task
        self.__eventsStack.start()

    # --------------------------------------------------------------------------
    # Destructor.
    # --------------------------------------------------------------------------
    def destroy(self):
        """Destructor.
        """
        self.releaseAccess()
        self.__eventsStack.stop()

    # --------------------------------------------------------------------------
    # Get the id.
    # --------------------------------------------------------------------------
    def getId(self):
        """Get the id.
        @return: The id.
        """
        return self.__id

    # --------------------------------------------------------------------------
    # Add an event in the excluded list.
    # --------------------------------------------------------------------------
    def addExcludedEvent(self, eventName):
        """Add an event in the excluded list.
        @param eventName: Event name.
        """
        self.__eventsStack.addExcludedEvent(eventName)
        self.__logger.logDebug("Client (%s) add an excluded event : (%s)" % (
            self.__id, eventName))

    # --------------------------------------------------------------------------
    # Remove an event from the excluded list.
    # --------------------------------------------------------------------------
    def removeExcludedEvent(self, eventName):
        """Remove an event from the excluded list.
        @param eventName: Event name.
        """
        self.__eventsStack.removeExcludedEvent(eventName)
        self.__logger.logDebug("Client (%s) remove an excluded event : (%s)" % (
            self.__id, eventName))

    # --------------------------------------------------------------------------
    # Set the restricted events list.
    # --------------------------------------------------------------------------
    def setRestrictedEventsList(self, eventsList):
        """Set the restricted events list.
        Only for the RESTRICTED clients. The client need to have the access
        priority to receive these events. (Typically head, left, right buttons)
        @param eventsList: List of the restricted events.
        """
        for eventName in eventsList:
            self.__restrictedEventsList.append(eventName)

    # --------------------------------------------------------------------------
    # Push an events list to the stack.
    # --------------------------------------------------------------------------
    def pushEvents(self, events = []):
        """Push an events list to the stack.
        @param events: Events list.
        """
        if len(events) != 0:
            if self.__level == TDS_CLIENT_LEVEL_RESTRICTED:
                if not self.__accessManager.checkUserHaveAccess(self.__id):
                    eventsToSend = []
                    for event in events:
                        if event['name'] in self.__restrictedEventsList:
                            continue
                        eventsToSend.append(event)
                else:
                    eventsToSend = events
            else:
                eventsToSend = events
            if len(eventsToSend) != 0:
                self.__eventsStack.push(eventsToSend)

    # --------------------------------------------------------------------------
    # Pop the events list from the stack.
    # --------------------------------------------------------------------------
    def popEvents(self):
        """Pop the events list from the stack.
        @return: The popped events list.
        """
        self.__lastTransactionTime = time.time()
        return self.__eventsStack.pop()

    # --------------------------------------------------------------------------
    # Get the delay since the last transaction.
    # --------------------------------------------------------------------------
    def getLastTansactionDelay(self):
        """Get the delay since the last transaction.
        @return: The delay since the last transaction.
        """
        return (time.time() - self.__lastTransactionTime)

    # --------------------------------------------------------------------------
    # Check if the user have the access.
    # --------------------------------------------------------------------------
    def checkAccess(self):
        """Check if the user have the access.
        @return: True or False.
        """
        return self.__accessManager.checkUserHaveAccess(self.__id)

    # --------------------------------------------------------------------------
    # Aquire the access.
    # --------------------------------------------------------------------------
    def acquireAccess(self, priorityLevel):
        """Aquire the access.
        @param priorityLevel: <ACCESS_PRIORITY_LOW|ACCESS_PRIORITY_NORMAL|
                               ACCESS_PRIORITY_HIGH|ACCESS_PRIORITY_CRITICAL>
        @return: True or False.
        """
        return self.__accessManager.acquireAccess(self.__id, priorityLevel)

    # --------------------------------------------------------------------------
    # Release the access.
    # --------------------------------------------------------------------------
    def releaseAccess(self):
        """Release the access.
        """
        self.__accessManager.releaseAccess(self.__id)

    # --------------------------------------------------------------------------
    # Forcing to release the access.
    # --------------------------------------------------------------------------
    def forcingReleaseAccess(self):
        """Forcing to release the access. (For ROOT client)
        """
        self.__accessManager.releaseAccess()

    # --------------------------------------------------------------------------
    # Forcing to aquire the access.
    # --------------------------------------------------------------------------
    def forcingAcquireAccess(self, idClient, priorityLevel):
        """Forcing to aquire the access. (For ROOT client)
        @param idClient: Id client.
        @param priorityLevel: <ACCESS_PRIORITY_LOW|ACCESS_PRIORITY_NORMAL|
                               ACCESS_PRIORITY_HIGH|ACCESS_PRIORITY_CRITICAL>
        @return: True or False.
        """
        self.__accessManager.releaseAccess()
        return self.__accessManager.acquireAccess(idClient, priorityLevel)

    # --------------------------------------------------------------------------
    # Lock the access.
    # --------------------------------------------------------------------------
    def lockAccess(self):
        """Lock the access. (For ROOT client)
        """
        self.__accessManager.setLocked(True)

    # --------------------------------------------------------------------------
    # Unlock the access.
    # --------------------------------------------------------------------------
    def unlockAccess(self):
        """Unlock the access. (For ROOT client)
        """
        self.__accessManager.setLocked(False)

# ------------------------------------------------------------------------------
# Tux Droid Server : Client events stack ancestor.
# ------------------------------------------------------------------------------
class TDSClientEventStackBase(object):
    """Tux Droid Server : Client events stack ancestor.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, clientsManager, id, loopDelay = 0.1):
        """Constructor.
        @param clientsManager: Clients manager object.
        @param id: Id client.
        @param loopDelay: Delay between two automatic stack pop.
        """
        self._stack = []
        self._stackMutex = threading.Lock()
        self._clientsManager = clientsManager
        self._id = id
        self._excludedEvents = []

    # --------------------------------------------------------------------------
    # Start the stack task.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the stack task.
        """
        pass

    # --------------------------------------------------------------------------
    # Stop the stack task.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the stack task.
        """
        pass

    # --------------------------------------------------------------------------
    # Add an event in the excluded list.
    # --------------------------------------------------------------------------
    def addExcludedEvent(self, eventName):
        """Add an event in the excluded list.
        @param eventName: Event name.
        """
        self._stackMutex.acquire()
        self._excludedEvents.append(eventName)
        self._stackMutex.release()

    # --------------------------------------------------------------------------
    # Remove an event from the excluded list.
    # --------------------------------------------------------------------------
    def removeExcludedEvent(self, eventName):
        """Remove an event from the excluded list.
        @param eventName: Event name.
        """
        self._stackMutex.acquire()
        try:
            self._excludedEvents.remove(eventName)
        except:
            pass
        self._stackMutex.release()

    # --------------------------------------------------------------------------
    # Push an events list.
    # --------------------------------------------------------------------------
    def push(self, events = []):
        """Push an events list.
        @param events: Events list.
        """
        pass

    # --------------------------------------------------------------------------
    # Pop the events from the list.
    # --------------------------------------------------------------------------
    def pop(self):
        """Pop the events from the list.
        @return: The events list.
        """
        return []

# ------------------------------------------------------------------------------
# Tux Droid Server : Client events stack master.
# ------------------------------------------------------------------------------
class TDSClientEventStackMaster(TDSClientEventStackBase):
    """Tux Droid Server : Client events stack master.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, clientsManager, id, loopDelay = 0.1):
        """Constructor.
        @param clientsManager: Clients manager object.
        @param id: Id client.
        @param loopDelay: Delay between two automatic stack pop.
        """
        TDSClientEventStackBase.__init__(self, clientsManager, id, loopDelay)
        self.__startedMutex = threading.Lock()
        self.__startedFlag = False
        self.__loopDelay = loopDelay

    # --------------------------------------------------------------------------
    # Get the stack task is started or not.
    # --------------------------------------------------------------------------
    def getStarted(self):
        """Get the stack task is started or not.
        @return: True or False.
        """
        self.__startedMutex.acquire()
        result = self.__startedFlag
        self.__startedMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the state of the stack task.
    # --------------------------------------------------------------------------
    def __setStarted(self, value):
        """Set the state of the stack task.
        @param value: True or False.
        """
        self.__startedMutex.acquire()
        self.__startedFlag = value
        self.__startedMutex.release()

    # --------------------------------------------------------------------------
    # Pop loop.
    # --------------------------------------------------------------------------
    def __popLoop(self):
        """Pop loop.
        """
        self.__setStarted(True)
        while self.getStarted():
            time.sleep(self.__loopDelay)
            self._stackMutex.acquire()
            stack = self._stack
            self._stack = []
            self._stackMutex.release()
            for event in stack:
                eventString = "%s|%s|%s|%s" % (event['name'],
                    str(event['value']), event['type'], event['delay'])
                self._clientsManager.notify(eventString, self._id)

    # --------------------------------------------------------------------------
    # Start the stack task.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the stack task.
        """
        if self.__loopDelay != 0.0:
            t = threading.Thread(target = self.__popLoop)
            t.start()

    # --------------------------------------------------------------------------
    # Stop the stack task.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the stack task.
        """
        if self.__loopDelay != 0.0:
            self.__setStarted(False)

    # --------------------------------------------------------------------------
    # Push an events list.
    # --------------------------------------------------------------------------
    def push(self, events = []):
        """Push an events list.
        @param events: Events list.
        """
        if len(events) == 0:
            return
        self._stackMutex.acquire()
        for event in events:
            if event['name'] in self._excludedEvents:
                continue
            self._stack.append(event)
        self._stackMutex.release()
        if self.__loopDelay == 0.0:
            self.__pop()

    # --------------------------------------------------------------------------
    # Pop the events from the stack and send its to the client.
    # --------------------------------------------------------------------------
    def __pop(self):
        """Pop the events from the stack and send its to the client.
        """
        self._stackMutex.acquire()
        stack = self._stack
        self._stack = []
        self._stackMutex.release()
        def async():
            for event in stack:
                eventString = "%s|%s|%s|%s" % (event['name'],
                    str(event['value']), event['type'], event['delay'])
                self._clientsManager.notify(eventString, self._id)
        t = threading.Thread(target = async)
        t.start()

# ------------------------------------------------------------------------------
# Tux Droid Server : Client events stack slave.
# ------------------------------------------------------------------------------
class TDSClientEventStackSlave(TDSClientEventStackBase):
    """Tux Droid Server : Client events stack slave.
    """

    # --------------------------------------------------------------------------
    # Push an events list.
    # --------------------------------------------------------------------------
    def push(self, events = []):
        """Push an events list.
        @param events: Events list.
        """
        if len(events) == 0:
            return
        self._stackMutex.acquire()
        for event in events:
            if event['name'] in self._excludedEvents:
                continue
            self._stack.append(event)
        self._stackMutex.release()

    # --------------------------------------------------------------------------
    # Pop the events from the list.
    # --------------------------------------------------------------------------
    def pop(self):
        """Pop the events from the list.
        @return: The events list.
        """
        self._stackMutex.acquire()
        stack = self._stack
        self._stack = []
        self._stackMutex.release()
        return stack
