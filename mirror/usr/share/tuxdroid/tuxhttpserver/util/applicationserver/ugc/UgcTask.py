#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

# ------------------------------------------------------------------------------
# UGC task class.
# ------------------------------------------------------------------------------
class UgcTask(object):
    """UGC task class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary):
        """Constructor of the class.
        @param parent: Parent Ugc.
        @param dictionary: Description as dictionary.
        """
        self.__parent = parent
        self.__dictionary = dictionary
        self.__name = None
        self.__activated = None
        self.__weekMask = None
        self.__date = None
        self.__hoursBegin = None
        self.__hoursEnd = None
        self.__delay = None
        self.__update(dictionary)
        self.__taskId1 = None
        self.__taskId2 = None

    # --------------------------------------------------------------------------
    # Get the parent Ugc.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent Ugc.
        @return: An Ugc object.
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
        self.__activated = dictionary['activated']
        self.__weekMask = "true,true,true,true,true,true,true"
        if dictionary.has_key('weekMask'):
            self.__weekMask = dictionary['weekMask']
        self.__date = "0000/00/00"
        if dictionary.has_key('date'):
            self.__date = dictionary['date']
        self.__hoursBegin = "00:00:00"
        if dictionary.has_key('hoursBegin'):
            self.__hoursBegin = dictionary['hoursBegin']
        self.__hoursEnd = "23:59:59"
        if dictionary.has_key('hoursEnd'):
            self.__hoursEnd = dictionary['hoursEnd']
        self.__delay = "00:01:00"
        if dictionary.has_key('delay'):
            self.__delay = dictionary['delay']

    # --------------------------------------------------------------------------
    # Get the task name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the task name.
        @return: A string.
        """
        return self.__name

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
    # Set if the task is activated or not.
    # --------------------------------------------------------------------------
    def setActivated(self, activated):
        """Set if the task is activated or not.
        @param activated: Activated as string <"true"|"false">.
        """
        self.__activated = "true"
        dictionary['activated'] = self.__activated
        # TODO : configure scheduler

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
    # Set the week mask.
    # --------------------------------------------------------------------------
    def setWeekMask(self, weekMask):
        """Set the week mask.
        @param weekMask: A string.
        """
        self.__weekMask = weekMask
        dictionary['weekMask'] = self.__weekMask

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
    # Get the date.
    # --------------------------------------------------------------------------
    def getDate(self):
        """Get the date.
        @return: A string "YYYY/MM/DD".
        """
        return self.__date

    # --------------------------------------------------------------------------
    # Set the date.
    # --------------------------------------------------------------------------
    def setDate(self, date):
        """Set the date.
        @param date: A string "YYYY/MM/DD".
        """
        self.__date = date
        dictionary['date'] = self.__date

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
    # Get the hours begin.
    # --------------------------------------------------------------------------
    def getHoursBegin(self):
        """Get the hours begin.
        @return: A string "HH:MM:SS".
        """
        return self.__hoursBegin

    # --------------------------------------------------------------------------
    # Set the hours begin.
    # --------------------------------------------------------------------------
    def setHoursBegin(self, hoursBegin):
        """Set the hours begin.
        @param hoursBegin: A string "HH:MM:SS".
        """
        self.__hoursBegin = hoursBegin
        self.__dictionary['hoursBegin'] = self.__hoursBegin

    # --------------------------------------------------------------------------
    # Get the hours end.
    # --------------------------------------------------------------------------
    def getHoursEnd(self):
        """Get the hours end.
        @return: A string "HH:MM:SS".
        """
        return self.__hoursEnd

    # --------------------------------------------------------------------------
    # Set the hours end.
    # --------------------------------------------------------------------------
    def setHoursEnd(self, hoursEnd):
        """Set the hours end.
        @param hoursEnd: A string "HH:MM:SS".
        """
        self.__hoursEnd = hoursEnd
        self.__dictionary['hoursEnd'] = self.__hoursEnd

    # --------------------------------------------------------------------------
    # Get the delay.
    # --------------------------------------------------------------------------
    def getDelay(self):
        """Get the delay.
        @return: A string "HH:MM:SS".
        """
        return self.__delay

    # --------------------------------------------------------------------------
    # Set the delay.
    # --------------------------------------------------------------------------
    def setDelay(self, delay):
        """Set the delay.
        @param delay: A string "HH:MM:SS".
        """
        self.__delay = delay
        self.__dictionary['delay'] = self.__delay

    # --------------------------------------------------------------------------
    # Set the task id number 1.
    # --------------------------------------------------------------------------
    def setTaskId1(self, taskId):
        """Set the task id number 1.
        @param taskId: The task id.
        """
        self.__taskId1 = taskId

    # --------------------------------------------------------------------------
    # Get the task id number 1.
    # --------------------------------------------------------------------------
    def getTaskId1(self):
        """Get the task id number 1.
        @return: The task id.
        """
        return self.__taskId1

    # --------------------------------------------------------------------------
    # Set the task id number 2.
    # --------------------------------------------------------------------------
    def setTaskId2(self, taskId):
        """Set the task id number 2.
        @param taskId: The task id.
        """
        self.__taskId2 = taskId

    # --------------------------------------------------------------------------
    # Get the task id number 2.
    # --------------------------------------------------------------------------
    def getTaskId2(self):
        """Get the task id number 2.
        @return: The task id.
        """
        return self.__taskId2
