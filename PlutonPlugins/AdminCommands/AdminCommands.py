__author__ = 'DreTaX'
__version__ = '1.0'

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
            loc.AddSetting("Help", "KitNames", "starter, admin, builder")
            loc.AddSetting("Settings", "Time", "2400000")
            loc.Save()
        return Plugin.GetIni("AdminCmdConfig")

    # method by Illuminati
    def CheckV(self, Player, args):
        systemname = "Admin Commands"
        p = Server.FindPlayer(String.Join(" ", args))
        if p is not None:
            return p

        count = 0
        for pl in Server.ActivePlayers:
            for namePart in args:
                if namePart in pl.Name:
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.MessageFrom(systemname, String.Format("Couldn't find {0}!", String.Join(" ", args)))
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(systemname, String.Format("Found {0} player with similar name. Use more correct name!"))
            return None

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        ini = self.AdminCmdConfig()
        if cmd.cmd == "kit":
            if Player.Admin:
                if len(args) == 0:
                    Player.Message("Available kits: starter, admin, builder")
                    return
                if Server.LoadOuts.ContainsKey(args[0]):
                    loadout = Server.LoadOuts[args[0]]
                    loadout.ToInv(Player.Inventory)
                    return
                else:
                    Player.Message("Kit " + str(cmd.args[0]) + " not found!")
                    return
            else:
                if len(args) == 0:
                    Player.Message("Available kits: starter")
                    return
                cooldown = int(ini.GetSetting("Settings", "Time"))
                if cooldown > 0:
                    systick = System.Environment.TickCount
                    time = DataStore.Get("startercooldown", Player.SteamID)
                    if time is None or (systick - time) < 0 or math.isnan(systick - time):
                        DataStore.Add("startercooldown", Player.SteamID, 7)
                    calc = systick - time
                    if calc >= cooldown or time == 7:
                        loadout = Server.LoadOuts["starter"]
                        loadout.ToInv(Player.Inventory)
                        DataStore.Add("startercooldown", Player.SteamID, System.Environment.TickCount)
                    else:
                        Player.Message("You have to wait before using this again!")
                        done = round((calc / 1000) / 60, 2)
                        done2 = round((cooldown / 1000) / 60, 2)
                        Player.Message("Time Remaining: " + str(done) + "/" + str(done2) + " minutes")
                else:
                    loadout = Server.LoadOuts["starter"]
                    loadout.ToInv(Player.Inventory)

        elif cmd.cmd == "tpto":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                Player.GroundTeleport(pl.Location)
                Player.Teleport(pl.Location)
        elif cmd.cmd == "tphere":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            pl = self.CheckV(Player, args)
            if pl is not None:
                pl.GroundTeleport(Player.Location)
                pl.Teleport(Player.Location)