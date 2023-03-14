# -*- coding: utf-8 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 Acness World
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import xml.dom.minidom
from xml.dom.minidom import Node
import os

# ==============================================================================
# Public functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Create the content of a XML file from a python structure.
# ------------------------------------------------------------------------------
def toXML(structure, stylesheetFile = None):
    """Create the content of a XML file from a python structure.
    @param structure: Python structure to write.
    @param stylesheetFile: Stylesheet file path to include in the xml file.
                           (Default None)
    @return: The success of the XML file write.
    """
    # Check if structure is valid
    if str(type(structure)) != "<type 'dict'>":
        raise TypeError, "structure MUST be a dictionary"
    # Create the XML string
    return __structToXML(structure, stylesheetFile)

# ------------------------------------------------------------------------------
# Read the content of a XML file to a python structure.
# ------------------------------------------------------------------------------
def fromXML(xmlFile):
    """Read the content of a XML file to a python structure.
    @param xmlFile: XML file to read.
    @return: A python dictionary or None.
    """
    # Check if xmlFile exists
    if not os.path.isfile(xmlFile):
        errText = "%s file not found" % xmlFile
        raise IOError, errText
    # Retrieve the structure from the XML
    ret, structure = __xmlToStruct(xmlFile)
    if ret:
        return structure
    else:
        return None

# ==============================================================================
# Private functions
# ==============================================================================

# ------------------------------------------------------------------------------
# Insert a leaf in a xml structure.
# ------------------------------------------------------------------------------
def __insertLeaf(parentNode, textID, textValue):
    """Insert a leaf in a xml structure.
    """
    if textID.find("|") != -1:
        textID = textID[:textID.find("|")]
    xmlObj = xml.dom.minidom.Document()
    leafNode = xmlObj.createElement(textID)
    typeStr = str(type(textValue)).replace("<type '", '')
    typeStr = typeStr.replace("'>", '')
    if typeStr == 'str':
        if textValue == "":
            textValue = " "
    leafNode.setAttribute('type', typeStr)
    text = xmlObj.createTextNode(str(textValue))
    leafNode.appendChild(text)
    parentNode.appendChild(leafNode)

# ------------------------------------------------------------------------------
# Insert a node in a xml structure.
# ------------------------------------------------------------------------------
def __insertNode(parentNode, nodeID):
    """Insert a node in a xml structure
    """
    if nodeID.find("|") != -1:
        nodeID = nodeID[:nodeID.find("|")]
    xmlObj = xml.dom.minidom.Document()
    newNode = xmlObj.createElement(nodeID)
    parentNode.appendChild(newNode)
    return newNode

# ------------------------------------------------------------------------------
# Write a xml file from a dict structure.
# ------------------------------------------------------------------------------
def __structToXML(struct, xslPath = None):
    """Write a xml file from a dict structure.
    """
    xmlObj = xml.dom.minidom.Document()

    if xslPath != None:
        strD = "type=\"text/xsl\" href=\"%s\"" % xslPath
        xslObj = xmlObj.createProcessingInstruction("xml-stylesheet", strD)
        xmlObj.appendChild(xslObj)

    def nodeStructToNXML(parentNode, nodeStruct):
        keys = nodeStruct.keys()
        keys.sort()
        for key in keys:
            if str(type(nodeStruct[key])) <> "<type 'dict'>":
                __insertLeaf(parentNode,  key, nodeStruct[key])
            else:
                newNode = __insertNode(parentNode, key)
                nodeStructToNXML(newNode, nodeStruct[key])

    nodeStructToNXML(xmlObj, struct)

    result = xmlObj.toxml()
    xmlObj.unlink()
    del(xmlObj)

    return result

# ------------------------------------------------------------------------------
# Get a dict structure from a xml file.
# ------------------------------------------------------------------------------
def __xmlToStruct(xml_path):
    """Get a dict structure from a xml file.
    """
    struct = {}
    def nodeXMLToStruct(parentNode, nodeStruct):
        for childNode in parentNode.childNodes:
            if childNode.nodeValue == None:
                it = parentNode.getElementsByTagName(childNode.localName)
                try:
                    t = len(it[0].childNodes)
                except:
                    name = childNode.localName.encode('utf-8','replace')
                    nDict = ''
                    nodeStruct[name] = nDict
                    continue
                if len(it[0].childNodes) > 0:
                    value = it[0].childNodes[0].nodeValue
                else:
                    value = ''
                typeVal = it[0].getAttribute('type')
                name = childNode.localName
                if it[0].getAttribute('type') != '':
                    leafName = name.encode('utf-8','replace')
                    value = value.encode('utf-8','replace')
                    if typeVal != 'str':
                        value = eval(value)
                    nodeStruct[leafName] = value
                else:
                    name = name.encode('utf-8','replace')
                    nDict = {}
                    nodeStruct[name] = nDict
                    nodeXMLToStruct(it[0], nodeStruct[name])

    try:
        fXML = open(xml_path, 'rb')
    except IOError:
        return False, struct
    xmlStr = fXML.read()
    fXML.close()
    xmlObj = xml.dom.minidom.parseString(xmlStr)
    nodeXMLToStruct(xmlObj, struct)
    xmlObj.unlink()
    del(xmlObj)
    return True, struct
