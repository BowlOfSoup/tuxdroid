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

from lib.Helper import Helper
from lib.EventsHandler import EventsHandler
from const.ConstAccess import *
from const.ConstApi import *
from const.ConstClient import *
from const.ConstServer import *

from ApiBaseServer import ApiBaseServer
from Event import Event
from Access import Access
from Status import Status

# ------------------------------------------------------------------------------
# API Base.
# ------------------------------------------------------------------------------
class ApiBase(Helper):
    """API Base.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, host = '127.0.0.1', port = 270):
        """Constructor of the class.
        @param host: host of the server.
        @param port: port of the server.
        """
        # Create the events handler
        self.__eventsHandler = EventsHandler()
        # Register base status/events of the server
        for statusName in SW_NAME_API:
            self.__eventsHandler.insert(statusName)
        for statusName in SW_NAME_EXTERNAL:
            self.__eventsHandler.insert(statusName)
        # Create the client to the server object
        self.server = ApiBaseServer(self, host, port)
        # Create the access object
        self.access = Access(self, self.server)
        # Create the status object
        self.status = Status(self, self.server)
        # Create the event object
        self.event = Event(self, self.server)
        # Initialize the helper
        Helper.__init__(self)

    # --------------------------------------------------------------------------
    # Destructor of the class.
    # --------------------------------------------------------------------------
    def destroy(self):
        """Destructor of the class.
        """
        self.server.destroy()
        self.__eventsHandler.destroy()

    # --------------------------------------------------------------------------
    # Get the events handler.
    # --------------------------------------------------------------------------
    def getEventsHandler(self):
        """Get the events handler.
        @return: The events handler.
        """
        return self.__eventsHandler

    # --------------------------------------------------------------------------
    # Get the events handler.
    # --------------------------------------------------------------------------
    def getEventHandlers(self):
        """Deprecated. Use getEventsHandler()
        """
        return self.__eventsHandler

    # --------------------------------------------------------------------------
    # Get the version of this API.
    # --------------------------------------------------------------------------
    def getVersion(self):
        """Get the version of this api.
        @return: A string.
        """
        return "tuxisalive.lib.base.ApiBase-%s" % __version__
