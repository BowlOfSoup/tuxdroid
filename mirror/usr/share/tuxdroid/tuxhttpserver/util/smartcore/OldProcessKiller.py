#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import sys

# ------------------------------------------------------------------------------
# Create a process list as pid, name, command line. Unix.
# ------------------------------------------------------------------------------
def __getProcessIdNameCmdLineListUnix():
    """Create a process list as pid, name, command line. Unix.
    """
    def getPidList():
        pidList = []
        for pidDir in os.listdir("/proc/"):
            try:
                pid = int(pidDir)
            except:
                continue
            pidList.append(pid)
        return pidList

    def getProcessCmdLine(pid):
        fileName = "/proc/%d/cmdline" % pid
        if not os.path.isfile(fileName):
            return ""
        else:
            try:
                f = open(fileName, "r")
                result = f.read().replace("\x00", " ")
                f.close()
            except:
                return ""
            return result

    def getProcessName(pid):
        fileName = "/proc/%d/status" % pid
        if not os.path.isfile(fileName):
            return ""
        else:
            try:
                f = open(fileName, "r")
                result = f.readline()[6:-1]
                f.close()
            except:
                return ""
            return result

    result = []
    pidList = getPidList()
    for pid in pidList:
        e = [pid, getProcessName(pid), getProcessCmdLine(pid)]
        result.append(e)
    return result

# ------------------------------------------------------------------------------
# Kill all process alive from a previous instance of smart-core. Window.
# ------------------------------------------------------------------------------
def __killOldSmartCoreChildrenWin32():
    """Kill all process alive from a previous instance of smart-core. Window.
    """
    import win32api
    from win32com.client import GetObject
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    pidToKill = []
    for process in processes:
        name = process.Properties_('Name').Value
        cmdLine = process.Properties_('CommandLine').Value
        if name == "python.exe":
            if cmdLine.find('executables') != -1:
                pidToKill.append(process.Properties_('ProcessId').Value)
                continue
        if cmdLine != None:
            if cmdLine.lower().find('workforplugins') != -1:
                pidToKill.append(process.Properties_('ProcessId').Value)
                continue
            if (cmdLine.lower().find('smart-server') != -1) and \
                (cmdLine.lower().find('util') != -1):
                pidToKill.append(process.Properties_('ProcessId').Value)
                continue
    for pid in pidToKill:
        try:
            handle = win32api.OpenProcess(1, False, pid)
            win32api.TerminateProcess(handle, -1)
            win32api.CloseHandle(handle)
        except:
            pass

# ------------------------------------------------------------------------------
# Kill previous smart-server. Window.
# ------------------------------------------------------------------------------
def __killPreviousSmartServerWin32():
    """Kill previous smart-server. Window.
    """
    import win32api
    from win32com.client import GetObject
    WMI = GetObject('winmgmts:')
    processes = WMI.InstancesOf('Win32_Process')
    pidToKill = []
    for process in processes:
        name = process.Properties_('Name').Value
        cmdLine = process.Properties_('CommandLine').Value
        pid = process.Properties_('ProcessId').Value
        if name.lower() == "pythonfortuxdroid.exe":
            if cmdLine.find("tuxhttpserver") != -1:
                if pid != os.getpid():
                    pidToKill.append(pid)
    for pid in pidToKill:
        try:
            handle = win32api.OpenProcess(1, False, pid)
            win32api.TerminateProcess(handle, -1)
            win32api.CloseHandle(handle)
        except:
            pass

# ------------------------------------------------------------------------------
# Kill all process alive from a previous instance of smart-core. Unix.
# ------------------------------------------------------------------------------
def __killOldSmartCoreChildrenUnix():
    """Kill all process alive from a previous instance of smart-core. Unix.
    """
    processInfosList = __getProcessIdNameCmdLineListUnix()
    pidToKill = []
    for e in processInfosList:
        pid = e[0]
        name = e[1]
        cmdline = e[2]
        if name.lower().find("python") != -1:
            if cmdline.lower().find("executables") != -1:
                pidToKill.append(pid)
                continue
        if cmdline.lower().find("workforplugins") != -1:
            pidToKill.append(pid)
            continue
        if (cmdline.lower().find("tuxdroid") != -1) and \
            (cmdline.lower().find("util") != -1):
            pidToKill.append(pid)
            continue
    for pid in pidToKill:
        os.system("kill -9 " + str(pid))

# ------------------------------------------------------------------------------
# Kill previous smart-server. Unix.
# ------------------------------------------------------------------------------
def __killPreviousSmartServerUnix():
    """Kill previous smart-server. Unix.
    """
    processInfosList = __getProcessIdNameCmdLineListUnix()
    pidToKill = []
    for e in processInfosList:
        pid = e[0]
        name = e[1]
        cmdline = e[2]
        if name.lower().find("python") != -1:
            if cmdline.lower().find("tuxhttpserver") != -1:
                if cmdline.lower().find("start") != -1:
                    if pid != os.getpid():
                        pidToKill.append(pid)
    for pid in pidToKill:
        os.system("kill -3 -15 -9 " + str(pid))

# ------------------------------------------------------------------------------
# Kill all process alive from a previous instance of smart-core.
# ------------------------------------------------------------------------------
def killOldSmartCoreChildren():
    """Kill all process alive from a previous instance of smart-core.
    """
    if os.name == "nt":
        __killOldSmartCoreChildrenWin32()
    else:
        __killOldSmartCoreChildrenUnix()

# ------------------------------------------------------------------------------
# Kill previous smart-server.
# ------------------------------------------------------------------------------
def killPreviousSmartServer():
    """Kill previous smart-server.
    """
    if os.name == "nt":
        __killPreviousSmartServerWin32()
    else:
        __killPreviousSmartServerUnix()
