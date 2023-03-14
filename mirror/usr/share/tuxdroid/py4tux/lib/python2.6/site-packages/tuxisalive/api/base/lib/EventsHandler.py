# -*- coding: latin1 -*-

#    Copyright (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from EventHandler import EventHandler

# ------------------------------------------------------------------------------
# EventsHandler is a container of EventHandler objects.
# ------------------------------------------------------------------------------
class EventsHandler(object):
    """EventsHandler is a container of EventHandler objects.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        self.__eventDic = {}
        self.insert('all')

    # --------------------------------------------------------------------------
    # Destructor of the class.
    # --------------------------------------------------------------------------
    def destroy(self):
        """Destructor of the class.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].destroy()
        self.__eventDic = {}

    # --------------------------------------------------------------------------
    # Create and insert a new event handler in the container.
    # --------------------------------------------------------------------------
    def insert(self, eventName):
        """Create and insert a new event handler in the container.
        @param eventName: name of the new event handler.
        """
        if eventName not in self.__eventDic.keys():
            self.__eventDic[eventName] = EventHandler()
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Get the events name list.
    # --------------------------------------------------------------------------
    def getEventsNameList(self):
        """Get the events name list.
        @return: The events name list.
        """
        eventsList = self.__eventDic.keys()
        eventsList.remove("all")
        return eventsList

    # --------------------------------------------------------------------------
    # Get an event handler by its name.
    # --------------------------------------------------------------------------
    def getEventHandler(self, eventName):
        """Get an event handler by its name.
        @param eventName: name of the handler.
        @return: a EventHandler object or null if the event name was not found.
        """
        if eventName in self.__eventDic.keys():
            return self.__eventDic[eventName]
        else:
            return None

    # --------------------------------------------------------------------------
    # Register a callback function to an event handler.
    # --------------------------------------------------------------------------
    def register(self, eventName, funct, condition = None, idx = None):
        """Register a callback function to an event handler.
        @param eventName: name of the event handler.
        @param funct: function pointer.
        @param condition: list of the rules of the condition.
        @return: the index of the callback in the handler.
        """
        if eventName not in self.__eventDic.keys():
            return -1
        else:
            return self.__eventDic[eventName].register(funct, condition, idx)

    # --------------------------------------------------------------------------
    # Unregister a callback from an event handler.
    # --------------------------------------------------------------------------
    def unregister(self, eventName, idx):
        """Unregister a callback from an event handler.
        @param eventName: name of the event handler.
        @param idx: index of the callback.
        """
        if eventName in self.__eventDic.keys():
            self.__eventDic[eventName].unregister(idx)

    # --------------------------------------------------------------------------
    # This method store in a stack the configuration of the linked callbacks in
    # the event handlers.
    # --------------------------------------------------------------------------
    def storeContext(self):
        """This method store in a stack the configuration of the linked
        callbacks in the event handlers.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].storeContext()

    # --------------------------------------------------------------------------
    # This method restore from a stack the configuration of the linked callbacks
    # in the event handlers.
    # --------------------------------------------------------------------------
    def restoreContext(self):
        """This method restore from a stack the configuration of the linked
        callbacks in the event handlers.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].restoreContext()

    # --------------------------------------------------------------------------
    # This method clears the configuration of the linked callbacks in the event
    # handlers.
    # --------------------------------------------------------------------------
    def clearContext(self):
        """This method clears the configuration of the linked callbacks in the
        event handlers.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].clearContext()

    # --------------------------------------------------------------------------
    # Update the state of an event without throwing callback.
    # --------------------------------------------------------------------------
    def updateState(self, eventName, state):
        """Update the state of an event without throwing callback.
        @param eventName: name of the handler.
        @param state: state.
        """
        if eventName in self.__eventDic.keys():
            self.__eventDic[eventName].updateState(state)

    # --------------------------------------------------------------------------
    # Emit a signal on the event handler with a set of parameters.
    # --------------------------------------------------------------------------
    def emit(self, eventName, args):
        """Emit a signal on the event handler with a set of parameters.
        @param eventName: name of the handler.
        @param args: parameters.
        """
        if eventName in self.__eventDic.keys():
            self.__eventDic[eventName].emit(*args)
            args = list(args)
            args.insert(0, eventName)
            self.__eventDic['all'].emit(*args)

    # --------------------------------------------------------------------------
    # Emit a signal on the event handler with a set of parameters.
    # --------------------------------------------------------------------------
    def notify(self, eventName, args):
        """Emit a signal on the event handler with a set of parameters.
        @param eventName: name of the handler.
        @param args: parameters.
        """
        if eventName in self.__eventDic.keys():
            self.__eventDic[eventName].emit(*args)
            args = list(args)
            args.insert(0, eventName)
            self.__eventDic['all'].emit(*args)

    # --------------------------------------------------------------------------
    # Synchronize a condition with a specific event.
    # --------------------------------------------------------------------------
    def waitCondition(self, eventName, condition, timeout = 999999999.0):
        """Synchronize a condition with a specific event.
        @param eventName: name of the handler.
        @param condition: list of the rules of the condition.
        @param timeout: maximal delay to wait.
        @return: the success of the waiting.
        """
        if eventName not in self.__eventDic.keys():
            return False
        else:
            return self.__eventDic[eventName].waitCondition(condition, timeout)

    # --------------------------------------------------------------------------
    # Clear all pending wait.
    # --------------------------------------------------------------------------
    def clearPending(self):
        """Clear all pending wait.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].clearPending()
