__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import UnityEngine
from UnityEngine import *
import Fougerite
from Fougerite import Entity
import re
import sys
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")
Lib = True
try:
    import random
except ImportError:
    Lib = False

"""
    Class
"""

Players = []
#Doors
doors = []
#Chests
loot = []
#Colors
blue = "[color #0099FF]"
red = "[color #FF0000]"
pink = "[color #CC66FF]"
teal = "[color #00FFFF]"
green = "[color #009900]"
purple = "[color #6600CC]"
white = "[color #FFFFFF]"
sysname = "HungerGames"
maxp = 14
class HungerGames:
    # Values
    IsActive = False
    HasStarted = False
    bd = None
    dp = None
    objects = None
    chests = None

    def On_PluginInit(self):
        self.bd = Util.TryFindReturnType("BasicDoor")
        if self.bd is None:
            Plugin.Log("Error", "Couldn't find return type.")
        self.dp = Util.TryFindReturnType("DeployableObject")
        if self.dp is None:
            Plugin.Log("Error", "Couldn't find return type2.")
        Util.ConsoleLog("HungerGames by " + __author__ + " Version: " + __version__ + " loaded.", False)
        if not Lib:
            Plugin.Log("Error", "Download IronPython Extralibs to run the plugin.")

    """
        Main Methods
    """

    def HungerGames(self):
        if not Plugin.IniExists("HungerGames"):
            ini = Plugin.CreateIni("HungerGames")
            ini.Save()
        return Plugin.GetIni("HungerGames")

    def DefaultItems(self):
        if not Plugin.IniExists("DefaultItems"):
            ini = Plugin.CreateIni("DefaultItems")
            ini.AddSetting("DefaultItems", "P250", "1")
            ini.AddSetting("DefaultItems", "9mm Ammo", "10")
            ini.AddSetting("DefaultItems", "Bandage", "2")
            ini.AddSetting("Rewards", "M4", "4")
            ini.AddSetting("Rewards", "Large Medkit", "20")
            ini.AddSetting("Random", "Items", "4")
            ini.AddSetting("Random", "Count", "20")
            ini.AddSetting("RandomItems", "1", "Stone Hatchet")
            ini.AddSetting("RandomItems", "2", "Pick Axe")
            ini.AddSetting("RandomItems", "3", "")
            ini.Save()
        return Plugin.GetIni("DefaultItems")

    def Replace(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(',')

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def recordInventory(self, Player):
        Inventory = []
        counter = 0
        id = Player.SteamID
        for Item in Player.Inventory.Items:
            if Item and Item.Name:
                myitem = {}
                myitem.name = Item.Name
                myitem.quantity = Item.Quantity
                myitem.slot = Item.Slot
                Inventory[counter + 1] = myitem
        for Item in Player.Inventory.ArmorItems:
            if Item and Item.Name:
                myitem = {}
                myitem.name = Item.Name
                myitem.quantity = Item.Quantity
                myitem.slot = Item.Slot
                Inventory[counter + 1] = myitem
        for Item in Player.Inventory.BarItems:
            if Item and Item.Name:
                myitem = {}
                myitem.name = Item.Name
                myitem.quantity = Item.Quantity
                myitem.slot = Item.Slot
                Inventory[counter + 1] = myitem

        DataStore.Add("HungerGames", id, Inventory)
        Player.Inventory.ClearAll()

    def returnInventory(self, Player):
        id = Player.SteamID
        Player.Inventory.ClearAll()
        if DataStore.ContainsKey("HungerGames", id):
            Inventory = DataStore.Get("HungerGames", id)
            if Inventory:
                Player.Inventory.ClearAll()
                for i in xrange(0, len(Inventory)):
                    Item = Inventory[i]
                    if Item and Item.name:
                        Player.Inventory.AddItemTo(Item.name, Item.slot, Item.quantity)
                Player.MessageFrom(sysname, green + "Your have received your original inventory")
            else:
                Player.MessageFrom(sysname, "Inventory == null")
            DataStore.Remove("HungerGames", id)
        else:
            Player.MessageFrom(sysname, "No Items found!")

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd != "hungergames":
            if self.IsActive:
                if Player in Players:
                    Player.MessageFrom(sysname, "You can't do any other commands, while in the event!")
                    Player.MessageFrom(sysname, "/hungergames leave - To leave the event.")
                    return
        else:
            if len(args) == 0:
                Player.MessageFrom(sysname, green + "Hunger Games By DreTaX! " + blue + __version__)
                Player.MessageFrom(sysname, "/hungergames join - Join HG")
                Player.MessageFrom(sysname, "/hungergames leave - Leave HG")
                Player.MessageFrom(sysname, "/hungergames info - HG info")
                #Player.MessageFrom(sysname, "/hungergames inv - Gives your inventory back, if you didn't get it.")
                return
            else:
                arg = args[0]
                if arg == "announce":
                    if Player.Admin:
                        if self.IsActive:
                            Player.MessageFrom(sysname, "Hunger Games is already active!")
                        else:
                            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                            Server.BroadcastFrom(sysname, "Hunger Games is now active! Type /hungergames join to enter the battle!")
                            Server.BroadcastFrom(sysname, "Type /hungergames info to know more!")
                            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                            self.IsActive = True
                    else:
                        Player.Message("You aren't admin!")
                elif arg == "disable":
                    if Player.Admin:
                        Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                        Server.BroadcastFrom(sysname, "Hunger Games is now inactive.")
                        Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                        if self.HasStarted:
                            if len(Players) == 1:
                                contains = DataStore.ContainsValue("HungerGamesP", 1)
                                if contains:
                                    self.EndGame(Players[0]) #todo: prizez and shets
                                else:
                                    Player.MessageFrom(sysname, "Didn't find any players in the list?!")
                            else:
                                Player.MessageFrom(sysname, "You can't disable it, there are still more players alive than 1")
                                return
                        else:
                            #Reset(); todo:
                    else:
                        Player.Message("You aren't admin!")
                        return
                elif arg == "info":
                    Player.MessageFrom(sysname, green + "HungerGames By DreTaX " + blue + __version__)
                    Player.MessageFrom(sysname, "You will start in a small house. In the middle of the area")
                    Player.MessageFrom(sysname, "there are Boxes on a foundation which contains loot, and you may try to take it.")
                    Player.MessageFrom(sysname, "You can head to the big buildings, which contains loot.")
                    Player.MessageFrom(sysname, "Don't forget to look for hidden stashes, those may contain C4, ")
                    Player.MessageFrom(sysname, "which allows you to blow 1x1 houses, which contain even better loot.")
                elif arg == "addspawn":
                    ini = self.HungerGames()
                    count = len(ini.EnumSection("SpawnLocations"))
                    if maxp == count:
                        Player.MessageFrom(sysname, "You reached the max spawnpoints")
                        return
                    ini.AddSetting("SpawnLocations", str(count + 1), str(Player.Location))
                    ini.Save()
                    Player.MessageFrom(sysname, "Added.")
                elif arg == "entitymode":
                    if DataStore.ContainsKey("HDoorMode", id):
                        DataStore.Remove("HDoorMode", id)
                        Player.MessageFrom(sysname, "You quit Door Adding mode.")
                    else:
                        DataStore.Add("HDoorMode", id, 1)
                        Player.MessageFrom(sysname, "You are in Door Adding mode.")
                        Player.MessageFrom(sysname, "Hit the SpawnPoint Shelter's door.")
                        Player.MessageFrom(sysname, "You can't use shotgun.")
                elif arg == "join":
                    if not self.IsActive:
                        Player.MessageFrom(sysname, "HungerGames is not active.")
                        return
                    if self.HasStarted:
                        Player.MessageFrom(sysname, "There is a game in progress.")
                        return
                    if Player in Players:
                        Player.MessageFrom(sysname, "You are already in the game, nab.")
                    else:
                        Players.append(Player)
                        leng = len(Players)
                        ini = self.HungerGames()
                        ini2 = self.DefaultItems()
                        DataStore.Add("HLastLoc", Player.SteamID, str(Player.Location))
                        l = self.Replace(ini.GetSetting("SpawnLocations", str(leng)))
                        loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                        Player.SafeTeleportTo(loc)
                        self.recordInventory(Player)
                        enum = ini2.EnumSection("DefaultItems")
                        for item in enum:
                            c = int(ini2.GetSetting("DefaultItems", item))
                            Player.Inventory.AddItem(item, c)
                        Player.MessageFrom(sysname, "You joined the game!")
                        self.StartGame()
                elif arg == "leave":
                    if not self.IsActive:
                        Player.MessageFrom(sysname, "HungerGames is not active.")
                        return
                    if Player not in Players:
                        Player.MessageFrom(sysname, "You are not even in the game, nab.")
                    else:
                        self.RemovePlayerDirectly(Player)
                        if self.HasStarted:
                            leng = len(Players)
                            if leng > 1:
                                Server.BroadcastFrom(sysname, green + Player.Name + red + " has left HungerGames. " + green + str(leng) + red + " Players are still alive.")
                            else:
                                Server.BroadcastFrom(sysname, green + Player.Name + red + " has left HungerGames. ")
                                self.EndGame(Players[0])
                        #todo check the prizes later.



    def RemovePlayerDirectly(self, Player):
        Players.remove(Player)
        l = self.Replace(DataStore.Get("HLastLoc", Player.SteamID))
        loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
        Player.SafeTeleportTo(loc)
        DataStore.Remove("HLastLoc", Player.SteamID)

    def FindDoor(self, location):
        for door in self.objects:
            Distance = Util.GetVectorsDistance(location, door.transform.position)
            if Distance < 1.5:
                doors.append(Entity(door))
                return
        Server.BroadcastFrom(sysname, red + " Warning. Failed to find a door at spawnpoint.")

    def FindChest(self, location):
        for chest in self.chests:
            Distance = Util.GetVectorsDistance(location, chest.transform.position)
            if Distance < 1:
                loot.append(Entity(chest))
                return
        Server.BroadcastFrom(sysname, red + " Warning. Failed to find a door at spawnpoint.")

    def StartGame(self):
        if self.HasStarted or not self.IsActive:
            return
        leng = len(Players)
        if leng < maxp:
            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
            Server.BroadcastFrom(sysname, str(leng) + "/" + str(maxp) + " are waiting.")
            Server.BroadcastFrom(sysname, green + "Type /hungergames for the commands, and join!")
        else:
            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
            Server.BroadcastFrom(sysname, green + "Loading.........")
            ini = self.HungerGames()
            enum = ini.EnumSection("DoorLocations")
            enum2 = ini.EnumSection("ChestLocations")
            self.objects = UnityEngine.Object.FindObjectsOfType(self.bd)
            self.chests = UnityEngine.Object.FindObjectsOfType(self.dp)
            for door in enum:
                l = ini.GetSetting("DoorLocations", door).split(',')
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                self.FindDoor(loc)
            Server.BroadcastFrom(sysname, green + "Loaded 50%")
            for chest in enum2:
                l = ini.GetSetting("ChestLocations", chest).split(',')
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                self.FindChest(loc)
            Server.BroadcastFrom(sysname, green + "Loaded 75%")
            for chest in loot:
                inv = chest.Inventory
                if inv is None:
                    continue
                inv.ClearAll()
                if chest.Name == "Wood Box":
                    slot = random.randint(1, 11)
                else:
                    slot = random.randint(1, 35)
                item = int(ini.GetSetting("Random", "Items"))
                count = int(ini.GetSetting("Random", "Count"))
                itemr = random.randint(1, item)
                countr = random.randint(1, count)
                gitem = ini.GetSetting("RandomItems", itemr)
                inv.AddItemTo(gitem, slot, countr)
            Server.BroadcastFrom(sysname, green + "Loaded 100%!")
            Plugin.CreateTimer("StartingIn", 60000)
            Server.BroadcastFrom(sysname, green + "HungerGames is starting in 60 seconds!")


    def StartingInCallback(self):
        Plugin.Killtimer("StartingIn")
        Server.BroadcastFrom(sysname, blue + "Shoot to kill! Or swing to kill?")
        for door in doors:
            ent = Entity(door)
            ent.Destroy()

    def EndGame(self, Player):
        Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
        Server.BroadcastFrom(sysname, green + Player.Name + " won the match! Congratulations!")
        self.RemovePlayerDirectly(Player)
        self.HasStarted = False
        self.IsActive = False
        ini = self.DefaultItems()
        enum = ini.EnumSection("Rewards")
        for item in enum:
            c = int(ini.GetSetting("Rewards", item))
            Player.Inventory.AddItem(item, c)
        Player.MessageFrom(sysname, red + "You received your rewards!")

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Victim is not None and HurtEvent.Attacker is not None:
            if (HurtEvent.Victim in Players and HurtEvent.Attacker not in Players) or (HurtEvent.Victim not in Players and HurtEvent.Attacker in Players):
                HurtEvent.DamageAmount = float(0)

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.DamageType is not None and DeathEvent.Victim is not None and DeathEvent.Attacker is not None:
            if DeathEvent.Victim in Players and self.HasStarted:
                Players.remove(DeathEvent.Victim)
                leng = len(Players)
                if leng > 1:
                    Server.BroadcastFrom(sysname, green + DeathEvent.Victim.Name + red + " has been killed. " + green + str(leng) + red + " Players are still alive.")
                else:
                    Server.BroadcastFrom(sysname, green + DeathEvent.Victim.Name + red + " has been killed. ")
                    self.EndGame(Players[0])

    def On_PlayerDisconnected(self, Player):
        if Player in Players:
            Players.remove(Player)
            leng = len(Players)
            if leng > 1:
                Server.BroadcastFrom(sysname, green + Player.Name + red + " has disconnected. " + green + str(leng) + red + " Players are still alive.")
            else:
                Server.BroadcastFrom(sysname, green + Player.Name + red + " has disconnected. ")
                self.EndGame(Players[0])

    def On_PlayerSpawned(self, Player, SpawnEvent):
        if DataStore.ContainsKey("HLastLoc", Player.SteamID):
            l = self.Replace(DataStore.Get("HLastLoc", Player.SteamID))
            loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
            Player.SafeTeleportTo(loc)
            DataStore.Remove("HLastLoc", Player.SteamID)

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            gun = HurtEvent.WeaponName
            if gun == "Shotgun":
                return
            if HurtEvent.Attacker in Players:
                #Todo: Add config option for this later.
                HurtEvent.DamageAmount = float(0)
                return
            if DataStore.ContainsKey("HDoorMode", id):
                if HurtEvent.Entity.Name == "MetalDoor":
                    ini = self.HungerGames()
                    count = len(ini.EnumSection("DoorLocations"))
                    if maxp == count:
                        HurtEvent.Attacker.MessageFrom(sysname, "You reached the max spawnpoints")
                        return
                    ini.AddSetting("DoorLocations", str(count + 1), str(HurtEvent.Entity.X) + "," + str(HurtEvent.Entity.Y) + "," + str(HurtEvent.Entity.Z))
                    ini.Save()
                    HurtEvent.Attacker.MessageFrom(sysname, "Added door.")
                    return
                if "Wood Box" in HurtEvent.Entity.Name:
                    ini = self.HungerGames()
                    count = len(ini.EnumSection("ChestLocations"))
                    ini.AddSetting("ChestLocations", str(count + 1), str(HurtEvent.Entity.X) + "," + str(HurtEvent.Entity.Y) + "," + str(HurtEvent.Entity.Z))
                    ini.Save()
                    HurtEvent.Attacker.MessageFrom(sysname, "Added Chest.")
                HurtEvent.DamageAmount = float(0)