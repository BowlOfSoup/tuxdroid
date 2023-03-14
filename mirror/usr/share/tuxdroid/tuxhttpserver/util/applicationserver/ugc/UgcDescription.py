#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

# ------------------------------------------------------------------------------
# UGC description class.
# ------------------------------------------------------------------------------
class UgcDescription(object):
    """UGC description class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary):
        """Constructor of the class.
        @param parent: Parent UGC.
        @param dictionary: Description as dictionary.
        """
        self.__parent = parent
        self.__dictionary = dictionary
        self.__name = None
        self.__ttsName = None
        self.__uuid = None
        self.__onDemandIsActivated = None
        self.__update(dictionary)

    # --------------------------------------------------------------------------
    # Get the parent UGC.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent UGC.
        @return: A Ugc object.
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
    def __update(self, dictionary):
        """Update the description.
        """
        # Save the dictionary
        self.__dictionary = dictionary
        # Get the descriptor values
        self.__name = dictionary['name']
        self.__name = self.__parent.getParentGadget().getDescription().normalizeName(self.__name)
        self.__ttsName = self.__name
        if dictionary.has_key('ttsName'):
            self.__ttsName = dictionary['ttsName']
        self.__uuid = dictionary['uuid']
        self.__onDemandIsActivated = "false"
        if dictionary.has_key('onDemandIsActivated'):
            self.__onDemandIsActivated = dictionary['onDemandIsActivated']

    # --------------------------------------------------------------------------
    # Get the name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the name.
        @return: A string.
        """
        return self.__name

    # --------------------------------------------------------------------------
    # Set the name.
    # --------------------------------------------------------------------------
    def setName(self, name):
        """Set the name.
        @param name: A string.
        """
        self.__name = name
        self.__dictionary['name'] = self.__name

    # --------------------------------------------------------------------------
    # Get the TTS name.
    # --------------------------------------------------------------------------
    def getTtsName(self, language = None):
        """Get the TTS name.
        @return: A string.
        """
        return self.__ttsName

    # --------------------------------------------------------------------------
    # Set the TTS name.
    # --------------------------------------------------------------------------
    def setTtsName(self, ttsName):
        """Set the TTS name.
        @param ttsName: A string.
        """
        self.__ttsName = ttsName
        self.__dictionary['ttsName'] = self.__ttsName

    # --------------------------------------------------------------------------
    # Get the uuid.
    # --------------------------------------------------------------------------
    def getUuid(self):
        """Get the uuid.
        @return: A string.
        """
        return self.__uuid

    # --------------------------------------------------------------------------
    # Get if the UGC is on demand or not.
    # --------------------------------------------------------------------------
    def onDemandIsActivated(self):
        """Get if the UGC is on demand or not.
        @return: A string.
        """
        return self.__onDemandIsActivated

    # --------------------------------------------------------------------------
    # Set if the UGC is on demand or not.
    # --------------------------------------------------------------------------
    def setOnDemandIsActivated(self, onDemandIsActivated):
        """Set if the UGC is on demand or not.
        @param onDemandIsActivated: A string.
        """
        self.__onDemandIsActivated = onDemandIsActivated
        self.__dictionary['onDemandIsActivated'] = self.__onDemandIsActivated
