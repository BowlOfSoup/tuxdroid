#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import time

from util.string.String import String

PGU_CONTEXT_LAYER_USER = 0
PGU_CONTEXT_LAYER_SCHEDULER = 1

PGU_EVENT_TYPE_MESSAGE = 0
PGU_EVENT_TYPE_ACTUATION = 1
PGU_EVENT_TYPE_ATTITUNE = 2

class PguContext(object):
    """
    """

    def __init__(self, pluginInterpreterContext):
        """
        """
        self.__createTime = time.time()
        self.__pluginInterpreterContext = pluginInterpreterContext
        uuid = pluginInterpreterContext.getHostUuid()
        # Get pguObject
        self.__pguObject = resourcePluginsServer.getPluginsContainer().getPluginByUuid(uuid)
        if self.__pguObject == None:
            self.__pguObject = resourceGadgetsServer.getGadgetsContainer().getGadgetByUuid(uuid)
        if self.__pguObject == None:
            self.__pguObject = resourceUgcServer.getUgcContainer().getUgcByUuid(uuid)
        # Get context layer
        self.__contextLayer = PGU_CONTEXT_LAYER_USER
        if self.__pluginInterpreterContext.getInstanceParameters().has_key("startedBy"):
            if self.__pluginInterpreterContext.getInstanceParameters()['startedBy'] == 'scheduler':
                self.__contextLayer = PGU_CONTEXT_LAYER_SCHEDULER
        self.__eventStack = []
        self.__messagesHistory = []
        self.__eventStackMutex = threading.Lock()
        self.__contextComplete = False
        self.__contextCompleteMutex = threading.Lock()
        self.__startStopPauseMutex = threading.Lock()
        self.__execStarted = False
        self.__execPaused = False
        self.__language = resourcePluginsServer.getPluginsContainer().getLanguage()

    def getPluginInterpreterContext(self):
        """
        """
        return self.__pluginInterpreterContext

    def getPguUuid(self):
        """
        """
        return self.__pluginInterpreterContext.getHostUuid()

    def getPguName(self):
        """
        """
        return self.__pguObject.getDescription().getName()

    def getContextLayer(self):
        """
        """
        return self.__contextLayer

    def getPguObject(self):
        """
        """
        return self.__pguObject

    def isDaemon(self):
        """
        """
        return self.__pluginInterpreterContext.instanceIsDaemon()

    def getPluginCommand(self):
        """
        """
        if self.__pguObject != None:
            return self.__pguObject.getCommand(
                self.__pluginInterpreterContext.getInstanceCommandName())
        else:
            return None

    def setContextIsComplete(self):
        """
        """
        if not self.contextIsComplete():
            print "PGU Context [%s] : content is complete" % self.getPguName()
            self.__contextCompleteMutex.acquire()
            self.__contextComplete = True
            self.__contextCompleteMutex.release()

    def contextIsComplete(self):
        """
        """
        self.__contextCompleteMutex.acquire()
        result = self.__contextComplete
        self.__contextCompleteMutex.release()
        return result

    def __insertEvent(self, eventType, arguments = {}):
        """
        """
        if self.contextIsComplete():
            return
        self.__eventStackMutex.acquire()
        self.__eventStack.append({
            'type' : eventType,
            'arguments' : arguments,
        })
        self.__eventStackMutex.release()
        print "PGU context [%s] : Insert event (%s)" % (self.getPguName(), eventType)

    def __getEvent(self):
        """
        """
        self.__eventStackMutex.acquire()
        result = None
        if len(self.__eventStack) > 0:
            result = self.__eventStack.pop(0)
        self.__eventStackMutex.release()
        return result

    def getMessagesHistory(self):
        """
        """
        self.__eventStackMutex.acquire()
        result = []
        for message in self.__messagesHistory:
            result.append(message)
        self.__eventStackMutex.release()
        return result

    def insertMessage(self, message, locutor, pitch):
        """
        """
        self.__insertEvent(PGU_EVENT_TYPE_MESSAGE, {
            'message' : message,
            'locutor' : locutor,
            'pitch' : pitch,
        })
        self.__messagesHistory.append(message)

    def insertActuation(self, actuationName, arguments = []):
        """
        """
        # Little hack for plugins audio menu
        if actuationName == "abortTts":
            self.__breakMessage()
            return
        self.__insertEvent(PGU_EVENT_TYPE_ACTUATION, {
            'actuationName' : actuationName,
            'actuationArguments' : arguments,
        })

    def insertAttitune(self, attituneName):
        """
        """
        self.__insertEvent(PGU_EVENT_TYPE_ATTITUNE, {
            'attituneName' : attituneName,
        })

    def startExecution(self):
        """
        """
        if self.executionIsStarted():
            return
        expirationDelay = self.getPluginCommand().getExpirationDelay()
        if expirationDelay > 0:
            if (time.time() - self.__createTime) > expirationDelay:
                print "PGU context [%s] : Execution aborted (Context expiration)" % self.getPguName()
                return
        self.__startStopPauseMutex.acquire()
        self.__execStarted = True
        self.__execPaused = False
        self.__startStopPauseMutex.release()
        print "PGU context [%s] : Start execution" % self.getPguName()
        self.__executionLoop()

    def executionIsStarted(self):
        """
        """
        self.__startStopPauseMutex.acquire()
        result = self.__execStarted
        self.__startStopPauseMutex.release()
        return result

    def stopExecution(self):
        """
        """
        if not self.getPluginCommand().isNotifier():
            while self.__pluginInterpreterContext.isRun():
                self.__pluginInterpreterContext.abort()
                time.sleep(0.1)
        if not self.executionIsStarted():
            return
        print "PGU context [%s] : Stop execution" % self.getPguName()
        self.__startStopPauseMutex.acquire()
        self.__execStarted = False
        self.__execPaused = False
        self.__eventStackMutex.acquire()
        self.__eventStack = []
        self.__eventStackMutex.release()
        self.__startStopPauseMutex.release()
        self.__breakAttitune()
        self.__breakMessage()
        self.__breakActuation()
        print "PGU context [%s] : Execution stopped" % self.getPguName()
        if not self.getPluginCommand().isNotifier():
            if self.getContextLayer() == PGU_CONTEXT_LAYER_SCHEDULER:
                resourceTuxDriver.playSound(15, 100.0)
            else:
                resourceTuxDriver.playSound(16, 100.0)
            time.sleep(0.5)

    def pauseExecution(self):
        """
        """
        if not self.executionIsStarted():
            return
        if self.executionIsPaused():
            return
        print "PGU context [%s] : Pause execution" % self.getPguName()
        self.__startStopPauseMutex.acquire()
        self.__execPaused = True
        self.__startStopPauseMutex.release()
        self.__breakAttitune()
        self.__breakMessage()
        self.__breakActuation()

    def unpauseExecution(self):
        """
        """
        if not self.executionIsStarted():
            return
        if not self.executionIsPaused():
            return
        print "PGU context [%s] : Unpause execution" % self.getPguName()
        self.__startStopPauseMutex.acquire()
        self.__execPaused = False
        self.__startStopPauseMutex.release()

    def executionIsPaused(self):
        """
        """
        self.__startStopPauseMutex.acquire()
        result = self.__execPaused
        self.__startStopPauseMutex.release()
        return result

    def __executeAttitune(self, attituneName):
        """
        """
        resourceAttituneManager.playAttituneSync(attituneName, 0.0)

    def __breakAttitune(self):
        """
        """
        resourceAttituneManager.stopAttitune()

    def __executeMessage(self, text, locutor, pitch):
        """
        """
        if not self.executionIsStarted():
            return
        resourceTuxDriver.openMouth()
        if not self.executionIsStarted():
            resourceTuxDriver.closeMouth()
            return
        text = ttsFixer.fixeWordsInText(text, self.__language)
        resourceTuxOSL.ttsSpeak(text, locutor, pitch)
        if not self.executionIsStarted():
            resourceTuxDriver.closeMouth()
            return
        if not eventsHandler.waitCondition(ST_NAME_TTS_SOUND_STATE, ("ON",
            None), 3.0):
            return
        if self.executionIsStarted():
            eventsHandler.waitCondition(ST_NAME_TTS_SOUND_STATE, ("OFF", None),
                600.0)
        resourceTuxDriver.closeMouth()

    def __breakMessage(self):
        """
        """
        resourceTuxOSL.ttsStop()
        eventsHandler.emit(ST_NAME_TTS_SOUND_STATE, ("OFF", 0.0))

    def __executeActuation(self, actuationName, arguments):
        """
        """
        argsString = ""
        for argument in arguments:
            if len(argsString) > 0:
                argsString += ","
            try:
                argument = int(argument)
                argsString += str(argument)
            except:
                try:
                    argument = float(argument)
                    argsString += str(argument)
                except:
                    argsString += '"' + str(argument) + '"'
        cmdString = "resourceTuxDriver.%s(%s)" % (actuationName, argsString)
        try:
            exec(cmdString) in globals()
        except:
            print "!!! Error in command :", cmdString

    def __breakActuation(self):
        """
        """
        resourceTuxDriver.clearAll()

    def __executionLoop(self):
        """
        """
        if not self.getPluginCommand().isNotifier():
            if self.getContextLayer() == PGU_CONTEXT_LAYER_SCHEDULER:
                introAtt = None
                try:
                    introAtt = self.getPguObject().getAlertAttitune()
                    if introAtt == "----":
                        introAtt = None
                except:
                    pass
                if introAtt != None:
                    self.__executeAttitune(introAtt)
                else:
                    resourceTuxDriver.playSound(14, 100.0)
                    time.sleep(0.5)
            else:
                resourceTuxDriver.playSound(13, 100.0)
                time.sleep(0.5)
        while self.executionIsStarted():
            while self.executionIsPaused():
                time.sleep(0.1)
            nextEvent = self.__getEvent()
            if nextEvent == None:
                if self.contextIsComplete():
                    self.__startStopPauseMutex.acquire()
                    self.__execStarted = False
                    self.__execPaused = False
                    self.__startStopPauseMutex.release()
                    print "PGU context [%s] : Execution stopped" % self.getPguName()
                    if not self.getPluginCommand().isNotifier():
                        if self.getContextLayer() == PGU_CONTEXT_LAYER_SCHEDULER:
                            resourceTuxDriver.playSound(15, 100.0)
                        else:
                            resourceTuxDriver.playSound(16, 100.0)
                        time.sleep(0.5)
                    return
            else:
                print "PGU context [%s] : Execute event (%s)" % (self.getPguName(), nextEvent['type'])
                arguments = nextEvent['arguments']
                if not self.executionIsStarted():
                    continue
                if nextEvent['type'] == PGU_EVENT_TYPE_MESSAGE:
                    self.__executeMessage(arguments['message'],
                        arguments['locutor'], arguments['pitch'])
                elif nextEvent['type'] == PGU_EVENT_TYPE_ACTUATION:
                    self.__executeActuation(arguments['actuationName'],
                        arguments['actuationArguments'])
                elif nextEvent['type'] == PGU_EVENT_TYPE_ATTITUNE:
                    self.__executeAttitune(arguments['attituneName'])
                print "PGU context [%s] : Event finished (%s)" % (self.getPguName(), nextEvent['type'])
            time.sleep(0.1)

