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

from ApiBaseChildResource import ApiBaseChildResource
from const.ConstServer import *
from const.ConstClient import *

# ------------------------------------------------------------------------------
# Class to control the statuses.
# ------------------------------------------------------------------------------
class Status(ApiBaseChildResource):
    """Class to control the statuses.
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
    # Get the value and delay of a status.
    # --------------------------------------------------------------------------
    def requestOne(self, statusName):
        """Get the value and delay of a status.
        @return: A tuple (<object>, <float>)
        """
        if not self._checkObjectType("statusName", statusName, "str"):
            return None, None
        eventHandler = self.getEventsHandler().getEventHandler(statusName)
        if eventHandler == None:
            return None, None
        statusStruct = eventHandler.getLastState()
        return statusStruct[0], statusStruct[1]

    # --------------------------------------------------------------------------
    # Send a status.
    # --------------------------------------------------------------------------
    def send(self, statusName, statusValues, encoding = "latin-1"):
        """Send a status.
        @param statusName: name of the status.
        @param statusValues: values of the status as list.
        @param encoding: encoding format of the source.
            ( By example, the encoding must be set with sys.stdin.encoding if
              the status is sent from Tuxshell. The encoding must be set to
              "utf-8" if the status is sent from a python script coded in utf-8)
        @return: the success of the command.
        """
        if not self._checkObjectType('statusName', statusName, "str"):
            return False
        if not self._checkObjectType('statusValues', statusValues, "list"):
            return False
        if len(statusValues) == 0:
            return False
        for statusValue in statusValues:
            if not self._checkObjectType('value in statusValues', statusValue,
                "str"):
                return False
        valuesStr = ""
        for statusValue in statusValues:
            valuesStr += "%s|" % statusValue
        valuesStr = valuesStr[:-1]
        try:
            u = unicode(valuesStr, encoding)
            valuesStr = u.encode("latin-1", 'replace')
        except:
            pass
        try:
            u = statusName.decode(encoding)
            statusName = u.encode("latin-1", 'replace')
        except:
            pass
        parameters = {
            'name' : statusName,
            'value' : valuesStr,
        }
        cmd = "status/send?"
        return self._sendCommandBooleanResult(cmd, parameters)

    # --------------------------------------------------------------------------
    # Wait a specific state of a status.
    # --------------------------------------------------------------------------
    def wait(self, statusName, condition = None, timeout = 999999999.0):
        """Wait a specific state of a status.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param statusName: name of the status.
        @param condition: list of the rules of the condition.
        @param timeout: maximal delay to wait.
        @return: the success of the waiting.
        """
        if self.getServer().getClientLevel() == CLIENT_LEVEL_ANONYME:
            return False
        if not self._checkObjectType('statusName', statusName, "str"):
            return False
        if not self._checkObjectType('timeout', timeout, "float"):
            return False
        if condition != None:
            if not self._checkObjectType('condition', condition, "tuple"):
                return False
        return self.getEventsHandler().waitCondition(statusName, condition, timeout)
