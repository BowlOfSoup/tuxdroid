# -*- coding: latin1 -*-

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

from thomas.thomas import Bayes

# ------------------------------------------------------------------------------
# Class to get the language of a text string.
# ------------------------------------------------------------------------------
class LanguageFinder(object):
    """Class to get the language of a text string.
    """

    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self):
        """Constructor of the class.
        """
        self.__languageGuesser = Bayes()
        self.__isLoaded = False

    # --------------------------------------------------------------------------
    # Load the database.
    # --------------------------------------------------------------------------
    def load(self):
        """Load the database.
        """
        guesseFileName = os.path.join(os.path.split(__file__)[0],
            "language_guesser.bay")
        if os.path.isfile(guesseFileName):
            self.__languageGuesser.load(guesseFileName)
            self.__isLoaded = True
            return True
        else:
            self.__isLoaded = False
            return False

    # --------------------------------------------------------------------------
    # Find the language of a text.
    # --------------------------------------------------------------------------
    def findLanguage(self, text, default = 'en_US'):
        """Find the language of a text.
        @param text: Input text.
        @param default: Default returned language if the function can't retrieve
            the text language.
        @return: The text language.
        """
        if not self.__isLoaded:
            return default
        def normalizeText(text):
            text = text.lower()
            text = text.replace("'", " ")
            text = text.replace(".", " ")
            text = text.replace(",", " ")
            text = text.replace("!", " ")
            text = text.replace("?", " ")
            text = text.replace("\n", " ")
            text = text.replace('"', " ")
            text = text.replace("(", " ")
            text = text.replace(")", " ")
            text = text.replace("’", " ")
            text = text.replace("  ", " ")
            return text
        res = self.__languageGuesser.guess(normalizeText(text))
        if len(res) > 0:
            return res[0][0]
        else:
            return default
