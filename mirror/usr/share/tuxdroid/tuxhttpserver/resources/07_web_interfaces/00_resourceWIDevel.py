# ==============================================================================
# Resource : Web Interface - Devel.
# ==============================================================================

from util.applicationserver.gadget.GadgetGenerator import GadgetGenerator

# ------------------------------------------------------------------------------
# Declaration of the resource "wi_devel".
# ------------------------------------------------------------------------------
class TDSResourceWIDevel(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "wi_devel"
        self.comment = "Resource to manage the web interface - devel."
        self.fileName = RESOURCE_FILENAME
        # Some records
        self.gadgetPreviewData = {}
        self.lastGeneratedGadgetUuid = None

# Create an instance of the resource
resourceWIDevel = TDSResourceWIDevel("resourceWIDevel")
# Register the resource into the resources manager
resourcesManager.addResource(resourceWIDevel)

# ------------------------------------------------------------------------------
# Declaration of the service "show_plugin".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelShowPlugin(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "show_plugin"
        self.comment = "Show the plugin informations."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        data = resourcePluginsServer.getPluginData(uuid, language)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
            contentStruct['root']['skin'] = "devel"
            contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/devel/xsl/plugin_infos.xsl"
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelShowPlugin)

# ------------------------------------------------------------------------------
# Declaration of the service "show_gadget".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelShowGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "show_gadget"
        self.comment = "Show the gadget informations."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        data = resourceGadgetsServer.getGadgetData(uuid, language)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
            contentStruct['root']['skin'] = "devel"
            contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/devel/xsl/gadget_infos.xsl"
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelShowGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "show_ugc".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelShowUgc(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "show_ugc"
        self.comment = "Show the UGC informations."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        data = resourceUgcServer.getUgcData(uuid, language)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
            contentStruct['root']['skin'] = "devel"
            contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/devel/xsl/ugc_infos.xsl"
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelShowUgc)

# ------------------------------------------------------------------------------
# Declaration of the service "plugin_to_gadget".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelPluginToGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "plugin_to_gadget"
        self.comment = "Show the plugin to gadget tool."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        data = resourcePluginsServer.getPluginData(uuid, language)
        if data == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            contentStruct['root']['data'] = data
            contentStruct['root']['skin'] = "devel"
            contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/devel/xsl/plugin_to_gadget.xsl"
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelPluginToGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "generate_gadget".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelGenerateGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'o_uuid' : 'string',
            'language' : 'string',
            'parameters' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "generate_gadget"
        self.comment = "Generate a gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        oUuid = parameters['o_uuid']
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
        tmpGadgetUrl, nUuid = GadgetGenerator.generateGadget(oUuid, params,
            resourcePluginsServer.getPluginsContainer().getPluginByUuid(uuid),
            resourcesManager)
        resourceWIDevel.lastGeneratedGadgetUuid = nUuid
        resourceGadgetsServer.insertTemporaryServerGadgetInContainer(tmpGadgetUrl)
        contentStruct['root']['skin'] = "devel"
        contentStruct['root']['language'] = language
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelGenerateGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "apply_ugc".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelApplyUgc(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
            'parameters' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "apply_ugc"
        self.comment = "Apply the UGC confiuration."

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
        resourceWIDevel.lastGeneratedGadgetUuid = nUuid
        resourceUgcServer.insertTemporaryServedUgcInContainer(tmpUgcUrl)
        contentStruct['root']['skin'] = "devel"
        contentStruct['root']['language'] = language
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelApplyUgc)

# ------------------------------------------------------------------------------
# Declaration of the service "post_preview_gadget".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelPostPreviewGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
            'parameters' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "post_preview_gadget"
        self.comment = "Post gadget preview data."

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
        resourceWIDevel.gadgetPreviewData = GadgetGenerator.generatePreviewGadget(params,
            resourcePluginsServer.getPluginsContainer().getPluginByUuid(uuid),
            resourcesManager, language)
        contentStruct['root']['skin'] = "devel"
        contentStruct['root']['language'] = language
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelPostPreviewGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "show_preview_gadget".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelShowPreviewGadget(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "show_preview_gadget"
        self.comment = "Show the gadget preview."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        data = resourceWIDevel.gadgetPreviewData
        contentStruct['root']['data'] = data
        contentStruct['root']['skin'] = "devel"
        contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/devel/xsl/gadget_preview.xsl"
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelShowPreviewGadget)

# ------------------------------------------------------------------------------
# Declaration of the service "gadget_edit".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelGadgetEdit(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "gadget_edit"
        self.comment = "Edit a gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        gadget = resourceGadgetsServer.getGadgetsContainer().getGadgetByUuid(uuid)
        if gadget == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            data = gadget.getPGData(language)
            contentStruct['root']['data'] = data
            contentStruct['root']['skin'] = "devel"
            contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/devel/xsl/gadget_edit.xsl"
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelGadgetEdit)

