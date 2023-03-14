# ==============================================================================
# Users resource.
# ==============================================================================

from util.osl.TuxOSL import TUX_OSL_ACAPELA_LOCUTORS_BY_LANGUAGE_COUNTRY_DICT
from util.misc.tuxPaths import TUXDROID_LANGUAGE
from util.misc.tuxPaths import TUXDROID_LANGUAGE2
from util.misc.tuxPaths import TUXDROID_DEFAULT_LOCUTOR
from util.misc.tuxPaths import TUXDROID_SECOND_LOCUTOR

# ------------------------------------------------------------------------------
# Declaration of the resource "users".
# ------------------------------------------------------------------------------
class TDSResourceUsers(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "users"
        self.comment = "Resource to manage the users configurations."
        self.fileName = RESOURCE_FILENAME
        # Ensure that the users_conf directory exists
        DirectoriesAndFilesTools.MKDirs(TDS_USERS_CONF_PATH)

    def start(self):
        # Read the last logged user name
        self.__lastUser = self.getLastLoggedUserName()
        # Create user directories if not exists
        self.createUserIfNotExists()
        # Load the user configuration
        self.__userConfiguration = self.loadUserConfiguration()

    # --------------------------------------------------------------------------
    # Shared methods
    # --------------------------------------------------------------------------

    def getLastLoggedUserName(self):
        """Get the name of the last logged user.
        @return: A string.
        """
        lastUserConf = os.path.join(TDS_USERS_CONF_PATH, "last_user.name")
        if not os.path.isfile(lastUserConf):
            f = open(lastUserConf, "w")
            f.write("default")
            f.close()
        f = open(lastUserConf, "r")
        result = f.read()
        f.close()
        return result

    def createUserIfNotExists(self):
        """Create the user configuration of the last selected user if not
        exists.
        """
        userName = self.__lastUser
        DirectoriesAndFilesTools.MKDirs(os.path.join(TDS_USERS_CONF_PATH,
            userName))
        DirectoriesAndFilesTools.MKDirs(os.path.join(TDS_USERS_CONF_PATH,
            userName, "gadgets"))
        DirectoriesAndFilesTools.MKDirs(os.path.join(TDS_USERS_CONF_PATH,
            userName, "attitunes"))
        DirectoriesAndFilesTools.MKDirs(os.path.join(TDS_USERS_CONF_PATH,
            userName, "ugcs"))

    def loadUserConfiguration(self):
        """Load an user configuration.
        @return: The user configuration as dictionary.
        """
        userName = self.__lastUser
        userConfFile = os.path.join(TDS_USERS_CONF_PATH, userName, "user.conf")

        # If the server has been started as normal user on Linux and
        # if the user configuration file doesn't exists, copy the master 
        # configuration located in /etc/tuxdroid/users_conf/default/user.conf
        if systemPaths.isUser() and os.name != 'nt':
            if not os.path.isfile(userConfFile):
                os.system("cp /etc/tuxdroid/users_conf/default/user.conf %s"%userConfFile)
            else:
                try:
                    f_sys = open("/etc/tuxdroid/users_conf/default/user.conf", "r")
                    dict = eval(f_sys.read())
                    f_sys.close()
                    lang_sys = dict['language1']
                except:
                    lang_sys = None
                try:
                    path = os.path.join(systemPaths.getUserConfPath(), "default", "user.conf")
                    f_user = open(path, "r")
                    dict = eval(f_user.read())
                    f_user.close()
                    lang_user = dict['language1']
                except:
                    lang_user = None 

                if lang_user != lang_sys and lang_user != None and lang_sys != None:
                    os.system("cp /etc/tuxdroid/users_conf/default/user.conf %s"%userConfFile)

        if not os.path.isfile(userConfFile):
            # Create default configuration
            splitedLC = TUXDROID_LANGUAGE.split("_")
            language = splitedLC[0]
            if len(splitedLC) > 1:
                country = splitedLC[1]
            else:
                country = language.upper()
            splitedLC = TUXDROID_LANGUAGE2.split("_")
            language2 = splitedLC[0]
            locutor = TUXDROID_DEFAULT_LOCUTOR
            locutor2 = TUXDROID_SECOND_LOCUTOR
            # Todo : Get second language and locutor
            pitch = 120
            defaultConfDict = {
                'name' : userName,
                'login' : None,
                'password' : None,
                'language1' : language,
                'language2' : language2,
                'country' : country,
                'locutor1' : locutor,
                'locutor2' : locutor2,
                'pitch' : pitch,
            }
            f = open(userConfFile, "w")
            f.write(str(defaultConfDict))
            f.close()
        # Load user configuration
        f = open(userConfFile, "r")
        result = eval(f.read())
        f.close()
        # Reference the user attitunes directory
        resourceAttituneManager.getAttitunesContainer().addDirectory(
            os.path.join(TDS_USERS_CONF_PATH, userName, "attitunes"),
            "userAttitunes")
        # Set locales in the plugins server
        resourcePluginsServer.getPluginsContainer().setLocales(
            result['language1'], result['country'],
            result['locutor1'], result['pitch'])
        # Start gadgets server
        resourceGadgetsServer.startServer()
        # Reference user gadgets directory
        resourceGadgetsServer.getGadgetsContainer().addDirectory(
            os.path.join(TDS_USERS_CONF_PATH, userName, "gadgets"))
        # Start ugc server
        resourceUgcServer.startServer(os.path.join(TDS_USERS_CONF_PATH,
            userName, "ugcs"))
        # Start the webbrowser (TuxBox)
        t = threading.Thread(target = resourcePluginsServer.startPlugin,
            args = ("63ef331b-eb82-4e4b-b246-07412191f263", "run", {}))
        t.start()
        return result

    def getCurrentUserConfiguration(self):
        """Get the current user configuration.
        @return: The current user configuration as string.
        """
        return self.__userConfiguration

    def getCurrentUserBasePath(self):
        """Get the current user base directory
        @return: A string.
        """
        userName = self.__userConfiguration['name']
        return os.path.join(TDS_USERS_CONF_PATH, userName)

    def getCurrentFirstLocutor(self):
        """
        """
        return self.__userConfiguration['locutor1'].replace("8k", "")

    def setNewFirstLocutor(self, locutor):
        """
        """
        if locutor.find("8k") == -1:
            locutor += "8k"
        if locutor == self.getCurrentFirstLocutor():
            return
        self.__userConfiguration['locutor1'] = locutor
        # Set locales in the plugins server
        resourcePluginsServer.getPluginsContainer().setLocales(
            self.__userConfiguration['language1'], self.__userConfiguration['country'],
            self.__userConfiguration['locutor1'], self.__userConfiguration['pitch'])

    def getCurrentFirstLanguage(self):
        """
        """
        return self.__userConfiguration['language1']

    def getCurrentSecondLocutor(self):
        """
        """
        return self.__userConfiguration['locutor2'].replace("8k", "")

    def getCurrentSecondLanguage(self):
        """
        """
        return self.__userConfiguration['language2']

    def getLocutorsFromFirstLanguage(self):
        """
        """
        firstLocutor = self.getCurrentFirstLocutor()
        locDict = TUX_OSL_ACAPELA_LOCUTORS_BY_LANGUAGE_COUNTRY_DICT
        for key in locDict.keys():
            if firstLocutor in locDict[key]:
                return locDict[key]
        return []

    def getCurrentPitch(self):
        """
        """
        return self.__userConfiguration['pitch']

    def setNewPitch(self, pitch):
        """
        """
        if pitch == self.getCurrentPitch():
            return
        self.__userConfiguration['pitch'] = pitch
        # Set locales in the plugins server
        resourcePluginsServer.getPluginsContainer().setLocales(
            self.__userConfiguration['language1'], self.__userConfiguration['country'],
            self.__userConfiguration['locutor1'], self.__userConfiguration['pitch'])

    def storeUserConfiguration(self):
        """
        """
        # Update configuration file
        userConfFile = os.path.join(TDS_USERS_CONF_PATH, self.__lastUser,
            "user.conf")
        f = open(userConfFile, "w")
        f.write(str(self.__userConfiguration))
        f.close()

    def updateCurrentUserConfiguration(self, userConfiguration):
        """Update the current user configuration.
        @param userConfiguration: New configuration as dictionary.
        - This function will restart the server.
        """
        # Update configuration file
        userConfFile = os.path.join(TDS_USERS_CONF_PATH, self.__lastUser,
            "user.conf")
        f = open(userConfFile, "w")
        f.write(str(userConfiguration))
        f.close()
        # Restart the server
        resourceServer.restartServer()

    def switchUser(self, userName):
        """Switch to an other user.
        @param userName: Name of the requested user.
        - This function will restart the server.
        """
        # Store the requested user name
        lastUserConf = os.path.join(TDS_USERS_CONF_PATH, "last_user.name")
        f = open(lastUserConf, "w")
        f.write(userName)
        f.close()
        # Restart the server
        resourceServer.restartServer()

# Create an instance of the resource
resourceUsers = TDSResourceUsers("resourceUsers")
# Register the resource into the resources manager
resourcesManager.addResource(resourceUsers)

# ------------------------------------------------------------------------------
# Declaration of the service "switch_user".
# ------------------------------------------------------------------------------
class TDSServiceUsersSwitchUser(TDSService):

    def configure(self):
        self.parametersDict = {
            'name' : 'string',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = False
        self.name = "switch_user"
        self.comment = "Switch to another user."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        name = parameters['name']
        resourceUsers.switchUser(name)
        return headersStruct, contentStruct

# Register the service into the resource
resourceUsers.addService(TDSServiceUsersSwitchUser)
