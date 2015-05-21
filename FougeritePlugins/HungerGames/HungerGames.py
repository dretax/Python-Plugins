__author__ = 'DreTaX'
__version__ = '1.2'
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
try:
    import random
except ImportError:
    raise ImportError("Failed to import random! Download the lib!")

"""
    Class
"""

#  Walls
walls = []
#  Chests
loot = []
#  Colors
blue = "[color #0099FF]"
red = "[color #FF0000]"
pink = "[color #CC66FF]"
teal = "[color #00FFFF]"
green = "[color #009900]"
purple = "[color #6600CC]"
white = "[color #FFFFFF]"
sysname = "HungerGames"
#  Minimum players to start the 5 minutes counter.
minp = 7
#  Timer for the force start at minimum players.
#  If we reach 7 players we start the timer. Once It elapsed we start the game.
#  This is in minutes
MinimumTime = 3
#  MaxPlayers! This line is editable
maxp = 14
#  Secs before match start
secs = 30
#  Cleanup loots Stacks after game in close range?
LootStackClean = True
#  Distance for loots if we look from the first spawn point?
CDist = 400

WallsCache = {

}

PlayerSlots = {

}

RestrictedCommands = []
class HungerGames:
    # Values
    IsActive = False
    HasStarted = False
    dp = None
    st = None
    objects = None
    chests = None
    structures = None
    RandomAdmin = None
    count = None
    count2 = None
    count3 = None
    count4 = None
    count5 = None
    times = None
    MTimes = None
    item = None
    sitem = None
    Players = []
    LootableObject = None
    LootableObjects = None
    FirstLocation = None

    def On_PluginInit(self):
        self.dp = Util.TryFindReturnType("DeployableObject")
        if self.dp is None:
            Plugin.Log("Error", "Couldn't find return type2.")
        self.st = Util.TryFindReturnType("StructureComponent")
        if self.st is None:
            Plugin.Log("Error", "Couldn't find return type3.")
        self.LootableObject = Util.TryFindReturnType("LootableObject")
        Util.ConsoleLog("HungerGames by " + __author__ + " Version: " + __version__ + " loaded.", False)
        DataStore.Flush("HDoorMode")
        ini = self.HungerGames()
        ini2 = self.DefaultItems()
        enum = ini.EnumSection("RestrictedCommands")
        for x in enum:
            RestrictedCommands.append(ini.GetSetting("RestrictedCommands", x))
        self.count = int(ini2.GetSetting("Random", "Count"))
        self.count2 = int(ini2.GetSetting("Random", "Count2"))
        self.count3 = int(ini2.GetSetting("Random", "Count3"))
        self.count4 = int(ini2.GetSetting("Random", "Count4"))
        self.count5 = int(ini2.GetSetting("Random", "Count5"))
        self.times = int(ini2.GetSetting("Random", "Times"))
        self.MTimes = int(ini2.GetSetting("Random", "MTimes"))
        self.item = int(ini2.GetSetting("Random", "Items"))
        self.sitem = int(ini2.GetSetting("Random", "SItems"))
        for x in xrange(1, maxp + 1):
            PlayerSlots[x] = None

    """
        Main Methods
    """

    def HungerGames(self):
        if not Plugin.IniExists("HungerGames"):
            ini = Plugin.CreateIni("HungerGames")
            ini.AddSetting("RestrictedCommands", "1", "tpa")
            ini.AddSetting("RestrictedCommands", "2", "home")
            ini.AddSetting("RestrictedCommands", "3", "shop")
            ini.AddSetting("RestrictedCommands", "4", "destroy")
            ini.AddSetting("RestrictedCommands", "5", "starter")
            ini.AddSetting("RestrictedCommands", "6", "buy")
            ini.AddSetting("RestrictedCommands", "7", "sell")
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
            ini.AddSetting("Random", "Items", "3")
            ini.AddSetting("Random", "SItems", "2")
            ini.AddSetting("Random", "Count", "50")
            ini.AddSetting("Random", "Count2", "5")
            ini.AddSetting("Random", "Count3", "5")
            ini.AddSetting("Random", "Count4", "20")
            ini.AddSetting("Random", "Count5", "2")
            ini.AddSetting("Random", "MTimes", "2")
            ini.AddSetting("Random", "Times", "5")
            ini.AddSetting("RandomItems", "1", "Stone Hatchet")
            ini.AddSetting("RandomItems", "2", "Pick Axe")
            ini.AddSetting("RandomItems", "3", "P250")
            ini.AddSetting("SItems", "1", "Silencer")
            ini.AddSetting("SItems", "2", "Holo sight")
            ini.Save()
        return Plugin.GetIni("DefaultItems")

    def Replace(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(',')

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def recordInventory(self, Player):
        Inventory = []
        id = Player.SteamID
        for Item in Player.Inventory.Items:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in Player.Inventory.ArmorItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)
        for Item in Player.Inventory.BarItems:
            if Item and Item.Name:
                myitem = {'name': Item.Name, 'quantity': Item.Quantity, 'slot': Item.Slot}
                Inventory.append(myitem)

        DataStore.Add("HungerGames", id, Inventory)
        DataStore.Save()
        Player.Inventory.ClearAll()

    def returnInventory(self, Player):
        id = Player.SteamID
        if DataStore.ContainsKey("HungerGames", id):
            Inventory = DataStore.Get("HungerGames", id)
            Player.Inventory.ClearAll()
            for dictionary in Inventory:
                if dictionary['name'] is not None:
                    Player.Inventory.AddItemTo(dictionary['name'], dictionary['slot'], dictionary['quantity'])
                else:
                    Player.MessageFrom(sysname, red + "No dictionary found in the for cycle?!")
            Player.MessageFrom(sysname, green + "Your have received your original inventory")
            DataStore.Remove("HungerGames", id)
        else:
            Player.MessageFrom(sysname, red + "No Items of your last inventory found!")

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if self.IsActive or self.HasStarted:
            if Player in self.Players and cmd in RestrictedCommands:
                Server.BroadcastFrom(sysname, red + Player.Name +
                                     " you can't do any other commands, while in the event!")
                Server.BroadcastFrom(sysname, red + "We are now removing you from the event.")
                self.RemovePlayerDirectly(Player)
                return
        if cmd == "hg":
            if len(args) == 0:
                Player.MessageFrom(sysname, green + "Hunger Games By DreTaX! V" + blue + __version__)
                Player.MessageFrom(sysname, "/hg join - Join HG")
                Player.MessageFrom(sysname, "/hg leave - Leave HG")
                Player.MessageFrom(sysname, "/hg info - HG info")
                Player.MessageFrom(sysname, "/hg inventory - Gives your inventory back, if you didn't get it.")
                Player.MessageFrom(sysname, "/hg alive - List the alive players!")
                return
            else:
                arg = args[0]
                if arg == "announce":
                    if Player.Admin or self.isMod(Player.SteamID):
                        if self.IsActive:
                            Player.MessageFrom(sysname, "Hunger Games is already active!")
                        else:
                            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                            Server.BroadcastFrom(sysname, green + "Hunger Games is now active! Type /hg join to enter the battle!")
                            Server.BroadcastFrom(sysname, green + "Type /hg to know more!")
                            Server.BroadcastFrom(sysname, teal + "Pack your items at home just incase!")
                            Server.BroadcastFrom(sysname, teal + "The plugins saves your inventory when you join.")
                            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                            self.RandomAdmin = Player
                            self.IsActive = True
                            del self.Players[:]
                            if Plugin.GetTimer("StartingIn") is not None:
                                Plugin.KillTimer("StartingIn")
                            if Plugin.GetTimer("Force") is not None:
                                Plugin.KillTimer("Force")
                    else:
                        Player.Message("You aren't admin!")
                elif arg == "cleanloot":
                    if LootStackClean:
                        self.LootableObjects = UnityEngine.Object.FindObjectsOfType(self.LootableObject)
                        c = 0
                        for x in self.LootableObjects:
                            if "lootsack" in x.name.lower():
                                dist = Util.GetVectorsDistance(Player.Location, x.transform.position)
                                if dist <= CDist:
                                    x._inventory.Clear()
                                    Util.DestroyObject(x.gameObject)
                                    c += 1
                        Player.MessageFrom(sysname, "Cleaned " + str(c) + " lootsacks!")
                elif arg == "disable":
                    if Player.Admin or self.isMod(Player.SteamID):
                        if self.HasStarted:
                            if len(self.Players) == 1:
                                Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                                Server.BroadcastFrom(sysname, "Hunger Games is now inactive.")
                                Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                                self.EndGame(self.Players[0])
                            else:
                                Player.MessageFrom(sysname, "You can't disable it, there are still more players alive than 1")
                        else:
                            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                            Server.BroadcastFrom(sysname, "Hunger Games is now inactive. (Not Started Yet)")
                            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
                            self.Reset()
                    else:
                        Player.Message("You aren't admin!")
                        return
                elif arg == "info":
                    Player.MessageFrom(sysname, green + "HungerGames By " + __author__ + blue + "V" + __version__)
                    Player.MessageFrom(sysname, "You will start in a house. In the middle of an area")
                    Player.MessageFrom(sysname, "there are Boxes what contains loot, and you may try to take it.")
                    Player.MessageFrom(sysname, "You are against " + str(maxp) + " players. Your aim is to survive.")
                    Player.MessageFrom(sysname, "If you survive you will get rewards!")
                elif arg == "addspawn":
                    if Player.Admin or self.isMod(Player.SteamID):
                        ini = self.HungerGames()
                        count = len(ini.EnumSection("SpawnLocations"))
                        if maxp == count:
                            Player.MessageFrom(sysname, "You reached the max spawnpoints")
                            return
                        ini.AddSetting("SpawnLocations", str(count + 1), str(Player.Location))
                        ini.Save()
                        Player.MessageFrom(sysname, "Added.")
                elif arg == "entity":
                    if Player.Admin or self.isMod(Player.SteamID):
                        if DataStore.ContainsKey("HDoorMode", id):
                            DataStore.Remove("HDoorMode", id)
                            Player.MessageFrom(sysname, "You quit Door Adding mode.")
                        else:
                            DataStore.Add("HDoorMode", id, 1)
                            Player.MessageFrom(sysname, "You are in Entity Adding mode.")
                            Player.MessageFrom(sysname, "Hit the SpawnPoint Shelter's door.")
                            Player.MessageFrom(sysname, "You can't use shotgun.")
                elif arg == "join":
                    if not self.IsActive:
                        Player.MessageFrom(sysname, "HungerGames is not active.")
                        return
                    if self.HasStarted:
                        Player.MessageFrom(sysname, "There is a game in progress.")
                        return
                    ini2 = self.DefaultItems()
                    enum = len(ini2.EnumSection("Rewards"))
                    if Player.Inventory.FreeSlots < enum:
                        Player.MessageFrom(sysname, purple + "You need to have atleast " + str(enum)
                                           + " free slots in your inventory!")
                        return
                    if len(self.Players) == maxp:
                        Player.MessageFrom(sysname, red + "HungerGames is full!")
                        return
                    if Player in self.Players:
                        Player.MessageFrom(sysname, "You are already in the game, nab.")
                    else:
                        self.Players.append(Player)
                        leng = len(self.Players)
                        ini = self.HungerGames()
                        if PlayerSlots.get(leng) is not None:
                            for x in PlayerSlots.keys():
                                if PlayerSlots[x] is None:
                                    leng = x
                                    PlayerSlots[x] = Player
                                    break
                        else:
                            PlayerSlots[leng] = Player
                        DataStore.Add("HLastLoc", Player.SteamID, str(Player.Location))
                        l = self.Replace(ini.GetSetting("SpawnLocations", str(leng)))
                        loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                        Player.TeleportTo(loc)
                        self.recordInventory(Player)
                        enum = ini2.EnumSection("DefaultItems")
                        for item in enum:
                            c = int(ini2.GetSetting("DefaultItems", item))
                            Player.Inventory.AddItem(item, c)
                        Player.MessageFrom(sysname, "You joined the game!")
                        DataStore.Add("HGIG", id, "1")
                        if leng == minp:
                            Server.BroadcastFrom(sysname, purple + "Detected " + str(minp) + " players.")
                            Server.BroadcastFrom(sysname, purple + "Forcing game start in " + str(MinimumTime) +
                                                 " minutes.")
                            Plugin.CreateTimer("Force", MinimumTime * 1000)
                        self.StartGame()
                elif arg == "leave":
                    if not self.IsActive:
                        Player.MessageFrom(sysname, "HungerGames is not active.")
                        return
                    if Player not in self.Players:
                        Player.MessageFrom(sysname, "You are not even in the game, nab.")
                    else:
                        leng = len(self.Players)
                        if leng > 1:
                            self.RemovePlayerDirectly(Player)
                            leng = len(self.Players)
                            if self.HasStarted:
                                Server.BroadcastFrom(sysname, green + Player.Name + red + " has left HungerGames. "
                                                     + green + str(leng) + red + " Players are still alive.")
                            else:
                                Server.BroadcastFrom(sysname, green + Player.Name + red + " has left HungerGames. "
                                                     + green + str(leng) + red + " Players are still in-game.")
                        else:
                            Server.BroadcastFrom(sysname, green + Player.Name + red + " has left HungerGames. ")
                            Player.MessageFrom(sysname, teal + "Use /hg inventory to get your old inventory back.")
                            if self.HasStarted:
                                self.EndGame(self.Players[0])
                        leng = len(self.Players)
                        if leng < minp:
                            Server.BroadcastFrom(sysname, red + "Minimum player count is not enough to force start.")
                            Server.BroadcastFrom(sysname, red + "Stopping timer...")
                            Plugin.KillTimer("Force")
                elif arg == "inventory":
                    self.returnInventory(Player)
                elif arg == "alive":
                    if len(self.Players) == 0:
                        Player.MessageFrom(sysname, "There are 0 players in hungergames")
                        return
                    Player.MessageFrom(sysname, green + "Currently alive: " + str(len(self.Players)))
                    for x in self.Players:
                        Player.MessageFrom(sysname, "- " + x.Name)

    def RemovePlayerDirectly(self, Player, Disconnected=False, Dead=False):
        if Player in self.Players:
            self.Players.remove(Player)
        DataStore.Remove("HGIG", Player.SteamID)
        for x in PlayerSlots.keys():
            if PlayerSlots[x] == Player:
                PlayerSlots[x] = None
        if not Disconnected:
            if DataStore.ContainsKey("HLastLoc", Player.SteamID) and not Dead:
                l = self.Replace(DataStore.Get("HLastLoc", Player.SteamID))
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                Player.TeleportTo(loc)
                DataStore.Remove("HLastLoc", Player.SteamID)

    def FindWalls(self, location):
        for wall in self.structures:
            Distance = Util.GetVectorsDistance(location, wall.transform.position)
            if Distance < 1.5:
                walls.append(Entity(wall))
                return
        Server.BroadcastFrom(sysname, red + " Warning. Failed to find a door at spawnpoint.")

    def FindChest(self, location):
        for chest in self.chests:
            Distance = Util.GetVectorsDistance(location, chest.transform.position)
            if Distance < 1:
                loot.append(Entity(chest))
                return
        Server.BroadcastFrom(sysname, red + " Warning. Failed to find a door at spawnpoint.")

    def StartGame(self, ForceStart=False):
        if self.HasStarted or not self.IsActive:
            return
        if Plugin.GetTimer("StartingIn") is not None:
            Server.BroadcastFrom(sysname, red + "A player has joined while hungergames loaded. (Free Slot)")
            Server.BroadcastFrom(sysname, red + "Current Players: " + str(len(self.Players)))
            return
        if Plugin.GetTimer("Force") is not None:
            Plugin.KillTimer("Force")
        leng = len(self.Players)
        if leng < maxp and not ForceStart:
            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
            Server.BroadcastFrom(sysname, green + "Currently " + str(leng) + " of " + str(maxp) + " players are waiting.")
            Server.BroadcastFrom(sysname, green + "Type /hg for the commands, and join!")
            #  Server.BroadcastFrom(sysname, green + "Pack your items at home just in-case!")
            #  Server.BroadcastFrom(sysname, green + "The plugins saves your inventory when you join.")
        else:
            Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
            if ForceStart:
                Server.BroadcastFrom(sysname, green + "HungerGames force started!")
            Server.BroadcastFrom(sysname, green + "Loading.........")
            ini = self.HungerGames()
            self.FirstLocation = ini.GetSetting("SpawnLocations", "1")
            l = self.Replace(self.FirstLocation)
            self.FirstLocation = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
            enum2 = ini.EnumSection("ChestLocations")
            enum3 = ini.EnumSection("WallLocations")
            self.structures = UnityEngine.Object.FindObjectsOfType(self.st)
            self.chests = UnityEngine.Object.FindObjectsOfType(self.dp)
            for chest in enum2:
                l = ini.GetSetting("ChestLocations", chest).split(',')
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                self.FindChest(loc)
            Server.BroadcastFrom(sysname, green + "Loaded 50%")
            for wall in enum3:
                l = ini.GetSetting("WallLocations", wall).split(',')
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                self.FindWalls(loc)
            Server.BroadcastFrom(sysname, green + "Loaded 75%")
            for chest in loot:
                inv = chest.Inventory
                if inv is None:
                    continue
                inv.ClearAll()
                ini2 = self.DefaultItems()
                times = random.randint(self.MTimes, self.times)
                for i in xrange(0, times):
                    if "large" not in chest.Name.lower():
                        slot = random.randint(1, 11)
                    else:
                        slot = random.randint(1, 35)
                    itemr = random.randint(1, self.item)
                    countr = 1
                    gitem = ini2.GetSetting("RandomItems", str(itemr))
                    if "ammo" in gitem.lower() or "shell" in gitem.lower():
                        countr = random.randint(1, self.count)
                    elif "medkit" in gitem.lower():
                        countr = random.randint(1, self.count2)
                    elif "grenade" in gitem.lower():
                        countr = random.randint(1, self.count3)
                    elif "arrow" in gitem.lower():
                        countr = random.randint(1, self.count4)
                    try:
                        inv.AddItemTo(gitem, slot, countr)
                    except:
                        pass
                if self.sitem > 0:
                    countr = random.randint(1, self.count5)
                    for i in xrange(0, countr):
                        if "large" not in chest.Name.lower():
                            slot = random.randint(1, 11)
                        else:
                            slot = random.randint(1, 35)
                        whichsight = random.randint(1, self.sitem)
                        gitem = ini2.GetSetting("SItems", str(whichsight))
                        try:
                            inv.AddItemTo(gitem, slot, 1)
                        except:
                            pass

            Server.BroadcastFrom(sysname, green + "Loaded 100%!")
            Plugin.CreateTimer("StartingIn", secs * 1000).Start()
            Server.BroadcastFrom(sysname, green + "HungerGames is starting in " + blue + str(secs) + green + " seconds!")

    def ForceCallback(self, timer):
        timer.Kill()
        if Plugin.GetTimer("StartingIn") is not None:
            Plugin.KillTimer("StartingIn")
        self.StartGame(True)

    def StartingInCallback(self, timer):
        timer.Kill()
        Server.BroadcastFrom(sysname, blue + "Shoot to kill! Or swing to kill?")
        self.HasStarted = True
        for wall in walls:
            loc = wall.Location
            spawnRot = wall.Object.transform.rotation
            WallsCache[loc] = spawnRot
            try:
                wall.Destroy()
            except Exception as e:
                Server.BroadcastFrom(sysname, "Failed to destroy a wall!")
                Plugin.Log("Error", str(e))

    def Reset(self):
        self.HasStarted = False
        self.IsActive = False
        for chest in loot:
            inv = chest.Inventory
            if inv is None:
                continue
            inv.ClearAll()
        for pl in self.Players:
            self.RemovePlayerDirectly(pl)
        del self.Players[:]
        del walls[:]
        del loot[:]

    def EndGame(self, Player):
        Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
        Server.BroadcastFrom(sysname, green + Player.Name + " won the match! Congratulations!")
        Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
        self.RemovePlayerDirectly(Player)
        ini = self.DefaultItems()
        enum = ini.EnumSection("Rewards")
        Player.Inventory.ClearAll()
        self.returnInventory(Player)
        for item in enum:
            c = int(ini.GetSetting("Rewards", item))
            Player.Inventory.AddItem(item, c)
        i = 0
        for loc in WallsCache.keys():
            spawnRot = WallsCache.get(loc)
            try:
                sm = World.CreateSM(self.RandomAdmin, loc.x, loc.y, loc.z, spawnRot)
                ent = Entity(World.Spawn(';struct_wood_wall', loc.x, loc.y, loc.z, spawnRot))
                sm.AddStructureComponent(ent.Object.gameObject.GetComponent[self.st]())
                walls[i] = ent
            except Exception as e:
                Server.BroadcastFrom(sysname, "Failed to place walls at the end of the game.")
                Plugin.Log("Error", str(e))
            i += 1
        if LootStackClean:
            self.LootableObjects = UnityEngine.Object.FindObjectsOfType(self.LootableObject)
            for x in self.LootableObjects:
                if "lootsack" in x.name.lower():
                    dist = Util.GetVectorsDistance(self.FirstLocation, x.transform.position)
                    if dist <= CDist:
                        x._inventory.Clear()
                        Util.DestroyObject(x.gameObject)
        self.Reset()
        Player.MessageFrom(sysname, red + "You received your rewards!")

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Victim is not None and HurtEvent.Attacker is not None:
            d = (HurtEvent.Victim not in self.Players and HurtEvent.Attacker in self.Players)
            d2 = HurtEvent.Attacker in self.Players
            if d:
                HurtEvent.DamageAmount = float(0)
            if d2 and HurtEvent.Sleeper:
                HurtEvent.DamageAmount = float(0)

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.Victim is not None:
            if DeathEvent.Victim in self.Players and self.HasStarted:
                self.RemovePlayerDirectly(DeathEvent.Victim, False, True)
                leng = len(self.Players)
                if len(self.Players) > 1:
                    Server.BroadcastFrom(sysname, green + DeathEvent.Victim.Name + red + " has been killed. "
                                         + green + str(leng) + red + " Players are still alive.")
                else:
                    Server.BroadcastFrom(sysname, green + DeathEvent.Victim.Name + red + " has been killed. ")
                    self.EndGame(self.Players[0])
            elif DeathEvent.Victim in self.Players and self.IsActive:
                self.RemovePlayerDirectly(DeathEvent.Victim, False, True)
                Server.BroadcastFrom(sysname, green + DeathEvent.Victim.Name + red + " has been killed. ")
                Server.BroadcastFrom(sysname, red + "The match didn't even start yet!")

    def On_PlayerDisconnected(self, Player):
        if Player in self.Players:
            self.RemovePlayerDirectly(Player, True)
            leng = len(self.Players)
            if leng > 1:
                if self.HasStarted:
                    Server.BroadcastFrom(sysname, green + Player.Name + red + " has disconnected. "
                                         + green + str(leng) + red + " Players are still alive.")
                elif self.IsActive:
                    if leng < minp:
                        Server.BroadcastFrom(sysname, red + "Minimum player count is not enough to force start.")
                        Server.BroadcastFrom(sysname, red + "Stopping timer...")
                        Plugin.KillTimer("Force")
                    Server.BroadcastFrom(sysname, green + Player.Name + red + " has disconnected. "
                                         + green + str(leng) + red + " Players are still in-game.")
            else:
                Server.BroadcastFrom(sysname, green + Player.Name + red + " has disconnected. ")
                if self.HasStarted:
                    self.EndGame(self.Players[0])

    def On_PlayerSpawned(self, Player, SpawnEvent):
        if DataStore.ContainsKey("HLastLoc", Player.SteamID):
            l = self.Replace(DataStore.Get("HLastLoc", Player.SteamID))
            loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
            Player.TeleportTo(loc)
            self.returnInventory(Player)
            DataStore.Remove("HLastLoc", Player.SteamID)

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            gun = HurtEvent.WeaponName
            if gun == "Shotgun":
                return
            if HurtEvent.Attacker in self.Players:
                HurtEvent.DamageAmount = float(0)
                return
            if DataStore.ContainsKey("HDoorMode", id):
                if HurtEvent.Entity.Name == "WoodWall":
                    ini = self.HungerGames()
                    count = len(ini.EnumSection("WallLocations"))
                    enum = ini.EnumSection("WallLocations")
                    for x in enum:
                        if ini.GetSetting("WallLocations", x) == \
                                (str(HurtEvent.Entity.X) + "," + str(HurtEvent.Entity.Y) + "," + str(HurtEvent.Entity.Z)):
                                HurtEvent.Attacker.MessageFrom(sysname, "This wall is already in.")
                                HurtEvent.DamageAmount = float(0)
                                return
                    if maxp == count:
                        HurtEvent.Attacker.MessageFrom(sysname, "You reached the max spawnpoints")
                        return
                    ini.AddSetting("WallLocations", str(count + 1), str(HurtEvent.Entity.X) + "," + str(HurtEvent.Entity.Y) + "," + str(HurtEvent.Entity.Z))
                    ini.Save()
                    HurtEvent.Attacker.MessageFrom(sysname, "Added Wall.")
                elif "box" in HurtEvent.Entity.Name.lower():
                    ini = self.HungerGames()
                    count = len(ini.EnumSection("ChestLocations"))
                    enum = ini.EnumSection("ChestLocations")
                    for x in enum:
                        if ini.GetSetting("ChestLocations", x) == \
                                (str(HurtEvent.Entity.X) + "," + str(HurtEvent.Entity.Y) + "," + str(HurtEvent.Entity.Z)):
                            HurtEvent.Attacker.MessageFrom(sysname, "This chest is already in.")
                            HurtEvent.DamageAmount = float(0)
                            return

                    ini.AddSetting("ChestLocations", str(count + 1), str(HurtEvent.Entity.X) + "," + str(HurtEvent.Entity.Y) + "," + str(HurtEvent.Entity.Z))
                    ini.Save()
                    HurtEvent.Attacker.MessageFrom(sysname, "Added Chest.")
                HurtEvent.DamageAmount = float(0)
