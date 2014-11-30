__author__ = 'DreTaX'
__version__ = '1.4'

import clr

clr.AddReferenceByPartialName("Pluton")
import Pluton
import math
import System
from System import *
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
            loc.AddSetting("PlayerKits", "DefaultKits", "starter:True,DreTaX:False")
            loc.Save()
        return Plugin.GetIni("KitsConfig")

    def On_PluginInit(self):
        self.KitsConfig()

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
        systemname = "Kits"
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
                    Player.MessageFrom("Kits", "Commands: /setdefaultkit kitname | /givekit playername")
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
        elif cmd.cmd == "givekit":
            if Player.Admin:
                if len(args) <= 1:
                    Player.MessageFrom("Kits", 'Usage: /givekit "playername" "kitname"')
                    return
                playerr = self.CheckV(Player, args[0])
                if playerr is None:
                    return
                kit = args[1]
                if Server.LoadOuts.ContainsKey(kit):
                    Player.MessageFrom("Kits", "This Kit doesn't exist!")
                    return
                loadout = Server.LoadOuts[kit]
                loadout.ToInv(Player.Inventory)
                Player.MessageFrom("Kits", playerr.Name + " Received the kit: " + kit)
                playerr.MessageFrom("Kits", "You received a kit: " + kit)

        elif cmd.cmd == "setdefaultkit":
            if Player.Admin:
                if len(args) == 0:
                    Player.MessageFrom("Kits", "Usage: /setdefaultkit name")
                    return
                DataStore.Add("AdminKit", Player.SteamID, args[0])
                Player.MessageFrom("Kits", "DefaultKit " + str(args[0]) + " set!")

    def DelayCallback(self, timer):
        timer.Kill()
        Delay = timer.Args
        Player = Server.FindPlayer(Delay["Player"])
        if Player is None:
            return
        self.GiveRespawnKit(Player)

    def GiveRespawnKit(self, Player):
        Ini = self.KitsConfig()
        values = Ini.GetSetting("PlayerKits", "DefaultKits")
        array = values.split(',')
        if Player.Admin:
            akit = DataStore.Get("AdminKit", Player.SteamID)
            if akit is not None:
                loadout = Server.LoadOuts[akit]
                loadout.ToInv(Player.Inventory)
        else:
            pkits = Ini.GetSetting("PlayerKits", "AvailableKits").split(',')
            for kit in array:
                get = self.GetStringFromArray(array, str(kit))
                get = re.sub('[[\]\']+', '', get).split(':')
                if not Server.LoadOuts.ContainsKey(get[0]):
                    continue
                d = bool(get[1])
                if d:
                    loadout = Server.LoadOuts[get[0]]
                    loadout.ToInv(Player.Inventory)
                else:
                    cd = self.GetStringFromArray(pkits, get[0])
                    cd = re.sub('[[\]\']+', '', cd).split(':')
                    cooldown = int(cd[1])
                    if cooldown > 0:
                        systick = System.Environment.TickCount
                        if DataStore.Get("startercooldown"+str(get[0]), Player.SteamID) is None:
                            DataStore.Add("startercooldown"+str(get[0]), Player.SteamID, 7)
                        time = DataStore.Get("startercooldown"+str(get[0]), Player.SteamID)
                        if (systick - time) < 0 or math.isnan(systick - time):
                            DataStore.Add("startercooldown"+str(get[0]), Player.SteamID, 7)
                            time = 7
                        calc = systick - time
                        if calc >= cooldown or time == 7:
                            loadout = Server.LoadOuts[get[0]]
                            loadout.ToInv(Player.Inventory)
                            DataStore.Add("startercooldown"+str(get[0]), Player.SteamID, System.Environment.TickCount)
                        else:
                            done = round((calc / 1000) / 60, 2)
                            done2 = round((cooldown / 1000) / 60, 2)
                            Player.MessageFrom("Kits", str(get[0]) + " is still on cooldown: " + str(done) + "/" + str(done2) + " minutes")

    def On_Respawn(self, RespawnEvent):
        Delay = Plugin.CreateDict()
        Delay["Player"] = RespawnEvent.Player.SteamID
        c = 5 * 1000
        Plugin.CreateParallelTimer("Delay", c, Delay).Start()