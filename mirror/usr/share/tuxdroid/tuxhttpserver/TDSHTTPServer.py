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

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import sys
import traceback
import threading
import os
import time
import urllib
import cgi

from util.logger import *
from TDSConfiguration import *

resourcesManager = None
serverLogger = None

# ------------------------------------------------------------------------------
# Tux Droid Server : HTTP Server.
# ------------------------------------------------------------------------------
class TDSHTTPServer(object):
    """Tux Droid Server : HTTP Server.
    """

    # --------------------------------------------------------------------------
    # Contructor.
    # --------------------------------------------------------------------------
    def __init__(self, resManager):
        """Constructor.
        @param resManager: Resource manager (to share with the request handler)
        """
        global resourcesManager
        global serverLogger

        resourcesManager = resManager
        self.__logger = SimpleLogger(TDS_FILENAME_HTTPSERVER_LOG)
        serverLogger = self.__logger
        self.__logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.__logger.setTarget(TDS_CONF_LOG_TARGET)
        self.__logger.resetLog()
        self.__logger.logInfo("-----------------------------------------------")
        self.__logger.logInfo("TDSHTTPServer%s" % __version__)
        self.__logger.logInfo("Author : %s" % __author__)
        self.__logger.logInfo("Licence : %s" % __licence__)
        self.__logger.logInfo("-----------------------------------------------")
        self.__started = False
        self.__startedMutex = threading.Lock()
        self.__server = None
        self.__createServer()

    # --------------------------------------------------------------------------
    # Create the HTTP server.
    # --------------------------------------------------------------------------
    def __createServer(self):
        """Create the HTTP server.
        """
        if self.__server != None:
            return False
        try:
            if TDS_HTTP_ASYNCHRONOUS_REQUESTS:
                self.__server = ThreadedHTTPServer((TDS_CONF_HOST_ADDRESS,
                    TDS_HTTP_PORT), TDSHttpRequestHandler)
            else:
                self.__server = HTTPServer((TDS_CONF_HOST_ADDRESS,
                    TDS_HTTP_PORT), TDSHttpRequestHandler)
            self.__logger.logInfo("Create an HTTP server on port %d" % TDS_HTTP_PORT)
        except:
            self.__server = None
            self.__logger.logError("(__createServer) Can't create the server")
            return False
        return True

    # --------------------------------------------------------------------------
    # Start the server.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the server.
        """
        if self.__getStarted():
            return False
        if self.__server == None:
            return False
        try:
            self.__setStarted(True)
            self.__logger.logInfo("Server started.")
            if TDS_HTTP_ASYNCHRONOUS_ACCEPT:
                self.__server.socket.setblocking(0)
                while self.__getStarted():
                    self.__server.handle_request()
                    time.sleep(TDS_HTTP_ASYNCHRONOUS_ACCEPT_DELAY)
            else:
                while self.__getStarted():
                    self.__server.handle_request()
        except:
            self.__logger.logError("(Start) Unexpected error.")
            self.__logger.logError(self.__formatException())
        self.__logger.logInfo("Server stopped.")
        self.__setStarted(False)
        return True

    # --------------------------------------------------------------------------
    # Stop the server.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the server.
        """
        self.__setStarted(False)

    # --------------------------------------------------------------------------
    # Set the value of the started flag.
    # --------------------------------------------------------------------------
    def __setStarted(self, value = True):
        """Set the value of the started flag.
        @param value: True or False.
        """
        self.__startedMutex.acquire()
        self.__started = value
        self.__startedMutex.release()

    # --------------------------------------------------------------------------
    # Get the value of the started flag.
    # --------------------------------------------------------------------------
    def __getStarted(self):
        """Get the value of the started flag.
        @return: True or False.
        """
        value = False
        self.__startedMutex.acquire()
        value = self.__started
        self.__startedMutex.release()
        return value

    # --------------------------------------------------------------------------
    # Get the value of the started flag.
    # --------------------------------------------------------------------------
    def getStarted(self):
        """Get the value of the started flag.
        @return: True or False.
        """
        return self.__getStarted()

    # --------------------------------------------------------------------------
    # Get if the server has been created or not.
    # --------------------------------------------------------------------------
    def getCreated(self):
        """Get if the server has been created or not.
        @return: True or False.
        """
        if self.__server == None:
            return False
        else:
            return True

    # --------------------------------------------------------------------------
    # Format the last exception to a string.
    # --------------------------------------------------------------------------
    def __formatException(self):
        """Format the last exception to a string.
        @return: The formated string.
        """
        fList = traceback.format_exception(sys.exc_info()[0],
                    sys.exc_info()[1],
                    sys.exc_info()[2])
        result = ""
        for line in fList:
            result += line
        return result

