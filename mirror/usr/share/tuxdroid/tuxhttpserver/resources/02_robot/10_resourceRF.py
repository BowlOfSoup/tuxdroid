# ==============================================================================
# Wifi avoidance resource.
# ==============================================================================

import math

from util.wifi.TuxWifiChannel import TuxWifiChannel
from util.misc import URLTools

# ------------------------------------------------------------------------------
# Wifi and ATR2406
# ------------------------------------------------------------------------------

FLOAT_INT_ROUND = 0
FLOAT_INT_FLOOR = 1
FLOAT_INT_CEIL = 0

WIFI_LOWER_FREQ = 2401
WIFI_FIRST_CHANNEL_C_FREQ = 2412
WIFI_CHANNEL_STEP = 5
WIFI_CHANNEL_BANDWIDTH = 22
WIFI_DEFAULT_AVOIDED_BANDWIDTH = 55

ATR2406_FIRST_FREQ = 2401.056
ATR2406_CHANNEL_STEP = 0.864
ATR2406_MIN_CHANNEL = 0
ATR2406_MAX_CHANNEL = 94

def ATR2406_ChannelToFreq(channel):
    return ATR2406_FIRST_FREQ + (channel * ATR2406_CHANNEL_STEP)

def ATR2406_FreqToChannel(freq, ff = FLOAT_INT_ROUND):
    freq -= ATR2406_FIRST_FREQ
    channel = freq / ATR2406_CHANNEL_STEP
    if ff == FLOAT_INT_FLOOR:
        result = int(math.floor(channel))
    elif ff == FLOAT_INT_CEIL:
        result = int(math.ceil(channel))
    else:
        result = int(channel + 0.5)
    if result < ATR2406_MIN_CHANNEL:
        result = ATR2406_MIN_CHANNEL
    elif result > ATR2406_MAX_CHANNEL:
        result = ATR2406_MAX_CHANNEL
    return result

def WIFI_ChannelToFreq(channel):
    if channel == 14:
        return 2484
    else:
        channel -= 1
        return WIFI_FIRST_CHANNEL_C_FREQ + (WIFI_CHANNEL_STEP * channel)

def WIFI_ChannelLowFreq(channel, bandwidth = WIFI_CHANNEL_BANDWIDTH):
    freq = WIFI_ChannelToFreq(channel)
    freq -= bandwidth / 2
    if freq < WIFI_LOWER_FREQ:
        freq = WIFI_LOWER_FREQ
    return freq

def WIFI_ChannelHighFreq(channel, bandwidth = WIFI_CHANNEL_BANDWIDTH):
    freq = WIFI_ChannelToFreq(channel)
    freq += bandwidth / 2
    return freq

def WIFI_ATR2406_ChannelInfos(channel, bandwidth = WIFI_CHANNEL_BANDWIDTH):
    wCFreq = WIFI_ChannelToFreq(channel)
    wLFreq = WIFI_ChannelLowFreq(channel, bandwidth)
    wHFreq = WIFI_ChannelHighFreq(channel, bandwidth)
    aCChan = ATR2406_FreqToChannel(wCFreq, FLOAT_INT_ROUND)
    aCFreq = ATR2406_ChannelToFreq(aCChan)
    aLChan = ATR2406_FreqToChannel(wLFreq, FLOAT_INT_FLOOR)
    aLFreq = ATR2406_ChannelToFreq(aLChan)
    aHChan = ATR2406_FreqToChannel(wHFreq, FLOAT_INT_CEIL)
    aHFreq = ATR2406_ChannelToFreq(aHChan)
    aBandWidth = aHFreq - aLFreq
    return wCFreq, wLFreq, wHFreq, aCChan, aCFreq, aLChan, aLFreq, aHChan, aHFreq, aBandWidth

