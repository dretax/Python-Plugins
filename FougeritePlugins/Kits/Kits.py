__author__ = 'DreTaX'
__version__ = '1.3.3'

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
    AdminCanBypassMaxUses = False
    ModeratorCanBypassMaxUses = False
    OnlyGiveOnSpawnIfHavingDefaultItems = True
    HowCanOneGetTheKit = 0
    MaxUses = 0
    ItemsDict = None

    def __init__(self, Enabled, Cooldown, AdminCanUse, ModeratorCanUse, NormalCanUse, ItemsDict, AutoGiveOnSpawn,
                 AdminCanBypassCooldown, ModeratorCanBypassCooldown, ClearInvOnUse, MaxUses, AdminCanBypassMaxUses,
                 ModeratorCanBypassMaxUses, OnlyGiveOnSpawnIfHavingDefaultItems, HowCanOneGetTheKit):
        self.Enabled = Enabled
        self.Cooldown = Cooldown
        self.AdminCanUse = AdminCanUse
        self.ModeratorCanUse = ModeratorCanUse
        self.NormalCanUse = NormalCanUse
        self.AutoGiveOnSpawn = AutoGiveOnSpawn
        self.AdminCanBypassCooldown = AdminCanBypassCooldown
        self.ModeratorCanBypassCooldown = ModeratorCanBypassCooldown
        self.ClearInvOnUse = ClearInvOnUse
        self.AdminCanBypassMaxUses = AdminCanBypassMaxUses
        self.ModeratorCanBypassMaxUses = ModeratorCanBypassMaxUses
        self.OnlyGiveOnSpawnIfHavingDefaultItems = OnlyGiveOnSpawnIfHavingDefaultItems
        self.HowCanOneGetTheKit = HowCanOneGetTheKit
        self.MaxUses = MaxUses
        self.ItemsDict = ItemsDict


"""
    Storing Item Data
"""


class ItemData:

    Amount = 1
    Slot = None

    def __init__(self, Amount, Slot):
        self.Amount = Amount
        self.Slot = Slot


KitStore = {

}


