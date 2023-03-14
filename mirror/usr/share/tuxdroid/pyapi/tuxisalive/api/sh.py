# -*- coding: latin1 -*-

"""
Tux shell
=========
Tux shell is the shell way to use Tuxdroid. It create an API object with the
"Free" client mode.
"""
import os
import time
if os.name == 'nt':
    from version import author, date, version, licence
else:
    from tuxisalive.api.version import author, date, version, licence

__author__ = author
__date__ = date
__version__ = version
__licence__ = licence

del author, date, version, licence

#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import sys
import signal
import atexit

if os.name == 'nt':
    from TuxAPI import *
else:
    from tuxisalive.api.TuxAPI import *

global tux

# Try to connect to the port 270
tux = TuxAPI("127.0.0.1", 270)
time.sleep(0.5)
# If the API is not connected to the port 270, then try the port 54321 (user
# mode)
if tux.server.connect(CLIENT_LEVEL_FREE, "TuxShell", "NoPasswd"):
    tux.server.disconnect()
else:
    tux = TuxAPI("127.0.0.1", 54321)

verString = tux.getVersion()
verH = "".join("=" * len(verString))
print verH
print verString
print verH

tux.server.autoConnect(CLIENT_LEVEL_FREE, "TuxShell", "NoPasswd")
tux.tts.isConsole()

def sigExit(signum, frame):
    sys.exit(signum)

def exit():
    tux.destroy()
    sys.exit(0)

def myExitFunct():
    tux.destroy()

signal.signal(signal.SIGTERM, sigExit)
signal.signal(signal.SIGINT, sigExit)
atexit.register(myExitFunct)
