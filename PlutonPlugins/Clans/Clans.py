__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import *
import sys
import re
path = Util.GetPublicFolder()
Lib = True
try:
    sys.path.append(path + "\\Python\\Lib\\")
    import hashlib
except ImportError:
    Lib = False
import datetime

class Clans:

    """
        Clan Methods.
    """

    def ClansConfig(self):
        if not Plugin.IniExists("ClansConfig"):
            ini = Plugin.CreateIni("ClansConfig")
            ini.AddSetting("Settings", "Sys", "[Clans]")
            ini.AddSetting("Settings", "Cost", "0")
            ini.Save()
        return Plugin.GetIni("ClansConfig")

    def Clans(self):
        if not Plugin.IniExists("Clans"):
            ini = Plugin.CreateIni("Clans")
            ini.Save()
        return Plugin.GetIni("Clans")

    def ClanInfo(self):
        if not Plugin.IniExists("ClanInfo"):
            ini = Plugin.CreateIni("ClanInfo")
            ini.Save()
        return Plugin.GetIni("ClanInfo")

    def HasClan(self, ID):
        ini = self.Clans()
        if ini.ContainsSetting("ClanMembers", ID) or ini.ContainsSetting("ClanOfficers", ID) or ini.ContainsSetting("ClanOwners", ID) or ini.ContainsSetting("ClanCoOwners", ID):
            return True
        else:
            return False

    def GetClanMember(self, Clan, ID):
        ini = self.Clans()
        if ini.GetSetting(Clan, ID) is not None:
            return ini.GetSetting(Clan, ID)
        return None

    def GetClanOfPlayer(self, ID):
        ini = self.Clans()
        if ini.ContainsSetting("ClanMembers", ID):
            return ini.GetSetting("ClanMembers", ID)
        if ini.ContainsSetting("ClanOfficers", ID):
            return ini.GetSetting("ClanOfficers", ID)
        if ini.ContainsSetting("ClanOwners", ID):
            return ini.GetSetting("ClanOwners", ID)
        if ini.ContainsSetting("ClanCoOwners", ID):
            return ini.GetSetting("ClanCoOwners", ID)
        return None

    def GetAllOnlinePlayersOfClan(self, Clan):
        ini = self.Clans()
        sec = ini.EnumSection(Clan)
        ids = []
        for id in sec:
            ids.append(id)
        return ids

    def GetClanPopulation(self, Clan):
        ini = self.Clans()
        try:
            return len(ini.EnumSection(Clan))
        except:
            return None

    def GetClanRank(self, ID):
        ini = self.Clans()
        if ini.ContainsSetting("ClanMembers", ID):
            return 1
        if ini.ContainsSetting("ClanOfficers", ID):
            return 2
        if ini.ContainsSetting("ClanCoOwners", ID):
            return 3
        if ini.ContainsSetting("ClanOwners", ID):
            return 4
        return None

    def TranslateToRank(self, Number):
        if Number == 1:
            return "Member"
        elif Number == 2:
            return "Officer"
        elif Number == 3:
            return "Co-Owner"
        elif Number == 4:
            return "Owner"

    def CreateClan(self, Clan, ID, Name):
        ini = self.Clans()
        claninfo = self.ClanInfo()
        now = datetime.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M")
        ini.AddSetting(Clan, ID, Name)
        ini.AddSetting("ClanOwners", ID, Clan)
        ini.Save()
        claninfo.AddSetting("ClanInfo" + Clan, "Creation", str(t))
        claninfo.AddSetting("ClanInfo" + Clan, "Owner", Name)
        claninfo.Save()
        #Todo: More to come.

    def DeleteClan(self, Clan):
        cfg = self.ClansConfig()
        ini = self.Clans()
        sys = cfg.GetSetting("Settings", "Sys")
        online = self.GetAllOnlinePlayersOfClan(Clan)
        for player in Server.ActivePlayers:
            if player.SteamID in online:
                player.MessageFrom(sys, "Your clan was disbanded.")
        enum = ini.EnumSection(Clan)
        for d in enum:
            ini.DeleteSetting(Clan, d)
        sec = ini.EnumSection("ClanMembers")
        sec2 = ini.EnumSection("ClanOwners")
        sec3 = ini.EnumSection("ClanOfficers")
        sec4 = ini.EnumSection("ClanCoOwners")
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
        for p in sec4:
            n = ini.GetSetting("ClanCoOwners", p)
            if n == Clan:
                ini.DeleteSetting("ClanCoOwners", p)
        ini.Save()

    def AddPlayerToClan(self, Clan, ID, Name, Rank = None):
        ini = self.Clans()
        ini.AddSetting(Clan, ID, Name)
        if Rank == 1 or Rank == None:
            ini.AddSetting("ClanMembers", ID, Clan)
        elif Rank == 2:
            ini.AddSetting("ClanOfficers", ID, Clan)
        elif Rank == 3:
            ini.AddSetting("ClanCoOwners", ID, Clan)
        elif Rank == 4:
            ini.AddSetting("ClanOwners", ID, Clan)
        ini.Save()
        claninfo = self.ClanInfo()
        now = datetime.datetime.now()
        t = now.strftime("%Y-%m-%d %H:%M")
        claninfo.AddSetting("ClanInfo" + Clan, "Join" + ID, str(t))
        claninfo.Save()

    def PromotePlayer(self, ID):
        ini = self.Clans()
        cur = self.GetClanRank(ID)
        if cur == 1:
            ini.DeleteSetting("ClanMembers", ID)
            ini.AddSetting("ClanOfficers", ID)
        elif cur == 2:
            ini.DeleteSetting("ClanOfficers", ID)
            ini.AddSetting("ClanCoOwners", ID)
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
            ini.DeleteSetting("ClanCoOwners", ID)
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
            ini.DeleteSetting("ClanCoOwners", ID)
        elif rank == 4:
            ini.DeleteSetting(Clan, ID)
            ini.DeleteSetting("ClanOwners", ID)
        ini.Save()

    def GetClanMembers(self, Clan):
        ini = self.Clans()
        sec = ini.EnumSection(Clan)
        s = ""
        for m in sec:
            g = ini.GetSetting(Clan, m)
            s = s + g +", "
        return s

    def IsPending(self, id):
        if DataStore.ContainsKey("Clans", id):
            return True
        return False

    def SendPrivateMessage(self, Clan, FromPlayer, Message):
        online = self.GetAllOnlinePlayersOfClan(Clan)
        for player in Server.ActivePlayers:
            if player.SteamID in online:
                player.MessageFrom("[" + Clan + "]", FromPlayer + " -> " + Message)

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
        Economy Methods
    """

    def GetMoney(self, id):
        m = DataStore.Get("iConomy", id)
        return float(m)

    def TakeMoney(self, id, amount, Player=None):
        sys = DataStore.Get("iConomy", "SysName")
        mark = DataStore.Get("iConomy", "MoneyMark")
        m = float(DataStore.Get("iConomy", id))
        c = m - float(amount)
        if c < 0.0:
            return 12
        if Player is not None:
            Player.MessageFrom(sys, "You magically lost " + str(amount) + mark)
        DataStore.Add("iConomy", id, c)

    """
        Events/Methods.
    """

    def On_PlayerConnected(self, Player):
        if self.HasClan(Player.SteamID):
            clan = self.GetClanOfPlayer(Player.SteamID)
            name = Player.Name
            #Player.basePlayer.displayName = "[" + clan + "] " + name
            Player.basePlayer.name = "[" + clan + "] " + name
            claninfo = self.ClanInfo()
            if claninfo.ContainsSetting("ClanInfo" + clan, "Motd"):
                motd = claninfo.GetSetting("ClanInfo" + clan, "Motd")
                Player.MessageFrom(clan, motd)


    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        qargs = cmd.quotedArgs
        command = cmd.cmd
        cfg = self.ClansConfig()
        claninfo = self.ClanInfo()
        sys = cfg.GetSetting("Settings", "Sys")
        if command == "chelp":
            Player.MessageFrom(sys, "Clans Created by " + __author__ + " V" + __version__)
            Player.MessageFrom(sys, "Type the commands in for more info.")
            Player.MessageFrom(sys, "/crankpw - Sets Clan Recovery password for owners")
            Player.MessageFrom(sys, "/cloginpw - Adds you back to owner, If you lost your powers.")
            Player.MessageFrom(sys, "/ccreate - Creates you a clan.")
            Player.MessageFrom(sys, "/cinvite - Invites player to the clan")
            Player.MessageFrom(sys, "/cdeny - Denies Invitation (Auto Deny: 40 secs)")
            Player.MessageFrom(sys, "/cjoin - Accept the invitation")
            Player.MessageFrom(sys, "/clist - Lists all the clans")
            Player.MessageFrom(sys, "/cinfo - Tells info of the clan")
            Player.MessageFrom(sys, "/cmembers - Tells the specified or your clan's name")
            Player.MessageFrom(sys, "/cm - Send a Message to your clan")
            Player.MessageFrom(sys, "/ckick - Kicks the player from the clan (Could be used Only from Officer rank)")
            Player.MessageFrom(sys, "/cpromote - Promotes player (Can promote until Co-Owner)")
            Player.MessageFrom(sys, "/cdemote - Demotes player (Can demote until Member)")
            Player.MessageFrom(sys, "/crank - Gets the rank status of you or another player's")
            Player.MessageFrom(sys, "/cmotd - Sets motd of the clan")
            Player.MessageFrom(sys, "/cdisband - Disbands clan, If ownerpw was set, It will need It")
        elif command == "clist":
            Player.MessageFrom(sys, "---Clan List---")
            sec = claninfo.Sections
            for clanname in sec:
                name = clanname.replace("ClanInfo", "")
                Player.MessageFrom(sys, "[" + name + "]")
        elif command == "cinfo":
            if len(args) == 0:
                Player.MessageFrom(sys, "Specify Clan name!")
                return
            sec = claninfo.Sections
            for clanname in sec:
                name = clanname.replace("ClanInfo", "")
                n = self.GetClanPopulation(name)
                own = claninfo.GetSetting(clanname, "Owner")
                ex = claninfo.GetSetting(clanname, "Creation")
                Player.MessageFrom(sys, "Clan: [" + name + "]")
                Player.MessageFrom(sys, "Owner: " + own)
                Player.MessageFrom(sys, "Members: " + n)
                Player.MessageFrom(sys, "Exists Since: " + str(ex))
        elif command == "cmembers":
            id = Player.SteamID
            if len(args) == 0:
                clan = self.GetClanOfPlayer(id)
                Player.MessageFrom(sys, self.GetClanMembers(clan))
            else:
                clan = String.Join(" ", args)
                if self.GetClanOfPlayer(clan) is not None:
                    Player.MessageFrom(sys, "Clan named " + clan + " doesn't exist.")
                    return
                clan = self.GetClanOfPlayer(clan)
                Player.MessageFrom(sys, self.GetClanMembers(clan))
        elif command == "crankpw":
            if len(args) == 0 or len(args) > 1:
                Player.MessageFrom(sys, "Usage /crankpw password")
                Player.MessageFrom(sys, "YOU WON'T BE ABLE TO CHANGE THE PASSWORD AFTER THIS.")
                Player.MessageFrom(sys, "Only admins will be able to reset this password.")
                return
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan.")
                return
            if not Lib:
                Player.MessageFrom(sys, "Sorry, this feature doesn't work on this server.")
                return
            rank = self.GetClanOfPlayer(id)
            if rank < 4:
                Player.MessageFrom(sys, "Online the Owner of the clan can do this.")
                return
            clan = self.GetClanOfPlayer(id)
            if claninfo.ContainsSetting("ClanInfo" + clan, "Password"):
                Player.MessageFrom(sys, "Password is already set.")
                return
            n = hashlib.md5(str(args[0])).hexdigest()
            claninfo.AddSetting("ClanInfo" + clan, "Password", n)
            claninfo.Save()
            Player.MessageFrom(sys, "Password " + qargs[0] + " set.")
        elif command == "cloginpw":
            if len(args) == 0 or len(args) > 2:
                Player.MessageFrom(sys, 'Usage /cloginpw "clanname" "password"')
                Player.MessageFrom(sys, "Quotes are REQUIRED!")
                return
            id = Player.SteamID
            name = Player.Name
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan.")
                return
            if not Lib:
                Player.MessageFrom(sys, "Sorry, this feature doesn't work on this server.")
                return
            clan = str(qargs[0])
            epw = str(qargs[1])
            if self.GetClanPopulation(clan) is None:
                Player.MessageFrom(sys, "Clan named " + clan + " doesn't exist.")
                return
            n = hashlib.md5(epw).hexdigest()
            pw = claninfo.GetSetting("ClanInfo" + clan, "Password")
            n2 = hashlib.md5(pw).hexdigest()
            if n == n2:
                self.AddPlayerToClan(clan, id, name, 4)
                Player.MessageFrom(sys, "Clan Ownership recovered.")
            else:
                Player.MessageFrom(sys, "Wrong Password.")
        elif command == "ccreate":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /ccreate clanname - No need to add [] or ()")
                cost = cfg.GetSetting("Settings", "Cost")
                if int(cost) > 0:
                    Player.MessageFrom(sys, "Cost of Creation: " + str(cost))
                return
            id = Player.SteamID
            if self.HasClan(id):
                Player.MessageFrom(sys, "You already have a clan. Leave first.")
                return
            text = String.Join(" ", args)
            if len(text) < 3 or not re.match("[\w]+$", text):
                Player.MessageFrom(sys, "Give atleast 3 characters without spaces.")
                return
            self.CreateClan(text, id, str(Player.Name))
            cost = cfg.GetSetting("Settings", "Cost")
            if int(cost) > 0:
                self.TakeMoney(id, cost, Player)
            Server.BroadcastFrom(sys, text + " got created by " + Player.Name)
            Player.MessageFrom(sys, "You created your first clan! /cinvite playername to invite!")
        elif command == "cinvite":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cinvite playername")
                return
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            if self.GetClanRank(id) == 1:
                Player.MessageFrom(sys, "You must be an officer or an owner to do this.")
                return
            playerr = self.CheckV(Player, args)
            if playerr is None:
                return
            if self.HasClan(playerr.SteamID):
                Player.MessageFrom(sys, "This player has a clan.")
                return
            if self.IsPending(playerr.SteamID):
                Player.MessageFrom(sys, "This player is pending a request. Try after a few seconds.")
                return
            if playerr.SteamID == id:
                Player.MessageFrom(sys, "Gosh, this is yourself....")
                return
            clan = self.GetClanOfPlayer(id)
            self.MakePending(playerr.SteamID, id)
            playerr.MessageFrom(sys, "Clan " + clan + " invited you to join their forces!")
            playerr.MessageFrom(sys, "Type /cjoin to accept or /cdeny to deny! You have 40 seconds to accept.")
            online = self.GetAllOnlinePlayersOfClan(clan)
            for player in Server.ActivePlayers:
                if player.SteamID in online:
                    player.MessageFrom(sys, Player.Name + " invited " + playerr.Name + " to join the clan.")
            autokill = Plugin.CreateDict()
            autokill["PlayerR"] = Player.SteamID
            autokill["PlayerT"] = playerr.SteamID
            Plugin.CreateParallelTimer("ClansAutoKill", 1000 * 40, autokill).Start()
        elif command == "cdeny":
            id = Player.SteamID
            if not self.IsPending(id):
                Player.MessageFrom(sys, "You aren't pending any requests!")
                return
            inviterid = DataStore.Get("Clans", id)
            inviter = Server.FindPlayer(inviterid)
            DataStore.Remove("Clans", id)
            inviter.MessageFrom(sys, Player.Name + "  Denied the request!")
            Player.MessageFrom(sys, "You denied the request!")
        elif command == "cjoin":
            id = Player.SteamID
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
            for player in Server.ActivePlayers:
                if player.SteamID in online:
                    player.MessageFrom(sys, Player.Name + " joined to the clan!")
        elif command == "cm":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cm message")
                return
            name = str(Player.Name)
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            clan = self.GetClanOfPlayer(id)
            rank = self.GetClanRank(id)
            rank = self.TranslateToRank(rank)
            name = "(" + rank + ") " + name
            text = String.Join(" ", args)
            self.SendPrivateMessage(clan, name, text)
        elif command == "ckick":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /ckick playername")
                return
            name = str(Player.Name)
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            playerr = self.CheckV(Player, args)
            if playerr is None:
                return
            if playerr.SteamID == id:
                Player.MessageFrom(sys, "Gosh, this is yourself....")
                return
            rank = self.GetClanRank(playerr.SteamID)
            selfrank = self.GetClanRank(id)
            clan = self.GetClanOfPlayer(id)
            if self.GetClanOfPlayer(playerr.SteamID) is not None:
                Player.MessageFrom(sys, "This player doesn't even have a clan")
                return
            otherclan = self.GetClanOfPlayer(playerr.SteamID)
            if rank == selfrank:
                Player.MessageFrom(sys, "You can't kick people having higher or the same rank.")
                return
            if rank > selfrank:
                Player.MessageFrom(sys, "You can't kick people having higher or the same rank.")
                return
            if otherclan != clan:
                Player.MessageFrom(sys, "Heh. Silly you.")
                return
            self.RemovePlayerFromClan(clan, playerr.SteamID)
            online = self.GetAllOnlinePlayersOfClan(clan)
            for player in Server.ActivePlayers:
                if player.SteamID in online:
                    player.MessageFrom(clan, playerr.Name + " got kicked by: " + Player.Name)
            playerr.MessageFrom(clan, "You got kicked from the clan by: " + Player.Name)
        elif command == "cpromote":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cpromote playername")
                return
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            if self.GetClanRank(id) < 3:
                Player.MessageFrom(sys, "You must be an owner or co-owner to do this.")
                return
            playerr = self.CheckV(Player, args)
            if playerr is None:
                return
            if playerr.SteamID == id:
                Player.MessageFrom(sys, "Gosh, this is yourself....")
                return
            clan = self.GetClanOfPlayer(id)
            otherclan = self.GetClanOfPlayer(playerr.SteamID)
            if otherclan != clan:
                Player.MessageFrom(sys, "Heh. Silly you.")
                return
            rank = self.GetClanRank(playerr.SteamID)
            if rank > 0 and rank < 3:
                self.PromotePlayer(playerr.SteamID)
            else:
                Player.MessageFrom(sys, "You can't promote to Owner. Only one owner can exist.")
        elif command == "cdemote":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cdemote playername")
                return
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            if self.GetClanRank(id) < 3:
                Player.MessageFrom(sys, "You must be an owner or co-owner to do this.")
                return
            playerr = self.CheckV(Player, args)
            if playerr is None:
                return
            if playerr.SteamID == id:
                Player.MessageFrom(sys, "Gosh, this is yourself....")
                return
            clan = self.GetClanOfPlayer(id)
            otherclan = self.GetClanOfPlayer(playerr.SteamID)
            if otherclan != clan:
                Player.MessageFrom(sys, "Heh. Silly you.")
                return
            rank = self.GetClanRank(playerr.SteamID)
            selfrank = self.GetClanRank(id)
            if rank == 4:
                Player.MessageFrom(sys, "You can't demote an owner.")
                return
            if selfrank == rank:
                Player.MessageFrom(sys, "You can't demote people with the same rank.")
                return
            self.DemotePlayer(playerr.SteamID)
        elif command == "crank":
            if len(args) == 0:
                id = Player.SteamID
                if not self.HasClan(id):
                    Player.MessageFrom(sys, "You don't have a clan!")
                    return
                rank = self.GetClanRank(id)
                clan = self.GetClanOfPlayer(id)
                serv = claninfo.GetSetting("ClanInfo" + clan, "Join" + id)
                trans = self.TranslateToRank(rank)
                Player.MessageFrom(sys, Player.Name + " |  Rank: " + trans)
                Player.MessageFrom(sys, "Serving Since: " + str(serv))
            else:
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                id = playerr.SteamID
                if not self.HasClan(id):
                    Player.MessageFrom(sys, "This player doesn't have a clan!")
                    return
                rank = self.GetClanRank(id)
                clan = self.GetClanOfPlayer(id)
                serv = claninfo.GetSetting("ClanInfo" + clan, "Join" + id)
                trans = self.TranslateToRank(rank)
                Player.MessageFrom(sys, Player.Name + " |  Rank: " + trans)
                Player.MessageFrom(sys, "Serving Since: " + str(serv))
        elif command == "cmotd":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cmotd motd")
                return
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            rank = self.GetClanRank(id)
            if rank >= 3:
                clan = self.GetClanOfPlayer(id)
                text = String.Join(" ", args)
                claninfo.AddSetting("ClanInfo" + clan, "Motd", text)
                claninfo.Save()
                Player.MessageFrom(sys, "Motd Set")
        elif command == "cdisband":
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            rank = self.GetClanRank(id)
            clan = self.GetClanOfPlayer(id)
            if claninfo.ContainsSetting("ClanInfo" + clan, "Password"):
                if len(args) == 0:
                    Player.MessageFrom(sys, "Usage /cdisband ownerpassword - (This means password was set before)")
                    return
                if rank == 4:
                    pw = claninfo.GetSetting("ClanInfo" + clan, "Password")
                    n = hashlib.md5(str(args[0])).hexdigest()
                    if n == pw:
                        self.DeleteClan(clan)
                    else:
                        Player.MessageFrom(sys, "Wrong Password.")
            else:
                if rank == 4:
                    self.DeleteClan(clan)