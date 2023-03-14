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

import threading
import time
import os
import sys

from util.misc import FilesCache
from util.misc import DirectoriesAndFilesTools
from util.misc.tuxPaths import TUXDROID_BASE_PATH, TUXDROID_LANGUAGE
from util.misc.tuxPaths import TUXDROID_DEFAULT_LOCUTOR
from util.eventhandler.TuxEventHandlers import TuxEventHandlers

from TDSAccessManager import *
from TDSClientsManager import *
from TDSHTTPServer import *
from TDSResourcesManager import *
from TDSConfiguration import *
from TDSAutoUpdater import TDSAutoUpdater
from translation.Translation import Translation

# Create looger object
logger = SimpleLogger("SmartServerMain")
logger.setLevel(TDS_CONF_LOG_LEVEL)
logger.setTarget(TDS_CONF_LOG_TARGET)
# Define the events handler.
eventsHandler = TuxEventHandlers()
# Define the files cache manager.
filesCacheManager = FilesCache.CachedFilesContainer("TuxDroidServer")
# Define the access manager.
accessManager = TDSAccessManager()
# Define the clients manager.
clientsManager = TDSClientsManager(accessManager)
# Define the resources manager.
resourcesManager = TDSResourcesManager(accessManager, clientsManager, globals())
# Define the HTTP server.
httpServer = TDSHTTPServer(resourcesManager)
# Exit the program if the server can't be created (Typically when another server
# is bind to the same TCP/IP port)
if not httpServer.getCreated():
    sys.exit(1)
# Define a global variable with the server module version.
if os.name == 'nt':
    serverVersion = "%s-WINDOWS" % __version__
else:
    serverVersion = "%s-LINUX" % __version__
# Create the base path of the configurations if not exists
DirectoriesAndFilesTools.MKDirs(TDS_RESOURCES_CONF_PATH)
# Define TTS fixer object.
ttsFixer = Translation("tts_fixes")

def initializeServer():
    """Initialize the server.
    """
    # Check for updates
    logger.logInfo("Create auto-updater")
    autoUpdater = TDSAutoUpdater()
    logger.logInfo("Start auto-updater")
    autoUpdater.start()
    # Load and start the resources manager
    logger.logInfo("Load resources manager")
    resourcesManager.load(TDS_RESOURCES_PATH)
    logger.logInfo("Serve additional files")
    resourcesManager.addDirectoryToServe("/data/web_interface/server_menu/xsl/")
    resourcesManager.addFileToServe(os.path.join(TDS_APPLICATION_PATH,
        "data", "favicon", "favicon.ico"), "/favicon.ico")
    # Load wiky scripts
    resourcesManager.addDirectoryToServe("/data/web_interface/common/wiky/")
    # Commons
    resourcesManager.addDirectoryToServe("/data/web_interface/common/img/")
    # Devel web interface
    resourcesManager.addDirectoryToServe("/data/web_interface/devel/xsl/")
    resourcesManager.addDirectoryToServe("/data/web_interface/devel/css/")
    resourcesManager.addDirectoryToServe("/data/web_interface/devel/img/")
    resourcesManager.addDirectoryToServe("/data/web_interface/devel/js/")
    # User 01 web interface
    resourcesManager.addDirectoryToServe("/data/web_interface/user_01/xsl/")
    resourcesManager.addDirectoryToServe("/data/web_interface/user_01/css/")
    resourcesManager.addDirectoryToServe("/data/web_interface/user_01/img/")
    resourcesManager.addDirectoryToServe("/data/web_interface/user_01/js/")
    logger.logInfo("Start resources manager")
    resourcesManager.start()
    # Start the clients manager
    logger.logInfo("Start clients manager")
    clientsManager.start()

def finalizeServer():
    """Finalize the server.
    """
    # Stop the clients manager
    logger.logInfo("Stop clients manager")
    clientsManager.stop()
    # Stop the resources manager
    logger.logInfo("Stop resources manager")
    resourcesManager.stop()
    # Destroy the files cache manager
    logger.logInfo("Destroy files cache manager")
    filesCacheManager.destroy()
    # Destroy the events handler
    logger.logInfo("Destroy events handler")
    eventsHandler.destroy()
