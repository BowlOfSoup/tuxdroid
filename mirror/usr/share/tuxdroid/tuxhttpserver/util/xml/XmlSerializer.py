# -*- coding: utf-8 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import sys
import traceback
import cStringIO
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import XMLReader
from xml.sax import make_parser

LAST_TRACE_BACK = "No error"

# ------------------------------------------------------------------------------
# Xml parser handler to make a dictionary from a xml content.
# ------------------------------------------------------------------------------
class DictionaryHandler(ContentHandler):
    """Xml parser handler to make a dictionary from a xml content.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, encoding = "utf-8"):
        """Constructor of the class.
        @param encoding: Encoding of the xml content.
        """
        self.__currentNodeName = ''
        self.__parentNodeName = ''
        self.__nodesCounter = 0
        self.__dictionary = {}
        self.__currentNodeDict = {}
        self.__parentNodeDict = {}
        self.__nodeNameStack = []
        self.__nodeDictsStack = []
        self.__encoding = encoding

    # --------------------------------------------------------------------------
    # Get the resulting dictionary.
    # --------------------------------------------------------------------------
    def getDictionary(self):
        """Get the resulting dictionary.
        @return: A dictionary.
        """
        return self.__dictionary

    # --------------------------------------------------------------------------
    # Start event of a xml element parsing.
    # --------------------------------------------------------------------------
    def startElement(self, nodeName, nodeAttributes):
        """Start event of a xml element parsing.
        @param nodeName: Xml node name.
        @param nodeAttributes: Xml node attributes.
        """
        nodeAttributes = dict(nodeAttributes)
        for key in nodeAttributes.keys():
            try:
                node = nodeAttributes[key]
                node = node.encode(self.__encoding)
                nodeAttributes[key] = node
            except:
                pass
        if self.__nodesCounter == 0:
            self.__parentNodeName = nodeName
            self.__dictionary[nodeName] = [nodeAttributes, '', []]
            self.__currentNodeDict = self.__dictionary
        else:
            self.__parentNodeName = self.__nodeNameStack[-1]
            self.__parentNodeDict = self.__nodeDictsStack[-1]
            childNode = {nodeName: [nodeAttributes, '', []]}
            childNodesList = (self.__parentNodeDict[self.__parentNodeName])[2]
            childNodesList.append(childNode)
            self.__currentNodeDict = childNode
        if nodeName == self.__parentNodeName:
            self.__nodeDictsStack.insert(1, self.__currentNodeDict)
        else:
            self.__nodeDictsStack.append(self.__currentNodeDict)
        self.__nodeNameStack.append(nodeName)
        self.__currentNodeName = nodeName
        self.__nodesCounter += 1

    # --------------------------------------------------------------------------
    # End event of a xml element parsing.
    # --------------------------------------------------------------------------
    def endElement(self, nodeName):
        """End event of a xml element parsing.
        @param nodeName: Xml node name.
        """
        self.__nodeNameStack.remove(nodeName)
        for item in self.__nodeDictsStack:
            if item.has_key(nodeName):
                self.__nodeDictsStack.remove(item)

    # --------------------------------------------------------------------------
    # Event on text content parsing.
    # --------------------------------------------------------------------------
    def characters(self, content):
        """Event on text content parsing.
        @param content: Text content.
        """
        content = content.encode(self.__encoding).strip()
        if content:
            nodeDict = self.__parentNodeDict[self.__parentNodeName][2][-1]
            currentContent = nodeDict[self.__currentNodeName][1]
            nodeDict[self.__currentNodeName][1] = "".join((currentContent,
                content))

# ------------------------------------------------------------------------------
# Xml parser to make a xml content from a dictionary.
# ------------------------------------------------------------------------------
class XmlDictionaryParser(XMLReader):
    """Xml parser to make a xml content from a dictionary.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        XMLReader.__init__(self)
        self.__indent = 0

    # --------------------------------------------------------------------------
    # Start the parsing.
    # --------------------------------------------------------------------------
    def parse(self, dictionary):
        """Start the parsing.
        @param dictionary: Input dictionary.
        """
        self._cont_handler.startDocument()
        self.__parse(dictionary)
        self._cont_handler.endDocument()

    # --------------------------------------------------------------------------
    # Recursive parsing method.
    # --------------------------------------------------------------------------
    def __parse(self, dictionary):
        """Recursive parsing method.
        @param dictionary: Input dictionary.
        """
        for name, data in dictionary.items():
            # Print formating
            self._cont_handler.ignorableWhitespace(" " * self.__indent * 4)
            attributes = data[0]
            text = data[1]
            children = data[2]
            self._cont_handler.startElement(name, attributes)
            self._cont_handler.characters(text.decode("utf-8"))
            self.__indent += 1
            # Print formating
            if len(children) > 0:
                self._cont_handler.ignorableWhitespace('\n')
            for child in children:
                self.__parse(child)
            self.__indent -= 1
            # Print formating
            if len(children) > 0:
                self._cont_handler.ignorableWhitespace(" " * self.__indent * 4)
            self._cont_handler.endElement(name)
            # Print formating
            self._cont_handler.ignorableWhitespace('\n')

