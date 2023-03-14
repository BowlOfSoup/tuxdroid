# -*- coding: utf-8 -*-

import version
__author__ = version.author
__date__ = version.date
__version__ = version.version
__licence__ = version.licence
del version

#    Copyleft (C) 2008 C2ME Sa
#    Remi Jocaille <remi.jocaille@c2me.be>
#    Distributed under the terms of the GNU General Public License
#    http://www.gnu.org/copyleft/gpl.html

# Leds command structures
LEDS_BLINK_CANVAS = {'cmd' : 'leds_blink', 'count' : 1.0, 'speed' : 1}
LEDS_ON_CANVAS = {'cmd' : 'leds_on', 'duration' : 0.0}
LEDL_ON_CANVAS = {'cmd' : 'ledl_on', 'duration' : 0.0}
LEDR_ON_CANVAS = {'cmd' : 'ledr_on', 'duration' : 0.0}
LEDS_OFF_CANVAS = {'cmd' : 'leds_off', 'duration' : 0.0}
LEDL_OFF_CANVAS = {'cmd' : 'ledl_off', 'duration' : 0.0}
LEDR_OFF_CANVAS = {'cmd' : 'ledr_off', 'duration' : 0.0}

# Leds command types
LEDS_CMD_TYPES = {
    'Led on/off':
        [
            'leds_on',
            'ledl_on',
            'ledr_on',
            'leds_off',
            'ledl_off',
            'ledr_off'
        ],
    'Leds blink':
        ['leds_blink'],
}

# ------------------------------------------------------------------------------
# ledsBlinkTmc
# ------------------------------------------------------------------------------
def ledsBlinkTmc(struct):
    duration = (struct['speed'] * 0.004)
    cmd = 'TUX_CMD:LED:BLINK:LED_BOTH,%d,%f' % (struct['count'], duration)
    return [cmd,]

# ------------------------------------------------------------------------------
# ledsOnTmc
# ------------------------------------------------------------------------------
def ledsOnTmc(struct):
    cmd = 'TUX_CMD:LED:ON:LED_BOTH,1.0'
    return [cmd,]

# ------------------------------------------------------------------------------
# ledlOnTmc
# ------------------------------------------------------------------------------
def ledlOnTmc(struct):
    cmd = 'TUX_CMD:LED:ON:LED_LEFT,1.0'
    return [cmd,]

# ------------------------------------------------------------------------------
# ledrOnTmc
# ------------------------------------------------------------------------------
def ledrOnTmc(struct):
    cmd = 'TUX_CMD:LED:ON:LED_RIGHT,1.0'
    return [cmd,]

# ------------------------------------------------------------------------------
# ledsOffTmc
# ------------------------------------------------------------------------------
def ledsOffTmc(struct):
    cmd = 'TUX_CMD:LED:OFF:LED_BOTH'
    return [cmd,]

# ------------------------------------------------------------------------------
# ledlOffTmc
# ------------------------------------------------------------------------------
def ledlOffTmc(struct):
    cmd = 'TUX_CMD:LED:OFF:LED_LEFT'
    return [cmd,]

# ------------------------------------------------------------------------------
# ledrOffTmc
# ------------------------------------------------------------------------------
def ledrOffTmc(struct):
    cmd = 'TUX_CMD:LED:OFF:LED_RIGHT'
    return [cmd,]

# Mouth and eyes command structures
MOUTH_ON_CANVAS = {'cmd' : 'mouth_on', 'duration': 0.0, 'count' : 2}
MOUTH_OPEN_CANVAS = {'cmd' : 'mouth_open', 'duration': 0.0}
MOUTH_CLOSE_CANVAS = {'cmd' : 'mouth_close', 'duration': 0.0}
EYES_ON_CANVAS = {'cmd' : 'eyes_on', 'duration': 0.0, 'count' : 2}
EYES_OPEN_CANVAS = {'cmd' : 'eyes_open', 'duration': 0.0}
EYES_CLOSE_CANVAS = {'cmd' : 'eyes_close', 'duration': 0.0}

