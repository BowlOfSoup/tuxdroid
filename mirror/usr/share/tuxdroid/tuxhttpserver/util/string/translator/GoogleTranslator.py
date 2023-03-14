#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import sys
import urllib
import urllib2

from util.string.textfilter.chardet.chardet import detect
from util.misc.URLTools import URLCheckConnection

# ------------------------------------------------------------------------------
# Class to translate texts with google translator.
# ------------------------------------------------------------------------------
class GoogleTranslator(object):
    """Class to translate texts with google translator.
    """

    # --------------------------------------------------------------------------
    # Translate a text.
    # --------------------------------------------------------------------------
    def translate(fromLang, toLang, text):
        """Translate a text.
        @param fromLang: Language of the original text.
        @param toLang: Language of the translated text.
        @param text: 'utf-8' text to translate.
        @return: The translated text in or empty string if fail.
        """
        if not URLCheckConnection():
            return ""
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'translate.py/0.1')]
        s = ""
        try:
            o = opener.open(
                "http://translate.google.com/translate_t?" +
                urllib.urlencode({'langpair' : '%s|%s' % (fromLang, toLang)}),
                data = urllib.urlencode({'ie' : 'UTF8',
                                         'oe' : 'UTF8',
                                         'text': text})
            )
            try:
                s = o.read()
            except:
                pass
        finally:
            o.close()
        if s == "":
            return ""
        idx_b = s.find('id=result_box') + 24
        idx_e = s[idx_b:].find('</div>') + idx_b
        trad = s[idx_b:idx_e]
        if len(trad) > 0:
            return trad.decode("utf-8")
        else:
            return ""

    translate = staticmethod(translate)
