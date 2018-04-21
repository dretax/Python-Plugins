__author__ = 'DreTaX'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")

import Fougerite
import System
from System import *

Cooldown = {}
# Seconds that must pass after a player's message before he can send another one.
FloodSeconds = 2

class AntiSpam:

    def On_Chat(self, Player, ChatEvent):
        if Player.UID not in Cooldown:
            Cooldown[Player.UID] = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds
        else:
            calc = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds - Cooldown[Player.UID]
            if calc < FloodSeconds:
                ChatEvent.NewText = "    "
                Player.Message("WAIT A BIT BEFORE SENDING ANOTHER MESSAGE...")
            else:
                Cooldown[Player.UID] = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds

    def On_PlayerDisconnected(self, Player):
        if Player.UID in Cooldown.keys():
            Cooldown.pop(Player.UID)
