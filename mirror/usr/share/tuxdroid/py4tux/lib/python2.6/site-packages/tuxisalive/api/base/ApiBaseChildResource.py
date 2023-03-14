# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import urllib

from ApiBaseChild import ApiBaseChild

# ------------------------------------------------------------------------------
# Base class to exploit resources in the API.
# ------------------------------------------------------------------------------
class ApiBaseChildResource(ApiBaseChild):
    """Base class to exploit resources in the API.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, apiBase, apiBaseServer):
        """Constructor of the class.
        @param apiBase: ApiBase parent object.
        @param apiBaseServer: ApiBaseServer object.
        """
        ApiBaseChild.__init__(self, apiBase)
        self.__server = apiBaseServer

    # --------------------------------------------------------------------------
    # Get the ApiBaseServer object.
    # --------------------------------------------------------------------------
    def getServer(self):
        """Get the ApiBaseServer object.
        @return: An ApiBaseServer object.
        """
        return self.__server

    # --------------------------------------------------------------------------
    # Compute paramaters dictionary to valid url.
    # --------------------------------------------------------------------------
    def __computeParameters(self, parameters):
        """Compute paramaters dictionary to valid url.
        @param parameters: Parameters dictionary.
        @return: A string url.
        """
        result = ""
        if len(parameters.keys()) > 0:
            for key in parameters.keys():
                parameters[key] = self._reencodeText(parameters[key])
            result = urllib.urlencode(parameters)
        return result

    # --------------------------------------------------------------------------
    # Send a command to the server.
    # --------------------------------------------------------------------------
    def _sendCommandBooleanResult(self, cmd, parameters = {}):
        """Send a command to the server.
        @param cmd: Command to send.
        @return: True or False.
        """
        cmd = "%s%s" % (cmd, self.__computeParameters(parameters))
        if self.__server.request(cmd, {}, {}):
            return True
        return False

    # --------------------------------------------------------------------------
    # Send a command to the server.
    # --------------------------------------------------------------------------
    def _sendCommandFullResult(self, cmd, parameters = {}):
        """Send a command to the server.
        @param cmd: Command to send.
        @return: A tuple as (<boolean>, <dictionary>)
        """
        cmd = "%s%s" % (cmd, self.__computeParameters(parameters))
        result = {}
        if self.__server.request(cmd, {}, result):
            return True, result
        return False, None

    # --------------------------------------------------------------------------
    # Send a command to the server.
    # --------------------------------------------------------------------------
    def _sendCommandFullResultEx(self, cmd, parameters = {}):
        """Send a command to the server.
        @param cmd: Command to send.
        @return: A tuple as (<boolean>, <dictionary>)
        """
        cmd = "%s%s" % (cmd, self.__computeParameters(parameters))
        result = {}
        if self.__server.request(cmd, {}, result, False, True):
            return True, result
        return False, None

    # --------------------------------------------------------------------------
    # Syndicate the api to an event/status.
    # --------------------------------------------------------------------------
    def _syndicateEvent(self, eventName):
        """Syndicate the api to an event/status.
        @param eventName: Event/status name.
        """
        self.__server.syndicate(eventName)

    # --------------------------------------------------------------------------
    # Unsyndicate the api from an event/status.
    # --------------------------------------------------------------------------
    def _unSyndicateEvent(self, eventName):
        """Unsyndicate the api from an event/status.
        @param eventName: Event/status name.
        """
        self.__server.unSyndicate(eventName)
