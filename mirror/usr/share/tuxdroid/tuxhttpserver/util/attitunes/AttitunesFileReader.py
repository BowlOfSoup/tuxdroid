# -*- coding: utf-8 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import zipfile
import copy
from util.misc.FilesCache import CachedFilesContainer
from util.misc.XMLSerializer import fromXML
from AttituneToMacroDecl import attCmdToMacroCmd

# ==============================================================================
# Public class
# ==============================================================================

# ------------------------------------------------------------------------------
# Class to read and parse attitunes files.
# ------------------------------------------------------------------------------
class AttitunesFileReader(object):
    """Class to read and parse attitunes files.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self, attPath):
        """Constructor of attitunes file reader object.
        @param attPath: Attitune file path.
        """
        self.__isValid = True
        self.__fCacheContainer = CachedFilesContainer("attFileReader")

        fc = self.__fCacheContainer.createFileCache(attPath)
        if fc == None:
            self.__isValid = False
            return

        self.__attPath = fc.getOutputFilePath()
        self.__tmpAttPath = self.__fCacheContainer.getCacheDir()
        self.__tmpPath = ""
        self.__attRoot = ""
        self.__xmlPath = ""
        self.__wavsPath = ""

        self.__wavs = []
        self.__timeline = {}
        self.__blocksStruct = {}
        self.__blocksKeys = []
        self.__macroStruct = []

        if not self.__uncompress():
            self.__isValid = False
            return

        if not self.__getStructure():
            self.__isValid = False
            return

        self.__preMacro()

    # --------------------------------------------------------------------------
    # Return the validity of the attitunes read.
    # --------------------------------------------------------------------------
    def getValid(self):
        """Return the validity of the attitunes read.
        @return: True or False.
        """
        return self.__isValid

    # --------------------------------------------------------------------------
    # Uncompress the attitunes file.
    # --------------------------------------------------------------------------
    def __uncompress(self):
        """Uncompress the attitunes file.
        """
        try:
            if not os.path.isfile(self.__attPath):
                return False
        except:
            return False

        if self.__attPath.lower().find('.att') == -1:
            return False

        (fPath, fName) = os.path.split(self.__attPath)
        fDir = fName.lower().replace('.att', '')
        dPath = self.__tmpAttPath
        self.__tmpPath = os.path.join(dPath, fDir)

        try:
            zf = zipfile.ZipFile(self.__attPath, 'r')
        except:
            return False

        for name in zf.namelist():
            filePath = os.path.join(self.__tmpPath, name)
            filePath = filePath.replace("\\", "/")
            if not os.path.exists(os.path.dirname(filePath)):
                os.makedirs(os.path.dirname(filePath), 511)
            f = open(filePath, 'wb')
            f.write(zf.read(name))
            f.close()
        zf.close()

        try:
            fs = os.listdir(self.__tmpPath)
        except:
            return False

        for f in fs:
            if f not in [".", ".."]:
                self.__attRoot = os.path.join(self.__tmpPath, f)

                xmlPath = os.path.join(self.__attRoot, "scene.xml")
                if os.path.isfile(xmlPath):
                    self.__xmlPath = xmlPath

                wavsPath = os.path.join(self.__attRoot, "wavs")
                if os.path.isdir(wavsPath):
                    self.__wavsPath = wavsPath
                break
        return True

    # --------------------------------------------------------------------------
    # Get the structure of the attitunes.
    # --------------------------------------------------------------------------
    def __getStructure(self):
        """Get the structure of the attitunes.
        """
        self.__wavs = {}
        self.__timeline = {}
        self.__blocksStruct = {}
        self.__blocksKeys = []

        if self.__wavsPath != "":
            wd = os.listdir(self.__wavsPath)
            for wav in wd:
                if wav.lower().find(".wav") != -1:
                    self.__wavs[wav] = os.path.join(self.__wavsPath, wav)

        ret = False

        if self.__xmlPath != "":
            self.__timeline = fromXML(self.__xmlPath)

        if self.__timeline == None:
            return False

        self.__blocksStruct = \
            self.__timeline['scene']['body']['script']['timeline']
        self.__blocksKeys = self.__blocksStruct.keys()
        self.__blocksKeys.sort()

        return True

    # --------------------------------------------------------------------------
    # Convert the attitunes timeline to macro.
    # --------------------------------------------------------------------------
    def __preMacro(self):
        """Convert the attitunes timeline to macro.
        """
        self.__macroStruct = []

        for block in  self.__blocksKeys:
            blockStruct = self.__blocksStruct[block]
            mcs = attCmdToMacroCmd(blockStruct)
            for mc in mcs:
                cmdStruct = {
                    'delay' : blockStruct['start_time'],
                    'cmd' : mc,
                }

                if blockStruct['cmd'] == 'wav_play':
                    cmdStruct['delay'] = cmdStruct['delay'] - 0.3
                    if self.__wavs.has_key(blockStruct['wav_name']):
                        cmdStruct['wav_path'] = \
                            self.__wavs[blockStruct['wav_name']]
                elif blockStruct['cmd'] == 'tts_play':
                    cmdStruct['delay'] = cmdStruct['delay'] - 0.3

                self.__macroStruct.append(cmdStruct)

    # --------------------------------------------------------------------------
    # Get a macro from the attitunes.
    # --------------------------------------------------------------------------
    def toMacro(self, begin = 0.0):
        """Get a macro from the attitunes.
        @param begin: The time begin index in seconds.
        @return: The macro in a string.
        """
        result = ""
        if not self.__isValid:
            return result

        macroLst = []

        for cmd in self.__macroStruct:
            newCmd = copy.deepcopy(cmd)
            newCmd['delay'] += 0.5
            if newCmd['delay'] >= begin:
                if newCmd.has_key('wav_path'):
                    cmdStr = "OSL_CMD:WAV:PLAY:0.0,0.0,%s" % newCmd['wav_path']
                    newCmd['cmd'] = cmdStr
                newCmd['delay'] -= begin
                macroLst.append(newCmd)
            else:
                if newCmd.has_key('wav_path'):
                    idxb = begin - newCmd['delay']
                    if idxb < os.path.getsize(cmd['wav_path']):
                        cmdStr = "OSL_CMD:WAV:PLAY:%f,0.0,%s" % (idxb,
                            newCmd['wav_path'])
                        newCmd['cmd'] = cmdStr
                        newCmd['delay'] -= begin
                        macroLst.append(newCmd)

        for cmd in macroLst:
            tmpStr = "%f:%s\n" % (cmd['delay'], cmd['cmd'])
            result = result + tmpStr

        return result

    # --------------------------------------------------------------------------
    # Destroy the attitunes reader object.
    # --------------------------------------------------------------------------
    def destroy(self):
        """Destroy the attitunes reader object.
        """
        self.__wavs = []
        self.__timeline = {}
        self.__blocksStruct = {}
        self.__blocksKeys = []
        self.__macroStruct = []
        self.__fCacheContainer.destroy()
