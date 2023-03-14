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

from base.lib.Helper import Helper
from base.ApiBase import *
from tuxdroid.const.ConstTuxDriver import *
from tuxdroid.const.ConstTuxOsl import *
from tuxdroid.MouthEyes import MouthEyes
from tuxdroid.TTS import TTS
from tuxdroid.Wav import Wav
from tuxdroid.Attitune import Attitune
from tuxdroid.RawCommand import RawCommand
from tuxdroid.DongleRadio import DongleRadio
from tuxdroid.SoundFlash import SoundFlash
from tuxdroid.Led import Led
from tuxdroid.Button import Button
from tuxdroid.Flippers import Flippers
from tuxdroid.Spinning import Spinning
from tuxdroid.Light import Light
from tuxdroid.Battery import Battery
from tuxdroid.Charger import Charger

# ------------------------------------------------------------------------------
# Tux Droid API.
# ------------------------------------------------------------------------------
class TuxAPI(ApiBase):
    """Main module class to control Tuxdroid.
    """
    # --------------------------------------------------------------------------
    # Constructor of the class.
    # --------------------------------------------------------------------------
    def __init__(self, host = '127.0.0.1', port = 270):
        """Constructor of the class.
        @param host: host of the server.
        @param port: port of the server.
        """
        ApiBase.__init__(self, host, port)
        # Register base status/events of the server
        for statusName in SW_NAME_DRIVER:
            self.getEventsHandler().insert(statusName)
        for statusName in SW_NAME_OSL:
            self.getEventsHandler().insert(statusName)
        # Create the mouth object
        self.mouth = MouthEyes(self, self.server, ST_NAME_MOUTH_POSITION,
            ST_NAME_MOUTH_RM, "mouth")
        # Create the eyes object
        self.eyes = MouthEyes(self, self.server, ST_NAME_EYES_POSITION,
            ST_NAME_EYES_RM, "eyes")
        # Create the tts object
        self.tts = TTS(self, self.server)
        # Create the wav object
        self.wav = Wav(self, self.server)
        # Create the attitune object
        self.attitune = Attitune(self, self.server)
        # Create the raw command object
        self.raw = RawCommand(self, self.server)
        # Create the dongle object
        self.dongle = DongleRadio(self, self.server, ST_NAME_DONGLE_PLUG)
        # Create the radio object
        self.radio = DongleRadio(self, self.server, ST_NAME_RADIO_STATE)
        # Create the sound flash object
        self.soundFlash = SoundFlash(self, self.server)
        # Create led objects
        self.led = Led(self, self.server)
        # Create the button objects
        self.button = Button(self, self.server)
        # Create the flippers object
        self.flippers = Flippers(self, self.server)
        # Create the spinning object
        self.spinning = Spinning(self, self.server)
        # Create the light object
        self.light = Light(self, self.server)
        # Create the battery object
        self.battery = Battery(self, self.server)
        # Create the charger object
        self.charger = Charger(self, self.server)
        # Initialize the helper
        Helper.__init__(self)

    # --------------------------------------------------------------------------
    # Get the version of this API.
    # --------------------------------------------------------------------------
    def getVersion(self):
        """Get the version of this api.
        @return: A string.
        """
        return "tuxisalive.api-%s" % __version__

    # --------------------------------------------------------------------------
    # Get the Tux Droid system versions.
    # --------------------------------------------------------------------------
    def getVersions(self):
        """Get the Tux Droid system versions.
        @return: a dictionary.
        """
        verDict = {}
        verDict["tuxapi"] = __version__
        verDict["tuxdroidserver"] = self.server.getVersion()
        ver = self.server._requestOne(ST_NAME_DRIVER_SYMB_VER)
        if ver == None:
            verDict["tuxdriver"] = "Unknow"
        else:
            verDict["tuxdriver"] = ver[ver.find("_") + 1:]
        ver = self.server._requestOne(ST_NAME_OSL_SYMB_VER)
        if ver == None:
            verDict["tuxosl"] = "Unknow"
        else:
            verDict["tuxosl"] = ver[ver.find("_") + 1:]
        return verDict

    # --------------------------------------------------------------------------
    # Show the Tux Droid system versions.
    # --------------------------------------------------------------------------
    def showVersions(self):
        """Show the Tux Droid system versions.
        """
        verDict = self.getVersions()
        result = []
        for key in verDict.keys():
            result.append("%s : %s" % (key, verDict[key]))
        self._showStringList("Tux Droid System :", result)
