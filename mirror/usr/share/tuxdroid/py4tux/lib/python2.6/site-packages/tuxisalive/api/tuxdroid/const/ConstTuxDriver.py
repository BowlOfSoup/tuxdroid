#    Copyright (C) 2009 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

#
# Statuses declaration
#
ST_NAME_HEAD_BUTTON                 = 'head_button'
ST_NAME_LEFT_BUTTON                 = 'left_wing_button'
ST_NAME_RIGHT_BUTTON                = 'right_wing_button'
ST_NAME_REMOTE_BUTTON               = 'remote_button'
ST_NAME_MOUTH_POSITION              = 'mouth_position'
ST_NAME_MOUTH_RM                    = 'mouth_remaining_movements'
ST_NAME_EYES_POSITION               = 'eyes_position'
ST_NAME_EYES_RM                     = 'eyes_remaining_movements'
ST_NAME_FLIPPERS_POSITION           = 'flippers_position'
ST_NAME_FLIPPERS_RM                 = 'flippers_remaining_movements'
ST_NAME_SPINNING_DIRECTION          = 'spinning_direction'
ST_NAME_SPINNING_RM                 = 'spinning_remaining_movements'
ST_NAME_DONGLE_PLUG                 = 'dongle_plug'
ST_NAME_RADIO_STATE                 = 'radio_state'
ST_NAME_LEFT_LED                    = 'left_led_state'
ST_NAME_RIGHT_LED                   = 'right_led_state'
ST_NAME_CONNECTION_QUALITY          = 'connection_quality'
ST_NAME_AUDIO_FLASH_PLAY            = 'audio_flash_play'
ST_NAME_FLASH_PROG_END              = 'sound_reflash_end'
ST_NAME_EYES_MOTOR_ON               = 'eyes_motor_on'
ST_NAME_MOUTH_MOTOR_ON              = 'mouth_motor_on'
ST_NAME_FLIPPERS_MOTOR_ON           = 'flippers_motor_on'
ST_NAME_SPIN_LEFT_MOTOR_ON          = 'spin_left_motor_on'
ST_NAME_SPIN_RIGHT_MOTOR_ON         = 'spin_right_motor_on'
ST_NAME_DRIVER_SYMB_VER             = 'driver_symbolic_version'
ST_NAME_TUXCORE_SYMB_VER            = 'tuxcore_symbolic_version'
ST_NAME_TUXAUDIO_SYMB_VER           = 'tuxaudio_symbolic_version'
ST_NAME_FUXUSB_SYMB_VER             = 'fuxusb_symbolic_version'
ST_NAME_FUXRF_SYMB_VER              = 'fuxrf_symbolic_version'
ST_NAME_TUXRF_SYMB_VER              = 'tuxrf_symbolic_version'
ST_NAME_FLASH_SOUND_COUNT           = 'sound_flash_count'
ST_NAME_BATTERY_LEVEL               = 'battery_level'
ST_NAME_BATTERY_STATE               = 'battery_state'
ST_NAME_CHARGER_STATE               = 'charger_state'
ST_NAME_LIGHT_LEVEL                 = 'light_level'
ST_NAME_DESCRIPTOR_COMPLETE         = 'descriptor_complete'
ST_NAME_AUDIO_GENERAL_PLAY          = 'audio_general_play'
ST_NAME_FLASH_PROG_CURRENT_TRACK    = 'flash_programming_current_track'
ST_NAME_FLASH_PROG_LAST_TRACK_SIZE  = 'flash_programming_current_track'
ST_NAME_FLASH_PROG_BEGIN            = 'sound_reflash_begin'
SW_NAME_DRIVER = [
    ST_NAME_FLIPPERS_POSITION,
    ST_NAME_FLIPPERS_RM,
    ST_NAME_SPINNING_DIRECTION,
    ST_NAME_SPINNING_RM,
    ST_NAME_LEFT_BUTTON,
    ST_NAME_RIGHT_BUTTON,
    ST_NAME_HEAD_BUTTON,
    ST_NAME_REMOTE_BUTTON,
    ST_NAME_MOUTH_POSITION,
    ST_NAME_MOUTH_RM,
    ST_NAME_EYES_POSITION,
    ST_NAME_EYES_RM,
    ST_NAME_DESCRIPTOR_COMPLETE,
    ST_NAME_RADIO_STATE,
    ST_NAME_DONGLE_PLUG,
    ST_NAME_CHARGER_STATE,
    ST_NAME_BATTERY_LEVEL,
    ST_NAME_BATTERY_STATE,
    ST_NAME_LIGHT_LEVEL,
    ST_NAME_LEFT_LED,
    ST_NAME_RIGHT_LED,
    ST_NAME_CONNECTION_QUALITY,
    ST_NAME_AUDIO_FLASH_PLAY,
    ST_NAME_AUDIO_GENERAL_PLAY,
    ST_NAME_FLASH_PROG_CURRENT_TRACK,
    ST_NAME_FLASH_PROG_LAST_TRACK_SIZE,
    ST_NAME_TUXCORE_SYMB_VER,
    ST_NAME_TUXAUDIO_SYMB_VER,
    ST_NAME_FUXUSB_SYMB_VER,
    ST_NAME_FUXRF_SYMB_VER,
    ST_NAME_TUXRF_SYMB_VER,
    ST_NAME_DRIVER_SYMB_VER,
    ST_NAME_FLASH_PROG_CURRENT_TRACK,
    ST_NAME_FLASH_PROG_BEGIN,
    ST_NAME_FLASH_PROG_END,
    ST_NAME_EYES_MOTOR_ON,
    ST_NAME_MOUTH_MOTOR_ON,
    ST_NAME_FLIPPERS_MOTOR_ON,
    ST_NAME_SPIN_LEFT_MOTOR_ON,
    ST_NAME_SPIN_RIGHT_MOTOR_ON,
    ST_NAME_FLASH_SOUND_COUNT,
]

