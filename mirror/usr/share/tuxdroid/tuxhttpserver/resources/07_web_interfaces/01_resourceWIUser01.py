# ==============================================================================
# Resource : Web Interface - User 01.
# ==============================================================================

from translation.Translation import Translation
from util.misc import URLTools

# ------------------------------------------------------------------------------
# Declaration of the resource "wi_user_01".
# ------------------------------------------------------------------------------
class TDSResourceWIUser01(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "wi_user_01"
        self.comment = "Resource to manage the web interface - user 01."
        self.fileName = RESOURCE_FILENAME
        self.translations = Translation("wi_user")

    def getStates(self):
        state = eventsHandler.getEventHandler(ST_NAME_DONGLE_PLUG).getLastState()
        if state == None:
            dongleState = "off"
        else:
            if state[0]:
                dongleState = "on"
            else:
                dongleState = "off"
        state = eventsHandler.getEventHandler(ST_NAME_RADIO_STATE).getLastState()
        if state == None:
            radioState = "off"
        else:
            if state[0]:
                radioState = "on"
            else:
                radioState = "off"
        if (dongleState == "off") or (radioState == "off"):
            batteryState = "nodongle"
        else:
            state = eventsHandler.getEventHandler(ST_NAME_BATTERY_LEVEL).getLastState()
            if state == None:
                batteryState = "nodongle"
            else:
                battVal = state[0]
                if battVal < 4995:
                    batteryState = "empty"
                elif (battVal >= 4995) and (battVal <= 5128):
                    batteryState = "low"
                elif (battVal > 5128) and (battVal <= 5461):
                    batteryState = "middle"
                else:
                    batteryState = "high"
            state = eventsHandler.getEventHandler(ST_NAME_CHARGER_STATE).getLastState()
            if state != None:
                if state[0] != "UNPLUGGED":
                    batteryState = "charge"
        state = resourceRobotContentInteractions.getPguContextsManager().isStarted()
        if state:
            soundState = "on"
        else:
            soundState = "off"
        result = {}
        result['dongleState'] = dongleState
        result['radioState'] = radioState
        result['batteryState'] = batteryState
        result['soundState'] = soundState
        return result

    def getAvailableToolsData(self, language):
        result = {}
        # Attitunes studio
        attituneStudioData = resourcePluginsServer.getPluginData(
            "548f7a9a-567d-773e-a0dd-102fe68a1b49", language)
        if attituneStudioData != None:
            result['attitunes_studio'] = {
                'name' : attituneStudioData['description']['translatedName'],
                'icon' : attituneStudioData['description']['iconFile'],
                'uuid' : attituneStudioData['description']['uuid'],
                'help' : attituneStudioData['description']['helpFile'],
            }
        # Tux Controller
        tuxControllerData = resourcePluginsServer.getPluginData(
            "548f7a77-567d-773e-a0ef-321fe63a1c88", language)
        if tuxControllerData != None:
            result['tux_controller'] = {
                'name' : tuxControllerData['description']['translatedName'],
                'icon' : tuxControllerData['description']['iconFile'],
                'uuid' : tuxControllerData['description']['uuid'],
                'help' : tuxControllerData['description']['helpFile'],
            }
        # About TuxBox
        aboutTuxBoxData = resourcePluginsServer.getPluginData(
            "d7c4218d-5a5c-4cdd-b515-0df7411c000f", language)
        if aboutTuxBoxData != None:
            result['about'] = {
                'name' : aboutTuxBoxData['description']['translatedName'],
                'icon' : aboutTuxBoxData['description']['iconFile'],
                'uuid' : aboutTuxBoxData['description']['uuid'],
                'help' : aboutTuxBoxData['description']['helpFile'],
            }
        return result

# Create an instance of the resource
resourceWIUser01 = TDSResourceWIUser01("resourceWIUser01")
# Register the resource into the resources manager
resourcesManager.addResource(resourceWIUser01)

# ------------------------------------------------------------------------------
# Declaration of the service "index".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01Index(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
            'skin' : 'string',
            'menu' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "index"
        self.comment = "Show the main user page."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = str(resourceUsers.getCurrentUserConfiguration()['language1'])
        skin = parameters['skin']
        menu = parameters['menu']
        contentStruct['root']['data'] = {}
        contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        contentStruct['root']['skin'] = skin
        contentStruct['root']['menu'] = menu
        contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/index.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01Index)
