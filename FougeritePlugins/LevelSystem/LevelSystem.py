__author__ = 'BogdanWDK, tuneup by DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Fougerite")
import sys
import Fougerite

red = "[color #FF0000]"
teal = "[color#00FFFF]"
orange = "[color#FF8000]"
purple = "[color#AB00CD]"
blue = "[color#0174DF]"
yellow = "[color#FFFF00]"

class PlayerData:

    Level = None
    Experience = None

    def __init__(self, Level, Experience):
        self.Level = Level
        self.Experience = Experience


class LevelSystem:

    XpRate = None
    CritXpRate = None
    MaxWoodLevel = None
    MaxMetalLevel = None
    Levels = {}
    Players = {}
    DataBase = None

    def On_PluginInit(self):
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "XpRate", "5")
            ini.AddSetting("Config", "CritXpRate", "3")
            ini.AddSetting("Config", "MaxWoodLevel", "25")
            ini.AddSetting("Config", "MaxMetalLevel", "25")
            ini.AddSetting("Level", "1", "150")
            ini.AddSetting("Level", "2", "300")
            ini.AddSetting("Level", "3", "450")
            ini.AddSetting("Level", "4", "600")
            ini.AddSetting("Level", "5", "750")
            ini.AddSetting("Level", "6", "900")
            ini.AddSetting("Level", "7", "1050")
            ini.AddSetting("Level", "8", "1200")
            ini.AddSetting("Level", "9", "1350")
            ini.AddSetting("Level", "10", "1500")
            ini.AddSetting("Level", "11", "1750")
            ini.AddSetting("Level", "12", "1900")
            ini.AddSetting("Level", "13", "2050")
            ini.AddSetting("Level", "14", "2200")
            ini.AddSetting("Level", "15", "2350")
            ini.AddSetting("Level", "16", "2500")
            ini.AddSetting("Level", "17", "2750")
            ini.AddSetting("Level", "18", "2900")
            ini.AddSetting("Level", "19", "3050")
            ini.AddSetting("Level", "20", "3200")
            ini.AddSetting("Level", "21", "3350")
            ini.AddSetting("Level", "22", "3500")
            ini.AddSetting("Level", "23", "3750")
            ini.AddSetting("Level", "24", "3900")
            ini.AddSetting("Level", "25", "4500")
            ini.Save()

        if not Plugin.IniExists("Database"):
            Plugin.CreateIni("Database")
            ini2 = Plugin.GetIni("Database")
            ini2.Save()

        self.DataBase = Plugin.GetIni("Database")
        for x in self.DataBase.EnumSection("Level"):
            exp = int(self.DataBase.GetSetting("Experience", x))
            level = int(self.DataBase.GetSetting("Level", x))
            uid = Data.ToUlong(x)
            self.Players[uid] = PlayerData(level, exp)

        ini = Plugin.GetIni("Settings")
        for x in ini.EnumSection("Level"):
            self.Levels[int(x)] = int(ini.GetSetting("Level", x))
        self.MaxMetalLevel = int(ini.GetSetting("Config", "MaxMetalLevel"))
        self.CritXpRate = int(ini.GetSetting("Config", "CritXpRate"))
        self.XpRate = int(ini.GetSetting("Config", "XpRate"))
        self.MaxWoodLevel = int(ini.GetSetting("Config", "MaxWoodLevel"))

    def On_PluginShutdown(self):
        self.DataBase.Save()

    def On_ServerSaved(self, Objects, Seconds):
        self.DataBase.Save()

    """def On_ServerShutdown(self):
        for x in self.Players.keys():
            if self.DataBase.GetSetting("Level", str(x)) is not None:
                self.DataBase.SetSetting("Level", str(x), str(self.Players[x].Level))
                self.DataBase.SetSetting("Experience", str(x), str(self.Players[x].Experience))
            else:
                self.DataBase.AddSetting("Level", str(x), str(self.Players[x].Level))
                self.DataBase.AddSetting("Experience", str(x), str(self.Players[x].Experience))
        self.DataBase.Save()"""

    def On_PlayerDisconnected(self, Player):
        if Player.UID in self.Players.keys():
            self.DataBase.SetSetting("Level", Player.SteamID, str(self.Players[Player.UID].Level))
            self.DataBase.SetSetting("Experience", Player.SteamID, str(self.Players[Player.UID].Experience))
            self.Players.pop(Player.UID)

    def On_PlayerConnected(self, Player):
        if Player.UID not in self.Players.keys():
            if self.DataBase.GetSetting("Level", Player.SteamID) is not None:
                self.Players[Player.UID] = PlayerData(int(self.DataBase.GetSetting("Level", Player.SteamID)),
                                                      int(self.DataBase.GetSetting("Experience", Player.SteamID)))
            else:
                self.Players[Player.UID] = PlayerData(1, 0)
                self.DataBase.AddSetting("Level", Player.SteamID, "1")
                self.DataBase.AddSetting("Experience", Player.SteamID, "0")

    def On_PlayerGathering(self, Player, GatherEvent):
        rate = self.Players[Player.UID].Level
        if Player.Inventory.FreeSlots > 0:
            # gathered = (GatherEvent.Quantity) + 2 * int(rate) # original one
            gathered = (GatherEvent.Quantity) * rate  # this is by level
            GatherEvent.Quantity = gathered
        else:
            Player.InventoryNotice("0 x " + GatherEvent.Item)

        currentxp = self.Players[Player.UID].Experience
        totalxp = currentxp + self.XpRate
        self.Players[Player.UID].Experience = totalxp
        self.DataBase.SetSetting("Experience", Player.SteamID, str(totalxp))

    def On_Command(self, Player, cmd, args):
        if cmd == "level":
            if len(args) == 0:
                Player.MessageFrom("[LevelSystem]", "" + blue + "==============================================")
                Player.MessageFrom("[LevelSystem]", "" + orange + "Level System v" + __version__)
                Player.MessageFrom("[LevelSystem]", "" + yellow + "More functions coming soon!")
                Player.MessageFrom("[LevelSystem]", "" + blue + "==============================================")
                Player.MessageFrom("[LevelSystem]",
                                   "" + orange + "/level stats " + teal + "|" + yellow + " Check Your level status")
                Player.MessageFrom("[LevelSystem]",
                                   "" + orange + "/level rankup" + teal + "|" + yellow + " Check if you have enough XP to rank up")
                Player.MessageFrom("[LevelSystem]", "" + blue + "==============================================")
            elif len(args) == 1:
                if args[0] == "stats":
                    experience = self.Players[Player.UID].Experience
                    level = self.Players[Player.UID].Level

                    nextlevel = "Maximum level reached."
                    xptolevelup = 0
                    if level + 1 in self.Levels.keys():
                        nextlevel = self.Levels[level + 1]
                        if str(nextlevel).isdigit():
                            xptolevelup = nextlevel - experience

                    # gatherrate = 2 * int(level)
                    gatherrate = level
                    Player.MessageFrom("[LevelSystem]", "" + blue + "==============================================")
                    Player.MessageFrom("[LevelSystem]", "" + orange + "Level System v1.0")
                    Player.MessageFrom("[LevelSystem]", "" + yellow + "More functions coming soon!")
                    Player.MessageFrom("[LevelSystem]", "" + blue + "==============================================")
                    Player.MessageFrom("[LevelSystem]",
                                       "" + orange + "Your Level: " + red + str(level) + orange + "/" + red + "25")
                    Player.MessageFrom("[LevelSystem]", "" + orange + "Gather Rate: " + red + str(gatherrate))
                    Player.MessageFrom("[LevelSystem]", "" + orange + "Experience gathered: " + red + " " + str(
                        experience) + " " + orange + "/" + red + " " + str(nextlevel) + " ! ")
                    Player.MessageFrom("[LevelSystem]", "" + orange + "You need " + red + str(
                        xptolevelup) + orange + " experience in order to Level up!")
                    Player.MessageFrom("[LevelSystem]", "" + blue + "==============================================")
                elif args[0] == "rankup":
                    experience = self.Players[Player.UID].Experience
                    level = self.Players[Player.UID].Level
                    if level + 1 not in self.Levels.keys():
                        Player.MessageFrom("[LevelSystem]", orange + "You have reached max level!")
                        return
                    level = level + 1
                    nextlevel = self.Levels[level]
                    # gatherrate = 2 * int(level)
                    gatherrate = level
                    if experience == nextlevel or experience >= nextlevel:
                        self.DataBase.SetSetting("Level", Player.UID, level)
                        self.Players[Player.UID].Level = level
                        Player.MessageFrom("[LevelSystem]",
                                           "" + blue + "==============================================")
                        Player.MessageFrom("[LevelSystem]",
                                           "" + orange + "You've been ranked up to " + yellow + "Level " + red + str(level))
                        Player.MessageFrom("[LevelSystem]",
                                           "" + orange + "Your Gather Rate has been increased to " + red + str(
                                               str(gatherrate)))
                        Player.MessageFrom("[LevelSystem]",
                                           "" + blue + "==============================================")
                    else:
                        Player.MessageFrom("[LevelSystem]",
                                           "" + orange + "You don't have enough " + red + "Experience " + orange + "to rank up!")
                        Player.MessageFrom("[LevelSystem]",
                                           "" + orange + "Type " + red + "/level stats " + orange + "for more info about your level and experience")
