#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is highly inspired by a "gadget framework"  written by
#    "Yoran Brault" <http://artisan.karma-lab.net>

# Possible parameter types.
PARAMETER_TYPES_LIST = ['integer', 'string', 'boolean', 'booleans', 'float',
    'enum', 'password', 'file', 'directory', 'increment']

# ------------------------------------------------------------------------------
# Plugin parameter class.
# ------------------------------------------------------------------------------
class PluginParameter(object):
    """Plugin parameter class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary):
        """Constructor of the class.
        @param parent: Parent Plugin.
        @param dictionary: Parameter as dictionary.
        """
        self.__parent = parent
        self.__parentForTranslations = parent
        self.__dictionary = dictionary
        self.__name = None
        self.__type = None
        self.__enumValues = None
        self.__enumValuesList = None
        self.__defaultValue = None
        self.__description = None
        self.__category = None
        self.__minValue = None
        self.__maxValue = None
        self.__platform = None
        self.__visible = None
        self.__filters = None
        self.__stepValue = None
        self.__task = None
        self.__update()

    # --------------------------------------------------------------------------
    # Update the field values with the parameter dictionary.
    # --------------------------------------------------------------------------
    def __update(self):
        """Update the field values with the parameter dictionary.
        """
        self.__name = self.__dictionary['name']
        self.__type = self.__dictionary['type']
        self.__enumValuesList = []
        if self.__type.lower().find("enum") == 0:
            self.__type = "enum"
            idxb = self.__dictionary['type'].find("(") + 1
            idxe = self.__dictionary['type'].rfind(")")
            self.__enumValues = self.__dictionary['type'][idxb:idxe]
            for value in self.__enumValues.split(","):
                self.__enumValuesList.append(value.strip())
        elif self.__type.lower().find("booleans") == 0:
            self.__type = "booleans"
            idxb = self.__dictionary['type'].find("(") + 1
            idxe = self.__dictionary['type'].rfind(")")
            self.__enumValues = self.__dictionary['type'][idxb:idxe]
            for value in self.__enumValues.split(","):
                self.__enumValuesList.append(value.strip())
        else:
            self.__enumValues = ""
        self.__defaultValue = self.__dictionary['defaultValue']
        self.__description = self.__dictionary['description']
        self.__category = ""
        if self.__dictionary.has_key('category'):
            self.__category = self.__dictionary['category']
        self.__minValue = "0.0"
        if self.__dictionary.has_key('minValue'):
            self.__minValue = self.__dictionary['minValue']
        self.__maxValue = "1.0"
        if self.__dictionary.has_key('maxValue'):
            self.__maxValue = self.__dictionary['maxValue']
        self.__platform = "all"
        if self.__dictionary.has_key('platform'):
            self.__platform = self.__dictionary['platform'].lower()
        self.__visible = "true"
        if self.__dictionary.has_key('visible'):
            self.__visible = self.__dictionary['visible'].lower()
        self.__filters = ""
        if self.__dictionary.has_key('filters'):
            self.__filters = self.__dictionary['filters']
        self.__stepValue = "1"
        if self.__dictionary.has_key('stepValue'):
            self.__stepValue = self.__dictionary['stepValue']
        self.__task = "none"
        if self.__dictionary.has_key('task'):
            self.__task = self.__dictionary['task']

    # --------------------------------------------------------------------------
    # Get the parent plugin.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent plugin.
        @return: The parent plugin.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Set the parent object for translations.
    # --------------------------------------------------------------------------
    def setParentForTranslations(self, parent):
        """Set the parent object for translations.
        @param parent: Gadget or Plugin object.
        """
        self.__parentForTranslations = parent

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
    # Get the type.
    # --------------------------------------------------------------------------
    def getType(self):
        """Get the type.
        @return: A string.
        """
        return self.__type

    # --------------------------------------------------------------------------
    # Get the default value.
    # --------------------------------------------------------------------------
    def getDefaultValue(self, language = None):
        """Get the default value.
        @return: A string.
        """
        if self.__defaultValue == {}:
            return ""
        if language == None:
            return self.__defaultValue
        else:
            return self.__parentForTranslations.tr2(language, self.__defaultValue)

    # --------------------------------------------------------------------------
    # Set the default value.
    # --------------------------------------------------------------------------
    def setDefaultValue(self, defaultValue):
        """Set the default value.
        @param defaultValue: Default value to set.
        """
        self.__defaultValue = defaultValue

    # --------------------------------------------------------------------------
    # Get the description.
    # --------------------------------------------------------------------------
    def getDescription(self, language = None):
        """Get the description.
        @return: A string.
        """
        if language == None:
            return self.__parentForTranslations.tr(self.__description)
        else:
            return self.__parentForTranslations.tr2(language, self.__description)

    # --------------------------------------------------------------------------
    # Get the translated name.
    # --------------------------------------------------------------------------
    def getTranslatedName(self, language = None):
        """Get the translated name.
        @return: A string.
        """
        if language == None:
            return self.__parentForTranslations.tr(self.__name)
        else:
            return self.__parentForTranslations.tr2(language, self.__name)

    # --------------------------------------------------------------------------
    # Get the category.
    # --------------------------------------------------------------------------
    def getCategory(self):
        """Get the category.
        @return: A string.
        """
        return self.__category

    # --------------------------------------------------------------------------
    # Get the enumerated values.
    # --------------------------------------------------------------------------
    def getEnumValues(self, language = None):
        """Get the enumerated values.
        @return: A string.
        """
        if language == None:
            return self.__parentForTranslations.tr(self.__enumValues)
        else:
            return self.__parentForTranslations.tr2(language, self.__enumValues)

    # --------------------------------------------------------------------------
    # Get the untranslated value of an enumerated value.
    # --------------------------------------------------------------------------
    def getUntranslatedEnumValue(self, translatedValue, language = None):
        """Get the untranslated value of an enumerated value.
        @return: A string.
        """
        translatedValue = translatedValue.strip()
        translatedEnumValues = self.getEnumValues(language)
        idx = -1
        for i, value in enumerate(translatedEnumValues.split(",")):
            if value.strip() == translatedValue:
                idx = i
                break
        if idx != -1:
            try:
                result = self.__enumValuesList[idx]
            except:
                result = translatedValue
            return result
        else:
            return translatedValue

    # --------------------------------------------------------------------------
    # Get the minimal value.
    # --------------------------------------------------------------------------
    def getMinValue(self):
        """Get the minimal value.
        @return: A string.
        """
        return self.__minValue

    # --------------------------------------------------------------------------
    # Get the maximal value.
    # --------------------------------------------------------------------------
    def getMaxValue(self):
        """Get the maximal value.
        @return: A string.
        """
        return self.__maxValue

    # --------------------------------------------------------------------------
    # Get the platform of this parameter.
    # --------------------------------------------------------------------------
    def getPlatform(self):
        """Get the platform of this parameter.
        @return: A string. <"all"|"linux"|"windows">
        """
        return self.__platform

    # --------------------------------------------------------------------------
    # Get if the parameter is visible or not.
    # --------------------------------------------------------------------------
    def isVisible(self):
        """Get if the parameter is visible or not.
        @return: A string. <"true"|"false">
        """
        if self.__visible.lower() == "true":
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Set if the parameter is visible or not.
    # --------------------------------------------------------------------------
    def setVisible(self, isVisible):
        """Set if the parameter is visible or not.
        @param isVisible: A string. <"true"|"false">
        """
        self.__visible = isVisible

    # --------------------------------------------------------------------------
    # Get the file extention filters. (for type="file")
    # --------------------------------------------------------------------------
    def getFilters(self):
        """Get the file extention filters. (for type="file")
        @return: A string.
        """
        return self.__filters

    # --------------------------------------------------------------------------
    # Get the step value.
    # --------------------------------------------------------------------------
    def getStepValue(self):
        """Get the step value.
        @return: A string.
        """
        return self.__stepValue

    # --------------------------------------------------------------------------
    # Get the associated task.
    # --------------------------------------------------------------------------
    def getTask(self):
        """Get the associated task.
        @return: A string.
        """
        return self.__task

    # --------------------------------------------------------------------------
    # Get if the parameter is associated to a task or not.
    # --------------------------------------------------------------------------
    def forTask(self):
        """Get if the parameter is associated to a task or not.
        @return: A boolean.
        """
        return self.__task != "none"