# Mouth and eyes command types
MOUTH_EYES_CMD_TYPES = {
    'Mouth':
        [
            'mouth_on',
            'mouth_open',
            'mouth_close'
        ],
    'Eyes':
        [
            'eyes_on',
            'eyes_open',
            'eyes_close'
        ]
}

# ------------------------------------------------------------------------------
# mouthOnTmc
# ------------------------------------------------------------------------------
def mouthOnTmc(struct):
    cmd = 'TUX_CMD:MOUTH:ON:%d,NDEF' % struct['count']
    return [cmd,]

# ------------------------------------------------------------------------------
# mouthOpenTmc
# ------------------------------------------------------------------------------
def mouthOpenTmc(struct):
    cmd = 'TUX_CMD:MOUTH:OPEN'
    return [cmd,]

# ------------------------------------------------------------------------------
# mouthCloseTmc
# ------------------------------------------------------------------------------
def mouthCloseTmc(struct):
    cmd = 'TUX_CMD:MOUTH:CLOSE'
    return [cmd,]

# ------------------------------------------------------------------------------
# eyesOnTmc
# ------------------------------------------------------------------------------
def eyesOnTmc(struct):
    cmd = 'TUX_CMD:EYES:ON:%d,NDEF' % struct['count']
    return [cmd,]

# ------------------------------------------------------------------------------
# eyesOpenTmc
# ------------------------------------------------------------------------------
def eyesOpenTmc(struct):
    cmd = 'TUX_CMD:EYES:OPEN'
    return [cmd,]

# ------------------------------------------------------------------------------
# eyesCloseTmc
# ------------------------------------------------------------------------------
def eyesCloseTmc(struct):
    cmd = 'TUX_CMD:EYES:CLOSE'
    return [cmd,]

# Sound play command structures
PLAY_FLASH_CANVAS = {'cmd' : 'sound_play', 'index' : 0, 'duration' : 0.0}
PLAY_WAVE_CANVAS = {'cmd' : 'wav_play', 'wav_name' : 'none', 'duration' : 0.0}

# Sound plus command types
SOUND_CMD_TYPES = {
    'Sound':
        [
            'sound_play',
            'wav_play',
        ],
}

# ------------------------------------------------------------------------------
# soundPlayTmc
# ------------------------------------------------------------------------------
def soundPlayTmc(struct):
    cmd = 'TUX_CMD:SOUND_FLASH:PLAY:%d,100.0' % struct['index']
    return [cmd,]

# ------------------------------------------------------------------------------
# wavPlayTmc
# ------------------------------------------------------------------------------
def wavPlayTmc(struct):
    return ["",]

# Spinning command structures
SPINNING_LEFT_CANVAS = {'cmd' : 'spinl_on', 'duration': 0.0, 'count' : 2,
    'speed': 5}
SPINNING_RIGHT_CANVAS = {'cmd' : 'spinr_on', 'duration': 0.0, 'count' : 2,
    'speed': 5}

# Spinning command types
SPINNING_CMD_TYPES = {
    'Spinning':
        [
            'spinl_on',
            'spinr_on',
        ],
}

# ------------------------------------------------------------------------------
# spinlOnTmc
# ------------------------------------------------------------------------------
def spinlOnTmc(struct):
    cmd = 'TUX_CMD:SPINNING:LEFT_ON:%d' % struct['count']
    return [cmd,]

# ------------------------------------------------------------------------------
# spinrOnTmc
# ------------------------------------------------------------------------------
def spinrOnTmc(struct):
    cmd = 'TUX_CMD:SPINNING:RIGHT_ON:%d' % struct['count']
    return [cmd,]

# TTS command structures
PLAY_TTS_CANVAS = {'cmd' : 'tts_play', 'text' : "Hello world", 'speaker' : 3,
    'pitch': 100, 'duration' : 0.0}

