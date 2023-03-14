#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html
#
#    This module is a portage of a module of "Karma-Lab Common Toolkits" a
#    java library written by "Yoran Brault" <http://artisan.karma-lab.net>
#

import os
import locale
import codecs

# ------------------------------------------------------------------------------
# Class to read and use i18n po files.
# ------------------------------------------------------------------------------
class I18n(object):
    """Class to read and use i18n po files.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        self.__locale = locale.getdefaultlocale()[0]
        if self.__locale == None:
            self.__locale = "en_US"
        self.__language = self.__locale.split("_")[0]
        self.__country = self.__locale.split("_")[1]
        self.__poDirectory = None
        self.__data = {}

    # --------------------------------------------------------------------------
    # Get the target po directory.
    # --------------------------------------------------------------------------
    def getPoDirectory(self):
        """Get the target po directory.
        @return: A directory path as string.
        """
        return self.__poDirectory

    # --------------------------------------------------------------------------
    # Set the target po directory.
    # --------------------------------------------------------------------------
    def setPoDirectory(self, poDirectory):
        """Set the target po directory.
        @param poDirectory: Path of the po directory.
        """
        self.__poDirectory = poDirectory

    # --------------------------------------------------------------------------
    # Get the used locale value.
    # --------------------------------------------------------------------------
    def getLocale(self):
        """Get the used locale value.
        @return: The locale as "<language>_<country>" string.
        """
        return self.__locale

    # --------------------------------------------------------------------------
    # Set the used locale value.
    # --------------------------------------------------------------------------
    def setLocale(self, locale):
        """Set the used locale value.
        @param locale: Locale to use. "<language>_<country>".
        """
        self.__language = locale.split("_")[0]
        if len(locale.split("_")) > 1:
            self.__country = locale.split("_")[1]
        else:
            self.__country = self.__language.upper()
        self.__locale = "%s_%s" % (self.__language, self.__country)

    # --------------------------------------------------------------------------
    # Get the translation dictionnary.
    # --------------------------------------------------------------------------
    def getDictionnary(self):
        """Get the translation dictionnary.
        @return: A dictionnary.
        """
        return self.__data

    # --------------------------------------------------------------------------
    # Translate a message.
    # --------------------------------------------------------------------------
    def tr(self, message, *arguments):
        """Translate a message.
        @param message: Message to translate.
        @param arguments: Arguments to pass in the formated message.
        example:
        >>>print i18n.tr("This is the {0} test of the module {1}.", 4, "i18n")
        """
        message = message.replace("\\'", "'")
        if self.__data.has_key(message):
            value = self.__data[message]
        else:
            value = message
        value = value.replace("'", "''")
        for i, argument in enumerate(arguments):
            trArg = str(argument)
            if self.__data.has_key(trArg):
                trArg = self.__data[trArg]
            value = value.replace("{%d}" % i, trArg)
        return value

    # --------------------------------------------------------------------------
    # Update the internal data dictionary with the current po dictionary and
    # locale.
    # --------------------------------------------------------------------------
    def update(self):
        """Update the internal data dictionary with the current po dictionary
        and locale.
        """
        def decodeUtf8Bom(text):
            if text[:3] == codecs.BOM_UTF8:
                text = text[3:]
            (output, consumed) = codecs.utf_8_decode(text, "ignore", True)
            return output

        fileName = "%s.po" % self.__language
        poFile = os.path.join(self.__poDirectory, fileName)
        if os.path.isfile(poFile):
            try:
                f = open(poFile, "rb")
                fileContent = f.read()
                try:
                    u = decodeUtf8Bom(fileContent)
                    fileContent = u.encode("utf-8", "ignore")
                except:
                    pass
                try:
                    msgId = None
                    msgStr = None
                    lines = fileContent.split("\n")
                    for line in lines:
                        if line.find("msgid") == 0:
                            msgId = self.__extractContent(line)
                        elif line.find("msgstr") == 0:
                            msgStr = self.__extractContent(line)
                            if msgId != None and msgStr != None:
                                if (len(msgId) > 0) and (len(msgStr) > 0):
                                    self.__data[msgId] = msgStr
                            msgId = None
                finally:
                    f.close()
            except:
                pass

    # --------------------------------------------------------------------------
    # Extract the content of a po line.
    # --------------------------------------------------------------------------
    def __extractContent(self, line):
        """Extract the content of a po line.
        @param line: Line to parse.
        @return: The extracted content.
        """
        idx = 0
        for i in range(len(line)):
            if line[i] != " ":
                break
            idx += 1
        line = line[idx:]
        idx = 0
        for i in range(len(line)):
            if line[i] == " ":
                break
            idx += 1
        line = line[idx:]
        idx = 0
        for i in range(len(line)):
            if line[i] != " ":
                break
            idx += 1
        line = line[idx:]
        line = line.replace("\\\"", "\"")
        l = len(line.split("\"")[-1]) + 1
        line = line[1:-l]
        return line
