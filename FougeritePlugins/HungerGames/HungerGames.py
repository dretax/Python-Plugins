__author__ = 'DreTaX'
__version__ = '1.5.0'
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
yellow = "[color #FFFF00]"

sysname = "HungerGames"
#  Minimum players to start the MinimumTime counter.
minp = 15
#  Timer for the force start at minimum players.
#  If we reach 7 players we start the timer. Once It elapsed we start the game.
#  This is in minutes
MinimumTime = 2
#  MaxPlayers!
maxp = 40
#  Secs before match start
secs = 30
#  Cleanup loots Stacks after game in close range?
LootStackClean = True
#  Distance for loots if we look from the first spawn point? (Size of the Arena in meters)
CDist = 310
#  For safety reasons should we freeze the player when he joins for 2 secs?
Freeze = True
# Metal Walls for spawn points = 1 ; Wood Walls = 2 (For destroy/respawning)
WallsSpawn = 2
# Allow building in HG? If this is true, then the deployed entities will be destroyed at the end of the game.
Building = False
# Announce Rewards?
AnnounceRewards = True
# Enable Radiation Damage? Uses CDist and Middle position.
RadDmg = True
# The player count when the radiation damage should activate
CRad = 8
# How many minutes after should the radiation activate?
RadM = 0.1
# How many minutes after should the radius of the radiation "safe-zone" keep decreasing?
RadDC = 0.7
# How many meters should we remove from the radius after every execution?
RadME = 40
# Minimum distance where the radiation can't go further?
RadMDist = 95
# How much radiation should the players receive?
RadR = 65
# Time when we should execute radiation on players after the activation (Seconds)
RadS = 3
# Anti Radiation number if player is not out of the RadRange
RadAnti = 75
# Range where the radiation should Start
RadStart = 310  # Map size is marked at 400, I recommend the half
# TopList Count
TopListC = 5  # Shouldn't be more than 10
# Enable Shop?
EShop = True

PlayerSlots = {

}

Rewards = {

}

EntityList = {
    "WoodBoxLarge": ";deploy_wood_storage_large",
    "WoodBox": ";deploy_wood_box",
    "SmallStash": ";deploy_small_stash",
    "MetalWall": ";struct_metal_wall",
    "WoodWall": ";struct_wood_wall"
}

PlacedEntities = []

PointedPeople = {

}

Awaiting = []

ShopD = {

}


