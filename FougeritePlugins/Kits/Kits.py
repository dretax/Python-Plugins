__author__ = 'DreTaX'
__version__ = '1.0'

import clr
clr.AddReferenceByPartialName("Fougerite")

import Fougerite
import System
from System import *
import re
import math

path = Util.GetRootFolder()

"""
    Storing Kit Data in a class.
"""


class GivenKit:

    AdminCanUse = False
    ModeratorCanUse = False
    NormalCanUse = False
    ItemsDict = None

    def __init__(self, AdminCanUse, ModeratorCanUse, NormalCanUse, ItemsDict):
        self.AdminCanUse = AdminCanUse
        self.ModeratorCanUse = ModeratorCanUse
        self.NormalCanUse = NormalCanUse
        self.ItemsDict = ItemsDict

KitStore = {

}


class Kits:

    def KitsConfig(self):
        if not Plugin.IniExists("KitsConfig"):
            loc = Plugin.CreateIni("KitsConfig")
            loc.AddSetting("AdminKits", "AvailableKits", "starter, admin")
            loc.AddSetting("PlayerKits", "AvailableKits", "starter:120000")
            # loc.AddSetting("PlayerKits", "DefaultKits", "starter:True,AdminKit:False")
            loc.Save()
        return Plugin.GetIni("KitsConfig")

    def On_PluginInit(self):
        self.KitsConfig()

    def GetStringFromArray(self, Array, String):
        matching = str([s for s in Array if String in s])
        return matching

    def bool(self, s):
        if s is None:
            raise ValueError("[Kits] Config value is empty!")
        elif s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            raise ValueError("[Kits] Config value is not a boolean!")

    def GetKitData(self, name):
        if name in KitStore.keys():
            return KitStore[name]
        kit = Plugin.GetIni(path + "\\Save\\PyPlugins\\Kits\\\LoadOuts\\" + name)
        if kit is not None:
            Admin = self.bool(kit.GetSetting("Kit", "AdminCanUse"))
            Moderator = self.bool(kit.GetSetting("Kit", "ModeratorCanUse"))
            Normal = self.bool(kit.GetSetting("Kit", "NormalCanUse"))
            Items = kit.EnumSection("Items")
            dictt = {}
            for x in Items:
                l = int(kit.GetSetting("Items", x))
                dictt[x] = l
            c = GivenKit(Admin, Moderator, Normal, dictt)
            KitStore[name] = c
            return c
        return None

    def On_Command(self, Player, cmd, args):
        if cmd == "kit" or cmd == "kits":
            ini = self.KitsConfig()
            if Player.Admin or Player.Moderator:
                akits = ini.GetSetting("AdminKits", "AvailableKits")
                if len(args) == 0:
                    Player.MessageFrom("Kits", "Available Kits: " + akits)
                    Player.MessageFrom("Kits", "Commands: /kit kitname")
                    return
                data = self.GetKitData(args[0])
                if data is not None:
                    if (Player.Admin and data.AdminCanUse) or (Player.Moderator and data.ModeratorCanUse):
                        inv = Player.Inventory
                        for x in data.ItemsDict.keys():
                            inv.AddItem(x, data.ItemsDict[x])
                        Player.MessageFrom("Kits", "Kit " + args[0] + " received!")
                    else:
                        Player.MessageFrom("Kits", "You can't use this!")
                else:
                    Player.MessageFrom("Kits", "Kit " + args[0] + " not found!")
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
                data = self.GetKitData(args[0])
                if data is None:
                    Player.MessageFrom("Kits", "Kit " + str(args[0]) + " not found!")
                    return
                if not data.NormalCanUse:
                    Player.MessageFrom("Kits", "You can't get this!")
                    return
                get = self.GetStringFromArray(array, str(args[0]))
                get = re.sub('[[\]\']+', '', get).split(':')
                cooldown = int(get[1])
                if cooldown > 0:
                    systick = System.Environment.TickCount
                    if DataStore.Get("startercooldown" + str(args[0]), Player.SteamID) is None:
                        DataStore.Add("startercooldown" + str(args[0]), Player.SteamID, 7)
                    time = DataStore.Get("startercooldown" + str(args[0]), Player.SteamID)
                    if (systick - time) < 0 or math.isnan(systick - time):
                        DataStore.Add("startercooldown" + str(args[0]), Player.SteamID, 7)
                        time = 7
                    calc = systick - time
                    if calc >= cooldown or time == 7:
                        inv = Player.Inventory
                        for x in data.ItemsDict.keys():
                            inv.AddItem(x, data.ItemsDict[x])
                        Player.MessageFrom("Kits", "Kit " + args[0] + " received!")
                        DataStore.Add("startercooldown" + str(args[0]), Player.SteamID, System.Environment.TickCount)
                    else:
                        Player.MessageFrom("Kits", "You have to wait before using this again!")
                        done = round((calc / 1000) / 60, 2)
                        done2 = round((cooldown / 1000) / 60, 2)
                        Player.MessageFrom("Kits", "Time Remaining: " + str(done) + "/" + str(done2) + " minutes")
                else:
                    inv = Player.Inventory
                    for x in data.ItemsDict.keys():
                        inv.AddItem(x, data.ItemsDict[x])
                    Player.MessageFrom("Kits", "Kit " + args[0] + " received!")