# ------------------------------------------------------------------------------
# Declaration of the service "gadget_duplicate".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelGadgetDuplicate(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "gadget_duplicate"
        self.comment = "Duplicate a gadget."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        gadget = resourceGadgetsServer.getGadgetsContainer().getGadgetByUuid(uuid)
        if gadget == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            tmpGadgetUrl, nUuid = GadgetGenerator.duplicateGadget(gadget, language, resourcesManager)
            resourceWIDevel.lastGeneratedGadgetUuid = nUuid
            resourceGadgetsServer.insertTemporaryServerGadgetInContainer(tmpGadgetUrl)
            contentStruct['root']['skin'] = "devel"
            contentStruct['root']['language'] = language
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelGadgetDuplicate)

# ------------------------------------------------------------------------------
# Declaration of the service "ugc_duplicate".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelUgcDuplicate(TDSService):

    def configure(self):
        self.parametersDict = {
            'uuid' : 'string',
            'language' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "ugc_duplicate"
        self.comment = "Duplicate an UGC."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        uuid = parameters['uuid']
        language = parameters['language']
        ugc = resourceUgcServer.getUgcContainer().getUgcByUuid(uuid)
        if ugc == None:
            contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
        else:
            tmpUgcUrl, nUuid = GadgetGenerator.duplicateUgc(ugc, resourcesManager)
            resourceWIDevel.lastGeneratedGadgetUuid = nUuid
            resourceUgcServer.insertTemporaryServedUgcInContainer(tmpUgcUrl)
            contentStruct['root']['skin'] = "devel"
            contentStruct['root']['language'] = language
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelUgcDuplicate)

# ------------------------------------------------------------------------------
# Declaration of the service "index".
# ------------------------------------------------------------------------------
class TDSServiceWIDevelIndex(TDSService):

    def configure(self):
        self.parametersDict = {
            'language' : 'string',
            'skin' : 'string',
            'menu' : 'string',
            'firstUuid' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "index"
        self.comment = "Show the main devel page."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        language = parameters['language']
        skin = parameters['skin']
        menu = parameters['menu']
        firstUuid = parameters['firstUuid']
        data = {}
        data['elements'] = {}
        if menu == "plugins":
            pluginsContainer = resourcePluginsServer.getPluginsContainer()
            for i, plugin in enumerate(pluginsContainer.getPlugins()):
                elementName = "plugin_%.2d" % i
                pluginData = plugin.getData(language)
                data['elements'][elementName] = {}
                data['elements'][elementName]['iconFile'] = pluginData['description']['iconFile']
                data['elements'][elementName]['uuid'] = plugin.getDescription().getUuid()
                data['elements'][elementName]['translatedName'] = pluginData['description']['translatedName']
        elif menu == "gadgets":
            gadgetsContainer = resourceGadgetsServer.getGadgetsContainer()
            for i, gadget in enumerate(gadgetsContainer.getGadgets()):
                elementName = "gadget_%.2d" % i
                gadgetData = gadget.getData(language)
                data['elements'][elementName] = {}
                data['elements'][elementName]['iconFile'] = gadgetData['description']['iconFile']
                data['elements'][elementName]['uuid'] = gadget.getDescription().getUuid()
                data['elements'][elementName]['translatedName'] = gadgetData['description']['translatedName']
        elif menu == "ugcs":
            ugcContainer = resourceUgcServer.getUgcContainer()
            for i, ugc in enumerate(ugcContainer.getUgcs()):
                elementName = "ugc_%.2d" % i
                ugcData = ugc.getData(language)
                data['elements'][elementName] = {}
                data['elements'][elementName]['iconFile'] = ugcData['description']['iconFile']
                data['elements'][elementName]['uuid'] = ugc.getDescription().getUuid()
                data['elements'][elementName]['translatedName'] = ugcData['description']['translatedName']
        contentStruct['root']['data'] = data
        contentStruct['root']['skin'] = skin
        contentStruct['root']['menu'] = menu
        if resourceWIDevel.lastGeneratedGadgetUuid != None:
            firstUuid = resourceWIDevel.lastGeneratedGadgetUuid
            resourceWIDevel.lastGeneratedGadgetUuid = None
        contentStruct['root']['firstUuid'] = firstUuid
        contentStruct['root']['language'] = language
        self.haveXsl = True
        self.xslPath = "/data/web_interface/devel/xsl/index.xsl"
        return headersStruct, contentStruct

# Register the service into the resource
resourceWIDevel.addService(TDSServiceWIDevelIndex)
# Bind the resource index url to this service
resourcesManager.addBinding("devel", "wi_devel", "index", "skin=devel&language=en&menu=plugins&firstUuid=NULL")
resourcesManager.addBinding("devel/index", "wi_devel", "index", "skin=devel&language=en&menu=plugins&firstUuid=NULL")
