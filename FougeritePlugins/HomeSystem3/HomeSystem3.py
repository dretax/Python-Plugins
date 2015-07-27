__author__ = 'DreTaX'
__version__ = '3.5.1'
import clr

clr.AddReferenceByPartialName("Fougerite")
clr.AddReferenceByPartialName("UnityEngine")
import Fougerite
import UnityEngine
from UnityEngine import *
import math
import System
from System import *

"""
    Class
"""

import sys
path = Util.GetRootFolder()
sys.path.append(path + "\\Save\\Lib\\")

try:
    import random
except ImportError:
    raise ImportError("Missing the Libs!")

red = "[color #FF0000]"
green = "[color #009900]"
white = "[color #FFFFFF]"
TimerStore = "HomeTimer"

class HomeSystem3:
    """
        Methods
    """
    sys = None
    cooldown = None
    sendhome = None
    ecooldown = None
    randomloc = None
    msg = None
    max = None
    rcooldown = None
    dizzycheck = None

    def On_PluginInit(self):
        self.PlayersIni()
        ini = self.Config()
        self.sys = ini.GetSetting("Settings", "SysName")
        self.cooldown = int(ini.GetSetting("Settings", "JoinCooldown"))
        self.sendhome = int(ini.GetSetting("Settings", "SendPlayertoHomeorRandom"))
        self.ecooldown = int(ini.GetSetting("Settings", "EJoinCooldown"))
        self.randomloc = int(ini.GetSetting("Settings", "Randoms"))
        self.dizzycheck = int(ini.GetSetting("Settings", "DizzyCheck"))
        self.msg = ini.GetSetting("Settings", "Message")
        self.max = float(ini.GetSetting("Settings", "Distance"))
        self.rcooldown = int(ini.GetSetting("Settings", "Cooldown"))
        DataStore.Flush("HomeSys3JCD")
        DataStore.Flush("HomeTimer")
        DataStore.Flush("HomeSys3CD")
        DataStore.Flush("homesystemautoban")
        DataStore.Flush("HomeSys3Loc")
        Util.ConsoleLog("HomeSystem3 by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def addJob(self, Player, xtime):
        List = Plugin.CreateDict()
        List["Player"] = Player
        Plugin.CreateParallelTimer("JobTimer", xtime * 1000, List).Start()

    def JobTimerCallback(self, timer):
        timer.Kill()
        List = timer.Args
        Player = List["Player"]
        id = Player.SteamID
        v = DataStore.Get("HomeSys3JCD", id)
        if v is None:
             return
        v = self.Replace(v)
        ini = self.DefaultLocations()
        y = float(Player.Y)
        v = float(v[1])
        if v - y > 2.4:
            r = random.randrange(1, self.randomloc)
            randomloc = ini.GetSetting("DefaultLoc", str(r))
            tp = self.Replace(randomloc)
            home = Util.CreateVector(float(tp[0]), float(tp[1]), float(tp[2]))
            Player.TeleportTo(home)
            Server.BroadcastFrom(self.sys, Player.Name + red + " tried to fall through a house.")
            Plugin.Log("DizzyHackBypass", Player.Name + " - " + Player.SteamID + " - " +
                        Player.IP + " - " + str(Player.Location))
        DataStore.Remove("HomeSys3JCD", id)

    def PlayersIni(self):
        if not Plugin.IniExists("Players"):
            ini = Plugin.CreateIni("Players")
            ini.Save()
        return Plugin.GetIni("Players")

    def Config(self):
        if not Plugin.IniExists("Config"):
            ini = Plugin.CreateIni("Config")
            ini.AddSetting("Settings", "Message", "No Derppassing ask the owner if you can live here")
            ini.AddSetting("Settings", "Distance", "25")
            ini.AddSetting("Settings", "SysName", "HomeSystem")
            ini.AddSetting("Settings", "EJoinCooldown", "0")
            ini.AddSetting("Settings", "JoinCooldown", "30")
            ini.AddSetting("Settings", "Cooldown", "300000")
            ini.AddSetting("Settings", "SendPlayertoHomeorRandom", "0")
            ini.AddSetting("Settings", "Randoms", "8156")
            ini.AddSetting("Settings", "DizzyCheck", "0")
            ini.Save()
        return Plugin.GetIni("Config")

    def argsToText(self, args):
        text = str.join(" ", args)
        return text

    def getPlayer(self, d):
        try:
            id = str(d)
            pl = Server.FindPlayer(id)
            return pl
        except:
            return None

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
            Player.MessageFrom(self.sys, "Couldn't find [color#00FF00]" + str.join(" ", args) + "[/color]!")
            return None
        elif count == 1 and p is not None:
            return p
        else:
            Player.MessageFrom(self.sys, "Found [color#FF0000]" + str(count) +
                               "[/color] player with similar name. [color#FF0000] Use more correct name!")
            return None

    def DefaultLocations(self):
        if not Plugin.IniExists("DefaultLoc"):
            ini = Plugin.CreateIni("DefaultLoc")
            ini.Save()
        return Plugin.GetIni("DefaultLoc")

    def TrytoGrabID(self, Player):
        try:
            id = Player.SteamID
            return id
        except:
            return None

    def Replace(self, String):
        c = String.replace("(", "")
        c = c.replace(")", "")
        return c.split(",")

    def HasHome(self, id):
        beds = self.PlayersIni()
        if beds.GetSetting("Homes", id) and beds.GetSetting("Homes", id) is not None:
            return True
        return False

    def IsFriend(self, OwnerID, ID):
        beds = self.PlayersIni()
        if beds.GetSetting(OwnerID, ID):
            return True
        return False

    def On_Command(self, Player, cmd, args):
        id = Player.SteamID
        beds = self.PlayersIni()
        if cmd == "home":
            Player.MessageFrom(self.sys, green + "HomeSystem3 " + white + " by " + __author__)
            Player.MessageFrom(self.sys, "/setdefaulthome - Sets home, If standing on a bed or bag.")
            Player.MessageFrom(self.sys, "/delhome - Deletes your Default Home")
            Player.MessageFrom(self.sys, "/addfriendh name - Adds Player To Foundation Whitelist")
            Player.MessageFrom(self.sys, "/delfriendh name - Removes Player From Foundation Whitelist")
            Player.MessageFrom(self.sys, "/listwlh - List Players On Distance Whitelist")
        elif cmd == "setdefaulthome":
            loc = Player.Location
            if not self.HasHome(id):
                for x in World.Entities:
                    name = x.Name.lower()
                    if "sleeping" in name:
                        dist = round(Util.GetVectorsDistance(loc, x.Location), 2)
                        if dist < 2:
                            ownerid = long(x.ownerID)
                            if long(id) == ownerid:
                                beds.AddSetting("Homes", id, str(loc))
                                beds.Save()
                                Player.MessageFrom(self.sys, "Home Set.")
                                return
                    elif "single" in name:
                        dist = round(Util.GetVectorsDistance(loc, x.Location), 2)
                        if dist < 3.5:
                            ownerid = long(x.ownerID)
                            if long(id) == ownerid:
                                beds.AddSetting("Homes", id, str(loc))
                                beds.Save()
                                Player.MessageFrom(self.sys, "Home Set.")
                                return
                Player.MessageFrom(self.sys, "Couldn't find a bed placed within 1m / 3.5m.")
                Player.MessageFrom(self.sys, "Stand on a bed or sleeping bag.")
                Player.MessageFrom(self.sys, red + "Make sure the bed is yours.")
            else:
                Player.MessageFrom(self.sys, "You already have a home. Delete It first.")
        elif cmd == "delhome":
            if self.HasHome(id):
                beds.DeleteSetting("Homes", id)
                beds.Save()
                Player.MessageFrom(self.sys, "Home Deleted")
            else:
                Player.MessageFrom(self.sys, "You don't have a home set.")
        elif cmd == "addfriendh":
            if len(args) == 0:
                Player.MessageFrom(self.sys, "Usage: /addfriendh playername")
            else:
                playerr = self.CheckV(Player, args)
                if playerr is None:
                    return
                if playerr == Player:
                    Player.MessageFrom(self.sys, "This is you...")
                    return
                idr = playerr.SteamID
                nrr = str(playerr.Name)
                if beds.GetSetting(id, idr) is not None:
                    Player.MessageFrom(self.sys, nrr + " is already on your list.")
                    return
                beds.AddSetting(id, idr, nrr)
                beds.Save()
                Player.MessageFrom(self.sys, nrr + " was added to your list.")
        elif cmd == "delfriendh":
            if len(args) == 0:
                Player.MessageFrom(self.sys, "Usage: /delfriendh playername")
                return
            elif len(args) > 0:
                name = self.argsToText(args)
                id = Player.SteamID
                players = beds.EnumSection(id)
                counted = len(players)
                if counted == 0:
                    Player.MessageFrom(self.sys, "You have never whitelisted anyone.")
                    return
                name = name.lower()
                for playerid in players:
                    nameof = beds.GetSetting(id, playerid)
                    lowered = nameof.lower()
                    if lowered == name or name in lowered:
                        beds.DeleteSetting(id, playerid)
                        beds.Save()
                        Player.MessageFrom(self.sys, str(nameof) + " Removed from Whitelist")
                        return
                Player.MessageFrom(self.sys, name + " is not on your list!")
        elif cmd == "listwlh":
            id = Player.SteamID
            players = beds.EnumSection(id)
            Player.MessageFrom(self.sys, green + " List of Whitelisted Friends:")
            for playerid in players:
                nameof = beds.GetSetting(id, playerid)
                if nameof:
                    Player.MessageFrom(self.sys, "- " + str(nameof))

    def HomeTimerCallback(self):
        epoch = Plugin.GetTimestamp()
        if DataStore.Count(TimerStore) >= 1:
            ids = DataStore.Keys(TimerStore)
            for id in ids:
                time = int(DataStore.Get(TimerStore, id))
                if epoch >= time:
                    if not self.HasHome(id):
                        Player = self.getPlayer(id)
                        if Player is None:
                            DataStore.Remove(TimerStore, id)
                            continue
                        self.SendRandom(Player)
                    else:
                        Player = self.getPlayer(id)
                        if Player is None:
                            DataStore.Remove(TimerStore, id)
                            continue
                        self.SendH(Player)
                    DataStore.Remove(TimerStore, id)
        else:
            Plugin.KillTimer("HomeTimer")

    def SendRandom(self, Player):
        id = Player.SteamID
        rand = random.randint(1, self.randomloc)
        deff = self.DefaultLocations()
        randp = deff.GetSetting("DefaultLoc", str(rand))
        randp = self.Replace(randp)
        location = Util.CreateVector(float(randp[0]), float(randp[1]), float(randp[2]))
        Player.TeleportTo(location)
        DataStore.Add("homesystemautoban", id, "none")
        Player.MessageFrom(self.sys, red + "Teleported to a random location.")
        Player.MessageFrom(self.sys, red + "Type /home to get the commands.")


    def SendH(self, Player):
        id = Player.SteamID
        time = DataStore.Get("HomeSys3CD", id)
        if time is None:
            DataStore.Add("HomeSys3CD", id, 7)
            time = 7
        systick = System.Environment.TickCount
        if int(systick - int(time)) < 0 or math.isnan(int(systick - int(time))) or math.isnan(time):
            DataStore.Add("HomeSys3CD", id, 7)
            time = 7
        calc = systick - int(time)
        if calc >= self.rcooldown or time == 7 or self.rcooldown == 0:
            beds = self.PlayersIni()
            h = beds.GetSetting("Homes", id)
            h = self.Replace(h)
            home = Util.CreateVector(float(h[0]), float(h[1]), float(h[2]))
            Player.SafeTeleportTo(home)
            DataStore.Add("homesystemautoban", id, "none")
            Player.MessageFrom(self.sys, green + "Teleported to your home.")
            DataStore.Add("HomeSys3CD", id, System.Environment.TickCount)
        else:
            Player.MessageFrom(self.sys, green + "Your home teleportation is on cooldown.")
            done = round((calc / 1000) / 60, 2)
            done2 = round((self.rcooldown / 1000) / 60, 2)
            Player.MessageFrom(self.sys, green + "Time: " + str(done) + "/" + str(done2))
            rand = random.randint(1, self.randomloc)
            deff = self.DefaultLocations()
            randp = deff.GetSetting("DefaultLoc", str(rand))
            randp = self.Replace(randp)
            location = Util.CreateVector(float(randp[0]), float(randp[1]), float(randp[2]))
            Player.TeleportTo(location)
            DataStore.Add("homesystemautoban", id, "none")
            Player.MessageFrom(self.sys, green + "Teleported to a random location.")

    def SendPlayerToHome(self, id):
        DataStore.Remove("HomeSys3JCD", id)
        if not Plugin.GetTimer("HomeTimer"):
            Plugin.CreateTimer("HomeTimer", 2000).Start()
        epoch = Plugin.GetTimestamp()
        exectime = int(epoch) + 12
        DataStore.Add("homesystemautoban", id, "using")
        DataStore.Add(TimerStore, id, exectime)

    def On_PlayerConnected(self, Player):
        id = Player.SteamID
        jtime = DataStore.Get("HomeSys3JCD", id)
        if self.sendhome == 1:
            if jtime is None:
                self.SendPlayerToHome(id)
                return
            if int(System.Environment.TickCount - jtime) < 0 or math.isnan(int(System.Environment.TickCount - jtime)):
                self.SendPlayerToHome(id)
                return
        if self.ecooldown == 1:
            calc = int(System.Environment.TickCount - (jtime + (self.cooldown * 1000)))
            if System.Environment.TickCount <= jtime + self.cooldown * 1000:
                calc2 = self.cooldown * 1000
                calc2 = round((calc2 - calc) / 1000 - self.cooldown, 2)
                Player.MessageFrom(self.sys, red + str(self.cooldown) +
                                   " seconds cooldown at join. You can't join till: " + str(calc2) + " more seconds.")
                Player.Disconnect()
                return
            elif System.Environment.TickCount > jtime + (self.cooldown * 1000):
                if self.sendhome == 1:
                    self.SendPlayerToHome(id)
        if self.dizzycheck == 1:
            DataStore.Add("HomeSys3CheckS", id, 1)
        DataStore.Remove("HomeSys3JCD", id)

    def On_PlayerSpawned(self, Player, SpawnEvent):
        if DataStore.ContainsKey("HomeSys3CheckS", Player.SteamID):
            DataStore.Remove("HomeSys3CheckS", Player.SteamID)
            self.addJob(Player, 1)

    def On_PlayerDisconnected(self, Player):
        id = Player.SteamID
        loc = Player.Location
        if Player.Admin or Player.Moderator:
            return
        if not DataStore.ContainsKey("HomeSys3JCD", id):
            DataStore.Add("HomeSys3JCD", id, System.Environment.TickCount)
        if str(loc) != "(0.0, 0.0, 0.0)":
            DataStore.Add("HomeSys3Loc", id, str(Player.Location))
        DataStore.Add("homesystemautoban", id, "none")

    def On_EntityDeployed(self, Player, Entity):
        if Entity is not None and Player is not None:
            if Entity.Name == "SleepingBagA" or Entity.Name == "SingleBed":
                id = Player.SteamID
                loc = Entity.Location
                for x in World.Entities:
                    if "foundation" in x.Name.lower() or "ceiling" in x.Name.lower():
                        dist = round(Util.GetVectorsDistance(loc, x.Location), 2)
                        if dist > self.max:
                            continue
                        ownerid = long(x.OwnerID)
                        if ownerid == long(id):
                            continue
                        friends = self.IsFriend(str(ownerid), id)
                        if friends:
                            continue
                        else:
                            Entity.Destroy()
                            Player.MessageFrom(self.sys, self.msg)
                            return