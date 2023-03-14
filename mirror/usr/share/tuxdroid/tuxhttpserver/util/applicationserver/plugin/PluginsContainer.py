#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is highly inspired by a "gadget framework"  written by
#    "Yoran Brault" <http://artisan.karma-lab.net>

import sys
import os
import threading
import traceback

from util.filesystem.AutoDeployer import AutoDeployer
from util.xml.XmlSerializer import XmlSerializer
from Plugin import Plugin

# ------------------------------------------------------------------------------
# Plugins container class.
# ------------------------------------------------------------------------------
class PluginsContainer(object):
    """Plugins container class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        self.__language = "en"
        self.__country = "US"
        self.__locutor = "Ryan"
        self.__pitch = 130
        self.__plugins = []
        self.__mutex = threading.Lock()
        self.__autoDeployer = AutoDeployer("workForPlugins")
        self.__autoDeployer.setOnPluginDeployedCallback(self.__onPluginDeployed)
        self.__autoDeployer.setOnPluginUndeployedCallback(self.__onPluginUndeployed)
        self.__autoDeployer.setOnPluginDeploymentErrorCallback(self.__onPluginDeploymentError)
        self.__onDirectoryDeployedCallback = None
        self.__onPluginDeployedCallback = None
        self.__onPluginDeploymentErrorCallback = None
        self.__onPluginUndeployedCallback = None
        self.__locutors = []

    # --------------------------------------------------------------------------
    # Configure the locale values of the plugins container.
    # --------------------------------------------------------------------------
    def setLocales(self, language, country, locutor, pitch):
        """Configure the locale values of the plugins container.
        @param language: Language.
        @param country: Country.
        @param locutor: TTS locutor.
        @param pitch: TTS pitch
        """
        self.__language = language
        self.__country = country
        self.__locutor = locutor
        self.__pitch = pitch

    # --------------------------------------------------------------------------
    # Get the current container language.
    # --------------------------------------------------------------------------
    def getLanguage(self):
        """Get the current container language.
        @return: A string.
        """
        self.__mutex.acquire()
        result = self.__language
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the current container country.
    # --------------------------------------------------------------------------
    def getCountry(self):
        """Get the current container country.
        @return: A string.
        """
        self.__mutex.acquire()
        result = self.__country
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the current container locutor.
    # --------------------------------------------------------------------------
    def getLocutor(self):
        """Get the current container locutor.
        @return: A string.
        """
        self.__mutex.acquire()
        result = self.__locutor
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the current container pitch.
    # --------------------------------------------------------------------------
    def getPitch(self):
        """Get the current container pitch.
        @return: An integer.
        """
        self.__mutex.acquire()
        result = self.__pitch
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the available locutors list.
    # --------------------------------------------------------------------------
    def setLocutorsList(self, locutors):
        """Set the available locutors list.
        @param locutors: Locutors list.
        """
        self.__mutex.acquire()
        self.__locutors = []
        for locutor in locutors:
            self.__locutors.append(locutor.replace("8k", ""))
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Get the available locutors list.
    # --------------------------------------------------------------------------
    def getLocutorsList(self):
        """Get the available locutors list.
        @return: A list of strings.
        """
        self.__mutex.acquire()
        result = self.__locutors
        self.__mutex.release()
        return result

    # ==========================================================================
    # AUTO-DEPLOYER
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Add a plugins directory to deploy.
    # --------------------------------------------------------------------------
    def addDirectory(self, directory):
        """Add a plugins directory to deploy.
        @param directory: Directory path.
        """
        self.__autoDeployer.addDirectory(directory, [".scp",])

    # --------------------------------------------------------------------------
    # Remove a plugins directory to deploy.
    # --------------------------------------------------------------------------
    def removeDirectory(self, directory):
        """Remove a plugins directory to deploy.
        @param directory: Directory path.
        """
        self.__autoDeployer.removeDirectory(directory)

    # --------------------------------------------------------------------------
    # Get the list of the plugins directories.
    # --------------------------------------------------------------------------
    def getDirectories(self):
        """Get the list of the plugins directories.
        @return: A list of string.
        """
        return self.__autoDeployer.getDirectories()

    # --------------------------------------------------------------------------
    # Deploy the setted Plugins directories.
    # --------------------------------------------------------------------------
    def deploy(self):
        """Deploy the setted plugins directories.
        """
        self.__autoDeployer.deploy(False)

    # --------------------------------------------------------------------------
    # Undeploy the setted plugins directories.
    # --------------------------------------------------------------------------
    def undeploy(self):
        """Undeploy the setted plugins directories.
        """
        self.__autoDeployer.undeploy()

    # --------------------------------------------------------------------------
    # Check the plugins directories manually.
    # --------------------------------------------------------------------------
    def check(self):
        """Check the plugins directories manually.
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
    # Set the plugin deployed event callback.
    # --------------------------------------------------------------------------
    def setOnPluginDeployedCallback(self, funct):
        """Set the plugin deployed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginDeployed(plugin, pluginWorkingPath):
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
        def onPluginDeploymentError(observerName, pluginFileName, message):
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
        def onPluginUndeployed(plugin, pluginWorkingPath):
            pass
        """
        self.__onPluginUndeployedCallback = funct

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
        plugin, msg = self.__buildPlugin(observerName, fileName, pluginPath,
            pluginName)
        if plugin != None:
            if self.__onPluginDeployedCallback != None:
                self.__onPluginDeployedCallback(plugin, pluginPath)
            if self.isDeployed():
                if self.__onDirectoryDeployedCallback != None:
                    self.__onDirectoryDeployedCallback(observerName)
            result = True
        else:
            if self.__onPluginDeploymentErrorCallback != None:
                self.__onPluginDeploymentErrorCallback(observerName, pluginName,
                    msg)
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
        # Get the plugin object
        for plugin in self.__plugins:
            if plugin.getWorkingPath() == pluginPath:
                if self.__onPluginUndeployedCallback != None:
                    self.__onPluginUndeployedCallback(plugin, pluginPath)
                # Destroy the plugin
                self.__destroyPlugin(plugin)
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
        msg = "Invalid plugin file"
        if self.__onPluginDeploymentErrorCallback != None:
            self.__onPluginDeploymentErrorCallback(observerName, pluginName,
                msg)

    # ==========================================================================
    # PLUGINS
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Get if the plugins platform must be checked or not.
    # --------------------------------------------------------------------------
    def __mustCheckPlatform(self):
        """Get if the plugins platform must be checked or not.
        @return: A boolean.
        """
        if os.environ.has_key("TDS_PLUGIN_PLATFORM_ALL"):
            if os.environ["TDS_PLUGIN_PLATFORM_ALL"] == "True":
                return False
        return True

    # --------------------------------------------------------------------------
    # Format the last traceback.
    # --------------------------------------------------------------------------
    def __formatException(self):
        """Format the last traceback.
        @return: A string.
        """
        fList = traceback.format_exception(sys.exc_info()[0],
                    sys.exc_info()[1],
                    sys.exc_info()[2])
        result = ""
        for line in fList:
            result += line
        return result

    # --------------------------------------------------------------------------
    # Build a plugin object from a deployed plugin.
    # --------------------------------------------------------------------------
    def __buildPlugin(self, observerName, fileName, pluginPath, pluginName):
        """Build a plugin object from a deployed plugin.
        @param observerName: Directory observer name.
        @param fileName: Plugin file name.
        @param pluginPath: Path of the uncompressed plugin.
        @param pluginName: Name of the plugin.
        @return: A tuple (<plugin>, "<Message>")
        If the plugin can't be created, the "plugin" object will be None and
        the message explains the reason.
        """
        # Check for "plugin.xml"
        pluginXmlFile = os.path.join(pluginPath, "resources", "plugin.xml")
        if not os.path.isfile(pluginXmlFile):
            return None, "'plugin.xml' not found"
        pluginXmlDict = XmlSerializer.deserializeEx(pluginXmlFile)
        if pluginXmlDict == None:
            error = "'plugin.xml' XML format error\n" + XmlSerializer.getLastTraceback()
            return None, error
        # Check for "help.wiki"
        helpWikiFile = os.path.join(pluginPath, "resources", "help.wiki")
        if not os.path.isfile(helpWikiFile):
            return None, "'help.wiki' not found"
        # Check for "plugin.pot"
        pluginPotFile = os.path.join(pluginPath, "resources", "plugin.pot")
        if not os.path.isfile(pluginPotFile):
            return None, "'plugin.pot' not found"
        # Create the plugin
        try:
            plugin = Plugin(self, pluginXmlDict, fileName, pluginPath)
        except:
            error = "Error in 'plugin.xml'\n" + self.__formatException()
            return None, error
        # Check the plugin platform
        if self.__mustCheckPlatform():
            pluginPlatform = plugin.getDescription().getPlatform()
            if pluginPlatform != "all":
                if pluginPlatform == "windows":
                    if os.name != "nt":
                        return None, "Platform"
                else:
                    if os.name == "nt":
                        return None, "Platform"
        def getSplitedPluginVersion(thePlugin):
            vList = thePlugin.getDescription().getVersion().split(".")
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
        pluginUuid = plugin.getDescription().getUuid()
        pluginVersion = getSplitedPluginVersion(plugin)
        for sPlugin in self.__plugins:
            if sPlugin.getDescription().getUuid() == pluginUuid:
                sPluginVersion = getSplitedPluginVersion(sPlugin)
                # New plugin is more recent
                if cmpVersionGt(pluginVersion, sPluginVersion):
                    try:
                        # Remove the old plugin
                        os.remove(sPlugin.getScpFile())
                    except:
                        pass
                # New plugin is older
                else:
                    # Can't accept this plugin ...
                    return None, "Duplicated plugin UUID (%s)" % sPlugin.getDescription().getName()
        # Add this plugin to the container
        self.__mutex.acquire()
        self.__plugins.append(plugin)
        self.__mutex.release()
        return plugin, "Ok"

    # --------------------------------------------------------------------------
    # Destroy a plugin.
    # --------------------------------------------------------------------------
    def __destroyPlugin(self, plugin):
        """Destroy a plugin.
        @param plugin: PLugin object to destroy.
        """
        # Remove this plugin from the container
        self.__mutex.acquire()
        plugin.stop()
        self.__plugins.remove(plugin)
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Get the plugin objects list.
    # --------------------------------------------------------------------------
    def getPlugins(self):
        """Get the plugin objects list.
        @return: A list of Plugins objects.
        """
        self.__mutex.acquire()
        result = self.__plugins
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the number of plugins contained in the container.
    # --------------------------------------------------------------------------
    def getCount(self):
        """Get the number of plugins contains in the container.
        @return: An integer.
        """
        self.__mutex.acquire()
        result = len(self.__plugins)
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get a plugin object by it name.
    # --------------------------------------------------------------------------
    def getPluginByName(self, pluginName):
        """Get a plugin object by it name.
        @param pluginName: The name of the plugin.
        @return: A Plugin object or None.
        """
        self.__mutex.acquire()
        for plugin in self.__plugins:
            if plugin.getDescription().getName() == pluginName:
                self.__mutex.release()
                return plugin
        self.__mutex.release()
        return None

    # --------------------------------------------------------------------------
    # Get a plugin object by it uuid.
    # --------------------------------------------------------------------------
    def getPluginByUuid(self, pluginUuid):
        """Get a plugin object by it uuid.
        @param pluginName: The uuid of the plugin.
        @return: A Plugin object or None.
        """
        self.__mutex.acquire()
        for plugin in self.__plugins:
            if plugin.getDescription().getUuid() == pluginUuid:
                self.__mutex.release()
                return plugin
        self.__mutex.release()
        return None

    # --------------------------------------------------------------------------
    # Get a plugin object by it name.
    # --------------------------------------------------------------------------
    def getPlugin(self, pluginName):
        """Get a plugin object by it name.
        @param pluginName: The name of the plugin.
        @return: A Plugin object or None.
        """
        return self.getPluginByName(pluginName)

    # --------------------------------------------------------------------------
    # Stop all started plugins.
    # --------------------------------------------------------------------------
    def stopAllPlugins(self):
        """Stop all started plugins.
        @return: The success.
        """
        self.__mutex.acquire()
        for plugin in self.__plugins:
            plugin.stop()
        self.__mutex.release()
