# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import sys

# ------------------------------------------------------------------------------
# Helper class.
# ------------------------------------------------------------------------------
class Helper(object):
    """Helper class.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        self.__elementsList = []
        aElementsList = dir(Helper)
        oElementsList = dir(self)
        self.__elementsList.append(["__init__", "Constructor"])
        for element in oElementsList:
            if element in aElementsList:
                if element.find("_") == 0:
                    continue
            if element.find("__") == -1:
                if str(type(getattr(self, element))) != "<type 'instancemethod'>":
                    self.__elementsList.append([element, "Object"])
        for element in oElementsList:
            if element in aElementsList:
                if element.find("_") == 0:
                    continue
            if element.find("__") == -1:
                if str(type(getattr(self, element))) == "<type 'instancemethod'>":
                    self.__elementsList.append([element, "Method"])

    # --------------------------------------------------------------------------
    # Show a string list. Formated for the console.
    # --------------------------------------------------------------------------
    def _showStringList(self, header, list):
        """Show a string list. Formated for the console.
        @param header: String header.
        @param list: String list to show.
        """
        print ""
        print header
        print "".join("=" * len(header))
        for i, st in enumerate(list):
            # Try to encode the string
            try:
                st = st.decode("utf-8")
                st = st.encode(sys.stdin.encoding, 'replace')
            except:
                pass
            print "  %.2d : %s" % (i, st)
        print ""

    # --------------------------------------------------------------------------
    # Show the help of this class.
    # --------------------------------------------------------------------------
    def help(self, id = None):
        """Show the help of this class.
        @param id: Help element id.
        """
        if id == None:
            myList = []
            for element in self.__elementsList:
                myList.append("%s : %s" % (element[1], element[0]))
            self._showStringList("Elements list of this class :",
                myList)
        else:
            myList = []
            for element in self.__elementsList:
                myList.append(element[0])
            method = None
            if str(type(id)) == "<type 'int'>":
                if id in range(len(myList)):
                    method = myList[id]
            elif str(type(id)) == "<type 'str'>":
                if id in myList:
                    method = id
            if method != None:
                print ""
                hString = "%s.%s" % (str(self.__class__).split("'")[1],
                    method)
                print hString
                print "".join("=" * len(hString))
                print getattr(self, method).__doc__
                print ""
