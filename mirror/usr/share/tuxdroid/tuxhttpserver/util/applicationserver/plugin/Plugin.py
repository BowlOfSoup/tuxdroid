#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is highly inspired by a "gadget framework"  written by
#    "Yoran Brault" <http://artisan.karma-lab.net>

import os
import threading

from util.i18n.I18n import I18n
from interpreters.PluginInterpreter import PluginInterpreter
from interpreters.PluginInterpreterPython import PluginInterpreterPython
from interpreters.PluginInterpreterJava import PluginInterpreterJava
from interpreters.PluginInterpreterContext import PluginInterpreterContext
from PluginDescription import PluginDescription
from PluginParameter import PluginParameter
from PluginCommand import PluginCommand
from PluginTask import PluginTask

# Default list of the supported language.
SUPPORTED_LANGUAGES_LIST = ["en", "fr", "nl", "es", "it", "pt", "ar", "da",
    "de", "no", "sv",]
# Internal parameters list
INTERNAL_PARAMETERS_LIST = ["traces", "language", "country", "locutor", "pitch",
    "uuid"]

# ------------------------------------------------------------------------------
# Plugin class.
# ------------------------------------------------------------------------------
class Plugin(object):
    """Plugin class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary, scpFile, workingPath):
        """Constructor of the class.
        @param parent: Parent Plugins container.
        @param dictionary: Plugin structure as dictionary.
        @param scpFile: SCP file name of the plugin.
        @param workingPath: Working path of the plugin.
        """
        self.__parent = parent
        # Save the dictionary
        self.__dictionary = dictionary
        # Save the working path
        self.__workingPath = workingPath
        # Save the scp file name
        self.__scpFile = scpFile
        # Create i18n table
        self.__i18nList = {}
        self.__updateI18nList()
        # Create descriptor
        self.__description = PluginDescription(self, dictionary['description'],
            self.__workingPath)
        # Create parameters
        self.__parameters = []
        if dictionary.has_key('parameters'):
            keys = dictionary['parameters'].keys()
            keys.sort()
            for key in keys:
                pluginParameter = PluginParameter(self,
                    dictionary['parameters'][key])
                paramPlatform = pluginParameter.getPlatform()
                if paramPlatform != "all":
                    if paramPlatform == "windows":
                        if os.name != "nt":
                            pluginParameter.setVisible('false')
                    else:
                        if os.name == "nt":
                            pluginParameter.setVisible('false')
                self.__parameters.append(pluginParameter)
        # Add some other parameters
        pluginParameter = PluginParameter(self, {
            'name' : 'traces',
            'type' : 'boolean',
            'defaultValue' : 'true',
            'description' : 'Verbose mode',
            'category' : 'internals',
            'visible' : 'false',
        })
        self.__parameters.append(pluginParameter)
        pluginParameter = PluginParameter(self, {
            'name' : 'language',
            'type' : 'string',
            'defaultValue' : self.__parent.getLanguage(),
            'description' : 'Language',
            'category' : 'internals',
            'visible' : 'false',
        })
        self.__parameters.append(pluginParameter)
        pluginParameter = PluginParameter(self, {
            'name' : 'country',
            'type' : 'string',
            'defaultValue' : self.__parent.getCountry(),
            'description' : 'Country',
            'category' : 'internals',
            'visible' : 'false',
        })
        self.__parameters.append(pluginParameter)
        defaultLocutor = self.__parent.getLocutor().replace("8k", "")
        pluginParameter = PluginParameter(self, {
            'name' : 'locutor',
            'type' : 'enum(' + defaultLocutor + ')',
            'defaultValue' : defaultLocutor,
            'description' : 'Locutor',
            'category' : 'internals',
            'visible' : 'true',
        })
        self.__parameters.append(pluginParameter)
        pluginParameter = PluginParameter(self, {
            'name' : 'pitch',
            'type' : 'integer',
            'defaultValue' : str(self.__parent.getPitch()),
            'description' : 'Pitch',
            'category' : 'internals',
            'visible' : 'false',
        })
        self.__parameters.append(pluginParameter)
        pluginParameter = PluginParameter(self, {
            'name' : 'uuid',
            'type' : 'string',
            'defaultValue' : self.getDescription().getUuid(),
            'description' : 'Uuid',
            'category' : 'internals',
            'visible' : 'false',
        })
        self.__parameters.append(pluginParameter)
        pluginParameter = PluginParameter(self, {
            'name' : 'startedBy',
            'type' : 'string',
            'defaultValue' : 'user',
            'description' : 'Started by',
            'category' : 'internals',
            'visible' : 'false',
        })
        self.__parameters.append(pluginParameter)
        # Create commands
        self.__commands = []
        for key in dictionary['commands'].keys():
            self.__commands.append(PluginCommand(self,
                dictionary['commands'][key]))
        # Define default check and run commands
        commandNamesList = self.getCommandsName()
        if "run" in commandNamesList:
            self.__defaultRunCommandName = "run"
        else:
            self.__defaultRunCommandName = self.__commands[0].getName()
        if "check" in commandNamesList:
            self.__defaultCheckCommandName = "check"
        else:
            self.__defaultCheckCommandName = self.__defaultRunCommandName
        # Create tasks
        self.__tasks = []
        if dictionary.has_key('tasks'):
            for key in dictionary['tasks'].keys():
                self.__tasks.append(PluginTask(self,
                    dictionary['tasks'][key]))
        # Define interpreter
        interpreterClass = PluginInterpreter
        if dictionary['interpreter']['kind'] == 'python':
            interpreterClass = PluginInterpreterPython
        elif dictionary['interpreter']['kind'] == 'java':
            interpreterClass = PluginInterpreterJava
        self.__interpreterConf = {
            'class' : interpreterClass,
            'executable' : dictionary['interpreter']['executable'],
        }
        self.__pluginInterpreterContexts = []
        self.__interpreterMutex = threading.Lock()
        # Callbacks
        self.__onPluginNotificationCallback = None
        self.__onPluginMessageCallback = None
        self.__onPluginErrorCallback = None
        self.__onPluginTraceCallback = None
        self.__onPluginResultCallback = None
        self.__onPluginActuationCallback = None
        self.__onPluginStartingCallback = None
        self.__onPluginStoppedCallback = None

    # --------------------------------------------------------------------------
    # Get the data of the plugin as dictionary.
    # --------------------------------------------------------------------------
    def getData(self, language):
        """Get the data of the plugin as dictionary.
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
        data['description']['hasAttituneAlert'] = description.hasAttituneAlert()
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
        data['description']['scpFile'] = self.getScpFile()
        scpName = os.path.split(self.getScpFile())[-1]
        pluginDlUrl = '/plugins/%s' % scpName
        data['description']['scpUrl'] = pluginDlUrl
        data['defaultRunCommand'] = self.getDefaultRunCommandName()
        data['defaultCheckCommand'] = self.getDefaultCheckCommandName()
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
        commands = self.getCommands()
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
    # Get the directory path where this plugin is uncompressed.
    # --------------------------------------------------------------------------
    def getWorkingPath(self):
        """Get the directory path where this plugin is uncompressed.
        @return: A directory path as string.
        """
        return self.__workingPath

    # --------------------------------------------------------------------------
    # Get the SCP file of the plugin.
    # --------------------------------------------------------------------------
    def getScpFile(self):
        """Get the SCP file of the plugin.
        @return: A string.
        """
        return self.__scpFile

    # --------------------------------------------------------------------------
    # Get the dictionary of the plugin.
    # --------------------------------------------------------------------------
    def getDictionary(self):
        """Get the dictionary of the plugin.
        @return: A dictionary.
        """
        return self.__dictionary

    # --------------------------------------------------------------------------
    # Get the parent plugins container.
    # --------------------------------------------------------------------------
    def getContainer(self):
        """Get the parent plugins container.
        @return: The parent plugins container.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Get the plugin description object.
    # --------------------------------------------------------------------------
    def getDescription(self):
        """Get the plugin description object.
        @return: The plugin description object.
        """
        return self.__description

    # --------------------------------------------------------------------------
    # Get the plugin commands objects list.
    # --------------------------------------------------------------------------
    def getCommands(self):
        """Get the plugin command objects list.
        @return: The plugin commands objects list.
        """
        return self.__commands

    # --------------------------------------------------------------------------
    # Get a command object by it name.
    # --------------------------------------------------------------------------
    def getCommand(self, commandName):
        """Get a command object by it name.
        @param commandName: The name of the command.
        @return: The command object as PluginCommand or None.
        """
        for command in self.__commands:
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
        for command in self.__commands:
            result.append(command.getName())
        return result

    # --------------------------------------------------------------------------
    # Get the plugin tasks objects list.
    # --------------------------------------------------------------------------
    def getTasks(self):
        """Get the plugin tasks objects list.
        @return: The plugin tasks objects list.
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
        return self.__defaultCheckCommandName

    # --------------------------------------------------------------------------
    # Get the default run command name.
    # --------------------------------------------------------------------------
    def getDefaultRunCommandName(self):
        """Get the default run command name.
        @return: A string.
        """
        return self.__defaultRunCommandName

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

    # --------------------------------------------------------------------------
    # Get if the current running instance is in daemon mode or not.
    # --------------------------------------------------------------------------
    def instanceIsDaemon(self):
        """Get if the current running instance is in daemon mode or not.
        @return: True or False.
        """
        print "GET INSTANCE IS DAEMON (from Plugin object)"
        #if self.__pluginInterpreterContext != None:
        #    isDaemon = self.__pluginInterpreterContext.isDaemon()
        #else:
        #    isDaemon = False
        return False

    # ==========================================================================
    # I18N
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Update the i18n objects list of the plugin.
    # --------------------------------------------------------------------------
    def __updateI18nList(self):
        """Update the i18n objects list of the plugin.
        """
        self.__i18nList = {}
        language = self.__parent.getLanguage()
        if language not in SUPPORTED_LANGUAGES_LIST:
            SUPPORTED_LANGUAGES_LIST.append(language)
        for language in SUPPORTED_LANGUAGES_LIST:
            i18n = I18n()
            i18n.setPoDirectory(os.path.join(os.path.split(__file__)[0],
                "translation"))
            i18n.setLocale(language)
            i18n.update()
            i18n.setPoDirectory(os.path.join(self.__workingPath, "resources"))
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
        result = self.__i18nList[self.__parent.getLanguage()].tr(message,
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
            result = self.__i18nList[self.__parent.getLanguage()].tr(message,
                *arguments)
        result = result.replace("\\''", "'")
        result = result.replace("\\'", "'")
        result = result.replace("''", "'")
        return result

    # ==========================================================================
    # Plugin execution
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Set the plugin notification event callback.
    # --------------------------------------------------------------------------
    def setOnPluginNotificationCallback(self, funct):
        """Set the plugin notification event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginNotification(pluginInterpreterContext, messageId, *args):
            pass
        """
        self.__onPluginNotificationCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin message event callback.
    # --------------------------------------------------------------------------
    def setOnPluginMessageCallback(self, funct):
        """Set the plugin message event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginMessage(pluginInterpreterContext, message):
            pass
        """
        self.__onPluginMessageCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin error event callback.
    # --------------------------------------------------------------------------
    def setOnPluginErrorCallback(self, funct):
        """Set the plugin error event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginError(pluginInterpreterContext, *messagesList):
            pass
        """
        self.__onPluginErrorCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin trace event callback.
    # --------------------------------------------------------------------------
    def setOnPluginTraceCallback(self, funct):
        """Set the plugin trace event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginTrace(pluginInterpreterContext, *messagesList):
            pass
        """
        self.__onPluginTraceCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin result event callback.
    # --------------------------------------------------------------------------
    def setOnPluginResultCallback(self, funct):
        """Set the plugin result event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginResult(pluginInterpreterContext, pluginResult):
            pass
        """
        self.__onPluginResultCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin actuation event callback.
    # --------------------------------------------------------------------------
    def setOnPluginActuationCallback(self, funct):
        """Set the plugin actuation event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginActuation(pluginInterpreterContext, *messagesList):
            pass
        """
        self.__onPluginActuationCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin starting event callback.
    # --------------------------------------------------------------------------
    def setOnPluginStartingCallback(self, funct):
        """Set the plugin starting event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginStarting(pluginInterpreterContext):
            pass
        """
        self.__onPluginStartingCallback = funct

    # --------------------------------------------------------------------------
    # Set the plugin stopped event callback.
    # --------------------------------------------------------------------------
    def setOnPluginStoppedCallback(self, funct):
        """Set the plugin stopped event callback.
        @param funct: Function pointer.
        Function prototype:
        def onPluginStopped(pluginInterpreterContext):
            pass
        """
        self.__onPluginStoppedCallback = funct

    # --------------------------------------------------------------------------
    # Start this plugin.
    # --------------------------------------------------------------------------
    def start(self, command, parameters = {}):
        """Start this plugin.
        @param command: Command name to start the plugin.
        @param parameters: Parameters of the plugin as dictionary.
        @return: The success of the plugin starting.
        - When the parameters are not defined the plugin is started with the
        default ones.
        - If a parameter is wrong the default one is set.
        - If a parameter is missing the default one is set.
        """
        # Create the interpreter
        pluginInterpreterContext = PluginInterpreterContext(self,
            self.__interpreterConf['class'],
            self.__interpreterConf['executable'])
        # Set callbacks
        pluginInterpreterContext.setOnPluginNotificationCallback(
            self.__onPluginNotificationCallback)
        pluginInterpreterContext.setOnPluginMessageCallback(
            self.__onPluginMessageCallback)
        pluginInterpreterContext.setOnPluginErrorCallback(
            self.__onPluginErrorCallback)
        pluginInterpreterContext.setOnPluginTraceCallback(
            self.__onPluginTraceCallback)
        pluginInterpreterContext.setOnPluginResultCallback(
            self.__onPluginResultCallback)
        pluginInterpreterContext.setOnPluginActuationCallback(
            self.__onPluginActuationCallback)
        pluginInterpreterContext.setOnPluginStartingCallback(
            self.__onPluginStartingCallback)
        pluginInterpreterContext.setOnPluginStoppedCallback(
            self.__onPluginStoppedCallback)
        # Fill the parameters
        if parameters.has_key('language'):
            language = parameters['language']
        else:
            language = self.__parent.getLanguage()
        pluginParameters = {}
        for parameterName in self.getParametersName():
            pluginParameters[parameterName] = self.getParameter(parameterName).getDefaultValue(language)
        for parameterName in parameters.keys():
            if pluginParameters.has_key(parameterName):
                param = self.getParameter(parameterName)
                if param != None:
                    # Parameter "locutor" is a special parameter with a dynamique
                    # behavior.
                    if param.getName() != "locutor":
                        if param.getType() in ["enum", "booleans"]:
                            pluginParameters[parameterName] = param.getUntranslatedEnumValue(
                                parameters[parameterName], language)
                            continue
                pluginParameters[parameterName] = parameters[parameterName]
        pluginInterpreterContext.setInstanceParameters(pluginParameters)
        # Get the command
        pluginCommand = self.getCommand(command)
        if pluginCommand == None:
            pluginCommand = self.getCommands()[0]
        pluginInterpreterContext.setInstanceCommandName(pluginCommand.getName())
        pluginInterpreterContext.setInstanceIsDaemon(pluginCommand.isDaemon())
        # Add the interperter context in the list
        self.__interpreterMutex.acquire()
        self.__pluginInterpreterContexts.append(pluginInterpreterContext)
        self.__interpreterMutex.release()
        # Execute the plugin instance
        pluginInterpreterContext.run()
        return True

    # --------------------------------------------------------------------------
    # Stop the plugin.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the plugin.
        """
        self.__interpreterMutex.acquire()
        for pluginInterpreterContext in self.__pluginInterpreterContexts:
            pluginInterpreterContext.abort()
        self.__pluginInterpreterContexts = []
        self.__interpreterMutex.release()

    # --------------------------------------------------------------------------
    # Send event to the plugin. (Daemon mode)
    # --------------------------------------------------------------------------
    def sendEvent(self, eventName, eventValues = []):
        """Send event to the plugin. (Daemon mode)
        @eventName: Event name.
        @eventValues: Event values list.
        """
        self.__interpreterMutex.acquire()
        for pluginInterpreterContext in self.__pluginInterpreterContexts:
            pluginInterpreterContext.sendEvent(eventName, eventValues)
        self.__interpreterMutex.release()
