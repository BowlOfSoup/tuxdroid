#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import time
import random
import zipfile
import copy

try:
    from hashlib import md5
except:
    from md5 import md5

from util.misc.DirectoriesAndFilesTools import *
from Gadget import Gadget
from util.applicationserver.ugc.Ugc import Ugc

# ------------------------------------------------------------------------------
# Gadget generator static class.
# ------------------------------------------------------------------------------
class GadgetGenerator(object):
    """Gadget generator static class.
    """

    # --------------------------------------------------------------------------
    # Make a regular data dictionary from the request data.
    # --------------------------------------------------------------------------
    def requestDataToDict(requestData, parentPG):
        """Make a regular data dictionary from the request data.
        @param requestData: Data from the request.
        @param parentPG: Parent plugin or gadget.
        @return: A dictionary.
        """
        def parseElement(element, elementsDict, endsWith):
            if element.find(endsWith) == len(element) - len(endsWith):
                name = element[:-len(endsWith)]
                if not elementsDict.has_key(name):
                    elementsDict[name] = {}
                return True, name
            return False, None

        def fillDictKey(dict, name, name2, value):
            if not dict.has_key(name):
                dict[name] = {}
            dict[name][name2] = value

        def timeDictToString(dict):
            result = "%.2d:%.2d:%.2d" % (int(dict['hour']), int(dict['minute']),
                int(dict['second']))
            return result

        def dateDictToString(dict):
            result = "%.4d/%.2d/%.2d" % (int(dict['year']), int(dict['month']),
                int(dict['day']))
            return result

        def weekMaskDictToString(dict):
            result = ""
            for i in range(7):
                if len(result) > 0:
                    result += ","
                result += str(dict["day_%d" % i]).lower()
            return result

        result = {}
        # Remove "req_" prefix
        for i, e in enumerate(requestData):
            requestData[i][0] = e[0].replace("req_", "")
        # ALERT ATTITUNE section -----------------------------------------------
        for e in requestData:
            if e[0].find("alertAttitune") == 0:
                value = e[1]
                result["alertAttitune"] = value
                break
        # DESCRIPTION section --------------------------------------------------
        # Get gadget description elements
        gadgetDescription = {}
        for e in requestData:
            if e[0].find("gadget_") == 0:
                name = e[0].replace("gadget_", "")
                value = e[1]
                gadgetDescription[name] = value
        result["description"] = gadgetDescription
        # PARAMETERS section ---------------------------------------------------
        # Get gadget parameters elements
        gadgetParameters = {}
        for e in requestData:
            if e[0].find("param_") == 0:
                paramE = e[0].replace("param_", "")
                value = e[1]
                found, name = parseElement(paramE, gadgetParameters, "_visible")
                if found:
                    gadgetParameters[name]["visible"] = value
                    continue
                found, name = parseElement(paramE, gadgetParameters, "_value")
                if found:
                    gadgetParameters[name]["value"] = value
        affinedGadgetParameters = {}
        i = 0
        for parameterName in gadgetParameters.keys():
            if parameterName.replace(" ", "") == "":
                continue
            parameterData = gadgetParameters[parameterName]
            nodeName = "param_%.2d" % i
            i += 1
            affinedGadgetParameters[nodeName] = {}
            affinedGadgetParameters[nodeName]['name'] = parameterName
            affinedGadgetParameters[nodeName]['defaultValue'] = parameterData['value']
            affinedGadgetParameters[nodeName]['visible'] = parameterData['visible']
        result["parameters"] = affinedGadgetParameters
        # TASKS section --------------------------------------------------------
        # Get the plugin tasks
        gadgetTasks = {}
        for e in requestData:
            if e[0].find("task_") == 0:
                taskE = e[0].replace("task_", "")
                value = e[1]
                # Is visible
                found, name = parseElement(taskE, gadgetTasks, "_visible")
                if found:
                    gadgetTasks[name]["visible"] = value
                    continue
                # Is activated
                found, name = parseElement(taskE, gadgetTasks, "_activated")
                if found:
                    gadgetTasks[name]["activated"] = value
                    continue
                # Date
                found, name = parseElement(taskE, gadgetTasks, "_date_year")
                if found:
                    fillDictKey(gadgetTasks[name], "date", "year", value)
                    continue
                found, name = parseElement(taskE, gadgetTasks, "_date_month")
                if found:
                    fillDictKey(gadgetTasks[name], "date", "month", value)
                    continue
                found, name = parseElement(taskE, gadgetTasks, "_date_day")
                if found:
                    fillDictKey(gadgetTasks[name], "date", "day", value)
                    continue
                # Hours begin
                found, name = parseElement(taskE, gadgetTasks, "_hoursBegin_hour")
                if found:
                    fillDictKey(gadgetTasks[name], "hoursBegin", "hour", value)
                    continue
                found, name = parseElement(taskE, gadgetTasks, "_hoursBegin_minute")
                if found:
                    fillDictKey(gadgetTasks[name], "hoursBegin", "minute", value)
                    continue
                found, name = parseElement(taskE, gadgetTasks, "_hoursBegin_second")
                if found:
                    fillDictKey(gadgetTasks[name], "hoursBegin", "second", value)
                    continue
                # Hours end
                found, name = parseElement(taskE, gadgetTasks, "_hoursEnd_hour")
                if found:
                    fillDictKey(gadgetTasks[name], "hoursEnd", "hour", value)
                    continue
                found, name = parseElement(taskE, gadgetTasks, "_hoursEnd_minute")
                if found:
                    fillDictKey(gadgetTasks[name], "hoursEnd", "minute", value)
                    continue
                found, name = parseElement(taskE, gadgetTasks, "_hoursEnd_second")
                if found:
                    fillDictKey(gadgetTasks[name], "hoursEnd", "second", value)
                    continue
                # Delay
                found, name = parseElement(taskE, gadgetTasks, "_delay_hour")
                if found:
                    fillDictKey(gadgetTasks[name], "delay", "hour", value)
                    continue
                found, name = parseElement(taskE, gadgetTasks, "_delay_minute")
                if found:
                    fillDictKey(gadgetTasks[name], "delay", "minute", value)
                    continue
                found, name = parseElement(taskE, gadgetTasks, "_delay_second")
                if found:
                    fillDictKey(gadgetTasks[name], "delay", "second", value)
                    continue
                # Week mask : flat
                for i in range(7):
                    found, name = parseElement(taskE, gadgetTasks, "_weekMask_day_%d" % i)
                    if found:
                        fillDictKey(gadgetTasks[name], "weekMask", "day_%d" % i, value)
                        continue
                # Week mask : weekpart
                found, name = parseElement(taskE, gadgetTasks, "_weekMask_weekpart")
                if found:
                    for i in range(7):
                        fillDictKey(gadgetTasks[name], "weekMask", "day_%d" % i, True)
                    if value == '1':
                        fillDictKey(gadgetTasks[name], "weekMask", "day_5", False)
                        fillDictKey(gadgetTasks[name], "weekMask", "day_6", False)
                    elif value == '2':
                        fillDictKey(gadgetTasks[name], "weekMask", "day_0", False)
                        fillDictKey(gadgetTasks[name], "weekMask", "day_1", False)
                        fillDictKey(gadgetTasks[name], "weekMask", "day_2", False)
                        fillDictKey(gadgetTasks[name], "weekMask", "day_3", False)
                        fillDictKey(gadgetTasks[name], "weekMask", "day_4", False)
                    continue
                # Week mask : exclusive
                found, name = parseElement(taskE, gadgetTasks, "_weekMask_exclusive")
                if found:
                    for i in range(7):
                        fillDictKey(gadgetTasks[name], "weekMask", "day_%d" % i, False)
                    fillDictKey(gadgetTasks[name], "weekMask", "day_" + value, True)
        # Affine tasks list
        AffinedGadgetTasks = {}
        i = 0
        for taskName in gadgetTasks.keys():
            taskData = gadgetTasks[taskName]
            if taskData['visible'] == "true":
                originalTaskObj = parentPG.getTask(taskName)
                nodeName = "task_%.2d" % i
                i += 1
                AffinedGadgetTasks[nodeName] = {}
                # Add name
                AffinedGadgetTasks[nodeName]['name'] = taskName
                # Add activated
                AffinedGadgetTasks[nodeName]['activated'] = taskData['activated']
                # Affine date data
                AffinedGadgetTasks[nodeName]['date'] = {}
                if taskData.has_key('date'):
                    AffinedGadgetTasks[nodeName]['date'] = dateDictToString(taskData['date'])
                else:
                    AffinedGadgetTasks[nodeName]['date'] = originalTaskObj.getDate()
                # Affine hoursBegin data
                hoursBegin = {}
                originalHoursBegin = originalTaskObj.getTimeDict(originalTaskObj.getHoursBegin())
                if taskData.has_key('hoursBegin'):
                    if taskData['hoursBegin'].has_key('hour'):
                        hoursBegin['hour'] = taskData['hoursBegin']['hour']
                    else:
                        hoursBegin['hour'] = originalHoursBegin['hour']
                    if taskData['hoursBegin'].has_key('minute'):
                        hoursBegin['minute'] = taskData['hoursBegin']['minute']
                    else:
                        hoursBegin['minute'] = originalHoursBegin['minute']
                    if taskData['hoursBegin'].has_key('second'):
                        hoursBegin['second'] = taskData['hoursBegin']['second']
                    else:
                        hoursBegin['second'] = originalHoursBegin['second']
                else:
                    hoursBegin = originalHoursBegin
                AffinedGadgetTasks[nodeName]['hoursBegin'] = timeDictToString(hoursBegin)
                # Affine hoursEnd data
                hoursEnd = {}
                originalHoursEnd = originalTaskObj.getTimeDict(originalTaskObj.getHoursEnd())
                if taskData.has_key('hoursEnd'):
                    if taskData['hoursEnd'].has_key('hour'):
                        hoursEnd['hour'] = taskData['hoursEnd']['hour']
                    else:
                        hoursEnd['hour'] = originalHoursEnd['hour']
                    if taskData['hoursEnd'].has_key('minute'):
                        hoursEnd['minute'] = taskData['hoursEnd']['minute']
                    else:
                        hoursEnd['minute'] = originalHoursEnd['minute']
                    if taskData['hoursEnd'].has_key('second'):
                        hoursEnd['second'] = taskData['hoursEnd']['second']
                    else:
                        hoursEnd['second'] = originalHoursEnd['second']
                else:
                    hoursEnd = originalHoursEnd
                AffinedGadgetTasks[nodeName]['hoursEnd'] = timeDictToString(hoursEnd)
                # Affine delay data
                delay = {}
                originalDelay = originalTaskObj.getTimeDict(originalTaskObj.getDelay())
                if taskData.has_key('delay'):
                    if taskData['delay'].has_key('hour'):
                        delay['hour'] = taskData['delay']['hour']
                    else:
                        delay['hour'] = originalDelay['hour']
                    if taskData['delay'].has_key('minute'):
                        minutesInt = int(taskData['delay']['minute'])
                        if minutesInt >= 60:
                            delay['hour'] = "%.2d" % int(minutesInt / 60)
                            delay['minute'] = "%.2d" % int(minutesInt % 60)
                        else:
                            delay['minute'] = taskData['delay']['minute']
                    else:
                        delay['minute'] = originalDelay['minute']
                    if taskData['delay'].has_key('second'):
                        delay['second'] = taskData['delay']['second']
                    else:
                        delay['second'] = originalDelay['second']
                else:
                    delay = originalDelay
                AffinedGadgetTasks[nodeName]['delay'] = timeDictToString(delay)
                # Add weekMask
                weekMask = {}
                if taskData.has_key('weekMask'):
                    weekMask = taskData['weekMask']
                else:
                    weekMask = originalTaskObj.getWeekMaskDict()
                AffinedGadgetTasks[nodeName]['weekMask'] = weekMaskDictToString(weekMask)
        result["tasks"] = AffinedGadgetTasks
        return result

    # --------------------------------------------------------------------------
    # Make a dictionary with the resulting data of a request of a gadget
    # creation.
    # --------------------------------------------------------------------------
    def pluginToGadgetRequestDataToDict(requestData, plugin):
        """Make a dictionary with the resulting data of a request of a gadget
        creation.
        @param requestData: Data from the request.
        @param plugin: Parent plugin.
        @return: A dictionary.
        """
        result = GadgetGenerator.requestDataToDict(requestData, plugin)
        iconFileName = ""
        helpContent = ""
        # DESCRIPTION section --------------------------------------------------
        # Get icon file
        iconFileName = result['description']['iconFile']
        result['description']['iconFile'] = "gadget.png"
        # Add platform
        result["description"]['platform'] = plugin.getDescription().getPlatform()
        # HELP WIKI content ----------------------------------------------------
        # Get the wiki help text
        for e in requestData:
            if e[0].find("helpContent") == 0:
                helpContent = e[1]
        # PARENTPLUGIN section -------------------------------------------------
        parentPlugin = {}
        parentPlugin['uuid'] = plugin.getDescription().getUuid()
        parentPlugin['version'] = plugin.getDescription().getVersion()
        parentPlugin['url'] = "http://ftp.kysoh.com/"
        result["parentPlugin"] = parentPlugin
        return result, iconFileName, helpContent

    # --------------------------------------------------------------------------
    # Generate a single id.
    # --------------------------------------------------------------------------
    def generateSingleUuid():
        """Generate a single uuid.
        @return: The single uuid.
        """
        baseString = str(time.time() + random.random())
        md5H = md5()
        md5H.update(baseString)
        id = md5H.hexdigest()
        uuid = id[:8] + '-' + id[8:12] + '-' + id[12:16] + '-' + id[16:20] + \
            '-'+id[20:]
        return uuid

    # --------------------------------------------------------------------------
    # Create the xml content from a gadget dictionary.
    # --------------------------------------------------------------------------
    def gadgetDictToXml(gadgetDict):
        """Create the xml content from a gadget dictionary.
        @param gadgetDict: Gadget dictionary.
        @return: The xml content.
        """
        def recurse(struct, identation = ""):
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
                    nodeValue = nodeValue.decode("utf-8")
                    key = key.decode("utf-8")
                    result += "%s<%s>%s</%s>\n" % (identation, key, nodeValue, key)
                else:
                    nodeName = key
                    if nodeName.find("|") != -1:
                        nodeName = nodeName[:nodeName.find("|")]
                    result += "%s<%s>\n" % (identation, nodeName)
                    result += recurse(struct[key], identation + "    ")
                    result += "%s</%s>\n" % (identation, nodeName)
            return result
        result = ""
        result += recurse(gadgetDict)
        return result.encode("utf-8")

    # --------------------------------------------------------------------------
    # Generate the gadget file.
    # --------------------------------------------------------------------------
    def generateGadget(oUuid, requestData, plugin, resourcesManager):
        """Generate the gadget file.
        @param oUuid: Original uuid of the gadget.
        @param requestData: Data from the request.
        @param plugin: Parent plugin.
        @param resourcesManager: Resources manager of the host server.
        @return: The url of the served gadget scg file and its uuid.
        """
        if oUuid != 'NULL':
            gadgetUuid = oUuid
        else:
            gadgetUuid = GadgetGenerator.generateSingleUuid()
        gadgetInfoDict, iconFileName, helpFileContent = GadgetGenerator.pluginToGadgetRequestDataToDict(requestData, plugin)
        # Complete info dict to create a gadget.xml
        gadgetInfoDict['description']['uuid'] = gadgetUuid
        # Remove language parameter
        if gadgetInfoDict.has_key("parameters"):
            for key in gadgetInfoDict['parameters'].keys():
                if gadgetInfoDict['parameters'][key]['name'] == 'locutor':
                    gadgetInfoDict['parameters'][key]["defaultValue"] = ''
                    break
        gadgetXmlDict = {
            'gadget' : gadgetInfoDict
        }
        gadgetXmlFileContent = GadgetGenerator.gadgetDictToXml(gadgetXmlDict)
        # Get the icon
        locationType = "SMARTSERVER"
        if os.path.isfile(iconFileName):
            if iconFileName.lower().find(".png") == len(iconFileName) - 4:
                locationType = "HARDDRIVE"
        if locationType == "HARDDRIVE":
            gadgetIconFileContent = open(iconFileName, "rb").read()
        else:
            gadgetIconFileContent = resourcesManager.getServedFileContent(iconFileName)
        # Create the "gadget.pot" content
        gadgetPotFileContent = 'msgid "%s"\n' % gadgetInfoDict['description']['name'].replace('"', '\\"')
        gadgetPotFileContent += 'msgstr ""\n\n'
        gadgetPotFileContent += 'msgid "%s"\n' % gadgetInfoDict['description']['ttsName'].replace('"', '\\"')
        gadgetPotFileContent += 'msgstr ""\n\n'
        gadgetPotFileContent += 'msgid "%s"\n' % gadgetInfoDict['description']['description'].replace('"', '\\"')
        gadgetPotFileContent += 'msgstr ""\n'
        # Create the archive
        tmpRootDir = os.path.join(GetOSTMPDir(), "tmpGadgetGen")
        MKDirs(tmpRootDir)
        tmpFile = open(os.path.join(tmpRootDir, "gadget.xml"), "w")
        tmpFile.write(gadgetXmlFileContent)
        tmpFile.close()
        tmpFile = open(os.path.join(tmpRootDir, "gadget.png"), "wb")
        tmpFile.write(gadgetIconFileContent)
        tmpFile.close()
        tmpFile = open(os.path.join(tmpRootDir, "gadget.pot"), "w")
        tmpFile.write(gadgetPotFileContent)
        tmpFile.close()
        tmpFile = open(os.path.join(tmpRootDir, "help.wiki"), "w")
        tmpFile.write(helpFileContent)
        tmpFile.close()
        if os.name == 'nt':
            tmpGadgetFile = "gadget_%s.scg" % gadgetUuid
        else:
            tmpGadgetFile = "/tmp/gadget_%s.scg" % gadgetUuid
        zout = zipfile.ZipFile(tmpGadgetFile, "w")
        zout.write(os.path.join(tmpRootDir, "gadget.xml"), "gadget.xml")
        zout.write(os.path.join(tmpRootDir, "gadget.png"), "gadget.png")
        zout.write(os.path.join(tmpRootDir, "gadget.pot"), "gadget.pot")
        zout.write(os.path.join(tmpRootDir, "help.wiki"), "help.wiki")
        zout.close()
        RMDirs(tmpRootDir)
        # Serve the gadget file
        resourcesManager.addFileToServe(tmpGadgetFile, '/tmp/%s' % tmpGadgetFile)
        RMFile(tmpGadgetFile)
        return '/tmp/%s' % tmpGadgetFile, gadgetUuid

    # --------------------------------------------------------------------------
    # Duplicate a gadget.
    # --------------------------------------------------------------------------
    def duplicateGadget(gadget, language, resourcesManager):
        """Duplicate a gadget.
        @param gadget: Parent gadget.
        @param language: Language.
        @param resourcesManager: Resources manager of the host server.
        @return: The url of the served gadget scg file and its uuid.
        """
        gadgetUuid = GadgetGenerator.generateSingleUuid()
        gadgetName = gadget.getContainer().generateSingleName(
            gadget.getDescription().getTranslatedName(language), language)
        gadgetInfoDict = gadget.getDictionary()
        # Complete info dict to create a gadget.xml
        gadgetInfoDict['description']['uuid'] = gadgetUuid
        gadgetInfoDict['description']['name'] = gadgetName
        gadgetInfoDict['description']['ttsName'] = gadgetName
        # Remove language parameter
        if gadgetInfoDict.has_key("parameters"):
            for key in gadgetInfoDict['parameters'].keys():
                if gadgetInfoDict['parameters'][key]['name'] == 'locutor':
                    gadgetInfoDict['parameters'][key]["defaultValue"] = ''
                    break
        gadgetXmlDict = {
            'gadget' : gadgetInfoDict
        }
        gadgetXmlFileContent = GadgetGenerator.gadgetDictToXml(gadgetXmlDict)
        iconFileName = gadget.getData(language)['description']['iconFile']
        gadgetIconFileContent = resourcesManager.getServedFileContent(iconFileName)
        helpFileContent = gadget.getData(language)['description']['helpFile']
        # Create the "gadget.pot" content
        gadgetPotFileContent = 'msgid "%s"\n' % gadgetInfoDict['description']['name'].replace('"', '\\"')
        gadgetPotFileContent += 'msgstr ""\n\n'
        gadgetPotFileContent += 'msgid "%s"\n' % gadgetInfoDict['description']['ttsName'].replace('"', '\\"')
        gadgetPotFileContent += 'msgstr ""\n\n'
        gadgetPotFileContent += 'msgid "%s"\n' % gadgetInfoDict['description']['description'].replace('"', '\\"')
        gadgetPotFileContent += 'msgstr ""\n'
        # Create the archive
        tmpRootDir = os.path.join(GetOSTMPDir(), "tmpGadgetGen")
        MKDirs(tmpRootDir)
        tmpFile = open(os.path.join(tmpRootDir, "gadget.xml"), "w")
        tmpFile.write(gadgetXmlFileContent)
        tmpFile.close()
        tmpFile = open(os.path.join(tmpRootDir, "gadget.png"), "wb")
        tmpFile.write(gadgetIconFileContent)
        tmpFile.close()
        tmpFile = open(os.path.join(tmpRootDir, "gadget.pot"), "w")
        tmpFile.write(gadgetPotFileContent)
        tmpFile.close()
        tmpFile = open(os.path.join(tmpRootDir, "help.wiki"), "w")
        tmpFile.write(helpFileContent)
        tmpFile.close()
        tmpGadgetFile = "gadget_%s.scg" % gadgetUuid
        zout = zipfile.ZipFile(tmpGadgetFile, "w")
        zout.write(os.path.join(tmpRootDir, "gadget.xml"), "gadget.xml")
        zout.write(os.path.join(tmpRootDir, "gadget.png"), "gadget.png")
        zout.write(os.path.join(tmpRootDir, "gadget.pot"), "gadget.pot")
        zout.write(os.path.join(tmpRootDir, "help.wiki"), "help.wiki")
        zout.close()
        RMDirs(tmpRootDir)
        # Serve the gadget file
        resourcesManager.addFileToServe(tmpGadgetFile, '/tmp/%s' % tmpGadgetFile)
        RMFile(tmpGadgetFile)
        return '/tmp/%s' % tmpGadgetFile, gadgetUuid

    # --------------------------------------------------------------------------
    # Generate the preview of a gadget.
    # --------------------------------------------------------------------------
    def generatePreviewGadget(requestData, plugin, resourcesManager, language):
        """Generate the preview of a gadget.
        @param requestData: Data from the request.
        @param plugin: Parent plugin.
        @param resourcesManager: Resources manager of the host server.
        @return: The data dictionary of the preview of the gadget.
        """
        gadgetUuid = GadgetGenerator.generateSingleUuid()
        gadgetInfoDict, iconFileName, helpFileContent = GadgetGenerator.pluginToGadgetRequestDataToDict(requestData, plugin)
        # Complete info dict to create a gadget.xml
        gadgetInfoDict['description']['uuid'] = gadgetUuid
        # Get the icon
        locationType = "SMARTSERVER"
        if os.path.isfile(iconFileName):
            if iconFileName.lower().find(".png") == len(iconFileName) - 4:
                locationType = "HARDDRIVE"
        if locationType == "HARDDRIVE":
            gadgetIconFileContent = open(iconFileName, "rb").read()
        else:
            gadgetIconFileContent = resourcesManager.getServedFileContent(iconFileName)
        previewGadget = Gadget(None, gadgetInfoDict, "tmp", "tmp", plugin)
        result = previewGadget.getData(language)
        # Add temp icon
        result['description']['iconFile'] = "/tmp/gadget.png"
        resourcesManager.addContentToServe(gadgetIconFileContent, "/tmp/gadget.png")
        # Add help file
        result['description']['helpFile'] = helpFileContent
        return result

    # --------------------------------------------------------------------------
    # Generate an User Gadget Configuration from a gadget.
    # --------------------------------------------------------------------------
    def generateUgcFromGadget(gadget, ugcContainer, language, resourcesManager):
        """Generate an User Gadget Configuration from a gadget.
        @param gadget: Parent gadget.
        @param ugcContainer: UGC container.
        @param language: Language.
        @param resourcesManager: Server resources manager.
        @return: The url of the served ugc file and its uuid.
        """
        ugcUuid = GadgetGenerator.generateSingleUuid()
        ugcName = ugcContainer.generateSingleName(
            gadget.getDescription().getTranslatedName(language))
        if ugcName == gadget.getDescription().getTranslatedName(language):
            ugcTtsName = gadget.getDescription().getTtsName(language)
        else:
            ugcTtsName = ugcName
        ugcDataDict = {}
        # Creation time
        ugcDataDict['creationTime'] = time.time()
        # Default attitune for alerts introduction
        ugcDataDict['alertAttitune'] = "----"
        # Parent Gadget
        ugcDataDict['parentGadget'] = {
            'uuid' : gadget.getDescription().getUuid(),
            'name' : gadget.getDescription().getName(),
            'version' : gadget.getDescription().getVersion(),
        }
        # Description
        ugcDataDict['description'] = {
            'uuid' : ugcUuid,
            'name' : ugcName,
            'ttsName' : ugcTtsName,
            'onDemandIsActivated' : gadget.getDescription().onDemandIsAble(),
        }
        # Parameters
        ugcDataDict['parameters'] = {}
        i = 0
        for parameter in gadget.getParameters():
            if parameter.isVisible():
                defaultValue = parameter.getDefaultValue(language)
                if parameter.getName() == "locutor":
                    defaultValue = ugcContainer.getLocutor().replace("8k", "")
                nodeName = "param_%2d" % i
                i += 1
                ugcDataDict['parameters'][nodeName] = {
                    'name' : parameter.getName(),
                    'value' : defaultValue,
                }
        # Tasks
        ugcDataDict['tasks'] = {}
        for i, task in enumerate(gadget.getTasks()):
            nodeName = "task_%2d" % i
            if task.isActivated():
                isActivated = 'true'
            else:
                isActivated = 'false'
            ugcDataDict['tasks'][nodeName] = {
                'name' : task.getName(),
                'activated' : isActivated,
                'weekMask' : task.getWeekMaskOF(),
                'date' : task.getDate(),
                'hoursBegin' : task.getHoursBegin(),
                'hoursEnd' :  task.getHoursEnd(),
                'delay' :  task.getDelay(),
            }
        # Serve the ugc content
        resourcesManager.addContentToServe(str(ugcDataDict), '/tmp/%s.ugc' % ugcUuid)
        return '/tmp/%s.ugc' % ugcUuid, ugcUuid

    # --------------------------------------------------------------------------
    # Duplicate an User Gadget Configuration.
    # --------------------------------------------------------------------------
    def duplicateUgc(ugc, resourcesManager):
        """Duplicate an User Gadget Configuration.
        @param ugc: UGC to duplicate.
        @param resourcesManager: Server resources manager.
        @return: The url of the served ugc file and its uuid.
        """
        ugcUuid = GadgetGenerator.generateSingleUuid()
        ugcDataDict = copy.deepcopy(ugc.getDictionary())
        ugcName = ugc.getContainer().generateSingleName(
            ugc.getDescription().getName())
        # Description
        ugcDataDict['description']['uuid'] = ugcUuid
        ugcDataDict['description']['name'] = ugcName
        # Creation time
        ugcDataDict['creationTime'] = time.time()
        # Serve the ugc content
        resourcesManager.addContentToServe(str(ugcDataDict), '/tmp/%s.ugc' % ugcUuid)
        return '/tmp/%s.ugc' % ugcUuid, ugcUuid

    # --------------------------------------------------------------------------
    # Update an User Gadget Configuration.
    # --------------------------------------------------------------------------
    def updateUgc(ugc, requestData, resourcesManager):
        """Update an User Gadget Configuration.
        @param ugc: UGC to duplicate.
        @param requestData: Data from the request.
        @param resourcesManager: Server resources manager.
        @return: The url of the served ugc file and its uuid.
        """
        ugcUuid = ugc.getDescription().getUuid()
        parentGadget = ugc.getParentGadget()
        tmpDataDict = copy.deepcopy(GadgetGenerator.requestDataToDict(
            requestData, parentGadget))
        ugcContainer = ugc.getContainer()
        if tmpDataDict['description']['name'] != ugc.getDescription().getName():
            ugcName = ugcContainer.generateSingleName(tmpDataDict['description']['name'])
        else:
            ugcName = tmpDataDict['description']['name']
        tmpDataDict['description']['ttsName'] = ugcName
        ugcTtsName = tmpDataDict['description']['ttsName']
        ugcDataDict = {}
        # Parent Gadget
        ugcDataDict['parentGadget'] = {
            'uuid' : parentGadget.getDescription().getUuid(),
            'name' : parentGadget.getDescription().getName(),
            'version' : parentGadget.getDescription().getVersion(),
        }
        # Creation time
        ugcDataDict['creationTime'] = ugc.getUgcFileCreationTime()
        # Default attitune for alerts introduction
        if tmpDataDict.has_key("alertAttitune"):
            ugcDataDict['alertAttitune'] = tmpDataDict['alertAttitune']
        else:
            ugcDataDict['alertAttitune'] = "----"
        # Description
        onDemandIsActivated = "false"
        if tmpDataDict['description'].has_key('onDemandIsActivated'):
            onDemandIsActivated = tmpDataDict['description']['onDemandIsActivated']
        ugcDataDict['description'] = {
            'uuid' : ugcUuid,
            'name' : ugcName,
            'ttsName' : ugcTtsName,
            'onDemandIsActivated' : onDemandIsActivated,
        }
        # Parameters
        ugcDataDict['parameters'] = tmpDataDict['parameters']
        for key in ugcDataDict['parameters'].keys():
            del ugcDataDict['parameters'][key]['visible']
            ugcDataDict['parameters'][key]['value'] = ugcDataDict['parameters'][key]['defaultValue']
            del ugcDataDict['parameters'][key]['defaultValue']
        # Tasks
        ugcDataDict['tasks'] = tmpDataDict['tasks']
        # Serve the ugc content
        resourcesManager.addContentToServe(str(ugcDataDict), '/tmp/%s.ugc' % ugcUuid)
        return '/tmp/%s.ugc' % ugcUuid, ugcUuid

    generateSingleUuid = staticmethod(generateSingleUuid)
    requestDataToDict = staticmethod(requestDataToDict)
    pluginToGadgetRequestDataToDict = staticmethod(pluginToGadgetRequestDataToDict)
    generateGadget = staticmethod(generateGadget)
    gadgetDictToXml = staticmethod(gadgetDictToXml)
    generatePreviewGadget = staticmethod(generatePreviewGadget)
    duplicateGadget = staticmethod(duplicateGadget)
    generateUgcFromGadget = staticmethod(generateUgcFromGadget)
    duplicateUgc = staticmethod(duplicateUgc)
    updateUgc = staticmethod(updateUgc)
