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
#    
#    2020 tuxdroid.tounepi.com

import sys
import os
import getopt
import time
import tarfile
import shutil

from util.smartcore.OldProcessKiller import killOldSmartCoreChildren
from util.smartcore.OldProcessKiller import killPreviousSmartServer
from util.system.TaskBar import refreshTaskBar
from util.misc.URLTools import URLTestRequestGet
from TDSConfiguration import *
from util.logger import *

PART_NAMES = [
    'smart_content',
    'smart_api',
    'smart_server',
]

logger = None

updateUserPath = None

def initLogger():
    global logger
    logger = SimpleLogger("SmartServerMain")
    logger.setLevel(TDS_CONF_LOG_LEVEL)
    logger.setTarget(TDS_CONF_LOG_TARGET)
    logger.resetGlobalLogFile(TDS_CONF_LOG_GLOBAL)
    logger.resetLog()
    logger.logInfo("-----------------------------------------------")
    logger.logInfo("SmartServerMain%s" % __version__)
    logger.logInfo("Licence : %s" % __licence__)
    logger.logInfo("-----------------------------------------------")

def checkServerRun():
    return URLTestRequestGet("127.0.0.1", TDS_HTTP_PORT, "/", 200, 5.0)

def killServer():
    if os.name != 'nt':
        # Stop the server regularly
        URLTestRequestGet("127.0.0.1", TDS_HTTP_PORT, "/server/stop?", 200, 0.5)
        URLTestRequestGet("127.0.0.1", TDS_HTTP_PORT, "/server/stop?", 200, 0.5)
        # Wait 5 secs max that the previous server has been stopped
        for i in range(10):
            if not checkServerRun():
                break
            time.sleep(0.5)
    # Kill smart-core tasks if still alive
    killOldSmartCoreChildren()
    killPreviousSmartServer()
    # Refresh taskbar icons
    refreshTaskBar()

def killServerAndWait():
    logger.logInfo("Kill server")
    killServer()
    logger.logInfo("Server killed")
    time.sleep(0.5)

def runServer():
    logger.logInfo("Import initializeServer")
    from TuxDroidServer import initializeServer
    logger.logInfo("Import httpServer")
    from TuxDroidServer import httpServer
    logger.logInfo("Import finalizeServer")
    from TuxDroidServer import finalizeServer
    logger.logInfo("Initialize server")
    initializeServer()
    logger.logInfo("Start server")
    httpServer.start()
    logger.logInfo("Server stopped")
    logger.logInfo("Finalize server")
    finalizeServer()
    logger.logInfo("Server finalized")
    
