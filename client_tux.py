import time

from tuxisalive.api import *

# ----------------------
# soundFlash definitions
# ----------------------
#  1    snoring
#  2    fart, oops
#  3    yummy
#  4    hello
#  5    ready
#  6    yo!
#  7    you're talking to me?
#  8    ha ha ha laughing
#  9    plop
# 10    glass
# 11    tick
# 12    bong (soft)
# 13    boink (up)
# 14    red alert
# 15    swoosh
# 16    boink (down)
# 17    coo clock
# ----------------------

class Client:
    HTTP_SERVER = "127.0.0.1"
    HTTP_PORT = 54321

    def __init__(self):
        self.__client = TuxAPI(Client.HTTP_SERVER, Client.HTTP_PORT)

    def get_tux(self):
        self.__client.server.autoConnect(CLIENT_LEVEL_RESTRICTED, 'TuxGuestUser', 'TuxPass')
        time.sleep(1.0)

        return self.__client