# ------------------------------------------------------------------------------
# Declaration of the resource "rf".
# ------------------------------------------------------------------------------
class TDSResourceRF(TDSResource):

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def configure(self):
        self.name = "rf"
        self.comment = "Resource to manage the radio connection."
        self.fileName = RESOURCE_FILENAME
        self.__wifiChanDetector = TuxWifiChannel()
        self.__flagsMutex = threading.Lock()
        self.__channelInUse = None
        self.__connectionDetected = False
        self.__chanCycleMap = [1, 6, 11]
        self.__currentChanCycleIdx = 0
        defaultConfiguration = {
            'avoided_channel' : None,
            'avoided_bandwidth' : WIFI_DEFAULT_AVOIDED_BANDWIDTH,
        }
        # Create a logger
        self.logger = SimpleLogger("rf")
        self.logger.resetLog()
        self.logger.setLevel(TDS_CONF_LOG_LEVEL)
        self.logger.setTarget(TDS_CONF_LOG_TARGET)
        self.logger.logInfo("-----------------------------------------------")
        self.logger.logInfo("Smart-core RF")
        self.logger.logInfo("Licence : GPL")
        self.logger.logInfo("-----------------------------------------------")
        # Load configuration
        self.configurator.load('resourceRF.conf', defaultConfiguration)
        self.statesChecker()
        resourceScheduler.createTask_RunEveryX(
            "Wifi avoidance task",
            [True, True, True, True, True, True, True],
            [0, 0, 0],
            [23, 59, 59],
            [0, 0, 15],
            "resourceRF.statesChecker",
            (),
            None)
        eventsHandler.getEventHandler(ST_NAME_DONGLE_PLUG).register(self.__onDonglePlugCallback)
        eventsHandler.getEventHandler(ST_NAME_RADIO_STATE).register(self.__onRadioStateCallback)

    # --------------------------------------------------------------------------
    # Inherited methods from TDSResource
    # --------------------------------------------------------------------------

    def __channelIsInUse(self):
        self.__flagsMutex.acquire()
        result = self.__channelInUse
        self.__flagsMutex.release()
        return result

    def __setChannelInUse(self, channel):
        self.__flagsMutex.acquire()
        self.__channelInUse = channel
        self.__flagsMutex.release()

    def __connectionIsDetected(self):
        self.__flagsMutex.acquire()
        result = self.__connectionDetected
        self.__flagsMutex.release()
        return result

    def __setConnectionDetected(self, value):
        self.__flagsMutex.acquire()
        self.__connectionDetected = value
        self.__flagsMutex.release()

    def statesChecker(self):
        userChannel = self.configurator.getConfiguration()['avoided_channel']
        userBandwidth = self.configurator.getConfiguration()['avoided_bandwidth']
        if self.__channelIsInUse() != None:
            self.avoidChannel(self.__channelIsInUse(), userBandwidth)
        else:
            if userChannel != None:
                self.logger.logInfo("Manual wifi channel avoidance : ch=%d bw=%d" % (userChannel, userBandwidth))
                self.avoidChannel(userChannel, userBandwidth)
                self.__setChannelInUse(userChannel)
                self.__setConnectionDetected(True)
            else:
                detectedChannel = self.detectChannel()
                if detectedChannel != None:
                    self.logger.logInfo("Automatic wifi channel avoidance : ch=%d" % detectedChannel)
                    self.avoidChannel(detectedChannel, WIFI_DEFAULT_AVOIDED_BANDWIDTH)
                    self.__setChannelInUse(detectedChannel)
                    self.__setConnectionDetected(True)
                else:
                    chan = self.__chanCycleMap[self.__currentChanCycleIdx]
                    self.__currentChanCycleIdx += 1
                    if self.__currentChanCycleIdx >= len(self.__chanCycleMap):
                        self.__currentChanCycleIdx = 0
                    self.avoidChannel(chan, WIFI_DEFAULT_AVOIDED_BANDWIDTH)

    def resetStates(self):
        self.logger.logInfo("Reset wifi channel avoidance states")
        self.__setChannelInUse(None)
        self.__setConnectionDetected(False)

    def detectChannel(self):
        """Get the currently used wifi channel by your wifi network.
        @return: The channel as integer or None.
        """
        channel = self.__wifiChanDetector.getCurrent()
        return channel

    def avoidChannel(self, channel, bandwidth):
        """Avoid a WIFI channel from the RF connection.
        @param channel: Wifi channel to avoid.
        @param bandwidth: Bandwith around the avoid channel (in MHz).
        """
        wCFreq, wLFreq, wHFreq, aCChan, aCFreq, aLChan, aLFreq, aHChan, aHFreq, aBandWidth = WIFI_ATR2406_ChannelInfos(channel, bandwidth)
        cmd = "RAW_CMD:0x00:0x88:0x%.2x:0x%.2x:0x00" % (aLChan, aHChan)
        resourceTuxDriver.executeRawCommand(cmd)

    def sleepTuxDroid(self):
        """Switch Tux Droid to sleep mode.
        """
        cmd = "RAW_CMD:0x00:0xB7:0x01:0x00:0x00"
        resourceTuxDriver.executeRawCommand(cmd)

    def wakeUpTuxDroid(self):
        """Waking up Tux Droid.
        """
        cmd = "RAW_CMD:0x00:0xB6:0xFF:0x01:0x00"
        resourceTuxDriver.executeRawCommand(cmd)

    # ==========================================================================
    # Private methods
    # ==========================================================================

    # --------------------------------------------------------------------------
    # Event on dongle plug/unplug.
    # --------------------------------------------------------------------------
    def __onDonglePlugCallback(self, value, delay):
        """Event on dongle plug/unplug.
        """
        if not value:
            self.resetStates()

    # --------------------------------------------------------------------------
    # Event on radio state change.
    # --------------------------------------------------------------------------
    def __onRadioStateCallback(self, value, delay):
        """Event on radio state change.
        """
        if value:
            self.statesChecker()
        else:
            self.resetStates()

