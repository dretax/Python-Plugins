__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import sys
import re
from Fougerite import Entity
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

import random
import math

#  Colors
blue = "[color #0099FF]"
red = "[color #FF0000]"
pink = "[color #CC66FF]"
teal = "[color #00FFFF]"
green = "[color #009900]"
purple = "[color #6600CC]"
white = "[color #FFFFFF]"
yellow = "[color #FFFF00]"


Players = []
Team1 = []
Team2 = []
walls = []
PlacedEntities = []
Data = {

}

ShopData = {

}

EntityList = {
    "WoodBoxLarge": ";deploy_wood_storage_large",
    "WoodBox": ";deploy_wood_box",
    "SmallStash": ";deploy_small_stash",
    "MetalWall": ";struct_metal_wall",
    "WoodWall": ";struct_wood_wall"
}

# Maximum Team Count
Team1Max = 10
Team2Max = 10
# Don't even ask
MaxRounds = 15
#  Minimum players to start the MinimumTime counter.
MinimumPlayers = 10
#  Timer for the force start at minimum players.
#  If we reach 7 players we start the timer. Once It elapsed we start the game.
#  This is in minutes
MinimumTime = 2
# MaxPlayers
MaxPlayers = Team1Max + Team2Max
#  Secs before match start
secs = 30
#  Cleanup loots Stacks after game in close range?
LootStackClean = True
#  Distance if we look from the middle? (Size of the Arena in meters, circle)
CDist = 200
# Metal Walls for spawn points = 1 ; Wood Walls = 2 (For destroy/respawning)
WallsSpawn = 2
#  For safety reasons should we freeze the player when he joins for 2 secs?
Freeze = True
# Announce Cooldown WhiteList
WhiteList = ["7656119798204xxxx", "7656119798204yyyy"]
# Cooldown in minutes
AnnounceCooldown = 30
# Allow building in HG? If this is true, then the deployed entities will be destroyed at the end of the game.
Building = False

sysname = "TDM"


