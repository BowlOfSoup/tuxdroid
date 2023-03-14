#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import datetime

SCH_LOOP_ABS = 0
SCH_LOOP_REL = 1
SCH_ONCE_ABS = 2
SCH_ONCE_REL = 3

TASK_TYPE_NAMES = [
    "EVERY X",
    "EVERY X FROM FULL HOUR",
    "DAILY AT",
    "ONCE AT",
    "ONCE DELAYED",
]

# ------------------------------------------------------------------------------
# Task description class.
# ------------------------------------------------------------------------------
class TaskDescription(object):
    """Task description class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary):
        """Constructor of the class.
        @param parent: Parent Task.
        @param dictionary: Description as dictionary.
        """
        self.__parent = parent
        self.__dictionary = dictionary
        self.__name = None
        self.__id = None

    # --------------------------------------------------------------------------
    # Get the parent task.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent task.
        @return: A Task object.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Check if the current time is in the hours range.
    # --------------------------------------------------------------------------
    def _checkNowIsInHoursRange(self):
        """Check if the current time is in the hours range.
        @return: True or False.
        """
        now = datetime.datetime.now()
        hB = datetime.datetime(now.year, now.month, now.day,
            self.getHoursBegin()[0],
            self.getHoursBegin()[1],
            self.getHoursBegin()[2])
        hE = datetime.datetime(now.year, now.month, now.day,
            self.getHoursEnd()[0],
            self.getHoursEnd()[1],
            self.getHoursEnd()[2])
        if (hB <= hE): # case now in [1h .. 2h]
            if (now >= hB) and (now < hE):
                return True
            else:
                return False
        else: # case now in [2h .. 1h]
            m = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
            mm = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
            if ((now >= hB) and (now <= m)) or ((now >= mm) and (now < hE)):
                return True
            else:
                return False

    # --------------------------------------------------------------------------
    # Get the task name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the task name.
        @return: A string.
        """
        return self.__name

    # --------------------------------------------------------------------------
    # Set the task name.
    # --------------------------------------------------------------------------
    def setName(self, name):
        """Set the task name.
        @param name: Task name.
        """
        self.__name = name

    # --------------------------------------------------------------------------
    # Get the task identifier.
    # --------------------------------------------------------------------------
    def getId(self):
        """Get the task identifier.
        @return: A string.
        """
        return self.__id

    # --------------------------------------------------------------------------
    # Set the task identifier.
    # --------------------------------------------------------------------------
    def setId(self, id):
        """Set the task identifier.
        @param id: Task identifier.
        """
        self.__id = id

    # --------------------------------------------------------------------------
    # Get the task type.
    # --------------------------------------------------------------------------
    def getType(self):
        """Get the task type.
        @return: <SCH_LOOP_ABS|SCH_LOOP_REL|SCH_ONCE_ABS|SCH_ONCE_REL>.
        """
        return self.__dictionary['type']

    # --------------------------------------------------------------------------
    # Get the task configuration to string.
    # --------------------------------------------------------------------------
    def toString(self):
        """Get the task configuration to string.
        @return: A string
        """
        ymdDate = "%.4d/%.2d/%.2d" % (self.getDate()[0], self.getDate()[1],
            self.getDate()[2])
        hmsHb = "%.2d:%.2d:%.2d" % (self.getHoursBegin()[0],
            self.getHoursBegin()[1], self.getHoursBegin()[2])
        hmsHe = "%.2d:%.2d:%.2d" % (self.getHoursEnd()[0],
            self.getHoursEnd()[1], self.getHoursEnd()[2])
        hmsDelay = "%.2d:%.2d:%.2d" % (self.getDelay()[0], self.getDelay()[1],
            self.getDelay()[2])
        if self.getType() == SCH_LOOP_REL:
            return "[EVERY X] Delay %s Begin %s End %s" % (hmsDelay, hmsHb,
                hmsHe)
        elif self.getType() == SCH_LOOP_ABS:
            return "[EVERY X FROM FULL HOUR] Delay %s Begin %s End %s" % (
                hmsDelay, hmsHb, hmsHe)
        elif self.getType() == SCH_ONCE_ABS:
            if (self.getDate()[0] == 0) and (self.getDate()[1] == 0) and \
                (self.getDate()[2] == 0):
                return "[DAILY AT] Time %s" % hmsHb
            else:
                return "[ONCE AT] Date %s Time %s" % (ymdDate, hmsHb)
        else:
            return "[ONCE DELAYED] Timeout %s" % hmsDelay

    # --------------------------------------------------------------------------
    # Get the week mask.
    # --------------------------------------------------------------------------
    def getWeekMask(self):
        """Get the week mask.
        @return: Week mask. [True, True, True, True, True, True, True]
        """
        return self.__dictionary['weekMask']

    # --------------------------------------------------------------------------
    # Get the week mask.
    # --------------------------------------------------------------------------
    def getWeekMaskString(self):
        """Get the week mask.
        @return: A string.
        """
        result = ""
        for b in self.__dictionary['weekMask']:
            if len(result) > 0:
                result += ","
            if b:
                result += "true"
            else:
                result += "false"
        return result

    # --------------------------------------------------------------------------
    # Get the date values.
    # --------------------------------------------------------------------------
    def getDate(self):
        """Get the date values.
        @return: A list of integer.
        """
        return self.__dictionary['date']

    # --------------------------------------------------------------------------
    # Get the hoursBegin values.
    # --------------------------------------------------------------------------
    def getHoursBegin(self):
        """Get the hoursBegin values.
        @return: A list of integer.
        """
        return self.__dictionary['hoursBegin']

    # --------------------------------------------------------------------------
    # Get the hoursEnd values.
    # --------------------------------------------------------------------------
    def getHoursEnd(self):
        """Get the hoursEnd values.
        @return: A list of integer.
        """
        return self.__dictionary['hoursEnd']

    # --------------------------------------------------------------------------
    # Get the delay values.
    # --------------------------------------------------------------------------
    def getDelay(self):
        """Get the delay values.
        @return: A list of integer.
        """
        return self.__dictionary['delay']

    # --------------------------------------------------------------------------
    # Get the command.
    # --------------------------------------------------------------------------
    def getCommand(self):
        """Get the command.
        @return: A string.
        """
        return self.__dictionary['command']

    # --------------------------------------------------------------------------
    # Get the arguments of the command.
    # --------------------------------------------------------------------------
    def getArguments(self):
        """Get the arguments of the command.
        @return: A tuple.
        """
        return self.__dictionary['arguments']
