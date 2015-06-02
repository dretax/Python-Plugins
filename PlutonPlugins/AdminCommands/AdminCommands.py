__author__ = 'DreTaX'
__version__ = '1.8.8'

import clr

clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Assembly-CSharp")
import Pluton
import UnityEngine
from UnityEngine import Vector3 as Vector3
import System
from System import *
import math
import sys
import BasePlayer
path = Util.GetPublicFolder()
sys.path.append(path + "\\Python\\Lib\\")
try:
    import hashlib
except ImportError:
    raise ImportError('Download the Extra IronPython Libs from pluton-team.org')
import random
import re

"""
    Class
"""

Animals = ['stag', 'boar', 'chicken', 'bear', 'wolf', 'horse']
Resources = {

}
class AdminCommands:

    ohash = None
    mhash = None
    Disconnect = None
    Join = None
    DutyFirst = None
    Owners = None
    DefaultVector = None
    Friends = None
    Sysname = None
    ResourceList = None
    BuildingPrivlidge = None

    def On_PluginInit(self):
        DataStore.Flush('Duty')
        ini = self.AdminCmdConfig()
        password = ini.GetSetting("Settings", "OwnerPassword")
        password2 = ini.GetSetting("Settings", "ModeratorPassword")
        self.Disconnect = self.bool(ini.GetSetting("Settings", "DisconnectMessage"))
        self.Join = self.bool(ini.GetSetting("Settings", "JoinMessage"))
        self.DutyFirst = self.bool(ini.GetSetting("Settings", "DutyFirst"))
        self.Owners = self.bool(ini.GetSetting("Settings", "CanOwnersByPassDuty"))
        self.DefaultVector = Vector3(0, 0, 0)
        self.LogGive = self.bool(ini.GetSetting("Settings", "LogGive"))
        self.LogAirdropCalls = self.bool(ini.GetSetting("Settings", "LogAirdropCalls"))
        self.LogDuty = self.bool(ini.GetSetting("Settings", "LogDuty"))
        self.Friends = self.bool(ini.GetSetting("Settings", "Friends"))
        self.BuildingPrivlidge = Util.TryFindReturnType("BuildingPrivlidge")
        self.Sysname = ini.GetSetting("Settings", "Sysname")
        res = Plugin.GetIni("Resources")
        for x in res.EnumSection("Resources"):
            Resources[x] = res.GetSetting("Resources", x)
        if password != "SetThisToSomethingElse":
            if bool(re.findall(r"([a-fA-F\d]{32})", password)):
                return
            hashed = hashlib.md5(password).hexdigest()
            ini.SetSetting("Settings", "OwnerPassword", hashed)
            ini.Save()
            self.ohash = hashed
        if password2 != "SetThisToSomethingElse":
            if bool(re.findall(r"([a-fA-F\d]{32})", password2)):
                return
            hashed = hashlib.md5(password2).hexdigest()
            ini.SetSetting("Settings", "ModeratorPassword", hashed)
            ini.Save()
            self.mhash = hashed

    def AdminCmdConfig(self):
        if not Plugin.IniExists("AdminCmdConfig"):
            loc = Plugin.CreateIni("AdminCmdConfig")
            loc.AddSetting("Settings", "OwnerPassword", "SetThisToSomethingElse")
            loc.AddSetting("Settings", "ModeratorPassword", "SetThisToSomethingElse")
            loc.AddSetting("Settings", "Sysname", "Equinox")
            loc.AddSetting("Settings", "JoinMessage", "True")
            loc.AddSetting("Settings", "DisconnectMessage", "True")
            loc.AddSetting("Settings", "DutyFirst", "True")
            loc.AddSetting("Settings", "CanOwnersByPassDuty", "True")
            loc.AddSetting("Settings", "LogGive", "True")
            loc.AddSetting("Settings", "LogAirdropCalls", "True")
            loc.AddSetting("Settings", "LogDuty", "True")
            loc.AddSetting("Settings", "Friends", "True")
            loc.Save()
        return Plugin.GetIni("AdminCmdConfig")

    def bool(self, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            raise ValueError

    def FriendList(self):
        if not Plugin.IniExists("Friends"):
            loc = Plugin.CreateIni("Friends")
            loc.Save()
        return Plugin.GetIni("Friends")

    def FriendOF(self, ofid, id):
        ini = self.FriendList()
        if ini.GetSetting(ofid, id) and ini.GetSetting(ofid, id) is not None:
            return True
        return False

    def Teleport(self, Player, Location):
        Player.basePlayer.StartSleeping()
        Player.basePlayer.transform.position = Location
        Player.basePlayer.ClientRPCPlayer(None, Player.basePlayer, "ForcePositionTo", Location)
        Player.basePlayer.SetPlayerFlag(BasePlayer.PlayerFlags.ReceivingSnapshot, True)
        Player.basePlayer.UpdateNetworkGroup()
        Player.basePlayer.UpdatePlayerCollider(True, False)
        Player.basePlayer.SendNetworkUpdateImmediate(False)
        Player.basePlayer.ClientRPCPlayer(None, Player.basePlayer, "StartLoading")
        Player.basePlayer.SendFullSnapshot()
        Player.basePlayer.SetPlayerFlag(BasePlayer.PlayerFlags.ReceivingSnapshot, False)
        Player.basePlayer.ClientRPCPlayer(None, Player.basePlayer, "FinishLoading")

    """
        CheckV Assistants
    """

    def GetPlayerName(self, name, Mode=1):
        Name = name.lower()
        if Mode == 1:
            for pl in Server.ActivePlayers:
                if pl.Name.lower() == Name:
                    return pl
        elif Mode == 2:
            for pl in Server.OfflinePlayers.Values:
                if pl.Name.lower() == Name:
                    return pl
        else:
            for pl in Server.ActivePlayers:
                if pl.Name.lower() == Name:
                    return pl
            for pl in Server.OfflinePlayers.Values:
                if pl.Name.lower() == Name:
                    return pl
        return None

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        Mode: Search mode (Default: 1)
            1 = Search Online Players
            2 = Search Offline Players
            3 = Both
        V5.0
    """

    def CheckV(self, Player, args, Mode=1):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.Join(" ", args), Mode)
            if p is not None:
                return p
            if Mode == 1:
                for pl in Server.ActivePlayers:
                    for namePart in args:
                        if namePart.lower() in pl.Name.lower():
                            p = pl
                            count += 1
            elif Mode == 2:
                for offlineplayer in Server.OfflinePlayers.Values:
                    for namePart in args:
                        if namePart.lower() in offlineplayer.Name.lower():
                            p = offlineplayer
                            count += 1
            else:
                for pl in Server.ActivePlayers:
                    for namePart in args:
                        if namePart.lower() in pl.Name.lower():
                            p = pl
                            count += 1
                for offlineplayer in Server.OfflinePlayers.Values:
                    for namePart in args:
                        if namePart.lower() in offlineplayer.Name.lower():
                            p = offlineplayer
                            count += 1
        else:
            p = self.GetPlayerName(str(args), Mode)
            if p is not None:
                return p
            if Mode == 1:
                for pl in Server.ActivePlayers:
                    if str(args).lower() in pl.Name.lower():
                        p = pl
                        count += 1
            elif Mode == 2:
                for offlineplayer in Server.OfflinePlayers.Values:
                    if str(args).lower() in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
            else:
                for pl in Server.ActivePlayers:
                    if str(args).lower() in pl.Name.lower():
                        p = pl
                        count += 1
                for offlineplayer in Server.OfflinePlayers.Values:
                    if str(args).lower() in offlineplayer.Name.lower():
                        p = offlineplayer
                        count += 1
        if count == 0:
            Player.MessageFrom("AdminCommands", "Couldn't find " + str.Join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom("AdminCommands", "Found " + str(count) + " player with similar name. Use more correct name!")
            return None

    # Duty idea taken from Jakkee from Fougerite
    def IsonDuty(self, Player):
        if not self.DutyFirst:
            return True
        elif DataStore.ContainsKey("Duty", Player.SteamID):
            return True
        elif self.Owners and Player.Owner:
            return True
        return False

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.quotedArgs
        if cmd.cmd == "duty":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if self.IsonDuty(Player):
                DataStore.Remove("Duty", Player.SteamID)
                Server.BroadcastFrom(self.Sysname, Player.Name + " is off duty.")
                if self.LogDuty:
                    Plugin.Log("DutyLog", Player.Name + " off duty.")
            else:
                DataStore.Add("Duty", Player.SteamID, True)
                Server.BroadcastFrom(self.Sysname, Player.Name + " is on duty. Let him know if you need anything.")
                if self.LogDuty:
                    Plugin.Log("DutyLog", Player.Name + " on duty.")
        elif cmd.cmd == "tpto":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /tpto name")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            pl = self.CheckV(Player, args, 3)
            if pl is not None:
                if "offlineplayer" in str(pl).lower():
                    loc = Vector3(pl.X, pl.Y, pl.Z)
                    self.Teleport(Player, loc)
                else:
                    self.Teleport(Player, pl.Location)
        elif cmd.cmd == "tphere":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /tphere name")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                self.Teleport(pl, Player.Location)
        elif cmd.cmd == "god":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if DataStore.Get("godmode", Player.SteamID) == 1:
                DataStore.Remove("godmode", Player.SteamID)
                Player.basePlayer.InitializeHealth(100, 100)
                Player.MessageFrom(self.Sysname, "God mode off.")
            else:
                DataStore.Add("godmode", Player.SteamID, 1)
                infinity = float("inf")
                Player.basePlayer.InitializeHealth(infinity, infinity)
                Player.MessageFrom(self.Sysname, "God mode on.")
        elif cmd.cmd == "ad":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if DataStore.Get("adoor", Player.SteamID) == 1:
                DataStore.Remove("adoor", Player.SteamID)
                Player.MessageFrom(self.Sysname, "Magic is now gone.")
            else:
                DataStore.Add("adoor", Player.SteamID, 1)
                Player.MessageFrom(self.Sysname, "Open up, Sesame!")
        elif cmd.cmd == "mute":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if len(args) <= 1:
                Player.MessageFrom(self.Sysname, "Usage: /mute playername minutes")
                return
            pl = self.CheckV(Player, args[0])
            if pl is not None:
                if not args[1].isdigit():
                    Player.MessageFrom(self.Sysname, "Usage: /mute playername minutes")
                    return
                if 0 < int(args[1]) <= 60:
                    DataStore.Add("MuteList", pl.SteamID, System.Environment.TickCount)
                    DataStore.Add("MuteListT", pl.SteamID, int(args[1]))
                    Player.MessageFrom(self.Sysname, pl.Name + " was muted!")
                    pl.MessageFrom(self.Sysname, Player.Name + " muted you for " + args[1] + " minutes!")
                    return
                Player.MessageFrom(self.Sysname, "Mute time must be between 1-60 mins")
        elif cmd.cmd == "unmute":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /unmute playername")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                DataStore.Remove("MuteListT", pl.SteamID)
                DataStore.Remove("MuteList", pl.SteamID)
                Player.MessageFrom(self.Sysname, pl.Name + " was unmuted!")
        elif cmd.cmd == "instako":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if DataStore.ContainsKey("Instako", Player.SteamID):
                DataStore.Remove("Instako", Player.SteamID)
                Player.MessageFrom(self.Sysname, "InstaKO Off")
            else:
                DataStore.Add("Instako", Player.SteamID, True)
                Player.MessageFrom(self.Sysname, "InstaKO On")
        elif cmd.cmd == "kick":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /kick playername")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                Player.MessageFrom(self.Sysname, "Kicked " + pl.Name + "!")
                pl.Kick("Kicked by admin")
        elif cmd.cmd == "say":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /say text")
                return
            text = str.join(' ', args)
            Server.BroadcastFrom("Server", text)
        elif cmd.cmd == "clear":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            for x in Player.Inventory.AllItems():
                x._item.Remove(1)
            Player.MessageFrom(self.Sysname, "Cleared!")
        elif cmd.cmd == "repairall":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            for x in Player.Inventory.AllItems():
                x._item.RepairCondition(x._item.maxCondition)
            Player.MessageFrom(self.Sysname, "Repaired All!")
        elif cmd.cmd == "give":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if len(args) <= 1:
                Player.MessageFrom(self.Sysname, "Usage: /give playername item amount")
                return
            pl = self.CheckV(Player, args[0])
            if pl is not None:
                num = 1
                if len(args) == 2:
                    num = 1
                elif len(args) == 3:
                    if args[2].isdigit():
                        num = int(args[2])
                else:
                    Player.MessageFrom(self.Sysname, "Usage: /give playername item amount")
                    Player.MessageFrom(self.Sysname, 'Or Try: /give "playername" "item" amount (With quote)')
                    return
                if self.LogGive:
                    Plugin.Log("ItemAdd", Player.Name + " gave to: " + str.join(' ', args))
                item = args[1]
                pl.Inventory.Add(item, num)
        elif cmd.cmd == "i":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            num = 1
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /i item amount")
                return
            elif len(args) == 2:
                if args[1].isdigit():
                    num = int(args[1])
            else:
                Player.MessageFrom(self.Sysname, "Usage: /i item amount")
                Player.MessageFrom(self.Sysname, 'Or Try: /i "item" amount (With quote)')
                return
            if self.LogGive:
                Plugin.Log("ItemAdd", Player.Name + " gave himself: " + str.join(' ', args))
            item = args[0]
            Player.Inventory.Add(item, num)
        elif cmd.cmd == "addowner":
            if not Player.Owner:
                Player.MessageFrom(self.Sysname, "You aren't an owner!")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /addowner name")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.MakeOwner(Player.Name + " made " + pl.Name + " an owner")
                Player.MessageFrom(self.Sysname, pl.Name + " got owner rights!")
                pl.MessageFrom(self.Sysname, Player.Name + " made you an owner!")
                return
            Player.MessageFrom(self.Sysname, "Couldn't find player.")
        elif cmd.cmd == "addmoderator":
            if not Player.Owner:
                Player.MessageFrom(self.Sysname, "You aren't an owner!")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /addmoderator name")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.MakeModerator(Player.Name + " made " + pl.Name + " a moderator")
                Player.MessageFrom(self.Sysname, pl.Name + " got moderator rights!")
                pl.MessageFrom(self.Sysname, Player.Name + " made you a moderator!")
                return
            Player.MessageFrom(self.Sysname, "Couldn't find player.")
        elif cmd.cmd == "removerights":
            if not Player.Owner:
                Player.MessageFrom(self.Sysname, "You aren't an owner!")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /removerights name")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.MakeNone()
                Player.MessageFrom(self.Sysname, "You removed " + pl.Name + "'s rights.")
                pl.MessageFrom(self.Sysname, Player.Name + " removed your rights.")
                return
            Player.MessageFrom(self.Sysname, "Couldn't find player.")
        elif cmd.cmd == "getowner":
            if self.ohash is None:
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /getowner password")
                return
            text = str.join(' ', args)
            hash = hashlib.md5(text).hexdigest()
            if hash == self.ohash:
                Player.MessageFrom(self.Sysname, "You gained owner.")
                Player.MakeOwner(Player.Name + " made himself owner via /getowner")
                return
            Player.MessageFrom(self.Sysname, "That didn't work buddy.")
        elif cmd.cmd == "getmoderator":
            if self.mhash is None:
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /getmoderator password")
                return
            text = str.join(' ', args)
            hash = hashlib.md5(text).hexdigest()
            if hash == self.mhash:
                Player.MessageFrom(self.Sysname, "You gained moderator.")
                Player.MakeModerator(Player.Name + " made himself moderator via /getmoderator")
                return
            Player.MessageFrom(self.Sysname, "That didn't work buddy.")
        elif cmd.cmd == "settime":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            text = str.join(' ', args)
            if not text.isdigit():
                Player.MessageFrom(self.Sysname, "Must be a number.")
            World.Time = int(args[0])
            Player.MessageFrom(self.Sysname, "Time changed to " + text + ". Wait a few seconds....")
        elif cmd.cmd == "players":
            s = ''
            for pl in Server.ActivePlayers:
                s = s + pl.Name + ', '
            Player.MessageFrom(self.Sysname, "Online Players:")
            Player.MessageFrom(self.Sysname, s)
        elif cmd.cmd == "airdropr":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if self.LogAirdropCalls:
                Plugin.Log("AirdropCall", Player.Name + " called airdrop to a random place.")
            World.AirDrop()
            Player.MessageFrom(self.Sysname, "Called.")
        elif cmd.cmd == "airdrop":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if self.LogAirdropCalls:
                Plugin.Log("AirdropCall", Player.Name + " called airdrop to himself.")
            World.AirDropAtPlayer(Player)
            Player.MessageFrom(self.Sysname, "Called to you.")
        elif cmd.cmd == "freezetime":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            World.FreezeTime()
            Player.MessageFrom(self.Sysname, "Time froze!.")
        elif cmd.cmd == "unfreezetime":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            World.UnFreezeTime()
            Player.MessageFrom(self.Sysname, "Time is running out now :)...")
        elif cmd.cmd == "kill":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /kill playername")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.Kill()
                Player.MessageFrom(self.Sysname, pl.Name + " killed!")
        elif cmd.cmd == "vectortp":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            vector = Player.GetLookPoint(2000)
            if vector == self.DefaultVector:
                Player.MessageFrom(self.Sysname, "Target is too far.")
                return
            self.Teleport(Player, vector)
            Player.MessageFrom(self.Sysname, "Teleported!")
        elif cmd.cmd == "teleportto":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't a moderator!")
                return
            text = str.join(' ', args)
            if not ',' in text:
                Player.MessageFrom(self.Sysname, "Usage: /teleportto x,y,z")
                return
            sp = text.split(',')
            if len(sp) < 2:
                Player.MessageFrom(self.Sysname, "Usage: /teleportto x,y,z")
                return
            loc = Vector3(float(sp[0]), float(sp[1]), float(sp[2]))
            self.Teleport(Player, loc)
            Player.MessageFrom(self.Sysname, "Teleported!")
        elif cmd.cmd == "addfriend":
            if not self.Friends:
                Player.MessageFrom(self.Sysname, "Feature disabled.")
                return
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /addfriend name")
                return
            pl = self.CheckV(Player, args)
            if pl is None:
                return
            if self.FriendOF(Player.SteamID, pl.SteamID):
                Player.MessageFrom(self.Sysname, "You have him already as a friend.")
                return
            ini = self.FriendList()
            ini.AddSetting(Player.SteamID, pl.SteamID, pl.Name)
            ini.Save()
            Player.MessageFrom(self.Sysname, "Added " + pl.Name + "!")
        elif cmd.cmd == "delfriend":
            if not self.Friends:
                Player.MessageFrom(self.Sysname, "Feature disabled.")
                return
            id = Player.SteamID
            if len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /delfriend name")
                return
            ini = self.FriendList()
            text = str.join(' ', args).lower()
            enum = ini.EnumSection(id)
            if len(enum) == 0:
                Player.MessageFrom(self.Sysname, "You don't even have friends buddy.")
                return
            for playerid in enum:
                nameof = ini.GetSetting(id, playerid).lower()
                if nameof == text or text in nameof:
                    ini.DeleteSetting(id, playerid)
                    ini.Save()
                    Player.MessageFrom(self.Sysname, str(nameof) + " was Removed from your list")
                    return
            Player.MessageFrom(self.Sysname, text + " is not on your list!")
        elif cmd.cmd == "friends":
            if not self.Friends:
                Player.MessageFrom(self.Sysname, "Feature disabled.")
                return
            id = Player.SteamID
            ini = self.FriendList()
            enum = ini.EnumSection(id)
            if len(enum) == 0:
                Player.MessageFrom(self.Sysname, "You don't even have friends buddy.")
                return
            Player.MessageFrom(self.Sysname, "List of Friends:")
            for playerid in enum:
                nameof = ini.GetSetting(id, playerid)
                if nameof:
                    Player.MessageFrom(self.Sysname, "- " + str(nameof))
        elif cmd.cmd == "spawn":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            if len(args) > 2 or len(args) == 0:
                Player.MessageFrom(self.Sysname, "Usage: /spawn animalname number")
                Player.MessageFrom(self.Sysname, "Animal List: /spawn list")
                Player.MessageFrom(self.Sysname, "Spawn All Animals: /spawn all number")
                Player.MessageFrom(self.Sysname,
                                   "Resources: tree1-tree26, bush1-2, loot1-loot2, animalnamecorpse, orenameore")
                return
            res = Plugin.GetIni("Resources")
            num = 1
            if len(args) == 2:
                num = args[1]
                if not num.isnumeric():
                    Player.MessageFrom(self.Sysname, "Second argument must be a number")
                    return
                num = int(num)
            type = args[0].lower()
            vector = Player.GetLookPoint(2000)
            if vector == self.DefaultVector:
                Player.MessageFrom(self.Sysname, "Target is too far.")
                return
            if type == "all":
                for a in Animals:
                    ani = res.GetSetting("Resources", a)
                    for x in xrange(1, num + 1):
                        World.SpawnAnimal(ani, vector.x, vector.y + 1.0, vector.z)
                # Skully xD
                Player.MessageFrom(self.Sysname, "Hey " + Player.Name + " ... We are here to eat you :P")
            elif type == "list":
                Player.MessageFrom(self.Sysname, "List: " + str(Animals))
                return
            elif type in Animals:
                for x in xrange(1, num + 1):
                    World.SpawnAnimal(type, vector.x, vector.y + 1.0, vector.z)
                # Skully xD
                Player.MessageFrom(self.Sysname, "Hey " + Player.Name + " ... We are here to eat you :P")
            elif type in Resources.keys():
                for x in xrange(1, num + 1):
                    World.SpawnMapEntity(Resources[type], vector.x, vector.y, vector.z)
            else:
                Player.MessageFrom(self.Sysname, "Couldn't find command.")
        elif cmd.cmd == "boardusers":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            objects = UnityEngine.Object.FindObjectsOfType[self.BuildingPrivlidge]()
            if len(objects) == 0:
                Player.MessageFrom(self.Sysname, "Couldn't find any objects")
                return
            c = 0
            for x in objects:
                dist = Util.GetInstance().GetVectorsDistance(x.transform.position, Player.Location)
                if dist > 6.0:
                    continue
                c += 1
                Player.MessageFrom(self.Sysname, "---Object" + str(c) + "---")
                if len(x.authorizedPlayers) == 0:
                    Player.MessageFrom(self.Sysname, "No players in the object.")
                    continue
                for z in x.authorizedPlayers:
                    name = z.username
                    id = z.userid
                    Player.MessageFrom(self.Sysname, "Authorized player: " + str(name) + " - " + str(id))
        """elif cmd.cmd == "apache":
            if not Player.Admin:
                Player.MessageFrom(self.Sysname, "You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.MessageFrom(self.Sysname, "You aren't on duty!")
                return
            Inventory = Player.Inventory
            for x in Inventory.InnerBelt.itemList:
                name = str(x.info.name)
                Player.Message(name)
                if "rocket_launcher" in name:
                    Player.Message("Da")
                    Player.Message(str(x.flags))
        elif cmd.cmd == "bulletrain":
            x = Player.X
            z = Player.Z
            y = Player.Y + 45
            Player.MessageFrom(self.Sysname, "TAKE COVER")
            for number in xrange(0, 20):
                #xr = float(random.randrange(int(x) - 10, int(x) + 10))
                #zr = float(random.randrange(int(z) - 10, int(z) + 10))
                World.SpawnMapEntity("fx/impacts/bullet/metal/metal1", x, y, z)"""

    """def On_DoorUse(self, DoorEvent):
        Server.Broadcast("ASd" + DoorEvent.Player.SteamID)
        Server.Broadcast(str(DataStore.Get("adoor", DoorEvent.Player.SteamID)))
        if DataStore.Get("adoor", DoorEvent.Player.SteamID):
            DoorEvent.Open = True"""

    def On_Chat(self, args):
        if DataStore.ContainsKey("MuteList", args.User.SteamID):
            Player = args.User
            id = Player.SteamID
            cooldown = int(DataStore.Get("MuteListT", id))
            time = int(DataStore.Get("MuteList", id))
            calc = System.Environment.TickCount - time
            if calc < 0 or math.isnan(calc) or math.isnan(time):
                DataStore.Remove("MuteListT", id)
                DataStore.Remove("MuteList", id)
                return
            if calc >= cooldown * 60000:
                DataStore.Remove("MuteListT", id)
                DataStore.Remove("MuteList", id)
                return
            Player.MessageFrom(self.Sysname, "You have a " + str(cooldown) + " min(s) Mute Cooldown.")
            args.BroadcastName = ""
            args.FinalText = ""

    def On_CombatEntityHurt(self, EntityHurtEvent):
        if EntityHurtEvent.Attacker is not None and EntityHurtEvent.Victim is not None:
            if EntityHurtEvent.Attacker.ToPlayer() is None:
                return
            attacker = EntityHurtEvent.Attacker.ToPlayer()
            if DataStore.ContainsKey("Instako", attacker.SteamID):
                if EntityHurtEvent.Victim.ToBuildingPart() is None:
                    return
                EntityHurtEvent.Victim.ToBuildingPart().Destroy()

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Victim is not None:
            if not self.Friends:
                return
            attacker = HurtEvent.Attacker
            if not attacker.IsPlayer():
                return
            victim = HurtEvent.Victim
            if self.FriendOF(attacker.SteamID, victim.SteamID):
                for x in range(0, len(HurtEvent.DamageAmounts)):
                    HurtEvent.DamageAmounts[x] = 0

    def On_PlayerConnected(self, Player):
        if self.Join:
            Server.BroadcastFrom(self.Sysname, Player.Name + " joined the server.")

    def On_PlayerDisconnected(self, Player):
        if self.Disconnect:
            Server.BroadcastFrom(self.Sysname, Player.Name + " disconnected.")
        DataStore.Remove("Duty", Player.SteamID)