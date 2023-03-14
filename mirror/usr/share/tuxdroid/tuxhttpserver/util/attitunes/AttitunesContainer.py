#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import threading

from util.filesystem.AutoDeployer import AutoDeployer
from util.misc.XMLSerializer import fromXML
from Attitune import Attitune

# ------------------------------------------------------------------------------
# Attitunes container class.
# ------------------------------------------------------------------------------
class AttitunesContainer(object):
    """Attitunes container class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        self.__attitunes = []
        self.__mutex = threading.Lock()
        self.__autoDeployer = AutoDeployer("workForAttitunes")
        self.__autoDeployer.setOnPluginDeployedCallback(self.__onPluginDeployed)
        self.__autoDeployer.setOnPluginUndeployedCallback(self.__onPluginUndeployed)
        self.__autoDeployer.setOnPluginDeploymentErrorCallback(self.__onPluginDeploymentError)
        self.__onDirectoryDeployedCallback = None
        self.__onAttituneDeployedCallback = None
        self.__onAttituneDeploymentErrorCallback = None
        self.__onAttituneUndeployedCallback = None

    # ==========================================================================
    # AUTO-DEPLOYER
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Add an attitunes directory to deploy.
    # --------------------------------------------------------------------------
    def addDirectory(self, directory, name = None):
        """Add an attitunes directory to deploy.
        @param directory: Directory path.
        @param name: Name of the directory observer.
        """
        self.__autoDeployer.addDirectory(directory, [".att",], name)

    # --------------------------------------------------------------------------
    # Remove an attitunes directory to deploy.
    # --------------------------------------------------------------------------
    def removeDirectory(self, directory):
        """Remove an attitunes directory to deploy.
        @param directory: Directory path.
        """
        self.__autoDeployer.removeDirectory(directory)

    # --------------------------------------------------------------------------
    # Get the list of the attitunes directories.
    # --------------------------------------------------------------------------
    def getDirectories(self):
        """Get the list of the attitunes directories.
        @return: A list of string.
        """
        return self.__autoDeployer.getDirectories()

    # --------------------------------------------------------------------------
    # Deploy the setted attitunes directories.
    # --------------------------------------------------------------------------
    def deploy(self):
        """Deploy the setted attitunes directories.
        """
        self.__autoDeployer.deploy(False)

    # --------------------------------------------------------------------------
    # Undeploy the setted attitunes directories.
    # --------------------------------------------------------------------------
    def undeploy(self):
        """Undeploy the setted attitunes directories.
        """
        self.__autoDeployer.undeploy()

    # --------------------------------------------------------------------------
    # Check the attitunes directories manually.
    # --------------------------------------------------------------------------
    def check(self):
        """Check the attitunes directories manually.
        """
        self.__autoDeployer.check()

    # --------------------------------------------------------------------------
    # Get if the container is deployed or not.
    # --------------------------------------------------------------------------
    def isDeployed(self):
        """Get if the container is deployed or not.
        @return: A boolean.
        """
        return self.__autoDeployer.isDeployed()

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
        self.__autoDeployer.setOnDirectoryDeployedCallback(funct)

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
        self.__autoDeployer.setOnDirectoryUndeployedCallback(funct)

    # --------------------------------------------------------------------------
    # Set the attitune deployed event callback.
    # --------------------------------------------------------------------------
    def setOnAttituneDeployedCallback(self, funct):
        """Set the attitune deployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onAttituneDeployed(attitune, attituneWorkingPath):
            pass
        """
        self.__onAttituneDeployedCallback = funct

    # --------------------------------------------------------------------------
    # Set the attitune deployment error event callback.
    # --------------------------------------------------------------------------
    def setOnAttituneDeploymentErrorCallback(self, funct):
        """Set the attitune deployment error event callback.
        @param funct: Function pointer.
        Function prototype:
        def onAttituneDeploymentError(observerName, attituneFileName, message):
            pass
        """
        self.__onAttituneDeploymentErrorCallback = funct

    # --------------------------------------------------------------------------
    # Set the attitune undeployed event callback.
    # --------------------------------------------------------------------------
    def setOnAttituneUndeployedCallback(self, funct):
        """Set the attitune undeployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onAttituneUndeployed(attitune, attituneWorkingPath):
            pass
        """
        self.__onAttituneUndeployedCallback = funct

    # --------------------------------------------------------------------------
    # Event on plugin deployed.
    # --------------------------------------------------------------------------
    def __onPluginDeployed(self, observerName, fileName, pluginPath, pluginName):
        """Event on plugin deployed.
        @param observerName: Directory observer name.
        @param fileName: Plugin file name.
        @param pluginPath: Path of the uncompressed plugin.
        @param pluginName: Name of the plugin.
        @return: If the plugin structure is correct or not.
        """
        attitune, msg = self.__buildAttitune(observerName, fileName, pluginPath,
            pluginName)
        if attitune != None:
            if self.__onAttituneDeployedCallback != None:
                self.__onAttituneDeployedCallback(attitune,
                    attitune.getWorkingPath())
            if self.isDeployed():
                if self.__onDirectoryDeployedCallback != None:
                    self.__onDirectoryDeployedCallback(observerName)
            result = True
        else:
            if self.__onAttituneDeploymentErrorCallback != None:
                self.__onAttituneDeploymentErrorCallback(observerName,
                    pluginName, msg)
            result = False
        return result

    # --------------------------------------------------------------------------
    # Event on plugin undeployed.
    # --------------------------------------------------------------------------
    def __onPluginUndeployed(self, observerName, fileName, pluginPath, pluginName):
        """Event on plugin undeployed.
        @param observerName: Directory observer name.
        @param fileName: Plugin file name.
        @param pluginPath: Path of the uncompressed plugin.
        @param pluginName: Name of the plugin.
        """
        # Get the attitune object
        for attitune in self.__attitunes:
            if attitune.getWorkingPath() == os.path.join(pluginPath, pluginName):
                if self.__onAttituneUndeployedCallback != None:
                    self.__onAttituneUndeployedCallback(attitune,
                        attitune.getWorkingPath())
                # Destroy the attitune
                self.__destroyAttitune(attitune)
                if self.isDeployed():
                    if self.__onDirectoryDeployedCallback != None:
                        self.__onDirectoryDeployedCallback(observerName)
                break

    # --------------------------------------------------------------------------
    # Event on plugin deployment error.
    # --------------------------------------------------------------------------
    def __onPluginDeploymentError(self, observerName, pluginName):
        """Event on plugin deployment error.
        @param observerName: Directory observer name.
        @param pluginPath: Path of the uncompressed plugin.
        """
        msg = "Invalid attitune file"
        if self.__onAttituneDeploymentErrorCallback != None:
            self.__onAttituneDeploymentErrorCallback(observerName, pluginName,
                msg)

    # ==========================================================================
    # ATTITUNES
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Generate a single name.
    # --------------------------------------------------------------------------
    def generateSingleName(self, attName):
        """Generate a single name.
        @param attName: Requested name.
        @return: A single name in the attitunes container.
        """
        def checkNameExists(nameToCheck):
            result = False
            for attitune in self.getAttitunes():
                if attitune.getDescription().getName() == nameToCheck:
                    result = True
                    break
            return result
        baseAttName = attName
        if (baseAttName.find("(") > 0) and (baseAttName.find(")") != -1):
            baseAttName = baseAttName[:baseAttName.find("(") - 1]
        if baseAttName == "":
            baseAttName = "Default"
        i = 0
        while checkNameExists(attName):
            i += 1
            attName = "%s (%d)" % (baseAttName, i)
        return attName

    # --------------------------------------------------------------------------
    # Build an attitune object from a deployed plugin.
    # --------------------------------------------------------------------------
    def __buildAttitune(self, observerName, fileName, pluginPath, pluginName):
        """Build an attitune object from a deployed plugin.
        @param observerName: Directory observer name.
        @param fileName: Plugin file name.
        @param pluginPath: Path of the uncompressed plugin.
        @param pluginName: Name of the plugin.
        @return: A tuple (<attitune>, "<Message>")
        If the attitune can't be created, the "attitune" object will be None and
        the message explains the reason.
        """
        # Check for "scene.xml"
        sceneXmlFile = os.path.join(pluginPath, pluginName, "scene.xml")
        sceneXmlDict = fromXML(sceneXmlFile)
        sceneXmlDict['scene']['header']['name'] = self.generateSingleName(
            sceneXmlDict['scene']['header']['name'])
        if sceneXmlDict == None:
            return None, "'scene.xml' not found"
        # Create the attitune
        try:
            attitune = Attitune(self, sceneXmlDict, fileName,
                os.path.join(pluginPath, pluginName), observerName)
        except:
            return None, "Error in 'scene.xml'"
        # Add this attitune to the container
        self.__mutex.acquire()
        self.__attitunes.append(attitune)
        self.__mutex.release()
        return attitune, "Ok"

    # --------------------------------------------------------------------------
    # Destroy an attitune.
    # --------------------------------------------------------------------------
    def __destroyAttitune(self, attitune):
        """Destroy an attitune.
        @param attitune: Attitune object to destroy.
        """
        # Remove this attitune from the container
        self.__mutex.acquire()
        self.__attitunes.remove(attitune)
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Get the attitunes objects list.
    # --------------------------------------------------------------------------
    def getAttitunes(self):
        """Get the attitune objects list.
        @return: A list of Attitune objects.
        """
        self.__mutex.acquire()
        result = self.__attitunes
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the number of attitunes contains in the container.
    # --------------------------------------------------------------------------
    def getCount(self):
        """Get the number of attitunes contains in the container.
        @return: An integer.
        """
        self.__mutex.acquire()
        result = len(self.__attitunes)
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get an attitune object by it name.
    # --------------------------------------------------------------------------
    def getAttitune(self, attituneName):
        """Get an attitune object by it name.
        @param gadgetName: The name of the attitune.
        @return: An attitune object or None.
        """
        self.__mutex.acquire()
        for attitune in self.__attitunes:
            if attitune.getDescription().getName() == attituneName:
                self.__mutex.release()
                return attitune
        self.__mutex.release()
        return None
