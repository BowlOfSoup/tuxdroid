#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import subprocess
import threading
import time

from util.system.Device import Device
from Commands import *

# ------------------------------------------------------------------------------
# Mplayer stdin/stdout bridge.
# ------------------------------------------------------------------------------
class Mplayer(object):
    """Mplayer stdin/stdout bridge.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        if os.name == 'nt':
            mPath, mFile = os.path.split(__file__)
            self.__appMplayer = os.path.join(mPath, 'mplayer.exe')
        else:
            self.__appMplayer = 'mplayer'
        self.__runMutex = threading.Lock()
        self.__run = False
        self.__process = None
        self.__device = Device.getTuxDroidSoundDevice()
        self.__media = None
        self.__isAsync = False
        self.onStreamLoosedCallback = None

    # --------------------------------------------------------------------------
    # Start mplayer.
    # --------------------------------------------------------------------------
    def start(self, media, useAsync = False):
        """Start mplayer.
        @param media: Media to play.
        @param useAsync: Run async or not.
        """
        self.__media = media
        self.__isAsync = useAsync
        if not useAsync:
            self.__mainLoop(media)
        else:
            t = threading.Thread(target = self.__mainLoop, args = (media,))
            t.start()

    # --------------------------------------------------------------------------
    # Stop mplayer.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop mplayer.
        """
        if not self.__getRun():
            return
        self.__runMutex.acquire()
        if self.__process != None:
            if os.name == 'nt':
                import win32api
                try:
                    win32api.TerminateProcess(int(self.__process._handle), -1)
                except:
                    pass
            else:
                os.system("kill -3 -15 -9 " + str(self.__process.pid))
        self.__run = False
        self.__process = None
        time.sleep(0.25)
        self.__runMutex.release()

    # --------------------------------------------------------------------------
    # Restart mplayer.
    # --------------------------------------------------------------------------
    def restart(self):
        """Restart mplayer.
        """
        self.stop()
        if self.__media == None:
            return
        self.start(self.__media, self.__isAsync)

    # --------------------------------------------------------------------------
    # Get the pid of mplayer.
    # --------------------------------------------------------------------------
    def getPid(self):
        """Get the pid of mplayer.
        @return: An integer.
        """
        if self.__process != None:
            if os.name == 'nt':
                return int(self.__process.pid)
            else:
                return self.__process.pid
        else:
            return None

    # --------------------------------------------------------------------------
    # Get if mplayer is started or not.
    # --------------------------------------------------------------------------
    def __getRun(self):
        """Get if mplayer is started or not.
        @return: True or False.
        """
        self.__runMutex.acquire()
        result = self.__run
        self.__runMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get if mplayer is started or not.
    # --------------------------------------------------------------------------
    def isStarted(self):
        """Get if mplayer is started or not.
        @return: True or False.
        """
        return self.__getRun()

    # --------------------------------------------------------------------------
    # Set the run flag value.
    # --------------------------------------------------------------------------
    def __setRun(self, value):
        """Set the run flag value.
        @param value: Flag value. <True|False>
        """
        self.__runMutex.acquire()
        self.__run = value
        self.__runMutex.release()

    # --------------------------------------------------------------------------
    # Main loop of mplayer.
    # --------------------------------------------------------------------------
    def __mainLoop(self, uri):
        """Main loop of mplayer.
        """
        if self.__getRun():
            return
        self.__runMutex.acquire()
        cmd = [
            self.__appMplayer,
            "-slave",
            "-ao",
            self.__device,
            "-playlist",
            uri,
        ]
        if uri.lower().find("mms") == 0:
            uri = "http" + uri[3:]
        if uri.lower().find(".m3u") == -1:
            if uri.lower().find("http") == 0:
                cmd.pop(4)
        try:
            self.__process = subprocess.Popen(
                cmd,
                stdin = subprocess.PIPE,
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE)
        except:
            self.__runMutex.release()
            return
        incompleteLine = ""
        self.__run = True
        self.__runMutex.release()
        while self.__getRun():
            try:
                buffer = self.__process.stdout.read(100)
            except:
                time.sleep(0.1)
                self.stop()
                break

    # --------------------------------------------------------------------------
    # Send a command to mplayer.
    # --------------------------------------------------------------------------
    def sendCommand(self, command):
        """Send a command to mplayer.
        """
        if self.__process != None:
            self.__process.stdin.write("%s\n" % command)
