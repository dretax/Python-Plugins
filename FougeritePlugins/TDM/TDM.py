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
#  MaxPlayers!
maxp = 40
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
    AdminSpot = Util.CreateVector(0, 0, 0)
    RestrictedCommands = None

    def On_PluginInit(self):
        data = self.TDMData()
        lobby = Util.ConvertStringToVector3(data.GetSetting("Settings", "LobbyPosition"))
        t1 = Util.ConvertStringToVector3(data.GetSetting("Settings", "Team1Position"))
        t2 = Util.ConvertStringToVector3(data.GetSetting("Settings", "Team2Position"))
        asp = Util.ConvertStringToVector3(data.GetSetting("Settings", "AdminSpot"))
        enum = data.EnumSection("RestrictedCommands")
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
            ini.AddSetting("Settings", "Team1Position", str(self.LobbyPosition))
            ini.AddSetting("Settings", "Team2Position", str(self.LobbyPosition))
            ini.AddSetting("Settings", "AdminSpot", str(self.AdminSpot))
            ini.Save()
        return Plugin.GetIni("TDMData")


    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        if cmd == "tdm":
            if len(args) == 0:
                Player.MessageFrom(sysname, teal + "TDM By " + __author__ + " " + blue + "V" + __version__)
                Player.MessageFrom(sysname, green + "/tdm join - Join HG")
                return
