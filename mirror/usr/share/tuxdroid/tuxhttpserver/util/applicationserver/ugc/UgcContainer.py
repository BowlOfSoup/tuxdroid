#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import time
import threading

from util.filesystem.DirectoryContentObserver import DirectoryContentObserver
from util.applicationserver.gadget.Gadget import Gadget
from util.misc.DirectoriesAndFilesTools import *
from Ugc import Ugc

# ------------------------------------------------------------------------------
# UGC container class.
# ------------------------------------------------------------------------------
class UgcContainer(object):
    """UGC container class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, gadgetsContainer):
        """Constructor of the class.
        @param gadgetsContainer: Gadgets container object.
        """
        self.__gadgetsContainer = gadgetsContainer
        self.__ugcs = []
        self.__mutex = threading.Lock()
        self.__directoryObserver = DirectoryContentObserver("workForUGC")
        self.__directoryObserver.setOnAddedFileCallback(self.__onObserverAddedFile)
        self.__directoryObserver.setOnRemovedFileCallback(self.__onObserverRemovedFile)
        self.__onUgcDeployedCallback = None
        self.__onUgcDeploymentErrorCallback = None
        self.__onUgcUndeployedCallback = None

    # --------------------------------------------------------------------------
    # Configure the locale values of the UGC container.
    # --------------------------------------------------------------------------
    def setLocales(self, language, country, locutor, pitch):
        """Configure the locale values of the UGC container.
        @param language: Language.
        @param country: Country.
        @param locutor: TTS locutor.
        @param pitch: TTS pitch
        """
        self.__gadgetsContainer.setLocales(language, country, locutor, pitch)

    # --------------------------------------------------------------------------
    # Get the current container language.
    # --------------------------------------------------------------------------
    def getLanguage(self):
        """Get the current container language.
        @return: A string.
        """
        return self.__gadgetsContainer.getLanguage()

    # --------------------------------------------------------------------------
    # Get the current container country.
    # --------------------------------------------------------------------------
    def getCountry(self):
        """Get the current container country.
        @return: A string.
        """
        return self.__gadgetsContainer.getCountry()

    # --------------------------------------------------------------------------
    # Get the current container locutor.
    # --------------------------------------------------------------------------
    def getLocutor(self):
        """Get the current container locutor.
        @return: A string.
        """
        return self.__gadgetsContainer.getLocutor()

    # --------------------------------------------------------------------------
    # Get the current container pitch.
    # --------------------------------------------------------------------------
    def getPitch(self):
        """Get the current container pitch.
        @return: An integer.
        """
        return self.__gadgetsContainer.getPitch()

    # --------------------------------------------------------------------------
    # Generate a single name.
    # --------------------------------------------------------------------------
    def generateSingleName(self, ugcName):
        """Generate a single name.
        @param ugcName: Requested name.
        @return: A single name in the UGC container.
        """
        def checkNameExists(nameToCheck):
            result = False
            for ugc in self.getUgcs():
                if ugc.getDescription().getName() == nameToCheck:
                    result = True
                    break
            return result
        baseUgcName = ugcName
        if (baseUgcName.find("(") > 0) and (baseUgcName.find(")") != -1):
            baseUgcName = baseUgcName[:baseUgcName.find("(") - 1]
        if baseUgcName == "":
            baseUgcName = "Default"
        i = 0
        while checkNameExists(ugcName):
            i += 1
            ugcName = "%s (%d)" % (baseUgcName, i)
        return ugcName

    # ==========================================================================
    # DIRECTORY OBSERVER
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Set the UGC directory to deploy.
    # --------------------------------------------------------------------------
    def setDirectory(self, directory):
        """Set the UGC directory to deploy.
        @param directory: Directory path.
        """
        self.__directoryObserver.setDirectory(directory)
        self.__directoryObserver.setFilters([".ugc",])
        self.__directoryObserver.setRate(3.0)

    # --------------------------------------------------------------------------
    # Get the UGC directory.
    # --------------------------------------------------------------------------
    def getDirectory(self):
        """Get the UGC directory.
        @return: A string.
        """
        return self.__directoryObserver.getDirectory()

    # --------------------------------------------------------------------------
    # Check the UGC directory updates.
    # --------------------------------------------------------------------------
    def check(self):
        """Check the UGC directory updates.
        """
        self.__directoryObserver.check()

    # --------------------------------------------------------------------------
    # Set the ugc deployed event callback.
    # --------------------------------------------------------------------------
    def setOnUgcDeployedCallback(self, funct):
        """Set the ugc deployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onUgcDeployed(ugc, ugcFile):
            pass
        """
        self.__onUgcDeployedCallback = funct

    # --------------------------------------------------------------------------
    # Set the ugc deployment error event callback.
    # --------------------------------------------------------------------------
    def setOnUgcDeploymentErrorCallback(self, funct):
        """Set the ugc deployment error event callback.
        @param funct: Function pointer.
        Function prototype:
        def onUgcDeploymentError(observerName, ugcFile, message):
            pass
        """
        self.__onUgcDeploymentErrorCallback = funct

    # --------------------------------------------------------------------------
    # Set the ugc undeployed event callback.
    # --------------------------------------------------------------------------
    def setOnUgcUndeployedCallback(self, funct):
        """Set the ugc undeployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onUgcUndeployed(ugc, ugcFile):
            pass
        """
        self.__onUgcUndeployedCallback = funct

    # --------------------------------------------------------------------------
    # Event on directory oberver : added file.
    # --------------------------------------------------------------------------
    def __onObserverAddedFile(self, observerName, fileName):
        """Event on directory oberver : added file.
        """
        self.__mutex.acquire()
        # Read the UGC dictionary
        ugcDataDict = None
        try:
            f = open(fileName, "r")
            try:
                ugcDataDict = eval(f.read())
            finally:
                f.close()
        except:
            pass
        if ugcDataDict == None:
            if self.__onUgcDeploymentErrorCallback != None:
                self.__onUgcDeploymentErrorCallback(observerName, fileName,
                    "Can't read the ugc file")
            self.__mutex.release()
            return False
        # Add creation time if not exists
        if not ugcDataDict.has_key("creationTime"):
            ugcDataDict["creationTime"] = time.time()
            try:
                f = open(fileName, "w")
                try:
                    f.write(str(ugcDataDict))
                finally:
                    f.close()
            except:
                pass
        # Add alert attitune if not exists
        if not ugcDataDict.has_key("alertAttitune"):
            ugcDataDict["alertAttitune"] = "----"
        # Get the parent gadget
        if not ugcDataDict.has_key('parentGadget'):
            if self.__onUgcDeploymentErrorCallback != None:
                self.__onUgcDeploymentErrorCallback(observerName, fileName,
                    "Bad ugc file format")
            RMFile(fileName)
            self.__mutex.release()
            return False
        parentGadgetUuid = ugcDataDict['parentGadget']['uuid']
        parentGadget = self.__gadgetsContainer.getGadgetByUuid(parentGadgetUuid)
        if parentGadget == None:
            if self.__onUgcDeploymentErrorCallback != None:
                self.__onUgcDeploymentErrorCallback(observerName, fileName,
                    "Parent gadget not found")
            RMFile(fileName)
            self.__mutex.release()
            return False
        # Create the Ugc
        try:
            ugc = Ugc(self, ugcDataDict, fileName, parentGadget)
        except:
            if self.__onUgcDeploymentErrorCallback != None:
                self.__onUgcDeploymentErrorCallback(observerName, fileName,
                    "Bad UGC file format 2")
            RMFile(fileName)
            self.__mutex.release()
            return False
        # Add the Ugc in the container
        self.__ugcs.append(ugc)
        # Sort the ugc list by creation time
        unSortedList = []
        for ugcObj in self.__ugcs:
            unSortedList.append(ugcObj)
        self.__ugcs = []
        while len(unSortedList) > 0:
            older = 99999999999.0
            match = None
            for ugcObj in unSortedList:
                if ugcObj.getUgcFileCreationTime() < older:
                    match = ugcObj
                    older = ugcObj.getUgcFileCreationTime()
            unSortedList.remove(match)
            self.__ugcs.append(match)
        self.__mutex.release()
        if self.__onUgcDeployedCallback != None:
            self.__onUgcDeployedCallback(ugc, fileName)
        time.sleep(0.015)
        return True

    # --------------------------------------------------------------------------
    # Event on directory oberver : removed file.
    # --------------------------------------------------------------------------
    def __onObserverRemovedFile(self, observerName, fileName):
        """Event on directory oberver : removed file.
        """
        self.__mutex.acquire()
        # Get the ugc object
        for ugc in self.__ugcs:
            if ugc.getUgcFile() == fileName:
                self.__ugcs.remove(ugc)
                if self.__onUgcUndeployedCallback != None:
                    self.__onUgcUndeployedCallback(ugc, fileName)
                break
        self.__mutex.release()

    # ==========================================================================
    # UGC
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Destroy an UGC.
    # --------------------------------------------------------------------------
    def __destroyUgc(self, ugc):
        """Destroy an UGC.
        @param ugc: Ugc object to destroy.
        """
        # Remove this ugc from the container
        self.__mutex.acquire()
        ugc.stop()
        self.__ugcs.remove(ugc)
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Destroy ugc objects by parent gadget uuid.
    # --------------------------------------------------------------------------
    def destroyUgcByParentGadgetUuid(self, parentGadgetUuid):
        """Destroy ugc objects by parent gadget uuid.
        @param parentGadgetUuid: Parent gadget uuid.
        """
        for ugc in self.getUgcs():
            if ugc.getParentGadget().getDescription().getUuid() == parentGadgetUuid:
                self.__destroyUgc(ugc)

    # --------------------------------------------------------------------------
    # Update the parent gadget of ugc children.
    # --------------------------------------------------------------------------
    def updateParentGadgets(self):
        """Update the parent gadget of ugc children.
        """
        for parentGadget in self.__gadgetsContainer.getGadgets():
            parentGadgetUuid = parentGadget.getDescription().getUuid()
            for ugc in self.getUgcs():
                if ugc.getParentGadget().getDescription().getUuid() == parentGadgetUuid:
                    ugc.setParentGadget(parentGadget)

    # --------------------------------------------------------------------------
    # Get the ugc objects list.
    # --------------------------------------------------------------------------
    def getUgcs(self):
        """Get the ugc objects list.
        @return: A list of Ugc objects.
        """
        self.__mutex.acquire()
        result = self.__ugcs
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the number of ugc objects contained in the container.
    # --------------------------------------------------------------------------
    def getCount(self):
        """Get the number of ugc objects contained in the container.
        @return: An integer.
        """
        self.__mutex.acquire()
        result = len(self.__ugcs)
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get an ugc object by it name.
    # --------------------------------------------------------------------------
    def getUgcByName(self, ugcName):
        """Get an ugc object by it name.
        @param ugcName: The name of the ugc.
        @return: An Ugc object or None.
        """
        self.__mutex.acquire()
        for ugc in self.__ugcs:
            if ugc.getDescription().getName() == ugcName:
                self.__mutex.release()
                return ugc
        self.__mutex.release()
        return None

    # --------------------------------------------------------------------------
    # Get an ugc object by it uuid.
    # --------------------------------------------------------------------------
    def getUgcByUuid(self, ugcUuid):
        """Get an ugc object by it uuid.
        @param ugcUuid: The uuid of the ugc.
        @return: An Ugc object or None.
        """
        self.__mutex.acquire()
        for ugc in self.__ugcs:
            if ugc.getDescription().getUuid() == ugcUuid:
                self.__mutex.release()
                return ugc
        self.__mutex.release()
        return None

    # --------------------------------------------------------------------------
    # Get an ugc object by it name.
    # --------------------------------------------------------------------------
    def getGadget(self, ugcName):
        """Get an ugc object by it name.
        @param ugcName: The name of the ugc.
        @return: An Ugc object or None.
        """
        return self.getUgcByName(ugcName)

    # --------------------------------------------------------------------------
    # Stop all started ugc objects.
    # --------------------------------------------------------------------------
    def stopAllUgcs(self):
        """Stop all started ugc objects.
        @return: The success.
        """
        self.__mutex.acquire()
        for ugc in self.__ugcs:
            ugc.stop()
        self.__mutex.release()
