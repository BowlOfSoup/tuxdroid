#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is highly inspired by a "gadget framework"  written by
#    "Yoran Brault" <http://artisan.karma-lab.net>

import os

# ------------------------------------------------------------------------------
# Plugin description class.
# ------------------------------------------------------------------------------
class PluginDescription(object):
    """Plugin description.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary, workingPath):
        """Constructor of the class.
        @param parent: Parent Plugin.
        @param dictionary: Description as dictionary.
        @param workingPath: Working path of the plugin.
        """
        self.__parent = parent
        self.__dictionary = dictionary
        self.__name = None
        self.__uuid = None
        self.__author = None
        self.__version = None
        self.__description = None
        self.__iconFile = None
        self.__splashScreenFile = None
        self.__helpFile = None
        self.__platform = None
        self.__ttsName = None
        self.__noAttituneAlert = None
        self.__update(dictionary, workingPath)

    # --------------------------------------------------------------------------
    # Get the parent plugin.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent plugin.
        @return: A Plugin object.
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
        self.__author = dictionary['author']
        self.__version = dictionary['version']
        self.__uuid = dictionary['uuid']
        self.__iconFile = os.path.join(workingPath, dictionary['iconFile'])
        tmpFileName = os.path.join(workingPath, "resources", "splash.gif")
        if os.path.isfile(tmpFileName):
            self.__splashScreenFile = tmpFileName
        else:
            self.__splashScreenFile = None
        self.__description = dictionary['description']
        self.__workingPath = workingPath
        self.__platform = "all"
        if dictionary.has_key('platform'):
            self.__platform = dictionary['platform'].lower()
        self.__ttsName = self.__name
        if dictionary.has_key('ttsName'):
            self.__ttsName = dictionary['ttsName']
        self.__noAttituneAlert = "false"
        if dictionary.has_key('noAttituneAlert'):
            self.__noAttituneAlert = dictionary['noAttituneAlert']

    # --------------------------------------------------------------------------
    # Get the plugin name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the plugin name.
        @return: A string.
        """
        return self.__name

    # --------------------------------------------------------------------------
    # Get the translated name of the plugin.
    # --------------------------------------------------------------------------
    def getTranslatedName(self, language = None):
        """Get the translated name of the plugin.
        @return: A string.
        """
        if language == None:
            return self.__parent.tr(self.__name)
        else:
            return self.__parent.tr2(language, self.__name)

    # --------------------------------------------------------------------------
    # Get the TTS name of the plugin.
    # --------------------------------------------------------------------------
    def getTtsName(self, language = None):
        """Get the TTS name of the plugin.
        @return: A string.
        """
        if language == None:
            return self.__parent.tr(self.__ttsName)
        else:
            return self.__parent.tr2(language, self.__ttsName)

    # --------------------------------------------------------------------------
    # Get the uuid of the plugin.
    # --------------------------------------------------------------------------
    def getUuid(self):
        """Get the uuid of the plugin.
        @return: A string.
        """
        return self.__uuid

    # --------------------------------------------------------------------------
    # Get the author of the plugin.
    # --------------------------------------------------------------------------
    def getAuthor(self):
        """Get the author of the plugin.
        @return: A string.
        """
        return self.__author

    # --------------------------------------------------------------------------
    # Get the version of the plugin.
    # --------------------------------------------------------------------------
    def getVersion(self):
        """Get the version of the plugin.
        @return: A string.
        """
        return self.__version

    # --------------------------------------------------------------------------
    # Get the translated description of the plugin.
    # --------------------------------------------------------------------------
    def getDescription(self, language = None):
        """Get the translated description of the plugin.
        @return: A string.
        """
        if language == None:
            return self.__parent.tr(self.__description)
        else:
            return self.__parent.tr2(language, self.__description)

    # --------------------------------------------------------------------------
    # Get the icon url of the plugin.
    # --------------------------------------------------------------------------
    def getIconFile(self):
        """Get the icon url of the plugin.
        @return: A string.
        """
        return self.__iconFile

    # --------------------------------------------------------------------------
    # Get the splash-screen image of the plugin.
    # --------------------------------------------------------------------------
    def getSplashScreenFile(self):
        """Get the splash-screen image of the plugin.
        @return: A string.
        """
        return self.__splashScreenFile

    # --------------------------------------------------------------------------
    # Get the translated help content of the plugin.
    # --------------------------------------------------------------------------
    def getHelpFile(self, language = None):
        """Get the translated help content of the plugin.
        @return: A string.
        """
        if language == None:
            return os.path.join(self.__workingPath, "resources", "help.wiki")
        else:
            helpFile = os.path.join(self.__workingPath, "resources",
                "help_%s.wiki" % language)
            if not os.path.isfile(helpFile):
                return os.path.join(self.__workingPath, "resources",
                    "help.wiki")
            else:
                return helpFile

    # --------------------------------------------------------------------------
    # Get the platform of this plugin.
    # --------------------------------------------------------------------------
    def getPlatform(self):
        """Get the platform of this plugin.
        @return: A string. <"all"|"linux"|"windows">
        """
        return self.__platform

    # --------------------------------------------------------------------------
    # Get if the alert can have attitune introduction.
    # --------------------------------------------------------------------------
    def hasAttituneAlert(self):
        """Get if the alert can have attitune introduction.
        @return: True or False.
        """
        if self.__noAttituneAlert == "false":
            return True
        else:
            return False
