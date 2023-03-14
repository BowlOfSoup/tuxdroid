# -*- coding: utf8 -*-

from client_tux import Client
from logger import Logger
import time
import sys

class Main:
    TITLE = '''
    ▄▄▄▄▄▄• ▄▌▐▄• ▄     ·▄▄▄▄  ▄▄▄        ▪  ·▄▄▄▄  
    •██  █▪██▌ █▌█▌▪    ██▪ ██ ▀▄ █·▪     ██ ██▪ ██ 
     ▐█.▪█▌▐█▌ ·██·     ▐█· ▐█▌▐▀▀▄  ▄█▀▄ ▐█·▐█· ▐█▌
     ▐█▌·▐█▄█▌▪▐█·█▌    ██. ██ ▐█•█▌▐█▌.▐▌▐█▌██. ██ 
     ▀▀▀  ▀▀▀ •▀▀ ▀▀    ▀▀▀▀▀• .▀  ▀ ▀█▄▀▪▀▀▀▀▀▀▀▀• 
    '''

    def __init__(self):
        print("\033[33m" + self.TITLE + "\033[0m")

        client_tux = Client()
        self.__tux = client_tux.get_tux()
        self.__logger = Logger()

        if not self.__tux.server.getConnected():
            self.__logger.error("Tux HTTP server not up!")
            quit()

    def boot(self):
        if len(sys.argv) < 2:
            self.__logger.error("Please provide an action.")
            quit()

        action = sys.argv[1]
        if action == "alert":
            self.__action_alert()
        elif action == "poop":
            self.__action_poop()
        else:
            self.__logger.error("Invalid action provided.")

        self.__tux_reset()
        self.__deconstruct()

    def __tux_sound(self, number):
        self.__tux.soundFlash.play(number)
        time.sleep(0.5)

    def __tux_flippers(self, amount):
        time.sleep(0.5)
        self.__tux.flippers.on(amount)

    def __tux_reset(self):
        time.sleep(1.0)
        self.__tux.flippers.down()
        self.__tux.led.both.off()

    def __action_alert(self):
        self.__tux.led.both.blinkAsync(2, 14)
        self.__tux_flippers(4)
        self.__tux_sound(14)
        self.__tux_sound(14)
        self.__tux_sound(14)
        self.__tux_flippers(4)

    def __action_poop(self):
        self.__tux.led.both.on()
        time.sleep(0.5)
        self.__tux.flippers.up()
        time.sleep(0.5)

        self.__tux.eyes.close()

        time.sleep(1.0)
        self.__tux_sound(9)

        self.__tux.eyes.open()
        time.sleep(0.5)
        self.__tux.mouth.open()
        time.sleep(0.5)

        self.__tux_sound(8)
        self.__tux.mouth.close()

    def __deconstruct(self):
        self.__tux.destroy()
        quit()

main = Main()
main.boot()