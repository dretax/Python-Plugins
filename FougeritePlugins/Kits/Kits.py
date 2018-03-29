__author__ = 'DreTaX'
__version__ = '1.2'

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

    Enabled = True
    Cooldown = 0
    AdminCanUse = False
    ModeratorCanUse = False
    NormalCanUse = False
    AutoGiveOnSpawn = False
    AdminCanBypassCooldown = False
    ModeratorCanBypassCooldown = False
    ClearInvOnUse = False
    ItemsDict = None

    def __init__(self, Enabled, Cooldown, AdminCanUse, ModeratorCanUse, NormalCanUse, ItemsDict, AutoGiveOnSpawn,
                 AdminCanBypassCooldown, ModeratorCanBypassCooldown, ClearInvOnUse):
        self.Enabled = Enabled
        self.Cooldown = Cooldown
        self.AdminCanUse = AdminCanUse
        self.ModeratorCanUse = ModeratorCanUse
        self.NormalCanUse = NormalCanUse
        self.AutoGiveOnSpawn = AutoGiveOnSpawn
        self.AdminCanBypassCooldown = AdminCanBypassCooldown
        self.ModeratorCanBypassCooldown = ModeratorCanBypassCooldown
        self.ClearInvOnUse = ClearInvOnUse
        self.ItemsDict = ItemsDict

KitStore = {

}


