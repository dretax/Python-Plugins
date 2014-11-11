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
        if vm * __DeathPortion__ < 0:
            DataStore.Add("iConomy", Vid, 0.0)
            return str((am * __KillPortion__) - am) + ":0"
        DataStore.Add("iConomy", Vid, vm * __DeathPortion__)
        return str((am * __KillPortion__) - am) + ":" + str(vm - (vm * __DeathPortion__))

    def GiveMoney(self, id, amount, Player = None, FromPlayer = None):
        if Player is not None and FromPlayer is None:
            Player.MessageFrom(__Sys__, "You magically found " + str(amount) + __MoneyMark__)
        elif Player is not None and FromPlayer is not None:
            Player.MessageFrom(__Sys__, "You got " + str(amount) + __MoneyMark__ + " from " + FromPlayer.Name)
        m = DataStore.Get("iConomy", id)
        DataStore.Add("iConomy", id, m + float(amount))

    def TakeMoney(self, id, amount, Player=None):
        m = DataStore.Get("iConomy", id)
        c = m - float(amount)
        if c < 0:
            return "Player would have negative money. Cancelling."
        if Player is not None:
            Player.MessageFrom(__Sys__, "You magically lost " + str(amount) + __MoneyMark__)
        DataStore.Add("iConomy", id, c)

    def SetMoney(self, id, amount, Player=None):
        m = DataStore.Get("iConomy", id)
        c = m - float(amount)
        if c < 0:
            return "Player would have negative money. Cancelling."
        if Player is not None:
            Player.MessageFrom(__Sys__, "Your balance magically changed to " + str(amount) + __MoneyMark__)
        DataStore.Add("iConomy", id, c)

    def GetMoney(self, id):
        return DataStore.Get("iConomy", id)


    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        V3.2
    """
    def CheckV(self, Player, args):
        systemname = "iConomy"
        p = self.GetPlayerName(String.Join(" ", args))
        if p is not None:
            return p

        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            for pl in Server.ActivePlayers:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            for pl in Server.ActivePlayers:
                if args.lower() in pl.Name.lower():
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
                return
            if len(args) > 0 and Player.Admin:
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                Player.MessageFrom(__Sys__, playerr.Name + " has " + str(self.GetMoney(playerr.SteamID)) + __MoneyMark__)
        elif cmd.cmd == "pay":
            if len(args) == 0:
                Player.MessageFrom(__Sys__, 'Usage: /pay "PlayerName" "amount"')
            elif len(args) > 0:
                playerr = self.CheckV(Player, qargs[0])
                if playerr is None:
                    return
                m = self.GetMoney(Player.SteamID)
                if m < float(qargs[1]):
                    Player.MessageFrom(__Sys__, "You can't pay more than you currently have.")
                    return
                self.GiveMoney(playerr.SteamID, qargs[1], playerr, Player)
                Player.MessageFrom(__Sys__, "You payed " + qargs[1] + __MoneyMark__  + " to " + playerr.Name)
        elif cmd.cmd == "takemoney":
            if len(args) == 0:
                Player.MessageFrom(__Sys__, 'Usage: /takemoney "PlayerName" "amount"')
            elif len(args) > 0:
                if Player.Admin:
                    playerr = self.CheckV(Player, qargs[0])
                    if playerr is None:
                        return
                    d = self.TakeMoney(playerr.SteamID, qargs[1], playerr)
                    if d is not None:
                        Player.MessageFrom(__Sys__, d)
                    Player.MessageFrom(__Sys__, "You took " + qargs[1] + __MoneyMark__  + " from " + playerr.Name)
        elif cmd.cmd == "setmoney":
            if len(args) == 0:
                Player.MessageFrom(__Sys__, 'Usage: /setmoney "PlayerName" "amount"')
            elif len(args) > 0:
                if Player.Admin:
                    playerr = self.CheckV(Player, qargs[0])
                    if playerr is None:
                        return
                    d = self.SetMoney(playerr.SteamID, qargs[1], playerr)
                    if d is not None:
                        Player.MessageFrom(__Sys__, d)
                    Player.MessageFrom(__Sys__, "You set " + playerr.Name + "'s balance to " + qargs[1] + __MoneyMark__)
        elif cmd.cmd == "givemoney":
            if len(args) == 0:
                Player.MessageFrom(__Sys__, 'Usage: /givemoney "PlayerName" "amount"')
            elif len(args) > 0:
                if Player.Admin:
                    playerr = self.CheckV(Player, qargs[0])
                    if playerr is None:
                        return
                    self.GiveMoney(playerr.SteamID, qargs[1], playerr)
                    Player.MessageFrom(__Sys__, "You gave " + qargs[1] + __MoneyMark__ + " to " + playerr.Name)

    def On_PlayerConnected(self, Player):
        sid = Player.SteamID
        if DataStore.Get("iConomy", sid) is None:
            DataStore.Add("iConomy", sid, __DefaultMoney__)
        Player.MessageFrom(__Sys__, "You have " + str(DataStore.Get("iConomy", sid)) + __MoneyMark__)

    def On_PlayerDied(self, PlayerDeathEvent):
        if PlayerDeathEvent.Attacker.ToPlayer() is None:
            return

        attacker = Server.GetPlayer(PlayerDeathEvent.Attacker)
        victim = PlayerDeathEvent.Victim
        aid = attacker.SteamID
        vid = victim.SteamID
        s = self.HandleMoney(aid, vid)
        s = s.split(':')
        attacker.MessageFrom(__Sys__, "You found " + str(s[0]) + __MoneyMark__)
        if int(s[1]) == 0:
            victim.MessageFrom(__Sys__, "You lost all.")
            return
        victim.MessageFrom(__Sys__, "You lost " + str(s[1]) + __MoneyMark__)