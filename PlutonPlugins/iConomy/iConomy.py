__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import math
import System
from System import *

"""
    Class
"""
__MoneyMark__ = None
__KillPortion__ = None
__DeathPortion__ = None
__DefaultMoney__ = None
__Sys__ = None

class iConomy:
    def iConomy(self):
        if not Plugin.IniExists("iConomy"):
            ini = Plugin.CreateIni("iConomy")
            ini.AddSetting("Settings", "DefaultMoney", "100.0")
            ini.AddSetting("Settings", "MoneyMark", "$")
            ini.AddSetting("Settings", "KillPortion", "1.25")
            ini.AddSetting("Settings", "DeathPortion", "0.75")
            ini.AddSetting("Settings", "Sysname", "[iConomy]")
            ini.Save()
        return Plugin.GetIni("iConomy")

    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None

    """
        Economy Methods
    """

    def HandleMoney(self, Aid, Vid):
        am = DataStore.Get("iConomy", Aid)
        vm = DataStore.Get("iConomy", Vid)
        DataStore.Add("iConomy", Aid, am * __KillPortion__)
        DataStore.Add("iConomy", Vid, vm * __DeathPortion__)

    def GiveMoney(self, id, amount):
        m = DataStore.Get("iConomy", id)
        DataStore.Add("iConomy", id, m + float(amount))

    def TakeMoney(self, id, amount):
        m = DataStore.Get("iConomy", id)
        c = m - float(amount)
        if c < 0:
            return "Player would have negative money. Cancelling."
        DataStore.Add("iConomy", id, c)

    def GetMoney(self, id):
        return DataStore.Get("iConomy", id)


    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        V3.1
    """
    def CheckV(self, Player, args):
        systemname = "iConomy"
        p = self.GetPlayerName(String.Join(" ", args))
        if p is not None:
            return p

        count = 0
        for pl in Server.ActivePlayers:
            for namePart in args:
                if namePart.lower() in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, "Couldn't find " + String.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, "Found " + str(count) + " player with similar name. Use more correct name!")
            return None

    def On_PluginInit(self):
        ini = self.iConomy()
        __MoneyMark__ = ini.GetSetting("Settings", "MoneyMark")
        __KillPortion__ = float(ini.GetSetting("Settings", "KillPortion"))
        __DeathPortion__ = float(ini.GetSetting("Settings", "DeathPortion"))
        __DefaultMoney__ = float(ini.GetSetting("Settings", "DefaultMoney"))
        __Sys__ = ini.GetSetting("Settings", "Sysname")

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        qargs = cmd.quotedArgs
        if cmd.cmd == "money":
            if len(args) == 0:
                Player.MessageFrom(__Sys__, "You have " + str(self.GetMoney(Player.SteamID)) + __MoneyMark__)
            if len(args) > 0 and Player.Admin:
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                Player.MessageFrom(__Sys__, playerr.Name + " has " + str(self.GetMoney(playerr.SteamID)) + __MoneyMark__)

    def On_PlayerConnected(self, Player):
        sid = Player.SteamID
        if DataStore.Get("iConomy", sid) is None:
            DataStore.Add("iConomy", sid, __DefaultMoney__)


    def On_PlayerDied(self, PlayerDeathEvent):
        if PlayerDeathEvent.Attacker.ToPlayer() is None:
            return

        attacker = Server.GetPlayer(PlayerDeathEvent.Attacker)
        victim = PlayerDeathEvent.Victim
        aid = attacker.SteamID
        vid = victim.SteamID
        self.HandleMoney(aid, vid)