class PguContextsManager(object):
    """
    """

    def __init__(self):
        """
        """
        self.__pguContexts = []
        self.__pguContextsMutex = threading.Lock()
        self.__backgroundPguContext = None
        self.__foregroundPguContext = None
        self.__backgroundPguThread = None
        self.__bfPguContextMutex = threading.Lock()
        self.__isStarted = False
        self.__startedMutex = threading.Lock()
        self.__ugcInsertionMutex = threading.Lock()
        self.__loopThread = None
        self.__onDemandList = []
        self.__onDemandIndex = 0
        self.__onDemandDictForThumbnailBar = {}
        self.__onDemandDictForThumbnailBarMutex = threading.Lock()
        self.__lastRunStopActionTime = time.time()
        self.__lastRunStopActionTimeMutex = threading.Lock()

    def insertOnDemand(self, ugc):
        """
        """
        self.__onDemandList = []
        for ugcObj in resourceUgcServer.getUgcContainer().getUgcs():
            if ugcObj.getDescription().onDemandIsActivated() == 'true':
                self.__onDemandList.append(ugcObj)
        self.computeOnDemandDictForThumbnailBar()

    def removeOnDemand(self, ugc):
        """
        """
        for odUgc in self.__onDemandList:
            if odUgc == ugc:
                self.__onDemandList.remove(ugc)
                self.computeOnDemandDictForThumbnailBar()
                return

    def __speakOnDemand(self, intoSentence = ""):
        """
        """
        if len(self.__onDemandList) > 0:
            resourceTuxOSL.ttsStop()
            ugc = self.__onDemandList[self.__onDemandIndex]
            ugcTtsName = intoSentence + " " + ugc.getDescription().getName()
            locutor = resourcePluginsServer.getPluginsContainer().getLocutor()
            pitch = resourcePluginsServer.getPluginsContainer().getPitch()
            language = resourcePluginsServer.getPluginsContainer().getLanguage()
            fixedName = ttsFixer.fixeWordsInText(ugcTtsName, language)
            resourceTuxDriver.openMouth()
            resourceTuxOSL.ttsSpeak(fixedName, locutor, pitch)
            if not eventsHandler.waitCondition(ST_NAME_TTS_SOUND_STATE, ("ON",
                None), 3.0):
                return
            eventsHandler.waitCondition(ST_NAME_TTS_SOUND_STATE, ("OFF", None),
                600.0)
            resourceTuxDriver.closeMouth()

    def __onDemandNext(self):
        """
        """
        self.__onDemandIndex += 1
        if self.__onDemandIndex >= len(self.__onDemandList):
            self.__onDemandIndex = 0
        self.computeOnDemandDictForThumbnailBar()
        resourceTuxDriver.playSound(11, 100.0)
        self.__speakOnDemand()

    def __onDemandPrevious(self):
        """
        """
        self.__onDemandIndex -= 1
        if self.__onDemandIndex < 0:
            self.__onDemandIndex = len(self.__onDemandList) - 1
        self.computeOnDemandDictForThumbnailBar()
        resourceTuxDriver.playSound(11, 100.0)
        self.__speakOnDemand()

    def selectOnDemandByUuid(self, uuid):
        """
        """
        for i, ugcObj in enumerate(self.__onDemandList):
            if ugcObj.getDescription().getUuid() == uuid:
                self.__onDemandIndex = i
                self.computeOnDemandDictForThumbnailBar()
                return True
        return False

    def computeOnDemandDictForThumbnailBar(self):
        """
        """
        self.__onDemandDictForThumbnailBarMutex.acquire()
        self.__onDemandDictForThumbnailBar = {}
        if len(self.__onDemandList) == 0:
            self.__onDemandDictForThumbnailBarMutex.release()
            return
        maxListSize = len(self.__onDemandList)
        minIdx = 0
        maxIdx = maxListSize - 1
        centerIdx = self.__onDemandIndex
        def fillByIndex(rel, number):
            currIdx = (centerIdx + rel) % maxListSize
            ugc = self.__onDemandList[currIdx]
            self.__onDemandDictForThumbnailBar["gadget_%.2d_name" % number] = ugc.getDescription().getName()
            self.__onDemandDictForThumbnailBar["gadget_%.2d_uuid" % number] = ugc.getDescription().getUuid()
            self.__onDemandDictForThumbnailBar["gadget_%.2d_icon" % number] = "/%s/icon.png" % ugc.getParentGadget().getDescription().getUuid()
            if rel == 0:
                self.__onDemandDictForThumbnailBar["gadget_%.2d_description" % number] = ugc.getParentGadget().getDescription().getDescription(ugc.getContainer().getLanguage())

        fillByIndex(-3, 1)
        fillByIndex(-2, 2)
        fillByIndex(-1, 3)
        fillByIndex(0, 4)
        fillByIndex(1, 5)
        fillByIndex(2, 6)
        fillByIndex(3, 7)
        self.__onDemandDictForThumbnailBarMutex.release()

    def getGadgetsDictOnDemand(self):
        """
        """
        result = {}
        count = 0
        for ugcObj in resourceUgcServer.getUgcContainer().getUgcs():
            if ugcObj.getDescription().onDemandIsActivated() == 'true':
                result["gadget_%d_name" % count] = ugcObj.getDescription().getName()
                result["gadget_%d_uuid" % count] = ugcObj.getDescription().getUuid()
                result["gadget_%d_icon" % count] = "/%s/icon.png" % ugcObj.getParentGadget().getDescription().getUuid()
                result["gadget_%d_ondemand" % count] = ugcObj.getParentGadget().getDescription().onDemandIsAble()
                count += 1
        result['count'] = count
        return result

    def getGadgetsDictAll(self):
        """
        """
        result = {}
        count = 0
        for ugcObj in resourceUgcServer.getUgcContainer().getUgcs():
            result["gadget_%d_name" % count] = ugcObj.getDescription().getName()
            result["gadget_%d_uuid" % count] = ugcObj.getDescription().getUuid()
            result["gadget_%d_icon" % count] = "/%s/icon.png" % ugcObj.getParentGadget().getDescription().getUuid()
            result["gadget_%d_ondemand" % count] = ugcObj.getParentGadget().getDescription().onDemandIsAble()
            count += 1
        result['count'] = count
        return result

    def getGadgetsDictAlerts(self):
        """
        """
        result = {}
        count = 0
        for ugcObj in resourceUgcServer.getUgcContainer().getUgcs():
            taskActive = False
            for task in ugcObj.getTasks():
                if task.isActivated():
                    taskActive = True
                    break
            if taskActive:
                result["gadget_%d_name" % count] = ugcObj.getDescription().getName()
                result["gadget_%d_uuid" % count] = ugcObj.getDescription().getUuid()
                result["gadget_%d_icon" % count] = "/%s/icon.png" % ugcObj.getParentGadget().getDescription().getUuid()
                result["gadget_%d_ondemand" % count] = ugcObj.getParentGadget().getDescription().onDemandIsAble()
                count += 1
        result['count'] = count
        return result

    def getOnDemandDictForThumbnailBar(self):
        """
        """
        self.__onDemandDictForThumbnailBarMutex.acquire()
        result = self.__onDemandDictForThumbnailBar
        self.__onDemandDictForThumbnailBarMutex.release()
        return result

    def getCurrentUgcForegroundScheduled(self):
        """
        """
        result = {}
        self.__bfPguContextMutex.acquire()
        pguContext = self.__foregroundPguContext
        if pguContext != None:
            if pguContext.getContextLayer() == PGU_CONTEXT_LAYER_SCHEDULER:
                result['icon'] = "/%s/icon.png" % pguContext.getPguObject().getParentGadget().getDescription().getUuid()
                result['name'] = pguContext.getPguObject().getDescription().getName()
                result['uuid'] = pguContext.getPguObject().getDescription().getUuid()
        self.__bfPguContextMutex.release()
        return result

    def getLastStartedOnDemandUgcMessages(self):
        """
        """
        def fillResult(pguContext):
            result = {}
            if pguContext == None:
                result['count'] = 0
                return result
            else:
                if not pguContext.executionIsStarted():
                    result['count'] = 0
                    return result
            messages = pguContext.getMessagesHistory()
            result['count'] = len(messages)
            for i, message in enumerate(messages):
                result['msg_%d' % i] = message
            return result
        self.__bfPguContextMutex.acquire()
        pguContext = self.__foregroundPguContext
        if pguContext != None:
            if pguContext.getContextLayer() != PGU_CONTEXT_LAYER_SCHEDULER:
                ret = fillResult(pguContext)
            else:
                ret = fillResult(self.__backgroundPguContext)
        else:
            ret = fillResult(self.__backgroundPguContext)
        self.__bfPguContextMutex.release()
        return ret

    def __setStarted(self, value):
        """
        """
        self.__startedMutex.acquire()
        self.__isStarted = value
        self.__startedMutex.release()

    def isStarted(self):
        """
        """
        self.__startedMutex.acquire()
        result = self.__isStarted
        self.__startedMutex.release()
        return result

    def start(self):
        """
        """
        self.__loopThread = threading.Thread(target = self.__executionLoop)
        self.__loopThread.start()

    def stop(self):
        """
        """
        self.__setStarted(False)
        if self.getForegroundPguContext() != None:
            self.getForegroundPguContext().stopExecution()
        if self.__loopThread != None:
            if self.__loopThread.isAlive():
                self.__loopThread.join()

    def mute(self):
        """
        """
        self.stop()
        resourceTuxDriver.playSound(12, 100.0)
        self.__contextBtStandby("remote", ("K_STANDBY", 0.0))

    def unmute(self):
        """
        """
        resourceTuxDriver.playSound(12, 100.0)
        self.start()

    def __executionLoop(self):
        """
        """
        if self.isStarted():
            return
        self.__setStarted(True)
        while self.isStarted():
            if self.backgroundPguContextIsCritical():
                time.sleep(0.5)
                continue
            # Get the next pguContext which must be in foreground
            pguContext = None
            self.__pguContextsMutex.acquire()
            if len(self.__pguContexts) > 0:
                pguContext = self.__pguContexts.pop(0)
            if pguContext != None:
                self.__setForegroundPguContext(pguContext)
                self.__pguContextsMutex.release()
                if self.getBackgroundPguContext() != None:
                    # If the context is exclusive then stop the background context
                    if pguContext.getPluginCommand().isExclusive():
                        try:
                            self.getBackgroundPguContext().stopExecution()
                        except:
                            pass
                    # Else only pause-it
                    else:
                        self.getBackgroundPguContext().pauseExecution()
                self.getForegroundPguContext().startExecution()
                if self.getBackgroundPguContext() != None:
                    # Unpause background context
                    if self.getBackgroundPguContext() != None:
                        try:
                            self.getBackgroundPguContext().unpauseExecution()
                        except:
                            pass
                self.__setForegroundPguContext(None)
            else:
                self.__pguContextsMutex.release()
            time.sleep(1.0)

    def createPguContext(self, pluginInterpreterContext):
        """
        """
        if not self.isStarted():
            return
        # Create new pguContext
        pguContext = PguContext(pluginInterpreterContext)
        # Add the new pguContext in the system
        self.__insertPguContext(pguContext)

    def __startBackgroundPguContext(self):
        """
        """
        self.getBackgroundPguContext().startExecution()

    def __insertPguContext(self, pguContext):
        """
        """
        self.__ugcInsertionMutex.acquire()
        if pguContext.getPguObject() == None:
            self.__ugcInsertionMutex.release()
            return
        # Alerts and no daemon user calls must be inserted in the stack
        # as foreground.
        if (pguContext.getContextLayer() == PGU_CONTEXT_LAYER_SCHEDULER) or\
            (not pguContext.isDaemon()):
            self.__pguContextsMutex.acquire()
            for i, regPguContext in enumerate(self.__pguContexts):
                if regPguContext.getPguName() == pguContext.getPguName():
                    # Replace the context with the same pgu name.
                    print "PGU context [%s] updated in stack" % pguContext.getPguName()
                    self.__pguContexts[i] = pguContext
                    self.__pguContextsMutex.release()
                    self.__ugcInsertionMutex.release()
                    return
            # If the context command is critical and the context is run by the
            # scheduler then stop the current context and add the context on top
            # of the stack
            if (pguContext.getPluginCommand().isCritical()) and \
                (pguContext.getContextLayer() == PGU_CONTEXT_LAYER_SCHEDULER):
                self.__pguContexts.insert(0, pguContext)
                if self.getForegroundPguContext() != None:
                    self.getForegroundPguContext().stopExecution()
            # Add the new context at the bottom of the stack.
            else:
                self.__pguContexts.append(pguContext)
            self.__pguContextsMutex.release()
        # Daemon user calls must be referenced as background.
        else:
            currentBackgroundPguContext = self.getBackgroundPguContext()
            if currentBackgroundPguContext != None:
                # Stop old background context if exists
                currentBackgroundPguContext.stopExecution()
                if self.__backgroundPguThread != None:
                    if self.__backgroundPguThread.isAlive():
                        self.__backgroundPguThread.join()
            self.__setBackgroundPguContext(pguContext)
            self.__backgroundPguThread = threading.Thread(target = self.__startBackgroundPguContext)
            self.__backgroundPguThread.start()
        self.__ugcInsertionMutex.release()

    def getForegroundPguContext(self):
        """
        """
        self.__bfPguContextMutex.acquire()
        result = self.__foregroundPguContext
        self.__bfPguContextMutex.release()
        return result

    def getBackgroundPguContext(self):
        """
        """
        self.__bfPguContextMutex.acquire()
        result = self.__backgroundPguContext
        self.__bfPguContextMutex.release()
        return result

    def backgroundPguContextIsCritical(self):
        """
        """
        self.__bfPguContextMutex.acquire()
        result = False
        if self.__backgroundPguContext != None:
            if self.__backgroundPguContext.executionIsStarted():
                if self.__backgroundPguContext.getPluginCommand().isCritical():
                    result = True
        self.__bfPguContextMutex.release()
        return result

    def backgroundPguContextIsExclusive(self):
        """
        """
        self.__bfPguContextMutex.acquire()
        result = False
        if self.__backgroundPguContext != None:
            if self.__backgroundPguContext.executionIsStarted():
                if self.__backgroundPguContext.getPluginCommand().isExclusive():
                    result = True
        self.__bfPguContextMutex.release()
        return result

    def backgroundPguContextNeedAllUserButtons(self):
        """
        """
        self.__bfPguContextMutex.acquire()
        result = False
        if self.__backgroundPguContext != None:
            if self.__backgroundPguContext.executionIsStarted():
                if self.__backgroundPguContext.getPluginCommand().needAllUserButtons():
                    result = True
        self.__bfPguContextMutex.release()
        return result

    def __setForegroundPguContext(self, pguContext):
        """
        """
        self.__bfPguContextMutex.acquire()
        self.__foregroundPguContext = pguContext
        self.__bfPguContextMutex.release()

    def __setBackgroundPguContext(self, pguContext):
        """
        """
        self.__bfPguContextMutex.acquire()
        self.__backgroundPguContext = pguContext
        self.__bfPguContextMutex.release()

    def getPguContext(self, pluginInterpreterContext, noMutex = False):
        """
        """
        result = None
        if not noMutex:
            self.__pguContextsMutex.acquire()
        for pguContext in self.__pguContexts:
            if pguContext.getPluginInterpreterContext() == pluginInterpreterContext:
                result = pguContext
                break
        if result == None:
            if self.getForegroundPguContext() != None:
                if self.getForegroundPguContext().getPluginInterpreterContext() == pluginInterpreterContext:
                    result = self.getForegroundPguContext()
        if result == None:
            if self.getBackgroundPguContext() != None:
                if self.getBackgroundPguContext().getPluginInterpreterContext() == pluginInterpreterContext:
                    result = self.getBackgroundPguContext()
        if not noMutex:
            self.__pguContextsMutex.release()
        return result

    # ==========================================================================
    # Events from plugins execution.
    # ==========================================================================

    def insertMessage(self, pluginInterpreterContext, message, locutor, pitch):
        """
        """
        self.__pguContextsMutex.acquire()
        pguContext = self.getPguContext(pluginInterpreterContext, True)
        if pguContext != None:
            pguContext.insertMessage(message, locutor, pitch)
        self.__pguContextsMutex.release()

    def insertActuation(self, pluginInterpreterContext, actuationName,
        arguments = []):
        """
        """
        self.__pguContextsMutex.acquire()
        pguContext = self.getPguContext(pluginInterpreterContext, True)
        if pguContext != None:
            pguContext.insertActuation(actuationName, arguments)
        self.__pguContextsMutex.release()

    def insertAttitune(self, pluginInterpreterContext, attituneName):
        """
        """
        self.__pguContextsMutex.acquire()
        pguContext = self.getPguContext(pluginInterpreterContext, True)
        if pguContext != None:
            pguContext.insertAttitune(attituneName)
        self.__pguContextsMutex.release()

    def setContextIsComplete(self, pluginInterpreterContext):
        """
        """
        self.__pguContextsMutex.acquire()
        pguContext = self.getPguContext(pluginInterpreterContext, True)
        if pguContext != None:
            pguContext.setContextIsComplete()
        self.__pguContextsMutex.release()

    # ==========================================================================
    # Remote and robot button events
    # ==========================================================================

    def __setLastRunStopActionTime(self):
        """
        """
        self.__lastRunStopActionTimeMutex.acquire()
        self.__lastRunStopActionTime = time.time()
        self.__lastRunStopActionTimeMutex.release()

    def __getLastRunStopActionTime(self):
        """
        """
        self.__lastRunStopActionTimeMutex.acquire()
        result = self.__lastRunStopActionTime
        self.__lastRunStopActionTimeMutex.release()
        return result

    def __checkLastRunActionTime(self):
        """
        """
        if (time.time() - self.__getLastRunStopActionTime()) >= 1.5:
            self.__setLastRunStopActionTime()
            return True
        else:
            return False

    def __checkLastStopActionTime(self):
        """
        """
        if (time.time() - self.__getLastRunStopActionTime()) >= 0.5:
            self.__setLastRunStopActionTime()
            return True
        else:
            return False

    def __contextBtRunAbort(self, eventName, *args):
        """
        """
        # Abort foreground context if exists
        if self.getForegroundPguContext() != None:
            if self.getForegroundPguContext().executionIsStarted():
                if not self.__checkLastRunActionTime():
                    return
                self.getForegroundPguContext().stopExecution()
                return
        # Else abort background context if exists
        if self.getBackgroundPguContext() != None:
            if self.getBackgroundPguContext().executionIsStarted():
                # Exception for plugins commands with attribute "allUserButtons"
                if self.backgroundPguContextNeedAllUserButtons():
                    self.__contextBtOther(eventName, *args)
                    return
                if not self.__checkLastRunActionTime():
                    return
                self.getBackgroundPguContext().stopExecution()
                return
        # Else load current selected on demand gadget
        if len(self.__onDemandList) > 0:
            ugc = self.__onDemandList[self.__onDemandIndex]
            if not self.__checkLastStopActionTime():
                return
            ugc.start(ugc.getDefaultRunCommandName())

    def startCurrentGadget(self, ugc = None):
        """
        """
        if not self.isStarted():
            return
        # Return if foreground context exists
        if self.getForegroundPguContext() != None:
            if self.getForegroundPguContext().executionIsStarted():
                return
        # Else return if background context exists
        if self.getBackgroundPguContext() != None:
            if self.getBackgroundPguContext().executionIsStarted():
                return
        # Else load current selected on demand gadget
        if len(self.__onDemandList) > 0:
            if ugc == None:
                ugc = self.__onDemandList[self.__onDemandIndex]
            if not self.__checkLastStopActionTime():
                return
            t = threading.Thread(target = ugc.start, args = (ugc.getDefaultRunCommandName(),))
            t.start()

    def stopCurrentGadget(self):
        """
        """
        if not self.isStarted():
            return
        # Abort foreground context if exists
        if self.getForegroundPguContext() != None:
            if self.getForegroundPguContext().executionIsStarted():
                if not self.__checkLastRunActionTime():
                    return
                self.getForegroundPguContext().stopExecution()
                return
        # Else abort background context if exists
        if self.getBackgroundPguContext() != None:
            if self.getBackgroundPguContext().executionIsStarted():
                # Exception for plugins commands with attribute "allUserButtons"
                if self.backgroundPguContextNeedAllUserButtons():
                    return
                if not self.__checkLastRunActionTime():
                    return
                self.getBackgroundPguContext().stopExecution()
                return

    def startStopCurrentGadget(self):
        """
        """
        # Abort foreground context if exists
        if self.getForegroundPguContext() != None:
            if self.getForegroundPguContext().executionIsStarted():
                if not self.__checkLastRunActionTime():
                    return
                self.getForegroundPguContext().stopExecution()
                return
        # Else abort background context if exists
        if self.getBackgroundPguContext() != None:
            if self.getBackgroundPguContext().executionIsStarted():
                # Exception for plugins commands with attribute "allUserButtons"
                if self.backgroundPguContextNeedAllUserButtons():
                    return
                if not self.__checkLastRunActionTime():
                    return
                self.getBackgroundPguContext().stopExecution()
                return
        # Else load current selected on demand gadget
        if len(self.__onDemandList) > 0:
            ugc = self.__onDemandList[self.__onDemandIndex]
            if not self.__checkLastStopActionTime():
                return
            ugc.start(ugc.getDefaultRunCommandName())

    def getCurrentPlayingGadgets(self):
        """
        """
        if not self.isStarted():
            return "0", "0"
        uuid1 = "0"
        fc = self.getForegroundPguContext()
        if fc != None:
            if fc.executionIsStarted():
                uuid1 = fc.getPguUuid()
        uuid2 = "0"
        bc = self.getBackgroundPguContext()
        if bc != None:
            if bc.executionIsStarted():
                uuid2 = bc.getPguUuid()
        return uuid1, uuid2

    def __contextLTPrevious(self, eventName, *args):
        """
        """
        if self.getForegroundPguContext() != None:
            return
        if self.getBackgroundPguContext() != None:
            if self.getBackgroundPguContext().executionIsStarted():
                self.__contextBtOther(eventName, *args)
                return
        self.__onDemandPrevious()

    def previousGadget(self):
        """
        """
        if not self.isStarted():
            return
        if self.getForegroundPguContext() != None:
            return
        if self.getBackgroundPguContext() != None:
            if self.getBackgroundPguContext().executionIsStarted():
                return
        self.__onDemandPrevious()

    def __contextRBNext(self, eventName, *args):
        """
        """
        if self.getForegroundPguContext() != None:
            return
        if self.getBackgroundPguContext() != None:
            if self.getBackgroundPguContext().executionIsStarted():
                self.__contextBtOther(eventName, *args)
                return
        self.__onDemandNext()

    def nextGadget(self):
        """
        """
        if not self.isStarted():
            return
        if self.getForegroundPguContext() != None:
            return
        if self.getBackgroundPguContext() != None:
            if self.getBackgroundPguContext().executionIsStarted():
                return
        self.__onDemandNext()

    def __contextBtMenu(self, eventName, *args):
        """
        """
        if not self.isStarted():
            return
        if self.getForegroundPguContext() != None:
            return
        self.__speakOnDemand(intoSentence = "current_menu_is")

    def __contextBtMute(self, eventName, *args):
        """
        """
        if self.isStarted():
            self.mute()
        else:
            self.unmute()

    def __contextBtStandby(self, eventName, *args):
        """
        """
        # Flush the foreground stack
        self.__pguContextsMutex.acquire()
        self.__pguContexts = []
        self.__pguContextsMutex.release()
        # Stop current foreground context
        if self.getForegroundPguContext() != None:
            self.getForegroundPguContext().stopExecution()
        # Stop current background context
        if self.getBackgroundPguContext() != None:
            self.getBackgroundPguContext().stopExecution()

    def __contextBtOther(self, eventName, *args):
        """
        """
        if self.getForegroundPguContext() == None:
            bgPguContext = self.getBackgroundPguContext()
            if bgPguContext != None:
                bgPguContext.getPluginInterpreterContext().sendEvent(eventName,
                    args)

    def sendEvent(self, eventName, *args):
        """
        """
        if not self.isStarted():
            if eventName == "remote":
                if args[0] == "K_MUTE":
                    self.__contextBtMute(eventName, *args)
        else:
            if eventName == "head":
                if args[0] == True:
                    self.__contextBtRunAbort(eventName, *args)
            elif eventName == "left":
                if args[0] == True:
                    self.__contextRBNext(eventName, *args)
            elif eventName == "right":
                if args[0] == True:
                    self.__contextLTPrevious(eventName, *args)
            elif eventName == "remote":
                if args[0] == "K_OK":
                    self.__contextBtRunAbort(eventName, *args)
                elif args[0] == "K_LEFT":
                    self.__contextLTPrevious(eventName, *args)
                elif args[0] == "K_UP":
                    self.__contextLTPrevious(eventName, *args)
                elif args[0] == "K_RIGHT":
                    self.__contextRBNext(eventName, *args)
                elif args[0] == "K_DOWN":
                    self.__contextRBNext(eventName, *args)
                elif args[0] == "K_MENU":
                    self.__contextBtMenu(eventName, *args)
                elif args[0] == "K_MUTE":
                    self.__contextBtMute(eventName, *args)
                elif args[0] == "K_STANDBY":
                    self.__contextBtStandby(eventName, *args)
                else:
                    self.__contextBtOther(eventName, *args)

