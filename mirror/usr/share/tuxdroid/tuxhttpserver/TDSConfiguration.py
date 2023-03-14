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

from util.logger import *
from util.misc.tuxPaths import *
from util.misc.systemPaths import systemPaths

# ==============================================================================
# Class to retrieve the py file path.
# ==============================================================================
class localFilePath(object):
    """Class to retrieve the local file path.
    """
    def getPath(self):
        """Get the local file path.
        """
        mPath, mFile = os.path.split(__file__)
        return mPath

# ------------------------------------------------------------------------------
# HTTP server configuration
# ------------------------------------------------------------------------------
# Host address for the server sockets
if os.name == 'nt':
    TDS_CONF_HOST_ADDRESS = '127.0.0.1'
else:
    TDS_CONF_HOST_ADDRESS = ''

# HTTP server Port
TDS_HTTP_PORT = systemPaths.getServerPort()
# Use 50msec delay in request (CPU optimisation)
TDS_50MSEC_OPTIMISATION = False
# Use asynchronous requests treatment
TDS_HTTP_ASYNCHRONOUS_REQUESTS = True
# Use asynchronous requests reception
TDS_HTTP_ASYNCHRONOUS_ACCEPT = False
TDS_HTTP_ASYNCHRONOUS_ACCEPT_DELAY = 0.01

# ------------------------------------------------------------------------------
# TCP/IP server configuration
# ------------------------------------------------------------------------------
# Raw data server port
TDS_RAW_DATA_PORT = systemPaths.getServerPort() + 1

# ------------------------------------------------------------------------------
# Loggers configuration
# ------------------------------------------------------------------------------
# Global log level
TDS_CONF_LOG_LEVEL = LOG_LEVEL_INFO
# Global log target
TDS_CONF_LOG_TARGET = LOG_TARGET_FILE
# Activation of the global file for logs
# All log messages will be merged into one file (Single log files are preserved)
TDS_CONF_LOG_GLOBAL = True
# Filename of the global server log
TDS_FILENAME_TUXDROIDSERVER_LOG = "TuxDroidServer"
# Filename of the HTTP server log
TDS_FILENAME_HTTPSERVER_LOG = "TuxHTTPServer"
# Filename of the resources log
TDS_FILENAME_RESOURCES_LOG = "TuxServerResourcesManager"
# Filename of the client manager log
TDS_FILENAME_CLIENTS_LOG = "TuxServerClientsManager"

# ------------------------------------------------------------------------------
# Server paths configuration
# ------------------------------------------------------------------------------
# Path of the application
TDS_APPLICATION_PATH = localFilePath().getPath()
# Path of the resources
TDS_RESOURCES_PATH = os.path.join(TDS_APPLICATION_PATH, 'resources')
# All users base dir for Windows
if os.name == 'nt':
    ALLUSERSBASEDIR = os.path.join(os.environ['ALLUSERSPROFILE'], "Kysoh",
        "Tux Droid")
    if not os.path.isdir(ALLUSERSBASEDIR):
        os.makedirs(ALLUSERSBASEDIR)
# Path of the resources configurations of the httpserver
if os.name == 'nt':
    TDS_RESOURCES_CONF_PATH = os.path.join(ALLUSERSBASEDIR, "configurations", "resources")
else:
    TDS_RESOURCES_CONF_PATH = systemPaths.getResourcesConfPath()
# Path of the user configurations
if os.name == 'nt':
    TDS_USERS_CONF_PATH = os.path.join(ALLUSERSBASEDIR, "configurations", "users_conf")
else:
    TDS_USERS_CONF_PATH = systemPaths.getUserConfPath()
# Path of the default content of the server
if os.name == 'nt':
    TDS_DEFAULT_CONTENT_PATH = os.path.join(ALLUSERSBASEDIR, "resources")
else:
    TDS_DEFAULT_CONTENT_PATH = os.path.join(TUXDROID_BASE_PATH, "resources")
# Path of the server updates
if os.name == 'nt':
    TDS_UPDATES_PATH = os.path.join(TDS_DEFAULT_CONTENT_PATH, "updates")
else:
    TDS_UPDATES_PATH = systemPaths.getUpdateContentPath()

# ------------------------------------------------------------------------------
# Resources configuration
# ------------------------------------------------------------------------------
TDS_ONLY_BASE_RESOURCES = False

# ------------------------------------------------------------------------------
# Misc configurations
# ------------------------------------------------------------------------------
os.environ["TDS_PLUGIN_PLATFORM_ALL"] = "False"
