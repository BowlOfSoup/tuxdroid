# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import sys
import traceback
import re

from util.logger import *

from TDSClientLevels import *
from TDSService import TDSService
from TDSError import *
from TDSConfiguration import *

# ------------------------------------------------------------------------------
# Tux Droid Server : Resource class.
# ------------------------------------------------------------------------------
class TDSResource(object):
    """Tux Droid Server : Resource class.
    """

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __init__(self, instanceName):
        self.__logger = SimpleLogger(TDS_FILENAME_RESOURCES_LOG)
        self.__logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.__logger.setTarget(TDS_CONF_LOG_TARGET)
        self.logger = self.__logger
        self.__servicesDict = {}
        self.__instanceName = instanceName
        # Shared variables with the overriders
        self.name = ""
        self.comment = ""
        self.configurator = TDSResourceConf()
        self.fileName = ""
        # Configure
        self.configure()
        self.sharedMethodNamesList = []
        aElementsList = dir(TDSResource)
        oElementsList = dir(self)
        for element in oElementsList:
            if element not in aElementsList:
                if element[0] != "_":
                    if str(type(getattr(self, element)))== "<type 'instancemethod'>":
                        self.sharedMethodNamesList.append(element)

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getConfigurator(self):
        return self.configurator

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getXmlStructure(self):
        contentStruct = {
            'comment' : self.comment,
            'services' : {},
            'shared_methods' : {},
        }
        for i, sharedMethod in enumerate(self.sharedMethodNamesList):
            doc = getattr(self, sharedMethod).__doc__
            if doc == None:
                doc = {
                    'line_001' : "Not yet documented",
                }
            else:
                lines = doc.split("\n")
                doc = {}
                for j, line in enumerate(lines):
                    doc["line_%.3d" % j] = line
            infos = {
                'name' : "%s.%s" % (self.__instanceName, sharedMethod),
                'doc' : doc,
            }
            contentStruct['shared_methods']["method_%.3d" % i] = infos
        for serviceName in self.__servicesDict.keys():
            contentStruct['services'][serviceName] = \
                self.__servicesDict[serviceName].getXmlStructure()
        return contentStruct

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def configure(self):
        pass

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def start(self):
        pass

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def stop(self):
        pass

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def _doStart(self):
        keys = self.__servicesDict.keys()
        for key in keys:
            self.__logger.logInfo("Resource [%s] : Start service [%s]" % (self.name, key))
            self.__servicesDict[key].start()
            self.__logger.logInfo("Resource [%s] : Service Started [%s]" % (self.name, key))
        self.start()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def _doStop(self):
        keys = self.__servicesDict.keys()
        for key in keys:
            self.__logger.logInfo("Resource [%s] : Stop service [%s]" % (self.name, key))
            self.__servicesDict[key].stop()
            self.__logger.logInfo("Resource [%s] : Service Stopped [%s]" % (self.name, key))
        self.stop()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def addService(self, serviceClass):
        if (self.name == "") or (len(self.name) == 32):
            return
        service = serviceClass()
        self.__logger.logInfo("Resource [%s] : Registering service [%s]" % (self.name, service.name))
        if service.name == "":
            self.__logger.logError("Resource [%s] : Service must have a name ! (%s)" % (self.name, service))
            return
        if self.__servicesDict.has_key(service.name):
            self.__logger.logWarning("Resource [%s] : Duplicated service [%s]" % (self.name, service.name))
        self.__servicesDict[service.name] = service
        self.__logger.logInfo("Resource [%s] : Service registered [%s]" % (self.name, service.name))

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getService(self, serviceName):
        if self.serviceExists(serviceName):
            return self.__servicesDict[serviceName]
        else:
            return None

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def serviceExists(self, serviceName):
        return self.__servicesDict.has_key(serviceName)

