# -*- coding: latin1 -*-

"""
Api
===

    Python package for playing with Tuxdroid.

    http://www.tuxisalive.com

Using
=====

    Just write in Python

    >>> from tuxisalive.api import *
    >>> tux = TuxAPI('127.0.0.1', 270)
    >>> tux.server.autoConnect(CLIENT_LEVEL_RESTRICTED, 'MyAppName', 'myPassword')
    >>> tux.server.waitConnected(10.0)
    >>> tux.dongle.waitConnected(10.0)
    >>> tux.radio.waitConnected(10.0)
    >>> if tux.access.waitAcquire(10.0, ACCESS_PRIORITY_NORMAL):
    >>>     tux.attitune.load("http://www.tuxisalive.com/Members/remi/hammer.att")
    >>>     tux.attitune.play()
    >>>     time.sleep(10.0)
    >>>     tux.attitune.stop()
    >>>     tux.access.release()
    >>> ...
    >>> tux.server.disconnect()
    >>> tux.destroy()

"""

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

#
# Api package modules
#
from tuxisalive.api.TuxAPI import *
