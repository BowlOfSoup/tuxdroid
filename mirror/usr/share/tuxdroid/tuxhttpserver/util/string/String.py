#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os
import sys

from util.system.Clipboard import Clipboard
from translator.GoogleTranslator import GoogleTranslator
from textfilter.chardet.chardet import detect
from languagefinder.LanguageFinder import LanguageFinder
from textfilter.TextFilter import TextFilterContainer

# ------------------------------------------------------------------------------
# Utilities for string data.
# ------------------------------------------------------------------------------
class String(object):
    """Utilities for string data.
    """

    __languageFinder = LanguageFinder()
    __languageFinder.load()
    __textFilter = TextFilterContainer()
    __textFilter.load_directory(os.path.join(os.path.split(__file__)[0],
            'filters'))

    # --------------------------------------------------------------------------
    # Force the text encoding to 'utf-8'.
    # --------------------------------------------------------------------------
    def toUtf8(text, detectConsole = False):
        """Force the text encoding to 'utf-8'.
        @param text: Input text in any encoding.
        @return: The 'utf-8' text.
        """
        encoding = detect(text)['encoding']
        if detectConsole:
            if text.decode(sys.stdin.encoding) != text.decode(encoding):
                encoding = sys.stdin.encoding
        text = text.decode(encoding)
        text = text.encode('utf-8', 'replace')
        return text

    # --------------------------------------------------------------------------
    # Check if the text is encoded in 'utf-8'.
    # --------------------------------------------------------------------------
    def isUtf8(text):
        """Check if the text is encoded in 'utf-8'.
        @param text: Input text to check.
        @return: A boolean.
        """
        encoding = detect(text)['encoding']
        if encoding.lower() in ["utf8", "utf-8"]:
            return True
        else:
            return False

    # --------------------------------------------------------------------------
    # Translate a text.
    # --------------------------------------------------------------------------
    def translate(text, fromLang, toLang, inConsole = False):
        """Translate a text.
        @param text: Text to translate.
        @param fromLang: Language of the original text.
        @param toLang: Language of the translated text.
        @param inConsole: If the text will be showed in the console.
        @return: The translated text in or empty string if fail.
            - If the text must be showed in the console, the output string is
              reencoded in the console encoding, otherwise it is encoded in
              'utf-8'.
        """
        text = String.toUtf8(text, inConsole)
        text =  GoogleTranslator.translate(fromLang, toLang, text)
        text = String.__textFilter.apply(text, "ALL")
        if inConsole:
            text = text.encode(sys.stdin.encoding, 'ignore')
        else:
            text = text.encode('utf-8', 'replace')
        return text

    # --------------------------------------------------------------------------
    # Translate a text with auto-detection of the input text language.
    # --------------------------------------------------------------------------
    def autoTranslate(text, toLang, inConsole = False):
        """Translate a text with auto-detection of the input text language.
        @param text: Text to translate.
        @param toLang: Language of the translated text.
        @param inConsole: If the text will be showed in the console.
        @return: The translated text in or empty string if fail.
            - If the text must be showed in the console, the output string is
              reencoded in the console encoding, otherwise it is encoded in
              'utf-8'.
        """
        text = String.toUtf8(text, inConsole)
        fromLang = String.getLanguage(text)
        text =  GoogleTranslator.translate(fromLang, toLang, text)
        text = String.__textFilter.apply(text, "ALL")
        if inConsole:
            text = text.encode(sys.stdin.encoding, 'ignore')
        else:
            text = text.encode('utf-8', 'replace')
        return text

    # --------------------------------------------------------------------------
    # Find the language of a text.
    # --------------------------------------------------------------------------
    def getLanguage(text, default = "en_US"):
        """Find the language of a text.
        @param text: Input text.
        @param default: Default returned language if the function can't retrieve
            the text language.
        @return: The text language.
        """
        return String.__languageFinder.findLanguage(text, default)

    # --------------------------------------------------------------------------
    # Get the last copied text in the clipboard.
    # --------------------------------------------------------------------------
    def getClipboardText(inConsole = False):
        """Get the last copied text in the clipboard.
        @return: A string.
        """
        text = Clipboard.getText()
        text = text.decode(detect(text)['encoding'])
        text = String.__textFilter.apply(text, "ALL")
        text = text.replace("??", " ")
        text = text.replace("? ? ?", " ")
        text = text.replace("? ?", " ")
        text = text.replace('\r', "")
        text = text.replace(u'\xa0', "")
        text = text.replace('*', ".")
        text = text.replace('#', "")
        while text.find(". .") != -1:
            text = text.replace(". .", ".")
        for tag in ['html', 'head', 'body', 'table', 'td', 'tr', 'input', 'img',
            'a', 'span', 'div', 'xsl', 'link',]:
            while True:
                idxb = text.lower().find("<" + tag)
                if idxb == -1:
                    break
                idxe = text.lower().find(tag + ">")
                if idxe == -1:
                    break
                delText = text[idxb:idxe + len(tag) + 1]
                text = text.replace(delText, "")
        while text.find("\n\n") != -1:
            text = text.replace("\n\n", "\n")
        while text.find("\r\r") != -1:
            text = text.replace("\r\r", "\r")
        if inConsole:
            text = text.encode(sys.stdin.encoding, 'ignore')
        else:
            text = text.encode('utf-8', 'replace')
        return text

    # --------------------------------------------------------------------------
    # Get the last copied text in the clipboard, translated with language
    # auto-detection.
    # --------------------------------------------------------------------------
    def getTranslatedClipboardText(toLang, inConsole = False):
        """Get the last copied text in the clipboard, translated with language
        auto-detection.
        @param toLang: Language of the translated text.
        @param inConsole: If the text will be showed in the console.
        @return: A string.
        """
        text = String.getClipboardText()
        fromLang = String.getLanguage(text)
        text =  GoogleTranslator.translate(fromLang, toLang, text)
        text = String.__textFilter.apply(text, "ALL")
        if inConsole:
            text = text.encode(sys.stdin.encoding, 'ignore')
        else:
            text = text.encode('utf-8', 'replace')
        return text

    toUtf8 = staticmethod(toUtf8)
    isUtf8 = staticmethod(isUtf8)
    translate = staticmethod(translate)
    autoTranslate = staticmethod(autoTranslate)
    getLanguage = staticmethod(getLanguage)
    getClipboardText = staticmethod(getClipboardText)
    getTranslatedClipboardText = staticmethod(getTranslatedClipboardText)
