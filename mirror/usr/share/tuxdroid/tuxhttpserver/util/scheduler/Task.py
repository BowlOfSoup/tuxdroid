#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import datetime
import threading

from TaskDescription import *

# ------------------------------------------------------------------------------
# Class the create a scheduled task.
# ------------------------------------------------------------------------------
class Task(object):
    """Class the create a scheduled task.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, ruleType, weekMask, date, hoursBegin, hoursEnd, delay,
        command, arguments, data, storable = True):
        """Constructor of the class.
        @param ruleType: <SCH_LOOP_ABS|SCH_LOOP_REL|SCH_ONCE_ABS|SCH_ONCE_REL>
        @param weekMask: Week mask. [True, True, True, True, True, True, True]
        @param date: Date string as format [YYYY, MM, DD].
        @param hoursBegin: Hours begin as format [HH, MM, SS]
        @param hoursEnd: Hours end as format [HH, MM, SS]
        @param delay: Delay as format [HH, MM, SS]
        @param command: Command to execute as string.
        @param arguments: Arguments of the command as tuple.
        @param data: User data.
        @param storable: Task is storable or not.
        """
        dictionary = {
            'type' : ruleType,
            'weekMask' : weekMask,
            'date' : date,
            'hoursBegin' : hoursBegin,
            'hoursEnd' : hoursEnd,
            'delay' : delay,
            'command' : command,
            'arguments' : arguments,
        }
        self.__data = data
        self.__storable = storable
        self.__description = TaskDescription(self, dictionary)
        now = datetime.datetime.now()
        self.__monthAtStart = now.month
        self.__monthMask = self.__createMonthMask(self.__monthAtStart)
        if ruleType == SCH_LOOP_ABS:
            hourFixe = now.hour - delay[0]
            if hourFixe < 0:
                hourFixe = 0
            if delay[0] == 0:
                if delay[1] == 0:
                    m = 0
                else:
                    m = int(now.minute / delay[1]) * delay[1]
                self.__startTime = datetime.datetime(now.year, now.month,
                    now.day, hourFixe, m, delay[2])
                self.__incrementTime = datetime.timedelta(minutes = delay[1])
            else:
                self.__startTime = datetime.datetime(now.year, now.month,
                    now.day, hourFixe, delay[1], delay[2])
                self.__incrementTime = datetime.timedelta(hours = delay[0])
        elif ruleType == SCH_LOOP_REL:
            self.__startTime = datetime.datetime.now()
            self.__incrementTime = datetime.timedelta(seconds = delay[2],
                minutes = delay[1], hours = delay[0])
        elif ruleType == SCH_ONCE_ABS:
            if (date[0] != 0) and (date[1] != 0) and (date[2] != 0):
                self.__startTime = datetime.datetime(date[0], date[1], date[2],
                    hoursBegin[0], hoursBegin[1], hoursBegin[2])
                self.__incrementTime = None
            else:
                self.__startTime = datetime.datetime(now.year, now.month,
                    now.day, hoursBegin[0], hoursBegin[1], hoursBegin[2])
                self.__incrementTime = datetime.timedelta(days = 1)
        elif ruleType == SCH_ONCE_REL:
            self.__startTime = datetime.datetime.now()
            self.__incrementTime = datetime.timedelta(hours = delay[0],
                minutes = delay[1], seconds = delay[2])
        self.__lastExecuteTime = None

    # --------------------------------------------------------------------------
    # Get if the task is storable or not.
    # --------------------------------------------------------------------------
    def isStorable(self):
        """Get if the task is storable or not.
        @return: True or False.
        """
        return self.__storable

    # --------------------------------------------------------------------------
    # Get the description object of the task.
    # --------------------------------------------------------------------------
    def getDescription(self):
        """Get the description object of the task.
        @return: A TaskDescription object.
        """
        return self.__description

    # --------------------------------------------------------------------------
    # Get the task informations.
    # --------------------------------------------------------------------------
    def getDictionary(self):
        """Get the task informations.
        @return: A dictionary.
        """
        date = {
            'year' : self.getDescription().getDate()[0],
            'month' : self.getDescription().getDate()[1],
            'day' : self.getDescription().getDate()[2],
        }
        hoursBegin = {
            'hour' : self.getDescription().getHoursBegin()[0],
            'minute' : self.getDescription().getHoursBegin()[1],
            'second' : self.getDescription().getHoursBegin()[2],
        }
        hoursEnd = {
            'hour' : self.getDescription().getHoursEnd()[0],
            'minute' : self.getDescription().getHoursEnd()[1],
            'second' : self.getDescription().getHoursEnd()[2],
        }
        delay = {
            'hour' : self.getDescription().getDelay()[0],
            'minute' : self.getDescription().getDelay()[1],
            'second' : self.getDescription().getDelay()[2],
        }
        result = {
            'id' : self.getDescription().getId(),
            'name' : self.getDescription().getName(),
            'taskDesc' : self.getDescription().toString(),
            'type' : self.getDescription().getType(),
            'weekMaskString' : self.getDescription().getWeekMaskString(),
            'date' : date,
            'hoursBegin' : hoursBegin,
            'hoursEnd' : hoursEnd,
            'delay' : delay,
            'userData' : self.__data,
        }
        return result

    # --------------------------------------------------------------------------
    # Create the month mask.
    # --------------------------------------------------------------------------
    def __createMonthMask(self, month):
        """Create the month mask.
        @param month: Month index of the year.
        @return: The month mask.
        """
        now = datetime.datetime.now()
        firstDayOfMonth = datetime.datetime(now.year, month, 1, 0, 0,
            0).weekday()
        result = []
        dayIndex = firstDayOfMonth
        for i in range(40):
            result.append(self.__description.getWeekMask()[dayIndex])
            dayIndex += 1
            if dayIndex > 6:
                dayIndex = 0
        return result

    # --------------------------------------------------------------------------
    # Get the next allowed day for executing the task.
    # --------------------------------------------------------------------------
    def __getNextAllowedDay(self, day):
        """Get the next allowed day for executing the task.
        @param day: Day index of the month.
        @return: The number of day to skip.
        """
        inc = day
        while not self.__monthMask[inc]:
            inc += 1
        return inc - day

    # --------------------------------------------------------------------------
    # Get the next time date of task execute.
    # --------------------------------------------------------------------------
    def getNextExecuteTime(self):
        """Get the next time date of task execute.
        @return: The datetime value of the next execution.
        """
        result = None
        if self.__description.getType() == SCH_LOOP_ABS:
            if self.__lastExecuteTime == None:
                result = self.__startTime + self.__incrementTime
            else:
                result = self.__lastExecuteTime + self.__incrementTime
        elif self.__description.getType() == SCH_LOOP_REL:
            if self.__lastExecuteTime == None:
                result = self.__startTime + self.__incrementTime
            else:
                result = self.__lastExecuteTime + self.__incrementTime
        elif self.__description.getType() == SCH_ONCE_ABS:
            if self.__lastExecuteTime == None:
                result = self.__startTime
            else:
                if self.__incrementTime == None:
                    result = None
                else:
                    result = self.__lastExecuteTime + self.__incrementTime
        elif self.__description.getType() == SCH_ONCE_REL:
            if self.__lastExecuteTime == None:
                result = self.__startTime + self.__incrementTime
            else:
                result = None
        if result == None:
            return None
        if result.month != self.__monthAtStart:
            self.__monthAtStart = result.month
            self.__monthMask = self.__createMonthMask(self.__monthAtStart)
        if not self.__monthMask[result.day - 1]:
            inc = self.__getNextAllowedDay(result.day - 1)
            result += datetime.timedelta(days = inc)
        self.__lastExecuteTime = result
        return result

    # --------------------------------------------------------------------------
    # Execute the task.
    # --------------------------------------------------------------------------
    def execute(self, appGlobals):
        """Execute the task.
        """
        if self.getDescription().getType() in [SCH_LOOP_ABS, SCH_LOOP_REL]:
            if not self.getDescription()._checkNowIsInHoursRange():
                return False
        def async():
            try:
                command = eval(self.__description.getCommand(), appGlobals)
                arguments = self.__description.getArguments()
                command(*arguments)
            except:
                import sys
                import traceback
                fList = traceback.format_exception(sys.exc_info()[0],
                    sys.exc_info()[1],
                    sys.exc_info()[2])
                trace = ""
                for line in fList:
                    trace += line
                print trace
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Load a task.
    # --------------------------------------------------------------------------
    def load(filePath):
        """Load a task.
        @param filePath: Fle path of the task.
        @return: The Task object or None.
        """
        if not os.path.isfile(filePath):
            return None
        if filePath.lower().rfind(".tcf") != len(filePath) - 4:
            return None
        try:
            f = open(filePath, "rb")
            try:
                dictionary = eval(f.read())
            except:
                f.close()
                return None
        finally:
            f.close()
        try:
            id = dictionary['id']
            name = dictionary['name']
            ruleType = dictionary['type']
            weekMask = [True, True, True, True, True, True, True]
            splitedStr = dictionary['weekMaskString'].split(",")
            if len(splitedStr) == 7:
                for i, value in enumerate(splitedStr):
                    if value == "true":
                        weekMask[i] = True
                    else:
                        weekMask[i] = False
            date = [
                dictionary['date']['year'],
                dictionary['date']['month'],
                dictionary['date']['day'],
            ]
            hoursBegin = [
                dictionary['hoursBegin']['hour'],
                dictionary['hoursBegin']['minute'],
                dictionary['hoursBegin']['second'],
            ]
            hoursEnd = [
                dictionary['hoursEnd']['hour'],
                dictionary['hoursEnd']['minute'],
                dictionary['hoursEnd']['second'],
            ]
            delay = [
                dictionary['delay']['hour'],
                dictionary['delay']['minute'],
                dictionary['delay']['second'],
            ]
            command = dictionary['command']
            arguments = dictionary['arguments']
            data = dictionary['userData']
        except:
            return None
        task = Task(ruleType, weekMask, date, hoursBegin, hoursEnd, delay,
            command, arguments, data, True)
        task.getDescription().setId(id)
        task.getDescription().setName(name)
        return task

    # --------------------------------------------------------------------------
    # Store a task.
    # --------------------------------------------------------------------------
    def store(task, directory):
        """Store a task.
        @param task: Task object to store.
        @param directory: Directory where to store the task.
        @return: The success of the storing.
        """
        if not os.path.isdir(directory):
            return False
        taskInfos = task.getDictionary()
        taskInfos['command'] = task.getDescription().getCommand()
        taskInfos['arguments'] = task.getDescription().getArguments()
        fileName = taskInfos['id'] + ".tcf"
        filePath = os.path.join(directory, fileName)
        result = False
        try:
            f = open(filePath, "w")
            try:
                f.write(str(taskInfos))
                result = True
            except:
                pass
        finally:
            f.close()
        return result

    load = staticmethod(load)
    store = staticmethod(store)