# TTS command types
TTS_CMD_TYPES = {
    'TTS':
        [
            'tts_play',
        ],
}

# TTS locutors list
LOCUTOR_NAMES_LIST = [
        "Bruno8k", "Julie8k", "Ryan8k", "Heather8k","Sofie8k",
        "Klaus8k", "Sarah8k", "Graham8k","Lucy8k", "Salma8k",
        "Mette8k", "Maria8k", "Chiara8k", "Femke8k", "Kari8k",
        "Celia8k", "Erik8k", "Emma8k"
]

# ------------------------------------------------------------------------------
# ttsPlayTmc
# ------------------------------------------------------------------------------
def ttsPlayTmc(struct):
    cmds = []
    locutor = LOCUTOR_NAMES_LIST[struct['speaker'] - 1]
    cmd = "OSL_CMD:TTS:SET_LOCUTOR:%s" % locutor
    cmds.append(cmd)
    cmd = "OSL_CMD:TTS:SET_PITCH:%d" % struct['pitch']
    cmds.append(cmd)
    struct['text'] = struct['text'].replace("\n", " ")
    cmd = "OSL_CMD:TTS:SPEAK:%s" % struct['text']
    cmds.append(cmd)
    return cmds

# Flippers command structures
FLIPPERS_ON_CANVAS = {'cmd' : 'wings_on', 'duration': 0.0, 'count' : 2}
FLIPPERS_UP_CANVAS = {'cmd' : 'wings_up', 'duration': 0.0}
FLIPPERS_DOWN_CANVAS = {'cmd' : 'wings_down', 'duration': 0.0}

# Flippers command types
FLIPPERS_CMD_TYPES = {
    'Wings':
        [
            'wings_on',
            'wings_up',
            'wings_down',
        ],
}

# ------------------------------------------------------------------------------
# flippersOnTmc
# ------------------------------------------------------------------------------
def flippersOnTmc(struct):
    cmd = 'TUX_CMD:FLIPPERS:ON:%d,NDEF' % struct['count']
    return [cmd,]

# ------------------------------------------------------------------------------
# flippersUpTmc
# ------------------------------------------------------------------------------
def flippersUpTmc(struct):
    cmd = 'TUX_CMD:FLIPPERS:UP'
    return [cmd,]

# ------------------------------------------------------------------------------
# flippersDownTmc
# ------------------------------------------------------------------------------
def flippersDownTmc(struct):
    cmd = 'TUX_CMD:FLIPPERS:DOWN'
    return [cmd,]

# Commands binding list
ATT_CMD_TO_MACRO_CMD_FUNCTS = {
    'leds_on' : ledsOnTmc,
    'ledl_on' : ledlOnTmc,
    'ledr_on' : ledrOnTmc,
    'leds_off' : ledsOffTmc,
    'ledl_off' : ledlOffTmc,
    'ledr_off' : ledrOffTmc,
    'leds_blink' : ledsBlinkTmc,
    'mouth_on' : mouthOnTmc,
    'mouth_open' : mouthOpenTmc,
    'mouth_close' : mouthCloseTmc,
    'eyes_on' : eyesOnTmc,
    'eyes_open' : eyesOpenTmc,
    'eyes_close' : eyesCloseTmc,
    'sound_play' : soundPlayTmc,
    'wav_play' : wavPlayTmc,
    'spinl_on' : spinlOnTmc,
    'spinr_on' : spinrOnTmc,
    'tts_play' : ttsPlayTmc,
    'wings_on' : flippersOnTmc,
    'wings_up' : flippersUpTmc,
    'wings_down' : flippersDownTmc,
}

# ------------------------------------------------------------------------------
# attCmdToMacroCmd
# ------------------------------------------------------------------------------
def attCmdToMacroCmd(struct):
    if struct['cmd'] in ATT_CMD_TO_MACRO_CMD_FUNCTS.keys():
        return ATT_CMD_TO_MACRO_CMD_FUNCTS[struct['cmd']](struct)
    else:
        return []
