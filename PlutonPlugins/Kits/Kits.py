__author__ = 'DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import math
import System
import re

"""
    Class
"""


class Kits:

    def KitsConfig(self):
        if not Plugin.IniExists("KitsConfig"):
            loc = Plugin.CreateIni("KitsConfig")
            loc.AddSetting("AdminKits", "AvailableKits", "starter, builder, admin")
            loc.AddSetting("PlayerKits", "AvailableKits", "starter:120000,testkit:60000,DreTaX:99999")
            loc.Save()
        return Plugin.GetIni("KitsConfig")

    def GetStringFromArray(self, Array, String):
        matching = str([s for s in Array if String in s])
        return matching

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        if cmd.cmd == "kit" or cmd.cmd == "kits":
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
                array = pkits.split(',')
                if len(args) == 0:
                    leng = len(array)
                    i = 0
                    String = ''
                    for x in array:
                        if i <= leng:
                            x = x.split(':')
                            String = String + x[0] + ', '
                    Player.MessageFrom("Kits", "Available Kits: " + String)
                    return
                if not Server.LoadOuts.ContainsKey(args[0]):
                    Player.Message("Kit " + str(args[0]) + " not found!")
                    return
                get = self.GetStringFromArray(array, str(args[0]))
                get = re.sub('[[\]\']+', '', get).split(':')
                cooldown = int(get[1])
                if cooldown > 0:
                    systick = System.Environment.TickCount
                    if DataStore.Get("startercooldown"+str(args[0]), Player.SteamID) is None:
                        DataStore.Add("startercooldown"+str(args[0]), Player.SteamID, 7)
                    time = DataStore.Get("startercooldown"+str(args[0]), Player.SteamID)
                    if (systick - time) < 0 or math.isnan(systick - time):
                        DataStore.Add("startercooldown"+str(args[0]), Player.SteamID, 7)
                        time = 7
                    calc = systick - time
                    if calc >= cooldown or time == 7:
                        loadout = Server.LoadOuts[args[0]]
                        loadout.ToInv(Player.Inventory)
                        DataStore.Add("startercooldown"+str(args[0]), Player.SteamID, System.Environment.TickCount)
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