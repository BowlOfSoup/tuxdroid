#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import datetime

from util.scheduler.Scheduler import Scheduler
from util.scheduler.Task import *
from util.logger.SimpleLogger import *

# Scheduler manager events/statuses
ST_NAME_SCM_TASK_ADDED = "scheduler_manager_task_added"
ST_NAME_SCM_TASK_REMOVED = "scheduler_manager_task_removed"
ST_NAME_SCM_TASKS_LOADED = "scheduler_manager_tasks_loaded"
ST_NAME_SCM_TASKS_UNLOADED = "scheduler_manager_tasks_unloaded"

# Scheduler manager events/statuses list
SW_NAME_SCHEDULER_MANAGER = [
    ST_NAME_SCM_TASK_ADDED,
    ST_NAME_SCM_TASK_REMOVED,
    ST_NAME_SCM_TASKS_LOADED,
    ST_NAME_SCM_TASKS_UNLOADED,
]

# ==============================================================================
# ******************************************************************************
# RESOURCE DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the resource "scheduler".
# ==============================================================================
class TDSResourceScheduler(TDSResource):
    """Resource scheduler class.
    """

    # ==========================================================================
    # Inherited methods from TDSResource
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Configure the resource.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the resource.
        """
        self.name = "scheduler"
        self.comment = "Resource to manage the scheduler."
        self.fileName = RESOURCE_FILENAME
        # Create the scheduler.
        self.__scheduler = Scheduler(globals())
        self.__scheduler.setOnTaskAddedCallback(self.__onTaskAdded)
        self.__scheduler.setOnTaskRemovedCallback(self.__onTaskRemoved)
        self.__scheduler.setOnTasksLoadedCallback(self.__onTasksLoaded)
        self.__scheduler.setOnTasksUnloadedCallback(self.__onTasksUnloaded)
        # Registering the scheduler manager statuses.
        for statusName in SW_NAME_SCHEDULER_MANAGER:
            eventsHandler.insert(statusName)
        # Create a logger
        self.logger = SimpleLogger("scs_scheduler")
        self.logger.resetLog()
        self.logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.logger.setTarget(TDS_CONF_LOG_TARGET)
        self.logger.logInfo("-----------------------------------------------")
        self.logger.logInfo("Smart-core Scheduler")
        self.logger.logInfo("Licence : GPL")
        self.logger.logInfo("-----------------------------------------------")
        # Start the scheduler
        self.logger.logInfo("Starting the scheduler.")
        self.__scheduler.start()
        self.logger.logInfo("Scheduler is started.")

    # --------------------------------------------------------------------------
    # Stop the resource.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the resource.
        """
        self.logger.logInfo("Stopping the scheduler.")
        self.__scheduler.stop()
        self.logger.logInfo("Scheduler is stopped.")

    # ==========================================================================
    # Private methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Event on task added.
    # --------------------------------------------------------------------------
    def __onTaskAdded(self, task):
        """Event on task added.
        @param task: Task object.
        """
        taskName = task.getDescription().getName()
        taskDesc = task.getDescription().toString()
        self.logger.logInfo("Task added [%s] : %s" % (taskName, taskDesc))
        resourceStatus.publishEvents(False, ST_NAME_SCM_TASK_ADDED,
            [task.getDescription().getId(), task.getDescription().getName()])

    # --------------------------------------------------------------------------
    # Event on task removed.
    # --------------------------------------------------------------------------
    def __onTaskRemoved(self, task):
        """Event on task removed.
        @param task: Task object.
        """
        taskName = task.getDescription().getName()
        taskDesc = task.getDescription().toString()
        self.logger.logInfo("Task removed [%s] : %s" % (taskName, taskDesc))
        resourceStatus.publishEvents(False, ST_NAME_SCM_TASK_REMOVED,
            [task.getDescription().getId(), task.getDescription().getName()])

    # --------------------------------------------------------------------------
    # Event on tasks loaded.
    # --------------------------------------------------------------------------
    def __onTasksLoaded(self):
        """Event on tasks loaded.
        """
        self.logger.logInfo("Tasks container is loaded")
        resourceStatus.publishEvents(True, ST_NAME_SCM_TASKS_LOADED, ["True",])

    # --------------------------------------------------------------------------
    # Event on tasks unloaded.
    # --------------------------------------------------------------------------
    def __onTasksUnloaded(self):
        """Event on tasks unloaded.
        """
        self.logger.logInfo("Tasks container is unloaded")
        resourceStatus.publishEvents(True, ST_NAME_SCM_TASKS_UNLOADED,
            ["True",])

    # --------------------------------------------------------------------------
    # Convert week mask string to booleans list.
    # --------------------------------------------------------------------------
    def weekMaskStringToList(self, weekMaskString):
        """Convert week mask string to booleans list.
        @param weekMaskString: Week mask string.
        @return: A list of booleans.
        """
        result = [True, True, True, True, True, True, True]
        try:
            splitedStr = weekMaskString.split(",")
            if len(splitedStr) == 7:
                for i, value in enumerate(splitedStr):
                    if value == "true":
                        result[i] = True
                    else:
                        result[i] = False
        except:
            pass
        return result

    # --------------------------------------------------------------------------
    # Convert a date string to integers list.
    # --------------------------------------------------------------------------
    def dateStringToList(self, dateString):
        """Convert a date string to integers list.
        @param dateString: Date string.
        @return: A list of integers.
        """
        result = [0, 0, 0]
        try:
            splitedStr = dateString.split("/")
            if len(splitedStr) == 3:
                for i, value in enumerate(splitedStr):
                    result[i] = int(value)
        except:
            pass
        return result

    # --------------------------------------------------------------------------
    # Convert a time string to integers list.
    # --------------------------------------------------------------------------
    def timeStringToList(self, timeString):
        """Convert a time string to integers list.
        @param timeString: Time string.
        @return: A list of integers.
        """
        result = [0, 0, 0]
        try:
            splitedStr = timeString.split(":")
            if len(splitedStr) == 3:
                for i, value in enumerate(splitedStr):
                    result[i] = int(value)
        except:
            pass
        return result

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Get the scheduler object.
    # --------------------------------------------------------------------------
    def getScheduler(self):
        """Get the scheduler object.
        @return: A Scheduler object.
        """
        return self.__scheduler

    # --------------------------------------------------------------------------
    # Create a task which start every x delay.
    # --------------------------------------------------------------------------
    def createTask_RunEveryX(self, name, weekMask, hoursBegin, hoursEnd, delay,
        command, arguments, data):
        """Create a task which start every x delay.
        @param name: Task name.
        @param weekMask: Week mask. [True, True, True, True, True, True, True]
        @param hoursBegin: Hours begin. [Hour, Minute, Second]
        @param hoursEnd: Hours end. [Hour, Minute, Second]
        @param delay: Delay. [Hour, Minute, Second]
        @param command: Command to execute.
        @param arguments: Arguments of the command.
        @param data: User data.
        @return: The task id and the task name or None None.
        """
        task = Task(SCH_LOOP_REL, weekMask, [0, 0, 0], hoursBegin, hoursEnd,
            delay, command, arguments, data)
        return self.__scheduler.insertTask(task, name)

    # --------------------------------------------------------------------------
    # Create a task which start every x delay synchronized with hh:00:00.
    # --------------------------------------------------------------------------
    def createTask_RunEveryXFromFullHour(self, name, weekMask, hoursBegin,
        hoursEnd, delay, command, arguments, data):
        """Create a task which start every x delay synchronized with hh:00:00.
        @param name: Task name.
        @param weekMask: Week mask. [True, True, True, True, True, True, True]
        @param hoursBegin: Hours begin. [Hour, Minute, Second]
        @param hoursEnd: Hours end. [Hour, Minute, Second]
        @param delay: Delay. [Hour, Minute, Second]
        @param command: Command to execute.
        @param arguments: Arguments of the command.
        @param data: User data.
        @return: The task id and the task name or None None.
        """
        task = Task(SCH_LOOP_ABS, weekMask, [0, 0, 0], hoursBegin, hoursEnd,
            delay, command, arguments, data)
        return self.__scheduler.insertTask(task, name)

    # --------------------------------------------------------------------------
    # Create a daily task which run at fixed time.
    # --------------------------------------------------------------------------
    def createTask_RunDailyAtTime(self, name, weekMask, hoursBegin, command,
        arguments, data):
        """Create a daily task which run at fixed time.
        @param name: Task name.
        @param weekMask: Week mask. [True, True, True, True, True, True, True]
        @param hoursBegin: Hours begin. [Hour, Minute, Second]
        @param command: Command to execute.
        @param arguments: Arguments of the command.
        @param data: User data.
        @return: The task id and the task name or None None.
        """
        task = Task(SCH_ONCE_ABS, weekMask, [0, 0, 0], hoursBegin, [0, 0, 0],
            [0, 0, 0], command, arguments, data)
        return self.__scheduler.insertTask(task, name)

    # --------------------------------------------------------------------------
    # Create a task which run once time at a specific date time.
    # --------------------------------------------------------------------------
    def createTask_RunOnceAtDateTime(self, name, date, hoursBegin, command,
        arguments, data):
        """Create a task which run once time at a specific date time.
        @param name: Task name.
        @param date: Date. [Year, Month, Day]
        @param hoursBegin: Hours begin. [Hour, Minute, Second]
        @param command: Command to execute.
        @param arguments: Arguments of the command.
        @param data: User data.
        @return: The task id and the task name or None None.
        """
        task = Task(SCH_ONCE_ABS, [True, True, True, True, True, True, True],
            date, hoursBegin, [0, 0, 0], [0, 0, 0], command, arguments, data)
        return self.__scheduler.insertTask(task, name)

    # --------------------------------------------------------------------------
    # Create a task which run once time after a delay.
    # --------------------------------------------------------------------------
    def createTask_RunOnceDelayed(self, name, delay, command, arguments, data):
        """Create a task which run once time after a delay.
        @param name: Task name.
        @param delay: Delay. [Hour, Minute, Second]
        @param command: Command to execute.
        @param arguments: Arguments of the command.
        @param data: User data.
        @return: The task id and the task name or None None.
        """
        task = Task(SCH_ONCE_REL, [True, True, True, True, True, True, True],
            [0, 0, 0], [0, 0, 0], [0, 0, 0], delay, command, arguments, data)
        return self.__scheduler.insertTask(task, name)

    # --------------------------------------------------------------------------
    # Create a task.
    # --------------------------------------------------------------------------
    def createTask(self, command, arguments, taskType, taskName, weekMask, date,
        hoursBegin, hoursEnd, delay, data):
        """Create a task.
        @param command: Command to execute.
        @param arguments: Arguments of the command.
        @param taskType: <EVERY X|EVERY X FROM FULL HOUR|DAILY AT|ONCE AT|
                          ONCE DELAYED>
        @param taskName: Task name.
        @param weekMask: Week mask. [True, True, True, True, True, True, True]
        @param date: Date. [Year, Month, Day]
        @param hoursBegin: Hours begin. [Hour, Minute, Second]
        @param hoursEnd: Hours end. [Hour, Minute, Second]
        @param delay: Delay. [Hour, Minute, Second]
        @param data: User data.
        @return: The task id and the task name or None None.
        """
        if taskType == "EVERY X":
            return self.createTask_RunEveryX(taskName, weekMask, hoursBegin,
                hoursEnd, delay, command, arguments, data)
        if taskType == "EVERY X FROM FULL HOUR":
            return self.createTask_RunEveryXFromFullHour(taskName, weekMask,
                hoursBegin, hoursEnd, delay, command, arguments, data)
        if taskType == "DAILY AT":
            return self.createTask_RunDailyAtTime(taskName, weekMask,
                hoursBegin, command, arguments, data)
        if taskType == "ONCE AT":
            return self.createTask_RunOnceAtDateTime(taskName, date, hoursBegin,
                command, arguments, data)
        if taskType == "ONCE DELAYED":
            return self.createTask_RunOnceDelayed(taskName, delay,
                command, arguments, data)
        return None, None

    # --------------------------------------------------------------------------
    # Execute the action of a scheduled task.
    # --------------------------------------------------------------------------
    def executeTask(self, taskId):
        """Execute the action of a scheduled task.
        @param taskId: Task id.
        @return: A boolean.
        """
        tasks = self.__scheduler.getTasks()
        for task in tasks:
            if task.getDescription().getId() == taskId:
                task.execute(globals())
                return True
        return False

    # --------------------------------------------------------------------------
    # Remove a task from the scheduler.
    # --------------------------------------------------------------------------
    def removeTask(self, taskId):
        """Remove a task from the scheduler.
        @param taskId: Task id.
        """
        self.__scheduler.removeTask(taskId)

    # --------------------------------------------------------------------------
    # Clear the scheduler.
    # --------------------------------------------------------------------------
    def clear(self):
        """Clear the scheduler.
        """
        self.__scheduler.clear()