# ==============================================================================
# ******************************************************************************
# RESOURCE DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the resource "robot_content_interactions".
# ==============================================================================
class TDSResourceRobotContentInteractions(TDSResource):
    """Resource robot_content_interactions class.
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
        # General configuration (inherited from ancestor)
        self.name = "robot_content_interactions"
        self.comment = "Resource to handling the robot/content interactions."
        self.fileName = RESOURCE_FILENAME
        self.__pguContextsManager = PguContextsManager()
        # Register callback on plugin started/stopped
        eventsHandler.getEventHandler(ST_NAME_PS_PLUGIN_STARTED).register(
            self.__onPluginStarted)
        eventsHandler.getEventHandler(ST_NAME_PS_PLUGIN_STOPPED).register(
            self.__onPluginStopped)
        # Register callback on RC and robot buttons events
        eventsHandler.getEventHandler(ST_NAME_HEAD_BUTTON).register(
            self.__onHeadBtEvent)
        eventsHandler.getEventHandler(ST_NAME_LEFT_BUTTON).register(
            self.__onLeftBtEvent)
        eventsHandler.getEventHandler(ST_NAME_RIGHT_BUTTON).register(
            self.__onRightBtEvent)
        eventsHandler.getEventHandler(ST_NAME_REMOTE_BUTTON).register(
            self.__onRCBtEvent)

    # --------------------------------------------------------------------------
    # Start the resource.
    # --------------------------------------------------------------------------
    def startMe(self):
        """Start the resource.
        Started by the resourceTuxOSL.
        """
        self.__pguContextsManager.start()

    # --------------------------------------------------------------------------
    # Stop the resource.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the resource.
        """
        self.__pguContextsManager.stop()

    def __onPluginStarted(self, *args):
        pass

    def __onPluginStopped(self, *args):
        uuid = args[0]
        # When Attitune Studio is stopped, we need to observe eventual changes
        # In the deployed attitune directories.
        if uuid == "548f7a9a-567d-773e-a0dd-102fe68a1b49":
            resourceAttituneManager.checkForUpdates()

    def __onHeadBtEvent(self, *args):
        """
        """
        self.__pguContextsManager.sendEvent("head", *args)

    def __onLeftBtEvent(self, *args):
        """
        """
        self.__pguContextsManager.sendEvent("left", *args)

    def __onRightBtEvent(self, *args):
        """
        """
        self.__pguContextsManager.sendEvent("right", *args)

    def __onRCBtEvent(self, *args):
        """
        """
        self.__pguContextsManager.sendEvent("remote", *args)

    # ==========================================================================
    # Public methods
    # ==========================================================================

    def getPguContextsManager(self):
        """
        """
        return self.__pguContextsManager

