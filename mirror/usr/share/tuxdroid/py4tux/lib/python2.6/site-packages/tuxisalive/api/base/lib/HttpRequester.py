# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import threading
import xml.dom.minidom
from xml.dom.minidom import Node
import httplib
import socket
import time

# ------------------------------------------------------------------------------
# HttpRequester is a sender of request to a Tuxdroid service server.
# ------------------------------------------------------------------------------
class HttpRequester(object):
    """HttpRequester is a sender of request to a Tuxdroid service server.
    The resulting xml data is automatically parsed and returned to a
    data structure.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, host = '127.0.0.1', port = 270):
        """Constructor of the class.
        @param host: host of the server.
        @param port: port of the server.
        """
        self.__hostPort = "%s:%d" % (host, port)
        self.__mutex = threading.Lock()

    # --------------------------------------------------------------------------
    # Make a request to the server.
    # --------------------------------------------------------------------------
    def request(self, cmd, method = "GET", complexeXml = False):
        """Make a request to the server.
        @param cmd: formated command in an url.
        @param method: method of the request.
        @return: a data structure.
        """
        cmd = "/%s" % cmd
        xmlStruct = {
            'result' : 'Failed',
            'data_count' : 0,
            'server_run' : 'Failed',
        }
        resultStr = self.__requester(self.__hostPort, cmd, method)
        if resultStr != None:
            if not complexeXml:
                xmlStruct = self.__parseXml(resultStr)
            else:
                xmlStruct = self.__xmlToStruct(resultStr)
        return xmlStruct

    # --------------------------------------------------------------------------
    # Set the targeted server address.
    # --------------------------------------------------------------------------
    def setServerAddress(self, host = '127.0.0.1', port = 270):
        """Set the targeted server address.
        @param host: host of the server.
        @param port: port of the server.
        """
        self.__mutex.acquire()
        self.__hostPort = "%s:%d" % (host, port)
        self.__mutex.release()

    # --------------------------------------------------------------------------
    # Url requester.
    # --------------------------------------------------------------------------
    def __requester(self, address, cmd, method = "GET"):
        """Url requester.
        """
        result = None
        retryCount = 0
        while True:
            self.__mutex.acquire()
            # Connect to the server
            h = httplib.HTTPConnection(address)
            try:
                h.request(method, cmd)
            except socket.error, (errno, strerror):
                if errno == 10061:
                    # Connection refused. (No server or server DoS)
                    h.close()
                    retryCount += 1
                    if retryCount >= 3:
                        result = None
                        self.__mutex.release()
                        break
                    self.__mutex.release()
                    time.sleep(0.5)
                    continue
                elif errno == 10048:
                    # Connection already in use. (Server DoS)
                    h.close()
                    self.__mutex.release()
                    time.sleep(0.5)
                    continue
                else:
                    # Unexpected error.
                    h.close()
                    retryCount += 1
                    if retryCount > 3:
                        result = None
                        self.__mutex.release()
                        break
                    self.__mutex.release()
                    time.sleep(0.5)
                    continue
            except httplib.CannotSendRequest:
                # Error while server DoS
                h.close()
                self.__mutex.release()
                time.sleep(0.5)
                continue
            except:
                # Unexpected error.
                h.close()
                self.__mutex.release()
                time.sleep(0.5)
                continue
            # Get the responds
            try:
                f = h.getresponse()
                result = f.read()
            except socket.error, (errno, strerror):
                h.close()
                self.__mutex.release()
                time.sleep(0.5)
                continue
            except httplib.HTTPException:
                h.close()
                self.__mutex.release()
                time.sleep(0.5)
                continue
            except:
                h.close()
                self.__mutex.release()
                time.sleep(0.5)
                continue
            h.close()
            self.__mutex.release()
            break
        return result

    # --------------------------------------------------------------------------
    # Parse the xml string to a data structure.
    # --------------------------------------------------------------------------
    def __parseXml(self, string):
        """Parse the xml string to a data structure.
        """
        struct = {
            'result' : 'Failed',
            'data_count' : 0,
            'server_run' : 'Success',
        }
        dataCount = 0
        dataNodeName = ""
        try:
            root = xml.dom.minidom.parseString(string).firstChild
            for iNode in range(len(root.childNodes)):
                node = root.childNodes.item(iNode)
                if node.firstChild.nodeValue != None:
                    struct[node.nodeName] = node.firstChild.data.encode("utf-8")
                else:
                    subStruct = {}
                    for jNode in range(len(node.childNodes)):
                        node1 = node.childNodes.item(jNode)
                        subStruct[node1.nodeName] = node1.firstChild.data.encode("utf-8")
                    if node.nodeName == "data":
                        dataNodeName = "data%d" % dataCount
                        dataCount += 1
                    else:
                        dataNodeName = node.nodeName
                    struct[dataNodeName] = subStruct

            struct["data_count"] = dataCount
        except:
            pass

        return struct

    # --------------------------------------------------------------------------
    # Get a dict structure from a xml file.
    # --------------------------------------------------------------------------
    def __xmlToStruct(self, string):
        """Get a dict structure from a xml file.
        """
        struct = {
            'result' : 'Failed',
            'data_count' : 0,
            'server_run' : 'Success',
        }
        def nodeXMLToStruct(parentNode, nodeStruct):
            iDataCount = 0
            for i, childNode in enumerate(parentNode.childNodes):
                if childNode.nodeValue == None:
                    it = parentNode.getElementsByTagName(childNode.localName)
                    try:
                        t = len(it[0].childNodes)
                    except:
                        name = childNode.localName.encode('utf-8','replace')
                        nDict = ''
                        nodeStruct[name] = nDict
                        continue
                    name = childNode.localName
                    if len(it) == 1:
                        if len(it[0].childNodes) > 0:
                            value = it[0].childNodes[0].nodeValue
                            if value != None:
                                leafName = name.encode('utf-8','replace')
                                value = value.encode('utf-8','replace')
                                nodeStruct[leafName] = value
                                continue
                    if name == "data":
                        name = "data%d" % iDataCount
                        iDataCount += 1
                    nDict = {}
                    nodeStruct[name] = nDict
                    nodeXMLToStruct(childNode, nodeStruct[name])

        xmlObj = xml.dom.minidom.parseString(string)
        tmpStruct = {}
        nodeXMLToStruct(xmlObj, tmpStruct)
        xmlObj.unlink()
        del(xmlObj)
        if tmpStruct.has_key('root'):
            return tmpStruct['root']
        else:
            return struct
        return struct