# Create an instance of the resource
resourceScheduler = TDSResourceScheduler("resourceScheduler")
# Register the resource into the resources manager
resourcesManager.addResource(resourceScheduler)

# ==============================================================================
# ******************************************************************************
# SERVICES DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the service "tasks_infos".
# ==============================================================================
class TDSServiceSchedulerTasksInfos(TDSService):
    """Get the informations about the tasks.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "tasks_infos"
        self.comment = "Get the informations about the tasks."

    # --------------------------------------------------------------------------
    # Execute the service.
    # --------------------------------------------------------------------------
    def execute(self, id, parameters):
        """Execute the service.
        @param id: Client identifier.
        @param parameters: Request parameters.
        @return: The headers as list and the content dictionary of the request
            answer.
        """
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        tasks = resourceScheduler.getScheduler().getTasks()
        tasksNameList = []
        for task in tasks:
            tasksNameList.append(task.getDescription().getName())
        tasksNameList.sort()
        for i, taskName in enumerate(tasksNameList):
            task = resourceScheduler.getScheduler().getTaskByName(taskName)
            d_name = "data|%.3d" % i
            struct = task.getDictionary()
            contentStruct['root'][d_name] = struct
        return headersStruct, contentStruct

# Register the service into the resource
resourceScheduler.addService(TDSServiceSchedulerTasksInfos)

# ==============================================================================
# Declaration of the service "clear".
# ==============================================================================
class TDSServiceSchedulerClear(TDSService):
    """Clear the scheduler.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "clear"
        self.comment = "Clear the scheduler."

    # --------------------------------------------------------------------------
    # Execute the service.
    # --------------------------------------------------------------------------
    def execute(self, id, parameters):
        """Execute the service.
        @param id: Client identifier.
        @param parameters: Request parameters.
        @return: The headers as list and the content dictionary of the request
            answer.
        """
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceScheduler.clear()
        return headersStruct, contentStruct