# Bind the resource index url to this service
resourcesManager.addBinding("user", "wi_user_01", "index",
    "skin=user_01&language=en&menu=livewithtux")
resourcesManager.addBinding("user/index", "wi_user_01", "index",
    "skin=user_01&language=en&menu=livewithtux")
# Bind the root url to this service
resourcesManager.addBinding("ROOT", "wi_user_01", "index",
    "skin=user_01&language=en&menu=livewithtux")

# ------------------------------------------------------------------------------
# Declaration of the service "live_with_tux".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01LiveWithTux(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
            'skin' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "livewithtux"
        self.comment = "Show the Live with Tux page."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        skin = parameters['skin']
        contentStruct['root']['data'] = {}
        contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        contentStruct['root']['skin'] = skin
        contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/livewithtux.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01LiveWithTux)

# ------------------------------------------------------------------------------
# Declaration of the service "gadgets".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01Gadgets(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
            'skin' : 'string',
            'uuid' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "gadgets"
        self.comment = "Show the gadgets page."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        skin = parameters['skin']
        uuid = parameters['uuid']
        for ugc in resourceUgcServer.getUgcContainer().getUgcs():
            if ugc.getParentGadget().getDescription().getUuid() == uuid:
                uuid = ugc.getDescription().getUuid()
                break
        contentStruct['root']['data'] = {}
        contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        contentStruct['root']['skin'] = skin
        contentStruct['root']['language'] = language
        contentStruct['root']['uuid'] = uuid
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/gadgets.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01Gadgets)

# ------------------------------------------------------------------------------
# Declaration of the service "attitunes".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01Attitunes(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
            'skin' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "attitunes"
        self.comment = "Show the attitunes page."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        skin = parameters['skin']
        contentStruct['root']['data'] = {}
        contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        contentStruct['root']['skin'] = skin
        contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/attitunes.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01Attitunes)

# ------------------------------------------------------------------------------
# Declaration of the service "tools".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01Tools(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
            'skin' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "tools"
        self.comment = "Show the tools page."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        skin = parameters['skin']
        contentStruct['root']['data'] = resourceWIUser01.getAvailableToolsData(language)
        contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        contentStruct['root']['skin'] = skin
        contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/tools.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01Tools)

# ------------------------------------------------------------------------------
# Declaration of the service "online".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01Online(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
            'skin' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "online"
        self.comment = "Show the online page."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        skin = parameters['skin']
        contentStruct['root']['data'] = {}
        contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        contentStruct['root']['skin'] = skin
        contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/online.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01Online)

# ------------------------------------------------------------------------------
# Declaration of the service "get_states".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01GetStates(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "get_states"
        self.comment = "Get Tux Droid and gadget states."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        contentStruct['root']['data'] = resourceWIUser01.getStates()
        gadgetsData = resourceRobotContentInteractions.getPguContextsManager().getOnDemandDictForThumbnailBar()
        if gadgetsData != {}:
            contentStruct['root']['gadgets'] = gadgetsData
        currentAlertData = resourceRobotContentInteractions.getPguContextsManager().getCurrentUgcForegroundScheduled()
        if currentAlertData != {}:
            contentStruct['root']['alert'] = currentAlertData
        contentStruct['root']['gadget_messages'] = resourceRobotContentInteractions.getPguContextsManager().getLastStartedOnDemandUgcMessages()
        contentStruct['root']['language'] = resourceUsers.getCurrentFirstLanguage()
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01GetStates)

