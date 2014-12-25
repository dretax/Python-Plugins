import math

__author__ = 'DreTaX'
__version__ = '2.5.0'
import clr
clr.AddReferenceByPartialName("Fougerite")

import Fougerite
import re
import sys
import System
from System import Environment
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

try:
    import random
    import ast
except ImportError:
    pass

DStable = 'BZjobs'
class HomeSystem:

    """
        Functions
    """

    def Replace(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(',')

    def HomeConfig(self):
        if not Plugin.IniExists("HomeConfig"):
            homes = Plugin.CreateIni("HomeConfig")
            homes.Save()
        return Plugin.GetIni("HomeConfig")

    def Homes(self):
        if not Plugin.IniExists("Homes"):
            homes = Plugin.CreateIni("Homes")
            homes.Save()
        return Plugin.GetIni("Homes")

    def FriendOf(self, id, selfid):
        ini = self.Wl()
        check = ini.GetSetting(id, selfid)
        if check is not None:
            return True
        return False

    def Wl(self):
        if not Plugin.IniExists("WhiteListedPlayers"):
            homes = Plugin.CreateIni("WhiteListedPlayers")
            homes.Save()
        return Plugin.GetIni("WhiteListedPlayers")

    def DefaultLoc(self):
        if not Plugin.IniExists("DefaultLoc"):
            loc = Plugin.CreateIni("DefaultLoc")
            loc.Save()
        return Plugin.GetIni("DefaultLoc")

    def HomeOf(self, Player, Home):
        ini = self.Homes()
        check = ini.GetSetting(Player.SteamID, Home)
        if check is not None:
            c = self.Replace(check)
            return c
        return None

    def HomeOfID(self, id, Home):
        ini = self.Homes()
        check = ini.GetSetting(id, Home)
        if check is not None:
            c = self.Replace(check)
            return c
        return None

    def HasHome(self, id):
        ini = self.Homes()
        enum = ini.EnumSection(id)
        if len(enum) == 0 or enum is None:
            return False
        return True

    def GetHomeNumber(self, id):
        ini = self.Homes()
        enum = len(ini.EnumSection(id))
        return enum

    def GetListofHomes(self, id):
        ini = self.Homes()
        homes = ini.GetSetting("HomeNames", id)
        homes = homes.replace(' ')
        return homes.split(',')

    def CheckIfEmpty(self, id):
        ini = self.Homes()
        checkdist = ini.EnumSection(id)
        for home in checkdist:
            homes = ini.GetSetting(id, home)
            if homes and homes is not None:
                return True
        return False

    def DonatorRankCheck(self, id):
        if DataStore.Get("MaxHomes", id) is not None:
            maxh = DataStore.Get("MaxHomes", id)
            return maxh
        else:
            if DataStore.Get("DonatorRank", "PlayerHomesMax") is not None:
                maxh = DataStore.Get("DonatorRank", "PlayerHomesMax")
                return maxh
            else:
                config = self.HomeConfig()
                maxh = config.GetSetting("Settings", "Maxhomes")
                return maxh

    # exec, location, callback
    def Stringify(self, List):
        return str(List).strip('[]')

    def Parse(self, String):
        x = ast.literal_eval(String)
        x = [n.strip() for n in x]
        return x

    """
        Timer Functions
    """

    def addJob(self, id, xtime, location, callbacknumber, PlayerLoc = None):
        if id and xtime and location and callbacknumber:
            epoch = Plugin.GetTimestamp()
            exectime = int(epoch) + int(xtime)
            # ID, EXECTIME : Location : CallBack number  : Player's Last Location | Requires to be splited
            List = []
            List.append(str(exectime))
            List.append(str(location))
            List.append(str(callbacknumber))
            List.append(str(PlayerLoc))
            DataStore.Add(DStable, id, self.Stringify(List))
            self.startTimer()

    def killJob(self, id):
        DataStore.Remove(DStable, id)

    def startTimer(self):
        config = self.HomeConfig()
        gfjfhg = int(config.GetSetting("Settings", "run_timer")) * 1000
        try:
            if not Plugin.GetTimer("JobTimer"):
                Plugin.CreateTimer("JobTimer", gfjfhg).Start()
        except:
            pass

    def stopTimer(self):
        Plugin.KillTimer("JobTimer")

    def getPlayer(self, d):
        try:
            id = str(d)
            pl = Server.FindPlayer(id)
            return pl
        except:
            return None

    def clearTimers(self):
        DataStore.Flush(DStable)

    HomeJobs = {'name': 'HomeSystem', 'Author': 'DreTaX', 'Version': '2.0'}


    """
        Events
    """

    def On_PluginInit(self):
        DataStore.Flush("BZjobs")
        Util.ConsoleLog(self.HomeJobs['name'] + " v" + self.HomeJobs['version'] + " by " + self.HomeJobs['author'] + " loaded.", True)


    def JobTimerCallback(self):
        epoch = Plugin.GetTimestamp()
        if DataStore.Count(DStable) >= 1:
            pending = DataStore.Keys(DStable)
            config = self.HomeConfig()
            homesystemname = config.GetSetting("Settings", "homesystemname")
            for id in pending:
                if DataStore.Get(DStable, id) is None:
                    DataStore.Remove(DStable, id)
                    continue
                params = self.Parse(str(DataStore.Get(DStable, id)))
                if epoch >= int(params[0]):
                    callback = int(params[2])
                    xto = self.Replace(params[1])
                    player = self.getPlayer(id)
                    if player is None:
                        DataStore.Add("homesystemautoban", id, "none")
                        self.killJob(id)
                        continue
                    loc = Util.CreateVector(float(xto[0]), float(xto[1]), float(xto[2]))
                    DataStore.Add("homesystemautoban", id, "using")
                    # Join Callback, this should handle the delay
                    if callback == 1:
                        player.SafeTeleportTo(loc)
                        #BZHJ.addJob('jointp', checkn, jobxData.params);
                    # Home Teleport Callback
                    elif callback == 2:
                        movec = int(config.GetSetting("Settings", "movecheck"))
                        if movec == 1:
                            before = self.Replace(params[3])
                            before = Util.CreateVector(float(before[0]), float(before[1]), float(before[2]))
                            if before != player.Location:
                                player.Notice("You were moving!")
                                DataStore.Add("home_cooldown", id, 7)
                                self.killJob(id)
                            else:
                                player.SafeTeleportTo(loc)
                                player.Notice("You have been teleported home.")
                                #BZHJ.addJob('mytestt', checkn, jobxData.params);
                        else:
                            player.SafeTeleportTo(loc)
                            player.Notice("You have been teleported home.")
                            #BZHJ.addJob('mytestt', checkn, jobxData.params);
                    # Random Teleportation Delay
                    elif callback == 3:
                        player.SafeTeleportTo(loc)
                        player.MessageFrom(homesystemname, "You have been teleported to a random location!")
                        player.MessageFrom(homesystemname, "Type /setdefaulthome HOMENAME")
                        player.MessageFrom(homesystemname, "To spawn at your home!")
                        #BZHJ.addJob('randomtp', checkn, jobxData.params);
                    # Spawn Delay (Camp Used)
                    elif callback == 4:
                        player.SafeTeleportTo(loc)
                        player.MessageFrom(homesystemname, "You have been teleported to your home")
                    # Handles those players who joined after X seconds. Dizzy hack bypasser.
                    elif callback == 5:
                        randomloc = int(config.GetSetting("Settings", "randomlocnumber"))
                        DataStore.Add("home_joincooldown", id, 7)
                        r = random.randrange(0, randomloc)
                        ini = self.Homes()
                        getdfhome = ini.GetSetting("DefaultHome", )
                        tpdelay = int(config.GetSetting("Settings", "jointpdelay"))
                        if getdfhome is not None:
                            home = self.HomeOf(player, getdfhome)
                            home = Util.CreateVector(float(home[0]), float(home[1]), float(home[2]))
                            # ID, EXECTIME : Location : CallBack number  : Player's Last Location | Requires to be splited
                            self.addJob(id, tpdelay, home, 1)
                        else:
                            ini2 = self.DefaultLoc()
                            loc = ini2.GetSetting("DefaultLoc", str(r))
                            tp = self.Replace(loc)
                            home = Util.CreateVector(float(tp[0]), float(tp[1]), float(tp[2]))
                            self.addJob(id, tpdelay, home, 3)
                    DataStore.Add("homesystemautoban", id, "none")
                    DataStore.Remove(DStable, id)

    def On_Command(self, Player, cmd, args):
        config = self.HomeConfig()
        homesystemname = config.GetSetting("Settings", "homesystemname")
        id = Player.SteamID
        plloc = Player.Location
        if cmd == "cleartimers":
            if Player.Admin:
                self.clearTimers()
                Player.MessageFrom(homesystemname, "All timers killed.")
        elif cmd == "home":
            if len(args) != 1:
                Player.MessageFrom(homesystemname, "---HomeSystem---")
                Player.MessageFrom(homesystemname, "/home name - Teleport to Home")
                Player.MessageFrom(homesystemname, "/sethome name - Save Home")
                Player.MessageFrom(homesystemname, "/delhome name - Delete Home")
                Player.MessageFrom(homesystemname, "/setdefaulthome name - Default Spawn Point")
                Player.MessageFrom(homesystemname, "/homes - List Homes")
                Player.MessageFrom(homesystemname, "/addfriendh name - Adds Player To Distance Whitelist")
                Player.MessageFrom(homesystemname, "/delfriendh name - Removes Player From Distance Whitelist")
                Player.MessageFrom(homesystemname, "/listwlh - List Players On Distance Whitelist")
            else:
                home = str(args[0])
                check = self.HomeOf(Player, home)
                if check is None:
                    Player.MessageFrom(homesystemname, "You don't have a home called: " + home)
                    return
                cooldown = int(config.GetSetting("Settings", "Cooldown"))
                time = DataStore.Get("home_cooldown", id)
                tpdelay = int(config.GetSetting("Settings", "tpdelay"))
                calc = System.Environment.TickCount - time
                if time is None or calc < 0 or math.isnan(calc) or math.isnan(time):
                    DataStore.Add("home_cooldown", id, 7)
                    time = 7
                if calc >= cooldown or time == 7:
                    loc = Util.CreateVector(check[0], check[1], check[2])
                    if tpdelay == 0:
                        Player.SafeTeleportTo(loc)
                        DataStore.Add("home_cooldown", id, System.Environment.TickCount)
                        Player.MessageFrom(homesystemname, "Teleported to home!")
                    else:
                        DataStore.Add("home_cooldown", id, System.Environment.TickCount)
                        self.addJob(id, tpdelay, loc, 2, plloc)
                        Player.MessageFrom(homesystemname, "Teleporting you to home in: " + str(tpdelay) + " seconds")
                else:
                    Player.Notice("You have to wait before teleporting again!")
                    done = round((calc / 1000) / 60, 2)
                    done2 = round((cooldown / 1000) / 60, 2)
                    Player.MessageFrom(homesystemname, "Time: " + str(done) + "/" + str(done2))
        elif cmd == "sethome":
            if len(args) != 1:
                Player.MessageFrom(homesystemname, "Usage: /sethome name")
                return
            ini = self.Homes()
            maxh = self.DonatorRankCheck(id)
            if self.GetHomeNumber(id) == int(maxh):
                Player.MessageFrom(homesystemname, "You reached the max number of homes!")
                return
            home = str(args[0])
            check = self.HomeOf(Player, home)
            if check is not None:
                Player.MessageFrom(homesystemname, "You already have a home called like that!")
                return
            checkforit = int(config.GetSetting("Settings", "DistanceCheck"))
            checkwall = int(config.GetSetting("Settings", "CheckCloseWall"))
            if checkforit == 1:
                checkdist = ini.EnumSection("HomeNames")
                counted = len(checkdist)
                maxdist = int(config.GetSetting("Settings", "Distance"))
                if counted > 0:
                    for idof in checkdist:
                        homes = self.GetListofHomes(idof)
                        for i in xrange(0, len(homes)):
                            check = self.HomeOfID(idof, homes[i])
                            if check is not None and check:
                                vector = Util.CreateVector(float(check[0]), float(check[1]), float(check[2]))
                                dist = Util.GetVectorsDistance(vector, plloc)
                                if dist <= maxdist and not self.FriendOf(idof, id) and long(idof) != long(id):
                                    Player.MessageFrom(homesystemname, "There is a home within: " + str(maxdist) + "m!")
                                    return
                            else:
                                ini.DeleteSetting("HomeNames", idof)
                                ini.Save()
                else:
                    homes = ini.GetSetting("HomeNames", id)
                    n = homes + "" + home + ","
                    ini.AddSetting(id, home, str(plloc))
                    ini.AddSetting("HomeNames", id, n.replace("undefined", ""))
                    ini.Save()
                    Player.MessageFrom(homesystemname, "Home Saved")
                    return
            if checkwall == 1:
                type = Util.TryFindReturnType("StructureComponent")
                objects = UnityEngine.Resources.FindObjectsOfTypeAll(type)
                for x in objects:
                    if "Wall" in x.name:
                        distance = round(Util.GetVectorsDistance(x.gameObject.transform.position, plloc), 2)
                        if distance <= 1.50:
                            Player.MessageFrom(homesystemname, "You can't set home near walls!")
                            return
            homes = ini.GetSetting("HomeNames", id)
            n = homes + "" + home + ","
            ini.AddSetting(id, home, str(plloc))
            ini.AddSetting("HomeNames", id, n.replace("undefined", ""))
            ini.Save()
            Player.MessageFrom(homesystemname, "Home Saved")
        elif cmd == "setdefaulthome":
            if len(args) != 1:
                Player.MessageFrom(homesystemname, "Usage: /setdefaulthome name")
                return
            home = str(args[0])
            check = self.HomeOf(Player, home)
            if check is None:
                Player.MessageFrom(homesystemname, "You don't have a home called: " + home)
                return
            ini = self.Homes()
            ini.AddSetting("DefaultHome", id, home)
            ini.Save()
            Player.MessageFrom(homesystemname, "Default Home Set!")