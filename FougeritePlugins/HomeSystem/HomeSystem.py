__author__ = 'DreTaX'
__version__ = '2.6.3'

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
    raise ImportError("Failed to import Random!")

red = "[color #FF0000]"
Pending = []


class HomeSystem:

    sendhome = None
    ecooldown = None
    jointpdelay = None
    cooldown = None
    homesystemname = None
    checkdamage = None
    antihack = None
    antiroof = None
    type = None
    movec = None
    found = None
    doubleteleport = None
    MaxHomes = None
    HomeCooldown = None
    TpDelay = None

    def On_PluginInit(self):
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
        self.checkdamage = int(config.GetSetting("Settings", "checkdamage"))
        self.antihack = int(config.GetSetting("Settings", "Antihack"))
        self.antiroof = int(config.GetSetting("Settings", "antiroofdizzy"))
        self.type = Util.TryFindReturnType("StructureComponent")
        self.movec = int(config.GetSetting("Settings", "movecheck"))
        self.doubleteleport = self.bool(config.GetSetting("Settings", "doubleteleport"))
        self.found = self.bool(config.GetSetting("Settings", "foundationhome"))
        self.MaxHomes = config.GetSetting("Settings", "Maxhomes")
        self.HomeCooldown = int(config.GetSetting("Settings", "Cooldown"))
        self.TpDelay = int(config.GetSetting("Settings", "tpdelay"))
        Util.ConsoleLog("HomeSystem" + " v" + __version__ + " by " + __author__ + " loaded.", True)

    """
        Functions
    """

    def bool(self, s):
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        else:
            raise ValueError

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
        if selfid == id:
            return True
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

    def DonatorRankCheck(self, type, id):
        if type == "MaxHomes":
            if DataStore.Get("DonatorRank-MaxHomes", id) is not None:
                maxh = DataStore.Get("DonatorRank-MaxHomes", id)
                return maxh
            return self.MaxHomes
        elif type == "CoolDown":
            if DataStore.Get("DonatorRank-Cooldown", id) is not None:
                CoolDown = DataStore.Get("DonatorRank-Cooldown", id)
                return (CoolDown / 60000) * 60
            return (self.HomeCooldown / 60000) * 60
        elif type == "TpDelay":
            if DataStore.Get("DonatorRank-TpDelay", id) is not None:
                TpDelay = DataStore.Get("DonatorRank-TpDelay", id)
                return TpDelay
            return self.TpDelay
        return self.MaxHomes

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
            Player.MessageFrom(self.homesystemname, "Found [color#FF0000]" + str(count)
                               + "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def Freezer(self, Player, num, msg=True):
        if Player not in Pending:
            return False
        if num == 1:
            Player.SendCommand("input.bind Up 7 None")
            Player.SendCommand("input.bind Down 7 None")
            Player.SendCommand("input.bind Left 7 None")
            Player.SendCommand("input.bind Right 7 None")
            Player.SendCommand("input.bind Sprint 7 None")
            Player.SendCommand("input.bind Duck 7 None")
            Player.SendCommand("input.bind Jump 7 None")
            Player.SendCommand("input.bind Fire 7 None")
            if msg:
                Player.MessageFrom(self.homesystemname, red + "You froze!")
        else:
            Player.SendCommand("input.bind Up W UpArrow")
            Player.SendCommand("input.bind Down S DownArrow")
            Player.SendCommand("input.bind Left A LeftArrow")
            Player.SendCommand("input.bind Right D RightArrow")
            Player.SendCommand("input.bind Sprint LeftShift RightShift")
            Player.SendCommand("input.bind Duck LeftControl RightControl")
            Player.SendCommand("input.bind Jump Space None")
            Player.SendCommand("input.bind Fire Mouse0 None")
            if msg:
                Player.MessageFrom(self.homesystemname, red + "You are now free!")
        return True

    """
        Timer Functions
    """

    def addJob(self, Player, xtime, callbacknumber, location):
        List = Plugin.CreateDict()
        List["Player"] = Player
        List["Call"] = callbacknumber
        List["house"] = location
        Plugin.CreateParallelTimer("JobTimer", xtime * 1000, List).Start()

    def clearTimers(self):
        Plugin.KillParallelTimer("JobTimer")


    """
        Events
    """

    def JobTimerCallback(self, timer):
        timer.Kill()
        config = self.HomeConfig()
        List = timer.Args
        Player = List["Player"]
        if not Player.IsOnline or Player not in Pending:
            return
        id = Player.SteamID
        callback = List["Call"]
        loc = List["house"]
        DataStore.Add("homesystemautoban", id, "using")
        # Join Callback, this should handle the delay
        if callback == 1:
            Player.TeleportTo(loc, True)
            Player.MessageFrom(self.homesystemname, "You have been teleported to your home.")
            Pending.remove(Player)
        # Home Teleport Callback
        elif callback == 2:
            if self.movec == 1:
                fr = self.Freezer(Player, 2)
                if not fr:
                    return
                Player.TeleportToTheClosestSpawnpoint(loc, False)
                Player.MessageFrom(self.homesystemname, "You have been teleported near home.")
                DataStore.Add("homey", id, loc.y)
                self.addJob(Player, 3, 1, loc)
            else:
                Player.TeleportToTheClosestSpawnpoint(loc)
                self.addJob(Player, 3, 1, loc)
                Player.MessageFrom(self.homesystemname, "You have been teleported near home.")
        # Random Teleportation Delay
        elif callback == 3:
            Player.TeleportTo(loc)
            Player.MessageFrom(self.homesystemname, "You have been teleported to a random location!")
            Player.MessageFrom(self.homesystemname, "Type /setdefaulthome HOMENAME")
            Player.MessageFrom(self.homesystemname, "To spawn at your home!")
        # dizzy heck.
        elif callback == 4:
            DataStore.Add("homesystemautoban", id, "none")
            v = DataStore.Get("homey", id)
            ini = self.DefaultLoc()
            if v is None:
                return
            y = float(Player.Y)
            v = float(v)
            if v - y > 2.6:
                randomloc = int(config.GetSetting("Settings", "randomlocnumber"))
                DataStore.Add("home_joincooldown", id, 7)
                r = random.randrange(1, randomloc)
                randomloc = ini.GetSetting("DefaultLoc", str(r))
                tp = self.Replace(randomloc)
                home = Util.CreateVector(float(tp[0]), float(tp[1]), float(tp[2]))
                Player.TeleportTo(home)
                Server.BroadcastFrom(self.homesystemname, Player.Name + red + " tried to fall through a house.")
                Plugin.Log("DizzyHackBypass", Player.Name + " - " + Player.SteamID + " - " + Player.IP + " - "
                           + str(Player.Location))
                DataStore.Remove("homey", id)
                #  self.addJob(Player, 2, 6, None)
        # Handles those players who joined after X seconds. Dizzy hack bypasser.
        elif callback == 5:
            randomloc = int(config.GetSetting("Settings", "randomlocnumber"))
            DataStore.Add("home_joincooldown", id, 7)
            r = random.randrange(1, randomloc)
            ini = self.Homes()
            getdfhome = ini.GetSetting("DefaultHome", id)
            if getdfhome is not None:
                home = loc
                w = 1
            else:
                ini2 = self.DefaultLoc()
                locc = ini2.GetSetting("DefaultLoc", str(r))
                tp = self.Replace(locc)
                home = Util.CreateVector(float(tp[0]), float(tp[1]), float(tp[2]))
                w = 3
            self.addJob(Player, 2, w, home)
        """elif callback == 6:
            try:
                Player.Disconnect()
            except:
                pass"""

    def Check(self, Player, plloc):
        config = self.HomeConfig()
        ini = self.Homes()
        id = Player.SteamID
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
                            if dist <= maxdist and not self.FriendOf(idof, id):
                                Player.MessageFrom(self.homesystemname, "There is a home within: " + str(maxdist)
                                                   + "m!")
                                return False
        if checkwall == 1:
            objects = UnityEngine.Object.FindObjectsOfType(self.type)
            for x in objects:
                if "Wall" in x.name:
                    distance = round(Util.GetVectorsDistance(x.gameObject.transform.position, plloc), 2)
                    if distance <= 1.50:
                        Player.MessageFrom(self.homesystemname, "You can't set home near walls!")
                        return False
        return True

    def SaveHome(self, Player, home, loc):
        ini = self.Homes()
        id = Player.SteamID
        homes = ini.GetSetting("HomeNames", id)
        if homes is not None and "," in homes:
            n = homes + "" + home + ","
            ini.AddSetting(id, home, str(loc))
            ini.AddSetting("HomeNames", id, n)
            ini.Save()
            Player.MessageFrom(self.homesystemname, "Home Saved")
            return
        n = home + ","
        ini.AddSetting(id, home, str(loc))
        ini.AddSetting("HomeNames", id, n)
        ini.Save()
        Player.MessageFrom(self.homesystemname, "Home Saved")

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
                Player.MessageFrom(self.homesystemname, "/hcanc - Cancels Home Teleportation")
            else:
                home = str(args[0])
                check = self.HomeOf(Player, home)
                if check is None:
                    Player.MessageFrom(self.homesystemname, "You don't have a home called: " + home)
                    return
                cooldown = int(self.DonatorRankCheck("CoolDown", id))
                # cooldown = int(self.DonatorRankCheck("CoolDown", id))
                time = DataStore.Get("home_cooldown", id)
                if time is None:
                    time = 7
                tpdelay = int(self.DonatorRankCheck("TpDelay", id))
                calc = (TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds - time)
                if calc >= cooldown or time == 7:
                    loc = Util.CreateVector(float(check[0]), float(check[1]), float(check[2]))
                    TimeP = TimeSpan.FromTicks(DateTime.Now.Ticks).TotalSeconds
                    if tpdelay == 0:
                        Player.TeleportToTheClosestSpawnpoint(loc)
                        Pending.append(Player)
                        self.addJob(Player, 2, 1, loc)
                        DataStore.Add("home_cooldown", id, TimeP)
                        Player.MessageFrom(self.homesystemname, "Teleported near home!")
                    else:
                        DataStore.Add("home_cooldown", id, TimeP)
                        Pending.append(Player)
                        self.addJob(Player, tpdelay, 2, loc)
                        Player.MessageFrom(self.homesystemname, "Teleporting you to home in: " + str(tpdelay)
                                           + " seconds")
                        movec = int(config.GetSetting("Settings", "movecheck"))
                        dmg = int(config.GetSetting("Settings", "checkdamage"))
                        if movec == 1:
                            Player.MessageFrom(self.homesystemname, red + "You can't move while teleporting.")
                            fr = self.Freezer(Player, 1)
                            if not fr:
                                return
                        if dmg == 1:
                            Player.MessageFrom(self.homesystemname, red + "You can't take damage while teleporting.")
                else:
                    Player.Notice("You have to wait before teleporting again!")
                    done = round(calc, 2)
                    done2 = round(cooldown, 2)
                    Player.MessageFrom(self.homesystemname, "Time: " + str(done) + " / " + str(done2))
        elif cmd == "sethome":
            if len(args) != 1:
                Player.MessageFrom(self.homesystemname, "Usage: /sethome name")
                return
            maxh = self.DonatorRankCheck("MaxHomes", id)
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
            if not self.found:
                s = self.Check(Player, plloc)
                if not s:
                    return
                vec = Util.CreateVector(float(plloc.x), float(plloc.y) + 5.0, float(plloc.z))
                self.SaveHome(Player, home, vec)
            else:
                DataStore.Add("HomeHit", id, home)
                Player.MessageFrom(self.homesystemname, red + "Hit a foundation/ceiling to save your home!")
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
            playerr = self.CheckV(Player, args)
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
        elif cmd == "hcanc":
            if Player not in Pending:
                Player.MessageFrom(self.homesystemname, "You are not teleporting.")
                return
            if self.movec == 1:
                self.Freezer(Player, 2)
            Pending.remove(Player)
            Player.MessageFrom(self.homesystemname, "Teleportation Cancelled!")


    def On_EntityDeployed(self, Player, Entity):
        if Entity is not None and Player is not None:
            if self.antihack == 1:
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
        if self.checkdamage == 0:
            return
        if HurtEvent.Attacker is not None and HurtEvent.Victim is not None \
            and HurtEvent.VictimIsPlayer and HurtEvent.AttackerIsPlayer:
                id = HurtEvent.Attacker.SteamID
                vid = HurtEvent.Victim.SteamID
                if id is not None and vid is not None:
                    if HurtEvent.Victim in Pending:
                        if self.movec == 1:
                            self.Freezer(HurtEvent.Victim, 2)
                        Pending.remove(HurtEvent.Victim)
                        HurtEvent.Victim.MessageFrom(self.homesystemname,
                                                     "Teleportation Cancelled. You received damage.")
                        DataStore.Remove("home_cooldown", vid)

    def On_PlayerKilled(self, DeathEvent):
        if DeathEvent.DamageType is not None and DeathEvent.Victim is not None and DeathEvent.Attacker is not None \
                and DeathEvent.VictimIsPlayer:
            vid = DeathEvent.Victim.SteamID
            if vid is None:
                return
            if self.antiroof == 1:
                DataStore.Remove("homey", vid)
            if DeathEvent.Victim in Pending:
                Pending.remove(DeathEvent.Victim)

    def On_PlayerSpawned(self, Player, SpawnEvent):
        id = Player.SteamID
        camp = SpawnEvent.CampUsed
        if self.antiroof == 1 and not camp:
            self.addJob(Player, 2, 4, None)
        if camp:
            config = self.HomeConfig()
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
                    Player.TeleportTo(home)
                    if self.antiroof == 1:
                        DataStore.Add("homey", id, float(home[1]))
                        self.addJob(Player, 2, 4, home)
                    Player.MessageFrom(self.homesystemname, "Spawned at home!")

    def On_EntityHurt(self, HurtEvent):
        if HurtEvent.Attacker is not None and HurtEvent.Entity is not None and not HurtEvent.IsDecay \
                and HurtEvent.AttackerIsPlayer:
            id = HurtEvent.Attacker.SteamID
            if DataStore.ContainsKey("HomeHit", id):
                HurtEvent.DamageAmount = 0
                name = DataStore.Get("HomeHit", id)
                if "Ceiling" in HurtEvent.Entity.Name or "Foundation" in HurtEvent.Entity.Name:
                    if self.FriendOf(HurtEvent.Entity.OwnerID, id):
                        DataStore.Remove("HomeHit", id)
                        vec = Util.CreateVector(float(HurtEvent.Entity.X), float(HurtEvent.Entity.Y) + 5.7,
                                                float(HurtEvent.Entity.Z))
                        self.SaveHome(HurtEvent.Attacker, name, vec)
                    else:
                        HurtEvent.Attacker.MessageFrom(self.homesystemname, red
                                                       + "You are not whitelisted for this foundation!")
                else:
                    HurtEvent.Attacker.MessageFrom(self.homesystemname, red
                                                   + "Hit a foundation/ceiling to save your home!")

    def On_PlayerConnected(self, Player):
        id = Player.SteamID
        jtime = DataStore.Get("home_joincooldown", id)
        if self.sendhome == 1:
            if jtime is None:
                self.addJob(Player, self.jointpdelay, 5, None)
                return
            if int(System.Environment.TickCount - jtime) < 0 or math.isnan(int(System.Environment.TickCount - jtime)):
                DataStore.Remove("home_joincooldown", id)
                self.addJob(Player, self.jointpdelay, 5, None)
                return
        if self.ecooldown == 1:
            calc = int(System.Environment.TickCount - (jtime + (self.cooldown * 1000)))
            if System.Environment.TickCount <= jtime + self.cooldown * 1000:
                calc2 = self.cooldown * 1000
                calc2 = round((calc2 - calc) / 1000 - self.cooldown, 2)
                Player.MessageFrom(self.homesystemname, red + str(self.cooldown)
                                   + " seconds cooldown at join. You can't join till: " + str(calc2) + " more seconds.")
                Player.Disconnect()
                return
            elif System.Environment.TickCount > jtime + (self.cooldown * 1000):
                DataStore.Remove("home_joincooldown", id)
                if self.sendhome == 1:
                    self.addJob(Player, self.jointpdelay, 5, None)
        if self.movec == 1:
            self.Freezer(Player, 2, False)

    def On_PlayerDisconnected(self, Player):
        id = Player.SteamID
        y = Player.Y
        if self.antiroof == 1:
            if not Player.Admin and not self.isMod(id):
                DataStore.Add("homey", id, y)
        if self.ecooldown == 1:
            if not Player.Admin and not self.isMod(id):
                DataStore.Add("home_joincooldown", id, System.Environment.TickCount)
        if Player in Pending:
            Pending.remove(Player)
        DataStore.Add("homesystemautoban", id, "none")