#
# Possible string values of statuses
#
SSV_NDEF            = "NDEF"
SSV_OPEN            = "OPEN"
SSV_CLOSE           = "CLOSE"
SSV_UP              = "UP"
SSV_DOWN            = "DOWN"
SSV_LEFT            = "LEFT"
SSV_RIGHT           = "RIGHT"
SSV_ON              = "ON"
SSV_OFF             = "OFF"
SSV_CHANGING        = "CHANGING"

# Mouth and eyes positions
SSV_MOUTHEYES_POSITIONS = [
    SSV_NDEF,
    SSV_OPEN,
    SSV_CLOSE,
]

# Flippers positions
SSV_FLIPPERS_POSITIONS = [
    SSV_NDEF,
    SSV_UP,
    SSV_DOWN,
]

# Spinning directions
SSV_SPINNING_DIRECTIONS = [
    SSV_NDEF,
    SSV_LEFT,
    SSV_RIGHT,
]

# Led states
SSV_LED_STATES = [
    SSV_ON,
    SSV_OFF,
    SSV_CHANGING,
]

#
# Speed values
#
SPV_VERYSLOW    = 1
SPV_SLOW        = 2
SPV_NORMAL      = 3
SPV_FAST        = 4
SPV_VERYFAST    = 5
SPV_SPEED_VALUES = [
    SPV_VERYSLOW,
    SPV_SLOW,
    SPV_NORMAL,
    SPV_FAST,
    SPV_VERYFAST,
]

#
# Led effects
#

# Simples
LFX_NONE        = 0
LFX_FADE        = 1
LFX_STEP        = 2
LED_EFFECT_TYPE = [
    LFX_NONE,
    LFX_FADE,
    LFX_STEP,
]

# Extended
LFXEX_UNAFFECTED        = "UNAFFECTED"
LFXEX_LAST              = "LAST"
LFXEX_NONE              = "NONE"
LFXEX_DEFAULT           = "DEFAULT"
LFXEX_FADE_DURATION     = "FADE_DURATION"
LFXEX_FADE_RATE         = "FADE_RATE"
LFXEX_GRADIENT_NBR      = "GRADIENT_NBR"
LFXEX_GRADIENT_DELTA    = "GRADIENT_DELTA"
LED_EFFECT_TYPE_EX_NAMES = [
    LFXEX_UNAFFECTED,
    LFXEX_LAST,
    LFXEX_NONE,
    LFXEX_DEFAULT,
    LFXEX_FADE_DURATION,
    LFXEX_FADE_RATE,
    LFXEX_GRADIENT_NBR,
    LFXEX_GRADIENT_DELTA,
]

#
# Led names
#
LED_NAME_BOTH           = "LED_BOTH"
LED_NAME_RIGHT          = "LED_RIGHT"
LED_NAME_LEFT           = "LED_LEFT"

