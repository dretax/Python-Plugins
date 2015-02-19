__author__ = 'DreTaX'
__version__ = '2.5.4'
import clr
clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import Fougerite
import UnityEngine
from UnityEngine import *
import re
import sys
import System
import math
from System import *
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

try:
    import random
except ImportError:
    pass

DStable = 'BZjobs'
red = "[color #FF0000]"
class HomeSystem:

    sendhome = None
    ecooldown = None
    jointpdelay = None
    cooldown = None
    homesystemname = None

    def On_PluginInit(self):
        DataStore.Flush("BZjobs")
        DataStore.Flush("home_joincooldown")
        DataStore.Flush("homesystemautoban")
        DataStore.Flush("home_cooldown")
        DataStore.Flush("homey")
        config = self.HomeConfig()
        self.sendhome = int(config.GetSetting("Settings", "SendPlayertoHomeorRandom"))
        self.ecooldown = int(config.GetSetting("Settings", "EJoinCooldown"))
        self.jointpdelay = int(config.GetSetting("Settings", "jointpdelay"))
        self.cooldown = int(config.GetSetting("Settings", "rejoincd"))
        self.homesystemname = config.GetSetting("Settings", "homesystemname")
        Util.ConsoleLog(self.HomeJobs['Name'] + " v" + self.HomeJobs['Version'] + " by " + self.HomeJobs['Author'] + " loaded.", True)

    """
        Functions
    """

    def Replace(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(',')

    def ReplaceToDot(self, String):
        str = re.sub('[(\)]', '', String)
        return str.split(':')

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
        homes = homes.replace(' ', '')
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
    """def Stringify(self, List):
        return str(List).strip('[]')

    def Parse(self, String):
        x = ast.literal_eval(String)
        x = [n.strip() for n in x]
        return x"""

    def Stringify(self, List):
        s = re.sub("[[\]\'\ ]", '', str(List))
        return str(s)

    def Parse(self, String):
        return String.split(',')

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def isMod(self, id):
        if DataStore.ContainsKey("Moderators", id):
            return True
        return False

    def CutName(self, string):
        name = re.sub(r'[^\x00-\x7F]+', '', string)
        return name

    """
        CheckV method based on Spock's method.
        Upgraded by DreTaX
        Can Handle Single argument and Array args.
        V4.1
    """

    def GetPlayerName(self, namee):
        try:
            name = namee.lower()
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
            Player.MessageFrom(self.homesystemname, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(self.homesystemname, "Found [color#FF0000]" + str(count) + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    """
        Timer Functions
    """

    def addJob(self, id, xtime, location, callbacknumber, PlayerLoc = None):
        epoch = Plugin.GetTimestamp()
        exectime = int(epoch) + int(xtime)
        # ID, EXECTIME : Location : CallBack number  : Player's Last Location | Requires to be splited
        List = []
        List.append(str(exectime))
        List.append(str(location).replace(",", ":"))
        List.append(str(callbacknumber))
        List.append(str(PlayerLoc).replace(",", ":"))
        DataStore.Add(DStable, id, self.Stringify(List))
        self.startTimer()

    def isInjob(self, id):
        if DataStore.Get(DStable, id) is not None:
            return True
        return False

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
        self.stopTimer()

    HomeJobs = {'Name': 'HomeSystem', 'Author': 'DreTaX', 'Version': '2.5.0'}


    """
        Events
    """

    def JobTimerCallback(self):
        if DataStore.Count(DStable) >= 1:
            epoch = int(Plugin.GetTimestamp())
            pending = DataStore.Keys(DStable)
            config = self.HomeConfig()
            for id in pending:
                if DataStore.Get(DStable, id) is None:
                    DataStore.Remove(DStable, id)
                    continue
                params = self.Parse(str(DataStore.Get(DStable, id)))
                if epoch >= int(params[0]):
                    player = self.getPlayer(id)
                    if player is None:
                        DataStore.Add("homesystemautoban", id, "none")
                        self.killJob(id)
                        continue
                    callback = int(params[2])
                    self.killJob(id)
                    if callback != 6 and callback != 5 and callback != 4:
                        xto = self.ReplaceToDot(params[1])
                        loc = Util.CreateVector(float(xto[0]), float(xto[1]), float(xto[2]))
                    DataStore.Add("homesystemautoban", id, "using")
                    # Join Callback, this should handle the delay
                    if callback == 1:
                        player.SafeTeleportTo(loc)
                        player.MessageFrom(self.homesystemname, "You have been teleported to your home")
                    # Home Teleport Callback
                    elif callback == 2:
                        movec = int(config.GetSetting("Settings", "movecheck"))
                        if movec == 1:
                            before = self.ReplaceToDot(params[3])
                            before = Util.CreateVector(float(before[0]), float(before[1]), float(before[2]))
                            dist = Util.GetVectorsDistance(before, player.Location)
                            if dist > 1.0:
                                player.MessageFrom(self.homesystemname, "You were moving!")
                                DataStore.Add("home_cooldown", id, 7)
                            else:
                                player.SafeTeleportTo(loc)
                                player.MessageFrom(self.homesystemname, "You have been teleported home.")
                                DataStore.Add("homey", id, loc.y)
                                self.addJob(id, 2, None, 4)
                                #BZHJ.addJob('mytestt', checkn, jobxData.params);
                        else:
                            player.SafeTeleportTo(loc)
                            player.MessageFrom(self.homesystemname, "You have been teleported home.")
                    # Random Teleportation Delay
                    elif callback == 3:
                        player.SafeTeleportTo(loc)
                        player.MessageFrom(self.homesystemname, "You have been teleported to a random location!")
                        player.MessageFrom(self.homesystemname, "Type /setdefaulthome HOMENAME")
                        player.MessageFrom(self.homesystemname, "To spawn at your home!")
                    # dizzy heck.
                    elif callback == 4:
                        DataStore.Add("homesystemautoban", id, "none")
                        v = DataStore.Get("homey", id)
                        ini = self.DefaultLoc()
                        if v is None:
                            return
                        y = float(player.Y)
                        v = float(v)
                        if v - y > 3.0:
                            randomloc = int(config.GetSetting("Settings", "randomlocnumber"))
                            DataStore.Add("home_joincooldown", id, 7)
                            r = random.randrange(1, randomloc)
                            randomloc = ini.GetSetting("DefaultLoc", str(r))
                            tp = self.Replace(randomloc)
                            home = Util.CreateVector(float(tp[0]), float(tp[1]), float(tp[2]))
                            player.TeleportTo(home)
                            Server.BroadcastFrom(self.homesystemname, player.Name + red + " tried to fall through a house. Kicked.")
                            DataStore.Remove("homey", id)
                            self.addJob(id, 2, None, 6)
                        DataStore.Remove("homey", id)
                    # Handles those players who joined after X seconds. Dizzy hack bypasser.
                    elif callback == 5:
                        randomloc = int(config.GetSetting("Settings", "randomlocnumber"))
                        DataStore.Add("home_joincooldown", id, 7)
                        r = random.randrange(1, randomloc)
                        ini = self.Homes()
                        getdfhome = ini.GetSetting("DefaultHome", id)
                        if getdfhome is not None:
                            home = self.HomeOf(player, getdfhome)
                            home = Util.CreateVector(float(home[0]), float(home[1]), float(home[2]))
                            # ID, EXECTIME : Location : CallBack number  : Player's Last Location | Requires to be splited
                            w = 1
                        else:
                            ini2 = self.DefaultLoc()
                            locc = ini2.GetSetting("DefaultLoc", str(r))
                            tp = self.Replace(locc)
                            home = Util.CreateVector(float(tp[0]), float(tp[1]), float(tp[2]))
                            w = 3
                        self.addJob(id, 2, home, w)
                    elif callback == 6:
                        try:
                            player.Disconnect()
                        except:
                            pass
        else:
            self.clearTimers()

    def On_Command(self, Player, cmd, args):
        config = self.HomeConfig()
        id = Player.SteamID
        plloc = Player.Location
        if cmd == "cleartimers":
            if Player.Admin:
                self.clearTimers()
                Player.MessageFrom(self.homesystemname, "All timers killed.")
        elif cmd == "home":
            if len(args) != 1:
                Player.MessageFrom(self.homesystemname, "---HomeSystem---")
                Player.MessageFrom(self.homesystemname, "/home name - Teleport to Home")
                Player.MessageFrom(self.homesystemname, "/sethome name - Save Home")
                Player.MessageFrom(self.homesystemname, "/delhome name - Delete Home")
                Player.MessageFrom(self.homesystemname, "/setdefaulthome name - Default Spawn Point")
                Player.MessageFrom(self.homesystemname, "/homes - List Homes")
                Player.MessageFrom(self.homesystemname, "/addfriendh name - Adds Player To Distance Whitelist")
                Player.MessageFrom(self.homesystemname, "/delfriendh name - Removes Player From Distance Whitelist")
                Player.MessageFrom(self.homesystemname, "/listwlh - List Players On Distance Whitelist")
            else:
                home = str(args[0])
                check = self.HomeOf(Player, home)
                if check is None:
                    Player.MessageFrom(self.homesystemname, "You don't have a home called: " + home)
                    return
                cooldown = int(config.GetSetting("Settings", "Cooldown"))
                time = DataStore.Get("home_cooldown", id)
                if time is None:
                    DataStore.Add("home_cooldown", id, 7)
                    time = 7
                tpdelay = int(config.GetSetting("Settings", "tpdelay"))
                calc = System.Environment.TickCount - time
                if calc < 0 or math.isnan(calc) or math.isnan(time):
                    DataStore.Add("home_cooldown", id, 7)
                    time = 7
                if calc >= cooldown or time == 7:
                    loc = Util.CreateVector(float(check[0]), float(check[1]), float(check[2]))
                    if tpdelay == 0:
                        Player.SafeTeleportTo(loc)
                        DataStore.Add("home_cooldown", id, System.Environment.TickCount)
                        Player.MessageFrom(self.homesystemname, "Teleported to home!")
                    else:
                        DataStore.Add("home_cooldown", id, System.Environment.TickCount)
                        self.addJob(id, tpdelay, loc, 2, plloc)
                        Player.MessageFrom(self.homesystemname, "Teleporting you to home in: " + str(tpdelay) + " seconds")
                        movec = int(config.GetSetting("Settings", "movecheck"))
                        dmg = int(config.GetSetting("Settings", "checkdamage"))
                        if movec == 1:
                            Player.MessageFrom(self.homesystemname, "You can't move while teleporting.")
                        if dmg == 1:
                            Player.MessageFrom(self.homesystemname, "You can't take damage while teleporting.")

                else:
                    Player.Notice("You have to wait before teleporting again!")
                    done = round((calc / 1000) / 60, 2)
                    done2 = round((cooldown / 1000) / 60, 2)
                    Player.MessageFrom(self.homesystemname, "Time: " + str(done) + "/" + str(done2))
        elif cmd == "sethome":
            if len(args) != 1:
                Player.MessageFrom(self.homesystemname, "Usage: /sethome name")
                return
            ini = self.Homes()
            maxh = self.DonatorRankCheck(id)
            if self.GetHomeNumber(id) == int(maxh):
                Player.MessageFrom(self.homesystemname, "You reached the max number of homes!")
                return
            home = str(args[0])
            home = self.CutName(home)
            if len(home) == 0:
                Player.MessageFrom(self.homesystemname, "You need to use English Characters for home!")
                return
            a = re.match('^[a-zA-Z0-9]+$', home)
            if not a:
                Player.MessageFrom(self.homesystemname, "You need to use English Characters for home!")
                return
            check = self.HomeOf(Player, home)
            if check is not None:
                Player.MessageFrom(self.homesystemname, "You already have a home called like that!")
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
                            if check is not None:
                                vector = Util.CreateVector(float(check[0]), float(check[1]), float(check[2]))
                                dist = Util.GetVectorsDistance(vector, plloc)
                                if dist <= maxdist and not self.FriendOf(idof, id) and long(idof) != long(id):
                                    Player.MessageFrom(self.homesystemname, "There is a home within: " + str(maxdist) + "m!")
                                    return
                            #Note: I removed the home here if it was null
            if checkwall == 1:
                type = Util.TryFindReturnType("StructureComponent")
                objects = UnityEngine.Object.FindObjectsOfType(type)
                for x in objects:
                    if "Wall" in x.name:
                        distance = round(Util.GetVectorsDistance(x.gameObject.transform.position, plloc), 2)
                        if distance <= 1.50:
                            Player.MessageFrom(self.homesystemname, "You can't set home near walls!")
                            return
            homes = ini.GetSetting("HomeNames", id)
            if homes is not None and "," in homes:
                n = homes + "" + home + ","
                ini.AddSetting(id, home, str(plloc))
                ini.AddSetting("HomeNames", id, n)
                ini.Save()
                Player.MessageFrom(self.homesystemname, "Home Saved")
                return
            n = home + ","
            ini.AddSetting(id, home, str(plloc))
            ini.AddSetting("HomeNames", id, n)
            ini.Save()
            Player.MessageFrom(self.homesystemname, "Home Saved")
        elif cmd == "setdefaulthome":
            if len(args) != 1:
                Player.MessageFrom(self.homesystemname, "Usage: /setdefaulthome name")
                return
            home = str(args[0])
            check = self.HomeOf(Player, home)
            if check is None:
                Player.MessageFrom(self.homesystemname, "You don't have a home called: " + home)
                return
            ini = self.Homes()
            ini.AddSetting("DefaultHome", id, home)
            ini.Save()
            Player.MessageFrom(self.homesystemname, "Default Home Set!")
        elif cmd == "delhome":
            if len(args) != 1:
                Player.MessageFrom(self.homesystemname, "Usage: /delhome name")
                return
            home = str(args[0])
            ini = self.Homes()
            check = ini.GetSetting(id, home)
            ifdfhome = ini.GetSetting("DefaultHome", id)
            if check is not None:
                if ifdfhome is not None and ifdfhome == home:
                    ini.DeleteSetting("DefaultHome", id)
                homes = ini.GetSetting("HomeNames", id)
                second = homes.replace(home + ",", "")
                ini.DeleteSetting(id, home)
                if not second:
                    ini.DeleteSetting("HomeNames", id)
                else:
                    ini.AddSetting("HomeNames", id, second)
                ini.Save()
                Player.MessageFrom(self.homesystemname, "Home: " + home + " Deleted")
            else:
                Player.MessageFrom(self.homesystemname, "Home: " + home + " doesn't exists!")
        elif cmd == "homes":
            ini = self.Homes()
            if ini.GetSetting("HomeNames", id) is not None:
                homes = str(ini.GetSetting("HomeNames", id))
                homes = homes[:-1]
                homes = homes.split(',')
                Player.MessageFrom(self.homesystemname, "--List of your Homes--")
                for h in homes:
                    Player.MessageFrom(self.homesystemname, "- " + str(h))
            else:
                Player.MessageFrom(self.homesystemname, "You don't have homes!")
        elif cmd == "deletebeds":
            if Player.Admin:
                for x in World.Entities:
                    if x.Name == "SleepingBagA" or x.Name == "SingleBed":
                        x.Destroy()
                Player.MessageFrom(self.homesystemname, "Deleted all.")
        elif cmd == "addfriendh":
            if len(args) == 0:
                Player.MessageFrom(self.homesystemname, "Usage: /addfriendh playername")
                return
            playerr = self.CheckV(Player, args[0])
            if playerr is None:
                return
            if playerr == Player:
                Player.MessageFrom(self.homesystemname, "This is you....")
                return
            ini = self.Wl()
            ini.AddSetting(id, playerr.SteamID, playerr.Name)
            ini.Save()
            Player.MessageFrom(self.homesystemname, "Player Whitelisted")
        elif cmd == "delfriendh":
            if len(args) == 0:
                Player.MessageFrom(self.homesystemname, "Usage: /delfriendh playername")
                return
            name = str(args[0])
            ini = self.Wl()
            players = ini.EnumSection(id)
            if len(players) == 0:
                Player.MessageFrom(self.homesystemname, "You have never added anyone...")
                return
            name = name.lower()
            for playerid in players:
                nameof = ini.GetSetting(id, playerid)
                lowered = nameof.lower()
                if lowered == name:
                    ini.DeleteSetting(id, playerid)
                    ini.Save()
                    Player.MessageFrom(self.homesystemname, "Player Removed from Whitelist")
                    return
            Player.MessageFrom(self.homesystemname, "Couldn't find that player!")
        elif cmd == "listwlh":
            ini = self.Wl()
            players = ini.EnumSection(id)
            Player.MessageFrom(self.homesystemname, "Whitelisted Players:")
            if len(players) == 0:
                Player.MessageFrom(self.homesystemname, "You have never added anyone...")
                return
            for playerid in players:
                nameof = ini.GetSetting(id, playerid)
                Player.MessageFrom(self.homesystemname, "- " + nameof)

    def On_EntityDeployed(self, Player, Entity):
        if Entity is not None and Player is not None:
            config = self.HomeConfig()
            antihack = int(config.GetSetting("Settings", "Antihack"))
            if antihack == 1:
                if Entity.Name == "SleepingBagA":
                    inventory = Player.Inventory
                    Player.MessageFrom(self.homesystemname, "Sleeping bags are banned from this server!")
                    Player.MessageFrom(self.homesystemname, "Use /home")
                    Player.MessageFrom(self.homesystemname, "We disabled Beds, so players can't hack in your house!")
                    Player.MessageFrom(self.homesystemname, "You received 15 Cloth.")
                    Entity.Destroy()
                    inventory.AddItem("Cloth", 15)
                elif Entity.Name == "SingleBed":
                    inventory = Player.Inventory
                    Player.MessageFrom(self.homesystemname, "Beds are banned from this server!")
                    Player.MessageFrom(self.homesystemname, "Use /home")
                    Player.MessageFrom(self.homesystemname, "We disabled Beds, so players can't hack in your house!")
                    Player.MessageFrom(self.homesystemname, "You received 40 Cloth and 100 Metal Fragments.")
                    Entity.Destroy()
                    inventory.AddItem("Cloth", 40)
                    inventory.AddItem("Metal Fragments", 100)

    def On_PlayerHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Victim is not None:
            config = self.HomeConfig()
            checkdamage = int(config.GetSetting("Settings", "checkdamage"))
            if checkdamage == 0:
                return
            id = self.TrytoGrabID(HurtEvent.Attacker)
            if id is not None:
                vid = self.TrytoGrabID(HurtEvent.Victim)
                if self.isInjob(vid):
                    self.killJob(vid)
                    HurtEvent.Victim.MessageFrom(self.homesystemname, "Teleportation Cancelled. You received damage.")
                    DataStore.Remove("home_cooldown", vid)

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.DamageType is not None and DeathEvent.Victim is not None and DeathEvent.Attacker is not None:
            DataStore.Remove("homey", DeathEvent.Victim.SteamID)

    def On_PlayerSpawned(self, Player, SpawnEvent):
        id = Player.SteamID
        self.addJob(id, 2, None, 4)
        """camp = SpawnEvent.CampUsed
        if camp:
            #checkn = int(config.GetSetting("Settings", "safetpcheck"))
            cooldown = config.GetSetting("Settings", "Cooldown")
            time = DataStore.Get("home_cooldown", id)
            if time is None:
                time = 7
            calc = System.Environment.TickCount - time
            if calc < 0 or math.isnan(calc):
                DataStore.Add("home_cooldown", id, System.Environment.TickCount)
            if calc >= cooldown or time == 7:
                ini = self.Homes()
                check = ini.GetSetting("DefaultHome", id)
                if check is not None:
                    DataStore.Add("home_cooldown", id, System.Environment.TickCount)
                    home = self.HomeOf(Player, check)
                    home = Util.CreateVector(float(home[0]), float(home[1]), float(home[2]))
                    Player.SafeTeleportTo(home)
                    Player.MessageFrom(self.homesystemname, "Spawned at home!")"""

    def On_PlayerConnected(self, Player):
        id = self.TrytoGrabID(Player)
        if id is None:
            try:
                Player.Disconnect()
            except:
                pass
            return
        jtime = DataStore.Get("home_joincooldown", id)
        if jtime is None:
            if self.sendhome == 1:
                self.addJob(id, self.jointpdelay, None, 5)
            return
        if int(System.Environment.TickCount - jtime) < 0 or math.isnan(int(System.Environment.TickCount - jtime)):
            DataStore.Remove("home_joincooldown", id)
            if self.sendhome == 1:
                self.addJob(id, self.jointpdelay, None, 5)
            return
        if self.ecooldown == 1:
            calc = int(System.Environment.TickCount - (jtime + (self.cooldown * 1000)))
            if System.Environment.TickCount <= jtime + self.cooldown * 1000:
                calc2 = self.cooldown * 1000
                calc2 = round((calc2 - calc) / 1000 - self.cooldown, 2)
                Player.MessageFrom(self.homesystemname, red + str(self.cooldown) + " seconds cooldown at join. You can't join till: " + str(calc2) + " more seconds.")
                Player.Disconnect()
                return
            elif System.Environment.TickCount > jtime + (self.cooldown * 1000):
                DataStore.Remove("home_joincooldown", id)
                if self.sendhome == 1:
                    self.addJob(id, self.jointpdelay, None, 5)

    def On_PlayerDisconnected(self, Player):
        id = Player.SteamID
        config = self.HomeConfig()
        antiroof = int(config.GetSetting("Settings", "antiroofdizzy"))
        if antiroof == 1:
            if not Player.Admin and not self.isMod(id):
                DataStore.Add("homey", id, Player.Y)
        if self.ecooldown == 1:
            if not Player.Admin and not self.isMod(id):
                DataStore.Add("home_joincooldown", id, System.Environment.TickCount)
        DataStore.Add("homesystemautoban", id, "none")
        DataStore.Add("homey", id, Player.Y)
        Plugin.Log("assas", str(Player.Y))