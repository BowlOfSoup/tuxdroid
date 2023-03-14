#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import copy

from UgcDescription import UgcDescription
from UgcParameter import UgcParameter
from UgcTask import UgcTask

# ------------------------------------------------------------------------------
# Ugc class.
# ------------------------------------------------------------------------------
class Ugc(object):
    """Ugc class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary, ugcFile, parentGadget):
        """Constructor of the class.
        @param parent: Parent UGCs container.
        @param dictionary: Ugc structure as dictionary.
        @param ugcFile: UGC file name.
        @param parentGadget: Parent Gadget object.
        """
        self.__parent = parent
        # Save the dictionary
        self.__dictionary = dictionary
        # Save the ugc file name
        self.__ugcFile = ugcFile
        # Save the parent gadget object
        self.__parentGadget = parentGadget
        # Creation time of the ugc file
        self.__ugcFileCreationTime = dictionary['creationTime']
        # Alert attitune
        self.__alertAttitune = dictionary['alertAttitune']
        # Create descriptor
        self.__description = UgcDescription(self, dictionary['description'])
        # Create ugc parameters
        self.__checkForLocals(dictionary)
        self.__parameters = []
        if dictionary.has_key('parameters'):
            for key in dictionary['parameters'].keys():
                paramData = dictionary['parameters'][key]
                parameter = UgcParameter(self, paramData)
                self.__parameters.append(parameter)
        # Create ugc tasks
        self.__tasks = []
        if dictionary.has_key('tasks'):
            for key in dictionary['tasks'].keys():
                taskData = dictionary['tasks'][key]
                task = UgcTask(self, taskData)
                self.__tasks.append(task)

    # --------------------------------------------------------------------------
    # Check for locals
    # --------------------------------------------------------------------------
    def __checkForLocals(self, dictionary):
        """Check for locals
        """
        def checkParam(paramName, defaultValue):
            for key in dictionary['parameters'].keys():
                if dictionary['parameters'][key]['name'] == paramName:
                    return
            keyName = "param_%.2d" % len(dictionary['parameters'].keys())
            dictionary['parameters'][keyName] = {
                'name' : paramName,
                'value' : defaultValue,
            }
        if not dictionary.has_key('parameters'):
            return
        checkParam("locutor", self.__parent.getLocutor().replace("8k", ""))
        checkParam("pitch", self.__parent.getPitch())
        checkParam("language", self.__parent.getLanguage())
        checkParam("country", self.__parent.getCountry())

    # --------------------------------------------------------------------------
    # Get the data of the Ugc as dictionary.
    # --------------------------------------------------------------------------
    def getData(self, language):
        """Get the data of the Ugc as dictionary.
        @return a dictionary.
        """
        data = {}
        # Alert attitune
        data['alertAttitune'] = self.__alertAttitune
        # Description
        description = self.getDescription()
        parentDescription = self.getParentGadget().getDescription()
        data['description'] = {}
        data['description']['name'] = description.getName()
        data['description']['translatedName'] = description.getName()
        data['description']['ttsName'] = description.getTtsName()
        data['description']['uuid'] = description.getUuid()
        data['description']['version'] = parentDescription.getUuid()
        data['description']['author'] = parentDescription.getAuthor()
        data['description']['description'] = parentDescription.getDescription(language)
        data['description']['platform'] = parentDescription.getPlatform()
        data['description']['category'] = parentDescription.getCategory()
        data['description']['defaultLanguage'] = parentDescription.getDefaultLanguage()
        data['description']['onDemandIsAble'] = parentDescription.onDemandIsAble()
        data['description']['onDemandIsActivated'] = description.onDemandIsActivated()
        try:
            f = open(parentDescription.getHelpFile(language), "rb")
            try:
                helpContent = f.read()
            finally:
                f.close()
        except:
            helpContent = ""
        data['description']['helpFile'] = helpContent
        data['description']['iconFile'] = "/%s/icon.png" % parentDescription.getUuid()
        data['description']['workingPath'] = self.getParentGadget().getWorkingPath()
        data['description']['ugcFile'] = self.getUgcFile()
        ugcName = os.path.split(self.getUgcFile())[-1]
        ugcDlUrl = '/ugcs/%s' % ugcName
        data['description']['ugcUrl'] = ugcDlUrl
        data['description']['parentPluginName'] = self.getParentGadget().getParentPlugin().getDescription().getTranslatedName(language)
        data['description']['parentPluginUuid'] = self.getParentGadget().getParentPlugin().getDescription().getUuid()
        data['description']['parentGadgetName'] = self.getParentGadget().getDescription().getTranslatedName(language)
        data['description']['parentGadgetUuid'] = self.getParentGadget().getDescription().getUuid()
        data['defaultRunCommand'] = self.getDefaultRunCommandName()
        data['defaultCheckCommand'] = self.getDefaultCheckCommandName()
        # Parameters
        data['parameters'] = {}
        parentParameters = self.getParentGadget().getParameters()
        for i, parentParameter in enumerate(parentParameters):
            nodeName = "parameter_%.3d" % i
            data['parameters'][nodeName] = {}
            data['parameters'][nodeName]['name'] = parentParameter.getName()
            data['parameters'][nodeName]['translatedName'] = parentParameter.getTranslatedName(language)
            data['parameters'][nodeName]['description'] = parentParameter.getDescription(language)
            data['parameters'][nodeName]['platform'] = parentParameter.getPlatform()
            data['parameters'][nodeName]['category'] = parentParameter.getCategory()
            data['parameters'][nodeName]['type'] = parentParameter.getType()
            parameter = self.getParameter(parentParameter.getName())
            if parameter != None:
                if parameter.getValue() != parentParameter.getDefaultValue():
                    data['parameters'][nodeName]['defaultValue'] = parameter.getValue()
                else:
                    data['parameters'][nodeName]['defaultValue'] = parentParameter.getDefaultValue(language)
            else:
                data['parameters'][nodeName]['defaultValue'] = parentParameter.getDefaultValue(language)
            data['parameters'][nodeName]['enumValues'] = parentParameter.getEnumValues(language)
            # Hack for 'locutor' parameter. Locutors list is dynamique and depends
            # Of the dongle plug and Tuxosl states.
            if parentParameter.getName() == 'locutor':
                # Get the current locutors list from tuxosl
                locutorsList = self.getParentGadget().getParentPlugin().getContainer().getLocutorsList()
                # Insert the selected locutor
                selectedLocutor = data['parameters'][nodeName]['defaultValue']
                if not selectedLocutor in locutorsList:
                    locutorsList.append(selectedLocutor)
                locutorsStr = ""
                for locutor in locutorsList:
                    if len(locutorsStr) != 0:
                        locutorsStr += ","
                    locutorsStr += locutor
                data['parameters'][nodeName]['enumValues'] = locutorsStr
            data['parameters'][nodeName]['minValue'] = parentParameter.getMinValue()
            data['parameters'][nodeName]['maxValue'] = parentParameter.getMaxValue()
            data['parameters'][nodeName]['stepValue'] = parentParameter.getStepValue()
            data['parameters'][nodeName]['visible'] = parentParameter.isVisible()
            data['parameters'][nodeName]['filters'] = parentParameter.getFilters()
            data['parameters'][nodeName]['task'] = parentParameter.getTask()
        # Serialize values of enumerated parameters
        for key in data['parameters']:
            param = data['parameters'][key]
            if param['type'] in ['enum', 'booleans']:
                values = param['enumValues'].split(",")
                enums = {}
                for i, value in enumerate(values):
                    dName = "enum_%.2d" % i
                    if value != '':
                        enums[dName] = value.strip()
                param['enumValues'] = enums
        # Commands
        data['commands'] = {}
        commands = self.__parentGadget.getCommands()
        for i, command in enumerate(commands):
            nodeName = "command_%.3d" % i
            data['commands'][nodeName] = {}
            data['commands'][nodeName]['name'] = command.getName()
            data['commands'][nodeName]['translatedName'] = command.getTranslatedName(language)
            data['commands'][nodeName]['description'] = command.getDescription(language)
            data['commands'][nodeName]['isDaemon'] = command.isDaemon()
        # Tasks
        data['tasks'] = {}
        parentTasks = self.getParentGadget().getTasks()
        for i, parentTask in enumerate(parentTasks):
            nodeName = "task_%.3d" % i
            task = self.getTask(parentTask.getName())
            data['tasks'][nodeName] = {}
            data['tasks'][nodeName]['name'] = parentTask.getName()
            data['tasks'][nodeName]['translatedName'] = parentTask.getTranslatedName(language)
            data['tasks'][nodeName]['description'] = parentTask.getDescription(language)
            data['tasks'][nodeName]['command'] = parentTask.getCommand()
            data['tasks'][nodeName]['type'] = parentTask.getType()
            if task != None:
                data['tasks'][nodeName]['activated'] = task.isActivated()
            else:
                data['tasks'][nodeName]['activated'] = parentTask.isActivated()
            if task != None:
                data['tasks'][nodeName]['weekMask'] = task.getWeekMaskDict()
            else:
                data['tasks'][nodeName]['weekMask'] = parentTask.getWeekMaskDict()
            data['tasks'][nodeName]['weekMaskType'] = parentTask.getWeekMaskType()
            data['tasks'][nodeName]['weekMaskVisible'] = parentTask.getWeekMaskIsVisible()
            if task != None:
                data['tasks'][nodeName]['date'] = task.getDateDict()
            else:
                data['tasks'][nodeName]['date'] = parentTask.getDateDict()
            data['tasks'][nodeName]['dateVisible'] = parentTask.getDateIsVisible()
            if task != None:
                data['tasks'][nodeName]['hoursBegin'] = task.getTimeDict(task.getHoursBegin())
            else:
                data['tasks'][nodeName]['hoursBegin'] = parentTask.getTimeDict(parentTask.getHoursBegin())
            data['tasks'][nodeName]['hoursBeginMask'] = parentTask.getTimeMaskDict(parentTask.getHoursBeginMask())
            data['tasks'][nodeName]['hoursBeginVisible'] = parentTask.getHoursBeginIsVisible()
            if task != None:
                data['tasks'][nodeName]['hoursEnd'] = task.getTimeDict(task.getHoursEnd())
            else:
                data['tasks'][nodeName]['hoursEnd'] = parentTask.getTimeDict(parentTask.getHoursEnd())
            data['tasks'][nodeName]['hoursEndMask'] = parentTask.getTimeMaskDict(parentTask.getHoursEndMask())
            data['tasks'][nodeName]['hoursEndVisible'] = parentTask.getHoursEndIsVisible()
            if task != None:
                data['tasks'][nodeName]['delay'] = task.getTimeDict(task.getDelay())
            else:
                data['tasks'][nodeName]['delay'] = parentTask.getTimeDict(parentTask.getDelay())
            data['tasks'][nodeName]['delayType'] = parentTask.getDelayType()
            data['tasks'][nodeName]['delayMask'] = parentTask.getTimeMaskDict(parentTask.getDelayMask())
            data['tasks'][nodeName]['delayVisible'] = parentTask.getDelayIsVisible()
            data['tasks'][nodeName]['parameters'] = {}
            for key in data['parameters'].keys():
                if data['parameters'][key]['task'] == data['tasks'][nodeName]['name']:
                    data['tasks'][nodeName]['parameters'][key] = data['parameters'][key]
                    del data['parameters'][key]
        for key in data['parameters'].keys():
            if data['parameters'][key]['task'] != "none":
                data['parameters'][key]['visible'] = False
        return data

    # --------------------------------------------------------------------------
    # Get the parent gadget.
    # --------------------------------------------------------------------------
    def getParentGadget(self):
        """Get the parent gadget.
        @return: A Gadget object.
        """
        return self.__parentGadget

    # --------------------------------------------------------------------------
    # Set the parent gadget.
    # --------------------------------------------------------------------------
    def setParentGadget(self, parentGadget):
        """Set the parent gadget.
        @param parentGadget: The parent gagdet.
        """
        self.__parentGadget = parentGadget

    # --------------------------------------------------------------------------
    # Get the ugc dictionary.
    # --------------------------------------------------------------------------
    def getDictionary(self):
        """Get the ugc dictionary.
        @return: A dictionary.
        """
        return self.__dictionary

    # --------------------------------------------------------------------------
    # Get the UGC file.
    # --------------------------------------------------------------------------
    def getUgcFile(self):
        """Get the SCG file.
        @return: A string.
        """
        return self.__ugcFile

    # --------------------------------------------------------------------------
    # Set the creation time of the ugc file.
    # --------------------------------------------------------------------------
    def setUgcFileCreationTime(self, value):
        """Set the creation time of the ugc file.
        @param value: A float.
        """
        self.__ugcFileCreationTime = value

    # --------------------------------------------------------------------------
    # Get the creation time of the ugc file.
    # --------------------------------------------------------------------------
    def getUgcFileCreationTime(self):
        """Get the creation time of the ugc file.
        @return: A float.
        """
        return self.__ugcFileCreationTime

    # --------------------------------------------------------------------------
    # Get the selected attitune for alerts introduction.
    # --------------------------------------------------------------------------
    def getAlertAttitune(self):
        """Get the selected attitune for alerts introduction.
        @return: A string.
        """
        return self.__alertAttitune

    # --------------------------------------------------------------------------
    # Get the parent UGCs container.
    # --------------------------------------------------------------------------
    def getContainer(self):
        """Get the parent UGCs container.
        @return: The parent UGCs container.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Get the UGC description object.
    # --------------------------------------------------------------------------
    def getDescription(self):
        """Get the UGC description object.
        @return: The UgcDescription object.
        """
        return self.__description

    # --------------------------------------------------------------------------
    # Get the UGC commands objects list.
    # --------------------------------------------------------------------------
    def getCommands(self):
        """Get the UGC command objects list.
        @return: The UGC commands objects list.
        """
        return self.__parentGadget.getCommands()

    # --------------------------------------------------------------------------
    # Get a command object by it name.
    # --------------------------------------------------------------------------
    def getCommand(self, commandName):
        """Get a command object by it name.
        @param commandName: The name of the command.
        @return: The command object as PluginCommand or None.
        """
        for command in self.__parentGadget.getCommands():
            if command.getName().lower() == commandName:
                return command
        return None

    # --------------------------------------------------------------------------
    # Get the commands name list.
    # --------------------------------------------------------------------------
    def getCommandsName(self):
        """Get the commands name list.
        @return: A list of strings.
        """
        result = []
        for command in self.__parentGadget.getCommands():
            result.append(command.getName())
        return result

    # --------------------------------------------------------------------------
    # Get the UGC tasks objects list.
    # --------------------------------------------------------------------------
    def getTasks(self):
        """Get the UGC tasks objects list.
        @return: The UgcTasks objects list.
        """
        return self.__tasks

    # --------------------------------------------------------------------------
    # Get a task object by it name.
    # --------------------------------------------------------------------------
    def getTask(self, taskName):
        """Get a task object by it name.
        @param taskName: The name of the task.
        @return: The task object as UgcTask or None.
        """
        for task in self.__tasks:
            if task.getName() == taskName:
                return task
        return None

    # --------------------------------------------------------------------------
    # Get the tasks name list.
    # --------------------------------------------------------------------------
    def getTasksName(self):
        """Get the tasks name list.
        @return: A list of strings.
        """
        result = []
        for task in self.__tasks:
            result.append(task.getName())
        return result

    # --------------------------------------------------------------------------
    # Get the default check command name.
    # --------------------------------------------------------------------------
    def getDefaultCheckCommandName(self):
        """Get the default check command name.
        @return: A string.
        """
        return self.__parentGadget.getDefaultCheckCommandName()

    # --------------------------------------------------------------------------
    # Get the default run command name.
    # --------------------------------------------------------------------------
    def getDefaultRunCommandName(self):
        """Get the default run command name.
        @return: A string.
        """
        return self.__parentGadget.getDefaultRunCommandName()

    # --------------------------------------------------------------------------
    # Get the parameter objects list.
    # --------------------------------------------------------------------------
    def getParameters(self):
        """Get the parameter objects list.
        @return: The parameter objects list.
        """
        return self.__parameters

    # --------------------------------------------------------------------------
    # Get a parameter object by it name.
    # --------------------------------------------------------------------------
    def getParameter(self, parameterName):
        """Get a parameter object by it name.
        @param parameterName: The name of the parameter.
        @return: The UgcParameter object or None.
        """
        for parameter in self.__parameters:
            if parameter.getName() == parameterName:
                return parameter
        return None

    # --------------------------------------------------------------------------
    # Get the parameters name list.
    # --------------------------------------------------------------------------
    def getParametersName(self):
        """Get the parameters name list.
        @return: A list of strings.
        """
        result = []
        for parameter in self.__parameters:
            result.append(parameter.getName())
        return result

    # ==========================================================================
    # Ugc execution
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Start this Ugc.
    # --------------------------------------------------------------------------
    def start(self, command, parameters = {}):
        """Start this Ugc.
        @param command: Command name to start the Ugc.
        @param parameters: Parameters of the ugc as dictionary.
        @return: The success of the ugc starting.
        - When the parameters are not defined the ugc is started with the
        default ones.
        - If a parameter is wrong the default one is set.
        - If a parameter is missing the default one is set.
        """
        myParameters = {}
        for parameter in self.getParameters():
            if parameters.has_key(parameter.getName()):
                myParameters[parameter.getName()] = parameters[parameter.getName()]
            else:
                myParameters[parameter.getName()] = parameter.getValue()
        myParameters['uuid'] = self.getDescription().getUuid()
        for key in parameters.keys():
            if not myParameters.has_key(key):
                myParameters[key] = parameters[key]
        if not myParameters.has_key("language"):
            myParameters["language"] = self.__parent.getLanguage()
        if not myParameters.has_key("locutor"):
            myParameters["locutor"] = self.__parent.getLocutor()
        if not myParameters.has_key("pitch"):
            myParameters["pitch"] = self.__parent.getPitch()
        if not myParameters.has_key("country"):
            myParameters["country"] = self.__parent.getCountry()
        return self.__parentGadget.start(command, myParameters)

    # --------------------------------------------------------------------------
    # Stop the Ugc.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the Ugc.
        """
        self.__parentGadget.stop()

    # --------------------------------------------------------------------------
    # Send event to the UGC. (Daemon mode)
    # --------------------------------------------------------------------------
    def sendEvent(self, eventName, eventValues = []):
        """Send event to the UGC. (Daemon mode)
        @eventName: Event name.
        @eventValues: Event values list.
        """
        self.__parentGadget.sendEvent(eventName, eventValues)
