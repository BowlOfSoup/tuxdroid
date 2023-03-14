#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import threading

from util.filesystem.AutoDeployer import AutoDeployer
from util.xml.XmlSerializer import XmlSerializer
from util.misc import DirectoriesAndFilesTools
from util.misc import URLTools
from util.applicationserver.plugin.Plugin import SUPPORTED_LANGUAGES_LIST
from Gadget import Gadget
from GadgetGenerator import GadgetGenerator
from GadgetsOnlineContainer import GadgetsOnlineContainer

# ------------------------------------------------------------------------------
# Gadgets container class.
# ------------------------------------------------------------------------------
class GadgetsContainer(object):
    """Gadgets container class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, pluginsContainer):
        """Constructor of the class.
        @param pluginsContainer: Plugins container object.
        """
        self.__pluginsContainer = pluginsContainer
        self.__gadgets = []
        self.__mutex = threading.Lock()
        self.__autoDeployer = AutoDeployer("workForGadgets")
        self.__autoDeployer.setOnPluginDeployedCallback(self.__onGadgetDeployed)
        self.__autoDeployer.setOnPluginUndeployedCallback(self.__onGadgetUndeployed)
        self.__autoDeployer.setOnPluginDeploymentErrorCallback(self.__onGadgetDeploymentError)
        self.__onDirectoryDeployedCallback = None
        self.__onGadgetDeployedCallback = None
        self.__onGadgetDeploymentErrorCallback = None
        self.__onGadgetUndeployedCallback = None
        self.__gadgetsOnlineContainer = GadgetsOnlineContainer(self)

    # --------------------------------------------------------------------------
    # Configure the locale values of the gadgets container.
    # --------------------------------------------------------------------------
    def setLocales(self, language, country, locutor, pitch):
        """Configure the locale values of the gadgets container.
        @param language: Language.
        @param country: Country.
        @param locutor: TTS locutor.
        @param pitch: TTS pitch
        """
        self.__pluginsContainer.setLocales(language, country, locutor, pitch)

    # --------------------------------------------------------------------------
    # Get the current container language.
    # --------------------------------------------------------------------------
    def getLanguage(self):
        """Get the current container language.
        @return: A string.
        """
        return self.__pluginsContainer.getLanguage()

    # --------------------------------------------------------------------------
    # Get the current container country.
    # --------------------------------------------------------------------------
    def getCountry(self):
        """Get the current container country.
        @return: A string.
        """
        return self.__pluginsContainer.getCountry()

    # --------------------------------------------------------------------------
    # Get the current container locutor.
    # --------------------------------------------------------------------------
    def getLocutor(self):
        """Get the current container locutor.
        @return: A string.
        """
        return self.__pluginsContainer.getLocutor()

    # --------------------------------------------------------------------------
    # Get the current container pitch.
    # --------------------------------------------------------------------------
    def getPitch(self):
        """Get the current container pitch.
        @return: An integer.
        """
        return self.__pluginsContainer.getPitch()

    # --------------------------------------------------------------------------
    # Get the online gadgets container.
    # --------------------------------------------------------------------------
    def getGadgetsOnlineContainer(self):
        """Get the online gadgets container.
        @return: A GadgetsOnlineContainer object.
        """
        return self.__gadgetsOnlineContainer

    # --------------------------------------------------------------------------
    # Get the plugins container.
    # --------------------------------------------------------------------------
    def getPluginsContainer(self):
        """Get the plugins container.
        @return: A PluginsContainer object.
        """
        return self.__pluginsContainer

    # --------------------------------------------------------------------------
    # Generate a single name.
    # --------------------------------------------------------------------------
    def generateSingleName(self, gadgetName, language):
        """Generate a single name.
        @param gadgetName: Requested name.
        @return: A single name in the gadgets container.
        """
        def checkNameExists(nameToCheck):
            result = False
            for gadget in self.getGadgets():
                if gadget.getDescription().getTranslatedName(language) == nameToCheck:
                    result = True
                    break
            return result
        baseGadgetName = gadgetName
        if (baseGadgetName.find("(") > 0) and (baseGadgetName.find(")") != -1):
            baseGadgetName = baseGadgetName[:baseGadgetName.find("(") - 1]
        if baseGadgetName == "":
            baseGadgetName = "Default"
        i = 0
        while checkNameExists(gadgetName):
            i += 1
            gadgetName = "%s (%d)" % (baseGadgetName, i)
        return gadgetName

    # --------------------------------------------------------------------------
    # Export gadgets data to an external directory.
    # --------------------------------------------------------------------------
    def exportGadgets(self, destDirectory = "c:/gadgets"):
        """Export gadgets data to an external directory.
        @param destDirectory: Directory how to export the data.
        """
        baseDir = destDirectory
        if baseDir.rfind("gadgets") != 8:
            baseDir = os.path.join(baseDir, "gadgets")
        deflatedDir = os.path.join(baseDir, "deflated")
        scgDir = os.path.join(baseDir, "scg")
        gadgetXmlFile = os.path.join(baseDir, "gadgets.xml")
        # Create directories arch
        DirectoriesAndFilesTools.MKDirsF(baseDir)
        if not os.path.isdir(baseDir):
            return
        DirectoriesAndFilesTools.MKDirs(deflatedDir)
        DirectoriesAndFilesTools.MKDirs(scgDir)
        # Loop on gadgets data
        gadgetsXmlDict = {
            'gadgets' : {
                'count' : self.getCount(),
            },
        }
        for i, gadget in enumerate(self.getGadgets()):
            # Export scg file
            src = gadget.getScgFile()
            scgName = os.path.split(src)[-1]
            dest = os.path.join(scgDir, scgName)
            DirectoriesAndFilesTools.CPFile(src, dest)
            # Export deflated directory
            src = gadget.getWorkingPath()
            symbolicName = os.path.split(gadget.getWorkingPath())[-1]
            dest = os.path.join(deflatedDir, symbolicName)
            DirectoriesAndFilesTools.CPDir(src, dest)
            # Get some informations about the gadget
            gadgetData = {}
            gadgetData['symbolicName'] = symbolicName
            gadgetData['version'] = gadget.getDescription().getVersion()
            gadgetData['defaultLanguage'] = gadget.getDescription().getDefaultLanguage()
            gadgetData['category'] = gadget.getDescription().getCategory()
            gadgetData['author'] = gadget.getDescription().getAuthor()
            gadgetData['platform'] = gadget.getDescription().getPlatform()
            gadgetData['parentPluginUuid'] = gadget.getParentPlugin().getDescription().getUuid()
            gadgetData['name'] = {}
            gadgetData['description'] = {}
            gadgetData['helpFile'] = {}
            for lang in SUPPORTED_LANGUAGES_LIST:
                name = gadget.getDescription().getTranslatedName(lang)
                gadgetData['name'][lang] = name
                description = gadget.getDescription().getDescription(lang)
                gadgetData['description'][lang] = description
                helpFile = os.path.split(gadget.getDescription().getHelpFile(lang))[-1]
                gadgetData['helpFile'][lang] = helpFile
            gadgetsXmlDict['gadgets']['gadget_%.4d' % i] = gadgetData
        # Export gadgets.xml file
        gadgetsXmlFileContent = GadgetGenerator.gadgetDictToXml(gadgetsXmlDict)
        f = open(gadgetXmlFile, "w")
        f.write(gadgetsXmlFileContent)
        f.close()

    # ==========================================================================
    # AUTO-DEPLOYER
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Add a gadgets directory to deploy.
    # --------------------------------------------------------------------------
    def addDirectory(self, directory):
        """Add a gadgets directory to deploy.
        @param directory: Directory path.
        """
        self.__autoDeployer.addDirectory(directory, [".scg",])

    # --------------------------------------------------------------------------
    # Remove a gadgets directory to deploy.
    # --------------------------------------------------------------------------
    def removeDirectory(self, directory):
        """Remove a gadgets directory to deploy.
        @param directory: Directory path.
        """
        self.__autoDeployer.removeDirectory(directory)

    # --------------------------------------------------------------------------
    # Get the list of the gadgets directories.
    # --------------------------------------------------------------------------
    def getDirectories(self):
        """Get the list of the gadgets directories.
        @return: A list of string.
        """
        return self.__autoDeployer.getDirectories()

    # --------------------------------------------------------------------------
    # Deploy the setted gadgets directories.
    # --------------------------------------------------------------------------
    def deploy(self):
        """Deploy the setted gadgets directories.
        """
        self.__autoDeployer.deploy(False)

    # --------------------------------------------------------------------------
    # Undeploy the setted gadgets directories.
    # --------------------------------------------------------------------------
    def undeploy(self):
        """Undeploy the setted gadgets directories.
        """
        self.__autoDeployer.undeploy()

    # --------------------------------------------------------------------------
    # Check the gadgets directories manually.
    # --------------------------------------------------------------------------
    def check(self):
        """Check the gadgets directories manually.
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
    # Set the gadget deployed event callback.
    # --------------------------------------------------------------------------
    def setOnGadgetDeployedCallback(self, funct):
        """Set the gadget deployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onGadgetDeployed(gadget, gadgetWorkingPath):
            pass
        """
        self.__onGadgetDeployedCallback = funct

    # --------------------------------------------------------------------------
    # Set the gadget deployment error event callback.
    # --------------------------------------------------------------------------
    def setOnGadgetDeploymentErrorCallback(self, funct):
        """Set the gadget deployment error event callback.
        @param funct: Function pointer.
        Function prototype:
        def onGadgetDeploymentError(observerName, gadgetFileName, message):
            pass
        """
        self.__onGadgetDeploymentErrorCallback = funct

    # --------------------------------------------------------------------------
    # Set the gadget undeployed event callback.
    # --------------------------------------------------------------------------
    def setOnGadgetUndeployedCallback(self, funct):
        """Set the gadget undeployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onGadgetUndeployed(gadget, gadgetWorkingPath):
            pass
        """
        self.__onGadgetUndeployedCallback = funct

    # --------------------------------------------------------------------------
    # Event on gadget deployed.
    # --------------------------------------------------------------------------
    def __onGadgetDeployed(self, observerName, fileName, gadgetPath, gadgetName):
        """Event on gadget deployed.
        @param observerName: Directory observer name.
        @param fileName: Gadget file name.
        @param gadgetPath: Path of the uncompressed gadget.
        @param gadgetName: Name of the gadget.
        @return: If the gadget structure is correct or not.
        """
        gadget, msg = self.__buildGadget(observerName, fileName, gadgetPath,
            gadgetName)
        if gadget != None:
            if self.__onGadgetDeployedCallback != None:
                self.__onGadgetDeployedCallback(gadget, gadgetPath)
            if self.isDeployed():
                if self.__onDirectoryDeployedCallback != None:
                    self.__onDirectoryDeployedCallback(observerName)
            result = True
        else:
            if self.__onGadgetDeploymentErrorCallback != None:
                self.__onGadgetDeploymentErrorCallback(observerName, gadgetName,
                    msg)
            result = False
        return result

    # --------------------------------------------------------------------------
    # Event on gadget undeployed.
    # --------------------------------------------------------------------------
    def __onGadgetUndeployed(self, observerName, fileName, gadgetPath, gadgetName):
        """Event on gadget undeployed.
        @param observerName: Directory observer name.
        @param fileName: Gadget file name.
        @param gadgetPath: Path of the uncompressed gadget.
        @param gadgetName: Name of the gadget.
        """
        # Get the gadget object
        for gadget in self.__gadgets:
            if gadget.getWorkingPath() == gadgetPath:
                if self.__onGadgetUndeployedCallback != None:
                    self.__onGadgetUndeployedCallback(gadget, gadgetPath)
                # Destroy the gadget
                self.__destroyGadget(gadget)
                if self.isDeployed():
                    if self.__onDirectoryDeployedCallback != None:
                        self.__onDirectoryDeployedCallback(observerName)
                break

    # --------------------------------------------------------------------------
    # Event on gadget deployment error.
    # --------------------------------------------------------------------------
    def __onGadgetDeploymentError(self, observerName, gadgetName):
        """Event on gadget deployment error.
        @param observerName: Directory observer name.
        @param gadgetPath: Path of the uncompressed gadget.
        """
        msg = "Invalid gadget file"
        if self.__onGadgetDeploymentErrorCallback != None:
            self.__onGadgetDeploymentErrorCallback(observerName, gadgetName,
                msg)

    # ==========================================================================
    # GADGETS
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Build a gadget object from a deployed gadget.
    # --------------------------------------------------------------------------
    def __buildGadget(self, observerName, fileName, gadgetPath, gadgetName):
        """Build a gadget object from a deployed gadget.
        @param observerName: Directory observer name.
        @param fileName: Gadget file name.
        @param gadgetPath: Path of the uncompressed gadget.
        @param gadgetName: Name of the gadget.
        @return: A tuple (<gadget>, "<Message>")
        If the gadget can't be created, the "gadget" object will be None and
        the message explains the reason.
        """
        # Check for "gadget.xml"
        gadgetXmlFile = os.path.join(gadgetPath, "gadget.xml")
        gadgetXmlDict = XmlSerializer.deserializeEx(gadgetXmlFile)
        if gadgetXmlDict == None:
            return None, "'gadget.xml' not found"
        # Check for parent plugin existing and get it
        if not gadgetXmlDict.has_key('parentPlugin'):
            return None, "Error in 'gadget.xml'"
        parentPluginUuid = gadgetXmlDict['parentPlugin']['uuid']
        parentPlugin = self.__pluginsContainer.getPluginByUuid(parentPluginUuid)
        if parentPlugin == None:
            return None, "Parent plugin of this gadget is not found."
        # Check for "help.wiki"
        helpWikiFile = os.path.join(gadgetPath, "help.wiki")
        if not os.path.isfile(helpWikiFile):
            return None, "'help.wiki' not found"
        # Check for "gadget.pot"
        gadgetPotFile = os.path.join(gadgetPath, "gadget.pot")
        if not os.path.isfile(gadgetPotFile):
            return None, "'gadget.pot' not found"
        # Create the gadget
        try:
            gadget = Gadget(self, gadgetXmlDict, fileName, gadgetPath, parentPlugin)
        except:
            return None, "Error in 'gadget.xml'"
        # Check the gadget platform
        gadgetPlatform = gadget.getDescription().getPlatform()
        if gadgetPlatform != "all":
            if gadgetPlatform == "windows":
                if os.name != "nt":
                    return None, "Platform"
            else:
                if os.name == "nt":
                    return None, "Platform"
        def getSplitedGadgetVersion(theGadget):
            vList = theGadget.getDescription().getVersion().split(".")
            for i, v in enumerate(vList):
                try:
                    vList[i] = int(v)
                except:
                    vList[i] = 0
            if len(vList) < 3:
                if len(vList) < 2:
                    if len(vList) < 1:
                        vList.append(0)
                    vList.append(0)
                vList.append(0)
            return vList
        def cmpVersionGt(v1, v2):
            for i in range(3):
                if v1[i] > v2[i]:
                    return True
                elif v1[i] < v2[i]:
                    return False
            return False
        # Check for duplicated plugin uuid
        gadgetUuid = gadget.getDescription().getUuid()
        gadgetVersion = getSplitedGadgetVersion(gadget)
        for sGadget in self.__gadgets:
            if sGadget.getDescription().getUuid() == gadgetUuid:
                sGadgetVersion = getSplitedGadgetVersion(sGadget)
                # New gadget is more recent
                if cmpVersionGt(gadgetVersion, sGadgetVersion):
                    try:
                        # Remove the old gadget
                        os.remove(sGadget.getScgFile())
                        self.__destroyGadget(sGadget)
                    except:
                        pass
                # New gadget is older
                else:
                    # Can't accept this gadget ...
                    return None, "Duplicated gadget UUID (%s)" % sGadget.getDescription().getName()
        # Add this gadget to the container
        self.__mutex.acquire()
        self.__gadgets.append(gadget)
        self.__mutex.release()
        return gadget, "Ok"

    # --------------------------------------------------------------------------
    # Destroy a gadget.
    # --------------------------------------------------------------------------
    def __destroyGadget(self, gadget):
        """Destroy a gadget.
        @param gadget: Gadget object to destroy.
        """
        # Remove this gadget from the container
        self.__mutex.acquire()
        gadget.stop()
        self.__gadgets.remove(gadget)
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Destroy gadgets by parent plugin uuid.
    # --------------------------------------------------------------------------
    def destroyGadgetsByParentPluginUuid(self, parentPluginUuid):
        """Destroy gadgets by parent plugin uuid.
        @param parentPluginUuid: Parent plugin uuid.
        """
        for gadget in self.getGadgets():
            if gadget.getParentPlugin().getDescription().getUuid() == parentPluginUuid:
                self.__destroyGadget(gadget)

    # --------------------------------------------------------------------------
    # Get the gadget objects list.
    # --------------------------------------------------------------------------
    def getGadgets(self):
        """Get the gadget objects list.
        @return: A list of Gadget objects.
        """
        self.__mutex.acquire()
        result = self.__gadgets
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the number of gadgets contained in the container.
    # --------------------------------------------------------------------------
    def getCount(self):
        """Get the number of gadgets contains in the container.
        @return: An integer.
        """
        self.__mutex.acquire()
        result = len(self.__gadgets)
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get a gadget object by it name.
    # --------------------------------------------------------------------------
    def getGadgetByName(self, gadgetName):
        """Get a gadget object by it name.
        @param gadgetName: The name of the gadget.
        @return: A Gadget object or None.
        """
        self.__mutex.acquire()
        for gadget in self.__gadgets:
            if gadget.getDescription().getName() == gadgetName:
                self.__mutex.release()
                return gadget
        self.__mutex.release()
        return None

    # --------------------------------------------------------------------------
    # Get a gadget object by it uuid.
    # --------------------------------------------------------------------------
    def getGadgetByUuid(self, gadgetUuid):
        """Get a gadget object by it uuid.
        @param gadgetUuid: The uuid of the gadget.
        @return: A Gadget object or None.
        """
        self.__mutex.acquire()
        for gadget in self.__gadgets:
            if gadget.getDescription().getUuid() == gadgetUuid:
                self.__mutex.release()
                return gadget
        self.__mutex.release()
        return None

    # --------------------------------------------------------------------------
    # Get a gadget object by it name.
    # --------------------------------------------------------------------------
    def getGadget(self, gadgetName):
        """Get a gadget object by it name.
        @param gadgetName: The name of the gadget.
        @return: A Gadget object or None.
        """
        return self.getGadgetByName(gadgetName)

    # --------------------------------------------------------------------------
    # Stop all started gadgets.
    # --------------------------------------------------------------------------
    def stopAllGadgets(self):
        """Stop all started Gadgets.
        @return: The success.
        """
        self.__mutex.acquire()
        for gadget in self.__gadgets:
            gadget.stop()
        self.__mutex.release()
