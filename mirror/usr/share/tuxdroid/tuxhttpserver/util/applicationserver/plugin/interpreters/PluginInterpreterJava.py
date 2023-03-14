#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

from PluginInterpreter import PluginInterpreter

# ------------------------------------------------------------------------------
# Java plugin interpreter class.
# ------------------------------------------------------------------------------
class PluginInterpreterJava(PluginInterpreter):
    """Java plugin interpreter class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        PluginInterpreter.__init__(self)
        self.__classPathsList = []
        self.addClassPath(os.path.join(os.path.split(__file__)[0],
            "javacommonjar"))

    # --------------------------------------------------------------------------
    # Add a class path to the interpreter.
    # --------------------------------------------------------------------------
    def addClassPath(self, classPath):
        """Add a class path to the interpreter.
        @param classPath: Class path to add.
        """
        self.__classPathsList.append(classPath)

    # --------------------------------------------------------------------------
    # Set the working path (cwd) of the interpreter.
    # --------------------------------------------------------------------------
    def setWorkingPath(self, workingPath):
        """Set the working path (cwd) of the interpreter.
        @param workingPath: Working path.
        """
        PluginInterpreter.setWorkingPath(self, workingPath)
        self.addClassPath(os.path.join(workingPath, 'libraries'))

    # --------------------------------------------------------------------------
    # Prepare the shell commands list.
    # --------------------------------------------------------------------------
    def prepareCommand(self):
        """Prepare the shell commands list.
        @return: A shell commands as list.
        """
        # Get the jar files in the library
        fClassPath = ''
        for classPath in self.__classPathsList:
            if os.path.isdir(classPath):
                files = os.listdir(classPath)
                for file in files:
                    if file.lower().find(".jar") == (len(file) - 4):
                        if len(fClassPath) > 0:
                            fClassPath += os.pathsep
                        fClassPath += os.path.join(classPath, file)
        command = [
            'java',
            '-cp',
            fClassPath,
            self.getExecutable(),
        ]
        if self.getSplashScreen() != None:
            if os.name == 'nt':
                command.insert(1, "-splash:%s" % self.getSplashScreen())
        return command
