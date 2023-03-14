# -*- coding: utf-8 -*-

"""
daemonizer
==========

    Simple daemonizer for python.

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
# daemonizer package modules
#
from util.daemonizer.Daemonizer import *