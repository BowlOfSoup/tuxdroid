#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

ONLINE_FTP_URL = "http://tuxdroid.tounepi.com/ftp"
ONLINE_GADGETS_BASE_URL = ONLINE_FTP_URL + "/ssv3/content/gadgets/"

# ------------------------------------------------------------------------------
# Gadget online class.
# ------------------------------------------------------------------------------
class GadgetOnline(object):
    """Gadget online class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, gadgetsOnlineContainer, dictionary):
        """Constructor of the class.
        @param gadgetsOnlineContainer: Gadgets online container object.
        @param dictionary: Data dictionary.
        """
        self.__dictionary = dictionary

    # --------------------------------------------------------------------------
    # Get the author.
    # --------------------------------------------------------------------------
    def getAuthor(self):
        """Get the author.
        @return: A string.
        """
        return self.__dictionary['author']

    # --------------------------------------------------------------------------
    # Get the category.
    # --------------------------------------------------------------------------
    def getCategory(self):
        """Get the category.
        @return: A string.
        """
        return self.__dictionary['category']

    # --------------------------------------------------------------------------
    # Get the default language.
    # --------------------------------------------------------------------------
    def getDefaultLanguage(self):
        """Get the default language.
        @return: A string.
        """
        return self.__dictionary['defaultLanguage']

    # --------------------------------------------------------------------------
    # Get the symbolic name.
    # --------------------------------------------------------------------------
    def getSymbolicName(self):
        """Get the symbolic name.
        @return: A string.
        """
        return self.__dictionary['symbolicName']

    # --------------------------------------------------------------------------
    # Get the version.
    # --------------------------------------------------------------------------
    def getVersion(self):
        """Get the version.
        @return: A string.
        """
        return self.__dictionary['version']

    # --------------------------------------------------------------------------
    # Get the description.
    # --------------------------------------------------------------------------
    def getDescription(self, language):
        """Get the description.
        @param language: Language.
        @return: A string.
        """
        if self.__dictionary['description'].has_key(language):
            return self.__dictionary['description'][language]
        else:
            return self.__dictionary['description']['en']

    # --------------------------------------------------------------------------
    # Get the name.
    # --------------------------------------------------------------------------
    def getName(self, language):
        """Get the name.
        @param language: Language.
        @return: A string.
        """
        if self.__dictionary['name'].has_key(language):
            return self.__dictionary['name'][language]
        else:
            return self.__dictionary['name']['en']

    # --------------------------------------------------------------------------
    # Get the help file url.
    # --------------------------------------------------------------------------
    def getHelpFile(self, language):
        """Get the help file url.
        @param language: Language.
        @return: A string.
        """
        if self.__dictionary['helpFile'].has_key(language):
            fileName = self.__dictionary['helpFile'][language]
        else:
            fileName = self.__dictionary['helpFile']['en']
        result = "%sdeflated/%s/%s" % (ONLINE_GADGETS_BASE_URL,
            self.getSymbolicName(), fileName)
        return result

    # --------------------------------------------------------------------------
    # Get the icon url.
    # --------------------------------------------------------------------------
    def getIconFile(self):
        """Get the icon url.
        @return: A string.
        """
        result = "%sdeflated/%s/gadget.png" % (ONLINE_GADGETS_BASE_URL,
            self.getSymbolicName())
        return result

    # --------------------------------------------------------------------------
    # Get the target platform.
    # --------------------------------------------------------------------------
    def getPlatform(self):
        """Get the target platform.
        @return: <all|linux|windows>
        """
        if self.__dictionary.has_key('platform'):
            return self.__dictionary['platform']
        else:
            return "all"

    # --------------------------------------------------------------------------
    # Get the scg file.
    # --------------------------------------------------------------------------
    def getScgFile(self):
        """Get the scg file.
        @return: A string.
        """
        result = "%sscg/%s.scg" % (ONLINE_GADGETS_BASE_URL,
            self.getSymbolicName())
        return result

    # --------------------------------------------------------------------------
    # Get the parent plugin Uuid.
    # --------------------------------------------------------------------------
    def getParentPluginUuid(self):
        """Get the parent plugin Uuid.
        @return: The parent plugin Uuid.
        """
        if self.__dictionary.has_key('parentPluginUuid'):
            return self.__dictionary['parentPluginUuid']
        else:
            return "0"
