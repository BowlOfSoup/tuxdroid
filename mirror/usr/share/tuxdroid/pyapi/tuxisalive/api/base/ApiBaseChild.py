# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from lib.Helper import Helper

# ------------------------------------------------------------------------------
# Base class to add functionalities in the API.
# ------------------------------------------------------------------------------
class ApiBaseChild(Helper):
    """Base class to add functionalities in the API.
    """

    __ENCODING = "latin-1"

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, apiBase):
        """Constructor of the class.
        @param apiBase: ApiBase parent object.
        """
        Helper.__init__(self)
        self.__apiBase = apiBase
        self.__eventsHandler = self.__apiBase.getEventsHandler()
        self.__methodsList = []
        oElementsList = dir(self)
        self.__methodsList.append("__init__")
        for element in oElementsList:
            if element.find("__") == -1:
                if str(type(getattr(self, element)))== "<type 'instancemethod'>":
                    self.__methodsList.append(element)

    # --------------------------------------------------------------------------
    # Get the parent ApiBase object.
    # --------------------------------------------------------------------------
    def getParent(self):
        """Get the parent ApiBase object.
        @return: A ApiBase object.
        """
        return self.__apiBase

    # --------------------------------------------------------------------------
    # Get the global events handler.
    # --------------------------------------------------------------------------
    def getEventsHandler(self):
        """Get the global events handler.
        @return: The events handler.
        """
        return self.__eventsHandler

    # --------------------------------------------------------------------------
    # Set the source encoding.
    # --------------------------------------------------------------------------
    def setEncoding(self, encoding = "latin-1"):
        """Set the source encoding. Texts need to be encoded in "utf-8" before
        to sending it to the HTTP server.
        @param encoding: source encoding
                         example : "latin-1", "utf-8", "cp1252", ...
        """
        ApiBaseChild.__ENCODING = encoding

    # --------------------------------------------------------------------------
    # Set the current console encoding.
    # --------------------------------------------------------------------------
    def isConsole(self):
        """Set the current console encoding.
        (Only if the api run in an interactive python context)
        """
        import sys
        ApiBaseChild.__ENCODING = sys.stdin.encoding

    # --------------------------------------------------------------------------
    # Fixe a text with the correct encoding.
    # --------------------------------------------------------------------------
    def _reencodeText(self, text, removeReturns = False):
        """Fixe a text with the correct encoding.
        @param text: Text to fixe.
        @param removeReturns: True or False. Replace the returns chars by ". "
        @return: The fixed text.
        """
        # Try to encode the string
        try:
            text = text.decode(ApiBaseChild.__ENCODING)
            text = text.encode("utf-8", 'replace')
        except:
            pass
        # Remove ending lines
        if removeReturns:
            text = text.replace("\n", ". ")
        return text

    # --------------------------------------------------------------------------
    # Wait for a specific value of a status.
    # --------------------------------------------------------------------------
    def _waitFor(self, statusName, statusValue, timeout = 99999.0):
        """Wait for a specific value of a status.
        @param statusName: Status name.
        @param statusValue: Status value.
        @param timeout: Maximal delay to wait.
        """
        return self.__eventsHandler.waitCondition(statusName, (statusValue,
            None), timeout)

    # --------------------------------------------------------------------------
    # Check the type of an object.
    # --------------------------------------------------------------------------
    def _checkObjectType(self, name, value, requestedType):
        """Check the type of an object.
        @param name: Name of the object.
        @param value: Current value of the object.
        @param requestedType: Requested type.
        """
        # Get the type of the value to check
        vType = str(type(value))
        vType = vType[vType.find("'") + 1:vType.rfind("'")]
        # Check the type of the value
        if vType != requestedType:
            print "Invalid type for [%s] : Need <type'%s'>" % (name,
                requestedType)
            return False
        return True

    # --------------------------------------------------------------------------
    # Register a callback to an event.
    # --------------------------------------------------------------------------
    def _registerEvent(self, eventName, eventValue, funct, idx = None):
        """Register a callback to an event.
        @param eventName: Event name.
        @param eventValue: Event value. (can be None)
        @param funct: pointer to the function.
        @param idx: index from a previous register.
        @return: the new index of the callback in the handler.
        """
        nIdx = self.__eventsHandler.register(eventName, funct, (eventValue,
            None), idx)
        return nIdx

    # --------------------------------------------------------------------------
    # Unregister a callback from an event.
    # --------------------------------------------------------------------------
    def _unregisterEvent(self, eventName, idx):
        """Unregister a callback from an event.
        Not available for CLIENT_LEVEL_ANONYME level.
        @param eventName: Event name.
        @param idx: index from a previous register.
        """
        self.__eventsHandler.unregister(eventName, idx)

    # --------------------------------------------------------------------------
    # Insert a new event/status name in the events handler.
    # --------------------------------------------------------------------------
    def _insertNewEvent(self, eventName):
        """Insert a new event/status name in the events handler.
        @param eventName: Event name.
        """
        self.__eventsHandler.insert(eventName)

    # --------------------------------------------------------------------------
    # Get the last knowed value of a status/event.
    # --------------------------------------------------------------------------
    def _requestOne(self, statusName):
        """Get the last knowed value of a status/event.
        @param statusName: Name of the status.event.
        @return: The value.
        """
        if not self._checkObjectType('statusName', statusName, "str"):
            return None
        eventHandler = self.__eventsHandler.getEventHandler(statusName)
        if eventHandler == None:
            return None
        statusStruct = eventHandler.getLastState()
        if statusStruct == None:
            return None
        if len(statusStruct) == 0:
            return None
        return statusStruct[0]
