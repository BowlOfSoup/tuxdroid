#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

from util.applicationserver.plugin.Plugin import SUPPORTED_LANGUAGES_LIST

# ------------------------------------------------------------------------------
# Gadget description class.
# ------------------------------------------------------------------------------
class GadgetDescription(object):
    """Gadget description.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary, workingPath):
        """Constructor of the class.
        @param parent: Parent Gadget.
        @param dictionary: Description as dictionary.
        @param workingPath: Working path of the gadget.
        """
        self.__parent = parent
        self.__dictionary = dictionary
        self.__name = None
        self.__ttsName = None
        self.__description = None
        self.__author = None
        self.__version = None
        self.__iconFile = None
        self.__uuid = None
        self.__platform = None
        self.__category = None
        self.__defaultLanguage = None
        self.__workingPath = None
        self.__onDemandIsAble = None
        self.__update(dictionary, workingPath)

    # --------------------------------------------------------------------------
    # Get the parent gadget.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent gadget.
        @return: A Gadget object.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Get the dictionary.
    # --------------------------------------------------------------------------
    def getDictionary(self):
        """Get the dictionary.
        @return: A dictionary.
        """
        return self.__dictionary

    # --------------------------------------------------------------------------
    # Update the description.
    # --------------------------------------------------------------------------
    def __update(self, dictionary, workingPath):
        """Update the description.
        """
        # Save the dictionary
        self.__dictionary = dictionary
        # Get the descriptor values
        self.__name = dictionary['name']
        self.__ttsName = self.__name
        if dictionary.has_key('ttsName'):
            self.__ttsName = dictionary['ttsName']
        self.__description = dictionary['description']
        self.__author = dictionary['author']
        self.__version = dictionary['version']
        self.__iconFile = os.path.join(workingPath, dictionary['iconFile'])
        self.__uuid = dictionary['uuid']
        self.__platform = "all"
        if dictionary.has_key('platform'):
            self.__platform = dictionary['platform'].lower()
        self.__category = dictionary['category']
        self.__defaultLanguage = dictionary['defaultLanguage']
        self.__workingPath = workingPath
        self.__onDemandIsAble = "false"
        if dictionary.has_key('onDemandIsAble'):
            self.__onDemandIsAble = dictionary['onDemandIsAble']

    # --------------------------------------------------------------------------
    # Get the gadget name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the gadget name.
        @return: A string.
        """
        return self.__name

    # --------------------------------------------------------------------------
    # Get the translated name of the gadget.
    # --------------------------------------------------------------------------
    def getTranslatedName(self, language = None):
        """Get the translated name of the gadget.
        @return: A string.
        """
        if language == None:
            return self.__parent.tr(self.__name)
        else:
            return self.__parent.tr2(language, self.__name)

    # --------------------------------------------------------------------------
    # Normalize a gadget name with the correct translation.
    # --------------------------------------------------------------------------
    def normalizeName(self, name):
        """Normalize a gadget name with the correct translation.
        @param name: Gadget name to normalize.
        @return: A string.
        """
        isTr = False
        trLang = None
        for lang in SUPPORTED_LANGUAGES_LIST:
            trName = self.getTranslatedName(lang)
            if name.find(trName) == 0:
                isTr = True
                trLang = lang
                break
        if isTr:
            tgLang = self.__parent.getContainer().getLanguage()
            if tgLang != trLang:
                tgName = self.getTranslatedName(tgLang)
                return name.replace(trName, tgName)
            else:
                return name
        else:
            return name

    # --------------------------------------------------------------------------
    # Get the TTS name of the gadget.
    # --------------------------------------------------------------------------
    def getTtsName(self, language = None):
        """Get the TTS name of the gadget.
        @return: A string.
        """
        if language == None:
            return self.__parent.tr(self.__ttsName)
        else:
            return self.__parent.tr2(language, self.__ttsName)

    # --------------------------------------------------------------------------
    # Get the translated description of the gadget.
    # --------------------------------------------------------------------------
    def getDescription(self, language = None):
        """Get the translated description of the gadget.
        @return: A string.
        """
        if language == None:
            return self.__parent.tr(self.__description)
        else:
            return self.__parent.tr2(language, self.__description)

    # --------------------------------------------------------------------------
    # Get the author of the gadget.
    # --------------------------------------------------------------------------
    def getAuthor(self):
        """Get the author of the gadget.
        @return: A string.
        """
        return self.__author

    # --------------------------------------------------------------------------
    # Get the version of the gadget.
    # --------------------------------------------------------------------------
    def getVersion(self):
        """Get the version of the gadget.
        @return: A string.
        """
        return self.__version

    # --------------------------------------------------------------------------
    # Get the icon url of the gadget.
    # --------------------------------------------------------------------------
    def getIconFile(self):
        """Get the icon url of the gadget.
        @return: A string.
        """
        return self.__iconFile

    # --------------------------------------------------------------------------
    # Get the uuid of the gadget.
    # --------------------------------------------------------------------------
    def getUuid(self):
        """Get the uuid of the gadget.
        @return: A string.
        """
        return self.__uuid

    # --------------------------------------------------------------------------
    # Get the platform of this gadget.
    # --------------------------------------------------------------------------
    def getPlatform(self):
        """Get the platform of this gadget.
        @return: A string. <"all"|"linux"|"windows">
        """
        return self.__platform

    # --------------------------------------------------------------------------
    # Get the category of the gadget.
    # --------------------------------------------------------------------------
    def getCategory(self):
        """Get the category of the gadget.
        @return: A string.
        """
        return self.__category

    # --------------------------------------------------------------------------
    # Get the default language of the gadget.
    # --------------------------------------------------------------------------
    def getDefaultLanguage(self):
        """Get the default language of the gadget.
        @return: A string.
        """
        return self.__defaultLanguage

    # --------------------------------------------------------------------------
    # Get if the gadget have on demand function or not.
    # --------------------------------------------------------------------------
    def onDemandIsAble(self):
        """Get if the gadget have on demand function or not.
        @return: A string.
        """
        return self.__onDemandIsAble

    # --------------------------------------------------------------------------
    # Get the translated help content of the gadget.
    # --------------------------------------------------------------------------
    def getHelpFile(self, language = None):
        """Get the translated help content of the gadget.
        @return: A string.
        """
        if language == None:
            return os.path.join(self.__workingPath, "help.wiki")
        else:
            helpFile = os.path.join(self.__workingPath,
                "%s.wiki" % language)
            if not os.path.isfile(helpFile):
                return os.path.join(self.__workingPath, "help.wiki")
            else:
                return helpFile