def update():
    if os.name != 'nt':
        print("-----------------------------------------------")
        print("Tuxbox Update")
        print("-----------------------------------------------")
        print(" ")
        
        #test sudo
        try:
            os.mkdir("/usr/share/tuxdroid/test/", 0755 );
        except:
            print("Your are not allowed.")
            print("please type : sudo tuxhttpserver -u")
            exit()
        shutil.rmtree("/usr/share/tuxdroid/test")
        
        print("Stop the server")
        killServer()
        print(" ")
        
        #path list /home
        homePath =  os.listdir('/home')
        homePathList = list()
        for path in homePath:
            pathDir = os.path.join("/home",path)
            if os.path.isdir(pathDir):
                homePathList.append(path)
                
        if updateUserPath == None:
            if not len(homePathList) == 1:
                print "Multiple users"
                print "Please, specify your login :"
                for path in homePathList:
                    print "sudo tuxhttpserver -u -d ", path
                exit()
        else :
            upPath = os.path.join("/home",updateUserPath)
            userPathArg = updateUserPath
                
        if len(homePathList) == 1:
            upPath = os.path.join("/home",homePathList[0])
            userPathArg = homePathList[0]
            
        if not os.path.isdir(upPath):
            print "Error, wrong path."
            exit()
        
        #install
        updateStateNum = 0
        for partName in PART_NAMES:
            print(partName)
            confUrl = os.path.join(upPath,".tuxdroid","updates",partName+'.conf')
            if os.path.isfile(confUrl):
                f = open(confUrl, "r")
                try:
                    confDict = eval(f.read())
                except:
                    f.close()
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
                installerFile = os.path.join(upPath,".tuxdroid","updates",installerName)
                print(currentVersion)
                if os.path.isfile(installerFile):
                    print "Open..."
                    tmpPath = os.path.join(upPath,".tuxdroid","updates")
                    try:
                        tar = tarfile.open(installerFile, 'r:gz')
                    except:
                        print "Error install file : ", installerName
                        tar.close()
                        exit()
                    try:
                        tar.extractall(tmpPath)
                    except :
                        print "Error extract tar file : ", installerName
                        tar.close()
                        exit()
                    tar.close()
                    nameTar = partName + "_" + currentVersion
                    tmpPath = os.path.join(upPath,".tuxdroid","updates",nameTar)                    
                    tmpSh = "sh " + tmpPath + "/update.sh" + " " + currentVersion + " " + userPathArg
                    stream = os.popen(tmpSh)
                    output = stream.read()
                    try:
                        output
                    except:
                        print "Error running sh."
                        exit()
                    print(output)
                    try:
                        os.remove(installerFile)
                    except:
                        print "Error remove : ", installerFile
                        exit()
                    try:
                        shutil.rmtree(tmpPath)
                    except:
                        print "Error remove : ", tmpPath
                        exit()
                    tmpPath = os.path.join(upPath,".tuxdroid","updates",partName)
                    cfFile = tmpPath + ".conf"
                    try:
                        os.remove(cfFile)
                    except:
                        print "Error remove : ", cfFile
                        exit()
                    tmpPath = os.path.join(upPath,".tuxdroid","updates/")
                    cverFile = tmpPath + partName + ".cver"
                    try:
                        f = open(cverFile, "w")
                    except:
                        print "Error write : ", cverFile
                        exit()
                    f.write(currentVersion)
                    f.close()
                    print("Done")
                        
            else:
                print("Nothing to do.")
            print(" ")

        print 'Done'
        print "Quit sudo and run : tuxhttpserver --start"
    else:
        print("Linux command only.")

def usage():
    print '-'*80
    print 'Tux HTTP Server v. : %s'%__version__
    print 'Release date : %s'%__date__
    print 'Author       : %s'%__author__
    print 'Released under %s license'%__licence__
    print ''
    print '  Usage :'
    print '  python tuxhttpserver.py [slrh]'
    print '  -s , --stop    : Stop the server'
    print '  -l , --start   : Start the server'
    print '  -r , --restart : Restart the server'
    print '  -u , --update  : Update (Run : sudo tuxhttpserver -u, only for linux)'
    print '  -h , --help    : Display this help'
    print "  --no-daemon    : Don't daemonize the server"
    print '                   (only for Linux)'
    print ''
    print '-'*80
    print ''

# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    def start():
        if os.name == 'nt': # Windows
            runServer()
        else: # Linux
            if __daemon:
                from util.daemonizer import Daemonizer
                from util.misc.systemPaths import systemPaths
                tuxDroidDaemon = Daemonizer('tuxhttpserver', systemPaths.getLogPath(),
                    runServer, True)
                tuxDroidDaemon.start()
            else:
                runServer()

    __start = False
    __stop = False
    __restart = False
    __update = False
    __daemon = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], "slrudh", \
                ["stop", "start", "restart","update", "help", "no-daemon"])
    except getopt.error, msg:
        print msg
        usage()
        sys.exit(2)

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-s", "--stop"):
            __stop = True
        elif o in ("-l", "--start"):
            __start = True
        elif o in ("-r", "--restart"):
            __start = True
            __restart = True
        elif o in ("-u", "--update"):
            __update = True
        elif o in ("-d"):
            if args:
                updateUserPath = args[0]
        elif o in ("--no-daemon"):
            __daemon = False

    if __start and __stop:
        print "--start or --restart and --stop are exclusive options"
        print "Couldn't determine what should be done.. so, exiting."
        sys.exit(2)

    if __stop:
        killServer()
    elif __restart:
        initLogger()
        killServerAndWait()
        start()
    elif __update:
        update()
    else:
        if checkServerRun():
            print "Server is already started"
            print "Uses --restart if you want to restart the server.. so, exiting."
        else:
            initLogger()
            start()

