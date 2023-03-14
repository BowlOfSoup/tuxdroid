# -*- coding: latin1 -*-

# TODO : Add more complexe conditions (status1 or status2 or status 3)

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

import threading
import time
import copy
import traceback
import sys

class TuxEventHandler(object):
    """TuxEventHandler is an event controller which give to you the mechanisms to
    make interactive an asynchronous signal.
    """

    def __init__(self):
        """Constructor of the class.
        """
        self.__functStructList = []
        self.__fifoList = []
        self.__listMutex = threading.Lock()
        self.__lockList = []
        self.__lockMutex = threading.Lock()
        self.__lastState = None
        self.__lastStateMutex = threading.Lock()

    def destroy(self):
        """Destructor of the class.
        """
        self.clearPending()

    def getLastState(self):
        """Get the last knowed state of the event/status.
        @return: The last knowed state.
        """
        self.__lastStateMutex.acquire()
        result = self.__lastState
        self.__lastStateMutex.release()
        return result

    def __setLastState(self, value):
        """Set the state of the event.
        @param state: New state.
        """
        self.__lastStateMutex.acquire()
        self.__lastState = value
        self.__lastStateMutex.release()
        
    def updateState(self, state):
        """Update the state of the event without throwing callback.
        @param state: New state.
        """
        self.__setLastState(state)

    def register(self, funct, condition = None, idx = None):
        """Register a callback function.
        The "condition" is the rule to match the callback event with
        a specific set of parameters when a signal is emitted.
        The number of objects from the condition need to be the same
        than the parameters of the emitted signal.

        @param funct: function pointer.
        @param condition: list of the rules of the condition.
        @param idx: the index of the callback
        @return: the index of the callback in the handler.
        """
        if idx == None:
            result = self.__register(funct, condition)
        else:
            ret = self.__updateRegister(idx, funct, condition)
            if not ret:
                result = self.__register(funct, condition)
            else:
                result = idx

        return result

    def __register(self, funct, condition = None):
        """Called by the public register method.
        """
        self.__listMutex.acquire()
        idx = len(self.__functStructList)
        nFunct = {
            'funct' : funct,
            'condition' : condition,
        }
        self.__functStructList.append(nFunct)
        self.__listMutex.release()

        return idx

    def __updateRegister(self, idx, funct, condition = None):
        """Called by the public register method.
        """
        self.__listMutex.acquire()
        if (idx < len(self.__functStructList)) and (idx >= 0):
            nFunct = {
                'funct' : funct,
                'condition' : condition,
            }
            self.__functStructList[idx] = nFunct
            result = True
        else:
            result = False
        self.__listMutex.release()

        return result

    def unregister(self, idx):
        """Unregister a callback from the event handler.

        @param idx: index of the callback.
        """
        self.__listMutex.acquire()
        if (idx < len(self.__functStructList)) and (idx >= 0):
            self.__functStructList[idx] = None
        self.__listMutex.release()

    def storeContext(self):
        """This method store in a stack the configuration of the linked callbacks.
        In addition with the "restoreContext" and "clearContext" methods, you can manages the context
        of the event handler.
        """
        self.__listMutex.acquire()
        self.__fifoList.append(self.__functStructList)
        self.__listMutex.release()
        self.clearContext()

    def restoreContext(self):
        """This method restore from a stack the configuration of the linked callbacks.
        In addition with the "storeContext" and "clearContext" methods, you can manages the context
        of the event handler.
        """
        self.__listMutex.acquire()
        if len(self.__fifoList) > 0:
            self.__functStructList = self.__fifoList.pop()
        self.__listMutex.release()

    def clearContext(self):
        """This method clear the configuration of the linked callbacks.
        In addition with the "storeContext" and "restoreContext" methods, you can manages the context
        of the event handler.
        """
        self.__listMutex.acquire()
        self.__functStructList = []
        self.__listMutex.release()

    def __formatException(self):
        """Format the traceback.
        """
        fList = traceback.format_exception(sys.exc_info()[0],
                    sys.exc_info()[1],
                    sys.exc_info()[2])
        result = ""
        for line in fList:
            result += line
        return result

    def __run(self, functPtr, idx, fArgs):
        """Run a callback method.
        """
        def async():
            try:
                functPtr(*fArgs)
            except:
                print self.__formatException()
                self.unregister(idx)
        t = threading.Thread(target = async)
        t.start()

    def emit(self, *fArgs):
        """Emit a signal on the event handler with a set of parameters.

        @param fArgs: parameters.
        """
        self.notify(*fArgs)

    def notify(self, *fArgs):
        """Emit a signal on the event handler with a set of parameters.

        @param fArgs: parameters.
        """
        mFArgs = copy.copy(fArgs)
        self.__setLastState(mFArgs)
        self.__lockListProcess(mFArgs)

        self.__listMutex.acquire()
        if len(self.__functStructList) == 0:
            self.__listMutex.release()
            return
        try:
            functStructList = self.__functStructList
        except:
            self.__listMutex.release()
            return
        self.__listMutex.release()

        for idx, functStruct in enumerate(functStructList):

            if functStruct != None:
                conditionMatched = True
                if functStruct['condition'] != None:
                    if len(functStruct['condition']) > 0:
                        if len(functStruct['condition']) != len(mFArgs):
                            conditionMatched = False
                        else:
                            for i, rule in enumerate(functStruct['condition']):
                                if functStruct['condition'][i] not in [None, mFArgs[i]]:
                                    conditionMatched = False
                                    break

                if conditionMatched:
                    self.__run(functStruct['funct'], idx, mFArgs)

    def __lockListProcess(self, args):
        """Check if the locks needs to be released.
        """
        currentTime = time.time()

        self.__lockMutex.acquire()
        for myLock in self.__lockList:
            if myLock['timeout'] <= (currentTime - myLock['startTime']):
                myLock['result'] = False
                myLock['mutex'].acquire()
                myLock['mutex'].notify()
                myLock['mutex'].release()
                continue

            matchedCondition = True

            condition = myLock['condition']
            if condition != None:
                if len(condition) != len(args):
                    continue

                for i, rule in enumerate(condition):
                    if not rule in [None, args[i]]:
                        matchedCondition = False
                        break

            if not matchedCondition:
                continue
            else:
                myLock['result'] = True
                myLock['mutex'].acquire()
                myLock['mutex'].notify()
                myLock['mutex'].release()
        self.__lockMutex.release()

    def waitCondition(self, condition, timeout = 999999999.0):
        """Synchronize a condition with a specific event.

        @param condition: list of the rules of the condition.
        @param timeout: maximal delay to wait.
        @return:    the success of the waiting.
        """
        result = False
        mutex = threading.Condition(threading.Lock())
        newLock = {
            'condition' : condition,
            'result' : result,
            'mutex' : mutex,
            'startTime' : time.time(),
            'timeout' : timeout
        }
        self.__lockMutex.acquire()
        self.__lockList.append(newLock)
        self.__lockMutex.release()

        mutex.acquire()
        mutex.wait(timeout)
        mutex.release()

        self.__lockMutex.acquire()
        try:
            self.__lockList.remove(newLock)
        except:
            pass
        self.__lockMutex.release()

        return newLock['result']

    def clearPending(self):
        """Clear all pending wait.
        """
        self.__lockMutex.acquire()
        for myLock in self.__lockList:
            myLock['result'] = False
            myLock['mutex'].acquire()
            myLock['mutex'].notify()
            myLock['mutex'].release()
        self.__lockList = []
        self.__lockMutex.release()


