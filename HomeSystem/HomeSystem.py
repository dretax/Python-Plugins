__author__ = 'DreTaX'
__version__ = '2.5.0'
import clr
clr.AddReferenceByPartialName("Fougerite")

import Fougerite
import re
import sys
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

    def addJob(self, id, xtime, location, callbacknumber, PlayerLoc):
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
            id = long(d)
            for player in Server.Players:
                if long(player.SteamID) == id:
                    return player
            return None
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
                        checkn = config.GetSetting("Settings", "safetpcheck")
                        tpdelay = config.GetSetting("Settings", "jointpdelay")
                        if getdfhome is not None:
                            home = self.HomeOf(player, getdfhome)
                            j = []
                            j.append(str(params[0]))
                            j.append(str(home[0]))
                            j.append(str(home[1]))
                            j.append(str(home[2]))
                            #todo: Continue
                    DataStore.Add("homesystemautoban", params[0], "none")