class Kits:

    def On_PluginInit(self):
        Files = System.IO.Directory.GetFiles(path + "\\Save\\PyPlugins\\Kits\\LoadOuts\\", "*.ini",
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
        name = name.lower()
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
            OnlyGiveOnSpawnIfHavingDefaultItems = self.bool(kit.GetSetting("Kit", "OnlyGiveOnSpawnIfHavingDefaultItems"))
            AdminCanBypassCooldown = self.bool(kit.GetSetting("Kit", "AdminCanBypassCooldown"))
            ModeratorCanBypassCooldown = self.bool(kit.GetSetting("Kit", "ModeratorCanBypassCooldown"))
            ClearInvOnUse = self.bool(kit.GetSetting("Kit", "ClearInvOnUse"))
            AdminCanBypassMaxUses = self.bool(kit.GetSetting("Kit", "AdminCanBypassMaxUses"))
            ModeratorCanBypassMaxUses = self.bool(kit.GetSetting("Kit", "ModeratorCanBypassMaxUses"))
            HowCanOneGetTheKit = int(kit.GetSetting("Kit", "HowCanOneGetTheKit"))
            MaxUses = int(kit.GetSetting("Kit", "MaxUses"))
            Items = kit.EnumSection("Items")
            dictt = {}
            for x in Items:
                itemdata = kit.GetSetting("Items", x)
                SlotToPlace = None
                if "," in itemdata:
                    itemdata = itemdata.split(",")
                    l = int(itemdata[0])
                    SlotToPlace = int(itemdata[1])
                else:
                    l = int(itemdata)
                dictt[x] = ItemData(l, SlotToPlace)
            c = GivenKit(Enabled, Cooldown, Admin, Moderator, Normal, dictt, AutoGiveOnSpawn, AdminCanBypassCooldown,
                         ModeratorCanBypassCooldown, ClearInvOnUse, MaxUses, AdminCanBypassMaxUses,
                         ModeratorCanBypassMaxUses, OnlyGiveOnSpawnIfHavingDefaultItems, HowCanOneGetTheKit)
            KitStore[name] = c
            return c
        return None

    def GetKitDataWithPath(self, ppath):
        name = System.IO.Path.GetFileNameWithoutExtension(ppath)
        tname = name.lower()
        if tname in KitStore.keys():
            return KitStore[tname]
        kit = Plugin.GetIni(path + "\\Save\\PyPlugins\\Kits\\\LoadOuts\\" + name)
        if kit is not None:
            Enabled = self.bool(kit.GetSetting("Kit", "Enabled"))
            Cooldown = int(kit.GetSetting("Kit", "Cooldown"))
            Admin = self.bool(kit.GetSetting("Kit", "AdminCanUse"))
            Moderator = self.bool(kit.GetSetting("Kit", "ModeratorCanUse"))
            Normal = self.bool(kit.GetSetting("Kit", "NormalCanUse"))
            AutoGiveOnSpawn = self.bool(kit.GetSetting("Kit", "AutoGiveOnSpawn"))
            OnlyGiveOnSpawnIfHavingDefaultItems = self.bool(kit.GetSetting("Kit", "OnlyGiveOnSpawnIfHavingDefaultItems"))
            AdminCanBypassCooldown = self.bool(kit.GetSetting("Kit", "AdminCanBypassCooldown"))
            ModeratorCanBypassCooldown = self.bool(kit.GetSetting("Kit", "ModeratorCanBypassCooldown"))
            ClearInvOnUse = self.bool(kit.GetSetting("Kit", "ClearInvOnUse"))
            AdminCanBypassMaxUses = self.bool(kit.GetSetting("Kit", "AdminCanBypassMaxUses"))
            ModeratorCanBypassMaxUses = self.bool(kit.GetSetting("Kit", "ModeratorCanBypassMaxUses"))
            HowCanOneGetTheKit = int(kit.GetSetting("Kit", "HowCanOneGetTheKit"))
            MaxUses = int(kit.GetSetting("Kit", "MaxUses"))
            Items = kit.EnumSection("Items")
            dictt = {}
            for x in Items:
                itemdata = kit.GetSetting("Items", x)
                SlotToPlace = None
                if "," in itemdata:
                    itemdata = itemdata.split(",")
                    l = int(itemdata[0])
                    SlotToPlace = int(itemdata[1])
                else:
                    l = int(itemdata)
                dictt[x] = ItemData(l, SlotToPlace)
            c = GivenKit(Enabled, Cooldown, Admin, Moderator, Normal, dictt, AutoGiveOnSpawn, AdminCanBypassCooldown,
                         ModeratorCanBypassCooldown, ClearInvOnUse, MaxUses, AdminCanBypassMaxUses,
                         ModeratorCanBypassMaxUses, OnlyGiveOnSpawnIfHavingDefaultItems, HowCanOneGetTheKit)
            KitStore[name.lower()] = c
            return c
        return None

    def GiveKit(self, data, inventory):
        for x in data.ItemsDict.keys():
            itemdata = data.ItemsDict[x]
            if itemdata.Slot is not None:
                inventory.AddItemTo(x, itemdata.Slot, itemdata.Amount)
            else:
                inventory.AddItem(x, itemdata.Amount)

    def On_PlayerSpawned(self, Player, SpawnEvent):
        for name, x in KitStore.iteritems():
            if not x.Enabled:
                continue
            if x.HowCanOneGetTheKit == 1:
                continue
            if x.AutoGiveOnSpawn:
                if x.OnlyGiveOnSpawnIfHavingDefaultItems:
                    string = str.join(", ", Player.Inventory.BarItems)
                    if "Rock" not in string or "Torch" not in string or \
                                    "Bandage" not in string:
                        continue
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
                kitnames = str.join(", ", KitStore.keys())
                kitnames = kitnames.lower()
                Player.MessageFrom("Kits", "Available Kits: " + kitnames)
                Player.MessageFrom("Kits", "Commands: /kit kitname")
                Player.MessageFrom("Kits", "/kituses kitname")
                return
            inv = Player.Inventory
            kitname = args[0].lower()
            if Player.Admin or Player.Moderator:
                data = self.GetKitData(kitname)
                if data is not None:
                    if not data.Enabled:
                        Player.MessageFrom("Kits", "This kit has been disabled.")
                        return
                    if data.HowCanOneGetTheKit == 2:
                        Player.MessageFrom("Kits", "This kit can only be received by spawning.")
                        return
                    CurrentUses = DataStore.Get("KitMaxUses" + kitname, Player.UID) or 0
                    if CurrentUses:
                        CurrentUses = int(CurrentUses)
                    if data.MaxUses > 0:
                        if (Player.Admin and data.AdminCanBypassMaxUses) or (Player.Moderator and data.ModeratorCanBypassMaxUses):
                            CurrentUses = None
                    if (Player.Admin and data.AdminCanUse) or (Player.Moderator and data.ModeratorCanUse):
                        # If our Player is an admin and cannot bypass the Kit's Cooldown.
                        if Player.Admin and data.AdminCanUse and data.Cooldown > 0 and not data.AdminCanBypassCooldown:
                            cooldown = data.Cooldown / 60000 * 60
                            systick = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds
                            time = DataStore.Get("KitCooldown" + kitname, Player.UID)
                            if time is None:
                                DataStore.Add("KitCooldown" + kitname, Player.UID, 7)
                                time = 7
                            calc = systick - time
                            if calc < cooldown and time != 7:
                                Player.MessageFrom("Kits", "You have to wait before using this again!")
                                done = round(calc)
                                done2 = round(cooldown, 2)
                                Player.MessageFrom("Kits", "Time Remaining: " + str(done) + " / " + str(done2) +
                                                   " seconds")
                                return
                            DataStore.Add("KitCooldown" + kitname, Player.UID,
                                          TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds)
                        # If our Player is a Moderator and cannot bypass the Kit's Cooldown.
                        if Player.Moderator and not Player.Admin and data.ModeratorCanUse and data.Cooldown > 0 \
                                and not data.ModeratorCanBypassCooldown:
                            cooldown = data.Cooldown / 60000 * 60
                            systick = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds
                            time = DataStore.Get("KitCooldown" + kitname, Player.UID)
                            if time is None:
                                DataStore.Add("KitCooldown" + kitname, Player.UID, 7)
                                time = 7
                            calc = systick - time
                            if calc < cooldown and time != 7:
                                Player.MessageFrom("Kits", "You have to wait before using this again!")
                                done = round(calc)
                                done2 = round(cooldown, 2)
                                Player.MessageFrom("Kits", "Time Remaining: " + str(done) + " / " + str(done2) +
                                                   " seconds")
                                return
                            DataStore.Add("KitCooldown" + kitname, Player.UID,
                                          TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds)
                        if data.ClearInvOnUse:
                            inv.Clear()
                        if data.MaxUses > 0 and CurrentUses:
                            if CurrentUses >= data.MaxUses:
                                Player.MessageFrom("Kits", "You have reached the maximum uses of this kit!")
                                return
                            DataStore.Add("KitMaxUses" + kitname, Player.UID, CurrentUses + 1)
                        self.GiveKit(data, inv)
                        Player.MessageFrom("Kits", "Kit " + kitname + " received!")
                    else:
                        Player.MessageFrom("Kits", "You can't use this!")
                else:
                    Player.MessageFrom("Kits", "Kit " + kitname + " not found!")
            else:
                data = self.GetKitData(kitname)
                if data is None:
                    Player.MessageFrom("Kits", "Kit " + kitname + " not found!")
                    return
                if not data.Enabled:
                    Player.MessageFrom("Kits", "This kit has been disabled.")
                    return
                if not data.NormalCanUse:
                    Player.MessageFrom("Kits", "You can't get this!")
                    return
                CurrentUses = DataStore.Get("KitMaxUses" + kitname, Player.UID) or 0
                if CurrentUses:
                    CurrentUses = int(CurrentUses)
                if data.Cooldown > 0:
                    cooldown = data.Cooldown / 60000 * 60
                    systick = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds
                    time = DataStore.Get("KitCooldown" + kitname, Player.UID)
                    if time is None:
                        DataStore.Add("KitCooldown" + kitname, Player.UID, 7)
                        time = 7
                    calc = systick - time
                    if calc >= cooldown or time == 7:
                        if data.ClearInvOnUse:
                            inv.Clear()
                        if data.MaxUses > 0 and CurrentUses:
                            DataStore.Add("KitMaxUses" + kitname, Player.UID, CurrentUses + 1)
                        self.GiveKit(data, inv)
                        Player.MessageFrom("Kits", "Kit " + kitname + " received!")
                        DataStore.Add("KitCooldown" + kitname, Player.UID,
                                      TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds)
                    else:
                        Player.MessageFrom("Kits", "You have to wait before using this again!")
                        done = round(calc)
                        done2 = round(cooldown, 2)
                        Player.MessageFrom("Kits", "Time Remaining: " + str(done) + " / " + str(done2) + " seconds")
                else:
                    if data.MaxUses > 0 and CurrentUses:
                        if CurrentUses >= data.MaxUses:
                            Player.MessageFrom("Kits", "You have reached the maximum uses of this kit!")
                            return
                        DataStore.Add("KitMaxUses" + kitname, Player.UID, CurrentUses + 1)
                    self.GiveKit(data, inv)
                    Player.MessageFrom("Kits", "Kit " + kitname + " received!")
        elif cmd == "flushkit":
            if Player.Admin:
                if len(args) == 0:
                    Player.MessageFrom("Kits", "/flushkit kitname")
                    return
                text = str.join("", args).lower()
                DataStore.Flush("KitCooldown" + text)
                Player.MessageFrom("Kits", "Flushed all cooldowns for " + text + "!")
        elif cmd == "clearmaxuses":
            if Player.Admin:
                if len(args) == 0 or len(args) > 2:
                    Player.MessageFrom("Kits", "Usages:")
                    Player.MessageFrom("Kits", "/clearmaxuses kitname all")
                    Player.MessageFrom("Kits", "/clearmaxuses kitname steamid")
                    Player.MessageFrom("Kits", "/clearmaxuses kitname playername")
                    return
                kitname = args[0].lower()
                value = args[1]
                if value == "all":
                    DataStore.Flush("KitMaxUses" + kitname)
                    Player.MessageFrom("Kits", "Cleared maxuses for kit: " + kitname)
                elif value.isdigit():
                    ulon = Data.ToUlong(value)
                    DataStore.Remove("KitMaxUses" + kitname, ulon)
                    Player.MessageFrom("Kits", "Cleared maxuses for kit: " + kitname + " SteamID: " + value)
                else:
                    player = Server.FindPlayer(value)
                    if player is None:
                        Player.MessageFrom("Kits", "Failed to find player.")
                        return
                    DataStore.Remove("KitMaxUses" + kitname, player.UID)
                    Player.MessageFrom("Kits", "Cleared maxuses for kit: " + kitname + " Name: " + player.Name)
        elif cmd == "reloadkits":
            if Player.Admin:
                KitStore.clear()
                Files = System.IO.Directory.GetFiles(path + "\\Save\\PyPlugins\\Kits\\\LoadOuts\\", "*.ini",
                                                     System.IO.SearchOption.AllDirectories)
                for x in Files:
                    self.GetKitDataWithPath(x)
                Player.MessageFrom("Kits", "Reloaded all kits!")
        elif cmd == "kituses":
            if len(args) == 0 or len(args) > 1:
                Player.MessageFrom("Kits", "Usage: /kituses kitname")
                return
            CurrentUses = DataStore.Get("KitMaxUses" + args[0].lower(), Player.UID)
            if CurrentUses:
                Player.MessageFrom("Kits", "Your current uses: " + str(CurrentUses))
            else:
                Player.MessageFrom("Kits", "You seem to have no uses of the kit, or the kit doesn't have limits.")
