# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from tuxisalive.api.base.ApiBaseChildResource import ApiBaseChildResource

# ------------------------------------------------------------------------------
# Class to play the attitune files.
# ------------------------------------------------------------------------------
class Attitune(ApiBaseChildResource):
    """Class to play the attitune files.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, apiBase, apiBaseServer):
        """Constructor of the class.
        @param apiBase: ApiBase parent object.
        @param apiBaseServer: ApiBaseServer object.
        """
        ApiBaseChildResource.__init__(self, apiBase, apiBaseServer)

    # --------------------------------------------------------------------------
    # Load an attitune file.
    # --------------------------------------------------------------------------
    def load(self, path):
        """Load an attitune file.
        @param path: path of the attitune file.
        @return: the success of the command.
        """
        if not self._checkObjectType('path', path, "str"):
            return False
        parameters = {
            'path' : path,
        }
        cmd = "attitune/load?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Play the loaded attitune.
    # --------------------------------------------------------------------------
    def play(self, begin = 0.0):
        """Play the loaded attitune.
        @param begin: starting second.
        @return: the success of the command.
        """
        if not self._checkObjectType('begin', begin, "float"):
            return False
        parameters = {
            'begin' : begin,
        }
        cmd = "attitune/play?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Load and play an attitune file.
    # --------------------------------------------------------------------------
    def loadAndPlay(self, path):
        """Load and play an attitune file.
        @param path: path of the attitune file.
        @return: the success of the command.
        """
        if not self.load(path):
            return False
        return self.play()

    # --------------------------------------------------------------------------
    # Stop the current attitune.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the current attitune.
        @return: the success of the command.
        """
        cmd = "attitune/stop?"
        return self._sendCommandBooleanResult(cmd)
