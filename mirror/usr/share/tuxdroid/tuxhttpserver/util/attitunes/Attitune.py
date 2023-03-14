#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import threading
import copy

from AttituneDescription import AttituneDescription
from AttituneToMacroDecl import attCmdToMacroCmd

# ------------------------------------------------------------------------------
# Attitune class.
# ------------------------------------------------------------------------------
class Attitune(object):
    """Attitune class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, parent, dictionary, attFile, workingPath, observerName):
        """Constructor of the class.
        @param parent: Parent Gadgets container.
        @param dictionary: Gadget structure as dictionary.
        @param attFile: ATT file name of the attitune.
        @param workingPath: Working path of the attitune.
        @param observerName: Observer name.
        """
        self.__parent = parent
        # Save the dictionary
        self.__dictionary = dictionary
        # Save the working path
        self.__workingPath = workingPath
        # Save the att file name
        self.__attFile = attFile
        # Save the container name
        self.__observerName = observerName
        # Create descriptor
        self.__description = AttituneDescription(self,
            dictionary['scene']['header'], self.__workingPath)
        # Get wav files
        self.__wavs = {}
        wavsPath = os.path.join(workingPath, "wavs")
        if os.path.isdir(wavsPath):
            files = os.listdir(wavsPath)
            for file in files:
                if file.lower().find(".wav") != -1:
                    self.__wavs[file] = os.path.join(wavsPath, file)
        # Timeline
        self.__blocksStruct = dictionary['scene']['body']['script']['timeline']
        self.__blocksKeys = self.__blocksStruct.keys()
        self.__blocksKeys.sort()
        # Macro
        self.__macroStruct = []
        self.__buildPreMacro()

    # --------------------------------------------------------------------------
    # Convert the attitunes timeline to macro.
    # --------------------------------------------------------------------------
    def __buildPreMacro(self):
        """Convert the attitunes timeline to macro.
        """
        self.__macroStruct = []
        for block in self.__blocksKeys:
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
    # Get the directory path where this attitune is uncompressed.
    # --------------------------------------------------------------------------
    def getWorkingPath(self):
        """Get the directory path where this attitune is uncompressed.
        @return: A directory path as string.
        """
        return self.__workingPath

    # --------------------------------------------------------------------------
    # Get the ATT file of the gadget.
    # --------------------------------------------------------------------------
    def getAttFile(self):
        """Get the ATT file of the gadget.
        @return: A string.
        """
        return self.__attFile

    # --------------------------------------------------------------------------
    # Get the dictionary of the attitune.
    # --------------------------------------------------------------------------
    def getDictionary(self):
        """Get the dictionary of the attitune.
        @return: A dictionary.
        """
        return self.__dictionary

    # --------------------------------------------------------------------------
    # Get the parent attitunes container.
    # --------------------------------------------------------------------------
    def getContainer(self):
        """Get the parent attitunes container.
        @return: The parent attitunes container.
        """
        return self.__parent

    # --------------------------------------------------------------------------
    # Get the observer name.
    # --------------------------------------------------------------------------
    def getObserverName(self):
        """Get the observer name.
        @return: A string.
        """
        return self.__observerName

    # --------------------------------------------------------------------------
    # Get the attitune description object.
    # --------------------------------------------------------------------------
    def getDescription(self):
        """Get the attitune description object.
        @return: The attitune description object.
        """
        return self.__description

    # --------------------------------------------------------------------------
    # Get a macro from the attitunes.
    # --------------------------------------------------------------------------
    def getMacro(self, begin = 0.0):
        """Get a macro from the attitunes.
        @param begin: The time begin index in seconds.
        @return: The macro as string.
        """
        result = ""
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
