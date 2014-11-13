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

class iConomy:

    __MoneyMark__ = None
    __KillPortion__ = None
    __DeathPortion__ = None
    __DefaultMoney__ = None
    __Sys__ = None

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
        am = float(DataStore.Get("iConomy", Aid))
        vm = float(DataStore.Get("iConomy", Vid))
        DataStore.Add("iConomy", Aid, am * self.__KillPortion__)
        if vm * self.__DeathPortion__ < 0:
            DataStore.Add("iConomy", Vid, 0.0)
            return str((am * self.__KillPortion__) - am) + ":0"
        DataStore.Add("iConomy", Vid, vm * self.__DeathPortion__)
        return str((am * self.__KillPortion__) - am) + ":" + str(vm - (vm * self.__DeathPortion__))

    def GiveMoney(self, id, amount, Player = None, FromPlayer = None):
        if Player is not None and FromPlayer is None:
            Player.MessageFrom(self.__Sys__, "You magically found " + str(amount) + self.__MoneyMark__)
        elif Player is not None and FromPlayer is not None:
            Player.MessageFrom(self.__Sys__, "You got " + str(amount) + self.__MoneyMark__ + " from " + FromPlayer.Name)
        m = float(self.GetMoney(id))
        DataStore.Add("iConomy", id, m + float(amount))

    def TakeMoney(self, id, amount, Player=None):
        m = float(DataStore.Get("iConomy", id))
        c = m - float(amount)
        if c < 0:
            return 12
        if Player is not None:
            Player.MessageFrom(self.__Sys__, "You magically lost " + str(amount) + self.__MoneyMark__)
        DataStore.Add("iConomy", id, c)

    def SetMoney(self, id, amount, Player=None):
        if float(amount) < 0:
            return 12
        if Player is not None:
            Player.MessageFrom(self.__Sys__, "Your balance magically changed to " + str(amount) + self.__MoneyMark__)
        DataStore.Add("iConomy", id, float(amount))

    def GetMoney(self, id):
        return DataStore.Get("iConomy", id)


    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.0
    """
    def CheckV(self, Player, args):
        systemname = "iConomy"
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(String.Join(" ", args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            p = self.GetPlayerName(str(args))
            if p is not None:
                return p
            for pl in Server.ActivePlayers:
                if str(args).lower() in pl.Name.lower():
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
        self.__MoneyMark__ = ini.GetSetting("Settings", "MoneyMark")
        self.__KillPortion__ = float(ini.GetSetting("Settings", "KillPortion"))
        self.__DeathPortion__ = float(ini.GetSetting("Settings", "DeathPortion"))
        self.__DefaultMoney__ = float(ini.GetSetting("Settings", "DefaultMoney"))
        self.__Sys__ = ini.GetSetting("Settings", "Sysname")

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        qargs = cmd.quotedArgs
        if cmd.cmd == "money":
            if len(args) == 0:
                m = self.GetMoney(Player.SteamID)
                Player.MessageFrom(self.__Sys__, "You have " + str(m) + self.__MoneyMark__)
                return
            if len(args) > 0 and Player.Admin:
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                Player.MessageFrom(self.__Sys__, playerr.Name + " has " + str(self.GetMoney(playerr.SteamID)) + self.__MoneyMark__)
        elif cmd.cmd == "pay":
            if len(args) == 0:
                Player.MessageFrom(self.__Sys__, 'Usage: /pay "PlayerName" "amount"')
            elif len(args) > 0:
                playerr = self.CheckV(Player, qargs[0])
                if playerr is None:
                    return
                m = self.GetMoney(Player.SteamID)
                if m < float(qargs[1]):
                    Player.MessageFrom(self.__Sys__, "You can't pay more than you currently have.")
                    return
                self.GiveMoney(playerr.SteamID, qargs[1], playerr, Player)
                self.TakeMoney(Player.SteamID, qargs[1])
                Player.MessageFrom(self.__Sys__, "You payed " + qargs[1] + self.__MoneyMark__  + " to " + playerr.Name)
        elif cmd.cmd == "takemoney":
            if len(args) == 0:
                Player.MessageFrom(self.__Sys__, 'Usage: /takemoney "PlayerName" "amount"')
            elif len(args) > 0:
                if Player.Admin:
                    playerr = self.CheckV(Player, qargs[0])
                    if playerr is None:
                        return
                    d = self.TakeMoney(playerr.SteamID, qargs[1], playerr)
                    if d == 12:
                        Player.MessageFrom(self.__Sys__, "Player would have negative money. Cancelling.")
                        return
                    Player.MessageFrom(self.__Sys__, "You took " + qargs[1] + self.__MoneyMark__  + " from " + playerr.Name)
        elif cmd.cmd == "setmoney":
            if len(args) == 0:
                Player.MessageFrom(self.__Sys__, 'Usage: /setmoney "PlayerName" "amount"')
            elif len(args) > 0:
                if Player.Admin:
                    playerr = self.CheckV(Player, qargs[0])
                    if playerr is None:
                        return
                    d = self.SetMoney(playerr.SteamID, qargs[1], playerr)
                    if d == 12:
                        Player.MessageFrom(self.__Sys__, "Player would have negative money. Cancelling.")
                        return
                    Player.MessageFrom(self.__Sys__, "You set " + playerr.Name + "'s balance to " + qargs[1] + self.__MoneyMark__)
        elif cmd.cmd == "givemoney":
            if len(args) == 0:
                Player.MessageFrom(self.__Sys__, 'Usage: /givemoney "PlayerName" "amount"')
            elif len(args) > 0:
                if Player.Admin:
                    playerr = self.CheckV(Player, qargs[0])
                    if playerr is None:
                        return
                    self.GiveMoney(playerr.SteamID, qargs[1], playerr)
                    Player.MessageFrom(self.__Sys__, "You gave " + qargs[1] + self.__MoneyMark__ + " to " + playerr.Name)

    def On_PlayerConnected(self, Player):
        sid = Player.SteamID
        if DataStore.Get("iConomy", sid) is None:
            DataStore.Add("iConomy", sid, self.__DefaultMoney__)
        Player.MessageFrom(self.__Sys__, "You have " + str(DataStore.Get("iConomy", sid)) + self.__MoneyMark__)

    def On_PlayerDied(self, PlayerDeathEvent):
        if PlayerDeathEvent.Attacker.ToPlayer() is None:
            return

        attacker = Server.GetPlayer(PlayerDeathEvent.Attacker)
        victim = PlayerDeathEvent.Victim
        aid = attacker.SteamID
        vid = victim.SteamID
        s = self.HandleMoney(aid, vid)
        s = s.split(':')
        attacker.MessageFrom(self.__Sys__, "You found " + str(s[0]) + self.__MoneyMark__)
        if int(s[1]) == 0:
            victim.MessageFrom(self.__Sys__, "You lost everything.")
            return
        victim.MessageFrom(self.__Sys__, "You lost " + str(s[1]) + self.__MoneyMark__)