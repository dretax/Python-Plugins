__author__ = 'DreTaX'
__version__ = '1.0'
import clr

clr.AddReferenceByPartialName("Fougerite")
import Fougerite
import sys
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

import random

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
#  Distance for loots if we look from the middle? (Size of the Arena in meters)
CDist = 310
#  For safety reasons should we freeze the player when he joins for 2 secs?
Freeze = True

sysname = "TDM"
DataStoreName = "TDMDB"


class TDM:

    ZeroVector = Util.CreateVector(0, 0, 0)
    IsActive = False
    IsStarting = False
    HasStarted = False
    LobbyPosition = Util.CreateVector(0, 0, 0)
    Team1Position = Util.CreateVector(0, 0, 0)
    Team2Position = Util.CreateVector(0, 0, 0)
    SpectatePosition = Util.CreateVector(0, 0, 0)
    AdminSpot = Util.CreateVector(0, 0, 0)
    RestrictedCommands = None
    GotRustPP = None
    StartMoney = 800
    TeamWinMoney = 3200
    TeamLoseMoney = 1800

    def On_PluginInit(self):
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

        Util.ConsoleLog("TDM by " + __author__ + " Version: " + __version__ + " loaded.", False)

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
            ini.AddSetting("Settings", "SpectatePosition", str(self.SpectatePosition))
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
            ini.AddSetting("ShopMeaning", "Kevlar + Helmet,", "Kevlar Helmet:1,Kevlar Vest:1,Kevlar Pants:1,Kevlar Boots:1")
            ini.AddSetting("ShopMeaning", "Light Kevlar", "Leather Vest:1,Leather Pants:1,Leather Boots:1")
            ini.AddSetting("ShopMeaning", "Light Kevlar + Helmet", "Light Helmet:1,Light Vest:1,Light Pants:1,Light Boots:1")
            ini.AddSetting("ShopMeaning", "Grenade", "F1 Grenade:1")
            ini.AddSetting("ShopMeaning", "Flare", "Flare:1")
            ini.Save()
        return Plugin.GetIni("TDMData")


    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "tdm":
            if len(args) == 0:
                Player.MessageFrom(sysname, teal + "TDM By " + __author__ + " " + blue + "V" + __version__)
                Player.MessageFrom(sysname, green + "/tdm join - Join HG")
                return
            if args[0] == "join":
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
                    # todo: Continue code here
                    if DataStore.ContainsKey(DataStoreName, id):
                        Player.MessageFrom(sysname, green + "First you have to do /hg inventory !")
                        return
                    Players.append(Player)
                    for cmd in self.RestrictedCommands:
                        Player.RestrictCommand(cmd)
                    leng = len(Players)
                    DataStore.Add("TDMLastLoc", Player.SteamID, str(Player.Location))
                    l = self.Replace(ini.GetSetting("SpawnLocations", str(leng)))
                    loc = Util.CreateVector(float(l[0]), float(l[1]), float(l[2]))
                    Player.TeleportTo(loc, False)
                    self.recordInventory(Player)
                    enum = ini2.EnumSection("DefaultItems")
                    for item in enum:
                        c = int(ini2.GetSetting("DefaultItems", item))
                        Player.Inventory.AddItem(item, c)
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
                        Server.BroadcastFrom(sysname, pink + "Forcing game start in " + str(MinimumTime) +
                                                 " minutes.")
                        Plugin.CreateTimer("Force", MinimumTime * 60000).Start()
                    # self.StartGame()