# Register the service into the resource
resourceScheduler.addService(TDSServiceSchedulerClear)

# ==============================================================================
# Declaration of the service "remove_task".
# ==============================================================================
class TDSServiceSchedulerRemoveTask(TDSService):
    """Remove a task from the scheduler.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'task_id' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "remove_task"
        self.comment = "Remove a task from the scheduler."

    # --------------------------------------------------------------------------
    # Execute the service.
    # --------------------------------------------------------------------------
    def execute(self, id, parameters):
        """Execute the service.
        @param id: Client identifier.
        @param parameters: Request parameters.
        @return: The headers as list and the content dictionary of the request
            answer.
        """
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceScheduler.removeTask(parameters['task_id'])
        return headersStruct, contentStruct

# Register the service into the resource
resourceScheduler.addService(TDSServiceSchedulerRemoveTask)

# ==============================================================================
# Declaration of the service "execute_task".
# ==============================================================================
class TDSServiceSchedulerExecuteTask(TDSService):
    """Execute the action of a task.
    """

    # --------------------------------------------------------------------------
    # Configure the service.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the service.
        """
        self.parametersDict = {
            'task_id' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "execute_task"
        self.comment = "Execute the action of a task."

    # --------------------------------------------------------------------------
    # Execute the service.
    # --------------------------------------------------------------------------
    def execute(self, id, parameters):
        """Execute the service.
        @param id: Client identifier.
        @param parameters: Request parameters.
        @return: The headers as list and the content dictionary of the request
            answer.
        """
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        if not resourceScheduler.executeTask(parameters['task_id']):
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        return headersStruct, contentStruct

# Register the service into the resource
resourceScheduler.addService(TDSServiceSchedulerExecuteTask)
