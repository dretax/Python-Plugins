__author__ = 'BogdanWDK,DreTaX'
__version__ = '1.3a'

import clr

clr.AddReferenceByPartialName("Fougerite")
import sys
import time
import Fougerite

red = "[color #FF0000]"
teal = "[color#00FFFF]"
orange = "[color#FF8000]"
purple = "[color#AB00CD]"
blue = "[color#0174DF]"
yellow = "[color#FFFF00]"
green = "[color#00ff40]"
white = "[color#ffffff]"
cyan = "[color#4dff98]"


class PlayerData:

    Name = None
    Level = None
    Experience = None

    def __init__(self, Name, Level, Experience):
        self.Name = Name
        self.Level = Level
        self.Experience = Experience

class TopFive:

    Name = None
    Level = None

    def __init__(self, Name, Level):
        self.Level = Level
        self.Name = Name

class LevelSystem:

    XpRate = None
    Levels = {}
    Players = {}
    DataBase = None
    TopPlayers = {}

    def On_PluginInit(self):
        Server.BroadcastFrom("[LevelSystem]", teal + "LevelSystem v"+ yellow + "" + __version__ + teal + " Loaded!")
        if not Plugin.IniExists("Settings"):
            Plugin.CreateIni("Settings")
            ini = Plugin.GetIni("Settings")
            ini.AddSetting("Config", "XpRate", "5")
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
            ini.Save()

        if not Plugin.IniExists("Database"):
            Plugin.CreateIni("Database")
            ini2 = Plugin.GetIni("Database")
            ini2.Save()

        self.DataBase = Plugin.GetIni("Database")
        for x in self.DataBase.EnumSection("Level"):
            name =str(self.DataBase.GetSetting("Name", x))
            exp = int(self.DataBase.GetSetting("Experience", x))
            level = int(self.DataBase.GetSetting("Level", x))
            uid = Data.ToUlong(x)
            self.Players[uid] = PlayerData(name, level, exp)

        ini = Plugin.GetIni("Settings")
        for x in ini.EnumSection("Level"):
            self.Levels[int(x)] = int(ini.GetSetting("Level", x)) 
        self.XpRate = int(ini.GetSetting("Config", "XpRate"))

    def On_PluginShutdown(self):
        self.DataBase.Save()

    def On_ServerSaved(self):
        self.DataBase.Save()
        Server.Broadcast("[Level System] Data Saved")

    def GetPlayerName(self, name):
        try:
            name = name.lower()
            for pl in Server.Players:
                if pl.Name.lower() == name:
                    return pl
            return None
        except:
            return None

    def CheckV(self, Player, args):
        count = 0
        if hasattr(args, '__len__') and (not isinstance(args, str)):
            p = self.GetPlayerName(str.join(" ", args))
            if p is not None:
                return p
            for pl in Server.Players:
                for namePart in args:
                    if namePart.lower() in pl.Name.lower():
                        p = pl
                        count += 1
                        continue
        else:
            nargs = str(args).lower()
            p = self.GetPlayerName(nargs)
            if p is not None:
                return p
            for pl in Server.Players:
                if nargs in pl.Name.lower():
                    p = pl
                    count += 1
                    continue
        if count == 0:
            Player.Message("Couldn't find " + str.join(" ", args) + "!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.Message("Found " + str(count) + " players with similar a name. Use a more correct name!")
            return None

    def On_PlayerDisconnected(self, Player):
        if Player.UID in self.Players.keys():
            self.DataBase.SetSetting("Name", Player.SteamID, str(self.Players[Player.UID].Name))
            self.DataBase.SetSetting("Level", Player.SteamID, str(self.Players[Player.UID].Level))
            self.DataBase.SetSetting("Experience", Player.SteamID, str(self.Players[Player.UID].Experience))
            self.Players.pop(Player.UID)

    def On_PlayerConnected(self, Player):
        if Player.UID not in self.Players.keys():
            if self.DataBase.GetSetting("Level", Player.SteamID) is not None:
                self.Players[Player.UID] = PlayerData(str(self.DataBase.GetSetting("Name", Player.SteamID)),
                                                      int(self.DataBase.GetSetting("Level", Player.SteamID)),
                                                      int(self.DataBase.GetSetting("Experience", Player.SteamID)))
            else:
                self.Players[Player.UID] = PlayerData(Player.Name,1, 0)
                self.DataBase.AddSetting("Name", Player.SteamID, str(Player.Name))
                self.DataBase.AddSetting("Level", Player.SteamID, "1")
                self.DataBase.AddSetting("Experience", Player.SteamID, "0")


    def On_PlayerGathering(self, Player, GatherEvent):
        level = self.Players[Player.UID].Level
        i = Player.Inventory.AddItem
        if Player.Inventory.FreeSlots > 0:
            if 1 <= level <= 9:
                gathered = GatherEvent.Quantity
                i(GatherEvent.Item, gathered)
                #GatherEvent.Quantity = gathered
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            elif 10 <= level <= 15:
                gathered = (GatherEvent.Quantity) * 2
                i(GatherEvent.Item, gathered)
                #GatherEvent.Quantity = gathered
                Player.InventoryNotice(str(gathered) + " x " + GatherEvent.Item)
            else:
                gathered = GatherEvent.Quantity
                GatherEvent.Quantity = gathered
                #Player.InventoryNotice(gathered + " x " + GatherEvent.Item)
        else:
            Player.InventoryNotice("No inventory space")

        currentlevel = self.Players[Player.UID].Level
        currentxp = self.Players[Player.UID].Experience
        totalxp = currentxp + self.XpRate
        if Player.Inventory.FreeSlots > 0:
            if currentlevel + 1 not in self.Levels.keys():
                return
            else:
                self.Players[Player.UID].Experience = totalxp
                self.DataBase.AddSetting("Experience", str(Player.SteamID), str(totalxp))

        #Test ======================================================================================
        experience = self.Players[Player.UID].Experience
        level = self.Players[Player.UID].Level
        if level + 1 not in self.Levels.keys() and DataStore.Get("ls_maxlevel_check", Player.SteamID) is None:
            Player.MessageFrom("[LevelSystem]", orange + "You have reached max level!")
            DataStore.Add("ls_maxlevel_check", Player.SteamID, 1)
            return
        level = level + 1
        nextlevel = self.Levels[level]
        # gatherrate = 2 * int(level)
        if 1 <= level <= 9:
            gatherrate = 2
        elif 10 <= level <= 15:
            gatherrate = 3
        else:
            gatherrate = 2
        if experience == nextlevel or experience >= nextlevel:
            self.DataBase.SetSetting("Level", str(Player.UID), str(level))
            self.Players[Player.UID].Level = level

            if experience == nextlevel:
                self.Players[Player.UID].Experience = 0
                self.DataBase.AddSetting("Experience", str(Player.UID), "0")
            else:
                calc = self.Players[Player.UID].Experience - nextlevel
                self.Players[Player.UID].Experience = calc
                self.DataBase.AddSetting("Experience", str(Player.UID), str(calc))

            Player.MessageFrom("[LevelSystem]", "------------[ " + teal + "Level System v" + yellow + __version__ + white + " ]------------")
            Player.MessageFrom("[LevelSystem]", green + "Congrats! You have reached Level "+ yellow + str(level))
            Player.MessageFrom("[LevelSystem]", green + "Your " + teal + "Gather Rate" + green + " is " + yellow + str(gatherrate))
            Server.BroadcastFrom("[LevelSystem]", yellow + "WHOO! " + yellow + Player.Name + green + " is now Level " + yellow + str(level))
            #Web.POST("http://165.227.149.72/levelsystem.php?name=" + str(Player.Name) + "&level=" + str(level) + "","data")




    def On_Command(self, Player, cmd, args):
        if cmd == "level":
            if len(args) == 0:
                experience = self.Players[Player.UID].Experience
                level = self.Players[Player.UID].Level
                nextlevel = 0
                xptolevelup = 0
                if level + 1 in self.Levels.keys():
                    nextlevel = self.Levels[level + 1]
                    if str(nextlevel).isdigit():
                        xptolevelup = nextlevel - experience

                # gatherrate = 2 * int(level)
                if 1 <= level <= 9:
                    gatherrate = 2
                elif 10 <= level <= 15:
                    gatherrate = 3
                else:
                    gatherrate = 2

                Player.MessageFrom("[LevelSystem]", "------------[ " + teal + "Level System v" + yellow + __version__ + white + " ]------------")
                Player.MessageFrom("[LevelSystem]", teal + "Use " + yellow + "/level help" + teal + " for available commands!")
                Player.MessageFrom("[LevelSystem]", green + "Level: " + yellow + str(level) + green + "/" + orange + "15")
                Player.MessageFrom("[LevelSystem]", green + "Gather Rate: " + yellow + str(gatherrate))
                Player.MessageFrom("[LevelSystem]", green + "XP Rate: " + red + str(self.XpRate))
                if level < 15:
                    Player.MessageFrom("[LevelSystem]", green + "Experience: " + yellow + str(experience) + green + "/" + orange + str(nextlevel))
                else:
                    Player.MessageFrom("[LevelSystem]", green + "Experience: " + yellow + " Max level reached!")

            elif len(args) == 4:
                if args[0] == "set":
                    if Player.Admin:
                        if args[1] is None or args[2] is None or args[3] is None:
                            Player.MessageFrom("[LevelSystem]", "Usage: /level set <name> <level> <experience>")
                        else:
                            name = self.CheckV(Player, args[1])
                            if name is not None:
                                self.Players[name.UID].Level = int(args[2])
                                lvl = self.Players[name.UID].Level
                                self.DataBase.AddSetting("Level", str(name.SteamID), str(lvl))
                                self.Players[name.UID].Experience = int(args[3])
                                exp = self.Players[name.UID].Experience
                                self.DataBase.AddSetting("Experience", str(name.SteamID), str(exp))
                                if DataStore.ContainsKey("ls_maxlevel_check", name.SteamID):
                                    DataStore.Remove("ls_maxlevel_check", name.SteamID)
                                Player.MessageFrom("LevelSystem", green + "Adjusted " + teal + "LVL/EXP" + green + " for " + yellow + name.Name)
                                
                            else:
                                Player.MessageFrom("[LevelSystem]", "Player not found :(")

            elif len(args) == 2:
                if args[0] == "info":
                    name = self.CheckV(Player, args[1])
                    if name is not None:
                        lvl = self.Players[name.UID].Level
                        exp = self.Players[name.UID].Experience
                        Player.MessageFrom("[LevelSystem]","------------[ " + teal + "Level System v" + yellow + __version__ + white + " ]------------")
                        Player.MessageFrom("[LevelSystem]", "" + teal + "Name: " + yellow + str(name.Name))
                        Player.MessageFrom("[LevelSystem]", "" + teal + "Level: " + yellow + str(lvl))
                        Player.MessageFrom("[LevelSystem]", "" + teal + "Experience: " + yellow + str(exp))
                    else:
                        Player.MessageFrom("[LevelSystem]", "" + orange + "Player not found :(")


            elif len(args) == 1:
                if args[0] == "reward":
                    level = self.Players[Player.UID].Level
                    reward5 = DataStore.ContainsKey("levelsystem_reward_level5", Player.SteamID)
                    reward10 = DataStore.ContainsKey("levelsystem_reward_level10", Player.SteamID)
                    reward15 = DataStore.ContainsKey("levelsystem_reward_level15", Player.SteamID)
                    if level == 5:
                        if reward5:
                            Player.MessageFrom("[LevelSystem]", yellow + "You already redeemed the Level 5 Reward!")
                        else:
                            if Player.Inventory.FreeSlots >= 6:
                                Player.Inventory.AddItem("Supply Signal", 1)
                                Player.Inventory.AddItem("Research Kit 1", 1)
                                Player.Inventory.AddItem("P250", 1)
                                Player.Inventory.AddItem("9mm Ammo", 50)
                                Player.Inventory.AddItem("Small Medkit", 3)
                                Player.Inventory.AddItem("Metal Fragments", 150)
                                Player.Inventory.AddItem("Gunpowder", 150)
                                DataStore.Add("levelsystem_reward_level5", Player.SteamID, 1)
                                Player.MessageFrom("[LevelSystem]", green + "You have redeemed the " + yellow + "Level 5 Reward" + green + "!")
                            else:
                                Player.MessageFrom("[LevelSystem]", green + "You don't have enough space in your inventory!")
                    elif level == 10:
                        if reward10:
                            Player.MessageFrom("[LevelSystem]", yellow + "You already redeemed the Level 10 Reward!")
                        else:
                            if Player.Inventory.FreeSlots >= 6:
                                Player.Inventory.AddItem("Supply Signal", 1)
                                Player.Inventory.AddItem("M4", 1)
                                Player.Inventory.AddItem("556 Ammo", 250)
                                Player.Inventory.AddItem("Large Medkit", 5)
                                Player.Inventory.AddItem("Metal Fragments", 250)
                                Player.Inventory.AddItem("Gunpowder", 250)
                                DataStore.Add("levelsystem_reward_level10", Player.SteamID, 1)
                                Player.MessageFrom("[LevelSystem]", green + "You have redeemed the " + yellow + "Level 10 Reward" + green + "!")
                            else:
                                Player.MessageFrom("[LevelSystem]", green + "You don't have enough space in your inventory!")
                    else:
                        Player.MessageFrom("[LevelSystem]", green + "You don't meet the requirements to redeem the reward!")
                #if args[0] == "flush":
                #    if Player.Admin:
                #        self.Levels.clear()
                #        self.Players.clear()
                #        Player.MessageFrom("[LevelSystem]", teal + "Database flushed")
                elif args[0] == "help":
                    Player.MessageFrom("[LevelSystem]","------------[ " + teal + "Level System v" + yellow + __version__ + white + " ]------------")
                    Player.MessageFrom("[LevelSystem]", green + "/level" + yellow + " - Level Stats")
                    Player.MessageFrom("[LevelSystem]", green + "/level reward" + yellow + " - Rewards for level 5/10/15")
                    Player.MessageFrom("[LevelSystem]", green + "/level info <name>" + yellow + " - Check a Player Level")
                    if Player.Admin:
                        Player.MessageFrom("[LevelSystem]", purple + "[AdminCMD] " + teal + "/level set <name> <level> <experience>")
                        #Player.MessageFrom("[LevelSystem]", purple + "[AdminCMD] " + teal + "/level flush" + orange + " [DO NOT USE - WIPE ONLY] Deletes all levels")
