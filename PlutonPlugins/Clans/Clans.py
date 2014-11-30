__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import String

class Clans:

    """
        Clan Methods.
    """

    def ClansConfig(self):
        if not Plugin.IniExists("ClansConfig"):
            ini = Plugin.CreateIni("ClansConfig")
            ini.AddSetting("Settings", "Sys", "[Clans]")
            ini.Save()
        return Plugin.GetIni("ClansConfig")

    def Clans(self):
        if not Plugin.IniExists("Clans"):
            ini = Plugin.CreateIni("Clans")
            ini.Save()
        return Plugin.GetIni("Clans")

    def HasClan(self, ID):
        ini = self.Clans()
        if ini.GetSetting("ClanMembers", ID) is not None \
            or ini.GetSetting("ClanOfficers", ID) is not None \
            or ini.GetSetting("ClanOwners", ID) is not None:
                return True
        return False

    def GetClanMember(self, Clan, ID):
        ini = self.Clans()
        if ini.GetSetting(Clan, ID) is not None:
            return ini.GetSetting(Clan, ID)
        return None

    def GetClanOfPlayer(self, ID):
        ini = self.Clans()
        if ini.GetSetting("ClanMembers", ID) is not None:
            return ini.GetSetting("ClanMembers", ID)
        if ini.GetSetting("ClanOfficers", ID) is not None:
            return ini.GetSetting("ClanOfficers", ID)
        if ini.GetSetting("ClanOwners", ID) is not None:
            return ini.GetSetting("ClanOwners", ID)
        return None

    def GetAllOnlinePlayersOfClan(self, Clan):
        ini = self.Clans()
        sec = ini.EnumSection(Clan)
        ids = []
        Members = []
        for id in sec:
            ids.append(id)
        for player in Server.ActivePlayers:
            if player.GameID in ids:
                Members.append(player)
        return Members

    def GetClanPopulation(self, Clan):
        ini = self.Clans()
        return len(ini.EnumSection(Clan))

    def GetClanRank(self, ID):
        ini = self.Clans()
        if ini.GetSetting("ClanMembers", ID) is not None:
            return 1
        if ini.GetSetting("ClanOfficers", ID) is not None:
            return 2
        if ini.GetSetting("ClanOwners", ID) is not None:
            return 3
        return None

    def CreateClan(self, Clan, ID, Name):
        ini = self.Clans()
        ini.AddSetting(Clan, ID, Name)
        ini.AddSetting("ClanOwners", ID, Name)
        ini.Save()

    def DeleteClan(self, Clan):
        ini = self.Clans()
        ini.DeleteSetting(Clan)
        sec = ini.EnumSection("ClanMembers")
        sec2 = ini.EnumSection("ClanOwners")
        sec3 = ini.EnumSection("ClanOfficers")
        for p in sec:
            n = ini.GetSetting("ClanMembers", p)
            if n == Clan:
                ini.DeleteSetting("ClanMembers", p)
        for p in sec2:
            n = ini.GetSetting("ClanOwners", p)
            if n == Clan:
                ini.DeleteSetting("ClanOwners", p)
        for p in sec3:
            n = ini.GetSetting("ClanOfficers", p)
            if n == Clan:
                ini.DeleteSetting("ClanOfficers", p)
        ini.Save()

    def AddPlayerToClan(self, Clan, ID, Name, Rank = None):
        ini = self.Clans()
        ini.AddSetting(Clan, ID, Name)
        if Rank == 1 or Rank == None:
            ini.AddSetting("ClanMembers", ID, Name)
        elif Rank == 2:
            ini.AddSetting("ClanOfficers", ID, Name)
        elif Rank == 3:
            ini.AddSetting("ClanOwners", ID, Name)
        ini.Save()

    def PromotePlayer(self, ID):
        ini = self.Clans()
        cur = self.GetClanRank(ID)
        if cur == 1:
            ini.DeleteSetting("ClanMembers", ID)
            ini.AddSetting("ClanOfficers", ID)
        elif cur == 2:
            ini.DeleteSetting("ClanOfficers", ID)
            ini.AddSetting("ClanOwners", ID)
        else:
            return
        ini.Save()

    def DemotePlayer(self, ID):
        ini = self.Clans()
        cur = self.GetClanRank(ID)
        if cur == 2:
            ini.DeleteSetting("ClanOfficers", ID)
            ini.AddSetting("ClanMembers", ID)
        elif cur == 3:
            ini.DeleteSetting("ClanOwners", ID)
            ini.AddSetting("ClanOfficers", ID)
        else:
            return
        ini.Save()

    def RemovePlayerFromClan(self, Clan, ID):
        ini = self.Clans()
        rank = self.GetClanRank(ID)
        if rank == 1:
            ini.DeleteSetting(Clan, ID)
            ini.DeleteSetting("ClanMembers", ID)
        elif rank == 2:
            ini.DeleteSetting(Clan, ID)
            ini.DeleteSetting("ClanOfficers", ID)
        elif rank == 3:
            ini.DeleteSetting(Clan, ID)
            ini.DeleteSetting("ClanOwners", ID)
        ini.Save()

    def GetClanMembers(self, Clan):
        ini = self.Clans()
        sec = ini.EnumSection(Clan)
        s = ""
        for m in sec:
            s = s + m +", "
        return s

    def IsPending(self, id):
        if DataStore.ContainsKey("Clans", id):
            return True
        return False

    def SendPrivateMessage(self, Clan, FromPlayer, Message):
        online = self.GetAllOnlinePlayersOfClan(Clan)
        for pl in online:
            if pl is not None:
                pl.MessageFrom(Clan, FromPlayer + " -> " + Message)

    def MakePending(self, id, idinviter):
        DataStore.Add("Clans", id, idinviter)

    def ClansAutoKillCallback(self, timer):
        timer.Kill()
        ini = self.ClansConfig()
        sys = ini.GetSetting("Settings", "Sys")
        autokill = timer.Args
        if not self.IsPending(autokill["PlayerT"]):
            return
        DataStore.Remove("Clans", autokill["PlayerT"])
        PlayerFrom = Server.FindPlayer(autokill["PlayerR"])
        PlayerP = Server.FindPlayer(autokill["PlayerT"])
        if PlayerFrom is None or PlayerP is None:
            return
        PlayerFrom.MessageFrom(sys, "Request timed out.")
        PlayerP.MessageFrom(sys, "Request timed out.")

    def GetPlayerName(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None


    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.0
    """
    def CheckV(self, Player, args):
        ini = self.ClansConfig()
        systemname = ini.GetSetting("Settings", "Sys")
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

    """
        Events/Methods.
    """

    def On_PlayerConnected(self, Player):
        if self.HasClan(Player.GameID):
            clan = self.GetClanOfPlayer(Player.GameID)
            name = Player.Name
            Player.basePlayer.displayName = "[" + clan + "] " + name

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.quotedArgs
        command = cmd.cmd
        cfg = self.ClansConfig()
        sys = cfg.GetSetting("Settings", "Sys")
        if command == "chelp":
            Player.MessageFrom(sys, "TClans Created by " + __author__ + " V" + __version__)
            #todo: ......
        elif command == "ccreate":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /ccreate clanname")
                return
            id = Player.GameID
            if self.HasClan(id):
                Player.MessageFrom(sys, "You already have a clan. Leave first.")
                return
            self.CreateClan(args, id, str(Player.Name))
            Server.BroadcastFrom(sys, args + " got created by " + Player.Name)
            Player.MessageFrom(sys, "You created your first clan! /cinvite playername to invite!")
        elif command == "cinvite":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cinvite playername")
                return
            id = Player.GameID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            if self.GetClanRank(id) == 1:
                Player.MessageFrom(sys, "You must be an officer or an owner to do this.")
                return
            playerr = self.CheckV(Player, args)
            if playerr is None:
                return
            if self.HasClan(playerr.GameID):
                Player.MessageFrom(sys, "This player has a clan.")
                return
            if self.IsPending(playerr.GameID):
                Player.MessageFrom(sys, "This player is pending a request. Try after a few seconds.")
                return
            clan = self.GetClanOfPlayer(id)
            self.MakePending(playerr.GameID, id)
            playerr.MessageFrom(sys, "Clan " + clan + " invited you to join their forces!")
            playerr.MessageFrom(sys, "Type /cjoin to accept or /cdeny to deny! You have 40 seconds to accept.")
            autokill = Plugin.CreateDict()
            autokill["PlayerR"] = Player.GameID
            autokill["PlayerT"] = playerr.GameID
            Plugin.CreateParallelTimer("ClansAutoKill", 1000 * 40, autokill).Start()
        elif command == "cdeny":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cdeny")
                return
            id = Player.GameID
            if not self.IsPending(id):
                Player.MessageFrom(sys, "You aren't pending any requests!")
                return
            inviterid = DataStore.Get("Clans", id)
            inviter = Server.FindPlayer(inviterid)
            DataStore.Remove("Clans", id)
            inviter.MessageFrom(sys, Player.Name + "  Denied the request!")
            Player.MessageFrom(sys, "You denied the request!")
        elif command == "cjoin":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cjoin")
                return
            id = Player.GameID
            if self.HasClan(id):
                Player.MessageFrom(sys, "You already have a clan!")
                return
            if not self.IsPending(id):
                Player.MessageFrom(sys, "You aren't pending any requests!")
                return
            inv = DataStore.Get("Clans", id)
            clan = self.GetClanOfPlayer(inv)
            self.AddPlayerToClan(clan, id, str(Player.Name))
            online = self.GetAllOnlinePlayersOfClan(clan)
            for pl in online:
                if pl is not None:
                    pl.MessageFrom(sys, Player.Name + " joined to the clan!")
        elif command == "cm":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cm message")
                return
            name = str(Player.Name)
            id = Player.GameID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            clan = self.GetClanOfPlayer(id)
            self.SendPrivateMessage(clan, name, args)
        #Todo: Finish the other commands.