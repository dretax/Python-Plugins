__author__ = 'DreTaX'
__version__ = '1.4.2'

import clr
clr.AddReferenceByPartialName("Pluton")
clr.AddReferenceByPartialName("UnityEngine")
clr.AddReferenceByPartialName("Assembly-CSharp")
import Pluton
import UnityEngine
from UnityEngine import Vector3
import math
import System
import BasePlayer
from System import *
import re


"""
    Class
"""
class HomeSystem:

    def On_PluginInit(self):
        DataStore.Flush("home_cooldown")
        DataStore.Flush("HomeHit")
        Commands.Register("home")\
            .setCallback("home")\
            .setDescription("Home help options")\
            .setUsage("/home")
        Commands.Register("sethome")\
            .setCallback("sethome")\
            .setDescription("Set your home with name provided.")\
            .setUsage("/sethome homename")
        Commands.Register("setdefaulthome")\
            .setCallback("setdefaulthome")\
            .setDescription("Sets your default home")\
            .setUsage("/setdefaulthome name")
        Commands.Register("delhome")\
            .setCallback("delhome")\
            .setDescription("Deletes a home you created")\
            .setUsage("/delhome homename")
        Commands.Register("homes")\
            .setCallback("homes")\
            .setDescription("Lists all your homes")\
            .setUsage("/homes")
        Commands.Register("addfriendh")\
            .setCallback("addfriendh")\
            .setDescription("Adds a friend who can set home on your foundation")\
            .setUsage("/addfriendh playername")
        Commands.Register("delfriendh")\
            .setCallback("delfriendh")\
            .setDescription("Delete a friend from your home")\
            .setUsage("/delfriendh playername")
        Commands.Register("listwlh")\
            .setCallback("listwlh")\
            .setDescription("Shows who is whitelisted")\
            .setUsage("/listwlh")
        Commands.Register("resettime")\
            .setCallback("resettime")\
            .setDescription("Resets a players home cooldown")\
            .setUsage("/resettime playername")

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
        PLX = re.sub('[)\(\[\'\]\,]', '', str(PLX))
        PLZ = HomeSystem["LocationZ"]
        PLZ = re.sub('[)\(\[\'\]\,]', '', str(PLZ))
        HLoc = HomeSystem["HomeLocation"]
        #HLoc = re.sub('[)\(\[\'\]\,]', '', str(HLoc)) old
        HLoc = re.sub('[)\(\[\'\]]', '', str(HLoc))
        HLoc = HLoc.split(',')
        movec = int(config.GetSetting("Settings", "movecheck"))
        if movec == 1:
            if int(float(PLX)) != int(float(Player.X)) or int(float(PLZ)) != int(float(Player.Z)):
                Player.MessageFrom(homesystemname, "You moved before teleporting!")
                return
        if not self.IsFloat(HLoc[0]) or not self.IsFloat(HLoc[1]) or not self.IsFloat(HLoc[2]):
            Plugin.Log("HomeSystemError", "Something is wrong at: " + str(HLoc) + " | " + Player.Name
                       + " | " + Player.SteamID)
            Player.MessageFrom("HomeSystem", "Something is wrong at: " + str(HLoc) + " | " + Player.Name
                               + " | " + Player.SteamID)
            Player.MessageFrom("HomeSystem", "Teleportation cancelled, please tell the admin's to check HomeSystem's directory for logs.")
            DataStore.Add("home_cooldown", Player.SteamID, 7)
            return
        loc = Vector3(float(HLoc[0]),float(HLoc[1]) + 5.5, float(HLoc[2]))
        Player.Teleport(loc)
        #if safetp > 0:
            #Plugin.CreateParallelTimer("HomeSafeTy", safetp * 1000, HomeSystem).Start()
        Player.MessageFrom(homesystemname, "Teleported to Home!")


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
        if not self.IsFloat(HLoc[0]) or not self.IsFloat(HLoc[1]) or not self.IsFloat(HLoc[2]):
            Plugin.Log("HomeSystemError", "Something is wrong at: " + str(HLoc) + " | " + Player.Name
                       + " | " + Player.SteamID)
            Player.MessageFrom("HomeSystem", "Something is wrong at: " + str(HLoc) + " | " + Player.Name
                               + " | " + Player.SteamID)
            Player.MessageFrom("HomeSystem",
                               "Teleportation cancelled, please tell the admin's to check HomeSystem's directory for logs.")
            DataStore.Add("home_cooldown", Player.SteamID, 7)
            return
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
        if check:
            return True
        return False

    def DefaultLoc(self):
        if not Plugin.IniExists("DefaultLoc"):
            loc = Plugin.CreateIni("DefaultLoc")
            loc.Save()
        return Plugin.GetIni("DefaultLoc")

    def HomeOf(self, Player, Home):
        ini = self.Homes()
        if ini.ContainsSetting(Player.SteamID, Home):
            check = ini.GetSetting(Player.SteamID, Home)
            c = check.replace("(", "")
            c = c.replace(")", "")
            return c.split(",")
        return None

    def HomeOfID(self, id, Home):
        ini = self.Homes()
        if ini.ContainsSetting(id, Home):
            check = ini.GetSetting(id, Home)
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
            if homes:
                return True
            return False

    def IsFloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def CutName(self, string):
        name = re.sub(r'[^\x00-\x7F]+', '', string)
        return name

    def Check(self, Player, plloc):
        config = self.HomeConfig()
        homesystemname = config.GetSetting("Settings", "homesystemname")
        ini = self.Homes()
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
                    if not self.IsFloat(check[0]) or not self.IsFloat(check[1]) or not self.IsFloat(check[2]):
                        Plugin.Log("HomeSystemError", "Something is wrong at: " + str(check) + " | " + str(homes))
                        continue
                    vector = Vector3(float(check[0]), float(check[1]), float(check[2]))
                    dist = Util.GetVectorsDistance(vector, plloc)
                    if dist <= maxdist and not self.FriendOf(idof, id) and idof != id:
                        Player.MessageFrom(homesystemname, "There is a home within: " + str(maxdist) + "m!")
                        return True
                    if i == counted:
                        return False
        return False

    def SaveHome(self, Player, home, loc):
        id = Player.SteamID
        ini = self.Homes()
        config = self.HomeConfig()
        homesystemname = config.GetSetting("Settings", "homesystemname")
        homes = ini.GetSetting("HomeNames", id)
        if homes is not None and "," in homes:
            n = homes + "" + home + ","
            ini.AddSetting(id, home, str(loc))
            ini.AddSetting("HomeNames", id, n)
            ini.Save()
            Player.MessageFrom(homesystemname, "Home Saved")
            return
        n = home + ","
        ini.AddSetting(id, home, str(loc))
        ini.AddSetting("HomeNames", id, n)
        ini.Save()
        Player.MessageFrom(homesystemname, "Home Saved")

    def On_CombatEntityHurt(self, EntityHurtEvent):
        if EntityHurtEvent.Attacker.ToPlayer() is None:
            return
        attacker = EntityHurtEvent.Attacker.ToPlayer()
        if DataStore.ContainsKey("HomeHit", attacker.SteamID):
            if "foundation" in EntityHurtEvent.Victim.Name:
                loc = Vector3(EntityHurtEvent.Victim.X, EntityHurtEvent.Victim.Y + 4, EntityHurtEvent.Victim.Z)
                self.SaveHome(attacker, DataStore.Get("HomeHit", attacker.SteamID), loc)
            else:
                attacker.Message("Hit a foundation.")

    def home(self, args, Player):
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
            if check is None:
                Player.MessageFrom(homesystemname, "You don't have a home called: " + home)
            else:
                cooldown = int(config.GetSetting("Settings", "Cooldown"))
                if DataStore.Get("home_cooldown", id) is None:
                    DataStore.Add("home_cooldown", id, 7)
                time = DataStore.Get("home_cooldown", id)
                tpdelay = int(config.GetSetting("Settings", "tpdelay"))
                systick = System.Environment.TickCount
                if int(systick - int(time)) < 0 or math.isnan(int(systick - int(time))) or math.isnan(time):
                    DataStore.Add("home_cooldown", id, 7)

                calc = systick - int(time)

                if calc >= cooldown or time == 7:
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

    def sethome(self, args, Player):
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
            plloc = Player.Location
            maxh = int(config.GetSetting("Settings", "Maxhomes"))
            foundation = int(config.GetSetting("Settings", "Foundation"))
            Util.Log(str(ini.EnumSection(id)))
            homel = ini.EnumSection(id)
            count = len(homel)
            if count >= maxh:
                Player.MessageFrom(homesystemname, "You reached the max home limit. (" + str(maxh) + ")")
                return
            checkforit = int(config.GetSetting("Settings", "DistanceCheck"))
            home = self.CutName(home)
            if len(home) == 0:
                Player.MessageFrom(homesystemname, "You need to use English Characters for home!")
                return
            a = re.match('^[a-zA-Z0-9]+$', home)
            if not a:
                Player.MessageFrom(homesystemname, "You need to use English Characters for home!")
                return
            check = self.HomeOf(Player, home)
            if check is not None:
                Player.MessageFrom(homesystemname, "You already have a home called like that!")
                return
            if foundation == 0:
                if checkforit == 1:
                    s = self.Check(Player, plloc)
                    if not s:
                        return
                self.SaveHome(Player, home, plloc)
            else:
                DataStore.Add("HomeHit", id, home)
                Player.MessageFrom(homesystemname, "Hit a foundation/ceiling to save your home!")

    def setdefaulthome(self, args, Player):
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

    def delhome(self, args, Player):
        if len(args) == 1:
            config = self.HomeConfig()
            homesystemname = config.GetSetting("Settings", "homesystemname")
            home = args[0]
            ini = self.Homes()
            id = Player.SteamID
            check = ini.GetSetting(id, home)
            ifdfhome = ini.GetSetting("DefaultHome", id)
            if check:
                if ifdfhome:
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

    def homes(self, args, Player):
        config = self.HomeConfig()
        homesystemname = config.GetSetting("Settings", "homesystemname")
        ini = self.Homes()
        id = Player.SteamID
        if ini.GetSetting("HomeNames", id):
            homes = ini.GetSetting("HomeNames", id)
            homes = homes[:-1]
            homes = homes.split(',')
            for h in homes:
                Player.MessageFrom(homesystemname, "Homes: " + h)
        else:
            Player.MessageFrom(homesystemname, "You don't have homes!")

    def addfriendh(self, args, Player):
        config = self.HomeConfig()
        homesystemname = config.GetSetting("Settings", "homesystemname")
        if len(args) == 0:
            Player.MessageFrom(homesystemname, "Usage: /addfriendh playername")
            return
        elif len(args) > 0:
            playertor = self.GetPlayer(args[0])
            if playertor and playertor != Player:
                ini = self.Wl()
                id = Player.SteamID
                ini.AddSetting(id, playertor.SteamID, playertor.Name)
                ini.Save()
                Player.MessageFrom(homesystemname, "Player Whitelisted")
            else:
                Player.MessageFrom(homesystemname, "Player doesn't exist, or you tried to add yourself!")

    def delfriendh(self, args, Player):
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
                lowered = ini.GetSetting(id, playerid).lower()
                if lowered == name:
                    ini.DeleteSetting(id, playerid)
                    ini.Save()
                    Player.MessageFrom(homesystemname, "Player Removed from Whitelist")
                    return
                if i == counted:
                    Player.MessageFrom(homesystemname, "Player doesn't exist!")
                    return

    def listwlh(self, args, Player):
        config = self.HomeConfig()
        homesystemname = config.GetSetting("Settings", "homesystemname")
        ini = self.Wl()
        id = Player.SteamID
        players = ini.EnumSection(id)
        for playerid in players:
            nameof = ini.GetSetting(id, playerid)
            Player.MessageFrom(homesystemname, "Whitelisted: " + nameof)

    def resettime(self, args, Player):
        if Player.Admin:
            DataStore.Add("home_cooldown", Player.SteamID, 7)
            Player.Message("Time Reset!")
