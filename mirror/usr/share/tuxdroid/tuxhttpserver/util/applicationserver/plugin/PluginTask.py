#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

# ------------------------------------------------------------------------------
# Plugin task class.
# ------------------------------------------------------------------------------
class PluginTask(object):
    """Plugin task class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary):
        """Constructor of the class.
        @param parent: Parent Plugin.
        @param dictionary: Description as dictionary.
        """
        self.__parent = parent
        self.__dictionary = dictionary
        self.__name = None
        self.__description = None
        self.__command = None
        self.__type = None
        self.__activated = None
        self.__weekMask = None
        self.__weekMaskType = None
        self.__weekMaskVisible = None
        self.__date = None
        self.__dateVisible = None
        self.__hoursBegin = None
        self.__hoursBeginMask = None
        self.__hoursBeginVisible = None
        self.__hoursEnd = None
        self.__hoursEndMask = None
        self.__hoursEndVisible = None
        self.__delay = None
        self.__delayType = None
        self.__delayMask = None
        self.__delayVisible = None
        self.__update(dictionary)

    # --------------------------------------------------------------------------
    # Get the parent plugin.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent plugin.
        @return: A Gadget object.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Update the description.
    # --------------------------------------------------------------------------
    def __update(self, dictionary):
        """Update the description.
        """
        # Save the dictionary
        self.__dictionary = dictionary
        # Get the descriptor values
        # Mandatory values
        self.__name = dictionary['name']
        self.__description = dictionary['description']
        self.__command = dictionary['command'].lower()
        self.__type = dictionary['type'].upper()
        self.__activated = dictionary['activated']
        # Optional values
        self.__weekMask = "true,true,true,true,true,true,true"
        if dictionary.has_key('weekMask'):
            self.__weekMask = dictionary['weekMask']
        self.__weekMaskType = "weekMaskType"
        if dictionary.has_key('weekMaskType'):
            self.__weekMaskType = dictionary['weekMaskType'].lower()
        self.__weekMaskVisible = "false"
        if dictionary.has_key('weekMaskVisible'):
            self.__weekMaskVisible = dictionary['weekMaskVisible'].lower()
        self.__date = "0000/00/00"
        if dictionary.has_key('date'):
            self.__date = dictionary['date']
        self.__dateVisible = "false"
        if dictionary.has_key('dateVisible'):
            self.__dateVisible = dictionary['dateVisible'].lower()
        self.__hoursBegin = "00:00:00"
        if dictionary.has_key('hoursBegin'):
            self.__hoursBegin = dictionary['hoursBegin']
        self.__hoursBeginMask = "false,false,false"
        if dictionary.has_key('hoursBeginMask'):
            self.__hoursBeginMask = dictionary['hoursBeginMask'].lower()
        self.__hoursBeginVisible = "false"
        if dictionary.has_key('hoursBeginVisible'):
            self.__hoursBeginVisible = dictionary['hoursBeginVisible'].lower()
        self.__hoursEnd = "23:59:59"
        if dictionary.has_key('hoursEnd'):
            self.__hoursEnd = dictionary['hoursEnd']
        self.__hoursEndMask = "false,false,false"
        if dictionary.has_key('hoursEndMask'):
            self.__hoursEndMask = dictionary['hoursEndMask'].lower()
        self.__hoursEndVisible = "false"
        if dictionary.has_key('hoursEndVisible'):
            self.__hoursEndVisible = dictionary['hoursEndVisible'].lower()
        self.__delay = "00:01:00"
        if dictionary.has_key('delay'):
            self.__delay = dictionary['delay']
        self.__delayType = "hms"
        if dictionary.has_key('delayType'):
            self.__delayType = dictionary['delayType']
        self.__delayMask = "false,false,false"
        if dictionary.has_key('delayMask'):
            self.__delayMask = dictionary['delayMask'].lower()
        self.__delayVisible = "false"
        if dictionary.has_key('delayVisible'):
            self.__delayVisible = dictionary['delayVisible'].lower()

    # --------------------------------------------------------------------------
    # Get the task data as dictionary.
    # --------------------------------------------------------------------------
    def getDictionary(self):
        """Get the task data as dictionary.
        @return: A dictionary.
        """
        return self.__dictionary

    # --------------------------------------------------------------------------
    # Get the task name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the task name.
        @return: A string.
        """
        return self.__name

    # --------------------------------------------------------------------------
    # Get the translated name of the task.
    # --------------------------------------------------------------------------
    def getTranslatedName(self, language = None):
        """Get the translated name of the task.
        @return: A string.
        """
        if language == None:
            return self.__parent.tr(self.__name)
        else:
            return self.__parent.tr2(language, self.__name)

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
    # Get the command.
    # --------------------------------------------------------------------------
    def getCommand(self):
        """Get the command.
        @return: A string.
        """
        return self.__command

    # --------------------------------------------------------------------------
    # Get the task type.
    # --------------------------------------------------------------------------
    def getType(self):
        """Get the task type.
        @return: A string.
        """
        return self.__type

    # --------------------------------------------------------------------------
    # Get if the task is activated or not.
    # --------------------------------------------------------------------------
    def isActivated(self):
        """Get if the task is activated or not.
        @return: A boolean.
        """
        if self.__activated.lower() == "true":
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Get the week mask.
    # --------------------------------------------------------------------------
    def getWeekMask(self):
        """Get the week mask.
        @return: A list of 7 booleans.
        """
        tmpList = self.__weekMask.split(",")
        result = []
        for value in tmpList:
            if value.lower() == "true":
                result.append(True)
            else:
                result.append(False)
        if len(result) != 7:
            result = [True, True, True, True, True, True, True]
        return result

    # --------------------------------------------------------------------------
    # Get the week mask (original format).
    # --------------------------------------------------------------------------
    def getWeekMaskOF(self):
        """Get the week mask (original format).
        @return: A string.
        """
        return self.__weekMask

    # --------------------------------------------------------------------------
    # Get the week mask as dictionary.
    # --------------------------------------------------------------------------
    def getWeekMaskDict(self):
        """Get the week mask as dictionary.
        @return: A dictionary.
        """
        wList = self.getWeekMask()
        result = {}
        for i, day in enumerate(wList):
            key = "day_%d" % i
            result[key] = day
        return result

    # --------------------------------------------------------------------------
    # Get the week mask type.
    # --------------------------------------------------------------------------
    def getWeekMaskType(self):
        """Get the week mask type.
        @return: A string <"flat"|"weekpart"|"exclusive">.
        """
        return self.__weekMaskType

    # --------------------------------------------------------------------------
    # Get if the week mask is visible or not.
    # --------------------------------------------------------------------------
    def getWeekMaskIsVisible(self):
        """Get if the week mask is visible or not.
        @return: A boolean.
        """
        if self.__weekMaskVisible.lower() == "true":
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Get the date.
    # --------------------------------------------------------------------------
    def getDate(self):
        """Get the date.
        @return: A string "YYYY/MM/DD".
        """
        return self.__date

    # --------------------------------------------------------------------------
    # Get the date as dictionary.
    # --------------------------------------------------------------------------
    def getDateDict(self):
        """Get the date as dictionary.
        @return: A dictionary.
        """
        ymd = self.getDate().split("/")
        result = {
            'year' : int(ymd[0]),
            'month' : int(ymd[1]),
            'day' : int(ymd[2]),
        }
        return result

    # --------------------------------------------------------------------------
    # Get if the date is visible or not.
    # --------------------------------------------------------------------------
    def getDateIsVisible(self):
        """Get if the week mask is visible or not.
        @return: A boolean.
        """
        if self.__dateVisible.lower() == "true":
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Get the time as dictionary.
    # --------------------------------------------------------------------------
    def getTimeDict(self, timeString):
        """Get the time as dictionary.
        @param timeString: The time as string "HH:MM:SS".
        @return: A dictionary.
        """
        hms = timeString.split(":")
        result = {
            'hour' : int(hms[0]),
            'minute' : int(hms[1]),
            'second' : int(hms[2]),
        }
        return result

    # --------------------------------------------------------------------------
    # Get the time mask as dictionary.
    # --------------------------------------------------------------------------
    def getTimeMaskDict(self, timeMask):
        """Get the time mask as dictionary.
        @param timeMask: The time mask as list.
        @return: A dictionary.
        """
        result = {
            'hour' : timeMask[0],
            'minute' : timeMask[1],
            'second' : timeMask[2],
        }
        return result

    # --------------------------------------------------------------------------
    # Get the hours begin.
    # --------------------------------------------------------------------------
    def getHoursBegin(self):
        """Get the hours begin.
        @return: A string "HH:MM:SS".
        """
        return self.__hoursBegin

    # --------------------------------------------------------------------------
    # Get the hours begin mask.
    # --------------------------------------------------------------------------
    def getHoursBeginMask(self):
        """Get the hours begin mask.
        @return: A string.
        """
        tmpList = self.__hoursBeginMask.split(",")
        result = []
        for value in tmpList:
            if value.lower() == "true":
                result.append(True)
            else:
                result.append(False)
        if len(result) != 3:
            result = [True, True, True]
        return result

    # --------------------------------------------------------------------------
    # Get if the hours begin is visible or not.
    # --------------------------------------------------------------------------
    def getHoursBeginIsVisible(self):
        """Get if the hours begin is visible or not.
        @return: A boolean.
        """
        if self.__hoursBeginVisible.lower() == "true":
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Get the hours end.
    # --------------------------------------------------------------------------
    def getHoursEnd(self):
        """Get the hours end.
        @return: A string "HH:MM:SS".
        """
        return self.__hoursEnd

    # --------------------------------------------------------------------------
    # Get the hours end mask.
    # --------------------------------------------------------------------------
    def getHoursEndMask(self):
        """Get the hours end mask.
        @return: A string.
        """
        tmpList = self.__hoursEndMask.split(",")
        result = []
        for value in tmpList:
            if value.lower() == "true":
                result.append(True)
            else:
                result.append(False)
        if len(result) != 3:
            result = [True, True, True]
        return result

    # --------------------------------------------------------------------------
    # Get if the hours end is visible or not.
    # --------------------------------------------------------------------------
    def getHoursEndIsVisible(self):
        """Get if the hours end is visible or not.
        @return: A boolean.
        """
        if self.__hoursEndVisible.lower() == "true":
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Get the delay.
    # --------------------------------------------------------------------------
    def getDelay(self):
        """Get the delay.
        @return: A string "HH:MM:SS".
        """
        return self.__delay

    # --------------------------------------------------------------------------
    # Get the delay type.
    # --------------------------------------------------------------------------
    def getDelayType(self):
        """Get the delay type.
        @return: A string "hms|quarters|frequency".
        """
        return self.__delayType

    # --------------------------------------------------------------------------
    # Get the delay mask.
    # --------------------------------------------------------------------------
    def getDelayMask(self):
        """Get the delay mask.
        @return: A string.
        """
        tmpList = self.__delayMask.split(",")
        result = []
        for value in tmpList:
            if value.lower() == "true":
                result.append(True)
            else:
                result.append(False)
        if len(result) != 3:
            result = [True, True, True]
        return result

    # --------------------------------------------------------------------------
    # Get if the delay is visible or not.
    # --------------------------------------------------------------------------
    def getDelayIsVisible(self):
        """Get if the delay is visible or not.
        @return: A boolean.
        """
        if self.__delayVisible.lower() == "true":
            return True
        else:
            return False