if __name__ == "__main__":

    def fakeEventLoop():
        i = 0
        while i < 15:
            eventHandler.emit(1, i)
            i += 1
            time.sleep(1.)
        print "Loop of the fake events was stopped."
        print "Clear all pending conditions ..."
        eventHandler.clearPending()

    def onTestEvent(value1, value2):
        print "Event :", value1, value2

    def onTestEventC(value1, value2):
        print "Event with condition (1, 7) :", value1, value2

    print "Create an event handler..."
    eventHandler = TuxEventHandler()
    print "Insert a callback without condition ..."
    idx1 = eventHandler.register(onTestEvent)
    print "Insert a callback with condition ..."
    idx2 = eventHandler.register(onTestEventC, (1, 7))
    print "Start the loop of fake event"
    t = threading.Thread(target = fakeEventLoop)
    t.start()
    print "Wait a condition (1, 2) which will be completed ..."
    print eventHandler.waitCondition((1, 2), 10.0), "For condition (1, 2)"
    print "Wait a condition (1, 15) which will not be completed (timeout too short) ..."
    print eventHandler.waitCondition((1, 15), 5.0), "For condition (1, 15)"
    print "Wait a condition (1, 20) which will be cleared ..."
    print eventHandler.waitCondition((1, 20), 10.0), "For condition (1, 20)"
    print "Destroy the event handler ..."
    eventHandler.unregister(idx1)
    eventHandler.unregister(idx2)
    eventHandler.destroy()
    print "... Finish !!!"