class Kits:

    def On_PluginInit(self):
        Files = System.IO.Directory.GetFiles(path + "\\Save\\PyPlugins\\Kits\\\LoadOuts\\", "*.ini",
                                             System.IO.SearchOption.AllDirectories)
        for x in Files:
            self.GetKitDataWithPath(x)

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
            Enabled = self.bool(kit.GetSetting("Kit", "Enabled"))
            Cooldown = int(kit.GetSetting("Kit", "Cooldown"))
            Admin = self.bool(kit.GetSetting("Kit", "AdminCanUse"))
            Moderator = self.bool(kit.GetSetting("Kit", "ModeratorCanUse"))
            Normal = self.bool(kit.GetSetting("Kit", "NormalCanUse"))
            AutoGiveOnSpawn = self.bool(kit.GetSetting("Kit", "AutoGiveOnSpawn"))
            AdminCanBypassCooldown = self.bool(kit.GetSetting("Kit", "AdminCanBypassCooldown"))
            ModeratorCanBypassCooldown = self.bool(kit.GetSetting("Kit", "ModeratorCanBypassCooldown"))
            ClearInvOnUse = self.bool(kit.GetSetting("Kit", "ClearInvOnUse"))
            Items = kit.EnumSection("Items")
            dictt = {}
            for x in Items:
                l = int(kit.GetSetting("Items", x))
                dictt[x] = l
            c = GivenKit(Enabled, Cooldown, Admin, Moderator, Normal, dictt, AutoGiveOnSpawn, AdminCanBypassCooldown,
                         ModeratorCanBypassCooldown, ClearInvOnUse)
            KitStore[name] = c
            return c
        return None

    def GetKitDataWithPath(self, path):
        name = System.IO.GetFileName(path)
        if name in KitStore.keys():
            return KitStore[name]
        kit = Plugin.GetIni(path)
        if kit is not None:
            Enabled = self.bool(kit.GetSetting("Kit", "Enabled"))
            Cooldown = int(kit.GetSetting("Kit", "Cooldown"))
            Admin = self.bool(kit.GetSetting("Kit", "AdminCanUse"))
            Moderator = self.bool(kit.GetSetting("Kit", "ModeratorCanUse"))
            Normal = self.bool(kit.GetSetting("Kit", "NormalCanUse"))
            AutoGiveOnSpawn = self.bool(kit.GetSetting("Kit", "AutoGiveOnSpawn"))
            AdminCanBypassCooldown = self.bool(kit.GetSetting("Kit", "AdminCanBypassCooldown"))
            ModeratorCanBypassCooldown = self.bool(kit.GetSetting("Kit", "ModeratorCanBypassCooldown"))
            ClearInvOnUse = self.bool(kit.GetSetting("Kit", "ClearInvOnUse"))
            Items = kit.EnumSection("Items")
            dictt = {}
            for x in Items:
                l = int(kit.GetSetting("Items", x))
                dictt[x] = l
            c = GivenKit(Enabled, Cooldown, Admin, Moderator, Normal, dictt, AutoGiveOnSpawn, AdminCanBypassCooldown,
                         ModeratorCanBypassCooldown, ClearInvOnUse)
            KitStore[name] = c
            return c
        return

    def GiveKit(self, data, inventory):
        for x in data.ItemsDict.keys():
            inventory.AddItem(x, data.ItemsDict[x])

    def On_PlayerSpawned(self, Player, SpawnEvent):
        for name, x in KitStore.iteritems():
            if x.AutoGiveOnSpawn:
                if x.Cooldown > 0:
                    if (Player.Admin and x.AdminCanBypassCooldown) or (Player.Moderator and x.ModeratorCanBypassCooldown):
                        inv = Player.Inventory
                        if x.ClearInvOnUse:
                            inv.Clear()
                        self.GiveKit(x, inv)
                        continue
                    cooldown = x.Cooldown / 60000 * 60
                    systick = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds
                    time = DataStore.Get("KitCooldown" + name, Player.UID)
                    if time is None:
                        DataStore.Add("KitCooldown" + name, Player.UID, 7)
                        time = 7
                    calc = systick - time
                    if calc < cooldown and time != 7:
                        done = round(calc)
                        done2 = round(cooldown, 2)
                        Player.MessageFrom("Kits", "Time Remaining for " + name + " : "
                                           + str(done) + " / " + str(done2) + " seconds")
                        continue
                inv = Player.Inventory
                if x.ClearInvOnUse:
                    inv.Clear()
                self.GiveKit(x, inv)

    def On_Command(self, Player, cmd, args):
        if cmd == "kit" or cmd == "kits":
            if len(args) == 0 or len(args) > 1:
                kitnames = ""
                for x in KitStore.keys():
                    kitnames = kitnames + x + ", "
                Player.MessageFrom("Kits", "Available Kits: " + kitnames)
                Player.MessageFrom("Kits", "Commands: /kit kitname")
                return
            inv = Player.Inventory
            if Player.Admin or Player.Moderator:
                data = self.GetKitData(args[0])
                if data is not None:
                    if not data.Enabled:
                        Player.MessageFrom("Kits", "This kit has been disabled.")
                        return
                    if (Player.Admin and data.AdminCanUse) or (Player.Moderator and data.ModeratorCanUse):
                        # If our Player is an admin and cannot bypass the Kit's Cooldown.
                        if Player.Admin and data.AdminCanUse and data.Cooldown > 0 and not data.AdminCanBypassCooldown:
                            cooldown = data.Cooldown / 60000 * 60
                            systick = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds
                            time = DataStore.Get("KitCooldown" + str(args[0]), Player.UID)
                            if time is None:
                                DataStore.Add("KitCooldown" + str(args[0]), Player.UID, 7)
                                time = 7
                            calc = systick - time
                            if calc < cooldown and time != 7:
                                Player.MessageFrom("Kits", "You have to wait before using this again!")
                                done = round(calc)
                                done2 = round(cooldown, 2)
                                Player.MessageFrom("Kits", "Time Remaining: " + str(done) + " / " + str(done2) +
                                                   " seconds")
                                return
                            DataStore.Add("KitCooldown" + str(args[0]), Player.UID,
                                          TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds)
                        # If our Player is a Moderator and cannot bypass the Kit's Cooldown.
                        if Player.Moderator and not Player.Admin and data.ModeratorCanUse and data.Cooldown > 0 \
                                and not data.ModeratorCanBypassCooldown:
                            cooldown = data.Cooldown / 60000 * 60
                            systick = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds
                            time = DataStore.Get("KitCooldown" + str(args[0]), Player.UID)
                            if time is None:
                                DataStore.Add("KitCooldown" + str(args[0]), Player.UID, 7)
                                time = 7
                            calc = systick - time
                            if calc < cooldown and time != 7:
                                Player.MessageFrom("Kits", "You have to wait before using this again!")
                                done = round(calc)
                                done2 = round(cooldown, 2)
                                Player.MessageFrom("Kits", "Time Remaining: " + str(done) + " / " + str(done2) +
                                                   " seconds")
                                return
                            DataStore.Add("KitCooldown" + str(args[0]), Player.UID,
                                          TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds)
                        if data.ClearInvOnUse:
                            inv.Clear()
                        self.GiveKit(data, inv)
                        Player.MessageFrom("Kits", "Kit " + args[0] + " received!")
                    else:
                        Player.MessageFrom("Kits", "You can't use this!")
                else:
                    Player.MessageFrom("Kits", "Kit " + args[0] + " not found!")
            else:
                data = self.GetKitData(args[0])
                if data is None:
                    Player.MessageFrom("Kits", "Kit " + str(args[0]) + " not found!")
                    return
                if not data.Enabled:
                    Player.MessageFrom("Kits", "This kit has been disabled.")
                    return
                if not data.NormalCanUse:
                    Player.MessageFrom("Kits", "You can't get this!")
                    return
                if data.Cooldown > 0:
                    cooldown = data.Cooldown / 60000 * 60
                    systick = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds
                    time = DataStore.Get("KitCooldown" + str(args[0]), Player.UID)
                    if time is None:
                        DataStore.Add("KitCooldown" + str(args[0]), Player.UID, 7)
                        time = 7
                    calc = systick - time
                    if calc >= cooldown or time == 7:
                        if data.ClearInvOnUse:
                            inv.Clear()
                        self.GiveKit(data, inv)
                        Player.MessageFrom("Kits", "Kit " + args[0] + " received!")
                        DataStore.Add("KitCooldown" + str(args[0]), Player.UID,
                                      TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds)
                    else:
                        Player.MessageFrom("Kits", "You have to wait before using this again!")
                        done = round(calc)
                        done2 = round(cooldown, 2)
                        Player.MessageFrom("Kits", "Time Remaining: " + str(done) + " / " + str(done2) + " seconds")
                else:
                    self.GiveKit(data, inv)
                    Player.MessageFrom("Kits", "Kit " + args[0] + " received!")
        elif cmd == "flushkit":
            if Player.Admin:
                if len(args) == 0:
                    Player.MessageFrom("Kits", "/flushkit kitname")
                    return
                text = str.join("", args)
                DataStore.Flush("KitCooldown" + text)
                Player.MessageFrom("Kits", "Flushed all cooldowns for " + text + "!")
        elif cmd == "reloadkits":
            if Player.Admin:
                KitStore.clear()
                Files = System.IO.Directory.GetFiles(path + "\\Save\\PyPlugins\\Kits\\\LoadOuts\\", "*.ini",
                                                     System.IO.SearchOption.AllDirectories)
                for x in Files:
                    self.GetKitDataWithPath(x)
                Player.MessageFrom("Kits", "Reloaded all kits!")