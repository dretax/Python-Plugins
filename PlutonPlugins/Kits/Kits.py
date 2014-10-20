__author__ = 'DreTaX'
__version__ = '1.0'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import math
import System

"""
    Class
"""


class Kits:

    def KitsConfig(self):
        if not Plugin.IniExists("KitsConfig"):
            loc = Plugin.CreateIni("KitsConfig")
            loc.AddSetting("AdminKits", "AvailableKits", "starter, builder, admin")
            loc.AddSetting("PlayerKits", "AvailableKits", "starter")
            loc.AddSetting("PlayerKits", "Cooldown", "1200000")
            loc.Save()
        return Plugin.GetIni("KitsConfig")

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "kit":
            ini = self.KitsConfig()
            if Player.Admin:
                akits = ini.GetSetting("AdminKits", "AvailableKits")
                if len(args) == 0:
                    Player.MessageFrom("Kits", "Available Kits: " + akits)
                    return
                if Server.LoadOuts.ContainsKey(args[0]):
                    loadout = Server.LoadOuts[args[0]]
                    loadout.ToInv(Player.Inventory)
                    return
                else:
                    Player.Message("Kit " + str(args[0]) + " not found!")
                    return
            else:
                pkits = ini.GetSetting("PlayerKits", "AvailableKits")
                if len(args) == 0:
                    Player.MessageFrom("Kits", "Available Kits: " + pkits)
                    return
                cooldown = int(ini.GetSetting("PlayerKits", "Cooldown"))
                if cooldown > 0:
                    systick = System.Environment.TickCount
                    time = DataStore.Get("startercooldown", Player.SteamID)
                    if time is None or (systick - time) < 0 or math.isnan(systick - time):
                        DataStore.Add("startercooldown", Player.SteamID, 7)
                    calc = systick - time
                    if calc >= cooldown or time == 7:
                        if Server.LoadOuts.ContainsKey(args[0]):
                            loadout = Server.LoadOuts[args[0]]
                            loadout.ToInv(Player.Inventory)
                            DataStore.Add("startercooldown", Player.SteamID, System.Environment.TickCount)
                        else:
                            Player.Message("Kit " + str(args[0]) + " not found!")
                    else:
                        Player.Message("You have to wait before using this again!")
                        done = round((calc / 1000) / 60, 2)
                        done2 = round((cooldown / 1000) / 60, 2)
                        Player.Message("Time Remaining: " + str(done) + "/" + str(done2) + " minutes")
                else:
                    if Server.LoadOuts.ContainsKey(args[0]):
                        loadout = Server.LoadOuts[args[0]]
                        loadout.ToInv(Player.Inventory)
                    else:
                        Player.Message("Kit " + str(args[0]) + " not found!")