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

import os
import threading
import subprocess
import time

from TDSConfiguration import *

from util.misc import DirectoriesAndFilesTools
from util.misc import URLTools
from util.logger import *

#DIST_STATE = "beta-test"
DIST_STATE = "stable"

PART_CONF_SRC_URL = 0
PART_CONF_DEST = 1
PART_CVER_FILE = 2
PART_DEFAULT_VER = 3

UPDATES_PARTS = {
    'smart_server' : [
        'http://tuxdroid.tounepi.com/ftp/ssv3/smart_core/smart_server/%s.conf' % DIST_STATE,
        'smart_server.conf',
        'smart_server.cver',
        __version__,
    ],
    'smart_api' : [
        'http://tuxdroid.tounepi.com/ftp/ssv3/smart_core/smart_api/%s.conf' % DIST_STATE,
        'smart_api.conf',
        'smart_api.cver',
        '',
    ],
    'smart_content' : [
        'http://tuxdroid.tounepi.com/ftp/ssv3/smart_core/smart_content/%s.conf' % DIST_STATE,
        'smart_content.conf',
        'smart_content.cver',
        '',
    ],
}

PART_NAMES = [
    'smart_content',
    'smart_api',
    'smart_server',
]

# ------------------------------------------------------------------------------
# Tux Droid Server : Auto updater.
# ------------------------------------------------------------------------------
class TDSAutoUpdater(object):
    """Tux Droid Server : Auto updater.
    """

    # --------------------------------------------------------------------------
    # Constructor.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor.
        """
        if not os.path.isdir(TDS_UPDATES_PATH):
            DirectoriesAndFilesTools.MKDirs(TDS_UPDATES_PATH)
        self.__logger = SimpleLogger("auto_updater")
        self.__logger.setTarget(TDS_CONF_LOG_TARGET)
        self.__logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.__logger.resetLog()
        self.__logger.logInfo("-----------------------------------------------")
        self.__logger.logInfo("TDSAutoUpdater%s" % __version__)
        self.__logger.logInfo("Author : %s" % __author__)
        self.__logger.logInfo("Licence : %s" % __licence__)
        self.__logger.logInfo("-----------------------------------------------")
        # Write default CVER files
        self.__writeDefaultCVerFiles()

    # --------------------------------------------------------------------------
    # Write default cver files if not exists.
    # --------------------------------------------------------------------------
    def __writeDefaultCVerFiles(self):
        """Write default cver files if not exists.
        """
        for partName in PART_NAMES:
            defaultVersion = UPDATES_PARTS[partName][PART_DEFAULT_VER]
            cverFile = os.path.join(TDS_UPDATES_PATH,
                UPDATES_PARTS[partName][PART_CVER_FILE])
            if not os.path.isfile(cverFile):
                self.__writeCVerFile(partName, defaultVersion)

    # --------------------------------------------------------------------------
    # Write a cver file.
    # --------------------------------------------------------------------------
    def __writeCVerFile(self, partName, currentVersion):
        """Write a cver file.
        @param partName: Software part name.
        @param currentVersion: Current version of the software part.
        """
        cverFile = os.path.join(TDS_UPDATES_PATH,
            UPDATES_PARTS[partName][PART_CVER_FILE])
        if currentVersion != "":
            f = open(cverFile, "w")
            f.write(currentVersion)
            f.close()

    # --------------------------------------------------------------------------
    # Get the current version of a software part.
    # --------------------------------------------------------------------------
    def __getCurrentPartVersion(self, partName):
        """Get the current version of a software part.
        @param partName: Software part name.
        @return: A string.
        """
        cverFile = os.path.join(TDS_UPDATES_PATH,
            UPDATES_PARTS[partName][PART_CVER_FILE])
        if os.path.isfile(cverFile):
            f = open(cverFile, "r")
            result = f.read()
            f.close()
            return result
        else:
            return ""

    # --------------------------------------------------------------------------
    # Start the auto-updater.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the auto-updater.
        """
        self.__checkStartInstallers()
        t = threading.Thread(target = self.__updateFromTheNet)
        t.start()

    # --------------------------------------------------------------------------
    # Check / Start the installers.
    # --------------------------------------------------------------------------
    def __checkStartInstallers(self):
        """Check / Start the installers.
        """
        for partName in PART_NAMES:
            destConf = os.path.join(TDS_UPDATES_PATH,
                UPDATES_PARTS[partName][PART_CONF_DEST])
            cverFile = os.path.join(TDS_UPDATES_PATH,
                UPDATES_PARTS[partName][PART_CVER_FILE])
            if os.path.isfile(destConf):
                f = open(destConf, "r")
                try:
                    confDict = eval(f.read())
                except:
                    self.__logger.logError("Conf file is corrupted [%s]" % UPDATES_PARTS[partName][PART_CONF_DEST])
                    f.close()
                    DirectoriesAndFilesTools.RMFile(destConf)
                    DirectoriesAndFilesTools.RMFile(cverFile)
                    continue
                f.close()
                archName = "win32"
                if os.name == "nt":
                    if not confDict.has_key('win32'):
                        continue
                    archName = "win32"
                else:
                    if not confDict.has_key('unix'):
                        continue
                    archName = "unix"
                installerName = confDict[archName]["fileName"]
                currentVersion = confDict[archName]["version"]
                if self.__getCurrentPartVersion(partName) == currentVersion:
                    continue
                installerFile = os.path.join(TDS_UPDATES_PATH, installerName)
                if os.name == "nt":
                    cmd = [
                        installerFile,
                        "/S",
                        "/START=true",
                    ]
                    self.__logger.logInfo("Installation started [%s] (%s)" % (installerName, currentVersion))
                    process = subprocess.Popen(cmd)
                    process.wait()
                    self.__writeCVerFile(partName, currentVersion)
                    self.__logger.logInfo("Installation finished")
                else:
                    pass

    # --------------------------------------------------------------------------
    # Check for updates.
    # --------------------------------------------------------------------------
    def __updateFromTheNet(self):
        """Check for updates.
        """
        # Wait for connection to internet enabled
        while not URLTools.URLCheck("http://ftp.kysoh.com", 2.0):
            time.sleep(1.0)
        self.__logger.logInfo("Internet connection is detected")
        # Download conf files
        for partName in PART_NAMES:
            confUrl = UPDATES_PARTS[partName][PART_CONF_SRC_URL]
            confStr = URLTools.URLDownloadToString(confUrl)
            if confStr != None:
                try:
                    confDict = eval(confStr)
                except:
                    self.__logger.logError("Conf file is corrupted [%s]" % confUrl)
                    continue
                archName = "win32"
                if os.name == "nt":
                    if not confDict.has_key('win32'):
                        self.__logger.logWarning("Conf file have no information for your system [%s]" % confUrl)
                        continue
                    archName = "win32"
                else:
                    if not confDict.has_key('unix'):
                        self.__logger.logWarning("Conf file have no information for your system [%s]" % confUrl)
                        continue
                    archName = "unix"
                currentVersion = self.__getCurrentPartVersion(partName)
                stateVersion = confDict[archName]["version"]
                self.__logger.logInfo("Versions for [%s] :" % partName)
                self.__logger.logInfo("\tCurrent version : %s" % currentVersion)
                self.__logger.logInfo("\tServer version  : %s" % stateVersion)
                if stateVersion != currentVersion:
                    self.__logger.logInfo("\tNew version available")
                    installerUrl = confDict[archName]["url"]
                    installerDest = os.path.join(TDS_UPDATES_PATH,
                        confDict[archName]["fileName"])
                    self.__logger.logInfo("\tStart to download the new version installer")
                    self.__logger.logInfo("\tFrom [%s]" % installerUrl)
                    self.__logger.logInfo("\tTo [%s]" % installerDest)
                    if URLTools.URLDownloadToFile(installerUrl, installerDest, 9999.0):
                        self.__logger.logInfo("\tNew installer is successfully downloaded")
                        destConf = os.path.join(TDS_UPDATES_PATH,
                            UPDATES_PARTS[partName][PART_CONF_DEST])
                        f = open(destConf, "w")
                        f.write(str(confDict))
                        f.close()
                    else:
                        self.__logger.logInfo("\tCan't download the installer")
                else:
                    self.__logger.logInfo("\tYour version is up to date")
