__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import sys
import re
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")
import hashlib
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
        if ini.ContainsSetting("ClanMembers", ID) or ini.ContainsSetting("ClanOfficers", ID) or \
                ini.ContainsSetting("ClanOwners", ID) or ini.ContainsSetting("ClanCoOwners", ID):
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
        elif ini.ContainsSetting("ClanOfficers", ID):
            return ini.GetSetting("ClanOfficers", ID)
        elif ini.ContainsSetting("ClanOwners", ID):
            return ini.GetSetting("ClanOwners", ID)
        elif ini.ContainsSetting("ClanCoOwners", ID):
            return ini.GetSetting("ClanCoOwners", ID)
        return None

    def GetAllOnlinePlayersOfClan(self, Clan):
        ini = self.Clans()
        sec = ini.EnumSection(Clan)
        ids = []
        for id in sec:
            ids.append(id)
        Players = []
        for player in Server.Players:
            if player.SteamID in ids:
                Players.append(player)
        return Players

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
        elif ini.ContainsSetting("ClanOfficers", ID):
            return 2
        elif ini.ContainsSetting("ClanCoOwners", ID):
            return 3
        elif ini.ContainsSetting("ClanOwners", ID):
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
        claninfo.AddSetting("ClanInfo" + Clan, "FriendlyFire", "0")
        claninfo.AddSetting("ClanInfo" + Clan, "Join" + ID, str(t))
        claninfo.AddSetting("ClanInfo" + Clan, "Motd", "This clan has a default motd :( ")
        claninfo.AddSetting("ClanList", Clan, "1")
        claninfo.Save()
        # Todo: More to come.

    def DeleteClan(self, Clan):
        cfg = self.ClansConfig()
        ini = self.Clans()
        claninfo = self.ClanInfo()
        sys = cfg.GetSetting("Settings", "Sys")
        online = self.GetAllOnlinePlayersOfClan(Clan)
        for player in online:
            name = player.Name.replace('[' + Clan + ']', '').strip(' ')
            # player.basePlayer.displayName = name
            player.Name = name
            # ReflectionExtensions.SetFieldValue(player.basePlayer, "_displayName", name)
            player.MessageFrom(sys, "Your clan was disbanded.")
        enum = ini.EnumSection(Clan)
        for d in enum:
            ini.DeleteSetting(Clan, d)
        sec = ini.EnumSection("ClanMembers")
        sec2 = ini.EnumSection("ClanOwners")
        sec3 = ini.EnumSection("ClanOfficers")
        sec4 = ini.EnumSection("ClanCoOwners")
        sec5 = claninfo.EnumSection("ClanInfo" + Clan)
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
        for p in sec5:
            claninfo.DeleteSetting("ClanInfo" + Clan, p)
        ini.Save()
        # claninfo.DeleteSetting("ClanInfo" + Clan, "Creation")
        # claninfo.DeleteSetting("ClanInfo" + Clan, "Owner")
        claninfo.DeleteSetting("ClanList", Clan)
        claninfo.Save()

    def AddPlayerToClan(self, Clan, ID, Name, Rank=None):
        ini = self.Clans()
        ini.AddSetting(Clan, ID, Name)
        if Rank == 1 or Rank is None:
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

    def PromotePlayer(self, ID, pl):
        ini = self.Clans()
        cur = self.GetClanRank(ID)
        clan = self.GetClanOfPlayer(ID)
        if cur == 1:
            ini.DeleteSetting("ClanMembers", ID)
            ini.AddSetting("ClanOfficers", ID, clan)
            pr = "Officer"
        elif cur == 2:
            ini.DeleteSetting("ClanOfficers", ID)
            ini.AddSetting("ClanCoOwners", ID, clan)
            pr = "Co-Owner"
        else:
            return
        online = self.GetAllOnlinePlayersOfClan(clan)
        for player in online:
            player.MessageFrom("[" + clan + "]", pl.Name + " got promoted to: " + pr)
        ini.Save()

    def DemotePlayer(self, ID, pl):
        ini = self.Clans()
        cur = self.GetClanRank(ID)
        clan = self.GetClanOfPlayer(ID)
        if cur == 2:
            ini.DeleteSetting("ClanOfficers", ID)
            ini.AddSetting("ClanMembers", ID, clan)
            dr = "Member"
        elif cur == 3:
            ini.DeleteSetting("ClanCoOwners", ID)
            ini.AddSetting("ClanOfficers", ID, clan)
            dr = "Officer"
        else:
            return
        online = self.GetAllOnlinePlayersOfClan(clan)
        for player in online:
            player.MessageFrom("[" + clan + "]", pl.Name + " got demoted to: " + dr)
        ini.Save()

    def RemovePlayerFromClan(self, Clan, ID):
        ini = self.Clans()
        claninfo = self.ClanInfo()
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
        claninfo.DeleteSetting("ClanInfo" + Clan, "Join" + ID)

    def GetClanMembers(self, Clan):
        ini = self.Clans()
        sec = ini.EnumSection(Clan)
        s = ""
        for m in sec:
            g = ini.GetSetting(Clan, m)
            s = s + g + ", "
        return s

    def GetClanMembersList(self, Clan):
        ini = self.Clans()
        sec = ini.EnumSection(Clan)
        names = {}
        for id in sec:
            g = str(ini.GetSetting(Clan, id))
            g = g.lower()
            names.update({id: g})
        return names

    def GetKeyByValue(self, List, Value):
        for n, v in List.iteritems():
            if v == Value:
                return n
        return None

    def IsPending(self, id):
        if DataStore.ContainsKey("Clans", id):
            return True
        return False

    def SendPrivateMessage(self, Clan, FromPlayer, Message):
        online = self.GetAllOnlinePlayersOfClan(Clan)
        for player in online:
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

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.1
    """

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(sys, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(sys, "Found [color#FF0000]" + str(count)
                               + "[/color] player with similar name. [color#FF0000] Use more correct name!")
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
            # Player.basePlayer.displayName = "[" + clan + "] " + name
            # ReflectionExtensions.SetFieldValue(Player.basePlayer, "_displayName", "[" + clan + "] " + name)
            Player.Name = "[" + clan + "] " + name
            claninfo = self.ClanInfo()
            if claninfo.ContainsSetting("ClanInfo" + clan, "Motd"):
                motd = claninfo.GetSetting("ClanInfo" + clan, "Motd")
                Player.MessageFrom("[" + clan + "]", motd)

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.VictimIsPlayer and HurtEvent.AttackerIsPlayer:
            if HurtEvent.Victim is not None and HurtEvent.Attacker is not None:
                vid = HurtEvent.Victim.SteamID
                aid = HurtEvent.Attacker.SteamID
                if self.HasClan(vid) and self.HasClan(aid):
                    ca = self.GetClanOfPlayer(aid)
                    cv = self.GetClanOfPlayer(vid)
                    if ca == cv:
                        claninfo = self.ClanInfo()
                        ff = int(claninfo.GetSetting("ClanInfo" + ca, "FriendlyFire"))
                        if ff == 1:
                            return
                        HurtEvent.DamageAmount = float(0)

    """def On_Chat(self, ChatEvent):
        if self.HasClan(ChatEvent.User.SteamID):
            clan = self.GetClanOfPlayer(ChatEvent.User.SteamID)
            ChatEvent.BroadcastName = "[" + clan + "] " + ChatEvent.User.Name"""

    def On_Command(self, Player, command, args):
        cfg = self.ClansConfig()
        claninfo = self.ClanInfo()
        sys = cfg.GetSetting("Settings", "Sys")
        if command == "chelp":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /chelp pagenumber (1 or 2)")
            else:
                text = str.join(' ', args)
                if text == "1":
                    Player.MessageFrom(sys, "Clans Created by " + __author__ + " V" + __version__)
                    Player.MessageFrom(sys, "[PAGE 1/2]")
                    Player.MessageFrom(sys, "Type the commands in for more info.")
                    Player.MessageFrom(sys, "/crankpw - Sets Clan Recovery password for owners")
                    Player.MessageFrom(sys, "/cloginpw - Adds you back to owner, If you lost your powers.")
                    Player.MessageFrom(sys, "/ccreate - Creates you a clan.")
                    Player.MessageFrom(sys, "/cinvite - Invites player to the clan")
                    Player.MessageFrom(sys, "/cdeny - Denies Invitation (Auto Deny: 40 secs)")
                    Player.MessageFrom(sys, "/cjoin - Accept the invitation")
                    Player.MessageFrom(sys, "/clist - Lists all the clans")
                    Player.MessageFrom(sys, "/cinfo - Tells info of the clan")
                elif text == "2":
                    Player.MessageFrom(sys, "Clans Created by " + __author__ + " V" + __version__)
                    Player.MessageFrom(sys, "[PAGE 2/2]")
                    Player.MessageFrom(sys, "/cmembers - Lists the specified or your clan's members names")
                    Player.MessageFrom(sys, "/cm - Send a Message to your clan")
                    Player.MessageFrom(sys, "/cff 1 - 0 - Sets FriendlyFire on/off")
                    Player.MessageFrom(sys, "/ckick - Kicks the player from the clan (Could be used "
                                            "Only from Officer rank)")
                    Player.MessageFrom(sys, "/cpromote - Promotes player (Can promote until Co-Owner)")
                    Player.MessageFrom(sys, "/cdemote - Demotes player (Can demote until Member)")
                    Player.MessageFrom(sys, "/crank - Gets the rank status of you or another player's")
                    Player.MessageFrom(sys, "/cmotd - Sets motd of the clan")
                    Player.MessageFrom(sys, "/cleave - Leave clan")
                    Player.MessageFrom(sys, "/cdisband - Disbands clan, If ownerpw was set, It will need It")
                else:
                    Player.MessageFrom(sys, "Usage /chelp pagenumber (1 or 2)")
        elif command == "clist":
            Player.MessageFrom(sys, "---Clan List---")
            sec = claninfo.EnumSection("ClanList")
            for clanname in sec:
                Player.MessageFrom(sys, "[" + clanname + "]")
        elif command == "cinfo":
            if len(args) == 0:
                Player.MessageFrom(sys, "Specify Clan name!")
                return
            clan = str.Join(" ", args)
            if claninfo.ContainsSetting("ClanList", clan):
                motd = claninfo.GetSetting("ClanInfo" + clan, "Motd")
                n = self.GetClanPopulation(clan)
                own = claninfo.GetSetting("ClanInfo" + clan, "Owner")
                ex = claninfo.GetSetting("ClanInfo" + clan, "Creation")
                ff = claninfo.GetSetting("ClanInfo" + clan, "FriendlyFire")
                if int(ff) == 1:
                    ff = "Yes"
                else:
                    ff = "No"
                Player.MessageFrom(sys, "Clan: [" + clan + "]")
                Player.MessageFrom(sys, "Motd: [" + motd + "]")
                Player.MessageFrom(sys, "Owner: " + own)
                Player.MessageFrom(sys, "FriendlyFire: " + ff)
                Player.MessageFrom(sys, "Members: " + str(n))
                Player.MessageFrom(sys, "Exists Since: " + str(ex))
            else:
                Player.MessageFrom(sys, "Couldn't find clan " + clan)
        elif command == "cmembers":
            id = Player.SteamID
            if len(args) == 0:
                if not self.HasClan(id):
                    Player.MessageFrom(sys, "You don't have a clan!")
                    return
                clan = self.GetClanOfPlayer(id)
                Player.MessageFrom(clan + ' Members', self.GetClanMembers(clan))
            else:
                clan = str.Join(" ", args)
                if not claninfo.ContainsSetting("ClanList", clan):
                    Player.MessageFrom(sys, "Clan named " + clan + " doesn't exist.")
                    return
                Player.MessageFrom(clan + "'s Members", self.GetClanMembers(clan))
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
            Player.MessageFrom(sys, "Password " + args[0] + " set.")
        elif command == "cloginpw":
            if len(args) <= 1 or len(args) > 2:
                Player.MessageFrom(sys, 'Usage /cloginpw "clanname" "password"')
                Player.MessageFrom(sys, "Quotes are REQUIRED!")
                return
            id = Player.SteamID
            name = Player.Name
            if self.HasClan(id):
                Player.MessageFrom(sys, "First Leave your clan!")
                return
            clan = str(args[0])
            epw = str(args[1])
            if self.GetClanPopulation(clan) is None:
                Player.MessageFrom(sys, "Clan named " + clan + " doesn't exist.")
                return
            n = hashlib.md5(epw).hexdigest()
            pw = claninfo.GetSetting("ClanInfo" + clan, "Password")
            if n == pw:
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
            name = Player.Name
            if self.HasClan(id):
                Player.MessageFrom(sys, "You already have a clan. Leave first.")
                return
            text = str.Join(" ", args)
            if len(text) < 3 or len(text) > 10 or not re.match("[\w]+$", text):
                Player.MessageFrom(sys, "Give 3-10 characters without spaces.")
                return
            self.CreateClan(text, id, str(Player.Name))
            cost = cfg.GetSetting("Settings", "Cost")
            if int(cost) > 0:
                self.TakeMoney(id, cost, Player)
            Server.BroadcastFrom(sys, text + " got created by " + Player.Name)
            Player.MessageFrom(sys, "You created your first clan! /cinvite playername to invite!")
            # Player.basePlayer.displayName = "[" + text + "] " + name
            # ReflectionExtensions.SetFieldValue(Player.basePlayer, "_displayName", "[" + text + "] " + name)
            Player.Name = "[" + text + "] " + name
        elif command == "cinvite":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /cinvite playername")
                return
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            if self.GetClanRank(id) == 1:
                Player.MessageFrom(sys, "You must be an officer/co-owner/owner to do this.")
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
            nam = Player.Name.replace('[' + clan + ']', '').strip(' ')
            for player in online:
                player.MessageFrom("[" + clan + "]", nam + " invited " + playerr.Name + " to join the clan.")
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
            if not self.IsPending(id):
                Player.MessageFrom(sys, "You aren't pending any requests!")
                return
            if self.HasClan(id):
                Player.MessageFrom(sys, "You already have a clan!")
                DataStore.Remove("Clans", id)
                return
            inv = DataStore.Get("Clans", id)
            clan = self.GetClanOfPlayer(inv)
            self.AddPlayerToClan(clan, id, str(Player.Name))
            DataStore.Remove("Clans", id)
            online = self.GetAllOnlinePlayersOfClan(clan)
            for player in online:
                player.MessageFrom("[" + clan + "]", Player.Name + " joined to the clan!")
            # Player.basePlayer.displayName = "[" + clan + "] " + Player.Name
            # ReflectionExtensions.SetFieldValue(Player.basePlayer, "_displayName", "[" + clan + "] " + Player.Name)
            Player.Name = "[" + clan + "] " + Player.Name
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
            name = name.replace('[' + clan + ']', '').strip(' ')
            rank = self.GetClanRank(id)
            rank = self.TranslateToRank(rank)
            name = "(" + rank + ") " + name
            text = str.Join(" ", args)
            self.SendPrivateMessage(clan, name, text)
        elif command == "cff":
            if len(args) == 0 or len(args) > 1:
                Player.MessageFrom(sys, "Usage /cff 1 - 0 (0 means off)")
                return
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            if self.GetClanRank(id) <= 2:
                Player.MessageFrom(sys, "You must be an co-owner/owner to do this.")
                return
            clan = self.GetClanOfPlayer(id)
            v = args[0]
            if not v.isnumeric():
                Player.MessageFrom(sys, "Usage /cff 1 - 0 (0 means off)")
                return
            claninfo.SetSetting("ClanInfo" + clan, "FriendlyFire", str(v))
            claninfo.Save()
            Player.MessageFrom(sys, "Friendly fire was set to " + str(v))
        elif command == "ckick":
            if len(args) == 0:
                Player.MessageFrom(sys, "Usage /ckick playername")
                return
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            clan = self.GetClanOfPlayer(id)
            playerr = self.CheckV(Player, args, 3)
            selfrank = self.GetClanRank(id)
            if playerr is None:
                text = str.Join(" ", args)
                text = text.lower()
                list = self.GetClanMembersList(clan)
                values = list.values()
                namee = None
                for name in values:
                    if text in name:
                        n = self.GetKeyByValue(list, name)
                        otherrank = self.GetClanRank(n)
                        if otherrank >= selfrank:
                            Player.MessageFrom(sys, "You can't kick people having higher or the same rank.")
                            return
                        if n == id:
                            Player.MessageFrom(sys, "Gosh, this is yourself....")
                            return
                        self.RemovePlayerFromClan(clan, n)
                        namee = name
                if namee:
                    online = self.GetAllOnlinePlayersOfClan(clan)
                    for pl in online:
                        pl.MessageFrom("[" + clan + "]", namee + " got kicked by: " + Player.Name)
                        return
                Player.MessageFrom(sys, "Couldn't find player.")
                return
            else:
                if playerr.SteamID == id:
                    Player.MessageFrom(sys, "Gosh, this is yourself....")
                    return
                rank = self.GetClanRank(playerr.SteamID)
                if not self.HasClan(playerr.SteamID):
                    Player.MessageFrom(sys, "This player doesn't even have a clan")
                    return
                otherclan = self.GetClanOfPlayer(playerr.SteamID)
                if rank >= selfrank:
                    Player.MessageFrom(sys, "You can't kick people having higher or the same rank.")
                    return
                if otherclan != clan:
                    Player.MessageFrom(sys, "Heh. Silly you.")
                    return
                self.RemovePlayerFromClan(clan, playerr.SteamID)
                online = self.GetAllOnlinePlayersOfClan(clan)
                name = Player.Name.replace('[' + clan + ']', '').strip(' ')
                # playerr.basePlayer.displayName = name
                # ReflectionExtensions.SetFieldValue(playerr.basePlayer, "_displayName", name)
                playerr.Name = name
                for pl in online:
                    pl.MessageFrom("[" + clan + "]", playerr.Name + " got kicked by: " + Player.Name)
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
            if 0 < rank < 3:
                self.PromotePlayer(playerr.SteamID, playerr)
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
            self.DemotePlayer(playerr.SteamID, playerr)
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
                Player.MessageFrom(sys, "Clan: [" + clan + "]")
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
                Player.MessageFrom(sys, "Clan: [" + clan + "]")
                Player.MessageFrom(sys, playerr.Name + " |  Rank: " + trans)
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
                text = str.Join(" ", args)
                claninfo.AddSetting("ClanInfo" + clan, "Motd", text)
                claninfo.Save()
                online = self.GetAllOnlinePlayersOfClan(clan)
                for player in online:
                    player.MessageFrom("[" + clan + "]", "New Motd: " + text)
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
                    Player.MessageFrom(sys, "You need to be an owner to do this.")
            else:
                if rank == 4:
                    self.DeleteClan(clan)
        elif command == "cleave":
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            rank = self.GetClanRank(id)
            clan = self.GetClanOfPlayer(id)
            lenn = self.GetClanPopulation(clan)
            if lenn == 1:
                self.DeleteClan(clan)
                return
            if rank == 4:
                self.DeleteClan(clan)
            else:
                self.RemovePlayerFromClan(clan, id)
                online = self.GetAllOnlinePlayersOfClan(clan)
                name = Player.Name.replace('[' + clan + ']', '').strip(' ')
                # Player.basePlayer.displayName = name
                #ReflectionExtensions.SetFieldValue(Player.basePlayer, "_displayName", "[" + clan + "] " + name)
                Player.Name = "[" + clan + "] " + name
                for pl in online:
                    pl.MessageFrom("[" + clan + "]", name + " left the clan.")
                Player.MessageFrom(clan, "You left your clan.")
        """elif command == "cleave":
            id = Player.SteamID
            if not self.HasClan(id):
                Player.MessageFrom(sys, "You don't have a clan!")
                return
            clan = self.GetClanOfPlayer(id)
            rank = self.GetClanRank(id)
            name = Player.Name.replace('[' + clan + ']', '').strip(' ')
            if rank == 4:
                self.DeleteClan(clan)
                return
            Player.basePlayer.displayName = name
            self.RemovePlayerFromClan(clan, id)"""