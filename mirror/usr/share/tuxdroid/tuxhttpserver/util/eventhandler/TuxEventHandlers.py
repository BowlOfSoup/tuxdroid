# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from TuxEventHandler import TuxEventHandler

class TuxEventHandlers(object):
    """TuxEventHandlers is a container of TuxEventHandler objects.
    """

    def __init__(self):
        """Constructor of the class.
        """
        self.__eventDic = {}
        self.insert('all')

    def destroy(self):
        """Destructor of the class.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].destroy()
        self.__eventDic = {}

    def insert(self, eventName):
        """Create and insert a new event handler in the container.
        @param eventName: name of the new event handler.
        """
        if eventName not in self.__eventDic.keys():
            self.__eventDic[eventName] = TuxEventHandler()
            return True
        else:
            return False

    def getEventsNameList(self):
        """Get the events name list.
        @return: The events name list.
        """
        eventsList = self.__eventDic.keys()
        eventsList.remove("all")
        return eventsList

    def getEventHandler(self, eventName):
        """Get an event handler by its name.
        @param eventName: name of the handler.
        @return: a TuxEventHandler object or null if the event name was not found.
        """
        if eventName in self.__eventDic.keys():
            return self.__eventDic[eventName]
        else:
            return None

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

    def unregister(self, eventName, idx):
        """Unregister a callback from an event handler.
        @param eventName: name of the event handler.
        @param idx: index of the callback.
        """
        if eventName in self.__eventDic.keys():
            self.__eventDic[eventName].unregister(idx)

    def storeContext(self):
        """This method store in a stack the configuration of the linked callbacks in
        the event handlers.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].storeContext()

    def restoreContext(self):
        """This method restore from a stack the configuration of the linked callbacks in
        the event handlers.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].restoreContext()

    def clearContext(self):
        """This method clears the configuration of the linked callbacks in the
        event handlers.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].clearContext()

    def updateState(self, eventName, state):
        """Update the state of an event without throwing callback.
        @param eventName: name of the handler.
        @param state: state.
        """
        if eventName in self.__eventDic.keys():
            self.__eventDic[eventName].updateState(state)

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

    def clearPending(self):
        """Clear all pending wait.
        """
        for eventName in self.__eventDic.keys():
            self.__eventDic[eventName].clearPending()

if __name__ == "__main__":
    import threading
    import time

    def fakeEventLoop():
        i = 0
        while i < 15:
            eventHandlers.emit("testEvent", (1, i))
            i += 1
            time.sleep(1.)
        print "Loop of the fake events was finished."
        print "Clear all pending conditions ..."
        eventHandlers.clearPending()

    def onTestEvent(value1, value2):
        print "Event :", value1, value2

    def onTestEventC(value1, value2):
        print "Event with condition (1, 7) :", value1, value2

    print "Create an event handlers ..."
    eventHandlers = TuxEventHandlers()
    print "Insert a new event ..."
    eventHandlers.insert("testEvent")
    print "Insert a callback without condition ..."
    idx1 = eventHandlers.register("testEvent", onTestEvent)
    print "Insert a callback with condition ..."
    idx2 = eventHandlers.register("testEvent", onTestEventC, (1, 7))
    print "Start the loop of fake event"
    t = threading.Thread(target = fakeEventLoop)
    t.start()
    print "Store and clear the current context of callbacks. Callbacks must be inactive ..."
    eventHandlers.storeContext()
    eventHandlers.clearContext()
    print "Wait a condition (1, 2) which will be completed ..."
    print eventHandlers.waitCondition("testEvent", (1, 2), 10.0), "For condition (1, 2)"
    print "Wait a condition (1, 15) which will not be completed (timeout too short) ..."
    print eventHandlers.waitCondition("testEvent", (1, 15), 5.0), "For condition (1, 15)"
    print "Restore the previous context of callbacks ..."
    eventHandlers.restoreContext()
    print "Wait a condition (1, 20) which will be cleared ..."
    print eventHandlers.waitCondition("testEvent", (1, 20), 10.0), "For condition (1, 20)"
    print "Destroy the event handlers ..."
    eventHandlers.unregister("testEvent", idx1)
    eventHandlers.unregister("testEvent", idx2)
    eventHandlers.destroy()
    print "... Finish !!!"