__author__ = 'DreTaX'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")

import Fougerite
import System
from System import *

Cooldown = {}
Detection = {}
# Seconds that must pass after a player's message before he can send another one.
FloodSeconds = 3


class AntiSpam:

    def On_Chat(self, Player, ChatEvent):
        if Player.UID not in Cooldown:
            Cooldown[Player.UID] = float(TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds)
        else:
            calc = float(TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds) - Cooldown[Player.UID]
            if calc < FloodSeconds:
                ChatEvent.NewText = "    "
                Player.Message("[color red]PLEASE DON'T SPAM")
                if Player.UID not in Detection.keys():
                    Detection[Player.UID] = 0
                Detection[Player.UID] = Detection[Player.UID] + 1
                if Detection[Player.UID] == 3:
                    Player.Disconnect()
                    Server.BroadcastNotice(Player.Name + " Has been auto kicked for spamming")
            else:
                Cooldown[Player.UID] = float(TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds)
                if Player.UID in Detection.keys():
                    Detection.pop(Player.UID)

    def On_PlayerDisconnected(self, Player):
        if Player.UID in Cooldown.keys():
            Cooldown.pop(Player.UID)
        if Player.UID in Detection.keys():
            Detection.pop(Player.UID)