# Create an instance of the resource
resourceRF = TDSResourceRF("resourceRF")
# Register the resource into the resources manager
resourcesManager.addResource(resourceRF)

# ------------------------------------------------------------------------------
# Declaration of the service "avoid".
# ------------------------------------------------------------------------------
class TDSServiceRFAvoid(TDSService):

    def configure(self):
        self.parametersDict = {
            'channel' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "avoid"
        self.comment = "Avoid a wifi channel in the RF connection."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        channel = parameters['channel']
        configurator = resourceRF.getConfigurator()
        configurator.getConfiguration()['avoided_channel'] = channel
        configurator.getConfiguration()['avoided_bandwidth'] = WIFI_DEFAULT_AVOIDED_BANDWIDTH
        configurator.store()
        resourceRF.resetStates()
        resourceRF.statesChecker()
        return headersStruct, contentStruct

# Register the service into the resource
resourceRF.addService(TDSServiceRFAvoid)

# ------------------------------------------------------------------------------
# Declaration of the service "avoid_ex".
# ------------------------------------------------------------------------------
class TDSServiceRFAvoidEx(TDSService):

    def configure(self):
        self.parametersDict = {
            'channel' : 'uint8',
            'bandwidth' : 'uint8',
        }
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "avoid_ex"
        self.comment = "Avoid a wifi channel in the RF connection."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        channel = parameters['channel']
        bandwidth = parameters['bandwidth']
        configurator = resourceRF.getConfigurator()
        configurator.getConfiguration()['avoided_channel'] = channel
        configurator.getConfiguration()['avoided_bandwidth'] = bandwidth
        configurator.store()
        resourceRF.resetStates()
        resourceRF.statesChecker()
        return headersStruct, contentStruct

# Register the service into the resource
resourceRF.addService(TDSServiceRFAvoidEx)

# ------------------------------------------------------------------------------
# Declaration of the service "auto_avoid".
# ------------------------------------------------------------------------------
class TDSServiceRFAutoAvoid(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "auto_avoid"
        self.comment = "Automatic avoidance of wifi channel in the RF connection."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        configurator = resourceRF.getConfigurator()
        configurator.getConfiguration()['avoided_channel'] = None
        configurator.getConfiguration()['avoided_bandwidth'] = WIFI_DEFAULT_AVOIDED_BANDWIDTH
        configurator.store()
        resourceRF.resetStates()
        resourceRF.statesChecker()
        return headersStruct, contentStruct

# Register the service into the resource
resourceRF.addService(TDSServiceRFAutoAvoid)

# ------------------------------------------------------------------------------
# Declaration of the service "sleep".
# ------------------------------------------------------------------------------
class TDSServiceRFSleep(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "sleep"
        self.comment = "Sleeping."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceRF.sleepTuxDroid()
        return headersStruct, contentStruct

# Register the service into the resource
resourceRF.addService(TDSServiceRFSleep)

# ------------------------------------------------------------------------------
# Declaration of the service "wake_up".
# ------------------------------------------------------------------------------
class TDSServiceRFWakeUp(TDSService):

    def configure(self):
        self.parametersDict = {}
        self.minimalUserLevel = TDS_CLIENT_LEVEL_ANONYMOUS
        self.exclusiveExecution = True
        self.name = "wake_up"
        self.comment = "Wake up."

    def execute(self, id, parameters):
        headersStruct = self.getDefaultHeadersStruct()
        contentStruct = self.getDefaultContentStruct()
        contentStruct['root']['result'] = getStrError(E_TDREST_SUCCESS)
        resourceRF.wakeUpTuxDroid()
        return headersStruct, contentStruct

# Register the service into the resource
resourceRF.addService(TDSServiceRFWakeUp)
