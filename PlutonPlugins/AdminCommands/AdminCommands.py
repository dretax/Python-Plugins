__author__ = 'DreTaX'
__version__ = '1.6'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import System
from System import *
import math

"""
    Class
"""


class AdminCommands:

    def AdminCmdConfig(self):
        if not Plugin.IniExists("AdminCmdConfig"):
            loc = Plugin.CreateIni("AdminCmdConfig")
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

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.quotedArgs
        if cmd.cmd == "tpto":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if len(args) == 0:
                Player.Message("Usage: /tpto name")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                Player.GroundTeleport(pl.Location)
                Player.Teleport(pl.Location)
        elif cmd.cmd == "tphere":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
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
            if len(args) == 0:
                Player.Message("Usage: /ad")
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
            if len(args) <= 1:
                Player.Message("Usage: /mute playername minutes")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                if not args[1].isdigit():
                    Player.Message("Usage: /mute playername minutes")
                    return
                if 0 < int(args[1]) <= 60:
                    DataStore.Add("MuteList", Player.SteamID, System.Environment.TickCount)
                    DataStore.Add("MuteListT", Player.SteamID, int(args[1]))
                    Player.Message(pl.Name + " was muted!")
                    pl.Message(Player.Name + " muted you for " + args[1] + " minutes!")
                    return
                Player.Message("Mute time must be between 1-60 mins")
        elif cmd.cmd == "unmute":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
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
            if len(args) == 0:
                Player.Message("Usage: /kick playername")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                Player.Message("Kicked " + pl.Name + "!")
                pl.Disconnect()
        elif cmd.cmd == "say":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if len(args) == 0:
                Player.Message("Usage: /say text")
                return
            text = str.join(' ', args)
            Server.BroadcastFrom("Server", text)

    def On_DoorUse(self, DoorEvent):
        if DataStore.Get("adoor", DoorEvent.Player.SteamID):
            DoorEvent.Open = True

    def On_Chat(self, Player, args):
        if DataStore.ContainsKey("MuteList", Player.SteamID):
            time = int(DataStore.Get("MuteListT", Player.SteamID))
            calc = System.Environment.TickCount - (time * 60000)
            if calc < 0 or math.isnan(calc) or math.isnan(time):
                DataStore.Remove("MuteListT", Player.SteamID)
                DataStore.Remove("MuteList", Player.SteamID)
                return
            if calc >= time * 60000:
                DataStore.Remove("MuteListT", Player.SteamID)
                DataStore.Remove("MuteList", Player.SteamID)
                return
            done = round((calc / 1000) / 60, 2)
            Player.Message("Mute Cooldown: " + str(done) + "/" + str(time))
            args.BroadcastName = ""
            args.FinalText = ""

    def On_CombatEntityHurt(self, EntityHurtEvent):
        if EntityHurtEvent.Attacker.ToPlayer() is None:
            return
        attacker = EntityHurtEvent.Attacker.ToPlayer()
        if DataStore.ContainsKey("Instako", attacker.SteamID):
            EntityHurtEvent.Victim.ToBuildingPart().Health = 0
