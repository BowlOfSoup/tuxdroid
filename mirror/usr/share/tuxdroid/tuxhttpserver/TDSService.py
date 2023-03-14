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
import threading

from util.logger import *

from TDSClientLevels import *
from TDSError import *
from TDSConfiguration import *

# ------------------------------------------------------------------------------
# Tux Droid Server : Service class.
# ------------------------------------------------------------------------------
class TDSService(object):
    """Tux Droid Server : Service class.
    """

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__logger = SimpleLogger(TDS_FILENAME_RESOURCES_LOG)
        self.__logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.__logger.setTarget(TDS_CONF_LOG_TARGET)
        self.logger = self.__logger
        self.__mutex = threading.Lock()
        self.__defaultContentXml = ""
        # Shared variables with the overriders
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = ""
        self.comment = ""
        self.haveXsl = False
        self.xslPath = ""
        # Configure
        self.configure()
        self.__defaultContentXml = self.__contentStructToXml(self.getDefaultContentStruct())

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getXmlStructure(self):
        contentStruct = {
            'comment' : self.comment,
            'exclusiveExecution' : str(self.exclusiveExecution),
            'minimalUserLevel' : getClientLevelName(self.minimalUserLevel),
        }
        paramString = ""
        for key in self.parametersDict.keys():
            value = self.parametersDict[key]
            if value[0] == '<':
                value = value[1:-1]
            paramString += "%s=<%s>&" % (key, value)
        paramString = paramString[:-1]
        contentStruct['parameters'] = paramString
        return contentStruct

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def execute(self, id, parameters):
        pass

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
    def _doExecute(self, id, parameters):
        if self.exclusiveExecution:
            self.__mutex.acquire()
        # Parse and check parameters
        isValid, parameters = self.__parseAndCheckParameters(parameters)
        if isValid:
            # Do execute the overrided executor
            try:
                headersStruct, contentStruct = self.execute(id, parameters)
            except:
                headersStruct = self.getDefaultHeadersStruct()
                contentStruct = self.getDefaultContentStruct()
                contentStruct['root']['result'] = getStrError(E_TDREST_FAILED)
                self.__logger.logError("Bugged service : (%s)" % self.name)
                self.__logger.logError(self.__formatException())
        else:
            headersStruct = self.getDefaultHeadersStruct()
            contentStruct = self.getDefaultContentStruct()
            contentStruct['root']['result'] = getStrError(E_TDREST_INVALIDPARAMETERS)
        if self.exclusiveExecution:
            self.__mutex.release()
        content = self.__contentStructToXml(contentStruct)
        return headersStruct, content

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __contentStructToXml(self, contentStruct):
        def recurse(struct):
            keys = struct.keys()
            keys.sort()
            result = ""
            for key in keys:
                if str(type(struct[key])) <> "<type 'dict'>":
                    nodeValue = str(struct[key])
                    if nodeValue == "":
                        nodeValue = " "
                    else:
                        nodeValue = nodeValue.replace("&", "&amp;")
                        nodeValue = nodeValue.replace("<", "&#60;")
                        nodeValue = nodeValue.replace(">", "&#62;")
                    result += "<%s>%s</%s>" % (key, nodeValue, key)
                else:
                    nodeName = key
                    if nodeName.find("|") != -1:
                        nodeName = nodeName[:nodeName.find("|")]
                    result += "<%s>" % nodeName
                    result += recurse(struct[key])
                    result += "</%s>" % nodeName
            return result
        result = '<?xml version="1.0" encoding="UTF-8"?>'
        if self.haveXsl:
            result += '<?xml-stylesheet type="text/xsl" href="%s"?>' % self.xslPath
        result += recurse(contentStruct)
        return result

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getContentXmlFromStructure(self, contentStruct):
        return self.__contentStructToXml(contentStruct)

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def __parseAndCheckParameters(self, parameters):
        result = {}
        for key in self.parametersDict.keys():
            if parameters.has_key(key):
                try:
                    value = eval(parameters[key])
                except:
                    value = parameters[key]
                fmt = self.parametersDict[key]
                if fmt == "uint8":
                    if str(type(value)) == "<type 'int'>":
                        if (value >= 0) and (value <= 255):
                            result[key] = value
                        else:
                            self.__logger.logDebug("Service [%s] : Invalid parameter value range (%s in 0..255)" % (self.name, key))
                            return False, {}
                    else:
                        self.__logger.logDebug("Service [%s] : Bad parameter format (%s is '%s')" % (self.name, key, fmt))
                        return False, {}
                elif fmt == "int8":
                    if str(type(value)) == "<type 'int'>":
                        if (value >= -128) and (value <= 127):
                            result[key] = value
                        else:
                            self.__logger.logDebug("Service [%s] : Invalid parameter value range (%s in -128..127)" % (self.name, key))
                            return False, {}
                    else:
                        self.__logger.logDebug("Service [%s] : Bad parameter format (%s is '%s')" % (self.name, key, fmt))
                        return False, {}
                elif fmt == "int":
                    if str(type(value)) == "<type 'int'>":
                        result[key] = value
                    else:
                        self.__logger.logDebug("Service [%s] : Bad parameter format (%s is '%s')" % (self.name, key, fmt))
                        return False, {}
                elif fmt == "float":
                    if str(type(value)) == "<type 'float'>":
                        result[key] = value
                    else:
                        self.__logger.logDebug("Service [%s] : Bad parameter format (%s is '%s')" % (self.name, key, fmt))
                        return False, {}
                elif fmt == "bool":
                    if str(type(value)) == "<type 'bool'>":
                        result[key] = value
                    else:
                        self.__logger.logDebug("Service [%s] : Bad parameter format (%s is '%s')" % (self.name, key, fmt))
                        return False, {}
                elif fmt == "string":
                    if str(type(value)) == "<type 'str'>":
                        result[key] = value
                    else:
                        self.__logger.logDebug("Service [%s] : Bad parameter format (%s is '%s')" % (self.name, key, fmt))
                        return False, {}
                elif fmt.find("<") == 0:
                    if str(type(value)) != "<type 'str'>":
                        value = str(value)
                    ide = fmt.find(">")
                    fmt = fmt[1:ide]
                    vals = fmt.split("|")
                    if value in vals:
                        result[key] = value
                    else:
                        self.__logger.logDebug("Service [%s] : Bad parameter value (%s in %s)" % (self.name, key, fmt))
                        return False, {}
                elif fmt == "all":
                    result[key] = str(value)
                else:
                    self.__logger.logDebug("Service [%s] : Bad parameter format (%s is '%s')" % (self.name, key, fmt))
                    return False, {}
            else:
                self.__logger.logDebug("Service [%s] : Missing parameter (%s)" % (self.name, key))
                return False, {}
        return True, result

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getDefaultHeadersStruct(self):
        return [
            ['Content-type', 'text/xml; charset="utf-8"'],
            ['Connection', 'close'],
        ]

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getDefaultContentStruct(self):
        return {
            'root' : {
                'result' : getStrError(E_TDREST_ACCESSDENIED),
            },
        }

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getDefaultContentXml(self):
        return self.__defaultContentXml

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
