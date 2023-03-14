#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import subprocess
import threading
import time

# ------------------------------------------------------------------------------
# Web viewer class.
# ------------------------------------------------------------------------------
class WebViewer(object):
    """Web viewer class.
    This class create a window which embbed a webbrowser.
    This class only work on Windows.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, title, url, width = -1, height = -1):
        """Constructor of the class.
        @param title: Window title.
        @param url: Browse this url.
        @param width: Window width.
        @param height: Window height.
        """
        if os.name == 'nt':
            mPath, mFile = os.path.split(__file__)
            self.__appWebViewer = os.path.join(mPath, 'webviewer.exe')
        else:
            self.__appWebViewer = ''
        self.__runMutex = threading.Lock()
        self.__run = False
        self.__process = None
        self.__title = title
        self.__url = url
        self.__width = width
        self.__height = height

    # --------------------------------------------------------------------------
    # Start web viewer.
    # --------------------------------------------------------------------------
    def start(self):
        """Start Start web viewer.
        """
        if os.name != 'nt':
            return
        t = threading.Thread(target = self.__mainLoop)
        t.start()

    # --------------------------------------------------------------------------
    # Stop web viewer.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop web viewer.
        """
        if not self.__getRun():
            return
        if self.__process != None:
            if os.name == 'nt':
                import win32api
                try:
                    win32api.TerminateProcess(int(self.__process._handle), -1)
                except:
                    pass
            else:
                os.system("kill -9 " + str(self.__process.pid))
        self.__setRun(False)
        self.__process = None
        time.sleep(0.25)

    # --------------------------------------------------------------------------
    # Get if web viewer is started or not.
    # --------------------------------------------------------------------------
    def __getRun(self):
        """Get if web viewer is started or not.
        @return: True or False.
        """
        self.__runMutex.acquire()
        result = self.__run
        self.__runMutex.release()
        return result

    # --------------------------------------------------------------------------
    # Get if web viewer is started or not.
    # --------------------------------------------------------------------------
    def isStarted(self):
        """Get if web viewer is started or not.
        @return: True or False.
        """
        return self.__getRun()

    # --------------------------------------------------------------------------
    # Set if web viewer is started or not.
    # --------------------------------------------------------------------------
    def __setRun(self, value):
        """Set if web viewer is started or not.
        @param value: Flag value. <True|False>
        """
        self.__runMutex.acquire()
        self.__run = value
        self.__runMutex.release()

    # --------------------------------------------------------------------------
    # Main loop of web viewer.
    # --------------------------------------------------------------------------
    def __mainLoop(self):
        """Main loop of web viewer.
        """
        if self.__getRun():
            return
        self.__setRun(True)
        cmd = [
            self.__appWebViewer,
            self.__title,
            self.__url,
            '%d' % self.__height,
            '%d' % self.__width,
        ]
        self.__process = subprocess.Popen(
            cmd,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
        while self.__getRun():
            try:
                buffer = self.__process.stdout.read(100)
            except:
                buffer = ""
            if len(buffer) == 0:
                self.stop()
