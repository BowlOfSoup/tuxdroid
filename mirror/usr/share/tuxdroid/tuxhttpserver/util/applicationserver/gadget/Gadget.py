#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import copy

from util.i18n.I18n import I18n
from util.applicationserver.plugin.PluginParameter import PluginParameter
from util.applicationserver.plugin.PluginTask import PluginTask
from util.applicationserver.plugin.Plugin import SUPPORTED_LANGUAGES_LIST

from GadgetDescription import GadgetDescription

# ------------------------------------------------------------------------------
# Gadget class.
# ------------------------------------------------------------------------------
class Gadget(object):
    """Gadget class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary, scgFile, workingPath, parentPlugin):
        """Constructor of the class.
        @param parent: Parent gadgets container.
        @param dictionary: Gadget structure as dictionary.
        @param scgFile: SCG file name of the gadget.
        @param workingPath: Working path of the gadget.
        @param parentPlugin: Parent plugin of the gadget.
        """
        self.__parent = parent
        # Save the dictionary
        self.__dictionary = dictionary
        # Save the working path
        self.__workingPath = workingPath
        # Save the scg file name
        self.__scgFile = scgFile
        # Save the parent plugin object
        self.__parentPlugin = parentPlugin
        # Create i18n table
        self.__i18nList = {}
        self.__updateI18nList()
        # Create descriptor
        self.__description = GadgetDescription(self, dictionary['description'],
            self.__workingPath)
        # Create parameters
        self.__parameters = []
        # Copy the parameters list of the parent plugin
        for plgParameter in self.__parentPlugin.getParameters():
            gadgetParameter = PluginParameter(self.__parentPlugin,
                copy.deepcopy(plgParameter.getDictionary()))
            paramPlatform = gadgetParameter.getPlatform()
            if paramPlatform != "all":
                if paramPlatform == "windows":
                    if os.name != "nt":
                        gadgetParameter.setVisible('false')
                else:
                    if os.name == "nt":
                        gadgetParameter.setVisible('false')
            # Set gadget as parent for translations
            gadgetParameter.setParentForTranslations(self)
            self.__parameters.append(gadgetParameter)
        # Set the default value and visibility of the parameters
        if dictionary.has_key('parameters'):
            keys = dictionary['parameters'].keys()
            keys.sort()
            for key in keys:
                paramData = dictionary['parameters'][key]
                parameter = self.getParameter(paramData['name'])
                if parameter != None:
                    parameter.setDefaultValue(paramData['defaultValue'])
                    parameter.setVisible(paramData['visible'])
        # Create tasks
        self.__tasks = []
        if dictionary.has_key('tasks'):
            for key in dictionary['tasks'].keys():
                taskData = dictionary['tasks'][key]
                plgTask = self.__parentPlugin.getTask(taskData['name'])
                if plgTask != None:
                    plgTaskDict = copy.deepcopy(plgTask.getDictionary())
                    plgTaskDict['activated'] = taskData['activated']
                    plgTaskDict['date'] = taskData['date']
                    plgTaskDict['weekMask'] = taskData['weekMask']
                    plgTaskDict['hoursBegin'] = taskData['hoursBegin']
                    plgTaskDict['hoursEnd'] = taskData['hoursEnd']
                    plgTaskDict['delay'] = taskData['delay']
                    self.__tasks.append(PluginTask(self.__parentPlugin,
                        plgTaskDict))

    # --------------------------------------------------------------------------
    # Get the parent plugin.
    # --------------------------------------------------------------------------
    def getParentPlugin(self):
        """Get the parent plugin.
        @return: A Plugin object.
        """
        return self.__parentPlugin

    # --------------------------------------------------------------------------
    # Get the gadget dictionary.
    # --------------------------------------------------------------------------
    def getDictionary(self):
        """Get the gadget dictionary.
        @return: A dictionary.
        """
        return self.__dictionary

    # --------------------------------------------------------------------------
    # Get the data of the gadget as dictionary.
    # --------------------------------------------------------------------------
    def getData(self, language):
        """Get the data of the gadget as dictionary.
        @return a dictionary.
        """
        data = {}
        # Description
        description = self.getDescription()
        data['description'] = {}
        data['description']['name'] = description.getName()
        data['description']['translatedName'] = description.getTranslatedName(language)
        data['description']['ttsName'] = description.getTtsName(language)
        data['description']['uuid'] = description.getUuid()
        data['description']['version'] = description.getVersion()
        data['description']['author'] = description.getAuthor()
        data['description']['description'] = description.getDescription(language)
        data['description']['platform'] = description.getPlatform()
        data['description']['category'] = description.getCategory()
        data['description']['defaultLanguage'] = description.getDefaultLanguage()
        data['description']['onDemandIsAble'] = description.onDemandIsAble()
        try:
            f = open(description.getHelpFile(language), "rb")
            try:
                helpContent = f.read()
            finally:
                f.close()
        except:
            helpContent = ""
        data['description']['helpFile'] = helpContent
        data['description']['iconFile'] = "/%s/icon.png" % description.getUuid()
        data['description']['workingPath'] = self.getWorkingPath()
        data['description']['scgFile'] = self.getScgFile()
        scgName = os.path.split(self.getScgFile())[-1]
        gadgetDlUrl = '/gadgets/%s' % scgName
        data['description']['scgUrl'] = gadgetDlUrl
        data['description']['parentPluginName'] = self.__parentPlugin.getDescription().getTranslatedName(language)
        data['description']['parentPluginUuid'] = self.__parentPlugin.getDescription().getUuid()
        data['defaultRunCommand'] = self.__parentPlugin.getDefaultRunCommandName()
        data['defaultCheckCommand'] = self.__parentPlugin.getDefaultCheckCommandName()
        # Parameters
        data['parameters'] = {}
        parameters = self.getParameters()
        for i, parameter in enumerate(parameters):
            nodeName = "parameter_%.3d" % i
            data['parameters'][nodeName] = {}
            data['parameters'][nodeName]['name'] = parameter.getName()
            data['parameters'][nodeName]['translatedName'] = parameter.getTranslatedName(language)
            data['parameters'][nodeName]['description'] = parameter.getDescription(language)
            data['parameters'][nodeName]['platform'] = parameter.getPlatform()
            data['parameters'][nodeName]['category'] = parameter.getCategory()
            data['parameters'][nodeName]['type'] = parameter.getType()
            data['parameters'][nodeName]['defaultValue'] = parameter.getDefaultValue(language)
            data['parameters'][nodeName]['enumValues'] = parameter.getEnumValues(language)
            data['parameters'][nodeName]['minValue'] = parameter.getMinValue()
            data['parameters'][nodeName]['maxValue'] = parameter.getMaxValue()
            data['parameters'][nodeName]['stepValue'] = parameter.getStepValue()
            data['parameters'][nodeName]['visible'] = parameter.isVisible()
            data['parameters'][nodeName]['filters'] = parameter.getFilters()
            data['parameters'][nodeName]['task'] = parameter.getTask()
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
        commands = self.__parentPlugin.getCommands()
        for i, command in enumerate(commands):
            nodeName = "command_%.3d" % i
            data['commands'][nodeName] = {}
            data['commands'][nodeName]['name'] = command.getName()
            data['commands'][nodeName]['translatedName'] = command.getTranslatedName(language)
            data['commands'][nodeName]['description'] = command.getDescription(language)
            data['commands'][nodeName]['isDaemon'] = command.isDaemon()
        # Tasks
        data['tasks'] = {}
        tasks = self.getTasks()
        for i, task in enumerate(tasks):
            nodeName = "task_%.3d" % i
            data['tasks'][nodeName] = {}
            data['tasks'][nodeName]['name'] = task.getName()
            data['tasks'][nodeName]['translatedName'] = task.getTranslatedName(language)
            data['tasks'][nodeName]['description'] = task.getDescription(language)
            data['tasks'][nodeName]['command'] = task.getCommand()
            data['tasks'][nodeName]['type'] = task.getType()
            data['tasks'][nodeName]['activated'] = task.isActivated()
            data['tasks'][nodeName]['weekMask'] = task.getWeekMaskDict()
            data['tasks'][nodeName]['weekMaskType'] = task.getWeekMaskType()
            data['tasks'][nodeName]['weekMaskVisible'] = task.getWeekMaskIsVisible()
            data['tasks'][nodeName]['date'] = task.getDateDict()
            data['tasks'][nodeName]['dateVisible'] = task.getDateIsVisible()
            data['tasks'][nodeName]['hoursBegin'] = task.getTimeDict(task.getHoursBegin())
            data['tasks'][nodeName]['hoursBeginMask'] = task.getTimeMaskDict(task.getHoursBeginMask())
            data['tasks'][nodeName]['hoursBeginVisible'] = task.getHoursBeginIsVisible()
            data['tasks'][nodeName]['hoursEnd'] = task.getTimeDict(task.getHoursEnd())
            data['tasks'][nodeName]['hoursEndMask'] = task.getTimeMaskDict(task.getHoursEndMask())
            data['tasks'][nodeName]['hoursEndVisible'] = task.getHoursEndIsVisible()
            data['tasks'][nodeName]['delay'] = task.getTimeDict(task.getDelay())
            data['tasks'][nodeName]['delayType'] = task.getDelayType()
            data['tasks'][nodeName]['delayMask'] = task.getTimeMaskDict(task.getDelayMask())
            data['tasks'][nodeName]['delayVisible'] = task.getDelayIsVisible()
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
    # Get the data of the plugin to gadget as dictionary.
    # --------------------------------------------------------------------------
    def getPGData(self, language):
        """Get the data of the plugin to gadget as dictionary.
        @return a dictionary.
        """
        pluginData = copy.deepcopy(self.__parentPlugin.getData(language))
        gadgetData = copy.deepcopy(self.getData(language))
        # Description
        pluginData['description'] = gadgetData['description']
        pluginData['description']['o_uuid'] = pluginData['description']['uuid']
        pluginData['description']['uuid'] = self.__parentPlugin.getDescription().getUuid()
        # Parameters
        for key in gadgetData['parameters'].keys():
            paramGData = gadgetData['parameters'][key]
            for keyP in pluginData['parameters'].keys():
                paramPData = pluginData['parameters'][keyP]
                if paramPData['name'] == paramGData['name']:
                    paramPData['defaultValue'] = paramGData['defaultValue']
                    if paramGData['visible']:
                        paramPData['selected'] = True
                    else:
                        paramPData['selected'] = False
        # Tasks
        for key in gadgetData['tasks'].keys():
            taskGData = gadgetData['tasks'][key]
            for keyP in pluginData['tasks'].keys():
                taskPData = pluginData['tasks'][keyP]
                if taskPData['name'] == taskGData['name']:
                    taskPData['weekMask'] = taskGData['weekMask']
                    taskPData['hoursBegin'] = taskGData['hoursBegin']
                    taskPData['hoursEnd'] = taskGData['hoursEnd']
                    taskPData['date'] = taskGData['date']
                    taskPData['delay'] = taskGData['delay']
                    taskPData['selected'] = True
        return pluginData

    # --------------------------------------------------------------------------
    # Get the directory path where this gadget is uncompressed.
    # --------------------------------------------------------------------------
    def getWorkingPath(self):
        """Get the directory path where this gadget is uncompressed.
        @return: A directory path as string.
        """
        return self.__workingPath

    # --------------------------------------------------------------------------
    # Get the SCG file of the gadget.
    # --------------------------------------------------------------------------
    def getScgFile(self):
        """Get the SCG file of the gadget.
        @return: A string.
        """
        return self.__scgFile

    # --------------------------------------------------------------------------
    # Get the parent gadgets container.
    # --------------------------------------------------------------------------
    def getContainer(self):
        """Get the parent gadgets container.
        @return: The parent gadgets container.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Get the gadget description object.
    # --------------------------------------------------------------------------
    def getDescription(self):
        """Get the gadget description object.
        @return: The gadget description object.
        """
        return self.__description

    # --------------------------------------------------------------------------
    # Get the gadget commands objects list.
    # --------------------------------------------------------------------------
    def getCommands(self):
        """Get the gadget command objects list.
        @return: The gadget commands objects list.
        """
        return self.__parentPlugin.getCommands()

    # --------------------------------------------------------------------------
    # Get a command object by it name.
    # --------------------------------------------------------------------------
    def getCommand(self, commandName):
        """Get a command object by it name.
        @param commandName: The name of the command.
        @return: The command object as PluginCommand or None.
        """
        for command in self.__parentPlugin.getCommands():
            if command.getName() == commandName:
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
        for command in self.__parentPlugin.getCommands():
            result.append(command.getName())
        return result

    # --------------------------------------------------------------------------
    # Get the gadget tasks objects list.
    # --------------------------------------------------------------------------
    def getTasks(self):
        """Get the gadget tasks objects list.
        @return: The gadget tasks objects list.
        """
        return self.__tasks

    # --------------------------------------------------------------------------
    # Get a task object by it name.
    # --------------------------------------------------------------------------
    def getTask(self, taskName):
        """Get a task object by it name.
        @param taskName: The name of the task.
        @return: The task object as PluginTask or None.
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
        return self.__parentPlugin.getDefaultCheckCommandName()

    # --------------------------------------------------------------------------
    # Get the default run command name.
    # --------------------------------------------------------------------------
    def getDefaultRunCommandName(self):
        """Get the default run command name.
        @return: A string.
        """
        return self.__parentPlugin.getDefaultRunCommandName()

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
        @return: The parameter object or None.
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
    # I18N
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Update the i18n objects list of the gadget.
    # --------------------------------------------------------------------------
    def __updateI18nList(self):
        """Update the i18n objects list of the gadget.
        """
        self.__i18nList = {}
        language = self.__parentPlugin.getContainer().getLanguage()
        if language not in SUPPORTED_LANGUAGES_LIST:
            SUPPORTED_LANGUAGES_LIST.append(language)
        for language in SUPPORTED_LANGUAGES_LIST:
            i18n = I18n()
            i18n.setLocale(language)
            i18n.setPoDirectory(os.path.join(self.__parentPlugin.getWorkingPath(),
                "resources"))
            i18n.update()
            i18n.setPoDirectory(self.__workingPath)
            i18n.update()
            self.__i18nList[language] = i18n

    # --------------------------------------------------------------------------
    # Translate a message with the current language of the plugins container.
    # --------------------------------------------------------------------------
    def tr(self, message, *arguments):
        """Translate a message with the current language of the plugins
        container.
        @param message: Message to translate.
        @param arguments: Arguments to pass in the message.
        @return: The translated message.
        """
        result = self.__i18nList[
            self.__parentPlugin.getContainer().getLanguage()].tr(message,
            *arguments)
        result = result.replace("\\''", "'")
        result = result.replace("\\'", "'")
        result = result.replace("''", "'")
        return result

    # --------------------------------------------------------------------------
    # Translate a message with a specific language.
    # --------------------------------------------------------------------------
    def tr2(self, language, message, *arguments):
        """Translate a message with a specific language.
        @param language: Language of the traduction.
        @param message: Message to translate.
        @param arguments: Arguments to pass in the message.
        @return: The translated message.
        """
        if language in self.__i18nList.keys():
            result = self.__i18nList[language].tr(message, *arguments)
        else:
            result = self.__i18nList[
                self.__parentPlugin.getContainer().getLanguage()].tr(message,
                *arguments)
        result = result.replace("\\''", "'")
        result = result.replace("\\'", "'")
        result = result.replace("''", "'")
        return result

    # ==========================================================================
    # Gadget execution
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Start this gadget.
    # --------------------------------------------------------------------------
    def start(self, command, parameters = {}):
        """Start this gadget.
        @param command: Command name to start the gadget.
        @param parameters: Parameters of the gadget as dictionary.
        @return: The success of the gadget starting.
        - When the parameters are not defined the gadget is started with the
        default ones.
        - If a parameter is wrong the default one is set.
        - If a parameter is missing the default one is set.
        """
        myParameters = {}
        for parameter in self.getParameters():
            if parameters.has_key(parameter.getName()):
                myParameters[parameter.getName()] = parameters[parameter.getName()]
            else:
                myParameters[parameter.getName()] = parameter.getDefaultValue(self.__parent.getLanguage())
        if not parameters.has_key('uuid'):
            myParameters['uuid'] = self.getDescription().getUuid()
        for key in parameters.keys():
            if not myParameters.has_key(key):
                myParameters[key] = parameters[key]
        return self.__parentPlugin.start(command, myParameters)

    # --------------------------------------------------------------------------
    # Stop the gadget.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the gadget.
        """
        self.__parentPlugin.stop()

    # --------------------------------------------------------------------------
    # Send event to the gadget. (Daemon mode)
    # --------------------------------------------------------------------------
    def sendEvent(self, eventName, eventValues = []):
        """Send event to the gadget. (Daemon mode)
        @eventName: Event name.
        @eventValues: Event values list.
        """
        self.__parentPlugin.sendEvent(eventName, eventValues)
