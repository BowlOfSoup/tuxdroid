#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

# ------------------------------------------------------------------------------
# UGC parameter class.
# ------------------------------------------------------------------------------
class UgcParameter(object):
    """UGC parameter class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary):
        """Constructor of the class.
        @param parent: Parent Ugc.
        @param dictionary: Parameter as dictionary.
        """
        self.__parent = parent
        self.__dictionary = dictionary
        self.__name = None
        self.__value = None
        self.__update()

    # --------------------------------------------------------------------------
    # Update the field values with the parameter dictionary.
    # --------------------------------------------------------------------------
    def __update(self):
        """Update the field values with the parameter dictionary.
        """
        self.__name = self.__dictionary['name']
        self.__value = self.__dictionary['value']

    # --------------------------------------------------------------------------
    # Get the parent Ugc.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent Ugc.
        @return: The parent Ugc.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Get the parameter data as dictionary.
    # --------------------------------------------------------------------------
    def getDictionary(self):
        """Get the parameter data as dictionary.
        @return: A dictionary.
        """
        return self.__dictionary

    # --------------------------------------------------------------------------
    # Get the name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the name.
        @return: A string.
        """
        return self.__name

    # --------------------------------------------------------------------------
    # Get the value.
    # --------------------------------------------------------------------------
    def getValue(self):
        """Get the value.
        @return: A string.
        """
        return self.__value

    # --------------------------------------------------------------------------
    # Set the value.
    # --------------------------------------------------------------------------
    def setValue(self, value):
        """Set the value.
        @param value: Value.
        """
        self.__value = value
        self.__dictionary['value'] = value
