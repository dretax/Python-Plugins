__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import System
from System import *
import math

"""
    Class
"""

red = "[color #FF0000]"
green = "[color #009900]"
white = "[color #FFFFFF]"
DS = "Bambee"
Name = "BambeeProtector"

ProtectedPlayers = []

class BambeeProtector:

    """
        Methods
    """
    cooldown = None
    npcs = False

    def On_PluginInit(self):
        config = self.Config()
        self.cooldown = int(config.GetSetting("Settings", "Cooldown")) * 60000
        self.npcs = bool(config.GetSetting("Settings", "ProtectFromNpcs"))
        Util.ConsoleLog("BambeeProtector by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def Config(self):
        if not Plugin.IniExists("Config"):
            ini = Plugin.CreateIni("Config")
            ini.AddSetting("Settings", "Cooldown", "60")
            ini.AddSetting("Settings", "ProtectFromNpcs", "True")
            ini.Save()
        return Plugin.GetIni("Config")

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def TimeisUp(self, Player):
        id = Player.SteamID
        if (System.Environment.TickCount - DataStore.Get(DS, id)) >= self.cooldown:
            DataStore.Add(DS, id, False)
            ProtectedPlayers.remove(Player)
            Player.MessageFrom(Name, red + "You lost your protection. Time is over.")
            return True
        return False

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Victim is not None:
            if not HurtEvent.AttackerIsPlayer and self.npcs and HurtEvent.Victim in ProtectedPlayers:
                if not self.TimeisUp(HurtEvent.Victim):
                    HurtEvent.DamageAmount = 0
                    return
            if HurtEvent.AttackerIsPlayer:
                if HurtEvent.Victim in ProtectedPlayers:
                    if self.TimeisUp(HurtEvent.Victim):
                        return
                    HurtEvent.DamageAmount = 0
                    HurtEvent.Attacker.MessageFrom(Name, red + HurtEvent.Victim.Name + " is under protection")
                if HurtEvent.Attacker in ProtectedPlayers:
                    HurtEvent.DamageAmount = 0
                    HurtEvent.Attacker.MessageFrom(Name, red + "You cannot attack people while you are under protection")

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay \
                and HurtEvent.DamageType is not None:
            if not HurtEvent.AttackerIsPlayer:
                return
            if HurtEvent.DamageType == "Explosion" and HurtEvent.Attacker in ProtectedPlayers:
                HurtEvent.DamageAmount = 0
                HurtEvent.Attacker.MessageFrom(Name, red + "You cannot use c4/grenade under protection")

    def GiveProtection(self, Player):
        id = Player.SteamID
        if DataStore.ContainsKey(DS, id):
            time = DataStore.Get(DS, id)
            if not bool(time):
                return
            calc = System.Environment.TickCount - time
            if calc < 0 or math.isnan(calc):
                Player.MessageFrom(Name, red + "Your protection is off.")
                DataStore.Add(DS, id, False)
                return
            if calc >= self.cooldown :
                ProtectedPlayers.append(Player)
                done = str(round((time / 1000) / 60, 2))
                done2 = str(round((self.cooldown / 1000) / 60, 2))
                Player.MessageFrom(Name, green + "You still have protection. " + done + " passed of " + done2 + " minutes")
                Player.MessageFrom(Name, green + "You can disable this by typing /protectionoff")
                return
            DataStore.Add(DS, id, False)
        done2 = str(round((self.cooldown / 1000) / 60, 2))
        DataStore.Add(DS, id, System.Environment.TickCount)
        ProtectedPlayers.append(Player)
        Player.MessageFrom(Name, green + "You are a new player! You got " + done2 + " minute(s) kill protection.")
        Player.MessageFrom(Name, green + "You can't kill anyone.")
        Player.MessageFrom(Name, green + "You can disable this by typing /protectionoff")

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        self.GiveProtection(Player)

    def On_PlayerDisconnected(self, Player):
        if Player in ProtectedPlayers:
            ProtectedPlayers.remove(Player)

    def On_Command(self, Player, cmd, args):
        if cmd == "protectionoff":
            if Player in ProtectedPlayers:
                ProtectedPlayers.remove(Player)
                DataStore.Add(DS, Player.SteamID, False)
                Player.MessageFrom(Name, "Protection disabled.")
                return
            Player.MessageFrom(Name, "You aren't protected.")
        elif cmd == "resetprotection":
            if Player.Admin or self.isMod(Player.SteamID):
                DataStore.Flush(DS)
                Player.MessageFrom(Name, "Flushed!")