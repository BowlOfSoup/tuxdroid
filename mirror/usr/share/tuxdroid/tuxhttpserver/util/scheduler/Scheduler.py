#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import datetime
import threading
import time
import random

try:
    from hashlib import md5
except:
    from md5 import md5

from Task import Task

TASK_NEXT_TIME = 0
TASK_OBJECT = 1
TASK_ID = 2
TASK_NAME = 3

# ------------------------------------------------------------------------------
# Scheduler task manager.
# ------------------------------------------------------------------------------
class Scheduler(object):
    """Scheduler task manager.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, appGlobals):
        """Constructor.
        """
        self.__started = False
        self.__startedMutex = threading.Lock()
        self.__tasksToExecuteStack = []
        self.__tasksToExecuteStackMutex = threading.Lock()
        self.__appGlobals = appGlobals
        self.__onTaskAddedCallback = None
        self.__onTaskRemovedCallback = None
        self.__onTasksLoaded = None
        self.__onTasksUnloaded = None
        self.__tasksDirectory = None
        self.__tasksLoaded = False
        self.__tasksLoadedMutex = threading.Lock()

    # --------------------------------------------------------------------------
    # Load tasks from a directory.
    # --------------------------------------------------------------------------
    def loadTasks(self, directory):
        """Load tasks from a directory.
        @param directory: Directory where to search the task configurations.
        """
        if not os.path.isdir(directory):
            return
        self.__tasksDirectory = directory
        self.__tasksToExecuteStackMutex.acquire()
        self.__tasksToExecuteStack = []
        self.__tasksToExecuteStackMutex.release()
        self.__setTasksLoaded(False)
        files = os.listdir(directory)
        for file in files:
            filePath = os.path.join(directory, file)
            task = Task.load(filePath)
            if task == None:
                try:
                    os.remove(filePath)
                except:
                    pass
            else:
                id, name = self.insertTask(task, task.getDescription().getName(),
                    task.getDescription().getId())
                if id == None:
                    try:
                        os.remove(filePath)
                    except:
                        pass
        self.__setTasksLoaded(True)

    # --------------------------------------------------------------------------
    # Store tasks in a directory.
    # --------------------------------------------------------------------------
    def storeTasks(self):
        """Store tasks in a directory.
        """
        if self.__tasksDirectory == None:
            return
        # Get stored task fileNames list
        files = os.listdir(self.__tasksDirectory)
        for i, file in enumerate(files):
            if file.lower().rfind(".tcf") != len(file) - 4:
                files.remove(file)
            else:
                files[i] = file[:-4]
        self.__tasksToExecuteStackMutex.acquire()
        # Remove orphan configurations
        for file in files:
            isFound = False
            for taskInfo in self.__tasksToExecuteStack:
                if taskInfo[TASK_OBJECT].getDescription().getId() == file:
                    isFound = True
                    break
            if not isFound:
                try:
                    os.remove(os.path.join(self.__tasksDirectory, file + ".tcf"))
                except:
                    pass
        # Store task configurations
        for taskInfo in self.__tasksToExecuteStack:
            if not taskInfo[TASK_OBJECT].isStorable():
                continue
            isFound = False
            for file in files:
                if taskInfo[TASK_OBJECT].getDescription().getId() == file:
                    isFound = True
                    break
            if not isFound:
                Task.store(taskInfo[TASK_OBJECT], self.__tasksDirectory)
        self.__tasksToExecuteStackMutex.release()

    # --------------------------------------------------------------------------
    # Start the scheduler.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the scheduler.
        """
        t = threading.Thread(target = self.__tasksCheckerLoop)
        t.start()

    # --------------------------------------------------------------------------
    # Stop the scheduler.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the scheduler.
        """
        self.__setStarted(False)

    # --------------------------------------------------------------------------
    # Get if the scheduler is started or not.
    # --------------------------------------------------------------------------
    def isStarted(self):
        """Get if the scheduler is started or not.
        @return: True or False.
        """
        self.__startedMutex.acquire()
        result = self.__started
        self.__startedMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set the started flag of the scheduler.
    # --------------------------------------------------------------------------
    def __setStarted(self, value):
        """Set the started flag of the scheduler.
        @param value: True or False.
        """
        self.__startedMutex.acquire()
        self.__started = value
        self.__startedMutex.release()

    # --------------------------------------------------------------------------
    # Get if the tasks are loaded or not.
    # --------------------------------------------------------------------------
    def tasksAreLoaded(self):
        """Get if the tasks are loaded or not.
        @return: True or False
        """
        self.__tasksLoadedMutex.acquire()
        result = self.__tasksLoaded
        self.__tasksLoadedMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Set if the tasks are loaded or not.
    # --------------------------------------------------------------------------
    def __setTasksLoaded(self, value):
        """Set if the tasks are loaded or not.
        @param value: True or False
        """
        self.__tasksLoadedMutex.acquire()
        self.__tasksLoaded = value
        self.__tasksLoadedMutex.release()
        if value:
            if self.__onTasksLoadedCallback != None:
                self.__onTasksLoadedCallback()
        else:
            if self.__onTasksUnloadedCallback != None:
                self.__onTasksUnloadedCallback()

    # --------------------------------------------------------------------------
    # Generate a single id.
    # --------------------------------------------------------------------------
    def __generateSingleId(self, baseString = None):
        """Generate a single id.
        @baseString: Base string. (default None)
        @return: The single id.
        """
        if baseString == None:
            baseString = str(time.time() + random.random())
        md5H = md5()
        md5H.update(baseString)
        id = md5H.hexdigest()
        return id

    # --------------------------------------------------------------------------
    # This method generate a single task name from the taskName argument.
    # --------------------------------------------------------------------------
    def __generateSingleName(self, taskName):
        """This method generate a single task name from the taskName argument.
        @param taskName: Base task name.
        @return: A single task name.
        If the taskName is already not existing in the scheduler, the method
        return it.
        """
        def checkNameExists(taskNameToCheck):
            result = False
            self.__tasksToExecuteStackMutex.acquire()
            for taskInfo in self.__tasksToExecuteStack:
                if taskInfo[TASK_NAME] == taskNameToCheck:
                    result = True
                    break
            self.__tasksToExecuteStackMutex.release()
            return result
        baseTaskName = taskName
        if (baseTaskName.find("(") > 0) and (baseTaskName.find(")") != -1):
            baseTaskName = baseTaskName[:baseTaskName.find("(") - 1]
        if baseTaskName == "":
            baseTaskName = "Default"
        i = 0
        while checkNameExists(taskName):
            i += 1
            taskName = "%s (%d)" % (baseTaskName, i)
        return taskName

    # --------------------------------------------------------------------------
    # Insert a task in the scheduler.
    # --------------------------------------------------------------------------
    def insertTask(self, task, name, id = None):
        """Insert a task in the scheduler.
        @param task: Task object.
        @return: The task identifier and the task name or None None if fail.
        """
        nextTime = task.getNextExecuteTime()
        if id == None:
            id = self.__generateSingleId()
        name = self.__generateSingleName(name)
        self.__tasksToExecuteStackMutex.acquire()
        if nextTime != None:
            task.getDescription().setId(id)
            task.getDescription().setName(name)
            self.__tasksToExecuteStack.append([nextTime, task, id, name])
            resultId = id
            resultName = name
        else:
            resultId = None
            resultName = None
        self.__tasksToExecuteStackMutex.release()
        if resultId != None:
            if self.tasksAreLoaded():
                self.storeTasks()
                if self.__onTaskAddedCallback != None:
                    self.__onTaskAddedCallback(task)
                if self.__onTasksLoadedCallback != None:
                    self.__onTasksLoadedCallback()
        return resultId, resultName

    # --------------------------------------------------------------------------
    # Get the number of tasks contained in the scheduler.
    # --------------------------------------------------------------------------
    def getTasksCount(self):
        """Get the number of tasks contained in the scheduler.
        @return: An integer.
        """
        self.__tasksToExecuteStackMutex.acquire()
        result = len(self.__tasksToExecuteStack)
        self.__tasksToExecuteStackMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get the tasks contained in the scheduler.
    # --------------------------------------------------------------------------
    def getTasks(self):
        """Get the tasks contained in the scheduler.
        @return: A list of Task objects.
        """
        result = []
        self.__tasksToExecuteStackMutex.acquire()
        for taskInfo in self.__tasksToExecuteStack:
            result.append(taskInfo[TASK_OBJECT])
        self.__tasksToExecuteStackMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get a task by its name.
    # --------------------------------------------------------------------------
    def getTaskByName(self, taskName):
        """Get a task by its name.
        @param taskName: Task name.
        @return: The task object.
        """
        task = None
        self.__tasksToExecuteStackMutex.acquire()
        for taskInfo in self.__tasksToExecuteStack:
            if taskInfo[TASK_NAME] == taskName:
                task = taskInfo[TASK_OBJECT]
                break
        self.__tasksToExecuteStackMutex.release()
        return task

    # --------------------------------------------------------------------------
    # Remove a task from the scheduler by its identifier.
    # --------------------------------------------------------------------------
    def removeTaskById(self, taskId):
        """Remove a task from the scheduler by its identifier.
        @param taskId: Task identifier.
        """
        task = None
        self.__tasksToExecuteStackMutex.acquire()
        for taskInfo in self.__tasksToExecuteStack:
            if taskInfo[TASK_ID] == taskId:
                self.__tasksToExecuteStack.remove(taskInfo)
                task = taskInfo[TASK_OBJECT]
                break
        self.__tasksToExecuteStackMutex.release()
        if task != None:
            self.storeTasks()
            if self.tasksAreLoaded():
                if self.__onTaskRemovedCallback != None:
                    self.__onTaskRemovedCallback(task)
                if self.__onTasksLoadedCallback != None:
                    self.__onTasksLoadedCallback()

    # --------------------------------------------------------------------------
    # Remove a task from the scheduler by its name.
    # --------------------------------------------------------------------------
    def removeTaskByName(self, taskName):
        """Remove a task from the scheduler by its name.
        @param taskName: Task name.
        """
        task = None
        self.__tasksToExecuteStackMutex.acquire()
        for taskInfo in self.__tasksToExecuteStack:
            if taskInfo[TASK_NAME] == taskName:
                self.__tasksToExecuteStack.remove(taskInfo)
                task = taskInfo[TASK_OBJECT]
                break
        self.__tasksToExecuteStackMutex.release()
        if task != None:
            self.storeTasks()
            if self.tasksAreLoaded():
                if self.__onTaskRemovedCallback != None:
                    self.__onTaskRemovedCallback(task)
                if self.__onTasksLoadedCallback != None:
                    self.__onTasksLoadedCallback()

    # --------------------------------------------------------------------------
    # Remove a task from the scheduler.
    # --------------------------------------------------------------------------
    def removeTask(self, taskId):
        """Remove a task from the scheduler.
        @param taskId: Task identifier.
        """
        self.removeTaskById(taskId)

    # --------------------------------------------------------------------------
    # Clear the scheduler.
    # --------------------------------------------------------------------------
    def clear(self):
        """Clear the scheduler.
        """
        self.__tasksToExecuteStackMutex.acquire()
        self.__tasksToExecuteStack = []
        self.__tasksToExecuteStackMutex.release()
        self.__setTasksLoaded(False)
        self.storeTasks()
        self.__setTasksLoaded(True)

    # --------------------------------------------------------------------------
    # Set the on task added event callback.
    # --------------------------------------------------------------------------
    def setOnTaskAddedCallback(self, funct):
        """Set the on task added event callback.
        @param funct: Function pointer.
        Function prototype:
        def onTaskAdded(self, task):
            pass
        """
        self.__onTaskAddedCallback = funct

    # --------------------------------------------------------------------------
    # Set the on task removed event callback.
    # --------------------------------------------------------------------------
    def setOnTaskRemovedCallback(self, funct):
        """Set the on task removed event callback.
        @param funct: Function pointer.
        Function prototype:
        def onTaskRemoved(self, task):
            pass
        """
        self.__onTaskRemovedCallback = funct

    # --------------------------------------------------------------------------
    # Set the on tasks loaded event callback.
    # --------------------------------------------------------------------------
    def setOnTasksLoadedCallback(self, funct):
        """Set the on tasks loaded event callback.
        @param funct: Function pointer.
        Function prototype:
        def onTasksLoaded(self):
            pass
        """
        self.__onTasksLoadedCallback = funct

    # --------------------------------------------------------------------------
    # Set the on tasks unloaded event callback.
    # --------------------------------------------------------------------------
    def setOnTasksUnloadedCallback(self, funct):
        """Set the on tasks unloaded event callback.
        @param funct: Function pointer.
        Function prototype:
        def onTasksUnloaded(self):
            pass
        """
        self.__onTasksUnloadedCallback = funct

    # --------------------------------------------------------------------------
    # Loop of the tasks checker.
    # --------------------------------------------------------------------------
    def __tasksCheckerLoop(self):
        """Loop of the tasks checker.
        """
        if self.isStarted():
            return
        self.__setTasksLoaded(True)
        self.__setStarted(True)
        while self.isStarted():
            now = datetime.datetime.now()
            tasksToRemove = []
            tasksToAdd = []
            tasksFinished = []
            self.__tasksToExecuteStackMutex.acquire()
            for taskInfo in self.__tasksToExecuteStack:
                if now > taskInfo[TASK_NEXT_TIME]:
                    tasksToRemove.append(taskInfo)
                    nextTime = taskInfo[TASK_OBJECT].getNextExecuteTime()
                    diff = now - taskInfo[TASK_NEXT_TIME]
                    if diff.seconds <= 30:
                        taskInfo[TASK_OBJECT].execute(self.__appGlobals)
                    if nextTime != None:
                        tasksToAdd.append([nextTime, taskInfo[TASK_OBJECT],
                            taskInfo[TASK_ID], taskInfo[TASK_NAME]])
                    else:
                        tasksFinished.append(taskInfo[TASK_OBJECT])
            for taskInfo in tasksToRemove:
                self.__tasksToExecuteStack.remove(taskInfo)
            for taskInfo in tasksToAdd:
                self.__tasksToExecuteStack.append(taskInfo)
            self.__tasksToExecuteStackMutex.release()
            for task in tasksFinished:
                if self.__onTaskRemovedCallback != None:
                    self.__onTaskRemovedCallback(task)
            if len(tasksFinished) > 0:
                self.storeTasks()
                if self.__onTasksLoadedCallback != None:
                    self.__onTasksLoadedCallback()
            time.sleep(0.5)
        self.__setTasksLoaded(False)
