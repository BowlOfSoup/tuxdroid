# -*- coding: utf-8 -*-

"""
LibTuxOSL
=========

    LibTuxOSL is a wrapper to the shared library "libtuxosl.so".
    
    http://www.tuxisalive.com
"""

import version
__name__ = version.name
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

#
# LibTuxOSL package modules
#
from util.osl.TuxOSL import *