# ------------------------------------------------------------------------------
# Tux Droid Server : Threaded HTTP Server.
# ------------------------------------------------------------------------------
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread.
    """
    #allow_reuse_address = 0

# ------------------------------------------------------------------------------
# Tux Droid Server : HTTP request handler.
# ------------------------------------------------------------------------------
class TDSHttpRequestHandler(BaseHTTPRequestHandler):
    """Tux Droid Server : HTTP request handler.
    """

    # Configure the socket FileIO R/W
    rbufsize = 1024
    wbufsize = 1024

    # --------------------------------------------------------------------------
    # Format the last exception to a string.
    # --------------------------------------------------------------------------
    def __formatException(self):
        """Format the last exception to a string.
        @return: The formated string.
        """
        fList = traceback.format_exception(sys.exc_info()[0],
                    sys.exc_info()[1],
                    sys.exc_info()[2])
        result = ""
        for line in fList:
            result += line
        return result

    # --------------------------------------------------------------------------
    # Send the headers to the clients.
    # --------------------------------------------------------------------------
    def __sendHeaders(self, headers, content):
        """Send the headers to the clients.
        @param headers: Headers.
        @param content: Content of the response stream (for this length)
        @return: True or False.
        """
        try:
            if headers != None:
                for header in headers:
                    self.send_header(header[0], header[1])
                if content != None:
                    self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                return True
        except:
            serverLogger.logError("(__sendHeaders) Error while sending headers")
            serverLogger.logError(self.__formatException())
            return False

    # --------------------------------------------------------------------------
    # Handling a "HEADER" request.
    # --------------------------------------------------------------------------
    def do_HEADER(self):
        """Handling a "HEADER" request.
        """
        self.path = urllib.unquote_plus(self.path)
        serverLogger.logDebug("Request : (%s)" % self.path)
        code, headers, content = resourcesManager.executeUrl(self.path)
        if TDS_50MSEC_OPTIMISATION:
            time.sleep(0.05)
        if code == 404:
            try:
                serverLogger.logWarning("Invalid request : (%s)" % self.path)
                self.send_error(404, 'Service Not Found')
            except:
                serverLogger.logError("(do_HEADER) Error while sending 404 error")
                serverLogger.logError(self.__formatException())
        else:
            try:
                self.send_response(code)
            except:
                serverLogger.logError("(do_HEADER) Error while sending response code")
                serverLogger.logError(self.__formatException())
            self.__sendHeaders(headers, content)

    # --------------------------------------------------------------------------
    # Handling a "GET" request.
    # --------------------------------------------------------------------------
    def do_GET(self):
        """Handling a "GET" request.
        """
        self.path = urllib.unquote_plus(self.path)
        serverLogger.logDebug("Request : (%s)" % self.path)
        if TDS_50MSEC_OPTIMISATION:
            time.sleep(0.05)
        code, headers, content = resourcesManager.executeUrl(self.path)
        if code == 404:
            try:
                serverLogger.logWarning("Invalid request : (%s)" % self.path)
                self.send_error(404, 'Service Not Found')
            except:
                serverLogger.logError("(do_GET) Error while sending 404 error")
                serverLogger.logError(self.__formatException())
        else:
            try:
                self.send_response(code)
            except:
                serverLogger.logError("(do_HEADER) Error while sending response code")
                serverLogger.logError(self.__formatException())
            if not self.__sendHeaders(headers, content):
                return
            if content != None:
                try:
                    self.wfile.write(content)
                    self.wfile.flush()
                except:
                    serverLogger.logError("(do_GET) Error while sending content")
                    serverLogger.logError(self.__formatException())

    # --------------------------------------------------------------------------
    # Handling a "POST" request.
    # --------------------------------------------------------------------------
    def do_POST(self):
        """Handling a "POST" request.
        """
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ = {
                        'REQUEST_METHOD':'POST',
                        'CONTENT_TYPE':self.headers['Content-Type'],
                      })
        # Reformat request as GET command
        self.path += "?"
        for field in form.keys():
            field_item = form[field]
            self.path += "%s=%s&" % (field, form[field].value)
        if self.path[-1] == "&":
            self.path = self.path[:-1]
        serverLogger.logDebug("Request : (%s)" % self.path)
        if TDS_50MSEC_OPTIMISATION:
            time.sleep(0.05)
        code, headers, content = resourcesManager.executeUrl(self.path)
        #headers.append(["Location", self.path])
        if code == 404:
            try:
                serverLogger.logWarning("Invalid request : (%s)" % self.path)
                self.send_error(404, 'Service Not Found')
            except:
                serverLogger.logError("(do_GET) Error while sending 404 error")
                serverLogger.logError(self.__formatException())
        else:
            try:
                self.send_response(code)
            except:
                serverLogger.logError("(do_HEADER) Error while sending response code")
                serverLogger.logError(self.__formatException())
            if not self.__sendHeaders(headers, content):
                return
            if content != None:
                try:
                    self.wfile.write(content)
                    self.wfile.flush()
                except:
                    serverLogger.logError("(do_GET) Error while sending content")
                    serverLogger.logError(self.__formatException())

    # --------------------------------------------------------------------------
    # Handle one request.
    # --------------------------------------------------------------------------
    def handle_one_request(self):
        """Handle one request.
        (handled in order to prevent any communication error)
        """
        try:
            BaseHTTPRequestHandler.handle_one_request(self)
        except:
            serverLogger.logError("(handle_one_request) Unexpected error")
            serverLogger.logError(self.__formatException())

    # --------------------------------------------------------------------------
    # Log request.
    # --------------------------------------------------------------------------
    def log_request(self, code='-', size='-'):
        """Log request.
        """
        pass
