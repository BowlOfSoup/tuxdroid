#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from util.osl import *

# ==============================================================================
# ******************************************************************************
# RESOURCE DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the resource "tuxosl".
# ==============================================================================
class TDSResourceTuxOSL(TDSResource):
    """Resource tuxosl class.
    """

    # ==========================================================================
    # Inherited methods from TDSResource
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Configure the resource.
    # --------------------------------------------------------------------------
    def configure(self):
        """Configure the resource.
        """
        # General configuration (inherited from ancestor)
        self.name = "tuxosl"
        self.comment = "Resource to handling the TuxOSL library."
        self.fileName = RESOURCE_FILENAME
        # Registering the TuxOSL statuses
        for statusName in SW_NAME_OSL:
            eventsHandler.insert(statusName)
        # Create and configure a Tux OSL object
        self.__tuxOSL = TuxOSL()
        self.__tuxOSL.SetLogLevel(TDS_CONF_LOG_LEVEL)
        self.__tuxOSL.SetStatusCallback(self.__onStatusCallback)
        # Others
        self.__oslMutex = threading.Lock()

    # --------------------------------------------------------------------------
    # Start the resource.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the resource.
        """
        eventsHandler.getEventHandler(ST_NAME_DONGLE_PLUG).register(self.__onDonglePlugCallback)
        eventsHandler.getEventHandler(ST_NAME_OSL_SOUND_STATE).register(self.__onSoundStateCallback)
        if resourceTuxDriver.getDonglePlugged():
            self.__onDonglePlugCallback(True, 0.0)

    # --------------------------------------------------------------------------
    # Stop the resource.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the resource.
        """
        self.__tuxOSL.Stop()

    # ==========================================================================
    # Private methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Event on status.
    # --------------------------------------------------------------------------
    def __onStatusCallback(self, status):
        """Event on status.
        @param status: The status.
        """
        # Parse the structure of the status
        statusStruct = self.__tuxOSL.GetStatusStruct(status)
        # Send the status/event to the events handler
        def async1():
            eventsHandler.emit(statusStruct['name'], (statusStruct['value'],
                float(statusStruct['delay'])))
        t = threading.Thread(target = async1)
        t.start()
        # Send the status/events to the clients manager
        def async2():
            clientsManager.pushEvents([statusStruct,])
        t = threading.Thread(target = async2)
        t.start()

    # --------------------------------------------------------------------------
    # Event on dongle plug/unplug.
    # --------------------------------------------------------------------------
    def __onDonglePlugCallback(self, value, delay):
        """Event on dongle plug/unplug.
        """
        def startTuxOsl():
            self.__tuxOSL.Start("Acapela")
            time.sleep(0.5)
            resourceTuxDriver.ledsBlink("LED_BOTH", 100, 0.5)
            self.__initializeStatesInEventsHandler()
            time.sleep(1.5)
            # Load first voice
            pitch = resourceUsers.getCurrentUserConfiguration()['pitch']
            firstLocutor = resourceUsers.getCurrentUserConfiguration()['locutor1']
            self.ttsSpeak(" ", firstLocutor, pitch)
            time.sleep(1.5)
            # Load second voice
            secondLocutor = resourceUsers.getCurrentUserConfiguration()['locutor2']
            self.ttsSpeak(" ", secondLocutor, pitch)
            time.sleep(1.5)
            # Reference locutors list
            resourcePluginsServer.getPluginsContainer().setLocutorsList(self.ttsVoicesList())
            # Play the opening attitune.
            resourceTuxDriver.ledsOn("LED_BOTH", 1.0)
            resourceAttituneManager.playAttitune("TuxBox Ready", 0.0)
            # Start the robot/content interactions
            resourceRobotContentInteractions.startMe()
        if value:
            t = threading.Thread(target = startTuxOsl)
            t.start()
        else:
            t = threading.Thread(target = self.stop)
            t.start()

    # --------------------------------------------------------------------------
    # Event on sound state changed.
    # --------------------------------------------------------------------------
    def __onSoundStateCallback(self, value, delay):
        """Event on sound state changed.
        """
        if value == "ON":
            resourceTuxDriver.setSoundChannel("TTS")
        else:
            resourceTuxDriver.setSoundChannel("GENERAL")

    # --------------------------------------------------------------------------
    # Reencode text from utf-8 to cp1252.
    # --------------------------------------------------------------------------
    def __reencodeText(self, text):
        """Reencode text from utf-8 to cp1252.
        @param text: Original text.
        @return: The reencoded text.
        """
        try:
            u = unicode(text, "utf-8")
            text = u.encode("cp1252", "replace")
        except:
            pass
        return text

    # --------------------------------------------------------------------------
    # Initialize statuses state in the events handler.
    # --------------------------------------------------------------------------
    def __initializeStatesInEventsHandler(self):
        """Initialize statuses state in the events handler.
        """
        def async():
            states = self.__tuxOSL.GetAllStatusState()
            if len(states) > 0:
                states = states[:-1]
            states = states.split('\n')
            for state in states:
                stateStruct = self.__tuxOSL.GetStatusStruct(state)
                if stateStruct['name'] != "None":
                    eventsHandler.updateState(stateStruct['name'], (
                        stateStruct['value'], float(stateStruct['delay'])))
        t = threading.Thread(target = async)
        t.start()

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Perform a speech.
    # --------------------------------------------------------------------------
    def ttsSpeak(self, text, locutor, pitch):
        """Perform a speech.
        @param text: Text to speak.
        @param locutor: Locutor voice.
        @param pitch: Pitch of the voice. <50..250>
        """
        text = self.__reencodeText(text)
        if locutor.find('8k') == -1:
            locutor += '8k'
        def async():
            self.__oslMutex.acquire()
            cmd = 'OSL_CMD:TTS:STOP'
            self.__tuxOSL.PerformCommand(0.0, cmd)
            cmd = 'OSL_CMD:TTS:SET_LOCUTOR:%s' % locutor
            self.__tuxOSL.PerformCommand(0.0, cmd)
            cmd = 'OSL_CMD:TTS:SET_PITCH:%d' % pitch
            self.__tuxOSL.PerformCommand(0.0, cmd)
            cmd = 'OSL_CMD:TTS:SPEAK:%s' % text
            self.__tuxOSL.PerformCommand(0.0, cmd)
            time.sleep(0.1)
            self.__oslMutex.release()
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Set if the current speech is paused or not.
    # --------------------------------------------------------------------------
    def ttsPause(self, value = 'True'):
        """Set if the current speech is paused or not.
        @param value: Pause value. <True|False> as string.
        """
        def async():
            cmd = 'OSL_CMD:TTS:SET_PAUSE:%s' % value
            self.__tuxOSL.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Stop the current performed speech.
    # --------------------------------------------------------------------------
    def ttsStop(self):
        """Stop the current performed speech.
        """
        def async():
            cmd = 'OSL_CMD:TTS:STOP'
            self.__tuxOSL.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Retrieve the locutors/voices list.
    # --------------------------------------------------------------------------
    def ttsVoicesList(self):
        """Retrieve the locutors/voices list.
        @return: The voices list.
        """
        result = eventsHandler.getEventHandler(ST_NAME_VOICE_LIST).getLastState()
        voices = []
        if result != None:
            tmpVoices = result[0][1:-1].split(',')
            for voice in tmpVoices:
                if len(voice) < 2:
                    continue
                voices.append(voice)
        return voices

    # --------------------------------------------------------------------------
    # Reencode the sentences included in a macro to "cp1252" if they are in
    # "utf-8".
    # --------------------------------------------------------------------------
    def reencodeTTSTextInMacro(self, macro):
        """Reencode the sentences included in a macro to "cp1252" if they are
        in "utf-8".
        @param macro: Macro text.
        @return: The reencoded macro.
        """
        spText = macro.split("\n")
        result = ""
        for cmd in spText:
            if cmd.find("OSL_CMD:TTS:SPEAK:") != -1:
                try:
                    u = unicode(cmd, "utf-8")
                    text = u.encode("cp1252", "replace")
                    cmd = text
                except:
                    pass
            result += cmd + "\n"
        return result

    # --------------------------------------------------------------------------
    # Play a wave file (8K - 8bit - Mono)
    # --------------------------------------------------------------------------
    def wavPlay(self, path, begin, end):
        """Play a wave file (8K - 8bit - Mono)
        @param path: Path of the wave file.
        @param begin: Beginning second.
        @param end: Ending second.
        @return: The used channel by TuxOSL or not.
        - The used channel is important when you wait for the end of wav playing.
        """
        if not resourceTuxDriver.getDonglePlugged():
            return None
        # Check the file extension
        if path.lower().rfind(".wav") == -1:
            return None
        # Create a cached file with the wav file
        cFile = filesCacheManager.createFileCache(path)
        # If the attitune can't be cached then FAIL
        if cFile == None:
            return None
        cmd = 'OSL_CMD:WAV:PLAY:%f,%f,%s' % (begin, end,
            cFile.getOutputFilePath())
        return self.__tuxOSL.PerformCommand(0.01, cmd)

    # --------------------------------------------------------------------------
    # Set if the current waves played is paused or not.
    # --------------------------------------------------------------------------
    def wavPause(self, value):
        """Set if the current waves played is paused or not.
        @param value: Pause value. <True|False> as string.
        """
        def async():
            cmd = 'OSL_CMD:WAV:SET_PAUSE:%s' % value
            self.__tuxOSL.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Stop the current played wave files.
    # --------------------------------------------------------------------------
    def wavStop(self):
        """Stop the current played wave files.
        """
        def async():
            self.__tuxOSL.PerformCommand(0.0, 'OSL_CMD:WAV:STOP')
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Clear all the current played wave files and performed speech.
    # --------------------------------------------------------------------------
    def clearAll(self):
        """Clear all the current played wave files and performed speech.
        """
        self.__tuxOSL.ClearCommandStack()
        self.__tuxOSL.PerformCommand(0.0, "OSL_CMD:TTS:STOP")
        self.__tuxOSL.PerformCommand(0.0, "OSL_CMD:WAV:STOP")

    # --------------------------------------------------------------------------
    # Execute a macro text.
    # --------------------------------------------------------------------------
    def executeMacro(self, macro):
        """Execute a macro text.
        @param macro: Macro text.
        """
        self.__tuxOSL.PerformMacroText(macro)

# Create an instance of the resource
resourceTuxOSL = TDSResourceTuxOSL("resourceTuxOSL")
# Register the resource into the resources manager
resourcesManager.addResource(resourceTuxOSL)
