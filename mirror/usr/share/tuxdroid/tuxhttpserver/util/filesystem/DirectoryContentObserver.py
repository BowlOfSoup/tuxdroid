#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is highly inspired by a module of "Karma-Lab Common Toolkits" a
#    java library written by "Yoran Brault" <http://artisan.karma-lab.net>
#

import os
import time
import threading
try:
    from hashlib import md5
except:
    from md5 import md5

from util.misc.DirectoriesAndFilesTools import *

# ------------------------------------------------------------------------------
# Class to observe the files events from a directory. (file removed, file added)
# ------------------------------------------------------------------------------
class DirectoryContentObserver(object):
    """Class to observe the files events from a directory. (file removed,
    file added)
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, name):
        """Constructor of the class.
        @param name: Name of the instance of the class.
        """
        self.__name = name
        self.__mutex = threading.Lock()
        self.__isStarted = False
        self.__observerThread = None
        self.__directory = None
        self.__filesInfo = {}
        self.__filters = []
        self.__rate = 1.5
        self.__onAddedFileCallback = None
        self.__onRemovedFileCallback = None

    # --------------------------------------------------------------------------
    # Destructor of the class.
    # --------------------------------------------------------------------------
    def __del__(self):
        """Destructor of the class.
        """
        self.stop()

    # --------------------------------------------------------------------------
    # Get the instance name.
    # --------------------------------------------------------------------------
    def getName(self):
        """Get the instance name.
        @return: A string.
        """
        self.__mutex.acquire()
        name = self.__name
        self.__mutex.release()
        return name

    # --------------------------------------------------------------------------
    # Check for directory updates.
    # --------------------------------------------------------------------------
    def check(self):
        """Check for directory updates.
        """
        self.__checkForUpdate()

    # --------------------------------------------------------------------------
    # Start the observation of the selected directory.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the observation of the selected directory.
        @return: The start success as boolean.
        """
        if self.getDirectory() == None:
            return False
        if self.isStarted():
            return False
        self.__checkForUpdate()
        self.__setStarted(True)
        self.__observerThread = threading.Thread(target = self.__observerLoop)
        self.__observerThread.start()
        return True

    # --------------------------------------------------------------------------
    # Stop the current directory observation.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the current directory observation.
        """
        self.__setStarted(False)
        if self.__observerThread != None:
            if self.__observerThread.isAlive():
                if not self.__observerThread.join(self.__rate * 2):
                    self.__observerThread._Thread__stop()
        for key in self.__filesInfo.keys():
            if self.__onRemovedFileCallback != None:
                fileName = os.path.join(self.getDirectory(),
                    self.__filesInfo[key])
                self.__onRemovedFileCallback(self.getName(), fileName)

    # --------------------------------------------------------------------------
    # Set the directory to observe.
    # --------------------------------------------------------------------------
    def setDirectory(self, directory):
        """Set the directory to observe.
        @param directory: Directory path.
        """
        MKDirs(directory)
        if os.path.isdir(directory):
            self.__mutex.acquire()
            self.__directory = directory
            self.__mutex.release()

    # --------------------------------------------------------------------------
    # Get the current directory to observe.
    # --------------------------------------------------------------------------
    def getDirectory(self):
        """Get the current directory to observe.
        @return: A string.
        """
        self.__mutex.acquire()
        directory = self.__directory
        self.__mutex.release()
        return directory

    # --------------------------------------------------------------------------
    # Set the file filters.
    # --------------------------------------------------------------------------
    def setFilters(self, filters = ['.tgf',]):
        """Set the file filters.
        Only the files of the referenced extensions will be observed.
        @param filters: filters as list of strings.
        """
        self.__mutex.acquire()
        self.__filters = filters
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Get the file filters.
    # --------------------------------------------------------------------------
    def getFilters(self):
        """ Get the file filters.
        @return: A list of strings.
        """
        self.__mutex.acquire()
        filters = self.__filters
        self.__mutex.release()
        return filters

    # --------------------------------------------------------------------------
    # Set the speed rate of the observation.
    # --------------------------------------------------------------------------
    def setRate(self, rate):
        """Set the speed rate of the observation.
        @param rate: Speed rate in seconds as float.
        """
        self.__mutex.acquire()
        self.__rate = rate
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Get the speed rate of the observation.
    # --------------------------------------------------------------------------
    def getRate(self):
        """Get the speed rate of the observation.
        @return: A float.
        """
        self.__mutex.acquire()
        rate = self.__rate
        self.__mutex.release()
        return rate

    # --------------------------------------------------------------------------
    # Get if the observation is started or not.
    # --------------------------------------------------------------------------
    def isStarted(self):
        """Get if the observation is started or not.
        @return: A boolean.
        """
        self.__mutex.acquire()
        isStarted = self.__isStarted
        self.__mutex.release()
        return isStarted

    # --------------------------------------------------------------------------
    # Set if the started flag value.
    # --------------------------------------------------------------------------
    def __setStarted(self, isStarted):
        """Set if the started flag value.
        @param isStarted: Flag value as boolean.
        """
        self.__mutex.acquire()
        self.__isStarted = isStarted
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Set the added file event callback.
    # --------------------------------------------------------------------------
    def setOnAddedFileCallback(self, funct):
        """Set the added file event callback.
        @param funct: Function pointer.
        Function prototype:
        def onAddedFile(observerName, fileName):
            pass
        """
        self.__onAddedFileCallback = funct

    # --------------------------------------------------------------------------
    # Set the removed file event callback.
    # --------------------------------------------------------------------------
    def setOnRemovedFileCallback(self, funct):
        """Set the removed file event callback.
        @param funct: Function pointer.
        Function prototype:
        def onRemovedFile(observerName, fileName):
            pass
        """
        self.__onRemovedFileCallback = funct

    # --------------------------------------------------------------------------
    # Observe the directory.
    # --------------------------------------------------------------------------
    def __checkForUpdate(self):
        """Observe the directory.
        """
        directory = self.getDirectory()
        if directory == None:
            return
        currentContent = {}
        filters = self.getFilters()
        for root, dirs, files in os.walk(directory):
            if os.path.realpath(root) != directory:
                break
            for file in files:
                if len(filters) > 0:
                    matched = False
                    for filter in filters:
                        if file.lower().rfind(filter) == len(file) - len(filter):
                            matched = True
                            break
                    if not matched:
                        continue
                try:
                    timeStruct = time.localtime(os.path.getmtime(
                        os.path.join(root, file)))[:6]
                    fileTime = ""
                    for e in timeStruct:
                        fileTime += str(e)
                    fileSize = os.path.getsize(os.path.join(root, file))
                except:
                    continue
                md5H = md5()
                md5H.update(str(fileSize) + fileTime + file)
                md5Tag = md5H.hexdigest()
                currentContent[md5Tag] = file
        for key in self.__filesInfo.keys():
            if key not in currentContent.keys():
                if self.__onRemovedFileCallback != None:
                    fileName = os.path.join(directory, self.__filesInfo[key])
                    self.__onRemovedFileCallback(self.getName(), fileName)
        # Sort files by date creation in a list
        listedContent = []
        for key in currentContent.keys():
            if key not in self.__filesInfo.keys():
                fileName = os.path.join(directory, currentContent[key])
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fileName)
                listedContent.append([
                    key,
                    fileName,
                    ctime,
                ])
        sortedContent = []
        while len(listedContent) > 0:
            older = 99999999999
            match = []
            for fileInfo in listedContent:
                if fileInfo[2] < older:
                    match = fileInfo
                    older = fileInfo[2]
            listedContent.remove(match)
            sortedContent.append(match)
        for fileInfo in sortedContent:
            if self.__onAddedFileCallback != None:
                if not self.__onAddedFileCallback(self.getName(), fileInfo[1]):
                    del currentContent[fileInfo[0]]
        self.__filesInfo = currentContent

    # --------------------------------------------------------------------------
    # Observation loop.
    # --------------------------------------------------------------------------
    def __observerLoop(self):
        """Observation loop.
        """
        while self.isStarted():
            self.__checkForUpdate()
            m = int(self.__rate / 0.1)
            for i in range(m):
                if self.isStarted():
                    time.sleep(0.1)
                else:
                    return

# ------------------------------------------------------------------------------
# Program entry point for example.
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    def onAddedFile(name, file):
        print "Added file : ", file
        return True

    def onRemovedFile(name, file):
        print "Removed file : ", file

    o = DirectoryContentObserver("c")
    o.setDirectory("c:\\")
    o.setFilters(['.sys',])
    o.setRate(1.5)
    o.setOnAddedFileCallback(onAddedFile)
    o.setOnRemovedFileCallback(onRemovedFile)
    if o.start():
        time.sleep(3.0)
        o.stop()
