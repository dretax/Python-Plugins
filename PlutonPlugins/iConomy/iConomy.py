__author__ = 'DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import *

"""
    Class
"""

class iConomy:

    #Plugin Settings
    __MoneyMark__ = None
    __DefaultMoney__ = None
    __Sys__ = None
    #Player Settings!
    __MoneyMode__ = None
    __KillPortion__ = None
    __KillPortion2__ = None
    __DeathPortion__ = None
    __DeathPortion2__ = None

    def iConomy(self):
        if not Plugin.IniExists("iConomy"):
            ini = Plugin.CreateIni("iConomy")
            ini.AddSetting("Settings", "DefaultMoney", "100.0")
            ini.AddSetting("Settings", "MoneyMark", "$")
            ini.AddSetting("Settings", "Sysname", "[iConomy]")
            ini.AddSetting("PlayerKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("PlayerKillSettings", "KillPortion", "1.25")
            ini.AddSetting("PlayerKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("PlayerKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("PlayerKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("bearKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("bearKillSettings", "KillPortion", "1.25")
            ini.AddSetting("bearKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("bearKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("bearKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("stagKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("stagKillSettings", "KillPortion", "1.25")
            ini.AddSetting("stagKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("stagKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("stagKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("wolfKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("wolfKillSettings", "KillPortion", "1.25")
            ini.AddSetting("wolfKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("wolfKillSettings", "DeathPortion2", "4.0")
            ini.AddSetting("wolfKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("boarKillSettings", "PercentageOrExtra", "1")
            ini.AddSetting("boarKillSettings", "KillPortion", "1.25")
            ini.AddSetting("boarKillSettings", "DeathPortion", "0.75")
            ini.AddSetting("boarKillSettings", "KillPortion2", "5.0")
            ini.AddSetting("boarKillSettings", "DeathPortion2", "4.0")
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
        am = round(float(DataStore.Get("iConomy", Aid)), 2)
        vm = round(float(DataStore.Get("iConomy", Vid)), 2)
        if self.__MoneyMode__ == 0:
            return
        elif self.__MoneyMode__ == 1:
            if am == 0.0:
                amoney = round(float((am + 20.0) * self.__KillPortion__), 2)
            else:
                amoney = round(float(am * self.__KillPortion__), 2)
            vmoney = round(float(vm * self.__DeathPortion__), 2)
            DataStore.Add("iConomy", Aid, amoney)
            if vmoney < 0.0:
                DataStore.Add("iConomy", Vid, 0.0)
                return str(amoney - am) + ":0"
            DataStore.Add("iConomy", Vid, vmoney)
            return str(amoney - am) + ":" + str(vm - vmoney)
        else:
            amoney = round(float(am + self.__KillPortion2__), 2)
            vmoney = round(float(vm - self.__DeathPortion2__), 2)
            DataStore.Add("iConomy", Aid, amoney)
            if vmoney < 0.0:
                DataStore.Add("iConomy", Vid, 0.0)
                return str(self.__KillPortion2__) + ":0"
            DataStore.Add("iConomy", Vid, vmoney)
            return str(self.__KillPortion2__) + ":" + str(self.__DeathPortion2__)

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
        if c < 0.0:
            return 12
        if Player is not None:
            Player.MessageFrom(self.__Sys__, "You magically lost " + str(amount) + self.__MoneyMark__)
        DataStore.Add("iConomy", id, c)

    def SetMoney(self, id, amount, Player=None):
        if float(amount) < 0.0:
            return 12
        if Player is not None:
            Player.MessageFrom(self.__Sys__, "Your balance magically changed to " + str(amount) + self.__MoneyMark__)
        DataStore.Add("iConomy", id, float(amount))

    def GetMoney(self, id):
        m = DataStore.Get("iConomy", id)
        return float(m)


    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.0
    """
    def CheckV(self, Player, args):
        ini = self.iConomy()
        systemname = ini.GetSetting("Settings", "Sysname")
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
            s = str(args).lower()
            for pl in Server.ActivePlayers:
                if s in pl.Name.lower():
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

    def IsAnimal(self, String):
        s = String.replace('(Clone)', '')
        if s == 'stag' or s == 'wolf' or s == 'bear' or s == 'boar':
            return True
        return False

    def On_PluginInit(self):
        ini = self.iConomy()
        #Plugin Settings
        self.__MoneyMark__ = ini.GetSetting("Settings", "MoneyMark")
        self.__DefaultMoney__ = float(ini.GetSetting("Settings", "DefaultMoney"))
        self.__Sys__ = ini.GetSetting("Settings", "Sysname")
        #Player Settings!
        self.__MoneyMode__ = int(ini.GetSetting("PlayerKillSettings", "PercentageOrExtra"))
        self.__KillPortion__ = float(ini.GetSetting("PlayerKillSettings", "KillPortion"))
        self.__KillPortion2__ = float(ini.GetSetting("PlayerKillSettings", "KillPortion2"))
        self.__DeathPortion__ = float(ini.GetSetting("PlayerKillSettings", "DeathPortion"))
        self.__DeathPortion2__ = float(ini.GetSetting("PlayerKillSettings", "DeathPortion2"))

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
                if playerr.SteamID == Player.SteamID:
                    Player.MessageFrom(self.__Sys__, "You can't pay money to yourself.")
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
        elif cmd.cmd == "flushiconomy":
            if Player.Owner:
                DataStore.Flush('iConomy')
                Player.MessageFrom(self.__Sys__, "DataBase Flushed.")
                for p in Server.ActivePlayers:
                    DataStore.Add('iConomy', p.SteamID, self.__DefaultMoney__)
                    p.MessageFrom(self.__Sys__, "iConomy DataBase was Flushed.")


    def On_PlayerConnected(self, Player):
        sid = Player.SteamID
        if DataStore.Get("iConomy", sid) is None:
            DataStore.Add("iConomy", sid, self.__DefaultMoney__)
        Player.MessageFrom(self.__Sys__, "You have " + str(DataStore.Get("iConomy", sid)) + self.__MoneyMark__)

    def On_PlayerDied(self, PlayerDeathEvent):
        if PlayerDeathEvent.Attacker.ToPlayer() is None:
            if PlayerDeathEvent.Attacker.Name and self.IsAnimal(PlayerDeathEvent.Attacker.Name):
                name = PlayerDeathEvent.Attacker.Name
                name = name.replace('(Clone)', '')
                ini = self.iConomy()
                NMoneyMode = int(ini.GetSetting(name + "KillSettings", "PercentageOrExtra"))
                if NMoneyMode == 0:
                    return
                victim = PlayerDeathEvent.Victim
                NDeathPortion = float(ini.GetSetting(name + "KillSettings", "DeathPortion"))
                NDeathPortion2 = float(ini.GetSetting(name + "KillSettings", "DeathPortion2"))
                m = round(float(DataStore.Get("iConomy", victim.SteamID)), 2)
                if NMoneyMode == 1:
                    if m == 0.0:
                        m = 20.0
                    c = round(m * NDeathPortion, 2)
                    if c < 0.0:
                        DataStore.Add("iConomy", victim.SteamID, 0.0)
                        victim.MessageFrom(self.__Sys__, "You lost all the money you had.")
                        return
                    DataStore.Add("iConomy", victim.SteamID, c)
                    victim.MessageFrom(self.__Sys__, "You lost: " + str(c) + self.__MoneyMark__)
                else:
                    c = m - NDeathPortion2
                    if c < 0.0:
                        DataStore.Add("iConomy", victim.SteamID, 0.0)
                        victim.MessageFrom(self.__Sys__, "You lost all the money you had.")
                        return
                    DataStore.Add("iConomy", victim.SteamID, c)
                    victim.MessageFrom(self.__Sys__, "You lost: " + str(NDeathPortion2) + self.__MoneyMark__)
            return
        attacker = Server.GetPlayer(PlayerDeathEvent.Attacker)
        victim = PlayerDeathEvent.Victim
        aid = attacker.SteamID
        vid = victim.SteamID
        s = self.HandleMoney(aid, vid)
        s = s.split(':')
        attacker.MessageFrom(self.__Sys__, "You found " + str(s[0]) + self.__MoneyMark__)
        if float(s[1]) == 0.0:
            victim.MessageFrom(self.__Sys__, "You lost all the money you had.")
            return
        victim.MessageFrom(self.__Sys__, "You lost " + str(s[1]) + self.__MoneyMark__)

    def On_NPCKilled(self, NPCDeathEvent):
        NPC = NPCDeathEvent.Victim
        attacker = Server.GetPlayer(NPCDeathEvent.Attacker)
        ini = self.iConomy()
        name = NPC.Name
        name = name.replace('(Clone)', '')
        #NPC Settings
        NMoneyMode = int(ini.GetSetting(name + "KillSettings", "PercentageOrExtra"))
        if NMoneyMode == 0:
            return
        NKillPortion = float(ini.GetSetting(name + "KillSettings", "KillPortion"))
        NKillPortion2 = float(ini.GetSetting(name + "KillSettings", "KillPortion2"))
        Aid = round(float(DataStore.Get("iConomy", attacker.SteamID)), 2)
        if NMoneyMode == 1:
            n = None
            c = round(Aid * NKillPortion, 2)
            if Aid == 0.0:
                n = 20.0
                c = round(n * NKillPortion, 2)
            DataStore.Add("iConomy", attacker.SteamID, c)
            if n is not None:
               attacker.MessageFrom(self.__Sys__, "You received: " + str(c - Aid) + self.__MoneyMark__)
            else:
                attacker.MessageFrom(self.__Sys__, "You received: " + str(c - Aid) + self.__MoneyMark__)
        else:
            c = Aid + NKillPortion2
            DataStore.Add("iConomy", attacker.SteamID, c)
            attacker.MessageFrom(self.__Sys__, "You received: " + str(NKillPortion2) + self.__MoneyMark__)