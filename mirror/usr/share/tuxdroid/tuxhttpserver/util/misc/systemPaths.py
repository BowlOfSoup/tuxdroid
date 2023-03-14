# -*- coding: latin1 -*-

#    Copyright (C) 2009 Kysoh SA (http://www.kysoh.com)
#    Paul Rathgeb ( paul dot rathgeb at kysoh dot com )
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

class systemPaths(object):


    def getServerPort():
        """Get the server port
        """
        if os.name == "nt":
            return 270
        else:
            if os.geteuid() == 0:
                return 270
            else:
                return 54321

    def getLogPath():
        """Get the logs path
        """
        if os.name == "nt":
            #Default Path
            print "FIXME: Add the log path for Windows"
            return "None"
        else:
            if os.geteuid() == 0:
                #root
                return "/var/log/tuxdroid/"
            else:
                # Retrieve the HOME directory
                h = os.getenv("HOME")
                path = os.path.join(h, ".tuxdroid", "logs")
                if not os.path.isdir(path):
                    os.makedirs(path, mode=0755)
                return path

    def getPidPath():
        """Get the PID file Path
        """
        if os.name == "nt":
            print "FIXME: Add the PID file path for Windows"
            return "None"
        else:
            if os.geteuid() == 0:
                return "/var/run/"
            else:
                # Retrieve the HOME directory
                h = os.getenv("HOME")
                path = os.path.join(h, ".tuxdroid", "run")
                if not os.path.isdir(path):
                    os.makedirs(path, mode=0755)
                return path

    def getResourcesConfPath():
        """Get the resource configuration path
        """
        if os.name == "nt":
            print "FIXME: Add the resource configuration PATH for Windows"
            return "None"
        else:
            if os.geteuid() == 0:
                return os.path.join("/etc/tuxdroid", "resources_conf")
            else:
                h = os.getenv("HOME")
                path = os.path.join(h, ".tuxdroid", "resources_conf")
                if not os.path.isdir(path):
                    os.makedirs(path, mode=0755)
                return path
    
    def getUserConfPath():
        """Get the user configuration path
        """
        if os.name == "nt":
            print "FIXME: Add the user configuration PATH for Windows"
            return "None"
        else:
            if os.geteuid() == 0:
                return os.path.join("/etc/tuxdroid", "users_conf")
            else:
                h = os.getenv("HOME")
                path = os.path.join(h, ".tuxdroid", "users_conf")
                if not os.path.isdir(path):
                    os.makedirs(path, mode=0755)
                return path
    
    def getUpdateContentPath():
        """Get the user configuration path
        """
        if os.name == "nt":
            print "FIXME: Add the user configuration PATH for Windows"
            return "None"
        else:
            if os.geteuid() == 0:
                return os.path.join("/usr/share/tuxdroid/resources", "updates")
            else:
                h = os.getenv("HOME")
                path = os.path.join(h, ".tuxdroid", "updates")
                if not os.path.isdir(path):
                    os.makedirs(path, mode=0755)
                return path

    def isUser():
        if os.name == "nt":
            return True
        else:
            if os.geteuid() == 0:
                return False
            else:
                return True
    
    getServerPort = staticmethod(getServerPort)
    getLogPath = staticmethod(getLogPath)
    getPidPath = staticmethod(getPidPath)
    getResourcesConfPath = staticmethod(getResourcesConfPath)
    getUserConfPath = staticmethod(getUserConfPath)
    getUpdateContentPath = staticmethod(getUpdateContentPath)
    isUser = staticmethod(isUser)
