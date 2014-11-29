__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import *

"""
    Class
"""

class PlayerList:

    def On_Command(self, cmd):
        Player = cmd.User
        if cmd.cmd == "players":
            all = ""
            for pl in Server.ActivePlayers:
                all = all + str(pl.Name) + ", "
            Player.MessageFrom("Online Players", all)