class HungerGames:
    # Values
    IsActive = False
    IsStarting = False
    HasStarted = False
    dp = None
    st = None
    objects = None
    chests = None
    RandomAdmin = None
    count = None
    count2 = None
    count3 = None
    count4 = None
    count5 = None
    count6 = None
    times = None
    MTimes = None
    item = None
    sitem = None
    Players = []
    LootableObject = None
    LootableObjects = None
    ItemRewards = None
    StoreRewards = None
    MinRewards = None
    MaxRewards = None
    Middle = None
    AdminSpot = None
    RestrictedCommands = None
    CurrentRadRange = RadStart
    Metabolism = None
    RadRunning = False
    GotRustPP = False

    def On_PluginInit(self):
        self.dp = Util.TryFindReturnType("DeployableObject")
        self.st = Util.TryFindReturnType("StructureComponent")
        self.Metabolism = Util.TryFindReturnType("Metabolism")
        self.LootableObject = Util.TryFindReturnType("LootableObject")
        DataStore.Flush("HDoorMode")
        ini = self.HungerGames()
        ini2 = self.DefaultItems()
        enum = ini.EnumSection("RestrictedCommands")
        self.RestrictedCommands = Plugin.CreateList()
        for x in enum:
            self.RestrictedCommands.Add(ini.GetSetting("RestrictedCommands", x))
        self.count = int(ini2.GetSetting("Random", "Count"))
        self.count2 = int(ini2.GetSetting("Random", "Count2"))
        self.count3 = int(ini2.GetSetting("Random", "Count3"))
        self.count4 = int(ini2.GetSetting("Random", "Count4"))
        self.count5 = int(ini2.GetSetting("Random", "Count5"))
        self.count6 = int(ini2.GetSetting("Random", "Count6"))
        self.times = int(ini2.GetSetting("Random", "Times"))
        self.MTimes = int(ini2.GetSetting("Random", "MTimes"))
        self.item = int(ini2.GetSetting("Random", "Items"))
        self.sitem = int(ini2.GetSetting("Random", "SItems"))
        self.ItemRewards = self.bool(ini2.GetSetting("Random", "ItemRewards"))
        self.StoreRewards = self.bool(ini2.GetSetting("Random", "StoreRewards"))
        self.MinRewards = int(ini2.GetSetting("Random", "MinRewards"))
        self.MaxRewards = int(ini2.GetSetting("Random", "MaxRewards"))
        self.GotRustPP = Server.HasRustPP
        shop = self.Shop()
        senum = shop.EnumSection("Shop")
        for x in senum:
            ShopD[x] = float(shop.GetSetting("Shop", x))
        if ini.GetSetting("Middle", "1") is not None:
            n = self.Replace(ini.GetSetting("Middle", "1"))
            self.Middle = Util.CreateVector(float(n[0]), float(n[1]), float(n[2]))
            try:
                self.DecayMaxHP()
            except:
                pass
        if ini.GetSetting("AdminSpot", "1") is not None:
            l = self.Replace(ini.GetSetting("AdminSpot", "1"))
            self.AdminSpot = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
        for x in xrange(1, maxp + 1):
            PlayerSlots[x] = None
        enum = ini2.EnumSection("Rewards")
        for item in enum:
            Rewards[item] = int(ini2.GetSetting("Rewards", item))
        Util.ConsoleLog("HungerGames by " + __author__ + " Version: " + __version__ + " loaded.", False)

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
            ini.AddSetting("Random", "Count6", "5")
            ini.AddSetting("Random", "MTimes", "2")
            ini.AddSetting("Random", "Times", "5")
            ini.AddSetting("Random", "ItemRewards", "True")
            ini.AddSetting("Random", "StoreRewards", "False")
            ini.AddSetting("Random", "MinRewards", "3")
            ini.AddSetting("Random", "MaxRewards", "6")
            ini.AddSetting("RandomItems", "1", "Stone Hatchet")
            ini.AddSetting("RandomItems", "2", "Pick Axe")
            ini.AddSetting("RandomItems", "3", "P250")
            ini.AddSetting("SItems", "1", "Silencer")
            ini.AddSetting("SItems", "2", "Holo sight")
            ini.Save()
        return Plugin.GetIni("DefaultItems")

    def Shop(self):
        if not Plugin.IniExists("Shop"):
            ini = Plugin.CreateIni("Shop")
            ini.AddSetting("Shop", "P250", "10")
            ini.AddSetting("Shop", "M4", "30")
            ini.AddSetting("Shop", "Explosive Charge", "50")
            ini.Save()
        return Plugin.GetIni("Shop")

    def Store(self):
        if not Plugin.IniExists("Store"):
            ini = Plugin.CreateIni("Store")
            ini.Save()
        return Plugin.GetIni("Store")

    def Wins(self):
        if not Plugin.IniExists("Wins"):
            ini = Plugin.CreateIni("Wins")
            ini.Save()
        return Plugin.GetIni("Wins")

    def Kills(self):
        if not Plugin.IniExists("Kills"):
            ini = Plugin.CreateIni("Kills")
            ini.Save()
        return Plugin.GetIni("Kills")

    def DecayMaxHP(self):
        c = 0
        for entity in World.Entities:
            if "spike" in entity.Name.lower() or "box" in entity.Name.lower() \
                    or "stash" in entity.Name.lower():
                if Util.GetVectorsDistance(self.Middle, entity.Location) <= CDist:
                    entity.SetDecayEnabled(False)
                    try:
                        entity.Health = entity.MaxHealth
                    except:
                        pass
                    c += 1
        return c

    def Freezer(self, Player, num, msg=True):
        if not Freeze:
            return
        if num == 1:
            Player.SendCommand("input.bind Up 7 None")
            Player.SendCommand("input.bind Down 7 None")
            Player.SendCommand("input.bind Left 7 None")
            Player.SendCommand("input.bind Right 7 None")
            Player.SendCommand("input.bind Sprint 7 None")
            Player.SendCommand("input.bind Duck 7 None")
            Player.SendCommand("input.bind Jump 7 None")
            Player.SendCommand("input.bind Fire 7 None")
            if msg:
                Player.MessageFrom(sysname, red + "You froze!")
            List = Plugin.CreateDict()
            List["Player"] = Player
            Plugin.CreateParallelTimer("Freezer", 2000, List).Start()
        else:
            Player.SendCommand("input.bind Up W UpArrow")
            Player.SendCommand("input.bind Down S DownArrow")
            Player.SendCommand("input.bind Left A LeftArrow")
            Player.SendCommand("input.bind Right D RightArrow")
            Player.SendCommand("input.bind Sprint LeftShift RightShift")
            Player.SendCommand("input.bind Duck LeftControl RightControl")
            Player.SendCommand("input.bind Jump Space None")
            Player.SendCommand("input.bind Fire Mouse0 None")
            if msg:
                Player.MessageFrom(sysname, red + "You are now free!")

    def bool(self, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            raise ValueError('Failed to convert ' + s + ' to boolean! Config error!')

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
        if cmd == "hg":
            if len(args) == 0:
                Player.MessageFrom(sysname, teal + "HungerGames By " + __author__ + " " + blue + "V" + __version__)
                Player.MessageFrom(sysname, green + "/hg join - Join HG")
                Player.MessageFrom(sysname, green + "/hg leave - Leave HG")
                Player.MessageFrom(sysname, green + "/hg info - HG info")
                Player.MessageFrom(sysname, green + "/hg inventory - Gives your inventory back, if you didn't get it.")
                Player.MessageFrom(sysname, green + "/hg alive - List the alive players!")
                Player.MessageFrom(sysname, green + "/hg toplist - List the top5 players!")
                Player.MessageFrom(sysname, green + "/hg stats - View your stats!")
                Player.MessageFrom(sysname, green + "/hg buy - Buy items for points!")
                Player.MessageFrom(sysname, green + "/hg slist - List Shop Items!")
                return
            else:
                arg = args[0]
                if arg == "announce":
                    if Player.Admin or Player.Moderator:
                        if self.IsActive:
                            Player.MessageFrom(sysname, "Hunger Games is already active!")
                        else:
                            Server.BroadcastFrom(sysname, red + "----------------------------"
                                                                "HUNGERGAMES--------------------------------")
                            Server.BroadcastFrom(sysname, green +
                                                 "Hunger Games is now active! Type /hg join to enter the battle!")
                            Server.BroadcastFrom(sysname, green + "Type /hg to know more!")
                            Server.BroadcastFrom(sysname, teal + "Pack your items at home just incase!")
                            Server.BroadcastFrom(sysname, teal + "The plugins saves your inventory when you join.")
                            Server.BroadcastFrom(sysname, red + "----------------------------"
                                                                "HUNGERGAMES--------------------------------")
                            self.RandomAdmin = Player
                            self.IsActive = True
                            self.ResetWalls()
                            del self.Players[:]
                            if Plugin.GetTimer("StartingIn") is not None:
                                Plugin.KillTimer("StartingIn")
                            if Plugin.GetTimer("Force") is not None:
                                Plugin.KillTimer("Force")
                    else:
                        Player.Message("You aren't admin!")
                elif arg == "cleanloot":
                    if Player.Admin or Player.Moderator:
                        if self.Middle is None:
                            Player.MessageFrom(sysname, "Middle of HungerGames is not set!")
                            return
                        if LootStackClean:
                            self.LootableObjects = UnityEngine.Object.FindObjectsOfType(self.LootableObject)
                            c = 0
                            for x in self.LootableObjects:
                                if "lootsack" in x.name.lower():
                                    dist = Util.GetVectorsDistance(self.Middle, x.transform.position)
                                    if dist <= CDist:
                                        x._inventory.Clear()
                                        Util.DestroyObject(x.gameObject)
                                        c += 1
                            Player.MessageFrom(sysname, "Cleaned " + str(c) + " lootsacks!")
                elif arg == "forcestart":
                    if Player.Admin or Player.Moderator:
                        if Plugin.GetTimer("StartingIn") is not None or self.HasStarted:
                            Player.MessageFrom(sysname, red + "Game is already running!")
                            return
                        self.StartGame(True)
                elif arg == "disable":
                    if Player.Admin or Player.Moderator:
                        if self.HasStarted:
                            if len(self.Players) == 1:
                                Server.BroadcastFrom\
                                    (sysname, red + "----------------------------HUNGERGAMES"
                                                    "--------------------------------")
                                Server.BroadcastFrom(sysname, "Hunger Games is now inactive.")
                                Server.BroadcastFrom(sysname,
                                                     red + "----------------------------"
                                                     "HUNGERGAMES--------------------------------")
                                self.EndGame(self.Players[0])
                                self.ResetWalls()
                            else:
                                Server.BroadcastFrom\
                                    (sysname, red + "----------------------------HUNGERGAMES"
                                                    "--------------------------------")
                                Server.BroadcastFrom(sysname, "Hunger Games is now inactive.")
                                Server.BroadcastFrom(sysname,
                                                     red + "----------------------------"
                                                     "HUNGERGAMES--------------------------------")
                                self.Reset()
                                self.ResetWalls()
                        else:
                            if not self.IsActive:
                                Player.MessageFrom(sysname, "Hunger Games is already in-active!")
                                return
                            Server.BroadcastFrom(sysname, red +
                                                 "----------------------------"
                                                 "HUNGERGAMES--------------------------------")
                            Server.BroadcastFrom(sysname, "Hunger Games is now inactive. (Not Started Yet)")
                            Server.BroadcastFrom(sysname, red +
                                                 "----------------------------"
                                                 "HUNGERGAMES--------------------------------")
                            self.Reset()
                            self.ResetWalls()
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
                    if Player.Admin or Player.Moderator:
                        ini = self.HungerGames()
                        count = len(ini.EnumSection("SpawnLocations"))
                        if maxp == count:
                            Player.MessageFrom(sysname, "You reached the max spawnpoints")
                            return
                        ini.AddSetting("SpawnLocations", str(count + 1), str(Player.Location))
                        ini.Save()
                        Player.MessageFrom(sysname, "Added.")
                elif arg == "cleanchests":
                    if not self.HasStarted and Plugin.GetTimer("StartingIn") is None and \
                                    Plugin.GetTimer("Force") is None:
                        ini = self.HungerGames()
                        enum2 = ini.EnumSection("ChestLocations")
                        for chest in enum2:
                            l = ini.GetSetting("ChestLocations", chest).split(',')
                            name = chest.split('-')
                            loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                            self.FindChest(loc, name, l[3])
                        for x in loot:
                            x.Inventory.ClearAll()
                        del loot[:]
                        Player.MessageFrom(sysname, "All chests cleaned!")
                    else:
                        Player.MessageFrom(sysname, "Can't clean right now.")
                elif arg == "addchests":
                    if self.Middle is not None:
                        chests = Util.FindDeployablesAround(self.Middle, CDist, True)
                        c = 0
                        ini = self.HungerGames()
                        enum = ini.EnumSection("ChestLocations")
                        for x in enum:
                            ini.DeleteSetting("ChestLocations", x)
                        ini.Save()
                        for x in chests:
                            if "stash" in x.Name.lower() or "box" in x.Name.lower():
                                if Util.GetVectorsDistance(self.Middle, x.Location) <= CDist:
                                    name = x.Name
                                    c += 1
                                    ini.AddSetting("ChestLocations", name + "-" + str(c),
                                                   str(x.X) + "," +
                                                   str(x.Y) + "," +
                                                   str(x.Z) + "," +
                                                   str(x.Rotation.x) + "," +
                                                   str(x.Rotation.y) + "," +
                                                   str(x.Rotation.z) + "," +
                                                   str(x.Rotation.w))
                        ini.Save()
                        Player.MessageFrom(sysname, "Added " + str(c) + " entities.")
                elif arg == "middle":
                    if Player.Admin or Player.Moderator:
                        ini = self.HungerGames()
                        if ini.GetSetting("Middle", "1") is not None:
                            Player.MessageFrom(sysname, "Middle Re-Set!")
                            ini.SetSetting("Middle", "1", str(Player.Location))
                            ini.Save()
                            self.Middle = Player.Location
                            return
                        ini.AddSetting("Middle", "1", str(Player.Location))
                        ini.Save()
                        self.Middle = Player.Location
                        Player.MessageFrom(sysname, "Set!")
                elif arg == "entity":
                    if Player.Admin or Player.Moderator:
                        if DataStore.ContainsKey("HDoorMode", id):
                            DataStore.Remove("HDoorMode", id)
                            Player.MessageFrom(sysname, "You quit Entity Adding mode.")
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
                        if DataStore.ContainsKey("HungerGames", id):
                            Player.MessageFrom(sysname, green + "First you have to do /hg inventory !")
                            return
                        self.Players.append(Player)
                        for cmd in self.RestrictedCommands:
                            Player.RestrictCommand(cmd)
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
                        self.Freezer(Player, 1)
                        DataStore.Add("HLastLoc", Player.SteamID, str(Player.Location))
                        l = self.Replace(ini.GetSetting("SpawnLocations", str(leng)))
                        loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                        Player.TeleportTo(loc, False)
                        self.recordInventory(Player)
                        enum = ini2.EnumSection("DefaultItems")
                        for item in enum:
                            c = int(ini2.GetSetting("DefaultItems", item))
                            Player.Inventory.AddItem(item, c)
                        Player.MessageFrom(sysname, "You joined the game!")
                        DataStore.Add("HGIG", id, "1")
                        if self.GotRustPP:
                            Server.GetRustPPAPI().RemoveGod(Player.UID)
                            Server.GetRustPPAPI().RemoveInstaKO(Player.UID)
                            Server.GetRustPPAPI().GetFriendsCommand.AddTempException(Player.UID)
                        if leng == minp and Plugin.GetTimer("Force") is None:
                            if self.IsStarting or self.HasStarted:
                                return
                            Server.BroadcastFrom(sysname, pink + "Detected " + str(minp) + " players.")
                            Server.BroadcastFrom(sysname, pink + "Forcing game start in " + str(MinimumTime) +
                                                 " minutes.")
                            Plugin.CreateTimer("Force", MinimumTime * 60000).Start()
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
                            for cmd in self.RestrictedCommands:
                                Player.UnRestrictCommand(cmd)
                            leng = len(self.Players)
                            if self.HasStarted:
                                Server.BroadcastFrom(sysname, green + Player.Name + red + " has left HungerGames. "
                                                     + green + str(leng) + red + " Players are still alive.")
                            else:
                                Server.BroadcastFrom(sysname, green + Player.Name + red + " has left HungerGames. "
                                                     + green + str(leng) + red + " Players are still in-game.")
                            self.returnInventory(Player)
                        else:
                            Server.BroadcastFrom(sysname, green + Player.Name + red + " has left HungerGames. ")
                            Player.MessageFrom(sysname, teal + "Use /hg inventory to get your old inventory back.")
                            if self.HasStarted:
                                self.EndGame(self.Players[0])
                        leng = len(self.Players)
                        if leng < minp and Plugin.GetTimer("Force") is not None:
                            Server.BroadcastFrom(sysname, red + "Minimum player count is not enough to force start.")
                            Server.BroadcastFrom(sysname, red + "Stopping timer...")
                            Plugin.KillTimer("Force")
                elif arg == "inventory":
                    if Player in self.Players:
                        Player.MessageFrom(sysname, red + "You are in HungerGames, you can't use this!")
                        return
                    self.returnInventory(Player)
                elif arg == "adminspot":
                    if Player.Admin or Player.Moderator:
                        ini = self.HungerGames()
                        if ini.GetSetting("AdminSpot", "1") is not None:
                            ini.SetSetting("AdminSpot", "1", str(Player.Location))
                            ini.Save()
                            self.AdminSpot = Player.Location
                            Player.MessageFrom(sysname, "AdminSpot Re-Set!")
                            return
                        ini.AddSetting("AdminSpot", "1", str(Player.Location))
                        ini.Save()
                        self.AdminSpot = Player.Location
                        Player.MessageFrom(sysname, "Set!")
                elif arg == "spot":
                    if Player.Admin or Player.Moderator:
                        if self.AdminSpot is not None:
                            Player.TeleportTo(self.AdminSpot, False)
                            Player.MessageFrom(sysname, "Teleported!")
                        else:
                            Player.MessageFrom(sysname, "Admin spot is not set!")
                elif arg == "alive":
                    if len(self.Players) == 0:
                        Player.MessageFrom(sysname, "There are 0 players in hungergames")
                        return
                    Player.MessageFrom(sysname, green + "Currently alive: " + str(len(self.Players)))
                    for x in self.Players:
                        Player.MessageFrom(sysname, "- " + x.Name + " Rad: " + str(x.RadLevel))
                elif arg == "decay":
                    if Player.Admin or Player.Moderator:
                        if self.Middle is None:
                            Player.MessageFrom(sysname, "Middle of HungerGames is not set!")
                            return
                        try:
                            c = self.DecayMaxHP()
                        except:
                            return
                        Player.MessageFrom(sysname, "Decay is disabled on " + str(c) + " objects.")
                elif arg == "toplist":
                    wini = self.Wins()
                    enum = wini.EnumSection("Wins")
                    if len(enum) < 5:
                        Player.MessageFrom(sysname, red + "5 Winners are required for this atleast")
                        return
                    d = {}
                    for x in enum:
                        d[x] = float(wini.GetSetting("Wins", x))
                    top = sorted(d, key=d.get, reverse=True)[:TopListC]
                    dic = Server.GetRustPPAPI().Cache
                    Player.MessageFrom(sysname, pink + "===Top" + str(TopListC) + "===")
                    for nid in top:
                        try:
                            name = str(dic[long(nid)])
                        except:
                            name = "Unknown"
                        kills = self.Kills()
                        count = kills.GetSetting("Kills", nid)
                        if count is None:
                            count = "0"
                        Player.MessageFrom(sysname, pink + " - " + name + " Points: "
                                           + wini.GetSetting("Wins", nid)
                                           + " Kills: " + count)
                elif arg == "stats":
                    wini = self.Wins()
                    data = wini.GetSetting("Wins", id)
                    if data is None:
                        Player.MessageFrom(sysname, red + "No stats found")
                        return
                    enum = wini.EnumSection("Wins")
                    Player.MessageFrom(sysname, green + "==Stats==")
                    Player.MessageFrom(sysname, pink + "Name: " + Player.Name)
                    Player.MessageFrom(sysname, pink + "Points: " + data)
                    d = {}
                    for x in enum:
                        d[x] = float(wini.GetSetting("Wins", x))
                    count = len(enum)
                    top = sorted(d, key=d.get, reverse=True)[:count]
                    lid = long(id)
                    for i, fid in enumerate(top):
                        if lid == long(fid):
                            Player.MessageFrom(sysname, pink + "Ranked: " + str(i + 1) + "/" + str(count))
                            break
                    kills = self.Kills()
                    count = kills.GetSetting("Kills", id)
                    if count is None:
                        count = "0"
                    Player.MessageFrom(sysname, pink + "Kills: " + count)
                elif arg == "forcejoin":
                    if not Player.Admin:
                        return
                    if not self.IsActive:
                        Player.MessageFrom(sysname, "HungerGames is not active.")
                        return
                    if not self.HasStarted:
                        Player.MessageFrom(sysname, "Only use this if HungerGames has started.")
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
                        if DataStore.ContainsKey("HungerGames", id):
                            Player.MessageFrom(sysname, green + "First you have to do /hg inventory !")
                            return
                        self.Players.append(Player)
                        for cmd in self.RestrictedCommands:
                            Player.RestrictCommand(cmd)
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
                        self.Freezer(Player, 1)
                        DataStore.Add("HLastLoc", Player.SteamID, str(Player.Location))
                        l = self.Replace(ini.GetSetting("SpawnLocations", str(leng)))
                        loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                        Player.TeleportTo(loc, False)
                        self.recordInventory(Player)
                        enum = ini2.EnumSection("DefaultItems")
                        for item in enum:
                            c = int(ini2.GetSetting("DefaultItems", item))
                            Player.Inventory.AddItem(item, c)
                        if self.GotRustPP:
                            Server.GetRustPPAPI().RemoveGod(Player.UID)
                            Server.GetRustPPAPI().RemoveInstaKO(Player.UID)
                            Server.GetRustPPAPI().GetFriendsCommand.AddTempException(Player.UID)
                        Player.MessageFrom(sysname, "You joined the game!")
                        DataStore.Add("HGIG", id, "1")
                elif arg == "checkwalls":
                    if Player.Admin or Player.Moderator:
                        if self.HasStarted or self.IsStarting:
                            Player.MessageFrom(sysname, "You can't do this now.")
                            return
                        self.RandomAdmin = Player
                        self.ResetWalls()
                        Player.MessageFrom(sysname, "Walls replaced.")
                elif arg == "buy":
                    if not EShop:
                        Player.MessageFrom(sysname, red + "Feature is disabled on this server")
                        return
                    if Player in self.Players:
                        Player.MessageFrom(sysname, "You can't do this now.")
                        return
                    if len(args) <= 2:
                        Player.MessageFrom(sysname, 'Usage: /hg buy "item" "amount"')
                        Player.MessageFrom(sysname, '(Buying Items will reduce you rank)')
                        return
                    s = str.join(' ', args)
                    if '"' not in s:
                        Player.MessageFrom(sysname, 'Usage: /hg buy "item" "amount"')
                        Player.MessageFrom(sysname, '(Buying Items will reduce you rank)')
                        return
                    msg = re.sub('buy[\s]', '', s)
                    quote = Util.GetQuotedArgs(msg)
                    if len(quote) <= 1:
                        Player.MessageFrom(sysname, 'Usage: /hg buy "item" "amount"')
                        Player.MessageFrom(sysname, '(Buying Items will reduce you rank)')
                        return
                    if quote[0] not in ShopD.keys():
                        Player.MessageFrom(sysname, red + 'Item not found! Use /slist to list the items.')
                        return
                    if not quote[1].isnumeric():
                        Player.MessageFrom(sysname, 'Usage: /hg buy "item" "amount"')
                        Player.MessageFrom(sysname, '(Buying Items will reduce you rank)')
                        return
                    winsini = self.Wins()
                    item = quote[0]
                    amount = int(quote[1])
                    price = ShopD[item]
                    if winsini.GetSetting("Wins", id) is None:
                        Player.MessageFrom(sysname, red + 'GET POINTS FIRST YOU N00B')
                        return
                    points = float(winsini.GetSetting("Wins", id))
                    finalp = price * amount
                    if finalp > points:
                        Player.MessageFrom(sysname, red + "You can't afford buying " + str(amount) + " " + item
                                           + "(s) for " + str(finalp) + " points!")
                        return
                    if Player.Inventory.FreeSlots <= 6:
                        Player.MessageFrom(sysname, red + "Have atleast 6 free slots in your inventory")
                        return
                    winsini.SetSetting("Wins", id, str(points - finalp))
                    winsini.Save()
                    Player.MessageFrom(sysname, green + "You bought " + str(amount) + " " + item + "(s) for "
                                       + str(finalp) + " points!")
                    Plugin.Log("Purchases", Player.Name + "-" + id + " bought " + str(amount) + " amount of " + item
                               + "(s) for " + str(finalp) + " points!")
                    Player.Inventory.AddItem(item, amount)
                elif arg == "slist":
                    if not EShop:
                        Player.MessageFrom(sysname, red + "Feature is disabled on this server")
                        return
                    Player.MessageFrom(sysname, purple + "===Shop===")
                    for x in ShopD.keys():
                        Player.MessageFrom(sysname, green + "Item: " + yellow + x + teal + " Price: " + str(ShopD[x]))

    def RemovePlayerDirectly(self, Player, Disconnected=False, Dead=False, Remove=True):
        id = Player.SteamID
        if Player in self.Players and Remove:
            self.Players.remove(Player)
        if Player.UID in Awaiting:
            Awaiting.remove(Player.UID)
        if self.GotRustPP:
            Server.GetRustPPAPI().GetFriendsCommand.RemoveTempException(Player.UID)
        DataStore.Remove("HGIG", id)
        for cmd in self.RestrictedCommands:
            Player.UnRestrictCommand(cmd)
        for x in PlayerSlots.keys():
            if PlayerSlots[x] == Player:
                PlayerSlots[x] = None
        if not Disconnected:
            if DataStore.ContainsKey("HLastLoc", id) and not Dead:
                Player.AddAntiRad(Player.RadLevel)
                l = self.Replace(DataStore.Get("HLastLoc", id))
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                Player.TeleportTo(loc)
                DataStore.Remove("HLastLoc", id)

    def FindWalls(self, location, name, spawnRot):
        wall = Util.FindStructuresAround(location, float(1.5))
        if len(wall) >= 1:
            for x in wall:
                walls.append(x)
            return
        try:
            sm = World.CreateSM(self.RandomAdmin, location.x, location.y, location.z, spawnRot)
            if WallsSpawn == 2:
                ent = Entity(World.Spawn(';struct_wood_wall', location.x, location.y, location.z, spawnRot))
            else:
                ent = Entity(World.Spawn(';struct_metal_wall', location.x, location.y, location.z, spawnRot))
            sm.AddStructureComponent(ent.Object.gameObject.GetComponent[self.st]())
            walls.append(ent)
        except:
            pass

    def FindChest(self, location, name, spawnRot):
        chest = Util.FindChestAt(location)
        if chest is not None:
            loot.append(chest)
            return
        n = EntityList[name]
        try:
            ent = Entity(World.Spawn(n, location.x, location.y, location.z, spawnRot))
            ent.ChangeOwner(self.RandomAdmin)
            loot.append(ent)
        except:
            pass

    def StartGame(self, ForceStart=False):
        if self.HasStarted or not self.IsActive:
            return
        if Plugin.GetTimer("StartingIn") is not None:
            Server.BroadcastFrom(sysname, red + "A player has joined while hungergames loaded. (Free Slot)")
            Server.BroadcastFrom(sysname, red + "Current Players: " + str(len(self.Players)))
            return
        leng = len(self.Players)
        if leng < maxp and not ForceStart:
            Server.BroadcastFrom(sysname, red + "----------------------------"
                                                "HUNGERGAMES--------------------------------")
            Server.BroadcastFrom(sysname, green + "Currently " + str(leng) +
                                 " of " + str(maxp) + " players are waiting.")
            Server.BroadcastFrom(sysname, green + "Type /hg for the commands, and join!")
        else:
            if Plugin.GetTimer("Force") is not None:
                Plugin.KillTimer("Force")
            if self.IsStarting:
                return
            Server.BroadcastFrom(sysname, red + "----------------------------"
                                                "HUNGERGAMES--------------------------------")
            if ForceStart:
                Server.BroadcastFrom(sysname, green + "HungerGames force started!")
            Server.BroadcastFrom(sysname, green + "Loading.........")
            try:
                self.DecayMaxHP()
            except:
                pass
            ini = self.HungerGames()
            enum2 = ini.EnumSection("ChestLocations")
            enum3 = ini.EnumSection("WallLocations")
            for chest in enum2:
                l = ini.GetSetting("ChestLocations", chest).split(',')
                name = chest.split('-')
                quat = Util.CreateQuat(float(l[3]), float(l[4]), float(l[5]), float(l[6]))
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                self.FindChest(loc, name[0], quat)
            Server.BroadcastFrom(sysname, green + "Loaded 50%")
            for wall in enum3:
                l = ini.GetSetting("WallLocations", wall).split(',')
                name = wall.split('-')
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                quat = Util.CreateQuat(float(l[3]), float(l[4]), float(l[5]), float(l[6]))
                self.FindWalls(loc, name[0], quat)
            Server.BroadcastFrom(sysname, green + "Loaded 75%")
            for chest in loot:
                inv = chest.Inventory
                if inv is None:
                    continue
                inv.ClearAll()
                ini2 = self.DefaultItems()
                times = random.randint(self.MTimes, self.times)
                if "stash" in chest.Name.lower():
                    times = random.randint(1, 3)
                for i in xrange(0, times):
                    if "large" in chest.Name.lower():
                        slot = random.randint(1, 35)
                    elif "stash" in chest.Name.lower():
                        slot = random.randint(1, 3)
                    else:
                        slot = random.randint(1, 11)
                    itemr = 1
                    if self.item > 1:
                        itemr = random.randint(1, self.item)
                    countr = 1
                    gitem = ini2.GetSetting("RandomItems", str(itemr))
                    if "ammo" in gitem.lower() or "shell" in gitem.lower():
                        countr = random.randint(1, self.count)
                    elif "medkit" in gitem.lower():
                        countr = random.randint(1, self.count2)
                    elif "bandage" in gitem.lower():
                        countr = random.randint(1, self.count2)
                    elif "grenade" in gitem.lower():
                        countr = random.randint(1, self.count3)
                    elif "arrow" in gitem.lower():
                        countr = random.randint(1, self.count4)
                    elif "flare" in gitem.lower():
                        countr = random.randint(1, self.count6)
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
            Server.BroadcastFrom(sysname, green + "HungerGames is starting in " + blue + str(secs) +
                                 green + " seconds!")
            Server.BroadcastFrom(sysname, red + "TEAMWORK IS NOT ALLOWED.")
            self.IsStarting = True

    def ForceCallback(self, timer):
        timer.Kill()
        if Plugin.GetTimer("StartingIn") is not None:
            Plugin.KillTimer("StartingIn")
        self.StartGame(True)

    def StartingInCallback(self, timer):
        timer.Kill()
        Server.BroadcastFrom(sysname, blue + "----------------------------HUNGERGAMES--------------------------------")
        Server.BroadcastFrom(sysname, blue + "Shoot to kill! Or swing to kill?")
        self.HasStarted = True
        for wall in walls:
            wall.Destroy()
        del walls[:]

    def FreezerCallback(self, timer):
        timer.Kill()
        List = timer.Args
        Player = List["Player"]
        self.Freezer(Player, 2)

    def RadiationActivateCallback(self, timer):
        timer.Kill()
        Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
        Server.BroadcastFrom(sysname, red + "Radiation activated!")
        Server.BroadcastFrom(sysname, red + "You will receive " + str(RadR) + " rad every " + str(RadS) + " secs")
        Server.BroadcastFrom(sysname, red + "if you are out of range! Current range: "
                             + str(self.CurrentRadRange) + "m!")
        Plugin.CreateTimer("Radiation", RadS * 1000).Start()
        Plugin.CreateTimer("RadiationRange", RadDC * 60000).Start()

    def RadiationRangeCallback(self, timer):
        timer.Kill()
        if self.CurrentRadRange - RadME <= RadMDist:
            self.CurrentRadRange = RadMDist
            Server.BroadcastFrom(sysname, green + "Radiation range stopped at: " + str(RadMDist) + "m!")
            return
        self.CurrentRadRange -= RadME
        Server.BroadcastFrom(sysname, red + "Radiation range decreased to: " + str(self.CurrentRadRange) + "m!")
        Plugin.CreateTimer("RadiationRange", RadDC * 60000).Start()

    def RadiationCallback(self, timer):
        timer.Kill()
        if not self.HasStarted:
            return
        for x in self.Players:
            if Util.GetVectorsDistance(x.Location, self.Middle) >= self.CurrentRadRange:
                x.AddRads(RadR)
                try:
                    m = x.PlayerClient.controllable.GetComponent(self.Metabolism)
                    m.Vomit()
                except:
                    pass
            else:
                x.AddAntiRad(RadAnti)
        Plugin.CreateTimer("Radiation", RadS * 1000).Start()

    def CleanMess(self):
        for x in PlacedEntities:
            if x.Health > 0:
                x.Destroy()

    def Reset(self):
        self.HasStarted = False
        self.IsActive = False
        self.IsStarting = False
        self.CurrentRadRange = RadStart
        self.RadRunning = False
        if Plugin.GetTimer("Force") is not None:
            Plugin.KillTimer("Force")
        if Plugin.GetTimer("StartingIn") is not None:
            Plugin.KillTimer("StartingIn")
        if Plugin.GetTimer("Radiation") is not None:
            Plugin.KillTimer("Radiation")
        if Plugin.GetTimer("RadiationRange") is not None:
            Plugin.KillTimer("RadiationRange")
        if Plugin.GetTimer("RadiationActivate") is not None:
            Plugin.KillTimer("RadiationActivate")
        for chest in loot:
            inv = chest.Inventory
            if inv is None:
                continue
            inv.ClearAll()
        tplayers = []
        for pl in self.Players:
            tplayers.append(pl)
        for pl in tplayers:
            self.RemovePlayerDirectly(pl, False)
        #  Just in-case
        for x in PlayerSlots.keys():
            PlayerSlots[x] = None
        del self.Players[:]
        del walls[:]
        del loot[:]
        del Awaiting[:]
        PointedPeople.clear()
        self.CleanMess()
        del PlacedEntities[:]

    def ResetWalls(self):
        ini = self.HungerGames()
        enum3 = ini.EnumSection("WallLocations")
        for wall in enum3:
            l = ini.GetSetting("WallLocations", wall).split(',')
            name = wall.split('-')
            loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
            quat = Util.CreateQuat(float(l[3]), float(l[4]), float(l[5]), float(l[6]))
            self.FindWalls(loc, name[0], quat)

    def EndGame(self, Player):
        Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")
        Server.BroadcastFrom(sysname, green + Player.Name + " won the match! Congratulations!")
        self.RemovePlayerDirectly(Player)
        Player.Inventory.ClearAll()
        self.returnInventory(Player)
        winsini = self.Wins()
        for y in PointedPeople.keys():
            x = PointedPeople[y]
            if y == 3:
                p = 1.0
            elif y == 2:
                p = 3.0
            else:
                p = 5.0
            if winsini.GetSetting("Wins", x.SteamID) is not None:
                c = float(winsini.GetSetting("Wins", x.SteamID)) + p
                winsini.SetSetting("Wins", x.SteamID, str(c))
            else:
                winsini.AddSetting("Wins", x.SteamID, str(p))
        winsini.Save()
        Server.BroadcastFrom(sysname, pink + "---Stats---")
        try:
            Server.BroadcastFrom(sysname, "1st: " + PointedPeople[1].Name)
            Server.BroadcastFrom(sysname, "2nd: " + PointedPeople[2].Name)
            Server.BroadcastFrom(sysname, "3rd: " + PointedPeople[3].Name)
        except:
            Server.BroadcastFrom(sysname, "Failed to display stats...")
        arr = []
        if self.ItemRewards:
            max = random.randint(self.MinRewards, self.MaxRewards)
            for x in xrange(0, max):
                num = random.randint(1, len(Rewards.keys()) - 1)
                item = sorted(Rewards)[num]
                c = Rewards.get(item)
                if c != 1:
                    c = random.randint(1, c)
                Player.Inventory.AddItem(item, c)
                if AnnounceRewards:
                    arr.append(item)
        if AnnounceRewards:
            d = str.join(', ', arr)
            Server.BroadcastFrom(sysname, pink + "---Rewards---")
            Server.BroadcastFrom(sysname, pink + "Rewards he received: " + d)
        if LootStackClean:
            self.LootableObjects = UnityEngine.Object.FindObjectsOfType(self.LootableObject)
            for x in self.LootableObjects:
                if "lootsack" in x.name.lower():
                    dist = Util.GetVectorsDistance(self.Middle, x.transform.position)
                    if dist <= CDist:
                        x._inventory.Clear()
                        Util.DestroyObject(x.gameObject)
        self.Reset()
        self.ResetWalls()
        Player.MessageFrom(sysname, green + "You received your rewards!")
        Server.BroadcastFrom(sysname, red + "----------------------------HUNGERGAMES--------------------------------")

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Victim is not None and HurtEvent.Attacker is not None:
            weapon = HurtEvent.WeaponName
            d = (HurtEvent.Victim not in self.Players and HurtEvent.Attacker in self.Players) \
                and weapon != "Fall Damage"
            d2 = HurtEvent.Attacker in self.Players and weapon != "Fall Damage"
            d3 = HurtEvent.Victim in self.Players and HurtEvent.Attacker in self.Players and not self.HasStarted \
                 and weapon != "Fall Damage"
            if d:
                HurtEvent.DamageAmount = float(0)
            elif d2 and HurtEvent.Sleeper:
                HurtEvent.DamageAmount = float(0)
            elif d3:
                HurtEvent.DamageAmount = float(0)

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.Victim is not None:
            if DeathEvent.Victim in self.Players and self.HasStarted:
                self.RemovePlayerDirectly(DeathEvent.Victim, False, True)
                for cmd in self.RestrictedCommands:
                    DeathEvent.Victim.UnRestrictCommand(cmd)
                leng = len(self.Players)
                if leng < 3:
                    if leng == 2:
                        PointedPeople[3] = DeathEvent.Victim
                    elif leng == 1:
                        PointedPeople[2] = DeathEvent.Victim
                        PointedPeople[1] = self.Players[0]
                if leng > 1:
                    Server.BroadcastFrom(sysname, green + DeathEvent.Victim.Name + red + " has been killed. "
                                         + green + str(leng) + red + " Players are still alive.")
                    if RadDmg and leng <= CRad and not self.RadRunning:
                        self.RadRunning = True
                        Plugin.CreateTimer("RadiationActivate", 60000 * RadM).Start()
                else:
                    Server.BroadcastFrom(sysname, green + DeathEvent.Victim.Name + red + " has been killed. ")
                    self.EndGame(self.Players[0])
                if DeathEvent.Attacker is not None:
                    if DeathEvent.AttackerIsPlayer:
                        kills = self.Kills()
                        count = kills.GetSetting("Kills", DeathEvent.Attacker.SteamID)
                        if count is None:
                            count = 0
                        else:
                            count = int(count)
                        kills.AddSetting("Kills", DeathEvent.Attacker.SteamID, str(count + 1))
                        kills.Save()
            elif DeathEvent.Victim in self.Players and self.IsActive:
                self.RemovePlayerDirectly(DeathEvent.Victim, False, True)
                for cmd in self.RestrictedCommands:
                    DeathEvent.Victim.UnRestrictCommand(cmd)
                Server.BroadcastFrom(sysname, green + DeathEvent.Victim.Name + red + " has been killed. ")
                Server.BroadcastFrom(sysname, red + "The match didn't even start yet!")

    def On_PlayerDisconnected(self, Player):
        if Player in self.Players:
            if not self.HasStarted:
                self.RemovePlayerDirectly(Player, True)
                leng = len(self.Players)
                if leng < minp and Plugin.GetTimer("Force") is not None:
                    Server.BroadcastFrom(sysname, red + "Minimum player count is not enough to force start.")
                    Server.BroadcastFrom(sysname, red + "Stopping timer...")
                    Plugin.KillTimer("Force")
                Server.BroadcastFrom(sysname, green + Player.Name + red + " has disconnected. "
                                     + green + str(leng) + red + " Players are still in-game.")
            else:
                List = Plugin.CreateDict()
                List["Player"] = Player
                Awaiting.append(Player.UID)
                Plugin.CreateParallelTimer("LeftChecker", 60000, List).Start()
                Server.BroadcastFrom(sysname, green + Player.Name + red + " has 1 minute to reconnect!")

    def LeftCheckerCallback(self, timer):
        timer.Kill()
        List = timer.Args
        Player = List["Player"]
        if Player.UID not in Awaiting:
            return
        self.RemovePlayerDirectly(Player, True)
        leng = len(self.Players)
        Server.BroadcastFrom(sysname, green + Player.Name + red + " has failed to reconnect. "
                             + green + str(leng) + red + "  Players are still alive.")
        Awaiting.remove(Player.UID)
        for cmd in self.RestrictedCommands:
            Player.UnRestrictCommand(cmd)
        if leng < 3:
            if leng == 2:
                PointedPeople[3] = Player
            elif leng == 1:
                PointedPeople[2] = Player
                PointedPeople[1] = self.Players[0]
        if len(self.Players) == 1:
            self.EndGame(self.Players[0])

    def On_PlayerSpawned(self, Player, SpawnEvent):
        if Player.UID in Awaiting:
            Awaiting.remove(Player.UID)
            f = None
            for x in self.Players:
                if x.UID == Player.UID:
                    f = x
                    break
            if f is not None:
                self.Players.remove(f)
                self.Players.append(Player)
                f.CleanRestrictedCommands()
                for cmd in self.RestrictedCommands:
                    Player.RestrictCommand(cmd)
            Player.MessageFrom(sysname, green + "You reconnected in time!")
            return
        if DataStore.ContainsKey("HLastLoc", Player.SteamID):
            l = self.Replace(DataStore.Get("HLastLoc", Player.SteamID))
            loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
            Player.TeleportTo(loc)
            self.returnInventory(Player)
            DataStore.Remove("HLastLoc", Player.SteamID)
            self.Freezer(Player, 2, False)
            Player.AddAntiRad(Player.RadLevel)
            if self.GotRustPP:
                Server.GetRustPPAPI().GetFriendsCommand.RemoveTempException(Player.UID)

    def On_EntityDeployed(self, Player, Entity):
        if Player in self.Players:
            if not Building:
                Player.MessageFrom(sysname, "You can't spawn stuff in HG!")
                Entity.Destroy()
                return
            PlacedEntities.append(Entity)

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is None:
                return
            if HurtEvent.Attacker in self.Players:
                HurtEvent.Entity.Health = HurtEvent.Entity.MaxHealth
                HurtEvent.DamageAmount = float(0)
                return
            gun = HurtEvent.WeaponName
            if gun == "Shotgun":
                return
            if DataStore.ContainsKey("HDoorMode", id):
                if "wall" in HurtEvent.Entity.Name.lower():
                    ini = self.HungerGames()
                    count = len(ini.EnumSection("WallLocations"))
                    enum = ini.EnumSection("WallLocations")
                    data = str(HurtEvent.Entity.X) + "," + str(HurtEvent.Entity.Y) + "," + str(HurtEvent.Entity.Z)
                    for x in enum:
                        locs = ini.GetSetting("WallLocations", x)
                        if data in locs:
                            HurtEvent.Attacker.MessageFrom(sysname, "This wall is already in.")
                            HurtEvent.DamageAmount = float(0)
                            return
                    if maxp == count:
                        HurtEvent.Attacker.MessageFrom(sysname, "You reached the max spawnpoints")
                        return
                    name = HurtEvent.Entity.Name
                    c = count + 1
                    ini.AddSetting("WallLocations", name + "-" + str(c),
                                                   str(HurtEvent.Entity.X) + "," +
                                                   str(HurtEvent.Entity.Y) + "," +
                                                   str(HurtEvent.Entity.Z) + "," +
                                                   str(HurtEvent.Entity.Rotation.x) + "," +
                                                   str(HurtEvent.Entity.Rotation.y) + "," +
                                                   str(HurtEvent.Entity.Rotation.z) + "," +
                                                   str(HurtEvent.Entity.Rotation.w))
                    ini.Save()
                    HurtEvent.Attacker.MessageFrom(sysname, "Added Wall.")
                elif "box" in HurtEvent.Entity.Name.lower():
                    data = str(HurtEvent.Entity.X) + "," + str(HurtEvent.Entity.Y) + "," + str(HurtEvent.Entity.Z)
                    ini = self.HungerGames()
                    count = len(ini.EnumSection("ChestLocations"))
                    name = HurtEvent.Entity.Name
                    enum = ini.EnumSection("ChestLocations")
                    for x in enum:
                        locs = ini.GetSetting("ChestLocations", x)
                        if data in locs:
                            HurtEvent.Attacker.MessageFrom(sysname, "This chest is already in.")
                            HurtEvent.DamageAmount = float(0)
                            return
                    c = count + 1
                    ini.AddSetting("ChestLocations", name + "-" + str(c),
                                                   str(HurtEvent.Entity.X) + "," +
                                                   str(HurtEvent.Entity.Y) + "," +
                                                   str(HurtEvent.Entity.Z) + "," +
                                                   str(HurtEvent.Entity.Rotation.x) + "," +
                                                   str(HurtEvent.Entity.Rotation.y) + "," +
                                                   str(HurtEvent.Entity.Rotation.z) + "," +
                                                   str(HurtEvent.Entity.Rotation.w))
                    ini.Save()
                    HurtEvent.Attacker.MessageFrom(sysname, "Added Chest.")
                HurtEvent.DamageAmount = float(0)
