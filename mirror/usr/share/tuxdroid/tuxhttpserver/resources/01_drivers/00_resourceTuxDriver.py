#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

from util.driver import *

# ==============================================================================
# ******************************************************************************
# RESOURCE DECLARATION
# ******************************************************************************
# ==============================================================================

# ==============================================================================
# Declaration of the resource "tuxdriver".
# ==============================================================================
class TDSResourceTuxDriver(TDSResource):
    """Resource tuxdriver class.
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
        self.name = "tuxdriver"
        self.comment = "Resource to handling the TuxDriver library."
        self.fileName = RESOURCE_FILENAME
        # Specific
        # Registering the Tuxdriver statuses
        for statusName in SW_NAME_DRIVER:
            eventsHandler.insert(statusName)
        # Registering the statuses which must be excluded by default by the
        # clients.
        clientsManager.addDefaultExcludedEvent(ST_NAME_BATTERY_STATE)
        clientsManager.addDefaultExcludedEvent(ST_NAME_BATTERY_LEVEL)
        clientsManager.addDefaultExcludedEvent(ST_NAME_LIGHT_LEVEL)
        # Registering the statuses which need an exlusive access for the
        # RESTRICTED clients.
        clientsManager.addRestrictedEvent(ST_NAME_HEAD_BUTTON)
        clientsManager.addRestrictedEvent(ST_NAME_LEFT_BUTTON)
        clientsManager.addRestrictedEvent(ST_NAME_RIGHT_BUTTON)
        clientsManager.addRestrictedEvent(ST_NAME_REMOTE_BUTTON)
        # Create and configure a Tux Driver object
        self.__tuxDriver = TuxDrv()
        self.__tuxDriver.SetLogLevel(TDS_CONF_LOG_LEVEL)
        self.__tuxDriver.SetLogTarget(TDS_CONF_LOG_TARGET)
        self.__tuxDriver.SetStatusCallback(self.__onStatusCallback)
        self.__tuxDriver.SetEndCycleCallback(self.__onEndOfCycleCallback)
        eventsHandler.getEventHandler(ST_NAME_DONGLE_PLUG).register(self.__onDonglePlugCallback)
        # Others
        self.__donglePlugged = False
        self.__statusesStruct = []

    # --------------------------------------------------------------------------
    # Start the resource.
    # --------------------------------------------------------------------------
    def start(self):
        """Start the resource.
        """
        t = threading.Thread(target = self.__tuxDriver.Start)
        t.start()

    # --------------------------------------------------------------------------
    # Stop the resource.
    # --------------------------------------------------------------------------
    def stop(self):
        """Stop the resource.
        """
        self.__tuxDriver.Stop()

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
        self.__statusesStruct.append(self.__tuxDriver.GetStatusStruct(status))

    # --------------------------------------------------------------------------
    # Event on tuxdriver end of cycle ~100msec.
    # --------------------------------------------------------------------------
    def __onEndOfCycleCallback(self):
        """Event on tuxdriver end of cycle ~100msec.
        """
        def async():
            clientsManager.pushEvents(self.__statusesStruct)
            for statusStruct in self.__statusesStruct:
                eventsHandler.emit(statusStruct['name'], (statusStruct['value'],
                    float(statusStruct['delay'])))
            self.__statusesStruct = []
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Event on dongle plug/unplug.
    # --------------------------------------------------------------------------
    def __onDonglePlugCallback(self, value, delay):
        """Event on dongle plug/unplug.
        """
        self.__donglePlugged = value
        if value:
            self.__initializeStatesInEventsHandler()

    # --------------------------------------------------------------------------
    # Initialize statuses state in the events handler.
    # --------------------------------------------------------------------------
    def __initializeStatesInEventsHandler(self):
        """Initialize statuses state in the events handler.
        """
        def async():
            states = self.__tuxDriver.GetAllStatusState()
            if len(states) > 0:
                states = states[:-1]
            states = states.split('\n')
            for state in states:
                stateStruct = self.__tuxDriver.GetStatusStruct(state)
                if stateStruct['name'] != "None":
                    eventsHandler.updateState(stateStruct['name'], (
                        stateStruct['value'], float(stateStruct['delay'])))
        t = threading.Thread(target = async)
        t.start()

    # ==========================================================================
    # Public methods
    # ==========================================================================

    # Misc ---------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Get if the dongle is plugged or not.
    # --------------------------------------------------------------------------
    def getDonglePlugged(self):
        """Get if the dongle is plugged or not.
        @return: True or False.
        """
        return self.__donglePlugged

    # --------------------------------------------------------------------------
    # Reset the body positions and clear the commands stack.
    # --------------------------------------------------------------------------
    def clearAll(self):
        """Reset the body positions and clear the commands stack.
        """
        self.__tuxDriver.ClearCommandStack()
        self.__tuxDriver.ResetPositions()
        self.__tuxDriver.PerformCommand(0.0,'TUX_CMD:LED:ON:LED_BOTH,1.0')

    # --------------------------------------------------------------------------
    # Execute a macro text.
    # --------------------------------------------------------------------------
    def executeMacro(self, macro):
        """Execute a macro text.
        @param macro: Macro text.
        """
        self.__tuxDriver.PerformMacroText(macro)

    # --------------------------------------------------------------------------
    # Execute a RAW command.
    # --------------------------------------------------------------------------
    def executeRawCommand(self, rawCommand, delay = 0.0):
        """Execute a RAW command.
        @param rawCommand: RAW command.
        @param delay: Delay before to execute the command.
        """
        self.__tuxDriver.PerformCommand(0.0, rawCommand)

    # Sound --------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Set the current sound channel in the dongle.
    # --------------------------------------------------------------------------
    def setSoundChannel(self, channelName):
        """Set the current sound channel in the dongle.
        @param channelName: Name of the channel. <GENERAL|TTS>
        """
        def async():
            cmd = "TUX_CMD:AUDIO:CHANNEL_%s" % channelName
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()

    # --------------------------------------------------------------------------
    # Play a sound flash.
    # --------------------------------------------------------------------------
    def playSound(self, track, volume):
        """Play a sound flash.
        @param track: Number of the sound to play <1..255>
        @param volume: Volume of the sound <0.0 .. 100.0>
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:SOUND_FLASH:PLAY:%d,%f' % (track, volume)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Reflash the sound flash memory of Tux Droid.
    # --------------------------------------------------------------------------
    def reflashSoundMemory(self, tracks):
        """Reflash the sound flash memory of Tux Droid.
        @param tracks: Tracks list. "<wav_path_1>|<wav_path_2>|...|<wav_path_n>"
        """
        self.__tuxDriver.SoundReflash(tracks)

    # Eyes ---------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Open the eyes.
    # --------------------------------------------------------------------------
    def openEyes(self):
        """Open the eyes.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            self.__tuxDriver.PerformCommand(0.0, 'TUX_CMD:EYES:OPEN')
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Close the eyes.
    # --------------------------------------------------------------------------
    def closeEyes(self):
        """Close the eyes.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            self.__tuxDriver.PerformCommand(0.0, 'TUX_CMD:EYES:CLOSE')
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a movement of the eyes.
    # --------------------------------------------------------------------------
    def eyesOn(self, count, finalState):
        """Start a movement of the eyes.
        @param count: Number of movements.
        @param finalState: Final state of the eyes at the end of movements.
        <NDEF|OPEN|CLOSE>
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:EYES:ON:%d,%s' % (count, finalState)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a movement of the eyes.
    # --------------------------------------------------------------------------
    def eyesOnDuring(self, duration, finalState):
        """Start a movement of the eyes.
        @param duration: Duration of the eyes movement.
        @param finalState: Final state of the eyes at the end of movements.
        <NDEF|OPEN|CLOSE>
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:EYES:ON_DURING:%f,%s' % (duration, finalState)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Stop the eyes movement.
    # --------------------------------------------------------------------------
    def eyesOff(self):
        """Stop the eyes movement.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            self.__tuxDriver.PerformCommand(0.0, 'TUX_CMD:EYES:OFF')
        t = threading.Thread(target = async)
        t.start()
        return True

    # Mouth --------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Open the mouth.
    # --------------------------------------------------------------------------
    def openMouth(self):
        """Open the mouth.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            self.__tuxDriver.PerformCommand(0.0, 'TUX_CMD:MOUTH:OPEN')
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Close the mouth.
    # --------------------------------------------------------------------------
    def closeMouth(self):
        """Close the mouth.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            self.__tuxDriver.PerformCommand(0.0, 'TUX_CMD:MOUTH:CLOSE')
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a movement of the mouth.
    # --------------------------------------------------------------------------
    def mouthOn(self, count, finalState):
        """Start a movement of the mouth.
        @param count: Number of movements.
        @param finalState: Final state of the mouth at the end of movements.
        <NDEF|OPEN|CLOSE>
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:MOUTH:ON:%d,%s' % (count, finalState)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a movement of the mouth.
    # --------------------------------------------------------------------------
    def mouthOnDuring(self, duration, finalState):
        """Start a movement of the mouth.
        @param duration: Duration of the mouth movement.
        @param finalState: Final state of the mouth at the end of movements.
        <NDEF|OPEN|CLOSE>
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:MOUTH:ON_DURING:%f,%s' % (duration, finalState)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Stop the mouth movement.
    # --------------------------------------------------------------------------
    def mouthOff(self):
        """Stop the mouth movement.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            self.__tuxDriver.PerformCommand(0.0, 'TUX_CMD:MOUTH:OFF')
        t = threading.Thread(target = async)
        t.start()
        return True

    # Flippers -----------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Set the flippers position to up.
    # --------------------------------------------------------------------------
    def upFlippers(self):
        """Set the flippers position to up.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            self.__tuxDriver.PerformCommand(0.0, 'TUX_CMD:FLIPPERS:UP')
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Set the flippers position to down.
    # --------------------------------------------------------------------------
    def downFlippers(self):
        """Set the flippers position to down.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            self.__tuxDriver.PerformCommand(0.0, 'TUX_CMD:FLIPPERS:DOWN')
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a movement of the filppers.
    # --------------------------------------------------------------------------
    def flippersOn(self, count, finalState):
        """Start a movement of the filppers.
        @param count: Number of movements.
        @param finalState: Final state of the flippers at the end of movements.
        <NDEF|UP|DOWN>
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:FLIPPERS:ON:%d,%s' % (count, finalState)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a movement of the filppers.
    # --------------------------------------------------------------------------
    def flippersOnDuring(self, duration, finalState):
        """Start a movement of the filppers.
        @param duration: Duration of the flippers movement.
        @param finalState: Final state of the flippers at the end of movements.
        <NDEF|UP|DOWN>
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:FLIPPERS:ON_DURING:%f,%s' % (duration, finalState)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Stop the flippers movement.
    # --------------------------------------------------------------------------
    def flippersOff(self):
        """Stop the flippers movement.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            self.__tuxDriver.PerformCommand(0.0, 'TUX_CMD:FLIPPERS:OFF')
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Set the speed of the flippers movements.
    # --------------------------------------------------------------------------
    def setFlippersSpeed(self, speed):
        """Set the speed of the flippers movements.
        @param speed: Speed.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:FLIPPERS:SPEED:%d' % speed
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # Spinning -----------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Start a rotation to the left.
    # --------------------------------------------------------------------------
    def spinLeftOn(self, count):
        """Start a rotation to the left.
        @param count: Number of quarter of turns.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:SPINNING:LEFT_ON:%d' % count
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a rotation to the right.
    # --------------------------------------------------------------------------
    def spinRightOn(self, count):
        """Start a rotation to the right.
        @param count: Number of quarter of turns.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:SPINNING:RIGHT_ON:%d' % count
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a rotation to the left.
    # --------------------------------------------------------------------------
    def spinLeftOnDuring(self, duration):
        """Start a rotation to the left.
        @param duration: Duration of the rotation in seconds.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:SPINNING:LEFT_ON_DURING:%f' % duration
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a rotation to the right.
    # --------------------------------------------------------------------------
    def spinRightOnDuring(self, duration):
        """Start a rotation to the right.
        @param duration: Duration of the rotation in seconds.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:SPINNING:RIGHT_ON_DURING:%f' % duration
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Stop the rotation.
    # --------------------------------------------------------------------------
    def spinningOff(self):
        """Stop the rotation.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:SPINNING:OFF'
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Set the speed of the rotation.
    # --------------------------------------------------------------------------
    def setSpinningSpeed(self, speed):
        """Set the speed of the rotation.
        @param speed: Speed.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:SPINNING:SPEED:%d' % speed
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # Leds ---------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Start a blink of the leds.
    # --------------------------------------------------------------------------
    def ledsBlink(self, leds, count, delay):
        """Start a blink of the leds.
        @param leds: Leds. <LED_BOTH|LED_RIGHT|LED_LEFT>
        @param count: Number of blinks.
        @param delay: Delay between 2 blinks in seconds.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:LED:BLINK:%s,%d,%f' % (leds, count, delay)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Stop any leds state changes.
    # --------------------------------------------------------------------------
    def ledsOff(self, leds):
        """Stop any leds state changes.
        @param leds: Leds. <LED_BOTH|LED_RIGHT|LED_LEFT>
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:LED:OFF:%s' % leds
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Turn on the leds.
    # --------------------------------------------------------------------------
    def ledsOn(self, leds, intensity):
        """Turn on the leds.
        @param leds: Leds. <LED_BOTH|LED_RIGHT|LED_LEFT>
        @param intensity: Leds intensity. <0.0 .. 1.0>
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:LED:ON:%s,%f' % (leds, intensity)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a transition of the leds state.
    # --------------------------------------------------------------------------
    def ledsSet(self, leds, intensity, fxType, fxSpeed, fxStep):
        """Start a transition of the leds state.
        @param leds: Leds. <LED_BOTH|LED_RIGHT|LED_LEFT>
        @param intensity: Final leds intensity. <0.0 .. 1.0>
        @param fxType: <UNAFFECTED|LAST|NONE|DEFAULT|FADE_DURATION|FADE_RATE|GRADIENT_NBR|GRADIENT_DELTA>
        @param fxSpeed: Speed of the transition.
        @param fxStep: Number of steps while the leds transition.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:LED:SET:%s,%f,%s,%f,%d' % (leds, intensity, fxType,
                fxSpeed, fxStep)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

    # --------------------------------------------------------------------------
    # Start a pluse effect of the leds.
    # --------------------------------------------------------------------------
    def ledsPulse(self, leds, minIntensity, maxIntensity, count, period, fxType,
        fxSpeed, fxStep):
        """Start a pluse effect of the leds.
        @param leds: Leds. <LED_BOTH|LED_RIGHT|LED_LEFT>
        @param minIntensity: Minimal leds intensity. <0.0 .. 1.0>
        @param maxIntensity: Maximal leds intensity. <0.0 .. 1.0>
        @param count: Number of pulses.
        @param period: Period duration of the pulse transitions.
        @param fxType: <UNAFFECTED|LAST|NONE|DEFAULT|FADE_DURATION|FADE_RATE|GRADIENT_NBR|GRADIENT_DELTA>
        @param fxSpeed: Speed of the transitions.
        @param fxStep: Number of steps while the leds transition.
        @return: True or False. (depend of the dongle plug state)
        """
        if not self.__donglePlugged:
            return False
        def async():
            cmd = 'TUX_CMD:LED:PULSE:%s,%f,%f,%d,%f,%s,%f,%d' % (leds,
                minIntensity, maxIntensity, count, period, fxType, fxSpeed,
                fxStep)
            self.__tuxDriver.PerformCommand(0.0, cmd)
        t = threading.Thread(target = async)
        t.start()
        return True

# Create an instance of the resource
resourceTuxDriver = TDSResourceTuxDriver("resourceTuxDriver")
# Register the resource into the resources manager
resourcesManager.addResource(resourceTuxDriver)
