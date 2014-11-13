__author__ = 'DreTaX'
__version__ = '1.1'

import clr

clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("UnityEngine")
import Pluton
import UnityEngine
from UnityEngine import Vector3
import math
import System
from System import *
import re


"""
    Class
"""
class HomeSystem:

    """
        Timer
    """

    def HomeDelayCallback(self, timer):
        timer.Kill()
        config = self.HomeConfig()
        homesystemname = config.GetSetting("Settings", "homesystemname")
        safetp = int(config.GetSetting("Settings", "safetpcheck"))
        HomeSystem = timer.Args
        Player = Server.FindPlayer(HomeSystem["Player"])
        if Player is None:
            return
        PLX = HomeSystem["LocationX"]
        PLX = re.sub('[)\(\[\'\]\-\,]', '', str(PLX))
        PLZ = HomeSystem["LocationZ"]
        PLZ = re.sub('[)\(\[\'\]\-\,]', '', str(PLZ))
        HLoc = HomeSystem["HomeLocation"]
        HLoc = re.sub('[)\(\[\'\]]', '', str(HLoc))
        HLoc = HLoc.split(',')
        movec = int(config.GetSetting("Settings", "movecheck"))
        if movec == 1:
            if int(float(PLX)) != int(float(Player.X)) or int(float(PLZ)) != int(float(Player.Z)):
                Player.MessageFrom(homesystemname, "You moved before teleporting!")
                return
        Player.GroundTeleport(float(HLoc[0]),float(HLoc[1]) + 5.5, float(HLoc[2]))
        if safetp > 0:
            Plugin.CreateParallelTimer("HomeSafeTy", safetp * 1000, HomeSystem).Start()
        Player.MessageFrom(homesystemname, "Teleported to Home!")
        return



    def HomeSafeTyCallback(self, timer):
        timer.Kill()
        config = self.HomeConfig()
        homesystemname = config.GetSetting("Settings", "homesystemname")
        HomeSystem = timer.Args
        Player = Server.FindPlayer(HomeSystem["Player"])
        if Player is None:
            return
        HLoc = HomeSystem["HomeLocation"]
        HLoc = re.sub('[)\(\[\'\]]', '', str(HLoc))
        HLoc = HLoc.split(',')
        Home = Vector3(float(HLoc[0]), float(HLoc[1]) + 5.5, float(HLoc[2]))
        Player.Teleport(Home)
        Player.MessageFrom(homesystemname, "Teleported Again!")

    """
        Methods
    """

    def Homes(self):
        if not Plugin.IniExists("Homes"):
            homes = Plugin.CreateIni("Homes")
            homes.Save()
        return Plugin.GetIni("Homes")

    def Wl(self):
        if not Plugin.IniExists("WhiteListedPlayers"):
            homes = Plugin.CreateIni("WhiteListedPlayers")
            homes.Save()
        return Plugin.GetIni("WhiteListedPlayers")

    def FriendOf(self, id, selfid):
        ini = self.Wl()
        check = ini.GetSetting(id, selfid)
        if check and check is not None:
            return True
        return False

    def DefaultLoc(self):
        if not Plugin.IniExists("DefaultLoc"):
            loc = Plugin.CreateIni("DefaultLoc")
            loc.Save()
        return Plugin.GetIni("DefaultLoc")

    def HomeOf(self, Player, Home):
        ini = self.Homes()
        check = ini.GetSetting(Player.SteamID, Home)
        if check is not None:
            c = check.replace("(", "")
            c = c.replace(")", "")
            return c.split(",")
        return None

    def HomeOfID(self, id, Home):
        ini = self.Homes()
        check = ini.GetSetting(id, Home)
        if check is not None:
            c = check.replace("(", "")
            c = c.replace(")", "")
            return c.split(",")
        return None

    def HomeConfig(self):
        if not Plugin.IniExists("HomeConfig"):
            homes = Plugin.CreateIni("HomeConfig")
            homes.Save()
        return Plugin.GetIni("HomeConfig")


    def GetPlayer(self, namee):
        name = namee.lower()
        for pl in Server.ActivePlayers:
            if pl.Name.lower() == name:
                return pl
        return None

    def CheckIfEmpty(self, id):
        ini = self.Homes()
        checkdist = ini.EnumSection(id)
        for home in checkdist:
            homes = ini.GetSetting(id, home)
            if homes is not None:
                return True
            return False

    def isNoneOrEmptyOrBlankString(self, String):
        if String:
            if not String.strip():
                return True
            else:
                return False
        return False

    def On_Command(self, cmd):
        Player = cmd.User
        args = cmd.args
        command = cmd.cmd

        if command == "home":
            if len(args) == 0 or len(args) > 1:
                config = self.HomeConfig()
                homesystemname = config.GetSetting("Settings", "homesystemname")
                Player.MessageFrom(homesystemname, "---HomeSystem---")
                Player.MessageFrom(homesystemname, "/home name - Teleport to Home")
                Player.MessageFrom(homesystemname, "/sethome name - Save Home")
                Player.MessageFrom(homesystemname, "/delhome name - Delete Home")
                Player.MessageFrom(homesystemname, "/setdefaulthome name - Default Spawn Point")
                Player.MessageFrom(homesystemname, "/homes - List Homes")
                Player.MessageFrom(homesystemname, "/addfriendh name - Adds Player To Distance Whitelist")
                Player.MessageFrom(homesystemname, "/delfriendh name - Removes Player From Distance Whitelist")
                Player.MessageFrom(homesystemname, "/listwlh - List Players On Distance Whitelist")
                return
            elif len(args) > 0:
                config = self.HomeConfig()
                homesystemname = config.GetSetting("Settings", "homesystemname")
                home = str(args[0])
                check = self.HomeOf(Player, home)
                id = Player.SteamID
                loc = Player.Location
                if check is None:
                    Player.MessageFrom(homesystemname, "You don't have a home called: " + home)
                else:
                    cooldown = int(config.GetSetting("Settings", "Cooldown"))
                    if DataStore.Get("home_cooldown", id) is None:
                        DataStore.Add("home_cooldown", id, 7)
                    time = DataStore.Get("home_cooldown", id)
                    tpdelay = int(config.GetSetting("Settings", "tpdelay"))
                    systick = System.Environment.TickCount
                    if (systick - time) < 0 or math.isnan(systick - time) or math.isnan(time):
                        DataStore.Add("home_cooldown", id, 7)

                    calc = systick - time

                    if calc >= cooldown or calc == 0:
                        if tpdelay == 0:
                            DataStore.Add("homesystemautoban", id, "using")
                            Player.GroundTeleport(float(check[0]), float(check[1]) + 5.5, float(check[2]))
                            DataStore.Add("home_cooldown", id, System.Environment.TickCount)
                            Player.MessageFrom(homesystemname, "Teleported to home!")
                        else:
                            DataStore.Add("home_cooldown", id, System.Environment.TickCount)
                            HomeSystem = Plugin.CreateDict()
                            HomeSystem["Player"] = Player.SteamID
                            HomeSystem["LocationX"] = str(Player.X)
                            HomeSystem["LocationZ"] = str(Player.Z)
                            HomeSystem["HomeLocation"] = check
                            Plugin.CreateParallelTimer("HomeDelay", tpdelay * 1000, HomeSystem).Start()
                            Player.MessageFrom(homesystemname, "Teleporting you to home in: " + str(tpdelay) + " seconds")
                    else:
                        Player.MessageFrom(homesystemname, "You have to wait before teleporting again!")
                        done = round((calc / 1000) / 60, 2)
                        done2 = round((cooldown / 1000) / 60, 2)
                        Player.MessageFrom(homesystemname, "Time: " + str(done) + "/" + str(done2))

        elif command == "sethome":
            if args == 0 or args > 1:
                config = self.HomeConfig()
                homesystemname = config.GetSetting("Settings", "homesystemname")
                Player.MessageFrom(homesystemname, "Usage: /sethome name")
                return
            elif len(args) > 0:
                config = self.HomeConfig()
                homesystemname = config.GetSetting("Settings", "homesystemname")
                home = args[0]
                ini = self.Homes()
                id = Player.SteamID
                maxh = config.GetSetting("Settings", "Maxhomes")
                checkforit = int(config.GetSetting("Settings", "DistanceCheck"))
                #checkwall = config.GetSetting("Settings", "CheckCloseWall")
                if not self.CheckIfEmpty(id):
                    if checkforit == 1:
                        checkdist = ini.EnumSection("HomeNames")
                        counted = len(checkdist)
                        i = 0
                        maxdist = int(config.GetSetting("Settings", "Distance"))
                        if counted > 0 and checkdist:
                            for idof in checkdist:
                                i += 1
                                homes = ini.GetSetting("HomeNames", idof)
                                if homes:
                                    homes = homes.replace(",", "")
                                    check = self.HomeOfID(idof, homes)
                                    vector = Vector3(float(check[0]), float(check[1]), float(check[2]))
                                    dist = Util.GetVectorsDistance(vector, Player.Location)
                                    if dist <= maxdist and not self.FriendOf(idof, id) and idof != id:
                                        Player.MessageFrom(homesystemname, "There is a home within: " + str(maxdist) + "m!")
                                        return
                                    if i == counted:
                                        homes = ini.GetSetting("HomeNames", id)
                                        n = homes + "" + home + ","
                                        ini.AddSetting(id, home, str(Player.Location))
                                        ini.AddSetting("HomeNames", id, n.replace("undefined", ""))
                                        ini.Save()
                                        Player.MessageFrom(homesystemname, "Home Saved")
                                        return
                                else:
                                    ini.DeleteSetting("HomeNames", idof)
                                    ini.Save()
                        else:
                            homes = ini.GetSetting("HomeNames", id)
                            n = homes + "" + home + ","
                            ini.AddSetting(id, home, str(Player.Location))
                            ini.AddSetting("HomeNames", id, n.replace("undefined", ""))
                            ini.Save()
                            Player.MessageFrom(homesystemname, "Home Saved")
                            return
                    else:
                        homes = ini.GetSetting("HomeNames", id)
                        n = homes + "" + home + ","
                        ini.AddSetting(id, home, str(Player.Location))
                        ini.AddSetting("HomeNames", id, n.replace("undefined", ""))
                        ini.Save()
                        Player.MessageFrom(homesystemname, "Home Saved")
                        return
                else:
                    homel = ini.EnumSection(id)
                    count = len(homel)
                    parsed = int(count)
                    parsedd = int(maxh)
                    if parsed >= parsedd:
                        Player.MessageFrom(homesystemname, "You reached the max home limit. (" + str(maxh) + ")")
                        return
                    else:
                        if checkforit == 1:
                            checkdist = ini.EnumSection("HomeNames")
                            counted = len(checkdist)
                            i = 0
                            maxdist = int(config.GetSetting("Settings", "Distance"))
                            if counted > 0:
                                for idof in checkdist:
                                    i += 1
                                    homes = ini.GetSetting("HomeNames", idof)
                                    if homes:
                                        splitit = homes.split(',')
                                        if len(splitit) >= 2:
                                            for nn in xrange(-1, len(splitit)):
                                                nn += 1
                                                check = self.HomeOfID(idof, splitit[nn])
                                                vector = Vector3(float(check[0]), float(check[1]), float(check[2]))
                                                dist = Util.GetVectorsDistance(vector, Player.Location)
                                                if dist <= maxdist and not self.FriendOf(idof, id) and idof != id:
                                                    Player.MessageFrom(homesystemname, "There is a home within: " + str(maxdist) + "m!")
                                                    return
                                                if i == counted:
                                                    homes = ini.GetSetting("HomeNames", id)
                                                    n = homes + "" + home + ","
                                                    ini.AddSetting(id, home, str(Player.Location))
                                                    ini.AddSetting("HomeNames", id, n.replace("undefined", ""))
                                                    ini.Save()
                                                    Player.MessageFrom(homesystemname, "Home Saved")
                                                    return
                                        else:
                                            homes = homes.replace(",", "")
                                            check =self.HomeOfID(idof, homes)
                                            vector = Vector3(float(check[0]), float(check[1]), float(check[2]))
                                            dist = Util.GetVectorsDistance(vector, Player.Location)
                                            if dist <= maxdist and not self.FriendOf(idof, id) and idof != id:
                                                Player.MessageFrom(homesystemname, "There is a home within: " + str(maxdist) + "m!")
                                                return
                                            if i == counted:
                                                homes = ini.GetSetting("HomeNames", id)
                                                n = homes + "" + home + ","
                                                ini.AddSetting(id, home, str(Player.Location))
                                                ini.AddSetting("HomeNames", id, n.replace("undefined", ""))
                                                ini.Save()
                                                Player.MessageFrom(homesystemname, "Home Saved")
                                    else:
                                        ini.DeleteSetting("HomeNames", idof)
                                        ini.Save()
                            else:
                                homes = ini.GetSetting("HomeNames", id)
                                n = homes + "" + home + ","
                                ini.AddSetting(id, home, str(Player.Location))
                                ini.AddSetting("HomeNames", id, n.replace("undefined", ""))
                                ini.Save()
                                Player.MessageFrom(homesystemname, "Home Saved")
                        else:
                            homes = ini.GetSetting("HomeNames", id)
                            n = homes + "" + home + ","
                            ini.AddSetting(id, home, str(Player.Location))
                            ini.AddSetting("HomeNames", id, n.replace("undefined", ""))
                            ini.Save()
                            Player.MessageFrom(homesystemname, "Home Saved")
        elif command == "setdefaulthome":
            if len(args) > 0:
                config = self.HomeConfig()
                homesystemname = config.GetSetting("Settings", "homesystemname")
                home = args[0]
                check = self.HomeOf(Player, home)
                id = Player.SteamID
                if check is None:
                    Player.MessageFrom(homesystemname, "You don't have a home called: " + home)
                    return
                ini = self.Homes()
                ini.AddSetting("DefaultHome", id, home)
                ini.Save()
                Player.MessageFrom(homesystemname, "Default Home Set!")
            else:
                config = self.HomeConfig()
                homesystemname = config.GetSetting("Settings", "homesystemname")
                Player.MessageFrom(homesystemname, "Usage: /setdefaulthome name")

        elif command ==  "delhome":
            if len(args) == 1:
                config = self.HomeConfig()
                homesystemname = config.GetSetting("Settings", "homesystemname")
                home = args[0]
                ini = self.Homes()
                id = Player.SteamID
                check = ini.GetSetting(id, home)
                ifdfhome = ini.GetSetting("DefaultHome", id)
                if check is not None:
                    if ifdfhome is not None:
                        ini.DeleteSetting("DefaultHome", id)
                    homes = ini.GetSetting("HomeNames", id)
                    second = homes.replace(home+",", "")
                    ini.DeleteSetting(id, home)
                    if not second:
                        ini.DeleteSetting("HomeNames", id)
                    else:
                        ini.AddSetting("HomeNames", id, second)
                    ini.Save()
                    Player.MessageFrom(homesystemname, "Home: " + home + " Deleted")
                else:
                    Player.MessageFrom(homesystemname, "Home: " + home + " doesn't exists!")
            else:
                config = self.HomeConfig()
                homesystemname = config.GetSetting("Settings", "homesystemname")
                Player.MessageFrom(homesystemname, "Usage: /delhome name")

        elif command ==  "homes":
            config = self.HomeConfig()
            homesystemname = config.GetSetting("Settings", "homesystemname")
            ini = self.Homes()
            id = Player.SteamID
            if ini.GetSetting("HomeNames", id) is not None:
                homes = ini.GetSetting("HomeNames", id).split(',')
                leng = len(homes)
                for i in xrange(-1, leng):
                    i += 1
                    if i < leng:
                        if self.isNoneOrEmptyOrBlankString(homes[i]):
                            continue
                        Player.MessageFrom(homesystemname, "Homes: " + homes[i])
            else:
                Player.MessageFrom(homesystemname, "You don't have homes!")

        elif command ==  "addfriendh":
            config = self.HomeConfig()
            homesystemname = config.GetSetting("Settings", "homesystemname")
            if len(args) == 0:
                Player.MessageFrom(homesystemname, "Usage: /addfriendh playername")
                return
            elif len(args) > 0:
                playertor = self.GetPlayer(args[0])
                if playertor is not None and playertor != Player:
                    ini = self.Wl()
                    id = Player.SteamID
                    ini.AddSetting(id, playertor.SteamID, playertor.Name)
                    ini.Save()
                    Player.MessageFrom(homesystemname, "Player Whitelisted")
                else:
                    Player.MessageFrom(homesystemname, "Player doesn't exist, or you tried to add yourself!");

        elif command ==  "delfriendh":
            config = self.HomeConfig()
            homesystemname = config.GetSetting("Settings", "homesystemname")
            if len(args) == 0:
                Player.MessageFrom(homesystemname, "Usage: /delfriendh playername")
                return
            elif len(args) > 0:
                name = args[0]
                ini = self.Wl()
                id = Player.SteamID
                players = ini.EnumSection(id)
                i = 0
                counted = len(players)
                name = name.lower()
                for playerid in players:
                    i += 1
                    nameof = ini.GetSetting(id, playerid)
                    lowered = Data.ToLower(nameof)
                    if lowered == name:
                        ini.DeleteSetting(id, playerid)
                        ini.Save()
                        Player.MessageFrom(homesystemname, "Player Removed from Whitelist")
                        return
                    if i == counted:
                        Player.MessageFrom(homesystemname, "Player doesn't exist!")
                        return

        elif command == "listwlh":
            config = self.HomeConfig()
            homesystemname = config.GetSetting("Settings", "homesystemname")
            ini = self.Wl()
            id = Player.SteamID
            players = ini.EnumSection(id)
            for playerid in players:
                nameof = ini.GetSetting(id, playerid)
                Player.MessageFrom(homesystemname, "Whitelisted: " + nameof)
        elif command == "resettime":
            if Player.Admin:
                DataStore.Add("home_cooldown", Player.SteamID, 7)


    """def On_EntityDeployed(Player, Entity):
        config = self.HomeConfig()
        antihack = config.GetSetting("Settings", "Antihack")
        homesystemname = config.GetSetting("Settings", "homesystemname")
        if Entity is not None:
            if antihack == "1":
                inventory = Player.Inventory
                if Entity.Name == "SleepingBagA":
                    Player.MessageFrom(homesystemname, "Sleeping bags are banned from this server!")
                    Player.MessageFrom(homesystemname, "Use /home")
                    Player.MessageFrom(homesystemname, "We disabled Beds, so players can't hack in your house!")
                    Player.MessageFrom(homesystemname, "You received 15 Cloth.")
                    Entity.Destroy()
                    inventory.AddItem("Cloth", 15)
                if Entity.Name == "SingleBed":
                    Player.MessageFrom(homesystemname, "Beds are banned from this server!")
                    Player.MessageFrom(homesystemname, "Use /home")
                    Player.MessageFrom(homesystemname, "We disabled Beds, so players can't hack in your house!")
                    Player.MessageFrom(homesystemname, "You received 40 Cloth and 100 Metal Fragments.")
                    Entity.Destroy()
                    inventory.AddItem("Cloth", 40)
                    inventory.AddItem("Metal Fragments", 100)"""