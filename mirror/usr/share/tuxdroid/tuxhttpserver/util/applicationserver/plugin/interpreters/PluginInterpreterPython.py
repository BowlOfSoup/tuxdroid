#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import util

p = os.path.split(util.__file__)[0]
p = p[:p.rfind(os.sep) + 1]
os.environ['TUXDROID_SERVER_PYTHON_UTIL'] = p

from PluginInterpreter import PluginInterpreter

# ------------------------------------------------------------------------------
# Python plugin interpreter class.
# ------------------------------------------------------------------------------
class PluginInterpreterPython(PluginInterpreter):
    """Python plugin interpreter class.
    """

    # --------------------------------------------------------------------------
    # Prepare the shell commands list.
    # --------------------------------------------------------------------------
    def prepareCommand(self):
        """Prepare the shell commands list.
        @return: A shell commands as list.
        """
        command = [
            'python',
            self.getExecutable(),
        ]
        return command