# Create an instance of the resource
resourceRobotContentInteractions = TDSResourceRobotContentInteractions(
    "resourceRobotContentInteractions")
# Register the resource into the resources manager
resourcesManager.addResource(resourceRobotContentInteractions)

# ------------------------------------------------------------------------------
# Declaration of the service "mute".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsMute(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "mute"
        self.comment = "Mute Tux Droid."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        resourceRobotContentInteractions.getPguContextsManager().mute()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsMute)

# ------------------------------------------------------------------------------
# Declaration of the service "unmute".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsUnmute(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "unmute"
        self.comment = "Unmute Tux Droid."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        resourceRobotContentInteractions.getPguContextsManager().unmute()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsUnmute)

# ------------------------------------------------------------------------------
# Declaration of the service "next_gadget".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsNextGadget(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "next_gadget"
        self.comment = "Go to next gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        t = threading.Thread(target = resourceRobotContentInteractions.getPguContextsManager().nextGadget)
        t.start()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsNextGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "previous_gadget".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsPreviousGadget(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "previous_gadget"
        self.comment = "Go to previous gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        t = threading.Thread(target = resourceRobotContentInteractions.getPguContextsManager().previousGadget)
        t.start()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsPreviousGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "start_gadget".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsStartGadget(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "start_gadget"
        self.comment = "Start the current gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        t = threading.Thread(target = resourceRobotContentInteractions.getPguContextsManager().startCurrentGadget)
        t.start()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsStartGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "start_gadget_by_uuid".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsStartGadgetByUuid(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "start_gadget_by_uuid"
        self.comment = "Start a gadget by it uuid."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        uuid = parameters['uuid']
        if resourceRobotContentInteractions.getPguContextsManager().selectOnDemandByUuid(uuid):
            ugc = None
        else:
            ugc = resourceUgcServer.getUgcContainer().getUgcByUuid(uuid)
        t = threading.Thread(target = resourceRobotContentInteractions.getPguContextsManager().startCurrentGadget,
            args = (ugc,))
        t.start()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsStartGadgetByUuid)

# ------------------------------------------------------------------------------
# Declaration of the service "stop_gadget".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsStopGadget(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "stop_gadget"
        self.comment = "Stop the current gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        t = threading.Thread(target = resourceRobotContentInteractions.getPguContextsManager().stopCurrentGadget)
        t.start()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsStopGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "start_stop_gadget".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsStartStopGadget(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "start_stop_gadget"
        self.comment = "Start or Stop the current gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        t = threading.Thread(target = resourceRobotContentInteractions.getPguContextsManager().startStopCurrentGadget)
        t.start()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsStartStopGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "get_current_playing_gadgets".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsGetCurrentPlayingGadgets(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "get_current_playing_gadgets"
        self.comment = "Get the current playing gadgets uuid."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        uuid1, uuid2 = resourceRobotContentInteractions.getPguContextsManager().getCurrentPlayingGadgets()
        contentStruct['root']['uuid1'] = uuid1
        contentStruct['root']['uuid2'] = uuid2
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsGetCurrentPlayingGadgets)

# ------------------------------------------------------------------------------
# Declaration of the service "get_gadgets_data".
# ------------------------------------------------------------------------------
class TDSServiceRobotContentInteractionsGetGadgetsData(TDSService):

    def configure(self):
        self.parametersDict = {
            'filter' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "get_gadgets_data"
        self.comment = "Get gadgets data."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        filter = parameters['filter']
        if filter == 'on_demand':
            contentStruct['root']['data'] = resourceRobotContentInteractions.getPguContextsManager().getGadgetsDictOnDemand()
        elif filter == 'all_gadgets':
            contentStruct['root']['data'] = resourceRobotContentInteractions.getPguContextsManager().getGadgetsDictAll()
        elif filter == 'alerts':
            contentStruct['root']['data'] = resourceRobotContentInteractions.getPguContextsManager().getGadgetsDictAlerts()
        else:
            pass
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        return headersStruct, contentStruct

# Register the service into the resource
resourceRobotContentInteractions.addService(TDSServiceRobotContentInteractionsGetGadgetsData)
