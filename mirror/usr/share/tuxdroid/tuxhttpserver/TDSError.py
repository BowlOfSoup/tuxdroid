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

E_TDREST_BEGIN                  = 255
E_TDREST_SUCCESS                = 0
E_TDREST_FAILED                 = E_TDREST_BEGIN
E_TDREST_ACCESSDENIED           = E_TDREST_BEGIN + 1
E_TDREST_INVALIDPARAMETERS      = E_TDREST_BEGIN + 2

def getStrError(errorCode):
    if errorCode == E_TDREST_SUCCESS:
        return "Success"
    elif errorCode == E_TDREST_FAILED:
        return "Failed"
    elif errorCode == E_TDREST_ACCESSDENIED:
        return "Access denied"
    elif errorCode == E_TDREST_INVALIDPARAMETERS:
        return "Invalid parameters"
    else:
        return "Unexpected error"