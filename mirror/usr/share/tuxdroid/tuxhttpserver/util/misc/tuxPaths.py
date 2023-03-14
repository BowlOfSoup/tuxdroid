# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

TUXDROID_BASE_PATH = None
TUXDROID_LANGUAGE = None
TUXDROID_DEFAULT_LOCUTOR = None
TUXDROID_LANGUAGE2 = None
TUXDROID_SECOND_LOCUTOR = None
USER_BASE_PATH = None

def __getLocutorFromIsoLang(isoLang):
    """Get the locutor for an iso lang.
    """
    if isoLang == "ar":
        return "Salma8k"
    elif isoLang == "en_GB":
        return "Graham8k"
    elif isoLang == "da":
        return "Mette8k"
    elif isoLang == "nl":
        return "Femke8k"
    elif isoLang == "de":
        return "Klaus8k"
    elif isoLang == "no":
        return "Kari8k"
    elif isoLang == "pt":
        return "Celia8k"
    elif isoLang == "sv":
        return "Erik8k"
    elif isoLang == "fr":
        return "Bruno8k"
    elif isoLang == "en_US":
        return "Ryan8k"
    elif isoLang == "nl_BE":
        return "Sofie8k"
    elif isoLang == "it":
        return "Chiara8k"
    elif isoLang == "es":
        return "Maria8k"
    else:
        return "Ryan8k"

def __fillDefaultLocutor(isoLang):
    """Fill the default locutor for a iso lang.
    """
    global TUXDROID_DEFAULT_LOCUTOR
    TUXDROID_DEFAULT_LOCUTOR = __getLocutorFromIsoLang(isoLang)

def __fillSecondLocutor(isoLang):
    """Fill the default locutor for a iso lang.
    """
    global TUXDROID_SECOND_LOCUTOR
    TUXDROID_SECOND_LOCUTOR = __getLocutorFromIsoLang(isoLang)

if os.name == 'nt':
    from _winreg import *
    aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    aKey = OpenKey(aReg, r"SOFTWARE\Tux Droid\Installation")
    TUXDROID_BASE_PATH = QueryValueEx(aKey, "Install_Dir")[0]
    TUXDROID_LANGUAGE = QueryValueEx(aKey, "Language")[0]
    TUXDROID_LANGUAGE2 = QueryValueEx(aKey, "Language2")[0]
    CloseKey(aReg)
    __fillDefaultLocutor(TUXDROID_LANGUAGE)
    __fillSecondLocutor(TUXDROID_LANGUAGE2)
else:
    TUXDROID_LANGUAGE = "en_US"
    TUXDROID_LANGUAGE2 = "en_GB"
    __fillDefaultLocutor(TUXDROID_LANGUAGE)
    __fillSecondLocutor(TUXDROID_LANGUAGE2)
    if os.path.isfile("/etc/tuxdroid/tuxdroid.conf"):
        try:
            f = open("/etc/tuxdroid/tuxdroid.conf", 'rb')
            stream = f.read()
            lines = stream.split('\n')
            for line in lines:
                if line.find('PREFIX=') != -1:
                    prefix = line[7:]
                    TUXDROID_BASE_PATH = os.path.join(prefix, 'share/tuxdroid')
                # TODO first and second language
            f.close()
        except:
            TUXDROID_BASE_PATH = "/usr/share/tuxdroid"
USER_BASE_PATH = os.path.expanduser("~")
