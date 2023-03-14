#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is highly inspired by a "gadget framework"  written by
#    "Yoran Brault" <http://artisan.karma-lab.net>

# ------------------------------------------------------------------------------
# Plugin command class.
# ------------------------------------------------------------------------------
class PluginCommand(object):
    """Plugin command class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary):
        """Constructor of the class.
        @param parent: Parent Plugin object.
        @param dictionary: Command as dictionary.
        """
        self.__parent = parent
        self.__dictionary = dictionary
        self.__name = self.__dictionary['name']
        self.__daemon = "false"
        if self.__dictionary.has_key('daemon'):
            self.__daemon = self.__dictionary['daemon'].lower()
        self.__description = self.__dictionary['description']
        self.__exclusive = "false"
        if self.__dictionary.has_key('exclusive'):
            self.__exclusive = self.__dictionary['exclusive'].lower()
        self.__critical = "false"
        if self.__dictionary.has_key('critical'):
            self.__critical = self.__dictionary['critical'].lower()
        self.__expiration = "0"
        if self.__dictionary.has_key('expiration'):
            self.__expiration = self.__dictionary['expiration'].lower()
        self.__notifier = "false"
        if self.__dictionary.has_key('notifier'):
            self.__notifier = self.__dictionary['notifier'].lower()
        self.__allUserButtons = "false"
        if self.__dictionary.has_key('allUserButtons'):
            self.__allUserButtons = self.__dictionary['allUserButtons'].lower()

    # --------------------------------------------------------------------------
    # Get the parent plugin.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent plugin.
        @return: The parent plugin.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Get the name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the name.
        @return: A string.
        """
        return self.__name

    # --------------------------------------------------------------------------
    # Get if this plugin command work in daemon mode.
    # --------------------------------------------------------------------------
    def isDaemon(self):
        """Get if this plugin command work in daemon mode.
        @return: A boolean.
        """
        if self.__daemon == "false":
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Get if this plugin command is exclusive or not.
    # --------------------------------------------------------------------------
    def isExclusive(self):
        """Get if this plugin command is exclusive or not.
        @return: A boolean.
        """
        if self.__exclusive == "false":
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Get if this plugin command is critical or not.
    # --------------------------------------------------------------------------
    def isCritical(self):
        """Get if this plugin command is critical or not.
        @return: A boolean.
        """
        if self.__critical == "false":
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Get the expiration delay of the command.
    # --------------------------------------------------------------------------
    def getExpirationDelay(self):
        """Get the expiration delay of the command.
        @return: A boolean.
        """
        return int(self.__expiration)

    # --------------------------------------------------------------------------
    # Get if this plugin command is a daemon notifier or not.
    # --------------------------------------------------------------------------
    def isNotifier(self):
        """Get if this plugin command is a daemon notifier or not.
        @return: A boolean.
        """
        if self.__notifier == "false":
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Get if this plugin command need all user buttons or not.
    # --------------------------------------------------------------------------
    def needAllUserButtons(self):
        """Get if this plugin command need all user buttons or not.
        @return: A boolean.
        """
        if self.__allUserButtons == "false":
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Get the translated name.
    # --------------------------------------------------------------------------
    def getTranslatedName(self, language = None):
        """Get the translated name.
        @return: A string.
        """
        if language == None:
            return self.__parent.tr(self.__name)
        else:
            return self.__parent.tr2(language, self.__name)

    # --------------------------------------------------------------------------
    # Get the description.
    # --------------------------------------------------------------------------
    def getDescription(self, language = None):
        """Get the description.
        @return: A string.
        """
        if language == None:
            return self.__parent.tr(self.__description)
        else:
            return self.__parent.tr2(language, self.__description)
