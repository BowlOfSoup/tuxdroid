#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

# ------------------------------------------------------------------------------
# Attitune description.
# ------------------------------------------------------------------------------
class AttituneDescription(object):
    """Attitune description.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary, workingPath):
        """Constructor of the class.
        @param parent: Parent Attitune.
        @param dictionary: Description as dictionary.
        @param workingPath: Working path of the attitune.
        """
        self.__parent = parent
        self.__dictionary = dictionary
        self.__name = None
        self.__description = None
        self.__author = None
        self.__version = None
        self.__category = None
        self.__subCategory = None
        self.__duration = None
        self.__language = None
        self.__keywords = None
        self.__update(dictionary, workingPath)

    # --------------------------------------------------------------------------
    # Get the parent attitune.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent attitune.
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
        self.__name = dictionary['name']
        self.__description = dictionary['description']
        self.__author = dictionary['author']
        self.__version = dictionary['version']
        self.__category = dictionary['category']
        self.__subCategory = dictionary['sub_category']
        self.__duration = dictionary['length']
        self.__language = dictionary['language'] #convert language format ...
        self.__keywords = dictionary['keywords']

    # --------------------------------------------------------------------------
    # Get the attitune name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the attitune name.
        @return: A string.
        """
        return self.__name

    # --------------------------------------------------------------------------
    # Get the author of the attitune.
    # --------------------------------------------------------------------------
    def getAuthor(self):
        """Get the author of the attitune.
        @return: A string.
        """
        return self.__author

    # --------------------------------------------------------------------------
    # Get the version of the attitune.
    # --------------------------------------------------------------------------
    def getVersion(self):
        """Get the version of the attitune.
        @return: A string.
        """
        return self.__version

    # --------------------------------------------------------------------------
    # Get the description of the attitune.
    # --------------------------------------------------------------------------
    def getDescription(self):
        """Get the description of the attitune.
        @return: A string.
        """
        return self.__description

    # --------------------------------------------------------------------------
    # Get the category of the attitune.
    # --------------------------------------------------------------------------
    def getCategory(self):
        """Get the category of the attitune.
        @return: A string.
        """
        return self.__category

    # --------------------------------------------------------------------------
    # Get the sub-category of the attitune.
    # --------------------------------------------------------------------------
    def getSubCategory(self):
        """Get the sub-category of the attitune.
        @return: A string.
        """
        return self.__subCategory

    # --------------------------------------------------------------------------
    # Get the language of the attitune.
    # --------------------------------------------------------------------------
    def getLanguage(self):
        """Get the language of the attitune.
        @return: A string.
        """
        return self.__language

    # --------------------------------------------------------------------------
    # Get the duration of the attitune.
    # --------------------------------------------------------------------------
    def getDuration(self):
        """Get the duration of the attitune.
        @return: A string.
        """
        return float(self.__duration)

    # --------------------------------------------------------------------------
    # Get the keywords of the attitune.
    # --------------------------------------------------------------------------
    def getKeywords(self):
        """Get the keywords of the attitune.
        @return: A string.
        """
        return self.__keywords