#
# Sound reflash errors
#
SOUND_REFLASH_NO_ERROR              = "NO_ERROR"
SOUND_REFLASH_ERROR_RF_OFFLINE      = "ERROR_RF_OFFLINE"
SOUND_REFLASH_ERROR_WAV             = "ERROR_WAV"
SOUND_REFLASH_ERROR_USB             = "ERROR_USB"
SOUND_REFLASH_ERROR_PARAMETERS      = "ERROR_PARAMETERS"
SOUND_REFLASH_ERROR_BUSY            = "ERROR_BUSY"
SOUND_REFLASH_ERROR_BADWAVFILE      = "ERROR_BADWAVFILE"
SOUND_REFLASH_ERROR_WAVSIZEEXCEDED  = "ERROR_WAVSIZEEXCEDED"

#
# Remote keys
#
K_0             = "K_0"
K_1             = "K_1"
K_2             = "K_2"
K_3             = "K_3"
K_4             = "K_4"
K_5             = "K_5"
K_6             = "K_6"
K_7             = "K_7"
K_8             = "K_8"
K_9             = "K_9"
K_STANDBY       = "K_STANDBY"
K_MUTE          = "K_MUTE"
K_VOLUMEPLUS    = "K_VOLUMEPLUS"
K_VOLUMEMINUS   = "K_VOLUMEMINUS"
K_ESCAPE        = "K_ESCAPE"
K_YES           = "K_YES"
K_NO            = "K_NO"
K_BACKSPACE     = "K_BACKSPACE"
K_STARTVOIP     = "K_STARTVOIP"
K_RECEIVECALL   = "K_RECEIVECALL"
K_HANGUP        = "K_HANGUP"
K_STAR          = "K_STAR"
K_SHARP         = "K_SHARP"
K_RED           = "K_RED"
K_GREEN         = "K_GREEN"
K_BLUE          = "K_BLUE"
K_YELLOW        = "K_YELLOW"
K_CHANNELPLUS   = "K_CHANNELPLUS"
K_CHANNELMINUS  = "K_CHANNELMINUS"
K_UP            = "K_UP"
K_DOWN          = "K_DOWN"
K_LEFT          = "K_LEFT"
K_RIGHT         = "K_RIGHT"
K_OK            = "K_OK"
K_FASTREWIND    = "K_FASTREWIND"
K_FASTFORWARD   = "K_FASTFORWARD"
K_PLAYPAUSE     = "K_PLAYPAUSE"
K_STOP          = "K_STOP"
K_RECORDING     = "K_RECORDING"
K_PREVIOUS      = "K_PREVIOUS"
K_NEXT          = "K_NEXT"
K_MENU          = "K_MENU"
K_MOUSE         = "K_MOUSE"
K_ALT           = "K_ALT"
K_RELEASED      = "RELEASED"

REMOTE_KEY_LIST = [
    K_0,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_STANDBY,
    K_MUTE,
    K_VOLUMEPLUS,
    K_VOLUMEMINUS,
    K_ESCAPE,
    K_YES,
    K_NO,
    K_BACKSPACE,
    K_STARTVOIP,
    K_RECEIVECALL,
    K_HANGUP,
    K_STAR,
    K_SHARP,
    K_RED,
    K_GREEN,
    K_BLUE,
    K_YELLOW,
    K_CHANNELPLUS,
    K_CHANNELMINUS,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_OK,
    K_FASTREWIND,
    K_FASTFORWARD,
    K_PLAYPAUSE,
    K_STOP,
    K_RECORDING,
    K_PREVIOUS,
    K_NEXT,
    K_MENU,
    K_MOUSE,
    K_ALT,
    K_RELEASED,
]

#
# Battery states
#
BATTERY_STATE_FULL = "FULL"
BATTERY_STATE_HIGH = "HIGH"
BATTERY_STATE_LOW = "LOW"
BATTERY_STATE_EMPTY = "EMPTY"
BATTERY_STATES_LIST = [
    BATTERY_STATE_FULL,
    BATTERY_STATE_HIGH,
    BATTERY_STATE_LOW,
    BATTERY_STATE_EMPTY,
]

#
# Charger states
#
CHARGER_STATE_UNPLUGGED = "UNPLUGGED"
CHARGER_STATE_CHARGING = "CHARGING"
CHARGER_STATE_PLUGGED_NO_POWER = "PLUGGED_NO_POWER"
CHARGER_STATE_TRICKLE = "TRICKLE"
CHARGER_STATE_INHIBITED = "INHIBITED"
CHARGER_STATES_LIST = [
    CHARGER_STATE_UNPLUGGED,
    CHARGER_STATE_CHARGING,
    CHARGER_STATE_PLUGGED_NO_POWER,
    CHARGER_STATE_TRICKLE,
    CHARGER_STATE_INHIBITED,
]