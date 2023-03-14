# -*- coding: latin1 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

TDS_CLIENT_LEVEL_ANONYMOUS      = -1
TDS_CLIENT_LEVEL_FREE           = 0
TDS_CLIENT_LEVEL_RESTRICTED     = 1
TDS_CLIENT_LEVEL_ROOT           = 2

TDS_CLIENT_LEVEL_NAMES = [
    "ANONYMOUS",
    "FREE",
    "RESTRICTED",
    "ROOT",
]

def getClientLevelName(clientLevel):
    if (clientLevel >= -1) and (clientLevel <= 2):
        return TDS_CLIENT_LEVEL_NAMES[clientLevel + 1]
    else:
        return None

def checkClientLevel(clientLevel, minimalLevel):
    return (clientLevel >= minimalLevel)

