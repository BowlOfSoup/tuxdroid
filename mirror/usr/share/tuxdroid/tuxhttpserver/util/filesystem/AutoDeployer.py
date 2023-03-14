#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is highly inspired by a module of "Karma-Lab Common Toolkits" a
#    java library written by "Yoran Brault" <http://artisan.karma-lab.net>
#

import os
import threading
from zipfile import *

from util.misc.DirectoriesAndFilesTools import *
from DirectoryContentObserver import DirectoryContentObserver

# ------------------------------------------------------------------------------
# Class to auto-deploy plugins from a directories list.
# ------------------------------------------------------------------------------
class AutoDeployer(object):
    """Class to auto-deploy plugins from a directories list.
    Supported plugins must be a zipped directory like *.tgf and *.att.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, workingDirectoryName):
        """Constructor of the class.
        """
        self.__dirMutex = threading.Lock()
        self.__deployedMutex = threading.Lock()
        self.__isDeployed = False
        self.__autoObservation = True
        self.__eventMutex = threading.Lock()
        self.__directoryObservers = []
        self.__baseWorkingDirectory = os.path.join(GetOSTMPDir(),
            workingDirectoryName)
        try:
            MKDirsF(self.__baseWorkingDirectory)
        except:
            pass
        self.__onDirectoryDeployedCallback = None
        self.__onDirectoryUndeployedCallback = None
        self.__onPluginDeployedCallback = None
        self.__onPluginDeploymentErrorCallback = None
        self.__onPluginUndeployedCallback = None

    # --------------------------------------------------------------------------
    # Deploy the plugins from the referenced directories.
    # --------------------------------------------------------------------------
    def deploy(self, automatic = True):
        """Deploy the plugins from the referenced directories.
        @param automatic: Asynchronous automatic directories observation.
        """
        if self.isDeployed():
            return
        self.__dirMutex.acquire()
        self.__autoObservation = automatic
        for directoryObserver in self.__directoryObservers:
            if self.__autoObservation:
                directoryObserver[0].start()
            else:
                directoryObserver[0].check()
            if self.__onDirectoryDeployedCallback != None:
                self.__onDirectoryDeployedCallback(directoryObserver[1])
        self.setDeployed(True)
        self.__dirMutex.release()

    # --------------------------------------------------------------------------
    # Check the observed directories manually.
    # --------------------------------------------------------------------------
    def check(self):
        """Check the observed directories manually.
        """
        if not self.isDeployed():
            return
        if self.__autoObservation:
            return
        self.__dirMutex.acquire()
        for directoryObserver in self.__directoryObservers:
            directoryObserver[0].check()
        self.__dirMutex.release()

    # --------------------------------------------------------------------------
    # Undeploy the plugins from the referenced directories.
    # --------------------------------------------------------------------------
    def undeploy(self):
        """Undeploy the plugins from the referenced directories.
        """
        if not self.isDeployed():
            return
        self.__dirMutex.acquire()
        for directoryObserver in self.__directoryObservers:
            directoryObserver[0].stop()
            if self.__onDirectoryUndeployedCallback != None:
                self.__onDirectoryUndeployedCallback(directoryObserver[1])
            RMDirs(self.__baseWorkingDirectory)
        self.setDeployed(False)
        self.__dirMutex.release()

    # --------------------------------------------------------------------------
    # Get if the auto-deployer is deployed or not.
    # --------------------------------------------------------------------------
    def isDeployed(self):
        """Get if the auto-deployer is deployed or not.
        @return: A boolean.
        """
        self.__deployedMutex.acquire()
        isDeployed = self.__isDeployed
        self.__deployedMutex.release()
        return isDeployed

    # --------------------------------------------------------------------------
    # Set if the auto-deployer is deployed or not.
    # --------------------------------------------------------------------------
    def setDeployed(self, isDeployed):
        """Set if the auto-deployer is deployed or not.
        @param isDeployed: True or False.
        """
        self.__deployedMutex.acquire()
        self.__isDeployed = isDeployed
        self.__deployedMutex.release()

    # --------------------------------------------------------------------------
    # Add a directory in the directories list to deploy.
    # --------------------------------------------------------------------------
    def addDirectory(self, directory, filters = [], name = None):
        """Add a directory in the directories list to deploy.
        @param directory: Directory path.
        @param filters: Plugin extension list.
        @param name: Directory observer name.
        @return: The success of the directory add.
        If the auto-deployment is started, the directory is directly deployed.
        """
        if not os.path.isdir(directory):
            return False
        self.__dirMutex.acquire()
        if name == None:
            dirName = directory.split(os.sep)[-1]
        else:
            dirName = name
        direNames = []
        for directoryObserver in self.__directoryObservers:
            direNames.append(directoryObserver[1])
        while dirName in direNames:
            dirName += "_"
        try:
            MKDirsF(os.path.join(self.__baseWorkingDirectory, dirName))
        except:
            pass
        directoryObserver = DirectoryContentObserver(dirName)
        directoryObserver.setDirectory(directory)
        directoryObserver.setFilters(filters)
        directoryObserver.setRate(3.0)
        directoryObserver.setOnAddedFileCallback(self.__onObserverAddedFile)
        directoryObserver.setOnRemovedFileCallback(self.__onObserverRemovedFile)
        self.__directoryObservers.append([directoryObserver, dirName])
        if self.isDeployed():
            if self.__autoObservation:
                directoryObserver.start()
            else:
                directoryObserver.check()
            if self.__onDirectoryDeployedCallback != None:
                self.__onDirectoryDeployedCallback(dirName)
        self.__dirMutex.release()
        return True

    # --------------------------------------------------------------------------
    # Remove a directory from the directories list to deploy.
    # --------------------------------------------------------------------------
    def removeDirectory(self, directory):
        """Remove a directory from the directories list to deploy.
        @param directory: Directory path.
        """
        self.__dirMutex.acquire()
        for directoryObserver in self.__directoryObservers:
            if directoryObserver[0].getDirectory() == directory:
                directoryObserver[0].stop()
                self.__directoryObservers.remove(directoryObserver)
                if self.isDeployed():
                    if self.__onDirectoryUndeployedCallback != None:
                        self.__onDirectoryUndeployedCallback(directoryObserver[1])
                break
        self.__dirMutex.release()

    # --------------------------------------------------------------------------
    # Get the list of the observed directories.
    # --------------------------------------------------------------------------
    def getDirectories(self):
        """Get the list of the observed directories.
        @return: A list of string.
        """
        result = []
        self.__dirMutex.acquire()
        for directoryObserver in self.__directoryObservers:
            result.append(directoryObserver[0].getDirectory())
        self.__dirMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the list of the directory observer objects.
    # --------------------------------------------------------------------------
    def getDirectoryContentObservers(self):
        """Get the list of the directorie observer objects.
        @return: A list of DirectoryContentObserver objects.
        """
        result = []
        self.__dirMutex.acquire()
        for directoryObserver in self.__directoryObservers:
            result.append(directoryObserver)
        self.__dirMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the directory deployed event callback.
    # --------------------------------------------------------------------------
    def setOnDirectoryDeployedCallback(self, funct):
        """Set the directory deployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onDirectoryDeployed(observerName):
            pass
        """
        self.__onDirectoryDeployedCallback = funct

    # --------------------------------------------------------------------------
    # Set the directory undeployed event callback.
    # --------------------------------------------------------------------------
    def setOnDirectoryUndeployedCallback(self, funct):
        """Set the directory undeployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onDirectoryUndeployed(observerName):
            pass
        """
        self.__onDirectoryUndeployedCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin deployed event callback.
    # --------------------------------------------------------------------------
    def setOnPluginDeployedCallback(self, funct):
        """Set the plugin deployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginDeployed(observerName, fileName, pluginPath, pluginName):
            pass
        """
        self.__onPluginDeployedCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin deployment error event callback.
    # --------------------------------------------------------------------------
    def setOnPluginDeploymentErrorCallback(self, funct):
        """Set the plugin deployment error event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginDeploymentError(observerName, pluginName):
            pass
        """
        self.__onPluginDeploymentErrorCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin undeployed event callback.
    # --------------------------------------------------------------------------
    def setOnPluginUndeployedCallback(self, funct):
        """Set the plugin undeployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginUndeployed(observerName, fileName, pluginPath, pluginName):
            pass
        """
        self.__onPluginUndeployedCallback = funct

    # --------------------------------------------------------------------------
    # Event on directory oberver : added file.
    # --------------------------------------------------------------------------
    def __onObserverAddedFile(self, observerName, fileName):
        """Event on directory oberver : added file.
        """
        self.__eventMutex.acquire()
        pluginName = fileName.split(os.sep)[-1].split(".")[0]
        pluginPath = os.path.join(self.__baseWorkingDirectory, observerName,
            pluginName)
        if not self.__uncompressPlugin(fileName, pluginPath):
            if self.__onPluginDeploymentErrorCallback != None:
                self.__onPluginDeploymentErrorCallback(observerName, pluginName)
            RMFile(fileName)
            result = False
        else:
            result = True
            if self.__onPluginDeployedCallback != None:
                result = self.__onPluginDeployedCallback(observerName, fileName,
                    pluginPath, pluginName)
                if not result:
                    RMFile(fileName)
        self.__eventMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Event on directory oberver : removed file.
    # --------------------------------------------------------------------------
    def __onObserverRemovedFile(self, observerName, fileName):
        """Event on directory oberver : removed file.
        """
        self.__eventMutex.acquire()
        pluginName = fileName.split(os.sep)[-1].split(".")[0]
        pluginPath = os.path.join(self.__baseWorkingDirectory, observerName,
            pluginName)
        if self.__onPluginUndeployedCallback != None:
            self.__onPluginUndeployedCallback(observerName, fileName,
                pluginPath, pluginName)
        RMDirs(pluginPath)
        self.__eventMutex.release()

    # --------------------------------------------------------------------------
    # Uncompress a plugin.
    # --------------------------------------------------------------------------
    def __uncompressPlugin(self, zippedFile, outputPath):
        """Uncompress a plugin.
        @param zippedFile: Zipped plugin file.
        @param outputPath: Uncompressed output directory.
        """
        try:
            zf = ZipFile(zippedFile, 'r')
        except:
            return False
        try:
            MKDirsF(outputPath)
        except:
            zf.close()
            return True
        for name in zf.namelist():
            filePath = os.path.join(outputPath, name)
            if os.sep == "/":
                filePath = filePath.replace("\\", os.sep)
            else:
                filePath = filePath.replace("/", os.sep)
            if not os.path.exists(os.path.dirname(filePath)):
                os.makedirs(os.path.dirname(filePath), 511)
            if filePath[-1] != os.sep:
                try:
                    f = open(filePath, 'wb')
                    try:
                        f.write(zf.read(name))
                    except:
                        f.close()
                        return False
                finally:
                    f.close()
        zf.close()
        return True