# ------------------------------------------------------------------------------
# Class to serialize python dictionaries to xml contents.
# ------------------------------------------------------------------------------
class XmlSerializer(object):
    """Class to serialize python dictionaries to xml contents.
    """

    # --------------------------------------------------------------------------
    # Get the last traceback.
    # --------------------------------------------------------------------------
    def getLastTraceback():
        """Get the last traceback.
        @return: A string.
        """
        global LAST_TRACE_BACK
        return LAST_TRACE_BACK

    # --------------------------------------------------------------------------
    # Deserialize a xml file to a dictionary.
    # --------------------------------------------------------------------------
    def deserialize(xmlFileName):
        """Deserialize a xml file to a dictionary.
        @param xmlFileName: Input xml file.
        @return: The resulting dictionary.
        """
        def setLastTraceback():
            global LAST_TRACE_BACK
            fList = traceback.format_exception(sys.exc_info()[0],
                        sys.exc_info()[1],
                        sys.exc_info()[2])
            LAST_TRACE_BACK = ""
            for line in fList:
                LAST_TRACE_BACK += line
        def reinitLastTraceback():
            global LAST_TRACE_BACK
            LAST_TRACE_BACK = "No error"
        # Get the xml encoding
        encoding = "utf-8"
        try:
            f = open(xmlFileName, 'rb')
            try:
                lines = f.read().split("\n")
                for line in lines:
                    line = line.strip().lower()
                    if line.find("<?xml ") == 0:
                        if line.find("encoding") != -1:
                            encoding = line[line.find("encoding"):].split('"')[1]
            finally:
                f.close()
                reinitLastTraceback()
        except:
            setLastTraceback()
            return None
        try:
            parser = make_parser()
            dictionaryHandler = DictionaryHandler(encoding)
            parser.setContentHandler(dictionaryHandler)
            parser.parse(open(xmlFileName))
            reinitLastTraceback()
            return dictionaryHandler.getDictionary()
        except:
            setLastTraceback()
            return None

    # --------------------------------------------------------------------------
    # Deserialize a xml file to a dictionary. (Simpless dictionary srtucture)
    # --------------------------------------------------------------------------
    def deserializeEx(xmlFileName):
        """Deserialize a xml file to a dictionary.
        (Simpless dictionary srtucture)
        @param xmlFileName: Input xml file.
        @return: The resulting dictionary.
        This function is more usefull than the "deserialize" one, because the
        structure is less complexe. But the resulting xml can't be re-serialized
        """
        dictionary = XmlSerializer.deserialize(xmlFileName)
        if dictionary == None:
            return None
        def recNodes(nodeDict):
            result = {}
            attributes = nodeDict[0]
            text = nodeDict[1]
            children = nodeDict[2]
            # Check for attributes
            for attributeName in attributes.keys():
                result[attributeName] = attributes[attributeName]
            # Check for text
            if text != '':
                return text
            # Check for children
            i = 0
            for child in children:
                for childName in child.keys():
                    i += 1
                    if result.has_key(childName):
                        nodeName = "%s|%d" % (childName, i)
                    else:
                        nodeName = childName
                    result[nodeName] = recNodes(child[childName])
            return result
        for key in dictionary.keys():
            return recNodes(dictionary[key])

    # --------------------------------------------------------------------------
    # Serialize a dictionary to a xml content.
    # --------------------------------------------------------------------------
    def serialize(dictionary):
        """Serialize a dictionary to a xml content.
        @param dictionary: Dictionary to serialize.
        @return: The resulting xml content.
        """
        stringContent = cStringIO.StringIO()
        try:
            parser = XmlDictionaryParser()
            parser.setContentHandler(XMLGenerator(stringContent, "utf-8"))
            parser.parse(dictionary)
        except:
            return None
        return stringContent.getvalue()

    deserialize = staticmethod(deserialize)
    deserializeEx = staticmethod(deserializeEx)
    serialize = staticmethod(serialize)
    getLastTraceback = staticmethod(getLastTraceback)