# ------------------------------------------------------------------------------
# Declaration of the service "gadget_configuration".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01GadgetConfiguration(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
            'skin' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "gadget_configuration"
        self.comment = "Show the gadget configuration."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        skin = parameters['skin']
        data = resourceUgcServer.getUgcData(uuid, language)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            # Complete data with available alert attitunes
            # Check for alert type
            showAttitunes = False
            ugc = resourceUgcServer.getUgcContainer().getUgcByUuid(uuid)
            parentPlugin = ugc.getParentGadget().getParentPlugin()
            if parentPlugin.getDescription().hasAttituneAlert():
                tasks = ugc.getTasks()
                for task in tasks:
                    parentTask = parentPlugin.getTask(task.getName())
                    if parentTask != None:
                        parentCommand = parentPlugin.getCommand(parentTask.getCommand())
                        if parentCommand != None:
                            if not parentCommand.isNotifier():
                                showAttitunes = True
                                break
            data['showAlertAttitune'] = showAttitunes
            parentUuid = parentPlugin.getDescription().getUuid()
            attitunesList = resourceAttituneManager.getAttitunesNameByObserversList([parentUuid, "userAttitunes"])
            attitunesList.insert(0, "----")
            data['availableAttitunes'] = {}
            for i, attName in enumerate(attitunesList):
                nodeName = "att_%d" % i
                data['availableAttitunes'][nodeName] = attName
            contentStruct['root']['data'] = data
            contentStruct['root']['skin'] = skin
            contentStruct['root']['language'] = language
            contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/gadget_configuration.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01GadgetConfiguration)

# ------------------------------------------------------------------------------
# Declaration of the service "gadget_help".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01GadgetHelp(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
            'skin' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "gadget_help"
        self.comment = "Show the gadget help."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        skin = parameters['skin']
        data = resourceUgcServer.getUgcData(uuid, language)
        if data == None:
            data = resourcePluginsServer.getPluginData(uuid, language)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
            contentStruct['root']['skin'] = skin
            contentStruct['root']['language'] = language
            contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/gadget_help.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01GadgetHelp)

# ------------------------------------------------------------------------------
# Declaration of the service "online_gadget_help".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01OnlineGadgetHelp(TDSService):

    def configure(self):
        self.parametersDict = {
            'symbolic_name' : 'string',
            'language' : 'string',
            'skin' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "online_gadget_help"
        self.comment = "Show the online gadget help."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        symbolicName = parameters['symbolic_name']
        language = parameters['language']
        skin = parameters['skin']
        data = None
        onlineGadget = resourceGadgetsServer.getGadgetsContainer().getGadgetsOnlineContainer().getOnlineGadgetBySymbolicName(symbolicName)
        if onlineGadget != None:
            helpUrl = onlineGadget.getHelpFile(language)
            helpContent = URLTools.URLDownloadToString(helpUrl)
            if helpContent != None:
                data = {
                    'description' : {
                        'helpFile' : helpContent,
                    }
                }
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
            contentStruct['root']['skin'] = skin
            contentStruct['root']['language'] = language
            contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/gadget_help.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01OnlineGadgetHelp)

# ------------------------------------------------------------------------------
# Declaration of the service "apply_gadget".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01ApplyGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
            'parameters' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "apply_gadget"
        self.comment = "Apply the gadget configuration."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        params = []
        splParams = parameters['parameters'].split("|")
        for paramStruct in splParams:
            param = paramStruct.split("=")
            if len(param) == 2:
                name = param[0]
                value = param[1]
                value = value.replace('[RETURN]', '\n')
                value = value.replace('[EQUAL]', '=')
                value = value.replace('[PIPE]', '|')
                value = value.replace('[AMP]', '&')
                value = value.replace('[PLUS]', '+')
                params.append([name, value])
        tmpUgcUrl, nUuid = GadgetGenerator.updateUgc(
            resourceUgcServer.getUgcContainer().getUgcByUuid(uuid), params,
            resourcesManager)
        resourceUgcServer.insertTemporaryServedUgcInContainer(tmpUgcUrl)
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01ApplyGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "start_attitunes_studio".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01StartAttitunesStudio(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "start_attitunes_studio"
        self.comment = "Edit an attitune with Attitunes Studio."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        if language.lower() == "null":
            language = resourceUsers.getCurrentFirstLanguage()
        outputPath = os.path.join(resourceUsers.getCurrentUserBasePath(),
            "attitunes")
        t = threading.Thread(target = resourcePluginsServer.startPlugin,
            args = (
                "548f7a9a-567d-773e-a0dd-102fe68a1b49",
                "run",
                {
                    'outputpath' : outputPath,
                    'language' : language,
                }))
        t.start()
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01StartAttitunesStudio)

