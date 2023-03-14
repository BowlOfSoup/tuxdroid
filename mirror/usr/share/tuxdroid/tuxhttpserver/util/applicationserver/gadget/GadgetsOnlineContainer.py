#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import threading

from util.xml.XmlSerializer import XmlSerializer
from util.misc import DirectoriesAndFilesTools
from util.misc import URLTools
from GadgetOnline import GadgetOnline
from GadgetOnline import ONLINE_FTP_URL
from GadgetOnline import ONLINE_GADGETS_BASE_URL

# ------------------------------------------------------------------------------
# Gadgets online container class.
# ------------------------------------------------------------------------------
class GadgetsOnlineContainer(object):
    """Gadgets online container class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, gadgetsContainer):
        """Constructor of the class.
        @param gadgetsContainer: Gadgets container object.
        """
        self.__gadgetsContainer = gadgetsContainer
        self.__gadgetsOnline = []
        self.__gadgetsCount = 0
        self.__mutex = threading.Lock()

    # --------------------------------------------------------------------------
    # Update gadget structures with dictionary.
    # --------------------------------------------------------------------------
    def update(self):
        """Update gadget structures with dictionary.
        """
        self.__mutex.acquire()
        # Update only once
        if self.__gadgetsCount != 0:
            self.__mutex.release()
            return
        # Check ftp server
        if not URLTools.URLCheck(ONLINE_FTP_URL, 3.0):
            self.__mutex.release()
            return
        self.__gadgetsOnline = []
        self.__gadgetsCount = 0
        gadgetsXmlFile = os.path.join(DirectoriesAndFilesTools.GetOSTMPDir(),
            "gadgets.xml")
        # Download the xml file from the ftp
        gadgetsXmlUrl = ONLINE_GADGETS_BASE_URL + "gadgets.xml"
        if not URLTools.URLDownloadToFile(gadgetsXmlUrl, gadgetsXmlFile):
            self.__mutex.release()
            return
        # Parse the xml file
        gadgetsXmlFileContent = XmlSerializer.deserializeEx(gadgetsXmlFile)
        DirectoriesAndFilesTools.RMFile(gadgetsXmlFile)
        if gadgetsXmlFileContent == None:
            self.__mutex.release()
            return
        try:
            count = int(gadgetsXmlFileContent['count'])
            for i in range(count):
                onlineGadget = GadgetOnline(self,
                    gadgetsXmlFileContent['gadget_%.4d' % i])
                self.__gadgetsOnline.append(onlineGadget)
            self.__gadgetsCount = count
        except:
            pass
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Get the number of online gadgets.
    # --------------------------------------------------------------------------
    def getCount(self):
        """Get the number of online gadgets.
        @return: An integer.
        """
        self.__mutex.acquire()
        result = self.__gadgetsCount
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the online gadgets.
    # --------------------------------------------------------------------------
    def getOnlineGadgets(self):
        """Get the online gadgets.
        @return: A list of OnlineGadget.
        """
        self.__mutex.acquire()
        result = []
        for onlineGadget in self.__gadgetsOnline:
            result.append(onlineGadget)
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get an online gadget by it symbolic name.
    # --------------------------------------------------------------------------
    def getOnlineGadgetBySymbolicName(self, symbolicName):
        """Get an online gadget by it symbolic name.
        @param symbolicName: Symbolic name of the online gadget.
        @return: The online gadget or None.
        """
        self.__mutex.acquire()
        result = None
        for onlineGadget in self.__gadgetsOnline:
            if onlineGadget.getSymbolicName() == symbolicName:
                result = onlineGadget
                break
        self.__mutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the online gadgets data dictionary.
    # --------------------------------------------------------------------------
    def getData(self, language, category = "all_gadgets"):
        """Get the online gadgets data dictionary.
        @param language: Language.
        @param category: Gadget category as filter.
        @return: A dictionary.
        """
        def getSplitedVersion(version):
            vList = version.split(".")
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
        result = {}
        onlineGadgets = self.getOnlineGadgets()
        i = 0
        categories = []
        for onlineGadget in onlineGadgets:
            cat = onlineGadget.getCategory()
            if not cat.lower() in categories:
                categories.append(cat.lower())
            # Check the parent plugin
            parentPluginUuid = onlineGadget.getParentPluginUuid()
            if parentPluginUuid != "0":
                pluginsContainer = self.__gadgetsContainer.getPluginsContainer()
                parentPlugin = pluginsContainer.getPluginByUuid(parentPluginUuid)
                if parentPlugin == None:
                    continue
            # Check the category
            if category != "all_gadgets":
                if cat.lower() != category.lower():
                    continue
            # Check the language
            if not onlineGadget.getDefaultLanguage() in ["all", "English", language]:
                continue
            # Check the platform
            gadgetPlatform = onlineGadget.getPlatform()
            if gadgetPlatform != "all":
                if gadgetPlatform == "windows":
                    if os.name != "nt":
                        continue
                else:
                    if os.name == "nt":
                        continue
            # Check for gadget already present
            isAnUpdate = False
            abort = False
            splOnlineGadgetVersion = getSplitedVersion(onlineGadget.getVersion())
            onlineGadgetUuid = onlineGadget.getSymbolicName().replace("gadget_", "")
            for gadget in self.__gadgetsContainer.getGadgets():
                if onlineGadgetUuid == gadget.getDescription().getUuid():
                    splGadgetVersion = getSplitedVersion(gadget.getDescription().getVersion())
                    if cmpVersionGt(splOnlineGadgetVersion, splGadgetVersion):
                        isAnUpdate = True
                    else:
                        abort = True
                    break
            if abort:
                continue
            # Fill info to the result dict
            result["gadget_%d_name" % i] = onlineGadget.getName(language)
            result["gadget_%d_symbolicName" % i] = onlineGadget.getSymbolicName()
            result["gadget_%d_description" % i] = onlineGadget.getDescription(language)
            result["gadget_%d_category" % i] = onlineGadget.getCategory()
            result["gadget_%d_defaultLanguage" % i] = onlineGadget.getDefaultLanguage()
            result["gadget_%d_author" % i] = onlineGadget.getAuthor()
            result["gadget_%d_version" % i] = onlineGadget.getVersion()
            result["gadget_%d_helpFile" % i] = onlineGadget.getHelpFile(language)
            result["gadget_%d_iconFile" % i] = onlineGadget.getIconFile()
            result["gadget_%d_scgFile" % i] = onlineGadget.getScgFile()
            result["gadget_%d_isAnUpdate" % i] = isAnUpdate
            i += 1
        result['gadgets_count'] = i
        result['categories_count'] = len(categories)
        categories.sort()
        for i, category in enumerate(categories):
            result["category_%d" % i] = category
        return result
