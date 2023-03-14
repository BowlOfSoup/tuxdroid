#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

from util.i18n.I18n import I18n

# Default list of the supported language.
SUPPORTED_LANGUAGES_LIST = ["en", "fr", "nl", "es", "it", "pt", "ar", "da",
    "de", "no", "sv",]

class Translation(object):
    """
    """

    def __init__(self, name):
        """
        """
        self.__i18nList = {}
        self.__updateI18nList(name)

    def __updateI18nList(self, name):
        """
        """
        mPath, mFile = os.path.split(__file__)
        fullPath = os.path.join(mPath, name)
        self.__i18nList = {}
        for language in SUPPORTED_LANGUAGES_LIST:
            i18n = I18n()
            i18n.setPoDirectory(fullPath)
            i18n.setLocale(language)
            i18n.update()
            if i18n.getDictionnary() == {}:
                self.__i18nList[language] = self.__i18nList["en"]
            else:
                self.__i18nList[language] = i18n

    def addPoDirectory(self, directory):
        """
        """
        if not os.path.isdir(directory):
            return
        for language in SUPPORTED_LANGUAGES_LIST:
            if not self.__i18nList.has_key(language):
                i18n = I18n()
                i18n.setPoDirectory(directory)
                i18n.setLocale(language)
                i18n.update()
                if i18n.getDictionnary() == {}:
                    self.__i18nList[language] = self.__i18nList["en"]
                else:
                    self.__i18nList[language] = i18n
            else:
                i18n = self.__i18nList[language]
                i18n.setPoDirectory(directory)
                i18n.setLocale(language)
                i18n.update()

    def getTranslations(self, language):
        """
        """
        if not self.__i18nList.has_key(language):
            language = "en"
        return self.__i18nList[language].getDictionnary()

    def fixeWordsInText(self, text, language):
        """
        """
        translations = self.getTranslations(language)
        splitedText = text.lower().split(" ")
        fixedText = ""
        for i, word in enumerate(splitedText):
            if translations.has_key(word):
                splitedText[i] = translations[word]
            fixedText += splitedText[i] + " "
        return fixedText

    def getMsgIDList(self):
        """
        """
        return self.__i18nList.keys()
