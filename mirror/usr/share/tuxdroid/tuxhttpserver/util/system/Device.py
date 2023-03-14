#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

import os

# ------------------------------------------------------------------------------
# Class to get some information about smart-compagnon audio/video devices.
# ------------------------------------------------------------------------------
class Device(object):
    """Class to get some information about smart-compagnon audio/video devices.
    """

    # --------------------------------------------------------------------------
    # Get a sound device by a keyword. Win32.
    # --------------------------------------------------------------------------
    def getSoundDeviceByKeywordWin32(deviceKeyword):
        """Get a sound device by a keyword.
        @param deviceKeyword: Device keyword.
        @return: A tuple (device index, device name)
        """
        import win32com.directsound.directsound as ds
        devices = ds.DirectSoundEnumerate()
        for i, device in enumerate(devices):
            deviceName = device[1]
            if deviceName.lower().find(deviceKeyword.lower()) != -1:
                return i, deviceName
        return -1, None

    # --------------------------------------------------------------------------
    # Get the sound device name of Tux Droid Audio.
    # --------------------------------------------------------------------------
    def getSoundDeviceNameTuxdroidAudio():
        """Get the sound device name of Tux Droid Audio.
        @return: The device name or None (Win32) if not found.
        """
        if os.name == "nt":
            idx, deviceName = Device.getSoundDeviceByKeywordWin32("tuxdroid-audio")
            return deviceName
        else:
            return "plughw:TuxDroid,0"

    # --------------------------------------------------------------------------
    # Get the sound device name of Tux Droid TTS.
    # --------------------------------------------------------------------------
    def getSoundDeviceNameTuxdroidTts():
        """Get the sound device name of Tux Droid Tts.
        @return: The device name or None (Win32) if not found.
        """
        if os.name == "nt":
            idx, deviceName = Device.getSoundDeviceByKeywordWin32("tuxdroid-tts")
            return deviceName
        else:
            return "plughw:TuxDroid,1"

    # --------------------------------------------------------------------------
    # Get the sound device name of Tux Droid Micro.
    # --------------------------------------------------------------------------
    def getSoundDeviceNameTuxdroidMicro():
        """Get the sound device name of Tux Droid Micro.
        @return: The device name or None (Win32) if not found.
        """
        if os.name == "nt":
            from ctypes import windll
            winmm = windll.winmm
            wvcps = ' ' * 52
            cardsCount = winmm.waveInGetNumDevs()
            for i in range(cardsCount):
                try:
                    if winmm.waveInGetDevCapsA(i, wvcps,len(wvcps)) == 0:
                        deviceName = wvcps[8:].split("\0")[0]
                        if wvcps.lower().find("tuxdroid-audio") != -1:
                            return deviceName
                except:
                    pass
            return None
        else:
            return "plughw:TuxDroid,0"

    # --------------------------------------------------------------------------
    # Get the sound device of Tux Droid.
    # --------------------------------------------------------------------------
    def getTuxDroidSoundDevice():
        """Get the sound device of Tux Droid.
        @return: A string.
        """
        if os.name == 'nt':
            idx, deviceName = Device.getSoundDeviceByKeywordWin32("tuxdroid-audio")
            if idx == -1:
                return "dsound:device=1"
            else:
                return "dsound:device=%d" % idx
        else:
            return "alsa:device=plughw=TuxDroid,0"

    getSoundDeviceByKeywordWin32 = staticmethod(getSoundDeviceByKeywordWin32)
    getSoundDeviceNameTuxdroidAudio = staticmethod(getSoundDeviceNameTuxdroidAudio)
    getSoundDeviceNameTuxdroidTts = staticmethod(getSoundDeviceNameTuxdroidTts)
    getSoundDeviceNameTuxdroidMicro = staticmethod(getSoundDeviceNameTuxdroidMicro)
    getTuxDroidSoundDevice = staticmethod(getTuxDroidSoundDevice)