# ------------------------------------------------------------------------------
# Declaration of the service "edit_attitune".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01EditAttitune(TDSService):

    def configure(self):
        self.parametersDict = {
            'name' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "edit_attitune"
        self.comment = "Edit an attitune with Attitunes Studio."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        name = parameters['name']
        reencodedName = name
        try:
            tmp = reencodedName.decode("latin-1")
            reencodedName = tmp.encode("utf-8")
        except:
            pass
        language = parameters['language']
        attitunesContainer = resourceAttituneManager.getAttitunesContainer()
        attitunes = attitunesContainer.getAttitunes()
        for attitune in attitunes:
            if attitune.getDescription().getName() in [name, reencodedName]:
                attitunePath = attitune.getAttFile()
                t = threading.Thread(target = resourcePluginsServer.startPlugin,
                    args = (
                        "548f7a9a-567d-773e-a0dd-102fe68a1b49",
                        "run",
                        {
                            'path' : attitunePath,
                            'language' : language,
                        }))
                t.start()
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01EditAttitune)

# ------------------------------------------------------------------------------
# Declaration of the service "start_tux_controller".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01StartTuxController(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "start_tux_controller"
        self.comment = "Start Tux Controller tool."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        if language.lower() == "null":
            language = resourceUsers.getCurrentFirstLanguage()
        t = threading.Thread(target = resourcePluginsServer.startPlugin,
            args = (
                "548f7a77-567d-773e-a0ef-321fe63a1c88",
                "run",
                {
                    'language' : language,
                }))
        t.start()
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01StartTuxController)

# ------------------------------------------------------------------------------
# Declaration of the service "global_configuration".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01GlobalConfiguration(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
            'skin' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "global_configuration"
        self.comment = "Show the global configuration."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        skin = parameters['skin']
        data = {}
        data['availableLocutors'] = {}
        for i, locutor in enumerate(resourceUsers.getLocutorsFromFirstLanguage()):
            data['availableLocutors']['loc_%d' % i] = locutor
        data['defaultLocutor'] = resourceUsers.getCurrentFirstLocutor()
        data['defaultPitch'] = resourceUsers.getCurrentPitch()
        contentStruct['root']['data'] = data
        contentStruct['root']['skin'] = skin
        contentStruct['root']['language'] = language
        contentStruct['root']['translations'] = resourceWIUser01.translations.getTranslations(language)
        self.haveXsl = True
        self.xslPath = "/data/web_interface/%s/xsl/global_configuration.xsl" % skin
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01GlobalConfiguration)

# ------------------------------------------------------------------------------
# Declaration of the service "apply_global_configuration".
# ------------------------------------------------------------------------------
class TDSServiceWIUser01ApplyGlobalConfiguration(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
            'locutor' : 'string',
            'pitch' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "apply_global_configuration"
        self.comment = "Apply the global configuration."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        locutor = parameters['locutor']
        pitch = parameters['pitch']
        oldLocutor = resourceUsers.getCurrentFirstLocutor()
        resourceUsers.setNewFirstLocutor(locutor)
        resourceUsers.setNewPitch(pitch)
        resourceUsers.storeUserConfiguration()
        for ugc in resourceUgcServer.getUgcContainer().getUgcs():
            if ugc.getParameter('locutor') != None:
                if ugc.getParameter('locutor').getValue() == oldLocutor:
                    ugc.getParameter('locutor').setValue(locutor)
            if ugc.getParameter('pitch') != None:
                ugc.getParameter('pitch').setValue(pitch)
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIUser01.addService(TDSServiceWIUser01ApplyGlobalConfiguration)

