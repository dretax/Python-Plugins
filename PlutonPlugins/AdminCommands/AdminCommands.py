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
            loc.AddSetting("Help", "AKitNames", "starter, admin, builder")
            loc.AddSetting("Help", "PKitNames", "starter")
            loc.AddSetting("Settings", "EnableKits", "0")
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
            enablekits = int(ini.GetSetting("Settings", "EnableKits"))
            kitsl = ini.GetSetting("Settings", "AKitNames")
            if enablekits == 0:
                return
            if Player.Admin:
                if len(args) == 0:
                    Player.Message(kitsl)
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
        elif cmd.cmd == "god":
            if not Player.Admin:
                Player.Message("You aren't an admin!")
                return
            if args[0] == "on":
                DataStore.Add("godmode", Player.SteamID, 1)
                Player.Message("God mode on.")
            elif args[0] == "off":
                DataStore.Add("godmode", Player.SteamID, 0)
                Player.Message("God mode off.")


    def On_PlayerAttacked(self, PlayerHurtEvent):
         if PlayerHurtEvent.Attacker.ToPlayer().displayName is not None:
                get = DataStore.Get("godmode", PlayerHurtEvent.Victim.SteamID)
                if get is not None and get == 1:
                    PlayerHurtEvent.DamageAmount  = 0