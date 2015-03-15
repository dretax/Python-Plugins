__author__ = 'DreTaX'
__version__ = '1.7'

import clr

clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("UnityEngine")
import Pluton
from UnityEngine import Vector3
import System
from System import *
import math
import sys
path = Util.GetPublicFolder()
sys.path.append(path + "\\Python\\Lib\\")
import hashlib
import random
import re

"""
    Class
"""


class AdminCommands:

    ohash = None
    mhash = None
    Disconnect = None
    Join = None
    DutyFirst = None
    Owners = None
    DefaultVector = None

    def On_PluginInit(self):
        ini = self.AdminCmdConfig()
        password = ini.GetSetting("Settings", "OwnerPassword")
        password2 = ini.GetSetting("Settings", "ModeratorPassword")
        self.Disconnect = bool(ini.GetSetting("Settings", "DisconnectMessage"))
        self.Join = bool(ini.GetSetting("Settings", "JoinMessage"))
        self.DutyFirst = bool(ini.GetSetting("Settings", "DutyFirst"))
        self.Owners = bool(ini.GetSetting("Settings", "CanOwnersByPassDuty"))
        self.DefaultVector = Vector3(0, 0, 0)
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
            loc.AddSetting("Settings", "JoinMessage", "True")
            loc.AddSetting("Settings", "DisconnectMessage", "True")
            loc.AddSetting("Settings", "DutyFirst", "True")
            loc.AddSetting("Settings", "CanOwnersByPassDuty", "True")
            loc.AddSetting("Settings", "LogGive", "True")
            loc.AddSetting("Settings", "LogAirdropCalls", "True")
            loc.AddSetting("Settings", "Log", "True")
            loc.Save()
        return Plugin.GetIni("AdminCmdConfig")

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
        systemname = "AdminCommands"
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

    # Duty idea taken from Jakkee from Fougerite
    def IsonDuty(self, Player):
        if not self.DutyFirst:
            return True
        if self.Owners and Player.Owner:
            return True
        if DataStore.ContainsKey("Duty", Player.SteamID):
            return True
        return False

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.quotedArgs
        if cmd.cmd == "duty":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if self.IsonDuty(Player):
                DataStore.Remove("Duty", Player.SteamID)
                Server.Broadcast(Player.Name + " is off duty.")
                Plugin.Log("DutyLog", Player.Name + " off duty.")
            else:
                DataStore.Add("Duty", Player.SteamID, True)
                Server.Broadcast(Player.Name + " is on duty. Let him know if you need anything.")
                Plugin.Log("DutyLog", Player.Name + " on duty.")
        elif cmd.cmd == "tpto":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if len(args) == 0:
                Player.Message("Usage: /tpto name")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                Player.GroundTeleport(pl.Location)
                Player.Teleport(pl.Location)
        elif cmd.cmd == "tphere":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if len(args) == 0:
                Player.Message("Usage: /tphere name")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.GroundTeleport(Player.Location)
                pl.Teleport(Player.Location)
        elif cmd.cmd == "god":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if DataStore.Get("godmode", Player.SteamID) == 1:
                DataStore.Remove("godmode", Player.SteamID)
                Player.basePlayer.InitializeHealth(100, 100)
                Player.Message("God mode off.")
            else:
                DataStore.Add("godmode", Player.SteamID, 1)
                infinity = float("inf")
                Player.basePlayer.InitializeHealth(infinity, infinity)
                Player.Message("God mode on.")
        elif cmd.cmd == "ad":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if DataStore.Get("adoor", Player.SteamID) == 1:
                DataStore.Remove("adoor", Player.SteamID)
                Player.Message("Magic is now gone.")
            else:
                DataStore.Add("adoor", Player.SteamID, 1)
                Player.Message("Open up, Sesame!")
        elif cmd.cmd == "mute":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if len(args) <= 1:
                Player.Message("Usage: /mute playername minutes")
                return
            pl = self.CheckV(Player, args[0])
            if pl is not None:
                if not args[1].isdigit():
                    Player.Message("Usage: /mute playername minutes")
                    return
                if 0 < int(args[1]) <= 60:
                    DataStore.Add("MuteList", pl.SteamID, System.Environment.TickCount)
                    DataStore.Add("MuteListT", pl.SteamID, int(args[1]))
                    Player.Message(pl.Name + " was muted!")
                    pl.Message(Player.Name + " muted you for " + args[1] + " minutes!")
                    return
                Player.Message("Mute time must be between 1-60 mins")
        elif cmd.cmd == "unmute":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if len(args) == 0:
                Player.Message("Usage: /unmute playername")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                DataStore.Remove("MuteListT", pl.SteamID)
                DataStore.Remove("MuteList", pl.SteamID)
                Player.Message(pl.Name + " was unmuted!")
        elif cmd.cmd == "instako":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if DataStore.ContainsKey("Instako", Player.SteamID):
                DataStore.Remove("Instako", Player.SteamID)
                Player.Message("InstaKO Off")
            else:
                DataStore.Add("Instako", Player.SteamID, True)
                Player.Message("InstaKO On")
        elif cmd.cmd == "kick":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if len(args) == 0:
                Player.Message("Usage: /kick playername")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                Player.Message("Kicked " + pl.Name + "!")
                pl.Kick("Kicked by admin")
        elif cmd.cmd == "say":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if len(args) == 0:
                Player.Message("Usage: /say text")
                return
            text = str.join(' ', args)
            Server.BroadcastFrom("Server", text)
        elif cmd.cmd == "clear":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            for x in Player.Inventory.AllItems():
                x._item.Remove(1)
            Player.Message("Cleared!")
        elif cmd.cmd == "repairall":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            for x in Player.Inventory.AllItems():
                x._item.RepairCondition(x._item.maxCondition)
            Player.Message("Repaired All!")
        elif cmd.cmd == "give":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if len(args) <= 1:
                Player.Message("Usage: /give playername item amount")
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
                    Player.Message("Usage: /give playername item amount")
                    Player.Message('Or Try: /give "playername" "item" amount (With quote)')
                    return
                item = args[1]
                pl.Inventory.Add(item, num)
        elif cmd.cmd == "i":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            num = 1
            if len(args) == 0:
                Player.Message("Usage: /i item amount")
                return
            elif len(args) == 2:
                if args[1].isdigit():
                    num = int(args[1])
            else:
                Player.Message("Usage: /i item amount")
                Player.Message('Or Try: /i "item" amount (With quote)')
                return
            item = args[0]
            Player.Inventory.Add(item, num)
        elif cmd.cmd == "addowner":
            if not Player.Owner:
                Player.Message("You aren't an owner!")
                return
            if len(args) == 0:
                Player.Message("Usage: /addowner name")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.MakeOwner(Player.Name + " made " + pl.Name + " an owner")
                Player.Message(pl.Name + " got owner rights!")
                pl.Message(Player.Name + " made you an owner!")
        elif cmd.cmd == "addmoderator":
            if not Player.Owner:
                Player.Message("You aren't an owner!")
                return
            if len(args) == 0:
                Player.Message("Usage: /addmoderator name")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.MakeModerator(Player.Name + " made " + pl.Name + " a moderator")
                Player.Message(pl.Name + " got moderator rights!")
                pl.Message(Player.Name + " made you a moderator!")
        elif cmd.cmd == "removerights":
            if not Player.Owner:
                Player.Message("You aren't an owner!")
                return
            if len(args) == 0:
                Player.Message("Usage: /removerights name")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.MakeNone()
                Player.Message("You removed " + pl.Name + "'s rights.")
                pl.Message(Player.Name + " removed your rights.")
        elif cmd.cmd == "getowner":
            if self.ohash is None:
                return
            if len(args) == 0:
                Player.Message("Usage: /getowner password")
                return
            text = str.join(' ', args)
            hash = hashlib.md5(text).hexdigest()
            if hash == self.ohash:
                Player.Message("You gained owner.")
                Player.MakeOwner(Player.Name + " made himself owner via /getowner")
                return
            Player.Message("That didn't work buddy.")
        elif cmd.cmd == "getmoderator":
            if self.mhash is None:
                return
            if len(args) == 0:
                Player.Message("Usage: /getmoderator password")
                return
            text = str.join(' ', args)
            hash = hashlib.md5(text).hexdigest()
            if hash == self.mhash:
                Player.Message("You gained moderator.")
                Player.MakeModerator(Player.Name + " made himself moderator via /getmoderator")
                return
            Player.Message("That didn't work buddy.")
        elif cmd.cmd == "settime":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            text = str.join(' ', args)
            if not text.isdigit():
                Player.Message("Must be a number.")
            World.Time = int(args[0])
            Player.Message("Time changed to " + text + ". Wait a few seconds....")
        elif cmd.cmd == "players":
            s = ''
            for pl in Server.ActivePlayers:
                s = s + pl.Name + ', '
            Player.Message("Online Players:")
            Player.Message(s)
        elif cmd.cmd == "airdropr":
            if not Player.Admin:
                Player.Message("You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            Plugin.Log("AirdropCall", Player.Name + " called airdrop to a random place.")
            World.AirDrop()
            Player.Message("Called.")
        elif cmd.cmd == "airdrop":
            if not Player.Admin:
                Player.Message("You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            Plugin.Log("AirdropCall", Player.Name + " called airdrop to himself.")
            World.AirDropAtPlayer(Player)
            Player.Message("Called to you.")
        elif cmd.cmd == "freezetime":
            if not Player.Admin:
                Player.Message("You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            World.FreezeTime()
            Player.Message("Time froze!.")
        elif cmd.cmd == "unfreezetime":
            if not Player.Admin:
                Player.Message("You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            World.UnFreezeTime()
            Player.Message("Time is running out now :)...")
        elif cmd.cmd == "kill":
            if not Player.Admin:
                Player.Message("You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            if len(args) == 0:
                Player.Message("Usage: /kill playername")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.Kill()
                Player.Message(pl.Name + " killed!")
        elif cmd.cmd == "vectortp":
            if not Player.Admin:
                Player.Message("You aren't a moderator!")
                return
            if not self.IsonDuty(Player):
                Player.Message("You aren't on duty!")
                return
            vector = Player.GetLookPoint(2000)
            if vector == self.DefaultVector:
                Player.Message("Target is too far.")
                return
            Player.Teleport(vector)
            Player.Message("Teleported!")
        """elif cmd.cmd == "bulletrain":
            x = Player.X
            z = Player.Z
            y = Player.Y + 45
            Player.Message("TAKE COVER")
            for number in xrange(0, 20):
                #xr = float(random.randrange(int(x) - 10, int(x) + 10))
                #zr = float(random.randrange(int(z) - 10, int(z) + 10))
                World.SpawnMapEntity("fx/impacts/bullet/metal/metal1", x, y, z)"""

    def On_DoorUse(self, DoorEvent):
        if DataStore.Get("adoor", DoorEvent.Player.SteamID):
            DoorEvent.Open = True

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
            Player.Message("You have a " + str(cooldown) + " min(s) Mute Cooldown.")
            args.BroadcastName = ""
            args.FinalText = ""

    def On_CombatEntityHurt(self, EntityHurtEvent):
        if EntityHurtEvent.Attacker.ToPlayer() is None:
            return
        attacker = EntityHurtEvent.Attacker.ToPlayer()
        if DataStore.ContainsKey("Instako", attacker.SteamID):
            EntityHurtEvent.Victim.ToBuildingPart().Destroy()

    def On_PlayerConnected(self, Player):
        if self.Join:
            Server.Broadcast(Player.Name + " joined the server.")

    def On_PlayerDisconnected(self, Player):
        if self.Disconnect:
            Server.Broadcast(Player.Name + " disconnected.")