# ------------------------------------------------------------------------------
# Tux Droid Server : Resource configuration class.
# ------------------------------------------------------------------------------
class TDSResourceConf(object):
    """ Tux Droid Server : Resource configuration class.
    """

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor.
        """
        self.itemsDict = {}
        self.__confFileName = "default.conf"

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getConfiguration(self):
        """Get the current configuration.
        @return: A dictionary.
        """
        return self.itemsDict

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def load(self, confFileName, defaultConfigDict = {}):
        """ Load a configuration.
        @param confFileName: File name of the configuration.
        @param defaultConfigDict: Default configuration.
        """
        self.__confFileName = confFileName
        result = defaultConfigDict
        self.itemsDict = result
        confFile = os.path.join(TDS_RESOURCES_CONF_PATH, confFileName)
        if os.path.exists(confFile):
            try:
                file = open(confFile, "rb")
                result = eval(file.read())
                file.close()
                self.itemsDict = result
            except:
                result = defaultConfigDict
        else:
            self.store()
        return result

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def store(self):
        """ Store the configuration.
        """
        confFile = os.path.join(TDS_RESOURCES_CONF_PATH, self.__confFileName)
        try:
            file = open(confFile, "w")
            file.write(str(self.itemsDict))
            file.close()
        except:
            pass

# ------------------------------------------------------------------------------
# Tux Droid Server : Resources manager.
# ------------------------------------------------------------------------------
class TDSResourcesManager(object):
    """Tux Droid Server : Resources manager.
    """

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __init__(self, accessManager, clientsManager, sGlobals):
        self.__logger = SimpleLogger(TDS_FILENAME_RESOURCES_LOG)
        self.__logger.resetLog()
        self.__logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.__logger.setTarget(TDS_CONF_LOG_TARGET)
        self.logger = self.__logger
        self.__resourcesList = []
        self.__accessManager = accessManager
        self.__clientsManager = clientsManager
        self.__sGlobals = sGlobals
        self.__bindingList = {}
        self.__servedDirectoriesStruct = {}
        self.__servedDynamicFilesStruct = {}
        self.__dynamicFilesMutex = threading.Lock()
        self.__resourcePathsList = []

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def addBinding(self, url, resourceName, serviceName, parameters = ""):
        self.__bindingList[url] = [resourceName, serviceName, parameters]
        self.__logger.logInfo("A binding has been added [%s] -> [%s]" % (url,
            "%s/%s" % (resourceName, serviceName)))

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __checkForBindedUrl(self, url):
        for bind in self.__bindingList.keys():
            if (url.find(bind) == 1) or ((bind == "ROOT") and (url == "")):
                sepIdx = url.find("?")
                if sepIdx != -1:
                    url = url[sepIdx:]
                else:
                    url = ""
                if len(url) < 2:
                    url = "?" + self.__bindingList[bind][2]
                return url, self.__bindingList[bind][0], self.__bindingList[bind][1]
        return None, None, None

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def addFileToServe(self, fileName, destUrl):
        if not os.path.isfile(fileName):
            return
        if fileName.lower().rfind(".xsl") != -1:
            headers = [['Content-type', 'text/xml; charset="utf-8"'],]
        elif fileName.lower().rfind(".html") != -1:
            headers = [['Content-type', 'html; charset="utf-8"'],]
        elif fileName.lower().rfind(".png") != -1:
            headers = [['Content-type', 'image/png; charset="utf-8"'],]
        elif fileName.lower().rfind(".js") != -1:
            headers = [['Content-type', 'js; charset="utf-8"'],]
        elif fileName.lower().rfind(".css") != -1:
            headers = [['Content-type', 'text/css; charset="utf-8"'],]
        elif fileName.lower().rfind(".gif") != -1:
            headers = [['Content-type', 'image/gif; charset="utf-8"'],]
        elif fileName.lower().rfind(".ico") != -1:
            headers = [['Content-type', 'image/x-icon; charset="utf-8"'],]
        elif fileName.lower().rfind(".scp") != -1:
            headers = [['Content-type', 'application/x-scp; charset="utf-8"'],]
        elif fileName.lower().rfind(".scg") != -1:
            headers = [['Content-type', 'application/x-scg; charset="utf-8"'],]
        elif fileName.lower().rfind(".ugc") != -1:
            headers = [['Content-type', 'application/x-bin; charset="utf-8"'],]
        else:
            return
        try:
            content = open(fileName, "rb").read()
        except:
            return
        headers.append(['Content-Length', str(len(content))])
        self.__dynamicFilesMutex.acquire()
        self.__servedDynamicFilesStruct[destUrl] = {
            'headers' : headers,
            'content' : content,
        }
        self.__dynamicFilesMutex.release()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def addContentToServe(self, content, destUrl):
        if destUrl.lower().rfind(".xsl") != -1:
            headers = [['Content-type', 'text/xml; charset="utf-8"'],]
        elif destUrl.lower().rfind(".txt") != -1:
            headers = [['Content-type', 'text; charset="utf-8"'],]
        elif destUrl.lower().rfind(".html") != -1:
            headers = [['Content-type', 'html; charset="utf-8"'],]
        elif destUrl.lower().rfind(".png") != -1:
            headers = [['Content-type', 'image/png; charset="utf-8"'],]
        elif destUrl.lower().rfind(".js") != -1:
            headers = [['Content-type', 'js; charset="utf-8"'],]
        elif destUrl.lower().rfind(".xml") != -1:
            headers = [['Content-type', 'text/xml; charset="utf-8"'],]
        elif destUrl.lower().rfind(".css") != -1:
            headers = [['Content-type', 'text/css; charset="utf-8"'],]
        elif destUrl.lower().rfind(".gif") != -1:
            headers = [['Content-type', 'image/gif; charset="utf-8"'],]
        elif destUrl.lower().rfind(".ico") != -1:
            headers = [['Content-type', 'image/x-icon; charset="utf-8"'],]
        elif destUrl.lower().rfind(".ugc") != -1:
            headers = [['Content-type', 'image/x-bin; charset="utf-8"'],]
        else:
            return
        headers.append(['Content-Length', str(len(content))])
        self.__dynamicFilesMutex.acquire()
        self.__servedDynamicFilesStruct[destUrl] = {
            'headers' : headers,
            'content' : content,
        }
        self.__dynamicFilesMutex.release()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def removeFileToServe(self, destUrl):
        self.__dynamicFilesMutex.acquire()
        if not self.__servedDynamicFilesStruct.has_key(destUrl):
            self.__dynamicFilesMutex.release()
            return
        try:
            del self.__servedDynamicFilesStruct[destUrl]
        except:
            pass
        self.__dynamicFilesMutex.release()

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getServedFileContent(self, destUrl):
        self.__dynamicFilesMutex.acquire()
        if not self.__servedDynamicFilesStruct.has_key(destUrl):
            self.__dynamicFilesMutex.release()
            return None
        try:
            result = self.__servedDynamicFilesStruct[destUrl]['content']
        except:
            result = None
        self.__dynamicFilesMutex.release()
        return result

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def addDirectoryToServe(self, path):
        filesList = {}
        diskPath = os.path.join(TDS_APPLICATION_PATH, path[1:-1])
        if not os.path.isdir(diskPath):
            return
        dirList = os.listdir(diskPath)
        for file in dirList:
            if file.lower().rfind(".xsl") != -1:
                headers = [['Content-type', 'text/xml; charset="utf-8"'],]
            elif file.lower().rfind(".html") != -1:
                headers = [['Content-type', 'html; charset="utf-8"'],]
            elif file.lower().rfind(".js") != -1:
                headers = [['Content-type', 'js; charset="utf-8"'],]
            elif file.lower().rfind(".gif") != -1:
                headers = [['Content-type', 'image/gif; charset="utf-8"'],]
            elif file.lower().rfind(".png") != -1:
                headers = [['Content-type', 'image/png; charset="utf-8"'],]
            elif file.lower().rfind(".css") != -1:
                headers = [['Content-type', 'text/css; charset="utf-8"'],]
            elif file.lower().rfind(".ico") != -1:
                headers = [['Content-type', 'image/x-icon; charset="utf-8"'],]
            else:
                continue
            filePath = os.path.join(diskPath, file)
            content = open(filePath, "rb").read()
            headers.append(['Content-Length', str(len(content))])
            filesList[file] = {
                'headers' : headers,
                'content' : content,
            }
        if len(filesList.keys()) == 0:
            return
        self.__servedDirectoriesStruct[path] = {
            'diskPath' : diskPath,
            'filesList' : filesList,
        }
        self.__logger.logInfo("Added a directory to serve [%s]" % diskPath)

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __checkForServedFile(self, url):
        self.__dynamicFilesMutex.acquire()
        if self.__servedDynamicFilesStruct.has_key(url):
            result = self.__servedDynamicFilesStruct[url]['headers'], \
                self.__servedDynamicFilesStruct[url]['content']
            self.__dynamicFilesMutex.release()
            return result
        self.__dynamicFilesMutex.release()
        for key in self.__servedDirectoriesStruct.keys():
            if url.find(key) == 0:
                fileToMatch = url[len(key):]
                for file in self.__servedDirectoriesStruct[key]['filesList'].keys():
                    if fileToMatch == file:
                        return self.__servedDirectoriesStruct[key]['filesList'][file]['headers'], \
                            self.__servedDirectoriesStruct[key]['filesList'][file]['content']
        return None, None

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def load(self, resourcesPath):
        paths = []
        for path in os.listdir(resourcesPath):
            if path.find(".") == -1:
                paths.append(os.path.join(resourcesPath, path))
        paths.sort()
        self.__resourcePathsList = paths
        for resourcePath in paths:
            resourceList = os.listdir(resourcePath)
            resourceList.sort()
            for resource in resourceList:
                if resource.lower().rfind(".py") != -1:
                    resourceFile = os.path.join(resourcePath, resource)
                    try:
                        str = open(resourceFile, 'r').read()
                        self.__sGlobals['RESOURCE_FILENAME'] = resourceFile
                        exec(str) in self.__sGlobals
                    except:
                        self.__logger.logError("Error in the resource file [%s]" % resourceFile)
                        self.__logger.logError(self.__formatException())
            if TDS_ONLY_BASE_RESOURCES:
                break

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getResourcePathsList(self):
        return self.__resourcePathsList

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def addResource(self, resource):
        self.__logger.logInfo("Registering resource [%s]" % resource.name)
        if resource.name == "":
            self.__logger.logError("Resource must have a name ! (%s)" % resource)
            return
        if len(resource.name) == 32:
            self.__logger.logError("Resource name must be != of 32 (%s)" % resource.name)
            return
        for regResource in self.__resourcesList:
            if regResource[0] == resource.name:
                self.__logger.logWarning("Duplicated resource [%s]" % resource.name)
                return
        regResource = [
            resource.name,
            resource,
        ]
        self.__resourcesList.append(regResource)
        self.__logger.logInfo("Resource registered [%s]" % resource.name)

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getResource(self, resourceName):
        for regResource in self.__resourcesList:
            if regResource[0] == resourceName:
                return regResource[1]
        return None

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getResourcesList(self):
        result = []
        for regResource in self.__resourcesList:
            result.append(regResource[0])
        return result

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def resourceExists(self, resourceName):
        for regResource in self.__resourcesList:
            if regResource[0] == resourceName:
                return True
        return False

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def start(self):
        for regResource in self.__resourcesList:
            self.__logger.logInfo("Start resource [%s]" % regResource[0])
            regResource[1]._doStart()
            self.__logger.logInfo("Resource started [%s]" % regResource[0])

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def stop(self):
        self.__resourcesList.reverse()
        for regResource in self.__resourcesList:
            self.__logger.logInfo("Stop resource [%s]" % regResource[0])
            regResource[1]._doStop()
            self.__logger.logInfo("Resource stopped [%s]" % regResource[0])

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def executeUrl(self, urlString):
        headers = None
        contentXml = None
        # Check for served files
        h, c = self.__checkForServedFile(urlString)
        if h != None:
            return 200, h, c
        # Parse the urlString
        clientId, resourceName, serviceName, parameters = self.__parseUrl(urlString)
        # Check the client and level
        if clientId == "-1":
            clientLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        elif clientId == "0":
            clientLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        else:
            clientLevel = self.__clientsManager.getClientLevel(clientId)
        if clientLevel == None:
            # Client not found !
            return 404, None, None
        # Get the resource object
        resource = self.getResource(resourceName)
        if resource == None:
            return 404, None, None
        # Get the service object
        service = resource.getService(serviceName)
        if service == None:
            return 404, None, None
        # Get the service minimal level
        serviceLevel = service.minimalUserLevel
        # Check the client level
        if not checkClientLevel(clientLevel, serviceLevel):
            headers = service.getDefaultHeadersStruct()
            contentXml = service.getDefaultContentXml()
            return 200, headers, contentXml
        # Check the access only when the client level is RESTRICTED and the
        # minimal service access is ANONYMOUS
        if (clientLevel == TDS_CLIENT_LEVEL_RESTRICTED) and \
           (serviceLevel == TDS_CLIENT_LEVEL_ANONYMOUS):
            # Check the client access
            if not self.__accessManager.checkUserHaveAccess(clientId):
                headers = service.getDefaultHeadersStruct()
                contentXml = service.getDefaultContentXml()
                return 200, headers, contentXml
        # Excecute the service
        headers, contentXml = service._doExecute(clientId, parameters)
        return 200, headers, contentXml

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __parseUrl(self, urlString):
        clientId = "-1"
        resourceName = None
        serviceName = None
        parameters = {}
        # Get the user id
        tmpUrlString = urlString
        if tmpUrlString[0] == "/":
            tmpUrlString = tmpUrlString[1:]
            sepIdx = tmpUrlString.find("/")
            if sepIdx != -1:
                clientId = tmpUrlString[:sepIdx]
                tmpUrlString = tmpUrlString[sepIdx:]
        else:
            return clientId, resourceName, serviceName, parameters
        if (clientId == "-1") or (clientId == "0"):
            urlString = tmpUrlString
        else:
            if len(clientId) == 32:
                urlString = tmpUrlString
            else:
                clientId = "-1"
        sUrl, resourceName, serviceName = self.__checkForBindedUrl(urlString)
        if sUrl == None:
            # Get the resource name
            if urlString[0] == "/":
                urlString = urlString[1:]
                sepIdx = urlString.find("/")
                if sepIdx != -1:
                    resourceName = urlString[:sepIdx]
                    urlString = urlString[sepIdx:]
                else:
                    return clientId, resourceName, serviceName, parameters
            else:
                return clientId, resourceName, serviceName, parameters
            # Get the service name
            if urlString[0] == "/":
                urlString = urlString[1:]
                sepIdx = urlString.find("?")
                if sepIdx != -1:
                    serviceName = urlString[:sepIdx]
                    urlString = urlString[sepIdx:]
                else:
                    return clientId, resourceName, serviceName, parameters
            else:
                return clientId, resourceName, serviceName, parameters
        else:
            urlString = sUrl
        # Get the parameters
        if len(urlString) == 0:
            return clientId, resourceName, serviceName, parameters
        if urlString[0] == "?":
            urlString = urlString[1:]
        urlString = urlString.replace("&&", "#amp;")
        while 1:
            equIdx = urlString.find("=")
            if equIdx == -1:
                break
            paramName = urlString[:equIdx].replace("#amp;", "&")
            urlString = urlString[equIdx + 1:]
            sepIdx = urlString.find("&")
            if sepIdx == -1:
                # This is the last parameter
                paramValue = urlString
                parameters[paramName] = paramValue.replace("#amp;", "&")
                break
            else:
                paramValue = urlString[:sepIdx]
                parameters[paramName] = paramValue.replace("#amp;", "&")
                urlString = urlString[sepIdx + 1:]
        return clientId, resourceName, serviceName, parameters

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __formatException(self):
        fList = traceback.format_exception(sys.exc_info()[0],
                    sys.exc_info()[1],
                    sys.exc_info()[2])
        result = ""
        for line in fList:
            result += line
        return result