class TDM:

    ZeroVector = Util.CreateVector(0, 0, 0)
    IsActive = False
    IsStarting = False
    HasStarted = False
    LobbyPosition = Util.CreateVector(0, 0, 0)
    Team1Position = Util.CreateVector(0, 0, 0)
    Team2Position = Util.CreateVector(0, 0, 0)
    AdminSpot = Util.CreateVector(0, 0, 0)
    RestrictedCommands = None
    GotRustPP = None
    StartMoney = 800
    TeamWinMoney = 3200
    TeamLoseMoney = 1800
    Round = 1
    Team1Rounds = 0
    Team2Rounds = 0
    st = None
    dp = None

    def On_PluginInit(self):
        self.dp = Util.TryFindReturnType("DeployableObject")
        self.st = Util.TryFindReturnType("StructureComponent")
        data = self.TDMData()
        lobby = Util.ConvertStringToVector3(data.GetSetting("Settings", "LobbyPosition"))
        t1 = Util.ConvertStringToVector3(data.GetSetting("Settings", "Team1Position"))
        t2 = Util.ConvertStringToVector3(data.GetSetting("Settings", "Team2Position"))
        asp = Util.ConvertStringToVector3(data.GetSetting("Settings", "AdminSpot"))
        enum = data.EnumSection("RestrictedCommands")
        self.GotRustPP = Server.HasRustPP
        self.RestrictedCommands = Plugin.CreateList()
        for x in enum:
            self.RestrictedCommands.Add(data.GetSetting("RestrictedCommands", x))
        if lobby != self.ZeroVector:
            self.LobbyPosition = lobby
        if t1 != self.ZeroVector:
            self.Team1Position = t1
        if t2 != self.ZeroVector:
            self.Team2Position = t2
        if asp != self.ZeroVector:
            self.AdminSpot = asp
        self.StartMoney = int(data.GetSetting("Settings", "StartMoney"))
        self.TeamWinMoney = int(data.GetSetting("Settings", "TeamWinMoney"))
        self.TeamLoseMoney = int(data.GetSetting("Settings", "TeamLoseMoney"))
        shopenum = data.EnumSection("Shop")
        for x in shopenum:
            category = x.split(":")

        Util.ConsoleLog("TDM by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def Replace(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(',')

    def ResetWalls(self):
        ini = self.TDMData()
        enum3 = ini.EnumSection("WallLocations")
        for wall in enum3:
            l = ini.GetSetting("WallLocations", wall).split(',')
            name = wall.split('-')
            loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
            quat = Util.CreateQuat(float(l[3]), float(l[4]), float(l[5]), float(l[6]))
            self.FindWalls(loc, name[0], quat)

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

        DataStore.Add("TDMINV", id, Inventory)
        DataStore.Save()
        Player.Inventory.ClearAll()

    def returnInventory(self, Player):
        id = Player.SteamID
        if DataStore.ContainsKey("TDMINV", id):
            Inventory = DataStore.Get("TDMINV", id)
            Player.Inventory.ClearAll()
            for dictionary in Inventory:
                if dictionary['name'] is not None:
                    Player.Inventory.AddItemTo(dictionary['name'], dictionary['slot'], dictionary['quantity'])
                else:
                    Player.MessageFrom(sysname, red + "No dictionary found in the for cycle?!")
            Player.MessageFrom(sysname, green + "Your have received your original inventory")
            DataStore.Remove("TDMINV", id)
        else:
            Player.MessageFrom(sysname, red + "No Items of your last inventory found!")

    def DecayMaxHP(self):
        c = 0
        for entity in World.Entities:
            if "spike" in entity.Name.lower():
                if Util.GetVectorsDistance(self.LobbyPosition, entity.Location) <= CDist:
                    entity.SetDecayEnabled(False)
                    try:
                        entity.Health = entity.MaxHealth
                    except:
                        pass
                    c += 1
        return c

    def TDMData(self):
        if not Plugin.IniExists("TDMData"):
            ini = Plugin.CreateIni("TDMData")
            ini.AddSetting("RestrictedCommands", "1", "tpa")
            ini.AddSetting("RestrictedCommands", "2", "home")
            ini.AddSetting("RestrictedCommands", "3", "shop")
            ini.AddSetting("RestrictedCommands", "4", "destroy")
            ini.AddSetting("RestrictedCommands", "5", "starter")
            ini.AddSetting("RestrictedCommands", "6", "buy")
            ini.AddSetting("RestrictedCommands", "7", "sell")
            ini.AddSetting("Settings", "LobbyPosition", str(self.LobbyPosition))
            ini.AddSetting("Settings", "Team1Position", str(self.LobbyPosition))
            ini.AddSetting("Settings", "Team2Position", str(self.LobbyPosition))
            ini.AddSetting("Settings", "AdminSpot", str(self.AdminSpot))
            ini.AddSetting("Settings", "StartMoney", str(self.StartMoney))
            ini.AddSetting("Settings", "TeamWinMoney", str(self.TeamWinMoney))
            ini.AddSetting("Settings", "TeamLoseMoney", str(self.TeamLoseMoney))
            ini.AddSetting("StartingItems", "Revolver", "1")
            ini.AddSetting("StartingItems", "9mm Ammo", "35")
            ini.AddSetting("StartingItems", "Bandage", "5")
            ini.AddSetting("StartingItems", "Cloth Helmet", "1")
            ini.AddSetting("StartingItems", "Cloth Vest", "1")
            ini.AddSetting("StartingItems", "Cloth Pants", "1")
            ini.AddSetting("StartingItems", "Cloth Boots", "1")
            ini.AddSetting("Shop", "Equipment:1", "Kevlar:950")
            ini.AddSetting("Shop", "Equipment:2", "Kevlar + Helmet:1300")
            ini.AddSetting("Shop", "Equipment:3", "Light Kevlar:650")
            ini.AddSetting("Shop", "Equipment:4", "Light Kevlar + Helmet:900")
            ini.AddSetting("Shop", "Equipment:5", "Grenade:300")
            ini.AddSetting("Shop", "Equipment:6", "Flare:250")
            ini.AddSetting("Shop", "Equipment:7", "DeployableShield(x10):1000")
            ini.AddSetting("Shop", "Guns:1", "Hand Shotgun:450")
            ini.AddSetting("Shop", "Guns:2", "M9:500")
            ini.AddSetting("Shop", "Guns:3", "P250:800")
            ini.AddSetting("Shop", "Guns:4", "Pipe Shotgun:1200")
            ini.AddSetting("Shop", "Guns:5", "Shotgun:1800")
            ini.AddSetting("Shop", "Guns:6", "MP5:2400")
            ini.AddSetting("Shop", "Guns:7", "M4:3100")
            ini.AddSetting("Shop", "Guns:8", "AWP:4750")
            ini.AddSetting("Shop", "Close Combat:1", "Knife:300")
            ini.AddSetting("Shop", "Close Combat:2", "Pick Axe:320")
            ini.AddSetting("ShopMeaning", "Kevlar", "Kevlar Vest:1,Kevlar Pants:1,Kevlar Boots:1")
            ini.AddSetting("ShopMeaning",
                           "Kevlar + Helmet,", "Kevlar Helmet:1,Kevlar Vest:1,Kevlar Pants:1,Kevlar Boots:1")
            ini.AddSetting("ShopMeaning", "Light Kevlar", "Leather Vest:1,Leather Pants:1,Leather Boots:1")
            ini.AddSetting("ShopMeaning",
                           "Light Kevlar + Helmet", "Leather Helmet:1,Leather Vest:1,Leather Pants:1,Leather Boots:1")
            ini.AddSetting("ShopMeaning", "Grenade", "F1 Grenade:1")
            ini.AddSetting("ShopMeaning", "Flare", "Flare:1")
            ini.AddSetting("ShopMeaning", "Hand Shotgun", "Hand Cannon:1")
            ini.AddSetting("ShopMeaning", "M9", "9mm Pistol:1")
            ini.AddSetting("ShopMeaning", "P250", "P250:1")
            ini.AddSetting("ShopMeaning", "Pipe Shotgun", "Pipe Shotgun:1")
            ini.AddSetting("ShopMeaning", "Shotgun", "Shotgun:1")
            ini.AddSetting("ShopMeaning", "MP5", "MP5A4:1")
            ini.AddSetting("ShopMeaning", "M4", "M4:1")
            ini.AddSetting("ShopMeaning", "AWP", "Bolt Action Rifle:1")
            ini.AddSetting("ShopMeaning", "Knife", "Hatchet:1")
            ini.AddSetting("ShopMeaning", "Pick Axe", "Pick Axe:1")
            ini.AddSetting("ShopMeaning", "DeployableShield(x10)", "Wood Barricade:10")
            ini.Save()
        return Plugin.GetIni("TDMData")

    def RemovePlayerDirectly(self, Player, Disconnected=False, Dead=False, Remove=True):
        id = Player.SteamID
        if Player in Players and Remove:
            Players.remove(Player)
        if self.GotRustPP:
            Server.GetRustPPAPI().GetFriendsCommand.RemoveTempException(Player.UID)
        DataStore.Remove("TDMIG", id)
        for cmd in self.RestrictedCommands:
            Player.UnRestrictCommand(cmd)
        if not Disconnected:
            if DataStore.ContainsKey("TDMLastLoc", id) and not Dead:
                l = self.Replace(DataStore.Get("TDMLastLoc", id))
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                Player.TeleportTo(loc)
                DataStore.Remove("TDMLastLoc", id)

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

    def StartGame(self, ForceStart=False):
        if self.HasStarted or not self.IsActive:
            return
        if Plugin.GetTimer("TDMStartingIn") is not None:
            Server.BroadcastFrom(sysname, red + "A player has joined while TDM loaded. (Free Slot)")
            Server.BroadcastFrom(sysname, red + "Current Players: " + str(len(Players)))
            return
        leng = len(Players)
        if leng < MaxPlayers and not ForceStart:
            Server.BroadcastFrom(sysname, red
                                 + "----------------------------TDM--------------------------------")
            Server.BroadcastFrom(sysname, green + "Currently " + str(leng) +
                                 " of " + str(MaxPlayers) + " players are waiting.")
            Server.BroadcastFrom(sysname, green + "Type /tdm for the commands, and join!")
        else:
            if Plugin.GetTimer("TDMForce") is not None:
                Plugin.KillTimer("TDMForce")
            if self.IsStarting:
                return
            Server.BroadcastFrom(sysname, red + "----------------------------TDM--------------------------------")
            if ForceStart:
                Server.BroadcastFrom(sysname, green + "TDM force started!")
                Server.BroadcastFrom(sysname, green + "Prepairing...")
            try:
                self.DecayMaxHP()
            except:
                pass
            Server.BroadcastFrom(sysname, green + "Loading.........")
            ini = self.TDMData()
            enum3 = ini.EnumSection("WallLocations")
            for wall in enum3:
                l = ini.GetSetting("WallLocations", wall).split(',')
                name = wall.split('-')
                loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                quat = Util.CreateQuat(float(l[3]), float(l[4]), float(l[5]), float(l[6]))
                self.FindWalls(loc, name[0], quat)

            Server.BroadcastFrom(sysname, green + "Loaded 100%!")
            Plugin.CreateTimer("StartingIn", secs * 1000).Start()
            Server.BroadcastFrom(sysname, green + "TDM is starting in " + blue + str(secs) +
                                 green + " seconds!")
            self.IsStarting = True

    def On_EntityDeployed(self, Player, Entity, ActualPlacer):
        if ActualPlacer in Players:
            if not Building:
                ActualPlacer.MessageFrom(sysname, "You can't spawn stuff in TDM!")
                Entity.Destroy()
                return
            PlacedEntities.append(Entity)

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay:
            if not HurtEvent.AttackerIsPlayer:
                return
            if HurtEvent.Attacker in Players:
                HurtEvent.Entity.Health = HurtEvent.Entity.MaxHealth
                HurtEvent.DamageAmount = float(0)
                return
            gun = HurtEvent.WeaponName
            if gun == "Shotgun":
                return
            id = HurtEvent.Attacker.SteamID
            if DataStore.ContainsKey("TDMDoorMode", id):
                if "wall" in HurtEvent.Entity.Name.lower():
                    ini = self.TDMData()
                    count = len(ini.EnumSection("WallLocations"))
                    enum = ini.EnumSection("WallLocations")
                    data = str(HurtEvent.Entity.X) + "," + str(HurtEvent.Entity.Y) + "," + str(HurtEvent.Entity.Z)
                    for x in enum:
                        locs = ini.GetSetting("WallLocations", x)
                        if data in locs:
                            HurtEvent.Attacker.MessageFrom(sysname, "This wall is already in.")
                            HurtEvent.DamageAmount = float(0)
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
                HurtEvent.DamageAmount = float(0)

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "tdm":
            if len(args) == 0:
                Player.MessageFrom(sysname, teal + "TDM By " + __author__ + " " + blue + "V" + __version__)
                Player.MessageFrom(sysname, green + "/tdm join - Join HG")
                return
            if args[0] == "announce":
                if Player.Admin or Player.Moderator:
                    time = DataStore.Get("TDMACD", "Time")
                    if time is None:
                        DataStore.Add("TDMACD", "Time", 7)
                        time = 7
                    calc = System.Environment.TickCount - time
                    if calc < 0 or math.isnan(calc) or math.isnan(time):
                        DataStore.Add("TDMACD", "Time", 7)
                        time = 7
                    if calc >= AnnounceCooldown * 60000 or time == 7 or id in WhiteList:
                        if self.IsActive:
                            Player.MessageFrom(sysname, "TDM is already active!")
                        else:
                            Server.BroadcastFrom(sysname, red
                                                 + "----------------------------TDM--------------------------------")
                            Server.BroadcastFrom(sysname, green
                                                 + "TDM is now active! Type /tdm join to enter the battle!")
                            Server.BroadcastFrom(sysname, green + "Type /tdm to know more!")
                            Server.BroadcastFrom(sysname, teal + "Pack your items at home just in-case!")
                            Server.BroadcastFrom(sysname, teal + "The plugins saves your inventory when you join.")
                            Server.BroadcastFrom(sysname, red
                                                 + "----------------------------TDM--------------------------------")
                            self.RandomAdmin = Player
                            self.IsActive = True
                            self.ResetWalls()
                            del Players[:]
                            if Plugin.GetTimer("TDMStartingIn") is not None:
                                Plugin.KillTimer("StartingIn")
                            if Plugin.GetTimer("Force") is not None:
                                Plugin.KillTimer("Force")
                    else:
                        done = round((calc / 1000) / 60, 2)
                        Player.Notice("Cooldown: " + str(done) + "/" + str(AnnounceCooldown))
                else:
                    Player.Message("You aren't admin!")
            elif args[0] == "addspectatorspawn":
                if Player.Admin:
                    ini = self.TDMData()
                    if ini.GetSetting("Settings", "LobbyPosition") is not None:
                        ini.SetSetting("Settings", "LobbyPosition", str(Player.Location))
                        ini.Save()
                        self.LobbyPosition = Player.Location
                        Player.MessageFrom(sysname, green + "Set!")
                    else:
                        ini.AddSetting("Settings", "LobbyPosition", str(Player.Location))
                        ini.Save()
                        self.LobbyPosition = Player.Location
                        Player.MessageFrom(sysname, green + "Set!")
            elif args[0] == "team1spawn":
                if Player.Admin:
                    ini = self.TDMData()
                    if ini.GetSetting("Settings", "Team1Position") is not None:
                        ini.SetSetting("Settings", "Team1Position", str(Player.Location))
                        ini.Save()
                        self.Team1Position = Player.Location
                        Player.MessageFrom(sysname, green + "Set!")
                    else:
                        ini.AddSetting("Settings", "Team1Position", str(Player.Location))
                        ini.Save()
                        self.Team1Position = Player.Location
                        Player.MessageFrom(sysname, green + "Set!")
            elif args[0] == "team2spawn":
                if Player.Admin:
                    ini = self.TDMData()
                    if ini.GetSetting("Settings", "Team2Position") is not None:
                        ini.SetSetting("Settings", "Team2Position", str(Player.Location))
                        ini.Save()
                        self.Team2Position = Player.Location
                        Player.MessageFrom(sysname, green + "Set!")
                    else:
                        ini.AddSetting("Settings", "Team2Position", str(Player.Location))
                        ini.Save()
                        self.Team2Position = Player.Location
                        Player.MessageFrom(sysname, green + "Set!")
            elif args[0] == "entity":
                if Player.Admin:
                    if DataStore.ContainsKey("TDMDoorMode", id):
                        DataStore.Remove("TDMDoorMode", id)
                        Player.MessageFrom(sysname, "You quit Entity Adding mode.")
                    else:
                        DataStore.Add("TDMDoorMode", id, 1)
                        Player.MessageFrom(sysname, "You are in Entity Adding mode.")
                        Player.MessageFrom(sysname, "Hit the SpawnPoint Shelter's door.")
                        Player.MessageFrom(sysname, "You can't use shotgun.")
            elif args[0] == "join":
                if not self.IsActive:
                    Player.MessageFrom(sysname, "TDM is not active.")
                    return
                if self.HasStarted:
                    Player.MessageFrom(sysname, "There is a game in progress.")
                    return
                if len(Players) == MaxPlayers:
                    Player.MessageFrom(sysname, red + "TDM is full!")
                    return
                if Player in Players:
                    Player.MessageFrom(sysname, "You are already in the game, nab.")
                else:
                    if DataStore.ContainsKey("TDMINV", id):
                        Player.MessageFrom(sysname, green + "First you have to do /tdm inventory !")
                        return
                    Players.append(Player)
                    for cmd in self.RestrictedCommands:
                        Player.RestrictCommand(cmd)
                    leng = len(Players)
                    DataStore.Add("TDMLastLoc", Player.SteamID, str(Player.Location))
                    Player.TeleportTo(self.LobbyPosition, False)
                    self.recordInventory(Player)
                    Player.MessageFrom(sysname, "You joined the game!")
                    DataStore.Add("TDMIG", id, "1")
                    if self.GotRustPP:
                        Server.GetRustPPAPI().RemoveGod(Player.UID)
                        Server.GetRustPPAPI().RemoveInstaKO(Player.UID)
                        Server.GetRustPPAPI().GetFriendsCommand.AddTempException(Player.UID)
                    if leng == MinimumPlayers and Plugin.GetTimer("Force") is None:
                        if self.IsStarting or self.HasStarted:
                            return
                        Server.BroadcastFrom(sysname, pink + "Detected " + str(MinimumPlayers) + " players.")
                        Server.BroadcastFrom(sysname, pink + "Forcing game start in " + str(MinimumTime)
                                             + " minutes.")
                        Plugin.CreateTimer("ForceTDM", MinimumTime * 60000).Start()
                    self.StartGame()
            elif args[0] == "leave":
                if not self.IsActive:
                    Player.MessageFrom(sysname, "TDM is not active.")
                    return
                if Player not in Players:
                    Player.MessageFrom(sysname, "You are not even in the game, nab.")
                else:
                    leng = len(Players)
                    if leng > 1:
                        self.RemovePlayerDirectly(Player)
                        for cmd in self.RestrictedCommands:
                            Player.UnRestrictCommand(cmd)
                        leng = len(Players)
                        if self.HasStarted:
                            Server.BroadcastFrom(sysname, green + Player.Name + red + " has left TDM. "
                                                    + green + str(leng) + red + " Players are still alive.")
                        else:
                            Server.BroadcastFrom(sysname, green + Player.Name + red + " has left TDM. "
                                                     + green + str(leng) + red + " Players are still in-game.")
                        self.returnInventory(Player)
                    else:
                        Server.BroadcastFrom(sysname, green + Player.Name + red + " has left TDM. ")
                        Player.MessageFrom(sysname, teal + "Use /tdm inventory to get your old inventory back.")
                        if self.HasStarted:
                            self.EndGame(Players[0])
                    leng = len(Players)
                    if leng < MinimumPlayers and Plugin.GetTimer("ForceTDM") is not None:
                        Server.BroadcastFrom(sysname, red + "Minimum player count is not enough to force start.")
                        Server.BroadcastFrom(sysname, red + "Stopping timer...")
                        Plugin.KillTimer("ForceTDM")


class PlayerData:
    TDMInstance = None
    Player = None
    Money = 0
    Team = None
    Dead = False

    def __init__(self, TDMInstance, Player):
        self.TDMInstance = TDMInstance
        self.Player = Player
        self.Money = TDMInstance.StartMoney
